#!/usr/bin/env python3
"""Whitstone Weald — writes whitstone-weald.plan.json and whitstone-weald.finish.json beside itself.

A wooded mining weald for 32 a side. Each team holds two end-stone monuments: the Crag Stone on a shelf
under a crag with a wood on its outer flank, and the Green Stone on a green below a mining hamlet, with a
drift mine running under the hamlet from a quarry at the strait to a cutting that surfaces beside the green.

Every coordinate below is team red's (x < 0); the plan is rot_180 and the studio fans the rest. Every height
is a column height, as `base_height` states one: the top block is one lower.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = os.path.basename(HERE)

# ── the board's numbers, in blocks ──────────────────────────────────────────────────────────────
HALF_W = 72                           # z runs -72..72
CRAG_STONE = (-82, -36)               # the north monument
GREEN_STONE = (-82, 36)               # the south monument

# ── the mine ────────────────────────────────────────────────────────────────────────────────────
MINE_FLOOR = 12                       # every mine floor: top block y11, a player stands at y12
ROOF_FLOOR = 16                       # the ground over the gallery and chamber starts here: 4 of air
RIM_H = 18                            # the quarry's rim, where the cart ramp starts down
GREEN_H = 20                          # the green round the Green Stone, where the cutting surfaces
QUARRY = (-30, 48, -16, 66)           # the open pit at the strait: min_x, min_z, max_x, max_z
CART_RAMP = (-34, 48, -22, 52)        # 6 down over 12, from the rim to the pit floor
GALLERY = (-60, 55, -30, 60)          # roofed, 30 long and 5 wide
CHAMBER = (-76, 52, -60, 64)          # roofed, 16 x 12, two pillars
UP_RAMP = (-70, 34, -65, 52)          # an open cutting climbing 8 over 18 to the green
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
        "meta": {"name": "Whitstone Weald", "authors": ["Claude"],
                 "notes": "A wooded mining weald, two end-stone monuments a team, a drift mine under the south."},
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
    # The mine's notch in the strait edge: a quarry, a gallery, a chamber and a cutting, as one inlet. It is
    # drawn from both mouths inward so the chord closing it never crosses a wall already drawn, and the
    # chamber's west side goes in at a temporary point that is moved home once the ring has closed round it.
    qx0, qz0, qx1, qz1 = QUARRY
    cx0, cz0, _, _ = CART_RAMP
    gx0, gz0, gx1, gz1 = GALLERY
    hx0, hz0, hx1, hz1 = CHAMBER
    ux0, uz0, ux1, uz1 = UP_RAMP
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


# ── the mine: floors on a storey under the ground, roofs in the ground's own group ──────────────
def rect_shape(sid, box, base_height, **extra):
    x0, z0, x1, z1 = box
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0, "max_x": x1,
            "max_z": z1, "floor": 0, "base_height": base_height, **extra}


def mine_layer():
    cx0, cz0, cx1, cz1 = CART_RAMP
    ux0, uz0, ux1, uz1 = UP_RAMP
    hx0, hz0, hx1, hz1 = CHAMBER
    mid = (hz0 + hz1) // 2
    shapes = [
        rect_shape("quarry-floor", QUARRY, MINE_FLOOR),
        {"id": "cart-ramp", "type": "polygon", "operation": "add", "floor": 0, "base_height": RIM_H,
         "vertices": [[cx0, cz0], [cx1, cz0], [cx1, cz1], [cx0, cz1]],
         "anchor_heights": [RIM_H, MINE_FLOOR, MINE_FLOOR, RIM_H]},
        rect_shape("gallery-floor", GALLERY, MINE_FLOOR),
        rect_shape("chamber-floor", CHAMBER, MINE_FLOOR),
        rect_shape("pillar-w", (hx0 + 4, mid - 1, hx0 + 6, mid + 1), ROOF_FLOOR),
        rect_shape("pillar-e", (hx1 - 6, mid - 1, hx1 - 4, mid + 1), ROOF_FLOOR),
        {"id": "up-ramp", "type": "polygon", "operation": "add", "floor": 0, "base_height": GREEN_H,
         "vertices": [[ux0, uz0], [ux1, uz0], [ux1, uz1], [ux0, uz1]],
         "anchor_heights": [GREEN_H, GREEN_H, MINE_FLOOR, MINE_FLOOR]},
    ]
    for shape in shapes:
        if not shape["id"].startswith("pillar"):
            shape["theme"] = "works"
    return {"id": "mine", "name": "Mine", "base_y": 0, "below": True, "shapes": shapes,
            "groups": [{"id": "mine", "name": "Mine", "mirrors": True, "shapeIds": [s["id"] for s in shapes]}]}


def roofs():
    return [rect_shape("roof-gallery", GALLERY, 20, floor=ROOF_FLOOR, group="team"),
            rect_shape("roof-chamber", CHAMBER, 20, floor=ROOF_FLOOR, group="team")]


# ── the relief: a frame of marks where players stand, then the landforms ───────────────────────
def relief():
    ux0, uz0, ux1, _ = UP_RAMP
    marks = [
        {"id": "spawn-bench", "kind": "area", "h": 32, "bevel": 3, "ring": rect_ring(-152, -16, -126, 16)},
        # the bench's floor: the push `crag-bench` lifts this 5 to 27 and gives it a bank
        {"id": "crag-shelf", "kind": "area", "h": 22, "bevel": 2, "ring": ring(*CRAG_STONE, 10, lobes=0.12)},
        {"id": "green", "kind": "area", "h": GREEN_H, "bevel": 3,
         "ring": ring(*GREEN_STONE, 9, lobes=0.1, phase=1)},
        {"id": "ramp-head", "kind": "area", "h": GREEN_H, "ring": rect_ring(ux0 - 3, uz0 - 6, ux1 + 3, uz0)},
        {"id": "hamlet-terrace", "kind": "line", "r": 6, "h": [23, 22], "points": [[-114, 60], [-82, 60]]},
        # the ground over the gallery and chamber, deep enough that their ceiling course is rock, not soil
        {"id": "mine-cover", "kind": "line", "r": 5, "h": [23, 22, 20],
         "points": [[-80, 58], [-56, 57], [-34, 57]]},
        {"id": "quarry-rim", "kind": "line", "r": 3, "tread": 1, "h": RIM_H, "points": [[-38, 44], [-38, 53]]},
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


# ── the paint: one ground finished by its angle, the works floor, and worn patches ───────────────
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


GRASS, DIRT, COARSE, HARD_CLAY = solid(2), solid(3), solid(3, 1), solid(172)
STONE, GRANITE, POL_GRANITE, ANDESITE = solid(1), solid(1, 1), solid(1, 2), solid(1, 5)
COBBLE, GRAVEL, BRICK, CLAY = solid(4), solid(13), solid(45), solid(82)
DIORITE, POL_DIORITE = solid(1, 3), solid(1, 4)                   # the erratics: one rock the ground is not


def depth(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat", "bands": [{"thickness": t, "material": m} for m, t in bands]}}


def cell(seed, size, *palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 1, "warp": 2, "palette": list(palette),
            "rise": rise}


SOIL = cell(31, 3, DIRT, COARSE)                                   # dirt and coarse dirt, half and half
ROCK = cell(32, 3, STONE, ANDESITE, STONE, COBBLE)                 # stone and andesite, cobble a quarter
TURF = depth((GRASS, 1), (SOIL, 2))
ROCKY_TURF = depth(({"kind": "noise", "seed": 33, "scale": 2, "octaves": 1,
                     "stops": [ROCK, GRASS, GRASS, ROCK]}, 1), (SOIL, 2))


def themes():
    weald = {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": cell(34, 3, STONE, ANDESITE, STONE, COBBLE, rise=3), "wallEnabled": True,
        "wallOnTerrainFaces": True,
        "surface": {"enabled": True, "depth": 3, "material": {
            "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
                {"thickness": 38, "material": TURF},
                {"thickness": 14, "material": ROCKY_TURF},
                {"thickness": 40, "material": depth((ROCK, 3))}]}}},
        "rim": {"enabled": False, "depth": 1, "material": STONE},
        "rimEdges": "void",
    }
    works = {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE, "wall": cell(35, 3, STONE, ANDESITE, STONE, COBBLE, rise=3), "wallEnabled": True,
        "wallOnTerrainFaces": True, "edgesFromGround": True,
        "surface": {"enabled": True, "depth": 2, "material": depth((cell(36, 2, GRAVEL, ANDESITE, COBBLE), 1),
                                                                   (STONE, 1))},
        "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "void",
    }
    worn = {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE, "wall": cell(37, 3, STONE, ANDESITE, STONE, COBBLE, rise=3), "wallEnabled": True,
        "wallOnTerrainFaces": True, "edgesFromGround": True,
        "surface": {"enabled": True, "depth": 3, "material": depth((cell(38, 2, DIRT, COARSE), 1), (DIRT, 2))},
        "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "void",
    }
    return {"weald": weald, "works": works, "worn": worn}


def patches():
    """Ground of a different kind, each a shape carrying its own theme in the ground's own group."""
    def patch(sid, points, theme):
        return {"id": sid, "type": "polygon", "operation": "add", "floor": 0, "base_height": 20,
                "vertices": points, "theme": theme, "group": "team"}
    return [
        patch("farmyard", ring(-109, -38, 5.5, n=12, lobes=0.18, phase=0.4), "worn"),
        patch("hamlet-square", ring(-98, 64, 4.5, n=10, lobes=0.15), "worn"),
        patch("spoil", ring(-42, 44, 5, n=10, lobes=0.25, phase=1.2, sz=0.7), "works"),
        patch("mill-yard", ring(-60, -53, 6.5, n=12, lobes=0.12), "worn"),
    ]


