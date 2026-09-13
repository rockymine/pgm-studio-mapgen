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
  strand -> quay    the slipway, 24 of run for 11 of rise
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
        {"id": "channel", "rect": [-7, -6, 14, 12], "holes": []},
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
            # The beach, scooped out of the shore rather than butted against
            # it. Its ring is drawn long and irregular so the transition is a
            # different width at every point along it.
            {"id": "strand-flat", "kind": "area", "h": 9, "bevel": 4,
             "ring": [[-44, -30], [-36, -38], [-24, -34], [-14, -42],
                      [-2, -37], [10, -43], [22, -38], [32, -44], [42, -40],
                      [44, -26], [30, -22], [16, -26], [0, -22], [-16, -26],
                      [-30, -22]]},
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
            # lands landward. It runs the east half only — the west half has
            # no mark between beach and dune at all, so the two meet there by
            # relaxation. Not everything on a board meets the same way.
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
    "vertices": [
        [-40, -48], [10, -48], [10, -78],
        [2, -78], [2, -62], [-6, -62], [-6, -78],         # east gate notch, 16
        [-16, -78], [-16, -64], [-26, -64], [-26, -78],   # west gate notch, 14
        [-40, -78],
    ],
}

def flight(fid, verts, anchors, material=STONE_BRICK):
    """A flight is a thing somebody built, so it carries a material rather than
    a theme, keeps the dressing off itself, and runs at least twice its rise."""
    return {"id": fid, "type": "polygon", "operation": "add", "override": True,
            "height_mode": "level", "skirt": 0, "floor": 0, "keepClear": True,
            "vertices": verts, "anchor_heights": anchors, "material": material}

flights = [
    # strand -> quay, up the seaward face: 24 of run for 11 of rise.
    flight("slipway", [[10, -44], [10, -36], [-14, -42], [-14, -48]],
           [9, 9, 20, 20]),
    # links -> quay through the west notch: 12 for 6.
    flight("gate-west", [[-26, -78], [-16, -78], [-16, -64], [-26, -64]],
           [15, 15, 20, 20]),
    # links -> quay through the east notch: 14 for 6, and longer, so the two
    # gates do not cost the same thing.
    flight("gate-east", [[-6, -78], [2, -78], [2, -62], [-6, -62]],
           [15, 15, 20, 20]),
    # strand -> links out on the east flank, away from the quay entirely.
    flight("dune-ramp", [[24, -58], [34, -58], [34, -42], [24, -42]],
           [17, 17, 9, 9], material=SS_SMOOTH),
]

# A parapet along the quay's seaward edge, drawn as a POLYLINE: the rasterizer
# splines its points before offsetting the band, so four points draw as a
# flowing wall rather than a chain of chords.
sea_wall = {
    # `polyline`, not `path`: the openapi description for SketchShape.type
    # lists "rectangle, circle, polygon, lasso, path", and the studio draws
    # five kinds of which the fifth is polyline. A `path` draws no ground and
    # says so as SK3, on a 200.
    "id": "sea-wall", "type": "polyline", "operation": "add",
    "vertices": [[-40, -44], [-40, -49], [-22, -50], [-2, -49],
                 [10, -50], [10, -44]],
    "radius": 1.5, "stroke_edge": "solid",
    # From the quay's OWN floor to the parapet's top, not from the quay's top
    # to it. Among the shapes of one layer the taller add wins the column
    # floor included, so a parapet stated as [quay top, quay top + 2] deletes
    # the quay under every cell it covers and the world keeps only the wall
    # (SK9). Stated from 0 it is simply the taller shape and the quay survives.
    "floor": 0, "base_height": 22, "keepClear": True, "material": STONE_BRICK,
}

# The lagoon. A `sink` is applied over the ground the relief solved, so it
# cuts a real hollow in the strand without a second area mark pinning against
# `strand-flat` and meeting it on a step (RL3). skirt 1 rather than 3: a
# skirted sink has a sloped rim, and a pool laid across a slope takes the
# lowest surface it crosses as its line and empties every column above it
# (DR-BANK). Flat to its own edge, the pool fills it and nothing is dug that
# the water does not reach. Three courses deep and under water, so the sheer
# edge is a pool's edge rather than a pit.
lagoon = {
    "id": "lagoon", "type": "polygon", "operation": "add",
    "height_mode": "sink", "base_height": 3, "skirt": 1, "floor": 0,
    "vertices": ring(-8, -26, 8, 12, 0.16, 5),
    "theme": "strand",
}

def freckle(fid, pts, theme):
    """Solid first, freckled afterwards — and FLUSH. `height_mode: "raise"`
    with a base_height of 0 does not sit level: it stands one course proud,
    which on a beach reads as gravel plates somebody laid. `follow` takes the
    height the field settles on under the shape and holds it there, so the
    patch's top equals the ground it paints. A shore is painted one ground and then
    the places that are genuinely something else are drawn ON it — a patch is a
    shape, and a field sampled between two grounds is static, not a beach."""
    return {"id": fid, "type": "polygon", "operation": "add",
            "relief_scope": "follow", "base_height": 1, "floor": 0,
            "vertices": pts, "theme": theme}

