"""Writes sculpture-with-layers.layout.json — twenty pads and twenty made things, none of them a preset.

A layer is not a slab. It is one arbitrary height field — a `(floor, top)` pair per column — and the taller
add wins a column and brings its own floor with it. That one rule is the whole of what makes a wall, a
hollow box, a bridge and a dome authorable out of nothing but rectangles and circles.

Row 1 is one wall, four ways: the least that will do, the same wall curved, the same wall detailed across
four layers, and the same wall opened with a gateway. Row 2 is space — the hollow an override buys, crates
as cover, a span with air under it, and a tower whose corbel is a layer of its own. Row 3 is the round
thing there is no primitive for, solid out of discs and hollow out of rings, and what the painter does to a
made thing: a terrain material against a theme. Row 4 is what the rings are actually for — a field that
falls, a closed form of revolution, the reason a painted thing costs layers, and the one trap: a made thing
states an absolute floor and the ground does not know about it.

Row 5 is the rung above all of them. Where a thing stops being describable as shapes, it is written as a
SOLID and compiled — `tools/sculpt/solid.py` states it, `tools/sculpt/layers.py` splits every column into
maximal runs and puts the n-th run of every column on layer n. The layer count is then measured rather than
guessed, and on a shape a hand would have drawn the compiler draws exactly that.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from cards import SOLID, depth_stack, grid, moor
# The converter is the repository's, not a copy: a solid vocabulary and the run-index compiler behind
# `sculpture/models`. Row 5 is what it is for.
import layers as compiler
import solid

PANEL_W, PANEL_D = 64, 56
COL_X, ROW_Z = grid(4, 5, PANEL_W, PANEL_D)
GROUND_TOP = 20
PLAIN = 8                 # the solved plain: its top block is y7, so a made layer rests at base_y 8

MOOR = moor(grass_to=35, dirt_to=55)
# A made thing's theme: five buckets, so a face and a top answer differently and a cut shows a core.
MASONRY = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary",
    "rim": {"enabled": True, "depth": 1, "material": SOLID(98, 3)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(98), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 2, "material": depth_stack((SOLID(98, 1), 1), (SOLID(98), 1))},
}
# The other way to paint one: a single terrain material, which every course of every column resolves to.
PLAIN_STONE = {"kind": "cell", "cellSize": 5, "rise": 4,
               "palette": [SOLID(98), SOLID(98, 1), SOLID(98, 3), SOLID(1)]}
# Three paints that cannot be confused for one another, for the panel about what a colour costs.
PAINTS = [SOLID(24), SOLID(98), SOLID(5, 1)]


def rect(shape_id, cx, cz, half_x, half_z, floor=0, height=1, **words):
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": floor,
           "base_height": height, "min_x": cx - half_x, "min_z": cz - half_z,
           "max_x": cx + half_x, "max_z": cz + half_z}
    out.update(words)
    return out


def disc(shape_id, cx, cz, radius, floor=0, height=1, **words):
    out = {"id": shape_id, "type": "circle", "operation": "add", "floor": floor,
           "base_height": height, "center_x": cx, "center_z": cz, "radius": radius}
    out.update(words)
    return out


def dome(prefix, cx, cz, radius, step=1):
    """Concentric discs whose tops rise inward from one floor. The taller add wins the column, so no disc
    has to be cut against its neighbour and the whole dome is one layer."""
    out = []
    for r in range(radius, 0, -step):
        top = round(math.sqrt(max(0.0, radius * radius - (r - 1) ** 2)))
        out.append(disc(f"{prefix}-{r}", cx, cz, r, height=max(1, top)))
    return out


def ring(cx, cz, outer, thickness, points=48):
    """An annulus as ONE outline: the outer circle, a slit inward, the inner circle the other way round,
    and back. An outline is filled even-odd, so a ray into the middle crosses two boundaries and lands
    outside the fill, and the slit's two coincident edges cancel — a ring with no subtract in it."""
    def circle(radius, reverse=False):
        order = range(points - 1, -1, -1) if reverse else range(points)
        return [[round(cx + radius * math.cos(2 * math.pi * i / points), 2),
                 round(cz + radius * math.sin(2 * math.pi * i / points), 2)] for i in order]
    out, hole = circle(outer), circle(max(0.5, outer - thickness), reverse=True)
    return out + [out[0]] + hole + [hole[0]]


def shell_dome(prefix, cx, cz, radius, thickness, steps=11):
    """A HOLLOW dome, on one layer: rings whose floor and top both follow the shell's own curvature, so
    each column keeps the thickness of the shell at its radius. Rings rather than discs, because a floor
    that rises makes nested shapes stack — and a layer holds one span per column."""
    out = []
    for i in range(steps):
        r = radius * (1 - i / steps)
        inner = radius - thickness
        floor = round(math.sqrt(max(0.0, inner * inner - r * r)))
        top = round(math.sqrt(max(0.0, radius * radius - r * r))) + 1
        if top - floor < 1:
            continue
        out.append({"id": f"{prefix}-{i}", "type": "polygon", "operation": "add", "floor": floor,
                    "base_height": top - floor, "vertices": ring(cx, cz, r, radius / steps)})
    return out


