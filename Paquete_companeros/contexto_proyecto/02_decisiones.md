# Decisiones y delimitaciones

Actualizado: 9 de noviembre de 2026.

## Base de trabajo acordada

- **Idioma confirmado por el usuario el 9 de noviembre:** los textos de entrenamiento, generación y evaluación deben estar en español. El usuario lo recordó como acuerdo previo; las notas guardadas lo mantenían pendiente. Se corrige el estado actual sin inventar la fecha de aquel acuerdo. La propuesta del agente con OPT-125m/WikiText en inglés queda sustituida. Ya se preparó un nuevo notebook español, pendiente de importación y ejecución.
- Investigación de IMAC, FES Acatlán, UNAM.
- Título de trabajo: **Contenido sintético en Internet y degradación de modelos de lenguaje**. Puede refinarse; no hay un reemplazo confirmado.
- Objeto: cambios en diversidad y repetición del texto generado por reutilización recurrente de datos sintéticos, considerando proporción sintética y número de generaciones.
- Internet muerto funciona como motivación, no como teoría que se pretenda demostrar ni como estimación de cuánto contenido de Internet es artificial.
- Alcance previsto: modelos compactos, datos controlados y recursos limitados. No se plantea entrenar grandes modelos desde cero.
- El estudio debe permitir que los resultados no confirmen el deterioro esperado.

## Separación de documentos — aclaración expresa del usuario

- [Manuscrito/main.tex](../Manuscrito/main.tex) es el artículo de investigación.
- Las actividades de preguntas y la propuesta/justificación del capitulado son documentos separados. No insertarlas como entregables completos dentro del artículo.
- El capitulado orienta qué contenido desarrollar; no debe reproducirse como una lista de capítulos ya redactados.
- La justificación de la investigación sí puede formar parte de la introducción; no confundirla con justificar por qué se eligió cada capítulo.
- La redacción del artículo se realiza sobre el archivo existente, conservando la pestaña del editor salvo petición contraria.

## Formulaciones de investigación

La pregunta principal vigente es:

> ¿Cómo cambia la diversidad del contenido generado por modelos de lenguaje cuando se incorporan repetidamente datos sintéticos al proceso de entrenamiento?

Las cinco preguntas secundarias y las versiones de hipótesis se mantienen en las secciones 9 y 11 del [contexto maestro](../model_collapse_proyecto_contexto.md). Consultarlas antes de modificar objetivos o hipótesis.

- El artículo conserva la hipótesis del Main proporcionado: disminución progresiva de diversidad y aumento de repetición, con efectos esperados más pronunciados según proporción y generaciones.
- Hay una propuesta de refinamiento condicionada al protocolo en la revisión bibliográfica. No fue aprobada como reemplazo definitivo.
- El objetivo general y los cinco objetivos específicos de la introducción fueron redactados por el agente a partir de las preguntas; siguen pendientes de revisión del usuario.
- No asumir equivalencia literal entre las versiones de hipótesis del contexto y del artículo: conservar procedencia y someter cualquier unificación a revisión.

## Estructura y tiempo

- **Información del usuario del 8 de noviembre:** se dispone de aproximadamente cuatro días y puede utilizarse este equipo o Colab. No se confirmó fecha/hora exacta ni GPU disponible. Esto sustituye el estado anterior de plazo completamente desconocido.
- El usuario solicitó retirar Organización del documento del artículo y del capitulado revisado. La entrega histórica se conserva sin cambios; registrar la diferencia de versión.
- Se redactó una primera versión del marco teórico con búsqueda académica y citas; no supone selección definitiva de modelos, datos ni métricas. Véase [fuentes del marco](05_fuentes_marco_teorico.md).
- Referencia entregada: [capitulado completo](01_capitulado_entregado.md).
- Trabajo futuro es complementario y opcional, sujeto al tiempo y a los requisitos de la asignatura.
- La revisión local incorpora 7.6 como alternativa al capítulo 8. Ese apartado no aparece en lo entregado.
- Hay un plazo aproximado de cuatro días; la fecha y hora exactas no han sido proporcionadas.
- La carátula del artículo conserva «28 de septiembre de 2026» por proceder del Main enviado; no es confirmación de la fecha límite vigente.
- La fecha del capitulado, «18 de octubre de 2026», corresponde a elaboración.

## Propuestas que NO son decisiones cerradas

