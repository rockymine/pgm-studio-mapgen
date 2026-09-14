#!/usr/bin/env python3
"""Birkmire — the plan and the finish.

A destroy-the-core board on a frozen birch mire. One idea: white bark on white ground, and the core
out on a low holm in the middle of a frozen pan — so the last twenty blocks of every raid are across
open ice with nothing standing on it, and the whole of an attack is the decision to step off the
last hummock.

Everything that is cover on this board is a hummock with birches on it, and the hummocks stop at the
pan's rim on purpose. The pan is two courses below the mire, so it is also an entrance from below:
a player in it is out of sight of anyone standing on the mire and is seen by everyone on the holm.

The ground is finished by its ANGLE. A mire is flat, so almost all of it takes the first band; the
second is the drier shoulder of a hummock and the third is a peat hag's cut face, which is the one
dark thing on the board and is dark because it is a hole in the ground.
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-birkmire"
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894").rstrip("/")
API = API[:-4].rstrip("/") if API.endswith("/api") else API

PAN, HOLM, BANK, MIRE, HUMMOCK, GARTH = 16, 18, 19, 20, 23, 22   # a top block is h - 1

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
plan = {
    "plan": 2,
    "meta": {"name": "Birkmire"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 20, "surface": 20, "observerY": 54},
    "pieces": [
        {"id": "mire", "role": "piece", "rect": [-8, 2, 16, 15], "surface": 20},
        {"id": "holt", "role": "spawn", "rect": [-3, 17, 6, 3],  "surface": 21},
    ],
    "zones": [{"id": "lead", "rect": [-8, -4, 16, 8], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "holt", "at": [15, 7], "facing": "front",
                    "footprint": [7, 2, 16, 10]}],
        "iron":   [{"id": "iron-1", "piece": "holt", "at": [3, 7]},
                   {"id": "iron-2", "piece": "holt", "at": [27, 7]}],
        # a core states its interior — a casing size and a wall thickness are two numbers that can
        # contradict each other, and `lava` cannot. Float and leak pair: the lava free-falls six to
        # the holm and has to fall five to count, so a breach over open ground ends it.
        "cores": [{"id": "core-1", "piece": "mire", "at": [22, 42], "lava": 3, "lavaHeight": 3,
                   "float": 6, "leak": 5, "name": "The Thaw"}],
        "destroyables": [], "wools": [],
    },
    "walls": [], "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

SNOW, ICE, PACKED = solid(80), solid(79), solid(174)
GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
STONEBRICK, CHISELLED = solid(98), solid(98, 3)
BIRCH_LOG, BIRCH_PLANK = solid(17, 2), solid(5, 2)
WHITE_CLAY, PALE_CLAY, BLUE_CLAY = solid(159, 0), solid(159, 8), solid(159, 3)
LAID_BIRCH = {"kind": "laidLog", "id": 17, "data": 2}


def cell_(seed, size, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


MOSS = cell_(31, 9, [SNOW, GRASS])          # lying snow with the mire's turf showing through
SHOULDER = cell_(32, 6, [COARSE, SNOW])     # a hummock's drier flank
HAG = cell_(33, 8, [PODZOL, COARSE], rise=4)  # a peat hag's cut face: the one dark thing here
PEAT = cell_(34, 9, [COARSE, DIRT], rise=6)   # the body, which nobody sees until a face is cut

MIRE_SURFACE = layered([
    (10, layered([(1, MOSS), (2, DIRT)])),        # under 10 degrees: the mire itself
    (16, layered([(1, SHOULDER), (2, COARSE)])),  # 10-26: a hummock's flank
    (64, layered([(1, HAG), (3, COARSE)])),       # over 26: a cut peat face over its own soil
], axis="slope")

themes = {
    "mire": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COARSE},
        "surface": {"enabled": True, "depth": 4, "material": MIRE_SURFACE},
        "wall":    HAG, "wallEnabled": True,
        "fill":    PEAT,
    },
    # the pan: frozen hard, walked on, and the only place on the board with no cover at all
    "ice": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": PACKED},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(35, 11, [ICE, PACKED])), (2, PACKED)])},
        "wall":    cell_(36, 9, [PACKED, ICE], rise=5), "wallEnabled": True,
        "fill":    cell_(37, 9, [STONE, GRAVEL], rise=6),
    },
    # the garth: the pad cut into the north-west shoulder that the bothy stands on. Trodden ground
    # rather than mire — gravel walked bare over its own coarse soil, so the cut reads as used.
    "garth": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COBBLE},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(42, 5, [GRAVEL, COARSE, COBBLE])), (2, COARSE)])},
        "wall":    cell_(43, 7, [STONE, COBBLE, ANDESITE], rise=4), "wallEnabled": True,
        "fill":    cell_(44, 9, [STONE, ANDESITE], rise=5),
    },
    # the holm: shingle washed up round a knuckle of rock, two courses over the ice
    "holm": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(38, 6, [GRAVEL, SNOW])), (2, GRAVEL)])},
        "wall":    cell_(39, 8, [STONE, GRAVEL], rise=4), "wallEnabled": True,
        "fill":    cell_(40, 9, [STONE, ANDESITE], rise=5),
    },
}

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def lobe(cx, cz, radii, tilt=0.0):
    n = len(radii)
    return [[round(cx + r * math.cos(tilt + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(tilt + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]


relief = {
    "team": {
        "base": MIRE, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 18, "seed": 5},
        "marks": [
            # the bank: flat to the water's edge, because a bridge lands on something level
            {"id": "bank", "kind": "area", "h": BANK, "bevel": 3,
             "ring": lobe(0, 18, [41, 35, 39, 34, 41, 35, 39, 34], 0.25)},
            # the pan: four courses under the mire and open right across. It is stated BEFORE the
            # holm, because a later mark wins a contested cell.
            {"id": "pan", "kind": "area", "h": PAN, "bevel": 3,
             "ring": lobe(-18, 52, [27, 22, 25, 21, 28, 23, 24, 20], 0.5)},
            # the holm the core stands on: two courses over the ice, so stepping onto it costs a
            # placed block anywhere but the spit
            {"id": "holm", "kind": "area", "h": HOLM, "bevel": 1,
             "ring": lobe(-18, 52, [9, 7, 8, 7, 9, 7, 8, 7], 0.2)},
            # the spawn's garth
            {"id": "garth", "kind": "area", "h": GARTH, "bevel": 4,
             "ring": lobe(0, 92, [26, 22, 25, 20, 26, 22, 25, 20], 0.1)},
            # the hummocks: the dry ground a birch can stand on, and the only cover on the board.
            # Small radii, left to the relaxation — a wide radius pins a flat disc and builds a mesa.
            # There is no hummock on the pan's own ground: a mark standing seven courses over an area
            # mark's pinned band puts the whole difference in one cell (`RL3`), and the pan is the
            # one place on this board that is meant to have nothing on it at all.
            {"id": "hum-nw", "kind": "point", "at": [-34, 70], "r": 4, "h": HUMMOCK + 1},
            {"id": "hum-n",  "kind": "point", "at": [-6, 74],  "r": 5, "h": HUMMOCK},
            {"id": "hum-e",  "kind": "point", "at": [26, 44],  "r": 4, "h": HUMMOCK},
            # hum-s stands on the bank, so it is two courses over it rather than three — a step a
            # player scrambles instead of a seam that reads back as a wall.
            {"id": "hum-s",  "kind": "point", "at": [8, 32],   "r": 5, "h": BANK + 2},
        ],
        "pushes": [
            # the holt: the rise the wood stands on, east of the pan. The two gradients agree —
            # 5/8 up the skirt and 5/8 to the crown — so it is a hill and not a wall with a hill on
            # top of it (`RL6`).
            {"id": "holt-rise", "ring": lobe(24, 62, [10, 8, 9, 8, 10, 8, 9, 8], 0.4),
             "amount": 5, "falloff": 8, "crown": 5, "roughness": 1.5, "seed": 6},
            # and a low swell on the north-west so the mire is not one plane
            {"id": "swell", "ring": lobe(-30, 78, [9, 7, 8, 7, 9, 7, 8, 7], 0.9),
             "amount": 4, "falloff": 7, "crown": 4, "roughness": 1, "seed": 7},
        ],
    }
}

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
SHINGLE = cell_(41, 4, [GRAVEL, COBBLE, ANDESITE], rise=2)


def flight(id_, ring, low, high):
    """One polygon, a height per vertex, run at least twice the rise, sheer-sided and kept clear —
    and a material rather than a theme, because a made thing is not a place."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": SHINGLE,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


