"""Gypsum Reach — writes opus55-gypsum-reach.plan.json and .refinement.json.

A pale desert lane: each team's emerald monument stands in the open on a low shelf, with a dry wash sunk in
front of it under a timber bridge, a grassed mesa off its outer flank, and a sunken oasis with a hamlet round
it on its inner flank. The spawn stands in the corner beside the oasis. The halves meet across a 32-block build
zone over void, with an island in the middle of it, and ruined walls stand along the lip where a crossing lands.

Second pass, after the author's review: the first build was all sand over twenty blocks of sandstone, two
houses, and an empty front. The rock under the sand became stone with sandstone beds over it, the north flank
an oasis with a pool, grass, acacias and olives and a hamlet round it, and the outline was cut into a coast.

Third pass, after the author's notes 36–43: the frontline is pushed out on one side and pulled in on the
other, with a middle island; the spawn moved into the corner by the oasis, facing along it; the oasis floor
sits four under the field; the houses are stone brick with no cobble or clay; the boulders are all the
larger angular kind; the sandstone arch is a timber bridge on posts with rails; the mesa's tower is gone for grass,
a tree and rocks; the monument is an emerald cube.

Fourth pass, after the author's notes 51–60: the houses have polished-andesite posts, walls of stone brick and
andesite in alternate courses, clay gables and jungle roofs; the wash reaches further in; an irregular plaza
lies under the monument; the lip ruins stand on the ground; the island is cut ragged; a path network reaches
every house, the bridge from both ends and the frontline's edge; and cacti stand on the open sand.

Fifth pass, after the author's notes 56 and 65–69: no path along the mesa's cliff; two broken lines of
hardened clay in the beds and no orange; paths and plaza in oak and jungle planks; dead bushes on the sand;
the wash floored in stone, cobble and gravel with no boulder; a second, smaller mesa on the back coast; and
the spawn room in the houses' style.

Sixth pass, after the author's notes 72–74: twenty-eight dead bushes a team; six patches of hardened clay
broken with sand across each field; and a second island a team at the strait's ends.

Seventh pass, once the studio grew what the board had worked round: the wash's whole floor is lava (note 72),
under a stone bridge in the houses' own language — polished-andesite pillars, an andesite course under a
stone-brick deck, cobblestone-wall rails — which nothing can set alight; and the cacti and dead bushes grow
from the dressing's flora over the open sand, with no sand patch under each.

Team 0 is the west half (x < 0); rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
from studio_kit import kit
import props

SLUG = "opus55-gypsum-reach"
SURFACE = 20
DESERT_COVER = 0.4              # how thickly the flora grows cacti and dead bushes on the open sand

# --- the plan: a field a team with the spawn in its oasis corner, the build zone and an island between -----
plan = {
    "plan": 2,
    "meta": {"name": "Gypsum Reach", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": SURFACE},
    "pieces": [
        {"id": "field", "rect": [-26, -12, 22, 20]},          # x -104..-16,  z -48..32
        {"id": "field-east", "rect": [-22, 8, 18, 4]},        # x -88..-16,   z 32..48
        {"id": "field-west", "rect": [-28, 6, 2, 6]},         # x -112..-104, z 24..48
        {"id": "field-back", "rect": [-26, 11, 4, 1]},        # x -104..-88,  z 44..48
        # the spawn inside the corner, not against it (note 37): land on its north and west
        {"id": "spawn", "role": "spawn", "rect": [-26, 8, 4, 3], "surface": 21},   # x -104..-88, z 32..44
        # the middle island (note 36), one piece on the axis
        {"id": "isle", "rect": [-1, -4, 2, 8], "surface": 18, "mirrors": False},   # x -4..4, z -16..16
        # a second island a team at the strait's ends, to cross by (note 74): fanned, x 0..8, z -44..-28
        {"id": "isle-south", "rect": [0, -11, 2, 4], "surface": 18},
    ],
    "zones": [{"id": "strait", "rect": [-4, -12, 4, 24]}],
    "placements": {
        # facing -z, so the oasis is on the left: a player runs along it and turns right to the front
        "spawns": [{"id": "sp", "piece": "spawn", "at": [8, 6], "facing": "front", "footprint": [2, 2, 12, 8]}],
        # field min corner is (-104, -48); the monument at (-70, -2). An emerald cube (note 43).
        "destroyables": [{"id": "mon", "piece": "field", "at": [34, 46], "style": "cube-3",
                          "materials": "emerald block", "name": "Gypsum Monument"}],
    },
}


# --- the paint ------------------------------------------------------------------------------------------
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


# Three tone families: the ground pale (sand over sandstone over stone), the built grey (stone brick under
# brick roofs), the accent warm (granite and brick in the paths, hardened clay in the beds) and the timber
# of the bridge.
#
# Under the sand: stone and andesite to ten blocks below the ground, then sandstone beds with one bed of
# hardened clay and one thin orange bed, following the ground so the mesa and the wash cut through them.
# Note 65: two lines of hardened clay, each two courses deep, broken up by the sandstone around them, and no
# orange clay.
ROCK = kit.CellMaterial(cellSize=2, seed=8, palette=[solid(1), solid(1, 5), solid(1), solid(4)], rise=2)
CLAY_LINE = kit.CellMaterial(cellSize=2, seed=65, rise=1,
                             palette=[solid(172), solid(24), solid(172), solid(24), solid(172)])
SANDSTONE_BEDS = [(solid(24), 2), (CLAY_LINE, 2), (solid(24), 3), (CLAY_LINE, 2), (solid(24, 2), 2)]
STRATA = stack((ROCK, 30), *(SANDSTONE_BEDS * 5), axis="height", from_=-40, follow=100, reach=16, beyond=ROCK)

SAND = kit.NoiseMaterial(scale=2, seed=11, stops=[solid(24), solid(12), solid(12), solid(12)])
SHOULDER = kit.CellMaterial(cellSize=2, seed=12, palette=[solid(24), solid(24, 2), solid(12)])
desert = finish(stack((stack((SAND, 1), (solid(24), 2)), 28), (stack((SHOULDER, 1), (solid(24), 2)), 17),
                      (STRATA, 45), axis="slope"),
                wall=STRATA, fill=STRATA)

# The oasis: grass on a desert biome, which tints it the dry yellow-green that sits beside sand, over
# dirt; where it steepens, dirt and coarse dirt half and half.
oasis = finish(stack((stack((solid(2), 1), (solid(3), 2)), 24),
                     (stack((kit.CellMaterial(cellSize=2, seed=31, palette=[solid(3), solid(3, 1)]), 1),
                            (solid(3), 2)), 20),
                     (STRATA, 46), axis="slope"),
               wall=STRATA, fill=STRATA)
# Worn ground in the hamlet: dirt and coarse dirt as one area.
worn = finish(stack((stack((kit.CellMaterial(cellSize=2, seed=32, palette=[solid(3), solid(3, 1)]), 1),
                           (solid(3), 2)), 30),
                    (STRATA, 60), axis="slope"),
              wall=STRATA, fill=STRATA)

# Made things: the ruins are stone brick, the ground's rock dressed; the bridge (notes 41, 72) is the houses'
# stone — polished-andesite pillars, an andesite course under a stone-brick deck, cobblestone-wall rails — so
# the lava under it has nothing to burn.
masonry = one(kit.CellMaterial(cellSize=2, seed=41, palette=[solid(98), solid(98), solid(98, 2), solid(1, 5)],
                               rise=2))
deck = one(solid(98))
post = one(solid(1, 6))
fascia = one(solid(1, 5))
rail = one(solid(139))

# Note 66: the paths and the plaza in oak and jungle planks; granite and brick did not sit on sand.
PAVE = kit.CellMaterial(cellSize=2, seed=21, palette=[solid(5, 0), solid(5, 3), solid(5, 0), solid(5, 3)])
plaza = finish(stack((stack((PAVE, 1), (solid(24), 2)), 30), (STRATA, 60), axis="slope"), wall=STRATA, fill=STRATA)
clay_patch = finish(stack((stack((kit.NoiseMaterial(scale=2, seed=73, stops=[solid(172), solid(172), solid(12),
                                                                              solid(172), solid(24)]), 1),
                                 (solid(172), 2)), 28),
                          (STRATA, 60), axis="slope"),
                    wall=STRATA, fill=STRATA)
# The wash's floor and its lava's bank: stone, cobble and gravel.
WASH_STONE = kit.CellMaterial(cellSize=2, seed=67, palette=[solid(1), solid(4), solid(13), solid(1), solid(4)])
wash_floor = finish(stack((stack((WASH_STONE, 1), (solid(1), 2)), 20), (STRATA, 70), axis="slope"),
                    wall=STRATA, fill=STRATA)

# --- the ground ------------------------------------------------------------------------------------------
# The wash's outline, carried a little further in toward the monument south of the bridge (note 52): the
# ellipse's west points between z -17 and -7 give way to a lobe reaching x -60. One push over the whole
# outline, because a second push or a mark over the same ground stacks with it and digs a pit. The ellipse is
# 7 by 15 about (-44, -2) with three lobes at 0.12 and phase 0.5, and the points run round its centre by angle.
WASH = [[-57, -8], [-50.5, -5.2], [-52, -6], [-60, -11], [-59, -14], [-55, -17], [-50, -18], [-44.0, -16.1],
        [-42.6, -15.0], [-41.3, -14.0], [-39.9, -12.9], [-38.5, -11.4], [-37.2, -9.0], [-36.4, -5.7],
        [-36.3, -2.0], [-36.9, 1.5], [-37.9, 4.3], [-39.1, 6.4], [-40.2, 8.3], [-41.2, 10.3], [-42.5, 12.3],
        [-44.0, 13.9], [-45.7, 14.2], [-47.4, 13.1], [-48.7, 10.5], [-49.4, 7.3], [-49.8, 4.0], [-50.0, 0.9],
        [-50.3, -2.0]]

relief = {"team": kit.SketchReliefJson(
    base=SURFACE, reach=0, step=1, landform="rolling",
    marks=[
        kit.ReliefMarkJson(id="spawn-yard", kind="area", h=21, bevel=3,
                           ring=[[-106, 30], [-86, 30], [-86, 46], [-106, 46]]),
        kit.ReliefMarkJson(id="shelf", kind="area", h=22, bevel=3),
        # the lip follows the reshaped frontline three blocks in
        kit.ReliefMarkJson(id="lip", kind="line", r=4, h=[17, 16, 18, 17, 16, 18, 17, 16],
                           points=[[-17, -44], [-12, -31], [-19, -20], [-23, -8], [-24, 4], [-22, 16], [-25, 28],
                                   [-27, 40]]),
        # the oasis floor four under the field (note 38), so the grass lies in a hollow the pool sits in
        kit.ReliefMarkJson(id="oasis-floor", kind="area", h=16, bevel=4),
    ],
    pushes=[
        kit.ReliefPushJson(id="wash", ring=WASH, amount=-6, falloff=5, roughness=0.35, crown=0, seed=3),

        kit.ReliefPushJson(id="mesa", amount=10, falloff=3, roughness=0.4, crown=0, seed=4),
        # a second, smaller mesa on the back coast north of the monument (note 68), hanging off the edge the way
        # the first hangs off the south coast
        kit.ReliefPushJson(id="mesa-west", amount=8, falloff=3, roughness=0.4, crown=0, seed=14),
        # a dune ridge off the back coast, south of the spawn, so the back of the field rises
        kit.ReliefPushJson(id="dune", amount=6, falloff=10, roughness=0.3, crown=0, seed=6),
    ])}

# Hardened clay lying in the sand here and there, the way the dirt lies in the hamlet (note 73): each patch's
# centre and its two radii.
CLAY = [(-94, -38, 4, 3), (-70, -21, 4, 2), (-36, -6, 3, 3), (-28, 36, 4, 3), (-86, -20, 3, 3), (-48, -44, 3, 2)]

# Every lobed outline on the board, by the id of what it outlines.
outlines = {
    "shelf": kit.Outline(at=[-70, -2], radius=12, radiusZ=10, points=28),
    "oasis-floor": kit.Outline(at=[-62, 30], radius=16, radiusZ=11, points=24, wobble=0.1, lobes=3),
    "mesa": kit.Outline(at=[-70, -40], radius=16, radiusZ=10, points=28, wobble=0.1, lobes=4),
    "mesa-west": kit.Outline(at=[-103, 6], radius=8, radiusZ=7, points=28, wobble=0.1, lobes=4, phase=0.3),
    "dune": kit.Outline(at=[-110, -20], radius=8, radiusZ=14, points=28, wobble=0.15, lobes=3, turn=-10),
    "oasis-grass": kit.Outline(at=[-63, 31], radius=25, radiusZ=15, points=32, wobble=0.12, lobes=5, phase=0.7),
    "spring-green": kit.Outline(at=[-47, -30], radius=8, radiusZ=5, points=20, wobble=0.15, lobes=3, phase=1.1),
    "mesa-top": kit.Outline(at=[-70, -40], radius=11, radiusZ=7, points=24, wobble=0.15, lobes=3, phase=0.4),
    "hamlet-yard": kit.Outline(at=[-88, 18], radius=8, radiusZ=6, points=20, wobble=0.15, lobes=3),
    "plaza": kit.Outline(at=[-70, -2], radius=8, radiusZ=6, points=22, wobble=0.25, lobes=4, phase=0.3),
    **{f"clay-{i}": kit.Outline(at=[x, z], radius=rx, radiusZ=rz, points=18, wobble=0.25, lobes=3, phase=i * 0.7)
       for i, (x, z, rx, rz) in enumerate(CLAY)},
    "oasis-pool": kit.Outline(at=[-63, 31], radius=8, radiusZ=5, points=20, wobble=0.15, lobes=3),
    "oasis-cover": kit.Outline(at=[-62, 31], radius=24, radiusZ=16, points=16),
}

# The wash's floor, every column of it whose top course is y13 or lower, read off the heightmap and, under the
# deck, off `column` row by row. The lava fills exactly this, so it
# stands one course under the bank all round and cuts none of it.
WASH_FLOOR = [[-53, -19], [-53, -18], [-56, -18], [-56, -16], [-57, -16], [-57, -15], [-58, -15], [-58, -14],
              [-59, -14], [-59, -13], [-58, -13], [-58, -11], [-57, -11], [-57, -9], [-56, -9], [-56, -8],
              [-54, -8], [-54, -7], [-53, -7], [-53, -6], [-54, -6], [-54, -5], [-53, -5], [-53, -3],
              [-52, -3], [-52, -2], [-51, -2], [-51, 7], [-50, 7], [-50, 13], [-49, 13], [-49, 14],
              [-48, 14], [-48, 16], [-43, 16], [-43, 15], [-42, 15], [-42, 14], [-41, 14], [-41, 13],
              [-40, 13], [-40, 12], [-39, 12], [-39, 10], [-38, 10], [-38, 8], [-37, 8], [-37, 6],
              [-36, 6], [-36, 4], [-35, 4], [-35, 0], [-34, 0], [-34, -7], [-35, -7], [-35, -10],
              [-36, -10], [-36, -11], [-37, -11], [-37, -12], [-38, -12], [-38, -13], [-39, -13], [-39, -14],
              [-40, -14], [-40, -15], [-41, -15], [-41, -16], [-42, -16], [-42, -17], [-44, -17], [-44, -18],
              [-47, -18], [-47, -19]]


# --- the made things -------------------------------------------------------------------------------------
def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as storeys of made ground, all of one `part_of`."""
    return [kit.AddedLayer(id=layer["id"], name=layer["name"], base_y=layer["base_y"], kind="made", part_of=part_of,
                           shapes=layer["layout"]["shapes"], groups=layer["layout"]["groups"],
                           **({"seat": seat} if seat else {}))
            for layer in (layers if isinstance(layers, list) else [layers])]


