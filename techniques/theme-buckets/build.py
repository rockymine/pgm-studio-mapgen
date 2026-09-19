"""Writes theme-buckets.layout.json — ten panels carrying one ground and ten themes.

Every panel is the same island solved by the same relief: a plain at 10, a gentle swell to 20 and a mesa
with a sheer skirt to 30, so each has flat ground, a graded shoulder, a face, and the panel's own rim
against the void. Only the theme changes, which is the card: row 1 turns the four buckets on one at a
time, and row 2 is how a bucket's material is banded.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, grid, lobed_ring

PANEL_W, PANEL_D = 64, 60
COL_X, ROW_Z = grid(5, 2, PANEL_W, PANEL_D)
GROUND_TOP = 44
PLAIN = 8

# One landscape, not a swatch book: a grassy upland on sandstone. Meadow over earth, a stone body, a
# sandstone bed the cuts show, a weathered cobble lip, and scree between the turf and the bare rock.
GRASS, DIRT, STONE = SOLID(2), SOLID(3), SOLID(1)
SANDSTONE, COBBLE, GRAVEL, ANDESITE = SOLID(24), SOLID(4), SOLID(13), SOLID(1, 5)


def stack(*bands, ending="repeat"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for m, t in bands]}


def layered(axis, *bands, ending="repeat", **words):
    out = {"kind": "layered", "axis": axis, "stack": stack(*bands, ending=ending)}
    out.update(words)
    return out


SOIL = layered("depth", (GRASS, 1), (DIRT, 2))          # the ordinary surface: turf over earth


def over_soil(top, under=DIRT):
    """One course of a surfacing block over soil. `PT1` refuses a bare surfacing block as a band's material:
    a surfacing block is exactly one course thick and what is under it is earth, so every band of a height
    or slope stack is itself a little depth stack."""
    return layered("depth", (top, 1), (under, 2), ending="handOver")


def theme(surface=None, wall=None, rim=None, fill=None, rim_edges="void", surface_depth=3):
    """A whole ground theme. A bucket left None is switched off, which is how the first row is built."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": rim_edges,
        "rim": {"enabled": rim is not None, "depth": 1, "material": rim or STONE},
        "surface": {"enabled": surface is not None, "depth": surface_depth,
                    "material": surface or STONE},
        "wallEnabled": wall is not None,
        "wallOnTerrainFaces": wall is not None,
        "wall": wall or STONE,
        "fill": fill or STONE,
    }


# Row 1 — the four buckets, switched on one at a time over the same ground.
# Row 2 — how a bucket's material is banded: the axis a surface reads, and what a pattern does to a fill.
THEMES = {
    "fill-only":     theme(fill=STONE),
    "and-surface":   theme(fill=STONE, surface=SOIL),
    "and-wall":      theme(fill=STONE, surface=SOIL, wall=SANDSTONE),
    "and-rim":       theme(fill=STONE, surface=SOIL, wall=SANDSTONE, rim=COBBLE, rim_edges="void"),
    "rim-boundary":  theme(fill=STONE, surface=SOIL, wall=SANDSTONE, rim=COBBLE, rim_edges="boundary"),
    # The same three blocks banded two ways. `height` pins them to world Y, so a stack lands at one
    # altitude in every column; `slope` reads the ground's angle, so one stack puts meadow on the flat and
    # bare rock on the face of the same hill.
    # The same three surfacings in the same order on both axes — meadow, scree, bare rock — so the only
    # difference between the two panels is what decides where they land.
    "axis-height":   theme(fill=STONE, wall=SANDSTONE, surface=layered(
        "height", (over_soil(GRASS), 12), (over_soil(GRAVEL), 8), (over_soil(STONE), 70),
        **{"from": PLAIN})),
    "axis-slope":    theme(fill=STONE, wall=SANDSTONE, surface=layered(
        "slope", (over_soil(GRASS), 20), (over_soil(GRAVEL), 25), (over_soil(STONE), 45))),
    # The fourth axis: bands as concentric rings in from the landmass's void-facing edge — a scree apron.
    "axis-inward":   theme(fill=STONE, wall=SANDSTONE, surface=layered(
        "inward", (over_soil(GRAVEL), 4), (over_soil(STONE), 3), (over_soil(GRASS), 60))),
    # A fill is the tall bucket, so a pattern on it is read on every cut face rather than from above, and
    # `PT4` refuses one with no `rise` because a plane-sampled field stripes every face floor to sky.
    "fill-rise":     theme(surface=SOIL, fill={"kind": "cell", "cellSize": 9, "rise": 5,
                                               "palette": [STONE, ANDESITE, SANDSTONE]}),
    # A wall run varies along the perimeter arc and is constant up a column: a sawn cliff, not a bedded one.
    "wall-run":      theme(fill=STONE, surface=SOIL, wall={"kind": "wallRun", "runs": [
        {"material": SANDSTONE, "width": 6}, {"material": COBBLE, "width": 3},
        {"material": ANDESITE, "width": 4}]}),
}
PANELS = [(name, i % 5, i // 5) for i, name in enumerate(THEMES)]

shapes, groups, relief = [], [], {}
for name, col, row in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": name,
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": [
        # a mesa: 20 over a falloff of 5 is a skirt of 4.0 blocks a cell, which is a face
        {"id": "scar", "ring": lobed_ring(cx - 16, cz, 10, lobes=5, depth=0.16),
         "amount": 24, "falloff": 5, "crown": 0, "roughness": 0, "seed": 1},
        # a swell: 12 over 10 is 1.2, which is a shoulder rather than a face
        {"id": "swell", "ring": lobed_ring(cx + 14, cz, 8, lobes=4, depth=0.14),
         "amount": 12, "falloff": 10, "crown": 0, "roughness": 0, "seed": 2}]}

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "and-rim",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme-buckets.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(THEMES)} themes -> {out}")
for name, col, row in PANELS:
    t = THEMES[name]
    print(f"  {name:14s} surface {str(t['surface']['enabled']):5s} wall {str(t['wallEnabled']):5s} "
          f"rim {str(t['rim']['enabled']):5s} ({t['rimEdges']})")
