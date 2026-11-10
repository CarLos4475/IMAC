# Capitulado efectivamente entregado

Registrado: 3 de noviembre de 2026. Fecha de elaboración indicada en la carátula: 18 de octubre de 2026.

## Procedencia y estado

El usuario identificó el adjunto `9022ba73-218d-4ee9-a186-7def108f9e46/Texto pegado.txt` como el entregable. La estructura siguiente se transcribe de ese archivo, sin incorporar las correcciones posteriores de la versión local.

**Entregado no equivale a aprobado:** no se ha proporcionado confirmación de aprobación del profesor. Los títulos tampoco confirman que la metodología esté cerrada.

## Estructura entregada

### 1. Introducción

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
- **1.10.** Organización del documento

### 2. Marco teórico

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

### 3. Estado del arte

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

### 4. Metodología

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

### 5. Resultados

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

### 6. Discusión

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

### 7. Conclusiones

- **7.1.** Respuesta a la pregunta principal
- **7.2.** Respuestas a las preguntas secundarias
- **7.3.** Cumplimiento de los objetivos
- **7.4.** Conclusión sobre la hipótesis, dentro de las condiciones evaluadas
- **7.5.** Aportaciones del estudio

### 8. Trabajo futuro (opcional)

- **8.1.** Evaluación con otros modelos, tareas e idiomas
- **8.2.** Ampliación de generaciones y repeticiones
- **8.3.** Comparación de políticas de conservación de datos
- **8.4.** Evaluación de estrategias de mitigación

## Referencias y anexos

Referencias bibliográficas: fuentes citadas con datos verificados y formato uniforme.

Anexos:

- A. Configuraciones completas del experimento.
- B. Instrucciones y contextos utilizados para generar texto.
- C. Definiciones y fórmulas de las métricas seleccionadas.
- D. Tablas completas de resultados.
- E. Muestras de contenido por condición y generación.
- F. Código y guía de reproducción.

## Distinción de versiones

**Cambio solicitado el 3 de noviembre de 2026:** se eliminó Organización del documento del artículo y de `Capitulado/main.tex`. El apartado 1.10 se conserva en esta transcripción porque formaba parte del documento entregado; ya no forma parte de la estructura revisada vigente.

| Aspecto | Entregable identificado por el usuario | Revisión local posterior |
| --- | --- | --- |
| Presentación | Dice «estructura de ocho capítulos». | Expresa siete centrales y uno complementario opcional. |
| Trabajo futuro | Capítulo 8 expresamente opcional y condicionado al tiempo. | Mantiene la opcionalidad y aclara su relación con las conclusiones. |
| Conclusiones | Apartados 7.1–7.5. | Añade 7.6 como síntesis de limitaciones y continuación si no se incluye el capítulo 8. |
| Voz | Conserva algunas expresiones personales y erratas. | Unifica voz impersonal y corrige redacción. |

La revisión local está en [Capitulado/main.tex](../Capitulado/main.tex). No presentarla como transcripción de lo entregado.

## Relación con la introducción actual del artículo

La introducción de [Manuscrito/main.tex](../Manuscrito/main.tex) agrupa los temas en seis subapartados: contexto y motivación; planteamiento del problema; objetivos; hipótesis; justificación y aportación; alcances. El anterior apartado de organización fue retirado por solicitud del usuario.

Existe correspondencia temática con los diez apartados del capítulo 1 entregado, pero no coincidencia exacta de títulos ni numeración. Las preguntas orientan el problema y los objetivos; no se copió la actividad de preguntas. La adecuación exacta de encabezados sigue pendiente de una decisión del usuario.

## Criterio temporal

Se prioriza terminar el análisis y responder el problema de investigación. Las continuaciones pueden resumirse en las conclusiones si no hay tiempo para el capítulo opcional; ejecutar esas investigaciones queda fuera de la entrega actual. La fecha límite exacta no ha sido confirmada.

