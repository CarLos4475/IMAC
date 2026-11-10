"""Genera el notebook autónomo sin instalar Jupyter ni paquetes científicos."""
import ast
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cells = []


def add(kind, text):
    cell = {'cell_type': kind, 'id': uuid.uuid4().hex[:8], 'metadata': {},
            'source': text.strip() + '\n'}
    if kind == 'code':
        ast.parse(cell['source'])
        cell.update(execution_count=None, outputs=[])
    cells.append(cell)


add('markdown', '''# Piloto: reutilización de continuaciones sintéticas

**IMAC — 8 de noviembre de 2026.** Notebook autónomo: basta subir este archivo a Colab.

Se propone validar la viabilidad del experimento con **OPT-125m + WikiText-2 en inglés**.
Son **64 ejemplos de entrenamiento**, **32 de validación**, **dos ciclos**, proporciones
**0 y 100 %** de tokens objetivo sintéticos y una repetición. Se realizan cinco ajustes:
M0 humano y dos por cada condición. El conjunto de prueba queda reservado.

Los contextos siempre son humanos: «100 %» se refiere solo a continuaciones objetivo.
Cada ajuste vuelve a los pesos preentrenados y crea un optimizador nuevo. La recursión
se transmite por las continuaciones del modelo anterior, no por acumular sus pesos.

### Cómo ejecutarlo

1. En Colab, elegir **Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU**.
   Usar recursos disponibles; este notebook no contrata servicios ni requiere una clave.
2. Ejecutar las celdas en orden. La primera instala las bibliotecas Python necesarias;
   se conserva el PyTorch del entorno. Si Colab pide reiniciar, hacerlo y continuar con imports.
3. El piloto imprime avances y guarda archivos por etapa. Al terminar, descargar el ZIP
   en la última celda. Los archivos en `/content` son temporales: descargar antes de cerrar.

**Estado de entrega:** se comprobaron sintaxis y controles de protocolo localmente.
La instalación, las pruebas PyTorch, las descargas y el entrenamiento requieren ejecución
en Colab y no se presentan como realizados. No modificar parámetros para provocar colapso.
El piloto sirve para decidir escala y tiempos; no se mezcla con los resultados finales.
''')

add('markdown', '''## 1. Dependencias

Se necesitan Python >=3.11 y PyTorch >=2.6 (normalmente suministrado por Colab).
Transformers carga OPT y el codificador de embeddings; Datasets carga las particiones;
Matplotlib dibuja las trayectorias. Hugging Face Hub, NumPy y Safetensors son dependencias
del mismo entorno. Las versiones efectivas se guardan en el manifiesto.

Las versiones principales de instalación quedan fijadas; las dependencias transitivas
se resuelven al instalar y se registra su versión. No se afirma disponer de un entorno
completamente bloqueado o auditado. Ejecutar desde un runtime limpio.
''')

add('code', '''import sys
import subprocess
import importlib.util

if sys.version_info < (3, 11):
    raise RuntimeError("Seleccionar un runtime con Python 3.11 o posterior.")
if importlib.util.find_spec("torch") is None:
    raise RuntimeError("Falta PyTorch: utilizar un runtime estándar reciente de Colab con GPU.")
if any(name in sys.modules for name in ("transformers", "datasets")):
    raise RuntimeError("Las bibliotecas ya están importadas. Reiniciar la sesión antes de reinstalar.")

subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade",
                "transformers==5.22.2", "datasets==5.1.0", "matplotlib>=3.9,<4",
                "safetensors>=0.6"], check=True)
print("Instalación terminada. Si Colab solicita reiniciar, hacerlo antes de la siguiente celda.")
''')

add('markdown', '''## 2. Controles independientes del hardware

Se agrupan los párrafos de un artículo antes de tokenizar. Solo un encabezado de nivel
superior comienza otro artículo; los encabezados se retiran. Las ventanas de 64+128 tokens
no se solapan ni atraviesan artículos. Se conservan IDs y offsets.

Las etiquetas del contexto y del relleno son `-100`. Reemplazar ejemplos completos de
igual longitud garantiza la proporción exacta de tokens objetivo sintéticos. Una semilla
estable se deriva de SHA-256; no depende del hash aleatorio de Python.
''')
add('code', (ROOT/'controles.py').read_text(encoding='utf-8'))
tests = (ROOT/'test_controles.py').read_text(encoding='utf-8')
tests = tests.replace('from controles import articles, windows, labelled, mix_targets, stable_seed, lexical_metrics', '')
tests = tests.split("if __name__ == '__main__':")[0]
tests += '\nsuite = unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolTests)\n'
tests += 'report = unittest.TextTestRunner(verbosity=2).run(suite)\n'
tests += 'assert report.wasSuccessful(), "No continuar: fallaron controles del protocolo."\n'
add('code', tests)

