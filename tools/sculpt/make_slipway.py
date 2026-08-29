"""Write the spec for Slipway — a harbour DTM with a ship, two balloons and a dockside crane — for
`drive.py` to build.

The board exists to put the made-thing machinery on a map that is actually played rather than on a gallery
deck. Three things are stated three different ways, and the difference is the point:

- the **ship** floats, so it states an absolute floor at the load line and no seat;
- the **balloons** fly, so they state an absolute floor and no seat either;
- the **crane** stands on the dock, so it states `seat: "ground"` and settles onto it, one drop for all four
  of its layers. It faces the water and its load hangs out over the harbour.

**A settlement is a pad, then roads, then houses — in that order.** The dock and the upland are plan pieces
at their own surface whose compiled shapes are marked `relief_scope: "exclude"`, so the relaxation bends
around them and each is a flat terrace rather than a slope with buildings sliding down it. The roads are
drawn onto those pads and the houses are placed clear of them.

**The two settlements a team has are not each other's mirror.** One is on the dock at the water; the other is
cut back into the hill behind the town. Only the board is symmetric.

**The board's size is the goal rules.** `GO4` holds a destroy goal 40–90 blocks from its own spawn by walk
and `GO1` holds the enemy walk at 3–4 times that; `GO3` then holds opposing goals to 85–150 and `GO2` a
team's own pair to 35–65. Solved together they give a board 256 x 256. The **dock goal is deliberately
outside** GO1 and GO4 — a goal at the water is a forward objective and the bands are written for two goals in
the defender's rear — and `review/opus5-slipway.md` carries what it measures.

    python3 tools/sculpt/make_slipway.py specs/opus5-slipway
    python3 tools/drive.py specs/opus5-slipway "Slipway" --out /tmp/slipway
"""
import json
import math
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import board
import models
from layers import compile_layers, stats

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")

CELL = 4
# Surfaces, in blocks. Every step between neighbouring pieces is a multiple of two (`EL1`).
BASIN, WATER, DOCK, QUAY, PORT, TOWN, HEAD, RIDGE, BACK = 6, 16, 20, 22, 22, 24, 26, 28, 30

PLAN = {
    "plan": 1,
    "meta": {"name": "Slipway"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 28, "surface": QUAY,
                "observerY": 100},
    # The author's own composition, sketched on a phone and scaled up here: a harbour with the ship on it,
    # a crane dock west of centre, the first goal's dock at the middle, a port east, the dockside settlement
    # behind the west dock and a second settlement back and to the east with the other goal in front of it —
    # and a field on each arm for a balloon to stand over. `LN2` caps a lane at 110 blocks and rects sharing
    # a cross-axis interval merge into one lane however many pieces they are written as; 104 is the longest.
    "pieces": [
        {"id": "basin",           "role": "piece", "rect": [-13, -4, 26,  8], "surface": BASIN},
        {"id": "balloon-field",   "role": "piece", "rect": [-25, -4, 12, 11], "surface": HEAD},
        {"id": "crane-dock",      "role": "piece", "rect": [-13,  4,  6,  5], "surface": DOCK},
        {"id": "goal-dock",       "role": "piece", "rect": [ -7,  4,  7,  7], "surface": DOCK},
        {"id": "quay-e",          "role": "piece", "rect": [  0,  4, 11,  7], "surface": QUAY},
        {"id": "port",            "role": "piece", "rect": [ 11,  4, 14, 10], "surface": PORT},
        {"id": "dock-town",       "role": "piece", "rect": [-18,  7,  5,  7], "surface": TOWN},
        {"id": "dock-yard",       "role": "piece", "rect": [-13,  9,  6,  5], "surface": TOWN},
        {"id": "mid",             "role": "piece", "rect": [ -7, 11, 18,  3], "surface": TOWN},
        {"id": "back-settlement", "role": "piece", "rect": [  7, 14, 11, 10], "surface": BACK},
        {"id": "port-back",       "role": "piece", "rect": [ 18, 14,  7, 10], "surface": HEAD},
        {"id": "hill",            "role": "piece", "rect": [-18, 14, 25,  9], "surface": RIDGE},
        {"id": "fore-spawn",      "role": "piece", "rect": [ -7, 23, 14,  5], "surface": RIDGE},
        {"id": "back-band",       "role": "piece", "rect": [  7, 24, 11,  4], "surface": RIDGE},
        {"id": "spawn",           "role": "spawn", "rect": [ -3, 28,  5,  5], "surface": BACK},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [2.5, 2.5], "facing": "down"}],
        # Outside the spawn room and beside its door lane rather than in it: a player leaving for the front
        # passes the iron instead of walking into it. `ST2` complains that it is off the spawn piece, which
        # is the author's call — a stamped spawn has a doorway, and a chest in a doorway is in the way.
        "iron":   [{"id": "iron-1", "piece": "fore-spawn", "at": [11.0, 2.0]}],
        # One goal on the middle dock and one in front of the back settlement, which is the author's own
        # composition: the two a team defends stand at opposite corners of its ground rather than side by
        # side. The dock goal is a FORWARD objective and reads outside `GO1`/`GO4`, and its own mirror is
        # under `GO3` — the bands are written for two goals in a defender's rear, and this board is the
        # measurement that says what a forward one costs. `review/opus5-slipway.md` carries the numbers.
        "destroyables": [
            {"id": "destroyable-1", "style": "pillar-2", "at": [-6.0, 6.5], "materials": "obsidian",
             "float": 2, "name": "The Careening Beam"},
            {"id": "destroyable-2", "style": "pillar-2", "at": [ 9.0, 13.0], "materials": "obsidian",
             "float": 2, "name": "The Powder House"},
        ],
    },
}