# ── buildings ───────────────────────────────────────────────────────────────────────────────────
PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True}
DARK_LOG = solid(162, 1)
LAID = {"kind": "laidLog", "id": 162, "data": 1}
BIRCH_PLANK, DARK_PLANK, SPRUCE_PLANK = solid(5, 2), solid(5, 5), solid(5, 1)
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2, "width": 2,
             "height": 2, "spacing": 3}


def wall(*bands):
    return {"stack": {"bands": [{"material": m, "thickness": t} for m, t in bands], "ending": "repeat"},
            "extent": sum(t for _, t in bands)}


def pane():
    """Glass panes, cut wherever one fits: a pane has no stair or slab twin to share a host's material."""
    return {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0, "sill": 2,
            "width": 2, "height": 2, "spacing": 3}


def weald_house(upper=None):
    """Brick ground storey, a beam course, a birch-planked upper storey in a dark-oak frame, a dark roof."""
    upper = upper or wall((LAID, 1), (BIRCH_PLANK, 3))
    return {
        "foundation": {"plate": {"stack": {"bands": [{"material": SPRUCE_PLANK, "thickness": 1}],
                                           "ending": "repeat"}, "extent": 1}, "surface": PLAIN, "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1, "ridgeCap": True,
                 "hole": False, "body": DARK_PLANK, "verge": SPRUCE_PLANK, "gable": BIRCH_PLANK,
                 "gableWindows": {"form": "open", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                                  "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": wall((BRICK, 4)),
        "post": DARK_LOG,
        "windows": pane(),
        "storeys": [
            {"clear": 4, "wall": wall((BRICK, 4)), "post": DARK_LOG, "windows": pane(), "surface": PLAIN,
             "deck": None, "headroom": 4},
            {"clear": 4, "wall": upper, "post": DARK_LOG, "windows": pane(), "surface": PLAIN, "deck": None,
             "headroom": 4}],
        "porch": None, "front": None,
        "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "arched", "block": 164, "fill": "upperSlab", "fillBlock": 126,
                                           "fillData": 5}, "width": 2, "height": 3},
    }


