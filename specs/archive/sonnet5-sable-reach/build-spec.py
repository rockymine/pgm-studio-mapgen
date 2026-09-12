#!/usr/bin/env python3
"""Writes sonnet5-sable-reach.plan.json and sonnet5-sable-reach.finish.json.

Two rival trading posts face each other across a tidal river mouth. Each team's site is two
landmasses -- a main settlement island (quay, warehouse district, plaza, spawn, wool room) and a
smaller flanking mudbank/dock skerry -- joined by a short build zone. The two teams' islands are
joined only by a build zone spanning the tidal channel; a permanent timber-and-stone causeway
(the "low bridge") is the primary chokepoint and a pair of shallow sand fords are the secondary
route, per the wool-approach law (WL8): one chokepoint, plus an alternative.
"""
import json
import os

SLUG = "sonnet5-sable-reach"
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- blocks --
SAND = {"kind": "solid", "id": 12, "data": 0}
SANDSTONE = {"kind": "solid", "id": 24, "data": 0}
GRAVEL = {"kind": "solid", "id": 13, "data": 0}
CLAY = {"kind": "solid", "id": 82, "data": 0}
DIRT = {"kind": "solid", "id": 3, "data": 0}
COARSE_DIRT = {"kind": "solid", "id": 3, "data": 1}
STONE = {"kind": "solid", "id": 1, "data": 0}
ANDESITE = {"kind": "solid", "id": 1, "data": 5}
COBBLESTONE = {"kind": "solid", "id": 4, "data": 0}
STONE_BRICK = {"kind": "solid", "id": 98, "data": 0}
SPRUCE_PLANKS = {"kind": "solid", "id": 5, "data": 1}
OAK_LOG = {"kind": "solid", "id": 17, "data": 0}
GLASS_PANE = 102


def cell(seed, size, jitter, warp, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def band_stack(bands, ending="repeat"):
    return {"bands": [{"material": m, "thickness": t} for m, t in bands], "ending": ending}


def top_band(material, depth, enabled=True):
    return {"material": material, "depth": depth, "enabled": enabled}


# --------------------------------------------------------------- themes --

THEME_SHORE = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "rim": {"material": SAND, "depth": 1, "enabled": False},
    "surface": top_band(cell(101, 6, 40, 1, [SAND, SAND, SANDSTONE]), 3),
    "wall": {"kind": "solid", "id": 24, "data": 0},
    "fill": {"kind": "solid", "id": 12, "data": 0},
}

MUD_MATERIAL = cell(102, 5, 40, 1, [COARSE_DIRT, GRAVEL, CLAY], rise=3)

THEME_SETTLEMENT = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "rim": {"material": {"kind": "teamTint", "blockId": 159, "neutral": STONE_BRICK},
            "depth": 1, "enabled": True},
    "surface": top_band(cell(103, 6, 30, 1, [GRAVEL, ANDESITE, COBBLESTONE]), 3),
    "wall": {
        "kind": "wallDiagonal",
        "slope": 1,
        "runs": [
            {"material": {"kind": "layered",
                          "stack": band_stack([(COBBLESTONE, 3), (ANDESITE, 1), (STONE_BRICK, 2)])},
             "width": 6},
        ],
    },
    "fill": {"kind": "solid", "id": 1, "data": 0},
}

THEME_SKERRY = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "rim": {"material": GRAVEL, "depth": 1, "enabled": False},
    "surface": top_band(cell(104, 5, 45, 2, [COARSE_DIRT, GRAVEL, GRAVEL, CLAY]), 3),
    "wall": {"kind": "solid", "id": 1, "data": 5},
    "fill": {"kind": "solid", "id": 13, "data": 0},
}

THEMES = {"estuary-shore": THEME_SHORE, "sable-town": THEME_SETTLEMENT, "sable-skerry": THEME_SKERRY}

# ---------------------------------------------------------- house styles --

