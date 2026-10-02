"""Murkwick — writes sonnet55-murkwick.plan.json and .refinement.json for the stage in $STAGE (1..4).

The arrangement is composed board p16 t2 seed 43 (`composed-p16-seed43.plan.json`, pinned off GET /api/compose),
taken whole. Team 0 is the z > 0 half; rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "sonnet55-murkwick"
STAGE = int(os.environ.get("STAGE", "4"))

plan = json.load(open(os.path.join(HERE, "composed-p16-seed43.plan.json")))
plan["meta"] = {"name": "Murkwick", "authors": ["Sonnet 5.5"],
                "notes": "composed p16 t2 seed 43 (walled-4), arrangement unchanged"}
# The refinement's fields as each stage states them; every lobed outline on the board, by the id of what it
# outlines; and the dressing's recipes and placements, in the order they are placed.
finish = {"created": "2026-09-29", "authors": ["Sonnet 5.5"]}
outlines, styles, placed = {}, {}, []

# block ids the board paints with
GRASS, DIRT, HAY = 2, 3, 170
COARSE, PODZOL = (DIRT, 1), (DIRT, 2)
DARKOAK_PLANK, SPRUCE_PLANK = (5, 5), (5, 1)


def solid(block, data=0):
    return kit.SolidMaterial(id=block, data=data)


def stack(*bands, **reading):
    """A layered material: (material, thickness) bands repeating, read along `reading`."""
    return kit.LayeredMaterial(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=material, thickness=thickness) for material, thickness in bands]), **reading)


def theme(surface, wall, fill, depth=3, rim=None, rim_edges="void"):
    return kit.TerrainTheme(bedrock=kit.BedrockSpec(relative=False, value=1), rimEdges=rim_edges,
                            rim=kit.TopBand(enabled=rim is not None, depth=1, material=rim or solid(1)),
                            wallEnabled=True, wallOnTerrainFaces=True, wall=wall, fill=fill,
                            surface=kit.TopBand(enabled=True, depth=depth, material=surface))


# The rock under the board: stone and andesite, cobblestone at a quarter.
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
# The mud the water is banked in once the ground is painted, and the mudflat's top.
MUD = kit.CellMaterial(cellSize=2, seed=41, palette=[solid(DIRT), solid(DIRT), solid(*PODZOL), solid(*COARSE)])


def pool(pid, depth, shelf, shore):
    """Standing water over the outline stated under its id, banked in mud from stage 3."""
    return kit.FluidProp(id=pid, shape="pool", form="natural", layer="ground", radius=shelf, depth=depth, shore=shore,
                         shoreWander=True, edge=1.5, fluid="water", **({"bank": MUD} if STAGE >= 3 else {}))


def path(pid, seed, points, pave, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=1.5, claimsGround=True, wander=wander,
                          wanderLength=14, pave=pave, points=points)


def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


# --- stage 2: the outer coasts reshaped point by point, the relief, the water. No theme. -------------------------------
VARIANT = os.environ.get("RELIEF", "d")


def area(mark_id, height, ring):
    """A level area mark: `height` held to the ring's own outline."""
    return kit.ReliefMarkJson(id=mark_id, kind="area", h=height, bevel=0, ring=ring)


