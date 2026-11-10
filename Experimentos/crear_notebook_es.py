"""Genera el notebook español autónomo sin tocar la versión anterior."""
import ast
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cells = []


def add(kind, text):
    text = text.strip() + '\n'
    cell = {'cell_type': kind, 'id': uuid.uuid4().hex[:8], 'metadata': {}, 'source': text}
    if kind == 'code':
        ast.parse(text)
        cell.update(execution_count=None, outputs=[])
    cells.append(cell)


add('markdown', '''# Piloto en español: reutilización de continuaciones sintéticas

**IMAC — 9 de noviembre de 2026.** Este notebook es nuevo y autónomo: subir solo este archivo.

El usuario confirmó que la investigación debe medir texto en **español**. Se propone
`datificate/gpt2-small-spanish`, corpus `wikimedia/wikipedia` (`20231101.es`) y codificador
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. Son recursos del piloto,
pendientes de comprobar con esta ejecución, no una validación del protocolo final.

El modelo generador es un GPT-2 pequeño adaptado a español desde un checkpoint inglés,
según su ficha. Es un modelo de continuación, no un chat. El corpus también está en español;
no se traduce WikiText. El codificador semántico es multilingüe, apropiado para incluir español.

**Escala:** 64 ejemplos de entrenamiento, 32 de validación, dos ciclos, una repetición y
0/100 % de objetivos sintéticos. Cinco ajustes en total: M0 humano y dos por condición.
Los contextos de 64 tokens permanecen originales y los objetivos tienen 128 tokens.
Cada ajuste restaura el checkpoint base y crea un optimizador nuevo. La recursión se
transmite por datos, no mediante acumulación de pesos.

## Antes de ejecutar

1. Importar como notebook nuevo, conservando la copia anterior y sus salidas.
2. En Colab, **Entorno de ejecución → Reiniciar sesión** para limpiar imports interrumpidos.
   Seleccionar GPU en **Cambiar tipo de entorno de ejecución**. El código no compra recursos.
3. Ejecutar las celdas en orden. La primera instala bibliotecas y contiene todos los imports
   necesarios para ello. Si Colab pide reiniciar tras instalar, reiniciar y continuar con imports.
4. Descargar el ZIP al terminar: `/content` es temporal. No se monta Drive ni se requieren claves.

**Estado:** controles offline y sintaxis verificados; este nuevo notebook aún no se ejecutó
en Colab. Es un piloto de viabilidad, sin resultados finales ni promesa de duración.
''')
add('markdown', '''## 1. Instalación

Python >=3.11, PyTorch >=2.6 preinstalado por Colab. Se fijan Transformers 5.22.2 y Datasets
5.1.0; Matplotlib dibuja gráficas y Safetensors permite guardar pesos sin objetos pickle.
Se registran nombres/versiones del entorno al ejecutar. No se reemplaza el PyTorch de Colab.
''')
add('code', '''import sys
import subprocess
import importlib.util

if sys.version_info < (3, 11):
    raise RuntimeError("Usar un runtime reciente de Colab con Python >=3.11.")
if importlib.util.find_spec("torch") is None:
    raise RuntimeError("Falta PyTorch. Usar un entorno estándar de Colab con GPU.")
if any(name in sys.modules for name in ("transformers", "datasets")):
    raise RuntimeError("Reiniciar sesión para limpiar los imports anteriores antes de instalar.")
subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade",
                "transformers==5.22.2", "datasets==5.1.0", "matplotlib>=3.9,<4",
                "safetensors>=0.6"], check=True)
print("Dependencias instaladas. Si Colab pide reiniciar, hacerlo antes de continuar.")
''')
add('markdown', '''## 2. Controles del protocolo y del español

Se conservan tildes y ñ con normalización Unicode NFC. Se comprueban semillas, etiquetas,
mezclas exactas, longitudes comunes, separación por artículo y detección de duplicados.
Las etiquetas de contexto y relleno se excluyen de la pérdida mediante `-100`.
Las utilidades de WikiText del módulo anterior quedan como funciones auxiliares probadas,
pero no se usan para seleccionar el nuevo corpus: aquí cada registro ya es un artículo.
''')
helpers = (ROOT/'controles.py').read_text(encoding='utf-8')
spanish = (ROOT/'controles_es.py').read_text(encoding='utf-8')
spanish = spanish.replace(
    'from controles import stable_seed, words as base_words, lexical_metrics as base_lexical_metrics',
    'base_words = words\nbase_lexical_metrics = lexical_metrics')
