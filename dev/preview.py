"""Dibuja uno o varios animales Reto (líneas + color final) en /tmp/preview.png para revisarlos.
Uso: python3 dev/preview.py gato buho"""
import asyncio, importlib, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dibujos"))
from playwright.async_api import async_playwright
CSS = """body{margin:0;background:#fff}.row{display:flex;gap:10px;padding:10px}
svg{width:440px;height:440px;border:1px solid #ccc}svg *{fill:none;stroke-linecap:round;stroke-linejoin:round}
.ink *{stroke:#2F3A56;stroke-width:3.6}.ink .mid{stroke-width:2.6}.ink .fine{stroke-width:1.5}.ink .hatch{stroke-opacity:.55}
.ink .fillonly,.ink .erase{display:none}.fills *{stroke:none}"""
FILTER = ('<defs><filter id="pencil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" '
          'baseFrequency="0.035" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" '
          'scale="2.2" xChannelSelector="R" yChannelSelector="G"/></filter></defs>')
def fills(m):
    return "".join(t.group(0).replace("<path ", f'<path style="fill:{t.group(1)};stroke:none" ')
                   for t in re.finditer(r'<path [^>]*data-fill="([^"]+)"[^>]*/>', m))
async def main(names):
    html = f"<style>{CSS}</style>"
    for n in names:
        m = "".join(s["d"] for s in importlib.import_module(n).LESSON["steps"])
        html += (f'<div class="row"><svg viewBox="0 0 400 400"><g class="ink">{m}</g></svg>'
                 f'<svg viewBox="0 0 400 400">{FILTER}<g filter="url(#pencil)"><g class="fills">{fills(m)}</g><g class="ink">{m}</g></g></svg></div>')
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 920, "height": 465*len(names)})
        await pg.set_content(html); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/tmp/preview.png", full_page=True); await b.close()
    print("/tmp/preview.png")
asyncio.run(main(sys.argv[1:] or ["gato"]))
