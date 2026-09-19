#!/usr/bin/env python3
"""Hushwater — a composed micro CTW board adapted into a place.

The board is a lead hush: two mine heads facing each other across the gill their own
water tore out of the fell, where the dressing floors at the top are flat and made and
everything below them is raw, angled ground.

The arrangement is the composer's. `GET /api/compose?players=18&teams=2&symmetry=rot_180
&seedStart=5` is pinned, read back as a PlanModel, and then adapted: the unit is pushed a
cell back so a shoal fits in the gill, the board is given a height ladder from the gill to
the mine head, the east wool is turned into a walled lane and the west one into an open
spur, a bing is cut off the team's own ground and bridged back, and the flat crossing
is given a spoil bank to fight over.

    PGM_STUDIO_API=... python3 specs/opus5-hushwater/build-spec.py
    tools/drive.py specs/opus5-hushwater "Hushwater" --out maps/opus5-hushwater
"""
import json, os, urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-hushwater"
NAME = "Hushwater"

DESCRIPTOR = {"players": 18, "teams": 2, "symmetry": "rot_180", "cell": 4, "seed": 5,
              "composerVersion": "body-first-1", "schema": 1}

CELL = 4

# ── the studio ────────────────────────────────────────────────────────────────────────────

def get(path):
    with urllib.request.urlopen(API + path, timeout=180) as response:
        return json.load(response)


def post(path, body):
    request = urllib.request.Request(
        API + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


def delete(path):
    request = urllib.request.Request(API + path, method="DELETE")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response.read()
    except Exception:
        pass


def composed():
    """The composer's own plan for this descriptor, pinned and read back. The pinned row is
    dropped again — the spec is what the map is, and the descriptor is what reproduces it."""
    page = get(f"/compose?players={DESCRIPTOR['players']}&teams={DESCRIPTOR['teams']}"
               f"&symmetry={DESCRIPTOR['symmetry']}&seedStart={DESCRIPTOR['seed']}&count=1")
    card = page["cards"][0]
    pinned = post("/compose/pin", {**card["descriptor"], "index": 0})
    plan = json.loads(pinned["planJson"])
    delete(f"/plans/{pinned['id']}")
    return plan, card


# ── the adaptation ────────────────────────────────────────────────────────────────────────

# Every rect is [x, z, w, h] in cells; a block is four of them. The composed unit is kept
# where it recognisably is — ring hub with its yard, a bar frontline fronting it, a spawn
# hung off the back, one wool approach a side — and re-cut piece by piece.
#
#  surface   what stands there                                        relief
#     12     the shoal — the spoil bank standing in the gill            solved (neutral)
#     13     the wash — the scoured shore the crossing lands on         solved (team)
#     14     the bank the frontline is fought on                        solved (team)
#     16     the west spur out to the powder house                      solved (team)
#     17     the yard: the ring's three lower arms, round the shaft     solved (team)
#     18     the mine head, the walled lane and the assay house,
#            and the bing hung off the head's east side                 excluded
#     19     the spawn                                                  excluded
#
# The split is the board's whole idea and the made half of it is SMALL: the mine is a patch
# of laid stone in a fell, not a floor with a fell round it. Only the head, the lane behind
# the gate, the bing and the spawn are stated flat and taken out of the solve; everything
# else — the yard round the shaft included — is ground the relief decides.

PIECES = [
    # the gill and the bank up out of it
    ("frontline-t2", "piece",     [-4,  5,  8, 2], 13),
    ("frontline-t1", "piece",     [-4,  7, 12, 4], 14),
    # the ring: three arms at the floor level, the back arm a course higher at the head
    ("hub-t2",       "piece",     [-4, 11, 10, 4], 17),
    ("hub-t3",       "piece",     [-4, 15,  4, 4], 17),
    ("hub-t4",       "piece",     [ 4, 15,  5, 4], 17),   # the east nose the lane leaves from
    ("hub-t1",       "piece",     [-4, 19, 10, 4], 18),
    ("spawn-t1",     "piece",     [-2, 23,  4, 2], 19),
    ("spawn-room",   "spawn",     [-2, 25,  4, 2], 19),
    # west: the open spur out to the powder house, on moor rather than on made ground
    ("wool-a-t1",    "piece",     [-10, 15, 6, 4], 16),
    ("wool-a-room",  "wool-room", [-13, 16, 3, 2], 16),
    ("wool-a-apron", "piece",     [-13, 18, 3, 1], 16),
    # east: the walled lane out to the assay house
    ("wool-b-t1",    "piece",     [ 9, 15, 4, 4], 18),
    ("wool-b-room",  "wool-room", [13, 16, 2, 3], 18),
    ("wool-b-apron", "piece",     [13, 15, 2, 1], 18),
    # the bing: a team's own ground, cut off and bridged back — the spoil heap the
    # defence drops onto to get in behind its own wall
    ("bing",         "piece",     [10, 22, 4, 3], 18),
    # the gill's spoil bank — two legs, each the other's rot_180 image, so the short hop is
    # on the west hand for one team and the east for the other
    ("shoal-n",      "piece",     [-4,  0,  6, 2], 12, False),
    ("shoal-s",      "piece",     [-2, -2,  6, 2], 12, False),
]

ZONES = [
    # the crossing: one region, docking both frontlines, with the shoal standing in it
    ("mid-band",        [-4, -5, 8, 10]),
    # the two planks onto the bing — team ground on both ends of each, which is what makes
    # the bing a team transient-link (CT4) rather than a mid stone
    ("bing-plank-s",    [10, 19, 4, 3]),
    ("bing-plank-w",    [ 6, 20, 4, 4]),
]

WALLS = [("hub-t4", "wool-b-t1")]

PLACEMENTS = {
    "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [8, 4], "facing": "front"}],
    "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [6, 4]},
              {"id": "wool-2", "piece": "wool-b-room", "at": [4, 6]}],
    # no iron: WX8 wants the cube inside the spawn piece and clear of the shell, and WX1
    # makes the shell that piece inset one block, so a plan-compiled spawn has no room for one
    "iron": [],
    "destroyables": [], "cores": [],
}

