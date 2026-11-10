# Experimento principal en español

Preparado y comprobado localmente: **9 de noviembre de 2026**. El usuario aceptó preparar este notebook y armonizar el artículo. **El estudio principal no se ha ejecutado.**

Importar [experimento_principal_es.ipynb](experimento_principal_es.ipynb) en Colab. Es autónomo: 29 celdas con instalación, imports, controles, ejecución reanudable, resumen y exportación. El [piloto ejecutado](resultados/piloto_es_2026-11-09/RESUMEN.md) se conserva aparte.

## Diseño preparado

| Elemento | Configuración v1 |
| --- | --- |
| Generador | `datificate/gpt2-small-spanish`, 124 439 808 parámetros; ajuste completo |
| Corpus | `wikimedia/wikipedia`, `20231101.es`; prefijo de 2000 artículos |
| Partición | SHA-256 de semilla `20261109` e ID: aproximadamente 80/10/10; misma regla del piloto |
| Muestra | 512 entrenamiento, 128 validación, 128 prueba; una ventana por artículo |
| Ventana | Contexto original de 64 tokens y objetivo de 128 |
| Condiciones | 0, 50 y 100 % de objetivos sintéticos; contextos originales en todas |
| Ciclos y repeticiones | Cinco ciclos, tres repeticiones; M0 compartido dentro de cada repetición: 48 ajustes |
| Inicialización | Siempre pesos preentrenados y optimizador nuevo, no ajuste acumulativo del checkpoint anterior |
| Presupuesto por ajuste | Una época, 65 536 tokens objetivo, lote efectivo 8 y 64 actualizaciones |
| Mezcla | En 50 %, las mismas 256 posiciones sintéticas dentro de cada repetición; se generan 512 objetivos antes de mezclar |
| Generación | 128 tokens excluyendo IDs especiales; temperatura 1, top-p .95, RNG por solicitud |
| Métricas | Distinct-2/3, repetición de 4-gramas, dispersión MiniLM multilingüe y PPL sobre referencia original de prueba |
| Longitud léxica | W fijada solo con validación, hasta 32 palabras; no se filtran textos según calidad o idioma |

Las revisiones del generador, corpus y codificador están fijadas en el código a las usadas en el piloto. La reserva de prueba del piloto no se tokenizó entonces; el principal sí la prepara y selecciona 128 ejemplos para su evaluación. Se conservan la partición y las ventanas por artículo para impedir que referencias usadas en entrenamiento/validación del piloto pasen a prueba. No se garantiza ausencia de solapamiento con el preentrenamiento del generador ni autoría humana de todo Wikipedia.

Se guardan resultados de prueba por etapa, pero el notebook muestra el resumen conjunto al finalizar, sin adaptar el protocolo a esas métricas. La unidad de repetición es la cadena de entrenamiento, no cada texto. El resumen ofrece medias, rangos y contrastes pareados descriptivos; tres repeticiones no justifican por sí solas inferencias generales.

## Primera ejecución y continuación

1. Importar el notebook en una sesión limpia de Colab con GPU. Ejecutar instalación y controles en orden. La prueba diminuta de Safetensors comprueba guardado/restauración antes del estudio.
2. Revisar `OUTPUT_ROOT`, por defecto `/content/drive/MyDrive/IMAC/estudio_principal_es_v1`. Activar `PREPARE_DRIVE=True` y completar personalmente el montaje. El montaje concede acceso de Drive al runtime; no se ha realizado en esta preparación.
3. Activar `RUN_EXPERIMENT=True` y conservar **`MAX_NEW_STAGES=1`**. Ejecutar la celda de controles de ejecución y luego la de entrenamiento. Se prepara el conjunto final y se completa una etapa.
4. Comprobar en Drive los archivos de esa etapa. Repetir la celda de entrenamiento con la misma carpeta y configuración: debe omitir la etapa confirmada y avanzar a la siguiente. En una nueva sesión deben ejecutarse antes las dependencias y definiciones.
5. Una vez comprobada la reanudación, `MAX_NEW_STAGES=None` permite continuar lo restante. No ejecutar dos sesiones sobre la misma carpeta. Al terminar las 48 etapas se habilita resumen y descarga del ZIP sin pesos.

