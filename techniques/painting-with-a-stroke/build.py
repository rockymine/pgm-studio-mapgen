"""Writes painting-with-a-stroke.layout.json — twelve panels of the other instrument that paints.

A stroke is a band of surface along a drawn line. It repaints the top course of every column it crosses and
adds no cell, so it runs over a slope without becoming a ramp, and it can feather one finish into another
where a shape's outline stops dead.

Row 1 is a strand meeting a meadow, four ways. Row 2 is a road along a serpentine cut into a hillside, four
paves. Row 3 is what a pave can read and what turns a brush away.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid, moor

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(4, 3, PANEL_W, PANEL_D)
GROUND_TOP = 40

# Where the ground theme's slope bands cut, read off this board's own `incline`.
GRASS_TO, DIRT_TO = 30, 55
MOOR = moor(GRASS_TO, DIRT_TO)

SAND, GRASS, DIRT = SOLID(12), SOLID(2), SOLID(3)
COARSE, COBBLE, STONE, ANDESITE, PLANKS = SOLID(3, 1), SOLID(4), SOLID(1), SOLID(1, 5), SOLID(5, 1)

STRAND = {   # the beach: sand over sandstone, so it reads as a beach and not as grass with a rim
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SAND},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(24, 2), "fill": SOLID(24),
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((SAND, 2), (SOLID(24), 1))},
}
DECK = {     # the bridge, so a repainted deck can be told from one that kept its own boards
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": PLANKS},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(98), "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": PLANKS},
}
THEMES = {"moor": MOOR, "strand": STRAND, "deck": DECK}

# The paves. A pave is a full terrain material resolved at the cell, not a block list — which is what lets
# a road be a solid, a weathered fabric, or a stack read along one of the painter's own axes.
ROAD = {"kind": "cell", "cellSize": 4, "palette": [COBBLE, STONE, ANDESITE]}
# The broken-up look without a broken-up brush: the road's own blocks and the meadow's grass in one small
# cell pattern, so the band is solid and what varies is the fabric inside it.
WEATHERED = {"kind": "cell", "cellSize": 3, "palette": [COBBLE, GRASS, STONE, GRASS, ANDESITE, COARSE]}
SHORE = {"kind": "cell", "cellSize": 3, "palette": [SAND, GRASS, SAND, GRASS]}


def stroke(prop_id, points, pave, radius=3, style="solid", claims=False, **words):
    out = {"id": prop_id, "kind": "stroke", "layer": "ground", "points": points,
           "radius": radius, "style": style, "claimsGround": claims, "pave": pave, "seed": 4}
    out.update(words)
    return out


def flora(prop_id, ring, coverage=0.55):
    """Ground cover, which is the read on a claim: flora skips a claimed cell exactly and no others."""
    return {"id": prop_id, "kind": "flora", "layer": "ground", "points": ring,
            "spec": {"coverage": coverage, "scale": 9, "octaves": 3,
                     "fernShare": 0.25, "flowerShare": 0.2, "flowerScale": 14}}


def box(cx, cz, width, depth):
    return [[cx - width / 2, cz - depth / 2], [cx + width / 2, cz - depth / 2],
            [cx + width / 2, cz + depth / 2], [cx - width / 2, cz + depth / 2]]


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


def serpentine(x0, z0, limbs=(22, 22), limb=72, inset=12, z_from=10):
    """A switchback: limbs at the stated pitches, which is the route a player walks up the hillside."""
    points, z, near, far = [], z_from, inset, inset + limb
    for index, pitch in enumerate([0, *limbs]):
        z += pitch
        points += [[near, z], [far, z]] if index % 2 == 0 else [[far, z], [near, z]]
    return [[round(x0 + px, 2), round(z0 + pz, 2)] for px, pz in points]


shapes, groups, relief, props = [], [], {}, []
PANELS = ["butted", "feathered", "two-tongues", "tapered-tongue",
          "road", "weathered", "verge", "claimed",
          "by-height", "by-inward", "over-a-deck", "keep-clear"]

for index, name in enumerate(PANELS):
    col, row = index % 4, index // 4
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    members = [f"island-{name}"]
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})

    if row == 0:
        # A shore: the ground shelves from a low fell to a strand, and the sand is a SHAPE whose outline is
        # a ruled line. That line is what the row is about.
        seam = cz - 2
        members.append(f"strand-{name}")
        shapes.append({"id": f"strand-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                       "base_height": GROUND_TOP, "theme": "strand",
                       "min_x": x0, "min_z": seam, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
        # The ground shelves from a low fell to a strand that is already level and already under the water
        # line, so the sea fills what is dug for it: a pool drawn across a slope digs a pit (`DR-BANK`) and
        # a bed dug wider than the pool leaves a dry trench (`DR-DRY`). That argument is `water`'s card.
        relief[name] = {"base": 16, "reach": 0, "step": 1, "pushes": [], "marks": [
            area(f"fell-{name}", 22, box(cx, cz - 28, PANEL_W - 6, 16)),
            area(f"shelf-{name}", 10, box(cx, cz + 28, PANEL_W - 6, 20))]}
        props.append({"id": f"sea-{name}", "kind": "water", "shape": "pool", "layer": "ground",
                      "points": box(cx, cz + 27, PANEL_W + 12, 34), "radius": 10, "depth": 3,
                      "form": "natural", "edge": 1, "shore": 2, "shoreWander": True, "seed": 7,
                      "level": 11, "bank": {"kind": "cell", "cellSize": 5,
                                            "palette": [SAND, SOLID(24, 2), SAND]}})
        line = [[x0 + 4, seam], [cx - 22, seam + 3], [cx + 8, seam - 3], [x0 + PANEL_W - 4, seam + 2]]
        if name == "feathered":
            props.append(stroke(f"feather-{name}", line, SAND, radius=5, style="rough"))
        if name == "two-tongues":
            props.append(stroke(f"up-{name}", [[px, pz - 4] for px, pz in line], SHORE,
                                radius=6, style="rough", seed=9))
            props.append(stroke(f"down-{name}", [[px, pz + 5] for px, pz in line], SAND,
                                radius=4, style="rough", seed=3))
        if name == "tapered-tongue":
            # The same line, the other brush that keeps its band solid: `tapered` varies the WIDTH along the
            # arc, full in the middle and a third of it at the ends, so a spit fades out instead of stopping.
            props.append(stroke(f"spit-{name}", line, SAND, radius=6, style="tapered"))
        # Ground cover over the seam. Sand takes flora at a third of soil's density, which is why a sand
        # tongue reads as thinned meadow rather than as bare ground.
        props.append(flora(f"cover-{name}", box(cx, seam, PANEL_W - 8, 34)))

    elif name in ("over-a-deck", "keep-clear"):
        # A gill cut across the panel and a plank deck bridging it, with the path running over the deck.
        # Two banks and a gorge between them. One mark with nothing to argue against pins a whole group,
        # so the banks have to be stated as well as the cut; abutting marks make the walls sheer.
        relief[name] = {"base": 14, "reach": 0, "step": 1, "pushes": [], "marks": [
            area(f"north-{name}", 14, box(cx, z0 + 20, PANEL_W - 6, 32)),
            area(f"gill-{name}", 3, box(cx, cz, PANEL_W - 6, 14)),
            area(f"south-{name}", 14, box(cx, z0 + 56, PANEL_W - 6, 32))]}
        members.append(f"deck-{name}")
        deck = {"id": f"deck-{name}", "type": "rectangle", "operation": "add", "floor": 13,
                "height_mode": "level", "base_height": 1, "skirt": 0, "theme": "deck",
                "min_x": cx - 6, "min_z": cz - 11, "max_x": cx + 6, "max_z": cz + 11}
        if name == "keep-clear":
            deck["keepClear"] = True
        shapes.append(deck)
        props.append(stroke(f"way-{name}", [[cx, z0 + 6], [cx, z0 + PANEL_D - 6]], ROAD, radius=3))

    else:
        # A serpentine cut into a hillside: the relief makes the road BED and the stroke paves it.
        route = serpentine(x0, z0)
        relief[name] = {"base": 6, "reach": 0, "step": 1, "pushes": [], "marks": [
            {"id": f"route-{name}", "kind": "line", "h": [32, 6], "r": 12, "tread": 3, "points": route}]}
        if name == "road":
            props.append(stroke(f"way-{name}", route, ROAD))
        if name == "weathered":
            props.append(stroke(f"way-{name}", route, WEATHERED))
        if name in ("verge", "claimed"):
            # Two strokes on one line: the only way to band a path across its own width, because a pave is
            # resolved per cell and the painter hands a stroke no distance from its centerline.
            #
            # The pair differs in one word. A claiming stroke holds the ground it paved against everything
            # placed after it; paint claims nothing and is grown over, which is why paint is the default.
            props.append(stroke(f"verge-{name}", route, COARSE, radius=6,
                                claims=(name == "claimed")))
            props.append(stroke(f"way-{name}", route, ROAD, radius=3,
                                claims=(name == "claimed")))
            props.append(flora(f"cover-{name}", box(cx, cz, PANEL_W - 8, PANEL_D - 8)))
        if name == "by-height":
            props.append(stroke(f"way-{name}", route, {"kind": "layered", "axis": "height", "from": 6,
                "stack": {"ending": "repeat", "bands": [
                    {"thickness": 9, "material": COARSE},
                    {"thickness": 9, "material": COBBLE},
                    {"thickness": 40, "material": ANDESITE}]}}))
        if name == "by-inward":
            props.append(stroke(f"way-{name}", route, {"kind": "layered", "axis": "inward",
                "beyond": PLANKS, "stack": {"ending": "repeat", "bands": [
                    {"thickness": 1, "material": COBBLE},
                    {"thickness": 2, "material": COARSE}]}}))

    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": members})

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 10, "max_x": COL_X[-1] + PANEL_W + 10,
                       "min_z": ROW_Z[0] - 10, "max_z": ROW_Z[-1] + PANEL_D + 10},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
    "dressing": {"props": props},
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "painting-with-a-stroke.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(props)} props -> {out}")
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    mine = [p for p in props if p["id"].endswith(name)]
    said = " ".join(f"{p['kind']}:{p.get('style', '')}" for p in mine)
    print(f"  {name:13s} at x{x0:5d} z{z0:5d}  {said}")
