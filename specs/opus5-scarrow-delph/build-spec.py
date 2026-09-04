#!/usr/bin/env python3
"""Scarrow Delph — a worked hillside quarry, written as a plan and a finish.

The board is terrain. Two hillsides face each other across a drowned valley; a benched delph is
cut into each, a haul road spirals down it, a gallery is cut into the other shoulder, and the
valley bottom is a flooded pit standing in void that both sides have to bridge to.

Everything vertical is stated in the relief: the moor, the lip, the benches, the gallery, the
haul road and the incline are marks; the spoil heaps are pushes. The plan is five rectangles.
"""

import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-scarrow-delph"
CELL = 2

# ── heights ───────────────────────────────────────────────────────────────────
MOOR      = 44   # the moor above the quarry, where the camp stands
LIP       = 42   # the overburden lip: the quarry's own rim
BENCH3    = 36   # the upper bench
BENCH2    = 30   # the lower bench
FLOOR     = 24   # the delph floor
GALLERY   = 32   # the shelf cut into the eastern shoulder
GALLERY_HI = 38  # the bench above it
SHOULDER  = 15   # the valley shoulder
BRINK     = 13   # the last land before the void
STRAND    = 10   # the flooded pit's shore
BEACH     =  9
PAN       =  4   # the drowned floor
WATERLINE =  8

BASE_TEAM = 30   # the height the plan draws the team's ground at
BASE_NEUT = 10

# ── the board, in blocks ──────────────────────────────────────────────────────
HALF_X    = 54    # the board runs x -54..54: wider and `max-chain-length` (LN2) leaves its band
BACK      = -110  # the moor's back edge
MOOR_S    = -86   # where the moor ends and the workings begin
BRINK_Z   = -26   # the last land before the void
ISLE_Z    = -16   # the flooded pit's north shore
ISLE_X    = 44

# ── the quarry, as nested rings (outward-in; a later mark wins the cell) ───────
Q_LIP    = (-52, -86, -4, -36)    # x0, z0, x1, z1 — four levels, 6 blocks apart, benches 5 wide
Q_BENCH3 = (-47, -81, -9, -41)
Q_BENCH2 = (-42, -76, -14, -46)
Q_FLOOR  = (-37, -71, -19, -51)
SHELF    = (  8, -74,  36, -46)   # the lower gallery, cut into the eastern shoulder
SHELF_HI = ( 34, -82,  54, -56)   # the bench above it

GOAL_PIT   = (-28, -60)
GOAL_SHELF = ( 22, -58)
SPAWN_AT   = (  0, -98)

# ── blocks ────────────────────────────────────────────────────────────────────
def b(i, d=0):   return {"kind": "solid", "id": i, "data": d}
STONE, ANDESITE, DIORITE = b(1), b(1, 5), b(1, 3)
COBBLE, MOSSY, GRAVEL    = b(4), b(48), b(13)
GRASS, COARSE, DIRT      = b(2), b(3, 1), b(3)
SPRUCE                   = b(5, 1)

def cell(seed, size, palette, jitter=55, warp=1, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "rise": rise, "palette": palette}

# One bedded stack, shared as the wall and the fill of every theme, so every cut on the board
# shows the same rock in the same order and banding by depth is banding by altitude.
STRATA = {"bands": [{"material": STONE,    "thickness": 3},
                    {"material": DIORITE,  "thickness": 1},   # a pale bed
                    {"material": STONE,    "thickness": 3},
                    {"material": GRAVEL,   "thickness": 1},   # a parting
                    {"material": ANDESITE, "thickness": 3},
                    {"material": COBBLE,   "thickness": 2},   # a rubbly bed
                    {"material": STONE,    "thickness": 4},
                    {"material": COARSE,   "thickness": 1},   # a shale parting
                    {"material": STONE,    "thickness": 5},
                    {"material": ANDESITE, "thickness": 2}],
          "ending": "repeat"}

def rock(bucket_seed):
    return {"kind": "layered", "stack": STRATA, "axis": "depth", "beyond": STONE}

def theme(surface_material, depth=3):
    return {"bedrock": {"relative": False, "value": 1},
            "wallOnTerrainFaces": True,
            "surface": {"enabled": True, "depth": depth, "material": surface_material},
            "wall": rock(1), "wallEnabled": True,
            "fill": rock(2),
            # the rim is off: it caps every fall with a band and turns solved ground into contours
            "rim": {"enabled": False, "depth": 1, "material": STONE},
            "rimEdges": "void"}

# Turf is one course thick and what is under it is soil (PT1), so the moor's skin is a layered
# stack whose top band is the brush: grass where the turf holds, bare coarse dirt where it does not.
TURF = {"kind": "layered", "axis": "depth", "beyond": DIRT,
        "stack": {"bands": [{"material": cell(3101, 17, [GRASS, GRASS, GRASS, COARSE]), "thickness": 1},
                            {"material": DIRT, "thickness": 2}],
                  "ending": "handOver"}}

