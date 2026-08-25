#!/usr/bin/env python3
"""Write the two authored documents for `opus5-aerie`.

    python3 specs/opus5-aerie/build-spec.py

**A small mixed board, 72 x 128, and there is no ground on it.** Seven crags hang in open sky: a
home crag at each end carrying a spawn, a **fold** carrying that team's wool, a **spike** carrying
its core, and one stone in the middle that belongs to nobody. Everything between them is void with a
build zone over it, so **bridging is the map** — the only way to anything is a bridge somebody built
while being shot at.

Three things this board is for.

**A core, which the studio has never been asked for here.** A destroyable is broken; a core is
*breached*, and what finishes it is the lava getting out and falling below its leak line. On a crag
in open sky there is no floor to catch it, so a hole punched anywhere near the edge of the casing is
the end of it — which is why the core stands in the middle of its crag with eight blocks of rock all
round, and a breach on the inward side only spills onto its own stone.

**`teamTint`.** The one material kind nothing here had used. It resolves to the owning team's colour
where a cell belongs to a team and to a stated neutral where it does not — so a band of it in the
fold's surface makes each wool crag quietly its team's colour, with one material and no per-team
theme.

**`rimEdges: "drop"`.** On a board of islands, every edge is a fall, and the rim is the bucket that
caps one. A crag's rim, its wall and its underside are the whole of what an opponent bridging toward
it can see, so they are what this board's themes spend their material on.

Output: `opus5-aerie.plan.json` and `opus5-aerie.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-aerie"

# ── the frame ─────────────────────────────────────────────────────────────────────────────────
CELL = 2
BOARD_X, BOARD_Z = 36, 64           # 72 x 128 blocks

# Each crag is drawn as a slab ten courses thick — floor at `top - 10`, so what hangs under it is
# two courses of bedrock and eight of rock, and a crag reads as a crag from below rather than as a
# column going down to nothing.
THICK = 10

# **Six crags and one strait, not nine crags and eight hops.** The first draft put a stone in the
# middle and left six-block gaps between everything, and the critic answered `G2` (a corridor under
# ten wide), `G5` (a hop outside 10..20) and `CT12` on every pair — a board of short hops is a board
# with no crossing in it, because a six-block gap is a running jump. What the gaps are is the map,
# so they are the numbers stated first here and the crags are fitted round them.
# **The core takes the crag nearest the strait and the wool the one behind it.** The other way round
# is what the first draft did, and the critic's `WL10` named it: a wool eight blocks behind the
# frontline is the first thing an attacker lands on, which is not a capture board. The core is the
# forward objective because a core is the one that wants to be contested — it cannot be carried
# anywhere, only breached — and the wool is the deep one, which is what a wool is for.
HOME = (-20, 44, 20, 64); HOME_Y = 30       # the spawn's crag
SPIKE = (-32, 12, -8, 28); SPIKE_Y = 34     # the core's: nearest the strait, and the highest here
FOLD = (8, 20, 32, 34); FOLD_Y = 26         # the wool's, behind it and off to the side

SPAWN_RECT = (-8, 46, 8, 62)
WOOL_RECT = (12, 22, 28, 32)
CORE_AT = (-20, 20)


# ── materials ─────────────────────────────────────────────────────────────────────────────────
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
    """A Worley diagram: bands are **depths inward from a cell boundary**, measured against the
    `F2 - F1` gap, and are not weights. The loop stops one short — **the last band takes the whole
    rest of the cell whatever depth it states** — so the material a player sees most of is the one
    written *last*, and everything before it is veining along the boundaries. Written the other way
    round, a wadi of sand with a seventh of gravel comes out as a gravel bed with sand along the
    cracks."""
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


def team_tint(block, neutral):
    """The owning team's colour where a cell belongs to one, and `neutral` where it does not. The
    data value is the team's, so one material paints both sides."""
    return {"kind": "teamTint", "blockId": block, "neutral": neutral}


