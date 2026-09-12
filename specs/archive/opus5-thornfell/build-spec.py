#!/usr/bin/env python3
"""Write the finish document for `opus5-thornfell`.

    python3 specs/opus5-thornfell/build-spec.py

A capture board rather than a destroy one: void down the middle, and two wool rooms hung off the back of
each half on spurs a raider has to walk out along. Three ranges — one behind the spawn and one behind each
wool — and the ground between them is fell.

The plan is authored by hand and is not written here. Output: `opus5-thornfell.finish.json`.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-thornfell"


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


# One hue axis, and a cold one: peat and heather against wet grey rock, with the pale scoured stone of
# the tops as the only light in it. Every block is claimed by a paint family — a block no family names
# reads as magenta on `render/surface` and says nothing about the ground it is on.
STONE, GRANITE, POL_GRANITE = solid(1), solid(1, 1), solid(1, 2)
DIORITE, POL_DIORITE, ANDESITE = solid(1, 3), solid(1, 4), solid(1, 5)
COBBLE, MOSSY, GRAVEL, STONE_BRICK = solid(4), solid(48), solid(13), solid(98)
GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
CLAY, HARD_CLAY = solid(82), solid(172)
BROWN_CLAY, GREEN_CLAY, GREY_CLAY, WHITE_CLAY = solid(159, 12), solid(159, 13), solid(159, 7), solid(159)
SAND, SANDSTONE = solid(12), solid(24)


def band(material, thickness):
    return {"material": material, "thickness": thickness}


def layered(bands, beyond=None, axis="depth"):
    return {"kind": "layered", "axis": axis, "beyond": beyond or STONE,
            "stack": {"ending": "handOver", "bands": bands}}


def cell(seed, size, palette, jitter=65, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": palette}


def theme(surface, wall, fill, rim=None, rim_edges="void", depth=3, rim_depth=1):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": rim_edges,
            "wallOnTerrainFaces": True,
            "rim": {"enabled": rim is not None, "depth": rim_depth, "material": rim or solid(4)},
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill}


# ── the themes ────────────────────────────────────────────────────────────────────────────────
THEMES = {
    # the moor — the ground most of the board is, peat under thin grass
    "moor": theme(
        layered([band(cell(11, 11, [GRASS, GRASS, COARSE, PODZOL, GRASS]), 1), band(DIRT, 2),
                 band(COARSE, 1)]),
        layered([band(GRASS, 1), band(DIRT, 3), band(COARSE, 2), band(ANDESITE, 3)]),
        STONE, rim=COARSE),
    # the drier back of it, where the peat is bare
    "heath": theme(
        layered([band(cell(13, 8, [PODZOL, COARSE, BROWN_CLAY, PODZOL, GRASS]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),
    # the fell above them: the same green with the rock coming through
    "fell": theme(
        layered([band(cell(17, 9, [GRASS, COARSE, ANDESITE, GRASS, STONE]), 1), band(DIRT, 2),
                 band(ANDESITE, 1)]),
        layered([band(GRASS, 1), band(DIRT, 2), band(ANDESITE, 3), band(STONE, 3)]),
        STONE, rim=COARSE),
    # wet ground at the head of the strait, where the water would stand
    "bog": theme(
        layered([band(cell(19, 6, [PODZOL, GRAVEL, CLAY, MOSSY, PODZOL]), 2)]),
        layered([band(PODZOL, 1), band(CLAY, 3), band(STONE, 3)]), STONE),

    # the rock — the three ranges, and the spurs' own bones
    "crag": theme(
        layered([band(cell(23, 7, [ANDESITE, STONE, GRANITE, ANDESITE, GRAVEL]), 1),
                 band(ANDESITE, 2), band(STONE, 2)]),
        layered([band(ANDESITE, 2), band(STONE, 4), band(GRANITE, 3), band(DIORITE, 2)]),
        STONE, rim=ANDESITE),
    "scree": theme(
        layered([band(cell(29, 4, [GRAVEL, COBBLE, ANDESITE, GRAVEL, STONE]), 2)]),
        layered([band(GRAVEL, 1), band(COBBLE, 3), band(STONE, 4)]), STONE),
    "summit": theme(
        layered([band(cell(31, 6, [POL_DIORITE, DIORITE, STONE, WHITE_CLAY]), 2), band(DIORITE, 2)]),
        layered([band(POL_DIORITE, 1), band(DIORITE, 3), band(ANDESITE, 4)]),
        STONE, rim=POL_DIORITE, depth=2),

    # the spurs the wools stand on: a shade apart, so a raider on one knows it
    "spur": theme(
        layered([band(cell(37, 7, [COARSE, GRAVEL, PODZOL, COARSE, ANDESITE]), 1), band(COARSE, 2),
                 band(ANDESITE, 1)]),
        layered([band(COARSE, 1), band(GRAVEL, 2), band(ANDESITE, 3), band(STONE, 4)]),
        STONE, rim=GRAVEL),

    # the shore at the strait: scoured stone where the ground gives out
    "strand": theme(
        layered([band(cell(41, 6, [GRAVEL, STONE, COBBLE, GRAVEL, ANDESITE]), 2)]),
        layered([band(GRAVEL, 2), band(STONE, 4), band(ANDESITE, 3)]),
        STONE, rim=STONE),

    # the wood on the moor
    "holt": theme(
        layered([band(cell(43, 10, [GRASS, PODZOL, GRASS, COARSE, GRASS]), 1), band(DIRT, 2),
                 band(COARSE, 1)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(COARSE, 2), band(ANDESITE, 3)]),
        STONE, rim=COARSE),
    "understorey": theme(
        layered([band(cell(47, 6, [PODZOL, BROWN_CLAY, COARSE, PODZOL]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),

    # ── the five seams ─────────────────────────────────────────────────────────────────────────
    "seam-heath": theme(
        layered([band(cell(53, 7, [GRASS, PODZOL, COARSE, GRASS, PODZOL]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),
    "seam-crag": theme(
        layered([band(cell(59, 6, [ANDESITE, GRASS, COARSE, STONE, GRASS]), 1), band(DIRT, 1),
                 band(ANDESITE, 2)]),
        layered([band(ANDESITE, 2), band(DIRT, 2), band(STONE, 4)]), STONE),
    "seam-holt": theme(
        layered([band(cell(61, 8, [GRASS, PODZOL, GRASS, PODZOL, COARSE]), 1), band(DIRT, 2)]),
        layered([band(PODZOL, 1), band(DIRT, 3), band(ANDESITE, 3)]), STONE),
    "seam-strand": theme(
        layered([band(cell(67, 6, [GRAVEL, GRASS, COARSE, STONE, GRASS]), 1), band(DIRT, 1),
                 band(GRAVEL, 2)]),
        layered([band(GRAVEL, 1), band(DIRT, 2), band(STONE, 4)]), STONE),
    "seam-spur": theme(
        layered([band(cell(71, 6, [COARSE, GRASS, GRAVEL, COARSE, PODZOL]), 1), band(DIRT, 2)]),
        layered([band(COARSE, 1), band(DIRT, 2), band(ANDESITE, 3)]), STONE),
}


# ── the frame ─────────────────────────────────────────────────────────────────────────────────
Y_BASE = 24                        # the board's ground, and the plan's own surface
Y_PAD = 26                         # the flats: the moor, the spurs, the aprons and the wool rooms
Y_SHORE = 20                       # the shelf at the head of the strait, four courses down

# The plan's own rectangles, in blocks. A capture board branches, so "how wide is the land here" is not
# a function of z: at z 100 there are three separate runs of it with void between them. Membership is
# tested against the rectangles themselves, which is exact and is the same statement the plan makes.
RECTS = ((-70, 15, 70, 45), (-75, 45, 75, 75), (-60, 75, 60, 95),
         (-95, 95, -50, 110), (-30, 95, 30, 110), (50, 95, 95, 110),
         (-95, 110, -55, 125), (-10, 110, 10, 125), (55, 110, 95, 125),
         (-40, 125, 40, 145), (-95, 125, -55, 145), (55, 125, 95, 145))
MARGIN = 7                         # how far inside the plan's own edge a brush stroke has to stay


def in_rects(x, z):
    return any(x0 <= x <= x1 and z0 <= z <= z1 for x0, z0, x1, z1 in RECTS)


def on_land(x, z, margin=MARGIN):
    """Inside the union of the plan's rectangles by `margin`, tested at the four compass offsets so a
    seam between two abutting rectangles is land and the outer edge of either is not. A one-course
    brush stroke on a cell no region shape covers is the only add on that column and builds a speck of
    bedrock standing over the void, which on a board with void in the middle of it is easy to do."""
    z = abs(z)
    return (in_rects(x, z) and in_rects(x + margin, z) and in_rects(x - margin, z)
            and in_rects(x, z + margin) and in_rects(x, z - margin))


def fold(cx, cz):
    """Author on the +z half and let the orbit fan the rest: a stroke drawn wholly on the mirrored half
    is outside the compiled ground's own polygon, and the canvas reads it as an island of its own."""
    return (-cx, -cz) if cz < 0 else (cx, cz)


