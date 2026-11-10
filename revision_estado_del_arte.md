# Revisión del estado del arte: entrenamiento recursivo y model collapse

Fecha de consulta: 13 de octubre de 2026.

**Ampliación posterior:** el 3 de noviembre de 2026 se buscó literatura de fundamentos para el marco teórico y se añadieron citas al artículo. El registro de fuentes, consultas y límites está en [contexto/05_fuentes_marco_teorico.md](contexto/05_fuentes_marco_teorico.md). Este archivo conserva la revisión inicial y su fecha; la ampliación no constituye una revisión sistemática ni un estado del arte ya redactado en el artículo.

## Alcance de esta revisión

Revisión bibliográfica inicial orientada al proyecto de Investigación en Matemáticas Aplicadas y Computación. Se buscaron estudios sobre reutilización recursiva de texto sintético, diversidad lingüística, mezcla y conservación de datos y mitigación. Se priorizaron fuentes primarias: Nature, ACL Anthology, PMLR, actas de ICLR y arXiv. Se verificaron metadatos y resúmenes de los trabajos seleccionados y se consultaron apartados metodológicos y de resultados de Shumailov, Guo, Drayson y ForTIFAI. No constituye una revisión sistemática ni una lectura exhaustiva de todos los artículos.

Consultas empleadas: “model collapse recursive synthetic data accumulation language models”, “linguistic diversity recursive training”, “How to Synthesize Text Data without Model Collapse”, “Strong Model Collapse” y búsquedas de publicaciones de 2025–2026. Se excluyeron como evidencia las noticias, los agregadores y las afirmaciones sobre cuánto contenido de Internet es sintético.

## Trabajos centrales y lectura crítica

### 1. Shumailov et al. (2024): fundamento del fenómeno

