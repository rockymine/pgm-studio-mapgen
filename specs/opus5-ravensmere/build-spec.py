#!/usr/bin/env python3
"""Write the finish document for `opus5-ravensmere`.

    python3 specs/opus5-ravensmere/build-spec.py

One open landmass on a single layer: a mere with an island in it, a sand beach round the mere, rolling
downs cut by three crevasses, a wood, a brick-and-granite path with buildings scattered off it, and a
mountain backdrop standing behind the spawn. The geometry is arithmetic on a handful of levels, radii and
spines named once at the top, so a landform can be moved without its paint staying behind.

The plan is authored by hand and is not written here. Output: `opus5-ravensmere.finish.json`.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-ravensmere"


# ── materials ─────────────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


# One hue axis. The mere is the cool pole and the strand the warm one; the sward is the green that ties
# them, and the range behind the spawn is the crevasse's own rock stood on end rather than a fourth
# palette. Nothing is saturated except the end stone of the goal.
STONE, GRANITE, POL_GRANITE = solid(1), solid(1, 1), solid(1, 2)
DIORITE, POL_DIORITE, ANDESITE = solid(1, 3), solid(1, 4), solid(1, 5)
COBBLE, MOSSY, GRAVEL = solid(4), solid(48), solid(13)
GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
SAND, SANDSTONE, PALE_SAND = solid(12), solid(24), solid(121)
CLAY, HARD_CLAY, BRICK = solid(82), solid(172), solid(45)
BROWN_CLAY, GREEN_CLAY, WHITE_CLAY = solid(159, 12), solid(159, 13), solid(159)
STONE_BRICK = solid(98)

# Every block above is claimed by a paint family (`TerrainPalette.Grouped`). A block no family names
# reads as magenta on `render/surface` and says nothing about the ground it is on, so end stone stands
# in for smooth sandstone (24:2, unclaimed) and stained clay for the mushroom block (99:0).


def band(material, thickness):
    return {"material": material, "thickness": thickness}


def layered(bands, beyond=None, axis="depth"):
    return {"kind": "layered", "axis": axis, "beyond": beyond or STONE,
            "stack": {"ending": "handOver", "bands": bands}}


def cell(seed, size, palette, jitter=65, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": palette}


def theme(surface, wall, fill, rim=None, rim_edges="void", depth=3, rim_depth=1):
    out = {"bedrock": {"relative": False, "value": 1}, "rimEdges": rim_edges,
           "wallOnTerrainFaces": True,
           "rim": {"enabled": rim is not None, "depth": rim_depth,
                   "material": rim or solid(4)},
           "surface": {"enabled": True, "depth": depth, "material": surface},
           "wall": wall, "wallEnabled": True, "fill": fill}
    return out


# ── the themes ────────────────────────────────────────────────────────────────────────────────
# Eleven grounds and five seams. A seam theme is not a twelfth ground: it is one step off each of the two
# it stands between, so a stroke of it reads as the two mixing rather than as a third material arriving.
THEMES = {
    # the mere — under the water, and never seen dry
    "mere": theme(
        layered([band(cell(11, 6, [GRAVEL, CLAY, DIRT, GRAVEL, COARSE]), 2)]),
        layered([band(GRAVEL, 1), band(CLAY, 3), band(STONE, 4)]), STONE),
    # the shelf the water thins over
    "shallow": theme(
        layered([band(cell(13, 5, [SAND, GRAVEL, CLAY, SAND]), 2)]),
        layered([band(SAND, 1), band(SANDSTONE, 3), band(STONE, 3)]), SANDSTONE),

    # the strand — the beach, and the largest single ground on the board
    "strand": theme(
        layered([band(cell(17, 9, [SAND, SAND, SANDSTONE, SAND, PALE_SAND]), 2),
                 band(SANDSTONE, 2)]),
        layered([band(SAND, 2), band(SANDSTONE, 4), band(HARD_CLAY, 3)]),
        SANDSTONE, rim=SAND),
    # the dry back of it, where the wind has scoured to the stone under
    "dune": theme(
        layered([band(cell(19, 7, [SAND, PALE_SAND, SANDSTONE, SAND]), 2)]),
        layered([band(SAND, 1), band(SANDSTONE, 4)]), SANDSTONE),

    # the sward — the green that ties the two poles
    "sward": theme(
        layered([band(cell(23, 11, [GRASS, GRASS, COARSE, GRASS, PODZOL]), 1), band(DIRT, 2),
                 band(COARSE, 1)]),
        layered([band(GRASS, 1), band(DIRT, 3), band(COARSE, 2), band(ANDESITE, 3)]),
        STONE, rim=COARSE),
    # the downs above it: the same green with the rock beginning to show through
    "downs": theme(
        layered([band(cell(29, 8, [GRASS, COARSE, GRASS, ANDESITE, GRASS]), 1), band(DIRT, 2),
                 band(ANDESITE, 1)]),
        layered([band(GRASS, 1), band(DIRT, 2), band(ANDESITE, 3), band(STONE, 3)]),
        STONE, rim=COARSE),

    # the scar — a crevasse's floor and its walls, the one place the board's bones are bare
    "scar": theme(
        layered([band(cell(31, 5, [ANDESITE, STONE, COBBLE, GRAVEL, ANDESITE]), 2),
                 band(STONE, 2)]),
        layered([band(ANDESITE, 2), band(STONE, 3), band(COBBLE, 2), band(GRANITE, 3)]),
        STONE, rim=COBBLE),
    # damp at the bottom of one, where nothing dries
    "sump": theme(
        layered([band(cell(37, 4, [MOSSY, COBBLE, GRAVEL, MOSSY]), 2)]),
        layered([band(MOSSY, 1), band(COBBLE, 3), band(STONE, 4)]), STONE),

    # the holt — the wood, and the floor under its canopy
    "holt": theme(
        layered([band(cell(41, 10, [GRASS, PODZOL, GRASS, COARSE, GRASS]), 1), band(DIRT, 2),
                 band(COARSE, 1)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(COARSE, 2), band(ANDESITE, 3)]),
        STONE, rim=COARSE),
    "understorey": theme(
        layered([band(cell(43, 6, [PODZOL, BROWN_CLAY, COARSE, PODZOL]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),

    # the range behind the spawn: the scar's rock stood on end, and the pale scoured crest above it
    "crag": theme(
        layered([band(cell(47, 7, [ANDESITE, STONE, GRANITE, ANDESITE, GRAVEL]), 1),
                 band(ANDESITE, 2), band(STONE, 2)]),
        layered([band(ANDESITE, 2), band(STONE, 4), band(GRANITE, 3), band(DIORITE, 2)]),
        STONE, rim=ANDESITE),
    "summit": theme(
        layered([band(cell(53, 6, [POL_DIORITE, DIORITE, STONE, WHITE_CLAY]), 2), band(DIORITE, 2)]),
        layered([band(POL_DIORITE, 1), band(DIORITE, 3), band(ANDESITE, 4)]),
        STONE, rim=POL_DIORITE, depth=2),

    # the isle in the mere: sward over the sandstone the mere cut it from
    "isle": theme(
        layered([band(cell(59, 6, [GRASS, GRASS, COARSE, GREEN_CLAY, GRASS]), 1), band(SANDSTONE, 2)]),
        layered([band(GRASS, 1), band(SANDSTONE, 4), band(STONE, 3)]),
        SANDSTONE, rim=SANDSTONE),

    # ── the five seams ─────────────────────────────────────────────────────────────────────────
    # water to sand: the wet edge, where the gravel the mere carries meets the beach
    "seam-mere": theme(
        layered([band(cell(61, 5, [GRAVEL, SAND, CLAY, GRAVEL, SAND]), 2)]),
        layered([band(GRAVEL, 1), band(SANDSTONE, 3), band(STONE, 3)]), SANDSTONE),
    # sand to grass: the strand giving out into the sward, one stroke of each in the other
    "seam-strand": theme(
        layered([band(cell(67, 7, [SAND, GRASS, COARSE, SAND, GRASS]), 1), band(SANDSTONE, 2)]),
        layered([band(SAND, 1), band(DIRT, 3), band(SANDSTONE, 3)]), SANDSTONE),
    # grass to bare rock, on the lip of every crevasse
    "seam-scar": theme(
        layered([band(cell(71, 5, [GRASS, ANDESITE, COARSE, COBBLE, GRASS]), 1), band(DIRT, 2)]),
        layered([band(COARSE, 1), band(ANDESITE, 3), band(STONE, 4)]), STONE),
    # sward to wood: more podzol, less grass, no new material
    "seam-holt": theme(
        layered([band(cell(73, 8, [GRASS, PODZOL, GRASS, PODZOL, COARSE]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),
    # the foot of the range, where the mountain runs out into grass
    "seam-crag": theme(
        layered([band(cell(79, 6, [ANDESITE, GRASS, COARSE, STONE, GRASS]), 1), band(DIRT, 1),
                 band(ANDESITE, 2)]),
        layered([band(ANDESITE, 2), band(DIRT, 2), band(STONE, 4)]), STONE),
}


# ── the frame ─────────────────────────────────────────────────────────────────────────────────
Y_BASE = 24                        # the board's ground, and the plan's own surface
Y_MERE, Y_ISLE = 15, 22            # the mere's bed, and the isle standing out of it
Y_CREV = 12                        # a crevasse floor — twelve courses under the downs
Y_PAD = 26                         # the flats: the goal's ground, the apron and the spawn's

MERE_RX, MERE_RZ = 40, 30          # the mere's bed, an ellipse about the board's own centre
ISLE_RX, ISLE_RZ = 13, 11
WATER_RX, WATER_RZ = 25, 19        # the water prop's centreline, a CLOSED RING inside the bed
WATER_R = 12                       # its half-width: the band runs from the isle's edge out to r 37

BOARD_Z1 = 150
# The tiers the plan compiles to, widest at the mere and narrowing to the spawn, with the backdrop
# opening out again behind it.
# The coast wanders up to five blocks inside the tier it is drawn from, so a stroke clamped to the
# tier itself can still hang over the void: the inset is the wander plus a margin.
TIERS = [(-10, 10, 75), (0, 35, 75), (35, 75, 70), (75, 100, 60),
         (100, 115, 45), (115, 125, 45), (125, 150, 45)]
INSET = 8


def half_width(z):
    z = abs(z)
    best = 0.0
    for z0, z1, hw in TIERS:
        if abs(z0) <= z <= z1:
            best = max(best, hw)
    return best


def land_halfwidth(z):
    """What a brush stroke may reach at this z. A one-course add on a cell no region shape covers is
    the only add on that column and builds a speck of bedrock standing over the void."""
    return max(0.0, half_width(max(0, min(BOARD_Z1, abs(z)))) - INSET)


def clamp(x, z):
    zc = max(-BOARD_Z1 + 2, min(BOARD_Z1 - 2, z))
    hw = land_halfwidth(zc)
    return round(max(-hw, min(hw, x)), 1), round(zc, 1)


def clamp_int(x, z):
    cx, cz = clamp(x, z)
    return int(round(cx)), int(round(cz))


# ── shapes ────────────────────────────────────────────────────────────────────────────────────
def poly(pid, verts, theme=None, override=True, **kw):
    s = {"id": pid, "type": "polygon", "operation": "add", "override": override, "vertices": verts}
    if theme: s["theme"] = theme
    s.update(kw)
    return s


def ring_of(cx, cz, rx, rz, lobes=9, twist=0.0, clamped=True):
    """A closed ring with no straight edge in it. An `area` mark written as a rectangle builds a
    plateau with four sheer sides; the same mark on a lobed ring reads as ground."""
    verts = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes + twist
        wobble = 0.80 + 0.20 * math.sin(a * 3 + twist * 2)
        x, z = cx + rx * wobble * math.cos(a), cz + rz * wobble * math.sin(a)
        verts.append(list(clamp(x, z)) if clamped else [round(x, 1), round(z, 1)])
    return verts


def fold(cx, cz):
    """Author on the +z half and let the orbit fan the rest. A stroke drawn wholly on the -z half is
    outside the compiled ground's own polygon — the compiler emits one half and mirrors it — so the
    canvas reads it as an island of its own. Three islands where the board has one, all carrying the
    same restored id, is what silently detaches a relief keyed by that id."""
    return (-cx, -cz) if cz < 0 else (cx, cz)


def blob(pid, cx, cz, rx, rz, theme, lobes=7, twist=0.0):
    """A brush stroke: a small closed ring carrying a theme, added as an ordinary add one course
    thick. Paint scopes to the smallest shape covering a cell, so the stroke wins the colour; the
    column's height is decided by the taller add, so it can never lower what it is painted on."""
    cx, cz = fold(cx, cz)
    return poly(pid, ring_of(cx, cz, rx, rz, lobes, twist), theme, override=False, base_height=1)


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


