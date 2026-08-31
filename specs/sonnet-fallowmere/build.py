"""Fallowmere -- the author's basin flooded and walled, and left open around it.

Sonnet B's reading of the shared base: the same canal, the same single bridge, the same edgy
coast -- and then less of everything else. Two banks share one ground, the island keeps its own,
and the masonry is the third place. Few houses, a handful of trees, a scatter of stone -- the rest
is ground a player crosses rather than ground something stands on."""
import json, math, os, urllib.request

API = "http://localhost:7894/api"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = f"{ROOT}/specs/sonnet-fallowmere/sonnet-fallowmere"
plan   = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.plan.json"))
layout = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.layout.json"))
intent = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.intent.json"))

# G5 is the base's one hard failure: 'piece' and 'piece-4' hop 25 against a 10..20 band. Verified
# against POST /plan/evaluate -- valid: true, G5 gone -- without moving anything the layout draws.
for q in plan["pieces"]:
    if q["id"] == "piece":   q["rect"] = [-21, 14, 23, 10]
    if q["id"] == "piece-4": q["rect"] = [1, 5, 10, 9]
plan["meta"]["name"] = "Fallowmere"

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, PODZOL, DIRT, COARSE = solid(2), solid(3, 2), solid(3, 0), solid(3, 1)
STONE, GRANITE, ANDESITE, COBBLE, MOSSY_C, GRAVEL = solid(1), solid(1, 1), solid(1, 5), solid(4), solid(48), solid(13)
SBRICK, MOSSY_B, CHISEL = solid(98), solid(98, 1), solid(98, 3)
LOG, PLANK, PLANK_D = solid(17), solid(5, 0), solid(5, 2)
OAK_LEAVES = solid(18, 0)