source = (ROOT/'piloto_colab.py').read_text(encoding='utf-8')
sections = source.split('# %% ')[1:]
notes = {
    'Imports y configuración': '''## 3. Imports y parámetros del piloto

Los valores se mantienen como propuesta operativa. `allow_cpu=False` detiene la ejecución
sin GPU; cambiarlo solo si se desea deliberadamente usar CPU. `save_checkpoints=False`
evita guardar varios gigabytes de pesos: sí se guardan datos, métricas, semillas,
revisiones, hashes y tiempos. Puede activarse antes de ejecutar si hay espacio.

El ajuste es completo, una época, float32, AdamW (lr 2e-5, betas .9/.999,
eps 1e-8, weight decay .01 en todos los parámetros), clipping 1, sin scheduler.
Lote efectivo 8 mediante microbatches de 2: ocho actualizaciones por ajuste del piloto.
Se comprueba el hash de todos los pesos al reiniciar cada ajuste.
''',
    'Muestreo y controles con un modelo diminuto': '''## 4. Generación y comprobaciones PyTorch

Muestreo autorregresivo con caché, temperatura 1 y top-p .95; sin top-k, penalización de
repetición ni beam search. **Propuesta de política EOS del piloto:** se excluyen todos los
IDs especiales del tokenizador, incluido EOS, para obtener exactamente 128 tokens de texto.
Esta restricción modifica la distribución de generación y debe declararse en el estudio;
su conveniencia sigue pendiente de revisión tras el piloto. No se rechazan textos por calidad.

Cada solicitud tiene su generador independiente. La evaluación usa las mismas semillas
por prompt en todas las etapas (comparación pareada). La generación de datos de entrenamiento
utiliza otra familia de semillas por condición/ciclo; el ajuste y el barajado usan otras.

Antes de descargar el modelo se probarán pérdida causal, relleno, reinicio y muestreo con
un OPT diminuto de pesos aleatorios. No son resultados científicos ni requieren descargas.
''',
    'Archivos, tiempos y corpus': '''## 5. Preparación y trazabilidad

Se resuelven y registran los commits de modelo, dataset y codificador. Los repositorios
se cargan sin ejecutar código remoto ni usar tokens de autenticación. Se prefieren pesos
Safetensors; si OPT solo ofrece `.bin`, se exige la carga restringida `weights_only=True`
con PyTorch >=2.6. No se usa deserialización de objetos arbitrarios.

Solo se solicitan `train` y `validation`; no se carga ni se evalúa `test`.
Se muestrean bloques sin reemplazo de cada partición y se comprueban duplicados exactos
entre los bloques seleccionados. Esta comprobación no demuestra ausencia de toda posible
contaminación previa del preentrenamiento ni de similitud entre artículos.

Cada ejecución crea una carpeta nueva. En caso de error conserva resultados parciales;
una nueva ejecución empieza otro piloto. No hay reanudación automática de checkpoints.
''',
    'Métricas de evaluación': '''## 6. Evaluación

- **Perplejidad:** pérdida causal sobre las 128 posiciones humanas reservadas de validación;
  incluye la predicción del primer objetivo desde el contexto. No se evalúa sobre entrenamiento.
- **Distinct-2/3:** n-gramas únicos / n-gramas totales del corpus; sin cruzar fronteras de textos.
- **Repetición de 4-gramas:** promedio por texto de `1 - únicos / total`.
- **Dispersión semántica:** promedio de `1 - coseno` sobre todos los pares de textos, usando
  MiniLM, mean pooling con máscara y normalización L2. Mide dispersión, no calidad ni fidelidad.

Se fija W = mínimo entre 32 palabras y la continuación humana más corta de validación,
antes de generar. Métricas léxicas y semánticas usan las primeras W palabras en minúsculas.
Si alguna generación no llega a W, se informa su número y las métricas comparativas quedan
ausentes para toda esa etapa; no se filtran ejemplos ni se rellena texto. PPL sigue disponible.
El codificador tiene límite de 256 wordpieces; se registra cualquier truncamiento.
''',
    'Ejecución del piloto': '''## 7. Ejecutar los cinco ajustes

La siguiente celda define el procedimiento. La celda posterior lo ejecuta: carga recursos,
ajusta M0 y construye las dos cadenas. Cada ajuste inicia en el checkpoint base y optimizador
nuevo. M0 es compartido: la primera generación sintética de ambas condiciones parte del mismo
punto. El control 0 % usa siempre los objetivos humanos originales.

Se cronometran carga, ajuste, generación de corpus, generación de validación, perplejidad,
embeddings y escritura por separado. No se promete una duración antes de medirla.
''',
    'Gráficas y paquete de salida': '''## 8. Gráficas y descarga

Las trayectorias son descriptivas: solo hay una repetición por condición y dos ciclos.
No se calculan p-valores ni se demuestra colapso a partir de estas gráficas.
El ZIP incluye manifiesto, corpus, muestras, semillas, métricas, registros de ajustes,
tiempos, CSV y figura. Los checkpoints solo se incluyen si se activaron previamente.
'''
}

