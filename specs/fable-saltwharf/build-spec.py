"""Saltwharf — a stone quay under a grass headland. The core stands out on the quay, in the open, with a
warehouse either side of it; the spawn is on the headland behind, ten blocks up. Two stone flights and a
sandy bank are the three ways down from the headland to the quay, and the quay's front is the sea wall the
bridges land on."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fable-saltwharf"

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, DIRT, COARSE, GRAVEL, SAND, SANDSTONE = solid(2), solid(3), solid(3, 1), solid(13), solid(12), solid(24)
STONE, ANDESITE, COBBLE = solid(1), solid(1, 5), solid(4)
SBRICK, SBRICK_CH, PLANK_S, LOG_S, PLANK_D = solid(98), solid(98, 3), solid(5, 1), solid(17, 1), solid(5, 5)
CLAY_GREY = solid(159, 8)
def cell(pal, size, seed, rise=0, jitter=40):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 2, "palette": pal, "rise": rise}
def depth(*bands, ending="repeat", beyond=None):
    m = {"kind": "layered", "axis": "depth", "stack": {"ending": ending, "bands": [{"material": a, "thickness": t} for a, t in bands]}}
    if beyond: m["beyond"] = beyond
    return m
def inward(*bands, beyond):
    return {"kind": "layered", "axis": "inward", "beyond": beyond,
            "stack": {"ending": "handOver", "bands": [{"material": a, "thickness": t} for a, t in bands]}}
def slope(*bands):
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [{"material": a, "thickness": t} for a, t in bands]}}
TEAM_CLAY = {"kind": "teamTint", "blockId": 159, "neutral": CLAY_GREY}
ROCK = cell([STONE, ANDESITE], 9, 31, rise=3)
CLIFF = depth((COARSE, 1), (DIRT, 1), (ROCK, 40))
def theme(surface, surface_depth, wall, fill, rim=None):
    t = {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
         "rim": {"enabled": rim is not None, "depth": 1, "material": rim or STONE},
         "surface": {"enabled": True, "depth": surface_depth, "material": surface},
         "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": fill}
    return t
QUAY_FLOOR = inward((SBRICK, 1), (TEAM_CLAY, 1), beyond={"kind": "checker", "size": 3, "even": SBRICK, "odd": SBRICK_CH})
QUAY_WALL = {"kind": "wallRun", "runs": [{"material": SBRICK, "width": 7}, {"material": TEAM_CLAY, "width": 2}]}
THEMES = {
  "headland": theme(slope((depth((GRASS, 1), (DIRT, 2)), 32), (depth((COARSE, 1), (DIRT, 2)), 13), (ROCK, 45)), 3, CLIFF, ROCK),
  # the strand: sand on the flat, sand and gravel where it climbs
  "strand": theme(slope((depth((SAND, 2), (SANDSTONE, 2)), 30), (depth((cell([SAND, GRAVEL], 6, 17), 1), (SANDSTONE, 2)), 60)), 4,
                  depth((SAND, 1), (SANDSTONE, 2), (ROCK, 40)), ROCK),
  # the quay: a made thing, the same stone the whole way down, banded in the team's colour
  "quay": theme(QUAY_FLOOR, 1, QUAY_WALL, cell([SBRICK, COBBLE], 8, 33, rise=3)),
  "stair": theme(SBRICK, 1, SBRICK, SBRICK),
}

plan = {
  "plan": 2, "meta": {"name": "Saltwharf"},
  "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 12, "surface": 12, "observerY": 56},
  "pieces": [
    {"id": "quay",   "role": "piece", "rect": [-10, -8, 14, 6], "surface": 12},
    {"id": "strand", "role": "piece", "rect": [4, -8, 6, 6],    "surface": 13},
    {"id": "head-w", "role": "piece", "rect": [-10, -15, 4, 7], "surface": 22},
    {"id": "head-m", "role": "piece", "rect": [-6, -12, 4, 4],  "surface": 22},
    {"id": "spawn",  "role": "spawn", "rect": [-6, -15, 4, 3],  "surface": 22},
    {"id": "head-e", "role": "piece", "rect": [-2, -15, 12, 7], "surface": 22},
  ],
  "zones": [{"id": "sound", "rect": [-10, -2, 20, 4], "holes": []}],
  "placements": {
    "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 8], "facing": "back", "footprint": [5, 3, 10, 9]}],
    "wools": [], "iron": [], "destroyables": [],
    "cores": [{"id": "core-1", "piece": "quay", "at": [28, 18], "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5, "openTop": False}]},
  "walls": [], "boxes": []}

# ── the two flights, cut into the headland's front as slots, one course a block ──────────────────
def flight(sid, x0, x1):
    # twenty cells of run for ten courses: foot on the quay at z -40, head on the headland at z -60
    return {"id": sid, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "floor": 0, "base_height": 22, "theme": "stair", "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude",
            "vertices": [[x0, -40], [x1, -40], [x1, -60], [x0, -60]], "anchor_heights": [12, 12, 22, 22]}
FLIGHTS = [flight("flight-w", -34, -30), flight("flight-e", 14, 18)]

RELIEF = {"team": {
  "base": 22, "reach": 0, "step": 1, "landform": "rolling",
  "grain": {"amplitude": 0.7, "scale": 11, "seed": 3},
  "marks": [
    {"id": "strand-floor", "kind": "area", "h": 12, "bevel": 3, "ring": [[20, -10], [50, -10], [50, -24], [36, -27], [20, -24]]},
    {"id": "brow", "kind": "area", "h": 22, "bevel": 4,
     "ring": [[-50, -42], [-20, -42], [-10, -44], [10, -44], [22, -46], [50, -46], [50, -75], [-50, -75]]},
  ],
  "pushes": [
    {"id": "knoll-e", "ring": [[28, -52], [40, -50], [48, -56], [46, -66], [36, -70], [28, -64]],
     "amount": 4, "falloff": 8, "roughness": 0.3, "crown": 3, "seed": 4},
  ]}}

def storey(clear, wall_bands, post, windows):
    return {"clear": clear, "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}},
            "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": None, "headroom": clear + 1}
WIN_LATTICE = {"form": "stairLattice", "block": 134, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_PANE = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 1, "spacing": 3}
STONEWALL = {"kind": "noise", "seed": 41, "scale": 3, "octaves": 1, "stops": [SBRICK, ANDESITE], "rise": 2}
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
LOFT = storey(3, [{"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)
STORE = shell([storey(4, [{"material": STONEWALL, "thickness": 4}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)], beams=False)
HALL = shell([GROUND, LOFT], beams=True)
WAREHOUSE = shell([GROUND, LOFT], beams=True)

TREES = json.load(open(f"{os.path.dirname(HERE)}/fable-millrace-revamp/trees.json"))
def body(name): return {"kind": "tree", "form": "copied", "body": TREES[name]["body"]}
def tree(pid, x, z, style, seed):
    return {"id": pid, "kind": "tree", "seed": seed, "layer": "ground", "x": x, "z": z, "style": style}
ERRATIC = {"kind": "noise", "seed": 51, "scale": 3, "octaves": 1, "stops": [STONE, COBBLE, ANDESITE], "rise": 2}
def boulder(pid, x, z, form, size, seed):
    return {"id": pid, "kind": "boulder", "seed": seed, "layer": "ground", "x": x, "z": z, "form": form, "size": size, "mossy": False, "rock": ERRATIC}
def house(pid, x0, z0, x1, z1, style, front, seed):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground", "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
ROAD = cell([GRAVEL, ANDESITE, COBBLE], 3, 21)
SHORE_MIX = cell([SAND, SAND, GRASS], 4, 23)
DRESSING = {
  "styles": {"oak-a": body("oak-dense-2"), "oak-b": body("oak-dense-4")},
  "props": [
    # the road from the spawn door to the head of the east flight
    {"id": "road", "kind": "stroke", "seed": 5, "style": "solid", "claimsGround": True, "radius": 1.5,
     "points": [[-20, -62], [-24, -56], [-32, -56], [-32, -61]], "pave": ROAD},
    # the strand's edge against the grass, chopped up so the sand does not stop on a line
    {"id": "tide-line", "kind": "stroke", "seed": 6, "style": "worn", "coverage": 0.55, "claimsGround": False, "radius": 3,
     "points": [[21, -25], [30, -28], [40, -30], [50, -29]], "pave": SHORE_MIX},
    house("warehouse-w", -46, -38, -38, -30, WAREHOUSE, "posX", 11),
    house("store-e", 4, -36, 12, -30, STORE, "negX", 12),
    tree("oak-1", -42, -52, "oak-a", 1), tree("oak-2", 42, -70, "oak-b", 2), tree("oak-3", 8, -66, "oak-b", 3),
    boulder("stone-1", 40, -18, "round", 4, 21), boulder("stone-2", 30, -34, "angular", 3, 22),
    boulder("stone-3", 36, -60, "outcrop", 5, 23),
    {"id": "sward", "kind": "flora", "seed": 9, "points": [[-50, -75], [50, -75], [50, -10], [-50, -10]],
     "spec": {"coverage": 0.3, "scale": 12, "octaves": 3, "fernShare": 0.1, "flowerShare": 0.08, "flowerScale": 16, "tallShare": 0.03}},
  ]}

finish = {
  "authors": ["Fable 5.1"], "created": "2026-09-11",
  "themes": THEMES, "mapTheme": "headland",
  "themeById": {"head-e-12": "quay", "head-e-13": "strand"},
  "shapePropsById": {"head-e-12": {"relief_scope": "exclude"}},
  "roomStyles": {"spawn": HALL},
  "addShapes": FLIGHTS,
  "relief": RELIEF,
  "dressing": DRESSING,
}
json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
json.dump(finish, open(f"{HERE}/{SLUG}.finish.json", "w"), indent=1)
print("wrote", SLUG)
