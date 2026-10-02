"""Tanglecleft — writes sonnet55-tanglecleft.plan.json and .refinement.json for the stage in $STAGE (1..4)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "sonnet55-tanglecleft"
STAGE = int(os.environ.get("STAGE", "4"))

# --- the plan: arrangement only. Team 0 is the x < 0 half; rot_180 fans the rest. --------------------------------
HZ = int(os.environ.get("HZ", "10"))          # half the field's depth, in cells
BW = int(os.environ.get("BW", "3"))           # half the build band's width, cells
FW = int(os.environ.get("FW", "22"))          # the field's length, cells
MXA = int(os.environ.get("MXA", "-64"))       # the monument's x, blocks
MZ = int(os.environ.get("MZ", "24"))          # its z, blocks (team 0 is the +z side of the axis)
plan = {
    "plan": 2,
    "meta": {"name": "Tanglecleft", "authors": ["Sonnet 5.5"],
             "notes": "jungle: a monument on a temple shelf above a river dell"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 20, "surface": 12},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-(BW + FW + 5), -3, 5, 6]},
        {"id": "field", "rect": [-(BW + FW), -HZ, FW, 2 * HZ]},
    ],
    "zones": [{"id": "band", "rect": [-BW, -HZ, 2 * BW, 2 * HZ]}],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [8, 12], "facing": "right", "footprint": [1, 5, 14, 14]}],
        "destroyables": [{"id": "stone", "piece": "field", "at": [MXA + 4 * (BW + FW), 4 * HZ + MZ], "style": "pillar-3",
                          "name": "Ixcal Stone"}],
    },
    "walls": [],
}
# The refinement's fields as each stage states them; every lobed outline on the board, by the id of what it
# outlines; and the dressing's recipes and placements, in the order they are placed.
finish = {"created": "2026-09-29", "authors": ["Sonnet 5.5"]}
outlines, styles, placed = {}, {}, []

# block ids the board paints with
GRASS, DIRT, STONE, COBBLE, GRAVEL, CLAY, BRICKS = 2, 3, 1, 4, 13, 82, 98
COARSE, PODZOL = (DIRT, 1), (DIRT, 2)
ANDESITE, POL_ANDESITE = (STONE, 5), (STONE, 6)
JUNGLE_PLANK, SPRUCE_PLANK = (5, 3), (5, 1)


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


def path(pid, seed, points, pave, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=1.5, claimsGround=True, wander=wander,
                          wanderLength=14, pave=pave, points=points)


def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


# The rock under the board: stone and andesite, cobblestone at a quarter.
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
# The gravel and clay the water's bed and beach are laid with, from stage 4.
BANK = kit.CellMaterial(cellSize=2, seed=9, palette=[solid(GRAVEL), solid(*COARSE), solid(CLAY), solid(GRAVEL)])
BANKED = {"bank": BANK} if STAGE >= 4 else {}

# --- stage 2: the outline reshaped point by point, the relief, the water. No theme. ---------------------------------
VARIANT = os.environ.get("RELIEF", "d")

BENCH = kit.ReliefMarkJson(id="bench", kind="area", h=21, bevel=0,
                           ring=[[-122, -15], [-97, -15], [-97, 15], [-122, 15]])
FRONT = kit.ReliefMarkJson(id="front", kind="area", h=11, bevel=0,
                           ring=[[-26, -38], [-12, -38], [-12, 38], [-26, 38]])
SHELF = kit.ReliefMarkJson(id="shelf", kind="area", h=18, bevel=3)
DELL = kit.ReliefMarkJson(id="dell", kind="area", h=8, bevel=2,
                          ring=[[-66, -15], [-33, -15], [-33, -1], [-66, -1]])


def relief(variant):
    """The team's relief in one of the four sketches, and the outlines its shelf and pushes are drawn on."""
    drawn = {"shelf": kit.Outline(at=[-64, 24], radius=12, radiusZ=11, points=20, wobble=0.08, lobes=3)}
    if variant == "a":      # a dell along the temple's foot, a hill on the north edge, hummocks in the south wood
        marks = [BENCH, FRONT, SHELF, DELL]
        pushes = [
            kit.ReliefPushJson(id="hill", amount=12, falloff=14, crown=8, seed=5),
            kit.ReliefPushJson(id="hum-1", amount=5, falloff=9, crown=0, seed=7),
            kit.ReliefPushJson(id="hum-2", amount=6, falloff=9, crown=0, seed=8),
            kit.ReliefPushJson(id="hum-3", amount=6, falloff=10, crown=0, seed=9),
        ]
        drawn.update({
            "hill": kit.Outline(at=[-36, 40], radius=14, radiusZ=12, points=20, wobble=0.1, lobes=3),
            "hum-1": kit.Outline(at=[-80, -22], radius=9, radiusZ=7, points=16, wobble=0.12, lobes=3),
            "hum-2": kit.Outline(at=[-52, -29], radius=10, radiusZ=7, points=16, wobble=0.12, lobes=3, phase=1.0),
            "hum-3": kit.Outline(at=[-76, -38], radius=12, radiusZ=5, points=16, wobble=0.1, lobes=3),
        })
    elif variant == "d":    # the dell and hill of a, plus a dry cleft running from the south coast to the dell's foot
        marks = [BENCH, FRONT, SHELF, DELL]
        pushes = [
            kit.ReliefPushJson(id="cleft", ring=[[-44, -42], [-37, -42], [-37, -27], [-44, -27]], amount=-6, falloff=9,
                               crown=0, seed=3),
            kit.ReliefPushJson(id="hill", amount=12, falloff=14, crown=8, seed=5),
            kit.ReliefPushJson(id="hum-1", amount=5, falloff=9, crown=0, seed=7),
            kit.ReliefPushJson(id="hum-2", amount=4, falloff=7, crown=0, seed=8),
            kit.ReliefPushJson(id="hum-3", amount=6, falloff=10, crown=0, seed=9),
        ]
        drawn.update({
            "hill": kit.Outline(at=[-36, 40], radius=14, radiusZ=12, points=20, wobble=0.1, lobes=3),
            "hum-1": kit.Outline(at=[-82, -24], radius=9, radiusZ=7, points=16, wobble=0.12, lobes=3),
            "hum-2": kit.Outline(at=[-24, -30], radius=6, radiusZ=6, points=16, wobble=0.12, lobes=3, phase=1.0),
            "hum-3": kit.Outline(at=[-74, -38], radius=12, radiusZ=5, points=16, wobble=0.1, lobes=3),
        })
    elif variant == "b":    # a ravine across the field, north to south, with a land bridge under the north hill
        marks = [BENCH, FRONT, SHELF]
        pushes = [
            kit.ReliefPushJson(id="cleft", ring=[[-44, -40], [-37, -40], [-37, 6], [-44, 6]], amount=-8, falloff=12,
                               crown=0, seed=3),
            kit.ReliefPushJson(id="hill", amount=12, falloff=12, crown=8, seed=5),
            kit.ReliefPushJson(id="hum-1", amount=5, falloff=9, crown=0, seed=7),
            kit.ReliefPushJson(id="hum-2", amount=5, falloff=9, crown=0, seed=8),
        ]
        drawn.update({
            "hill": kit.Outline(at=[-30, 41], radius=13, radiusZ=12, points=20, wobble=0.1, lobes=3),
            "hum-1": kit.Outline(at=[-84, -18], radius=9, radiusZ=7, points=16, wobble=0.12, lobes=3),
            "hum-2": kit.Outline(at=[-72, 4], radius=9, radiusZ=7, points=16, wobble=0.12, lobes=3, phase=1.0),
        })
    else:                   # rolling: two long spurs along the lane and no cut at all
        marks = [BENCH, FRONT, SHELF]
        pushes = [
            kit.ReliefPushJson(id="spur-s", ring=[[-90, -40], [-40, -40], [-40, -30], [-90, -30]], amount=9, falloff=12,
                               crown=5, seed=5),
            kit.ReliefPushJson(id="spur-n", ring=[[-84, 38], [-30, 38], [-30, 46], [-84, 46]], amount=9, falloff=12,
                               crown=5, seed=6),
            kit.ReliefPushJson(id="knoll", amount=4, falloff=9, crown=0, seed=7),
        ]
        drawn["knoll"] = kit.Outline(at=[-48, -8], radius=10, radiusZ=8, points=16, wobble=0.12, lobes=3)
    team = kit.SketchReliefJson(base=12, reach=0, step=1, landform="hills", marks=marks, pushes=pushes)
    return {"team": team}, drawn


