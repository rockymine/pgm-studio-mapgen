"""Dustwath — a DTM board on a bleached dust-flat, split by the bed of a river that has gone.

The board is a lane: 88 blocks across and 208 long, with the two teams' ground ending at the
wath — the dry crossing that named the place — and a build zone spanning its whole width. Each
team's monument stands in the open on a low sand bench a short walk forward of its camp, fourteen
blocks off the centre line so that both flanks are on somebody's journey.

Four grounds meet on it and each is stated by the one instrument that can state it:

  the dust flat      area marks at three heights, bevelled into each other, with a dune grain
  the sand bench     an area mark the monument stands on, bevelled five cells into the flat
  the back dunes     two pushes, crowned and roughened, added to the solved surface
  the camp compound  a made floor with relief_scope exclude, met by an authored flight

and the braided scours that run down to the bed are line marks with a narrow tread, so the band
either side of each lofts back to the flat instead of walling itself.
"""

import json, os

SLUG = "opus5-dustwath"
HERE = os.path.dirname(os.path.abspath(__file__))

CELL = 4
FLAT = 20            # the dust flat: the board's own surface
BACK = 21            # the back dust, where the camp stands and the dunes are pushed up
BENCH = 23           # the sand bench the monument stands on
LIP = 19             # the flats, falling to the bank
FORD = 16            # the old ford's stone head, three below the flats and cut into the bank

# ── the plan: five rectangles, an arrangement and nothing else ───────────────────────────────
def plan():
    return {
        "plan": 2,
        "meta": {"name": "Dustwath"},
        "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12,
                    "surface": FLAT, "observerY": 52},
        "pieces": [
            # the back dust, where the dunes stand                blocks x -32..32, z -104..-80
            {"id": "head",  "role": "piece", "rect": [-8,  -26, 16,  6], "surface": BACK},
            # the camp, standing in it. 16 x 16 blocks, because a protection region is at most
            # 20 x 30 (ST10) and the piece is what the protection is cut from.
            {"id": "camp",  "role": "spawn", "rect": [-2,  -25,  4,  4], "surface": BACK},
            # the apron: the open ground the track crosses        blocks x -44..44, z -80..-56
            {"id": "apron", "role": "piece", "rect": [-11, -20, 22,  6], "surface": FLAT},
            # the sand bench the monument stands on               blocks x -32..32, z -56..-40
            {"id": "bench", "role": "piece", "rect": [-8,  -14, 16,  4], "surface": BENCH},
            # the flats, falling to the lip of the bed            blocks x -44..44, z -40..-24
            {"id": "flats", "role": "piece", "rect": [-11, -10, 22,  4], "surface": LIP},
        ],
        # the wath: the gap between the two teams' ground, spanned end to end and no further --
        # a zone reaching past the last ground it docks overhangs into void (BZ9)
        "zones": [{"id": "wath", "rect": [-11, -6, 22, 12]}],
        "placements": {
            # camp's minimum corner is (-8, -100), so this is (0, -92): the spawns 184 apart
            "spawns": [{"id": "spawn-1", "piece": "camp", "at": [8, 8], "facing": "back",
                        "footprint": [2, 2, 12, 12]}],
            # bench's minimum corner is (-32, -56), so this is (-14, -51) -- 14 blocks off the
            # centre line, which is what keeps the flanks on a journey somebody makes
            "destroyables": [{"id": "destroyable-1", "piece": "bench", "at": [18, 5],
                              "style": "pillar-3", "materials": "obsidian", "float": 4,
                              "name": "The Wath Stone"}],
        },
    }


# ── what it is made of ───────────────────────────────────────────────────────────────────────
# Three tone families, named before anything is painted:
#   ground  pale sand and sandstone, bleached, the lightest of this run's four boards
#   built   brick and weathered spruce -- red-brown masonry and dark timber, nowhere near the sand
#   accent  the dry olive grass the Savanna tint gives, and the acacia canopy over it
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}