BOXES = [
    ("hub",       "hub",       [-4, 11, 13, 12],
     ["hub-t1", "hub-t2", "hub-t3", "hub-t4"]),
    ("spawn",     "spawn",     [-2, 23, 4, 4], ["spawn-t1", "spawn-room"]),
    ("wool-a",    "wool",      [-13, 15, 9, 4], ["wool-a-t1", "wool-a-room", "wool-a-apron"]),
    ("wool-b",    "wool",      [9, 15, 6, 4], ["wool-b-t1", "wool-b-room", "wool-b-apron"]),
    ("frontline", "frontline", [-4, 5, 12, 6], ["frontline-t1", "frontline-t2"]),
    ("mid",       "mid",       [-4, -2, 8, 4], ["shoal-n", "shoal-s"]),
]


# ── the finish ────────────────────────────────────────────────────────────────────────────
#
# Three themes, and each is a place rather than a piece. The MOOR is the fell the mine was
# cut into and is the map default, read by its angle so the turf, the broken shoulder and
# the crag of one hillside are finished by one stack. The FLOOR is the made ground — the
# dressing floors, the lane behind the wall, the mine head — laid stone with a run-striped
# retaining face. The HUSH is the scour itself: the washed gravel the water tore down the
# bank, the shore it dumped at the gill and the spoil bank standing in it, which is the same
# ground at both ends of the fall and is what the board is named for.

STONE       = {"kind": "solid", "id": 1,  "data": 0}
ANDESITE    = {"kind": "solid", "id": 1,  "data": 5}
GRASS       = {"kind": "solid", "id": 2,  "data": 0}
DIRT        = {"kind": "solid", "id": 3,  "data": 0}
COARSE_DIRT = {"kind": "solid", "id": 3,  "data": 1}
COBBLE      = {"kind": "solid", "id": 4,  "data": 0}
GRAVEL      = {"kind": "solid", "id": 13, "data": 0}
STONE_BRICK = {"kind": "solid", "id": 98, "data": 0}


def depth_stack(*courses, beyond=None):
    """A depth stack: the top course, then what lies under it, handing over to the body."""
    return {"kind": "layered", "axis": "depth", "beyond": beyond or STONE,
            "stack": {"ending": "handOver",
                      "bands": [{"thickness": t, "material": m} for t, m in courses]}}


