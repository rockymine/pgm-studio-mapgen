"""Millrace — a walled water course cut down the sunken basin of the author's base board."""
import json, sys
sys.path.insert(0, "/tmp/claude-0/-home-user/645c418a-90ec-5c70-a0a2-d0b1a374602f/scratchpad")
from api import post

ROOT = "/home/user/pgm-studio-mapgen"
SPEC = f"{ROOT}/specs/opus5-millrace/opus5-millrace"
SLUG, NAME = "opus5-millrace", "Millrace"
plan   = json.load(open(SPEC + ".plan.json"))
layout = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.layout.json"))
intent = json.load(open(f"{ROOT}/specs/rockymine-map-experiment/map-experiment.intent.json"))

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS,PODZOL,DIRT,COARSE = solid(2),solid(3,2),solid(3,0),solid(3,1)
STONE,ANDESITE,SBRICK,MOSSY_B,CRACKED = solid(1),solid(1,5),solid(98),solid(98,1),solid(98,2)
GRAVEL,COBBLE,MOSSY_C = solid(13),solid(4),solid(48)
SANDSTONE,SMOOTH_SS = solid(24),solid(24,2)
DARKGLASS,WHITEGLASS = solid(95,15),solid(95,0)
PLANK_D,PLANK_S,LOG = solid(5,5),solid(5,1),solid(17)

def noise(a,b,scale,seed,rise=2,oct=4):
    return {"kind":"noise","seed":seed,"scale":scale,"octaves":oct,"stops":[a,b],"rise":rise}
def theme(surf, wall, fill, depth=1):
    return {"bedrock":{"relative":False,"value":1},"wallOnTerrainFaces":True,
            "surface":{"enabled":True,"depth":depth,"material":surf},
            "wall":wall,"wallEnabled":True,"fill":fill,
            "rim":{"enabled":False,"depth":1,"material":STONE},"rimEdges":"boundary"}
def flat(b): return theme(b, b, b)

# Three grounds, each a place, each two blocks of one family so the noise is grain and not static.
THEMES = {
 "moor": theme(noise(GRASS,PODZOL,26,11), noise(STONE,ANDESITE,18,12), noise(STONE,ANDESITE,18,12)),
 "wold": theme(noise(COARSE,DIRT,24,21), noise(SANDSTONE,SMOOTH_SS,16,22), noise(SANDSTONE,SMOOTH_SS,16,22)),
 "holm": theme(noise(MOSSY_C,GRAVEL,15,31), noise(STONE,COBBLE,14,32), noise(STONE,COBBLE,14,32)),
 # what people built here: both race walls, the sluice and both spans, in one stone.
 "masonry": theme(noise(SBRICK,MOSSY_B,12,41), noise(SBRICK,CRACKED,12,42), noise(SBRICK,CRACKED,12,42)),
 # made things, which are materials rather than places
 "sign-face": flat(WHITEGLASS), "sign-back": flat(DARKGLASS),
 "hull": flat(PLANK_D), "gunwale": flat(LOG), "sail": flat(solid(35,0)),
 "envelope": flat(solid(35,14)), "basket": flat(PLANK_S), "cloud": flat(WHITEGLASS),
}

SOUTH_BANK = [[-125,35],[-82,43],[-46,30],[-15,35]]
NORTH_BANK = [[-15,70],[-40,62],[-90,76],[-108,73],[-125,70]]
def edge_z(a,b,x): return a[1] + (x-a[0])*(b[1]-a[1])/(b[0]-a[0])
BANK_TOP, BASIN_TOP, WALL_TOP, WALL_FLOOR = 30, 25, 31, 15
SLUICE_X, BRIDGE_X, WATER_LEVEL = -70, -100, 23

def built(sid, pts, radius, floor, height, theme_id="masonry", seed=7):
    """A made edge: thin, sheer, holding its own top out of the relief."""
    return {"id":sid,"type":"path","operation":"add","override":True,"keepClear":True,
            "vertices":pts,"radius":radius,"path_edge":"solid","path_seed":seed,
            "floor":floor,"base_height":height,"height_mode":"level","skirt":0,
            "relief_scope":"exclude","theme":theme_id}

