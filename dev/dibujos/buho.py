from lib import *
import math
from shapely.geometry import box
WORLD = box(-50, -50, 450, 450)

BR = "#B4835C"; BR_D = "#875B3B"; DISC = "#F3E3CB"; BELLY = "#EBD3AE"; WING = "#99694A"
IRIS = "#F7C948"; BEAK = "#F2A93B"; INK = "#2F3A56"; BARK = "#9C6B48"; BARK_D = "#764E33"
LEAF = "#7DBE55"; MOON = "#FFF1B8"

BODY = "M200 70 C262 70 292 130 292 200 C292 272 252 318 200 318 C148 318 108 272 108 200 C108 130 138 70 200 70 Z"
TUFT_L = "M136 112 C126 90 120 68 117 48 C136 58 152 72 163 86"
TUFT_R = "M264 112 C274 90 280 68 283 48 C264 58 248 72 237 86"
DISC_D = "M200 104 C226 84 270 92 271 140 C272 178 244 198 200 202 C156 198 128 178 129 140 C130 92 174 84 200 104 Z"
WING_L = "M118 168 C94 202 96 264 132 304 C146 282 154 240 150 198 C146 180 134 170 118 168 Z"
WING_R = "M282 168 C306 202 304 264 268 304 C254 282 246 240 250 198 C254 180 266 170 282 168 Z"
BRANCH = "M14 322 C120 314 280 330 386 320 L386 346 C280 356 120 342 14 350 Z"
LEAF_R = "M346 322 C352 298 372 290 388 292 C384 312 366 324 346 322 Z"
LEAF_R2 = "M330 324 C326 304 334 286 344 278 C352 294 346 314 330 324 Z"
LEAF_L = "M58 318 C46 298 28 292 12 296 C20 314 38 322 58 318 Z"

body = poly(BODY); disc = poly(DISC_D); wingL = poly(WING_L); wingR = poly(WING_R)
belly = Point(200, 252).buffer(60).intersection(body).difference(wingL).difference(wingR).difference(disc)
branch = poly(BRANCH)

def radial(cx, cy, r0, r1, n, region):
    out = []
    for i in range(n):
        a = 2*math.pi*i/n
        out.append(f"M{f(cx+r0*math.cos(a))} {f(cy+r0*math.sin(a))} L{f(cx+r1*math.cos(a))} {f(cy+r1*math.sin(a))}")
    return clip_paths(" ".join(out), region)

eye_feathers = radial(164, 142, 31, 40, 26, disc.buffer(-3)) + " " + radial(236, 142, 31, 40, 26, disc.buffer(-3))

def wing_feathers(wing, x0, x1):
    rows = []
    for r, y in enumerate(range(190, 300, 14)):
        rows.append(scallops((x0+x1)/2 + (5 if r % 2 else 0), y, 10, 7, 4))
    return clip_paths(" ".join(rows), wing.buffer(-3))

belly_pts = []
for r, y in enumerate(range(212, 304, 13)):
    for x in range(146 + (8 if r % 2 else 0), 256, 16):
        belly_pts.append((x, y))
belly_ch = clip_paths(chevrons(belly_pts, 4.5, 4), belly.buffer(-3))

bark = clip_paths("M30 330 C90 326 140 334 200 332 M60 340 C120 336 200 344 260 340 M220 328 C270 330 320 334 370 328 "
                  "M290 340 C320 342 350 340 378 336", branch.buffer(-3))

TOES = ("M170 312 C164 318 164 326 168 330 M178 314 C176 322 177 330 180 334 M188 312 C190 320 189 328 185 332 "
        "M212 312 C210 320 211 328 215 332 M222 314 C224 322 223 330 220 334 M230 312 C236 318 236 326 232 330")

sh_body = crescent(body, 22, 10).difference(wingR).difference(disc)
sh_neck = body.intersection(poly(ellipse_d(200, 206, 70, 18))).difference(disc).difference(wingL).difference(wingR)
sh_wings = crescent(wingL, 7, 8).union(crescent(wingR, 9, 8))
sh_branch = branch.difference(affinity.translate(branch, 0, -10))
sh_on_branch = branch.intersection(poly(ellipse_d(204, 326, 80, 9)))

