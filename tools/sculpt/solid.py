"""Solids, in the units the sketch is drawn in.

A solid is a membership test over block centres plus the box it can possibly occupy. That pairing is the
whole design: a union is the cheapest possible test but the boxes are what keep a voxelize from sampling the
whole board for every part, so a twenty-part model costs twenty small sweeps rather than twenty full ones.

Coordinates are the studio's: `x` and `z` are the plan axes, `y` is up. A block at `(x, y, z)` occupies
`[x, x+1) x [y, y+1) x [z, z+1)`, so a test is asked about the centre `(x+0.5, y+0.5, z+0.5)` — the same
convention the rasterizer floors a surface with."""
import math

INF = float("inf")


class Solid:
    """A membership test and the box it lives in. `inside(x, y, z)` takes block *centres*."""

    def __init__(self, inside, bounds):
        self.inside = inside
        self.bounds = bounds                              # (x0, x1, y0, y1, z0, z1), block indices inclusive

    def __or__(self, other):
        return union(self, other)

    def __and__(self, other):
        return intersect(self, other)

    def __sub__(self, other):
        return difference(self, other)

    def cells(self):
        """Every block index the solid holds. The sweep is over its own box, never the board's."""
        x0, x1, y0, y1, z0, z1 = (int(math.floor(v)) for v in self.bounds)
        out = set()
        test = self.inside
        for x in range(x0, x1 + 1):
            cx = x + 0.5
            for z in range(z0, z1 + 1):
                cz = z + 0.5
                for y in range(y0, y1 + 1):
                    if test(cx, y + 0.5, cz):
                        out.add((x, y, z))
        return out


# ── combinators ───────────────────────────────────────────────────────────────────────────────────────────

def union(*parts):
    parts = [p for p in parts if p is not None]
    boxes = [p.bounds for p in parts]
    bounds = (min(b[0] for b in boxes), max(b[1] for b in boxes),
              min(b[2] for b in boxes), max(b[3] for b in boxes),
              min(b[4] for b in boxes), max(b[5] for b in boxes))
    return Solid(lambda x, y, z: any(p.inside(x, y, z) for p in parts), bounds)


def intersect(*parts):
    boxes = [p.bounds for p in parts]
    bounds = (max(b[0] for b in boxes), min(b[1] for b in boxes),
              max(b[2] for b in boxes), min(b[3] for b in boxes),
              max(b[4] for b in boxes), min(b[5] for b in boxes))
    return Solid(lambda x, y, z: all(p.inside(x, y, z) for p in parts), bounds)


def difference(base, *cut):
    """`base` minus every solid in `cut`. The box is the base's — subtraction never grows a solid."""
    return Solid(lambda x, y, z: base.inside(x, y, z) and not any(c.inside(x, y, z) for c in cut),
                 base.bounds)


def shell(solid, thickness=1, keep_bottom=False, keep_top=False):
    """A solid hollowed to a wall `thickness` blocks thick, by subtracting its own inward erosion. The
    erosion is a 6-neighbour test repeated `thickness` times over the solid's cells, so it works on any
    solid rather than only on the ones with an inward-offset formula."""
    cells = solid.cells()
    inner = cells
    for _ in range(thickness):
        inner = {c for c in inner
                 if (c[0] + 1, c[1], c[2]) in inner and (c[0] - 1, c[1], c[2]) in inner
                 and (c[0], c[1] + 1, c[2]) in inner and (c[0], c[1] - 1, c[2]) in inner
                 and (c[0], c[1], c[2] + 1) in inner and (c[0], c[1], c[2] - 1) in inner}
    if keep_bottom:
        floor = min(c[1] for c in cells)
        inner = {c for c in inner if c[1] > floor + thickness - 1}
    if keep_top:
        roof = max(c[1] for c in cells)
        inner = {c for c in inner if c[1] < roof - thickness + 1}
    kept = cells - inner
    return cells_solid(kept)


def cells_solid(cells):
    """A solid that *is* a set of blocks — what `shell` and any hand-listed part come back as."""
    if not cells:
        return Solid(lambda x, y, z: False, (0, -1, 0, -1, 0, -1))
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    zs = [c[2] for c in cells]
    frozen = frozenset(cells)
    return Solid(lambda x, y, z: (int(math.floor(x)), int(math.floor(y)), int(math.floor(z))) in frozen,
                 (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))


# ── transforms ────────────────────────────────────────────────────────────────────────────────────────────

def translate(solid, dx=0, dy=0, dz=0):
    x0, x1, y0, y1, z0, z1 = solid.bounds
    return Solid(lambda x, y, z: solid.inside(x - dx, y - dy, z - dz),
                 (x0 + dx, x1 + dx, y0 + dy, y1 + dy, z0 + dz, z1 + dz))


