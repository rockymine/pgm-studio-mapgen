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
import band as band_field

def opt(flag, default):
    return type(default)(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default

# ---------------------------------------------------------------- parameters
PUSH = opt("--push", 6)          # how far the wool lane sits below where its floating copy projects
HEAD = opt("--head", 8)          # air above the lane's walk surface, under the bedrock roof
HEAD_ROOM = opt("--head-room", 8)  # air above the raised wool-room floor
COVER_MIN = opt("--cover", 4)    # ground required between the roof's top and the surface above it
TAPER = opt("--taper", 2.5)      # how fast the ground's underside rises toward the map's edge; 0 fills to y 0
CENTRE = (24, 48)                # the 180-degree turn's pivot: block (24, 48)
ROTATE = "--no-rotate" not in sys.argv
XRAY = sys.argv[sys.argv.index("--xray") + 1] if "--xray" in sys.argv else None
OFFSET = (-35, -61, -43)         # floating copy -> ground, measured off the two cores

W = lambda d: (35, d)
KEY = {
    "walk": W(8), "lane": W(0), "roof_top": W(7), "facade": W(7), "sheet_face": W(5), "sheet_back": W(13),
    "terrain_low": W(4), "terrain_high": W(3), "crack": W(0), "tunnel_wall": W(9), "tunnel_floor": W(12),
    "tunnel_roof": W(11), "stair_wall": W(1), "hall_wall": W(2), "wool_goal": W(14), "void": W(10),
    "goal_plinth": W(15),
}
BEDROCK = (7, 0)
FILL = (1, 0)          # solid ground under every surface; its texture is not decided
MARK_SHEET, MARK_CRACK, MARK_TERRAIN = (133, 0), (42, 0), (41, 0)

src = World(SRC)
orig = {(x, y, z): (i, d) for x, y, z, i, d in src.blocks()}
out = dict(orig)
report = []

SPACE = set()          # cells that must stay air: every carved space, so the ground fill leaves them open
TUNNELS = []           # (route, x, z, roof_y) for every tunnel column, for the below-ground check
ROUTE = ["-"]          # the route the next tunnel piece belongs to
SKY_OPEN = set()       # columns meant to stand open to the sky all the way down: the canyon, the cracks, the pit
TUNNEL_BLOCKS = set()  # blocks the tunnels placed, which the band buries rather than meets
OPEN_SPACE = set()     # carved cells open to the sky by design: cuts, the canyon, cracks, the pit, doorways

def tput(cell, block):
    put(cell, block); TUNNEL_BLOCKS.add(cell)

def put(cell, block):
    out[cell] = block

def space_box(x0, x1, y0, y1, z0, z1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                SPACE.add((x, y, z))

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
BUNKER = set()
for cell, block in orig.items():
    x, y, z = cell
    if 8 <= x <= 52 and 85 <= y <= 157 and -22 <= z <= 47:
        moved = (x + OFFSET[0], y + OFFSET[1], z + OFFSET[2])
        put(moved, block); BUNKER.add(moved)
for cell, block in orig.items():
    if inside(cell, CORE_BOX) or inside(cell, TERRACE):
        put(cell, block)
pit = {(x, z) for (x, y, z), b in out.items() if b == KEY["void"] and y == 24 and z <= -9}
for (x, z) in pit:                                          # sink the purple pit into the floor
    for y in range(25, 41):
        if (x, y, z) in out and is_terrain(out[(x, y, z)]):
            clear((x, y, z))
    for y in list(range(0, 24)) + list(range(25, 41)):
        SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
    SKY_OPEN.add((x, z))
for (x, y, z), b in list(out.items()):
    if b == KEY["void"] and y == 24 and z > -9:
        for yy in range(25, 29):
            if (x, yy, z) not in out: SPACE.add((x, yy, z))
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
space_box(U_ROOM[0][0], U_ROOM[0][1], 0, R_ROOM - 1, U_ROOM[1][0], U_ROOM[1][1])
space_box(U_LANE[0][0], U_LANE[0][1], 0, R_LANE - 1, U_LANE[1][0], U_LANE[1][1])
space_box(CANYON[0][0], CANYON[0][1], 0, 60, CANYON[1][0], CANYON[1][1])
OPEN_SPACE.update((x, y, z) for x in range(CANYON[0][0], CANYON[0][1] + 1) for y in range(0, 61)
                  for z in range(CANYON[1][0], CANYON[1][1] + 1))
SKY_OPEN.update((x, z) for x in range(CANYON[0][0], CANYON[0][1] + 1) for z in range(CANYON[1][0], CANYON[1][1] + 1))

# walls, roof and the opening the lane leaves on its east side
def wall_column(x, z, top):
    for y in range(0, top):
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
for x in range(U_ROOM[0][0], U_ROOM[0][1] + 1):
    for z in range(U_ROOM[1][0], U_ROOM[1][1] + 1):
        TUNNELS.append(("the wool area's roof", x, z, R_ROOM + 1))
for x in range(U_LANE[0][0], U_LANE[0][1] + 1):
    for z in range(U_LANE[1][0], U_LANE[1][1] + 1):
        if roof_for(x, z) == R_LANE: TUNNELS.append(("the lane's roof", x, z, R_LANE + 1))
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
    for yy in range(y + 1, 61):
        SPACE.add((x, yy, z)); OPEN_SPACE.add((x, yy, z))
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
def crack(rings, carve_top_y=None, open_bottom=True, clip=None, to_void=False):
    """A ravine as rings of points, top to bottom, lofted into a one-block shell; the ground inside the top ring
    is carved and every ring's points are left as iron markers."""
    grid = loft.surface(rings, closed_rows=True, density=0.45)
    shell = loft.voxels(grid, thickness=1, closed_rows=True)[0]
    polys = [(r[0][1], [(p[0], p[2]) for p in loft.curve(r, closed=True)]) for r in rings]
    y_low = 0 if to_void else min(r[0][1] for r in rings) - 1; y_high = max(r[0][1] for r in rings) + 30
    for y in range(int(y_low), int(y_high)):
        poly = min(polys, key=lambda pr: abs(pr[0] - y))[1]
        xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
        for x in range(math.floor(min(xs)) - 1, math.ceil(max(xs)) + 2):
            for z in range(math.floor(min(zs)) - 1, math.ceil(max(zs)) + 2):
                if not loft.polygon_contains(poly, x + 0.5, z + 0.5): continue
                SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
                if y == int(max(r[0][1] for r in rings)): SKY_OPEN.add((x, z))
                if (x, y, z) in out and \
                        (is_terrain(out[(x, y, z)]) or out[(x, y, z)] in (BEDROCK, KEY["roof_top"])):
                    clear((x, y, z))
    for cell in shell:
        if clip and clip(cell): continue
        if cell not in out or is_terrain(out[cell]):
            put(cell, KEY["crack"]); SPACE.discard(cell)
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
report.append(f"middle: connector {connector} blocks")
# K2: the mid crack, one per half; the turn makes the pair a staggered S across the centre line
k2 = crack([ring(17, 31, 39, 24, 5, 12, 0.15, 10), ring(18, 24, 39.5, 21, 4, 8, 0.2, 10),
            ring(19, 14, 40, 17, 3, 15, 0.25, 10), ring(19.5, 4, 40.5, 12, 2, 10, 0.2, 10)], to_void=True)
report.append(f"cracks: K2 mid ({k2} shell blocks)")

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
                    if cell not in out or is_terrain(out[cell]): tput(cell, block)
                else:
                    SPACE.add(cell)
                    if cell in out and (is_terrain(out[cell]) or out[cell][0] in (35,)): clear(cell)
            TUNNELS.append((ROUTE[0], px, pz, y + 4))
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
                    if cell not in out or is_terrain(out[cell]): tput(cell, block)
                else:
                    SPACE.add(cell)
                    if cell in out and is_terrain(out[cell]): clear(cell)
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

FLOOR_T = L - 1          # the tunnel floor block sits one under the lane's walk surface
H1 = (10, -46, 21, -30)
ROUTE[0] = "hall"
hall(*H1, FLOOR_T, height=6)
# T3: the hall to the lane's west arm
ROUTE[0] = "T3 hall to the west arm"
corridor((22, -37), (35, -37), FLOOR_T); door(21, -37, FLOOR_T, "x")
# the spawn room, behind the door frame at x -9..-8, z -49..-40, which faces the valley
SPAWN = (-26, -11, -50, -39, 31)
ROUTE[0] = "spawn room"
hall(SPAWN[0], SPAWN[2], SPAWN[1], SPAWN[3], SPAWN[4], height=9)
for z in range(-48, -40):                              # the room opens into the frame, the frame onto the valley
    for y in range(32, 45):
        for x in (-11, -10, -9, -8, -7):
            if y <= 40 or x >= -9:
                if x <= -10: clear((x, y, z))
                SPACE.add((x, y, z))
                if x >= -9: OPEN_SPACE.add((x, y, z))
    for y in range(41, 47):                            # the lintel over the passage between the room and the frame
        put((-10, y, z), FILL)
    for x in range(-11, -6):                           # the doorway's floor, level with the room's
        if (x, 31, z) not in out: put((x, 31, z), KEY["walk"])
# T2: a switchback stairwell from the spawn room's floor: west into the mountain, a landing, then east
# well under the bunker's foundations and the valley floor to the hall
ROUTE[0] = "T2 spawn to the hall"
endA, yA = flight((-13, -47), (-1, 0), 31, -12)
landing = (endA[0] - 4, endA[0], -48, -39)
hall(landing[0], landing[2], landing[1], landing[3], yA, height=5)
for z in range(-47, -39):
    for y in range(yA + 1, yA + 6):
        clear((landing[1], y, z)); SPACE.add((landing[1], y, z))
end, y_end = flight((endA[0] - 1, -42), (1, 0), yA, FLOOR_T - yA)
corridor((end[0], -41), (9, -41), y_end); door(10, -41, FLOOR_T, "x")
# T1: the back room behind the purple pit, down and along to the hall's south door
for y in range(25, 28):
    for z in range(-4, -1):
        for x in (-9, -8): clear((x, y, z)); SPACE.add((x, y, z))
ROUTE[0] = "T1 back room to the hall"
end1, y1 = flight((-7, -3), (1, 0), 24, FLOOR_T - 24)
corridor((end1[0], -2), (15, -2), y1); corridor((15, -2), (15, -29), y1); door(15, -30, FLOOR_T, "z")
# T4: the core's terrace from the valley floor, entirely inside the south peak and the mountain behind the house.
# A mouth cut into the peak's foot at x -23, a flight west under the peak, a flight north under the mountain,
# then a corridor east at the terrace's height to a door in the house's west wall.
T4_MOUTH = (-24, 6, 31)
for x in range(-23, -18):                              # an open cut into the peak's foot, level with the floor
    for z in range(4, 8):
        if (x, 31, z) not in out or is_terrain(out[(x, 31, z)]): put((x, 31, z), KEY["walk"])
        for y in range(32, 46):
            SPACE.add((x, y, z)); OPEN_SPACE.add((x, y, z))
            if (x, y, z) in out and is_terrain(out[(x, y, z)]): clear((x, y, z))
ROUTE[0] = "T4 valley floor to the core terrace"
e4, ye4 = flight((-24, 5), (-1, 0), 31, 9)
e4b, ye4b = flight((e4[0] - 1, e4[1] + 1), (0, -1), ye4, 56 - ye4)
corridor((e4b[0] + 1, e4b[1]), (e4b[0] + 1, -15), 56)
corridor((e4b[0] + 1, -15), (-28, -15), 56)
door(-27, -15, 56, "x")
for x in range(-27, -21):
    for z in range(-16, -13):
        if (x, 56, z) not in out: put((x, 56, z), KEY["tunnel_floor"])
report.append(f"tunnels: hall at x {H1[0]}..{H1[2]} z {H1[1]}..{H1[3]} floor y {FLOOR_T}; T2 stairs end {end} y {y_end}; "
              f"T1 stairs end {end1} y {y1}; core stairs: mouth {T4_MOUTH}, flights end {e4} y {ye4} and {e4b} y {ye4b}, "
              f"then y 56 to a door in the house's west wall at x -27")

# ---------------------------------------------------------------- 9b. the mountain band
HALF = ((-60, 68), (-110, 48))
def reference(x, y, z):
    return 8 <= x <= 52 and y >= 85 and -22 <= z <= 47

def in_half(x, z):
    return HALF[0][0] <= x <= HALF[0][1] and HALF[1][0] <= z <= HALF[1][1]

YELLOW, BLUE = (35, 4), (35, 3)
style_pins, footprint = {}, set()
style_top = {}
for (x, y, z), b in orig.items():
    if not in_half(x, z) or not 27 <= y <= 86 or reference(x, y, z): continue
    if b[0] == 35 and b[1] in (0, 3, 4, 5, 8, 13): footprint.add((x, z))
    if b in (YELLOW, BLUE) and y > style_top.get((x, z), -1):
        style_top[(x, z)] = y; style_pins[(x, z)] = 1.0 if b == BLUE else 0.0
for (x, y, z), b in list(out.items()):           # the sketch's mountain shells and their loft points give way
    if in_half(x, z) and 27 <= y <= 86 and not reference(x, y, z) and (x, y, z) not in BUNKER \
            and (b in (YELLOW, BLUE) or (b[0] in (41, 57) and orig.get((x, y, z)) == b)):
        clear((x, y, z))

LOW_GROUND = {(35, 8), (35, 5), (35, 13)}
ground_top, struct_top, struct_base, under = {}, {}, {}, collections.defaultdict(lambda: -1)
for (x, y, z), b in out.items():
    if not in_half(x, z) or y > 86 or reference(x, y, z): continue
    col = (x, z)
    if (x, y, z) in TUNNEL_BLOCKS or y < 28:
        if y > under[col]: under[col] = y
        continue
    if b in LOW_GROUND and (x, y, z) not in BUNKER:
        if y > ground_top.get(col, -1): ground_top[col] = y
    elif b[0] not in (133, 42):
        if y > struct_top.get(col, -1): struct_top[col] = y
        if y < struct_base.get(col, 999): struct_base[col] = y
for (x, y, z) in SPACE - OPEN_SPACE:
    if in_half(x, z) and y <= 86 and y > under[(x, z)]: under[(x, z)] = y

def polygon_cells(poly):
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    return {(x, z) for x in range(min(xs), max(xs) + 1) for z in range(min(zs), max(zs) + 1)
            if loft.polygon_contains(poly, x + 0.5, z + 0.5)}

BAND_REACH = [
    [(-56, -70), (-8, -70), (-8, -23), (-27, -23), (-27, 14), (-56, 14)],  # behind the bunker's face, to the west edge
    [(33, -69), (67, -69), (67, -33), (33, -33)],                       # over the wool area and the lane's roofed half
    [(-58, 10), (-8, 18), (-5, 46), (-44, 46)],                         # the south peak's run down to the centre line
]
H_BOX = ((12, 30), (-85, -71))
def in_h(col):
    return H_BOX[0][0] <= col[0] <= H_BOX[0][1] and H_BOX[1][0] <= col[1] <= H_BOX[1][1]
standing = {c for c in struct_top if struct_base[c] <= 45 or in_h(c)}   # a structure that reaches the ground
reach = set()
for poly in BAND_REACH: reach |= polygon_cells(poly)
outline = set(footprint) | set(ground_top) | standing | reach
outline = {c for c in outline if in_half(*c)}
for _ in range(3):                                                       # close the gaps between the pieces
    outline |= {(x + dx, z + dz) for (x, z) in outline for dx, dz in band_field.N4 if in_half(x + dx, z + dz)}
for _ in range(3):
    outline = {c for c in outline if all((c[0] + dx, c[1] + dz) in outline for dx, dz in band_field.N4)
               or c in ground_top or c in standing or c in footprint}
outline |= {c for c in reach if in_half(*c)}
inner = (set(ground_top) | standing) & outline
mountain = outline - inner - SKY_OPEN
MIN_PATCH = 60                     # a scrap of band smaller than this is left to the ground around it, not stood up
pieces, left = [], set(mountain)
while left:
    seed = left.pop(); piece = [seed]; todo = [seed]
    while todo:
        x, z = todo.pop()
        for dx, dz in band_field.N4:
            n = (x + dx, z + dz)
            if n in left: left.remove(n); piece.append(n); todo.append(n)
    pieces.append(piece)
scraps = [p for p in pieces if len(p) < MIN_PATCH]
for piece in scraps: mountain -= set(piece)

def meets_at(col):
    x, z = col
    if col in standing:
        if in_h(col): return struct_base[col]
        bunker = any((x, y, z) in BUNKER for y in range(struct_base[col], struct_top[col] + 1))
        return struct_top[col] - (3 if bunker else 2)
    return ground_top[col]

inner_height = {c: meets_at(c) for c in inner
                if any((c[0] + dx, c[1] + dz) in mountain for dx, dz in band_field.N4)}
edge = {(x + dx, z + dz) for (x, z) in mountain for dx, dz in band_field.N4
        if (x + dx, z + dz) not in outline}
floor_under = {c: under[c] + 1 + COVER_MIN for c in mountain if under[c] >= 0}
heights, across = band_field.surface(mountain, inner_height, edge, style_pins, floor_under)
# a facade standing on the ground has ground under it up to its base
standing_base = {c: struct_base[c] for c in standing
                 if not in_h(c) and not any((c[0], y, c[1]) in BUNKER for y in range(struct_base[c], struct_top[c] + 1))}
erratic_cols = 0
for (x, z), (top, erratic) in heights.items():
    block = BLUE if erratic else YELLOW
    erratic_cols += erratic
    for k in range(5 if erratic else 3):
        cell = (x, top - k, z)
        if cell not in SPACE and (cell not in out or is_terrain(out[cell])): put(cell, block)
steps = collections.Counter()
for (x, z), (top, _) in heights.items():
    for n in ((x + 1, z), (x, z + 1)):
        if n in heights: steps[abs(top - heights[n][0])] += 1
report.append(f"mountain band: {len(mountain)} columns in one surface, {erratic_cols} in the erratic style and "
              f"{len(mountain) - erratic_cols} in the flat; it meets {len(inner_height)} columns on its inner side; "
              f"{len(scraps)} scraps under {MIN_PATCH} columns left to the ground ({sum(map(len, scraps))} columns)")
report.append(f"    heights y {min(v[0] for v in heights.values())}..{max(v[0] for v in heights.values())}; "
              f"largest step between neighbouring columns {max(steps)}, {sum(n for k, n in steps.items() if k > 4)} over 4")

# ---------------------------------------------------------------- 10. solid ground
GROUND = {(35, 8), (35, 4), (35, 3), (35, 5), (35, 13), (41, 0), (57, 0)}   # gold and diamond mark surface points
HALF = ((-60, 68), (-110, 48))

def columns_of(cells):
    by = collections.defaultdict(list)
    for (x, y, z) in cells:
        by[(x, z)].append(y)
    return by

ground_tops, structure_floors, space_top = {}, {}, {}
for (x, y, z), b in out.items():
    if not (HALF[0][0] <= x <= HALF[0][1] and HALF[1][0] <= z <= HALF[1][1]) or y > 120 \
            or (8 <= x <= 52 and y >= 85 and -22 <= z <= 47):
        continue
    if b in GROUND and (x, y, z) not in BUNKER:
        if y > ground_tops.get((x, z), -1): ground_tops[(x, z)] = y
    elif 20 <= y <= 40 and (x, y, z) not in SPACE:
        if y < structure_floors.get((x, z), 99): structure_floors[(x, z)] = y
space_low = {}
for (x, y, z) in SPACE:
    if y < space_low.get((x, z), 999): space_low[(x, z)] = y

tops = {}
for col, y in ground_tops.items(): tops[col] = y
for col, y in structure_floors.items():
    if col not in tops: tops[col] = y
for col, y in standing_base.items():
    if y > tops.get(col, -1): tops[col] = y
holes = 0
for _ in range(3):                      # a column with none, ringed by ones with ground, is a hole in a sheet
    added = {}
    for x in range(HALF[0][0], HALF[0][1] + 1):
        for z in range(HALF[1][0], HALF[1][1] + 1):
            if (x, z) in tops or (x, z) in SKY_OPEN: continue
            near = [tops[(x + dx, z + dz)] for dx in (-1, 0, 1) for dz in (-1, 0, 1)
                    if (dx or dz) and (x + dx, z + dz) in tops]
            if len(near) >= 6:
                added[(x, z)] = min(near)
    for (x, z), y in added.items():
        tops[(x, z)] = y
        if (x, y, z) not in out: put((x, y, z), KEY["walk"])
    holes += len(added)
open_cols = SKY_OPEN
HOUSE = ((-27, -5), (-22, 5))
TERRACE_Y = 56

def open_patches():
    """Columns with no ground under them, grouped: those enclosed by ground, and those that run into an intended
    opening (the canyon, a crack, the pit). Anything still joined to the half's border is outside the map."""
    candidates = {(x, z) for x in range(HALF[0][0], HALF[0][1] + 1) for z in range(HALF[1][0], HALF[1][1] + 1)
                  if (x, z) not in tops and (x, z) not in open_cols}
    def flood(seeds):
        got = set(seeds); todo = list(seeds)
        while todo:
            x, z = todo.pop()
            for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                if n in candidates and n not in got: got.add(n); todo.append(n)
        return got
    outside = flood([c for c in candidates if c[0] in HALF[0] or c[1] in HALF[1]])
    beside = flood([c for c in candidates - outside
                    if any(n in open_cols for n in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)))])
    def groups(cells):
        out_groups, left = [], set(cells)
        while left:
            seed = left.pop(); comp = [seed]; todo = [seed]
            while todo:
                x, z = todo.pop()
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    if n in left: left.remove(n); comp.append(n); todo.append(n)
            out_groups.append(comp)
        return out_groups
    return groups(candidates - outside - beside), groups(beside)