def pull(cx, cz, x, z):
    """A vertex walked back toward its own centre until it is on land."""
    for t in (1.0, 0.8, 0.6, 0.4, 0.2):
        px, pz = cx + (x - cx) * t, cz + (z - cz) * t
        if on_land(px, pz):
            return round(px, 1), round(pz, 1)
    return round(cx, 1), round(cz, 1)


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
        verts.append(list(pull(cx, cz, x, z)) if clamped else [round(x, 1), round(z, 1)])
    return verts


def blob(pid, cx, cz, rx, rz, theme, lobes=7, twist=0.0):
    """A brush stroke: a small closed ring carrying a theme, added as an ordinary add one course thick.
    Paint scopes to the smallest shape covering a cell, so the stroke wins the colour; the column's
    height is decided by the taller add, so it can never lower what it is painted on."""
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


def around(cx, cz, rx, rz, count, phase=0.0, half=True):
    span = math.pi if half else 2 * math.pi
    return [(cx + rx * math.cos(span * i / count + phase),
             cz + rz * math.sin(span * i / count + phase)) for i in range(count)]


# ── the landforms ─────────────────────────────────────────────────────────────────────────────
# Constraints state the plan of the board — the shore at the strait, the flats a player walks, the
# ground a stamped building stands on. Pushes state its relief — the rolling fell and the three ranges.
# A mark is honoured exactly and has no falloff, so it can hold a plateau and can never be a mountain;
# a push lifts the solved surface inside a drawn ring and its `crown` is what makes a landform of it.
FLATS = (("moor", 0, 60, 72, 16, 15, 0.2),
         ("neck", 0, 86, 56, 11, 13, 1.1),
         ("apron", 0, 102, 28, 8, 11, 0.7),
         ("spurpad-w", -72, 102, 21, 7, 11, 1.5),
         ("spurpad-e", 72, 102, 21, 7, 11, 2.3))
