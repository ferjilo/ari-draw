# Ari Draw — instrucciones para Claude

App web de clases de dibujo paso a paso para una niña de 6 años (Ari). Ella dibuja **en papel**; el iPad le enseña cada trazo animado y una voz natural se lo explica. Dos niveles: **Fácil** (dibujos simples) y **Reto** (estilo ilustrador: pelo, plumas, sombreado a rayas, acabado a lápiz).

- Web publicada: https://ferjilo.github.io/ari-draw/ (GitHub Pages desde `main`, raíz). **Publicar = `git push`**; tarda 1–2 min.
- Seguimiento, pasos pendientes y registro: `dev/SEGUIMIENTO.md`. Léelo siempre al empezar.

## Arranque de sesión (hazlo en este orden, sin explorar de más)
1. `add_repo` ferjilo/ari-draw con acceso `push`, y clónalo.
2. Lee **solo** `CLAUDE.md` y `dev/SEGUIMIENTO.md`.
3. `bash dev/setup.sh` (añade `voz` solo si vas a grabar frases nuevas: descarga ~500 MB).
4. Haz el paso pedido. Al acabar: `python3 dev/build.py`, `python3 dev/test.py`, commit, push, y actualiza `dev/SEGUIMIENTO.md`.

## Ahorro de tokens (obligatorio)
- **Nunca leas** `index.html` (se genera, ~220 KB) ni `dev/dibujos/reto.json`. No listes `audio/` (hay cientos de mp3).
- `src/app.html` es grande: usa Grep y Read con `offset`/`limit` sobre la zona que vas a tocar. No lo leas entero.
- No publiques Artifacts ni cargues skills de diseño: el producto es la web de GitHub Pages.
- Revisión visual: una sola captura por cambio (`dev/preview.py` para dibujos, o las de `dev/test.py`). Sin bucles de retoques.
- No uses subagentes. Respuestas finales cortas: qué ha cambiado y la dirección de la web.

## Estructura
```
index.html               GENERADO por dev/build.py. No editar a mano.
audio/<voz>/<clave>.mp3  Frases grabadas. Voces: lucia, pablo, dora.
src/app.html             Fuente de la app (HTML+CSS+JS). Aquí van los cambios de interfaz y los dibujos Fácil (const LESSONS).
dev/build.py             src/app.html + dibujos Reto -> index.html. Lista ANIMALES_RETO = orden del nivel Reto.
dev/dibujos/lib.py       Herramientas de dibujo procedural (ver abajo).
dev/dibujos/<animal>.py  Un dibujo Reto por fichero; define LESSON.
dev/voz/frases.js        Saca todas las frases que la app reproduce.
dev/voz/gen_audio.py     Graba las que falten con las 3 voces (o fuerza claves: gen_audio.py gato-r-3).
dev/preview.py           Captura de dibujos Reto -> /tmp/preview.png.
dev/test.py              Recorre todas las lecciones; avisa de errores JS y audios que faltan.
dev/setup.sh             Dependencias (+ modelos de voz con `voz`).
```

## Datos de una lección
`{id, title, card, what, color, steps:[{say, d}]}` · `d` = elementos SVG en un lienzo 400×400.
- Fácil: en `const LESSONS` de `src/app.html`. Ids sin sufijo (`gato`).
- Reto: `dev/dibujos/<animal>.py`, id con `-r` (`gato-r`), añadir el nombre a `ANIMALES_RETO`.
- `what` se lee en frases ("Has dibujado **un gato sentado**"): con artículo.
- `say`: castellano de España, 2.ª persona, frases cortas y concretas para 6 años. Si el paso tapa líneas, decir "Borra la línea que…".

## Convenciones de dibujo (Reto)
- Clases de trazo: sin clase = contorno · `mid` = detalle · `fine` = textura · `fine hatch` = sombreado a rayas · `fillonly` = solo color final (no se dibuja) · `erase` = línea que se dibuja pero desaparece al final.
- `data-fill="#color"` en un elemento = su color en el dibujo terminado. Los colores se pintan debajo de todas las líneas.
- Luz desde arriba a la izquierda: sombras con `crescent(forma, dx, dy)` + `hatch(...)` + relleno más oscuro `fillonly`.
- Las líneas de un objeto que queda detrás de otro se recortan con `clip_paths` (o se marcan `erase` si el niño las dibuja primero).
- Agrupa las texturas de un paso en **un solo path** (la animación dura poco).
- 8–10 pasos: forma grande → partes → cara → texturas → sombras → fondo.
- lib.py: `el, ellipse_d, circle_d, poly, poly_d, crescent, hatch, ticks_between, chevrons, scallops, scale_grid, clip_paths, fan, bridge`.
- Tinta `#2F3A56`. Revisa con `python3 dev/preview.py <animal>` (1 captura).

## Audio
Claves: `hola`, `<id>-<n>` (paso n), `<id>-0i` (intro + paso 0), `<id>-fin-nueva`, `<id>-fin-otra`. Textos de intro y final: `introText` / `finText` en `src/app.html`. Si cambias un texto ya grabado, regraba esa clave (`gen_audio.py <clave>`). La app usa la voz del sistema solo si falta el mp3.

## Interfaz
Estilo **Pastel Pop** (P9): tipos Fredoka (títulos) + Nunito. Fondo crema con manchas suaves; en la lección el fondo toma el pastel del animal (`--a` + `color-mix`, clase `in-lesson` en `<html>`). Botones blancos o coral sin borde, con sombra de color debajo. Mascota con bocadillo para las instrucciones y caminito numerado de pasos (`#dots`). Colores como variables en `:root` (`--pen` = tinta de los dibujos). Mockups de referencia en `dev/mockups/` (`gen.py`). Guardado local en el iPad (`localStorage`): `ari.done`, `ari.voz`, `ari.nivel`, `ari.voice`.

## Git
`git -c user.name="Fernando" -c user.email="ferjilo@users.noreply.github.com" commit -m "..."` y `git push origin main`.
Desde estas sesiones **no** se pueden crear repos ni cambiar ajustes de GitHub Pages; push sí.