for section in sections:
    title, code = section.split('\n', 1)
    code = code.split("if __name__ == '__main__':")[0]
    add('markdown', notes[title])
    add('code', code)
    if title == 'Ejecución del piloto':
        add('code', 'RUN_DIR, RESULTS = run_pilot(CFG)')

add('code', 'ARCHIVE = summarize_pilot(RUN_DIR, RESULTS)')
add('code', '''# Descarga al equipo; no monta Drive ni comparte resultados con terceros.
try:
    from google.colab import files
except ImportError:
    print("Fuera de Colab: el ZIP está en", ARCHIVE)
else:
    files.download(ARCHIVE)
''')
add('markdown', '''## Qué revisar al terminar

1. `manifest.json` debe indicar `status: complete`, `fit_count: 5` y `test_used: false`.
2. Cada `fit.json` debe mostrar ocho actualizaciones, 8192 tokens objetivo y el mismo hash
   inicial. Un optimizador empieza vacío en cada ajuste.
3. Revisar `short_texts`, truncamientos y textos generados antes de interpretar métricas.
4. Sumar los tiempos, especialmente generación autorregresiva. Decidir escala final con
   margen para interrupciones y redacción. El estudio propuesto de 48 ajustes no se inicia aquí.
5. Conservar el notebook ejecutado y el ZIP. Repetibilidad de semillas no garantiza identidad
   numérica entre versiones, hardware o backends diferentes. El determinismo estricto puede
   detener el piloto si un kernel no lo admite; registrar ese error antes de alterar la política.

### Fuentes de recursos y APIs

- [OPT-125m y sus condiciones de uso](https://huggingface.co/facebook/opt-125m).
- [WikiText, particiones y licencias](https://huggingface.co/datasets/Salesforce/wikitext).
- [MiniLM: mean pooling y normalización](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- [Auto classes de Transformers](https://huggingface.co/docs/transformers/main/en/model_doc/auto).
- [Parámetros de generación](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation).
- [Transformers 5.22.2](https://pypi.org/project/transformers/5.22.2/) y
  [Datasets 5.1.0](https://pypi.org/project/datasets/5.1.0/).

Se consultaron estas páginas el 8 de noviembre de 2026 para preparar el notebook.
No se incorporaron referencias nuevas al artículo. El código no redistribuye los pesos
ni el corpus: se descargan al ejecutar y deben respetarse sus condiciones de uso.
''')

notebook = {'cells': cells, 'metadata': {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12'},
    'colab': {'name': 'piloto_model_collapse.ipynb', 'provenance': []},
    'accelerator': 'GPU'}, 'nbformat': 4, 'nbformat_minor': 5}
path = ROOT/'piloto_model_collapse.ipynb'
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
print(f'{path}: {len(cells)} celdas; sintaxis Python comprobada al generar.')
