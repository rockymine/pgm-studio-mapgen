#!/usr/bin/env python3
"""Kilnbrow — a destroy-the-monument board on a red clay firing-ground.

Writes `opus5-kilnbrow.plan.json` and `opus5-kilnbrow.finish.json` beside this file.

The board is a lane. Each team's monument stands on an open shelf a short walk forward of
its spawn, and the ground around it answers four approaches rather than one: a spoil hill
east to climb and bridge from, a worked clay pit south-west to drop into and come up out
of, the kiln bench north to fight through, and the open pan in front. The two teams' lands
never touch — a build zone spans the whole width over the void between them.

Scale: cell 5. The team unit is authored at -z and rot_180 fans the rest.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-kilnbrow"

# ── blocks ────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE = 1, 2, 3, 4
GRAVEL, SANDSTONE = 13, 24
CLAY, STAINED_CLAY = 82, 159
LOG2, HARDENED_CLAY, RED_SANDSTONE = 162, 172, 179
SANDSTONE_STAIRS = 128
SANDSTONE_SLAB = (44, 1)
COARSE_DIRT, ANDESITE, DIORITE = (DIRT, 1), (STONE, 5), (STONE, 3)
DARK_OAK = (LOG2, 1)


def solid(block, data=0):
    """One block, the leaf every pattern bottoms out in."""
    if isinstance(block, tuple):
        block, data = block
    return {"kind": "solid", "id": block, "data": data}


def _stack(axis, flat):
    """A band stack on one axis, written as alternating material, thickness."""
    pairs = list(zip(flat[0::2], flat[1::2]))
    return {"kind": "layered", "axis": axis, "stack": {
        "ending": "repeat",
        "bands": [{"material": m, "thickness": t} for m, t in pairs]}}


def depth(*flat):
    """A stack down from the surface, so a surfacing block stays one course over its soil."""
    return _stack("depth", flat)


def slope(*flat):
    """A stack across the ground's angle: a thickness here is a span of degrees.

    It is the axis that tells a hillside from a meadow. A height stack would paint this
    board flat from above however much relief is under it.
    """
    return _stack("slope", flat)


def cells(palette, size, seed, jitter=40, warp=2, rise=3):
    """A jittered two-block texture — the brush a ground is mottled with."""
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": [solid(b) for b in palette], "rise": rise}


def voronoi(palette, size, seed, rise=4):
    """Rock nobody sees until a wall is cut. It is the fill, and it is stone.

    A voronoi draws a grid of lines with cells reading off it, which is nothing a landscape
    looks like — so it belongs in the body of the rock rather than on the surface. Band 0
    sits on the cell boundary and is the line; the last band takes whatever is left.
    """
    return {"kind": "voronoi", "seed": seed, "cellSize": size, "rise": rise,
            "bands": [{"material": solid(b), "depth": d}
                      for b, d in zip(palette, (1, 2, 3))]}


def theme(surface, wall, fill, rim=None, surface_depth=3):
    """The five buckets, bottom up. The surface is what is seen from above; the wall and
    the fill are what a cut shows, and a wall is only reached where a face is cut."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": ({"enabled": False, "depth": 1, "material": solid(STONE)} if rim is None
                else {"enabled": True, "depth": rim[0], "material": rim[1]}),
        "surface": {"enabled": True, "depth": surface_depth, "material": surface},
        "wallEnabled": True,
        "wallOnTerrainFaces": True,
        "wall": wall,
        "fill": fill,
    }


# ── the plan ──────────────────────────────────────────────────────────────────
# Three pieces, and no more: the pan is the ground the match is played on, the bench is the
# made terrace the works and the spawn stand on, and the spawn hall sits behind it.
# The hill, the pit and the fall of the pan are relief, not pieces — a piece that exists so
# a theme can hang on it is a plan deciding what the board will look like.
CELL = 5
PAN_SURFACE, BENCH_SURFACE = 12, 18

