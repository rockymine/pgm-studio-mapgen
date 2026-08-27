#!/usr/bin/env python3
"""Write the two authored documents for `opus5-liminal-dtm-ii`.

    python3 specs/opus5-liminal-dtm-ii/build-spec.py

Liminal DTM II is a three-level board — an undercroft, the desert surface and a ring of islands in
the air over the river — so its geometry is arithmetic on a handful of named courses. Those courses
are stated once below and every shape is written from them: a slab's floor, the wall that carries
it and the stair that reaches it are three statements of one number.

Output: `opus5-liminal-dtm-ii.plan.json` and `opus5-liminal-dtm-ii.finish.json` beside this file.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-liminal-dtm-ii"
CELL = 4

# ── the courses ───────────────────────────────────────────────────────────────────────────────
# A layer holds one span per column, so every storey is `floor` + a thickness inside its own layer.
# Read down the page: the world reads the same way.
HOLD_FLOOR   = 1                    # the Stronghold slab: blocks 1..3, stood on at y4
HOLD_H       = 3
HOLD_TOP     = HOLD_FLOOR + HOLD_H              # 4
UNDER_FLOOR  = 6                    # the undercroft slab: blocks 6..11, stood on at y12
UNDER_H      = 6
UNDER_TOP    = UNDER_FLOOR + UNDER_H            # 12 — the undercroft floor a player stands on
GROUND_FLOOR = 18                   # the desert landmass: blocks 18..35, stood on at y36
GROUND_H     = 18
SURFACE      = GROUND_FLOOR + GROUND_H          # 36
UNDER_WALL_H = GROUND_FLOOR - UNDER_FLOOR       # 12 — an undercroft wall meets the landmass at y18
RIVER_H      = 10                   # the river region: blocks 18..27, stood on at y28
RIVER        = GROUND_FLOOR + RIVER_H           # 28
LID_FLOOR    = 16                   # the backrooms ceiling: blocks 16..17, four courses of headroom
LID_H        = 2
SKY_FLOOR    = 50                   # a skyblock: obsidian at 50, dirt 51..52, grass 53
SKY_H        = 4
SKY_TOP      = SKY_FLOOR + SKY_H                # 54

# ── the frame, in blocks ──────────────────────────────────────────────────────────────────────
X_EDGE, Z_EDGE   = 124, 80          # the board: 248 x 160
X_TOWN, Z_TOWN   = 72, 48           # the village: 144 x 96
X_BANK           = 88               # the river's outer edge on the long sides


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def stack(*pairs, ending="repeat"):
    return {"bands": [{"material": m, "thickness": t} for m, t in pairs], "ending": ending}


def layered(band_stack, axis="depth"):
    return {"kind": "layered", "axis": axis, "stack": band_stack}


def noise(seed, scale, octaves, stops):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="void", bedrock=1):
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "rim": {"material": rim or solid(24, 2), "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True,
        "fill": fill,
    }


THEMES = {
    # the desert the whole board is made of: sand over sandstone, cut faces in sandstone
    "desert": theme(layered(stack((solid(12), 3), (solid(24), 2), ending="handOver")),
                    solid(24), solid(24), surface_depth=4),
    # the river region — the same desert, one course of it, so the drop reads as a drop
    "riverbed": theme(solid(12), solid(24), solid(24), surface_depth=3),
    # the Liminal Poolroom: the blocks of an indoor swimming pool
    "pool": theme(layered(stack((solid(159, 3), 1), (solid(159, 9), 1), ending="repeat")),
                  solid(159, 9), solid(168, 1), surface_depth=2),
    # the pools themselves: the same prismarine basin with water for its top courses, so the water is
    # the shape's own surface bucket rather than a channel swept over it — a pool has straight sides
    "pool-deep": theme(solid(9), solid(159, 9), solid(168, 1), surface_depth=4),
    "pool-sub":  theme(solid(9), solid(159, 9), solid(168, 1), surface_depth=2),
    # the Farm's furrow, the same trick one course deep
    "farm-water": theme(solid(9), solid(3), solid(24), surface_depth=1),
    # the Liminal Backroom Space: double smooth stone slab underfoot, smooth sandstone everywhere else
    "backroom": theme(solid(43, 8), solid(24, 2), solid(24, 2), surface_depth=1),
    # its ceiling, seen from underneath, which is the lid's fill
    "backroom-lid": theme(solid(24, 2), solid(24, 2), solid(24, 2), surface_depth=1),
    # the Pyramid's own mass: smooth sandstone banded with orange clay, the two courses the vanilla
    # structure wears, so the batter reads as built rather than as a sand dune
    "pyramid": theme(layered(stack((solid(24, 2), 1), (solid(159, 1), 1), (solid(24, 0), 2),
                                   ending="repeat")),
                     solid(24, 2), solid(24, 0), surface_depth=4),
    # the stair down: smooth sandstone the whole way, because a flight is one made thing
    "stair": theme(solid(24, 2), solid(24, 2), solid(24, 0), surface_depth=1),
    # the Stronghold: the vanilla mix of stone brick, cracked and mossy, at a period wide enough
    # to read as a course laid by hand rather than as a field
    "hold": theme(noise(12, 16, 2, [solid(98), solid(98, 2)]),
                  noise(12, 16, 2, [solid(98), solid(98, 1)]), solid(98), surface_depth=1),
    # the frame round the portal, which is decoration and says so
    "portal": theme(solid(121), solid(121), solid(121), surface_depth=1),
    # a skyblock: grass, two of dirt, obsidian
    "skyblock": theme(layered(stack((solid(2), 1), (solid(3), 2), ending="handOver")),
                      solid(3), solid(49), surface_depth=3, bedrock=0),
    # the Town Wall: stone brick grained with cobble, one ground rather than two
    "wall": theme(noise(3, 11, 2, [solid(98), solid(4)]), noise(3, 11, 2, [solid(98), solid(4)]),
                  solid(98), surface_depth=1),
    # the Snowy Taiga: snow lying in patches over the grass, at a period wide enough to read as
    # weather rather than as static, over the dirt and the stone the desert never shows
    "taiga": theme(layered(stack((noise(9, 20, 2, [solid(80), solid(2)]), 1), (solid(3), 2),
                                 ending="handOver")),
                   solid(1), solid(1), surface_depth=3),
    # the Farm's beds, laid in a two-block chequer so the plot reads as tilled rather than as dirt
    "farm": theme({"kind": "checker", "size": 2, "even": solid(3, 0), "odd": solid(3, 1)},
                  solid(3), solid(24), surface_depth=2),
    # a Small Hill: its top two courses are grass over dirt where everything round it is sand
    "hill": theme(layered(stack((solid(2), 1), (solid(3), 2), ending="handOver")),
                  solid(3), solid(24), surface_depth=3),
    # the two bridges: oak over the river, the one crossing a player is meant to take
    "bridge": theme(solid(5, 0), solid(17, 0), solid(5, 0), surface_depth=1),
}

# ── shape helpers ─────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def box(prefix, x0, z0, x1, z1, floor, height, theme_key=None, op="add", over=False, keep=False):
    shape = {"id": sid(prefix), "type": "rectangle", "operation": op,
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": height}
    if over:
        # An override add wins the column against the other shapes on its layer — and is still part of
        # the island's relief field, which then solves a surface straight through it. `height_mode`
        # is what makes a shape stand OUT of the field: `level` holds it at the absolute top its own
        # floor and height state, and `skirt: 0` is a sheer face, which is right for a built thing.
        shape["override"] = True
        shape["height_mode"] = "level"
        shape["skirt"] = 0
    if keep:
        shape["keepClear"] = True
    if theme_key:
        shape["theme"] = theme_key
    return shape


def island(ident, name, shapes, mirrors=True):
    return {"id": ident, "name": name, "mirrors": mirrors,
            "shapeIds": [s["id"] for s in shapes]}


def ring(prefix, x0, z0, x1, z1, thick, floor, height, theme_key, gaps=(), over=False, keep=False):
    """A wall round a room. A wall is not a shape on top of a floor — a layer keeps one span per
    column and the taller add wins it outright — so it is the same slab, carried higher, drawn as
    four bands outside the floor. `gaps` names ("e"|"w"|"n"|"s", from, to) left open for a doorway;
    an e/w gap is a z span and an n/s gap an x span."""
    def spans(side, lo, hi):
        out, at = [], lo
        for c0, c1 in sorted((g[1], g[2]) for g in gaps if g[0] == side):
            if c0 > at:
                out.append((at, min(c0, hi)))
            at = max(at, c1)
        if at < hi:
            out.append((at, hi))
        return out

    walls = []
    for lo, hi in spans("n", x0 - thick, x1 + thick):
        walls.append(box(prefix, lo, z0 - thick, hi, z0, floor, height, theme_key, over=over, keep=keep))
    for lo, hi in spans("s", x0 - thick, x1 + thick):
        walls.append(box(prefix, lo, z1, hi, z1 + thick, floor, height, theme_key, over=over, keep=keep))
    for lo, hi in spans("w", z0, z1):
        walls.append(box(prefix, x0 - thick, lo, x0, hi, floor, height, theme_key, over=over, keep=keep))
    for lo, hi in spans("e", z0, z1):
        walls.append(box(prefix, x1, lo, x1 + thick, hi, floor, height, theme_key, over=over, keep=keep))
    return walls


def ramp(prefix, x0, z0, x1, z1, floor, low, high, theme_key, along, keep=False):
    """A flight, as ONE shape. A polygon carries a thickness per vertex and the rasterizer samples its
    surface at each cell's centre and floors it into the column, so a tilted quad IS a stair — the
    courses are what a sloped surface rasterizes to, one course a cell at the steepest and a course
    every two or three at gentler runs. `along` is which end is the high one: `+x`, `-x`, `+z`, `-z`."""
    lo, hi = low - floor, high - floor
    corners = {"+x": [lo, hi, hi, lo], "-x": [hi, lo, lo, hi],
               "+z": [lo, lo, hi, hi], "-z": [hi, hi, lo, lo]}[along]
    shape = {"id": sid(prefix), "type": "polygon", "operation": "add", "override": True,
             "height_mode": "level", "skirt": 0,
             "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]],
             "anchor_heights": corners, "floor": floor, "base_height": hi}
    if keep:
        shape["keepClear"] = True
    if theme_key:
        shape["theme"] = theme_key
    return [shape]


def outside(rect, hole):
    """What is left of a rectangle once a hole is taken out of it, as rectangles."""
    x0, z0, x1, z1 = rect
    hx0, hz0, hx1, hz1 = hole
    if hx0 >= x1 or hx1 <= x0 or hz0 >= z1 or hz1 <= z0:
        return [rect]
    out = []
    if z0 < hz0:
        out.append((x0, z0, x1, min(hz0, z1)))
    if z1 > hz1:
        out.append((x0, max(hz1, z0), x1, z1))
    mid0, mid1 = max(z0, hz0), min(z1, hz1)
    if mid0 < mid1:
        if x0 < hx0:
            out.append((x0, mid0, min(hx0, x1), mid1))
        if x1 > hx1:
            out.append((max(hx1, x0), mid0, x1, mid1))
    return out


def clipped(shapes, holes):
    """The same shapes with the holes taken out of them, one rectangle a surviving piece. Two
    override adds over one column is not a refusal — the taller wins the geometry — but a theme is
    scoped separately and the SMALLER shape wins that, so a hill's ring crossing the Town Wall leaves
    a wall built to its own height and painted grass over dirt. What a shape may not land on, it is
    cut out of."""
    out = []
    for shape in shapes:
        parts = [(shape["min_x"], shape["min_z"], shape["max_x"], shape["max_z"])]
        for hole in holes:
            parts = [piece for part in parts for piece in outside(part, hole)]
        for x0, z0, x1, z1 in parts:
            out.append({**shape, "id": sid(shape["id"].rstrip("0123456789")),
                        "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1})
    return out


# ══ the undercroft ════════════════════════════════════════════════════════════════════════════
# The storey is a MASS with rooms cut out of it, not rooms standing in the void. A layer keeps one
# span per column, so a room's walls are simply the rock either side of it — which means the rock has
# to be STATED, over every column no room occupies, or the board's lower half is air and the desert
# above it floats on nothing. Everything down here therefore sits on the same two courses: the mass
# runs y1..17 and meets the landmass's own underside at y18, and a room is a shorter span in the same
# column with air over it.
MASS_FLOOR = 1
MASS_H     = GROUND_FLOOR - MASS_FLOOR           # 17 — the mass meets the landmass at y18
FLOOR_H    = UNDER_TOP - MASS_FLOOR              # 11 — a room's floor: blocks 1..11, stood on at y12

POOL   = (56, -12, 96, 36)          # the Liminal Poolroom, under the river band nearest that spawn
CORR   = (96, 28, 108, 36)          # the corridor out of its east wall, to the stairwell
WELL   = (100, 36, 108, 60)         # the stairwell, cut into the Pyramid's own ground
BACK   = (24, 4, 56, 12)            # the way west out of the Poolroom into the Backroom Space
PORTAL = (-16, -16, 16, 16)         # the End Portal Room, under the Village Well
HOLD_STAIR = (16, 24, 4, 12)        # eight treads from the Backrooms down into it


def mirror(rect):
    """A footprint's rot_180 image. The mass is authored once and fanned, so its holes have to be
    the union of what is authored and what the fan draws — or the image of the rock fills the
    authored rooms."""
    x0, z0, x1, z1 = rect
    return (-x1, -z1, -x0, -z0)


def carve(rect, blocks):
    """A corridor minus the boxes it must not run into, split along its own long axis. What is left
    is the maze the mass will have holes for; what is taken out is where a room's liner stands."""
    x0, z0, x1, z1 = rect
    along_x = (x1 - x0) >= (z1 - z0)
    lo, hi = (x0, x1) if along_x else (z0, z1)
    cuts = sorted((b[0], b[2]) if along_x else (b[1], b[3])
                  for b in blocks
                  if b[0] < x1 and b[2] > x0 and b[1] < z1 and b[3] > z0)
    spans, at = [], lo
    for c0, c1 in cuts:
        if c0 > at:
            spans.append((at, min(c0, hi)))
        at = max(at, c1)
    if at < hi:
        spans.append((at, hi))
    return [((a, z0, b, z1) if along_x else (x0, a, x1, b)) for a, b in spans if b > a]


