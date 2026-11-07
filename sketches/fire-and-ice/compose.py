"""Compose the fire-and-ice CTW/DTC sketch from the footprints of its structures: one half, then turned 180 degrees.

    python3 sketches/fire-and-ice/compose.py <source-region> <out-region> [--xray <dir>] [--no-rotate]

<source-region> is the author's sketch world (its four region files); nothing in it is written over. The structures
are carried as their rough form only, plain stone with every stair, slab, fence and relief step taken out; the
ground is rebuilt around them area by area, and the sketch's own surfaces are the control points the mountains are
drawn through. Every new piece is wool in a colour of its own; the ground under every surface is stone.
"""
import collections
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
sys.path.insert(0, HERE)
from anvil import World
from anvilw import write_world
import loft
import terrain

ROTATE = "--no-rotate" not in sys.argv
XRAY = sys.argv[sys.argv.index("--xray") + 1] if "--xray" in sys.argv else None

# ---------------------------------------------------------------- the frame
OFFSET = (-35, -61, -43)         # the floating copies onto the ground, measured off the two cores
CENTRE = (24, 48)                # the 180-degree turn's pivot: block (24, 48)
HALF = ((-60, 68), (-110, 48))
L = 14                           # the lane's walk surface: the floating lane's white top, brought down unchanged
ROOF_Y = L + 15                  # the flat roof over everything underground, fifteen over the walk
FLOOR_Y = 30                     # the valley floor's level wherever the composition lays new floor

W = lambda d: (35, d)
KEY = {"walk": W(8), "lane": W(0), "sheet_face": W(5), "sheet_back": W(13), "flat": W(4), "mountain": W(3),
       "tunnel_wall": W(9), "tunnel_floor": W(12), "tunnel_roof": W(11), "stair_wall": W(1), "hall_wall": W(2),
       "wool_goal": W(14), "goal_plinth": W(15), "void": W(10)}
STONE, BEDROCK, FILL = (1, 0), (7, 0), (1, 0)
CLAY, PLATE_WOOL = (82, 0), (35, 8)
MARK = (133, 0)

src = World(SRC)
orig = {(x, y, z): (i, d) for x, y, z, i, d in src.blocks()}
out = {}
report = []
SPACE, OPEN_SPACE, SKY_OPEN = set(), set(), set()
TUNNELS, TUNNEL_BLOCKS, ROUTE = [], set(), ["-"]


def put(cell, block):
    out[cell] = block


def clear(cell):
    out.pop(cell, None)


def tput(cell, block):
    put(cell, block); TUNNEL_BLOCKS.add(cell)


def is_terrain(block):
    return (block[0] == 35 and block[1] in (0, 3, 4, 5, 8, 13)) or block[0] in (41, 57, 133, 42)


def inside(cell, box):
    return all(lo <= v <= hi for v, (lo, hi) in zip(cell, box))


def in_half(x, z):
    return HALF[0][0] <= x <= HALF[0][1] and HALF[1][0] <= z <= HALF[1][1]


def reference(x, y, z):
    """The sketch's floating pieces and its swatches, kept where they are as reference."""
    return (8 <= x <= 52 and y >= 85 and -22 <= z <= 47) or (x >= 70 and 63 <= y <= 81 and -25 <= z <= 40) \
        or y >= 100 or z < -140


for cell, block in orig.items():
    if reference(*cell): put(cell, block)

# ---------------------------------------------------------------- 1. the structures, as their rough form
DETAIL = {53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180, 44, 126, 182, 85, 139, 188, 189, 190,
          191, 192, 107, 183, 184, 185, 186, 187, 101, 102, 160, 50, 75, 76, 55, 69, 77, 143, 151, 178, 131, 132,
          20, 95, 171, 96, 65, 63, 68}
KEEP = {7, 49, 10, 11, 82, 133, 35}


def rough(blocks):
    """A structure as its rough form: every stair, slab, fence, pane, torch and wire gone, every other building block
    plain stone, and every one-block recess in a wall filled so each face is one plane. The nether-brick fence stays,
    as stone: the antenna on the roof is built of it, and without it the antenna's cap floats."""
    kept = {}
    for cell, (i, d) in blocks.items():
        if i in DETAIL: continue
        kept[cell] = (i, d) if i in KEEP else STONE
    solid = {c for c, b in kept.items() if b in (STONE, BEDROCK)}
    for (x, y, z) in list(solid):
        for dx, dz in ((1, 0), (0, 1)):
            gap = (x + dx, y, z + dz)
            if gap not in kept and (x + 2 * dx, y, z + 2 * dz) in solid:
                kept[gap] = STONE
    return kept


STRUCTURE_IDS = {1, 4, 7, 49, 98, 109, 139, 101, 160, 113, 112, 114, 126, 44, 108, 45, 5, 67, 136, 82, 159, 155,
                 156, 48, 24}

# the bunker: the floating copy brought down onto the original, the original's lava core kept
BUNKER = rough({(x + OFFSET[0], y + OFFSET[1], z + OFFSET[2]): b for (x, y, z), b in orig.items()
                if 8 <= x <= 52 and 85 <= y <= 157 and -22 <= z <= 47})
