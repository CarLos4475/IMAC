# Bitácora del piloto en español

Fecha de trabajo: 9 de noviembre de 2026, America/Mexico_City.

## Entorno y preparación observados en Colab

- Notebook: `piloto_model_collapse_es.ipynb`, importado por el usuario.
- URL de trabajo: `https://colab.research.google.com/drive/1pJDpzWt50eXbPqe2rrUMSM9943hHGep9`.
- Al conectar se mostró «Demasiadas sesiones». El usuario informó que cerró todas; se comprobó «No hay sesiones activas» y se reconectó un entorno nuevo con GPU T4.
- La instalación de dependencias finalizó en esta sesión.
- Los 13 controles del protocolo pasaron en Colab (salida observada: `Ran 13 tests ... OK`).
- Diagnóstico observado: `PyTorch: 2.14.1+cu130 | Dispositivo: cuda`, `GPU: Tesla T4`.
- Las comprobaciones del GPT-2 diminuto de pesos aleatorios pasaron: pérdida causal, relleno, muestreo reproducible y reinicio de pesos/optimizador. Son controles de código, no resultados del experimento.
- Directorio de ejecución mostrado: `/content/imac_piloto_es/20261110T022838Z_1db7b1f0`. El nombre usa UTC y por eso comienza el 10 de noviembre; la fecha local de trabajo es el día 9.

## Estado final

**Piloto completado y archivado:** cinco ajustes, 32 generaciones de evaluación por etapa y dos corpus sintéticos de 64 continuaciones. El manifiesto indica `complete`, `fit_count: 5`, `test_used: false`, `language: es`. La ejecución registrada por el manifiesto duró 212.20 segundos, sin contar instalación ni controles previos; la suma de etapas cronometradas fue 210.97 segundos. No se inició el estudio final.

Los resultados originales del ZIP se extrajeron en [resultados/piloto_es_2026-11-09/datos](resultados/piloto_es_2026-11-09/datos). También se conservan el ZIP, el notebook ejecutado y una captura. La comprobación local pasó: particiones, presupuestos, semillas, mezclas y recomputación de métricas léxicas. Perplejidad y embeddings no se recalcularon localmente; sus valores proceden de Colab. Véase el [resumen](resultados/piloto_es_2026-11-09/RESUMEN.md).

## Observaciones de ejecución

- Se examinaron 2000 artículos; el código informó 1461 candidatos de entrenamiento y 202 de validación. Los conjuntos seleccionados se guardan por el protocolo, con 64/32 ejemplos.
- La carga del generador y del codificador terminó, igual que M0 y ambos ciclos de las dos condiciones. El notebook exportado contiene las 12 celdas de código ejecutadas y no contiene salidas de error.
- Apareció un aviso por claves `transformer.h.{0...11}.attn.masked_bias` inesperadas. Se contrastó la implementación original [Transformers 3.5.1](https://huggingface.co/transformers/v3.5.1/_modules/transformers/modeling_gpt2.html), que registra `masked_bias` como buffer escalar, con [GPT-2 en Transformers 5.22.2](https://raw.githubusercontent.com/huggingface/transformers/v5.22.2/src/transformers/models/gpt2/modeling_gpt2.py), que ya no lo registra. Se interpreta como un buffer legado, no como un parámetro entrenable faltante; el reporte observado no indicó claves faltantes de pesos. No se modificaron pesos ni bibliotecas por ese aviso.
- El aviso de solicitudes sin autenticación a Hugging Face no se trató como instrucción para crear o introducir claves; las descargas públicas continuaron sin ellas.
