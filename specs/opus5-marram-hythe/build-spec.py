#!/usr/bin/env python3
"""Marram Hythe — three grounds in a stack, and the board is getting between them.

In one sentence: a destroy board on a shore where the monument stands on a
built quay, so an attack crosses an open strand, climbs a dune field it can
hide in, and has to get up a made face at the end — three grounds, and none of
them costs what the last one did.

The grounds, and the instrument each is stated by. Nothing here is a push:
the dunes are point marks with the relaxation between them, which is what
makes them read as blown rather than stamped.

  the strand   y9    an `area` mark scooped out of one ground, not a piece:
                     a piece at a lower surface meets the next along a straight
                     line the width of the board
  the links    y14+  four `point` marks at r5-8 and a `line` slack between
                     them, on a team relief with reach 0
  the bars     y10   a SECOND relief on the `neutral` group: its own base, its
                     own reach of 8, its own landform. Two grounds meeting
  the quay     y20   `relief_scope: "exclude"` with a base_height and no
                     height_mode, so the solve bends round it and the two
                     tiers meet at a face

And the joins, every one of them chosen:

  strand -> links   the stated five-block drop between two plan pieces, which
                    is what stops them merging into one shape
  strand -> quay    a ramp AGAINST the west face, parallel to it, with a
                    landing at the top to stand and turn on
  links  -> quay    two gates, 12 and 14 of run for 6, each set INTO a notch
                    cut to its own length rather than leaning on a straight wall
  strand -> links   a dune ramp out on the east flank, 12 for 5
  bar    -> strand  bridged by players, over a build zone the width of the bar
"""
import json, os, sys, math

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
import props  # the studio's own form emitters; a lighthouse is not a new subsystem

SLUG = "opus5-marram-hythe"
CELL = 4

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

SAND        = solid(12, 0)
SANDSTONE   = solid(24, 0)
SS_SMOOTH   = solid(24, 2)
GRASS       = solid(2, 0)
DIRT        = solid(3, 0)
COARSE_DIRT = solid(3, 1)
GRAVEL      = solid(13, 0)
STONE       = solid(1, 0)
ANDESITE    = solid(1, 5)
COBBLE      = solid(4, 0)
STONE_BRICK = solid(98, 0)
QUARTZ      = solid(155, 0)
CLAY_RED    = solid(159, 14)
CLAY_WHITE  = solid(159, 0)
CLAY        = solid(82, 0)
GLASS       = solid(20, 0)
GLOWSTONE   = solid(89, 0)
DARK_PLANK  = solid(5, 5)
DARK_LOG    = solid(162, 1)   # log2:1 is dark oak; 17:5 is spruce on its side
SPRUCE_LOG  = solid(17, 1)

def depth_stack(*pairs, beyond=SANDSTONE):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in pairs]}}

def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def ring(cx, cz, r, n=11, wobble=0.0, seed=1):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wobble * math.sin(seed * 1.7 + i * 2.3))
        out.append([round(cx + rr * math.cos(a)), round(cz + rr * math.sin(a))])
    return out

# ---------------------------------------------------------------- the plan
# Two levels and a five-block drop between them. The quay is NOT a piece: a
# piece is a room or a corridor, and made ground is a shape.
plan = {
    "plan": 2,
    "meta": {"name": "Marram Hythe"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 14,
                "surface": 9, "observerY": 74},
    "pieces": [
        # ONE ground. The beach is not a piece: a full-width piece at a lower
        # surface meets the one behind it along a straight line the width of
        # the board, and no amount of dressing repairs that. It is an `area`
        # mark inside this piece instead, and what lies between it and the
        # dunes is the relaxation.
        {"id": "shore", "role": "piece", "rect": [-11, -28, 22, 22], "surface": 16},
        {"id": "spawn", "role": "spawn", "rect": [-3, -28, 6, 3], "surface": 16},
        # One bar in the channel, wide, and its own rot_180 image. Two bars
        # facing each other across a gap enclose a rotation hole between the
        # frontline and the band, which CT9 bands at [0, 0].
        {"id": "bar", "role": "piece", "rect": [-7, -3, 14, 6],
         "surface": 10, "mirrors": False},
    ],
    "zones": [
        # Exactly the bar's width: a mid-board stepping stone is used only
        # across the width of the build zone that reaches it. The hop is 16
        # either side and the whole crossing 48 — G5 wants 10 to 20 for the
        # hop a route depends on, and 40 to 60 in total.
        {"id": "channel", "rect": [-7, -9, 14, 18], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [12, 6], "facing": "back",
             "footprint": [5, 2, 14, 8]},
        ],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [
            {"id": "destroyable-1", "piece": "shore", "at": [30, 50],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "Hythe Light"},
        ],
    },
    "walls": [], "boxes": [],
}