def relief(variant):
    """The team's relief in one of the four sketches, and the outlines its pushes are drawn on."""
    spur_a = area("spur-a", 9, [[-50, 64], [-26, 64], [-26, 84], [-50, 84]])
    spur_b = area("spur-b", 9, [[26, 56], [50, 56], [50, 76], [26, 76]])
    front = area("front", 9, [[-24, 22], [24, 22], [24, 44], [-24, 44]])
    mid = area("mid", 9, [[-17, -13], [17, -13], [17, 13], [-17, 13]])
    if variant == "a":      # a flat swamp: the hub two over the frontline and nothing else
        marks = [front, mid, spur_a, spur_b,
                 area("hub", 11, [[-21, 52], [21, 52], [21, 98], [-21, 98]]),
                 area("spawn", 11, [[-6, 98], [14, 98], [14, 110], [-6, 110]])]
        pushes, drawn = [], {}
    elif variant == "b":    # the hub a village island three over the wet flat, grading up across the front bar
        marks = [front, mid, spur_a, spur_b,
                 area("hub", 12, [[-21, 52], [21, 52], [21, 98], [-21, 98]]),
                 area("spawn", 12, [[-6, 98], [14, 98], [14, 110], [-6, 110]])]
        pushes = [
            kit.ReliefPushJson(id="hummock-w", amount=2, falloff=5, crown=0, seed=4),
            kit.ReliefPushJson(id="hummock-e", amount=2, falloff=5, crown=0, seed=5),
        ]
        drawn = {
            "hummock-w": kit.Outline(at=[-19, 29], radius=4, radiusZ=3, points=12, wobble=0.1, lobes=3),
            "hummock-e": kit.Outline(at=[19, 30], radius=4, radiusZ=3, points=12, wobble=0.1, lobes=3),
        }
    elif variant == "d":    # b with the hub's bars carrying low hammocks, so the island is not a table
        marks = [front, mid, spur_a, spur_b,
                 area("hub", 12, [[-21, 52], [21, 52], [21, 98], [-21, 98]]),
                 area("spawn", 12, [[-6, 98], [14, 98], [14, 110], [-6, 110]])]
        pushes = [
            kit.ReliefPushJson(id="hummock-w", amount=2, falloff=5, crown=0, seed=4),
            kit.ReliefPushJson(id="hummock-e", amount=2, falloff=5, crown=0, seed=5),
            kit.ReliefPushJson(id="ham-1", amount=3, falloff=6, crown=0, seed=6),
            kit.ReliefPushJson(id="ham-2", amount=3, falloff=5, crown=0, seed=7),
            kit.ReliefPushJson(id="ham-3", amount=2, falloff=5, crown=0, seed=8),
            kit.ReliefPushJson(id="ham-4", amount=2, falloff=5, crown=0, seed=9),
            kit.ReliefPushJson(id="ham-5", amount=2, falloff=4, crown=0, seed=10),
        ]
        drawn = {
            "hummock-w": kit.Outline(at=[-19, 29], radius=4, radiusZ=3, points=12, wobble=0.1, lobes=3),
            "hummock-e": kit.Outline(at=[19, 30], radius=4, radiusZ=3, points=12, wobble=0.1, lobes=3),
            "ham-1": kit.Outline(at=[15, 57], radius=5, radiusZ=4, points=14, wobble=0.12, lobes=3),
            "ham-2": kit.Outline(at=[17, 88], radius=4, radiusZ=4, points=14, wobble=0.12, lobes=3),
            "ham-3": kit.Outline(at=[-16, 72], radius=4, radiusZ=5, points=14, wobble=0.12, lobes=3),
            "ham-4": kit.Outline(at=[17, 74], radius=3, radiusZ=4, points=14, wobble=0.12, lobes=3),
            "ham-5": kit.Outline(at=[-14, 60], radius=3, radiusZ=3, points=14, wobble=0.12, lobes=3),
        }
    else:                   # a sunken bog: the hub at 10 with its bars' middles hollowed to basins, rims left standing
        marks = [front, mid, spur_a, spur_b,
                 area("hub", 10, [[-21, 52], [21, 52], [21, 98], [-21, 98]]),
                 area("spawn", 10, [[-6, 98], [14, 98], [14, 110], [-6, 110]])]
        pushes = [
            kit.ReliefPushJson(id="basin-f", amount=-3, falloff=5, crown=0, seed=4),
            kit.ReliefPushJson(id="basin-b", amount=-3, falloff=5, crown=0, seed=5),
        ]
        drawn = {
            "basin-f": kit.Outline(at=[-6, 56], radius=10, radiusZ=4, points=14, wobble=0.1, lobes=3),
            "basin-b": kit.Outline(at=[8, 88], radius=10, radiusZ=4, points=14, wobble=0.1, lobes=3),
        }
    team = kit.SketchReliefJson(base=9, reach=0, step=1, landform="plain", marks=marks, pushes=pushes)
    return {"team": team}, drawn


