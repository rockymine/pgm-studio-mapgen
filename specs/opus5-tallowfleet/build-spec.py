#!/usr/bin/env python3
"""Tallowfleet — one board played for a monument and a wool at once.

Writes `opus5-tallowfleet.plan.json` and `opus5-tallowfleet.finish.json` beside this file.

A tidal tallow works on a grey estuary. Each team defends **two** objectives that ask for
opposite things, which is the whole reason this board exists: the monument stands out on the
open quay a short walk forward of the spawn, and the wool lies in a cellar at the end of a
walled spur behind it. One is broken where it stands and the other has to be fetched and
carried home, so a defence that holds the quay is not a defence that holds the cellar.

`docs/gameplay/approaches.md` settles the arrangement: a core or a monument is the forward
objective and a wool is the deep one, because a wool has to be brought back. Drafted the
other way round the wool sits at the front and `WL10` reads a wool-front-distance of 8.

Scale: cell 5. The team unit is authored at -z and rot_180 fans the rest.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-tallowfleet"

# ── blocks ────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE = 1, 2, 3, 4
GRAVEL, SAND, CLAY = 13, 12, 82
STONE_BRICK, LOG, LOG2, QUARTZ = 98, 17, 162, 155
SPRUCE_PLANKS, OAK_PLANKS = (5, 1), (5, 0)
SPRUCE_LOG = (LOG, 1)
SPRUCE_STAIRS, SPRUCE_SLAB = 134, (126, 1)
COARSE_DIRT, PODZOL = (DIRT, 1), (DIRT, 2)
ANDESITE, DIORITE = (STONE, 5), (STONE, 3)
MOSSY_BRICK, CHISELLED_BRICK = (STONE_BRICK, 1), (STONE_BRICK, 3)
WHITE_CLAY, BLACK_CLAY, BROWN_CLAY = (159, 0), (159, 15), (159, 12)


def solid(block, data=0):
    if isinstance(block, tuple):
        block, data = block
    return {"kind": "solid", "id": block, "data": data}


def _stack(axis, flat):
    pairs = list(zip(flat[0::2], flat[1::2]))
    return {"kind": "layered", "axis": axis, "stack": {
        "ending": "repeat",
        "bands": [{"material": m, "thickness": t} for m, t in pairs]}}


def depth(*flat):
    """A stack down from the surface, so a surfacing block stays one course over its soil."""
    return _stack("depth", flat)


def slope(*flat):
    """A stack across the ground's angle: a thickness here is a span of degrees."""
    return _stack("slope", flat)


def cells(palette, size, seed, jitter=40, warp=2, rise=3):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": [solid(b) for b in palette], "rise": rise}


def voronoi(palette, size, seed, rise=4):
    """The body of the rock a cut shows, and it is stone."""
    return {"kind": "voronoi", "seed": seed, "cellSize": size, "rise": rise,
            "bands": [{"material": solid(b), "depth": d}
                      for b, d in zip(palette, (1, 2, 3))]}


def theme(surface, wall, fill, rim=None, surface_depth=3):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": ({"enabled": False, "depth": 1, "material": solid(STONE)} if rim is None
                else {"enabled": True, "depth": rim[0], "material": rim[1]}),
        "surface": {"enabled": True, "depth": surface_depth, "material": surface},
        "wallEnabled": True,
        "wallOnTerrainFaces": True,
        "wall": wall,
        "fill": fill,
    }


# ── the plan ──────────────────────────────────────────────────────────────────
# Five pieces, and every one of them states something the arrangement needs. The quay is the
# forward ground the monument stands on and the contest happens over; the works is the
# terrace behind it; the spawn hangs off the works' west end and the cellar spur off its
# east, so the two objectives are reached by two different journeys rather than one corridor.
CELL = 5
QUAY_SURFACE, WORKS_SURFACE = 10, 15