# ---------------------------------------------------------- the two reliefs
relief = {
    # The shore, as one ground. `base` is the HIGH value and `reach` is 0, so
    # the marks decide the whole surface and everything between them is the
    # relaxation running from one to the next. That is what makes a beach rise
    # into a dune field with no border in it anywhere.
    #
    # The grain is 0.7. A large amplitude is noise laid over the answer, and
    # it is the first thing that stops a solved surface reading as one place.
    "team": {
        "base": 16, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.7, "scale": 12, "seed": 29},
        "marks": [
            # The wet flat, pinned at the water: a strip along the coast
            # itself rather than the whole front. An area mark holds one
            # height everywhere inside its ring, so a ring drawn over the
            # whole beach is a beach with no shape in it — which is what
            # this was, twenty-four courses deep and level to the block.
            # The tide line, pinned as a LINE and not as an area. An area
            # mark holds one height over everything inside its ring and the
            # grain with it, so a ring drawn over the front is twenty-four
            # courses of ground level to the block — which is what this was.
            # A line pins the water's edge and nothing else, and the beach
            # behind it is relaxation with grain in it.
            {"id": "tide-line", "kind": "line", "r": 3, "tread": 2,
             "h": [9, 9, 9, 9, 9, 9, 9, 9, 9],
             "points": [[-44, -24], [-30, -28], [-22, -34], [-10, -30],
                        [0, -27], [12, -30], [22, -32], [34, -27], [44, -24]]},
            # The dune toe: the low ridge of blown sand a beach piles up
            # behind the tide line, so the ground climbs out of the water
            # before the marram starts. It runs the middle of the front
            # only — the ramp holds the west end and the cut bank the east,
            # and a mark laid across either would fight it.
            {"id": "dune-toe", "kind": "line", "r": 3, "tread": 2,
             "h": [13, 12, 13],
             "points": [[-34, -45], [-20, -43], [-8, -45]]},
            # And three hummocks standing out of the strand between the two,
            # which is the only thing that keeps fifteen courses of relaxed
            # ground from solving level to the block. Small radii: a point
            # mark pins a flat disc, so a wide one is a table.
            {"id": "hump-w", "kind": "point", "at": [-36, -36], "r": 5, "h": 11},
            {"id": "hump-m", "kind": "point", "at": [-14, -40], "r": 4, "h": 11},
            {"id": "hump-e", "kind": "point", "at": [16, -38], "r": 5, "h": 11},
            # Kept clear of every dune: two marks that touch pin their bands
            # exactly, and the whole difference between them lands in one cell
            # (RL3). What is between them instead is the relaxation.
            {"id": "links-apron", "kind": "area", "h": 16, "bevel": 3,
             "ring": ring(0, -102, 16, 9, 0.12, 3)},
            # The dunes: small radii with the relaxation between them. A point
            # mark pins a flat disc, so a large one is a mesa and not a summit.
            {"id": "dune-1", "kind": "point", "at": [-30, -88], "r": 7, "h": 20},
            {"id": "dune-2", "kind": "point", "at": [-8, -76], "r": 6, "h": 23},
            {"id": "dune-3", "kind": "point", "at": [24, -88], "r": 8, "h": 19},
            {"id": "dune-4", "kind": "point", "at": [34, -68], "r": 5, "h": 22},
            {"id": "slack", "kind": "line", "r": 7, "tread": 3,
             "h": [14, 13, 13, 14],
             "points": [[-42, -74], [-20, -70], [4, -72], [26, -64]]},
            # And ONE stretch of it that does not flow: a cut bank where the
            # sea has been at the dunes, traced east to west so the high band
            # lands landward. It runs the east half only — west of it the
            # beach climbs its own berm and the berm relaxes into the dunes,
            # with no mark on the seam at all. Not everything on a board
            # meets the same way.
            {"id": "cut-bank", "kind": "scarp", "high": 17, "low": 9,
             "face": 3, "band": 3,
             "points": [[44, -44], [34, -49], [24, -45], [14, -50],
                        [6, -46], [0, -49]]},
        ],
        "pushes": [],
    },
    # The bar. A second ground with its own base, its own reach and its own
    # landform, so the channel reads as a different place rather than as more
    # of the shore's field.
    "neutral": {
        "base": 10, "reach": 8, "step": 1, "landform": "plain",
        "grain": {"amplitude": 0.6, "scale": 10, "seed": 5},
        "marks": [
            {"id": "bar-flat", "kind": "area", "h": 10, "bevel": 3,
             "ring": ring(-21, 0, 7, 10, 0.18, 7)},
            # The light's own ground, flat: a made thing states an absolute
            # floor and ground the relief moved under it would bury or float
            # the plinth.
            {"id": "light-pad", "kind": "area", "h": 12, "bevel": 2,
             "ring": ring(0, 0, 11, 11, 0.10, 3)},
            {"id": "bar-knap", "kind": "point", "at": [21, 0], "r": 5, "h": 14},
        ],
        "pushes": [],
    },
}