def works_house():
    """The barn and the engine house: dark weatherboard over a brick plinth, one tall storey."""
    board = wall((BRICK, 2), (LAID, 1), (DARK_PLANK, 3))
    style = weald_house()
    style["roof"].update({"body": SPRUCE_PLANK, "verge": DARK_PLANK, "gable": DARK_PLANK,
                          "gableWindows": dict(NO_WINDOW)})
    style["wall"] = board
    style["windows"] = dict(NO_WINDOW)
    style["storeys"] = [{"clear": 6, "wall": board, "post": DARK_LOG,
                         "windows": {"form": "slabBanded", "block": 126, "hostBlock": 5, "hostData": 5, "data": 5,
                                     "sill": 4, "width": 2, "height": 1, "spacing": 2},
                         "surface": PLAIN, "deck": None, "headroom": 6}]
    style["doorway"] = {"door": "air", "head": {"form": "none", "block": 164, "fill": "solid", "fillBlock": 5,
                                                "fillData": 5}, "width": 3, "height": 4}
    return style


def spawn_hall():
    """The weald house at hall size, with a course of the owner's colour over the beams."""
    tint = {"kind": "teamTint", "blockId": 159, "neutral": BIRCH_PLANK}
    return weald_house(upper=wall((LAID, 1), (tint, 1), (BIRCH_PLANK, 2)))