def ramp(cx, z0):
    """Two facing bands, twenty at the north edge and eight at the south, so the panel between them is one
    even grade. `reach` 0 needs no fall-back: two marks at two heights are what a hillside is made of."""
    half = PANEL_W / 2 - 4
    def band(mark_id, height, z_from, z_to):
        return {"id": mark_id, "kind": "area", "h": height, "bevel": 0,
                "ring": [[cx - half, z_from], [cx + half, z_from],
                         [cx + half, z_to], [cx - half, z_to]]}
    return [band("fell", 20, z0 + 4, z0 + 14), band("dale", 8, z0 + PANEL_D - 14, z0 + PANEL_D - 4)]


def compiled(name, cx, cz, seat=None):
    """A panel written as a SOLID and put through the run-index compiler, which answers with layers.

    A column's blocks split into maximal runs of one material and the n-th run of every column goes on
    layer n, so the stack is as deep as the busiest column is complicated and never deeper. Nothing here
    states a layer count; every one of them is read off the model."""
    if name == "compiled-wall":                     # the same wall `one-shape` draws, written as a box
        body = solid.box(cx - 16, cx + 15, PLAIN, PLAIN + 6, cz - 1, cz)
    elif name == "a-wheel":                         # a torus stood on edge: two runs in every column
        body = solid.torus(cx, PLAIN + 11, cz, major=8, minor=3, axis="z")
    elif name == "a-shell":                         # a hollow sphere: two runs, whatever the radius
        body = solid.shell(solid.sphere(cx, PLAIN + 10, cz, 9), thickness=2)
    elif name == "seated":                          # the wheel again, but told to settle onto the ground
        body = solid.torus(cx, PLAIN + 11, cz, major=8, minor=3, axis="z")
    else:
        raise KeyError(name)
    model = {cell: "masonry" for cell in body.cells()}
    built = compiler.compile_layers(model, prefix=f"{name}-", layer_prefix=f"{name}-run",
                                    group_name=name, part_of=name, seat=seat)
    return model, built


