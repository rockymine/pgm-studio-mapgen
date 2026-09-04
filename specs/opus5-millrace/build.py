"""Millrace — the author's basin flooded, walled, and bridged."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = f"{ROOT}/specs/opus5-millrace/opus5-millrace"
plan   = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.plan.json"))
layout = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.layout.json"))
intent = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.intent.json"))

# G5 is the one hard term the base fails: the island sits 25 blocks off the mainland against a
# band of 10..20, and the short alternative lies outside the build zone. The goals are the
# author's and stay exactly where they were drawn.
for q in plan["pieces"]:
    if q["id"] == "piece":   q["rect"] = [-21, 14, 23, 10]
    if q["id"] == "piece-4": q["rect"] = [1, 5, 10, 9]
plan["meta"]["name"] = "Millrace"

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, PODZOL, DIRT, COARSE = solid(2), solid(3,2), solid(3,0), solid(3,1)
STONE, ANDESITE, COBBLE, MOSSY_C, GRAVEL = solid(1), solid(1,5), solid(4), solid(48), solid(13)
SBRICK, MOSSY_B, CRACKED = solid(98), solid(98,1), solid(98,2)
LOG, PLANK_S, PLANK_D = solid(17), solid(5,1), solid(5,2)
WHITE_G, RED_W, WHITE_W = solid(95,0), solid(35,14), solid(35,0)

def noise(a, b, scale, seed, rise=2):
    return {"kind":"noise","seed":seed,"scale":scale,"octaves":4,"stops":[a,b],"rise":rise}
def theme(surf, wall, fill, depth=1):
    return {"bedrock":{"relative":False,"value":1},"wallOnTerrainFaces":False,
            "surface":{"enabled":True,"depth":depth,"material":surf},
            "wall":wall,"wallEnabled":True,"fill":fill,
            "rim":{"enabled":False,"depth":1,"material":STONE},"rimEdges":"boundary"}
def flat(b): return theme(b, b, b)

# Three grounds. Each noise pair is two shades of ONE family, so it reads as grain; where two
# grounds meet, the edge is a drawn shape and never a sampled field.
THEMES = {
 "moor": theme(GRASS, noise(STONE,ANDESITE,20,12), noise(STONE,ANDESITE,20,12)),
 "worn": theme(noise(COARSE,DIRT,18,13), noise(STONE,ANDESITE,20,12), noise(STONE,ANDESITE,20,12)),
 "wold": theme(noise(COARSE,DIRT,22,21), noise(STONE,COBBLE,17,22), noise(STONE,COBBLE,17,22)),
 "holm": theme(noise(PODZOL,COARSE,14,31), noise(STONE,MOSSY_C,13,32), noise(STONE,MOSSY_C,13,32)),
 "masonry": theme(noise(SBRICK,MOSSY_B,11,41), noise(SBRICK,CRACKED,11,42), noise(SBRICK,CRACKED,11,42)),
 "timber": flat(PLANK_S), "stone-pale": flat(solid(1,3)),
 "envelope": flat(RED_W), "envelope2": flat(WHITE_W), "basket": flat(PLANK_D),
 "hull": flat(PLANK_D), "cloud": flat(WHITE_G),
}

# ── the basin, and the wall that traces it ───────────────────────────────────
S0 = [[-132,49],[-125,35],[-82,43],[-46,30],[-15,35],[-7,54],[-15,70],[-40,62],[-90,76],[-108,73],[-125,70]]
SOUTH = [[-125,35],[-82,43],[-46,30],[-15,35]]
NORTH = [[-15,70],[-40,62],[-90,76],[-108,73],[-125,70]]
def zon(a, b, x): return a[1] + (x-a[0])*(b[1]-a[1])/(b[0]-a[0])
NB = lambda x: zon([-90,76], [-40,62], x)
BANK, WALL_TOP, WALL_FLOOR, WATER, BED = 30, 31, 12, 25, 17
BRIDGE_X = -48          # in einer Flucht mit der Querung zur Spiegel-Insel
STAIR_W, STAIR_E = -76, -62          # the one flight down to the water, on the moor side

def built(sid, pts, radius, floor, height, th="masonry", seed=7, level=True):
    s = {"id":sid,"type":"polyline","operation":"add","override":True,"keepClear":True,
         "vertices":pts,"radius":radius,"stroke_edge":"solid","stroke_seed":seed,
         "floor":floor,"base_height":height,"skirt":0,"relief_scope":"exclude","theme":th}
    if level: s["height_mode"] = "level"
    return s

ground = layout["layers"][0]["layout"]
for s in ground["shapes"]:
    s["theme"] = {"s0":"wold","s1":"moor","s2":"wold","s3":"holm"}.get(s["id"], s.get("theme"))

edges = [
  built("wall-s", SOUTH, 1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
  built("wall-n-w", [[-125,70],[-108,73],[-90,76],[STAIR_W, NB(STAIR_W)]], 1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
  built("wall-n-e", [[STAIR_E, NB(STAIR_E)],[-40,62],[-15,70]], 1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
  # the flight down to the water: a tilted quad, `exclude` only, so the per-vertex tilt survives
  {"id":"water-stair","type":"polygon","operation":"add","override":True,"keepClear":True,
   "vertices":[[STAIR_W,NB(STAIR_W)+4],[STAIR_E,NB(STAIR_E)+4],[STAIR_E,NB(STAIR_E)-22],[STAIR_W,NB(STAIR_W)-22]],
   "anchor_heights":[BANK-WALL_FLOOR, BANK-WALL_FLOOR, WATER-2-WALL_FLOOR, WATER-2-WALL_FLOOR],
   "floor":WALL_FLOOR,"base_height":BANK-WALL_FLOOR,"skirt":0,"relief_scope":"exclude","theme":"masonry"},
]

import math as _m
def arc(cx, cz, r, a0, a1, step=9):
    return [[round(cx + r*_m.cos(_m.radians(a))), round(cz + r*_m.sin(_m.radians(a)))]
            for a in range(a0, a1 + 1, step)]

# Three open runs at radius 20 round the author's own monument — the race wall's construction at a
# smaller scale, with gaps a player walks through rather than a ring nobody can enter.
MX, MZ = -90, 18
edges += [built(f"cairn-wall-{i}", arc(MX, MZ, 20, a0, a1), 1.0, 24, 11, seed=11+i)
          for i, (a0, a1) in enumerate(((20, 100), (145, 230), (265, 340)))]

# The spawn stood on ground rising 7 blocks under its own footprint, so the room was stamped on the
# lowest column of it and sat in a hole. It gets a terrace instead, level with the bank it adjoins.
# Vom Rand aus gewachsen: 7 Bloecke nach Westen in den Void (der Moor endet dort bei x -110),
# 15 nach Osten auf die Statue zu, 5 nach Norden in den Void (die Moorkante liegt bei z 121).
# Der Sockel steht von y0, sonst haengt er ueber Leere -- ein override-Add gewinnt die Saeule
# mitsamt ihrem Boden, also war unter floor 24 nichts.
SPX0, SPZ0, SPX1, SPZ1, TERRACE = -104-7, 94, -76+15, 120+5, 40
edges.append({"id":"spawn-terrace","type":"rectangle","operation":"add","override":True,
  "keepClear":False,"min_x":SPX0,"max_x":SPX1,"min_z":SPZ0,"max_z":SPZ1,
  "floor":0,"base_height":TERRACE,"height_mode":"level","skirt":0,
  "relief_scope":"exclude","theme":"masonry"})
# and a flight off its south face into the grass, the way the water stair goes down to the water
edges.append({"id":"spawn-stair","type":"polygon","operation":"add","override":True,"keepClear":True,
  "vertices":[[-97,SPZ0+2],[-85,SPZ0+2],[-85,SPZ0-14],[-97,SPZ0-14]],
  "anchor_heights":[TERRACE-24, TERRACE-24, 8, 8],
  "floor":24,"base_height":TERRACE-24,"skirt":0,"relief_scope":"exclude","theme":"masonry"})

ground["shapes"].extend(edges)
ground["groups"][0]["shapeIds"] = ["s0","s1","s2"] + [e["id"] for e in edges]
TEAM, ISLE = ground["groups"][0]["id"], ground["groups"][1]["id"]

# ── the bridge: a deck, two parapets and four piers, on its own layer ────────
def rect(sid, x0, z0, x1, z1, floor, h, th, keep=True):
    return {"id":sid,"type":"rectangle","operation":"add","override":True,"keepClear":keep,
            "min_x":x0,"max_x":x1,"min_z":z0,"max_z":z1,"floor":floor,"base_height":h,
            "height_mode":"level","skirt":0,"relief_scope":"exclude","theme":th}
def basin_span(x):
    """The basin's z extent at this x, read off its own ring so the span follows the shape."""
    hits = []
    for i in range(len(S0)):
        (ax, az), (bx, bz) = S0[i], S0[(i + 1) % len(S0)]
        if (ax <= x <= bx) or (bx <= x <= ax):
            if ax != bx: hits.append(az + (x - ax) * (bz - az) / (bx - ax))
    return (min(hits), max(hits)) if len(hits) >= 2 else (0, 0)

