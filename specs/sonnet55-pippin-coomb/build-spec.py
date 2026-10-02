#!/usr/bin/env python3
"""Pippin Coomb — a cider-orchard valley in chalk downland, two hamlets across a dry coomb.

Writes <slug>.plan.json and <slug>.refinement.json beside itself; tools/drive.py runs this first.
Every document is stated through the studio's own kit (GET /api/kit.py), so a wrong word or a wrong type
is refused here, before anything is posted.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from studio_kit import kit  # noqa: E402

SLUG = "sonnet55-pippin-coomb"
POND = (-22, -39)          # the dew pond, in the third lynchet
S = kit.SolidMaterial

# ── the plan: one team's ground, a build zone across the coomb, one monument ─────────────────────────────
# Team 0 stands north (z < 0); mirror_z fans it south. Cells are four blocks.
plan = kit.PlanModel(
    plan=2,
    meta=kit.PlanMeta(name="Pippin Coomb", authors=["Claude Sonnet 5.5"]),
    globals=kit.PlanGlobals(cell=4, symmetry="mirror_z", maxPlayers=10, surface=34),
    pieces=[
        kit.PlanPiece(id="down-w", rect=[-11, -28, 8, 7]),
        kit.PlanPiece(id="spawn", role="spawn", rect=[-3, -28, 5, 7]),
        kit.PlanPiece(id="down-e", rect=[2, -28, 9, 7]),
        kit.PlanPiece(id="farm", rect=[-11, -21, 22, 18]),
    ],
    zones=[kit.PlanZone(id="bridge", rect=[-11, -4, 22, 8])],
    placements=kit.PlanPlacements(
        spawns=[kit.SpawnPlacement(id="spawn-0", piece="spawn", at=[10, 10], facing="back",
                                   footprint=[1, 1, 18, 18])],
        destroyables=[kit.DestroyablePlacement(id="monument", piece="farm", at=[52, 26], style="pillar-3",
                                               materials="obsidian", float=4)],
    ),
)

def circle(cx, cz, radius, points=16):
    """A ring of `points` vertices about (cx, cz)."""
    return [[round(cx + radius * math.cos(2 * math.pi * k / points), 1),
             round(cz + radius * math.sin(2 * math.pi * k / points), 1)] for k in range(points)]


# ── the paint ────────────────────────────────────────────────────────────────────────────────────────────
GRASS, DIRT, COARSE = S(id=2), S(id=3), S(id=3, data=1)


def depth_stack(*bands):
    """One course of the first material over the rest."""
    return kit.LayeredMaterial(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=m, thickness=t) for m, t in bands]))


def cell(blocks, size=3, seed=1, jitter=70, warp=2, rise=None):
    """Even shares of a few blocks. A face wants `rise`, the vertical period that gives it grain (PT4)."""
    stated = {} if rise is None else {"rise": rise}
    return kit.CellMaterial(seed=seed, cellSize=size, jitter=jitter, warp=warp,
                            palette=[S(id=b, data=d) for b, d in blocks], **stated)


# chalk: warm white and two pale greys, one tone carried by three textures
CHALK = cell([(155, 0), (155, 0), (155, 0), (1, 4), (1, 3)], size=3, seed=11)
# The strata under the turf, read top to bottom: grass and two dirt (the surface bucket), then a slow fade from
# the dirt mix into granite, a granite bed that fades into chalk, and chalk as the deep rock. Each fade bed is a
# `cell` whose palette repeats entries to set the shares; `rise` gives a face its grain (PT4).
DIRTMIX = [(3, 0), (3, 1)]
GRANITE, POLISHED, CHALKBLOCKS = [(1, 1)], [(1, 2)], [(155, 0), (1, 4), (1, 3)]


def mix(upper, lower, upper_parts, total=8, seed=0, size=3):
    """`upper_parts` of `total` palette entries from `upper`, the rest from `lower`."""
    upper_cells = [upper[k % len(upper)] for k in range(upper_parts)]
    lower_cells = [lower[k % len(lower)] for k in range(total - upper_parts)]
    return cell(upper_cells + lower_cells, size=size, seed=seed, rise=2)


CHALK_FACE = cell([(155, 0), (155, 0), (155, 0), (1, 4), (1, 3)], size=3, seed=11, rise=3)
# bottom to top, because a height stack reads upward from `from`: chalk, chalk into granite, granite, granite into
# dirt, dirt. `follow` 100 carries the datum with the ground averaged over `reach` cells, so the beds ride the land.
STRATA_BEDS = [
    (CHALK_FACE, 42),                                         # the deep rock
    (mix(GRANITE + POLISHED, CHALKBLOCKS, 2, seed=61), 2),     # 25% granite, 75% chalk
    (mix(GRANITE + POLISHED, CHALKBLOCKS, 4, seed=62), 2),     # 50 / 50
    (mix(GRANITE + POLISHED, CHALKBLOCKS, 6, seed=63), 2),     # 75 / 25
    (cell([(1, 1), (1, 1), (1, 2)], size=3, seed=64, rise=2), 3),  # granite
    (mix(DIRTMIX, GRANITE, 2, seed=65), 2),                    # 25% dirt mix, 75% granite
    (mix(DIRTMIX, GRANITE, 4, seed=66), 2),                    # 50 / 50
    (mix(DIRTMIX, GRANITE, 6, seed=67), 2),                    # 75 / 25
    (cell(DIRTMIX, size=3, seed=68, rise=2), 1),               # the dirt mix, carried up to the surface bucket
]
STRATA = kit.LayeredMaterial(axis="height", from_=-60, follow=100, reach=16, stack=kit.BandStack(
    ending="repeat", bands=[kit.Band(material=m, thickness=n) for m, n in STRATA_BEDS]))

DOWN_SURFACE = kit.LayeredMaterial(axis="slope", stack=kit.BandStack(ending="repeat", bands=[
    kit.Band(material=depth_stack((GRASS, 1), (DIRT, 2)), thickness=36),
    kit.Band(material=depth_stack((cell([(3, 0), (3, 1)], size=3, seed=5), 1), (DIRT, 2)), thickness=9),
    kit.Band(material=depth_stack((cell(DIRTMIX, size=3, seed=5, rise=2), 1), (mix(DIRTMIX, GRANITE, 4, seed=66), 1), (mix(DIRTMIX, GRANITE, 2, seed=65), 1)), thickness=45),
]))

# the brown earth of yards, grove floors and lanes: three textures of one tone
EARTH = cell([(3, 2), (3, 0), (3, 2), (3, 1)], size=3, seed=21)

themes = {
    "farmstead": kit.TerrainTheme(
        bedrock=kit.BedrockSpec(relative=False, value=1), rimEdges="void", edgesFromGround=True,
        rim=kit.TopBand(enabled=False, depth=1, material=CHALK),
        surface=kit.TopBand(enabled=True, depth=3, material=depth_stack((EARTH, 1), (DIRT, 2))),
        wallEnabled=True, wallOnTerrainFaces=True, wall=STRATA, fill=STRATA),
    "chalk": kit.TerrainTheme(
        bedrock=kit.BedrockSpec(relative=False, value=1), rimEdges="void", edgesFromGround=True,
        rim=kit.TopBand(enabled=False, depth=1, material=CHALK),
        surface=kit.TopBand(enabled=True, depth=3, material=CHALK),
        wallEnabled=True, wallOnTerrainFaces=True, wall=STRATA, fill=STRATA),
    "down": kit.TerrainTheme(
        bedrock=kit.BedrockSpec(relative=False, value=1),
        rimEdges="void",
        rim=kit.TopBand(enabled=False, depth=1, material=CHALK),
        surface=kit.TopBand(enabled=True, depth=3, material=DOWN_SURFACE),
        wallEnabled=True, wallOnTerrainFaces=True, wall=STRATA, fill=STRATA),
}

# ── shapes and layers, stated through the kit ────────────────────────────────────────────────────────────
def rect(shape_id, x0, z0, x1, z1, floor=0, height=1, **rest):
    rest.setdefault("keepClear", True)
    return kit.SketchShape(id=shape_id, type="rectangle", operation="add",
                           min_x=x0, min_z=z0, max_x=x1, max_z=z1, floor=floor, base_height=height, **rest)


def disc(shape_id, cx, cz, radius, floor=0, height=1, **rest):
    rest.setdefault("keepClear", True)
    return kit.SketchShape(id=shape_id, type="circle", operation="add",
                           center_x=cx, center_z=cz, radius=radius, floor=floor, base_height=height, **rest)


def made_layer(layer_id, base_y, shapes, part_of, mirrors=True, **rest):
    """One made thing's slab: a layer of its own over its own span, grouped so its mirror is stated."""
    return kit.AddedLayer(id=layer_id, name=layer_id, base_y=base_y, kind="made", part_of=part_of,
                          shapes=shapes,
                          groups=[kit.SketchGroup(id=f"{layer_id}-g", name=layer_id, mirrors=mirrors,
                                                  shapeIds=[s["id"] for s in shapes])], **rest)


