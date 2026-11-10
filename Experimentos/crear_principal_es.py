"""Construye el notebook principal autónomo y protegido contra inicio accidental."""
import ast
import hashlib
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cells, source_parts = [], []


def add(kind, source):
    source = source.strip()+'\n'
    cell = {'cell_type': kind, 'id': uuid.uuid4().hex[:8], 'metadata': {}, 'source': source}
    if kind == 'code':
        ast.parse(source)
        cell.update(execution_count=None, outputs=[])
    cells.append(cell)


def without_local_imports(source):
    return '\n'.join(line for line in source.splitlines()
                     if not line.startswith(('from controles import', 'from controles_es import', 'from estado_principal_es import')))


add('markdown', '''# Experimento principal en español — IMAC

Preparado el **9 de noviembre de 2026**, después del piloto español de cinco ajustes.
Este archivo es nuevo y autónomo; conserva aparte el piloto y sus salidas.

**Diseño:** GPT-2 pequeño adaptado al español, Wikipedia `20231101.es`, 512 ejemplos,
contextos de 64 tokens y objetivos de 128; 0/50/100 % de objetivos sintéticos, cinco ciclos,
tres repeticiones. Son **48 ajustes**: tres M0 y 45 posteriores. M0 se comparte dentro
de cada repetición. Todos los ajustes vuelven al modelo preentrenado y optimizador nuevo.

**Preparación no equivale a ejecución:** se verificaron controles offline y sintaxis.
Este flujo completo y sus checkpoints en Drive aún no se probaron en Colab. La primera
ejecución queda limitada a **una etapa** para verificar persistencia y reanudación.
`RUN_EXPERIMENT=False` evita iniciar ajustes al usar «Ejecutar todas» por primera vez.

## Orden de uso

1. Importar este notebook, elegir GPU y utilizar una sesión limpia. Instalar dependencias.
2. Ejecutar controles y definiciones. La prueba diminuta verifica guardado/restauración,
   sin descargar el modelo grande ni ejecutar el estudio.
3. Revisar la ruta de salida. Activar `PREPARE_DRIVE=True` y completar personalmente la
   autorización de montaje si se desea guardar en Drive. El programa solo usa la carpeta
   de este experimento; montar Drive da acceso al entorno y requiere tu consentimiento.
4. Activar `RUN_EXPERIMENT=True` con `MAX_NEW_STAGES=1` para la primera etapa. Comprobar
   sus archivos y repetir esa celda para verificar que se omite la etapa confirmada.
5. Para continuar el resto, usar `MAX_NEW_STAGES=None` con la misma configuración y carpeta.
   Ejecutar una sola sesión a la vez. No cambiar parámetros mirando métricas de prueba.

Se estimaron unas 2.67 h de cálculo por extrapolación del piloto, **sin validar la duración
principal ni incluir el costo adicional de checkpoints, Drive e interrupciones**. Dejar
margen para análisis y redacción. No se compra cómputo ni se requieren claves de API.
''')
add('markdown', '''## 1. Dependencias

Se conservan las versiones observadas en el piloto para los paquetes principales.
PyTorch proviene del runtime de Colab: no se reemplaza automáticamente. Al reanudar se
exigen las mismas versiones esenciales, Python, CUDA y nombre de GPU que en la primera
sesión. Una incompatibilidad detiene el programa, no mezcla ejecuciones silenciosamente.
''')
add('code', '''import sys
import subprocess
import importlib.util
if sys.version_info < (3, 11) or importlib.util.find_spec('torch') is None:
    raise RuntimeError('Usar un runtime reciente de Colab con PyTorch y GPU.')
if any(name in sys.modules for name in ('transformers', 'datasets')):
    raise RuntimeError('Reiniciar sesión antes de reinstalar paquetes ya importados.')
subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade',
    'transformers==5.22.2', 'datasets==5.1.0', 'safetensors==0.8.0',
    'matplotlib==3.11.2', 'numpy==2.4.6', 'tokenizers==0.23.3'], check=True)
print('Instalación terminada. Si Colab pide reiniciar, hacerlo antes de continuar con imports.')
''')
add('markdown', '''## 2. Controles del protocolo y de reanudación

Se conservan Unicode NFC, tildes y ñ. Las particiones del piloto **no se cambian**:
hash de semilla 20261109 e ID de artículo, 80/10/10 aproximado. Ahora se preparan 512
ejemplos de entrenamiento, 128 de validación y 128 de prueba de artículos disjuntos.
Se usa un prefijo acotado de 2000 artículos, una ventana por artículo y controles de
duplicados. Si faltan candidatos, se detiene antes de ajustar.

La validación fija W (hasta 32 palabras); prueba no elige parámetros ni checkpoints.
Wikipedia es referencia original, sin certificar autoría humana individual. El modelo
ya se adaptó a Wikipedia: no se acredita ausencia de solapamiento con preentrenamiento.
''')
helpers = (ROOT/'controles.py').read_text(encoding='utf-8')
spanish = (ROOT/'controles_es.py').read_text(encoding='utf-8').replace(
    'from controles import stable_seed, words as base_words, lexical_metrics as base_lexical_metrics',
    'base_words = words\nbase_lexical_metrics = lexical_metrics')
