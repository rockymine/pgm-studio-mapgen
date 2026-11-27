"""Rebuild the author's terrain pieces with a few reusable functions, and measure how close they come.

Each piece is described by: a frame (the plane it lies in), control points (the author's own markers first, more
added where the surface strays), an outline polygon, and a thickness. `build_sheet` turns that description back
into blocks. Nothing of the piece's own blocks is copied: the description is all the rebuild sees.
"""
import collections
import math
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))          # loft.py, terrain.py
import terrain


# ---------------------------------------------------------------- the frame a sheet lies in
def frame(cells):
    n = len(cells)
    mean = [sum(c[k] for c in cells) / n for k in range(3)]
    cov = [[sum((c[i] - mean[i]) * (c[j] - mean[j]) for c in cells) / n for j in range(3)] for i in range(3)]

    def mul(v): return [sum(cov[i][j] * v[j] for j in range(3)) for i in range(3)]

    def unit(v):
        length = math.sqrt(sum(a * a for a in v)) or 1.0
        return [a / length for a in v]
    axes = []
    for seed in ([1, 0.3, 0.7], [0.2, 1, 0.1], [0.3, 0.2, 1]):
        v = unit(seed)
        for _ in range(120):
            v = mul(v)
            for a in axes:
                dot = sum(v[k] * a[k] for k in range(3)); v = [v[k] - dot * a[k] for k in range(3)]
            v = unit(v)
        axes.append(v)
    if axes[2][1] < 0: axes[2] = [-a for a in axes[2]]          # the normal points up where it can
    return mean, axes


def to_frame(p, fr):
    mean, axes = fr
    d = [p[k] - mean[k] for k in range(3)]
    return tuple(sum(d[k] * a[k] for k in range(3)) for a in axes)


def from_frame(u, v, w, fr):
    mean, axes = fr
    return tuple(mean[k] + u * axes[0][k] + v * axes[1][k] + w * axes[2][k] for k in range(3))


# ---------------------------------------------------------------- control points: the markers, then where it strays
def mid_surface(cells, fr):
    grid = collections.defaultdict(list)
    for c in cells:
        u, v, w = to_frame(c, fr); grid[(round(u), round(v))].append(w)
    return {key: sum(ws) / len(ws) for key, ws in grid.items()}


def control_points(target, markers, goal=0.95, spacing=5, budget=80, smooth=0.05):
    """The markers, plus points added one batch at a time where the surface through the current points is worst,
    until `goal` of the piece's columns sit within a block of it."""
    points = list(markers)
    added = 0
    while True:
        surface = terrain.fit(points, smooth=smooth) if len(points) >= 4 else None
        errors = sorted(((abs(surface(u, v) - w) if surface else 99, (u, v, w)) for (u, v), w in target.items()),
                        reverse=True)
        share = sum(e <= 1.0 for e, _ in errors) / len(errors)
        if share >= goal or added >= budget:
            return points, surface, share, added
        batch = []
        for e, p in errors:
            if e <= 1.0 or len(batch) >= 6: break
            if all(math.hypot(p[0] - q[0], p[1] - q[1]) >= spacing for q in batch + points):
                batch.append(p)
        if not batch:
            return points, surface, share, added
        points += batch; added += len(batch)


# ---------------------------------------------------------------- the outline: the loft's edge, simplified
def _simplify(pts, tolerance):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]
    far, idx = -1, 0
    for k, p in enumerate(pts[1:-1], 1):
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / (math.hypot(dx, dy) or 1)
        if d > far: far, idx = d, k
    if far <= tolerance: return [a, b]
    return _simplify(pts[:idx + 1], tolerance)[:-1] + _simplify(pts[idx:], tolerance)


def _area(loop):
    return sum(loop[k][0] * loop[(k + 1) % len(loop)][1] - loop[(k + 1) % len(loop)][0] * loop[k][1]
               for k in range(len(loop))) / 2


