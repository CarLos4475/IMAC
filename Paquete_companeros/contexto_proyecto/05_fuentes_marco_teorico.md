# Fuentes y búsqueda para el marco teórico

Fecha de búsqueda y registro: 3 de noviembre de 2026.

## Alcance real de la búsqueda

**Estado posterior:** el 8 de noviembre se redactó el estado del arte y se añadió Gerstgrasser como referencia 15 del artículo. Este archivo conserva la procedencia de la ampliación del marco; la nueva comparación se documenta en [06_comparacion_estado_del_arte.md](06_comparacion_estado_del_arte.md).

**Recursos metodológicos actualizados el 9 de noviembre:** al armonizar el artículo con el piloto español, las fichas de OPT y WikiText se sustituyeron por las de [GPT-2 español](https://huggingface.co/datificate/gpt2-small-spanish), [Wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) y [MiniLM multilingüe](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2), consultadas ese día. El artículo tiene **18 referencias, todas citadas**: 15 antecedentes/fundamentos y tres fichas de recursos. Claves nuevas: `spanishmodelcard`, `wikipediacard` y `multilingualcard`; retiradas `optmodelcard` y `wikitextcard`. No son tres nuevos estudios sobre colapso ni una nueva revisión sistemática; la fecha histórica de búsqueda del marco permanece arriba.

Se utilizó búsqueda web en repositorios y actas académicas: JMLR, ACL Anthology, NeurIPS, PMLR y arXiv. Se comprobaron títulos, autores, año y publicación en registros primarios; se consultaron resúmenes y apartados del texto completo pertinentes, especialmente métricas en Guo, Li y Texygen. No se afirma lectura íntegra de todos los artículos ni una revisión sistemática.

No se consultó directamente Google Scholar. Las consultas se dirigieron a las fuentes originales, evitando citar agregadores como evidencia. OpenReview presentó una verificación de navegador; para Holtzman se usó el registro arXiv, que confirma publicación en ICLR 2020. El DOI de Texygen no resultó accesible con el navegador de búsqueda; el registro de UCL y el PDF de autores proporcionaron vías alternativas.

Se aplicó la habilidad de gestión de plugins para buscar herramientas académicas. Se encontró **Scite**, se ofreció su conexión y después el usuario lo conectó. Se continuó la misma tarea con búsquedas por DOI, títulos y términos en Scite, contrastando los hallazgos pertinentes con las actas primarias. No se encontró una integración directa de Google Scholar en esa búsqueda; el catálogo no es exhaustivo.

## Referencias del marco registradas el 3 de noviembre

| Clave LaTeX | Fuente primaria | Uso principal |
| --- | --- | --- |
| `bengio2003` | [Bengio et al. (2003), A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html) | Distribuciones de secuencias y modelado neuronal. |
| `vaswani2017` | [Vaswani et al. (2017), Attention Is All You Need](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) | Arquitectura Transformer y atención. |
| `holtzman2020` | [Holtzman et al., The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) | Decodificación, muestreo y repetición. ICLR 2020; preprint inicial 2019. |
| `wang2023selfinstruct` | [Wang et al. (2023), Self-Instruct](https://aclanthology.org/2023.acl-long.754/) | Ajuste con instrucciones y generación/filtrado de ejemplos sintéticos. |
| `shumailov2024` | [Shumailov et al. (2024), AI models collapse when trained on recursively generated data](https://www.nature.com/articles/s41586-024-07566-y) | Colapso, errores acumulados y pérdida de colas. Ya citado previamente. |
| `kazdan2025` | [Kazdan et al. (2025), Collapse or Thrive](https://proceedings.mlr.press/v267/kazdan25a.html) | Diferencias entre reemplazo, acumulación y subconjuntos de tamaño fijo. Ya citado previamente. |
| `zhu2025` | [Zhu et al. (2025), How to Synthesize Text Data without Model Collapse?](https://proceedings.mlr.press/v267/zhu25d.html) | Datos semisintéticos, concentración de patrones y edición de tokens. |
| `drayson2025` | [Drayson et al. (2025), Machine-generated text detection prevents language model collapse](https://aclanthology.org/2025.emnlp-main.1506/) | Separar rendimiento, generación y semejanza con referencias. |
| `guo2024` | [Guo et al. (2024), The Curious Decline of Linguistic Diversity](https://aclanthology.org/2024.findings-naacl.228/) | Diversidad léxica, sintáctica y semántica; límites de métricas. |
| `li2016` | [Li et al. (2016), A Diversity-Promoting Objective Function for Neural Conversation Models](https://aclanthology.org/N16-1014/) | Distinct-n como medida léxica. |
| `reimers2019` | [Reimers y Gurevych (2019), Sentence-BERT](https://aclanthology.org/D19-1410/) | Representaciones de oraciones y similitud coseno. |
| `zhu2018texygen` | [Zhu et al. (2018), Texygen](https://arxiv.org/abs/1802.01886) | Self-BLEU y evaluación de diversidad; [registro institucional](https://discovery.ucl.ac.uk/id/eprint/10066104/). |
| `pillutla2021` | [Pillutla et al. (2021), MAUVE](https://papers.nips.cc/paper_files/paper/2021/hash/260c2432a0eecc28ce03c10dadc078a4-Abstract.html) | Comparación distribucional de texto humano y generado. |
| `suresh2025` | [Suresh, Thangaraj y Khandavally (2025), Rate of Model Collapse in Recursive Training](https://proceedings.mlr.press/v258/suresh25a.html) | Tasas de colapso bajo distribuciones simplificadas; distinguir existencia y rapidez. Encontrado en Scite como preprint de 2024 y contrastado con AISTATS 2025. |

El artículo pasó de 2 a 13 referencias durante la primera ampliación y a **14** tras continuar con Scite. Algunas ya estaban identificadas en la revisión inicial; no son doce hallazgos enteramente nuevos del campo. Ocho trabajos de fundamentos amplían esa revisión: Bengio, Vaswani, Holtzman, Wang, Li, Reimers, Texygen y MAUVE; se añade Suresh como antecedente sobre tasas de colapso.

## Continuación con Scite conectado

- Búsqueda por DOI de Shumailov y Guo; búsqueda `"model collapse" AND (recursive OR accumulation OR diversity)` y consulta por títulos de acumulación y tasas.
- Scite devolvió para Shumailov un aviso de corrección: DOI `10.1038/s41586-025-08905-3`, fechado el 21 de marzo de 2025. Ya estaba registrado; se mantiene como precaución para usar sus ecuaciones.
- Los fragmentos de cita recuperados de Shumailov distinguen repetición y colapso, en línea con la distinción conceptual del marco. No se interpretaron los contadores de citas como confirmación de verdad.
- Para Guo, el registro retornado omitía el primer autor, Yanzhu Guo. Se conserva la autoría de ACL Anthology. No sustituir metadatos primarios por registros incompletos.
- Scite encontró Suresh mediante el DOI de preprint `10.48550/arxiv.2412.17646`; `read_fulltext` no devolvió texto legible. Se consultaron las actas de AISTATS 2025 y su PDF en PMLR para respaldar el párrafo añadido y la autoría completa. El texto señala que, en ciertos escenarios de estimación simplificados, el olvido puede requerir muchas iteraciones; no deriva una tasa universal para LLMs.
- Otros candidatos recuperados: *SIGMA: Scalable Spectral Insights for LLM Model Collapse* (`10.48550/arxiv.2601.03385`), *When Sample Selection Bias Precipitates Model Collapse* (`10.48550/arxiv.2606.13732`) y *Reviewing Model Collapse and Countermeasures* (`10.48550/arxiv.2608.21366`). Se dejan pendientes de examen y verificación de versión; no se añadieron al artículo por aparecer en resultados.
- La ausencia de `editorialNotices` en un resultado significa que esa respuesta no aportó avisos, no una certificación de ausencia de correcciones o retractaciones.
- Compilación exitosa tras incorporar Suresh. El artículo tiene 14 referencias citadas. No hubo edición de colecciones ni subida de archivos a Scite.

## Consultas representativas

- `site.jmlr.org Bengio Ducharme Vincent Jauvin 2003 neural probabilistic language model`
- `site.papers.nips.cc Attention Is All You Need 2017 Vaswani`
- `site.aclanthology.org A Diversity-Promoting Objective Function Neural Conversation 2016 Li`
- `site.aclanthology.org Sentence-BERT Sentence Embeddings Siamese BERT Networks 2019`
- `site.arxiv.org The Curious Case of Neural Text Degeneration Holtzman 1904.09751`
- `site.aclanthology.org Self-Instruct Aligning Language Models Self Generated Instructions 2023`
- `site.proceedings.neurips.cc MAUVE Measuring the Gap Neural Text Human Text 2021`

## Qué respalda este marco y qué sigue abierto

- Los conceptos y ecuaciones son fundamentos de modelado, no resultados del proyecto.
- Las definiciones operativas de datos humanos, generación y política de mezcla deberán concretarse al cerrar el diseño.
- No se eligieron automáticamente TTR, Distinct-n, Self-BLEU, Sentence-BERT, perplejidad o MAUVE por describirlos aquí.
- La representación semántica debe validarse para el idioma elegido. Los modelos generadores y de representación cumplen funciones distintas.
- El estado del arte sigue pendiente como sección del artículo: el marco establece conceptos, no sustituye la comparación crítica detallada.
- La revisión inicial conserva su fecha de consulta del 13 de octubre; este archivo documenta una ampliación posterior.

## Verificación documental

Se retiró Organización del documento del artículo y del capitulado revisado. Se conserva en la transcripción histórica de lo entregado y se registra la diferencia. Compilación exitosa de ambos archivos LaTeX el 3 de noviembre de 2026; sin exportación de PDF ni inspección visual independiente.