def house(hid, style, corners, front, seed, **spec):
    wing = {"corners": corners}
    if spec:
        wing["spec"] = spec
    return {"id": hid, "kind": "house", "seed": seed, "wings": [wing], "front": front, "style": style}


def buildings():
    farmhouse = {"id": "farmhouse", "kind": "house", "seed": 41, "front": "posX", "style": "weald",
                 "wings": [{"corners": [[-127, -46], [-118, -38]]},
                           {"corners": [[-127, -37], [-122, -32]], "spec": {"storeysHigh": 1, "ridge": "alongZ"}}]}
    return [
        farmhouse,
        house("barn", "works", [[-114, -53], [-103, -47]], "posZ", 42),
        house("cottage-west", "weald", [[-120, 52], [-112, 60]], "posZ", 43, storeysHigh=1),
        house("cottage-hall", "weald", [[-104, 50], [-94, 60]], "posZ", 44),
        house("cottage-east", "weald", [[-89, 54], [-82, 61]], "posZ", 45, storeysHigh=1),
        house("engine-house", "works", [[-52, 54], [-42, 61]], "negZ", 46),
    ]


# ── made things: the engine house's chimney and the mill stump on the crag ──────────────────────
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
    chimney = {"id": "chimney", "name": "Engine chimney", "base_y": 20, "kind": "made", "part_of": "chimney",
               "seat": "ground",
               "shapes": [{"id": "chimney-stack", "type": "rectangle", "operation": "add", "min_x": -56,
                           "min_z": 55, "max_x": -53, "max_z": 58, "floor": 0, "base_height": 16,
                           "material": BRICK}],
               "groups": [{"id": "chimney", "name": "chimney", "mirrors": True, "shapeIds": ["chimney-stack"]}]}
    mill = {"id": "mill", "name": "Mill stump", "base_y": 30, "kind": "made", "part_of": "mill", "seat": "ground",
            "shapes": [{"id": "mill-wall", "type": "polygon", "operation": "add", "floor": 0, "base_height": 8,
                        "vertices": c_ring(-60, -53, 4.5, 3.4), "material": BRICK}],
            "groups": [{"id": "mill", "name": "mill", "mirrors": True, "shapeIds": ["mill-wall"]}]}
    return [chimney, mill]


# ── the dressing: the routes first, then the water, then the buildings, rock and trees ──────────
EARTH = cell(51, 2, DIRT, COARSE, HARD_CLAY)
HAUL = cell(52, 2, GRAVEL, ANDESITE, COBBLE)


def stroke(sid, points, radius, pave, seed):
    return {"id": sid, "kind": "stroke", "seed": seed, "points": [list(p) for p in points], "radius": radius,
            "style": "solid", "claimsGround": True, "pave": pave}


