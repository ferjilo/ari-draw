from lib import *

OR = "#F7883A"; OR_D = "#D8642A"; WHITE = "#FFFFFF"; GREEN = "#6BBF59"; GREEN_D = "#4C9A3E"
IRIS = "#F2B632"; INK = "#2F3A56"; BUB = "#DDF2FB"; SAND = "#F3DFB1"

BODY = ("M70 200 C88 145 165 112 235 126 C275 134 298 170 318 188 L318 212 "
        "C298 230 275 266 235 274 C165 288 88 255 70 200 Z")
TAIL_EDGE = "M372 116 C364 160 364 240 372 284"
TAIL = "M318 188 C338 160 358 130 372 116 C364 160 364 240 372 284 C358 270 338 240 318 212"
DORS_OUT = "M140 129 C160 86 222 68 272 86"
DORS = DORS_OUT + " C262 103 256 117 252 131"
VENT_OUT = "M196 281 C214 313 246 325 270 319"
VENT = VENT_OUT + " C262 303 258 286 256 271"
PECT = "M150 208 C176 196 206 206 218 228 C198 242 170 236 150 208 Z"
PECT_EDGE = "M218 228 C198 242 170 236 150 208"
GILL = "M140 148 C124 180 124 226 146 256"
WEED1 = "M38 386 C26 352 52 330 42 296 C36 274 50 258 46 244 C62 258 54 282 60 302 C68 336 46 358 54 386 Z"
WEED2 = "M318 388 C312 360 334 344 330 318 C328 304 336 294 334 284 C346 296 342 312 344 324 C348 352 330 366 334 388 Z"
WEED3 = "M70 388 C66 368 80 356 76 336 C88 348 84 362 86 388 Z"
SAND_D = "M14 388 C110 378 290 398 386 386 L386 392 L14 392 Z"

body = poly(BODY); tail = poly(TAIL + " Z")
band1 = poly("M150 90 C138 160 138 240 156 310 L186 310 C172 240 172 160 184 90 Z").intersection(body)
band2 = poly("M240 90 C232 160 232 240 244 310 L268 310 C258 240 258 160 266 90 Z").intersection(body)
eye_zone = Point(115, 182).buffer(26)

def band_edges(b):
    return clip_paths(poly_d(b), body.buffer(-2.5))

def _scales():
    out = []
    for r, y in enumerate(range(138, 272, 15)):
        x0 = 96 + (9 if r % 2 else 0)
        x = x0
        while x < 330:
            out.append(f"M{x} {y} Q{x+6.5} {y+12} {x+13} {y}")
            x += 18
    return " ".join(out)
scale_d = _scales()
scales = clip_paths(scale_d, body.buffer(-5).difference(eye_zone).difference(Point(80, 200).buffer(30)))

sh_body = crescent(body, 6, 24)
sh_tail = crescent(tail, 6, 14)
sh_pect = poly(PECT).intersection(poly(ellipse_d(190, 232, 34, 12)))

steps = [
  {"say": "El cuerpo del pez: una forma como un limón tumbado, con la boca a la izquierda y más estrecho hacia la cola.",
   "d": [el(BODY, fill=OR)]},
  {"say": "La cola: un abanico grande. Dibuja rayitas que salen del centro hacia el borde.",
   "d": [el(TAIL, fill=OR), el(fan(322, 200, TAIL_EDGE, [i/9 for i in range(1, 9)], 0.93, 0.18), "fine")]},
  {"say": "Las aletas de arriba y de abajo, también con rayitas.",
   "d": [el(DORS, fill=OR), el(VENT, fill=OR),
         el(bridge(DORS_OUT, "M146 131 L254 133", [i/8 for i in range(1, 8)], 0.92), "fine"),
         el(bridge(VENT_OUT, "M202 282 L258 273", [i/6 for i in range(1, 6)], 0.92), "fine")]},
  {"say": "La aleta del costado, en medio del cuerpo, como una hoja pequeña.",
   "d": [el(PECT, fill=OR), el(fan(154, 208, PECT_EDGE, [i/5 for i in range(1, 5)], 0.88, 0.25), "fine")]},
  {"say": "El ojo grande: un círculo, dentro otro más pequeño y un puntito negro con brillo. La boca y una curva detrás del ojo.",
   "d": [el(circle_d(115, 182, 17), fill=WHITE), el(circle_d(117, 183, 10), "mid", fill=IRIS),
         el(circle_d(118, 184, 5.5), fill=INK), el(circle_d(121, 180, 2.6), fillonly=True, fill=WHITE),
         el("M70 200 C76 207 85 209 93 206 M71 198 C76 192 84 191 90 194", "mid"),
         el(GILL), el("M150 160 C138 186 138 220 154 244", "fine")]},
  {"say": "Dos franjas blancas que cruzan el cuerpo de arriba abajo, como un pez payaso.",
   "d": [el(poly_d(band1), fillonly=True, fill=WHITE), el(poly_d(band2), fillonly=True, fill=WHITE),
         el(band_edges(band1) + " " + band_edges(band2), "mid")]},
  {"say": "Las escamas: filas de curvitas pequeñas, como sonrisas, por todo el cuerpo.",
   "d": [el(scales, "fine")]},
  {"say": "Las sombras: rayitas en la parte de abajo del cuerpo y de la cola.",
   "d": [el(poly_d(sh_body.difference(band1).difference(band2)), fillonly=True, fill=OR_D),
         el(poly_d(sh_body.intersection(band1.union(band2))), fillonly=True, fill="#E4E8EF"),
         el(poly_d(sh_tail), fillonly=True, fill=OR_D), el(poly_d(sh_pect), fillonly=True, fill=OR_D),
         el(hatch(sh_body) + " " + hatch(sh_tail) + " " + hatch(sh_pect, sp=5), "fine hatch")]},
  {"say": "Para terminar, el fondo del mar: unas burbujas, algas que se mueven y la arena.",
   "d": [el(circle_d(50, 160, 8), "mid", fill=BUB), el(circle_d(38, 128, 5.5), "mid", fill=BUB),
         el(circle_d(52, 100, 3.5), "mid", fill=BUB),
         el(WEED1, fill=GREEN), el(WEED2, fill=GREEN), el(WEED3, fill=GREEN_D),
         el("M46 380 C42 350 54 330 48 300 M326 382 C324 360 338 340 336 316", "fine"),
         el(SAND_D, fillonly=True, fill=SAND), el("M14 388 C110 378 290 398 386 386", "mid")]},
]

LESSON = {"id": "pez-r", "title": "El pez payaso", "card": "Pez payaso", "what": "un pez payaso",
          "color": "#1A86C2", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