layers, patches = [], []

# ── the undercroft: a sunk cellar under the cider barn, a crawl east, a chamber under a barrow ───────────
# The pits are relief; what roofs them is made. Yard top block is y33, the pits' floor block y29, so a roof
# slab laid at y33 leaves three blocks of air (y30-32) in the cellar and two under the crawl.
layers.append(made_layer("cellar-roof", 33, [
    rect("cellar-slab", 13, -79, 26, -68, theme="farmstead")], part_of="undercroft"))
layers.append(made_layer("crawl-roof", 32, [
    rect("crawl-slab", 26, -76, 32, -72, floor=0, height=2, theme="farmstead")], part_of="undercroft"))
mound = [disc(f"mound-{k}", 36, -74, 7.5 - 2 * k, height=1 + k, theme="down") for k in range(4)]
layers.append(made_layer("barrow-mound", 33, mound, part_of="barrow"))

# the floors of the sunk rooms are chalk, painted as a patch over the ground that the relief leaves there
for patch_id, x0, z0, x1, z1 in (("cellar-floor", 14, -78, 26, -69), ("crawl-floor", 26, -75, 31, -73),
                                 ("chamber-floor", 31, -78, 41, -70)):
    patches.append(rect(patch_id, x0, z0, x1, z1, floor=0, height=60, theme="chalk"))

