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

def closed_spline(points, samples=6):
    """A closed Catmull-Rom ring through the points."""
    n = len(points)
    out = []
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        for k in range(samples):
            t = k / samples
            out.append([0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t
                               + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                               + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)])
    return out


def even(ring, spacing):
    """The ring resampled at an even arc spacing, so a push's `amounts`, which are read by arc
    fraction, land on the vertices they are computed for."""
    closed = ring + [ring[0]]
    seg = [math.dist(closed[i], closed[i + 1]) for i in range(len(ring))]
    total = sum(seg)
    count = max(8, int(total / spacing))
    out, i, walked = [], 0, 0.0
    for k in range(count):
        target = total * k / count
        while walked + seg[i] < target:
            walked += seg[i]
            i += 1
        t = (target - walked) / seg[i] if seg[i] else 0
        a, b = closed[i], closed[i + 1]
        out.append([round(a[0] + (b[0] - a[0]) * t, 1), round(a[1] + (b[1] - a[1]) * t, 1)])
    return out


# The tableland: one push over a ring whose east side is the rim, curving with the ground below it,
# and whose back runs off the board. Its lift is 12 everywhere but where the rim falls to the pass,
# so the table itself sags into a collapsed descent rather than being cut by a ramp.
RIM = [[-100, -100], [-96, -70], [-104, -46], [-96, -26], [-86, -8], [-88, 10], [-80, 30],
       [-90, 52], [-98, 76], [-94, 100]]
TABLE = even(closed_spline(RIM + [[-176, 104], [-176, -104]]), 3)
PASS = (-102, -42)


def table_lift(x, z):
    reach = math.dist((x, z), PASS)
    if reach >= 18:
        return 12
    t = reach / 18
    return round(3 + 9 * t * t * (3 - 2 * t), 1)


TABLE_AMOUNTS = [table_lift(x, z) for x, z in TABLE]

CANYON = [[-60, -84], [-66, -50], [-56, -24], [-62, -4], [-54, 26], [-62, 54], [-58, 84]]
CANYON_N = [[-60, -84], [-66, -50], [-56, -24], [-62, -8]]
CANYON_S = [[-60, 8], [-54, 26], [-62, 54], [-58, 84]]
LIP = [[-22, -100], [-18, -72], [-27, -46], [-20, -20], [-29, 4], [-20, 30], [-25, 56], [-18, 82],
       [-22, 100]]

relief = {"team": {
    "base": 24, "reach": 0, "step": 1,
    "grain": {"amplitude": 1.5, "scale": 14, "seed": 11},
    "marks": [
        # layer 1 — the frame: the spawn's footing (the tableland's push lifts it to 38), the
        # monument's shelf, and a lip that wanders in both course and height
        {"id": "spawn-footing", "kind": "area", "h": 26, "bevel": 0, "ring": rect(-136, -14, -108, 14)},
        {"id": "monument-shelf", "kind": "area", "h": 26, "bevel": 3, "ring": ellipse(-72, -12, 7, 6, 12, 0.3)},
        {"id": "lip", "kind": "line", "points": LIP, "h": [21, 23, 20, 24, 22, 25, 21, 23, 22], "r": 2},
    ],
    "pushes": [
        # layer 2 — the tableland, sagging to the pass
        {"id": "tableland", "ring": TABLE, "amounts": TABLE_AMOUNTS, "amount": 12, "falloff": 4,
         "crown": 0, "roughness": 2, "seed": 7},
        # the table's own swell, so its top rolls rather than reading as one level
        {"id": "table-swell", "ring": ellipse(-126, 50, 18, 16, 16, 0.4, 3, 0.1), "amount": 4, "falloff": 18,
         "crown": 3, "roughness": 0, "seed": 13},
        # layer 3 — the bench's own swells and one pan, so it rolls between the rim and the lip
        {"id": "swell-n", "ring": ellipse(-46, -44, 20, 14, 16, 0.3, 3, 0.1), "amount": 5, "falloff": 16,
         "crown": 3, "roughness": 0, "seed": 8},
        {"id": "swell-s", "ring": ellipse(-42, 40, 16, 20, 16, -0.2, 3, 0.1), "amount": 4, "falloff": 14,
         "crown": 3, "roughness": 0, "seed": 9},
        {"id": "pan", "ring": ellipse(-78, 34, 9, 7, 12, 0.5), "amount": -3, "falloff": 10, "crown": 0,
         "roughness": 0, "seed": 10},
        # layer 4 — the canyon, two pushes deep: a wide shallow trough the whole length, which is the
        # crossing where it is alone, and a slot inside it in two reaches, so each wall has a ledge
        {"id": "trough", "ring": band_ring(CANYON, 9), "amount": -4, "falloff": 3, "crown": 0,
         "roughness": 2, "seed": 5},
        {"id": "slot-n", "ring": band_ring(CANYON_N, 4), "amount": -8, "falloff": 3, "crown": 0,
         "roughness": 1.5, "seed": 6},
        {"id": "slot-s", "ring": band_ring(CANYON_S, 4), "amount": -8, "falloff": 3, "crown": 0,
         "roughness": 1.5, "seed": 12},
        # the buttes: crownless, on short rough falloffs
        {"id": "butte-n", "ring": ellipse(-36, -32, 7, 6, 12, 0.4, 3, 0.1), "amount": 12, "falloff": 3,
         "crown": 0, "roughness": 1.5, "seed": 1},
        {"id": "butte-s", "ring": ellipse(-30, 34, 5, 6, 12, -0.3, 3, 0.1), "amount": 10, "falloff": 3,
         "crown": 0, "roughness": 1.5, "seed": 2},
        {"id": "needle", "ring": ellipse(-42, 10, 3, 5, 10, 0.6), "amount": 8, "falloff": 2,
         "crown": 0, "roughness": 1, "seed": 3},
        {"id": "outlier", "ring": ellipse(-78, -50, 7, 6, 12, 0.2, 3, 0.1), "amount": 9, "falloff": 3,
         "crown": 0, "roughness": 1.5, "seed": 4},
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
