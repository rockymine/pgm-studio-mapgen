"""Tanglecleft — writes sonnet55-tanglecleft.plan.json and .refinement.json for the stage in $STAGE (1..4)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (ring, coast_edits, pool, channel, made, patch, path, tree, boulder, house, flora,
                        boulder_style, copied_trees, house_style)
from sonnet55_kit import *
import props

HERE = os.path.dirname(os.path.abspath(__file__))
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
finish = {"created": "2026-09-29", "authors": ["Sonnet 5.5"]}

# --- stage 2: the outline reshaped point by point, the relief, the water. No theme. ---------------------------------
# The ring the plan compiles the team-0 ground to (spawn bench and field fused): edge 2 is the south coast,
# 4 the north coast, 1 and 5 the field's west edges beside the spawn. Edge 3 is the frontline and stays as cut.
GROUND = [[-120, -12], [-100, -12], [-100, -40], [-12, -40], [-12, 40], [-100, 40], [-100, 12], [-120, 12]]
VARIANT = os.environ.get("RELIEF", "d")

BENCH = {"id": "bench", "kind": "area", "h": 21, "bevel": 0, "ring": [[-122, -15], [-97, -15], [-97, 15], [-122, 15]]}
FRONT = {"id": "front", "kind": "area", "h": 11, "bevel": 0, "ring": [[-26, -38], [-12, -38], [-12, 38], [-26, 38]]}
SHELF = {"id": "shelf", "kind": "area", "h": 18, "bevel": 3, "ring": ring(-64, 24, 12, 11, 20, 0.08, 3)}


def relief(variant):
    if variant == "a":      # a dell along the temple's foot, a hill on the north edge, hummocks in the south wood
        marks = [BENCH, FRONT, SHELF,
                 {"id": "dell", "kind": "area", "h": 8, "bevel": 2, "ring": [[-66, -15], [-33, -15], [-33, -1], [-66, -1]]}]
        pushes = [
            {"id": "hill", "ring": ring(-36, 40, 14, 12, 20, 0.1, 3), "amount": 12, "falloff": 14, "crown": 8, "seed": 5},
            {"id": "hum-1", "ring": ring(-80, -22, 9, 7, 16, 0.12, 3), "amount": 5, "falloff": 9, "crown": 0, "seed": 7},
            {"id": "hum-2", "ring": ring(-52, -29, 10, 7, 16, 0.12, 3, 1.0), "amount": 6, "falloff": 9, "crown": 0, "seed": 8},
            {"id": "hum-3", "ring": ring(-76, -38, 12, 5, 16, 0.1, 3), "amount": 6, "falloff": 10, "crown": 0, "seed": 9},
        ]
    elif variant == "d":    # the dell and hill of a, plus a dry cleft running from the south coast to the dell's foot
        marks = [BENCH, FRONT, SHELF,
                 {"id": "dell", "kind": "area", "h": 8, "bevel": 2, "ring": [[-66, -15], [-33, -15], [-33, -1], [-66, -1]]}]
        pushes = [
            {"id": "cleft", "ring": [[-44, -42], [-37, -42], [-37, -27], [-44, -27]], "amount": -6, "falloff": 9, "crown": 0, "seed": 3},
            {"id": "hill", "ring": ring(-36, 40, 14, 12, 20, 0.1, 3), "amount": 12, "falloff": 14, "crown": 8, "seed": 5},
            {"id": "hum-1", "ring": ring(-82, -24, 9, 7, 16, 0.12, 3), "amount": 5, "falloff": 9, "crown": 0, "seed": 7},
            {"id": "hum-2", "ring": ring(-24, -30, 6, 6, 16, 0.12, 3, 1.0), "amount": 4, "falloff": 7, "crown": 0, "seed": 8},
            {"id": "hum-3", "ring": ring(-74, -38, 12, 5, 16, 0.1, 3), "amount": 6, "falloff": 10, "crown": 0, "seed": 9},
        ]
    elif variant == "b":    # a ravine across the field, north to south, with a land bridge under the north hill
        marks = [BENCH, FRONT, SHELF]
        pushes = [
            {"id": "cleft", "ring": [[-44, -40], [-37, -40], [-37, 6], [-44, 6]], "amount": -8, "falloff": 12, "crown": 0, "seed": 3},
            {"id": "hill", "ring": ring(-30, 41, 13, 12, 20, 0.1, 3), "amount": 12, "falloff": 12, "crown": 8, "seed": 5},
            {"id": "hum-1", "ring": ring(-84, -18, 9, 7, 16, 0.12, 3), "amount": 5, "falloff": 9, "crown": 0, "seed": 7},
            {"id": "hum-2", "ring": ring(-72, 4, 9, 7, 16, 0.12, 3, 1.0), "amount": 5, "falloff": 9, "crown": 0, "seed": 8},
        ]
    else:                   # rolling: two long spurs along the lane and no cut at all
        marks = [BENCH, FRONT, SHELF]
        pushes = [
            {"id": "spur-s", "ring": [[-90, -40], [-40, -40], [-40, -30], [-90, -30]], "amount": 9, "falloff": 12, "crown": 5, "seed": 5},
            {"id": "spur-n", "ring": [[-84, 38], [-30, 38], [-30, 46], [-84, 46]], "amount": 9, "falloff": 12, "crown": 5, "seed": 6},
            {"id": "knoll", "ring": ring(-48, -8, 10, 8, 16, 0.12, 3), "amount": 4, "falloff": 9, "crown": 0, "seed": 7},
        ]
    return {"team": {"base": 12, "reach": 0, "step": 1, "landform": "hills", "marks": marks, "pushes": pushes}}


if STAGE >= 2:
    finish["relief"] = relief(VARIANT)
    finish["editShapes"] = {"field-12": coast_edits(GROUND, {
        1: [(0.35, 3), (0.7, 6)],
        2: [(0.10, 1), (0.22, 4), (0.34, 2), (0.47, 5), (0.60, 1), (0.72, 4), (0.86, 2)],
        4: [(0.12, 2), (0.25, 5), (0.40, 2), (0.55, 4), (0.70, 1), (0.85, 4)],
        5: [(0.30, 5), (0.65, 2)],
    })}
    finish["dressing"] = {"styles": {}, "props": [] if VARIANT not in ("a", "d") else [
        channel("brook", [[-34, -8], [-42, -8], [-48, -8]], radius=2.5, depth=2, shore=0),
        pool("lagoon", ring(-54, -8, 6, 4, 12, 0.05, 3), depth=2, shelf=2, shore=0),
    ]}



# --- stage 3: made things on layers, the biome, the themes finished by angle, patches, room styles --------------------
# Three families, named before any theme: the GROUND is green — turf over dirt and coarse dirt, rock where it is
# too steep for either; what is BUILT is pale grey stone brick with a faint mossy vein; the ACCENT is jungle wood,
# which the bridge, the trails and the spawn's timbers all share.
if STAGE >= 3:
    TURF = noise([cell([S(DIRT, 0), S(*COARSE)], 2, 7), S(GRASS), S(GRASS), S(GRASS), S(GRASS)],
                 scale=2, seed=11)
    SOIL = cell([S(DIRT, 0), S(*COARSE)], 2, 5)
    EARTH = cell([S(DIRT, 0), S(*COARSE), S(DIRT, 0), S(*PODZOL)], 2, 6)
    SOILR = cell([S(DIRT, 0), S(*COARSE)], 2, 5, rise=2)
    STRATA = [(SOILR, 2), (ROCK, 5), (cell([S(*ANDESITE), S(STONE)], 2, 3, rise=2), 2), (ROCK, 4)] * 9
    jungle = theme(
        by_slope((44, depth(TURF, SOIL)), (8, depth(EARTH, SOIL)), (38, ROCK)),
        wall=beds(STRATA, start=-40, reach=16, beyond=ROCK),
        fill=beds(STRATA, start=-40, reach=16, beyond=ROCK))
    BRICK4 = cell([S(BRICKS), S(BRICKS), S(*POL_ANDESITE), S(*ANDESITE), S(BRICKS), S(BRICKS, 1)], 2, 21, rise=2)
    temple = one(BRICK4)
    timber = one(cell([S(*JUNGLE_PLANK), S(*JUNGLE_PLANK), S(*SPRUCE_PLANK)], 2, 22, rise=2))
    bed = theme(cell([S(GRAVEL), S(*ANDESITE), S(*COARSE), S(GRAVEL)], 2, 31), wall=ROCK, fill=ROCK, depth_=2)
    finish["biome"] = {"kind": "solid", "id": 21}
    finish["themes"] = {"jungle": jungle, "temple": temple, "timber": timber, "bed": bed}
    finish["mapTheme"] = "jungle"
    finish["addShapes"] = [patch("cleft-bed", [[-46, -36], [-36.5, -36], [-36.5, -27], [-46, -27]], "bed", 12, group="team")]

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

    finish["roomStyles"] = {"spawn": repaint(shipped("talltimber-hall"), solids={(17, 1): JUNGLE_LOG, (17, 0): JUNGLE_LOG,
                                                                              (5, 1): JUNGLE_PLANK}, beams=JUNGLE_LOG),
                            "wool": "@sb-spawn"}

# --- stage 4: dressing — paths first (the circulation), then ground cover, then trees, rocks and a cabin ---------------
if STAGE >= 4:
    PAVE = cell([S(DIRT, 0), S(*COARSE), S(*JUNGLE_PLANK), S(*COARSE)], 2, 21)
    BANK = cell([S(GRAVEL), S(*COARSE), S(CLAY), S(GRAVEL)], 2, 9)
    props_ = [p_ for p_ in finish["dressing"]["props"]]
    for p_ in props_:
        p_["bank"] = BANK
    props_ += [
        # spawn door to the monument, through the second gap in the terrace lip
        path("path-spawn", 51, [[-99, 1], [-90, 5], [-80, 9], [-70, 12], [-70, 17], [-69, 21]], PAVE, wander=1),
        # spawn door through the south wood to the cleft bridge, and on from its east end to the front
        path("path-south-w", 52, [[-99, -2], [-93, -10], [-84, -20], [-74, -28], [-64, -32], [-58, -33]], PAVE),
        path("path-south-e", 53, [[-31, -33], [-26, -28], [-20, -20], [-16, -14]], PAVE, wander=1),
        # the band's way up to the terrace, south of the hill and north of the dell
        path("path-front", 54, [[-16, 8], [-26, 11], [-38, 13], [-50, 15], [-60, 16]], PAVE),
        flora("floor-cover", [[-120, -12], [-100, -12], [-100, -40], [-12, -40], [-12, 40], [-100, 40], [-100, 12], [-120, 12]],
              coverage=0.3, scale=9, fern=0.5, flowers=0.04, flower_scale=10, tall=0.03, seed=5),
    ]
    finish["dressing"]["props"] = props_

    # Two species, and never three: jungle giants (library row r16) and, under them, dark oak (row r5). Every site was
    # read off the seats mask after the paths were in, and each stands at least its crown and its neighbour's apart.
    JUNGLE = [f"tree-showcase-r16-{i}" for i in range(1, 7)]
    OAK = [f"tree-showcase-r5-{i}" for i in (1, 2, 3)]
    styles = dict(copied_trees(HERE, JUNGLE + OAK))
    styles["rock"] = boulder_style(cell([S(STONE), S(*ANDESITE), S(COBBLE), S(*ANDESITE)], 2, 8), "outcrop", 3)
    styles["wet-rock"] = boulder_style(cell([S(STONE), S(*ANDESITE), S(COBBLE), S(*ANDESITE)], 2, 9), "outcrop", 3, mossy=True)
    styles["cabin"] = {"kind": "house", "shell": repaint(
        shipped("talltimber-cottage"), solids={(17, 1): JUNGLE_LOG, (17, 0): JUNGLE_PLANK, (17, 2): (5, 0), (5, 5): (5, 5)},
        beams=JUNGLE_LOG)}
    finish["dressing"]["styles"] = styles
    props_ += [
        tree("j-1", -90, -30, JUNGLE[0], 1), tree("j-2", -76, -36, JUNGLE[3], 2), tree("j-3", -60, -26, JUNGLE[1], 3),
        tree("j-4", -76, -14, JUNGLE[4], 4), tree("j-5", -44, -18, JUNGLE[2], 5), tree("j-6", -31, -24, JUNGLE[5], 6),
                tree("o-1", -66, -7, OAK[0], 8), tree("o-2", -80, 2, OAK[1], 9), tree("o-3", -26, -2, OAK[2], 10),
        tree("o-4", -48, 31, OAK[0], 11),
        boulder("b-1", -30, -17, "wet-rock", 1), boulder("b-2", -24, -10, "wet-rock", 2), boulder("b-3", -70, -12, "rock", 3),
        boulder("b-4", -91, -23, "rock", 4), boulder("b-5", -72, -2, "rock", 5),
        house("cabin", "cabin", [[-64, -20], [-55, -13]], front="negZ", seed=21),
    ]
    finish["dressing"]["props"] = props_

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG, "stage", STAGE)
