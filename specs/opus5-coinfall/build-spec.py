#!/usr/bin/env python3
"""Coinfall — a two-team CTW board whose blocks are bought.

Two camps face a neutral holm across a pair of twenty-block gaps. Each team's ground falls in three steps —
the camp and the long run at 20, the wool's plinth raised to 25 above it, the bank against the void dropped to
17 — and the only way back up from the bank is the two flights cut into the seam. What a player carries across
the gap is bought: a villager stands in each camp trading the kit's own wood for the gapple, the arrows, the
ladders and the iron bars a wool run needs.

The run is deliberately lopsided. It stops twenty-five blocks west of the camp, where it used to run out into
ground no journey passed, and reaches seventy blocks east to carry the plinth — so the wool sits at the far
end of a walk rather than beside the spawn.

    python3 specs/opus5-coinfall/build-spec.py
    tools/drive.py specs/opus5-coinfall "Coinfall" --out maps/opus5-coinfall --renders specs/opus5-coinfall/renders
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "opus5-coinfall"
CELL = 5

# ── the surfaces the board is cut at ────────────────────────────────────────────────
CAMP_Y, RUN_Y, PLINTH_Y, BANK_Y, HOLM_Y = 20, 20, 25, 17, 18

# ── materials ───────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE, GRAVEL = 1, 2, 3, 4, 13
BRICKWORK, LOG, PLANKS = 98, 17, 5
BRICK_STAIR, SPRUCE_STAIR, BRICK_SLAB = 109, 134, 44   # the stair an arch turns on, and the slab it fills with
CLAY = 159                       # stained clay: the block a team tint colours


def solid(block_id, data=0):
    return {"kind": "solid", "id": block_id, "data": data}


GRANITE, ANDESITE, DIORITE = solid(STONE, 1), solid(STONE, 5), solid(STONE, 3)
POLISHED_ANDESITE, POLISHED_DIORITE = solid(STONE, 6), solid(STONE, 4)
COARSE_DIRT, PLAIN_DIRT, SOD = solid(DIRT, 1), solid(DIRT), solid(GRASS)
BRICK, MOSSY, CRACKED, CHISELLED = (solid(BRICKWORK, d) for d in (0, 1, 2, 3))


def cells(size, *palette, rise=0):
    """A cell field. `rise` is its vertical period in blocks, and a bucket a player reads edge-on — the wall,
    the fill — must state one or every block of a column resolves alike and the face comes out striped (PT4)."""
    field = {"kind": "cell", "cellSize": size, "palette": list(palette)}
    if rise:
        field["rise"] = rise
    return field


def depth(*bands):
    """A vertical stack: the top course first, each band a material and how many courses of it."""
    return {"kind": "layered", "stack": {"ending": "repeat",
                                         "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def by_slope(*bands):
    """A stack on the slope axis: a thickness here is a span of DEGREES, so one stack finishes the flat, the
    shoulder and the face of the same hill. `GET …/incline?format=text` is what says where the cuts land."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def team_tint(neutral, block_id=CLAY):
    """The bucket's block in the colour of the team that owns the cell, and `neutral` on ground nobody owns."""
    return {"kind": "teamTint", "blockId": block_id, "neutral": neutral}


def diagonal(*runs, slope=1):
    """Stripes that travel round the whole void-facing perimeter and shear one cell along per course up, so a
    slope of one reads 45° on a square-blocked face (TP17). Each run is a material and how many cells wide."""
    return {"kind": "wallDiagonal", "slope": slope,
            "runs": [{"material": m, "width": w} for m, w in runs]}


def wall_run(*runs):
    """The same stripe cycle read without the shear, so the runs stand vertical and wrap the perimeter as
    pilasters. A diagonal is this pattern sheared; the two belong in one face because the eye reads the shear
    only against something straight."""
    return {"kind": "wallRun", "runs": [{"material": m, "width": w} for m, w in runs]}