def solid_around(x0, z0, x1, z1, holes, prefix, floor, height, theme_key):
    """The rock a storey is cut out of: the box minus the holes, as z-bands split in x. Stated rather
    than carved, because a subtract reaches only the layer it is on and a shorter add inside a taller
    one is not in the world at all."""
    edges = sorted({z0, z1} | {z for h in holes for z in (h[1], h[3]) if z0 < z < z1})
    out = []
    for za, zb in zip(edges, edges[1:]):
        blocked = sorted((h[0], h[2]) for h in holes if h[1] < zb and h[3] > za)
        at = x0
        for bx0, bx1 in blocked:
            if bx0 > at:
                out.append(box(prefix, at, za, min(bx0, x1), zb, floor, height, theme_key))
            at = max(at, bx1)
        if at < x1:
            out.append(box(prefix, at, za, x1, zb, floor, height, theme_key))
    return out


# ── the Backroom Space ─────────────────────────────────────────────────────────────────────────
# A lattice of four-wide corridors on a sixteen-block pitch, with one link in three taken out. What
# that leaves is what the brief asks for and what a plain grid is not: long runs, short ones, loops
# back into a corridor already walked, and dead ends. The rule is stated rather than rolled, and it
# is symmetric under rot_180 by construction — `(k + m) % 3` is unchanged by negating both — so the
# maze is its own mirror image and the two teams walk the same one.
MAZE_PITCH, MAZE_WIDE = 20, 4
KS = range(-6, 7)                                # the grid lines, indexed off the origin
MAZE_LINE = [-2 + MAZE_PITCH * k for k in KS]    # a corridor spans [line, line + 4)