**AI models collapse when trained on recursively generated data.** Nature, 631, 755–759. [Artículo](https://www.nature.com/articles/s41586-024-07566-y).

Combina análisis de distribuciones simplificadas con experimentos de ajuste de OPT-125m. Describe pérdida de eventos poco probables y deterioro mediante generaciones sucesivas. Es el fundamento para estudiar fidelidad a la distribución inicial, además de repetición.

**Límite:** sus resultados deben interpretarse dentro de los supuestos teóricos y protocolos empleados; no establecen un porcentaje universal de datos sintéticos que produzca colapso.

**Aplicación:** comparar cada generación con datos originales reservados y observar patrones poco frecuentes. El uso de un modelo compacto ya tiene precedente.

Existe una [corrección de marzo de 2025](https://www.nature.com/articles/s41586-025-08905-3): en una condición de la sección teórica, beta sustituye a alfa. Consultar la versión corregida si se reproducen sus ecuaciones. El preprint de 2023, *The Curse of Recursion*, es antecedente de este trabajo; no debe contarse como evidencia experimental independiente.

### 2. Guo et al. (2024): antecedente más cercano a la pregunta principal

Yanzhu Guo, Guokan Shang, Michalis Vazirgiannis y Chloé Clavel. **The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text.** Findings of NAACL 2024, 3589–3604. [Artículo y PDF](https://aclanthology.org/2024.findings-naacl.228/).

Estudia ajuste recursivo en tareas en inglés y distingue diversidad léxica, sintáctica y semántica. Utiliza TTR, Distinct-n, Self-BLEU y distancias entre representaciones de oraciones. La reducción léxica y sintáctica es más clara; la diversidad semántica resulta relativamente más estable.

**Límite:** no conviene describir todas las dimensiones como si disminuyeran con la misma intensidad. Los autores señalan límites al trasladar las métricas a otros idiomas. Controlan la longitud al comparar TTR y Distinct-n.

**Aplicación:** es lectura prioritaria para operacionalizar “diversidad”. La pregunta del proyecto ya tiene antecedentes directos; la contribución debe especificar qué condiciones se reproducen o comparan.

### 3. Gerstgrasser et al. (2024): reemplazo frente a acumulación

**Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data.** Preprint arXiv:2404.01413. [Registro primario](https://arxiv.org/abs/2404.01413).

Contrasta sustituir los datos originales con conservarlos y acumular generaciones sintéticas. En sus experimentos, la acumulación evita el colapso observado con el reemplazo.

**Límite:** conservar y entrenar con un corpus creciente no equivale a extraer una muestra de tamaño fijo de ese corpus. Tampoco demuestra conservación universal de todas las dimensiones de diversidad.

**Aplicación:** definir si los datos originales se conservan, se sustituyen o se vuelven a muestrear. La proporción sintética no describe por sí sola el protocolo.

### 4. Kazdan et al. (2025): el presupuesto de datos cambia la interpretación

Joshua Kazdan, Rylan Schaeffer, Apratim Dey, Matthias Gerstgrasser, Rafael Rafailov, David L. Donoho y Sanmi Koyejo. **Collapse or Thrive: Perils and Promises of Synthetic Data in a Self-Generating World.** ICML 2025, PMLR 267, 29469–29494. [Publicación](https://proceedings.mlr.press/v267/kazdan25a.html).

Compara reemplazo, acumulación con uso de todos los datos y acumulación con subconjuntos de tamaño fijo. Evalúa estimación gaussiana, densidad y ajuste de modelos de lenguaje. El reemplazo produce colapso; usar toda la acumulación mantiene estable la pérdida de prueba; restringir el tamaño permite deterioro gradual.

**Límite:** estabilidad de pérdida de prueba no equivale a demostrar que toda la diversidad permanece intacta.

**Aplicación:** declarar si la comparación mantiene constantes los tokens de entrenamiento o permite que crezcan. Esta decisión puede explicar diferencias entre estudios.

### 5. Zhu et al. (2025): proporciones, concentración y síntesis alternativa

**How to Synthesize Text Data without Model Collapse?** ICML 2025, PMLR 267, 79746–79771. [Publicación](https://proceedings.mlr.press/v267/zhu25d.html).

Analiza diferentes proporciones sintéticas, cambios distribucionales y concentración de n-gramas. Propone edición de tokens de textos humanos para construir datos semisintéticos y evalúa preentrenamiento, preentrenamiento continuo y ajuste supervisado.

**Límite:** su mitigación preserva estructura de textos humanos; no equivale a generar documentos completos sin referencia humana. Sus resultados no fijan un umbral universal para todas las tareas y modelos.

**Aplicación:** fundamenta la comparación de proporciones y el análisis de patrones repetidos. En la bibliografía del proyecto conviene actualizar la referencia: existe una publicación de 2025, además del preprint arXiv:2412.14689 de 2024.

### 6. Drayson, Yilmaz y Lampos (2025): la decodificación y la curación importan

**Machine-generated text detection prevents language model collapse.** EMNLP 2025, 29657–29673. [Artículo y PDF](https://aclanthology.org/2025.emnlp-main.1506/).

Estudia estrategias de decodificación y propone remuestreo guiado por un detector de texto sintético. Evalúa GPT-2 y SmolLM2, de 124M a 1.7B parámetros. Utiliza diversidad, Self-BLEU, MAUVE y medidas de rendimiento.

**Límite:** las mejoras corresponden a sus escenarios y a la capacidad del detector. Algunos resultados mantienen alta diversidad mientras empeoran la calidad y el rendimiento: variedad superficial no basta para establecer salud del modelo. Su comparación de acumulación usa un tamaño fijo por generación.

**Aplicación:** controlar temperatura, top-k/top-p y estrategia de generación; acompañar diversidad con evaluación sobre datos humanos reservados.

### 7. Dohmatob et al. (ICLR 2025): otra definición de colapso

Elvis Dohmatob, Yunzhen Feng, Arjun Subramonian y Julia Kempe. **Strong Model Collapse.** [Artículo en actas de ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/284afdc2309f9667d2d4fb9290235b0c-Paper-Conference.pdf), [preprint de 2024](https://arxiv.org/abs/2410.04840).

Estudia un deterioro en el escalamiento del error: aumentar los datos puede dejar de mejorar el rendimiento bajo contaminación sintética. El análisis central usa regresión supervisada y aproximaciones de modelos, con validaciones adicionales.

**Límite:** esta noción no equivale directamente a repetición textual o pérdida semántica. Los resultados con fracciones pequeñas no deben convertirse en una regla sobre cualquier LLM.

**Aplicación:** definir explícitamente qué significado de colapso utiliza el proyecto y qué indicadores pueden respaldarlo.

### 8. Shabgahi et al. (2026): mitigación mediante el objetivo de entrenamiento

Soheil Zibakhsh Shabgahi, Pedram Aghazadeh, Azalia Mirhoseini y Farinaz Koushanfar. **ForTIFAI: fending off recursive training induced failure for AI model collapse.** npj Artificial Intelligence, 2, artículo 70, publicado el 4 de julio de 2026. [Artículo](https://www.nature.com/articles/s44387-026-00127-w).

Propone pérdidas sensibles a la confianza, incluida entropía cruzada truncada, para reducir el peso de tokens de alta confianza. Reporta mayor resistencia al deterioro y evalúa retención de conocimiento y divergencia distribucional.

**Límite:** los experimentos usan actualización de todos los parámetros y modelos de hasta 1.5B. Extender sus conclusiones a modelos mayores o ajustes parciales requiere validación.

**Aplicación:** muestra que el objetivo de entrenamiento también modifica el proceso. Es una referencia reciente para mitigación, aunque reproducirla no es indispensable para este proyecto.

### 9. Liu y Han (2026): control del muestreo y revisión de conclusiones

**Break Step: Recursive Training Resonates with Replayed Sampling Noise.** Preprint arXiv:2609.11149v3, revisado el 29 de septiembre de 2026. [Versión consultada](https://arxiv.org/abs/2609.11149v3).

Los autores atribuyen parte de una pérdida rápida de diversidad a compartir y repetir semillas de muestreo en vLLM. Al modificar ese mecanismo cambian los resultados. El registro aclara que la primera versión tenía otro título, *A Fragility Spectrum for Recursive Language-Model Training*, y que sus conclusiones fueron revisadas sustancialmente.

**Límite:** es un preprint reciente; no refuta por sí solo la literatura sobre colapso ni establece que todo deterioro sea un artefacto.

**Aplicación:** documentar versiones, semillas por muestra y por generación, y comprobar duplicados. No citar la versión inicial como si describiera los resultados actuales.

## Síntesis para el proyecto

La literatura seleccionada sugiere estudiar condiciones de aparición e intensidad del deterioro. La pregunta general sobre cambios en diversidad tiene antecedentes; la hipótesis debe permitir resultados distintos según el protocolo. Una formulación de trabajo sería:

> Bajo un protocolo de entrenamiento y generación definido, la proporción de datos sintéticos y el número de generaciones modifican las métricas de diversidad y repetición del contenido; se evaluará si esos cambios corresponden a una disminución de diversidad y si dependen de la conservación de datos originales.

Esta es una propuesta editorial y metodológica derivada de la comparación, no un resultado experimental ni una conclusión textual de un solo artículo.

### Aportación defendible

Una reproducción controlada y accesible puede ser adecuada para la materia. Trabajar con modelos pequeños, por sí solo, no distingue el proyecto. La aportación debe concretarse en modelo, tarea, idioma, presupuesto y protocolo.

Posible objetivo, pendiente de recursos y datos:

> Comparar la evolución de diversidad léxica, diversidad semántica y repetición en un modelo compacto, variando proporción sintética y número de generaciones con un presupuesto fijo de tokens y condiciones de generación controladas.

Si se trabaja en español, validar las herramientas lingüísticas y las representaciones utilizadas. Esta revisión no demuestra que no existan estudios previos en español; antes de reclamar novedad por idioma hace falta una búsqueda específica.

### Decisiones necesarias antes de cerrar el diseño

1. Definir una generación: entrenamiento o ajuste, generación de nuevos datos y evaluación. Precisar si cada ciclo parte del modelo base o del checkpoint anterior.
2. Separar reemplazo, mezcla y acumulación. Registrar qué datos humanos permanecen y si el corpus crece.
3. Establecer una condición sin datos sintéticos con entrenamiento comparable y un conjunto humano de evaluación reservado.
4. Controlar presupuesto de tokens, longitudes, prompts y configuración de muestreo. Distinguir semillas de entrenamiento y generación y usar repeticiones independientes.
5. Seleccionar métricas que respondan a dimensiones diferentes; evitar sumar indicadores redundantes sin justificación.
6. Evaluar diversidad junto con fidelidad o rendimiento. Una secuencia incoherente puede presentar muchos n-gramas únicos.
7. Medir patrones poco frecuentes respecto de una referencia explícita; la repetición sola no demuestra pérdida de las colas.
8. Identificar la unidad de réplica experimental: las respuestas de una misma cadena de entrenamiento no son entrenamientos independientes.

### Estructura sugerida del estado del arte

1. Evidencia inicial y mecanismos de pérdida distribucional: Shumailov.
2. Diversidad lingüística como objeto de evaluación: Guo.
3. Mezcla, reemplazo, acumulación y presupuesto de entrenamiento: Gerstgrasser y Kazdan.
4. Generación y selección de datos sintéticos: Zhu y Drayson.
5. Definiciones y mitigaciones recientes: Dohmatob, ForTIFAI y, con su carácter provisional, Liu y Han.
6. Comparación crítica y delimitación del experimento propio.

No convertir el capítulo en una lista de resúmenes: cada apartado debe comparar protocolos, indicadores y límites, y terminar explicando qué decisión orienta en el estudio.

## Pendientes de la revisión

**Estado al 8 de noviembre de 2026:** la primera sección de estado del arte ya está integrada en el artículo con siete antecedentes centrales. La comparación y sus límites están en [contexto/06_comparacion_estado_del_arte.md](contexto/06_comparacion_estado_del_arte.md). Permanecen pendientes la extracción metodológica completa y la revisión del borrador; la fecha inicial de este documento se conserva.

- Extraer en una matriz detallada datasets, tamaños, ciclos, repeticiones, inicialización y presupuesto de cada experimento que se vaya a reproducir.
- Leer íntegramente los artículos elegidos como base experimental y consultar sus repositorios antes de implementar.
- Ampliar la búsqueda sobre experimentos y métricas en español si ese será el idioma de trabajo.
- Seleccionar el antecedente metodológico según los recursos reales de cómputo.
- Revisar y profundizar la sección de estado del arte integrada en el LaTeX; completar configuraciones de los antecedentes que se elijan para reproducir.
