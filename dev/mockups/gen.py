"""Mockups de estilo (paso P9). Genera tres propuestas estáticas con los dibujos reales de la app
y sus capturas. NO toca la app. Uso: python3 dev/mockups/gen.py  -> dev/mockups/*.html + /tmp/mockup-*.png
Las capturas usan fuentes locales (npm @fontsource en $FONTS) porque Google Fonts no es accesible aquí."""
import asyncio, json, os, re, subprocess, sys, time
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(os.path.dirname(here))

# ---------- Datos reales ----------
FACIL = json.loads(subprocess.check_output(["node", "-e", r'''
const s=require("fs").readFileSync(process.argv[1],"utf8");const a=s.indexOf("const LESSONS = [");const b=s.indexOf("\n];",a)+3;
process.stdout.write(JSON.stringify(eval(s.slice(a+15,b))))''', os.path.join(root, "src", "app.html")]))
RETO = json.load(open(os.path.join(root, "dev", "dibujos", "reto.json")))
DONE = {"gato", "pez"}                       # pegatinas ganadas en el mockup
LES = next(l for l in RETO if l["id"] == "gato-r"); K = 4   # lección mostrada: gato Reto, paso 5
PASTEL = {"gato": "#FFE3CC", "pez": "#D6ECFA", "tortuga": "#DCF2D6", "buho": "#EFE2D6", "raton": "#FBDDEA"}
SHADE = {"gato": "#F2B98F", "pez": "#9CCBEA", "tortuga": "#A9D99E", "buho": "#D4BBA4", "raton": "#EDAAC6"}

def fills(m):
    return re.sub(r'<(\w+) ([^>]*?)data-fill="([^"]+)"([^>]*)/>',
                  lambda t: f'<{t.group(1)} {t.group(2)}style="fill:{t.group(3)};stroke:none"{t.group(4)}/>',
                  "".join(re.findall(r'<\w+ [^>]*data-fill="[^"]+"[^>]*/>', m)))
def thumb(l, ink="#2F3A56"):
    all_ = "".join(s["d"] for s in l["steps"])
    return (f'<svg class="thumb" viewBox="-10 -10 420 420"><g>{fills(all_)}</g><g class="lines" fill="none" stroke="{ink}" '
            f'stroke-width="9" stroke-linecap="round" stroke-linejoin="round" style="fill:none">{re.sub(r"data-fill=.[^\"]*.", "", all_)}</g></svg>')
def canvas(now_color):
    prev = "".join(s["d"] for s in LES["steps"][:K]); now = LES["steps"][K]["d"]
    return (f'<svg class="cv reto" viewBox="0 0 400 400" style="--now:{now_color}"><g class="prev">{prev}</g><g class="now">{now}</g></svg>')
