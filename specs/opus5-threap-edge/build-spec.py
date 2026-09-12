#!/usr/bin/env python3
"""Threap Edge — the first King of the Hill board.

A gritstone edge runs east-west across the middle of a moor, and the three hills are cut into it: one on
the summit at the edge's centre and one on each nab where the crest breaks down toward the flanks. Both
teams spawn on low moorland, north and south, so the crest is the same climb from either side and no
point is anybody's doorstep.

The layout is the author's rule for a capture board (`docs/gameplay/approaches.md`): one point dead
centre and the rest **across** the line between the spawns rather than along it, because a point belongs
to nobody and the only positions that are the same walk for everyone lie on the map's own axis of
symmetry. The nabs sit at 0.66 of the centre-to-spawn distance, which is the corpus median.

    python3 specs/opus5-threap-edge/build-spec.py     writes the plan and the finish beside this file
"""

import json
import os

SLUG = "opus5-threap-edge"
HERE = os.path.dirname(os.path.abspath(__file__))

CELL = 2                 # blocks per plan cell
MOOR = 12                # the low moor's surface
SUMMIT = 32              # the edge at its highest
NAB = 22                 # the two nabs the side hills stand on, 10 below the summit
SPAWN_SURFACE = MOOR

# The board's symmetry centre under rot_180 is the block boundary at -0.5: cell c images onto -1-c, so
# block b images onto -1-b. Every coordinate below is written about that, which is what lets a pad be its
# own mirror and a pair of pads be each other's.
MID = -0.5
HALF_SEPARATION = 48     # spawn to centre, so the spawns stand 96 blocks apart
NAB_OUT = 32             # 0.66 x 48, the corpus median for an off-centre point

# A hill is a square pad and the stamper centres it with Centred(anchor, size): minimum at anchor-(n-1)/2.
# An EVEN side is what puts a pad exactly on the symmetry line -- size 8 at anchor -1 spans [-4, 3], whose
# image under b -> -1-b is itself -- and what makes the two nabs exact images of each other.
HILL_SIZE = 8
MID_ANCHOR = -1                      # blocks [-4, 3]:  centred on -0.5
EAST_ANCHOR = 31                     # blocks [28, 35]: centre 31.5, i.e. 32 out
WEST_ANCHOR = -33                    # blocks [-36, -29]: the image of the east pad


def plan():
    return {
        "plan": 2,
        "meta": {"name": "Threap Edge"},
        "globals": {
            "cell": CELL,
            "symmetry": "rot_180",
            "maxPlayers": 16,
            "surface": MOOR,
            "observerY": 64,
        },
        "pieces": [
            # The moor is one shape, not a partition: the edge that crosses it is relief, and cutting the
            # board up so a theme had somewhere to hang is what makes a board read chopped.
            {"id": "moor", "role": "piece", "rect": [-27, -21, 54, 42], "surface": MOOR},
            # One spawn plateau; the symmetry fans the other. Blocks x[-10,9], z[-54,-43] -- 20x12, inside
            # ST9's 20x20 building cap and ST10's 20x30 region cap.
            {"id": "edge-head", "role": "spawn", "rect": [-5, -27, 10, 6], "surface": SPAWN_SURFACE},
        ],
        "placements": {
            # `at` is in blocks from the piece corner. 10 blocks in from x=-10 is the grid line x=0, so the
            # 2x2 spawn pad straddles the symmetry line; 6 in from z=-54 is z=-48, pad centre -48.5.
            "spawns": [{"id": "spawn-1", "piece": "edge-head", "at": [10, 6], "facing": "back"}],
        },
    }


def crest():
    """The edge itself: one line along z=-0.5, exactly self-symmetric under rot_180.

    Each x is the image of its partner (-1-x), so the mark maps onto itself rather than onto a copy a
    block away, and the height list is a palindrome for the same reason. The ridge is highest between the
    spawns and steps down through the two nabs to the moor at either end, so the three hills stand on one
    landform at three heights rather than on three pieces.

    The tread is nine of the fifteen-block reach, so the top is flat where the hills stand and the last six
    blocks of the band are the face: twenty blocks of fall over six at the summit, ten over six at the nabs.
    It grades into the moor's own mark rather than ending on it, which is what keeps the seam terrain
    instead of a wall nothing is named for (`RL3`)."""
    xs = [-54.5, -44.5, -32.5, -20.5, -0.5, 19.5, 31.5, 43.5, 53.5]
    hs = [MOOR, MOOR + 3, NAB, 28, SUMMIT, 28, NAB, MOOR + 3, MOOR]
    return {
        "id": "crest", "kind": "line", "r": 15, "tread": 9,
        "points": [[x, -0.5] for x in xs], "h": hs,
    }


