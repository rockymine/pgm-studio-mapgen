"""The sculpture gallery — seven compiled models on one board, exported as a world.

Each model is voxelized, compiled to layers by run index, posted, built, read back and rendered. The table it
prints is what the board exists to ask: how many layers and how many shapes does a shape the layer system was
never designed for actually take — and, beside it, **how many the geometry alone would need**. The gap
between those two numbers is the finding: a Rubik's cube is one run per column and takes seven layers.
"""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "render"))

import board
import models
import props
from layers import compile_layers, stats

# A sculpture is painted with **solid** themes, one block a material, and that is a finding rather than a
# preference. The painter's five buckets are a model of *ground* — bedrock at the bottom, fill through the
# middle, a wall down every exposed riser and a rim capping every plateau boundary — and a curved voxel form
# is nothing but plateau boundaries, so a three-tone theme speckles the whole surface. Ground keeps its
# shading; the pieces state one block each and let the geometry do the reading.
THEMES = {
    "ground": board.shaded(surface=(2, 0), wall=(3, 0), rim=(4, 0)),
    "plinth": board.shaded(surface=(1, 4), wall=(1, 3), rim=(98, 3)),
    "pad": board.shaded(surface=(155, 0), wall=(1, 4), rim=(1, 6)),

    # the robot and the droid share a palette — one is the other's small cousin
    "shell": board.solid(155, 0),
    "trim": board.solid(35, 1),
    "joint": board.solid(1, 6),
    "panel": board.solid(35, 3),
    "visor": board.solid(168, 2),
    "eye": board.solid(35, 4),

    # the station
    "hull": board.solid(155, 0),
    "deck": board.solid(42, 0),
    "glass": board.solid(95, 3),
    "solar": board.solid(22, 0),

    # the car
    "paint": board.solid(35, 14),
    "stripe": board.solid(155, 0),
    "chrome": board.solid(42, 0),
    "lamp": board.solid(89, 0),
    "tail": board.solid(159, 14),
    "tyre": board.solid(35, 15),

    # the statue
    "stone": board.shaded(surface=(1, 4), wall=(24, 2), rim=(24, 0)),
    "robe": board.solid(159, 8),
    "fold": board.solid(159, 7),
    "hood": board.solid(159, 9),
    "dark": board.solid(49, 0),
    "metal": board.solid(42, 0),
    "flame": board.solid(89, 0),

    # the starship
    "ship-hull": board.solid(155, 0),
    "ship-grey": board.solid(1, 6),
    "ship-red": board.solid(35, 14),
    "ship-dark": board.solid(49, 0),
    "ship-glow": board.solid(89, 0),
    "ship-glass": board.solid(95, 9),

    # the dragon
    "scale": board.solid(35, 13),
    "belly": board.solid(159, 4),
    "membrane": board.solid(159, 14),
    "spine": board.solid(159, 15),
    "bone": board.solid(159, 0),
    "ember": board.solid(89, 0),
    "rock": board.shaded(surface=(1, 5), wall=(1, 0), rim=(4, 0)),

    # the cube — six sticker colours and a black frame
    "frame": board.solid(35, 15),
    "white": board.solid(155, 0),
    "yellow": board.solid(35, 4),
    "green": board.solid(35, 13),
    "blue": board.solid(35, 11),
    "red": board.solid(35, 14),
    "orange": board.solid(35, 1),
}

DECK_TOP = 5
SPAWN = (0, DECK_TOP + 1, -108)

# `(name, maker, origin, plinth half-width or None for a piece that flies)`. The front row stands, the middle
# row stands, and the two that fly hang over the back of the board with nothing under them — a mass with sky
# over it and no route onto it, which is what `SK11` says about all of them and none of it a fault.
PIECES = [
    ("robot", models.robot, (-116, DECK_TOP + 1, -74), 17),
    ("droid", models.droid, (-76, DECK_TOP + 1, -74), 12),
    ("rubik", models.rubik, (-40, DECK_TOP + 1, -84), 17),
    ("statue", models.statue, (10, DECK_TOP + 1, -74), 15),
    ("car", models.car, (62, DECK_TOP + 1, -74), 24),
    ("walker", models.walker, (112, DECK_TOP + 1, -74), 26),
    ("dragon", models.dragon, (-64, DECK_TOP + 1, 10), 46),
    ("starship", models.starship, (66, DECK_TOP + 24, -10), None),
    ("station", models.station, (66, DECK_TOP + 34, 76), None),
]