def paths():
    return [
        stroke("spawn-apron", [(-130, 0), (-118, 1)], 3, EARTH, 61),
        stroke("hogs-back-track", [(-118, 1), (-106, 2), (-90, 3), (-74, 3), (-62, 2), (-56, -8), (-44, -16),
                                   (-22, -14)], 2, EARTH, 62),
        stroke("crag-track", [(-106, 2), (-100, -10), (-94, -20), (-89, -26)], 2, EARTH, 63),
        stroke("green-track", [(-106, 2), (-100, 14), (-94, 24), (-90, 28)], 2, EARTH, 64),
        stroke("crag-front", [(-73, -32), (-60, -31), (-46, -27), (-32, -25), (-21, -25)], 2, EARTH, 65),
        stroke("green-front", [(-73, 30), (-58, 26), (-42, 22), (-28, 20), (-21, 20)], 2, EARTH, 66),
        stroke("farm-track", [(-136, -10), (-126, -18), (-116, -27), (-111, -35)], 1.5, EARTH, 67),
        stroke("farm-to-crag", [(-104, -40), (-98, -40), (-93, -39)], 1.5, EARTH, 68),
        stroke("green-to-hamlet", [(-92, 40), (-100, 46), (-108, 52), (-108, 62)], 1.5, EARTH, 69),
        stroke("hamlet-lane", [(-120, 63), (-106, 64), (-92, 65), (-78, 66)], 2, EARTH, 70),
        stroke("haul-road", [(-78, 66), (-64, 66), (-50, 65), (-40, 63), (-37, 56), (-36, 51)], 2, HAUL, 71),
    ]


def trees():
    oaks = [(-134, -63, "oak-a"), (-117, -62, "oak-b"), (-100, -66, "oak-c")]
    birches = [(-92, -58, "birch-b"), (-136, -44, "birch-c"), (-78, -55, "birch-d"),
               (-48, -63, "birch-e"), (-38, -55, "birch-f"), (-141, -35, "birch-a")]
    orchard = [(-140, 20, "young-oak-a"), (-130, 20, "young-oak-b"), (-120, 26, "young-oak-c"),
               (-140, 31, "young-oak-b"), (-130, 31, "young-oak-c")]
    hamlet = [(-135, 58, "oak-great"), (-110, 43, "birch-c"), (-120, 44, "young-oak-b"), (-137, 38, "birch-e"),
              (-112, 34, "young-oak-a"), (-106, 18, "birch-f")]
    placed = []
    for index, (x, z, style) in enumerate(oaks + birches + orchard + hamlet):
        placed.append({"id": f"tree-{index + 1}", "kind": "tree", "seed": 100 + index, "x": x, "z": z,
                       "style": style})
    return placed


def boulders():
    spots = [(-48, -38), (-66, -47), (-40, -62), (-36, 36)]
    return [{"id": f"erratic-{i + 1}", "kind": "boulder", "seed": 200 + i, "x": x, "z": z, "style": "erratic"}
            for i, (x, z) in enumerate(spots)]


def dressing():
    with open(os.path.join(HERE, "trees.json")) as handle:
        library = json.load(handle)
    styles = {key: entry["style"] for key, entry in library.items()}
    styles["weald"] = {"kind": "house", "shell": weald_house()}
    styles["works"] = {"kind": "house", "shell": works_house()}
    styles["erratic"] = {"kind": "boulder", "form": "round", "size": 2.5, "mossy": True,
                         "rock": cell(81, 3, DIORITE, DIORITE, POL_DIORITE)}
    pond = {"id": "pond", "kind": "water", "layer": "ground", "shape": "pool", "form": "natural", "seed": 90,
            "points": POND_RING, "radius": 3, "depth": 3,
            "shore": 2, "shoreWander": True, "edge": 1.5, "bank": cell(91, 2, GRAVEL, CLAY, ANDESITE)}
    cover = {"id": "ground-cover", "kind": "flora", "seed": 95,
             "points": [[-150, -74], [-14, -74], [-14, 74], [-150, 74]],
             "spec": {"coverage": 0.2, "scale": 9, "octaves": 2, "fernShare": 0.35, "flowerShare": 0.08,
                      "flowerScale": 7, "tallShare": 0.03}}
    props = paths() + [pond] + buildings() + boulders() + trees() + [cover]
    return {"styles": styles, "props": props}


def finish():
    return {
        "authors": ["Claude"],
        "created": "2026-09-27",
        "editShapes": {"weald-20": outline_ops()},
        "addLayers": [mine_layer()] + made_layers(),
        "addShapes": roofs() + patches(),
        "relief": relief(),
        "themes": themes(),
        "mapTheme": "weald",
        "biome": {"kind": "solid", "id": 4},
        "roomStyles": {"spawn": spawn_hall()},
        "dressing": dressing(),
    }


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan(), handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish(), handle, indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")


if __name__ == "__main__":
    main()