CORE_BOX = ((-9, -3), (39, 56), (-22, -9))
for cell, (i, d) in orig.items():
    if inside(cell, CORE_BOX):
        if i in (10, 11): BUNKER[cell] = (11, 0)
        elif i in (49, 35): BUNKER[cell] = (49, 0)
for cell, (i, d) in orig.items():
    if i in (155, 156) and inside(cell, ((-21, -9), (56, 56), (-20, -11))): BUNKER[cell] = STONE
# the roof plates over the spawn wing, carried back over the rest of it in the same six-block checker
PLATE_Y = 67
PLATES = set()
for z in range(-65, -21):
    row = sorted((x, BUNKER[(x, PLATE_Y, z)]) for x in range(-10, 0) if (x, PLATE_Y, z) in BUNKER)
    if not row: continue
    x0, block = row[0]
    for x in range(x0 - 1, -29, -1):
        steps = (x0 - 1 - x) // 6 + 1
        here = (PLATE_WOOL if block == CLAY else CLAY) if block in (CLAY, PLATE_WOOL) and steps % 2 else block
        BUNKER[(x, PLATE_Y, z)] = here
        PLATES.add((x, z))
for cell, block in BUNKER.items(): put(cell, block)


def lift(box):
    return {c: b for c, b in orig.items() if inside(c, box) and b[0] in STRUCTURE_IDS}


# the H dome, the shelf's two walls and the small stone piece by the planes, each as its rough form
H_DOME = rough(lift(((10, 30), (56, 67), (-85, -71))))
Y_WALLS = rough(lift(((40, 67), (32, 51), (-70, -28))))
for part in (H_DOME, Y_WALLS, rough(lift(((15, 24), (36, 39), (-57, -53))))):
    for cell, block in part.items(): put(cell, block)
report.append(f"structures as their rough form: bunker {len(BUNKER)} blocks with {len(PLATES)} plate columns carried "
              f"back, H dome {len(H_DOME)}, the shelf's walls {len(Y_WALLS)}")

# ---------------------------------------------------------------- 2. the sketch's floor and its retaining planes
floor_top, plane_top = {}, {}
for (x, y, z), b in orig.items():
    if not in_half(x, z) or reference(x, y, z) or not 27 <= y <= 60: continue
    if b == KEY["walk"] and y <= 36:
        if (x, y, z) in out: continue
        put((x, y, z), b)
        if y > floor_top.get((x, z), -1): floor_top[(x, z)] = y
    elif b in (KEY["sheet_face"], KEY["sheet_back"]):
        put((x, y, z), b)
        if y > plane_top.get((x, z), -1): plane_top[(x, z)] = y
for (x, y, z), b in orig.items():                       # the planes' own loft points; the loose markers stay behind
    if b == MARK and in_half(x, z) and not reference(x, y, z) and any(
            orig.get((x + dx, y + dy, z + dz)) in (KEY["sheet_face"], KEY["sheet_back"])
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))):
        put((x, y, z), b)

# the pit under the core, its ramp and its back room are open from the top: no floor lies over them
pit_cols = {(x, z) for (x, y, z) in BUNKER if y <= 29 and in_half(x, z)}
for (x, z) in pit_cols:
    for y in range(24, 41):
        if out.get((x, y, z)) == KEY["walk"] and (x, y, z) not in BUNKER: clear((x, y, z))
    floor_top.pop((x, z), None)
    if BUNKER.get((x, 24, z)) == KEY["void"] and z <= -9:
        for y in range(0, 24):
            SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
        SKY_OPEN.add((x, z))
    for y in range(25, 41):
        if (x, y, z) not in out: SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
report.append(f"the pit, its ramp and its back room: {len(pit_cols)} columns open from the top")

# ---------------------------------------------------------------- 3. the wool lane and its flat roof
LANE_SRC = ((70, 101), (63, 81), (-25, 40))
lane = rough({(x + OFFSET[0], y + OFFSET[1], z + OFFSET[2]): b for (x, y, z), b in orig.items()
              if inside((x, y, z), LANE_SRC)})
for cell, block in lane.items(): put(cell, block)
roofed = {(x, z) for x in range(33, 68) for z in range(-69, -24)
          if (34 <= x <= 64 and -68 <= z <= -52) or (34 <= x <= 66 and -51 <= z <= -26)}
for (x, z) in roofed:
    for y in range(0, ROOF_Y):
        if (x, y, z) not in out: SPACE.add((x, y, z))
    put((x, ROOF_Y, z), BEDROCK)
    TUNNELS.append(("the lane's roof", x, z, ROOF_Y))
    edge = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, z + dz) not in roofed]
    if not edge: continue
    if all((ex > x and x == 66) or (ez > z and z == -26 and x >= 48) or (ex < x and x == 34 and -39 <= z <= -34)
           for ex, ez in edge):
        continue                                        # the long side open to the void, the mouth, the west arm
    for y in range(0, ROOF_Y):
        if (x, y, z) not in out: put((x, y, z), BEDROCK if y <= L + 3 else STONE)
gx, gz = 47, -60
floor_y = max(y for (x, y, z), b in lane.items() if (x, z) == (gx, gz) and b[0] == 35)
for dx in (-1, 0, 1):
    for dz in (-1, 0, 1): put((gx + dx, floor_y + 1, gz + dz), KEY["goal_plinth"])
