"""Gypsum Reach — writes opus55-gypsum-reach.plan.json and .finish.json.

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

Team 0 is the west half (x < 0); rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, beds, by_slope, theme, one, ROCK, ring, patch, path, tree,
                        boulder, house, flora, pool, house_style, boulder_style, copied_trees, made, coast_edits)
import props

SLUG = "opus55-gypsum-reach"
# field-20 as the plan compiles it: the field, less the spawn's corner, plus the strip west of the spawn
FIELD = [[-112, 24], [-104, 24], [-104, -48], [-16, -48], [-16, 48], [-112, 48]]
SURFACE = 20
ISLE = [[-4, -16], [4, -16], [4, 16], [-4, 16]]             # isle-18, the middle island
# (t, inward) along the short ends and along the long sides; a negative pull pushes the coast out
ISLE_CUTS = {0: [(0.3, 2), (0.7, -1)], 1: [(0.12, -2), (0.3, 1), (0.5, -3), (0.68, 2), (0.85, -1)]}

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
# Three tone families: the ground pale (sand over sandstone over stone), the built grey (stone brick under
# brick roofs), the accent warm (granite and brick in the paths, hardened clay in the beds) and the timber
# of the bridge.
#
# Under the sand: stone and andesite to ten blocks below the ground, then sandstone beds with one bed of
# hardened clay and one thin orange bed, following the ground so the mesa and the wash cut through them.
SANDSTONE_BEDS = [(S(24, 0), 3), (S(24, 2), 2), (S(172), 1), (S(24, 0), 2), (S(159, 1), 1), (S(24, 0), 2)]
STRATA = beds([(ROCK, 30)] + SANDSTONE_BEDS * 5, start=-40, beyond=ROCK)

SAND = noise([S(24, 0), S(12), S(12), S(12)], scale=2, seed=11)
SHOULDER = cell([S(24, 0), S(24, 2), S(12)], size=2, seed=12)
desert = theme(by_slope((28, depth(SAND, S(24, 0))), (17, depth(SHOULDER, S(24, 0))), (45, STRATA)),
               wall=STRATA, fill=STRATA)

# The oasis: grass on a desert biome, which tints it the dry yellow-green that sits beside sand, over
# dirt; where it steepens, dirt and coarse dirt half and half.
oasis = theme(by_slope((24, depth(S(2), S(3))), (20, depth(cell([S(3), S(3, 1)], 2, 31), S(3))),
                       (46, STRATA)), wall=STRATA, fill=STRATA)
# Worn ground in the hamlet: dirt and coarse dirt as one area.
worn = theme(by_slope((30, depth(cell([S(3), S(3, 1)], 2, 32), S(3))), (60, STRATA)),
             wall=STRATA, fill=STRATA)

# Made things: the ruins are stone brick, the ground's rock dressed; the bridge is spruce planks on dark-oak
# posts behind oak-fence rails (note 41).
masonry = one(cell([S(98), S(98), S(98, 2), S(1, 5)], 2, 41, rise=2))
deck = one(S(5, 1))
post = one(S(162, 1))
rail = one(S(85))
cactus = one(S(81))
sand_bed = theme(depth(S(12), S(12)), wall=S(12), fill=S(12))

PAVE = cell([S(1, 1), S(1, 2), S(45), S(1, 1)], size=2, seed=21)
plaza = theme(by_slope((30, depth(PAVE, S(24, 0))), (60, STRATA)), wall=STRATA, fill=STRATA)

# --- the ground ------------------------------------------------------------------------------------------
# The wash's outline, carried a little further in toward the monument south of the bridge (note 52): the
# ellipse's west points between z -17 and -7 give way to a lobe reaching x -60. One push over the whole
# outline, because a second push or a mark over the same ground stacks with it and digs a pit.
def wash_ring():
    import math
    cx, cz = -44, -2
    pts = [p for p in ring(cx, cz, 7, 15, wobble=0.12, lobes=3, phase=0.5)
           if not (p[0] < cx and -18 <= p[1] <= -6)]
    pts += [[-50, -18], [-55, -17], [-59, -14], [-60, -11], [-57, -8], [-52, -6]]
    return sorted(pts, key=lambda p: math.atan2(p[1] - cz, p[0] - cx))
WASH = wash_ring()

relief = {"team": {
    "base": SURFACE, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "spawn-yard", "kind": "area", "h": 21, "bevel": 3,
         "ring": [[-106, 30], [-86, 30], [-86, 46], [-106, 46]]},
        {"id": "shelf", "kind": "area", "h": 22, "bevel": 3, "ring": ring(-70, -2, 12, 10)},
        # the lip follows the reshaped frontline three blocks in
        {"id": "lip", "kind": "line", "r": 4, "h": [17, 16, 18, 17, 16, 18, 17, 16],
         "points": [[-17, -44], [-12, -31], [-19, -20], [-23, -8], [-24, 4], [-22, 16], [-25, 28], [-27, 40]]},
        # the oasis floor four under the field (note 38), so the grass lies in a hollow the pool sits in
        {"id": "oasis-floor", "kind": "area", "h": 16, "bevel": 4, "ring": ring(-62, 30, 16, 11, 24, 0.1, 3)},
    ],
    "pushes": [
        {"id": "wash", "ring": WASH,
         "amount": -6, "falloff": 5, "roughness": 0.35, "crown": 0, "seed": 3},

        {"id": "mesa", "ring": ring(-70, -40, 16, 10, wobble=0.1, lobes=4),
         "amount": 10, "falloff": 3, "roughness": 0.4, "crown": 0, "seed": 4},
        # a dune ridge off the back coast, south of the spawn, so the back of the field rises
        {"id": "dune", "ring": ring(-110, -20, 8, 14, wobble=0.15, lobes=3, turn=-10),
         "amount": 6, "falloff": 10, "roughness": 0.3, "crown": 0, "seed": 6},
    ],
}}

# --- the made things -------------------------------------------------------------------------------------
# The bridge over the wash (note 41): a spruce deck five wide, standing on three pairs
# of dark-oak posts down to the wash floor, with an oak-fence rail along each side. Left open to the air
# under it, so nothing clears the wash beneath.
def bridge_part(pid, cells):
    """One part of the bridge; a rect covers x0..x1-1 and z0..z1-1."""
    b = props.LayerBuilder(pid)
    for x0, z0, x1, z1, floor, height, th in cells:
        b.rect(x0, z0, x1, z1, floor, height, th, keepClear=False)
    return b.done()

# The deck stands at 19 over the wash's west rim and steps down one to the lip at 17 on its east end.
BX0, BX1, BZ0, BZ1, BY = -54, -35, -4, 0, SURFACE - 2
layers = made([
    bridge_part("bridge-deck", [(BX0, BZ0, BX1 + 1, BZ1 + 1, BY, 1, "deck"),
                                (BX1 + 1, BZ0 + 1, BX1 + 3, BZ1, BY - 1, 1, "deck")]),
    bridge_part("bridge-posts", [(x, z, x + 1, z + 1, 11, BY - 11, "post")
                                 for x in (-50, -44, -38) for z in (BZ0, BZ1)]),
    bridge_part("bridge-rails", [(BX0, z, BX1 + 1, z + 1, BY + 1, 1, "rail") for z in (BZ0, BZ1)]),
], "wash-bridge")
# Cacti on the open sand (note 60), on made layers because the dressing has no cactus yet. Each stands on the
# ground's top course as `column` read it, one to three tall, with nothing solid beside it.
# The studio paints the ground under a made column with its theme's fill, and a 1.8 cactus off sand breaks
# at the first block update beside it. So each cactus stands in a small patch whose fill is sand; a made layer
# of sand under it would not do, because a made layer does not replace the ground's own blocks.
CACTI = [(-100, 2, 20, 2), (-98, 14, 20, 3), (-96, -40, 20, 1), (-101, -22, 20, 2),
         (-40, -45, 17, 3), (-30, 42, 15, 2), (-56, 9, 18, 1)]
cacti = props.LayerBuilder("cacti")
for x, z, top, tall in CACTI:
    cacti.rect(x, z, x + 1, z + 1, top + 1, tall, "cactus", keepClear=False)
layers += made(cacti.done(), "cacti")
# Ruined walls along the lip, cover where a crossing lands.
# Each stands from y14, below the lip's ground (top course y16 in the north, y17 in the south), so no column of
# it floats (note 54): the seat on the ground did not lower them, and `column` under each is the check.
layers += made(props.crenellated_wall("ruin-north", -32, 18, -29, 34, 1, 14, 6, "masonry",
                                      merlon=2, crenel=3, parapet=1), "ruin-north")
layers += made(props.crenellated_wall("ruin-south", -29, -44, -26, -30, 1, 14, 6, "masonry",
                                      merlon=3, crenel=2, parapet=2), "ruin-south")

# --- the patches --------------------------------------------------------------------------------------
shapes = [
    patch("oasis-grass", ring(-63, 31, 25, 15, 32, 0.12, 5, 0.7), "oasis", SURFACE, group="team"),
    # a spring at the mesa's foot, east of the monument's approach from above: a copse on a green
    patch("spring-green", ring(-47, -30, 8, 5, 20, 0.15, 3, 1.1), "oasis", SURFACE, group="team"),
    # grass on the mesa top where the tower stood (note 42)
    patch("mesa-top", ring(-70, -40, 11, 7, 24, 0.15, 3, 0.4), "oasis", SURFACE, group="team"),
    patch("hamlet-yard", ring(-88, 18, 8, 6, 20, 0.15, 3), "worn", SURFACE, group="team"),
    # an irregular plaza of the path's own paving under the monument (note 53)
    patch("plaza", ring(-70, -2, 8, 6, 22, 0.25, 4, 0.3), "plaza", SURFACE, group="team"),
] + [
    patch(f"cactus-bed-{i}", [[x - 1, z - 1], [x + 2, z - 1], [x + 2, z + 2], [x - 1, z + 2]], "sand-bed", SURFACE,
          group="team") for i, (x, z, _, _) in enumerate(CACTI)
]

# --- the dressing ---------------------------------------------------------------------------------------
TREES = ["tree-showcase-r8-1", "tree-showcase-r8-3",
         "tree-showcase-r10-1", "tree-showcase-r10-3"]
styles = dict(copied_trees(HERE, TREES))

# The houses (notes 39 and 51): the shipped stone house repainted to the author's words. Polished-andesite
# posts, walls of stone brick and andesite in alternate courses on every storey, a hardened-clay gable, and a
# jungle-plank roof with jungle slabs.
def stone_walls(shell):
    # a stack's `repeat` carries its last band on rather than cycling, so the alternation is written out
    wall = {"stack": {"ending": "repeat", "bands": [
        {"material": S(98) if i % 2 == 0 else S(1, 5), "thickness": 1} for i in range(12)]}, "extent": 5}
    shell["wall"] = wall
    shell["post"] = S(1, 6)
    for storey in shell["storeys"]:
        storey["wall"] = dict(wall, extent=storey["wall"]["extent"])
        storey["post"] = S(1, 6)
    shell["roof"].update({"body": S(5, 3), "verge": S(5, 3), "gable": S(172), "slab": 126, "slabData": 3})
    shell["foundation"]["plate"]["stack"]["bands"][0]["material"] = S(98)
    return shell

stonehouse = house_style("hw-stonehouse")
stone_walls(stonehouse["shell"])
styles["stonehouse"] = stonehouse
# One kind of rock (note 40): the larger angular boulder; the small round one read as a stone box.
styles["rock"] = boulder_style(cell([S(1), S(1, 5), S(1), S(4)], 2, 51), form="angular", size=2.5)

props_ = [
    # the path network (notes 56-59): every house reached, the bridge reached from both ends, and every road
    # that heads for the front run on until the ground ends
    path("path-mon", 41, [[-97, 31], [-96, 20], [-90, 8], [-80, 1], [-76, -1]], PAVE),
    path("path-hamlet", 42, [[-96, 22], [-86, 15], [-72, 14], [-58, 13], [-46, 17], [-32, 15], [-24, 12],
                             [-17, 12]], PAVE),
    path("path-bridge-west", 43, [[-64, -2], [-55, -2]], PAVE, radius=2, wander=0),
    path("path-bridge-east", 44, [[-32, -2], [-26, -3], [-17, -5]], PAVE, radius=2, wander=1),
    path("path-houses", 45, [[-76, -7], [-81, -11], [-81, -20], [-81, -29]], PAVE),
    path("path-spring", 46, [[-81, -29], [-73, -27], [-66, -29], [-56, -29], [-47, -27], [-36, -27],
                             [-24, -26], [-10, -30]], PAVE),
    path("path-d-porch", 48, [[-55, -23], [-51, -27]], PAVE, wander=0),
    path("path-oasis", 47, [[-45, 17], [-45, 27], [-41, 36]], PAVE, wander=1),
    # the houses, moved out of the spawn's way (note 37): two behind the monument, one by the spring, and two
    # on the oasis's rim
    house("house-a", "stonehouse", [[-92, -14], [-84, -7]], front="posX", seed=31),
    house("house-b", "stonehouse", [[-92, -32], [-84, -25]], front="posX", seed=32),
    house("house-c", "stonehouse", [[-72, 16], [-65, 22]], front="negZ", seed=33, storeys=2),
    house("house-d", "stonehouse", [[-64, -26], [-57, -20]], front="posX", seed=34),
    house("house-e", "stonehouse", [[-44, 38], [-37, 44]], front="negZ", seed=35),
    # the pool the oasis is for
    pool("oasis-pool", ring(-63, 31, 8, 5, 20, 0.15, 3), depth=3, shelf=3, shore=2,
         bank=cell([S(12), S(24, 0), S(12)], 2, 61)),
    # palms of the warm kinds: acacias round the water, olives by the houses
    tree("t1", -78, 25, "tree-showcase-r8-1", 1), tree("t2", -69, 41, "tree-showcase-r8-3", 2),
    tree("t4", -52, 24, "tree-showcase-r8-1", 4), tree("t5", -50, 34, "tree-showcase-r10-1", 5),
    tree("t7", -51, -34, "tree-showcase-r10-1", 7),
    tree("t-mesa", -72, -40, "tree-showcase-r8-3", 8),
    # rocks at the wash's head, the mesa top, the lip and the middle island
    boulder("b1", -36, -40, "rock", 8), boulder("b2", -36, 22, "rock", 9),
    boulder("b3", -57, -12, "rock", 10), boulder("b4", -24, -18, "rock", 11),
    boulder("b-mesa-1", -64, -43, "rock", 12), boulder("b-mesa-2", -77, -37, "rock", 13),
    boulder("b-isle", -1, -9, "rock", 14),
    # the grass carries a little cover, and none of it tall
    flora("oasis-cover", ring(-62, 31, 24, 16, 16), coverage=0.35, scale=8, fern=0.2, flowers=0.05,
          tall=0.03, seed=71),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 2},
    "themes": {"desert": desert, "oasis": oasis, "worn": worn, "masonry": masonry,
               "deck": deck, "post": post, "rail": rail, "plaza": plaza, "cactus": cactus, "sand-bed": sand_bed},
    "mapTheme": "desert",
    "relief": relief,
    # The frontline (note 36): pushed out toward the island south of it and pulled in north of it, t along
    # the edge being (z + 48) / 96 and a negative pull a push. The back, south and north coasts cut lightly;
    # the spawn's seams are left as the plan cut them.
    "editShapes": {"field-20": coast_edits(FIELD, {
        1: [(0.3, 2), (0.6, 3), (0.85, 2)],
        2: [(0.15, 2), (0.4, 3), (0.65, 1), (0.88, 3)],
        3: [(0.083, -4), (0.19, -7), (0.29, 0), (0.42, 4), (0.54, 5), (0.67, 3), (0.79, 6), (0.9, 8), (0.97, 3)],
        4: [(0.1, 3), (0.3, 2), (0.5, 4), (0.7, 2)]}),
        # the middle island (note 55): one on the axis and not fanned, so its edits are stated in rot_180
        # pairs, the same t on each opposite edge, and it stays fair to both teams
        "isle-18": coast_edits(ISLE, {e: ISLE_CUTS[e % 2] for e in range(4)})},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@sb-spawn"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