enclosed, beside = open_patches()
closed_patches = []
for comp in enclosed:
    cells = set(comp)
    if any(HOUSE[0][0] <= x <= HOUSE[0][1] and HOUSE[1][0] <= z <= HOUSE[1][1] for x, z in comp):
        level, why = TERRACE_Y, "the bunker's body, up to the terrace"
    else:
        ring = [ground_tops[n] for x, z in comp for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))
                if n not in cells and n in ground_tops]
        level, why = (min(ring) if ring else 30), "the lowest ground around it"
    for (x, z) in comp:
        tops[(x, z)] = level
        if (x, level, z) not in out: put((x, level, z), KEY["walk"])
    xs = [c[0] for c in comp]; zs = [c[1] for c in comp]
    closed_patches.append(f"    closed {len(comp):4d} columns  x {min(xs)}..{max(xs)}  z {min(zs)}..{max(zs)}  to y {level}, {why}")
report.append(f"surface: {len(enclosed)} enclosed patches with no ground under them, closed:")
report.extend(closed_patches)
for comp in beside:
    xs = [c[0] for c in comp]; zs = [c[1] for c in comp]
    report.append(f"    left open {len(comp):4d} columns  x {min(xs)}..{max(xs)}  z {min(zs)}..{max(zs)}  "
                  f"(runs into the canyon, a crack or the pit)")