add('code', helpers+'\n\n'+spanish)
test_sources = []
for filename in ('test_controles.py', 'test_controles_es.py'):
    src = (ROOT/filename).read_text(encoding='utf-8').split("if __name__ == '__main__':")[0]
    src = '\n'.join(line for line in src.splitlines() if not line.startswith('from controles'))
    test_sources.append(src)
test_sources.append('''suite = unittest.TestSuite([
    unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolTests),
    unittest.defaultTestLoader.loadTestsFromTestCase(SpanishProtocolTests),
])
report = unittest.TextTestRunner(verbosity=2).run(suite)
assert report.wasSuccessful(), "No continuar si falla algún control."
''')
add('code', '\n\n'.join(test_sources))

notes = {
'Imports y configuración': '''## 3. Imports y configuración

Configuración acotada al piloto. Ajuste completo en float32, una época, AdamW con tasa
2e-5, betas .9/.999, epsilon 1e-8 y weight decay .01 en todos los parámetros, clipping 1,
sin scheduler. Lote efectivo 8, microbatch 2: ocho actualizaciones por ajuste.

GPU obligatoria por defecto. `allow_cpu=True` permite CPU deliberadamente, sin tiempos
comprobados. `save_checkpoints=False` evita varios GB: se guardan datos, parámetros,
semillas y resultados. Puede activarse antes de ejecutar si se desean también los pesos.
''',
'Muestreo y controles con un modelo diminuto': '''## 4. Generación y comprobaciones PyTorch

Temperatura 1, top-p .95, sin top-k ni penalización de repetición. Un generador independiente
por solicitud; evaluación con semillas pareadas entre etapas y separadas de generación de
datos y entrenamiento. Se producen 128 tokens, excluyendo todos los IDs especiales,
incluido EOS. Es una política propuesta de longitud fija que modifica la distribución de
decodificación y debe documentarse; no se filtra por calidad.

Antes de descargar los recursos grandes, un GPT-2 diminuto de pesos aleatorios comprueba
pérdida causal, relleno, caché, reproducibilidad y restauración de pesos/optimizador.
No requiere descargas y no constituye un resultado del experimento.
''',
'Archivos, tiempos y corpus': '''## 5. Corpus español y particiones propias

Wikipedia ofrece `20231101.es` con una sola partición oficial `train`. **No se inventan
particiones oficiales:** se asigna cada artículo por SHA-256 de semilla e ID a train,
validación o reserva de prueba (80/10/10 aproximado). Se aplica streaming a un prefijo
de hasta 2000 artículos, para limitar la preparación; ese prefijo no es una muestra
representativa de toda Wikipedia. El streaming puede descargar buffers adicionales.

Los artículos reservados para prueba se omiten antes de tokenizar. De cada artículo
elegible se elige una sola ventana entre sus bloques no solapados de 64+128 tokens, con
semilla fija; después se muestrean 64 artículos para entrenamiento y 32 para validación.
No se mezclan artículos entre particiones. Se verifican duplicados por ID, hash del texto
completo y ventanas exactas. Si faltan candidatos o hay duplicados, se detiene sin reemplazos
silenciosos. Se guardan revisión, IDs, URLs, hashes, offsets, conteos y regla de selección.

**Límite de procedencia:** Wikipedia se usa como referencia original; no acredita autoría
humana individual ni ausencia de contenido sintético. El modelo ya fue adaptado a Wikipedia
en español; separar artículos en este piloto no demuestra ausencia de solapamiento con su
preentrenamiento. La PPL es una referencia relativa de dominio, no evidencia de conocimiento nuevo.

Se usan revisiones registradas, `trust_remote_code=False` y recursos públicos sin claves.
Safetensors cuando está disponible; para los pesos `.bin` del GPT-2 se exige
`weights_only=True` con PyTorch >=2.6. Cada ejecución crea otra carpeta; sin reanudación
automática. Los errores conservan archivos parciales.
''',
'Métricas de evaluación': '''## 6. Métricas para los textos en español

- **Perplejidad:** sobre las 128 posiciones objetivo originales de validación; se excluye
  el contexto, incluyendo correctamente la primera predicción de continuación.
- **Distinct-2/3:** proporción de n-gramas únicos del corpus, sin cruzar textos.
- **Repetición de 4-gramas:** promedio por texto de `1 - únicos/total`.
- **Dispersión semántica:** promedio de `1 - coseno` entre pares, con MiniLM multilingüe,
  mean pooling con máscara y normalización L2; es un indicador de dispersión, no de calidad.

Se conservan tildes y ñ. El conteo usa palabras/números Unicode en minúsculas, sin stemming
ni eliminación de palabras vacías. Se fija W con las referencias de validación: mínimo
entre 32 y la longitud de su continuación más corta. Métricas léxicas/semánticas usan las
primeras W palabras. Si una salida no alcanza W, se registra y las métricas de esa etapa
quedan ausentes, sin descartar textos ni rellenarlos. PPL sigue calculándose.

MiniLM multilingüe usa un límite de 128 wordpieces, coherente con su configuración; se
informa cualquier truncamiento. Un modelo generador español no garantiza que cada salida
sea español fluido: se guardan las muestras para revisarlas, sin filtrar por idioma o calidad.
''',
'Ejecución del piloto': '''## 7. Ejecutar el piloto en español

La celda siguiente define el procedimiento y la posterior lo ejecuta. Son cinco ajustes:
M0 y dos ciclos en cada condición. M0 se comparte y cada ajuste vuelve a los pesos base.
El control conserva objetivos originales; al 100 % solo las continuaciones se sustituyen
por texto del modelo anterior. Los contextos siguen siendo originales.

Se guardan datos y resultados incrementalmente. Se cronometran carga, ajuste, generación
de corpus, generación de evaluación, perplejidad, embeddings y escritura por separado.
''',
'Gráficas y paquete de salida': '''## 8. Gráficas y descarga

Se muestran trayectorias descriptivas de una sola repetición por condición. No se calculan
p-valores ni se identifica colapso únicamente por las gráficas. El ZIP incluye manifiesto,
corpus, salidas de validación, métricas, semillas, tiempos, CSV y figura. Los checkpoints
solo se incluyen si se activaron previamente. Descargar antes de cerrar Colab.
'''
}
source = (ROOT/'piloto_colab_es.py').read_text(encoding='utf-8')
for section in source.split('# %% ')[1:]:
    title, code = section.split('\n', 1)
    code = code.split("if __name__ == '__main__':")[0]
    add('markdown', notes[title])
    add('code', code)
    if title == 'Ejecución del piloto':
        add('code', 'RUN_DIR, RESULTS = run_pilot(CFG)')
