#!/usr/bin/env python3
"""Write the finish document for `opus5-sandcaster-ii`.

    python3 specs/opus5-sandcaster-ii/build-spec.py

One open landmass, a range of mountains drawn round it and a corridor buried under the middle of it.
The geometry is a few hundred shapes whose coordinates are arithmetic on a handful of levels, spines
and region bounds; those are named once at the top and everything is written from them, which is the
only way a tunnel's floor, the lid over it and the ramp that reaches it can be kept from drifting a
course apart, and the only way a massif can be moved without its paint staying behind.

The plan is authored by hand and is not written here. Output: `opus5-sandcaster-ii.finish.json`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-sandcaster-ii"

# ── the levels ────────────────────────────────────────────────────────────────────────────────
Y_PASS, Y_WASH, Y_REEF, Y_HOLT = 18, 20, 22, 24   # the plan's four surfaces, as stood-on heights
U_FLOOR, U_H = 0, 7                # the corridor slab: blocks 0..6, stood on at y7
U_WALL_H = 15                      # its walls: blocks 0..14, meeting the lid's underside at y15
BASIN_H = 4                        # the drained basin: blocks 0..3, stood on at y4 — three down
LID_FLOOR, LID_H = 15, 7           # the reef's lid: blocks 15..21, stood on at y22
HOLT_LID_FLOOR, HOLT_LID_H = 19, 5 # the holt's lid: blocks 19..23, stood on at y24

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
CHASM_W = 15                       # the chasm runs x −15..15 the length of both arms
ARM_Z0, ARM_Z1 = 30, 140           # the arms: reef x −50..−15, wash x 15..50
PASS_Z1 = 30                       # the pass: x −50..50, z 0..30
HOLT_Z0, HOLT_Z1 = 140, 180
# The corridor runs under the REEF rather than under the wash, and that is a decision the two
# regions' own landforms make: the reef's are towers standing ON the surface, which a flat lid
# carries perfectly, and the wash's are dunes carved INTO it, which a lid would erase.
COR_X0, COR_X1 = -43, -33          # the corridor, inside its walls at −45..−43 and −33..−31
COR_Z0, COR_Z1 = 66, 140
LID_X0, LID_X1 = -47, -30          # the lid over all of it, and over the four bays at −47..−43
LID_Z0, LID_Z1 = 62, 144
BAYS = (76, 94, 112, 130)          # four identical bays off the west wall, at even 18-block spacing


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


# The board is one hue axis. The reef is the cool pole, the wash the warm one, the holt the green
# that ties them, and the corridor under it all is the same value range gone cold and institutional.
# Nothing on this board is saturated except one prismarine accent in the pool and the obsidian goals.
DIORITE, POL_DIORITE, MUSHROOM = solid(1, 3), solid(1, 4), solid(99)
CLAY, STONE_SLAB, QUARTZ = solid(82), solid(43), solid(155)
STONE, ANDESITE, POL_ANDESITE, STONE_BRICK = solid(1), solid(1, 5), solid(1, 6), solid(98)
COBBLE, GRAVEL, CRACKED, MOSSY = solid(4), solid(13), solid(98, 2), solid(48)
GRANITE = solid(1, 1)

SAND, SANDSTONE, END_STONE, WHITE_CLAY, BIRCH = solid(12), solid(24), solid(121), solid(159), solid(5, 2)
RED_SAND, RED_SANDSTONE, ORANGE_CLAY, HARD_CLAY = solid(12, 1), solid(179), solid(159, 1), solid(172)
ACACIA, YELLOW_CLAY = solid(5, 4), solid(159, 4)

GRASS, GREEN_CLAY, LIME_CLAY = solid(2), solid(159, 13), solid(159, 5)
PODZOL, BROWN_CLAY, DARK_OAK = solid(3, 2), solid(159, 12), solid(5, 5)
COARSE, DIRT = solid(3, 1), solid(3)

PRISMARINE, PRIS_BRICK, DARK_PRIS = solid(168), solid(168, 1), solid(168, 2)
GREY_CLAY, BLACK_CLAY = solid(159, 7), solid(159, 15)


def band(material, thickness):
    return {"material": material, "thickness": thickness}


def layered(bands, beyond=None, axis="depth"):
    return {"kind": "layered", "axis": axis, "beyond": beyond or STONE,
            "stack": {"ending": "handOver", "bands": bands}}


def cell(seed, size, palette, jitter=65, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette}


def voronoi(seed, size, bands):
    return {"kind": "voronoi", "seed": seed, "cellSize": size,
            "bands": [{"depth": d, "material": m} for d, m in bands]}


def noise(seed, scale, stops, octaves=2, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": even, "odd": odd}


def theme(surface, wall, fill, rim=None, rim_edges="void", depth=3, rim_depth=1):
    """A theme's five buckets. `rim` absent turns the rim off rather than guessing one."""
    return {"bedrock": {"relative": False, "value": 1},
            "rimEdges": rim_edges, "wallOnTerrainFaces": True,
            "rim": {"enabled": rim is not None, "depth": rim_depth, "material": rim or COBBLE},
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill}


