"""Cutwater — the author's basin flooded, walled and bridged, Sonnet A's own composition."""
import json, math, os, urllib.request

ROOT = "/home/user/pgm-studio-mapgen"
SPEC = f"{ROOT}/specs/sonnet-cutwater/sonnet-cutwater"
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
STYLES = f"{ROOT}/tools/styles"

plan   = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.plan.json"))
layout = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.layout.json"))
intent = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.intent.json"))


def api_get(path):
    with urllib.request.urlopen(API + path, timeout=30) as response:
        return json.loads(response.read())


# G5 is the one hard term the base fails: 'piece' and 'piece-4' hop 25 against a band of
# 10..20. Widening 'piece' by one cell and shifting 'piece-4' the same amount clears it without
# opening a new gap to 'piece-2' — verified against /plan/evaluate before anything else is built.
for piece in plan["pieces"]:
    if piece["id"] == "piece":   piece["rect"] = [-21, 14, 23, 10]
    if piece["id"] == "piece-4": piece["rect"] = [1, 5, 10, 9]
plan["meta"]["name"] = "Cutwater"

# ── materials ─────────────────────────────────────────────────────────────────────────────
def solid(block, data=0): return {"kind": "solid", "id": block, "data": data}
def noise(a, b, scale, seed, rise=2):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 4, "stops": [a, b], "rise": rise}

GRASS, PODZOL, COARSE = solid(2), solid(3, 2), solid(3, 1)
STONE, DIORITE = solid(1, 0), solid(1, 3)
COBBLE, MOSSY_C, GRAVEL = solid(4), solid(48), solid(13)
SBRICK, MOSSY_B, CRACKED_B = solid(98, 0), solid(98, 1), solid(98, 2)
LOG, PLANK_DARK = solid(17, 0), solid(5, 5)
WHITE_WOOL, RED_WOOL = solid(35, 0), solid(35, 14)
QUARTZ, WHITE_GLASS = solid(155, 0), solid(95, 0)
STONE_PALE = solid(1, 3)