plan = {
    "plan": 2,
    "meta": {
        "name": "Kilnbrow",
        "notes": ("DTM. One monument a team on an open clay shelf: a spoil hill east to bridge "
                  "from, a worked pit south-west to come up out of, the kiln bench behind. The "
                  "two lands are joined by a build zone over void, never by ground."),
    },
    "globals": {
        "cell": CELL,
        "symmetry": "rot_180",
        "maxPlayers": 12,
        "surface": PAN_SURFACE,
        "observerY": 56,
    },
    "pieces": [
        # blocks x[-35,35] z[-80,-20] — the firing pan, the ground the contest happens on
        {"id": "pan", "role": "piece", "rect": [-7, -16, 14, 12], "surface": PAN_SURFACE},
        # blocks x[-35,35] z[-110,-80] — the kiln bench, made ground five courses up. It is
        # thirty deep because a building wants eight blocks of passable ground on a side
        # and is seven deep itself, and a terrace that cannot answer that is a terrace whose
        # row has no way past it (DR-PASS).
        {"id": "bench", "role": "piece", "rect": [-7, -22, 14, 6], "surface": BENCH_SURFACE},
        # blocks x[-10,10] z[-130,-110] — the spawn hall at the back of the bench
        {"id": "spawn", "role": "spawn", "rect": [-2, -26, 4, 4], "surface": BENCH_SURFACE},
    ],
    "zones": [
        # blocks x[-35,35] z[-20,20] — the whole width, over void. The land ends where the
        # ground stops being anybody's, and the crossing is a decision an attacker makes.
        {"id": "sound", "rect": [-7, -4, 14, 8], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [10, 5], "facing": "back",
             "footprint": [3, 3, 14, 9]},
        ],
        "wools": [],
        # in the yard behind the hall, clear of its shell by more than the cube's own reach
        "iron": [{"id": "iron-1", "piece": "spawn", "at": [10, 16]}],
        # block (-20, -70): 53 blocks from its own spawn by walk and 186 from the enemy's,
        # a ratio of 3.5. It stands well off the centre line, and that is what makes both
        # flanks ground somebody crosses — a goal on the axis leaves them unvisited.
        "destroyables": [
            {"id": "destroyable-1", "piece": "pan", "at": [15, 10],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "Kilnbrow Monument"},
        ],
        "cores": [],
    },
    "walls": [],
    "boxes": [],
}

# ── the themes ────────────────────────────────────────────────────────────────
# Three. The moor is the ground, the works is what somebody built on it, and the pit is the
# one patch of the board made of something else.
#
# The ground family is warm: a dry olive turf over red clay, on a Mesa biome, where the
# grass tint (#90814d) comes to meet the coarse dirt and the clay instead of arguing with
# them. The built family is pale sandstone, which is not the family under its feet. The
# accent is dark oak.
#
# The surface bands cut on the slope axis, and where they cut is read off this board's own
# `incline`: 55.3% of its ground stands under 10°, 14% at 10–19° and 10.1% at 40° or
# steeper. So the turf runs to 20° — a bucket boundary rather than the middle of the 20–29°
# population, which a cut through a flank's own angles stripes row by row — the worked
# shoulder to 45°, and bare clay on everything steeper.
MOOR_FLAT = depth(cells([GRASS, COARSE_DIRT], 11, 17), 1,
                  solid(DIRT), 2)
MOOR_SHOULDER = depth(solid(COARSE_DIRT), 1,
                      solid(DIRT), 2)
MOOR_FACE = depth(cells([HARDENED_CLAY, (STAINED_CLAY, 14)], 9, 23), 2,
                  solid(RED_SANDSTONE), 3)

