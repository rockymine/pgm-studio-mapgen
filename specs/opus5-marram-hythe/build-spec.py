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
QUARTZ_PILL = solid(155, 2)
DARK_PLANK  = solid(5, 5)
DARK_LOG    = solid(17, 5)
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
                "surface": 9, "observerY": 52},
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
        {"id": "bar", "role": "piece", "rect": [-7, -2, 14, 4],
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
            {"id": "destroyable-1", "piece": "shore", "at": [22, 50],
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
             "ring": ring(-14, 0, 11, 10, 0.18, 7)},
            {"id": "bar-knap", "kind": "point", "at": [18, 0], "r": 6, "h": 14},
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
        [-38, -52], [-6, -52], [-6, -72],
        [-12, -72], [-12, -58], [-18, -58], [-18, -72],   # east gate notch, 14
        [-26, -72], [-26, -60], [-34, -60], [-34, -72],   # west gate notch, 12
        [-38, -72],
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
    flight("slipway", [[-6, -50], [-6, -42], [-30, -46], [-30, -50]],
           [9, 9, 20, 20]),
    # links -> quay through the west notch: 12 for 6.
    flight("gate-west", [[-34, -72], [-26, -72], [-26, -60], [-34, -60]],
           [14, 14, 20, 20]),
    # links -> quay through the east notch: 14 for 6, and longer, so the two
    # gates do not cost the same thing.
    flight("gate-east", [[-18, -72], [-12, -72], [-12, -58], [-18, -58]],
           [14, 14, 20, 20]),
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
    "vertices": [[-38, -53], [-26, -54], [-14, -53], [-6, -54]],
    "radius": 1.5, "stroke_edge": "solid",
    # From the quay's OWN floor to the parapet's top, not from the quay's top
    # to it. Among the shapes of one layer the taller add wins the column
    # floor included, so a parapet stated as [quay top, quay top + 2] deletes
    # the quay under every cell it covers and the world keeps only the wall
    # (SK9). Stated from 0 it is simply the taller shape and the quay survives.
    "floor": 0, "base_height": 22, "keepClear": True, "material": STONE_BRICK,
}

def freckle(fid, pts, theme):
    """Solid first, freckled afterwards. A shore is painted one ground and then
    the places that are genuinely something else are drawn ON it — a patch is a
    shape, and a field sampled between two grounds is static, not a beach."""
    return {"id": fid, "type": "polygon", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": pts, "theme": theme}

freckles = [
    freckle("wrack-1", ring(-30, -30, 9, 9, 0.24, 2), "strand"),
    freckle("wrack-2", ring(4, -24, 11, 10, 0.22, 4), "strand"),
    freckle("wrack-3", ring(30, -34, 8, 9, 0.26, 6), "strand"),
    freckle("blowout", ring(8, -84, 7, 9, 0.2, 8), "strand"),
]

# --------------------------------------------------------- the lighthouse
# A made thing out of the studio's own emitters: nested annuli whose tops rise
# inward for the tower, concentric discs for the lantern. `kind: "made"` is
# what keeps the stacking rules off it — SK10 reads a solid sinking into ground
# as a lost gap, and SK11 reads its head as standable ground with no stair.
LIGHT = (-34, -56)
tower = props.tapered_tower("light-tower", LIGHT[0], LIGHT[1],
                            base_radius=5, top_radius=3.5, thickness=5,
                            floor=20, height=18, theme=None,
                            name="Light tower", mirrors=True)
lantern = props.dome("light-lantern", LIGHT[0], LIGHT[1], radius=4,
                     floor=38, theme=None, squash=0.8,
                     name="Light lantern", mirrors=True)

def as_made(layer, material, part):
    """props.py emits a SketchLayer — {id, name, base_y, layout:{shapes,
    groups}} — which is what the layers route takes. drive.py's `addLayers`
    takes the same thing FLAT, so the nesting is unwrapped here.

    One material rather than a theme: the tower is drawn as terrain and made of
    one thing, which is what `material` on a shape is for, and it keeps the
    board at three themes. `kind: "made"` is what keeps the stacking rules off
    it — SK10 reads a solid sinking into ground as a lost gap, and SK11 reads
    its head as standable ground with no stair onto it."""
    inner = layer.pop("layout")
    layer["shapes"] = inner["shapes"]
    layer["groups"] = inner["groups"]
    layer["kind"] = "made"
    layer["part_of"] = part
    for shape in layer["shapes"]:
        shape.pop("theme", None)
        shape["material"] = material
    return layer

tower = as_made(tower, STONE_BRICK, "lighthouse")
lantern = as_made(lantern, QUARTZ, "lighthouse")

# ---------------------------------------------------------------- themes
# Three, and three tone families named before any of them was written:
# GROUND is sand and marram, BUILT is stone brick and dark oak, and the ACCENT
# is the team tint, which appears on the quay's own face and nowhere else.
links_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    # The rim is off: this ground is relief-solved, and a rim caps every fall
    # with a band, which turns a dune field into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": SANDSTONE},
    # Finished by angle. Marram holds the flat and the shoulder of a dune; the
    # steep face of one is bare blown sand, and the slope axis is the only
    # thing on the board that knows the difference.
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        (depth_stack((GRASS, 1), (DIRT, 1), (SAND, 2)), 16),
        (depth_stack((COARSE_DIRT, 1), (SAND, 3)), 18),
        (depth_stack((SAND, 3), (SANDSTONE, 1)), 56),
    )},
    "wall": {"kind": "wallRun", "runs": [
        {"material": SANDSTONE, "width": 4},
        {"material": SAND, "width": 2},
        {"material": SS_SMOOTH, "width": 1},
    ]},
    "wallEnabled": True,
    # A voronoi is never ground: it goes in the fill, in stone, where it is the
    # body of the rock nobody sees until a face is cut.
    "fill": {"kind": "voronoi", "seed": 41, "cellSize": 13, "rise": 6,
             "bands": [{"material": SANDSTONE, "depth": 2},
                       {"material": STONE, "depth": 1}]},
}