# ── small made things: barrels, a well, a cider press, a bench ───────────────────────────────────────────
def ring_points(cx, cz, radius, points=24, reverse=False):
    order = range(points - 1, -1, -1) if reverse else range(points)
    return [[round(cx + radius * math.cos(2 * math.pi * k / points), 2),
             round(cz + radius * math.sin(2 * math.pi * k / points), 2)] for k in order]


def annulus(cx, cz, outer, inner, points=24):
    """A ring as one outline: outer circle, a slit inward, the inner circle the other way, and back (even-odd)."""
    out_ring, in_ring = ring_points(cx, cz, outer, points), ring_points(cx, cz, inner, points, reverse=True)
    return out_ring + [out_ring[0]] + in_ring + [in_ring[0]]


def column(shape_id, x, z, floor, height, material, **rest):
    """One block column of a thing: x/z name the block, the span runs [floor, floor + height)."""
    return rect(shape_id, x, z, x + 1, z + 1, floor=floor, height=height, material=material, **rest)


BARREL = S(id=5, data=5)
barrels = []
for k, x in enumerate((15, 18, 21)):
    barrels.append(rect(f"barrel-n{k}", x, -78, x + 2, -76, height=2, material=BARREL))
    barrels.append(rect(f"barrel-s{k}", x, -71, x + 2, -69, height=2, material=BARREL))
layers.append(made_layer("barrels", 30, barrels, part_of="undercroft"))