def cell(seed, size, *palette):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 2, "warp": 3,
            "palette": list(palette), "rise": 0}

def depth_stack(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def by_slope(*bands):
    """One stack finishing the flat, the shoulder and the cut face of the same ground. A thickness
    on the slope axis is a span of degrees, so this is the one thing that tells a bank from a pan."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


SAND = solid(12)
SANDSTONE = solid(24)
SMOOTH = solid(24, 2)
CHISELLED = solid(24, 1)
GRASS = solid(2)
DIRT = solid(3)
COARSE = solid(3, 1)
BRICK = solid(45)
SPRUCE = solid(5, 1)
SPRUCE_LOG = solid(17, 1)

# The flat is dry grass gone over to sand in patches -- two blocks at a brush wide enough to read as
# patches rather than as speckle. The shoulder is the sand alone with the silt showing through it.
# The face is bedded sandstone, which is what the banks of this bed are cut in.
FLAT_TOP = cell(21, 11, GRASS, SAND, GRASS, SAND)
SHOULDER_TOP = cell(23, 8, SAND, COARSE, SAND, SAND)

def dust_theme():
    return {
        "bedrock": {"relative": False, "value": 1},
        # the lip of the bank over the bed is the one made edge on this board's ground
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        "rim": {"material": SMOOTH, "depth": 1, "enabled": True},
        "surface": {"depth": 4, "enabled": True, "material": by_slope(
            (depth_stack((FLAT_TOP, 1), (DIRT, 2), (SANDSTONE, 1)), 13),
            (depth_stack((SHOULDER_TOP, 1), (SAND, 1), (SANDSTONE, 2)), 19),
            (depth_stack((SANDSTONE, 2), (SMOOTH, 1), (SANDSTONE, 1)), 58))},
        # the cut banks: bedding planes, which is the whole reason this board has a bed in it
        "wall": {"kind": "wallRun", "runs": [
            {"material": SANDSTONE, "width": 3},
            {"material": SMOOTH, "width": 1},
            {"material": SANDSTONE, "width": 2},
            {"material": CHISELLED, "width": 1}]},
        "wallEnabled": True,
        # the body of the rock, seen only where the bed cuts it: two sandstones, cells wider than tall
        "fill": {"kind": "voronoi", "seed": 17, "cellSize": 15, "rise": 7, "bands": [
            {"material": SMOOTH, "depth": 2}, {"material": SANDSTONE, "depth": 1}]},
    }


def scour_theme():
    """The floor of a dry watercourse: what the water left when it stopped coming. Stated on
    patches drawn where the braid widens into a pan, not sampled over the whole board."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": False,
        "rim": {"material": SANDSTONE, "depth": 1, "enabled": True},
        "surface": {"depth": 3, "enabled": True, "material": depth_stack(
            (cell(29, 7, SAND, solid(13), SAND, COARSE), 1), (SAND, 1), (SANDSTONE, 1))},
        "wall": {"kind": "wallRun", "runs": [
            {"material": SANDSTONE, "width": 2}, {"material": SMOOTH, "width": 1}]},
        "wallEnabled": True,
        "fill": {"kind": "voronoi", "seed": 19, "cellSize": 13, "rise": 6, "bands": [
            {"material": SANDSTONE, "depth": 2}, {"material": SMOOTH, "depth": 1}]},
    }


