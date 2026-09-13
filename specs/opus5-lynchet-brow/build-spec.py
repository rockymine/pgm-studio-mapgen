#!/usr/bin/env python3
"""Lynchet Brow — a hillside farmed into terraces, where every fight is about getting up or down
exactly one retaining wall.

Where made ground meets grown ground, worked as a whole board. Four decisions carry it:

  the made ground is relief_scope "exclude", never "hold" — hold lets the relief ramp up to meet
    the shelf, and then there is no step and no reason for a stair;
  the boundary is not a straight line — each terrace's downhill edge carries a re-entrant, and
    every one of them is cut to exactly the flight that fills it;
  the height is bridged by a stair and not by the relief — height_mode "level" with
    anchor_heights, skirt 0, keepClear, a material rather than a theme, and three times the run
    as rise;
  the made ground's face is where its paint goes — wallRun along the perimeter, wallDiagonal to
    shear the stripes by height, and a teamTint in the wall of the terrace the core stands on.

Writes <slug>.plan.json and <slug>.finish.json beside itself.
"""
import json, math, os, random

SLUG = "opus5-lynchet-brow"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- blocks
#   GROUND  green pasture — grass, dirt, coarse dirt. The hill is grown.
#   BUILT   drystone — cobble, mossy cobble, andesite, stone. Every wall and every flight.
#   ACCENT  the team's own clay, in one stripe of the terrace its core stands on.
GRASS   = {"kind": "solid", "id": 2,   "data": 0}
DIRT    = {"kind": "solid", "id": 3,   "data": 0}
COARSE  = {"kind": "solid", "id": 3,   "data": 1}
STONE   = {"kind": "solid", "id": 1,   "data": 0}
ANDESITE = {"kind": "solid", "id": 1,  "data": 5}
POLANDES = {"kind": "solid", "id": 1,  "data": 6}
COBBLE  = {"kind": "solid", "id": 4,   "data": 0}
MOSSCOB = {"kind": "solid", "id": 48,  "data": 0}
GRAVEL  = {"kind": "solid", "id": 13,  "data": 0}
OAK     = {"kind": "solid", "id": 5,   "data": 0}
OAKLOG  = {"kind": "solid", "id": 17,  "data": 0}
BRICKS  = {"kind": "solid", "id": 98,  "data": 0}
MOSSBRK = {"kind": "solid", "id": 98,  "data": 1}
HAY     = {"kind": "solid", "id": 170, "data": 0}

def depth_stack(bands, beyond=None, ending="handOver"):
    out = {"kind": "layered", "axis": "depth",
           "stack": {"ending": ending,
                     "bands": [{"material": m, "thickness": t} for m, t in bands]}}
    if beyond:
        out["beyond"] = beyond
    return out

def slope_stack(bands, beyond=None):
    """Thicknesses here are spans of DEGREES, so one stack finishes the pasture, the shoulder and
    the broken face of the same hill."""
    out = {"kind": "layered", "axis": "slope",
           "stack": {"ending": "repeat",
                     "bands": [{"material": m, "thickness": t} for m, t in bands]}}
    if beyond:
        out["beyond"] = beyond
    return out

def theme(surface, wall, fill, rim, depth=3, rim_edges="void", wall_on_faces=True):
    return {"bedrock": {"relative": False, "value": 1},
            "rimEdges": rim_edges,
            "wallOnTerrainFaces": wall_on_faces,
            "rim": {"enabled": True, "depth": 1, "material": rim},
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall,
            "wallEnabled": True,
            "fill": fill}

def lobe(cx, cz, rx, rz, n, wobble, seed):
    rnd = random.Random(seed)
    return [[round(cx + rx * (1 + wobble * (rnd.random() - .5)) * math.cos(2 * math.pi * i / n)),
             round(cz + rz * (1 + wobble * (rnd.random() - .5)) * math.sin(2 * math.pi * i / n))]
            for i in range(n)]

# ---------------------------------------------------------------- the hillside, stated once
VALLEY, BROW = 20, 36
XW, XE = -44, 43                     # the farmed block; the hill's two ends stay unterraced
NOTCH_HALF, NOTCH_RUN = 2, 8         # a flight 5 wide, 8 of run for 4 of rise

# id, top height, z band (uphill..downhill), the x of each flight up ONTO it
TERRACES = [
    ("lynch1", 24, -36, -21, [-30, 18]),
    ("lynch2", 28, -52, -37, [26, -10]),
    ("lynch3", 32, -68, -53, [-36, 34]),
    ("lynch4", 36, -84, -69, [6, -24]),
]

