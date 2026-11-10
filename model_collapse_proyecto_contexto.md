# Proyecto de investigación — Model Collapse y contenido sintético

**Última actualización del contexto:** 10 de noviembre de 2026.
**Archivo maestro de trabajo:** `model_collapse_proyecto_contexto.md`, en la raíz de `IMAC`.  
**Referencias organizadas:** [contexto/README.md](contexto/README.md), con capitulado entregado, decisiones, criterios editoriales y pendientes. Consultar esa carpeta además del estado general de este documento.
**Mantenimiento:** seguir `AGENTS.md` y actualizar este archivo al concluir avances sustantivos. La copia de Descargas se sincronizó al establecer este maestro; las actualizaciones posteriores se realizan aquí, salvo solicitud de sincronización externa.

**Estado comprobado en la revisión de entrega del 10 de noviembre:** el artículo actual contiene los siete capítulos centrales, referencias y anexos A–B; el principal está completo (48 etapas). La fuente original `Manuscrito/main.tex`, con babel español y newtx, compiló correctamente en el compilador del editor. Se comprobaron 48 marcadores y los hashes de 240 archivos de etapas, sin discrepancias; se confirmaron 39 etapas sin métricas léxicas originales y 75 continuaciones cortas. Se inspeccionó la figura PNG, no la maquetación de todas las páginas ni un PDF exportado. Este estado sustituye las descripciones antiguas de ejecución/compilación pendiente que aún aparecen abajo. La carátula actual indica entrega el 11 de noviembre, conforme al cambio registrado previamente.

**Valoración de entrega (revisión, no aprobación del profesor):** trabajo completo y defendible como investigación académica exploratoria. El usuario pidió aplicar los ajustes el 10 de noviembre y se incorporaron al artículo: ausencia de tendencia sostenida en el control, cumplimiento parcial del objetivo de repetición entre textos, recordatorio en conclusiones del análisis post hoc de 90 contextos y cautela sobre la dirección del sesgo de selección. Se retiró el lenguaje de diseño pendiente en el estado del arte. La fuente corregida y la copia Overleaf compilaron correctamente en el editor. No se modificaron cifras, protocolo ni resultados experimentales; no se hicieron nuevos entrenamientos. `Overleaf_IMAC/` y `Overleaf_IMAC.zip` quedaron sincronizados: ocho archivos del ZIP verificados mediante SHA-256. Los cambios se publicaron con autorización del usuario en `CarLos4475/IMAC`, rama `main`, commit `3056349`. La revisión visual del PDF completo sigue pendiente.

> **Documento maestro de contexto para agentes de IA**
>
> Este archivo consolida el estado actual del proyecto de investigación de la materia **Investigación en Matemáticas Aplicadas y Computación**. Debe utilizarse como contexto de trabajo y no como una versión definitiva del paper. Los elementos marcados como **provisionales**, **pendientes** o **por verificar** no deben tratarse como decisiones finales.

---

## 1. Identidad y contexto académico

- **Materia:** Investigación en Matemáticas Aplicadas y Computación.
- **Institución:** UNAM, Facultad de Estudios Superiores Acatlán.
- **Tema general actual:** contenido sintético en Internet, entrenamiento recurrente de modelos de lenguaje y *model collapse*.
- **Tema/título de trabajo usado hasta ahora:** `Contenido sintético en Internet y degradación de modelos de lenguaje`.
- El título todavía puede modificarse conforme avance la investigación.
- **Integrantes:** Carlos Emiliano Segura Loera; Valeria Hernandez Santos; Nehiel Ramirez Hernandez.
- **Profesor:** Sergio Quiroz Almaraz.
- **Lugar de la carátula:** Naucalpan de Juárez, Estado de México.
- Los nombres se conservan como aparecen en los archivos proporcionados. No modificar su escritura sin indicación del usuario.
- La carátula de la actividad de capitulado usa **18 de octubre de 2026 como fecha de elaboración**, no como fecha de entrega confirmada. El Main.tex original indicaba una entrega anterior, del 28 de septiembre de 2026.

---

# 2. Idea central del proyecto

El proyecto parte del crecimiento de contenido generado mediante inteligencia artificial en Internet y lo conecta con el fenómeno conocido como **model collapse**.

La idea inicial surgió a partir de la llamada **Dead Internet Theory / teoría del Internet muerto**, que plantea un escenario en el que una proporción considerable del contenido y de las interacciones de Internet es producida por sistemas automatizados.

### Importante: qué SÍ y qué NO estudia el proyecto

**NO se pretende:**

- demostrar que la teoría del Internet muerto sea verdadera;
- calcular qué porcentaje actual de Internet es generado por IA;
- demostrar que Internet ya esté "muerto";
- estudiar de manera general todas las consecuencias sociales de la IA generativa.

**SÍ se pretende:**

- utilizar el concepto de Internet muerto únicamente como **contexto y motivación**;
- estudiar un problema técnico que sí puede investigarse experimentalmente;
- analizar qué ocurre cuando contenido generado por modelos de lenguaje se reutiliza como datos para entrenar generaciones posteriores;
- estudiar particularmente cambios en **diversidad, repetición y distribución del contenido generado**;
- relacionar estos cambios con el fenómeno de **model collapse**.

---

# 3. Problema de investigación

Los modelos de lenguaje necesitan grandes cantidades de datos para su entrenamiento. Conforme aumenta la cantidad de contenido generado artificialmente, existe la posibilidad de que datos sintéticos terminen mezclándose con datos producidos originalmente por humanos y sean posteriormente utilizados para entrenar nuevos modelos.

El problema de investigación consiste en estudiar qué ocurre cuando este proceso se vuelve recurrente.

De forma simplificada:

```text
Datos originales
      ↓
Modelo / generación 1
      ↓
Contenido sintético
      ↓
Entrenamiento / generación 2
      ↓
Nuevo contenido sintético
      ↓
Entrenamiento / generación 3
      ↓
...
```

La preocupación es que, después de varias generaciones, puedan aparecer cambios sistemáticos en la distribución del contenido generado, como:

- disminución de diversidad;
- aumento de repetición;
- concentración alrededor de patrones frecuentes;
- pérdida de información asociada a casos poco frecuentes;
- cambios progresivos en la distribución de las respuestas.

La literatura previa sobre *model collapse* hace especialmente relevante la posibilidad de pérdida de información de las colas de la distribución y una concentración progresiva en patrones más comunes.

---

# 4. Motivación

El interés del proyecto surge de la conexión entre dos fenómenos:

1. El crecimiento del contenido generado por inteligencia artificial en Internet.
2. La necesidad de grandes cantidades de datos para entrenar nuevos modelos.

La pregunta motivadora es:

> ¿Qué ocurre cuando los modelos empiezan a consumir información generada por otros modelos?

El interés no es únicamente conceptual. Desde matemáticas aplicadas y computación, el problema permite estudiar propiedades estadísticas de las distribuciones generadas por los modelos y observar cómo cambian al aumentar la presencia de información sintética.

---

# 5. Justificación: factibilidad, interés, novedad, ética y relevancia

## Factibilidad

El proyecto debe mantenerse dentro de los recursos disponibles. Entrenar modelos grandes desde cero no es realista para un proyecto académico de tiempo limitado.

Se propone trabajar con:

- modelos de lenguaje pequeños o compactos;
- modelos disponibles públicamente;
- ejecución local cuando sea posible;
- conjuntos de datos de tamaño controlado;
- un número limitado de generaciones/ciclos.

El objetivo no es reproducir exactamente el entrenamiento de un modelo comercial grande, sino construir un experimento reducido y controlado que permita observar comportamientos relacionados con *model collapse*.

## Interés

El problema está relacionado directamente con el crecimiento reciente de la IA generativa y con la transformación de la información disponible en Internet.

## Novedad

**No se debe presentar model collapse como un fenómeno nuevo.**

El fenómeno ya ha sido estudiado. La posible aportación del proyecto consiste en diseñar y analizar un experimento accesible, reproducible y de escala reducida que permita observar sus efectos utilizando recursos limitados.

## Ética

El experimento no requiere:

- información personal;
- interacción con usuarios;
- datos privados.

Se pretende utilizar:

- datasets públicos;
- datos diseñados específicamente para el experimento;
- modelos disponibles públicamente.

## Relevancia

Comprender las consecuencias de reutilizar información sintética para alimentar nuevos sistemas de IA puede ser relevante para el desarrollo futuro de modelos generativos.

Conforme aumenta la cantidad de contenido producido mediante IA, puede adquirir mayor importancia distinguir y conservar información originalmente producida por humanos para la construcción de futuros conjuntos de entrenamiento.

---

# 6. Delimitación actual

**Idioma confirmado el 9 de noviembre de 2026: español.** El usuario lo recordó como acuerdo previo; las notas lo mantenían pendiente y se corrige ese estado. La propuesta del agente con OPT-125m y WikiText-2 en inglés queda sustituida. El piloto español ya se ejecutó; el notebook principal está preparado, con su flujo completo aún pendiente de comprobación. No se afirma una fecha anterior de aprobación que no se haya verificado.

La investigación se ha delimitado preliminarmente de la siguiente manera:

- Principalmente **modelos generativos de texto**.
- Modelos pequeños, compactos o disponibles para ejecución local.
- No entrenar LLM grandes desde cero.
- Trabajar con datasets de tamaño controlado.
- Estudiar sucesivas generaciones de generación/reutilización de contenido sintético.
- Medir principalmente:
  - diversidad léxica;
  - diversidad semántica;
  - repetición de palabras, frases o estructuras;
  - concentración de respuestas;
  - cambios en la distribución;
  - posible pérdida de patrones poco frecuentes.
- Internet muerto funciona únicamente como **contexto/motivación**.
- El foco técnico es **model collapse** y los cambios producidos por el uso recurrente de datos sintéticos.
- La configuración v1 está concretada en el notebook principal y en la metodología, pero su ejecución completa sigue pendiente. Cualquier cambio posterior deberá documentarse sin ajustarlo a resultados de prueba.

---

# 7. Dirección experimental preliminar

