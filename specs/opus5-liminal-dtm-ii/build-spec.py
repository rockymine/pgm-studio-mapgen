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
HOLD_FLOOR   = 1                    # the stronghold slab: blocks 1..3, stood on at y4
HOLD_H       = 3
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
    # the Liminal Backroom Space: double smooth stone slab underfoot, smooth sandstone everywhere else
    "backroom": theme(solid(43, 8), solid(24, 2), solid(24, 2), surface_depth=1),
    # its ceiling, seen from underneath, which is the lid's fill
    "backroom-lid": theme(solid(24, 2), solid(24, 2), solid(24, 2), surface_depth=1),
    # the stair down: smooth sandstone the whole way, because a flight is one made thing
    "stair": theme(solid(24, 2), solid(24, 2), solid(24, 0), surface_depth=1),
    # a skyblock: grass, two of dirt, obsidian
    "skyblock": theme(layered(stack((solid(2), 1), (solid(3), 2), ending="handOver")),
                      solid(3), solid(49), surface_depth=3, bedrock=0),
    # the Town Wall: stone brick grained with cobble, one ground rather than two
    "wall": theme(noise(3, 11, 2, [solid(98), solid(4)]), noise(3, 11, 2, [solid(98), solid(4)]),
                  solid(98), surface_depth=1),
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


