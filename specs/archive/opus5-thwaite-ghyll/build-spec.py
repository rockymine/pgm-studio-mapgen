#!/usr/bin/env python3
"""Thwaite Ghyll — a valley, built to find out what the new relief vocabulary can and cannot do.

Nothing here is a fix or a demonstration. It is a landscape authored cold against the three
mechanisms that landed this session, to see which of them compose and where the next fault is:

  1. THE ANGLE MASK finishes the ground by how steeply it falls rather than by how high it is,
     so the moor, the shoulder and the face of one hill take three materials from one stack.
  2. A LINE'S TREAD keeps a road flat while its shoulder grades, and a BATTER makes that grade
     steeper than the drawing would leave it. The ghyll road is a switchback, which is the shape
     that walls itself without one.
  3. A MARK'S SHOULDER blends into whatever an earlier mark pinned beside it, so the shelf can be
     cut into the hillside without a seam round it.

The board is a valley: high moor at the back of each side, a bench cut into the slope for the
monument, a road switchbacking down to the water, and a ghyll along the middle. Authored for the
-z half; rot_180 folds it.

Writes opus5-thwaite-ghyll.plan.json and .finish.json beside this file.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-thwaite-ghyll"

BED, POOL, BANK, SHELF, MOOR, CREST = 8, 12, 16, 26, 34, 42

marks = []

# ── the back of the board: high moor falling toward the water ────────────────────────────────
#    A tread of 6 on a reach of 16 leaves ten cells of shoulder, so the moor's front edge grades
#    into the slope rather than ending on it. Its own top stays flat, which is what a spawn wants.
marks.append({"id": "moor", "kind": "line", "r": 14, "tread": 6,
              "points": [[-48, -70], [0, -74], [48, -70]], "h": [MOOR, CREST, MOOR]})

# ── the bench the monument stands on: cut into the slope, three anchors so it already tilts ──
#    Stated as a line rather than an area because only a line states a height per point, and a
#    shelf that is dead level reads as a stamped pad. The tread holds the standing ground flat
#    and the six cells past it grade into the hillside the bench is cut from.
marks.append({"id": "shelf", "kind": "line", "r": 12, "tread": 7,
              "points": [[14, -52], [34, -44], [48, -34]], "h": [SHELF + 2, SHELF, SHELF - 3]})

# ── the road: a switchback down the western slope, moor to bank ──────────────────────────────
#    Three limbs. The pitch between them is what the batter has to work in: the limbs sit about
#    14 apart, a tread of 3 leaves 8 blocks of run, and the fall from one to the next is 9 — so
#    left alone it grades at 48 degrees and `batter` is stated only to put a bench at each toe.
marks.append({"id": "road", "kind": "line", "r": 7, "tread": 3, "batter": 58,
              "points": [[-44, -60], [-16, -57], [-14, -45], [-42, -42], [-40, -30], [-14, -27]],
              "h": [MOOR, 31, 28, 24, 21, BANK + 1]})

# ── the water's own two statements: the bank it runs between, and the bed it runs in ─────────
marks.append({"id": "bank", "kind": "line", "r": 9, "tread": 4,
              "points": [[-54, -16], [-18, -13], [18, -15], [54, -11]], "h": [BANK, BANK - 1, BANK - 1, BANK]})
marks.append({"id": "ghyll", "kind": "line", "r": 6, "tread": 3,
              "points": [[-54, 0], [-16, -3], [16, 3], [54, 0]], "h": [BED + 1, BED, BED, BED + 1]})

finish = {
    "authors": ["Opus 5"], "created": "2026-09-05",
    "relief": {"*": {"base": BANK, "reach": 0, "step": 1, "landform": "rolling",
                     "grain": {"amplitude": 0.8, "scale": 17, "seed": 7},
                     "marks": marks}},
    "addShapes": [],
    "themes": {}, "mapTheme": "ghyll",
    "dressing": {"props": [
        {"id": "river", "kind": "water", "shape": "channel", "level": POOL, "depth": 4,
         "points": [[-54, 0], [-16, -3], [16, 3], [54, 0]], "radius": 11},
    ]},
}


def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}
def cell(a, b, size): return {"kind": "cell", "cellSize": size, "palette": [solid(*a), solid(*b)]}


def over(top, soil=solid(3), depth=2):
    """A surfacing block one course thick over its soil — what every band of the mask carries."""
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": soil, "thickness": depth}]}}


# The angle mask. Cuts to be read back off `GET /map/{slug}/incline` once it is built, not guessed:
# these are the ones scarp-mask settled on and this board's distribution may not be the same.
MASK = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": over(cell((2,), (2,), 15)), "thickness": 30},        # moor, 0-29
    {"material": over(solid(3, 1)), "thickness": 15},                 # shoulder, 30-44
    {"material": cell((1,), (4,), 9), "thickness": 45}]}}             # face, 45+

BEDS = {"kind": "layered", "layers": [
    {"material": solid(1), "thickness": 3}, {"material": solid(1, 5), "thickness": 1},
    {"material": solid(1), "thickness": 4}, {"material": solid(13), "thickness": 1},
    {"material": solid(1, 3), "thickness": 2}, {"material": solid(4), "thickness": 2}]}

finish["themes"] = {
    "ghyll": {"bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
              "wallOnTerrainFaces": True,
              "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
              "surface": {"material": MASK, "depth": 3, "enabled": True},
              "wall": {"kind": "wallRun", "runs": [{"material": BEDS, "width": 6}]},
              "wallEnabled": True, "fill": solid(1, 5)},
}
finish["themeByHeight"] = {}

plan = {
    "plan": 2, "meta": {"name": "Thwaite Ghyll"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": BANK, "observerY": 74},
    "pieces": [
        {"id": "fell", "role": "spawn", "rect": [-5, -38, 10, 6], "surface": CREST},
        {"id": "west", "role": "piece", "rect": [-27, -32, 27, 32], "surface": BANK},
        {"id": "east", "role": "piece", "rect": [0, -32, 27, 32], "surface": BANK},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "fell", "at": [10, 6], "facing": "back"}],
        "destroyables": [
            {"id": "dt-shelf", "piece": "east", "at": [31, 18], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Thwaite"},
            {"id": "dt-ford", "piece": "west", "at": [23, 15], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Ghyll"},
        ],
    },
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)
print(f"{len(marks)} relief mark(s), {len(finish['themes'])} theme, {len(plan['pieces'])} pieces a side")