themes = {
    # the firing-ground: turf where it lies flat, bare red clay where it steepens
    "moor": theme(
        surface=slope(MOOR_FLAT, 30, MOOR_SHOULDER, 20, MOOR_FACE, 40),
        wall=depth(solid(HARDENED_CLAY), 1, solid(RED_SANDSTONE), 2, solid(STONE), 4),
        fill=voronoi([STONE, ANDESITE, DIORITE], 14, 5),
    ),
    # the kiln bench — laid courses above, a striped retaining face where it holds the pan
    "works": theme(
        surface=depth(solid((SANDSTONE, 2)), 1, solid(SANDSTONE), 2),
        wall={"kind": "wallRun", "runs": [
            {"material": solid((SANDSTONE, 1)), "thickness": 1},
            {"material": solid(SANDSTONE), "thickness": 3},
            {"material": solid((STAINED_CLAY, 12)), "thickness": 1},
            {"material": solid(SANDSTONE), "thickness": 4},
        ]},
        fill=voronoi([STONE, ANDESITE], 12, 9),
        rim=(1, solid((SANDSTONE, 1))),        # a made edge is where a rim belongs
    ),
    # the worked pit floor: wet clay and the gravel it is dug out of
    "pit": theme(
        surface=depth(cells([CLAY, GRAVEL], 8, 31), 1, solid(GRAVEL), 2),
        wall=depth(solid(HARDENED_CLAY), 1, solid((STAINED_CLAY, 1)), 2,
                   solid(RED_SANDSTONE), 3),
        fill=voronoi([STONE, ANDESITE], 12, 13),
    ),
}

# ── the flights ───────────────────────────────────────────────────────────────
# The bench is made ground and comes out of the solve, so it meets the pan at an eight-block
# face. A relief graded across that seam would delete the boundary; a flight states it.
# Two of them, because a goal a team defends wants more than one angle onto it. Sixteen
# blocks of run for eight of rise, and a material rather than a theme — a stair is a thing
# somebody built, and it reads as one stone the whole way up.
#
# `height_mode` and `skirt` are what the relief reads; `keepClear` is what the dressing
# reads. Both are needed and neither substitutes for the other, and a shape stating a
# `relief_scope` beside a `height_mode` has the scope silently discarded.
YARD_H = 13
STAIR = depth(solid(COBBLE), 1, solid(STONE), 2, solid(ANDESITE), 3)


def flight(name, x0, x1):
    return {
        "id": name, "type": "polygon", "operation": "add", "override": True,
        "keepClear": True, "floor": 0, "base_height": BENCH_SURFACE,
        "height_mode": "level", "skirt": 0, "material": STAIR,
        "vertices": [[x0, -88], [x1, -88], [x1, -72], [x0, -72]],
        "anchor_heights": [BENCH_SURFACE, BENCH_SURFACE, YARD_H, YARD_H],
    }


# A patch owns the paint on a cell only where its own drawn top is the tallest drawn top
# there, so a patch drawn one course short of the landmass under it paints nothing at all
# and nothing reports it. Both of these state the pan's own `base_height`.
add_shapes = [
    flight("flight-w", -31, -23),
    flight("flight-e", 13, 21),
    # the worked floor of the clay pit, inside the ring the push digs
    {"id": "pit-floor", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": PAN_SURFACE, "theme": "pit",
     "vertices": [[-30, -45], [-22, -47], [-16, -43], [-20, -39], [-29, -40]]},
    # The works' boundary wall along the back of the bench, drawn as a polyline: the
    # rasterizer splines its points before offsetting the band, so four points read as a
    # wall that follows the terrace rather than as a chain of chords.
    {"id": "works-wall", "type": "polyline", "operation": "add", "keepClear": True,
     "floor": 0, "base_height": BENCH_SURFACE + 3, "theme": "works",
     "stroke_edge": "solid", "radius": 1,
     "vertices": [[2, -105], [14, -104], [26, -105], [34, -103]]},
    # the bare, worn clay where the west flight lands on the pan
    {"id": "apron-w", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": PAN_SURFACE, "theme": "pit",
     "vertices": [[-33, -74], [-21, -75], [-19, -67], [-27, -64], [-34, -68]]},
]

