"""The prop showcase: every prop in `catalogue.py` placed where it would be used, on one flat board.

A street with both lanes in use, a village square, a farm, a harbour, a railway and an airstrip. The ground is
one sketch layer of rectangles; every prop is compiled to `made` layers of its own, named by `part_of`, so the
editor's strip shows one row a prop. Nothing is seated: the board is flat and every height is stated.

    python3 specs/prop-showcase/build-spec.py <out-dir> [world-dir]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))

import board                                   # noqa: E402
from layers import compile_layers              # noqa: E402
from catalogue import PROPS, place                 # noqa: E402
from placements import GROUND, PLACEMENTS, decor, SPAWN, OBSERVER, catalogue, CATALOGUE_SPAWN   # noqa: E402

SLUG = "prop-showcase"
NAME = "Prop Showcase"


def themes():
    return dict(GROUND)


def block_theme(block):
    return f"b{block[0]}_{block[1]}"


def build(placements, ground, decor_cells):
    by_name = {p.name: p for p in PROPS}

    layers = [ground]
    theme_table = themes()
    placed = []
    taken = set()

    for index, (name, x, y, z, turns) in enumerate(placements):
        voxels = place(by_name[name], x, y, z, turns)
        taken |= set(voxels)
        thing = f"{name}-{index}"
        named = {cell: block_theme(block) for cell, block in voxels.items()}
        for block in voxels.values():
            theme_table.setdefault(block_theme(block), board.solid(*block))
        layers += compile_layers(named, prefix=f"{thing}-", layer_prefix=f"{thing}-L",
                                 group_name=thing, part_of=thing, mirrors=False)
        xs = [c[0] for c in voxels]
        zs = [c[2] for c in voxels]
        ys = [c[1] for c in voxels]
        placed.append({"thing": thing, "prop": name, "title": by_name[name].title,
                       "theme": by_name[name].theme, "blocks": len(voxels),
                       "box": [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]})

    extra = {cell: block for cell, block in decor_cells.items() if cell not in taken}
    named = {cell: block_theme(block) for cell, block in extra.items()}
    for block in extra.values():
        theme_table.setdefault(block_theme(block), board.solid(*block))
    layers += compile_layers(named, prefix="decor-", layer_prefix="decor-L", group_name="decor",
                             part_of="decor", mirrors=False)
    return layers, theme_table, placed


def boards():
    from placements import ground_layer
    town = (SLUG, NAME, PLACEMENTS, ground_layer(), decor(), SPAWN, OBSERVER)
    cat_placements, cat_ground, cat_water = catalogue(PROPS)
    x, y, z = CATALOGUE_SPAWN
    cat = ("prop-catalogue", "Prop Catalogue", cat_placements, cat_ground, cat_water, CATALOGUE_SPAWN,
           (x, y + 40, z - 10))
    return [town, cat]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/prop-showcase"
    worlds = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(out, exist_ok=True)

    for slug, name, placements, ground, decor_cells, spawn, observer in boards():
        layers, theme_table, placed = build(placements, ground, decor_cells)
        document = board.layout(layers, theme_table, map_theme="grass", mirror="none", room_styles=None)
        json.dump(document, open(f"{out}/{slug}.layout.json", "w"), indent=1)
        json.dump(placed, open(f"{out}/{slug}.placed.json", "w"), indent=1)
        shapes = sum(len(layer["layout"]["shapes"]) for layer in layers)
        print(f"{slug}: {len(placed)} props, {len(layers)} layers, {shapes} shapes, {len(theme_table)} themes")
        board.store(slug, name, document, authors=("Claude",), spawn=spawn, observer=observer)
        if worlds:
            board.export(slug, os.path.join(worlds, slug))
