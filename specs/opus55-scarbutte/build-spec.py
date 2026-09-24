"""Scarbutte — a tableland whose rim breaks off onto a bench of buttes, split by a slot canyon.

Plan: one field and a spawn at one height (20), fused into `field-20`. The outline is bitten by two
canyon-mouth bays. Relief in four layers — the rim (one scarp per run, broken where the road comes
down), the bench and the lip, the canyon (a line mark with a ford where it shallows), and flat-topped
buttes (crownless pushes on short falloffs). Unthemed. Team 0 is authored on x < 0; rot_180 fans it.
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
    "plan": 2, "meta": {"name": "Scarbutte"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
    "pieces": [{"id": "spawn", "role": "spawn", "rect": [-33, -2, 5, 4]},
               {"id": "field", "role": "piece", "rect": [-28, -15, 24, 30]}],
    "zones": [{"id": "strait", "rect": [-4, -15, 8, 30], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "red-spawn", "piece": "spawn", "at": [10, 8], "facing": "right"}],
        # blocks from the field's corner (-112, -60): (-72, -12), on the bench below the rim
        "destroyables": [{"id": "red-monument", "piece": "field", "at": [40, 48],
                          "style": "pillar-3", "materials": "obsidian", "float": 4}]},
    "walls": []}

# The compiled ring: 0 (-132,-8) 1 (-112,-8) 2 (-112,-60) 3 (-16,-60) 4 (-16,60) 5 (-112,60) 6 (-112,8) 7 (-132,8)
edits = outline_ops(
    moves={1: (-128, -26), 6: (-128, 26)},
    inserts={1: [(-122, -48)],
             2: [(-96, -66), (-72, -58), (-62, -76), (-50, -70), (-30, -64)],
             4: [(-26, 62), (-40, 40), (-52, 38), (-60, 58), (-90, 64)],
             5: [(-122, 48)]})

RIM = dict(high=38, low=26, face=2, band=4)
CANYON_N = [[-60, -84], [-66, -50], [-56, -24], [-62, -8]]
CANYON_S = [[-60, 8], [-54, 26], [-62, 54], [-58, 84]]
BENCH = [[-90, -90], [-36, -90], [-36, 90], [-92, 90], [-76, 40], [-82, 16], [-70, 10], [-70, -8],
         [-80, -14], [-92, -40]]

relief = {"team": {
    "base": 24, "reach": 0, "step": 1,
    "marks": [
        # layer 1 — the rim: the tableland's edge, one scarp per straight run, high side west,
        # open between z -10 and 12 where the relaxation grades the road down
        {"id": "rim-1", "kind": "scarp", "points": [[-98, -84], [-100, -40]], **RIM},
        {"id": "rim-2", "kind": "scarp", "points": [[-100, -40], [-88, -10]], **RIM},
        {"id": "rim-3", "kind": "scarp", "points": [[-92, 12], [-84, 40]], **RIM},
        {"id": "rim-4", "kind": "scarp", "points": [[-84, 40], [-100, 84]], **RIM},
        {"id": "spawn-top", "kind": "area", "h": 38, "bevel": 0, "ring": rect(-136, -14, -108, 14)},
        # layer 2 — the bench's lip at the strait
        {"id": "lip", "kind": "area", "h": 22, "bevel": 0, "ring": rect(-24, -90, -8, 90)},
        # the bench itself, held at 26 from the rim's foot to twelve blocks short of the lip,
        # pulled back where the road comes down through the rim's gap
        {"id": "bench", "kind": "area", "h": 26, "bevel": 0, "ring": BENCH},
    ],
    "pushes": [
        # layer 3 — the slot canyon, carved twelve blocks into the bench after the solve, in two
        # reaches with the bench left whole between them at z -8..8 as the one crossing
        {"id": "canyon-n", "ring": band_ring(CANYON_N, 5), "amount": -12, "falloff": 1, "crown": 0,
         "roughness": 0, "seed": 5},
        {"id": "canyon-s", "ring": band_ring(CANYON_S, 5), "amount": -12, "falloff": 1, "crown": 0,
         "roughness": 0, "seed": 6},
        # layer 4 — buttes: flat tops, short falloffs, so each stands off the bench on a face
        {"id": "butte-n", "ring": ellipse(-36, -32, 7, 6, 12, 0.4, 3, 0.1), "amount": 12, "falloff": 3,
         "crown": 0, "roughness": 0, "seed": 1},
        {"id": "butte-s", "ring": ellipse(-30, 34, 5, 6, 12, -0.3, 3, 0.1), "amount": 10, "falloff": 3,
         "crown": 0, "roughness": 0, "seed": 2},
        {"id": "needle", "ring": ellipse(-42, 10, 3, 5, 10, 0.6), "amount": 8, "falloff": 2,
         "crown": 0, "roughness": 0, "seed": 3},
        {"id": "outlier", "ring": ellipse(-78, -50, 7, 6, 12, 0.2, 3, 0.1), "amount": 9, "falloff": 3,
         "crown": 0, "roughness": 0, "seed": 4},
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
