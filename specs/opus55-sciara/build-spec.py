"""Sciara — two hill villages on the flank of a volcano, each defending a core on its threshing floor.

Writes `opus55-sciara.plan.json` and `opus55-sciara.refinement.json`. Every coordinate is red's unit, on the
z < 0 half; the rot_180 symmetry fans the plan and the `team` group to blue. Front is +z, toward the ravine.

The hillside is terraced. Every terrace is a polygon whose front and back edges are contours shared with the
terraces in front of and behind it, so the rows stack against each other with no ground between them. Each
terrace is a plane tilted a block or so by its vertex heights, and a terrace stands two or three blocks over
the one in front. Its front edge carries a crumbled lava-stone parapet one block over its own ground, drawn as
a polyline whose vertex heights follow the terrace's tilt. Every face a path crosses has a flight set into a
notch cut in the upper terrace.

Heights a player stands on, red's half:
  upper village (behind)        37
  lower village, rear lane      35
  piazza and the spawn's yard   34
  the aia                       31, the threshing floor on it 32 inside a kerb at 33
  grove terraces, back to front 32–33 · 30–31 · 27–28 · 24–25
  the open slope                27 → 22, relief, pinned at the aia's front and at the ravine lip
  the sciara                    a push down the east flank; a smaller lobe on the west
  the cava                      a quarry pit at the aia's foot, its floor 23, opening into a tunnel under it
"""
import json, os, random

SLUG = "opus55-sciara"
HERE = os.path.dirname(os.path.abspath(__file__))


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data} if data else {"kind": "solid", "id": block}


GRASS, DIRT, STONE, COBBLE = 2, 3, 1, 4
CLAY, HARD_CLAY, COAL_BLOCK, BRICK = 159, 172, 173, 45
PLANKS, LOG, FENCE, QUARTZ, WOOL, SLAB = 5, 17, 85, 155, 35, 44

# --- materials -------------------------------------------------------------------------------------------

def over_dirt(top):
    """One course of `top` over two of dirt, read down from the surface."""
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": solid(DIRT), "thickness": 2}]}}


LAVA_ROCK = {"kind": "cell", "seed": 11, "cellSize": 2, "jitter": 1, "warp": 1,
             "palette": [solid(CLAY, 15), solid(CLAY, 15), solid(CLAY, 7), solid(COAL_BLOCK)], "rise": 2}

MATERIALS = {
    # the lava stone: black and grey stained clay with coal block as its grain — the rock the whole
    # mountain is made of, so it is the wall, the fill, the steepest band of every theme and every parapet
    "lava-rock": LAVA_ROCK,
    "worn": {"kind": "cell", "seed": 5, "cellSize": 2, "jitter": 1, "warp": 1,
             "palette": [solid(DIRT), solid(DIRT, 1)]},
    # the sciara's own top: the lava stone as ground, grey clay patches at one end, coal at the other.
    # A named material is stated inline where another named material holds it: the store keeps a `use`
    # nested inside `materials` unresolved, and every read of the board then refuses it.
    "sciara-top": {"kind": "noise", "seed": 23, "scale": 3, "octaves": 2, "stops": [
        solid(CLAY, 7), LAVA_ROCK, LAVA_ROCK, solid(COAL_BLOCK)]},
    # the village floor: granite, polished granite, hardened clay and brick, a quarter each
    "paving": {"kind": "cell", "seed": 3, "cellSize": 3, "jitter": 1, "warp": 1,
               "palette": [solid(STONE, 1), solid(STONE, 2), solid(HARD_CLAY), solid(BRICK)]},
    # the dry-stone walls along the terrace fronts: cobblestone with andesite, a pale course laid on the
    # dark lava face under it
    "drystone": {"kind": "cell", "seed": 29, "cellSize": 2, "jitter": 1, "warp": 0, "rise": 1,
                 "palette": [solid(COBBLE), solid(COBBLE), solid(STONE, 5)]},
    # a made face: the lava stone up to the lip's height, dry stone above it — so a terrace's retaining walls
    # are cobbled and the cliff under it, where the ground meets the void, is the mountain's own rock
    "terrace-face": {"kind": "layered", "axis": "height", "from": 0, "stack": {"ending": "repeat", "bands": [
        {"material": LAVA_ROCK, "thickness": 23},
        {"material": {"kind": "cell", "seed": 29, "cellSize": 2, "jitter": 1, "warp": 0, "rise": 1,
                      "palette": [solid(COBBLE), solid(COBBLE), solid(STONE, 5)]}, "thickness": 1}]}},
    # a farm track: dirt, coarse dirt and spruce planks a third each
    "track": {"kind": "cell", "seed": 17, "cellSize": 1, "jitter": 0, "warp": 0,
              "palette": [solid(DIRT), solid(DIRT, 1), solid(PLANKS, 1)]},
}


def theme(surface, surface_depth=1, rim_top=None, wall="lava-rock"):
    """A theme whose wall, fill and steepest ground are the lava stone. Where `rim_top` is stated the rim
    caps every edge with it one course deep, so a terrace face is lava stone up to its top course rather
    than the surface's soil."""
    rim = ({"material": rim_top, "depth": 1} if rim_top
           else {"material": {"use": "lava-rock"}, "enabled": False})
    return {"rim": rim,
            "surface": {"material": surface, "depth": surface_depth},
            "wall": {"use": wall},
            "fill": {"use": "lava-rock"}}


