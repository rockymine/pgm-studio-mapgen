#!/usr/bin/env python3
"""Flintwick — a capture board on two chalk headlands facing each other over a sound.

The board is about one material: flint. Chalk is white end to end, and the only dark thing on it is
the flint that the chalk itself carries — so the dark is never laid across the board as a band. It is
painted on the `slope` axis over about thirty-two degrees and in the wall bucket, which means a black
cell can only appear where the ground has an exposed face: the sea cliff, the cut behind each wool
room, the sides of the stair. A boundary between white and black is therefore always a break of slope.

The arrangement is four grounds and the joins between them:

  the sound      the twenty blocks of void down the middle; crossed by a bridge a player builds
  the strand     the wave-cut platform at the water, where that bridge lands — one flat ground
  the cliff      a `scarp` mark traced as a curve, so the frontline is not the plan rectangle's edge
  the headland   the chalk top the match is fought on, carrying the spawn and the two wool rooms

and the wick the board is named for: a bay of open void cut thirty-five blocks into the headland
between its two nabs, so the land is two arms joined only behind the bay head. A raider who lands on
one strand is on one arm, and the wool room at the other end of the board is a walk round the wick or
a second bridge. It is also what keeps the plan off the corpus's fill-ratio ceiling: a capture board
in the envelope is not a solid rectangle of land.

and the two stairs, which are authored flights rather than graded relief: a flight states a boundary
where a relief graded across the seam would delete it.
"""
import json, math, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-flintwick"
API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api").rstrip("/").removesuffix("/api")

# ── the plan: the arrangement, and nothing else ──────────────────────────────────────────────────
# One headland piece carries the whole played ground. The three pieces behind it are the spawn and
# the two wool rooms, which are rooms rather than landforms: a room needs a piece of its own for the
# compiler to seat it in. Everything else — the cliff, the strand, the coombe — is authored below.
plan = {
    "plan": 2,
    "meta": {"name": "Flintwick"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": 26, "observerY": 60},
    "pieces": [
        {"id": "west-nab", "role": "piece",     "rect": [-8,  2,  6, 12], "surface": 26},
        {"id": "east-nab", "role": "piece",     "rect": [ 2,  2,  6, 12], "surface": 26},
        {"id": "wick",     "role": "piece",     "rect": [-2,  9,  4,  8], "surface": 26},
        # A wool room stands at the far end of a spur off the island, not alongside the spawn: a
        # lane piece the width of the room and twenty-five blocks long, with the room on its tip.
        # The spawn is a separate piece with void either side of it, so neither room is something a
        # defender is already standing in.
        #
        # The lane's four pieces are stated at 31 and not at the 26 the rest of the board uses,
        # because the relief settles this corner five courses over `base` and the WALL's height is
        # taken from the plan: at 26 its top lands at y30 and the terrain buries it, cobweb course
        # and all. The seam `EL1` then reports against `west-nab` is not in the world — the two
        # solve within a block of each other, and the transect up the lane walks `worst step 1`.
        {"id": "lane-w",   "role": "piece",     "rect": [-8, 14,  4,  2], "surface": 31},
        {"id": "head-w",   "role": "piece",     "rect": [-8, 16,  4,  3], "surface": 31},
        {"id": "lane-e",   "role": "piece",     "rect": [ 4, 14,  4,  2], "surface": 31},
        {"id": "head-e",   "role": "piece",     "rect": [ 4, 16,  4,  3], "surface": 31},
        {"id": "staith",   "role": "spawn",     "rect": [-3, 17,  6,  3], "surface": 27},
        {"id": "knapp-w",  "role": "wool-room", "rect": [-8, 19,  4,  3], "surface": 31},
        {"id": "knapp-e",  "role": "wool-room", "rect": [ 4, 19,  4,  3], "surface": 31},
    ],
    # The wick is a build zone as well as the sound is: a bay a player cannot bridge is a wall
    # drawn as water, and it also turns each arm's inner face into thirty blocks of frontline
    # instead of the ten-block funnel `FR9` names.
    "zones": [{"id": "sound", "rect": [-8, -4, 16, 8], "kind": "build"},
              {"id": "wick-water", "rect": [-2, 4, 4, 5], "kind": "build"}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "staith", "at": [15, 7], "facing": "front",
                    "footprint": [6, 3, 18, 9]}],
        "iron": [{"id": "iron-1", "piece": "staith", "at": [2, 7]},
                 {"id": "iron-2", "piece": "staith", "at": [28, 7]}],
        "wools": [{"id": "wool-1", "piece": "knapp-w", "at": [10, 7], "footprint": [2, 2, 16, 11]},
                  {"id": "wool-2", "piece": "knapp-e", "at": [10, 7], "footprint": [2, 2, 16, 11]}],
        "destroyables": [], "cores": [],
    },
    # the bedrock wall along each lane, at the seam fifteen blocks in front of the room's door,
    # which is where `ST8` seats one. It is the only thing a lane is dressed with.
    "walls": [{"a": "lane-w", "b": "head-w"}, {"a": "lane-e", "b": "head-e"}],
    "boxes": [],
}

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0):  return {"kind": "solid", "id": i, "data": d}

