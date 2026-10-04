from lib import *
from shapely.geometry import box

SKIN = "#F6D3B6"; SKIN_D = "#E2AE8E"; HAIR = "#B9773F"; HAIR_D = "#8C5428"
DRESS = "#EBA6D2"; DRESS_D = "#C77AAF"; DRESS_T = "#F6CBE6"; GOLD = "#F7CE4A"; GOLD_D = "#D9A52A"
GEM_A = "#7FC8F2"; GEM_B = "#F27FA6"; ROSE = "#F06B8B"; LEAF = "#6DBF4B"; SHOE = "#B05A9A"
INK = "#2F3A56"; GROUND = "rgba(47,58,86,.13)"
WORLD = box(-50, -50, 450, 450)

# ---------- formas (de delante hacia atrás) ----------
FACE = ellipse_d(200, 114, 34, 40)
FRINGE = ("M166 106 C166 82 182 68 202 68 C222 68 236 82 235 104 "
          "C226 92 214 86 204 92 C194 84 180 90 166 106 Z")
CROWN = "M176 70 L179 46 L190 59 L200 38 L210 59 L221 46 L224 70 C210 64 190 64 176 70 Z"
HAIR_OUT = ("M158 250 C146 232 154 214 142 196 C128 172 132 128 142 100 C152 72 176 56 200 56 "
            "C224 56 248 72 258 100 C268 128 272 172 258 196 C246 214 254 232 242 250 "
            "C230 238 170 238 158 250 Z")
NECK = "M190 146 L190 172 L210 172 L210 146 Z"
BODICE = "M172 170 C186 162 214 162 228 170 L223 224 C211 230 189 230 177 224 Z"
SLEEVE_L = ellipse_d(168, 180, 17, 14, -15)
SLEEVE_R = ellipse_d(232, 180, 17, 14, 15)
ARM_L = "M156 189 C146 208 150 230 180 240 L186 230 C166 222 164 208 172 194 Z"
ARM_R = "M244 189 C254 208 250 230 220 240 L214 230 C234 222 236 208 228 194 Z"
HANDS = ellipse_d(200, 236, 19, 9)
ROSE_C = circle_d(200, 220, 12)
LEAF_L = "M190 228 C178 226 172 218 172 210 C182 210 190 216 190 228 Z"
LEAF_R = "M210 228 C222 226 228 218 228 210 C218 210 210 216 210 228 Z"
SKIRT = ("M177 222 C168 262 128 302 94 344 C112 356 128 346 146 356 C164 366 182 352 200 360 "
         "C218 352 236 366 254 356 C272 346 288 356 306 344 C272 302 232 262 223 222 "
         "C211 230 189 230 177 222 Z")
SHOE_L = ellipse_d(178, 362, 13, 7); SHOE_R = ellipse_d(222, 362, 13, 7)

face = poly(FACE); fringe = poly(FRINGE); crown = poly(CROWN); hair = poly(HAIR_OUT).union(fringe)
neck = poly(NECK); bodice = poly(BODICE); sl_l = poly(SLEEVE_L); sl_r = poly(SLEEVE_R)
arm_l = poly(ARM_L); arm_r = poly(ARM_R); hands = poly(HANDS); rose = poly(ROSE_C)
leaf_l = poly(LEAF_L); leaf_r = poly(LEAF_R); skirt = poly(SKIRT)
shoe_l = poly(SHOE_L); shoe_r = poly(SHOE_R)

front_flower = rose.union(leaf_l).union(leaf_r)
front_arms = arm_l.union(arm_r).union(hands).union(front_flower)
front_top = sl_l.union(sl_r)

def vis(d, *front):
    """Parte visible de un contorno: lo que no tapan las formas de delante."""
    g = WORLD
    for s in front: g = g.difference(s)
    return clip_paths(d, g)