_zlo, _zhi = basin_span(BRIDGE_X)
Z0, Z1 = _zlo - 7, _zhi + 7

def arch(sid, axis, a0, a1, cross0, cross1, spring, crown_rise, piers, pier_foot,
         theme_id="masonry", base=None):
    """A bridge drawn as one slice per block along its span: the deck rises to a crown, and the
    masonry under it springs from each pier in an arc, so the openings are voids rather than a
    solid wall. Piers stand where `piers` names them and carry down to `pier_foot`."""
    import math
    out, span = [], a1 - a0
    lo, hi = (BANK, BANK) if base is None else (base if isinstance(base, tuple) else (base, base))
    def deck_at(a):
        f = (a - a0) / span
        return round(lo + (hi - lo) * f + crown_rise * math.sin(math.pi * f))
    stops = [a0] + list(piers) + [a1]
    for a in range(int(a0), int(a1) + 1):
        top = deck_at(a)
        if any(abs(a - q) <= 4 for q in piers):
            floor = pier_foot                                     # a pier, founded in the bed
        else:
            left = max([q for q in stops if q <= a], default=a0)
            right = min([q for q in stops if q >= a], default=a1)
            half, mid = max((right - left) / 2, 1), (left + right) / 2
            r = max(0.0, 1 - ((a - mid) / half) ** 2) ** 0.5
            floor = int(round(spring + (top - 2 - spring) * r))   # the soffit, highest at mid-span
        lo_c, hi_c = cross0, cross1
        if axis == "z":
            out.append(rect(f"{sid}-{a}", lo_c, a, hi_c, a + 1, floor, top - floor + 1, theme_id))
            out.append(rect(f"{sid}-pw-{a}", lo_c - 2, a, lo_c, a + 1, top + 1, 3, theme_id))
            out.append(rect(f"{sid}-pe-{a}", hi_c, a, hi_c + 2, a + 1, top + 1, 3, theme_id))
        else:
            out.append(rect(f"{sid}-{a}", a, lo_c, a + 1, hi_c, floor, top - floor + 1, theme_id))
            out.append(rect(f"{sid}-pw-{a}", a, lo_c - 2, a + 1, lo_c, top + 1, 3, theme_id))
            out.append(rect(f"{sid}-pe-{a}", a, hi_c, a + 1, hi_c + 2, top + 1, 3, theme_id))
    return out

