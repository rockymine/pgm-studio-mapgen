#!/usr/bin/env python3
"""Write the two authored documents for `opus5-rimegarth`.

    python3 specs/opus5-rimegarth/build-spec.py

**A regular capture-the-wool board, and the plan under it was composed rather than drawn.**
`composed.plan.json` beside this file is `GET /api/compose?players=10&symmetry=rot_180&seed=26`
pinned verbatim — the composer's own board, score 0 on every hard term, structure
`{wools: [donut], hub: twin, frontline: bar}`. What this script does is everything a composed plan
does not carry: it is flat at one surface, it has no walls, and it has no world.

**The donut is why this seed was picked.** A composed wool box is normally a bar or an L; once in
forty-eight it comes out as a **ring** — five pieces enclosing a hole, with the wool room closing the
far corner of it. Read as a place that is a walled garth: a yard you can only go round, with the wool
in the byre at the far side of it and the middle of it open. The hole is void in the plan, and the
one thing here that changes the composer's geometry is filling it — a pond five courses down, so the
garth has a middle rather than a shaft.

Everything else is added on top of what was composed: the relief that lifts the hall over the green,
the four themes, the approach wall across the garth's near gate, and what stands on it.

Output: `opus5-rimegarth.plan.json` and `opus5-rimegarth.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-rimegarth"
COMPOSED = json.load(open(os.path.join(HERE, "composed.plan.json")))

CELL = COMPOSED["globals"]["cell"]           # 5
SURFACE = 12                                 # the level the composed board is lifted to


def blocks(piece_id):
    """One composed piece's rectangle in blocks — the plan states cells."""
    x, z, w, h = next(p for p in COMPOSED["pieces"] if p["id"] == piece_id)["rect"]
    return (x * CELL, z * CELL, (x + w) * CELL, (z + h) * CELL)


# The composed board, read once and named. Nothing below re-types a coordinate.
GATE = blocks("spawn-room")                  # x -50..-40, z 40..50
HALL = blocks("hub-t1")                      # x -35..  0, z 40..50
SOLAR = blocks("hub-t2")                     # x -35..-25, z 30..40
BUTTERY = blocks("hub-t3")                   # x -15..  0, z 30..40
GREEN = blocks("frontline-t1")               # x -15.. 15, z 10..30
NECK = blocks("wool-a-t4")                   # x -25..  0, z 50..60
RING_W = blocks("wool-a-t1")                 # x -25..-15, z 60..105
RING_S = blocks("wool-a-t2")                 # x -15..  0, z 60.. 70
RING_E = blocks("wool-a-t5")                 # x   0.. 10, z 60.. 95
RING_N = blocks("wool-a-t3")                 # x -15..  0, z 95..105
BYRE = blocks("wool-a-room")                 # x   0.. 10, z 95..105

RING = (RING_W[0], RING_S[1], RING_E[2], RING_N[3])          # the garth's outer bound
GARTH = (RING_S[0], RING_S[3], RING_S[2], RING_E[3])         # the hole in it: x -15..0, z 70..95
POOL_Y = SURFACE - 5
GREEN_Y = SURFACE - 2

# Every piece's rectangle, so nothing below is placed on ground that is not there. A composed board
# **is** its pieces — there is no landscape round them, only void — and a coordinate typed by eye
# lands off the map about a third of the time. `write()` refuses to emit a document that does.
GROUND = [blocks(p["id"]) for p in COMPOSED["pieces"]]


def on_ground(x, z, margin=2):
    return any(x0 + margin <= x <= x1 - margin and z0 + margin <= z <= z1 - margin
               for x0, z0, x1, z1 in GROUND)


MID = COMPOSED["zones"][0]["rect"]
GILL = (MID[0] * CELL, MID[1] * CELL, (MID[0] + MID[2]) * CELL, (MID[1] + MID[3]) * CELL)