maze = []
for k, x in zip(KS, MAZE_LINE):                  # every north-south run, whole
    if -X_EDGE <= x and x + MAZE_WIDE <= X_EDGE:
        maze.append((x, -Z_EDGE, x + MAZE_WIDE, Z_EDGE))
for m, z in zip(KS, MAZE_LINE):                  # the east-west links, one in three missing
    if not (-Z_EDGE <= z and z + MAZE_WIDE <= Z_EDGE):
        continue
    for k, x in zip(KS, MAZE_LINE):
        nxt = x + MAZE_PITCH
        if nxt + MAZE_WIDE > X_EDGE or (2 * k + 1 + 2 * m) % 3 == 0:
            continue
        maze.append((x + MAZE_WIDE, z, nxt, z + MAZE_WIDE))

# The two rooms the maze may not open into anywhere it likes: their walls are their own material and
# their doors are authored. Everything else the maze meets, it joins.
LINED = [POOL, PORTAL]
LINER = [(r[0] - 2, r[1] - 2, r[2] + 2, r[3] + 2) for r in LINED]
STAIR_BOX = (HOLD_STAIR[0], HOLD_STAIR[2], HOLD_STAIR[1], HOLD_STAIR[3])
KEEP_OUT = [r for rect in LINER + [CORR, WELL, STAIR_BOX] for r in (rect, mirror(rect))]
maze = [seg for rect in maze for seg in carve(rect, KEEP_OUT)]

# and the way out of the Poolroom, split round the runs it crosses for the same reason
BACK_LEGS = carve(BACK, [seg for seg in maze if seg[3] - seg[1] > seg[2] - seg[0]])

# ── what the mass has holes for ────────────────────────────────────────────────────────────────
SIDED = [POOL, CORR, WELL] + BACK_LEGS           # what one team has and the other's image mirrors
HOLES = [r for rect in SIDED + LINER for r in (rect, mirror(rect))] \
    + maze + [PORTAL, STAIR_BOX, mirror(STAIR_BOX)]

# ── the two islands, and why the rock is not one of the mirrored ones ──────────────────────────
# The mass covers the whole board, so its own rot_180 image would cover it a second time and every
# column would carry the same span twice (`SK9`). It is drawn once instead — an island that does not
# mirror stamps its shapes once — and its holes are stated for both halves. The maze is the same
# case: the rule that draws it is symmetric about the origin, so the lattice IS its own image.
FRAME = (-4, -4, 4, 4)
whole = solid_around(-X_EDGE, -Z_EDGE, X_EDGE, Z_EDGE, HOLES, "ms",
                     MASS_FLOOR, MASS_H, "backroom")
whole += [box("mf", *rect, MASS_FLOOR, FLOOR_H, "backroom") for rect in maze]
whole += ring("hw", *PORTAL, 2, MASS_FLOOR, MASS_H, "hold",
              gaps=[("e", 4, 12), ("w", -12, -4)])

# ══ the Stronghold ════════════════════════════════════════════════════════════════════════════
# It gets its height by standing lower rather than reaching higher: a floor at y4 under the same
# ceiling every other room has leaves fourteen courses of air where the Poolroom's leaves six.
whole += solid_around(*PORTAL, [FRAME], "hf", HOLD_FLOOR, HOLD_H, "hold")
whole.append(box("hf", -3, -3, 3, 3, HOLD_FLOOR, HOLD_H, "hold"))
whole += ring("hp", -3, -3, 3, 3, 1, HOLD_FLOOR, HOLD_TOP, "portal")

sided = [box("rf", *rect, MASS_FLOOR, FLOOR_H, "pool" if rect in (POOL, CORR) else "backroom")
         for rect in SIDED]
sided += ring("pw", *POOL, 2, MASS_FLOOR, MASS_H, "pool",
              gaps=[("e", 28, 36), ("w", 4, 12)])

