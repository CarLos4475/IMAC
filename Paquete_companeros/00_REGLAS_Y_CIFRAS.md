# Reglas y cifras que NO deben cambiar (contexto breve)

## Qué es el trabajo
Artículo de investigación para la materia «Investigación en Matemáticas Aplicadas y Computación» (FES Acatlán, UNAM). Profesor: Sergio Quiroz Almaraz. Equipo: Carlos Emiliano Segura Loera, Valeria Hernandez Santos, Nehiel Ramirez Hernandez.

Título: «Contenido sintético en Internet y degradación de modelos de lenguaje».

Pregunta principal: ¿Cómo cambia la diversidad del contenido generado por modelos de lenguaje cuando se incorporan repetidamente datos sintéticos al proceso de entrenamiento?

Hipótesis: al aumentar la proporción de texto sintético y el número de ciclos recursivos, la diversidad del texto generado disminuye y la repetición aumenta.

## Experimento realizado (ya ejecutado; no se puede rehacer ni modificar)
- Modelo: `datificate/gpt2-small-spanish` (124 439 808 parámetros). Datos: Wikipedia en español (`wikimedia/wikipedia`, 20231101.es), primeros 2000 artículos, partición por hash 80/10/10, semilla 20261109. Ventanas: 512 de ajuste, 128 de validación, 128 de prueba (64 tokens de contexto + 128 de continuación).
- Tres proporciones de sustitución sintética α = 0, 0.5 y 1; cinco ciclos; tres repeticiones; 48 ajustes (3 modelos base M0 + 45). Cada ajuste reinicia desde el modelo preentrenado. AdamW, lr 2e-5, 64 actualizaciones, lote efectivo 8. Muestreo T = 1, top-p 0.95, 128 tokens. La mezcla α se aplica solo a las continuaciones (65 536 tokens objetivo por ajuste).
- Métricas: perplejidad sobre texto humano (128 contextos de prueba), Distinct-2, Distinct-3, repetición de 4-gramas, dispersión semántica (1 − coseno con MiniLM multilingüe). Ventana W = 30 palabras.
- Análisis descriptivo: media y rango de las 3 cadenas, diferencias frente a M0 y frente al control α = 0. **No hay valores p ni pruebas de significación.**
- Cómputo: Colab Tesla T4, ≈ 2.8 h, una reanudación.

## Incidencia que debe seguir declarada (desviación del protocolo)
La regla preregistrada (si alguna de las 128 continuaciones tenía menos de W = 30 palabras, la etapa quedaba sin métricas léxicas/semánticas) dejó sin esas métricas a 39 de 48 etapas. 75 de 6 144 continuaciones fueron cortas (M0: 2; α = 0: 19; α = 0.5: 16; α = 1: 38). Por eso se hizo un **análisis complementario post hoc** (decidido después de ver los faltantes) sobre los 90 contextos que alcanzan W en las 48 etapas. Esto excluye 38 contextos, probablemente de los más degradados. La perplejidad sí usa los 128 contextos (preregistrada). Esta aclaración no debe suavizarse ni eliminarse.

## Cifras (media de 3 cadenas, ciclo 5)
| Métrica | M0 | α=0 | α=0.5 | α=1 |
|---|---|---|---|---|
| Perplejidad (128 contextos) | 30.46 | 30.47 | 31.90 | 39.30 |
| Distinct-2 (90) | 0.913 | 0.905 | 0.896 | 0.825 |
| Distinct-3 (90) | 0.990 | 0.985 | 0.984 | 0.940 |
| Repetición 4-gramas (90) | 0.003 | 0.004 | 0.005 | 0.035 |
| Dispersión semántica (90) | 0.883 | 0.890 | 0.898 | 0.903 |

- α = 1: perplejidad +8.83 (≈ +29 %), creciente en cada ciclo; baja la diversidad léxica y sube la repetición; las 3 cadenas van en la misma dirección.
- α = 0.5: perplejidad +1.44 (≈ +4.7 %), estable desde el ciclo 1–2; cambios léxicos pequeños e inconsistentes.
- α = 0: estable.
- Dispersión semántica: **no disminuye**; ligero aumento en todas las condiciones.
- Conclusión sobre la hipótesis: **apoyada parcialmente** (se observa en lo léxico y en la repetición bajo reemplazo total, no en lo semántico). Se describe como «compatible con una etapa temprana» del deterioro, no como colapso demostrado.

## Reglas de redacción
1. Español académico, voz impersonal («se observó», «se propone»), prosa clara y prudente. Sin lenguaje sensacionalista ni grandilocuente.
2. No cambiar ninguna cifra, signo, proporción, nombre de métrica ni conteo (48 ajustes, 3 repeticiones, 5 ciclos, 90 y 128 contextos, 39/48, 75/6144…).
3. No inventar datos, resultados, citas, referencias ni autores. Solo se pueden citar las 18 referencias que ya están en `\begin{thebibliography}` de `main.tex`; conservar sus claves `\cite{...}`.
4. No afirmar causalidad ni generalizar más allá de: un modelo pequeño (GPT-2 small), un idioma (español), un corpus (Wikipedia), 5 ciclos.
5. No afirmar que el entrenamiento sintético siempre causa colapso, ni que diversidad alta implique calidad.
6. No presentar el análisis como inferencial; no añadir «significativo», «p < …», intervalos de confianza ni pruebas.
7. Mantener la estructura de secciones (ver `articulo/main.tex`) y las etiquetas `\label`/`\ref`, tablas, figura y anexos. Solo se entrega el PDF: evitar referencias a archivos, carpetas, notebooks o repositorios dentro del texto.
8. Conservar el LaTeX válido: no romper `\cite`, `\ref`, `$...$`, `\input`, entornos ni tablas. Los acentos van en UTF-8 normal.
9. «Humanizar» significa: variar sintaxis y ritmo, usar el vocabulario propio del equipo, quitar muletillas y redundancias, pero conservando el contenido técnico exacto.
10. No declarar pruebas, validaciones o experimentos que no se hicieron.