STONE_B = solid(1, 0)
GRANITE = solid(1, 1)
ANDESITE = solid(1, 5)
GRASS = solid(2, 0)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
PODZOL = solid(3, 2)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
MOSSY_COBBLE = solid(48, 0)
CLAY_STAINED = 159                  # the block `teamTint` writes the team's damage value into
STONE_BRICK = solid(98, 0)
MOSSY_BRICK = solid(98, 1)

# What hangs under a crag, read down from the top of the face: turf and soil for two courses, then
# the rock, then the roots of it in cobble and gravel. Every theme here shares it, because the
# underside of one crag is the underside of all of them.
UNDERSIDE = layered(stack(
    (COARSE, 1),
    (DIRT, 2),
    (STONE_B, 3),
    (ANDESITE, 2),
    (noise(11, 5, 2, [STONE_B, COBBLE, GRAVEL]), 3),
    (MOSSY_COBBLE, 2),
))


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="drop", bedrock=8):
    """`bedrock` is stated **relative**: everything under the top `bedrock` painted blocks is
    bedrock, which on a ten-course crag is the bottom two. An absolute floor would write nothing at
    all here — there is no terrain down at y1 to write it into."""
    return {
        "bedrock": {"relative": True, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or COARSE, "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the ordinary crag: turf over soil over rock, with a lip of coarse dirt where it falls away
    "crag": theme(
        surface=layered(stack((noise(12, 8, 3, [GRASS, GRASS, COARSE]), 1), (DIRT, 2))),
        wall=UNDERSIDE, fill=STONE_B, rim=COARSE, surface_depth=3),

    # the fold: the same crag with one course of its team's colour in the turf, so a player on a
    # bridge can see whose wool they are coming at from a long way off
    "fold": theme(
        surface=layered(stack((noise(13, 7, 2, [GRASS, COARSE, GRASS]), 1),
                              (team_tint(CLAY_STAINED, PODZOL), 1), (DIRT, 1))),
        wall=UNDERSIDE, fill=STONE_B, rim=team_tint(CLAY_STAINED, COARSE), surface_depth=3),

    # the spike: bare, because nothing grows on the highest thing on a board of crags
    "spike": theme(
        surface=layered(stack((voronoi(14, 6, [(GRANITE, 1), (ANDESITE, 2), (STONE_B, 1)]), 2),
                              (STONE_B, 2))),
        wall=UNDERSIDE, fill=STONE_B, rim=ANDESITE, surface_depth=3),
}

# ── the crags ─────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def crag(prefix, box, top, theme_key, inset=3.0, seed=0):
    """One crag, as a polygon inset from its plan rectangle at the corners and bulged between them,
    so an island is an island rather than a box. Its floor is `THICK` under its top, which is what
    gives it an underside to paint."""
    x0, z0, x1, z1 = box
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    rx, rz = (x1 - x0) / 2, (z1 - z0) / 2
    ring = []
    for k in range(12):
        angle = 2 * math.pi * k / 12
        swell = 1.0 + 0.10 * math.sin(3 * angle + seed) + 0.06 * math.sin(5 * angle + 1.3 * seed)
        # a square-ish superellipse, so a crag keeps a usable middle instead of tapering to a point
        cosine, sine = math.cos(angle), math.sin(angle)
        shape = 1 / max(0.55, (abs(cosine) ** 3 + abs(sine) ** 3) ** (1 / 3))
        ring.append((round(cx + rx * swell * shape * cosine, 1),
                     round(cz + rz * swell * shape * sine, 1)))
    return {"id": sid(prefix), "type": "polygon", "operation": "add",
            "vertices": [[x, z] for x, z in ring],
            "floor": top - THICK, "base_height": THICK + 4, "theme": theme_key}


shapes = [
    crag("home", HOME, HOME_Y, "crag", seed=0.4),
    crag("spike", SPIKE, SPIKE_Y, "spike", seed=3.1),
    crag("fold", FOLD, FOLD_Y, "fold", seed=1.9),
]


# ── the relief ────────────────────────────────────────────────────────────────────────────────
def point(ident, x, z, h, r):
    return {"id": ident, "kind": "point", "at": [x, z], "h": h, "r": r}


def area(ident, x0, z0, x1, z1, h):
    return {"id": ident, "kind": "area",
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "h": h}


MARKS = [
    # the three tops, each level enough to stand and build on
    area("home", *HOME, HOME_Y),
    area("fold", *FOLD, FOLD_Y),
    area("spike", *SPIKE, SPIKE_Y),

    # one knoll on each, off-centre, so a crag has a side to stand behind
    point("home-knoll", -12, 54, HOME_Y + 3, 4),
    point("fold-knoll", 29, 31, FOLD_Y + 3, 3),
    point("spike-knoll", -12, 25, SPIKE_Y + 4, 3),
]

# **`base` is under every crag, and that is what shoulders them.** Each crag's top is stated by an
# `area` over its plan rectangle; the polygon is drawn wider than the rectangle, so the fringe
# between the two is unpinned and decays toward `base` — which, set low, means every crag's edge
# falls a course or two before the drop rather than running level to it.
#
# A `rim` mark would be the direct way to say that and is the wrong instrument here: it states **one
# height for every island in the relief**, and these three stand at 26, 30 and 34. It is for a board
# whose islands are level with each other.
RELIEF = {"*": {"base": HOME_Y - 6, "reach": 6, "step": 1, "stairs": False,
                "grain": {"amplitude": 0.6, "scale": 6, "seed": 5},
                "marks": MARKS}}


# ── what stands on it ─────────────────────────────────────────────────────────────────────────
def tree(ident, x, z, species, height, seed):
    return {"id": ident, "kind": "tree", "seed": seed, "x": x, "z": z,
            "form": "template", "species": species, "height": height}


def boulder(ident, x, z, size, seed, form="angular", mossy=False):
    return {"id": ident, "kind": "boulder", "seed": seed, "x": x, "z": z,
            "form": form, "size": size, "mossy": mossy,
            "rock": voronoi(15, 4, [(MOSSY_COBBLE, 1), (ANDESITE, 1), (STONE_B, 1)])}


def flora(ident, ring, coverage, seed, scale=7, fern=0.2, flower=0.2, tall=0.16):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 5, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "path", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


props = [
    # **Everything that stands stands on the home crag.** The other two are the size of what they
    # carry: a core's clearance takes most of the spike, and the fold is a room with two blocks of
    # margin round it — five props were declined `OB19` and `DR-KEEP` before this was accepted. A
    # bare rock spire and a walled pen are what those crags are, and turf is all they get.
    # The middle of the home crag is the spawn's and its keep-out reaches past the room's own walls,
    # so what stands here stands in the two strips either side of it.
    tree("rowan-a", 17, 48, "oak", 8, 201),
    tree("rowan-b", -17, 58, "birch", 7, 202),
    tree("rowan-c", 16, 61, "birch", 6, 203),

    boulder("crag-a", 13, 54, 2.4, 61, form="round", mossy=True),
    boulder("crag-b", -16, 52, 2.0, 62, form="cairn"),

    flora("turf-home", [(-18, 45), (18, 45), (18, 63), (-18, 63)], 0.5, 81),
    flora("turf-fold", [(9, 21), (31, 21), (31, 33), (9, 33)], 0.44, 82),
    flora("turf-spike", [(-31, 13), (-9, 13), (-9, 27), (-31, 27)], 0.16, 83,
          fern=0.06, flower=0.1, tall=0.05),

    # the two paths a team wears on its own crags, and nothing across the gaps, because there is
    # nothing across the gaps until somebody builds it
    stroke("home-path", [(0, 58), (-5, 51), (-12, 47), (-18, 45)], 2.2,
           voronoi(21, 4, [(GRAVEL, 1), (DIRT, 1), (COARSE, 1)]),
           style="solid", coverage=1.0, route=True, seed=31),
    stroke("fold-path", [(31, 22), (31, 30), (24, 33), (14, 33)], 2.0,
           voronoi(22, 4, [(GRAVEL, 1), (COARSE, 1)]), coverage=0.85, route=True, seed=32),
]


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
def cells(x0, z0, x1, z1):
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


plan = {
    "plan": 1,
    "meta": {"name": "Aerie"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": HOME_Y},
    "pieces": [
        # One piece per crag, split where a room has to abut ground rather than nest in it.
        {"id": "home-w", "role": "piece", "rect": cells(HOME[0], HOME[1], SPAWN_RECT[0], HOME[3]),
         "surface": HOME_Y},
        {"id": "home-s", "role": "piece",
         "rect": cells(SPAWN_RECT[0], HOME[1], SPAWN_RECT[2], SPAWN_RECT[1]), "surface": HOME_Y},
        {"id": "camp", "role": "spawn", "rect": cells(*SPAWN_RECT), "surface": HOME_Y},
        {"id": "home-e", "role": "piece", "rect": cells(SPAWN_RECT[2], HOME[1], HOME[2], HOME[3]),
         "surface": HOME_Y},

        {"id": "fold-w", "role": "piece", "rect": cells(FOLD[0], FOLD[1], WOOL_RECT[0], FOLD[3]),
         "surface": FOLD_Y},
        {"id": "fold-s", "role": "piece",
         "rect": cells(WOOL_RECT[0], FOLD[1], WOOL_RECT[2], WOOL_RECT[1]), "surface": FOLD_Y},
        {"id": "wool-room", "role": "wool-room", "rect": cells(*WOOL_RECT), "surface": FOLD_Y},
        {"id": "fold-n", "role": "piece",
         "rect": cells(WOOL_RECT[0], WOOL_RECT[3], WOOL_RECT[2], FOLD[3]), "surface": FOLD_Y},
        {"id": "fold-e", "role": "piece", "rect": cells(WOOL_RECT[2], FOLD[1], FOLD[2], FOLD[3]),
         "surface": FOLD_Y},

        {"id": "spike", "role": "piece", "rect": cells(*SPIKE), "surface": SPIKE_Y},
    ],
    # The four gaps, and they are the map: `deny(void)` closes everything outside a build area, so
    # what is drawn here is the whole list of places a bridge may be put.
    "zones": [
        {"id": "gap-home-fold", "rect": cells(FOLD[0], FOLD[3], FOLD[2], HOME[1]), "holes": []},
        {"id": "gap-home-spike", "rect": cells(SPIKE[0], SPIKE[3], SPIKE[2], HOME[1]), "holes": []},
        {"id": "gap-spike-fold", "rect": cells(SPIKE[2], SPIKE[1], FOLD[0], FOLD[3]), "holes": []},
        # the strait: twenty-four blocks of nothing, and the only way from one team's crags to the
        # other's. It is drawn once and is its own mirror image.
        {"id": "strait", "rect": cells(-BOARD_X + 2, -SPIKE[1], BOARD_X - 2, SPIKE[1]),
         "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [4, 4], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-room", "at": [4, 3]}],
        "cores": [
            # 5 x 5 x 5 of obsidian over a lava interior, floated six over the spike's crown. `leak`
            # is the level under it the lava has to reach; on a crag in open sky it reaches it by
            # falling off, so the casing stands in the middle of the crag with rock all round.
            {"id": "core-1", "at": [CORE_AT[0] / CELL, CORE_AT[1] / CELL],
             "size": 5, "height": 5, "shell": 1, "openTop": False, "float": 6, "leak": 5,
             "name": "The Eyrie"},
        ],
    },
}

finish = {
    "authors": ["Opus 5"],
    "addShapes": shapes,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "crag",
    "roomStyles": {"cage": "@ae-fold", "spawn": "@ae-lodge"},
    "dressing": {"props": props},
}


def write():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    print(f"board {2 * BOARD_X} x {2 * BOARD_Z}  crags home y{HOME_Y} fold y{FOLD_Y} "
          f"spike y{SPIKE_Y}, {THICK} thick")
    print(f"gaps: home-fold {HOME[1] - FOLD[3]}  home-spike {HOME[1] - SPIKE[3]}  "
          f"spike-fold {FOLD[0] - SPIKE[2]}  strait {2 * SPIKE[1]}")
    print(f"shapes {len(shapes)} · marks {len(MARKS)} · themes {len(THEMES)} · "
          f"props {len(props)} {kinds}")


if __name__ == "__main__":
    write()