# ------------------------------------------------------- the made ground
# `relief_scope: "exclude"` with a base_height and NO height_mode. exclude
# takes the footprint out of the solve, so the land is whatever that outline
# would have produced and the quay keeps its own height: the two tiers meet at
# a face. `hold` would let the relief bring the lower tier up to it, and then
# there is no step and no reason for a stair.
#
# The landward edge is notched twice, and each notch is cut to exactly the
# flight that fills it — 12 blocks for the west gate and 14 for the east — so
# a stair is set INTO the wall rather than leaning on it. A retaining wall is
# straight where it is a wall and interesting where it is a gate.
quay = {
    "id": "quay", "type": "polygon", "operation": "add",
    "relief_scope": "exclude", "base_height": 20, "floor": 0,
    "keepClear": True, "theme": "quay",
    # No notches. A flight set INTO a platform is a hole in the platform, and
    # the houses that went in the notches were standing in the stairwells.
    # The way up runs along the OUTSIDE of the west face instead.
    "vertices": [
        [-38, -48], [10, -48], [10, -78], [-38, -78],
    ],
}

def flight(fid, verts, anchors, material=STONE_BRICK):
    """A flight is a thing somebody built, so it carries a material rather than
    a theme, keeps the dressing off itself, and runs at least twice its rise."""
    return {"id": fid, "type": "polygon", "operation": "add", "override": True,
            "height_mode": "level", "skirt": 0, "floor": 0, "keepClear": True,
            "vertices": verts, "anchor_heights": anchors, "material": material}

flights = [
    # The way onto the quay: a ramp AGAINST its west face, on the strip of
    # ground between the platform and the coast, running parallel to it for
    # 22 blocks and rising 10. Nothing is cut into the platform.
    flight("quay-ramp", [[-44, -50], [-38, -50], [-38, -72], [-44, -72]],
           [10, 10, 20, 20]),
    # And the landing at the top of it: six blocks of flat, level with the
    # quay, so a player arriving has somewhere to stand and turn rather than
    # stepping off a slope straight onto a platform.
    flight("quay-landing", [[-44, -72], [-38, -72], [-38, -78], [-44, -78]],
           [20, 20, 20, 20]),
    # The other way up the board, out on the east flank and away from the
    # quay entirely: strand to links.
    flight("dune-ramp", [[24, -58], [34, -58], [34, -42], [24, -42]],
           [17, 17, 9, 9], material=SS_SMOOTH),
]


# THE BEACH AND ITS FORESHORE. Two shapes over the whole front of the island,
# the second inside the first, so the ground reads out from the water in
# bands: wet gravel at the edge, dry sand behind it, marram behind that.
#
# `base_height` matches the island's own, which is what makes the paint land.
# A shape only owns the theme on a cell it FORMS the surface of; one stated
# lower than the ground it lies on runs under it, forms nothing, and paints
# nothing at all. Flush with the island and smaller in area, it wins the cell.
#
# And NO `relief_scope`. A shape that states one is a statement about height:
# `follow` seats the shape on the solved field and then pins its whole ring
# there RIGID, which over a footprint this size is a floor — the strand came
# out level to the block and every mark inside it was overwritten. Stating
# nothing leaves the shape as ordinary ground of the group, which is what a
# beach is: the marks shape it and the theme says what it is made of.
#
# The outlines trace the island's own coast vertex for vertex, so the beach
# reaches the water everywhere along it rather than stopping short in grass.
COAST = [[-44, -24], [-30, -28], [-22, -34], [-10, -30], [0, -27],
         [12, -30], [22, -32], [34, -27], [44, -24]]

