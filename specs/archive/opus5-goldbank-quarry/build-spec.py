#!/usr/bin/env python3
"""Goldbank Quarry — ground that people cut away.

The whole board is one worked limestone quarry and both destroyables stand on the floor of it,
under everybody. Five relief instruments carry five different jobs, which is the point of the run:

  push    the unworked fell behind each spawn, its spine set past the coast so the crest is off-map
  area    the rim, the two working benches and the spawn apron — only ground a player walks
  step 3  + stairs, which terraces the graded faces between those marks into quarry benches
  line    the haul road, with a tread and a batter in degrees, so it cuts a bank as it climbs
  sink    the deep cut: skirt 1, notched rather than tilted, so it is sheer but for one ramp a side

Writes <slug>.plan.json and <slug>.finish.json beside itself.
"""
import json, math, os, random

SLUG = "opus5-goldbank-quarry"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- blocks
# Three tone families, named before anything is painted.
#   GROUND  pale gold oolitic limestone — buff sandstone, end stone, sand. Warm, never grey.
#   BUILT   the quarry plant — spruce timber, iron, stone brick. Dark against the ground.
#   ACCENT  rust — hardened clay and orange stained clay, one thin bed and the plant's ironwork.
GRASS       = {"kind": "solid", "id": 2,   "data": 0}
DIRT        = {"kind": "solid", "id": 3,   "data": 0}
COARSE      = {"kind": "solid", "id": 3,   "data": 1}
SANDSTONE   = {"kind": "solid", "id": 24,  "data": 0}
CHISELLED   = {"kind": "solid", "id": 24,  "data": 1}
SMOOTH      = {"kind": "solid", "id": 24,  "data": 2}
ENDSTONE    = {"kind": "solid", "id": 121, "data": 0}
SAND        = {"kind": "solid", "id": 12,  "data": 0}
GRAVEL      = {"kind": "solid", "id": 13,  "data": 0}
RUST        = {"kind": "solid", "id": 172, "data": 0}
ORANGE      = {"kind": "solid", "id": 159, "data": 1}
SANDSLAB    = {"kind": "solid", "id": 43,  "data": 1}
SPRUCE      = {"kind": "solid", "id": 5,   "data": 1}
SPRUCELOG   = {"kind": "solid", "id": 17,  "data": 1}
IRON        = {"kind": "solid", "id": 42,  "data": 0}
BRICKS      = {"kind": "solid", "id": 98,  "data": 0}
MOSSYBRICK  = {"kind": "solid", "id": 98,  "data": 1}
COBBLE      = {"kind": "solid", "id": 4,   "data": 0}

# ---------------------------------------------------------------- material helpers
def depth_stack(bands, beyond=None, ending="handOver"):
    """A band stack read down from the top of its bucket."""
    out = {"kind": "layered", "axis": "depth",
           "stack": {"ending": ending,
                     "bands": [{"material": m, "thickness": t} for m, t in bands]}}
    if beyond:
        out["beyond"] = beyond
    return out

def slope_stack(bands, beyond=None):
    """A band stack whose thicknesses are spans of DEGREES — the flat, the shoulder and the face
    of one hill finished by one material."""
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
    """An area mark's ring is a shape: a rectangle builds a literal square mesa, so every ring
    here is a nine-to-eleven point lobed outline."""
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1.0 + wobble * (rnd.random() - 0.5)
        pts.append([round(cx + rx * k * math.cos(a)), round(cz + rz * k * math.sin(a))])
    return pts

