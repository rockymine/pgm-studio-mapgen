#!/usr/bin/env python3
"""Whitstone Weald — writes whitstone-weald.plan.json and whitstone-weald.refinement.json beside itself.

A dry heath of acacia and olive on banded red rock, for 32 a side. Each team holds two end-stone monuments:
the Crag Stone on a bench under a red crag with a wood on its outer flank, and the Green Stone on a village
green with a stone-built hamlet behind it and an old rock-cut cistern under the ground in front of it, reached
from a sunken court at the strait and by a stepped cutting beside the green.

Every coordinate below is team red's (x < 0); the plan is rot_180 and the studio fans the rest. Every height
is a column height, as `base_height` states one: the top block is one lower.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SLUG = os.path.basename(HERE)

# ── the board's numbers, in blocks ──────────────────────────────────────────────────────────────
HALF_W = 72                           # z runs -72..72
CRAG_STONE = (-82, -36)               # the north monument
GREEN_STONE = (-82, 36)               # the south monument

# ── the cistern ─────────────────────────────────────────────────────────────────────────────────
FLOOR_H = 12                       # every cistern floor: top block y11, a player stands at y12
ROOF_FLOOR = 16                       # the rock over the culvert and the hall starts here: 4 of air
RIM_H = 18                            # the court's rim, where the stair starts down
GREEN_H = 20                          # the green round the Green Stone, where the cutting surfaces
COURT = (-30, 48, -16, 66)           # the sunken court, open to the strait: min_x, min_z, max_x, max_z
COURT_STAIR = (-34, 48, -22, 52)        # the court stair, 6 down over 12, from the rim to the court floor
CULVERT = (-60, 55, -30, 60)          # the culvert, roofed, 30 long and 5 wide
HALL = (-76, 52, -60, 64)          # the cistern hall, roofed, 16 x 12, four pillars round a pool
CUTTING = (-70, 34, -65, 52)          # an open cutting climbing 8 over 18 to the green
CISTERN_POOL = (-70, 55, -66, 61)     # the water in the middle of the hall
POND = (-43, 2)                       # the pond at the front of the Hog's Back, between the two stones


def ring(cx, cz, r, n=14, lobes=0.0, phase=0.0, sx=1.0, sz=1.0):
    """A closed outline of n points round (cx, cz), lobed by a gentle cosine so it reads as ground."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1.0 + lobes * math.cos(3 * a + phase)
        out.append([round(cx + r * k * sx * math.cos(a), 1), round(cz + r * k * sz * math.sin(a), 1)])
    return out


def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


POND_RING = ring(*POND, 9, lobes=0.1, sz=1.15)


# ── the plan ────────────────────────────────────────────────────────────────────────────────────
def plan():
    cells = HALF_W // 4
    return {
        "plan": 2,
        "meta": {"name": "Whitstone Weald", "authors": ["Opus 5.5"],
                 "notes": "A heath of acacia and olive on red rock, two end-stone monuments a team, a cistern under the south."},
        "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 32, "surface": 20, "observerY": 74},
        "pieces": [
            {"id": "weald", "rect": [-32, -cells, 28, 2 * cells]},
            {"id": "weald-n", "rect": [-37, -cells, 5, cells - 3]},
            {"id": "weald-s", "rect": [-37, 3, 5, cells - 3]},
            {"id": "yard", "role": "spawn", "rect": [-37, -3, 5, 6]},
        ],
        "zones": [{"id": "strait", "rect": [-4, -cells, 4, 2 * cells]}],
        "placements": {
            "spawns": [{"id": "spawn", "piece": "yard", "at": [10, 12], "facing": "right",
                        "footprint": [3, 3, 14, 18]}],
            "destroyables": [
                {"id": "crag-stone", "at": list(CRAG_STONE), "style": "cube-4", "materials": "ender stone",
                 "float": 4, "name": "Crag Stone"},
                {"id": "green-stone", "at": list(GREEN_STONE), "style": "cube-4", "materials": "ender stone",
                 "float": 4, "name": "Green Stone"},
            ],
        },
    }


