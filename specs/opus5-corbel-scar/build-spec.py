#!/usr/bin/env python3
"""Corbel Scar — Scarrow Delph's concept, restated with as few marks as it takes.

The board is an ordering experiment before it is a map. Three facts decided every line of it, each
measured on a probe board before anything here was written:

  1. A HELD SHAPE IS A FLAT PAD, WHATEVER IT WAS DRAWN AS.  A sketch polygon's `anchor_heights`
     describe a full surface over its ring, and the relief path reads that surface at ONE point —
     the ring's centroid — because `AreaMark` carries a single height. So a shelf laid on a slope
     comes out level whichever way it is bound, and a sloped shelf cannot be stated as a shape at
     all. It cuts down as readily as it lifts, which the earlier note here had wrong: `hold` and
     `exclude` both write their height over whatever the field solved to. What they cannot do is
     tilt. That is the order: base, then dig, then place.
  2. ONLY A `line` MARK CAN TILT.  A point, an area and a rim state one height; a line states one per
     point. So the pit and any graded terrace are line marks, and an `area` is only ever a flat pad.
  3. A SPIRAL LINE IS A WHOLE QUARRY.  One mark whose radius shrinks as it winds cuts the benches and
     the road down them together, walkable at worst step 1 — where four nested area rings plus a
     twenty-one-point haul road are five marks that leave a blade of uncut ground between them.

Writes corbel-scar.plan.json and .finish.json beside this file.
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-corbel-scar"

BED, BANK, MID, CREST = 10, 14, 22, 36        # bed, bank, the field, the knoll          # the four heights the board is built out of
PIT_TOP, PIT_FLOOR = 26, 12
PAD, SHELF_HI, SHELF_LO = 17, 24, 18


def spiral(cx, cz, r0, r1, turns, n, start_deg=90.0):
    return [[round(cx + (r0 + (r1 - r0) * i / n) * math.cos(math.radians(start_deg) + 2 * math.pi * turns * i / n), 2),
             round(cz + (r0 + (r1 - r0) * i / n) * math.sin(math.radians(start_deg) + 2 * math.pi * turns * i / n), 2)]
            for i in range(n + 1)]


# ── the base: four line marks and nothing else ────────────────────────────────────────────────
marks = [
    # the knoll the spawn stands on, and the fall off it onto the field
    {"id": "crest", "kind": "line", "r": 18,
     "points": [[-34, -84], [0, -90], [34, -84]], "h": [30, CREST, 30]},
    # the bank above the water
    {"id": "bank", "kind": "line", "r": 10,
     "points": [[-54, -24], [-20, -21], [20, -21], [54, -24]], "h": [BANK + 2, BANK, BANK, BANK + 2]},
    # the channel itself, drawn symmetric about the origin so its own image lands on it
    {"id": "channel", "kind": "line", "r": 7,
     "points": [[-54, 0], [0, 0], [54, 0]], "h": [BED + 1, BED, BED + 1]},
]

# ── the way off the knoll. SP8 refuses a spawn whose piece drops onto the next in one step, and it
#    is right: 36 to 22 over the seam is a cliff out of the door. Stated as a line it is the lane.
marks.append({"id": "spine", "kind": "line", "r": 7,
              "points": [[0, -92], [0, -84], [1, -72], [0, -58], [-1, -44], [0, -30], [0, -22]],
              "h": [CREST, 33, 29, 25, 21, 17, BANK]})

# ── the quarry: ONE mark. The radius shrinks as it winds, so the turns lie beside one another and
#    the ramp between them is the way down. ──────────────────────────────────────────────────────
PIT = (-32, -56)
_pts = spiral(*PIT, r0=21, r1=5, turns=2.5, n=44)
marks.append({"id": "delph", "kind": "line", "r": 5,
              "points": _pts,
              # the last six samples run level, so the sump is a floor rather than the end of a ramp
              # and the monument does not stand two courses over the cell beside it (WX11)
              "h": [round(PIT_TOP + (PIT_FLOOR - PIT_TOP) * min(i, len(_pts) - 7) / (len(_pts) - 7), 2)
                    for i in range(len(_pts))]})

# ── the terrace. Stated as a WIDE LINE, not as a polygon with anchor heights, and the difference is
#    the whole ordering lesson. A shape only ever RAISES: an excluded polygon appears where its own
#    height beats what the board would otherwise have there and is swallowed everywhere else, and no
#    mark underneath changes that — measured identical at base 20 and base 12, with and without a pad
#    dug to 17 under it, against the tilt asked for. A line mark states a height per point, so it
#    tilts; and it is part of the solve, so it pulls the ground down to meet it as readily as up.
marks.append({"id": "terrace", "kind": "line", "r": 13,
              "points": [[10, -66], [28, -58], [44, -46]], "h": [SHELF_HI, 21, SHELF_LO]})

finish = {
    "authors": ["Opus 5"], "created": "2026-09-05",
    "relief": {"*": {"base": MID, "reach": 0, "step": 1, "landform": "rolling",
                     "grain": {"amplitude": 0.6, "scale": 21, "seed": 41},
                     "marks": marks}},
    "addShapes": [],
    "themes": {}, "mapTheme": "scar-moor",
    "dressing": {"props": [
        {"id": "river", "kind": "water", "shape": "channel", "level": BED + 3, "depth": 3,
         "points": [[-54, 0], [-18, -3], [18, 3], [54, 0]], "radius": 9},
    ]},
}


def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}
def cell(a, b, size): return {"kind": "cell", "cellSize": size, "palette": [solid(*a), solid(*b)]}

BEDS = {"kind": "layered", "layers": [
    {"material": solid(1), "thickness": 3}, {"material": solid(1, 5), "thickness": 1},
    {"material": solid(1), "thickness": 4}, {"material": solid(13), "thickness": 1},
    {"material": solid(1, 3), "thickness": 2}, {"material": solid(4), "thickness": 2}]}

def theme(surface, depth=3):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
            "wallOnTerrainFaces": True, "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
            "surface": {"material": surface, "depth": depth, "enabled": True},
            "wall": {"kind": "wallRun", "runs": [{"material": BEDS, "width": 6}]},
            "wallEnabled": True, "fill": solid(1, 5)}

finish["themes"] = {
    "scar-moor": theme({"kind": "layered", "layers": [
        {"material": cell((2,), (2,), 15), "thickness": 1}, {"material": solid(3), "thickness": 2}]}),
    "scar-cut":  theme(cell((1,), (4,), 11), depth=2),
}
finish["themeByHeight"] = {}

# ── the plan: two pieces a side. The knoll is a spur off the field and touches it on its +z face
#    ALONE, which is what puts the hall's one door on the front — `PieceDoors.ForSpawn` ranks the
#    walls by how much board each meets and takes the two widest, so a piece touching land on three
#    sides is given a side door whatever its facing says. ──────────────────────────────────────
plan = {
    "plan": 2, "meta": {"name": "Corbel Scar"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": MID, "observerY": 70},
    "pieces": [
        {"id": "knoll", "role": "spawn", "rect": [-5, -48, 10, 6], "surface": CREST},
        {"id": "field", "role": "piece", "rect": [-27, -42, 54, 42], "surface": MID},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "knoll", "at": [10, 6], "facing": "back"}],
        "destroyables": [
            {"id": "dt-pit", "piece": "field", "at": [22, 28], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Scar"},
            {"id": "dt-shelf", "piece": "field", "at": [80, 26], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Corbel"},
        ],
    },
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)
print(f"{len(marks)} relief mark(s), {len(finish['addShapes'])} shape, "
      f"{len(finish['themes'])} themes, {len(plan['pieces'])} pieces a side")