FILLED = set()
edge_dist = {}
frontier = [c for c in tops if any((c[0] + dx, c[1] + dz) not in tops and (c[0] + dx, c[1] + dz) not in SKY_OPEN
                                   for dx, dz in band_field.N4)]
for c in frontier: edge_dist[c] = 1
while frontier:
    nxt = []
    for (x, z) in frontier:
        for dx, dz in band_field.N4:
            n = (x + dx, z + dz)
            if n in tops and n not in edge_dist:
                edge_dist[n] = edge_dist[(x, z)] + 1; nxt.append(n)
    frontier = nxt
lowest = {}
for (x, y, z) in list(SPACE) + [c for c, b in out.items() if b != FILL]:
    if in_half(x, z) and y < lowest.get((x, z), 999): lowest[(x, z)] = y
for (x, z), top in tops.items():
    bottom = 0
    if TAPER > 0:
        bottom = max(0, int(top - 5 - TAPER * edge_dist.get((x, z), 99)))
        bottom = min(bottom, lowest.get((x, z), 0))
    for y in range(bottom, top):
        cell = (x, y, z)
        if cell in out or cell in SPACE: continue
        out[cell] = FILL; FILLED.add(cell)
report.append(f"ground: {len(tops)} columns filled solid to y 0, {len(FILLED)} blocks; {holes} holes in sheets closed")
after_enclosed, _ = open_patches()
report.append(f"surface after the fill: {len(after_enclosed)} enclosed patches with no ground under them")

