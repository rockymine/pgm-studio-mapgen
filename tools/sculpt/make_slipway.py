"""Write the spec for Slipway — a harbour DTM with a ship, two balloons and a dockside crane — for
`drive.py` to build.

The board exists to put the made-thing machinery on a map that is actually played rather than on a gallery
deck. Three things are stated three different ways, and the difference is the point:

- the **ship** floats, so it states an absolute floor at the load line and no seat;
- the **balloons** fly, so they state an absolute floor and no seat either;
- the **crane** stands on the dock, so it states `seat: "ground"` and settles onto it, one drop for all four
  of its layers. It faces the water and its load hangs out over the harbour.

**A settlement is a pad, then roads, then houses — in that order.** The dock and the upland are plan pieces
at their own surface whose compiled shapes are marked `relief_scope: "exclude"`, so the relaxation bends
around them and each is a flat terrace rather than a slope with buildings sliding down it. The roads are
drawn onto those pads and the houses are placed clear of them.

**A layer holds a stair as well as a sculpture, because both are a thickness over a stated base.** The port
is walled on two sides by the grounds above it, so `port-stairs` sits at the port's own surface and carries
a flight per face — a polygon whose corners state a course at the foot and the face's own at the head,
which the rasterizer interpolates into treads.

**The two settlements a team has are not each other's mirror.** One is on the dock at the water; the other is
cut back into the hill behind the town. Only the board is symmetric.

**The board's size is the goal rules.** `GO4` holds a destroy goal 40–90 blocks from its own spawn by walk
and `GO1` holds the enemy walk at 3–4 times that; `GO3` then holds opposing goals to 85–150 and `GO2` a
team's own pair to 35–65. Solved together they give a board 256 x 256. The **dock goal is deliberately
outside** GO1 and GO4 — a goal at the water is a forward objective and the bands are written for two goals in
the defender's rear — and `review/opus5-slipway.md` carries what it measures.

    python3 tools/sculpt/make_slipway.py specs/opus5-slipway
    python3 tools/drive.py specs/opus5-slipway "Slipway" --out /tmp/slipway
"""
import json
import math
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import board
import models
from layers import compile_layers, stats

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")

CELL = 4
# Surfaces, in blocks. Every step between neighbouring pieces is a multiple of two (`EL1`).
BASIN, WATER, DOCK, QUAY, PORT, TOWN, HEAD, RIDGE, BACK = 6, 16, 20, 22, 22, 24, 26, 28, 30

# The Y a balloon's basket floor is stated at. A balloon is a made thing that flies, so its height is
# authored rather than seated, and this one rides well clear of the roofs on the field it flies off — the
# steading below the western envelope tops at y42. It costs the board no build ceiling: a made thing is not
# what the ceiling clears.
FLYING = HEAD + 22

PLAN = {
    "plan": 1,
    "meta": {"name": "Slipway"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 28, "surface": QUAY,
                "observerY": 100},
    # The author's own composition, sketched on a phone and scaled up here: a harbour with the ship on it,
    # a crane dock west of centre, the first goal's dock at the middle, a port east, the dockside settlement
    # behind the west dock and a second settlement back and to the east with the other goal in front of it —
    # and a field on each arm for a balloon to stand over. `LN2` caps a lane at 110 blocks and rects sharing
    # a cross-axis interval merge into one lane however many pieces they are written as.
    #
    # **Ground that reads as nothing is not drawn.** A piece behind the port stood a thousand columns at one
    # height with no route across it, no relief mark over it and nothing built on it — a flat pad the eye
    # takes for unfinished map. Its corner is now the board's, and the outline draws it.
    "pieces": [
        {"id": "basin",           "role": "piece", "rect": [-13, -4, 26,  8], "surface": BASIN},
        {"id": "balloon-field",   "role": "piece", "rect": [-25, -4, 12, 11], "surface": HEAD},
        {"id": "crane-dock",      "role": "piece", "rect": [-13,  4,  6,  5], "surface": DOCK},
        {"id": "goal-dock",       "role": "piece", "rect": [ -7,  4,  7,  7], "surface": DOCK},
        {"id": "quay-e",          "role": "piece", "rect": [  0,  4, 11,  7], "surface": QUAY},
        {"id": "port",            "role": "piece", "rect": [ 11,  4, 14, 10], "surface": PORT},
        {"id": "dock-town",       "role": "piece", "rect": [-18,  7,  5,  7], "surface": TOWN},
        {"id": "dock-yard",       "role": "piece", "rect": [-13,  9,  6,  5], "surface": TOWN},
        {"id": "mid",             "role": "piece", "rect": [ -7, 11, 18,  3], "surface": TOWN},
        {"id": "back-settlement", "role": "piece", "rect": [  7, 14, 11, 10], "surface": BACK},
        {"id": "hill",            "role": "piece", "rect": [-18, 14, 25,  9], "surface": RIDGE},
        {"id": "fore-spawn",      "role": "piece", "rect": [ -7, 23, 14,  5], "surface": RIDGE},
        {"id": "back-band",       "role": "piece", "rect": [  7, 24, 11,  4], "surface": RIDGE},
        {"id": "spawn",           "role": "spawn", "rect": [ -3, 28,  5,  5], "surface": BACK},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [2.5, 2.5], "facing": "down"}],
        # Outside the spawn room and beside its door lane rather than in it: a player leaving for the front
        # passes the iron instead of walking into it. `ST2` complains that it is off the spawn piece, which
        # is the author's call — a stamped spawn has a doorway, and a chest in a doorway is in the way.
        "iron":   [{"id": "iron-1", "piece": "fore-spawn", "at": [11.0, 2.0]}],
        # One goal on the dock beside the crane and one at the corner of the port's car park, which is the
        # author's own composition: the two a team defends stand at opposite corners of its ground rather
        # than side by side, and each is named for what it stands at. The dock goal is a FORWARD objective and reads outside `GO1`/`GO4`, and its own mirror is
        # under `GO3` — the bands are written for two goals in a defender's rear, and this board is the
        # measurement that says what a forward one costs. `review/opus5-slipway.md` carries the numbers.
        "destroyables": [
            {"id": "destroyable-1", "style": "pillar-2", "at": [-6.0, 6.5], "materials": "obsidian",
             "float": 2, "name": "Crane"},
            {"id": "destroyable-2", "style": "pillar-2", "at": [10.75, 11.5], "materials": "obsidian",
             "float": 2, "name": "Car Park"},
        ],
    },
}


