"""Gypsum Reach — writes opus55-gypsum-reach.plan.json and .finish.json.

A pale desert lane: each team's obsidian monument stands in the open on a low shelf, with a dry wash sunk
in front of it and a sandstone arch over the wash (the way in from below), a mesa with a ruined watchtower
off its outer flank (the way in from above), and an oasis village on its inner flank (the way in through).
The two halves meet across a 32-block build zone over void that spans the board's whole width, and ruined
walls stand along the lip where a crossing lands.

Second pass, after the author's review: the first build was all sand over twenty blocks of sandstone, two
houses, and an empty front. Now the rock under the sand is stone with sandstone beds over it, the north
flank is an oasis with a pool, grass, acacias and olives and a hamlet of six houses round it, the wash
carries an arch, the mesa a tower, the lip two ruins, and the outline is cut and bent into a coast.

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
FIELD = [[-104, -48], [-16, -48], [-16, 48], [-104, 48]]   # field-20 as the plan compiles it
SURFACE = 20

# --- the plan: a spawn bench and one field a team, the build zone between them -------------------------
plan = {
    "plan": 2,
    "meta": {"name": "Gypsum Reach", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": SURFACE},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-31, -3, 5, 6], "surface": 24},
        {"id": "field", "rect": [-26, -12, 22, 24]},
    ],
    "zones": [{"id": "strait", "rect": [-4, -12, 4, 24]}],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [10, 12], "facing": "right",
                    "footprint": [2, 5, 14, 14]}],
        # field min corner is (-104, -48); the monument at (-66, -16) is 38, 32 blocks in
        "destroyables": [{"id": "mon", "piece": "field", "at": [38, 32], "style": "pillar-3",
                          "name": "Gypsum Monument"}],
    },
}

# --- the paint ------------------------------------------------------------------------------------------
# Three tone families: the ground pale (sand over sandstone over stone), the built grey (stone brick under
# brick roofs), the accent warm (granite and brick in the paths, hardened clay in the beds).
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

# Made things: the ruins and the watchtower are stone brick, the ground's rock dressed; the arch is the
# sandstone beds themselves, a natural bridge left standing when the wash was cut.
masonry = one(cell([S(98), S(98), S(98, 2), S(1, 5)], 2, 41, rise=2))
arch_rock = one(cell([S(24, 0), S(24, 2), S(24, 0)], 2, 42, rise=2))

PAVE = cell([S(1, 1), S(1, 2), S(45), S(1, 1)], size=2, seed=21)

# --- the ground ------------------------------------------------------------------------------------------
relief = {"team": {
    "base": SURFACE, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "bench", "kind": "area", "h": 24, "bevel": 3,
         "ring": [[-124, -14], [-100, -14], [-100, 14], [-124, 14]]},
        {"id": "ramp-spawn-field", "kind": "line", "r": 3, "points": [[-109, 0], [-99, 0]], "h": [24, 20]},
        {"id": "shelf", "kind": "area", "h": 22, "bevel": 3, "ring": ring(-68, -16, 13, 11)},
        {"id": "lip", "kind": "line", "r": 4, "h": [17, 16, 18, 16, 17],
         "points": [[-19, -46], [-20, -24], [-18, 0], [-20, 24], [-19, 46]]},
        # the oasis floor, a little under the field, so the grass lies in a hollow the pool sits in
        {"id": "oasis-floor", "kind": "area", "h": 18, "bevel": 4, "ring": ring(-62, 30, 16, 11, 24, 0.1, 3)},
    ],
    "pushes": [
        {"id": "wash", "ring": ring(-40, -12, 7, 19, wobble=0.12, lobes=3, phase=0.5),
         "amount": -6, "falloff": 5, "roughness": 0.35, "crown": 0, "seed": 3},
        {"id": "mesa", "ring": ring(-70, -46, 16, 11, wobble=0.1, lobes=4),
         "amount": 13, "falloff": 3, "roughness": 0.4, "crown": 0, "seed": 4},
        # a dune ridge behind the village, off the north-west coast, so the back of the flank rises
        {"id": "dune", "ring": ring(-106, 50, 14, 8, wobble=0.15, lobes=3, turn=-10),
         "amount": 6, "falloff": 10, "roughness": 0.3, "crown": 0, "seed": 6},
    ],
}}

# --- the made things -------------------------------------------------------------------------------------
layers = []
# The natural arch over the wash: two piers on the rims and a deck at the shelf's height, so a player can
# cross the wash dry-shod or drop under it.
layers += made(props.arch("wash-arch", -52, -30, -13, 5, 12, 3, 2, "arch-rock", steps=9), "wash-arch")
# A ruined watchtower on the mesa, looking down on the monument: an open drum, no roof.
layers += made(props.tapered_tower("mesa-tower", -76, -45, 4.5, 3.5, 1.5, 34, 9, "masonry", courses=3),
               "mesa-tower", seat="ground")
# Ruined walls along the lip, cover where a crossing lands.
layers += made(props.crenellated_wall("ruin-north", -32, 18, -29, 34, 1, 20, 3, "masonry",
                                      merlon=2, crenel=3, parapet=1), "ruin-north", seat="ground")
layers += made(props.crenellated_wall("ruin-south", -29, -44, -26, -30, 1, 20, 2, "masonry",
                                      merlon=3, crenel=2, parapet=2), "ruin-south", seat="ground")

# --- the patches --------------------------------------------------------------------------------------
shapes = [
    patch("oasis-grass", ring(-63, 31, 25, 15, 32, 0.12, 5, 0.7), "oasis", SURFACE, group="team"),
    # a spring at the mesa's foot, east of the monument's approach from above: a copse on a green
    patch("spring-green", ring(-47, -36, 9, 6, 20, 0.15, 3, 1.1), "oasis", SURFACE, group="team"),
    patch("hamlet-yard", ring(-86, 26, 9, 7, 20, 0.15, 3), "worn", SURFACE, group="team"),
]

# --- the dressing ---------------------------------------------------------------------------------------
TREES = ["tree-showcase-r8-1", "tree-showcase-r8-3",
         "tree-showcase-r10-1", "tree-showcase-r10-3"]
styles = dict(copied_trees(HERE, TREES))
styles["stonehouse"] = house_style("hw-stonehouse")
styles["rock"] = boulder_style(cell([S(1), S(1, 5), S(1), S(4)], 2, 51), form="angular", size=2.5)
styles["rock-small"] = boulder_style(cell([S(1), S(1, 5), S(4)], 2, 52), form="round", size=1.8)

props_ = [
    # the monument's own path, and the hamlet road on to the lip
    path("path-mon", 41, [[-102, -2], [-88, -9], [-76, -14]], PAVE),
    path("path-hamlet", 42, [[-102, 3], [-92, 12], [-78, 18], [-62, 16], [-46, 14], [-32, 10], [-22, 8]], PAVE),
    # the two houses behind the monument
    house("house-a", "stonehouse", [[-86, -4], [-77, 4]], front="posX", seed=31),
    house("house-b", "stonehouse", [[-92, -32], [-84, -25]], front="posX", seed=32),
    # the hamlet round the oasis: one style, varied in footprint and height
    house("house-c", "stonehouse", [[-97, 12], [-89, 20]], front="posX", seed=33, storeys=2),
    house("house-d", "stonehouse", [[-84, 35], [-77, 41]], front="negZ", seed=34),
    house("house-e", "stonehouse", [[-54, 38], [-47, 44]], front="negZ", seed=35),
    house("house-f", "stonehouse", [[-48, 18], [-41, 25]], front="negX", seed=36, storeys=2),
    # the pool the oasis is for
    pool("oasis-pool", ring(-63, 31, 8, 5, 20, 0.15, 3), depth=3, shelf=3, shore=2,
         bank=cell([S(12), S(24, 0), S(12)], 2, 61)),
    # palms of the warm kinds: acacias round the water, olives by the houses
    tree("t1", -75, 24, "tree-showcase-r8-1", 1), tree("t2", -69, 41, "tree-showcase-r8-3", 2),
    tree("t4", -52, 24, "tree-showcase-r8-1", 4),
    tree("t5", -40, 33, "tree-showcase-r10-1", 5), tree("t6", -88, 30, "tree-showcase-r10-3", 6),
    tree("t7", -50, -37, "tree-showcase-r10-1", 7),
    # rocks at the wash's head and the mesa's foot
    boulder("b1", -36, -40, "rock", 8), boulder("b2", -35, 12, "rock-small", 9),
    boulder("b3", -58, -31, "rock", 10), boulder("b4", -24, -18, "rock-small", 11),
    # the grass carries a little cover, and none of it tall
    flora("oasis-cover", ring(-62, 31, 24, 16, 16), coverage=0.35, scale=8, fern=0.2, flowers=0.05,
          tall=0.03, seed=71),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 2},
    "themes": {"desert": desert, "oasis": oasis, "worn": worn, "masonry": masonry, "arch-rock": arch_rock},
    "mapTheme": "desert",
    "relief": relief,
    # the field's coast: a cove bitten into the north coast east of the village, by the lip, then the whole ring bent
    # Only the two coasts: the back edge is the spawn bench's seam and the east edge the frontline, and a
    # bend over the whole ring pulled the back edge off the bench and left the spawn on an island (EX1).
    "editShapes": {"field-20": coast_edits(FIELD, {
        0: [(0.08, 2), (0.2, 4), (0.3, 1), (0.52, 3), (0.62, 1), (0.74, 4), (0.86, 2), (0.95, 3)],
        2: [(0.06, 2), (0.14, 8), (0.2, 3), (0.3, 1), (0.42, 3), (0.55, 1), (0.66, 4), (0.8, 2), (0.9, 3)]})},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@sb-spawn"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
