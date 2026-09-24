"""Twingill — a dale between two ridges, its gill falling from the spawn's head to the strait.

Plan: one field and a spawn at one height (20), fused into `field-20`. The outline pinches at the dale
head and flares at the lip. Relief in four layers — the dale floor (a falling line mark) with the gill carved into it,
the two ridges (the southern one saddled), coombes bitten into the north ridge's inner flank, and the terraces a spawn and a
monument stand on. Unthemed. Team 0 is authored on x < 0; rot_180 fans it.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = os.path.basename(HERE)


def ellipse(cx, cz, rx, rz, n=16, turn=0.0, lobes=0, lobe=0.0):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + lobe * math.sin(lobes * a) if lobes else 1
        x, z = rx * k * math.cos(a), rz * k * math.sin(a)
        c, s = math.cos(turn), math.sin(turn)
        pts.append([round(cx + x * c - z * s, 1), round(cz + x * s + z * c, 1)])
    return pts


def rect(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def outline_ops(moves, inserts):
    """Vertex moves on the compiled ring first, then inserts edge by edge from the last edge back,
    so every index an op names is the index on the ring as it stands when the op runs."""
    ops = [{"index": i, "x": x, "z": z} for i, (x, z) in sorted(moves.items())]
    for edge in sorted(inserts, reverse=True):
        for k, (x, z) in enumerate(inserts[edge]):
            ops.append({"after": edge + k, "x": x, "z": z})
    return ops




def spline(points, samples=6):
    """Centripetal-free uniform Catmull-Rom through the points, so a band drawn along it bends
    rather than kinks."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(samples):
            t = k / samples
            out.append([0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t
                               + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                               + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)])
    out.append(list(points[-1]))
    return out


def band_ring(points, half):
    """The closed outline of a band `half` blocks either side of a course: one side out, the other back."""
    line = spline(points)
    left, right = [], []
    for i, (x, z) in enumerate(line):
        a = line[max(i - 1, 0)]
        b = line[min(i + 1, len(line) - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dz) or 1
        nx, nz = -dz / n, dx / n
        left.append([round(x + nx * half, 1), round(z + nz * half, 1)])
        right.append([round(x - nx * half, 1), round(z - nz * half, 1)])
    return left + right[::-1]


plan = {
    "plan": 2, "meta": {"name": "Twingill"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
    "pieces": [{"id": "spawn", "role": "spawn", "rect": [-33, -2, 5, 4]},
               {"id": "field", "role": "piece", "rect": [-28, -17, 24, 34]}],
    "zones": [{"id": "strait", "rect": [-4, -17, 8, 34], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "red-spawn", "piece": "spawn", "at": [10, 8], "facing": "right"}],
        # blocks from the field's corner (-112, -68): (-66, 20), on the south valley side
        "destroyables": [{"id": "red-monument", "piece": "field", "at": [46, 88],
                          "style": "pillar-3", "materials": "obsidian", "float": 4}]},
    "walls": []}

# The compiled ring: 0 (-132,-8) 1 (-112,-8) 2 (-112,-68) 3 (-16,-68) 4 (-16,68) 5 (-112,68) 6 (-112,8) 7 (-132,8)
edits = outline_ops(
    moves={1: (-126, -20), 2: (-104, -44), 5: (-104, 44), 6: (-126, 20)},
    inserts={1: [(-118, -36)],
             2: [(-84, -58), (-60, -62), (-38, -72)],
             4: [(-34, 74), (-56, 64), (-80, 60)],
             5: [(-116, 34)]})

GILL = [[-104, 0], [-94, 10], [-76, -4], [-58, 8], [-40, -6], [-24, 4], [-8, 0]]

relief = {"team": {
    "base": 18, "reach": 0, "step": 1,
    "grain": {"amplitude": 0, "scale": 16, "seed": 11},
    "marks": [
        # layer 1 — the dale floor: a line falling seventeen blocks from the head to the lip, wide
        # enough to be the valley's bottom rather than its stream
        {"id": "dale-floor", "kind": "line", "points": GILL, "h": [29, 26, 23, 20, 17, 14, 12], "r": 8},
        # layer 4 — the terraces: the spawn's bench at the head, the monument's on the south side
        {"id": "spawn-bench", "kind": "area", "h": 30, "bevel": 0, "ring": rect(-136, -14, -110, 14)},
        {"id": "monument-terrace", "kind": "area", "h": 24, "bevel": 2, "ring": ellipse(-66, 20, 9, 8, 12, 0.3)},
        {"id": "holm", "kind": "area", "h": 17, "bevel": 2, "ring": ellipse(-38, -24, 12, 9, 14, 0.2)},
    ],
    "pushes": [
        # layer 2 — the ridges: one long north ridge, a saddled pair on the south
        {"id": "north-ridge", "ring": ellipse(-78, -60, 54, 11, 20, -0.12, 3, 0.08), "amount": 14,
         "falloff": 20, "crown": 8, "roughness": 0, "seed": 1},
        {"id": "south-fell", "ring": ellipse(-100, 48, 24, 10, 14, 0.25), "amount": 16, "falloff": 18,
         "crown": 8, "roughness": 0, "seed": 2},
        {"id": "south-knott", "ring": ellipse(-44, 64, 20, 10, 14, -0.2), "amount": 12, "falloff": 16,
         "crown": 6, "roughness": 0, "seed": 3},
        # the gill itself, carved into the dale floor after the solve: four blocks deep, eight across
        {"id": "gill", "ring": band_ring(GILL[1:], 3), "amount": -4, "falloff": 2, "crown": 0,
         "roughness": 0, "seed": 8},
        # layer 3 — coombes bitten into the north ridge's inner flank
        {"id": "coombe-w", "ring": ellipse(-90, -46, 6, 10, 12, 0.2), "amount": -6, "falloff": 6,
         "crown": 0, "roughness": 0, "seed": 5},
        {"id": "coombe-e", "ring": ellipse(-54, -48, 6, 9, 12, -0.2), "amount": -6, "falloff": 6,
         "crown": 0, "roughness": 0, "seed": 6},
    ]}}

finish = {
    "created": "2026-09-24", "authors": ["Opus 5.5"],
    "editShapes": {"field-20": edits},
    "bendShapes": {"field-20": {"k": 0.22, "wander": 2, "step": 10, "seed": 5, "side": "out"}},
    "relief": relief}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)
print("wrote", SLUG)
