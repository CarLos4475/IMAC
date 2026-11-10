# Comparación para el estado del arte

Actualizado: 8 de noviembre de 2026.

## Alcance

Primera redacción de la sección 3 de `Manuscrito/main.tex`, con nueve subapartados correspondientes a la estructura revisada. Revisión dirigida, no sistemática ni exhaustiva. Se contrastaron registros y resúmenes primarios y se consultaron apartados pertinentes de los textos. No se afirma lectura integral ni reproducción de todos los estudios.

## Matriz de lectura

| Trabajo | Tipo y eje | Hallazgo relevante | Límite de comparación | Decisión que orienta, todavía pendiente |
| --- | --- | --- | --- | --- |
| [Shumailov et al., 2024](https://doi.org/10.1038/s41586-024-07566-y) | Análisis teórico y ajuste de OPT-125m sobre WikiText-2; generación por búsqueda en haz. | Pérdida de información y cambios entre generaciones. | No representa cualquier política sintética ni cualquier decodificación. Aviso de corrección de 2025 ya registrado. | Precisar referencia inicial, inicialización, generación y qué se considerará evidencia de deterioro. |
| [Guo et al., 2024](https://doi.org/10.18653/v1/2024.findings-naacl.228) | Ajuste recursivo y diversidad en tareas en inglés. | Dimensiones léxica, sintáctica y semántica muestran diferente sensibilidad. | Idioma, tarea y longitud condicionan métricas y comparación. | Elegir dimensiones y validar instrumentos para el idioma seleccionado. |
| [Gerstgrasser et al., 2024](https://doi.org/10.48550/arXiv.2404.01413) | Preprint v2; comparación de reemplazo y acumulación. | Conservar originales y acumular datos evita deterioro en los escenarios estudiados. | Corpus creciente y presupuesto creciente no equivalen a tamaño fijo. | Definir si se conserva el corpus y cuánto de él se usa. |
| [Kazdan et al., 2025](https://proceedings.mlr.press/v267/kazdan25a.html) | Reemplazo, acumulación total y subconjuntos fijos en varios escenarios. | Cambia la trayectoria de pérdida de prueba según el procedimiento. | Estabilidad de pérdida no prueba conservación de toda diversidad. | Fijar presupuesto y separar fidelidad de diversidad. |
| [Zhu et al., 2025](https://proceedings.mlr.press/v267/zhu25d.html) | Proporciones sintéticas y edición de tokens humanos. | Concentración de n-gramas y mejoras mediante datos semisintéticos en sus configuraciones. | Editar texto humano no equivale a producir documentos enteramente sintéticos. | Definir construcción del dato y unidad de proporción. |
| [Drayson et al., 2025](https://doi.org/10.18653/v1/2025.emnlp-main.1506) | GPT-2/SmolLM2, decodificación y remuestreo guiado por detector. | La generación y selección de datos modifican las trayectorias. | Calidad del detector, tamaño fijo y estrategias de generación delimitan el resultado. | Controlar muestreo, longitudes y evaluar más que variedad superficial. |
| [Suresh et al., 2025](https://proceedings.mlr.press/v258/suresh25a.html) | Tasas teóricas para distribuciones simplificadas, con simulaciones. | La escala temporal del olvido depende de muestras y supuestos de estimación. | No proporciona directamente una tasa de colapso para LLMs. | Justificar duración del experimento y describir magnitudes sin exigir colapso completo. |

Esta matriz es conceptual. Sigue pendiente extraer de los antecedentes metodológicos seleccionados las configuraciones completas: dataset, tamaño, ciclos, semillas, inicialización, repeticiones y presupuesto. No sustituye esa extracción ni cierra el experimento.

## Consultas y verificaciones del 8 de noviembre

- Scite: consulta por DOI de Shumailov, Guo, Drayson y ForTIFAI, con términos `diversity OR decoding OR confidence`.
- Fuentes primarias: páginas PMLR de Kazdan, Zhu y Suresh; registro arXiv v2 de Gerstgrasser; PDF de ACL de Guo y Drayson; búsqueda en Nature para la configuración de Shumailov.
- Se verificó otra vez el aviso de corrección de Shumailov en Scite. La ausencia de avisos en otros registros no certifica ausencia de correcciones.
- El registro de Scite de Guo sigue omitiendo su primer autor; se mantiene la autoría de ACL. Para Drayson, Scite devuelve páginas 29645–29661, pero el PDF de la publicación consultada indica 29657–29673; se conservan estas últimas, ya usadas en el manuscrito.
- Nature bloqueó la apertura de ForTIFAI y su corrección de Shumailov mediante redirección. No se añadieron nuevas afirmaciones sobre ForTIFAI ni se incorporó como referencia al artículo en esta tarea.
- No se usaron los contadores o etiquetas automáticas de citas como demostración de un hallazgo.

## Estado del artículo

- Sección de estado del arte redactada como borrador sujeto a revisión del usuario.
- Se añadió únicamente `gerstgrasser2024`; hay 15 referencias y las 15 están citadas.
- Hipótesis, modelo, datos, idioma, proporciones, ciclos y métricas no se cambiaron ni se dieron por cerrados.
- Compilación exitosa mediante el editor. No se exportó PDF ni se inspeccionó visualmente en esta tarea.
- Las guías de estudio independientes no se modificaron ni integraron al artículo.
