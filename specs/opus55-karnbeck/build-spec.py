"""Karnbeck — writes opus55-karnbeck.plan.json and .refinement.json.

A wooded beck valley. Each team's core stands in the ruined courtyard of a keep on a bluff at the front of
its half, over a beck that winds across the valley floor below it under a timber footbridge. Behind the
bluff lies a mill hamlet round a mill pond, and oakwood climbs the valley's two sides. The halves meet across
a 32-block build zone over void the whole width of the board.

A core is breached where it stands, so it belongs forward, where it is fought over; the keep's broken ring
gives the defence something to hold, with three gaps in it, and the beck and the bluff make the attacker's
last stretch a climb out of a wet valley floor.

Team 0 is the west half (x < 0); rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-karnbeck"
SURFACE = 16

plan = {
    "plan": 2,
    "meta": {"name": "Karnbeck", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": SURFACE},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-31, -3, 4, 6], "surface": 24},
        {"id": "field", "rect": [-27, -14, 23, 28]},
    ],
    "zones": [{"id": "strait", "rect": [-4, -14, 4, 28]}],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [8, 12], "facing": "right",
                    "footprint": [1, 5, 14, 14]}],
        # field min corner (-108, -56): the core at (-62, 10)
        "cores": [{"id": "core", "piece": "field", "at": [46, 66], "name": "Keep Core"}],
    },
}


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


# Families: the ground green (meadow over dirt over grey rock), the built white and dark (white clay
# between dark-oak timbers; the keep's grey stone), the accent red (brick roofs, the granite and brick of
# the keep's yard).
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
MEADOW = kit.NoiseMaterial(scale=2, seed=4, stops=[kit.CellMaterial(cellSize=2, seed=3, palette=[solid(3), solid(3, 1)]),
                                                   solid(2), solid(2), solid(2)])
SOIL = stack((ROCK, 34), (solid(3), 4), (solid(3), 2), axis="height", from_=-40, follow=100, reach=16, beyond=ROCK)
meadow = finish(stack((stack((MEADOW, 1), (solid(3), 2)), 34),
                      (stack((kit.CellMaterial(cellSize=2, seed=5, palette=[solid(3), solid(3, 1)]), 1), (solid(3), 2)), 14),
                      (kit.CellMaterial(cellSize=2, seed=6, palette=[solid(1), solid(1, 5), solid(1), solid(4)]), 42),
                      axis="slope"),
                wall=SOIL, fill=SOIL)
# The keep's yard: a built floor of four blocks of one tone.
yard = finish(stack((kit.CellMaterial(cellSize=2, seed=7, palette=[solid(98), solid(1, 6), solid(1, 5), solid(1)]), 1),
                    (solid(1), 2)), wall=ROCK, fill=ROCK, depth=2)
KEEP = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(98), solid(98), solid(1, 5), solid(98, 2)], rise=2)
keep = finish(KEEP, KEEP, KEEP, depth=1, rim=KEEP, rim_edges="boundary")
timber = finish(solid(5, 1), solid(5, 1), solid(5, 1), depth=1, rim=solid(5, 1), rim_edges="boundary")

PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(3), solid(3, 1), solid(5, 1)])

relief = {"team": kit.SketchReliefJson(
    base=SURFACE, reach=0, step=1, landform="hills",
    marks=[
        kit.ReliefMarkJson(id="spawn-bench", kind="area", h=24, bevel=3,
                           ring=[[-126, -14], [-106, -14], [-106, 14], [-126, 14]]),
        kit.ReliefMarkJson(id="ramp", kind="line", r=4, points=[[-108, 0], [-94, 2]], h=[24, 19]),
        # the bluff the keep stands on
        kit.ReliefMarkJson(id="bluff", kind="area", h=22, bevel=3),
        # the valley floor the beck runs down, and the far bank rising to the lip
        kit.ReliefMarkJson(id="valley", kind="line", r=7, tread=3,
                           points=[[-38, -56], [-42, -20], [-40, 10], [-44, 56]], h=[12, 12, 12, 12]),
        # the way down the bluff's east face, out through the keep's east gap to the bridge
        kit.ReliefMarkJson(id="bluff-ramp", kind="line", r=3, points=[[-54, 3], [-42, 2]], h=[22, 13]),
        kit.ReliefMarkJson(id="lip", kind="line", r=3, h=[16, 17, 16, 17, 16],
                           points=[[-19, -54], [-20, -26], [-18, 0], [-20, 26], [-19, 54]]),
        # the mill pond's floor behind the bluff
        kit.ReliefMarkJson(id="mill-floor", kind="area", h=15, bevel=3),
    ],
    pushes=[
        # the valley's two sides, centred off the coasts so only their flanks are on the board
        kit.ReliefPushJson(id="north-side", amount=10, falloff=18, roughness=0.4, crown=0, seed=5),
        kit.ReliefPushJson(id="south-side", amount=9, falloff=18, roughness=0.4, crown=0, seed=6),
    ])}

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "bluff": kit.Outline(at=[-64, 8], radius=15, radiusZ=14, points=24, wobble=0.1, lobes=3),
    "mill-floor": kit.Outline(at=[-88, -30], radius=12, radiusZ=9, points=24, wobble=0.12, lobes=3),
    "north-side": kit.Outline(at=[-86, 62], radius=24, radiusZ=10, points=28, wobble=0.15, lobes=4),
    "south-side": kit.Outline(at=[-74, -62], radius=22, radiusZ=9, points=28, wobble=0.15, lobes=4, phase=1),
    "keep-yard": kit.Outline(at=[-62, 10], radius=10.5, radiusZ=10.5, points=32),
    "mill-pond": kit.Outline(at=[-88, -30], radius=8, radiusZ=6, points=20, wobble=0.12, lobes=3),
}


# --- made things ----------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


layers = []
# The keep's broken ring round the core: four courses of stone, three gaps (east, south-west, north-west).
layers += made(props.ring_wall("keep-ring", -62, 10, 12, 1.5, 24, 4, "keep",
                               doors=[(90, 6), (215, 5), (325, 5)]), "keep", seat="ground")
# One standing tower of it, on the ring's north-east, a lookout over the beck.
layers += made(props.drum_tower("keep-tower", -52, 1, 4, 1.5, 19, 12, "keep", merlons=8, parapet=2),
               "keep")
# The footbridge over the beck, a course over the valley floor, left open to the water under it. Stated level
# with the floor (y12) it was carved away with the ground over the water; a course up, it stands.
bridge = props.LayerBuilder("footbridge")
bridge.rect(-50, -2, -32, 3, 13, 1, "timber", keepClear=False)
layers += made(bridge.done(), "footbridge")

# --- patches ---------------------------------------------------------------------------------------------
shapes = [{**kit.SketchShape(id="keep-yard", type="polygon", operation="add", base_height=SURFACE, theme="yard"),
           **kit.ShapeJoin(group="team")}]

# --- dressing ------------------------------------------------------------------------------------------
# The copied trees, each the showcase tree it names, as corpus/tree-showcase/trees.json carries it.
SHOWCASE = json.load(open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")))["trees"]
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "tree-showcase-r12-1": "oak-5", "tree-showcase-r12-2": "oak-6", "tree-showcase-r12-4": "oak-8",
    "tree-showcase-r13-3": "birch-3", "tree-showcase-r13-6": "birch-6"}.items()}
# The tall timber cottage in dark oak over white clay, under a brick roof.
styles["timbered"] = kit.library("talltimber-cottage", kind="house", shell={
    "wall": {"stack": {"bands": [kit.Band(material=kit.LaidLogMaterial(id=162, data=1), thickness=1),
                                 kit.Band(material=solid(159, 0), thickness=4)]}},
    "post": solid(162, 1),
    "roof": {"body": solid(45), "verge": solid(5, 5), "gable": solid(159, 0)}})
styles["rock"] = kit.BoulderStyle(form="round", size=2.2, mossy=True,
                                  rock=kit.CellMaterial(cellSize=2, seed=51, palette=[solid(1), solid(1, 5), solid(4)]))
BANK = kit.CellMaterial(cellSize=2, seed=61, palette=[solid(13), solid(3, 1), solid(4)])


def path(pid, seed, points, radius=1.5, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=radius, claimsGround=True, wander=wander,
                          wanderLength=14, pave=PAVE, points=points)


def house(pid, corners, front, seed, storeys=None):
    return kit.HouseProp(id=pid, style="timbered", seed=seed, front=front, wings=[
        kit.AuthoredWing(corners=corners, **({"spec": kit.WingSpec(storeysHigh=storeys)} if storeys else {}))])


props_ = [
    kit.FluidProp(id="beck", shape="channel", form="stream", layer="ground", radius=3, depth=2, shore=2,
                  shoreWander=True, edge=1.5, bank=BANK,
                  points=[[-38, -58], [-43, -34], [-38, -14], [-41, 0], [-38, 14], [-44, 34], [-42, 58]]),
    kit.FluidProp(id="mill-pond", shape="pool", form="natural", layer="ground", radius=3, depth=3, shore=2,
                  shoreWander=True, edge=1.5, fluid="water", bank=BANK),
    # paths: spawn to the keep, the keep down to the bridge, and a lane past the mill hamlet to the south
    path("path-keep", 41, [[-106, 1], [-94, 2], [-80, 6], [-72, 8]]),
    path("path-bridge", 42, [[-52, 4], [-51, 1]], wander=0),
    path("path-bridge-east", 45, [[-31, 1], [-24, 0], [-19, 0]], wander=1),
    path("path-mill", 43, [[-100, -8], [-94, -18], [-80, -22], [-66, -26], [-50, -24]]),
    # a lane through the north wood to the beck, and on from the far bank to the lip: the way round
    path("path-wood", 46, [[-100, 10], [-90, 22], [-76, 36], [-60, 34], [-50, 28]]),
    path("path-wood-east", 47, [[-34, 30], [-26, 28], [-20, 26]], wander=1),
    # the mill hamlet round the pond
    house("mill", [[-78, -44], [-68, -36]], "negX", 31, storeys=2),
    house("house-a", [[-104, -40], [-96, -33]], "posX", 32),
    house("house-b", [[-102, -26], [-95, -19]], "posX", 33, storeys=2),
    house("house-c", [[-84, 12], [-77, 19]], "negZ", 34),
    # oakwood on the valley sides; birch where the wood thins toward the beck
    kit.TreeProp(id="oak-1", x=-96, z=40, style="tree-showcase-r12-1", seed=1),
    kit.TreeProp(id="oak-2", x=-82, z=46, style="tree-showcase-r12-2", seed=2),
    kit.TreeProp(id="oak-3", x=-68, z=44, style="tree-showcase-r12-4", seed=3),
    kit.TreeProp(id="oak-4", x=-104, z=24, style="tree-showcase-r12-2", seed=4),
    kit.TreeProp(id="birch-1", x=-60, z=27, style="tree-showcase-r13-3", seed=6),
    kit.TreeProp(id="birch-2", x=-52, z=48, style="tree-showcase-r13-6", seed=7),
    kit.TreeProp(id="oak-6", x=-56, z=-46, style="tree-showcase-r12-1", seed=8),
    kit.TreeProp(id="birch-4", x=-30, z=-46, style="tree-showcase-r13-6", seed=10),
    kit.TreeProp(id="birch-5", x=-28, z=42, style="tree-showcase-r13-3", seed=11),
    kit.BoulderProp(id="b1", x=-46, z=-12, style="rock", seed=12),
    kit.BoulderProp(id="b2", x=-34, z=24, style="rock", seed=13),
    kit.BoulderProp(id="b3", x=-74, z=26, style="rock", seed=14),
    kit.FloraProp(id="meadow-cover", seed=71, points=[[-108, -56], [-16, -56], [-16, 56], [-108, 56]],
                  spec=kit.FloraSpec(coverage=0.3, scale=10, octaves=2, fernShare=0.25, flowerShare=0.1,
                                     flowerScale=12, tallShare=0.04, deadBushShare=0.0, cactusShare=0.0)),
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=4),
    themes={"meadow": meadow, "yard": yard, "keep": keep, "timber": timber},
    mapTheme="meadow",
    relief=relief,
    outlines=outlines,
    # The field's two long coasts cut point by point; the frontline and the spawn's seam stay as the plan cut them.
    editShapes={"field-16": [kit.VertexEdit(pulls={
        "0": [[0.08, 2], [0.2, 5], [0.3, 2], [0.45, 3], [0.58, 1], [0.7, 4], [0.84, 2], [0.94, 3]],
        "2": [[0.06, 3], [0.18, 2], [0.3, 5], [0.42, 1], [0.55, 3], [0.68, 2], [0.8, 5], [0.92, 2]]})]},
    addShapes=shapes,
    addLayers=layers,
    roomStyles={"spawn": kit.library("brick-roofed-stone-and-spruce-house")},
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
