"""Quarrymoot — writes opus55-quarrymoot.plan.json and .refinement.json.

A King of the Hill board in a red-sandstone quarry. The two spawns stand on the quarry's rim at either end
and look into a pit that steps down one bench to a floor. Three hills: the centre on the floor under a
crusher house's roof, paying double, and one on each side of the bench across the line between the spawns.
Four haul roads come down the benches, a conveyor gantry crosses the whole pit at rim height over the
crusher house, and quarried blocks stand about the floor and the benches as cover.

`match-flow.md` §10 is the law it is built to: the ground is made, a point is not raised over the ground
round it, the centre pays more than the flanks, cover is placed in two sizes, and every part of the board
is a way toward a point. The centre sits lowest and is roofed, so nothing on the rim has a line onto its pad
and the gantry above it is a second storey fought over the same footprint.

The board is one landmass: each team's half of the quarry is one piece, the two meeting on the axis (a
landmass may not mix a fanned piece with an unfanned one, PL12). rot_180 fans the halves, the spawns, the
made things marked to mirror and every prop; the crusher house and the gantry are stated once, off it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-quarrymoot"
RIM, BENCH, FLOOR = 22, 18, 14

plan = {
    "plan": 2,
    "meta": {"name": "Quarrymoot", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": RIM},
    "pieces": [
        {"id": "half", "rect": [-16, 0, 32, 18]},
        {"id": "spawn", "role": "spawn", "rect": [-3, 18, 6, 4], "surface": 24},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [12, 10], "facing": "front",
                    "footprint": [2, 2, 20, 12]}],
        "controlPoints": 3,
    },
}


# --- paint ------------------------------------------------------------------------------------------------
def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def stack(*bands, **reading):
    """A layered material: (material, thickness) bands repeating, read along `reading`."""
    return kit.LayeredMaterial(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=material, thickness=thickness) for material, thickness in bands]), **reading)


def finish(surface, wall, fill, depth=3, rim=None, rim_edges="void"):
    return kit.TerrainTheme(bedrock=kit.BedrockSpec(relative=False, value=1), rimEdges=rim_edges,
                            rim=kit.TopBand(enabled=rim is not None, depth=1, material=rim or solid(1)),
                            wallEnabled=True, wallOnTerrainFaces=True, wall=wall, fill=fill,
                            surface=kit.TopBand(enabled=True, depth=depth, material=surface))


def one(material):
    """A theme answering one material in every bucket — a made thing too thin to have a core."""
    return finish(material, material, material, depth=1, rim=material, rim_edges="boundary")


# Families: the ground orange (red sand, red sandstone and orange clay in the pit; turf on the rim under a
# Mesa sky that tints it to meet them), the built grey and dark (stone brick, dark-oak timber), the accent the
# gravel of the haul roads and the iron of the gantry's rails.
ORANGE = kit.CellMaterial(cellSize=2, seed=3, palette=[solid(12, 1), solid(179), solid(159, 1)])
WORN = kit.CellMaterial(cellSize=2, seed=4, palette=[solid(3), solid(3, 1)])
PIT_FLOOR = kit.NoiseMaterial(scale=2, seed=5, stops=[WORN, ORANGE, ORANGE, ORANGE, solid(172)])
STRATA = stack(*([(kit.CellMaterial(cellSize=2, seed=6, palette=[solid(179), solid(179, 2)], rise=2), 3),
                  (solid(159, 1), 1), (solid(179), 2), (solid(172), 1), (solid(179, 2), 2), (solid(159, 1), 1)] * 7
                 + [(solid(179), 1)]),
               axis="height", from_=-40, follow=100, reach=16, beyond=solid(179))
quarry = finish(stack((stack((PIT_FLOOR, 1), (solid(179), 2)), 30),
                      (stack((kit.CellMaterial(cellSize=2, seed=7, palette=[solid(12, 1), solid(179)]), 1),
                             (solid(179), 2)), 14),
                      (STRATA, 46),
                      axis="slope"),
                wall=STRATA, fill=STRATA)
turf = finish(stack((stack((kit.NoiseMaterial(scale=2, seed=8, stops=[WORN, solid(2), solid(2), solid(2)]), 1),
                           (solid(3), 2)), 30),
                    (STRATA, 60),
                    axis="slope"),
              wall=STRATA, fill=STRATA)
brick = one(kit.CellMaterial(cellSize=2, seed=9, palette=[solid(98), solid(98), solid(98, 2), solid(1, 5)], rise=2))
timber = one(solid(5, 5))
post = one(solid(162, 1))
blocks = one(kit.CellMaterial(cellSize=2, seed=10, palette=[solid(179), solid(179, 2), solid(179)], rise=2))

PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(13), solid(1, 5), solid(4)])


def haul(pid, pts):
    return kit.ReliefMarkJson(id=pid, kind="line", r=5, tread=2, points=pts, h=[RIM, BENCH, FLOOR])


def image(p):
    """A block's rot_180 image."""
    return [-p[0] - 1, -p[1] - 1]


