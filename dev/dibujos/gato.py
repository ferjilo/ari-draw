from lib import *

ORANGE = "#F4A65B"; ORANGE_D = "#D97C34"; CREAM = "#FCE3BE"; PINK = "#F4A3B4"
EYE = "#B9DB6A"; INK = "#2F3A56"; GROUND = "rgba(47,58,86,.13)"

HEAD = ("M200 62 C245 62 272 88 274 118 C276 140 268 150 282 163 L262 165 "
        "C252 179 230 187 200 187 C170 187 148 179 138 165 L118 163 C132 150 124 140 126 118 "
        "C128 88 155 62 200 62 Z")
EAR_L = "M141 92 C132 66 126 44 128 26 C148 35 168 50 185 67"
EAR_R = "M259 92 C268 66 274 44 272 26 C252 35 232 50 215 67"
EAR_IN_L = "M147 80 C141 64 138 50 139 40 C152 48 163 57 171 65"
EAR_IN_R = "M253 80 C259 64 262 50 261 40 C248 48 237 57 229 65"
BODY = ("M158 180 C128 206 112 250 116 295 C118 322 140 337 200 337 "
        "C260 337 282 322 284 295 C288 250 272 206 242 180")
BODY_CLOSED = BODY + " Z"
LEG_L = "M171 234 C166 274 161 304 159 327 C151 343 192 348 193 331 C195 300 197 272 199 246"
LEG_R = "M229 234 C234 274 239 304 241 327 C249 343 208 348 207 331 C205 300 203 272 201 246"
TAIL_OUT = "M282 318 C338 318 362 280 346 240 C338 220 312 220 310 236"
TAIL_IN = "M310 236 C322 262 314 288 284 298"
TAIL = TAIL_OUT + " C322 262 314 288 284 298"
EYE_L = "M157 112 C167 97 186 97 193 112 C184 125 166 125 157 112 Z"
EYE_R = "M243 112 C233 97 214 97 207 112 C216 125 234 125 243 112 Z"

head = poly(HEAD); body = poly(BODY_CLOSED); tail = poly(TAIL + " Z")
legs = poly(LEG_L + " Z").union(poly(LEG_R + " Z"))
earL = poly(EAR_L + " Z"); earR = poly(EAR_R + " Z")

# sombras (luz desde arriba a la izquierda)
sh_head = crescent(head, 16, 12)
sh_body = crescent(body, 26, 6).difference(legs)
sh_neck = body.intersection(poly(ellipse_d(200, 192, 62, 18))).difference(head)
sh_tail = crescent(tail, 9, 9)
sh_ears = crescent(earR, 8, 6).difference(head)
ground = poly(ellipse_d(222, 342, 128, 15)).difference(body).difference(legs).difference(tail)
sh_legs = poly(LEG_L + " Z").intersection(poly(ellipse_d(196, 250, 30, 26)))

chest_pts = [(200 + dx, y) for y, row in [(205, [-14, 0, 14]), (220, [-21, -7, 7, 21]), (236, [-14, 0, 14]),
                                           (252, [-7, 7]), (266, [0])] for dx in row]

