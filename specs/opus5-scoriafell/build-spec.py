#!/usr/bin/env python3
"""Scoriafell — one mountain between two valleys, and the pass over it is the whole map.

A mountain is a push; no mark can be one. A relief mark is a constraint honoured exactly, so a point
mark at height builds a drum and a line of them builds a row of oil drums. The landform here is two
pushes and nothing else:

  fell   a long east-west ribbon whose ring is its own rot_180 image, so the fan draws it onto
         itself rather than beside itself. Its two gradients are made to agree: outside the ring the
         ground climbs at amount / falloff, inside it at crown / half, and where they disagree the
         range has a step at its own outline — a cliff with a hill on top. Both are near 1.7.
  notch  a negative push crossing the ridge, which dishes rather than domes: the pass.

Only ground a player walks is pinned — the two dale floors, the pass floor, the spawn aprons. The
flanks carry no mark at all, because a board with a mark on every region is a table with bumps on
it. reach 0 goes with that.

Writes <slug>.plan.json and <slug>.finish.json beside itself.
"""
import json, math, os, random

SLUG = "opus5-scoriafell"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- blocks
#   GROUND  volcanic — ash grey, scoria, and a genuinely black note on the crags.
#   BUILT   dark timber on nether-brick footings. Never the ground's family.
#   ACCENT  ember — netherrack, in one thin bed in the strata and one patch by the pass.
GRAVEL     = {"kind": "solid", "id": 13,  "data": 0}
STONE      = {"kind": "solid", "id": 1,   "data": 0}
ANDESITE   = {"kind": "solid", "id": 1,   "data": 5}
POLANDES   = {"kind": "solid", "id": 1,   "data": 6}
COBBLE     = {"kind": "solid", "id": 4,   "data": 0}
COALBLOCK  = {"kind": "solid", "id": 173, "data": 0}
BLACKCLAY  = {"kind": "solid", "id": 159, "data": 15}
GREYCLAY   = {"kind": "solid", "id": 159, "data": 7}
SILVERCLAY = {"kind": "solid", "id": 159, "data": 8}
NETHERBRK  = {"kind": "solid", "id": 112, "data": 0}
NETHERRACK = {"kind": "solid", "id": 87,  "data": 0}
ORANGECLAY = {"kind": "solid", "id": 159, "data": 1}
DARKOAK    = {"kind": "solid", "id": 5,   "data": 5}
DARKOAKLOG = {"kind": "solid", "id": 162, "data": 1}
STONEBRICK = {"kind": "solid", "id": 98,  "data": 0}

def depth_stack(bands, beyond=None, ending="handOver"):
    out = {"kind": "layered", "axis": "depth",
           "stack": {"ending": ending,
                     "bands": [{"material": m, "thickness": t} for m, t in bands]}}
    if beyond:
        out["beyond"] = beyond
    return out

def slope_stack(bands, beyond=None):
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

def paired(half):
    """A ring that is its own rot_180 image: half its points, then their negations in the same
    order, so vertex i and vertex i + n/2 are the pair the fan maps onto each other."""
    ring = half + [[-x, -z] for x, z in half]
    assert sorted(ring) == sorted([[-x, -z] for x, z in ring])
    return ring

VALLEY = 22