# ---------------------------------------------------------------- the plan
# One surface for every piece. The plan states the board's ARRANGEMENT — a fell behind, a rim,
# an approach, a pit floor — and the relief states every height on it. A piece cut so a theme has
# somewhere to hang is the failure this avoids.
CELL = 4
plan = {
    "plan": 2,
    "meta": {"name": "Goldbank Quarry"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20, "surface": 32},
    "pieces": [
        {"id": "fell",  "role": "piece", "rect": [-13, -28, 26, 5]},   # x -52..51  z -112..-93
        {"id": "brow",  "role": "piece", "rect": [-13, -23, 26, 5]},   #            z  -92..-73
        {"id": "camp",  "role": "spawn", "rect": [-3, -23, 5, 4]},     # x -12..7   z  -92..-77
        {"id": "brink", "role": "piece", "rect": [-13, -18, 26, 4]},   #            z  -72..-57
        {"id": "floor", "role": "piece", "rect": [-13, -14, 26, 9]},   #            z  -56..-21
        # The cut narrows at its waist: a neck of floor with an unquarried shelf either side. The
        # junction is the arrangement's, not a decoration — a lane that runs the board's whole
        # length without one is LN2's complaint and a corridor to play in.
        {"id": "waist",   "role": "piece", "rect": [-8, -5, 16, 5]},    # x -32..31  z  -20..-1
        {"id": "shelf-w", "role": "piece", "rect": [-13, -5, 5, 5]},    # x -52..-33
        {"id": "shelf-e", "role": "piece", "rect": [8, -5, 5, 5]},      # x  32..51
    ],
    "zones": [{"id": "pit", "rect": [-13, -7, 26, 14]}],               # x -52..51  z  -28..27
    "placements": {
        # The shell is 16x12 on a 20x16 piece: ST9 caps a building at 20x20 and ST10 a spawn
        # region at 20x30, and a piece with no footprint stamps itself inset one block.
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 8], "facing": "back",
                    "footprint": [2, 2, 16, 12]}],
        # Placed by absolute board position rather than on a piece, because what this stands on is
        # the sunk floor of an authored shape and not the flat rectangle the plan states. World
        # (-32, -49): eleven blocks inside the pit's north-west lobe, 43 from its own spawn and 145
        # from the enemy's.
        "destroyables": [{"id": "goldbank-stone", "at": [-32, -49],
                          "style": "cube-4", "materials": "ender stone", "float": 4,
                          "name": "The Goldbank Stone"}],
    },
}

# ---------------------------------------------------------------- the pit
# A self-symmetric ring: half its points plus their negations, so the symmetry fan draws it onto
# itself rather than beside itself. anchor_heights on a sink state DEPTH per vertex, and the two
# notches are indices 3,4 and their images 9,10 — one shallow ramp in on each team's side.
PIT_HALF = [[-50, -22], [-44, -60], [-20, -52], [0, -44], [24, -40], [46, -22]]
PIT_RING = PIT_HALF + [[-x, -z] for x, z in PIT_HALF]
PIT_DEPTH = [10, 10, 1, 1, 10, 10, 10, 10, 1, 1, 10, 10]
assert all(PIT_DEPTH[i] == PIT_DEPTH[(i + 6) % 12] for i in range(12))
assert sorted(PIT_RING) == sorted([[-x, -z] for x, z in PIT_RING])

# ---------------------------------------------------------------- themes
# The strata one stack, shared by every cut on the board, so each bench face shows the same beds
# in the same order. It goes in wall AND fill: a stack stated in surface alone bands the top four
# courses and leaves the face plain, and the face is the whole point of a quarry.
STRATA = depth_stack([(ENDSTONE, 2), (SANDSTONE, 3), (RUST, 1), (SMOOTH, 4), (SANDSTONE, 5)],
                     beyond=SANDSTONE, ending="repeat")

GOLDMOOR = theme(
    # 0-20 deg the fell's turf; 20-38 the soil it wears through to; 38+ the limestone under it.
    surface=slope_stack([(depth_stack([(GRASS, 1), (DIRT, 2)], beyond=SANDSTONE), 18),
                         (depth_stack([(COARSE, 1), (DIRT, 1), (SANDSTONE, 2)], beyond=SANDSTONE), 24),
                         (depth_stack([(SANDSTONE, 2), (ENDSTONE, 2)], beyond=SANDSTONE), 48)],
                        beyond=SANDSTONE),
    wall=STRATA,
    fill={"kind": "voronoi", "seed": 19, "cellSize": 17, "rise": 9,
          "bands": [{"material": ENDSTONE, "depth": 2}, {"material": SANDSTONE, "depth": 1}]},
    rim=SANDSTONE, depth=3, rim_edges="void", wall_on_faces=True)

QUARRYFACE = theme(
    # Worked ground: no turf at any angle. The flat is swept rock, the bench faces are sawn.
    surface=slope_stack([(depth_stack([(SANDSTONE, 1), (ENDSTONE, 1), (SANDSTONE, 2)], beyond=SANDSTONE), 14),
                         (depth_stack([(GRAVEL, 1), (SANDSTONE, 2)], beyond=SANDSTONE), 22),
                         (depth_stack([(SMOOTH, 2), (SANDSTONE, 2)], beyond=SANDSTONE), 54)],
                        beyond=SANDSTONE),
    # wallRun stands vertical: a sawn face is scored, where a weathered one is bedded.
    wall={"kind": "wallDiagonal", "slope": 3,
          "runs": [{"material": SMOOTH, "width": 4},
                   {"material": SANDSTONE, "width": 2},
                   {"material": CHISELLED, "width": 1}]},
    fill=STRATA, rim=SANDSTONE, depth=3, rim_edges="void", wall_on_faces=True)

