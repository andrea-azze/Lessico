"""Genera le icone di Lessico (libro con bandiera inglese) in icons/.
Uso:  python3 tools/make_icons.py   (richiede Pillow)"""
import os
from PIL import Image, ImageDraw

S = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")

def union_jack(w, h):
    k = 4
    W, H = w * k, h * k
    im = Image.new("RGB", (W, H), "#012169")
    d = ImageDraw.Draw(im)
    def diag(width, color):
        for a, b in (((0, 0), (W, H)), ((W, 0), (0, H))):
            d.line([a, b], fill=color, width=int(width))
    diag(H * 0.22, "white")
    diag(H * 0.085, "#C8102E")
    d.rectangle([0, H * 0.5 - H * 0.17, W, H * 0.5 + H * 0.17], fill="white")
    d.rectangle([W * 0.5 - W * 0.12, 0, W * 0.5 + W * 0.12, H], fill="white")
    d.rectangle([0, H * 0.5 - H * 0.10, W, H * 0.5 + H * 0.10], fill="#C8102E")
    d.rectangle([W * 0.5 - W * 0.07, 0, W * 0.5 + W * 0.07, H], fill="#C8102E")
    return im.resize((w, h), Image.LANCZOS)

def build():
    bg = Image.new("RGB", (S, S), "#1B2730")
    d = ImageDraw.Draw(bg)
    # pagine (sotto la copertina), dorso e copertina con bandiera
    bx0, by0, bx1, by1 = 232, 150, 792, 874
    d.rounded_rectangle([bx0 + 34, by0 + 34, bx1 + 22, by1 + 22], 40, fill="#F4EFE2")   # blocco pagine
    for i in range(5):
        y = by1 + 4 + i * 5
        d.line([(bx0 + 70, y), (bx1 + 10, y)], fill="#CFC8B4", width=3)
    cover_w, cover_h = bx1 - bx0, by1 - by0
    flag = union_jack(cover_w, cover_h)
    mask = Image.new("L", (cover_w, cover_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cover_w - 1, cover_h - 1], 44, fill=255)
    bg.paste(flag, (bx0, by0), mask)
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([bx0, by0, bx0 + 62, by1], 44, fill="#0B1A3D")                  # dorso
    d.rectangle([bx0 + 30, by0, bx0 + 62, by1], fill="#0B1A3D")
    d.line([(bx0 + 62, by0 + 10), (bx0 + 62, by1 - 10)], fill="#34456E", width=4)
    return bg

os.makedirs(OUT, exist_ok=True)
base = build()
for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
    base.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
print("icone create in", os.path.abspath(OUT))