beach = {
    "id": "beach", "type": "polygon", "operation": "add",
    "base_height": 16, "floor": 0,
    "theme": "strand",
    "vertices": COAST + [[44, -43], [32, -45], [22, -42], [10, -46],
                         [-2, -43], [-14, -48], [-28, -44], [-44, -47]],
}

foreshore = {
    "id": "foreshore", "type": "polygon", "operation": "add",
    "base_height": 16, "floor": 0,
    "theme": "foreshore",
    "vertices": COAST + [[44, -28], [32, -32], [22, -37], [10, -35],
                         [0, -32], [-10, -35], [-22, -39], [-32, -33],
                         [-44, -28]],
}

# --------------------------------------------------------- the lighthouse
# On the bar, dead centre of the board, which is where a light belongs: it is
# the thing both teams cross toward and the one landmark neither owns.
#
# Built rather than assembled. props.py's emitters are primitives, not a
# lighthouse — the shape of one is a splayed plinth, a banded shaft, a
# colonnade carrying an overhanging gallery, a glazed lantern and a cap, and
# every one of those is a ring or a disc at its own floor. A column up the
# shaft crosses white, red, white, red, so each band is its own layer: a
# colour change splits a run as surely as air does.
LIGHT = (0, 0)
GROUND = 12                       # the bar, pinned flat under it

def made_layer(lid, shapes, material, part="lighthouse", mirrors=False):
    """One material rather than a theme, stamped onto every shape: a made
    thing is drawn as terrain and made of one thing, and a shape carrying
    neither takes the map default — which builds a lighthouse out of grass."""
    for shape in shapes:
        shape["material"] = material
    return {"id": lid, "name": lid.replace("-", " "), "base_y": 0,
            "kind": "made", "part_of": part, "shapes": shapes,
            "groups": [{"id": f"{lid}-body", "name": lid,
                        "mirrors": mirrors,
                        "shapeIds": [x["id"] for x in shapes]}]}

def disc(sid, cx, cz, r, floor, height):
    return {"id": sid, "type": "circle", "center_x": cx, "center_z": cz,
            "radius": r, "floor": floor, "base_height": height,
            "operation": "add", "keepClear": True}

def ringwall(sid, cx, cz, r, thickness, floor, height, points=48):
    """A hollow ring as ONE even-odd polygon: the outer circle, a slit inward,
    the inner circle the other way round, and the slit's two edges cancel. An
    outer circle minus an inner one is a `subtract`, and SK13 reads a subtract
    as the board's negative space and refuses any add that fills it."""
    return {"id": sid, "type": "polygon", "operation": "add",
            "floor": floor, "base_height": height, "keepClear": True,
            "vertices": props.annulus(cx, cz, r, r, thickness, points)}

lighthouse = []

# The splayed plinth it stands on: two drums, the lower wider.
lighthouse.append(made_layer("lh-plinth", [
    disc("lh-plinth-0", *LIGHT, 10, GROUND, 2),
    disc("lh-plinth-1", *LIGHT, 8, GROUND, 4),
], STONE_BRICK))

# Stilts. Eight legs standing off the plinth, so the shaft rises out of a
# frame rather than off a slab — and a boat could be drawn under them.
STILT = []
for i in range(8):
    a = 2 * math.pi * i / 8
    STILT.append(disc(f"lh-stilt-{i}", round(LIGHT[0] + 7 * math.cos(a)),
                      round(LIGHT[1] + 7 * math.sin(a)), 1, GROUND + 4, 4))
lighthouse.append(made_layer("lh-stilts", STILT, DARK_LOG))

# The shaft: six bands, white and red, tapering 6 to 4. Each band is its own
# layer because a layer holds one span per column and these share every one.
BANDS = [(QUARTZ, "white"), (CLAY_RED, "red")] * 3
shaft_floor = GROUND + 8
for i, (mat, name) in enumerate(BANDS):
    r = 6 - (i * 2.0) / len(BANDS)
    lighthouse.append(made_layer(
        f"lh-band-{i}",
        [ringwall(f"lh-band-{i}-w", *LIGHT, r, 2, shaft_floor + i * 4, 4)],
        mat))

# A colonnade carrying the gallery, so it overhangs on posts rather than
# corbelling out of nothing.
gallery_floor = shaft_floor + len(BANDS) * 4
POSTS = []
for i in range(8):
    a = 2 * math.pi * i / 8 + math.pi / 8
    POSTS.append(disc(f"lh-post-{i}", round(LIGHT[0] + 5 * math.cos(a)),
                      round(LIGHT[1] + 5 * math.sin(a)), 1, gallery_floor - 3, 3))
