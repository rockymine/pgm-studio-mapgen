#!/usr/bin/env python3
"""Write the two authored documents for `opus5-rimegarth`.

    python3 specs/opus5-rimegarth/build-spec.py

**A regular capture-the-wool board, and the plan under it was composed rather than drawn.**
`composed.plan.json` beside this file is `GET /api/compose?players=10&symmetry=rot_180&seed=26`
pinned verbatim — the composer's own board, score 0 on every hard term, structure
`{wools: [donut], hub: twin, frontline: bar}`. It is kept untouched; what this script does is
everything a composed plan does not carry.

**The donut is why this seed was picked.** A composed wool box is normally a bar or an L; five times
in forty-eight it comes out as a **ring** — pieces enclosing a hole, with the wool room closing the
far corner of it. Read as a place that is a walled garth: a yard you can only go round, with the wool
in the byre at the far side and the middle of it open.

Three things are changed about what the composer drew, and each is a thing it never emits.

**The ring's two arms are split, so two walls can bar both lanes.** A ring has two ways round it and
one wall closes one of them; an attacker simply takes the other. `wool-a-t1` and `wool-a-t5` are cut
in half at z 80, and the approach wall goes on each new interface — a pair either side of the hole,
parallel to each other, each across the **full width of its own lane**.

**Every piece states a surface, and they step by one.** `walls` and `surface` are the two fields a
composed plan is always empty of; the second turns a flat board into a stair from the gill up to the
byre — 9, 10, 11, 12, 13, 14, 15, one course at each interface and never two. **No relief is stated
at all**, because a relief solves a height for every cell of an island and would take the plan's
surfaces with it: on this board the plan is the terrain.

**The hole gets a pond.** A composed plan compiles to one merged polygon and a `subtract`, and the
subtract is what cuts the hole; a subtract beats every add on its layer, so an `addShapes` rectangle
over the hole draws nothing at all. The pond is a slab of its own, stated `below` the compiled ground.

Output: `opus5-rimegarth.plan.json` and `opus5-rimegarth.finish.json` beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-rimegarth"
COMPOSED = json.load(open(os.path.join(HERE, "composed.plan.json")))
CELL = COMPOSED["globals"]["cell"]           # 5

# ── the plan: the composed board, with the ring cut and every piece given a height ─────────────
plan = json.loads(json.dumps(COMPOSED))
plan["meta"] = {"name": "Rimegarth"}

SPLIT_Z = 16                                 # in cells: block z 80, level with the middle of the hole


def split_arm(piece_id, a_id, b_id):
    """Cut one arm of the ring in two across the lane, so its seam can carry a wall. The composer
    emits an arm as one long piece; a wall is authored on an **interface**, and a piece with no seam
    across it has none to put one on."""
    pieces = plan["pieces"]
    index = next(i for i, p in enumerate(pieces) if p["id"] == piece_id)
    x, z, w, h = pieces[index]["rect"]
    pieces[index:index + 1] = [
        {"id": a_id, "role": "piece", "rect": [x, z, w, SPLIT_Z - z]},
        {"id": b_id, "role": "piece", "rect": [x, SPLIT_Z, w, h - (SPLIT_Z - z)]},
    ]


split_arm("wool-a-t1", "wool-a-t1a", "wool-a-t1b")      # the west lane, x -25..-15
split_arm("wool-a-t5", "wool-a-t5a", "wool-a-t5b")      # the east lane, x   0.. 10

# **The stair.** One course at every interface on the board, from the green at the gill's lip to the
# byre the wool stands in. Stated here rather than in a relief, because a relief would replace them.
SURFACES = {
    "frontline-t1": 9,                                   # the green, lowest and nearest the gill
    "hub-t1": 10, "hub-t2": 10, "hub-t3": 10,            # the hall's yard
    "spawn-t1": 11, "spawn-room": 11,                    # the gatehouse, a step above it
    "wool-a-t4": 11,                                     # the neck into the garth
    "wool-a-t2": 12,                                     # the garth's south arm
    "wool-a-t1a": 12, "wool-a-t1b": 13, "wool-a-t3": 14,  # the west lane, rising
    "wool-a-t5a": 13, "wool-a-t5b": 14,                  # and the east lane, rising with it
    "wool-a-room": 15,                                   # the byre, highest thing on the board
}
for piece in plan["pieces"]:
    piece["surface"] = SURFACES[piece["id"]]
plan["globals"]["surface"] = min(SURFACES.values())

# **Two walls, one to a lane, level with the middle of the hole.** A bedrock barrier two thick and
# three tall across the full interface, stamped on the attack side. Neither is the wool room's own
# interface (`PL13`); both are an approach out, which is where the device belongs.
plan["walls"] = [{"a": "wool-a-t1a", "b": "wool-a-t1b"},
                 {"a": "wool-a-t5a", "b": "wool-a-t5b"}]


def blocks(piece_id):
    """One piece's rectangle in blocks — the plan states cells."""
    x, z, w, h = next(p for p in plan["pieces"] if p["id"] == piece_id)["rect"]
    return (x * CELL, z * CELL, (x + w) * CELL, (z + h) * CELL)