# ---------------------------------------------------------------- 11. closure: where the sky reaches underground
UNDERGROUND = set()
for name, (x0, x1), (z0, z1), y1 in (("room", U_ROOM[0], U_ROOM[1], R_ROOM - 1), ("lane", U_LANE[0], U_LANE[1], R_LANE - 1)):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(0, y1 + 1):
                if (x, y, z) not in out: UNDERGROUND.add((x, y, z))
for name, tx, tz, roof in TUNNELS:
    for y in range(roof - 6, roof):
        if (tx, y, tz) in SPACE and (tx, y, tz) not in out: UNDERGROUND.add((tx, y, tz))
for x in range(SPAWN[0] + 1, SPAWN[1]):
    for z in range(SPAWN[2] + 1, SPAWN[3]):
        for y in range(SPAWN[4] + 1, SPAWN[4] + 10): UNDERGROUND.add((x, y, z))

ENTRIES = [
    ("main entrance: the lane runs out into the canyon and the ramp", (47, 67, 0, 60, -35, -32)),
    ("the lane's open east side, toward the void", (65, 68, 0, 60, -52, -33)),
    ("crack K1 into the west arm", (30, 48, 0, 40, -41, -32)),
    ("the spawn door", (-11, -6, 30, 46, -50, -39)),
    ("the core stairs' mouth in the south peak's foot", (-25, -18, 30, 46, 3, 9)),
    ("the core stairs' door onto the terrace", (-29, -20, 55, 61, -18, -12)),
]
X0, X1, Y0, Y1, Z0, Z1 = -62, 70, 0, 100, -112, 50
NX, NY, NZ = X1 - X0 + 1, Y1 - Y0 + 1, Z1 - Z0 + 1
solid = bytearray(NX * NY * NZ)
for (x, y, z) in out:
    if X0 <= x <= X1 and Y0 <= y <= Y1 and Z0 <= z <= Z1:
        if 8 <= x <= 52 and y >= 85 and -22 <= z <= 47: continue
        solid[((x - X0) * NY + (y - Y0)) * NZ + (z - Z0)] = 1
