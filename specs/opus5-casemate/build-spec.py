#!/usr/bin/env python3
"""Casemate — a structural King of the Hill board.

`match-flow.md` §10 is the law this is built to. A capture board is a control game: the objective is a
place rather than a thing, so the board is plazas, walls, decks and vaults rather than landscape, it has
no dead ground, and no point stands high over open ground looking down on the approach that takes it.

    terreplein  y20   the open works both teams spawn onto, cut by pillars and low cover
    casemate    y13   a vault under the middle of it, lit by one slot, holding the centre point
    rampart     y22   a raised walk round the flanks, entering each bay by a two-block drop

The three points sit where the structure decides, not where the ground happens to be high:

    The Cistern   under the terreplein, in the casemate, entered down two ramps or through the slot
    West Bay      a walled bay at the flank, open on one side only, plus a one-way port at the back
    East Bay      its image

Every shape is written out for both halves rather than left to a fan, because the structure is the board
and a structure that is mirrored by something else is a structure nobody can read the coordinates of.

    python3 specs/opus5-casemate/build-spec.py
"""

import json
import os

SLUG = "opus5-casemate"
HERE = os.path.dirname(os.path.abspath(__file__))

CELL = 2
DECK = 20                # the terreplein: the ground both teams walk out onto
VAULT = 13               # the casemate floor, seven below it
LID = 20                 # the casemate's ceiling course: one over the terreplein, so the roof
                         # is stepped onto rather than driven into the ground beside it (`SK10`)
RAMPART = 22             # the raised walk that enters each bay over a two-block drop

# rot_180 images block b onto -1-b, so the board's centre is the -0.5 boundary and an EVEN pad is the
# only one that can sit on it. Centred(anchor, 8) spans [anchor-3, anchor+4].
HILL = 8
CISTERN_ANCHOR = -1      # blocks [-4, 3]: its own mirror
EAST_BAY_ANCHOR = 37     # blocks [34, 41], centre 37.5 -- 38 out
WEST_BAY_ANCHOR = -39    # blocks [-42, -35]: the image of the east pad
HALF_SEPARATION = 44     # 38/44 = 0.86, the top of the corpus's own range (quartiles 0.52 and 0.88)

# What the middle is worth. A board whose points all pay the same is a board two teams settle by taking
# one each and standing on them, so the middle pays double and is the thing there is a match about.
# 13 of the 83 corpus KotH boards vary the rate, and in 10 of those the highest-paying point is the one
# named for the middle; `koth/catre_koth` and `koth/abaddon_koth` are both exactly 1 / 2 / 1.
CENTRE_POINTS = 2
FLANK_POINTS = 1


def images(x0, z0, x1, z1):
    """A block rect and its three images, so the works are symmetric across BOTH axes rather than only
    under the half-turn. A board carrying a pair of flank points wants to read the same from the left as
    from the right: rot_180 alone sends a wall on one team's west to the other team's east, and the two
    halves of the board then differ in a way neither team's play can be compared across.

    Mirror in x maps b -> -1-b on x alone, mirror in z on z alone, and the half-turn is the two together.
    Duplicates are dropped, so a shape already sitting on an axis contributes only the images it has."""
    out, seen = [], set()
    for rect_box in ((x0, z0, x1, z1), (-1 - x1, z0, -1 - x0, z1),
                     (x0, -1 - z1, x1, -1 - z0), (-1 - x1, -1 - z1, -1 - x0, -1 - z0)):
        if rect_box in seen: continue
        seen.add(rect_box)
        out.append(rect_box)
    return out


def rect(shape_id, box, floor, height, theme, group=None, layer=None):
    x0, z0, x1, z1 = box
    out = {"id": shape_id, "type": "rectangle", "operation": "add",
           "min_x": x0, "min_z": z0, "max_x": x1 + 1, "max_z": z1 + 1,
           "floor": floor, "base_height": height, "theme": theme}
    if group: out["group"] = group
    if layer: out["layer"] = layer
    return out