put((gx, floor_y + 2, gz), KEY["wool_goal"])
report.append(f"lane: walk y {L}, flat roof y {ROOF_Y} from the wool area to z -26; wool on its plinth at "
              f"({gx}, {floor_y + 2}, {gz})")

# ---------------------------------------------------------------- 4. the entrance: wall, retaining strip, ramp
CANYON = ((48, 66), (-25, -4))
for x in range(CANYON[0][0], CANYON[0][1] + 1):
    for z in range(CANYON[1][0], CANYON[1][1] + 1):
        SKY_OPEN.add((x, z))
        for y in range(0, 61):
            if (x, y, z) not in out: SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))

LANE_END = max(y for (x, y, z), b in lane.items() if b == KEY["lane"] and z == -5)
ramp_rows = [                                            # the lane already climbs to its south end; the ramp goes on
    [(48, LANE_END, -4.5), (53.5, LANE_END, -4.4), (59, LANE_END, -4.6), (65.6, LANE_END, -4.5)],
    [(48, 23.1, 1.5), (53.8, 22.8, 1.9), (59.6, 22.6, 1.2), (65.4, 22.9, 1.7)],
    [(47.6, 26.0, 7.5), (53.0, 25.6, 8.1), (58.4, 25.4, 7.3), (64.6, 25.8, 7.9)],
    [(47.0, 28.7, 13.2), (52.2, 28.4, 13.9), (57.5, 28.1, 13.0), (63.0, 28.5, 13.6)],
    [(45.5, 30, 18.6), (50.6, 30, 19.4), (55.8, 29.8, 18.8), (61.0, 30, 19.6)],
]
ramp_top = {}
for row in loft.surface(ramp_rows, density=0.35):
    for p in row:
        col = (math.floor(p[0]), math.floor(p[2]))
        ramp_top[col] = max(ramp_top.get(col, -99), min(FLOOR_Y, math.floor(p[1])))
for (x, z), y in ramp_top.items():
    for yy in range(y + 1, 61):
        if out.get((x, yy, z)) == KEY["walk"]: clear((x, yy, z))
        SPACE.add((x, yy, z)); OPEN_SPACE.add((x, yy, z))
    put((x, y, z), KEY["walk"]); put((x, y - 1, z), KEY["walk"])
    floor_top.pop((x, z), None)


def ramp_y(z):
    near = [y for (x, zz), y in ramp_top.items() if zz == z and 48 <= x <= 52]
    return max(near) if near else None


def wall_top(z):
    """The lane's west wall carried on to the ramp: flat-roof height under the roof, eight over the old wall by the
    boulder, lower by the entrance, then down in steps of three alongside the ramp until the floor meets it."""
    if z <= -26: return ROOF_Y
    if z <= -17: return 25
    if z <= -5: return 23
    r = ramp_y(z)
    if r is None or r >= FLOOR_Y - 2: return None
    return min(FLOOR_Y, 3 * math.ceil((r + 3) / 3))


wall_end = -7
for z in range(-29, 40):
    top = wall_top(z)
    if top is None: break
    wall_end = z
    for x in (46, 47):
        for y in range(8, top + 1):
            if (x, y, z) not in out or out[(x, y, z)] == KEY["walk"]: put((x, y, z), STONE)

# the retaining strip: the floor held back over the wall, from the floor's edge down onto the wall's top
strip_top, strip_bottom = [], []
for k, z in enumerate((-25.5, -21.0, -16.5, -12.2, -7.4, -2.6, 2.9, 8.3, 13.1, 17.8, 22.6)):
    if z > wall_end + 1: break
    top = wall_top(math.floor(z)) or FLOOR_Y
    strip_top.append((43.6 + (0.6, -0.3, 0.0)[k % 3], FLOOR_Y, z))
    strip_bottom.append((46.4, top + 0.5, z))
sheet = loft.surface([strip_bottom, strip_top], density=0.3)
for sign in (1, -1):
    layers = loft.voxels(sheet, thickness=2, normal_sign=sign)
    if sum(c[0] for c in layers[1]) / len(layers[1]) < sum(c[0] for c in layers[0]) / len(layers[0]): break
for cell in layers[1]:
    if cell not in out: put(cell, KEY["sheet_back"])
for cell in layers[0]:
    if cell not in out or out[cell] == KEY["sheet_back"]: put(cell, KEY["sheet_face"])
strip_cols = {(c[0], c[2]) for c in layers[0] | layers[1]}
for (x, y, z) in layers[0] | layers[1]:
    if y > plane_top.get((x, z), -1): plane_top[(x, z)] = y
report.append(f"entrance: west wall carried to z {wall_end}; a retaining strip of {len(strip_cols)} columns from the "
              f"floor down onto it; ramp {len(ramp_top)} columns on from the lane's end at y {LANE_END} to the floor at z 19")

# the floor carried east to the wall, and laid over the roof in front of the shelf's south wall
y_wall_cols = {(x, z) for (x, y, z) in Y_WALLS}
for z in range(-30, wall_end + 1):
    for x in range(30, 46):
        if (x, z) in floor_top or (x, z) in ramp_top or (x, z) in strip_cols: continue
        if any((x, y, z) in out for y in range(FLOOR_Y - 1, FLOOR_Y + 8)): continue
        put((x, FLOOR_Y, z), KEY["walk"]); floor_top[(x, z)] = FLOOR_Y