def theme(surface, wall, fill, depth=1):
    return {"bedrock": {"relative": False, "value": 1}, "wallOnTerrainFaces": False,
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill,
            "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "boundary"}
def flat(material): return theme(material, material, material)

# Three grounds, three places: the bank both masses share, the quay the wall and bridge stand
# on, and the island's own heath. Each paint is one family in two shades, so a ground reads as
# grain rather than as a stamped pattern.
THEMES = {
    "bank": theme(GRASS, noise(STONE, DIORITE, 17, 21), noise(STONE, DIORITE, 17, 21)),
    "quay": theme(noise(SBRICK, MOSSY_B, 11, 41), noise(SBRICK, CRACKED_B, 11, 42),
                  noise(SBRICK, CRACKED_B, 11, 42)),
    "heath": theme(noise(PODZOL, COARSE, 14, 31), noise(STONE, MOSSY_C, 13, 32),
                   noise(STONE, MOSSY_C, 13, 32)),
    # Flat single-material paint for the made things below — a hull, a sail, a fuselage is not a
    # place, so these ride outside the three-ground count the ground itself is held to.
    "canvas-red": flat(RED_WOOL), "canvas-white": flat(WHITE_WOOL), "timber-dark": flat(PLANK_DARK),
    "hull-log": flat(LOG), "hull-plank": flat(solid(5, 0)), "metal-white": flat(QUARTZ),
    "statue-stone": flat(STONE_PALE), "cloud-glass": flat(WHITE_GLASS),
}

# ── the basin, its neighbours, and the wall that traces it ─────────────────────────────────
S0 = [[-132, 49], [-125, 35], [-82, 43], [-46, 30], [-15, 35], [-7, 54], [-15, 70],
      [-40, 62], [-90, 76], [-108, 73], [-125, 70]]
# The south arc (shared with s2) continues through the basin's own tapered nose to vertex 6,
# and the north arc (shared with s1) picks up from there — together they trace the whole inner
# shore in two open chains, leaving only the outer tip (toward the map edge) unwalled.
SOUTH_ARC = [S0[1], S0[2], S0[3], S0[4], S0[5], S0[6]]
NORTH_ARC = [S0[6], S0[7], S0[8], S0[9], S0[10]]

BANK, WATER, BED = 30, 24, 15
WALL_TOP, WALL_FLOOR = 33, 11
BRIDGE_X = -82                              # the canal's narrowest crossing, measured off S0

def wall(sid, pts, seed):
    return {"id": sid, "type": "path", "operation": "add", "override": True, "keepClear": True,
            "vertices": pts, "radius": 1.6, "path_edge": "solid", "path_seed": seed,
            "floor": WALL_FLOOR, "base_height": WALL_TOP - WALL_FLOOR, "height_mode": "level",
            "skirt": 0, "theme": "quay"}

ground = layout["layers"][0]["layout"]
by_id = {s["id"]: s for s in ground["shapes"]}
by_id["s0"]["theme"] = "bank"
by_id["s1"]["theme"] = "bank"
by_id["s2"]["theme"] = "bank"
by_id["s3"]["theme"] = "heath"

edges = [wall("wall-south", SOUTH_ARC, 51), wall("wall-north", NORTH_ARC, 52)]
ground["shapes"].extend(edges)
ground["groups"][0]["shapeIds"] = ["s0", "s1", "s2"] + [e["id"] for e in edges]
TEAM, ISLE = ground["groups"][0]["id"], ground["groups"][1]["id"]

# ── the bridge: a deck, parapets and one mid-stream pier, on its own layer ──────────────────
def rect(sid, x0, z0, x1, z1, floor, height, th, keep=True):
    return {"id": sid, "type": "rectangle", "operation": "add", "override": True, "keepClear": keep,
            "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1, "floor": floor, "base_height": height,
            "height_mode": "level", "skirt": 0, "theme": th}

def basin_span(x):
    """The basin's z-extent at this x, read off S0's own ring so the span follows the shape."""
    hits = []
    for i in range(len(S0)):
        (ax, az), (bx, bz) = S0[i], S0[(i + 1) % len(S0)]
        if (ax <= x <= bx) or (bx <= x <= ax):
            if ax != bx:
                hits.append(az + (x - ax) * (bz - az) / (bx - ax))
    return (min(hits), max(hits)) if len(hits) >= 2 else (0, 0)

_zlo, _zhi = basin_span(BRIDGE_X)          # measured 43.0 .. 73.8 at x=-82
Z0, Z1 = _zlo, _zhi                        # the deck's own span is exactly the water it crosses

def arch(sid, x0, x1, cross0, cross1, spring, crown_rise, piers, pier_foot, theme_id="quay"):
    """The deck rises to a crown at mid-span, over WALL_TOP so it never sits lower than the
    quay it springs from. Between the shore and a pier the soffit is flush with the deck at
    both ends of that run and opens to `spring` at its own middle — a real arch, not a trench —
    so the two layers never compete for the same block at the wall crossing itself."""
    out, span = [], x1 - x0
    def deck_at(a):
        f = (a - x0) / span
        return round(WALL_TOP + crown_rise * math.sin(math.pi * f))
    stops = [x0] + list(piers) + [x1]
    for a in range(int(x0), int(x1) + 1):
        top = deck_at(a)
        if any(abs(a - q) <= 3 for q in piers):
            floor = pier_foot
        else:
            left = max([q for q in stops if q <= a], default=x0)
            right = min([q for q in stops if q >= a], default=x1)
            run = max(right - left, 1)
            opening = math.sin(math.pi * min(max((a - left) / run, 0.0), 1.0))
            floor = int(round(top - (top - spring) * opening))
        out.append(rect(f"{sid}-{a}", cross0, a, cross1, a + 1, floor, top - floor + 1, theme_id))
        out.append(rect(f"{sid}-pw-{a}", cross0 - 2, a, cross0, a + 1, top + 1, 3, theme_id))
        out.append(rect(f"{sid}-pe-{a}", cross1, a, cross1 + 2, a + 1, top + 1, 3, theme_id))
    return out

span = arch("bridge", Z0, Z1, BRIDGE_X - 5, BRIDGE_X + 5,
            spring=BED + 1, crown_rise=7, piers=(round((_zlo + _zhi) / 2),), pier_foot=BED - 1)
layout["layers"] = [layout["layers"][0],
    {"id": "spans", "name": "spans", "base_y": 0, "layout": {"shapes": span,
     "groups": [{"id": "spans-body", "name": "spans", "mirrors": True,
                 "shapeIds": [s["id"] for s in span]}]}}]

# ── relief: hills and a cliff line where the four hint layers stood, a dished bed under the
# water, a graded pit under the near destroyable ────────────────────────────────────────────
def ring(cx, cz, rx, rz, n=10):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n)), round(cz + rz * math.sin(2 * math.pi * i / n))]
            for i in range(n)]

