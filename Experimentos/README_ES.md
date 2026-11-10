# Notebook nuevo en español

Archivo para importar: **[piloto_model_collapse_es.ipynb](piloto_model_collapse_es.ipynb)**.

Es autónomo: solo se sube ese `.ipynb`. Incluye instalación, imports, controles, cinco ajustes del piloto, métricas, gráficas y descarga del ZIP. El notebook anterior en inglés se conserva sin sobrescribir. **El usuario ya lo importó y el piloto español se ejecutó el 9 de noviembre.** La fuente se conserva como plantilla; la copia ejecutada con salidas y el ZIP están en [resultados/piloto_es_2026-11-09](resultados/piloto_es_2026-11-09/RESUMEN.md).

Para repetirlo, usar una sesión limpia con GPU y las celdas en orden. Si la instalación solicita reiniciar, hacerlo y continuar con imports. Se comprobó una ejecución completa en Tesla T4, PyTorch 2.14.1+cu130, Transformers 5.22.2 y Datasets 5.1.0. El procesamiento registrado duró 212.20 s, aparte de instalación y controles previos; no garantiza duración ni disponibilidad en otra sesión.

## Recursos propuestos para el piloto

| Recurso | Selección y motivo |
| --- | --- |
| Generador | `datificate/gpt2-small-spanish`: GPT-2 pequeño adaptado a español, manejable para un piloto acotado. Su ficha declara adaptación desde el GPT-2 inglés con Wikipedia española. |
| Corpus | `wikimedia/wikipedia`, `20231101.es`: registros de artículos en español; streaming acotado para preparar la muestra. |
| Semántica | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`: codificador multilingüe; mean pooling con máscara, normalización L2 y límite de 128 wordpieces de su configuración. |

Se conserva el piloto de 64 ejemplos de entrenamiento, 32 de validación, dos ciclos, 0/100 % de objetivos sintéticos y una repetición. Los contextos son siempre originales. Cada uno de los cinco ajustes vuelve al checkpoint preentrenado y al optimizador nuevo.

Wikipedia tiene una sola partición oficial. Se crean particiones propias por hash de ID de artículo: 80/10/10 aproximado. Se recorre un prefijo de hasta 2000 artículos y se elige una ventana de 64+128 tokens por artículo elegible; después se muestrean las cantidades del piloto. Los artículos de prueba se omiten antes de tokenizar. Se detectan duplicados sin reemplazarlos silenciosamente. El límite del prefijo y sus sesgos quedan documentados; no es una muestra representativa de Internet.

Se preservan tildes y ñ mediante Unicode NFC. Distinct-2/3, repetición de 4-gramas y dispersión semántica usan una longitud común de hasta 32 palabras; la perplejidad se calcula sobre objetivos originales de validación. Las muestras generadas se guardan, sin filtrar por idioma/calidad. Un modelo adaptado al español puede producir errores o texto de otros idiomas; esos casos forman parte de lo que debe inspeccionarse.

El corpus no certifica autoría humana de cada texto. El generador ya fue adaptado a Wikipedia: no se garantiza ausencia de solapamiento con su entrenamiento previo. No presentar la evaluación como evidencia de conocimientos nuevos ni el idioma/modelo como novedad científica.

## Fuentes y elección descartada

Consultadas el 9 de noviembre de 2026:

- [Ficha del generador](https://huggingface.co/datificate/gpt2-small-spanish) y [archivos](https://huggingface.co/datificate/gpt2-small-spanish/tree/main).
- [Corpus y licencias](https://huggingface.co/datasets/wikimedia/wikipedia).
- [Codificador multilingüe](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) y [configuración de longitud](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/sentence_bert_config.json).
- [Streaming de Datasets](https://huggingface.co/docs/datasets/stream).

Se consideró `PlanTL-GOB-ES/gpt2-base-bne`, pero su ficha indica que está deprecado y su árbol actual solo muestra metadatos/documentación, sin pesos ni configuración. No se seleccionó un recurso cuya descarga de pesos no pudo verificarse. Esto no es una evaluación experimental de calidad entre modelos.

## Verificación y mantenimiento

Se comprobaron **13 controles offline**, incluidos los seis específicos de español, tanto desde los módulos como embebidos en el notebook. Se validaron las 22 celdas, JSON, IDs, imports completos, autonomía y sintaxis. Después pasaron en Colab los 13 controles y las pruebas PyTorch, y terminaron los cinco ajustes. Se descargaron el ZIP y el notebook con sus 12 celdas de código ejecutadas y sin salidas de error. Se verificaron los archivos y se recalcularon métricas léxicas localmente mediante `verificar_resultados_es.py`. No se modificó el artículo durante el piloto; después se armonizó al preparar el estudio principal.

Fuentes nuevas: `piloto_colab_es.py`, `controles_es.py`, `test_controles_es.py` y `crear_notebook_es.py`. Regenerar con `py -3.12 Experimentos/crear_notebook_es.py`; no hacerlo sobre una copia ejecutada sin conservar sus salidas.

La revisión proporcional de seguridad está en [VERIFICACION.md](VERIFICACION.md). El código no requiere claves, no ejecuta código remoto de repositorios y no actúa sobre el contenido generado. No se hizo una auditoría del entorno Colab ni se prometen tiempos de ejecución.

## Continuación preparada

El [notebook principal](experimento_principal_es.ipynb) conserva el idioma y los recursos del piloto, amplía la muestra y añade persistencia/reanudación. Ver [README_PRINCIPAL_ES.md](README_PRINCIPAL_ES.md). No se han ejecutado sus 48 ajustes ni se reemplazaron los resultados del piloto.
