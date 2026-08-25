#!/usr/bin/env python3
"""Write the two authored documents for `opus5-tarnfell`.

    python3 specs/opus5-tarnfell/build-spec.py

This board is a landscape rather than a building, so almost nothing in it is a rectangle. The plan
states one spawn and one goal; the ground is a single 26-vertex polygon; and every height on it is a
relief mark. What the marks are and where they sit is the whole design, so they are the part of this
file worth reading.

**The marks reach past the coast on purpose.** A `point` mark iterates its own radius and keeps the
cells the footprint has, and a `line` mark walks the land and measures its distance to a polyline
that may run anywhere — so a summit centred twenty blocks out to sea, with a radius that reaches
back in, holds the coastal strip at the summit's height and puts the peak itself off the map. The
edge of the board is then a mountainside cut through rather than ground tapering to base, which is
what makes the high ground read from the side.

Output: `opus5-tarnfell.plan.json` and `opus5-tarnfell.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-tarnfell"

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
# A cell of two blocks, because the two distances the board is authored to are odd numbers: the
# goal stands 30 right and 50 ahead of the spawn, and the two goals stand 150 apart.
CELL = 2
SPAWN = (0, 119)                    # the marker, in blocks
GOAL = (SPAWN[0] + 30, SPAWN[1] - 50)                       # 30 right, 50 ahead
GOAL_SPAN = 2 * math.hypot(*GOAL)                           # what the pair actually measures

BASE = 20                           # the level the field falls back to where nothing is stated
LAKE_Y, BEACH_Y, ISLE_Y = 6, 10, 16
SHELF_Y = 32                        # the spawn's own terrace
LAND_H = 24                         # the drawn thickness of the ground before the relief solves it


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def stack(*pairs, ending="repeat"):
    return {"bands": [{"material": m, "thickness": t} for m, t in pairs], "ending": ending}


def layered(band_stack, axis="depth", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": band_stack}
    if beyond is not None:
        out["beyond"] = beyond
    return out


def noise(seed, scale, octaves, stops):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}


def voronoi(seed, cell_size, bands):
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


def theme(surface, wall, fill, rim=None, surface_depth=3, rim_edges="void", bedrock=1):
    """One paintable recipe. **The rim is off on every theme here**, because every edge on this
    board was solved rather than built: a rim caps each fall with a band and turns a rolling hill
    into contour lines."""
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or solid(155, 0), "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


GRASS = solid(2, 0)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
PODZOL = solid(3, 2)
STONE = solid(1, 0)
ANDESITE = solid(1, 5)
DIORITE = solid(1, 3)
POLISHED_DIORITE = solid(1, 4)
GRANITE = solid(1, 1)
COBBLE = solid(4, 0)
MOSSY = solid(48, 0)
GRAVEL = solid(13, 0)
SAND = solid(12, 0)
SANDSTONE = solid(24, 0)
SAND_SLAB = solid(43, 9)
CLAY = solid(82, 0)
SNOW = solid(80, 0)
STONE_BRICK = solid(98, 0)
MUSHROOM_STEM = solid(99, 15)

# ── the themes, one per landform ──────────────────────────────────────────────────────────────
# Three families and no more across the whole board: verdant for what grows, sand for the shore,
# grey stone for what the water and the weather left. The peaks carry no theme at all — they are
# brushed, below.
THEMES = {
    # the rolling hills, and the map's default: grass over dirt, worn to coarse dirt on the crowns
    "meadow": theme(
        surface=layered(stack((noise(11, 13, 3, [GRASS, GRASS, COARSE]), 1), (DIRT, 2))),
        wall=layered(stack((DIRT, 2), (COARSE, 1), (STONE, 4))),
        fill=STONE, surface_depth=3),

    # the forest floor: the same grass gone over to podzol under the canopy
    "wood": theme(
        surface=layered(stack((noise(12, 9, 3, [GRASS, PODZOL, PODZOL]), 1), (DIRT, 1), (COARSE, 1))),
        wall=layered(stack((PODZOL, 1), (DIRT, 2), (STONE, 4))),
        fill=STONE, surface_depth=3),

    # the beach: four courses of sand deep, so a shore dug into is still a shore
    "beach": theme(
        surface=layered(stack((voronoi(13, 9, [(SAND, 3), (SAND, 2), (SANDSTONE, 1)]), 2),
                              (SANDSTONE, 2))),
        wall=layered(stack((SAND, 2), (SANDSTONE, 3), (STONE, 3))),
        fill=SANDSTONE, surface_depth=4),

    # what is under the water: the bed the lake was cut into
    "lakebed": theme(
        surface=layered(stack((voronoi(14, 6, [(GRAVEL, 2), (SAND, 2), (CLAY, 1)]), 2), (GRAVEL, 1))),
        wall=layered(stack((GRAVEL, 2), (STONE, 4))),
        fill=STONE, surface_depth=3),

    # the island in the middle of it: grass with the sand still showing through at its own shore
    "isle": theme(
        surface=layered(stack((noise(15, 7, 2, [GRASS, GRASS, SAND]), 1), (SAND, 1), (SANDSTONE, 1))),
        wall=layered(stack((SAND, 2), (SANDSTONE, 2), (STONE, 4))),
        fill=STONE, surface_depth=3),

    # the mountains, unbrushed: bare rock, which is what the strokes are laid over
    "crag": theme(
        surface=layered(stack((noise(16, 11, 3, [STONE, ANDESITE, DIORITE]), 2), (STONE, 2))),
        wall=layered(stack((ANDESITE, 2), (STONE, 3), (GRANITE, 1), (STONE, 4))),
        fill=STONE, surface_depth=3),
}


# ── the ground ────────────────────────────────────────────────────────────────────────────────
# One polygon, authored on the +z half and fanned. Its z = 0 edge is the seam the mirror closes,
# so the coast is drawn on three sides and the fourth is where the two halves meet.
COAST = [
    (84, 0), (88, 22), (79, 46), (86, 70), (74, 96), (85, 118), (72, 140), (56, 158),
    (30, 169), (2, 172), (-26, 168), (-52, 157), (-70, 140), (-84, 120), (-73, 96),
    (-86, 72), (-77, 46), (-88, 22), (-84, 0),
]

# The two crevasses, one to a flank: a slot open at the coast and closing inland, so the ground goes
# round rather than being cut in two. A subtract takes the whole column, which is what makes a
# crevasse deep — no relief mark of any kind cuts a hole.
CREVASSES = [
    [(-92, 84), (-46, 70), (-41, 78), (-88, 93)],
    [(92, 116), (50, 100), (46, 108), (88, 125)],
]

_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def polygon(prefix, points, floor=0, height=LAND_H, op="add", theme_key=None):
    shape = {"id": sid(prefix), "type": "polygon", "operation": op,
             "vertices": [[x, z] for x, z in points], "floor": floor, "base_height": height}
    if theme_key:
        shape["theme"] = theme_key
    return shape


def circle(prefix, cx, cz, radius, theme_key, floor=0, height=LAND_H):
    return {"id": sid(prefix), "type": "circle", "operation": "add",
            "center_x": cx, "center_z": cz, "radius": radius,
            "floor": floor, "base_height": height, "theme": theme_key}


def rect(prefix, x0, z0, x1, z1, theme_key, floor=0, height=LAND_H):
    return {"id": sid(prefix), "type": "rectangle", "operation": "add",
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": height, "theme": theme_key}


shapes = [polygon("land", COAST, theme_key="meadow")]
shapes += [polygon("crev", ring, height=64, op="subtract") for ring in CREVASSES]

# The paint scopes. On an island a relief has solved, a shape's own height is not read — every cell
# takes the solved field — so a shape added here changes which theme owns its cells and nothing
# else. They nest smallest-first, which is the order the scope resolves in.
shapes += [
    rect("t", -88, 58, 88, 104, "wood"),        # the forest, a band across the board
    circle("t", 0, 0, 58, "beach"),             # the shore round the water
    circle("t", 0, 0, 40, "lakebed"),           # what the water covers
    circle("t", 0, 0, 12, "isle"),              # and the island in the middle of it
    rect("t", -88, 124, 88, 174, "crag"),       # the mountains behind the spawn
]

# ── the relief ────────────────────────────────────────────────────────────────────────────────
def point(ident, x, z, h, r):
    return {"id": ident, "kind": "point", "at": [x, z], "h": h, "r": r}


def line(ident, points, heights, width):
    return {"id": ident, "kind": "line", "points": [[x, z] for x, z in points],
            "h": heights, "r": width}


def area(ident, ring, h):
    return {"id": ident, "kind": "area", "ring": [[x, z] for x, z in ring], "h": h}


def ring_of(cx, cz, radius, count=16, wobble=0.0, phase=0.0):
    """A closed ring. `wobble` swells and pinches the radius on two beats round the circle, because
    a lake drawn at one radius reads as a compass circle and nothing on this board is drawn."""
    out = []
    for k in range(count):
        angle = 2 * math.pi * k / count
        r = radius * (1 + wobble * (math.sin(3 * angle + phase) * 0.6
                                    + math.sin(5 * angle + 1.7 * phase) * 0.4))
        out.append((round(cx + r * math.cos(angle), 1), round(cz + r * math.sin(angle), 1)))
    return out


MARKS = [
    # ── the water, first, so everything stated after it wins the cells they share ──
    # An `area` mark pins its whole interior flat, which is what a lake pan is; the ring is wobbled
    # so the shore is a shape rather than a compass circle.
    area("lake-pan", ring_of(0, 0, 42, 22, wobble=0.10), LAKE_Y),
    # Two shore lines with unpinned ground between them: butted, they build as two terraces and a
    # five-course step at the seam; seven blocks apart, the relaxation ramps 8 to 14 across the gap
    # and the beach shelves instead.
    line("shore-lo", ring_of(0, 0, 43, 24, wobble=0.09, phase=0.6)
         + [ring_of(0, 0, 43, 24, wobble=0.09, phase=0.6)[0]], [BEACH_Y - 2], 5),
    line("shore-hi", ring_of(0, 0, 60, 24, wobble=0.08, phase=1.4)
         + [ring_of(0, 0, 60, 24, wobble=0.08, phase=1.4)[0]], [BEACH_Y + 4], 4),

    # ── the rolling hills ──
    # **A point mark's radius pins a flat disc**, so a radius is a mesa and not a summit: these are
    # three to six, and the rolling comes from the relaxation between them and from `reach`.
    point("hill-w", -52, 74, 30, 5),
    point("hill-c", 18, 88, 34, 5),
    point("hill-nw", -26, 104, 29, 4),
    point("hill-e", 58, 96, 33, 5),
    point("hill-se", 46, 66, 26, 4),
    point("hill-n", -66, 102, 36, 5),
    point("hill-fore", 4, 66, 23, 4),
    point("hill-w2", -74, 60, 27, 4),
    point("hill-e2", 76, 74, 29, 4),
    point("hill-c2", 8, 106, 31, 4),
    point("hill-sw", -40, 56, 24, 3),
    point("hill-s2", 62, 50, 25, 3),
    point("dip-w", -18, 78, 21, 4),
    point("dip-e", 34, 96, 23, 4),

    # a gully cut through the hills — twenty courses under the ground either side of it, and walkable
    line("gully", [(-24, 120), (-12, 102), (-24, 84), (-16, 70)], [16, 9, 9, 14], 4),

    # ── the mountains ──
    # The crest, inside the board, with its height varying along its length.
    line("ridge", [(-96, 148), (-52, 158), (-8, 165), (34, 160), (78, 150), (100, 140)],
         [58, 67, 73, 69, 62, 56], 10),
    # And three lines run *outside* the coast: a line mark walks the land and measures its distance
    # to a polyline that may lie anywhere, so a ridge traced eight blocks out to sea pins the
    # coastal strip at its own heights and puts the crest itself off the map. The board's edge is
    # then a mountainside cut through — which a mark inside the coast cannot produce, because the
    # relaxation would have to fall to base before it got there.
    line("brow-n", [(-46, 180), (-14, 184), (18, 183), (50, 177)], [70, 80, 78, 72], 15),
    line("brow-w", [(-98, 104), (-96, 128), (-86, 150), (-70, 166)], [58, 72, 70, 62], 14),
    line("brow-e", [(100, 96), (98, 122), (88, 146), (70, 164)], [56, 70, 68, 60], 14),
    # true summits, small-radiused, so the crest has peaks on it rather than a flat top
    point("peak-a", -36, 152, 68, 4),
    point("peak-b", 10, 160, 76, 4),
    point("peak-c", 54, 144, 64, 3),
    point("peak-d", -70, 140, 66, 3),
    point("foot-w", -58, 128, 44, 5),
    point("foot-e", 54, 130, 42, 5),

    # ── the shelf the spawn stands on, and the shelf the goal stands on ──
    area("spawn-shelf", ring_of(SPAWN[0], SPAWN[1], 15, 12), SHELF_Y),
    area("goal-shelf", ring_of(GOAL[0], GOAL[1], 11, 12, wobble=0.12), 27),

    # ── and the island, last of all, because it is the one mark inside the lake ──
    line("isle-shore", ring_of(0, 0, 11, 16, wobble=0.14) + [ring_of(0, 0, 11, 16, wobble=0.14)[0]],
         [LAKE_Y + 3], 3),
    area("isle", ring_of(0, 0, 8, 16, wobble=0.16), ISLE_Y),
    point("isle-knoll", 2, 3, ISLE_Y + 4, 3),
]

PUSHES = [
    # spurs off the flanks of two hills — a push adds to the solved surface, so it is a shape on a
    # landform rather than a restatement of it
    {"id": "spur-w", "ring": [[x, z] for x, z in ring_of(-40, 90, 16, 10)],
     "amount": 6, "falloff": 14, "roughness": 0.35, "crown": 2, "seed": 3},
    {"id": "spur-e", "ring": [[x, z] for x, z in ring_of(36, 108, 15, 10)],
     "amount": 5, "falloff": 12, "roughness": 0.4, "crown": 2, "seed": 4},
]

# `*` rather than a name: the shapes are appended onto the island the compile emitted, which is
# called `team`, and one relief over every island is what a board of one island wants said.
RELIEF = {
    "*": {
        "base": BASE, "reach": 36, "step": 1, "stairs": False,
        "grain": {"amplitude": 1.9, "scale": 9, "seed": 7},
        "marks": MARKS,
        "pushes": PUSHES,
    }
}


# ── the brush ─────────────────────────────────────────────────────────────────────────────────
def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "path", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


TRACK = voronoi(21, 4, [(COARSE, 2), (DIRT, 2), (GRAVEL, 1)])
FOOTWORN = voronoi(22, 3, [(COARSE, 2), (PODZOL, 1)])

# The main path: seven blocks across, from the spawn's terrace over the hills, through the forest,
# to the water. It is the only stroke on the board that claims its cells as a route.
MAIN_PATH = [(0, 116), (-13, 106), (2, 95), (-11, 84), (5, 72), (-4, 62), (7, 54), (0, 47)]

STROKES = [
    stroke("path-main", MAIN_PATH, 3.5, TRACK, style="solid", coverage=1.0, route=True, seed=31),

    # the thinner ones, off it, to the four places somebody lives
    stroke("path-cabin-n", [(-13, 106), (-20, 102), (-27, 99)], 1.6, FOOTWORN,
           coverage=0.85, route=True, seed=32),
    stroke("path-cabin-e", [(2, 95), (11, 93), (19, 91)], 1.6, FOOTWORN,
           coverage=0.85, route=True, seed=33),
    stroke("path-cabin-w", [(-11, 84), (-22, 76), (-32, 69)], 1.6, FOOTWORN,
           coverage=0.85, route=True, seed=34),
    stroke("path-camp", [(-4, 62), (4, 55), (14, 53)], 1.4, FOOTWORN,
           coverage=0.8, route=True, seed=35),

    # ── the peaks, coloured strictly with the brush ──
    # The crag theme lays bare rock and stops there; every band above it is a stroke traced along
    # the ridge, which is the only instrument that follows a line of ground rather than a footprint.
    stroke("peak-rock", [(-96, 148), (-52, 158), (-8, 165), (34, 160), (78, 150), (100, 140)],
           13, voronoi(23, 7, [(ANDESITE, 3), (STONE, 2), (DIORITE, 1)]),
           style="rough", coverage=0.9, seed=41),
    stroke("peak-pale", [(-70, 152), (-30, 161), (8, 166), (46, 158), (84, 147)],
           8, voronoi(24, 5, [(DIORITE, 2), (POLISHED_DIORITE, 1), (ANDESITE, 1)]),
           style="rough", coverage=0.8, seed=42),
    stroke("peak-snow", [(-48, 157), (-18, 164), (14, 164), (48, 156)],
           5, voronoi(25, 4, [(SNOW, 3), (MUSHROOM_STEM, 1), (DIORITE, 1)]),
           style="rough", coverage=0.75, seed=43),
    # the two summits that stand off the board get their own, so the edge is snow and not bare rock
    stroke("peak-snow-n", [(-34, 172), (-14, 176), (6, 174)], 6,
           voronoi(26, 4, [(SNOW, 3), (DIORITE, 1)]), style="rough", coverage=0.7, seed=44),
    stroke("peak-snow-w", [(-86, 128), (-78, 140), (-70, 149)], 6,
           voronoi(27, 4, [(SNOW, 2), (DIORITE, 1), (ANDESITE, 1)]), style="rough",
           coverage=0.65, seed=45),
    stroke("peak-snow-e", [(88, 116), (82, 128), (74, 140)], 6,
           voronoi(28, 4, [(SNOW, 2), (DIORITE, 1), (ANDESITE, 1)]), style="rough",
           coverage=0.65, seed=46),

    # ── the seams, brushed so no two areas meet along a line ──
    # Each one is laid in the material of the area on the far side of it, at a coverage that leaves
    # most of the ground it crosses showing, so the join reads as a gradient rather than an edge.
    stroke("seam-shore", ring_of(0, 0, 58, 28, wobble=0.07)
           + [ring_of(0, 0, 58, 28, wobble=0.07)[0]], 11,
           voronoi(29, 6, [(SAND, 2), (GRASS, 2), (COARSE, 1)]),
           style="rough", coverage=0.26, seed=51),
    stroke("seam-wood-s", [(-88, 60), (-44, 56), (0, 59), (44, 56), (88, 60)], 9,
           voronoi(30, 5, [(PODZOL, 2), (GRASS, 2), (COARSE, 1)]),
           style="rough", coverage=0.28, seed=52),
    stroke("seam-wood-n", [(-88, 103), (-44, 106), (0, 102), (44, 106), (88, 103)], 9,
           voronoi(31, 5, [(PODZOL, 2), (GRASS, 2), (COARSE, 1)]),
           style="rough", coverage=0.28, seed=53),
    stroke("seam-crag", [(-88, 126), (-44, 122), (0, 127), (44, 122), (88, 126)], 8,
           voronoi(32, 6, [(ANDESITE, 2), (COARSE, 2), (GRAVEL, 1)]),
           style="rough", coverage=0.45, seed=54),
    stroke("seam-isle", ring_of(0, 0, 10, 14, wobble=0.12)
           + [ring_of(0, 0, 10, 14, wobble=0.12)[0]], 3,
           voronoi(33, 4, [(SAND, 2), (GRASS, 1)]), style="rough", coverage=0.5, seed=55),
]


# ── what stands on it ─────────────────────────────────────────────────────────────────────────
def tree(ident, x, z, species, height, seed):
    return {"id": ident, "kind": "tree", "seed": seed, "x": x, "z": z,
            "form": "template", "species": species, "height": height}


def house(ident, x, z, width, depth, style, seed, front="negZ"):
    return {"id": ident, "kind": "house", "seed": seed, "front": front,
            "wings": [{"corners": [[x, z], [x + width, z + depth]]}], "style": style}


def boulder(ident, x, z, size, seed, form="angular", mossy=False):
    return {"id": ident, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": form, "size": size, "mossy": mossy,
            "rock": voronoi(34, 5, [(STONE, 2), (ANDESITE, 2), (COBBLE, 1)])}


def flora(ident, ring, coverage, seed, scale=11, fern=0.12, flower=0.24, tall=0.12):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 8, "tallShare": tall}}


# The forest: a stand thick enough to be one, drawn as a list rather than scattered, because every
# one of them is a place a player can stand behind.
# The forest: a stand thick enough to be one, drawn as a list rather than scattered, because every
# one of them is a place a player can stand behind. Nothing here comes within sixteen of the goal at
# (30, 69), inside the crevasse slots, or within three of the main path.
FOREST = [
    (-76, 68, "oak", 11), (-66, 60, "spruce", 13), (-58, 60, "oak", 10), (-70, 92, "birch", 9),
    (-48, 64, "oak", 12), (-44, 84, "spruce", 14), (-36, 60, "birch", 10), (-34, 78, "oak", 11),
    (-24, 64, "spruce", 12), (-44, 100, "oak", 10), (-15, 74, "oak", 13), (-18, 66, "birch", 9),
    (8, 62, "oak", 11), (13, 79, "spruce", 13), (30, 48, "oak", 10), (9, 97, "birch", 11),
    (34, 90, "oak", 12), (44, 56, "spruce", 12), (48, 80, "oak", 10), (44, 88, "birch", 9),
    (64, 66, "oak", 13), (70, 86, "spruce", 14), (76, 62, "oak", 11), (80, 80, "birch", 10),
    (-80, 98, "spruce", 12), (58, 58, "oak", 9), (-56, 98, "oak", 10), (28, 102, "birch", 9),
]

props = [
    # the water. One ring traced round the island at a radius that leaves the isle standing and
    # reaches the beach on the other side, cut three courses into a pan the relief already flattened
    {"id": "the-mere", "kind": "water", "seed": 5, "form": "natural",
     "points": [[x, z] for x, z in ring_of(0, 0, 25, 24, wobble=0.08, phase=0.3)]
               + [list(ring_of(0, 0, 25, 24, wobble=0.08, phase=0.3)[0])],
     "radius": 12.0, "depth": 3, "edge": 0.9, "shore": 7, "shoreWander": True,
     "bank": voronoi(35, 5, [(SAND, 3), (SAND, 2), (GRAVEL, 1), (SANDSTONE, 1)])},
]

props += [tree(f"wood-{k}", x, z, sp, h, 200 + k)
          for k, (x, z, sp, h) in enumerate(FOREST)]

props += [
    # the four places somebody lives, each at the end of a thinner path
    house("cabin-n", -31, 96, 7, 6, "@tf-cabin", 11),
    house("cabin-e", 19, 88, 8, 6, "@tf-cabin", 12, front="posZ"),
    house("cabin-w", -37, 65, 7, 7, "@tf-cabin", 13),
    house("tent-a", 2, 47, 4, 5, "@tf-tent", 14),
    house("tent-b", 16, 52, 4, 4, "@tf-tent", 15),
    house("tent-c", -12, 51, 4, 4, "@tf-tent", 16, front="posZ"),

    # the boulders: the crevasse lips and the foot of the mountains, where loose rock belongs
    boulder("rock-crev-w1", -52, 90, 3.0, 61),
    boulder("rock-crev-w2", -66, 96, 2.4, 62, form="outcrop"),
    boulder("rock-crev-e1", 54, 94, 3.2, 63),
    boulder("rock-crev-e2", 68, 120, 2.2, 64, form="outcrop"),
    boulder("rock-foot-w", -44, 120, 4.0, 65, form="cairn"),
    boulder("rock-foot-e", 38, 122, 3.6, 66),
    boulder("rock-shore-w", -46, 40, 2.6, 67, form="round", mossy=True),
    boulder("rock-shore-e", 44, 34, 2.2, 68, form="round", mossy=True),
    boulder("rock-isle", 4, -3, 2.0, 69, form="cairn", mossy=True),

    # ground cover: dense in the wood, thin on the hills, a fringe on the beach and the island
    flora("turf-wood", [(-86, 58), (86, 58), (86, 102), (-86, 102)], 0.5, 71,
          scale=9, fern=0.22, flower=0.18, tall=0.2),
    flora("turf-hills", [(-84, 104), (84, 104), (84, 124), (-84, 124)], 0.3, 72,
          scale=13, fern=0.08, flower=0.3, tall=0.08),
    flora("turf-shore", ring_of(0, 0, 54, 18), 0.22, 73, scale=8, fern=0.05, flower=0.35, tall=0.05),
    flora("turf-isle", ring_of(0, 0, 8, 12), 0.45, 74, scale=6, fern=0.1, flower=0.4, tall=0.1),
]

props += STROKES


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


plan = {
    "plan": 1,
    "meta": {"name": "Tarnfell"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": BASE},
    "pieces": [
        # The plan's rectangles are inset inside the drawn coast rather than approximating it: the
        # outline the board builds is the polygon's, and these exist so the reads that walk a plan
        # have ground to walk. Without them the spawn's door opens onto void at the plan tier
        # (`SP9`) and `GO1` answers nothing at all, because the only piece on the board is the
        # spawn itself.
        {"id": "fell-s",    "role": "piece", "rect": cells(-64, 0, 64, 58),      "surface": BASE},
        {"id": "fell-m",    "role": "piece", "rect": cells(-64, 58, 64, 104),    "surface": BASE},
        {"id": "fell-nl",   "role": "piece", "rect": cells(-60, 104, -24, 110),  "surface": BASE + 4},
        {"id": "fell-n",    "role": "piece", "rect": cells(-24, 104, 24, 110),   "surface": SHELF_Y},
        {"id": "fell-nr",   "role": "piece", "rect": cells(24, 104, 60, 110),    "surface": BASE + 4},
        {"id": "fell-w2",   "role": "piece", "rect": cells(-60, 110, -20, 126),  "surface": BASE + 6},
        {"id": "fell-nw",   "role": "piece", "rect": cells(-20, 110, -8, 126),   "surface": SHELF_Y},
        {"id": "fell-ne",   "role": "piece", "rect": cells(8, 110, 20, 126),     "surface": SHELF_Y},
        {"id": "fell-e2",   "role": "piece", "rect": cells(20, 110, 60, 126),    "surface": BASE + 6},
        {"id": "fell-back", "role": "piece", "rect": cells(-52, 126, 52, 150),   "surface": SHELF_Y},
        {"id": "camp",      "role": "spawn", "rect": cells(-8, 110, 8, 126),     "surface": SHELF_Y},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [4, 4.5], "facing": "front"}],
        "destroyables": [
            # An absolute placement: the goal stands on ground the plan has no rectangle for.
            {"id": "destroyable-1", "at": [GOAL[0] / CELL, GOAL[1] / CELL],
             "style": "cube-4", "materials": "ender stone", "float": 4,
             "name": "The Wardstone"},
        ],
    },
}

finish = {
    "authors": ["Opus 5"],
    "addShapes": shapes,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "meadow",
    "roomStyles": {"cage": None, "spawn": "@tf-cabin"},
    "dressing": {"props": props},
}


def write():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"spawn {SPAWN}  goal {GOAL}  "
          f"(right {GOAL[0] - SPAWN[0]}, ahead {SPAWN[1] - GOAL[1]}, "
          f"goal-to-goal {GOAL_SPAN:.1f})")
    print(f"shapes {len(shapes)} · marks {len(MARKS)} · pushes {len(PUSHES)} · "
          f"themes {len(THEMES)} · props {len(props)} {kinds}")


if __name__ == "__main__":
    write()