DESTROYABLE_1 = (-90, 18)   # red's own — the quarry pit sinks around it
DESTROYABLE_2 = (-15, 98)

layout["relief"] = {
    TEAM: {"base": BANK, "reach": 5, "step": 1, "stairs": True, "landform": "hills",
        "grain": {"amplitude": 1.0, "scale": 18, "seed": 201},
        "marks": [{"id": "basin", "kind": "area", "h": BED, "ring": S0}],
        "pushes": [
            # the north hill, where 'Layer 2'/'Layer 5' stood on s1
            {"id": "hill-north", "ring": ring(-38, 120, 20, 16), "amount": 9, "falloff": 24,
             "roughness": 0.4, "crown": 4, "seed": 21},
            # the west hill, where 'Layer 2'/'Layer 5' stood on s2
            {"id": "hill-south", "ring": ring(-80, 8, 26, 18), "amount": 8, "falloff": 28,
             "roughness": 0.4, "crown": 4, "seed": 22},
            # the pit destroyable-1 sits down inside, graded rather than punched — 'hill-south'
            # reaches this far too, so the amount nets against its own +8 rather than against
            # the bare BANK the two pushes would give a point neither of them touched
            {"id": "quarry-pit", "ring": ring(*DESTROYABLE_1, 13, 11), "amount": -20, "falloff": 18,
             "roughness": 0.3, "crown": 3, "seed": 23}]},
    ISLE: {"base": 25, "reach": 12, "step": 1, "stairs": True, "landform": "hills",
        "grain": {"amplitude": 0.8, "scale": 13, "seed": 211},
        "marks": [],
        "pushes": [{"id": "isle-knoll", "ring": ring(47, 53, 15, 13), "amount": 9, "falloff": 18,
                    "roughness": 0.35, "crown": 4, "seed": 31}]},
}
# A scarp for real vertical: the south hill drops to a low bluff facing away from the canal,
# a narrow face rather than the pushes' rolled shoulders. Points measured safely inside s2's
# own southern boundary (which dips to z -20 near x -89) so the scarp states ground s2 owns.
layout["relief"][TEAM]["marks"].append(
    {"id": "south-bluff", "kind": "scarp", "points": [[-100, 0], [-85, -6], [-68, 4]],
     "high": 36, "low": 22, "face": 4, "band": 6})

layout["themes"], layout["mapTheme"] = THEMES, "bank"

# ── house styles: one preset, forked, and a repaint for the far bank ────────────────────────
STYLE = json.loads(api_get("/room-styles/7/json")["styleJson"])          # 'longhouse'
VARIANT = json.loads(json.dumps(STYLE))
SWAP = {(1, 0): (1, 3), (1, 6): (1, 4), (5, 1): (5, 3)}    # a cooler diorite stone, jungle roof
def repaint(node):
    if isinstance(node, dict):
        if node.get("kind") == "solid" and (node.get("id"), node.get("data", 0)) in SWAP:
            node["id"], node["data"] = SWAP[(node["id"], node.get("data", 0))]
            return
        for value in node.values():
            repaint(value)
    elif isinstance(node, list):
        for value in node:
            repaint(value)
repaint(VARIANT)

