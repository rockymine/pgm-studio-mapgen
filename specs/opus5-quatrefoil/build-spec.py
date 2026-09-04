#!/usr/bin/env python3
"""Quatrefoil — a four-team capture board at the scale it was drawn.

The plan is the author's, at the author's `cell: 1`: 98 x 98 blocks, eleven rectangles, their ids and
their arrangement untouched. What is added here is what the plan cannot state — the build zones that
join nine islands, the paint, and the shaping.

**The shaping is piece heights and ramps, not relief.** The relief carries a grain and nothing else.
Every place the plan steps two blocks is an authored ramp over the piece that steps: the approach in
front of each wool room, the arm's inner run, and the flight onto the keep. A ramp is a `level` shape
with one anchor a vertex, so the ground it draws is exact rather than solved.

Writes <slug>.plan.json and <slug>.finish.json beside this file. Nothing here reads a built world.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-quatrefoil"
CELL = 1

# ── the palette ───────────────────────────────────────────────────────────────────────────────────
# Five colours the author named, resolved through `GET /api/terrain/blocks` to the nearest block that
# is ground rather than a stated shade — stained clay, wool and glass are shade rows, never terrain.
#   muted teal  #ABC4AB  mossy cobblestone #6e7b62 · prismarine brick #63a08f
#   camel       #A39171  coarse dirt #7e5a3c · sandstone #d9cfa1
#   pale oak    #DCC9B6  smooth sandstone #d8cea0 · sand #dbd3a0
#   grey        #727D71  mossy cobblestone · cobblestone #7a7a7a · stone brick · andesite
#   coffee bean #6D4C3D  podzol #5d421f · spruce planks #725430
MOSS      = {"kind": "solid", "id": 48,  "data": 0}
COBBLE    = {"kind": "solid", "id": 4,   "data": 0}
STONE     = {"kind": "solid", "id": 1,   "data": 0}
ANDESITE  = {"kind": "solid", "id": 1,   "data": 5}
BRICK     = {"kind": "solid", "id": 98,  "data": 0}
CHISELLED = {"kind": "solid", "id": 98,  "data": 3}
COARSE    = {"kind": "solid", "id": 3,   "data": 1}
DIRT      = {"kind": "solid", "id": 3,   "data": 0}
PODZOL    = {"kind": "solid", "id": 3,   "data": 2}
GRAVEL    = {"kind": "solid", "id": 13,  "data": 0}
SANDSTONE = {"kind": "solid", "id": 24,  "data": 0}
SMOOTH    = {"kind": "solid", "id": 24,  "data": 2}
SAND      = {"kind": "solid", "id": 12,  "data": 0}
PRISM     = {"kind": "solid", "id": 168, "data": 1}

# ── heights ───────────────────────────────────────────────────────────────────────────────────────
# The author's tiers, with the two rooms brought level with the ground they are entered from: a room
# that stands over its own approach is a plinth of bedrock, and a spawn that stands under its own
# egress is a wall at the door.
H_SPAWN   = 8    # the compound: one riser under the march it opens onto, which is a step and not a wall
H_QUARTER = 9    # both marches, the arm and the cape
H_POCKET  = 11   # the wool room, and the top of the ramp it is entered across
H_ARM_IN  = 11   # the lip at the arm's inner end, and the top of the ramp that climbs to it
H_APRON   = 13   # the keep's landing, one per arm
H_KEEP    = 15   # the keep — the author's own number
H_TIER1, H_TIER2 = 16, 17

# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
# The author's eleven rectangles and their ids, in their order, at their scale. Only `surface` moves.
PIECES = [
    ("piece-4",  "piece",     [-10, -10, 20, 20], H_KEEP),     # the keep, its own image under rot_90
    ("piece",    "piece",     [-32,  -5,  8, 10], H_QUARTER),  # the arm's inner run — a ramp
    ("piece-2",  "piece",     [-45,  -6, 13, 12], H_QUARTER),  # the arm's middle
    ("piece-5",  "piece",     [-45, -28, 13, 15], H_QUARTER),  # the march to the west arm
    ("piece-6",  "piece",     [-28, -45, 15, 13], H_QUARTER),  # the march to the north arm
    ("piece-8",  "piece",     [-32, -25,  7, 10], H_QUARTER),  # the wool approach, west — a ramp
    ("piece-9",  "piece",     [-25, -32, 10,  7], H_QUARTER),  # the wool approach, north — a ramp
    ("piece-10", "piece",     [-17,  -5,  7, 10], H_APRON),    # the keep's apron — the flight up
    ("piece-11", "piece",     [-49,  -5,  4, 10], H_QUARTER),  # the arm's outer cape
    ("spawn",    "spawn",     [-48, -48, 20, 20], H_SPAWN),    # the corner: region 20x20, hall 14x14
    ("wool",     "wool-room", [-25, -25, 10, 10], H_POCKET),   # the room, level with its approaches
]

# What the plan states no zone for, and cannot be played without: nine islands and no frontline.
ZONES = [
    ("bz-arm",   [-45, -13, 13, 26]),   # the arm and the quarter gap either side of it
    ("bz-cross", [-26,  -5, 11, 10]),   # the arm's hop onto the keep's apron
]


def plan():
    return {
        "plan": 2,
        "meta": {"name": "Quatrefoil"},
        "globals": {"cell": CELL, "symmetry": "rot_90", "maxPlayers": 12,
                    "surface": 9, "observerY": 34},
        "pieces": [{"id": i, "role": r, "rect": rect, "surface": s} for i, r, rect, s in PIECES],
        "zones": [{"id": i, "rect": rect, "holes": []} for i, rect in ZONES],
        "placements": {
            # The hall is 14x14 in the piece's outer corner, so the other two sides of the 20x20 region
            # are ground anybody walks along rather than wall a spawning player meets.
            "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [7, 7],
                        "facing": "back", "footprint": [1, 1, 14, 14]}],
            "wools":  [{"id": "wool-1", "piece": "wool", "at": [5, 5]}],
            "iron":   [{"id": "iron-1", "piece": "spawn", "at": [7.5, 18.5]}],
            "destroyables": [], "cores": [],
        },
        "walls": [], "boxes": [],
    }


# ── themes ────────────────────────────────────────────────────────────────────────────────────────
def cell_pattern(seed, size, palette, rise=None, jitter=60, warp=2):
    out = {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
           "palette": palette}
    if rise is not None:
        out["rise"] = rise
    return out


def layered(bands, beyond):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def theme(surface_bands, wall_bands, fill, rim=None, rim_edges="void", depth=3):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"enabled": rim is not None, "depth": 1, "material": rim or COBBLE},
        "surface": {"enabled": True, "depth": depth,
                    "material": layered(surface_bands, wall_bands[-1][0])},
        "wall": layered(wall_bands[:-1], wall_bands[-1][0]),
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the quarters: a mossy grey-green turf over coffee-dark earth, two materials in the top course
    "moor": theme(
        surface_bands=[(cell_pattern(11, 7, [MOSS, MOSS, COARSE]), 1), (DIRT, 1), (COARSE, 1)],
        wall_bands=[(MOSS, 1), (COARSE, 2), (DIRT, 1), (STONE, 3), (ANDESITE, 1)],
        fill=cell_pattern(21, 7, [STONE, STONE, ANDESITE], rise=4)),
    # the patches worn into it, and the beds cut into the keep's deck
    "brake": theme(
        surface_bands=[(cell_pattern(13, 5, [PODZOL, COARSE]), 1), (DIRT, 1)],
        wall_bands=[(PODZOL, 1), (COARSE, 2), (STONE, 3), (ANDESITE, 1)],
        fill=cell_pattern(21, 7, [STONE, STONE, ANDESITE], rise=4), depth=2),
    # the four capes: pale sand, the board's own rim and the one ground that is not the moor
    "strand": theme(
        surface_bands=[(cell_pattern(17, 7, [SANDSTONE, SANDSTONE, SAND, GRAVEL]), 1), (SANDSTONE, 1)],
        wall_bands=[(SANDSTONE, 1), (SMOOTH, 2), (SANDSTONE, 3), (STONE, 1)],
        fill=cell_pattern(23, 7, [SMOOTH, SANDSTONE], rise=4), depth=2),
    # the keep: made, and made of something the ground is not — courses rather than a field
    "keep": theme(
        surface_bands=[({"kind": "checker", "size": 3, "even": SMOOTH, "odd": SANDSTONE}, 1),
                       (BRICK, 1), (STONE, 1)],
        wall_bands=[(CHISELLED, 1), (SMOOTH, 1), (PRISM, 1), (BRICK, 3), (ANDESITE, 1)],
        fill=cell_pattern(31, 7, [BRICK, STONE], rise=4),
        rim=CHISELLED, rim_edges="drop", depth=3),
}


def lobed(cx, cz, rx, rz, points=9, wobble=0.16, phase=0.0):
    """A ring that is not a rectangle — a rectangle builds a mesa with sheer sides."""
    ring = []
    for i in range(points):
        a = 2 * math.pi * i / points + phase
        r = 1.0 + wobble * math.sin(3 * a + phase * 2.3) + 0.5 * wobble * math.sin(5 * a + 1.1)
        ring.append([round(cx + rx * r * math.cos(a), 1), round(cz + rz * r * math.sin(a), 1)])
    return ring


def catmull(ring, divisor=6.0):
    n, controls = len(ring), {}
    for i in range(n):
        p0, p1, p2 = ring[(i - 1) % n], ring[i], ring[(i + 1) % n]
        tx, tz = (p2[0] - p0[0]) / divisor, (p2[1] - p0[1]) / divisor
        controls[str(i)] = {"in": [round(p1[0] - tx, 2), round(p1[1] - tz, 2)],
                            "out": [round(p1[0] + tx, 2), round(p1[1] + tz, 2)]}
    return controls


# ── the shaping ───────────────────────────────────────────────────────────────────────────────────
def ramp(shape_id, ring, anchors, theme_name):
    """A tilted plane over one piece: `level` with a height a vertex, out of the elevation model so the
    grain cannot wobble it. Every rise here runs at least twice its own height, which is what makes the
    risers one block rather than two."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
            "base_height": min(anchors), "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude", "theme": theme_name,
            "vertices": ring, "anchor_heights": anchors}