GATE = blocks("spawn-room")                  # x -50..-40, z 40..50
HALL = blocks("hub-t1")                      # x -35..  0, z 40..50
GREEN = blocks("frontline-t1")               # x -15.. 15, z 10..30
NECK = blocks("wool-a-t4")                   # x -25..  0, z 50..60
RING_W = (blocks("wool-a-t1a")[0], blocks("wool-a-t1a")[1],
          blocks("wool-a-t1b")[2], blocks("wool-a-t1b")[3])
RING_S = blocks("wool-a-t2")                 # x -15..  0, z 60.. 70
RING_E = (blocks("wool-a-t5a")[0], blocks("wool-a-t5a")[1],
          blocks("wool-a-t5b")[2], blocks("wool-a-t5b")[3])
RING_N = blocks("wool-a-t3")                 # x -15..  0, z 95..105
BYRE = blocks("wool-a-room")                 # x   0.. 10, z 95..105

RING = (RING_W[0], RING_S[1], RING_E[2], RING_N[3])          # the garth's outer bound
GARTH = (RING_S[0], RING_S[3], RING_S[2], RING_E[3])         # the hole in it: x -15..0, z 70..95
POOL_TOP = 7                                                 # five courses under the garth's low arm
WALL_Z = SPLIT_Z * CELL                                      # z 80, where both walls stand

GROUND = [blocks(p["id"]) for p in plan["pieces"]]


def on_ground(x, z, margin=2):
    return any(x0 + margin <= x <= x1 - margin and z0 + margin <= z <= z1 - margin
               for x0, z0, x1, z1 in GROUND)


# ── materials ─────────────────────────────────────────────────────────────────────────────────
# Winter, and two greys: snow and ice for what the weather left, stone and cobble for what was built
# out of the hill, spruce for what was cut. The only colour is each team's own.
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
CLAY_STAINED = 159
CLAY_WHITE = solid(159, 0)