def works_theme():
    """The ford's own head: laid brick with a spruce deck, the one made ground on the board, and
    deliberately out of the sand's family so that it reads as somebody's work from the far bank."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": CHISELLED, "depth": 1, "enabled": True},
        "surface": {"depth": 2, "enabled": True, "material": depth_stack(
            (cell(31, 6, BRICK, SPRUCE, BRICK, BRICK), 1), (BRICK, 1))},
        # the revetment face, in courses, because a wall of one material reads as a cut
        "wall": {"kind": "wallRun", "runs": [
            {"material": BRICK, "width": 3},
            {"material": SMOOTH, "width": 1},
            {"material": BRICK, "width": 2}]},
        "wallEnabled": True,
        "fill": solid(24, 2),
    }


# ── the ground, as four things that meet ─────────────────────────────────────────────────────
def marks():
    """Written in the order they are solved: a later mark wins a contested cell, so the pans are
    stated first, the bench over them, and the scours last, cutting down through both."""
    return [
        # the back dust the camp stands on
        {"id": "back-pan", "kind": "area", "h": 21, "bevel": 3,
         "ring": [[-31, -103], [-12, -101], [14, -103], [31, -100],
                  [30, -84], [10, -82], [-16, -83], [-30, -85]]},
        # the apron: the open ground the track crosses
        {"id": "apron-pan", "kind": "area", "h": 20, "bevel": 4,
         "ring": [[-43, -78], [-12, -76], [20, -78], [43, -75],
                  [42, -59], [8, -57], [-22, -59], [-42, -60]]},
        # the flats, held at their own height right up to the lip, so the bank is a face and not
        # a grade -- the one thing that makes a cut bank read as cut
        {"id": "flats-pan", "kind": "area", "h": 19, "bevel": 3,
         "ring": [[-43, -39], [-10, -37], [22, -39], [43, -37],
                  [43, -25], [10, -25], [-14, -25], [-43, -26]]},
        # the sand bench the monument stands on: deposited, so nothing is pinned that need not be
        # and the bevel is what grades it into the apron on one side and the flats on the other
        {"id": "sand-bench", "kind": "area", "h": 23, "bevel": 5,
         "ring": [[-30, -54], [-16, -55], [2, -53], [18, -54], [28, -50],
                  [26, -43], [8, -41], [-12, -42], [-26, -44], [-31, -49]]},
        # two braided scours falling to the bed. A narrow tread and the rest of the band lofts, so
        # each reads as a scour rather than as a trench with a wall down both sides.
        # a hollow in the flats, short of the bank: an entrance from below onto the bench, and
        # the one place on this board where the ground drops without the bed doing it
        {"id": "hollow", "kind": "area", "h": 16, "bevel": 2,
         "ring": [[-14, -42], [-4, -44], [6, -41], [9, -35], [2, -31],
                  [-8, -31], [-15, -36]]},
        {"id": "braid-w", "kind": "line", "h": 17.5, "r": 6, "tread": 1,
         "points": [[-40, -66], [-34, -56], [-31, -44], [-28, -30]]},
        {"id": "braid-e", "kind": "line", "h": 18, "r": 5, "tread": 1,
         "points": [[36, -72], [31, -60], [27, -46], [24, -31]]},
    ]


def pushes():
    """Added to the solved surface after the marks, so each is kept off the ground a mark had to
    arrive at: the flight's foot, the bench, and the lip."""
    return [
        {"id": "dune-w", "ring": [[-31, -102], [-22, -100], [-18, -92], [-24, -85], [-30, -88]],
         "amount": 3.0, "falloff": 10, "crown": 2.5, "roughness": 1.5, "seed": 4},
        {"id": "dune-e", "ring": [[17, -103], [28, -101], [31, -93], [24, -86], [17, -92]],
         "amount": 2.2, "falloff": 9, "crown": 2.0, "roughness": 1.2, "seed": 11},
        # a low swell on the apron's east hand, so the open ground is not a table
        {"id": "swell", "ring": [[16, -76], [38, -74], [42, -64], [26, -60], [14, -66]],
         "amount": 1.6, "falloff": 12, "crown": 1.5, "roughness": 1.0, "seed": 21},
    ]


