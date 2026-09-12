"""Ashcombe Delph — a worked quarry on a moor. Each team's monument stands on the bench above the quarry
face; the loading yard below it is where the bridges land. The face is worked deeper in some bays than
others, so the yard bites into the moor here and the moor reaches the sound there. Four ways onto the
bench: the haul ramp at the west end, the face itself with a placed block, and the adits — two mouths in
the face feeding one gallery under the bench, which comes up two flights, one west of the monument and
one beside it."""
import json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fable-ashcombe-delph"
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
SBRICK, PLANK_S, LOG_S, PLANK_D = solid(98), solid(5, 1), solid(17, 1), solid(5, 5)

def cell(pal, size, seed, rise=0, jitter=40):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 2, "palette": pal, "rise": rise}
def depth(*bands):
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
def slope(*bands):
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
ROCK = cell([STONE, ANDESITE], 9, 31, rise=3)
CLIFF = depth((DIRT, 1), (ROCK, 40))          # a cut through the moor: one course of soil, then the rock
def theme(surface, surface_depth, wall, fill):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
            "rim": {"enabled": False, "depth": 1, "material": STONE},
            "surface": {"enabled": True, "depth": surface_depth, "material": surface},
            "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": fill}
THEMES = {
  "moor": theme(slope((depth((GRASS, 1), (DIRT, 2)), 30), (depth((COARSE, 1), (DIRT, 2)), 15), (ROCK, 45)), 3, CLIFF, ROCK),
  "yard": theme(cell([GRAVEL, ANDESITE, COBBLE], 6, 12), 1, ROCK, ROCK),     # worked ground: stone to the bone
  "rock": theme(STONE, 1, ROCK, ROCK),
  "adit": theme(cell([GRAVEL, COBBLE], 5, 14), 1, ROCK, ROCK),
  "stair": theme(SBRICK, 1, SBRICK, SBRICK),
  "crag": theme(ROCK, 2, ROCK, ROCK),
}

YARD, BENCH, TERRACE = 12, 20, 26
plan = {
  "plan": 2, "meta": {"name": "Ashcombe Delph"},
  "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 12, "surface": YARD, "observerY": 60},
  "pieces": [
    # the yard, worked to a different depth in each bay
    {"id": "yard-w",  "role": "piece", "rect": [-10, -12, 5, 8], "surface": YARD},
    {"id": "yard-mw", "role": "piece", "rect": [-5, -8, 5, 4],   "surface": YARD},
    {"id": "yard-me", "role": "piece", "rect": [0, -11, 5, 7],   "surface": YARD},
    {"id": "yard-e",  "role": "piece", "rect": [5, -9, 5, 5],    "surface": YARD},
    # the bench, whatever the yard left of it
    {"id": "bench-w",  "role": "piece", "rect": [-10, -16, 5, 4], "surface": BENCH},
    {"id": "bench-mw", "role": "piece", "rect": [-5, -16, 5, 8],  "surface": BENCH},
    {"id": "bench-me", "role": "piece", "rect": [0, -16, 5, 5],   "surface": BENCH},
    {"id": "bench-e",  "role": "piece", "rect": [5, -16, 5, 7],   "surface": BENCH},
    # the terrace the spawn stands on
    {"id": "terrace-w", "role": "piece", "rect": [-10, -22, 8, 6], "surface": TERRACE},
    {"id": "terrace-m", "role": "piece", "rect": [-2, -18, 4, 2],  "surface": TERRACE},
    {"id": "spawn",     "role": "spawn", "rect": [-2, -22, 4, 4],  "surface": TERRACE},
    {"id": "terrace-e", "role": "piece", "rect": [2, -22, 8, 6],   "surface": TERRACE},
  ],
  "zones": [{"id": "sound", "rect": [-10, -4, 20, 8], "holes": []}],
  "placements": {
    "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 8], "facing": "back", "footprint": [5, 3, 10, 10]}],
    "wools": [], "iron": [],
    "destroyables": [{"id": "destroyable-1", "piece": "bench-me", "at": [2, 20], "style": "pillar-3",
                      "materials": "obsidian", "float": 4, "name": "Delph Monument"}],
    "cores": []},
  "walls": [], "boxes": []}

def post(route, body):
    req = urllib.request.Request(API + route, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(req))
compiled = post("/plan/compile", plan)["layout"]
shapes = {s["id"]: s for lay in compiled["layers"] for s in lay["layout"]["shapes"] if s.get("vertices")}
by_height = {s["base_height"]: sid for sid, s in shapes.items() if s.get("operation") == "add" and s.get("base_height") in (YARD, BENCH, TERRACE)}
print("compiled:", {sid: (s["base_height"], s["vertices"]) for sid, s in shapes.items()})

def edits(shape_id, wanted):
    """(A, B, P) puts P on the edge A->B; ("remove", V) takes vertex V out. Indices are read off the ring
    as it stands at each step, in the order the driver replays them."""
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