if STAGE >= 2:
    finish["relief"], drawn = relief(VARIANT)
    outlines.update(drawn)
    # Each edge is named by the vertex it leaves on the ring the plan compiles the team-0 ground to (spawn bench and
    # field fused), from (-120, -12) round by (-100, -12): edge 2 is the south coast, 4 the north coast, 1 and 5 the
    # field's west edges beside the spawn. Edge 3 is the frontline and stays as cut.
    finish["editShapes"] = {"field-12": [kit.VertexEdit(pulls={
        "1": [[0.35, 3], [0.7, 6]],
        "2": [[0.10, 1], [0.22, 4], [0.34, 2], [0.47, 5], [0.60, 1], [0.72, 4], [0.86, 2]],
        "4": [[0.12, 2], [0.25, 5], [0.40, 2], [0.55, 4], [0.70, 1], [0.85, 4]],
        "5": [[0.30, 5], [0.65, 2]],
    })]}
    if VARIANT in ("a", "d"):
        placed += [
            kit.FluidProp(id="brook", shape="channel", form="stream", layer="ground", radius=2.5, depth=2, shore=0,
                          shoreWander=True, edge=1.5, points=[[-34, -8], [-42, -8], [-48, -8]], **BANKED),
            # The lagoon's shore: twelve points round (-54, -8), 6 by 4 with three lobes of 0.05. They are stated as
            # points because three of them stand on a twentieth of a block, where an outline of those numbers
            # rounds the other way.
            kit.FluidProp(id="lagoon", shape="pool", form="natural", layer="ground", radius=2, depth=2, shore=0,
                          shoreWander=True, edge=1.5, fluid="water", **BANKED,
                          points=[[-47.7, -8.0], [-48.8, -6.0], [-51.1, -4.7], [-54.0, -4.0], [-57.1, -4.4],
                                  [-59.2, -6.0], [-59.7, -8.0], [-59.2, -10.0], [-57.2, -11.6], [-54.0, -12.0],
                                  [-51.1, -11.3], [-48.8, -10.0]]),
        ]