def style(name):
    """One of the author's own ground patterns, by the name it was saved under. Fetched rather than
    transcribed: a copy here would be free to disagree with the library the studio paints from."""
    with urllib.request.urlopen(f"{API}/styles?limit=400") as answer:
        rows = json.load(answer)
    for row in rows:
        if row.get("name") == name:
            return json.loads(row["params"])
    raise SystemExit(f"no style named {name!r} in the library")


def ground(surface, wall, rim=None, fill=None):
    """A theme with a **face**: a one-course surface, a wall down every exposed riser, and optionally a rim
    capping the plateau boundaries. What built ground wants — a quay is masonry with a kerb along its edge
    and a cut face where it drops to the water, and the seabed's shelf is a face too.

    The materials are the author's own library patterns rather than four blocks, so binding one to a bucket
    is the whole of using them. The surface is one course: `all green` and `all sand` are picks, and a pick
    two courses deep is soil surfaced twice over, which `PT1` refuses."""
    theme = {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "rim": {"enabled": rim is not None, "depth": 1,
                "material": rim or {"kind": "solid", "id": 1, "data": 0}},
        "surface": {"enabled": True, "depth": 1, "material": surface},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill or wall,
    }
    if rim is not None: theme["rimEdges"] = "boundary"
    return theme


def layers(*courses):
    """A theme that is nothing but a stack of courses, read down from the surface — `(pattern, thickness)`
    top first, the last one repeating to the bedrock however deep the ground is.

    **A landform has courses; it does not have a face.** With no rim, no surface bucket and no wall the
    painter leaves one `Fill` band spanning the whole column over the bedrock, and a `layered` material on
    the depth axis is then the courses themselves — depth 0 is the top block. A wall is the other model: it
    paints the exposed riser in one material, which draws every drop as a cut face and every plateau
    boundary as a line, and a hillside is neither. Stated this way the ground reads as what it is made of
    all the way down, and a cut through it shows soil over subsoil over rock rather than a rind."""
    bands = [{"material": material, "thickness": thickness} for material, thickness in courses]
    stone = {"kind": "solid", "id": 1, "data": 0}
    return {
        "bedrock": {"relative": False, "value": 1},
        "rim": {"enabled": False, "depth": 1, "material": stone},
        "surface": {"enabled": False, "depth": 1, "material": stone},
        "wall": stone,
        "wallEnabled": False,
        "wallOnTerrainFaces": False,
        "fill": {"kind": "layered", "axis": "depth", "stack": {"bands": bands, "ending": "repeat"}},
    }


def turn(model, quarter):
    """A model rotated a quarter turn at a time about its own origin, in the plan axes."""
    def spun(x, y, z):
        for _ in range(quarter % 4):
            x, z = -z, x
        return x, y, z
    return {spun(x, y, z): material for (x, y, z), material in model.items()}


def place(model, at, quarter=0):
    dx, dy, dz = at
    return {(x + dx, y + dy, z + dz): material for (x, y, z), material in turn(model, quarter).items()}