def style(name):
    """One of the author's own ground patterns, by the name it was saved under. Fetched rather than
    transcribed: a copy here would be free to disagree with the library the studio paints from."""
    with urllib.request.urlopen(f"{API}/styles?limit=400") as answer:
        rows = json.load(answer)
    for row in rows:
        if row.get("name") == name:
            return json.loads(row["params"])
    raise SystemExit(f"no style named {name!r} in the library")


def ground(surface, wall, rim=None, fill=None):
    """A terrain theme over four full materials rather than four blocks — which is what the author's styles
    are, so binding one to a bucket is the whole of using them. The surface is one course: `all green` and
    `all sand` are picks, and a pick two courses deep is soil surfaced twice over, which `PT1` refuses.

    **Landscape takes no rim.** A rim caps a plateau boundary, and `rimEdges: "boundary"` caps every one of
    them — a face against a structure and against level ground the paint calls a different plateau included.
    On grass or on terracotta that draws a hard line round every patch and the ground reads as a diagram of
    itself; the surface is what a landscape is, so it runs to the edge. A rim is for ground that is built —
    a stone kerb along a quay is a kerb — so a theme states one only where it means one."""
    theme = {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "rim": {"enabled": rim is not None, "depth": 1,
                "material": rim or {"kind": "solid", "id": 1, "data": 0}},
        "surface": {"enabled": True, "depth": 1, "material": surface},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill or wall,
    }
    if rim is not None: theme["rimEdges"] = "boundary"
    return theme


def turn(model, quarter):
    """A model rotated a quarter turn at a time about its own origin, in the plan axes."""
    def spun(x, y, z):
        for _ in range(quarter % 4):
            x, z = -z, x
        return x, y, z
    return {spun(x, y, z): material for (x, y, z), material in model.items()}


def place(model, at, quarter=0):
    dx, dy, dz = at
    return {(x + dx, y + dy, z + dz): material for (x, y, z), material in turn(model, quarter).items()}