# Over the water: three piers founded in the bed, a crown eight courses over the bank.
# Two arches over one mid-stream pier, and the soffit springs from BED+1 -- below the water line,
# so the race runs through the openings instead of being dammed by them.
span = arch("race-bridge", "z", Z0, Z1, BRIDGE_X-6, BRIDGE_X+6,
            spring=BED+1, crown_rise=8, piers=(round((_zlo+_zhi)/2),), pier_foot=BED-1)
# The second crossing runs the SAME way as the one over the water -- along z at a constant x --
# from the wold the monument and its ring stand on, south over the build region to the mirrored
# middle island. The fan makes the matching span on the other half. Measured: at x -48 the wold's
# south edge is z 3 and the island's north edge z -30, the shortest crossing between the two.
HOLM_X = -48
span += arch("holm-bridge", "z", -34, 8, HOLM_X-6, HOLM_X+6,
             spring=22, crown_rise=3, piers=(), pier_foot=22, base=(29, 37))
layout["layers"] = [layout["layers"][0],
  {"id":"spans","name":"spans","base_y":0,"layout":{"shapes":span,
   "groups":[{"id":"spans-body","name":"spans","mirrors":True,
              "shapeIds":[s["id"] for s in span]}]}}]

# ── relief: rolling banks, not a flat table with knobs on ───────────────────
# Relief, on the showcases' own scale: a small `r` and a FINITE `reach`, which is what makes a
# mark a local landform. `reach: 0` is unlimited, so every mark reaches every cell and the field
# comes out as the contour steps RL2 calls ground that was cut rather than shaped.
BASIN = [[-122,38],[-82,46],[-46,33],[-18,38],[-11,54],[-18,67],[-40,65],[-90,73],[-107,70],[-122,67]]
# A `point` mark's `r` is a FLAT core, so a point above base builds a small mesa with sheer sides —
# which is what RL2 counts as a barrier. A `push` is the landform tool: a ring raised by `amount`
# with `falloff` blocks of blend around it, and a `crown` that rounds the top.
BASIN = [[-122,38],[-82,46],[-46,33],[-18,38],[-11,54],[-18,67],[-40,65],[-90,73],[-107,70],[-122,67]]
MOOR  = [[-113,95],[-108,73],[-90,76],[-40,62],[1,75],[13,96],[5,120],[-34,131],[-68,122],[-105,120]]
WOLD  = [[-122,15],[-115,0],[-89,-20],[-65,-2],[-33,6],[-15,35],[-46,30],[-82,43],[-125,35]]
def ring(cx, cz, rx, rz, n=9):
    import math
    return [[round(cx + rx*math.cos(2*math.pi*i/n)), round(cz + rz*math.sin(2*math.pi*i/n))]
            for i in range(n)]