lighthouse.append(made_layer("lh-colonnade", POSTS, DARK_LOG))

# The gallery: a disc that oversails the shaft, and a parapet ring on it.
lighthouse.append(made_layer("lh-gallery", [
    disc("lh-gallery-0", *LIGHT, 6, gallery_floor, 1),
], STONE_BRICK))
lighthouse.append(made_layer("lh-rail", [
    ringwall("lh-rail-0", *LIGHT, 6, 1, gallery_floor + 1, 1),
], DARK_LOG))

# The lantern: a glazed drum, and the light itself standing in it.
lighthouse.append(made_layer("lh-lantern", [
    ringwall("lh-lantern-0", *LIGHT, 4, 1, gallery_floor + 2, 4),
], GLASS))
lighthouse.append(made_layer("lh-lamp", [
    disc("lh-lamp-0", *LIGHT, 1, gallery_floor + 3, 2),
], GLOWSTONE))

# And the cap: a dome, which is the one thing the emitter does better by hand.
cap = props.dome("lh-cap", LIGHT[0], LIGHT[1], radius=4,
                 floor=gallery_floor + 6, theme=None, squash=0.7,
                 name="Light cap", mirrors=False)
cap_inner = cap.pop("layout")
cap["shapes"] = cap_inner["shapes"]
cap["groups"] = cap_inner["groups"]
cap["kind"] = "made"
cap["part_of"] = "lighthouse"
for shape in cap["shapes"]:
    shape.pop("theme", None)
    shape["material"] = CLAY_RED
lighthouse.append(cap)

# ---------------------------------------------------------------- themes
# Three, and three tone families named before any of them was written:
# GROUND is sand and marram, BUILT is stone brick and dark oak, and the ACCENT
# is the team tint, which appears on the quay's own face and nowhere else.
links_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    # OFF on terrain faces. The wall bucket paints every exposed riser, and a
    # dune field with grain in it is nothing but small risers — turned on, it
    # lays a brown web of sandstone across the marram. A dune's face is the
    # surface stack's steep band, which is what the slope axis is for.
    "wallOnTerrainFaces": False,
    # The rim is off too: this ground is relief-solved, and a rim caps every
    # fall with a band, which turns a dune field into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": SANDSTONE},
    # Finished by angle. Marram holds the flat and the shoulder of a dune; the
    # steep face of one is bare blown sand, and the slope axis is the only
    # thing on the board that knows the difference.
    # Sand is a SURFACE fact. Dune sand lies on the steep faces and blows a
    # course or two over the flats; what is under all of it is soil and then
    # rock. A stack that hands over to sandstone at every angle is a board
    # made of sand to bedrock, which no shore is.
    "surface": {"enabled": True, "depth": 6, "material": slope_stack(
        (depth_stack((GRASS, 1), (DIRT, 3), (COARSE_DIRT, 2), beyond=STONE), 16),
        (depth_stack((COARSE_DIRT, 1), (SAND, 1), (DIRT, 3), beyond=STONE), 18),
        (depth_stack((SAND, 3), (SANDSTONE, 2), beyond=STONE), 56),
    )},
    # A NOISE between two near shades, with a `rise`. Without a rise every
    # area pattern samples the plane, so a column resolves to one block and
    # the field reads as bands down a cut face — which is a wall run wearing a
    # pattern's name. With one it is a volume, and a dune face reads as sand
    # with grain in it rather than as stratified rock.
    # Banded on the HEIGHT axis, which is the one that can say what is deep.
    # A cut face of sand and sandstone top to bottom is a board made of sand;
    # the bottom nine courses are stone, then sandstone, then the sand that
    # actually belongs at the surface.
    "wall": {"kind": "layered", "axis": "height", "beyond": STONE,
             "stack": {"ending": "handOver", "bands": [
                 {"material": {"kind": "noise", "seed": 61, "scale": 10,
                               "octaves": 2, "rise": 6,
                               "stops": [STONE, ANDESITE]}, "thickness": 9},
                 {"material": {"kind": "noise", "seed": 62, "scale": 9,
                               "octaves": 2, "rise": 5,
                               "stops": [SANDSTONE, STONE]}, "thickness": 5},
                 {"material": {"kind": "noise", "seed": 63, "scale": 8,
                               "octaves": 2, "rise": 5,
                               "stops": [SAND, SANDSTONE]}, "thickness": 12},
             ]}},
    "wallEnabled": True,
    # A voronoi is never ground: it goes in the fill, in STONE, where it is the
    # body of the rock nobody sees until a face is cut.
    "fill": {"kind": "voronoi", "seed": 41, "cellSize": 13, "rise": 6,
             "bands": [{"material": STONE, "depth": 3},
                       {"material": ANDESITE, "depth": 1}]},
}