# ── the outline: the fused field reshaped one point at a time ───────────────────────────────────
class Ring:
    """The compiled outline as the studio holds it, so each op names the index the ring has when it runs.
    The studio refuses any op that folds the ring, so the order the points go in is part of the design."""

    def __init__(self, points):
        self.points = [tuple(p) for p in points]
        self.ops = []

    def insert_after(self, before, point):
        at = self.points.index(tuple(before))
        self.points.insert(at + 1, tuple(point))
        self.ops.append({"after": at, "x": point[0], "z": point[1]})

    def move(self, old, new):
        at = self.points.index(tuple(old))
        self.points[at] = tuple(new)
        self.ops.append({"index": at, "x": new[0], "z": new[1]})

    def run(self, before, points):
        for point in points:
            self.insert_after(before, point)
            before = point


V0, V1, V2, V3 = (-148, -HALF_W), (-16, -HALF_W), (-16, HALF_W), (-148, HALF_W)
NORTH_COAST = [(-138, -70), (-128, -66), (-118, -67), (-108, -71), (-98, -70), (-90, -64), (-84, -60),
               (-76, -61), (-68, -66), (-58, -70), (-48, -69), (-40, -65), (-32, -66), (-24, -70)]
SOUTH_COAST = [(-26, 72), (-38, 70), (-50, 72), (-64, 71), (-78, 72), (-92, 71), (-104, 72), (-116, 72),
               (-126, 68), (-134, 64), (-140, 68)]
BACK_EDGE = [(-146, 58), (-143, 44), (-147, 28), (-148, 14), (-148, -14), (-145, -30), (-142, -46),
             (-146, -60)]


def outline_ops():
    shape = Ring([V0, V1, V2, V3])
    shape.run(V3, BACK_EDGE)
    shape.run(V2, SOUTH_COAST)
    shape.run(V0, NORTH_COAST)
    # The cistern's notch in the strait edge: a court, a culvert, a hall and a cutting, as one inlet. It is
    # drawn from both mouths inward so the chord closing it never crosses a wall already drawn, and the
    # hall's west side goes in at a temporary point that is moved home once the ring has closed round it.
    qx0, qz0, qx1, qz1 = COURT
    cx0, cz0, _, _ = COURT_STAIR
    gx0, gz0, gx1, gz1 = CULVERT
    hx0, hz0, hx1, hz1 = HALL
    ux0, uz0, ux1, uz1 = CUTTING
    p = {0: (qx1, cz0), 1: (cx0, cz0), 2: (cx0, qz0 + 4), 3: (qx0, qz0 + 4), 4: (qx0, gz0), 5: (gx0, gz0),
         6: (hx1, hz0), 7: (ux1, hz0), 8: (ux1, uz0), 9: (ux0, uz0), 10: (ux0, hz0), 11: (hx0, hz0),
         12: (hx0, hz1), 13: (hx1, hz1), 14: (hx1, gz1), 15: (qx0, gz1), 16: (qx0, qz1), 17: (qx1, qz1)}
    temp = (hx0, (gz0 + gz1) // 2 - 0.5)
    shape.insert_after(V1, p[0])
    shape.insert_after(p[0], p[17])
    shape.insert_after(p[0], p[1])
    shape.insert_after(p[1], p[2])
    shape.insert_after(p[2], p[16])
    shape.insert_after(p[2], p[3])
    shape.insert_after(p[3], p[4])
    shape.insert_after(p[4], p[15])
    shape.insert_after(p[4], p[5])
    shape.insert_after(p[5], p[14])
    shape.insert_after(p[5], temp)
    shape.insert_after(p[5], p[6])
    shape.insert_after(temp, p[13])
    shape.insert_after(temp, p[12])
    shape.move(temp, p[11])
    shape.insert_after(p[6], p[7])
    shape.insert_after(p[7], p[10])
    shape.insert_after(p[7], p[8])
    shape.insert_after(p[8], p[9])
    # the two back corners cut last
    shape.move(V0, (-145, -71))
    shape.move(V3, (-146, 71))
    return shape.ops


# ── the cistern: floors on a storey under the ground, roofs in the ground's own group ───────────
def rect_shape(sid, box, base_height, **extra):
    x0, z0, x1, z1 = box
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0, "max_x": x1,
            "max_z": z1, "floor": 0, "base_height": base_height, **extra}