def made(name, voxels, seat=None):
    """A model compiled to layers, in the shape `addLayers` takes. `kind`, `part_of` and `seat` ride with it."""
    layers = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L", group_name=name,
                            part_of=name, seat=seat)
    return [{"id": layer["id"], "name": layer["name"], "base_y": 0, "kind": layer["kind"],
             "part_of": layer["part_of"], **({"seat": layer["seat"]} if "seat" in layer else {}),
             "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
            for layer in layers], stats(voxels, layers)


def sculpted():
    add_layers, table = [], []

    # The ship lies athwart the basin so both shores see the same broadside, and floats: her load strake sits
    # at the water line and her keel clears the basin floor.
    ship = place(models.ship(), (-5, WATER - 8, 0), quarter=1)
    layers, row = made("ship", ship)
    add_layers += layers
    table.append(("ship", row))

    # A balloon flying over each arm's own field. Two rather than one because a single one on a rot_180
    # board is the one thing on it that is not answered across the axis.
    for name, at in [("balloon-w", (-78, FLYING, -8)), ("balloon-e", (78, FLYING, 8))]:
        layers, row = made(name, place(models.balloon(), at))
        add_layers += layers
        table.append((name, row))

    # The crane stands on its own dock at the water's edge, unturned, so its shear legs rake out over the
    # harbour and the load on its chain hangs past the quay — the whole reason a crane is on a quay. Seated:
    # the sill and feet find the pad's top, and the jib is free to reach over water they never touch.
    for name, at, quarter in [("crane-w", (-40, DOCK, 18), 0), ("crane-e", (40, DOCK, -18), 2)]:
        layers, row = made(name, place(models.crane(), at, quarter), seat="ground")
        add_layers += layers
        table.append((name, row))

    # **A sky over the board.** A board with a balloon flying over it wants something else in the air, or the
    # balloon reads as the one thing that got away. Three puffs, each answered across the axis, riding at the
    # altitude the balloons' own shoulders do — `CLOUD_BASE` is the underside, and a cumulus is eight blocks
    # deep, so they sit inside the y75-102 the envelopes occupy.
    #
    # **A cloud costs the board nothing it has.** It is the one made thing nobody can reach: the build
    # ceiling clears the terrain and the buildings and stops at 68, and these fly from 78, so no player
    # stands on one or builds to one. It takes no ground, seats on nothing, and in layers it is the cheapest
    # thing here — a solid blob is one run per column, so one layer apiece against the balloon's eight.
    #
    # **A cloud stands off a goal's marker.** The marker is a sky sign — a player crossing open ground reads
    # where the goal is from it — and it hangs five over the build ceiling, which is exactly the air a cloud
    # wants. The first placement put one three blocks over both of them.
    for index, (name, at) in enumerate([("cloud-mid", (0, 78, -60)),
                                        ("cloud-back", (35, 84, 70)),
                                        ("cloud-town", (-70, 80, 40))]):
        for side, (px, pz) in enumerate([(at[0], at[2]), (-at[0], -at[2])]):
            layers, row = made(f"{name}-{side}", place(models.cumulus(index), (px, at[1], pz)))
            add_layers += layers
            if side == 0:
                table.append((name, row))

    # A car park on the port, four cars a side. At nine blocks a car is four boxes and four cubes, which is
    # the other end of the scale from the ship — and what makes the port read as somewhere goods leave from.
    #
    # **A car states its floor rather than seating on the ground.** A seat lands a thing's lowest course on
    # the ground's own top block, which is right for a building whose foundation cuts into the surface and
    # wrong for a wheel: the car reads sunk a course into the tarmac. The port is one flat terrace under all
    # eight of them, so the floor the model was drawn at IS the floor it wants.
    for index, (x, z, quarter, back) in enumerate([(58, 26, 0, True), (70, 26, 0, False),
                                                   (58, 40, 2, True), (70, 40, 2, False)]):
        for side, (px, pz, turn_) in enumerate([(x, z, quarter), (-x, -z, (quarter + 2) % 4)]):
            name = f"car-{index}-{side}"
            layers, row = made(name, place(models.minicar(cabin_back=back), (px, PORT, pz), turn_))
            add_layers += layers
            if side == 0:
                table.append((name, row))

    return add_layers, table


# ── the settlements: a pad, then roads, then houses ───────────────────────────────────────────────────────

ROADS = [
    # The waterfront's back lane, from the goal dock east past the port. It starts where the crane dock ends
    # — a road through a crane's sill is a road broken by it — and runs along the **back** of the quay, which
    # leaves the eighteen blocks between it and the water as working ground rather than a verge.
    {"id": "quay-road", "kind": "path", "seed": 3, "route": True, "radius": 3, "coverage": 0.95,
     "points": [[-24, 38], [4, 40], [30, 38], [58, 34], [92, 32]],
     "pave": {"kind": "solid", "id": 98, "data": 0}},
    # Behind the crane, along the back of the dock and into the town: the lane a load leaves the quay by.
    {"id": "dock-road", "kind": "path", "seed": 8, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-66, 40], [-44, 40], [-30, 42], [-18, 44]],
     "pave": {"kind": "solid", "id": 98, "data": 0}},
    # Up out of the dock, round the terrace row's western end and along the foot of the hill. It leaves the
    # dock town uncrossed on purpose: a twenty-block strip with a road down it holds no house, and the row
    # across the middle is the one thing joining the two towns.
    {"id": "town-road", "kind": "path", "seed": 4, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-18, 44], [-26, 54], [-32, 62], [-20, 66], [2, 70]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
    # The lane to the back settlement, past the goal that stands in front of it.
    {"id": "back-road", "kind": "path", "seed": 5, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-20, 66], [10, 64], [34, 70], [48, 82], [54, 92]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
    # And up over the hill to the spawn.
    {"id": "spawn-road", "kind": "path", "seed": 6, "route": True, "radius": 3, "coverage": 0.9,
     "points": [[-20, 66], [-22, 84], [-10, 98], [0, 114]],
     "pave": {"kind": "solid", "id": 4, "data": 0}},
]

# `(id, style, low corner, high corner, front)`. Footprints are inclusive of both corners and capped at 192
# blocks (`HP3`); they are laid **1.5:2 rather than square**, staggered in depth so a street is not a row of
# identical boxes, and turned four different ways — a rectangle with its door on the short end reads
# differently from the same rectangle with its door on the long one, and every house facing one way is a
# shed row rather than a town.
#
# **Four styles, and the ground decides which two a house may take.** Eleven styles over sixteen plots is a
# catalogue rather than a town: nothing recurs, so nothing reads as belonging anywhere. Each ground now
# carries a pair, and a pair is enough — two roofs alternating down a street is a settlement, one is a
# terrace and four is a sample book.
#
# | ground | the two it takes |
# |---|---|
# | the meadow — town, terrace row, hill, settlements | `@17h-hall` red-brick gable · `@sb-spawn` stone gable |
# | the quay and the port, where the cars stand | `@17h-hall` red-brick gable · `@sn-compass-well` diorite and blue clay |
# | the dock and the terracotta fields | `@hoar-longhall` white gable · `@sb-spawn` stone gable |
#
# The footprints are untouched: a plot is a position the board's ground was searched for, and a style change
# is not a reason to re-search one.
#
# **Every plot is a position the board's own ground was searched for**: the `ground` layer carries every
# column of the plot and a two-block ring, the rise across that stays under the building's own height
# (`DR-SLOPE`), it clears the roads (`DR-CROSS`), it clears every other plot's claim (`DR-CLAIM`) and it
# stands outside the +-10-block square a destroy goal keeps clear (`DressingScope.GoalStandoff`, `OB19`).
HOUSES = [
    # The dock town, on the meadow: the sailmaker and the cooperage in the yard behind the crane.
    ("sailmaker",      "@sb-spawn",        ( -69,  45), ( -60,  57), "posZ"),
    ("cooperage",      "@17h-hall",        ( -53,  46), ( -42,  55), "negX"),
    # The quay east of the goal dock: a harbour office at the water, and a store along from it.
    ("harbour-office", "@sn-compass-well", (   5,  19), (  16,  32), "negZ"),
    ("quay-store",     "@17h-hall",        (  35,  21), (  44,  29), "posX"),
    # The row across the middle, which is the one thing joining the two towns.
    ("arcade-w",       "@sb-spawn",        ( -12,  46), (   2,  53), "negZ"),
    ("arcade-e",       "@17h-hall",        (  16,  46), (  30,  53), "posZ"),
    # The upland: a barn on the hill's own shoulder, and the back settlement flattened into it.
    ("granary",        "@17h-hall",        ( -40,  75), ( -29,  86), "negX"),
    ("counting",       "@sb-spawn",        (  28,  82), (  37,  91), "posZ"),
    ("upland-hall",    "@17h-hall",        (  55,  66), (  66,  80), "posX"),
    # The field the balloon flies off, which the drawn coast made room on: five, so it reads as somewhere
    # rather than as the ground beside somewhere.
    ("balloon-shed",   "@hoar-longhall",   ( -81,  18), ( -69,  27), "posZ"),
    ("balloon-store",  "@sb-spawn",        ( -64,  20), ( -55,  28), "negZ"),
    ("field-cottage",  "@hoar-longhall",   ( -94,  13), ( -86,  24), "posX"),
    ("field-barn",     "@sb-spawn",        (-103, -13), ( -92,  -1), "posZ"),
    ("field-byre",     "@hoar-longhall",   ( -79,  -8), ( -69,   1), "negX"),
    # The port, beside the car park.
    ("warehouse",      "@sn-compass-well", (  99,  18), ( 110,  32), "posZ"),
    ("port-office",    "@17h-hall",        (  90,  39), (  99,  50), "posX"),
]