freckles = [
    freckle("wrack-1", ring(-30, -30, 9, 9, 0.24, 2), "strand"),
    freckle("wrack-2", ring(4, -24, 11, 10, 0.22, 4), "strand"),
    freckle("wrack-3", ring(30, -34, 8, 9, 0.26, 6), "strand"),
    freckle("blowout", ring(8, -84, 7, 9, 0.2, 8), "strand"),
]

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
    "wall": {"kind": "noise", "seed": 41, "scale": 11, "octaves": 2, "rise": 7,
             "stops": [SAND, SANDSTONE]},
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
    "wall": {"kind": "noise", "seed": 43, "scale": 9, "octaves": 2, "rise": 6,
             "stops": [SAND, SANDSTONE]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 43, "cellSize": 12, "rise": 6,
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

quay_shell = {
    "kind": "house",
    "shell": {
        "foundation": {
            "plate": {"stack": {"bands": [{"material": STONE_BRICK, "thickness": 1}],
                                "ending": "repeat"}, "extent": 1},
            "surface": {"field": None, "border": None, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": True},
            "footing": None,
        },
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0,
                 "overhang": 1, "ridgeCap": True, "hole": False,
                 "body": DARK_PLANK, "verge": solid(5, 1), "gable": solid(5, 1),
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                                  "hostData": 0, "data": 0, "sill": 2,
                                  "width": 2, "height": 2, "spacing": 3}},
        "wall": {"stack": {"bands": [
            {"material": STONE_BRICK, "thickness": 2},
            {"material": DARK_PLANK, "thickness": 4},
        ], "ending": "repeat"}, "extent": 6},
        "post": DARK_LOG,
        "windows": {"form": "arched", "block": 164, "hostBlock": 5,
                    "hostData": 5, "data": 0, "sill": 3, "width": 1,
                    "height": 2, "spacing": 3},
        "storeys": [], "porch": None, "front": None,
        "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "arched", "block": 164,
                    "fill": "upperSlab", "fillBlock": 126, "fillData": 5},
                    "width": 2, "height": 3},
    },
}

dressing_props = [
    # Two sheds on the quay: one style, two plots, differing in height and
    # footprint and in nothing else. Three styles would be three ideas.
    {"id": "net-store", "kind": "house", "seed": 21, "front": "posZ",
     "style": "quay-shed", "wings": [{"corners": [[-34, -74], [-25, -66]]}]},
    {"id": "warehouse", "kind": "house", "seed": 22, "front": "posZ",
     "style": "quay-shed", "wings": [{"corners": [[-2, -75], [8, -64]]}]},
    # A path is a claim about circulation, so it runs from the spawn door to
    # the west gate and stops there, at a door, rather than ending nowhere.
    {"id": "quay-road", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 11, "pave": PAVE,
     "points": [[0, -98], [-10, -90], [-20, -82], [-21, -70], [-18, -58]]},
    # Scrub on the dune crests, pines in the slacks where there is shelter.
    {"id": "scrub-a", "kind": "tree", "seed": 700, "x": -34, "z": -92, "style": "scrub-1"},
    {"id": "scrub-b", "kind": "tree", "seed": 701, "x": -34, "z": -80, "style": "scrub-2"},
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
    # A tidal pool, drawn INSIDE ground that is already level: the strand is
    # pinned flat at 9, so the pool fills a hollow rather than cutting one.
    {"id": "tide-pool", "kind": "water", "seed": 3, "shape": "pool",
     # The hollow and the pool that fills it are two statements about one
     # lake: `shore` widens the dug basin past the outline, and the difference
     # is a dry trench beside the water (DR-DRY). On ground already level the
     # pool needs neither a shore band nor a dig.
     # `radius` on a POOL is not a width — it is the shelf, how far in from
     # the outline the bed is held up. A shelf on ground already at the water
     # line is dug and holds nothing, which is the whole of DR-DRY's 56 dry
     # columns. No shelf, and the bed is cut two below the line it fills to.
     # It fills the hollow the sink cut, rather than cutting one: the basin
     # floor is 6, the line is 8, and `radius` — which on a pool is the SHELF
     # rather than a width — stays small. At radius 0 there is no pool at all.
     "level": 8, "depth": 1, "shore": 0, "shoreWander": False, "radius": 1,
     "bank": {"kind": "cell", "seed": 23, "cellSize": 9, "jitter": 3,
              "warp": 2, "rise": 3, "palette": [GRAVEL, SAND]},
     "points": ring(-8, -26, 10, 12, 0.14, 5)},
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
    "themes": {"links": links_theme, "strand": strand_theme, "quay": quay_theme},
    "mapTheme": "links",
    "addShapes": [quay] + flights + [sea_wall, lagoon] + freckles,
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