# ---------------------------------------------------------------- the plan
CELL = 4
plan = {
    "plan": 2,
    "meta": {"name": "Scoriafell"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20, "surface": VALLEY},
    "pieces": [
        {"id": "head",  "role": "piece", "rect": [-13, -26, 26, 5]},   # x -52..51  z -104..-85
        {"id": "camp",  "role": "spawn", "rect": [-3, -25, 5, 4]},     # x -12..7   z -100..-85
        {"id": "dale",  "role": "piece", "rect": [-13, -21, 26, 8]},   #            z  -84..-53
        {"id": "flank", "role": "piece", "rect": [-13, -13, 26, 8]},   #            z  -52..-21
        # The pass is a piece of its own with a shoulder either side, which is both the arrangement
        # and the junction that keeps the crest from reading as one corridor end to end.
        {"id": "pass",    "role": "piece", "rect": [-4, -5, 8, 5]},    # x -16..15  z  -20..-1
        {"id": "scree-w", "role": "piece", "rect": [-13, -5, 9, 5]},   # x -52..-17
        {"id": "scree-e", "role": "piece", "rect": [4, -5, 9, 5]},     # x  16..51
    ],
    "zones": [{"id": "saddle", "rect": [-13, -5, 26, 10]}],            # x -52..51  z -20..19
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 8], "facing": "back",
                    "footprint": [2, 2, 16, 12]}],
        # World (-30, -58), on the north dale floor: 44 from its own spawn and 152 from the
        # enemy's. The fell crosses the whole board, so the pass is the only way to reach it.
        "destroyables": [{"id": "scoria-stone", "at": [-30, -58],
                          "style": "cube-4", "materials": "coal block", "float": 4,
                          "name": "The Scoria Stone"}],
    },
}

# ---------------------------------------------------------------- the landform
# The fell's ribbon. amounts is one lift per ring vertex, wrapped along the arc, so the crest falls
# the way the ring was drawn; the two vertices nearest x = 0 carry less, which is the saddle the
# pass is cut through. Vertex i pairs with i + 6, so the dip is symmetric by construction.
FELL_HALF = [[-58, -11], [-32, -13], [-6, -10], [20, -12], [46, -10], [60, -5]]
FELL_RING = paired(FELL_HALF)
FELL_AMOUNTS = [26, 25, 19, 24, 26, 25, 26, 25, 19, 24, 26, 25]
assert all(FELL_AMOUNTS[i] == FELL_AMOUNTS[(i + 6) % 12] for i in range(12))

# The pass, as a push that dishes instead of doming. A negative amount lowers and a negative crown
# hollows the middle of the ring, which is a defile rather than a col.
NOTCH_HALF = [[-15, -30], [-9, -14], [-14, -2]]
NOTCH_RING = paired(NOTCH_HALF)

relief = {
    "*": {
        "base": VALLEY,
        "reach": 0,          # a finite reach pulls the flanks back to base and the range becomes hills
        "step": 1,
        "grain": {"amplitude": 2.1, "scale": 26, "seed": 11},
        "marks": [
            {"id": "apron", "kind": "area", "h": 24, "bevel": 3,
             "ring": lobe(-2, -92, 30, 10, 9, 0.15, 3)},
            {"id": "roompad", "kind": "area", "h": 24,
             "ring": [[-20, -104], [15, -104], [15, -80], [-20, -80]]},
            {"id": "dale-floor", "kind": "area", "h": VALLEY, "bevel": 5,
             "ring": lobe(0, -66, 46, 13, 11, 0.16, 4)},
            # The pass floor, pinned flat so the ground a player crosses on is not a ridge of grain.
            # It is a self-symmetric ring, so the fan lays it back over itself.
            {"id": "pass-floor", "kind": "area", "h": VALLEY,
             "ring": paired([[-13, -14], [-7, -17], [2, -15], [10, -9], [13, -2]])},
        ],
        "pushes": [
            # Outside the ring 26 over a falloff of 16 is 1.63 courses a block; inside, crown 18
            # over a half-width of about 11 is 1.64. The two agree, so the fell is one mountainside
            # from the dale to the crest instead of a cliff with a hill on top of it.
            {"id": "fell", "ring": FELL_RING, "amounts": FELL_AMOUNTS,
             "falloff": 16, "crown": 18, "roughness": 4, "seed": 13},
            # RL6 measured this pair at 1.2 against 0.6 and named the step it puts at the ring.
            # -13 over a falloff of 11 is 1.18 a block; a crown of -12 over a half-width of about
            # 10 is 1.20. The defile now meets the mountainside instead of stepping off it.
            {"id": "notch", "ring": NOTCH_RING,
             "amount": -13, "falloff": 11, "crown": -12, "roughness": 2, "seed": 19},
        ],
    }
}