def terrace_ring(zmin, zmax, notches, seed):
    """A terrace's outline. The uphill edge wanders; the downhill edge is cut back by exactly one
    flight's run at every x a flight climbs, so the stair stands in a bay of the wall rather than
    sticking out of it."""
    rnd = random.Random(seed)
    ring = [[XW, zmin]]
    for x in range(XW + 12, XE - 6, 12):
        ring.append([x, zmin + rnd.choice([-2, -1, 0, 1, 2])])
    ring.append([XE, zmin])
    ring.append([XE, zmax])
    for cx in sorted(notches, reverse=True):          # east to west along the downhill edge
        ring.append([cx + NOTCH_HALF, zmax])
        ring.append([cx + NOTCH_HALF, zmax - NOTCH_RUN])
        ring.append([cx - NOTCH_HALF, zmax - NOTCH_RUN])
        ring.append([cx - NOTCH_HALF, zmax])
    ring.append([XW, zmax])
    return ring

shapes, flights = [], []
below = VALLEY
for (tid, top, zmin, zmax, notches) in TERRACES:
    shapes.append({
        "id": tid, "type": "polygon", "operation": "add", "floor": 0,
        # exclude, never hold: the relief is left to make whatever hillside it would have made and
        # meets this shelf at a face. That face is the retaining wall the whole board is about.
        "relief_scope": "exclude", "base_height": top + 1,
        "vertices": terrace_ring(zmin, zmax, notches, 70 + top),
        "theme": "lynchet-tint" if tid == "lynch2" else "lynchet"})
    for j, cx in enumerate(notches):
        flights.append({
            "id": f"{tid}-stair-{j}", "type": "polygon", "operation": "add", "floor": 0,
            "height_mode": "level", "skirt": 0, "keepClear": True,
            "base_height": below,
            "vertices": [[cx - NOTCH_HALF, zmax - NOTCH_RUN], [cx + NOTCH_HALF, zmax - NOTCH_RUN],
                         [cx + NOTCH_HALF, zmax + 1], [cx - NOTCH_HALF, zmax + 1]],
            "anchor_heights": [top, top, below, below],
            # A material rather than a theme: a flight is made, and it is the same stone top to
            # bottom even where the shelf above and the floor below each have their own.
            "material": {"kind": "cell", "seed": 90 + j, "cellSize": 9, "jitter": 2, "warp": 3,
                         "rise": 6, "palette": [COBBLE, ANDESITE]}})
    below = top
# ---------------------------------------------------------------- the plan
CELL = 4
plan = {
    "plan": 2,
    "meta": {"name": "Lynchet Brow"},
    # Every piece at one surface. The plan states the arrangement — a brow, four lynchets, a holm
    # and the two rough ends — and the relief and the excluded shelves state every height on it.
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20, "surface": VALLEY},
    "pieces": [
        {"id": "brow",   "role": "piece", "rect": [-13, -26, 26, 5]},   # x -52..51  z -104..-85
        {"id": "camp",   "role": "spawn", "rect": [-3, -25, 5, 4]},     # x -12..7   z -100..-85
        {"id": "lynch4", "role": "piece", "rect": [-13, -21, 26, 4]},   #            z  -84..-69
        {"id": "lynch3", "role": "piece", "rect": [-13, -17, 26, 4]},   #            z  -68..-53
        {"id": "lynch2", "role": "piece", "rect": [-13, -13, 26, 4]},   #            z  -52..-37
        {"id": "lynch1", "role": "piece", "rect": [-13, -9, 26, 4]},    #            z  -36..-21
        # The holm is split three ways, so the valley bottom is a junction rather than a corridor
        # running the board's whole length.
        {"id": "holm",   "role": "piece", "rect": [-8, -5, 16, 5]},     # x -32..31  z  -20..-1
        {"id": "ing-w",  "role": "piece", "rect": [-13, -5, 5, 5]},     # x -52..-33
        {"id": "ing-e",  "role": "piece", "rect": [8, -5, 5, 5]},       # x  32..51
    ],
    "zones": [{"id": "bottom", "rect": [-13, -6, 26, 12]}],             # x -52..51  z -24..23
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 8], "facing": "back",
                    "footprint": [2, 2, 16, 12]}],
        # The core stands on the second lynchet, backed against the third's wall so the casing has
        # ground on every side and a breach has somewhere to pool rather than an edge to fall off.
        "cores": [{"id": "lynchet-core", "at": [-24, -50], "lava": 3, "lavaHeight": 3,
                   "float": 5, "leak": 4, "name": "Brow Core"}],
    },
}

# ---------------------------------------------------------------- themes
DRYSTONE_RUNS = [{"material": COBBLE, "width": 3},
                 {"material": ANDESITE, "width": 2},
                 {"material": MOSSCOB, "width": 1},
                 {"material": STONE, "width": 2}]