def face(shear, cornice, string, run, shear_courses=7):
    """A cut face read in registers, top down. The board drops twenty courses in one go, and one pattern over
    all of it reads as a texture rather than as a wall — so the diagonal takes the seven courses under the rim
    where a player standing above it actually meets it, a two-course string closes that register, and the
    vertical run holds everything below (the last band claims the rest of the face). Depth is counted from the
    top of the wall bucket, so a face that steps keeps its registers in register."""
    return depth((shear, shear_courses), (cornice, 1), (string, 1), (run, 1))


def theme(surface, wall, rim, fill, rim_edges="drop"):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"material": rim, "depth": 1, "enabled": True},
        "surface": {"material": surface, "depth": 3},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
        "edgesFromGround": True,
    }


# The ground a team walks on, finished by its ANGLE: meadow to 30°, a worn shoulder to 45, bare rock above it.
# Its cut faces carry the team's own colour twice over — as a narrow stripe in the diagonal under the rim, and
# as the pilasters of the run below the string — so a player at the bank reads whose ground stands above them
# whichever register they are looking at.
HOLT = theme(
    surface=by_slope(
        (depth((SOD, 1), (PLAIN_DIRT, 2)), 10),
        (depth((COARSE_DIRT, 1), (PLAIN_DIRT, 2)), 10),
        (cells(9, ANDESITE, solid(COBBLE), rise=3), 70)),
    wall=face(
        shear=diagonal((cells(7, ANDESITE, solid(STONE), rise=3), 5),
                       (team_tint(GRANITE), 1),
                       (solid(COBBLE), 3),
                       (team_tint(GRANITE), 1), slope=1),
        cornice=solid(COBBLE),
        string=POLISHED_ANDESITE,
        run=wall_run((cells(6, solid(STONE), ANDESITE, rise=4), 6),
                     (team_tint(GRANITE), 2),
                     (solid(COBBLE), 3),
                     (team_tint(GRANITE), 2))),
    rim=solid(COBBLE),
    fill=solid(STONE))

# The plinth the wool stands on: worked masonry rather than ground, and the one place the team colour is not a
# stripe but a course of its own — a plinth read from the run below is mostly wall.
PLINTH = theme(
    surface=depth((cells(5, BRICK, MOSSY, CRACKED, rise=2), 1), (solid(STONE), 2)),
    wall=face(
        shear=diagonal((cells(6, BRICK, MOSSY, rise=2), 4),
                       (team_tint(CHISELLED), 2),
                       (solid(BRICKWORK, 0), 4),
                       (team_tint(CHISELLED), 2), slope=1),
        cornice=CHISELLED,
        string=POLISHED_ANDESITE,
        run=wall_run((cells(6, BRICK, CRACKED, rise=3), 5),
                     (team_tint(CHISELLED), 2),
                     (MOSSY, 3),
                     (team_tint(CHISELLED), 2))),
    rim=CHISELLED,
    fill=solid(STONE))

# The holm belongs to nobody, so nothing on it is tinted: a pale, quarried rock that reads as a third place
# from either camp. Its diagonal leans the other way and its run is gravel rather than clay, which is the
# whole of what says the middle is not either team's.
HOLM = theme(
    surface=by_slope(
        (depth((SOD, 1), (PLAIN_DIRT, 1), (solid(STONE), 1)), 10),
        (depth((cells(8, solid(GRAVEL), COARSE_DIRT, rise=2), 1), (solid(STONE), 2)), 15),
        (cells(7, DIORITE, ANDESITE, rise=2), 65)),
    wall=face(
        shear=diagonal((cells(8, DIORITE, solid(STONE), rise=3), 6),
                       (solid(GRAVEL), 2),
                       (ANDESITE, 4), slope=-1),
        cornice=solid(COBBLE),
        string=POLISHED_DIORITE,
        run=wall_run((cells(7, DIORITE, solid(STONE), rise=4), 5),
                     (ANDESITE, 2),
                     (solid(GRAVEL), 1),
                     (ANDESITE, 2))),
    rim=DIORITE,
    fill=solid(STONE))