for x in range(44, 67):
    for z in range(-31, -25):
        if any((x, z2) in y_wall_cols for z2 in range(z, -26)): continue
        if (x, FLOOR_Y, z) not in out and (x, z) not in strip_cols:
            put((x, FLOOR_Y, z), KEY["walk"]); floor_top[(x, z)] = FLOOR_Y

# ---------------------------------------------------------------- 5. the ground between the halves
def south_edge(x):
    best = None
    for z in range(10, 40):
        for y in range(26, 34):
            if orig.get((x, y, z)) == KEY["walk"]: best = (z, y)
    return best


edge = [(x, found[1], found[0] - 1) for x in range(-6, 53, 6) if (found := south_edge(x))]
connector_rows = [edge,
                  [(-8, 30, 36.5), (6, 30.4, 37.8), (22, 30.2, 36.9), (38, 29.8, 38.3), (52, 30, 37.2)],
                  [(-5, 30, 48), (8, 30, 48), (24, 30, 48), (40, 30, 48), (53, 30, 48)]]
connector = set()
for layer in loft.voxels(loft.surface(connector_rows, density=0.4), thickness=2):
    for cell in layer:
        if cell not in out and (cell[0], cell[2]) not in ramp_top:
            put(cell, KEY["walk"]); connector.add((cell[0], cell[2]))
            if cell[1] > floor_top.get((cell[0], cell[2]), -1): floor_top[(cell[0], cell[2])] = cell[1]
report.append(f"middle: floor from the valley floor's south edge to the centre line, {len(connector)} columns")

# ---------------------------------------------------------------- 6. tunnels
def corridor(a, b, y):
    """A straight 3-wide, 3-tall corridor along x or z from a to b (inclusive) with its floor at y."""
    (x0, z0), (x1, z1) = a, b
    along_x = z0 == z1
    n = abs(x1 - x0) if along_x else abs(z1 - z0)
    step = 1 if (x1 - x0 if along_x else z1 - z0) >= 0 else -1
    for k in range(n + 1):
        cx, cz = (x0 + k * step, z0) if along_x else (x0, z0 + k * step)
        for w in range(-2, 3):
            px, pz = (cx, cz + w) if along_x else (cx + w, cz)
            for dy in range(0, 5):
                cell = (px, y + dy, pz)
                if abs(w) == 2 or dy in (0, 4):
                    block = KEY["tunnel_floor"] if dy == 0 else KEY["tunnel_roof"] if dy == 4 else KEY["tunnel_wall"]
                    if cell not in out or is_terrain(out[cell]): tput(cell, block)
                else:
                    SPACE.add(cell)
                    if cell in out and (is_terrain(out[cell]) or out[cell][0] in (35,)): clear(cell)
            TUNNELS.append((ROUTE[0], px, pz, y + 4))
    return n + 1

def flight(start, direction, y, dy_total, open_above=None):
    """A 2-wide stair shaft from `start` heading `direction`, its floor block at `y`, moving `dy_total` blocks
    (negative is down): three steps, then a one-block landing. Returns the end and its floor height."""
    (x, z), (dx, dz) = start, direction
    sign = 1 if dy_total > 0 else -1
    moved = 0; k = 0
    while True:
        for w in (-1, 0, 1, 2):
            px, pz = (x + w * abs(dz), z + w * abs(dx))
            for dy in range(0, 6):
                cell = (px, y + dy, pz)
                if open_above is not None and y + dy > open_above:
                    SPACE.add(cell); OPEN_SPACE.add(cell)
                    if cell in out and out[cell] != BEDROCK: clear(cell)
                    continue
                if dy == 0 or dy == 5 or w in (-1, 2):
                    block = KEY["tunnel_floor"] if dy == 0 else KEY["tunnel_roof"] if dy == 5 else KEY["stair_wall"]
                    if cell not in out or is_terrain(out[cell]): tput(cell, block)
                else:
                    SPACE.add(cell)
                    if cell in out and (is_terrain(out[cell]) or (open_above is not None and out[cell] == STONE)):
                        clear(cell)
            if open_above is None or y + 5 <= open_above:
                TUNNELS.append((ROUTE[0], px, pz, y + 5))
        if moved == abs(dy_total): break
        x += dx; z += dz; k += 1
        if k % 4 != 0:
            y += sign; moved += 1
    return (x, z), y

def hall(x0, z0, x1, z1, y, height=6):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for dy in range(0, height + 2):
                cell = (x, y + dy, z)
                if dy == 0: tput(cell, KEY["tunnel_floor"])
                elif dy == height + 1: tput(cell, KEY["tunnel_roof"])
                elif edge: tput(cell, KEY["hall_wall"])
                else:
                    SPACE.add(cell)
                    if cell in out and is_terrain(out[cell]): clear(cell)
            TUNNELS.append((ROUTE[0], x, z, y + height + 1))