El 8 de noviembre se avanzó en la redacción del estado del arte y su matriz conceptual. El contenido es un borrador para revisión del usuario; las implicaciones de diseño siguen siendo recomendaciones, no selección definitiva de un protocolo.

**El idioma ya se confirmó: español.** El 9 de noviembre el usuario aceptó preparar el protocolo principal descrito en [07_propuesta_metodologia.md](07_propuesta_metodologia.md) y armonizar el artículo. La configuración v1 está concretada en código; esto no prueba su ejecución completa ni constituye aprobación del profesor. Las pruebas inferenciales adicionales y el refinamiento de objetivos e hipótesis siguen abiertos.

El 8 de noviembre se concretó una propuesta para piloto: OPT-125m y WikiText-2 en inglés, tres proporciones, cinco ciclos y tres réplicas. El detalle está en [07_propuesta_metodologia.md](07_propuesta_metodologia.md). Sustituye la ausencia de una propuesta operativa, pero no equivale a validación de factibilidad, ejecución o aprobación definitiva de cada parámetro.

El diseño inglés del 8 de noviembre es un antecedente sustituido. Los recursos españoles ya se ejecutaron en el piloto y se conservaron para el notebook principal: 512/128/128 ejemplos, 0/50/100 %, cinco ciclos y tres repeticiones. El presupuesto fijo y las métricas están implementados en esa propuesta v1; el flujo completo con Drive aún requiere comprobación. No presentarlo como experimento principal ejecutado.

## Registro breve de decisiones

- **9 de noviembre de 2026 (preparación principal):** tras revisar el piloto, el usuario respondió «vale» a preparar un notebook completo con reanudación y armonizar la metodología en español. Se creó `Experimentos/experimento_principal_es.ipynb` sin reemplazar el piloto. El artículo incorpora el protocolo de 48 ajustes y 18 referencias, con compilación exitosa. La preparación se entrega con ejecución desactivada y primera etapa limitada a un ajuste; no se montó Drive ni se inició el estudio principal.
- **9 de noviembre de 2026 (ejecución):** tras importar el archivo español, el usuario autorizó trabajar en su pestaña de Chrome. Colab mostró límite de sesiones y el usuario informó que cerró todas. Se reconectó T4 y completó el piloto de cinco ajustes. Se conservaron ZIP y notebook ejecutado, sin cambiar parámetros ni iniciar el estudio final. Los resultados se registran como piloto, separados de hipótesis y resultados definitivos.
- **9 de noviembre de 2026 (nuevo archivo):** el usuario pidió crear otro notebook y dijo que él lo importará y avisará. Se creó `Experimentos/piloto_model_collapse_es.ipynb`, conservando el anterior. Modelo español, corpus y codificador multilingüe son propuestas del agente para el piloto; no aprobación del profesor ni validación de ejecución. No se actuó en Colab ni se modificó el artículo en esta tarea.
- **9 de noviembre de 2026:** el usuario corrigió el idioma hacia español antes de continuar. Se interrumpió el notebook en imports, tras instalar dependencias y conectar GPU T4. Sin entrenamiento. Corresponde seleccionar modelo/corpus/codificador adecuados, adaptar el notebook y armonizar después la metodología del artículo.
- **8 de noviembre de 2026 (notebook):** el usuario autorizó trabajar en su Colab abierto y, tras el bloqueo de la herramienta de navegador, aceptó entregar un notebook local completo con imports. Se creó `Experimentos/piloto_model_collapse.ipynb`. Esto autoriza su preparación; no convierte la configuración propuesta en protocolo final ni prueba ejecución o disponibilidad de GPU.
- **3 de noviembre de 2026:** retiro de Organización del documento del artículo y revisión local del capitulado; redacción del marco teórico con ampliación de fuentes. La transcripción entregada no se modifica.
- **18 de octubre de 2026:** coherencia de tono y alcance entre entregables; Trabajo futuro opcional; correcciones de voz y estructura en revisión local.
- **3 de noviembre de 2026:** el Main será el artículo; se retiró la unión inicial de entregables.
- **3 de noviembre de 2026:** se inició la introducción y se distinguió el capitulado entregado de la revisión local.
- **3 de noviembre de 2026:** se creó esta carpeta para consultar y mantener las referencias del proyecto.

Para una decisión nueva, registrar fecha, indicación del usuario, alcance y qué propuesta sustituye. No registrar la aprobación del profesor si solo existe feedback de procedencia no confirmada.