SLOPE_STACK = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": over_dirt(solid(GRASS)), "thickness": 34},
    {"material": over_dirt({"use": "worn"}), "thickness": 14},
    {"material": {"use": "lava-rock"}, "thickness": 42}]}}

THEMES = {
    # the countryside: savanna grass, worn earth where it leans, lava stone where it stands up
    "campagna": theme({"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
        {"material": over_dirt(solid(GRASS)), "thickness": 34},
        {"material": over_dirt({"use": "worn"}), "thickness": 14},
        {"material": {"use": "lava-rock"}, "thickness": 42}]}}, 3, solid(GRASS)),
    # made ground: the same grass, its faces the cobbled walls that hold it up
    "terrazza": theme(SLOPE_STACK, 3, solid(GRASS), "terrace-face"),
    "sciara": theme({"use": "sciara-top"}, 2),
    "borgo": theme({"use": "paving"}, 2, {"use": "paving"}, "drystone"),
}

# --- the plan --------------------------------------------------------------------------------------------

PLAN = {
    "plan": 2,
    "meta": {"name": "Sciara"},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 20, "surface": 22,
                # over the build ceiling, so the platform is no stepping stone in the ravine
                "observerY": 64},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-5, -32, 6, 5], "surface": 34},
        {"id": "village-w", "rect": [-12, -37, 7, 13], "surface": 34},
        {"id": "village-e", "rect": [1, -37, 11, 13], "surface": 34},
        {"id": "village-front", "rect": [-5, -27, 6, 3], "surface": 34},
        {"id": "village-rear", "rect": [-5, -37, 6, 5], "surface": 34},
        {"id": "flank", "rect": [-12, -24, 24, 21], "surface": 22},
    ],
    "zones": [{"id": "ravine", "rect": [-12, -3, 24, 3]}],
    "placements": {
        # the hall and its marker as POST /plan/room answers them for a 16 × 12 building
        "spawns": [{"id": "spawn-0", "piece": "spawn", "at": [12, 10], "facing": "back",
                    "footprint": [4, 4, 16, 12]}],
        "cores": [{"id": "core-0", "piece": "", "at": [10, -68], "name": "Aia Core"}],
    },
}

# --- shapes ------------------------------------------------------------------------------------------------

LIP, SLOPE_TOP, AIA, FLOOR, KERB = 22, 27, 31, 32, 33
PIAZZA, LOWER, UPPER = 34, 35, 37


def made(shape_id, vertices, height, theme_id="terrazza", anchors=None):
    """Made ground: out of the relief, meeting it at a face. `anchors` tilts it, one height a vertex."""
    shape = {"id": shape_id, "type": "polygon", "operation": "add", "relief_scope": "exclude",
             "theme": theme_id, "vertices": [[round(x, 2), round(z, 2)] for x, z in vertices]}
    if anchors:
        shape["anchor_heights"] = [round(h, 2) for h in anchors]
        shape["base_height"] = round(max(anchors))
    else:
        shape["base_height"] = height
    return shape


def flight(shape_id, x0, x1, z_foot, z_head, low, high):
    """A stair from ground standing at `low` to ground standing at `high`, foot edge at `z_foot` and head
    edge at `z_head`, at least two blocks of run a course. Anchors sit half a riser past the first and last
    tread so every tread comes out the same depth."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "height_mode": "level", "skirt": 0,
            "keepClear": True, "material": solid(STONE, 6),  # polished andesite treads
            "vertices": [[x0, z_foot], [x1, z_foot], [x1, z_head], [x0, z_head]],
            "anchor_heights": [low + 0.5, low + 0.5, high + 0.5, high + 0.5]}


def flight_x(shape_id, z0, z1, x_foot, x_head, low, high):
    """The same flight running east or west: foot edge at `x_foot`, head edge at `x_head`."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "height_mode": "level", "skirt": 0,
            "keepClear": True, "material": solid(STONE, 6),
            "vertices": [[x_foot, z0], [x_foot, z1], [x_head, z1], [x_head, z0]],
            "anchor_heights": [low + 0.5, low + 0.5, high + 0.5, high + 0.5]}


def z_on(contour, x):
    """The contour's z at x, read along its straight pieces."""
    for (xa, za), (xb, zb) in zip(contour, contour[1:]):
        if min(xa, xb) <= x <= max(xa, xb):
            return za + (zb - za) * (x - xa) / (xb - xa) if xb != xa else za
    return contour[0][1] if x < contour[0][0] else contour[-1][1]


def along(contour, x0, x1):
    """The contour from x0 to x1, its own points between them and both ends."""
    lo, hi = min(x0, x1), max(x0, x1)
    points = [(lo, z_on(contour, lo))] + [(x, z) for x, z in contour if lo < x < hi] + [(hi, z_on(contour, hi))]
    return points if x0 < x1 else list(reversed(points))


def flatten(contour, x0, x1):
    """The contour with a level piece from x0 to x1, so a flight can cross it square."""
    zc = z_on(contour, (x0 + x1) / 2)
    kept = [(x, z) for x, z in contour if not (x0 - 1 <= x <= x1 + 1)]
    return sorted(kept + [(x0, zc), (x1, zc)])


class Plane:
    """A terrace's ground: `base` at (`x`, `z`), falling `gx` a block eastward and `gz` a block frontward."""

    def __init__(self, base, x, z, gx=0.0, gz=0.0):
        self.base, self.x, self.z, self.gx, self.gz = base, x, z, gx, gz

    def at(self, x, z):
        return self.base + self.gx * (x - self.x) + self.gz * (z - self.z)