def patch(id_, ring, theme):
    """A paint patch on solved ground. It declares a height_mode or `ShapeScopeOwners` never makes it
    a candidate and it paints nothing, in silence; a raise of 0 sits flush at the median ground."""
    return {"id": id_, "type": "polygon", "operation": "add", "group": "team",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": [[x, z] for x, z in ring], "theme": theme}


add_shapes = [
    # the spit: the one walked way onto the holm, off the pan's north rim. Six blocks of run for two
    # courses, which is three times the rise — the rest of the holm costs a placed block.
    flight("spit", [(-22, 60), (-16, 60), (-16, 66), (-22, 66)], PAN, HOLM),
    # the ice, drawn rather than sampled: a pan is a shape and its edge is where the shape ends
    patch("ice-pan", lobe(-18, 52, [27, 22, 25, 21, 28, 23, 24, 20], 0.5), "ice"),
    patch("holm-top", lobe(-18, 52, [9.5, 7.5, 8.5, 7.5, 9.5, 7.5, 8.5, 7.5], 0.2), "holm"),
    # and the shore of the sound, which is the same ice at the board's own edge
    patch("ice-shore", [(-40, 12), (40, 12), (40, 21), (12, 24), (-14, 22), (-40, 24)], "ice"),
    # the garth: a pad cut level into the north-west shoulder. `relief_scope: "exclude"` takes the
    # footprint out of the solve, so the shoulder — which stands at 30 over the crown and 25 at the
    # track — meets the pad at a face instead of being graded into it. The back of the garth is that
    # face; the track comes in over the low east side, where the two are within a block.
    {"id": "garth-pad", "type": "polygon", "operation": "add", "group": "team",
     "height_mode": "level", "base_height": 26, "skirt": 0, "relief_scope": "exclude",
     "theme": "garth",
     "vertices": [[-37, 73], [-25, 73], [-25, 83], [-37, 83]]},
]

# ── the bothy ────────────────────────────────────────────────────────────────────────────────────
# Three families named before painting: the ground is WHITE, what is built is white-limed clay on a
# stone footing, and the accent is BIRCH — the frame, the beams and the wood, which is the one thing
# on this board that is a colour rather than a value.
def bothy_style(storeys):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": 2, "slab": 44, "slabData": 5, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": STONEBRICK, "verge": LAID_BIRCH, "gable": BIRCH_PLANK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(1, WHITE_CLAY)], "repeat"), "extent": 5},
        "post": BIRCH_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 4},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1}, "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 4, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(1, COBBLE), (3, WHITE_CLAY)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 1, "height": 2, "spacing": 4},
}
UPPER_STOREY = {
    "clear": 3, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(2, PALE_CLAY), (1, LAID_BIRCH)], "repeat"), "extent": 3},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 1, "spacing": 4},
}
bothy = bothy_style([GROUND_STOREY, UPPER_STOREY])
hut = bothy_style([dict(GROUND_STOREY, clear=4)])

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
BIRCHES = ["tree-showcase-r13-%d" % n for n in (2, 4, 6, 8, 10)]


