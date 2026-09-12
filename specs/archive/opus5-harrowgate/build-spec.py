#!/usr/bin/env python3
"""Harrowgate — one board using every piece of relief vocabulary this branch added.

Each statement does one job and no two do the same one:

  moor    a line with a TREAD — high ground whose front edge grades into the slope below it
  shelf   an AREA MARK WITH A HEIGHT PER CORNER and a BEVEL — a tilted bench cut into that slope,
          which could not be stated at all before: a held pad was level whatever it was drawn as
  scarp   a SCARP — the deliberate cliff. Not everything should grade, and a face is what decides
          where players go
  stair   a switchback line with a TREAD and a BATTER — the one way up the scarp, flat road and
          benched bank rather than a wall
  field   a broad AREA at one height with a BEVEL — the flat the map is fought on, graded at its rim
          into the scarp's toe and the river's bank. Its interior is what keeps RL5 quiet
  bank    the river's shoulder, TREAD 4
  ghyll   the river's bed, TREAD 3 — bed and bank grading into each other is what makes a V the
          water can fill to, instead of a flat trench it faces air across
  knoll   a PUSH — the sculpting half. It composes over the solved field instead of pinning it, so
          the field stays flat underneath and the knoll is a landform rather than a constraint

Authored for the -z half; rot_180 folds it. Writes the plan and finish beside this file.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-harrowgate"

BED, POOL, BANK, FIELD, SCARP_TOP, SHELF, MOOR, CREST = 8, 13, 17, 22, 32, 34, 40, 44

marks = []

# ── the high ground at the back, and the slope off its front ─────────────────────────────────
marks.append({"id": "moor", "kind": "line", "r": 15, "tread": 6,
              "points": [[-46, -82], [0, -86], [46, -82]], "h": [MOOR, CREST, MOOR]})

# ── the bench, cut into that slope. Four corners, not one height: it falls the way the hill does
#    rather than sitting on it as a level pad, and the bevel grades its rim into the hillside
#    instead of ending on the right angle a ring used to leave at each of its corners. ─────────
marks.append({"id": "shelf", "kind": "area", "bevel": 6,
              "ring": [[10, -70], [44, -68], [44, -54], [10, -56]],
              "h": [SHELF + 2, SHELF + 1, SHELF - 3, SHELF - 2]})

# ── the cliff. A scarp states a DROP, not a height, so this is the one edge on the board that is
#    meant to be a wall — 10 blocks over a 3-block face is not crossed on foot either way. ─────
marks.append({"id": "scarp", "kind": "scarp", "points": [[-54, -52], [54, -52]],
              "high": SCARP_TOP, "low": FIELD, "face": 3, "band": 10})

# ── the way up it: three limbs, 12 apart, falling 5 between each. A tread of 3 leaves 6 blocks of
#    run, which grades at 40 degrees left alone; the batter takes it to 58 and puts a bench at each
#    toe, which is what a cut stair through a scarp actually looks like. ────────────────────────
marks.append({"id": "stair", "kind": "line", "r": 8, "tread": 3, "batter": 58,
              "points": [[-40, -62], [-14, -60], [-12, -50], [-38, -48], [-36, -38], [-12, -36]],
              "h": [SCARP_TOP, 30, 27, 25, 23, FIELD]})

# ── the gate's own standing ground: a small tilted pad on the scarp face, bevelled into the stair
#    that reaches it. Without it the monument stands on the stair's own crown and WX11 fills the
#    face beside it with bedrock — a wall a player cannot climb and nobody drew. ─────────────────
marks.append({"id": "gatepad", "kind": "area", "bevel": 4,
              "ring": [[-38, -57], [-16, -57], [-16, -41], [-38, -41]],
              "h": 26})

# ── the flat the map is fought on. One height, a wide bevel: the middle is level ground and the
#    rim grades into the scarp's toe on one side and the river's bank on the other. ─────────────
marks.append({"id": "field", "kind": "area", "bevel": 5,
              "ring": [[-52, -48], [52, -48], [52, -20], [-52, -20]], "h": FIELD})

# ── the water's two statements, each with a tread so they grade into one another and leave a V ──
marks.append({"id": "bank", "kind": "line", "r": 9, "tread": 4,
              "points": [[-54, -15], [-18, -12], [18, -14], [54, -11]],
              "h": [BANK, BANK - 1, BANK - 1, BANK]})
marks.append({"id": "ghyll", "kind": "line", "r": 6, "tread": 3,
              "points": [[-54, 0], [-16, -3], [16, 3], [54, 0]], "h": [BED + 1, BED, BED, BED + 1]})

# ── and one push: a knoll on the field. A push composes over the solved surface rather than
#    pinning it, so the field stays flat under it and this is a landform, not a statement. ──────
pushes = [{"id": "knoll", "ring": [[24, -40], [40, -40], [40, -28], [24, -28]],
           "amount": 5, "falloff": 11, "roughness": 0.25, "crown": 2, "seed": 5}]

finish = {
    "authors": ["Opus 5"], "created": "2026-09-05",
    "relief": {"*": {"base": FIELD, "reach": 0, "step": 1, "landform": "rolling",
                     "grain": {"amplitude": 0.7, "scale": 19, "seed": 11},
                     "marks": marks, "pushes": pushes}},
    "addShapes": [],
    "themes": {}, "mapTheme": "harrow",
    "dressing": {"props": [
        {"id": "river", "kind": "water", "shape": "channel", "level": POOL, "depth": 4,
         "points": [[-54, 0], [-16, -3], [16, 3], [54, 0]], "radius": 11},
    ]},
}


def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}
def cell(a, b, size): return {"kind": "cell", "cellSize": size, "palette": [solid(*a), solid(*b)]}
def over(top, soil=solid(3), depth=2):
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": soil, "thickness": depth}]}}


# The angle mask. Cuts to be re-read off `GET …/incline` once it is built — this board has a scarp
# in it, so its distribution is not the one the last two settled on.
MASK = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": over(cell((2,), (2,), 15)), "thickness": 30},       # moor and field, 0-29
    {"material": over(solid(3, 1)), "thickness": 15},                # the worn shoulder, 30-44
    {"material": cell((1,), (4,), 9), "thickness": 45}]}}            # the scarp and the banks, 45+

BEDS = {"kind": "layered", "layers": [
    {"material": solid(1), "thickness": 3}, {"material": solid(1, 5), "thickness": 1},
    {"material": solid(1), "thickness": 4}, {"material": solid(13), "thickness": 1},
    {"material": solid(1, 3), "thickness": 2}, {"material": solid(4), "thickness": 2}]}

finish["themes"] = {
    "harrow": {"bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
               "wallOnTerrainFaces": True,
               "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
               "surface": {"material": MASK, "depth": 3, "enabled": True},
               "wall": {"kind": "wallRun", "runs": [{"material": BEDS, "width": 6}]},
               "wallEnabled": True, "fill": solid(1, 5)},
}
finish["themeByHeight"] = {}

plan = {
    "plan": 2, "meta": {"name": "Harrowgate"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": FIELD, "observerY": 76},
    "pieces": [
        {"id": "fell",  "role": "spawn", "rect": [-5, -44, 10, 6], "surface": CREST},
        {"id": "west",  "role": "piece", "rect": [-27, -38, 27, 38], "surface": FIELD},
        {"id": "east",  "role": "piece", "rect": [0, -38, 27, 38], "surface": FIELD},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "fell", "at": [10, 6], "facing": "back"}],
        "destroyables": [
            {"id": "dt-shelf", "piece": "east", "at": [32, 16], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Harrow"},
            {"id": "dt-gate", "piece": "west", "at": [28, 26], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Gate"},
        ],
    },
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)
print(f"{len(marks)} marks, {len(pushes)} push, {len(plan['pieces'])} pieces a side")