def cistern_layer():
    cx0, cz0, cx1, cz1 = COURT_STAIR
    ux0, uz0, ux1, uz1 = CUTTING
    hx0, hz0, hx1, hz1 = HALL
    pillar = {"material": STONE_BRICK}
    shapes = [
        rect_shape("court-floor", COURT, FLOOR_H),
        {"id": "court-stair", "type": "polygon", "operation": "add", "floor": 0, "base_height": RIM_H,
         "vertices": [[cx0, cz0], [cx1, cz0], [cx1, cz1], [cx0, cz1]],
         "anchor_heights": [RIM_H, FLOOR_H, FLOOR_H, RIM_H]},
        rect_shape("culvert-floor", CULVERT, FLOOR_H),
        rect_shape("hall-floor", HALL, FLOOR_H),
        rect_shape("pillar-nw", (hx0 + 2, hz0 + 1, hx0 + 4, hz0 + 3), ROOF_FLOOR, **pillar),
        rect_shape("pillar-ne", (hx1 - 4, hz0 + 1, hx1 - 2, hz0 + 3), ROOF_FLOOR, **pillar),
        rect_shape("pillar-sw", (hx0 + 2, hz1 - 3, hx0 + 4, hz1 - 1), ROOF_FLOOR, **pillar),
        rect_shape("pillar-se", (hx1 - 4, hz1 - 3, hx1 - 2, hz1 - 1), ROOF_FLOOR, **pillar),
        {"id": "stair-cutting", "type": "polygon", "operation": "add", "floor": 0, "base_height": GREEN_H,
         "vertices": [[ux0, uz0], [ux1, uz0], [ux1, uz1], [ux0, uz1]],
         "anchor_heights": [GREEN_H, GREEN_H, FLOOR_H, FLOOR_H]},
    ]
    for shape in shapes:
        if not shape["id"].startswith("pillar"):
            shape["theme"] = "paving"
    return {"id": "cistern", "name": "Cistern", "base_y": 0, "below": True, "shapes": shapes,
            "groups": [{"id": "cistern", "name": "Cistern", "mirrors": True,
                        "shapeIds": [s["id"] for s in shapes]}]}


def roofs():
    return [rect_shape("roof-culvert", CULVERT, 20, floor=ROOF_FLOOR, group="team"),
            rect_shape("roof-hall", HALL, 20, floor=ROOF_FLOOR, group="team")]