# `(x, z, species, height)`. The field the balloon flies off, the hill behind the town, the back
# settlement's own green — and then the wood on the upland the spawn stands in.
#
# **The upland is the one ground on this board a player crosses on foot the whole way.** It is grass from
# the spawn's own door to the settlements, and bare grass at that width reads as a field to walk over
# rather than as somewhere. The wood is oak and birch at eight to eleven blocks, which is the stock the
# rest of the board already carries, and it is laid to three rules: it stands on the meadow shape and
# nowhere else, it leaves the ground in front of the spawn door open, and it thickens and thins rather
# than standing at one pitch — a crown's own radius plus a gap that runs between one block and six, so the
# upland carries groves and glades instead of an orchard.
#
# Every trunk is a position the board's own ground was searched for: the meadow under its whole crown, a
# rise under it below six, four blocks off a route's claim (`DR-ROAD` asks three), its crown clear of every
# building's claim, of every other crown and of the objectives' standoff (`OB19`). A tree is RNG-free, so
# a crown's reach is a function of its species and height and can be measured before any world exists.
TREES = [
    # The balloon's field, the hill and the back green.
    ( -63, -12, "oak", 9),   ( -86,   0, "birch", 10), ( -78,   8, "spruce", 11),
    ( -94,   5, "oak", 12),  (  11,  73, "birch", 9),  ( -13,  76, "oak", 10),
    (  -5,  90, "birch", 11), (   0,  79, "spruce", 12), (  21,  77, "oak", 9),
    (  62,  90, "birch", 10), (  32,  60, "oak", 11),  (  40,  63, "birch", 12),
    # The upland wood, west of the spawn's approach and east of it.
    ( -20,  58, "birch", 9), ( -10,  58, "oak", 8), (  18,  58, "oak", 9),
    ( -80,  60, "oak", 9), ( -47,  61, "birch", 11), ( -39,  61, "oak", 9),
    ( -62,  63, "birch", 9), ( -56,  64, "birch", 9), ( -70,  65, "oak", 8),
    ( -64,  69, "oak", 8), ( -54,  70, "birch", 8), ( -39,  70, "birch", 8),
    ( -31,  70, "birch", 10), ( -48,  71, "birch", 10), ( -76,  73, "birch", 10),
    ( -70,  75, "birch", 9), (  -6,  75, "birch", 9), ( -64,  77, "oak", 8),
    ( -53,  79, "birch", 10), ( -46,  80, "oak", 9), (  10,  82, "oak", 9),
    ( -72,  83, "birch", 11), ( -61,  83, "oak", 9), ( -12,  84, "oak", 8),
    (  19,  84, "oak", 9), (   1,  87, "birch", 8), ( -47,  88, "oak", 9),
    ( -63,  91, "birch", 9), ( -27,  91, "birch", 10), ( -55,  92, "oak", 8),
    ( -38,  96, "birch", 11), (  29,  98, "birch", 11), (  40,  98, "oak", 10),
    (  73,  98, "birch", 8), (  82,  99, "birch", 8), (  61, 102, "oak", 10),
    (  51, 104, "oak", 8), ( -29, 105, "birch", 8), (  27, 107, "oak", 9),
    (  72, 107, "oak", 8), (  42, 108, "oak", 9), (  34, 109, "birch", 9),
]


def houses():
    return [{"id": name, "kind": "house", "seed": 40 + index, "front": front,
             "points": [list(low), list(high)], "style": style_name}
            for index, (name, style_name, low, high, front) in enumerate(HOUSES)]


def trees():
    return [{"id": f"tree-{index}", "kind": "tree", "seed": 200 + index, "x": x, "z": z,
             "form": "template", "species": species, "height": height}
            for index, (x, z, species, height) in enumerate(TREES)]


def crates():
    """Cargo on the dock and under the balloon: boulders in a timber material read as bales and crates at
    this scale, and they are the one prop that takes a rock of its own."""
    timber = {"kind": "cell", "seed": 3, "cellSize": 3, "jitter": 40, "warp": 2,
              "palette": [{"kind": "solid", "id": 5, "data": 1}, {"kind": "solid", "id": 5, "data": 5},
                          {"kind": "solid", "id": 17, "data": 1}]}
    # Searched for like every other plot: clear of the crane's own ground, off the roads and outside the
    # dock goal's +-10 square, which a boulder standing in is `OB19`.
    at = [(-9, 29), (-10, 21), (-2, 21), (27, 28), (28, 20)]
    return [{"id": f"crate-{index}", "kind": "boulder", "seed": 500 + index, "x": x, "z": z,
             "form": "angular", "size": 1.4 + 0.3 * (index % 3), "mossy": False, "rock": timber}
            for index, (x, z) in enumerate(at)]


# ── the stairs the port is reached by ─────────────────────────────────────────────────────────────────────