layout["relief"] = {
 TEAM: {"base":BANK,"reach":34,"step":1,"stairs":True,"landform":"moor",
   "grain":{"amplitude":1.1,"scale":19,"seed":5},
   "marks":[
     {"id":"basin","kind":"area","h":BED,"ring":S0},
     {"id":"moor-bank","kind":"area","h":BANK,"ring":MOOR},
     {"id":"wold-bank","kind":"area","h":BANK,"ring":WOLD}],
   "pushes":[
     {"id":"moor-brow","ring":ring(-42,116,34,15),"amount":6,"falloff":30,"roughness":0.4,"crown":4,"seed":5},
     {"id":"moor-swell","ring":ring(-88,106,20,12),"amount":5,"falloff":20,"roughness":0.35,"crown":3,"seed":6},
     {"id":"wold-fell","ring":ring(-104,6,30,17),"amount":7,"falloff":32,"roughness":0.45,"crown":4,"seed":7},
     {"id":"wold-swell","ring":ring(-46,8,22,13),"amount":5,"falloff":20,"roughness":0.35,"crown":3,"seed":8},
     # the quarry the author's own monument stands in, graded rather than punched
     {"id":"quarry","ring":ring(-90,18,16,11),"amount":-7,"falloff":18,"roughness":0.3,"crown":3,"seed":9}]},
 ISLE: {"base":25,"reach":26,"step":1,"stairs":True,"landform":"knoll",
   "grain":{"amplitude":0.8,"scale":14,"seed":9},
   "marks":[],
   "pushes":[{"id":"crown","ring":ring(48,50,20,13),"amount":6,"falloff":26,"roughness":0.4,"crown":4,"seed":11}]},
}
layout["themes"], layout["mapTheme"] = THEMES, "moor"
STYLE = json.load(open(f"{ROOT}/tools/styles/17h-croft.json"))
VARIANT = json.loads(json.dumps(STYLE))
SWAP = {(4,0): (1,5), (98,0): (1,0), (98,1): (1,5)}      # the variation is a greyer stone, not sandstone
def repaint(n):
    if isinstance(n, dict):
        if n.get("kind") == "solid" and (n.get("id"), n.get("data", 0)) in SWAP:
            n["id"], n["data"] = SWAP[(n["id"], n.get("data", 0))]; return n
        for v in n.values(): repaint(v)
    elif isinstance(n, list):
        for v in n: repaint(v)
repaint(VARIANT)
layout["roomStyles"] = {"spawn": json.load(open(f"{ROOT}/tools/styles/showcase-hall.json"))}
def prop_layer(lid, prop, shapes, mirrors=True):
    return {"id":lid,"name":lid,"base_y":0,"kind":"made","part_of":prop,
            "layout":{"shapes":shapes,"groups":[{"id":lid+"-body","name":prop,"mirrors":mirrors,
                      "shapeIds":[s["id"] for s in shapes]}]}}
def disc(sid, cx, cz, r, floor, h, th):
    return {"id":sid,"type":"circle","operation":"add","center_x":cx,"center_z":cz,"radius":r,
            "floor":floor,"base_height":h,"theme":th,"keepClear":False}

