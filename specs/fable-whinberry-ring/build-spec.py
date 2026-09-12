"""Whinberry Ring — a heath board grown from composer seed 18 at sixteen players (`composed-seed-18.plan.json`
beside this file is the board as the composer emitted it). The composer's arrangement is kept: a ring hub with
a hole in it, a spawn behind, two flank wools. What is added is what the composer does not do: three
levels of ground, a twin frontline with a bay between its prongs, a stepping stone on the axis, a defence
wall on each wool approach, and an outline reshaped so the pieces read as heath rather than as tiles."""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fable-whinberry-ring"

plan = json.load(open(f"{HERE}/composed-seed-18.plan.json"))
plan["plan"] = 2
plan["meta"]["name"] = "Whinberry Ring"
plan["globals"]["observerY"] = 50
BACK, MID, FRONT = 15, 12, 9
HEIGHTS = {"spawn-room": BACK, "spawn-t1": BACK, "hub-t1": BACK,
           "hub-t2": MID, "hub-t3": BACK, "hub-t4": BACK,
           "wool-a-t1": MID, "wool-a-room": MID, "wool-b-t1": MID, "wool-b-room": MID}
pieces = [q for q in plan["pieces"] if q["id"] != "frontline-t1"]
for q in pieces:
    q["surface"] = HEIGHTS[q["id"]]
# the frontline as two prongs and a bar, with a bay of void between the prongs
pieces += [
  {"id": "front-w",   "role": "piece", "rect": [-3, 3, 2, 3], "surface": FRONT},
  {"id": "front-e",   "role": "piece", "rect": [1, 3, 2, 3],  "surface": FRONT},
  # the stepping stone on the axis: its own rot_180 image, so it is stated once
  {"id": "stone",     "role": "piece", "rect": [-1, -1, 2, 2], "surface": FRONT, "mirrors": False},
]
for q in pieces:
    if q["id"] == "wool-a-t1":   q["rect"] = [-6, 9, 3, 2]
    if q["id"] == "wool-a-room": q["rect"] = [-8, 9, 2, 2]
plan["zones"] = [{"id": "mid-band", "rect": [-3, -3, 6, 6], "holes": []}]
plan["pieces"] = pieces
plan["boxes"] = []
plan["walls"] = [{"a": "wool-a-t1", "b": "hub-t1"},
                 {"a": "wool-b-t1", "b": "hub-t2"}]
# the marker offsets: version 2 states them in blocks from the piece corner
plan["placements"]["spawns"] = [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 5], "facing": "front",
                                 "footprint": [1, 1, 8, 8]}]
plan["placements"]["wools"] = [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5], "footprint": [1, 1, 8, 8]},
                               {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5], "footprint": [1, 1, 8, 8]}]
json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
print("wrote plan")

# ── the finish ────────────────────────────────────────────────────────────────────────────────
import urllib.request
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
def post(route, body):
    req = urllib.request.Request(API + route, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(req))
compiled = post("/plan/compile", plan)["layout"]
shapes = {s["id"]: s for lay in compiled["layers"] for s in lay["layout"]["shapes"]}
print("compiled shapes:", {k: len(v.get("vertices") or []) for k, v in shapes.items()})

def inserts(shape_id, wanted):
    """Each wanted entry is (A, B, P): put P on the edge A->B of the compiled ring. The ops are
    replayed in order by the driver, so the indices are read off the ring as it stands at each step."""
    ring = [list(v) for v in shapes[shape_id]["vertices"]]
    ops = []
    for a, b, p in wanted:
        n = len(ring)
        i = next((i for i in range(n) if ring[i] == list(a) and ring[(i + 1) % n] == list(b)), None)
        if i is None:
            print(f"    ! {shape_id}: no edge {a}->{b} on the ring {ring}"); continue
        ops.append({"after": i, "x": p[0], "z": p[1]})
        ring.insert(i + 1, list(p))
    return ops

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, DIRT, COARSE, GRAVEL = solid(2), solid(3), solid(3, 1), solid(13)
STONE, ANDESITE, COBBLE = solid(1), solid(1, 5), solid(4)
SBRICK, PLANK_S, LOG_S, PLANK_D = solid(98), solid(5, 1), solid(17, 1), solid(5, 5)
def cell(pal, size, seed, rise=0, jitter=40):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 2, "palette": pal, "rise": rise}
def depth(*bands):
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
def slope(*bands):
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
ROCK = cell([STONE, ANDESITE], 9, 31, rise=3)
CLIFF = depth((COARSE, 1), (DIRT, 1), (ROCK, 40))
def theme(surface, surface_depth, wall, fill):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
            "rim": {"enabled": False, "depth": 1, "material": STONE},
            "surface": {"enabled": True, "depth": surface_depth, "material": surface},
            "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": fill}
HEATH_TOP = cell([GRASS, GRASS, GRASS, GRASS, COARSE], 12, 12)          # grass with a worn patch here and there
THEMES = {
  "heath": theme(slope((depth((HEATH_TOP, 1), (DIRT, 2)), 32),
                       (depth((COARSE, 1), (DIRT, 2)), 13),
                       (ROCK, 45)), 3, CLIFF, ROCK),
}
TRACK = cell([DIRT, COARSE, PLANK_S], 3, 21)

def storey(clear, wall_bands, post, windows):
    return {"clear": clear, "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}},
            "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": None, "headroom": clear + 1}