if STAGE >= 2:
    finish["relief"], drawn = relief(VARIANT)
    outlines.update(drawn)
    # The team-0 ground's outer coasts, each edge named by the vertex it leaves on the ring the plan compiles that
    # ground to, from (-48, 68) round by (-24, 68). Its wall seams (x -29..-27 and 27..29), the wool rooms' faces and
    # the frontline's face to the band stay exactly as the composer cut them.
    finish["editShapes"] = {"frontline-t1-9": [kit.VertexEdit(pulls={
        "0": [[0.58, 2]],
        "1": [[0.15, 3], [0.35, 5], [0.55, 2], [0.75, 4], [0.90, 1]],
        "11": [[0.12, 2], [0.30, 5], [0.50, 2], [0.70, 4], [0.88, 1]],
        "12": [[0.42, 2]],
        "14": [[0.58, 2]],
        "15": [[0.20, 3], [0.50, 5], [0.80, 2]],
        "16": [[0.5, 2]],
        "20": [[0.3, 3], [0.7, 2]],
        "21": [[0.25, 4], [0.60, 2]],
        "22": [[0.42, 2]],
    })]}
    placed += [pool("pond-front", depth=2, shelf=2, shore=1), pool("pond-back", depth=2, shelf=2, shore=1)]
    outlines.update({
        "pond-front": kit.Outline(at=[-4, 56], radius=8, radiusZ=3.5, points=14, wobble=0.1, lobes=3),
        "pond-back": kit.Outline(at=[-12, 88], radius=7, radiusZ=3.5, points=14, wobble=0.1, lobes=3),
    })

