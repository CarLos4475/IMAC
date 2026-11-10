# Contenido sintético en Internet y degradación de modelos de lenguaje

Proyecto de la asignatura *Investigación en Matemáticas Aplicadas y Computación* (FES Acatlán, UNAM).
Equipo: Valeria Hernández Santos, Nehiel Ramírez Hernández y Carlos. Profesor: Sergio Quiroz Almaraz.

Estudio experimental de *model collapse*: un GPT-2 pequeño en español se reentrena durante cinco ciclos con 0, 50 y 100 % de continuaciones sintéticas (tres repeticiones, 48 ajustes en Google Colab con una GPU T4).

## Estructura
- `Manuscrito/main.tex`: artículo (Resultados, Discusión y Conclusiones incluidos). Tablas y figura en `Manuscrito/resultados_generados/`.
- `Capitulado/`: entregable de capitulado y justificación.
- `Experimentos/`: notebooks del piloto y del estudio principal, código fuente, pruebas y scripts de análisis.
- `Experimentos/resultados/`: resultados del piloto (9 nov 2026) y del estudio principal (10 nov 2026); ver `RESUMEN.md` en cada carpeta.
- `contexto/` y `model_collapse_proyecto_contexto.md`: contexto, decisiones y registro del proyecto.

## Reproducir tablas y figura
```
cd Experimentos
python analisis_complementario_es.py resultados/principal_es_2026-11-10/extraido
python generar_resultados_latex.py resultados/principal_es_2026-11-10/complementario
```