def wander(z, base, amp, phase, period=47.0, second=0.37):
    """A deterministic edge: two sines of incommensurate period, so the coast never repeats over the
    length of the board and the script re-runs identical."""
    return base + amp * (0.68 * math.sin(z / period + phase)
                         + 0.32 * math.sin(z / (period * second) + phase * 2.1))


def controls(ring, k=0.20, only=None):
    """Catmull-Rom handles as cubic Bezier controls, so the coast curves rather than turning corners.
    `only` restricts the bend, which is what keeps the seam the board mirrors about dead straight."""
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


def coast(side, phase):
    pts = []
    for z in list(range(0, BOARD_Z1, 5)) + [BOARD_Z1]:
        inset = 2.0 + 3.0 * wander(z, 0.0, 1.0, phase)
        pts.append([round(side * (half_width(z) - inset), 1), z])
    return pts


def outline():
    """The whole landmass as one bent ring. The z = 0 face is left straight because it is the axis the
    board mirrors about — a coast that wandered there would meet its own `rot_180` image half a block
    out and leave a seam of void down the middle of the mere."""
    west = coast(-1, 2.0)
    east = coast(1, 4.6)[::-1]
    ring = west + east
    curved = set(range(1, len(west) - 1)) | set(range(len(west) + 1, len(ring) - 1))
    return {"vertices": ring, "controls": controls(ring, only=curved)}


