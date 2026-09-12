#!/usr/bin/env python3
"""Kilnholt Cut — two rival stonework guilds excavating opposite flanks of one worked-out quarry.

One sentence: two guilds have driven their excavation into opposite flanks of the same worked-out
quarry, each guarding two buried obsidian monuments at the bottom of their own cut, and a played-out
mine adit under the west flank still connects the two sides for whoever is bold enough to use it.

Board shape: one team landmass (spawn fused to its excavation) per side, `rot_180` about the origin,
joined only by a void gap spanned by a build zone (approaches.md: void between the teams, never across
an approach). The ground is finished by ANGLE, not by height — one `layered` stack on the `slope` axis
carries the flat reclaimed floor, the worked stone shoulder and the bare cut face in one material.

The tunnel is written bottom-up as its own layers under the void: the compiled ground layer carries an
override cavity (self-symmetric under `rot_180`, so the fan reproduces it rather than duplicating it),
then `tunnel-walls`, `tunnel-cover` and `tunnel-resume` are new layers stated `mirrors: false` so the
adit is built exactly once, under the west flank only.

Writes sonnet5-kilnholt-cut.plan.json and .finish.json beside this file.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5-kilnholt-cut"

# ---- heights (blocks) --------------------------------------------------------------------------
BASE = 16          # relief base a mark's reach decays toward
RIM = 30           # the outer hillside flanking each cut
CREST = 28         # the spawn knoll
FLOOR = 10         # the worked pit floor the destroyables stand on
BRINK = 6          # the low apron right before the void

TUN_FLOOR = 1       # tunnel floor, world Y
TUN_WALL_TOP = 4    # top of the tunnel's side walls (3 tall corridor)
TUN_COVER_TOP = 6   # top of the roof slab sealing it
TUN_RESUME_TOP = 8  # a little rock resumed above the roof before natural ground picks up

# ---- the two portals: a straight line through the origin, so it is its own rot_180 image --------
RED_PORTAL = (-30.0, -22.0)
BLUE_PORTAL = (30.0, 22.0)


def unit(a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dz)
    return dx / length, dz / length, length


def strip(a, b, n_lo, n_hi):
    """The four corners of a rectangle running a -> b, offset [n_lo, n_hi] along the normal.
    Self-symmetric under rot_180 whenever b == (-a[0], -a[1]) and n_lo == -n_hi."""
    ux, uz, _ = unit(a, b)
    nx, nz = -uz, ux
    return [[round(a[0] + nx * n_lo, 2), round(a[1] + nz * n_lo, 2)],
            [round(b[0] + nx * n_lo, 2), round(b[1] + nz * n_lo, 2)],
            [round(b[0] + nx * n_hi, 2), round(b[1] + nz * n_hi, 2)],
            [round(a[0] + nx * n_hi, 2), round(a[1] + nz * n_hi, 2)]]


def rect_along(a, b, half_width):
    return strip(a, b, -half_width, half_width)


ux, uz, tunnel_len = unit(RED_PORTAL, BLUE_PORTAL)
STAIR_LEN = 11
red_stair_far = (RED_PORTAL[0] - ux * STAIR_LEN, RED_PORTAL[1] - uz * STAIR_LEN)
blue_stair_far = (-red_stair_far[0], -red_stair_far[1])  # the rot_180 image, authored by the fan

# ---- the compiled ground layer: rim, spine, and a self-symmetric floor cavity for the adit -------
CUT_HW = 40       # half-width of the excavation piece, in BLOCKS
CUT_HW_CELLS = CUT_HW // 2   # the same, in cells (cell = 2 blocks)

marks = [
    {"id": "rim-w", "kind": "line", "r": 9,
     "points": [[-34, -90], [-34, -20]], "h": [RIM, RIM - 2]},
    {"id": "rim-e", "kind": "line", "r": 9,
     "points": [[34, -90], [34, -20]], "h": [RIM, RIM - 2]},
    # the spawn knoll, the pit floor and the low apron before the void, one wide descending spine.
    # `tread` keeps the middle 24 blocks either side flat and lofts the outer 14 into whatever
    # `rim-w`/`rim-e` already put there, so the shoulder grades instead of walling at the overlap.
    {"id": "descent", "kind": "line", "r": 38, "tread": 24,
     "points": [[0, -90], [0, -70], [0, -46], [0, -30], [0, -17]],
     "h": [CREST, 20, FLOOR, 9, BRINK]},
]

tunnel_cavity = {
    "id": "adit-cavity", "type": "polygon", "operation": "add", "override": True,
    "floor": 0, "base_height": TUN_FLOOR, "height_mode": "level", "skirt": 0,
    "relief_scope": "exclude",
    "vertices": rect_along(RED_PORTAL, BLUE_PORTAL, 4),
    "theme": "quarry-under",
}

# ---- the tunnel's own layers, bottom-up, stated `mirrors: false` so the fan does not duplicate ---
tunnel_full = rect_along(RED_PORTAL, BLUE_PORTAL, 4)
wall_lo = strip(RED_PORTAL, BLUE_PORTAL, -4, -1.5)
wall_hi = strip(RED_PORTAL, BLUE_PORTAL, 1.5, 4)


def tunnel_group(group_id, shape_ids):
    return [{"id": group_id, "name": group_id, "mirrors": False, "shapeIds": shape_ids}]


tunnel_layers = [
    {"id": "tunnel-walls", "name": "Tunnel Walls", "base_y": TUN_FLOOR,
     "shapes": [
         {"id": "adit-wall-lo", "type": "polygon", "operation": "add",
          "floor": 0, "base_height": TUN_WALL_TOP - TUN_FLOOR, "height_mode": "level", "skirt": 0,
          "vertices": wall_lo, "theme": "quarry-under"},
         {"id": "adit-wall-hi", "type": "polygon", "operation": "add",
          "floor": 0, "base_height": TUN_WALL_TOP - TUN_FLOOR, "height_mode": "level", "skirt": 0,
          "vertices": wall_hi, "theme": "quarry-under"},
     ],
     "groups": tunnel_group("adit-walls", ["adit-wall-lo", "adit-wall-hi"])},
    {"id": "tunnel-cover", "name": "Tunnel Cover", "base_y": TUN_WALL_TOP,
     "shapes": [
         {"id": "adit-cover", "type": "polygon", "operation": "add",
          "floor": 0, "base_height": TUN_COVER_TOP - TUN_WALL_TOP, "height_mode": "level",
          "skirt": 0, "vertices": tunnel_full, "theme": "quarry-under"},
     ],
     "groups": tunnel_group("adit-cover", ["adit-cover"])},
    {"id": "tunnel-resume", "name": "Tunnel Resume", "base_y": TUN_COVER_TOP,
     "shapes": [
         {"id": "adit-resume", "type": "polygon", "operation": "add",
          "floor": 0, "base_height": TUN_RESUME_TOP - TUN_COVER_TOP, "height_mode": "level",
          "skirt": 2, "vertices": tunnel_full, "theme": "quarry-cut"},
     ],
     "groups": tunnel_group("adit-resume", ["adit-resume"])},
]

# the stair back to the surface at the red end; the fan builds blue's for free
stair_red = {
    "id": "adit-stair-red", "type": "polygon", "operation": "add", "override": True,
    "floor": 0, "base_height": 1, "height_mode": "level", "skirt": 0,
    "relief_scope": "exclude",
    # strip()'s vertex order is [near-lo, far-lo, far-hi, near-hi] -- the two RED_PORTAL corners
    # are index 0 and 3, the two surface-end corners are 1 and 2.
    "vertices": rect_along(RED_PORTAL, red_stair_far, 3),
    "anchor_heights": [TUN_FLOOR, RIM - 16, RIM - 16, TUN_FLOOR],
    "theme": "quarry-cut",
}

# ---- materials -----------------------------------------------------------------------------------
def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


def cell(size, *mats, rise=0):
    doc = {"kind": "cell", "cellSize": size, "palette": [solid(*m) for m in mats]}
    if rise:
        doc["rise"] = rise
    return doc


def layered_depth(top, soil, depth=2):
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": 1}, {"material": soil, "thickness": depth}]}}


# grass reclaiming a played-out floor, a worked-stone shoulder, bare rock on the cut face —
# finished by the angle of the ground, not by its height (`incline?format=text` decided the cuts)
SLOPE_MASK = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": layered_depth(solid(2), cell(3, (3, 0), (3, 1)), 2), "thickness": 28},
    {"material": layered_depth(cell(4, (3, 1), (4, 0)), solid(3, 1)), "thickness": 16},
    {"material": cell(4, (1, 0), (4, 0), (1, 5)), "thickness": 46},
]}}

STRATA = {"kind": "layered", "layers": [
    {"material": solid(1), "thickness": 3}, {"material": solid(4), "thickness": 1},
    {"material": solid(1, 5), "thickness": 3}, {"material": solid(1), "thickness": 2},
    {"material": solid(4), "thickness": 2}]}

THEME_CUT = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
    "wallOnTerrainFaces": True, "rim": {"material": solid(1, 5), "depth": 1, "enabled": False},
    "surface": {"material": SLOPE_MASK, "depth": 2, "enabled": True},
    "wall": {"kind": "wallRun", "runs": [{"material": STRATA, "width": 6}]},
    "wallEnabled": True, "fill": cell(7, (1, 0), (1, 5), (4, 0), rise=8),
}
THEME_UNDER = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "drop",
    "wallOnTerrainFaces": True, "rim": {"material": solid(4), "depth": 1, "enabled": False},
    "surface": {"material": cell(3, (1, 0), (1, 5), (4, 0)), "depth": 2, "enabled": True},
    "wall": {"kind": "wallRun", "runs": [{"material": STRATA, "width": 6}]},
    "wallEnabled": True, "fill": solid(1),
}

# ---- the winch shed: a fork of the "cottage" preset, timber posts over a brick wall --------------
SHED = {
    "foundation": {"plate": {"stack": {"bands": [{"material": solid(4), "thickness": 1}],
                                        "ending": "repeat"}, "extent": 2},
                   "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                               "inlayInset": 2, "isPlain": True},
                   "footing": None},
    "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
             "ridgeCap": True, "hole": False,
             "body": solid(5, 1), "verge": solid(5, 1), "gable": solid(5, 1),
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1, "hostData": 0,
                               "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": solid(45), "thickness": 5}], "ending": "repeat"},
             "extent": 5},
    "post": solid(17, 1),
    "windows": {"form": "arched", "block": 109, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 3, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None, "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air", "head": {"form": "arched", "block": 109, "fill": "upperSlab",
                                         "fillBlock": 44, "fillData": 5}, "width": 2, "height": 3},
}

# ---- dressing --------------------------------------------------------------------------------
dressing_props = [
    {"id": "path-approach", "kind": "stroke", "style": "solid", "radius": 3,
     "pave": cell(3, (13, 0), (1, 5), (4, 0)), "claimsGround": True,
     "points": [[0, -80], [0, -60], [0, -50]]},
    {"id": "shed-1", "kind": "house", "seed": 90, "points": [[-24, -73], [-16, -65]],
     "front": "posZ", "style": SHED},
]

rim_trees = [(-36, -64, 71), (-33, -34, 44), (36, -60, 19), (33, -30, 8),
             (-37, -50, 63), (37, -46, 27)]
for tx, tz, seed in rim_trees:
    dressing_props.append({"id": f"tree-rim-{seed}", "kind": "tree", "x": tx, "z": tz,
                            "seed": seed, "form": "template", "species": "spruce",
                            "height": 10 + seed % 5})

finish = {
    "authors": ["Sonnet 5"], "created": "2026-09-11",
    "relief": {"team": {"base": BASE, "reach": 30, "step": 1, "landform": "rolling",
                        "grain": {"amplitude": 0.5, "scale": 18, "seed": 71},
                        "marks": marks}},
    "addShapes": [tunnel_cavity, stair_red],
    "addLayers": tunnel_layers,
    "themes": {"quarry-cut": THEME_CUT, "quarry-under": THEME_UNDER},
    "mapTheme": "quarry-cut",
    "themeByHeight": {},
    "roomStyles": {},
    "dressing": {"props": dressing_props},
}

# ---- the plan: one spawn piece fused to one big excavation piece, per team -----------------------
plan = {
    "plan": 2, "meta": {"name": "Kilnholt Cut"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": BASE, "observerY": 52},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-5, -47, 10, 10], "surface": BASE},
        {"id": "cut", "role": "piece", "rect": [-CUT_HW_CELLS, -37, 2 * CUT_HW_CELLS, 29],
         "surface": BASE},
    ],
    "zones": [
        {"id": "the-gap", "rect": [-CUT_HW_CELLS, -8, 2 * CUT_HW_CELLS, 16]},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 10], "facing": "back"}],
        "destroyables": [
            {"id": "destroyable-1", "piece": "", "at": [-19, -50], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "Kilnholt's Deep Mark"},
            {"id": "destroyable-2", "piece": "", "at": [19, -50], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "Kilnholt's Shallow Mark"},
        ],
    },
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)
print(f"{len(marks)} relief mark(s), {len(finish['addShapes'])} authored shape(s), "
      f"{len(tunnel_layers)} tunnel layer(s), {len(dressing_props)} dressing prop(s), "
      f"tunnel length {tunnel_len:.1f}")