plan = {
    "plan": 2,
    "meta": {
        "name": "Tallowfleet",
        "notes": ("CTW and DTM on one board. The monument stands forward on the open quay "
                  "and the wool lies in a cellar at the end of a walled spur behind the "
                  "works, so holding the quay is not holding the cellar."),
    },
    "globals": {
        "cell": CELL,
        "symmetry": "rot_180",
        "maxPlayers": 16,
        "surface": QUAY_SURFACE,
        "observerY": 56,
    },
    "pieces": [
        # blocks x[-35,15] z[-95,-75] — the tallow works, five courses up
        {"id": "works", "role": "piece", "rect": [-7, -19, 10, 4], "surface": WORKS_SURFACE},
        # blocks x[15,40] z[-95,-75] — the spur the cellar hangs off
        {"id": "spur", "role": "piece", "rect": [3, -19, 5, 4], "surface": WORKS_SURFACE},
        # blocks x[10,25] z[-115,-95] — the back lane, fifteen blocks wide, from the
        # works' north-east corner to the cellar's west face. It is the cellar's second way in and
        # a chokepoint in its own right: with only the walled approach the room is sealed
        # rather than defended, and `PL9` refuses a wool no enemy can reach.
        {"id": "lane", "role": "piece", "rect": [2, -23, 3, 4], "surface": WORKS_SURFACE},
        # The quay is three fingers with the fleet's two creeks between them. A board
        # carrying a wool is about a third land and `G8`'s fill-ratio is where that is
        # measured, so the void here is the instrument rather than what was left over.
        # blocks x[-10,10] z[-75,-20] — the centre finger, which the beacon stands on. It
        # straddles the symmetry axis, so a beacon on it faces its own image across the
        # middle: on a flanking finger the two beacons sit diagonally opposite and `GO3`
        # reads the walk between them at 201 against a band topping out at 150.
        {"id": "quay-c", "role": "piece", "rect": [-2, -15, 4, 11], "surface": QUAY_SURFACE},
        # blocks x[-35,-20] z[-75,-20] — the west finger. Fifteen blocks across, because
        # `FR9` holds a crossing to a frontline of fifteen and a finger is the whole of
        # the front the crossing onto it presents. It was widened outward rather than
        # inward so the creeks between the fingers keep their ten blocks of void.
        {"id": "quay-w", "role": "piece", "rect": [-7, -15, 3, 11], "surface": QUAY_SURFACE},
        # blocks x[20,35] z[-75,-20] — the east finger, which reaches the spur and not the
        # works, so a player coming up it has not walked round the wall's end
        {"id": "quay-e", "role": "piece", "rect": [4, -15, 3, 11], "surface": QUAY_SURFACE},
        # blocks x[-40,-20] z[-115,-95] — the spawn hall at the works' west end
        {"id": "spawn", "role": "spawn", "rect": [-8, -23, 4, 4], "surface": WORKS_SURFACE},
        # blocks x[25,45] z[-115,-95] — the cellar in the board's own corner: void north and
        # void east, so a defender holds two lines and an attacker picks between two.
        #
        # It is what sets the board's width, and that is the answer `G8` wanted. Widening
        # the flanking fingers to the fifteen blocks `FR9` holds a crossing to took the
        # fill ratio to 0.571 against a band topping out at 0.542, and every way of paying
        # for it out of the pieces cost a journey: a shorter finger widens the strait past
        # `CT12`'s forty, a narrower terrace chokes the spawn's own way out. The ratio is
        # land over the board's own box, so moving the cellar five blocks further into its
        # corner takes the box to ninety and the ratio to 0.517 with no ground given up.
        {"id": "cellar", "role": "wool-room", "rect": [5, -23, 4, 4], "surface": WORKS_SURFACE},
    ],
    "zones": [
        # One crossing per finger, each docking ground on both sides of the middle
        {"id": "fleet-c", "rect": [-2, -4, 4, 8], "holes": []},
        {"id": "fleet-w", "rect": [-7, -4, 3, 8], "holes": []},
        {"id": "fleet-e", "rect": [4, -4, 3, 8], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [10, 10], "facing": "back",
             "footprint": [3, 4, 14, 8]},
        ],
        # block (30, -105): at the end of the spur, three faces on void
        # no colour stated: the team's first wool takes its own team colour, and naming one
        # gives both images of the marker the same dye (RQ5)
        "wools": [{"id": "wool-1", "piece": "cellar", "at": [10, 10]}],
        "iron": [{"id": "iron-1", "piece": "spawn", "at": [10, 16]}],
        # block (-4, -61): forward on the centre finger, a short walk from its own spawn
        # and most of the board from the enemy's
        "destroyables": [
            {"id": "destroyable-1", "piece": "quay-c", "at": [6, 14],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "Tallowfleet Beacon"},
        ],
        "cores": [],
    },
    # One wall, on one interface, and not on the cellar's own: the spur's outer interface is
    # where it meets the works, twenty blocks out from the room. It spans the whole of that
    # interface, so there is no shoulder beside it to walk round.
    "walls": [{"a": "spur", "b": "works"}],
    "boxes": [],
}

