"""Karnbeck — writes opus55-karnbeck.plan.json and .finish.json.

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
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, beds, by_slope, theme, one, ROCK, ring, patch, path, tree,
                        boulder, house, flora, pool, channel, house_style, boulder_style, copied_trees, made,
                        coast_edits)
import props

SLUG = "opus55-karnbeck"
SURFACE = 16
FIELD = [[-108, -56], [-16, -56], [-16, 56], [-108, 56]]

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
# Families: the ground green (meadow over dirt over grey rock), the built white and dark (white clay
# between dark-oak timbers; the keep's grey stone), the accent red (brick roofs, the granite and brick of
# the keep's yard).
MEADOW = noise([cell([S(3), S(3, 1)], 2, 3), S(2), S(2), S(2)], scale=2, seed=4)
SOIL = beds([(ROCK, 34), (S(3), 4), (S(3), 2)], start=-40, beyond=ROCK)
meadow = theme(by_slope((34, depth(MEADOW, S(3))), (14, depth(cell([S(3), S(3, 1)], 2, 5), S(3))),
                        (42, cell([S(1), S(1, 5), S(1), S(4)], 2, 6))), wall=SOIL, fill=SOIL)
# The keep's yard: a built floor of four blocks of one tone.
yard = theme(depth(cell([S(98), S(1, 6), S(1, 5), S(1)], 2, 7), S(1)), wall=ROCK, fill=ROCK, depth_=2)
keep = one(cell([S(98), S(98), S(1, 5), S(98, 2)], 2, 8, rise=2))
timber = one(S(5, 1))

PAVE = cell([S(3), S(3, 1), S(5, 1)], size=2, seed=21)

relief = {"team": {
    "base": SURFACE, "reach": 0, "step": 1, "landform": "hills",
    "marks": [
        {"id": "spawn-bench", "kind": "area", "h": 24, "bevel": 3,
         "ring": [[-126, -14], [-106, -14], [-106, 14], [-126, 14]]},
        {"id": "ramp", "kind": "line", "r": 4, "points": [[-108, 0], [-94, 2]], "h": [24, 19]},
        # the bluff the keep stands on
        {"id": "bluff", "kind": "area", "h": 22, "bevel": 3, "ring": ring(-64, 8, 15, 14, 24, 0.1, 3)},
        # the valley floor the beck runs down, and the far bank rising to the lip
        {"id": "valley", "kind": "line", "r": 7, "tread": 3,
         "points": [[-38, -56], [-42, -20], [-40, 10], [-44, 56]], "h": [12, 12, 12, 12]},
        # the way down the bluff's east face, out through the keep's east gap to the bridge
        {"id": "bluff-ramp", "kind": "line", "r": 3, "points": [[-54, 3], [-42, 2]], "h": [22, 13]},
        {"id": "lip", "kind": "line", "r": 3, "h": [16, 17, 16, 17, 16],
         "points": [[-19, -54], [-20, -26], [-18, 0], [-20, 26], [-19, 54]]},
        # the mill pond's floor behind the bluff
        {"id": "mill-floor", "kind": "area", "h": 15, "bevel": 3, "ring": ring(-88, -30, 12, 9, 24, 0.12, 3)},
    ],
    "pushes": [
        # the valley's two sides, centred off the coasts so only their flanks are on the board
        {"id": "north-side", "ring": ring(-86, 62, 24, 10, 28, 0.15, 4), "amount": 10, "falloff": 18,
         "roughness": 0.4, "crown": 0, "seed": 5},
        {"id": "south-side", "ring": ring(-74, -62, 22, 9, 28, 0.15, 4, 1), "amount": 9, "falloff": 18,
         "roughness": 0.4, "crown": 0, "seed": 6},
    ],
}}

# --- made things ----------------------------------------------------------------------------------------
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
shapes = [patch("keep-yard", ring(-62, 10, 10.5, 10.5, 32), "yard", SURFACE, group="team")]

# --- dressing ------------------------------------------------------------------------------------------
TREES = ["tree-showcase-r12-1", "tree-showcase-r12-2", "tree-showcase-r12-4", "tree-showcase-r13-3",
         "tree-showcase-r13-6"]
styles = dict(copied_trees(HERE, TREES))
timbered = json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "styles",
                                        "talltimber-cottage.json")))
timbered["wall"]["stack"]["bands"] = [
    {"material": {"kind": "laidLog", "id": 162, "data": 1}, "thickness": 1},
    {"material": S(159, 0), "thickness": 4}]
timbered["post"] = S(162, 1)
timbered["roof"]["body"] = S(45)
timbered["roof"]["verge"] = S(5, 5)
timbered["roof"]["gable"] = S(159, 0)
styles["timbered"] = {"kind": "house", "shell": timbered}
styles["rock"] = boulder_style(cell([S(1), S(1, 5), S(4)], 2, 51), form="round", size=2.2, mossy=True)
BANK = cell([S(13), S(3, 1), S(4)], 2, 61)

props_ = [
    channel("beck", [[-38, -58], [-43, -34], [-38, -14], [-41, 0], [-38, 14], [-44, 34], [-42, 58]],
            radius=3, depth=2, shore=2, bank=BANK),
    pool("mill-pond", ring(-88, -30, 8, 6, 20, 0.12, 3), depth=3, shelf=3, shore=2, bank=BANK),
    # paths: spawn to the keep, the keep down to the bridge, and a lane past the mill hamlet to the south
    path("path-keep", 41, [[-106, 1], [-94, 2], [-80, 6], [-72, 8]], PAVE),
    path("path-bridge", 42, [[-52, 4], [-51, 1]], PAVE, radius=1.5, wander=0),
    path("path-bridge-east", 45, [[-31, 1], [-24, 0], [-19, 0]], PAVE, radius=1.5, wander=1),
    path("path-mill", 43, [[-100, -8], [-94, -18], [-80, -22], [-66, -26], [-50, -24]], PAVE, radius=1.5),
    # a lane through the north wood to the beck, and on from the far bank to the lip: the way round
    path("path-wood", 46, [[-100, 10], [-90, 22], [-76, 36], [-60, 34], [-50, 28]], PAVE, radius=1.5),
    path("path-wood-east", 47, [[-34, 30], [-26, 28], [-20, 26]], PAVE, radius=1.5, wander=1),
    # the mill hamlet round the pond
    house("mill", "timbered", [[-78, -44], [-68, -36]], front="negX", seed=31, storeys=2),
    house("house-a", "timbered", [[-104, -40], [-96, -33]], front="posX", seed=32),
    house("house-b", "timbered", [[-102, -26], [-95, -19]], front="posX", seed=33, storeys=2),
    house("house-c", "timbered", [[-84, 12], [-77, 19]], front="negZ", seed=34),
    # oakwood on the valley sides; birch where the wood thins toward the beck
    tree("oak-1", -96, 40, "tree-showcase-r12-1", 1), tree("oak-2", -82, 46, "tree-showcase-r12-2", 2),
    tree("oak-3", -68, 44, "tree-showcase-r12-4", 3), tree("oak-4", -104, 24, "tree-showcase-r12-2", 4),
    tree("birch-1", -60, 27, "tree-showcase-r13-3", 6),
    tree("birch-2", -52, 48, "tree-showcase-r13-6", 7), tree("oak-6", -56, -46, "tree-showcase-r12-1", 8),
    tree("birch-4", -30, -46, "tree-showcase-r13-6", 10),
    tree("birch-5", -28, 42, "tree-showcase-r13-3", 11),
    boulder("b1", -46, -12, "rock", 12), boulder("b2", -34, 24, "rock", 13), boulder("b3", -74, 26, "rock", 14),
    flora("meadow-cover", [[-108, -56], [-16, -56], [-16, 56], [-108, 56]], coverage=0.3, scale=10, fern=0.25,
          flowers=0.1, flower_scale=12, tall=0.04, seed=71),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 4},
    "themes": {"meadow": meadow, "yard": yard, "keep": keep, "timber": timber},
    "mapTheme": "meadow",
    "relief": relief,
    "editShapes": {"field-16": coast_edits(FIELD, {
        0: [(0.08, 2), (0.2, 5), (0.3, 2), (0.45, 3), (0.58, 1), (0.7, 4), (0.84, 2), (0.94, 3)],
        2: [(0.06, 3), (0.18, 2), (0.3, 5), (0.42, 1), (0.55, 3), (0.68, 2), (0.8, 5), (0.92, 2)]})},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@17h-hall"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
