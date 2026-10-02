#!/usr/bin/env python3
"""opus5c-wetherslack — destroy the core. The approach dimension is BELOW.

A wooded gill with a beck down it, and the core standing on a vaulted terrace
built out over the gill's west side. The terrace's deck is flush with the
shoulder behind it, so from the west a player walks straight on; from the gill
floor the way at it is the undercroft underneath, entered by two mouths and
leaving by a shaft in the deck that comes up four blocks from the casing. The
two ways differ in dimension rather than in hand — one is across and one is
under — and nobody standing on the deck can see the second one coming.

Tone families: the ground is deep green moss and wet leaf, what is built is
pale birch and quartz on a stone plinth, and the accent is the gill's own
grey rock where the slope bands expose it.

Writes opus5c-wetherslack.plan.json and opus5c-wetherslack.refinement.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit

SLUG = "opus5c-wetherslack"
CELL = 4


# ---------------------------------------------------------------- materials

def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def cells(seed, size, rise, palette):
    """Flat patches of `palette`, `size` blocks across at 45% jitter, their edges wandering a block."""
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=45, warp=1, rise=rise, palette=palette)


def layered(axis, *bands):
    """(thickness, material) bands read along `axis`, the last carrying on."""
    return kit.LayeredMaterial(axis=axis, stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=material, thickness=thickness) for thickness, material in bands]))


def soil(top, under):
    """One course of a surfacing block over two of soil, which is what a depth stack owes a surface that has to
    stay one course thick."""
    return layered("depth", (1, top), (2, under))


def slope_stack(bands):
    """A surface finished by the ground's angle. `bands` is (degrees, material) lowest first, each band running
    from the edge below it to its own, so one stack finishes the flat, the shoulder and the face of one hill."""
    edges = [0] + [edge for edge, _ in bands]
    return layered("slope", *[(edge - below, material) for below, (edge, material) in zip(edges, bands)])


# ---------------------------------------------------------------- the plan
#
# Two pieces a team and both at the board's own surface, in blocks:
#
#   slack      x -24..24   z  16..96    the gill, its shoulders and its floor
#   spawn      x   0..20   z  96..120   20 x 24, inside ST10's cap
#   mid-band   x -24..24   z -16..16    a build zone over 32 of void
#
# The spawn stands at the same height as the gill rather than on a shelf over
# it, so there is no riser to cut a ramp into and no seam for EL1 to walk flat.
# What gives this board its height is the relief and the terrace, and both are
# downstream of the plan — a piece that exists so a landform can be hung on it
# should have been a shape scope.
#
# The spawn is offset EAST of the centre line, which puts the walk out of the
# door on the gill's east shoulder and the core on its west: a defender
# returning and a raider arriving are on opposite sides of the beck for the
# whole length of it.

SPAWN_AT = (10, 108)
CORE_AT = (-4, 62)
SLACK_MIN = (-24, 16)

plan = {
    "plan": 2,
    "meta": {"name": "Wetherslack"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "slack", "role": "piece", "rect": [-6, 4, 12, 20], "surface": 9},
        {"id": "spawn", "role": "spawn", "rect": [0, 24, 5, 6], "surface": 9},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-6, -4, 12, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-slack", "piece": "spawn",
                    "at": [10, 13], "facing": "front",
                    "footprint": [4, 7, 12, 12]}],
        "wools": [],
        "iron": [{"id": "iron-slack", "piece": "spawn", "at": [10.0, 3.5]}],
        "destroyables": [],
        # A core is breached where it stands, so it belongs where it will be
        # fought over and nothing is put between it and the middle. It NAMES
        # the deck's layer: a stacked board has a surface per layer, and a core
        # naming none seated on the terrain under the terrace instead — casing
        # at y18 over ground at y11, hanging in the undercroft's own airspace
        # with the deck running through it at y21.
        "cores": [{"id": "core", "piece": "slack",
                   "at": [CORE_AT[0] - SLACK_MIN[0], CORE_AT[1] - SLACK_MIN[1]],
                   "layer": "vault-deck",
                   "lava": 3, "float": 6, "leak": 5,
                   "name": "Wetherslack Cistern"}],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# A gill is two shoulders and a floor, and the sides between them are pinned by
# nothing — which is where the ground gets its shape. Five marks, no push: the
# landform here is a valley, and a valley is what a relaxation makes between
# two heights when nothing in the middle argues with it.
#
# The beck is a LINE mark rather than an area, because a watercourse is a line
# and an area mark of that shape would pin a pan. It carries a tread, since a
# line pins every cell to the nearest pass of itself and two passes a winding
# apart put the whole difference in one cell.

relief = {
    "*": kit.SketchReliefJson(
        base=9, reach=0, step=1, landform="rolling",
        grain=kit.ReliefGrainJson(amplitude=1.3, scale=19, seed=5501),
        marks=[
            # the strand: x -26..26, z 14..30 walked as a wandering ring
            kit.ReliefMarkJson(id="strand", kind="area", h=9, bevel=2, ring=[
                [-23.58, 13.85], [-14.83, 14.52], [0.4, 13.94], [11.22, 15.89], [28.14, 13.59], [24.78, 19.74],
                [23.55, 20.54], [26.1, 26.13], [27.97, 27.51], [13.68, 27.78], [-2.38, 32.11], [-11.46, 31.64],
                [-26.37, 30.16], [-25.65, 26.93], [-27.38, 24.44], [-24.14, 17.56]]),
            # The tread is what decides how wide the water may be: it grades
            # the band's shoulder, so only 2*(half-width - tread) blocks in the
            # middle are pinned flat and the rest lofts. At tread 3 the channel
            # at radius 3 reached into the lofted part and DR-BANK read a
            # straight-sided wall three courses over the water's own line.
            kit.ReliefMarkJson(id="beck", kind="line", width=10, tread=2,
                               points=[[12, 30], [9, 50], [13, 70], [11, 92]], h=[8, 8, 8, 8]),
            # A bevel grades inward from BOTH edges of a mark's ring, so a
            # bevel of 5 on a strip ten blocks wide leaves no flat core to pin
            # and the mark is silent — which is what RL4 read of the first cut
            # of this shoulder.
            #
            # And the gill carries ONE shoulder rather than two. A scar on the
            # west and a bank that grades away east is what a gill cut into a
            # dipping bed looks like, and two 10-wide shoulders in a board 48
            # across leave the beck's own band nothing to sit in — the second
            # one won the cells beside the water and stood a 20-block rim on
            # the bank the channel was about to be carved into.
            # the west shoulder: x -26..-10, z 30..92 walked as a wandering ring
            kit.ReliefMarkJson(id="shoulder-w", kind="area", h=21, bevel=4, ring=[
                [-27.32, 31.92], [-20.86, 29.27], [-16.58, 29.06], [-12.19, 30.26], [-11.33, 31.25], [-11.64, 47.23],
                [-11.45, 61.07], [-11.19, 75.19], [-10.54, 91.8], [-15.55, 91.6], [-17.9, 93.63], [-23.45, 91.39],
                [-26.76, 91.71], [-24.16, 76.44], [-24.62, 62.59], [-27.95, 47.47]]),
            # the bench the terrace's walls stand on, stated LAST so it wins
            # the cells it shares with the west shoulder: the walls want a
            # level floor at 12 and the shoulder behind them wants 21
            # the bench: a wobbled ring of radius 14 round (-4, 62)
            kit.ReliefMarkJson(id="bench", kind="area", h=12, bevel=3, ring=[
                [10.22, 62.0], [10.61, 69.67], [2.77, 71.81], [-2.16, 77.12], [-8.8, 74.65], [-15.69, 72.35],
                [-17.93, 65.43], [-19.74, 58.12], [-15.02, 52.24], [-9.15, 48.42], [-2.16, 46.83], [2.82, 52.12],
                [7.91, 55.75]]),
        ],
        pushes=[],
    )
}

# ---------------------------------------------------------------- the terrace
#
# Two layers, and what they make is the air between them. The walls stand on
# the bench at base_y 12 and run nine courses to a segment top of 21; the deck
# rests at 21, which is one course over the west shoulder's own top block, so a
# player walks onto it from the shoulder with a single step up.
#
# The undercroft is ground nobody drew on. An opening is a gap between shapes
# rather than a subtract — SK13 reads a subtract as the board's negative space
# and refuses any add that fills it — so the walls are six rectangles with two
# mouths left between them, and the shaft is a four-block square the deck's own
# four rectangles are drawn around.

WALL_Y, DECK_Y = 12, 21
VAULT = cells(5521, 5, 3, [solid(98, 0), solid(98, 3), solid(4, 0)])
DECK_MAT = cells(5522, 4, 2, [solid(98, 0), solid(1, 0)])


def slab(sid, x0, z0, x1, z1, material, thickness):
    """A rectangle of `material`, `thickness` courses deep, that the dressing keeps clear of."""
    return kit.SketchShape(id=sid, type="rectangle", operation="add", floor=0, min_x=x0, min_z=z0, max_x=x1,
                           max_z=z1, base_height=thickness, material=material, keepClear=True)


wall_shapes = [
    slab("vault-w", -16, 52, -14, 72, VAULT, 9),
    slab("vault-n", -14, 70, 6, 72, VAULT, 9),
    # the east mouth, onto the beck: the gap at z 60..64
    slab("vault-e-s", 6, 52, 8, 60, VAULT, 9),
    slab("vault-e-n", 6, 64, 8, 72, VAULT, 9),
    # the south mouth, onto the strand: the gap at x -6..-2
    slab("vault-s-w", -14, 52, -6, 54, VAULT, 9),
    slab("vault-s-e", -2, 52, 6, 54, VAULT, 9),
]

deck_shapes = [
    slab("deck-s", -16, 52, 8, 56, DECK_MAT, 1),
    slab("deck-n", -16, 60, 8, 72, DECK_MAT, 1),
    slab("deck-w", -16, 56, -12, 60, DECK_MAT, 1),
    slab("deck-e", -8, 56, 8, 60, DECK_MAT, 1),
    # the shaft is x -12..-8, z 56..60 — the four blocks no rectangle covers
]

vault_walls = kit.AddedLayer(
    id="vault-walls", name="the vault's walls", base_y=WALL_Y, kind="made", part_of="slack",
    groups=[kit.SketchGroup(id="vault-walls", name="the vault's walls", mirrors=True,
                            shapeIds=[shape["id"] for shape in wall_shapes])],
    shapes=wall_shapes)

vault_deck = kit.AddedLayer(
    id="vault-deck", name="the terrace deck", base_y=DECK_Y, kind="made", part_of="slack",
    groups=[kit.SketchGroup(id="vault-deck", name="the terrace deck", mirrors=True,
                            shapeIds=[shape["id"] for shape in deck_shapes])],
    shapes=deck_shapes)

# ---------------------------------------------------------------- the paint

MOSS = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
ANDESITE = solid(1, 5)
GRAVEL = solid(13, 0)
CLAY = solid(82, 0)
BIRCH = solid(5, 2)
QUARTZ = solid(155, 0)
DARKOAK = solid(5, 5)

GILL_ROCK = cells(5531, 7, 5, [STONE, COBBLE, ANDESITE])
GILL_BRAE = cells(5532, 7, 3, [WORN, GRAVEL, EARTH])

# cut off this board's own GET .../incline
SLOPE_FLAT, SLOPE_BRAE = 18, 34


def rock_fill(seed):
    """Stone and andesite in nine-block voronoi cells."""
    return kit.VoronoiMaterial(seed=seed, cellSize=9, rise=4, bands=[kit.VoronoiBand(material=STONE, depth=5),
                                                                     kit.VoronoiBand(material=ANDESITE, depth=4)])


def theme(surface, wall, fill, rim, rim_enabled=True, rim_edges="void"):
    """A theme on one block of bedrock, its wall on every face, its rim one course deep and its surface three."""
    return kit.TerrainTheme(bedrock=kit.BedrockSpec(relative=False, value=1), fill=fill, wall=wall, wallEnabled=True,
                            wallOnTerrainFaces=True, rim=kit.TopBand(enabled=rim_enabled, depth=1, material=rim),
                            rimEdges=rim_edges, surface=kit.TopBand(enabled=True, depth=3, material=surface))


gill_theme = theme(
    surface=slope_stack([
        (SLOPE_FLAT, soil(MOSS, EARTH)),
        (SLOPE_BRAE, soil(GILL_BRAE, EARTH)),
        (90, layered("depth", (3, GILL_ROCK))),
    ]),
    wall=GILL_ROCK, fill=rock_fill(5533), rim=STONE)

flush_theme = theme(
    surface=soil(cells(5535, 7, 0, [GRAVEL, COBBLE, CLAY]), GRAVEL),
    wall=GILL_ROCK, fill=rock_fill(5534), rim=STONE, rim_enabled=False)

garth_theme = theme(
    surface=soil(cells(5538, 5, 0, [COBBLE, GRAVEL, STONE]), STONE),
    wall=cells(5537, 6, 4, [COBBLE, STONE]), fill=rock_fill(5536), rim=COBBLE, rim_edges="boundary")

# ---------------------------------------------------------------- the shapes

GROUND = 9


def patch(sid, paint, vertices):
    """A polygon of ground GROUND blocks thick, painted with the theme `paint`."""
    return kit.SketchShape(id=sid, type="polygon", operation="add", floor=0, base_height=GROUND, theme=paint,
                           vertices=vertices)


add_shapes = [
    # the undercroft's own floor, marked with a shape rather than a stroke: a
    # stroke ignores `layer` and would come back on the deck. It will not
    # appear in themes/census either, which counts the top surface per column
    # and every cell of it has a deck over it.
    kit.SketchShape(id="vault-floor", type="rectangle", operation="add", floor=0, min_x=-14, min_z=54, max_x=6,
                    max_z=70, base_height=GROUND, theme="garth"),
    kit.SketchShape(id="shoulder-flight", type="polygon", operation="add", floor=0, base_height=GROUND,
                    height_mode="level", skirt=0, keepClear=True, anchor_heights=[21, 21, 12, 12],
                    material=cells(5545, 4, 2, [COBBLE, STONE, GRAVEL]),
                    vertices=[[-21.5, 38.3], [-26.5, 41.7], [-14.5, 59.7], [-9.5, 56.3]]),

    # a wobbled ring of radius 9 round (11, 36)
    patch("shingle-lower", "flush", [
        [20.4, 36.0], [19.92, 40.68], [16.54, 44.02], [11.8, 42.61], [7.24, 45.92], [3.16, 42.95], [2.75, 38.03],
        [2.27, 33.85], [5.73, 31.33], [8.18, 28.57], [11.93, 28.35], [15.89, 28.92], [20.31, 31.12]]),
    # a wobbled ring of radius 8 round (12, 80)
    patch("shingle-upper", "flush", [
        [21.13, 80.0], [18.12, 83.21], [16.1, 85.93], [13.07, 88.82], [9.73, 86.0], [5.72, 85.56], [5.44, 81.62],
        [5.5, 78.4], [6.58, 75.19], [8.91, 71.86], [12.74, 73.89], [16.55, 73.41], [20.74, 75.41]]),
    # a wobbled ring of radius 7 round (10, 56)
    patch("shingle-mid", "flush", [
        [18.54, 56.0], [16.58, 60.23], [13.55, 63.78], [9.04, 62.69], [5.65, 61.02], [3.7, 57.85], [4.87, 54.49],
        [4.6, 49.76], [8.98, 48.88], [12.3, 50.96], [16.99, 51.51]]),
    # x 0..20, z 96..118 walked as a wandering ring
    patch("spawn-yard", "garth", [
        [-1.42, 95.02], [5.45, 94.56], [10.68, 94.59], [16.27, 96.24], [21.18, 95.85], [20.88, 102.19],
        [18.82, 106.7], [18.36, 114.13], [19.92, 118.88], [14.46, 117.53], [10.37, 117.78], [5.83, 119.69],
        [0.53, 116.54], [-0.2, 114.49], [0.77, 108.78], [0.08, 101.77]]),
]

# ---------------------------------------------------------------- the dressing

# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "oak": "dense-oak-5",        # dense oak — the gill's wood
    "birch": "birch-4",          # birch — the shoulders
    "willow": "willow-2",        # willow — the beck
}.items()}
styles["gritstone"] = kit.BoulderStyle(form="round", size=2, mossy=False, rock=kit.TurbulenceMaterial(
    seed=5551, scale=3, octaves=3, stops=[STONE, COBBLE, ANDESITE], rise=3))

# dirt, coarse dirt and spruce planks: three blocks a reader cannot quite tell
# apart, which is what a path on soft ground is
PAVE = cells(5552, 3, 0, [EARTH, WORN, solid(5, 1)])


def way(pid, seed, points):
    return kit.StrokeProp(id=pid, seed=seed, radius=2, style="solid", claimsGround=True, pave=PAVE, points=points)


props = [
    kit.FluidProp(id="beck-water", seed=5561, shape="channel", points=[[12, 34], [9, 50], [13, 70], [11, 88]],
                  radius=2, depth=2, level=6, shore=2, shoreWander=True,
                  bank=cells(5562, 4, 0, [GRAVEL, CLAY, COBBLE])),

    way("spawn-way", 5571, [[10, 96], [14, 88], [18, 76], [20, 64], [20, 50]]),
    way("shoulder-way", 5572, [[-20, 88], [-22, 76], [-22, 64], [-21, 56]]),

    kit.HouseProp(id="bank-house", seed=5574, style="mill", front="posX",
                  wings=[kit.AuthoredWing(corners=[[-13, 30], [-4, 36]], spec=kit.WingSpec(storeysHigh=2))]),
    kit.HouseProp(id="gill-house", seed=5575, style="mill", front="posX",
                  wings=[kit.AuthoredWing(corners=[[-15, 76], [-7, 81]], spec=kit.WingSpec(storeysHigh=1))]),
]

# Every position below sits on a cell POST .../sketch/seats marks legal for its
# own kind, and the willows stand on the beck's BANK rather than in it: a tree
# drawn on the channel's own cells is claimed by the water and is not in the
# world. Three of each, to the outside of the gill rather than down the middle
# of it, and none within four blocks of a road or of the flight's keep-clear.
props += [kit.TreeProp(id=f"oak-{i}", seed=5600 + i, x=x, z=z, style="oak")
          for i, (x, z) in enumerate([(-6, 42), (-20, 30), (-16, 93),
                                      (-14, 84), (-4, 84)])]
props += [kit.TreeProp(id=f"birch-{i}", seed=5620 + i, x=x, z=z, style="birch")
          for i, (x, z) in enumerate([(17, 42), (0, 25)])]
props += [kit.TreeProp(id=f"willow-{i}", seed=5640 + i, x=x, z=z, style="willow")
          for i, (x, z) in enumerate([(15, 30), (4, 35), (22, 78)])]
props += [kit.BoulderProp(id=f"gritstone-{i}", seed=5660 + i, x=x, z=z, style="gritstone")
          for i, (x, z) in enumerate([(-6, 25), (22, 88)])]

# A wooded gill is the one board of this run where ground cover is the place
# rather than a dressing over it, so the coverage is high and the fern share
# higher. The tall share stays low all the same: two-block grass in front of a
# core is cover nobody authored.
props += [
    kit.FloraProp(id="flora", seed=5580,
                  spec=kit.FloraSpec(coverage=0.34, scale=24, octaves=3, fernShare=0.38, flowerShare=0.08,
                                     flowerScale=16, tallShare=0.05),
                  # x -24..24, z 16..118 walked as a wandering ring
                  points=[
                      [-26.23, 13.87], [-11.03, 16.14], [1.8, 18.1], [13.12, 18.46], [24.58, 13.93], [24.07, 43.19],
                      [26.04, 68.9], [23.48, 94.41], [26.29, 116.6], [9.52, 115.92], [-1.65, 120.06], [-9.84, 115.95],
                      [-24.61, 117.14], [-22.05, 92.49], [-23.29, 67.16], [-22.85, 39.22]]),
]

# ---------------------------------------------------------------- the house
#
# Forked from the shipped `alpine mining` preset, whose footing is already
# null. The ground is deep green moss, so what stands on it is pale birch and
# quartz over a stone plinth — a building has to read as a built thing from
# across the gill, which means its walls are not in the family under its feet.

BIRCH_LOG = kit.LaidLogMaterial(id=17, data=2)

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}


def storey(clear, panel):
    """A storey `clear` blocks high, walled in a course of stone, `panel` courses of quartz and birch and a course
    of laid birch log."""
    return {
        "clear": clear,
        "wall": {"stack": {"bands": [
            {"material": STONE, "thickness": 1},
            {"material": cells(5591, 3, 2, [QUARTZ, BIRCH]), "thickness": panel},
            {"material": BIRCH_LOG, "thickness": 1}], "ending": "repeat"},
            "extent": clear},
        "post": solid(17, 2),
        "windows": {"form": "arched", "block": 135, "hostBlock": -1, "hostData": 0,
                    "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "surface": PLAIN, "deck": None, "headroom": clear,
    }


MILL = kit.build("HouseStyle", {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONE, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARKOAK, "verge": STONE, "gable": BIRCH,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": STONE, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 2),
    "windows": NO_WINDOW,
    "storeys": [storey(5, 3)],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 135, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 2},
                "width": 2, "height": 3},
})

# the spawn hall and the wool rooms: the mill, hipped and built taller
HALL = kit.build("HouseStyle", {
    **MILL,
    "roof": {"form": "hip", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": False, "hole": False,
             "body": DARKOAK, "verge": STONE, "gable": None,
             "gableWindows": NO_WINDOW},
    "storeys": [storey(7, 5)],
})

styles["mill"] = kit.HouseStyleRef(shell=MILL)

refinement = kit.Refinement(
    authors=["Opus 5"],
    created="2026-09-21",
    themes={"gill": gill_theme, "flush": flush_theme, "garth": garth_theme},
    mapTheme="gill",
    # Roofed forest (#79c05a): a deep wooded green for a board whose grass and
    # leaves are most of what a player sees. The palette states no podzol,
    # because that tint is too bright to meet brown and the pair would read as
    # neither ground. Asked of GET /api/terrain/biomes.
    biome=kit.SolidBiome(id=29),
    relief=relief,
    addShapes=add_shapes,
    # in base_y order, which is the order the world builds them in and what
    # SK20 complains about otherwise
    addLayers=[vault_walls, vault_deck],
    roomStyles=kit.SketchRoomStyles(spawn=HALL, wool=HALL),
    dressing=kit.DressingDoc(styles=styles, props=props),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