strand_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    # A beach IS sand a long way down, and then it is rock like everywhere
    # else. Five courses of it, handing over to sandstone, over a stone fill.
    "surface": {"enabled": True, "depth": 5, "material": depth_stack(
        (GRAVEL, 1), (SAND, 4), beyond=SANDSTONE)},
    "wall": {"kind": "layered", "axis": "height", "beyond": STONE,
             "stack": {"ending": "handOver", "bands": [
                 {"material": {"kind": "noise", "seed": 64, "scale": 10,
                               "octaves": 2, "rise": 6,
                               "stops": [STONE, ANDESITE]}, "thickness": 9},
                 {"material": {"kind": "noise", "seed": 65, "scale": 9,
                               "octaves": 2, "rise": 5,
                               "stops": [SANDSTONE, STONE]}, "thickness": 5},
                 {"material": {"kind": "noise", "seed": 66, "scale": 8,
                               "octaves": 2, "rise": 5,
                               "stops": [SAND, SANDSTONE]}, "thickness": 12},
             ]}},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 43, "cellSize": 12, "rise": 6,
             "bands": [{"material": STONE, "depth": 3},
                       {"material": ANDESITE, "depth": 1}]},
}

# The tide line. Sand that the sea is still reaching: gravel and clay laid
# through the sand in a cell field, so the band reads as wet ground rather
# than as a second flat colour. It is the one thing on the board that says
# where the water is, on a map whose water is the void between the islands.
foreshore_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 4, "material": depth_stack(
        ({"kind": "cell", "seed": 57, "cellSize": 5, "jitter": 2, "warp": 2,
          "rise": 2, "palette": [GRAVEL, SAND, CLAY, GRAVEL]}, 1),
        (SAND, 3), beyond=SANDSTONE)},
    "wall": {"kind": "layered", "axis": "height", "beyond": STONE,
             "stack": {"ending": "handOver", "bands": [
                 {"material": {"kind": "noise", "seed": 67, "scale": 10,
                               "octaves": 2, "rise": 6,
                               "stops": [STONE, ANDESITE]}, "thickness": 9},
                 {"material": {"kind": "noise", "seed": 68, "scale": 9,
                               "octaves": 2, "rise": 5,
                               "stops": [SANDSTONE, STONE]}, "thickness": 5},
                 {"material": {"kind": "noise", "seed": 69, "scale": 8,
                               "octaves": 2, "rise": 4,
                               "stops": [GRAVEL, SANDSTONE]}, "thickness": 12},
             ]}},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 44, "cellSize": 12, "rise": 6,
             "bands": [{"material": STONE, "depth": 3},
                       {"material": ANDESITE, "depth": 1}]},
}

quay_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "boundary",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONE_BRICK},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        ({"kind": "cell", "seed": 53, "cellSize": 11, "jitter": 3, "warp": 2,
          "rise": 3, "palette": [STONE_BRICK, COBBLE, SS_SMOOTH]}, 1),
        (COBBLE, 2), beyond=STONE)},
    # The made ground's face is where its paint goes. A wallDiagonal shears the
    # stripes by height so they climb the wall at a slope, and nothing sampled
    # from the plane can reach this surface at all. The teamTint run is what
    # lets a player read whose quay they are looking at from the far bank.
    "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
        {"material": COBBLE, "width": 3},
        {"material": STONE_BRICK, "width": 1},
        {"material": {"kind": "teamTint", "blockId": 159,
                      "neutral": SS_SMOOTH}, "width": 1},
        {"material": STONE, "width": 2},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 47, "cellSize": 12, "rise": 7,
             "bands": [{"material": STONE, "depth": 3},
                       {"material": COBBLE, "depth": 1}]},
}