def outline(target_keys, tolerance=1.5, min_hole=6):
    """The edge of the covered (u, v) cells as simplified loops: the outer one, and every hole bigger than
    `min_hole` square blocks. Edges run with the inside on their left, and at a corner where two loops touch the
    walk turns right, so touching loops stay apart."""
    covered = set(target_keys)
    outgoing = collections.defaultdict(list)
    for (u, v) in covered:
        for (du, dv), (a, b) in (((0, -1), ((u - .5, v - .5), (u + .5, v - .5))), ((1, 0), ((u + .5, v - .5), (u + .5, v + .5))),
                                 ((0, 1), ((u + .5, v + .5), (u - .5, v + .5))), ((-1, 0), ((u - .5, v + .5), (u - .5, v - .5)))):
            if (u + du, v + dv) not in covered: outgoing[a].append(b)
    used, loops = set(), []
    for start in list(outgoing):
        for first in list(outgoing[start]):
            if (start, first) in used: continue
            loop, prev, cur = [start], start, first
            used.add((start, first))
            while cur != start:
                loop.append(cur)
                d0 = (cur[0] - prev[0], cur[1] - prev[1])
                options = [n for n in outgoing[cur] if (cur, n) not in used]
                if not options: break
                def turn(n):
                    d1 = (n[0] - cur[0], n[1] - cur[1]); cross = d0[0] * d1[1] - d0[1] * d1[0]
                    return 0 if cross < 0 else 1 if cross == 0 else 2
                nxt = min(options, key=turn)
                used.add((cur, nxt)); prev, cur = cur, nxt
            loops.append(loop)
    loops = [l for l in loops if len(l) >= 4]
    outer = max(loops, key=_area)
    holes = [l for l in loops if _area(l) < -min_hole]

    def simplify_loop(loop):
        half = len(loop) // 2
        return _simplify(loop[:half + 1], tolerance)[:-1] + _simplify(loop[half:] + [loop[0]], tolerance)[:-1]
    return [simplify_loop(outer)] + [simplify_loop(h) for h in holes]


def _in_loop(poly, x, y):
    hit = False
    for k in range(len(poly)):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): hit = not hit
    return hit


def inside(loops, x, y):
    return _in_loop(loops[0], x, y) and not any(_in_loop(h, x, y) for h in loops[1:])


# ---------------------------------------------------------------- thickness and the build
def thickness(cells, fr, surface, description=None):
    """The offset window off the surface that rebuilds the piece best: centred on the median offset, as wide as
    gives the highest overlap with the piece."""
    offsets = sorted(to_frame(c, fr)[2] - surface(*to_frame(c, fr)[:2]) for c in cells)
    centre = offsets[len(offsets) // 2]
    if description is None: return centre - 0.5, centre + 0.5
    best = None
    for width in (0.0, 0.5, 1.0, 1.5, 2.0):
        trial = dict(description, thickness=(centre - width / 2, centre + width / 2))
        blocks = build_sheet(trial)
        iou = len(blocks & cells) / len(blocks | cells)
        if best is None or iou > best[0]: best = (iou, trial["thickness"])
    return best[1]


def build_sheet(description, step=0.4):
    """Blocks from a description: every (u, v) inside the outline, from the surface's low offset to its high one."""
    fr, surface, poly, (lo, hi) = description["frame"], description["surface"], description["outline"], description["thickness"]
    us = [p[0] for p in poly[0]]; vs = [p[1] for p in poly[0]]
    out = set()
    u = min(us)
    while u <= max(us):
        v = min(vs)
        while v <= max(vs):
            if inside(poly, u, v):
                w0 = surface(u, v)
                o = lo
                while o <= hi + 1e-9:
                    x, y, z = from_frame(u, v, w0 + o, fr)
                    out.add((math.floor(x + 0.5), math.floor(y + 0.5), math.floor(z + 0.5)))
                    o += 0.5
            v += step
        u += step
    return out


def describe(piece):
    cells = list(piece["cells"])
    fr = frame(cells)
    target = mid_surface(cells, fr)
    markers = [to_frame(p, fr) for p, _ in piece["marks"]]
    points, surface, share, added = control_points(target, markers)
    loops = outline(target.keys())
    d = {"colour": piece["colour"], "frame": fr, "surface": surface, "outline": loops, "markers": len(markers),
         "added": added, "points": len(points), "outline_points": sum(map(len, loops)), "holes": len(loops) - 1,
         "surface_share": share, "control": points}
    d["thickness"] = thickness(cells, fr, surface)
    d["thickness"] = thickness(set(piece["cells"]), fr, surface, d)
    return d


def score(original, rebuilt):
    near = lambda c, s: any((c[0] + a, c[1] + b, c[2] + e) in s for a in (-1, 0, 1) for b in (-1, 0, 1) for e in (-1, 0, 1))
    exact = len(original & rebuilt) / len(original | rebuilt)
    recall = sum(near(c, rebuilt) for c in original) / len(original)
    precision = sum(near(c, original) for c in rebuilt) / len(rebuilt)
    return exact, recall, precision
