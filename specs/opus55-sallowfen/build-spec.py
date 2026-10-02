"""Sallowfen — writes opus55-sallowfen.plan.json and .refinement.json.

A fen of willows and reed pools, where each team keeps two monuments on peat hummocks north and south of a
dry causeway running out from its spawn. A stream winds across the fen in front of both hummocks, crossed
by two plank boardwalks; pools lie in hollows on the flanks; a hamlet of stilt houses stands on the
causeway by the spawn, and a watch platform on four legs stands near the lip where a crossing lands. The
halves meet across a 32-block build zone over void the whole width of the board.

Team 0 is the west half (x < 0); rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-sallowfen"
SURFACE = 12

plan = {
    "plan": 2,
    "meta": {"name": "Sallowfen", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 20, "surface": SURFACE},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-35, -3, 4, 6], "surface": 16},
        {"id": "field", "rect": [-31, -16, 27, 32]},
    ],
    "zones": [{"id": "strait", "rect": [-4, -16, 4, 32]}],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [8, 12], "facing": "right",
                    "footprint": [1, 5, 14, 14]}],
        # field min corner (-124, -64): the south stone at (-78, -30), the north stone at (-76, 30)
        "destroyables": [
            {"id": "south", "piece": "field", "at": [46, 34], "style": "pillar-3", "name": "Willow Stone"},
            {"id": "north", "piece": "field", "at": [48, 94], "style": "pillar-3", "name": "Reed Stone"},
        ],
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


# Families: the ground green-brown (fen grass with podzol and worn earth), the built timber (spruce on
# stilts under oak roofs), the accent the grey of stone gables and the boardwalks' spruce.
# Swampland tints grass the olive that meets podzol as one leaf-littered floor.
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
GRASS, PODZOL = solid(2), solid(3, 2)
WORN = kit.CellMaterial(cellSize=2, seed=7, palette=[solid(3), solid(3, 1)])
FEN = kit.NoiseMaterial(scale=2, seed=5, stops=[PODZOL, GRASS, GRASS, GRASS, WORN])
PEAT = stack((ROCK, 30), (solid(82), 2), (solid(3), 3), (solid(3, 1), 1), (solid(3), 4), (solid(3), 20),
             axis="height", from_=-40, follow=100, reach=16, beyond=ROCK)
fen = finish(stack((stack((FEN, 1), (solid(3), 2)), 26), (stack((WORN, 1), (solid(3), 2)), 20), (PEAT, 44),
                   axis="slope"),
             wall=PEAT, fill=PEAT)
# The hummocks' tops: podzol under the willows, one leaf-littered floor on this biome.
hummock = finish(stack((stack((kit.NoiseMaterial(scale=2, seed=13, stops=[GRASS, PODZOL, PODZOL, GRASS]), 1),
                              (solid(3), 2)), 26),
                       (PEAT, 64),
                       axis="slope"),
                 wall=PEAT, fill=PEAT)
planks = one(solid(5, 1))
post = one(solid(17, 1))

PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(3), solid(3, 1), solid(5, 1)])

relief = {"team": kit.SketchReliefJson(
    base=SURFACE, reach=0, step=1, landform="plain",
    marks=[
        kit.ReliefMarkJson(id="knoll", kind="area", h=16, bevel=3,
                           ring=[[-142, -14], [-120, -14], [-120, 14], [-142, 14]]),
        kit.ReliefMarkJson(id="ramp", kind="line", r=4, points=[[-122, 0], [-108, 0]], h=[16, 13]),
        kit.ReliefMarkJson(id="causeway", kind="line", r=5, tread=3, points=[[-108, 0], [-84, 2], [-60, -1]],
                           h=[13, 13, 13]),
        kit.ReliefMarkJson(id="hummock-s", kind="area", h=17, bevel=4),
        kit.ReliefMarkJson(id="hummock-n", kind="area", h=17, bevel=4),
        kit.ReliefMarkJson(id="lip", kind="line", r=4, h=[11, 12, 11, 12, 11],
                           points=[[-19, -62], [-20, -30], [-18, 0], [-20, 30], [-19, 62]]),
    ],
    pushes=[
        # The south-west hollow and the north bank are stated by their points: each has points falling on a
        # twentieth of a block (the hollow's x -89.35 and -111.35, the bank's z 82.35), which an outline rounds
        # to the other tenth.
        kit.ReliefPushJson(id="hollow-sw", amount=-4, falloff=4, roughness=0.3, crown=0, seed=3, ring=[
            [-89.3, -42.0], [-90.2, -39.7], [-92.5, -38.0], [-95.0, -36.9], [-97.3, -36.1], [-99.5, -35.1],
            [-102.0, -34.0], [-105.1, -33.5], [-108.3, -34.0], [-110.6, -35.7], [-111.5, -38.0], [-111.5, -40.1],
            [-111.3, -42.0], [-111.5, -43.9], [-111.5, -46.0], [-110.6, -48.3], [-108.3, -50.0], [-105.1, -50.5],
            [-102.0, -50.0], [-99.5, -48.9], [-97.3, -47.9], [-95.0, -47.1], [-92.5, -46.0], [-90.2, -44.3]]),
        kit.ReliefPushJson(id="hollow-nw", amount=-4, falloff=4, roughness=0.3, crown=0, seed=4),
        kit.ReliefPushJson(id="hollow-front", amount=-2, falloff=4, roughness=0.3, crown=0, seed=5),
        # carr banks: wooded rises centred off both coasts, so the fen's flanks climb out of the wet
        kit.ReliefPushJson(id="bank-n", amount=6, falloff=8, roughness=0.4, crown=0, seed=6, ring=[
            [-43.5, 72.0], [-46.0, 74.2], [-51.9, 75.8], [-57.7, 76.9], [-61.8, 78.1], [-65.4, 79.8], [-70.7, 81.6],
            [-78.0, 82.3], [-85.3, 81.6], [-90.6, 79.8], [-94.2, 78.1], [-98.3, 76.9], [-104.1, 75.8],
            [-110.0, 74.2], [-112.5, 72.0], [-110.0, 69.8], [-104.1, 68.2], [-98.3, 67.1], [-94.2, 65.9],
            [-90.6, 64.2], [-85.3, 62.4], [-78.0, 61.6], [-70.7, 62.4], [-65.4, 64.2], [-61.8, 65.9],
            [-57.7, 67.1], [-51.9, 68.2], [-46.0, 69.8]]),
        kit.ReliefPushJson(id="bank-s", amount=5, falloff=8, roughness=0.4, crown=0, seed=7),
    ])}

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "hummock-s": kit.Outline(at=[-78, -30], radius=12, radiusZ=10, points=24, wobble=0.12, lobes=3),
    "hummock-n": kit.Outline(at=[-76, 30], radius=12, radiusZ=10, points=24, wobble=0.12, lobes=3, phase=1),
    "hollow-nw": kit.Outline(at=[-100, 44], radius=10, radiusZ=8, points=24, wobble=0.15, lobes=3, phase=2),
    "hollow-front": kit.Outline(at=[-30, -28], radius=7, radiusZ=9, points=24, wobble=0.15, lobes=3, phase=1),
    "bank-s": kit.Outline(at=[-96, -72], radius=26, radiusZ=9, points=28, wobble=0.15, lobes=4, phase=1),
    "hummock-s-top": kit.Outline(at=[-78, -30], radius=15, radiusZ=12, points=24, wobble=0.12, lobes=4),
    "hummock-n-top": kit.Outline(at=[-76, 30], radius=15, radiusZ=12, points=24, wobble=0.12, lobes=4, phase=1),
    "pool-sw": kit.Outline(at=[-102, -42], radius=8, radiusZ=5, points=20, wobble=0.15, lobes=3),
    "pool-nw": kit.Outline(at=[-100, 44], radius=7, radiusZ=5, points=20, wobble=0.15, lobes=3, phase=2),
    "pool-front": kit.Outline(at=[-30, -28], radius=4, radiusZ=6, points=20, wobble=0.15, lobes=3, phase=1),
}


# --- made things --------------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


layers = []
# Two boardwalks over the stream: one on the causeway, one in front of the north stone, a course over the fen
# so the stream runs under them (stated inside the ground's top course, they stopped the stream being cut).
walks = props.LayerBuilder("boardwalks")
# keepClear off: the builder states it on every shape, and a kept-clear column is one the dressing pass —
# the water with it — leaves alone, so the stream was never cut under a kept-clear deck.
walks.rect(-56, -3, -38, 4, 13, 1, "planks", keepClear=False)
walks.rect(-50, 36, -34, 41, 13, 1, "planks", keepClear=False)
layers += made(walks.done(), "boardwalks")
# The watch platform near the lip: four spruce legs and a plank deck six up, open to climb onto by pillar.
WX, WZ = -34, 12
legs = props.LayerBuilder("watch-legs")
for dx in (0, 5):
    for dz in (0, 5):
        legs.rect(WX + dx, WZ + dz, WX + dx + 1, WZ + dz + 1, 11, 7, "post")
deck = props.LayerBuilder("watch-deck")
deck.rect(WX - 1, WZ - 1, WX + 7, WZ + 7, 18, 1, "planks")
layers += made([legs.done(), deck.done()], "watch-platform")

# --- patches ------------------------------------------------------------------------------------------
shapes = [{**kit.SketchShape(id=pid, type="polygon", operation="add", base_height=SURFACE, theme="hummock"),
           **kit.ShapeJoin(group="team")} for pid in ("hummock-s-top", "hummock-n-top")]

# --- dressing -------------------------------------------------------------------------------------------
# The copied trees, each the showcase tree it names, as the studio's tree library carries it.
from showcase import trees as studio_trees
SHOWCASE = studio_trees()
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "tree-showcase-r17-1": "willow-1", "tree-showcase-r17-3": "willow-3", "tree-showcase-r17-5": "willow-5",
    "tree-showcase-r5-1": "dark-oak-1", "tree-showcase-r5-2": "dark-oak-2"}.items()}
# The stilt house stands over the fen rather than on a floor laid across it: the plate is air (HS10).
styles["stilt"] = kit.library("oak-stilt-house", kind="house", shell={"foundation": {
    "plate": {"stack": {"bands": [kit.Band(material=solid(0), thickness=1)], "ending": "repeat"}, "extent": 1},
    "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
    "footing": None}})
styles["rock"] = kit.BoulderStyle(form="round", size=2, mossy=True,
                                  rock=kit.CellMaterial(cellSize=2, seed=51, palette=[solid(1), solid(1, 5), solid(4)]))
BANK = kit.CellMaterial(cellSize=2, seed=61, palette=[solid(3), solid(3, 1), solid(13)])


def pool(pid, shore):
    return kit.FluidProp(id=pid, shape="pool", form="natural", layer="ground", radius=2, depth=2, shore=shore,
                         shoreWander=True, edge=1.5, fluid="water", bank=BANK)


def path(pid, seed, points, radius=1.5, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=radius, claimsGround=True, wander=wander,
                          wanderLength=14, pave=PAVE, points=points)


def house(pid, corners, front, seed, storeys=None):
    return kit.HouseProp(id=pid, style="stilt", seed=seed, front=front, wings=[
        kit.AuthoredWing(corners=corners, **({"spec": kit.WingSpec(storeysHigh=storeys)} if storeys else {}))])


props_ = [
    # water: the stream across the fen in front of both stones, and two pools in the flank hollows
    kit.FluidProp(id="stream", shape="channel", form="stream", layer="ground", radius=3, depth=2, shore=1,
                  shoreWander=True, edge=1.5, bank=BANK,
                  points=[[-44, 66], [-40, 44], [-46, 22], [-44, 2], [-50, -18], [-46, -42], [-52, -66]]),
    pool("pool-sw", 2),
    pool("pool-nw", 2),
    pool("pool-front", 1),
    # paths: the causeway, and a spur to each stone
    # the causeway, broken at the boardwalk: a stroke repaints the top course it crosses, water included, so
    # one drawn through the stream paved it over
    path("path-causeway", 41, [[-122, 0], [-104, 1], [-84, 2], [-66, 0], [-57, 0]], radius=2),
    path("path-causeway-east", 44, [[-37, 0], [-30, 1], [-22, 0]], radius=2, wander=1),
    path("path-south", 42, [[-90, 1], [-86, -12], [-82, -20]]),
    path("path-north", 43, [[-88, 3], [-84, 14], [-80, 20]]),
    # the stilt hamlet along the causeway
    house("house-a", [[-114, 8], [-106, 15]], "negZ", 31),
    house("house-b", [[-100, 9], [-92, 16]], "negZ", 32, storeys=3),
    house("house-c", [[-114, -16], [-106, -9]], "posZ", 33, storeys=3),
    house("house-d", [[-100, -17], [-92, -10]], "posZ", 34),
    house("house-e", [[-116, 26], [-108, 33]], "posX", 35),
    # willows at the water and the hummocks' outer sides, dark oaks at the back coasts
    kit.TreeProp(id="w1", x=-110, z=-34, style="tree-showcase-r17-1", seed=1),
    kit.TreeProp(id="w2", x=-92, z=-52, style="tree-showcase-r17-3", seed=2),
    kit.TreeProp(id="w3", x=-112, z=52, style="tree-showcase-r17-5", seed=3),
    kit.TreeProp(id="w4", x=-88, z=54, style="tree-showcase-r17-1", seed=4),
    kit.TreeProp(id="w5", x=-62, z=50, style="tree-showcase-r17-3", seed=5),
    kit.TreeProp(id="w6", x=-64, z=-50, style="tree-showcase-r17-5", seed=6),
    kit.TreeProp(id="w7", x=-30, z=50, style="tree-showcase-r17-1", seed=7),
    kit.TreeProp(id="w8", x=-26, z=-52, style="tree-showcase-r17-3", seed=8),
    kit.TreeProp(id="o1", x=-120, z=-52, style="tree-showcase-r5-1", seed=9),
    kit.TreeProp(id="o2", x=-103, z=34, style="tree-showcase-r5-2", seed=10),
    kit.TreeProp(id="o3", x=-92, z=30, style="tree-showcase-r5-1", seed=11),
    kit.TreeProp(id="o4", x=-94, z=-28, style="tree-showcase-r5-2", seed=12),
    kit.BoulderProp(id="b1", x=-58, z=-20, style="rock", seed=13),
    kit.BoulderProp(id="b2", x=-60, z=18, style="rock", seed=14),
    kit.FloraProp(id="fen-cover", seed=71, points=[[-124, -64], [-16, -64], [-16, 64], [-124, 64]],
                  spec=kit.FloraSpec(coverage=0.3, scale=9, octaves=2, fernShare=0.4, flowerShare=0.06,
                                     flowerScale=10, tallShare=0.04, deadBushShare=0.0, cactusShare=0.0)),
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=6),
    themes={"fen": fen, "hummock": hummock, "planks": planks, "post": post},
    mapTheme="fen",
    relief=relief,
    outlines=outlines,
    # The field's two long coasts cut point by point; the frontline and the spawn's seam stay as the plan cut them.
    editShapes={"field-12": [kit.VertexEdit(pulls={
        "0": [[0.06, 3], [0.16, 6], [0.24, 2], [0.36, 4], [0.48, 1], [0.6, 5], [0.7, 2], [0.82, 4], [0.93, 2]],
        "2": [[0.07, 2], [0.18, 4], [0.3, 7], [0.4, 2], [0.52, 3], [0.64, 1], [0.76, 5], [0.86, 2], [0.95, 3]]})]},
    addShapes=shapes,
    addLayers=layers,
    roomStyles={"spawn": kit.library("andesite-gabled-house")},
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
