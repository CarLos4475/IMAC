# Presentación (Exposición IMAC)

`index.html` es la presentación completa en un solo archivo (HTML, CSS y JS, sin dependencias de compilación). Solo carga tipografías de Google Fonts, así que necesita conexión para verse con las fuentes correctas.

- Navegación: flechas, espacio, Re Pág / Av Pág, Inicio / Fin, clic (borde izquierdo retrocede) o deslizar en pantallas táctiles.
- La dirección recuerda la diapositiva (`#s7` abre la 7).
- Reparto: Carlos 1–7, Valeria 8–12, Nehiel 13–19.
- Las gráficas se dibujan con los datos reales del experimento (media de 3 repeticiones, barras mínimo y máximo).

## Publicar en Vercel

El `vercel.json` de la raíz del repositorio ya apunta a esta carpeta como salida estática (sin instalación ni compilación). Basta con importar el repositorio en Vercel y desplegar. Si prefieren no usar ese archivo, importen el repositorio con *Root Directory* = `Presentacion` y *Framework Preset* = *Other*.