def door(x, z, y, axis):
    for w in (-1, 0, 1):
        for dy in (1, 2, 3):
            cell = (x + (w if axis == "z" else 0), y + dy, z + (w if axis == "x" else 0))
            clear(cell); SPACE.add(cell)


FLOOR_T = L - 1
H1 = (10, -46, 21, -30)
ROUTE[0] = "hall"
hall(*H1, FLOOR_T, height=6)
ROUTE[0] = "T3 hall to the west arm"
corridor((22, -37), (35, -37), FLOOR_T); door(21, -37, FLOOR_T, "x")
SPAWN = (-26, -11, -50, -39, 31)
ROUTE[0] = "spawn room"
hall(SPAWN[0], SPAWN[2], SPAWN[1], SPAWN[3], SPAWN[4], height=9)
for z in range(-48, -40):                               # the room opens into the door frame, the frame onto the valley
    for y in range(32, 45):
        for x in (-11, -10, -9, -8, -7):
            if y <= 40 or x >= -9:
                if x <= -10: clear((x, y, z))
                SPACE.add((x, y, z))
                if x >= -9: OPEN_SPACE.add((x, y, z))
    for x in range(-11, -6):
        if (x, 31, z) not in out: put((x, 31, z), KEY["walk"])
    for y in range(41, 47): put((-10, y, z), STONE)
ROUTE[0] = "T2 spawn to the hall"
endA, yA = flight((-12, -47), (-1, 0), 31, -9)
for x in range(endA[0] - 2, endA[0] + 2):              # the landing, under the room's floor
    for z in range(-48, -39):
        tput((x, yA, z), KEY["tunnel_floor"]); tput((x, yA + 6, z), KEY["tunnel_roof"])
        for y in range(yA + 1, yA + 6):
            if x == endA[0] - 2 or z in (-48, -39): tput((x, y, z), KEY["hall_wall"])
            else: clear((x, y, z)); SPACE.add((x, y, z))
        TUNNELS.append((ROUTE[0], x, z, yA + 6))
end, y_end = flight((endA[0], -42), (1, 0), yA, FLOOR_T - yA)
corridor((end[0], -41), (9, -41), y_end); door(10, -41, FLOOR_T, "x")
ROUTE[0] = "T1 back room to the hall"
for y in range(25, 28):
    for z in range(-4, -1):
        for x in (-9, -8): clear((x, y, z)); SPACE.add((x, y, z))
end1, y1 = flight((-7, -3), (1, 0), 24, FLOOR_T - 24)
corridor((end1[0], -2), (15, -2), y1); corridor((15, -2), (15, -29), y1); door(15, -30, FLOOR_T, "z")
ROUTE[0] = "T4 valley floor to the core terrace"
for x in range(-23, -15):                               # a cut into the south peak's foot, level with the floor
    for z in range(8, 12):
        put((x, 31, z), KEY["walk"])
        for y in range(32, 46): SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
e4, ye4 = flight((-24, 9), (-1, 0), 31, 8)
e4b, ye4b = flight((e4[0] - 1, e4[1] + 1), (0, -1), ye4, 9)
corridor((e4b[0] + 1, e4b[1] - 1), (-22, e4b[1] - 1), ye4b)
e4c, ye4c = flight((-22, e4b[1] - 2), (0, -1), ye4b, 56 - ye4b, open_above=56)
report.append(f"tunnels: hall floor y {FLOOR_T}; spawn stairwell lands at y {yA}; core stairs: a cut at x -23..-19, "
              f"flights to {e4} y {ye4} and {e4b} y {ye4b}, a corridor east into the bunker's body, then a flight up "
              f"through the terrace to {e4c} y {ye4c}")

# ---------------------------------------------------------------- 7. the mountains, through the sketch's own surfaces
YELLOW, BLUE = KEY["flat"], KEY["mountain"]
sketch_top = {}
for (x, y, z), b in orig.items():
    if not in_half(x, z) or reference(x, y, z) or not 27 <= y <= 90: continue
    if b[0] == 35 and b[1] in (3, 4, 5, 13, 8) and y > sketch_top.get((x, z), (-1,))[0]:
        sketch_top[(x, z)] = (y, b)
structure_cols = {(x, z) for (x, y, z) in out if 30 <= y and not reference(x, y, z) and in_half(x, z)
                  and out[(x, y, z)] not in (KEY["walk"], KEY["sheet_face"], KEY["sheet_back"])
                  and (x, y, z) not in TUNNEL_BLOCKS}
taken = structure_cols | set(floor_top) | set(plane_top) | set(ramp_top) | SKY_OPEN | connector
# the shelf: everything inside the two walls' angle, up to the north peak, flat at the walls' top
shelf = set()
for x in range(44, 67):
    for z in range(-72, -30):
        if (x, z) in y_wall_cols: continue
        west = any((xx, z) in y_wall_cols for xx in range(40, x))
        south = any((min(x, 65), zz) in y_wall_cols for zz in range(z + 1, -27))
        if (west or z < -68) and south: shelf.add((x, z))