# the well: a stone ring, two posts and a beam over the water
WELLSTONE = cell([(98, 0), (4, 0), (1, 5)], size=2, seed=31, rise=2)
OAKLOG = S(id=162, data=1)
WELL = (-6.5, -73.0)
layers.append(made_layer("well", 0, [
    kit.SketchShape(id="well-ring", type="polygon", operation="add", keepClear=True, floor=0, base_height=3,
                    vertices=annulus(WELL[0], WELL[1], 2.8, 1.7), material=WELLSTONE),
    column("well-post-w", -9, -74, 0, 6, OAKLOG),
    column("well-post-e", -5, -74, 0, 6, OAKLOG),
    rect("well-beam", -8, -74, -5, -73, floor=5, height=1, material=OAKLOG, keepClear=False),
], part_of="well", seat="ground"))

# the cider press: a planked bed, two posts and a screw of dark oak, a beam across
PLANK = S(id=5, data=1)
PX, PZ = 19, -64
layers.append(made_layer("cider-press", 0, [
    rect("press-bed-n", PX, PZ, PX + 5, PZ + 1, floor=0, height=1, material=PLANK),
    rect("press-bed-s", PX, PZ + 2, PX + 5, PZ + 3, floor=0, height=1, material=PLANK),
    column("press-post-w", PX, PZ + 1, 0, 5, OAKLOG, override=True),
    column("press-screw", PX + 2, PZ + 1, 0, 5, OAKLOG, override=True),
    column("press-post-e", PX + 4, PZ + 1, 0, 5, OAKLOG, override=True),
    column("press-beam-w", PX + 1, PZ + 1, 4, 1, OAKLOG, override=True),
    column("press-beam-e", PX + 3, PZ + 1, 4, 1, OAKLOG, override=True),
], part_of="press", seat="ground"))

# the bench under the old oak, three wide and two deep, its back to the hill and its face to the coomb
BX, BZ = -38, -27
layers.append(made_layer("bench", 0, [
    column("bench-bl", BX, BZ, 0, 3, PLANK), column("bench-bm", BX + 1, BZ, 1, 2, PLANK),
    column("bench-br", BX + 2, BZ, 0, 3, PLANK),
    column("bench-fl", BX, BZ + 1, 0, 2, PLANK), column("bench-fm", BX + 1, BZ + 1, 1, 1, PLANK),
    column("bench-fr", BX + 2, BZ + 1, 0, 2, PLANK),
], part_of="bench", seat="ground"))

# three round hayricks behind the farmhouse: a disc of bales under a smaller one
HAY = S(id=170, data=0)
ricks = []
for k, (rx, rz) in enumerate(((-31, -86), (-24, -88), (-17, -86))):
    ricks.append(disc(f"rick-{k}", rx, rz, 2.6, height=3, material=HAY))
    ricks.append(disc(f"rick-{k}-crown", rx, rz, 1.4, height=4, material=HAY, override=True))
layers.append(made_layer("hayricks", 0, ricks, part_of="hayricks", seat="ground"))