# Two faces stand over the port and neither can be climbed: the terracotta field the balloon flies off,
# along the water side, and the settlement the spawn road comes down from, along the back. Seven blocks and
# eight of bedrock wall, which is a player walking the length of the port looking for a way up.
#
# **A stair is a thickness over the ground it is laid on, so it is one layer and not a shape apiece.** The
# layer states the port's own surface as its base and every shape on it is a height above that — which is
# what lets a flight be stated as one polygon: the corners at the foot carry a course and the corners at
# the head carry the face's own, and the rasterizer interpolates across the footprint and rounds per cell,
# which is a staircase. The anchors sit half a course either side of those numbers so that every cell
# centre lands on a whole course rather than on a tie between two.
#
# **And it climbs ALONG the face rather than into it.** A flight cut square into a wall puts a player at
# the top still walking the way they climbed, and what is at the top here is a car park on one side and a
# street on the other. Turned ninety degrees the climb ends on a landing level with the ground above, and
# that ground is a step to the side — which is how a quay stair is built and why it is five blocks deep
# rather than the width of the thing it serves.
#
# One statement, two of everything: the group mirrors, so each flight is answered at the far arm's own face.
STAIR_DEEP = 5      # across a flight — a stair rather than a ramp
STAIR_LAND = 5      # along the landing at its head
# `(name, the face in blocks, the flight's FOOT, which way it climbs, what its landing is paved as)`. The
# port floors at 21, the terracotta field tops at 28 and the settlement at 29, so the two rises are the two
# differences.
#
# **The back face carries a pair, and the second is the first turned about.** One flight is a way up; two
# climbing away from each other is a choice of which way to go up. **The two flights face each other and the
# landings go to the ends**: a landing is a solid block the full height of the face, so a pair of them in the
# middle reads as two towers standing off the wall, while at the ends they read as the wall — and what a
# player walking the port then meets in the middle is stairs rather than masonry. Eleven blocks of port
# between the two feet. The water face carries one, because the frontage east of the car park is not wide
# enough for two and a stair over the cars is a stair in the car park.
#
# **A flight is stone and a landing is the ground it joins.** The steps are the port's own masonry carried
# up the face, so they read as built; the landing is the last block before a player is simply on the field
# or in the settlement, and paving it as that ground is what stops the climb ending on a grey plate.
STAIRS = [
    ("field-stair",   7, (77, 16), +1, "head"),
    ("ridge-stair-w", 8, (61, 51), -1, "meadow"),
    ("ridge-stair-e", 8, (73, 51), +1, "meadow"),
]


def stairs():
    """The port's flights and their landings, on a layer at the port's own surface. The steps are ground
    somebody drew rather than ground that happened, so they are marked `keepClear` and the dressing pass
    puts nothing on them."""
    shapes = []
    for name, rise, (x, z), step, landing in STAIRS:
        flight = sorted(x + step * tread for tread in range(rise))
        head = sorted(x + step * (rise + along) for along in range(STAIR_LAND))
        # A course at the foot and the face's own at the head. The anchors sit half a course either side of
        # those, because a cell is sampled at its centre: on the whole numbers every tread falls on a tie and
        # the rounding turns a 1:1 flight into two-block steps.
        low, high = (0.5, rise + 0.5) if step > 0 else (rise + 0.5, 0.5)
        shapes += [
            {"id": f"{name}-flight", "type": "polygon", "operation": "add", "keepClear": True,
             "theme": "quay", "floor": 0,
             "vertices": [[flight[0], z], [flight[-1] + 1, z],
                          [flight[-1] + 1, z + STAIR_DEEP], [flight[0], z + STAIR_DEEP]],
             "anchor_heights": [low, high, high, low]},
            {"id": f"{name}-landing", "type": "rectangle", "operation": "add", "keepClear": True,
             "theme": landing, "floor": 0, "base_height": rise,
             "min_x": head[0], "max_x": head[-1] + 1, "min_z": z, "max_z": z + STAIR_DEEP},
        ]
    return {"id": "port-stairs", "name": "Port stairs", "base_y": PORT, "shapes": shapes,
            "groups": [{"id": "port-stairs-body", "name": "Port stairs", "mirrors": True,
                        "shapeIds": [shape["id"] for shape in shapes]}]}

THEMES = {
    # **Two grounds are built and take a face; the rest are landforms and take a stack.** A quay is masonry
    # with a kerb along its edge and a cut face where it drops to the water, and the seabed shelves into the
    # basin the same way — both want a surface, a wall and, on the quay, a rim. Grass, terracotta and a
    # working dock want none of that: a wall paints every riser as one material and a rim draws a line round
    # every plateau, which turns a hillside into a diagram of itself. Those three are stated as courses
    # instead, read down from the top block, the last repeating to the bedrock.
    #
    # **No ground a prop stands on is finished in a style whose palette holds wool.** The dressing pass reads
    # a wool-topped column as a stamp rather than terrain and declines everything on it (`DR-KEEP`), so a
    # quay paved in `white stone cells` or a hill turfed in `grass clay surface dark` takes no crate, no tree
    # and no house however flat it is. The rule is about the TOP block, which is why `stone dark voronoi` is
    # fine as a remainder: nothing stands on ground four courses down.
    "quay":   ground(style("oldstone · fill"), style("stone fractal"),
                     {"kind": "solid", "id": 98, "data": 0}),
    "seabed": ground(style("all sand"), style("dirt fractal")),

    # **One grass, not three.** `grass clay surface`, `oldstone · surface` and `meadow · surface` were three
    # greens doing one job, and a player crossing from the town to the hill to the back settlement read three
    # grounds where the board means one. The meadow is what survives, and it carries the whole upland — the
    # dock town, the terrace row, the hill, the spawn's approach and the settlements behind it.
    "meadow": layers((style("meadow · surface"), 1), (style("dirt fractal"), 3), (style("stone fractal"), 1)),
    "head":   layers((style("rust cells"), 2), (style("dirt fractal"), 3), (style("stone dark voronoi"), 1)),
    "dock":   layers((style("dirt fractal"), 2), (style("stone dark voronoi"), 1)),

    # A made thing is painted in solids: the painter's buckets are a model of ground — a rim capping every
    # plateau boundary, a wall down every riser — and a curved form is nothing but boundaries, so a shaded
    # theme speckles it.
    # Weather. White stained glass rather than wool or quartz: a cloud is the one thing on a board that
    # should not read as a solid, and the glass carries the light through instead of casting the map into
    # a shadow the shape of itself.
    "cloud": board.solid(95, 0),

    "car-paint": board.solid(159, 14), "car-trim": board.solid(35, 15),
    "car-glass": board.solid(95, 3), "car-tail": board.solid(35, 14),

    "hull": board.solid(5, 1), "strake": board.solid(35, 14), "rail": board.solid(5, 0),
    "deck": board.solid(5, 2), "spar": board.solid(17, 1), "rig": board.solid(35, 15),
    "canvas": board.solid(155, 0), "glass": board.solid(95, 3), "lamp": board.solid(89, 0),

    "envelope-a": board.solid(35, 14), "envelope-b": board.solid(35, 0),
    "envelope-band": board.solid(35, 11), "wicker": board.solid(5, 4), "flame": board.solid(89, 0),

    "stone": board.solid(98, 0), "iron": board.solid(35, 15), "chain": board.solid(1, 6),
    "timber": board.solid(5, 1),
}