strand_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (GRAVEL, 1), (SAND, 2))},
    "wall": {"kind": "wallRun", "runs": [
        {"material": SAND, "width": 3},
        {"material": GRAVEL, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 43, "cellSize": 12, "rise": 6,
             "bands": [{"material": SANDSTONE, "depth": 2},
                       {"material": STONE, "depth": 1}]},
}

quay_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "boundary",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONE_BRICK},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (STONE_BRICK, 1), (COBBLE, 2), beyond=STONE)},
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
             "bands": [{"material": STONE, "depth": 2},
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
    "beams": {"block": 17, "data": 5, "reach": 1, "any": True},
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

PAVE = {"kind": "cell", "seed": 19, "cellSize": 9, "entries": [
    {"material": GRAVEL}, {"material": ANDESITE}, {"material": COBBLE}]}

dressing_props = [
    # A path is a claim about circulation, so it runs from the spawn door to
    # the west gate and stops there, at a door, rather than ending nowhere.
    {"id": "quay-road", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 11, "pave": PAVE,
     "points": [[0, -98], [-12, -90], [-24, -82], [-30, -74]]},
    # Scrub on the dune crests, pines in the slacks where there is shelter.
    {"id": "scrub-a", "kind": "tree", "seed": 700, "x": -34, "z": -92, "style": "scrub-1"},
    {"id": "scrub-b", "kind": "tree", "seed": 701, "x": -34, "z": -80, "style": "scrub-2"},
    {"id": "scrub-c", "kind": "tree", "seed": 702, "x": 24,  "z": -94, "style": "scrub-3"},
    {"id": "scrub-d", "kind": "tree", "seed": 703, "x": 36,  "z": -76, "style": "scrub-1"},
    {"id": "pine-a",  "kind": "tree", "seed": 710, "x": -42, "z": -62, "style": "pine-1"},
    {"id": "pine-b",  "kind": "tree", "seed": 711, "x": 2,   "z": -78, "style": "pine-2"},
    {"id": "pine-c",  "kind": "tree", "seed": 712, "x": 8,   "z": -70, "style": "pine-4"},
    {"id": "pine-d",  "kind": "tree", "seed": 713, "x": 30,  "z": -60, "style": "pine-5"},
    # A boulder is stone, and these are the ones the tide left on the strand.
    {"id": "skerry-0", "kind": "boulder", "x": -18, "z": -34, "seed": 61, "radius": 3},
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
     "level": 9, "depth": 2, "shore": 0, "shoreWander": False, "radius": 0,
     "bank": {"kind": "cell", "seed": 23, "cellSize": 9,
              "entries": [{"material": GRAVEL}, {"material": SAND}]},
     "points": ring(-6, -26, 11, 12, 0.18, 5)},
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
    "addShapes": [quay] + flights + [sea_wall] + freckles,
    "addLayers": [tower, lantern],
    "relief": relief,
    # Savanna: its grass tint is #bfb755, a dry yellow-green, which is what
    # marram is. Plains' #91bd59 beside blown sand reads as a summer lawn.
    "biome": {"kind": "solid", "biome": 35},
    "roomStyles": {"spawn": spawn_style},
    "dressing": {"styles": tree_styles, "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}: {len(finish['addShapes'])} shapes, "
      f"{len(finish['addLayers'])} made layers, "
      f"{sum(len(g['marks']) for g in relief.values())} marks in {len(relief)} reliefs, "
      f"{len(tree_styles)} tree recipes")
