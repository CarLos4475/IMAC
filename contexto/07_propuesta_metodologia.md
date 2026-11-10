# Propuesta operativa de metodología

Actualizado: 9 de noviembre de 2026.

## Información confirmada por el usuario

- **Español**, confirmado expresamente el 9 de noviembre. La propuesta anterior en inglés fue del agente y queda sustituida. No basta traducir los encabezados: deben adecuarse modelo, corpus y evaluación semántica.
- Se dispone de aproximadamente **cuatro días**.
- Puede utilizarse esta computadora o Google Colab.
- No se confirmó una fecha y hora exactas de entrega. El 9 de noviembre se ejecutaron diagnóstico PyTorch/CUDA y piloto completo en **Tesla T4**; no se garantiza disponibilidad posterior del mismo acelerador.

No sustituir la fecha histórica de la carátula por una fecha inferida sin distinguir su carácter aproximado.

## Estado de la propuesta

**Estado vigente del 9 de noviembre:** se completó el piloto español en Colab con T4: cinco ajustes, dos ciclos y una cadena por condición. Pasaron los 13 controles del protocolo y las pruebas PyTorch. Se archivaron ZIP y notebook ejecutado y se verificaron registros, mezclas, semillas y métricas léxicas localmente. Véase el [resumen del piloto](../Experimentos/resultados/piloto_es_2026-11-09/RESUMEN.md). Después, el usuario aceptó preparar el notebook principal reanudable y armonizar el artículo; ambas tareas están realizadas. **El estudio principal no se inició.**

## Protocolo principal v1 preparado — 9 de noviembre

Notebook: [experimento_principal_es.ipynb](../Experimentos/experimento_principal_es.ipynb); instrucciones y límites: [README_PRINCIPAL_ES.md](../Experimentos/README_PRINCIPAL_ES.md). La aceptación del usuario comprende esta preparación, no la ejecución de 48 ajustes en esta tarea ni aprobación del profesor.

- Se mantienen los recursos del piloto. Revisiones fijadas: generador `02e3092372e8a8b20c64e29350a024a998a7c00d`, corpus `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`, codificador `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`.
- Prefijo de 2000 artículos; regla SHA-256 80/10/10 aproximada y semilla `20261109` conservadas del piloto. Selección de 512 ejemplos de entrenamiento, 128 de validación y 128 de prueba; una ventana original de 64+128 tokens por artículo. El principal prepara la reserva de prueba que el piloto no tokenizó. Sin sustitución silenciosa ante duplicados o candidatos insuficientes.
- Proporciones 0/.5/1 de objetivos sintéticos, cinco ciclos y tres repeticiones. Tres M0 y 45 ajustes posteriores; mismo modelo preentrenado y optimizador nuevo en cada ajuste. En 50 %, las 256 posiciones sintéticas permanecen fijas por repetición entre ciclos; se generan 512 objetivos antes de mezclar. Contextos originales siempre.
- Una época, 65 536 tokens objetivo y 64 actualizaciones por ajuste; microbatch 2, lote efectivo 8. AdamW: lr 2e-5, betas .9/.999, epsilon 1e-8, decay .01, clipping 1; float32, sin scheduler/AMP/TF32. Muestreo T=1, top-p=.95 y 128 tokens excluyendo IDs especiales.
- Distinct-2/3, repetición de 4-gramas, dispersión MiniLM multilingüe y PPL sobre objetivos originales de prueba. W se fija solo con validación, hasta 32 palabras; encoder limitado a 128 wordpieces. Métricas por etapa guardadas, resumen al finalizar, sin adaptar parámetros al test. Contrastes descriptivos pareados con M0 y control del mismo ciclo; cadena como unidad de repetición.
- Drive persistente optativo mediante montaje personal; banderas de montaje y ejecución desactivadas al entregar. Primera ejecución limitada a una etapa. Hashes de código/configuración/entorno, artefactos y lotes; una sola sesión escritora. Reanuda entre ajustes y lotes; un ajuste incompleto vuelve a base y semilla, sin restaurar el optimizador a mitad de época. Checkpoints Safetensors de M0 y último necesario; purga de pesos propios anteriores tras confirmar la etapa sucesora, manteniendo corpus y resultados.
- Pasaron 20 controles locales y los mismos 20 embebidos; sintaxis y autonomía verificadas. El nuevo flujo PyTorch/checkpoints/Drive no se ejecutó; sus pruebas diminutas están incluidas para la primera sesión. La estimación de 2.67 h del piloto no incluye el costo adicional de persistencia ni garantiza la duración final.
- `Manuscrito/main.tex` ya describe este diseño en español; se corrigió también la delimitación que aún declaraba todos los parámetros pendientes. Compilación exitosa, 18 referencias citadas: fichas de recursos españoles sustituyen las dos inglesas. No hay exportación de PDF independiente ni inspección visual nueva. El piloto permanece separado de los resultados finales.