band = {c for c, (y, b) in sketch_top.items() if b in (YELLOW, BLUE)} | shelf
for _ in range(2):                                      # close the seams between the sketch's pieces
    band |= {(x + dx, z + dz) for (x, z) in band for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
             if sum((x + dx + ex, z + dz + ez) in band for ex, ez in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 3}
band = {c for c in band - taken if in_half(*c)}

wall_top_y = max(y for (x, y, z) in Y_WALLS)
h_base = min(y for (x, y, z) in H_DOME)
h_cols = {(x, z) for (x, y, z) in H_DOME}
points = []
for (x, z) in sorted(band):
    if (x, z) in shelf:
        if (x * 73 + z * 151) % 37 == 0: points.append((x, z, wall_top_y + ((x * 7 + z) % 3) * 0.4))
    elif (x, z) in sketch_top and (x * 73 + z * 151) % 29 == 0:
        points.append((x, z, sketch_top[(x, z)][0]))
for (x, z) in sorted(band):
    if (x * 5 + z * 3) % 3: continue
    near = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    if any(n in y_wall_cols for n in near): points.append((x, z, wall_top_y))
    elif any(n in plane_top for n in near): points.append((x, z, max(plane_top[n] for n in near if n in plane_top)))
    elif any(n in h_cols for n in near): points.append((x, z, h_base))
    elif any(n in PLATES for n in near): points.append((x, z, PLATE_Y - 1))
surface_at = terrain.fit(points, smooth=0.6)

buried = collections.defaultdict(lambda: -1)
for (x, y, z) in TUNNEL_BLOCKS | (SPACE - OPEN_SPACE):
    if y > buried[(x, z)]: buried[(x, z)] = y
colour_of = {c: b for c, (y, b) in sketch_top.items() if b in (YELLOW, BLUE)}
colour_of.update({c: YELLOW for c in shelf})
frontier = list(colour_of)
while frontier:                                          # a column the sketch left bare takes its nearest colour
    nxt = []
    for (x, z) in frontier:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n in band and n not in colour_of: colour_of[n] = colour_of[(x, z)]; nxt.append(n)
    frontier = nxt
heights = {}
for (x, z) in band:
    h = surface_at(x, z)
    if buried[(x, z)] >= 0: h = max(h, buried[(x, z)] + 5)
    heights[(x, z)] = int(round(min(88.0, max(FLOOR_Y + 1, h))))
for (x, z), top in heights.items():
    colour = colour_of.get((x, z), YELLOW)
    for k in range(3):
        cell = (x, top - k, z)
        if cell not in SPACE and cell not in out: put(cell, colour)
steps = collections.Counter()
for (x, z), top in heights.items():
    for n in ((x + 1, z), (x, z + 1)):
        if n in heights: steps[abs(top - heights[n])] += 1
report.append(f"mountains: {len(band)} columns drawn through {len(points)} points off the sketch's own surfaces; "
              f"y {min(heights.values())}..{max(heights.values())}; steps between neighbours "
              + ", ".join(f"{k}: {n}" for k, n in sorted(steps.items())))

# ---------------------------------------------------------------- 8. solid ground, straight down to the world's floor
GROUND = {KEY["walk"], YELLOW, BLUE, KEY["sheet_face"], KEY["sheet_back"]}
ground_tops, structure_floors, standing = {}, {}, {}
for (x, y, z), b in out.items():
    if not in_half(x, z) or reference(x, y, z) or (x, y, z) in TUNNEL_BLOCKS: continue
    if b in GROUND and (x, y, z) not in BUNKER:
        if y > ground_tops.get((x, z), -1): ground_tops[(x, z)] = y
    elif 20 <= y <= 40 and (x, y, z) not in SPACE:
        if y < structure_floors.get((x, z), 99): structure_floors[(x, z)] = y
for (x, y, z) in list(Y_WALLS) + list(H_DOME):           # a wall that stands on the ground has ground up to its base
    if y < standing.get((x, z), 999): standing[(x, z)] = y
tops = dict(ground_tops)
for col, y in structure_floors.items():
    if col not in tops: tops[col] = y
for col, y in standing.items():
    if y > tops.get(col, -1): tops[col] = y
for col in PLATES:                                       # the plates roof the spawn wing's body
    tops[col] = PLATE_Y
holes = 0
for _ in range(3):
    added = {}
    for x in range(HALF[0][0], HALF[0][1] + 1):
        for z in range(HALF[1][0], HALF[1][1] + 1):
            if (x, z) in tops or (x, z) in SKY_OPEN: continue
            near = [tops[(x + dx, z + dz)] for dx in (-1, 0, 1) for dz in (-1, 0, 1)
                    if (dx or dz) and (x + dx, z + dz) in tops]
            if len(near) >= 6: added[(x, z)] = min(near)
    for (x, z), y in added.items():
        tops[(x, z)] = y
        if (x, y, z) not in out: put((x, y, z), KEY["walk"])
    holes += len(added)
HOUSE = ((-27, -5), (-22, 5))
TERRACE_Y = 56
for x in range(HOUSE[0][0], HOUSE[0][1] + 1):           # the bunker's body behind the core, solid up to the terrace
    for z in range(HOUSE[1][0], HOUSE[1][1] + 1):
        if (x, z) in pit_cols or (x, z) in SKY_OPEN or tops.get((x, z), -1) >= TERRACE_Y: continue
        tops[(x, z)] = TERRACE_Y
        if (x, TERRACE_Y, z) not in out and (x, TERRACE_Y, z) not in SPACE: put((x, TERRACE_Y, z), STONE)


def open_patches():
    """Columns with no ground under them: those enclosed by ground, and those that run into an intended opening."""
    candidates = {(x, z) for x in range(HALF[0][0], HALF[0][1] + 1) for z in range(HALF[1][0], HALF[1][1] + 1)
                  if (x, z) not in tops and (x, z) not in SKY_OPEN}

    def flood(seeds):
        got = set(seeds); todo = list(seeds)
        while todo:
            x, z = todo.pop()
            for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                if n in candidates and n not in got: got.add(n); todo.append(n)
        return got

    outside = flood([c for c in candidates if c[0] in HALF[0] or c[1] in HALF[1]])
    beside = flood([c for c in candidates - outside
                    if any(n in SKY_OPEN for n in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)))])

    def groups(cells):
        found, left = [], set(cells)
        while left:
            seed = left.pop(); comp = [seed]; todo = [seed]
            while todo:
                x, z = todo.pop()
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    if n in left: left.remove(n); comp.append(n); todo.append(n)
            found.append(comp)
        return found
    return groups(candidates - outside - beside), groups(beside)


