"""Prueba rápida: sirve la web, recorre TODAS las lecciones de los dos niveles hasta el final
y avisa de errores de JavaScript o audios que faltan. Capturas en /tmp/test-*.png.
Uso: python3 dev/test.py"""
import asyncio, os, subprocess, time
from playwright.async_api import async_playwright
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", "8765"], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    errs, missing = [], set()
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1024, "height": 768})
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("response", lambda r: missing.add(r.url.split("8765/")[-1]) if r.status >= 400 else None)
            await pg.goto("http://localhost:8765/"); await pg.wait_for_timeout(300)
            for lvl in ("facil", "reto"):
                await pg.click(f'[data-l="{lvl}"]'); await pg.wait_for_timeout(200)
                await pg.screenshot(path=f"/tmp/test-home-{lvl}.png")
                n = await pg.locator(".card").count()
                for i in range(n):
                    await pg.locator(".card").nth(i).click(); await pg.wait_for_timeout(150)
                    while not await pg.locator("#donePanel").is_visible():
                        await pg.click("#nextBtn"); await pg.wait_for_timeout(120)
                    await pg.click("#otherBtn"); await pg.wait_for_timeout(150)
                # pegatina rosa / dorada visibles tras terminar todo
            await pg.screenshot(path="/tmp/test-home-final.png")
            await b.close()
    finally:
        srv.terminate()
    missing.discard("favicon.ico")
    print("Errores JS:", errs or "ninguno"); print("Ficheros que faltan:", sorted(missing) or "ninguno")
asyncio.run(main())
