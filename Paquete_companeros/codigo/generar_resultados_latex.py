#!/usr/bin/env python3
"""Genera tablas y figura LaTeX del estudio principal a partir de results.csv.

Uso:
    python generar_resultados_latex.py CARPETA_CON_results.csv [--salida RUTA] [--ciclo-final 5]

Solo calcula medias, rangos y diferencias descriptivas. No calcula p-valores ni
afirma efectos: la interpretación se redacta aparte, con los datos a la vista.
La carpeta de entrada debe contener results.csv (y, si existe, contrasts.csv).
Los .tex generados se pueden incluir con \\input{...}; no editar a mano.
"""
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

METRICS = [
    ('human_perplexity', 'Perplejidad sobre referencias originales', '{:.2f}'),
    ('distinct_2', 'Distinct-2', '{:.4f}'),
    ('distinct_3', 'Distinct-3', '{:.4f}'),
    ('repeat_4_mean', 'Repetición media de 4-gramas', '{:.4f}'),
    ('semantic_dispersion', 'Dispersión semántica', '{:.4f}'),
]
ALPHAS = (0.0, 0.5, 1.0)
LABEL_ALPHA = {0.0: '0\\,\\%', 0.5: '50\\,\\%', 1.0: '100\\,\\%'}
NUMERIC = {m for m, _, _ in METRICS} | {'human_nll', 'ppl_target_tokens', 'word_limit',
           'n_texts', 'short_texts', 'embedding_truncated_texts', 'rep', 'cycle', 'alpha'}


def read_rows(path):
    rows = []
    with Path(path).open(encoding='utf-8', newline='') as stream:
        for raw in csv.DictReader(stream):
            row = {}
            for key, value in raw.items():
                if key in NUMERIC:
                    row[key] = None if value in ('', 'None', 'nan') else float(value)
                else:
                    row[key] = value
            rows.append(row)
    return rows


def verify(rows):
    """Controles de integridad. Devuelve (lista de problemas, dict de hechos)."""
    problems = []
    if len(rows) != 48:
        problems.append(f'Se esperaban 48 filas y hay {len(rows)}.')
    reps = sorted({int(r['rep']) for r in rows})
    if reps != [0, 1, 2]:
        problems.append(f'Repeticiones encontradas: {reps}; se esperaban [0, 1, 2].')
    for rep in reps:
        mine = [r for r in rows if int(r['rep']) == rep]
        if sum(int(r['cycle']) == 0 for r in mine) != 1:
            problems.append(f'Repetición {rep}: debe haber exactamente un M0.')
        for alpha in ALPHAS:
            cycles = sorted(int(r['cycle']) for r in mine if r['alpha'] == alpha)
            if cycles != [1, 2, 3, 4, 5]:
                problems.append(f'Repetición {rep}, alfa {alpha}: ciclos {cycles}.')
    missing = [(r['stage'], m) for r in rows for m, _, _ in METRICS if r.get(m) is None]
    if missing:
        problems.append(f'Métricas ausentes en {len(missing)} casos: {missing[:6]}...')
    facts = {
        'textos_cortos_total': sum(int(r['short_texts'] or 0) for r in rows),
        'truncamientos_codificador_total': sum(int(r['embedding_truncated_texts'] or 0) for r in rows),
        'longitudes_lexicas_W': sorted({int(r['word_limit']) for r in rows if r['word_limit']}),
        'textos_por_etapa': sorted({int(r['n_texts']) for r in rows if r['n_texts']}),
    }
    return problems, facts


def values(rows, metric, alpha, cycle):
    if cycle == 0:
        picked = [r for r in rows if int(r['cycle']) == 0]
    else:
        picked = [r for r in rows if int(r['cycle']) == cycle and r['alpha'] == alpha]
    return [r[metric] for r in sorted(picked, key=lambda r: r['rep'])]


def fmt(fmt_str, value):
    return 'n/d' if value is None else fmt_str.format(value)


def summary(vals, fmt_str):
    if not vals or any(v is None for v in vals):
        return 'n/d'
    # Modo matemático: el signo menos se compone correctamente y el rango no genera guiones largos.
    return (f"${fmt_str.format(statistics.fmean(vals))}$ "
            f"[${fmt_str.format(min(vals))}$; ${fmt_str.format(max(vals))}$]")


NOTE = ''  # Texto opcional añadido a todas las leyendas (--nota).

HEADER = ('% Generado por Experimentos/generar_resultados_latex.py desde {origin}.\n'
          '% No editar a mano: volver a ejecutar el script.\n')


def table_means(rows, metric, title, fmt_str, origin):
    lines = [HEADER.format(origin=origin),
             '\\begin{table}[ht]', '\\centering', '\\footnotesize',
             '\\begin{tabular}{c c c c}', '\\hline',
             'Ciclo & $\\alpha=0$ & $\\alpha=0.5$ & $\\alpha=1$ \\\\', '\\hline']
    m0 = summary(values(rows, metric, None, 0), fmt_str)
    lines.append(f'0 ($M_0$) & \\multicolumn{{3}}{{c}}{{{m0}}} \\\\')
    for cycle in range(1, 6):
        cells = [summary(values(rows, metric, a, cycle), fmt_str) for a in ALPHAS]
        lines.append(f'{cycle} & ' + ' & '.join(cells) + ' \\\\')
    lines += ['\\hline', '\\end{tabular}',
              f'\\caption{{{title}: media y rango [mínimo; máximo] de las tres cadenas '
              'por ciclo y proporción sintética $\\alpha$. $M_0$ es compartido por las '
              f'tres proporciones dentro de cada repetición.{NOTE}}}',
              f'\\label{{tab:medias_{metric}}}', '\\end{table}', '']
    return '\n'.join(lines)


