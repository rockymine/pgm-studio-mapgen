#!/usr/bin/env python3
"""opus5b-alderquay — a wool and a monument at once.

A dark alder holt on a slow backwater: each team's monument stands out in the
open on a timber quay at the water's edge, where anyone crossing the delta can
see it; the wool it defends sits in a room on a spur at the back, past a
prepared bedrock line. So a team is fighting for two different things at two
different depths, and the ground that carries the raid out to the enemy's spur
is the same ground its own monument watches.

Tone families: the ground is dark and wet — podzol, coarse dirt, clay; what is
built is white plaster framed in dark oak; the accent is the water.

Writes opus5b-alderquay.plan.json and opus5b-alderquay.refinement.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit

SLUG = "opus5b-alderquay"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# blocks:  eyot-w     x -36..-20  z  16..44   surface  9   the west delta island
#          eyot-e     x  20..36   z  16..44   surface  9   the east one
#          holt-w     x -36..-20  z  44..72   surface 11   the west bank
#          holt-e     x  12..36   z  44..72   surface 11   the east bank and the quay
#          holt-n     x -20..12   z  60..72   surface 11   the head of the channel
#          spur       x -36..-20  z  72..92   surface 15   the wool approach
#          wool-room  x -36..-20  z  92..104  surface 15
#          yard       x   4..36   z  72..92   surface 15   the timber works
#          yard-w     x   4..8    z  92..112  surface 15
#          camp       x   8..28   z  92..112  surface 15   the spawn (20 x 20)
#          yard-e     x  28..36   z  92..112  surface 15
#          mid-band   x -36..36   z -16..16   the build zone over the delta
#
# The void down the middle is the delta's own channel, and it reaches the mid
# rather than sitting inside the team's ground: approaches.md withdraws the
# middle-of-terrain hole on a destroy board, and what it endorses instead is a
# river, which is what this is — a drop that forces a bridge, a chokepoint that
# has to be built before it can be used. The backwater on the west bank is the
# other half of that ruling, a depression a player drops into and comes up
# under the wool approach.
#
# Two frontline legs rather than one face: a single piece across the whole
# board read FR6 frontline-width 18 against a band of [1, 16]; each eyot reads
# four.
#
# The monument stands on the open bank above the quay, a short walk
# forward of its own spawn — the destroy topology, where the thing a team
# defends is its own and the contested space is everything beyond it. The wool
# it defends is on the far side of the board behind a bedrock line, which is
# the capture topology. A team fights for two things at two depths.
#
# The spur is exactly the width of the interface the wall is stamped on, so
# there is no shoulder of ground past the wall's ends for a player to walk
# round; a wall with a way round it has stopped being a decision.

SPAWN_AT = (19, 102)
GOAL_AT = (30, 52)
HOLT_E_MIN = (12, 44)
CAMP_MIN = (8, 92)

plan = {
    "plan": 2,
    "meta": {"name": "Alderquay"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "eyot-w", "role": "piece", "rect": [-9, 4, 4, 7], "surface": 9},
        {"id": "eyot-e", "role": "piece", "rect": [5, 4, 4, 7], "surface": 9},
        {"id": "holt-w", "role": "piece", "rect": [-9, 11, 4, 7], "surface": 11},
        {"id": "holt-e", "role": "piece", "rect": [3, 11, 6, 7], "surface": 11},
        {"id": "holt-n", "role": "piece", "rect": [-5, 15, 8, 3], "surface": 11},
        {"id": "spur", "role": "piece", "rect": [-9, 18, 4, 5], "surface": 15},
        {"id": "wool-room", "role": "wool-room", "rect": [-9, 23, 4, 3], "surface": 15},
        {"id": "yard", "role": "piece", "rect": [1, 18, 8, 5], "surface": 15},
        {"id": "yard-w", "role": "piece", "rect": [1, 23, 1, 5], "surface": 15},
        {"id": "camp", "role": "spawn", "rect": [2, 23, 5, 5], "surface": 15},
        {"id": "yard-e", "role": "piece", "rect": [7, 23, 2, 5], "surface": 15},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-9, -4, 18, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-camp", "piece": "camp",
                    "at": [SPAWN_AT[0] - CAMP_MIN[0], SPAWN_AT[1] - CAMP_MIN[1]],
                    "facing": "front", "footprint": [6, 2, 10, 16]}],
        "wools": [{"id": "wool-spur", "piece": "wool-room", "at": [8, 6]}],
        "iron": [{"id": "iron-camp", "piece": "camp", "at": [2.5, 10.0]}],
        "destroyables": [{"id": "monument", "piece": "holt-e",
                          "at": [GOAL_AT[0] - HOLT_E_MIN[0],
                                 GOAL_AT[1] - HOLT_E_MIN[1]],
                          "style": "pillar-3", "materials": "obsidian",
                          "float": 4, "name": "Alderquay Monument"}],
        "cores": [],
    },
    "walls": [{"a": "holt-w", "b": "spur"}],
}

# ---------------------------------------------------------------- the ground
#
# Every ring the ground is drawn with — the marks and pushes here, the patches,
# the pool and the flora below — is a lobed outline written out point by point:
# a circle with each radius pushed in or out, or a rectangle walked with each
# point moved off its edge. A rectangle builds a mesa with sheer square sides;
# a ring of this shape is indistinguishable from ground.

relief = {
    "*": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="rolling",
        grain=kit.ReliefGrainJson(amplitude=1.5, scale=20, seed=7103),
        marks=[
            # the rectangle x -38..38, z 12..42, every point moved up to 3 blocks along each axis
            kit.ReliefMarkJson(id="strand", kind="area", h=9, bevel=2, ring=[
                [-36.67, 10.55], [-19.13, 13.44], [-1.57, 12.9], [18.6, 12.99], [37.12, 14.13], [40.11, 21.14],
                [37.4, 27.63], [39.98, 32.94], [38.94, 42.35], [18.14, 40.4], [-0.6, 44.11], [-19.78, 42.92],
                [-38.14, 44.4], [-40.73, 33.83], [-37.26, 26.39], [-39.9, 17.42]]),
            # the rectangle x -38..38, z 46..70, every point moved up to 3 blocks along each axis
            kit.ReliefMarkJson(id="holt-flat", kind="area", h=11, bevel=4, ring=[
                [-35.55, 47.6], [-21.23, 45.72], [0.08, 45.56], [17.45, 45.11], [38.55, 44.51], [39.1, 54.15],
                [38.16, 60.49], [38.08, 66.32], [35.77, 67.03], [21.0, 70.45], [2.42, 72.02], [-17.79, 68.03],
                [-38.83, 71.78], [-38.39, 62.11], [-39.54, 56.84], [-39.05, 53.4]]),
            # The backwater's pan. Water fills whatever is level, so the pool
            # is the size of the pan rather than of the outline drawn for it —
            # and a pool drawn across a grade cuts a shaft in the bank instead,
            # which is what DR-BANK says.
            # Its ring: radius 9 round (-28, 58), every radius up to 22% off.
            kit.ReliefMarkJson(id="pool-pan", kind="area", h=8, bevel=3, ring=[
                [-20.6, 58.0], [-21.18, 62.38], [-23.8, 67.2], [-29.09, 65.6], [-34.64, 65.67], [-35.51, 60.21],
                [-34.93, 55.97], [-32.7, 52.58], [-29.47, 47.8], [-24.02, 49.29], [-20.38, 53.1]]),
            # the rectangle x -38..-18, z 74..108, every point moved up to 2 blocks along each axis
            kit.ReliefMarkJson(id="spur-pad", kind="area", h=15, bevel=3, ring=[
                [-38.87, 75.13], [-33.28, 75.52], [-29.74, 75.93], [-21.56, 74.91], [-19.73, 72.17],
                [-18.61, 80.62], [-16.87, 91.14], [-16.48, 98.23], [-19.71, 109.58], [-21.85, 107.05],
                [-26.37, 109.23], [-33.55, 106.83], [-39.47, 108.37], [-39.14, 100.62], [-38.07, 89.49],
                [-37.58, 84.08]]),
            # the rectangle x 2..38, z 74..116, every point moved up to 2 blocks along each axis
            kit.ReliefMarkJson(id="yard-pad", kind="area", h=15, bevel=3, ring=[
                [1.88, 73.17], [9.33, 74.37], [19.36, 75.04], [29.67, 73.65], [37.23, 73.75], [36.72, 82.96],
                [39.63, 96.38], [38.26, 106.83], [38.18, 115.37], [28.05, 116.42], [19.64, 117.18],
                [11.77, 116.9], [0.07, 115.95], [2.42, 105.81], [0.41, 93.12], [2.99, 84.4]]),
        ],
        pushes=[
            # radius 7 round (-28, 28), every radius up to 22% off
            kit.ReliefPushJson(id="bank-swell", amount=7, falloff=9, crown=3, roughness=1.4, seed=7122, ring=[
                [-20.73, 28.0], [-23.01, 32.19], [-26.52, 36.37], [-32.07, 35.05], [-36.0, 30.91],
                [-34.36, 25.68], [-31.53, 21.89], [-26.76, 20.99], [-22.08, 23.03]]),
            # radius 6 round (30, 28), every radius up to 20% off
            kit.ReliefPushJson(id="alder-rise", amount=6, falloff=8, crown=2, roughness=1.2, seed=7124, ring=[
                [37.11, 28.0], [34.34, 31.64], [30.95, 33.41], [27.24, 32.78], [24.26, 30.09], [23.28, 25.55],
                [27.44, 23.57], [31.21, 21.12], [34.07, 24.59]]),
        ]),
}

# ---------------------------------------------------------------- the paint


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


TURF = solid(2, 0)
PODZOL = solid(3, 2)
EARTH = solid(3, 0)
WORN = solid(3, 1)
CLAY = solid(82, 0)
GRAVEL = solid(13, 0)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
ANDESITE = solid(1, 5)
STONEBRICK = solid(98, 0)
DARKOAK = solid(5, 5)
PLASTER = solid(159, 0)

BANK_FACE = cells(7131, 7, 5, [STONE, CLAY])

# Cut off this board's own GET .../incline, which reads 55.7% of the ground
# under 10 degrees, 20.7% between 10 and 19, 13% between 20 and 29 and 3.7%
# at 40 or steeper. The cuts at 20 and 40 put the wood's floor on three
# quarters of the board, the worn clay bank on the fifth that is shoulder, and
# bare rock only on what is actually a face.
SLOPE_WOOD, SLOPE_BANK = 20, 40

carr_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=STONE,
    wall=BANK_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=WORN),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3, material=stack("slope", [
        band(SLOPE_WOOD, soil(cells(7132, 9, 0, [TURF, PODZOL]), EARTH)),
        band(SLOPE_BANK - SLOPE_WOOD, soil(cells(7133, 7, 0, [WORN, CLAY]), EARTH)),
        band(90 - SLOPE_BANK, stack("depth", [band(3, BANK_FACE)])),
    ])),
)

reed_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=STONE,
    wall=BANK_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=False, depth=1, material=WORN),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3, material=soil(cells(7134, 6, 0, [CLAY, GRAVEL]), EARTH)),
)

works_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=STONE,
    wall=cells(7135, 5, 4, [STONEBRICK, ANDESITE]),
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=STONEBRICK),
    rimEdges="boundary",
    surface=kit.TopBand(enabled=True, depth=3,
                        material=soil(cells(7136, 5, 0, [COBBLE, ANDESITE, STONEBRICK]), STONE)),
)

# ---------------------------------------------------------------- the shapes

FLATS_BASE, HOLT_BASE, BACK_BASE = 9, 11, 15

add_shapes = [
    # radius 12 round (-28, 58), every radius up to 20% off
    kit.SketchShape(id="reed-bed", type="polygon", operation="add",
                    floor=0, base_height=HOLT_BASE, theme="reed", vertices=[
        [-16.85, 58.0], [-17.31, 63.61], [-22.54, 65.91], [-26.76, 68.18], [-32.26, 69.22], [-38.7, 67.48],
        [-40.51, 61.08], [-38.65, 55.37], [-37.0, 50.03], [-32.62, 45.82], [-26.37, 44.57], [-21.62, 48.75],
        [-18.59, 53.06]]),
    # the rectangle x 6..34, z 76..110, every point moved up to 2 blocks along each axis
    kit.SketchShape(id="works-ground", type="polygon", operation="add",
                    floor=0, base_height=BACK_BASE, theme="works", vertices=[
        [6.04, 74.1], [13.62, 77.4], [21.11, 77.02], [26.97, 77.89], [34.97, 74.44], [34.61, 84.21],
        [33.36, 91.82], [32.13, 100.8], [33.2, 109.53], [25.54, 111.49], [21.86, 109.62], [13.45, 110.85],
        [7.65, 110.84], [4.58, 99.92], [7.4, 93.16], [6.2, 83.09]]),
]

# The quay: a plank deck one course proud of the holt at the pool's north edge,
# and the ground the monument stands on. It is a made layer, so SK10's pair
# walk and SK11's reachability walk leave it alone, and the goal seats on the
# top of the column, which is the deck.
quay_posts = kit.AddedLayer(
    id="quay-posts", name="the quay's posts", base_y=0,
    kind="made", part_of="quay",
    groups=[kit.SketchGroup(id="quay-posts", name="the quay's posts", mirrors=True,
                            shapeIds=["quay-posts-run"])],
    shapes=[
        kit.SketchShape(id="quay-posts-run", type="polyline", operation="add",
                        floor=8, base_height=3, radius=1.0,
                        stroke_edge="solid", keepClear=True,
                        material=solid(17, 1),
                        vertices=[[15, 48], [14, 54], [15, 60], [19, 63]]),
    ],
)

# The deck stands on a layer of its own: a layer holds one span per column, so
# the posts under it and the deck over it on one layer is SK9 — the taller add
# wins and the lower shape is simply not in the world.
quay_deck = kit.AddedLayer(
    id="quay-deck", name="the quay", base_y=0,
    kind="made", part_of="quay",
    groups=[kit.SketchGroup(id="quay-deck", name="the quay", mirrors=True,
                            shapeIds=["quay-deck-plate"])],
    shapes=[
        kit.SketchShape(id="quay-deck-plate", type="rectangle", operation="add",
                        floor=11, base_height=1, keepClear=True,
                        material=cells(7151, 4, 1, [DARKOAK, solid(5, 1)]),
                        min_x=13, max_x=24, min_z=46, max_z=62),
    ],
)

# ---------------------------------------------------------------- the dressing

# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()

PAVE = cells(7162, 3, 0, [GRAVEL, WORN, COBBLE])

WILLOWS = [(-16, 62), (-4, 68), (8, 66)]
BIRCHES = [(-34, 22), (-24, 34), (22, 18), (22, 34)]
ROCKS = [(16, 44), (-12, 60), (33, 70)]
# Both positions come off POST .../sketch/seats for a 9 x 6 house, which marks
# 80 cells on this board: the spawn hall's own door apron is kept clear for
# thirty blocks in front of it and takes most of the works yard.
# One building, not two. The works yard holds none — the spawn hall's own door
# apron is kept clear for thirty blocks in front of it — and a second shed put
# anywhere the seats raster allowed fell inside the sawmill's claim or left the
# pair of them with no eight blocks of passable ground down one side (DR-PASS,
# which is asked of a group of buildings rather than of each one). The quay
# beside it is the board's other built thing.
HOUSES = [("sawmill", [[12, 64], [20, 69]], 2, "posZ")]

styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "willow": "willow-2", "birch": "birch-4"}.items()}
styles["erratic"] = kit.BoulderStyle(
    form="round", size=2, mossy=True,
    rock=kit.TurbulenceMaterial(seed=7161, scale=3, octaves=3, stops=[STONE, COBBLE, ANDESITE], rise=3))

props = [
    # spawn door to the quay, and the quay forward to the delta the crossing
    # lands on; and the spawn door out to the wool spur's mouth
    kit.StrokeProp(id="quay-road", seed=7171, radius=2,
                   style="solid", claimsGround=True, pave=PAVE,
                   points=[[19, 92], [22, 84], [26, 76], [28, 68], [26, 62]]),
    kit.StrokeProp(id="spur-road", seed=7172, radius=2,
                   style="solid", claimsGround=True, pave=PAVE,
                   points=[[10, 92], [4, 84], [-4, 78], [-14, 74], [-28, 76]]),
    kit.StrokeProp(id="delta-road", seed=7173, radius=2,
                   style="solid", claimsGround=True, pave=PAVE,
                   points=[[-30, 68], [-30, 56], [-30, 44], [-28, 32], [-26, 20]]),

    # radius 6 round (-28, 58), every radius up to 20% off
    kit.FluidProp(id="backwater", seed=7174, shape="pool",
                  radius=2, depth=2, shore=3, shoreWander=True,
                  bank=cells(7176, 4, 0, [CLAY, GRAVEL, WORN]), points=[
        [-21.59, 58.0], [-22.33, 61.65], [-25.87, 62.65], [-28.81, 63.67], [-32.5, 63.2], [-33.56, 59.63],
        [-32.99, 56.54], [-32.17, 53.18], [-28.89, 51.8], [-25.85, 53.3], [-23.73, 55.26]]),
]

props += [kit.TreeProp(id=f"willow-{i}", seed=7200 + i, x=x, z=z, style="willow")
          for i, (x, z) in enumerate(WILLOWS)]
props += [kit.TreeProp(id=f"birch-{i}", seed=7220 + i, x=x, z=z, style="birch")
          for i, (x, z) in enumerate(BIRCHES)]
props += [kit.BoulderProp(id=f"rock-{i}", seed=7240 + i, x=x, z=z, style="erratic")
          for i, (x, z) in enumerate(ROCKS)]
props += [kit.HouseProp(id=pid, seed=7260 + i, style="delta-house", front=front,
                        wings=[kit.AuthoredWing(corners=corners, spec=kit.WingSpec(storeysHigh=high))])
          for i, (pid, corners, high, front) in enumerate(HOUSES)]

props += [
    # the rectangle x -36..36, z 16..110, every point moved up to 3 blocks along each axis
    kit.FloraProp(id="flora", seed=7180, points=[
        [-34.25, 18.17], [-20.78, 16.99], [0.1, 13.49], [15.09, 17.68], [33.24, 16.15], [33.65, 41.08],
        [34.79, 61.68], [37.23, 87.07], [37.33, 111.66], [19.35, 108.55], [0.29, 112.05], [-18.03, 112.49],
        [-36.42, 111.19], [-36.8, 84.7], [-38.76, 65.65], [-38.75, 41.22]],
        spec=kit.FloraSpec(coverage=0.26, scale=24, octaves=3, fernShare=0.30,
                           flowerShare=0.06, flowerScale=16, tallShare=0.06)),
]

# ---------------------------------------------------------------- the house
#
# White plaster framed in dark oak: the ground is the darkest of the four
# boards, so the buildings are the palest thing standing on it.

DARK_LOG = kit.LaidLogMaterial(id=162, data=1)
PLASTER_WALL = cells(7191, 3, 2, [PLASTER, solid(155, 0)])
PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}


def delta_storey(height, plaster):
    """A storey `height` courses tall and clear: a course of stone brick, `plaster` up to the last course, and that
    one of dark log."""
    return {
        "clear": height,
        "wall": {"stack": {"bands": [
            {"material": STONEBRICK, "thickness": 1},
            {"material": plaster, "thickness": height - 2},
            {"material": DARK_LOG, "thickness": 1}], "ending": "repeat"},
            "extent": height},
        "post": solid(162, 1),
        "windows": {"form": "arched", "block": 164, "hostBlock": -1, "hostData": 0,
                    "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "surface": PLAIN_SURFACE, "deck": None, "headroom": height,
    }


DELTA_HOUSE = kit.build("HouseStyle", {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE, "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARKOAK, "verge": DARK_LOG, "gable": PLASTER,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(162, 1),
    "windows": NO_WINDOW,
    "storeys": [delta_storey(5, PLASTER_WALL)],
    "porch": None, "front": None,
    "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 164, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 5},
                "width": 2, "height": 3},
})

# The spawn hall is the house hipped, its storey seven courses tall.
DELTA_HALL = kit.build("HouseStyle", {
    **DELTA_HOUSE,
    "roof": {"form": "hip", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": False, "hole": False,
             "body": DARKOAK, "verge": DARK_LOG, "gable": None,
             "gableWindows": NO_WINDOW},
    "storeys": [delta_storey(7, PLASTER_WALL)],
})

# The wool room is the house under a flat stone-brick roof, its storey six
# courses tall and its plaster broken with stone brick.
WOOL_ROOM = kit.build("HouseStyle", {
    **DELTA_HOUSE,
    "roof": {"form": "flat", "pitch": 1, "slab": -1, "slabData": 0,
             "overhang": 0, "ridgeCap": False, "hole": False,
             "body": STONEBRICK, "verge": STONEBRICK, "gable": None,
             "gableWindows": NO_WINDOW},
    "storeys": [delta_storey(6, cells(7192, 4, 2, [PLASTER, STONEBRICK]))],
})

styles["delta-house"] = kit.HouseStyleRef(shell=DELTA_HOUSE)

refinement = kit.Refinement(
    authors=["Opus 5"],
    created="2026-09-21",
    themes={"carr": carr_theme, "reed": reed_theme, "works": works_theme},
    mapTheme="carr",
    # Swampland: grass tints #6a7039, which comes to meet podzol's brown so the
    # pair reads as one dark, leaf-littered floor. Read off /api/terrain/biomes.
    biome=kit.SolidBiome(id=6),
    relief=relief,
    addShapes=add_shapes,
    addLayers=[quay_posts, quay_deck],
    roomStyles=kit.SketchRoomStyles(spawn=DELTA_HALL, wool=WOOL_ROOM),
    dressing=kit.DressingDoc(styles=styles, props=props),
)

for part, document in (("plan", plan), ("refinement", refinement)):
    path = os.path.join(HERE, f"{SLUG}.{part}.json")
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
    print(f"wrote {path}")
