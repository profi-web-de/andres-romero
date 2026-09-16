#!/usr/bin/env python3
"""Sincroniza las ultimas publicaciones de Instagram en el repositorio.

Por que descargar las imagenes en vez de enlazarlas: las URL que devuelve la
API son de un CDN firmado y caducan a los pocos dias. Si se enlazan en caliente,
el feed se rompe solo. Bajandolas, ademas pasan por el pipeline de imagenes de
Hugo (WebP + srcset) como el resto del sitio.

Escribe:
  data/instagram.json          <- lo consume layouts/instagram/list.html
  assets/images/instagram/*    <- las imagenes, servidas desde /images/instagram/

NUNCA se editan a mano: la siguiente sincronizacion los sobreescribe. Lo
editable (titulo, visibilidad, excepciones por publicacion) vive en
content/instagram/_index.*.md.

Uso:
  IG_ACCESS_TOKEN=... python3 scripts/sync_instagram.py
  IG_ACCESS_TOKEN=... python3 scripts/sync_instagram.py --refresh-token

Sin token no falla: avisa y no toca nada, para que el sitio siga publicado con
la ultima instantanea buena.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "instagram.json"
IMAGE_DIR = ROOT / "assets" / "images" / "instagram"
PUBLIC_PREFIX = "/images/instagram"

API_HOST = os.environ.get("IG_API_HOST", "https://graph.instagram.com")
API_VERSION = os.environ.get("IG_API_VERSION", "").strip()
LIMIT = int(os.environ.get("IG_LIMIT", "12"))
TIMEOUT = 30

FIELDS = (
    "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,"
    "children{media_type,media_url,thumbnail_url}"
)


def log(message: str) -> None:
    print(f"[instagram] {message}", flush=True)


def api_url(path: str) -> str:
    base = f"{API_HOST}/{API_VERSION}" if API_VERSION else API_HOST
    return f"{base.rstrip('/')}/{path.lstrip('/')}"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        return json.load(response)


def strip_trailing_hashtags(caption: str) -> str:
    """Quita el bloque de hashtags del final, que en la web es solo ruido.

    Solo el del final: un hashtag en mitad de una frase forma parte del texto.
    """
    text = (caption or "").strip()
    if not text:
        return ""

    def is_droppable(line: str) -> bool:
        tokens = line.split()
        if not tokens:
            return True
        # Una linea de solo puntos es el separador que se usa en Instagram para
        # empujar los hashtags fuera de la vista previa.
        if all(set(token) <= {".", "\u00b7", "\u2022", "-", "\u2014"} for token in tokens):
            return True
        return all(token.startswith("#") for token in tokens)

    lines = text.split("\n")
    while lines and is_droppable(lines[-1]):
        lines.pop()

    if lines:
        tokens = lines[-1].split()
        while tokens and tokens[-1].startswith("#"):
            tokens.pop()
        lines[-1] = " ".join(tokens)
        while lines and is_droppable(lines[-1]):
            lines.pop()

    return "\n".join(lines).strip()


def pick_image_url(post: dict) -> str | None:
    """Una sola imagen por publicacion: la del post, la miniatura del video o
    el primer elemento del carrusel."""
    media_type = post.get("media_type")
    if media_type == "VIDEO":
        return post.get("thumbnail_url") or post.get("media_url")
    if media_type == "CAROUSEL_ALBUM":
        children = (post.get("children") or {}).get("data") or []
        for child in children:
            url = (
                child.get("thumbnail_url")
                if child.get("media_type") == "VIDEO"
                else child.get("media_url")
            )
            if url:
                return url
        return post.get("media_url")
    return post.get("media_url")


def download(url: str, destination: Path) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return True
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            temporary.write_bytes(response.read())
    except (urllib.error.URLError, OSError) as error:
        log(f"no se pudo descargar {destination.name}: {error}")
        temporary.unlink(missing_ok=True)
        return False
    if temporary.stat().st_size == 0:
        temporary.unlink(missing_ok=True)
        return False
    temporary.replace(destination)
    return True


def refresh_token(token: str) -> int:
    """Imprime un token nuevo de 60 dias. El viejo sigue valido hasta caducar,
    asi que solo sirve si quien llama lo guarda."""
    url = api_url("refresh_access_token") + "?" + urllib.parse.urlencode(
        {"grant_type": "ig_refresh_token", "access_token": token}
    )
    try:
        payload = get_json(url)
    except (urllib.error.URLError, OSError, ValueError) as error:
        log(f"no se pudo refrescar el token: {error}")
        return 1
    new_token = payload.get("access_token")
    if not new_token:
        log("la respuesta de refresco no traia token")
        return 1
    log(f"token refrescado, caduca en {payload.get('expires_in', '?')} s")
    print(new_token)
    return 0


def main() -> int:
    token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not token:
        log("sin IG_ACCESS_TOKEN: no se toca nada y se conserva la ultima instantanea")
        return 0

    if "--refresh-token" in sys.argv:
        return refresh_token(token)

    url = api_url("me/media") + "?" + urllib.parse.urlencode(
        {"fields": FIELDS, "limit": LIMIT, "access_token": token}
    )
    try:
        payload = get_json(url)
    except (urllib.error.URLError, OSError, ValueError) as error:
        # Un fallo de red o un token caducado no pueden dejar el sitio sin feed.
        log(f"la API fallo ({error}); se conserva la ultima instantanea")
        return 0

    raw_posts = payload.get("data") or []
    if not raw_posts:
        log("la API no devolvio publicaciones; se conserva la ultima instantanea")
        return 0

    posts = []
    for raw in raw_posts:
        post_id = str(raw.get("id") or "").strip()
        image_url = pick_image_url(raw)
        if not post_id or not image_url:
            continue
        filename = f"{re.sub(r'[^A-Za-z0-9_-]', '', post_id)}.jpg"
        if not download(image_url, IMAGE_DIR / filename):
            continue
        posts.append(
            {
                "id": post_id,
                "media_type": raw.get("media_type", "IMAGE"),
                "is_video": raw.get("media_type") == "VIDEO",
                "image": f"{PUBLIC_PREFIX}/{filename}",
                "permalink": raw.get("permalink", ""),
                "timestamp": raw.get("timestamp", ""),
                "caption": strip_trailing_hashtags(raw.get("caption", "")),
            }
        )

    if not posts:
        log("ninguna publicacion utilizable; se conserva la ultima instantanea")
        return 0

    posts.sort(key=lambda item: item["timestamp"], reverse=True)

    previous = {}
    if DATA_FILE.exists():
        try:
            previous = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except ValueError:
            previous = {}

    feed = {
        "demo": False,
        "profile": previous.get("profile", {}),
        "synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "posts": posts,
    }

    DATA_FILE.write_text(
        json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Limpieza: las imagenes de publicaciones que ya no estan en el feed.
    keep = {Path(post["image"]).name for post in posts}
    if IMAGE_DIR.exists():
        for stale in IMAGE_DIR.iterdir():
            if stale.is_file() and stale.name not in keep:
                stale.unlink()
                log(f"eliminada {stale.name} (ya no esta en el feed)")

    log(f"{len(posts)} publicaciones sincronizadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
