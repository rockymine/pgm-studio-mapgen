#!/usr/bin/env python3
"""opus5c-culvergate — capture the points. The approach dimension is THROUGH.

A brick waterworks fought room by room. The middle point stands inside a long
engine hall divided into three rooms by cross-walls whose doors are on opposite
hands, so crossing it is a zigzag and every room is entered at a known door;
the two flank points stand in settling yards walled on three sides with one
mouth apiece. The hall's roof and the gantries out to the yards are a second
storey, so two players heading for the same point need never meet until one of
them arrives.

The middle pays two against the flanks' one. A board whose points all pay alike
is a board two teams settle by taking one each and standing on them.

Tone families: the ground is pale limestone flags — made ground, not landscape
— what is built is red brick under dark slate, and the accent is the iron white
of the cover.

Writes opus5c-culvergate.plan.json and opus5c-culvergate.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from opus5c import (solid, cells, field, voronoi, band, stack, soil,
                    wander_rect, write)

SLUG = "opus5c-culvergate"
CELL = 4

# ---------------------------------------------------------------- the plan
#
#   works-mid  x -36..36   z -28..28    the neutral floor
#   works-w    x -52..-36  z -12..12    the arm the west yard stands on
#   works-e    x  36..52   z -12..12
#   approach   x -16..16   z  28..44    the way out of the spawn
#   spawn      x  -8..8    z  44..68    16 x 24, inside ST10's cap
#
# The spawn is 16 wide rather than 20 because it has to be CENTRED on x 0: an
# off-centre spawn puts the two flank points at different walks from the two
# teams, and fairness on a capture board is a property of the board's symmetry
# rather than of any measurement. A 20-block piece cannot be centred on a
# 4-block cell grid; 16 can.
#
# The points sit one dead centre and the rest to the sides, and "the sides"
# means across the line between the spawns rather than along it — the only
# positions that are the same walk for everyone. At x +/-44 on a centre-to-spawn
# distance of 56 they stand at 0.79 of it, which is the top of the corpus's
# 0.52-0.88 range: a pair close to the middle is a pair the team holding the
# middle also covers, and three points collapse back into one place.
#
# There is no void and no build zone. A capture board is one landmass — its
# ground is built rather than landscape, and a works is a floor.
#
# The works is FANNED like everything else, though it is the neutral middle.
# Stated `mirrors: false` it refuses at PL12 — a non-fanned piece must form its
# own island and this one touches both approaches — and fanning costs nothing
# here, because a rectangle centred on the symmetry centre is its own rot_180
# image.
#
# And it is a cross rather than a rectangle. Drawn 104 by 56 it carried four
# corners behind the yards that no journey reached — 727 cells, 9.3% of the
# board — and on a capture board a dead share is a fault rather than a note. A
# second mouth into each yard and a road round the back moved it by nothing at
# all: coverage measures journeys between waypoints, a journey takes the short
# way, and an alternative route is invisible to it. The arms stop where the
# yards do, which is the only thing that answered.

SPAWN_AT = (0, 56)
CENTRE = (0, 0)
FLANK_X = 44

plan = {
    "plan": 2,
    "meta": {"name": "Culvergate"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": 9},
    "pieces": [
        {"id": "works-mid", "role": "piece", "rect": [-9, -7, 18, 14],
         "surface": 9},
        {"id": "works-w", "role": "piece", "rect": [-13, -3, 4, 6],
         "surface": 9},
        {"id": "works-e", "role": "piece", "rect": [9, -3, 4, 6],
         "surface": 9},
        {"id": "approach", "role": "piece", "rect": [-4, 7, 8, 4], "surface": 9},
        {"id": "spawn", "role": "spawn", "rect": [-2, 11, 4, 6], "surface": 9},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-gate", "piece": "spawn",
                    "at": [8, 13], "facing": "front",
                    "footprint": [3, 7, 10, 12]}],
        "wools": [],
        "iron": [{"id": "iron-gate", "piece": "spawn", "at": [8.0, 3.5]}],
        "destroyables": [],
        "cores": [],
        # The plan states the COUNT and the finish states the geometry. PL3
        # counts the capture points a board states a count of, so a koth board
        # that says nothing here is a board with no objective at the plan tier.
        "controlPoints": 3,
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# There is none, and that is the decision rather than an omission. A capture
# board is a control game: its ground is built — plazas, yards, decks, walls —
# and relief is a blunt instrument beside a wall somebody placed on purpose. A
# board that answers the gamemode's name literally and stands its points on a
# hill has already lost the game the mode is about, because the first team onto
# a high pad keeps it.
#
# So the field is constant at the board's own surface, every cell of it is
# level, and every height on this board is a course somebody laid.

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "plain",
        "marks": [], "pushes": [],
    }
}

# ---------------------------------------------------------------- the works
#
# The floor's top block is y8, so every layer standing on it has base_y 9. The
# walls run six courses to a segment top of 15 and the roof rests at 15, which
# is the seam a layer's inclusive span makes: one lower is SK10 and the slab is
# absorbed into the layer under it.

FLOOR_Y, ROOF_Y = 9, 15

BRICK = solid(45, 0)
STONE = solid(1, 0)
STONE_BRICK = solid(98, 0)
ANDESITE = solid(1, 5)
ANDESITE_P = solid(1, 6)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
CLAY = solid(82, 0)
QUARTZ = solid(155, 0)
DARKOAK = solid(5, 5)

BRICKWORK = cells(5701, 5, 3, [BRICK, solid(45, 0), STONE_BRICK])
SLATE = cells(5702, 4, 2, [ANDESITE, ANDESITE_P])
IRONWHITE = cells(5703, 3, 1, [QUARTZ, STONE_BRICK])
GANTRY = cells(5704, 4, 2, [DARKOAK, BRICK])


def slab(sid, x0, z0, x1, z1, material, height, floor=0):
    return {"id": sid, "type": "rectangle", "operation": "add", "floor": floor,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "base_height": height, "material": material, "keepClear": True}


# The engine hall: a shell with one mouth a side, and two cross-walls whose
# doors are on opposite hands — so a player crossing it goes north to pass the
# first and south to pass the second, and each of the three rooms is entered at
# a door the defence knows. Each cross-wall is the rot_180 image of the other,
# which is what keeps the zigzag the same for both teams.
hall = [
    slab("hall-n-w", -32, 8, -4, 10, BRICKWORK, 6),
    slab("hall-n-e", 4, 8, 32, 10, BRICKWORK, 6),
    slab("hall-s-w", -32, -10, -4, -8, BRICKWORK, 6),
    slab("hall-s-e", 4, -10, 32, -8, BRICKWORK, 6),
    slab("hall-w-s", -32, -10, -30, -4, BRICKWORK, 6),
    slab("hall-w-n", -32, 4, -30, 10, BRICKWORK, 6),
    slab("hall-e-s", 30, -10, 32, -4, BRICKWORK, 6),
    slab("hall-e-n", 30, 4, 32, 10, BRICKWORK, 6),
    slab("bay-w", -18, -10, -16, 2, BRICKWORK, 6),
    slab("bay-e", 16, -2, 18, 10, BRICKWORK, 6),
]

# The settling yards: walled on two of their four sides, with a mouth facing
# the hall and a second in the outer long wall. Coverage read the works' four
# corners as 708 dead cells behind the yards, and on a capture board a dead
# share is a fault rather than a note — every part of the board is there to
# offer a different way toward a point. The second mouth is what makes the
# corner one. A
# pad tucked into a corner of the structure takes approaches away deliberately,
# so the ones that remain are the ones the board wants players in — and it is
# still the same walk from both spawns, because the structure is mirrored too.
yards = [
    slab("yard-w-w", -52, -12, -50, 12, BRICKWORK, 6),
    # the outer long wall carries a SECOND mouth at x -46..-42, which is what
    # turns the works' corner behind the yard from dead ground into an approach
    slab("yard-w-n-a", -52, 10, -46, 12, BRICKWORK, 6),
    slab("yard-w-n-b", -42, 10, -36, 12, BRICKWORK, 6),
    slab("yard-w-s", -52, -12, -36, -10, BRICKWORK, 6),
    slab("yard-e-e", 50, -12, 52, 12, BRICKWORK, 6),
    slab("yard-e-s-a", 46, -12, 52, -10, BRICKWORK, 6),
    slab("yard-e-s-b", 36, -12, 42, -10, BRICKWORK, 6),
    slab("yard-e-n", 36, 10, 52, 12, BRICKWORK, 6),
]

# Large cover: a pillar ten blocks across that a player goes round from two
# sides is not an obstacle, it is a decision — it splits the approach into two
# and hides each from the other. One stands in each team's own approach.
pillars = [
    slab("pillar-n", -6, 18, 4, 26, BRICKWORK, 6),
    slab("pillar-s", -4, -26, 6, -18, BRICKWORK, 6),
]

works_walls = {
    "id": "works-walls", "name": "the works' walls", "base_y": FLOOR_Y,
    "kind": "made", "part_of": "works-mid",
    "groups": [{"id": "works-walls", "name": "the works' walls",
                "mirrors": False,
                "shapeIds": [s["id"] for s in hall + yards + pillars]}],
    "shapes": hall + yards + pillars,
}

# Small cover: boxes two and three courses tall that a player crouches behind,
# stands on or shoots over. These go INSIDE the spaces, the hall's rooms
# included, because an open room with nothing in it is a room nobody crosses.
# Every one is authored with its rot_180 partner.
cover_boxes = [
    slab("cover-mid-w", -8, -4, -5, -1, IRONWHITE, 3),
    slab("cover-mid-e", 5, 1, 8, 4, IRONWHITE, 3),
    slab("cover-hall-w", -26, 2, -23, 5, IRONWHITE, 2),
    slab("cover-hall-e", 23, -5, 26, -2, IRONWHITE, 2),
    slab("cover-yard-w", -46, 6, -43, 9, IRONWHITE, 3),
    slab("cover-yard-e", 43, -9, 46, -6, IRONWHITE, 3),
    slab("cover-floor-w", -38, -16, -35, -13, IRONWHITE, 2),
    slab("cover-floor-e", 35, 13, 38, 16, IRONWHITE, 2),
    slab("cover-appr-w", -14, 16, -11, 19, IRONWHITE, 2),
    slab("cover-appr-e", 11, -19, 14, -16, IRONWHITE, 2),
]

works_cover = {
    "id": "works-cover", "name": "the works' cover", "base_y": FLOOR_Y,
    "kind": "made", "part_of": "works-mid",
    "groups": [{"id": "works-cover", "name": "the works' cover",
                "mirrors": False,
                "shapeIds": [s["id"] for s in cover_boxes]}],
    "shapes": cover_boxes,
}

# The roof and the two gantries, one course at the walls' own segment top. The
# gantry crosses four blocks of open floor on nothing at all before it reaches
# the yard's west wall, which is what a layer boundary buys: the painter writes
# each layer over its own span only, so the air under a deck stays air.
upper = [
    slab("hall-roof", -32, -10, 32, 10, SLATE, 1),
    slab("gantry-w", -52, -4, -32, 4, GANTRY, 1),
    slab("gantry-e", 32, -4, 52, 4, GANTRY, 1),
]

works_upper = {
    "id": "works-upper", "name": "the roof and the gantries", "base_y": ROOF_Y,
    "kind": "made", "part_of": "works-mid",
    "groups": [{"id": "works-upper", "name": "the roof and the gantries",
                "mirrors": False,
                "shapeIds": [s["id"] for s in upper]}],
    "shapes": upper,
}

# ---------------------------------------------------------------- the paint

flags_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5711, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": cells(5712, 6, 4, [STONE, STONE_BRICK, ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONE_BRICK},
    "rimEdges": "void",
    # A depth stack rather than a slope stack, because the slope axis answers a
    # landform's question and this board has no landform: every cell of it is
    # level and the only faces on it are courses somebody laid.
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5713, 6, 0, [STONE, STONE_BRICK,
                                                    ANDESITE]), STONE)},
}

settling_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5714, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": cells(5715, 6, 4, [STONE, ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": STONE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5716, 5, 0, [CLAY, GRAVEL, STONE]),
                                 STONE)},
}

garth_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5717, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": cells(5718, 6, 4, [COBBLE, STONE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5719, 5, 0, [COBBLE, GRAVEL, DARKOAK]),
                                 STONE)},
}

# ---------------------------------------------------------------- the shapes

GROUND = 9

add_shapes = [
    # the two settling beds, marked with shapes so the yards read as what they
    # are rather than as more of the works' floor
    {"id": "bed-west", "type": "rectangle", "operation": "add", "floor": 0,
     "min_x": -50, "min_z": -10, "max_x": -36, "max_z": 10,
     "base_height": GROUND, "theme": "settling"},
    {"id": "bed-east", "type": "rectangle", "operation": "add", "floor": 0,
     "min_x": 36, "min_z": -10, "max_x": 50, "max_z": 10,
     "base_height": GROUND, "theme": "settling"},
    {"id": "garth-north", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "garth",
     "vertices": wander_rect(-10, 46, 10, 66, wobble=1.5, seed=5721)},
    {"id": "garth-south", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "garth",
     "vertices": wander_rect(-10, -66, 10, -46, wobble=1.5, seed=5722)},

    # The two flights onto the hall's roof, one a team, each the rot_180 image
    # of the other. height_mode level with anchor_heights, skirt 0, keepClear
    # and a MATERIAL rather than a theme — a stair is a thing somebody built.
    # It runs 16 blocks for a rise of 7, which is over twice the run the rise
    # wants, and its head stands one course over the roof's own edge.
    {"id": "stair-nw", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "height_mode": "level", "skirt": 0,
     "keepClear": True, "anchor_heights": [9, 9, 16, 16],
     "material": cells(5723, 4, 2, [STONE_BRICK, STONE, ANDESITE]),
     "vertices": [[-28, 26], [-20, 26], [-20, 10], [-28, 10]]},
    {"id": "stair-se", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "height_mode": "level", "skirt": 0,
     "keepClear": True, "anchor_heights": [9, 9, 16, 16],
     "material": cells(5723, 4, 2, [STONE_BRICK, STONE, ANDESITE]),
     "vertices": [[28, -26], [20, -26], [20, -10], [28, -10]]},
]

# ---------------------------------------------------------------- the dressing
#
# Cover on a capture board is BUILT — boxes, pillars, walls, things with faces
# placed where a sightline needs breaking — and natural dressing strewn over
# open ground looks like cover and works like decoration, because nothing
# decided where it went. So this board carries no tree, no boulder and no
# flora, and its cover is the two layers above.
#
# What it does carry is the circulation, drawn before anything else: the way out
# of each spawn, and the way along the works to each yard's mouth.

PAVE = cells(5731, 3, 0, [GRAVEL, ANDESITE, COBBLE])

props = [
    {"id": "gate-way-n", "kind": "stroke", "seed": 5741, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[0, 46], [0, 34], [-8, 24], [-14, 14], [-14, 2]]},
    {"id": "gate-way-s", "kind": "stroke", "seed": 5742, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[0, -46], [0, -34], [8, -24], [14, -14], [14, -2]]},
    {"id": "yard-way-w", "kind": "stroke", "seed": 5743, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-30, -14], [-36, -6], [-40, 0], [-44, 2]]},
    {"id": "back-way-w", "kind": "stroke", "seed": 5745, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-22, 13], [-32, 14], [-42, 14], [-45, 13]]},
    {"id": "yard-way-e", "kind": "stroke", "seed": 5744, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[30, 14], [36, 6], [40, 0], [44, -2]]},
    {"id": "back-way-e", "kind": "stroke", "seed": 5746, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[22, -13], [32, -14], [42, -14], [45, -13]]},
]



TANK_BANK = cells(5761, 4, 0, [CLAY, GRAVEL, STONE])


def tank(tid, x0, z0, x1, z1):
    return {"id": tid, "kind": "water", "seed": 5760 + len(tid), "shape": "pool",
            "points": wander_rect(x0, z0, x1, z1, wobble=1.2, seed=5762),
            "radius": 2, "depth": 3, "level": 7, "shore": 1,
            "bank": TANK_BANK}


props += [
    tank("tank-n", 14, 16, 30, 26),
    tank("tank-s", -30, -26, -14, -16),
]

# ---------------------------------------------------------------- the house
#
# One structure only: the spawn hall, which is the one building a player sees
# from the inside. The ground is pale limestone flags, so the hall is red brick
# under dark slate — a building has to read as a built thing from across the
# works, which means its walls are not in the family under its feet.

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

GATE_STOREY = {
    "clear": 7,
    "wall": {"stack": {"bands": [
        {"material": STONE_BRICK, "thickness": 1},
        {"material": cells(5751, 4, 2, [BRICK, QUARTZ]), "thickness": 5},
        {"material": {"kind": "laidLog", "id": 17, "data": 0}, "thickness": 1}],
        "ending": "repeat"},
        "extent": 7},
    "post": solid(17, 0),
    "windows": {"form": "arched", "block": 108, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN, "deck": None, "headroom": 7,
}

GATE_HALL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONE_BRICK,
                                       "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN,
        # null is the answer rather than an omission: a footing is what a DEEP
        # plate stands on, and over one course it is a rim round a building
        # with no foundation to speak of
        "footing": None},
    "roof": {"form": "hip", "pitch": 2, "slab": 44, "slabData": 3,
             "overhang": 1, "ridgeCap": False, "hole": False,
             "body": COBBLE, "verge": STONE_BRICK, "gable": None,
             "gableWindows": NO_WINDOW},
    "wall": {"stack": {"bands": [{"material": STONE_BRICK, "thickness": 1}],
                       "ending": "repeat"}, "extent": 7},
    "post": solid(17, 0),
    "windows": NO_WINDOW,
    "storeys": [GATE_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 0, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 108, "fill": "upperSlab",
                         "fillBlock": 44, "fillData": 4},
                "width": 2, "height": 3},
}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"flags": flags_theme, "settling": settling_theme,
               "garth": garth_theme},
    "mapTheme": "flags",
    # Plains: almost nothing on this board is tinted, because almost nothing on
    # it is grass, leaf or water — a works is a floor and its colour is stated.
    "biome": {"kind": "solid", "id": 1},
    "relief": relief,
    "addShapes": add_shapes,
    # in base_y order, which is the order the world builds them in
    "addLayers": [works_walls, works_cover, works_upper],
    "roomStyles": {"spawn": GATE_HALL, "wool": GATE_HALL},
    "dressing": {"props": props},
    # Every point of the board is stated here, already fanned: the intent
    # carries no symmetry, so a centre plus one side would be a two-hill board.
    # The middle pays two against the flanks' one, which is the corpus's own
    # ratio and what puts a reason to leave a held point back into the match.
    "controlPoints": [
        {"name": "The Cistern", "anchor": {"x": CENTRE[0], "y": 8,
                                           "z": CENTRE[1]},
         "size": 8, "points": 2},
        {"name": "West Settling", "anchor": {"x": -FLANK_X, "y": 8, "z": 0},
         "size": 8, "points": 1},
        {"name": "East Settling", "anchor": {"x": FLANK_X, "y": 8, "z": 0},
         "size": 8, "points": 1},
    ],
    "scoreLimit": 750,
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
