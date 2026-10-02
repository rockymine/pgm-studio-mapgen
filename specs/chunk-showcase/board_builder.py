"""The board every plot showcase is built on: plots on chunk boundaries standing out of a sea, bridged at their
surface height, with a spawn platform to the south. A plot is a `kit.Chunk` of any size; its ground, its made
blocks and its dressing are laid out here at the plot's origin.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))

import board                                   # noqa: E402
import props as sculpt                         # noqa: E402
from layers import compile_layers              # noqa: E402
from kit import BASE, THEMES                   # noqa: E402
from catalogue import place as place_prop, PROPS as CATALOGUE   # noqa: E402

COLUMNS = 4
SEA_TOP = 4                   # sea floor tops out at y3
WATER_TOP = 7                 # water surface course y6
TREES = json.load(open(os.path.join(HERE, "trees.json")))


def origins(names, step):
    """Each plot's north-west corner, on a chunk boundary, four plots to a row."""
    rows = (len(names) + COLUMNS - 1) // COLUMNS
    west = -(COLUMNS * step // 2) // 16 * 16
    north = -(rows * step // 2) // 16 * 16
    return {name: (west + (index % COLUMNS) * step, north + (index // COLUMNS) * step)
            for index, name in enumerate(names)}


SURFACING = {2, 60, 110, (3, 2)}


def made_theme(block):
    """One block a made cell; a block that only ever surfaces ground keeps soil under it, which is all the
    painter accepts of it."""
    if block[0] in SURFACING or block in SURFACING:
        return board.shaded(surface=block, wall=(3, 0), rim=block)
    return board.solid(*block)


def block_theme(block):
    return f"b{block[0]}_{block[1]}"


def build(selected, size, step):
    """The board's document: every plot `size` square, `step` apart, on a sea, bridged, with a spawn platform.
    Answers the document, a row of facts a plot and the spawn point."""
    mid = size // 2
    placed = origins([c.name for c in selected], step)
    xs = [o[0] for o in placed.values()]
    zs = [o[1] for o in placed.values()]
    box = (min(xs) - 24, min(zs) - 24, max(xs) + size + 24, max(zs) + size + 56)

    ground = sculpt.LayerBuilder("ground", name="Ground", mirrors=False)
    upper = sculpt.LayerBuilder("upper", name="Cave roofs", mirrors=False)
    ground.rect(box[0], box[1], box[2], box[3], 0, SEA_TOP, "sea-floor", keepClear=False)
    themes = dict(THEMES)
    dressing, styles = [], {}
    serial = 0

    for chunk in selected:
        ox, oz = placed[chunk.name]
        ground.rect(ox, oz, ox + size, oz + size, 0, BASE, chunk.theme, keepClear=False)
        for shape in chunk.shapes:
            shape = dict(shape)
            kind = shape.pop("kind")
            height = BASE + shape.pop("h")
            theme = shape.pop("theme") or chunk.theme
            extra = {"override": True} if shape.pop("override") else {}
            if kind == "circle":
                ground.disc(ox + shape["cx"] + 0.5, oz + shape["cz"] + 0.5, shape["r"], 0, height, theme,
                            keepClear=False, **extra)
            else:
                ground.poly([(ox + px, oz + pz) for px, pz in shape["points"]], 0, height, theme,
                            keepClear=False, **extra)
        for (x0, z0, x1, z1), h, theme, override in chunk.ground:
            ground.rect(ox + x0, oz + z0, ox + x1 + 1, oz + z1 + 1, 0, BASE + h, theme, keepClear=False,
                        **({"override": True} if override else {}))
        for (x0, z0, x1, z1), floor, top, theme in chunk.upper:
            upper.rect(ox + x0, oz + z0, ox + x1 + 1, oz + z1 + 1, BASE + floor, top - floor, theme, keepClear=False)
        for x, z, style in chunk.trees:
            serial += 1
            styles[style] = TREES[style]
            dressing.append({"id": f"t{serial}", "kind": "tree", "seed": serial, "x": ox + x, "z": oz + z,
                             "style": style})
        for x, z, form, reach, mossy in chunk.boulders:
            serial += 1
            key = f"{form}-{reach}{'-moss' if mossy else ''}"
            styles[key] = {"kind": "boulder", "form": form, "size": reach, "mossy": mossy}
            dressing.append({"id": f"b{serial}", "kind": "boulder", "seed": serial, "x": ox + x, "z": oz + z,
                             "style": key})
        for points, spec in chunk.flora:
            serial += 1
            dressing.append({"id": f"f{serial}", "kind": "flora", "seed": serial,
                             "points": [[ox + px, oz + pz] for px, pz in points], "spec": spec})

    layers = [ground.done()]
    if upper.shapes:
        layers.append(upper.done())

    # the sea, the bridges between neighbouring chunks, and the spawn platform
    sea = {}
    for x in range(box[0], box[2]):
        for z in range(box[1], box[3]):
            for y in range(SEA_TOP, WATER_TOP):
                sea[(x, y, z)] = (9, 0)
    taken = set()
    for name, (ox, oz) in placed.items():
        taken |= {(x, z) for x in range(ox, ox + size) for z in range(oz, oz + size)}
    south = max(oz for _, oz in placed.values())
    nearest = min((ox for ox, oz in placed.values() if oz == south), key=lambda v: abs(v + mid))
    spawn = (nearest + mid - 8, south + size + 16)
    taken |= {(x, z) for x in range(spawn[0], spawn[0] + 16) for z in range(spawn[1], spawn[1] + 16)}
    ground.rect(spawn[0], spawn[1], spawn[0] + 16, spawn[1] + 16, 0, BASE, "plank")
    layers[0] = ground.done()

    bridges = {}
    catalogue = {p.name: p for p in CATALOGUE}
    for (dx, dz, turns) in ((1, 1, 0), (14, 1, 2), (1, 14, 0), (14, 14, 2)):
        bridges.update(place_prop(catalogue["lantern-post"], spawn[0] + dx, BASE, spawn[1] + dz, turns))
    for dz in (4, 11):
        bridges.update(place_prop(catalogue["park-bench"], spawn[0] + 2, BASE, spawn[1] + dz, 1))
        bridges.update(place_prop(catalogue["park-bench"], spawn[0] + 13, BASE, spawn[1] + dz, 3))

    def bridge(x0, z0, x1, z1):
        along_x = z0 == z1
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                if (x, z) in taken:
                    continue
                for w in (-1, 0, 1):
                    cx, cz = (x, z + w) if along_x else (x + w, z)
                    bridges[(cx, BASE - 1, cz)] = (5, 1)
                    if w != 0:
                        bridges[(cx, BASE, cz)] = (85, 0)
                    step = (x if along_x else z)
                    if w != 0 and step % 4 == 0:
                        for y in range(WATER_TOP - 1, BASE - 1):
                            bridges[(cx, y, cz)] = (17, 1)

    cols = {}
    for name, (ox, oz) in placed.items():
        cols[(ox, oz)] = name
    for (ox, oz) in cols:
        if (ox + step, oz) in cols:
            bridge(ox + size - 1, oz + mid, ox + step, oz + mid)
        if (ox, oz + step) in cols:
            bridge(ox + mid, oz + size - 1, ox + mid, oz + step)
    bridge(nearest + mid, south + size - 1, nearest + mid, spawn[1])

    for cell in list(sea):
        if (cell[0], cell[2]) in taken:
            del sea[cell]
    for cell in bridges:
        sea.pop(cell, None)

    def add(cells, prefix):
        named = {}
        for cell, block in cells.items():
            themes.setdefault(block_theme(block), made_theme(block))
            named[cell] = block_theme(block)
        return compile_layers(named, prefix=f"{prefix}-", layer_prefix=f"{prefix}-L", group_name=prefix,
                              part_of=prefix, mirrors=False)

    layers += add(sea, "sea")
    layers += add(bridges, "bridges")
    report = []
    for chunk in selected:
        ox, oz = placed[chunk.name]
        inside = lambda x, y, z: 0 <= x < size and 0 <= z < size and -BASE < y < 32   # noqa: E731
        out = [cell for cell in chunk.blocks if not inside(*cell)]
        if out:
            print(f"  ! {chunk.name}: {len(out)} blocks outside the plot left out, e.g. {out[:3]}")
        cells = {(ox + x, BASE + y, oz + z): block for (x, y, z), block in chunk.blocks.items() if inside(x, y, z)}
        made_layers = add(cells, chunk.name) if cells else []
        layers += made_layers
        report.append({"name": chunk.name, "title": chunk.title, "blurb": chunk.blurb, "origin": [ox, oz],
                       "blocks": len(cells), "layers": len(made_layers), "trees": len(chunk.trees),
                       "boulders": len(chunk.boulders)})

    document = board.layout(layers, themes, map_theme="sea-floor", mirror="none", room_styles=None,
                            dressing={"props": dressing, "styles": styles})
    document["setup"]["bbox"] = {"min_x": box[0], "max_x": box[2], "min_z": box[1], "max_z": box[3]}
    spawn_point = (spawn[0] + 8, BASE, spawn[1] + 8)
    return document, report, spawn_point


def run(argv, plots, slug, name, size, step, test_prefix):
    """The command line both showcases share: `<out-dir> [world-dir] [--only name,name]`."""
    args = [a for a in argv if not a.startswith("--")]
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].split(",")
        args = [a for a in args if a != argv[argv.index("--only") + 1]]
    out = args[0] if args else f"/tmp/{slug}"
    world = args[1] if len(args) > 1 else None
    os.makedirs(out, exist_ok=True)

    selected = [c for c in plots if not only or c.name in only]
    if only:
        slug = test_prefix + "-".join(only)[:40]
    document, report, spawn = build(selected, size, step)
    json.dump(document, open(f"{out}/{slug}.layout.json", "w"), indent=1)
    json.dump(report, open(f"{out}/{slug}.placed.json", "w"), indent=1)
    shapes = sum(len(layer["layout"]["shapes"]) for layer in document["layers"])
    print(f"{slug}: {len(report)} plots, {len(document['layers'])} layers, {shapes} shapes")
    board.store(slug, name if not only else slug, document, authors=("Claude",), spawn=spawn,
                observer=(spawn[0], spawn[1] + 30, spawn[2] + 10))
    if world:
        board.export(slug, world)