**Estado vigente del 9 de noviembre: piloto español completado y principal preparado.** Tras importar el notebook, el usuario autorizó trabajar en Chrome. Cerró las sesiones anteriores al aparecer el límite de Colab y se conectó una T4 nueva. Pasaron 13 controles del protocolo y las pruebas PyTorch; se completaron cinco ajustes (M0 y dos ciclos por condición, 0/100 %, una repetición), con GPT-2 pequeño adaptado al español, Wikipedia `20231101.es` y MiniLM multilingüe. Se archivaron ZIP, notebook con salidas, captura, corpus, métricas y tiempos en `Experimentos/resultados/piloto_es_2026-11-09/`. Registros y métricas léxicas se verificaron localmente. El manifiesto registra 212.20 s, excluyendo instalación/controles previos. Después el usuario aceptó preparar el notebook principal reanudable y armonizar el artículo: ambas tareas están realizadas. El estudio final no se inició. Véanse `contexto/07_propuesta_metodologia.md` y `Experimentos/README_PRINCIPAL_ES.md`.

**Principal v1 preparado, no ejecutado:** `Experimentos/experimento_principal_es.ipynb`, autónomo, 29 celdas. Mantiene recursos/revisiones del piloto; 512 ejemplos de entrenamiento, 128 de validación y 128 de prueba, contextos/objetivos de 64/128 tokens. Conserva la partición por artículo y semilla `20261109` para no trasladar artículos del piloto a prueba. Tres proporciones 0/.5/1, cinco ciclos, tres repeticiones: 48 ajustes desde la misma base, tres M0 compartidos dentro de repetición. En 50 %, las mismas 256 posiciones sintéticas por repetición entre ciclos; se generan 512 objetivos antes de mezclar. Una época, 65 536 tokens objetivo y 64 actualizaciones por ajuste. Métricas léxicas/semánticas y PPL con referencia original reservada; W se fija con validación, no con prueba. Resumen descriptivo pareado al finalizar, sin tratar textos como réplicas independientes.

**Persistencia preparada:** Drive mediante montaje personal, banderas de montaje/ejecución desactivadas y límite inicial de una etapa. Se congelan código, configuración y entorno; se comprueban hashes de corpus, registros y lotes. Reanudación entre ajustes/lotes; ajuste incompleto se repite desde base y semilla, sin reanudar optimizador. Checkpoints Safetensors: M0 y último necesario; pesos propios anteriores se purgan tras confirmar sucesor, manteniendo datos/resultados. Estimación de al menos unos 3 GB con margen y unos 24 GB de escrituras acumuladas, sin medir costo de Drive. Pasaron 20 controles locales y embebidos, sintaxis/autonomía; nuevo guardado PyTorch y flujo Drive pendientes de integración. No se montó Drive ni se entrenó en esta preparación. La estimación de 2.67 h excluye esa persistencia y no garantiza duración completa.

**Artículo armonizado el 9 de noviembre:** metodología de doce subapartados en español e introducción coherente con el protocolo v1. Tres fichas de recursos españoles sustituyen las dos inglesas; 18 referencias, todas citadas. Compilación exitosa; sin exportación de PDF independiente ni nueva inspección visual. El piloto se menciona como comprobación reducida y sus resultados se conservan separados de resultados finales.

**Resultado propio del piloto, no conclusión final:** PPL inicial 29.4677; control al segundo ciclo 29.4150; cadena sintética al segundo ciclo 31.9012. La diversidad no mostró una caída sostenida. Con una cadena y dos ciclos no se sostiene colapso general ni significación estadística. No incorporar el piloto automáticamente como resultados definitivos. Se midieron tiempos para orientar la escala, no para asegurar disponibilidad continua de GPU.

**Antecedente de conexión del 9 de noviembre:** tras instalar la extensión, se leyó Colab y conectó una T4. Se inició Ejecutar todas en la copia inglesa; finalizó instalación y se interrumpió durante imports por la corrección de idioma. Se verificó `KeyboardInterrupt` y ausencia de ejecución activa. No hubo entrenamiento. Conservar esa copia y reiniciar sesión antes de ejecutar la nueva.

**Notebook preparado el 8 de noviembre de 2026:** a petición del usuario se creó `Experimentos/piloto_model_collapse.ipynb`, autónomo para Colab, con instalación/imports, controles, cinco ajustes del piloto, métricas, gráficas y descarga de resultados. El usuario autorizó trabajar en el notebook abierto; el control de Brave y Chrome terminó porque la herramienta no pudo verificar la URL, sin leer ni modificar su contenido. Después aceptó la alternativa local. Se verificaron siete controles offline y sintaxis; no se ejecutaron PyTorch, descargas o entrenamiento. EOS sin tokens especiales, MiniLM y límite común de palabras son concreciones propuestas del agente para piloto, pendientes de validación; véase `contexto/07_propuesta_metodologia.md`. No se modificó el artículo ni se cerró el protocolo final.

**Actualización del 8 de noviembre de 2026:** el usuario confirmó aproximadamente cuatro días y posibilidad de usar esta computadora o Colab. Se concretó una propuesta de ajuste de OPT-125m con WikiText-2 en inglés: tres proporciones de continuaciones sintéticas, cinco ciclos y tres réplicas, con 512 ejemplos de contexto/continuación y evaluación reservada. La inicialización desde el mismo modelo preentrenado separa la transmisión por datos de la acumulación de pesos. Los contextos seguirían siendo humanos incluso al 100 % sintético de objetivos. La propuesta se documenta en `contexto/07_propuesta_metodologia.md` y en el artículo; sus valores dependen del piloto, que todavía no se ha ejecutado. No se afirma viabilidad ni se cambió la hipótesis.

Una posibilidad considerada es generar varias generaciones de contenido:

```text
Dataset / contenido inicial
        ↓
Modelo inicial
        ↓
Generación 0
        ↓
Entrenamiento / ajuste con datos sintéticos
        ↓
Generación 1
        ↓
Entrenamiento / ajuste
        ↓
Generación 2
        ↓
...
```

La salida de una generación podría utilizarse como parte de los datos de la siguiente generación.

Después se compararían las generaciones mediante métricas relacionadas con:

- diversidad léxica;
- diversidad semántica;
- repetición;
- concentración;
- representación de patrones frecuentes y poco frecuentes;
- eventualmente calidad de las respuestas.

### Variables que podrían manipularse

1. **Proporción de datos sintéticos**
   - por ejemplo, diferentes porcentajes de datos sintéticos mezclados con datos originales.

2. **Número de generaciones/ciclos**
   - comparar el comportamiento después de diferentes cantidades de generaciones.

### Variables de resultado

- diversidad;
- repetición;
- concentración/distribución;
- pérdida de información poco frecuente;
- otros indicadores que se definan después de la revisión bibliográfica.

> **Pendiente:** definir exactamente qué modelo(s), dataset(s), tarea(s), proporciones, número de generaciones y métricas se utilizarán.

---

# 8. Pregunta principal de investigación

> **¿Cómo cambia la diversidad del contenido generado por modelos de lenguaje cuando se incorporan repetidamente datos sintéticos al proceso de entrenamiento?**

Esta es la formulación actualmente preferida.

La pregunta está deliberadamente centrada en una dimensión concreta y medible: **la diversidad del contenido generado**.

---

# 9. Preguntas secundarias

Actualmente se propone trabajar con cinco preguntas secundarias:

### 1. Diversidad

> **¿Cómo cambia la diversidad léxica y semántica del contenido generado conforme aumenta el número de generaciones de entrenamiento con datos sintéticos?**

### 2. Proporción de datos sintéticos

> **¿Cómo influye la proporción de datos sintéticos utilizados durante el entrenamiento en la diversidad del contenido generado?**

### 3. Repetición

> **¿Cómo cambia la frecuencia de patrones, frases o estructuras repetitivas conforme se incorporan datos sintéticos de manera recurrente?**

### 4. Proporción × generaciones

> **¿Qué relación existe entre la proporción de datos sintéticos y el número de generaciones de entrenamiento en los cambios observados en la diversidad del contenido?**

### 5. Identificación de model collapse

> **¿Qué características del contenido generado permiten identificar la aparición de un proceso asociado con el *model collapse*?**

---

# 10. Por qué estas preguntas

Las preguntas están diseñadas para que el proyecto pueda convertirse posteriormente en un capitulado.

La estructura conceptual es:

```text
                         PREGUNTA PRINCIPAL
                                │
             ┌──────────────────┼──────────────────┐
             ↓                  ↓                  ↓
       Diversidad         Datos sintéticos     Repetición
             │                  │                  │
             └────────────┬─────┴──────────┬───────┘
                          ↓                ↓
                  Generaciones       Model collapse
```

Las preguntas secundarias permiten estudiar:

- diversidad léxica y semántica;
- efecto de la proporción de datos sintéticos;
- repetición de patrones;
- efecto acumulativo de las generaciones;
- características observables asociadas con *model collapse*.

Esto también permite que las preguntas apoyen posteriormente la construcción del capitulado y de la hipótesis.

---

# 11. Hipótesis

## Hipótesis de investigación actual

> **El entrenamiento recurrente de modelos de lenguaje utilizando contenido sintético produce cambios significativos en la diversidad y repetición del contenido generado, observándose una disminución de la diversidad y un incremento de la repetición conforme aumenta la proporción de datos sintéticos y el número de generaciones de entrenamiento.**

Esta es la formulación formal registrada en el contexto original. **No se ha aprobado una sustitución definitiva.** La revisión bibliográfica posterior sugiere acotarla al protocolo experimental y permitir efectos dependientes de la conservación de datos originales, el presupuesto y la generación del texto.

En `revision_estado_del_arte.md` se propuso una formulación alternativa de trabajo, todavía pendiente de decisión:
> Bajo un protocolo de entrenamiento y generación definido, la proporción de datos sintéticos y el número de generaciones modifican las métricas de diversidad y repetición del contenido; se evaluará si esos cambios corresponden a una disminución de diversidad y si dependen de la conservación de datos originales.

No reemplazar silenciosamente la hipótesis registrada ni convertir esta sugerencia en una decisión del usuario. La hipótesis nula también deberá operacionalizarse con parámetros y contrastes concretos; ausencia de significación observada no equivale por sí sola a demostrar ausencia de efecto.

## Versión conceptual anterior

También se había formulado de manera más descriptiva:

> La incorporación recurrente de contenido generado por modelos de lenguaje en los datos utilizados para entrenar nuevos modelos provoca una disminución progresiva en la diversidad del contenido generado, acompañada de un aumento en la repetición de patrones y características presentes en los datos sintéticos.

La primera formulación es actualmente preferible para el documento formal.

## Hipótesis nula

> **El entrenamiento recurrente de modelos de lenguaje utilizando contenido sintético no produce cambios estadísticamente significativos en la diversidad ni en la repetición del contenido generado.**

### Clasificación de la hipótesis