# ── the relief: a frame of marks where players stand, then the landforms ───────────────────────
def relief():
    ux0, uz0, ux1, _ = CUTTING
    marks = [
        {"id": "spawn-bench", "kind": "area", "h": 32, "bevel": 3, "ring": rect_ring(-152, -16, -126, 16)},
        # the bench's floor: the push `crag-bench` lifts this 5 to 27 and gives it a bank
        {"id": "crag-shelf", "kind": "area", "h": 22, "bevel": 2, "ring": ring(*CRAG_STONE, 10, lobes=0.12)},
        {"id": "green", "kind": "area", "h": GREEN_H, "bevel": 3,
         "ring": ring(*GREEN_STONE, 9, lobes=0.1, phase=1)},
        {"id": "ramp-head", "kind": "area", "h": GREEN_H, "ring": rect_ring(ux0 - 3, uz0 - 6, ux1 + 3, uz0)},
        {"id": "hamlet-terrace", "kind": "line", "r": 6, "h": [23, 22], "points": [[-114, 60], [-82, 60]]},
        # the ground over the culvert and the hall, deep enough that their ceiling course is rock, not soil
        {"id": "culvert-cover", "kind": "line", "r": 5, "h": [23, 22, 20],
         "points": [[-80, 58], [-56, 57], [-34, 57]]},
        {"id": "court-rim", "kind": "line", "r": 3, "tread": 1, "h": RIM_H, "points": [[-38, 44], [-38, 53]]},
        {"id": "farm-yard", "kind": "area", "h": 29, "bevel": 2, "ring": ring(-110, -38, 8, lobes=0.1)},
        {"id": "barn-stead", "kind": "area", "h": 29, "bevel": 2, "ring": rect_ring(-117, -56, -100, -45)},
        # the pond's pan, the size of the water that fills it, so the ground rises straight out of the pool
        {"id": "pond-pan", "kind": "area", "h": 15, "ring": POND_RING},
        {"id": "lip", "kind": "line", "r": 2, "h": [16, 15, 17, 16, 15, 16, 17, 16],
         "points": [[-22, -70], [-20, -52], [-24, -30], [-19, -8], [-23, 14], [-20, 34], [-22, 46],
                    [-21, 70]]},
    ]
    pushes = [
        {"id": "fell-north", "ring": ring(-158, -66, 18, lobes=0.15, sx=1.2, sz=0.8), "amount": 11,
         "falloff": 14, "crown": 8, "roughness": 0.5, "seed": 3},
        {"id": "crag-bench", "ring": ring(-84, -38, 11, lobes=0.14, phase=0.7, sx=1.1), "amount": 5,
         "falloff": 5, "crown": 0, "roughness": 0.5, "seed": 8},
        {"id": "hogs-back", "ring": ring(-90, 2, 24, n=18, lobes=0.05, sz=0.3), "amount": 4, "falloff": 12,
         "crown": 4, "roughness": 0, "seed": 9},
        {"id": "fell-south", "ring": ring(-158, 64, 18, lobes=0.15, phase=2), "amount": 11, "falloff": 14,
         "crown": 8, "roughness": 0.5, "seed": 4},
        # the crag stands clear over the Crag Stone, so bridging off its shoulder arrives from above
        {"id": "crag", "ring": ring(-62, -53, 8, lobes=0.2, sx=1.3), "amount": 12, "falloff": 12, "crown": 6,
         "roughness": 0.5, "seed": 5},
        {"id": "wood-rise", "ring": ring(-116, -65, 16, lobes=0.1, sx=1.6, sz=0.35), "amount": 5,
         "falloff": 8, "crown": 3, "roughness": 0, "seed": 6},
    ]
    return {"team": {"base": 20, "reach": 0, "step": 1, "marks": marks, "pushes": pushes}}


# ── the paint: one heath finished by its angle over banded red rock, a paved floor, worn yards ────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
HARD_CLAY, ORANGE_CLAY, RED_SANDSTONE = solid(172), solid(159, 1), solid(179)
BROWN_CLAY, YELLOW_CLAY, WHITE_CLAY = solid(159, 12), solid(159, 4), solid(159, 0)
STONE, GRANITE, POL_GRANITE, ANDESITE, POL_ANDESITE = solid(1), solid(1, 1), solid(1, 2), solid(1, 5), solid(1, 6)
STONE_BRICK, CLAY, RED_SAND = solid(98), solid(82), solid(12, 1)
DIORITE, POL_DIORITE = solid(1, 3), solid(1, 4)                   # the erratics: one rock the ground is not