ROAD_A = [[-12, 66], [-38, 40], [-26, 17]]
ROAD_B = [[12, 66], [38, 40], [26, 17]]
relief = {"*": kit.SketchReliefJson(
    base=RIM, reach=0, step=1, landform="rolling",
    marks=[
        kit.ReliefMarkJson(id="bench", kind="area", h=BENCH, bevel=2),
        kit.ReliefMarkJson(id="floor", kind="area", h=FLOOR, bevel=2),
        kit.ReliefMarkJson(id="spawn-rim", kind="area", h=24, bevel=3,
                           ring=[[-14, 72], [14, 72], [14, 90], [-14, 90]]),
        haul("road-a", ROAD_A), haul("road-b", ROAD_B),
        haul("road-a2", [image(p) for p in ROAD_A]), haul("road-b2", [image(p) for p in ROAD_B]),
    ],
    pushes=[
        # spoil heaps on the rim, either side of each spawn's view down into the pit
        kit.ReliefPushJson(id="spoil-w", amount=6, falloff=5, roughness=0.4, crown=0, seed=3),
        kit.ReliefPushJson(id="spoil-e", amount=6, falloff=5, roughness=0.4, crown=0, seed=3),
        kit.ReliefPushJson(id="spoil-e2", amount=5, falloff=5, roughness=0.4, crown=0, seed=4),
        kit.ReliefPushJson(id="spoil-w2", amount=5, falloff=5, roughness=0.4, crown=0, seed=4),
    ])}

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "bench": kit.Outline(at=[-0.5, -0.5], radius=50, radiusZ=42, points=48),
    "floor": kit.Outline(at=[-0.5, -0.5], radius=30, radiusZ=24, points=40),
    "spoil-w": kit.Outline(at=[-34, 62], radius=9, radiusZ=6, points=20, wobble=0.15, lobes=3),
    "spoil-e": kit.Outline(at=[33, -63], radius=9, radiusZ=6, points=20, wobble=0.15, lobes=3),
    "spoil-e2": kit.Outline(at=[34, 60], radius=7, radiusZ=5, points=20, wobble=0.15, lobes=3, phase=1),
    "spoil-w2": kit.Outline(at=[-35, -61], radius=7, radiusZ=5, points=20, wobble=0.15, lobes=3, phase=1),
    "sump": kit.Outline(at=[-2, 17], radius=4, radiusZ=3, points=20, wobble=0.15, lobes=3),
}


# --- made things ----------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


layers = []
# The crusher house over the centre: four 3x3 stone piers at its corners and a stone-slab roof six courses
# over the floor, open on every side. Stated for the whole board, off the mirror.
crusher = props.LayerBuilder("crusher-piers", mirrors=False)
for cx, cz in [(-10, -10), (8, -10), (-10, 8), (8, 8)]:
    crusher.rect(cx, cz, cx + 3, cz + 3, FLOOR - 1, 7, "brick")
roof = props.LayerBuilder("crusher-roof", mirrors=False)
roof.rect(-11, -11, 12, 12, FLOOR + 6, 1, "brick")
layers += made([crusher.done(), roof.done()], "crusher-house")
# The conveyor gantry: a timber deck at the rim's height from rim to rim across the pit, on log trestles
# stood on whatever they land on, passing over the crusher's roof.
gantry = props.LayerBuilder("gantry-deck", mirrors=False)
gantry.rect(-56, -3, 56, 3, RIM, 1, "timber", keepClear=False)
layers += made(gantry.done(), "gantry")
trestle = props.LayerBuilder("gantry-trestles", mirrors=False)
for x in (-54, -32, -21, 20, 31, 53):
    for z in (-3, 2):
        base = BENCH - 1 if abs(x + 0.5) > 30 else FLOOR - 1
        trestle.rect(x, z, x + 1, z + 1, base, RIM - base, "post")
layers += made(trestle.done(), "gantry")
# Quarried blocks as cover: small (two courses) on the floor and the benches, and two large stacks by the
# flank hills that a player goes round from two sides — one stated here, beside the west hill on this team's
# side, and its image beside the east hill on the other. One team's half, fanned.
cover = props.LayerBuilder("cover-blocks")
for x0, z0, w, d, h in [(-22, 6, 3, 2, 2), (-16, 16, 2, 3, 3), (16, 10, 2, 2, 2), (6, 20, 2, 3, 2),
                        (-28, 4, 2, 3, 2), (12, 16, 2, 2, 2)]:
    cover.rect(x0, z0, x0 + w, z0 + d, FLOOR - 1, h + 1, "blocks")
