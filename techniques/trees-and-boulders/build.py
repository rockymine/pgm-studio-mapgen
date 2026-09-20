"""Writes trees-and-boulders.layout.json and .intent.json — twelve pads, one road or rock or wood each.

A prop is not drawn, it is **asked for**. The dressing pass seats every one against a book of claims and
answers on a 200: a prop the book refuses is simply not in the world, and the only thing that says so is the
decline beside it. So the numbers in that book are the whole of what an author needs, and every one of them
is measured here rather than remembered.

Row 1 is what paving keeps off: the standoff a tree takes from a paved cell, the shorter one a boulder
takes, what a wide brush therefore costs, and the road drawn so that nothing is lost. Row 2 is what a prop
keeps off another: footprint overlap between two rocks, the list order that decides which of an overlapping
pair survives, and the separate rule between two canopies — then a wood thrown against it. Row 3 is what
the ground and the goals keep off: an authored shape that says `keepClear` and the same shape that does not,
a monument's clearance seen from the prop's end, and the overlay that is never declined at all.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, grid, moor

PANEL_W, PANEL_D = 64, 56
COL_X, ROW_Z = grid(4, 3, PANEL_W, PANEL_D)
GROUND_TOP = 20
PLAIN = 8                 # the solved plain: its top block is y7

MEADOW = moor(grass_to=35, dirt_to=55)
# What a road is made of, and what a wall authored as terrain is made of.
ROAD = {"kind": "cell", "seed": 3301, "cellSize": 3, "jitter": 55, "warp": 1, "rise": 0,
        "palette": [SOLID(4), SOLID(1), SOLID(1, 6)]}
MASONRY = {"bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary",
           "rim": {"enabled": True, "depth": 1, "material": SOLID(98, 3)},
           "wallEnabled": True, "wallOnTerrainFaces": True,
           "wall": SOLID(98), "fill": SOLID(1),
           "surface": {"enabled": True, "depth": 1, "material": SOLID(98)}}

# The crown reach of each recipe, in blocks from the trunk, read off the ladder in `two-trees`: a pair of
# nines stands at four and not at three, a pair of fourteens at five and not at four.
CROWN = {9: 4, 14: 5}

STYLES = {
    "oak-9":  {"kind": "tree", "form": "template", "species": "oak", "height": 9},
    "oak-14": {"kind": "tree", "form": "template", "species": "oak", "height": 14},
    "rock-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": True,
               "rock": {"kind": "turbulence", "seed": 3302, "scale": 3, "octaves": 3, "rise": 3,
                        "stops": [SOLID(4), SOLID(48), SOLID(1, 5)]}},
}


def centre(name):
    index = PANELS.index(name)
    return (COL_X[index % 4] + PANEL_W // 2, ROW_Z[index // 4] + PANEL_D // 2)


def road(prop_id, cx, cz, radius=2, style="solid", **words):
    """A straight stroke along x, so its claimed band is a known pair of rows and a standoff is countable.
    A curve would be the honest thing to draw and the wrong thing to measure against."""
    out = {"id": prop_id, "kind": "stroke", "seed": 3311, "radius": radius, "style": style,
           "claimsGround": True, "pave": ROAD,
           "points": [[cx - 30, cz], [cx - 10, cz], [cx + 10, cz], [cx + 30, cz]]}
    out.update(words)
    return out


def tree(prop_id, x, z, style="oak-9", seed=None):
    return {"id": prop_id, "kind": "tree", "seed": seed if seed is not None else 3400 + abs(x + z),
            "x": x, "z": z, "style": style}


def rock(prop_id, x, z, style="rock-3", seed=None):
    return {"id": prop_id, "kind": "boulder", "seed": seed if seed is not None else 3500 + abs(x + z),
            "x": x, "z": z, "style": style}


def wall(shape_id, cx, cz, keep_clear):
    """A town wall authored as terrain: an override add on the ground layer, six courses over the plain.

    Two fields for two passes, and neither substitutes for the other. `height_mode: "level"` with `skirt: 0`
    is what the RELIEF needs — an override add carrying neither that nor `relief_scope` is `SK14`, and comes
    out level with the ground beside it. `keepClear` is what the DRESSING pass needs: without it the shape
    is ground like any other and a prop stands inside it, reported by nothing."""
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "override": True,
           "height_mode": "level", "skirt": 0,
           "floor": 0, "base_height": PLAIN + 6, "theme": "masonry",
           # Eleven cells deep, so its head has flat ground on it: a five-cell wall is all edge, and
           # `DR-STEEP` declines a boulder standing on ground the theme paints as a face.
           "min_x": cx - 18, "min_z": cz - 5, "max_x": cx + 18, "max_z": cz + 5}
    if keep_clear:
        out["keepClear"] = True
    return out


def wood(prefix, cx, cz, count=26, half_x=26, half_z=22, seed=7):
    """Darts thrown at a box and accepted against the canopy rule in Chebyshev. A lattice at the same
    spacing either reads as a grid or breaks its own minimum; thrown points accept right up against it."""
    placed, out = [], []
    state = seed
    for _ in range(count * 60):
        if len(placed) >= count:
            break
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        x = cx - half_x + state % (2 * half_x + 1)
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        z = cz - half_z + state % (2 * half_z + 1)
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        height = 9 if state % 3 else 14
        # The measured rule, not a remembered formula: a tree is TESTED at its trunk and CLAIMS its whole
        # crown, so what two trees need between them is the larger of the two crowns — four blocks for a
        # nine and five for a fourteen — rather than the sum of both.
        if any(math.dist((x, z), (px, pz)) < CROWN[max(height, ph)] for px, pz, ph in placed):
            continue
        placed.append((x, z, height))
        out.append(tree(f"{prefix}-{len(out)}", x, z, style=f"oak-{height}", seed=3600 + len(out)))
    return out


def flora(prop_id, cx, cz):
    """The overlay, which is not a prop standing anywhere: it is grass and ferns written onto whatever cells
    the pass left free, so nothing declines it and nothing has to be spaced."""
    ring = [[round(cx + 27 * math.cos(2 * math.pi * k / 12)),
             round(cz + 23 * math.sin(2 * math.pi * k / 12))] for k in range(12)]
    return {"id": prop_id, "kind": "flora", "seed": 3700,
            "spec": {"coverage": 0.8, "scale": 8, "octaves": 3, "fernShare": 0.5,
                     "flowerShare": 0.08, "flowerScale": 14, "tallShare": 0.06},
            "points": ring}


PANELS = ["tree-standoff", "boulder-standoff", "a-wide-brush", "set-back",
          "two-boulders", "kind-decides", "two-trees", "a-wood",
          "a-kept-clear-wall", "an-unmarked-wall", "a-goal-clearance", "flora-overlay"]

# ── the props, panel by panel ──────────────────────────────────────────────────────────────────────────
props, extra_shapes = [], []

cx, cz = centre("tree-standoff")
props.append(road("road-trees", cx, cz))
# Four oaks stepping away from a band whose edge is at cz + 2, so the gaps are one, two, three and four.
props += [tree(f"off-{gap}", cx - 21 + (gap - 1) * 14, cz + 2 + gap) for gap in (1, 2, 3, 4)]

cx, cz = centre("boulder-standoff")
props.append(road("road-rocks", cx, cz))
props += [rock(f"rock-off-{gap}", cx - 21 + (gap - 1) * 14, cz + 2 + gap) for gap in (1, 2, 3, 4)]

cx, cz = centre("a-wide-brush")
# A texture brush is a road with a wide radius, and `rough` fills its band solid rather than freckling it
# — while wandering its own half-width, which is what this ladder is for. Four oaks at ONE distance from
# the centreline and four different places along it: the band's edge is not a constant offset, so the same
# stated distance is inside the keep-out at one x and outside it at the next.
props.append(road("brush", cx, cz, radius=8, style="rough", coverage=0.3))
props += [tree(f"brush-at-{index}", cx - 24 + index * 16, cz + 11, seed=3470 + index)
          for index in range(4)]

cx, cz = centre("set-back")
props.append(road("road-back", cx, cz))
# Inside the pad and clear of the road: `DR-SITE` declines a prop off the coast and `DR-CLAIM` one on
# the paving, and both are the author's arithmetic rather than the pass's opinion.
props += wood("back", cx, cz + 15, count=9, half_x=26, half_z=9, seed=11)

cx, cz = centre("two-boulders")
# DR-CLAIM is footprint overlap and nothing else: a pair three apart contests, a pair nine apart does not.
props += [rock("pair-near-a", cx - 16, cz - 6), rock("pair-near-b", cx - 13, cz - 6),
          rock("pair-clear-a", cx + 8, cz - 6), rock("pair-clear-b", cx + 17, cz - 6)]

cx, cz = centre("kind-decides")
# The same overlap twice, and the document order is opposite in the two: rock first on the west, tree
# first on the east. The pass runs in kind order, so the order stated changes nothing.
props += [rock("rock-first", cx - 14, cz), tree("tree-second", cx - 12, cz),
          tree("tree-first", cx + 14, cz), rock("rock-second", cx + 16, cz)]

cx, cz = centre("two-trees")
# Two ladders rather than a formula, and the step is along x alone so the stated separation IS the
# distance. Four pairs of nines and four of fourteens; the reading says where the pass actually cuts.
# One seed pair down each ladder, so the step is the only thing that changes between rungs.
for column, step in enumerate((1, 2, 3, 4)):
    px = cx - 24 + column * 16
    props += [tree(f"nine-{step}-a", px, cz - 14, "oak-9", seed=3411),
              tree(f"nine-{step}-b", px + step, cz - 14, "oak-9", seed=3412)]
for column, step in enumerate((2, 3, 4, 5)):
    px = cx - 24 + column * 16
    props += [tree(f"tall-{step}-a", px, cz + 14, "oak-14", seed=3431),
              tree(f"tall-{step}-b", px + step, cz + 14, "oak-14", seed=3432)]

cx, cz = centre("a-wood")
props += wood("wood", cx, cz, count=45, seed=23)
props.append(flora("wood-cover", cx, cz))

cx, cz = centre("a-kept-clear-wall")
extra_shapes.append(("a-kept-clear-wall", wall("kept-wall", cx, cz, keep_clear=True)))
props += [rock("kept-rock", cx - 10, cz), tree("kept-tree", cx + 10, cz)]

cx, cz = centre("an-unmarked-wall")
extra_shapes.append(("an-unmarked-wall", wall("plain-wall", cx, cz, keep_clear=False)))
props += [rock("plain-rock", cx - 10, cz), tree("plain-tree", cx + 10, cz)]

cx, cz = centre("a-goal-clearance")
GOAL = (cx, cz)
# Four oaks on two bearings, at a stated Chebyshev reach from the monument's own cell — and far enough
# from each other that the only rule that can refuse one is the clearance.
# The clearance is a 21 x 21 square on the monument's own cell — Chebyshev 10 — so the ladder brackets it.
props += [tree("goal-off-9", cx + 9, cz, seed=3451), tree("goal-off-10", cx, cz + 10, seed=3452),
          tree("goal-off-11", cx - 11, cz, seed=3453), tree("goal-off-12", cx, cz - 12, seed=3454)]

cx, cz = centre("flora-overlay")
props.append(road("road-cover", cx, cz))
props.append(rock("cover-rock", cx - 14, cz + 12))
props.append(flora("cover", cx, cz))

# ── the pads ───────────────────────────────────────────────────────────────────────────────────────────
shapes, groups, relief = [], [], {}
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "meadow",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    # An authored shape joins its panel's group: a shape in no group is read for its keep-out and built
    # nowhere, which is a wall that declines what leans on it and cannot be seen.
    own = [f"island-{name}"] + [shape["id"] for panel, shape in extra_shapes if panel == name]
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": own})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": []}

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"meadow": MEADOW, "masonry": MASONRY},
    "mapTheme": "meadow",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes + [shape for _, shape in extra_shapes],
                           "groups": groups}}],
    "dressing": {"styles": STYLES, "props": props},
}

# ── the intent, for the one panel that needs a goal ────────────────────────────────────────────────────
# The spawns the export needs, on the two pads whose claims a keep-out cannot reach: the wall panels
# state their props at the wall line and these stand twenty blocks south of it.
red_x, red_z = centre("a-kept-clear-wall")
blue_x, blue_z = centre("an-unmarked-wall")
intent = {
    "teams": [{"id": "red", "name": "Red", "color": "red"},
              {"id": "blue", "name": "Blue", "color": "blue"}],
    "maxPlayers": 12,
    "spawns": [{"team": "red", "yaw": 90, "iron": [],
                "point": {"x": red_x - 20, "y": PLAIN, "z": red_z + 20},
                "protection": [{"minX": red_x - 26, "minZ": red_z + 16,
                                "maxX": red_x - 14, "maxZ": red_z + 24}]},
               {"team": "blue", "yaw": 270, "iron": [],
                "point": {"x": blue_x + 20, "y": PLAIN, "z": blue_z + 20},
                "protection": [{"minX": blue_x + 14, "minZ": blue_z + 16,
                                "maxX": blue_x + 26, "maxZ": blue_z + 24}]}],
    "observer": {"point": {"x": 0, "y": 40, "z": 0}, "yaw": 0},
    # One destroyable, on the one pad the card asks a goal's clearance about.
    "destroyables": [{"owner": "blue", "name": "Clearance Monument", "style": "pillar-3",
                      "materials": "obsidian", "float": 4,
                      "anchor": {"x": GOAL[0], "y": PLAIN - 1, "z": GOAL[1]}}],
    "meta": {"name": "Trees And Boulders", "created": "2026-09-20",
             "authors": ["the technique cards"], "contributors": []},
}

json.dump(layout, open(os.path.join(HERE, "trees-and-boulders.layout.json"), "w"), indent=1)
json.dump(intent, open(os.path.join(HERE, "trees-and-boulders.intent.json"), "w"), indent=1)
kinds = {}
for prop in props:
    kinds[prop["kind"]] = kinds.get(prop["kind"], 0) + 1
print(f"{len(PANELS)} panels, {len(props)} props {kinds}, {len(extra_shapes)} authored shape(s)")
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    print(f"  {name:20s} at x{x0:5d} z{z0:5d}")
