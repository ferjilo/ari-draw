from lib import *
from shapely.geometry import box, LineString
import math

SKIN = "#F6D3B6"; SKIN_D = "#E2AE8E"; HAIR = "#E07A3F"; HAIR_D = "#B4552A"
DRESS = "#F8D66A"; DRESS_D = "#DDB043"; DRESS_T = "#FBE8A6"; GOLD = "#F2B33D"
STAR = "#F59AC0"; STICK = "#FFF6FB"; SHOE = "#D97BA6"; FRECK = "#C9825A"
INK = "#2F3A56"; GROUND = "rgba(47,58,86,.13)"
WORLD = box(-50, -50, 450, 450)

def star_d(cx, cy, R_, r, rot=-90):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36); rr = R_ if i % 2 == 0 else r
        pts.append(f"{f(cx + rr*math.cos(a))} {f(cy + rr*math.sin(a))}")
    return "M" + " L".join(pts) + " Z"

# ---------- formas ----------
FACE = ellipse_d(190, 128, 33, 38)
FRINGE = ("M158 120 C158 96 172 84 192 84 C212 84 224 96 223 116 "
          "C214 104 202 98 192 104 C184 98 168 104 158 120 Z")
HAIR_OUT = ("M154 166 C144 150 144 120 150 104 C158 82 174 74 190 74 C206 74 222 82 230 104 "
            "C236 120 236 150 226 166 C222 158 218 152 212 150 L168 150 C162 152 158 158 154 166 Z")
BUN_L = circle_d(158, 82, 20); BUN_R = circle_d(222, 82, 20)
TIARA = "M170 82 C182 74 198 74 210 82 L207 88 C197 81 183 81 173 88 Z"
TSTAR = star_d(190, 70, 11, 4.8)
NECK = "M182 162 L182 184 L198 184 L198 162 Z"
BODICE = "M164 182 C178 174 202 174 216 182 L211 236 C199 242 181 242 169 236 Z"
SLEEVE_L = ellipse_d(160, 192, 16, 13, -15); SLEEVE_R = ellipse_d(220, 192, 16, 13, 15)
ARM_L = "M147 200 C137 220 139 242 148 262 L158 258 C150 240 150 222 156 206 Z"
ARM_R = "M226 198 C242 184 252 166 258 148 L269 152 C264 172 252 194 234 210 Z"
HAND_L = circle_d(153, 266, 8.5); HAND_R = circle_d(264, 142, 9)
WSTAR = star_d(294, 64, 23, 10, -84)
SKIRT = ("M169 234 C160 270 134 312 114 352 C150 364 230 364 266 352 "
         "C246 312 220 270 211 234 C199 242 181 242 169 236 Z")
SHOE_L = ellipse_d(174, 366, 13, 7); SHOE_R = ellipse_d(206, 366, 13, 7)

face = poly(FACE); fringe = poly(FRINGE); hair = poly(HAIR_OUT).union(fringe)
bun_l = poly(BUN_L); bun_r = poly(BUN_R); tiara = poly(TIARA).union(poly(TSTAR))
neck = poly(NECK); bodice = poly(BODICE); sleeves = poly(SLEEVE_L).union(poly(SLEEVE_R))
arm_l = poly(ARM_L); arm_r = poly(ARM_R); hand_l = poly(HAND_L); hand_r = poly(HAND_R)
wstar = poly(WSTAR); skirt = poly(SKIRT); shoe_l = poly(SHOE_L); shoe_r = poly(SHOE_R)
stick = LineString([(258, 154), (288, 82)]).buffer(3.2)
STICK_D = poly_d(stick)

def vis(d, *front):
    g = WORLD
    for s in front: g = g.difference(s)
    return clip_paths(d, g)

# Líneas visibles
face_line = vis(FACE, fringe, tiara)
fringe_line = vis(FRINGE, tiara)
hair_line = vis(HAIR_OUT, face, fringe, tiara, neck)
buns_line = vis(BUN_L, hair, tiara) + " " + vis(BUN_R, hair, tiara)
tiara_line = vis(TIARA, poly(TSTAR))
neck_line = vis(NECK, face, bodice)
bodice_line = vis(BODICE, sleeves)
arms_line = vis(ARM_L, sleeves, hand_l) + " " + vis(ARM_R, sleeves, hand_r)
stick_line = vis(STICK_D, hand_r, wstar)
skirt_line = vis(SKIRT, bodice, hand_l)
shoes_line = vis(SHOE_L, skirt) + " " + vis(SHOE_R, skirt)