# --------------------------------------------------------------- the shell
# Forked from the shipped longhouse. No footing — over the one-course plate a
# board gives it, a footing is a plinth nobody drew. The walls leave the
# ground's family: sand and marram outside, stone brick and dark oak in.
spawn_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONE_BRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 2},
        "surface": {"field": None, "border": None, "borderWidth": 1,
                    "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARK_PLANK, "verge": solid(5, 1), "gable": solid(5, 1),
             "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 2, "width": 2,
                              "height": 2, "spacing": 3}},
    "wall": {"stack": {"bands": [
        {"material": STONE_BRICK, "thickness": 2},
        {"material": DARK_PLANK, "thickness": 4},
    ], "ending": "repeat"}, "extent": 6},
    # A log is a post or a beam, and a wall is neither. Posts at the corners
    # are what make a house read as framed.
    "post": DARK_LOG,
    # 164 is dark oak stairs, to the wall's dark oak. A window and its host
    # are one opening, so they are cut from one material (HS4).
    "windows": {"form": "arched", "block": 164, "hostBlock": 5, "hostData": 5,
                "data": 0, "sill": 4, "width": 2, "height": 2, "spacing": 2},
    "storeys": [], "porch": None, "front": None,
    "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air", "head": {"form": "arched", "block": 164,
                "fill": "upperSlab", "fillBlock": 126, "fillData": 5},
                "width": 3, "height": 4},
}

# ---------------------------------------------------------------- dressing
# The trees are bodies cut out of showcase/tree-showcase with
# `tools/trees.py bodies`, so they are hand-built trees rather than the
# vanilla stamp. None stands within 20 blocks of the monument: OB19's ring
# stops at ten, and a fifteen-block crown beside a goal floating four is still
# the defender's problem.
trees = json.load(open(os.path.join(D, "trees.json")))
tree_styles = {k: {"kind": "tree", "form": "copied", "body": v["body"]}
               for k, v in trees.items()}

# `cell` takes `palette`, and `jitter` and `warp` are required. `entries` is
# not a field the studio reads: inside a snapshot it is dropped in silence and
# the pattern renders as a flat swatch, and in a surface bucket the theme gate
# throws on the null and answers RQ2 — a 500 — rather than naming it.
PAVE = {"kind": "cell", "seed": 19, "cellSize": 9, "jitter": 3, "warp": 2,
        "rise": 4, "palette": [GRAVEL, ANDESITE, COBBLE]}

# A quay shed is not a cottage. It is low and wide, it sits on the stone it
# is built on rather than on a plinth, its roof is a shallow HIP rather than
# a gable so it reads as a shed from every side, and its walls are tarred
# board over a stone base with the posts standing proud at the corners.
quay_shell = {
    "kind": "house",
    "shell": {
        "foundation": {
            # One course, flush with the platform: a shed on a quay stands on
            # the quay. No footing — over a one-course plate it is a rim
            # round a building with no foundation to speak of.
            "plate": {"stack": {"bands": [{"material": STONE_BRICK, "thickness": 1}],
                                "ending": "repeat"}, "extent": 0},
            "surface": {"field": None, "border": None, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": True},
            "footing": None,
        },
        "roof": {"form": "hip", "pitch": 1, "slab": -1, "slabData": 0,
                 "overhang": 1, "ridgeCap": True, "hole": False,
                 "body": DARK_PLANK, "verge": DARK_PLANK, "gable": DARK_PLANK,
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                                  "hostData": 0, "data": 0, "sill": 2,
                                  "width": 2, "height": 2, "spacing": 3}},
        # Stone to the sill, board above — which is how a store beside water
        # is built, and it ties the shed to the platform under it.
        "wall": {"stack": {"bands": [
            {"material": COBBLE, "thickness": 2},
            {"material": DARK_PLANK, "thickness": 3},
        ], "ending": "repeat"}, "extent": 5},
        "post": DARK_LOG,
        # Wide, low openings: a store takes cargo, not daylight.
        # slabBanded raises half a cube for the sill and lowers half for the
        # lintel, so its block has to be a single slab — 126:5 is dark oak.
        "windows": {"form": "slabBanded", "block": 126, "hostBlock": 5,
                    "hostData": 5, "data": 5, "sill": 2, "width": 2,
                    "height": 1, "spacing": 4},
        "storeys": [], "porch": None, "front": None,
        "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 164,
                    "fill": "upperSlab", "fillBlock": 126, "fillData": 5},
                    "width": 3, "height": 3},
    },
}