def made(name, voxels, seat=None):
    """A model compiled to layers, in the shape `addLayers` takes. `kind`, `prop` and `seat` ride with it."""
    layers = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L", group_name=name,
                            prop=name, seat=seat)
    return [{"id": layer["id"], "name": layer["name"], "base_y": 0, "kind": layer["kind"],
             "prop": layer["prop"], **({"seat": layer["seat"]} if "seat" in layer else {}),
             "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
            for layer in layers], stats(voxels, layers)


def sculpted():
    add_layers, table = [], []

    # The ship lies athwart the basin so both shores see the same broadside, and floats: her load strake sits
    # at the water line and her keel clears the basin floor.
    ship = place(models.ship(), (-5, WATER - 8, 0), quarter=1)
    layers, row = made("ship", ship)
    add_layers += layers
    table.append(("ship", row))

    # A balloon standing over each arm's own field, just risen off it. Two rather than one because a single
    # one on a rot_180 board is the one thing on it that is not answered across the axis. What a made thing
    # costs a played board is build ceiling — the highest column plus twenty — so height here is spent.
    for name, at in [("balloon-w", (-78, HEAD + 2, -8)), ("balloon-e", (78, HEAD + 2, 8))]:
        layers, row = made(name, place(models.balloon(), at))
        add_layers += layers
        table.append((name, row))

    # The crane stands on its own dock at the water's edge, unturned, so its shear legs rake out over the
    # harbour and the load on its chain hangs past the quay — the whole reason a crane is on a quay. Seated:
    # the sill and feet find the pad's top, and the jib is free to reach over water they never touch.
    for name, at, quarter in [("crane-w", (-40, DOCK, 18), 0), ("crane-e", (40, DOCK, -18), 2)]:
        layers, row = made(name, place(models.crane(), at, quarter), seat="ground")
        add_layers += layers
        table.append((name, row))

    # A car park on the port, four cars a side. At nine blocks a car is four boxes and four cubes, which is
    # the other end of the scale from the ship — and what makes the port read as somewhere goods leave from.
    for index, (x, z, quarter, back) in enumerate([(58, 26, 0, True), (70, 26, 0, False),
                                                   (58, 40, 2, True), (70, 40, 2, False)]):
        for side, (px, pz, turn_) in enumerate([(x, z, quarter), (-x, -z, (quarter + 2) % 4)]):
            name = f"car-{index}-{side}"
            layers, row = made(name, place(models.minicar(cabin_back=back), (px, PORT, pz), turn_),
                               seat="ground")
            add_layers += layers
            if side == 0:
                table.append((name, row))

    return add_layers, table


# ── the settlements: a pad, then roads, then houses ───────────────────────────────────────────────────────

ROADS = [
    # The waterfront's back lane, from the goal dock east past the port. It starts where the crane dock ends
    # — a road through a crane's sill is a road broken by it — and runs along the **back** of the quay, which
    # leaves the eighteen blocks between it and the water as working ground rather than a verge.
    {"id": "quay-road", "kind": "path", "seed": 3, "route": True, "radius": 3, "coverage": 0.95,
     "points": [[-24, 38], [4, 40], [30, 38], [58, 34], [92, 32]],
     "pave": {"kind": "solid", "id": 98, "data": 0}},
    # Behind the crane, along the back of the dock and into the town: the lane a load leaves the quay by.
    {"id": "dock-road", "kind": "path", "seed": 8, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-66, 40], [-44, 40], [-30, 42], [-18, 44]],
     "pave": {"kind": "solid", "id": 98, "data": 0}},
    # Up out of the dock, round the terrace row's western end and along the foot of the hill. It leaves the
    # dock town uncrossed on purpose: a twenty-block strip with a road down it holds no house, and the row
    # across the middle is the one thing joining the two towns.
    {"id": "town-road", "kind": "path", "seed": 4, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-18, 44], [-26, 54], [-32, 62], [-20, 66], [2, 70]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
    # The lane to the back settlement, past the goal that stands in front of it.
    {"id": "back-road", "kind": "path", "seed": 5, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-20, 66], [10, 64], [34, 70], [48, 82], [54, 92]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
    # And up over the hill to the spawn.
    {"id": "spawn-road", "kind": "path", "seed": 6, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-20, 66], [-22, 84], [-10, 98], [0, 114]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
]

