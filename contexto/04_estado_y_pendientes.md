# Estado y pendientes

Actualizado: 10 de noviembre de 2026.

## Revisión vigente para entrega — 10 de noviembre

El artículo actual desarrolla los siete capítulos centrales, 18 referencias y anexos A–B. La fuente original, con babel español y newtx, compiló correctamente en el compilador del editor durante esta revisión. Se comprobaron los 48 marcadores del estudio y 240 hashes de archivos de etapas, sin discrepancias. Se inspeccionó la figura PNG; sigue pendiente revisar visualmente todas las páginas del PDF final. Esta comprobación sustituye el pendiente antiguo de compilar únicamente una copia con babel inglés.

La revisión considera el trabajo completo y defendible para la asignatura. El usuario autorizó aplicar los ajustes y se incorporaron: ausencia de tendencia sostenida en el control, cumplimiento parcial del objetivo de repetición entre textos, recordatorio del análisis post hoc sobre 90 contextos en conclusiones y cautela sobre la dirección del sesgo de selección. El estado del arte ya describe la evaluación realizada. La versión corregida compiló correctamente en el editor. Se sincronizan `Overleaf_IMAC/` y `Overleaf_IMAC.zip` y se prepara el envío autorizado a `CarLos4475/IMAC`. No se cambiaron cifras ni se ejecutaron entrenamientos nuevos.

## Material disponible y su estado

| Material | Estado comprobado |
| --- | --- |
| [Artículo](../Manuscrito/main.tex) | Artículo completo con resultados, discusión, conclusiones, 18 referencias y anexos A–B; fuente original compilada el 10 de noviembre. Revisión de redacción y maquetación final recomendada. |
| [Capitulado entregado](01_capitulado_entregado.md) | Estructura transcrita del adjunto identificado por el usuario; no hay confirmación de aprobación del profesor. |
| [Capitulado revisado](../Capitulado/main.tex) | Correcciones locales de coherencia, voz y apartado 7.6; compilación verificada anteriormente. |
| [Revisión bibliográfica](../revision_estado_del_arte.md) | Nueve trabajos seleccionados; revisión inicial consultada el 13 de octubre de 2026. |
| [Contexto maestro](../model_collapse_proyecto_contexto.md) | Formulaciones, inventario e historial del proyecto. |
| [Notebook piloto anterior](../Experimentos/piloto_model_collapse.ipynb) | Versión inglesa conservada como antecedente. Se interrumpió durante imports, sin entrenamiento. Sustituida operativamente por el nuevo archivo español; no continuar esta copia. |
| [Notebook español](../Experimentos/piloto_model_collapse_es.ipynb) | Piloto ejecutado en T4: cinco ajustes completos; controles del protocolo y PyTorch pasaron. Fuente conservada sin sobrescribir con salidas. |
| [Resultados de piloto](../Experimentos/resultados/piloto_es_2026-11-09/RESUMEN.md) | ZIP, notebook ejecutado, métricas, tiempos, captura y comprobación local archivados. Una repetición por condición y dos ciclos; no son resultados finales. |
| [Fuente del estudio principal](../Experimentos/README_PRINCIPAL_ES.md) | Notebook autónomo conservado como fuente, con ejecución desactivada al distribuir; las 48 etapas se completaron en una copia en Colab y sus salidas están archivadas aparte. |
| [Estudio principal ejecutado](../Experimentos/resultados/principal_es_2026-11-10/RESUMEN.md) | 48/48 etapas el 10 de noviembre; resultados, análisis complementario post hoc y tablas/figura incorporados en `main.tex`. |

El 3 de noviembre se verificaron nuevamente Shumailov y Kazdan para la introducción y se amplió la búsqueda con fuentes de fundamentos para el marco teórico. El registro está en [05_fuentes_marco_teorico.md](05_fuentes_marco_teorico.md). Esto no constituye una revisión sistemática.

La introducción actual tiene seis subapartados; el capítulo 1 del entregable proponía diez. Organización del documento se eliminó de la revisión local por indicación del usuario. La correspondencia restante es temática; queda pendiente decidir si se desea correspondencia literal de encabezados. Los objetivos redactados y el marco teórico requieren revisión del usuario.

Ya existen resultados propios del **piloto** español ejecutado el 9 de noviembre. El estudio principal se completó el 10 de noviembre (48/48 etapas) y sus resultados están en [principal_es_2026-11-10/RESUMEN.md](../Experimentos/resultados/principal_es_2026-11-10/RESUMEN.md). El artículo incluye Resultados, Discusión y Conclusiones y sus ajustes de precisión ya están aplicados y compilados. Pendientes inmediatos: revisar todas las páginas del PDF final y confirmar su exportación para entrega. La limpieza de temporales y la celda adicional de Colab son mantenimiento opcional, no requisitos de la entrega. Las métricas léxicas y semánticas provienen de un análisis complementario post hoc declarado en el texto.

## Pendientes de redacción y coordinación

1. Revisar la introducción y los objetivos propuestos.
2. Decidir el grado de correspondencia de sus encabezados con el capitulado entregado.
3. Se confirmó un plazo aproximado de cuatro días y este equipo o Colab. Precisar hora de entrega, validar disponibilidad de cómputo y revisar la fecha histórica de la carátula.
4. Revisar los borradores del marco teórico y del estado del arte; profundizar en los antecedentes metodológicos elegidos. El estado del arte ya fue redactado el 8 de noviembre, sin cerrar el diseño.
5. Mantener separados el artículo y los entregables de planificación.

## Pendientes metodológicos

- Hecho el 10 de noviembre: guardado, reanudación y las 48 etapas se completaron en Colab T4 (~2.8 h registradas).
- La metodología describe la ejecución completa: recursos españoles del piloto, 512/128/128 ejemplos, tres proporciones, cinco ciclos, tres repeticiones y 48 ajustes desde la misma base. No hay confirmación de aprobación del profesor.
- Mantener la reserva de prueba fuera del ajuste de parámetros y conservar la misma regla de partición del piloto. Registrar sin filtrar problemas de generación y métricas ausentes.
- Verificar reanudación con los hashes y el entorno congelado; preservar salidas, checkpoints necesarios y una sola sesión escritora.
- El análisis implementado es descriptivo y pareado; cualquier prueba inferencial adicional requiere justificación y no debe tratar textos como réplicas independientes.
- Ajustar objetivos e hipótesis cuando el diseño se cierre.

## Pendientes bibliográficos

- Leer íntegramente los antecedentes elegidos como base experimental.
- Preparar matriz comparable de tareas, modelos, datos, ciclos, presupuesto y métricas.
- Revisar repositorios pertinentes.
- Profundizar en antecedentes en español; el idioma ya está confirmado.
- Verificar publicación y versión antes de incorporar nuevas citas.

## Cómo cambiar estados

Mover un pendiente a realizado solo con evidencia concreta. Registrar fecha, archivo afectado y comprobación. Si se descarta o sustituye una propuesta, indicar el motivo sin presentarla como un resultado negativo del experimento.


## Paquete para el equipo (10 de noviembre de 2026)
Se creó `Paquete_companeros/` (y `Paquete_companeros.zip`) con reglas y cifras, prompts para LLM, contexto completo en un solo archivo, artículo, resultados, código y contexto del proyecto, para que el equipo humanice el texto sin alterar cifras ni advertencias.
