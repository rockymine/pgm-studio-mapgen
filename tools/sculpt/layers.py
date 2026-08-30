"""A voxel model compiled into sketch layers.

The sketch's layer is a **slab**: one span per column, `[floor, floor + base_height)`, shifted by the
layer's `base_y`, and where two adds contest a cell the taller one replaces the shorter outright. That is the
one constraint the whole compilation is written against, and it has an exact consequence — a column may hold
as many spans as the document has layers, and no more.

So the decomposition is not "one layer per height". It is **one layer per run index**: a column's solid
blocks split into maximal runs of one material, and the *n*-th run of every column goes on layer *n*. The
stack is therefore as deep as the busiest column is complicated, not as tall as the model — a thirty-block
robot whose worst column passes through a boot, a shin and a hand needs three layers, and a solid tower needs
one. Runs of one column on different layers are separated by air by construction, so no pair of layers is
ever driven into another (SK10) and no shape is ever hidden under a taller one on its own layer (SK9).

Within a layer every column carries at most one run, so the shapes are laid out by grouping the runs that
agree on `(material, floor, top)` and covering each group's footprint with axis-aligned rectangles. The
covering is greedy — maximal horizontal runs, extended down while the row below repeats them — which is what
keeps a flat 40x40 plate one rectangle instead of sixteen hundred.

Material becomes **theme**: one terrain theme per material, and each shape carries the theme id, since a
theme is scoped to a shape and a cell is painted by the smallest-area shape covering it."""
from collections import defaultdict


def runs_of(column_ys):
    """One column's `{y: material}` as maximal runs `(floor, top_exclusive, material)`, bottom first."""
    out = []
    for y in sorted(column_ys):
        material = column_ys[y]
        if out and out[-1][1] == y and out[-1][2] == material:
            out[-1][1] = y + 1
        else:
            out.append([y, y + 1, material])
    return [tuple(run) for run in out]


def rectangles(cells):
    """A set of `(x, z)` cells covered by as few axis-aligned rectangles as the greedy pass finds.

    Rows are scanned north to south; each maximal run of one row is extended south while the row below holds
    exactly that run and has not been claimed. Yields `(min_x, min_z, max_x, max_z)`, inclusive."""
    by_row = defaultdict(set)
    for x, z in cells:
        by_row[z].add(x)
    claimed = set()
    out = []
    for z in sorted(by_row):
        row = sorted(by_row[z])
        start = 0
        while start < len(row):
            end = start
            while end + 1 < len(row) and row[end + 1] == row[end] + 1:
                end += 1
            x0, x1 = row[start], row[end]
            if all((x, z) not in claimed for x in range(x0, x1 + 1)):
                z1 = z
                while all((x, z1 + 1) in cells and (x, z1 + 1) not in claimed for x in range(x0, x1 + 1)) \
                        and not any((x, z1 + 1) in cells and x < x0 - 0 for x in ()):
                    # the row below must repeat the run exactly, or the rectangle would swallow a neighbour
                    below = by_row.get(z1 + 1, set())
                    if (x0 - 1 in below) or (x1 + 1 in below):
                        break
                    z1 += 1
                for zz in range(z, z1 + 1):
                    for x in range(x0, x1 + 1):
                        claimed.add((x, zz))
                out.append((x0, z, x1, z1))
            start = end + 1
    return out


def compile_layers(voxels, prefix="s", layer_prefix="L", mirrors=False, group_name=None,
                   part_of=None, seat=None):
    """A `{(x, y, z): material}` model as the `layers` array of a sketch layout.

    Every layer sits at `base_y` 0 and every shape states its own `floor`, which is what lets one layer hold
    runs at different heights: the layer is a slot in the per-column run order, not a storey at a height.
    Each layer's shapes are grouped into one group so the mirror can be turned off for the whole sculpture at
    once — a group's `mirrors` flag is the only thing that decides whether the fan copies it.

    Every layer states `kind: "made"`, which is what keeps the stacking rules off a made thing: `SK10` reads
    two layers whose spans meet as a lost gap and `SK11` reads an overhang as standable ground nothing
    reaches, and neither is true of a sculpture. `part_of` names the made thing every one of its layers is a
    slice of, so
    the studio draws one row for it and seats it as a unit; `seat="ground"` takes its floors from the lowest
    solid column under its own footprint, which is what a thing standing on terrain wants and a thing flying
    over it does not.

    **A shape marks itself kept clear only when the thing it belongs to stands on the ground.** That flag
    says the cells under it are not terrain to dress, which is true of a crane's legs and false of a balloon
    flying thirty blocks up: a floating thing's footprint is ground an author decorates, not ground it
    occupies. So `seat` decides it — the same field that says whether the model settles onto terrain."""
    stands = seat is not None
    columns = defaultdict(dict)
    for (x, y, z), material in voxels.items():
        columns[(x, z)][y] = material

    slots = defaultdict(list)                             # run index -> [(x, z, floor, top, material)]
    for (x, z), ys in columns.items():
        for index, (floor, top, material) in enumerate(runs_of(ys)):
            slots[index].append((x, z, floor, top, material))

    layers = []
    serial = 0
    for index in sorted(slots):
        groups = defaultdict(set)
        for x, z, floor, top, material in slots[index]:
            groups[(material, floor, top)].add((x, z))

        shapes = []
        for (material, floor, top), cells in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            for x0, z0, x1, z1 in rectangles(cells):
                shapes.append({
                    "id": f"{prefix}{serial}",
                    "type": "rectangle",
                    "operation": "add",
                    "min_x": x0, "min_z": z0, "max_x": x1 + 1, "max_z": z1 + 1,
                    "floor": floor,
                    "base_height": top - floor,
                    "theme": material,
                    "keepClear": stands,
                })
                serial += 1

        layer_id = f"{layer_prefix}{index}"
        layers.append({
            "id": layer_id,
            "name": f"{group_name or layer_prefix} run {index}",
            "base_y": 0,
            "kind": "made",
            **({"part_of": part_of} if part_of else {}),
            **({"seat": seat} if seat else {}),
            "layout": {
                "shapes": shapes,
                "groups": [{
                    "id": f"{layer_id}-body",
                    "name": group_name or layer_id,
                    "mirrors": mirrors,
                    "shapeIds": [shape["id"] for shape in shapes],
                }],
            },
        })
    return layers


def stats(voxels, layers):
    """What the compilation cost, which is the number the whole question turns on: how many shapes and how
    many layers a model of this many blocks came out as."""
    shapes = sum(len(layer["layout"]["shapes"]) for layer in layers)
    return {
        "blocks": len(voxels),
        "layers": len(layers),
        "shapes": shapes,
        "blocks_per_shape": round(len(voxels) / shapes, 1) if shapes else 0,
        "materials": len({m for m in voxels.values()}),
    }
