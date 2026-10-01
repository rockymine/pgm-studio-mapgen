#!/usr/bin/env python3
"""opus5b-ochredrift — capture the wool.

A red mesa mining camp over a dry wash: each team keeps two wools in rock-cut
rooms on spurs at the far corners of its own ground, one bedrock line across
each spur's mouth, and a hole through the middle of its hub — so a raider
chooses which side of that hole to come round, and a defender has two prepared
lines and cannot hold both.

Tone families: the ground is red — clay, red sandstone and dry litter; what is
built is pale sandstone and birch on a grey plinth; the accent is the grey of
the crusher yard's paving.

The crusher terrace is the one piece of made ground on the board: its compiled
shape carries relief_scope exclude, so it meets the hub at a face rather than a
grade, and a flight cut into that face is the way up.

Writes opus5b-ochredrift.plan.json and opus5b-ochredrift.refinement.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit

SLUG = "opus5b-ochredrift"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# blocks:  front-w      x -48..-8   z  16..40   surface  9   the wash-side shelf
#          front-e      x  12..48   z  16..36   surface  9
#          hub-w        x -48..-32  z  36..64   surface 15
#          hub-e        x  32..48   z  36..64   surface 15
#          hub-link-w   x -32..-16  z  52..64   surface 15
#          hub-n        x -16..16   z  48..64   surface 15
#          hub-link-e   x  16..32   z  52..64   surface 15
#          w-approach   x -48..-32  z  64..80   surface 15
#          w-room       x -48..-32  z  80..92   surface 15
#          e-approach   x  32..48   z  64..80   surface 15
#          e-room       x  32..48   z  80..92   surface 15
#          yard         x -16..16   z  64..84   surface 21   the crusher terrace
#          spawn        x -16..4    z  84..104  surface 21   (20 x 20)
#          yard-ne      x   4..12   z  84..104  surface 21
#          mid-band     x -48..48   z -16..16   the build zone over the wash
#
# Two holes are made by arrangement and neither is covered by any piece: a
# notch between the two frontline legs, x -12..12 from z 16 to 36, and a slot
# across the hub, x -32..32 from z 36 up to 48 in the middle and 52 at the
# flanks. They meet, so what the compile declares is one T of void through the
# middle of a team's own ground.
#
# What that buys is the funnel. The only ground joining the wash shelf to the
# hub is the sixteen blocks at each end, x -48..-32 and x 32..48, and a ramp is
# cut through each — so an attacker who has crossed the wash chooses a hand,
# and a defender knows the two places anyone arrives by. Nothing bridges the
# holes, because no build zone covers them.
#
# The frontline is what a build zone touches, and FR6 caps it at sixteen cells.
# One piece across the whole 96-block face read 24; the two legs read ten each.
#
# Each wool room has three faces on void and one connecting piece, which is the
# corner a room is defended from, and the bay between a room and the terrace is
# sixteen blocks — WL12's floor, because a shorter one is crossed by towering
# at the near edge and jumping in rather than by building.

SPAWN_PIECE_MIN = (-16, 84)

plan = {
    "plan": 2,
    "meta": {"name": "Ochre Drift"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 22,
                "surface": 9},
    "pieces": [
        {"id": "front-w", "role": "piece", "rect": [-12, 4, 9, 5], "surface": 9},
        {"id": "front-e", "role": "piece", "rect": [3, 4, 9, 5], "surface": 9},
        {"id": "hub-w", "role": "piece", "rect": [-12, 9, 4, 7], "surface": 15},
        {"id": "hub-e", "role": "piece", "rect": [8, 9, 4, 7], "surface": 15},
        {"id": "hub-link-w", "role": "piece", "rect": [-8, 13, 4, 3], "surface": 15},
        {"id": "hub-n", "role": "piece", "rect": [-4, 12, 8, 4], "surface": 15},
        {"id": "hub-link-e", "role": "piece", "rect": [4, 13, 4, 3], "surface": 15},
        {"id": "w-approach", "role": "piece", "rect": [-12, 16, 4, 4], "surface": 15},
        {"id": "w-room", "role": "wool-room", "rect": [-12, 20, 4, 3], "surface": 15},
        {"id": "e-approach", "role": "piece", "rect": [8, 16, 4, 4], "surface": 15},
        {"id": "e-room", "role": "wool-room", "rect": [8, 20, 4, 3], "surface": 15},
        {"id": "yard", "role": "piece", "rect": [-4, 16, 8, 5], "surface": 21},
        {"id": "spawn", "role": "spawn", "rect": [-4, 21, 5, 5], "surface": 21},
        {"id": "yard-ne", "role": "piece", "rect": [1, 21, 2, 5], "surface": 21},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-12, -4, 24, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-camp", "piece": "spawn", "at": [11, 10],
                    "facing": "front", "footprint": [6, 2, 10, 16]}],
        "wools": [
            {"id": "wool-west", "piece": "w-room", "at": [8, 6]},
            {"id": "wool-east", "piece": "e-room", "at": [8, 6]},
        ],
        "iron": [{"id": "iron-camp", "piece": "spawn", "at": [2.5, 10.0]}],
        "destroyables": [],
        "cores": [],
    },
    # One wall on one interface each, at the mouth of a spur rather than on the
    # room's own edge — PL13 refuses that, and two in series is a sealed room
    # rather than a prepared line. The interface is sixteen blocks wide, inside
    # ST8's ten-to-twenty lane mouth, and the spur carries no ground past the
    # wall's ends for a player to stroll round.
    "walls": [
        {"a": "hub-w", "b": "w-approach"},
        {"a": "hub-e", "b": "e-approach"},
    ],
}

# ---------------------------------------------------------------- the ground

relief = {
    "*": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="rolling",
        grain=kit.ReliefGrainJson(amplitude=1.2, scale=16, seed=6103),
        marks=[
            # the wash shelf: x -50..50 by z 12..34, walked as a wandering ring
            kit.ReliefMarkJson(id="wash-shelf", kind="area", h=9, bevel=2, ring=[
                [-52.94, 12.84], [-24.17, 12.18], [1.96, 9.29], [22.76, 10.78],
                [52.78, 12.49], [50.63, 15.67], [48.68, 25.89], [52.31, 27.26],
                [48.83, 34.52], [25.93, 36.99], [-1.26, 32.62], [-27.89, 34.83],
                [-50.33, 35.77], [-48.51, 25.95], [-50.76, 23.85], [-50.82, 18.64]]),
            # the hub's bar: x -50..50 by z 46..66, walked as a wandering ring
            kit.ReliefMarkJson(id="hub-bar", kind="area", h=15, bevel=3, ring=[
                [-51.82, 43.9], [-26.26, 44.46], [-2.38, 47.95], [27.61, 48.91],
                [48.21, 48.86], [49.62, 49.68], [49.45, 54.75], [50.42, 63.65],
                [51.66, 63.19], [22.79, 65.05], [1.75, 64.53], [-25.91, 63.93],
                [-51.02, 67.15], [-52.17, 63.23], [-47.04, 56.3], [-49.97, 49.62]]),
            # the west spur: x -50..-30 by z 38..94, walked as a wandering ring
            kit.ReliefMarkJson(id="spur-west", kind="area", h=15, bevel=3, ring=[
                [-50.46, 38.63], [-43.24, 39.83], [-40.49, 38.41], [-34.02, 38.69],
                [-30.24, 37.49], [-30.92, 51.46], [-29.86, 66.4], [-30.99, 80.36],
                [-31.0, 93.91], [-34.56, 94.74], [-40.82, 92.97], [-44.28, 94.7],
                [-51.14, 94.36], [-49.89, 80.68], [-49.54, 65.83], [-49.42, 53.4]]),
            # the east spur: x 30..50 by z 38..94, walked as a wandering ring
            kit.ReliefMarkJson(id="spur-east", kind="area", h=15, bevel=3, ring=[
                [30.28, 36.67], [35.36, 38.68], [40.61, 37.52], [45.21, 37.44],
                [50.71, 39.07], [48.41, 51.81], [50.65, 67.64], [51.75, 78.95],
                [50.89, 95.7], [43.34, 92.11], [41.18, 92.91], [33.04, 92.77],
                [28.4, 93.94], [31.67, 79.87], [28.94, 65.46], [31.15, 51.73]]),
            # the two cuts up off the wash, one at each end of the funnel
            kit.ReliefMarkJson(id="ramp-west", kind="line", r=5, tread=3,
                               points=[[-40, 28], [-40, 46]], h=[9, 15]),
            kit.ReliefMarkJson(id="ramp-east", kind="line", r=5, tread=3,
                               points=[[40, 28], [40, 46]], h=[9, 15]),
        ],
        pushes=[
            # Two buttes on the hub, one a side of the hole, so the ground an
            # attacker crosses has height on it to climb and bridge from and
            # the two lanes round the hole are not the same walk.
            # The west butte: a lobed ring of radius 7 round (-20, 26).
            kit.ReliefPushJson(id="butte-west", ring=[
                [-11.94, 26.0], [-14.15, 30.91], [-18.96, 31.92], [-23.73, 32.46],
                [-26.79, 28.47], [-27.43, 23.3], [-23.09, 20.64], [-18.94, 20.01],
                [-14.97, 21.78]],
                amount=9, falloff=9, crown=4, roughness=1.4, seed=6122),
            # The east butte: a lobed ring of radius 6 round (22, 24).
            kit.ReliefPushJson(id="butte-east", ring=[
                [27.28, 24.0], [27.13, 28.31], [23.02, 29.76], [19.59, 28.17],
                [17.36, 25.69], [16.69, 22.07], [18.53, 17.99], [23.06, 17.96],
                [27.31, 19.54]],
                amount=6, falloff=8, crown=3, roughness=1.2, seed=6124),
        ]),
}

# ---------------------------------------------------------------- the paint

def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def cells(seed, size, rise, palette):
    """A cell pattern of `palette` at jitter 45 and warp 1."""
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=45, warp=1, rise=rise, palette=palette)


def band(thickness, material):
    return kit.Band(material=material, thickness=thickness)


def stack(axis, bands):
    """`bands` read along `axis`, the last one carried on past the end."""
    return kit.LayeredMaterial(axis=axis, stack=kit.BandStack(ending="repeat", bands=bands))


def soil(top, under, depth=2):
    """One course of a surfacing block over `depth` of soil."""
    return stack("depth", [band(1, top), band(depth, under)])


RED_SAND = solid(12, 1)
RED_SANDSTONE = solid(179, 0)
RED_SANDSTONE_SM = solid(179, 2)
CLAY_RED = solid(172, 0)
WORN = solid(3, 1)
EARTH = solid(3, 0)
PODZOL = solid(3, 2)
TURF = solid(2, 0)
GRAVEL = solid(13, 0)
STONEBRICK = solid(98, 0)
PALE_ANDESITE = solid(1, 6)
COBBLE = solid(4, 0)
SANDSTONE = solid(24, 0)
BIRCH = solid(5, 2)

MESA_FACE = cells(6131, 7, 5, [CLAY_RED, RED_SANDSTONE])

# Cut off this board's own GET .../incline, which reads 69.8% of the ground
# under 10 degrees, 15.8% between 10 and 29 and 7.2% at 40 or steeper: the
# cuts at 10 and 30 land on bucket walls, so the mesa tops take the dry litter,
# the ramps and skirts take red sand, and only the risers take bare rock.
SLOPE_LITTER, SLOPE_SCREE = 10, 30

mesa_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=RED_SANDSTONE,
    wall=MESA_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=RED_SANDSTONE_SM),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3, material=stack("slope", [
        band(SLOPE_LITTER, soil(cells(6132, 8, 0, [TURF, PODZOL]), EARTH)),
        band(SLOPE_SCREE - SLOPE_LITTER, soil(cells(6133, 7, 0, [RED_SAND, WORN]), EARTH)),
        band(90 - SLOPE_SCREE, stack("depth", [band(3, MESA_FACE)])),
    ])),
)

wash_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=RED_SANDSTONE,
    wall=MESA_FACE,
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=False, depth=1, material=RED_SANDSTONE_SM),
    rimEdges="void",
    surface=kit.TopBand(enabled=True, depth=3,
                        material=soil(cells(6134, 7, 0, [RED_SAND, GRAVEL]), RED_SANDSTONE)),
)

works_theme = kit.TerrainTheme(
    bedrock=kit.BedrockSpec(relative=False, value=1),
    fill=RED_SANDSTONE,
    wall=cells(6135, 5, 4, [STONEBRICK, PALE_ANDESITE]),
    wallEnabled=True,
    wallOnTerrainFaces=True,
    rim=kit.TopBand(enabled=True, depth=1, material=STONEBRICK),
    rimEdges="boundary",
    surface=kit.TopBand(enabled=True, depth=3,
                        material=soil(cells(6136, 5, 0, [STONEBRICK, PALE_ANDESITE, COBBLE]), solid(1, 0))),
)

# ---------------------------------------------------------------- the shapes

FRONT_BASE, BENCH_BASE, TERRACE_BASE = 9, 15, 21

add_shapes = [
    # the wash floor: x -44..44 by z 16..34, walked as a wandering ring
    kit.SketchShape(id="wash-floor", type="polygon", operation="add", floor=0, base_height=FRONT_BASE,
                    theme="wash", vertices=[
                        [-43.33, 18.4], [-24.02, 18.56], [-2.46, 15.26], [21.26, 18.51],
                        [41.69, 15.64], [44.43, 22.07], [41.57, 23.62], [43.42, 30.89],
                        [43.85, 36.79], [24.74, 32.77], [-0.88, 36.03], [-19.43, 32.07],
                        [-41.02, 35.25], [-44.26, 32.46], [-41.11, 27.25], [-43.47, 18.12]]),
]

# The flight down off the crusher terrace. It is a made layer of its own, so
# nothing in the ground's relief answers for it and SK10's pair walk leaves it
# alone; anchor_heights are thicknesses at the polygon's corners, so the four
# read foot, foot, head, head. Twelve blocks of run for six of rise, which is
# twice the rise, and the head lands on the terrace's own top block.
terrace_steps = kit.AddedLayer(
    id="crusher-steps", name="the crusher steps", base_y=0, kind="made", part_of="crusher",
    groups=[kit.SketchGroup(id="crusher-steps", name="the crusher steps", mirrors=True,
                            shapeIds=["steps-main"])],
    shapes=[
        kit.SketchShape(id="steps-main", type="polygon", operation="add", floor=0, keepClear=True,
                        anchor_heights=[BENCH_BASE, BENCH_BASE, TERRACE_BASE, TERRACE_BASE],
                        material=cells(6151, 4, 3, [STONEBRICK, PALE_ANDESITE]),
                        vertices=[[-5, 52], [5, 52], [5, 64], [-5, 64]]),
    ],
)

# ---------------------------------------------------------------- the dressing

PAVE = cells(6162, 3, 0, [GRAVEL, WORN, COBBLE])

SCRUBS = [(-47, 40), (-47, 54), (44, 44), (40, 40)]
OLIVES = [(-30, 30), (24, 28)]
ROCKS = [(-46, 26), (22, 22), (36, 40)]
# The crusher terrace itself seats no building: the hall, its door apron and
# the flight take all of it, and POST .../sketch/seats for a 9 x 6 house marks
# 216 cells on the whole board and none of them there. So the stamp mill stands
# on the wash edge where a stamp mill belongs — one side against the coast,
# which DR-PASS allows — and the winding house on the east arm of the hub.
HOUSES = [("crusher", [[-24, 17], [-16, 22]], 2, "posZ"),
          ("winding-house", [[38, 52], [46, 57]], 1, "negX")]

# The copied trees, each the showcase tree it names, as corpus/tree-showcase/trees.json carries it.
SHOWCASE = json.load(open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")))["trees"]
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "scrub": "acacia-3", "olive": "olive-2"}.items()}
styles["erratic"] = kit.BoulderStyle(form="round", size=2, mossy=False, rock=kit.TurbulenceMaterial(
    seed=6161, scale=3, octaves=3, stops=[solid(1, 0), COBBLE, solid(1, 5)], rise=3))

props = [
    # spawn door to each spur's mouth, drawn before the scenery
    kit.StrokeProp(id="west-haul", seed=6171, radius=2, style="solid", claimsGround=True, pave=PAVE,
                   points=[[-2, 84], [-8, 78], [-18, 70], [-28, 66], [-38, 68]]),
    kit.StrokeProp(id="east-haul", seed=6172, radius=2, style="solid", claimsGround=True, pave=PAVE,
                   points=[[4, 84], [10, 78], [20, 70], [30, 66], [38, 68]]),
    kit.StrokeProp(id="front-haul", seed=6173, radius=2, style="solid", claimsGround=True, pave=PAVE,
                   points=[[-40, 60], [-40, 48], [-38, 36], [-34, 26], [-30, 18]]),
]

props += [kit.TreeProp(id=f"scrub-{i}", seed=6200 + i, x=x, z=z, style="scrub")
          for i, (x, z) in enumerate(SCRUBS)]
props += [kit.TreeProp(id=f"olive-{i}", seed=6220 + i, x=x, z=z, style="olive")
          for i, (x, z) in enumerate(OLIVES)]
props += [kit.BoulderProp(id=f"rock-{i}", seed=6240 + i, x=x, z=z, style="erratic")
          for i, (x, z) in enumerate(ROCKS)]
props += [kit.HouseProp(id=pid, seed=6260 + i, style="camp-house", front=front,
                        wings=[kit.AuthoredWing(corners=corners, spec=kit.WingSpec(storeysHigh=high))])
          for i, (pid, corners, high, front) in enumerate(HOUSES)]

props += [
    # the flora's ground: x -48..48 by z 16..102, wash to spawn, walked as a wandering ring
    kit.FloraProp(id="flora", seed=6180, points=[
        [-50.52, 14.46], [-25.82, 15.73], [-2.36, 15.88], [25.25, 15.48],
        [48.9, 14.51], [50.17, 35.61], [46.07, 59.93], [49.57, 81.4],
        [47.22, 103.83], [21.15, 99.14], [-0.38, 100.57], [-26.14, 104.39],
        [-48.61, 102.55], [-50.59, 82.82], [-46.25, 57.11], [-49.67, 36.44]],
        spec=kit.FloraSpec(coverage=0.14, scale=28, octaves=3, fernShare=0.06, flowerShare=0.05,
                           flowerScale=20, tallShare=0.04)),
]

# ---------------------------------------------------------------- the house
#
# Pale sandstone and birch on a grey plinth: the ground is red, so a building
# reads as built by not being in the ground's family at all.

BIRCH_LOG = kit.LaidLogMaterial(id=17, data=2)
PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}


def courses(extent, bands):
    """A wall or a plate `extent` courses high, laid in `bands` from its base, the last one carried on."""
    return {"stack": {"bands": bands, "ending": "repeat"}, "extent": extent}


def camp_storey(clear, fill, thickness):
    """A storey `clear` blocks high: a course of stone brick, `thickness` courses of `fill`, then a laid birch
    log; birch posts and arched windows."""
    return {"clear": clear, "headroom": clear,
            "wall": courses(clear, [band(1, STONEBRICK), band(thickness, fill), band(1, BIRCH_LOG)]),
            "post": solid(17, 2),
            "windows": {"form": "arched", "block": 135, "hostBlock": -1, "hostData": 0,
                        "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
            "surface": PLAIN_SURFACE, "deck": None}


def camp_style(roof, storey):
    """The camp's shell: a stone-brick plinth and ground course, birch posts and beam ends and an open arched
    doorway, under `roof` and over the one `storey`."""
    return kit.build("HouseStyle", {
        "foundation": {"plate": courses(1, [band(1, STONEBRICK)]), "surface": PLAIN_SURFACE, "footing": None},
        "roof": roof,
        "wall": courses(5, [band(1, STONEBRICK)]),
        "post": solid(17, 2),
        "windows": NO_WINDOW,
        "storeys": [storey],
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": 135, "fill": "upperSlab",
                             "fillBlock": 126, "fillData": 2},
                    "width": 2, "height": 3},
    })


CAMP_FILL = cells(6191, 3, 2, [SANDSTONE, BIRCH])

CAMP_HOUSE = camp_style(
    {"form": "gable", "pitch": 2, "slab": 126, "slabData": 2, "overhang": 1, "ridgeCap": True, "hole": False,
     "body": BIRCH, "verge": SANDSTONE, "gable": SANDSTONE,
     "gableWindows": {"form": "open", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 1,
                      "width": 1, "height": 1, "spacing": 3}},
    camp_storey(5, CAMP_FILL, 3))

# The spawn hall: the camp house seven blocks clear, under a hipped roof.
CAMP_HALL = camp_style(
    {"form": "hip", "pitch": 2, "slab": 126, "slabData": 2, "overhang": 1, "ridgeCap": False, "hole": False,
     "body": BIRCH, "verge": SANDSTONE, "gable": None, "gableWindows": NO_WINDOW},
    camp_storey(7, CAMP_FILL, 5))

# The wool room is a rock-cut chamber: sandstone walls on a stone plinth under
# a flat sandstone lid, so what a raider stands inside belongs to the camp
# rather than to the studio's bedrock default.
WOOL_ROOM = camp_style(
    {"form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 0, "ridgeCap": False, "hole": False,
     "body": solid(24, 2), "verge": solid(24, 2), "gable": None, "gableWindows": NO_WINDOW},
    camp_storey(6, cells(6192, 4, 2, [SANDSTONE, solid(24, 2)]), 4))

styles["camp-house"] = kit.HouseStyleRef(shell=CAMP_HOUSE)

refinement = kit.Refinement(
    authors=["Opus 5"],
    created="2026-09-21",
    themes={"mesa": mesa_theme, "wash": wash_theme, "works": works_theme},
    mapTheme="mesa",
    # Mesa: grass tints #90814d, which is where podzol's brown comes to meet it
    # and the pair reads as one dry, leaf-littered floor rather than as two
    # grounds. Read off GET /api/terrain/biomes.
    biome=kit.SolidBiome(id=37),
    relief=relief,
    addShapes=add_shapes,
    addLayers=[terrace_steps],
    # The crusher terrace is made ground, so its compiled shape comes out of
    # the solve: `exclude` keeps the raw column and the two tiers meet at a
    # face, where `hold` would let the relief bring the hub up to it and there
    # would be no step and no reason for a flight. The key is the shape id
    # POST /plan/compile answers — a height key cannot tell two pieces at one
    # surface apart, and the compile fuses every piece at 21 into this one.
    shapePropsById={"e-approach-21": kit.SketchShape(relief_scope="exclude")},
    themeById={"e-approach-21": "works"},
    roomStyles={"spawn": CAMP_HALL, "wool": WOOL_ROOM},
    dressing=kit.DressingDoc(styles=styles, props=props),
)

for name, doc in (("plan", plan), ("refinement", refinement)):
    path = os.path.join(HERE, f"{SLUG}.{name}.json")
    with open(path, "w") as handle:
        json.dump(doc, handle, indent=1)
    print(f"wrote {path}")