# ── the themes ────────────────────────────────────────────────────────────────
# Three. The strand is the ground, the works is what was built on it, and the flats are the
# wet silt the tide leaves.
#
# This is the run's one grey board and it is where grey belongs: a gravel and andesite
# estuary under **Extreme hills** (`#8ab689`), a cool grey-green. The built family is warm
# spruce over stone brick, which is the reverse of the other three boards and is what keeps
# a building legible against a cold ground; the accent is white clay on the works' own face.
# The bands are cut against this board's own `incline`: 68.2% of the ground stands under
# 10°, 85.3% under 20°, and 0.9% at 40° or steeper. Written first as 28°/50° the face band
# painted nothing at all — the cut was above the whole population — and the shoulder carried
# the estuary. Twenty and thirty-two put the shoulder on the shingle bank's sides and bare
# stone only where the ground genuinely stands up.
STRAND_FLAT = depth(cells([GRAVEL, COARSE_DIRT], 11, 13), 1, solid(DIRT), 2)
STRAND_SHOULDER = depth(cells([GRAVEL, ANDESITE], 8, 23), 1, solid(GRAVEL), 2)
STRAND_FACE = depth(cells([STONE, COBBLE], 7, 29), 2, solid(STONE), 3)

themes = {
    "strand": theme(
        surface=slope(STRAND_FLAT, 20, STRAND_SHOULDER, 12, STRAND_FACE, 58),
        wall=depth(solid(GRAVEL), 1, solid(ANDESITE), 2, solid(STONE), 4),
        fill=voronoi([STONE, ANDESITE, DIORITE], 13, 5),
    ),
    # the works terrace: a laid stone floor, and a striped face where it retains the quay
    "works": theme(
        surface=depth(cells([STONE_BRICK, ANDESITE], 6, 37), 1, solid(STONE_BRICK), 2),
        wall={"kind": "wallRun", "runs": [
            {"material": solid(CHISELLED_BRICK), "thickness": 1},
            {"material": solid(STONE_BRICK), "thickness": 3},
            {"material": solid(WHITE_CLAY), "thickness": 1},
            {"material": solid(MOSSY_BRICK), "thickness": 1},
            {"material": solid(STONE_BRICK), "thickness": 3},
        ]},
        fill=voronoi([STONE, ANDESITE], 12, 19),
        rim=(1, solid(CHISELLED_BRICK)),
    ),
    # the tide flats: wet silt and shell, where the fleet leaves the quay
    "flats": theme(
        surface=depth(cells([CLAY, SAND], 9, 43), 1, solid(CLAY), 2),
        wall=depth(solid(CLAY), 1, solid(GRAVEL), 2, solid(STONE), 3),
        fill=voronoi([STONE, ANDESITE], 11, 31),
    ),
}

# ── the shapes ────────────────────────────────────────────────────────────────
# The works is made ground and comes out of the solve, so it keeps the height it was drawn at
# and meets the quay at a five-course face. Two flights state that face — one at each end of
# the terrace, because two objectives behind it means two journeys off it.
STEPS = depth(solid(STONE_BRICK), 1, solid(MOSSY_BRICK), 1, solid(STONE), 3)