FLAT_RINGS = {name: ring_of(cx, cz, rx, rz, lobes=lobes, twist=twist, clamped=False)
              for name, cx, cz, rx, rz, lobes, twist in FLATS}
ROOMS = ((-75, 117), (75, 117))     # the two wool rooms, and the ground each is stamped on

# Rolling, which is a statement about the gradient rather than about the height: a lift of 5 over a
# 12-block skirt is a knoll at one course every two blocks, and anything standing on it has five courses
# of relief across its own footprint. At 20 the same lift is one course every four.
HILL_FALLOFF = 20
HILLS = ((-56, 34, 12, 10, 6), (56, 34, 12, 10, 6), (-64, 62, 12, 10, 7),
         (64, 62, 12, 10, 7), (-30, 44, 11, 9, 5), (30, 44, 11, 9, 5),
         (-46, 84, 11, 9, 5), (46, 84, 11, 9, 5))
# Three ranges: one behind the spawn, and one behind each wool room. The two behind the wools are what
# makes a spur read as a headland rather than as a shelf — the ground it hangs off ends in rock.
# Two numbers decide whether a range reads as a mountainside or as a wall, and neither is its height.
# The first is where its skirt ends: a push is applied after every constraint, so a range whose skirt
# crosses a wool room lifts the pad the room is stamped on and leaves the room standing on a plinth of
# its own foundation. Each spine is set back far enough that its ring plus skirt stops at the edge of
# the piece in front of it — z 125 for the spawn and for both wool rooms.
# The second is the gradient, which is `amount / falloff` on the skirt and `crown / half` inside the
# ring, and a range is a wall wherever those two disagree. Both are ~1.7 courses a block here, so the
# climb is one slope from the foot to the board's back edge; the medial axis is past that edge, which
# is what makes the summit read as being behind the map rather than on it.
SPINE_S = [[-32, 144], [-14, 148], [10, 145], [32, 148]]
LIFT_S = [13, 17, 14, 16]
SPINE_W = [[-88, 144], [-75, 148], [-62, 144]]
LIFT_W = [14, 17, 14]
SPINE_E = [[62, 144], [75, 148], [88, 144]]
LIFT_E = [14, 17, 14]
RANGES = (("range-s", SPINE_S, LIFT_S, 7, 10, 3), ("range-w", SPINE_W, LIFT_W, 6, 10, 11),
          ("range-e", SPINE_E, LIFT_E, 6, 10, 15))
