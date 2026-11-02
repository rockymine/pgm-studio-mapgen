"""Lofted surfaces through control points, voxelised: the stand-in for a loft tool.

A curve is a list of 3D points joined by a centripetal Catmull-Rom spline, so it passes through every point
and rounds off a point that sticks out. A surface is a list of curves (rows); each row is resampled to the
same count by arc length and the rows are then joined by a second spline across them. Two surfaces that
share a row meet along it exactly, which is how separate sections line up.
"""
import math

def _cr(p0, p1, p2, p3, t, alpha=0.5):
    def tj(ti, a, b):
        d = math.dist(a, b)
        return ti + max(d, 1e-6) ** alpha
    t0 = 0.0; t1 = tj(t0, p0, p1); t2 = tj(t1, p1, p2); t3 = tj(t2, p2, p3)
    tt = t1 + (t2 - t1) * t
    def lerp(a, b, ta, tb):
        if tb - ta < 1e-9: return a
        return tuple(((tb - tt) * a[k] + (tt - ta) * b[k]) / (tb - ta) for k in range(3))
    a1 = lerp(p0, p1, t0, t1); a2 = lerp(p1, p2, t1, t2); a3 = lerp(p2, p3, t2, t3)
    b1 = lerp(a1, a2, t0, t2); b2 = lerp(a2, a3, t1, t3)
    return lerp(b1, b2, t1, t2)

def curve(points, closed=False, step=0.25):
    """Dense samples along the spline through `points`."""
    pts = [tuple(map(float, p)) for p in points]
    if len(pts) < 2: return pts
    if closed:
        ext = [pts[-1]] + pts + [pts[0], pts[1]]; segs = len(pts)
    else:
        ext = [tuple(2 * a - b for a, b in zip(pts[0], pts[1]))] + pts + \
              [tuple(2 * a - b for a, b in zip(pts[-1], pts[-2]))]
        segs = len(pts) - 1
    out = []
    for s in range(segs):
        p0, p1, p2, p3 = ext[s], ext[s + 1], ext[s + 2], ext[s + 3]
        n = max(2, int(math.dist(p1, p2) / step) + 1)
        for k in range(n):
            out.append(_cr(p0, p1, p2, p3, k / n))
    if not closed: out.append(pts[-1])
    return out

def resample(samples, n, closed=False):
    """`n` points spaced evenly by arc length along dense `samples`."""
    pts = samples + ([samples[0]] if closed else [])
    acc = [0.0]
    for a, b in zip(pts, pts[1:]): acc.append(acc[-1] + math.dist(a, b))
    total = acc[-1] or 1.0
    out, j = [], 0
    count = n if closed else n - 1
    for k in range(n):
        target = total * k / count
        while j < len(acc) - 2 and acc[j + 1] < target: j += 1
        seg = (acc[j + 1] - acc[j]) or 1.0
        t = (target - acc[j]) / seg
        out.append(tuple(pts[j][m] + (pts[j + 1][m] - pts[j][m]) * t for m in range(3)))
    return out

def surface(rows, closed_rows=False, density=0.4):
    """A grid of points on the surface lofted through `rows`: returns grid[i][j] (i across rows)."""
    dense_rows = [curve(r, closed=closed_rows, step=0.25) for r in rows]
    length = max(sum(math.dist(a, b) for a, b in zip(d, d[1:])) for d in dense_rows)
    n = max(4, int(length / density))
    sampled = [resample(d, n, closed=closed_rows) for d in dense_rows]
    columns = []
    for j in range(n):
        col = curve([sampled[i][j] for i in range(len(rows))], step=density)
        columns.append(col)
    m = max(len(c) for c in columns)
    columns = [resample(c, m) for c in columns]
    return [[columns[j][i] for j in range(n)] for i in range(m)]

def voxels(grid, thickness=1, normal_sign=1, closed_rows=False):
    """Cells touched by the surface, thickened along its normal. Returns a list of sets, one per layer."""
    layers = [set() for _ in range(thickness)]
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            p = grid[i][j]
            a = grid[min(i + 1, rows - 1)][j]; b = grid[max(i - 1, 0)][j]
            jn = (j + 1) % cols if closed_rows else min(j + 1, cols - 1)
            jp = (j - 1) % cols if closed_rows else max(j - 1, 0)
            c = grid[i][jn]; d = grid[i][jp]
            u = [a[k] - b[k] for k in range(3)]; v = [c[k] - d[k] for k in range(3)]
            nx = u[1] * v[2] - u[2] * v[1]; ny = u[2] * v[0] - u[0] * v[2]; nz = u[0] * v[1] - u[1] * v[0]
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            nrm = (normal_sign * nx / ln, normal_sign * ny / ln, normal_sign * nz / ln)
            for layer in range(thickness):
                for off in (layer + 0.0, layer + 0.5):
                    q = (p[0] + nrm[0] * off, p[1] + nrm[1] * off, p[2] + nrm[2] * off)
                    layers[layer].add((math.floor(q[0]), math.floor(q[1]), math.floor(q[2])))
    for k in range(1, thickness):
        layers[k] -= set().union(*layers[:k])
    return layers

def polygon_contains(poly, x, z):
    inside = False
    n = len(poly)
    for k in range(n):
        x1, z1 = poly[k]; x2, z2 = poly[(k + 1) % n]
        if (z1 > z) != (z2 > z):
            if x < x1 + (z - z1) * (x2 - x1) / (z2 - z1): inside = not inside
    return inside
