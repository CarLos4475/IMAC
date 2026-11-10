# Verificación del notebook

Actualizado: 9 de noviembre de 2026.

## Comprobaciones y evidencias

- **Principal preparado, 9 de noviembre:** `experimento_principal_es.ipynb`, 29 celdas y 16 de código. Pasaron 20 pruebas locales (13 anteriores y siete nuevas) y las mismas 20 embebidas. Se comprobaron calendario de 48 ajustes, particiones/duplicados, firma de código/configuración/entorno, relectura JSON de tuplas, marcadores incompletos, artefactos corruptos y cachés de lotes. JSON, IDs, sintaxis, autonomía y banderas desactivadas comprobados. El artículo quedó armonizado en español con 18 referencias citadas y compilación exitosa. No se ejecutaron ajustes principales, montaje de Drive ni la nueva prueba PyTorch de checkpoint.
- **Ejecución integrada completada, 9 de noviembre:** cinco ajustes del piloto español en Tesla T4; 13 pruebas del protocolo y controles PyTorch pasaron. PyTorch 2.14.1+cu130, Transformers 5.22.2 y Datasets 5.1.0. ZIP, notebook con salidas, captura, tiempos y datos archivados en [resultados/piloto_es_2026-11-09](resultados/piloto_es_2026-11-09/RESUMEN.md). Verificación posterior de particiones, presupuestos, mezclas, semillas, longitudes y métricas léxicas: pasó. Embeddings/PPL no se recalcularon localmente. No se ejecutó el estudio final.
- **Preparación del notebook español, antes de ejecutarlo el 9 de noviembre:** `piloto_model_collapse_es.ipynb`, 22 celdas. Pasaron 13 pruebas de protocolo (siete heredadas y seis de español), también al ejecutar las celdas de controles embebidas. Se comprobaron Unicode, separación por artículo, reserva de prueba, duplicados, tamaños, JSON/IDs, sintaxis, imports completos y autonomía. La ejecución científica ocurrió después y se registra en la entrada anterior; la copia inglesa se conservó.
- Python 3.12 está disponible a través de `py -3.12`; `python` apunta a un alias de Windows que no se pudo ejecutar.
- Siete controles de protocolo pasaron con biblioteca estándar: artículos, ventanas, etiquetas, mezcla exacta, semillas, n-gramas y tratamiento de textos cortos.
- Se observó el fallo previo por ausencia del módulo antes de implementar los controles; después se obtuvo el pase de las siete pruebas.
- Se generó un notebook de 22 celdas. Cada celda de código se analizó con `ast.parse`; las fuentes `.py` compilaron con `py_compile`.

## Pendiente

En el Python local consultado no están instalados PyTorch, Transformers ni Datasets. No se instalaron paquetes científicos localmente. **En Colab sí se completaron instalación, controles y piloto español**; ya hay resultados propios de piloto y tiempos registrados. El notebook principal y la armonización del artículo están preparados. Pendientes: nueva prueba de checkpoint PyTorch, montaje de Drive, primera etapa/reanudación y ejecución final. Controles offline y compilación no verifican ese flujo integrado.

**Antecedente de la versión inglesa:** tras instalar la extensión, se leyó el notebook remoto y se observó T4. Se inició Ejecutar todas y se interrumpió durante imports por la aclaración de español. Se observó `KeyboardInterrupt`, instalación finalizada y ausencia de entrenamiento. Python 3.13 aparecía en esa traza; aún no se había diagnosticado CUDA, que sí se comprobó en la ejecución española posterior.

La versión en inglés queda sustituida en su alcance lingüístico. La adaptación `piloto_model_collapse_es.ipynb` ya se ejecutó tras el aviso del usuario y su autorización de trabajar en Chrome. Se resolvió un límite de sesiones cuando el usuario las cerró. No se cambió el artículo durante el piloto; se armonizó después al preparar el principal. La ejecución anterior interrumpida, descrita arriba, es un antecedente distinto.

Los intentos previos de control de Brave y Chrome terminaron porque la herramienta no pudo verificar la URL del navegador. Se observó un notebook de Colab en los títulos del inventario de ventanas, pero no se leyó ni modificó su contenido. El archivo local se creó tras la autorización del usuario de continuar con esta alternativa.

El notebook español incluye una prueba PyTorch con un GPT-2 diminuto aleatorio: pérdida causal, máscara de relleno, restauración de pesos/optimizador y muestreo repetible. Pasó antes de descargar el generador español. El notebook inglés conservaba la variante OPT y no se continuó su entrenamiento.

## Revisión de seguridad proporcional al notebook

