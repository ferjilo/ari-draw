from lib import *
import math

SHELL = "#86C25A"; SHELL_L = "#A9D67E"; SHELL_D = "#5C9A3A"; RIM_C = "#6EAB47"
SKIN = "#D3D68A"; SKIN_D = "#A8AE5C"; INK = "#2F3A56"; GROUND = "rgba(47,58,86,.13)"; GRASS = "#7DBE55"

DOME = "M92 248 C96 168 150 122 214 122 C280 122 328 168 330 248"
DOME_C = DOME + " Z"
RIM = "M86 246 C150 264 270 264 336 246 L340 258 C272 279 150 279 82 258 Z"
NECKHEAD = ("M316 214 C334 204 342 196 350 186 C356 168 384 164 394 180 C402 194 396 214 376 218 "
            "C366 220 356 216 352 210 C348 228 340 242 326 248")
FL = "M288 262 C292 284 290 302 284 316 C296 323 316 323 321 315 C318 298 316 280 317 262"
BL = "M112 262 C106 282 100 300 94 314 C106 322 126 322 132 314 C131 296 132 280 134 266"
TAIL = "M86 248 C70 250 58 256 48 266 C64 266 78 262 90 258"

dome = poly(DOME_C); rim = poly(RIM)
skin = poly(NECKHEAD + " Z").union(poly(FL + " Z")).union(poly(BL + " Z")).union(poly(TAIL + " Z"))

def hexagon(cx, cy, r, rot=0):
    pts = [(cx + r*math.cos(math.radians(60*i+rot)), cy + r*math.sin(math.radians(60*i+rot))*0.82) for i in range(6)]
    return Polygon(pts)

inner = dome.buffer(-3)
hexes = [hexagon(152, 190, 36, 30), hexagon(214, 190, 36, 30), hexagon(276, 190, 36, 30)]
plates = [h.intersection(inner) for h in hexes]
def outline(g): return lines_d([LineString(list(g.exterior.coords))])
plate_lines = " ".join(outline(p) for p in plates)
# divisiones desde las placas hasta el borde
div = ("M214 160 L214 118 M152 160 L138 136 M276 160 L290 136 M183 175 L174 124 M245 175 L254 124 "
       "M121 175 L100 186 M121 205 L95 228 M307 175 L326 186 M307 205 L331 228 "
       "M152 219 L150 254 M214 219 L214 256 M276 219 L278 254 M183 205 L184 256 M245 205 L244 256")
div = clip_paths(div, inner)
rings = " ".join(outline(p.buffer(-8)) + " " + outline(p.buffer(-15)) for p in plates if not p.buffer(-15).is_empty)
rim_div = " ".join(f"M{x} {y0} L{x+(-2 if x<210 else 2)} {y0+12}" for x, y0 in
                   [(112, 254), (142, 260), (176, 263), (210, 264), (244, 263), (278, 260), (308, 254)])

neck_wr = clip_paths("M326 210 C332 222 336 234 334 244 M338 202 C344 214 346 226 344 236", poly(NECKHEAD + " Z").buffer(-2))
leg_sc = clip_paths(" ".join(scallops(cx, y, 8, 3, 3) for cx in (120, 304) for y in (274, 288, 300)), skin.buffer(-3))

sh_dome = crescent(dome, 26, 3).difference(rim)
sh_rim = rim.intersection(poly(ellipse_d(260, 276, 90, 14)))
sh_skin = crescent(skin, 6, 8)
ground = poly(ellipse_d(216, 322, 150, 12)).difference(poly(FL + " Z")).difference(poly(BL + " Z"))
under = poly("M92 258 L330 258 L320 300 L102 300 Z").intersection(poly(ellipse_d(212, 266, 120, 10))).difference(rim).difference(skin)

steps = [
  {"say": "El caparazón: una cúpula grande, como medio balón, más alta por el centro.",
   "d": [el("M90 240 L332 240 L334 247 C270 266 150 266 88 247 Z", fillonly=True, fill=SHELL), el(DOME, fill=SHELL)]},
  {"say": "Debajo, el borde del caparazón: una banda curva. Divídela en trocitos con rayas pequeñas.",
   "d": [el(RIM, fill=RIM_C), el(rim_div, "mid")]},
  {"say": "Las placas del caparazón: tres hexágonos en el centro, y rayas que bajan hasta el borde.",
   "d": [el(" ".join(poly_d(p) for p in plates), fillonly=True, fill=SHELL_L), el(plate_lines), el(div, "mid")]},
  {"say": "Dentro de cada placa, dos anillos más pequeños, como los de un árbol.",
   "d": [el(rings, "fine")]},
  {"say": "El cuello y la cabeza: salen por la derecha. La cabeza es redonda, como una pelota pequeña.",
   "d": [el(NECKHEAD, fill=SKIN)]},
  {"say": "Las patas, gorditas como columnas, con tres uñas cada una. Y una colita en punta detrás.",
   "d": [el(FL, fill=SKIN), el(BL, fill=SKIN), el(TAIL, fill=SKIN),
         el("M289 320 l-3 5 M299 322 l-1 6 M310 321 l1 5 M98 318 l-3 5 M108 320 l-1 6 M119 319 l1 5", "mid")]},
  {"say": "La cara: un ojo con brillo, una sonrisa y la nariz. Arrugas en el cuello y escamas en las patas.",
   "d": [el(circle_d(379, 186, 5.5), fill=INK), el(circle_d(381, 184, 1.8), fillonly=True, fill="#FFFFFF"),
         el("M380 205 C387 208 393 206 397 200", "mid"), el(circle_d(396, 186, 1.2), "fine", fill=INK),
         el(neck_wr + " " + leg_sc, "fine")]},
  {"say": "Las sombras: rayitas a la derecha del caparazón, debajo del borde y en el suelo.",
   "d": [el(poly_d(sh_dome), fillonly=True, fill=SHELL_D), el(poly_d(sh_rim), fillonly=True, fill=SHELL_D),
         el(poly_d(sh_skin), fillonly=True, fill=SKIN_D), el(poly_d(under), fillonly=True, fill="rgba(47,58,86,.25)"),
         el(poly_d(ground), fillonly=True, fill=GROUND),
         el(" ".join([hatch(sh_dome), hatch(sh_rim, sp=5), hatch(sh_skin, sp=5), hatch(under, sp=5),
                      hatch(ground, ang=-20, sp=5.5)]), "fine hatch")]},
  {"say": "Por último, el suelo: una línea, unas matas de hierba y algunas piedras.",
   "d": [el("M14 324 C100 318 300 330 386 322", "mid"),
         el("M30 322 L36 302 L40 320 L46 296 L50 321 L56 306 L60 323 "
            "M344 322 L350 304 L354 321 L360 298 L364 322 L370 308 L374 323", "mid", fill=GRASS),
         el(ellipse_d(196, 340, 12, 6), "mid", fill="#C9CED8"), el(ellipse_d(220, 344, 7, 4), "mid", fill="#C9CED8"),
         el(ellipse_d(70, 342, 9, 5), "mid", fill="#C9CED8")]},
]

LESSON = {"id": "tortuga-r", "title": "La tortuga paseando", "card": "Tortuga", "what": "una tortuga paseando",
          "color": "#2E8B3A", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