STAR = '<path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/>'
def star(fill, stroke="none", w=0): return f'<svg viewBox="0 0 24 24" class="st"><g fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round">{STAR}</g></svg>'
I = {  # iconos
  "back": '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  "next": '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  "again": '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v5h5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  "voice": '<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
  "pencil": '<svg viewBox="0 0 24 24"><path d="M4 20l1.2-4.6L15.6 5a2.1 2.1 0 0 1 3 0l.4.4a2.1 2.1 0 0 1 0 3L8.6 18.8z" fill="currentColor"/><path d="M4 20l4.6-1.2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  "check": '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4L19 7" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
N = len(LES["steps"]); SAY = LES["steps"][K]["say"]
CANVAS_CSS = """.cv{width:100%;height:100%;display:block;overflow:visible}.cv *{fill:none;stroke-linecap:round;stroke-linejoin:round}
.cv .fillonly,.cv .erase{display:none}.cv .prev *{stroke:#BAC1D3;stroke-width:3.4}.cv .prev .mid{stroke-width:2.4}.cv .prev .fine{stroke-width:1.4}
.cv .now *{stroke:var(--now);stroke-width:5.2}.cv .now .mid{stroke-width:3.8}.cv .now .fine{stroke-width:2.4}
.thumb{display:block;width:100%;height:auto;aspect-ratio:1}.thumb .lines .fillonly,.thumb .lines .erase{display:none}"""
SHELL = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800;900&display=swap">
<style>body{{margin:0;background:#E9E9EF;font-family:Nunito,system-ui,sans-serif}}
.cap{{font:800 15px Nunito,sans-serif;color:#555;letter-spacing:.08em;text-transform:uppercase;margin:18px 0 8px 2px}}
.wrap{{padding:8px 12px 30px;transform-origin:0 0}}.frame{{width:1180px;height:820px;box-sizing:border-box;position:relative;overflow:hidden;border-radius:28px;box-shadow:0 10px 40px rgba(0,0,0,.15)}}
.frame *{{box-sizing:border-box}}button{{font:inherit;color:inherit;border:0;background:none;padding:0}}
{canvas}
{css}</style></head><body><div class="wrap" id="w"><h1 style="font:900 26px Nunito;margin:10px 2px 0">{title}</h1>
<p style="margin:4px 2px 0;color:#555;font-weight:700;max-width:70ch">{blurb}</p>
<div class="cap">Inicio</div><div class="frame">{home}</div><div class="cap">Lección (Reto · paso {k} de {n})</div><div class="frame">{lesson}</div></div>
<script>function fit(){{const s=Math.min(1,(innerWidth-24)/1180),w=document.getElementById("w");w.style.transform="scale("+s+")";document.body.style.height=(w.scrollHeight*s+20)+"px"}}addEventListener("resize",fit);fit()</script></body></html>"""

def cards(tpl):
    return "".join(tpl(l) for l in FACIL)

# ======================= A · ESTUDIO =======================
def style_a():
    css = """
.A{--bg:#F6F4FF;--ink:#231F3A;--soft:#7A7596;--acc:#6B4EF6;--acc2:#8F76FF;--line:#E7E3FA;
 background:var(--bg);color:var(--ink);font-family:Nunito;font-weight:700;padding:34px 44px;height:100%}
.A .disp{font-family:"Baloo 2";font-weight:800}
.A .top{display:flex;align-items:center;justify-content:space-between}
.A .logo{display:flex;align-items:center;gap:12px;font-family:"Baloo 2";font-weight:800;font-size:28px}
.A .logo i{width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,var(--acc2),var(--acc));display:grid;place-items:center;color:#fff;box-shadow:0 6px 16px rgba(107,78,246,.35)}
.A .logo i svg{width:24px;height:24px}
.A .right{display:flex;gap:12px;align-items:center}
.A .pill{display:flex;align-items:center;gap:10px;background:#fff;border-radius:999px;padding:8px 16px 8px 12px;box-shadow:0 4px 14px rgba(60,40,140,.08);font-size:16px}
.A .pill .st{width:24px;height:24px}
.A .seg{display:flex;background:#fff;border-radius:999px;padding:5px;box-shadow:0 4px 14px rgba(60,40,140,.08)}
.A .seg b{padding:8px 16px;border-radius:999px;font-size:16px;color:var(--soft)}
.A .seg b.on{background:var(--acc);color:#fff}
.A .hero{display:flex;align-items:flex-end;justify-content:space-between;margin:44px 0 26px}
.A h1{font-size:60px;line-height:1;margin:0}.A h1 em{font-style:normal;color:var(--acc)}
.A .sub{font-size:22px;color:var(--soft);margin:8px 0 0}
.A .tabs{display:flex;gap:10px}.A .tab{padding:12px 24px;border-radius:16px;font-family:"Baloo 2";font-weight:700;font-size:21px;background:#fff;color:var(--soft);box-shadow:0 4px 14px rgba(60,40,140,.06);display:flex;align-items:center;gap:8px}
.A .tab.on{background:var(--ink);color:#fff}.A .tab .st{width:20px;height:20px}
.A .grid{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.A .card{background:#fff;border-radius:28px;padding:12px 12px 16px;box-shadow:0 10px 30px rgba(60,40,140,.09);position:relative}
.A .card .art{border-radius:20px;padding:14px}
.A .card .nm{font-family:"Baloo 2";font-weight:800;font-size:24px;margin:12px 4px 0;line-height:1}
.A .card .meta{display:flex;justify-content:space-between;align-items:center;margin:6px 4px 0;color:var(--soft);font-size:15px}
.A .ok{position:absolute;top:22px;right:22px;width:34px;height:34px;border-radius:50%;background:#2BC48A;color:#fff;display:grid;place-items:center;box-shadow:0 4px 10px rgba(43,196,138,.4)}
.A .ok svg{width:20px;height:20px}
.A .play{width:34px;height:34px;border-radius:50%;background:var(--bg);color:var(--acc);display:grid;place-items:center}.A .play svg{width:18px;height:18px}
.A .tip{margin-top:34px;display:flex;gap:14px;align-items:center;background:#fff;border-radius:20px;padding:16px 22px;color:var(--soft);font-size:17px;box-shadow:0 4px 14px rgba(60,40,140,.05)}
.A .tip i{flex:none;width:40px;height:40px;border-radius:12px;background:#FFF1C9;display:grid;place-items:center;font-style:normal;font-size:22px}
/* lección */
.A .bar{display:grid;grid-template-columns:56px 1fr 56px;align-items:center}
.A .round{width:56px;height:56px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 4px 14px rgba(60,40,140,.1)}.A .round svg{width:26px;height:26px}
.A .round.on{color:var(--acc)}
.A .ttl{text-align:center;font-family:"Baloo 2";font-weight:800;font-size:30px;display:flex;justify-content:center;align-items:center;gap:12px}
.A .tag{font-family:Nunito;font-size:14px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;background:#FFE3F0;color:#C2387A;padding:5px 12px;border-radius:999px}
.A .les{display:grid;grid-template-columns:650px 1fr;gap:36px;margin-top:22px;align-items:stretch}
.A .board{background:#fff;border-radius:36px;box-shadow:0 18px 50px rgba(60,40,140,.12);padding:34px;height:650px}
.A .panel{display:flex;flex-direction:column;padding:10px 0}
.A .prog{display:flex;gap:6px}.A .prog span{flex:1;height:10px;border-radius:99px;background:var(--line)}
.A .prog span.past{background:var(--acc2);opacity:.45}.A .prog span.on{background:var(--acc)}
.A .lbl{margin:16px 0 0;color:var(--acc);font-weight:900;letter-spacing:.08em;text-transform:uppercase;font-size:15px}
.A .say{font-family:"Baloo 2";font-weight:700;font-size:36px;line-height:1.15;margin:14px 0 0}
.A .legend{display:flex;gap:18px;margin-top:20px;color:var(--soft);font-size:16px}.A .legend b{display:inline-block;width:26px;height:6px;border-radius:9px;vertical-align:middle;margin-right:8px}
.A .ctr{margin-top:auto;display:flex;gap:14px;align-items:center}
.A .ctr .sec{width:76px;height:76px;border-radius:24px;background:#fff;display:grid;place-items:center;box-shadow:0 6px 18px rgba(60,40,140,.1)}.A .ctr .sec svg{width:30px;height:30px}
.A .ctr .pri{flex:1;height:76px;border-radius:24px;background:linear-gradient(135deg,var(--acc2),var(--acc));color:#fff;font-family:"Baloo 2";font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 12px 26px rgba(107,78,246,.35)}
.A .ctr .pri svg{width:30px;height:30px}"""
    card = lambda l: (f'<div class="card"><div class="art" style="background:{PASTEL[l["id"]]}">{thumb(l)}</div>'
        f'<p class="nm">{l["card"]}</p><div class="meta"><span>{len(l["steps"])} pasos</span><span class="play">{I["next"]}</span></div>'
        + (f'<span class="ok">{I["check"]}</span>' if l["id"] in DONE else "") + "</div>")
    home = f'''<div class="A">
<div class="top"><div class="logo"><i>{I["pencil"]}</i>Ari Draw</div>
<div class="right"><div class="pill">{star("#FFC53D")} <span>2 de 5 pegatinas</span></div>
<div class="seg"><b class="on">Lucía</b><b>Pablo</b><b>Dora</b></div></div></div>
<div class="hero"><div><h1 class="disp">¡Hola, <em>Ari</em>!</h1><p class="sub">¿Qué animal dibujamos hoy?</p></div>
<div class="tabs"><span class="tab on">Fácil</span><span class="tab">{star("#FF7EB6")} Reto</span></div></div>
<div class="grid">{cards(card)}</div>
<div class="tip"><i>✏️</i>Mira la línea de color, escucha y dibújala en tu papel. Al terminar, ¡pegatina!</div></div>'''
    prog = "".join(f'<span class="{"past" if i < K else "on" if i == K else ""}"></span>' for i in range(N))
    lesson = f'''<div class="A">
<div class="bar"><span class="round">{I["back"]}</span><div class="ttl">{LES["title"]}<span class="tag">Reto</span></div><span class="round on">{I["voice"]}</span></div>
<div class="les"><div class="board">{canvas("#6B4EF6")}</div>
<div class="panel"><div class="prog">{prog}</div><p class="lbl">Paso {K+1} de {N}</p><p class="say">{SAY}</p>
<div class="legend"><span><b style="background:#6B4EF6"></b>Nueva</span><span><b style="background:#BAC1D3"></b>Ya la tienes</span></div>
<div class="ctr"><span class="sec">{I["back"]}</span><span class="sec">{I["again"]}</span><span class="pri">Siguiente {I["next"]}</span></div></div></div></div>'''
    return ("Estilo A · Estudio", "Limpio y luminoso, en la línea de Simply Draw: fondo lavanda muy claro, tarjetas blancas con sombra suave, un solo color de acento (violeta) y barra de progreso por segmentos.", css, home, lesson)

# ======================= B · PASTEL POP =======================
def style_b():
    css = """
.B{--bg:#FFF5EA;--ink:#2B2A35;--soft:#7C7480;--acc:#FF6B4A;--accd:#D9482A;
 background:var(--bg);color:var(--ink);font-family:Nunito;font-weight:700;padding:32px 44px;height:100%;position:relative}
.B .blob{position:absolute;border-radius:50%;filter:blur(2px);opacity:.55;z-index:0}
.B>*{position:relative;z-index:1}.B>.blob{position:absolute;z-index:0}
.B .f{font-family:Fredoka;font-weight:700}
.B .top{display:flex;justify-content:space-between;align-items:flex-start}
.B .brand{font-family:Fredoka;font-weight:700;font-size:64px;line-height:.9;margin:0;letter-spacing:-.01em}
.B .brand span:nth-child(1){color:#FF6B4A}.B .brand span:nth-child(2){color:#FFB830}.B .brand span:nth-child(3){color:#3DB8A8}
.B .hi{display:flex;align-items:center;gap:14px;margin-top:18px}
.B .mascot{width:64px;height:64px;flex:none}
.B .bubble{background:#fff;border-radius:22px;padding:12px 20px;font-size:22px;position:relative;box-shadow:0 6px 0 #F1DDC8}
.B .bubble:before{content:"";position:absolute;left:-10px;top:22px;border:10px solid transparent;border-right-color:#fff;border-left:0}
.B .bubble b{font-family:Fredoka;color:var(--acc)}
.B .side{display:flex;flex-direction:column;align-items:flex-end;gap:14px}
.B .stk{display:flex;gap:8px;background:#fff;border-radius:24px;padding:10px 14px;box-shadow:0 6px 0 #F1DDC8;align-items:center}
.B .stk .s{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#F4ECE4}
.B .stk .s.got{background:#FFD15C;box-shadow:inset 0 -4px 0 #EDB12F}.B .stk .st{width:26px;height:26px}
.B .stk em{font-style:normal;font-family:Fredoka;font-weight:600;font-size:18px;margin-left:6px}
.B .voices{display:flex;gap:8px}.B .v{display:flex;align-items:center;gap:8px;padding:6px 14px 6px 6px;border-radius:999px;background:#fff;font-family:Fredoka;font-weight:600;font-size:18px;box-shadow:0 4px 0 #F1DDC8}
.B .v i{width:30px;height:30px;border-radius:50%;display:block}.B .v.on{background:var(--ink);color:#fff;box-shadow:0 4px 0 #000}
.B .tabs{display:flex;gap:12px;margin:30px 0 22px}
.B .tab{font-family:Fredoka;font-weight:700;font-size:24px;padding:12px 28px;border-radius:22px;background:#fff;box-shadow:0 6px 0 #F1DDC8;display:flex;gap:8px;align-items:center}
.B .tab.on{background:var(--acc);color:#fff;box-shadow:0 6px 0 var(--accd)}.B .tab .st{width:24px;height:24px}
.B .grid{display:grid;grid-template-columns:repeat(5,1fr);gap:22px}
.B .card{border-radius:34px;padding:16px 16px 18px;text-align:center;position:relative}
.B .card .plate{background:#fff;border-radius:50%;padding:16px;box-shadow:inset 0 -6px 0 rgba(0,0,0,.05)}
.B .card .nm{font-family:Fredoka;font-weight:700;font-size:28px;margin:12px 0 2px}
.B .card .n{font-size:15px;color:rgba(43,42,53,.6)}
.B .card .badge{position:absolute;top:-10px;right:-6px;width:52px;height:52px;border-radius:50%;background:#FFD15C;display:grid;place-items:center;box-shadow:0 4px 0 #EDB12F;transform:rotate(12deg)}
.B .card .badge .st{width:30px;height:30px}
/* lección */
.B .bar{display:flex;align-items:center;justify-content:space-between}
.B .rb{width:64px;height:64px;border-radius:22px;background:#fff;display:grid;place-items:center;box-shadow:0 6px 0 rgba(0,0,0,.08)}.B .rb svg{width:30px;height:30px}
.B .ttl{font-family:Fredoka;font-weight:700;font-size:38px}
.B .les{display:grid;grid-template-columns:640px 1fr;gap:34px;margin-top:20px}
.B .board{background:#fff;border-radius:44px;padding:32px;height:640px;box-shadow:0 10px 0 rgba(0,0,0,.07);
 background-image:radial-gradient(#EDE6DE 1.6px,transparent 1.7px);background-size:26px 26px}
.B .panel{display:flex;flex-direction:column}
.B .path{display:flex;align-items:center;gap:0;margin:6px 0 0}
.B .path i{width:30px;height:30px;border-radius:50%;background:#fff;display:grid;place-items:center;font:600 14px Fredoka;font-style:normal;color:#B9AFA6;flex:none}
.B .path i.past{background:#3DB8A8;color:#fff}.B .path i.on{width:44px;height:44px;background:var(--acc);color:#fff;font-size:20px;box-shadow:0 4px 0 var(--accd)}
.B .path b{flex:1;height:5px;background:#fff;min-width:4px}.B .path b.past{background:#3DB8A8}
.B .talk{display:flex;gap:14px;align-items:flex-start;margin-top:34px}
.B .talk .bubble{font-family:Fredoka;font-weight:600;font-size:32px;line-height:1.2;padding:22px 26px;border-radius:30px;box-shadow:0 8px 0 rgba(0,0,0,.06)}
.B .talk .bubble:before{top:26px}
.B .hint{color:var(--soft);font-size:17px;margin:18px 0 0 78px}
.B .ctr{margin-top:auto;display:flex;gap:14px}
.B .ctr .sec{width:84px;height:84px;border-radius:28px;background:#fff;display:grid;place-items:center;box-shadow:0 7px 0 rgba(0,0,0,.08)}.B .ctr .sec svg{width:34px;height:34px}
.B .ctr .pri{flex:1;height:84px;border-radius:28px;background:var(--acc);color:#fff;font-family:Fredoka;font-weight:700;font-size:32px;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 7px 0 var(--accd)}.B .ctr .pri svg{width:34px;height:34px}"""
    mascot = ('<svg class="mascot" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#FFB830"/><circle cx="23" cy="28" r="4" fill="#2B2A35"/>'
              '<circle cx="41" cy="28" r="4" fill="#2B2A35"/><circle cx="17" cy="38" r="5" fill="#FF8C6B" opacity=".6"/><circle cx="47" cy="38" r="5" fill="#FF8C6B" opacity=".6"/>'
              '<path d="M24 40 Q32 48 40 40" fill="none" stroke="#2B2A35" stroke-width="3.4" stroke-linecap="round"/><path d="M30 2 L34 2 L38 14 L26 14 Z" fill="#FF6B4A"/></svg>')
    card = lambda l: (f'<div class="card" style="background:{PASTEL[l["id"]]};box-shadow:0 8px 0 {SHADE[l["id"]]}"><div class="plate">{thumb(l)}</div>'
        f'<p class="nm">{l["card"]}</p><span class="n">{len(l["steps"])} pasos</span>'
        + (f'<span class="badge">{star("#fff", "#2B2A35", 1.4)}</span>' if l["id"] in DONE else "") + "</div>")
    stk = "".join(f'<span class="s {"got" if l["id"] in DONE else ""}">{star("#fff" if l["id"] in DONE else "#E3D8CE")}</span>' for l in FACIL)
    blobs = ('<i class="blob" style="width:420px;height:420px;background:#FFD9C4;right:-120px;top:-160px"></i>'
             '<i class="blob" style="width:300px;height:300px;background:#CFEDE8;left:-120px;bottom:-120px"></i>')
    home = f'''<div class="B">{blobs}
<div class="top"><div><h1 class="brand"><span>Ari</span> <span>Dr</span><span>aw</span></h1>
<div class="hi">{mascot}<div class="bubble">¡Hola, <b>Ari</b>! ¿Qué animal dibujamos hoy?</div></div></div>
<div class="side"><div class="stk">{stk}<em>2 de 5</em></div>
<div class="voices"><span class="v on"><i style="background:#FF8C6B"></i>Lucía</span><span class="v"><i style="background:#6BB7F0"></i>Pablo</span><span class="v"><i style="background:#B98CF0"></i>Dora</span></div></div></div>
<div class="tabs"><span class="tab on">Fácil</span><span class="tab">{star("#FF7EB6","#2B2A35",1.3)} Reto</span></div>
<div class="grid">{cards(card)}</div></div>'''
    path = "".join((f'<b class="{"past" if i <= K else ""}"></b>' if i else "") + f'<i class="{"past" if i < K else "on" if i == K else ""}">{i+1}</i>' for i in range(N))
    lesson = f'''<div class="B" style="background:{PASTEL["gato"]}">
<div class="bar"><span class="rb">{I["back"]}</span><span class="ttl">{LES["title"]}</span><span class="rb" style="color:var(--acc)">{I["voice"]}</span></div>
<div class="les"><div class="board">{canvas("#FF6B4A")}</div>
<div class="panel"><div class="path">{path}</div>
<div class="talk">{mascot}<div class="bubble">{SAY}</div></div>
<p class="hint">La línea naranja es la nueva. Lo gris ya lo tienes.</p>
<div class="ctr"><span class="sec">{I["back"]}</span><span class="sec">{I["again"]}</span><span class="pri">Siguiente {I["next"]}</span></div></div></div></div>'''
    return ("Estilo B · Pastel Pop", "Alegre y de juguete moderno: cada animal tiene su color pastel, botones gordos sin bordes negros, una mascota que 'habla' en bocadillo y un caminito numerado de pasos.", css, home, lesson)

# ======================= C · NOCHE ESTRELLADA =======================
def style_c():
    css = """
.C{--ink:#fff;--soft:#B9B3E0;--acc:#FFC93C;--glass:rgba(255,255,255,.08);--gl:rgba(255,255,255,.14);
 color:#fff;font-family:Nunito;font-weight:700;padding:34px 44px;height:100%;
 background:radial-gradient(1.6px 1.6px at 12% 18%,#fff8 50%,transparent 51%),radial-gradient(1.4px 1.4px at 78% 12%,#fff7 50%,transparent 51%),
 radial-gradient(2px 2px at 64% 42%,#fff5 50%,transparent 51%),radial-gradient(1.4px 1.4px at 30% 70%,#fff6 50%,transparent 51%),
 radial-gradient(1.8px 1.8px at 90% 80%,#fff6 50%,transparent 51%),radial-gradient(1.2px 1.2px at 46% 8%,#fff8 50%,transparent 51%),
 radial-gradient(900px 600px at 85% -10%,#5B3FD0 0%,transparent 60%),radial-gradient(700px 500px at 0% 110%,#2E5BC9 0%,transparent 60%),#1A1640}
.C .d{font-family:"Baloo 2";font-weight:800}
.C .top{display:flex;justify-content:space-between;align-items:center}
.C .logo{display:flex;align-items:center;gap:10px;font-family:"Baloo 2";font-weight:800;font-size:30px}.C .logo .st{width:34px;height:34px;filter:drop-shadow(0 0 10px #FFC93C)}
.C .right{display:flex;gap:12px}
.C .glass{background:var(--glass);border:1px solid var(--gl);border-radius:999px;padding:9px 16px;display:flex;align-items:center;gap:10px;font-size:16px;backdrop-filter:blur(10px)}
.C .glass .st{width:22px;height:22px}.C .glass .on{color:#1A1640;background:var(--acc);border-radius:999px;padding:4px 12px;margin:-4px 0}
.C .glass .off{color:var(--soft);padding:0 6px}
.C .hero{margin:46px 0 26px;display:flex;justify-content:space-between;align-items:flex-end}
.C h1{font-size:60px;line-height:1;margin:0}.C h1 em{font-style:normal;color:var(--acc)}
.C .sub{color:var(--soft);font-size:22px;margin:8px 0 0}
.C .tabs{display:flex;background:var(--glass);border:1px solid var(--gl);border-radius:20px;padding:5px}
.C .tab{padding:10px 24px;border-radius:15px;font-family:"Baloo 2";font-weight:700;font-size:21px;color:var(--soft);display:flex;gap:8px;align-items:center}
.C .tab.on{background:#fff;color:#1A1640}.C .tab .st{width:20px;height:20px}
.C .grid{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.C .card{background:var(--glass);border:1px solid var(--gl);border-radius:28px;padding:12px 12px 16px;position:relative}
.C .card .art{background:#FFFDF7;border-radius:20px;padding:14px}
.C .card .nm{font-family:"Baloo 2";font-weight:800;font-size:24px;margin:12px 4px 0;line-height:1}
.C .card .n{color:var(--soft);font-size:15px;margin:4px 4px 0;display:block}
.C .card .badge{position:absolute;top:-12px;right:-10px}.C .card .badge .st{width:44px;height:44px;filter:drop-shadow(0 0 12px #FFC93Caa)}
.C .tip{margin-top:34px;color:var(--soft);font-size:17px;display:flex;gap:10px;align-items:center}
/* lección */
.C .bar{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:12px}
.C .gb{height:56px;border-radius:18px;background:var(--glass);border:1px solid var(--gl);display:flex;align-items:center;gap:8px;padding:0 18px 0 14px;font-size:17px}.C .gb svg{width:24px;height:24px}
.C .ttl{text-align:center;font-family:"Baloo 2";font-weight:800;font-size:32px}
.C .les{display:grid;grid-template-columns:650px 1fr;gap:38px;margin-top:22px}
.C .board{background:#FFFDF7;border-radius:36px;padding:34px;height:650px;box-shadow:0 0 0 6px rgba(255,201,60,.18),0 0 60px rgba(120,90,255,.45)}
.C .panel{display:flex;flex-direction:column;padding-top:8px}
.C .stars{display:flex;gap:6px;flex-wrap:wrap}.C .stars .st{width:34px;height:34px}.C .stars .cur{filter:drop-shadow(0 0 10px #FFC93C);transform:scale(1.25)}
.C .lbl{margin:18px 0 0;color:var(--acc);font-weight:900;letter-spacing:.1em;text-transform:uppercase;font-size:15px}
.C .say{font-family:"Baloo 2";font-weight:700;font-size:36px;line-height:1.15;margin:12px 0 0}
.C .hint{color:var(--soft);font-size:17px;margin:18px 0 0}
.C .ctr{margin-top:auto;display:flex;gap:14px}
.C .ctr .sec{width:78px;height:78px;border-radius:26px;background:var(--glass);border:1px solid var(--gl);display:grid;place-items:center}.C .ctr .sec svg{width:30px;height:30px}
.C .ctr .pri{flex:1;height:78px;border-radius:26px;background:var(--acc);color:#1A1640;font-family:"Baloo 2";font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 0 30px rgba(255,201,60,.45)}.C .ctr .pri svg{width:30px;height:30px}"""
    card = lambda l: (f'<div class="card"><div class="art">{thumb(l)}</div><p class="nm">{l["card"]}</p><span class="n">{len(l["steps"])} pasos</span>'
        + (f'<span class="badge">{star("#FFC93C")}</span>' if l["id"] in DONE else "") + "</div>")
    stars = "".join(star("#FFC93C" if l["id"] in DONE else "rgba(255,255,255,.18)") for l in FACIL)
    home = f'''<div class="C">
<div class="top"><div class="logo">{star("#FFC93C")}Ari Draw</div>
<div class="right"><div class="glass">{stars}<span>2 de 5</span></div><div class="glass"><span class="on">Lucía</span><span class="off">Pablo</span><span class="off">Dora</span></div></div></div>
<div class="hero"><div><h1 class="d">¡Hola, <em>Ari</em>!</h1><p class="sub">¿Qué animal dibujamos hoy?</p></div>
<div class="tabs"><span class="tab on">Fácil</span><span class="tab">{star("#FF7EB6")} Reto</span></div></div>
<div class="grid">{cards(card)}</div>
<p class="tip">✏️ Mira la línea de color, escucha y dibújala en tu papel.</p></div>'''
    st = "".join(f'<span class="{"cur" if i == K else ""}">' + star("#FFC93C" if i < K else "#fff" if i == K else "rgba(255,255,255,.18)") + "</span>" for i in range(N))
    lesson = f'''<div class="C">
<div class="bar"><span class="gb">{I["back"]}Animales</span><span class="ttl">{LES["title"]}</span><span class="gb" style="padding:0 16px;color:var(--acc)">{I["voice"]}</span></div>
<div class="les"><div class="board">{canvas("#7B5CFF")}</div>
<div class="panel"><div class="stars">{st}</div><p class="lbl">Paso {K+1} de {N}</p><p class="say">{SAY}</p>
<p class="hint">La línea morada es la nueva. Lo gris ya lo tienes.</p>
<div class="ctr"><span class="sec">{I["back"]}</span><span class="sec">{I["again"]}</span><span class="pri">Siguiente {I["next"]}</span></div></div></div></div>'''
    return ("Estilo C · Noche estrellada", "Inmersivo y oscuro, ideal para dibujar por la tarde: fondo azul con estrellas, el lienzo blanco brilla en el centro, acento amarillo y los pasos como estrellas que se encienden.", css, home, lesson)

# ---------- Escribir HTML + capturas ----------
OUT = [("a-estudio", style_a), ("b-pastel", style_b), ("c-noche", style_c)]
for name, fn in OUT:
    title, blurb, css, home, lesson = fn()
    open(os.path.join(here, name + ".html"), "w").write(SHELL.format(title=title, blurb=blurb, canvas=CANVAS_CSS, css=css, home=home, lesson=lesson, k=K + 1, n=N))
open(os.path.join(here, "index.html"), "w").write("""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ari Draw · estilos</title></head>
<body style="font:700 20px system-ui;padding:24px;line-height:2"><h1>Ari Draw · propuestas de estilo (P9)</h1>
<a href="a-estudio.html">A · Estudio</a><br><a href="b-pastel.html">B · Pastel Pop</a><br><a href="c-noche.html">C · Noche estrellada</a></body></html>""")
print("HTML en dev/mockups/")

FONTS = os.environ.get("FONTS")
if FONTS:
    from playwright.async_api import async_playwright
    F = {("Baloo 2", w): f"baloo-2/files/baloo-2-latin-{w}-normal.woff2" for w in (600, 700, 800)}
    F.update({("Fredoka", w): f"fredoka/files/fredoka-latin-{w}-normal.woff2" for w in (500, 600, 700)})
    F.update({("Nunito", w): f"nunito/files/nunito-latin-{w}-normal.woff2" for w in (600, 700, 800, 900)})
    FACE = "".join(f'@font-face{{font-family:"{f}";font-weight:{w};src:url(https://fonts.local/{p})}}' for (f, w), p in F.items())
    async def shots():
        srv = subprocess.Popen(["python3", "-m", "http.server", "8767"], cwd=here, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
        try:
            async with async_playwright() as p:
                b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1204, "height": 900})
                await pg.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body=FACE, content_type="text/css"))
                await pg.route("https://fonts.local/**", lambda r: r.fulfill(path=os.path.join(FONTS, r.request.url.split("fonts.local/")[1])))
                for name, _ in OUT:
                    await pg.goto(f"http://localhost:8767/{name}.html"); await pg.wait_for_timeout(500)
                    await pg.screenshot(path=f"/tmp/mockup-{name}.png", full_page=True)
                await b.close()
        finally:
            srv.terminate()
        print("Capturas en /tmp/mockup-*.png")
    asyncio.run(shots())
