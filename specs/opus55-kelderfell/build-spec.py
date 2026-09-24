"""Kelderfell — a fellside falling to the strait, broken by a scarp with a pass in it.

Plan: one field and a spawn at one height (20), fused by the compile into one shape, `field-20`.
Ground: the outline reshaped point by point, then relief in five layers — a lean, a broken scarp,
a fell massif off the north-back corner, a south headland, and a tarn hollow with a knoll.
Unthemed. Team 0 is authored on x < 0; rot_180 fans it.
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


plan = {
    "plan": 2, "meta": {"name": "Kelderfell"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
    "pieces": [{"id": "spawn", "role": "spawn", "rect": [-33, -2, 5, 4]},
               {"id": "field", "role": "piece", "rect": [-28, -15, 24, 30]}],
    "zones": [{"id": "strait", "rect": [-4, -15, 8, 30], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "red-spawn", "piece": "spawn", "at": [10, 8], "facing": "right"}],
        # blocks from the field's corner (-112, -60): (-68, -18)
        "destroyables": [{"id": "red-monument", "piece": "field", "at": [44, 42],
                          "style": "pillar-3", "materials": "obsidian", "float": 4}]},
    "walls": []}

# The compiled ring: 0 (-132,-8) 1 (-112,-8) 2 (-112,-60) 3 (-16,-60) 4 (-16,60) 5 (-112,60) 6 (-112,8) 7 (-132,8)
edits = outline_ops(
    moves={1: (-132, -30), 2: (-120, -66), 5: (-116, 64), 6: (-130, 34)},
    inserts={1: [(-128, -50)],
             2: [(-96, -78), (-70, -72), (-44, -64), (-28, -58)],
             4: [(-30, 64), (-52, 50), (-68, 48), (-86, 62), (-102, 70)],
             5: [(-126, 48)]})

relief = {"team": {
    "base": 20, "reach": 0, "step": 1,
    "marks": [
        # layer 1 — the lean: the spawn's bench high at the back, the strand low at the lip
        {"id": "spawn-bench", "kind": "area", "h": 36, "bevel": 0, "ring": rect(-136, -14, -108, 14)},
        {"id": "strand", "kind": "area", "h": 12, "bevel": 0, "ring": rect(-24, -90, -8, 90)},
        # layer 2 — the scarp, one mark per straight run, broken at z -14..8 for the pass
        {"id": "scarp-n1", "kind": "scarp", "points": [[-114, -84], [-98, -40]], "high": 34, "low": 22, "face": 3, "band": 5},
        {"id": "scarp-n2", "kind": "scarp", "points": [[-98, -40], [-92, -14]], "high": 34, "low": 22, "face": 3, "band": 5},
        {"id": "scarp-s1", "kind": "scarp", "points": [[-88, 8], [-80, 36]], "high": 34, "low": 22, "face": 3, "band": 5},
        {"id": "scarp-s2", "kind": "scarp", "points": [[-80, 36], [-64, 84]], "high": 34, "low": 22, "face": 3, "band": 5},
        # a stair cut up the south run's face, a block of rise every two of run
        {"id": "south-stair", "kind": "line", "points": [[-70, 22], [-92, 22]], "h": [22, 34], "r": 2},
        # the monument's shelf, below the scarp
        {"id": "monument-shelf", "kind": "area", "h": 22, "bevel": 2, "ring": ellipse(-68, -18, 8, 8, 12)},
    ],
    "pushes": [
        # layer 3 — the fell: a massif centred past the north-back coast, so the board holds its flank
        {"id": "fell", "ring": ellipse(-134, -86, 36, 26, 18, 0.3, 3, 0.12), "amount": 18, "falloff": 20,
         "crown": 16, "roughness": 0, "seed": 1},
        # layer 4 — the south headland, lower and off the coast
        {"id": "headland", "ring": ellipse(-98, 68, 22, 12, 14, -0.2), "amount": 9, "falloff": 16,
         "crown": 7, "roughness": 0, "seed": 2},
        # layer 5 — detail: the tarn hollow on the strand, a knoll beside the monument
        {"id": "tarn", "ring": ellipse(-42, 30, 12, 8, 14, 0.4, 2, 0.15), "amount": -7, "falloff": 8,
         "crown": 0, "roughness": 0, "seed": 3},
        {"id": "knoll", "ring": ellipse(-52, -46, 7, 6, 12), "amount": 6, "falloff": 10, "crown": 4,
         "roughness": 0, "seed": 4},
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