# Líneas visibles de cada pieza
face_line = vis(FACE, fringe)
fringe_line = vis(FRINGE, crown)
hair_line = vis(HAIR_OUT, face, fringe, crown, neck, bodice, front_top, front_arms, skirt)
neck_line = vis(NECK, face, bodice)
bodice_line = vis(BODICE, front_top, front_arms)
sleeve_line = SLEEVE_L + " " + SLEEVE_R
arms_line = vis(ARM_L, hands, front_flower) + " " + vis(ARM_R, hands, front_flower)
hands_line = vis(HANDS, front_flower)
skirt_line = vis(SKIRT, bodice, front_arms)
shoes_line = vis(SHOE_L, skirt) + " " + vis(SHOE_R, skirt)

# Rellenos (solo lo visible de cada pieza, para que no se pisen)
hair_fill = hair.difference(face.difference(fringe)).difference(crown)
face_fill = face.difference(fringe)
neck_fill = neck.difference(face)
bodice_fill = bodice.difference(front_top)
skirt_fill = skirt.difference(bodice)
shoe_fill = shoe_l.union(shoe_r).difference(skirt)

# ---------- texturas ----------
hair_strands = clip_paths(
    "M150 110 C144 150 150 180 152 210 M160 98 C154 140 162 176 160 214 M250 110 C256 150 250 180 248 210 "
    "M240 98 C246 140 238 176 240 214 M148 200 C156 214 150 228 160 240 M252 200 C244 214 250 228 240 240 "
    "M182 80 C188 74 196 72 204 74 M212 78 C220 82 226 88 230 96",
    hair_fill)
skirt_folds = clip_paths(
    "M188 232 C182 270 160 316 146 354 M200 234 C200 280 200 320 200 358 M212 232 C218 270 240 316 254 354 "
    "M182 230 C170 262 136 312 118 348 M218 230 C230 262 264 312 282 348",
    skirt_fill.difference(front_arms))
stars = [(150, 330), (176, 300), (226, 300), (250, 330), (200, 322), (166, 344), (234, 344)]
skirt_dots = " ".join(circle_d(x, y, 2.6) for x, y in stars)
lace = clip_paths(scallops(200, 172, 8, 6, 3.2), bodice) + " " + \
       clip_paths(scallops(200, 351, 13, 16, 3.5), skirt)
sleeve_puff = ("M160 172 C162 182 162 188 158 192 M170 168 C174 178 174 186 172 192 "
               "M240 172 C238 182 238 188 242 192 M230 168 C226 178 226 186 228 192")
belt = clip_paths("M177 222 C189 228 211 228 223 222", WORLD.difference(front_arms))
rose_spiral = "M200 220 C204 216 208 222 202 226 C194 228 192 216 200 212 C210 208 214 222 206 230"

# ---------- sombras (luz arriba a la izquierda) ----------
sh_neck = neck_fill.intersection(poly("M190 146 L210 146 L210 162 L190 156 Z"))
sh_hair = crescent(hair_fill, 12, 6).difference(front_arms)
sh_skirt = crescent(skirt_fill.difference(front_arms), 34, 6)
sh_under_bodice = skirt_fill.intersection(poly(ellipse_d(200, 232, 30, 9))).difference(front_arms)
sh_bodice = crescent(bodice_fill.difference(front_arms), 10, 4)
ground = poly(ellipse_d(200, 364, 128, 12)).difference(skirt).difference(shoe_l).difference(shoe_r)

sparkles = " ".join(f"M{x} {y-9} L{x} {y+9} M{x-9} {y} L{x+9} {y}" for x, y in [(70, 90), (334, 70), (342, 210), (58, 240)])