QUARRYPIT = theme(
    # The deep cut. Its floor is the rubble the last blast left; its faces carry the whole bed.
    surface=slope_stack([(depth_stack([(SAND, 1), (GRAVEL, 1), (SANDSTONE, 2)], beyond=SANDSTONE), 12),
                         (depth_stack([(GRAVEL, 2), (SANDSTONE, 2)], beyond=SANDSTONE), 20),
                         (depth_stack([(ENDSTONE, 2), (SMOOTH, 3)], beyond=SANDSTONE), 58)],
                        beyond=SANDSTONE),
    wall=STRATA, fill=STRATA, rim=ENDSTONE, depth=3, rim_edges="void", wall_on_faces=True)

# ---------------------------------------------------------------- the shell the spawn is stamped in
def house_style(wall_mat, plate, roof_body, roof_form, post, storeys, slab, slab_data,
                verge_log=(17, 1), beams=False, window_block=126, window_data=1,
                head_block=134):
    """A HouseStyle the studio will take. Three things it refuses and this settles:
    a roof's verge may not be a bare log (HS3) — it is a laid log, which takes the axis the ridge
    is going; the half-course slab continues the body in the body's own material (HS3); and beams
    only come out of a course that is itself a laid log (HS9), so they are opt-in here."""
    top_course = {"kind": "laidLog", "id": verge_log[0], "data": verge_log[1]}
    def storey(clear, wall):
        bands = [{"material": m, "thickness": t} for m, t in wall]
        if beams:
            bands.append({"material": top_course, "thickness": 1})
        return {"clear": clear,
                "wall": {"stack": {"bands": bands, "ending": "repeat"}, "extent": clear},
                "post": post,
                "windows": {"form": "slabBanded", "block": window_block, "hostBlock": -1,
                            "hostData": 0, "data": window_data, "sill": 2, "width": 2,
                            "height": 2, "spacing": 4},
                "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                            "inlayInset": 2, "isPlain": True},
                "deck": None, "headroom": clear}
    wall_bands = [{"material": m, "thickness": t} for m, t in wall_mat]
    if beams:
        wall_bands.append({"material": top_course, "thickness": 1})
    return {
        "foundation": {"plate": {"stack": {"bands": [{"material": plate, "thickness": 1}],
                                           "ending": "repeat"}, "extent": 2},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": roof_form, "pitch": 1, "slab": slab, "slabData": slab_data, "overhang": 1,
                 "ridgeCap": True, "hole": False, "body": roof_body, "verge": top_course,
                 "gable": roof_body,
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                                  "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2,
                                  "spacing": 3}},
        "wall": {"stack": {"bands": wall_bands, "ending": "repeat"}, "extent": 5},
        "post": post,
        "windows": {"form": "slabBanded", "block": window_block, "hostBlock": -1, "hostData": 0,
                    "data": window_data, "sill": 2, "width": 2, "height": 2, "spacing": 4},
        "storeys": [storey(c, w) for c, w in storeys],
        "porch": None, "front": None,
        "beams": ({"block": verge_log[0], "data": verge_log[1], "reach": 1, "any": False}
                  if beams else {"block": -1, "data": 0, "reach": 1, "any": False}),
        # HS4: the head's corners and the line between them are one head, so the stair block
        # and the slab that fills it are cut from the same material — spruce stairs over a
        # spruce slab, never stone brick stairs over a wooden one.
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": head_block, "fill": "upperSlab",
                             "fillBlock": slab, "fillData": slab_data},
                    "width": 3, "height": 4},
    }

# The plant is timber and iron on a stone-brick footing — never the ground's own family.
# Spruce roof, spruce half-course (126:1 is the spruce slab), laid-log verge and beams.
PLANT_SHELL = house_style(
    wall_mat=[(SPRUCE, 3), (IRON, 1)], plate=BRICKS, roof_body=SPRUCE, roof_form="gable",
    post=SPRUCELOG, storeys=[(5, [(SPRUCE, 3), (RUST, 1)]), (4, [(SPRUCE, 4)])],
    slab=126, slab_data=1, beams=True)