# ══ the water in them ═════════════════════════════════════════════════════════════════════════
# A pool is a room with water in it, not a river that happens to be indoors. A `water` prop sweeps a
# disc along a polyline and carves its own bed, which is right for a river and wrong here: the edge
# comes out lobed and the depth follows the sweep. Stated as a rectangle whose theme puts water in its
# surface bucket, the pool is exactly the rectangle drawn — straight sides, one depth, flush with the
# deck at y11 — and the prismarine under it is the same fill the room already has.
MAIN_POOL = (60, -8, 92, 32)        # 32 x 40 of the room's 40 x 48 — the brief's ~70%, four deep
SUB_BATHS = [(92, -4, 96, 4), (92, 12, 96, 20)]     # two along the east deck, two deep
sided.append(box("pl", *MAIN_POOL, MASS_FLOOR, FLOOR_H, "pool-deep", over=True))
sided += [box("pl", *rect, MASS_FLOOR, FLOOR_H, "pool-sub", over=True) for rect in SUB_BATHS]
for j in range(UNDER_TOP - HOLD_TOP):
    edge = HOLD_STAIR[1] - 1 - j
    sided.append(box("hs", edge, HOLD_STAIR[2], edge + 1, HOLD_STAIR[3],
                     HOLD_FLOOR, UNDER_TOP - 1 - j, "hold"))

under = whole + sided

# The lid the Backroom Space keeps its four courses under: the mass alone would leave six, which is
# the Poolroom's height and not the maze's. It covers the corridors and nothing beside them, so it
# is never driven into the rock either side of one (`SK10`).
lid_whole = [box("bl", *rect, LID_FLOOR, LID_H, "backroom-lid") for rect in maze]
lid_sided = [box("bl", *rect, LID_FLOOR, LID_H, "backroom-lid") for rect in BACK_LEGS]
lid = lid_whole + lid_sided

# ══ the stairwell ═════════════════════════════════════════════════════════════════════════════
# The stair is cut into the LANDMASS, not into a hole in it. A hole in the ground layer — drawn as
# a subtract or left as a gap the compiler declares a void — is refused the moment anything on a
# lower layer stands under it (`SK13`), so the well is stated the other way round: an override add
# overwrites whatever column it lands on, floor and all, so a tread at `floor 12` replaces the
# desert's `floor 18` outright and the shaft is the air left over it.
#
# It descends onto the undercroft's own floor rather than through it: the shaft is one of the mass's
# holes, so the rock stops at the shaft wall and the flight rests on the room floor beneath it at
# y12. Every tread is its own rectangle, so a course is a course rather than a rasterized guess — a
# ramp at one course a cell builds as treads of two, and a two-block rise costs a placed block.
WX0, WZ0, WX1, WZ1 = WELL
add_shapes = ramp("st", WX0, WZ0, WX1, WZ1, UNDER_TOP, UNDER_TOP + 1, SURFACE, "stair", "+z")

# ══ the bridges ═══════════════════════════════════════════════════════════════════════════════
# A deck over the river rather than a causeway through it: on the ground layer a taller add replaces
# the column it lands on floor and all, so a crossing drawn there would dam the water. It is a slab
# of its own, spanning exactly the river's columns so its ends butt the two banks at their own top
# course and the join is a step of none. rot_180 fans the two into four.
BRIDGE_FLOOR = SURFACE - 2                       # blocks 34..35, walked at y36 like the banks
BRIDGE_Z = (28, 36)
bridges = [
    box("bg", X_TOWN, BRIDGE_Z[0], X_BANK, BRIDGE_Z[1], BRIDGE_FLOOR, 2, "bridge"),
    box("bg", -X_BANK, BRIDGE_Z[0], -X_TOWN, BRIDGE_Z[1], BRIDGE_FLOOR, 2, "bridge"),
]

# ══ the slipways ══════════════════════════════════════════════════════════════════════════════
# The river sits eight courses under everything around it, so without these it is a pit: a player
# who drops in cannot climb out without placing a block. Each is a notch cut into the bank beside a
# bridge — the same override add the stairwell is, one tread a block, so the descent walks both ways
# — and there is one on each side of each crossing. rot_180 fans four into eight.
SLIP_Z = (BRIDGE_Z[0] - 8, BRIDGE_Z[0])          # the eight blocks north of a bridge
SLIP_FALL = SURFACE - RIVER                      # 8 courses

def slipway(x_bank, into):
    """Steps cut into a bank, falling toward the water. `into` is the direction the river lies in
    from that bank, so the tread against the water is the low one and the flight walks both ways."""
    start = x_bank - into * SLIP_FALL
    x0, x1 = (start, x_bank) if into > 0 else (x_bank, start)
    return ramp("sw", x0, SLIP_Z[0], x1, SLIP_Z[1], GROUND_FLOOR,
                RIVER, SURFACE, "stair", "-x" if into > 0 else "+x")


# The outer banks only: the village's own is where the Town Wall stands, and a flight cut into that
# is a pit against a wall rather than a way out of the water.
for bank, into in ((X_BANK, -1), (-X_BANK, 1)):
    add_shapes += slipway(bank, into)

# ══ the Town Wall ═════════════════════════════════════════════════════════════════════════════
# Nine courses over the village and four thick, open only where a bridge lands. A wall is not a
# shape on top of the ground: it is the ground's own column carried higher, so it is an override add
# at the same floor with a greater thickness. Authored for z >= 0 and fanned, which is what puts a
# gate on each of the four crossings.
WALL_TOP = SURFACE + 8                           # blocks 18..44, walked at y45
WALL_T = 4
GATE = BRIDGE_Z                                  # (28, 36) — where a bridge meets the wall


def wall(x0, z0, x1, z1):
    return box("wl", x0, z0, x1, z1, GROUND_FLOOR, WALL_TOP - GROUND_FLOOR + 1, "wall",
               over=True, keep=True)


add_shapes += [
    wall(-X_TOWN, Z_TOWN - WALL_T, X_TOWN, Z_TOWN),                       # the whole north face
    wall(X_TOWN - WALL_T, 0, X_TOWN, GATE[0]),                            # east, up to its gate
    wall(X_TOWN - WALL_T, GATE[1], X_TOWN, Z_TOWN - WALL_T),              # east, past it
    wall(-X_TOWN, 0, -X_TOWN + WALL_T, GATE[0]),                          # west, up to its gate
    wall(-X_TOWN, GATE[1], -X_TOWN + WALL_T, Z_TOWN - WALL_T),            # west, past it
]

# Up onto the wall-walk: nine treads against the inner face beside each gate, one course a block, so
# the climb walks both ways and costs nothing.
# A flight is ONE shape, not one rectangle a course. A polygon carries a height per vertex and the
# rasterizer interpolates between them, so a tilted quad IS a stair — the courses are what a sloped
# surface rasterizes to. What decides whether it walks is the gradient: at one course a cell the
# rasterization lands nine two-block steps in twenty-four, and a two-block rise costs a placed block
# to climb. At two cells a course, none. So the run is twice the rise and the flight is one quad.
STAIR_RUN = 2 * (WALL_TOP - SURFACE)             # 16 blocks of run for eight courses of rise


