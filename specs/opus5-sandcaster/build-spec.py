#!/usr/bin/env python3
"""Write the finish document for `opus5-sandcaster`.

    python3 specs/opus5-sandcaster/build-spec.py

The board is three landscapes and a buried corridor, so its geometry is a few hundred shapes whose
coordinates are arithmetic on a handful of levels and region bounds. Those are named once at the top
and everything is written from them, which is the only way a tunnel's floor, the lid over it and the
ramp that reaches it can be kept from drifting a course apart.

The plan is authored by hand and is not written here. Output: `opus5-sandcaster.finish.json`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-sandcaster"

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
}


# ── the outline ───────────────────────────────────────────────────────────────────────────────
import math

def wander(z, base, amp, phase, period=33.0, second=0.37):
    """A deterministic edge: two sines of incommensurate period, so the coast never repeats over the
    length of an arm and the script re-runs identical. No generator, no seed to lose."""
    return base + amp * (0.68 * math.sin(z / period + phase)
                         + 0.32 * math.sin(z / (period * second) + phase * 2.1))


def edge(z0, z1, fn, step=8):
    """A boundary sampled as vertices, inclusive of both ends."""
    zs = list(range(z0, z1, step)) + [z1]
    return [[round(fn(z), 1), z] for z in zs]


# The four wandering edges. The period is short enough that each swings both ways over the length of
# an arm rather than bulging one way the whole run, which is what a long period on a 110-block edge
# quietly does. Measured over z 0..200: WEST −54.9..−45.0, EAST 45.2..54.3, CH_W −21.0..−11.3,
# CH_E 11.3..20.2 — so the chasm is never narrower than 22 blocks and the coast never leaves the
# plan's own bbox.
# WEST carries the tunnel, so its swing is narrower and its base further out: the lid reaches
# x −47 the whole length of the workings and a coast that wandered to −45 would put part of it over
# the void. −54.2..−47.8 measured over the board.
WEST   = lambda z: wander(z, -51.0, 3.2, 2.0)     # the outer coast, west
EAST   = lambda z: wander(z,  50.0, 5.0, 4.6)     # the outer coast, east
CH_W   = lambda z: wander(z, -16.0, 5.0, 3.4)     # the chasm's west wall — the reef's own edge
CH_E   = lambda z: wander(z,  16.0, 5.0, 0.9)     # the chasm's east wall — the wash's edge


def controls(ring, k=0.20, only=None):
    """Catmull-Rom handles as cubic Bézier controls: the tangent at a vertex is the chord between its
    two neighbours and each handle reaches k along it. `only` restricts the bend to a run of indices,
    so a seam two shapes share stays straight while the coast beside it curves."""
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


def bent(ring, curved):
    """A ring plus controls on the indices named, as a shapePropsById patch."""
    return {"vertices": ring, "controls": controls(ring, only=set(curved))}


def ring_reef():
    """The reef: outer coast north, straight across the holt seam, chasm wall south, straight
    across the pass seam. Only the two long edges bend; the two seams are shared with another
    shape and have to agree with it block for block."""
    west = edge(ARM_Z0, ARM_Z1, WEST)          # south → north up the coast
    chas = edge(ARM_Z1, ARM_Z0, CH_W, -10)     # north → south down the chasm wall
    ring = west + chas
    curved = set(range(1, len(west) - 1)) | set(range(len(west) + 1, len(ring) - 1))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


def ring_wash():
    """The wash, the same way round: chasm wall north, outer coast south."""
    chas = edge(ARM_Z0, ARM_Z1, CH_E)
    east = edge(ARM_Z1, ARM_Z0, EAST, -10)
    ring = chas + east
    curved = set(range(1, len(chas) - 1)) | set(range(len(chas) + 1, len(ring) - 1))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


def ring_pass():
    """The pass. Its south edge is the axis the board mirrors about and stays dead straight; its
    north edge is the seam the two arms and the chasm's head open off, and stays straight too. Only
    the two ends wander."""
    ring = ([[-50, 0], [50, 0]]
            + edge(8, PASS_Z1, EAST, 8)                       # the east end, going north
            + [[round(WEST(PASS_Z1), 1), PASS_Z1]]            # across the seam
            + edge(PASS_Z1 - 8, 8, WEST, -8))                 # the west end, coming south
    curved = set(range(2, 2 + len(edge(8, PASS_Z1, EAST, 8)))) | \
             set(range(len(ring) - len(edge(PASS_Z1 - 8, 8, WEST, -8)), len(ring)))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


def ring_holt():
    """The back of the board: a straight seam onto the two arms, coast either side, and the spawn
    spur left rectilinear because a stamped building stands on it."""
    east = edge(HOLT_Z0 + 8, HOLT_Z1, EAST)
    west = edge(HOLT_Z1, HOLT_Z0 + 8, WEST, -10)
    spur = [[30, 180], [30, 190], [10, 190], [10, 200], [-10, 200], [-10, 190], [-30, 190], [-30, 180]]
    ring = ([[round(WEST(HOLT_Z0), 1), HOLT_Z0], [round(EAST(HOLT_Z0), 1), HOLT_Z0]]
            + east + spur + west)
    curved = set(range(2, 2 + len(east))) | set(range(len(ring) - len(west), len(ring)))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


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


def blob(pid, cx, cz, rx, rz, theme, lobes=7, twist=0.0):
    """A brush stroke: a small closed ring carrying a theme, added as an **ordinary add one course
    thick**. Paint scopes to the smallest shape covering a cell, so the stroke wins the colour; the
    column's height is decided by `MergeCell`, where the taller add wins — so a one-course stroke
    can never lower the ground it is painted on.

    It is deliberately NOT an override-add. An override-add overwrites the column outright, and a
    shape with no `base_height` rasterizes to a single course at floor 0 (`HeightFn`: `BaseHeight ??
    1`); the relief normally repairs that by writing the solved surface back over the cell, but only
    where the cell is in a solved footprint. Over ground a `relief_scope: "exclude"` shape owns —
    the lid over the workings, here — there is no field to repair it with, and the stroke reads as a
    one-block slab on the bedrock. Measured: eleven strokes punched holes 20 courses deep."""
    verts = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes + twist
        wobble = 0.78 + 0.22 * math.sin(a * 3 + twist * 2)
        verts.append([round(cx + rx * wobble * math.cos(a), 1),
                      round(cz + rz * wobble * math.sin(a), 1)])
    return poly(pid, verts, theme, override=False, base_height=1)


def erect(pid, cx, cz, rx, rz, tops, theme, skirt=3, lobes=6, twist=0.0):
    """A landform stated as its own shape: `raise` reads its datum from the median of the solved
    ground under its footprint, `anchor_heights` are offsets from that, and the skirt is what makes
    it grow out of the ground rather than stand on it."""
    verts = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes + twist
        wobble = 0.75 + 0.25 * math.sin(a * 2 + twist)
        verts.append([round(cx + rx * wobble * math.cos(a), 1),
                      round(cz + rz * wobble * math.sin(a), 1)])
    return poly(pid, verts, theme, height_mode="raise", skirt=skirt,
                base_height=max(tops), anchor_heights=[tops[i % len(tops)] for i in range(lobes)])


# ── the relief ────────────────────────────────────────────────────────────────────────────────
# One island carrying four regions at four heights, so every region is held by an `area` mark at
# its own height before anything else is said. Marks resolve in order and the last wins a contested
# cell: the rim first so nothing cuts a doorway through the coast, then the four regions, then the
# landforms written over them.
def area(mid, ring, h):
    return {"id": mid, "kind": "area", "h": h, "ring": ring}


def point(mid, x, z, h, r):
    return {"id": mid, "kind": "point", "at": [x, z], "h": h, "r": r}


def line(mid, pts, hs, r):
    return {"id": mid, "kind": "line", "points": pts, "h": hs, "r": r}


def relief_marks():
    marks = [{"id": "coast", "kind": "rim", "h": 18, "depth": 1}]
    marks += [area("hold-pass", ring_pass()["vertices"], Y_PASS),
              area("hold-wash", ring_wash()["vertices"], Y_WASH),
              area("hold-reef", ring_reef()["vertices"], Y_REEF),
              area("hold-holt", ring_holt()["vertices"], Y_HOLT)]

    # the reef: a scoured pavement. Four clefts cut into it, and one line held level the whole
    # length of the arm so there is always a road through the towers.
    for i, (x, z, rz) in enumerate(CLEFTS):
        marks.append(area(f"cleft-{i}", [[x - 4, z - rz], [x + 4, z - rz + 3],
                                         [x + 3, z + rz], [x - 5, z + rz - 2]], Y_REEF - 7))
    marks.append(line("reef-road", [[-33, 32], [-30, 62], [-34, 96], [-31, 138]],
                      [Y_REEF, Y_REEF, Y_REEF, Y_REEF], 4))

    # the wash: dunes as stated summits, then the pan held flat over the corridor. The pan is
    # written after them, so where a dune reaches it the pan wins and the dune stops at its edge.
    for i, (x, z, h, r) in enumerate(((24, 44, 27, 8), (40, 62, 29, 9), (26, 92, 28, 8),
                                      (44, 112, 26, 7), (28, 132, 28, 8))):
        marks.append(point(f"dune-{i}", x, z, h, r))
    for i, (x, z) in enumerate(((36, 54), (22, 118))):
        marks.append(area(f"swale-{i}", [[x - 9, z - 7], [x + 8, z - 6], [x + 9, z + 8],
                                         [x - 8, z + 7]], Y_WASH - 5))
    # the dry pan: one genuinely flat place in the dune field, where the wind has scoured to gravel
    marks.append(area("pan", [[34, 76], [48, 78], [48, 118], [34, 116]], Y_WASH))

    # the holt: rolling, and gentle on purpose — this is the ground both goals are walked from.
    for i, (x, z, h, r) in enumerate(((-30, 152, 27, 11), (26, 156, 28, 10), (-6, 170, 26, 9))):
        marks.append(point(f"brow-{i}", x, z, h, r))
    # three knolls on the reef's east strip. None on its west half, which is the lid over the
    # workings and holds y22 whatever the solve says.
    for i, (x, z, h, r) in enumerate(((-24, 62, 26, 5), (-22, 90, 25, 5), (-26, 116, 27, 5))):
        marks.append(point(f"knoll-{i}", x, z, h, r))
    marks.append(area("dell", [[-14, 146], [8, 148], [10, 162], [-12, 160]], Y_HOLT - 4))

    # the pass: a wind-scoured saddle between two knolls, and the saddle is the road across
    marks.append(point("horn-w", -36, 16, 23, 7))
    marks.append(point("horn-e", 34, 14, 22, 7))
    # the saddle: the road across the front. Written last so it wins the two knolls where it meets
    # them, and drawn as a line that wanders rather than a band across the board — a straight mark
    # of even width reads from above as exactly what it is, a rectangle.
    marks.append(line("saddle", [[-52, 22], [-34, 15], [-16, 20], [2, 13], [20, 19], [38, 12], [54, 17]],
                      [Y_PASS, Y_PASS - 3, Y_PASS - 1, Y_PASS - 4, Y_PASS - 1, Y_PASS - 3, Y_PASS], 5))
    return marks


# ── the brush ─────────────────────────────────────────────────────────────────────────────────
# What a single large pattern over a whole region cannot do: say where one material gives way to
# another. Every stroke below answers a *why here* — scree at the foot of a tower, a crest on a dune
# the relief already raised, red sand in the swale it already sank, podzol where the trees stand.
# Six towers. Four stand on the lid over the workings, which a `raise` shape carries perfectly
# because it reads its datum from the solved ground under it and the lid's top IS that ground; two
# stand on the reef's solid east strip.
TOWERS = ((-44, 40, 7, 9, (10, 14, 12, 16)), (-23, 60, 5, 8, (9, 13, 11, 15)),
          (-41, 84, 8, 10, (12, 17, 14, 19)), (-22, 114, 5, 7, (8, 12, 10, 13)),
          (-38, 122, 7, 9, (11, 15, 13, 17)), (-36, 56, 5, 6, (7, 10, 8, 11)))
DUNES = ((24, 44, 8), (40, 62, 9), (26, 92, 8), (44, 112, 7), (28, 132, 8))
SWALES = ((36, 54), (22, 118))
# The clefts sit in the reef's east strip, between the lid's edge at x −30 and the chasm's own wall
# at −19..−12. A cleft cuts to y15 and the lid's floor IS y15, so one drawn over the workings would
# open into the corridor from above — which is a hole in the map rather than a landform.
CLEFTS = ((-23, 48, 8), (-24, 76, 7), (-23, 104, 9), (-25, 128, 7))
COPSES = ((-34, 150, 12, 9), (18, 152, 13, 10), (-8, 168, 10, 8), (36, 168, 9, 7))


def pushes():
    """Rolling ground, added to the solved surface rather than stated into it. A push crosses every
    constraint it covers, so none of these touches the reef — whose lid is `relief_scope: exclude`
    and would be left standing as a step beside ground the push lifted — and none reaches a seam
    between two regions. Wash and holt only, and clear of z 30 and z 140 by more than the falloff.
    """
    out = []
    for i, (x, z, rx, rz, amount, crown) in enumerate((
            (26, 58, 12, 16, 4, 3), (42, 88, 11, 18, 5, 3), (24, 112, 12, 15, 4, 2))):
        ring = [[x - rx, z - rz], [x + rx, z - rz + 4], [x + rx - 2, z + rz],
                [x - rx + 3, z + rz - 3]]
        out.append({"id": f"dune-swell-{i}", "ring": ring, "amount": amount, "falloff": 10,
                    "roughness": 0.5, "crown": crown, "seed": 11 + 2 * i})
    for i, (x, z, rx, rz, amount) in enumerate(((-24, 158, 18, 12, 3), (22, 162, 16, 11, 3))):
        ring = [[x - rx, z - rz], [x + rx, z - rz + 3], [x + rx - 2, z + rz], [x - rx + 2, z + rz - 2]]
        out.append({"id": f"holt-swell-{i}", "ring": ring, "amount": amount, "falloff": 9,
                    "roughness": 0.45, "crown": 2, "seed": 21 + 2 * i})
    return out


def brush():
    out = []
    # the reef: scree spilling off every tower, moss in every cleft, bare pavement between
    for i, (x, z, rx, rz, _tops) in enumerate(TOWERS):
        out.append(blob(f"br-scree-{i}", x + 2, z + rz + 2, rx + 5, rz - 1, "scree", twist=0.4 * i))
    for i, (x, z, rz) in enumerate(CLEFTS):
        out.append(blob(f"br-cleft-{i}", x, z, 5, rz + 2, "cleft", twist=0.7 * i))
    for i, (x, z) in enumerate(((-35, 68), (-26, 92), (-45, 110), (-20, 136))):
        out.append(blob(f"br-pave-{i}", x, z, 9, 7, "tower", lobes=5, twist=0.3 * i))

    # the wash: the pale crest of each dune, red sand in each swale, gravel where the pan is bare
    for i, (x, z, r) in enumerate(DUNES):
        out.append(blob(f"br-crest-{i}", x, z, r - 1, r - 2, "crest", lobes=6, twist=0.5 * i))
    for i, (x, z) in enumerate(SWALES):
        out.append(blob(f"br-hollow-{i}", x, z, 11, 9, "hollow", twist=0.9 * i))
    for i, (x, z, rx, rz) in enumerate(((34, 66, 8, 7), (44, 92, 7, 9), (32, 126, 9, 8))):
        out.append(blob(f"br-pan-{i}", x, z, rx, rz, "pan", lobes=6, twist=0.6 * i))
    # and the drift where the wash spills over the chasm's lip, which is the one place the two
    # palettes touch on open ground
    for i, z in enumerate((46, 78, 110, 134)):
        out.append(blob(f"br-drift-{i}", CH_E(z) + 5, z, 7, 10, "hollow", lobes=6, twist=0.4 * i))

    # the holt: podzol under the copses, worn tracks between them and the spawn
    for i, (x, z, rx, rz) in enumerate(COPSES):
        out.append(blob(f"br-under-{i}", x, z, rx, rz, "understorey", lobes=7, twist=0.35 * i))
    for i, (x, z, rx, rz) in enumerate(((-16, 176, 14, 4), (14, 176, 14, 4), (0, 186, 6, 5),
                                        (-30, 166, 5, 12), (30, 164, 5, 12))):
        out.append(blob(f"br-track-{i}", x, z, rx, rz, "track", lobes=6, twist=0.8 * i))

    # the pass: the reef's pale stone reaching across the saddle from one side and the wash's
    # hard clay from the other, so the front reads as the seam between two countries
    for i, (x, z, rx, rz) in enumerate(((-38, 22, 12, 8), (-18, 9, 11, 7), (-30, 6, 9, 5))):
        out.append(blob(f"br-pass-w-{i}", x, z, rx, rz, "pass-cool", lobes=6, twist=0.5 * i))
    for i, (x, z, rx, rz) in enumerate(((34, 22, 12, 8), (16, 8, 11, 7), (28, 5, 9, 5))):
        out.append(blob(f"br-pass-e-{i}", x, z, rx, rz, "pass-warm", lobes=6, twist=0.7 * i))
    return out


def towers():
    return [erect(f"tor-{i}", x, z, rx, rz, tops, "tower", skirt=3, twist=0.6 * i)
            for i, (x, z, rx, rz, tops) in enumerate(TOWERS)]


# ── the workings ──────────────────────────────────────────────────────────────────────────────
# A layer holds one span per column. So a wall is not a shape standing on a floor — it is the same
# slab carried higher, and a room with something lower inside it is drawn as rectangles clamped
# AROUND that thing rather than under it (`SK9`: a shorter shape inside a taller one on one layer is
# simply not in the world).
POOL_Z0, POOL_Z1 = 92, 112          # the drained pool, midway along the corridor
CIST_Z0, CIST_Z1 = 118, 134         # the cistern chamber, one door, off the corridor's north end
WELLS = (86, 116)                   # two light wells: the only daylight down there


def under_layer():
    S, W = [], -45                                  # W: the outer face of the west wall
    def slab(pid, x0, z0, x1, z1, h, th):
        S.append(rect(pid, x0, z0, x1, z1, th, floor=U_FLOOR, base_height=h))

    # the floor, drawn around the pool and around the cistern's own sunk sill
    slab("u-cor-s", COR_X0, COR_Z0, COR_X1, POOL_Z0, U_H, "corridor")
    slab("u-cor-n", COR_X0, POOL_Z1, COR_X1, COR_Z1, U_H, "corridor")
    slab("u-deck-w", COR_X0, POOL_Z0, COR_X0 + 2, POOL_Z1, U_H, "pool-deck")
    slab("u-deck-e", COR_X1 - 2, POOL_Z0, COR_X1, POOL_Z1, U_H, "pool-deck")
    slab("u-deck-s", COR_X0 + 2, POOL_Z0, COR_X1 - 2, POOL_Z0 + 3, U_H, "pool-deck")
    slab("u-deck-n", COR_X0 + 2, POOL_Z1 - 3, COR_X1 - 2, POOL_Z1, U_H, "pool-deck")
    # the basin, three courses down, and the two lanes in it: the same two courses carrying a
    # different theme, because a stroke prop ignores `layer` and would land on the surface above
    slab("u-basin", COR_X0 + 2, POOL_Z0 + 3, COR_X1 - 2, POOL_Z1 - 3, BASIN_H, "basin")
    slab("u-lane-w", COR_X0 + 3, POOL_Z0 + 5, COR_X0 + 5, POOL_Z1 - 5, BASIN_H, "lane")
    slab("u-lane-e", COR_X1 - 5, POOL_Z0 + 5, COR_X1 - 3, POOL_Z1 - 5, BASIN_H, "lane")

    # four bays off the west wall, identical and evenly spaced: the same room four times
    for i, z in enumerate(BAYS):
        slab(f"u-bay-{i}", W, z, COR_X0, z + 5, U_H, "corridor")
        slab(f"u-bench-{i}", W + 1, z + 1, W + 3, z + 4, U_H + 1, "corridor-wall")

    # the cistern chamber, and the one door into it
    slab("u-cist", COR_X0, CIST_Z0, COR_X1, CIST_Z1, U_H, "cistern")

    # the walls. West is broken by the bays, east is unbroken, and both stop at y15 where the lid's
    # underside begins — eight courses of headroom over the floor.
    def wall(pid, x0, z0, x1, z1, th="corridor-wall"):
        S.append(rect(pid, x0, z0, x1, z1, th, floor=U_FLOOR, base_height=U_WALL_H))
    edges = [COR_Z0 - 2] + [v for z in BAYS for v in (z, z + 5)] + [COR_Z1 + 2]
    for i in range(0, len(edges) - 1, 2):
        wall(f"u-ww-{i}", W, edges[i], COR_X0, edges[i + 1])
    for i, z in enumerate(BAYS):                     # the bays' own back and side walls
        wall(f"u-bw-{i}", W - 2, z - 2, W, z + 7)
    wall("u-ew", COR_X1, COR_Z0 - 2, COR_X1 + 2, COR_Z1 + 2)
    wall("u-end-s", W - 2, COR_Z0 - 2, COR_X1 + 2, COR_Z0)
    wall("u-end-n", W - 2, COR_Z1, COR_X1 + 2, COR_Z1 + 2)
    # the cistern's own walls, with a two-block door in its south face
    wall("u-cist-w", COR_X0 - 2, CIST_Z0 - 2, COR_X0, CIST_Z1 + 2, "cistern")
    wall("u-cist-e", COR_X1, CIST_Z0 - 2, COR_X1 + 2, CIST_Z1 + 2, "cistern")
    wall("u-cist-n", COR_X0, CIST_Z1, COR_X1, CIST_Z1 + 2, "cistern")
    wall("u-cist-sw", COR_X0, CIST_Z0 - 2, COR_X0 + 4, CIST_Z0, "cistern")
    wall("u-cist-se", COR_X1 - 4, CIST_Z0 - 2, COR_X1, CIST_Z0, "cistern")

    # the two ramps, each a wedge from the corridor's floor to the surface it comes up on. A slope
    # of one course a cell builds as treads of two, so the run is over twice the rise on both.
    S.append(poly("u-ramp-s", [[COR_X0 + 1, 36], [COR_X1 - 1, 36],
                               [COR_X1 - 1, COR_Z0], [COR_X0 + 1, COR_Z0]],
                  "corridor", floor=U_FLOOR, base_height=Y_REEF,
                  anchor_heights=[Y_REEF, Y_REEF, U_H, U_H]))
    S.append(poly("u-ramp-n", [[COR_X0 + 1, COR_Z1], [COR_X1 - 1, COR_Z1],
                               [COR_X1 - 1, 175], [COR_X0 + 1, 175]],
                  "corridor", floor=U_FLOOR, base_height=Y_HOLT,
                  anchor_heights=[U_H, U_H, Y_HOLT, Y_HOLT]))
    # No cheek walls beside the ramps. The cutting is exactly the ramp's own width, so its sides are
    # the reef's own rock; a wall drawn there would stand *inside* solid ground, which is what
    # `SK10` reports as two layers driven into each other.
    return S


def lid_and_cuttings():
    """What the ground layer does over the workings: a lid where the corridor runs, holes where the
    two ramps come up and where the two light wells fall in."""
    out = []
    # the lid, drawn as four rectangles round the north cutting's mouth so the ramp has somewhere
    # to arrive; `relief_scope: exclude` keeps it out of the island's solve at exactly y22.
    out.append(rect("lid", LID_X0, LID_Z0, LID_X1, LID_Z1, "reef",
                    floor=LID_FLOOR, base_height=LID_H, relief_scope="exclude"))
    # The two cuttings: the ground is taken out entirely, so the ramp under it IS the ground. Each
    # stops one block short of its ramp's own high end — a subtract that runs past the ramp leaves a
    # gap of pure void between the surface and the top of the way down, and the way down then
    # reaches nothing. That is what `SK11` reports as standable ground with no route onto it.
    out.append(rect("cut-s", COR_X0 + 1, 36, COR_X1 - 1, LID_Z0, None, operation="subtract"))
    out.append(rect("cut-n", COR_X0 + 1, LID_Z1, COR_X1 - 1, 175, None, operation="subtract"))
    # the light wells — square holes in the pan of the reef, fifteen blocks over the corridor floor
    for i, z in enumerate(WELLS):
        out.append(rect(f"well-{i}", -40, z, -36, z + 4, None, operation="subtract"))
    return out


# ── the dressing ──────────────────────────────────────────────────────────────────────────────
def dressing():
    props = []
    # the holt: four copses, dark oak dominant with birch under it, and the density falling at the
    # margin so the wood has an edge rather than a boundary
    wood = [(-46, 146, "dark oak", 13), (-28, 150, "dark oak", 15), (-22, 145, "birch", 11),
            (-29, 163, "dark oak", 14), (-23, 157, "birch", 12), (-17, 152, "birch", 9),
            (12, 147, "dark oak", 14), (19, 153, "dark oak", 13), (25, 147, "birch", 11),
            (14, 159, "birch", 12), (11, 167, "dark oak", 15), (41, 156, "birch", 9),
            (-8, 150, "birch", 11), (-24, 183, "dark oak", 13), (-14, 164, "birch", 10),
            (33, 174, "birch", 10), (44, 166, "dark oak", 12), (-46, 172, "birch", 9),
            (24, 179, "dark oak", 12), (-38, 178, "birch", 10)]
    for i, (x, z, sp, h) in enumerate(wood):
        props.append({"id": f"t{i}", "kind": "tree", "seed": 200 + i, "x": x, "z": z,
                      "form": "template", "species": sp, "height": h})
    for i, (x, z, rx, rz, cov) in enumerate(((-27, 154, 15, 12, 0.5), (20, 156, 15, 12, 0.5),
                                             (-20, 174, 11, 8, 0.35))):
        props.append({"id": f"f{i}", "kind": "flora", "seed": 220 + i,
                      "points": [[x - rx, z - rz], [x + rx, z - rz], [x + rx, z + rz], [x - rx, z + rz]],
                      "spec": {"coverage": cov, "scale": 12, "octaves": 3, "fernShare": 0.4,
                               "flowerShare": 0.08, "flowerScale": 17, "tallShare": 0.12}})

    # the reef: fallen blocks at the foot of the towers, grouped, never scattered
    # A boulder grows from its anchor rather than sitting on it, so three things decide where one may
    # go and none of them is visible in a top-down: the coast (`DR-SITE` — no ground under the
    # footprint), the goal's clearance ring (`OB19`), and every prop already placed (`DR-CLAIM`).
    # x is clamped to the reef's own body and each stone is kept six blocks off the last.
    goal_keep = (-52, -26, 104, 148)          # the Cistern's clearance, widened off its first declines
    placed = []
    for i, (x, z, rx, rz, _t) in enumerate(TOWERS):
        for j, (dx, dz, form, size) in enumerate(((-rx - 4, 2, "angular", 3), (-rx - 7, -5, "round", 2),
                                                  (2, rz + 4, "outcrop", 3))):
            bx, bz = max(-46, min(-18, x + dx)), z + dz
            if goal_keep[0] <= bx <= goal_keep[1] and goal_keep[2] <= bz <= goal_keep[3]:
                continue
            if any(abs(bx - px) < 7 and abs(bz - pz) < 7 for px, pz in placed):
                continue
            placed.append((bx, bz))
            props.append({"id": f"b{i}{j}", "kind": "boulder", "seed": 240 + 4 * i + j,
                          "x": bx, "z": bz, "form": form, "size": size,
                          "mossy": form == "round", "rock": DIORITE})

    # the wash: nothing planted, because a dune field with trees on it is not a dune field. What it
    # gets instead is the one dead thing that grows there, on the swales where water would collect.
    for i, (x, z) in enumerate(SWALES):
        props.append({"id": f"w{i}", "kind": "tree", "seed": 260 + i, "x": x, "z": z - 4,
                      "form": "template", "species": "acacia", "height": 7})
    props.append({"id": "wf", "kind": "flora", "seed": 262,
                  "points": [[18, 40], [30, 40], [30, 130], [18, 130]],
                  "spec": {"coverage": 0.12, "scale": 20, "octaves": 2, "fernShare": 0.0,
                           "flowerShare": 0.05, "flowerScale": 26, "tallShare": 0.5}})

    # the road out of the spawn, forking to the two goals — the circulation diagram, drawn
    props.append({"id": "road-w", "kind": "stroke", "seed": 270,
                  "points": [[0, 188], [-20, 176], [-34, 166], [-38, 150]],
                  "radius": 2, "style": "worn", "coverage": 0.7, "route": True, "pave": COARSE})
    props.append({"id": "road-e", "kind": "stroke", "seed": 271,
                  "points": [[0, 188], [18, 178], [30, 166], [36, 150]],
                  "radius": 2, "style": "worn", "coverage": 0.7, "route": True, "pave": COARSE})
    return {"props": props}


# ── assembly ──────────────────────────────────────────────────────────────────────────────────
def main():
    finish = {
        "authors": ["Opus 5"],
        "roomStyles": {"spawn": "@showcase-hall", "cage": "@showcase-cage"},
        "themes": THEMES,
        "mapTheme": "pass",
        # s0 pass · s1 wash · s2 reef · s3 holt+apron+spawn, read off POST /plan/compile
        "themeById": {"s0": "pass", "s1": "wash", "s2": "reef", "s3": "holt"},
        "shapePropsById": {"s0": ring_pass(), "s1": ring_wash(),
                           "s2": ring_reef(), "s3": ring_holt()},
        "relief": {"team": {"base": Y_WASH, "reach": 16, "step": 1, "stairs": True,
                            "grain": {"amplitude": 1.5, "scale": 12, "seed": 3},
                            "marks": relief_marks(), "pushes": pushes()}},
        "addShapes": lid_and_cuttings() + towers() + brush(),
        "addLayers": [{"id": "under", "name": "The workings", "base_y": 0, "below": True,
                       "shapes": under_layer(),
                       "islands": [{"id": "under", "name": "The workings", "mirrors": True,
                                    "shapeIds": [s["id"] for s in under_layer()]}]}],
        "goalLayers": {"destroyable-2": "under"},
        "dressing": dressing(),
    }
    out = os.path.join(HERE, f"{SLUG}.finish.json")
    with open(out, "w") as handle:
        json.dump(finish, handle, indent=1)
    print(f"{out}: {len(finish['themes'])} themes · {len(finish['addShapes'])} shapes · "
          f"{len(finish['addLayers'][0]['shapes'])} under · "
          f"{len(finish['relief']['team']['marks'])} marks · "
          f"{len(finish['dressing']['props'])} props")


if __name__ == "__main__":
    main()