# The bridge over the wash (notes 41, 72): a stone-brick deck five wide on an andesite course, standing on three
# pairs of polished-andesite pillars down through the lava to the wash floor, with a cobblestone-wall rail along
# each side. Left open to the air under it, so nothing clears the wash beneath.
def bridge_part(pid, cells, keep_clear=False):
    """One part of the bridge; a rect covers x0..x1-1 and z0..z1-1."""
    b = props.LayerBuilder(pid)
    for x0, z0, x1, z1, floor, height, th in cells:
        b.rect(x0, z0, x1, z1, floor, height, th, keepClear=keep_clear)
    return b.done()

# The deck stands at 19 over the wash's west rim and steps down one to the lip at 17 on its east end.
BX0, BX1, BZ0, BZ1, BY = -54, -35, -4, 0, SURFACE - 2
layers = made([
    bridge_part("bridge-deck", [(BX0, BZ0, BX1 + 1, BZ1 + 1, BY, 1, "deck"),
                                (BX1 + 1, BZ0 + 1, BX1 + 3, BZ1, BY - 1, 1, "deck")]),
    # the pillars are kept clear, so the lava fills round them and never cuts the floor out from under them
    bridge_part("bridge-posts", [(x, z, x + 1, z + 1, 11, BY - 11, "post")
                                 for x in (-50, -44, -38) for z in (BZ0, BZ1)], keep_clear=True),
    bridge_part("bridge-fascia", [(BX0, z, BX1 + 1, z + 1, BY - 1, 1, "fascia") for z in (BZ0, BZ1)]),
    bridge_part("bridge-rails", [(BX0, z, BX1 + 1, z + 1, BY + 1, 1, "rail") for z in (BZ0, BZ1)]),
], "wash-bridge")
# Ruined walls along the lip, cover where a crossing lands.
# Each stands from y14, below the lip's ground (top course y16 in the north, y17 in the south), so no column of
# it floats (note 54): the seat on the ground did not lower them, and `column` under each is the check.
layers += made(props.crenellated_wall("ruin-north", -32, 18, -29, 34, 1, 14, 6, "masonry",
                                      merlon=2, crenel=3, parapet=1), "ruin-north")