**Ejecución anterior interrumpida:** la extensión de Chrome permitió leer el notebook y conectarlo a una T4. Se inició Ejecutar todas; finalizó instalación y se interrumpió durante imports por la aclaración de español. Se verificó `KeyboardInterrupt` y ausencia de ejecución activa. Sin entrenamiento ni resultados. Reiniciar la sesión antes de ejecutar la nueva versión para limpiar imports parciales.

## Configuración ejecutada en el piloto en español

Los recursos siguientes fueron selección operativa del agente para el piloto, ejecutado dentro de la autorización del usuario; el **idioma español es decisión del usuario**. Se comprobó una ejecución con estos recursos y escala en T4. El protocolo y la factibilidad del estudio completo siguen pendientes de fijación y ejecución.

| Elemento | Propuesta actual |
| --- | --- |
| Generador | `datificate/gpt2-small-spanish`, GPT-2 pequeño adaptado desde un checkpoint inglés con Wikipedia española. Ajuste de todos los parámetros. |
| Corpus | `wikimedia/wikipedia`, `20231101.es`; lectura streaming de un prefijo de hasta 2000 artículos. |
| Particiones | Propias, por SHA-256 de semilla e ID de artículo: 80/10/10 aproximado. Una ventana por artículo elegible. La reserva de prueba no se tokeniza ni evalúa. No confundir con particiones oficiales. |
| Muestra piloto | 64 artículos de entrenamiento, 32 de validación; contexto 64 y objetivo 128 tokens; dos ciclos, 0/100 %, una repetición, cinco ajustes. |
| Semántica | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, mean pooling enmascarado, L2, límite 128 wordpieces y truncamientos registrados. |
| Preprocesamiento | Unicode NFC, tildes y ñ conservadas; sin stemming ni quitar palabras vacías. |
| Entrenamiento y generación | Mantiene los controles propuestos de reinicio desde base, AdamW, presupuestos, semillas separadas, longitud fija y política EOS del piloto anterior. Pruebas diminutas adaptadas a GPT-2. |

Se registran IDs, URLs, hashes de texto/ventanas, offsets, revisiones y versiones. Se detiene ante duplicados o muestra insuficiente. El prefijo no es una muestra representativa de toda Wikipedia. No se certifica autoría humana de cada texto ni ausencia de solapamiento con la adaptación previa del modelo a Wikipedia. Estas limitaciones afectan la interpretación de la referencia y la PPL.

