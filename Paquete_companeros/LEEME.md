# Paquete para el equipo — Artículo IMAC (versión del 10 de noviembre de 2026)

Esta carpeta reúne todo lo necesario para que cualquier integrante del equipo (o cualquier LLM) tenga el contexto completo del proyecto.

## Empiecen por aquí
1. `00_REGLAS_Y_CIFRAS.md` — resumen de una página: qué se hizo, cifras finales y reglas de redacción que no se pueden romper.
2. `01_PROMPTS_PARA_LLM.md` — prompts listos para humanizar secciones, revisar consistencia, preparar defensa, etc.
3. `CONTEXTO_COMPLETO_PARA_LLM.md` — **un solo archivo** con todo (reglas, resultados, decisiones, capitulado, preguntas de investigación y el `main.tex` completo). Es el que se adjunta o pega en otro LLM.
4. `CONTEXTO_BREVE_PARA_LLM.md` — lo mismo pero sin el `main.tex` (para modelos con poco contexto; se pega aparte la sección que se vaya a trabajar).

## Carpetas
- `articulo/` — `main.tex` (artículo actual), `Overleaf_IMAC.zip` (súbanlo tal cual a Overleaf y compila: incluye figura y tablas) y un PDF de referencia compilado en Overleaf (puede no reflejar los últimos cambios).
- `resultados/` — resumen de resultados, `results.csv` (datos originales de los 48 ajustes), `results_complementario.csv` y `semantica_complementaria.csv` (análisis post hoc), contrastes, protocolo, tiempos y figuras.
- `contexto_proyecto/` — contexto maestro del proyecto, decisiones, criterios editoriales, estado y pendientes, fuentes del marco teórico, comparación del estado del arte, propuesta de metodología y revisión bibliográfica.
- `preguntas_y_capitulado/` — preguntas de investigación y capitulado entregado/revisado.
- `codigo/` — notebook del experimento (Colab) y scripts de análisis y generación de tablas.

## Qué falta
- Que cada quien reescriba («humanice») sus secciones con su voz, sin cambiar cifras ni advertencias.
- Compilar en Overleaf y exportar el PDF (solo se entrega el PDF).
- Poner acentos en los nombres de la carátula si el equipo lo desea.
- Verificar con el profesor la política de uso de IA.

## Importante
- No se debe volver a ejecutar ni modificar el experimento: los resultados son definitivos.
- El archivo `AGENTS.md` dentro de `contexto_proyecto/` son instrucciones internas para asistentes de IA; pueden ignorarlo.
