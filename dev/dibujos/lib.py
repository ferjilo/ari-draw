"""Herramientas para generar dibujos 'tipo ilustrador' en SVG: contornos, sombreado a rayas,
pelo/plumas a base de trazos cortos y sombras de color. Todo en un lienzo de 400x400."""
import math, random
from svgpathtools import parse_path
from shapely.geometry import Polygon, LineString, MultiLineString, GeometryCollection, Point
from shapely import affinity
from shapely.ops import unary_union

R = random.Random(7)

def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")

# ---------- elementos ----------
def el(d, cls=None, fill=None, fillonly=False):
    c = []
    if cls: c.append(cls)
    if fillonly: c.append("fillonly")
    a = f' class="{" ".join(c)}"' if c else ""
    fl = f' data-fill="{fill}"' if fill else ""
    return f'<path d="{d}"{a}{fl}/>'

# ---------- formas ----------
def ellipse_d(cx, cy, rx, ry, rot=0):
    k = 0.5523
    pts = [(rx, 0), (rx, k*ry), (k*rx, ry), (0, ry), (-k*rx, ry), (-rx, k*ry), (-rx, 0),
           (-rx, -k*ry), (-k*rx, -ry), (0, -ry), (k*rx, -ry), (rx, -k*ry), (rx, 0)]
    t = math.radians(rot); c, s = math.cos(t), math.sin(t)
    P = [(cx + x*c - y*s, cy + x*s + y*c) for x, y in pts]
    d = f"M{f(P[0][0])} {f(P[0][1])}"
    for i in range(1, 13, 3):
        d += " C" + " ".join(f"{f(P[j][0])} {f(P[j][1])}" for j in (i, i+1, i+2))
    return d + " Z"

def circle_d(cx, cy, r):
    return ellipse_d(cx, cy, r, r)

def poly(d, n=260):
    """Polígono shapely a partir de un path (se cierra solo)."""
    p = parse_path(d)
    pts = [p.point(i/n) for i in range(n+1)]
    return Polygon([(z.real, z.imag) for z in pts]).buffer(0)

def iter_lines(g):
    if g.is_empty: return []
    if isinstance(g, LineString): return [g]
    if isinstance(g, (MultiLineString, GeometryCollection)):
        out = []
        for x in g.geoms: out += iter_lines(x)
        return out
    return []

def lines_d(lines):
    d = []
    for ln in lines:
        cs = list(ln.coords)
        d.append("M" + " L".join(f"{f(x)} {f(y)}" for x, y in cs))
    return " ".join(d)

def poly_d(g):
    if g.is_empty: return ""
    geoms = [g] if isinstance(g, Polygon) else list(getattr(g, "geoms", []))
    out = []
    for p in geoms:
        if not isinstance(p, Polygon) or p.area < 4: continue
        cs = list(p.exterior.coords)
        out.append("M" + " L".join(f"{f(x)} {f(y)}" for x, y in cs) + " Z")
    return " ".join(out)

# ---------- sombreado ----------
def hatch(region, ang=-38, sp=6.5, minlen=4, wobble=0.0):
    if region.is_empty: return ""
    minx, miny, maxx, maxy = region.bounds
    cx, cy = (minx+maxx)/2, (miny+maxy)/2
    Rr = math.hypot(maxx-minx, maxy-miny)
    t = math.radians(ang); dx, dy = math.cos(t), math.sin(t); nx, ny = -dy, dx
    segs = []
    k = -Rr
    while k <= Rr:
        o = k + (R.uniform(-wobble, wobble) if wobble else 0)
        a = (cx + nx*o - dx*Rr, cy + ny*o - dy*Rr); b = (cx + nx*o + dx*Rr, cy + ny*o + dy*Rr)
        for s in iter_lines(LineString([a, b]).intersection(region)):
            if s.length >= minlen: segs.append(s)
        k += sp
    return lines_d(segs)

def crescent(shape, dx, dy):
    """Banda en sombra (lado contrario a la luz, que viene de arriba a la izquierda)."""
    return shape.difference(affinity.translate(shape, -dx, -dy))

# ---------- trazos de textura ----------
def _pt(path, t):
    z = path.point(t); dz = path.derivative(t)
    L = abs(dz) or 1
    return (z.real, z.imag), (dz.real/L, dz.imag/L)

