# Resumen del piloto en español

Fecha local: 9 de noviembre de 2026. Estado: **completado; resultados de piloto, no del estudio final**.

## Alcance comprobado

GPU Tesla T4; PyTorch 2.14.1+cu130, Transformers 5.22.2, Datasets 5.1.0. Generador de 124439808 parámetros. Cinco ajustes; 64 ejemplos por ajuste, ocho actualizaciones y 8192 tokens objetivo; evaluación con 32 contextos y 4096 posiciones objetivo. Primeras 32 palabras para las métricas de diversidad. Sin textos cortos ni truncamientos del codificador.

## Métricas observadas

| Etapa | PPL de referencia | Distinct-2 | Distinct-3 | Repetición 4 | Dispersión semántica |
| --- | ---: | ---: | ---: | ---: | ---: |
| M0_human | 29.4677 | 0.9214 | 0.9885 | 0.0032 | 0.9123 |
| alpha_000_g1 | 29.1010 | 0.9375 | 0.9958 | 0.0000 | 0.8889 |
| alpha_000_g2 | 29.4150 | 0.9264 | 0.9927 | 0.0000 | 0.9077 |
| alpha_100_g1 | 30.4300 | 0.9204 | 0.9896 | 0.0032 | 0.9263 |
| alpha_100_g2 | 31.9012 | 0.9234 | 0.9896 | 0.0065 | 0.9043 |

La PPL de la cadena 100 % sintética pasa de 29.4677 a 31.9012 (+8.26 % frente a M0), mientras el control termina en 29.4150. La diversidad no presenta una caída sostenida. La repetición sigue siendo baja y cambia entre etapas. Una sola cadena por condición y dos ciclos no permiten afirmar colapso general, significación estadística ni confirmar la hipótesis.

Se inspeccionaron los primeros dos textos, por orden guardado, de cada una de las cinco etapas (diez extractos, hasta 300 caracteres). Predomina español, con incoherencias factuales y lingüísticas ya desde M0. No es evaluación humana sistemática ni verificación de todos los textos. El registro local detecta tres caracteres U+FFFD en total (dos en M0 y uno en control g1); se conservaron sin filtrar.

## Tiempo medido

Entre las marcas del manifiesto: 212.20 s. Suma de etapas: 210.97 s; ambos excluyen instalación y pruebas previas. Los tiempos incluyen la primera carga de recursos, no disponibilidad continua de GPU.

| Actividad | Segundos totales |
| --- | ---: |
| resolve_revisions | 0.44 |
| load_tokenizer_data | 56.17 |
| load_model | 11.20 |
| load_embeddings | 8.03 |
| reference_embeddings | 1.09 |
| fit | 49.68 |
| eval_generation | 45.39 |
| eval_perplexity | 3.31 |
| eval_embeddings | 4.35 |
| write_outputs | 0.01 |
| train_generation | 31.31 |

## Estimación orientativa para planear la escala final

La extrapolación lineal de 48 ajustes de 512 ejemplos, evaluación de 128 contextos por modelo y generación de 512 continuaciones en cada ciclo no humano (dos condiciones, cinco ciclos, tres réplicas) da aproximadamente 2.67 horas de esas tareas de cálculo. No es un tiempo validado: excluye interrupciones, nuevos controles, lectura/escritura adicional, preparación de la referencia final y posibles cambios de rendimiento con el tamaño. Solo orienta el presupuesto; el estudio completo no se ejecutó. El notebook actual sigue acotado al piloto.

## Archivos y comprobación

- [Notebook ejecutado](notebook_ejecutado.ipynb), 12 celdas de código ejecutadas y sin salidas de error.
- [ZIP original](resultados.zip) y [datos originales](datos/manifest.json).
- [Tabla CSV](datos/results.csv), [tiempos](datos/timings.json) y [métricas JSON](datos/results.json).
- [Gráfica](datos/pilot_metrics.png) y [captura de Colab](colab_resultados.png).
- [Comprobación local](comprobacion_local.json); repetible con py -3.12 Experimentos/verificar_resultados_es.py.

Se verificaron los registros del mismo hash inicial, optimizador vacío, ocho actualizaciones, presupuesto, particiones por artículo, contextos originales, mezclas 0/100 %, semillas y longitudes de generación; se recalcularon localmente Distinct-2/3 y repetición. No se repitieron entrenamiento, inferencia GPU, embeddings ni perplejidad desde pesos. No hay checkpoints guardados porque esa opción estaba desactivada.

El artículo no se modificó. Se debe armonizar su metodología en español y fijar la escala antes de ejecutar el estudio final; el conjunto de prueba permanece reservado.