def depth(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat", "bands": [{"thickness": t, "material": m} for m, t in bands]}}


def cell(seed, size, *palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 1, "warp": 2, "palette": list(palette),
            "rise": rise}


SOIL = cell(31, 3, DIRT, COARSE)                                   # dirt and coarse dirt, half and half
RED_ROCK = cell(32, 3, HARD_CLAY, ORANGE_CLAY, HARD_CLAY, RED_SANDSTONE)   # terracotta, one tone
TURF = depth((GRASS, 1), (SOIL, 2))
ROCKY_TURF = depth(({"kind": "noise", "seed": 33, "scale": 2, "octaves": 1,
                     "stops": [RED_ROCK, GRASS, GRASS, RED_ROCK]}, 1), (SOIL, 2))


def strata():
    """The red rock's beds, read on every cut: hardened clay carrying thin bands of stained clay. The beds follow
    the ground averaged sixteen cells either side, so they rise with the land toward the back of each half and a
    hill cuts through them. They start 48 courses under that ground, which reaches the bedrock under the highest
    of it (y50) and puts an orange bed in the culvert's walls, and are stated four times over so the stack still
    runs past the tallest face, because a height stack holds its last band rather than cycling."""
    beds = [(HARD_CLAY, 3), (ORANGE_CLAY, 2), (HARD_CLAY, 2), (BROWN_CLAY, 1), (HARD_CLAY, 3),
            (YELLOW_CLAY, 1), (ORANGE_CLAY, 2), (HARD_CLAY, 2), (WHITE_CLAY, 1), (HARD_CLAY, 2)]
    bands = [{"thickness": t, "material": m} for _ in range(4) for m, t in beds]
    return {"kind": "layered", "axis": "height", "from": -48, "follow": 100, "reach": 16, "beyond": HARD_CLAY,
            "stack": {"ending": "repeat", "bands": bands}}


def themes():
    heath = {
        "bedrock": {"relative": False, "value": 1},
        "fill": strata(),
        "wall": strata(), "wallEnabled": True, "wallOnTerrainFaces": True,
        "surface": {"enabled": True, "depth": 3, "material": {
            "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
                {"thickness": 38, "material": TURF},
                {"thickness": 14, "material": ROCKY_TURF},
                {"thickness": 40, "material": strata()}]}}},
        "rim": {"enabled": False, "depth": 1, "material": HARD_CLAY},
        "rimEdges": "void",
    }
    paving = {
        "bedrock": {"relative": False, "value": 1},
        "fill": strata(), "wall": strata(), "wallEnabled": True, "wallOnTerrainFaces": True,
        "edgesFromGround": True,
        "surface": {"enabled": True, "depth": 2, "material": depth(
            (cell(36, 3, STONE_BRICK, POL_ANDESITE, ANDESITE, STONE), 1), (STONE, 1))},
        "rim": {"enabled": False, "depth": 1, "material": HARD_CLAY}, "rimEdges": "void",
    }
    worn = {
        "bedrock": {"relative": False, "value": 1},
        "fill": strata(), "wall": strata(), "wallEnabled": True, "wallOnTerrainFaces": True,
        "edgesFromGround": True,
        "surface": {"enabled": True, "depth": 3, "material": depth((cell(38, 2, DIRT, COARSE), 1), (DIRT, 2))},
        "rim": {"enabled": False, "depth": 1, "material": HARD_CLAY}, "rimEdges": "void",
    }
    return {"heath": heath, "paving": paving, "worn": worn}


def patches():
    """Ground of a different kind, each a shape carrying its own theme in the ground's own group."""
    def patch(sid, points, theme):
        return {"id": sid, "type": "polygon", "operation": "add", "floor": 0, "base_height": 20,
                "vertices": points, "theme": theme, "group": "team"}
    return [
        patch("farmyard", ring(-109, -38, 5.5, n=12, lobes=0.18, phase=0.4), "worn"),
        patch("hamlet-square", ring(-98, 64, 4.5, n=10, lobes=0.15), "worn"),
        patch("court-apron", ring(-40, 50, 3.5, n=10, lobes=0.1), "paving"),
        patch("mill-yard", ring(-60, -53, 6.5, n=12, lobes=0.12), "worn"),
    ]


# ── buildings: grey masonry under a spruce-boarded storey and an acacia roof ─────────────────────
PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True}
SPRUCE_LOG = solid(17, 1)
LAID = {"kind": "laidLog", "id": 17, "data": 1}
SPRUCE_PLANK, ACACIA_PLANK = solid(5, 1), solid(5, 4)
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2,
             "height": 2, "spacing": 3}