# `(id, style, low corner, high corner, front)`. Footprints are inclusive of both corners and capped at 192
# blocks (`HP3`); they are laid **1.5:2 rather than square**, staggered in depth so a street is not a row of
# identical boxes, and turned four different ways — a rectangle with its door on the short end reads
# differently from the same rectangle with its door on the long one, and every house facing one way is a
# shed row rather than a town. Half the styles carry two or three storeys.
#
# **Every plot is a position the board's own ground was searched for**: the `ground` layer carries every
# column of the plot and a two-block ring, the rise across that stays under the building's own height
# (`DR-SLOPE`), it clears the roads (`DR-CROSS`), it clears every other plot's claim (`DR-CLAIM`) and it
# stands outside the +-10-block square a destroy goal keeps clear (`DressingScope.GoalStandoff`, `OB19`).
HOUSES = [
    # The dock town, kept where it was: the chandler at the head of the street, the sailmaker and the
    # cooperage in the yard behind the crane.
    ("chandler",       "@wh-count",        ( -68,  26), ( -58,  35), "posX"),
    ("sailmaker",      "@hoar-steading",   ( -65,  45), ( -56,  57), "posZ"),
    ("cooperage",      "@wh-shed",         ( -51,  46), ( -40,  55), "negX"),
    # The quay east of the goal dock: a harbour office at the water, and a store along from it.
    ("harbour-office", "@sn-compass-well", (   5,  19), (  16,  32), "negZ"),
    ("quay-store",     "@kr-deck",         (  21,  23), (  30,  31), "posX"),
    # The row across the middle, which is the one thing joining the two towns.
    ("arcade-w",       "@terrace",         ( -10,  47), (   4,  54), "negZ"),
    ("arcade-e",       "@terrace",         (   9,  47), (  23,  54), "posZ"),
    # The back settlement, cut into the upland and flattened.
    ("counting",       "@wh-count",        (  28,  82), (  37,  91), "posZ"),
    ("upland-hall",    "@17h-hall",        (  55,  66), (  66,  80), "posX"),
    # Under the balloon: what a field a balloon flies off has on it.
    ("balloon-shed",   "@wh-shed",         ( -81,  -8), ( -69,   1), "posZ"),
    ("field-cottage",  "@cairn-cottage",   ( -82,  13), ( -74,  24), "posX"),
    # The port, beside the car park.
    ("warehouse",      "@hoar-longhall",   (  79,  40), (  90,  54), "negZ"),
]

# The field the balloon flies off, the hill behind the town, and the back settlement's own green.
TREES = [(-90, -12), (-68, 19), (-89, 22), (-89, 14), (-31, 82), (11, 73), (-13, 76), (-5, 90), (0, 79),
         (21, 77), (62, 90), (47, 69), (43, 90)]

SPECIES = ["oak", "birch", "spruce", "oak", "birch"]


def houses():
    return [{"id": name, "kind": "house", "seed": 40 + index, "front": front,
             "points": [list(low), list(high)], "style": style_name}
            for index, (name, style_name, low, high, front) in enumerate(HOUSES)]


def trees():
    return [{"id": f"tree-{index}", "kind": "tree", "seed": 200 + index, "x": x, "z": z,
             "form": "template", "species": SPECIES[index % len(SPECIES)], "height": 9 + (index % 4)}
            for index, (x, z) in enumerate(TREES)]


def crates():
    """Cargo on the dock and under the balloon: boulders in a timber material read as bales and crates at
    this scale, and they are the one prop that takes a rock of its own."""
    timber = {"kind": "cell", "seed": 3, "cellSize": 3, "jitter": 40, "warp": 2,
              "palette": [{"kind": "solid", "id": 5, "data": 1}, {"kind": "solid", "id": 5, "data": 5},
                          {"kind": "solid", "id": 17, "data": 1}]}
    # Searched for like every other plot: clear of the crane's own ground, off the roads and outside the
    # dock goal's +-10 square, which a boulder standing in is `OB19`.
    at = [(-9, 29), (-10, 21), (-2, 21), (41, 26)]
    return [{"id": f"crate-{index}", "kind": "boulder", "seed": 500 + index, "x": x, "z": z,
             "form": "angular", "size": 1.4 + 0.3 * (index % 3), "mossy": False, "rock": timber}
            for index, (x, z) in enumerate(at)]