layout["roomStyles"] = {"spawn": json.load(open(f"{STYLES}/showcase-hall.json"))}

def prop_layer(layer_id, prop, shapes, mirrors=True, seat=None):
    slab = {"id": layer_id, "name": layer_id, "base_y": 0, "kind": "prop", "prop": prop,
            "layout": {"shapes": shapes, "groups": [{"id": layer_id + "-body", "name": prop,
                       "mirrors": mirrors, "shapeIds": [s["id"] for s in shapes]}]}}
    if seat:
        slab["seat"] = seat
    return slab

def disc(sid, cx, cz, radius, floor, height, th, keep=False):
    return {"id": sid, "type": "circle", "operation": "add", "center_x": cx, "center_z": cz,
            "radius": radius, "floor": floor, "base_height": height, "keepClear": keep, "theme": th}

def house(pid, x0, z0, x1, z1, style, front):
    return {"id": pid, "kind": "house", "seed": abs(x0 * 7 + z0 * 13) % 9973, "layer": "ground",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}

def tree(pid, x, z, wood, height, **knobs):
    base = {"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973, "layer": "ground",
            "form": "grown", "x": x, "z": z, "wood": wood, "height": height, "stems": 1, "levels": 2}
    return base | knobs

def oak(pid, x, z, height):
    return tree(pid, x, z, "oak", height, leader=0.5, flow=0.5, branchAngle=1.15,
                leafSize=0.68, whorled=False)

def fir(pid, x, z, height):
    return tree(pid, x, z, "spruce", height, leader=0.78, flow=0.2, branchAngle=0.8,
                leafSize=0.58, whorled=True)

def template_tree(pid, x, z, species, height):
    return {"id": pid, "kind": "tree", "seed": abs(x * 13 + z * 19) % 9973, "layer": "ground",
            "form": "template", "x": x, "z": z, "species": species, "height": height}

def boulder(pid, x, z, form, size, rock, mossy=True):
    return {"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973, "layer": "ground",
            "x": x, "z": z, "form": form, "size": size, "rock": rock, "mossy": mossy}

# Broadleaf on the bank's grass, both sides of the water; conifer on the island's earth. Every
# site below is read off the built columns — flat, clear of the goals' clearance and the wall —
# rather than guessed off the plan's now-superseded flat hint layers.
OAKS_N = [(-65, 82, 10), (-25, 85, 9), (-35, 105, 9)]
OAKS_S = [(-40, 10, 10), (-114, 22, 9)]
FIRS_ISLE = [(38, 48, 13), (55, 62, 11), (60, 45, 14)]
GNEISS, GRIT = noise(STONE, COBBLE, 3, 61), noise(STONE, GRAVEL, 2, 62)
BOULDERS = [
    ("erratic-north", -25, 118, "outcrop", 7, GNEISS),
    ("erratic-west", -108, 10, "angular", 6, GRIT),
    ("erratic-isle", 45, 45, "cairn", 5, GRIT),
    ("erratic-quarry", -72, 6, "round", 8, GRIT),
]