Se aplicó la habilidad `svc`. Se revisaron dependencias, fichas oficiales y los artefactos de una ejecución integrada del piloto. No se realizó una auditoría de vulnerabilidades del entorno de Colab; comprobar el funcionamiento no equivale a certificar todas sus dependencias. El bloque siguiente corresponde al piloto; la ampliación principal se registra después.

```txt
Security check:
- Data touched: Wikipedia española, pesos públicos y salidas del piloto; WikiText solo en el notebook histórico. Se archivaron los archivos de resultados descargados, sin leer otros documentos privados.
- Auth required: cuenta del usuario para Colab; el código no implementa login ni solicita credenciales para Hugging Face.
- Authorization enforced at: sesión de Colab del usuario; no modifica permisos ni crea enlaces compartidos.
- Secrets: sin claves incorporadas; token=False y desactivación del uso implícito de tokens para los repositorios públicos.
- Input validation: configuración acotada al piloto; 13 tests y pruebas PyTorch pasaron en Colab. Verificación local de artefactos, particiones, presupuestos, semillas y métricas léxicas pasó; no se ejecuta el texto generado.
- Output rendering: texto/JSON/CSV y gráficas; el contenido generado no se interpreta como código ni se renderiza como HTML.
- Logs/errors: se guardan parámetros, hashes y métricas; el manejador registra solo el tipo de error, sin volcar variables de entorno o cabeceras.
- DB/storage rules: sin base de datos ni buckets; carpetas nuevas en el runtime y ZIP descargado; no se monta Drive automáticamente.
- Dependencies: versiones del manifiesto verificadas (PyTorch 2.14.1+cu130, Transformers 5.22.2, Datasets 5.1.0). Piloto integrado completado. Sin nueva instalación local ni auditoría de vulnerabilidades; no se certifica seguridad de todas las dependencias.
- Rate limiting / abuse controls: sin endpoint ni API de inferencia; cinco ajustes acotados, sin contratación de servicios. El runtime puede consumir su cuota disponible.
- Web risks: descargas de tres repositorios definidos en la configuración; sin servidor, formularios, redirecciones propias ni URLs con credenciales.
- Prototype/security debt: piloto académico ejecutado; no es un servicio de producción. Carga sin código remoto y con weights_only=True para pesos binarios. Sin auditoría de seguridad completa ni protocolo final ejecutado.
```

## Revisión de la preparación principal

```txt
Security check:
- Data touched: pesos y corpus públicos, datos del estudio y carpeta de salida específica de Drive. No se montó Drive ni se leyó contenido privado en esta preparación.
- Auth required: Colab y montaje personal de Drive; banderas por defecto False. El notebook no solicita claves Hugging Face ni introduce credenciales.
- Authorization enforced at: consentimiento interactivo de montaje de la cuenta y carpeta OUTPUT_ROOT; una sesión escritora. El montaje concede acceso al runtime, no aislamiento al nivel de una carpeta.
- Secrets: token=False y uso implícito de tokens desactivado; sin credenciales incorporadas ni registro de variables de entorno.
- Input validation: configuración principal acotada, mismo split_seed que el piloto, huellas de configuración/código/entorno; 20 controles locales/embebidos. Rutas de artefactos no pueden escapar de la etapa y se comprueban hashes.
- Output rendering: JSON, CSV, texto y gráficas; el contenido de Wikipedia y las generaciones no se ejecutan ni se interpretan como HTML.
- Logs/errors: parámetros, versiones, hashes, corpus público, resultados y tiempos de actividades completadas. No se vuelcan credenciales; los errores por corrupción detienen sin sobrescritura silenciosa.
- DB/storage rules: sin servidor ni base de datos; persistencia en subcarpeta de MyDrive. Reemplazo de JSON pendientes y checkpoints Safetensors; purga limitada a nombres propios de checkpoints de etapas confirmadas. Sin garantía de transacción distribuida de Drive.
- Dependencies: paquetes principales fijados a versiones observadas en el piloto; PyTorch del runtime >=2.6, carga de generador binario weights_only=True y trust_remote_code=False; codificador y checkpoints Safetensors. Sin instalación ML local, auditoría de vulnerabilidades o ejecución integrada principal.
- Rate limiting / abuse controls: sin endpoint ni API de pago. 48 ajustes previstos, RUN_EXPERIMENT=False y MAX_NEW_STAGES=1 al entregar; no contratación de recursos.
- Web risks: descargas de tres repositorios definidos con revisiones fijas, sin servicio web propio ni enlaces compartidos creados; montaje Drive pendiente.
- Prototype/security debt: protocolo académico preparado. Faltan prueba PyTorch nueva de checkpoint, persistencia real en Drive, interrupción/reanudación integrada y ejecución principal; no se afirma tolerancia completa a fallos ni seguridad certificada.
```