THEMES = {
    # **No ground a prop stands on is finished in a style whose palette holds wool.** The dressing pass reads
    # a wool-topped column as a stamp rather than terrain and declines everything on it (`DR-KEEP`), so a
    # quay paved in `white stone cells` or a hill turfed in `grass clay surface dark` takes no crate, no tree
    # and no house however flat it is. Every surface and wall below is drawn from the wool-free half of the
    # library, which is 159 of its 168 styles.
    #
    # **The two built grounds take a rim and the five landscapes do not.** A quay is masonry and a kerb along
    # its edge is a kerb; grass, terracotta and a seabed have no such line, and capping every plateau
    # boundary on them draws the plan back over the ground it was supposed to become.
    "quay":   ground(style("oldstone · fill"), style("stone fractal"),
                     {"kind": "solid", "id": 98, "data": 0}),
    "dock":   ground(style("terracotta with dirt"), style("stone fractal"),
                     {"kind": "solid", "id": 5, "data": 1}),
    # Clay turf rather than `all green`: `all green` mixes wool into its palette, the dressing pass reads
    # wool as a stamp's own block, and a tree on it is declined as built ground rather than terrain.
    "town":   ground(style("grass clay surface"), style("dirt clay fill")),
    "ridge":  ground(style("meadow · surface"), style("stone fractal")),
    "back":   ground(style("oldstone · surface"), style("stone fractal")),
    "head":   ground(style("rust cells"), style("stone fractal")),
    "seabed": ground(style("all sand"), style("dirt fractal")),

    # A made thing is painted in solids: the painter's buckets are a model of ground — a rim capping every
    # plateau boundary, a wall down every riser — and a curved form is nothing but boundaries, so a shaded
    # theme speckles it.
    "car-paint": board.solid(159, 14), "car-trim": board.solid(35, 15),
    "car-glass": board.solid(95, 3), "car-tail": board.solid(35, 14),

    "hull": board.solid(5, 1), "strake": board.solid(35, 14), "rail": board.solid(5, 0),
    "deck": board.solid(5, 2), "spar": board.solid(17, 1), "rig": board.solid(35, 15),
    "canvas": board.solid(155, 0), "glass": board.solid(95, 3), "lamp": board.solid(89, 0),

    "envelope-a": board.solid(35, 14), "envelope-b": board.solid(35, 0),
    "envelope-band": board.solid(35, 11), "wicker": board.solid(5, 4), "flame": board.solid(89, 0),

    "stone": board.solid(98, 0), "iron": board.solid(35, 15), "chain": board.solid(1, 6),
    "timber": board.solid(5, 1),
}


# How far a sample of the outline may be drawn in, and how often one is taken along a run of open shore.
# `showcase/04-organic-outline` pushes each of its ring samples inward by nought to nine blocks and takes one
# every fourteen; the cycle is what makes a shore wander rather than round off, and its length being coprime
# with nothing in the board keeps a long edge from repeating.
DRAW_IN = (0, 5, 9, 3, 7, 2, 8, 4, 6, 1, 7, 3)
SAMPLE_EVERY = 13
# The curve each sample's handles reach along the chord between its neighbours (Catmull-Rom). Below about
# 0.15 the ring still reads as straight segments; above about 0.35 a handle overshoots its own edge.
CURVE = 0.22


def plan_cells():
    """Every block the plan states ground at, its `rot_180` image included — the board's silhouette. Read
    from `PLAN` rather than from a build, so what the outline is tested against is the same set of rectangles
    the pieces are written as and cannot fall out of step with them."""
    cells = set()
    for piece in PLAN["pieces"]:
        cx, cz, wide, deep = piece["rect"]
        for x in range(cx * CELL, (cx + wide) * CELL):
            for z in range(cz * CELL, (cz + deep) * CELL):
                cells.add((x, z))
                cells.add((-x - 1, -z - 1))
    return cells


