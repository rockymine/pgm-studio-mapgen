#!/usr/bin/env python3
"""Braidwater Ford — a wide braided river, and the two sides meet at three fords and nowhere else.

Four instruments, each doing one job:

  push   two gentle valley sides, held well clear of the river. A push is added AFTER the marks
         solve, so a skirt that reaches a scarp grades that scarp — the carr push stops 28 blocks
         short of the lip, and the overlook knoll 5 blocks short, so the cut bank stays a cut bank.
  scarp  the cut bank itself. Which side the shelf lands on is the order the points are written in:
         the high band's normal is (-dz, dx), so a lip traced EAST TO WEST puts high to the north.
         Traced the other way the shelf lands in the river and the drop lands on the bank.
  line   the fords, as ramps across the channel — later marks win contested cells, so each ford
         cuts its own way through the lip the scarp laid.
  area   both banks of every ford, which is that instrument's own case: flat is the point where a
         crossing lands.

The channels are reaches BETWEEN the fords and never across one. A channel reads the surface top
and carves down from it, so a channel laid over a ford would cut the crossing to its own bed depth
and the ford would stop being wadeable.

Writes <slug>.plan.json and <slug>.finish.json beside itself.
"""
import json, math, os, random

SLUG = "opus5-braidwater-ford"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- blocks
#   GROUND  ochre and brown floodplain silt — dirt, coarse dirt, podzol, brown clay.
#   BUILT   pale birch on cobble footings, which is the one light thing on a brown board.
#   ACCENT  the shingle bars: pale gravel and sand between the braids.
GRASS      = {"kind": "solid", "id": 2,   "data": 0}
DIRT       = {"kind": "solid", "id": 3,   "data": 0}
COARSE     = {"kind": "solid", "id": 3,   "data": 1}
PODZOL     = {"kind": "solid", "id": 3,   "data": 2}
GRAVEL     = {"kind": "solid", "id": 13,  "data": 0}
SAND       = {"kind": "solid", "id": 12,  "data": 0}
CLAY       = {"kind": "solid", "id": 82,  "data": 0}
HARDCLAY   = {"kind": "solid", "id": 172, "data": 0}
BROWNCLAY  = {"kind": "solid", "id": 159, "data": 12}
STONE      = {"kind": "solid", "id": 1,   "data": 0}
ANDESITE   = {"kind": "solid", "id": 1,   "data": 5}
COBBLE     = {"kind": "solid", "id": 4,   "data": 0}
MOSSCOB    = {"kind": "solid", "id": 48,  "data": 0}
BIRCH      = {"kind": "solid", "id": 5,   "data": 2}
BIRCHLOG   = {"kind": "solid", "id": 17,  "data": 2}
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

HAUGH, WATERLINE, BARS = 22, 12, 13
TERRACE, APRON = 26, 28
FORDS = [-36, 0, 36]

# ---------------------------------------------------------------- the plan
CELL = 4
plan = {
    "plan": 2,
    "meta": {"name": "Braidwater Ford"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20, "surface": 20},
    "pieces": [
        {"id": "head",   "role": "piece", "rect": [-13, -28, 26, 5]},   # x -52..51  z -112..-93
        {"id": "camp",   "role": "spawn", "rect": [-3, -27, 5, 4]},     # x -12..7   z -108..-93
        {"id": "carr",   "role": "piece", "rect": [-13, -23, 26, 9]},   #            z  -92..-57
        {"id": "haugh",  "role": "piece", "rect": [-13, -14, 26, 10]},  #            z  -56..-17
        # The river band is three pieces, one to a ford, so the crossings are the arrangement and
        # the braid is a junction rather than one lane running the board's whole width.
        {"id": "braid-w", "role": "piece", "rect": [-13, -4, 9, 4]},    # x -52..-17 z  -16..-1
        {"id": "braid-c", "role": "piece", "rect": [-4, -4, 8, 4]},     # x -16..15
        {"id": "braid-e", "role": "piece", "rect": [4, -4, 9, 4]},      # x  16..51
    ],
    "zones": [{"id": "water", "rect": [-13, -5, 26, 10]}],              # x -52..51  z -20..19
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 8], "facing": "back",
                    "footprint": [2, 2, 16, 12]}],
        # World (-26, -58), on the carr behind the river: 48 from its own spawn and 159 from the
        # enemy's, which is what puts the crossing between an attacker and the goal.
        "destroyables": [{"id": "braidwater-stone", "at": [-26, -58],
                          "style": "cube-4", "materials": "ender stone", "float": 4,
                          "name": "The Braidwater Stone"}],
    },
}

