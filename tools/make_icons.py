"""Genera le icone di Lessico (libro blu con piccola bandiera inglese in alto) in icons/.
Uso:  python3 tools/make_icons.py   (richiede Pillow)"""
import os
from PIL import Image, ImageDraw, ImageFilter

S = 1024          # lato dell'icona "grande"
Q = 3             # sovracampionamento: si disegna 3 volte più grande e poi si riduce (bordi lisci)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")

SFONDO = "#EEF1EC"      # lo stesso chiaro dell'app
COPERTINA = "#5B9BEA"
DORSO = "#4683DB"
DORSO_SCURO = "#3B73C8"
BORDO_BASSO = "#3866BE"
PAGINE = "#D9D6CB"
PAGINE_LUCE = "#E8E5DC"
PAGINE_OMBRA = "#C6C3B7"
TAPPO = "#1F2A5C"

def q(*v):
    return [round(x * Q) for x in v]

def union_jack(w, h):
    """Bandiera inglese (Union Jack) nelle proporzioni 2:1."""
    k = 4
    W, H = w * k, h * k
    im = Image.new("RGB", (W, H), "#012169")
    d = ImageDraw.Draw(im)
    def diag(width, color):
        for (x0, y0), (x1, y1) in (((0, 0), (W, H)), ((W, 0), (0, H))):
            dx, dy = x1 - x0, y1 - y0   # si allunga la linea oltre gli angoli, così non restano buchi
            d.line([(x0 - dx * .1, y0 - dy * .1), (x1 + dx * .1, y1 + dy * .1)], fill=color, width=int(width))
    diag(H * 0.22, "white")
    diag(H * 0.07, "#C8102E")
    d.rectangle([0, H * 0.5 - H * 0.167, W, H * 0.5 + H * 0.167], fill="white")
    d.rectangle([W * 0.5 - H * 0.167, 0, W * 0.5 + H * 0.167, H], fill="white")
    d.rectangle([0, H * 0.5 - H * 0.10, W, H * 0.5 + H * 0.10], fill="#C8102E")
    d.rectangle([W * 0.5 - H * 0.10, 0, W * 0.5 + H * 0.10, H], fill="#C8102E")
    return im.resize((w, h), Image.LANCZOS)

def build():
    img = Image.new("RGB", (S * Q, S * Q), SFONDO)

    # --- libro: tutti i pezzi su un livello, poi ritagliati con la sagoma arrotondata ---
    bx0, by0, bx1, by1 = 170, 104, 854, 920
    livello = Image.new("RGB", img.size, COPERTINA)
    d = ImageDraw.Draw(livello)
    d.rectangle(q(bx0, by0, bx0 + 116, by1), fill=DORSO)                     # dorso
    d.rectangle(q(bx0 + 68, by0, bx0 + 116, by1), fill=DORSO_SCURO)          # incavo del dorso
    d.rectangle(q(bx0, by1 - 132, bx1, by1), fill=BORDO_BASSO)               # bordo sotto la copertina
    d.rectangle(q(bx0 + 70, by1 - 130, bx0 + 116, by1), fill="#2E58AA")      # dorso in basso, più scuro

    sagoma = Image.new("L", img.size, 0)
    ImageDraw.Draw(sagoma).rounded_rectangle(q(bx0, by0, bx1, by1), round(34 * Q), fill=255)
    img.paste(livello, (0, 0), sagoma)

    # --- pagine in basso ---
    d = ImageDraw.Draw(img)
    py0, py1 = by1 - 150, by1 - 36
    d.rounded_rectangle(q(bx0 + 24, py0 - 4, bx0 + 84, py1 + 4), round(26 * Q), fill=TAPPO)   # tappo scuro a sinistra
    d.rounded_rectangle(q(bx0 + 48, py0, bx1 - 14, py1), round(30 * Q), fill=PAGINE)
    d.rounded_rectangle(q(bx0 + 62, py0 + 8, bx1 - 30, py0 + 36), round(14 * Q), fill=PAGINE_LUCE)
    d.rounded_rectangle(q(bx0 + 62, py1 - 30, bx1 - 30, py1 - 8), round(12 * Q), fill=PAGINE_OMBRA)

    # --- bandiera inglese in alto sulla copertina (la zona cerchiata) ---
    fw, fh = 440, 220
    cx = (bx0 + 116 + bx1) / 2
    fx0, fy0 = round(cx - fw / 2), by0 + 70
    flag = union_jack(fw * Q, fh * Q)
    maschera = Image.new("L", flag.size, 0)
    ImageDraw.Draw(maschera).rounded_rectangle([0, 0, flag.width - 1, flag.height - 1], round(12 * Q), fill=255)

    ombra = Image.new("L", img.size, 0)
    ImageDraw.Draw(ombra).rounded_rectangle(q(fx0, fy0 + 10, fx0 + fw, fy0 + fh + 10), round(12 * Q), fill=110)
    ombra = ombra.filter(ImageFilter.GaussianBlur(10 * Q))
    img.paste(Image.new("RGB", img.size, "#1D3F7A"), (0, 0), ombra)
    img.paste(flag, (fx0 * Q, fy0 * Q), maschera)

    return img.resize((S, S), Image.LANCZOS)

os.makedirs(OUT, exist_ok=True)
base = build()
for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
    base.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)
print("icone create in", os.path.abspath(OUT))