def mirror_x(solid, at=0.0):
    """Reflected across the plane `x = at`. The plane is a seam between blocks when `at` is an integer,
    which is what keeps a mirrored pair from sharing a doubled centre column."""
    x0, x1, y0, y1, z0, z1 = solid.bounds
    lo, hi = 2 * at - (x1 + 1), 2 * at - x0
    return Solid(lambda x, y, z: solid.inside(2 * at - x, y, z),
                 (math.floor(lo), math.ceil(hi), y0, y1, z0, z1))


def mirror_z(solid, at=0.0):
    x0, x1, y0, y1, z0, z1 = solid.bounds
    lo, hi = 2 * at - (z1 + 1), 2 * at - z0
    return Solid(lambda x, y, z: solid.inside(x, y, 2 * at - z),
                 (x0, x1, y0, y1, math.floor(lo), math.ceil(hi)))


def rotate_y(solid, degrees, cx=0.0, cz=0.0):
    """Turned about the vertical through `(cx, cz)`. Any angle is allowed — the sample is taken by rotating
    the query point back — so a part can sit at 30 degrees without a second modelling pass."""
    rad = math.radians(-degrees)
    cos, sin = math.cos(rad), math.sin(rad)
    x0, x1, y0, y1, z0, z1 = solid.bounds
    corners = [(x, z) for x in (x0, x1 + 1) for z in (z0, z1 + 1)]
    turned = [(cx + (x - cx) * math.cos(-rad) - (z - cz) * math.sin(-rad),
               cz + (x - cx) * math.sin(-rad) + (z - cz) * math.cos(-rad)) for x, z in corners]
    return Solid(
        lambda x, y, z: solid.inside(cx + (x - cx) * cos - (z - cz) * sin, y,
                                     cz + (x - cx) * sin + (z - cz) * cos),
        (math.floor(min(p[0] for p in turned)), math.ceil(max(p[0] for p in turned)), y0, y1,
         math.floor(min(p[1] for p in turned)), math.ceil(max(p[1] for p in turned))))


# ── primitives ────────────────────────────────────────────────────────────────────────────────────────────

def box(x0, x1, y0, y1, z0, z1):
    """A cuboid over inclusive block ranges: `box(0, 3, ...)` is four blocks wide."""
    return Solid(lambda x, y, z: x0 <= x <= x1 + 1 and y0 <= y <= y1 + 1 and z0 <= z <= z1 + 1,
                 (x0, x1, y0, y1, z0, z1))


def ellipsoid(cx, cy, cz, rx, ry, rz):
    """Centred on `(cx, cy, cz)` with the three semi-axes. A sphere is this with one radius."""
    def inside(x, y, z):
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0
    return Solid(inside, (math.floor(cx - rx), math.ceil(cx + rx),
                          math.floor(cy - ry), math.ceil(cy + ry),
                          math.floor(cz - rz), math.ceil(cz + rz)))


def sphere(cx, cy, cz, r):
    return ellipsoid(cx, cy, cz, r, r, r)


def cylinder(cx, cz, r, y0, y1, rz=None):
    """An upright cylinder — or an elliptical one where `rz` differs from `r`."""
    rz = r if rz is None else rz
    def inside(x, y, z):
        return y0 <= y <= y1 + 1 and ((x - cx) / r) ** 2 + ((z - cz) / rz) ** 2 <= 1.0
    return Solid(inside, (math.floor(cx - r), math.ceil(cx + r), y0, y1,
                          math.floor(cz - rz), math.ceil(cz + rz)))


def frustum(cx, cz, r0, r1, y0, y1):
    """A cone or a truncated one: radius `r0` at `y0` easing to `r1` at `y1 + 1`."""
    span = (y1 + 1) - y0
    def inside(x, y, z):
        if not (y0 <= y <= y1 + 1):
            return False
        r = r0 + (r1 - r0) * (y - y0) / span
        return r > 0 and (x - cx) ** 2 + (z - cz) ** 2 <= r * r
    top = max(r0, r1)
    return Solid(inside, (math.floor(cx - top), math.ceil(cx + top), y0, y1,
                          math.floor(cz - top), math.ceil(cz + top)))


def torus(cx, cy, cz, major, minor, axis="y"):
    """A ring of tube radius `minor` whose centreline is a circle of radius `major` about `axis`."""
    def inside(x, y, z):
        if axis == "y":
            a, b, c = x - cx, z - cz, y - cy
        elif axis == "z":
            a, b, c = x - cx, y - cy, z - cz
        else:
            a, b, c = y - cy, z - cz, x - cx
        return (math.hypot(a, b) - major) ** 2 + c * c <= minor * minor
    reach = major + minor
    return Solid(inside, (math.floor(cx - reach), math.ceil(cx + reach),
                          math.floor(cy - reach), math.ceil(cy + reach),
                          math.floor(cz - reach), math.ceil(cz + reach)))