# --- stage 3: made things on layers, the biome, the themes finished by angle, patches, room styles --------------------
# Three families, named before any theme: the GROUND is green — turf over dirt and coarse dirt, rock where it is
# too steep for either; what is BUILT is pale grey stone brick with a faint mossy vein; the ACCENT is jungle wood,
# which the bridge, the trails and the spawn's timbers all share.
if STAGE >= 3:
    TURF = kit.NoiseMaterial(scale=2, seed=11, stops=[
        kit.CellMaterial(cellSize=2, seed=7, palette=[solid(DIRT), solid(*COARSE)]),
        solid(GRASS), solid(GRASS), solid(GRASS), solid(GRASS)])
    SOIL = kit.CellMaterial(cellSize=2, seed=5, palette=[solid(DIRT), solid(*COARSE)])
    EARTH = kit.CellMaterial(cellSize=2, seed=6, palette=[solid(DIRT), solid(*COARSE), solid(DIRT), solid(*PODZOL)])
    SOILR = kit.CellMaterial(cellSize=2, seed=5, palette=[solid(DIRT), solid(*COARSE)], rise=2)
    GREY = kit.CellMaterial(cellSize=2, seed=3, palette=[solid(*ANDESITE), solid(STONE)], rise=2)
    STRATA = [(SOILR, 2), (ROCK, 5), (GREY, 2), (ROCK, 4)] * 9
    BEDS = stack(*STRATA, axis="height", from_=-40, follow=100, reach=16, beyond=ROCK)
    jungle = theme(
        stack((stack((TURF, 1), (SOIL, 2)), 44), (stack((EARTH, 1), (SOIL, 2)), 8), (ROCK, 38), axis="slope"),
        wall=BEDS, fill=BEDS)
    BRICK4 = kit.CellMaterial(cellSize=2, seed=21, rise=2, palette=[
        solid(BRICKS), solid(BRICKS), solid(*POL_ANDESITE), solid(*ANDESITE), solid(BRICKS), solid(BRICKS, 1)])
    temple = theme(BRICK4, BRICK4, BRICK4, depth=1, rim=BRICK4, rim_edges="boundary")
    TIMBER = kit.CellMaterial(cellSize=2, seed=22, rise=2, palette=[
        solid(*JUNGLE_PLANK), solid(*JUNGLE_PLANK), solid(*SPRUCE_PLANK)])
    timber = theme(TIMBER, TIMBER, TIMBER, depth=1, rim=TIMBER, rim_edges="boundary")
    BED = kit.CellMaterial(cellSize=2, seed=31, palette=[
        solid(GRAVEL), solid(*ANDESITE), solid(*COARSE), solid(GRAVEL)])
    bed = theme(BED, wall=ROCK, fill=ROCK, depth=2)
    finish["biome"] = kit.SolidBiome(id=21)
    finish["themes"] = {"jungle": jungle, "temple": temple, "timber": timber, "bed": bed}
    finish["mapTheme"] = "jungle"
    # The cleft's floor: a patch of different ground at the height of the ground it lies on.
    finish["addShapes"] = [
        {**kit.SketchShape(id="cleft-bed", type="polygon", operation="add", base_height=12, theme="bed",
                           vertices=[[-46, -36], [-36.5, -36], [-36.5, -27], [-46, -27]]), **kit.ShapeJoin(group="team")}]

    layers = []
    # The temple: a three-tier ziggurat on the plateau behind the monument, and a line of broken pillars between
    # it and the stone, so the way to the monument is through a colonnade and not over a hill.
    layers += made(props.ziggurat("temple-zigg", -86, 26, 9, 18, 3, 2, 2, "temple", name="Temple ziggurat"),
                   "temple")
    # A stair up the ziggurat's east face, three wide, one course a step: the temple is climbed, not scrambled onto.
    stair = props.LayerBuilder("temple-stair", name="Temple stair")
    stair.rect(-77, 25, -75, 28, 18, 1, "temple")
    stair.rect(-79, 25, -77, 28, 20, 1, "temple")
    stair.rect(-81, 25, -79, 28, 22, 1, "temple")
    layers += made(stair.done(), "temple")
    pil = props.LayerBuilder("temple-pillars", name="Broken pillars")
    for x, z, h in [(-74, 17, 7), (-74, 22, 4), (-74, 30, 6), (-74, 35, 3)]:
        pil.disc(x, z, 1.2, 18, h, "temple")
    layers += made(pil.done(), "temple")
    lip = props.LayerBuilder("temple-lip", name="Terrace lip")
    for x0, x1, top in [(-93, -84, 23), (-80, -72, 21), (-68, -61, 21)]:
        lip.rect(x0, 15, x1, 16.5, 16, top - 16, "temple")
    layers += made(lip.done(), "temple")
    # The rope bridge over the dry cleft: a plank deck and posts, timber, on ground that stands at 10 on the west
    # rim and 12 on the east.
    br = props.LayerBuilder("cleft-bridge", name="Cleft bridge")
    br.rect(-56, -36, -32, -33, 10, 1, "timber")
    rails = props.LayerBuilder("cleft-rails", name="Bridge posts")
    for x in (-54, -48, -42, -36):
        rails.rect(x, -36, x + 1, -35, 11, 3, "timber")
        rails.rect(x, -34, x + 1, -33, 11, 3, "timber")
    layers += made(rails.done(), "cleft-bridge")
    layers += made(br.done(), "cleft-bridge")
    finish["addLayers"] = layers

    # The spawn's hall is the tall timber hall in jungle wood, its logs, beam ends and spruce planks all jungle.
    finish["roomStyles"] = {"spawn": kit.library("talltimber-hall-jungle"), "wool": kit.library("andesite-gabled-house")}