# ── the landforms ─────────────────────────────────────────────────────────────────────────────
# Constraints state the PLAN of the board — where the water is, where the flats are, where the ground
# is cut through. Pushes state its RELIEF — the hills and the range. A mark is honoured exactly and has
# no falloff, so it can pin a lake bed or cut a crevasse with sheer walls but can never be a mountain;
# a push lifts the solved surface inside a drawn ring, and its `crown` is what makes a landform of it.
CREVASSES = (
    ("crev-w", [[-70, 58], [-58, 64], [-46, 60], [-36, 66]]),
    ("crev-e", [[68, 50], [57, 56], [47, 53], [38, 58]]),
    ("crev-n", [[-58, 84], [-46, 90], [-34, 86], [-24, 92]]),
)
# Rolling hills: small pushes over the downs and the wood, kept clear of the crevasses and of the
# goal's own flat — a push crosses every constraint it covers, so one drawn over a cut fills it in.
# Every hill is kept clear of two things, because a push crosses whatever it covers: the road, which
# has to stay walkable end to end, and the goal's own flat, which a push's edge would tilt. The
# clearance is the ring's radius plus its falloff — 24 blocks for the largest of them.
# None of them is on the beach. A push's skirt is where its gradient lives, and the two roads that
# loop round the mere cross the sand from end to end: a hill sited there put a two-block riser in one
# of them, which is the one thing a path may not have. Rolling ground is the downs' and the wood's.
HILLS = ((-52, 72, 10, 8, 6), (58, 70, 10, 8, 6), (-70, 74, 10, 8, 5),
         (52, 84, 10, 8, 5), (54, 96, 12, 9, 6), (-38, 104, 12, 9, 5),
         (36, 104, 12, 9, 6), (-24, 110, 11, 8, 4), (22, 110, 11, 8, 4))