# How far a corner may be drawn out, largest first — a vertex takes the first of these its own guard admits.
# Every block of it is ground nobody walks, so the budget is a look bought at a price: at these reaches the
# board grows about 8% and its dead share about two points, and at twice them it grows a quarter and reads
# as an island with a rind.
DRAW_OUT = (14, 10, 18, 8, 12, 16)
# And how much new ground one may take. The reach alone does not bound it: the triangle a corner sweeps is
# half its reach times the edge it swings, so ten blocks at the end of a hundred-block quay is five hundred
# cells of shore nobody walks. Capping the area is what makes the same budget mean the same thing on a
# forty-block field and on that quay — a long edge simply takes a shallower move. Set it much under this and
# the shapes worth reshaping are the ones refused: a forty-four-block edge cannot move a corner seven blocks
# inside two hundred cells.
GAIN_CAP = 320
# How far a drawn corner keeps off a goal, so an objective is never left standing on the step one made.
GOAL_STANDOFF = 14
# The curve a drawn corner's handles reach along the chord between its neighbours (Catmull-Rom). Below about
# 0.15 the pair of new edges still reads as two straight cuts; above about 0.35 a handle overshoots.
CURVE = 0.26


def plan_cells():
    """Every block the plan states ground at, its `rot_180` image included — the board's silhouette. Read
    from `PLAN` rather than from a build, so what the outline is tested against is the same set of rectangles
    the pieces are written as and cannot fall out of step with them."""
    cells = set()
    for piece in PLAN["pieces"]:
        cx, cz, wide, deep = piece["rect"]
        for x in range(cx * CELL, (cx + wide) * CELL):
            for z in range(cz * CELL, (cz + deep) * CELL):
                cells.add((x, z))
                cells.add((-x - 1, -z - 1))
    return cells


def goal_cells():
    """Every goal's own cell and its image. A pad drawn out to a goal's doorstep leaves the goal standing on
    the step (`WX11`), and a bay cut to it would strand it outright, so the outline keeps its distance."""
    at = set()
    for goal in PLAN["placements"]["destroyables"]:
        x, z = int(goal["at"][0] * CELL), int(goal["at"][1] * CELL)
        at.add((x, z)); at.add((-x, -z))
    return at


def spawn_cells():
    """Every block of a spawn piece and its image. A spawn's ground is a room's frame, stamped as a
    rectangle, so the shape carrying one keeps the corners the plan gave it."""
    cells = set()
    for piece in PLAN["pieces"]:
        if piece.get("role") != "spawn": continue
        cx, cz, wide, deep = piece["rect"]
        for x in range(cx * CELL, (cx + wide) * CELL):
            for z in range(cz * CELL, (cz + deep) * CELL):
                cells.add((x, z)); cells.add((-x - 1, -z - 1))
    return cells