def noise(a, b, scale, seed, rise=2):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 4, "stops": [a, b], "rise": rise}
def theme(surf, wall, fill, depth=1):
    return {"bedrock": {"relative": False, "value": 1}, "wallOnTerrainFaces": False,
            "surface": {"enabled": True, "depth": depth, "material": surf},
            "wall": wall, "wallEnabled": True, "fill": fill,
            "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "boundary"}
def flat(b): return theme(b, b, b)

# Three places and no more. The two banks share one ground -- the water is what tells them apart,
# not the paint -- and the island keeps its own; the masonry is the third, and it is the only thing
# on the board that reads as built rather than grown.
THEMES = {
 "sward": theme(GRASS, noise(DIRT, STONE, 16, 42), noise(STONE, GRANITE, 20, 43)),
 "holt": theme(noise(COARSE, PODZOL, 16, 51), noise(STONE, MOSSY_C, 14, 52), noise(STONE, MOSSY_C, 14, 52)),
 "wrought": theme(noise(SBRICK, ANDESITE, 12, 61), noise(SBRICK, CHISEL, 10, 62), noise(SBRICK, CHISEL, 10, 62)),
 "plank": flat(PLANK), "plank-dark": flat(PLANK_D), "canvas": flat(solid(35, 0)), "leaf": flat(OAK_LEAVES),
}

# ── the canal, and the wall that traces it ───────────────────────────────────
S0 = [[-132,49],[-125,35],[-82,43],[-46,30],[-15,35],[-7,54],[-15,70],[-40,62],[-90,76],[-108,73],[-125,70]]
S1 = [[-113,95],[-108,73],[-90,76],[-40,62],[1,75],[13,96],[5,120],[-34,131],[-68,122],[-105,120]]
S2 = [[-122,15],[-115,0],[-89,-20],[-65,-2],[-33,6],[-15,35],[-46,30],[-82,43],[-125,35]]
SOUTH = [[-125,35],[-82,43],[-46,30],[-15,35]]   # s0's edge shared with s2
NORTH = [[-15,70],[-40,62],[-90,76],[-108,73],[-125,70]]  # s0's edge shared with s1
BANK, WALL_TOP, WALL_FLOOR, WATER, BED = 30, 30, 15, 23, 16
BRIDGE_X, DECK_HALF, LAND_IN = -70, 6, 6   # a single crossing, central on the canal's own run

def basin_span(x):
    """The canal's z-extent at this x, read off its own ring so the span follows the shape."""
    hits = []
    for i in range(len(S0)):
        (ax, az), (bx, bz) = S0[i], S0[(i + 1) % len(S0)]
        if (ax <= x <= bx) or (bx <= x <= ax):
            if ax != bx: hits.append(az + (x - ax) * (bz - az) / (bx - ax))
    return (min(hits), max(hits)) if len(hits) >= 2 else (0, 0)

def built(sid, pts, radius, floor, height, th="wrought", seed=7):
    return {"id": sid, "type": "path", "operation": "add", "override": True, "keepClear": True,
            "vertices": pts, "radius": radius, "path_edge": "solid", "path_seed": seed,
            "floor": floor, "base_height": height, "skirt": 0, "relief_scope": "exclude",
            "theme": th, "height_mode": "level"}

ground = layout["layers"][0]["layout"]
for s in ground["shapes"]:
    s["theme"] = {"s0": "wrought", "s1": "sward", "s2": "sward", "s3": "holt"}.get(s["id"], s.get("theme"))

# The wall runs unbroken -- the bridge does not cut a gate through it, it rides over it, since the
# wall's own top and the bank it retains are one height (BANK) and the deck starts from the same.
# A gap cut here instead would bare the raw, un-graded seam between the bank's own area mark and
# the canal-bed's -- two flat marks meeting with no blend between them, which is a cliff no wall
# and no deck then covers.
edges = [
  built("wall-n", NORTH, 1.0, WALL_FLOOR, WALL_TOP - WALL_FLOOR),
  built("wall-s", SOUTH, 1.0, WALL_FLOOR, WALL_TOP - WALL_FLOOR),
]
ground["shapes"].extend(edges)
ground["groups"][0]["shapeIds"] = ["s0", "s1", "s2"] + [e["id"] for e in edges]
TEAM, ISLE = ground["groups"][0]["id"], ground["groups"][1]["id"]

# ── the bridge: one deck, one pier, on its own layer ──────────────────────────
def rect(sid, x0, z0, x1, z1, floor, h, th, keep=True):
    return {"id": sid, "type": "rectangle", "operation": "add", "override": True, "keepClear": keep,
            "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1, "floor": floor, "base_height": h,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": th}

def arch(sid, a0, a1, water_lo, water_hi, cross0, cross1, spring, crown_rise, piers, pier_foot,
         theme_id="wrought"):
    """A bridge drawn one slice per block along z: the deck rises from bank height at a0/a1 to a
    crown over mid-span. Over the true water it is an open soffit springing from each pier in an
    arc, so the race runs through the openings; short of the water, on the wall it rides over, it
    is a thin causeway a couple of courses deep -- there to carry the deck across the wall's own
    top rather than to dig into the bank beside it, which is what a thick fill there would do."""
    out, span = [], a1 - a0
    def deck_at(a):
        f = (a - a0) / span
        return round(BANK + crown_rise * math.sin(math.pi * f))
    stops = [water_lo] + list(piers) + [water_hi]
    for a in range(int(a0), int(a1) + 1):
        top = deck_at(a)
        if a < water_lo or a > water_hi:
            floor = top - 2                                    # a thin causeway over the wall
        elif any(abs(a - q) <= 4 for q in piers):
            floor = pier_foot
        else:
            left = max([q for q in stops if q <= a], default=water_lo)
            right = min([q for q in stops if q >= a], default=water_hi)
            half, mid = max((right - left) / 2, 1), (left + right) / 2
            r = max(0.0, 1 - ((a - mid) / half) ** 2) ** 0.5
            floor = int(round(spring + (top - 2 - spring) * r))
        out.append(rect(f"{sid}-{a}", cross0, a, cross1, a + 1, floor, top - floor + 1, theme_id))
        out.append(rect(f"{sid}-pw-{a}", cross0 - 2, a, cross0, a + 1, top + 1, 2, theme_id))
        out.append(rect(f"{sid}-pe-{a}", cross1, a, cross1 + 2, a + 1, top + 1, 2, theme_id))
    return out

_zlo, _zhi = basin_span(BRIDGE_X)
WATER_LO, WATER_HI = round(_zlo), round(_zhi)
Z0, Z1 = WATER_LO - LAND_IN, WATER_HI + LAND_IN
span = arch("bridge", Z0, Z1, WATER_LO, WATER_HI, BRIDGE_X - DECK_HALF, BRIDGE_X + DECK_HALF,
            spring=BED + 1, crown_rise=6, piers=(round((_zlo + _zhi) / 2),), pier_foot=BED - 1)
layout["layers"] = [layout["layers"][0],
  {"id": "spans", "name": "Bridge", "base_y": 0, "layout": {"shapes": span,
   "groups": [{"id": "spans-body", "name": "bridge", "mirrors": True,
               "shapeIds": [s["id"] for s in span]}]}}]

# ── relief: two flat banks pinned by marks, rolled by pushes; the canal a level floor ───────────
def ring(cx, cz, rx, rz, n=9):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n)), round(cz + rz * math.sin(2 * math.pi * i / n))]
            for i in range(n)]