# The range behind the spawn, drawn the way `showcase/19-mountain-range` draws one.
SPINE_W = [[-42, 132], [-31, 143], [-20, 133], [-10, 142]]
LIFT_W = [20, 34, 24, 32]
SPINE_E = [[10, 142], [20, 133], [31, 144], [42, 133]]
LIFT_E = [32, 24, 36, 20]
SUMMITS = ((SPINE_W[1], 0), (SPINE_W[3], 1), (SPINE_E[0], 2), (SPINE_E[2], 3))
GOAL = (30, 69)


def relief_marks():
    """Written in the order they resolve: the rim first, so nothing cuts a doorway through the coast,
    then the water's own ground, then the flats a player has to stand on, then the crevasses last —
    because a cut has to win the cells it takes from the plateau it is cut into."""
    marks = [{"id": "coast", "kind": "rim", "h": Y_BASE, "depth": 1},
             {"id": "mere", "kind": "area", "h": Y_MERE,
              "ring": ring_of(0, 0, MERE_RX, MERE_RZ, lobes=17, twist=0.4, clamped=False)},
             {"id": "isle", "kind": "area", "h": Y_ISLE,
              "ring": ring_of(0, 0, ISLE_RX, ISLE_RZ, lobes=9, twist=1.1, clamped=False)},
             # the downs and the wood, held level so the hills have something to roll over and the
             # crevasses have something with a straight lip to cut through
             {"id": "downs", "kind": "area", "h": Y_PAD,
              "ring": ring_of(0, 66, 68, 17, lobes=15, twist=0.2, clamped=False)},
             {"id": "wood", "kind": "area", "h": Y_PAD,
              "ring": ring_of(0, 94, 57, 17, lobes=15, twist=1.4, clamped=False)},
             {"id": "apron", "kind": "area", "h": Y_PAD,
              "ring": ring_of(0, 108, 42, 9, lobes=11, twist=0.7, clamped=False)},
             {"id": "spawnpad", "kind": "area", "h": Y_PAD,
              "ring": ring_of(0, 120, 9, 5, lobes=9, twist=0.3, clamped=False)},
             ]
    # Each crevasse tapers back up to the ground at both ends, so it is a cut in the downs rather
    # than a channel that halves the board.
    for pid, points in CREVASSES:
        marks.append({"id": pid, "kind": "line", "points": points,
                      "h": [Y_PAD, Y_CREV, Y_CREV, Y_PAD], "r": 3})
    # The goal's own flat is written LAST, after the cuts: marks resolve in order and the last wins a
    # contested cell, so the ground the Wardstone stands on cannot be taken by a crevasse that passes
    # near it however close the two are drawn.
    marks.append({"id": "goalpad", "kind": "area", "h": Y_PAD + 1,
                  "ring": ring_of(GOAL[0], GOAL[1], 13, 11, lobes=9, twist=0.9, clamped=False)})
    return marks


