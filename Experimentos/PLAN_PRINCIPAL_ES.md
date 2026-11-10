# Preparación del experimento principal

9 de noviembre de 2026. Alcance aceptado por el usuario: crear notebook principal reanudable y armonizar metodología en español. **No ejecutar los 48 ajustes en esta tarea.**

Configuración: 512 contextos/objetivos de 64/128 tokens; 128 referencias de validación y 128 de prueba; tres proporciones 0/.5/1, cinco ciclos y tres repeticiones. Tres M0 compartidos dentro de repetición y 45 ajustes posteriores. Recursos/revisiones del piloto español. La regla de partición conserva la semilla 20261109 para no mover artículos usados en el piloto a prueba. La validación fija la longitud; el test no interviene en entrenamiento ni selección de parámetros.

Pasos:

1. Probar particiones finales, calendario de 48 ajustes, huellas de configuración, detección de corrupción y marcadores de etapa completos.
2. Implementar guardado persistente con hashes, muestras por lotes y reanudación entre ajustes. Un ajuste incompleto vuelve al mismo modelo base y semilla; no se afirma reanudación dentro del optimizador. Conservar M0 y último checkpoint necesario; los anteriores se purgan solo después de confirmar su sucesor completo.
3. Construir el notebook autónomo con imports, montaje interactivo de Drive, preparación, controles y ejecución protegida por una bandera explícita. No montar Drive ni iniciar cómputo ahora.
4. Adaptar metodología y referencias del artículo, sin añadir resultados del piloto como resultados definitivos; compilar el archivo existente.
5. Verificar código, notebook, controles y documentación; registrar límites de comprobación y actualizar contexto.

La evaluación sigue un protocolo congelado: resultados de prueba por etapa guardados y resumen mostrado al terminar, sin uso adaptativo de las métricas. Un cambio de configuración o entorno esencial impide continuar en el mismo directorio. No se guardan ni leen credenciales. Los checkpoints se serializan con Safetensors; el contenido del corpus nunca se ejecuta.

## Estado de la preparación

Los cinco pasos de preparación están implementados. Pasaron 20 controles locales y los mismos 20 embebidos; se comprobaron sintaxis y autonomía del notebook de 29 celdas. El artículo fue armonizado en español, con 18 referencias citadas y compilación exitosa. Instrucciones: [README_PRINCIPAL_ES.md](README_PRINCIPAL_ES.md). Pendientes de primera ejecución: prueba PyTorch de checkpoint, montaje de Drive y verificación de primera etapa/reanudación. No se ejecutó ninguno de los 48 ajustes del principal.
