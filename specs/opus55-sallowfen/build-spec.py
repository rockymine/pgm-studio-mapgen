"""Sallowfen — writes opus55-sallowfen.plan.json and .finish.json.

A fen of willows and reed pools, where each team keeps two monuments on peat hummocks north and south of a
dry causeway running out from its spawn. A stream winds across the fen in front of both hummocks, crossed
by two plank boardwalks; pools lie in hollows on the flanks; a hamlet of stilt houses stands on the
causeway by the spawn, and a watch platform on four legs stands near the lip where a crossing lands. The
halves meet across a 32-block build zone over void the whole width of the board.

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

SLUG = "opus55-sallowfen"
SURFACE = 12
FIELD = [[-124, -64], [-16, -64], [-16, 64], [-124, 64]]      # field-12 as the plan compiles it

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
# Families: the ground green-brown (fen grass with podzol and worn earth), the built timber (spruce on
# stilts under oak roofs), the accent the grey of stone gables and the boardwalks' spruce.
# Swampland tints grass the olive that meets podzol as one leaf-littered floor.
GRASS, PODZOL = S(2), S(3, 2)
WORN = cell([S(3), S(3, 1)], 2, 7)
FEN = noise([PODZOL, GRASS, GRASS, GRASS, WORN], scale=2, seed=5)
PEAT = beds([(ROCK, 30), (S(82), 2), (S(3), 3), (S(3, 1), 1), (S(3), 4)] + [(S(3), 20)], start=-40, beyond=ROCK)
fen = theme(by_slope((26, depth(FEN, S(3))), (20, depth(WORN, S(3))), (44, PEAT)), wall=PEAT, fill=PEAT)
# The hummocks' tops: podzol under the willows, one leaf-littered floor on this biome.
hummock = theme(by_slope((26, depth(noise([GRASS, PODZOL, PODZOL, GRASS], 2, 13), S(3))), (64, PEAT)),
                wall=PEAT, fill=PEAT)
planks = one(S(5, 1))
post = one(S(17, 1))

PAVE = cell([S(3), S(3, 1), S(5, 1)], size=2, seed=21)

relief = {"team": {
    "base": SURFACE, "reach": 0, "step": 1, "landform": "plain",
    "marks": [
        {"id": "knoll", "kind": "area", "h": 16, "bevel": 3,
         "ring": [[-142, -14], [-120, -14], [-120, 14], [-142, 14]]},
        {"id": "ramp", "kind": "line", "r": 4, "points": [[-122, 0], [-108, 0]], "h": [16, 13]},
        {"id": "causeway", "kind": "line", "r": 5, "tread": 3, "points": [[-108, 0], [-84, 2], [-60, -1]],
         "h": [13, 13, 13]},
        {"id": "hummock-s", "kind": "area", "h": 17, "bevel": 4, "ring": ring(-78, -30, 12, 10, 24, 0.12, 3)},
        {"id": "hummock-n", "kind": "area", "h": 17, "bevel": 4, "ring": ring(-76, 30, 12, 10, 24, 0.12, 3, 1)},
        {"id": "lip", "kind": "line", "r": 4, "h": [11, 12, 11, 12, 11],
         "points": [[-19, -62], [-20, -30], [-18, 0], [-20, 30], [-19, 62]]},
    ],
    "pushes": [
        {"id": "hollow-sw", "ring": ring(-102, -42, 11, 8, 24, 0.15, 3), "amount": -4, "falloff": 4,
         "roughness": 0.3, "crown": 0, "seed": 3},
        {"id": "hollow-nw", "ring": ring(-100, 44, 10, 8, 24, 0.15, 3, 2), "amount": -4, "falloff": 4,
         "roughness": 0.3, "crown": 0, "seed": 4},
        {"id": "hollow-front", "ring": ring(-30, -28, 7, 9, 24, 0.15, 3, 1), "amount": -2, "falloff": 4,
         "roughness": 0.3, "crown": 0, "seed": 5},
        # carr banks: wooded rises centred off both coasts, so the fen's flanks climb out of the wet
        {"id": "bank-n", "ring": ring(-78, 72, 30, 9, 28, 0.15, 4), "amount": 6, "falloff": 8,
         "roughness": 0.4, "crown": 0, "seed": 6},
        {"id": "bank-s", "ring": ring(-96, -72, 26, 9, 28, 0.15, 4, 1), "amount": 5, "falloff": 8,
         "roughness": 0.4, "crown": 0, "seed": 7},
    ],
}}

# --- made things --------------------------------------------------------------------------------------------
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
shapes = [
    patch("hummock-s-top", ring(-78, -30, 15, 12, 24, 0.12, 4), "hummock", SURFACE, group="team"),
    patch("hummock-n-top", ring(-76, 30, 15, 12, 24, 0.12, 4, 1), "hummock", SURFACE, group="team"),
]

# --- dressing -------------------------------------------------------------------------------------------
TREES = ["tree-showcase-r17-1", "tree-showcase-r17-3", "tree-showcase-r17-5",
         "tree-showcase-r5-1", "tree-showcase-r5-2"]
styles = dict(copied_trees(HERE, TREES))
# The stilt house stands over the fen rather than on a floor laid across it: the plate is air (HS10).
styles["stilt"] = house_style("stilts", foundation={
    "plate": {"stack": {"bands": [{"material": S(0), "thickness": 1}], "ending": "repeat"}, "extent": 1},
    "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
    "footing": None})
styles["rock"] = boulder_style(cell([S(1), S(1, 5), S(4)], 2, 51), form="round", size=2, mossy=True)
BANK = cell([S(3), S(3, 1), S(13)], 2, 61)

props_ = [
    # water: the stream across the fen in front of both stones, and two pools in the flank hollows
    channel("stream", [[-44, 66], [-40, 44], [-46, 22], [-44, 2], [-50, -18], [-46, -42], [-52, -66]],
            radius=3, depth=2, shore=1, bank=BANK),
    pool("pool-sw", ring(-102, -42, 8, 5, 20, 0.15, 3), depth=2, shelf=2, shore=2, bank=BANK),
    pool("pool-nw", ring(-100, 44, 7, 5, 20, 0.15, 3, 2), depth=2, shelf=2, shore=2, bank=BANK),
    pool("pool-front", ring(-30, -28, 4, 6, 20, 0.15, 3, 1), depth=2, shelf=2, shore=1, bank=BANK),
    # paths: the causeway, and a spur to each stone
    # the causeway, broken at the boardwalk: a stroke repaints the top course it crosses, water included, so
    # one drawn through the stream paved it over
    path("path-causeway", 41, [[-122, 0], [-104, 1], [-84, 2], [-66, 0], [-57, 0]], PAVE, radius=2),
    path("path-causeway-east", 44, [[-37, 0], [-30, 1], [-22, 0]], PAVE, radius=2, wander=1),
    path("path-south", 42, [[-90, 1], [-86, -12], [-82, -20]], PAVE, radius=1.5),
    path("path-north", 43, [[-88, 3], [-84, 14], [-80, 20]], PAVE, radius=1.5),
    # the stilt hamlet along the causeway
    house("house-a", "stilt", [[-114, 8], [-106, 15]], front="negZ", seed=31),
    house("house-b", "stilt", [[-100, 9], [-92, 16]], front="negZ", seed=32, storeys=3),
    house("house-c", "stilt", [[-114, -16], [-106, -9]], front="posZ", seed=33, storeys=3),
    house("house-d", "stilt", [[-100, -17], [-92, -10]], front="posZ", seed=34),
    house("house-e", "stilt", [[-116, 26], [-108, 33]], front="posX", seed=35),
    # willows at the water and the hummocks' outer sides, dark oaks at the back coasts
    tree("w1", -110, -34, "tree-showcase-r17-1", 1), tree("w2", -92, -52, "tree-showcase-r17-3", 2),
    tree("w3", -112, 52, "tree-showcase-r17-5", 3), tree("w4", -88, 54, "tree-showcase-r17-1", 4),
    tree("w5", -62, 50, "tree-showcase-r17-3", 5), tree("w6", -64, -50, "tree-showcase-r17-5", 6),
    tree("w7", -30, 50, "tree-showcase-r17-1", 7), tree("w8", -26, -52, "tree-showcase-r17-3", 8),
    tree("o1", -120, -52, "tree-showcase-r5-1", 9), tree("o2", -103, 34, "tree-showcase-r5-2", 10),
    tree("o3", -92, 30, "tree-showcase-r5-1", 11), tree("o4", -94, -28, "tree-showcase-r5-2", 12),
    boulder("b1", -58, -20, "rock", 13), boulder("b2", -60, 18, "rock", 14),
    flora("fen-cover", [[-124, -64], [-16, -64], [-16, 64], [-124, 64]], coverage=0.3, scale=9, fern=0.4,
          flowers=0.06, flower_scale=10, tall=0.04, seed=71),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 6},
    "themes": {"fen": fen, "hummock": hummock, "planks": planks, "post": post},
    "mapTheme": "fen",
    "relief": relief,
    "editShapes": {"field-12": coast_edits(FIELD, {
        0: [(0.06, 3), (0.16, 6), (0.24, 2), (0.36, 4), (0.48, 1), (0.6, 5), (0.7, 2), (0.82, 4), (0.93, 2)],
        2: [(0.07, 2), (0.18, 4), (0.3, 7), (0.4, 2), (0.52, 3), (0.64, 1), (0.76, 5), (0.86, 2), (0.95, 3)]})},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@sb-spawn"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