THEMES = {
    # the ground: turf over gritstone, one brush, two members
    "gritstone": theme(TURF),
    # the workings: bare rock, stripped
    "workings":  theme(cell(3102, 12, [STONE, COBBLE]), depth=2),
    # the spoil: what was moved
    "spoil":     theme(cell(3103, 11, [GRAVEL, COARSE]), depth=2),
}

# ── plan ──────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]

plan = {
    "plan": 2,
    "meta": {"name": "Scarrow Delph",
             "notes": "A worked hillside quarry: benched delph, haul road, gallery, drowned pit."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24,
                "surface": BASE_TEAM, "observerY": 74},
    "pieces": [
        {"id": "moor-w", "role": "piece", "rect": cells(-HALF_X, BACK, -10, MOOR_S), "surface": BASE_TEAM},
        {"id": "camp",   "role": "spawn", "rect": cells(-10, BACK, 10, MOOR_S), "surface": BASE_TEAM},
        {"id": "moor-e", "role": "piece", "rect": cells(10, BACK, HALF_X, MOOR_S), "surface": BASE_TEAM},
        {"id": "works",  "role": "piece", "rect": cells(-HALF_X, MOOR_S, HALF_X, BRINK_Z), "surface": BASE_TEAM},
        {"id": "sump",   "role": "piece", "rect": cells(-ISLE_X, ISLE_Z, ISLE_X, -ISLE_Z),
         "surface": BASE_NEUT, "mirrors": False},
    ],
    "zones": [
        {"id": "crossing", "rect": cells(-HALF_X, -30, HALF_X, 30), "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "camp",
             "at": [10, 12],                       # blocks from the piece's min corner
             "facing": "back", "footprint": [2, 4, 16, 14]},
        ],
        "destroyables": [
            {"id": "dt-pit", "piece": "", "at": list(GOAL_PIT), "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Sump"},
            {"id": "dt-shelf", "piece": "", "at": list(GOAL_SHELF), "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Gallery"},
        ],
    },
}
# ── relief ────────────────────────────────────────────────────────────────────
def ring(box):
    x0, z0, x1, z1 = box
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]

def area(mid, box, h):
    return {"id": mid, "kind": "area", "ring": ring(box), "h": h}

def line(mid, pts, hs, r):
    return {"id": mid, "kind": "line", "points": [list(p) for p in pts], "h": hs, "r": r}

# The haul road: it leaves the spine at the brow, spirals the lip clockwise, doubles back along
# the upper bench and drops into the floor. Written after the benches, so it cuts their faces.
# 250 blocks of run for 17 of fall — 0.07 a block, which is what makes it a road and not a stair.
HAUL = [(-2, -84), (-14, -83), (-32, -83), (-47, -82), (-49, -70), (-49, -54),
        (-49, -42), (-42, -38), (-26, -38), (-12, -39), (-11, -46), (-11, -58),
        (-12, -70), (-14, -78), (-30, -79), (-42, -76), (-44, -66), (-44, -56),
        (-42, -49), (-32, -48), (-28, -54)]
HAUL_H = [41, LIP, LIP, 41, 40, 39,
          38, 37, 36, 35, 34, 33,
          32, 31, 30, 29, 28, 27,
          26, 25, FLOOR]

# The incline: the gallery's own way down to the valley shoulder, traversing the eastern face.
INCL = [(30, -48), (36, -42), (42, -36), (48, -31), (51, -28)]
INCL_H = [GALLERY, 27, 22, 17, SHOULDER - 1]

# The spine: the ramp down between the two workings, which is the board's main lane. Unstated,
# the relaxation holds it level with the lip and the shelf either side of it and then drops it
# 19 blocks in four cells at z -38..-34 — measured on the first build, at x=2.
SPINE = [(0, -88), (2, -76), (2, -62), (0, -50), (-2, -38), (-3, -29)]
SPINE_H = [43, 39, 34, 28, 21, SHOULDER + 1]

# The gallery ramp: the one graded way onto the shelf, off the spine between the two workings.
GRAMP = [(4, -60), (10, -59), (15, -58)]
GRAMP_H = [31, 32, GALLERY]