# ---------------------------------------------------------------- themes
# Two blocks to a pattern, never a family; cells well above 6 across.
ASHMIX    = {"kind": "cell", "seed": 42, "cellSize": 14, "jitter": 3, "warp": 5, "rise": 6,
             "palette": [GRAVEL, SILVERCLAY]}
SCORIAMIX = {"kind": "cell", "seed": 43, "cellSize": 12, "jitter": 3, "warp": 4, "rise": 5,
             "palette": [COBBLE, ANDESITE]}
BLACKMIX  = {"kind": "cell", "seed": 41, "cellSize": 11, "jitter": 3, "warp": 4, "rise": 5,
             "palette": [COALBLOCK, BLACKCLAY]}
# One stack shared as the wall of every theme, so every crag on the board is the same rock in the
# same order — and the one warm bed on a board with no other warm note.
STRATA = depth_stack([(BLACKCLAY, 2), (ANDESITE, 3), (NETHERRACK, 1), (STONE, 4),
                      (COALBLOCK, 2), (POLANDES, 4)], beyond=STONE, ending="repeat")

SCORIA = theme(
    surface=slope_stack([(depth_stack([(ASHMIX, 1), (GRAVEL, 1), (STONE, 2)], beyond=STONE), 15),
                         (depth_stack([(SCORIAMIX, 2), (STONE, 2)], beyond=STONE), 21),
                         (depth_stack([(BLACKMIX, 2), (ANDESITE, 2)], beyond=STONE), 54)],
                        beyond=STONE),
    wall=STRATA, fill=STRATA, rim=BLACKCLAY)

ASHDALE = theme(
    surface=slope_stack([(depth_stack([(GRAVEL, 1), (ASHMIX, 1), (SILVERCLAY, 2)], beyond=STONE), 14),
                         (depth_stack([(ASHMIX, 2), (GRAVEL, 2)], beyond=STONE), 22),
                         (depth_stack([(SCORIAMIX, 2), (ANDESITE, 2)], beyond=STONE), 54)],
                        beyond=STONE),
    wall=STRATA,
    fill={"kind": "voronoi", "seed": 29, "cellSize": 18, "rise": 9,
          "bands": [{"material": COALBLOCK, "depth": 2}, {"material": ANDESITE, "depth": 1}]},
    rim=GRAVEL)

FUMAROLE = theme(
    surface=depth_stack([({"kind": "cell", "seed": 44, "cellSize": 9, "jitter": 2, "warp": 3,
                           "rise": 4, "palette": [NETHERRACK, ORANGECLAY]}, 1),
                         (NETHERRACK, 2)], beyond=STONE),
    wall=STRATA, fill=STRATA, rim=NETHERRACK)

# ---------------------------------------------------------------- the shell
def house_style(wall_mat, plate, roof_body, roof_form, post, storeys, slab, slab_data,
                verge_log=(162, 1), beams=False, window_block=126, window_data=5, head_block=164):
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

LODGE = house_style(wall_mat=[(DARKOAK, 3), (NETHERBRK, 1)], plate=NETHERBRK, roof_body=DARKOAK,
                    roof_form="gable", post=DARKOAKLOG,
                    storeys=[(5, [(DARKOAK, 3), (STONEBRICK, 1)]), (4, [(DARKOAK, 4)])],
                    slab=126, slab_data=5, beams=True)
WATCH = house_style(wall_mat=[(NETHERBRK, 3), (DARKOAK, 2)], plate=NETHERBRK, roof_body=DARKOAK,
                    roof_form="hip", post=DARKOAKLOG, storeys=[], slab=126, slab_data=5, beams=True)

# ---------------------------------------------------------------- authored shapes
# The dale floors and the one ember patch, each a standing shape so it owns its columns: an add
# with no height_mode is a one-course thing at bedrock and never wins the cell, so it paints
# nothing and nothing says so. Each sits on ground that is pinned flat, because a raise reads the
# median under its own footprint and across a slope comes out a plate.
add_shapes = [
    {"id": "dale-n", "type": "polygon", "operation": "add", "floor": 0, "base_height": 0,
     "height_mode": "raise", "skirt": 0,
     "vertices": lobe(0, -66, 45, 12, 11, 0.14, 51), "theme": "ashdale"},
    {"id": "fumarole", "type": "polygon", "operation": "add", "floor": 0, "base_height": 0,
     "height_mode": "raise", "skirt": 0,
     "vertices": lobe(-9, -9, 7, 6, 9, 0.2, 52), "theme": "fumarole"},
]

