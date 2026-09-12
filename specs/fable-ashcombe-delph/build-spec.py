"""Ashcombe Delph — a worked quarry on a moor. Each team's monument stands on the bench above the
quarry face; the loading yard below it is where the bridges land. Three ways onto the bench: the haul
ramp round the west end, the face itself with a placed block or two, and the adit — a tunnel cut into
the face that runs under the bench and comes up a flight beside the monument."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fable-ashcombe-delph"

def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
SBRICK, PLANK_S, LOG_S, PLANK_D = solid(98), solid(5, 1), solid(17, 1), solid(5, 5)

def cell(a, b, size, seed, rise=0, jitter=40):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 2,
            "palette": [a, b], "rise": rise}
def cell3(a, b, c, size, seed, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 40, "warp": 2,
            "palette": [a, b, c], "rise": rise}
def depth(*bands):
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat",
            "bands": [{"material": m, "thickness": t} for m, t in bands]}}
def slope(*bands):
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat",
            "bands": [{"material": m, "thickness": t} for m, t in bands]}}

ROCK = cell(STONE, ANDESITE, 9, 31, rise=3)            # the body of the hill, seen only where it is cut
CLIFF = depth((COARSE, 1), (DIRT, 1), (ROCK, 40))        # a cut face: a lip of soil, then the rock
def theme(surface, surface_depth, wall, fill, rim=False):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
            "rim": {"enabled": rim, "depth": 1, "material": STONE},
            "surface": {"enabled": True, "depth": surface_depth, "material": surface},
            "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": fill}

THEMES = {
  # the moor: grass on the flat, coarse dirt on the shoulders, bare rock on the faces of the same hill
  "moor": theme(slope((depth((GRASS, 1), (DIRT, 2)), 28),
                      (depth((COARSE, 1), (DIRT, 2)), 17),
                      (ROCK, 45)), 3, CLIFF, ROCK),
  # the loading yard: worked ground, gravel and mud
  "yard": theme(cell(GRAVEL, COARSE, 7, 12), 1, CLIFF, ROCK),
  # the rock the adit is cut through
  "rock": theme(STONE, 1, ROCK, ROCK),
  # the adit floor
  "adit": theme(cell(GRAVEL, COBBLE, 5, 14), 1, ROCK, ROCK),
  # a flight of steps is made, and reads as one stone the whole way up
  "stair": theme(SBRICK, 1, SBRICK, SBRICK),
}

plan = {
  "plan": 2, "meta": {"name": "Ashcombe Delph"},
  "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 12, "surface": 12, "observerY": 58},
  "pieces": [
    {"id": "yard",      "role": "piece", "rect": [-10, -6, 20, 4], "surface": 12},
    {"id": "bench",     "role": "piece", "rect": [-10, -14, 20, 8], "surface": 20},
    {"id": "terrace-w", "role": "piece", "rect": [-10, -20, 8, 6], "surface": 26},
    {"id": "terrace-m", "role": "piece", "rect": [-2, -16, 4, 2], "surface": 26},
    {"id": "spawn",     "role": "spawn", "rect": [-2, -20, 4, 4], "surface": 26},
    {"id": "terrace-e", "role": "piece", "rect": [2, -20, 8, 6], "surface": 26},
  ],
  "zones": [{"id": "sound", "rect": [-10, -2, 20, 4], "holes": []}],
  "placements": {
    "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 8], "facing": "back",
                "footprint": [5, 3, 10, 10]}],
    "wools": [], "iron": [],
    "destroyables": [{"id": "destroyable-1", "piece": "bench", "at": [50, 18],
                      "style": "pillar-3", "materials": "obsidian", "float": 4,
                      "name": "Delph Monument"}],
    "cores": []},
  "walls": [], "boxes": []}

# ── the adit: rock under the bench, a corridor through it, a flight out of it ──────────────────
TX0, TX1 = 17, 22            # the corridor's x span
MOUTH, DIVE, FOOT, HEAD = -30, -48, -48, -64   # the face, where the flight starts, and where it lands
def rect(sid, x0, z0, x1, z1, floor, h, th, **more):
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0,
            "max_x": x1, "max_z": z1, "floor": floor, "base_height": h, "theme": th, **more}
UNDER = [
  rect("rock-w", -50, -70, TX0, MOUTH, 0, 16, "rock"),
  rect("rock-e", TX1, -70, 50, MOUTH, 0, 16, "rock"),
  rect("rock-s", TX0, -70, TX1, HEAD, 0, 16, "rock"),
  rect("adit", TX0, HEAD, TX1, MOUTH, 0, 12, "adit"),
]
FLIGHT = {"id": "adit-flight", "type": "polygon", "operation": "add", "override": True,
          "keepClear": True, "floor": 12, "base_height": 8, "theme": "stair",
          "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
          "vertices": [[TX0, FOOT], [TX1, FOOT], [TX1, HEAD], [TX0, HEAD]],
          "anchor_heights": [1, 1, 8, 8]}

def ring(cx, cz, rx, rz, n=9, seed=0):
    import math
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        wob = 1 + 0.12 * math.sin(3 * a + seed)
        out.append([round(cx + rx * wob * math.cos(a)), round(cz + rz * wob * math.sin(a))])
    return out

RELIEF = {"team": {
  "base": 12, "reach": 0, "step": 1, "landform": "plain",
  "grain": {"amplitude": 0.6, "scale": 11, "seed": 7},
  "marks": [
    # the quarry face: the yard at 12, the bench at 20, three blocks of rock between them
    {"id": "face", "kind": "scarp", "points": [[60, MOUTH - 2], [20, MOUTH - 1], [-20, MOUTH - 2], [-60, MOUTH - 1]],
     "high": 20, "low": 12, "face": 3, "band": 4},
    # the bench the monument stands on, held flat to its edge
    {"id": "bench", "kind": "area", "h": 20, "ring": [[-50, -36], [50, -36], [50, -64], [30, -68], [-30, -68], [-50, -64]]},
    # the spawn terrace, graded down over its front edge
    {"id": "terrace", "kind": "area", "h": 26, "bevel": 5,
     "ring": [[-50, -78], [-30, -76], [0, -78], [30, -76], [50, -78], [50, -100], [-50, -100]]},
    # the haul ramp round the west end of the face, one course every two blocks
    {"id": "haul", "kind": "line", "points": [[-40, -18], [-40, -26], [-40, -34], [-40, -42]],
     "h": [12, 14, 17, 20], "r": 4, "tread": 1},
  ],
  "pushes": []}}

# ── the two buildings: one style, a stone ground storey under a timbered loft ─────────────────
def storey(clear, wall_bands, post, windows):
    return {"clear": clear, "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}},
            "post": post, "windows": windows,
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
            "deck": None, "headroom": clear + 1}
WIN_LATTICE = {"form": "stairLattice", "block": 134, "hostBlock": -1, "hostData": 0, "data": 0,
               "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
            "sill": 2, "width": 2, "height": 2, "spacing": 3}
WIN_PANE = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
            "sill": 2, "width": 2, "height": 1, "spacing": 3}
STONEWALL = {"kind": "noise", "seed": 41, "scale": 3, "octaves": 1, "stops": [COBBLE, ANDESITE], "rise": 2}
LAID = {"kind": "laidLog", "id": 17, "data": 1}
def office(storeys):
    return {
      "foundation": {"plate": {"stack": {"bands": [{"material": SBRICK, "thickness": 1}], "ending": "repeat"}, "extent": 1},
                     "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
                     "footing": None},
      "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": False, "hole": False,
               "body": PLANK_D, "verge": LAID, "gable": PLANK_S, "gableWindows": WIN_NONE},
      "wall": {"stack": {"bands": [{"material": STONEWALL, "thickness": 4}], "ending": "repeat"}, "extent": 4},
      "post": LOG_S,
      "windows": WIN_LATTICE,
      "storeys": storeys,
      "porch": None, "front": None,
      "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
      "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab", "fillBlock": 126, "fillData": 0},
                  "width": 2, "height": 3}}
GROUND_STOREY = storey(3, [{"material": STONEWALL, "thickness": 3}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)
LOFT = storey(3, [{"material": PLANK_S, "thickness": 2}, {"material": LAID, "thickness": 1}], LOG_S, WIN_PANE)
OFFICE = office([GROUND_STOREY, LOFT])           # two storeys
STORE = office([storey(3, [{"material": STONEWALL, "thickness": 3}, {"material": LAID, "thickness": 1}], LOG_S, WIN_LATTICE)])
STORE["beams"] = {"block": -1, "data": 0, "reach": 1, "any": False}   # one storey lays no beams
HALL = office([GROUND_STOREY, LOFT])

def house(pid, x0, z0, x1, z1, style, front, seed):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
def spruce(pid, x, z, h, seed):
    return {"id": pid, "kind": "tree", "seed": seed, "layer": "ground", "form": "template",
            "species": "spruce", "height": h, "x": x, "z": z}
ERRATIC = {"kind": "noise", "seed": 51, "scale": 3, "octaves": 1, "stops": [STONE, COBBLE, ANDESITE], "rise": 2}
def boulder(pid, x, z, form, size, seed):
    return {"id": pid, "kind": "boulder", "seed": seed, "layer": "ground", "x": x, "z": z,
            "form": form, "size": size, "mossy": False, "rock": ERRATIC}
ROAD = cell3(GRAVEL, ANDESITE, COBBLE, 3, 21)

DRESSING = {"props": [
  {"id": "road", "kind": "stroke", "seed": 5, "style": "solid", "claimsGround": True, "radius": 2,
   "points": [[0, -80], [0, -72], [-14, -62], [-30, -50], [-40, -40], [-40, -22], [-30, -14]], "pave": ROAD},
  house("office", -46, -58, -38, -51, OFFICE, "posX", 11),
  house("store", 22, -92, 29, -86, STORE, "negX", 12),
  spruce("fir-1", -42, -94, 13, 1), spruce("fir-2", -36, -90, 11, 2), spruce("fir-3", -44, -84, 10, 3),
  spruce("fir-4", 40, -96, 12, 4), spruce("fir-5", 45, -88, 14, 5),
  spruce("fir-6", -46, -73, 12, 6),
  boulder("stone-1", -20, -18, "round", 4, 21), boulder("stone-2", 30, -24, "angular", 5, 22),
  boulder("stone-3", 8, -14, "round", 3, 23), boulder("stone-4", 42, -58, "angular", 4, 24),
  {"id": "sward", "kind": "flora", "seed": 9, "points": [[-50, -100], [50, -100], [50, -10], [-50, -10]],
   "spec": {"coverage": 0.3, "scale": 12, "octaves": 3, "fernShare": 0.12, "flowerShare": 0.06, "flowerScale": 16, "tallShare": 0.04}},
]}

finish = {
  "authors": ["Fable 5.1"], "created": "2026-09-11",
  "themes": THEMES, "mapTheme": "moor",
  "themeById": {"bench-12": "yard"},
  "shapePropsById": {"bench-20": {"floor": 16, "base_height": 4}},
  "roomStyles": {"spawn": HALL},
  "addLayers": [{"id": "under", "name": "Under the bench", "base_y": 0, "below": True,
                 "shapes": UNDER,
                 "groups": [{"id": "under", "name": "under", "mirrors": True, "shapeIds": [s["id"] for s in UNDER]}]}],
  "addShapes": [FLIGHT],
  "relief": RELIEF,
  "dressing": DRESSING,
}
json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
json.dump(finish, open(f"{HERE}/{SLUG}.finish.json", "w"), indent=1)
print("wrote", SLUG)