def shapes():
    """What the plan cannot state: the bays the bed ate out of the bank, the flight down onto the
    causeway head, its two revetments, and the pans of scour the braids run into."""
    out = []

    # The two bays: void, eaten out of the bank either side of the ford, so the crossing is 31
    # blocks at the causeway and about 50 at the flanks -- short and watched against long and safe.
    # A subtract is the board's statement of its own negative space; nothing may fill one.
    out.append({"id": "bay-w", "type": "polygon", "operation": "subtract",
                "vertices": [[-46, -28], [-40, -31], [-35, -28], [-31, -33], [-26, -31],
                             [-22, -25], [-18, -27], [-17, -14], [-46, -14]]})
    out.append({"id": "bay-e", "type": "polygon", "operation": "subtract",
                "vertices": [[16, -24], [19, -31], [24, -34], [27, -28], [31, -30],
                             [35, -35], [40, -30], [46, -27], [46, -14], [16, -14]]})


    # The causeway head: a tongue of laid brick reaching into the gap, so the crossing is 23
    # blocks here against about 50 at the flanks. It is authored rather than planned because it
    # is a landform somebody made, not a room that has to be exactly somewhere -- and a piece
    # there presents its own two sides to the zone as an eight-block front (FR9).
    out.append({"id": "ford-head", "type": "polygon", "operation": "add",
                "base_height": FORD, "relief_scope": "exclude", "keepClear": True,
                "theme": "works",
                "vertices": [[-12, -25], [-4, -26], [5, -25], [12, -24],
                             [11, -13], [-2, -12], [-11, -13]]})

    # The flight down the bank onto the causeway head: level, sheer-sided, out of the relief's
    # solve so it arrives where it was told, ten blocks of run against three of rise, and a
    # material rather than a theme -- a stair is a thing somebody built and a theme is a place.
    out.append({"id": "ford-flight", "type": "polygon", "operation": "add",
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "keepClear": True, "floor": 0,
                "vertices": [[-7, -29], [7, -29], [7, -19], [-7, -19]],
                "anchor_heights": [19, 19, 16, 16],
                "material": {"kind": "cell", "seed": 37, "cellSize": 7, "jitter": 1, "warp": 2,
                             "palette": [BRICK, SMOOTH, BRICK, SANDSTONE], "rise": 3}})

    # The revetments either side of it. Out of the solve, so they keep the height they were drawn
    # at while the ground falls away under them: one course proud at the head, four at the foot,
    # which is what a revetment does. Brick, because the built family is not the sand's.
    for side, xs in (("w", -9), ("e", 8)):
        out.append({"id": f"revet-{side}", "type": "polyline", "operation": "add",
                    "radius": 1, "stroke_edge": "solid", "base_height": 20,
                    "relief_scope": "exclude", "keepClear": True,
                    "vertices": [[xs, -31], [xs, -26], [xs, -21], [xs, -17]],
                    "material": {"kind": "layered", "axis": "depth", "stack": {
                        "ending": "repeat", "bands": [
                            {"material": CHISELLED, "thickness": 1},
                            {"material": BRICK, "thickness": 4}]}}})

    # Where each braid widens into a pan, the ground the water left. A brush has to state a
    # height_mode or it is never a candidate for the paint at all; a raise of zero sits flush on
    # ground a mark already pinned level and changes no height.
    for name, ring in (("pan-w", [[-38, -43], [-28, -45], [-21, -39],
                                  [-25, -34], [-35, -33], [-41, -38]]),
                       ("pan-e", [[21, -45], [31, -46], [36, -41],
                                  [32, -37], [22, -36], [17, -40]]),
                       ("pan-mid", [[-11, -40], [-2, -41], [5, -39],
                                    [5, -34], [-3, -33], [-11, -36]])):
        out.append({"id": name, "type": "polygon", "operation": "add",
                    "height_mode": "raise", "base_height": 0, "skirt": 0,
                    "vertices": ring, "theme": "scour"})
    return out


# ── what a team walks out of, and what stands on the flanks ──────────────────────────────────
def band(*bands):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "extent": sum(t for _m, t in bands)}

def window(form, block, width=1, height=2, sill=2, spacing=4, data=0):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": data,
            "sill": sill, "width": width, "height": height, "spacing": spacing}

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                 "inlayInset": 2, "isPlain": True}