La hipótesis principal se clasifica **principalmente como causal**, porque plantea que la incorporación recurrente de datos sintéticos durante el entrenamiento produce cambios en la diversidad y la repetición del contenido generado. Esta clasificación supone que el experimento podrá controlar las condiciones relevantes y comparar resultados entre condiciones de entrenamiento.

El diseño también tendrá un componente **comparativo**, ya que se contrastarán resultados obtenidos con distintas proporciones de datos sintéticos y diferentes números de generaciones. Además, se podrán describir los cambios observados y examinar asociaciones entre variables, pero estos componentes no sustituyen la clasificación principal de la hipótesis.

### Los cinco tipos de hipótesis considerados

- **Descriptiva:** busca describir las características o los cambios observados en una variable. En este proyecto, permitiría describir cómo evolucionan la diversidad y la repetición del contenido generado.
- **Correlacional:** examina la relación entre variables sin afirmar por sí misma que una cause la otra. Aquí permitiría estudiar la asociación entre la proporción de datos sintéticos, el número de generaciones y las métricas de diversidad.
- **Causal:** propone una relación de causa y efecto. Es la clasificación principal de nuestra hipótesis, pues plantea que la reutilización recurrente de datos sintéticos produce cambios en el contenido generado.
- **Comparativa:** contrasta resultados entre grupos o condiciones. En este estudio, se compararían distintas proporciones de datos sintéticos y diferentes números de generaciones.
- **Nula:** plantea que no existe un efecto o diferencia estadísticamente significativa. En este proyecto, establece que el entrenamiento recurrente con datos sintéticos no produce cambios estadísticamente significativos en la diversidad ni en la repetición.

**Precisión metodológica:** aunque la hipótesis principal es causal, la clasificación no demuestra causalidad por sí sola. Para sostener una interpretación causal, será necesario diseñar un experimento controlado y considerar factores que puedan influir en los resultados. La hipótesis nula se evaluará mediante el análisis estadístico que se defina al cerrar la metodología.

### Nota metodológica

No conviene asumir desde el principio que necesariamente ocurrirá un "colapso total". La investigación debe permitir observar:

- si el efecto existe;
- qué tan grande es;
- bajo qué proporción de datos sintéticos aparece;
- cómo cambia con las generaciones;
- qué dimensiones del contenido son afectadas.

---

# 12. Abstract / resumen provisional

> **Resumen provisional:**  
> El crecimiento de contenido generado mediante inteligencia artificial plantea nuevos desafíos para el desarrollo de modelos de lenguaje, especialmente cuando información sintética puede incorporarse posteriormente a nuevos conjuntos de entrenamiento. Esta investigación estudia el fenómeno conocido como *model collapse*, enfocándose en los cambios que pueden producirse en la diversidad y repetición del contenido generado cuando los datos sintéticos son reutilizados de manera recurrente durante sucesivas generaciones de entrenamiento. El estudio busca construir un experimento controlado utilizando modelos de lenguaje pequeños y conjuntos de datos de tamaño limitado, evaluando el efecto de diferentes proporciones de datos sintéticos y diferentes números de generaciones. Se analizarán características como la diversidad léxica y semántica, la frecuencia de patrones repetitivos y los cambios en la distribución del contenido generado. La llamada teoría del ``Internet muerto'' se utilizará únicamente como contexto para motivar el problema, mientras que el objeto de estudio será el comportamiento de los modelos ante la reutilización recurrente de contenido sintético. El objetivo es aportar una aproximación experimental accesible que permita comprender mejor algunas de las condiciones bajo las cuales pueden aparecer efectos asociados con el *model collapse*.

> **Estado:** provisional. Debe revisarse después de cerrar metodología, variables y resultados esperados.

---

# 13. Palabras clave

Palabras clave actualmente propuestas:

- Model collapse
- Datos sintéticos
- Modelos de lenguaje
- Inteligencia artificial generativa
- Entrenamiento recursivo
- Contenido generado por IA
- Diversidad lingüística
- Datos sintéticos recursivos

### Palabras clave útiles para búsqueda bibliográfica

- `model collapse`
- `recursive training`
- `synthetic data`
- `synthetic data contamination`
- `recursive synthetic data`
- `language model collapse`
- `AI-generated text`
- `synthetic data in language models`
- `tail distribution model collapse`
- `model degradation`

---

# 14. Literatura identificada y ampliación del estado del arte

La revisión inicial de dos referencias se amplió a nueve trabajos. El detalle de hallazgos, límites, enlaces y aplicaciones está en [revision_estado_del_arte.md](revision_estado_del_arte.md). La revisión se realizó el **13 de octubre de 2026**; esta actualización del contexto no constituye una nueva búsqueda bibliográfica.