def fanned(shape_id, box, floor, height, theme):
    """One structure and every image of it, written out."""
    return [rect(f"{shape_id}-{at}", image, floor, height, theme)
            for at, image in enumerate(images(*box))]


# ── the plan: two rectangles and nothing else ────────────────────────────────────────────────────
def plan():
    return {
        "plan": 2,
        "meta": {"name": "Casemate"},
        "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                    "surface": DECK, "observerY": 56},
        "pieces": [
            # The works. One shape: the board's parts are walls and decks placed on it, not pieces cut
            # out of it, which is what keeps a structural board from reading as a partition.
            {"id": "works", "role": "piece", "rect": [-27, -19, 54, 38], "surface": DECK},
            # One gate house; the symmetry fans the other. Blocks x[-10,9], z[-50,-39].
            {"id": "gate", "role": "spawn", "rect": [-5, -25, 10, 6], "surface": DECK},
        ],
        "placements": {
            # 10 in from x=-10 is the grid line x=0 and 6 in from z=-50 is z=-44, so the 2x2 pad
            # straddles the symmetry line at (-0.5, -44.5). The spawns stand 88 blocks apart.
            "spawns": [{"id": "spawn-1", "piece": "gate", "at": [10, 6], "facing": "back"}],
        },
    }


# ── the casemate: a vault under the middle, and the one slot that lights it ──────────────────────
PIT = (-19, -13, 18, 12)                 # the hole cut in the terreplein, 38 x 26
SLOT = (-19, -4, 18, 3)                  # the strip left open to the sky, straight over the pad


def casemate_relief():
    """The vault is cut by relief rather than built by a layer: an `area` mark states the floor and,
    with no bevel, meets the terreplein on a step -- which is the seven-block wall that makes the
    casemate a room instead of a dip.

    Both ramps run down the board's own x axis, one from each end, so the pair is symmetric in z as well
    as in x and each team meets the same descent. Three points, not two: the first segment is level, so
    the ramp's head is flush with the works it leaves rather than landing wherever the cell grid rounds
    a two-point mark to."""
    x0, z0, x1, z1 = PIT
    return [
        {"id": "works-flat", "kind": "area", "h": DECK,
         "ring": [[-54.5, -38.5], [53.5, -38.5], [53.5, 37.5], [-54.5, 37.5]]},
        {"id": "cistern", "kind": "area", "h": VAULT,
         "ring": [[x0 - 0.5, z0 - 0.5], [x1 + 0.5, z0 - 0.5], [x1 + 0.5, z1 + 0.5], [x0 - 0.5, z1 + 0.5]]},
        {"id": "ramp-north", "kind": "line", "r": 3,
         "points": [[-0.5, -31.5], [-0.5, -25.5], [-0.5, -14.5]], "h": [DECK, DECK, VAULT]},
        {"id": "ramp-south", "kind": "line", "r": 3,
         "points": [[-0.5, 30.5], [-0.5, 24.5], [-0.5, 13.5]], "h": [DECK, DECK, VAULT]},
    ]


def lid():
    """The casemate's ceiling: plates at y20 over the aisles either side of the slot, so the vault is a
    roofed room with one light well down the middle of it. The plate is a course over the terreplein
    rather than flush with it, because a plate sized into the hole is driven into the ground beside it
    (`SK10`) and a plate sized to the ring is an island nobody can step onto (`SK11`).

    The relief solves on the CELL grid, two blocks to a cell, so the hole an `area` ring cuts is the
    cells its ring covers and not the blocks its corners name -- which is why the plates reach two blocks
    past the ring on every side and land on the rim whatever the rounding did.

    Each aisle carries two holes, placed as a mirrored pair so the roof reads the same from either flank.
    A hole is a seven-block drop into the aisle: a route in, and never a route out."""
    x0, z0, x1, z1 = PIT
    x0, x1, z0, z1 = x0 - 2, x1 + 2, z0 - 2, z1 + 2
    slot_z0, slot_z1 = SLOT[1], SLOT[3]
    plates = []
    for aisle, (az0, az1) in (("n", (z0, slot_z0 - 1)), ("s", (slot_z1 + 1, z1))):
        for at, (px0, px1) in enumerate(((x0, -14), (-7, 6), (13, x1))):
            plates.append(rect(f"lid-{aisle}{at}", (px0, az0, px1, az1), LID - VAULT, 1, "lid"))
    return plates


