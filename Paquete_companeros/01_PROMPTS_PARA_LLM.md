# Prompts listos para pegar

Cómo usarlos: abre una conversación nueva en el LLM que prefieran, adjunta o pega `CONTEXTO_COMPLETO_PARA_LLM.md` (contiene todo) y después pega el prompt. Si el modelo tiene poco contexto, pega solo `00_REGLAS_Y_CIFRAS.md` y, además, la sección de `main.tex` que van a trabajar.

Recomendación: trabajen **una sección por vez** (no todo el artículo de golpe), revisen la salida contra las cifras de `00_REGLAS_Y_CIFRAS.md` y copien el resultado a una sola copia del `main.tex` (la de Overleaf).

---

## Prompt 1 — Dar contexto (siempre al inicio)

```
Voy a darte el contexto completo de un artículo de investigación universitario (FES Acatlán, UNAM) sobre contenido sintético y degradación de modelos de lenguaje. El experimento ya se ejecutó y los resultados son definitivos. Lee todo el contexto, sobre todo las reglas y cifras que no se pueden cambiar. No respondas todavía con ediciones: confirma en 5 líneas qué entendiste del estudio (pregunta, diseño, resultado principal, incidencia post hoc) y qué reglas vas a respetar. Después espera mis instrucciones.
```

## Prompt 2 — Humanizar una sección

```
Reescribe la sección que pego abajo para que suene como escrita por estudiantes de matemáticas aplicadas, en español académico claro y natural. Objetivos: variar la sintaxis y el ritmo, eliminar redundancias y frases de relleno, evitar que suene a texto generado por IA (sin listas innecesarias, sin muletillas como «cabe destacar», «es importante mencionar», «en el panorama actual»), y mantener la voz impersonal.
Restricciones estrictas: no cambies ninguna cifra, conteo ni nombre de métrica; no quites ninguna advertencia (análisis post hoc, descriptivo sin pruebas de significación, compatible con una etapa temprana, alcance limitado a un modelo pequeño/español/Wikipedia); no agregues datos ni citas nuevas; conserva todos los \cite, \ref, \label, ecuaciones y tablas. Devuélveme el LaTeX completo de la sección listo para pegar, y al final una lista corta de los cambios de contenido (si los hubo) para que yo los verifique.

Sección:
[PEGAR AQUÍ]
```

## Prompt 3 — Revisar consistencia numérica

```
Compara el texto del artículo (main.tex) con la tabla de cifras de las reglas. Lista cualquier número, porcentaje, conteo o afirmación del texto que no coincida con las cifras, o que afirme más de lo que los datos permiten (causalidad, significancia, generalización). Cita la frase exacta y propón la corrección mínima. No reescribas nada que esté correcto.
```

## Prompt 4 — Detectar afirmaciones sin sustento

```
Revisa esta sección y marca cada afirmación que no esté respaldada por (a) los resultados del experimento, (b) una de las 18 referencias del documento o (c) una definición estándar. Para cada una propón: suavizarla, eliminarla o respaldarla con el pasaje exacto del experimento. No inventes referencias.

Sección:
[PEGAR AQUÍ]
```

## Prompt 5 — Preparar defensa / preguntas del profesor

```
Con base en el artículo y los resultados, genera 15 preguntas difíciles que podría hacer el profesor en la revisión o defensa (diseño, validez, la incidencia de las métricas ausentes y el análisis post hoc, limitaciones, relación con la literatura) y una respuesta breve y honesta para cada una, citando solo lo que está en el documento.
```

## Prompt 6 — Resumen / abstract / ajuste de extensión

```
Reduce [o reescribe] el siguiente texto a aproximadamente [N] palabras sin cambiar cifras ni quitar la advertencia sobre el análisis post hoc. Mantén la voz impersonal y el registro académico.

Texto:
[PEGAR AQUÍ]
```

---

## Advertencias para el equipo
- Verifiquen la política de uso de IA de la materia con el profesor antes de entregar.
- Los LLM tienden a «mejorar» el texto exagerando conclusiones, agregando citas inventadas o cambiando números. Revisen siempre contra `00_REGLAS_Y_CIFRAS.md`.
- Después de humanizar, compilen en Overleaf, revisen que el índice, las tablas y la figura sigan bien, y exporten el PDF.
- Trabajen sobre **una sola copia** del `main.tex` para no mezclar versiones.
