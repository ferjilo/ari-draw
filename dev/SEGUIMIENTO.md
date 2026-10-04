# Ari Draw — seguimiento

## Cómo trabajar en un hilo nuevo
Abre un chat nuevo y pega esto, cambiando el número de paso:

> Trabaja en mi repo de GitHub **ferjilo/ari-draw**. Lee CLAUDE.md y dev/SEGUIMIENTO.md y haz el **paso P1**. Al terminar, publica y actualiza el seguimiento.

Un paso por hilo. Si un paso sale grande, Claude lo parte y deja la mitad apuntada aquí.

## Estado actual (v1.7 · 4-oct-2026)
- 5 animales en **Fácil** (gato, pez, tortuga, búho, ratón) y 5 en **Reto** (gato sentado, pez payaso, tortuga paseando, búho en la rama, ratón con queso).
- 2 princesas en cada nivel: **Fácil** (princesa con corona y lazo · princesa con varita, 6 pasos cada una) y **Reto** (princesa con una rosa · princesa con la varita mágica, 10 pasos cada una). De momento aparece en la misma lista que los animales, al final; los textos de inicio ya dicen "dibujo" en vez de "animal".
- Trazo animado paso a paso, puntos de progreso, Atrás / Otra vez / Siguiente.
- 3 voces naturales grabadas (Lucía, Pablo, Dora), elegibles en el inicio.
- Pegatinas: doradas (Fácil) y rosas "de artista" (Reto), guardadas en el iPad. Cada dibujo guarda cuántas veces se ha hecho y la fecha de la última (`ari.done` = `{id:{n,t}}`; los antiguos `true` siguen valiendo).
- **Rincón de papás** (botón discreto con candado al pie del inicio, se entra con una suma): lista de dibujos por nivel con veces y última fecha, quitar una pegatina suelta o borrarlas todas (pide confirmar).
- Colores y sombras al terminar; acabado a lápiz en Reto. Pantalla encendida mientras dibuja.
- Estilo **Pastel Pop**: color pastel por animal, botones gordos sin bordes negros, mascota con bocadillo y caminito numerado de pasos.
- Instalada en el iPad desde Safari → Añadir a pantalla de inicio.

## Pasos pendientes
Marca `[x]` al terminar y añade una línea al registro.

- [ ] **P1 · Funciona sin internet.** Manifest + service worker que guarde la app y los audios en el iPad, para usarla en el coche o el avión. Comprobar que una actualización nueva llega al abrirla con conexión.
- [ ] **P2 · Animal nuevo (repetible).** Un animal por hilo, en Fácil y Reto, con sus voces. Lista de candidatos (tachar al hacerlo): perro · conejo · elefante · pingüino · caballo · mariposa · dinosaurio · unicornio.
- [ ] **P10 · Princesas (repetible).** Una princesa por hilo, en Fácil y Reto, con sus voces. Diseños originales (nada de personajes de películas). Hechas: princesa con corona / princesa con la rosa · princesa con varita (pelirroja con moños, vestido amarillo). Ideas: princesa en su castillo · princesa con capa de invierno · princesa bailando · princesa con su mascota.
- [ ] **P11 · Pantalla de categorías.** Antes de la lista de dibujos, elegir categoría (**Animales**, **Princesas**, y las que vengan) con tarjetas grandes y su dibujo. Campo `cat` en cada lección (Fácil en `LESSONS`, Reto en cada `.py`); `ANIMALES_RETO` pasa a ser `RETO` con todas. Pegatinas por categoría y nivel, el botón "Dibujos" de la lección vuelve a la categoría, y guardar la última categoría en `ari.cat`. Regrabar frases genéricas si cambian.
- [ ] **P3 · Mis dibujos.** Botón "Hacer foto a mi dibujo" al terminar: foto con la cámara del iPad, guardada en el propio iPad con el animal y la fecha, y una galería para verlas.
- [ ] **P4 · Álbum de pegatinas.** Pantalla propia con todas las pegatinas (ganadas y por ganar), con la miniatura de cada animal.
- [ ] **P5 · Sonidos.** Un sonido suave al pasar de paso y un "ta-chán" al terminar, generados por código (sin ficheros). Respetar el botón de voz.
- [ ] **P6 · Cuadrícula de ayuda en Reto.** Opción de ver una cuadrícula suave en el lienzo, igual que la del papel, para copiar proporciones.
- [x] **P7 · Rincón de papás.** Acceso protegido con una suma sencilla: qué ha dibujado y cuándo, y reiniciar pegatinas (todas o una a una).
- [ ] **P8 · Nivel 3 "Experto".** Dibujos con escena completa (fondo, dos animales, perspectiva sencilla). Solo cuando domine Reto.
- [x] **P9 · Estilo más moderno (tipo Simply Draw).** Rediseño visual de inicio y lección, sin cambiar el funcionamiento.
  - [x] P9a · Tres mockups con los dibujos reales: https://ferjilo.github.io/ari-draw/dev/mockups/ — A · Estudio (claro, violeta), B · Pastel Pop (color por animal, mascota), C · Noche estrellada (oscuro, amarillo). Se regeneran con `dev/mockups/gen.py`.
  - [x] P9b · Elegido **B · Pastel Pop** y aplicado en `src/app.html` (CSS, marcado de inicio y lección, fuente Fredoka, `theme-color` en `dev/build.py`). Los mockups A y C quedan en `dev/mockups/` como referencia.

## Ideas sueltas (sin priorizar)
- Animales de casa o de sitios que visitáis, como lecciones especiales.
- Lecciones de temporada (Navidad, Halloween).

## Registro
- 2026-10-03 · v1.0 Primera versión (5 animales, voz del sistema). Repo y GitHub Pages.
- 2026-10-03 · v1.1 Voces naturales grabadas: Lucía, Pablo y Dora.
- 2026-10-03 · v1.2 Nivel Reto con 5 dibujos tipo ilustrador.
- 2026-10-03 · v1.3 Código fuente, herramientas y este seguimiento en el repo.
- 2026-10-03 · P9a Tres mockups de estilo en `dev/mockups/` (la app no cambia).
- 2026-10-03 · v1.4 P9b Estilo Pastel Pop aplicado a toda la app.
- 2026-10-04 · v1.5 P10 Primera princesa (Fácil + Reto, `dev/dibujos/princesa.py`) con las 3 voces. Textos "animal" → "dibujo" y `hola` regrabado. P11 (categorías) apuntado.
- 2026-10-04 · v1.6 P10 Segunda princesa: con varita (Fácil `varita` + Reto `dev/dibujos/varita.py`), pelirroja con dos moños y vestido amarillo, con las 3 voces.
- 2026-10-04 · v1.7 P7 Rincón de papás: suma para entrar, veces y fecha de cada dibujo, quitar una pegatina o borrarlas todas.