layers += made(props.crenellated_wall("ruin-south", -29, -44, -26, -30, 1, 14, 6, "masonry",
                                      merlon=3, crenel=2, parapet=2), "ruin-south")


# --- the patches --------------------------------------------------------------------------------------
def patch(pid, theme_id, vertices=None):
    """A patch of different ground: a polygon at the height of the ground it lies on, in the team's group, with
    its own theme and no relief_scope, so it paints the cells it forms the surface of and nothing else. Its
    outline is `vertices`, or the outline stated under its id."""
    return {**kit.SketchShape(id=pid, type="polygon", operation="add", base_height=SURFACE, theme=theme_id,
                              **({"vertices": vertices} if vertices else {})),
            **kit.ShapeJoin(group="team")}


shapes = [
    patch("oasis-grass", "oasis"),
    # a spring at the mesa's foot, east of the monument's approach from above: a copse on a green
    patch("spring-green", "oasis"),
    # grass on the mesa top where the tower stood (note 42)
    patch("mesa-top", "oasis"),
    patch("hamlet-yard", "worn"),
    # an irregular plaza of the path's own paving under the monument (note 53)
    patch("plaza", "plaza"),
    # hardened clay lying in the sand here and there, the way the dirt lies in the hamlet (note 73)
] + [
    patch(f"clay-{i}", "clay-patch") for i in range(len(CLAY))
] + [
    # the wash's floor in stone, cobble and gravel; its banks keep the beds (note 67)
    patch("wash-floor", "wash-floor", WASH),
]