def sculpture(name, cx, cz):
    """The shapes of one panel's made thing, by layer: a list of (base_y, [shapes])."""
    if name == "one-shape":
        return [(PLAIN, [rect("wall", cx, cz, 16, 1, height=7)])]
    if name == "a-polyline":
        arc = [[round(cx + 16 * math.cos(a)), round(cz + 10 * math.sin(a) - 10)]
               for a in [math.pi * k / 8 for k in range(9)]]
        return [(PLAIN, [{"id": "wall", "type": "polyline", "operation": "add", "floor": 0,
                          "base_height": 7, "radius": 1.5, "vertices": arc}])]
    if name == "detailed":
        # Four layers, because four things happen at four heights and each wants its own footprint.
        merlons = [rect(f"merlon-{k}", cx - 15 + k * 4, cz, 1, 1, height=2)
                   for k in range(8)]
        return [(PLAIN, [rect("plinth", cx, cz, 17, 2, height=1)]),
                (PLAIN + 1, [rect("body", cx, cz, 16, 1, height=5)]),
                (PLAIN + 6, [rect("string", cx, cz, 17, 2, height=1)]),
                (PLAIN + 7, merlons)]
    if name == "an-arch":
        # A gateway is two piers and a lintel, not a subtract: the opening is ground nobody drew on.
        return [(PLAIN, [rect("west", cx - 10, cz, 6, 1, height=7),
                         rect("east", cx + 10, cz, 6, 1, height=7)]),
                (PLAIN + 7, [rect("lintel", cx, cz, 16, 1, height=2)])]
    if name == "a-basin":
        # Nested rings whose floors rise: the outside is a wall and the middle is air, in one layer.
        return [(PLAIN, [rect("outer", cx, cz, 12, 10, height=6),
                         rect("inner", cx, cz, 10, 8, height=1, **{"override": True})])]
    if name == "cover":
        boxes = [(-10, -6, 3), (-2, 2, 2), (8, -4, 3), (2, -8, 2), (10, 6, 2)]
        return [(PLAIN, [rect(f"crate-{k}", cx + bx, cz + bz, s, s, height=s + 1)
                         for k, (bx, bz, s) in enumerate(boxes)])]
    if name == "a-bridge":
        return [(PLAIN, [rect("pier-w", cx - 12, cz, 2, 3, height=8),
                         rect("pier-e", cx + 12, cz, 2, 3, height=8)]),
                (PLAIN + 8, [rect("deck", cx, cz, 18, 3, height=1)]),
                # The rails are a second span over the deck's own columns, so they are a second LAYER:
                # one layer holds one span per column, and a parapet on a deck is `SK9` otherwise.
                (PLAIN + 9, [rect("rail-n", cx, cz - 2.5, 18, 0.5, height=1),
                             rect("rail-s", cx, cz + 2.5, 18, 0.5, height=1)])]
    if name == "a-tower":
        # A round thing there is no primitive for: discs stacked and stepped in, plus a corbelled top.
        # Three layers rather than three nested shapes: a layer holds ONE span per column, and a corbel
        # sitting on a shaft is a second span over the same ground — which is `SK9`.
        return [(PLAIN, [disc("shaft", cx, cz, 7, height=13)]),
                (PLAIN + 13, [disc("corbel", cx, cz, 8, height=2)]),
                (PLAIN + 15, [disc("cap", cx, cz, 6, height=2)])]
    if name == "a-dome":
        return [(PLAIN, dome("solid", cx, cz, 11))]
    if name == "a-hollow-dome":
        # The same dome with its floors raised by the inner sphere's curvature. Drawn as RINGS, not discs:
        # a floor that rises makes nested shapes stack, and rings that do not overlap contest nothing.
        return [(PLAIN, shell_dome("shell", cx, cz, 11, 3))]
    if name == "a-bowl":
        # A field that FALLS inward. Nesting cannot draw one: the disc that should keep only its own ring
        # is also the tallest thing over the middle, so nested discs come out a flat plate. Rings overlap
        # nothing, so each tier keeps exactly the ground it was drawn over.
        out = []
        for i in range(11):
            r = 11 * (1 - i / 11)
            drop = 8 * (1 - (r / 11) ** 2)
            out.append({"id": f"tier-{i}", "type": "polygon", "operation": "add", "floor": 0,
                        "base_height": max(1, 11 - round(drop)), "vertices": ring(cx, cz, r, 1)})
        return [(PLAIN, out)]
    if name == "a-balloon":
        # A closed form of revolution: the envelope's floor AND top both curve, so it is rings again.
        # Three layers, because a column through it passes through basket, rope and envelope in turn.
        envelope = []
        for i in range(9):
            r = 9 * (1 - i / 9)
            half = math.sqrt(max(0.0, 81 - r * r))
            floor, top = round(9 - half), round(9 + half)
            envelope.append({"id": f"skin-{i}", "type": "polygon", "operation": "add", "floor": floor,
                             "base_height": max(1, top - floor), "vertices": ring(cx, cz, r, 1)})
        ropes = [rect(f"rope-{k}", cx + rx, cz + rz, 0.5, 0.5, height=5)
                 for k, (rx, rz) in enumerate([(-3, -3), (3, -3), (-3, 3), (3, 3)])]
        return [(PLAIN, [rect("basket", cx, cz, 4, 4, height=4),
                         rect("inside", cx, cz, 3, 3, height=1, **{"override": True})]),
                (PLAIN + 4, ropes),
                (PLAIN + 9, envelope)]
    if name == "two-colours":
        # What a painted thing costs is not colours, it is COLUMNS: a column passing through three paints
        # passes through three runs, and a run is a span, and a layer holds one span.
        west = [rect("one-paint", cx - 20, cz, 6, 6, height=9, material=PAINTS[0])]
        banded = [(PLAIN, [rect("band-0", cx, cz, 6, 6, height=3, material=PAINTS[0])]),
                  (PLAIN + 3, [rect("band-1", cx, cz, 6, 6, height=3, material=PAINTS[1])]),
                  (PLAIN + 6, [rect("band-2", cx, cz, 6, 6, height=3, material=PAINTS[2])])]
        beside = [rect(f"stripe-{k}", cx + 16 + k * 4, cz, 2, 6, height=9, material=PAINTS[k])
                  for k in range(3)]
        return [(PLAIN, west + beside + banded[0][1]), banded[1], banded[2]]
    if name == "on-a-slope":
        # The one trap, and its answer, on one grade. `by-hand` states 15 because `POST /sketch/columns`
        # reads y14 as the highest ground under its footprint; `told-to-settle` beside it, on the same
        # ground, states no height at all and is put there by the studio.
        return [(PLAIN, [rect("buried", cx - 14, cz - 16, 3, 3, height=5)]),
                (15, [rect("by-hand", cx - 5, cz, 3, 3, height=5)]),
                (20, [rect("floating", cx + 14, cz + 16, 3, 3, height=5)]),
                # The fourth states the two words instead of a number. `kind` keeps the stacking rules off
                # a made thing and `seat` takes the whole layer down onto the lowest ground under it.
                (PLAIN, [rect("told-to-settle", cx + 5, cz, 3, 3, height=5)],
                 {"kind": "made", "part_of": "on-a-slope-crate", "seat": "ground"})]
    if name in ("material-only", "a-theme"):
        # Nested from ONE floor, not stacked on each other's tops: the taller add wins the column, so a
        # ziggurat is four rectangles sharing a floor. Stacking them instead is `SK9`, and the world keeps
        # one span per column.
        return [(PLAIN, [rect("step-1", cx, cz, 12, 8, height=3),
                         rect("step-2", cx, cz, 9, 6, height=6),
                         rect("step-3", cx, cz, 6, 4, height=9),
                         rect("step-4", cx, cz, 3, 2, height=13)])]
    raise KeyError(name)


