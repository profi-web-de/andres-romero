# Manual para cargar imágenes y videos

Este manual explica cómo agregar imágenes a la galería de imágenes y videos a la galería de videos desde el panel de administración del sitio.

## Dónde se editan

- Galería de imágenes: `Multimedia / Resources` -> `Images Gallery`
- Galería de videos: `Multimedia / Resources` -> `Videos Gallery`

## Antes de empezar

- Ten listas las imágenes con buena resolución. No hace falta optimizarlas ni comprimirlas a mano: el sitio genera automáticamente versiones ligeras (WebP) para cada tamaño de pantalla.
- Si vas a publicar un video, ten a mano el enlace de YouTube.
- Revisa siempre los tres idiomas. El sitio está en alemán, español e inglés, así que el título, la descripción y los textos visibles deben actualizarse en las tres versiones.

## Cómo agregar una imagen a la galería de imágenes

1. Entra a `/admin`.
2. Abre `Multimedia / Resources`.
3. Entra en `Images Gallery`.
4. Edita una versión de idioma y luego las demás.
5. Busca la lista `Gallery Images`.
6. Haz clic en `Add Gallery Images` o en el botón para agregar un nuevo elemento.
7. Completa los campos.
8. Guarda o publica los cambios.

### Campos de cada imagen

- `Show in Gallery`: si está activado, la imagen se muestra. Si lo desactivas, la imagen queda guardada pero oculta.
- `Image`: sube o selecciona el archivo.
- `Title`: título visible en la galería.
- `Description`: texto breve opcional.
- `Alt Text`: texto alternativo para accesibilidad y SEO.

### Recomendaciones para imágenes

- Usa imágenes de al menos `1600 px` en el lado más largo.
- No hace falta reducir el peso antes de subirlas: sube la mejor calidad que tengas y el sitio se encarga de generar las versiones optimizadas.
- Si puedes, usa nombres de archivo claros y consistentes, por ejemplo `carlos-johnson-recital-berlin.jpg`.
- Mantén el mismo orden en alemán y en español para que ambas galerías coincidan.

## Cómo agregar un video a la galería de videos

1. Entra a `/admin`.
2. Abre `Multimedia / Resources`.
3. Entra en `Videos Gallery`.
4. Edita una versión de idioma y luego las demás.
5. Busca la lista `Gallery Videos`.
6. Agrega un nuevo elemento.
7. Completa los campos.
8. Guarda o publica los cambios.

### Campos de cada video

- `Show in Gallery`: controla si el video aparece o queda oculto.
- `Title`: título del video.
- `Publication Date`: fecha de publicación o de referencia.
- `YouTube Video ID`: identificador del video en YouTube.
- `Cover Image (optional)`: miniatura personalizada opcional.
- `Description or Concert Notes`: descripción, programa, intérpretes o notas del concierto.

### Cómo obtener el `YouTube Video ID`

No copies el enlace completo. Usa solo la parte final del enlace.

Ejemplos:

- Si la URL es `https://www.youtube.com/watch?v=MGreSb1NjtA`, debes pegar `MGreSb1NjtA`.
- Si la URL es `https://youtu.be/MGreSb1NjtA`, debes pegar `MGreSb1NjtA`.

### Sobre la portada del video

- La portada es opcional.
- Si subes una imagen en `Cover Image`, esa imagen se usa como miniatura en la galería.
- Si no subes portada, la galería usa automáticamente la miniatura de YouTube.

## Orden, edición y ocultación

- En ambas galerías puedes reordenar los elementos desde la lista del CMS.
- El orden de la lista es el orden en que aparecen en la página.
- Si no quieres borrar un elemento, desactiva `Show in Gallery`.

## Revisión antes de publicar

Antes de cerrar el cambio, revisa esto:

- La imagen o el video aparece en la galería correcta.
- El texto está actualizado en alemán y en español.
- El orden de los elementos es correcto.
- El `Alt Text` de las imágenes está completo.
- El `YouTube Video ID` funciona.
- La portada del video se ve bien, si se agregó una.

## Anexo: guía rápida para imágenes del hero de inicio

Estas recomendaciones aplican al carrusel principal de la home.

- Tamaño ideal: `1600 x 2400 px`
- Tamaño mínimo: `1200 x 1800 px`
- Proporción recomendada: `2:3`
- Mejor resultado: retratos verticales
- Mantén el sujeto centrado o ligeramente a la derecha
- Deja margen de seguridad para el recorte en tablet y móvil
- Formato: `JPG` o `PNG` en buena calidad; el sitio genera solo las versiones `WebP` optimizadas

Si solo sigues una regla, exporta cada imagen del hero en `1600 x 2400 px` y verifica que siga funcionando bien con recorte centrado.

## Citas de prensa en la portada

La portada muestra un bloque de citas de crítica. Se edita en `/admin` -> `Homepage` -> `Press Quotes`.

- `Section Title`: el título del bloque, por ejemplo `Prensa`.
- Cada cita tiene el texto (`Quote`), el medio (`Source`) y un enlace opcional (`Link`).
- Escribe la cita **sin comillas**: el sitio las pone solas.
- En `Source` conviene poner medio y año, por ejemplo `Lübeckische Blätter, 2022`.
- Si borras todas las citas, el bloque entero desaparece de la portada.

