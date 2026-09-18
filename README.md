# andres-romero

Sitio web trilingüe (alemán · español · inglés) del guitarrista **Andrés Romero**,
editable por él mismo desde un CMS y desplegado en GitHub Pages.

- **Producción:** https://profi-web-de.github.io/andres-romero/
- **Panel de administración:** `/admin`
- **Manual para el cliente:** [user-manual.md](user-manual.md)

---

## Stack

| Pieza | Tecnología | Detalle |
|---|---|---|
| Generador | **Hugo extended** | Versión fijada en el workflow: `0.159.1` (requiere Dart Sass) |
| Tema | **PaperMod** | Vendorizado dentro del repo (`themes/PaperMod`), **no** es submódulo |
| CMS | **Sveltia CMS** | `static/admin/`, backend GitHub, config compatible con Decap/Netlify CMS |
| Hosting | **GitHub Pages** | Deploy vía GitHub Actions |
| Formulario | **formsubmit.co** | Envío AJAX, sin backend propio |
| Analítica | **Google Analytics 4** | Con banner de consentimiento propio. **Hoy desactivada** |
| Idiomas | `de` (por defecto) + `es` + `en` | `i18n.structure: multiple_files` |

---

## Estructura

```
.
├── .github/workflows/hugo.yml     # Build + deploy a GitHub Pages
├── hugo.toml                      # Config del sitio, idiomas y menús
├── archetypes/                    # Plantillas de front matter
├── assets/
│   ├── css/extended/              # CSS extra a nivel de proyecto
│   ├── fonts/                     # Tipografías autoalojadas (woff2)
│   └── images/                    # Media del CMS (pasa por el pipeline de Hugo)
├── content/                       # Contenido en .md, un archivo por idioma
├── data/site_settings.yml         # Ajustes globales editables desde el CMS
├── layouts/                       # Overrides de proyecto (ganan sobre el tema)
├── scripts/
│   ├── make-favicons.py           # Genera los iconos desde un solo color
│   └── sync_instagram.py          # Sincronización del feed (hoy sin usar)
├── static/                        # Panel del CMS, iconos, imagen de compartir
└── themes/PaperMod/               # Tema + TODAS las customizaciones
```

> **Precedencia:** existen dos `footer.html` (en `layouts/partials/` y en el
> tema). Hugo usa siempre el de la raíz del proyecto.

---

## Idiomas

Alemán es el idioma por defecto y **omite el sufijo**; español e inglés lo llevan:

```
content/about.md       → alemán  (/about/)
content/about.es.md    → español (/es/about/)
content/about.en.md    → inglés  (/en/about/)
```

Toda página nueva debe crearse en **los tres** idiomas.

> **Trampa de TOML:** `defaultContentLanguage` tiene que ir **antes** de
> cualquier cabecera `[tabla]` en `hugo.toml`. Dentro de una tabla, TOML la
> trata como clave de esa tabla y Hugo cae en silencio a `en`.

> **Trampa de YAML:** un escalar sin comillas que contenga `": "` rompe el
> parseo del front matter. Los campos de texto libre van entre comillas.

---

## Secciones

| Ruta | Layout |
|---|---|
| `content/_index.md` | `partials/index_profile.html` (hero, conciertos, video) |
| `content/home/*.md` | Fragmentos de la portada, leídos por el layout de la home |
| `content/about.md` | `_default/single.html` |
| `content/projects/_index.md` | `projects/list.html` — bandas y formaciones |
| `content/concerts/` | `concerts/list.html` + `single.html` |
| `content/teaching/_index.md` | `teaching/list.html` — clases de guitarra |
| `content/images/_index.md` | `images/list.html` — galería con lightbox |
| `content/videos/_index.md` | `videos/list.html` + `single.html` |
| `content/audios/_index.md` | `audios/list.html` |
| `content/instagram/_index.md` | `instagram/list.html` |
| `content/contact.md` | `contact/single.html` (`type: contact`) |
| `content/impressum.md` · `privacy.md` | `_default/single.html` |