# Rellenos visibles
bun_fill = bun_l.union(bun_r).difference(hair).difference(tiara)
hair_fill = hair.difference(face.difference(fringe)).difference(tiara)
face_fill = face.difference(fringe).difference(tiara)
neck_fill = neck.difference(face)
bodice_fill = bodice.difference(sleeves)
arm_fill = arm_l.union(arm_r).difference(sleeves)
stick_fill = stick.difference(hand_r).difference(wstar)
skirt_fill = skirt.difference(bodice)
shoe_fill = shoe_l.union(shoe_r).difference(skirt)

# ---------- texturas ----------
bun_spirals = ("M158 82 C162 78 166 84 160 88 C152 90 150 78 158 74 C168 70 174 84 168 92 "
               "M222 82 C226 78 230 84 224 88 C216 90 214 78 222 74 C232 70 238 84 232 92")
hair_strands = clip_paths(
    "M154 120 C150 140 152 152 158 162 M226 120 C230 140 228 152 222 162 "
    "M168 92 C176 86 186 86 194 90 M204 90 C212 92 218 98 220 106",
    hair_fill)
skirt_folds = clip_paths(
    "M180 244 C172 280 152 318 138 354 M200 244 C208 280 226 318 240 354 M190 246 C190 290 190 330 190 360",
    skirt_fill.difference(hand_l))
ruffle = clip_paths("M124 336 C158 348 222 348 256 336", skirt_fill) + " " + \
         clip_paths(scallops(190, 355, 13, 12, 3.2), skirt)
skirt_stars = " ".join(star_d(x, y, 6, 2.6) for x, y in [(160, 300), (220, 300), (190, 276), (146, 330), (234, 330), (190, 318)])
belt = "M169 228 C181 234 199 234 211 228"
buckle = star_d(190, 232, 7, 3)
sleeve_puff = ("M152 184 C154 194 154 198 150 202 M162 180 C166 190 166 198 164 204 "
               "M228 184 C226 194 226 198 230 202 M218 180 C214 190 214 198 216 204")

# ---------- sombras (luz arriba a la izquierda) ----------
sh_neck = neck_fill.intersection(poly("M182 162 L198 162 L198 178 L182 172 Z"))
sh_hair = crescent(hair_fill, 10, 6)
sh_buns = crescent(bun_fill, 7, 5)
sh_skirt = crescent(skirt_fill.difference(hand_l), 30, 6)
sh_under_bodice = skirt_fill.intersection(poly(ellipse_d(190, 244, 28, 9)))
sh_bodice = crescent(bodice_fill, 10, 4)
sh_arm = crescent(arm_r.difference(sleeves).difference(hand_r), -5, 6)
ground = poly(ellipse_d(190, 368, 120, 11)).difference(skirt).difference(shoe_l).difference(shoe_r)

def twinkle(x, y, s):
    return f"M{x} {y-s} Q{x} {y} {x+s} {y} Q{x} {y} {x} {y+s} Q{x} {y} {x-s} {y} Q{x} {y} {x} {y-s} Z"
magic = " ".join(twinkle(x, y, s) for x, y, s in [(336, 40, 9), (338, 104, 7), (252, 34, 7), (322, 140, 6)])
magic_dots = " ".join(circle_d(x, y, 2.4) for x, y in [(318, 30), (346, 70), (330, 122), (272, 22), (60, 110), (70, 230), (330, 250)])