dressing_props = [
    # Two sheds on the quay: one style, two plots, differing in height and
    # footprint and in nothing else. Three styles would be three ideas.
    # Two sheds ON the quay — one style, two plots, differing in height and
    # footprint and in nothing else. Both stand well inside the platform's
    # own edges and clear of the goal's clearance.
    {"id": "net-store", "kind": "house", "seed": 21, "front": "posZ",
     "style": "quay-shed", "wings": [{"corners": [[-34, -74], [-26, -67]]}]},
    {"id": "warehouse", "kind": "house", "seed": 22, "front": "posZ",
     "style": "quay-shed", "wings": [{"corners": [[0, -76], [7, -67]]}]},
    # A path is a claim about circulation, so it runs from the spawn door to
    # the west gate and stops there, at a door, rather than ending nowhere.
    {"id": "quay-road", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 11, "pave": PAVE,
     "points": [[0, -98], [-14, -90], [-30, -84], [-40, -76], [-41, -62]]},
    # Scrub on the dune crests, pines in the slacks where there is shelter.
    {"id": "scrub-a", "kind": "tree", "seed": 700, "x": -34, "z": -92, "style": "scrub-1"},
    {"id": "scrub-b", "kind": "tree", "seed": 701, "x": -26, "z": -92, "style": "scrub-2"},
    {"id": "scrub-c", "kind": "tree", "seed": 702, "x": 24,  "z": -94, "style": "scrub-3"},
    {"id": "scrub-d", "kind": "tree", "seed": 703, "x": 36,  "z": -76, "style": "scrub-1"},
    {"id": "pine-a",  "kind": "tree", "seed": 710, "x": -42, "z": -90, "style": "pine-1"},
    {"id": "pine-b",  "kind": "tree", "seed": 711, "x": 16,  "z": -84, "style": "pine-2"},
    {"id": "pine-c",  "kind": "tree", "seed": 712, "x": 36,  "z": -60, "style": "pine-4"},
    {"id": "pine-d",  "kind": "tree", "seed": 713, "x": 30,  "z": -60, "style": "pine-5"},
    # A boulder is stone, and these are the ones the tide left on the strand.
    {"id": "skerry-0", "kind": "boulder", "x": -30, "z": -36, "seed": 61, "radius": 3},
    {"id": "skerry-1", "kind": "boulder", "x": 14,  "z": -40, "seed": 62, "radius": 2},
    {"id": "skerry-2", "kind": "boulder", "x": 38,  "z": -28, "seed": 63, "radius": 3},
    # Ground cover is ONE shape over the whole board, and the density field
    # does the patchiness. Both gameplay numbers stay low: high coverage is
    # ground a player cannot read, and tall grass is cover nobody authored.
    {"id": "marram", "kind": "flora", "seed": 9,
     "points": [[-44, -104], [44, -104], [44, -14], [0, -12], [-44, -14]],
     "spec": {"coverage": 0.22, "scale": 25, "octaves": 2, "fernShare": 0.15,
              "flowerShare": 0.05, "flowerScale": 14, "tallShare": 0.04}},
]

finish = {
    "created": "2026-09-13",
    "authors": ["Opus 5"],
    "themes": {"links": links_theme, "strand": strand_theme,
               "foreshore": foreshore_theme, "quay": quay_theme},
    "mapTheme": "links",
    "addShapes": [quay] + flights + [beach, foreshore],
    "addLayers": lighthouse,
    # The compiled ground is a rectangle, which is the board's shape and not
    # its coast. Seven of the eight boards this one was measured against
    # reshape theirs per vertex; none bends. `after` inserts on the edge
    # LEAVING that vertex and the indices move under it, so these are counted
    # in order: two corner moves, two inserts that cut the back corners off as
    # triangles, then three that give the frontline a shape instead of a line.
    "editShapes": {
        "shore-16": [
            {"index": 0, "x": -24, "z": -112},
            {"index": 1, "x": 24, "z": -112},
            {"after": 1, "x": 44, "z": -92},
            {"after": 4, "x": -44, "z": -92},
            {"after": 3, "x": 22, "z": -32},
            {"after": 4, "x": 0, "z": -27},
            {"after": 5, "x": -22, "z": -34},
        ],
    },
    "relief": relief,
    # Savanna: its grass tint is #bfb755, a dry yellow-green, which is what
    # marram is. Plains' #91bd59 beside blown sand reads as a summer lawn.
    "biome": {"kind": "solid", "biome": 35},
    "roomStyles": {"spawn": spawn_style},
    "dressing": {"styles": dict(tree_styles, **{"quay-shed": quay_shell}),
                 "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}: {len(finish['addShapes'])} shapes, "
      f"{len(finish['addLayers'])} made layers, "
      f"{sum(len(g['marks']) for g in relief.values())} marks in {len(relief)} reliefs, "
      f"{len(tree_styles)} tree recipes")
