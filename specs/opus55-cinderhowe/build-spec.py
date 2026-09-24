"""Cinderhowe — a caldera on the axis of the board, breached twice, with the monument in its floor.

Plan: one field and a spawn at one height (20), fused into `field-20`, rounded point by point into a
lobed island. Relief in four layers — the crater (a floor and a closed rim line whose per-vertex heights
open a breach toward each spawn), the strand and the spawn's bench, parasitic cones on the outer flank,
and a lava tongue out of the east breach. Unthemed. Team 0 is authored on x < 0; rot_180 fans it.
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
    "plan": 2, "meta": {"name": "Cinderhowe"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
    "pieces": [{"id": "spawn", "role": "spawn", "rect": [-35, -2, 5, 4]},
               {"id": "field", "role": "piece", "rect": [-30, -16, 26, 32]}],
    "zones": [{"id": "strait", "rect": [-4, -16, 8, 32], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "red-spawn", "piece": "spawn", "at": [10, 8], "facing": "right"}],
        # blocks from the field's corner (-120, -64): (-66, 4), in the caldera's floor
        "destroyables": [{"id": "red-monument", "piece": "field", "at": [54, 68],
                          "style": "pillar-3", "materials": "obsidian", "float": 4}]},
    "walls": []}

# The compiled ring: 0 (-140,-8) 1 (-120,-8) 2 (-120,-64) 3 (-16,-64) 4 (-16,64) 5 (-120,64) 6 (-120,8) 7 (-140,8)
edits = outline_ops(
    moves={1: (-132, -24), 2: (-108, -58), 5: (-108, 58), 6: (-132, 24)},
    inserts={1: [(-126, -44)],
             2: [(-88, -72), (-62, -80), (-38, -74)],
             4: [(-36, 76), (-60, 82), (-86, 72)],
             5: [(-126, 44)]})

CX, CZ, RIM_R = -70, 0, 26


def rim_line():
    """A closed ring of the rim's crest: 32 at every vertex but the two breaches — east-south-east toward
    the strait, and west toward the spawn — with their shoulders in between."""
    n = 24
    pts, hs = [], []
    for i in range(n + 1):
        a = 2 * math.pi * (i % n) / n
        pts.append([round(CX + RIM_R * math.cos(a), 1), round(CZ + RIM_R * math.sin(a), 1)])
        east = min(abs(i % n - 1), n - abs(i % n - 1))       # the breach at 15 degrees
        west = min(abs(i % n - 12), n - abs(i % n - 12))     # the breach at 180 degrees
        h = 38
        if east == 0: h = 15
        elif east == 1: h = 27
        if west == 0: h = 24
        elif west == 1: h = 31
        hs.append(h)
    return pts, hs


RIM_PTS, RIM_H = rim_line()

relief = {"team": {
    "base": 16, "reach": 0, "step": 1,
    "marks": [
        # layer 1 — the crater: its floor, and the rim as one closed line with the breaches in its heights
        {"id": "floor", "kind": "area", "h": 13, "bevel": 0, "ring": ellipse(CX, CZ, 14, 14, 16)},
        {"id": "rim", "kind": "line", "points": RIM_PTS, "h": RIM_H, "r": 4},
        # layer 2 — the spawn's bench and the strand
        {"id": "spawn-bench", "kind": "area", "h": 24, "bevel": 0, "ring": rect(-144, -14, -116, 14)},
        {"id": "strand", "kind": "area", "h": 14, "bevel": 0, "ring": rect(-24, -100, -8, 100)},
    ],
    "pushes": [
        # layer 3 — parasitic cones on the outer flank
        {"id": "cone-nw", "ring": ellipse(-112, -46, 7, 7, 12), "amount": 12, "falloff": 14, "crown": 8,
         "roughness": 0, "seed": 1},
        {"id": "cone-ne", "ring": ellipse(-34, -54, 5, 5, 10), "amount": 7, "falloff": 10, "crown": 5,
         "roughness": 0, "seed": 2},
        {"id": "cone-s", "ring": ellipse(-40, 56, 6, 6, 10), "amount": 9, "falloff": 12, "crown": 6,
         "roughness": 0, "seed": 3},
        # layer 4 — the lava tongue out of the east breach, a low raised flow toward the strait
        {"id": "tongue", "ring": ellipse(-30, 18, 14, 5, 16, 0.35, 2, 0.1), "amount": 4, "falloff": 6,
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