def flight(name, x0, x1):
    return {
        "id": name, "type": "polygon", "operation": "add", "override": True,
        "keepClear": True, "floor": 0, "base_height": WORKS_SURFACE,
        "height_mode": "level", "skirt": 0, "material": STEPS,
        "vertices": [[x0, -83], [x1, -83], [x1, -67], [x0, -67]],
        "anchor_heights": [WORKS_SURFACE, WORKS_SURFACE, QUAY_SURFACE, QUAY_SURFACE],
    }


add_shapes = [
    flight("steps-c", -7, 1),
    flight("steps-w", -28, -22),
    flight("steps-e", 20, 28),
    # the tide flats, a splotch of wet silt where the fleet runs out over the quay. It states
    # the quay's own `base_height`: a patch drawn one course short of the ground under it
    # forms no surface and paints nothing at all.
    {"id": "flats-w", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": QUAY_SURFACE, "theme": "flats",
     "vertices": [[-9, -44], [4, -46], [9, -38], [6, -28], [-6, -26], [-9, -34]]},
    # The works' own sea wall, drawn as a polyline: the rasterizer splines its points before
    # offsetting the band, so five points read as a wall following the quay's edge.
    {"id": "sea-wall", "type": "polyline", "operation": "add", "keepClear": True,
     "floor": 0, "base_height": QUAY_SURFACE + 3, "theme": "works",
     "stroke_edge": "solid", "radius": 1,
     "vertices": [[-34, -78], [-20, -80], [-4, -78], [10, -80], [22, -78]]},
]

# ── the relief ────────────────────────────────────────────────────────────────
# Two long marks facing each other are what a fall is made of, and between them the quay is
# left to the solver. The monument's ground is pinned flat because an objective wants open
# ground round it, and the shingle bank is the one landform.
relief = {
    "team": {
        "base": QUAY_SURFACE,
        "reach": 0,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 14, "seed": 9},
        "marks": [
            # the hard standing at the foot of the works' face, where the flights land
            {"id": "hard", "kind": "area", "h": QUAY_SURFACE + 2, "bevel": 0,
             "ring": [[-35, -74], [35, -74], [35, -68], [-35, -68]]},
            # the beacon's own pan: level and open, which is what a goal wants round it
            {"id": "beacon-pan", "kind": "area", "h": QUAY_SURFACE + 1, "bevel": 2,
             "ring": [[-10, -68], [10, -68], [10, -54], [-10, -54]]},
            # the tide line, two courses lower, where an attacker lands off a crossing
            {"id": "tideline", "kind": "area", "h": QUAY_SURFACE - 2, "bevel": 0,
             "ring": [[-35, -30], [35, -30], [35, -20], [-35, -20]]},
        ],
        "pushes": [
            # The shingle bank the fleet piles across the centre finger, south of the
            # beacon: the one landform, and the height an attacker coming up the middle
            # climbs to look down on the pan. Skirt 5/8 = 0.63 a block against a crown of
            # 3/5 = 0.60, which is RL6 satisfied rather than approximately met.
            {"id": "shingle", "amount": 5, "falloff": 8, "crown": 3,
             "roughness": 0, "seed": 3,
             "ring": [[-8, -48], [4, -50], [9, -44], [7, -36], [-4, -34], [-9, -40]]},
        ],
    },
}

# ── the rooms ─────────────────────────────────────────────────────────────────
# Stated from the first pass, because a finish that states none stamps the studio's built-in
# bedrock box for both the spawn and the cellar — at 200, with no finding — and those are the
# two structures a player sees from the inside. Both wear the works' own family under a
# gambrel, which breaks on the way up and so rises further than a gable over the same span:
# a warehouse roof, which is what a tallow works has.
ROOM_WALL = {"stack": {"bands": [
    {"material": {"kind": "laidLog", "id": LOG, "data": 1}, "thickness": 1},
    {"material": solid(SPRUCE_PLANKS), "thickness": 3},
    {"material": solid(STONE_BRICK), "thickness": 4},
], "ending": "repeat"}, "extent": 8}