def deltas(rows, metric, alpha, cycle, against):
    out = []
    for rep in sorted({int(r['rep']) for r in rows}):
        pick = lambda c, a: next((r[metric] for r in rows if int(r['rep']) == rep
                                  and int(r['cycle']) == c and (c == 0 or r['alpha'] == a)), None)
        now = pick(cycle, alpha)
        ref = pick(0, None) if against == 'M0' else pick(cycle, 0.0)
        out.append(None if now is None or ref is None else now - ref)
    return out


SHORT = {'human_perplexity': 'Perplejidad', 'repeat_4_mean': 'Repetición de 4-gramas'}


def table_contrasts(rows, cycle, origin):
    lines = [HEADER.format(origin=origin),
             '\\begin{table}[ht]', '\\centering', '\\footnotesize',
             '\\resizebox{\\textwidth}{!}{%', '\\begin{tabular}{l c c c c}', '\\hline',
             'Métrica & $\\alpha$ & $\\Delta$ frente a $M_0$ & $\\Delta$ frente al control & '
             'Cadenas con $\\Delta>0$ \\\\', '\\hline']
    for metric, title, fmt_str in METRICS:
        signed = fmt_str.replace('{:', '{:+')
        for alpha in (0.5, 1.0):
            d0 = deltas(rows, metric, alpha, cycle, 'M0')
            dc = deltas(rows, metric, alpha, cycle, 'control')
            pos = 'n/d' if any(v is None for v in dc) else f'{sum(v > 0 for v in dc)}/{len(dc)}'
            lines.append(f'{SHORT.get(metric, title)} & {LABEL_ALPHA[alpha]} & {summary(d0, signed)} & '
                         f'{summary(dc, signed)} & {pos} \\\\')
        lines.append('\\hline')
    lines += ['\\end{tabular}}',
              f'\\caption{{Diferencias descriptivas en el ciclo {cycle}: media y rango de las tres '
              'cadenas. $\\Delta$ frente a $M_0$ compara con el punto inicial de la misma repetición; '
              '$\\Delta$ frente al control compara con la condición $\\alpha=0$ del mismo ciclo y '
              f'repetición. No se calculan pruebas de significación.{NOTE}}}',
              f'\\label{{tab:contrastes_ciclo{cycle}}}', '\\end{table}', '']
    return '\n'.join(lines)


def figure(rows, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.5))
    for ax, (metric, title, _) in zip(axes.flat, METRICS):
        for alpha in ALPHAS:
            mean, low, high = [], [], []
            for cycle in range(6):
                v = values(rows, metric, alpha, cycle)
                if not v or any(x is None for x in v):
                    mean.append(float('nan')); low.append(float('nan')); high.append(float('nan'))
                else:
                    mean.append(statistics.fmean(v)); low.append(min(v)); high.append(max(v))
            ax.plot(range(6), mean, marker='o', label=f'{alpha:.0%}')
            ax.fill_between(range(6), low, high, alpha=.15)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel('Ciclo')
        ax.grid(alpha=.3)
    axes.flat[0].legend(title='Objetivos sintéticos', fontsize=8)
    axes.flat[-1].axis('off')
    fig.tight_layout()
    fig.savefig(path.with_suffix('.pdf'), bbox_inches='tight')
    fig.savefig(path.with_suffix('.png'), dpi=200, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('entrada', type=Path, help='Carpeta que contiene results.csv')
    parser.add_argument('--salida', type=Path, default=Path(__file__).resolve().parents[1] / 'Manuscrito' / 'resultados_generados')
    parser.add_argument('--ciclo-final', type=int, default=5)
    parser.add_argument('--nota', default='', help='Texto añadido al final de cada leyenda')
    args = parser.parse_args()
    global NOTE
    NOTE = (' ' + args.nota) if args.nota else ''
    rows = read_rows(args.entrada / 'results.csv')
    problems, facts = verify(rows)
    args.salida.mkdir(parents=True, exist_ok=True)
    origin = str(args.entrada.name)
    for metric, title, fmt_str in METRICS:
        (args.salida / f'tabla_medias_{metric}.tex').write_text(
            table_means(rows, metric, title, fmt_str, origin), encoding='utf-8')
    (args.salida / 'tabla_contrastes.tex').write_text(
        table_contrasts(rows, args.ciclo_final, origin), encoding='utf-8')
    figure(rows, args.salida / 'figura_trayectorias')
    numeric = {m: {f'a{int(a*100):03d}': {str(c): values(rows, m, a, c) for c in range(6)} for a in ALPHAS}
               for m, _, _ in METRICS}
    report = {'origen': origin, 'problemas': problems, 'hechos': facts, 'valores_por_cadena': numeric}
    (args.salida / 'verificacion_y_valores.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Problemas de integridad:', problems or 'ninguno')
    print('Hechos:', facts)
    print('Archivos escritos en', args.salida)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
