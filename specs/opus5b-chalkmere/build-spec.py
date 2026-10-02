#!/usr/bin/env python3
"""opus5b-chalkmere — destroy the monument.

A chalk downland split by a dry combe: each team's monument stands alone on a
pale turf shoulder above its own steading, and the two downs are joined only by
a build zone over the gap between them — so every attack is a crossing made in
the open, and the combe is the one place to drop out of sight once across.

Tone families: the ground is pale chalk and turf, what is built is dark flint
and cobble, and the accent is weathered oak.

Writes opus5b-chalkmere.plan.json and opus5b-chalkmere.refinement.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit

SLUG = "opus5b-chalkmere"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# Four pieces a team. The down is the board; the steading and the two folds are
# the shallow back band the spawn hall is seated in, so the hall is not a
# promontory with void on three sides.
#
# blocks:  down      x -24..24   z   8..92
#          fold-w    x -24..-16  z  92..108
#          steading  x -16..4    z  92..108   (20 x 16 - inside ST10's cap)
#          fold-e    x   4..24   z  92..108
#          strait    x -24..24   z -16..16    a build zone over 16 blocks of void
#
# Three numbers here were read rather than chosen, all of them off the dead
# share. The first cut was 72 blocks wide and G8 read 0.272 against its band
# of [0, 0.12], because the flanks were ground no journey went to; the back
# band was 24 blocks deep and the ground behind a spawn is ground nobody walks
# (SP2); and at 56 wide the built board still read GET .../coverage 0.1208,
# with its four largest dead patches in the back corners of the band. So the
# board is 48 wide and the band stops where the down's corners did.

SPAWN_AT = (-5, 100)           # blocks, world - the hall's own centre
GOAL_AT = (12, 62)             # blocks, world - off the centre line on purpose

DOWN_MIN = (-24, 8)            # the down piece's minimum corner, in blocks
STEAD_MIN = (-16, 92)

plan = {
    "plan": 2,
    "meta": {"name": "Chalkmere"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "down", "role": "piece", "rect": [-6, 2, 12, 21], "surface": 9},
        {"id": "fold-w", "role": "piece", "rect": [-6, 23, 2, 4], "surface": 19},
        {"id": "steading", "role": "spawn", "rect": [-4, 23, 5, 4], "surface": 19},
        {"id": "fold-e", "role": "piece", "rect": [1, 23, 5, 4], "surface": 19},
    ],
    "zones": [
        {"id": "strait", "rect": [-6, -4, 12, 8], "holes": []},
    ],
    "placements": {
        # The hall is 10 x 12 inside a 20 x 16 piece, which leaves a six-block
        # strip down the west side; the iron cube stands in that strip with two
        # blocks of air to the shell, which is what WX8 asks for. Both numbers
        # come from POST /plan/room rather than from arithmetic.
        "spawns": [{"id": "spawn-steading", "piece": "steading",
                    "at": [SPAWN_AT[0] - STEAD_MIN[0], SPAWN_AT[1] - STEAD_MIN[1]],
                    "facing": "front", "footprint": [6, 2, 10, 12]}],
        "wools": [],
        "iron": [{"id": "iron-steading", "piece": "steading", "at": [2.5, 8.0]}],
        "destroyables": [{"id": "monument", "piece": "down",
                          "at": [GOAL_AT[0] - DOWN_MIN[0], GOAL_AT[1] - DOWN_MIN[1]],
                          "style": "pillar-3", "materials": "obsidian",
                          "float": 4, "name": "Chalkmere Monument"}],
        "cores": [],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# Three marks and two pushes. The strand is the shelf a bridger lands on, the
# shoulder is the open turf the monument stands alone on, and the apron is the
# steading's flat. Everything between them is unpinned, which is where the
# ground gets its shape.
#
# The nab is the hill an attacker climbs to bridge at the monument from above;
# the combe is the hollow on the other hand, an entrance from below that opens
# onto the strand. Each push's ring plus its falloff clears the shoulder mark.
#
# Every ring the ground is drawn with — the marks and the push here, the
# patches, the pond and the flora below — is a lobed outline written out point
# by point: a circle with each radius pushed in or out, or a rectangle walked
# with each point moved off its edge. A rectangle builds a mesa with sheer
# square sides; a ring of this shape is indistinguishable from ground.

relief = {
    "*": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="rolling",
        grain=kit.ReliefGrainJson(amplitude=1.5, scale=20, seed=4103),
        marks=[
            # the rectangle x -26..26, z 4..24, every point moved up to 2.5 blocks along each axis
            kit.ReliefMarkJson(id="strand", kind="area", h=9, bevel=2, ring=[
                [-25.56, 3.53], [-10.71, 2.05], [-2.47, 5.73], [13.07, 4.32], [24.41, 1.67], [24.06, 6.69],
                [23.71, 15.17], [28.49, 18.5], [26.5, 24.71], [11.77, 24.14], [-2.16, 22.04], [-13.93, 24.53],
                [-26.59, 24.42], [-27.74, 18.74], [-24.12, 12.15], [-24.88, 10.32]]),
            # radius 13 round the monument's (12, 62), every radius up to 20% off
            kit.ReliefMarkJson(id="shoulder", kind="area", h=17, bevel=4, ring=[
                [26.43, 62.0], [24.75, 70.2], [17.64, 74.34], [9.91, 76.53], [4.23, 70.96], [-1.09, 65.84],
                [0.41, 58.6], [4.34, 53.16], [10.21, 49.54], [17.25, 50.51], [24.88, 53.72]]),
            # the rectangle x -26..26, z 88..112, every point moved up to 2.5 blocks along each axis
            kit.ReliefMarkJson(id="steading-apron", kind="area", h=19, bevel=4, ring=[
                [-23.69, 87.62], [-14.2, 88.18], [0.28, 87.5], [11.15, 90.19], [26.8, 89.62], [27.38, 92.55],
                [24.98, 99.26], [25.33, 106.98], [26.23, 112.17], [11.54, 110.57], [-2.14, 109.89],
                [-10.63, 112.71], [-27.74, 111.39], [-23.83, 103.71], [-27.92, 102.23], [-28.47, 96.12]]),
            # The combe is a mark rather than a push. Drawn as a push it took
            # its floor down to y1 — the ground there solves to 9 and the lift
            # is arithmetic on the answer — and the pool in it then cut three
            # courses of bank away and raised DR-BANK, because a push dishes
            # and a pool's line is the lowest surface it crosses. A pinned pan
            # is level, and water fills whatever is level.
            # Its ring: radius 12 round (-16, 46), every radius up to 22% off.
            kit.ReliefMarkJson(id="combe-pan", kind="area", h=7, bevel=5, ring=[
                [-2.27, 46.0], [-5.33, 51.6], [-8.38, 57.04], [-14.45, 58.8], [-19.9, 56.28], [-23.7, 52.83],
                [-26.18, 48.51], [-29.25, 42.73], [-23.18, 39.64], [-20.77, 33.41], [-14.81, 36.19],
                [-10.49, 38.01], [-5.06, 40.26]]),
        ],
        pushes=[
            # radius 8 round (15, 28), every radius up to 22% off
            kit.ReliefPushJson(id="nab", amount=11, falloff=11, crown=4, roughness=1.2, seed=4122, ring=[
                [22.84, 28.0], [21.11, 33.13], [16.37, 35.76], [11.45, 34.14], [6.62, 31.05], [7.08, 25.12],
                [10.83, 20.78], [16.35, 20.34], [21.31, 22.71]]),
        ]),
}

# ---------------------------------------------------------------- the paint
#
# Three themes. The down is the board's one ground, finished on the slope axis
# so the shoulder of a hill is not painted like the meadow beside it; the combe
# floor and the steading yard are the two places that are made of something
# else, and each is a shape carrying its own theme.
#
# The band edges are cut off this board's own GET .../incline.


def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def cells(seed, size, rise, palette):
    """A cell material at jitter 45 and warp 1, which every one on this board is cut at."""
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=45, warp=1, rise=rise, palette=palette)


def band(thickness, material):
    return kit.Band(material=material, thickness=thickness)


def stack(axis, bands):
    """A layered material: `bands` read along `axis`, the last carried on for good."""
    return kit.LayeredMaterial(axis=axis, stack=kit.BandStack(ending="repeat", bands=bands))


def soil(top, under, depth=2):
    """One course of a surfacing block over `depth` of soil — what PT1 wants."""
    return stack("depth", [band(1, top), band(depth, under)])


CHALK = solid(24, 0)             # sandstone — the chalk itself
CHALK_SMOOTH = solid(24, 2)
FLINT = solid(1, 5)              # andesite
TURF = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)               # coarse dirt
GRAVEL = solid(13, 0)

CHALK_FACE = cells(4131, 7, 5, [CHALK, CHALK_SMOOTH])

# The slope band edges are this board's own: GET .../incline reads 45.4% of
# its ground under 10 degrees, 24.9% between 10 and 19, and 11.7% at 40 or
# steeper, so cuts at 20 and 38 fall between three real populations and
# neither of them runs through the middle of one.
SLOPE_TURF, SLOPE_WORN = 20, 38

down_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=CHALK,
    wall=CHALK_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=CHALK),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3, material=stack("slope", [
        band(SLOPE_TURF, soil(TURF, EARTH)),
        band(SLOPE_WORN - SLOPE_TURF, soil(WORN, EARTH)),
        band(90 - SLOPE_WORN, stack("depth", [band(3, CHALK_FACE)])),
    ])),
)

combe_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=CHALK,
    wall=CHALK_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=False, depth=1, material=CHALK),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3, material=soil(cells(4132, 6, 0, [GRAVEL, WORN]), EARTH)),
)

yard_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=CHALK,
    wall=cells(4133, 6, 4, [FLINT, solid(4, 0)]),
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=solid(4, 0)),
    rimEdges="boundary",
    surface=kit.TopBand(enabled=True, depth=3,
                        material=soil(cells(4134, 5, 0, [solid(4, 0), FLINT, solid(98, 0)]), solid(1, 0))),
)

# ---------------------------------------------------------------- the shapes
#
# Two patches on the ground layer, each stating the compiled down's own
# base_height so it forms the surface of the cells it covers, and one made
# layer: the dry-stone wall that encloses the steading yard, drawn as a
# polyline so it flows rather than turning square corners.

# The compile emits one shape per surface: down-9 for the board and down-19 for
# the back band. A patch owns the paint on a cell only where its own drawn top
# equals the tallest drawn top there, so each of the two states the base_height
# of the ground it lies on. The first cut stated 10 for both and the yard
# painted 100 cells of the 480 it covers.
DOWN_LOW, DOWN_HIGH = 9, 19

add_shapes = [
    # radius 13 round (-16, 46), every radius up to 22% off
    kit.SketchShape(id="combe-floor", type="polygon", operation="add",
                    floor=0, base_height=DOWN_LOW, theme="combe", vertices=[
        [-4.78, 46.0], [-3.65, 52.48], [-8.67, 56.62], [-14.43, 58.94], [-20.14, 56.91], [-24.33, 53.38],
        [-30.08, 49.47], [-26.87, 43.32], [-25.02, 38.01], [-21.41, 31.75], [-14.72, 35.49], [-8.27, 34.8],
        [-2.69, 39.01]]),
    # the rectangle x -20..10, z 90..106, every point moved up to 2 blocks along each axis
    kit.SketchShape(id="steading-yard", type="polygon", operation="add",
                    floor=0, base_height=DOWN_HIGH, theme="yard", vertices=[
        [-20.5, 88.69], [-13.96, 88.88], [-4.83, 91.8], [2.79, 91.49], [10.29, 89.15], [11.64, 94.77],
        [11.93, 97.33], [8.8, 101.95], [8.97, 105.87], [0.63, 104.67], [-4.47, 106.64], [-12.28, 106.66],
        [-18.73, 105.58], [-20.99, 100.66], [-21.59, 97.08], [-21.64, 95.03]]),
]

yard_wall = kit.AddedLayer(
    id="yard-wall", name="the steading wall", base_y=0,
    kind="made", part_of="steading",
    groups=[kit.SketchGroup(id="yard-wall", name="the steading wall",
                            mirrors=True,
                            shapeIds=["yard-wall-west", "yard-wall-east"])],
    shapes=[
        # a polyline rather than a chain of rectangles: the rasterizer splines
        # the points before offsetting the band, so six points draw a wall that
        # flows round the yard. The studio's kinds are rectangle, circle,
        # polygon, lasso and polyline — "path" is what the schema calls it and
        # SK3 is what the store answers to that word.
        # Two runs rather than one. A single run round the yard crossed the
        # hall's own footprint and SK18 read twenty columns where the made
        # thing and the stamped room hold the same courses: the rasterizer lays
        # one and the stamper writes the other, and neither reads the other.
        kit.SketchShape(id="yard-wall-west", type="polyline", operation="add",
                        floor=19, base_height=2, radius=1.0,
                        stroke_edge="solid", keepClear=True,
                        material=cells(4151, 4, 2, [solid(4, 0), FLINT]),
                        vertices=[[-19, 91], [-20, 97], [-18, 103], [-13, 106]]),
        kit.SketchShape(id="yard-wall-east", type="polyline", operation="add",
                        floor=19, base_height=2, radius=1.0,
                        stroke_edge="solid", keepClear=True,
                        material=cells(4151, 4, 2, [solid(4, 0), FLINT]),
                        vertices=[[3, 107], [8, 104], [11, 98], [10, 92]]),
    ],
)

# ---------------------------------------------------------------- the dressing
#
# Four ideas, and each thing is where it is because there is an answer to why
# there. The west approach is composed: a dew pond in the combe a player drops
# into, a two-house fold on the west bank to be fought through, and a beech
# shaw between the fold and the monument that carries cover to within fifteen
# blocks of it. The east approach is the nab, which is bare on purpose —
# climbing it and bridging down is the other way in, and the ground in front of
# a goal wants reading at a glance.
#
# Every position below was taken off POST .../sketch/seats for its own kind,
# which is a raster of the cells a footprint's minimum corner may sit on; none
# was chosen by eye.

# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()

styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "beech": "dense-oak-3",     # the shaw
    "thorn": "tiny-oak-4",      # the rim
}.items()}
styles["flint-rock"] = kit.BoulderStyle(
    form="round", size=2, mossy=False,
    rock=kit.TurbulenceMaterial(seed=4161, scale=3, octaves=3, stops=[solid(1, 0), solid(4, 0), FLINT], rise=3))

PAVE = cells(4162, 3, 0, [GRAVEL, WORN, solid(4, 0)])

FLINTS = [(-4, 30), (-22, 56), (12, 28)]

props = [
    # The routes are drawn before the scenery, because circulation is decided
    # first: the door of the hall to the monument, and the monument forward to
    # the strand a crossing lands on. Both are solid and three tones a reader
    # cannot quite tell apart.
    kit.StrokeProp(id="steading-track", seed=4171, radius=2,
                   style="solid", claimsGround=True, pave=PAVE,
                   points=[[-5, 94], [-3, 86], [2, 78], [8, 70], [11, 66]]),
    kit.StrokeProp(id="forward-track", seed=4172, radius=2,
                   style="solid", claimsGround=True, pave=PAVE,
                   points=[[12, 54], [11, 42], [8, 30], [4, 18], [2, 10]]),

    # the dew pond in the combe floor — the reason to drop into it; its ring is
    # radius 6 round (-16, 46), every radius up to 20% off
    kit.FluidProp(id="dew-pond", seed=4173, shape="pool",
                  radius=2, depth=2, shore=3, shoreWander=True,
                  bank=cells(4175, 4, 0, [GRAVEL, solid(82, 0), WORN]), points=[
        [-10.36, 46.0], [-11.5, 49.78], [-14.77, 53.0], [-18.45, 50.25], [-21.31, 47.93], [-22.39, 43.67],
        [-18.92, 40.93], [-14.81, 39.22], [-11.95, 42.6]]),

    # the fold: one style, two plots, one of them a storey taller and wider
    kit.HouseProp(id="fold-house", seed=4176, style="fold-house", front="posX",
                  wings=[kit.AuthoredWing(corners=[[-24, 62], [-14, 69]], spec=kit.WingSpec(storeysHigh=2))]),
    kit.HouseProp(id="fold-byre", seed=4177, style="fold-house", front="posX",
                  wings=[kit.AuthoredWing(corners=[[-24, 76], [-16, 82]], spec=kit.WingSpec(storeysHigh=1))]),
]

# the shaw — five beeches west of the monument, trunk to trunk no closer than
# the larger of two crowns, and the nearest of them fifteen blocks off the
# monument's own anchor
props += [kit.TreeProp(id=f"beech-{i}", seed=4200 + i, x=x, z=z, style="beech")
          for i, (x, z) in enumerate([(-10, 52), (-4, 57), (-9, 63), (-2, 68),
                                      (-4, 48)])]
# two thorns on the combe's rim, to the outside of the piece rather than down
# the middle of it
props += [kit.TreeProp(id=f"thorn-{i}", seed=4220 + i, x=x, z=z, style="thorn")
          for i, (x, z) in enumerate([(-20, 30), (-8, 34)])]
# three flints, each on ground flat enough to hold one
# Three flints, each on ground the incline read calls flat: a boulder is a
# mass the ice left, so DR-STEEP turns one away from a face, and the first cut
# put all three on 41, 48 and 54 degrees.
props += [kit.BoulderProp(id=f"flint-{i}", seed=4240 + i, x=x, z=z, style="flint-rock")
          for i, (x, z) in enumerate(FLINTS)]

props += [
    # the rectangle x -24..24, z 8..106, every point moved up to 2 blocks along each axis
    kit.FloraProp(id="flora", seed=4180, points=[
        [-23.37, 6.04], [-11.93, 6.14], [-0.86, 7.11], [10.38, 8.72], [25.48, 8.81], [23.47, 30.62],
        [25.76, 56.63], [25.5, 82.53], [24.66, 107.44], [12.49, 106.22], [-1.14, 104.39], [-12.25, 107.47],
        [-24.67, 105.53], [-24.11, 80.54], [-24.83, 57.69], [-23.67, 32.08]],
        spec=kit.FloraSpec(coverage=0.22, scale=26, octaves=3, fernShare=0.12,
                           flowerShare=0.10, flowerScale=18, tallShare=0.05)),
]

# ---------------------------------------------------------------- the house
#
# The ground is pale chalk, so what is built on it is dark timber over a cobble
# plinth: a building has to read as a built thing from across the board, which
# means its walls are not in the tone family under its feet. One style, and the
# variety is in the plan rather than in a second palette.
#
# The frame is one wood throughout — post, beam, every storey's post and the
# laid-log course the beams are the ends of — which is what HS4 and HS9 ask.

SPRUCE = solid(5, 1)
DARKOAK = solid(5, 5)
SPRUCE_LOG = kit.LaidLogMaterial(id=17, data=1)

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}


def steading_storey(height):
    """A storey `height` courses tall and clear: a course of cobble, spruce and dark oak up to the last course, and
    that one of laid spruce log."""
    return {
        "clear": height,
        "wall": {"stack": {"bands": [
            {"material": solid(4, 0), "thickness": 1},
            {"material": cells(4191, 3, 2, [SPRUCE, DARKOAK]), "thickness": height - 2},
            {"material": SPRUCE_LOG, "thickness": 1}], "ending": "repeat"},
            "extent": height},
        "post": solid(17, 1),
        "windows": {"form": "arched", "block": 134, "hostBlock": -1, "hostData": 0,
                    "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "surface": PLAIN_SURFACE, "deck": None, "headroom": height,
    }


CHALK_HOUSE = kit.build("HouseStyle", {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(4, 0), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 1,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": SPRUCE, "verge": DARKOAK, "gable": DARKOAK,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": solid(4, 0), "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 1),
    "windows": NO_WINDOW,
    "storeys": [steading_storey(5)],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
})

# The spawn hall is the same steading built taller and hipped, so what a player
# walks out of belongs to the farm rather than to the studio's bedrock default.
SPAWN_HALL = kit.build("HouseStyle", {
    **CHALK_HOUSE,
    "roof": {"form": "hip", "pitch": 2, "slab": 126, "slabData": 1,
             "overhang": 1, "ridgeCap": False, "hole": False,
             "body": SPRUCE, "verge": DARKOAK, "gable": None,
             "gableWindows": NO_WINDOW},
    "storeys": [steading_storey(7)],
})

styles["fold-house"] = kit.HouseStyleRef(shell=CHALK_HOUSE)

refinement = kit.Refinement(
    authors=["Opus 5"],
    created="2026-09-21",
    themes={"down": down_theme, "combe": combe_theme, "yard": yard_theme},
    mapTheme="down",
    # Plains: grass at #91bd59 reads fresh against sandstone, which is what a
    # chalk down wants. Asked of GET /api/terrain/biomes rather than assumed.
    biome=kit.SolidBiome(id=1),
    relief=relief,
    addShapes=add_shapes,
    addLayers=[yard_wall],
    roomStyles=kit.SketchRoomStyles(spawn=SPAWN_HALL, wool=SPAWN_HALL),
    dressing=kit.DressingDoc(styles=styles, props=props),
)

for part, document in (("plan", plan), ("refinement", refinement)):
    path = os.path.join(HERE, f"{SLUG}.{part}.json")
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
    print(f"wrote {path}")
