# Piloto en Colab

**Estudio principal preparado el 9 de noviembre:** [experimento_principal_es.ipynb](experimento_principal_es.ipynb), autónomo y reanudable; ver [README_PRINCIPAL_ES.md](README_PRINCIPAL_ES.md). No ejecutado: 20 controles offline/embebidos pasaron; primera etapa limitada a un ajuste y banderas de ejecución desactivadas.

**Piloto vigente:** [piloto_model_collapse_es.ipynb](piloto_model_collapse_es.ipynb), ya ejecutado con cinco ajustes; consultar [README_ES.md](README_ES.md) y sus [resultados archivados](resultados/piloto_es_2026-11-09/RESUMEN.md). Esta página conserva debajo las instrucciones históricas de la versión inglesa, interrumpida durante imports; no continuar esa copia ni confundirla con el principal.

Subir **[piloto_model_collapse.ipynb](piloto_model_collapse.ipynb)** a [Google Colab](https://colab.research.google.com/) mediante **Archivo → Subir notebook**. Elegir un entorno con GPU y ejecutar las celdas en orden. Solo hace falta subir ese archivo: incluye instalación, imports, funciones, controles y descarga del ZIP de resultados.

No requiere claves de API ni montar Drive. No contrata recursos. Si la instalación solicita reiniciar el runtime, reiniciarlo antes de continuar con imports. El código conserva el PyTorch del entorno y exige Python >=3.11, PyTorch >=2.6 y GPU CUDA por defecto. Para un uso deliberado de CPU existe `allow_cpu=True`; su duración no está comprobada.

## Alcance

- OPT-125m, WikiText-2 raw en inglés; ajuste completo, una época.
- 64 bloques humanos de entrenamiento y 32 de validación, sin cargar `test`.
- Contextos de 64 tokens y objetivos de 128; contextos humanos fijos.
- M0 humano y dos ciclos por proporción (0 y 100 %): **cinco ajustes**.
- Cada ajuste restaura los pesos preentrenados y crea un optimizador nuevo.
- AdamW, tasa 2e-5, lote efectivo 8; ocho actualizaciones y 8192 tokens objetivo por ajuste.
- Generación con temperatura 1 y top-p .95, sin top-k; un RNG por solicitud.
- Propuesta operativa para EOS: excluir todos los tokens especiales y generar exactamente 128 tokens. Debe revisarse después del piloto y declararse si se conserva.
- Distinct-2/3, repetición de 4-gramas, dispersión MiniLM y perplejidad sobre referencias humanas de validación.

Para comparar longitudes se fija un límite común de hasta 32 palabras a partir de las referencias de validación antes de generar. Una etapa con textos más cortos informa el problema y deja ausentes sus métricas léxicas/semánticas, sin excluir textos silenciosamente. La perplejidad usa las 128 posiciones objetivo completas.

Este es un piloto de viabilidad. No ejecuta el estudio final de 48 ajustes y sus trayectorias no permiten inferencia estadística ni prueban por sí solas colapso. Los detalles añadidos por el código son propuestas del agente para este piloto, no decisiones finales del usuario o del profesor. El artículo no se modificó.

## Qué entrega una ejecución

La carpeta `/content/imac_piloto/<fechaUTC_identificador>/` contiene:

- `manifest.json`: configuración, dispositivo, versiones, commits, política de generación, estado de ejecución y huellas del corpus/pesos.
- `train_human.jsonl`, `validation_human.jsonl`: IDs, offsets y tokens seleccionados.
- Archivos `*_synthetic.jsonl`: datos sintéticos y semillas que alimentan las siguientes generaciones.
- Una carpeta por ajuste con corpus utilizado, registro de reinicio/entrenamiento, muestras de validación y métricas.
- `results.csv`, `results.json`, `timings.json`, referencia humana y `pilot_metrics.png`.
- Un ZIP al terminar, descargable desde la última celda.

Por defecto **no guarda checkpoints** para evitar varios GB. Se puede activar `save_checkpoints=True` antes de ejecutar. Se conserva la información necesaria para repetir el cálculo, pero no se garantiza identidad entre hardware/versiones diferentes. Una interrupción conserva archivos parciales; no hay reanudación automática y ejecutar de nuevo crea otra carpeta. Descargar los archivos antes de cerrar el runtime: `/content` es temporal.

## Archivos de desarrollo y comprobaciones

| Archivo | Función |
| --- | --- |
| `piloto_model_collapse.ipynb` | Entrega autónoma para Colab. |
| `piloto_colab.py` | Procedimientos de carga, ajuste, muestreo, evaluación y archivos. |
| `controles.py` | Preparación del corpus, etiquetas, mezcla, semillas y métricas léxicas; solo biblioteca estándar. |
| `test_controles.py` | Siete controles de protocolo ejecutables sin GPU ni descargas. |
| `crear_notebook.py` | Regenera el notebook embebiendo las fuentes; no necesita Jupyter. |
| `PLAN.md` | Alcance y orden de implementación. |
| `VERIFICACION.md` | Evidencia real y límites de comprobación. |

Desde la raíz del proyecto:

```powershell
py -3.12 -m unittest discover -s Experimentos -v
py -3.12 Experimentos/crear_notebook.py
py -3.12 -m py_compile Experimentos/controles.py Experimentos/piloto_colab.py
```

Si se modifican las fuentes, regenerar el notebook. Al regenerarlo se vacían las salidas; conservar por separado cualquier copia ejecutada que se quiera archivar.

## Si aparece un error

Sin GPU, seleccionar GPU y ejecutar desde el principio; no se cambia automáticamente el protocolo para usar CPU. Si Colab no asigna recursos, conservar el error y revisar alternativas. Ante una incompatibilidad de paquetes, una operación no determinista o falta de memoria, conservar el mensaje completo y el manifiesto; no desactivar controles ni cambiar el modelo según las métricas observadas. Las pruebas con el OPT diminuto se ejecutan antes de descargar los recursos grandes.

La consulta de fuentes de APIs, recursos y versiones se hizo el 8 de noviembre de 2026. Los enlaces están en la última celda del notebook. La validación con recursos reales sigue pendiente de ejecución en Colab.