Las banderas se distribuyen en `False`; «Ejecutar todas» así no monta Drive ni inicia ajustes. Sí instala paquetes y ejecuta controles diminutos. La instalación se detiene si Transformers/Datasets ya están importados: usar una sesión limpia en ese caso.

## Qué se conserva y cómo se reanuda

- `protocol.json` congela configuración, huella de código y entorno esencial. Una diferencia de versiones, Python, CUDA o GPU impide mezclar ejecuciones en la misma carpeta. Los mismos valores no garantizan identidad numérica entre máquinas.
- `data/` conserva particiones, tokens y metadatos. `stages/` conserva corpus, semillas, registros del ajuste, generaciones, métricas y marcador `complete.json` con hashes.
- Los lotes de generación se guardan individualmente y se reutilizan solo si coinciden sus entradas y hashes. Los JSON se escriben primero como pendientes y luego se reemplazan; esto no constituye una garantía de transacción distribuida de Drive.
- Un ajuste interrumpido antes de guardar `fit.json` se repite desde la base con su misma semilla. Un ajuste guardado puede continuar su evaluación. **No se restaura el optimizador a mitad de época.**
- Los checkpoints propios usan Safetensors. Se conservan los M0 y el último checkpoint necesario. Los pesos no iniciales anteriores se eliminan únicamente después de confirmar la etapa sucesora; los datos y métricas se mantienen. No borrar manualmente el checkpoint padre de una etapa pendiente.
- Reservar al menos unos **3 GB para pesos y archivos**, con margen adicional; es una estimación, no una medición del estudio completo. Aunque los pesos antiguos se purguen, escribir 48 checkpoints supone alrededor de 24 GB acumulados de transferencias. Su costo en Drive aún no se midió.
- Los tiempos registran actividades terminadas; el trabajo interrumpido antes de guardar el tiempo no queda contabilizado. La extrapolación del piloto de unas 2.67 h excluye checkpoints, Drive e interrupciones y no garantiza la duración principal.

El ZIP final incluye resultados, contrastes, protocolo y registros, sin pesos ni cachés de lotes. Guardar también el notebook ejecutado desde Colab; no reemplazar la fuente local sin conservar antes sus salidas.

## Verificación y fuentes

Pasaron **20 pruebas locales** y las mismas 20 embebidas en el notebook; se verificaron sintaxis, autonomía, IDs únicos, salidas vacías y banderas de ejecución desactivadas. Las pruebas cubren calendario de 48 ajustes, particiones y duplicados, mezcla, semillas, métricas léxicas, persistencia, incompatibilidades y corrupción de archivos. El artículo se armonizó y compiló.

El flujo nuevo de 48 ajustes, el montaje de Drive y el guardado/restauración PyTorch de este notebook **siguen pendientes de ejecución integrada**. No hay PyTorch local. Los componentes de entrenamiento heredados sí pasaron el piloto en T4; eso no verifica el flujo principal completo. Detalles y revisión proporcional de seguridad en [VERIFICACION.md](VERIFICACION.md).

Fuentes oficiales consultadas el 9 de noviembre: [generador](https://huggingface.co/datificate/gpt2-small-spanish), [corpus](https://huggingface.co/datasets/wikimedia/wikipedia), [codificador](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), [Safetensors](https://huggingface.co/docs/safetensors/main/en/api/torch) y [límites de Colab](https://research.google.com/colaboratory/faq.html).

Fuentes locales: `principal_colab_es.py`, `estado_principal_es.py`, `test_estado_principal_es.py`, `crear_principal_es.py` y funciones del piloto. Para regenerar la **fuente sin salidas**: `py -3.12 Experimentos/crear_principal_es.py`. No ejecutar ese generador sobre una copia que contenga resultados sin archivarla primero.