CHALK, QUARTZ, RUBBLE = solid(159, 0), solid(155, 0), solid(159, 8)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
FLINT = solid(173)                       # the one dark block on the board
STONEBRICK, CHISELLED = solid(98), solid(98, 3)
BIRCH_LOG, BIRCH_PLANK = solid(17, 2), solid(5, 2)
QUARTZ_PILLAR, QUARTZ_SLAB, QUARTZ_STAIR = solid(155, 2), 44, 156
GRASS, COARSE = solid(2), solid(3, 1)
LAID_BIRCH = {"kind": "laidLog", "id": 17, "data": 2}


def cell_(seed, size, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


DOWN   = cell_(21, 11, [CHALK, QUARTZ, CHALK, GRASS, RUBBLE])  # chalk top, turf showing through
SHOULD = cell_(22,  7, [RUBBLE, GRAVEL, CHALK])          # where it starts to shed
KNAP   = cell_(23,  6, [FLINT, ANDESITE, GRAVEL])        # flint: faces only, never a flat
SHINGLE = cell_(24, 5, [GRAVEL, COBBLE, ANDESITE, STONE])

# The whole argument of the board is in this one stack. A band on the `slope` axis is a span of
# degrees, so the black band cannot be reached by any cell that is not standing on a face — and each
# band takes a depth stack of its own, so the flint is one course over chalk rather than a black hill.
CHALK_SURFACE = layered([
    (12, layered([(1, DOWN),   (3, CHALK)])),            # under 12°: the down itself
    (20, layered([(1, SHOULD), (3, CHALK)])),            # 12-32°: the rubble shoulder
    (58, layered([(1, KNAP),   (3, cell_(25, 8, [STONE, CHALK]))])),   # over 32°: knapped flint
], axis="slope")

themes = {
    "chalk": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHALK},
        "surface": {"enabled": True, "depth": 4, "material": CHALK_SURFACE},
        # the wall bucket is the exposed riser, which on chalk is exactly where flint shows
        "wall":    cell_(26, 7, [FLINT, ANDESITE, STONE, GRAVEL], rise=4), "wallEnabled": True,
        "fill":    cell_(27, 9, [CHALK, STONE], rise=5),
    },
    # the strand: the wave-cut platform at the water. Shingle, walked flat, and grey against the
    # chalk above it rather than against the chalk beside it — the cliff is what separates them.
    "strand": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COBBLE},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, SHINGLE), (2, cell_(28, 7, [GRAVEL, STONE]))])},
        "wall":    cell_(29, 8, [STONE, COBBLE, FLINT], rise=5), "wallEnabled": True,
        "fill":    cell_(30, 9, [STONE, ANDESITE], rise=6),
    },
    # the sward: the hollows and lee slopes where soil has stayed on the chalk. It is the only ground
    # on this board a tree can stand on — a thorn seated on quartz or on flint reads as a tree
    # growing out of a floor, and there is no other soil anywhere in the palette.
    "sward": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": COARSE},
        "surface": {"enabled": True, "depth": 4,
                    "material": layered([(1, cell_(39, 9, [GRASS, GRASS, COARSE])),
                                         (3, cell_(40, 7, [COARSE, CHALK]))])},
        "wall":    cell_(41, 6, [CHALK, RUBBLE, FLINT], rise=3), "wallEnabled": True,
        "fill":    cell_(42, 9, [CHALK, STONE], rise=5),
    },
    # the knapping floors: the cut yards the two wool rooms stand in, and the working ground round
    # them. Flint chippings trodden into chalk rubble — the one place flint lies on a flat, and it
    # lies there because it is waste from the faces cut behind it.
    "knap": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim":     {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 3,
                    "material": layered([(1, cell_(31, 4, [RUBBLE, GRAVEL, FLINT, COBBLE])),
                                         (2, cell_(32, 7, [CHALK, COBBLE]))])},
        "wall":    cell_(33, 6, [FLINT, ANDESITE, COBBLE], rise=4), "wallEnabled": True,
        "fill":    cell_(34, 9, [CHALK, STONE], rise=5),
    },
}