steps = [
  {"say": "El cuerpo del búho: un óvalo grande, como un huevo de pie.",
   "d": [el(BODY, fillonly=True, fill=BR), el(clip_paths(BODY, WORLD.difference(wingL).difference(wingR))),
         el(clip_paths(BODY, wingL.union(wingR)), "erase")]},
  {"say": "Arriba, dos plumas de las orejas en punta, una a cada lado.",
   "d": [el(TUFT_L, fill=BR), el(TUFT_R, fill=BR),
         el("M132 98 C128 82 124 68 122 58 M268 98 C272 82 276 68 278 58", "fine")]},
  {"say": "La cara: una forma de corazón grande en la parte de arriba del cuerpo.",
   "d": [el(DISC_D, fill=DISC)]},
  {"say": "Los ojos, muy grandes y redondos. Dentro, la pupila negra con dos brillos.",
   "d": [el(circle_d(164, 142, 25), fill=IRIS), el(circle_d(236, 142, 25), fill=IRIS),
         el(circle_d(166, 144, 12), fill=INK), el(circle_d(234, 144, 12), fill=INK),
         el(circle_d(170, 139, 4.5), fillonly=True, fill="#FFFFFF"), el(circle_d(238, 139, 4.5), fillonly=True, fill="#FFFFFF"),
         el(circle_d(162, 149, 2), fillonly=True, fill="#FFFFFF"), el(circle_d(230, 149, 2), fillonly=True, fill="#FFFFFF")]},
  {"say": "El pico, un triángulo pequeño hacia abajo. Y alrededor de cada ojo, rayitas como los rayos del sol.",
   "d": [el("M189 162 C194 156 206 156 211 162 L200 186 Z", fill=BEAK), el(eye_feathers, "fine")]},
  {"say": "Las alas a los lados del cuerpo. Borra la línea del cuerpo que queda dentro de las alas, y dibuja filas de plumas como escamas.",
   "d": [el(WING_L, fill=WING), el(WING_R, fill=WING),
         el(scale_grid(wingL.buffer(-3), 96, 156, 186, 304, 9, 13, 7, 12) + " " + scale_grid(wingR.buffer(-3), 244, 306, 186, 304, 9, 13, 7, 12), "fine")]},
  {"say": "La barriga: llénala de uves pequeñas, en filas, para que parezcan plumas.",
   "d": [el(poly_d(belly), fillonly=True, fill=BELLY), el(belly_ch, "fine")]},
  {"say": "La rama donde está sentado, con rayas en la corteza. Y las patas agarradas a la rama.",
   "d": [el(BRANCH, fill=BARK), el(bark, "fine"), el(ellipse_d(96, 336, 9, 5), "fine", fill=BARK_D),
         el(TOES, "mid")]},
  {"say": "Las sombras: rayitas en el lado derecho del búho, debajo de la cara y en la parte de abajo de la rama.",
   "d": [el(poly_d(sh_body), fillonly=True, fill=BR_D), el(poly_d(sh_neck), fillonly=True, fill=BR_D),
         el(poly_d(sh_wings), fillonly=True, fill="#7A5236"), el(poly_d(sh_branch), fillonly=True, fill=BARK_D),
         el(poly_d(sh_on_branch), fillonly=True, fill=BARK_D),
         el(" ".join([hatch(sh_body), hatch(sh_neck, sp=5.5), hatch(sh_wings, sp=5.5), hatch(sh_branch, ang=-25, sp=5),
                      hatch(sh_on_branch, ang=-25, sp=5)]), "fine hatch")]},
  {"say": "Para terminar, la noche: una luna, unas estrellas y unas hojas en la rama.",
   "d": [el("M352 40 C334 44 324 62 330 80 C336 98 356 104 372 96 C356 94 344 82 344 66 C344 54 348 46 352 40 Z", fill=MOON),
         el("M60 60 L60 76 M52 68 L68 68 M90 100 L90 110 M85 105 L95 105 M300 120 L300 130 M295 125 L305 125", "mid"),
         el(LEAF_R, fill=LEAF), el(LEAF_R2, fill=LEAF), el(LEAF_L, fill=LEAF),
         el("M348 321 C360 306 372 298 386 294 M332 322 C336 306 340 292 344 282 M56 317 C44 306 30 299 14 297", "fine")]},
]

LESSON = {"id": "buho-r", "title": "El búho en la rama", "card": "Búho", "what": "un búho en una rama",
          "color": "#8A5A3C", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