def geometric_depth(voxels):
    """How many layers the model's *shape* alone would need — maximal runs per column, ignoring material.
    The compiler's own count is this plus every colour change inside a run."""
    columns = defaultdict(set)
    for (x, y, z) in voxels:
        columns[(x, z)].add(y)
    deepest = 0
    for ys in columns.values():
        runs = sum(1 for y in ys if y - 1 not in ys)
        deepest = max(deepest, runs)
    return deepest


def deck():
    ground = props.LayerBuilder("deck", name="Deck")
    ground.rect(-146, -124, 146, 120, 0, DECK_TOP, "ground")
    for name, _, (dx, _, dz), half in PIECES:
        if half:
            ground.rect(dx - half, dz - half, dx + half, dz + half, 0, DECK_TOP + 1, "plinth")
    ground.rect(SPAWN[0] - 9, SPAWN[2] - 5, SPAWN[0] + 9, SPAWN[2] + 5, 0, DECK_TOP + 1, "pad")
    return ground.done()


def build():
    layers = [deck()]
    table = []
    for name, make, (dx, dy, dz), _ in PIECES:
        voxels = {(x + dx, y + dy, z + dz): material for (x, y, z), material in make().items()}
        made = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L", island_name=name)
        layers.extend(made)
        row = stats(voxels, made)
        row["model"] = name
        row["depth"] = geometric_depth(voxels)
        row["footprint"] = (max(c[0] for c in voxels) - min(c[0] for c in voxels) + 1,
                            max(c[1] for c in voxels) - min(c[1] for c in voxels) + 1,
                            max(c[2] for c in voxels) - min(c[2] for c in voxels) + 1)
        table.append(row)
    return layers, table


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sculpture"
    world = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(out, exist_ok=True)

    layers, table = build()
    document = board.layout(layers, THEMES, map_theme="ground", mirror="none", room_styles=None)
    json.dump(document, open(f"{out}/sculpture.layout.json", "w"), indent=1)

    print(f"{'model':<10} {'size (x,y,z)':>16} {'blocks':>8} {'shape':>6} {'layers':>7} {'shapes':>7}")
    for row in table:
        size = "x".join(str(v) for v in row["footprint"])
        print(f"{row['model']:<10} {size:>16} {row['blocks']:>8} {row['depth']:>6} {row['layers']:>7} "
              f"{row['shapes']:>7}")
    print(f"{'BOARD':<10} {'':>16} {'':>8} {'':>6} {len(layers):>7} "
          f"{sum(len(l['layout']['shapes']) for l in layers):>7}")
    print("  'shape' is the layer count the geometry alone would need; 'layers' adds every colour band")

    board.store("sculpture-gallery", "Sculpture Gallery", document, spawn=SPAWN,
                observer=(0, DECK_TOP + 80, -150))
    payload = board.columns("sculpture-gallery", document)
    json.dump(payload, open(f"{out}/sculpture.columns.json", "w"))
    if world:
        board.export("sculpture-gallery", world)

    import iso
    iso.isometric(payload, f"{out}/sculpture-iso.png", scale=3, quarter=2,
                  title="nine solids compiled into sketch layers",
                  caption="every block here is a rectangle on a layer of one sketch document")
    for name, make, (dx, dy, dz), half in PIECES:
        cells = make()
        clip = (dx + min(c[0] for c in cells) - 4, dx + max(c[0] for c in cells) + 4,
                dy - (2 if half else 0), dy + max(c[1] for c in cells) + 2,
                dz + min(c[2] for c in cells) - 4, dz + max(c[2] for c in cells) + 4)
        iso.isometric(payload, f"{out}/{name}-iso.png", scale=6, clip=clip, title=name, quarter=2)
        iso.elevation(payload, f"{out}/{name}-front.png", face="north", scale=6, clip=clip,
                      title=f"{name} - north elevation")
        iso.exploded(payload, f"{out}/{name}-layers.png", scale=4, clip=clip, quarter=2,
                     title=f"{name} - one panel per sketch layer",
                     order=[l for l in payload["layers"] if l.startswith(f"{name}-L")])
    print("rendered", out)
