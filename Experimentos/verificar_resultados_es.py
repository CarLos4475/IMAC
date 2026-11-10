"""Comprueba los artefactos descargados del piloto; no vuelve a entrenar ni usa red."""
import hashlib
import json
import math
from pathlib import Path
from controles import stable_seed
from controles_es import lexical_metrics, article_partition

ROOT = Path(__file__).resolve().parent/'resultados'/'piloto_es_2026-11-09'
DATA = ROOT/'datos'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def check_artifacts():
    manifest, results = read_json(DATA/'manifest.json'), read_json(DATA/'results.json')
    cfg = manifest['config']
    assert manifest['status'] == 'complete' and manifest['fit_count'] == 5
    assert manifest['test_used'] is False and cfg['language'] == 'es'
    assert cfg['train_examples'] == 64 and cfg['eval_examples'] == 32
    train, valid = read_rows(DATA/'train_human.jsonl'), read_rows(DATA/'validation_human.jsonl')
    assert len(train) == 64 and len(valid) == 32
    assert {r['article'] for r in train}.isdisjoint(r['article'] for r in valid)
    assert {r['text_sha256'] for r in train}.isdisjoint(r['text_sha256'] for r in valid)
    assert all(article_partition(r['article'], cfg['seed']) == 'train' for r in train)
    assert all(article_partition(r['article'], cfg['seed']) == 'validation' for r in valid)
    original = {r['id']: r for r in train}
    reports, eval_seeds = [], None
    expected_names = {'M0_human', 'alpha_000_g1', 'alpha_000_g2', 'alpha_100_g1', 'alpha_100_g2'}
    assert {r['stage'] for r in results} == expected_names
    for result in results:
        name = result['stage']
        fit = read_json(DATA/name/'fit.json')
        assert fit['initial_weight_sha256'] == manifest['base_weight_sha256']
        assert fit['optimizer_initial_entries'] == 0
        assert fit['updates'] == 8 and fit['target_tokens_seen'] == 8192
        assert fit['train_seed'] == stable_seed(cfg['seed'], 'fit', 'replicate_0', result['cycle'])
        assert fit['final_weight_sha256'] != fit['initial_weight_sha256']
        corpus = read_rows(DATA/name/'training_corpus.jsonl')
        assert len(corpus) == 64 and {r['id'] for r in corpus} == set(original)
        for row in corpus:
            assert row['context'] == original[row['id']]['context']
            assert len(row['target']) == 128
            if not result['alpha']:
                assert row['target'] == original[row['id']]['target']
        count_synthetic = sum(bool(r.get('synthetic', False)) for r in corpus)
        assert count_synthetic == (64 if result['alpha'] == 1 else 0)
        if result['alpha'] == 1:
            synthetic = read_rows(DATA/f'{name}_synthetic.jsonl')
            by_id = {r['id']: r for r in synthetic}
            assert len(by_id) == 64 and set(by_id) == set(original)
            assert all(r['target'] == by_id[r['id']]['target_ids'] for r in corpus)
            namespace = f'train_alpha_{result["alpha"]}_cycle_{result["cycle"]}'
            assert all(r['seed'] == stable_seed(cfg['seed'], 'sampling', namespace, r['id'])
                       for r in synthetic)
        generations = read_rows(DATA/name/'validation_generations.jsonl')
        assert len(generations) == 32
        assert [g['id'] for g in generations] == [r['id'] for r in valid]
        seeds = [g['seed'] for g in generations]
        assert seeds == [stable_seed(cfg['seed'], 'sampling', 'validation_paired', r['id']) for r in valid]
        if eval_seeds is None:
            eval_seeds = seeds
        assert seeds == eval_seeds
        forbidden = set(manifest['forbidden_generation_ids'])
        assert all(len(g['target_ids']) == 128 and not (set(g['target_ids']) & forbidden) for g in generations)
        metrics = lexical_metrics([g['text'] for g in generations], manifest['word_limit'])
        for key in ('distinct_2', 'distinct_3', 'repeat_4_mean'):
            assert math.isclose(metrics[key], result[key], abs_tol=1e-12)
        assert result['short_texts'] == metrics['short_texts'] == 0
        assert result['embedding_truncated_texts'] == 0
        assert result['ppl_target_tokens'] == 4096
        assert math.isclose(result['human_perplexity'], math.exp(result['human_nll']), abs_tol=1e-12)
        assert math.isfinite(result['semantic_dispersion']) and 0 <= result['semantic_dispersion'] <= 2
        reports.append({'stage': name, 'updates': fit['updates'], 'target_tokens': fit['target_tokens_seen'],
                        'synthetic_examples': count_synthetic, 'eval_texts': len(generations),
                        'replacement_characters_in_text': sum(g['text'].count('\ufffd') for g in generations),
                        'checks': 'passed'})
    times = read_json(DATA/'timings.json')
    assert all(x['status'] == 'ok' and x['seconds'] >= 0 for x in times)
    assert sum(x['stage'] == 'fit' for x in times) == 5
    notebook = read_json(ROOT/'notebook_ejecutado.ipynb')
    assert sum(c['cell_type'] == 'code' and c.get('execution_count') is not None for c in notebook['cells']) == 12
    assert not any(o.get('output_type') == 'error' for c in notebook['cells'] for o in c.get('outputs', []))
    output = {'status': 'passed', 'run': DATA.name, 'fits': reports,
              'timed_seconds': sum(x['seconds'] for x in times),
              'archive_sha256': hashlib.sha256((ROOT/'resultados.zip').read_bytes()).hexdigest(),
              'not_recomputed': ['training', 'GPU inference', 'embeddings', 'perplexity from weights'],
              'checks': ['metadata', 'article partitions', 'initial weights/optimizer logs',
                         'budgets', 'contexts', 'exact synthetic mixture', 'sampling seeds',
                         'generated token lengths', 'lexical metrics recomputed', 'timings',
                         'executed notebook without error outputs']}
    (ROOT/'comprobacion_local.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    check_artifacts()