# ── the adits: rock under the bench, corridors cut through it, flights up out of it ────────────────
def rect(sid, x0, z0, x1, z1, floor, h, th, **more):
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": h, "theme": th, **more}
ROCK_TOP, ADIT_FLOOR = 16, 12
UNDER = [
  rect("rock-w",  -50, -80, -25, -60, 0, ROCK_TOP, "rock"),
  rect("rock-mw", -25, -80,   0, -40, 0, ROCK_TOP, "rock"),
  rect("rock-me",   0, -80,  25, -55, 0, ROCK_TOP, "rock"),
  rect("rock-e",   25, -80,  50, -45, 0, ROCK_TOP, "rock"),
  # the corridors overwrite the rock's column outright, which is what cuts them
  rect("adit-e",   12, -70, 17, -55, 0, ADIT_FLOOR, "adit", override=True),
  rect("adit-far", 32, -70, 37, -45, 0, ADIT_FLOOR, "adit", override=True),
  rect("gallery", -36, -70, 37, -65, 0, ADIT_FLOOR, "adit", override=True),
  rect("rise-c",   -8, -65, -3, -49, 0, ADIT_FLOOR, "adit", override=True),
]
def flight(sid, x0, z0, x1, z1, anchors):
    return {"id": sid, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "floor": ADIT_FLOOR, "base_height": BENCH - ADIT_FLOOR, "theme": "stair",
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]], "anchor_heights": anchors}
FLIGHTS = [
  flight("flight-w", -36, -70, -20, -65, [8, 1, 1, 8]),      # up out of the gallery's west end, onto the bench
  flight("flight-c", -8, -65, -3, -49, [1, 1, 8, 8]),        # up beside the monument
]
# the flight from the bench to the terrace: a made thing, stone the whole way, on its own
TERRACE_FLIGHT = {"id": "terrace-flight", "type": "polygon", "operation": "add", "override": True, "keepClear": True,
                  "floor": ROCK_TOP, "base_height": TERRACE - ROCK_TOP, "theme": "stair", "height_mode": "level", "skirt": 0,
                  "relief_scope": "exclude",
                  "vertices": [[-3, -77], [3, -77], [3, -90], [-3, -90]], "anchor_heights": [BENCH - ROCK_TOP, BENCH - ROCK_TOP, TERRACE - ROCK_TOP, TERRACE - ROCK_TOP]}
# a crag over the west bench, eased into the moor over eight blocks, with the office at its foot
CRAG = {"id": "crag", "type": "polygon", "operation": "add", "theme": "crag",
        "floor": 0, "base_height": BENCH + 14, "height_mode": "level", "skirt": 8,
        "vertices": [[-50, -80], [-40, -80], [-38, -74], [-40, -68], [-46, -66], [-50, -68]]}
# two low walls, cover built out of the quarry's own stone
def wall(sid, x0, z0, x1, z1):
    return {"id": sid, "type": "rectangle", "operation": "add", "override": True, "keepClear": True,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1, "floor": 0, "base_height": 2,
            "height_mode": "raise", "skirt": 0, "theme": "stair"}
WALLS = [wall("wall-bench", 1, -52, 11, -51), wall("wall-yard", -22, -30, -8, -29)]

RELIEF = {"team": {
  "base": YARD, "reach": 0, "step": 1, "landform": "plain",
  "grain": {"amplitude": 0.6, "scale": 11, "seed": 7},
  "marks": [
    # the west bay is worked four courses shallower than the east, so the yard falls across its width
    {"id": "yard-w", "kind": "area", "h": 16, "bevel": 3, "ring": [[-50, -20], [-27, -20], [-27, -58], [-50, -58]]},
    {"id": "yard-e", "kind": "area", "h": 12, "bevel": 3, "ring": [[3, -20], [50, -20], [50, -43], [27, -43], [23, -53], [3, -53]]},
    # the face, traced east to west so the bench is on its -z hand, jogging with the bays
    {"id": "face-e", "kind": "scarp", "high": BENCH, "low": 12, "face": 3, "band": 3,
     "points": [[60, -46], [27, -46], [23, -56], [2, -56], [-2, -40], [-25, -40]]},
    {"id": "face-w", "kind": "scarp", "high": BENCH, "low": 16, "face": 3, "band": 3,
     "points": [[-25, -60], [-60, -60]]},
    {"id": "bench", "kind": "area", "h": BENCH,
     "ring": [[-50, -63], [-24, -63], [-22, -43], [-2, -43], [2, -58], [23, -58], [27, -48], [50, -48], [50, -78], [-50, -78]]},
    {"id": "terrace", "kind": "area", "h": TERRACE,
     "ring": [[-50, -81], [40, -81], [40, -110], [-50, -110]]},
    # the haul ramp up the west face, one course every two blocks
    {"id": "haul", "kind": "line", "points": [[-40, -50], [-40, -58], [-40, -66]], "h": [16, 18, 20], "r": 4, "tread": 1},
  ],
  "pushes": []}}

