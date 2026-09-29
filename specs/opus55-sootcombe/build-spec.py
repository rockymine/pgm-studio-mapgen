"""Sootcombe — writes opus55-sootcombe.plan.json and .finish.json.

A capture board on an ash field: a combe of grey slag falling from each team's brick hamlet, standing on a
terrace four blocks over its hub, down to a flat frontline and a slag stone in the middle of the build band
with a ruined engine house on it. Two wools a team: one at the end of a spur west of the hub behind a
bedrock wall, one at the east end of the terrace behind another. A timber headframe stands over the shaft
at the hub bar's west end, beside the slag heap the shaft threw up.

The arrangement is composed board p12 t2 #21 (`composed-p12-seed21.plan.json`, pinned off GET /api/compose),
taken whole: this spec states its elevation, its paint, its made things and its dressing, and nothing about
where the pieces are. Team 0 is the z > 0 half; rot_180 fans the rest.

Second pass, after the author's review: the first build was bare ash. The outer coasts were cut point by
point, and birch and tiny spruce stand on regrowth along the hub's outer rims.

Third pass, after the author's notes 6, 8, 10 and 33–35: the ground is back to black clay on grey stained clay,
in larger patches, over granite; the slag heap, the engine house and the timber stacks are gone; the
headframe is now a shorter archer tower on each frontline with a one-course deck; the frontline and the mid
stone carry granite boulders; the paths are wider and laid in dirt, coarse dirt and spruce planks; and every
room is a timber lodge in the headframe's own language.

Fourth pass, after the author's notes 33 and 44–50: the rocks are cyan stained clay; the archer tower has a
spruce platform at its frame's course with a nether-brick fence on its beams and a ladder up through it; the
ash is a turbulence field with more black and a little dark oak; the faces and the fill are tilted beds of
hardened clay, granite and a mix, parted by thin lines of hardened clay; the hub's north-west corner rises
five blocks; a second build zone lies east of each hub; and a coast cut that pushed ground past the east
wall's end is turned the right way.

Fifth pass, after the author's notes 7, 10, 33 and 61–64: the mid stone rises a block in its middle and dips
at the lips facing the frontlines, and each frontline dips along part of its edge; every room is the stone
house of Gypsum Reach under a pitched roof; the boulders are andesite and cobble, two larger ones on the
mid stone; grass patches lie at the frontline's back, on the mid stone and on the west rise; and a willow
written for the board stands in the regrowth and on the mid stone's edge.

Sixth pass, after the author's notes 10, 64, 70 and 71: the doors are three tall and the wool rooms' doors
are stained glass in the wool's colour; two more willows stand on the west rise and at the terrace's edge;
and a grass patch lies on each frontline's west front.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, by_slope, theme, one, ring, patch, path, tree, flora,
                        boulder, boulder_style, copied_trees, made, coast_edits, willow)
import props

SLUG = "opus55-sootcombe"
plan = json.load(open(os.path.join(HERE, "composed-p12-seed21.plan.json")))
plan["meta"] = {"name": "Sootcombe", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 21 (walled-4), arrangement unchanged but for one build zone"}
# A build zone along the hub's east side (note 50): four blocks of void east of the hub between the frontline
# and the east approach, overlapping the hub by eight so a bridge leaves it with no gap, and ending seven
# blocks short of the east wool's wall. Twelve blocks wide because G2 wants a zone corridor of ten.
plan["zones"].append({"id": "hub-flank", "rect": [-2, 10, 3, 7], "holes": []})

# The one fused ground shape the plan compiles to, as it compiles.
GROUND = [[-44, 56], [-20, 56], [-20, 40], [-16, 40], [-16, 20], [16, 20], [16, 40], [0, 40], [0, 68],
          [36, 68], [36, 80], [-4, 80], [-4, 96], [-16, 96], [-16, 80], [-20, 80], [-20, 68], [-44, 68]]

# --- paint -----------------------------------------------------------------------------------------------
# Families: the ground dark (black clay on grey stained clay, granite under it), the built timber (spruce
# planks between dark-oak logs), the accent the granite of the rock, the boulders and the odd path block.
GREY, BLACK = S(159, 7), S(159, 15)
WORN = cell([S(3, 1), S(3, 0)], 2, 7)
# The author's ruling on note 6: the black clay on grey stained clay of the first build, in larger patches;
# and on note 46, more black and a little dark oak, as a turbulence field. A turbulence folds the field, so
# the low stops run as creases through it and the high ones billow: black in the creases, grey and worn
# earth between, black again and a few dark-oak plank patches at the top.
ASH = {"kind": "turbulence", "seed": 5, "scale": 7, "octaves": 3,
       "stops": [BLACK, BLACK, GREY, GREY, WORN, GREY, BLACK, BLACK, S(5, 5)]}
# The rock under it is granite and polished granite (note 6), and it is also the steepest band.
GRANITE = cell([S(1, 1), S(1, 2), S(1, 1), S(1, 2)], 2, 8, rise=2)
SHOULDER = cell([GREY, S(1, 1), S(1, 2)], 2, 6)
# The faces (note 47): tilted beds of three kinds, mostly hardened clay, mostly granite, and a wider mix,
# each parted from the next by a thin line of hardened clay; the mix is granite with grey and black clay, so
# the clay lines read against it. A diagonal wall pattern shears its stripes one
# arc cell per two courses, so a bed eight cells wide stands four courses thick and a line two wide is one.
CLAY_BED = cell([S(172), S(172), S(172), S(1, 1)], 3, 71, rise=2)
GRANITE_BED = cell([S(1, 1), S(1, 2), S(1, 1), S(1, 2)], 3, 72, rise=2)
MIXED_BED = cell([S(1, 1), GREY, S(1, 2), S(159, 15), GREY], 2, 73, rise=2)
LINE = S(172)
STRATA = {"kind": "wallDiagonal", "slope": 2, "runs": [
    {"material": GRANITE_BED, "width": 8}, {"material": LINE, "width": 2},
    {"material": MIXED_BED, "width": 6}, {"material": LINE, "width": 2},
    {"material": CLAY_BED, "width": 8},
    {"material": GRANITE_BED, "width": 6}, {"material": LINE, "width": 2},
    {"material": MIXED_BED, "width": 8}, {"material": LINE, "width": 2}]}
ash = theme(by_slope((30, depth(ASH, GREY)), (15, depth(SHOULDER, S(1, 1))), (45, GRANITE)),
            wall=STRATA, fill=STRATA)
# Regrowth: grass and worn earth where birch has taken hold.
regrowth = theme(by_slope((30, depth(noise([WORN, S(2), S(2), S(2)], 2, 12), S(3))), (60, GRANITE)),
                 wall=STRATA, fill=STRATA)
# Made: the archer tower's dark-oak logs and planks, the headframe's own two blocks.
timber = one(S(5, 5))
post = one(S(162, 1))
# The archer tower's platform (note 45): spruce planks, nether-brick fence, and a ladder set against a beam.
# The mirror turns a layer and not a block's data, so each team's ladder is stated with its own facing:
# red's faces north onto its south beam, blue's image faces south onto its north beam.
planks = one(S(5, 1))
fence = one(S(113))
ladder_n = one(S(65, 2))
ladder_s = one(S(65, 3))

# The paths (note 6): dirt, coarse dirt and spruce planks, with very little granite — one entry in seven.
PAVE = cell([S(3), S(3, 1), S(5, 1), S(3), S(3, 1), S(5, 1), S(1, 1)], size=2, seed=21)

# The rooms (notes 10, twice): the lodge's timber read brown on the brown ash, so every room is now the stone
# house of Gypsum Reach, which the author named as fitting: polished-andesite posts, walls of stone brick and
# andesite in alternate courses, a hardened-clay gable under a pitched jungle-plank roof. It is forked from
# the lodge's own room style, so the room's entry and floor stay what a room needs; only the paint and the
# roof's form change. A stack's `repeat` carries its last band on rather than cycling, so the courses are
# written out.
LODGE = json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "styles", "lk-spawn.json")))
STONE_WALL = {"stack": {"ending": "repeat", "bands": [
    {"material": S(98) if i % 2 == 0 else S(1, 5), "thickness": 1} for i in range(12)]}, "extent": 5}
LODGE["foundation"]["plate"]["stack"]["bands"][0]["material"] = S(98)
LODGE["foundation"]["footing"] = None
LODGE["wall"] = STONE_WALL
LODGE["post"] = S(1, 6)
LODGE["roof"].update({"form": "gable", "ridgeCap": True, "body": S(5, 3), "verge": S(5, 3), "gable": S(172),
                      "slab": 126, "slabData": 3})
for storey in LODGE["storeys"]:
    storey["wall"] = dict(STONE_WALL, extent=storey["wall"]["extent"])
    storey["post"] = S(1, 6)
# note 10 again: a door three tall. Its width is not the style's: the studio cuts a room's door to its wall
# (WX7), four on these walls. The wool rooms' doors are filled with stained-glass panes in the wool's colour,
# which an attacker breaks through; the spawn rooms keep an open door.
LODGE["doorway"].update({"width": 2, "height": 3})
WOOL_ROOM = json.loads(json.dumps(LODGE))
WOOL_ROOM["doorway"]["door"] = "stainedGlassPane"

relief = {"team": {
    "base": 10, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "terrace", "kind": "area", "h": 13, "ring": [[-20, 70], [36, 70], [36, 97], [-20, 97]]},
        {"id": "front", "kind": "area", "h": 9, "ring": [[-17, 20], [17, 20], [17, 33], [-17, 33]]},
        {"id": "spur", "kind": "line", "r": 6, "tread": 4, "points": [[-22, 62], [-42, 62]], "h": [11, 10]},
    ],
    # The slag heap is gone (note 8): the board is too small to carry a rock that size. In its place the
    # hub's north-west corner, where the spur meets it, rises five blocks over the terrain (note 49).
    "pushes": [
        # note 7: the mid stone rises a block or two in its middle, from two offset bumps that the fan
        # overlaps (a push on its centre would be fanned onto itself and doubled), and dips at the lip
        # facing each frontline. The stone takes its relief from its z < 0 half and fans it, so its pushes
        # are stated there. Each frontline dips two blocks along part of its edge, in a curve.
        {"id": "mid-rise", "ring": ring(-3, 0, 4, 3, wobble=0.1, lobes=3), "amount": 1, "falloff": 3,
         "roughness": 0.2, "crown": 0, "seed": 11},
        {"id": "mid-lip", "ring": ring(3, -8, 5, 2, wobble=0.1, lobes=3), "amount": -2, "falloff": 2,
         "roughness": 0.2, "crown": 0, "seed": 12},
        {"id": "front-dip", "ring": ring(2, 20, 6, 3, wobble=0.1, lobes=3), "amount": -2, "falloff": 4,
         "roughness": 0.2, "crown": 0, "seed": 13},
        {"id": "west-rise", "ring": ring(-19, 74, 3, 6, wobble=0.1, lobes=3), "amount": 5,
                "falloff": 7, "roughness": 0.3, "crown": 0, "seed": 9}],
}}

# --- made things -----------------------------------------------------------------------------------------
layers = []

# The archer tower on each frontline (note 35): the headframe, shorter and moved to the front — four dark-oak
# log legs, a plank frame halfway up, and a deck one course thick. The engine house on the mid stone is gone
# (note 33), and the timber stacks are boulders now (note 34).
AX, AZ, AW = 9, 33, 5            # its west-north corner and its width, at the frontline's back east corner
FLOOR = 9                        # the frontline is pinned at 9, so its top course is y8
legs = props.LayerBuilder("archer-legs")
for dx in (0, AW - 1):
    for dz in (0, AW - 1):
        legs.rect(AX + dx, AZ + dz, AX + dx + 1, AZ + dz + 1, FLOOR, 9, "post")
frame = props.LayerBuilder("archer-frame")
for x0, z0, x1, z1 in [(AX + 1, AZ, AX + AW - 1, AZ + 1), (AX + 1, AZ + AW - 1, AX + AW - 1, AZ + AW),
                       (AX, AZ + 1, AX + 1, AZ + AW - 1), (AX + AW - 1, AZ + 1, AX + AW, AZ + AW - 1)]:
    frame.rect(x0, z0, x1, z1, FLOOR + 4, 1, "timber")
# The platform (note 45): the four beams ring a 3 x 3 floor of spruce planks at the frame's course, open in
# one cell against the south beam, where a ladder climbs from the ground; a nether-brick fence stands on
# every beam, and the roof is the deck one course thick over it. A rect covers x0 .. x1 - 1.
HX, HZ = AX + 2, AZ + AW - 2                     # the ladder's hole, against the beam at z = AZ + AW - 1
floor_ = props.LayerBuilder("archer-floor")
for x in range(AX + 1, AX + AW - 1):
    for z in range(AZ + 1, AZ + AW - 1):
        if (x, z) != (HX, HZ):
            floor_.rect(x, z, x + 1, z + 1, FLOOR + 4, 1, "planks", keepClear=False)
rail = props.LayerBuilder("archer-rail")
for x0, z0, x1, z1 in [(AX + 1, AZ, AX + AW - 1, AZ + 1), (AX + 1, AZ + AW - 1, AX + AW - 1, AZ + AW),
                       (AX, AZ + 1, AX + 1, AZ + AW - 1), (AX + AW - 1, AZ + 1, AX + AW, AZ + AW - 1)]:
    rail.rect(x0, z0, x1, z1, FLOOR + 5, 1, "fence", keepClear=False)
climb = props.LayerBuilder("archer-ladder", mirrors=False)
climb.rect(HX, HZ, HX + 1, HZ + 1, FLOOR, 5, "ladder-n", keepClear=False)
climb.rect(-HX - 1, -HZ - 1, -HX, -HZ, FLOOR, 5, "ladder-s", keepClear=False)
deck = props.LayerBuilder("archer-deck")
deck.rect(AX - 1, AZ - 1, AX + AW + 1, AZ + AW + 1, FLOOR + 9, 1, "timber")
layers += made([legs.done(), frame.done(), floor_.done(), rail.done(), climb.done(), deck.done()],
               "archer-tower")

# --- patches -------------------------------------------------------------------------------------------
shapes = [
    patch("regrowth-west", [[-20, 42], [-14, 43], [-13, 52], [-15, 60], [-14, 67], [-20, 67]], "regrowth", 9,
          group="team"),
    patch("regrowth-bar", [[-2, 76], [10, 76], [12, 80], [-2, 80]], "regrowth", 9, group="team"),
    # grass at the frontline's back, on the mid stone round its willow, and on the west rise's top (61, 62, 64)
    patch("regrowth-front", ring(2, 38, 4, 3, 16, 0.2, 3), "regrowth", 9, group="team"),
    patch("regrowth-mid", ring(-8, -5, 4, 3, 16, 0.2, 3, 0.5), "regrowth", 9, group="team"),
    patch("regrowth-rise", ring(-18, 74, 3, 5, 16, 0.2, 3), "regrowth", 9, group="team"),
    # grass on the frontline's west front (note 71)
    patch("regrowth-front-west", ring(-9, 24, 6, 4, 16, 0.2, 3, 0.8), "regrowth", 9, group="team"),
]

# --- dressing ------------------------------------------------------------------------------------------
# One willow in the regrowth and a smaller one at the mid stone's edge (notes 62, 63). The tree library has
# no willow, so the kit writes one as a copied recipe: leaves hanging in curtains from a flattened crown.
styles = {"willow": willow(11, 5, seed=3, gaps=0.45), "willow-small": willow(9, 4, seed=7)}
# The boulders (notes 34 and 33), small and medium, all of cyan stained clay, which the 1.8 textures draw
# as a dark grey.
# note 33 again: andesite and cobblestone, whose texture stands off the flat clay ground; two larger rocks on
# the mid stone in place of four
ROCK_MIX = cell([S(1, 5), S(4), S(1, 5), S(4), S(1, 6)], 2, 33)
styles["rock-small"] = boulder_style(ROCK_MIX, form="round", size=1.6)
styles["rock-medium"] = boulder_style(ROCK_MIX, form="angular", size=2.4)
styles["rock-large"] = boulder_style(ROCK_MIX, form="angular", size=3.0)

props_ = [
    # wider than before (note 6): four blocks across the front path, three to the wools
    path("path-front", 51, [[-10, 86], [-10, 72], [-8, 54], [-4, 38], [0, 23]], PAVE, radius=2),
    path("path-wool-a", 52, [[-12, 60], [-24, 62], [-33, 62]], PAVE, radius=2, wander=1),
    path("path-wool-b", 53, [[-6, 75], [8, 74], [25, 74]], PAVE, radius=2, wander=1),
    # boulders on the frontline where the timber stacks stood, and on the mid stone where the engine house did
    boulder("front-1", -11, 27, "rock-medium", 21), boulder("front-2", 5, 29, "rock-small", 22),
    boulder("front-3", -9, 35, "rock-small", 23), boulder("front-4", 12, 25, "rock-medium", 24),
    boulder("mid-1", 5, -4, "rock-large", 26),
    tree("willow-1", -18, 50, "willow", 1),
    tree("willow-mid", -9, -5, "willow-small", 2),
    # two more willows (notes 64, 70): on the west rise's top, and at the terrace's north edge by the stem
    tree("willow-rise", -18, 74, "willow-small", 4),
    tree("willow-terrace", 2, 79, "willow-small", 5),
    flora("regrowth-cover", [[-21, 41], [-12, 41], [-12, 68], [-21, 68]], coverage=0.3, scale=6, fern=0.4,
          flowers=0.03, tall=0.02, seed=8),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 32},
    "themes": {"ash": ash, "regrowth": regrowth, "timber": timber, "post": post, "planks": planks,
               "fence": fence, "ladder-n": ladder_n, "ladder-s": ladder_s},
    "mapTheme": "ash",
    "relief": relief,
    # The outer coasts only. The frontline's face to the band, the wall seams at x -24 and x 12, and the
    # wool rooms' own faces stay as the composer cut them.
    "editShapes": {"frontline-t1-9": coast_edits(GROUND, {
        0: [(0.25, 1), (0.5, 2)],                 # the spur's south coast, west of its wall
        1: [(0.3, 2), (0.7, 3)],                  # the hub's west coast
        3: [(0.3, 2), (0.65, 1)],                 # the frontline's west coast
        5: [(0.4, 2), (0.75, 1)],                 # the frontline's east coast
        7: [(0.25, 2), (0.5, 3), (0.8, 1)],       # the hub's east coast, along the hole
        8: [(0.14, 2)],                           # the east approach's south coast, short of its wall
        16: [(0.5, 2), (0.78, 1)],                # the spur's north coast
    })},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": LODGE, "wool": WOOL_ROOM},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