ground = layout["layers"][0]["layout"]
for s in ground["shapes"]:
    s["theme"] = {"s0":"wold","s1":"moor","s2":"wold","s3":"holm"}.get(s["id"], s.get("theme"))

# The walls the author asked for: thin open shapes traced along the basin's own outline,
# two blocks thick, standing sheer from the bed to a course above the bank.
def ramp(sid, x0_, x1, z_top, z_bot, y_top, y_bot, floor=WALL_FLOOR):
    """A tilted quad is a stair: the surface is floored per cell, so it climbs a course at a time."""
    return {"id":sid,"type":"polygon","operation":"add","override":True,"keepClear":True,
            "vertices":[[x0_,z_top],[x1,z_top],[x1,z_bot],[x0_,z_bot]],
            "anchor_heights":[y_top-floor, y_top-floor, y_bot-floor, y_bot-floor],
            "floor":floor,"base_height":y_top-floor,
            # `exclude` alone: it keeps the per-vertex tilt, where `level` would cut the ramp flat.
            "skirt":0,"relief_scope":"exclude","theme":"masonry"}

# The north wall is two runs with a gate between them, because a yard nobody can walk into
# is ground the export refuses to reach (EX1) and the monument stands in it.
WHARF_W, WHARF_E = -86, -74
GATE_W, GATE_E = -64, -52
NB = lambda x: edge_z([-90,76], [-40,62], x)     # the long north lip, which both gates cut
edges = [built("race-wall-s", SOUTH_BANK, 1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
         # west run, up to the wharf
         built("race-wall-n-a", [[-125,70],[-108,73],[-90,76],[WHARF_W, NB(WHARF_W)]],
               1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
         # between the wharf and the yard gate
         built("race-wall-n-b", [[WHARF_E, NB(WHARF_E)],[GATE_W, NB(GATE_W)]],
               1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
         # east run, from the yard gate to the race mouth
         built("race-wall-n-c", [[GATE_E, NB(GATE_E)],[-40,62],[-15,70]],
               1.0, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
         built("sluice", [[SLUICE_X, edge_z(SOUTH_BANK[1],SOUTH_BANK[2],SLUICE_X)-1],
                          [SLUICE_X, NB(SLUICE_X)+1]],
               1.5, WALL_FLOOR, WALL_TOP-WALL_FLOOR),
         ramp("yard-ramp", GATE_W, GATE_E, 71, 54, BANK_TOP, 19),
         ramp("wharf-steps", WHARF_W, WHARF_E, 75, 60, BANK_TOP, WATER_LEVEL-3)]
ground["shapes"].extend(edges)
ground["groups"][0]["shapeIds"] = ["s0","s1","s2"] + [e["id"] for e in edges]
TEAM, ISLE = ground["groups"][0]["id"], ground["groups"][1]["id"]

# A span is its own layer. On the ground layer an override add wins the column floor and all,
# so a deck written there takes the race bed out from under itself.
def span_layer(lid, shapes):
    return {"id":lid,"name":lid,"base_y":0,
            "layout":{"shapes":shapes,
                      "groups":[{"id":lid+"-body","name":lid,"mirrors":True,
                                 "shapeIds":[s["id"] for s in shapes]}]}}
viaduct = built("viaduct", [[BRIDGE_X, edge_z(SOUTH_BANK[0],SOUTH_BANK[1],BRIDGE_X)-5],
                            [BRIDGE_X, edge_z(NORTH_BANK[3],NORTH_BANK[2],BRIDGE_X)+5]],
                3.0, BANK_TOP, 1, seed=3)
piers = [{"id":f"pier-{i}","type":"rectangle","operation":"add","override":True,"keepClear":True,
          "min_x":BRIDGE_X-2,"max_x":BRIDGE_X+2,"min_z":z-2,"max_z":z+2,
          "floor":17,"base_height":BANK_TOP-17,"height_mode":"level","skirt":0,
          "relief_scope":"exclude","theme":"masonry"} for i,z in enumerate((46,57,68))]
causeway = built("causeway", [[-11,54],[6,53],[26,53]], 3.0, BASIN_TOP-1, 1, seed=4)

# ── the hills the four hint slabs only pointed at ────────────────────────────
layout["layers"] = [layout["layers"][0], span_layer("spans", [viaduct]+piers+[causeway])]
layout["relief"] = {
 TEAM: {"base":BANK_TOP,"reach":0,"step":1,"stairs":True,"landform":"moor",
        "grain":{"amplitude":1.2,"scale":17,"seed":5},
        "marks":[
          {"id":"race","kind":"line","r":15,
           "points":[[-15,52],[-52,50],[-70,54],[-100,57],[-128,52]],"h":[24,23,22,20,19]},
          {"id":"moor-bank","kind":"area","h":BANK_TOP,
           "ring":[[-113,95],[-108,73],[-90,76],[-40,62],[1,75],[13,96],[5,120],[-34,131],[-68,122],[-105,120]]},
          {"id":"wold-bank","kind":"area","h":BANK_TOP,
           "ring":[[-122,15],[-115,0],[-89,-20],[-65,-2],[-33,6],[-15,35],[-46,30],[-82,43],[-125,35]]},
          {"id":"pit","kind":"point","at":[-52,52],"h":19,"r":11},
          {"id":"moor-brow","kind":"point","at":[-40,118],"h":40,"r":26},
          {"id":"fell-head","kind":"point","at":[-110,12],"h":43,"r":24},
          {"id":"wold-brow","kind":"point","at":[-45,9],"h":38,"r":20}]},
 ISLE: {"base":BASIN_TOP,"reach":0,"step":1,"stairs":True,"landform":"knoll",
        "grain":{"amplitude":1.6,"scale":12,"seed":9},
        "marks":[{"id":"knoll","kind":"point","at":[47,50],"h":39,"r":20}]},
}
layout["themes"], layout["mapTheme"] = THEMES, "moor"
STYLE = json.load(open(f"{ROOT}/tools/styles/17h-croft.json"))
VARIANT = json.loads(json.dumps(STYLE))          # the second style is a repaint of the first
# The second style is the first repainted: a wall is a band stack, so what changes is the
# material inside each band and never the structure around it.
SWAP = {(4,0): (24,0), (98,0): (24,2), (98,1): (24,2), (17,0): (5,2)}
def repaint(node):
    if isinstance(node, dict):
        if node.get("kind") == "solid" and (node.get("id"), node.get("data", 0)) in SWAP:
            node["id"], node["data"] = SWAP[(node["id"], node.get("data", 0))]
            return node
        for v in node.values(): repaint(v)
    elif isinstance(node, list):
        for v in node: repaint(v)
    return node
repaint(VARIANT)
layout["roomStyles"] = {"spawn": json.load(open(f"{ROOT}/tools/styles/showcase-hall.json"))}

# ── the sky sign ─────────────────────────────────────────────────────────────
FONT = {
 "M":["10001","11011","10101","10001","10001","10001","10001"],
 "I":["11111","00100","00100","00100","00100","00100","11111"],
 "L":["10000","10000","10000","10000","10000","10000","11111"],
 "R":["11110","10001","10001","11110","10100","10010","10001"],
 "A":["01110","10001","10001","11111","10001","10001","10001"],
 "C":["01110","10001","10000","10000","10000","10001","01110"],
 "E":["11111","10000","10000","11110","10000","10000","11111"]}
PX, TOP_Y, WORD, SIGN_Z = 3, 84, "MILLRACE", -4
pitch = 5*PX + PX
letters, x0 = [], -(len(WORD)*pitch - PX)//2
for li, ch in enumerate(WORD):
    for row, bits in enumerate(FONT[ch]):
        run = 0
        for col in range(6):
            on = col < 5 and bits[col] == "1"
            if on: run += 1; continue
            if run:
                sx = x0 + li*pitch + (col-run)*PX
                letters.append({"id":f"sign-{li}-{row}-{col}","type":"rectangle","operation":"add",
                    "min_x":sx,"max_x":sx+run*PX,"min_z":SIGN_Z,"max_z":SIGN_Z+3,
                    "floor":TOP_Y-row*PX,"base_height":PX,"theme":"sign-face","keepClear":False})
            run = 0
backdrop = [{"id":"sign-back","type":"rectangle","operation":"add",
    "min_x":x0-4,"max_x":x0+len(WORD)*pitch-PX+4,"min_z":SIGN_Z+3,"max_z":SIGN_Z+5,
    "floor":TOP_Y-6*PX-4,"base_height":7*PX+8,"theme":"sign-back","keepClear":False}]
def prop_layer(lid, prop, shapes, mirrors=False):
    return {"id":lid,"name":lid,"base_y":0,"kind":"prop","prop":prop,
            "layout":{"shapes":shapes,
                      "groups":[{"id":lid+"-body","name":prop,"mirrors":mirrors,
                                 "shapeIds":[s["id"] for s in shapes]}]}}
layout["layers"] += [prop_layer("sign-L0","sign",backdrop), prop_layer("sign-L1","sign",letters)]

# ── a barge on the water, and a balloon over the moor ────────────────────────
def box(sid, x0_,z0_,x1,z1, floor, h, th):
    return {"id":sid,"type":"rectangle","operation":"add","min_x":x0_,"max_x":x1,
            "min_z":z0_,"max_z":z1,"floor":floor,"base_height":h,"theme":th,"keepClear":False}
BX, BZ = -108, 55
barge_hull = [box("barge-h0",BX-9,BZ-3,BX+9,BZ+3,WATER_LEVEL-2,2,"hull"),
              box("barge-h1",BX-11,BZ-2,BX-9,BZ+2,WATER_LEVEL-2,2,"hull"),
              box("barge-h2",BX+9,BZ-2,BX+11,BZ+2,WATER_LEVEL-2,2,"hull")]
barge_rail = [box("barge-r0",BX-9,BZ-3,BX+9,BZ-2,WATER_LEVEL,1,"gunwale"),
              box("barge-r1",BX-9,BZ+2,BX+9,BZ+3,WATER_LEVEL,1,"gunwale"),
              box("barge-r2",BX-2,BZ-1,BX+2,BZ+1,WATER_LEVEL,4,"sail")]
layout["layers"] += [prop_layer("barge-L0","barge",barge_hull),
                     prop_layer("barge-L1","barge",barge_rail)]
def disc(sid, cx, cz, r, floor, h, th):
    return {"id":sid,"type":"circle","operation":"add","center_x":cx,"center_z":cz,"radius":r,
            "floor":floor,"base_height":h,"theme":th,"keepClear":False}
# One run per layer. Stacked discs written to one layer lose all but the tallest, because a
# layer keeps one span per column and a plain add wins it floor and all.
BAL_X, BAL_Z = -58, 100
bal_runs = [[disc("bal-0",BAL_X,BAL_Z,5,56,3,"envelope")],
            [disc("bal-1",BAL_X,BAL_Z,8,59,4,"envelope")],
            [disc("bal-2",BAL_X,BAL_Z,10,63,5,"envelope")],
            [disc("bal-3",BAL_X,BAL_Z,8,68,4,"envelope")],
            [disc("bal-4",BAL_X,BAL_Z,4,72,2,"envelope")],
            [disc("bal-b",BAL_X,BAL_Z,2,51,3,"basket")]]
for i, run in enumerate(bal_runs):
    layout["layers"].append(prop_layer(f"balloon-L{i}","balloon",run))
cloud = [disc("cl-0",30,-60,11,88,4,"cloud"), disc("cl-1",22,-52,7,88,3,"cloud"),
         disc("cl-2",40,-66,8,88,3,"cloud")]
layout["layers"] += [prop_layer("cloud-L0","cloud",cloud, mirrors=True)]

# ── water, and the few things placed because there is an answer to why here ──
race_ring = [[-72,41],[-84,45],[-122,38],[-129,49],[-122,68],[-107,70],[-90,73],[-73,68]]
props = [
 {"id":"race-water","kind":"water","seed":7,"layer":"ground","shape":"pool","points":race_ring,
  "radius":12,"depth":5,"shore":2,"shoreWander":True,"edge":1.0,"level":WATER_LEVEL,
  "bank":{"kind":"solid","id":13,"data":0}},
 {"id":"towpath","kind":"path","seed":3,"route":True,"radius":2,"coverage":0.9,
  "points":[[-90,100],[-95,84],[-100,74],[-100,40],[-92,26]],"pave":{"kind":"solid","id":98,"data":0}},
 {"id":"yard-lane","kind":"path","seed":5,"route":True,"radius":2,"coverage":0.85,
  "points":[[-100,74],[-78,72],[-58,66],[-52,58]],"pave":{"kind":"solid","id":98,"data":2}},
 # The mill stands on the bank over the wharf. `OB19` keeps a 10-block square about the goal
 # plus eaves, so x -64..-40 z 40..64 is out for every building, tree and boulder.
 # Coverage walks the authored routes, so ground a lane never crosses is ground nobody has a
 # reason to be on however well it is painted. These two are the crossing and the far bank.
 {"id":"holm-way","kind":"path","seed":7,"route":True,"radius":2,"coverage":0.9,
  "points":[[-30,62],[-14,56],[6,53],[28,52],[44,50]],"pave":{"kind":"solid","id":4,"data":0}},
 {"id":"wold-lane","kind":"path","seed":9,"route":True,"radius":2,"coverage":0.85,
  "points":[[-92,26],[-72,24],[-48,16],[-28,22]],"pave":{"kind":"solid","id":24,"data":2}},
 {"id":"mill","kind":"house","seed":41,"front":"posZ","points":[[-76,78],[-64,90]],"style":STYLE},
 {"id":"croft-a","kind":"house","seed":42,"front":"posZ","points":[[-45,95],[-33,107]],"style":STYLE},
 {"id":"croft-b","kind":"house","seed":43,"front":"posZ","points":[[-50,80],[-40,90]],"style":STYLE},
 {"id":"steading","kind":"house","seed":44,"front":"negZ","points":[[-84,20],[-72,32]],"style":VARIANT},
 {"id":"holm-hut","kind":"house","seed":45,"front":"posX","points":[[36,40],[46,48]],"style":VARIANT},
]
for i,(x,z,h) in enumerate([(-30,110,8),(-22,102,7),(-46,120,9),(-58,118,8),(-70,114,7),
                            (-14,90,8),(-96,118,9),(-108,104,7),(-84,120,8),
                            (-36,18,7),(-40,22,8),(-52,2,7),(-84,6,8),(-110,36,7),
                            (-112,32,8),(-64,4,7),(38,62,7),(52,40,8)]):
    props.append({"id":f"tree-{i}","kind":"tree","seed":200+i,"x":x,"z":z,
                  "form":"template","species":"oak" if i%3 else "spruce","height":h})
for i,(x,z,s) in enumerate([(-56,112,2.6),(-18,76,2.2),(-66,118,2.4),(-30,26,2.3)]):
    props.append({"id":f"erratic-{i}","kind":"boulder","seed":500+i,"x":x,"z":z,
                  "form":"round","size":s,"mossy":True})
layout["dressing"] = {"props": props}

GOAL = {"x": -52, "z": 52}
intent["destroyables"] = [
 {"layer":None,"stamp":{"kind":"destroyable","unit":"destroyable-1","image":i},
  "owner":o,"name":n,"style":"pillar-3","materials":"obsidian",
  "anchor":{"x":GOAL["x"]*sg,"y":19,"z":GOAL["z"]*sg},"float":4,"box":None}
 for i,(o,n,sg) in enumerate([("red","Red Monument",1),("blue","Blue Monument",-1)])]
intent["meta"]["name"], intent["meta"]["created"] = NAME, "2026-08-30"
intent["meta"]["authors"] = ["Opus 5"]

json.dump(layout, open(SPEC + ".layout.json","w"), indent=1)
json.dump(intent, open(SPEC + ".intent.json","w"), indent=1)
st,w,b = post("/map/from-documents", {"slug":SLUG,"name":NAME,"plan":plan,"layout":layout,
                                      "intent":intent,"authors":["Opus 5"]})
print(f"from-documents {st}  Pgm-Warnings: {w}   cells={b.get('cells')} islands={b.get('islands')}")
for f in (b.get("warnings") or b.get("findings") or []):
    if isinstance(f,dict): print(f"  {f.get('rule','')} {f.get('severity','')}: {f.get('message','')[:200]}")
if "error" in b: print("  ERROR", b["error"], str(b.get("message"))[:500])