# ── the themes ────────────────────────────────────────────────────────────────────────────────
# Nine on the surface and six under it. Each names a structural family and one accent and stops.
THEMES = {
    # the reef — a limestone pavement, the cool pole. Pale stone against ash, nothing warm in it.
    "reef": theme(
        layered([band(cell(11, 7, [DIORITE, POL_DIORITE, CLAY, DIORITE, STONE_SLAB]), 1),
                 band(ANDESITE, 2)]),
        layered([band(DIORITE, 1), band(ANDESITE, 3), band(STONE, 3)]),
        STONE, rim=CLAY),
    # the pavement's clefts, where water sat: darker, and the only green on the reef
    "cleft": theme(
        layered([band(cell(13, 4, [MOSSY, COBBLE, GRAVEL, MOSSY]), 1), band(GRAVEL, 2)]),
        layered([band(MOSSY, 1), band(COBBLE, 2), band(STONE, 3)]),
        STONE, rim=MOSSY),
    # scree at the foot of a tower: broken pavement, no rim, because a spill has no edge
    "scree": theme(
        layered([band(cell(17, 3, [GRAVEL, COBBLE, ANDESITE, GRAVEL, CRACKED]), 2)]),
        ANDESITE, STONE),
    # a tower's own flank: banded, so a stack of them reads as bedding rather than as a lump
    "tower": theme(
        cell(19, 5, [POL_DIORITE, DIORITE, MUSHROOM, DIORITE]),
        layered([band(DIORITE, 2), band(CLAY, 2), band(ANDESITE, 3), band(STONE, 4)]),
        STONE, rim=QUARTZ, depth=2),

    # the wash — dunes, the warm pole. Sand against rust, held to the same value as the reef.
    "wash": theme(
        layered([band(cell(23, 9, [SAND, SANDSTONE, END_STONE, SAND, WHITE_CLAY]), 1),
                 band(SANDSTONE, 2)]),
        layered([band(SAND, 1), band(SANDSTONE, 3), band(RED_SANDSTONE, 2), band(HARD_CLAY, 2)]),
        SANDSTONE, rim=SANDSTONE),
    # the crest of a dune, scoured to the pale grains
    "crest": theme(
        layered([band(cell(29, 6, [END_STONE, SAND, WHITE_CLAY, END_STONE]), 2)]),
        SANDSTONE, SANDSTONE),
    # the hollows between dunes, where the red sand collects
    "hollow": theme(
        layered([band(cell(31, 5, [RED_SANDSTONE, SANDSTONE, ORANGE_CLAY, RED_SAND, SANDSTONE]), 1),
                 band(RED_SANDSTONE, 2)]),
        layered([band(RED_SAND, 1), band(RED_SANDSTONE, 3), band(HARD_CLAY, 3)]),
        SANDSTONE),
    # the pan over the corridor: a hard gravel floor the dunes have not covered
    "pan": theme(
        layered([band(cell(37, 4, [GRAVEL, HARD_CLAY, ANDESITE, GRAVEL, ORANGE_CLAY]), 2)]),
        layered([band(GRAVEL, 1), band(HARD_CLAY, 3), band(SANDSTONE, 3)]),
        SANDSTONE, rim=HARD_CLAY),

    # the holt — the green that ties the two poles, over the loam family rather than plain dirt
    "holt": theme(
        layered([band(voronoi(41, 15, [(1, COARSE), (1, GRASS)]), 1), band(DIRT, 2), band(COARSE, 1)]),
        layered([band(PODZOL, 1), band(DIRT, 2), band(COARSE, 2), band(ANDESITE, 3)]),
        STONE, rim=COARSE),
    # under the trees, where nothing grows
    "understorey": theme(
        layered([band(cell(43, 6, [PODZOL, BROWN_CLAY, COARSE, PODZOL]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]),
        STONE),
    # the tracks worn through it
    "track": theme(
        layered([band(cell(47, 3, [COARSE, DIRT, GRAVEL, COARSE]), 2)]),
        DIRT, STONE),

    # the pass — where the two palettes meet, and the only place both are in one theme
    "pass": theme(
        layered([band(cell(53, 8, [ANDESITE, DIORITE, GRANITE, STONE, GRAVEL]), 1),
                 band(ANDESITE, 2)]),
        layered([band(COBBLE, 1), band(ANDESITE, 3), band(GRANITE, 2), band(STONE, 3)]),
        STONE, rim=COBBLE),
    # the two transitions the pass is brushed with: the reef's stone reaching across it from one
    # side and the wash's from the other, each only one step off `pass` so the seam reads as a
    # gradient rather than as two more materials
    "pass-cool": theme(
        layered([band(cell(61, 6, [DIORITE, ANDESITE, CLAY, ANDESITE]), 1), band(ANDESITE, 2)]),
        layered([band(DIORITE, 1), band(ANDESITE, 4), band(STONE, 3)]), STONE),
    "pass-warm": theme(
        layered([band(cell(67, 6, [GRANITE, ANDESITE, SANDSTONE, GRAVEL]), 1), band(GRANITE, 2)]),
        layered([band(GRANITE, 1), band(HARD_CLAY, 3), band(STONE, 3)]), STONE),

    # the corridor under the wash: the same value range gone cold. No hue the surface has.
    "corridor": theme(
        checker(4, CLAY, STONE_SLAB),
        layered([band(CLAY, 2), band(POL_ANDESITE, 5), band(GREY_CLAY, 4)]),
        POL_ANDESITE, rim=CLAY, rim_edges="boundary", depth=2),
    # the walls of it, read as their own surface where a wall's top is walked
    "corridor-wall": theme(
        CLAY,
        layered([band(CLAY, 2), band(POL_ANDESITE, 6), band(GREY_CLAY, 6)]),
        POL_ANDESITE, depth=1),
    # the pool room's deck and its drained basin — the one cold accent on the board
    "pool-deck": theme(
        checker(2, CLAY, QUARTZ),
        layered([band(PRIS_BRICK, 1), band(CLAY, 4)]), POL_ANDESITE,
        rim=PRIS_BRICK, rim_edges="drop", depth=2),
    "basin": theme(
        cell(59, 5, [CLAY, QUARTZ, CLAY, STONE_SLAB]),
        layered([band(PRIS_BRICK, 1), band(PRISMARINE, 3)]), PRISMARINE, depth=2),
    "lane": theme(DARK_PRIS, PRISMARINE, PRISMARINE, depth=2),
    # the cistern chamber: the corridor's palette with the light taken out of it
    "cistern": theme(
        checker(4, POL_ANDESITE, GREY_CLAY),
        layered([band(GREY_CLAY, 2), band(POL_ANDESITE, 6)]), BLACK_CLAY,
        rim=GREY_CLAY, rim_edges="boundary", depth=2),

    # the range: bare rock above the sand and the pavement, and the pale scoured crest above that.
    # Both are the reef's own family — a mountain on this board is the pavement stood on end, not a
    # fourth palette — so nothing new enters the hue axis.
    "crag": theme(
        layered([band(cell(71, 6, [ANDESITE, DIORITE, STONE, GRANITE, GRAVEL]), 1),
                 band(ANDESITE, 2), band(STONE, 2)]),
        layered([band(ANDESITE, 2), band(DIORITE, 2), band(STONE, 4), band(GRANITE, 3)]),
        STONE, rim=ANDESITE),
    "summit": theme(
        layered([band(cell(73, 5, [QUARTZ, POL_DIORITE, DIORITE, WHITE_CLAY]), 2),
                 band(DIORITE, 2)]),
        layered([band(POL_DIORITE, 1), band(DIORITE, 3), band(ANDESITE, 4)]),
        STONE, rim=QUARTZ, depth=2),
    # the shaded inner flank, where the corries bite in
    "shadow": theme(
        layered([band(cell(79, 5, [ANDESITE, GRAVEL, COBBLE, ANDESITE, CRACKED]), 1),
                 band(GRAVEL, 2)]),
        layered([band(ANDESITE, 1), band(COBBLE, 3), band(STONE, 4)]),
        STONE, rim=GRAVEL),
}


# ── the outline ───────────────────────────────────────────────────────────────────────────────
import math

def wander(z, base, amp, phase, period=41.0, second=0.37):
    """A deterministic edge: two sines of incommensurate period, so the coast never repeats over the
    length of the board and the script re-runs identical. No generator, no seed to lose."""
    return base + amp * (0.68 * math.sin(z / period + phase)
                         + 0.32 * math.sin(z / (period * second) + phase * 2.1))


def controls(ring, k=0.20, only=None):
    """Catmull-Rom handles as cubic Bézier controls: the tangent at a vertex is the chord between its
    two neighbours and each handle reaches k along it. `only` restricts the bend to a run of indices,
    so the seam the board mirrors about stays dead straight while the coast beside it curves."""
    n, out = len(ring), {}
    for i, (x, z) in enumerate(ring):
        if only is not None and i not in only:
            continue
        px, pz = ring[(i - 1) % n]
        nx, nz = ring[(i + 1) % n]
        tx, tz = (nx - px) * k, (nz - pz) * k
        out[str(i)] = {"in": [round(x - tx, 2), round(z - tz, 2)],
                       "out": [round(x + tx, 2), round(z + tz, 2)]}
    return out


# The compiled outline is one shape: a staircase of six nested rectangles, widest at the basin and
# narrowing to the spawn. Its two long sides are replaced by wandering edges and its z = 0 face is
# not, because that face is the axis the board mirrors about — a coast that wandered there would
# meet its own `rot_180` image half a block out and leave a seam of void down the middle.
TIERS = [(0, 40, 40), (40, 80, 50), (80, 120, 45), (120, 170, 35), (170, 190, 25), (190, 200, 10)]
BOARD_Z1 = 200


def half_width(z):
    for z0, z1, hw in TIERS:
        if z0 <= z <= z1:
            return hw
    return 10


def coast(side, phase):
    """One long side of the board, sampled every six blocks: the tier's own half-width pulled in by
    a wander that never reaches the tier below it, so the silhouette is the plan's and the edge is
    not a staircase."""
    pts = []
    for z in list(range(0, BOARD_Z1, 6)) + [BOARD_Z1]:
        hw = half_width(z)
        inset = 2.5 + 2.5 * wander(z, 0.0, 1.0, phase)
        pts.append([round(side * (hw - inset), 1), z])
    return pts


def outline():
    """The whole landmass as one bent ring. West side south → north, across the spawn's head, east
    side north → south, and the straight mirror face home."""
    west = coast(-1, 2.0)
    east = coast(1, 4.6)[::-1]
    ring = west + east
    curved = set(range(1, len(west) - 1)) | set(range(len(west) + 1, len(ring) - 1))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


def land_halfwidth(z):
    """What a brush stroke may reach at this z, two blocks inside the drawn coast. A one-course add
    on a cell no region shape covers is the only add on that column and builds a speck of bedrock
    standing over the void — `/coverage` reports it as an island hundreds of blocks from used
    ground, and it is the one way paint can put a hole in a map."""
    hw = half_width(max(0, min(BOARD_Z1, abs(z))))
    return max(0.0, hw - 8.0)


def clamp(x, z):
    zc = max(-BOARD_Z1 + 4, min(BOARD_Z1 - 4, z))
    hw = land_halfwidth(zc)
    return round(max(-hw, min(hw, x)), 1), round(zc, 1)


def clamp_int(x, z):
    """The same clamp for a dressing prop, whose x and z are read as whole numbers (`DR-DOC`)."""
    cx, cz = clamp(x, z)
    return int(round(cx)), int(round(cz))


# ── shapes ────────────────────────────────────────────────────────────────────────────────────
def poly(pid, verts, theme=None, override=True, **kw):
    s = {"id": pid, "type": "polygon", "operation": "add", "override": override, "vertices": verts}
    if theme: s["theme"] = theme
    s.update(kw)
    return s


def rect(pid, x0, z0, x1, z1, theme=None, **kw):
    s = {"id": pid, "type": "rectangle", "operation": "add", "override": True,
         "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}
    if theme: s["theme"] = theme
    s.update(kw)
    return s


def ring_of(cx, cz, rx, rz, lobes=9, twist=0.0, clamped=True):
    """A closed ring with no straight edge in it, optionally clamped into the land."""
    verts = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes + twist
        wobble = 0.78 + 0.22 * math.sin(a * 3 + twist * 2)
        x, z = cx + rx * wobble * math.cos(a), cz + rz * wobble * math.sin(a)
        verts.append(list(clamp(x, z)) if clamped else [round(x, 1), round(z, 1)])
    return verts


def blob(pid, cx, cz, rx, rz, theme, lobes=7, twist=0.0):
    """A brush stroke: a small closed ring carrying a theme, added as an ordinary add one course
    thick. Paint scopes to the smallest shape covering a cell, so the stroke wins the colour; the
    column's height is decided by `MergeCell`, where the taller add wins — so a one-course stroke
    can never lower the ground it is painted on, and it is safe over ground a `relief_scope:
    "exclude"` shape owns, which an override-add is not."""
    return poly(pid, ring_of(cx, cz, rx, rz, lobes, twist), theme, override=False, base_height=1)


def swollen(x0, z0, x1, z1, amp=4.0, step=8, phase=0.0):
    """A rectangle's outline pushed OUTWARD by a wander, sampled every few blocks. Outward rather
    than either way, because the shape this draws has to cover the rectangle it was given — a lid
    that wanders inward opens a hole over the corridor it roofs."""
    out = []
    for z in list(range(z0, z1, step)) + [z1]:
        out.append([round(x1 + amp * (0.5 + 0.5 * math.sin(z / 17.0 + phase)), 1), z])
    for x in list(range(x1, x0, -step)) + [x0]:
        out.append([x, round(z1 + amp * (0.5 + 0.5 * math.sin(x / 13.0 + phase * 2)), 1)])
    for z in list(range(z1, z0, -step)) + [z0]:
        out.append([round(x0 - amp * (0.5 + 0.5 * math.sin(z / 19.0 + phase * 3)), 1), z])
    for x in list(range(x0, x1, step)) + [x1]:
        out.append([x, round(z0 - amp * (0.5 + 0.5 * math.sin(x / 11.0 + phase)), 1)])
    return out


def ribbon(spine, half, wobble=0.22, phase=0.0):
    """A closed ring around a polyline — a massif's footprint — and the spine index each ring vertex
    came from, so a per-vertex lift array can be built from the spine's own profile."""
    ring, src = [], []
    n = len(spine)
    def normal(i):
        j, k = min(i + 1, n - 1), max(i - 1, 0)
        dx, dz = spine[j][0] - spine[k][0], spine[j][1] - spine[k][1]
        length = math.hypot(dx, dz) or 1.0
        return dz / length, -dx / length
    for side in (1, -1):
        for i in (range(n) if side == 1 else range(n - 1, -1, -1)):
            nx, nz = normal(i)
            w = half * (1.0 + wobble * math.sin(i * 1.7 + phase + (0.0 if side == 1 else 2.3)))
            ring.append([round(spine[i][0] + side * nx * w, 1),
                         round(spine[i][1] + side * nz * w, 1)])
            src.append(i)
    return ring, src


# ── the levels and the frame ──────────────────────────────────────────────────────────────────
Y_BASE = 22                        # the board's ground, and the plan's own surface
U_FLOOR, U_H = 0, 7                # the corridor slab: blocks 0..6, stood on at y7
U_WALL_H = 15                      # its walls: blocks 0..14, meeting the lid's underside at y15
BASIN_H = 4                        # the drained pool: blocks 0..3, stood on at y4 — three down
LID_FLOOR, LID_H = 15, 7           # the lid over the workings: blocks 15..21, stood on at y22

COR_X0, COR_X1 = -14, -2           # the corridor, inside its walls at −16..−14 and −2..0
COR_Z0, COR_Z1 = 62, 148
LID_X0, LID_X1 = -19, 9            # the lid, over the corridor and over the four bays at 0..6
LID_Z0, LID_Z1 = 58, 152
BAYS = (72, 92, 112, 132)          # four bays off the EAST wall, at even 20-block spacing
POOL_Z0, POOL_Z1 = 76, 96          # the drained pool, south of the cistern
CIST_Z0, CIST_Z1 = 102, 124        # the cistern chamber, where the second goal stands
WELLS = (70, 138)                  # two light wells: the only daylight down there
RAMP_S_Z0, RAMP_N_Z1 = 32, 178     # the ramps' open ends — run 30 against a rise of 15

# The range. Two massifs and a spur inside each, drawn as pushes rather than stated as marks: a
# mark is a constraint honoured exactly with no falloff, so a `point` summit is a flat drum on a
# sheer wall and a `line` ridge is a wall with a flat top. `crown` is what makes a mountain — it
# lifts the ring's own medial axis, a point on a round ring and a crest on a long one — and
# `falloff` is what leaves a map: at 20 on a board this wide the two skirts meet in the middle.
SPINE_W = [[-45, 4], [-39, 32], [-44, 60], [-37, 88], [-42, 116], [-36, 140]]
LIFT_W  = [12, 28, 17, 31, 20, 10]
SPINE_E = [[45, 12], [38, 40], [43, 68], [36, 96], [41, 124], [35, 148]]
LIFT_E  = [11, 24, 30, 18, 27, 10]
SPUR_W  = [[-30, 20], [-26, 50], [-31, 80], [-25, 108]]
LIFT_SW = [7, 13, 9, 14]
SPUR_E  = [[30, 28], [25, 58], [30, 88], [24, 116]]
LIFT_SE = [8, 12, 10, 13]
SUMMITS = [(SPINE_W[1], 0), (SPINE_W[3], 1), (SPINE_E[2], 2), (SPINE_E[4], 3)]
CORRIES = [(-38, 74), (38, 82)]

# The three landscapes, painted onto one open landmass rather than cut into separate pieces. The
# wash takes the west of the middle and the reef the east; `rot_180` hands each team both.
DUNES  = ((-27, 30, 8), (-24, 60, 7), (-26, 88, 8), (-23, 112, 7), (-25, 46, 6))
SWALES = ((-25, 44), (-24, 100))
PAVE   = ((22, 38, 9, 7), (30, 66, 8, 9), (20, 94, 9, 8), (28, 118, 8, 7))
CLEFTS = ((17, 52, 8), (24, 80, 7), (16, 106, 8))
# The copses are kept off the two roads and out of the apron in front of the spawn's door: a tree
# within three blocks of a route is declined (`DR-ROAD`), one on it is declined by the route's own
# claim (`DR-CLAIM`), and one in a doorway's approach is declined by the keep-out (`DR-KEEP`).
COPSES = ((-30, 124, 10, 8), (-13, 128, 8, 7), (13, 132, 8, 7), (30, 128, 10, 8),
          (-28, 144, 10, 9), (28, 148, 10, 9), (0, 138, 8, 7), (-20, 162, 9, 8),
          (20, 166, 9, 8), (-30, 174, 8, 6), (30, 178, 8, 6))


def relief_marks():
    """Only the ground a player has to stand on is pinned. Pinning a region flat because it should
    be about that height leaves the solver nothing to solve, and a board with a mark on every region
    is a table with bumps on it however tall the bumps are. Four marks: the coast, the open floor,
    the goal's shelf and the spawn's apron. The rim is written first, because a rim written after a
    landform cuts a doorway through the coast where the two meet."""
    return [
        {"id": "coast", "kind": "rim", "h": Y_BASE, "depth": 1},
        {"id": "floor", "kind": "line",
         "points": [[0, 4], [-7, 48], [6, 96], [-5, 140], [0, 184]],
         "h": [Y_BASE, Y_BASE, Y_BASE, Y_BASE, Y_BASE], "r": 26},
        {"id": "shelf", "kind": "area", "h": Y_BASE + 2,
         "ring": ring_of(25, 112, 14, 11, twist=0.3)},
        {"id": "apron", "kind": "area", "h": Y_BASE + 2,
         "ring": ring_of(0, 184, 22, 9, lobes=11, twist=0.9)},
    ]


def pushes():
    out = []
    for pid, spine, lift, half, crown, fall, seed in (
            ("massif-w", SPINE_W, LIFT_W, 10, 14, 12, 3),
            ("massif-e", SPINE_E, LIFT_E, 10, 14, 12, 7),
            ("spur-w",   SPUR_W,  LIFT_SW, 7,  8,  9, 11),
            ("spur-e",   SPUR_E,  LIFT_SE, 7,  8,  9, 15)):
        ring, src = ribbon(spine, half, phase=seed * 0.4)
        out.append({"id": pid, "ring": ring, "amount": max(lift),
                    "amounts": [lift[i] for i in src],
                    "falloff": fall, "roughness": 0.38, "crown": crown, "seed": seed})
    # a corrie bitten out of each massif's inner flank: a negative crown dishes the ring it is
    # drawn on rather than doming it
    for i, (x, z) in enumerate(CORRIES):
        out.append({"id": f"corrie-{i}", "ring": ring_of(x, z, 9, 8, twist=0.5 + i, clamped=False),
                    "amount": 3, "falloff": 7, "roughness": 0.3, "crown": -10, "seed": 21 + i})
    # the dune field in the wash: the same operation at a tenth of the amount, and a positive crown
    # so each swell has a back rather than a table. None of them reaches the lid — a push over
    # ground `relief_scope: "exclude"` owns is not applied, and the step where it stopped would show.
    for i, (x, z, r) in enumerate(DUNES):
        out.append({"id": f"dune-{i}", "ring": ring_of(x, z, r + 4, r + 6, lobes=7,
                                                       twist=0.6 * i, clamped=False),
                    "amount": 5, "falloff": 8, "roughness": 0.5, "crown": 4, "seed": 31 + i})
    for i, (x, z) in enumerate(SWALES):
        out.append({"id": f"swale-{i}", "ring": ring_of(x, z, 9, 7, twist=1.1 * i, clamped=False),
                    "amount": 1, "falloff": 6, "roughness": 0.4, "crown": -5, "seed": 41 + i})
    return out


# ── the brush ─────────────────────────────────────────────────────────────────────────────────
# What a single large pattern over a whole region cannot do: say where one material gives way to
# another. Every stroke answers a *why here* — bare rock on a crest the pushes raised, scoured pale
# stone on a summit, red sand in a swale they sank, podzol where the trees stand. Every stroke is
# placed off a spine or a landform rather than typed as a coordinate, so moving a massif moves its
# paint with it, and every vertex is clamped into the land.
def brush():
    out = []
    # The three landscapes, painted at region scale first. Paint scopes to the SMALLEST shape
    # covering a cell, so a region-wide stroke is a ground the detail strokes below are read
    # against rather than a layer that hides them: the crag on a massif, the pavement on the east
    # of the middle, the wood at the back, and the wash left as the board's own theme.
    for pid, spine, half, seed in (("rg-crag-w", SPINE_W, 11, 3), ("rg-crag-e", SPINE_E, 11, 7)):
        ring, _src = ribbon(spine, half, phase=seed * 0.4)
        out.append(poly(pid, [list(clamp(x, z)) for x, z in ring], "crag",
                        override=False, base_height=1))
    for pid, box, theme, phase in (("rg-reef", (10, 14, 40, 122), "reef", 0.7),
                                   ("rg-holt", (-33, 118, 33, 190), "holt", 2.1)):
        out.append(poly(pid, [list(clamp(x, z)) for x, z in swollen(*box, amp=6, phase=phase)],
                        theme, override=False, base_height=1))

    # the range: the scoured crest of each summit, bare rock along both spines between them, and
    # the shaded rock in each corrie
    for i, (point, _n) in enumerate(SUMMITS):
        out.append(blob(f"br-summit-{i}", point[0], point[1], 8, 8, "summit", twist=0.4 * i))
    for i, (spine, index) in enumerate([(SPINE_W, 0), (SPINE_W, 2), (SPINE_W, 4), (SPINE_W, 5),
                                        (SPINE_E, 0), (SPINE_E, 1), (SPINE_E, 3), (SPINE_E, 5)]):
        out.append(blob(f"br-crag-{i}", spine[index][0], spine[index][1], 9, 12, "crag",
                        twist=0.6 * i))
    for i, (x, z) in enumerate(CORRIES):
        out.append(blob(f"br-shadow-{i}", x, z, 10, 9, "shadow", twist=0.8 * i))
    # scree where each massif's skirt runs out onto the flat, one step in from the spine
    for i, (spine, index, side) in enumerate([(SPINE_W, 1, 1), (SPINE_W, 3, 1), (SPINE_W, 4, 1),
                                              (SPINE_E, 2, -1), (SPINE_E, 4, -1), (SPINE_E, 1, -1)]):
        out.append(blob(f"br-scree-{i}", spine[index][0] + side * 12, spine[index][1], 7, 11,
                        "scree", twist=0.5 * i))

    # the wash: the pale crest of every dune, red sand in every swale, the hard pan where the
    # dunes have not covered it
    for i, (x, z, r) in enumerate(DUNES):
        out.append(blob(f"br-crest-{i}", x, z, r - 1, r - 2, "crest", lobes=6, twist=0.5 * i))
    for i, (x, z) in enumerate(SWALES):
        out.append(blob(f"br-hollow-{i}", x, z, 11, 9, "hollow", twist=0.9 * i))
    for i, (x, z, rx, rz) in enumerate(((-24, 20, 8, 7), (-22, 74, 7, 9), (-25, 126, 8, 8))):
        out.append(blob(f"br-pan-{i}", x, z, rx, rz, "pan", lobes=6, twist=0.6 * i))
    for i, (x, z) in enumerate(((-24, 100, ), (-26, 132,))):
        out.append(blob(f"br-wash-{i}", x, z, 10, 9, "wash", lobes=6, twist=0.7 * i))

    # the reef: pavement where the ground is bare, moss in every cleft
    for i, (x, z, rx, rz) in enumerate(PAVE):
        out.append(blob(f"br-pave-{i}", x, z, rx, rz, "tower", lobes=5, twist=0.3 * i))
    for i, (x, z, rz) in enumerate(CLEFTS):
        out.append(blob(f"br-cleft-{i}", x, z, 5, rz + 2, "cleft", twist=0.7 * i))

    # the holt: podzol under every copse, worn tracks between them and the spawn
    for i, (x, z, rx, rz) in enumerate(COPSES):
        out.append(blob(f"br-under-{i}", x, z, rx, rz, "understorey", lobes=7, twist=0.35 * i))
    for i, (x, z, rx, rz) in enumerate(((-14, 182, 12, 4), (12, 182, 12, 4), (0, 192, 6, 4),
                                        (-22, 160, 5, 12), (22, 158, 5, 12))):
        out.append(blob(f"br-track-{i}", x, z, rx, rz, "track", lobes=6, twist=0.8 * i))

    # the pass: the reef's pale stone reaching across the front from one side and the wash's hard
    # clay from the other, so the seam reads as the border between two countries rather than as a
    # third material
    for i, (x, z, rx, rz) in enumerate(((-28, 22, 12, 8), (-14, 8, 11, 7), (-24, 4, 9, 5))):
        out.append(blob(f"br-pass-w-{i}", x, z, rx, rz, "pass-warm", lobes=6, twist=0.5 * i))
    for i, (x, z, rx, rz) in enumerate(((26, 22, 12, 8), (12, 8, 11, 7), (22, 4, 9, 5))):
        out.append(blob(f"br-pass-e-{i}", x, z, rx, rz, "pass-cool", lobes=6, twist=0.7 * i))
    return out


# ── the workings ──────────────────────────────────────────────────────────────────────────────
# A layer holds one span per column. So a wall is not a shape standing on a floor — it is the same
# slab carried higher, and a room with something lower inside it is drawn as rectangles clamped
# AROUND that thing rather than under it (`SK9`: a shorter shape inside a taller one on one layer is
# simply not in the world).
def under_layer():
    S = []
    E = COR_X1 + 2                                  # E: the outer face of the east wall

    def slab(pid, x0, z0, x1, z1, h, th):
        S.append(rect(pid, x0, z0, x1, z1, th, floor=U_FLOOR, base_height=h))

    def wall(pid, x0, z0, x1, z1, th="corridor-wall"):
        S.append(rect(pid, x0, z0, x1, z1, th, floor=U_FLOOR, base_height=U_WALL_H))

    # the floor, drawn around the pool's sunk basin
    slab("u-cor-s", COR_X0, COR_Z0, COR_X1, POOL_Z0, U_H, "corridor")
    slab("u-cor-n", COR_X0, POOL_Z1, COR_X1, COR_Z1, U_H, "corridor")
    slab("u-deck-w", COR_X0, POOL_Z0, COR_X0 + 2, POOL_Z1, U_H, "pool-deck")
    slab("u-deck-e", COR_X1 - 2, POOL_Z0, COR_X1, POOL_Z1, U_H, "pool-deck")
    slab("u-deck-s", COR_X0 + 2, POOL_Z0, COR_X1 - 2, POOL_Z0 + 3, U_H, "pool-deck")
    slab("u-deck-n", COR_X0 + 2, POOL_Z1 - 3, COR_X1 - 2, POOL_Z1, U_H, "pool-deck")
    slab("u-basin", COR_X0 + 2, POOL_Z0 + 3, COR_X1 - 2, POOL_Z1 - 3, BASIN_H, "basin")
    slab("u-lane-w", COR_X0 + 3, POOL_Z0 + 5, COR_X0 + 5, POOL_Z1 - 5, BASIN_H, "lane")
    slab("u-lane-e", COR_X1 - 5, POOL_Z0 + 5, COR_X1 - 3, POOL_Z1 - 5, BASIN_H, "lane")

    # four bays off the east wall, identical and evenly spaced: the same room four times
    for i, z in enumerate(BAYS):
        slab(f"u-bay-{i}", COR_X1, z, E + 4, z + 5, U_H, "corridor")
        slab(f"u-bench-{i}", E + 1, z + 1, E + 3, z + 4, U_H + 1, "corridor-wall")

    # the cistern chamber, where the second goal stands
    slab("u-cist", COR_X0, CIST_Z0, COR_X1, CIST_Z1, U_H, "cistern")

    # the walls. East is broken by the bays, west is unbroken, and both stop at y15 where the lid's
    # underside begins — eight courses of headroom over the floor.
    edges = [COR_Z0 - 2] + [v for z in BAYS for v in (z, z + 5)] + [COR_Z1 + 2]
    for i in range(0, len(edges) - 1, 2):
        wall(f"u-ew-{i}", COR_X1, edges[i], E, edges[i + 1])
    for i, z in enumerate(BAYS):                     # each bay's own back and side walls
        wall(f"u-bw-{i}", E + 4, z - 2, E + 6, z + 7)
        wall(f"u-bs-{i}", COR_X1, z - 2, E + 6, z)
        wall(f"u-bn-{i}", COR_X1, z + 5, E + 6, z + 7)
    wall("u-ww", COR_X0 - 2, COR_Z0 - 2, COR_X0, COR_Z1 + 2)
    # The two end walls are drawn in halves, clear of the ramp between them. Among the shapes of one
    # layer the TALLER override-add wins the column, not the later one, so a wall drawn across a ramp
    # does not lose to it — it plugs it, and the way down then ends in solid rock with the corridor
    # behind it detached from the board (`SK11`). Measured: a 3-block plug at z 59..61 sealed both
    # mouths and the whole workings read as an island.
    for pid, z0, z1 in (("u-end-s", COR_Z0 - 2, COR_Z0), ("u-end-n", COR_Z1, COR_Z1 + 2)):
        wall(f"{pid}-w", COR_X0 - 2, z0, COR_X0 + 1, z1)
        wall(f"{pid}-e", COR_X1 - 1, z0, E, z1)
    # the cistern's own walls, with a four-block door in each of its end faces for the same reason
    wall("u-cist-w", COR_X0 - 2, CIST_Z0 - 2, COR_X0, CIST_Z1 + 2, "cistern")
    wall("u-cist-e", COR_X1, CIST_Z0 - 2, COR_X1 + 2, CIST_Z1 + 2, "cistern")
    wall("u-cist-sw", COR_X0, CIST_Z0 - 2, COR_X0 + 4, CIST_Z0, "cistern")
    wall("u-cist-se", COR_X1 - 4, CIST_Z0 - 2, COR_X1, CIST_Z0, "cistern")
    wall("u-cist-nw", COR_X0, CIST_Z1, COR_X0 + 4, CIST_Z1 + 2, "cistern")
    wall("u-cist-ne", COR_X1 - 4, CIST_Z1, COR_X1, CIST_Z1 + 2, "cistern")

    # the two ramps, each a wedge from the corridor's floor to the ground it comes up on. A slope of
    # one course a cell builds as treads of two, so the run is over twice the rise on both: 30
    # against 15. No cheek walls beside them — the cutting is exactly the ramp's own width, so its
    # sides are the board's own rock, and a wall drawn there would stand INSIDE solid ground, which
    # is what `SK10` reports as two layers driven into each other.
    S.append(poly("u-ramp-s", [[COR_X0 + 1, RAMP_S_Z0], [COR_X1 - 1, RAMP_S_Z0],
                               [COR_X1 - 1, COR_Z0], [COR_X0 + 1, COR_Z0]],
                  "corridor", floor=U_FLOOR, base_height=Y_BASE,
                  anchor_heights=[Y_BASE, Y_BASE, U_H, U_H]))
    S.append(poly("u-ramp-n", [[COR_X0 + 1, COR_Z1], [COR_X1 - 1, COR_Z1],
                               [COR_X1 - 1, RAMP_N_Z1], [COR_X0 + 1, RAMP_N_Z1]],
                  "corridor", floor=U_FLOOR, base_height=Y_BASE,
                  anchor_heights=[U_H, U_H, Y_BASE, Y_BASE]))
    return S


def lid_and_cuttings():
    """What the ground layer does over the workings: a lid where the corridor runs, holes where the
    two ramps come up and where the two light wells fall in."""
    out = []
    # `relief_scope: exclude` takes the lid's cells out of the island's solve, so it stands at
    # exactly y22 and the relaxation bends round it as it bends round void.
    out.append(poly("lid", swollen(LID_X0, LID_Z0, LID_X1, LID_Z1, phase=1.3), "pan",
                    floor=LID_FLOOR, base_height=LID_H, relief_scope="exclude"))
    # The two cuttings: the ground is taken out entirely, so the ramp under it IS the ground. Each
    # stops where the lid begins — a subtract that runs past its ramp's high end leaves a gap of
    # pure void between the surface and the top of the way down, which `SK11` reports as standable
    # ground with no route onto it.
    out.append(rect("cut-s", COR_X0 + 1, RAMP_S_Z0, COR_X1 - 1, LID_Z0, None, operation="subtract"))
    out.append(rect("cut-n", COR_X0 + 1, LID_Z1, COR_X1 - 1, RAMP_N_Z1, None, operation="subtract"))
    # the light wells — square holes in the lid, fifteen blocks over the corridor floor
    for i, z in enumerate(WELLS):
        out.append(rect(f"well-{i}", COR_X0 + 3, z, COR_X0 + 7, z + 4, None, operation="subtract"))
    return out


# ── the dressing ─────────────────────────────────────────────────────────────────────────────
# Five things can refuse a prop and none of them is visible in a plan view: the coast (`DR-SITE` —
# no ground under the footprint), a goal's clearance ring (`OB19`), the approach in front of a door
# (`DR-KEEP`), a route's own claim on the cells it paves (`DR-CLAIM`), and the three-block margin
# either side of that route (`DR-ROAD`). A tree also claims every cell its CANOPY reaches rather
# than its trunk cell, so two placed nine blocks apart can still argue. Rather than hand-tuning
# coordinates against five rules, the copses state where a wood is and a filter decides which of
# their trees are actually planted — the same answer the dressing pass would give, arrived at before
# the post rather than after it.
ROADS = ([[0, 188], [-11, 172], [-13, 150], [-9, 128]],
         [[0, 188], [11, 174], [13, 150], [9, 128]])
GOAL_KEEPS = ((10, 40, 96, 128), (-24, 8, 96, 128))
DOOR_KEEP = (-16, 16, 166, 200)


def seg_distance(px, pz, ax, az, bx, bz):
    dx, dz = bx - ax, bz - az
    length = dx * dx + dz * dz
    t = 0.0 if length == 0 else max(0.0, min(1.0, ((px - ax) * dx + (pz - az) * dz) / length))
    return math.hypot(px - (ax + t * dx), pz - (az + t * dz))


def road_distance(x, z):
    return min(seg_distance(x, z, *road[i], *road[i + 1])
               for road in ROADS for i in range(len(road) - 1))


def blocked(x, z):
    if any(x0 <= x <= x1 and z0 <= z <= z1 for x0, x1, z0, z1 in GOAL_KEEPS):
        return True
    if DOOR_KEEP[0] <= x <= DOOR_KEEP[1] and DOOR_KEEP[2] <= z <= DOOR_KEEP[3]:
        return True
    return road_distance(x, z) < 6.0


def dressing():
    props, placed = [], []

    def free(x, z, gap):
        return not blocked(x, z) and all(math.hypot(x - px, z - pz) >= gap for px, pz in placed)

    # the range first, so the wood yields to the rock rather than the other way round: fallen blocks
    # where each massif's skirt runs out onto the flat
    for i, (spine, index, side) in enumerate([(SPINE_W, 1, 1), (SPINE_W, 2, 1), (SPINE_W, 4, 1),
                                              (SPINE_E, 1, -1), (SPINE_E, 3, -1), (SPINE_E, 4, -1)]):
        for j, (dx, dz, form, size) in enumerate(((14, 3, "angular", 3), (18, -6, "round", 2),
                                                  (11, 9, "outcrop", 3))):
            x, z = clamp_int(spine[index][0] + side * dx, spine[index][1] + dz)
            if not free(x, z, 8.0):
                continue
            placed.append((x, z))
            props.append({"id": f"b{i}{j}", "kind": "boulder", "seed": 240 + 4 * i + j,
                          "x": x, "z": z, "form": form, "size": size,
                          "mossy": form == "round", "rock": DIORITE})

    # the holt: copses of dark oak with birch under them, five stands to a copse and the density
    # falling at the margin so the wood has an edge rather than a boundary
    trees = 0
    for i, (cx, cz, rx, rz) in enumerate(COPSES):
        for dx, dz, species, height in ((0, 0, "dark oak", 15),
                                        (-rx + 2, -rz + 3, "dark oak", 14),
                                        (rx - 2, -rz + 3, "birch", 11),
                                        (rx - 3, rz - 3, "birch", 12),
                                        (-rx + 3, rz - 3, "dark oak", 13),
                                        (0, -rz - 3, "birch", 10),
                                        (0, rz + 3, "birch", 9),
                                        (-rx - 4, 0, "dark oak", 12),
                                        (rx + 4, 0, "dark oak", 12)):
            x, z = clamp_int(cx + dx, cz + dz)
            if not free(x, z, 8.0):
                continue
            placed.append((x, z))
            props.append({"id": f"t{trees}", "kind": "tree", "seed": 200 + trees, "x": x, "z": z,
                          "form": "template", "species": species, "height": height})
            trees += 1
    for i, (cx, cz, rx, rz) in enumerate(COPSES[:6]):
        props.append({"id": f"f{i}", "kind": "flora", "seed": 220 + i,
                      "points": [[cx - rx, cz - rz], [cx + rx, cz - rz],
                                 [cx + rx, cz + rz], [cx - rx, cz + rz]],
                      "spec": {"coverage": 0.45, "scale": 12, "octaves": 3, "fernShare": 0.4,
                               "flowerShare": 0.08, "flowerScale": 17, "tallShare": 0.12}})

    # the wash: nothing planted, because a dune field with trees on it is not a dune field. What it
    # gets instead is the one dead thing that grows there, on the swales where water would collect.
    for i, (x, z) in enumerate(SWALES):
        x, z = clamp_int(x, z - 5)
        if not free(x, z, 10.0):
            continue
        placed.append((x, z))
        props.append({"id": f"w{i}", "kind": "tree", "seed": 260 + i, "x": x, "z": z,
                      "form": "template", "species": "acacia", "height": 7})
    props.append({"id": "wf", "kind": "flora", "seed": 262,
                  "points": [[-30, 30], [-16, 30], [-16, 120], [-30, 120]],
                  "spec": {"coverage": 0.12, "scale": 20, "octaves": 2, "fernShare": 0.0,
                           "flowerShare": 0.05, "flowerScale": 26, "tallShare": 0.5}})

    # the road out of the spawn, forking to the two goals — the circulation diagram, drawn
    for name, road in (("road-w", ROADS[0]), ("road-e", ROADS[1])):
        props.append({"id": name, "kind": "stroke", "seed": 270 + len(props) % 2,
                      "points": road, "radius": 2, "style": "worn", "coverage": 0.7,
                      "route": True, "pave": COARSE})
    return {"props": props}


# ── assembly ──────────────────────────────────────────────────────────────────────────────────
def main():
    under = under_layer()
    finish = {
        "authors": ["Opus 5"],
        "roomStyles": {"spawn": "@showcase-hall", "cage": "@showcase-cage"},
        "themes": THEMES,
        "mapTheme": "pass",
        # one compiled shape: six nested rectangles resolve to a single open landmass, which is the
        # whole difference from the first Sandcaster. Read off POST /plan/compile.
        "themeById": {"s0": "wash"},
        "shapePropsById": {"s0": outline()},
        "relief": {"team": {"base": Y_BASE, "reach": 0, "step": 1, "stairs": True,
                            "grain": {"amplitude": 2.0, "scale": 13, "seed": 5},
                            "marks": relief_marks(), "pushes": pushes()}},
        "addShapes": lid_and_cuttings() + brush(),
        "addLayers": [{"id": "under", "name": "The workings", "base_y": 0, "below": True,
                       "shapes": under,
                       "islands": [{"id": "under", "name": "The workings", "mirrors": True,
                                    "shapeIds": [s["id"] for s in under]}]}],
        "dressing": dressing(),
    }
    out = os.path.join(HERE, f"{SLUG}.finish.json")
    with open(out, "w") as handle:
        json.dump(finish, handle, indent=1)
    print(f"{out}: {len(finish['themes'])} themes · {len(finish['addShapes'])} shapes · "
          f"{len(under)} under · {len(finish['relief']['team']['marks'])} marks · "
          f"{len(finish['relief']['team']['pushes'])} pushes · "
          f"{len(finish['dressing']['props'])} props")


if __name__ == "__main__":
    main()