def wall_stair(x_face, into, z0):
    """`into` is the direction the village lies in from the wall's inner face."""
    far = x_face + into * STAIR_RUN
    x0, x1 = (x_face, far) if into > 0 else (far, x_face)
    return [{
        "id": sid("ws"), "type": "polygon", "operation": "add", "override": True,
        "keepClear": True, "height_mode": "level", "skirt": 0, "theme": "wall",
        "vertices": [[x0, z0], [x1, z0], [x1, z0 + 4], [x0, z0 + 4]],
        "floor": GROUND_FLOOR, "base_height": WALL_TOP - GROUND_FLOOR + 1,
        # a thickness a vertex, measured from the shape's own floor: the wall's top at its face and
        # the village's own surface at the far end, whichever way round the two ends fall in x
        "anchor_heights": ([WALL_TOP - GROUND_FLOOR + 1, SURFACE - GROUND_FLOOR,
                            SURFACE - GROUND_FLOOR, WALL_TOP - GROUND_FLOOR + 1] if into > 0 else
                           [SURFACE - GROUND_FLOOR, WALL_TOP - GROUND_FLOOR + 1,
                            WALL_TOP - GROUND_FLOOR + 1, SURFACE - GROUND_FLOOR]),
    }]


STAIR_KEEP = []
for face, into in ((X_TOWN - WALL_T, -1), (-X_TOWN + WALL_T, 1)):
    for z0 in (GATE[1] + 2, 10):
        flight = wall_stair(face, into, z0)
        add_shapes += flight
        # the run the flight fans over, both halves, so a mound drawn near it is cut round it
        low, high = (face - STAIR_RUN, face) if into < 0 else (face, face + STAIR_RUN)
        STAIR_KEEP += [(low, z0, high, z0 + 4), (-high, -z0 - 4, -low, -z0)]

# ══ the Village Well ══════════════════════════════════════════════════════════════════════════
# One on the whole map, on the origin, where the four roads meet. Two courses of smooth sandstone
# round a 2x2 mouth — the vanilla well's proportions without the water in it yet.
add_shapes += ring("wh", -1, -1, 1, 1, 2, GROUND_FLOOR, SURFACE - GROUND_FLOOR + 2, "stair", over=True)

# ══ the Farm ══════════════════════════════════════════════════════════════════════════════════
# The one Village component that is not a building: a plot sunk a course under the village with a
# kerb round it and a furrow of water down the middle, which is what a vanilla farm is once the
# crops are taken out — and crops are the one thing the prop vocabulary has no word for.
FARM = (47, 18, 59, 26)
add_shapes.append(box("fm", *FARM, GROUND_FLOOR, SURFACE - GROUND_FLOOR - 1, "farm",
                      over=True, keep=True))
add_shapes += ring("fm", *FARM, 1, GROUND_FLOOR, SURFACE - GROUND_FLOOR + 1, "stair",
                   over=True, keep=True)

add_shapes.append(box("fw", 53, 19, 54, 26, GROUND_FLOOR, SURFACE - GROUND_FLOOR - 1,
                      "farm-water", over=True, keep=True))


# ══ the Small Hills ═══════════════════════════════════════════════════════════════════════════
# Six, three courses over the village on a 10x6 top, each stepped twice so it meets the sand rather
# than standing on it. Three are authored and rot_180 makes the other three.
HILLS = [(-34, -39), (14, -30), (56, 6)]
# The four faces of the Town Wall as rectangles — what a mound drawn near one is cut out of. Stated
# for both halves, since a hill authored on one side has its rot_180 image on the other.
WALL_KEEP = [
    (-X_TOWN, Z_TOWN - WALL_T, X_TOWN, Z_TOWN),          # north
    (-X_TOWN, -Z_TOWN, X_TOWN, -Z_TOWN + WALL_T),        # south
    (X_TOWN - WALL_T, -Z_TOWN, X_TOWN, Z_TOWN),          # east
    (-X_TOWN, -Z_TOWN, -X_TOWN + WALL_T, Z_TOWN),        # west
]

for cx, cz in HILLS:
    mound = [box("hl", cx - 5, cz - 3, cx + 5, cz + 3,
                 GROUND_FLOOR, SURFACE + 3 - GROUND_FLOOR, "hill", over=True)]
    mound += ring("hl", cx - 5, cz - 3, cx + 5, cz + 3, 3,
                  GROUND_FLOOR, SURFACE + 2 - GROUND_FLOOR, "hill", over=True)
    mound += ring("hl", cx - 8, cz - 6, cx + 8, cz + 6, 3,
                  GROUND_FLOOR, SURFACE + 1 - GROUND_FLOOR, "hill", over=True)
    add_shapes += clipped(mound, WALL_KEEP + STAIR_KEEP)