# ── materials ─────────────────────────────────────────────────────────────────────────────────
# Winter, and two greys: snow and ice for what the weather left, stone and cobble for what was
# built out of the hill, spruce for what was cut. The only colour on the board is each team's own,
# and it is written by one material.
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
    """Bands are depths inward from a cell boundary, and **the last one takes the rest of the
    cell** — so the ground a player sees most of is written last and the rest is veining."""
    return {"kind": "voronoi", "seed": seed, "cellSize": cell_size, "rise": 0,
            "bands": [{"material": m, "thickness": t} for m, t in bands]}


def team_tint(block, neutral):
    """The owning team's colour where a cell belongs to one, the neutral where it does not."""
    return {"kind": "teamTint", "blockId": block, "neutral": neutral}


STONE = solid(1, 0)
GRANITE = solid(1, 1)
DIORITE = solid(1, 3)
ANDESITE = solid(1, 5)
DIRT = solid(3, 0)
COARSE = solid(3, 1)
PODZOL = solid(3, 2)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
MOSSY_COBBLE = solid(48, 0)
ICE = solid(79, 0)
SNOW = solid(80, 0)
PACKED_ICE = solid(174, 0)
STONE_BRICK = solid(98, 0)
MOSSY_BRICK = solid(98, 1)
CLAY_STAINED = 159
CLAY_WHITE = solid(159, 0)

# What the board is cut out of, seen on every face that drops into the gill: snow and frozen soil
# over the hill's own stone.
SECTION = layered(stack(
    (SNOW, 1), (COARSE, 1), (PODZOL, 1),
    (STONE, 3), (ANDESITE, 2),
    (noise(11, 5, 2, [STONE, COBBLE, GRAVEL]), 3),
    (GRANITE, 2),
))