def held_cells():
    """Ground the outline may not draw in over: a spawn pad and its image, and the ground round each goal.
    `showcase/04` pins the samples over its spawn pads at nought for the same reason — a spawn standing off
    the coast is a spawn on a jetty (`WX11`), and a bay cut deep enough to strand an objective is the export
    gate's refusal rather than a decoration."""
    held = set()
    for piece in PLAN["pieces"]:
        if piece.get("role") != "spawn": continue
        cx, cz, wide, deep = piece["rect"]
        for x in range(cx * CELL - 4, (cx + wide) * CELL + 4):
            for z in range(cz * CELL - 4, (cz + deep) * CELL + 4):
                held.add((x, z)); held.add((-x - 1, -z - 1))
    for goal in PLAN["placements"]["destroyables"]:
        gx, gz = int(goal["at"][0] * CELL), int(goal["at"][1] * CELL)
        for x in range(gx - 14, gx + 15):
            for z in range(gz - 14, gz + 15):
                held.add((x, z)); held.add((-x, -z))
    return held


def compiled_rings():
    """The polygons `POST /plan/compile` fuses the plan into, by shape id — abutting pieces of equal height
    become one ring apiece. Asked rather than assumed: the ids and the winding are the compile's."""
    body = json.dumps(PLAN).encode()
    request = urllib.request.Request(f"{API}/plan/compile", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as answer:
        compiled = json.load(answer)
    return [(shape["id"], shape.get("base_height"), [tuple(v) for v in (shape.get("vertices") or [])])
            for shape in compiled["layout"]["layers"][0]["layout"]["shapes"]]


def within(ring, px, pz):
    """Whether a point lies inside a ring — the winding-independent crossing test."""
    hit = False
    for index in range(len(ring)):
        ax, az = ring[index]
        bx, bz = ring[(index + 1) % len(ring)]
        if (az > pz) != (bz > pz) and px < (bx - ax) * (pz - az) / (bz - az) + ax:
            hit = not hit
    return hit


def outline():
    """The board's silhouette, redrawn on the shapes the plan compiles to.

    A plan is written in cell rectangles, so it can say where ground is and never what shape its edge is.
    What the compile hands back is that edge as a ring per fused component — the upland here is one eight
    vertex polygon, a stretched T where the spawn's approach steps back out of the hill — and **the ring is
    what to redraw**. `shapePropsById` merges `vertices` and `controls` onto a compiled shape, so a drawn
    ring replaces the compiled one and nothing upstream knows.

    **Only the samples over open water move.** A ring's edges are of two kinds and they behave oppositely: an
    edge facing the void is the board's own coast and drawing it in shortens the coast, while an edge shared
    with the neighbouring shape is a seam, and drawing one side of a seam in leaves a strip of void between
    two pieces that were flush. So every step along every edge is classified by what lies two blocks off it,
    a sample is taken at each original vertex, at each point where an edge changes kind, and every
    `SAMPLE_EVERY` blocks along a run of open shore — and only the samples strictly inside such a run are
    drawn in. A sample over a spawn pad or a goal's ground is pinned at nought whatever it faces.

    The handles are Catmull-Rom: the tangent at a sample is the chord between its two neighbours and each
    handle reaches `CURVE` along it. Written by hand they fight each other and kink."""
    ground, held = plan_cells(), held_cells()
    props = {}

    for shape_id, _height, ring in compiled_rings():
        if len(ring) < 3: continue

        def open_shore(ax, az, bx, bz, at):
            """Whether the shore is open `at` blocks along the edge from (ax, az) to (bx, bz) — the cell two
            off its outward side holding no ground."""
            span = math.hypot(bx - ax, bz - az)
            px, pz = ax + (bx - ax) * at / span, az + (bz - az) * at / span
            step_x, step_z = (bz - az) / span, -(bx - ax) / span
            for side in (1, -1):
                probe = (px + step_x * side * 2.5, pz + step_z * side * 2.5)
                if not within(ring, *probe):
                    return (math.floor(probe[0]), math.floor(probe[1])) not in ground, (step_x * side, step_z * side)
            return False, (0.0, 0.0)

        samples = []                                     # (x, z, inward normal or None)
        for index in range(len(ring)):
            ax, az = ring[index]
            bx, bz = ring[(index + 1) % len(ring)]
            span = int(round(math.hypot(bx - ax, bz - az)))
            if span == 0: continue
            kinds = [open_shore(ax, az, bx, bz, at + 0.5) for at in range(span)]
            samples.append((ax, az, None))               # the vertex itself: a corner is never drawn in
            run_from = None
            for at in range(span):
                shore, normal = kinds[at]
                changed = at > 0 and kinds[at - 1][0] != shore
                if changed:
                    at_x, at_z = ax + (bx - ax) * at / span, az + (bz - az) * at / span
                    samples.append((at_x, at_z, None))   # the seam's own end, held where the compile put it
                    run_from = at if shore else None
                elif at == 0:
                    run_from = 0 if shore else None
                if shore and run_from is not None and at > run_from and (at - run_from) % SAMPLE_EVERY == 0 \
                        and span - at > SAMPLE_EVERY // 2:
                    at_x, at_z = ax + (bx - ax) * at / span, az + (bz - az) * at / span
                    samples.append((at_x, at_z, (-normal[0], -normal[1])))

        drawn, moved, step = [], [], 0
        for x, z, inward in samples:
            if inward is None or (math.floor(x), math.floor(z)) in held:
                drawn.append([round(x, 1), round(z, 1)])
                moved.append(False)
                continue
            reach = DRAW_IN[step % len(DRAW_IN)]
            step += 1
            drawn.append([round(x + inward[0] * reach, 1), round(z + inward[1] * reach, 1)])
            moved.append(True)

        # A handle is clamped to a fraction of the **shorter** of its two edges, and a sample that was not
        # drawn in gets none at all. Catmull-Rom's tangent is the chord between a sample's neighbours, which
        # is right on an evenly-spaced ring and wrong on this one: a compiled corner has one neighbour a
        # block away and the other seventy, so the chord swings the curve clear outside the polygon and
        # bites a hole where two shapes were flush. Pinning the corners is also what keeps a seam a seam.
        controls = {}
        for index, (x, z) in enumerate(drawn):
            if moved[index] is False: continue
            before, after = drawn[index - 1], drawn[(index + 1) % len(drawn)]
            tangent_x = (after[0] - before[0]) * CURVE
            tangent_z = (after[1] - before[1]) * CURVE
            reach = math.hypot(tangent_x, tangent_z)
            room = CURVE * min(math.hypot(x - before[0], z - before[1]),
                               math.hypot(after[0] - x, after[1] - z)) * 2
            if reach > room > 0:
                tangent_x, tangent_z = tangent_x * room / reach, tangent_z * room / reach
            controls[str(index)] = {"in": [round(x - tangent_x, 2), round(z - tangent_z, 2)],
                                    "out": [round(x + tangent_x, 2), round(z + tangent_z, 2)]}
        props[shape_id] = {"vertices": drawn, "controls": controls}
    return props


def finish(add_layers):
    # Every ground a settlement stands on is a terrace, not a slope: the docks, the quay and the port, the
    # town and the upland stand out of the relief entirely, so the relaxation bends round them and a house is
    # built on the flat. The hill and the balloon's field keep their relief, which is what they are for.
    # The coast and the terraces are two statements about the same compiled shapes, so they are merged onto
    # one entry apiece rather than one overwriting the other.
    shaped = outline()
    for shape_id, height, _ring in compiled_rings():
        if height in (DOCK, PORT, TOWN, BACK):
            shaped.setdefault(shape_id, {})["relief_scope"] = "exclude"

    return {
        "authors": ["Opus 5"],
        "created": "2026-08-29",
        "themeByHeight": {str(BASIN): "seabed", str(DOCK): "dock", str(QUAY): "quay", str(TOWN): "town",
                          str(HEAD): "head", str(RIDGE): "ridge", str(BACK): "back"},
        "mapTheme": "quay",
        "themes": THEMES,
        "shapePropsById": shaped,
        "addLayers": add_layers,
        # The spawn is a building rather than a bedrock box: a stamped two-storey hall with its own doorway.
        "roomStyles": {"spawn": "@sb-spawn"},
        # The ground the plan states is a set of plateaus; the relief is what makes it terrain. `reach` 26
        # shelves the quay into the basin over a beach rather than dropping it down a wall, and the marks
        # behind it roll the town — the two terraces excluded above stay flat inside it.
        "relief": {"team": {"base": TOWN, "reach": 26, "step": 1, "stairs": True, "marks": [
            {"id": "harbour-floor", "kind": "area", "h": BASIN,
             "ring": [[-50, -14], [50, -14], [50, 14], [-50, 14]]},
            {"id": "quay-line", "kind": "line", "h": QUAY,
             "points": [[-52, 20], [-10, 22], [30, 20], [96, 22]]},
            {"id": "town-roll", "kind": "area", "h": TOWN + 2,
             "ring": [[-70, 34], [-32, 32], [-28, 58], [-68, 62]]},
            {"id": "field-crown", "kind": "point", "at": [-80, -12], "h": HEAD + 3, "r": 22},
            {"id": "port-flat", "kind": "area", "h": PORT,
             "ring": [[46, 18], [98, 18], [98, 54], [46, 54]]},
            {"id": "hill-crown", "kind": "line", "h": RIDGE + 5,
             "points": [[-66, 76], [-16, 82], [22, 80], [66, 78]]},
            {"id": "back-flat", "kind": "area", "h": BACK,
             "ring": [[30, 58], [70, 58], [70, 94], [30, 94]]},
        ]}},
        "dressing": {"props": ROADS + [
            # The harbour: a filled ring at a stated level, on the ground layer so its bed is the seabed and
            # not the hull of the ship floating in it. `radius` on a pool is the shelf — how far in from the
            # shore the bed reaches full depth — so the water shallows against the quays.
            # **The ring is the basin piece, to the block.** A pool cuts its bed wherever the ground stands
            # above it, so a ring drawn wider than the water's own ground digs the quay it laps and floods
            # the field beside it: the harbour's edge is the plan's, not a rectangle around it.
            {"id": "harbour", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool",
             "points": [[-52, -16], [52, -16], [52, 16], [-52, 16]],
             "radius": 12, "depth": 6, "shore": 2, "shoreWander": True, "edge": 1.2, "level": WATER,
             "bank": {"kind": "voronoi", "seed": 3, "cellSize": 6, "bands": [
                 {"material": {"kind": "solid", "id": 13, "data": 0}, "thickness": 2},
                 {"material": {"kind": "solid", "id": 3, "data": 1}, "thickness": 1},
                 {"material": {"kind": "solid", "id": 12, "data": 0}, "thickness": 1}]}},
        ] + houses() + crates() + trees()},
        "voidEnforcement": True,
    }


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "specs/opus5-slipway"
    slug = os.path.basename(os.path.abspath(out))
    os.makedirs(out, exist_ok=True)

    add_layers, table = sculpted()
    json.dump(PLAN, open(f"{out}/{slug}.plan.json", "w"), indent=2)
    json.dump(finish(add_layers), open(f"{out}/{slug}.finish.json", "w"), indent=2)

    width = max(len(name) for name, _ in table)
    print(f"{'model':<{width}}  {'blocks':>7} {'layers':>7} {'shapes':>7} {'b/shape':>8}")
    for name, row in table:
        print(f"{name:<{width}}  {row['blocks']:>7} {row['layers']:>7} {row['shapes']:>7} "
              f"{row['blocks_per_shape']:>8}")
    print(f"\nspec written to {out}/ ({len(add_layers)} added layers, {len(HOUSES)} houses)")


if __name__ == "__main__":
    main()