# ── the works above: what breaks a sightline, and what takes a section out of play ───────────────
def structure():
    """Everything above the terreplein, authored in the NORTH-WEST quadrant alone and fanned into the
    other three. A shape that straddles an axis is drawn up to it and its mirror completes it, so the
    board is symmetric in x and in z and not only under the half-turn."""
    shapes = []

    # Two pillars per quadrant, ten blocks wide and eight tall: not an obstacle but a decision, because
    # a player goes round one from either side and neither side can see the other.
    #
    # Nothing climbs one, and that is the point. `SK11` reports their tops as standable ground with no
    # route onto it and says outright to leave it where a detached group is what the thing is: a pillar
    # is cover, and a pillar a team can stand on top of is a firing platform in the middle of the works.
    shapes += fanned("pillar-mid", (-34, -26, -25, -17), 0, 8, "works")
    shapes += fanned("pillar-lane", (-16, -30, -7, -21), 0, 8, "works")

    # The traverses: a wall across the run out of each gate house, so leaving the spawn is a choice of
    # lane rather than a straight line at the objective. This is the large cover of `match-flow.md`
    # §10.4 -- it takes a section out of play rather than breaking one line.
    shapes += fanned("traverse", (-22, -30, -6, -28), 0, 6, "works")
    shapes += fanned("traverse-flank", (-46, -26, -38, -24), 0, 6, "works")

    # The bay: three walls and one mouth, so each flank point is entered from the middle or through its
    # own back door and from nowhere else. Drawn to the z axis; the mirror closes it.
    shapes += fanned("bay-outer", (-48, -13, -46, -3), 0, 5, "works")
    shapes += fanned("bay-north", (-48, -15, -30, -13), 0, 5, "works")

    # The rampart, and the one-way port off it. Two blocks is a step nobody climbs back up, so a player
    # walking the rampart drops into the bay through the gap in its outer wall and cannot leave that way.
    shapes += fanned("rampart", (-54, -15, -49, -1), 0, 2, "works")
    shapes += fanned("rampart-stair", (-54, -20, -49, -16), 0, 1, "works")
    shapes += fanned("sally-step", (-48, -2, -46, -1), 0, 2, "works")

    # Small cover: boxes two and three tall, each placed on a line that needs breaking. None within ten
    # blocks of a gate house -- cover at a spawn breaks nothing, because the ground in front of a door
    # is where a team already stands.
    #
    # None of them stands over the vault's roof plate either, which is a course of its own at the same
    # height and would build as one mass with them.
    boxes = [((-30, -34, -27, -31), 3),     # the lane out of the traverse's west end
             ((-14, -36, -11, -33), 2),     # beside the ramp head, breaking the run down it
             ((-40, -20, -37, -17), 2),     # inside the bay's mouth
             ((-28, -10, -25, -7), 3),      # between the bay and the vault rim
             ((-36, -34, -33, -31), 2)]     # the outer lane, before the rampart stair
    for at, (box, height) in enumerate(boxes):
        shapes += fanned(f"cover-{at}", box, 0, height, "works")
    return shapes


# ── what a team walks out of ─────────────────────────────────────────────────────────────────────
def band(*bands):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def window(form, block, width=1, height=2, sill=2, spacing=4):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": 0,
            "sill": sill, "width": width, "height": height, "spacing": spacing}