def storey(clear, wall_bands, post, windows):
    return {"clear": clear, "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}}, "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": None, "headroom": clear + 1}
WIN_LATTICE = {"form": "stairLattice", "block": 134, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_PANE = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 1, "spacing": 3}
STONEWALL = {"kind": "noise", "seed": 41, "scale": 3, "octaves": 1, "stops": [COBBLE, ANDESITE], "rise": 2}
LAID = {"kind": "laidLog", "id": 17, "data": 1}
def office(storeys, beams=True):
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
GROUND_STOREY = storey(3, [{"material": STONEWALL, "thickness": 3}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)
LOFT = storey(3, [{"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)
OFFICE = office([GROUND_STOREY, LOFT])
STORE = office([GROUND_STOREY], beams=False)
HALL = office([GROUND_STOREY, LOFT])

def house(pid, x0, z0, x1, z1, style, front, seed):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground", "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
def spruce(pid, x, z, h, seed):
    return {"id": pid, "kind": "tree", "seed": seed, "layer": "ground", "form": "template", "species": "spruce", "height": h, "x": x, "z": z}
ERRATIC = {"kind": "noise", "seed": 51, "scale": 3, "octaves": 1, "stops": [STONE, COBBLE, ANDESITE], "rise": 2}
def boulder(pid, x, z, form, size, seed):
    return {"id": pid, "kind": "boulder", "seed": seed, "layer": "ground", "x": x, "z": z, "form": form, "size": size, "mossy": False, "rock": ERRATIC}
ROAD = cell([GRAVEL, ANDESITE, COBBLE], 3, 21)
FIRS = [(-38, -98, 13), (-30, -106, 12), (-24, -84, 10),
        (38, -98, 13), (36, -105, 10), (20, -101, 12), (44, -88, 11),
        (-47, -84, 12), (46, -72, 11), (-20, -78, 10)]
DRESSING = {"props": [
  {"id": "road", "kind": "stroke", "seed": 5, "style": "solid", "claimsGround": True, "radius": 2, "pave": ROAD,
   "points": [[0, -95], [0, -91]]},
  {"id": "road-bench", "kind": "stroke", "seed": 6, "style": "solid", "claimsGround": True, "radius": 2, "pave": ROAD,
   "points": [[0, -77], [-12, -71], [-26, -66], [-38, -62], [-40, -56], [-40, -34], [-32, -26]]},
  house("office", -36, -80, -28, -73, OFFICE, "posX", 11),
  house("store", 26, -104, 33, -98, STORE, "negX", 12),
] + [spruce(f"fir-{n}", x, z, h, n + 1) for n, (x, z, h) in enumerate(FIRS)] + [
  boulder("stone-1", -20, -46, "round", 3, 21), boulder("stone-2", 40, -62, "angular", 4, 22),
  boulder("stone-3", 14, -72, "round", 3, 23),
  {"id": "sward", "kind": "flora", "seed": 9, "points": [[-50, -110], [50, -110], [50, -20], [-50, -20]],
   "spec": {"coverage": 0.3, "scale": 12, "octaves": 3, "fernShare": 0.12, "flowerShare": 0.06, "flowerScale": 16, "tallShare": 0.04}},
]}

yard_id, bench_id, terrace_id = by_height[YARD], by_height[BENCH], by_height[TERRACE]
finish = {
  "authors": ["Fable 5.1"], "created": "2026-09-12",
  "themes": THEMES, "mapTheme": "moor",
  "themeById": {yard_id: "yard"},
  "shapePropsById": {bench_id: {"floor": ROCK_TOP, "base_height": BENCH - ROCK_TOP}},
  "roomStyles": {"spawn": HALL},
  "addLayers": [{"id": "under", "name": "Under the bench", "base_y": 0, "below": True, "shapes": UNDER,
                 "groups": [{"id": "under", "name": "under", "mirrors": True, "shapeIds": [s["id"] for s in UNDER]}]}],
  "addShapes": FLIGHTS + [TERRACE_FLIGHT, CRAG] + WALLS,
  "editShapes": {
    # the yard's coast: cracked, in and out, never a line
    yard_id: edits(yard_id, [((50, -20), (-50, -20), (34, -23)), ((34, -23), (-50, -20), (20, -16)),
                             ((20, -16), (-50, -20), (6, -21)), ((6, -21), (-50, -20), (-8, -17)),
                             ((-8, -17), (-50, -20), (-24, -24)), ((-24, -24), (-50, -20), (-40, -18))]),
    # the terrace's back corners cut away, so the ground behind the spawn is not a dead square
    terrace_id: edits(terrace_id, [((-50, -110), (50, -110), (-32, -110)), ((-50, -80), (-50, -110), (-50, -94)),
                                   ("remove", (-50, -110)),
                                   ((-32, -110), (50, -110), (32, -110)), ((50, -110), (50, -80), (50, -94)),
                                   ("remove", (50, -110))]),
  },
  "relief": RELIEF,
  "dressing": DRESSING,
}
json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
json.dump(finish, open(f"{HERE}/{SLUG}.finish.json", "w"), indent=1)
print("wrote", SLUG)