D1X, D1Z = -90, 18   # destroyable-1's own anchor -- the pit goes under this one
layout["relief"] = {
 TEAM: {"base": BANK, "reach": 42, "step": 1, "stairs": True, "landform": "rolling",
   "grain": {"amplitude": 0.5, "scale": 19, "seed": 5},
   "marks": [
     {"id": "canal-bed", "kind": "area", "h": BED, "ring": S0},
     {"id": "north-bank", "kind": "area", "h": BANK, "ring": S1},
     {"id": "south-bank", "kind": "area", "h": BANK, "ring": S2}],
   "pushes": [
     {"id": "north-rise", "ring": ring(-38, 116, 18, 13), "amount": 5, "falloff": 18,
      "roughness": 0.35, "crown": 3, "seed": 11},
     {"id": "south-rise", "ring": ring(-32, -6, 18, 12), "amount": 5, "falloff": 18,
      "roughness": 0.35, "crown": 3, "seed": 12},
     {"id": "goal-hollow", "ring": ring(D1X, D1Z, 10, 7), "amount": -6, "falloff": 10,
      "roughness": 0.3, "crown": -3, "seed": 13},
     {"id": "canal-dish", "ring": S0, "amount": -3, "falloff": 6,
      "roughness": 0.25, "crown": -3, "seed": 14}]},
 ISLE: {"base": 25, "reach": 30, "step": 1, "stairs": True, "landform": "rolling",
   "grain": {"amplitude": 0.7, "scale": 13, "seed": 15},
   "marks": [],
   "pushes": [{"id": "knoll", "ring": ring(48, 50, 18, 13), "amount": 5, "falloff": 22,
               "roughness": 0.3, "crown": 3, "seed": 16}]},
}
layout["themes"], layout["mapTheme"] = THEMES, "sward"
layout["roomStyles"] = {"spawn": json.load(open(f"{ROOT}/tools/styles/showcase-hall.json"))}

# Forked from a shipped preset rather than written from nothing (id 6, "cottage").
with urllib.request.urlopen(f"{API}/room-styles/6/json") as response:
    STYLE = json.loads(json.load(response)["styleJson"])