def densify(ring, step=10):
    """A ring resampled so no two consecutive points are far apart — a pool floods within
    `radius` of its own points, so a basin wider than the gap between two corner vertices
    leaves the water short of the middle of its own long edges unless they carry points too."""
    out = []
    n = len(ring)
    for i in range(n):
        ax, az = ring[i]
        bx, bz = ring[(i + 1) % n]
        out.append([ax, az])
        length = math.hypot(bx - ax, bz - az)
        cuts = max(1, int(length // step))
        for c in range(1, cuts):
            t = c / cuts
            out.append([round(ax + (bx - ax) * t, 1), round(az + (bz - az) * t, 1)])
    return out

def expand(ring, margin):
    """The ring pushed outward from its own centroid — the relief's basin mark grades into the
    bank over a few blocks past S0's own edge, and the pool has to reach that far too or the
    graded slope dips under the waterline with no water drawn on it."""
    cx = sum(p[0] for p in ring) / len(ring)
    cz = sum(p[1] for p in ring) / len(ring)
    out = []
    for x, z in ring:
        length = math.hypot(x - cx, z - cz) or 1
        out.append([round(x + (x - cx) / length * margin, 1), round(z + (z - cz) / length * margin, 1)])
    return out

layout["dressing"] = {"props": [
    {"id": "canal-water", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool",
     "points": densify(expand(S0, 15)), "radius": 20, "depth": WATER - BED, "shore": 1,
     "shoreWander": False, "edge": 0.6, "level": WATER, "bank": GRAVEL},
    {"id": "road-bridge-n", "kind": "stroke", "seed": 41, "route": True, "radius": 2,
     "points": [[-58, 108], [-64, 96], [BRIDGE_X, Z1]], "pave": GRAVEL},
    {"id": "road-bridge-s", "kind": "stroke", "seed": 42, "route": True, "radius": 2,
     "points": [[BRIDGE_X, Z0], [-88, 26], [DESTROYABLE_1[0], DESTROYABLE_1[1] + 8]], "pave": GRAVEL},
    house("house-north-1", -58, 85, -48, 93, STYLE, "posZ"),
    house("house-north-2", -40, 84, -30, 92, VARIANT, "negZ"),
    house("house-south-1", -56, 6, -46, 14, VARIANT, "posZ"),
] + [oak(f"oak-n{n}", x, z, h) for n, (x, z, h) in enumerate(OAKS_N)]
  + [oak(f"oak-s{n}", x, z, h) for n, (x, z, h) in enumerate(OAKS_S)]
  + [fir(f"fir-{n}", x, z, h) for n, (x, z, h) in enumerate(FIRS_ISLE)]
  + [template_tree("template-oak-a", -66, 84, "oak", 14),
     template_tree("template-oak-b", -74, 96, "oak", 12)]
  + [boulder(pid, x, z, form, size, rock) for pid, x, z, form, size, rock in BOULDERS]}

# ── made things: a balloon and clouds aloft, a barge in the canal, a plane overhead, a
# guardian statue at the bridgehead. Every shape below paints with one of the flat single-
# material themes registered above — the same mechanism the ground paints with, since a made
# thing's colour is stated the same way a ground's is. ─────────────────────────────────────
BALLOON_X, BALLOON_Z, BALLOON_Y = -50, 45, 62
balloon = [
    ("lower", [disc("bl-lo", BALLOON_X, BALLOON_Z, 7, BALLOON_Y, 5, "canvas-red")]),
    ("mid", [disc("bl-mid", BALLOON_X, BALLOON_Z, 9, BALLOON_Y + 5, 6, "canvas-white")]),
    ("upper", [disc("bl-up", BALLOON_X, BALLOON_Z, 6, BALLOON_Y + 11, 5, "canvas-red")]),
    ("cap", [disc("bl-cap", BALLOON_X, BALLOON_Z, 2, BALLOON_Y + 16, 2, "canvas-white")]),
    ("basket", [rect("bl-bk", BALLOON_X - 1, BALLOON_Z - 1, BALLOON_X + 2, BALLOON_Z + 2,
                      BALLOON_Y - 4, 3, "timber-dark", keep=False)]),
]
for name, shapes in balloon:
    layout["layers"].append(prop_layer(f"balloon-{name}", "balloon", shapes))

for n, (cx, cz, y) in enumerate(((-15, 65, 78), (-95, 100, 74))):
    lobes = [disc(f"cl{n}-0", cx, cz, 9, y, 3, "cloud-glass"),
             disc(f"cl{n}-1", cx - 8, cz + 3, 6, y, 3, "cloud-glass"),
             disc(f"cl{n}-2", cx + 7, cz - 3, 6, y, 3, "cloud-glass")]
    layout["layers"].append(prop_layer(f"cloud-{n}", f"cloud-{n}", lobes))

BOAT_X, BOAT_Z = -108, 52
boat = [
    ("keel", [rect("bt-k", BOAT_X - 5, BOAT_Z - 2, BOAT_X + 5, BOAT_Z + 2, WATER - 3, 3,
                    "hull-log", keep=False)]),
    ("hull", [rect("bt-h", BOAT_X - 7, BOAT_Z - 3, BOAT_X + 7, BOAT_Z + 3, WATER, 2,
                    "timber-dark", keep=False)]),
    ("deck", [rect("bt-d", BOAT_X - 8, BOAT_Z - 4, BOAT_X + 8, BOAT_Z + 4, WATER + 2, 1,
                    "hull-plank", keep=False)]),
    ("cabin", [rect("bt-c", BOAT_X - 2, BOAT_Z - 2, BOAT_X + 3, BOAT_Z + 2, WATER + 3, 3,
                     "timber-dark", keep=False)]),
    ("mast", [rect("bt-m", BOAT_X - 5, BOAT_Z, BOAT_X - 4, BOAT_Z + 1, WATER + 3, 8,
                    "hull-log", keep=False)]),
]
for name, shapes in boat:
    layout["layers"].append(prop_layer(f"boat-{name}", "boat", shapes))

# The airplane: a fuselage along x, wings crossing it, a fin and stabilizer at the tail.
PX, PZ, PY = -58, 55, 58
plane = [
    ("fuselage", [rect("pl-f", PX - 12, PZ - 1, PX + 12, PZ + 1, PY, 3, "metal-white", keep=False)]),
    ("wing", [rect("pl-w", PX - 3, PZ - 14, PX + 2, PZ + 14, PY + 1, 1, "metal-white", keep=False)]),
    ("fin", [rect("pl-fin", PX + 9, PZ - 1, PX + 12, PZ + 1, PY + 3, 4, "canvas-red", keep=False)]),
    ("stabilizer", [rect("pl-stab", PX + 8, PZ - 6, PX + 12, PZ + 6, PY + 3, 1,
                          "metal-white", keep=False)]),
]
for name, shapes in plane:
    layout["layers"].append(prop_layer(f"plane-{name}", "plane", shapes))

# The statue: a guardian at the north bridgehead, plinth to head, one layer per vertical run.
SX, SZ, SY = -78, 82, BANK
statue = [
    ("plinth", [rect("st-p", SX - 4, SZ - 4, SX + 4, SZ + 4, SY, 3, "statue-stone", keep=False)]),
    ("body", [rect("st-b", SX - 2, SZ - 2, SX + 2, SZ + 2, SY + 3, 10, "statue-stone", keep=False)]),
    ("arms", [rect("st-a1", SX - 4, SZ - 1, SX - 2, SZ + 1, SY + 9, 5, "statue-stone", keep=False),
              rect("st-a2", SX + 2, SZ - 1, SX + 4, SZ + 1, SY + 9, 5, "statue-stone", keep=False)]),
    ("head", [rect("st-h", SX - 1, SZ - 1, SX + 1, SZ + 1, SY + 13, 3, "statue-stone", keep=False)]),
]
for name, shapes in statue:
    layout["layers"].append(prop_layer(f"statue-{name}", "statue", shapes, seat="ground"))

# ── intent: meta, and the destroyable-1 anchor lowered to match the pit ────────────────────
intent["meta"]["name"] = "Cutwater"
intent["meta"]["created"] = "2026-08-30"
intent["meta"]["authors"] = ["Sonnet 5"]
for goal in intent["destroyables"]:
    if (goal.get("stamp") or {}).get("unit") == "destroyable-1":
        goal["anchor"]["y"] = 21          # the pit's ring height — measured, not the flat bank's 30

# No finish.json: its mere presence now tells the driver this spec is compiled from its plan
# every run, discarding a drawn layout/intent as if they were only its output. This board's
# geometry IS the layout, so authorship rides directly on intent.meta instead, set above.
json.dump(plan, open(SPEC + ".plan.json", "w"), indent=1)
json.dump(layout, open(SPEC + ".layout.json", "w"), indent=1)
json.dump(intent, open(SPEC + ".intent.json", "w"), indent=1)
print(f"wrote {len(layout['layers'])} layers, {len(ground['shapes'])} ground shapes, "
      f"{len(layout['dressing']['props'])} dressing props")
