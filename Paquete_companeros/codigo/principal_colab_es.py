"""Estudio principal. Preparado para Colab; no ejecutar al importar."""
from controles import stable_seed, mix_targets, WORD_PATTERN
from controles_es import normalized_text, article_partition, words, lexical_metrics
from estado_principal_es import canonical_hash, file_hash, atomic_json, make_plan, freeze_protocol, commit_stage, stage_complete, final_selection, cached_chunk, save_chunk
from piloto_colab_es import Config as PilotConfig, seed_training, weight_hash, cpu_state, fit_one, sample_targets, torch_smoke_checks, human_perplexity, semantic_dispersion

# %% Configuración del estudio principal
import csv
import gc
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import random
import shutil
import sys
import time
from dataclasses import dataclass, asdict, replace
from datetime import datetime, timezone
from pathlib import Path
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from safetensors.torch import save_model, load_model
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class MainConfig(PilotConfig):
    train_examples: int = 512
    eval_examples: int = 128
    validation_examples: int = 128
    repetitions: int = 3
    save_checkpoints: bool = True
    cycles: int = 5
    alphas: tuple = (0.0, 0.5, 1.0)
    split_seed: int = 20261109  # Conserva las particiones del piloto.
    seed: int = 20261109
    model_revision: str = '02e3092372e8a8b20c64e29350a024a998a7c00d'
    dataset_revision: str = 'b04c8d1ceb2f5cd4588862100d08de323dccfbaa'
    embedding_revision: str = 'e8f8c211226b894fcb81acc59f3b34ba3efd5f42'


MAIN_CFG = MainConfig()