# --- the dressing ---------------------------------------------------------------------------------------
# The copied trees, each the showcase tree it names, as corpus/tree-showcase/trees.json carries it.
SHOWCASE = json.load(open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")))["trees"]
styles = {key: kit.build("TreeStyle", SHOWCASE[tree]["style"]) for key, tree in {
    "tree-showcase-r8-1": "acacia-1", "tree-showcase-r8-3": "acacia-3",
    "tree-showcase-r10-1": "olive-1", "tree-showcase-r10-3": "olive-3"}.items()}


# The houses (notes 39 and 51): the shipped stone house repainted to the author's words. Polished-andesite
# posts, walls of stone brick and andesite in alternate courses on every storey, a hardened-clay gable, and a
# jungle-plank roof with jungle slabs.
def stone_wall(extent):
    # a stack's `repeat` carries its last band on rather than cycling, so the alternation is written out
    return kit.RoomPart(stack=kit.BandStack(ending="repeat", bands=[
        kit.Band(material=solid(98) if course % 2 == 0 else solid(1, 5), thickness=1) for course in range(12)]),
        extent=extent)


PLAIN = kit.FloorSurface(field=None, border=None, borderWidth=1, inlay=None, inlayInset=2)


def stone(storeys):
    """The stone laid over a library row: its walls, posts, roof and foundation plate, and `storeys`, the row's
    own storeys in the stone, each stated whole because a list laid over a row replaces the row's."""
    return {"wall": stone_wall(5), "post": solid(1, 6), "storeys": storeys,
            "roof": {"body": solid(5, 3), "verge": solid(5, 3), "gable": solid(172), "slab": 126, "slabData": 3},
            "foundation": {"plate": {"stack": {"bands": [kit.Band(material=solid(98), thickness=1)]}}}}


styles["stonehouse"] = kit.library("hw-stonehouse", kind="house", shell=stone([
    kit.Storey(clear=5, wall=stone_wall(5), post=solid(1, 6), surface=PLAIN, deck=None, headroom=5,
               windows=kit.WindowStyle(form="pane", block=102, hostBlock=-1, hostData=0, data=0, sill=2, width=2,
                                       height=2, spacing=4)),
    kit.Storey(clear=4, wall=stone_wall(4), post=solid(1, 6), surface=PLAIN, deck=None, headroom=4,
               windows=kit.WindowStyle(form="pane", block=102, hostBlock=-1, hostData=0, data=0, sill=1, width=2,
                                       height=2, spacing=4))]))
# The spawn room in the houses' own style (note 69): the shipped spawn room in the stone, so its entry and floor
# stay what a room needs.
SPAWN_ROOM = kit.library("sb-spawn", **stone([
    kit.Storey(clear=5, wall=stone_wall(5), post=solid(1, 6), surface=PLAIN, deck=None, headroom=5,
               windows=kit.WindowStyle(form="pane", block=160, hostBlock=-1, hostData=0, data=0, sill=3, width=2,
                                       height=2, spacing=3)),
    kit.Storey(clear=4, wall=stone_wall(4), post=solid(1, 6), surface=PLAIN, deck=None, headroom=4,
               windows=kit.WindowStyle(form="stairLattice", block=134, hostBlock=-1, hostData=0, data=0, sill=2,
                                       width=2, height=2, spacing=3))]))
# One kind of rock (note 40): the larger angular boulder; the small round one read as a stone box.
styles["rock"] = kit.BoulderStyle(form="angular", size=2.5, mossy=False, rock=kit.CellMaterial(
    cellSize=2, seed=51, palette=[solid(1), solid(1, 5), solid(1), solid(4)]))


def path(pid, seed, points, radius=1.5, wander=2):
    return kit.StrokeProp(id=pid, seed=seed, style="solid", radius=radius, claimsGround=True, wander=wander,
                          wanderLength=14, pave=PAVE, points=points)


def house(pid, corners, front, seed, storeys=None):
    return kit.HouseProp(id=pid, style="stonehouse", seed=seed, front=front, wings=[
        kit.AuthoredWing(corners=corners, **({"spec": kit.WingSpec(storeysHigh=storeys)} if storeys else {}))])


props_ = [
    # the path network (notes 56-59): every house reached, the bridge reached from both ends, and every road
    # that heads for the front run on until the ground ends
    path("path-mon", 41, [[-97, 31], [-94, 20], [-88, 8], [-80, 1], [-76, -1]]),
    path("path-hamlet", 42, [[-96, 22], [-86, 15], [-72, 14], [-58, 13], [-46, 17], [-32, 15], [-24, 12],
                             [-17, 12]]),
    path("path-bridge-west", 43, [[-64, -2], [-55, -2]], radius=2, wander=0),
    path("path-bridge-east", 44, [[-32, -2], [-26, -3], [-17, -5]], radius=2, wander=1),
    path("path-houses", 45, [[-76, -7], [-81, -11], [-81, -20], [-81, -27]]),
    # the third house's path runs from its door east to the lip, and no longer along the mesa's cliff (note 56)
    path("path-spring", 46, [[-55, -23], [-47, -26], [-36, -27], [-24, -26], [-10, -30]]),
    path("path-oasis", 47, [[-45, 17], [-45, 27], [-41, 36]], wander=1),
    # the houses, moved out of the spawn's way (note 37): two behind the monument, one by the spring, and two
    # on the oasis's rim
    house("house-a", [[-92, -14], [-84, -7]], "posX", 31),
    house("house-b", [[-92, -32], [-84, -25]], "posX", 32),
    house("house-c", [[-72, 16], [-65, 22]], "negZ", 33, storeys=2),
    house("house-d", [[-64, -26], [-57, -20]], "posX", 34),
    house("house-e", [[-44, 38], [-37, 44]], "negZ", 35),
    # the pool the oasis is for
    kit.FluidProp(id="oasis-pool", shape="pool", form="natural", layer="ground", radius=3, depth=3, shore=2,
                  shoreWander=True, edge=1.5, fluid="water",
                  bank=kit.CellMaterial(cellSize=2, seed=61, palette=[solid(12), solid(24), solid(12)])),
    # palms of the warm kinds: acacias round the water, olives by the houses
    kit.TreeProp(id="t1", x=-78, z=25, style="tree-showcase-r8-1", seed=1),
    kit.TreeProp(id="t2", x=-69, z=41, style="tree-showcase-r8-3", seed=2),
    kit.TreeProp(id="t4", x=-52, z=24, style="tree-showcase-r8-1", seed=4),
    kit.TreeProp(id="t5", x=-50, z=34, style="tree-showcase-r10-1", seed=5),
    kit.TreeProp(id="t7", x=-51, z=-34, style="tree-showcase-r10-1", seed=7),
    kit.TreeProp(id="t-mesa", x=-72, z=-40, style="tree-showcase-r8-3", seed=8),
    # rocks at the wash's head, the mesa top, the lip and the middle island
    kit.BoulderProp(id="b1", x=-36, z=-40, style="rock", seed=8),
    kit.BoulderProp(id="b2", x=-36, z=22, style="rock", seed=9),
    kit.BoulderProp(id="b4", x=-24, z=-18, style="rock", seed=11),
    kit.BoulderProp(id="b-mesa-1", x=-64, z=-43, style="rock", seed=12),
    kit.BoulderProp(id="b-mesa-2", x=-77, z=-37, style="rock", seed=13),
    kit.BoulderProp(id="b-isle", x=-1, z=-9, style="rock", seed=14),
    # the grass carries a little cover, and none of it tall
    kit.FloraProp(id="oasis-cover", seed=71,
                  spec=kit.FloraSpec(coverage=0.35, scale=8, octaves=2, fernShare=0.2, flowerShare=0.05,
                                     flowerScale=12, tallShare=0.03, deadBushShare=0.0, cactusShare=0.0)),
    # the wash's whole floor in lava (note 72), stated at 13 so it lies one course under the bank
    kit.FluidProp(id="wash-lava", shape="pool", form="natural", layer="ground", points=WASH_FLOOR, radius=2,
                  depth=2, shore=0, shoreWander=True, edge=0, fluid="lava", bank=WASH_STONE, level=13),
] + [
    # cacti and dead bushes over the open sand (notes 60, 66, 73), in rings that keep off the grass: the oasis,
    # the spring's green and the mesa top grow grass under any flora
    kit.FloraProp(id=f"sand-cover-{i}", seed=90 + i, points=box,
                  spec=kit.FloraSpec(coverage=DESERT_COVER, scale=3, octaves=2, fernShare=0, flowerShare=0,
                                     flowerScale=12, tallShare=0, deadBushShare=1.0, cactusShare=0.4))
    for i, box in enumerate([
        [[-104, -48], [-82, -48], [-82, 10], [-104, 10]],        # the back strip, west of the mesa
        [[-82, -32], [-56, -32], [-56, 10], [-82, 10]],          # behind the monument, north of the mesa top
        [[-56, -24], [-18, -24], [-18, 10], [-56, 10]],          # the wash's banks and the lip, north of the spring
        [[-38, -48], [-18, -48], [-18, -24], [-38, -24]],        # east of the spring
        [[-58, -48], [-39, -48], [-39, -36], [-58, -36]],        # between the mesa top and the spring
        [[-104, 10], [-88, 10], [-88, 48], [-104, 48]],          # the spawn's side, west of the oasis
        [[-34, 10], [-18, 10], [-18, 48], [-34, 48]],            # the lip's north end, clear of the oasis grass
        [[-88, 10], [-38, 10], [-38, 15], [-88, 15]],            # the strip between the hamlet road and the oasis
    ])
]

refinement = kit.Refinement(
    created="2026-09-28",
    authors=["Opus 5.5"],
    biome=kit.SolidBiome(id=2),
    themes={"desert": desert, "oasis": oasis, "worn": worn, "masonry": masonry, "deck": deck, "post": post,
            "rail": rail, "plaza": plaza, "wash-floor": wash_floor, "clay-patch": clay_patch, "fascia": fascia},
    mapTheme="desert",
    relief=relief,
    outlines=outlines,
    # The frontline (note 36): pushed out toward the island south of it and pulled in north of it, t along
    # the edge being (z + 48) / 96 and a negative pull a push. The back, south and north coasts cut lightly;
    # the spawn's seams are left as the plan cut them. A pull is (t, inward), on an edge named by the vertex it
    # leaves.
    editShapes={
        "field-20": [kit.VertexEdit(pulls={
            "1": [[0.3, 2], [0.6, 3], [0.85, 2]],                                      # the back coast
            "2": [[0.15, 2], [0.4, 3], [0.65, 1], [0.88, 3]],                           # the south coast
            "3": [[0.083, -4], [0.19, -7], [0.29, 0], [0.42, 4], [0.54, 5], [0.67, 3], [0.79, 6], [0.9, 8],
                  [0.97, 3]],                                                          # the frontline
            "4": [[0.1, 3], [0.3, 2], [0.5, 4], [0.7, 2]]})],                           # the north coast
        # the middle island (note 55) stands on the axis, so its cuts are stated on one short end and one long
        # side, and the studio makes each at its rot_180 image too: the same t on each opposite edge, which keeps
        # it fair to both teams
        "isle-18": [kit.VertexEdit(pulls={"0": [[0.3, 2], [0.7, -1]],
                                          "1": [[0.12, -2], [0.3, 1], [0.5, -3], [0.68, 2], [0.85, -1]]})],
        # the strait's end island, fanned to its image on red's side with its cuts
        "isle-south-18": [kit.VertexEdit(pulls={"0": [[0.3, 2], [0.7, -1]], "1": [[0.2, -2], [0.5, 2], [0.8, -1]],
                                                "2": [[0.4, 1], [0.75, -2]], "3": [[0.25, 1], [0.6, -2]]})]},
    addShapes=shapes,
    addLayers=layers,
    roomStyles={"spawn": SPAWN_ROOM},
    dressing=kit.DressingDoc(styles=styles, props=props_),
)

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