# The crests, taken on the board rather than off the back of it: the spine's own summits are past the
# coast, and a stroke centred past it has nothing to clamp to and collapses onto its own centre.
SUMMITS = (((-14, 138), 0), ((32, 138), 1), ((-75, 138), 2), ((75, 138), 3))


def relief_marks():
    """Written in the order they resolve: the rim first, so nothing cuts a doorway through the coast,
    then the shelf at the strait, then the flats a player walks, then the two the wool rooms stand on —
    a mark that has to win its cells is written after whatever else wants them."""
    marks = [{"id": "coast", "kind": "rim", "h": Y_BASE, "depth": 1},
             # the head of the strait, four courses under the moor: the ground falls to the void rather
             # than ending at it, which is what makes the crossing read as a crossing
             {"id": "shore", "kind": "line",
              "points": [[-64, 19], [-24, 22], [24, 22], [64, 19]],
              "h": [Y_SHORE, Y_SHORE + 1, Y_SHORE + 1, Y_SHORE], "r": 9},
             *[{"id": name, "kind": "area", "h": Y_PAD, "ring": FLAT_RINGS[name]}
               for name, *_rest in FLATS],
             {"id": "spawnpad", "kind": "area", "h": Y_PAD,
              "ring": ring_of(0, 117, 10, 8, lobes=9, twist=0.3, clamped=False)}]
    for i, (x, z) in enumerate(ROOMS):
        # the room and both ledges beside it, so the ground the room is stamped on runs out to the
        # coast either side of it and the room stands in the land rather than on a pedestal of it
        marks.append({"id": f"roompad-{i}", "kind": "area", "h": Y_PAD,
                      "ring": ring_of(x, z, 22, 10, lobes=9, twist=0.6 * i, clamped=False)})
    for i, (x, z, _style, _front) in enumerate(YARDS):
        marks.append({"id": f"yard-{i}", "kind": "area", "h": Y_PAD,
                      "ring": ring_of(x, z, 11, 9, lobes=9, twist=0.4 * i, clamped=False)})
    return marks


def pushes():
    out = []
    for i, (x, z, rx, rz, amount) in enumerate(HILLS):
        out.append({"id": f"hill-{i}", "ring": ring_of(x, z, rx, rz, lobes=8, twist=0.6 * i,
                                                       clamped=False),
                    "amount": amount, "falloff": HILL_FALLOFF, "roughness": 0.55,
                    "crown": 3 + (i % 2), "seed": 31 + i})
    for pid, spine, lift, half, falloff, seed in RANGES:
        ring, src = ribbon(spine, half, phase=seed * 0.4)
        out.append({"id": pid, "ring": ring, "amount": max(lift),
                    "amounts": [lift[i] for i in src],
                    "falloff": falloff, "roughness": 0.38, "crown": 12, "seed": seed})
    return out


# ── the brush ─────────────────────────────────────────────────────────────────────────────────
# Two passes. The first paints the grounds at region scale; the second answers *why here* for every
# patch inside them and strings the seam themes along every boundary. Paint scopes to the SMALLEST
# shape covering a cell, so a later, smaller stroke always wins.
COPSES = ((-34, 62, 13, 10), (34, 62, 13, 10), (-14, 76, 12, 9),
          (14, 76, 12, 9), (-52, 52, 11, 9), (52, 52, 11, 9))