def ticks(d, t0, t1, n, length, shape=None, out=True, curl=0.35, jitter=0.25, inset=0.15):
    """Trazos cortos perpendiculares al contorno (pelo, plumas). out=True hacia fuera."""
    p = parse_path(d)
    parts = []
    for i in range(n):
        t = t0 + (t1 - t0) * (i + 0.5) / n
        (x, y), (tx, ty) = _pt(p, t)
        nx, ny = ty, -tx
        if shape is not None:
            inside = shape.contains(Point(x + nx*2, y + ny*2))
            if inside == out: nx, ny = -nx, -ny
        L = length * (1 + R.uniform(-jitter, jitter))
        sx, sy = x - nx*L*inset, y - ny*L*inset
        ex, ey = x + nx*L, y + ny*L
        cx_, cy_ = (sx+ex)/2 + tx*L*curl, (sy+ey)/2 + ty*L*curl
        parts.append(f"M{f(sx)} {f(sy)} Q{f(cx_)} {f(cy_)} {f(ex)} {f(ey)}")
    return " ".join(parts)

def chevrons(points, w, h):
    """Uves pequeñas (plumas del pecho, pelo del pecho)."""
    return " ".join(f"M{f(x-w)} {f(y-h)} L{f(x)} {f(y)} L{f(x+w)} {f(y-h)}" for x, y in points)

def scallops(cx, y, w, n, h):
    """Fila de semicírculos (plumas, escamas)."""
    out = []
    x0 = cx - w*n/2
    for i in range(n):
        a = x0 + i*w
        out.append(f"M{f(a)} {f(y)} Q{f(a+w/2)} {f(y+h*2)} {f(a+w)} {f(y)}")
    return " ".join(out)

def bridge(d_outer, d_inner, ts, frac=1.0, rev_inner=False):
    """Líneas que cruzan una forma tubular (rayas de una cola, anillos)."""
    po, pi = parse_path(d_outer), parse_path(d_inner)
    out = []
    for t in ts:
        a = po.point(t); b = pi.point(1-t if rev_inner else t)
        e = a + (b - a) * frac
        m = (a + e)/2 + (complex(-(e-a).imag, (e-a).real) * 0.12)
        out.append(f"M{f(a.real)} {f(a.imag)} Q{f(m.real)} {f(m.imag)} {f(e.real)} {f(e.imag)}")
    return " ".join(out)

def sample(d, t):
    z = parse_path(d).point(t); return (z.real, z.imag)

def tnear(d, x, y, n=600):
    p = parse_path(d); best = (1e9, 0)
    for i in range(n+1):
        z = p.point(i/n); dd = abs(z - complex(x, y))
        if dd < best[0]: best = (dd, i/n)
    return best[1]

def ticks_between(d, a, b, n, length, shape=None, **kw):
    t0, t1 = tnear(d, *a), tnear(d, *b)
    if t0 > t1: t0, t1 = t1, t0
    return ticks(d, t0, t1, n, length, shape, **kw)

def fan(cx, cy, d_edge, ts, frac=0.92, start=0.12):
    p = parse_path(d_edge); o = complex(cx, cy); out = []
    for t in ts:
        e = p.point(t); a = o + (e - o)*start; b = o + (e - o)*frac
        out.append(f"M{f(a.real)} {f(a.imag)} L{f(b.real)} {f(b.imag)}")
    return " ".join(out)

def clip_paths(d, region):
    """Recorta un trazo (path) a una región, devuelve d."""
    p = parse_path(d)
    segs = []
    for sub in p.continuous_subpaths():
        n = max(12, int(sub.length()/3))
        pts = [sub.point(i/n) for i in range(n+1)]
        ln = LineString([(z.real, z.imag) for z in pts])
        segs += [s for s in iter_lines(ln.intersection(region)) if s.length > 3]
    return lines_d(segs)

def lin(a, b, n):
    return [a + (b-a)*i/(n-1) for i in range(n)] if n > 1 else [a]

def scale_grid(region, x0, x1, y0, y1, w=12, step=16, h=9, dy=13):
    out = []
    for r, y in enumerate(range(int(y0), int(y1), dy)):
        x = x0 + (step/2 if r % 2 else 0)
        while x < x1:
            out.append(f"M{f(x)} {y} Q{f(x+w/2)} {f(y+h)} {f(x+w)} {y}")
            x += step
    return clip_paths(" ".join(out), region)