def gate_house():
    """The gate. A capture board is a work of masonry and the thing a team walks out of is part of it, so
    the gate house is the same stone as the traverses: a flat-roofed block with a parapet, not a cottage
    and not the shell's plain box.

    Flat because the works are flat -- a pitched roof on a fort reads as a farm -- and because a parapet
    course over an air course is what a battlement is: the top storey states one block of stone over two
    of nothing, so the stamp writes a rail and leaves the walk behind it open.

    A band of the owner's clay runs through the wall at eye height and the parapet is laid in it outright,
    so a player can tell whose gate they are looking at from across the works -- which on a board whose
    every structure is the same stone is the only thing that says so."""
    stone, chiselled, cobble = solid(98), solid(98, 3), solid(4)
    andesite, air = solid(1, 6), {"kind": "solid", "id": 0, "data": 0}
    return {
        "foundation": {
            "plate": {**band((stone, 1)), "extent": 2},
            "surface": {"field": andesite, "border": chiselled, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": False},
            "footing": cobble,
        },
        "wall": {**band((cobble, 1), (stone, 2), (team_clay(chiselled), 1), (stone, 1)), "extent": 5},
        "post": chiselled,
        "windows": window("slabBanded", 44, width=2, height=2, sill=2, spacing=5),
        "storeys": [
            {"clear": 4, "wall": band((cobble, 1), (stone, 2), (team_clay(chiselled), 1), (stone, 1)),
             "post": chiselled,
             "windows": window("slabBanded", 44, width=2, height=2, sill=2, spacing=5),
             "surface": {"field": andesite, "border": chiselled, "borderWidth": 1,
                         "inlay": None, "inlayInset": 2, "isPlain": False},
             "deck": andesite, "headroom": 4},
            # The battlement: one course of parapet, then two of air, so the walk behind it is open.
            {"clear": 3, "wall": band((team_clay(chiselled), 1), (air, 2)), "post": chiselled,
             "windows": window("none", 0), "surface": None, "deck": andesite, "headroom": 3},
        ],
        "roof": {"form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": False, "hole": False,
                 "body": andesite, "verge": chiselled, "gable": None,
                 "gableWindows": window("none", 0)},
        "beams": {"block": -1, "data": 0, "reach": 1},
        "doorway": {"door": "air", "width": 4, "height": 4,
                    "head": {"form": "none", "block": 109, "fill": "upperSlab",
                             "fillBlock": 44, "fillData": 5}},
        "porch": None,
        "front": None,
    }


# ── what it is made of ───────────────────────────────────────────────────────────────────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def cell(seed, size, *palette):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": list(palette)}


def depth_stack(*bands):
    return {"kind": "layered", "stack": {"ending": "repeat",
                                         "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def by_slope(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


# The works are laid stone: flagged where it is walked, a rougher setts course where the ramps fall,
# rubble where a face is exposed. The board is structural, so the surface is nearly all one band and the
# slope axis is doing a smaller job than it does on a landscape board -- but the ramps are the one place
# the ground turns, and they are what the second band is for.
def team_clay(neutral):
    """A course of the owning team's colour, in stained clay, falling back where no team owns the cell.
    It reads `team` off the board's own territory decomposition, so the works near a gate house come out
    in that team's colour and the middle -- which is nobody's -- comes out in the neutral behind it.
    That is the whole point of using it on a capture board: the ground says whose end you are standing at
    without a sign, and says nothing at all where the answer is the thing being fought over."""
    return {"kind": "teamTint", "blockId": 159, "neutral": neutral}


# The works are laid stone: flagged where they are walked, a rougher setts course where the ramps fall,
# rubble where a face is exposed. No mossy anything -- a board made of cobblestone and stone brick has
# no business carrying a green block, and the two mossy variants are the only green in the palette.
FLAGS = depth_stack((cell(5, 7, solid(1, 6), solid(98), solid(1, 6), solid(98, 0)), 1),
                    (solid(1), 2))
SETTS = depth_stack((cell(9, 4, solid(4), solid(98, 2), solid(4), solid(98)), 1), (solid(1), 2))
RUBBLE = cell(11, 5, solid(4), solid(98, 2), solid(98), solid(4))

# The exposed riser, as bedded masonry with a course of the owner's colour banded through it. A wall
# run varies along the arc and is flat inside a plateau, so this is what the casemate's seven-block face
# and every wall the works raise are read off.
WALL_RUN = {"kind": "wallRun", "runs": [{"width": 4, "material": {"kind": "layered", "layers": [
    {"material": solid(98), "thickness": 3},
    {"material": solid(98, 3), "thickness": 1},
    {"material": team_clay(solid(4)), "thickness": 1},
    {"material": solid(4), "thickness": 2},
    {"material": solid(98), "thickness": 4},
    {"material": team_clay(solid(98, 2)), "thickness": 1},
    {"material": solid(98, 2), "thickness": 1},
]}}]}


def works_theme():
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": solid(98, 3), "depth": 1, "enabled": True},
        "surface": {"material": by_slope((FLAGS, 8), (SETTS, 26), (RUBBLE, 56)), "depth": 3,
                    "enabled": True},
        # The seven-block face round the casemate is the one the whole board is read off, so it is
        # bedded rather than flat: a wall of one material reads as a cut and not as masonry.
        "wall": WALL_RUN,
        "wallEnabled": True,
        # Cobblestone, not andesite. The body of the board is eighteen courses deep on every exposed
        # face and every pit wall, so the fill is the single material most of the map is made of --
        # and andesite is the green one.
        "fill": solid(4),
    }


def vault_theme():
    """Under the lid. Darker and damper than the works over it, so a player can tell at a glance which
    storey they are standing on -- which is the whole of what a second theme is for on a board whose
    two levels share a footprint."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": solid(98, 3), "depth": 1, "enabled": True},
        "surface": {"material": depth_stack(
            (cell(13, 5, solid(98, 2), solid(4), solid(98), solid(98, 2)), 1), (solid(1), 2)),
            "depth": 2, "enabled": True},
        "wall": WALL_RUN,
        "wallEnabled": True,
        "fill": solid(4),
    }


def lid_theme():
    """The vault's roof, walked on from above and looked up at from inside it. Masonry, like everything
    else the works are made of: a timber plate over a stone board reads as a platform somebody left there
    rather than as the lid of the room under it, and a lid nobody can name is a lid nobody knows to
    look under. Its rim is the one course that differs, so the edge a player drops past is legible."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "rim": {"material": solid(98, 3), "depth": 1, "enabled": True},
        "surface": {"material": depth_stack((cell(17, 6, solid(98), solid(4), solid(98)), 1)),
                    "depth": 1, "enabled": True},
        "wall": {"kind": "layered", "layers": [
            {"material": solid(98), "thickness": 2},
            {"material": team_clay(solid(98, 3)), "thickness": 1},
        ]},
        "wallEnabled": True,
        "fill": solid(98),
    }


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-12",
        "relief": {"*": {"base": DECK, "reach": 0, "step": 1, "landform": "plain",
                         "grain": {"amplitude": 0.0, "scale": 24, "seed": 3},
                         "marks": casemate_relief()}},
        "addLayers": [
            {"id": "lid", "name": "The lid", "base_y": VAULT,
             "shapes": lid(), "groups": [{"id": "lid", "shapeIds": [s["id"] for s in lid()]}]},
            {"id": "works", "name": "The works", "base_y": DECK,
             "shapes": structure(),
             "groups": [{"id": "works", "shapeIds": [s["id"] for s in structure()]}]},
        ],
        "roomStyles": {"spawn": gate_house()},
        "themes": {"works": works_theme(), "vault": vault_theme(), "lid": lid_theme()},
        "mapTheme": "works",
        "controlPoints": [
            {"name": "The Cistern", "anchor": {"x": CISTERN_ANCHOR, "y": 0, "z": -1},
             "size": HILL, "points": CENTRE_POINTS},
            {"name": "West Bay", "anchor": {"x": WEST_BAY_ANCHOR, "y": 0, "z": -1},
             "size": HILL, "points": FLANK_POINTS},
            {"name": "East Bay", "anchor": {"x": EAST_BAY_ANCHOR, "y": 0, "z": -1},
             "size": HILL, "points": FLANK_POINTS},
        ],
        "scoreLimit": 750,
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