| Referencia | Publicación o versión registrada | Función en el proyecto |
| --- | --- | --- |
| Shumailov et al., *AI models collapse when trained on recursively generated data* | Nature 631, 755–759 (2024). [Artículo](https://www.nature.com/articles/s41586-024-07566-y) | Fundamento del fenómeno y pérdida de información de la distribución original. |
| Guo et al., *The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text* | Findings of NAACL 2024, 3589–3604. [Artículo](https://aclanthology.org/2024.findings-naacl.228/) | Antecedente directo para estudiar diversidad léxica, sintáctica y semántica. |
| Gerstgrasser et al., *Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data* | Preprint arXiv:2404.01413 (2024). [Registro](https://arxiv.org/abs/2404.01413) | Diferencia entre reemplazar los datos y conservarlos mientras se acumulan generaciones sintéticas. |
| Kazdan et al., *Collapse or Thrive: Perils and Promises of Synthetic Data in a Self-Generating World* | ICML 2025, PMLR 267, 29469–29494. [Publicación](https://proceedings.mlr.press/v267/kazdan25a.html) | Distingue acumulación completa y entrenamiento con subconjuntos de tamaño fijo. |
| Zhu et al., *How to Synthesize Text Data without Model Collapse?* | ICML 2025, PMLR 267, 79746–79771. [Publicación](https://proceedings.mlr.press/v267/zhu25d.html); preprint inicial arXiv:2412.14689 (2024). | Proporción sintética, concentración de n-gramas y edición de tokens de texto humano. |
| Drayson, Yilmaz y Lampos, *Machine-generated text detection prevents language model collapse* | EMNLP 2025, 29657–29673. [Artículo](https://aclanthology.org/2025.emnlp-main.1506/) | Decodificación, selección de datos y evaluación en modelos pequeños. |
| Dohmatob et al., *Strong Model Collapse* | ICLR 2025; preprint arXiv:2410.04840 (2024). [Registro](https://arxiv.org/abs/2410.04840) | Distingue deterioro del escalamiento del error de repetición o reducción de diversidad textual. |
| Shabgahi et al., *ForTIFAI: fending off recursive training induced failure for AI model collapse* | npj Artificial Intelligence 2, artículo 70 (4 de julio de 2026). [Artículo](https://www.nature.com/articles/s44387-026-00127-w) | Mitigación mediante objetivos de entrenamiento sensibles a la confianza. |
| Liu y Han, *Break Step: Recursive Training Resonates with Replayed Sampling Noise* | Preprint arXiv:2609.11149v3 (29 de septiembre de 2026). [Versión consultada](https://arxiv.org/abs/2609.11149v3) | Control del muestreo y de semillas compartidas y repetidas. Evidencia provisional. |

### Precisiones bibliográficas

- **Zhu:** actualizar la cita inicial de preprint 2024 a la publicación de ICML 2025 cuando corresponda.
- **Shumailov:** existe una [corrección de 2025](https://www.nature.com/articles/s41586-025-08905-3) en una condición teórica; usar la versión corregida para las ecuaciones. El preprint de 2023 *The Curse of Recursion* es antecedente de este trabajo y no debe contarse como evidencia experimental independiente.
- **Liu y Han:** la primera versión se titulaba *A Fragility Spectrum for Recursive Language-Model Training*. El título y las conclusiones fueron revisados sustancialmente; no tratar la versión anterior y v3 como estudios independientes ni mezclar sus resultados.
- Diferenciar artículos publicados y preprints; conservar la versión efectivamente consultada.

---

# 15. Estado de la revisión bibliográfica

**Avance del 8 de noviembre de 2026:** se redactó la sección Estado del arte en `Manuscrito/main.tex` con nueve subapartados: criterios, evidencia y velocidad, diversidad lingüística, proporción sintética, conservación/acumulación, generación, mitigación, comparación crítica y aportación. Se creó `contexto/06_comparacion_estado_del_arte.md` con una matriz conceptual y registro de verificaciones. Se añadió Gerstgrasser como referencia 15 del artículo. La revisión sigue siendo dirigida; no se han extraído todos los hiperparámetros ni se ha cerrado el diseño.

**Continuación con Scite conectado (3 de noviembre):** tras la conexión confirmada se ejecutaron búsquedas académicas, se comprobó el aviso de corrección de Shumailov y se encontró Suresh et al., publicado en AISTATS 2025. Se contrastó en PMLR antes de incorporarlo como referencia 14 del artículo. Los avisos previos de Scite no conectado describen el momento anterior y ya no son un impedimento vigente. Véase el registro detallado en `contexto/05_fuentes_marco_teorico.md`.

**Ampliación del 3 de noviembre de 2026:** se realizó búsqueda dirigida en fuentes académicas primarias para redactar el marco teórico. El artículo pasó de 2 a 13 referencias citadas; ocho trabajos de fundamentos amplían los nueve previamente identificados. El detalle está en [contexto/05_fuentes_marco_teorico.md](contexto/05_fuentes_marco_teorico.md). Se consultaron registros, resúmenes y apartados pertinentes; no se afirma lectura íntegra de todo el corpus ni revisión sistemática. Se encontró y sugirió Scite, sin conexión confirmada ni uso para obtener resultados. No hubo consulta directa de Google Scholar.

**Realizado:** revisión inicial orientada al proyecto, basada en fuentes primarias, con verificación de metadatos y resúmenes y consulta de apartados metodológicos y de resultados de algunos artículos. Se generó `revision_estado_del_arte.md`.

**Límites:** no es una revisión sistemática, no es exhaustiva y no implica haber leído íntegramente los nueve artículos. Tampoco constituye aún un capítulo formal integrado en el LaTeX.

### Implicaciones para el proyecto

- La pregunta sobre diversidad tiene antecedentes directos, particularmente Guo et al.; los modelos pequeños por sí solos no constituyen una novedad.
- La aportación se perfila como reproducción o comparación accesible bajo condiciones explícitas de modelo, tarea, idioma, presupuesto y protocolo. Estos detalles siguen pendientes.
- Distinguir mezcla, reemplazo y acumulación. Conservar un corpus creciente no equivale a entrenar con muestras de tamaño fijo.
- Separar diversidad de fidelidad y rendimiento; muchos n-gramas únicos no garantizan coherencia ni descartan deterioro.
- Controlar longitudes, prompts, decodificación, presupuesto de tokens y semillas. Documentar la unidad de réplica experimental.
- No se ha decidido que el experimento sea en español ni se ha demostrado novedad por idioma.
- El presupuesto fijo de tokens y las evaluaciones complementarias son recomendaciones de diseño, no configuraciones definitivas.

### Pendientes bibliográficos

1. Leer íntegramente los antecedentes seleccionados para el experimento.
2. Extraer una matriz comparable de modelos, datasets, tareas, ciclos, inicialización, métricas, repeticiones y presupuesto.
3. Consultar los repositorios que se utilicen como base metodológica.
4. Ampliar la búsqueda por idioma si se elige español.
5. Redactar e integrar el capítulo de estado del arte con citas verificadas y comparación crítica, sin limitarse a una lista de resúmenes.

---

# 16. Posibles métricas

Estas son métricas/dimensiones que se han mencionado como posibilidades, no decisiones finales:

## Diversidad léxica

Podrían estudiarse medidas relacionadas con:

- variedad de vocabulario;
- proporción entre tipos y tokens;
- diversidad de términos utilizados.

## Diversidad semántica

Podría estudiarse mediante:

- embeddings;
- similitud semántica;
- dispersión entre respuestas;
- agrupamiento de respuestas.

## Repetición

Podría analizarse:

- repetición de palabras;
- repetición de frases;
- repetición de n-gramas;
- similitud entre respuestas;
- estructuras repetitivas.

## Distribución

Podría analizarse:

- concentración en patrones frecuentes;
- pérdida de ejemplos poco frecuentes;
- cambios en la distribución de características del contenido.

> **Pendiente:** seleccionar métricas concretas basándose en la literatura y en la viabilidad computacional.

Como candidatas se identificaron TTR, Distinct-n, Self-BLEU, distancias entre embeddings y evaluación complementaria de fidelidad o rendimiento. **No están seleccionadas definitivamente.** TTR y Distinct-n requieren controlar la longitud; la diversidad sintáctica está incluida en los fundamentos, pero su medición no es todavía un compromiso experimental.

---

# 17. Capitulado provisional elaborado

Se sustituyó el esquema inicial de seis capítulos por una propuesta granular de **siete capítulos centrales y un octavo opcional de Trabajo futuro**, elaborada para la actividad de creación de capitulado. El usuario solicitó convertirla a LaTeX con carátula y justificar las selecciones. El archivo se creó y su primera versión compiló correctamente; sigue siendo una propuesta, pendiente de evaluación de la asignatura.

**Fuente del entregable:** [Capitulado/main.tex](Capitulado/main.tex). Contiene la jerarquía completa y la justificación de cada capítulo y de su relación con las preguntas de investigación.

**Aclaración posterior sobre lo efectivamente entregado (3 de noviembre de 2026):** el usuario identificó como entregable el texto del adjunto `9022ba73-218d-4ee9-a186-7def108f9e46/Texto pegado.txt`. Esta versión es anterior a las correcciones de feedback conservadas en `Capitulado/main.tex`: no contiene el apartado 7.6, conserva «estructura de ocho capítulos» y alterna algunas expresiones personales. El capítulo 8 sí figura como opcional. Distinguir la versión efectivamente entregada de la revisión local posterior; no atribuir a la entrega las correcciones locales ni suponer aprobación del profesor.

La introducción del entregable tiene diez apartados: 1.1 Contexto del contenido sintético y los modelos de lenguaje; 1.2 Motivación del estudio (Internet muerto como contexto y reutilización de contenido sintético); 1.3 Planteamiento del problema; 1.4 Pregunta principal; 1.5 Preguntas secundarias; 1.6 Objetivos (general y específicos); 1.7 Hipótesis; 1.8 Justificación y aportación esperada; 1.9 Alcances y delimitaciones; 1.10 Organización del documento. Por petición posterior se retiró Organización del documento del artículo y de la revisión local. La introducción actual tiene seis subapartados y formula las preguntas dentro del problema y los objetivos; la transcripción entregada conserva su estructura histórica. La correspondencia temática restante no implica coincidencia exacta de encabezados.

### Criterios de la actividad

- Pensar de manera granular, desde capítulos hasta subapartados.
- Evitar una introducción extensa que repita el marco teórico.
- Detallar instrumentos y procedimientos en la metodología.
- Separar resultados de discusión.
- Redactar conclusiones que respondan las preguntas de investigación.

### Estructura detallada


#### Capítulo 1. Introducción

- **1.1.** Contexto del contenido sintético y los modelos de lenguaje
- **1.2.** Motivación del estudio
  - 1.2.1. La teoría del Internet muerto como contexto
  - 1.2.2. Reutilización de contenido sintético en el entrenamiento
- **1.3.** Planteamiento del problema
- **1.4.** Pregunta principal de investigación
- **1.5.** Preguntas secundarias
- **1.6.** Objetivos de la investigación
  - 1.6.1. Objetivo general
  - 1.6.2. Objetivos específicos
- **1.7.** Hipótesis de investigación
- **1.8.** Justificación y aportación esperada
- **1.9.** Alcances y delimitaciones
> Organización del documento se retiró de la revisión local por solicitud del usuario del 3 de noviembre. Se conserva en la transcripción histórica de contexto/01_capitulado_entregado.md.

#### Capítulo 2. Marco teórico

- **2.1.** Modelos generativos de lenguaje
  - 2.1.1. Generación de texto como proceso probabilístico
  - 2.1.2. Preentrenamiento y ajuste de modelos
  - 2.1.3. Estrategias de muestreo y decodificación
- **2.2.** Datos utilizados en el entrenamiento
  - 2.2.1. Datos de origen humano
  - 2.2.2. Datos sintéticos y semisintéticos
  - 2.2.3. Mezcla, reemplazo y acumulación de datos
- **2.3.** Entrenamiento recursivo
  - 2.3.1. Ciclos de entrenamiento y generación
  - 2.3.2. Transmisión de información entre generaciones
- **2.4.** El fenómeno de *model collapse*
  - 2.4.1. Definición y manifestaciones
  - 2.4.2. Cambios en la distribución del contenido
  - 2.4.3. Pérdida de patrones poco frecuentes
  - 2.4.4. Diferencias entre colapso, repetición y disminución del rendimiento
- **2.5.** Diversidad del contenido generado
  - 2.5.1. Diversidad léxica
  - 2.5.2. Diversidad semántica
  - 2.5.3. Diversidad sintáctica
- **2.6.** Repetición y concentración de patrones
  - 2.6.1. Repetición dentro de un texto
  - 2.6.2. Similitud entre textos generados
- **2.7.** Fundamentos de las métricas de evaluación
  - 2.7.1. Medidas de diversidad léxica
  - 2.7.2. Medidas de diversidad semántica
  - 2.7.3. Medidas de repetición
  - 2.7.4. Medidas de fidelidad distribucional y rendimiento

#### Capítulo 3. Estado del arte

- **3.1.** Criterios de búsqueda y selección de literatura
- **3.2.** Evidencia inicial del colapso por entrenamiento recursivo
- **3.3.** Estudios sobre pérdida de diversidad lingüística
- **3.4.** Efectos de la proporción de datos sintéticos
- **3.5.** Conservación de datos originales y acumulación de generaciones
- **3.6.** Influencia de las estrategias de generación
- **3.7.** Estrategias de mitigación
  - 3.7.1. Selección y filtrado de datos
  - 3.7.2. Generación de datos semisintéticos
  - 3.7.3. Modificación del objetivo de entrenamiento
- **3.8.** Comparación crítica de los trabajos revisados
  - 3.8.1. Modelos, datasets y tareas
  - 3.8.2. Protocolos y presupuestos de entrenamiento
  - 3.8.3. Métricas y limitaciones
- **3.9.** Delimitación de la aportación del presente estudio

#### Capítulo 4. Metodología

- **4.1.** Enfoque y diseño experimental
- **4.2.** Definición operacional de las variables
  - 4.2.1. Proporción de datos sintéticos
  - 4.2.2. Número de generaciones
  - 4.2.3. Diversidad léxica y semántica
  - 4.2.4. Repetición del contenido
  - 4.2.5. Variables de control
- **4.3.** Recursos e instrumentos computacionales
  - 4.3.1. Hardware disponible
  - 4.3.2. Software, bibliotecas y versiones
  - 4.3.3. Herramientas de entrenamiento y evaluación
- **4.4.** Selección del modelo de lenguaje
  - 4.4.1. Criterios de selección
  - 4.4.2. Características y configuración del modelo
- **4.5.** Selección y preparación del conjunto de datos
  - 4.5.1. Procedencia, idioma y características
  - 4.5.2. Limpieza y eliminación de duplicados
  - 4.5.3. División en entrenamiento, validación y prueba
  - 4.5.4. Identificación de patrones frecuentes y poco frecuentes
- **4.6.** Condiciones experimentales
  - 4.6.1. Condición de referencia sin datos sintéticos
  - 4.6.2. Proporciones sintéticas seleccionadas
  - 4.6.3. Número de generaciones y repeticiones independientes
  - 4.6.4. Política de conservación o reemplazo de datos originales
  - 4.6.5. Presupuesto de datos y entrenamiento por condición
- **4.7.** Procedimiento de entrenamiento recursivo
  - 4.7.1. Preparación del modelo inicial
  - 4.7.2. Generación del contenido sintético
  - 4.7.3. Construcción del conjunto de entrenamiento siguiente
  - 4.7.4. Inicialización y ajuste del modelo en cada generación
  - 4.7.5. Evaluación y almacenamiento de resultados
- **4.8.** Configuración de generación del texto
  - 4.8.1. Selección de instrucciones o contextos de entrada
  - 4.8.2. Longitud y cantidad de textos generados
  - 4.8.3. Parámetros de muestreo y decodificación
  - 4.8.4. Gestión de semillas aleatorias
- **4.9.** Métricas e instrumentos de evaluación
  - 4.9.1. Cálculo de diversidad léxica
  - 4.9.2. Cálculo de diversidad semántica
  - 4.9.3. Cálculo de repetición dentro y entre textos
  - 4.9.4. Evaluación de patrones poco frecuentes
  - 4.9.5. Evaluación complementaria de rendimiento o fidelidad
- **4.10.** Procedimiento de análisis estadístico
  - 4.10.1. Unidad de análisis y unidad de réplica experimental
  - 4.10.2. Estadísticos descriptivos e incertidumbre
  - 4.10.3. Comparación entre proporciones y generaciones
  - 4.10.4. Análisis de la interacción entre ambos factores
  - 4.10.5. Criterios de contrastación de la hipótesis
- **4.11.** Controles de reproducibilidad y calidad
  - 4.11.1. Registro de configuraciones y versiones
  - 4.11.2. Prevención de filtración de datos de evaluación
  - 4.11.3. Verificación de duplicados y errores del procedimiento
- **4.12.** Consideraciones éticas y licencias de uso

#### Capítulo 5. Resultados

- **5.1.** Ejecución del experimento y datos obtenidos
- **5.2.** Resultados de la condición de referencia
- **5.3.** Evolución de la diversidad léxica
  - 5.3.1. Diferencias entre generaciones
  - 5.3.2. Diferencias entre proporciones sintéticas
- **5.4.** Evolución de la diversidad semántica
  - 5.4.1. Diferencias entre generaciones
  - 5.4.2. Diferencias entre proporciones sintéticas
- **5.5.** Evolución de la repetición
  - 5.5.1. Repetición dentro de los textos
  - 5.5.2. Similitud entre textos
- **5.6.** Cambios en la representación de patrones poco frecuentes
- **5.7.** Resultados de la evaluación complementaria
- **5.8.** Interacción entre proporción sintética y generaciones
- **5.9.** Variabilidad entre repeticiones experimentales
- **5.10.** Resultados de los contrastes estadísticos

#### Capítulo 6. Discusión

- **6.1.** Interpretación de los cambios en diversidad
- **6.2.** Interpretación de los cambios en repetición
- **6.3.** Efecto conjunto de la proporción sintética y las generaciones
- **6.4.** Relación entre diversidad, fidelidad y rendimiento
- **6.5.** Evidencia compatible con *model collapse*
  - 6.5.1. Indicadores observados
  - 6.5.2. Explicaciones alternativas y alcance de la evidencia
- **6.6.** Comparación con los estudios previos
- **6.7.** Evaluación de la hipótesis de investigación
- **6.8.** Limitaciones y amenazas a la validez
  - 6.8.1. Modelo, dataset e idioma
  - 6.8.2. Presupuesto computacional y número de repeticiones
  - 6.8.3. Limitaciones de las métricas
  - 6.8.4. Alcance de la generalización de los resultados

#### Capítulo 7. Conclusiones

- **7.1.** Respuesta a la pregunta principal
- **7.2.** Respuestas a las preguntas secundarias
- **7.3.** Cumplimiento de los objetivos
- **7.4.** Conclusión sobre la hipótesis, dentro de las condiciones evaluadas
- **7.5.** Aportaciones del estudio
- **7.6.** Limitaciones y líneas de continuación (si no se incluye el capítulo 8)

#### Capítulo 8. Trabajo futuro (opcional)

Por indicación del usuario, su inclusión y extensión quedan sujetas al tiempo disponible antes de la fecha límite. Se trata como apartado complementario en esta propuesta, salvo requisito expreso de la asignatura. Si no se desarrolla como capítulo, sus líneas pueden resumirse al final de las conclusiones. Ejecutar esas investigaciones no es un compromiso de la entrega actual. El usuario ha indicado que existe una fecha límite, pero no ha proporcionado la fecha exacta.

- **8.1.** Evaluación con otros modelos, tareas e idiomas
- **8.2.** Ampliación de generaciones y repeticiones
- **8.3.** Comparación de políticas de conservación de datos
- **8.4.** Evaluación de estrategias de mitigación

### Referencias y anexos

Se incluyen referencias bibliográficas y anexos A–F: configuraciones, instrucciones/contextos, fórmulas de métricas, tablas completas, muestras por condición y generación, y código con guía de reproducción.

### Justificación de la organización

- **Introducción:** delimita problema, preguntas, objetivos e hipótesis sin repetir los fundamentos.
- **Marco teórico:** define conceptos y distingue dimensiones de diversidad, repetición, colapso y rendimiento.
- **Estado del arte:** compara antecedentes y protocolos para orientar la aportación concreta.
- **Metodología:** concentra el mayor detalle para hacer explícitos instrumentos, condiciones, evaluación y reproducibilidad.
- **Resultados:** presenta las observaciones y mediciones sin mezclar su interpretación.
- **Discusión:** interpreta, contrasta literatura, evalúa hipótesis y examina explicaciones alternativas y límites.
- **Conclusiones:** responde preguntas y objetivos de acuerdo con la evidencia obtenida. El apartado 7.6 sintetiza limitaciones y líneas de continuación cuando no se incluye el capítulo 8, sin duplicar su análisis en la discusión.
- **Trabajo futuro:** apartado opcional, sujeto al tiempo disponible y a los requisitos de la asignatura; ubica extensiones fuera del alcance actual sin convertirlas en compromisos. Se priorizan el análisis y las respuestas de la investigación.
- Los apartados de patrones poco frecuentes, diversidad sintáctica y evaluación complementaria deben ajustarse a la viabilidad de su medición.
- La correspondencia entre preguntas secundarias y apartados específicos se justifica en el entregable.

---

# 18. Entregables realizados hasta ahora

## Entregable inicial: elección/acotación del tema

Se trabajó un documento sobre:

**Contenido sintético en Internet y degradación de modelos de lenguaje**

Incluyó:

- idea general;
- interés;
- revisión inicial de literatura;
- problema de investigación;
- viabilidad;
- delimitación;
- factibilidad;
- interés;
- novedad;
- ética;
- relevancia;
- dirección inicial.

## Entregable de preguntas de investigación

Se desarrolló un documento basado en el texto:

**Leonardo Ordóñez Díaz — "Claves para plantear preguntas de investigación"**

El documento propone, entre otras cosas:

- explorar ampliamente el tema;
- identificar el problema;
- formular la pregunta de forma concisa;
- comprobar que sea viable;
- evitar preguntas que se respondan simplemente con sí/no;
- evitar preguntas demasiado totalizantes;
- evaluar pertinencia, viabilidad y potencial de generación de conocimiento.

Las preguntas del proyecto fueron adaptadas siguiendo esos criterios.

---

## Revisión inicial del estado del arte

- Archivo: [revision_estado_del_arte.md](revision_estado_del_arte.md).
- Incluye nueve trabajos, sus límites e implicaciones para el diseño.
- No es todavía un capítulo formal del manuscrito ni una revisión sistemática.

## Actividad: creación de capitulado

- Archivo: [Capitulado/main.tex](Capitulado/main.tex).
- Incluye carátula basada en el Main.tex original, siete capítulos centrales y un octavo opcional con subapartados y justificación por capítulo.
- Incluye correspondencia con las preguntas de investigación y delimitaciones del diseño.
- La versión ajustada a partir del texto enviado por el usuario conserva una explicación más directa del carácter provisional y del interés de Trabajo futuro. Se eliminó la justificación separada de referencias y anexos, manteniendo ambos apartados en el capitulado. Se corrigieron acentuación y concordancia sin cambiar el sentido de sus modificaciones.
- Tras el feedback compartido en dos capturas, se armonizó la presentación como siete capítulos centrales y uno opcional, se añadió el apartado 7.6, se unificó la voz impersonal y se reforzó la descripción de las tareas metodológicas previstas. No se atribuye este feedback al profesor: su autoría no fue confirmada por el usuario.
- **Validación:** compilación exitosa confirmada por el compilador del editor de Codex en esta conversación. No se exportó un PDF independiente.
- Fecha de elaboración del documento: 18 de octubre de 2026.
- No se han redactado resultados ni ejecutado experimentos.

---

# 19. Criterios del documento sobre preguntas de investigación

El material de Ordóñez Díaz establece que la pregunta debe:

1. ser concisa y precisa;
2. ser investigable dentro del tiempo y recursos disponibles;
3. ser pertinente respecto al estado de la cuestión;
4. apuntar a generar conocimiento nuevo;
5. ser interesante y abrir horizontes de trabajo plausibles.

También recomienda, cuando sea posible, formular preguntas abiertas en lugar de preguntas cuya respuesta sea únicamente sí/no.

**Aplicación al proyecto:**

Las preguntas actuales deben conservarse como preguntas abiertas y evitar formularlas como:

- "¿Existe model collapse?"
- "¿Los datos sintéticos causan model collapse?"
- "¿Internet está muerto?"

Es preferible estudiar **cómo cambia una variable observable bajo determinadas condiciones**.

---

# 20. Cosas que NO debemos afirmar sin evidencia

Un agente que trabaje sobre este proyecto debe evitar convertir hipótesis o motivaciones en hechos establecidos.

No afirmar como hecho que:

- Internet ya está dominado por contenido de IA.
- La mayor parte de Internet es contenido sintético.
- Todo entrenamiento con datos sintéticos produce necesariamente *model collapse*.
- *Model collapse* ocurre con cualquier proporción de datos sintéticos.
- Los modelos necesariamente pierden calidad en todos los escenarios.
- Nuestro experimento ya demuestra *model collapse*.
- El proyecto presenta un fenómeno nuevo.

Debe distinguirse entre:

- **lo que dice la literatura;**
- **la hipótesis que estamos planteando;**
- **lo que nuestro experimento podría encontrar.**

---

# 21. Estado actual del proyecto

### Definido en el contexto del proyecto

- Tema, pregunta principal y cinco preguntas secundarias.
- Internet muerto como motivación y model collapse como fenómeno central.
- Foco en texto, modelos compactos y recursos limitados.
- Hipótesis de investigación y nula registradas; refinamiento metodológico pendiente.
- Dimensiones generales: diversidad, repetición y distribución.

### Elaborado en esta conversación

- Notebook anterior `Experimentos/piloto_model_collapse.ipynb` conservado en inglés como antecedente. Nuevo notebook español `Experimentos/piloto_model_collapse_es.ipynb` ejecutado: cinco ajustes y controles completos. Artefactos y verificación local en `Experimentos/resultados/piloto_es_2026-11-09/`; resultados propios de piloto, separados del estudio final.
- Carpeta `contexto/` creada por petición del usuario: índice, transcripción estructural del capitulado entregado, decisiones, criterios editoriales, estado/pendientes y un `AGENTS.md` de mantenimiento. El `AGENTS.md` de la raíz apunta a esos archivos. El contexto maestro permanece en la raíz y ambos se mantienen coherentes.
- Artículo en desarrollo en `Manuscrito/main.tex`: carátula, índice, resumen, introducción de seis subapartados y borrador de marco teórico con siete bloques. Organización del documento fue retirada. Se conserva la hipótesis original y hay 18 referencias citadas y cinco ecuaciones de fundamentos. Estado del arte de nueve subapartados y metodología en español de doce. Compiló el 9 de noviembre al armonizar el protocolo principal. Piloto documentado aparte; resultados finales y secciones posteriores pendientes. No hay PDF independiente nuevo ni inspección visual nueva.
- Notebook principal `Experimentos/experimento_principal_es.ipynb` preparado por aceptación del usuario: 48 ajustes previstos, guardado/reanudación en Drive, 20 controles locales y embebidos pasaron. Banderas desactivadas y primera etapa limitada a un ajuste. No se ejecutó el principal ni se montó Drive.
- Estudio principal completado el 10 de noviembre de 2026 (48/48 etapas). Resultados archivados en `Experimentos/resultados/principal_es_2026-11-10/` (ver `RESUMEN.md`), con análisis complementario post hoc por la regla de textos cortos. `Manuscrito/main.tex` ya incluye Resultados, Discusión y Conclusiones con cifras reales; pendiente revisión del equipo y compilación en su editor.
- Revisión bibliográfica inicial ampliada a nueve trabajos, con límites y enlaces.
- Propuesta granular de siete capítulos centrales y un octavo opcional de Trabajo futuro, separando resultados y discusión. La opcionalidad responde al límite de tiempo indicado por el usuario, sin fecha exacta confirmada.
- LaTeX del capitulado con carátula y justificación; compilación exitosa.
- Contexto maestro actualizado y `AGENTS.md` de mantenimiento del proyecto.
- No hay confirmación de aprobación del capitulado por el profesor.

### Propuesto, sin decisión definitiva

- Objetivo general y cinco objetivos específicos redactados en la introducción a partir de las preguntas vigentes; pendientes de revisión del usuario. La redacción de la introducción es una primera versión y no implica metodología cerrada.
- Reformular la hipótesis para acotarla al protocolo.
- Comparación con presupuesto fijo de tokens y controles de generación.
- Métricas candidatas y evaluación complementaria.
- Configuración v1 implementada con recursos españoles del piloto, 512/128/128 ejemplos, tres proporciones, cinco ciclos, tres repeticiones y reinicio desde la base. Su flujo completo aún debe comprobarse en Colab; no representa resultados finales ni aprobación del profesor.
- Análisis inferencial adicional, si se justifica más allá del resumen descriptivo implementado.

### Próximos pendientes

1. Revisar la propuesta de capitulado según retroalimentación del usuario o profesor.
2. Profundizar en los antecedentes que orientarán el experimento y completar la matriz bibliográfica.
3. Precisar fecha/hora de entrega y comprobar disponibilidad de cómputo. La extrapolación del piloto no incluye persistencia ni asegura una T4 posterior.
4. Comprobar el nuevo guardado/restauración PyTorch y la primera etapa/reanudación en Drive antes de continuar el estudio de 48 ajustes. No iniciarlo automáticamente por esta preparación.
5. Conservar evaluación reservada y protocolo v1 sin ajustes guiados por test; registrar desviaciones antes del análisis.
6. Conservar resultados del piloto separados y salidas/checkpoints necesarios del principal cuando se ejecute.
7. Revisar el análisis descriptivo por cadenas; justificar cualquier inferencia adicional con solo tres repeticiones.
8. Refinar hipótesis y objetivos al cerrar el diseño.
9. Redactar el manuscrito por apartados.
10. Ejecutar el experimento y después redactar resultados, discusión y conclusiones.

---

# 22. Regla conceptual principal para cualquier agente

La investigación puede resumirse en:

> **Estudiar experimentalmente cómo la reutilización recurrente de contenido sintético en el entrenamiento de modelos de lenguaje afecta la diversidad y repetición del contenido generado, considerando la proporción de datos sintéticos y el número de generaciones.**

El concepto de **Internet muerto** explica por qué el problema resulta interesante, pero **no es la variable principal ni el objeto de demostración**.

El concepto central es:

> **Datos sintéticos → reutilización recurrente → cambios en la distribución → diversidad/repetición → posibles efectos asociados con model collapse.**

---

# 23. Tono y estilo esperado del trabajo

**Preferencia expresa del usuario:** conservar la coherencia de enfoque, tono e intensidad entre todos los entregables. La referencia de estilo son los documentos originales de preguntas y el resumen de Main.tex: prosa académica sencilla, explicativa y prudente, con alcance viable. La mayor granularidad del capitulado responde a la actividad y no amplía por sí sola las obligaciones del experimento.

Las decisiones abiertas deben describirse como propuestas. Evitar que un cambio de documento convierta una posibilidad en un compromiso o que las aclaraciones sobre tiempo adopten un tono excesivamente normativo. En la revisión de coherencia se simplificó la justificación de Trabajo futuro y se ajustaron expresiones metodológicas para conservar ese carácter provisional.

Mantener voz impersonal uniforme en el entregable. Distinguir entre decisiones pendientes y tareas previstas: «se justificará la selección» es adecuado para la obligación de explicar el procedimiento, aunque el modelo siga pendiente de elección. Este criterio sustituye las alternancias anteriores de primera persona y la expresión más débil «se buscará justificar». El conteo debe expresarse como siete capítulos centrales y uno complementario opcional, coherente con la alternativa del apartado 7.6.

El proyecto debe escribirse como una investigación académica de computación/matemáticas aplicadas:

- claro;
- formal;
- preciso;
- sin exagerar las conclusiones;
- evitando lenguaje sensacionalista alrededor de "Internet muerto";
- distinguiendo hipótesis de resultados;
- priorizando variables observables y medibles;
- manteniendo un alcance viable para un proyecto académico.

La investigación debe ser **factible, interesante, novedosa en su implementación, ética y relevante**, pero no debe pretender presentar como novedoso el fenómeno de *model collapse* en sí.

---

# 24. Resumen de una sola frase para dar contexto rápido a un agente

> Estamos desarrollando una investigación académica sobre *model collapse* que estudia, mediante un experimento controlado con modelos de lenguaje pequeños, cómo la reutilización recurrente de datos sintéticos afecta la diversidad y repetición del contenido generado; la teoría del "Internet muerto" funciona únicamente como contexto y motivación.

---

# 25. Inventario de archivos y fuente de verdad

| Archivo | Función y estado |
| --- | --- |
| `model_collapse_proyecto_contexto.md` | Contexto maestro vivo, en la raíz del proyecto. Leer primero y mantener actualizado. |
| `AGENTS.md` | Instrucciones para trabajar en este proyecto y mantener el contexto. |
| `contexto/README.md` | Índice de referencias temáticas y relación con el contexto maestro. |
| `contexto/AGENTS.md` | Instrucciones de mantenimiento de la carpeta de referencias. |
| `contexto/01_capitulado_entregado.md` | Estructura íntegra transcrita de la versión identificada como entregada, con diferencias respecto de la revisión local. |
| `contexto/02_decisiones.md` | Acuerdos y delimitaciones, separación de documentos y propuestas pendientes. |
| `contexto/03_criterios_editoriales.md` | Tono, coherencia, rigor y comprobaciones de documentos. |
| `contexto/04_estado_y_pendientes.md` | Avances comprobados y pendientes de coordinación, redacción, metodología y bibliografía. |
| `contexto/05_fuentes_marco_teorico.md` | Ampliación de búsqueda académica, 13 referencias citadas, herramientas y límites de consulta del 3 de noviembre. |
| `contexto/06_comparacion_estado_del_arte.md` | Matriz conceptual, fuentes y verificaciones de la primera redacción del estado del arte del 8 de noviembre. |
| `contexto/07_propuesta_metodologia.md` | Propuesta operativa con piloto, alcance mínimo, recursos observados y plan de cuatro días. |
| `Experimentos/piloto_model_collapse.ipynb` | Notebook anterior en inglés, conservado como antecedente; ejecución interrumpida durante imports, sin entrenamiento. Sustituido por el nuevo archivo español. |
| `Experimentos/piloto_model_collapse_es.ipynb` y `Experimentos/README_ES.md` | Fuente autónoma del piloto español ejecutado e instrucciones; copia con salidas archivada aparte. |
| `Experimentos/piloto_colab_es.py`, `controles_es.py`, `test_controles_es.py` y `crear_notebook_es.py` | Fuentes españolas: selección por artículo, Unicode, pruebas y generador sin sobrescribir el notebook anterior. |
| `Experimentos/bitacora_piloto_es_2026-11-09.md` | Entorno, incidentes y observaciones del piloto completado. |
| `Experimentos/resultados/piloto_es_2026-11-09/` | ZIP original, notebook ejecutado, datos extraídos, resumen, captura de Colab y verificación local. Sin checkpoints por configuración explícita. |
| `Experimentos/verificar_resultados_es.py` | Verificación reproducible de metadatos, particiones, presupuestos, semillas y métricas léxicas del piloto archivado, sin red ni nuevo entrenamiento. |
| `Experimentos/experimento_principal_es.ipynb` y `Experimentos/README_PRINCIPAL_ES.md` | Notebook principal autónomo de 29 celdas e instrucciones: 48 ajustes previstos, ejecución desactivada, persistencia/reanudación preparadas, flujo completo sin ejecutar. |
| `Experimentos/principal_colab_es.py`, `estado_principal_es.py`, `test_estado_principal_es.py` y `crear_principal_es.py` | Fuentes del principal, persistencia por hashes, siete controles nuevos y generador; 20 controles totales locales y embebidos pasaron. |
| `Experimentos/generar_resultados_latex.py` | Convierte `results.csv` en tablas y figura LaTeX (`Manuscrito/resultados_generados/`), con `--nota` para leyendas, y verifica integridad. Ejecutado con los resultados reales el 10 de noviembre. |
| `Experimentos/analisis_complementario_es.py` | Análisis complementario post hoc de métricas léxicas sobre los 90 contextos comunes; la parte semántica se calculó en Colab. |
| `Experimentos/resultados/principal_es_2026-11-10/` | ZIP original, contenido extraído, análisis complementario, verificación preregistrada y `RESUMEN.md` del estudio principal. |
| `Manuscrito/resultados_generados/` | Tablas `.tex` y figura usadas por `main.tex` (perplejidad desde `preregistrado/`). |
| `Manuscrito/main_respaldo_antes_resultados_2026-11-10.tex` | Respaldo de `main.tex` antes de incorporar resultados. |
| `Manuscrito/borrador_resultados_discusion.tex` | Esqueleto anterior sin cifras; obsoleto, sustituido por las secciones de `main.tex`. |
| `Experimentos/PLAN_PRINCIPAL_ES.md` | Alcance aceptado de preparación, diseño y estado de verificación; no autoriza iniciar automáticamente el principal. |
| `Experimentos/README.md` y `Experimentos/VERIFICACION.md` | Instrucciones, archivos de salida, límites y verificaciones realmente realizadas. |
| `Experimentos/piloto_colab.py`, `controles.py`, `test_controles.py`, `crear_notebook.py` y `PLAN.md` | Fuentes del notebook, controles de protocolo, generador y alcance de implementación. |
| `revision_estado_del_arte.md` | Revisión inicial y crítica de la literatura; documento de apoyo, no capítulo final. |
| `Capitulado/main.tex` | Entregable de capitulado y justificación. Es un proyecto LaTeX independiente; compilación verificada. |
| `Manuscrito/main.tex` | Artículo con introducción sin Organización del documento, marco teórico, estado del arte, metodología armonizada en español y 18 referencias citadas. Piloto documentado aparte; resultados finales y secciones posteriores pendientes. Compilación verificada el 9 de noviembre de 2026. |
| `C:\Users\PC\Downloads\model_collapse_proyecto_contexto.md` | Archivo de contexto originalmente proporcionado. Se sincronizó al establecer el maestro; los cambios posteriores se mantienen en el proyecto salvo solicitud de sincronización. |
| `C:\Users\PC\Downloads\Esqueleto.tex` | Entregable inicial de elección del tema. Contiene preguntas anteriores y una frase suelta; no es la fuente de preguntas actuales. |
| `C:\Users\PC\Downloads\Preguntas_de_investigación.tex` | Entregable de pregunta principal y cinco secundarias. |
| `C:\Users\PC\Downloads\Main.tex` | Manuscrito original con carátula, resumen e hipótesis; cuerpo principal pendiente. No se integró aquí el capitulado. |

No confundir `Capitulado/main.tex`, el `Main.tex` histórico de Descargas y el documento integrado `Manuscrito/main.tex`. Este último usa como base el texto adjunto enviado el 3 de noviembre de 2026 (adjunto `753a2aee-50c9-4763-85e3-8a54a14abf5c/Texto pegado.txt`). Se conservó la fecha de entrega de esa fuente, 28 de septiembre de 2026; no confirma la fecha límite vigente. Los originales no fueron sobrescritos. No declarar aprobados por el usuario o el profesor los detalles que solo se han propuesto. Si existen copias divergentes, comparar su contenido y la conversación antes de actualizar; no elegir únicamente por el nombre o la fecha de modificación.

# 26. Mantenimiento y registro de avances

- **10 de noviembre de 2026 (ajustes de entrega y publicación):** el usuario solicitó aplicar la revisión, actualizar el ZIP de Overleaf y subir los cambios a GitHub. Se corrigieron formulaciones demasiado absolutas sobre el control, se reconoció el cumplimiento parcial del objetivo de repetición entre respuestas, se recordó el alcance post hoc de 90 contextos en conclusiones y se matizó la dirección desconocida del sesgo de selección. Se actualizó el estado del arte para describir la evaluación realizada. Compilación exitosa de la fuente original y copia Overleaf en el editor; sin exportación nueva ni revisión de todas las páginas. Se actualizaron el paquete Overleaf (ocho entradas verificadas por hashes) y los documentos de continuidad. `git push origin main` confirmó publicación del commit `3056349` en `CarLos4475/IMAC`; no se forzó el historial.

- **10 de noviembre de 2026 (revisión para entrega):** a petición del usuario se revisaron artículo, tablas, figura y artefactos locales. La fuente original compiló con éxito en el editor; 48 marcadores y 240 hashes de archivos de etapas concordaron. Se confirmaron los faltantes originales (39 etapas, 75 salidas cortas) y el alcance post hoc del subconjunto de 90 contextos. Se identificaron ajustes recomendados de prudencia en conclusiones y cumplimiento de objetivos, sin editar el manuscrito ni ejecutar entrenamientos. No se inspeccionó el PDF completo ni se exportó otro PDF. Se actualizó `contexto/04_estado_y_pendientes.md`.

Al finalizar una tarea sustantiva, actualizar las secciones afectadas de este documento, la fecha superior y este registro breve. Mantener un estado actual coherente; no limitarse a añadir notas que contradigan secciones anteriores. Distinguir decisiones del usuario, propuestas, evidencia bibliográfica y resultados propios. Registrar archivos y verificaciones reales, sin inventar resultados o aprobaciones.

## Registro

- **10 de noviembre de 2026 (legibilidad y entrega solo en PDF):** el usuario indicó que solo se entrega el PDF; se quitaron el anexo C, las rutas a archivos y la promesa de conservar código/datos en Aportaciones. Se añadió a la metodología un resumen del procedimiento por pasos (contexto, continuación objetivo, ciclo), se simplificó la jerga de ajuste y reproducibilidad y se actualizó el marco teórico para quitar lenguaje de planeación y conectar cada concepto con la elección del estudio. Respaldo: `Manuscrito/main_respaldo_antes_legibilidad_2026-11-10.tex`. Compilación de prueba (babel inglés): 35 páginas, sin errores ni cajas desbordadas.
- **10 de noviembre de 2026 (ajuste al capitulado y Overleaf):** a petición del usuario, fecha de portada 11 de noviembre de 2026 (entrega al día siguiente) y `es-tabla` en babel. Para cuadrar con el capitulado entregado se añadieron a `Manuscrito/main.tex`: apartado de preguntas de investigación (principal y cinco secundarias, tomadas de `Preguntas_de_investigación.tex`), resultados de interacción proporción×ciclos, variabilidad entre repeticiones y aspectos previstos no evaluados, conclusiones por pregunta, objetivos, hipótesis, aportaciones y limitaciones/trabajo futuro, y anexos A–C (configuración, tablas completas, muestras y reproducción). Respaldo en `Manuscrito/main_respaldo_antes_capitulado_2026-11-10.tex`. Carpeta `Overleaf_IMAC/` y `Overleaf_IMAC.zip` listas para subir; el usuario compiló una versión anterior en Overleaf sin problemas. Se crearon `README.md` y `.gitignore`; subida a GitHub (`CarLos4475/IMAC`) pendiente de acceso. Compilación local de comprobación solo con babel inglés. Sin anexo de patrones raros; sin pruebas de significación.
- **10 de noviembre de 2026 (estudio principal completado y artículo con resultados):** la corrida terminó a las 07:33 UTC con 48/48 etapas (una reanudación; ~2.8 h de cómputo registrado). Con autorización previa del usuario (dormido, pidió trabajo autónomo) se ejecutó la celda de resumen, se descargó el ZIP y se archivó en `Experimentos/resultados/principal_es_2026-11-10/` con `RESUMEN.md`. Incidencia: la regla preregistrada de textos cortos (<30 palabras) dejó sin métricas léxicas/semánticas 39 de 48 etapas (75 de 6144 continuaciones cortas). Se hizo un análisis complementario post hoc, declarado como desviación, sobre 90 contextos comunes: `Experimentos/analisis_complementario_es.py` (léxicas) y una celda temporal añadida al final de la copia de Colab del usuario (semántica, misma revisión del codificador). Resultados: con α=1 la perplejidad sobre texto humano sube de 30.46 a 39.30 (~+29 %), Distinct-2 baja de 0.913 a 0.825 y la repetición de 4-gramas sube de 0.003 a 0.035; con α=0.5 la perplejidad sube ~4.7 % y se estabiliza; α=0 estable; la dispersión semántica no baja. Se actualizó `Manuscrito/main.tex`: resumen nuevo, introducción (alcances, hipótesis), metodología en pasado y sin “pendiente”, `graphicx`, y secciones Resultados, Discusión (con limitaciones) y Conclusiones con trabajo futuro; respaldo previo en `Manuscrito/main_respaldo_antes_resultados_2026-11-10.tex`. Tablas y figura generadas en `Manuscrito/resultados_generados/`. Se verificaron con Scite las referencias académicas (14 verificadas; Bengio 2003 sin DOI en JMLR; la corrección de Shumailov 2025 es una errata de notación). Compilación comprobada solo en una copia con babel inglés y mathptmx (la VM no tiene babel español ni newtx): sin errores ni cajas desbordadas; falta compilar el original en el editor del usuario. `Manuscrito/borrador_resultados_discusion.tex` quedó obsoleto. Archivos temporales de revisión movidos a `_to_delete/` (no se pudieron borrar). Los textos redactados requieren revisión del equipo para ajustar a su voz.
- **10 de noviembre de 2026 (corrida principal en curso y preparación de resultados):** el usuario ejecutó en Colab (T4, Drive `IMAC/estudio_principal_es_v1`) el notebook principal con `RUN_EXPERIMENT = True`; la corrida comenzó la noche del 9 de noviembre (~22:42, hora de CDMX) y se supervisó con revisiones periódicas. Hasta la última lectura (~35 de 48 etapas confirmadas, ~2.85 min por etapa) no había errores; al momento de este registro **no estaba completada**, por lo que no existen resultados finales ni cifras en el artículo. Se crearon `Experimentos/generar_resultados_latex.py` (verifica integridad de `results.csv`, genera tablas `.tex` y figura de trayectorias) y `Manuscrito/borrador_resultados_discusion.tex` (esqueleto comentado, sin cifras, no incluido en `main.tex`). El script se probó solo con datos sintéticos que no se guardaron como resultados; `Manuscrito/main.tex` no se modificó ni se recompiló, y la máquina virtual local carece de babel en español, así que la compilación debe hacerse en el editor del usuario. Pendiente: descargar el ZIP, archivarlo en `Experimentos/resultados/`, generar tablas, redactar Resultados/Discusión/Conclusiones con cifras reales y actualizar pasajes que aún dicen "pendiente".
- **9 de noviembre de 2026 (principal preparado):** el usuario aceptó preparar un notebook reanudable y armonizar la metodología en español. Se crearon `experimento_principal_es.ipynb`, sus fuentes, siete pruebas adicionales, plan e instrucciones, conservando el piloto ejecutado. Configuración v1: 512/128/128 ejemplos, 0/50/100 %, cinco ciclos y tres repeticiones; 48 ajustes previstos. Persistencia preparada con hashes, lotes y checkpoints Safetensors; banderas desactivadas y primera etapa limitada a un ajuste. Pasaron 20 controles locales y embebidos, sintaxis y autonomía. Se armonizaron metodología y delimitación del artículo; 18 referencias citadas y compilación exitosa. Sin montaje de Drive, ejecución principal, nueva prueba PyTorch de checkpoint, PDF exportado ni inspección visual. Contexto, notas temáticas e instrucciones actualizados.
- **9 de noviembre de 2026 (piloto completado):** el usuario confirmó importación y autorizó trabajar en Chrome. Tras cerrar él las sesiones anteriores, se ejecutó en T4 el piloto español de cinco ajustes. Pasaron 13 controles y las pruebas PyTorch. Se descargaron ZIP y notebook ejecutado; se archivaron datos, captura y bitácora y se verificaron localmente particiones, semillas, presupuestos y métricas léxicas. Duración del manifiesto 212.20 s, sin instalación/controles previos. PPL inicial 29.4677, control final 29.4150 y sintético final 31.9012; sin caída sostenida de diversidad y sin inferencia estadística por una cadena/dos ciclos. Se registró una estimación de presupuesto, no se inició el estudio completo. Artículo sin cambios; contexto e instrucciones actualizados.
- **9 de noviembre de 2026 (notebook español nuevo):** el usuario pidió un archivo nuevo y dijo que lo importará y avisará. Se creó `Experimentos/piloto_model_collapse_es.ipynb` con recursos y controles de español, instalación/imports y salida ZIP; se conservó el anterior. Se verificaron fuentes primarias, se descartó el recurso BNE deprecado sin pesos visibles y se documentaron particiones propias, Unicode y límites de procedencia/solapamiento. Pasaron 13 pruebas offline y embebidas, validación de JSON/autonomía y sintaxis. No se ejecutaron PyTorch ni Colab en esta tarea; sin entrenamiento, resultados o tiempos. Artículo sin cambios y bibliografía inicial sin nueva fecha de consulta. Contexto e instrucciones actualizados.
- **9 de noviembre de 2026 (conexión e idioma):** la extensión instalada por el usuario permitió leer el notebook de Colab y conectar T4. Se inició la ejecución autorizada; completó instalación y fue interrumpida durante imports cuando el usuario recordó que las mediciones debían hacerse en español. Se verificó interrupción y ausencia de ejecución activa; sin entrenamiento ni resultados. El español queda como requisito confirmado y sustituye la propuesta del agente en inglés. Notebook y artículo aún requieren adaptación; se actualizaron decisiones, estado, metodología propuesta, verificación e instrucciones. No se modificó LaTeX ni se volvió a consultar bibliografía.
- **8 de noviembre de 2026 (notebook piloto):** tras bloqueos del control de navegador por verificación de URL, el usuario aceptó un archivo local completo con imports. Se creó `Experimentos/` con notebook autónomo de 22 celdas, fuentes, instalación, cinco ajustes propuestos, métricas, gráficas y guardado/descarga. Siete controles offline pasaron y las fuentes/celdas superaron revisión de sintaxis. Se consultaron APIs y fichas oficiales para la implementación, sin cambiar las referencias del artículo ni la fecha de consulta de la revisión inicial. PyTorch y Colab no se ejecutaron: sin descargas, entrenamiento, resultados ni tiempos. Se documentaron concreciones propuestas de EOS, embeddings, longitudes y optimizador. Artículo sin cambios; no correspondía recompilar LaTeX. Contexto e instrucciones actualizados.
- **8 de noviembre de 2026 (propuesta metodológica):** el usuario indicó plazo aproximado de cuatro días y cómputo local o Colab. Se redactaron doce subapartados de metodología con configuración propuesta, control de mezcla, reinicialización, evaluación por cadenas y piloto de viabilidad. Se añadieron fichas oficiales de OPT-125m y WikiText; hay 17 referencias citadas. Se registró CPU Ryzen 5 5600G mediante lectura del registro; CIM no permitió verificar RAM/GPU, por lo que no se asegura su capacidad. No se descargaron recursos ni se entrenaron modelos. Compilación exitosa; contexto y referencias actualizados.
- **8 de noviembre de 2026:** al retomar la investigación se redactó Estado del arte en el artículo, con nueve subapartados y comparación de siete antecedentes. Se contrastaron fuentes primarias y registros de Scite, manteniendo autoría y páginas de ACL ante discrepancias del índice. Se añadió `gerstgrasser2024`; hay 15 referencias citadas. Se creó una matriz conceptual en `contexto/06_comparacion_estado_del_arte.md` y se actualizaron estado e instrucciones. Compilación exitosa; sin PDF exportado ni inspección visual. La metodología permanece abierta y las guías independientes no se modificaron.
- **3 de noviembre de 2026 (Scite conectado):** se continuó la búsqueda con la integración confirmada. Se consultaron registros y fragmentos, se conservaron metadatos de ACL ante una omisión en el registro de Guo y se verificó la publicación de Suresh en AISTATS 2025 con PMLR. Se añadió al artículo una distinción entre posibilidad y rapidez de colapso en escenarios simplificados; 14 referencias citadas. Compilación exitosa. Candidatos adicionales quedaron documentados para revisión, sin incorporarlos automáticamente ni modificar la metodología.
- **3 de noviembre de 2026 (marco teórico y fuentes):** se eliminó Organización del documento del artículo y del capitulado revisado; se conservó la transcripción histórica. Se redactó el marco teórico con siete bloques y subapartados y se amplió la bibliografía del artículo de 2 a 13 referencias. Se buscaron herramientas académicas y se sugirió Scite, sin conexión confirmada; las fuentes se consultaron con búsqueda web en repositorios y actas primarias. Se creó `contexto/05_fuentes_marco_teorico.md` y se actualizaron decisiones, estado e instrucciones. Ambos documentos compilaron correctamente; sin inspección visual ni exportación de PDF. La metodología sigue abierta.
- **3 de noviembre de 2026 (referencias organizadas):** a petición del usuario se creó `contexto/` con seis archivos Markdown. Se transcribió el capitulado íntegro desde el adjunto confirmado como entregado, diferenciándolo de la revisión local, y se organizaron decisiones, criterios y pendientes. Se enlazó desde `AGENTS.md` de la raíz y desde este contexto. No se modificó el artículo ni se cambió el diseño experimental.
- **3 de noviembre de 2026 (versión entregada):** el usuario identificó el adjunto `9022ba73-218d-4ee9-a186-7def108f9e46/Texto pegado.txt` como el capitulado efectivamente entregado. Se comparó con el archivo local y se registraron las diferencias de versión y la estructura exacta de la introducción. No se modificó `Manuscrito/main.tex` ni se sustituyó la revisión local del capitulado; no correspondía compilar al no editar LaTeX.
- **3 de noviembre de 2026 (introducción):** se redactó la introducción en el Main abierto, alineada temáticamente con el capitulado y adaptada al formato de artículo. Contexto/motivación y preguntas se integran en el planteamiento; se propusieron un objetivo general y cinco específicos. Se conservó la hipótesis y se explicitaron sus límites; se añadieron justificación, delimitación y organización. Se verificaron en fuentes primarias las dos citas incorporadas, sin ampliar ni cambiar la fecha de la revisión bibliográfica inicial. Compilación exitosa del archivo guardado. No se exportó PDF ni se inspeccionó visualmente; el resto del artículo sigue pendiente.
- **3 de noviembre de 2026 (aclaración del usuario):** el Main debe ser el artículo, no una colección de entregables. Se retiraron preguntas y propuesta/justificación del capitulado del manuscrito, se limpió su preámbulo y se ubicó la hipótesis original en la introducción. El resto de la estructura quedó en comentarios, sin inventar contenido. `Capitulado/main.tex` se conserva como entregable independiente. Compilación de la versión corregida exitosa; contexto e instrucciones actualizados.
- **3 de noviembre de 2026:** a petición de unificar en el Main, se creó `Manuscrito/main.tex` con el texto base adjunto, las preguntas principal/secundarias y el capitulado corregido con justificación. Se eliminaron duplicados de preámbulo, carátula y pregunta principal en la presentación del capitulado; se conservó la hipótesis y la fecha de entrega de la fuente. Se verificó un único entorno de documento y compilación exitosa mediante el editor. Se actualizaron este contexto y `AGENTS.md`; no se exportó PDF ni se hizo una nueva revisión bibliográfica.
- **18 de octubre de 2026 (feedback posterior):** se revisaron los cuatro puntos legibles en las capturas compartidas por el usuario y se corrigió `Capitulado/main.tex`: conteo de siete capítulos centrales y uno opcional, apartado 7.6 como alternativa al capítulo 8, voz impersonal y formulación «se justificará» para tareas previstas. Se actualizaron los criterios de `AGENTS.md` y este contexto. Compilación exitosa de la versión guardada, tras reintentar un aviso de proyecto desactualizado; no se exportó un PDF independiente.
- **13 de octubre de 2026:** revisión inicial del estado del arte; se creó `revision_estado_del_arte.md` con nueve trabajos y sus implicaciones metodológicas. Fecha de consulta registrada en dicho archivo.
- **18 de octubre de 2026:** se elaboró el capitulado granular de ocho capítulos y su justificación en `Capitulado/main.tex`, con carátula basada en los documentos proporcionados. Compilación confirmada por el editor.
- **18 de octubre de 2026:** a solicitud del usuario, se actualizó el contexto original, se estableció una copia maestra dentro de IMAC y se creó `AGENTS.md` para indicar lectura y mantenimiento del contexto.
- **18 de octubre de 2026:** se marcó Trabajo futuro como capítulo opcional, condicionado al tiempo disponible y a los requisitos de la asignatura, tanto en el capitulado como en su justificación. Puede resumirse en las conclusiones; las extensiones no comprometen la entrega actual. La versión modificada compiló correctamente con el compilador del editor. Se actualizaron este contexto y `AGENTS.md`; no se sincronizó de nuevo la copia de Descargas.
- **18 de octubre de 2026:** el usuario indicó conservar coherencia de enfoque, tono e intensidad entre documentos. Se comparó el capitulado con los originales, se simplificó la justificación del capítulo opcional y se ajustaron expresiones de metodología para no presentar decisiones abiertas como cerradas. Se registró el criterio editorial en este contexto y en `AGENTS.md`.
- **18 de octubre de 2026:** se incorporaron los cambios del texto LaTeX adjunto por el usuario en `Capitulado/main.tex`: explicación más directa de decisiones pendientes, aclaración breve de Trabajo futuro según el tiempo disponible y eliminación de la justificación separada de referencias y anexos. Se ajustaron únicamente redacción, acentos y concordancia; se conserva la estructura temática. La versión actual compiló correctamente en el editor tras repetir una compilación inicialmente marcada como desactualizada.

