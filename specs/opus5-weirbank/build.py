"""Weirbank -- a flooded bay bitten into a moor, and the one bridge over the gulf beyond it.

Half of Millrace's bounding box: 130 x 120 blocks against 250 x 240. The extent is symmetric about the
origin under rot_180, so its width in cells is always even and an exact 125 is not expressible; 130 is
the nearer of the two and the depth is exactly half.

The art direction is Millrace's and the geometry is not. Three grounds, each a two-shade noise pair of
ONE family so it reads as grain; every edge between two grounds is a drawn shape and never a sampled
field; everything built is one masonry, including the flights of steps; the landforms are in the relief
rather than in the piece list.

Three things are deliberately not Millrace's, and each was forced by a refusal rather than chosen:

  * **The cut is void, not water.** Millrace's race is water on a bed, and a bed is a floor: it joins
    the two halves with ground a player walks. The brief's ruling is that the sides meet over a build
    zone above void and never by a land connection, so the water came inland.
  * **The crossing is a promontory, not an open face.** A shelf presenting its whole length to the cut
    refuses on FR6 (frontline-width 24 against a band of [1, 16]), and leaves the walk so short that
    GO1's ratio ceiling of L/4 and GO4's floor of 40 blocks have no common solution. The quay narrows
    the frontage to six cells and lengthens the walk until both fit.
  * **A bay is bitten into the shelf.** One shelf 120 blocks deep is a single unbroken lane and refuses
    on LN2 (max-chain-length 120 against [25, 110]). Splitting the piece does not help -- the chain is
    measured over contiguous ground, not per rectangle -- so the ground itself has to break. The bay is
    that break, the water in it is why the board is called Weirbank, and the neck beside the quay is
    the only ground joining the shelf's two halves.

Measured on the final plan: goal 41 blocks from its own spawn (GO4 [40, 90]), ratio 3.41 (GO1
[3.0, 4.0]), opposing goals 99 apart (GO3 [85, 150]), no violations.

No grown trees on this board. `TreeForm` has exactly two values and the other one is `template`, the
vanilla tree of a named species, so the copses are template oak, birch and spruce; a template takes a
`species` where a grown tree takes a `wood`.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = f"{ROOT}/specs/opus5-weirbank/opus5-weirbank"

# ── the board ────────────────────────────────────────────────────────────────────────────────────
CELL = 5
plan = {
 "plan": 1,
 "meta": {"name": "Weirbank"},
 "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 8, "surface": 9,
             # Absent, this is derived as surface + 15 = 24, which on this board is inside the
             # bridge's own masonry. Twenty over that clears the deck and its parapets.
             "observerY": 44},
 "pieces": [
   # A team's ground is an L: the moor arm, and the neck reaching east to the water's edge. Surface 29
   # rather than 30 so the delta off globals.surface is even, which is what EL1 asks for.
   {"id": "moor",  "role": "piece", "rect": [-13,  2, 8, 10], "surface": 29},
   {"id": "neck",  "role": "piece", "rect": [-10, -3, 8,  6], "surface": 29},
   # The quay: the promontory the bridge springs from, six cells of frontage on the cut. A shelf
   # presenting its whole length instead refuses on FR6, frontline-width 24 against a band of [1, 16].
   {"id": "quay",  "role": "piece", "rect": [-3, -3, 1, 6], "surface": 29},
   # PL4 refuses two overlapping pieces with different surfaces, and the spawn nests inside the moor,
   # so the platform cannot be raised by its own piece. What sank it was never the piece: the
   # `brow-north` push stood a landform under the stated terrace and took the ground beside it to
   # y39 while the terrace held y34. Moving the brow off the spawn is the fix; the surface stays.
   {"id": "spawn", "role": "spawn", "rect": [-12, 10, 2, 2], "surface": 29},
 ],
 # The neck carries the quay's own frontage inland rather than narrowing behind it: at z -10..10
 # against the quay's z -15..15, a five-block notch opened either side of the landing -- a bay
 # nobody drew. The crossing keeps its width and that width continues into the map.
 # The cut: the build zone over the void, and only where the two quays actually face each other. It
 # ran the board's whole length while the shelf did; now that a team's frontage is the quay's six
 # cells, a bridgeable zone anywhere else is a crossing over ground nobody stands on. Narrowing it
 # costs nothing measurable -- GO1 3.29, GO3 93 and the goal's own 41 are identical either way.
 "zones": [{"id": "cut", "rect": [-2, -3, 4, 6], "holes": []}],
 "placements": {
   "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [1, 1], "facing": "front"}],
   "wools": [], "iron": [],
   # A 3x3x3 of ender stone rather than the default 1x3x1 of obsidian. The vocabulary is six styles
   # -- pillar-1|2|3, cube-3, cube-4, column-plus -- and four materials: obsidian, emerald block,
   # gold block, ender stone. Obsidian at pillar-3 is three very slow breaks, which is a coarse
   # progression on a board this small and rewards a defender for arriving at all; a cube-3 is 27
   # blocks and ender stone breaks quickly, so the attack shows as it accumulates rather than in
   # three lumps.
   "destroyables": [{"id": "destroyable-1", "piece": "moor", "at": [5, 2],
                     "style": "cube-3", "materials": "ender stone"}],
   "cores": [],
 },
 "walls": [], "boxes": [],
}

# The world coordinates the plan above works out to, named once so nothing below repeats a number.
MOOR_W, MOOR_E, MOOR_S, MOOR_N = -65, -25, 10, 60    # the moor arm
NECK_W, NECK_E, NECK_Z         = -50, -10, 10        # the neck, and its half-depth
QUAY_E                         = -10                 # the quay's face; void from here to x 10
GOAL                           = (-40, 20)           # destroyable-1's anchor, read off the compile
SPAWN                          = (-55, 55)
TARN                           = (-34, 38)           # centre of the water, on the moor arm

# ── the palette ──────────────────────────────────────────────────────────────────────────────────
def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
GRASS, PODZOL, DIRT, COARSE = solid(2), solid(3, 2), solid(3, 0), solid(3, 1)
STONE, ANDESITE, COBBLE, MOSSY_C, GRAVEL = solid(1), solid(1, 5), solid(4), solid(48), solid(13)
SBRICK, MOSSY_B, CRACKED = solid(98), solid(98, 1), solid(98, 2)

def noise(a, b, scale, seed, rise=2):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 4, "stops": [a, b], "rise": rise}
def theme(surf, wall, fill, depth=1):
    return {"bedrock": {"relative": False, "value": 1}, "wallOnTerrainFaces": False,
            "surface": {"enabled": True, "depth": depth, "material": surf},
            "wall": wall, "wallEnabled": True, "fill": fill,
            "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "boundary"}

# Three grounds and one masonry. Each noise pair is two shades of one family: grass over a stone body
# is the moor, coarse-dirt over stone the trodden ground, podzol over mossy stone the bay's shore. The
# rim is off on all of them -- a rim caps every fall with a band and turns a relief's rolling ground
# into contour lines, and it belongs on an edge that was made rather than solved.
THEMES = {
 "moor":    theme(GRASS, noise(STONE, ANDESITE, 20, 12), noise(STONE, ANDESITE, 20, 12)),
 "worn":    theme(noise(COARSE, DIRT, 18, 13), noise(STONE, ANDESITE, 20, 12),
                  noise(STONE, ANDESITE, 20, 12)),
 "holm":    theme(noise(PODZOL, COARSE, 15, 31), noise(STONE, MOSSY_C, 13, 32),
                  noise(STONE, MOSSY_C, 13, 32)),
 "masonry": theme(noise(SBRICK, MOSSY_B, 11, 41), noise(SBRICK, CRACKED, 11, 42),
                  noise(SBRICK, CRACKED, 11, 42)),
 # No theme for the tarn's floor. The bed and the beach are the water's business, not the ground's:
 # the pool prop states them itself on `bank`, and a theme here would be a second, unread copy.
}

# ── heights ──────────────────────────────────────────────────────────────────────────────────────
BANK      = 29   # the shelf, and the plan's own stated surface
TERRACE   = 32   # the terrace: top y31, one course over the moor at y30 beside it, measured
DECK      = 27   # the bridge deck, one course under the quay's lip so the crossing sits into it
SPRING    = 8    # where the arch springs from, at the quay's face
WATER     = 27   # the tarn: two courses under the bank it laps
TARN_BED  = 23   # four under the water line, which is what the water prop carves to
BAY_SHELF = 4    # a POOL's radius is its SHELF -- how far in from shore the bed reaches full depth
TARN_CUT  = 6    # how far the tarn's basin is sunk below the moor it is cut into

def rect(sid, x0, z0, x1, z1, floor, h, th, keep=True, level=True):
    s = {"id": sid, "type": "rectangle", "operation": "add", "override": True, "keepClear": keep,
         "min_x": x0, "max_x": x1, "min_z": z0, "max_z": z1, "floor": floor, "base_height": h,
         "skirt": 0, "relief_scope": "exclude", "theme": th}
    if level: s["height_mode"] = "level"
    return s

def built(sid, pts, radius, floor, height, th="masonry", seed=7, mode="raise"):
    """A built run. `mode` decides whether it is a made thing standing at one height or a wall that
    goes where the ground goes: `level` cuts a flat top at an absolute height, `raise` holds it a
    fixed amount above the ground under it, so a run over a rolling bank follows the incline rather
    than cutting a flat line across it. A shape declaring a height_mode reads the ground under its own
    footprint to know where to stand, so it must NOT also be excluded from the relief."""
    s = {"id": sid, "type": "path", "operation": "add", "override": True, "keepClear": True,
         "vertices": pts, "radius": radius, "path_edge": "solid", "path_seed": seed,
         "floor": floor, "base_height": height, "skirt": 0, "height_mode": mode, "theme": th}
    if mode == "level": s["relief_scope"] = "exclude"
    return s

def blob(sid, pts, th):
    """A splotch: a drawn patch of a second ground over the first. TP10 is winner-takes-all per shape,
    so a patch of worn dirt is a shape with a theme rather than a field sampled over the meadow it
    sits in. relief_scope is left alone -- the ground under it should still roll."""
    return {"id": sid, "type": "polygon", "operation": "add", "override": False, "keepClear": False,
            "vertices": pts, "theme": th}

# The tarn's outline, needed by the basin shape, the relief and the water prop alike.
def ring(cx, cz, rx, rz, n=9):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n)),
             round(cz + rz * math.sin(2 * math.pi * i / n))] for i in range(n)]

TARN_RING = ring(TARN[0], TARN[1], 7, 9, 11)

shapes = []

# ── the revetment: the quay's face on the cut, and the one thing the two sides see of each other ──
# It stands from y0 rather than from a stated foot: a wall founded partway up hangs over the chasm with
# nothing under it, which reads as masonry floating in air. `raise` holds its cap two courses over
# whatever the quay is doing beneath it, so the run follows the incline rather than cutting a flat line.
# Each run reaches one block further into the crossing than the parapet it meets: the bridge's own
# fencing occupies z -5..-4 and z 4..5, and a wall stopping at z -5 / z 5 leaves the corner column bare
# on either side. Ending at -4 and 4 abuts the two.
shapes += [
  built("rev-s", [[QUAY_E - 1, -15], [QUAY_E - 1, -4]], 1.0, 0, 2),
  built("rev-n", [[QUAY_E - 1,   4], [QUAY_E - 1, 15]], 1.0, 0, 2),
]

# ── the bridge: half an arch, drawn once and fanned into the other half ──────────────────────────
# From the first void column rather than from inside the quay: an arch begun two blocks inland has its
# soffit at y9 under ground at y29, and the two layers then build as one solid mass -- which is what
# SK10 reported the first time round, 18 blocks deep over 32 columns. The revetment is the abutment.
def arch(sid, x0, x1, z0, z1, deck, spring, th="masonry"):
    out, half = [], float(x1 - x0)
    for x in range(int(x0), int(x1)):
        f = (x - x0) / half                      # 0 at the face, 1 at the crown
        soffit = spring + (deck - 2 - spring) * math.sqrt(max(0.0, 1 - (1 - f) ** 2))
        floor = int(round(soffit))
        out.append(rect(f"{sid}-{x}", x, z0, x + 1, z1, floor, deck - floor + 1, th))
        out.append(rect(f"{sid}-pn-{x}", x, z1, x + 1, z1 + 1, deck + 1, 2, th))
        out.append(rect(f"{sid}-ps-{x}", x, z0 - 1, x + 1, z0, deck + 1, 2, th))
    return out

BRIDGE = arch("span", QUAY_E, 0, -4, 4, DECK, SPRING)

# ── the spawn terrace, and the flight off it into the moor ───────────────────────────────────────
# The spawn room is stamped inside x -60..-50, z 50..60. The terrace carries it six courses over the
# moor and gives the door its apron; it stands from y0 because an override-add wins the whole column
# including its floor, so under it there would otherwise be nothing.
shapes.append(rect("spawn-terrace", -62, 47, -49, 60, 0, TERRACE, "masonry", keep=False))
# No flight off the terrace. Two were drawn here before this one was measured. The first fell from y37
# to y29 on the assumption that the moor was at BANK -- it was at y36 -- and built a masonry trench
# running DOWN into the hill that dead-ended where the ground rose back. The second took a real
# three-course fall, and was still a ramp in front of a door. The platform simply stands one course
# over the moor now, which is a step rather than a descent, and the ground here is flat enough that no
# relief touches it: the terrace is `level` and `relief_scope: "exclude"` either way.

# No weir, and no steps down to the water. Both were drawn when the tarn was a sheet of water lying on
# the moor and needed a dam to explain it. Once the basin was cut with `height_mode: "sink"` the water
# sits in a dish of its own with a shelf running 25 -> 23 -> 24 -> 26, so there is nothing to hold back
# and nothing to climb down: the dam was a wall standing beside a pond that did not need one, and the
# flight ran into water a player can simply walk into.

# No pad under the goal. One was drawn here when WX11 reported the monument standing two courses over
# the cell beside it -- but that was under the old relief, with `brow-north` still lifting the ground
# around it. With that push gone the moor under the goal is flat enough on its own, and the pad had
# become a shape with a `height_mode` sitting across the lane: such a shape wins the theme over a plain
# patch, so it painted the moor back over the trodden ground for the whole stretch past the objective.

# The croft's own pad: a level top at y27, which is the corner's own height, so the single cell that
# reads 26 comes up and nothing else moves. It runs out to the neck's edge while the house stays inset
# on it, so every wall stands on level pad and the two-course kerb belongs to the pad rather than to a
# foundation. No skirt: a skirt eases the pad back into the ground over its outer blocks, and with the
# house close to the pad's edge that put its walls on the slope (DR-SLOPE, ten blocks of rise across
# the footprint). One course of lift wants a kerb, not a ramp.
shapes.append({"id": "croft-pad", "type": "polygon", "operation": "add", "override": False,
  "keepClear": False,
  "vertices": [[-49, -15], [-37, -15], [-37, -2], [-49, -2]],
  "floor": 0, "base_height": 28, "height_mode": "level", "skirt": 0, "theme": "moor"})

# ── the ground people have worn ──────────────────────────────────────────────────────────────────
# ONE lane, drawn as a path rather than as three polygons. It leaves the spawn terrace, falls south
# down the moor, passes the goal, crosses the throat where the moor arm meets the neck, and runs the
# length of the neck onto the bridge -- which is the route, end to end, and the only route there is.
# It was three separate patches before: one down to the goal, one at the throat and one at the
# landing, with untrodden grass between them. A lane that stops at the objective says the objective is
# where people stop going, and the three read as dirt spilled on the map rather than as a way across
# it.
shapes.append({"id": "worn-lane", "type": "path", "operation": "add", "override": False,
  "keepClear": False, "path_edge": "solid", "path_seed": 5, "radius": 3.0,
  "vertices": [[-55, 46], [-53, 36], [-49, 27], [-44, 21], [-40, 15], [-36, 10],
               [-31, 6], [-25, 3], [-18, 1], [-10, 0]],
  "theme": "worn"})

# The tarn's shore stays: it is the edge of the water rather than a patch of trodden ground, and it is
# `holm` -- podzol over mossy stone -- rather than the lane's coarse dirt.
shapes.append(blob("shore", [[-44, 30], [-34, 28], [-24, 31], [-23, 42], [-31, 48], [-42, 45],
                             [-45, 38]], "holm"))

# No obelisk. A dressed pale-stone pillar on a moor is a monument, and this board has nothing that
# would have raised one -- it read as an ornament dropped on the landscape rather than as something the
# place contains. Its job, a landmark on the neck where the two routes meet, is done by a standing rock
# instead: see `err-stone` in the dressing below. That leaves the bridge as the only layer over the
# compiled ground, and no made things at all.

def prop_layer(lid, part, shs, mirrors=True, seat="ground"):
    """A made thing. `seat: "ground"` settles the whole run of layers onto the terrain under it as one
    unit: written at an absolute floor instead, the obelisk's base sat at y29 over ground the relief
    had taken to y22 and the pillar stood in seven courses of air."""
    return {"id": lid, "name": lid, "base_y": 0, "kind": "made", "part_of": part, "seat": seat,
            "shapes": shs,
            "groups": [{"id": lid + "-body", "name": part, "mirrors": mirrors,
                        "shapeIds": [s["id"] for s in shs]}]}

layers = [{"id": "span", "name": "span", "base_y": 0, "shapes": BRIDGE,
           "groups": [{"id": "span-body", "name": "span", "mirrors": True,
                       "shapeIds": [s["id"] for s in BRIDGE]}]}]

# ── relief ───────────────────────────────────────────────────────────────────────────────────────
# A finite `reach` is what makes a mark local; `reach: 0` is unlimited and every mark then reaches every
# cell, which is the contour-step ground RL2 calls cut rather than shaped. RL2 also refuses ground whose
# every step is a barrier, so the pushes are few, far apart and widely blended: a wide falloff against a
# small amount is what rolls, and the first pass at half these falloffs read as 31 steps taller than a
# player can scramble.
RELIEF = {"team": {
  "base": BANK, "reach": 34, "step": 1, "stairs": True, "landform": "moor",
  "grain": {"amplitude": 0.8, "scale": 22, "seed": 5},
  "marks": [],   # the tarn is cut by a `sink` shape, not graded by a mark -- see tarn-basin
  "pushes": [
    {"id": "fell-west",  "ring": ring(-58, 20, 12,  9), "amount": 3, "falloff": 38,
     "roughness": 0.2, "crown": 2, "seed": 8},
    {"id": "swell-neck", "ring": ring(-32,  0, 12,  7), "amount": -2, "falloff": 30,
     "roughness": 0.2, "crown": 2, "seed": 9},
  ]}}

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────
# Every coordinate is placed because there is an answer to "why here", and every one is kept out of
# three boxes: OB19's is a 10-block square about the goal's anchor tested against a prop's eaves as well
# as its footprint, so the goal at (-50, 15) reserves x -62..-38, z 3..27 with one for the overhang;
# DR-KEEP's is the spawn door's approach, twenty blocks out from the room's face, here x -60..-50 and
# z 30..50; and DR-CLAIM refuses anything standing in a column the tarn's own channel has claimed.
def template_tree(pid, x, z, species, height):
    """A vanilla tree of a named species. `form: "template"` is the other half of TreeForm -- the grown
    skeleton is what this board does not use -- and a template takes a `species` where a grown tree
    takes a `wood`, because the species carries the canopy profile and the proportions."""
    return {"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973, "layer": "ground",
            "form": "template", "species": species, "x": x, "z": z, "height": height}

def boulder(pid, x, z, form, size, rock):
    return {"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973, "layer": "ground",
            "x": x, "z": z, "form": form, "size": size, "rock": rock, "mossy": True}

def house(pid, x0, z0, x1, z1, style, front):
    return {"id": pid, "kind": "house", "seed": abs(x0 * 7 + z0 * 13) % 9973, "layer": "ground",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}

GNEISS = noise(STONE, COBBLE, 3, 51)     # stone mottled with cobble, in the rock's own frame
GRIT   = noise(STONE, GRAVEL, 2, 52)     # stone shot through with gravel

# A copse is a stand, not a scatter: one on the brow behind the spawn, one along the tarn's far shore,
# one on the neck above the gulf. Heights are the species' own -- a spruce listed at an oak's height
# grows a stalk under a canopy that never widens.
# Every tree on the board is a spruce: a notched cone on a leader that climbs almost the whole height,
# which is the silhouette a taiga wants. Heights vary 9..15 -- the species' own natural height is 13,
# and a spruce listed at an oak's height grows a stalk under a canopy that never widens.
COPSE_WEST  = [(-63, 16, "spruce", 13), (-61, 26, "spruce", 15), (-64, 34, "spruce", 12),
               (-56, 12, "spruce", 10)]
COPSE_SPAWN = [(-64, 52, "spruce", 13), (-64, 44, "spruce", 12), (-47, 57, "spruce", 11),
               (-46, 48, "spruce", 10), (-48, 41, "spruce", 14)]
COPSE_TARN  = [(-27, 50, "spruce", 11), (-31, 57, "spruce", 13)]
COPSE_NECK  = [(-36, -12, "spruce", 12), (-33, -9, "spruce", 10), (-20, 10, "spruce", 11),
               (-16, -11, "spruce",  9)]

# `cairn` is the one tapering form -- three shrinking lobes stacked up -- so it is what a standing rock
# has to be built from; the other three are a rounded mass, that mass broken up, and a low outcrop. A
# boulder takes no aspect, only `size`, and the proportions come with the form: at 6 it stands about
# twelve courses on a base five across. Bigger reads taller but the base widens with it, and at 8 the
# footprint overruns the neck's own lip.
BOULDERS = [("err-brow",  -37, 51, "angular", 6, GNEISS),
            ("err-lane",  -53, 20, "round",   5, GNEISS),
            ("err-stone", -26, -8, "cairn",   6, GNEISS)]

STYLE   = json.load(open(f"{ROOT}/tools/styles/17h-croft.json"))
# No cobble ring at the sill. `Foundation.footing` is the course ringing the plate one block proud, and
# null -- its own default -- is a building that meets the ground without one.
STYLE["foundation"]["footing"] = None
VARIANT = json.loads(json.dumps(STYLE))
SWAP = {(4, 0): (1, 5), (98, 0): (1, 0), (98, 1): (1, 5)}     # a greyer stone, not a second family
def repaint(n):
    if isinstance(n, dict):
        if n.get("kind") == "solid" and (n.get("id"), n.get("data", 0)) in SWAP:
            n["id"], n["data"] = SWAP[(n["id"], n.get("data", 0))]; return
        for v in n.values(): repaint(v)
    elif isinstance(n, list):
        for v in n: repaint(v)
repaint(VARIANT)

DRESSING = {"props": [
  # The tarn. Its ring is the hollow the relief already cut, so the water is the shape of the ground
  # rather than a second outline disagreeing with it. On a pool `radius` is the SHELF -- how far in from
  # the shore the bed reaches full depth -- so a value near the pool's own half-width shelves the whole
  # way and lays a sheet of water on grass, which is exactly what the first build did.
  {"id": "tarn-water", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool",
   "points": TARN_RING, "radius": BAY_SHELF, "depth": WATER - TARN_BED, "shore": 3,
   "shoreWander": False, "edge": 0.6, "level": WATER,
   # The bed and the beach are one material and it is not the moor's grass: two blocks of one family,
   # gravel shot through with coarse dirt, which is what shows through the shallows.
   "bank": noise(GRAVEL, COARSE, 4, 53)},
  # Two crofts. One on the neck by the throat, where the two routes meet; one on the moor above the
  # tarn. Neither is walled in the ground's own tone family: the style is timber and pale stone.
  house("croft-fold", -47, -12, -39,  -4, STYLE,   "posZ"),
 ]
 + [template_tree(f"west-{n}",  x, z, sp, h) for n, (x, z, sp, h) in enumerate(COPSE_WEST)]
 + [template_tree(f"spawn-{n}", x, z, sp, h) for n, (x, z, sp, h) in enumerate(COPSE_SPAWN)]
 + [template_tree(f"tarn-{n}", x, z, sp, h) for n, (x, z, sp, h) in enumerate(COPSE_TARN)]
 + [template_tree(f"neck-{n}", x, z, sp, h) for n, (x, z, sp, h) in enumerate(COPSE_NECK)]
 + [boulder(pid, x, z, form, size, rock) for pid, x, z, form, size, rock in BOULDERS]}

finish = {
 "themes": THEMES, "mapTheme": "moor",
 # Taiga against cold beach, as jittered cells. A biome places nothing and costs nothing -- it is the
 # byte the client reads to tint grass, leaves and water -- so a board varies in colour without one
 # extra block. `cell` is the kind to reach for first because jittered regions are the shape a biome
 # map actually has; `cellSize` is in blocks, so 36 puts two or three regions across each headland.
 # Taiga is 5 in the studio's own named table. Cold beach is 26, which that table does not name -- it
 # lists "the ones whose tint an author would reach for" and says a field may name any id whatever is
 # there -- so the palette carries the raw vanilla id.
 "biome": {"kind": "cell", "seed": 11, "cellSize": 36, "jitter": 55, "palette": [5, 26]},
 "addShapes": shapes,
 "addLayers": layers,
 "relief": RELIEF,
 "roomStyles": {"spawn": "@showcase-hall"},
 "dressing": DRESSING,
 "authors": ["Opus 5"],
 "created": "2026-08-31",
}

json.dump(plan,   open(SPEC + ".plan.json", "w"),   indent=1)
json.dump(finish, open(SPEC + ".finish.json", "w"), indent=1)
print(f"wrote plan and finish: {len(shapes)} authored shapes, {len(layers)} layers, "
      f"{len(DRESSING['props'])} props "
      f"({sum(1 for p in DRESSING['props'] if p['kind'] == 'tree')} template trees, 0 grown)")