state = without_local_imports((ROOT/'estado_principal_es.py').read_text(encoding='utf-8'))
helper_source = helpers+'\n\n'+spanish+'\n\n'+state
source_parts.append(helper_source)
add('code', helper_source)
tests = []
for name in ('test_controles.py', 'test_controles_es.py', 'test_estado_principal_es.py'):
    tests.append(without_local_imports((ROOT/name).read_text(encoding='utf-8').split("if __name__ == '__main__':")[0]))
tests.append('''suite = unittest.TestSuite([
    unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolTests),
    unittest.defaultTestLoader.loadTestsFromTestCase(SpanishProtocolTests),
    unittest.defaultTestLoader.loadTestsFromTestCase(MainProtocolTests),
])
test_result = unittest.TextTestRunner(verbosity=2).run(suite)
assert test_result.wasSuccessful(), 'No continuar si falla algún control.'
''')
add('code', '\n\n'.join(tests))
add('markdown', '''## 3. Funciones de aprendizaje y métricas usadas en el piloto

Se reutiliza el ajuste completo de una época, AdamW 2e-5 (betas .9/.999, epsilon 1e-8,
decay .01 uniforme), clipping 1, lote efectivo 8 y microbatch 2. Son 64 actualizaciones
y 65 536 tokens objetivo por ajuste. Contexto/relleno se enmascaran con `-100`.

Muestreo T=1, top-p=.95, sin top-k ni penalización de repetición; exactamente 128 tokens,
excluyendo IDs especiales, incluido EOS. Un RNG por solicitud. Las semillas de evaluación
se emparejan entre etapas de la misma repetición; las de entrenamiento/datos son distintas.

Distinct-2/3 por corpus sin cruzar textos, repetición media por texto, dispersión media
de coseno con MiniLM multilingüe y PPL de continuaciones originales reservadas. La métrica
semántica utiliza mean pooling/L2, máximo 128 wordpieces y truncamientos registrados.
Las etapas con salidas más cortas que W conservan esos textos y dejan ausentes las métricas
léxicas/semánticas afectadas. Se guardan muestras sin filtrar por idioma/calidad.
''')
core = (ROOT/'piloto_colab_es.py').read_text(encoding='utf-8')
for section in core.split('# %% ')[1:]:
    title, code = section.split('\n', 1)
    if title in ('Ejecución del piloto', 'Gráficas y paquete de salida'):
        continue
    source_parts.append(code)
    add('code', code)
add('code', 'PilotConfig = Config')
add('markdown', '''## 4. Configuración principal, checkpoints y persistencia

Revisiones del modelo, dataset y codificador fijadas a los commits del piloto. Un cambio
de parámetros, código o entorno esencial bloquea reanudación en el mismo directorio.

Se guardan checkpoints Safetensors para M0 y para continuar la cadena activa. Después
de confirmar el sucesor completo se purgan únicamente los pesos no iniciales anteriores
creados por este programa. Sus corpus, semillas, métricas y marcadores se conservan.
No se promete conservar los pesos de los 48 modelos. El máximo habitual ronda 2.5–3 GB
en pesos durante escritura, más datos; quedan transferencias acumuladas e I/O de Drive.

Los lotes de generación se guardan con hashes de entrada, productor y salida. Un ajuste
interrumpido antes de guardar su checkpoint se repite desde base/semilla; un ajuste ya
guardado continúa en evaluación. Los marcadores completos verifican archivos y evitan
reentrenar etapas confirmadas. No es una transacción distribuida ni garantiza sincronización
instantánea de Drive: un archivo incompleto o corrupto causa detención, no sustitución silenciosa.
''')
main_source = (ROOT/'principal_colab_es.py').read_text(encoding='utf-8')
for section in main_source.split('# %% ')[1:]:
    title, code = section.split('\n', 1)
    source_parts.append(code)
    if title != 'Configuración del estudio principal':
        add('markdown', '### '+title)
    add('code', code)