# ── the relief ────────────────────────────────────────────────────────────────
# Two long marks facing each other are what a hillside is made of: a field pinned in
# scattered patches relaxes into fans, a field pinned along two opposite edges relaxes into
# the ramp between them. So the pan is pinned low at the bench's foot and lower again at the
# frontline, with one shelf between them holding the ground the monument stands on — open,
# level and exposed, which is what an objective wants around it.
#
# Neither band carries a bevel: a bevel is paid for out of the mark's own floor from every
# side at once, and a five-cell band at a bevel of three pins nothing.
#
# Everything else is left free. Pinning every region leaves the solver nothing to solve.
relief = {
    "team": {
        "base": PAN_SURFACE,
        "reach": 0,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 15, "seed": 3},
        "marks": [
            # the yard at the foot of the retaining face, the whole width
            {"id": "yard", "kind": "area", "h": YARD_H, "bevel": 0,
             "ring": [[-35, -80], [35, -80], [35, -74], [-35, -74]]},
            # the monument's shelf — wide, because an objective wants open ground around it
            # and because a board graded end to end has nowhere to stand on (RL5)
            {"id": "shelf", "kind": "area", "h": 15, "bevel": 3,
             "ring": [[-33, -69], [-20, -71], [-8, -66], [-8, -56], [-20, -51], [-32, -55]]},
            # the frontline apron, where an attacker lands off the build zone. It falls only
            # three blocks from the shelf over nineteen, which is nine degrees and reads as
            # level ground rather than as a ramp.
            {"id": "front", "kind": "area", "h": 12, "bevel": 0,
             "ring": [[-35, -34], [35, -34], [35, -20], [-35, -20]]},
        ],
        "pushes": [
            # The spoil hill. An attacker climbs it and bridges from its head toward the
            # monument, which is the approach from above; its skirt grades at 8/14 = 0.57 a
            # block and its crown at 5/9.5 = 0.53, which is inside RL6's factor of two.
            # Its ring plus its falloff stop clear of the shelf, because a push lifts
            # everything inside that circle whatever a mark states there.
            {"id": "spoil", "amount": 8, "falloff": 10, "crown": 5,
             "roughness": 0, "seed": 4,
             "ring": [[9, -62], [20, -65], [31, -57], [30, -44], [19, -39], [8, -47]]},
            # The worked clay pit. A depression rather than a hole: on a destroy board void
            # belongs between the teams, and a hole cut in a team's own ground empties the
            # ground the contest was supposed to happen on. Seven blocks down over a
            # five-block falloff is a wall whose worst step is three — scrambled out of
            # rather than walked, which is what an entrance from below should cost.
            # `crown` is 0 because a crown is signed in world space and domes a pit's floor
            # back up, and any non-zero crown at this size raises RL6.
            {"id": "pit", "amount": -7, "falloff": 5, "crown": 0,
             "roughness": 0, "seed": 6,
             "ring": [[-32, -46], [-22, -48], [-15, -43], [-19, -38], [-30, -39]]},
        ],
    },
}

# ── the buildings ─────────────────────────────────────────────────────────────
# A kiln row on the bench: one style, three plots, the middle one a storey taller. That is
# a town. Three styles would be three ideas and five would be a swatch book, so what carries
# the variety is shape.
#
# The walls are pale sandstone over a red clay ground, because a building is never the
# ground it stands on. The frame is one wood throughout — post, storey post, beams and the
# laid-log course the beams are the ends of — which is what HS4 and HS9 ask for. There is no
# footing: over a plate of one course it is a rim round a building with no foundation to
# speak of, and it reads as noise rather than as masonry.
KILN_WALL = {"stack": {"bands": [
    {"material": {"kind": "laidLog", "id": LOG2, "data": 1}, "thickness": 1},
    {"material": solid((SANDSTONE, 2)), "thickness": 2},
    {"material": solid(SANDSTONE), "thickness": 5},
], "ending": "repeat"}, "extent": 8}