team_relief = {
    "base": BASE_TEAM,
    "reach": 0,               # the marks decide the whole surface: this board is all designed
    "step": 1,
    "stairs": True,
    "landform": "hills",
    "grain": {"amplitude": 0.7, "scale": 17, "seed": 771},
    "marks": [
        # the moor and its skyline
        line("crest", [(-54, -106), (-18, -104), (18, -105), (54, -103)],
             [MOOR + 3, MOOR + 2, MOOR + 2, MOOR + 3], 7),
        area("camp-pad", (-18, -108, 18, -88), MOOR),
        # the two works platforms: a quarry building stands on ground that was levelled for it
        area("pad-winder", (-34, -102, -14, -86), MOOR),
        area("pad-smithy", (14, -102, 34, -86), MOOR),
        line("brow", [(-54, -88), (-16, -86), (16, -86), (54, -88)],
             [MOOR, MOOR - 1, MOOR - 1, MOOR], 5),

        # the delph, outward-in: a later mark wins the cell, so the rings terrace
        area("q-lip",    Q_LIP,    LIP),
        area("q-bench3", Q_BENCH3, BENCH3),
        area("q-bench2", Q_BENCH2, BENCH2),
        area("q-floor",  Q_FLOOR,  FLOOR),

        # the eastern shoulder, cut as two galleries rather than left as a plateau
        area("shelf-hi", SHELF_HI, GALLERY_HI),
        area("shelf",    SHELF,    GALLERY),

        # the valley shoulder and the last land before the void
        line("shoulder", [(-54, -31), (-16, -30), (16, -30), (54, -31)],
             [SHOULDER + 1, SHOULDER, SHOULDER, SHOULDER + 1], 4),
        line("brink", [(-54, -27), (0, -27), (54, -27)], [BRINK, BRINK, BRINK], 2),

        # the roads, last, so they cut the faces they cross
        line("spine", SPINE, SPINE_H, 6),
        line("gallery-ramp", GRAMP, GRAMP_H, 3),
        line("incline", INCL, INCL_H, 4),
        line("haul", HAUL, HAUL_H, 3.5),
    ],
    "pushes": [
        {"id": "spoil-nw", "ring": ring((-54, -110, -42, -100)), "amount": 7,
         "falloff": 7, "roughness": 3.0, "crown": 3, "seed": 21},
        {"id": "spoil-ne", "ring": ring((42, -110, 54, -100)), "amount": 6,
         "falloff": 7, "roughness": 3.0, "crown": 3, "seed": 22},
        # the overburden tipped over the delph's own south face, down toward the valley
        {"id": "tip", "ring": ring((-40, -34, -12, -28)), "amount": 4,
         "falloff": 6, "roughness": 2.5, "crown": 2, "seed": 23},
    ],
}

neutral_relief = {
    "base": BASE_NEUT,
    "reach": 0,
    "step": 1,
    "stairs": False,
    "landform": "plain",
    "grain": {"amplitude": 0.5, "scale": 9, "seed": 772},
    "marks": [
        area("strand", (-ISLE_X, ISLE_Z, ISLE_X, -ISLE_Z), STRAND),
        area("beach",  (-38, -12, 38, 12), BEACH),
        area("pan",    (-32,  -8, 32,  8), PAN),
    ],
}

# ── the paint patches: one ground, and the few places that are something else ──
def patch(pid, verts, tid):
    """A theme scoped to a patch of ground: an ordinary one-course add, never an override."""
    return {"id": pid, "type": "polygon", "operation": "add",
            "vertices": [list(v) for v in verts], "floor": 0, "base_height": 1, "theme": tid}

def box_verts(box, inset=0):
    x0, z0, x1, z1 = box
    return [(x0 + inset, z0 + inset), (x1 - inset, z0 + inset),
            (x1 - inset, z1 - inset), (x0 + inset, z1 - inset)]

add_shapes = [
    patch("paint-delph", box_verts(Q_LIP), "workings"),
    patch("paint-shelf", box_verts(SHELF), "workings"),
    patch("paint-shelf-hi", box_verts(SHELF_HI), "workings"),
    patch("paint-spoil-nw", [(-54, -107), (-24, -105), (-22, -88), (-52, -87)], "spoil"),
    patch("paint-spoil-ne", [(22, -106), (52, -105), (52, -89), (23, -90)], "spoil"),
    # the quarry's own face over the valley, and the shoulder the crossing lands on
    patch("paint-face", [(-52, -40), (-2, -40), (2, -27), (-52, -27)], "workings"),
    # The loading stage stands on a quay, not on the falling shoulder: `hold` pins a shape at its
    # own top and lets the surface be solved knowing where it has to arrive, which is the one way
    # to state a level floor inside a relief. The same rectangle at `exclude` built no plate at all.
    {"id": "quay", "type": "rectangle", "operation": "add",
     "min_x": 0, "min_z": -41, "max_x": 16, "max_z": -29,
     "floor": 0, "base_height": 18, "relief_scope": "hold", "theme": "workings"},
]

# ── dressing ──────────────────────────────────────────────────────────────────
ROAD_PAVE = cell(4400, 5, [GRAVEL, COBBLE, GRAVEL])