def slab(shape_id, x0, z0, x1, z1, height, theme_name):
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
            "base_height": height, "skirt": 0, "relief_scope": "exclude", "theme": theme_name,
            "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def brush(shape_id, ring, theme_name):
    """A paint patch on solved ground: an ordinary one-course add, never an override."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "controls": catmull(ring), "theme": theme_name}


ADD_SHAPES = [
    # ── the three places the plan steps two blocks, each one a ramp over the piece that steps ─────
    # the approach in front of the wool room, west: 9 at the march, 11 at the room's door, over 7
    ramp("ramp-wool-w", [[-32, -25], [-25, -25], [-25, -15], [-32, -15]],
         [H_QUARTER, H_POCKET, H_POCKET, H_QUARTER], "moor"),
    # and north, the same climb turned a quarter
    ramp("ramp-wool-n", [[-25, -32], [-15, -32], [-15, -25], [-25, -25]],
         [H_QUARTER, H_QUARTER, H_POCKET, H_POCKET], "moor"),
    # the arm's inner run: 9 where it meets the arm, 11 at the lip it is bridged from
    ramp("ramp-arm", [[-32, -5], [-24, -5], [-24, 5], [-32, 5]],
         [H_QUARTER, H_ARM_IN, H_ARM_IN, H_QUARTER], "strand"),
    # ── the keep: the flight up each face, and two terraces over the deck ─────────────────────────
    ramp("keep-ramp", [[-17, -5], [-10, -5], [-10, 5], [-17, 5]],
         [H_APRON, H_KEEP, H_KEEP, H_APRON], "keep"),
    slab("keep-t1", -6, -6, 6, 6, H_TIER1, "keep"),
    slab("keep-t2", -2, -2, 2, 2, H_TIER2, "keep"),
    # ── what lets the keep go green: beds cut into the deck's corners, one fanned four ways ───────
    brush("keep-bed", lobed(-8, -8, 2, 2, points=8, wobble=0.18), "brake"),
    # ── the quarters: patches of bare earth worn into the moor ────────────────────────────────────
    brush("brake-march-s", lobed(-39, -21, 5, 4, points=9, wobble=0.22), "brake"),
    brush("brake-march-e", lobed(-21, -39, 4, 5, points=9, wobble=0.22, phase=0.9), "brake"),
    brush("brake-yard", lobed(-38, -38, 4, 4, points=9, wobble=0.25, phase=1.7), "brake"),
]

# ── the relief ────────────────────────────────────────────────────────────────────────────────────
# A grain and nothing else. The shape of this board is its tiers and its ramps; a push here would put
# a hill where the plan drew flat ground, and the plan is the author's.
# `reach: 0` is unlimited, and a group whose only constraint is the wool room's own pin then solves the
# whole quarter at the room's height. A finite reach pulls the ground back to base away from a pin.
RELIEF = {"team": {"base": 9, "reach": 5, "step": 1, "stairs": True,
                   "grain": {"amplitude": 0.9, "scale": 13, "seed": 7},
                   "marks": [], "pushes": []}}

# ── dressing ──────────────────────────────────────────────────────────────────────────────────────
DRESSING = {"props": [
    # the track out of the spawn door, over the march to the wool approach
    {"id": "track-south", "kind": "stroke", "seed": 70, "style": "worn", "coverage": 0.8,
     "radius": 1.5, "route": True,
     "points": [[-41, -32], [-40, -26], [-38, -20], [-34, -18]],
     "pave": cell_pattern(83, 3, [GRAVEL, COARSE, COBBLE, GRAVEL], jitter=100, warp=0)},
    {"id": "track-east", "kind": "stroke", "seed": 71, "style": "worn", "coverage": 0.8,
     "radius": 1.5, "route": True,
     "points": [[-32, -41], [-26, -40], [-20, -38], [-18, -34]],
     "pave": cell_pattern(84, 3, [GRAVEL, COARSE, COBBLE, GRAVEL], jitter=100, warp=0)},
    {"id": "flora-marches", "kind": "flora", "seed": 250,
     "points": [[-45, -27], [-33, -27], [-33, -14], [-45, -14]],
     "spec": {"coverage": 0.32, "scale": 9, "octaves": 3, "fernShare": 0.45,
              "flowerShare": 0.07, "flowerScale": 11, "tallShare": 0.1}},
    {"id": "flora-dell", "kind": "flora", "seed": 251,
     "points": [[-27, -45], [-14, -45], [-14, -33], [-27, -33]],
     "spec": {"coverage": 0.34, "scale": 9, "octaves": 3, "fernShare": 0.5,
              "flowerShare": 0.08, "flowerScale": 11, "tallShare": 0.1}},
    {"id": "flora-keep", "kind": "flora", "seed": 252,
     "points": [[-10, -10], [-6, -10], [-6, -6], [-10, -6]],
     "spec": {"coverage": 0.6, "scale": 5, "octaves": 2, "fernShare": 0.35,
              "flowerShare": 0.35, "flowerScale": 7, "tallShare": 0.05}},
]}

# A 98-block board with four spawn keep-outs and four wool-room door approaches on it has little free
# ground, and `06-claims.txt` is where the free cells are read off rather than guessed at.
TREES = [
    ("t-march", -20, -44, "spruce", 8),
    ("t-arm-1", -44, 4, "birch", 6), ("t-arm-2", -40, -5, "birch", 6),
    ("t-keep", -8, -8, "birch", 5),
]
for i, (tid, tx, tz, species, height) in enumerate(TREES):
    DRESSING["props"].append({"id": tid, "kind": "tree", "seed": 200 + i, "x": tx, "z": tz,
                              "form": "template", "species": species, "height": height})

# Two erratics and no more: on a 98-block board the four spawn keep-outs, the four wool-room door
# approaches and the two tracks claim nearly every cell of a quarter, and `--candidates` answers "none of
# them" for a third. Bare ground you chose beats dressing that would not stand.
BOULDERS = [
    ("b-keep", -14, -3, "angular", 2, True, MOSS),
    ("b-cape", -46, -3, "round", 2, False, SANDSTONE),
]
for i, (bid, bx, bz, form, size, mossy, rock) in enumerate(BOULDERS):
    DRESSING["props"].append({"id": bid, "kind": "boulder", "seed": 300 + i, "x": bx, "z": bz,
                              "form": form, "size": size, "mossy": mossy, "rock": rock})


def finish():
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-04",
        "roomStyles": {"spawn": "@hb-spawn", "cage": "@hb-cage"},
        "themes": THEMES,
        "mapTheme": "moor",
        # keyed on the compiled ids, because pieces at one height fuse into one shape and a height
        # key cannot tell two of them apart
        "themeById": {
            "s0": "keep",     # the apron is the keep's own landing, not the arm's end
            "s1": "keep",     # the keep
            "s2": "strand",   # the arm and its cape, on the axis
            "s3": "moor",     # the spawn compound, one riser under the marches
            "s4": "moor",     # both marches and both wool approaches
            "s5": "moor",     # the room's own ground
        },
        "shapePropsById": {
            # the keep and its aprons are made: out of the elevation model, flat and sheer
            "s0": {"relief_scope": "exclude"},
            "s1": {"relief_scope": "exclude"},
            # the room is a pad at the top of its ramps, and a pad does not wobble
            "s5": {"relief_scope": "hold"},
        },
        "relief": RELIEF,
        "addShapes": ADD_SHAPES,
        "dressing": DRESSING,
    }


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
        json.dump(plan(), f, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
        json.dump(finish(), f, indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")


if __name__ == "__main__":
    main()