def beam(p0, p1, r, square=False):
    """A capsule (or a square-section bar) between two points in space — the one primitive the layer system
    has no answer for on its own, since a sloped strut is neither a slab nor a stack of them."""
    ax, ay, az = p0
    bx, by, bz = p1
    dx, dy, dz = bx - ax, by - ay, bz - az
    length2 = dx * dx + dy * dy + dz * dz or 1.0

    def inside(x, y, z):
        t = ((x - ax) * dx + (y - ay) * dy + (z - az) * dz) / length2
        t = max(0.0, min(1.0, t))
        ox, oy, oz = x - (ax + dx * t), y - (ay + dy * t), z - (az + dz * t)
        if square:
            return max(abs(ox), abs(oy), abs(oz)) <= r
        return ox * ox + oy * oy + oz * oz <= r * r
    return Solid(inside, (math.floor(min(ax, bx) - r), math.ceil(max(ax, bx) + r),
                          math.floor(min(ay, by) - r), math.ceil(max(ay, by) + r),
                          math.floor(min(az, bz) - r), math.ceil(max(az, bz) + r)))


def prism(points, y0, y1):
    """A 2-D outline in the plan extruded between two heights. `points` are `(x, z)` in blocks; the winding
    does not matter, since membership is the even-odd crossing count."""
    def inside(x, y, z):
        if not (y0 <= y <= y1 + 1):
            return False
        hits = 0
        for i in range(len(points)):
            x0, z0 = points[i]
            x1, z1 = points[(i + 1) % len(points)]
            if (z0 <= z < z1) or (z1 <= z < z0):
                if x < x0 + (z - z0) * (x1 - x0) / (z1 - z0):
                    hits += 1
        return hits % 2 == 1
    xs = [p[0] for p in points]
    zs = [p[1] for p in points]
    return Solid(inside, (math.floor(min(xs)), math.ceil(max(xs)), y0, y1,
                          math.floor(min(zs)), math.ceil(max(zs))))


def revolve(profile, cx, cz, y0):
    """A profile `[(radius, height), ...]` spun about the vertical through `(cx, cz)`, `y0` the first
    height's level. Radii are linearly interpolated between the stated heights, which is how a vase, a
    dome or a mushroom cap is one statement rather than a stack of circles."""
    heights = [y0 + entry[1] for entry in profile]
    radii = [entry[0] for entry in profile]

    def radius_at(y):
        if y < heights[0] or y > heights[-1]:
            return 0.0
        for i in range(len(heights) - 1):
            if heights[i] <= y <= heights[i + 1]:
                span = heights[i + 1] - heights[i] or 1
                t = (y - heights[i]) / span
                return radii[i] + (radii[i + 1] - radii[i]) * t
        return radii[-1]

    def inside(x, y, z):
        r = radius_at(y)
        return r > 0 and (x - cx) ** 2 + (z - cz) ** 2 <= r * r
    reach = max(radii)
    return Solid(inside, (math.floor(cx - reach), math.ceil(cx + reach),
                          math.floor(heights[0]), math.ceil(heights[-1]),
                          math.floor(cz - reach), math.ceil(cz + reach)))


def half_space(nx, ny, nz, d):
    """Everything on one side of the plane `n . p <= d`. The knife every chamfer is cut with."""
    return Solid(lambda x, y, z: nx * x + ny * y + nz * z <= d, (-4096, 4096, 0, 255, -4096, 4096))


def _even_odd(points, a, b):
    hits = 0
    for i in range(len(points)):
        a0, b0 = points[i]
        a1, b1 = points[(i + 1) % len(points)]
        if (b0 <= b < b1) or (b1 <= b < b0):
            if a < a0 + (b - b0) * (a1 - a0) / (b1 - b0):
                hits += 1
    return hits % 2 == 1


def extrude_x(profile, x0, x1):
    """A silhouette in the `(z, y)` plane — a side elevation — swept across `x`. The one primitive a vehicle
    needs: a car is a profile first and a plan second, and intersecting the two is what gives it both."""
    zs = [p[0] for p in profile]
    ys = [p[1] for p in profile]
    return Solid(lambda x, y, z: x0 <= x <= x1 + 1 and _even_odd(profile, z, y),
                 (x0, x1, math.floor(min(ys)), math.ceil(max(ys)),
                  math.floor(min(zs)), math.ceil(max(zs))))


def extrude_z(profile, z0, z1):
    """The same for a front elevation: a silhouette in `(x, y)` swept along `z`."""
    xs = [p[0] for p in profile]
    ys = [p[1] for p in profile]
    return Solid(lambda x, y, z: z0 <= z <= z1 + 1 and _even_odd(profile, x, y),
                 (math.floor(min(xs)), math.ceil(max(xs)),
                  math.floor(min(ys)), math.ceil(max(ys)), z0, z1))
