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
EAST_BAY_ANCHOR = 28     # blocks [25, 32], centre 28.5 -- 29 out
WEST_BAY_ANCHOR = -30    # blocks [-33, -26]: the image of the east pad
HALF_SEPARATION = 44     # 0.66 x 44 = 29, the corpus median for an off-centre point


def mirrored(x0, z0, x1, z1):
    """The rot_180 image of a block rect. b -> -1-b on both axes, so a rect's corners swap."""
    return (-1 - x1, -1 - z1, -1 - x0, -1 - z0)


def rect(shape_id, box, floor, height, theme, group=None, layer=None):
    x0, z0, x1, z1 = box
    out = {"id": shape_id, "type": "rectangle", "operation": "add",
           "min_x": x0, "min_z": z0, "max_x": x1 + 1, "max_z": z1 + 1,
           "floor": floor, "base_height": height, "theme": theme}
    if group: out["group"] = group
    if layer: out["layer"] = layer
    return out


def pair(shape_id, box, floor, height, theme):
    """One structure and its image, both written out."""
    return [rect(f"{shape_id}-a", box, floor, height, theme),
            rect(f"{shape_id}-b", mirrored(*box), floor, height, theme)]


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
    casemate a room instead of a dip. Two line marks ramp down into its ends."""
    x0, z0, x1, z1 = PIT
    # The ramps come down into the vault's ENDS, along z, and not along x. Along x they would run into
    # the flank bays, and a pad whose own footprint spans a ramp trench is a pad the stamper builds as a
    # plinth over the hole instead of a floor on the ground.
    #
    # Seven blocks of fall over twelve of run: every step is one, so each is walked in both directions --
    # which is what separates a ramp from the drop holes in the roof, and the board needs both.
    ramps = [
        # Three points, not two: the first segment is level, so the ramp's head is flush with the works
        # it leaves. A two-point mark's head lands wherever the cell grid rounds it to, and a ramp whose
        # first step is a six-block drop is a hole with a slope at the bottom of it.
        {"id": "ramp-north", "kind": "line", "r": 3,
         "points": [[-15.5, -31.5], [-15.5, -25.5], [-15.5, -14.5]], "h": [DECK, DECK, VAULT]},
        {"id": "ramp-south", "kind": "line", "r": 3,
         "points": [[14.5, 30.5], [14.5, 24.5], [14.5, 13.5]], "h": [DECK, DECK, VAULT]},
    ]
    return [
        {"id": "works-flat", "kind": "area", "h": DECK,
         "ring": [[-54.5, -38.5], [53.5, -38.5], [53.5, 37.5], [-54.5, 37.5]]},
        {"id": "cistern", "kind": "area", "h": VAULT,
         "ring": [[x0 - 0.5, z0 - 0.5], [x1 + 0.5, z0 - 0.5], [x1 + 0.5, z1 + 0.5], [x0 - 0.5, z1 + 0.5]]},
        *ramps,
    ]


def lid():
    """The casemate's ceiling: two plates at y19 covering the aisles either side of the slot, so the
    vault is a roofed room with one light well down the middle of it. Standing on a plate is standing on
    the terreplein -- its top course is the course the open ground is at.

    Each plate carries a hole a player falls through and cannot climb back out of (`match-flow.md` §10.5):
    seven blocks down into the aisle, which is a route in and never a route out."""
    x0, z0, x1, z1 = PIT
    slot_z0, slot_z1 = SLOT[1], SLOT[3]
    # The relief solves on the CELL grid, two blocks to a cell, so the hole an `area` ring cuts is the
    # cells its ring covers and not the blocks its corners name. A plate sized to the ring leaves a slot
    # round the vault the width of that rounding, and the plate is then an island nobody can step onto
    # (`SK11`). Reaching two blocks past the ring on every side lands the plate on the rim whatever the
    # rounding did, and flush with the terreplein rather than driven into it.
    x0, x1, z0, z1 = x0 - 2, x1 + 2, z0 - 2, z1 + 2
    # Each aisle roof is two plates with a gap between them: the gap is a hole a player falls seven
    # blocks through onto the vault floor and cannot climb back out of.
    return [rect("lid-n1", (x0, z0, -13, slot_z0 - 1), LID - VAULT, 1, "lid"),
            rect("lid-n2", (-6, z0, x1, slot_z0 - 1), LID - VAULT, 1, "lid"),
            rect("lid-s1", (x0, slot_z1 + 1, 5, z1), LID - VAULT, 1, "lid"),
            rect("lid-s2", (12, slot_z1 + 1, x1, z1), LID - VAULT, 1, "lid")]


# ── the works above: what breaks a sightline, and what takes a section out of play ───────────────
def structure():
    shapes = []

    # Two pillars per half, ten blocks wide and eight tall: not an obstacle but a decision, because a
    # player goes round one from either side and neither side can see the other.
    #
    # Nothing climbs one, and that is the point. `SK11` reports their tops as standable ground with no
    # route onto it and says outright to leave it where a detached group is what the thing is: a pillar
    # is cover, and a pillar a team can stand on top of is a firing platform in the middle of the works.
    shapes += pair("pillar-in", (-25, -25, -16, -16), 0, 8, "works")
    shapes += pair("pillar-out", (15, -25, 24, -16), 0, 8, "works")

    # The bays. Three walls and one mouth, so each flank point is entered from the centre or through
    # its own back door and from nowhere else.
    for side, sign in (("w", -1), ("e", 1)):
        outer = (21, -12, 23, 9) if sign < 0 else (-24, -10, -22, 11)
        pass
    # West bay: pad at [-33,-26] x [-4,3]. Walls on north, south and the outer (-x) face.
    shapes += [rect("bay-w-out1", (-38, -12, -36, -3), 0, 5, "works"),
               rect("bay-w-out2", (-38, 2, -36, 11), 0, 5, "works"),
               rect("bay-w-n", (-38, -14, -22, -12), 0, 5, "works"),
               rect("bay-w-s", (-38, 11, -22, 13), 0, 5, "works")]
    shapes += [rect("bay-e-out1", (35, 2, 37, 11), 0, 5, "works"),
               rect("bay-e-out2", (35, -12, 37, -3), 0, 5, "works"),
               rect("bay-e-n", (21, 11, 37, 13), 0, 5, "works"),
               rect("bay-e-s", (21, -14, 37, -12), 0, 5, "works")]

    # The rampart: a two-block walk round each flank that enters its bay through the gap in the outer
    # wall and drops two into it. Two blocks is a step nobody climbs back up, so the port runs one way.
    shapes += pair("rampart", (-46, -14, -39, 13), 0, 2, "works")
    shapes += pair("rampart-step", (-38, -2, -36, 1), 0, 2, "works")

    # The way up onto it: a one-block step, then the walk. Two blocks in one go is a scramble, and a
    # route a player cannot take in both directions by walking is a route only half the board has.
    shapes += pair("rampart-stair", (-47, -18, -39, -15), 0, 1, "works")

    # The traverses: two long walls per half, standing across the run from a gate house to the middle so
    # that leaving the spawn is a choice of lane rather than a straight line at the objective. This is the
    # large cover of `match-flow.md` §10.4 -- it takes a section out of play rather than breaking one line.
    shapes += pair("traverse-in", (-34, -30, -12, -28), 0, 6, "works")
    shapes += pair("traverse-out", (2, -30, 30, -28), 0, 6, "works")
    shapes += pair("traverse-flank", (-48, -30, -40, -28), 0, 6, "works")

    # Small cover: boxes two and three tall, placed on the lines that need breaking rather than strewn.
    # An open square with nothing on it is a square nobody crosses. None of them stands over the vault's
    # roof plate, which is a course of its own at the same height and would build as one mass with them.
    boxes = [((-12, -36, -9, -33), 3), ((4, -36, 7, -33), 3),
             ((-32, -26, -29, -23), 2), ((24, -26, 27, -23), 2),
             ((-6, -22, -2, -18), 2), ((-46, -6, -43, -3), 3),
             ((-30, -20, -27, -17), 2), ((8, -22, 11, -19), 2),
             ((-38, -24, -35, -21), 2), ((30, -22, 33, -19), 3),
             ((-44, -34, -41, -31), 2), ((40, -34, 43, -31), 2),
             ((-50, -18, -47, -15), 2), ((44, -12, 47, -9), 3),
             ((16, -24, 19, -21), 2), ((-20, -34, -17, -31), 2)]
    for at, (box, height) in enumerate(boxes):
        shapes += pair(f"cover-{at}", box, 0, height, "works")
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
    of nothing, so the stamp writes a rail and leaves the walk behind it open."""
    stone, chiselled, cobble = solid(98), solid(98, 3), solid(4)
    mossy, andesite, air = solid(98, 1), solid(1, 6), {"kind": "solid", "id": 0, "data": 0}
    return {
        "foundation": {
            "plate": {**band((stone, 1)), "extent": 2},
            "surface": {"field": andesite, "border": chiselled, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": False},
            "footing": cobble,
        },
        "wall": {**band((cobble, 1), (stone, 4)), "extent": 5},
        "post": chiselled,
        "windows": window("slabBanded", 44, width=2, height=2, sill=2, spacing=5),
        "storeys": [
            {"clear": 4, "wall": band((cobble, 1), (stone, 3), (mossy, 1)), "post": chiselled,
             "windows": window("slabBanded", 44, width=2, height=2, sill=2, spacing=5),
             "surface": {"field": andesite, "border": chiselled, "borderWidth": 1,
                         "inlay": None, "inlayInset": 2, "isPlain": False},
             "deck": andesite, "headroom": 4},
            # The battlement: one course of parapet, then two of air, so the walk behind it is open.
            {"clear": 3, "wall": band((chiselled, 1), (air, 2)), "post": chiselled,
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
FLAGS = depth_stack((cell(5, 7, solid(1, 6), solid(98), solid(1, 6), solid(98, 0)), 1),
                    (solid(1), 2))
SETTS = depth_stack((cell(9, 4, solid(4), solid(98, 2), solid(4), solid(1, 5)), 1), (solid(1), 2))
RUBBLE = cell(11, 5, solid(4), solid(98, 1), solid(1, 5), solid(4))

WALL_RUN = {"kind": "wallRun", "runs": [{"width": 4, "material": {"kind": "layered", "layers": [
    {"material": solid(98), "thickness": 3},
    {"material": solid(98, 3), "thickness": 1},
    {"material": solid(4), "thickness": 2},
    {"material": solid(98), "thickness": 4},
    {"material": solid(98, 1), "thickness": 2},
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
        "fill": solid(1, 5),
    }


def vault_theme():
    """Under the lid. Darker and damper than the works over it, so a player can tell at a glance which
    storey they are standing on -- which is the whole of what a second theme is for on a board whose
    two levels share a footprint."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": solid(98, 1), "depth": 1, "enabled": True},
        "surface": {"material": depth_stack(
            (cell(13, 5, solid(98, 1), solid(4), solid(98, 2), solid(98, 1)), 1), (solid(1), 2)),
            "depth": 2, "enabled": True},
        "wall": WALL_RUN,
        "wallEnabled": True,
        "fill": solid(1, 5),
    }


def lid_theme():
    """The ceiling plate, seen from under it as much as walked on, so it is timbered rather than flagged."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "rim": {"material": solid(17, 1), "depth": 1, "enabled": True},
        "surface": {"material": depth_stack((cell(17, 6, solid(98), solid(1, 6), solid(98)), 1)),
                    "depth": 1, "enabled": True},
        "wall": {"kind": "solid", "id": 17, "data": 1},
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
             "size": HILL, "points": 1},
            {"name": "West Bay", "anchor": {"x": WEST_BAY_ANCHOR, "y": 0, "z": -1},
             "size": HILL, "points": 1},
            {"name": "East Bay", "anchor": {"x": EAST_BAY_ANCHOR, "y": 0, "z": -1},
             "size": HILL, "points": 1},
        ],
        "scoreLimit": 750,
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