enclosed, beside = open_patches()
report.append(f"surface: {len(enclosed)} enclosed patches with no ground under them, closed:")
for comp in enclosed:
    cells = set(comp)
    if any(HOUSE[0][0] <= x <= HOUSE[0][1] and HOUSE[1][0] <= z <= HOUSE[1][1] for x, z in comp):
        level, why = TERRACE_Y, "the bunker's body, up to the terrace"
    else:
        ring = [ground_tops[n] for x, z in comp for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))
                if n not in cells and n in ground_tops]
        level, why = (min(ring) if ring else FLOOR_Y), "the lowest ground around it"
    for (x, z) in comp:
        tops[(x, z)] = level
        if (x, level, z) not in out: put((x, level, z), KEY["walk"])
    xs = [c[0] for c in comp]; zs = [c[1] for c in comp]
    report.append(f"    closed {len(comp):4d} columns  x {min(xs)}..{max(xs)}  z {min(zs)}..{max(zs)}  to y {level}, {why}")
for comp in beside:
    xs = [c[0] for c in comp]; zs = [c[1] for c in comp]
    report.append(f"    left open {len(comp):4d} columns  x {min(xs)}..{max(xs)}  z {min(zs)}..{max(zs)}  "
                  f"(runs into the canyon or the pit)")
FILLED = set()
for (x, z), top in tops.items():
    for y in range(0, top):
        cell = (x, y, z)
        if cell in out or cell in SPACE: continue
        out[cell] = FILL; FILLED.add(cell)
report.append(f"ground: {len(tops)} columns filled solid down to y 0, {len(FILLED)} blocks; {holes} holes in sheets closed")
after, _ = open_patches()
report.append(f"surface after the fill: {len(after)} enclosed patches with no ground under them")

# ---------------------------------------------------------------- 9. closure: where the sky reaches underground
UNDERGROUND = {(x, y, z) for (x, z) in roofed for y in range(0, ROOF_Y) if (x, y, z) not in out}
for name, tx, tz, roof in TUNNELS:
    for y in range(roof - 7, roof):
        if (tx, y, tz) in SPACE and (tx, y, tz) not in out and (tx, y, tz) not in OPEN_SPACE:
            UNDERGROUND.add((tx, y, tz))
ENTRIES = [
    ("main entrance: the lane runs out into the canyon and the ramp", (47, 67, 0, 60, -28, -24)),
    ("the lane's long side, open to the void", (65, 68, 0, 30, -52, -24)),
    ("the spawn door", (-11, -6, 30, 46, -50, -39)),
    ("the core stairs' cut in the south peak's foot", (-25, -15, 30, 46, 7, 13)),
    ("the core stairs' opening in the terrace", (-24, -18, 50, 62, -24, -5)),
    ("the back room, open from the top with the pit and its ramp", (-15, 14, 23, 31, -23, 1)),
]
X0, X1, Y0, Y1, Z0, Z1 = -62, 70, 0, 100, -112, 50
NX, NY, NZ = X1 - X0 + 1, Y1 - Y0 + 1, Z1 - Z0 + 1
solid = bytearray(NX * NY * NZ)
for (x, y, z) in out:
    if X0 <= x <= X1 and Y0 <= y <= Y1 and Z0 <= z <= Z1 and not reference(x, y, z):
        solid[((x - X0) * NY + (y - Y0)) * NZ + (z - Z0)] = 1
seen = bytearray(NX * NY * NZ)
stack = []
for xi in range(NX):
    for yi in range(NY):
        for zi in range(NZ):
            if (yi == NY - 1 or xi in (0, NX - 1) or zi in (0, NZ - 1)):
                i = (xi * NY + yi) * NZ + zi
                if not solid[i] and not seen[i]: seen[i] = 1; stack.append(i)
SX, SY = NY * NZ, NZ
while stack:
    i = stack.pop()
    xi, rem = divmod(i, SX); yi, zi = divmod(rem, SY)
    for j, ok in ((i - SX, xi > 0), (i + SX, xi < NX - 1), (i - SY, yi > 0), (i + SY, yi < NY - 1),
                  (i - 1, zi > 0), (i + 1, zi < NZ - 1)):
        if ok and not solid[j] and not seen[j]:
            seen[j] = 1; stack.append(j)