### Galerías y proyectos: listas, no carpetas

Las galerías y los proyectos **no** son carpetas de páginas: son arrays en el
front matter del `_index` de cada sección (`gallery_items`, `gallery_videos`,
`gallery_audios`, `gallery_projects`). Así se reordenan arrastrando desde el CMS
y se ocultan elementos sin borrarlos, con el flag `enabled`.

### Visibilidad de secciones

`show_page` controla si una sección aparece en el menú, en el pie y en su propia
página, **sin borrar el contenido**. La regla vive en un único sitio,
`layouts/partials/section-visible.html`, para que menú y página no se
contradigan. Hoy están ocultas **conciertos**, **audios** e **instagram**.

---

## Tres piezas, un solo cambio

El **CMS**, el **front matter** y el **layout** describen lo mismo. Si se cambian
los campos en `static/admin/config.yml` sin tocar el layout, la página sale
vacía y **el build no falla**: no hay error, solo una sección en blanco. Se
tocan juntos y se comprueba con un build.

Además, el CMS **borra al guardar** cualquier clave del front matter que no
declare en su configuración. Por eso el `cascade` de `content/home/` vive en
`hugo.toml` y no en el front matter.

---

## Pipeline de imágenes

El media vive en `assets/images` (no en `static/`), así que Hugo lo procesa en
el build: redimensiona, convierte a **WebP** y genera `srcset` + `width`/`height`.

Dos partials encapsulan todo: `responsive-image.html` devuelve un `<img>`
completo e `image-url.html` solo la URL de una versión procesada.

**No hace falta optimizar a mano** antes de subir una imagen. Lo único que
importa es subirla con resolución suficiente y en la proporción correcta.

> `responsive-image.html` emite `width`/`height` como atributos HTML, y esa
> altura es definitiva: cualquier regla con `aspect-ratio` necesita también
> `height: auto` o se ignora en silencio.

---

## Tipografías

Autoalojadas en `assets/fonts`, declaradas en `layouts/partials/extend_head.html`.
**No se piden a Google**: cargarlas desde sus servidores transmite la IP del
visitante a un tercero, que es justo lo que el banner de consentimiento intenta
evitar y lo que los tribunales alemanes han considerado problemático.

Los archivos son los `woff2` oficiales, obtenidos de `@fontsource` vía npm.

---

## Legal

`content/impressum.*` y `content/privacy.*`, enlazadas desde el pie. El
Impressum es **obligatorio** en Alemania. Ambas tienen huecos marcados
`PENDIENTE` que tiene que rellenar Andrés.

La página de privacidad lleva el inventario real de lo que el sitio hace con
datos: GitHub Pages, formsubmit.co, YouTube incrustado y GA4 cuando se active.

---

## Desarrollo local

Requisitos: **Hugo extended** `0.159.x` y **Dart Sass**.

```bash
hugo server -D                 # servidor de desarrollo
hugo --minify                  # build de producción en ./public
```

`public/` y `resources/_gen/` están en `.gitignore`: el sitio se compila en CI.

---

## Despliegue

`.github/workflows/hugo.yml` se dispara en cada push a `main`. Cada cambio
guardado desde `/admin` es un commit, así que **publicar desde el CMS dispara el
deploy** (≈1–2 minutos).

El `baseURL` de `hugo.toml` apunta a la project page, pero el workflow lo
sobrescribe con el valor real de Pages. Para un dominio propio hay que añadir
`static/CNAME` y configurar el DNS.

---

## Pendiente

- Dirección visual: tokens de color y pareja tipográfica.
- `scripts/make-favicons.py` con el color definitivo, y el mismo valor en
  `hugo.toml` (`theme_color`) y en `static/favicon.svg`.
- Propiedad de Google Analytics 4 y su ID en `hugo.toml`.
- `booking_email` en `data/site_settings.yml`: sin él, el formulario no se pinta.
- Contenido marcado `PENDIENTE` en `content/`.
- Feed de Instagram: necesita App Review de Meta.