seen = bytearray(NX * NY * NZ)
stack = []
for xi in range(NX):
    for zi in range(NZ):
        i = (xi * NY + (NY - 1)) * NZ + zi
        if not solid[i]: seen[i] = 1; stack.append(i)
for xi in range(NX):
    for yi in range(NY):
        for zi in (0, NZ - 1):
            i = (xi * NY + yi) * NZ + zi
            if not solid[i] and not seen[i]: seen[i] = 1; stack.append(i)
for zi in range(NZ):
    for yi in range(NY):
        for xi in (0, NX - 1):
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
leaks = 0
for comp in sorted(groups, key=len, reverse=True):
    bb = [(min(c[k] for c in comp), max(c[k] for c in comp)) for k in range(3)]
    named = [n for n, (a0, a1, b0, b1, c0, c1) in ENTRIES
             if bb[0][0] <= a1 and bb[0][1] >= a0 and bb[1][0] <= b1 and bb[1][1] >= b0 and bb[2][0] <= c1 and bb[2][1] >= c0]
    if not named: leaks += 1
    report.append(f"    opening {'ENTRY' if named else 'LEAK '} {len(comp):5d} cells  x {bb[0][0]}..{bb[0][1]}  "
                  f"y {bb[1][0]}..{bb[1][1]}  z {bb[2][0]}..{bb[2][1]}  {named[0] if named else ''}")