def pushes():
    out = []
    for i, (x, z, rx, rz, amount) in enumerate(HILLS):
        out.append({"id": f"hill-{i}", "ring": ring_of(x, z, rx, rz, lobes=8, twist=0.6 * i,
                                                       clamped=False),
                    "amount": amount, "falloff": 12, "roughness": 0.55,
                    "crown": 4 + (i % 3), "seed": 31 + i})
    for pid, spine, lift, seed in (("range-w", SPINE_W, LIFT_W, 3),
                                   ("range-e", SPINE_E, LIFT_E, 7)):
        ring, src = ribbon(spine, 9, phase=seed * 0.4)
        out.append({"id": pid, "ring": ring, "amount": max(lift),
                    "amounts": [lift[i] for i in src],
                    "falloff": 12, "roughness": 0.38, "crown": 16, "seed": seed})
    return out


# ── the brush ─────────────────────────────────────────────────────────────────────────────────
# Two passes. The first paints the five grounds at region scale; the second answers *why here* for
# every patch inside them, and strings the seam themes along every boundary between two grounds.
# Paint scopes to the SMALLEST shape covering a cell, so a later, smaller stroke always wins — which
# is what lets one ring of `strand` carry the whole beach and a dozen strokes sit inside it.
def around(cx, cz, rx, rz, count, phase=0.0, half=True):
    """Points spaced round an ellipse — the way a seam is walked. `half` walks only the upper arc,
    because a ring about the board's own centre is its own `rot_180` image: authoring the whole ring
    draws every stroke twice and puts half of them on the mirrored side of the compiled ground."""
    span = math.pi if half else 2 * math.pi
    out = []
    for i in range(count):
        a = span * i / count + phase
        out.append((cx + rx * math.cos(a), cz + rz * math.sin(a)))
    return out