# ══ the sky ═══════════════════════════════════════════════════════════════════════════════════
# Eight islands on the ellipse the river runs, evenly spaced; four authored, four fanned. Each is an
# L of two rectangles, five to eight blocks along both axes.
SKYBLOCKS = [(74, 22, 8), (31, 54, 6), (-31, 54, 7), (-74, 22, 5)]
sky = []
for cx, cz, n in SKYBLOCKS:
    arm = max(3, n // 2 + 1)
    sky.append(box("sk", cx - n // 2, cz - n // 2, cx - n // 2 + n, cz - n // 2 + arm,
                   SKY_FLOOR, SKY_H, "skyblock"))
    sky.append(box("sk", cx - n // 2, cz - n // 2 + arm, cx - n // 2 + arm, cz - n // 2 + n,
                   SKY_FLOOR, SKY_H, "skyblock"))

# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


PYR_TOP, PYR_STEPS, PYR_RUN = SURFACE + 4, 4, 2
IRON_AT = (-106, 40)                # the Snowy Taiga's iron blocks

SPAWN_ROOM = (104, 60, 124, 80)     # the Pyramid itself: a spawn-role piece sizes the stamped room,
                                    # and its rect is the protection, so it is a building and not a region
SPAWN_AT   = (112, 70)              # inside it, at the head of the stairwell
GOAL_TOWN  = (56, 32)               # the Village Monument, on the road in from the Pyramid
GOAL_POOL  = (80, 8)                # the Liminal Monument, over the Main Pool
GOAL_SKY   = (74, 22)               # the Skyblock Monument, on the island nearest the Pyramid

# One oak on the tip of each island's short leg — except the island the Skyblock Monument stands on: a
# goal holds a 21-block square against every placed prop (`OB19`, `DressingScope.GoalStandoff`) and the
# widest island here is eight across, so no cell of it is far enough from the monument to plant on.
SKY_OAKS = [
    {"kind": "tree", "id": f"sky-oak-{i}", "seed": 80 + i, "layer": "sky",
     "x": cx - n // 2 + 1, "z": cz - n // 2 + n - 1,
     "form": "template", "species": "oak", "height": 7}
    for i, (cx, cz, n) in enumerate(SKYBLOCKS) if (cx, cz) != GOAL_SKY
]


def piece(ident, x0, z0, x1, z1, surface):
    return {"id": ident, "role": "piece", "rect": cells(x0, z0, x1, z1), "surface": surface}


plan = {
    "plan": 1,
    "meta": {"name": "Liminal DTM II"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": SURFACE,
                # the platform is a 6x6 of bedrock at this height, and the derived surface+15 would
                # stand it in the air over the Village Well
                "observerY": 74},
    "pieces": [
        piece("village", -X_TOWN, 0, X_TOWN, Z_TOWN, SURFACE),
        piece("river-s", -X_BANK, Z_TOWN, X_BANK, Z_EDGE, RIVER),
        piece("river-e", X_TOWN, 0, X_BANK, Z_TOWN, RIVER),
        piece("river-w", -X_BANK, 0, -X_TOWN, Z_TOWN, RIVER),
        piece("taiga",   -X_EDGE, 0, -X_BANK, Z_EDGE, SURFACE),
        # the Pyramid's ground, drawn round the spawn room rather than under it: a spawn marker's
        # protection is the whole piece it stands on, and one piece for the region would bar the
        # enemy from a quarter of the board
        piece("pyramid-w", X_BANK, 0, SPAWN_ROOM[0], Z_EDGE, SURFACE),
        piece("pyramid-e", SPAWN_ROOM[0], 0, X_EDGE, SPAWN_ROOM[1], SURFACE),
        {"id": "pyramid-spawn", "role": "spawn",
         "rect": cells(*SPAWN_ROOM), "surface": PYR_TOP},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "pyramid-spawn",
                    "at": [(SPAWN_AT[0] - SPAWN_ROOM[0]) / CELL, (SPAWN_AT[1] - SPAWN_ROOM[1]) / CELL],
                    "facing": "left"}],
        "iron": [{"id": "iron-1", "piece": "taiga",
                  "at": [(IRON_AT[0] - -X_EDGE) / CELL, IRON_AT[1] / CELL]}],
        "destroyables": [
            {"id": "destroyable-1", "style": "pillar-2", "at": [GOAL_TOWN[0] / CELL, GOAL_TOWN[1] / CELL],
             "materials": "obsidian", "float": 2, "name": "The Desert Well"},
            {"id": "destroyable-2", "style": "pillar-2", "at": [GOAL_POOL[0] / CELL, GOAL_POOL[1] / CELL],
             "materials": "obsidian", "float": 3, "name": "The Deep End"},
            {"id": "destroyable-3", "style": "pillar-2", "at": [GOAL_SKY[0] / CELL, GOAL_SKY[1] / CELL],
             "materials": "obsidian", "float": 2, "name": "The Floating Garden"},
        ],
    },
}


# ══ the roads, and what stands on the hills ═══════════════════════════════════════════════════
# Circulation before scenery: each gate is joined to the Well, so the two sides meet where the roads
# do. Two are authored and fanned into four.
def road(ident, points):
    return {"kind": "stroke", "id": ident, "seed": 4, "points": points, "radius": 3,
            "style": "solid", "route": True, "layer": "ground",
            "pave": noise(6, 9, 2, [solid(13), solid(4)])}


ROADS = [
    road("road-e", [[X_TOWN, 32], [60, 33], [44, 32], [24, 14], [4, 2]]),
    road("road-w", [[-X_TOWN, 32], [-60, 33], [-44, 32], [-24, 14], [-4, 2]]),
]

# Three oaks a hill, and nothing else on them: a hill is a place to fight over, not a wood.
OAKS = [
    {"kind": "tree", "id": f"oak-{i}-{j}", "seed": 20 + 3 * i + j, "layer": "ground",
     "x": cx + dx, "z": cz + dz, "form": "template", "species": "oak", "height": 8}
    for i, (cx, cz) in enumerate(HILLS)
    for j, (dx, dz) in enumerate(((-5, -2), (0, -2), (-3, 2)))
]

# ══ what stands in the village ════════════════════════════════════════════════════════════════
# Five of the vanilla components, one of each, all authored on the +x side of the origin so rot_180
# lands their images on the other side and no building can collide with its own orbit. Sandstone
# walls on sand is the desert village's own idiom rather than the accident the paint rules warn
# about, so what separates a house from the ground under it is the course of orange clay under its
# eaves and the sandstone-slab roof over them.
def house(ident, x0, z0, x1, z1, front, seed):
    return {"kind": "house", "id": ident, "seed": seed, "layer": "ground", "front": front,
            "style": "@desert-house",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}]}


HOUSES = [
    house("small-house", 10, 30, 17, 37, "negZ", 31),      # 7 x 7
    house("large-house", 32,  7, 43, 16, "negX", 32),      # 11 x 9
    house("library",     33, -19, 46, -10, "posZ", 33),    # 13 x 9
    house("blacksmith",  30, -40, 39, -31, "posZ", 34),   # 9 x 9, clear of the wall stairs
    house("church",      18, -4, 25,  5, "negX", 35),      # 7 x 9
]

# ══ the Snowy Taiga ═══════════════════════════════════════════════════════════════════════════
# Spruce and snow against the desert's sand, and two buildings somebody gave up on. Authored on the
# -x side, so rot_180 puts their images in the Taiga at the other end of the other edge.
TAIGA_TREES = [(-120, 12), (-98, 26), (-118, 40), (-92, 46), (-110, 66), (-120, 72), (-100, 8)]
SPRUCE = [
    {"kind": "tree", "id": f"spruce-{i}", "seed": 40 + i, "layer": "ground",
     "x": x, "z": z, "form": "template", "species": "spruce", "height": 12}
    for i, (x, z) in enumerate(TAIGA_TREES)
]

UNFINISHED = [
    house("taiga-shed", -110, 20, -103, 25, "posX", 36),      # 7 x 5, no roof
    house("taiga-hall", -104, 54, -96, 62, "negZ", 37),       # 8 x 8, no roof
]
for build in UNFINISHED:
    build["style"] = "@taiga-unfinished"

TAIGA_FLORA = [{
    "kind": "flora", "id": "taiga-cover", "seed": 44, "layer": "ground",
    "points": [[-122, 4], [-90, 4], [-90, 76], [-122, 76]],
    "spec": {"coverage": 0.4, "scale": 14, "octaves": 3,
             "fernShare": 0.5, "flowerShare": 0.05, "tallShare": 0.3},
}]