rng = random.Random(7)
SHAPES, WALLS = [], []


def offset(points, depth):
    """A line moved `depth` blocks into the terrace along each point's own inward normal — the terrace is on
    the -z hand of an edge running east."""
    out = []
    for i, (x, z) in enumerate(points):
        xa, za = points[max(0, i - 1)]
        xb, zb = points[min(len(points) - 1, i + 1)]
        dx, dz = xb - xa, zb - za
        length = (dx * dx + dz * dz) ** 0.5 or 1.0
        out.append((x + depth * dz / length, z - depth * dx / length))
    return out


def parapet(wall_id, points, plane, gaps, trim=2.0):
    """A dry-stone wall one course over a terrace along its front edge, as a strip of polygon between two
    lines set 0.15 and 1.6 blocks in from the edge — a polygon rather than a line with a width, so no
    column outside the terrace is ever part of it and the lava face under it stays the face. Its vertex
    heights are the terrace's own plus one, so it follows the tilt. It stops short of the terrace's corners
    and of every flight, and is broken into runs of eight to sixteen blocks with a block missing between a
    few of them, which is the crumbling."""
    x_start, x_end = points[0][0], points[-1][0]
    dense = []
    for (xa, za), (xb, zb) in zip(points, points[1:]):
        steps = max(1, int(abs(xb - xa) // 2))
        dense += [(xa + (xb - xa) * i / steps, za + (zb - za) * i / steps) for i in range(steps)]
    dense.append(points[-1])
    runs, run = [], []
    for x, z in dense:
        if x < x_start + trim or x > x_end - trim or any(a - 2.5 <= x <= b + 2.5 for a, b in gaps):
            if len(run) > 1:
                runs.append(run)
            run = []
            continue
        run.append((x, z))
    if len(run) > 1:
        runs.append(run)
    pieces = []
    for points_run in runs:
        i = 0
        while i < len(points_run) - 1:
            length = rng.randint(4, 8)
            piece = points_run[i:i + length + 1]
            if len(piece) > 1:
                pieces.append(piece)
            i += length + (1 if rng.random() < 0.25 else 0)
    for n, piece in enumerate(pieces):
        ring = offset(piece, 0.15) + list(reversed(offset(piece, 1.6)))
        anchors = [plane.at(x, z) + 1 for x, z in ring]
        WALLS.append({"id": f"{wall_id}-{n}", "type": "polygon", "operation": "add",
                      "relief_scope": "exclude", "material": {"use": "drystone"}, "keepClear": True,
                      "vertices": [[round(x, 2), round(z, 2)] for x, z in ring],
                      "anchor_heights": [round(h, 2) for h in anchors],
                      "base_height": round(max(anchors))})


# The contours the grove's rows are cut along, west to east. C0 is the front of the lowest row.
WEST, EAST = -48, -6
C0 = [(-36, -20), (-28, -22), (-20, -19), (-12, -21), (EAST, -20)]
C1 = [(-36, -35), (-29, -33), (-21, -37), (-13, -34), (EAST, -36)]
C2 = [(WEST, -52), (-38, -50), (-27, -54), (-17, -51), (EAST, -53)]
C3 = [(WEST, -70), (-37, -67), (-26, -71), (-15, -68), (EAST, -70)]
C4 = [(WEST, -90), (-36, -88), (-26, -91), (-15, -89), (EAST, -90)]

# Where a flight crosses each contour: (x0, x1).
CROSS = {"C0": [(-17, -13)], "C1": [(-31, -27), (-11, -7)], "C2": [(-25, -21)],
         "C3": [(-38, -34)], "C4": [(-40, -36)]}
C0, C1, C2, C3, C4 = (flatten(c, *span) if span else c for c, span in
                      ((C0, CROSS["C0"][0]), (C1, None), (C2, CROSS["C2"][0]), (C3, CROSS["C3"][0]),
                       (C4, CROSS["C4"][0])))
for span in CROSS["C1"]:
    C1 = flatten(C1, *span)

# The rows: each cell is (id, plane, x at its front edge west, east, x at its back edge west, east).
ROWS = [
    ("row-a", C0, C1, [("a1", Plane(24, -28, -28, gx=0.04, gz=0.02), -36, -22, -36, -24),
                       ("a2", Plane(25, -14, -28, gx=0.03, gz=0.02), -22, EAST, -24, EAST)]),
    ("row-b", C1, C2, [("b1", Plane(27, -32, -44, gx=0.05), -36, -20, -36, -18),
                       ("b2", Plane(28, -12, -44, gx=-0.06, gz=0.02), -20, EAST, -18, EAST)]),
    ("row-c", C2, C3, [("c1", Plane(30, -38, -60, gx=0.05, gz=0.02), WEST, -29, WEST, -31),
                       ("c2", Plane(30, -21, -60, gz=0.02), -29, -14, -31, -15),
                       ("c3", Plane(31, -10, -60), -14, EAST, -15, EAST)]),
    ("row-d", C3, C4, [("d1", Plane(33, -38, -80, gx=-0.03), WEST, -25, WEST, -27),
                       ("d2", Plane(32, -16, -80, gx=0.02), -25, EAST, -27, EAST)]),
]
PLANES = {cell: plane for _, _, _, cells in ROWS for cell, plane, *_ in cells}


def level_of(plane_or_height, x, z):
    return round(plane_or_height.at(x, z)) if isinstance(plane_or_height, Plane) else plane_or_height


# the flights up the grove's faces: (id, contour, span, the ground at the foot, the terrace at the head)
NOTCH = {}   # (contour label, x0) -> how far the flight reaches into the terrace above
for fid, label, contour, (x0, x1), low, high in [
        ("stair-lip", "C0", C0, CROSS["C0"][0], LIP, PLANES["a2"]),
        ("stair-a1b1", "C1", C1, CROSS["C1"][0], PLANES["a1"], PLANES["b1"]),
        ("stair-a2b2", "C1", C1, CROSS["C1"][1], PLANES["a2"], PLANES["b2"]),
        ("stair-b1c2", "C2", C2, CROSS["C2"][0], PLANES["b1"], PLANES["c2"]),
        ("stair-c1d1", "C3", C3, CROSS["C3"][0], PLANES["c1"], PLANES["d1"])]:
    zc = z_on(contour, (x0 + x1) / 2)
    lo, hi = level_of(low, (x0 + x1) / 2, zc + 1), level_of(high, (x0 + x1) / 2, zc - 4)
    NOTCH[(label, x0)] = 2 * (hi - lo)
    SHAPES.append(flight(fid, x0, x1, zc, zc - 2 * (hi - lo), lo, hi))

FRONT = {"row-a": "C0", "row-b": "C1", "row-c": "C2", "row-d": "C3"}
for row, front, back, cells in ROWS:
    label = FRONT[row]
    crossings = CROSS[label]
    for cell, plane, fx0, fx1, bx0, bx1 in cells:
        front_edge = along(front, fx0, fx1)
        notched = []
        for x, z in front_edge:
            notched.append((x, z))
            for a, b in crossings:
                if abs(x - a) < 1e-6 and fx0 <= a and b <= fx1:
                    depth = NOTCH[(label, a)]
                    notched += [(a, z - depth), (b, z - depth)]
        back_edge = along(back, bx1, bx0)
        ring = notched + back_edge
        SHAPES.append(made(f"terrace-{cell}", ring, None, anchors=[plane.at(x, z) for x, z in ring]))
        gaps = [span for span in crossings if fx0 <= span[0] and span[1] <= fx1]
        parapet(f"wall-{cell}", front_edge, plane, gaps)

# --- the aia, the cava and the tunnel under the aia ---

# the aia's terrace: an irregular field, notched west for the stair from the grove, front for the stair
# from the open slope and the tunnel's mouth, back for the stair down from the piazza
AIA_RING = [(-6, -84), (16, -84), (27, -85), (28, -60), (26, -52),
            (23, -52), (23, -60), (18, -60), (18, -52), (11, -52), (11, -58), (8, -58), (8, -52),
            (-6, -53)]
SHAPES.append(made("aia", AIA_RING, AIA))
SHAPES.append(flight("stair-front", 18, 23, -52, -60, SLOPE_TOP, AIA))
SHAPES.append(flight("stair-piazza", 6, 11, -84, -90, AIA, PIAZZA))
# the threshing floor: a paved disc a block proud of the aia inside a lava-stone kerb, four gaps in it
CX, CZ = 10, -68


def arc(cx, cz, r, a0, a1, n):
    import math
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


SHAPES.append({"id": "aia-floor", "type": "circle", "operation": "add", "center_x": CX, "center_z": CZ,
               "radius": 9, "base_height": FLOOR, "relief_scope": "exclude", "theme": "borgo"})
for n, (a0, a1) in enumerate([(12, 78), (102, 168), (192, 258), (282, 348)]):
    SHAPES.append({"id": f"aia-kerb-{n}", "type": "polyline", "operation": "add", "radius": 0.55,
                   "relief_scope": "exclude", "material": {"use": "drystone"}, "keepClear": True,
                   "vertices": [[round(x, 2), round(z, 2)] for x, z in arc(CX, CZ, 9.3, a0, a1, 6)],
                   "base_height": KERB})
# the cava: a quarry pit cut at the aia's foot, its floor at 23, and the tunnel it opens into
CAVA_FLOOR = 23
SHAPES.append(made("cava", [(2, -51), (16, -51), (17, -45), (13, -40), (6, -39), (2, -44)], CAVA_FLOOR,
                   "sciara"))
SHAPES.append(made("tunnel-floor", [(8, -58), (11, -58), (11, -51), (8, -51)], CAVA_FLOOR, "sciara"))
TUNNEL_ROOF = {"id": "tunnel-roof", "name": "Tunnel roof", "base_y": 0,
               "shapes": [{"id": "tunnel-roof-slab", "type": "rectangle", "operation": "add",
                           "min_x": 8, "min_z": -58, "max_x": 11, "max_z": -52,
                           "floor": CAVA_FLOOR + 3, "base_height": AIA - CAVA_FLOOR - 3,
                           "theme": "campagna"}],
               "groups": [{"id": "tunnel-roof-body", "name": "Tunnel roof", "mirrors": True,
                           "shapeIds": ["tunnel-roof-slab"]}]}

# --- the village ---

PIAZZA_RING = [(-20, -110), (4, -108), (16, -108), (16, -84), (11, -84), (11, -90), (6, -90), (6, -84),
               (-6, -84)]
PIAZZA_RING += along(C4, EAST, -20)
SHAPES.append(made("piazza", PIAZZA_RING, PIAZZA, "borgo"))
LOWER_W = [(-48, -114), (-20, -112)] + along(C4, -20, -48)
LOWER_W = [(x, z) for x, z in LOWER_W]
# notch the lower west quarter for the stair down to the grove at C4
x0, x1 = CROSS["C4"][0]
zc = z_on(C4, (x0 + x1) / 2)
notched = []
for x, z in LOWER_W:
    notched.append((x, z))
    if abs(x - x1) < 1e-6:
        notched += [(x1, z - 4), (x0, z - 4)]
SHAPES.append(made("village-lower-w", notched, LOWER))
SHAPES.append(flight("stair-grove", x0, x1, zc, zc - 4, round(PLANES["d1"].at(x0, zc)), LOWER))
parapet("wall-village-w", along(C4, -48, -20), Plane(LOWER, 0, 0), [CROSS["C4"][0]])
parapet("wall-piazza", along(C4, -20, EAST), Plane(PIAZZA, 0, 0), [])
parapet("wall-piazza-aia", [(-6, -84), (6, -84)], Plane(PIAZZA, 0, 0), [])
parapet("wall-piazza-aia-e", [(11, -84), (16, -84)], Plane(PIAZZA, 0, 0), [])
UPPER_W_FRONT = [(-48, -114), (-38, -113.3), (-34, -113.3), (-20, -112)]
SHAPES.append(made("village-upper-w", [(-48, -148), (-20, -148), (-20, -136), (-24, -136), (-24, -132),
                                       (-20, -132), (-20, -112), (-34, -113.3), (-34, -117.3),
                                       (-38, -117.3), (-38, -113.3), (-48, -114)], UPPER))
SHAPES.append(flight("stair-upper-w", -38, -34, -113.3, -117.3, LOWER, UPPER))
SHAPES.append(flight_x("stair-rear-w", -136, -132, -20, -24, LOWER, UPPER))
parapet("wall-upper-w", UPPER_W_FRONT, Plane(UPPER, 0, 0), [(-38, -34)])
SHAPES.append(made("village-rear", [(-20, -148), (16, -148), (16, -128), (-20, -128)], LOWER))
SHAPES.append(made("village-lower-e", [(16, -114), (48, -116), (48, -88), (27, -85), (16, -84)], LOWER))
parapet("wall-lower-e", [(16, -84), (27, -85)], Plane(LOWER, 0, 0), [])
SHAPES.append(made("village-upper-e", [(16, -148), (48, -148), (48, -116), (36, -115.6), (36, -119.6),
                                       (32, -119.6), (32, -115.5), (16, -114), (16, -132), (20, -132),
                                       (20, -136), (16, -136)], UPPER))
SHAPES.append(flight("stair-upper-e", 32, 36, -115.5, -119.5, LOWER, UPPER))
SHAPES.append(flight_x("stair-rear-e", -136, -132, 16, 20, LOWER, UPPER))
parapet("wall-upper-e", [(16, -114), (32, -115.5), (36, -115.6), (48, -116)], Plane(UPPER, 0, 0),
        [(32, 36)])

# --- paint on relief ground: the sciara, the west lobe ---
SHAPES += [
    {"id": "sciara-flow", "type": "polygon", "operation": "add", "base_height": LIP, "theme": "sciara",
     "vertices": [[0, 0], [1, 0], [1, 1]]},
    {"id": "lobe-flow", "type": "polygon", "operation": "add", "base_height": LIP, "theme": "sciara",
     "vertices": [[0, 0], [1, 0], [1, 1]]},
]

OUTLINES = {
    "sciara-flow": {"at": [38, -56], "radius": 16, "radiusZ": 31, "points": 36, "lobes": 5,
                    "wobble": 0.18, "phase": 0.7, "turn": -6},
    "tongue": {"at": [38, -56], "radius": 8, "radiusZ": 24, "points": 32, "lobes": 5, "wobble": 0.15,
               "phase": 0.7, "turn": -6},
    "lobe-flow": {"at": [-43, -36], "radius": 8, "radiusZ": 17, "points": 24, "lobes": 3, "wobble": 0.2,
                  "phase": 2.1, "turn": 8},
    "lobe": {"at": [-43, -36], "radius": 4, "radiusZ": 12, "points": 20, "lobes": 3, "wobble": 0.15,
             "phase": 2.1, "turn": 8},
}

RELIEF = {"team": {
    "base": LIP, "reach": 0, "step": 1, "landform": "rolling",
    "grain": {"amplitude": 2, "scale": 32, "seed": 9},
    "marks": [
        {"id": "lip", "kind": "line", "points": [[-56, -16], [-20, -15], [12, -17], [56, -16]],
         "h": LIP, "r": 3},
        {"id": "slope-top", "kind": "line", "points": [[-6, -55], [2, -55], [18, -56], [32, -54]],
         "h": SLOPE_TOP, "r": 2},
    ],
    "pushes": [
        {"id": "tongue", "ring": [[0, 0], [1, 0], [1, 1]], "amount": 9, "falloff": 10, "crown": 4,
         "roughness": 0.5, "seed": 3},
        {"id": "lobe", "ring": [[0, 0], [1, 0], [1, 1]], "amount": 5, "falloff": 6, "crown": 2,
         "roughness": 0.5, "seed": 5},
    ],
}}

# --- made things ---------------------------------------------------------------------------------------------

def block_rect(shape_id, x0, z0, x1, z1, floor, height, block):
    return {"id": shape_id, "type": "rectangle", "operation": "add", "keepClear": True,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1, "floor": floor, "base_height": height,
            "material": solid(*block)}


def made_layer(layer_id, name, part_of, shapes):
    return {"id": layer_id, "name": name, "base_y": 0, "kind": "made", "part_of": part_of,
            "shapes": shapes,
            "groups": [{"id": f"{layer_id}-body", "name": name, "mirrors": True,
                        "shapeIds": [shape["id"] for shape in shapes]}]}


def posts_and_roof(prefix, x0, z0, x1, z1, foot, posts_high, post_block, roof_block, roof_overhang=0):
    """Four corner posts and a one-course roof on them, one layer: the posts rise a course past the roof
    so they win their columns."""
    shapes = [block_rect(f"{prefix}-roof", x0 - roof_overhang, z0 - roof_overhang, x1 + roof_overhang,
                         z1 + roof_overhang, foot + posts_high, 1, roof_block)]
    for i, (px, pz) in enumerate([(x0, z0), (x1 - 1, z0), (x0, z1 - 1), (x1 - 1, z1 - 1)]):
        shapes.append(block_rect(f"{prefix}-post-{i}", px, pz, px + 1, pz + 1, foot, posts_high + 2,
                                 post_block))
    return shapes


def campanile(cx, cz, foot):
    """The church's bell tower: a quartz shaft whose four corner posts rise past it to frame an open
    belfry, under a stepped brick cap. Two layers, because the posts and the cap are two spans a column."""
    x0, z0, x1, z1 = cx - 2, cz - 2, cx + 3, cz + 3
    shaft, belfry = 15, 4
    body = [block_rect("campanile-shaft", x0, z0, x1, z1, foot, shaft, (QUARTZ, 0))]
    for i, (px, pz) in enumerate([(x0, z0), (x1 - 1, z0), (x0, z1 - 1), (x1 - 1, z1 - 1)]):
        body.append(block_rect(f"campanile-post-{i}", px, pz, px + 1, pz + 1, foot, shaft + belfry,
                               (QUARTZ, 2)))
    cap = [block_rect(f"campanile-cap-{step}", x0 - 1 + step, z0 - 1 + step, x1 + 1 - step, z1 + 1 - step,
                      foot + shaft + belfry, step + 1, (BRICK, 0)) for step in range(4)]
    return [made_layer("campanile-body", "Campanile", "campanile", body),
            made_layer("campanile-cap", "Campanile cap", "campanile", cap)]


def well(cx, cz, foot):
    """The piazza's well: a ring of quartz two courses high round water, two oak posts on the ring carrying
    a brick-slab roof. Three layers, one span a column each."""
    ring = [block_rect("well-ring-n", cx - 2, cz - 2, cx + 2, cz - 1, foot, 2, (QUARTZ, 0)),
            block_rect("well-ring-s", cx - 2, cz + 1, cx + 2, cz + 2, foot, 2, (QUARTZ, 0)),
            block_rect("well-ring-w", cx - 2, cz - 1, cx - 1, cz + 1, foot, 2, (QUARTZ, 0)),
            block_rect("well-ring-e", cx + 1, cz - 1, cx + 2, cz + 1, foot, 2, (QUARTZ, 0)),
            block_rect("well-water", cx - 1, cz - 1, cx + 1, cz + 1, foot, 1, (9, 0))]
    posts = [block_rect(f"well-post-{i}", px, cz - 1, px + 1, cz, foot + 2, 2, (FENCE, 0))
             for i, px in enumerate([cx - 2, cx + 1])]
    roof = [block_rect("well-roof", cx - 2, cz - 2, cx + 2, cz + 1, foot + 4, 1, (SLAB, 4))]
    return [made_layer("well-ring", "Well", "well", ring), made_layer("well-posts", "Well posts", "well", posts),
            made_layer("well-roof", "Well roof", "well", roof)]


def stall(prefix, x0, z0, foot, awning):
    """A market stall: a plank counter under an awning of wool on four oak posts."""
    x1, z1 = x0 + 4, z0 + 3
    top = posts_and_roof(prefix, x0, z0, x1, z1, foot, 3, (FENCE, 0), (WOOL, awning))
    counter = [block_rect(f"{prefix}-counter", x0 + 1, z1 - 1, x1 - 1, z1, foot, 1, (PLANKS, 0))]
    return [made_layer(f"{prefix}-top", "Market stall", prefix, top),
            made_layer(f"{prefix}-counter", "Market stall counter", prefix, counter)]


def lookout(cx, cz, foot):
    """A wooden lookout over the grove's front: four oak posts to a spruce deck at eight, a fence rail round
    the deck, and a ladder up the south-west post into a hole in the deck."""
    x0, z0, x1, z1 = cx - 2, cz - 2, cx + 2, cz + 2
    deck = foot + 8
    posts = [block_rect(f"lookout-post-{i}", px, pz, px + 1, pz + 1, foot, 8, (LOG, 0))
             for i, (px, pz) in enumerate([(x0, z0), (x1 - 1, z0), (x0, z1 - 1), (x1 - 1, z1 - 1)])]
    posts.append(block_rect("lookout-ladder", x0, z1, x0 + 1, z1 + 1, foot, 9, (65, 3)))
    floor = [block_rect("lookout-deck", x0 - 1, z0 - 1, x1 + 1, z1, deck, 1, (PLANKS, 1)),
             block_rect("lookout-deck-w", x0 - 1, z1, x0, z1 + 1, deck, 1, (PLANKS, 1)),
             block_rect("lookout-deck-e", x0 + 1, z1, x1 + 1, z1 + 1, deck, 1, (PLANKS, 1))]
    rail = [block_rect("lookout-rail-n", x0 - 1, z0 - 1, x1 + 1, z0, deck + 1, 1, (FENCE, 0)),
            block_rect("lookout-rail-s", x0 + 1, z1, x1 + 1, z1 + 1, deck + 1, 1, (FENCE, 0)),
            block_rect("lookout-rail-w", x0 - 1, z0, x0, z1 + 1, deck + 1, 1, (FENCE, 0)),
            block_rect("lookout-rail-e", x1, z0, x1 + 1, z1, deck + 1, 1, (FENCE, 0))]
    return [made_layer("lookout-posts", "Lookout", "lookout", posts),
            made_layer("lookout-deck", "Lookout deck", "lookout", floor),
            made_layer("lookout-rail", "Lookout rail", "lookout", rail)]


def shrine(cx, cz, foot):
    """A wayside shrine among the olives: a quartz pillar on a lava-stone step, a brick-slab hood over it."""
    body = [block_rect("shrine-step", cx - 1, cz - 1, cx + 2, cz + 2, foot, 1, (CLAY, 15)),
            block_rect("shrine-pillar", cx, cz, cx + 1, cz + 1, foot, 4, (QUARTZ, 2))]
    hood = [block_rect("shrine-hood", cx - 1, cz - 1, cx + 2, cz + 2, foot + 4, 1, (SLAB, 4))]
    return [made_layer("shrine-body", "Shrine", "shrine", body),
            made_layer("shrine-hood", "Shrine hood", "shrine", hood)]


def crates(prefix, x0, z0, foot):
    """Olive crates stacked at a terrace's edge after the picking: spruce planks two high and one."""
    return [made_layer(prefix, "Olive crates", prefix, [
        block_rect(f"{prefix}-a", x0, z0, x0 + 2, z0 + 1, foot, 2, (PLANKS, 1)),
        block_rect(f"{prefix}-b", x0 + 2, z0, x0 + 3, z0 + 1, foot, 1, (PLANKS, 1))])]


LAYERS = [TUNNEL_ROOF]
LAYERS += campanile(13, -106, PIAZZA)
LAYERS += well(-19, -96, PIAZZA)
LAYERS += stall("stall-west", -4, -58, AIA, 14)
LAYERS += stall("stall-back", 19, -80, AIA, 0)
LAYERS += lookout(-32, -25, round(PLANES["a1"].at(-32, -25)))
LAYERS += shrine(-44, -82, round(PLANES["d1"].at(-44, -82)))
LAYERS += crates("crates-b1", -33, -47, round(PLANES["b1"].at(-33, -47)))
LAYERS += crates("crates-c2", -24, -64, round(PLANES["c2"].at(-24, -64)))

# --- dressing ---------------------------------------------------------------------------------------------

def tree(prop_id, x, z, style):
    return {"id": prop_id, "kind": "tree", "x": x, "z": z, "style": style}


def track(prop_id, points, wander=2):
    """A farm track: three blocks of soft ground a third each, solid, wandering a little between its ends."""
    return {"id": prop_id, "kind": "stroke", "points": points, "radius": 1.5, "style": "solid",
            "claimsGround": True, "wander": wander, "wanderLength": 14, "pave": {"use": "track"}}


def street(prop_id, points, radius=2):
    """A village street, paved like the piazza, running door to door."""
    return {"id": prop_id, "kind": "stroke", "points": points, "radius": radius, "style": "solid",
            "claimsGround": True, "pave": {"use": "paving"}}


def house(prop_id, x0, z0, x1, z1, front, storeys=1, wing=None):
    """A house of the village's one style. `wing` is a second rectangle sharing a whole edge with the
    first, one storey lower, which is what makes two houses of one style differ in shape."""
    main = {"corners": [[x0, z0], [x1, z1]], "spec": {"storeysHigh": storeys}}
    wings = [main]
    if wing:
        # the main block is the hall, its ridge along the edge the wing shares; the wing's ridge runs into it
        shared_along_z = wing[0][0] > x1 or wing[1][0] < x0
        main["spec"]["ridge"] = "alongZ" if shared_along_z else "alongX"
        wings.append({"corners": [list(wing[0]), list(wing[1])],
                      "spec": {"storeysHigh": max(1, storeys - 1),
                               "ridge": "alongX" if shared_along_z else "alongZ"}})
    return {"id": prop_id, "kind": "house", "style": "casa", "front": front, "wings": wings}


HOUSES = [
    # The west quarter stands flush against the straight back and west coasts, so those sides are the map's
    # edge, and eight blocks clear of the spawn hall, so its east side is a way past.
    house("casa-w1", -47, -111, -40, -105, "posZ"), house("casa-w2", -33, -111, -27, -105, "posZ", 2,
                                                                 ((-26, -111), (-23, -107))),
    house("casa-w4", -34, -98, -27, -93, "negZ"),
    house("casa-w5", -47, -128, -41, -121, "posZ", 2,
                                                         ((-40, -128), (-37, -124))), house("casa-w6", -33, -128, -26, -121, "posZ"),
    house("casa-w7", -47, -147, -39, -140, "posZ"), house("casa-w8", -35, -147, -27, -140, "posZ", 2),
    # the east quarter the same way against the east coast
    house("casa-e1", 21, -128, 30, -121, "posZ"), house("casa-e2", 41, -128, 47, -119, "posZ", 2,
                                                        ((37, -128), (40, -124))),
    house("casa-e3", 21, -147, 29, -140, "posZ", 2), house("casa-e4", 36, -147, 47, -140, "posZ"),
    house("casa-e5", 21, -111, 29, -105, "posZ"), house("casa-e6", 40, -110, 47, -102, "posZ", 2,
                                                        ((36, -110), (39, -106))),
    # the church on the piazza, its campanile beside it
    house("chiesa", 2, -107, 9, -98, "negX", 2, ((3, -97), (8, -94))),
]

DRESSING = {
    "styles": {
        "olive-a": {"library": "olive-3"}, "olive-b": {"library": "olive-7"},
        "olive-c": {"library": "olive-9"}, "olive-young": {"library": "small-olive-2"},
        "casa": {"kind": "house", "library": "brick-roofed-quartz-house"},
        "lava-erratic": {"kind": "boulder", "form": "angular", "size": 3, "rock": {"use": "lava-rock"},
                         "mossy": False},
        "lava-cinder": {"kind": "boulder", "form": "angular", "size": 2, "rock": {"use": "lava-rock"},
                        "mossy": False},
    },
    "props": [
        # the village streets, door to door, and the lane behind the spawn
        street("street-main", [[-8, -111], [-8, -96], [8, -91]]),
        street("street-west", [[-20, -101], [-30, -101.5], [-47, -101.5]]),
        street("street-west-up", [[-36, -103], [-36, -112]], 1.5),
        street("street-west-top", [[-36, -118], [-36, -131], [-46, -131.5]], 1.5),
        street("street-rear", [[-8, -125], [-8, -134], [-19, -134]], 1.5),
        street("street-rear-w", [[-25, -134], [-36, -134]], 1.5),
        street("street-rear-e", [[-8, -134], [15, -134]], 1.5),
        street("street-rear-e2", [[21, -134], [34, -133], [47, -133]], 1.5),
        street("street-east", [[16, -100], [34, -101], [47, -101]]),
        street("street-east-up", [[34, -103], [34, -114.5]], 1.5),
        street("street-east-top", [[34, -121], [34, -132]], 1.5),
        # the farm tracks through the grove, flight to flight
        track("track-d", [[-38, -87], [-37, -80], [-36, -72]]),
        track("track-c", [[-36, -66], [-32, -62], [-23, -58]]),
        track("track-b", [[-23, -52], [-26, -46], [-29, -42]]),
        track("track-a", [[-29, -34], [-23, -29], [-15, -27]]),
        track("track-a2", [[-9, -34], [-10, -30], [-14, -27]], 1),
        # the lava the mountain threw, lying at the foot of the sciara and the lobe
        {"id": "erratic-1", "kind": "boulder", "x": 19, "z": -34, "style": "lava-erratic"},
        {"id": "erratic-2", "kind": "boulder", "x": 22, "z": -25, "style": "lava-cinder"},
        {"id": "erratic-3", "kind": "boulder", "x": 30, "z": -23, "style": "lava-erratic"},
        {"id": "erratic-4", "kind": "boulder", "x": 45, "z": -22, "style": "lava-cinder"},
        {"id": "erratic-5", "kind": "boulder", "x": -40, "z": -17, "style": "lava-cinder"},
        # the grove: each terrace planted in a line a third of the way back from its parapet
        tree("olive-b1", -34, -41, "olive-c"), tree("olive-b2", -16, -42, "olive-a"),
        
        tree("olive-c1", -43, -58, "olive-a"), tree("olive-c2", -26, -66, "olive-young"),
        tree("olive-c3", -18, -57, "olive-c"),
        tree("olive-d1", -44, -76, "olive-b"), tree("olive-d2", -30, -78, "olive-a"),
        tree("olive-d3", -18, -76, "olive-c"), tree("olive-d4", -10, -78, "olive-young"),
        # young olives in the village
        tree("olive-v1", -44, -117, "olive-young"), tree("olive-v2", 44, -114, "olive-young"),
        *HOUSES,
        # ground cover over the whole side, low and short so the ground still reads
        {"id": "cover", "kind": "flora", "points": [[-56, -152], [56, -152], [56, -8], [-56, -8]],
         "spec": {"coverage": 0.22, "scale": 9, "octaves": 2, "fernShare": 0.1, "flowerShare": 0.04,
                  "flowerScale": 7, "tallShare": 0.03, "deadBushShare": 0.15}},
    ],
}

REFINEMENT = {
    "materials": MATERIALS,
    "themes": THEMES,
    "mapTheme": "campagna",
    "biome": {"kind": "solid", "id": 35},   # Savanna: grass #bfb755, foliage #aea42a
    "shapePropsById": {"flank-34": {"relief_scope": "exclude"}},
    "addShapes": SHAPES + WALLS,
    "addLayers": LAYERS,
    "outlines": OUTLINES,
    "bendShapes": {
        "flank-22": {"tension": 0.22, "wander": 3, "step": 9, "seed": 5, "side": "out"},
    },
    "relief": RELIEF,
    "roomStyles": {"spawn": {"library": "brick-roofed-quartz-house"}},
    "dressing": DRESSING,
    "authors": [{"name": "Opus 5.5", "contribution": "authored through the studio's API"}],
    "created": "2026-10-05",
}

json.dump(PLAN, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(REFINEMENT, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.refinement.json — {len(SHAPES)} shapes, {len(WALLS)} wall "
      f"pieces, {len(LAYERS)} layers")