def body():
    """The rock under everything, in the fill where a body belongs — two stones at a cell
    wider than it is tall, so a cut face reads as blobs rather than as vertical runs."""
    return {"kind": "cell", "seed": 21, "cellSize": 9, "jitter": 40, "warp": 3, "rise": 5,
            "palette": [STONE, ANDESITE]}


def moor_surface():
    """The fell read by its angle. A thickness on the slope axis is a span of degrees, so
    one stack finishes the turf, the broken shoulder and the crag of the same hillside; the
    cuts come off GET .../incline, which answers how much ground stands in each ten."""
    return {"kind": "layered", "axis": "slope", "beyond": STONE,
            "stack": {"ending": "repeat", "bands": [
                # the flat and the roll: turf over two of soil
                {"thickness": 12, "material": depth_stack((1, GRASS), (2, DIRT))},
                # the shoulder, where the turf is broken and the soil shows through
                {"thickness": 14, "material": depth_stack(
                    (1, {"kind": "cell", "seed": 23, "cellSize": 5, "jitter": 55, "warp": 3,
                         "palette": [COARSE_DIRT, GRASS]}), (2, DIRT))},
                # the face: rock, mottled so a crag is not one flat grey
                {"thickness": 70, "material": depth_stack(
                    (2, {"kind": "cell", "seed": 5, "cellSize": 6, "jitter": 45, "warp": 2,
                         "palette": [STONE, COBBLE]}), (3, STONE))},
            ]}}


def hush_surface():
    """The scour. Washed gravel where the water ran and bare rock where it cut, on the same
    angle axis — so the shore at the bottom of the fall and the scar at the top are one
    ground and the eye joins them."""
    return {"kind": "layered", "axis": "slope", "beyond": STONE,
            "stack": {"ending": "repeat", "bands": [
                # a hush strips the turf to subsoil before it gets to rock, so the flat of
                # it is brown-and-pale rather than grey
                {"thickness": 12, "material": depth_stack(
                    (1, {"kind": "cell", "seed": 17, "cellSize": 7, "jitter": 45, "warp": 3,
                         "palette": [COARSE_DIRT, GRAVEL]}), (2, GRAVEL))},
                {"thickness": 14, "material": depth_stack(
                    (1, {"kind": "cell", "seed": 19, "cellSize": 5, "jitter": 50, "warp": 2,
                         "palette": [GRAVEL, STONE]}), (2, GRAVEL))},
                {"thickness": 70, "material": depth_stack((2, STONE), (2, COBBLE))},
            ]}}


THEMES = {
    "moor": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        # no rim: this ground is relief-solved, and a rim caps every fall with a band and
        # turns a rolling fell into contour lines
        "rim": {"enabled": False, "depth": 1, "material": COARSE_DIRT},
        "surface": {"enabled": True, "depth": 3, "material": moor_surface()},
        # a cut face is a soil profile, which is what a bank sliced by a gill looks like
        "wall": depth_stack((1, COARSE_DIRT), (2, DIRT), (3, GRAVEL)),
        "wallEnabled": True,
        "fill": body(),
    },
    "floor": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        # the made ground DOES want a rim: its edge is a built lip, not a hillside
        "rim": {"enabled": True, "depth": 1, "material": STONE_BRICK},
        "surface": {"enabled": True, "depth": 3, "material": depth_stack(
            (1, {"kind": "cell", "seed": 9, "cellSize": 6, "jitter": 25, "warp": 1,
                 "palette": [COBBLE, STONE_BRICK]}), (2, GRAVEL))},
        # a retaining wall is the one surface on a board that wants a wallRun: the courses
        # stripe along the perimeter instead of being sampled from the plane
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONE_BRICK, "width": 1},
            {"material": COBBLE, "width": 2},
            {"material": ANDESITE, "width": 1},
            {"material": COBBLE, "width": 3},
        ]},
        "wallEnabled": True,
        "fill": body(),
    },
    "hush": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
        "surface": {"enabled": True, "depth": 3, "material": hush_surface()},
        "wall": depth_stack((2, GRAVEL), (3, STONE)),
        "wallEnabled": True,
        "fill": body(),
    },
}

# The made ground is stated flat and taken out of the solve; the grown ground is left in it.
SHAPE_PROPS_BY_HEIGHT = {
    "18": {"relief_scope": "exclude"},
    "19": {"relief_scope": "exclude"},
}

