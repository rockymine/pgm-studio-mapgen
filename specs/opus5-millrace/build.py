"""Millrace — the author's basin flooded, walled, and bridged."""
import json, sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user/645c418a-90ec-5c70-a0a2-d0b1a374602f/scratchpad")

ROOT = "/home/user/pgm-studio-mapgen"
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
BRIDGE_X = -100
STAIR_W, STAIR_E = -76, -62          # the one flight down to the water, on the moor side

def built(sid, pts, radius, floor, height, th="masonry", seed=7, level=True):
    s = {"id":sid,"type":"path","operation":"add","override":True,"keepClear":True,
         "vertices":pts,"radius":radius,"path_edge":"solid","path_seed":seed,
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
SPX0, SPZ0, SPX1, SPZ1, TERRACE = -104, 94, -76, 120, 40
edges.append({"id":"spawn-terrace","type":"rectangle","operation":"add","override":True,
  "keepClear":False,"min_x":SPX0,"max_x":SPX1,"min_z":SPZ0,"max_z":SPZ1,
  "floor":24,"base_height":TERRACE-24,"height_mode":"level","skirt":0,
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
Z0, Z1 = zon(SOUTH[0], SOUTH[1], BRIDGE_X)-7, zon([-108,73],[-90,76], BRIDGE_X)+7

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
            spring=BED+1, crown_rise=8, piers=(57,), pier_foot=BED-1)
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
    return {"id":lid,"name":lid,"base_y":0,"kind":"prop","prop":prop,
            "layout":{"shapes":shapes,"groups":[{"id":lid+"-body","name":prop,"mirrors":mirrors,
                      "shapeIds":[s["id"] for s in shapes]}]}}
def disc(sid, cx, cz, r, floor, h, th):
    return {"id":sid,"type":"circle","operation":"add","center_x":cx,"center_z":cz,"radius":r,
            "floor":floor,"base_height":h,"theme":th,"keepClear":False}

# A cloud is a flat base and a lumpy silhouette: lobes at ONE floor and one height, so they merge
# into a single span instead of the tallest eating the rest.
for n, (cx, cz, y) in enumerate(((-46, 128, 86), (16, 86, 80))):
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

layout["dressing"] = {"props": [
 {"id":"race-water","kind":"water","seed":7,"layer":"ground","shape":"pool","points":S0,
  "radius":26,"depth":10,"shore":1,"shoreWander":False,"edge":0.6,"level":WATER,
  "bank":{"kind":"solid","id":13,"data":0}},
]}

json.dump({"authors":["Opus 5"],"created":"2026-08-30"}, open(SPEC + ".finish.json","w"), indent=1)
json.dump(plan,   open(SPEC + ".plan.json","w"),   indent=1)
json.dump(layout, open(SPEC + ".layout.json","w"), indent=1)
json.dump(intent, open(SPEC + ".intent.json","w"), indent=1)
print(f"wrote {len(layout['layers'])} layers, {len(ground['shapes'])} ground shapes")