def read_record(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def environment_record():
    names = ('torch', 'transformers', 'datasets', 'safetensors', 'numpy', 'tokenizers', 'huggingface-hub')
    return {'python': platform.python_version(),
            'packages': {n: importlib.metadata.version(n) for n in names},
            'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu',
            'cuda': torch.version.cuda, 'cudnn': torch.backends.cudnn.version()}


def check_main_config(cfg, output_root):
    if sys.version_info < (3, 11) or tuple(int(x) for x in torch.__version__.split('+')[0].split('.')[:2]) < (2, 6):
        raise RuntimeError('Se requiere Python >=3.11 y PyTorch >=2.6.')
    if (cfg.language != 'es' or cfg.subset != '20231101.es' or cfg.train_examples != 512
            or cfg.eval_examples != 128 or cfg.validation_examples != 128
            or cfg.repetitions != 3 or cfg.cycles != 5 or cfg.alphas != (0.0, .5, 1.0)):
        raise ValueError('La configuración difiere del protocolo principal preparado.')
    if cfg.split_seed != 20261109:
        raise ValueError('No cambiar las particiones utilizadas en el piloto.')
    if not torch.cuda.is_available():
        raise RuntimeError('Se requiere GPU CUDA para esta configuración.')
    if cfg.effective_batch % cfg.micro_batch or cfg.train_examples % cfg.effective_batch:
        raise ValueError('Presupuesto y acumulación incompatibles.')
    # En Colab se exige persistencia en Drive: /content desaparece con la sesión.
    root = Path(output_root).resolve()
    if Path('/content').exists() and not root.is_relative_to(Path('/content/drive/MyDrive')):
        raise ValueError('Usar la carpeta persistente de MyDrive preparada en el notebook.')
    if Path('/content').exists() and not Path('/content/drive/MyDrive').is_dir():
        raise RuntimeError('Google Drive aún no está montado; completar esa celda manualmente.')


class MainClock:
    def __init__(self, root):
        self.root = root

    def measure(self, name, action):
        torch.cuda.synchronize()
        start = time.perf_counter()
        result = action()
        torch.cuda.synchronize()
        records = read_record(self.root/'timings.json') if (self.root/'timings.json').exists() else []
        records.append({'activity': name, 'seconds': time.perf_counter()-start,
                        'recorded_utc': datetime.now(timezone.utc).isoformat()})
        atomic_json(self.root/'timings.json', records)
        return result

# %% Preparación y reanudación
def prepare_main_data(root, cfg, tokenizer, signature):
    folder = root/'data'
    if stage_complete(folder, signature):
        return read_record(folder/'corpus.json'), read_record(folder/'metadata.json')
    pools = {s: [] for s in ('train', 'validation', 'test')}
    counts = {s: 0 for s in pools}
    seen = set()
    stream = load_dataset(cfg.dataset, cfg.subset, split='train', streaming=True,
                           revision=cfg.dataset_revision, token=False)
    width = cfg.context_tokens + cfg.target_tokens
    for number, article in enumerate(stream):
        if number >= cfg.article_pool:
            break
        identity = str(article['id'])
        if identity in seen:
            raise ValueError('ID de artículo duplicado en el corpus.')
        seen.add(identity)
        split = article_partition(identity, cfg.split_seed)
        counts[split] += 1
        text = normalized_text(article['text'])
        ids = tokenizer(text, add_special_tokens=False, truncation=False, verbose=False)['input_ids']
        windows_count = len(ids)//width
        if not windows_count:
            continue
        offset = random.Random(stable_seed(cfg.split_seed, 'window', identity)).randrange(windows_count)*width
        block = ids[offset:offset+width]
        pools[split].append({'id': f'es:{split}:{identity}:{offset}', 'split': split,
            'article': identity, 'title': article.get('title', ''), 'url': article.get('url', ''),
            'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'offset': offset,
            'context': block[:cfg.context_tokens], 'target': block[cfg.context_tokens:]})
    selected = final_selection(pools, (cfg.train_examples, cfg.validation_examples, cfg.eval_examples), cfg.seed)
    # Se fija longitud exclusivamente con validación, nunca con resultados de prueba.
    validation = tokenizer.batch_decode([r['target'] for r in selected['validation']], skip_special_tokens=True)
    limit = min(cfg.max_words, min(len(words(t)) for t in validation))
    if limit < 4:
        raise ValueError('Validación no permite longitud léxica común suficiente.')
    metadata = {'word_limit': limit, 'scanned_articles': len(seen), 'split_counts': counts,
        'eligible_counts': {k: len(v) for k, v in pools.items()}, 'corpus_sha256': canonical_hash(selected),
        'split_seed': cfg.split_seed, 'test_used_for_tuning': False,
        'normalization': 'NFC; minúsculas solo en métricas; tildes y ñ conservadas'}
    atomic_json(folder/'corpus.json', selected)
    atomic_json(folder/'metadata.json', metadata)
    commit_stage(folder, signature, ['corpus.json', 'metadata.json'], {'kind': 'data_prepared'})
    return selected, metadata


def save_checkpoint(model, folder):
    pending, target = folder/'model.pending.safetensors', folder/'model.safetensors'
    save_model(model, str(pending))
    pending.replace(target)
    return file_hash(target)


def restore_checkpoint(model, folder, device='cuda'):
    record = read_record(folder/'fit.json')
    path = folder/'model.safetensors'
    if not path.is_file() or file_hash(path) != record['checkpoint_sha256']:
        raise ValueError(f'Checkpoint necesario ausente o modificado: {folder.name}')
    load_model(model, str(path), strict=True, device=device)
    if weight_hash(model) != record['final_weight_sha256']:
        raise ValueError('Los pesos restaurados no coinciden con la huella registrada.')
    model.eval()


def sampled_batches(model, rows, cfg, tokenizer, namespace, folder, signature, producer_hash):
    folder.mkdir(parents=True, exist_ok=True)
    generated = []
    for start in range(0, len(rows), cfg.sample_batch):
        chunk = rows[start:start+cfg.sample_batch]
        path = folder/f'batch_{start:05d}.json'
        input_hash = canonical_hash({'signature': signature, 'namespace': namespace, 'producer': producer_hash,
                                      'rows': chunk, 'seed': cfg.seed})
        outputs = cached_chunk(path, input_hash)
        if outputs is None:
            ids, seeds = sample_targets(model, chunk, cfg, 'cuda', tokenizer.all_special_ids,
                                         namespace, progress=False)
            outputs = [{'id': r['id'], 'seed': s, 'target_ids': t,
                        'text': tokenizer.decode(t, skip_special_tokens=True)}
                       for r, s, t in zip(chunk, seeds, ids)]
            save_chunk(path, input_hash, outputs)
        if len(outputs) != len(chunk) or [x['id'] for x in outputs] != [x['id'] for x in chunk]:
            raise ValueError('Lote guardado incompleto.')
        for row, output in zip(chunk, outputs):
            if (len(output['target_ids']) != cfg.target_tokens
                    or set(output['target_ids']) & set(tokenizer.all_special_ids)
                    or output['seed'] != stable_seed(cfg.seed, 'sampling', namespace, row['id'])):
                raise ValueError('Longitud o semilla de lote inválida.')
        generated.extend(outputs)
    return generated


def prune_previous_checkpoints(root, current, signature):
    # Solo pesos creados por este programa, de etapas completas no iniciales.
    # Se llama DESPUÉS de verificar y confirmar el sucesor completo.
    for job in make_plan():
        folder = root/'stages'/job['id']
        if folder == current or folder.name.endswith('_M0'):
            continue
        checkpoint = folder/'model.safetensors'
        if checkpoint.is_file() and stage_complete(folder, signature):
            checkpoint.unlink()

# %% Ejecución principal protegida
def run_main(cfg, output_root, code_sha256, max_new_stages=None):
    check_main_config(cfg, output_root)
    if max_new_stages is not None and (not isinstance(max_new_stages, int) or max_new_stages < 1):
        raise ValueError('El límite de etapas debe ser positivo o None.')
    root = Path(output_root).resolve()
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.benchmark = False
    environment = environment_record()
    signature = freeze_protocol(root, {'config': asdict(cfg), 'code_sha256': code_sha256,
        'eos_policy': '128 tokens sin IDs especiales', 'word_pattern': WORD_PATTERN,
        'mixture_policy': 'subset sintético fijo por repetición/alpha; generar 512 antes de mezclar'}, environment)
    clock = MainClock(root)
    jobs = make_plan(cfg.repetitions, cfg.cycles, cfg.alphas)
    completed = [job for job in jobs if stage_complete(root/'stages'/job['id'], signature)]
    if len(completed) == len(jobs):
        atomic_json(root/'finished.json', {'status': 'complete', 'stages': len(jobs), 'signature': signature})
        print('Las 48 etapas ya están completas; no se vuelve a entrenar.')
        return root
    torch_smoke_checks()
    print('Entorno:', environment['gpu'], '| Etapas completas:', len(completed), '/', len(jobs), flush=True)
    tokenizer = AutoTokenizer.from_pretrained(cfg.model, revision=cfg.model_revision,
                                              token=False, trust_remote_code=False)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    data, metadata = clock.measure('prepare_data', lambda: prepare_main_data(root, cfg, tokenizer, signature))
    model = clock.measure('load_generator', lambda: AutoModelForCausalLM.from_pretrained(
        cfg.model, revision=cfg.model_revision, token=False, trust_remote_code=False,
        use_safetensors=False, weights_only=True, dtype=torch.float32,
        attn_implementation='eager').to('cuda'))
    model.config.pad_token_id = tokenizer.pad_token_id
    if not all(p.requires_grad for p in model.parameters()):
        raise RuntimeError('El ajuste debe actualizar todos los parámetros.')
    base, base_hash = cpu_state(model), weight_hash(model)
    model_record = root/'base_model.json'
    if model_record.exists() and read_record(model_record)['weight_hash'] != base_hash:
        raise ValueError('Los pesos preentrenados cambiaron respecto a la ejecución guardada.')
    atomic_json(model_record, {'weight_hash': base_hash, 'parameters': sum(p.numel() for p in model.parameters())})
    enc_tokenizer = AutoTokenizer.from_pretrained(cfg.embedding, revision=cfg.embedding_revision,
                                                 token=False, trust_remote_code=False)
    encoder = clock.measure('load_encoder', lambda: AutoModel.from_pretrained(cfg.embedding,
        revision=cfg.embedding_revision, token=False, trust_remote_code=False,
        use_safetensors=True, dtype=torch.float32).cpu().eval())
    new_count = 0
    for job in jobs:
        folder = root/'stages'/job['id']
        if stage_complete(folder, signature):
            continue
        folder.mkdir(parents=True, exist_ok=True)
        local_cfg = replace(cfg, seed=stable_seed(cfg.seed, 'replicate', job['rep']))
        print('Procesando:', job['id'], flush=True)
        if (folder/'fit.json').exists():
            restore_checkpoint(model, folder)  # Ajuste terminado; evaluación pendiente.
        else:
            if (folder/'training_corpus.json').exists() and (folder/'corpus_record.json').exists():
                corpus = read_record(folder/'training_corpus.json')
                corpus_record = read_record(folder/'corpus_record.json')
                if corpus_record != {'signature': signature, 'sha256': canonical_hash(corpus)}:
                    raise ValueError('Corpus parcial incompatible o modificado.')
            else:
                synthetic = None
                if job['alpha']:
                    parent = root/'stages'/job['parent']
                    if not stage_complete(parent, signature):
                        raise ValueError('El modelo padre no tiene una etapa completa.')
                    restore_checkpoint(model, parent)
                    outputs = clock.measure(job['id']+'/train_generation', lambda: sampled_batches(
                        model, data['train'], local_cfg, tokenizer,
                        f"train_a{job['alpha']}_g{job['cycle']}", folder/'train_batches', signature,
                        read_record(parent/'fit.json')['final_weight_sha256']))
                    synthetic = [row['target_ids'] for row in outputs]
                mixture_seed = stable_seed(cfg.seed, 'mixture', job['rep'], job['alpha'])
                corpus = mix_targets(data['train'], synthetic, job['alpha'] or 0.0, mixture_seed)
                atomic_json(folder/'training_corpus.json', corpus)
                atomic_json(folder/'corpus_record.json', {'signature': signature, 'sha256': canonical_hash(corpus)})
            if (len(corpus) != cfg.train_examples
                    or [x['id'] for x in corpus] != [x['id'] for x in data['train']]
                    or [x['context'] for x in corpus] != [x['context'] for x in data['train']]
                    or any(len(x['target']) != cfg.target_tokens for x in corpus)
                    or sum(x['synthetic'] for x in corpus) != round((job['alpha'] or 0)*cfg.train_examples)):
                raise ValueError('El corpus guardado no respeta el presupuesto o la mezcla.')
            if any(not row['synthetic'] and row['target'] != original['target']
                   for row, original in zip(corpus, data['train'])):
                raise ValueError('Objetivo original cambiado en el corpus guardado.')
            fit_seed = stable_seed(cfg.seed, 'fit', job['rep'], job['cycle'])
            fit = clock.measure(job['id']+'/fit', lambda: fit_one(model, base, base_hash,
                corpus, local_cfg, fit_seed, 'cuda', tokenizer.pad_token_id))
            fit['corpus_sha256'] = canonical_hash(corpus)
            fit['checkpoint_sha256'] = clock.measure(job['id']+'/checkpoint', lambda: save_checkpoint(model, folder))
            atomic_json(folder/'fit.json', fit)
        fit = read_record(folder/'fit.json')
        if fit['corpus_sha256'] != canonical_hash(read_record(folder/'training_corpus.json')):
            raise ValueError('El corpus del ajuste guardado cambió.')
        samples = clock.measure(job['id']+'/test_generation', lambda: sampled_batches(model,
            data['test'], local_cfg, tokenizer, 'test_paired', folder/'test_batches', signature,
            fit['final_weight_sha256']))
        texts = [row['text'] for row in samples]
        metrics = clock.measure(job['id']+'/test_ppl', lambda: human_perplexity(model,
            data['test'], local_cfg, 'cuda', tokenizer.pad_token_id))
        metrics.update(lexical_metrics(texts, metadata['word_limit']))
        metrics.update(clock.measure(job['id']+'/embeddings', lambda: semantic_dispersion(
            texts, encoder, enc_tokenizer, local_cfg, metadata['word_limit'])))
        metrics.update(stage=job['id'], rep=job['rep'], cycle=job['cycle'], alpha=job['alpha'])
        atomic_json(folder/'test_generations.json', samples)
        atomic_json(folder/'metrics.json', metrics)
        commit_stage(folder, signature, ['training_corpus.json', 'corpus_record.json', 'fit.json', 'test_generations.json', 'metrics.json'], job)
        assert stage_complete(folder, signature)
        prune_previous_checkpoints(root, folder, signature)
        new_count += 1
        print('Etapa confirmada:', job['id'], '(métricas guardadas; resumen al finalizar)', flush=True)
        if max_new_stages is not None and new_count >= max_new_stages:
            print('Límite voluntario de etapas alcanzado. Reanudar con la misma carpeta/configuración.')
            return root
    atomic_json(root/'finished.json', {'status': 'complete', 'stages': len(jobs),
        'signature': signature, 'finished_utc': datetime.now(timezone.utc).isoformat()})
    print('Estudio principal completo: 48 etapas. Puede ejecutar el resumen.')
    return root

# %% Resumen del estudio principal
def summarize_main(root):
    root = Path(root)
    protocol = read_record(root/'protocol.json')
    signature = protocol['signature']
    plan = make_plan()
    if not all(stage_complete(root/'stages'/job['id'], signature) for job in plan):
        raise RuntimeError('El resumen de prueba se muestra al completar las 48 etapas.')
    rows = [read_record(root/'stages'/job['id']/'metrics.json') for job in plan]
    with (root/'results.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    atomic_json(root/'results.json', rows)
    keys = ['distinct_2', 'distinct_3', 'repeat_4_mean', 'semantic_dispersion', 'human_perplexity']
    contrasts = []
    for row in rows:
        if row['alpha'] not in (.5, 1.0):
            continue
        initial = next(r for r in rows if r['rep'] == row['rep'] and r['cycle'] == 0)
        control = next(r for r in rows if r['rep'] == row['rep'] and r['cycle'] == row['cycle'] and r['alpha'] == 0)
        contrast = {k: row[k] for k in ('rep', 'cycle', 'alpha')}
        for metric in keys:
            contrast[metric+'_vs_M0'] = None if row[metric] is None or initial[metric] is None else row[metric]-initial[metric]
            contrast[metric+'_vs_control'] = None if row[metric] is None or control[metric] is None else row[metric]-control[metric]
        contrasts.append(contrast)
    atomic_json(root/'contrasts.json', contrasts)
    with (root/'contrasts.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(contrasts[0]))
        writer.writeheader(); writer.writerows(contrasts)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for ax, metric in zip(axes.flat, keys):
        for alpha in (0.0, .5, 1.0):
            means, lows, highs = [], [], []
            for cycle in range(6):
                values = [r[metric] for r in rows if r['cycle'] == cycle
                          and (cycle == 0 or r['alpha'] == alpha)]
                if any(v is None for v in values):
                    means.append(float('nan')); lows.append(float('nan')); highs.append(float('nan'))
                else:
                    means.append(sum(values)/len(values)); lows.append(min(values)); highs.append(max(values))
            ax.plot(range(6), means, marker='o', label=f'{alpha:.0%}')
            ax.fill_between(range(6), lows, highs, alpha=.12)
        ax.set(title=metric, xlabel='Ciclo'); ax.grid(alpha=.3)
    axes.flat[0].legend(title='Objetivos sintéticos')
    axes.flat[-1].axis('off')
    fig.suptitle('Estudio principal: media y rango de tres cadenas; sin p-valores')
    fig.tight_layout()
    fig.savefig(root/'results.png', dpi=160, bbox_inches='tight')
    plt.show()
    # Exportación ligera: excluye checkpoints, lotes parciales y directorios ajenos.
    import zipfile
    archive = root/'resultados_sin_pesos.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as target:
        for name in ('protocol.json', 'base_model.json', 'finished.json', 'timings.json',
                     'results.csv', 'results.json', 'results.png', 'contrasts.csv', 'contrasts.json'):
            if (root/name).exists():
                target.write(root/name, name)
        for folder in [root/'data']+[root/'stages'/job['id'] for job in plan]:
            for path in folder.glob('*.json'):
                target.write(path, path.relative_to(root))
    print('Resumen y exportación sin pesos:', archive)
    return archive