def box(prefix, x0, z0, x1, z1, floor, height, theme_key=None, op="add", over=False):
    shape = {"id": sid(prefix), "type": "rectangle", "operation": op,
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": height}
    if over:
        shape["override"] = True
    if theme_key:
        shape["theme"] = theme_key
    return shape


def island(ident, name, shapes, mirrors=True):
    return {"id": ident, "name": name, "mirrors": mirrors,
            "shapeIds": [s["id"] for s in shapes]}


def ring(prefix, x0, z0, x1, z1, thick, floor, height, theme_key, gaps=(), over=False):
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
        walls.append(box(prefix, lo, z0 - thick, hi, z0, floor, height, theme_key, over=over))
    for lo, hi in spans("s", x0 - thick, x1 + thick):
        walls.append(box(prefix, lo, z1, hi, z1 + thick, floor, height, theme_key, over=over))
    for lo, hi in spans("w", z0, z1):
        walls.append(box(prefix, x0 - thick, lo, x0, hi, floor, height, theme_key, over=over))
    for lo, hi in spans("e", z0, z1):
        walls.append(box(prefix, x1, lo, x1 + thick, hi, floor, height, theme_key, over=over))
    return walls


# ══ the undercroft ════════════════════════════════════════════════════════════════════════════
# One team's half; rot_180 fans it. The Poolroom sits under the river band nearest that spawn, a
# corridor runs east from it and a switchback stair climbs out of the corridor into the Pyramid
# through a well the plan leaves open by arrangement — a hole in a plan is a gap no piece covers,
# never a subtract, and a subtract on the ground layer with an add climbing through it is `SK13`.
POOL  = (56, -12, 96, 36)           # the Liminal Poolroom
CORR  = (96, 28, 108, 36)           # the corridor out of its east wall
WELL  = (100, 36, 108, 60)          # the stairwell, open to the sky until the Pyramid stands over it
BACK  = (8, 4, 56, 12)              # the Backroom Space, west out of the Poolroom
CROSS = (-8, -12, 8, 12)            # its middle, on the origin, which rot_180 maps onto itself
BACK_WALL_H = LID_FLOOR - UNDER_FLOOR            # 10 — a backroom wall stops under its own ceiling

under = []
under.append(box("pf", *POOL, UNDER_FLOOR, UNDER_H, "pool"))
under += ring("pw", *POOL, 2, UNDER_FLOOR, UNDER_WALL_H, "pool",
              gaps=[("e", 28, 36), ("w", 4, 12)])
under.append(box("cf", *CORR, UNDER_FLOOR, UNDER_H, "pool"))
under.append(box("cw", CORR[0], CORR[1] - 2, CORR[2], CORR[1], UNDER_FLOOR, UNDER_WALL_H, "pool"))
under.append(box("cw", CORR[2], CORR[1] - 2, CORR[2] + 2, CORR[3], UNDER_FLOOR, UNDER_WALL_H, "pool"))

# the Backroom stub, and the lid that gives it four courses of headroom rather than six
under.append(box("bf", *BACK, UNDER_FLOOR, UNDER_H, "backroom"))
under += ring("bw", *BACK, 2, UNDER_FLOOR, BACK_WALL_H, "backroom", gaps=[("e", 4, 12)])
# stopping two blocks short of the Poolroom's own wall, which stands to y17 and would otherwise be
# driven into the lid's own courses (`SK10`)
under.append(box("xf", *CROSS, UNDER_FLOOR, UNDER_H, "backroom"))
under += ring("xw", *CROSS, 2, UNDER_FLOOR, BACK_WALL_H, "backroom",
              gaps=[("e", 4, 12), ("w", -12, -4)])
lid = [box("bl", BACK[0] - 2, BACK[1] - 2, BACK[2] - 2, BACK[3] + 2, LID_FLOOR, LID_H, "backroom-lid"),
       box("bl", CROSS[0] - 2, CROSS[1] - 2, CROSS[2] + 2, CROSS[3] + 2, LID_FLOOR, LID_H, "backroom-lid")]

# ══ the stairwell ═════════════════════════════════════════════════════════════════════════════
# The stair is cut into the LANDMASS, not into a hole in it. A hole in the ground layer — drawn as
# a subtract or left as a gap the compiler declares a void — is refused the moment anything on a
# lower layer stands under it (`SK13`), so the well is stated the other way round: an override add
# overwrites whatever column it lands on, floor and all, so a tread at `floor 6` replaces the
# desert's `floor 18` outright and the shaft is the air left over it.
#
# Every tread is its own rectangle, so a course is a course rather than a rasterized guess — a ramp
# at one course a cell builds as treads of two, and a two-block rise costs a placed block. Two
# flights round a landing, so the well is sixteen blocks deep rather than twenty-four.
WX0, WZ0, WX1, WZ1 = WELL
TREADS = SURFACE - UNDER_TOP                     # 24 courses, one block of run each

add_shapes = []
for i in range(TREADS):
    add_shapes.append(box("st", WX0, WZ1 - 1 - i, WX1, WZ1 - i,
                          UNDER_FLOOR, SURFACE - i - UNDER_FLOOR, "stair", over=True))

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
    out, start = [], x_bank - into * SLIP_FALL
    for j in range(SLIP_FALL):
        edge = start + into * j
        x0, x1 = (edge, edge + 1) if into > 0 else (edge - 1, edge)
        out.append(box("sw", x0, SLIP_Z[0], x1, SLIP_Z[1],
                       GROUND_FLOOR, SURFACE - j - GROUND_FLOOR, "stair", over=True))
    return out


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
    return box("wl", x0, z0, x1, z1, GROUND_FLOOR, WALL_TOP - GROUND_FLOOR + 1, "wall", over=True)


add_shapes += [
    wall(-X_TOWN, Z_TOWN - WALL_T, X_TOWN, Z_TOWN),                       # the whole north face
    wall(X_TOWN - WALL_T, 0, X_TOWN, GATE[0]),                            # east, up to its gate
    wall(X_TOWN - WALL_T, GATE[1], X_TOWN, Z_TOWN - WALL_T),              # east, past it
    wall(-X_TOWN, 0, -X_TOWN + WALL_T, GATE[0]),                          # west, up to its gate
    wall(-X_TOWN, GATE[1], -X_TOWN + WALL_T, Z_TOWN - WALL_T),            # west, past it
]

# Up onto the wall-walk: nine treads against the inner face beside each gate, one course a block, so
# the climb walks both ways and costs nothing.
def wall_stair(x_face, into, z0):
    """`into` is the direction the village lies in from the wall's inner face."""
    out = []
    for j in range(WALL_TOP - SURFACE + 1):
        edge = x_face + into * j
        x0, x1 = (edge, edge + 1) if into > 0 else (edge - 1, edge)
        out.append(box("ws", x0, z0, x1, z0 + 4, GROUND_FLOOR,
                       WALL_TOP - j - GROUND_FLOOR + 1, "wall", over=True))
    return out


for face, into in ((X_TOWN - WALL_T, -1), (-X_TOWN + WALL_T, 1)):
    for z0 in (GATE[1] + 2, 10):
        add_shapes += wall_stair(face, into, z0)

# ══ the Village Well ══════════════════════════════════════════════════════════════════════════
# One on the whole map, on the origin, where the four roads meet. Two courses of smooth sandstone
# round a 2x2 mouth — the vanilla well's proportions without the water in it yet.
add_shapes += ring("wh", -1, -1, 1, 1, 2, GROUND_FLOOR, SURFACE - GROUND_FLOOR + 2, "stair", over=True)

# ══ the Small Hills ═══════════════════════════════════════════════════════════════════════════
# Six, three courses over the village on a 10x6 top, each stepped twice so it meets the sand rather
# than standing on it. Three are authored and rot_180 makes the other three.
HILLS = [(-34, -34), (14, -30), (56, 6)]
for cx, cz in HILLS:
    add_shapes.append(box("hl", cx - 5, cz - 3, cx + 5, cz + 3,
                          GROUND_FLOOR, SURFACE + 3 - GROUND_FLOOR, "hill", over=True))
    add_shapes += ring("hl", cx - 5, cz - 3, cx + 5, cz + 3, 3,
                       GROUND_FLOOR, SURFACE + 2 - GROUND_FLOOR, "hill", over=True)
    add_shapes += ring("hl", cx - 8, cz - 6, cx + 8, cz + 6, 3,
                       GROUND_FLOOR, SURFACE + 1 - GROUND_FLOOR, "hill", over=True)

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


SPAWN_ROOM = (104, 60, 124, 80)     # the Pyramid itself: a spawn-role piece sizes the stamped room,
                                    # and its rect is the protection, so it is a building and not a region
SPAWN_AT   = (112, 70)              # inside it, at the head of the stairwell
GOAL_TOWN  = (56, 32)               # the Village Monument, on the road in from the Pyramid
GOAL_POOL  = (80, 8)                # the Liminal Monument, over the Main Pool
GOAL_SKY   = (74, 22)               # the Skyblock Monument, on the island nearest the Pyramid


def piece(ident, x0, z0, x1, z1, surface):
    return {"id": ident, "role": "piece", "rect": cells(x0, z0, x1, z1), "surface": surface}


plan = {
    "plan": 1,
    "meta": {"name": "Liminal DTM II"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 48, "surface": SURFACE,
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
         "rect": cells(*SPAWN_ROOM), "surface": SURFACE},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "pyramid-spawn",
                    "at": [(SPAWN_AT[0] - SPAWN_ROOM[0]) / CELL, (SPAWN_AT[1] - SPAWN_ROOM[1]) / CELL],
                    "facing": "left"}],
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
            "pave": layered(stack((solid(24, 2), 1), (solid(24), 1), ending="repeat"))}


