"""Análisis complementario post hoc (no preregistrado) del estudio principal.

Motivo: la regla del protocolo deja ausentes las métricas léxicas y semánticas
de una etapa si al menos una de sus 128 continuaciones tiene menos de W palabras.
Esto ocurrió en 39 de 48 etapas. Este script NO sustituye el resultado
preregistrado: recalcula las métricas léxicas sobre el subconjunto común de
contextos de prueba cuyas continuaciones alcanzan W palabras en las 48 etapas,
de modo que todas las etapas se comparan con el mismo número de textos y los
mismos contextos. Usa exactamente las funciones de métricas del notebook.

Uso: python analisis_complementario_es.py CARPETA_EXTRAIDA
Escribe results_complementario.csv y subconjunto_comun.json en esa carpeta.
"""
import csv, json, sys
from pathlib import Path
from controles_es import words, lexical_metrics

root = Path(sys.argv[1])
rows = list(csv.DictReader(open(root/'results.csv', encoding='utf-8')))
W = int(rows[0]['word_limit'])
gens = {}
for r in rows:
    data = json.load(open(root/'stages'/r['stage']/'test_generations.json', encoding='utf-8'))
    gens[r['stage']] = {g['id']: g['text'] for g in data}
ids = sorted(next(iter(gens.values())))
assert all(sorted(g) == ids for g in gens.values()), 'IDs de prueba distintos entre etapas'
common = [i for i in ids if all(len(words(g[i])) >= W for g in gens.values())]
short_any = len(ids) - len(common)
out = []
for r in rows:
    texts = [gens[r['stage']][i] for i in common]
    m = lexical_metrics(texts, W)
    assert m['short_texts'] == 0
    out.append({'stage': r['stage'], 'rep': r['rep'], 'cycle': r['cycle'], 'alpha': r['alpha'],
                'human_perplexity': r['human_perplexity'], 'word_limit': W,
                'n_texts': m['n_texts'], 'short_texts_full_set': r['short_texts'],
                'distinct_2': m['distinct_2'], 'distinct_3': m['distinct_3'],
                'repeat_4_mean': m['repeat_4_mean']})
with open(root/'results_complementario.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)
json.dump({'word_limit': W, 'n_test_contexts': len(ids), 'n_common': len(common),
           'excluded_contexts': short_any, 'common_ids': common},
          open(root/'subconjunto_comun.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('W', W, 'contextos', len(ids), 'comunes', len(common))