# What the board is cut out of, seen on every face — and on a board of steps every interface is one.
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
    # the heath the hall's yard is trodden out of
    "heath": theme(
        surface=layered(stack((noise(12, 9, 3, [COARSE, SNOW, SNOW]), 1), (PODZOL, 1), (DIRT, 1))),
        wall=SECTION, fill=STONE, rim=COBBLE, surface_depth=3),

    # the gatehouse's forecourt and the neck: walked through to the gravel under it
    "yard": theme(
        surface=layered(stack((voronoi(13, 5, [(SNOW, 1), (MOSSY_COBBLE, 1), (COARSE, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=SECTION, fill=STONE, rim=STONE_BRICK, surface_depth=3),

    # the garth: paved, because a yard with a pond in it was laid rather than worn
    "garth": theme(
        surface=layered(stack((voronoi(16, 4, [(SNOW, 1), (MOSSY_COBBLE, 1), (COBBLE, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=SECTION, fill=STONE, rim=STONE_BRICK, surface_depth=3),

    # the green before the gill, and **the one place the board says whose it is**: `teamTint` caps
    # the drop, so the lip a team defends is that team's colour seen from the other side of the void
    "green": theme(
        surface=layered(stack((noise(14, 7, 3, [SNOW, SNOW, COARSE]), 1), (COARSE, 1), (DIRT, 1))),
        wall=SECTION, fill=STONE,
        rim=team_tint(CLAY_STAINED, CLAY_WHITE), surface_depth=3),

    # the pond in the middle of the garth
    "pool": theme(
        surface=layered(stack((voronoi(15, 4, [(PACKED_ICE, 1), (GRAVEL, 2), (ICE, 1)]), 1),
                              (GRAVEL, 1), (STONE, 2))),
        wall=layered(stack((PACKED_ICE, 1), (GRAVEL, 2), (STONE, 4))),
        fill=STONE, rim=PACKED_ICE, surface_depth=2),
}

# **The stair is what themes the board.** Every band of the plan now stands at its own height, so a
# theme per height needs no shapes at all — which is as well, since an `addShapes` rectangle at one
# height over ground at another is two adds stacked on one layer (`SK9`).
THEME_BY_HEIGHT = {"9": "green", "10": "heath", "11": "yard",
                   "12": "garth", "13": "garth", "14": "garth", "15": "garth"}

# ── the pond's own slab ───────────────────────────────────────────────────────────────────────
pool = [{"id": "pool1", "type": "rectangle", "operation": "add",
         "min_x": GARTH[0], "min_z": GARTH[1], "max_x": GARTH[2], "max_z": GARTH[3],
         "floor": 0, "base_height": POOL_TOP + 1, "theme": "pool"}]


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
            "rock": voronoi(17, 4, [(MOSSY_COBBLE, 1), (ANDESITE, 1), (STONE, 1)])}


def flora(ident, ring, coverage, seed, scale=8, fern=0.24, flower=0.1, tall=0.2):
    return {"id": ident, "kind": "flora", "seed": seed,
            "points": [[x, z] for x, z in ring],
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flower, "flowerScale": 6, "tallShare": tall}}


def stroke(ident, points, radius, pave, style="worn", coverage=0.4, route=False, seed=1):
    out = {"id": ident, "kind": "stroke", "seed": seed, "style": style, "radius": radius,
           "coverage": coverage, "pave": pave}
    if route:
        out["route"] = True
    out["points"] = [[x, z] for x, z in points]
    return out


TROD = voronoi(21, 4, [(SNOW, 1), (GRAVEL, 1), (COARSE, 1)])

# The three roads, stated once and read by both the strokes and the scatter below. Each lane's road
# runs through its own wall, because a wall is opened on its approach face and the way is through it.
STREET = [(-44, 45), (-30, 46), (-14, 44), (-6, 38), (-2, 28), (0, 16), (0, 11)]
GARTH_W = [(-14, 52), (-20, 58), (-20, 74), (-20, 92), (-14, 100), (-2, 100)]
GARTH_E = [(-10, 54), (-6, 64), (4, 68), (5, 84), (5, 96)]
ROADS = ((STREET, 3.0), (GARTH_W, 2.4), (GARTH_E, 2.2))

HOUSES = [("hall", (-14, 41, 13, 7), "@rg-hall", "negZ"),
          ("solar", (-33, 32, 7, 7), "@rg-hall", "posZ")]

# The two wall seams, kept clear the way a doorway is.
WALL_SEAMS = [(RING_W[0] - 4, WALL_Z - 7, RING_W[2] + 4, WALL_Z + 7),
              (RING_E[0] - 4, WALL_Z - 7, RING_E[2] + 4, WALL_Z + 7)]


def _near_segment(x, z, a, b):
    (ax, az), (bx, bz) = a, b
    dx, dz = bx - ax, bz - az
    span = dx * dx + dz * dz
    t = 0.0 if span == 0 else max(0.0, min(1.0, ((x - ax) * dx + (z - az) * dz) / span))
    return math.hypot(x - (ax + t * dx), z - (az + t * dz))


def clear_spot(x, z):
    """Whether a prop may stand here. **Every rule the dressing pass declines on, asked before the
    document is written** — the board is lanes ten blocks wide with a road down each of them, so a
    coordinate that merely looks free almost never is. A road's standoff is measured to its **paved
    cells**, so what is cleared is the stroke's radius plus the standoff its kind states."""
    if not on_ground(x, z, margin=3):
        return False
    for road, radius in ROADS:
        for a, b in zip(road, road[1:]):
            if _near_segment(x, z, a, b) < radius + 4:
                return False
    for _, (hx, hz, hw, hd), _, _ in HOUSES:
        if hx - 4 <= x <= hx + hw + 4 and hz - 4 <= z <= hz + hd + 4:
            return False
    for room in (GATE, BYRE):
        if room[0] - 15 <= x <= room[2] + 15 and room[1] - 15 <= z <= room[3] + 15:
            return False
    for seam in WALL_SEAMS:
        if seam[0] <= x <= seam[2] and seam[1] <= z <= seam[3]:
            return False
    if GARTH[0] - 3 <= x <= GARTH[2] + 3 and GARTH[1] - 3 <= z <= GARTH[3] + 3:
        return False
    return True


def scatter(count, apart=8):
    """The clear spots, taken in a fixed order and thinned. No randomness: the same board always
    dresses the same way."""
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
    # The pond. **A water prop fills its own band and does not spread to the level it finds**, so
    # the band is the pond: a centreline down the middle of the hole at a radius that leaves a block
    # and a half of bank inside the garth's wall.
    {"id": "the-stank", "kind": "water", "seed": 5, "form": "canal",
     "points": [[(GARTH[0] + GARTH[2]) / 2, GARTH[1] + 9],
                [(GARTH[0] + GARTH[2]) / 2, GARTH[3] - 9]],
     "radius": 6.0, "depth": 2, "edge": 0.3, "shore": 1, "shoreWander": False,
     "bank": voronoi(18, 4, [(PACKED_ICE, 1), (GRAVEL, 1), (COBBLE, 1)])},
]

props += [house(ident, x, z, w, d, style, 11 + k, front=front)
          for k, (ident, (x, z, w, d), style, front) in enumerate(HOUSES)]

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
    # and the two ways round the garth, one to a lane, each through its own wall
    stroke("garth-w", GARTH_W, ROADS[1][1], TROD, coverage=0.85, route=True, seed=32),
    stroke("garth-e", GARTH_E, ROADS[2][1], TROD, coverage=0.8, route=True, seed=33),

    # and two that are paint rather than a way
    stroke("drift", [(RING[0] + 3, RING[1] + 3), (RING[0] + 3, RING[3] - 3),
                     (RING[2] - 3, RING[3] - 3), (RING[2] - 3, RING[1] + 3)], 3.0, SNOW,
           style="worn", coverage=0.45, seed=34),
    stroke("tread", [(GREEN[0] + 4, GREEN[3] - 4), (0, GREEN[1] + 8), (GREEN[2] - 4, GREEN[3] - 4)],
           5.0, voronoi(22, 4, [(SNOW, 1), (COBBLE, 1), (GRAVEL, 1)]),
           style="worn", coverage=0.35, seed=35),
]

finish = {
    "authors": ["Opus 5"],
    "themeByHeight": THEME_BY_HEIGHT,
    "addLayers": [
        {"id": "garth-pool", "name": "The stank", "base_y": 0, "below": True,
         "shapes": pool,
         "islands": [{"id": "stank", "name": "The stank", "mirrors": True,
                      "shapeIds": [p["id"] for p in pool]}]},
    ],
    "themes": THEMES,
    "mapTheme": "heath",
    "roomStyles": {"cage": "@rg-cage", "spawn": "@rg-gate"},
    "dressing": {"props": props},
}


def write():
    steps = sorted(set(SURFACES.values()))
    if steps != list(range(steps[0], steps[-1] + 1)):
        raise SystemExit(f"the stair skips a course: {steps}")
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
    print(f"composed p{plan['globals']['maxPlayers']} seed 26 · cell {CELL} · "
          f"{len(COMPOSED['pieces'])} pieces composed -> {len(plan['pieces'])} after the ring is cut")
    print(f"stair {steps} · walls at z{WALL_Z}: "
          f"west x{RING_W[0]}..{RING_W[2]}, east x{RING_E[0]}..{RING_E[2]}")
    print(f"garth {RING} · hole {GARTH} · pond top y{POOL_TOP}")
    print(f"themes {len(THEMES)} by height {THEME_BY_HEIGHT} · props {len(props)} {kinds}")
    print(f"scatter found {len(SPOTS)} clear spots: {SPOTS}")


if __name__ == "__main__":
    write()
