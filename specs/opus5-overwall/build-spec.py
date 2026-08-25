#!/usr/bin/env python3
"""Write the two authored documents for `opus5-overwall`.

    python3 specs/opus5-overwall/build-spec.py

A labyrinth of pillars and walls on a 22-block grid: every pillar is ten blocks square, every wall
between two of them is ten thick, and what is left over is **twelve blocks wide everywhere**, which
is the one measurement the whole board is built to.

The board is three slabs.

  `ground`  the floor the match is played on, rolling gently under a relief of its own. The wall
            footprints are re-drawn on it as `hold` shapes at one flat level, so the ground under
            every wall is exactly the level the wall stands on and the corridors roll between them.
  `walls`   the labyrinth itself, founded on that level, with a second relief solved over its own
            footprint — so the tops of the walls are landscape rather than a flat capping course,
            and the wood, the rock and the four houses up there are out of reach of anyone playing.
  `span`    two bridges, each landing on a pair of pillar tops the walls' relief holds flat, so a
            slab seats on them sharing one course and nothing is driven into anything.

The maze is a picture, below, and every rectangle, every route and every prop position is read off
it rather than typed — a coordinate written by hand is a coordinate that ends up inside a wall.

Output: `opus5-overwall.plan.json` and `opus5-overwall.finish.json` beside this file.
"""
import json, math, os
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-overwall"

# ── the grid ──────────────────────────────────────────────────────────────────────────────────
CELL = 2
PITCH = 22                          # node to node
WALL = 10                           # a pillar's side, and a wall's thickness
PASS = PITCH - WALL                 # 12, and it is 12 between every pair of solids on this board
HALF = WALL // 2

NODE_X = [-66, -44, -22, 0, 22, 44, 66]
NODE_Z = [77, 55, 33, 11]                       # north to south, as the picture reads
CELL_X = [-77, -55, -33, -11, 11, 33, 55, 77]
CELL_Z = [88, 66, 44, 22, 0]

EDGE_X = 83                         # the inner face of the side wall
COURT_WALL_Z = (94, 104)            # the wall the spawn court opens through
COURT_Z = (104, 124)
BACK_Z = (124, 132)
BOARD_X, BOARD_Z = 92, 132

FLOOR_Y = 12                        # the level every wall is founded on
WALL_TOP = 26                       # in the walls layer's own frame, whose base_y is FLOOR_Y
SPAN_Y = FLOOR_Y + WALL_TOP         # 38 — where the four bridge pillars are held flat

# ── the maze ──────────────────────────────────────────────────────────────────────────────────
# One character per grid position, north at the top and west at the left. Odd columns are the eight
# cell columns of `CELL_X`; even columns are the seven node columns of `NODE_X`, with the two side
# walls at either end. Odd lines are the five cell rows of `CELL_Z`; even lines are the four node
# rows of `NODE_Z`, with the spawn court's own wall as line 0. `#` is solid and `.` is open —
# including at a node, where a `.` takes the pillar out and merges the four cells round it into one
# court thirty-four blocks square. Two of those are what the objectives stand in.
#
# The last line is the seam the mirror closes, so it is a palindrome: it is drawn once and stands
# once, and the two halves of the board meet along the gallery it opens.
MAZE = """\
#######.#.#######
#.......#.......#
###.###.#.#...###
#.........#...#.#
###.#.###.#.###.#
#.........#.....#
#.#...#.#.###.#.#
#.....#.#.......#
###.#.#.#.###.###
#.....#...#.....#\
""".splitlines()

RIVER_COLUMN = 9                    # the one cell column no wall crosses, which the river runs down
GOAL_COURT = (44, 77)               # the pillar taken out at line 2, column 12
WOOL_COURT = (-44, 33)              # and the one at line 6, column 4
DOORS = (7, 9)                      # the two columns the court's wall opens through
COLUMNS, LINES = len(MAZE[0]), len(MAZE)