def timber_style(wall_extent, roof_form, checker_species_a, checker_species_b, window_h):
    return {
        "foundation": {
            "plate": {"stack": band_stack([(COBBLESTONE, 1)]), "extent": 1},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": None,
        },
        "roof": {
            "form": roof_form,
            "pitch": 1,
            "slab": -1,
            "slabData": 0,
            "overhang": 1,
            "ridgeCap": True,
            "hole": False,
            "body": SPRUCE_PLANKS,
            "verge": {"kind": "laidLog", "id": 17, "data": 0},
            "gable": SPRUCE_PLANKS,
            "gableWindows": {"form": "open", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                              "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {
            "stack": {
                "bands": [
                    {"material": {"kind": "laidLog", "id": 17, "data": checker_species_a}, "thickness": 2},
                    {"material": {"kind": "checker", "size": 1,
                                  "even": {"kind": "solid", "id": 17, "data": checker_species_a},
                                  "odd": {"kind": "solid", "id": 17, "data": checker_species_b}},
                     "thickness": 1},
                    {"material": SPRUCE_PLANKS, "thickness": wall_extent - 3},
                ],
                "ending": "repeat",
            },
            "extent": wall_extent,
        },
        "post": OAK_LOG,
        "windows": {"form": "arched", "block": 109, "hostBlock": -1, "hostData": 0,
                     "data": 0, "sill": 3, "width": 2, "height": window_h, "spacing": 4},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": 17, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "web", "head": {"form": "arched", "block": 109, "fill": "upperSlab",
                                              "fillBlock": 44, "fillData": 5},
                     "width": 2, "height": 3},
    }


WAREHOUSE_STYLE = timber_style(wall_extent=8, roof_form="gable", checker_species_a=0,
                                checker_species_b=1, window_h=2)
COTTAGE_STYLE = timber_style(wall_extent=5, roof_form="hip", checker_species_a=1,
                              checker_species_b=0, window_h=2)


# -------------------------------------------------------------- the plan --

def make_plan():
    return {
        "plan": 2,
        "meta": {"name": "Sable Reach"},
        "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": 10,
                    "observerY": 46},
        "pieces": [
            {"id": "quay", "role": "piece", "rect": [-10, 3, 20, 3], "surface": 9},
            {"id": "warehouse", "role": "piece", "rect": [-10, 6, 20, 7], "surface": 12},
            {"id": "back-w", "role": "piece", "rect": [-10, 13, 3, 4], "surface": 12},
            {"id": "spawn", "role": "spawn", "rect": [-7, 13, 6, 4], "surface": 12},
            {"id": "back-mid", "role": "piece", "rect": [-1, 13, 1, 4], "surface": 12},
            {"id": "back-e", "role": "piece", "rect": [0, 13, 10, 4], "surface": 12},
            {"id": "rear", "role": "piece", "rect": [-10, 17, 20, 2], "surface": 12},
            {"id": "wool-w", "role": "piece", "rect": [-10, 19, 4, 4], "surface": 12},
            {"id": "wool", "role": "wool-room", "rect": [-6, 19, 6, 4], "surface": 12},
            {"id": "wool-e", "role": "piece", "rect": [0, 19, 10, 4], "surface": 12},
            {"id": "skerry", "role": "piece", "rect": [13, 6, 7, 8], "surface": 7},
        ],
        "zones": [
            {"id": "mid-band", "rect": [-8, -3, 16, 6], "holes": []},
            {"id": "skerry-link", "rect": [10, 6, 3, 7], "holes": []},
            {"id": "plaza-yard", "rect": [-3, 8, 6, 3], "holes": []},
        ],
        "placements": {
            "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [15, 10], "facing": "front",
                        "footprint": [5, 3, 20, 14]}],
            "wools": [{"id": "wool-1", "piece": "wool", "at": [15, 10],
                       "footprint": [5, 3, 20, 14]}],
            "iron": [], "destroyables": [], "cores": [],
        },
    }


# ------------------------------------------------------------- the finish --

def ramp(shape_id, x0, x1, z0, z1, h_low, h_high, theme):
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
            "base_height": h_high, "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude", "theme": theme,
            "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]],
            "anchor_heights": [h_low, h_low, h_high, h_high]}