def room_shell(roof_body, door_width):
    return {
        "foundation": {
            "plate": {"stack": {"bands": [{"material": solid(STONE_BRICK), "thickness": 1}],
                                "ending": "repeat"}, "extent": 1},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": None,      # a footing over a one-course plate is a rim, not masonry
        },
        "roof": {
            "form": "gambrel", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": False,
            "body": solid(roof_body),
            "verge": {"kind": "laidLog", "id": LOG, "data": 1},
            "gable": solid(SPRUCE_PLANKS),
            "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
        },
        "wall": ROOM_WALL,
        "post": solid(SPRUCE_LOG),         # one wood for post, beams and the laid course
        "windows": {"form": "stairLattice", "block": SPRUCE_STAIRS, "hostBlock": -1,
                    "hostData": 0, "data": 0, "sill": 3, "width": 2, "height": 2,
                    "spacing": 4},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": LOG, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": SPRUCE_STAIRS, "fill": "upperSlab",
                             "fillBlock": SPRUCE_SLAB[0], "fillData": SPRUCE_SLAB[1]},
                    "width": door_width, "height": 4},
    }


# ── the buildings ─────────────────────────────────────────────────────────────
# Two plots of one style on the works, differing in height and footprint and in nothing
# else, which is a row rather than three ideas. Warm spruce over stone brick on a grey
# ground: a building is never the ground it stands on.
TRY_WORKS_SHELL = {
    **room_shell(SPRUCE_PLANKS, 2),
    "roof": {
        "form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": solid(OAK_PLANKS),
        "verge": {"kind": "laidLog", "id": LOG, "data": 1},
        "gable": solid(SPRUCE_PLANKS),
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "storeys": [{
        "clear": 4,
        "wall": {"stack": {"bands": [
            {"material": {"kind": "laidLog", "id": LOG, "data": 1}, "thickness": 1},
            {"material": solid(SPRUCE_PLANKS), "thickness": 3},
            {"material": solid(STONE_BRICK), "thickness": 3},
        ], "ending": "repeat"}, "extent": 7},
        "post": solid(SPRUCE_LOG),
        "windows": {"form": "arched", "block": SPRUCE_STAIRS, "hostBlock": -1,
                    "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2,
                    "spacing": 4},
    }],
}

# ── the dressing ──────────────────────────────────────────────────────────────
# A path is solid and three colours a reader cannot quite tell apart. This ground is hard,
# so the track is gravel, andesite and cobblestone.
TRACK = cells([GRAVEL, ANDESITE, COBBLE], 3, 47, rise=0)

TREES = json.load(open(os.path.join(HERE, "trees.json")))
TREE_KEYS = {"willow-a": "showcase-r17-2", "birch-a": "showcase-r13-2",
             "oak-a": "showcase-r6-3", "olive-a": "showcase-r10-2"}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}


def rock(pid, x, z, size, seed, form="angular"):
    """An erratic in a dark clay, because this board's ground is already the stone palette.

    Stone, cobblestone and andesite is the palette that reads as rock over sand, grass and
    dirt, and it is exactly what the strand is cut from here — so a rock made of it has no
    silhouette and reads as a patch of the estuary standing up. `DR-TONE` names that and
    says to take the rock the other way on grey ground rather than to deepen the grey. Dark
    clay over one cobble accent is a mass carried here and left, which is what an erratic is.
    """
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "layer": "ground",
            "form": form, "size": size, "mossy": False, "seed": seed,
            "rock": cells([BLACK_CLAY, BROWN_CLAY, COBBLE], 5, seed + 90, rise=4)}


def tryworks(pid, x0, z0, x1, z1, seed, storeys_high=0):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground",
            "style": "tryworks", "front": "posZ",
            "wings": [{"corners": [[x0, z0], [x1, z1]],
                       "spec": {"ridge": "alongX", "storeysHigh": storeys_high}}]}