# --- stage 3: made things on layers, the biome, the themes finished by angle, patches, room styles --------------------
# Three families, named before any theme: the GROUND is olive and brown — swamp-tinted turf with podzol and coarse
# dirt, which Swampland's tint meets rather than fights; what is BUILT is dark timber, dark oak and spruce; the ACCENT
# is thatch, hay bale, on every roof and on the mid stone's platform.
if STAGE >= 3:
    PODSET = kit.CellMaterial(cellSize=2, seed=3, palette=[solid(*PODZOL), solid(*COARSE), solid(*PODZOL)])
    TURF = kit.NoiseMaterial(scale=2, seed=17, stops=[
        PODSET, solid(GRASS), solid(GRASS), solid(GRASS),
        kit.CellMaterial(cellSize=2, seed=4, palette=[solid(*COARSE), solid(DIRT)])])
    SOIL = kit.CellMaterial(cellSize=2, seed=5, palette=[solid(DIRT), solid(*COARSE)])
    EARTH = kit.CellMaterial(cellSize=2, seed=6, palette=[solid(*PODZOL), solid(*COARSE), solid(DIRT)])
    SOILR = kit.CellMaterial(cellSize=2, seed=5, palette=[solid(*COARSE), solid(DIRT)], rise=2)
    STRATA = [(SOILR, 3), (ROCK, 5), (SOILR, 1), (ROCK, 4)] * 9
    BEDS = stack(*STRATA, axis="height", from_=-40, follow=100, reach=16, beyond=ROCK)
    bog = theme(stack((stack((TURF, 1), (SOIL, 2)), 40), (stack((EARTH, 1), (SOIL, 2)), 14), (ROCK, 36), axis="slope"),
                wall=BEDS, fill=BEDS)
    mud = theme(stack((MUD, 1), (solid(DIRT), 2)), wall=ROCK, fill=ROCK)
    PEAT = kit.CellMaterial(cellSize=2, seed=43, palette=[solid(*PODZOL), solid(*PODZOL), solid(*COARSE), solid(DIRT)])
    peat = theme(stack((PEAT, 1), (solid(DIRT), 2)), wall=ROCK, fill=ROCK)
    TIMBER = kit.CellMaterial(cellSize=2, seed=22, rise=2, palette=[
        solid(*DARKOAK_PLANK), solid(*SPRUCE_PLANK), solid(*DARKOAK_PLANK), solid(*DARKOAK_PLANK)])
    timber = theme(TIMBER, TIMBER, TIMBER, depth=1, rim=TIMBER, rim_edges="boundary")
    THATCH = kit.CellMaterial(cellSize=2, seed=23, palette=[solid(HAY), solid(HAY)], rise=2)
    thatch = theme(THATCH, THATCH, THATCH, depth=1, rim=THATCH, rim_edges="boundary")
    finish["biome"] = kit.SolidBiome(id=6)
    finish["themes"] = {"bog": bog, "mud": mud, "peat": peat, "timber": timber, "thatch": thatch}
    finish["mapTheme"] = "bog"
    # Patches of different ground on the team's ground, each at the height of the ground it lies on.
    finish["addShapes"] = [
        {**kit.SketchShape(id="mudflat", type="polygon", operation="add", base_height=9, theme="mud",
                           vertices=[[-14, 34], [10, 34], [12, 42], [-16, 44]]), **kit.ShapeJoin(group="team")},
        {**kit.SketchShape(id="peat-1", type="polygon", operation="add", base_height=9, theme="peat"),
         **kit.ShapeJoin(group="team")},
        {**kit.SketchShape(id="peat-2", type="polygon", operation="add", base_height=9, theme="peat"),
         **kit.ShapeJoin(group="team")},
        {**kit.SketchShape(id="peat-3", type="polygon", operation="add", base_height=9, theme="peat"),
         **kit.ShapeJoin(group="team")},
    ]
    outlines.update({
        "peat-1": kit.Outline(at=[15, 57], radius=4, radiusZ=3.2, points=14, wobble=0.12, lobes=3),
        "peat-2": kit.Outline(at=[17, 88], radius=3.4, radiusZ=3.2, points=14, wobble=0.12, lobes=3),
        "peat-3": kit.Outline(at=[-16, 72], radius=3.2, radiusZ=4, points=14, wobble=0.12, lobes=3),
    })

    layers = []
    # The mid stone's platform: one for the board, so off the mirror. Four corner posts and a deck on stilts three
    # over the stone, a hay roof on four posts over it, and a stair of three steps up the east side.
    hut = props.LayerBuilder("hut-deck", name="Stilt platform deck", mirrors=False)
    hut.rect(-7, -4, 5, 4, 12, 1, "timber")
    layers += made(hut.done(), "stilt-platform")
    legs = props.LayerBuilder("hut-legs", name="Stilt platform legs", mirrors=False)
    for x, z in [(-7, -4), (4, -4), (-7, 3), (4, 3)]:
        legs.rect(x, z, x + 1, z + 1, 9, 3, "timber")
    for h, x in zip((3, 2, 1), (5, 6, 7)):
        legs.rect(x, -1, x + 1, 1, 9, h, "timber")
    layers += made(legs.done(), "stilt-platform")
    posts = props.LayerBuilder("hut-posts", name="Roof posts", mirrors=False)
    for x, z in [(-7, -4), (4, -4), (-7, 3), (4, 3)]:
        posts.rect(x, z, x + 1, z + 1, 13, 4, "timber")
    layers += made(posts.done(), "stilt-platform")
    roof = props.spire("hut-roof", -1, 0, 8.5, 17, 4, "thatch", sides=4, mirrors=False, name="Thatch roof")
    layers += made(roof, "stilt-platform")
    # Two planked walks over the ponds, a course over the ground beside the water, and off the kept-clear rule.
    walk = props.LayerBuilder("pond-walk", name="Pond walks")
    walk.rect(-6, 50, -3, 62, 12, 1, "timber", keepClear=False)
    walk.rect(-13, 87, -3, 89, 12, 1, "timber", keepClear=False)
    layers += made(walk.done(), "pond-walk")
    finish["addLayers"] = layers

    # The spawn's hall is the showcase hall under hay thatch; the wool rooms' is the 17h hall in spruce under hay.
    finish["roomStyles"] = {"spawn": kit.library("hay-roofed-stone-and-dark-oak-house"), "wool": kit.library("hay-roofed-stone-and-spruce-house")}