def library_tree(name):
    with urllib.request.urlopen(f"{API}/api/tree-styles") as handle:
        index = {row["name"]: row["id"] for row in json.load(handle)}
    with urllib.request.urlopen(f"{API}/api/tree-styles/{index[name]}") as handle:
        style = json.load(handle)
    return {"kind": "tree", "form": "copied", "body": style["body"]}


def path(id_, points, radius, pave, style="solid", coverage=1.0, seed=0, claims=True):
    return {"id": id_, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": claims, "pave": pave, "points": points}


WAY = cell_(42, 5, [GRAVEL, ANDESITE, COBBLE])

BOULDER = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell_(43, 4, [STONE, COBBLE, ANDESITE], rise=2)}

props = [
    # the ways, drawn before the scenery. The mire is soft, so a track on it is laid: the spine runs
    # from the door to the pan's north rim and stops at the water, and the flank road serves the
    # holt and the east shore.
    path("track", [[0, 86], [-6, 74], [-14, 66], [-18, 64]], 2, WAY, seed=51),
    path("track-east", [[8, 86], [14, 74], [18, 60], [22, 46], [26, 36]], 2, WAY, seed=52),
    path("track-shore", [[-30, 26], [-18, 22], [-4, 22], [10, 26], [20, 32]], 2, WAY, seed=53),
    path("track-bothy", [[-12, 80], [-18, 79], [-24, 79]], 2, WAY, seed=54),
    # the bothy: a two-storey house with a low cross wing, out on the north-west shoulder where the
    # west road runs — clear of the spawn door's own approach (`DR-KEEP`), and nowhere near the
    # Thaw's ten-block keep-out (`OB19`)
    {"id": "bothy", "kind": "house", "seed": 611, "front": "posX", "style": "bothy",
     "wings": [{"corners": [[-36, 74], [-30, 82]], "spec": {"ridge": "alongZ"}},
               {"corners": [[-29, 77], [-26, 81]], "spec": {"storeysHigh": 1, "ridge": "alongX"}}]},
    {"id": "sward", "kind": "flora", "seed": 910,
     "points": [[-38, 12], [38, 12], [38, 98], [-38, 98]],
     "spec": {"coverage": 0.20, "scale": 24, "octaves": 3, "fernShare": 0.35,
              "flowerShare": 0.04, "flowerScale": 12, "tallShare": 0.04}},
]
# the birches: on the hummocks and on the holt, ten apart, and none of them on the pan — the ice is
# the one place with nothing on it, and that is the whole point of the board. `DR-CLAIM` is footprint
# overlap rather than a standoff, and a copied body is wider than the template one.
for i, (x, z) in enumerate([(-38, 40), (-24, 30), (-36, 68), (-24, 70), (26, 58), (36, 62),
                            (28, 72), (38, 74), (10, 44), (30, 44), (2, 34)]):
    props.append({"id": f"birk-{i}", "kind": "tree", "seed": 710 + i, "x": x, "z": z,
                  "style": BIRCHES[i % len(BIRCHES)]})
# erratics: stone, cobblestone and andesite and nothing else. Each is on the mire's own ground at a
# place a player would otherwise cross without a decision.
for i, (x, z) in enumerate([(-4, 58), (6, 58), (-32, 20), (34, 32), (16, 36), (20, 76)]):
    props.append(dict(BOULDER, id=f"erratic-{i}", kind="boulder", seed=810 + i, x=x, z=z,
                      size=4 if i % 2 == 0 else 3))

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-13",
    "themes": themes,
    "mapTheme": "mire",
    # Ice plains tints grass #80b497, so the turf under the snow reads as a cold pale mint rather
    # than a summer meadow running through a snowfield
    "biome": {"kind": "solid", "id": 12},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": hut},
    "dressing": {"styles": dict({name: library_tree(name) for name in BIRCHES},
                                bothy={"kind": "house", "shell": bothy}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