def camp_hall():
    """The spawn hall: brick to the sill, spruce above it, spruce posts at the corners and a
    beam course of laid log where the storey changes -- a beam has to be the end of something.
    No footing: over a plate one course deep it is a rim round a building with no foundation."""
    return {
        "foundation": {"plate": band((BRICK, 1)), "surface": PLAIN_SURFACE, "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": 126, "slabData": 1, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": SPRUCE, "verge": {"kind": "laidLog", "id": 17, "data": 1},
                 "gable": solid(5, 1),
                 "gableWindows": window("pane", 102, width=1, height=2, sill=1, spacing=3)},
        "wall": band((BRICK, 3), (SPRUCE, 4)),
        "post": SPRUCE_LOG,
        "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
        "storeys": [
            {"clear": 5, "wall": band((BRICK, 3), (SPRUCE, 3)), "post": SPRUCE_LOG,
             "windows": window("pane", 102, width=2, height=2, sill=3, spacing=4),
             "surface": PLAIN_SURFACE, "deck": None, "headroom": 5},
        ],
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": False},
        "doorway": {"door": "air", "width": 2, "height": 3,
                    "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                             "fillBlock": 126, "fillData": 1}},
    }


def shelter():
    """One style, and the two plots differ in height and footprint and in nothing else, which is
    what makes two buildings a row rather than two ideas."""
    shell = camp_hall()
    shell["wall"] = band((BRICK, 2), (SPRUCE, 3))
    shell["storeys"] = []
    shell["roof"] = dict(shell["roof"], form="hip", pitch=1, overhang=1, ridgeCap=False)
    shell["windows"] = window("pane", 102, width=1, height=2, sill=2, spacing=3)
    return {"kind": "house", "shell": shell}


def dressing():
    trees = json.load(open(f"{HERE}/trees.json"))
    styles = dict(trees)
    styles["shelter"] = shelter()

    props = [
        # The track: out of the camp door, past the drovers' shelter, over the bench's west
        # shoulder and down to the causeway. Three blocks a reader cannot quite tell apart, solid,
        # because a worn band reads as litter and a path is a claim about where people walk.
        {"id": "track-camp", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True,
         "pave": cell(43, 5, DIRT, COARSE, SPRUCE, DIRT),
         "points": [[0, -84], [-8, -78], [-18, -72], [-26, -66]]},
        {"id": "track-bench", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True,
         "pave": cell(44, 5, DIRT, COARSE, SPRUCE, DIRT),
         "points": [[-26, -66], [-25, -56], [-21, -46], [-14, -38]]},
        {"id": "track-ford", "kind": "stroke", "seed": 45, "radius": 2, "style": "solid",
         "coverage": 1.0, "claimsGround": True,
         "pave": cell(46, 5, DIRT, COARSE, SPRUCE, DIRT),
         "points": [[-14, -38], [-8, -34], [-2, -31], [0, -28]]},
        # The braid floors: not a path, so not solid -- a scoured bed reads as stones left behind.
        {"id": "bed-w", "kind": "stroke", "seed": 47, "radius": 4, "style": "stones",
         "coverage": 0.7, "claimsGround": True,
         "pave": cell(48, 6, SAND, solid(13), SAND, COARSE),
         "points": [[-40, -66], [-34, -56], [-31, -44], [-28, -31]]},
        {"id": "bed-e", "kind": "stroke", "seed": 49, "radius": 3, "style": "stones",
         "coverage": 0.7, "claimsGround": True,
         "pave": cell(50, 6, SAND, solid(13), SAND, COARSE),
         "points": [[36, -72], [31, -60], [27, -46], [24, -32]]},
    ]

    # Two shelters on the apron, one plot taller than the other. They are here because the flanks
    # need a reason to be walked and a sightline across the apron needs breaking, and the track
    # runs to the west one's door.
    props.append({"id": "shelter-w", "kind": "house", "seed": 501, "front": "posZ",
                  "style": "shelter",
                  "wings": [{"corners": [[-36, -75], [-26, -67]], "spec": {"ridge": "alongX"}}]})
    props.append({"id": "shelter-e", "kind": "house", "seed": 502, "front": "negZ",
                  "style": "shelter",
                  "wings": [{"corners": [[22, -74], [32, -65]],
                             "spec": {"storeysHigh": 1, "ridge": "alongX"}}]})

    # Boulders are stone and nothing else, and each one sits where the scour dropped it.
    for at, (bx, bz) in enumerate([(-28, -47), (-19, -35), (38, -66), (16, -48), (-27, -90)]):
        props.append({"id": f"rock-{at}", "kind": "boulder", "seed": 610 + at,
                      "x": bx, "z": bz, "style": "rock"})

    # Thorn trees: the flat-topped acacias on the open ground, the slim ones where the dust is
    # deepest. Every one is placed off the track and off the bench's top, which is the goal's.
    plant = [("thorn-1", -26, -96), ("thorn-2", 22, -95), ("thorn-3", -22, -83),
             ("thorn-1", 27, -84), ("thorn-2", 14, -72), ("thorn-3", 12, -63),
             ("spar-1", -40, -58), ("spar-2", 38, -60), ("spar-1", -42, -36),
             ("spar-2", 8, -52), ("thorn-2", -18, -101), ("spar-1", 18, -100)]
    for at, (style, tx, tz) in enumerate(plant):
        props.append({"id": f"thorn-{at}", "kind": "tree", "seed": 700 + at,
                      "x": tx, "z": tz, "style": style})

    # Ground cover over the whole board rather than in patches: the density field is better at
    # patchiness than a hand-drawn outline is. Both gameplay numbers stay low -- tall grass is
    # cover nobody authored, in front of a goal nobody chose.
    props.append({"id": "cover", "kind": "flora", "seed": 800,
                  "points": [[-48, -108], [48, -108], [48, -14], [-48, -14]],
                  "spec": {"coverage": 0.17, "scale": 34, "octaves": 3, "fernShare": 0.10,
                           "flowerShare": 0.05, "flowerScale": 20, "tallShare": 0.04}})

    # A boulder is stone: stone, cobblestone and andesite is the whole palette that reads as rock
    # from any distance, and the field is resolved in the rock's own frame so every image matches.
    styles["rock"] = {"kind": "boulder", "form": "angular", "size": 3.0, "mossy": False,
                      "rock": cell(53, 4, solid(1), solid(4), solid(1, 5), solid(1))}
    return {"styles": styles, "props": props}


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-14",
        # Savanna: the grass tint is #bfb755, the olive of dry grass, which is the one colour on
        # this board a block does not state for itself. A pale sand board on Plains has a summer
        # meadow running through it.
        "biome": {"kind": "solid", "id": 35},
        "themes": {"dust": dust_theme(), "scour": scour_theme(), "works": works_theme()},
        "mapTheme": "dust",
        # the causeway head carries its own theme and its own relief_scope on the shape itself,
        # so nothing here has to key on a compiled id that a re-plan could rename

        # the board's coast, drawn as a coast rather than as the staircase of rectangles the plan
        # compiled to. Nothing moves outward, so no strait is closed by it.
        "bendShapes": {"apron-21": {"k": 0.18, "wander": 3, "step": 11, "seed": 5},
                       "apron-20": {"k": 0.18, "wander": 3, "step": 11, "seed": 9}},
        "relief": {"*": {"base": FLAT, "reach": 0, "step": 1, "landform": "plain",
                         "grain": {"amplitude": 1.2, "scale": 20, "seed": 7},
                         "marks": marks(), "pushes": pushes()}},
        "addShapes": shapes(),
        "roomStyles": {"spawn": camp_hall()},
        "dressing": dressing(),
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