WIN_LATTICE = {"form": "stairLattice", "block": 134, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
STONEWALL = {"kind": "noise", "seed": 41, "scale": 3, "octaves": 1, "stops": [COBBLE, ANDESITE], "rise": 2}
LAID = {"kind": "laidLog", "id": 17, "data": 1}
def shell(storeys, beams):
    return {
      "foundation": {"plate": {"stack": {"bands": [{"material": SBRICK, "thickness": 1}], "ending": "repeat"}, "extent": 1},
                     "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
                     "footing": None},
      "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": False, "hole": False,
               "body": PLANK_D, "verge": LAID, "gable": PLANK_S, "gableWindows": WIN_NONE},
      "wall": {"stack": {"bands": [{"material": STONEWALL, "thickness": 4}], "ending": "repeat"}, "extent": 4},
      "post": LOG_S, "windows": WIN_LATTICE, "storeys": storeys, "porch": None, "front": None,
      "beams": {"block": 17, "data": 1, "reach": 1, "any": True} if beams else {"block": -1, "data": 0, "reach": 1, "any": False},
      "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab", "fillBlock": 126, "fillData": 0}, "width": 2, "height": 3}}
GROUND = storey(3, [{"material": STONEWALL, "thickness": 3}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)
LOFT = storey(3, [{"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)
HALL = shell([GROUND, LOFT], beams=True)
CAGE = shell([GROUND], beams=False)
CAGE["doorway"]["door"] = "stainedGlassPane"

ERRATIC = {"kind": "noise", "seed": 51, "scale": 3, "octaves": 1, "stops": [STONE, COBBLE, ANDESITE], "rise": 2}
TREES = json.load(open(f"{os.path.dirname(HERE)}/fable-millrace-revamp/trees.json"))
def body(name): return {"kind": "tree", "form": "copied", "body": TREES[name]["body"]}
def oak(pid, x, z, style, seed):
    return {"id": pid, "kind": "tree", "seed": seed, "layer": "ground", "x": x, "z": z, "style": style}
def boulder(pid, x, z, form, size, seed):
    return {"id": pid, "kind": "boulder", "seed": seed, "layer": "ground", "x": x, "z": z, "form": form, "size": size, "mossy": False, "rock": ERRATIC}
def track(pid, pts, seed):
    return {"id": pid, "kind": "stroke", "seed": seed, "style": "solid", "claimsGround": True, "radius": 1.5, "points": pts, "pave": TRACK}

DRESSING = {
  "styles": {"oak-a": body("oak-dense-1"), "oak-b": body("oak-dense-4"), "oak-c": body("oak-dense-3")},
  "props": [
    track("road", [[5, 58], [5, 48], [8, 42], [8, 33], [7, 28], [7, 12]], 5),
    track("cross", [[-13, 36], [0, 36], [14, 36]], 6),
    oak("oak-1", 13, 50, "oak-a", 1), oak("oak-2", -9, 52, "oak-b", 2), oak("oak-3", -12, 33, "oak-c", 3),
    boulder("stone-1", -10, 20, "round", 3, 21), boulder("stone-2", 12, 24, "angular", 3, 22),
    {"id": "bracken", "kind": "flora", "seed": 9, "points": [[-45, 0], [45, 0], [45, 75], [-45, 75]],
     "spec": {"coverage": 0.4, "scale": 11, "octaves": 3, "fernShare": 0.4, "flowerShare": 0.05, "flowerScale": 16, "tallShare": 0.04}},
  ]}

RELIEF = {"team": {
  "base": MID, "reach": 0, "step": 1, "landform": "plain",
  "grain": {"amplitude": 0.7, "scale": 10, "seed": 5},
  "marks": [
    {"id": "terrace", "kind": "area", "h": BACK, "bevel": 4,
     "ring": [[-17, 45], [17, 45], [17, 57], [12, 62], [12, 72], [-2, 72], [-2, 62], [-17, 57]]},
    {"id": "west-lea", "kind": "area", "h": MID, "bevel": 3,
     "ring": [[-46, 43], [-18, 43], [-18, 57], [-30, 61], [-46, 57]]},
    {"id": "front", "kind": "area", "h": FRONT, "bevel": 3,
     "ring": [[-17, 12], [17, 12], [17, 26], [-17, 26]]},
  ],
  "pushes": []}}

finish = {
  "authors": ["Fable 5.1"], "created": "2026-09-11",
  "themes": THEMES, "mapTheme": "heath",
  "roomStyles": {"spawn": HALL, "wool": CAGE},
  "editShapes": {
    "front-e-9": inserts("front-e-9", [((-15, 30), (-15, 15), (-18, 22)), ((-15, 15), (-5, 15), (-10, 12))]),
    "front-e-9-2": inserts("front-e-9-2", [((15, 15), (15, 30), (18, 22)), ((5, 15), (15, 15), (10, 12))]),
    "front-e-12": inserts("front-e-12", [
        ((-15, 30), (35, 30), (17, 30)), ((17, 30), (35, 30), (27, 27)),
        ((35, 30), (35, 40), (39, 35)),
        ((35, 40), (-15, 40), (17, 40)), ((35, 40), (17, 40), (26, 44)),
        ((-15, 40), (-15, 30), (-18, 35))]),
    "front-e-12-2": inserts("front-e-12-2", [
        ((-40, 45), (-15, 45), (-28, 41)), ((-40, 55), (-40, 45), (-44, 50)), ((-15, 55), (-40, 55), (-28, 59))]),
    "front-e-15": inserts("front-e-15", [
        ((0, 70), (0, 55), (-4, 63)), ((10, 55), (10, 70), (14, 63)), ((15, 40), (15, 55), (19, 49))]),
    "stone-9": inserts("stone-9", [((-5, 5), (-5, -5), (-8, 0)), ((5, -5), (5, 5), (8, 0)),
                                   ((-5, -5), (5, -5), (0, -8)), ((5, 5), (-5, 5), (0, 8))]),
  },
  "relief": RELIEF,
  "dressing": DRESSING,
}
json.dump(finish, open(f"{HERE}/{SLUG}.finish.json", "w"), indent=1)
print("wrote finish")