# ---------------------------------------------------------------- the relief
def ford_line(x, reach, tread, seed):
    """A ford as a ramp across the channel: bank, shallows, bed, shallows, bank. It is stated after
    the scarp, so it wins the cells the lip would otherwise have walled."""
    rnd = random.Random(seed)
    return {"id": f"ford-{x}", "kind": "line", "r": reach, "tread": tread,
            "h": [HAUGH, BARS + 3, BARS, BARS + 3, HAUGH],
            "points": [[x + rnd.choice([-1, 0, 1]), z] for z in (-26, -13, 0, 13, 26)]}

relief = {
    "*": {
        "base": 20,
        "reach": 0,
        "step": 1,
        "grain": {"amplitude": 1.1, "scale": 17, "seed": 8},
        "marks": [
            {"id": "apron", "kind": "area", "h": APRON, "bevel": 3,
             "ring": lobe(-2, -100, 30, 10, 9, 0.15, 3)},
            {"id": "roompad", "kind": "area", "h": APRON,
             "ring": [[-20, -112], [15, -112], [15, -88], [-20, -88]]},
            {"id": "terrace", "kind": "area", "h": TERRACE,
             "ring": lobe(0, -74, 48, 15, 11, 0.15, 4)},
            {"id": "haugh-floor", "kind": "area", "h": HAUGH,
             "ring": lobe(0, -38, 48, 12, 11, 0.16, 5)},
            # The cut bank. Traced east to west, so the high band is north of the lip — the bank —
            # and the low band is the channel. Traced the other way the shelf lands in the river.
            # face 2 is a bank a player cannot walk up, which is what makes the fords the crossings.
            {"id": "lip-n", "kind": "scarp", "high": HAUGH, "low": BARS, "face": 2, "band": 4,
             "points": [[50, -17], [30, -19], [8, -16], [-14, -19], [-34, -16], [-50, -18]]},
            ford_line(FORDS[1], 11, 7, 21),     # the centre: wide, long, and overlooked
            ford_line(FORDS[0], 6, 3, 22),      # the west: narrow, covered — its image is the east
            ford_line(FORDS[2], 6, 3, 23),
            # Both banks of every ford. An area pins a flat disc and is right where flat is the
            # point, and the ground a crossing lands on is exactly that.
            {"id": "bank-c", "kind": "area", "h": HAUGH, "ring": lobe(0, -31, 14, 5, 9, 0.18, 31)},
            {"id": "bank-w", "kind": "area", "h": HAUGH, "ring": lobe(-36, -31, 9, 4, 9, 0.18, 32)},
            {"id": "bank-e", "kind": "area", "h": HAUGH, "ring": lobe(36, -31, 9, 4, 9, 0.18, 33)},
        ],
        "pushes": [
            # The valley side. Gentle, because the river is the subject: 8 over a falloff of 22 is
            # 0.36 courses a block, and crown 5 over a half-width of about 15 is 0.33. Its skirt
            # reaches z -46, twenty-eight blocks short of the lip at z -18.
            {"id": "side", "ring": lobe(0, -66, 46, 12, 9, 0.16, 41),
             "amount": 8, "falloff": 14, "crown": 7, "roughness": 3, "seed": 15},
            # The bluff that overlooks the centre ford. Its skirt reaches z -23, five blocks short
            # of the lip — near enough to loom over the crossing, far enough to leave it sharp.
            {"id": "bluff", "ring": lobe(-24, -44, 16, 9, 9, 0.2, 42),
             "amount": 9, "falloff": 12, "crown": 7, "roughness": 2, "seed": 16},
        ],
    }
}

# ---------------------------------------------------------------- themes
SILTMIX = {"kind": "cell", "seed": 51, "cellSize": 13, "jitter": 3, "warp": 5, "rise": 5,
           "palette": [COARSE, PODZOL]}
BARMIX  = {"kind": "cell", "seed": 52, "cellSize": 15, "jitter": 3, "warp": 5, "rise": 6,
           "palette": [GRAVEL, SAND]}