report.insert(len(report) - len(groups), f"closure: {len(groups)} openings from the sky into the underground, {leaks} not an entry")

# ---------------------------------------------------------------- 12. every tunnel below the ground over it
above = {}
for (x, z), top in tops.items(): above[(x, z)] = top
exposed, raised = [], 0
for name, x, z, roof in TUNNELS:
    if (x, z) in SKY_OPEN: continue                    # a roof under a crack is the crack's way in
    top = above.get((x, z))
    near = [above[(x + dx, z + dz)] for dx in (-1, 0, 1) for dz in (-1, 0, 1) if (dx or dz) and (x + dx, z + dz) in above]
    local = max(near) if near else None
    if (top is None or top < roof) and local is not None and roof - 1 <= local <= roof + 2:
        top = roof                                     # the floor beside it is at the roof: the roof replaced the floor
    if top is not None and roof >= top and roof + 1 - top <= 2:
        for y in range(top + 1, roof + 2):            # a tunnel grazing the surface: the floor is raised over it
            if (x, y, z) not in out: put((x, y, z), KEY["walk"])
        above[(x, z)] = roof + 1; raised += 1
        continue
    if top is None or roof >= top:
        exposed.append((name, x, z, roof, top))
report.append(f"below ground: {len(TUNNELS)} tunnel columns, {len(exposed)} with a roof at or above the ground over them; "
              f"{raised} where the floor was raised one or two blocks over a roof")