def compiled_rings():
    """The polygons `POST /plan/compile` fuses the plan into, by shape id — abutting pieces of equal height
    become one ring apiece. Asked rather than assumed: the ids and the winding are the compile's."""
    body = json.dumps(PLAN).encode()
    request = urllib.request.Request(f"{API}/plan/compile", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as answer:
        compiled = json.load(answer)
    return [(shape["id"], shape.get("base_height"), [tuple(v) for v in (shape.get("vertices") or [])])
            for shape in compiled["layout"]["layers"][0]["layout"]["shapes"]]


def within(ring, px, pz):
    """Whether a point lies inside a ring — the winding-independent crossing test."""
    hit = False
    for index in range(len(ring)):
        ax, az = ring[index]
        bx, bz = ring[(index + 1) % len(ring)]
        if (az > pz) != (bz > pz) and px < (bx - ax) * (pz - az) / (bz - az) + ax:
            hit = not hit
    return hit


def outline():
    """The board's silhouette, redrawn on the shapes the plan compiles to.

    A plan is written in cell rectangles, so it can say where ground is and never what shape its edge is.
    What the compile hands back is that edge as a ring per fused component — the upland here is a single
    eight-vertex polygon, a stretched T where the spawn's approach steps back out of the hill — and **the
    ring is what to redraw**. `shapePropsById` merges `vertices` and `controls` onto a compiled shape, so a
    drawn ring replaces the compiled one and nothing upstream knows.

    **A corner is drawn out, never in.** Each vertex is offered a move along the bisector of its own two
    edges, in the direction that leaves the polygon: an outer corner grows a chamfer and the reflex corner of
    an L is pushed across its notch until the notch is a diagonal. The board gains a triangle of ground and
    reads as a landmass rather than a stack of rectangles.

    **What makes that safe is that it only ever adds.** A vertex may move only where the redrawn ring covers
    every cell the compiled one did and every cell it gains was void — so it cannot erode the shore, cannot
    reach into a neighbouring shape, and above all cannot open a **seam**: an edge shared with the shape
    beside it is exactly an edge whose outward side is that shape's ground, and a move across it fails the
    guard on its first cell. Drawing inward has no such property, which is what a subtract along the
    perimeter has to be checked for by hand.

    The guard is asked of the fan too, because a corner drawn out is drawn out twice — once here and once at
    its `rot_180` image — and two shapes growing into the same water is two shapes overlapping."""
    ground = plan_cells()
    occupied = set(ground)
    keep_square, goals = spawn_cells(), goal_cells()
    props = {}

    for shape_id, _height, ring in compiled_rings():
        if len(ring) < 3: continue
        ring = list(ring)
        # A shape carrying a spawn keeps the corners the plan gave it: a room is stamped as a rectangle.
        if any(cell in keep_square for cell in
               ((int(x), int(z)) for x, z in ring)): continue

        # **No two neighbours move.** A corner drawn out slants both of its edges, which is the whole effect;
        # move the vertex beside it the same way and the edge between them merely translates and the shape
        # is the rectangle it was, somewhere else.
        # **A reflex corner is offered its move first.** Only one vertex of any pair of neighbours may move,
        # so the order decides which; the vertex inside a notch is the one whose move is worth most, because
        # drawing it across the notch turns an L into a coast while drawing an outer corner only chamfers
        # one that already reads as an edge.
        curved, mine = set(), set()
        order = sorted(range(len(ring)),
                       key=lambda index: not reflex(ring[index - 1], ring[index],
                                                    ring[(index + 1) % len(ring)], ring))
        for index in order:
            if (index - 1) % len(ring) in curved or (index + 1) % len(ring) in curved: continue
            before, here, after = ring[index - 1], ring[index], ring[(index + 1) % len(ring)]
            for step, reach in ((step, reach) for reach in DRAW_OUT
                                for step in ways_out(before, here, after, ring)):
                moved = (round(here[0] + step[0] * reach, 1), round(here[1] + step[1] * reach, 1))
                drawn = ring[:index] + [moved] + ring[index + 1:]
                gained = trades(ring, drawn, before, here, after, moved)
                if gained is None: continue                       # the move would give ground back
                if len(gained) > GAIN_CAP: continue
                if any(cell in occupied or (-cell[0] - 1, -cell[1] - 1) in occupied for cell in gained):
                    continue
                if any(max(abs(x - gx), abs(z - gz)) < GOAL_STANDOFF
                       for x, z in gained for gx, gz in goals): continue
                occupied.update(gained)
                occupied.update((-x - 1, -z - 1) for x, z in gained)
                mine.update(gained)
                ring[index] = moved
                curved.add(index)
                break

        # A drawn corner bows an edge only where that edge **faces open water along its whole length**. The
        # guard that admits the move reads the polygon, and a Bézier leaves the polygon: bowing an edge
        # shared with the shape beside it pushes ground over that shape whatever the straight ring did, which
        # is how the upland came to stand six blocks proud one block from a goal. The test is per edge rather
        # than per corner, so a corner between a coast and a seam bows the one and holds the other.
        controls = {}
        for index in sorted(curved):
            x, z = ring[index]
            before, after = ring[index - 1], ring[(index + 1) % len(ring)]
            arriving = open_water(before, ring[index], ring, occupied, mine)
            leaving = open_water(ring[index], after, ring, occupied, mine)
            if not (arriving or leaving): continue
            tangent_x = (after[0] - before[0]) * CURVE
            tangent_z = (after[1] - before[1]) * CURVE
            reach = math.hypot(tangent_x, tangent_z)
            room = CURVE * 2 * min(math.hypot(x - before[0], z - before[1]),
                                   math.hypot(after[0] - x, after[1] - z))
            if reach > room > 0:
                tangent_x, tangent_z = tangent_x * room / reach, tangent_z * room / reach
            # A handle on the seam side is the vertex itself, which is a straight edge: `in` governs the edge
            # arriving and `out` the edge leaving, so one corner can bow its coast and hold its seam.
            controls[str(index)] = {
                "in": [round(x - tangent_x, 2), round(z - tangent_z, 2)] if arriving else [x, z],
                "out": [round(x + tangent_x, 2), round(z + tangent_z, 2)] if leaving else [x, z]}

        props[shape_id] = {"vertices": [[x, z] for x, z in ring]}
        if controls: props[shape_id]["controls"] = controls
    return props


def open_water(start, end, ring, occupied, mine):
    """Whether an edge faces nothing but void along its whole length — what a curve may bow into."""
    span = math.hypot(end[0] - start[0], end[1] - start[1])
    if span < 1: return False
    step_x, step_z = (end[1] - start[1]) / span, -(end[0] - start[0]) / span
    for at in range(int(span) + 1):
        px = start[0] + (end[0] - start[0]) * at / span
        pz = start[1] + (end[1] - start[1]) * at / span
        for side in (1, -1):
            probe = (px + step_x * side * 2.0, pz + step_z * side * 2.0)
            if within(ring, *probe): continue
            cell = (math.floor(probe[0]), math.floor(probe[1]))
            if cell in occupied and cell not in mine: return False
            break
    return True


def reflex(before, here, after, ring):
    """Whether a vertex is the inside corner of a notch — the interior reaching round more than a half turn,
    which is what an L has where its two arms meet."""
    def unit(from_point, to_point):
        length = math.hypot(to_point[0] - from_point[0], to_point[1] - from_point[1])
        return None if length == 0 else ((to_point[0] - from_point[0]) / length,
                                         (to_point[1] - from_point[1]) / length)
    back, on = unit(here, before), unit(here, after)
    if back is None or on is None: return False
    step_x, step_z = back[0] + on[0], back[1] + on[1]
    length = math.hypot(step_x, step_z)
    if length < 0.2: return False
    # The two steps toward a vertex's neighbours sum toward the interior at a convex corner and away from it
    # at a reflex one, which is the whole test.
    return not within(ring, here[0] + step_x / length * 2, here[1] + step_z / length * 2)


def ways_out(before, here, after, ring):
    """The unit steps a corner may be drawn along, in the order they are worth trying.

    **Carrying one edge on is tried before opening the angle.** A corner has two edges and a move along
    either keeps that one collinear and swings only the other, which is the whole of what makes a move
    admissible where one of the two is a seam: the west corner of the terracotta field carries its own north
    edge on and the field grows a headland, while the same corner taken along the bisector swings that north
    edge into the town beside it and the guard has to throw the move away. The bisector is tried last, and it
    is what a corner with two free edges — the reflex vertex inside the upland's notch — takes."""
    def unit(from_point, to_point):
        length = math.hypot(to_point[0] - from_point[0], to_point[1] - from_point[1])
        return None if length == 0 else ((to_point[0] - from_point[0]) / length,
                                         (to_point[1] - from_point[1]) / length)
    along_back, along_on = unit(before, here), unit(after, here)
    if along_back is None or along_on is None: return []
    away_back, away_on = (-along_back[0], -along_back[1]), (-along_on[0], -along_on[1])
    corner_x, corner_z = away_back[0] + away_on[0], away_back[1] + away_on[1]
    length = math.hypot(corner_x, corner_z)
    steps = [along_back, along_on]
    if length >= 0.2:
        corner = (corner_x / length, corner_z / length)
        steps.append(corner if not within(ring, here[0] + corner[0] * 2, here[1] + corner[1] * 2)
                     else (-corner[0], -corner[1]))
    return steps


def trades(ring, drawn, before, here, after, moved):
    """The cells a redrawn ring gains, or `None` if it gives any back. Only the two triangles either side of
    the moved vertex can change, so that is all this reads."""
    corners = [before, here, after, moved]
    lo_x, hi_x = int(min(c[0] for c in corners)) - 2, int(max(c[0] for c in corners)) + 2
    lo_z, hi_z = int(min(c[1] for c in corners)) - 2, int(max(c[1] for c in corners)) + 2
    gained = []
    for x in range(lo_x, hi_x + 1):
        for z in range(lo_z, hi_z + 1):
            was = within(ring, x + 0.5, z + 0.5)
            now = within(drawn, x + 0.5, z + 0.5)
            if was and not now: return None
            if now and not was: gained.append((x, z))
    return gained


def finish(add_layers):
    # Every ground a settlement stands on is a terrace, not a slope: the docks, the quay and the port, the
    # town and the upland stand out of the relief entirely, so the relaxation bends round them and a house is
    # built on the flat. The hill and the balloon's field keep their relief, which is what they are for.
    # The coast and the terraces are two statements about the same compiled shapes, so they are merged onto
    # one entry apiece rather than one overwriting the other.
    shaped = outline()
    for shape_id, height, _ring in compiled_rings():
        if height in (DOCK, PORT, TOWN, BACK):
            shaped.setdefault(shape_id, {})["relief_scope"] = "exclude"

    return {
        "authors": ["Opus 5"],
        "created": "2026-08-29",
        "themeByHeight": {str(BASIN): "seabed", str(DOCK): "dock", str(QUAY): "quay", str(TOWN): "meadow",
                          str(HEAD): "head", str(RIDGE): "meadow", str(BACK): "meadow"},
        "mapTheme": "quay",
        "themes": THEMES,
        "shapePropsById": shaped,
        # The stairs first: they are ground laid on the compiled ground, and the made things stand on both.
        "addLayers": [stairs()] + add_layers,
        # The spawn is a building rather than a bedrock box: a stamped two-storey hall with its own doorway.
        "roomStyles": {"spawn": "@sb-spawn"},
        # The ground the plan states is a set of plateaus; the relief is what makes it terrain. `reach` 26
        # shelves the quay into the basin over a beach rather than dropping it down a wall, and the marks
        # behind it roll the town — the two terraces excluded above stay flat inside it.
        "relief": {"team": {"base": TOWN, "reach": 26, "step": 1, "stairs": True, "marks": [
            {"id": "harbour-floor", "kind": "area", "h": BASIN,
             "ring": [[-50, -14], [50, -14], [50, 14], [-50, 14]]},
            {"id": "quay-line", "kind": "line", "h": QUAY,
             "points": [[-52, 20], [-10, 22], [30, 20], [96, 22]]},
            {"id": "town-roll", "kind": "area", "h": TOWN + 2,
             "ring": [[-70, 34], [-32, 32], [-28, 58], [-68, 62]]},
            {"id": "field-crown", "kind": "point", "at": [-80, -12], "h": HEAD + 3, "r": 22},
            {"id": "port-flat", "kind": "area", "h": PORT,
             "ring": [[46, 18], [98, 18], [98, 54], [46, 54]]},
            {"id": "hill-crown", "kind": "line", "h": RIDGE + 5,
             "points": [[-66, 76], [-16, 82], [22, 80], [66, 78]]},
            {"id": "back-flat", "kind": "area", "h": BACK,
             "ring": [[30, 58], [70, 58], [70, 94], [30, 94]]},
        ]}},
        "dressing": {"props": ROADS + [
            # The harbour: a filled ring at a stated level, on the ground layer so its bed is the seabed and
            # not the hull of the ship floating in it. `radius` on a pool is the shelf — how far in from the
            # shore the bed reaches full depth — so the water shallows against the quays.
            # **The ring is the basin piece, to the block.** A pool cuts its bed wherever the ground stands
            # above it, so a ring drawn wider than the water's own ground digs the quay it laps and floods
            # the field beside it: the harbour's edge is the plan's, not a rectangle around it.
            {"id": "harbour", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool",
             "points": [[-52, -16], [52, -16], [52, 16], [-52, 16]],
             "radius": 12, "depth": 6, "shore": 2, "shoreWander": True, "edge": 1.2, "level": WATER,
             "bank": {"kind": "voronoi", "seed": 3, "cellSize": 6, "bands": [
                 {"material": {"kind": "solid", "id": 13, "data": 0}, "thickness": 2},
                 {"material": {"kind": "solid", "id": 3, "data": 1}, "thickness": 1},
                 {"material": {"kind": "solid", "id": 12, "data": 0}, "thickness": 1}]}},
        ] + houses() + crates() + trees()},
        "voidEnforcement": True,
    }


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "specs/opus5-slipway"
    slug = os.path.basename(os.path.abspath(out))
    os.makedirs(out, exist_ok=True)

    add_layers, table = sculpted()
    json.dump(PLAN, open(f"{out}/{slug}.plan.json", "w"), indent=2)
    json.dump(finish(add_layers), open(f"{out}/{slug}.finish.json", "w"), indent=2)

    width = max(len(name) for name, _ in table)
    print(f"{'model':<{width}}  {'blocks':>7} {'layers':>7} {'shapes':>7} {'b/shape':>8}")
    for name, row in table:
        print(f"{name:<{width}}  {row['blocks']:>7} {row['layers']:>7} {row['shapes']:>7} "
              f"{row['blocks_per_shape']:>8}")
    print(f"\nspec written to {out}/ ({len(add_layers)} added layers, {len(HOUSES)} houses)")


if __name__ == "__main__":
    main()