def theme(surface, wall, fill, surface_depth=3, rim=None, rim_edges="drop", bedrock=1):
    return {
        "bedrock": {"relative": False, "value": bedrock},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim or COBBLE, "depth": 1, "enabled": rim is not None},
        "surface": {"material": surface, "depth": surface_depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


THEMES = {
    # the heath the whole board is cut from: snow lying on frozen ground, thin where it is walked
    "heath": theme(
        surface=layered(stack((noise(12, 9, 3, [COARSE, SNOW, SNOW]), 1), (PODZOL, 1), (DIRT, 1))),
        wall=SECTION, fill=STONE, rim=COBBLE, surface_depth=3),

    # the hall's yard and the garth's: trodden through to the cobble that was laid under it
    "yard": theme(
        surface=layered(stack((voronoi(13, 5, [(SNOW, 1), (MOSSY_COBBLE, 1), (COBBLE, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=SECTION, fill=STONE, rim=STONE_BRICK, surface_depth=3),

    # the green before the gill, and **the one place the board says whose it is**: `teamTint` caps
    # the drop, so the lip a team defends is that team's colour seen from the other side of the void
    "green": theme(
        surface=layered(stack((noise(14, 7, 3, [SNOW, SNOW, COARSE]), 1), (COARSE, 1), (DIRT, 1))),
        wall=SECTION, fill=STONE,
        rim=team_tint(CLAY_STAINED, CLAY_WHITE), surface_depth=3),

    # the pond in the middle of the garth: ice at its edges over the gravel it was dug into
    "pool": theme(
        surface=layered(stack((voronoi(15, 4, [(PACKED_ICE, 1), (GRAVEL, 2), (ICE, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=layered(stack((PACKED_ICE, 1), (GRAVEL, 2), (STONE, 4))),
        fill=STONE, rim=PACKED_ICE, surface_depth=2),
}

# ── the shapes ────────────────────────────────────────────────────────────────────────────────
_ids = {}


def sid(prefix):
    _ids[prefix] = _ids.get(prefix, 0) + 1
    return f"{prefix}{_ids[prefix]}"


def rect(prefix, box, theme_key, floor=0, height=SURFACE):
    x0, z0, x1, z1 = box
    return {"id": sid(prefix), "type": "rectangle", "operation": "add",
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": height, "theme": theme_key}


# **A composed plan compiles to one merged polygon and a `subtract`**, and the subtract is what cuts
# the garth's hole out of it. A subtract beats every add on its layer whatever order they are in, so
# an `addShapes` rectangle over the hole draws nothing at all — the pond is a **slab of its own**,
# stated `below` the compiled ground so the painter reaches it first, filling exactly the rectangle
# the subtract took and no more.
pool = [rect("pool", GARTH, "pool", height=POOL_Y + 1)]

shapes = [
    # paint scopes over what is already there
    rect("t", (RING[0], RING[1], RING[2], RING[3]), "yard"),
    rect("t", (SOLAR[0], SOLAR[1], BUTTERY[2], HALL[3]), "yard"),
    rect("t", NECK, "yard"),
    rect("t", GREEN, "green"),
]


# ── the relief ────────────────────────────────────────────────────────────────────────────────
def point(ident, x, z, h, r):
    return {"id": ident, "kind": "point", "at": [x, z], "h": h, "r": r}


def area(ident, box, h):
    x0, z0, x1, z1 = box
    return {"id": ident, "kind": "area",
            "ring": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "h": h}


MARKS = [
    # the garth, level, because a yard is. Nothing here states the pond: it is a slab on its own
    # layer and flat by construction, which is what the bottom of one is.
    area("garth-floor", RING, SURFACE),

    # the green two courses under the hall, with the seam left unpinned so the ground ramps rather
    # than steps — the only slope on a board that is otherwise a floor
    area("green", GREEN, GREEN_Y),

    # and a hand of low swells so the flat is not flat: on the hall's yard, on the neck, and one
    # behind the gatehouse
    point("hall-swell", -22, 45, SURFACE + 2, 6),
    point("neck-swell", -12, 55, SURFACE + 1, 5),
    point("gate-rise", -46, 45, SURFACE + 2, 5),
    point("garth-swell", -20, 82, SURFACE + 1, 5),
    point("green-dip", 6, 18, GREEN_Y - 1, 5),
]

RELIEF = {"*": {"base": SURFACE, "reach": 14, "step": 1, "stairs": False,
                "grain": {"amplitude": 0.6, "scale": 8, "seed": 5},
                "marks": MARKS}}


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
            "rock": voronoi(16, 4, [(MOSSY_COBBLE, 1), (ANDESITE, 1), (STONE, 1)])}


def flora(ident, ring, coverage, seed, scale=8, fern=0.24, flower=0.1, tall=0.2):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 6, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "path", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


TROD = voronoi(21, 4, [(SNOW, 1), (GRAVEL, 1), (COARSE, 1)])

# The three roads, stated once and read by both the strokes and the scatter below.
STREET = [(-44, 45), (-30, 46), (-14, 44), (-6, 38), (-2, 28), (0, 16), (0, 11)]
GARTH_W = [(-14, 52), (-20, 58), (-20, 74), (-20, 92), (-14, 100), (-2, 100)]
GARTH_E = [(-10, 54), (-6, 64), (4, 68), (5, 84), (5, 96)]
# **A road's standoff is measured to its paved cells, not its centreline**, so what a prop has to
# clear is the stroke's own radius plus the standoff its kind states — three blocks for a tree, two
# for a boulder. Each road carries its radius here and the scatter adds four.
ROADS = ((STREET, 3.0), (GARTH_W, 2.4), (GARTH_E, 2.2))

# The approach wall's interface, which is kept clear the way a doorway is.
WALL_SEAM = (RING_S[0] - 4, NECK[3] - 8, RING_S[2] + 4, RING_S[1] + 8)

# The two buildings, likewise: corner, corner.
HOUSES = [("hall", (-14, 41, 13, 7), "@rg-hall", "negZ"),
          ("solar", (-33, 32, 7, 7), "@rg-hall", "posZ")]


def _near_segment(x, z, a, b):
    (ax, az), (bx, bz) = a, b
    dx, dz = bx - ax, bz - az
    span = dx * dx + dz * dz
    t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (z - az) * dz) / span))
    return math.hypot(x - (ax + t * dx), z - (az + t * dz))


def clear_spot(x, z):
    """Whether a prop may stand here. **Every rule the dressing pass declines on, asked before the
    document is written** — the board is corridors ten blocks wide with a road down each of them,
    so a coordinate that merely looks free almost never is."""
    if not on_ground(x, z, margin=3):
        return False
    for road, radius in ROADS:
        for a, b in zip(road, road[1:]):
            if _near_segment(x, z, a, b) < radius + 4:
                return False
    if WALL_SEAM[0] <= x <= WALL_SEAM[2] and WALL_SEAM[1] <= z <= WALL_SEAM[3]:
        return False
    for _, (hx, hz, hw, hd), _, _ in HOUSES:
        if hx - 4 <= x <= hx + hw + 4 and hz - 4 <= z <= hz + hd + 4:
            return False
    for room in (GATE, BYRE):                       # the two doors, and the ground kept clear of them
        if room[0] - 15 <= x <= room[2] + 15 and room[1] - 15 <= z <= room[3] + 15:
            return False
    if GARTH[0] - 3 <= x <= GARTH[2] + 3 and GARTH[1] - 3 <= z <= GARTH[3] + 3:
        return False                                 # the pond and its bank
    return True


def scatter(count, apart=8):
    """The clear spots, taken in a fixed order and thinned to `apart` blocks between them. No
    randomness: the same board always dresses the same way."""
    picks = []
    for z in range(10, 106):
        for x in range(-50, 16):
            if not clear_spot(x, z):
                continue
            if any(math.hypot(x - px, z - pz) < apart for px, pz in picks):
                continue
            picks.append((x, z))
    return picks[:count]


SPOTS = scatter(20)

props = [
    # the pond, cut into the pan the relief already flattened
    # The pond. **A water prop fills its own band and does not spread to a level pan**, so the band
    # is the pond: a centreline down the middle of the hole at a radius that leaves a block and a
    # half of bank inside the yard's five-course wall.
    {"id": "the-stank", "kind": "water", "seed": 5, "form": "canal",
     "points": [[(GARTH[0] + GARTH[2]) / 2, GARTH[1] + 9],
                [(GARTH[0] + GARTH[2]) / 2, GARTH[3] - 9]],
     "radius": 6.0, "depth": 2, "edge": 0.3, "shore": 1, "shoreWander": False,
     "bank": voronoi(17, 4, [(PACKED_ICE, 1), (GRAVEL, 1), (COBBLE, 1)])},

    # **The hall on the hub and its solar wing stepped off it, and nothing in the garth.** The ring
    # is ten blocks wide the whole way round — a corridor, not a yard — so a house in it is a house
    # standing on the only route there is.
]
props += [house(ident, x, z, w, d, style, 11 + k, front=front)
          for k, (ident, (x, z, w, d), style, front) in enumerate(HOUSES)]

# Spruce and stone in the spots the scatter found, alternating, which is every place on this board
# that is on ground, off the roads, clear of the buildings and out of both doorways' approaches.
props += [
    tree(f"fir-{k}", x, z, "spruce", 9 + (k % 4), 200 + k) if k % 2 == 0
    else boulder(f"stone-{k}", x, z, 2.0 + 0.2 * (k % 4), 60 + k,
                 form=("cairn", "round", "outcrop", "angular")[k % 4], mossy=k % 3 == 0)
    for k, (x, z) in enumerate(SPOTS)
]

props += [

    flora("heath-turf", [(-50, 30), (15, 30), (15, 60), (-50, 60)], 0.28, 81),
    flora("garth-turf", [(RING[0], RING[1]), (RING[2], RING[1]),
                         (RING[2], RING[3]), (RING[0], RING[3])], 0.2, 82,
          fern=0.3, flower=0.06, tall=0.14),
    flora("green-turf", [(GREEN[0], GREEN[1]), (GREEN[2], GREEN[1]),
                         (GREEN[2], GREEN[3]), (GREEN[0], GREEN[3])], 0.16, 83,
          fern=0.1, flower=0.04, tall=0.1),

    # the one road: out of the gatehouse, down the hall's length, over the green to the gill's lip
    stroke("street", STREET, ROADS[0][1], TROD, style="solid", coverage=1.0, route=True, seed=31),
    # and the way into the garth, which forks round the pond because a ring is what it is
    stroke("garth-w", GARTH_W, ROADS[1][1], TROD, coverage=0.85, route=True, seed=32),
    stroke("garth-e", GARTH_E, ROADS[2][1], TROD, coverage=0.8, route=True, seed=33),

    # and two that are paint rather than a way: snow drifted into the lee of the garth's walls, and
    # the green worn through to the stone under it where a board this narrow is walked most
    stroke("drift", [(RING[0] + 3, RING[1] + 3), (RING[0] + 3, RING[3] - 3),
                     (RING[2] - 3, RING[3] - 3), (RING[2] - 3, RING[1] + 3)], 3.0, SNOW,
           style="worn", coverage=0.45, seed=34),
    stroke("tread", [(GREEN[0] + 4, GREEN[3] - 4), (0, GREEN[1] + 8), (GREEN[2] - 4, GREEN[3] - 4)],
           5.0, voronoi(22, 4, [(SNOW, 1), (COBBLE, 1), (GRAVEL, 1)]),
           style="worn", coverage=0.35, seed=35),
]


# ── the plan ──────────────────────────────────────────────────────────────────────────────────
# The composed document, with three things added and nothing moved: the surface it is lifted to,
# the approach wall, and a name.
plan = json.loads(json.dumps(COMPOSED))
plan["meta"] = {"name": "Rimegarth"}
plan["globals"]["surface"] = SURFACE
# `walls` is always empty on a composed board — a defence wall is authored, never composed. This one
# bars the garth's near gate, so the way to the wool is round the ring rather than straight up it.
# Not the wool room's own interface, which is `PL13`.
plan["walls"] = [{"a": "wool-a-t4", "b": "wool-a-t2"}]

finish = {
    "authors": ["Opus 5"],
    "addShapes": shapes,
    "addLayers": [
        {"id": "garth-pool", "name": "The stank", "base_y": 0, "below": True,
         "shapes": pool,
         "islands": [{"id": "stank", "name": "The stank", "mirrors": True,
                      "shapeIds": [p["id"] for p in pool]}]},
    ],
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "heath",
    "roomStyles": {"cage": "@rg-cage", "spawn": "@rg-gate"},
    "dressing": {"props": props},
}


def write():
    for prop in props:
        if prop["kind"] in ("tree", "boulder") and not clear_spot(prop["x"], prop["z"]):
            raise SystemExit(f"{prop['id']} at {prop['x']},{prop['z']} is not a clear spot")
        if prop["kind"] == "house":
            (x0, z0), (x1, z1) = prop["wings"][0]["corners"]
            for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
                if not on_ground(x, z, margin=1):
                    raise SystemExit(f"{prop['id']} reaches void at {x},{z}")
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    kinds = {}
    for prop in props:
        kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
    span_x = max(p["rect"][0] + p["rect"][2] for p in plan["pieces"]) * CELL
    span_z = max(p["rect"][1] + p["rect"][3] for p in plan["pieces"]) * CELL
    print(f"composed p{COMPOSED['globals']['maxPlayers']} seed 26 · cell {CELL} · "
          f"authored half reaches x{span_x} z{span_z} -> board about {2 * 50} x {2 * span_z}")
    print(f"garth {RING} · hole {GARTH} · pool y{POOL_Y} · green y{GREEN_Y} · yard y{SURFACE}")
    print(f"pieces {len(plan['pieces'])} · walls {len(plan['walls'])} · shapes {len(shapes)} "
          f"+ {len(pool)} on the pond's own slab · "
          f"marks {len(MARKS)} · themes {len(THEMES)} · props {len(props)} {kinds}")
    print(f"scatter found {len(SPOTS)} clear spots: {SPOTS}")


if __name__ == "__main__":
    write()