# A cloud is a flat base and a lumpy silhouette: lobes at ONE floor and one height, so they merge
# into a single span instead of the tallest eating the rest.
#
# Both stand on the x + z = 0 diagonal at a height that clears the board's own isometric
# silhouette. An isometric read draws a block at (x + z) / 2 - y, so a cloud off the diagonal has
# its -x, -z image drawn as far above the board as the original is drawn into it, and one too low
# on the diagonal lands on the terrain in both.
for n, (cx, cz, y) in enumerate(((-118, 118, 104), (-30, 30, 108))):
    lobes = [disc(f"cl{n}-0", cx, cz, 13, y, 3, "cloud"),
             disc(f"cl{n}-1", cx-11, cz+5, 8, y, 3, "cloud"),
             disc(f"cl{n}-2", cx+12, cz-4, 9, y, 3, "cloud"),
             disc(f"cl{n}-3", cx+3, cz+9, 7, y, 3, "cloud")]
    layout["layers"].append(prop_layer(f"cloud-{n}", f"cloud-{n}", lobes))

# A statue over the race, on the moor brow. One layer per vertical run: a layer keeps one span per
# column, so a plinth written beside the torso above it is simply not in the world.
SX, SZ, SY = -30, 96, 34
statue = [("plinth", [rect("st-p", SX-5, SZ-5, SX+5, SZ+5, SY, 4, "masonry", keep=False)]),
          ("legs",   [rect("st-l1", SX-3, SZ-2, SX-1, SZ+2, SY+4, 9, "stone-pale", keep=False),
                      rect("st-l2", SX+1, SZ-2, SX+3, SZ+2, SY+4, 9, "stone-pale", keep=False)]),
          ("torso",  [rect("st-t", SX-4, SZ-3, SX+4, SZ+3, SY+13, 11, "stone-pale", keep=False)]),
          ("arms",   [rect("st-a1", SX-6, SZ-2, SX-4, SZ+2, SY+16, 7, "stone-pale", keep=False),
                      rect("st-a2", SX+4, SZ-2, SX+6, SZ+2, SY+16, 7, "stone-pale", keep=False)]),
          ("head",   [rect("st-h", SX-2, SZ-2, SX+2, SZ+2, SY+24, 5, "stone-pale", keep=False)])]
for name, shapes in statue:
    layout["layers"].append(prop_layer(f"statue-{name}", "statue", shapes))

# A lighter moored in the wide reach west of the bridge: keel bedded in the water, hull to the
# waterline, a deck over it, a cabin aft and a mast carrying two courses of canvas. The rig shares
# one layer with the cabin because they stand on different columns, and a layer holds one span per
# column rather than one shape.
BX, BZ, WATERLINE = -100, 57, WATER
lighter = [("keel",  [rect("bt-k", BX-7, BZ-2, BX+7, BZ+2, WATERLINE-3, 3, "hull", keep=False)]),
           ("hull",  [rect("bt-h", BX-10, BZ-4, BX+10, BZ+4, WATERLINE, 3, "hull", keep=False)]),
           ("deck",  [rect("bt-d", BX-11, BZ-5, BX+11, BZ+5, WATERLINE+3, 1, "timber", keep=False)]),
           ("cabin", [rect("bt-c", BX+2, BZ-2, BX+8, BZ+2, WATERLINE+4, 4, "timber", keep=False)]),
           # A rectangle's max edge is exclusive, so a mast is stated as two columns to build one.
           # The sail hangs one block aft of it rather than through it: a layer holds one span per
           # column, so a plate crossing the mast's own column would take the mast's place in it.
           ("rig",   [rect("bt-m", BX-4, BZ-1, BX-3, BZ, WATERLINE+4, 19, "hull", keep=False),
                      rect("bt-s", BX-3, BZ-6, BX-2, BZ+6, WATERLINE+5, 15, "envelope2", keep=False)])]
for name, shapes in lighter:
    layout["layers"].append(prop_layer(f"lighter-{name}", "lighter", shapes))

# ── dressing: the water, the woods, the erratics and the crofts ─────────────
# Every coordinate below was read off the built world rather than guessed: a site is a cell whose
# 5x5 neighbourhood varies by one block, carries nothing standing on it, and lies clear of the
# goals, the spawn and the statue. A prop is stated once on the red half; the symmetry fan writes
# its image.
def tree(pid, x, z, wood, height, **knobs):
    base = {"id":pid,"kind":"tree","seed":abs(x*31+z*17)%9973,"layer":"ground","form":"grown",
            "x":x,"z":z,"wood":wood,"height":height,"stems":1,"levels":2}
    return base | knobs