# --- stage 4: dressing — the roads first, then ground cover, then trees, rocks and cabins -------------------------------
if STAGE >= 4:
    PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[
        solid(*SPRUCE_PLANK), solid(*DARKOAK_PLANK), solid(*SPRUCE_PLANK), solid(*COARSE)])
    placed += [
        # the spawn door down the hub's east side to the front bar, and on to the frontline
        path("road-main", 61, [[5, 98], [8, 92], [15, 86], [18, 78], [16, 68], [12, 58], [8, 50], [6, 46]], PAVE),
        # the front bar's edge west, then north up the hub's west side to the first wool's neck
        path("road-a", 62, [[8, 50], [-4, 49.5], [-14, 50], [-19, 56], [-19, 66], [-21, 73], [-25, 74]], PAVE),
        # and east to the second wool's neck
        path("road-b", 63, [[14, 54], [20, 61], [23, 66], [26, 66]], PAVE, wander=1),
        kit.FloraProp(id="reed-cover", seed=5,
                      points=[[-48, 68], [-24, 68], [-24, 32], [-4, 24], [20, 24], [24, 32], [24, 60], [48, 60],
                              [48, 72], [24, 72], [24, 96], [12, 96], [12, 108], [-4, 108], [-4, 96], [-24, 96],
                              [-24, 80], [-48, 80]],
                      spec=kit.FloraSpec(coverage=0.35, scale=8, octaves=2, fernShare=0.3, flowerShare=0.02,
                                         flowerScale=10, tallShare=0.03, deadBushShare=0.0, cactusShare=0.0)),
    ]

    # Cover on the frontline: hay stacks two and three courses tall, off the road and off the hummocks — a box a
    # player crouches behind, which is what a capture board wants small cover to be.
    stacks = props.LayerBuilder("hay-stacks", name="Hay stacks")
    for x0, z0, x1, z1, h in [(-16, 27, -12, 29, 2), (-9, 34, -6, 36, 2), (10, 27, 13, 29, 3), (15, 35, 18, 37, 2),
                              (-20, 43, -17, 45, 2)]:
        stacks.rect(x0, z0, x1, z1, 9, h, "thatch")
    finish["addLayers"] += made(stacks.done(), "hay-stacks", seat="ground")

    # Two species and no third: willows (row r17) on the ring and the back bar, and under them a small oak (row r6),
    # each the showcase tree it names, as the studio's tree library carries it.
    WILLOW = [f"tree-showcase-r17-{i}" for i in range(1, 6)]
    OAK = [f"tree-showcase-r6-{i}" for i in (1, 4, 6)]
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from showcase import trees as studio_trees
    SHOWCASE = studio_trees()
    styles.update({key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
        "tree-showcase-r17-1": "willow-1", "tree-showcase-r17-2": "willow-2", "tree-showcase-r17-3": "willow-3",
        "tree-showcase-r17-4": "willow-4", "tree-showcase-r17-5": "willow-5", "tree-showcase-r6-1": "tiny-oak-1",
        "tree-showcase-r6-4": "tiny-oak-4", "tree-showcase-r6-6": "tiny-oak-6"}.items()})
    # The marsh: the frontline's middle drowned a course deep, so the contested ground is waded and the hay stacks stand
    # in it as dry hummocks. Water on ground pinned level, so it digs no trench.
    placed += [pool("marsh", depth=1, shelf=1, shore=1)]
    outlines["marsh"] = kit.Outline(at=[-2, 39], radius=12, radiusZ=5, points=18, wobble=0.15, lobes=3)
    placed += [
        kit.TreeProp(id="w-2", x=-13, z=68, style=WILLOW[2], seed=2),
        kit.TreeProp(id="w-3", x=10, z=74, style=WILLOW[1], seed=3),
        kit.TreeProp(id="w-4", x=19, z=92, style=WILLOW[3], seed=4),
        kit.TreeProp(id="w-5", x=-17, z=44, style=WILLOW[4], seed=5),
        kit.TreeProp(id="o-1", x=6, z=61, style=OAK[0], seed=6),
        kit.TreeProp(id="o-2", x=-6, z=81, style=OAK[1], seed=7),
    ]

if outlines:
    finish["outlines"] = outlines
if STAGE >= 2:
    finish["dressing"] = kit.DressingDoc(styles=styles, props=placed)
refinement = kit.Refinement(**finish)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG, "stage", STAGE)
