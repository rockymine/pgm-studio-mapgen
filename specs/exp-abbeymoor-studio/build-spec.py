#!/usr/bin/env python3
"""Abbeymoor — a destroy-the-monument board for two teams of sixteen, two monuments a team: a high moor where each
team holds the hill of a ruined abbey, with an orchard village below it, and a peat bog with standing stones
between the two sides, joined by land. Under each abbey a crypt, and a passage from it that comes up in the
village well beside the village monument. Written for the experiment (exp-abbeymoor-studio).

Unit = team 0 on the north (z < 0); rot_180 fans the south side. The bog is the neutral piece on the axis.
  moor 38 (spawn)  ->  abbey hill 46 (crown flat, ruins + crypt under it)  ->  village terrace 34  ->
  orchard terraces 28, 22  ->  the bog 20 on the axis.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import showcase  # noqa: E402

SLUG = "exp-abbeymoor-studio"
C = 4

BOG, MOOR, PLAT, TERR, ORCH1, ORCH2 = 20, 38, 46, 34, 27, 22
X0, X1, Z0, Z1 = -56, 56, -120, -24


def cells(x0, z0, x1, z1):
    assert all(v % C == 0 for v in (x0, z0, x1, z1)), (x0, z0, x1, z1)
    return [x0 // C, z0 // C, (x1 - x0) // C, (z1 - z0) // C]


# ── the plan: arrangement only. The ground is the relief's. ─────────────────────────────
SPAWN = (-16, -120, 12, -100)
pieces = [{"id": "spawn", "role": "spawn", "rect": cells(*SPAWN), "surface": MOOR}]
# the moor: everything else in the unit, as rectangles around the spawn piece
moor_rects = [(X0, Z0, SPAWN[0], SPAWN[3]), (SPAWN[2], Z0, X1, SPAWN[3]), (X0, SPAWN[3], X1, Z1)]
for i, r in enumerate(moor_rects):
    pieces.append({"id": f"moor-{i + 1}", "role": "piece", "rect": cells(*r), "surface": MOOR})
pieces.append({"id": "bog", "role": "piece", "rect": cells(X0, -24, X1, 0), "surface": BOG})

plan = {
    "plan": 2,
    "meta": {"name": "Abbeymoor"},
    "globals": {"cell": C, "symmetry": "rot_180", "maxPlayers": 16, "surface": MOOR},
    "pieces": pieces,
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [14, 8], "facing": "back", "footprint": [4, 1, 20, 15]}],
        "iron": [{"id": "iron-1", "piece": "spawn", "at": [1.5, 4.5]}],
        # the two monuments, stated as absolute block positions (no plan piece carries them)
        "destroyables": [
            {"id": "abbey-monument", "piece": "", "at": [-24, -69], "style": "pillar-3", "materials": "obsidian",
             "float": 3, "name": "Abbey Monument"},
            {"id": "village-monument", "piece": "", "at": [30, -62], "style": "pillar-3", "materials": "obsidian",
             "float": 4, "name": "Village Monument"},
        ],
    },
}


# ── materials ────────────────────────────────────────────────────────────────────────
def S(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


STONE, ANDESITE, POLISHED, COBBLE, MOSSY = S(1), S(1, 5), S(1, 6), S(4), S(48)
GRASS, DIRT, COARSE, PODZOL, GRAVEL = S(2), S(3), S(3, 1), S(3, 2), S(13)
SBRICK, SBRICK_MOSS, SBRICK_CRACK = S(98), S(98, 1), S(98, 2)


def cell(seed, size, palette, jitter=60, warp=3, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def noise(seed, scale, stops, octaves=2, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops, "rise": rise}


def depth_stack(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def strata():
    beds = [(ANDESITE, 2), (STONE, 3), (POLISHED, 1), (STONE, 2), (ANDESITE, 3), (COBBLE, 1), (STONE, 2)]
    return {"kind": "layered", "axis": "height", "from": -10, "follow": 100, "reach": 16, "beyond": STONE,
            "stack": {"ending": "handOver", "bands": [{"material": m, "thickness": t} for m, t in beds]}}


ROCK = cell(21, 4, [STONE, ANDESITE, STONE, COBBLE, ANDESITE, POLISHED], jitter=70, warp=4)

# moor: grass to 30 degrees with dry coarse-dirt patches inside it, a worn shoulder, then grey rock
MOOR_TOP = slope_stack(
    (depth_stack((noise(22, 4, [COARSE, GRASS, GRASS, GRASS, COARSE]), 1), (DIRT, 2)), 30),
    (depth_stack((cell(23, 3, [DIRT, COARSE, DIRT, COARSE]), 1), (DIRT, 2)), 10),
    (ROCK, 50))
# the bog: dark, wet — podzol and coarse dirt with dirt, no grass worth the name
BOG_TOP = slope_stack(
    (depth_stack((noise(24, 4, [PODZOL, COARSE, PODZOL, PODZOL, DIRT]), 1), (DIRT, 2)), 35),
    (ROCK, 55))
# the abbey's floor and the village square: laid paving, a built floor of one tone
PAVING = cell(25, 3, [SBRICK, POLISHED, ANDESITE, STONE], jitter=50, warp=2)
HARD_PATH = cell(26, 3, [GRAVEL, ANDESITE, COBBLE], jitter=40, warp=2)
SOFT_PATH = cell(27, 3, [DIRT, COARSE, S(5, 1)], jitter=40, warp=2)


def theme(top, depth=3):
    return {"rimEdges": "void", "rim": {"material": cell(28, 3, [ANDESITE, STONE, POLISHED]), "depth": 1, "enabled": True},
            "surface": {"material": top, "depth": depth, "enabled": True},
            "wall": strata(), "wallEnabled": True, "fill": strata()}


themes = {
    "moor": theme(MOOR_TOP),
    "bog": theme(BOG_TOP),
    "peat": theme(slope_stack(
        (depth_stack((noise(33, 3, [PODZOL, PODZOL, COARSE, S(3, 0), PODZOL]), 1), (DIRT, 2)), 35),
        (ROCK, 55))),
    "plot": theme(slope_stack(
        (depth_stack((cell(36, 3, [S(60, 7), S(60, 7), COARSE, S(60, 7)], jitter=30, warp=1), 1), (DIRT, 2)), 33),
        (ROCK, 55))),
    "heath": theme(slope_stack(
        (depth_stack((noise(34, 3, [PODZOL, GRASS, COARSE, GRASS, PODZOL, GRASS]), 1), (DIRT, 2)), 33),
        (ROCK, 55))),
}


# ── relief ───────────────────────────────────────────────────────────────────────────
def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def blob_ring(cx, cz, rx, rz, n=10, turn=0.0):
    return [[round(cx + rx * math.cos(2 * math.pi * k / n + turn)), round(cz + rz * math.sin(2 * math.pi * k / n + turn))]
            for k in range(n)]


PLATFORM = [[-44, -92], [-38, -97], [-26, -98], [-14, -97], [-6, -94], [-3, -86], [-4, -76], [-6, -68], [-14, -65],
            [-28, -64], [-38, -66], [-43, -72], [-45, -82]]
VILLAGE = [[-2, -88], [10, -91], [26, -92], [42, -91], [53, -88], [56, -82], [56, -64], [54, -58], [44, -56], [30, -57],
           [16, -55], [4, -57], [-2, -58]]
ORCH1_RING = [[-2, -49], [10, -50], [24, -48], [40, -50], [56, -49], [56, -41], [44, -40], [30, -42], [16, -40], [4, -42], [-2, -41]]
ORCH2_RING = [[-2, -34], [12, -35], [26, -33], [40, -35], [56, -34], [56, -28], [42, -27], [28, -29], [14, -27], [0, -29], [-2, -28]]
BOG_RING = [[-56, -22], [-46, -29], [-34, -26], [-24, -32], [-10, -26], [2, -33], [14, -27], [26, -31], [38, -26], [48, -29], [56, -22], [56, 0], [-56, 0]]
POND = blob_ring(40, -108, 4, 3, 9, 0.3)

team_marks = [
    {"id": "moor-n", "kind": "area", "ring": rect_ring(-56, -120, 56, -96), "h": MOOR},
    # the moor rolls: a knoll in the north-east corner, the pond's hollow beside the grange
    {"id": "knoll-e", "kind": "area", "ring": blob_ring(49, -97, 7, 4, 9), "h": 41, "bevel": 6},
    {"id": "pond", "kind": "area", "ring": POND, "h": 33, "bevel": 4},
    {"id": "platform", "kind": "area", "ring": PLATFORM, "h": PLAT},
    {"id": "cliff-e", "kind": "scarp", "points": [[-6, -98], [-2, -92], [-4, -85], [-4, -76], [-7, -70], [-4, -64]],
     "high": PLAT, "low": TERR, "face": 3, "band": 2},
    {"id": "village", "kind": "area", "ring": VILLAGE, "h": TERR},
    {"id": "s-orch1", "kind": "scarp", "points": [[56, -53], [42, -54], [28, -52], [14, -54], [2, -52], [-2, -53]],
     "high": TERR, "low": ORCH1, "face": 5, "band": 2},
    {"id": "orch1", "kind": "area", "ring": ORCH1_RING, "h": ORCH1},
    {"id": "s-orch2", "kind": "scarp", "points": [[56, -38], [42, -39], [28, -37], [14, -39], [2, -37], [-2, -38]],
     "high": ORCH1, "low": ORCH2, "face": 5, "band": 2},
    {"id": "orch2", "kind": "area", "ring": ORCH2_RING, "h": ORCH2},
    {"id": "bog-edge", "kind": "area", "ring": BOG_RING, "h": BOG},
    # the bog is a basin: its two ends climb to the moor, and two hummocks stand in it
    {"id": "rise-w", "kind": "area", "ring": blob_ring(-53, -9, 6, 10, 10), "h": 26, "bevel": 5},
    {"id": "rise-e", "kind": "area", "ring": blob_ring(53, -10, 6, 9, 10, 0.3), "h": 25, "bevel": 5},
    {"id": "hummock-1", "kind": "area", "ring": blob_ring(-4, -22, 5, 3, 9), "h": 22, "bevel": 4},
    {"id": "hummock-2", "kind": "area", "ring": blob_ring(44, -18, 5, 3, 9, 0.5), "h": 22, "bevel": 4},
    # shelves on the abbey hill's south flank, so the flank is not one plane
    {"id": "shelf-w", "kind": "area", "ring": blob_ring(-38, -48, 8, 5, 10, 0.4), "h": 36, "bevel": 6},
    {"id": "shelf-sw", "kind": "area", "ring": blob_ring(-49, -36, 6, 4, 9), "h": 28, "bevel": 5},
    # the road from the bog up the orchard terraces to the village
    {"id": "ramp-orchard", "kind": "line", "r": 4, "tread": 2, "points": [[8, -26], [8, -38], [8, -50], [8, -58]],
     "h": [ORCH2, ORCH2, ORCH1, TERR]},
    # the hill's road: from the bog up the abbey hill's south face to the forecourt
    {"id": "ramp-abbey", "kind": "line", "r": 4, "tread": 2, "points": [[-30, -28], [-34, -46], [-30, -60], [-24, -66]],
     "h": [BOG + 2, 32, 42, PLAT]},
]
def grown(ring, by):
    cx = sum(p[0] for p in ring) / len(ring); cz = sum(p[1] for p in ring) / len(ring)
    out = []
    for x, z in ring:
        d = math.hypot(x - cx, z - cz)
        out.append([round(x + (x - cx) / d * by), round(z + (z - cz) / d * by)])
    return out


POOL_A = [[-34, -14], [-22, -17], [-12, -12], [-14, -3], [-28, -1], [-36, -7]]
POOL_C = [[-10, 8], [-2, 6], [4, 11], [-3, 17], [-11, 15]]
neutral_marks = [
    {"id": "pool-a", "kind": "area", "ring": POOL_A, "h": 15, "bevel": 4},
    {"id": "pool-c", "kind": "area", "ring": POOL_C, "h": 15, "bevel": 4},
]
relief = {
    "team": {"base": MOOR, "reach": 60, "marks": team_marks + neutral_marks, "pushes": [],
             "grain": {"amplitude": 1.2, "scale": 8, "seed": 5}},
}


# ── added ground shapes: the crypt (subtracts and the lids over them), worn patches ──
def rectpoly(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def blob(cx, cz, rx, rz, n=10, turn=0.0):
    return [[round(cx + rx * math.cos(2 * math.pi * k / n + turn), 1),
             round(cz + rz * math.sin(2 * math.pi * k / n + turn), 1)] for k in range(n)]


def poly(sid, pts, **fields):
    return {"id": sid, "type": "polygon", "operation": "add", "vertices": pts, "floor": 0, "layer": "ground",
            "group": "team", **fields}


def cut(sid, pts, floor, height):
    return poly(sid, pts, operation="subtract", floor=floor, base_height=height)


def lid(sid, pts, floor, top):
    return poly(sid, pts, override=True, floor=floor, base_height=top - floor, keepClear=False)


HALL = (-40, -88, -12, -72)
WSHAFT = (-37, -85, -33, -81)      # the monks' stair, a shaft from the hall up to the abbey floor
CORR1 = (-12, -83, 27, -78)
CORR2 = (22, -78, 27, -62)
VSHAFT = (23, -62, 26, -59)        # the well in the village square

shapes = [
    cut("crypt-hall-w", rectpoly(-40, -88, -37, -72), 19, 1),
    cut("crypt-hall-e", rectpoly(-33, -88, -12, -72), 19, 1),
    cut("crypt-hall-n", rectpoly(-37, -88, -33, -85), 19, 1),
    cut("crypt-hall-s", rectpoly(-37, -81, -33, -72), 19, 1),
    cut("crypt-corridor-1", rectpoly(*CORR1), 17, 1),
    cut("crypt-corridor-2", rectpoly(*CORR2), 17, 1),
    cut("crypt-well", rectpoly(*VSHAFT), 50, 1),
    cut("crypt-stair", rectpoly(*WSHAFT), 50, 1),
    # the lids: ground over the voids, whose tops state the ground they sit in
    lid("lid-hall-w", rectpoly(-40, -88, -37, -72), 20, PLAT),
    lid("lid-hall-e", rectpoly(-33, -88, -12, -72), 20, PLAT),
    lid("lid-hall-n", rectpoly(-37, -88, -33, -85), 20, PLAT),
    lid("lid-hall-s", rectpoly(-37, -81, -33, -72), 20, PLAT),
    lid("lid-corridor-abbey", rectpoly(-12, -83, -4, -78), 18, PLAT),
    lid("lid-corridor-village", rectpoly(-4, -83, 27, -78), 18, TERR),
    lid("lid-corridor-2", rectpoly(22, -78, 27, -62), 18, TERR),
]

# worn ground and a few patches of their own
BOG_EDGE = [[-56, -26], [-44, -29], [-30, -25], [-16, -30], [-2, -26], [14, -30], [30, -25], [44, -29], [56, -27],
            [56, 0], [-56, 0]]
shapes += [
    poly("bog-paint", BOG_EDGE, base_height=1, theme="bog"),
    # peat hags: darker, lower patches in the bog's margin
    poly("hag-1", blob(-44, -18, 7, 4, 10, 0.2), base_height=1, height_mode="sink", theme="peat"),
    poly("hag-2", blob(-4, -8, 6, 4, 10, 0.7), base_height=1, height_mode="sink", theme="peat"),
    poly("hag-3", blob(44, -9, 7, 5, 10, 0.4), base_height=1, height_mode="sink", theme="peat"),
    poly("hag-4", blob(14, -21, 5, 3, 9, 0.1), base_height=1, height_mode="sink", theme="peat"),
    # heath: patches of podzol and grass on the moor
    poly("heath-1", blob(-46, -108, 8, 6, 11, 0.3), base_height=1, height_mode="sink", theme="heath"),
    poly("heath-2", blob(36, -36, 9, 5, 11, 0.8), base_height=1, height_mode="sink", theme="heath"),
    poly("heath-3", blob(-26, -48, 8, 5, 10, 0.5), base_height=1, height_mode="sink", theme="heath"),
    poly("heath-4", blob(20, -104, 9, 5, 11, 0.1), base_height=1, height_mode="sink", theme="heath"),
    # two plots of tilled ground beside the grange barn
    poly("plot-1", rectpoly(-55, -112, -48, -104), base_height=1, theme="plot"),
    poly("plot-2", rectpoly(-55, -102, -48, -94), base_height=1, theme="plot"),
    poly("worn-square", blob(36, -66, 8, 5, 11, 0.3), base_height=1, height_mode="sink", theme="moor"),
]

# ── made things ──────────────────────────────────────────────────────────────────────
def box(sid, x0, z0, x1, z1, floor, height, material):
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": height, "material": material}


def made_layer(layer_id, part, base_y, shapes_, seat=None, mirrors=True):
    layer = {"id": layer_id, "name": layer_id, "base_y": base_y, "kind": "made", "part_of": part,
             "shapes": shapes_, "groups": [{"id": layer_id, "name": layer_id, "mirrors": mirrors,
                                            "shapeIds": [x["id"] for x in shapes_]}]}
    if seat:
        layer["seat"] = seat
    return layer


RUIN = cell(31, 3, [SBRICK, SBRICK, SBRICK_MOSS, SBRICK, SBRICK_CRACK, COBBLE], jitter=60, warp=3, rise=2)
FLAG = cell(32, 3, [SBRICK, POLISHED, ANDESITE, STONE], jitter=50, warp=2, rise=2)
LADDER = lambda d: S(65, d)  # noqa: E731

# the crypt: floor, pillars, lamps, ladders
crypt_floor = [box("floor-hall", *HALL[:2], *HALL[2:], 0, 12, FLAG),
               box("floor-c1", *CORR1[:2], *CORR1[2:], 0, 12, FLAG),
               box("floor-c2", *CORR2[:2], *CORR2[2:], 0, 12, FLAG),
               box("floor-well", *VSHAFT[:2], *VSHAFT[2:], 0, 12, FLAG)]
pillar_cells = [(x, z) for x in (-33, -27, -21, -15) for z in (-85, -77)]
pillars = [box(f"pillar-{i}", x, z, x + 2, z + 2, 0, 6, SBRICK) for i, (x, z) in enumerate(pillar_cells)]
lamps = [box(f"lamp-{i}", x, z, x + 2, z + 2, 0, 1, S(89)) for i, (x, z) in enumerate(pillar_cells)]
ladders = [box("ladder-abbey", -36, -85, -35, -84, 0, 34, LADDER(3)),     # on the north wall of the stair, facing south
           box("ladder-well", 24, -60, 25, -59, 0, 22, LADDER(2))]         # on the south wall of the well, facing north
# the well's curb, a block high round the opening, open on the village side
curb = [box("curb-n", 22, -63, 27, -62, 0, 1, FLAG), box("curb-w", 22, -62, 23, -59, 0, 1, FLAG),
        box("curb-e", 26, -62, 27, -59, 0, 1, FLAG)]

# the abbey's ruins: one layer of walls of every height, none over another
AX0, AX1, AZ0, AZ1 = -40, -12, -88, -72
walls = []


def wall_run(prefix, x0, z0, x1, z1, heights, along_x=True):
    """A wall as a run of segments of stated height; a height of 0 is a gap."""
    n = len(heights)
    for i, h in enumerate(heights):
        if h <= 0:
            continue
        if along_x:
            a = x0 + (x1 - x0) * i // n
            b = x0 + (x1 - x0) * (i + 1) // n
            walls.append(box(f"{prefix}-{i}", a, z0, b, z1, 0, h, RUIN))
        else:
            a = z0 + (z1 - z0) * i // n
            b = z0 + (z1 - z0) * (i + 1) // n
            walls.append(box(f"{prefix}-{i}", x0, a, x1, b, 0, h, RUIN))


wall_run("wall-n", AX0 + 1, AZ0, AX1 - 1, AZ0 + 1, [9, 9, 4, 11, 3, 0, 6, 8, 2, 7], True)
wall_run("wall-s", AX0 + 7, AZ1 - 1, AX1 - 1, AZ1, [8, 5, 0, 0, 4, 9, 3, 6], True)       # a doorway gap, two broken stretches
wall_run("wall-w", AX0, AZ0, AX0 + 1, AZ1, [14, 14, 14, 9, 12, 6, 14, 5], False)          # the west gable stands tall
wall_run("wall-e", AX1 - 1, AZ0, AX1, AZ1, [7, 4, 0, 5, 2, 8, 0, 3], False)
# the tower stump at the south-west corner, a ring broken at the top
walls += [box("tower-n", AX0 + 1, AZ1 - 7, AX0 + 7, AZ1 - 6, 0, 16, RUIN), box("tower-e", AX0 + 6, AZ1 - 6, AX0 + 7, AZ1 - 1, 0, 11, RUIN),
          box("tower-s", AX0 + 1, AZ1 - 1, AX0 + 6, AZ1, 0, 15, RUIN)]
# a cloister to the north: colonnade stumps
for i, x in enumerate(range(-38, -12, 6)):
    walls.append(box(f"cloister-{i}", x, -94, x + 2, -92, 0, 5 + (i * 3) % 6, RUIN))
# the standing stones of the bog: two rings (one a side by the fan), seven stones each
stones = []
ring_c = (24, -10)
for i in range(7):
    ang = 2 * math.pi * i / 7
    sx, sz = round(ring_c[0] + 9 * math.cos(ang)), round(ring_c[1] + 7 * math.sin(ang))
    stones.append(box(f"stone-{i}", sx, sz, sx + 1 + (i % 2), sz + 2 - (i % 2), 0, 4 + (i * 5) % 4, S(1, 5)))
# the causeway stones: a line of single stones beside the old way across the bog
for i, (sx, sz) in enumerate([(2, -20), (6, -14), (-3, -12), (9, -8), (1, -4)]):
    stones.append(box(f"way-{i}", sx, sz, sx + 1, sz + 1, 0, 3 + i % 3, S(1, 5)))

GARTH = cell(37, 3, [COBBLE, MOSSY, STONE, COBBLE], jitter=60, warp=3, rise=2)
yard_walls = [box("yard-w", -24, -100, -23, -90, 0, 2, GARTH), box("yard-e", 21, -100, 22, -90, 0, 2, GARTH),
              box("yard-s-w", -24, -91, -5, -90, 0, 2, GARTH), box("yard-s-e", 5, -91, 22, -90, 0, 2, GARTH)]
gate_posts = [box("gate-w", -5, -91, -3, -89, 0, 4, GARTH), box("gate-e", 3, -91, 5, -89, 0, 4, GARTH)]
layers = [
    made_layer("yard-walls", "grange", 0, yard_walls, seat="ground"),
    made_layer("gate-posts", "grange", 0, gate_posts, seat="ground"),
    made_layer("crypt-floor", "crypt", 0, crypt_floor, mirrors=True),
    made_layer("crypt-pillars", "crypt", 12, pillars),
    made_layer("crypt-lamps", "crypt", 18, lamps),
    made_layer("crypt-ladders", "crypt", 12, ladders),
    made_layer("well-curb", "well", 0, curb, seat="ground"),
    made_layer("abbey-ruins", "abbey", 0, walls, seat="ground"),
    made_layer("standing-stones", "stones", 0, stones, seat="ground"),
]

# ── dressing ─────────────────────────────────────────────────────────────────────────
TREES = showcase.trees()
OAK = TREES["tiny-oak-3"]["style"]
OAK2 = TREES["tiny-oak-6"]["style"]
YEW = TREES["tiny-spruce-2"]["style"]
ROCKSTYLE = {"kind": "boulder", "form": "angular", "size": 4, "rock": cell(53, 4, [STONE, ANDESITE, COBBLE, STONE], 2, 3), "mossy": False}
TOR = {"kind": "boulder", "form": "outcrop", "size": 5, "rock": cell(54, 4, [STONE, ANDESITE, STONE, COBBLE], 2, 3), "mossy": False}

styles = {
    "oak": OAK, "oak-b": OAK2, "yew": YEW, "rock": ROCKSTYLE, "tor": TOR,
    "cot-a": {"library": "spruce-roofed-stone-cottage", "kind": "house"},
    "cot-b": {"library": "dark-oak-roofed-stone-cottage", "kind": "house"},
    "farm": {"library": "rubble-and-spruce-house", "kind": "house"},
    "barn": {"library": "stone-and-spruce-barn", "kind": "house"},
    "longhouse": {"library": "spruce-roofed-stone-longhouse", "kind": "house"},
}


def house(pid, style, x0, z0, x1, z1, front="posZ", ridge=None):
    spec = {"ridge": ridge} if ridge else {}
    return {"id": pid, "kind": "house", "layer": "ground", "seed": 5, "front": front, "style": style,
            "wings": [{"corners": [[x0, z0], [x1, z1]], "spec": spec}]}


def stroke(pid, pts, radius=2, wander=1.0, pave=None, claims=True):
    return {"id": pid, "kind": "stroke", "layer": "ground", "seed": 3, "points": pts, "radius": radius,
            "style": "solid", "pave": pave or HARD_PATH, "claimsGround": claims, "wander": wander, "wanderLength": 14}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "layer": "ground", "seed": 7, "x": x, "z": z, "style": style}


def boulder(pid, style, x, z):
    return {"id": pid, "kind": "boulder", "layer": "ground", "seed": 9, "x": x, "z": z, "style": style}


props = [
    # circulation first: the moor road, the abbey way, the village street, the bog causeway
    stroke("road-spawn", [[-2, -98], [-8, -92], [-20, -86]], 2, 1.5, SOFT_PATH),
    stroke("road-village", [[2, -98], [14, -92], [30, -86]], 2, 1.0, SOFT_PATH),
    stroke("street", [[6, -83], [26, -83], [48, -83]], 2, 0.5, HARD_PATH),
    stroke("street-n", [[28, -90], [28, -83]], 2, 0.5, HARD_PATH),
    stroke("street-s", [[8, -60], [8, -83]], 2, 0.5, HARD_PATH),
    stroke("way-abbey", [[-30, -28], [-34, -46], [-30, -60], [-24, -66]], 2, 1.0, HARD_PATH),
    stroke("way-orchard", [[8, -26], [8, -38], [8, -50], [8, -58]], 2, 0.5, HARD_PATH),
    stroke("way-bog", [[0, -26], [2, -20], [6, -14], [4, -8], [0, 0]], 2, 1.0, S(1, 6)),
    stroke("abbey-floor", [[-38, -80], [-14, -80]], 7, 0.0, FLAG, False),
    # the village on its terrace
    house("farm-1", "longhouse", 12, -79, 24, -72, "posZ"),
    house("cot-1", "cot-a", 29, -79, 35, -73, "negZ"),
    house("cot-2", "cot-b", 40, -79, 46, -73, "negZ"),
    # the abbey's grange round the spawn longhouse: a barn, a cottage, a walled yard, a forecourt, a pond
    house("grange-barn", "cot-b", -45, -113, -38, -106, "posZ"),
    house("grange-cot", "cot-a", 23, -113, 29, -107, "posZ"),
    stroke("forecourt", [[-4, -99], [4, -99]], 5, 0.3, HARD_PATH),
    # the orchard: rows on the two terraces and on the village's south edge
    tree("o1", "oak", 2, -41), tree("o2", "oak-b", 14, -45), tree("o3", "oak", 24, -45), tree("o5", "oak", 44, -45), tree("o6", "oak-b", 53, -45),
    tree("o7", "oak", 20, -31), tree("o9", "oak", 47, -35),
    # yews in the abbey's garth, a tor on the moor
    tree("y1", "yew", -34, -94),
    boulder("tor-1", "tor", -50, -50), boulder("tor-2", "tor", 50, -113), boulder("r1", "rock", -50, -98), boulder("r2", "rock", 40, -28),
    *[{"id": f"pool-{name}-water", "kind": "fluid", "layer": "ground", "seed": seed, "shape": "basin", "level": 18,
       "points": grown(ring, 4), "radius": 2, "depth": 2, "fluid": "water", "shore": 1}
      for name, seed, ring in (("a", 6, POOL_A), ("b", 6, [[-x, -z] for x, z in POOL_A]),
                               ("c", 8, POOL_C), ("d", 8, [[-x, -z] for x, z in POOL_C]))],
    *[{"id": f"pond-{name}", "kind": "fluid", "layer": "ground", "seed": 12, "shape": "basin", "level": 36,
       "points": grown(ring, 4), "radius": 2, "depth": 2, "fluid": "water", "shore": 1}
      for name, ring in (("n", POND), ("s", [[-x, -z] for x, z in POND]))],
    {"id": "cover", "kind": "flora", "layer": "ground", "seed": 11,
     "points": [[-56, -120], [56, -120], [56, -24], [-56, -24]],
     "spec": {"coverage": 0.2, "scale": 9, "octaves": 2, "fernShare": 0.3, "flowerShare": 0.18, "flowerScale": 7, "tallShare": 0.03}},
]

refinement = {
    "created": "2026-10-10",
    "authors": [{"name": "Sonnet 5.5", "contribution": "Plan, ground, crypt, paint, dressing"}],
    "themes": themes, "mapTheme": "moor",
    "relief": relief,
    "addShapes": shapes,
    "addLayers": layers,
    "biome": {"kind": "solid", "biome": 6},
    "roomStyles": {"spawn": {"library": "spruce-roofed-stone-longhouse"}},
    "dressing": {"styles": styles, "props": props},
}

if __name__ == "__main__":
    json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
    print("pieces", len(pieces), "props", len(props), "wall shapes", len(walls))