# The wash and the shoal are the same scoured ground at the two ends of the fall.
THEME_BY_HEIGHT = {"12": "hush", "13": "hush", "18": "floor", "19": "floor"}

# The bing is spoil rather than floor — it is what came out of the shaft, not something laid.
THEME_BY_ID = {"bing-18": "hush"}

RELIEF = {
    "team": {
        "base": 16,
        "reach": 24,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 13, "seed": 7},
        "marks": [
            # the shore the crossing lands on, six under the yard it is cut out of — which
            # is what puts the bank at an angle instead of at a gradient
            {"id": "wash", "kind": "area", "h": 11, "bevel": 2,
             "ring": [[-20, 16], [20, 16], [20, 30], [-20, 30]]},
            # the knoll on the bank's east end — the one high stand over the long hop
            {"id": "knowe", "kind": "point", "at": [25, 37], "r": 9, "h": 18},
            # the hush itself: a gully torn down the bank, flat-bottomed for two cells
            # either side of its course and lofted out to the ground beside it
            {"id": "scar", "kind": "line", "r": 6, "tread": 2,
             "points": [[-13, 47], [-11, 36], [-9, 26]], "h": [16, 13, 11]},
            # the yard round the shaft: worked ground, level to fight on but not laid, so
            # it is stated as a mark rather than taken out of the solve
            {"id": "yard", "kind": "area", "h": 17, "bevel": 2,
             "ring": [[-16, 44], [38, 44], [38, 78], [-16, 78]]},
            # the fell swelling over the west spur, so the powder house sits in its lee
            {"id": "spurhead", "kind": "point", "at": [-34, 68], "r": 11, "h": 18},
        ],
        "pushes": [
            # the bank's own shoulder over the gill, added to the solved surface
            {"id": "brow", "amount": 2, "falloff": 12, "roughness": 2, "crown": 1, "seed": 5,
             "ring": [[-12, 32], [20, 32], [20, 44], [-12, 44]]},
        ],
    },
    "neutral": {
        "base": 12,
        "reach": 7,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 7, "seed": 11},
        # the spoil the water carried down, heaped at the elbow of the bank: a crown to
        # hold, with the two legs falling away from it to the water
        "marks": [{"id": "heap", "kind": "point", "at": [0, 0], "r": 5, "h": 15},
                  {"id": "tail-w", "kind": "point", "at": [-13, 5], "r": 4, "h": 12},
                  {"id": "tail-e", "kind": "point", "at": [13, -5], "r": 4, "h": 12}],
        "pushes": [],
    },
}

STAIR = {"kind": "cell", "seed": 31, "cellSize": 4, "jitter": 30, "warp": 1, "rise": 3,
         "palette": [COBBLE, STONE_BRICK]}
LAUNDER = {"kind": "cell", "seed": 41, "cellSize": 5, "jitter": 40, "warp": 2, "rise": 3,
           "palette": [GRAVEL, ANDESITE]}


