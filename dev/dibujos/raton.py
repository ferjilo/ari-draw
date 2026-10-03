from lib import *
from shapely.geometry import box

GREY = "#BDB6C6"; GREY_D = "#91889F"; PINK = "#F4A3B4"; BELLY = "#E8E3EE"; INK = "#2F3A56"
CHEESE = "#F7CE4A"; CHEESE_T = "#FBE08A"; CHEESE_D = "#D9A52A"; HOLE = "#D29B1F"; GROUND = "rgba(47,58,86,.13)"
WORLD = box(-50, -50, 450, 450)

HEAD = ("M206 118 C240 118 262 144 258 176 C254 204 228 214 200 210 C176 206 152 196 128 186 "
        "C118 182 116 172 126 166 C150 150 170 120 206 118 Z")
BODY = "M210 190 C258 190 292 236 293 282 C294 318 270 337 228 337 C186 337 160 318 160 284 C160 240 176 202 210 190 Z"
CH_TOP = "M134 246 L222 222 L246 246 Z"
CH_FRONT = "M134 246 L246 246 L246 284 L134 284 Z"
TAIL = "M288 306 C332 316 364 294 360 262 C356 236 326 234 328 256 C330 272 350 272 354 258"

head = poly(HEAD); body = poly(BODY)
cheese = poly(CH_TOP).union(poly(CH_FRONT))
earF = Point(236, 106).buffer(36); earB = Point(186, 102).buffer(27)
earF_in = Point(238, 108).buffer(23); earB_in = Point(188, 104).buffer(16)

out_head = WORLD.difference(head)
earF_line = clip_paths(circle_d(236, 106, 36), out_head)
earB_line = clip_paths(circle_d(186, 102, 27), out_head.difference(earF))
earF_in_line = clip_paths(circle_d(238, 108, 23), out_head)
earB_in_line = clip_paths(circle_d(188, 104, 16), out_head.difference(earF))
earF_fill = earF.difference(head); earB_fill = earB.difference(head).difference(earF)

body_keep = clip_paths(BODY, WORLD.difference(head).difference(cheese))
body_erase = clip_paths(BODY, cheese.difference(head))

ARM_L = "M172 226 C156 232 144 242 138 252"
ARM_R = "M266 226 C262 236 256 244 250 250"
belly = poly(ellipse_d(212, 300, 42, 30)).intersection(body)

holes_front = [circle_d(160, 264, 7), circle_d(196, 272, 5), circle_d(228, 260, 6.5)]
hole_top = ellipse_d(206, 238, 7, 3.2)

sh_head = crescent(head, 10, 12)
sh_body = crescent(body, 24, 8).difference(cheese)
sh_cheese = poly(CH_FRONT).intersection(poly("M206 246 L246 246 L246 284 L196 284 Z"))
sh_under_head = body.intersection(poly(ellipse_d(214, 214, 52, 14))).difference(head).difference(cheese)
ground = poly(ellipse_d(222, 342, 132, 13)).difference(body)

fur = (ticks_between(HEAD, (176, 128), (232, 120), 6, 7, head, curl=0.4) + " " +
       ticks_between(BODY, (262, 214), (293, 282), 7, 7, body, curl=0.5) + " " +
       clip_paths(chevrons([(204, 298), (220, 298), (212, 310), (196, 310), (228, 310), (212, 322)], 4, 4), belly))

steps = [
  {"say": "La cabeza del ratón: redonda por detrás y con el hocico en punta hacia la izquierda.",
   "d": [el(HEAD, fill=GREY)]},
  {"say": "Dos orejas enormes y redondas: una delante y otra un poco escondida detrás. Dentro, otro círculo.",
   "d": [el(poly_d(earB_fill), fillonly=True, fill=GREY), el(poly_d(earF_fill), fillonly=True, fill=GREY),
         el(poly_d(earB_in.difference(head).difference(earF)), fillonly=True, fill=PINK),
         el(poly_d(earF_in.difference(head)), fillonly=True, fill=PINK),
         el(earB_line), el(earF_line), el(earF_in_line + " " + earB_in_line, "mid")]},
  {"say": "El cuerpo: una pera gordita sentada, que empieza debajo de la cabeza.",
   "d": [el(BODY + "", fillonly=True, fill=GREY), el(poly_d(belly), fillonly=True, fill=BELLY),
         el(body_keep), el(body_erase, "erase")]},
  {"say": "Un trozo de queso delante de la barriga: un triángulo arriba y un rectángulo debajo. Borra la línea del cuerpo que queda dentro del queso.",
   "d": [el(CH_FRONT, fill=CHEESE), el(CH_TOP, fill=CHEESE_T)]},
  {"say": "Los agujeros del queso. Y los bracitos que lo sujetan, con las manos redondas.",
   "d": [el(" ".join(holes_front + [hole_top]), "mid", fill=HOLE),
         el(ARM_L), el(ARM_R), el(ellipse_d(134, 256, 7, 6), fill=GREY), el(ellipse_d(250, 255, 7, 6), fill=GREY)]},
  {"say": "La cara: un ojo brillante, la nariz rosa en la punta, una boquita y los bigotes largos.",
   "d": [el(ellipse_d(178, 158, 6.5, 8.5), fill=INK), el(circle_d(180, 155, 2.4), fillonly=True, fill="#FFFFFF"),
         el(circle_d(122, 174, 6.5), fill=PINK), el(ellipse_d(160, 182, 9, 6), fillonly=True, fill=PINK),
         el("M132 186 C138 192 146 192 150 188", "mid"),
         el("M134 172 C112 160 94 156 74 158 M132 178 C110 176 92 180 74 188 M136 182 C118 188 102 198 90 210", "fine")]},
  {"say": "Las patas de abajo, como dos óvalos, y una cola larga que se enrosca al final.",
   "d": [el("M148 336 C148 324 178 322 188 332 C190 340 156 343 148 336 Z", fill=GREY),
         el("M226 338 C226 326 256 324 266 334 C268 342 234 345 226 338 Z", fill=GREY),
         el(TAIL, "mid")]},
  {"say": "El pelo: rayitas cortas en la cabeza y en la espalda, y uves en la barriga.",
   "d": [el(fur, "fine")]},
  {"say": "Las sombras: rayitas en el lado derecho del ratón, en un lado del queso, debajo de la cabeza y en el suelo.",
   "d": [el(poly_d(sh_head), fillonly=True, fill=GREY_D), el(poly_d(sh_body), fillonly=True, fill=GREY_D),
         el(poly_d(sh_cheese), fillonly=True, fill=CHEESE_D), el(poly_d(sh_under_head), fillonly=True, fill=GREY_D),
         el(poly_d(ground), fillonly=True, fill=GROUND),
         el(" ".join([hatch(sh_head, sp=5.5), hatch(sh_body), hatch(sh_cheese, sp=5.5), hatch(sh_under_head, sp=5),
                      hatch(ground, ang=-20, sp=5.5)]), "fine hatch")]},
  {"say": "Por último, la línea del suelo y unas miguitas de queso.",
   "d": [el("M20 346 C120 338 300 352 384 344", "mid"),
         el("M96 350 L104 344 L106 352 Z M320 356 L326 350 L330 357 Z M80 358 L86 354 L87 360 Z", "mid", fill=CHEESE)]},
]

LESSON = {"id": "raton-r", "title": "El ratón con queso", "card": "Ratón", "what": "un ratón con su queso",
          "color": "#B83C72", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