with open(os.path.join(HERE, "..", "..", "tools", "styles", "rk-shed.json")) as _fh:
    STAGE_STYLE = json.load(_fh)
STAGE_STYLE["roof"]["slab"], STAGE_STYLE["roof"]["slabData"] = 44, 1
def stroke(sid, pts, radius, seed, pave=None, route=True, style="solid", coverage=1.0):
    return {"id": sid, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": route, "pave": pave or ROAD_PAVE,
            "points": [list(p) for p in pts]}

BANK = cell(4401, 6, [GRAVEL, COARSE])

props = [
    # the water: one pool, one stated level, the pan it fills drawn at the size of the water
    {"id": "tarn", "kind": "water", "seed": 91, "shape": "pool",
     "points": [[-40, -6], [-20, -7], [0, -7], [20, -7], [40, -6],
                [41, 0], [40, 6], [20, 7], [0, 7], [-20, 7], [-40, 6], [-41, 0]],
     "radius": 6, "depth": 4, "level": WATERLINE - 1, "shore": 3, "shoreWander": True,
     "bank": BANK},

    # the roads, paved over the ground the relief already graded
    stroke("road-haul", HAUL, 4.0, 41),
    stroke("road-incline", INCL, 3.5, 42),
    stroke("road-gallery", GRAMP, 3.0, 43),
    stroke("road-spine", [(0, -88), (2, -74), (1, -60), (0, -46), (-2, -34), (-4, -28)], 3.0, 44),

    # two buildings, both of the works, neither in the ground's own family
    {"id": "winder", "kind": "house", "seed": 201, "front": "posZ", "style": "@wh-stamps",
     "wings": [{"corners": [[-30, -98], [-18, -90]]}]},
    {"id": "smithy", "kind": "house", "seed": 202, "front": "negX", "style": "@wh-shed",
     "wings": [{"corners": [[18, -98], [30, -90]]}]},
    # rk-shed forked in place: its roof steps a sandstone body in spruce half-courses, which HS3
    # refuses — a half-course slab continues the body, so it takes the body's own material.
    {"id": "stage", "kind": "house", "seed": 204, "front": "posZ", "style": STAGE_STYLE,
     "wings": [{"corners": [[3, -38], [13, -32]]}]},
    {"id": "crusher", "kind": "house", "seed": 203, "front": "posX", "style": "@wh-shed",
     "wings": [{"corners": [[40, -76], [50, -68]]}]},
]

# spoil blocks: cut stone left on the benches and the heaps, placed, never scattered
for i, (bx, bz, size) in enumerate([(-44, -94, 3.0), (-52, -94, 2.5), (-38, -104, 3.5),
                                    (44, -96, 3.0), (34, -104, 2.5),
                                    (-50, -31, 2.5), (-34, -31, 3.0), (24, -86, 2.5),
                                    (48, -60, 3.0), (44, -80, 2.5)]):
    props.append({"id": f"blk{i}", "kind": "boulder", "seed": 500 + i, "x": bx, "z": bz,
                  "form": "angular", "size": size, "mossy": False,
                  "rock": cell(4402 + i, 5, [STONE, ANDESITE])})

# the moor's cover: rough grazing behind the works, nothing inside the quarry
for i, (tx, tz) in enumerate([(-52, -100), (-36, -107), (-24, -104), (24, -108),
                              (46, -106), (52, -92), (-44, -108), (36, -100)]):
    props.append({"id": f"tr{i}", "kind": "tree", "seed": 600 + i, "x": tx, "z": tz,
                  "form": "template", "species": "spruce", "height": 9 + (i % 4)})

props.append({"id": "fl-moor", "kind": "flora", "seed": 31,
              "points": [[-53, -109], [53, -109], [53, -88], [-53, -88]],
              "spec": {"coverage": 0.28, "scale": 11, "octaves": 2, "fernShare": 0.55,
                       "flowerShare": 0.1, "flowerScale": 12, "tallShare": 0.2}})

finish = {
    "themes": THEMES,
    "mapTheme": "gritstone",
    "addShapes": add_shapes,
    "relief": {"team": team_relief, "neutral": neutral_relief},
    # s1 is the neutral island the compile emits; `addShapes` can only reach group 0, so the
    # drowned pit is themed by its shape id rather than painted with a patch.
    "themeById": {"sump-10": "spoil"},
    "dressing": {"props": props},
    "biome": {"kind": "solid", "id": 3},
    "authors": ["Opus 5"],
    "created": "2026-09-03",
}

if __name__ == "__main__":
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as fh:
        json.dump(plan, fh, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as fh:
        json.dump(finish, fh, indent=1)
    print(f"wrote {SLUG}.plan.json ({len(plan['pieces'])} pieces) and "
          f"{SLUG}.finish.json ({len(props)} props, {len(THEMES)} themes)")
