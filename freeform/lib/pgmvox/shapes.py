"""Shapes over the board's grid: polygons, polylines, discs, ellipses and rings as boolean masks and distance
fields, and the depth of every cell inside a mask.

A polygon is a list of (x, z) corners in order; a polyline a list of points. Masks are boolean arrays over X, Z
grids of block centres at integer x, z (World.grid() or numpy.meshgrid with indexing="ij").
"""
import numpy as np


def inside(X, Z, poly):
    """True where the block (x, z) lies inside the polygon."""
    X = np.asarray(X, float); Z = np.asarray(Z, float)
    res = np.zeros(X.shape, bool)
    n = len(poly)
    for i in range(n):                          # even-odd rule, one edge at a time over the whole grid
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % n]
        if z1 == z2:
            continue
        crosses = (z1 > Z) != (z2 > Z)
        xc = x1 + (Z - z1) * (x2 - x1) / (z2 - z1)
        res ^= crosses & (X < xc)
    return res


def seg_distance(X, Z, a, b):
    """Distance from every (X, Z) to the segment a-b, and the parameter t of the nearest point on it."""
    ax, az = a; bx, bz = b
    dx, dz = bx - ax, bz - az
    L2 = dx * dx + dz * dz or 1e-9
    t = np.clip(((X - ax) * dx + (Z - az) * dz) / L2, 0, 1)
    return np.hypot(X - (ax + t * dx), Z - (az + t * dz)), t


def edge_distance(X, Z, poly):
    """Distance to the polygon's boundary."""
    best = np.full(X.shape, np.inf)
    for i in range(len(poly)):
        d, _ = seg_distance(X, Z, poly[i], poly[(i + 1) % len(poly)])
        best = np.minimum(best, d)
    return best


def signed_distance(X, Z, poly):
    """Negative inside, positive outside, in blocks."""
    d = edge_distance(X, Z, poly)
    return np.where(inside(X, Z, poly), -d, d)


def polyline(X, Z, pts, side=False):
    """Distance to a polyline and the arc length along it of the nearest point; with `side`, also which side of it
    each point lies, +1 to the right walking along it (x east, z south) and -1 to the left."""
    best = np.full(np.shape(X), np.inf)
    along = np.zeros(np.shape(X))
    right = np.ones(np.shape(X))
    s0 = 0.0
    for i in range(len(pts) - 1):
        (ax, az), (bx, bz) = pts[i], pts[i + 1]
        d, t = seg_distance(X, Z, pts[i], pts[i + 1])
        L = float(np.hypot(bx - ax, bz - az))
        m = d < best
        best = np.where(m, d, best)
        along = np.where(m, s0 + t * L, along)
        if side:
            right = np.where(m, np.where((bx - ax) * (Z - az) - (bz - az) * (X - ax) >= 0, 1.0, -1.0), right)
        s0 += L
    return (best, along, right) if side else (best, along)


def nearest_on(pts, x, z):
    """The distance from (x, z) to a polyline and the arc length along it of the nearest point."""
    d, s = polyline(np.array(float(x)), np.array(float(z)), pts)
    return float(d), float(s)


def length(pts):
    return float(sum(np.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)))


def point_at(pts, s):
    """The point and the unit heading at arc length s along a polyline."""
    for i in range(len(pts) - 1):
        (ax, az), (bx, bz) = pts[i], pts[i + 1]
        L = float(np.hypot(bx - ax, bz - az))
        if s <= L or i == len(pts) - 2:
            t = min(max(s / L, 0), 1) if L else 0
            return (ax + t * (bx - ax), az + t * (bz - az)), ((bx - ax) / L, (bz - az) / L)
        s -= L


def walk_cells(pts):
    """The four-connected cells along a polyline, in order, each once."""
    out = []
    for i in range(len(pts) - 1):
        (ax, az), (bx, bz) = pts[i], pts[i + 1]
        n = int(max(abs(bx - ax), abs(bz - az)) * 3) + 2
        for t in np.linspace(0, 1, n):
            c = (int(round(ax + (bx - ax) * t)), int(round(az + (bz - az) * t)))
            if out and c == out[-1]:
                continue
            if out and abs(c[0] - out[-1][0]) + abs(c[1] - out[-1][1]) == 2:
                out.append((c[0], out[-1][1]))
            out.append(c)
    return out


def rect_cells(x0, z0, x1, z1):
    """The cells of a rectangle by its corners, (x0, z0) to (x1, z1) inclusive, in either order: the order every
    function here takes. `Raster.rect` and `pieces.box` take ranges, (x0, x1, z0, z1)."""
    return {(x, z) for x in range(min(x0, x1), max(x0, x1) + 1) for z in range(min(z0, z1), max(z0, z1) + 1)}


def poly_cells(poly):
    """The cells whose centres lie inside a polygon, as a set."""
    xs, zs = [p[0] for p in poly], [p[1] for p in poly]
    x0, x1, z0, z1 = int(np.floor(min(xs))) - 1, int(np.ceil(max(xs))) + 1, int(np.floor(min(zs))) - 1, int(np.ceil(max(zs))) + 1
    X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    m = inside(X + 0.0, Z + 0.0, poly)
    return {(int(x), int(z)) for x, z in zip(X[m], Z[m])}


def disc(X, Z, cx, cz, r):
    return np.hypot(X - cx, Z - cz) <= r


def ring(X, Z, cx, cz, r0, r1):
    d = np.hypot(X - cx, Z - cz)
    return (d >= r0) & (d <= r1)


def ellipse(X, Z, cx, cz, rx, rz, angle=0.0):
    """An ellipse, its x radius turned `angle` radians from east toward south."""
    dx, dz = X - cx, Z - cz
    c, s = np.cos(angle), np.sin(angle)
    u, v = dx * c + dz * s, -dx * s + dz * c
    return (u / rx) ** 2 + (v / rz) ** 2 <= 1.0


def stroke(X, Z, a, b, w0, w1=None, round_end=True):
    """A tapered stroke from a to b, w0 wide at a and w1 at b, its far end rounded."""
    w1 = w0 if w1 is None else w1
    d, t = seg_distance(X, Z, a, b)
    half = (w0 + (w1 - w0) * t) / 2
    m = d <= half
    if round_end:
        m |= np.hypot(X - b[0], Z - b[1]) <= w1 / 2
    return m


def boundary(mask, diagonal=False):
    """The cells of a mask with a neighbour outside it (four neighbours, or eight)."""
    m = np.pad(mask, 1)
    out = ~m[:-2, 1:-1] | ~m[2:, 1:-1] | ~m[1:-1, :-2] | ~m[1:-1, 2:]
    if diagonal:
        out |= ~m[:-2, :-2] | ~m[2:, 2:] | ~m[:-2, 2:] | ~m[2:, :-2]
    return mask & out


def edge_depth(mask):
    """For every cell of a mask, how many steps it lies inside its edge (0 on the edge, -1 outside): the
    measure an underside, a parapet inset or a terrace is cut by."""
    from scipy import ndimage
    inside_ = ndimage.distance_transform_cdt(mask, metric="taxicab")
    return np.where(mask, inside_ - 1, -1)