# The way worn between the camp, the wool and the frontline. Its own surface and nothing else: a stroke that
# owned its whole column would repaint the board's edge wherever it reached one.
TRACK = theme(
    surface=depth((cells(4, COARSE_DIRT, PLAIN_DIRT, solid(GRAVEL), rise=2), 1), (PLAIN_DIRT, 2)),
    wall=solid(COBBLE), rim=COARSE_DIRT, fill=solid(STONE))
TRACK["edgesFromGround"] = True


def track(shape_id, points, radius=2.0, seed=5):
    """A worn way, drawn as a path: the rasterizer splines its centreline before offsetting the band, so five
    stated points come out a curve rather than five straight runs.

    It states the run's own surface, and that is what makes it paint. A stroke owns the theme on a cell only
    where it reaches the tallest ground stated there, and the reading is taken against the ground the SHAPES
    draw rather than the one the relief carves — so a path lying on the terrace it crosses has to be stated at
    that terrace's height, whatever the flight under it later does to the column. Its own height changes
    nothing about where it ends up: the relief owns the ground once a group carries one, so the way follows
    the flight down onto the bank exactly as the ground does."""
    return {
        "id": shape_id, "type": "polyline", "operation": "add", "override": False, "keepClear": True,
        "stroke_edge": "rough", "stroke_seed": seed, "radius": radius, "theme": "track",
        "floor": 0, "base_height": RUN_Y,
        "vertices": points,
    }


TRACKS = [
    # Out of the camp door, along the run, and up the plinth's own flight to the wool.
    track("way-wool", [[0, -63], [9, -60], [20, -55], [33, -54], [44, -56]], seed=5),
    # And the other way out of the door: down the flight onto the bank and on to the frontline.
    track("way-front", [[-2, -63], [-5, -57], [-6, -50], [-7, -42], [-9, -33]], radius=1.8, seed=9),
]

# ── the plan ────────────────────────────────────────────────────────────────────────
def piece(piece_id, role, x, z, w, h, surface):
    """A rectangle of ground, in signed proxy cells about the symmetry centre. Team 0's unit only — rot_180
    fans the rest, so everything with a team on it sits at z < 0."""
    return {"id": piece_id, "role": role, "rect": [x, z, w, h], "surface": surface}


PLAN = {
    "plan": 2,
    "meta": {"name": "Coinfall"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": RUN_Y},
    "pieces": [
        piece("camp", "spawn", -2, -16, 4, 3, CAMP_Y),        # x -10..10,  z -80..-65
        piece("run", "piece", -5, -13, 15, 3, RUN_Y),         # x -25..50,  z -65..-50
        piece("plinth", "wool-room", 10, -13, 4, 3, PLINTH_Y),  # x  50..70, z -65..-50
        piece("bank", "piece", -4, -10, 12, 4, BANK_Y),       # x -20..40,  z -50..-30
        piece("holm", "piece", -5, -2, 10, 4, HOLM_Y),        # x -25..25,  z -10..10
    ],
    # Twenty blocks of void between each bank and the holm, buildable from the first tick and wide enough to
    # bridge anywhere along the frontline rather than at one crossing.
    "zones": [{"id": "ford", "rect": [-8, -6, 16, 12]}],      # x -40..40, z -30..30
    "walls": [],
    "placements": {
        # Piece-relative offsets in BLOCKS from the piece's minimum corner. `back` is +z, toward the holm.
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 8], "facing": "back"}],
        "wools": [{"id": "wool-1", "piece": "plinth", "at": [10, 8]}],
    },
}