VARIANT = json.loads(json.dumps(STYLE))
SWAP = {(5, 1): (5, 0), (5, 5): (1, 0)}   # the variation is pale ash plank and stone verge, not oak
def repaint(node):
    if isinstance(node, dict):
        if node.get("kind") == "solid" and (node.get("id"), node.get("data", 0)) in SWAP:
            node["id"], node["data"] = SWAP[(node["id"], node.get("data", 0))]; return node
        for v in node.values(): repaint(v)
    elif isinstance(node, list):
        for v in node: repaint(v)
repaint(VARIANT)

def prop_layer(lid, prop, shapes, mirrors=True):
    return {"id": lid, "name": lid, "base_y": 0, "kind": "made", "part_of": prop,
            "layout": {"shapes": shapes, "groups": [{"id": lid + "-body", "name": prop,
                       "mirrors": mirrors, "shapeIds": [s["id"] for s in shapes]}]}}

# ── dressing: what stands on ground that was actually measured ──────────────
# Every coordinate below was read off POST .../column against the board this script had already
# built -- a site is flat within a block or two, carries nothing standing on it, and sits clear of
# the wall, the bridge, the route, the pit and the goal standoff. Fewer of them is the point.
def tree(pid, x, z, wood, height, **knobs):
    base = {"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973, "layer": "ground",
            "form": "grown", "x": x, "z": z, "wood": wood, "height": height, "stems": 1, "levels": 2}
    return base | knobs

def oak(pid, x, z, height):
    # A broadleaf: a low leader and a wide fork, so the crown spreads over the grass it stands on.
    return tree(pid, x, z, "oak", height, leader=0.5, flow=0.5, branchAngle=1.15,
                leafSize=0.66, whorled=False)

def fir(pid, x, z, height):
    # A conifer: branches gathered into whorls on a leader that climbs the whole height, against
    # the broadleaf -- and set on the island's coarser earth rather than the banks' grass.
    return tree(pid, x, z, "spruce", height, leader=0.8, flow=0.2, branchAngle=0.75,
                leafSize=0.56, whorled=True)

# Stone mottled with cobble in the rock's own frame -- two forms, three sizes, so the erratics read
# against each other rather than as one boulder copied.
ERRATIC = noise(STONE, COBBLE, 3, 71)
BOULDERS = [
 ("erratic-bank",  -108,   1, "round",   4, ERRATIC),
 ("erratic-shelf",  -84,  -9, "outcrop", 6, ERRATIC),
 ("erratic-cairn",  -55,  10, "cairn",   3, ERRATIC),
 ("erratic-north", -105,  88, "angular", 5, ERRATIC),
 ("erratic-holm",    46,  40, "cairn",   4, ERRATIC),
]

def house(pid, x0, z0, x1, z1, style, front):
    return {"id": pid, "kind": "house", "seed": abs(x0 * 7 + z0 * 13) % 9973, "layer": "ground",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}

# The bridge's own approach, spawn door to the far bank, so the crossing is a route and not
# scenery: a worn trail rather than a paved road, fitting ground that means to look unbuilt.
PACKED = noise(COARSE, DIRT, 9, 81, rise=1)
ROUTE_PTS = [[-90, 99], [-85, 85], [-73, 75], [-70, 55], [-73, 38], [-83, 26], [-90, 19]]
# A short branch off the crossing's own approach toward the airfield east of the croft -- passing
# east of the house rather than through it, since a road may end at a porch and may not cross one.
YARD_PTS = [[-83, 26], [-77, 12], [-70, 5], [-64, 3]]

# A rowboat moored in the wide reach west of the bridge -- the cheapest made thing that answers the
# canal directly, since it costs nothing the water was not already carrying.
BX, BZ = -100, 52
lighter = [("keel", [rect("bt-k", BX - 5, BZ - 2, BX + 5, BZ + 2, WATER - 3, 3, "plank-dark", keep=False)]),
           ("hull", [rect("bt-h", BX - 6, BZ - 3, BX + 6, BZ + 3, WATER, 2, "plank-dark", keep=False)]),
           ("thwart", [rect("bt-t", BX - 1, BZ - 3, BX + 1, BZ + 3, WATER + 2, 1, "plank", keep=False)])]