# ── patches of ground: worn earth where people stand, the dew pond's bed, the grove floors ───────────────
for patch in (
        rect("ramp-earth", 2, -76, 14, -72, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("well-yard", WELL[0], WELL[1], 4.5, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("press-yard", PX + 2.5, PZ + 1.5, 5, floor=0, height=60, theme="farmstead", keepClear=False),
        rect("barn-apron", 15, -67, 26, -64, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("pond-bed", POND[0], POND[1], 5.2, floor=0, height=60, theme="chalk", keepClear=False),
        disc("grove-1", -42, -48, 3.5, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("grove-2", -34, -48, 3.5, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("fairy-ring", 36, -86, 3.8, floor=0, height=60, theme="farmstead", keepClear=False),
        disc("grove-3", -17, -48, 3.5, floor=0, height=60, theme="farmstead", keepClear=False)):
    patches.append(patch)

# the white horse: cut into the south face of Horse Hill, drawn upright for someone standing south of it
HORSE_X, HORSE_Z = 19.0, -27.0


def horse_part(part_id, outline):
    """An outline in (u east, v north) turned onto the ground, where north is -z."""
    return kit.SketchShape(id=part_id, type="polygon", operation="add", keepClear=True, floor=0, base_height=60,
                           theme="chalk", vertices=[[HORSE_X + u, HORSE_Z - v] for u, v in outline])


for part in (("horse-body", [(3, 5), (15, 5), (15, 8.5), (3, 8.5)]),
             ("horse-hind-1", [(3, 0), (5.5, 0), (5.5, 5), (3, 5)]),
             ("horse-hind-2", [(6.5, 1), (8.5, 1), (8.5, 5), (6.5, 5)]),
             ("horse-fore-1", [(12.5, 0), (15, 0), (15, 5), (12.5, 5)]),
             ("horse-fore-2", [(9.5, 1), (11.5, 1), (11.5, 5), (9.5, 5)]),
             ("horse-neck", [(13, 8), (16.5, 8), (19.5, 13.5), (16.5, 13.5)]),
             ("horse-head", [(17, 12.5), (23, 11), (23, 13), (20, 14.5), (17, 14.5)]),
             ("horse-tail", [(3, 8.5), (3, 6.5), (0, 3.5), (0, 7)])):
    patches.append(horse_part(*part))


# ── dressing: what is placed, each for a reason ──────────────────────────────────────────────────────────
styles = {
    "cottage": kit.library("brick-roofed-terracotta-and-oak-house", kind="house"),
    "barn": kit.library("hay-gambrel-barn", kind="house"),
    "orchard-oak": kit.library("tiny-oak-3", kind="tree"),
    "old-oak": kit.library("large-oak-1", kind="tree"),
    "flint-cairn": kit.BoulderStyle(form="cairn", size=2.0, mossy=False,
                                    rock=cell([(1, 0), (1, 5), (4, 0), (1, 0)], size=2, seed=43)),
    "flint": kit.BoulderStyle(form="angular", size=1.0, mossy=False,
                              rock=cell([(1, 0), (1, 5), (4, 0), (1, 0)], size=2, seed=41)),
}
props = []

# paths first: each is a way somebody walks, three blocks wide, paved a third each of three earths
LANE_PAVE = cell([(3, 0), (3, 1), (5, 1)], size=3, seed=51)


def path(path_id, points, wander=1.5):
    return kit.StrokeProp(id=path_id, points=points, radius=1.5, style="solid", claimsGround=True,
                          wander=wander, wanderLength=12, pave=LANE_PAVE, seed=len(props) + 1)


props += [
    # the hall opens through its west and east walls, so a way leaves each door and both run into the lane
    path("from-the-west-door", [[-13, -102], [-16, -97], [-11, -92], [-5, -90], [-1, -86]], wander=0.8),
    path("from-the-east-door", [[9, -102], [12, -97], [8, -92], [3, -89.5], [0, -86]], wander=0.8),
    path("lane", [[-1, -88], [-1, -82], [2, -72], [6, -64], [8, -62]]),
    path("to-barn", [[3, -67], [10, -65.5], [20, -65.5]], wander=0.8),
    path("to-houses", [[-1, -77], [-8, -78.5], [-14, -76]], wander=0.8),
    path("orchard-track", [[-3, -67], [-14, -66], [-28, -66.5], [-42, -65.5]], wander=1.2),
    path("to-the-bench", [[-25, -66], [-24, -55], [-26, -46], [-29, -37], [-32, -29]]),
    path("down-to-the-lip", [[8, -54], [6, -42], [3, -30], [1, -16]]),
    path("to-the-cairn", [[16, -56], [20, -54], [24, -51]]),
    path("to-the-ricks", [[-14, -78], [-15, -84], [-22, -85.5], [-28, -85]], wander=0.8),
]

# houses: one style in two plots, a storey apart, and a barn over the cellar
props += [
    kit.HouseProp(id="farmhouse", style="cottage", front="posX", seed=3,
                  wings=[kit.AuthoredWing(corners=[[-25, -80], [-12, -71]], spec=kit.WingSpec(storeysHigh=2))]),
    kit.HouseProp(id="cottage", style="cottage", front="posX", seed=4,
                  wings=[kit.AuthoredWing(corners=[[-35, -77], [-29, -70]], spec=kit.WingSpec(storeysHigh=1))]),
    kit.HouseProp(id="cider-barn", style="barn", front="posZ", seed=5,
                  wings=[kit.AuthoredWing(corners=[[14, -91], [26, -83]], spec=kit.WingSpec(storeysHigh=1))]),
]

# the well's water, three blocks down inside the stone ring
props.append(kit.FluidProp(id="well-water", shape="pool", fluid="water", level=30, depth=5, radius=0.5,
                           points=ring_points(WELL[0], WELL[1], 1.5, points=10), seed=15))

# the dew pond, in a hollow the relief digs, with its lilies and a stone standing in the water
props += [
    kit.FluidProp(id="dew-pond", shape="basin", fluid="water", level=25, points=ring_points(POND[0], POND[1], 5.4, points=18),
                  seed=11),
    kit.BoulderProp(id="pond-stone", style="flint", x=POND[0], z=POND[1], seed=12),
    kit.BoulderProp(id="barrow-stone", style="flint", x=36, z=-85, seed=13),
    kit.BoulderProp(id="down-cairn", style="flint-cairn", x=30, z=-46, seed=14),
]

# the orchard: two rows on the two lynchets, each tree where a row of trees would be planted
for k, (xa, xb) in enumerate(((-42, -42), (-34, -34), (-16, -17), (-8, -9))):
    props.append(kit.TreeProp(id=f"apple-a{k}", style="orchard-oak", x=xa, z=-60, seed=20 + k))
    props.append(kit.TreeProp(id=f"apple-b{k}", style="orchard-oak", x=xb, z=-48, seed=30 + k))
props.append(kit.TreeProp(id="old-oak", style="old-oak", x=-38, z=-34, seed=40))

# the hidden room's chest
props.append(kit.ChestProp(id="barrow-chest", x=36, z=-74, y=30, facing="posZ", seed=50, items=[
    kit.ChestItem(item="apple", count=6), kit.ChestItem(item="bread", count=4)]))

# ground cover: one outline for the whole ground, and two small ones where the water and the podzol are
props += [
    kit.FloraProp(id="pond-lilies", seed=61, points=ring_points(POND[0], POND[1], 5.4, points=12),
                  spec=kit.FloraSpec(coverage=0.3, scale=3, fernShare=0, tallShare=0, flowerShare=0, lilyShare=0.6)),
    kit.FloraProp(id="fairy-ring", seed=63, points=ring_points(36, -86, 4.2, points=10),
                  spec=kit.FloraSpec(coverage=0.8, scale=3, fernShare=0, tallShare=0, flowerShare=0, mushroomShare=0.7)),
    kit.FloraProp(id="grove-fungi", seed=62, points=[[-45, -52], [-14, -52], [-14, -44], [-45, -44]],
                  spec=kit.FloraSpec(coverage=0.5, scale=4, fernShare=0, tallShare=0, mushroomShare=0.4)),
    kit.FloraProp(id="down-cover", seed=60, points=[[-43, -111], [42, -111], [42, -14], [-43, -14]],
                  spec=kit.FloraSpec(coverage=0.2, scale=9, fernShare=0, tallShare=0.02, flowerShare=0.12,
                                     flowerScale=7)),
]

refinement = kit.Refinement(
    created="2026-10-02",
    authors=["Claude Sonnet 5.5"],
    themes=themes,
    # the coomb's rim is not a ruled line: seven points pulled inland along the one edge that faces the gap
    editShapes={"down-e-34": [kit.VertexEdit(pulls={"2": [[0.07, 2.5], [0.18, 0.5], [0.3, 4], [0.43, 1],
                                                           [0.55, 3.5], [0.68, 0.5], [0.8, 3], [0.92, 1]]})]},
    # and drawn as a coast along that edge, so the pulled points are joined by curves rather than chords
    bendShapes={"down-e-34": kit.ShapeBend(wander=1.2, step=6, seed=4, tension=0.22, side="in", edges=list(range(2, 11)))},
    # the dew pond's outline is stated by its shape, a lobed ellipse, the same for the pit, the water and the lilies
    outlines={pond_id: kit.Outline(at=[POND[0], POND[1]], radius=radius, radiusZ=radius * 0.85, lobes=4,
                                   wobble=0.1, turn=20, points=20)
              for pond_id, radius in (("dew-pond-pit", 3.2), ("dew-pond", 5.4), ("pond-lilies", 5.4))},
    addLayers=layers,
    addShapes=patches,
    dressing=kit.DressingDoc(styles=styles, props=props),
    mapTheme="down",
    roomStyles=kit.SketchRoomStyles(spawn=kit.library("oak-and-spruce-timbered-house")),
    biome=kit.SolidBiome(id=35),
    relief={"team": kit.SketchReliefJson(
        base=30, reach=0, step=1, landform="hills",
                marks=[
            kit.ReliefMarkJson(id="spawn-pad", kind="area", h=36, bevel=2,
                               ring=[[-14, -113], [10, -113], [10, -83], [-14, -83]]),
            kit.ReliefMarkJson(id="yard", kind="area", h=34, bevel=3,
                               ring=[[-34, -81], [52, -81], [52, -66], [-34, -66]]),
            # the monument's shelf, off the centre line
            kit.ReliefMarkJson(id="shelf", kind="area", h=32, bevel=3, ring=circle(8, -58, 9)),
            # two chalk-cut lynchets under the orchard: level strips with a steep little bank between them
            kit.ReliefMarkJson(id="bank-1", kind="scarp", high=31, low=29, face=2, band=5,
                               points=[[-14, -55], [-44, -55]]),
            kit.ReliefMarkJson(id="bank-2", kind="scarp", high=29, low=27, face=2, band=5,
                               points=[[-14, -43], [-44, -43]]),
            kit.ReliefMarkJson(id="apron", kind="area", h=24, bevel=1,
                               ring=[[-43, -26], [43, -26], [43, -13], [-43, -13]]),
            # the undercroft: a sunk ramp from the lane, a cellar, a crawl and a chamber, all floored at 30
            kit.ReliefMarkJson(id="cellar-ramp", kind="line", r=2, tread=2, points=[[2, -74], [14, -74]], h=[34, 30]),
            kit.ReliefMarkJson(id="cellar-pit", kind="area", h=30, bevel=0,
                               ring=[[14, -78], [26, -78], [26, -69], [14, -69]]),
            kit.ReliefMarkJson(id="crawl", kind="area", h=30, bevel=0,
                               ring=[[26, -75], [31, -75], [31, -73], [26, -73]]),
            kit.ReliefMarkJson(id="chamber", kind="area", h=30, bevel=0,
                               ring=[[31, -78], [41, -78], [41, -70], [31, -70]]),
        ],
        pushes=[
            # Horse Hill: the down that carries the barrow on its crown and the white horse on its south face
            kit.ReliefPushJson(id="horse-hill", ring=circle(36, -42, 9), amount=6, falloff=14, crown=1,
                               roughness=1, seed=3),
            kit.ReliefPushJson(id="dew-pond-pit", ring=circle(POND[0], POND[1], 3.2, points=14), amount=-3, falloff=2, crown=0,
                               roughness=0, seed=5),
            kit.ReliefPushJson(id="oak-knoll", ring=circle(-35, -29, 6), amount=4, falloff=9, crown=1,
                               roughness=1, seed=4),
        ],
    )},
)


def write(name, document):
    path = os.path.join(HERE, f"{SLUG}.{name}.json")
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
    return path


if __name__ == "__main__":
    write("plan", plan)
    write("refinement", refinement)
    print("wrote", SLUG, "plan + refinement")