PASTURE = slope_stack([(depth_stack([(GRASS, 1), (DIRT, 3)], beyond=STONE), 24),
                       (depth_stack([(COARSE, 1), (DIRT, 2), (STONE, 1)], beyond=STONE), 16),
                       (depth_stack([(COBBLE, 1), (STONE, 3)], beyond=STONE), 50)],
                      beyond=STONE)
HILLFILL = {"kind": "voronoi", "seed": 23, "cellSize": 16, "rise": 8,
            "bands": [{"material": ANDESITE, "depth": 2}, {"material": STONE, "depth": 1}]}

GROWN = theme(surface=PASTURE,
              # The grown hill's own broken edges are bedded, not coursed.
              wall={"kind": "noise", "seed": 33, "scale": 14, "octaves": 3, "rise": 9,
                    "stops": [STONE, ANDESITE, COBBLE]},
              fill=HILLFILL, rim=STONE)

LYNCHET = theme(surface=PASTURE,
                # wallRun stands vertical and wraps the perimeter: a retaining wall is coursed.
                wall={"kind": "wallDiagonal", "slope": 4, "runs": DRYSTONE_RUNS},
                fill=HILLFILL, rim=COBBLE)

LYNCHET_TINT = theme(surface=PASTURE,
                     # One course of the team's own clay, so a player reads whose terrace they are
                     # looking at from the far side of the valley.
                     wall={"kind": "wallRun", "runs": [
                         {"material": COBBLE, "width": 3},
                         {"material": {"kind": "teamTint", "blockId": 159, "neutral": ANDESITE},
                          "width": 1},
                         {"material": MOSSCOB, "width": 2},
                         {"material": STONE, "width": 2}]},
                     fill=HILLFILL, rim=COBBLE)

# ---------------------------------------------------------------- the shell
def house_style(wall_mat, plate, roof_body, roof_form, post, storeys, slab, slab_data,
                verge_log=(17, 0), beams=False, window_block=126, window_data=0, head_block=53):
    top_course = {"kind": "laidLog", "id": verge_log[0], "data": verge_log[1]}
    def band(stack):
        out = [{"material": m, "thickness": t} for m, t in stack]
        if beams:
            out.append({"material": top_course, "thickness": 1})
        return out
    def storey(clear, wall):
        return {"clear": clear,
                "wall": {"stack": {"bands": band(wall), "ending": "repeat"}, "extent": clear},
                "post": post,
                "windows": {"form": "slabBanded", "block": window_block, "hostBlock": -1,
                            "hostData": 0, "data": window_data, "sill": 2, "width": 2,
                            "height": 2, "spacing": 4},
                "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                            "inlayInset": 2, "isPlain": True},
                "deck": None, "headroom": clear}
    return {
        "foundation": {"plate": {"stack": {"bands": [{"material": plate, "thickness": 1}],
                                           "ending": "repeat"}, "extent": 2},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": roof_form, "pitch": 1, "slab": slab, "slabData": slab_data, "overhang": 1,
                 "ridgeCap": True, "hole": False, "body": roof_body, "verge": top_course,
                 "gable": roof_body,
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}},
        "wall": {"stack": {"bands": band(wall_mat), "ending": "repeat"}, "extent": 5},
        "post": post,
        "windows": {"form": "slabBanded", "block": window_block, "hostBlock": -1, "hostData": 0,
                    "data": window_data, "sill": 2, "width": 2, "height": 2, "spacing": 4},
        "storeys": [storey(c, w) for c, w in storeys],
        "porch": None, "front": None,
        "beams": ({"block": verge_log[0], "data": verge_log[1], "reach": 1, "any": False}
                  if beams else {"block": -1, "data": 0, "reach": 1, "any": False}),
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": head_block, "fill": "upperSlab",
                             "fillBlock": slab, "fillData": slab_data},
                    "width": 3, "height": 4},
    }

# Built, and never the ground's family: the field walls are drystone, so the buildings are timber
# and lime over a mossy-brick plinth.
STEADING = house_style(wall_mat=[(OAK, 3), (MOSSBRK, 1)], plate=MOSSBRK, roof_body=OAK,
                       roof_form="gable", post=OAKLOG,
                       storeys=[(5, [(OAK, 3), (BRICKS, 1)]), (4, [(OAK, 4)])],
                       slab=126, slab_data=0, beams=True)
BYRE = house_style(wall_mat=[(MOSSBRK, 3), (OAK, 2)], plate=MOSSBRK, roof_body=OAK,
                   roof_form="shed", post=OAKLOG, storeys=[], slab=126, slab_data=0, beams=True)