# A surfacing block is exactly one course thick and whatever is under it is soil (PT1), so grass and
# podzol go in the SAME top course as a two-block patchwork rather than one under the other.
CARRMIX = {"kind": "cell", "seed": 53, "cellSize": 12, "jitter": 3, "warp": 5, "rise": 4,
           "palette": [GRASS, PODZOL]}
# One stack shared by every cut on the board, so a bank anywhere shows the same beds: silt over
# clay over the gravel the river laid down.
STRATA = depth_stack([(BROWNCLAY, 2), (HARDCLAY, 3), (CLAY, 2), (GRAVEL, 3), (ANDESITE, 4)],
                     beyond=STONE, ending="repeat")

SILT = theme(
    surface=slope_stack([(depth_stack([(SILTMIX, 1), (DIRT, 2), (CLAY, 1)], beyond=GRAVEL), 14),
                         (depth_stack([(COARSE, 1), (BROWNCLAY, 2)], beyond=GRAVEL), 20),
                         (depth_stack([(HARDCLAY, 2), (BROWNCLAY, 2)], beyond=GRAVEL), 56)],
                        beyond=GRAVEL),
    wall=STRATA, fill=STRATA, rim=BROWNCLAY)

CARR = theme(
    surface=slope_stack([(depth_stack([(CARRMIX, 1), (DIRT, 3)], beyond=GRAVEL), 16),
                         (depth_stack([(SILTMIX, 1), (DIRT, 2)], beyond=GRAVEL), 20),
                         (depth_stack([(COARSE, 1), (BROWNCLAY, 2)], beyond=GRAVEL), 54)],
                        beyond=GRAVEL),
    wall=STRATA,
    fill={"kind": "voronoi", "seed": 37, "cellSize": 17, "rise": 9,
          "bands": [{"material": HARDCLAY, "depth": 2}, {"material": GRAVEL, "depth": 1}]},
    rim=PODZOL)

BAR = theme(
    surface=depth_stack([(BARMIX, 2), (GRAVEL, 2)], beyond=GRAVEL),
    wall=STRATA, fill=STRATA, rim=GRAVEL)

# ---------------------------------------------------------------- the shell
def house_style(wall_mat, plate, roof_body, roof_form, post, storeys, slab, slab_data,
                verge_log=(17, 2), beams=False, window_block=126, window_data=2, head_block=135):
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

STEADING = house_style(wall_mat=[(BIRCH, 3), (COBBLE, 1)], plate=COBBLE, roof_body=BIRCH,
                       roof_form="gable", post=BIRCHLOG,
                       storeys=[(5, [(BIRCH, 3), (STONEBRICK, 1)]), (4, [(BIRCH, 4)])],
                       slab=126, slab_data=2, beams=True)
FISHHUT = house_style(wall_mat=[(COBBLE, 3), (BIRCH, 2)], plate=MOSSCOB, roof_body=BIRCH,
                      roof_form="shed", post=BIRCHLOG, storeys=[], slab=126, slab_data=2,
                      beams=True)

# ---------------------------------------------------------------- authored shapes
# The shingle bars, as standing shapes so they own their columns. Each sits on the flat river bed,
# because a raise reads the median ground under its own footprint and across a slope reads as a
# plate. The carr is the wooded terrace behind the haugh.
add_shapes = [
    {"id": "carr-n", "type": "polygon", "operation": "add", "floor": 0, "base_height": 0,
     "height_mode": "raise", "skirt": 0,
     "vertices": lobe(0, -74, 47, 14, 11, 0.13, 61), "theme": "carr"},
]
for i, (bx, bz, rx, rz) in enumerate([(-22, -9, 11, 5), (18, -6, 12, 5), (-46, -8, 6, 4)]):
    add_shapes.append({"id": f"bar-{i}", "type": "polygon", "operation": "add", "floor": 0,
                       "base_height": 1, "height_mode": "raise", "skirt": 1,
                       "vertices": lobe(bx, bz, rx, rz, 9, 0.22, 70 + i), "theme": "bar"})

# ---------------------------------------------------------------- dressing
props = []
# The braids, as reaches BETWEEN the fords. Water is the one prop that changes the ground, so a
# channel laid across a crossing would carve the crossing.
BRAIDS = [("braid-a", [[-30, -13], [-24, -10], [-16, -12], [-8, -9]], 5, 3),
          ("braid-b", [[-30, 3], [-22, 6], [-14, 4], [-8, 7]], 4, 2),
          ("braid-c", [[-50, -14], [-46, -10], [-42, -6]], 5, 3),
          ("braid-d", [[10, -8], [18, -11], [26, -8], [30, -12]], 4, 2)]