def wall(*bands):
    return {"stack": {"bands": [{"material": m, "thickness": t} for m, t in bands], "ending": "repeat"},
            "extent": sum(t for _, t in bands)}


def pane():
    """Glass panes, cut wherever one fits: a pane has no stair or slab twin to share a host's material."""
    return {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2,
            "width": 2, "height": 2, "spacing": 3}


def heath_house(upper=None):
    """Stone-brick ground storey, a laid spruce beam course, a spruce-boarded upper storey, an acacia roof."""
    upper = upper or wall((LAID, 1), (SPRUCE_PLANK, 3))
    return {
        "foundation": {"plate": {"stack": {"bands": [{"material": SPRUCE_PLANK, "thickness": 1}],
                                           "ending": "repeat"}, "extent": 1}, "surface": PLAIN, "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": True,
                 "hole": False, "body": ACACIA_PLANK, "verge": SPRUCE_PLANK, "gable": SPRUCE_PLANK,
                 "gableWindows": {"form": "open", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                                  "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": wall((STONE_BRICK, 4)),
        "post": SPRUCE_LOG,
        "windows": pane(),
        "storeys": [
            {"clear": 4, "wall": wall((STONE_BRICK, 4)), "post": SPRUCE_LOG, "windows": pane(),
             "surface": PLAIN, "deck": None, "headroom": 4},
            {"clear": 4, "wall": upper, "post": SPRUCE_LOG, "windows": pane(), "surface": PLAIN, "deck": None,
             "headroom": 4}],
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "arched", "block": 134, "fill": "upperSlab", "fillBlock": 126,
                                           "fillData": 1}, "width": 2, "height": 3},
    }


def barn_house():
    """The barn and the well-house: spruce weatherboard over a stone-brick plinth, one tall storey."""
    board = wall((STONE_BRICK, 2), (LAID, 1), (SPRUCE_PLANK, 3))
    style = heath_house()
    style["roof"].update({"gableWindows": dict(NO_WINDOW)})
    style["wall"] = board
    style["windows"] = dict(NO_WINDOW)
    style["storeys"] = [{"clear": 6, "wall": board, "post": SPRUCE_LOG,
                         "windows": {"form": "slabBanded", "block": 126, "hostBlock": 5, "hostData": 1, "data": 1,
                                     "sill": 4, "width": 2, "height": 1, "spacing": 2},
                         "surface": PLAIN, "deck": None, "headroom": 6}]
    style["doorway"] = {"door": "air", "head": {"form": "none", "block": 134, "fill": "solid", "fillBlock": 5,
                                                "fillData": 1}, "width": 3, "height": 4}
    return style


def spawn_hall():
    """The heath house at hall size, with a course of the owner's colour over the beams."""
    tint = {"kind": "teamTint", "blockId": 159, "neutral": SPRUCE_PLANK}
    return heath_house(upper=wall((LAID, 1), (tint, 1), (SPRUCE_PLANK, 2)))


def house(hid, style, corners, front, seed, **spec):
    wing = {"corners": corners}
    if spec:
        wing["spec"] = spec
    return {"id": hid, "kind": "house", "seed": seed, "wings": [wing], "front": front, "style": style}


def buildings():
    farmhouse = {"id": "farmhouse", "kind": "house", "seed": 41, "front": "posX", "style": "heath",
                 "wings": [{"corners": [[-127, -46], [-118, -38]]},
                           {"corners": [[-127, -37], [-122, -32]], "spec": {"storeysHigh": 1, "ridge": "alongZ"}}]}
    return [
        farmhouse,
        house("barn", "barn", [[-114, -53], [-103, -47]], "posZ", 42),
        house("cottage-west", "heath", [[-120, 52], [-112, 60]], "posZ", 43, storeysHigh=1),
        house("cottage-hall", "heath", [[-104, 50], [-94, 60]], "posZ", 44),
        house("cottage-east", "heath", [[-89, 54], [-82, 61]], "posZ", 45, storeysHigh=1),
        house("well-house", "barn", [[-51, 55], [-45, 61]], "negZ", 46),
    ]