# ── the relief ──────────────────────────────────────────────────────────────────────
# Every level the board is cut at is stated, because the solve owns the ground once a group carries a relief
# and an unstated piece would be tweened into its neighbour. The two flights are lines with a height per
# vertex, which is what makes a band a ramp rather than a terrace.
RELIEF = {
    "base": RUN_Y,
    "reach": 0,
    "step": 1,
    "landform": "plain",
    "grain": {"amplitude": 0.6, "scale": 13, "seed": 17},
    "marks": [
        {"id": "run", "kind": "area", "bevel": 3, "h": RUN_Y,
         "ring": [[-25, -65], [50, -65], [50, -50], [-25, -50]]},
        {"id": "camp", "kind": "area", "bevel": 2, "h": CAMP_Y,
         "ring": [[-10, -80], [10, -80], [10, -65], [-10, -65]]},
        {"id": "plinth", "kind": "area", "h": PLINTH_Y,
         "ring": [[50, -65], [70, -65], [70, -50], [50, -50]]},
        # The flight onto the plinth is the WHOLE of its front: five courses over the twelve blocks of run
        # before the seam and fifteen wide, so the platform is climbed rather than walked round. A narrower
        # flight would stand proud of the run on both cheeks and put its own four-block step beside itself
        # (RL3) — a ramp is graded by being the face, not by being on it. It is stated before the bank so the
        # bank wins back the row they share.
        {"id": "plinth-stair", "kind": "line", "r": 7, "step": 1,
         "points": [[38, -57], [50, -57]], "h": [RUN_Y, PLINTH_Y]},
        {"id": "bank", "kind": "area", "bevel": 3, "h": BANK_Y,
         "ring": [[-20, -50], [40, -50], [40, -30], [-20, -30]]},
        # The flight down to the bank, and a second one at the wool end so the bank is not a one-way drop.
        {"id": "bank-stair", "kind": "line", "r": 5, "step": 1,
         "points": [[-6, -56], [-6, -44]], "h": [RUN_Y, BANK_Y]},
        {"id": "bank-ramp", "kind": "line", "r": 4, "step": 1,
         "points": [[33, -56], [33, -44]], "h": [RUN_Y, BANK_Y]},
        # The holm, which the same solve owns: a shore low enough to bridge onto and a crown that has to be
        # climbed, so holding the middle is standing on top of it rather than stepping across it.
        {"id": "shore", "kind": "area", "bevel": 4, "h": HOLM_Y,
         "ring": [[-25, -10], [25, -10], [25, 10], [-25, 10]]},
        {"id": "crown", "kind": "area", "bevel": 7, "h": HOLM_Y + 5,
         "ring": [[-11, -8], [11, -8], [13, 0], [11, 8], [-11, 8], [-13, 0]]},
    ],
}


# ── the houses ──────────────────────────────────────────────────────────────────────
def window(form, block, sill, width, height, spacing, data=0):
    return {"form": form, "block": block, "hostBlock": -1, "hostData": 0, "data": data,
            "sill": sill, "width": width, "height": height, "spacing": spacing}


def wall_part(*bands, extent):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "extent": extent}


def storey(clear, wall, windows, deck=None):
    out = {"clear": clear, "wall": wall, "windows": windows, "post": solid(LOG, 1),
           "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                       "inlayInset": 2, "isPlain": True}}
    if deck is not None:
        out["deck"] = deck
    return out


# The ground storey is masonry and the two over it are timbered, which is what makes the building read tall
# from the far bank: the stone is a plinth and the frame above it is the storey count made visible.
STONE_WALL = wall_part((cells(5, BRICK, MOSSY, rise=2), 4), (CHISELLED, 1), extent=5)
# The timbered storey's top course is a LAID log, which is what the beam ends run out of: a beam whose wall
# has no laid course behind it is masonry with timber stuck to it (HS9).
TIMBER_WALL = wall_part((solid(PLANKS, 1), 3), ({"kind": "laidLog", "id": LOG, "data": 1}, 1), extent=4)

SPRUCE_ROOF = {
    "form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
    "ridgeCap": True, "hole": False,
    "body": solid(PLANKS, 1), "verge": solid(PLANKS, 5),
    "gable": solid(PLANKS, 5),
    "gableWindows": window("none", 102, 2, 1, 1, 3),
}

HALL_STYLE = {
    "foundation": {
        "plate": {"stack": {"ending": "repeat", "bands": [{"material": cells(4, BRICK, CRACKED, rise=2), "thickness": 1}]},
                  "extent": 2},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": SPRUCE_ROOF,
    "wall": STONE_WALL,
    "post": solid(LOG, 1),
    "windows": window("pane", 102, 2, 2, 2, 3),
    # Three storeys of four clear: fifteen courses of wall under a roof that climbs two a block.
    "storeys": [
        storey(4, STONE_WALL, window("arched", BRICK_STAIR, 2, 2, 3, 4)),
        storey(4, TIMBER_WALL, window("pane", 102, 2, 2, 2, 3), deck=solid(PLANKS, 1)),
        storey(4, TIMBER_WALL, window("pane", 102, 1, 2, 2, 4), deck=solid(PLANKS, 1)),
    ],
    "porch": None,
    "front": "negZ",
    "beams": {"block": LOG, "data": 1, "reach": 1, "any": True},
    # An arch turns its two corners on a stair and fills the line between them with that stair's own slab,
    # which is one material at three cuts (HS1, HS4); five of height leaves the doorway its clearance once
    # the head is written in (HS2).
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": BRICK_STAIR, "fill": "upperSlab",
                         "fillBlock": BRICK_SLAB, "fillData": 5},
                "width": 3, "height": 5},
}