for name, shapes in lighter:
    layout["layers"].append(prop_layer(f"boat-{name}", "boat", shapes))

# A grounded biplane on the open flat south of the house -- the new thing to try, parked rather
# than flying, so it costs a footprint and nothing overhead. Wings and tail sit on their own
# layers, since a layer keeps one span per column and the wing crosses the fuselage's own.
PX, PZ, PY = -64, 3, 29
plane = [("fuselage", [rect("pl-f", PX - 6, PZ - 1, PX + 6, PZ + 1, PY, 2, "plank-dark", keep=False)]),
         ("nose",     [rect("pl-n", PX + 6, PZ - 1, PX + 7, PZ + 1, PY, 2, "wrought", keep=False)]),
         ("wings",    [rect("pl-w", PX - 2, PZ - 6, PX + 1, PZ + 6, PY, 2, "plank", keep=False)]),
         ("tail",     [rect("pl-tf", PX - 7, PZ - 3, PX - 6, PZ + 3, PY + 1, 1, "plank", keep=False),
                       rect("pl-tv", PX - 7, PZ - 1, PX - 6, PZ + 1, PY, 5, "plank-dark", keep=False)])]
for name, shapes in plane:
    layout["layers"].append(prop_layer(f"plane-{name}", "plane", shapes))

layout["dressing"] = {"props": [
 {"id": "canal-water", "kind": "water", "seed": 9, "layer": "ground", "shape": "pool", "points": S0,
  "radius": 6, "depth": 8, "shore": 1, "shoreWander": False, "edge": 0.5, "level": WATER,
  "bank": {"kind": "cell", "seed": 91, "cellSize": 4, "jitter": 25, "warp": 1,
           "palette": [GRAVEL, COARSE, solid(12, 0)], "rise": 0}},
 {"id": "route", "kind": "stroke", "seed": 21, "layer": "ground", "points": ROUTE_PTS,
  "radius": 2.5, "style": "worn", "coverage": 0.72, "route": True, "pave": PACKED},
 {"id": "route-yard", "kind": "stroke", "seed": 22, "layer": "ground", "points": YARD_PTS,
  "radius": 2, "style": "worn", "coverage": 0.7, "route": True, "pave": PACKED},
 house("croft-bank", -101, -6, -93, 1, STYLE, "posZ"),
 house("croft-north", -68, 84, -60, 90, VARIANT, "negZ"),
] + [oak(f"oak-{n}", x, z, h) for n, (x, z, h) in enumerate((
        (-104, -4, 10), (-97, -9, 9), (-68, 11, 11), (-100, 86, 10), (-80, 90, 12)))]
  + [fir(f"fir-{n}", x, z, h) for n, (x, z, h) in enumerate((
        (30, 40, 11), (60, 48, 13), (36, 58, 10)))]
  + [{"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973, "layer": "ground",
      "x": x, "z": z, "form": form, "size": size, "rock": rock, "mossy": True}
     for pid, x, z, form, size, rock in BOULDERS]}

# No finish.json: the current driver compiles from the plan whenever a finish exists at all, even
# an authorship-only one, and this board's geometry is the layout -- hand-drawn, not derivable from
# the plan. Authorship rides directly on the intent it is free to state.
intent["meta"]["name"] = "Fallowmere"
intent["meta"]["authors"] = ["Sonnet"]
intent["meta"]["created"] = "2026-08-30"
json.dump(plan,   open(SPEC + ".plan.json",   "w"), indent=1)
json.dump(layout, open(SPEC + ".layout.json", "w"), indent=1)
json.dump(intent, open(SPEC + ".intent.json", "w"), indent=1)
print(f"wrote {len(layout['layers'])} layers, {len(ground['shapes'])} ground shapes, "
      f"bridge deck {Z0}..{Z1}, water {WATER_LO}..{WATER_HI}")