KILN_SHELL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(SANDSTONE), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                    "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": solid((STAINED_CLAY, 12)),
        "verge": {"kind": "laidLog", "id": LOG2, "data": 1},
        "gable": solid((SANDSTONE, 2)),
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": KILN_WALL,
    "post": solid(DARK_OAK),
    # `stairLattice` is built out of stairs, so the form and the block are one decision
    "windows": {"form": "stairLattice", "block": SANDSTONE_STAIRS, "hostBlock": -1,
                "hostData": 0, "data": 0, "sill": 3, "width": 2, "height": 2, "spacing": 4},
    "storeys": [{
        "clear": 4,
        "wall": {"stack": {"bands": [
            {"material": {"kind": "laidLog", "id": LOG2, "data": 1}, "thickness": 1},
            {"material": solid((SANDSTONE, 2)), "thickness": 2},
            {"material": solid(SANDSTONE), "thickness": 4},
        ], "ending": "repeat"}, "extent": 7},
        "post": solid(DARK_OAK),
        "windows": {"form": "arched", "block": SANDSTONE_STAIRS, "hostBlock": -1,
                    "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2,
                    "spacing": 4},
    }],
    "porch": None,
    "front": None,
    "beams": {"block": LOG2, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": SANDSTONE_STAIRS,
                         "fill": "upperSlab", "fillBlock": SANDSTONE_SLAB[0],
                         "fillData": SANDSTONE_SLAB[1]},
                "width": 2, "height": 3},
}

# ── the rooms ─────────────────────────────────────────────────────────────────
# A spawn and a wool room stamp the studio's built-in bedrock box unless the finish states a
# shell for them, and the box is the first thing every player on the board looks at from the
# inside. The spawn hall is therefore the kiln row's own style, one storey and flat-roofed:
# `flat` is the only roof form that can carry a hole, which is why a room wears it.
SPAWN_SHELL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(SANDSTONE), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                    "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": True,
        "body": solid((STAINED_CLAY, 12)),
        "verge": {"kind": "laidLog", "id": LOG2, "data": 1},
        "gable": solid((STAINED_CLAY, 12)),
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": KILN_WALL,
    "post": solid(DARK_OAK),
    "windows": {"form": "stairLattice", "block": SANDSTONE_STAIRS, "hostBlock": -1,
                "hostData": 0, "data": 0, "sill": 3, "width": 2, "height": 2, "spacing": 4},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": LOG2, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": SANDSTONE_STAIRS,
                         "fill": "upperSlab", "fillBlock": SANDSTONE_SLAB[0],
                         "fillData": SANDSTONE_SLAB[1]},
                "width": 3, "height": 4},
}

# ── the dressing ──────────────────────────────────────────────────────────────
# The routes are drawn before the scenery, because scenery placed first is scenery standing
# in the routes. A path is solid and three colours a reader cannot quite tell apart, and
# these three are the ground's own worn blocks rather than the grey a hard path usually
# takes, so the track reads as part of the works.
#
# The way is two strokes and not one: the flights carry `keepClear`, so a stroke run across
# one would be turned away there anyway, and a stair is not a thing a road should repaint.
TRACK = cells([GRAVEL, COARSE_DIRT, HARDENED_CLAY], 3, 41, rise=0)

TREES = json.load(open(os.path.join(HERE, "trees.json")))
TREE_KEYS = {"acacia-a": "showcase-r8-2", "acacia-b": "showcase-r8-5",
             "olive-a": "showcase-r1-1", "olive-b": "showcase-r1-3"}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}


def rock(pid, x, z, size, seed, form="angular"):
    """A boulder is stone: stone, cobblestone and andesite, and nothing else, whatever the
    board is painted in."""
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "layer": "ground",
            "form": form, "size": size, "mossy": False, "seed": seed,
            "rock": cells([STONE, COBBLE, ANDESITE], 5, seed + 40, rise=4)}


def kiln(pid, x0, z0, x1, z1, seed, storeys_high=0):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground",
            "style": "kiln", "front": "posZ",
            "wings": [{"corners": [[x0, z0], [x1, z1]],
                       "spec": {"ridge": "alongX", "storeysHigh": storeys_high}}]}