add('code', 'ARCHIVE = summarize_pilot(RUN_DIR, RESULTS)')
add('code', '''try:
    from google.colab import files
except ImportError:
    print("El paquete está en", ARCHIVE)
else:
    files.download(ARCHIVE)
''')
add('markdown', '''## Comprobación final y fuentes

`manifest.json` debe indicar `status: complete`, `fit_count: 5`, `test_used: false` y
`config.language: es`. Cada ajuste debe tener ocho actualizaciones, 8192 tokens objetivo
y la misma huella de pesos iniciales. Revisar textos cortos, truncamientos y ejemplos.
Las semillas facilitan repetir la ejecución, pero no garantizan identidad numérica entre
hardware/versiones. Si un kernel no admite el determinismo estricto, registrar el error.

Guardar este notebook ejecutado y el ZIP. Revisar tiempos antes de decidir escala final;
no se inicia automáticamente el estudio de 48 ajustes. El piloto no se mezcla con sus resultados.

Fuentes primarias consultadas el **9 de noviembre de 2026**:

- [GPT-2 pequeño adaptado al español: ficha y procedencia](https://huggingface.co/datificate/gpt2-small-spanish).
- [Archivos del modelo, configuración y pesos](https://huggingface.co/datificate/gpt2-small-spanish/tree/main).
- [Wikipedia: configuración española y licencias](https://huggingface.co/datasets/wikimedia/wikipedia).
- [Codificador multilingüe](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).
- [Límite del codificador: 128 tokens](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/sentence_bert_config.json).
- [Streaming de Datasets](https://huggingface.co/docs/datasets/stream).

La ficha del generador y del codificador indican Apache-2.0; Wikipedia declara CC-BY-SA-3.0
y GFDL. Conservar atribución y condiciones correspondientes al usar o redistribuir recursos.
Este archivo contiene código; pesos y corpus se descargan solo al ejecutar. Las referencias
del artículo no se modificaron durante la preparación de esta nueva entrega.
''')
notebook = {'cells': cells, 'metadata': {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.13'},
    'colab': {'name': 'piloto_model_collapse_es.ipynb', 'provenance': []},
    'accelerator': 'GPU'}, 'nbformat': 4, 'nbformat_minor': 5}
path = ROOT/'piloto_model_collapse_es.ipynb'
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
print(f'{path}: {len(cells)} celdas; sintaxis comprobada.')