least = {}
for name, x, z, roof in TUNNELS:
    top = above.get((x, z))
    if top is None: continue
    cover = top - roof
    if name not in least or cover < least[name][0]: least[name] = (cover, x, z, roof, top)
for name, (cover, x, z, roof, top) in least.items():
    report.append(f"    {name}: least ground over the roof {cover} at ({x}, {z}), roof y {roof}, surface y {top}")
for name, x, z, roof, top in exposed[:15]:
    report.append(f"    exposed {name} at ({x}, {z}): roof y {roof}, ground {top}")

if XRAY:
    xray = {c: b for c, b in out.items() if c not in FILLED}

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
        if XRAY and (x, y, z) not in FILLED: xray[(2 * cx - x, y, 2 * cz - z)] = turned_block(b)
    report.append(f"turned {len(half)} blocks 180 degrees about block {CENTRE}")

tiles = [{"id": "DLDetector", "x": x, "y": y, "z": z} for (x, y, z), b in out.items() if b[0] in (151, 178)]
chunks, regions = write_world(out, OUT, tile_entities=tiles)
report.append(f"wrote {len(out)} blocks in {chunks} chunks, {regions} regions -> {OUT}")
if XRAY:
    write_world(xray, XRAY, tile_entities=tiles)
    report.append(f"x-ray copy without the ground fill -> {XRAY}")
print("\n".join(report))