# The wool's tower: the same masonry, two storeys and a steeper roof over a smaller footprint, so the plinth
# reads as one building rather than a second hall.
VAULT_STYLE = dict(HALL_STYLE)
VAULT_STYLE["storeys"] = [
    storey(5, STONE_WALL, window("arched", BRICK_STAIR, 2, 1, 3, 3)),
    storey(4, wall_part((cells(5, BRICK, MOSSY, rise=2), 3),
                        ({"kind": "laidLog", "id": LOG, "data": 1}, 1), extent=4),
           window("pane", 102, 1, 2, 2, 3), deck=solid(PLANKS, 1)),
]
VAULT_STYLE["roof"] = dict(SPRUCE_ROOF, form="hip", pitch=2, ridgeCap=True)
VAULT_STYLE["front"] = "negX"


# ── the dressing ────────────────────────────────────────────────────────────────────
ERRATIC = {
    "kind": "boulder", "form": "angular", "size": 4, "mossy": True,
    "rock": {"kind": "turbulence", "seed": 41, "scale": 3, "octaves": 3, "rise": 3,
             "stops": [DIORITE, ANDESITE, solid(GRAVEL)]},
}
CRAG = dict(ERRATIC, form="outcrop", size=4, rock={"kind": "cell", "cellSize": 3, "rise": 2,
                                                   "palette": [ANDESITE, solid(COBBLE), DIORITE]})
FIR = {"kind": "tree", "form": "template", "species": "spruce", "height": 11}
BIRCH = {"kind": "tree", "form": "template", "species": "birch", "height": 8}


def tree(prop_id, style, x, z, seed):
    return {"id": prop_id, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}


def rock(prop_id, style, x, z, seed):
    return {"id": prop_id, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}


DRESSING = {
    "styles": {"erratic": ERRATIC, "crag": CRAG, "fir": FIR, "birch": BIRCH},
    "props": [
        # The holm's own landmark, off the crown so the top of the knoll stays somewhere to stand.
        rock("run-stone", "erratic", 22, -61, 911),
        rock("front-crag", "crag", -16, -36, 913),
        # Firs where the run turns the camp's corner, and birches along its short end, where the ground
        # would otherwise read as nothing but grass.
        tree("run-fir-w", "fir", -20, -62, 301), tree("run-fir-e", "fir", 38, -52, 307),
        tree("run-birch-a", "birch", -22, -55, 311), tree("run-birch-b", "birch", -14, -53, 313),
        tree("run-fir-m", "fir", 34, -62, 317),
        tree("bank-birch-a", "birch", 8, -34, 319), tree("bank-birch-b", "birch", -18, -43, 323),
        tree("run-birch-c", "birch", 14, -63, 331),
        tree("bank-fir", "fir", 30, -36, 341),
        # The holm's own pair, on its grass shore clear of the crown and the stumps: one prop, and `rot_180`
        # stands the second at (18, -2), so the middle keeps a tree at each end and neither team's half of it
        # is the bare one.
        tree("holm-birch", "birch", -18, 2, 347),
        {"id": "cover", "kind": "flora", "seed": 71,
         "spec": {"coverage": 0.45, "scale": 9, "octaves": 3, "fernShare": 0.35,
                  "flowerShare": 0.10, "flowerScale": 14, "tallShare": 0.08},
         "points": [[-20, -60], [10, -58], [40, -60], [0, -45], [-15, -38], [25, -40],
                    [-22, -52], [46, -54], [-6, -34], [36, -46]]},
    ],
}