def moor():
    """The flat the edge stands out of, pinned rather than left to the solver.

    With `reach` unlimited a mark decides the whole surface, so a board carrying one ridge and nothing else
    ramps from the ridge to its own corners and has nowhere level on it at all (`RL5`). Stating the flat is
    what makes the ground either side of the edge ground. Only the north half is authored; the fan carries
    it south."""
    return {
        "id": "moor", "kind": "area", "h": MOOR,
        "ring": [[-54.5, -54.5], [53.5, -54.5], [53.5, -16.5], [-54.5, -16.5]],
    }


def ramp(mark_id, cx):
    """The way up onto a nab: a corridor of moor lifted from the flat to the nab's own height, ending at
    the crest band's edge so the two meet at one number and leave no seam.

    Only the north pair is authored. The fan carries each onto the far nab's south side, so every nab is
    entered from both ends of the board and neither team starts closer to a way up than the other."""
    return {
        "id": mark_id, "kind": "line", "r": 8, "tread": 3,
        "points": [[cx, -32], [cx, -17]], "h": [MOOR, NAB],
    }


# ── what the ground is made of ───────────────────────────────────────────────────────────────────
# 1.8 block ids: 1 stone (:5 andesite, :3 diorite), 2 grass, 3 dirt (:1 coarse, :2 podzol),
# 4 cobblestone, 13 gravel.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def cell(size, *palette):
    return {"kind": "cell", "seed": 3, "cellSize": size, "jitter": max(1, size // 3),
            "warp": max(1, size // 4), "palette": list(palette)}


def mottle(seed, scale, *stops):
    """A fractal field folded on itself — billowy rather than drifting, which is what puts two ground
    materials through each other at the scale of a footstep instead of in fields of one and fields of the
    other. `stops` is read by the field's value, so a material repeated is a material weighted."""
    return {"kind": "turbulence", "seed": seed, "scale": scale, "octaves": 3, "stops": list(stops)}


def depth_stack(*bands):
    """A depth stack: what a column is made of downward from its own top."""
    return {"kind": "layered",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def by_slope(*bands):
    """The one rule that makes a relieved board read as relief: the surface is banded by the ground's own
    ANGLE, not by its height or by which plan piece it stands on. A thickness on this axis is a span of
    degrees, so one stack finishes the moor, the shoulder and the face of the same edge.

    The cuts are read off `GET .../incline?format=text`, which answers how much ground stands in each ten
    degrees: 49% under 10, 15% in the teens, 15% in the twenties, 7% in the thirties and 14% at 40 or
    steeper. So the moor takes everything under 14, the shoulder the run to 32, and the crag the rest."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


# Heather moor: podzol through grass at the scale a moor actually mottles at, which is a few blocks and
# not a few tens. Podzol beside grass is only a colour that works where the grass is **tinted away from
# green** — the biome below puts the whole board in swampland and mesa for exactly that reason.
MOOR_TOP = depth_stack(
    (mottle(17, 5, solid(2), solid(2), solid(3, 2), solid(2), solid(2), solid(3, 1),
            solid(3, 2), solid(2)), 1),
    (solid(3), 2))
SHOULDER = depth_stack((cell(9, solid(3, 1), solid(3, 1), solid(13)), 1), (solid(3), 2))
CRAG = cell(9, solid(1), solid(4), solid(1, 5), solid(1))


def theme():
    """One theme for the whole board. The edge is not a second material hung on a second piece — it is the
    same ground standing at a steeper angle, and the slope axis is what tells the two apart."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
        "surface": {"material": by_slope((MOOR_TOP, 14), (SHOULDER, 18), (CRAG, 45)), "depth": 3,
                    "enabled": True},
        # The riser the edge exposes, as bedded gritstone: a board whose faces are one flat material
        # reads as a cut rather than as rock.
        "wall": {"kind": "wallRun", "runs": [{"width": 5, "material": {"kind": "layered", "layers": [
            {"material": solid(1), "thickness": 3},
            {"material": solid(1, 5), "thickness": 1},
            {"material": solid(4), "thickness": 2},
            {"material": solid(1), "thickness": 4},
            {"material": solid(13), "thickness": 1},
            {"material": solid(1, 5), "thickness": 2},
        ]}}]},
        "wallEnabled": True,
        # Not 1:0: a column read has to say which theme filled it, and every board painting plain stone
        # answers the same thing whatever laid it.
        "fill": solid(1, 5),
    }


# ── what a team walks out of ─────────────────────────────────────────────────────────────────────
# The shooting box: the gritstone field house a moor like this carries, so the building a team spawns in
# is made of the board's own rock rather than the default shell's plain box. Walls of stone brick on a
# cobble plinth, spruce corner posts, and a gable roof stepped in stone-brick slabs the way a flagged
# roof lies. It stands two storeys because the spawn plateau sits below the edge and the board needs a
# thing on it that is visible from the crest.
def band(*bands):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def window(form, block, width=1, height=2, sill=2, spacing=4, data=0):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": data,
            "sill": sill, "width": width, "height": height, "spacing": spacing}


STONE, MOSSY, CHISELLED = solid(98), solid(98, 1), solid(98, 3)
# A laid log runs along the wall rather than standing up it, so the course shows bark down the side and
# the sawn face at the corners. It is the wall plate the beam ends come out of: beams over a course of
# masonry are eight logs stuck in stone with nothing behind them (`HS9`).
WALL_PLATE = {"kind": "laidLog", "id": 17, "data": 1}
COBBLE, SPRUCE_LOG, SPRUCE_PLANK = solid(4), solid(17, 1), solid(5, 1)
DRYSTONE = band((COBBLE, 1), (STONE, 4))


def spawn_house():
    return {
        "foundation": {
            "plate": {**band((STONE, 1)), "extent": 2},
            # A flagged floor inside a stone kerb, which is what the border is for.
            "surface": {"field": SPRUCE_PLANK, "border": STONE, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": False},
            "footing": COBBLE,
        },
        "wall": {**DRYSTONE, "extent": 5},
        "post": SPRUCE_LOG,
        "windows": window("pane", 102),
        "storeys": [
            # The room itself: four clear, a plank floor, small lights high in the wall.
            {"clear": 4, "wall": DRYSTONE, "post": SPRUCE_LOG, "windows": window("pane", 102),
             "surface": {"field": SPRUCE_PLANK, "border": STONE, "borderWidth": 1,
                         "inlay": None, "inlayInset": 2, "isPlain": False},
             "deck": SPRUCE_PLANK, "headroom": 4},
            # The loft over it: a mossy course, a chiselled band, and a spruce wall plate at the eave that
            # the beam ends come out of.
            {"clear": 3, "wall": band((MOSSY, 1), (CHISELLED, 1), (WALL_PLATE, 1)),
             "post": SPRUCE_LOG, "windows": window("open", 0, width=1, height=1, sill=1, spacing=3),
             "surface": None, "deck": SPRUCE_PLANK, "headroom": 3},
        ],
        "roof": {
            "form": "gable", "pitch": 1,
            # Stepped in stone-brick slabs: a flagged roof lies in halves, not in whole blocks.
            "slab": 44, "slabData": 5,
            "overhang": 1, "ridgeCap": True, "hole": False,
            "body": STONE, "verge": MOSSY, "gable": COBBLE,
            "gableWindows": window("open", 0, width=1, height=1, sill=1, spacing=3),
        },
        "beams": {"block": 17, "data": 1, "reach": 1},
        "doorway": {"door": "air", "width": 3, "height": 3,
                    "head": {"form": "arched", "block": 109, "fill": "upperSlab",
                             "fillBlock": 44, "fillData": 5}},
        "porch": None,
        "front": None,
    }


# ── what stands on it ────────────────────────────────────────────────────────────────────────────
# Only the north half is placed. The dressing pass fans every prop across the board's orbit, so a stone
# put on the north moor stands again on the south and the two halves cannot drift apart by hand.
def styles():
    """The recipes the props name. A prop's `style` is a key into the document's own registry rather than a
    name in the studio's library, so a spec builds the same board on any install."""
    grit = cell(4, solid(1), solid(4), solid(1, 5), solid(1))
    return {
        # Dry-stone, no moss: a summit cairn is built and kept bare.
        "cairn": {"kind": "boulder", "form": "cairn", "size": 4, "rock": grit, "mossy": False},
        "outcrop": {"kind": "boulder", "form": "outcrop", "size": 6, "rock": grit, "mossy": True},
        "shattered": {"kind": "boulder", "form": "angular", "size": 4, "rock": grit, "mossy": False},
        "erratic": {"kind": "boulder", "form": "round", "size": 5, "rock": solid(1), "mossy": True},
        "birch": {"kind": "tree", "form": "template", "species": "birch", "height": 7},
        "rowan": {"kind": "tree", "form": "template", "species": "oak", "height": 6},
    }


def boulder(prop_id, x, z, style, seed):
    return {"id": prop_id, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}


def tree(prop_id, x, z, style, seed):
    return {"id": prop_id, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}


def props():
    # Five, not twelve, and not one of them on the crag. A gritstone boulder standing on the crag band is
    # the same rock as the ground under it and disappears into it, so every position here is read off
    # `GET .../column?at=` first and stands where the ground measures under 20 degrees — the moor's grass
    # and podzol, or the shoulder's coarse dirt. The four that stood along the edge's face are gone.
    stones = [
        # A cairn on a moor top is what marks a summit, so the summit and one nab carry one — standing on
        # the crest's own flat (11-16 degrees, so the shoulder band's brown) rather than against the face.
        boulder("cairn-mid", -12, -1, "cairn", 21),
        boulder("cairn-nab", -45, -1, "cairn", 22),
        # Erratics dropped on the flat, which is what says the moor was left by ice. All three stand at
        # 0 degrees, where the ground is grass and podzol.
        boulder("erratic-a", -20, -30, "erratic", 51),
        boulder("erratic-c", 37, -28, "erratic", 53),
        boulder("scree-a", -40, -30, "shattered", 41),
    ]
    # Sparse and low down: a moor top carries no trees, and the shelter is at the foot of the edge.
    trees = [
        tree("birch-a", -15, -26, "birch", 61),
        tree("birch-b", 15, -29, "birch", 62),
        tree("rowan-a", -39, -37, "rowan", 63),
        tree("rowan-b", 45, -35, "rowan", 64),
        tree("thorn", 42, -24, "birch", 65),
    ]
    heather = {
        "id": "heather", "kind": "flora", "seed": 7,
        "points": [[-54, -44], [53, -44], [53, -17], [-54, -17]],
        # Ferns and tall grass carry it; flowers are the thing a moor does not have much of.
        "spec": {"coverage": 0.82, "scale": 7, "octaves": 3, "fernShare": 0.55,
                 "flowerShare": 0.02, "flowerScale": 21, "tallShare": 0.22},
    }
    # The sheep-tracks off the spawn, one to each nab's ramp. They are the routes the board is walked on,
    # drawn so a player can see where the ways up are from the door.
    tracks = [
        {"id": "track-west", "kind": "stroke", "seed": 5, "radius": 2.0, "style": "rough",
         "coverage": 0.75, "claimsGround": True,
         "points": [[-2, -44], [-14, -40], [-25, -35], [-32, -29], [-32, -20]],
         "pave": {"kind": "cell", "cellSize": 5,
                  "palette": [solid(3, 1), solid(13), solid(3, 1), solid(1, 5)]}},
        {"id": "track-east", "kind": "stroke", "seed": 6, "radius": 2.0, "style": "rough",
         "coverage": 0.75, "claimsGround": True,
         "points": [[1, -44], [13, -40], [24, -35], [31, -29], [31, -20]],
         "pave": {"kind": "cell", "cellSize": 5,
                  "palette": [solid(3, 1), solid(13), solid(3, 1), solid(1, 5)]}},
    ]
    return [*tracks, heather, *stones, *trees]


def finish():
    return {
        "authors": [{"name": "Opus 5"}],
        "created": "2026-09-12",
        "relief": {
            "*": {
                "base": MOOR,
                "reach": 0,
                "step": 1,
                "landform": "rolling",
                "grain": {"amplitude": 0.6, "scale": 19, "seed": 31},
                "marks": [
                    crest(),
                    # The moor before the ramps: a cell takes the last mark that claims it, and a ramp has
                    # to win the corridor it cuts through the flat.
                    moor(),
                    ramp("ramp-west", -32.5),
                    ramp("ramp-east", 31.5),
                ],
            },
        },
        # Swampland drifting into mesa — 6 tints grass #6a7039 and 37 tints it #90814d, both olive rather
        # than green. It is the biome that makes the ground's own palette legal: podzol reads as heather
        # beside an olive grass and as a brown hole beside a green one, so the mix above is only right
        # under these two. Folded through the board's symmetry with everything else.
        "biome": {"kind": "noise", "seed": 11, "scale": 46, "octaves": 2, "stops": [6, 6, 37, 6]},
        "roomStyles": {"spawn": spawn_house()},
        "dressing": {"styles": styles(), "props": props()},
        "themes": {"threap-moor": theme()},
        "mapTheme": "threap-moor",
        # Three hills: the summit between the spawns and a nab to each side, every one of them stated,
        # because a compiled intent carries no symmetry and nothing downstream will fan them.
        "controlPoints": [
            {"name": "The Edge", "anchor": {"x": MID_ANCHOR, "y": 0, "z": -1},
             "size": HILL_SIZE, "points": 1},
            {"name": "West Nab", "anchor": {"x": WEST_ANCHOR, "y": 0, "z": -1},
             "size": HILL_SIZE, "points": 1},
            {"name": "East Nab", "anchor": {"x": EAST_ANCHOR, "y": 0, "z": -1},
             "size": HILL_SIZE, "points": 1},
        ],
        "scoreLimit": 750,
    }


if __name__ == "__main__":
    with open(f"{HERE}/{SLUG}.plan.json", "w") as handle:
        json.dump(plan(), handle, indent=2)
    with open(f"{HERE}/{SLUG}.finish.json", "w") as handle:
        json.dump(finish(), handle, indent=2)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