def reached(c):
    x, y, z = c
    return X0 <= x <= X1 and Y0 <= y <= Y1 and Z0 <= z <= Z1 and seen[((x - X0) * NY + (y - Y0)) * NZ + (z - Z0)]


openings = set()
for c in UNDERGROUND:
    if not reached(c): continue
    x, y, z = c
    for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
        if n not in UNDERGROUND and n not in out and reached(n):
            openings.add(c); break
groups, left = [], set(openings)
while left:
    seed = left.pop(); comp = [seed]; todo = [seed]
    while todo:
        x, y, z = todo.pop()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    n = (x + dx, y + dy, z + dz)
                    if n in left: left.remove(n); comp.append(n); todo.append(n)
    groups.append(comp)
leaks, lines = 0, []
for comp in sorted(groups, key=len, reverse=True):
    bb = [(min(c[k] for c in comp), max(c[k] for c in comp)) for k in range(3)]
    named = [n for n, (a0, a1, b0, b1, c0, c1) in ENTRIES
             if bb[0][0] <= a1 and bb[0][1] >= a0 and bb[1][0] <= b1 and bb[1][1] >= b0 and bb[2][0] <= c1 and bb[2][1] >= c0]
    leaks += not named
    lines.append(f"    opening {'ENTRY' if named else 'LEAK '} {len(comp):5d} cells  x {bb[0][0]}..{bb[0][1]}  "
                 f"y {bb[1][0]}..{bb[1][1]}  z {bb[2][0]}..{bb[2][1]}  {named[0] if named else ''}")
report.append(f"closure: {len(groups)} openings from the sky into the underground, {leaks} not an entry")
report.extend(lines)

# ---------------------------------------------------------------- 10. every tunnel below the ground over it
above = dict(tops)
exposed, raised = [], 0
for name, x, z, roof in TUNNELS:
    if (x, z) in SKY_OPEN: continue
    top = above.get((x, z))
    near = [above[(x + dx, z + dz)] for dx in (-1, 0, 1) for dz in (-1, 0, 1) if (dx or dz) and (x + dx, z + dz) in above]
    local = max(near) if near else None
    if (top is None or top < roof) and local is not None and roof - 1 <= local <= roof + 2:
        top = roof
    if top is not None and roof >= top and roof + 1 - top <= 2:
        for y in range(top + 1, roof + 2):
            if (x, y, z) not in out: put((x, y, z), KEY["walk"])
        above[(x, z)] = roof + 1; raised += 1
        continue
    if top is None or roof >= top:
        exposed.append((name, x, z, roof, top))
report.append(f"below ground: {len(TUNNELS)} tunnel and roof columns, {len(exposed)} with a roof at or above the ground "
              f"over them; {raised} where the floor was raised one or two blocks over a roof")
least = {}
for name, x, z, roof in TUNNELS:
    top = above.get((x, z))
    if top is None or (x, z) in SKY_OPEN: continue
    if name not in least or top - roof < least[name][0]: least[name] = (top - roof, x, z, roof, top)
for name, (cover, x, z, roof, top) in least.items():
    report.append(f"    {name}: least ground over the roof {cover} at ({x}, {z}), roof y {roof}, surface y {top}")
for name, x, z, roof, top in exposed[:15]:
    report.append(f"    exposed {name} at ({x}, {z}): roof y {roof}, ground {top}")

xray = {c: b for c, b in out.items() if c not in FILLED} if XRAY else None

# ---------------------------------------------------------------- 11. the turn
def turned_block(block):
    i, d = block
    if i in (53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180):
        return (i, (d & 4) | ({0: 1, 1: 0, 2: 3, 3: 2}[d & 3]))
    if i in (50, 75, 76, 77, 143):
        return (i, {1: 2, 2: 1, 3: 4, 4: 3}.get(d & 7, d & 7) | (d & 8))
    if i in (131, 183, 184, 185, 186, 187, 107):
        return (i, (d & ~3) | ((d + 2) & 3))
    return block


if ROTATE:
    cx, cz = CENTRE
    half = {c: b for c, b in out.items() if -60 <= c[0] <= 68 and c[1] <= 99 and -110 <= c[2] <= cz
            and not reference(*c)}
    for (x, y, z), b in half.items():
        out[(2 * cx - x, y, 2 * cz - z)] = turned_block(b)
        if XRAY and (x, y, z) not in FILLED: xray[(2 * cx - x, y, 2 * cz - z)] = turned_block(b)
    report.append(f"turned {len(half)} blocks 180 degrees about block {CENTRE}")

tiles = [{"id": "DLDetector", "x": x, "y": y, "z": z} for (x, y, z), b in out.items() if b[0] in (151, 178)]
chunks, regions = write_world(out, OUT, tile_entities=tiles)
report.append(f"wrote {len(out)} blocks in {chunks} chunks, {regions} regions -> {OUT}")
if XRAY:
    write_world(xray, XRAY, tile_entities=tiles)
    report.append(f"x-ray copy without the ground fill -> {XRAY}")
print("\n".join(report))