# ── made things: the mill stump on the crag ─────────────────────────────────────────────────────
def c_ring(cx, cz, outer, inner, gap_deg=40, facing_deg=35, n=28):
    """An annulus as one polygon with a doorway cut through it: the outer arc, across the gap, the inner arc
    back, and across again."""
    half = math.radians(gap_deg / 2)
    start = math.radians(facing_deg) + half
    span = 2 * math.pi - 2 * half
    arc = lambda r, a: [round(cx + r * math.cos(a), 1), round(cz + r * math.sin(a), 1)]
    outer_pts = [arc(outer, start + span * i / n) for i in range(n + 1)]
    inner_pts = [arc(inner, start + span * i / n) for i in range(n, -1, -1)]
    return outer_pts + inner_pts


def made_layers():
    mill = {"id": "mill", "name": "Mill stump", "base_y": 30, "kind": "made", "part_of": "mill", "seat": "ground",
            "shapes": [{"id": "mill-wall", "type": "polygon", "operation": "add", "floor": 0, "base_height": 8,
                        "vertices": c_ring(-60, -53, 4.5, 3.4), "material": STONE_BRICK}],
            "groups": [{"id": "mill", "name": "mill", "mirrors": True, "shapeIds": ["mill-wall"]}]}
    return [mill]


# ── the dressing: the routes first, then the water, then the buildings, rock and trees ──────────
TRACK = cell(51, 2, GRANITE, POL_GRANITE, HARD_CLAY)              # a warm path: granite with hardened clay


def stroke(sid, points, radius, pave, seed):
    return {"id": sid, "kind": "stroke", "seed": seed, "points": [list(p) for p in points], "radius": radius,
            "style": "solid", "claimsGround": True, "pave": pave}


def paths():
    return [
        stroke("spawn-apron", [(-130, 0), (-118, 1)], 3, TRACK, 61),
        stroke("hogs-back-track", [(-118, 1), (-106, 2), (-90, 3), (-74, 3), (-62, 2), (-56, -8), (-44, -16),
                                   (-22, -14)], 2, TRACK, 62),
        stroke("crag-track", [(-106, 2), (-100, -10), (-94, -20), (-89, -26)], 2, TRACK, 63),
        stroke("green-track", [(-106, 2), (-100, 14), (-94, 24), (-90, 28)], 2, TRACK, 64),
        stroke("crag-front", [(-73, -32), (-60, -31), (-46, -27), (-32, -25), (-21, -25)], 2, TRACK, 65),
        stroke("green-front", [(-73, 30), (-58, 26), (-42, 22), (-28, 20), (-21, 20)], 2, TRACK, 66),
        stroke("farm-track", [(-136, -10), (-126, -18), (-116, -27), (-111, -35)], 1.5, TRACK, 67),
        stroke("farm-to-crag", [(-104, -40), (-98, -40), (-93, -39)], 1.5, TRACK, 68),
        stroke("green-to-hamlet", [(-92, 40), (-100, 46), (-108, 52), (-108, 62)], 1.5, TRACK, 69),
        stroke("hamlet-lane", [(-120, 63), (-106, 64), (-92, 65), (-78, 66)], 2, TRACK, 70),
        stroke("court-road", [(-78, 66), (-64, 66), (-54, 65), (-42, 63), (-37, 56), (-36, 51)], 2, TRACK, 71),
    ]


