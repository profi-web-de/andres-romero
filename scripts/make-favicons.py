#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los iconos del sitio a partir de un solo color.

El <head> de PaperMod pide favicon-16x16.png, favicon-32x32.png,
apple-touch-icon.png y safari-pinned-tab.svg ademas del favicon.svg. Sin ellos
el navegador se come cuatro 404 en cada visita.

Cuando se elija la direccion visual, cambia BG (y FG si hace falta) y vuelve a
ejecutarlo. El mismo color tiene que ir en:
  - static/favicon.svg
  - hugo.toml -> params.assets.theme_color y msapplication_TileColor

    A Pico  #e0402a   B Andes #1f6b4a   C Marcador #ffd400 (FG #0e0e0e)
    D Neon  #2f5cff

Uso:  python3 scripts/make-favicons.py [color-de-fondo] [color-de-letra]
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont

BG = sys.argv[1] if len(sys.argv) > 1 else "#111111"
FG = sys.argv[2] if len(sys.argv) > 2 else "#ffffff"
TEXT = "AR"
OUT = pathlib.Path(__file__).resolve().parent.parent / "static"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def icon(size, radius_ratio=0.1875, pad_ratio=0.0):
    img = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s, r = size * 4, int(size * 4 * radius_ratio)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=BG)
    # El tamano de letra se busca por medida real: "AR" no ocupa lo mismo en
    # cada fuente y a 16 px cualquier desajuste se nota.
    target = s * (0.58 if size > 20 else 0.68)
    fs = int(target)
    while fs > 4:
        f = ImageFont.truetype(FONT, fs)
        box = d.textbbox((0, 0), TEXT, font=f)
        if box[2] - box[0] <= s * 0.74:
            break
        fs -= 2
    box = d.textbbox((0, 0), TEXT, font=f)
    d.text(((s - (box[2] - box[0])) / 2 - box[0],
            (s - (box[3] - box[1])) / 2 - box[1]), TEXT, font=f, fill=FG)
    return img.resize((size, size), Image.LANCZOS)


for name, size in [("favicon-16x16.png", 16), ("favicon-32x32.png", 32),
                   ("apple-touch-icon.png", 180)]:
    icon(size).save(OUT / name, "PNG", optimize=True)
    print("%-24s %dx%d" % (name, size, size))

# Safari pinned tab: silueta monocroma, sin fondo. El navegador la recolorea.
(OUT / "safari-pinned-tab.svg").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
    '  <text x="32" y="45" font-family="Helvetica, Arial, sans-serif" '
    'font-size="34" font-weight="700" text-anchor="middle" fill="black">AR</text>\n'
    '</svg>\n', encoding="utf-8")
print("safari-pinned-tab.svg")