def brush():
    out = []

    # ── the grounds ────────────────────────────────────────────────────────────────────────────
    out.append(blob("rg-strand", 0, 0, 72, 50, "strand", lobes=15, twist=0.3))
    out.append(blob("rg-downs", 0, 66, 70, 18, "downs", lobes=15, twist=0.9))
    out.append(blob("rg-holt", 0, 96, 58, 21, "holt", lobes=15, twist=1.7))
    for pid, spine, seed in (("rg-crag-w", SPINE_W, 3), ("rg-crag-e", SPINE_E, 7)):
        ring, _src = ribbon(spine, 13, phase=seed * 0.4)
        out.append(poly(pid, [list(clamp(x, z)) for x, z in ring], "crag",
                        override=False, base_height=1))
    # the mere's own bed, and the isle standing in the middle of it — each smaller than the ground
    # it is drawn over, so each wins the cells it covers
    out.append(blob("rg-mere", 0, 0, MERE_RX + 1, MERE_RZ + 1, "mere", lobes=17, twist=0.4))
    out.append(blob("rg-isle", 0, 0, ISLE_RX, ISLE_RZ, "isle", lobes=9, twist=1.1))

    # ── inside each ground ─────────────────────────────────────────────────────────────────────
    # the beach: dry scoured dune at the back of it, where the sand stops being washed
    for i, (x, z) in enumerate([(-58, 22), (-34, -30), (36, 26), (58, -20), (-64, -8), (62, 6)]):
        out.append(blob(f"br-dune-{i}", x, z, 13, 10, "dune", twist=0.5 * i))
    # the shelf the water thins over, just inside the water's outer edge
    for i, (x, z) in enumerate(around(0, 0, 34, 25, 5, 0.4)):
        out.append(blob(f"br-shallow-{i}", x, z, 9, 7, "shallow", lobes=6, twist=0.7 * i))
    # the crevasses: a ribbon of bare rock along each cut rather than a row of round patches, and moss
    # in the bottom of it where nothing dries
    for pid, points in CREVASSES:
        ring, _src = ribbon(points, 7, phase=0.9)
        out.append(poly(f"br-scar-{pid}", [list(clamp(x, z)) for x, z in ring], "scar",
                        override=False, base_height=1))
        mid = points[len(points) // 2]
        out.append(blob(f"br-sump-{pid}", mid[0], mid[1], 7, 5, "sump", lobes=6, twist=1.2))
    # the wood: podzol under every copse
    for i, (x, z) in enumerate([(-40, 88), (-16, 96), (10, 90), (34, 98), (-30, 104), (24, 106)]):
        out.append(blob(f"br-under-{i}", x, z, 13, 10, "understorey", twist=0.35 * i))
    # the range: a scoured crest on every summit
    for i, (point, _n) in enumerate(SUMMITS):
        out.append(blob(f"br-summit-{i}", point[0], point[1], 9, 8, "summit", twist=0.4 * i))

    # ── the five seams ─────────────────────────────────────────────────────────────────────────
    # water to sand, all the way round the mere's outer edge
    for i, (x, z) in enumerate(around(0, 0, MERE_RX - 1, MERE_RZ - 1, 7, 0.2)):
        out.append(blob(f"sm-mere-{i}", x, z, 10, 8, "seam-mere", lobes=6, twist=0.6 * i))
    # sand to grass, round the back of the beach
    for i, (x, z) in enumerate(around(0, 0, 70, 48, 7, 0.5)):
        out.append(blob(f"sm-strand-{i}", x, z, 12, 10, "seam-strand", lobes=6, twist=0.4 * i))
    # grass to bare rock, a wider ribbon on the same line: the smaller `scar` inside wins its own
    # cells, so what is left of this one is exactly the lip
    for pid, points in CREVASSES:
        ring, _src = ribbon(points, 13, phase=1.7)
        out.append(poly(f"sm-scar-{pid}", [list(clamp(x, z)) for x, z in ring], "seam-scar",
                        override=False, base_height=1))
    # sward to wood, along the downs' own northern edge
    for i, x in enumerate(range(-56, 57, 16)):
        out.append(blob(f"sm-holt-{i}", x, 80 + 3 * math.sin(x / 17.0), 12, 8, "seam-holt",
                        lobes=6, twist=0.3 * i))
    # the foot of the range, where the mountain runs out into the wood
    for i, x in enumerate(range(-50, 51, 14)):
        out.append(blob(f"sm-crag-{i}", x, 126 + 3 * math.cos(x / 13.0), 11, 8, "seam-crag",
                        lobes=6, twist=0.7 * i))
    return out


# ── the dressing ──────────────────────────────────────────────────────────────────────────────
# Five rules can refuse a prop and none of them is visible in a plan view: the coast (`DR-SITE`), the
# goal's clearance ring (`OB19`), the approach in front of a door (`DR-KEEP`), a route's claim on the
# cells it paves (`DR-CLAIM`), and the three-block margin either side of it (`DR-ROAD`). A tree also
# claims every cell its CANOPY reaches rather than its trunk cell. So the copses and the yards state
# where a thing belongs and a filter decides which of them are actually placed.
PAVE = cell(83, 4, [BRICK, GRANITE, POL_GRANITE, BRICK, GRANITE], jitter=100, warp=0)
# The spine starts outside the spawn's own footprint, and both shore branches are kept a dozen
# blocks off the crevasse ends — the ground beside one falls twelve courses, and a road drawn across
# that slope picks up the two-block risers a path is exactly the thing that must not have.
ROADS = ([[0, 113], [5, 104], [-6, 92], [4, 76], [-2, 60], [-10, 48], [-4, 40]],
         [[2, 78], [16, 73], [27, 71]],
         [[-8, 48], [-34, 44], [-54, 34], [-62, 16]],
         [[2, 48], [34, 44], [54, 34], [62, 16]])
YARDS = ((-26, 98, "@17h-croft", "posX"), (24, 96, "@17h-barn", "negX"),
         (-24, 56, "@17h-granary", "posX"), (46, 58, "@17h-coop", "negX"),
         (18, 112, "@17h-croft", "negX"), (-58, 46, "@17h-barn", "posX"),
         (-20, 118, "@17h-coop", "posZ"), (34, 108, "@17h-granary", "negX"))
COPSES = ((-42, 86, 12, 9), (-16, 96, 12, 9), (12, 88, 12, 9), (36, 98, 11, 8),
          (-30, 106, 11, 8), (26, 108, 11, 8), (-50, 96, 10, 8), (48, 88, 10, 8))


def seg_distance(px, pz, ax, az, bx, bz):
    dx, dz = bx - ax, bz - az
    length = dx * dx + dz * dz
    t = 0.0 if length == 0 else max(0.0, min(1.0, ((px - ax) * dx + (pz - az) * dz) / length))
    return math.hypot(px - (ax + t * dx), pz - (az + t * dz))


def road_distance(x, z):
    return min(seg_distance(x, z, *road[i], *road[i + 1])
               for road in ROADS for i in range(len(road) - 1))


def dressing():
    props, placed = [], []

    def free(x, z, gap, road_gap=7.0):
        if math.hypot(x - GOAL[0], z - GOAL[1]) < 16:
            return False
        if road_distance(x, z) < road_gap:
            return False
        return all(math.hypot(x - px, z - pz) >= gap for px, pz in placed)

    # The mere, drawn as a CLOSED RING rather than a line across the basin. A ring floods its own band
    # and leaves the ground inside it dry, which is the island — the same donut `showcase/13-pond`
    # reports as a mistake when the basin was meant to be a pond, and is the whole shape here.
    ring = [[int(round(x)), int(round(z))]
            for x, z in around(0, 0, WATER_RX, WATER_RZ, 12, 0.15, half=False)]
    ring.append(ring[0])
    props.append({"id": "ravensmere", "kind": "water", "points": ring, "radius": WATER_R,
                  "depth": 3, "form": "natural", "edge": 1.0, "shore": 1.4,
                  "shoreWander": True, "seed": 41})

    # The path: brick with granite and smooth granite through it, seven blocks across (`radius` 3
    # reaches three either side of the centreline). It is declared a route, which is what the
    # standoff every other prop is filtered against is measured to.
    for name, road in zip(("path-spine", "path-ward", "path-shore-w", "path-shore-e"), ROADS):
        props.append({"id": name, "kind": "stroke", "seed": 70 + len(props), "points": road,
                      "radius": 3, "style": "worn", "coverage": 0.95, "route": True, "pave": PAVE})

    # the buildings, scattered off the path rather than lined along it
    for i, (x, z, style, front) in enumerate(YARDS):
        if not free(x, z, 18.0, road_gap=11.0):
            continue
        placed.append((x, z))
        props.append({"id": f"house-{i}", "kind": "house", "seed": 100 + i,
                      "points": [[x - 4, z - 3], [x + 4, z + 3]], "front": front, "style": style})

    # the wood: oak and birch in copses, five stands to a copse and the density falling at the margin
    trees = 0
    for cx, cz, rx, rz in COPSES:
        for dx, dz, species, height in ((0, 0, "oak", 13), (-rx + 2, -rz + 3, "birch", 11),
                                        (rx - 2, -rz + 3, "oak", 12), (rx - 3, rz - 3, "birch", 10),
                                        (-rx + 3, rz - 3, "oak", 14), (0, -rz - 3, "birch", 9),
                                        (0, rz + 3, "oak", 12)):
            x, z = clamp_int(cx + dx, cz + dz)
            if not free(x, z, 8.0):
                continue
            placed.append((x, z))
            props.append({"id": f"t{trees}", "kind": "tree", "seed": 200 + trees, "x": x, "z": z,
                          "form": "template", "species": species, "height": height})
            trees += 1
    # a few standing alone on the downs, so the wood has an outrunner rather than a boundary
    for i, (x, z) in enumerate([(-52, 70), (-20, 56), (44, 66), (18, 74), (-40, 58)]):
        x, z = clamp_int(x, z)
        if not free(x, z, 9.0):
            continue
        placed.append((x, z))
        props.append({"id": f"lone-{i}", "kind": "tree", "seed": 230 + i, "x": x, "z": z,
                      "form": "template", "species": "oak", "height": 11})

    for i, (cx, cz, rx, rz) in enumerate(COPSES[:5]):
        props.append({"id": f"f{i}", "kind": "flora", "seed": 250 + i,
                      "points": [[cx - rx, cz - rz], [cx + rx, cz - rz],
                                 [cx + rx, cz + rz], [cx - rx, cz + rz]],
                      "spec": {"coverage": 0.45, "scale": 12, "octaves": 3, "fernShare": 0.4,
                               "flowerShare": 0.1, "flowerScale": 17, "tallShare": 0.12}})
    props.append({"id": "f-sward", "kind": "flora", "seed": 260,
                  "points": [[-58, 52], [58, 52], [58, 78], [-58, 78]],
                  "spec": {"coverage": 0.2, "scale": 20, "octaves": 2, "fernShare": 0.15,
                           "flowerShare": 0.25, "flowerScale": 22, "tallShare": 0.3}})

    # fallen rock: at the foot of the range, and spilled along every crevasse lip
    anchors = [(x, z + 4) for x, z in [tuple(p) for p in SPINE_W + SPINE_E]]
    anchors += [(p[0], p[1] + 9) for _pid, pts in CREVASSES for p in pts[::2]]
    anchors += [(p[0], p[1] - 9) for _pid, pts in CREVASSES for p in pts[1::2]]
    for i, (x, z) in enumerate(anchors):
        x, z = clamp_int(x, z)
        if not free(x, z, 10.0):
            continue
        placed.append((x, z))
        props.append({"id": f"b{i}", "kind": "boulder", "seed": 300 + i, "x": x, "z": z,
                      "form": ("angular", "round", "outcrop")[i % 3], "size": 2 + (i % 2),
                      "mossy": i % 3 == 1, "rock": ANDESITE})
    return {"props": props}


# ── assembly ──────────────────────────────────────────────────────────────────────────────────
def main():
    finish = {
        "authors": ["Opus 5"],
        "roomStyles": {"spawn": "@showcase-hall", "cage": "@showcase-cage"},
        "themes": THEMES,
        "mapTheme": "sward",
        # one compiled shape: six nested tiers resolve to a single open landmass
        "themeById": {"s0": "sward"},
        "shapePropsById": {"s0": outline()},
        "relief": {"team": {"base": Y_BASE, "reach": 0, "step": 1, "stairs": True,
                            "grain": {"amplitude": 1.0, "scale": 17, "seed": 7},
                            "marks": relief_marks(), "pushes": pushes()}},
        "addShapes": brush(),
        "dressing": dressing(),
    }
    out = os.path.join(HERE, f"{SLUG}.finish.json")
    with open(out, "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in finish["dressing"]["props"]:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"{out}: {len(finish['themes'])} themes · {len(finish['addShapes'])} strokes · "
          f"{len(finish['relief']['team']['marks'])} marks · "
          f"{len(finish['relief']['team']['pushes'])} pushes · props {kinds}")


if __name__ == "__main__":
    main()