def trees():
    acacias = [(-134, -63, "acacia-a"), (-117, -62, "acacia-b"), (-100, -66, "acacia-c")]
    olives = [(-92, -58, "olive-a"), (-136, -44, "olive-b"), (-78, -55, "olive-c"),
              (-48, -63, "olive-d"), (-38, -55, "olive-e"), (-141, -35, "olive-a")]
    grove = [(-140, 20, "olive-small-a"), (-130, 20, "olive-small-b"), (-120, 26, "olive-small-c"),
             (-140, 31, "olive-small-b"), (-130, 31, "olive-small-c")]
    hamlet = [(-135, 58, "acacia-great"), (-110, 43, "olive-b"), (-120, 44, "olive-small-b"), (-137, 38, "olive-e"),
              (-115, 31, "olive-small-a"), (-106, 18, "olive-c")]
    placed = []
    for index, (x, z, style) in enumerate(acacias + olives + grove + hamlet):
        placed.append({"id": f"tree-{index + 1}", "kind": "tree", "seed": 100 + index, "x": x, "z": z,
                       "style": style})
    return placed


def boulders():
    spots = [(-48, -38), (-66, -47), (-40, -62), (-36, 36)]
    return [{"id": f"erratic-{i + 1}", "kind": "boulder", "seed": 200 + i, "x": x, "z": z, "style": "erratic"}
            for i, (x, z) in enumerate(spots)]


def dressing():
    # the copied trees are the showcase's own: each key names the showcase tree it is, and its recipe
    # comes whole from the showcase snapshot
    with open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")) as handle:
        showcase = json.load(handle)["trees"]
    styles = {key: showcase[tree]["style"] for key, tree in {
        "acacia-a": "acacia-1", "acacia-b": "acacia-2", "acacia-c": "acacia-3", "acacia-d": "acacia-4",
        "acacia-e": "acacia-5", "acacia-f": "acacia-6", "acacia-great": "acacia-7",
        "olive-a": "olive-1", "olive-b": "olive-2", "olive-c": "olive-3", "olive-d": "olive-4", "olive-e": "olive-5",
        "olive-small-a": "small-olive-1", "olive-small-b": "small-olive-2", "olive-small-c": "small-olive-3"}.items()}
    styles["heath"] = {"kind": "house", "shell": heath_house()}
    styles["barn"] = {"kind": "house", "shell": barn_house()}
    styles["erratic"] = {"kind": "boulder", "form": "round", "size": 2.5, "mossy": False,
                         "rock": cell(81, 3, DIORITE, DIORITE, POL_DIORITE)}
    pond = {"id": "pond", "kind": "fluid", "layer": "ground", "shape": "pool", "form": "natural", "seed": 90,
            "points": POND_RING, "radius": 3, "depth": 3,
            "shore": 2, "shoreWander": True, "edge": 1.5, "bank": cell(91, 2, COARSE, RED_SAND, HARD_CLAY)}
    px0, pz0, px1, pz1 = CISTERN_POOL
    cistern = {"id": "cistern-pool", "kind": "fluid", "layer": "cistern", "shape": "pool", "form": "canal",
               "seed": 92, "points": rect_ring(px0, pz0, px1, pz1), "radius": 1, "depth": 2, "shore": 0,
               "bank": STONE_BRICK}
    cover = {"id": "ground-cover", "kind": "flora", "seed": 95,
             "points": [[-150, -74], [-14, -74], [-14, 74], [-150, 74]],
             "spec": {"coverage": 0.18, "scale": 9, "octaves": 2, "fernShare": 0.1, "flowerShare": 0.03,
                      "flowerScale": 7, "tallShare": 0.04}}
    props = paths() + [pond, cistern] + buildings() + boulders() + trees() + [cover]
    return {"styles": styles, "props": props}


def finish():
    return {
        "authors": ["Opus 5.5"],
        "created": "2026-09-27",
        "editShapes": {"weald-20": outline_ops()},
        "addLayers": [cistern_layer()] + made_layers(),
        "addShapes": roofs() + patches(),
        "relief": relief(),
        "themes": themes(),
        "mapTheme": "heath",
        "biome": {"kind": "solid", "id": 35},
        "roomStyles": {"spawn": spawn_hall()},
        "dressing": dressing(),
    }


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan(), handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w") as handle:
        json.dump(finish(), handle, indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.refinement.json")


if __name__ == "__main__":
    main()