dressing = {
    "styles": {
        "tryworks": {"kind": "house", "shell": TRY_WORKS_SHELL},
        **{key: TREES[name] for key, name in TREE_KEYS.items()},
    },
    "props": [
        # The fleet: a tidal channel across the works terrace. It names its layer, states no
        # level because the terrace is ground that is already there, and keeps its run
        # level, because a channel carried down a fall is trenched by the fall's whole
        # height. Its east end stops eight blocks short of the centre flight's head: the
        # flight is `keepClear` and cuts its own column, so a channel reaching it leaves the
        # water standing against an open face — `DR-DRY`, which counts a column the board
        # drew and then left open and passes over the void at the rim.
        {"id": "fleet", "kind": "water", "seed": 61, "layer": "ground",
         "shape": "channel", "form": "canal",
         "points": [[-32, -91], [-24, -88], [-16, -88], [-8, -90]],
         "radius": 3, "depth": 3, "shore": 2, "shoreWander": True, "edge": 1,
         "bank": cells([GRAVEL, CLAY, SAND], 6, 71, rise=3)},

        # the two journeys, drawn before the scenery: the spawn door to the beacon by the
        # west steps, and the spawn door to the cellar along the works
        {"id": "trod-beacon", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[-30, -100], [-24, -92], [-14, -80], [-6, -74], [-4, -68]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},
        {"id": "trod-cellar", "kind": "stroke", "seed": 6, "layer": "ground",
         "points": [[-26, -98], [-10, -94], [4, -92], [16, -98], [28, -104]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},

        # The try-works, two plots of one style. Both corners came off
        # `POST …/sketch/seats?kind=house&width=&depth=` rather than off the terrace's
        # middle: a 10 x 8 footprint has 34 legal cells on this whole board and not one of
        # them is on the spur, because the cellar's room, the defence wall and the east
        # finger's own edge take it between them. An 8 x 6 has two, and this is one.
        tryworks("tryhouse-works", 1, -86, 8, -81, 311, storeys_high=0),
        tryworks("tryhouse-quay", 0, -50, 9, -43, 312, storeys_high=1),

        # trees to the outside of the quay, never on the beacon's pan and never on the tide
        # line an attacker lands on
        tree("salt-1", "willow-a", -25, -62),
        tree("salt-2", "birch-a", -25, -45),
        tree("salt-3", "oak-a", 25, -62),
        # Deep inside a seat block rather than on its edge: a placement names where the
        # recipe is seated and a copied tree's foot is several cells across, so the cell it
        # comes to rest on is not the cell asked for. This one asked for (-19, -77), rested
        # on (-16, -76) and came back `DR-ROAD`. The spur's south end is eleven cells of
        # seat across and six deep, which is margin rather than a guess.
        tree("salt-4", "olive-a", 32, -78),
        tree("salt-5", "oak-a", -6, -40),

        # One erratic on each flanking finger and one on the centre, all of them off the
        # shingle: the bank's skirt runs to 33° and the strand's own paint calls anything
        # from 30° a face, so a rock on it is half-buried in the band that was meant to
        # show bare rock.
        rock("erratic-1", -26, -52, 2, 21),
        rock("erratic-2", 26, -50, 2, 22, form="round"),
        rock("erratic-3", -32, -38, 2, 23, form="cairn"),

        # Ground cover over the team's own land, held off the tide line: the ground an
        # attacker lands on is fought over and wants reading at a glance.
        {"id": "sward", "kind": "flora", "seed": 9,
         "points": [[-35, -94], [40, -94], [40, -36], [-35, -36]],
         "spec": {"coverage": 0.20, "scale": 24, "octaves": 2,
                  "fernShare": 0.30, "flowerShare": 0.06, "flowerScale": 28,
                  "tallShare": 0.04}},
    ],
}

# ── the made layers ───────────────────────────────────────────────────────────
# The boiling house on the spur, where the dressing pass has no say. A house prop cannot
# stand here — the seat mask answers none on the spur at any size — and the spur is the
# whole of the walled approach to the cellar, so the one thing on it that an attacker has
# to go round is built out of layers instead.
#
# Three walls and a roof, open to the south, standing in the spur's north-east corner. It
# is east of the flight down to the finger, not over it: drawn across the flight's head, a
# transect at x 25 read BARRIER +6 and DROP -7 and never reached the flight at all. `kind: "made"` with a
# `part_of` keeps `SK10`'s pair walk and `SK11`'s reachability walk off it: a shed has no
# gap to lose and its roof is not a stair somebody forgot.
#
# The masonry is a **material** and not a theme. A wall two blocks thick has no column with
# ground on all eight sides, so the surface bucket paints none of them and the rim and the
# wall buckets carry the whole shape — `SK23`, which is right: a theme is a place and a
# shed's wall is a thing that was built.
SPUR_TOP = WORKS_SURFACE          # the spur's top block is WORKS_SURFACE - 1
BOIL_WALL_HEIGHT = 5
BOIL_MASONRY = depth(cells([STONE_BRICK, MOSSY_BRICK], 4, 53), 2, solid(STONE_BRICK), 3)

add_layers = [
    {"id": "boil-walls", "name": "boil-walls", "base_y": SPUR_TOP,
     "kind": "made", "part_of": "boil-house",
     "shapes": [
         {"id": "boil-w", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": BOIL_WALL_HEIGHT, "material": BOIL_MASONRY,
          "min_x": 29, "min_z": -93, "max_x": 30, "max_z": -84},
         {"id": "boil-e", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": BOIL_WALL_HEIGHT, "material": BOIL_MASONRY,
          "min_x": 38, "min_z": -93, "max_x": 39, "max_z": -84},
         {"id": "boil-n", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": BOIL_WALL_HEIGHT, "material": BOIL_MASONRY,
          "min_x": 29, "min_z": -93, "max_x": 39, "max_z": -92},
     ],
     "groups": [{"id": "boil-shell", "name": "boiling house shell", "mirrors": True,
                 "shapeIds": ["boil-w", "boil-e", "boil-n"]}]},
    # The roof sits on the walls' own top block plus one. One course lower and the slab is
    # absorbed by the layer beneath it.
    {"id": "boil-roof", "name": "boil-roof", "base_y": SPUR_TOP + BOIL_WALL_HEIGHT,
     "kind": "made", "part_of": "boil-house",
     "shapes": [
         {"id": "boil-lid", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 1, "material": depth(solid(SPRUCE_SLAB), 1, solid(SPRUCE_PLANKS), 2),
          "min_x": 28, "min_z": -94, "max_x": 40, "max_z": -83},
     ],
     "groups": [{"id": "boil-lid-group", "name": "boiling house roof", "mirrors": True,
                 "shapeIds": ["boil-lid"]}]},
]


finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    # Extreme hills, #8ab689 — a cool grey-green over a gravel estuary
    "biome": {"kind": "solid", "id": 3},
    "roomStyles": {"spawn": room_shell(SPRUCE_PLANKS, 3),
                   "wool": room_shell(OAK_PLANKS, 2)},
    "mapTheme": "strand",
    "themes": themes,
    # Keyed on the compiled shape ids, read off POST /plan/compile: the compiler fuses the
    # pieces that share a height, so the three quay fingers are `cellar-10`, `-10-2` and
    # `-10-3`, and the works, the spur, the lane, the spawn and the cellar together are
    # `cellar-15`.
    "themeById": {"cellar-15": "works"},
    # The works tier is made ground and comes out of the solve, so it keeps the height it
    # was drawn at and meets the quay at a five-course face for the flights to state. Left
    # in the solve it settled to the quay's own level and the board built with no face on
    # it at all — `03-slopes.txt` read 0 barrier and 0 faces.
    "shapePropsById": {"cellar-15": {"relief_scope": "exclude"}},
    "addShapes": add_shapes,
    "addLayers": add_layers,
    "relief": relief,
    "dressing": dressing,
}


def write(name, document):
    path = os.path.join(HERE, name)
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
        handle.write("\n")
    print(f"wrote {path}")


write(f"{SLUG}.plan.json", plan)
write(f"{SLUG}.finish.json", finish)