dressing = {
    "styles": {
        "kiln": {"kind": "house", "shell": KILN_SHELL},
        **{key: TREES[name] for key, name in TREE_KEYS.items()},
    },
    "props": [
        # the works track: the spawn door down to the head of the west flight, kept out of
        # the lane the spawn's own door claims
        {"id": "track-bench", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[0, -114], [-4, -106], [-9, -98], [-12, -90], [-20, -87], [-27, -87]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},
        # the kiln lane, in front of the row's doors
        {"id": "track-lane", "kind": "stroke", "seed": 6, "layer": "ground",
         "points": [[-26, -90], [-10, -89], [6, -89], [20, -90], [33, -90]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},
        # and the haul road off the flight's foot, down the shelf's western side to the
        # pit, which is the reason the pit is where it is
        {"id": "track-pan", "kind": "stroke", "seed": 7, "layer": "ground",
         "points": [[-27, -72], [-31, -64], [-30, -54], [-27, -45], [-25, -40]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},

        # The kiln row, on the bench, fronting south onto the lane. One style, three plots,
        # the middle one two storeys: a row is buildings that differ in height and footprint
        # and in nothing else. Each is well inside HP3's 192-block cap, each keeps nine
        # blocks of yard on its south side for DR-PASS, and all three stand clear of the
        # x −8…8 lane the spawn's door claims.
        kiln("kiln-w", -26, -100, -16, -93, 311, storeys_high=1),
        kiln("kiln-m", 10, -101, 22, -93, 312, storeys_high=0),
        kiln("kiln-e", 26, -100, 34, -93, 313, storeys_high=1),

        # Trees to the outside of the pan, never on the approach in front of the monument
        # and never on the brink an attacker arrives at. Every one stands more than eleven
        # blocks from the monument's marker, which clears OB19's 21×21 clearance, and more
        # than three from any claimed paving, which clears DR-ROAD.
        tree("tree-w1", "acacia-a", -34, -78),
        tree("tree-w2", "olive-a", -33, -24),
        tree("tree-e1", "acacia-b", 33, -76),
        tree("tree-e2", "olive-b", 33, -46),
        # one on the spoil hill's own shoulder, where a climber tops out
        tree("tree-h1", "acacia-a", 16, -52),

        # Boulders on flat ground: a rock pinned to a face reads as neither the rock nor the
        # face, and a prop seats on the lowest column its feet cover, so a stepped cell
        # buries half of it.
        rock("rock-y1", 3, -77, 3, 21),
        rock("rock-p2", -31, -31, 3, 22, form="round"),
        rock("rock-e1", 30, -27, 4, 23),

        # Ground cover over the whole board rather than a patch of it: the density field is
        # better at patchiness than a hand-drawn polygon, and several small shapes come out
        # as islands of planting with bare ground between them where no edge exists.
        # Both of its gameplay numbers stay low — two-block grass is cover nobody authored,
        # in front of an objective nobody chose.
        {"id": "sward", "kind": "flora", "seed": 9,
         "points": [[-35, -108], [35, -108], [35, -38], [-35, -38]],
         "spec": {"coverage": 0.24, "scale": 26, "octaves": 2,
                  "fernShare": 0.22, "flowerShare": 0.10, "flowerScale": 34,
                  "tallShare": 0.05}},
    ],
}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    # Mesa, #90814d. A tinted block takes its colour from the chunk's biome byte and nothing
    # else on a board does, so this is a palette decision rather than a line added at the end.
    "biome": {"kind": "solid", "id": 37},
    "roomStyles": {"spawn": SPAWN_SHELL},
    "mapTheme": "moor",
    "themes": themes,
    # Keyed on the compiled shape ids, read off POST /plan/compile: the compiler fuses the
    # pieces that share a height, so the pan is `bench-12` and the bench and the spawn
    # together are `bench-18`.
    "themeById": {"bench-18": "works"},
    # The bench is made ground, so it comes out of the solve and the two tiers meet at a
    # face: `hold` would let the relief bring the pan up to it and there would be no step
    # for a stair to state. It is the taller add over its own columns, so it keeps 18.
    "shapePropsById": {"bench-18": {"relief_scope": "exclude"}},
    "addShapes": add_shapes,
    "relief": relief,
    "dressing": dressing,
}


def write(name, document):
    path = os.path.join(HERE, name)
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
        handle.write("\n")
    print(f"wrote {path}")


write(f"{SLUG}.plan.json", plan)
write(f"{SLUG}.finish.json", finish)