source_hash = hashlib.sha256('\n'.join(source_parts).encode()).hexdigest()
add('markdown', '''## 5. Comprobar checkpoints con un modelo diminuto

Este control adicional está preparado para ejecutarse en Colab. Guarda un GPT-2 diminuto,
modifica un parámetro y restaura los pesos verificando la misma huella. No descarga el
generador ni utiliza el corpus de prueba. La comprobación aún no se ha ejecutado durante
la preparación local de este notebook.
''')
add('code', '''import tempfile
torch_smoke_checks()
with tempfile.TemporaryDirectory(dir=Path.cwd()) as checkpoint_temp:
    checkpoint_folder = Path(checkpoint_temp)
    tiny = GPT2LMHeadModel(GPT2Config(vocab_size=32, n_embd=16, n_inner=32,
        n_layer=1, n_head=2, n_positions=32, bos_token_id=2, eos_token_id=2, pad_token_id=1)).cpu()
    signature_before = weight_hash(tiny)
    disk_hash = save_checkpoint(tiny, checkpoint_folder)
    atomic_json(checkpoint_folder/'fit.json', {'checkpoint_sha256': disk_hash,
                                              'final_weight_sha256': signature_before})
    with torch.no_grad():
        next(tiny.parameters()).add_(.01)
    assert weight_hash(tiny) != signature_before
    restore_checkpoint(tiny, checkpoint_folder, device='cpu')
    assert weight_hash(tiny) == signature_before
    del tiny
print('Checkpoint diminuto guardado y restaurado correctamente.')
''')
add('markdown', '''## 6. Ruta persistente y autorización de Drive

La carpeta del experimento se crea al iniciar, no al importar. Mantener una sola sesión
escribiendo en ella. Elegir una ruta nueva si ya tiene archivos ajenos o un protocolo diferente.

`PREPARE_DRIVE=True` permite solicitar el montaje; el usuario debe completar la autorización
de su cuenta. El programa no introduce credenciales ni aprueba ese acceso por su cuenta.
No cambiar a `/content` para una ejecución que se pretenda reanudar tras perder la VM.
''')
add('code', f'''SOURCE_SHA256 = '{source_hash}'
OUTPUT_ROOT = Path('/content/drive/MyDrive/IMAC/estudio_principal_es_v1')
PREPARE_DRIVE = False
RUN_EXPERIMENT = False
MAX_NEW_STAGES = 1  # Primera comprobación de I/O; None continúa todas las etapas restantes.

if PREPARE_DRIVE and not Path('/content/drive/MyDrive').is_dir():
    from google.colab import drive
    drive.mount('/content/drive')
else:
    print('Montaje no solicitado o Drive ya disponible. Ruta:', OUTPUT_ROOT)
print('Diseño:', len(make_plan()), 'ajustes; ejecución activada:', RUN_EXPERIMENT)
''')
add('markdown', '''## 7. Ejecutar o reanudar

Al activar la bandera, el mismo procedimiento detecta etapas completas y continúa las
pendientes. Los 48 ajustes no se iniciaron durante la creación de este archivo. Primero
se recomienda confirmar una etapa completa y probar la reanudación con su checkpoint.

La muestra sintética de 50 % usa los mismos 256 IDs durante los ciclos de una repetición.
Se generan 512 continuaciones en cada ciclo no humano y se aplica esa selección fija.
Los 128 contextos de prueba son comunes a condiciones/repeticiones. Sus métricas se guardan
por etapa, pero el programa muestra el resumen conjunto al terminar, sin utilizarlas para
decidir parámetros, checkpoints o detención temprana.
''')
add('code', '''if RUN_EXPERIMENT:
    MAIN_RUN = run_main(MAIN_CFG, OUTPUT_ROOT, SOURCE_SHA256, max_new_stages=MAX_NEW_STAGES)
else:
    print('Configuración preparada. No se han iniciado ajustes principales.')
''')
add('markdown', '''## 8. Resumen final y exportación

Las gráficas presentan media y rango de tres cadenas, no 128 réplicas de entrenamiento.
Se exportan resultados y contrastes por repetición frente a M0 y frente al control del
mismo ciclo. No se calculan p-valores con estos tamaños pequeños.
El ZIP excluye pesos, pero Drive conserva los checkpoints necesarios para reanudar.
''')
add('code', '''if RUN_EXPERIMENT and (OUTPUT_ROOT/'finished.json').exists():
    MAIN_ARCHIVE = summarize_main(OUTPUT_ROOT)
    from google.colab import files
    files.download(str(MAIN_ARCHIVE))
else:
    print('Resumen disponible al confirmar las 48 etapas; no se muestran métricas parciales de prueba.')
''')
add('markdown', '''## Fuentes y límites

- [Generador español](https://huggingface.co/datificate/gpt2-small-spanish),
  [Wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) y
  [MiniLM multilingüe](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).
- [Safetensors: save_model/load_model y pesos compartidos](https://huggingface.co/docs/safetensors/main/en/api/torch).
- [Colab: límites de recursos, sesiones y Drive](https://research.google.com/colaboratory/faq.html).

Consultadas el 9 de noviembre de 2026. Conservar licencias/atribución de recursos al
redistribuir. Semillas e igualdad de versiones facilitan repetir, sin garantizar identidad
entre entornos. El piloto no probó la escritura de checkpoints en Drive ni la duración
de 48 ajustes. Se verificaron localmente calendario, particiones, corrupción y reanudación
de registros/lotes; siguen pendientes la prueba integrada y la ejecución principal.
''')
notebook = {'cells': cells, 'metadata': {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.13'},
    'colab': {'name': 'experimento_principal_es.ipynb', 'provenance': []},
    'accelerator': 'GPU'}, 'nbformat': 4, 'nbformat_minor': 5}
path = ROOT/'experimento_principal_es.ipynb'
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
print(f'{path}: {len(cells)} celdas. Código científico SHA256: {source_hash}')
