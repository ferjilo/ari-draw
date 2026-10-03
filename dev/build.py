"""Genera index.html (la web) a partir de src/app.html + los dibujos Reto de dev/dibujos/.
Uso: python3 dev/build.py"""
import base64, importlib, io, json, os, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
sys.path.insert(0, os.path.join(here, "dibujos"))

# Orden de los animales del nivel Reto (cada uno es un fichero en dev/dibujos/<nombre>.py con LESSON)
ANIMALES_RETO = ["gato", "pez", "tortuga", "buho", "raton"]

reto = []
for n in ANIMALES_RETO:
    L = importlib.import_module(n).LESSON; L["reto"] = True; reto.append(L)
json.dump(reto, open(os.path.join(here, "dibujos", "reto.json"), "w"), ensure_ascii=False)

src = open(os.path.join(root, "src", "app.html")).read()
assert src.count("__RETO__") == 1
body = src.replace("__RETO__", json.dumps(reto, ensure_ascii=False))

from PIL import Image, ImageDraw   # icono de la pantalla de inicio (gato)
S = 180; im = Image.new("RGB", (S, S), "#D9622B"); d = ImageDraw.Draw(im); ink = "#2F3A56"
d.polygon([(48,78),(54,28),(86,56)], fill="#F7B267", outline=ink, width=7)
d.polygon([(132,78),(126,28),(94,56)], fill="#F7B267", outline=ink, width=7)
d.ellipse((34,46,146,158), fill="#F7B267", outline=ink, width=7)
for cx in (70,110): d.ellipse((cx-10,86,cx+10,106), fill="#9BD67B", outline=ink, width=5)
d.polygon([(82,118),(98,118),(90,128)], fill="#F28AA0", outline=ink)
buf = io.BytesIO(); im.save(buf, "PNG"); icon = base64.b64encode(buf.getvalue()).decode()

head_part, rest = body.split("<style>", 1); css, after = rest.split("</style>", 1)
doc = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Ari Draw">
<meta name="theme-color" content="#FFF5EA">
<link rel="apple-touch-icon" href="data:image/png;base64,{icon}">
{head_part}<style>body{{margin:0}}[hidden]{{display:none!important}}:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
{css}</style>
</head>
<body>
{after}
</body>
</html>'''
open(os.path.join(root, "index.html"), "w").write(doc)
print("index.html OK", round(len(doc)/1024), "KB |", ", ".join(f'{l["id"]}:{len(l["steps"])}' for l in reto))