PANELS = ["one-shape", "a-polyline", "detailed", "an-arch",
          "a-basin", "cover", "a-bridge", "a-tower",
          "a-dome", "a-hollow-dome", "material-only", "a-theme",
          "a-bowl", "a-balloon", "two-colours", "on-a-slope",
          "compiled-wall", "a-wheel", "a-shell", "seated"]
# Row 5 is compiled rather than drawn, and the last of them is told to settle onto a grade.
COMPILED = {"compiled-wall": None, "a-wheel": None, "a-shell": None, "seated": "ground"}

shapes, groups, relief, layers, stats = [], [], {}, [], {}
for index, name in enumerate(PANELS):
    col, row = index % 4, index // 4
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W // 2, z0 + PANEL_D // 2
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "pushes": [],
                    # Eighteen pads are flat, because a shape on a ground layer states an absolute floor.
                    # Two are a ramp on purpose: the panel about what that costs, and the panel that
                    # answers it.
                    "marks": ramp(cx, z0) if name in ("on-a-slope", "seated") else []}

    if name in COMPILED:
        model, built = compiled(name, cx, cz, seat=COMPILED[name])
        stats[name] = compiler.stats(model, built)
        layers.extend(built)
        continue

    paint = ({"material": PLAIN_STONE} if name == "material-only" else {"theme": "masonry"})
    for tier, entry in enumerate(sculpture(name, cx, cz)):
        base_y, drawn = entry[0], entry[1]
        words = entry[2] if len(entry) > 2 else {}
        layer_id = f"{name}-{tier}"
        for shape in drawn:
            shape["id"] = f"{shape['id']}-{name}"
            # A shape that states its own paint keeps it; everything else takes the board's masonry.
            if "material" not in shape:
                shape.update(paint)
        layers.append({"id": layer_id, "name": layer_id, "base_y": base_y, **words,
                       "layout": {"shapes": drawn,
                                  "groups": [{"id": layer_id, "name": layer_id, "mirrors": False,
                                              "shapeIds": [s["id"] for s in drawn]}]}})

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR, "masonry": MASONRY},
    "mapTheme": "moor",
    "relief": relief,
    # Ordered by `base_y`: the world is built from it either way, and a list disagreeing with it is `SK20`.
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}]
              + sorted(layers, key=lambda tier: tier["base_y"]),
}
out = os.path.join(HERE, "sculpture-with-layers.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {1 + len(layers)} layers -> {out}")

# What the compiler charged, written beside the board: the layer count of a compiled thing is the busiest
# column's run count, and nothing in row 5 states one.
with open(os.path.join(HERE, "compiled.txt"), "w") as report:
    report.write("tools/sculpt/layers.py — what the run-index compiler answered for row 5.\n"
                 "A column's blocks split into maximal runs of one material; the n-th run of every column\n"
                 "goes on layer n. The layer count is read off the model, never stated.\n\n")
    report.write(f"{'panel':16s}{'blocks':>8s}{'layers':>8s}{'shapes':>8s}{'blocks/shape':>14s}\n")
    for name in PANELS:
        if name not in stats:
            continue
        got = stats[name]
        report.write(f"{name:16s}{got['blocks']:8d}{got['layers']:8d}{got['shapes']:8d}"
                     f"{got['blocks_per_shape']:14.1f}\n")
    report.write("\nthe same four solids, by hand: `compiled-wall` is one rectangle and the other three\n"
                 "have no statement in rectangles and circles at all.\n")
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    if name in COMPILED:
        got = stats[name]
        print(f"  {name:14s} at x{x0:5d} z{z0:5d}  {got['layers']} layer(s), {got['shapes']} shape(s)"
              f"   compiled from {got['blocks']} block(s)")
        continue
    tiers = sculpture(name, x0 + PANEL_W // 2, z0 + PANEL_D // 2)
    print(f"  {name:14s} at x{x0:5d} z{z0:5d}  {len(tiers)} layer(s), "
          f"{sum(len(tier[1]) for tier in tiers)} shape(s)")