steps = [
  {"say": "La cara de la princesa: un óvalo, un poco más alto que ancho.",
   "d": [el(poly_d(face_fill), fillonly=True, fill=SKIN), el(face_line)]},
  {"say": "El pelo, corto y con las puntas hacia fuera, como dos ganchitos. Y un flequillo de lado que tapa un poco la frente.",
   "d": [el(poly_d(hair_fill), fillonly=True, fill=HAIR), el(hair_line), el(fringe_line)]},
  {"say": "Encima de la cabeza, dos moños redondos, uno a cada lado. En el medio, una diadema con una estrella.",
   "d": [el(poly_d(bun_fill), fillonly=True, fill=HAIR), el(buns_line),
         el(TIARA, fill=GOLD), el(TSTAR, "mid", fill=STAR)]},
  {"say": "El cuello y la parte de arriba del vestido. A los lados, dos mangas redondas como globos.",
   "d": [el(poly_d(neck_fill), fillonly=True, fill=SKIN), el(neck_line),
         el(poly_d(bodice_fill), fillonly=True, fill=DRESS), el(bodice_line),
         el(SLEEVE_L, fill=DRESS_T), el(SLEEVE_R, fill=DRESS_T)]},
  {"say": "Los brazos. Uno baja pegadito al cuerpo. El otro sube muy alto, con la mano cerrada.",
   "d": [el(poly_d(arm_fill), fillonly=True, fill=SKIN), el(arms_line),
         el(HAND_L, fill=SKIN), el(HAND_R, fill=SKIN)]},
  {"say": "La varita mágica: un palito largo que sale de la mano de arriba. En la punta, una estrella de cinco puntas.",
   "d": [el(poly_d(stick_fill), fillonly=True, fill=STICK), el(stick_line, "mid"),
         el(WSTAR, fill=STAR)]},
  {"say": "La falda: larga y abierta hacia abajo, como una letra A. Debajo asoman los zapatos.",
   "d": [el(poly_d(skirt_fill), fillonly=True, fill=DRESS), el(skirt_line),
         el(poly_d(shoe_fill), fillonly=True, fill=SHOE), el(shoes_line, "mid")]},
  {"say": "La cara: dos ojos grandes con pestañas, las cejas, una naricita, una sonrisa, las mejillas y unas pecas.",
   "d": [el(ellipse_d(177, 130, 6, 7.5), fill=INK), el(ellipse_d(203, 130, 6, 7.5), fill=INK),
         el(circle_d(179, 127, 2.2) + " " + circle_d(205, 127, 2.2), fillonly=True, fill="#FFFFFF"),
         el("M169 124 L165 120 M172 121 L170 116 M211 124 L215 120 M208 121 L210 116", "fine"),
         el("M169 115 C174 111 181 111 185 113 M195 113 C199 111 206 111 211 115", "mid"),
         el("M189 138 C188 142 190 144 193 143", "mid"),
         el("M181 150 C186 156 196 156 201 150", "mid", fill="#E8707F"),
         el(circle_d(169, 144, 6) + " " + circle_d(211, 144, 6), fillonly=True, fill="#F4A3B4"),
         el(" ".join(circle_d(x, y, 1.3) for x, y in [(174, 140), (178, 143), (172, 145), (206, 140), (202, 143), (208, 145)]),
            "fine", fill=FRECK)]},
  {"say": "Los detalles: espirales en los moños, mechones en el pelo, un cinturón con estrella, pliegues y un volante en la falda, y estrellitas en el vestido.",
   "d": [el(bun_spirals + " " + hair_strands + " " + sleeve_puff, "fine"),
         el(belt, "mid"), el(buckle, "mid", fill=GOLD),
         el(skirt_folds + " " + ruffle, "fine"),
         el(skirt_stars, "fine", fill=DRESS_T)]},
  {"say": "Las sombras: rayitas en el lado derecho del pelo, de los moños y de la falda, en el cuello y debajo del brazo. Por último, la sombra en el suelo y la magia que sale de la varita.",
   "d": [el(poly_d(sh_hair), fillonly=True, fill=HAIR_D), el(poly_d(sh_buns), fillonly=True, fill=HAIR_D),
         el(poly_d(sh_neck), fillonly=True, fill=SKIN_D), el(poly_d(sh_arm), fillonly=True, fill=SKIN_D),
         el(poly_d(sh_skirt), fillonly=True, fill=DRESS_D), el(poly_d(sh_under_bodice), fillonly=True, fill=DRESS_D),
         el(poly_d(sh_bodice), fillonly=True, fill=DRESS_D),
         el(" ".join([hatch(sh_hair, sp=6), hatch(sh_buns, sp=5), hatch(sh_neck, sp=4.5), hatch(sh_arm, sp=4.5),
                      hatch(sh_skirt), hatch(sh_under_bodice, sp=5), hatch(sh_bodice, sp=5)]), "fine hatch"),
         el(poly_d(ground), fillonly=True, fill=GROUND), el(hatch(ground, ang=-20, sp=5.5), "fine hatch"),
         el(magic, "mid", fill="#FCE38A"), el(magic_dots, "fine", fill=STAR)]},
]

LESSON = {"id": "varita-r", "title": "La princesa con la varita mágica", "card": "Varita",
          "what": "una princesa con su varita mágica",
          "color": "#2A9D8F", "steps": [{"say": s["say"], "d": "".join(s["d"])} for s in steps]}
