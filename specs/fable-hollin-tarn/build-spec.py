"""Hollin Tarn — a snowed valley head. The monument stands on a low green knoll behind a frozen tarn; the
tarn is the open ground in front of it, and whoever crosses the ice does so in plain view. Either side of
the valley a spruce-clad shoulder gives the long way round, and the height. The lodge at the valley head is
the spawn."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fable-hollin-tarn"

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, DIRT, COARSE, GRAVEL = solid(2), solid(3), solid(3, 1), solid(13)
STONE, ANDESITE, COBBLE = solid(1), solid(1, 5), solid(4)
SNOW, ICE = solid(80), solid(174)
SBRICK, PLANK_S, LOG_S, PLANK_D = solid(98), solid(5, 1), solid(17, 1), solid(5, 5)
def cell(pal, size, seed, rise=0, jitter=40):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 2, "palette": pal, "rise": rise}
def depth(*bands):
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [{"material": a, "thickness": t} for a, t in bands]}}
def slope(*bands):
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [{"material": a, "thickness": t} for a, t in bands]}}
ROCK = cell([STONE, ANDESITE], 9, 31, rise=3)
CLIFF = depth((DIRT, 1), (ROCK, 40))
def theme(surface, surface_depth, wall, fill):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
            "rim": {"enabled": False, "depth": 1, "material": STONE},
            "surface": {"enabled": True, "depth": surface_depth, "material": surface},
            "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": fill}
SNOWFIELD = cell([SNOW, SNOW, SNOW, GRASS], 9, 12)          # snow lying on the grass, worn through here and there
THEMES = {
  "snow": theme(slope((depth((SNOWFIELD, 1), (DIRT, 2)), 30),
                      (depth((cell([GRASS, COARSE], 7, 13), 1), (DIRT, 2)), 15),
                      (ROCK, 45)), 3, CLIFF, ROCK),
  "tarn": theme(depth((ICE, 1), (GRAVEL, 2)), 3, depth((GRAVEL, 1), (ROCK, 40)), ROCK),
}

plan = {
  "plan": 2, "meta": {"name": "Hollin Tarn"},
  "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 12, "surface": 12, "observerY": 56},
  "pieces": [
    {"id": "dale",   "role": "piece", "rect": [-10, -16, 20, 14], "surface": 12},
    {"id": "head-w", "role": "piece", "rect": [-10, -19, 8, 3],   "surface": 18},
    {"id": "spawn",  "role": "spawn", "rect": [-2, -19, 4, 3],    "surface": 18},
    {"id": "head-e", "role": "piece", "rect": [2, -19, 8, 3],     "surface": 18},
  ],
  "zones": [{"id": "gap", "rect": [-10, -2, 20, 4], "holes": []}],
  "placements": {
    "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 8], "facing": "back", "footprint": [4, 3, 12, 10]}],
    "wools": [], "iron": [],
    "destroyables": [{"id": "destroyable-1", "piece": "dale", "at": [40, 31], "style": "pillar-3",
                      "materials": "obsidian", "float": 4, "name": "Hollin Monument"}],
    "cores": []},
  "walls": [], "boxes": []}

import math
def ring(cx, cz, rx, rz, n=10, seed=0, wob=0.12):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        w = 1 + wob * math.sin(3 * a + seed)
        out.append([round(cx + rx * w * math.cos(a)), round(cz + rz * w * math.sin(a))])
    return out
TARN = ring(0, -26, 17, 9, n=12, seed=2)
KNOLL = ring(-10, -49, 16, 8, n=10, seed=1)
SHORE = ring(0, -26, 21, 12, n=12, seed=2)      # the plate's own ring grown by a fifth: the flat the ice is set into
RELIEF = {"team": {
  "base": 12, "reach": 0, "step": 1, "landform": "plain",
  "grain": {"amplitude": 0.6, "scale": 12, "seed": 7},
  "marks": [
    {"id": "shore", "kind": "area", "h": 12, "bevel": 3, "ring": SHORE},
    {"id": "knoll", "kind": "area", "h": 14, "bevel": 4, "ring": KNOLL},
    {"id": "head", "kind": "area", "h": 18, "bevel": 5,
     "ring": [[-50, -73], [-30, -75], [-10, -72], [10, -72], [30, -75], [50, -73], [50, -95], [-50, -95]]},
  ],
  "pushes": [
    {"id": "shoulder-w", "ring": [[-50, -24], [-34, -28], [-26, -40], [-28, -60], [-38, -71], [-50, -69]],
     "amount": 5, "falloff": 20, "roughness": 0.35, "crown": 5, "seed": 4},
    {"id": "shoulder-e", "ring": [[50, -24], [34, -28], [26, -40], [28, -60], [38, -71], [50, -69]],
     "amount": 5, "falloff": 20, "roughness": 0.35, "crown": 5, "seed": 5},
  ]}}
# the ice is paint on the pan the relief cut: a one-course add, so it can never lower what it lies on
# the tarn is the sheet itself: a flat plate cut through the field at its own level, so the pan is its
# footprint, its one-block face is the shore, and the ice is its own paint
BROOK = {"id": "brook", "type": "polyline", "operation": "add", "floor": 0, "base_height": 11,
         "height_mode": "level", "skirt": 0, "theme": "tarn", "radius": 1.5, "stroke_edge": "rough", "stroke_seed": 3,
         "vertices": [[-16, -25], [-25, -21], [-34, -17], [-42, -13], [-50, -11]]}
CRAG = {"id": "crag", "type": "polygon", "operation": "add", "theme": "snow",
        "floor": 0, "base_height": 20, "height_mode": "level", "skirt": 6,
        "vertices": [[24, -12], [36, -11], [42, -17], [40, -25], [30, -27], [22, -21]]}
ICE_SHEET = {"id": "ice-sheet", "type": "polygon", "operation": "add", "floor": 0, "base_height": 11,
             "height_mode": "level", "skirt": 0, "theme": "tarn", "vertices": TARN}

def storey(clear, wall_bands, post, windows):
    return {"clear": clear, "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}},
            "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": None, "headroom": clear + 1}
WIN_PANE = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 1, "spacing": 3}
WIN_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
LAID = {"kind": "laidLog", "id": 17, "data": 1}
STONEFOOT = {"kind": "noise", "seed": 41, "scale": 3, "octaves": 1, "stops": [COBBLE, ANDESITE], "rise": 2}
def lodge(storeys, beams):
    return {
      "foundation": {"plate": {"stack": {"bands": [{"material": PLANK_S, "thickness": 1}], "ending": "repeat"}, "extent": 1},
                     "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
                     "footing": None},
      "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": False, "hole": False,
               "body": PLANK_D, "verge": LAID, "gable": PLANK_S, "gableWindows": WIN_NONE},
      "wall": {"stack": {"bands": [{"material": PLANK_S, "thickness": 4}], "ending": "repeat"}, "extent": 4},
      "post": LOG_S, "windows": WIN_PANE, "storeys": storeys, "porch": None, "front": None,
      "beams": {"block": 17, "data": 1, "reach": 1, "any": True} if beams else {"block": -1, "data": 0, "reach": 1, "any": False},
      "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab", "fillBlock": 126, "fillData": 0}, "width": 2, "height": 3}}
# a stone footing course, plank walls, and a laid-log course the floor beams come out of
GROUND = storey(3, [{"material": STONEFOOT, "thickness": 1}, {"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)
LOFT = storey(3, [{"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)
LODGE = lodge([GROUND, LOFT], beams=True)
HUT = lodge([storey(3, [{"material": STONEFOOT, "thickness": 1}, {"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)], beams=False)

TREES = json.load(open(f"{os.path.dirname(HERE)}/fable-millrace-revamp/trees.json"))
def body(name): return {"kind": "tree", "form": "copied", "body": TREES[name]["body"]}
def tree(pid, x, z, style, seed):
    return {"id": pid, "kind": "tree", "seed": seed, "layer": "ground", "x": x, "z": z, "style": style}
ERRATIC = {"kind": "noise", "seed": 51, "scale": 3, "octaves": 1, "stops": [STONE, COBBLE, ANDESITE], "rise": 2}
def boulder(pid, x, z, form, size, seed):
    return {"id": pid, "kind": "boulder", "seed": seed, "layer": "ground", "x": x, "z": z, "form": form, "size": size, "mossy": False, "rock": ERRATIC}
def house(pid, x0, z0, x1, z1, style, front, seed):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground", "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
TRACK = cell([GRAVEL, ANDESITE, COBBLE], 3, 21)
FIRS = [("fir-1", -40, -65, "fir-t1"), ("fir-2", -30, -50, "fir-t2"), ("fir-3", -42, -44, "fir-t3"),
        ("fir-4", -34, -33, "fir-t1"), ("fir-5", -46, -26, "fir-s1"), ("fir-6", -26, -67, "fir-s2"),
        ("fir-7", 40, -65, "fir-t2"), ("fir-8", 30, -50, "fir-t3"), ("fir-9", 42, -44, "fir-t1"),
        ("fir-10", 34, -33, "fir-s1"), ("fir-11", 46, -26, "fir-s2"), ("fir-12", 26, -67, "fir-t2"),
        ("fir-13", -36, -87, "fir-s1"), ("fir-14", 36, -87, "fir-s2")]
DRESSING = {
  "styles": {"fir-t1": body("fir-tall-5"), "fir-t2": body("fir-tall-6"), "fir-t3": body("fir-tall-7"),
             "fir-s1": body("fir-small-1"), "fir-s2": body("fir-small-4")},
  "props": [
    {"id": "track", "kind": "stroke", "seed": 5, "style": "solid", "claimsGround": True, "radius": 1.5,
     "points": [[0, -78], [-4, -69], [-14, -56], [-24, -46], [-27, -34], [-23, -24], [-19, -16], [-17, -11]], "pave": TRACK},
    {"id": "track-hut", "kind": "stroke", "seed": 6, "style": "solid", "claimsGround": True, "radius": 1.5,
     "points": [[-18, -15], [-15, -15], [-13, -15]], "pave": TRACK},
    house("hut", -12, -17, -6, -12, HUT, "negX", 11),
  ] + [tree(pid, x, z, st, n + 1) for n, (pid, x, z, st) in enumerate(FIRS)] + [
    boulder("stone-1", -26, -34, "round", 3, 21), boulder("stone-2", 22, -65, "angular", 4, 22),
    boulder("stone-3", 12, -20, "round", 3, 23),
    {"id": "sward", "kind": "flora", "seed": 9, "points": [[-50, -95], [50, -95], [50, -10], [-50, -10]],
     "spec": {"coverage": 0.15, "scale": 12, "octaves": 3, "fernShare": 0.2, "flowerShare": 0.0, "flowerScale": 16, "tallShare": 0.0}},
  ]}

import urllib.request
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
def post(route, body):
    req = urllib.request.Request(API + route, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(req))
compiled = post("/plan/compile", plan)["layout"]
shapes = {s["id"]: s for lay in compiled["layers"] for s in lay["layout"]["shapes"] if s.get("vertices")}
head_id = next(sid for sid, s in shapes.items() if s.get("base_height") == 18)
def edits(shape_id, wanted):
    ring = [list(v) for v in shapes[shape_id]["vertices"]]
    ops = []
    for entry in wanted:
        n = len(ring)
        if entry[0] == "remove":
            i = ring.index(list(entry[1])); ops.append({"remove": i}); ring.pop(i); continue
        a, b, p = entry
        i = next((i for i in range(n) if ring[i] == list(a) and ring[(i + 1) % n] == list(b)), None)
        if i is None:
            print(f"    ! {shape_id}: no edge {a}->{b} on {ring}"); continue
        ops.append({"after": i, "x": p[0], "z": p[1]}); ring.insert(i + 1, list(p))
    return ops
print("head ring", shapes[head_id]["vertices"])

finish = {
  "authors": ["Fable 5.1"], "created": "2026-09-12",
  "editShapes": {head_id: edits(head_id, [((-50, -95), (50, -95), (-30, -95)), ((-50, -80), (-50, -95), (-50, -85)),
                                          ("remove", (-50, -95)),
                                          ((-30, -95), (50, -95), (30, -95)), ((50, -95), (50, -80), (50, -85)),
                                          ("remove", (50, -95))])},
  "themes": THEMES, "mapTheme": "snow",
  "biome": {"kind": "solid", "id": 30},
  "roomStyles": {"spawn": LODGE},
  "addShapes": [ICE_SHEET, BROOK, CRAG],
  "relief": RELIEF,
  "dressing": DRESSING,
}
json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
json.dump(finish, open(f"{HERE}/{SLUG}.finish.json", "w"), indent=1)
print("wrote", SLUG)