for name, pts, radius, depth in BRAIDS:
    props.append({"id": name, "kind": "water", "seed": 60 + len(props), "shape": "channel",
                  "points": pts, "radius": radius, "depth": depth, "level": WATERLINE,
                  "form": "natural", "edge": 0.6, "shore": 1, "shoreWander": False,
                  "bank": {"kind": "cell", "seed": 55, "cellSize": 11, "jitter": 2, "warp": 4,
                           "rise": 4, "palette": [GRAVEL, SAND]}})

# The track down to each ford, so the crossings read as used.
for i, x in enumerate(FORDS):
    props.append({"id": f"ford-track-{i}", "kind": "stroke", "claimsGround": True, "radius": 2,
                  "seed": 80 + i, "style": "worn", "coverage": 0.8,
                  "points": [[x - 4, -56], [x, -40], [x + 2, -28]], "pave": GRAVEL})

props.append({"id": "steading", "kind": "house", "seed": 601, "front": "posZ",
              "wings": [{"corners": [[20, -104], [32, -94]]}], "style": STEADING})
props.append({"id": "fish-hut", "kind": "house", "seed": 602, "front": "posZ",
              "wings": [{"corners": [[16, -70], [24, -63]]}], "style": FISHHUT})

for i, (x, z, size) in enumerate([(-44, -48, 5), (12, -46, 4), (44, -40, 5), (-10, -60, 4),
                                  (30, -78, 5), (-46, -66, 4)]):
    props.append({"id": f"erratic-{i}", "kind": "boulder", "seed": 400 + i, "x": x, "z": z,
                  "form": "round", "size": size, "mossy": True,
                  "rock": {"kind": "noise", "seed": 81 + i, "scale": 3, "octaves": 3, "rise": 2,
                           "stops": [COBBLE, ANDESITE, MOSSCOB]}})
# Alder on the west ford's north bank only. Under rot_180 its image lands on the EAST ford's south
# bank, so a player crossing west enters cover and leaves open, and crossing east does the reverse:
# two crossings out of one authored shape that are not the same way round drawn twice.
for i, (x, z, h) in enumerate([(-46, -26, 11), (-44, -30, 12), (-28, -22, 10), (-28, -31, 11),
                               (-48, -34, 12), (-26, -38, 10)]):
    props.append({"id": f"alder-{i}", "kind": "tree", "seed": 2000 + i, "form": "template",
                  "species": "oak", "x": x, "z": z, "height": h})
# Birch on the carr, well back from the river.
for i, (x, z, h) in enumerate([(-46, -80, 13), (-30, -86, 12), (-14, -78, 14), (12, -78, 12),
                               (20, -86, 13), (44, -86, 12), (-40, -64, 11), (40, -62, 12)]):
    props.append({"id": f"carr-tree-{i}", "kind": "tree", "seed": 2100 + i, "form": "template",
                  "species": "birch", "x": x, "z": z, "height": h})
props.append({"id": "carr-cover", "kind": "flora",
              "points": [[-50, -92], [50, -92], [50, -58], [-50, -58]],
              "spec": {"coverage": 0.45, "scale": 15, "octaves": 3, "fernShare": 0.3,
                       "flowerShare": 0.05, "flowerScale": 9, "tallShare": 0.4}})

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"silt": SILT, "carr": CARR, "bar": BAR},
    "mapTheme": "silt",
    # Swampland: grass #6a7039. A tinted block's family is the biome's to decide, and podzol against
    # Plains grass reads as neither ground — against this one the pair is a damp leaf-littered floor.
    "biome": {"kind": "solid", "id": 6},
    "addShapes": add_shapes,
    "relief": relief,
    "roomStyles": {"spawn": STEADING},
    "dressing": {"props": props},
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
    json.dump(plan, handle, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
    json.dump(finish, handle, indent=1)
print(f"{SLUG}: {len(plan['pieces'])} pieces, {len(relief['*']['marks'])} marks, "
      f"{len(relief['*']['pushes'])} pushes, {len(add_shapes)} shapes, {len(props)} props")