ROADS = [
    road("road-e", [[X_TOWN, 32], [48, 26], [20, 10], [4, 2]]),
    road("road-w", [[-X_TOWN, 32], [-48, 26], [-20, 10], [-4, 2]]),
]

# Three oaks a hill, and nothing else on them: a hill is a place to fight over, not a wood.
OAKS = [
    {"kind": "tree", "id": f"oak-{i}-{j}", "seed": 20 + 3 * i + j, "layer": "ground",
     "x": cx + dx, "z": cz + dz, "form": "template", "species": "oak", "height": 9}
    for i, (cx, cz) in enumerate(HILLS)
    for j, (dx, dz) in enumerate(((-3, -1), (1, 2), (4, -2)))
]

# ── the finish ────────────────────────────────────────────────────────────────────────────────
# `below` inserts at the head of the stack, so the two undercroft layers are listed top-down here
# and land bottom-up in the document: [under, lid, ground, sky].
finish = {
    "authors": ["Opus 5"],
    "created": "2026-08-26",
    "shapePropsByHeight": {
        str(SURFACE): {"floor": GROUND_FLOOR, "base_height": GROUND_H},
        str(RIVER):   {"floor": GROUND_FLOOR, "base_height": RIVER_H},
    },
    "themeByHeight": {str(SURFACE): "desert", str(RIVER): "riverbed"},
    "addShapes": add_shapes,
    "addLayers": [
        {"id": "lid",   "name": "Backroom ceiling", "base_y": 0, "below": True,
         "shapes": lid,   "islands": [island("lid", "Backroom ceiling", lid)]},
        {"id": "under", "name": "Undercroft",       "base_y": 0, "below": True,
         "shapes": under, "islands": [island("under", "Undercroft", under)]},
        {"id": "bridge", "name": "Bridges", "base_y": 0,
         "shapes": bridges, "islands": [island("bridge", "Bridges", bridges)]},
        {"id": "sky",   "name": "Skyblocks",        "base_y": 0,
         "shapes": sky,   "islands": [island("sky", "Skyblocks", sky)]},
    ],
    "goalLayers": {"destroyable-1": "ground", "destroyable-2": "under", "destroyable-3": "sky"},
    "mapTheme": "desert",
    "themes": THEMES,
    "dressing": {"props": ROADS + OAKS + [
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