# ---------------------------------------------------------------- the relief
# Only ground a player walks is pinned: the holm at the bottom and the brow at the top. Everything
# between is the relaxation's, which is what lets the hillside arrive under the shelves instead of
# being cut into steps a second time.
relief = {
    "*": {
        "base": VALLEY,
        "reach": 0,
        "step": 1,
        "grain": {"amplitude": 1.3, "scale": 19, "seed": 5},
        "marks": [
            {"id": "holm", "kind": "area", "h": VALLEY, "bevel": 4,
             "ring": lobe(0, -12, 50, 13, 11, 0.14, 3)},
            {"id": "brow", "kind": "area", "h": BROW, "bevel": 3,
             "ring": lobe(-2, -95, 48, 11, 11, 0.13, 4)},
            # The steading's own pad, wider than the shell on every side. A stamped shell levels
            # the column under its whole footprint at the footprint's highest, so a neighbouring
            # cell below that floor is met with a face of bedrock nobody drew (WX11).
            {"id": "roompad", "kind": "area", "h": BROW,
             "ring": [[-20, -106], [15, -106], [15, -78], [-20, -78]]},
        ],
        "pushes": [
            # A knoll on the brow's west shoulder, its ring past the coast at z -104 so the crest
            # is behind the map. 14 over a falloff of 12 is 1.17 courses a block outside the ring;
            # crown 9 over a half-width of about 8 is 1.13 inside it — the two agree.
            {"id": "knoll", "ring": lobe(-34, -118, 22, 8, 9, 0.2, 17),
             "amount": 14, "falloff": 12, "crown": 9, "roughness": 3, "seed": 9},
        ],
    }
}

# ---------------------------------------------------------------- dressing
props = []
# The lane along the holm, and the two headland tracks that link the flights on each terrace.
props.append({"id": "holm-lane", "kind": "stroke", "claimsGround": True, "radius": 3, "seed": 4,
              "style": "worn", "coverage": 0.85,
              "points": [[-50, -8], [-20, -14], [10, -10], [40, -16], [50, -10]], "pave": GRAVEL})
for i, (pts, seed) in enumerate([
        ([[-32, -27], [-4, -30], [20, -26]], 21),
        ([[24, -43], [0, -46], [-12, -42]], 22),
        ([[-38, -59], [-6, -62], [32, -58]], 23)]):
    props.append({"id": f"headland-{i}", "kind": "stroke", "claimsGround": True, "radius": 2,
                  "seed": seed, "style": "worn", "coverage": 0.7, "points": pts, "pave": COARSE})

props.append({"id": "steading", "kind": "house", "seed": 401, "front": "posZ",
              "wings": [{"corners": [[18, -98], [30, -88]]}], "style": STEADING})
props.append({"id": "byre", "kind": "house", "seed": 402, "front": "posZ",
              "wings": [{"corners": [[-46, -80], [-37, -73]]}], "style": BYRE})

# Field clearance: the stone taken off the lynchets, heaped at the ends of them.
for i, (x, z, size) in enumerate([(-48, -30, 5), (46, -34, 4), (-48, -62, 5), (46, -66, 4),
                                  (-49, -46, 4), (47, -50, 5)]):
    props.append({"id": f"clearance-{i}", "kind": "boulder", "seed": 220 + i, "x": x, "z": z,
                  "form": "round", "size": size, "mossy": True,
                  "rock": {"kind": "noise", "seed": 61 + i, "scale": 3, "octaves": 3, "rise": 2,
                           "stops": [COBBLE, STONE, MOSSCOB]}})
# A hanger of oak along the rough west end, where the plough never went.
for i, (x, z, h) in enumerate([(-49, -24, 11), (-47, -38, 13), (-50, -52, 12), (-48, -70, 11),
                               (48, -28, 12), (50, -44, 11), (47, -58, 13), (49, -74, 12),
                               (-30, -101, 12), (44, -100, 11)]):
    props.append({"id": f"hanger-{i}", "kind": "tree", "seed": 1800 + i, "form": "template",
                  "species": "oak", "x": x, "z": z, "height": h})
props.append({"id": "pasture-cover", "kind": "flora",
              "points": [[-50, -102], [50, -102], [50, -22], [-50, -22]],
              "spec": {"coverage": 0.5, "scale": 16, "octaves": 3, "fernShare": 0.1,
                       "flowerShare": 0.12, "flowerScale": 11, "tallShare": 0.35}})

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"grown": GROWN, "lynchet": LYNCHET, "lynchet-tint": LYNCHET_TINT},
    "mapTheme": "grown",
    "biome": {"kind": "solid", "id": 1},     # Plains: #91bd59, bright pasture green
    "addShapes": shapes + flights,
    "relief": relief,
    "roomStyles": {"spawn": STEADING},
    "dressing": {"props": props},
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
    json.dump(plan, handle, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
    json.dump(finish, handle, indent=1)
print(f"{SLUG}: {len(plan['pieces'])} pieces, {len(shapes)} terraces, {len(flights)} flights, "
      f"{len(relief['*']['marks'])} marks, {len(props)} props")
