# Ari Draw — seguimiento

## Cómo trabajar en un hilo nuevo
Abre un chat nuevo y pega esto, cambiando el número de paso:

> Trabaja en mi repo de GitHub **ferjilo/ari-draw**. Lee CLAUDE.md y dev/SEGUIMIENTO.md y haz el **paso P1**. Al terminar, publica y actualiza el seguimiento.

Un paso por hilo. Si un paso sale grande, Claude lo parte y deja la mitad apuntada aquí.

## Estado actual (v1.4 · 3-oct-2026)
- 5 animales en **Fácil** (gato, pez, tortuga, búho, ratón) y 5 en **Reto** (gato sentado, pez payaso, tortuga paseando, búho en la rama, ratón con queso).
- Trazo animado paso a paso, puntos de progreso, Atrás / Otra vez / Siguiente.
- 3 voces naturales grabadas (Lucía, Pablo, Dora), elegibles en el inicio.
- Pegatinas: doradas (Fácil) y rosas "de artista" (Reto), guardadas en el iPad.
- Colores y sombras al terminar; acabado a lápiz en Reto. Pantalla encendida mientras dibuja.
- Estilo **Pastel Pop**: color pastel por animal, botones gordos sin bordes negros, mascota con bocadillo y caminito numerado de pasos.
- Instalada en el iPad desde Safari → Añadir a pantalla de inicio.

## Pasos pendientes
Marca `[x]` al terminar y añade una línea al registro.

- [ ] **P1 · Funciona sin internet.** Manifest + service worker que guarde la app y los audios en el iPad, para usarla en el coche o el avión. Comprobar que una actualización nueva llega al abrirla con conexión.
- [ ] **P2 · Animal nuevo (repetible).** Un animal por hilo, en Fácil y Reto, con sus voces. Lista de candidatos (tachar al hacerlo): perro · conejo · elefante · pingüino · caballo · mariposa · dinosaurio · unicornio.
- [ ] **P3 · Mis dibujos.** Botón "Hacer foto a mi dibujo" al terminar: foto con la cámara del iPad, guardada en el propio iPad con el animal y la fecha, y una galería para verlas.
- [ ] **P4 · Álbum de pegatinas.** Pantalla propia con todas las pegatinas (ganadas y por ganar), con la miniatura de cada animal.
- [ ] **P5 · Sonidos.** Un sonido suave al pasar de paso y un "ta-chán" al terminar, generados por código (sin ficheros). Respetar el botón de voz.
- [ ] **P6 · Cuadrícula de ayuda en Reto.** Opción de ver una cuadrícula suave en el lienzo, igual que la del papel, para copiar proporciones.
- [ ] **P7 · Rincón de papás.** Acceso protegido con una suma sencilla: qué ha dibujado y cuándo, y reiniciar pegatinas.
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