# A broadleaf: a low leader, a wandering trunk and a wide fork, so the crown spreads.
def oak(pid, x, z, height):
    return tree(pid, x, z, "oak", height, leader=0.5, flow=0.5, branchAngle=1.15,
                leafSize=0.68, whorled=False)

# A conifer: the branches gathered into whorls, each ring shorter than the one below, on a leader
# that climbs almost the whole height -- which is the spire the earth banks want.
def fir(pid, x, z, height):
    return tree(pid, x, z, "spruce", height, leader=0.78, flow=0.2, branchAngle=0.8,
                leafSize=0.58, whorled=True)

OAKS = [(-62,80,12), (-21,83,10), (-106,86,13), (-51,112,11), (-40,114,13),
        (-30,117,9), (-16,118,12), (-52,122,10), (-39,124,13)]
FIRW = [(-100,-7,18), (-63,2,14), (-37,9,13), (-32,18,16), (-101,28,15), (-91,32,13)]
FIRI = [(-52,-67,14), (-35,-67,12), (-65,-43,16), (-32,-36,13)]

# Four forms at four scales, so the erratics can be read against each other: a rounded mass, the
# same mass broken up, a low outcrop with its middle at the surface, and three shrinking lobes.
GNEISS  = noise(STONE, COBBLE, 3, 51)     # stone mottled with cobble, in the rock's own frame
GRIT    = noise(STONE, GRAVEL, 2, 52)     # stone shot through with gravel
BOULDERS = [("erratic-round",  -10,  80, "round",   5, GNEISS),
            ("erratic-broken", -77,  84, "angular", 7, GNEISS),
            ("erratic-shelf",  -56,  93, "outcrop", 8, GRIT),
            ("erratic-cairn",   -6, 115, "cairn",   4, GNEISS),
            ("erratic-crag",   -75,  17, "angular", 6, GRIT),
            ("erratic-cobble",-118,  23, "round",   4, GRIT),
            ("erratic-ledge",  -35, -54, "outcrop", 7, GNEISS),
            ("erratic-stack",  -66, -54, "cairn",   4, GRIT)]

def house(pid, x0, z0, x1, z1, style, front):
    return {"id":pid,"kind":"house","seed":abs(x0*7+z0*13)%9973,"layer":"ground",
            "wings":[{"corners":[[x0,z0],[x1,z1]]}],"front":front,"style":style}

layout["dressing"] = {"props": [
 {"id":"race-water","kind":"water","seed":7,"layer":"ground","shape":"pool","points":S0,
  "radius":26,"depth":10,"shore":1,"shoreWander":False,"edge":0.6,"level":WATER,
  "bank":{"kind":"solid","id":13,"data":0}},
 # Two crofts on the spawn plaza, clear of the band round the spawn room so nothing stands in
 # front of its door whichever wall it is cut through.
 house("croft-quay",   -77,  96, -67, 106, STYLE,   "posX"),
 house("croft-yard",   -78, 112, -68, 121, VARIANT, "negZ"),
 # One on the earth bank the monument stands on, one on the moor above the water,
 house("croft-fell",   -93, -13, -86,  -7, STYLE,   "posZ"),
 house("croft-bank",   -37,  69, -27,  78, VARIANT, "posZ"),
 # and one on the holm the second crossing lands on.
 house("croft-holm",   -53, -54, -45, -47, VARIANT, "posZ"),
] + [oak(f"oak-{n}", x, z, h) for n, (x, z, h) in enumerate(OAKS)]
  + [fir(f"fir-{n}", x, z, h) for n, (x, z, h) in enumerate(FIRW + FIRI)]
  + [{"id":pid,"kind":"boulder","seed":abs(x*11+z*5)%9973,"layer":"ground",
      "x":x,"z":z,"form":form,"size":size,"rock":rock,"mossy":True}
     for pid, x, z, form, size, rock in BOULDERS]}

# A drawn spec carries no finish -- the driver reads one as a compile recipe and would run the compile
# over the top of this layout -- so what a finish would have stated about the map is stated here.
intent.setdefault("meta", {}).update({"name": "Millrace", "authors": ["Opus 5"],
                                      "created": "2026-08-30"})
json.dump(plan,   open(SPEC + ".plan.json","w"),   indent=1)
json.dump(layout, open(SPEC + ".layout.json","w"), indent=1)
json.dump(intent, open(SPEC + ".intent.json","w"), indent=1)
print(f"wrote {len(layout['layers'])} layers, {len(ground['shapes'])} ground shapes")
