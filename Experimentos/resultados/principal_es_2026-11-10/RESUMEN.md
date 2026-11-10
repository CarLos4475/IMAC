# Estudio principal en español — resultados (10 de noviembre de 2026)

## Ejecución
- Notebook `Experimentos/experimento_principal_es.ipynb` (SOURCE_SHA256 `42531e6e…5c624`) ejecutado en una copia de Colab, Tesla T4, Drive `MyDrive/IMAC/estudio_principal_es_v1`.
- 48/48 etapas confirmadas; `finished.json` con hora de fin 2026-11-10T07:33:28Z. Una reanudación (la sesión principal empezó con 2/48 etapas ya hechas). `timings.json` suma 10 145 s (~2.8 h) de actividad registrada.
- Firma del protocolo `85e3dd5d…12156`; entorno: Python 3.13.16, torch 2.14.1+cu130, transformers 5.22.2, CUDA 13.0.

## Archivos
- `original/resultados_sin_pesos.zip`: ZIP descargado por la celda de resumen (SHA-256 `b7a3d616ea35ac856bb1adf54eb212645e34ea3effbbf068083c5116119a3612`). Sin pesos.
- `extraido/`: contenido del ZIP (results.csv/json, contrasts, results.png, protocol, data, stages con textos de prueba) + archivos del análisis complementario (`results_complementario.csv`, `subconjunto_comun.json`, `textos_subconjunto_comun.json`, `semantica_complementaria.csv`).
- `complementario/results.csv`: perplejidad original + métricas léxicas y semánticas del análisis complementario (90 contextos).
- `verificacion_preregistrada/`: salida de `generar_resultados_latex.py` sobre el results.csv original (registra las 156 métricas ausentes).
- Tablas/figura usadas en el artículo: `Manuscrito/resultados_generados/` (perplejidad desde `preregistrado/`).

## Incidencia importante
La regla preregistrada (si una de las 128 continuaciones tiene < W = 30 palabras, la etapa queda sin métricas léxicas y semánticas) dejó sin esas métricas a 39 de 48 etapas. 75 de 6 144 continuaciones fueron cortas: M0 2, α=0 19, α=0.5 16, α=1 38. Muchas contienen saltos de línea o símbolos repetidos.

Análisis complementario post hoc (decidido después de ver los faltantes): 90 contextos de prueba que alcanzan W en las 48 etapas; métricas léxicas con las mismas funciones (`Experimentos/analisis_complementario_es.py`, local) y dispersión semántica con la misma revisión del codificador, calculada con una celda temporal añadida al final de la copia de Colab (descargó `semantica_complementaria.csv`). Excluye 38 contextos, probablemente los más degradados.

## Resultados principales (media de 3 cadenas; ciclo 5)
| Métrica | M0 | α=0 | α=0.5 | α=1 |
|---|---|---|---|---|
| Perplejidad (128 contextos) | 30.46 | 30.47 | 31.90 | 39.30 |
| Distinct-2 (90) | 0.913 | 0.905 | 0.896 | 0.825 |
| Distinct-3 (90) | 0.990 | 0.985 | 0.984 | 0.940 |
| Repetición 4-gramas (90) | 0.003 | 0.004 | 0.005 | 0.035 |
| Dispersión semántica (90) | 0.883 | 0.890 | 0.898 | 0.903 |

- α=1: perplejidad +8.83 (~+29 %) creciente en cada ciclo; diversidad léxica baja y repetición sube; 3/3 cadenas en la misma dirección.
- α=0.5: perplejidad +1.44 (~+4.7 %), estable desde el ciclo 1-2; cambios léxicos pequeños e inconsistentes.
- α=0: estable.
- Dispersión semántica: no disminuye; ligero aumento en todas las condiciones.
Análisis descriptivo, sin p-valores.