def brush():
    out = []
    # ── the grounds ────────────────────────────────────────────────────────────────────────────
    out.append(blob("rg-moor", 0, 60, 74, 20, "moor", lobes=15, twist=0.3))
    out.append(blob("rg-heath", 0, 88, 58, 14, "heath", lobes=15, twist=1.2))
    out.append(blob("rg-strand", 0, 22, 66, 12, "strand", lobes=13, twist=0.8))
    for i, (x, z) in enumerate(ROOMS):
        out.append(blob(f"rg-spur-{i}", x, 104, 22, 18, "spur", lobes=11, twist=0.5 + i))
    for pid, spine, _lift, half, _falloff, seed in RANGES:
        ring, _src = ribbon(spine, half + 5, phase=seed * 0.4)
        heart = fold(spine[len(spine) // 2][0], spine[len(spine) // 2][1] - 10)
        out.append(poly(f"rg-crag-{pid}", [list(pull(*heart, x, z)) for x, z in ring],
                        "crag", override=False, base_height=1))
    # the wood, sitting on the moor rather than replacing it
    for i, (x, z, rx, rz) in enumerate(COPSES):
        out.append(blob(f"rg-holt-{i}", x, z, rx + 4, rz + 3, "holt", lobes=9, twist=0.4 * i))

    # ── inside each ground ─────────────────────────────────────────────────────────────────────
    for i, (x, z, rx, rz) in enumerate(COPSES):
        out.append(blob(f"br-under-{i}", x, z, rx - 2, rz - 2, "understorey", twist=0.35 * i))
    # the fell: where the rock begins to show through the moor, on the shoulders under each range
    for i, (x, z) in enumerate([(-60, 105), (60, 105), (-20, 100), (20, 100), (0, 90)]):
        out.append(blob(f"br-fell-{i}", x, z, 14, 9, "fell", twist=0.5 * i))
    # scree spilling off every range
    for i, (spine, index) in enumerate([(SPINE_S, 0), (SPINE_S, 3), (SPINE_W, 0), (SPINE_W, 2),
                                        (SPINE_E, 0), (SPINE_E, 2)]):
        out.append(blob(f"br-scree-{i}", spine[index][0], spine[index][1] - 9, 11, 7, "scree",
                        lobes=6, twist=0.6 * i))
    # a scoured crest on every summit
    for i, (point, _n) in enumerate(SUMMITS):
        out.append(blob(f"br-summit-{i}", point[0], point[1], 8, 7, "summit", twist=0.4 * i))
    # wet ground at the head of the strait, where the fall to the void collects what runs off the moor
    for i, x in enumerate(range(-56, 57, 22)):
        out.append(blob(f"br-bog-{i}", x, 26 + 3 * math.sin(x / 19.0), 12, 7, "bog",
                        lobes=6, twist=0.4 * i))

    # ── the five seams ─────────────────────────────────────────────────────────────────────────
    # moor to heath, along the back of the moor
    for i, x in enumerate(range(-56, 57, 16)):
        out.append(blob(f"sm-heath-{i}", x, 78 + 3 * math.cos(x / 17.0), 12, 8, "seam-heath",
                        lobes=6, twist=0.3 * i))
    # moor to shore, along the front of it
    for i, x in enumerate(range(-60, 61, 17)):
        out.append(blob(f"sm-strand-{i}", x, 36 + 3 * math.sin(x / 21.0), 12, 8, "seam-strand",
                        lobes=6, twist=0.5 * i))
    # the foot of every range
    for pid, spine, _lift, _half, _falloff, seed in RANGES:
        for i, (x, z) in enumerate(spine):
            out.append(blob(f"sm-crag-{pid}-{i}", x, z - 12, 12, 8, "seam-crag",
                            lobes=6, twist=0.4 * i + seed))
    # where the neck gives out onto each spur — the one seam a raider crosses on purpose
    for i, (x, z) in enumerate([(-58, 102), (58, 102), (-62, 105), (62, 105)]):
        out.append(blob(f"sm-spur-{i}", x, z, 11, 8, "seam-spur", lobes=6, twist=0.7 * i))
    # sward to wood, round every copse
    for i, (x, z, rx, rz) in enumerate(COPSES):
        out.append(blob(f"sm-holt-{i}", x, z + rz + 4, rx, 7, "seam-holt", lobes=6, twist=0.6 * i))
    return out


# ── the dressing ──────────────────────────────────────────────────────────────────────────────
# Five rules can refuse a prop and none is visible in a plan view: the coast (`DR-SITE`), a wool room's
# own keep-out and the lane in front of its door (`DR-KEEP`), a route's claim (`DR-CLAIM`), the margin
# either side of it (`DR-ROAD`), and — for a building — a site with more relief across its footprint
# than the building itself stands (`DR-SLOPE`). So the copses and the yards state where a thing belongs
# and a filter decides which of them are actually placed.
PAVE = cell(83, 4, [COBBLE, ANDESITE, GRAVEL, COBBLE, STONE], jitter=100, warp=0)
# A track out of the spawn that forks to each wool room, and one down to each ford. Five blocks across
# rather than seven: this is a way worn over a fell, not a street.
# Every track starts outside the spawn's own footprint. One drawn from inside it reads its first cells
# off the building's roof, which is a ten-block step in a transect and no step at all on the ground.
ROADS = ([[0, 108], [-16, 103], [-40, 102], [-64, 106]],
         [[0, 108], [16, 103], [40, 102], [64, 106]],
         [[0, 106], [-6, 88], [-24, 70], [-40, 50], [-44, 30]],
         [[0, 106], [6, 88], [24, 70], [40, 50], [44, 30]])
FOOT = (5, 4)
STYLES = ("@17h-granary", "@17h-barn", "@17h-croft")


def seg_distance(px, pz, ax, az, bx, bz):
    dx, dz = bx - ax, bz - az
    length = dx * dx + dz * dz
    t = 0.0 if length == 0 else max(0.0, min(1.0, ((px - ax) * dx + (pz - az) * dz) / length))
    return math.hypot(px - (ax + t * dx), pz - (az + t * dz))


def road_distance(x, z):
    return min(seg_distance(x, z, *road[i], *road[i + 1])
               for road in ROADS for i in range(len(road) - 1))


def inside(ring, x, z):
    hit, n = False, len(ring)
    for i in range(n):
        (x1, z1), (x2, z2) = ring[i], ring[(i + 1) % n]
        if (z1 > z) != (z2 > z) and x < x1 + (z - z1) * (x2 - x1) / (z2 - z1):
            hit = not hit
    return hit


def skirts():
    """Every push as a centre and how far a building has to stay from it — which is not the same as how
    far the push reaches. A mark cannot hold ground level underneath a push, because a push is applied
    after every constraint; what decides whether a building can stand is the gradient where it stands.
    Inside a ring the ground is domed toward the medial axis and steep, so a building keeps out of the
    ring itself; on a skirt of 20 the gradient is a course every four blocks, two across a footprint,
    and a building may stand on that. A massif's flank is steep on any reading and is kept out whole."""
    out = [(x, z, max(rx, rz) + 4) for x, z, rx, rz, _amount in HILLS]
    out += [(x, z, half + 12) for _pid, spine, _lift, half, _f, _seed in RANGES for x, z in spine]
    return out


def yards(count=3, spacing=26):
    """Where a building may stand, searched rather than typed. A building seats on the LOWEST column of
    its footprint and the terrain over that floor is carved out of it, so what it needs is a plateau —
    which on this board is ground an `area` mark pins level that no push reaches. Both halves are read
    off the same geometry the relief is written from, so the answer cannot drift from the terrain."""
    marked = []
    for x in range(-70, 71, 2):
        for z in range(20, 112, 2):
            ring = next((r for r in FLAT_RINGS.values()
                         if all(inside(r, x + dx, z + dz)
                                for dx in (-FOOT[0], FOOT[0]) for dz in (-FOOT[1], FOOT[1]))), None)
            if ring is None or not on_land(x, z, MARGIN + 4):
                continue
            clear = min(math.hypot(x - sx, z - sz) - reach for sx, sz, reach in skirts())
            if clear < 7 or road_distance(x, z) < 12:
                continue
            marked.append((clear, x, z))
    marked.sort(reverse=True)
    taken = []
    for _clear, x, z in marked:
        if any(math.hypot(x - px, z - pz) < spacing for px, pz in taken):
            continue
        taken.append((x, z))
        if len(taken) == count:
            break
    out = []
    for i, (x, z) in enumerate(sorted(taken, key=lambda p: (-p[1], p[0]))):
        near = min(((seg_distance(x, z, *road[j], *road[j + 1]), road[j], road[j + 1])
                    for road in ROADS for j in range(len(road) - 1)), key=lambda e: e[0])
        toward = ((near[1][0] + near[2][0]) / 2 - x, (near[1][1] + near[2][1]) / 2 - z)
        front = ("posX" if toward[0] > 0 else "negX") if abs(toward[0]) >= abs(toward[1]) \
            else ("posZ" if toward[1] > 0 else "negZ")
        out.append((x, z, STYLES[i % len(STYLES)], front))
    return out


YARDS = yards()


def dressing():
    props, placed = [], []

    def free(x, z, gap, road_gap=7.0):
        if not on_land(x, z, MARGIN):
            return False
        if any(math.hypot(x - rx, z - rz) < 24 for rx, rz in ROOMS):
            return False                    # a wool room's own ground, and the lane out of its door
        if road_distance(x, z) < road_gap:
            return False
        return all(math.hypot(x - px, z - pz) >= gap for px, pz in placed)

    # the tracks: cobble and andesite over gravel, five blocks across, declared routes so the standoff
    # every other prop is filtered against is measured to them
    for name, road in zip(("track-wool-w", "track-wool-e", "track-ford-w", "track-ford-e"), ROADS):
        props.append({"id": name, "kind": "stroke", "seed": 70 + len(props), "points": road,
                      "radius": 2, "style": "worn", "coverage": 0.9, "claimsGround": True, "pave": PAVE})

    for i, (x, z, style, front) in enumerate(YARDS):
        placed.append((x, z))
        props.append({"id": f"steading-{i}", "kind": "house", "seed": 100 + i,
                      "points": [[x - 4, z - 3], [x + 4, z + 3]], "front": front, "style": style})

    # the wood: rowan and birch in copses, thin at the margin so it has an edge rather than a boundary
    trees = 0
    for cx, cz, rx, rz in COPSES:
        for dx, dz, species, height in ((0, 0, "oak", 12), (-rx + 2, -rz + 3, "birch", 10),
                                        (rx - 2, -rz + 3, "oak", 11), (rx - 3, rz - 3, "birch", 9),
                                        (-rx + 3, rz - 3, "oak", 13), (0, -rz - 3, "birch", 8),
                                        (0, rz + 3, "oak", 11)):
            x, z = int(round(cx + dx)), int(round(cz + dz))
            if not free(x, z, 8.0):
                continue
            placed.append((x, z))
            props.append({"id": f"t{trees}", "kind": "tree", "seed": 200 + trees, "x": x, "z": z,
                          "form": "template", "species": species, "height": height})
            trees += 1
    for i, (cx, cz, rx, rz) in enumerate(COPSES[:4]):
        props.append({"id": f"f{i}", "kind": "flora", "seed": 250 + i,
                      "points": [[cx - rx, cz - rz], [cx + rx, cz - rz],
                                 [cx + rx, cz + rz], [cx - rx, cz + rz]],
                      "spec": {"coverage": 0.4, "scale": 12, "octaves": 3, "fernShare": 0.45,
                               "flowerShare": 0.08, "flowerScale": 17, "tallShare": 0.15}})
    props.append({"id": "f-moor", "kind": "flora", "seed": 260,
                  "points": [[-60, 40], [60, 40], [60, 78], [-60, 78]],
                  "spec": {"coverage": 0.22, "scale": 22, "octaves": 2, "fernShare": 0.35,
                           "flowerShare": 0.12, "flowerScale": 24, "tallShare": 0.3}})

    # fallen rock at the foot of every range, and along the lip of the strait
    anchors = [(x, z - 13) for _pid, spine, _lift, _half, _f, _seed in RANGES for x, z in spine]
    anchors += [(x, 28) for x in range(-58, 59, 20)]
    for i, (x, z) in enumerate(anchors):
        x, z = int(round(x)), int(round(z))
        if not free(x, z, 11.0):
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
        "mapTheme": "moor",
        "themeById": {"s0": "moor"},
        # The compiled outline drawn as a coast rather than restated by hand: the plan's own vertices
        # stay where they are and only the points inserted between them move, and only inward — a
        # point moved outward could close the strait this board is measured on.
        "bendShapes": {"s0": {"k": 0.22, "wander": 3.0, "step": 9, "seed": 5}},
        "relief": {"team": {"base": Y_BASE, "reach": 0, "step": 1, "stairs": True,
                            "grain": {"amplitude": 1.2, "scale": 17, "seed": 7},
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
          f"{len(finish['relief']['team']['pushes'])} pushes · yards {len(YARDS)} · props {kinds}")


if __name__ == "__main__":
    main()