def flight(shape_id, x0, x1, foot, head, z_foot, z_head):
    """One cut in the dressing floor's face. A flight is a made thing, so it takes a
    material rather than a theme and the same one the whole way up; level with anchors at
    the foot and the head is what states the face instead of grading it away."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "override": True,
            "keepClear": True, "floor": 0, "base_height": head, "material": STAIR,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x0, z_foot], [x1, z_foot], [x1, z_head], [x0, z_head]],
            "anchor_heights": [foot, foot, head, head]}


def brush(shape_id, theme, vertices):
    """A patch of a theme on ground that is already there. It has to declare a height_mode
    or ShapeScopeOwners never makes it a candidate and it paints nothing in silence; raise
    with no height sits flush at the median under its own footprint, so it is drawn small
    and on ground that is close to level."""
    return {"id": shape_id, "type": "polygon", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "theme": theme, "vertices": vertices}


ADD_SHAPES = [
    # the two cut tracks up the fell. The shore track is the one that earns its place: the
    # ground it replaces climbs off the landing in two-block scrambles at (8, 21) and
    # (8, 31), measured on a transect, and a flight is what states that rise instead.
    # Fourteen of run for six of rise, which is over twice the rise the ruling asks for.
    flight("flight-shore", 3, 11, 11, 17, 20, 34),
    flight("flight-bank", -6, 2, 14, 18, 33, 48),
    # the launder that fed the hush, laid into the mine head's floor — four points, which
    # the rasterizer splines before it offsets the band, so it draws as a curve. It shares
    # the head's own exclusion, or the relief solves a surface straight through it (SK14)
    {"id": "launder", "type": "polyline", "operation": "add", "override": True,
     "base_height": 18, "floor": 0, "stroke_edge": "solid", "material": LAUNDER,
     "relief_scope": "exclude",
     "vertices": [[-14, 88], [-2, 82], [10, 87], [22, 81]], "radius": 2},
    # the tramway from the gate to the assay house door, on the lane behind the wall
    {"id": "tramway", "type": "polyline", "operation": "add", "override": True,
     "base_height": 18, "floor": 0, "stroke_edge": "solid", "material": LAUNDER,
     "relief_scope": "exclude",
     "vertices": [[38, 70], [44, 65], [50, 70]], "radius": 2},
    # what the water left when it was let go. These are drawn to CROSS the risers rather
    # than to sit inside a plateau, so the paint boundary is not the height boundary: the
    # scar runs off the yard, down the bank and onto the shore as one patch of ground.
    brush("spill-head", "hush", [[-16, 46], [-7, 47], [-4, 56], [-11, 60], [-16, 58]]),
    brush("spill-yard", "hush", [[22, 62], [34, 64], [32, 74], [22, 73]]),
    brush("scar-foot", "hush", [[-16, 22], [-6, 25], [-4, 34], [-15, 33]]),
    # and turf coming the other way, down onto the shore where nothing scoured it — the
    # scoured half of the shore is the west, and the east half kept its ground
    brush("shore-turf", "moor", [[0, 21], [15, 21], [15, 31], [0, 30]]),
]

# ── what stands on it ─────────────────────────────────────────────────────────────────────
#
# Two buildings, one style, different footprints: the whim house over the shaft at the mine
# head and the powder house out on the west spur. A board that already stands a spawn hall
# and two wool rooms does not want five more. Everything else is placed because there is an
# answer to *why here*: the trees are in the lee behind the head and on the spur's north
# edge where the wind is off them, and the rocks are on the knoll the relief raised.

DRESSING = {
    "styles": {
        "birk":  {"kind": "tree", "form": "template", "species": "birch", "height": 7},
        "fir":   {"kind": "tree", "form": "template", "species": "spruce", "height": 9},
        "erratic": {"kind": "boulder", "form": "angular", "size": 3,
                    "rock": {"kind": "cell", "seed": 61, "cellSize": 3, "jitter": 40,
                             "rise": 3, "palette": [STONE, ANDESITE]}, "mossy": True},
        "erratic-round": {"kind": "boulder", "form": "round", "size": 2.5,
                          "rock": {"kind": "cell", "seed": 62, "cellSize": 3, "jitter": 40,
                                   "rise": 3, "palette": [STONE, COBBLE]}, "mossy": True},
    },
    "props": [
        # ground cover over the whole of the grown ground rather than in patches — the
        # patchiness is the density field's job and it is better at it than a polygon
        {"id": "fell-cover", "kind": "flora", "seed": 90,
         "spec": {"coverage": 0.34, "scale": 14, "octaves": 3, "fernShare": 0.32,
                  "flowerShare": 0.05, "flowerScale": 18, "tallShare": 0.05},
         "points": [[-56, 58], [-56, 78], [-14, 78], [38, 78], [38, 44], [34, 26],
                    [-18, 26], [-18, 58]]},
        # the way up off the crossing and out to each room, drawn so the ground along it
        # stays clean; three blocks a reader cannot quite tell apart, on hard ground
        {"id": "road-spine", "kind": "stroke", "seed": 3, "claimsGround": True,
         "points": [[6, 22], [9, 38], [4, 54], [1, 70], [0, 86]], "radius": 2,
         "style": "solid",
         "pave": {"kind": "cell", "seed": 13, "cellSize": 4, "jitter": 40, "warp": 2,
                  "palette": [GRAVEL, ANDESITE, COBBLE]}},
        {"id": "road-west", "kind": "stroke", "seed": 4, "claimsGround": True,
         "points": [[-8, 66], [-24, 70], [-40, 68]], "radius": 2, "style": "solid",
         "pave": {"kind": "cell", "seed": 14, "cellSize": 4, "jitter": 40, "warp": 2,
                  "palette": [GRAVEL, ANDESITE, COBBLE]}},
        # the whim house stands over the shaft at the head, facing the yard it worked
        {"id": "head-store", "kind": "house", "seed": 101, "style": "@hw-minehouse", "front": "negZ",
         "wings": [{"corners": [[17, 85], [23, 91]]}]},
        # the powder house, out on the spur away from everything, as a powder house is
        {"id": "powder", "kind": "house", "seed": 102, "style": "@hw-minehouse", "front": "posZ",
         "wings": [{"corners": [[-31, 60], [-25, 64]]}]},
        # a clump in the lee of the spur's north edge, off the road by more than a canopy
        {"id": "birk-1", "kind": "tree", "style": "birk", "x": -34, "z": 75},
        {"id": "birk-2", "kind": "tree", "style": "fir",  "x": -29, "z": 74},
        {"id": "birk-3", "kind": "tree", "style": "birk", "x": -24, "z": 75},
        {"id": "birk-4", "kind": "tree", "style": "fir",  "x": -19, "z": 74},
        {"id": "birk-5", "kind": "tree", "style": "birk", "x": -13, "z": 62},
        # and rocks on the knoll the relief raised at the bank's east end
        {"id": "rock-1", "kind": "boulder", "style": "erratic", "x": 24, "z": 30},
        {"id": "rock-2", "kind": "boulder", "style": "erratic-round", "x": 28, "z": 42},
        {"id": "rock-3", "kind": "boulder", "style": "erratic", "x": -36, "z": 62},
    ],
}



def adapt(plan):
    plan["meta"] = {"name": NAME}
    plan["globals"]["surface"] = 12
    pieces = []
    for entry in PIECES:
        piece = {"id": entry[0], "role": entry[1], "rect": entry[2], "surface": entry[3]}
        if len(entry) > 4:
            piece["mirrors"] = entry[4]
        pieces.append(piece)
    plan["pieces"] = pieces
    plan["zones"] = [{"id": i, "rect": r, "holes": []} for i, r in ZONES]
    plan["walls"] = [{"a": a, "b": b} for a, b in WALLS]
    plan["placements"] = PLACEMENTS
    plan["boxes"] = [{"id": i, "kind": k, "rect": r, "members": m} for i, k, r, m in BOXES]
    return plan


def finish_document():
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-18",
        "voidEnforcement": True,
        "mapTheme": "moor",
        "themes": THEMES,
        "themeByHeight": THEME_BY_HEIGHT,
        "themeById": THEME_BY_ID,
        "shapePropsByHeight": SHAPE_PROPS_BY_HEIGHT,
        "relief": RELIEF,
        "addShapes": ADD_SHAPES,
        "dressing": DRESSING,
        "roomStyles": {"spawn": "@hw-minehouse", "wool": "@hw-assay"},
        # the fell's own green: Extreme hills tints grass #8ab689, a grey-green that agrees
        # with the stone beside it where Plains' #91bd59 would read as a lawn on a moor
        "biome": {"kind": "solid", "biome": 3},
    }


def main():
    print(f"studio at {API}")
    plan, card = composed()
    before = {"score": card["score"], "structure": card["structure"], "spend": card["spend"],
              "topSoft": card["topSoft"], "descriptor": card["descriptor"],
              "pieces": len(plan["pieces"]), "zones": len(plan["zones"]),
              "walls": len(plan["walls"])}
    print(f"  composed  score {card['score']:.3f}  hub {card['structure']['hub']}  "
          f"front {card['structure']['frontline']}  wools {','.join(card['structure']['wools'])}  "
          f"land {card['spend']['unit']['cells']}/{card['spend']['unit']['budgetCells']:.0f}  "
          f"mid {card['spend']['mid']['cells']}")
    json.dump(before, open(os.path.join(HERE, "composed.json"), "w"), indent=1)

    plan = adapt(plan)
    json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    json.dump(finish_document(), open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
    print(f"  adapted   pieces {len(plan['pieces'])}  zones {len(plan['zones'])}  "
          f"walls {len(plan['walls'])}  themes {len(THEMES)}  "
          f"marks {sum(len(g['marks']) for g in RELIEF.values())}  shapes {len(ADD_SHAPES)}")


if __name__ == "__main__":
    main()