SHED_SHELL = house_style(
    wall_mat=[(SPRUCE, 4), (RUST, 1)], plate=BRICKS, roof_body=SPRUCE, roof_form="shed",
    post=SPRUCELOG, storeys=[], slab=126, slab_data=1, beams=True)

# ---------------------------------------------------------------- the relief
# Marks go on team 0's half only: the fanned group mirrors them. Nothing is pinned that a player
# does not walk — the graded faces between the benches carry no mark at all, which is where the
# step quantum gets to make the terracing.
relief = {
    "*": {
        "base": 32,
        "reach": 0,
        "step": 3,           # every stated level is 32 - 3k, or the quantum rounds it away
        "grain": {"amplitude": 1.4, "scale": 22, "seed": 7},
        "marks": [
            {"id": "apron", "kind": "area", "h": 32, "bevel": 3,
             "ring": lobe(-2, -84, 30, 12, 9, 0.16, 11)},
            # The hut's own pad, drawn wider than the hut on every side. A stamped shell fills the
            # column under its whole footprint and levels it at the footprint's highest, so where
            # a neighbouring cell sits below that floor what the building meets the world with is
            # a face of bedrock nobody drew (WX11). The apron's lobed ring left three cells of the
            # camp's west side outside it; this covers all four sides at the shell's own height.
            {"id": "roompad", "kind": "area", "h": 32,
             "ring": [[-20, -98], [15, -98], [15, -70], [-20, -70]]},
            {"id": "rim", "kind": "area", "h": 32,
             "ring": lobe(0, -77, 50, 4, 11, 0.12, 12)},
            {"id": "bench", "kind": "area", "h": 29,
             "ring": lobe(0, -67, 50, 3, 11, 0.14, 13)},
            {"id": "toe", "kind": "area", "h": 26,
             "ring": lobe(0, -61, 50, 2, 11, 0.14, 14)},
            # The haul road. A line mark pins every cell in its band exactly, so the tread is the
            # running surface and the batter cuts the bank either side of it at 34 degrees down to
            # whatever the benches put there.
            {"id": "haul", "kind": "line", "r": 9, "tread": 3, "batter": 34,
             "h": [26, 29, 32, 32],
             "points": [[-10, -52], [6, -60], [24, -68], [44, -76]]},
        ],
        "pushes": [
            # The unworked fell. Its ring sits past the coast at z -112, so what is on the board is
            # one uninterrupted climb and the crest reads as being behind the map. 16 over a
            # falloff of 20 is 0.80 courses a block outside the ring, and crown 10 over a half-width
            # of about 12 is 0.83 inside it: the two agree, so there is no step at the ring — and
            # 39 degrees keeps the fell under the slope stack's bare-rock cut, so it stays grassed.
            {"id": "fell", "ring": lobe(0, -124, 46, 12, 9, 0.18, 21),
             "amount": 16, "falloff": 20, "crown": 10, "roughness": 3, "seed": 5},
        ],
    }
}

# ---------------------------------------------------------------- authored shapes
# The pit, and the worked ground the benches are cut in. Neither states a height_mode except the
# pit: an add with none is ordinary ground and the relief is its height, so these repaint the
# bench band without moving a block of it.
add_shapes = [
    {"id": "pit", "type": "polygon", "operation": "add", "floor": 0, "base_height": 10,
     "height_mode": "sink", "skirt": 1, "vertices": PIT_RING, "anchor_heights": PIT_DEPTH,
     "theme": "quarrypit"},
    # The worked ground the benches are cut in, and the stripped patch on the brow where the
    # overburden came off. Each is a one-block sink: an add with no height_mode is the flat
    # one-block behaviour at y=0, which loses the column to the ground and so owns no theme
    # scope at all — the census reports a theme that painted nothing. A sink stands out of the
    # field, keeps its columns, and one block of cut is what stripped ground is.
    {"id": "cut-rim", "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
     "height_mode": "sink", "skirt": 1,
     "vertices": lobe(0, -77, 50, 4, 11, 0.10, 32), "theme": "quarryface"},
    {"id": "cut-bench", "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
     "height_mode": "sink", "skirt": 1,
     "vertices": lobe(0, -67, 50, 3, 11, 0.10, 33), "theme": "quarryface"},
    {"id": "cut-toe", "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
     "height_mode": "sink", "skirt": 1,
     "vertices": lobe(0, -61, 50, 2, 11, 0.10, 34), "theme": "quarryface"},
    {"id": "spoil-w", "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
     "height_mode": "sink", "skirt": 1,
     "vertices": lobe(-40, -76, 11, 4, 9, 0.22, 41), "theme": "quarrypit"},
    {"id": "strip-e", "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
     "height_mode": "sink", "skirt": 1,
     "vertices": lobe(34, -82, 15, 9, 9, 0.24, 42), "theme": "quarryface"},
]