for x0, z0, w, d, h in [(-36, 14, 3, 2, 2), (34, 12, 3, 3, 3), (-48, 24, 3, 2, 2)]:
    cover.rect(x0, z0, x0 + w, z0 + d, BENCH - 1, h + 1, "blocks")
for x0, z0, w, d in [(-46, 8, 6, 7)]:
    cover.rect(x0, z0, x0 + w, z0 + d, BENCH - 1, 6, "blocks")
layers += made(cover.done(), "cover-blocks")

# --- patches ----------------------------------------------------------------------------------------------
# Turf on the rim outside the bench, one ring for the board: the board's edge, then the pit's edge the other
# way round as its hole — an ellipse of radii 53 and 45 about the board's centre, drawn with 48 points.
PIT_EDGE = [[52.5, -0.5], [52.0, 5.4], [50.7, 11.1], [48.5, 16.7], [45.4, 22.0], [41.5, 26.9], [37.0, 31.3],
            [31.8, 35.2], [26.0, 38.5], [19.8, 41.1], [13.2, 43.0], [6.4, 44.1], [-0.5, 44.5], [-7.4, 44.1],
            [-14.2, 43.0], [-20.8, 41.1], [-27.0, 38.5], [-32.8, 35.2], [-38.0, 31.3], [-42.5, 26.9],
            [-46.4, 22.0], [-49.5, 16.7], [-51.7, 11.1], [-53.0, 5.4], [-53.5, -0.5], [-53.0, -6.4],
            [-51.7, -12.1], [-49.5, -17.7], [-46.4, -23.0], [-42.5, -27.9], [-38.0, -32.3], [-32.8, -36.2],
            [-27.0, -39.5], [-20.8, -42.1], [-14.2, -44.0], [-7.4, -45.1], [-0.5, -45.5], [6.4, -45.1],
            [13.2, -44.0], [19.8, -42.1], [26.0, -39.5], [31.8, -36.2], [37.0, -32.3], [41.5, -27.9],
            [45.4, -23.0], [48.5, -17.7], [50.7, -12.1], [52.0, -6.4]]
outer = [[-64, -72], [64, -72], [64, 72], [-64, 72]]
shapes = [{**kit.SketchShape(id="rim-turf", type="polygon", operation="add",
                             vertices=outer + [outer[0]] + list(reversed(PIT_EDGE)) + [PIT_EDGE[-1]],
                             base_height=RIM, theme="turf"),
           **kit.ShapeJoin(group="team")}]

# --- dressing --------------------------------------------------------------------------------------------
# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "tree-showcase-r8-2": "acacia-2", "tree-showcase-r8-4": "acacia-4"}.items()}
styles["works"] = kit.library("banded-stone-house", kind="house")


def path(pid, seed, points):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=2, claimsGround=True, wander=0,
                          wanderLength=14, pave=PAVE, points=points)


def house(pid, corners, front, seed, storeys=None):
    return kit.HouseProp(id=pid, style="works", seed=seed, front=front, wings=[
        kit.AuthoredWing(corners=corners, **({"spec": kit.WingSpec(storeysHigh=storeys)} if storeys else {}))])


props_ = [
    path("road-a", 41, ROAD_A),
    path("road-b", 42, ROAD_B),
    path("rim-road", 43, [[-12, 70], [0, 71], [12, 70]]),
    kit.FluidProp(id="sump", shape="pool", form="natural", layer="ground", radius=2, depth=2, shore=1,
                  shoreWander=True, edge=1.5, fluid="water",
                  bank=kit.CellMaterial(cellSize=2, seed=61, palette=[solid(13), solid(12, 1)])),
    house("works-a", [[-54, 50], [-46, 58]], "posX", 31, storeys=2),
    house("works-b", [[44, 52], [52, 59]], "negX", 32),
    kit.TreeProp(id="a1", x=-56, z=36, style="tree-showcase-r8-2", seed=1),
    kit.TreeProp(id="a2", x=-58, z=64, style="tree-showcase-r8-4", seed=2),
    kit.TreeProp(id="a3", x=56, z=36, style="tree-showcase-r8-4", seed=3),
    kit.TreeProp(id="a4", x=24, z=66, style="tree-showcase-r8-2", seed=4),
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=37),
    themes={"quarry": quarry, "turf": turf, "brick": brick, "timber": timber, "post": post, "blocks": blocks},
    mapTheme="quarry",
    relief=relief,
    outlines=outlines,
    addShapes=shapes,
    addLayers=layers,
    roomStyles={"spawn": kit.library("andesite-gabled-house")},
    controlPoints=[
        kit.ControlPointIntent(name="Crusher", anchor=kit.Pt(x=0, z=0), size=7, points=2),
        kit.ControlPointIntent(name="West Bench", anchor=kit.Pt(x=-42, z=0), size=7, points=1),
        kit.ControlPointIntent(name="East Bench", anchor=kit.Pt(x=41, z=-1), size=7, points=1),
    ],
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