def col_x(index):
    """The block span of one grid column: a side wall, a cell column, or a node column."""
    if index == 0: return (-BOARD_X, -EDGE_X)
    if index == COLUMNS - 1: return (EDGE_X, BOARD_X)
    if index % 2: return (CELL_X[index // 2] - PASS // 2, CELL_X[index // 2] + PASS // 2)
    return (NODE_X[index // 2 - 1] - HALF, NODE_X[index // 2 - 1] + HALF)


def row_z(line):
    """The block span of one grid line, reading south from the court's wall."""
    if line == 0: return COURT_WALL_Z
    if line % 2: return (CELL_Z[line // 2] - PASS // 2, CELL_Z[line // 2] + PASS // 2)
    return (NODE_Z[line // 2 - 1] - HALF, NODE_Z[line // 2 - 1] + HALF)


def at(line, index):
    """The block centre of one grid position, whatever kind it is."""
    x0, x1 = col_x(index)
    z0, z1 = row_z(line)
    return ((x0 + x1) // 2, (z0 + z1) // 2)


def solid_rects():
    """Every rectangle the labyrinth stands on — one per `#`, merged along a line so the layer
    carries tens of shapes rather than hundreds."""
    out = []
    for line, text in enumerate(MAZE):
        z0, z1 = row_z(line)
        run = None
        for index, mark in enumerate(text + " "):
            if mark == "#":
                x0, x1 = col_x(index)
                run = (run[0], x1) if run else (x0, x1)
            elif run:
                out.append((run[0], z0, run[1], z1))
                run = None
    return out


SOLID = solid_rects()
# The side walls run the board's whole length rather than line by line, and the back wall closes the
# court. Drawn on the authored half only, like everything else.
SOLID += [(-BOARD_X, -6, -EDGE_X, BACK_Z[1]), (EDGE_X, -6, BOARD_X, BACK_Z[1]),
          (-BOARD_X, BACK_Z[0], BOARD_X, BACK_Z[1])]


def cells_open():
    return {(line, index) for line in range(1, LINES, 2) for index in range(1, COLUMNS, 2)
            if MAZE[line][index] == "."}


OPEN = cells_open()


def neighbours(cell):
    line, index = cell
    for dline, dindex in ((0, 2), (0, -2), (2, 0), (-2, 0)):
        nxt = (line + dline, index + dindex)
        gate = (line + dline // 2, index + dindex // 2)
        if nxt in OPEN and MAZE[gate[0]][gate[1]] == ".":
            yield nxt, gate


def walk(start, goal, avoid=frozenset()):
    """The shortest way through the maze from one cell to another, as the grid positions it passes
    — cell, gate, cell, gate — so a route drawn along it never crosses a wall. `avoid` keeps a route
    out of cells it has no business in: a stroke repaints the surface it crosses, and the surface of
    the river's corridor is the river."""
    came = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == goal: break
        for nxt, gate in neighbours(cell):
            if nxt in came or nxt in avoid: continue
            came[nxt] = (cell, gate)
            queue.append(nxt)
    if goal not in came: raise SystemExit(f"no way through the maze from {start} to {goal}")
    chain, cursor = [goal], goal
    while came[cursor] is not None:
        cell, gate = came[cursor]
        chain += [gate, cell]
        cursor = cell
    return list(reversed(chain))


def flood():
    seen, stack = {next(iter(OPEN))}, [next(iter(OPEN))]
    while stack:
        for nxt, _ in neighbours(stack.pop()):
            if nxt not in seen:
                seen.add(nxt); stack.append(nxt)
    return len(seen), len(OPEN)


def cell_of(x, z):
    """The grid cell a block position falls in, or None where it is inside a wall."""
    for line in range(1, LINES, 2):
        z0, z1 = row_z(line)
        if not z0 <= z < z1: continue
        for index in range(1, COLUMNS, 2):
            x0, x1 = col_x(index)
            if x0 <= x < x1: return (line, index)
    return None


def node_at(x, z):
    """The grid position of one node, by the block coordinates of its centre."""
    return (2 * (NODE_Z.index(z) + 1), 2 * (NODE_X.index(x) + 1))


def court_cells(node):
    """The four cells a court merges when its pillar is taken out."""
    line, index = node
    return [(line + dl, index + di) for dl in (-1, 1) for di in (-1, 1)]


DOOR_CELL = (1, DOORS[0])
GOAL_NODE, WOOL_NODE = node_at(*GOAL_COURT), node_at(*WOOL_COURT)
GOAL_CELL, WOOL_CELL = court_cells(GOAL_NODE)[0], court_cells(WOOL_NODE)[0]


def positions(kind):
    """Every grid position of one kind, as (line, index): `open` is a cell a player stands in,
    `pillar` is a node that was not taken out, `wall` is a segment between two nodes."""
    for line in range(LINES):
        for index in range(COLUMNS):
            if index in (0, COLUMNS - 1) or line == 0: continue
            mark = MAZE[line][index]
            if kind == "open" and line % 2 and index % 2 and mark == ".": yield (line, index)
            if kind == "pillar" and not line % 2 and not index % 2 and mark == "#": yield (line, index)
            if kind == "wall" and mark == "#" and (line % 2) != (index % 2): yield (line, index)


# ── materials ─────────────────────────────────────────────────────────────────────────────────
# One stone family and one green, and nothing else: stone, andesite and three faces of stone brick
# are the labyrinth; grass, dirt and coarse dirt are what grew on top of it; gravel and sand are the
# river. Every pattern here is a shape cut in those, not a fourth colour.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def stack(*pairs, ending="repeat"):
    return {"bands": [{"material": m, "thickness": t} for m, t in pairs], "ending": ending}


def layered(band_stack, axis="depth", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": band_stack}
    if beyond is not None:
        out["beyond"] = beyond
    return out


def noise(seed, scale, octaves, stops):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}


def voronoi(seed, cell_size, bands):
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


def wall_frame(edge, fill, angle=40, thickness=1):
    """An edge material inked wherever a wall turns sharply enough and along its top and bottom
    courses, panelling the fill inside it. It is the one pattern that reads as masonry rather than
    as a texture, because what it follows is the wall's own corners."""
    return {"kind": "wallFrame", "edge": edge, "fill": fill, "angle": angle, "thickness": thickness}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": even, "odd": odd}


STONE = solid(1, 0)
ANDESITE = solid(1, 5)
GRASS = solid(2, 0)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
COBBLE = solid(4, 0)
SAND = solid(12, 0)
GRAVEL = solid(13, 0)
MOSSY_COBBLE = solid(48, 0)
BRICK = solid(98, 0)
MOSSY_BRICK = solid(98, 1)
CRACKED_BRICK = solid(98, 2)
CHISELED_BRICK = solid(98, 3)


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="void", bedrock=1):
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or STONE, "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the labyrinth floor: worn ground, grass where nobody goes and coarse dirt where they do
    "floor": theme(
        surface=layered(stack((noise(11, 12, 3, [GRASS, GRASS, COARSE]), 1), (DIRT, 2))),
        wall=layered(stack((COARSE, 1), (STONE, 4), (ANDESITE, 2))),
        fill=STONE, surface_depth=3),

    # the walls, whose faces are what the palette is for: a stone-brick frame inked round every
    # corner and along the top and bottom courses, panelling a stone-and-andesite fill. Two blocks
    # in the panel and three faces of one brick in the frame — a pattern in one material family
    # rather than a colour scheme.
    "rampart": theme(
        # A crest is thin soil over rock, and saying so is also what makes the board legible from
        # above: with grass on the walls as well as the floor the whole maze reads as one lawn.
        surface=layered(stack((noise(12, 9, 3, [GRASS, COARSE, STONE]), 1), (COARSE, 1), (STONE, 4))),
        wall=wall_frame(
            edge=voronoi(13, 6, [(BRICK, 3), (MOSSY_BRICK, 1), (CRACKED_BRICK, 1)]),
            fill=layered(stack((noise(14, 7, 2, [STONE, STONE, ANDESITE]), 4),
                               (checker(2, STONE, ANDESITE), 1)), axis="inward"),
            angle=38, thickness=2),
        fill=STONE, surface_depth=2),

    # the court the spawn stands in: the same stone, laid rather than grown
    "court": theme(
        surface=layered(stack((voronoi(15, 5, [(COBBLE, 3), (BRICK, 2), (GRAVEL, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=layered(stack((COBBLE, 2), (STONE, 4))),
        fill=STONE, surface_depth=2),

    # the bridges: dressed brick, so what crosses over the maze reads as built and the maze reads
    # as grown into
    "deck": theme(
        surface=layered(stack((voronoi(16, 4, [(BRICK, 3), (CRACKED_BRICK, 1), (MOSSY_BRICK, 1)]), 2),
                              (STONE, 2))),
        wall=wall_frame(edge=CHISELED_BRICK, fill=voronoi(17, 5, [(BRICK, 4), (MOSSY_BRICK, 1)]),
                        angle=35, thickness=1),
        fill=STONE, surface_depth=2),
}

# ── the shapes ────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def rect(prefix, x0, z0, x1, z1, theme_key, floor=0, height=12, scope=None):
    shape = {"id": sid(prefix), "type": "rectangle", "operation": "add",
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": height, "theme": theme_key}
    if scope:
        shape["relief_scope"] = scope
    return shape


# On the ground layer the labyrinth's footprint is re-drawn as `hold` shapes at one flat level. A
# held shape pins its whole interior at the height it states and is applied after every other mark,
# so the floor under every wall is exactly `FLOOR_Y` and the corridors roll between them — which is
# what lets the walls layer be founded at `FLOOR_Y` sharing one course and nothing driven into
# anything.
ground_shapes = [rect("hold", x0, z0, x1, z1, "floor", height=FLOOR_Y, scope="hold")
                 for x0, z0, x1, z1 in SOLID]
ground_shapes.append(rect("court", -EDGE_X, COURT_Z[0], EDGE_X, COURT_Z[1], "court",
                          height=FLOOR_Y))

wall_shapes = [rect("wall", x0, z0, x1, z1, "rampart", height=WALL_TOP)
               for x0, z0, x1, z1 in SOLID]

# ── the two bridges ───────────────────────────────────────────────────────────────────────────
# Each lands on a pair of pillar tops the walls' relief holds flat at `SPAN_Y`, so the slab shares
# one course with what it stands on. The deck is tucked inside its parapets rather than drawn under
# them: two adds over one another on one layer is `SK9`, and the taller would take the shorter's
# ground outright.
BRIDGES = [
    {"id": "mill", "gate": (4, 9)},      # over the river, between the pillars at (0, 55) and (22, 55)
    {"id": "walk", "gate": (2, 7)},      # over the west corridor, between (-22, 77) and (0, 77)
]

span_shapes = []
for bridge in BRIDGES:
    line, index = bridge["gate"]
    _, gz = at(line, index)
    piers = [at(line, index - 1), at(line, index + 1)]
    for px, pz in piers:
        span_shapes.append(rect(f"pier-{bridge['id']}", px - HALF, pz - HALF, px + HALF, pz + HALF,
                                "deck", height=8))
    x0, x1 = col_x(index)
    span_shapes.append(rect(f"deck-{bridge['id']}", x0, gz - 3, x1, gz + 3, "deck",
                            floor=6, height=2))
    span_shapes.append(rect(f"kerb-{bridge['id']}", x0, gz - HALF, x1, gz - 3, "deck",
                            floor=6, height=5))
    span_shapes.append(rect(f"kerb-{bridge['id']}", x0, gz + 3, x1, gz + HALF, "deck",
                            floor=6, height=5))
    bridge["piers"] = piers


def island(ident, name, shapes):
    return {"id": ident, "name": name, "mirrors": True, "shapeIds": [s["id"] for s in shapes]}


# ── the relief ────────────────────────────────────────────────────────────────────────────────
def point(ident, x, z, h, r):
    return {"id": ident, "kind": "point", "at": [x, z], "h": h, "r": r}


def line_mark(ident, points, heights, width):
    return {"id": ident, "kind": "line", "points": [[x, z] for x, z in points],
            "h": heights, "r": width}


def area(ident, x0, z0, x1, z1, h):
    return {"id": ident, "kind": "area",
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "h": h}


# The river runs down that column and west along the seam, where it meets its own image and the two
# make one water.
RIVER = [(CELL_X[RIVER_COLUMN // 2], 92), (CELL_X[RIVER_COLUMN // 2], 62),
         (CELL_X[RIVER_COLUMN // 2], 34), (CELL_X[RIVER_COLUMN // 2], 3), (0, 0)]

FLOOR_MARKS = [
    # gentle, and few: the brief is elevation rather than hills, and every wall foot is pinned flat
    # anyway, so what these do is bow the middle of a corridor a little above its ends
    point("rise-w", -55, 66, 16, 5),
    point("rise-e", 55, 22, 17, 5),
    point("rise-n", -33, 88, 15, 5),
    point("rise-s", 33, 0, 15, 4),
    point("rise-far", 77, 66, 16, 4),
    point("dip-w", -77, 44, 12, 4),
    point("dip-e", 33, 88, 13, 4),
    point("dip-s", -55, 0, 12, 4),
    # the river's channel, a course under the ground it runs through, so the water reads as water
    line_mark("river", RIVER, [11, 10, 10, 11, 11], 3),
    # and the three places that have to be level
    area("court-floor", -EDGE_X, COURT_Z[0], EDGE_X, COURT_Z[1], 14),
    area("goal-floor", GOAL_COURT[0] - 12, GOAL_COURT[1] - 12,
         GOAL_COURT[0] + 12, GOAL_COURT[1] + 12, 13),
]

# The walls' own relief, solved over the labyrinth's footprint in that layer's frame. A ten-wide
# network has nowhere for a landform to sit, so what these do is make a wall's run rise and fall
# along its length: the marks stand on nodes and the relaxation carries the line between them.
WALL_MARKS = [
    point("crest-a", -66, 77, 30, 5), point("crest-b", -22, 33, 29, 5),
    point("crest-c", 66, 55, 30, 5), point("crest-d", 66, 11, 28, 4),
    point("crest-e", -44, 11, 27, 4), point("crest-f", 22, 99, 29, 5),
    point("low-a", -66, 33, 21, 5), point("low-b", 0, 33, 22, 4),
    point("low-c", 44, 33, 21, 4), point("low-d", -22, 77, 22, 4),
    point("low-e", 66, 77, 20, 4), point("low-f", -44, 99, 22, 4),
    # the two side walls and the court's wall carry a parapet, level along their run
    line_mark("parapet-w", [(-88, -6), (-88, 128)], [25], 6),
    line_mark("parapet-e", [(88, -6), (88, 128)], [25], 6),
    line_mark("parapet-court", [(-88, 99), (88, 99)], [24], 6),
    line_mark("parapet-back", [(-88, 128), (88, 128)], [24], 6),
] + [area(f"seat-{bridge['id']}-{k}", px - HALF, pz - HALF, px + HALF, pz + HALF, WALL_TOP)
     for bridge in BRIDGES for k, (px, pz) in enumerate(bridge["piers"])]

RELIEF_FLOOR = {"base": 14, "reach": 26, "step": 1, "stairs": False,
                "grain": {"amplitude": 0.9, "scale": 14, "seed": 5}, "marks": FLOOR_MARKS}
RELIEF_WALLS = {"base": 25, "reach": 14, "step": 1, "stairs": False,
                "grain": {"amplitude": 1.3, "scale": 7, "seed": 6}, "marks": WALL_MARKS}


# ── the routes ────────────────────────────────────────────────────────────────────────────────
# Walked rather than drawn: the shortest way the maze allows from the court's west door to each
# objective, and the loop the east door opens onto. Every waypoint is a cell or a gate, so no
# stroke crosses a wall and no tree is planted where a stroke already claims the ground.
def spine(chain):
    return [at(line, index) for line, index in chain]


ROUTE_GOAL = walk(DOOR_CELL, GOAL_CELL)
ROUTE_WOOL = walk(DOOR_CELL, WOOL_CELL)
RIVER_CELLS = frozenset(cell for cell in OPEN if cell[1] == RIVER_COLUMN)
ROUTE_EAST = [(1, DOORS[1]), (1, DOORS[1] + 1)] + walk((1, DOORS[1] + 2), (LINES - 1, COLUMNS - 2),
                                                       avoid=RIVER_CELLS)
ON_ROUTE = {step for chain in (ROUTE_GOAL, ROUTE_WOOL, ROUTE_EAST) for step in chain}


# ── what stands on it ─────────────────────────────────────────────────────────────────────────
def tree(ident, x, z, species, height, seed):
    return {"id": ident, "kind": "tree", "seed": seed, "x": x, "z": z,
            "form": "template", "species": species, "height": height}


def house(ident, x, z, width, depth, style, seed, front="negZ"):
    return {"id": ident, "kind": "house", "seed": seed, "front": front,
            "wings": [{"corners": [[x, z], [x + width, z + depth]]}], "style": style}


def boulder(ident, x, z, size, seed, form="angular", mossy=False):
    return {"id": ident, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": form, "size": size, "mossy": mossy,
            "rock": voronoi(18, 5, [(STONE, 2), (ANDESITE, 2), (COBBLE, 1), (MOSSY_COBBLE, 1)])}


def flora(ident, ring, coverage, seed, scale=9, fern=0.18, flower=0.16, tall=0.14):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 7, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "path", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


SPECIES = ["oak", "birch", "oak", "spruce"]
props = [
    # the river, down the one corridor no wall crosses and out along the seam into its own image
    {"id": "the-race", "kind": "water", "seed": 5, "form": "stream",
     "points": [[x, z] for x, z in RIVER],
     "radius": 2.2, "depth": 2, "edge": 0.7, "shore": 3, "shoreWander": True,
     "bank": voronoi(19, 4, [(GRAVEL, 3), (SAND, 1), (COARSE, 1)])},
]

# Inside: a tree in the middle of a cell no route passes through and neither objective stands in.
# A cell is twelve across, so one tree in it is a thing to walk round rather than a blockage.
# Three things take a cell out of the running. The two courts are the objectives'. The river's
# column is the channel's, and a tree standing in it is declined `DR-CLAIM`. And on the **seam row**
# only the east half is planted: that row is its own mirror image, so a tree at (-33, 0) and the
# image of a tree at (33, 0) land a block apart and one of them is declined.
KEEP = set(court_cells(GOAL_NODE)) | set(court_cells(WOOL_NODE)) | RIVER_CELLS
inside = [cell for cell in sorted(OPEN)
          if cell not in ON_ROUTE and cell not in KEEP
          and not (cell[0] == LINES - 1 and cell[1] < COLUMNS // 2)]
for k, (line, index) in enumerate(inside):
    x, z = at(line, index)
    props.append(tree(f"in-{k}", x + (k % 3) - 1, z + (k % 5) - 2,
                      SPECIES[k % len(SPECIES)], 9 + (k % 4), 200 + k))

# Up top: the wood, the loose rock and the four houses, all on wall and pillar tops, all out of
# reach. The positions come off the picture, so nothing here can be standing in a corridor.
PILLARS = [pos for pos in positions("pillar")]
WALL_RUNS = [pos for pos in positions("wall")]
BRIDGE_SEATS = {bridge["gate"] for bridge in BRIDGES}
BRIDGE_PIERS = {(line, index + d) for line, index in BRIDGE_SEATS for d in (-1, 1)}

HOUSES = [pos for k, pos in enumerate(PILLARS) if pos not in BRIDGE_PIERS and k % 5 == 2][:4]
for k, pos in enumerate(HOUSES):
    x, z = at(*pos)
    props.append(house(f"stilt-{k}", x - 4, z - 5, 7, 9, "@ow-stilt", 11 + k,
                       front="posZ" if k % 2 else "negZ"))

for k, pos in enumerate(pillar for pillar in PILLARS
                        if pillar not in BRIDGE_PIERS and pillar not in HOUSES):
    x, z = at(*pos)
    if k % 2:
        props.append(tree(f"up-{k}", x, z, SPECIES[(k + 1) % len(SPECIES)], 10 + (k % 3), 300 + k))
    else:
        props.append(boulder(f"crag-{k}", x, z, 2.2 + 0.3 * (k % 4), 400 + k,
                             form=("cairn", "outcrop", "angular", "round")[k % 4],
                             mossy=k % 3 == 0))

for k, pos in enumerate(WALL_RUNS):
    # Not the row under the court's wall: the ground in front of a door is kept clear, and the
    # keep-out is a mask in plan, so a prop on the wall top over it is declined `DR-KEEP` too.
    if k % 3 or pos[0] == 1: continue
    x, z = at(*pos)
    props.append(tree(f"run-{k}", x, z, SPECIES[k % len(SPECIES)], 9 + (k % 3), 500 + k))

# The side walls and the court's wall are long enough to carry a run of their own.
for k, z in enumerate(range(6, 126, 24)):
    props.append(tree(f"edge-w-{k}", -88, z, SPECIES[k % len(SPECIES)], 10 + (k % 3), 600 + k))
    props.append(boulder(f"edge-e-{k}", 88, z + 12, 2.4 + 0.2 * (k % 3), 620 + k,
                         form="outcrop", mossy=k % 2 == 0))

props.append(flora("turf", [(-BOARD_X, -6), (BOARD_X, -6), (BOARD_X, BACK_Z[1]),
                            (-BOARD_X, BACK_Z[1])], 0.3, 81,
                   scale=8, fern=0.22, flower=0.14, tall=0.16))

TRACK = voronoi(21, 4, [(COARSE, 2), (DIRT, 2), (GRAVEL, 1)])
props += [
    stroke("path-goal", spine(ROUTE_GOAL)[:-1], 3.0, TRACK,
           style="solid", coverage=1.0, route=True, seed=31),
    stroke("path-wool", spine(ROUTE_WOOL)[:-1], 2.4, TRACK, coverage=0.85, route=True, seed=32),
    stroke("path-east", spine(ROUTE_EAST), 2.4, TRACK, coverage=0.8, route=True, seed=33),
]


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


WOOL_RECT = (WOOL_COURT[0] - 8, WOOL_COURT[1] - 9, WOOL_COURT[0] + 8, WOOL_COURT[1] + 7)
SPAWN_RECT = (-8, 106, 8, 122)
SPAWN = ((SPAWN_RECT[0] + SPAWN_RECT[2]) // 2, (SPAWN_RECT[1] + SPAWN_RECT[3]) // 2)

plan = {
    "plan": 1,
    "meta": {"name": "Overwall"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": FLOOR_Y},
    "pieces": [
        # The floor, in rectangles that tile it: the maze, the wool room inside it, the court either
        # side of the spawn, and the spawn. The labyrinth is not in the plan at all — it is a slab
        # standing on this.
        # The maze floor is four rectangles rather than one because the wool room has to **abut**
        # ground rather than sit inside it: a room nested in a piece has no seam, and the plan tier
        # answers `WX6` — the room is unreachable, with no land edge to enter it by.
        {"id": "maze-w", "role": "piece",
         "rect": cells(-BOARD_X, 0, WOOL_RECT[0], COURT_Z[0]), "surface": FLOOR_Y},
        {"id": "maze-s", "role": "piece",
         "rect": cells(WOOL_RECT[0], 0, WOOL_RECT[2], WOOL_RECT[1]), "surface": FLOOR_Y},
        {"id": "wool-room", "role": "wool-room", "rect": cells(*WOOL_RECT), "surface": FLOOR_Y},
        {"id": "maze-n", "role": "piece",
         "rect": cells(WOOL_RECT[0], WOOL_RECT[3], WOOL_RECT[2], COURT_Z[0]), "surface": FLOOR_Y},
        {"id": "maze-e", "role": "piece",
         "rect": cells(WOOL_RECT[2], 0, BOARD_X, COURT_Z[0]), "surface": FLOOR_Y},
        {"id": "court-w", "role": "piece",
         "rect": cells(-BOARD_X, COURT_Z[0], SPAWN_RECT[0], BACK_Z[1]), "surface": FLOOR_Y},
        {"id": "court-e", "role": "piece",
         "rect": cells(SPAWN_RECT[2], COURT_Z[0], BOARD_X, BACK_Z[1]), "surface": FLOOR_Y},
        {"id": "court-s", "role": "piece",
         "rect": cells(SPAWN_RECT[0], COURT_Z[0], SPAWN_RECT[2], SPAWN_RECT[1]), "surface": FLOOR_Y},
        {"id": "camp", "role": "spawn", "rect": cells(*SPAWN_RECT), "surface": FLOOR_Y},
        {"id": "court-n", "role": "piece",
         "rect": cells(SPAWN_RECT[0], SPAWN_RECT[3], SPAWN_RECT[2], BACK_Z[1]), "surface": FLOOR_Y},
    ],
    # The mid band: the twelve-wide gallery the seam opens, which is where the two halves meet and
    # the one place on the board worth building in. It is also what makes the plan tier's frontline
    # exist at all — `Frontline` is the pieces a build zone touches, and with no zone `SP1` reads
    # every wool as reachable only through a spawn.
    "zones": [{"id": "mid-band", "rect": cells(-BOARD_X, -6, BOARD_X, 6), "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [4, 4], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-room", "at": [4, 4]}],
        "destroyables": [
            {"id": "destroyable-1", "at": [GOAL_COURT[0] / CELL, GOAL_COURT[1] / CELL],
             # `DC3`: a cube-3 is 27 blocks and obsidian is worth at most 3 of them, so a cube
             # asked for in obsidian is built in ender stone and the document is the thing that
             # was wrong. Stated as what it is.
             "style": "cube-3", "materials": "ender stone", "float": 3, "name": "The Keystone"},
        ],
    },
}

finish = {
    "authors": ["Opus 5"],
    "addShapes": ground_shapes,
    "addLayers": [
        {"id": "walls", "name": "The labyrinth", "base_y": FLOOR_Y,
         "shapes": wall_shapes, "islands": [island("walls", "The labyrinth", wall_shapes)]},
        {"id": "span", "name": "The bridges", "base_y": SPAN_Y,
         "shapes": span_shapes, "islands": [island("span", "The bridges", span_shapes)]},
    ],
    "relief": {"*": RELIEF_FLOOR, "walls": RELIEF_WALLS},
    "themes": THEMES,
    "mapTheme": "floor",
    "roomStyles": {"cage": "@ow-cage", "spawn": "@ow-gate"},
    "dressing": {"props": props},
}


def write():
    walked, total = flood()
    if walked != total:
        raise SystemExit(f"the maze reaches {walked} of {total} cells — a court is sealed off")
    for chain in (ROUTE_GOAL, ROUTE_WOOL, ROUTE_EAST):
        for line, index in chain:
            if MAZE[line][index] != ".":
                raise SystemExit(f"a route runs through the wall at line {line}, column {index}")
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"maze {COLUMNS}x{LINES} · every passage {PASS} wide · {walked}/{total} cells reachable")
    print(f"board {2 * BOARD_X} x {2 * BOARD_Z}  spawn {SPAWN}  goal {GOAL_COURT}  "
          f"wool {WOOL_COURT}  routes {len(ROUTE_GOAL)}/{len(ROUTE_WOOL)}/{len(ROUTE_EAST)} steps")
    print(f"ground {len(ground_shapes)} · walls {len(wall_shapes)} · span {len(span_shapes)} · "
          f"marks {len(FLOOR_MARKS)}/{len(WALL_MARKS)} · themes {len(THEMES)} · "
          f"props {len(props)} {kinds}")


if __name__ == "__main__":
    write()