Fuentes primarias consultadas el **9 de noviembre de 2026**: [generador](https://huggingface.co/datificate/gpt2-small-spanish), [corpus](https://huggingface.co/datasets/wikimedia/wikipedia), [codificador](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), [límite del codificador](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/sentence_bert_config.json) y [streaming](https://huggingface.co/docs/datasets/stream). Se descartó BNE al comprobar deprecación y ausencia de pesos/configuración en su árbol actual. Al preparar el piloto no se modificó la bibliografía del artículo; después se sustituyeron las fichas metodológicas al armonizarlo, como se registra arriba. No se cambió la fecha de consulta de la revisión inicial. Detalles en [README_ES.md](../Experimentos/README_ES.md).

**Antecedente del 8 de noviembre:**

Se redactó la sección Metodología en `Manuscrito/main.tex`. Los valores siguientes son una **configuración propuesta para verificar en piloto**, no un experimento realizado, ni una confirmación de viabilidad. El usuario dejó un notebook de Colab abierto y autorizó trabajar allí; el control de navegador terminó por imposibilidad de verificar la URL tanto en Brave como en Chrome. No se leyó ni modificó su contenido. El usuario aceptó la alternativa de un notebook local completo, con imports. Se creó [Experimentos/piloto_model_collapse.ipynb](../Experimentos/piloto_model_collapse.ipynb), autónomo para subir a Colab. No se descargaron modelos o datos ni se inició entrenamiento.

## Configuración anterior — pendiente de adaptar a español

Los recursos e idioma de esta tabla se conservan para trazabilidad, no como selección vigente. El resto de valores sigue siendo propuesto hasta validar un piloto en español.

| Elemento | Propuesta |
| --- | --- |
| Modelo | `facebook/opt-125m`, base, ajuste de todos los parámetros. |
| Corpus | `Salesforce/wikitext`, subconjunto `wikitext-2-raw-v1`. |
| Idioma y tarea | Inglés en la propuesta anterior; **sustituido por español** el 9 de noviembre. Se mantiene continuación de texto como tarea propuesta. |
| Ejemplos por ciclo | 512; bloques no solapados de un mismo artículo, contexto 64 tokens + continuación 128 tokens. |
| Proporciones | 0 %, 50 %, 100 % de tokens objetivo sintéticos. Contextos humanos fijos en las tres. |
| Generaciones | Una inicial sobre humanos + cinco ciclos posteriores. |
| Repeticiones | Tres cadenas por condición, con punto inicial compartido entre condiciones dentro de cada repetición. |
| Inicialización | Cada ajuste desde el mismo checkpoint preentrenado, optimizador reiniciado. Dependencia recursiva a través del corpus, no de pesos acumulados. |
| Ajuste inicial | Una época, tasa 2e-5, AdamW, lote efectivo 8. Enmascarar contexto y relleno. |
| Presupuesto objetivo | 65 536 tokens de continuación y 64 actualizaciones por ajuste. |
| Generación | Temperatura 1, top-p 0.95, sin penalización de repetición ni beam search. Tratamiento de EOS por fijar en piloto. |
| Evaluación | 128 contextos fijos de prueba; nunca generar datos de entrenamiento desde prueba. |
| Métricas | Distinct-2/3, repetición de 4-gramas, dispersión de embeddings y perplejidad en referencias humanas. |
| Inferencia | Trayectorias, cambios frente a inicial y control, magnitudes y variabilidad de cadenas. Exploratorio por pocas réplicas. |

El diseño completo implica **48 ajustes**: tres iniciales y 45 posteriores. Cada salida adicional tiene costo de generación autorregresiva: no estimar duración considerando solo los pasos de entrenamiento.

## Piloto y criterios de fijación

- 64 ejemplos de entrenamiento, 32 contextos de validación, proporciones 0 y 100 %, dos ciclos y una repetición.
- Comprobar que los tensores de etiquetas no aprendan el contexto ni el relleno.
- Comprobar inicialización idéntica del checkpoint y reinicio de optimizador en cada ciclo.
- Cronometrar por separado carga, ajuste, generación de corpus, evaluación, embeddings y escritura de archivos.
- Verificar cómo se obtienen 128 posiciones objetivo sin introducir una política desigual de EOS, longitudes o rechazo por condición.
- Fijar revisión del modelo, dataset, modelo de embeddings, límite léxico común y todos los parámetros del optimizador antes de ejecutar la evaluación final.
- Guardar manifiesto de decisiones del piloto; no ajustar parámetros para provocar el colapso.
- Estimar tiempo completo con margen para interrupciones y redacción; el piloto no garantiza disponibilidad continua de Colab.

## Plan de cuatro días, sujeto a tiempos medidos

1. **Día 1:** preparar entorno y piloto; fijar corpus, generación, métricas y escala viable.
2. **Día 2:** ejecutar cadenas con guardado de configuraciones y salidas; atender interrupciones sin cambiar criterios según resultados.
3. **Día 3:** completar métricas y controles; producir tablas y gráficas y revisar ejemplos por regla fija.
4. **Día 4:** redactar resultados, discusión y conclusiones, revisar coherencia y compilar la entrega.

No programar todas las horas del último día como cómputo. Si hay que reducir, hacerlo antes de las comparaciones finales, preferentemente en ejemplos o ciclos y conservando condiciones y réplicas cuando sea viable. Si no caben tres réplicas, limitar el alcance inferencial explícitamente; no sustituirlas por muchos textos de una cadena.

## Qué queda fuera del mínimo

- Comparar múltiples modelos o idiomas.
- Implementar todas las mitigaciones del estado del arte.
- Evaluación sintáctica, MAUVE y Self-BLEU como obligaciones simultáneas.
- Afirmar pérdida de colas sin una medición específica previa.
- Probar un umbral universal de colapso o declarar causalidad general.

Estas exclusiones operativas deberán armonizarse con las dimensiones conceptuales del marco y las conclusiones. No se cambió la hipótesis original; su interpretación se limita al diseño que finalmente se ejecute.

## Entorno local observado

La consulta CIM de RAM, equipo y GPU fue rechazada por falta de acceso al recurso. Una lectura posterior del registro devolvió **AMD Ryzen 5 5600G with Radeon Graphics** como procesador. No se verificaron RAM, VRAM ni capacidad CUDA; no se infiere de esa observación ausencia de otra GPU. `nvidia-smi` no se localizó mediante la consulta realizada. No se solicitaron permisos elevados ni se modificó el sistema.

## Fuentes de elección de recursos

- [Ficha de OPT-125m](https://huggingface.co/facebook/opt-125m): modelo base y condiciones de uso. Antecedente experimental en Shumailov, ya citado.
- [Ficha de WikiText](https://huggingface.co/datasets/Salesforce/wikitext): configuraciones, particiones y licencias indicadas.
- Se consultó [SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) como alternativa, pero no se incluyó en el diseño mínimo.

Las fichas se consultaron el 8 de noviembre de 2026 y se citaron en el artículo. La bibliografía del artículo pasó a 17 referencias. Los hiperparámetros propuestos son una decisión de diseño para piloto, no una afirmación de que ya estén validados por las fichas o por una reproducción exacta del paper.

## Verificación

La metodología redactada compiló en una tarea anterior. No se modificó LaTeX al crear o ejecutar el notebook. El piloto español sí tiene ejecución integrada comprobada, cinco ajustes completos y artefactos archivados. Sin PDF nuevo. Se inspeccionó la salida de Colab y se guardó una captura.

### Resultados y tiempos de piloto — 9 de noviembre

- PyTorch `2.14.1+cu130`, Transformers `5.22.2`, Datasets `5.1.0`, Tesla T4. Generador de 124 439 808 parámetros. Revisiones fijadas en el manifiesto descargado.
- De 2000 artículos: 1461 candidatos de entrenamiento, 202 de validación y 199 reservados como prueba (sin tokenizar); 138 artículos cortos de entrenamiento/validación. Se seleccionaron 64/32.
- Cada ajuste registró el mismo hash inicial, optimizador nuevo, ocho actualizaciones y 8192 tokens objetivo. Generaciones de validación de 128 tokens; métricas sobre 32 palabras. Sin textos cortos ni truncamientos del codificador en las cinco etapas.
- PPL: M0 29.4677; control final 29.4150; cadena sintética final 31.9012. No hubo caída sostenida de diversidad. Una cadena y dos ciclos no permiten inferencia estadística ni demostrar colapso.
- 212.20 s entre marcas del manifiesto, 210.97 s de etapas cronometradas. Excluye instalación y controles previos. Los cinco ajustes sumaron 49.68 s y las generaciones 76.70 s. No extrapolar solo desde ajuste.
- La extrapolación lineal del cálculo a la propuesta de 48 ajustes resulta aproximadamente 2.67 h bajo supuestos explícitos del resumen. Es orientación presupuestaria, no una duración validada ni ejecución iniciada.
- Se recomputaron localmente las métricas léxicas y se comprobaron particiones, semillas y presupuestos. Perplejidad y embeddings proceden de Colab, sin recomputación local. Se revisaron diez extractos por regla fija; hay incoherencias ya desde M0 y tres caracteres U+FFFD en total, conservados sin filtrar.
- La preparación principal y la armonización del artículo ya se realizaron después del piloto. Próximo paso: comprobar primera etapa y reanudación en Colab con la evaluación reservada separada. No incorporar el piloto automáticamente como resultados definitivos.

## Notebook preparado — 8 de noviembre de 2026

Registro histórico del estado de aquella entrega inglesa; sus pendientes de ejecución quedaron sustituidos por la preparación y ejecución españolas descritas arriba. No continuar esa copia como protocolo vigente.

- [Notebook autónomo](../Experimentos/piloto_model_collapse.ipynb), con instalación, imports, controles, cinco ajustes, métricas, gráficas y descarga de ZIP.
- [Instrucciones y fuentes de código](../Experimentos/README.md); [verificación real](../Experimentos/VERIFICACION.md).
- Se verificaron siete controles offline del protocolo y sintaxis de las 22 celdas. Las pruebas PyTorch diminutas están incluidas, pero pendientes de ejecución, igual que las descargas y el piloto.
- Se propone para el piloto excluir todos los tokens especiales durante generación, incluido EOS, y fijar 128 tokens. Es una restricción de decodificación que debe declararse; no se presenta como decisión final del usuario.
- Se concreta MiniLM `sentence-transformers/all-MiniLM-L6-v2`, mean pooling con máscara y normalización L2. Se usan primeras W palabras, con W fijado por referencias de validación y tope 32; se registra truncamiento del codificador a 256 wordpieces. Una etapa con textos cortos informa ausencia de métricas léxicas/semánticas sin descartar ejemplos.
- AdamW propuesto: betas .9/.999, epsilon 1e-8, weight decay .01 uniforme, clipping 1, sin scheduler; float32, sin AMP/TF32, determinismo estricto. Estas concreciones son propuestas operativas del agente, no resultados validados.
- Revisiones de modelo/dataset/codificador y versiones se resolverán y registrarán al ejecutar. Generadores separados por solicitud; semillas de evaluación pareadas entre etapas y separadas de entrenamiento/generación de corpus.
- No se guardan checkpoints por defecto; se conservan datos, semillas, configuraciones y salidas. Opción explícita para guardarlos antes de ejecutar. Carpetas nuevas y archivos parciales; sin reanudación automática. `/content` debe descargarse antes de cerrar Colab.
- La configuración sigue limitada al piloto. El estudio final requiere fijación posterior del protocolo y cómputo viable. El artículo no se actualizó automáticamente con estas propuestas.