# ══ the two ways out of the Pyramid ═══════════════════════════════════════════════════════════
# Orange wool toward the bridge, because a player leaving a spawn needs to be told which way the
# map is; gravel and stone along the edge to the Snowy Taiga, which is the guideline the brief
# asks for rather than a road.
WAYS = [
    {"kind": "stroke", "id": "way-out", "seed": 51, "layer": "ground", "route": True,
     "points": [[SPAWN_ROOM[0], 70], [96, 58], [92, 44], [90, 34]], "radius": 2,
     "style": "solid", "pave": solid(35, 1)},
    {"kind": "stroke", "id": "way-taiga", "seed": 52, "layer": "ground", "route": True,
     "points": [[SPAWN_ROOM[0], 72], [114, 48], [114, 16], [110, -16]], "radius": 3,
     "style": "worn", "coverage": 0.6, "pave": noise(7, 10, 2, [solid(13), solid(1)])},
]

# ══ the Pyramid's own mass ════════════════════════════════════════════════════════════════════
# A hip roof over a square footprint is a pyramid's cap and nothing else: what a vanilla desert
# pyramid mostly is, is the battered mass under it. That is not a house's to draw — it is terrain —
# so it is stated the way every made thing on this board is: override adds, one rectangle a course.
#
# The platform is the spawn PIECE's own surface, four courses over the desert — a piece states its
# height and the compiler seats the spawn on it. Raising the terrain under a stamped room any other
# way leaves the room on the higher ground and its spawn marker at the height the plan still says,
# which is inside the mass: the spawn then walks nowhere and `EX1` refuses the export.
#
# The steps fall away from that platform, two blocks of run to one of rise, which walks both ways for
# nothing. Only the west and north faces carry them, the other two being the board's own edge, and
# each is cut out of the stairwell it crosses — the well is `override` too and a later override on
# the same layer would simply win the column, which would fill the shaft back in.


for k in range(1, PYR_STEPS + 1):
    step = (SPAWN_ROOM[0] - PYR_RUN * k, SPAWN_ROOM[1] - PYR_RUN * k,
            SPAWN_ROOM[0] - PYR_RUN * (k - 1), SPAWN_ROOM[3])
    brow = (SPAWN_ROOM[0] - PYR_RUN * (k - 1), SPAWN_ROOM[1] - PYR_RUN * k,
            SPAWN_ROOM[2], SPAWN_ROOM[1] - PYR_RUN * (k - 1))
    for rect in (step, brow):
        add_shapes += [box("py", *part, GROUND_FLOOR, PYR_TOP - k - GROUND_FLOOR, "pyramid",
                           over=True, keep=True)
                       for part in outside(rect, WELL)]

# ══ the Desert Well the Village Monument hides in ═════════════════════════════════════════════
# The vanilla well's rim, two courses over the road, standing round the goal: the monument is inside
# a structure a player has to take apart rather than a pillar in the open.
# open on all four sides, which is what a vanilla well is and what keeps the goal inside it both
# visible and walkable — a closed rim reads to `SK11` as ground nothing can reach, and to a player
# as a box
add_shapes += ring("dw", GOAL_TOWN[0] - 3, GOAL_TOWN[1] - 3, GOAL_TOWN[0] + 3, GOAL_TOWN[1] + 3,
                   1, GROUND_FLOOR, SURFACE - GROUND_FLOOR + 4, "stair", over=True, keep=True,
                   gaps=[("n", GOAL_TOWN[0] - 1, GOAL_TOWN[0] + 2),
                         ("s", GOAL_TOWN[0] - 1, GOAL_TOWN[0] + 2),
                         ("e", GOAL_TOWN[1] - 1, GOAL_TOWN[1] + 2),
                         ("w", GOAL_TOWN[1] - 1, GOAL_TOWN[1] + 2)])

# ══ the village floor ═════════════════════════════════════════════════════════════════════════
# The brief asks the village for a gentle four-block roll, and a relief is what states one: a mark is
# a CONSTRAINT — the ground here IS h — and everything between the marks is the surface of least
# curvature subject to them, whose extremes can only sit where a mark put one. So a handful of areas
# two courses over and two under the desert give a four-course range that rolls rather than terraces.
#
# A relief is keyed on the island, and this board's ground is one island, so the parts that must NOT
# move have to say so: the river region would otherwise relax up to `base` and lose its eight-course
# drop, and the outer strip would slope into it and take the bridges' landings with it. Every made
# thing is exempt without asking — the wall, the flights, the hills, the Farm, the Pyramid and the
# well are override adds, and an erected shape goes on after the relief rather than into it.
def plots_of(house, margin=4):
    """A building's footprint grown by a margin, and its rot_180 image — the two rects a plateau mark
    under it takes. Both, because only the primary half of the board is solved and its image copied
    back: a house on the far half is pinned by its image, and one straddling the axis needs both or
    the half the solve never visits comes back sloped."""
    (x0, z0), (x1, z1) = house["wings"][0]["corners"]
    rect = (x0 - margin, z0 - margin, x1 + margin, z1 + margin)
    return rect, (-rect[2], -rect[3], -rect[0], -rect[1])