# --- stage 4: dressing — paths first (the circulation), then ground cover, then trees, rocks and a cabin ---------------
if STAGE >= 4:
    PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[
        solid(DIRT), solid(*COARSE), solid(*JUNGLE_PLANK), solid(*COARSE)])
    placed += [
        # spawn door to the monument, through the second gap in the terrace lip
        path("path-spawn", 51, [[-99, 1], [-90, 5], [-80, 9], [-70, 12], [-70, 17], [-69, 21]], PAVE, wander=1),
        # spawn door through the south wood to the cleft bridge, and on from its east end to the front
        path("path-south-w", 52, [[-99, -2], [-93, -10], [-84, -20], [-74, -28], [-64, -32], [-58, -33]], PAVE),
        path("path-south-e", 53, [[-31, -33], [-26, -28], [-20, -20], [-16, -14]], PAVE, wander=1),
        # the band's way up to the terrace, south of the hill and north of the dell
        path("path-front", 54, [[-16, 8], [-26, 11], [-38, 13], [-50, 15], [-60, 16]], PAVE),
        kit.FloraProp(id="floor-cover", seed=5,
                      points=[[-120, -12], [-100, -12], [-100, -40], [-12, -40], [-12, 40], [-100, 40], [-100, 12],
                              [-120, 12]],
                      spec=kit.FloraSpec(coverage=0.3, scale=9, octaves=2, fernShare=0.5, flowerShare=0.04,
                                         flowerScale=10, tallShare=0.03, deadBushShare=0.0, cactusShare=0.0)),
    ]

    # Two species, and never three: jungle giants (library row r16) and, under them, dark oak (row r5), each the
    # showcase tree it names, as the studio's tree library carries it. Every site stands where the seats mask
    # leaves room once the paths are in, and each at least its crown and its neighbour's apart.
    JUNGLE = [f"tree-showcase-r16-{i}" for i in range(1, 7)]
    OAK = [f"tree-showcase-r5-{i}" for i in (1, 2, 3)]
    from showcase import trees as studio_trees
    SHOWCASE = studio_trees()
    styles.update({key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
        "tree-showcase-r16-1": "jungle-1", "tree-showcase-r16-2": "jungle-2", "tree-showcase-r16-3": "jungle-3",
        "tree-showcase-r16-4": "jungle-4", "tree-showcase-r16-5": "jungle-5", "tree-showcase-r16-6": "jungle-6",
        "tree-showcase-r5-1": "dark-oak-1", "tree-showcase-r5-2": "dark-oak-2",
        "tree-showcase-r5-3": "dark-oak-3"}.items()})
    styles["rock"] = kit.BoulderStyle(form="outcrop", size=3, mossy=False, rock=kit.CellMaterial(
        cellSize=2, seed=8, palette=[solid(STONE), solid(*ANDESITE), solid(COBBLE), solid(*ANDESITE)]))
    styles["wet-rock"] = kit.BoulderStyle(form="outcrop", size=3, mossy=True, rock=kit.CellMaterial(
        cellSize=2, seed=9, palette=[solid(STONE), solid(*ANDESITE), solid(COBBLE), solid(*ANDESITE)]))
    # The cabin is the tall timber cottage in jungle wood: jungle logs and beam ends, jungle and oak planks.
    styles["cabin"] = kit.library("jungle-framed-cottage", kind="house")
    placed += [
        kit.TreeProp(id="j-1", x=-90, z=-30, style=JUNGLE[0], seed=1),
        kit.TreeProp(id="j-2", x=-76, z=-36, style=JUNGLE[3], seed=2),
        kit.TreeProp(id="j-3", x=-60, z=-26, style=JUNGLE[1], seed=3),
        kit.TreeProp(id="j-4", x=-76, z=-14, style=JUNGLE[4], seed=4),
        kit.TreeProp(id="j-5", x=-44, z=-18, style=JUNGLE[2], seed=5),
        kit.TreeProp(id="j-6", x=-31, z=-24, style=JUNGLE[5], seed=6),
        kit.TreeProp(id="o-1", x=-66, z=-7, style=OAK[0], seed=8),
        kit.TreeProp(id="o-2", x=-80, z=2, style=OAK[1], seed=9),
        kit.TreeProp(id="o-3", x=-26, z=-2, style=OAK[2], seed=10),
        kit.TreeProp(id="o-4", x=-48, z=31, style=OAK[0], seed=11),
        kit.BoulderProp(id="b-1", x=-30, z=-17, style="wet-rock", seed=1),
        kit.BoulderProp(id="b-2", x=-24, z=-10, style="wet-rock", seed=2),
        kit.BoulderProp(id="b-3", x=-70, z=-12, style="rock", seed=3),
        kit.BoulderProp(id="b-4", x=-91, z=-23, style="rock", seed=4),
        kit.BoulderProp(id="b-5", x=-72, z=-2, style="rock", seed=5),
        kit.HouseProp(id="cabin", style="cabin", seed=21, front="negZ",
                      wings=[kit.AuthoredWing(corners=[[-64, -20], [-55, -13]])]),
    ]

if outlines:
    finish["outlines"] = outlines
if STAGE >= 2:
    finish["dressing"] = kit.DressingDoc(styles=styles, props=placed)
refinement = kit.Refinement(**finish)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG, "stage", STAGE)
