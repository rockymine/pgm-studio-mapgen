"""Rimeholt — writes opus55-rimeholt.plan.json and .refinement.json.

A capture board in snow and spruce: each team's hub is a snowfield leaning up from its frontline to a timber
lookout on a hamlet behind it, log cabins on its corners, spruce fells off both its coasts, with a frozen tarn in its west corner and spruce standing along
its coasts. A ring of standing stones stands on the mid stone in the build band. Two wools a team, each at
the end of a spur behind a bedrock wall.

The arrangement is composed board p12 t2 #7 (`composed-p12-seed7.plan.json`, pinned off GET /api/compose).
One piece is added — the hamlet, twenty by eight blocks behind the hub's west half, flush with the spawn — and
nothing else about where the pieces stand is changed. Team 0 is the z > 0 half; rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-rimeholt"
plan = json.load(open(os.path.join(HERE, "composed-p12-seed7.plan.json")))
plan["meta"] = {"name": "Rimeholt", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 7 (walled-4), with a hamlet piece added behind the hub"}
plan["pieces"].append({"id": "hamlet", "rect": [-4, 20, 5, 2]})   # flush with the spawn, no gap (WL12)


# --- paint ----------------------------------------------------------------------------------------------
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


# Families: the ground white (snow over packed ice, grey rock where it is too steep to hold snow), the built
# brown (spruce logs laid and stood), the accent grey (the standing stones, the gravel of the paths).
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
SNOW = kit.NoiseMaterial(scale=3, seed=4, stops=[solid(174), solid(80), solid(80), solid(80)])
snowfield = finish(stack((stack((SNOW, 1), (solid(80), 2)), 32),
                         (stack((kit.CellMaterial(cellSize=2, seed=5, palette=[solid(80), solid(1), solid(1, 5)]), 1),
                                (solid(1), 2)), 12),
                         (kit.CellMaterial(cellSize=2, seed=6, palette=[solid(1), solid(1, 5), solid(1), solid(4)]), 46),
                         axis="slope"),
                   wall=ROCK, fill=ROCK)
# Under the spruce: podzol and coarse dirt, the needle floor the snow does not lie on.
needles = finish(stack((stack((kit.NoiseMaterial(scale=2, seed=7,
                                                 stops=[solid(80), solid(3, 2), solid(3, 2), solid(3, 1)]), 1),
                              (solid(3), 2)), 46),
                       (kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(4)]), 44),
                       axis="slope"),
                 wall=ROCK, fill=ROCK)
# The tarn: packed ice set a course into the snow.
tarn = finish(stack((kit.CellMaterial(cellSize=2, seed=9, palette=[solid(174), solid(174), solid(79)]), 1),
                    (solid(1), 2)),
              wall=ROCK, fill=ROCK, depth=1)
stones = one(kit.CellMaterial(cellSize=2, seed=10, palette=[solid(1), solid(1, 5), solid(1, 6)], rise=2))
spruce = one(solid(5, 1))
logpost = one(solid(17, 1))

PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(13), solid(4), solid(1, 5)])

relief = {"team": kit.SketchReliefJson(
    base=10, reach=0, step=1, landform="rolling",
    marks=[
        kit.ReliefMarkJson(id="front", kind="area", h=9, ring=[[-17, 20], [17, 20], [17, 36], [-17, 36]]),
        kit.ReliefMarkJson(id="hub-back", kind="area", h=14, bevel=4,
                           ring=[[-17, 66], [17, 66], [17, 93], [-17, 93]]),
        kit.ReliefMarkJson(id="tarn-bed", kind="area", h=11, bevel=2),
        kit.ReliefMarkJson(id="spur-a", kind="line", r=6, tread=4, points=[[-18, 74], [-38, 74]], h=[13, 12]),
        kit.ReliefMarkJson(id="spur-b", kind="line", r=6, tread=4, points=[[18, 58], [38, 58]], h=[12, 11]),
    ],
    pushes=[
        # fells centred off the hub's two coasts: the spruce stands on their flanks, the snowfield between
        kit.ReliefPushJson(id="fell-west", amount=8, falloff=7, roughness=0.4, crown=0, seed=5),
        kit.ReliefPushJson(id="fell-east", amount=6, falloff=6, roughness=0.4, crown=0, seed=6),
    ])}

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "tarn-bed": kit.Outline(at=[-9, 52], radius=6, radiusZ=5, points=20, wobble=0.12, lobes=3),
    "fell-west": kit.Outline(at=[-27, 50], radius=10, radiusZ=12, points=24, wobble=0.15, lobes=3),
    "fell-east": kit.Outline(at=[28, 36], radius=8, radiusZ=7, points=24, wobble=0.15, lobes=3, phase=1),
    "tarn": kit.Outline(at=[-9, 52], radius=5, radiusZ=4, points=20, wobble=0.12, lobes=3),
}


# --- made things -------------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


layers = []
# Standing stones on the mid stone: eight, round its middle, belonging to nobody.
layers += made(props.colonnade("stones", -0.5, -0.5, 7, 8, 1.3, 9, 4, "stones", mirrors=False), "stones",
               seat="ground")
# The lookout over the hamlet: four log legs, a spruce deck nine up, and a roof over it on posts.
LX, LZ = -14, 82
legs = props.LayerBuilder("lookout-legs")
for dx in (0, 4):
    for dz in (0, 4):
        legs.rect(LX + dx, LZ + dz, LX + dx + 1, LZ + dz + 1, 13, 14, "logpost")
deck = props.LayerBuilder("lookout-deck")
deck.rect(LX + 1, LZ + 1, LX + 4, LZ + 4, 21, 1, "spruce")
roof = props.LayerBuilder("lookout-roof")
roof.rect(LX - 1, LZ - 1, LX + 6, LZ + 6, 27, 1, "spruce")
layers += made([legs.done(), deck.done(), roof.done()], "lookout")
# Log piles on the frontline's two prongs, cover two courses tall.
piles = props.LayerBuilder("log-piles")
for x0, z0, x1, z1 in [(-14, 22, -11, 24), (11, 25, 14, 27), (-6, 31, -3, 33), (4, 34, 7, 36)]:
    piles.rect(x0, z0, x1, z1, 9, 2, "logpost")
layers += made(piles.done(), "log-piles", seat="ground")


# --- patches -------------------------------------------------------------------------------------------
def patch(pid, theme, vertices=None):
    """A patch of different ground on the hub: a polygon at the ground's height with its own theme, painting the
    cells it forms the surface of and nothing else."""
    return {**kit.SketchShape(id=pid, type="polygon", operation="add", base_height=9, theme=theme,
                              **({"vertices": vertices} if vertices else {})),
            **kit.ShapeJoin(group="team")}


shapes = [
    patch("tarn", "tarn"),
    patch("needles-west", "needles", [[-17, 40], [-9, 41], [-8, 46], [-9, 60], [-11, 66], [-17, 66]]),
    patch("needles-east", "needles", [[11, 40], [17, 40], [17, 54], [11, 54]]),
]

# --- dressing -------------------------------------------------------------------------------------------
# The copied trees, each the showcase tree it names, as corpus/tree-showcase/trees.json carries it.
SHOWCASE = json.load(open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")))["trees"]
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "tree-showcase-r7-1": "tall-spruce-1", "tree-showcase-r7-3": "tall-spruce-3",
    "tree-showcase-r4-2": "tiny-spruce-2", "tree-showcase-r4-4": "tiny-spruce-4"}.items()}
styles["cabin"] = kit.library("talltimber-cottage", kind="house")
styles["rock"] = kit.BoulderStyle(form="angular", size=2, mossy=False,
                                  rock=kit.CellMaterial(cellSize=2, seed=31, palette=[solid(1), solid(1, 5), solid(4)]))


def path(pid, seed, points, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=1.5, claimsGround=True, wander=wander,
                          wanderLength=14, pave=PAVE, points=points)


def house(pid, corners, front, seed):
    return kit.HouseProp(id=pid, style="cabin", seed=seed, front=front, wings=[kit.AuthoredWing(corners=corners)])


props_ = [
    path("path-front", 51, [[10, 82], [8, 70], [2, 56], [0, 42], [0, 30]]),
    path("path-wool-a", 52, [[-4, 74], [-16, 74], [-26, 74]], wander=1),
    path("path-wool-b", 53, [[4, 58], [16, 58], [24, 58]], wander=1),
    house("cabin-a", [[-16, 63], [-9, 70]], "posX", 31),
    house("cabin-b", [[12, 44], [16, 49]], "negX", 32),
    kit.TreeProp(id="s1", x=-15, z=44, style="tree-showcase-r7-1", seed=1),
    kit.TreeProp(id="s2", x=-15, z=58, style="tree-showcase-r7-3", seed=2),
    kit.TreeProp(id="s6", x=14, z=52, style="tree-showcase-r4-2", seed=6),
    kit.BoulderProp(id="r1", x=-12, z=26, style="rock", seed=7),
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=30),
    themes={"snowfield": snowfield, "needles": needles, "tarn": tarn, "stones": stones, "spruce": spruce,
            "logpost": logpost},
    mapTheme="snowfield",
    relief=relief,
    outlines=outlines,
    addShapes=shapes,
    addLayers=layers,
    roomStyles={"spawn": kit.library("talltimber-hall"), "wool": kit.library("talltimber-hall")},
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
