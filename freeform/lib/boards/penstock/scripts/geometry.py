"""Polygons and polylines over the board's grid: the plan is drawn in them, and every stage reads its masks
and distances from here rather than from circles.

A polygon is a list of (x, z) corners in order; a polyline a list of points. Masks are boolean arrays over
the Field's X, Z grids (block centres at integer x, z).
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


def polyline(X, Z, pts):
    """Distance to a polyline and the arc length along it of the nearest point."""
    best = np.full(X.shape, np.inf)
    along = np.zeros(X.shape)
    s0 = 0.0
    for i in range(len(pts) - 1):
        d, t = seg_distance(X, Z, pts[i], pts[i + 1])
        L = float(np.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]))
        m = d < best
        best = np.where(m, d, best)
        along = np.where(m, s0 + t * L, along)
        s0 += L
    return best, along


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


def centroid(poly):
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    return sum(xs) / len(xs), sum(zs) / len(zs)