def flat(shape_id, x0, x1, z0, z1, height, theme=None, material=None, keep_clear=False, floor=0):
    # `theme` and `material` answer the same question and may not both be stated (SK24): a
    # theme is read bucket by bucket, a material paints the shape's whole span outright.
    shape = {"id": shape_id, "type": "polygon", "operation": "add", "floor": floor,
             "base_height": height, "height_mode": "level", "skirt": 0,
             "relief_scope": "exclude",
             "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}
    if material is not None:
        shape["material"] = material
    else:
        shape["theme"] = theme
    if keep_clear:
        shape["keepClear"] = True
    return shape


def make_add_shapes():
    shapes = []
    # The town stair: quay (top y8) climbs to the warehouse plateau (top y11) over the seam
    # both pieces share at z = 30.
    shapes.append(ramp("town-stair", -6, 6, 25, 35, 9, 12, "sable-town"))

    # The ford: a shallow sand causeway off-centre, with a narrower band of mud fraying into
    # the water on each edge. It auto-fans to a second ford on the opposite flank under
    # rot_180, so both teams get one near their own side.
    shapes.append(flat("ford-a-sand", -25, -15, -15, 15, 8, "estuary-shore"))
    shapes.append(flat("ford-a-mud-w", -28, -25, -15, 15, 8, "estuary-shore", material=MUD_MATERIAL))
    shapes.append(flat("ford-a-mud-e", -15, -12, -15, 15, 8, "estuary-shore", material=MUD_MATERIAL))

    # The bridge: a low, permanent timber-and-stone causeway at the centre of the channel --
    # the single, made, keepClear chokepoint. Flush with the quay on both banks.
    shapes.append(flat("bridge", -4, 4, -15, 15, 9, "sable-town", keep_clear=True, floor=1))
    return shapes


def make_dressing():
    props = []

    stony_pave = {"kind": "cell", "seed": 201, "cellSize": 3, "jitter": 30, "warp": 1,
                  "palette": [GRAVEL, ANDESITE, COBBLESTONE]}
    woody_pave = {"kind": "cell", "seed": 202, "cellSize": 3, "jitter": 30, "warp": 1,
                  "palette": [DIRT, COARSE_DIRT, SPRUCE_PLANKS]}

    props.append({"id": "path-quay", "kind": "stroke", "seed": 1, "radius": 3, "style": "solid",
                  "coverage": 1.0, "pave": stony_pave, "points": [[0, 17], [0, 30]]})
    props.append({"id": "path-spine", "kind": "stroke", "seed": 2, "radius": 2.5, "style": "solid",
                  "coverage": 1.0, "pave": woody_pave,
                  "points": [[0, 30], [0, 45], [0, 60], [0, 74]]})
    props.append({"id": "path-wool", "kind": "stroke", "seed": 3, "radius": 2, "style": "solid",
                  "coverage": 1.0, "pave": woody_pave,
                  "points": [[0, 74], [-5, 86], [-15, 98], [-15, 108]]})
    props.append({"id": "path-skerry", "kind": "stroke", "seed": 4, "radius": 2, "style": "worn",
                  "coverage": 0.8, "pave": woody_pave,
                  "points": [[10, 42], [50, 42], [75, 48], [90, 55]]})
    props.append({"id": "path-wool-flank-w", "kind": "stroke", "seed": 5, "radius": 1.5,
                  "style": "worn", "coverage": 0.75, "pave": woody_pave,
                  "points": [[-15, 100], [-38, 102]]})
    props.append({"id": "path-wool-flank-e", "kind": "stroke", "seed": 6, "radius": 1.5,
                  "style": "worn", "coverage": 0.75, "pave": woody_pave,
                  "points": [[3, 100], [38, 102]]})

    def house(prop_id, style, cx, cz, w, d, front, seed):
        return {"id": prop_id, "kind": "house", "seed": seed, "front": front, "style": style,
                "wings": [{"corners": [[cx, cz], [cx + w, cz + d]]}]}

    props.append(house("h-warehouse-w1", WAREHOUSE_STYLE, -46, 34, 12, 10, "posZ", 11))
    props.append(house("h-warehouse-w2", WAREHOUSE_STYLE, -46, 48, 12, 9, "posZ", 12))
    props.append(house("h-cottage-e1", COTTAGE_STYLE, 22, 34, 9, 7, "posZ", 13))
    props.append(house("h-cottage-e2", COTTAGE_STYLE, 22, 48, 9, 7, "posZ", 14))
    props.append(house("h-dock-shed", COTTAGE_STYLE, 76, 44, 8, 6, "posZ", 15))

    def boulder(prop_id, x, z, size, form, seed):
        return {"id": prop_id, "kind": "boulder", "seed": seed, "x": x, "z": z, "form": form,
                "size": size, "mossy": False,
                "rock": {"kind": "cell", "seed": seed + 900, "cellSize": 3, "jitter": 40,
                          "warp": 1, "rise": 1, "palette": [ANDESITE, STONE, GRAVEL]}}

    props.append(boulder("b1", 72, 38, 3.5, "round", 31))
    props.append(boulder("b2", 95, 62, 4, "outcrop", 32))
    props.append(boulder("b3", -20, 0, 3, "angular", 33))

    def tree(prop_id, x, z, species, height, seed):
        return {"id": prop_id, "kind": "tree", "seed": seed, "x": x, "z": z, "form": "template",
                "species": species, "height": height}

    for index, x in enumerate((-45, -37, 37, 45)):
        props.append(tree(f"t-rear-{index}", x, 102, "spruce", 9 + (index % 2), 40 + index))
    props.append(tree("t-skerry-1", 70, 60, "spruce", 8, 44))
    props.append(tree("t-skerry-2", 92, 40, "spruce", 7, 45))

    props.append({"id": "f-rear", "kind": "flora", "seed": 51,
                  "points": [[-48, 86], [48, 86], [48, 94], [-48, 94]],
                  "spec": {"coverage": 0.35, "scale": 10, "octaves": 2, "fernShare": 0.25,
                            "flowerShare": 0.08, "flowerScale": 14, "tallShare": 0.08}})
    props.append({"id": "f-wool-flanks", "kind": "flora", "seed": 53,
                  "points": [[-48, 97], [48, 97], [48, 113], [-48, 113]],
                  "spec": {"coverage": 0.3, "scale": 10, "octaves": 2, "fernShare": 0.22,
                            "flowerShare": 0.06, "flowerScale": 12, "tallShare": 0.06}})
    props.append({"id": "f-skerry", "kind": "flora", "seed": 52,
                  "points": [[68, 33], [97, 33], [97, 67], [68, 67]],
                  "spec": {"coverage": 0.18, "scale": 8, "octaves": 2, "fernShare": 0.2,
                            "flowerShare": 0.02, "flowerScale": 10, "tallShare": 0.05}})

    return {"props": props}


def make_finish():
    return {
        "authors": [{"name": "Sonnet 5"}],
        "created": "2026-09-11",
        "themes": THEMES,
        "mapTheme": "estuary-shore",
        # Keyed on the shape ids the compile actually emits (read off POST /plan/compile),
        # not the plan's own piece ids: abutting equal-height pieces fuse into one polygon
        # named for the component, and a spawn or wool piece compiles to its own shape.
        "themeById": {
            "back-e-12": "sable-town", "back-e-9": "sable-town", "skerry-7": "sable-skerry",
            "spawn-red": "sable-town", "spawn-blue": "sable-town",
            "wool-red-red": "sable-town", "wool-blue-blue": "sable-town",
        },
        "addShapes": make_add_shapes(),
        "roomStyles": {"wool": WAREHOUSE_STYLE, "spawn": WAREHOUSE_STYLE},
        "dressing": make_dressing(),
    }


def main():
    plan = make_plan()
    finish = make_finish()
    with open(os.path.join(OUT, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(OUT, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")


if __name__ == "__main__":
    main()