# ---------------------------------------------------------------- dressing
props = []
# The haul road paved over the line mark that cut it, so the road reads as made ground.
props.append({"id": "haul-road", "kind": "stroke", "claimsGround": True, "radius": 3, "seed": 4,
              "style": "worn", "coverage": 0.92,
              "points": [[-12, -48], [4, -57], [24, -66], [44, -72], [46, -82]],
              "pave": GRAVEL})
# Two grass tongues over the brow's shoulder, so the turf breaks into the rock instead of stopping
# dead on the outline of a shape.
TURF = [([[-46, -96], [-36, -86], [-28, -78]], 61),
        ([[26, -98], [18, -88], [10, -80]], 62)]
for i, (pts, seed) in enumerate(TURF):
    props.append({"id": f"turf-{i}", "kind": "stroke", "claimsGround": False, "radius": 5,
                  "seed": seed, "style": "worn", "coverage": 0.45, "points": pts, "pave": GRASS})

# The plant: a winding house on the rim above the haul road, and a crusher shed on the brow.
props.append({"id": "winding-house", "kind": "house", "seed": 311, "front": "negZ",
              "wings": [{"corners": [[6, -84], [18, -74]]}], "style": PLANT_SHELL})
props.append({"id": "crusher-shed", "kind": "house", "seed": 312, "front": "posZ",
              "wings": [{"corners": [[-46, -82], [-36, -75]]}], "style": SHED_SHELL})

# Spoil: block on the benches and fallen stone across the pit floor.
BOULDERS = [(-40, -70, 5), (-28, -66, 4), (48, -60, 5), (18, -90, 3),
            (-46, -20, 6), (-24, -30, 4), (36, -34, 5), (20, -14, 4), (-8, -8, 5)]
for i, (x, z, size) in enumerate(BOULDERS):
    props.append({"id": f"spoil-{i}", "kind": "boulder", "seed": 150 + i, "x": x, "z": z,
                  "form": "angular", "size": size, "mossy": False,
                  "rock": {"kind": "noise", "seed": 51 + i, "scale": 4, "octaves": 3, "rise": 3,
                           "stops": [SANDSTONE, ENDSTONE, SMOOTH]}})
# Birch on the fell only — the quarry itself is bare, which is what makes it read as worked.
TREES = [(-46, -104, 11), (-34, -108, 13), (-18, -106, 12), (-24, -108, 11),
         (14, -108, 13), (30, -104, 12), (44, -108, 11), (48, -96, 12),
         (-48, -92, 10), (20, -94, 11)]
for i, (x, z, h) in enumerate(TREES):
    props.append({"id": f"fell-tree-{i}", "kind": "tree", "seed": 1700 + i, "form": "template",
                  "species": "birch", "x": x, "z": z, "height": h})
# Ground cover on the fell's turf, and nowhere else.
props.append({"id": "fell-cover", "kind": "flora",
              "points": [[-50, -112], [50, -112], [50, -90], [-50, -90]],
              "spec": {"coverage": 0.4, "scale": 14, "octaves": 3, "fernShare": 0.15,
                       "flowerShare": 0.06, "flowerScale": 9, "tallShare": 0.3}})

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"goldmoor": GOLDMOOR, "quarryface": QUARRYFACE, "quarrypit": QUARRYPIT},
    "mapTheme": "goldmoor",
    "biome": {"kind": "solid", "id": 35},   # Savanna: #bfb755 turf, warm against buff stone
    "addShapes": add_shapes,
    "relief": relief,
    "roomStyles": {"spawn": PLANT_SHELL},   # `wool`/`spawn` — `cage` is dropped in silence
    "dressing": {"props": props},
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
    json.dump(plan, handle, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
    json.dump(finish, handle, indent=1)
print(f"{SLUG}: {len(plan['pieces'])} pieces, {len(relief['*']['marks'])} marks, "
      f"{len(relief['*']['pushes'])} push, {len(add_shapes)} shapes, {len(props)} props")
