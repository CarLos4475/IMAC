# Notebook del piloto

**Revisión del 9 de noviembre:** el usuario solicitó un nuevo notebook en español y lo importará por su cuenta. Se conserva la versión anterior. Se añaden fuentes `_es`, selección de artículos de Wikipedia por hash y codificador multilingüe; se mantienen los cinco ajustes del piloto. Verificaciones locales y contexto se actualizan sin ejecutar Colab ni cambiar el artículo.

Fecha: 8 de noviembre de 2026. Alcance autorizado: entregar un notebook local completo para Colab, con instalación, imports y ejecución del piloto descrito en `contexto/07_propuesta_metodologia.md`. No ejecutar el estudio completo ni modificar el artículo en esta tarea.

Se construirá un `.ipynb` autónomo, acompañado por el código fuente y controles reproducibles. El usuario podrá subir solo el notebook. Se descarta depender de archivos externos o de montar Drive para iniciar. El diseño experimental sigue siendo propuesto, pendiente de tiempos y resultados del piloto.

1. Probar controles independientes del hardware: separación de artículos y particiones, ventanas no solapadas, etiquetas, mezcla exacta, semillas y métricas de longitud común.
2. Implementar carga con revisiones registradas, ajuste desde pesos base y optimizador nuevo, muestreo reproducible, evaluación y guardado incremental.
3. Incorporar comprobaciones con un OPT diminuto inicializado localmente en Colab, antes de descargar OPT-125m. Incluir instalación e imports completos y diagnóstico de GPU.
4. Generar el notebook autocontenido desde el código, validar JSON/sintaxis/controles locales y documentar qué requiere ejecución real en Colab.
5. Actualizar contexto maestro y notas temáticas, conservando el estado de ausencia de entrenamiento propio.

Casos relevantes: encabezados de subsección que no deben dividir artículos; objetivos sintéticos de longitud incorrecta; textos demasiado cortos para la métrica léxica; interrupciones del runtime; entorno sin GPU o versiones incompatibles. Cada uno debe producir un control o una explicación concreta, sin cambiar automáticamente el protocolo.