def area(ident, x0, z0, x1, z1, height):
    return {"id": ident, "kind": "area", "h": height,
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


VERGE = 12                          # the band inside the wall the roll is kept out of

RELIEF = {"team": {
    "base": SURFACE, "reach": 24, "step": 1, "stairs": True,
    "marks": [
        # the river region keeps its own floor
        area("river-n", -X_BANK, -Z_EDGE, X_BANK, -Z_TOWN, RIVER),
        # — but only as far out as the water's own band reaches. Past that the region is dry sand
        #   between the channel and the board's edge, and it is the dunes below that shape it
        area("river-s", -X_BANK, Z_TOWN, X_BANK, Z_EDGE - 16, RIVER),
        area("river-e", X_TOWN, -Z_TOWN, X_BANK, Z_TOWN, RIVER),
        area("river-w", -X_BANK, -Z_TOWN, -X_TOWN, Z_TOWN, RIVER),
        # the outer strip is not pinned flat — it rolls too (below) — so what is pinned there is what
        # a crossing needs: the ground a bridge lands on and the bank its slipway is cut into, and the
        # apron the Pyramid's own batter steps down to
        area("land-e", X_BANK, 16, X_BANK + 16, 44, SURFACE),
        area("land-w", -X_BANK - 16, 16, -X_BANK, 44, SURFACE),
        area("pyr-foot", X_BANK + 6, 48, X_EDGE, Z_EDGE, SURFACE),
        # and so does a verge inside the wall: a mark pins its own cells and the relaxation slopes
        # everything within `reach` of one, so an unpinned village floor is drawn down into the
        # river's eight-course drop and the gates come out below the bridges that land in them
        area("verge-n", -X_TOWN, -Z_TOWN, X_TOWN, -Z_TOWN + VERGE, SURFACE),
        area("verge-s", -X_TOWN, Z_TOWN - VERGE, X_TOWN, Z_TOWN, SURFACE),
        area("verge-e", X_TOWN - VERGE, -Z_TOWN, X_TOWN, Z_TOWN, SURFACE),
        area("verge-w", -X_TOWN, -Z_TOWN, -X_TOWN + VERGE, Z_TOWN, SURFACE),
        # then the roll itself, two courses over the desert and two under. Every mark is stated on
        # the board's PRIMARY half — the side the plan's pieces are authored on, here z >= 0 — because
        # a relief is solved over the island's own cells and its mirror copies that solved surface
        # back through the same transform. A mark on the far half is not a second constraint; it is a
        # constraint on cells the solve never visits, and the image of the near half overwrites it.
    ] + [area(f"rise-{i}", x0, z0, x0 + 14, z0 + 14, SURFACE + 2)
         for i, (x0, z0) in enumerate(((-58, 4), (-12, 20), (44, 20), (-4, 4)))]
      + [area(f"dip-{i}", x0, z0, x0 + 14, z0 + 14, SURFACE - 2)
         for i, (x0, z0) in enumerate(((-58, 20), (24, 4), (14, 20), (-30, 2)))]
      # and the outer bank, which is the ground a player crosses between the moat and the two
      # corners: three courses of roll rather than four, so the crossings' aprons still meet it
      + [area(f"bank-up-{i}", x0, z0, x0 + 16, z0 + 16, SURFACE + 2)
         for i, (x0, z0) in enumerate(((94, 0), (-122, 0), (-106, 60), (-122, 30),
                                       (106, 20), (-122, 62)))]
      + [area(f"bank-dn-{i}", x0, z0, x0 + 16, z0 + 16, SURFACE - 1)
         for i, (x0, z0) in enumerate(((108, 2), (-106, 4), (-122, 60), (94, 30),
                                       (-104, 64), (106, 36)))]
      # and the long dry bank on the board's own edge, where the sand meets the water. Dunes only:
      # a channel's level is the LOWEST surface its band crosses, so a hollow inside that band drops
      # the whole river, while a crest inside it changes nothing. The pinned river floor stops ten
      # blocks short of them, and the relaxation between the two is what makes the bank a slope
      # rather than a step.
      + [area(f"dune-{i}", x0, Z_EDGE - 10, x0 + 22, Z_EDGE, RIVER + up)
         for i, (x0, up) in enumerate(((-84, 3), (-56, 5), (-28, 3), (0, 6), (28, 3), (56, 5)))]
      # and last, because a later constraint wins the cells it shares with an earlier one, the ground
      # each building stands on — its footprint mirrored onto the primary half where it was authored
      # on the far one. A house seats on the lowest column of its footprint and the terrain over that
      # floor is carved out of it, so a footprint on a slope shows its foundation on the downhill
      # side (`WX11`); a plateau mark under it is what the rule asks for.
      + [area(f"plot-{h['id']}-{side}", *rect, SURFACE)
         for h in HOUSES + UNFINISHED for side, rect in zip("ab", plots_of(h))]
      # the taiga's iron cube takes one for the same reason, and last for the same reason
      + [area("iron-plot", IRON_AT[0] - 6, IRON_AT[1] - 6,
              IRON_AT[0] + 6, IRON_AT[1] + 6, SURFACE)],
}}

# ── the finish ────────────────────────────────────────────────────────────────────────────────
# `below` inserts at the head of the stack, so the two undercroft layers are listed top-down here
# and land bottom-up in the document: [under, lid, ground, sky].
finish = {
    "authors": ["Opus 5"],
    "created": "2026-08-26",
    "shapePropsByHeight": {
        str(SURFACE): {"floor": GROUND_FLOOR, "base_height": GROUND_H},
        str(RIVER):   {"floor": GROUND_FLOOR, "base_height": RIVER_H},
        str(PYR_TOP): {"floor": GROUND_FLOOR, "base_height": PYR_TOP - GROUND_FLOOR},
    },
    "themeByHeight": {str(SURFACE): "desert", str(RIVER): "riverbed", str(PYR_TOP): "pyramid"},
    # s2 is the Snowy Taiga: the compile emits one shape a piece group, and a height key cannot
    # tell it from the Pyramid, which stands at the same course
    "themeById": {"s2": "taiga"},
    "addShapes": add_shapes,
    "addLayers": [
        {"id": "lid",   "name": "Backroom ceiling", "base_y": 0, "below": True,
         "shapes": lid,
         "islands": [island("lid-maze", "Backroom ceiling", lid_whole, mirrors=False),
                     island("lid-rooms", "Room ceilings", lid_sided)]},
        {"id": "under", "name": "Undercroft",       "base_y": 0, "below": True,
         "shapes": under,
         "islands": [island("under-rock", "The rock", whole, mirrors=False),
                     island("under-rooms", "The rooms", sided)]},
        {"id": "bridge", "name": "Bridges", "base_y": 0,
         "shapes": bridges, "islands": [island("bridge", "Bridges", bridges)]},
        {"id": "sky",   "name": "Skyblocks",        "base_y": 0,
         "shapes": sky,   "islands": [island("sky", "Skyblocks", sky)]},
    ],
    "goalLayers": {"destroyable-1": "ground", "destroyable-2": "under", "destroyable-3": "sky"},
    "roomStyles": {"spawn": "@desert-pyramid"},
    "mapTheme": "desert",
    "themes": THEMES,
    "relief": RELIEF,
    "dressing": {"props": ROADS + WAYS + OAKS + SKY_OAKS + HOUSES + SPRUCE + UNFINISHED
                          + TAIGA_FLORA + [
        # the river: the east half of an oval traced round the town wall, fanned into a closed ring
        {"kind": "water", "id": "river", "seed": 11, "layer": "ground",
         "points": [[0, 58], [48, 58], [68, 54], [78, 44], [80, 24], [80, 0],
                    [80, -24], [78, -44], [68, -54], [48, -58], [0, -58]],
         "radius": 7, "depth": 4, "form": "natural", "edge": 1.2,
         "shore": 3, "shoreWander": True, "bank": solid(12)},
    ]},
    "voidEnforcement": True,
}


def write():
    for name, doc in ((f"{SLUG}.plan.json", plan), (f"{SLUG}.finish.json", finish)):
        with open(os.path.join(HERE, name), "w") as handle:
            json.dump(doc, handle, indent=1)
        print(f"  {name}")


if __name__ == "__main__":
    print(f"{SLUG}: {len(under)} undercroft, {len(lid)} lid, {len(bridges)} bridge, "
          f"{len(sky)} sky, {len(add_shapes)} ground shape(s)")
    write()