# ── the menu ────────────────────────────────────────────────────────────────────────
# **The currency is the kit's own wood**, which is the one thing on this board a player both starts with (64)
# and earns more of (16 a kill, from the studio's default kill reward): pgm-studio has no way to state a
# currency source yet, so a shop priced in anything else is a shop nobody can buy from.
SHOP = {
    "id": "quartermaster",
    "name": "Quartermaster",
    "keeper": {"name": "`6`lQuartermaster", "mob": "Villager"},
    "categories": [{
        "id": "kit",
        "material": "gold ingot",
        "name": "`6Supplies",
        "items": [
            {"material": "golden apple", "name": "`6Runner's Apple", "price": 16, "currency": "wood"},
            {"material": "arrow", "amount": 16, "price": 8, "currency": "wood"},
            {"material": "ladder", "amount": 8, "price": 8, "currency": "wood"},
            {"material": "stained clay", "amount": 16, "price": 12, "currency": "wood", "teamColor": True},
            {"material": "iron fence", "amount": 8, "price": 24, "currency": "wood"},
        ],
    }],
}

# The holm is drawn as a rectangle and is not one. Bending it INWARD roughens the coast without narrowing
# the strait: every cut takes ground away from the island, so the twenty blocks the frontline stands off it
# is the closest the two ever come.
BENDS = {"holm-18": {"wander": 3, "step": 9, "seed": 29, "side": "in", "tension": 0.3}}


def pillar(prop_id, x, z, side, height):
    """One stump of the ruin on the holm: a thing standing ON the ground rather than ground, so it is cut
    level, sheer-sided and left out of the relief solve."""
    return {
        "id": prop_id, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
        "floor": HOLM_Y, "base_height": height, "height_mode": "level", "skirt": 0,
        "relief_scope": "exclude",
        "material": cells(3, MOSSY, BRICK, CRACKED, rise=2),
        "vertices": [[x, z], [x + side, z], [x + side, z + side], [x, z + side]],
    }


# Four stumps of a gate nobody remembers, standing where the crown gives out — cover on the one piece of
# ground both teams want, and the thing a player names the middle by.
RUIN = [
    pillar("pier-nw", -8, -7, 3, 9), pillar("pier-ne", 5, -7, 3, 7),
    pillar("pier-sw", -8, 4, 3, 7), pillar("pier-se", 5, 4, 3, 9),
]

FINISH = {
    "authors": ["Opus 5"],
    "created": "2026-09-12",
    "addShapes": RUIN + TRACKS,
    "bendShapes": BENDS,
    "themes": {"holt": HOLT, "plinth": PLINTH, "holm": HOLM, "track": TRACK},
    "mapTheme": "holt",
    "themeByHeight": {str(PLINTH_Y): "plinth", str(HOLM_Y): "holm"},
    "relief": {"*": RELIEF},
    "roomStyles": {"spawn": HALL_STYLE, "wool": VAULT_STYLE},
    "dressing": DRESSING,
    "shops": [SHOP],
}


def write(name, document):
    path = os.path.join(HERE, name)
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
        handle.write("\n")
    print(f"wrote {path}")


write(f"{BASE}.plan.json", PLAN)
write(f"{BASE}.finish.json", FINISH)