steps = [
  {"say": "La cara de la princesa: un óvalo, un poco más alto que ancho.",
   "d": [el(poly_d(face_fill), fillonly=True, fill=SKIN), el(face_line)]},
  {"say": "El pelo, largo y ondulado. Empieza encima de la cabeza y baja por los dos lados hasta los hombros. Y un flequillo que tapa un poco la frente.",
   "d": [el(poly_d(hair_fill), fillonly=True, fill=HAIR), el(hair_line), el(fringe_line)]},
  {"say": "La corona: tres picos, el del medio más alto. Pon una piedra preciosa en cada pico.",
   "d": [el(CROWN, fill=GOLD),
         el(circle_d(200, 54, 4), "mid", fill=GEM_B), el(circle_d(185, 62, 3), "mid", fill=GEM_A),
         el(circle_d(215, 62, 3), "mid", fill=GEM_A)]},
  {"say": "El cuello y la parte de arriba del vestido. A los lados, dos mangas redondas como globos.",
   "d": [el(poly_d(neck_fill), fillonly=True, fill=SKIN), el(neck_line),
         el(poly_d(bodice_fill), fillonly=True, fill=DRESS), el(bodice_line),
         el(SLEEVE_L, fill=DRESS_T), el(SLEEVE_R, fill=DRESS_T)]},
  {"say": "Los brazos bajan y se juntan delante. Las manos sujetan una rosa con dos hojas.",
   "d": [el(ARM_L + " " + ARM_R, fillonly=True, fill=SKIN), el(arms_line),
         el(poly_d(hands.difference(front_flower)), fillonly=True, fill=SKIN), el(hands_line),
         el(LEAF_L, fill=LEAF), el(LEAF_R, fill=LEAF), el(ROSE_C, fill=ROSE)]},
  {"say": "La falda: muy grande, con forma de campana y el borde de abajo ondulado. Debajo asoman los zapatos.",
   "d": [el(poly_d(skirt_fill), fillonly=True, fill=DRESS), el(skirt_line),
         el(poly_d(shoe_fill), fillonly=True, fill=SHOE), el(shoes_line, "mid")]},
  {"say": "La cara: dos ojos grandes con pestañas, las cejas, una naricita, una sonrisa y las mejillas.",
   "d": [el(ellipse_d(186, 116, 6, 7.5), fill=INK), el(ellipse_d(214, 116, 6, 7.5), fill=INK),
         el(circle_d(188, 113, 2.2) + " " + circle_d(216, 113, 2.2), fillonly=True, fill="#FFFFFF"),
         el("M178 110 L174 106 M181 107 L179 102 M222 110 L226 106 M219 107 L221 102", "fine"),
         el("M178 101 C183 97 190 97 194 99 M206 99 C210 97 217 97 222 101", "mid"),
         el("M199 124 C198 128 200 130 203 129", "mid"),
         el("M190 136 C195 142 205 142 210 136", "mid", fill="#E8707F"),
         el(circle_d(178, 130, 6) + " " + circle_d(222, 130, 6), fillonly=True, fill="#F4A3B4")]},
  {"say": "Los detalles: mechones en el pelo, la espiral de la rosa, pliegues en la falda, puntillas en los bordes y unos puntitos brillantes.",
   "d": [el(hair_strands + " " + rose_spiral + " " + sleeve_puff, "fine"),
         el(belt, "mid"),
         el(skirt_folds + " " + lace + " " + skirt_dots, "fine")]},
  {"say": "Las sombras: rayitas en el lado derecho del pelo y de la falda, en el cuello y debajo de la cintura.",
   "d": [el(poly_d(sh_hair), fillonly=True, fill=HAIR_D), el(poly_d(sh_neck), fillonly=True, fill=SKIN_D), el(poly_d(sh_skirt), fillonly=True, fill=DRESS_D),
         el(poly_d(sh_under_bodice), fillonly=True, fill=DRESS_D), el(poly_d(sh_bodice), fillonly=True, fill=DRESS_D),
         el(" ".join([hatch(sh_hair, sp=6), hatch(sh_neck, sp=4.5), hatch(sh_skirt),
                      hatch(sh_under_bodice, sp=5), hatch(sh_bodice, sp=5)]), "fine hatch")]},
  {"say": "Por último, la sombra en el suelo y unas estrellitas que brillan alrededor.",
   "d": [el(poly_d(ground), fillonly=True, fill=GROUND), el(hatch(ground, ang=-20, sp=5.5), "fine hatch"),
         el(sparkles, "mid")]},
]

LESSON = {"id": "princesa-r", "title": "La princesa con la rosa", "card": "Princesa", "what": "una princesa con su rosa",
          "color": "#8E5BC9", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