steps = [
  {"say": "Empezamos por la cabeza: un círculo un poco aplastado, con dos picos de pelo en las mejillas.",
   "d": [el(HEAD, fill=ORANGE)]},
  {"say": "Las orejas: dos triángulos con la punta redondeada. Dentro, otra línea más pequeña.",
   "d": [el(EAR_L, fill=ORANGE), el(EAR_R, fill=ORANGE),
         el(EAR_IN_L + " Z", fillonly=True, fill=PINK), el(EAR_IN_R + " Z", fillonly=True, fill=PINK),
         el(EAR_IN_L, "mid"), el(EAR_IN_R, "mid")]},
  {"say": "El cuerpo: baja dos curvas desde la cabeza, como una pera grande sentada.",
   "d": [el(BODY, fill=ORANGE)]},
  {"say": "Las patas de delante: dos líneas largas hasta abajo, con las patitas redondas. Y unas rayitas para los dedos.",
   "d": [el(LEG_L + " Z", fillonly=True, fill=ORANGE), el(LEG_R + " Z", fillonly=True, fill=ORANGE),
         el(LEG_L), el(LEG_R),
         el("M168 336 L169 342 M178 338 L178 344 M232 336 L231 342 M222 338 L222 344", "mid")]},
  {"say": "La cola: sale del cuerpo y se enrosca hacia arriba por el lado derecho.",
   "d": [el(TAIL, fill=ORANGE)]},
  {"say": "La cara: dos ojos como almendras, con la pupila larga y un brillo. La nariz, la boca y los bigotes.",
   "d": [el(ellipse_d(200, 150, 30, 19), fillonly=True, fill=CREAM),
         el(EYE_L, fill=EYE), el(EYE_R, fill=EYE),
         el(ellipse_d(175, 111, 4, 10), fill=INK), el(ellipse_d(225, 111, 4, 10), fill=INK),
         el(circle_d(180, 106, 3), fillonly=True, fill="#FFFFFF"), el(circle_d(230, 106, 3), fillonly=True, fill="#FFFFFF"),
         el("M192 136 C196 131 204 131 208 136 C206 142 202 145 200 146 C198 145 194 142 192 136 Z", fill=PINK),
         el("M200 146 L200 152 M200 152 C196 160 186 160 182 154 M200 152 C204 160 214 160 218 154", "mid"),
         el("M168 146 C140 140 120 140 96 146 M168 153 C140 153 118 157 98 166 "
            "M232 146 C260 140 280 140 304 146 M232 153 C260 153 282 157 302 166", "fine")]},
  {"say": "Ahora las rayas de gato atigrado: en la frente, en las mejillas, en el cuerpo y en la cola.",
   "d": [el(ellipse_d(200, 262, 30, 52), fillonly=True, fill=CREAM),
         el("M186 72 C188 82 190 90 190 97 M200 66 L200 93 M214 72 C212 82 210 90 210 97 "
            "M127 121 C140 123 148 128 152 134 M126 138 C136 138 144 142 148 147 "
            "M273 121 C260 123 252 128 248 134 M274 138 C264 138 256 142 252 147 "
            "M121 248 C134 250 144 257 150 265 M117 278 C130 279 140 285 146 294 "
            "M279 248 C266 250 256 257 250 265 M283 278 C270 279 260 285 254 294", "mid"),
         el(bridge(TAIL_OUT, TAIL_IN, [0.32, 0.5, 0.66], frac=0.55, rev_inner=True), "mid")]},
  {"say": "El pelo: rayitas cortas en el borde de las mejillas y uves en el pecho, como un abrigo suave.",
   "d": [el(ticks_between(HEAD, (274,126), (279,159), 5, 8, head, curl=0.5) + " " + ticks_between(HEAD, (126,126), (121,159), 5, 8, head, curl=-0.5) + " " + ticks_between(HEAD, (180,186), (220,186), 5, 6, head, curl=0.3) + " " +
            ticks(BODY, 0.12, 0.3, 5, 6, body, curl=0.6) + " " + ticks(BODY, 0.7, 0.88, 5, 6, body, curl=-0.6) + " " +
            chevrons(chest_pts, 4, 5), "fine")]},
  {"say": "Por último, las sombras: rayitas inclinadas en el lado derecho, donde no da la luz, y una sombra en el suelo.",
   "d": [el(poly_d(sh_head), fillonly=True, fill=ORANGE_D), el(poly_d(sh_body), fillonly=True, fill=ORANGE_D),
         el(poly_d(sh_tail), fillonly=True, fill=ORANGE_D), el(poly_d(sh_neck), fillonly=True, fill=ORANGE_D),
         el(poly_d(ground), fillonly=True, fill=GROUND),
         el(" ".join([hatch(sh_head), hatch(sh_body), hatch(sh_tail), hatch(sh_neck, sp=5.5),
                      hatch(sh_ears, sp=5), hatch(sh_legs, sp=5.5), hatch(ground, ang=-20, sp=5.5)]), "fine hatch")]},
]

LESSON = {"id": "gato-r", "title": "El gato sentado", "card": "Gato", "what": "un gato sentado",
          "color": "#D9622B", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