# ── the relief: four grounds, and where each one ends ────────────────────────────────────────────
STRAND, LEDGE, DOWNLAND, NAB, GARTH = 19, 22, 27, 31, 28


def lobe(cx, cz, radii, tilt=0.0):
    n = len(radii)
    return [[round(cx + r * math.cos(tilt + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(tilt + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]


relief = {
    "team": {
        "base": DOWNLAND, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 20, "seed": 3},
        "marks": [
            # the strand: flat to the water, because a bridge lands on something level. Its inland
            # edge is drawn rather than ruled — the coast of this board is a curve and the plan
            # rectangle it sits in is not visible anywhere on it.
            {"id": "strand", "kind": "area", "h": STRAND, "bevel": 2,
             "ring": [[-44, 6], [-30, 13], [-14, 21], [6, 16], [22, 25], [38, 18], [44, 6]]},
            # a shelf halfway up the west end, so the cliff is two steps there and one everywhere
            # else: the west is the way up that costs less and is watched from more places.
            {"id": "ledge", "kind": "area", "h": LEDGE, "bevel": 2,
             "ring": lobe(-28, 28, [13, 10, 12, 9, 13, 10, 12, 9], 0.3)},
            # the cliff. Traced with x increasing, which puts the high side on +z — the headland.
            # Five courses over a three-block face is a drop rather than a path.
            {"id": "cliff", "kind": "scarp",
             "points": [[-42, 24], [-26, 33], [-8, 29], [10, 36], [28, 31], [42, 38]],
             "high": DOWNLAND - 1, "low": STRAND + 2, "face": 3, "band": 8},
            # the garth behind the spawn, which the two wool rooms open onto
            {"id": "garth", "kind": "area", "h": GARTH, "bevel": 4,
             "ring": lobe(0, 92, [22, 18, 21, 16, 22, 18, 21, 16], 0.1)},
            # two chalk nabs on the down, which is what keeps the top from being one plane and gives
            # the board somewhere to stand that is not the route
            {"id": "nab-w", "kind": "point", "at": [-26, 58], "r": 7, "h": NAB},
            {"id": "nab-e", "kind": "point", "at": [24, 68], "r": 6, "h": NAB - 1},
        ],
        "pushes": [
            # the coombe: a dry valley in the down, which is the one piece of cover between the
            # cliff and the garth. Four down over a seven-block skirt, so it is a hollow and not a pit.
            {"id": "coombe", "ring": lobe(2, 60, [16, 13, 15, 12, 16, 13, 15, 12], 0.6),
             "amount": -4, "falloff": 7, "crown": 6, "roughness": 1, "seed": 4},
            # a swell east of it so the down reads as ground rather than as a table with a dent in it
            {"id": "swell", "ring": lobe(-6, 78, [12, 10, 11, 9, 12, 10, 11, 9], 0.2),
             "amount": 3, "falloff": 8, "crown": 4, "roughness": 1, "seed": 5},
        ],
    }
}

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
STAIR_STONE = cell_(35, 4, [COBBLE, STONE, ANDESITE], rise=2)


def flight(id_, ring, low, high):
    """One polygon, a height per vertex: sheer-sided, kept clear, and a material rather than a theme
    because a made thing is not a place. Run at least twice the rise, or it is a wall with treads."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": STAIR_STONE,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


def pad(id_, ring, height, theme):
    """Ground the relief is not allowed to touch. `relief_scope: "exclude"` takes the footprint out
    of the solve, so the down meets the cut at a face instead of being graded into it."""
    return {"id": id_, "type": "polygon", "operation": "add", "group": "team",
            "height_mode": "level", "base_height": height, "skirt": 0,
            "relief_scope": "exclude", "theme": theme,
            "vertices": [[x, z] for x, z in ring]}


def wall(id_, points, seed):
    """A knapped field wall: a `polyline`, whose band is `radius` and whose centreline is `vertices`,
    splined before the band is offset so four clicked points draw as a curve."""
    return {"id": id_, "type": "polyline", "operation": "add", "group": "team",
            "height_mode": "raise", "base_height": 2, "radius": 1.5, "stroke_edge": "rough",
            "stroke_seed": seed, "skirt": 0,
            "material": cell_(36, 5, [FLINT, COBBLE, ANDESITE, CHALK], rise=2),
            "vertices": [[x, z] for x, z in points]}


def paint(id_, ring, theme):
    """A paint patch on solved ground: it declares a height_mode or it is never a candidate for the
    cell and paints nothing, in silence. A raise of 0 sits flush at the median ground."""
    return {"id": id_, "type": "polygon", "operation": "add", "group": "team",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": [[x, z] for x, z in ring], "theme": theme}


add_shapes = [
    # The sward goes down FIRST. A later shape wins a contested cell, and a `raise 0` paint patch
    # drawn over a flight sets that column back to the median ground — which flattened the west
    # stair's upper half into the down and put a four-course drop at (-29, 40) that reads as terrain
    # and names nothing. Paint the ground, then cut the flights into it.
    # the sward, in the coombe and on each arm's lee. Every one of them is somewhere the ground is
    # shallow and out of the wind, which is the answer to "why here".
    paint("sward-coombe", lobe(0, 60, [16, 13, 15, 12, 16, 13, 15, 12], 0.5), "sward"),
    paint("sward-west",   lobe(-31, 52, [13, 10, 12, 9, 13, 10, 12, 9], 0.3), "sward"),
    paint("sward-east",   lobe(28, 62, [16, 13, 15, 12, 16, 13, 15, 12], 0.3), "sward"),
    # the two ways off the cliff. West is a stair in two flights off the shelf, east is one long
    # ramp cut in the face. Both are run at more than twice their rise and both are authored, so
    # neither is a seam the relief happened to leave.
    flight("stair-w-lo", [(-33, 14), (-25, 14), (-25, 27), (-33, 27)], STRAND, LEDGE),
    # BOTH ends are cut to the height the ground ACTUALLY has where the flight meets it, read off the
    # built world at x -29: y24 at z32 below the face and y31 at z48 above it. A flight given one
    # number for two different grounds tops out under the down at one end or over the ledge at the
    # other, and either way it is not a way up anything (`SK26`). Sixteen of run for seven of rise.
    flight("stair-w-hi", [(-30, 32), (-22, 32), (-22, 48), (-30, 48)], 24, 31),
    # The east arm is lower than the west where its ramp arrives: the down stands at 26 at
    # (24, 46) and the head is cut to meet it, not to the west stair's number.
    flight("ramp-e",     [(20, 16), (28, 16), (28, 46), (20, 46)], STRAND, DOWNLAND - 1),
    # the strand's own paint, drawn to the mark that made it
    paint("strand-floor", [[-44, 6], [-30, 13], [-14, 21], [6, 16], [22, 25], [38, 18], [44, 6]],
          "strand"),
    # No flight on either lane. The ground already climbs it — read at x -30, the lane runs y26 at
    # the wall to y31 at the room's door — and a `level` flight anchored to the plan's numbers
    # instead of to that reading cut a five-course slot across the mouth and made the spur one-way.
    # A lane needn't be flat and this one is not; what it must not have is a hole in it.
    # the two knapping yards: the wool rooms stand in cuts, not on the down. The cut's back wall is
    # a face, which is where the theme's flint lands — the dark is the reason the room is there.
    pad("yard-w", [(-37, 88), (-23, 88), (-23, 94), (-37, 94)], 31, "knap"),
    pad("yard-e", [(23, 88), (37, 88), (37, 94), (23, 94)], 31, "knap"),
    # a knapped wall along each arm's cliff top, drawn as a polyline so the rasterizer splines it:
    # four clicked points come out as a curve, which a chain of rectangles cannot do. It is the built
    # edge the down stops at, and it is the reason the one straight-looking line on the board is not
    # straight. One per arm, because the wick between them is open water and a wall does not cross it.
    # A flowing line is a `polyline`, and its band is stated the way every other shape states one:
    # `radius` is the half-width and `vertices` the open centreline, which the rasterizer splines
    # before it offsets. Given `width` and `points` instead it is a path of width nought and draws
    # no ground at all, on a 200 (`SK4`).
    # Each arm's wall is TWO runs with a gateway between them, and the gateway is where the flight
    # comes up. Drawn as one run it stands two courses proud across the head of the ramp, which reads
    # back as `BARRIER +3` at (24, 44) and a stair that arrives at a wall — a fault of the wall and
    # not of the flight, and invisible to everything but a transect.
    wall("wall-w-a", [[-40, 38], [-35, 42], [-31, 43]], 7),
    wall("wall-w-b", [[-21, 41], [-17, 43], [-13, 48]], 9),
    wall("wall-e-a", [[10, 50], [15, 44], [19, 42]], 8),
    wall("wall-e-b", [[29, 44], [34, 46], [40, 42]], 10),
]

# ── what is built ────────────────────────────────────────────────────────────────────────────────
# Three families, named before anything is painted: the GROUND is chalk-white, what is BUILT is
# knapped flint coursed with chalk rubble on a cobble footing, and the ACCENT is the flint itself.
# Nothing here is a colour; the whole board is a value range from white to black.
def knap_style(storeys, tinted=True):
    top = ({"kind": "teamTint", "blockId": 159, "neutral": CHISELLED} if tinted else CHISELLED)
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 2},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": STONEBRICK},
        "roof": {"form": "hip", "pitch": 1, "slab": QUARTZ_SLAB, "slabData": 7, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": QUARTZ, "verge": QUARTZ_PILLAR, "gable": CHALK,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": stack([(4, {"kind": "voronoi", "seed": 61, "cellSize": 4, "rise": 0,
                                      "bands": [{"thickness": 2, "material": FLINT},
                                                {"thickness": 1, "material": CHALK},
                                                {"thickness": 1, "material": COBBLE}]}),
                                 (1, top)], "repeat"), "extent": 5},
        "post": CHISELLED,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 4},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
        # `HS4`: the two corners of a head and the line between them are cut from one material, so
        # quartz stairs take a quartz slab and never a stone-brick one.
        "doorway": {"door": "air", "head": {"form": "arched", "block": QUARTZ_STAIR,
                                            "fill": "upperSlab",
                                            "fillBlock": QUARTZ_SLAB, "fillData": 7},
                    "width": 2, "height": 3},
    }


WORK_STOREY = {
    "clear": 5, "post": CHISELLED, "deck": None,
    "wall": {"stack": stack([(2, COBBLE), (3, CHALK)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 4},
}
LOFT_STOREY = {
    "clear": 3, "post": BIRCH_LOG, "deck": None,
    "wall": {"stack": stack([(2, CHALK), (1, LAID_BIRCH)], "repeat"), "extent": 3},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 1, "spacing": 4},
}
knapping_shed = knap_style([WORK_STOREY], tinted=True)
staith_hall = knap_style([WORK_STOREY, LOFT_STOREY], tinted=False)
watch = knap_style([dict(WORK_STOREY, clear=4)], tinted=False)

# ── what stands on it ────────────────────────────────────────────────────────────────────────────
# Thorn on the exposed down, birch in the coombe where it is out of the wind: two bodies for two
# places, which is the only reason to carry two.
THORN = ["tree-showcase-r4-%d" % n for n in (1, 2, 3, 4, 5)]
BIRCH = ["tree-showcase-r13-%d" % n for n in (1, 3, 5)]


def library_tree(name):
    with urllib.request.urlopen(f"{API}/api/tree-styles") as handle:
        index = {row["name"]: row["id"] for row in json.load(handle)}
    with urllib.request.urlopen(f"{API}/api/tree-styles/{index[name]}") as handle:
        style = json.load(handle)
    return {"kind": "tree", "form": "copied", "body": style["body"]}


def path(id_, points, radius, pave, style="solid", coverage=1.0, seed=0, claims=True):
    return {"id": id_, "kind": "stroke", "seed": seed, "radius": radius, "style": style,
            "coverage": coverage, "claimsGround": claims, "pave": pave, "points": points}


WAY = cell_(37, 5, [CHALK, GRAVEL, RUBBLE])              # a chalk track: white, worn through
BOULDER = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell_(38, 4, [STONE, COBBLE, ANDESITE], rise=2)}

props = [
    # the ways: out of the door, along the top, and down to each stair head. A chalk track on a
    # chalk down is the right kind of invisible — it is read as worn, not as a line drawn on.
    path("way-spine",  [[0, 86], [-2, 74], [2, 62], [0, 52]], 2, WAY, seed=41),
    path("way-west",   [[-6, 80], [-18, 74], [-26, 60], [-27, 47]], 2, WAY, seed=42),
    path("way-east",   [[8, 80], [19, 74], [24, 60], [24, 47]], 2, WAY, seed=43),
    path("way-yard-w", [[-26, 66], [-30, 76], [-30, 90]], 2, WAY, seed=44),
    path("way-yard-e", [[26, 66], [30, 76], [30, 90]], 2, WAY, seed=45),
    # the watch: one small building on the nab east of the coombe, looking over the sound. It is on
    # the down rather than in a yard, so it stands where the two ways meet and nowhere near a door.
    {"id": "watch", "kind": "house", "seed": 601, "front": "negX", "style": "watch",
     "wings": [{"corners": [[30, 52], [37, 60]], "spec": {"ridge": "alongZ"}},
               {"corners": [[25, 54], [29, 59]], "spec": {"storeysHigh": 1, "ridge": "alongX"}}]},
    {"id": "sward", "kind": "flora", "seed": 901,
     "points": [[-38, 14], [38, 14], [38, 96], [-38, 96]],
     "spec": {"coverage": 0.16, "scale": 26, "octaves": 3, "fernShare": 0.22,
              "flowerShare": 0.05, "flowerScale": 14, "tallShare": 0.05}},
]
# thorn on the open down, birch down in the coombe. Nothing on the strand: the landing ground is
# bare, and that is what makes crossing the sound the decision the board is about.
for i, (x, z) in enumerate([(-34, 50), (-38, 56), (-37, 48), (16, 44), (36, 64), (16, 58)]):
    props.append({"id": f"thorn-{i}", "kind": "tree", "seed": 701 + i, "x": x, "z": z,
                  "style": THORN[i % len(THORN)]})
for i, (x, z) in enumerate([(-8, 58), (8, 62), (6, 54)]):
    props.append({"id": f"birk-{i}", "kind": "tree", "seed": 721 + i, "x": x, "z": z,
                  "style": BIRCH[i % len(BIRCH)]})
# sarsens: stone, cobblestone and andesite and nothing else. Pale ground is exactly where a paled
# boulder disappears, so these are left the colour stone is. One of them lies on the strand, which is
# where a chalk coast puts the flints the cliff has already given up.
for i, (x, z) in enumerate([(-32, 62), (16, 20), (-36, 40), (32, 44), (-20, 52), (12, 54)]):
    props.append(dict(BOULDER, id=f"sarsen-{i}", kind="boulder", seed=741 + i, x=x, z=z,
                      size=4 if i % 2 == 0 else 3))

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-14",
    "themes": themes,
    "mapTheme": "chalk",
    # Stone Beach tints grass and water a cold grey-green, which is what a sound between two chalk
    # headlands looks like — not the blue of a warm sea.
    "biome": {"kind": "solid", "id": 25},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"wool": knapping_shed, "spawn": staith_hall},
    "dressing": {"styles": dict({name: library_tree(name) for name in THORN + BIRCH},
                                watch={"kind": "house", "shell": watch}),
                 "props": props},
}

json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json  "
      f"({len(plan['pieces'])} pieces, {len(relief['team']['marks'])} marks, "
      f"{len(relief['team']['pushes'])} pushes, {len(add_shapes)} shapes, {len(props)} props)")
