"""Compose the fire-and-ice CTW/DTC sketch: one half integrated, then turned 180 degrees.

    python3 sketches/fire-and-ice/compose.py <source-region> <out-region>
        [--push N] [--head N] [--head-room N] [--cover N] [--no-rotate]

<source-region> is the author's sketch world (its four region files); nothing in it is written over.

Every new piece is wool in a colour of its own (the KEY below), with the control points of every lofted
surface left in place as marker blocks, the way the hand-built sketch carries its loft points.
"""
import math, sys, collections

import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
sys.path.insert(0, HERE)
from anvil import World
from anvilw import write_world
import loft

def opt(flag, default):
    return type(default)(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default

# ---------------------------------------------------------------- parameters
PUSH = opt("--push", 6)          # how far the wool lane sits below where its floating copy projects
HEAD = opt("--head", 8)          # air above the lane's walk surface, under the bedrock roof
HEAD_ROOM = opt("--head-room", 8)  # air above the raised wool-room floor
COVER_MIN = opt("--cover", 4)    # ground required between the roof's top and the surface above it
CENTRE = (24, 48)                # the 180-degree turn's pivot: block (24, 48)
ROTATE = "--no-rotate" not in sys.argv
OFFSET = (-35, -61, -43)         # floating copy -> ground, measured off the two cores

W = lambda d: (35, d)
KEY = {
    "walk": W(8), "lane": W(0), "roof_top": W(7), "facade": W(7), "sheet_face": W(5), "sheet_back": W(13),
    "terrain_low": W(4), "terrain_high": W(3), "crack": W(0), "tunnel_wall": W(9), "tunnel_floor": W(12),
    "tunnel_roof": W(11), "stair_wall": W(1), "hall_wall": W(2), "wool_goal": W(14), "void": W(10),
    "goal_plinth": W(15),
}
BEDROCK = (7, 0)
MARK_SHEET, MARK_CRACK, MARK_TERRAIN = (133, 0), (42, 0), (41, 0)

src = World(SRC)
orig = {(x, y, z): (i, d) for x, y, z, i, d in src.blocks()}
out = dict(orig)
report = []

def put(cell, block):
    out[cell] = block

def clear(cell):
    out.pop(cell, None)

TERRAIN_WOOL = {0, 3, 4, 5, 8, 13, 6}
MARKERS = {41, 57, 133, 42}

def is_terrain(block):
    return block[0] == 35 and block[1] in TERRAIN_WOOL or block[0] in MARKERS

# ---------------------------------------------------------------- 1. clear the exploratory ravine shells
for cell, block in list(out.items()):
    x, y, z = cell
    if y <= 27 and not (-1 <= x <= 1 and -1 <= z <= 1) and -60 <= x <= 70 and -110 <= z <= 40:
        clear(cell)

# ---------------------------------------------------------------- 2. the detailed bunker into the old one's place
STRUCTURE = {1, 4, 7, 49, 11, 44, 98, 109, 139, 101, 160, 113, 112, 114, 126, 155, 156, 108, 45, 5, 67, 136, 152,
             76, 55, 77, 178, 191, 186, 131, 82, 159, 95}
CORE_BOX = ((-9, -3), (39, 56), (-22, -9))
TERRACE = ((-21, -9), (56, 56), (-20, -11))

def inside(cell, box):
    return all(lo <= v <= hi for v, (lo, hi) in zip(cell, box))

for cell, block in list(out.items()):
    x, y, z = cell
    if -30 <= x <= 16 and 28 <= y <= 84 and -67 <= z <= 8:
        if block[0] in STRUCTURE or (block[0] == 35 and block[1] in (1, 6, 7, 14, 15)):
            clear(cell)
for cell, block in orig.items():
    x, y, z = cell
    if 8 <= x <= 52 and 85 <= y <= 157 and -22 <= z <= 47:
        put((x + OFFSET[0], y + OFFSET[1], z + OFFSET[2]), block)
for cell, block in orig.items():
    if inside(cell, CORE_BOX) or inside(cell, TERRACE):
        put(cell, block)
pit = {(x, z) for (x, y, z), b in out.items() if b == KEY["void"] and y == 24}
for (x, z) in pit:                                          # sink the purple pit into the floor
    for y in range(25, 41):
        if (x, y, z) in out and is_terrain(out[(x, y, z)]):
            clear((x, y, z))
report.append(f"bunker: floating copy lowered by {OFFSET}; old core's lava and terrace kept; pit {len(pit)} cells sunk")

# ---------------------------------------------------------------- 3. the wool lane
LANE_SRC = ((70, 101), (63, 81), (-25, 40))
DY = OFFSET[1] - PUSH
lane = {}
for cell, block in orig.items():
    if inside(cell, LANE_SRC):
        lane[(cell[0] + OFFSET[0], cell[1] + DY, cell[2] + OFFSET[2])] = block
L = 75 + DY                       # the lane's walk surface (its white top)
ROOM = 81 + DY                    # the raised wool area's highest walk surface
R_LANE = L + HEAD + 1             # bedrock roof over the lane
R_ROOM = ROOM + HEAD_ROOM + 1     # bedrock roof over the wool area

# underground envelope, lowered coordinates: the wool area, then the lane's north half and its cross bar
U_ROOM = ((34, 64), (-68, -50))
U_LANE = ((34, 66), (-51, -34))
CANYON = ((48, 66), (-33, -4))

def surface_y(x, z, ymin, ymax=86):
    ys = [y for y in range(ymax, ymin - 1, -1) if (x, y, z) in out and is_terrain(out[(x, y, z)])]
    return ys[0] if ys else None

def roof_for(x, z):
    if U_ROOM[0][0] <= x <= U_ROOM[0][1] and U_ROOM[1][0] <= z <= U_ROOM[1][1]:
        return R_ROOM
    if U_LANE[0][0] <= x <= U_LANE[0][1] and U_LANE[1][0] <= z <= U_LANE[1][1]:
        return R_LANE
    return None

# cover check against the ground as it stands, before anything is carved
cover_rows = []
for x in range(34, 67):
    for z in range(-68, -33):
        roof = roof_for(x, z)
        if roof is None: continue
        top = surface_y(x, z, roof + 1)
        if top is None: continue
        cover_rows.append((top - roof - 1, x, z, top, roof))
cover_rows.sort()
short = [r for r in cover_rows if r[0] < COVER_MIN]
report.append(f"lane: walk y={L}, wool area y={ROOM}, roof y={R_LANE} (lane) / {R_ROOM} (room); "
              f"cover min {cover_rows[0][0] if cover_rows else '-'} over {len(cover_rows)} roofed columns; "
              f"{len(short)} below {COVER_MIN}")
for c, x, z, top, roof in short[:12]:
    report.append(f"    short cover {c:3d} at ({x}, {z}): surface y {top}, roof y {roof}")

# carve the cavity out of any ground, then lay the lane in
for x in range(33, 68):
    for z in range(-69, -3):
        roof = roof_for(x, z)
        top = roof if roof is not None else 40 if inside((x, 0, z), (CANYON[0], (0, 0), CANYON[1])) else None
        if top is None: continue
        for y in range(L - 8, top + 1):
            if (x, y, z) in out and is_terrain(out[(x, y, z)]):
                clear((x, y, z))
for cell, block in lane.items():
    put(cell, block)

# walls, roof and the opening the lane leaves on its east side
def wall_column(x, z, top):
    for y in range(L - 6, top):
        if (x, y, z) in out: continue
        put((x, y, z), BEDROCK if y <= L + 3 else KEY["facade"])

for x in range(U_ROOM[0][0], U_ROOM[0][1] + 1):
    for z in range(U_ROOM[1][0], U_ROOM[1][1] + 1):
        put((x, R_ROOM, z), BEDROCK); put((x, R_ROOM + 1, z), KEY["roof_top"])
        edge = x in U_ROOM[0] or z == U_ROOM[1][0] or (z == U_ROOM[1][1] and not 50 <= x <= 66)
        if edge: wall_column(x, z, R_ROOM)
for x in range(U_LANE[0][0], U_LANE[0][1] + 1):
    for z in range(U_LANE[1][0], U_LANE[1][1] + 1):
        if roof_for(x, z) != R_LANE: continue
        put((x, R_LANE, z), BEDROCK); put((x, R_LANE + 1, z), KEY["roof_top"])
        west = x == U_LANE[0][0] and not -39 <= z <= -34          # the west arm stays open to its tunnel
        south = z == U_LANE[1][1] and not 48 <= x <= 66           # the lane runs out south into the canyon
        if west or south: wall_column(x, z, R_LANE)
for x in range(50, 65):                                              # the step between the two roofs
    for y in range(R_LANE + 1, R_ROOM):
        put((x, y, U_ROOM[1][1]), KEY["facade"])
# the wool itself: a plinth on the raised floor, the goal block on it
gx, gz = 47, -60
floor_y = max(y for (x, y, z) in lane if (x, z) == (gx, gz) and lane[(x, y, z)][0] == 35)
for dx in (-1, 0, 1):
    for dz in (-1, 0, 1):
        put((gx + dx, floor_y + 1, gz + dz), KEY["goal_plinth"])
put((gx, floor_y + 2, gz), KEY["wool_goal"])
report.append(f"wool: plinth at ({gx}, {floor_y + 1}, {gz}), the goal block at y {floor_y + 2}")

# ---------------------------------------------------------------- 4. the drift ramp down into the lane's south end
def lerp(f):
    return L + (30 - L) * f

ramp_rows = [
    [(52, L, -6), (58, L, -6), (65, L, -6)],
    [(51, lerp(0.25) + 1, 6), (58, lerp(0.25), 6), (65, lerp(0.25), 6)],
    [(48, lerp(0.5) + 1, 18), (55, lerp(0.5), 18), (63, lerp(0.5) - 0.5, 19)],
    [(44, lerp(0.78) + 1, 28), (51, lerp(0.78), 29), (58, lerp(0.78) - 1, 31)],
    [(36, 30, 36), (44, 30, 38), (52, 29.5, 40)],
]
ramp_grid = loft.surface(ramp_rows, density=0.35)
ramp_top = {}
for row in ramp_grid:
    for p in row:
        cx, cy, cz = math.floor(p[0]), math.floor(p[1]), math.floor(p[2])
        ramp_top[(cx, cz)] = max(ramp_top.get((cx, cz), -99), cy)
for (x, z), y in ramp_top.items():
    for yy in range(y + 1, y + 14):                     # open the cut where the ramp is below the floor
        if (x, yy, z) in out and is_terrain(out[(x, yy, z)]):
            clear((x, yy, z))
    put((x, y, z), KEY["walk"]); put((x, y - 1, z), KEY["walk"])
for row in ramp_rows:
    for p in row: put(tuple(map(math.floor, p)), MARK_SHEET)
report.append(f"ramp: {len(ramp_top)} columns, from y {L} at z -6 to y 30 at z 38")

# ---------------------------------------------------------------- 5. the retaining sheet along the floor's east edge
sheet_top = [(47.5, 34, -34), (45.5, 34, -32), (40.5, 32, -20), (38.5, 31, -7), (43.5, 31, 4), (44.5, 30.5, 16),
             (40.5, 30, 26), (35.5, 30, 35)]
sheet_bottom = [(49.5, L - 4, -34), (47.5, L - 4, -32), (46.5, L + 3, -20), (44.5, L - 4, -7),
                (49.5, lerp(0.25) - 1, 6), (46.5, lerp(0.5) - 1, 18), (42.5, lerp(0.78) - 1, 28), (36.5, 29, 36)]
sheet = loft.surface([sheet_bottom, sheet_top], density=0.3)
for sign in (1, -1):
    layers = loft.voxels(sheet, thickness=2, normal_sign=sign)
    cx0 = sum(c[0] for c in layers[0]) / len(layers[0]); cx1 = sum(c[0] for c in layers[1]) / len(layers[1])
    if cx1 < cx0: break                                  # the back layer sits on the ground side, west
for cell in layers[1]:
    if cell not in out or is_terrain(out[cell]): put(cell, KEY["sheet_back"])
for cell in layers[0]:
    if cell not in out or is_terrain(out[cell]): put(cell, KEY["sheet_face"])
for p in sheet_top + sheet_bottom: put(tuple(map(math.floor, p)), MARK_SHEET)

# ---------------------------------------------------------------- 6. cracks, placed on purpose
def crack(rings, carve_top_y=None, open_bottom=True, clip=None):
    """A ravine as rings of points, top to bottom, lofted into a one-block shell; the ground inside the top ring
    is carved and every ring's points are left as iron markers."""
    grid = loft.surface(rings, closed_rows=True, density=0.45)
    shell = loft.voxels(grid, thickness=1, closed_rows=True)[0]
    polys = [(r[0][1], [(p[0], p[2]) for p in loft.curve(r, closed=True)]) for r in rings]
    y_low = min(r[0][1] for r in rings) - 1; y_high = max(r[0][1] for r in rings) + 8
    for y in range(int(y_low), int(y_high)):
        poly = min(polys, key=lambda pr: abs(pr[0] - y))[1]
        xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
        for x in range(math.floor(min(xs)) - 1, math.ceil(max(xs)) + 2):
            for z in range(math.floor(min(zs)) - 1, math.ceil(max(zs)) + 2):
                if loft.polygon_contains(poly, x + 0.5, z + 0.5) and (x, y, z) in out and \
                        (is_terrain(out[(x, y, z)]) or out[(x, y, z)] in (BEDROCK, KEY["roof_top"])):
                    clear((x, y, z))
    for cell in shell:
        if clip and clip(cell): continue
        if cell not in out or is_terrain(out[cell]): put(cell, KEY["crack"])
    for ring in rings:
        for p in ring: put(tuple(map(math.floor, p)), MARK_CRACK)
    return len(shell)

def ring(cx, y, cz, length, width, turn_deg, wobble=0.0, n=8):
    t = math.radians(turn_deg); pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1 + wobble * math.sin(3 * a + cx)
        u, v = math.cos(a) * length / 2 * r, math.sin(a) * width / 2 * r
        pts.append((cx + u * math.cos(t) - v * math.sin(t), y, cz + u * math.sin(t) + v * math.cos(t)))
    return pts

# K1: a drop from the floor into the west arm of the lane, the way in that skips the long walk down
k1 = crack([ring(38, 31, -36.5, 12, 4.5, 4, 0.12), ring(39, 27, -36.5, 10, 3.5, -3, 0.15),
            ring(39.5, R_LANE + 1, -36.5, 9, 4, 2, 0.1)],
           clip=lambda c: inside(c, ((35, 50), (L, R_LANE - 1), (-39, -34))))
report.append(f"cracks: K1 into the west arm ({k1} shell blocks)")

# ---------------------------------------------------------------- 7. the ground between the halves
def loft_terrain(rows, block, thickness=1, marker=MARK_TERRAIN):
    grid = loft.surface(rows, density=0.4)
    cells = set().union(*loft.voxels(grid, thickness=thickness))
    for cell in cells:
        if cell not in out: put(cell, block)
    for row in rows:
        for p in row: put(tuple(map(math.floor, p)), marker)
    return len(cells)

def south_edge(x):
    """The valley floor's southern edge at column x: the last floor block going south, and its height."""
    best = None
    for z in range(10, 40):
        for y in range(26, 34):
            if orig.get((x, y, z)) == KEY["walk"]:
                best = (z, y)
    return best

edge = []
for x in range(-6, 53, 6):
    found = south_edge(x)
    if found: edge.append((x, found[1], found[0] - 1))
report.append("floor's south edge: " + ", ".join(f"({x},{y},{z})" for x, y, z in edge))
connector = loft_terrain([
    edge,
    [(x, 30, 38 + (2 if 6 < x < 40 else 0)) for x, _, _ in edge],
    [(x, 30, 48) for x in range(-6, 55, 6)],
], KEY["walk"], thickness=2)
spur_rows = [
    [(-50, 62, 24), (-36, 58, 26), (-22, 46, 27), (-8, 32, 28)],
    [(-48, 58, 36), (-32, 53, 37), (-18, 41, 37), (-6, 31, 38)],
    [(-42, 50, 48), (-26, 45, 48), (-14, 36, 48), (-5, 31, 48)],
]
spur = loft_terrain(spur_rows, KEY["terrain_low"])
report.append(f"middle: connector {connector} blocks, west spur {spur}")
# K2: the mid crack, one per half; the turn makes the pair a staggered S across the centre line
k2 = crack([ring(17, 31, 39, 24, 5, 12, 0.15, 10), ring(18, 24, 39.5, 21, 4, 8, 0.2, 10),
            ring(19, 14, 40, 17, 3, 15, 0.25, 10), ring(19.5, 4, 40.5, 12, 2, 10, 0.2, 10)])
report.append(f"cracks: K2 mid ({k2} shell blocks)")

# ---------------------------------------------------------------- 8. the mountain the bunker is sunk into
def face_line():
    rows = []
    for z in range(-66, 9, 8):
        xs = [x for (x, y, zz), b in out.items() if zz == z and -32 <= x <= 16 and 30 <= y <= 84
              and b[0] in STRUCTURE | {49}]
        if not xs: continue
        fx = min(xs)
        ys = [y for (x, y, zz), b in out.items() if zz == z and fx <= x <= fx + 6 and 30 <= y <= 84
              and b[0] in STRUCTURE]
        rows.append((fx, max(ys), z))
    return rows

face = face_line()
row0 = [(fx - 1.5, top - 3, z) for fx, top, z in face]
row1 = [(fx - 9, top + 5, z) for fx, top, z in face]
row2 = [(-40, top + 11, z) for fx, top, z in face]
row3 = [(-53, top - 4, z) for fx, top, z in face]
cap_low = loft_terrain([row0, row1], KEY["terrain_low"], thickness=2)
cap_high = loft_terrain([row1, row2, row3], KEY["terrain_high"], thickness=2)
report.append(f"bunker mountain: face sampled at {len(face)} stations; {cap_low} + {cap_high} blocks")

# ---------------------------------------------------------------- 9. tunnels
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
                    if cell not in out or is_terrain(out[cell]): put(cell, block)
                else:
                    if cell in out and (is_terrain(out[cell]) or out[cell][0] in (35,)): clear(cell)
    return n + 1

def flight(start, direction, y, dy_total):
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
                if dy == 0 or dy == 5 or w in (-1, 2):
                    block = KEY["tunnel_floor"] if dy == 0 else KEY["tunnel_roof"] if dy == 5 else KEY["stair_wall"]
                    if cell not in out or is_terrain(out[cell]): put(cell, block)
                elif cell in out and is_terrain(out[cell]): clear(cell)
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
                if dy == 0: put(cell, KEY["tunnel_floor"])
                elif dy == height + 1: put(cell, KEY["tunnel_roof"])
                elif edge: put(cell, KEY["hall_wall"])
                elif cell in out and is_terrain(out[cell]): clear(cell)

def door(x, z, y, axis):
    for w in (-1, 0, 1):
        for dy in (1, 2, 3):
            cell = (x + (w if axis == "z" else 0), y + dy, z + (w if axis == "x" else 0))
            clear(cell)

FLOOR_T = L - 1          # the tunnel floor block sits one under the lane's walk surface
H1 = (10, -46, 21, -30)
hall(*H1, FLOOR_T, height=6)
# T3: the hall to the lane's west arm
corridor((22, -37), (35, -37), FLOOR_T); door(21, -37, FLOOR_T, "x")
# T2: from behind the spawn door, down under the valley floor to the hall
end, y_end = flight((-26, -42), (1, 0), 31, FLOOR_T - 31)
corridor((end[0], -41), (9, -41), y_end); door(10, -41, FLOOR_T, "x")
# T1: the back room behind the purple pit, down and along to the hall's south door
for y in range(25, 28):
    for z in range(-4, -1):
        for x in (-9, -8): clear((x, y, z))
end1, y1 = flight((-7, -3), (1, 0), 24, FLOOR_T - 24)
corridor((end1[0], -2), (15, -2), y1); corridor((15, -2), (15, -29), y1); door(15, -30, FLOOR_T, "z")
# T4: up from the floor south of the house to the core's terrace at y 56
e4, ye4 = flight((-1, 9), (-1, 0), 30, 18)
e4b, ye4b = flight(e4, (0, -1), ye4, 56 - ye4)
corridor((e4b[0] + 1, e4b[1]), (e4b[0] + 1, -15), 56); corridor((e4b[0] + 1, -15), (-21, -15), 56)
report.append(f"tunnels: hall at x {H1[0]}..{H1[2]} z {H1[1]}..{H1[3]} floor y {FLOOR_T}; T2 stairs end {end} y {y_end}; "
              f"T1 stairs end {end1} y {y1}; core climb ends {e4b} y {ye4b} then along y 56 to the terrace")

# ---------------------------------------------------------------- 10. the turn
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
    half = {c: b for c, b in out.items()
            if -60 <= c[0] <= 68 and c[1] <= 86 and -110 <= c[2] <= cz
            and not (8 <= c[0] <= 52 and c[1] >= 85 and -22 <= c[2] <= 47)}
    for (x, y, z), b in half.items():
        out[(2 * cx - x, y, 2 * cz - z)] = turned_block(b)
    report.append(f"turned {len(half)} blocks 180 degrees about block {CENTRE}")

tiles = [{"id": "DLDetector", "x": x, "y": y, "z": z} for (x, y, z), b in out.items() if b[0] in (151, 178)]
chunks, regions = write_world(out, OUT, tile_entities=tiles)
report.append(f"wrote {len(out)} blocks in {chunks} chunks, {regions} regions -> {OUT}")
print("\n".join(report))