# ---------------------------------------------------------------- dressing
props = []
# The track over the pass, one each side, meeting in the defile.
props.append({"id": "pass-track", "kind": "stroke", "claimsGround": True, "radius": 3, "seed": 6,
              "style": "worn", "coverage": 0.8,
              "points": [[-6, -76], [-2, -56], [4, -36], [0, -16], [-4, 0]], "pave": GRAVEL})
props.append({"id": "dale-track", "kind": "stroke", "claimsGround": True, "radius": 2, "seed": 7,
              "style": "worn", "coverage": 0.7,
              "points": [[-38, -62], [-14, -70], [10, -66], [34, -72]], "pave": ANDESITE})

props.append({"id": "lodge", "kind": "house", "seed": 501, "front": "posZ",
              "wings": [{"corners": [[20, -98], [32, -88]]}], "style": LODGE})
props.append({"id": "watch", "kind": "house", "seed": 502, "front": "posZ",
              "wings": [{"corners": [[38, -88], [46, -80]]}], "style": WATCH})

# Bombs and blocks down the flanks — angular, dark, and off the track.
for i, (x, z, size) in enumerate([(-44, -40, 6), (-24, -34, 5), (22, -38, 6), (44, -44, 5),
                                  (-46, -22, 5), (30, -24, 6), (-30, -14, 4), (36, -10, 5),
                                  (-20, -78, 4), (30, -60, 5)]):
    props.append({"id": f"bomb-{i}", "kind": "boulder", "seed": 300 + i, "x": x, "z": z,
                  "form": "angular", "size": size, "mossy": False,
                  "rock": {"kind": "noise", "seed": 71 + i, "scale": 4, "octaves": 3, "rise": 3,
                           "stops": [ANDESITE, COALBLOCK, COBBLE]}})
# Spruce holds on the dale floors only; nothing grows on the fell.
for i, (x, z, h) in enumerate([(-44, -74, 12), (-46, -78, 14), (-24, -80, 11), (14, -76, 13),
                               (24, -84, 12), (42, -70, 11), (-46, -58, 13), (46, -58, 12),
                               (-30, -96, 11), (16, -90, 12)]):
    props.append({"id": f"holt-{i}", "kind": "tree", "seed": 1900 + i, "form": "template",
                  "species": "spruce", "x": x, "z": z, "height": h})

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"scoria": SCORIA, "ashdale": ASHDALE, "fumarole": FUMAROLE},
    "mapTheme": "scoria",
    "biome": {"kind": "solid", "id": 3},     # Extreme hills: a muted sage, the only green allowed
    "addShapes": add_shapes,
    "relief": relief,
    "roomStyles": {"spawn": LODGE},
    "dressing": {"props": props},
    # Capture is driven from the finish: the compiled intent carries no symmetry, so every point is
    # stated already fanned. A centre point plus one side would be a two-hill board.
    "controlPoints": [
        {"name": "The Scoria Pass", "anchor": {"x": -2, "y": 0, "z": 0}, "size": 9, "points": 2},
        {"name": "North Dale", "anchor": {"x": -34, "y": 0, "z": -64}, "size": 8, "points": 1},
        {"name": "South Dale", "anchor": {"x": 34, "y": 0, "z": 64}, "size": 8, "points": 1},
    ],
    "scoreLimit": 750,
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
    json.dump(plan, handle, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
    json.dump(finish, handle, indent=1)
print(f"{SLUG}: {len(plan['pieces'])} pieces, {len(relief['*']['marks'])} marks, "
      f"{len(relief['*']['pushes'])} pushes, {len(add_shapes)} shapes, {len(props)} props, "
      f"{len(finish['controlPoints'])} points")