Recuerda revisar los tres idiomas.

## Bloque de cierre de la portada

Debajo de todo hay un bloque en color con una invitación a escribir. Se edita en `Homepage` -> `Closing Call to Action`.

- `Title`: la pregunta o frase principal.
- `Text`: una línea de contexto.
- `Button Label`: el texto del botón, que siempre lleva a la página de contacto.
- Si dejas el `Title` vacío, el bloque no se muestra.

## Retrato de la biografía

La biografía puede abrir con una foto. Se edita en `/admin` -> `Pages (Biography, etc.)` -> `Biography` -> `Portrait`.

- Funciona mejor una foto **apaisada**: se recorta a formato panorámico.
- Si no subes ninguna, la página simplemente empieza por el texto.

## Cómo mostrar u ocultar la agenda de conciertos

La agenda de conciertos **viene oculta**. Mientras esté oculta no aparece en el menú, ni en el pie, ni en la portada, aunque ya tengas conciertos cargados.

Para mostrarla:

1. Entra a `/admin`.
2. Abre `Concert Schedule - List Page`.
3. Activa `Show Concert Schedule`.
4. Guarda o publica los cambios.

Este interruptor es común a los tres idiomas: lo activas una vez y se aplica al alemán, al español y al inglés.

Para volver a ocultarla, desactívalo. **No se borra nada**: los conciertos cargados siguen guardados y vuelven a aparecer cuando la actives de nuevo.

Conviene activarla solo cuando haya fechas confirmadas, y volver a ocultarla si la agenda se queda sin próximos conciertos durante una temporada.

## La sección de Instagram

La sección de Instagram se llena sola: una vez al día el sitio consulta la cuenta, **se descarga las fotos y las leyendas** y las publica. No hay que copiar ni pegar nada.

Como las fotos quedan guardadas en el sitio, si un día Instagram falla o la conexión caduca, lo último que se sincronizó sigue publicado. La página no se rompe nunca.

### Qué se puede editar y qué no

Las publicaciones **no se editan a mano**. Si cambias una leyenda desde el panel, la siguiente sincronización la vuelve a pisar con la de Instagram. Lo que sí controlas está en `/admin` → `Instagram Feed`:

- **Show Page in Submenu**: muestra u oculta la sección entera. Viene oculta.
- **Title** y **Subtitle**: el titular de la página, en cada idioma.
- **Posts to Show**: cuántas publicaciones se ven (hasta 12).
- **Show Captions**: si se muestran las leyendas o solo las fotos.
- **Caption Language**: el idioma en el que escribes en Instagram. Instagram da una sola leyenda por publicación, así que se muestra tal cual en las tres versiones del sitio; este campo sirve para que los lectores de pantalla la pronuncien bien.
- **Per-post Exceptions**: para **ocultar una publicación concreta** o corregirle el texto alternativo. Necesitas el identificador de la publicación, que aparece en `data/instagram.json`.

### Qué hace falta para activarla

Dos cosas que no dependen del sitio:

1. Que la cuenta de Instagram sea **Creator o Business**. Es gratis, se cambia desde la propia aplicación y se puede volver atrás.
2. Que el desarrollador conecte la cuenta una vez para autorizar el acceso.

Hasta entonces la sección queda oculta y con publicaciones de ejemplo.

### Una advertencia

La autorización de Instagram **caduca cada 60 días**. Está previsto que se renueve sola, pero si algún día la sección deja de actualizarse, ese suele ser el motivo: avisa al desarrollador.

## Configuración de Google Analytics 4

La integración de GA4 quedó implementada en el tema para que, en usos futuros, solo haya que configurar el ID.

### Paso único de configuración

En [hugo.toml](hugo.toml), completa este valor:

```toml
[services]
  [services.googleAnalytics]
    id = "G-XXXXXXXXXX"
```

Si el `id` está vacío, GA4 no se carga y el banner de consentimiento no aparece.

### Qué hace la integración

- Carga GA4 solo en producción.
- No activa analítica hasta que la persona acepte.
- Mantiene `ad_storage` desactivado y solo habilita `analytics_storage` tras consentimiento.
- No mide `/admin`.
- Registra automáticamente `page_view` cuando hay consentimiento.
- Registra eventos reutilizables como clics salientes y envío correcto del formulario de contacto.

### Dónde quedó implementado

- Partial principal de GA4: `themes/PaperMod/layouts/partials/google_analytics.html`
- Banner y gestión de consentimiento: `themes/PaperMod/layouts/partials/footer.html`
- Estilos del banner: `themes/PaperMod/assets/css/extended/analytics-consent.css`

### Verificación recomendada

1. Configura el `id` de GA4.
2. Levanta el sitio en producción o revisa el despliegue de GitHub Pages.
3. Acepta la analítica en el banner.
4. Revisa `DebugView` en GA4.
5. Confirma que aparecen `page_view`, `outbound_click` y `contact_form_submit_success`.
