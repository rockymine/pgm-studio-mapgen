"""The sculpture gallery — four compiled models on one board, and what each cost.

Each model is voxelized, compiled to layers by run index, posted, built and read back. The table it prints
is the answer to the question the board exists to ask: how many layers and how many shapes does a shape the
layer system was never designed for actually take."""
import json
import os
import sys

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

    # the robot
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
}

DECK_TOP = 5

# The plinth stands one course above the deck, so a piece resting on it starts a course above that: two
# layers whose spans meet by more than the seam build as one mass and SK10 names the pair.
PIECES = [
    ("robot", models.robot, (-48, DECK_TOP + 1, -16), 14),
    ("station", models.station, (58, DECK_TOP + 22, 6), 44),
    ("car", models.car, (-44, DECK_TOP + 1, 28), 20),
    ("statue", models.statue, (0, DECK_TOP + 1, 24), 14),
]


def deck():
    ground = props.LayerBuilder("deck", name="Deck")
    ground.rect(-72, -46, 124, 52, 0, DECK_TOP, "ground")
    for name, _, (dx, _, dz), half in PIECES:
        if name == "station":
            continue
        ground.rect(dx - half, dz - half, dx + half, dz + half, 0, DECK_TOP + 1, "plinth")
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
        row["footprint"] = (max(c[0] for c in voxels) - min(c[0] for c in voxels) + 1,
                            max(c[1] for c in voxels) - min(c[1] for c in voxels) + 1,
                            max(c[2] for c in voxels) - min(c[2] for c in voxels) + 1)
        table.append(row)
    return layers, table


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sculpture"
    os.makedirs(out, exist_ok=True)

    layers, table = build()
    document = board.layout(layers, THEMES, map_theme="ground", mirror="none")
    json.dump(document, open(f"{out}/sculpture.layout.json", "w"), indent=1)

    print(f"{'model':<10} {'size (x,y,z)':>16} {'blocks':>8} {'layers':>7} {'shapes':>7} {'blk/shape':>10}")
    for row in table:
        size = "x".join(str(v) for v in row["footprint"])
        print(f"{row['model']:<10} {size:>16} {row['blocks']:>8} {row['layers']:>7} "
              f"{row['shapes']:>7} {row['blocks_per_shape']:>10}")
    print(f"{'BOARD':<10} {'':>16} {'':>8} {len(layers):>7} "
          f"{sum(len(l['layout']['shapes']) for l in layers):>7}")

    board.store("sculpture-gallery", "Sculpture Gallery", document)
    payload = board.columns("sculpture-gallery", document)
    json.dump(payload, open(f"{out}/sculpture.columns.json", "w"))

    import iso
    iso.isometric(payload, f"{out}/sculpture-iso.png", scale=4,
                  title="four solids compiled into sketch layers",
                  caption="every block here is a rectangle on a layer of one sketch document")
    for name, make, (dx, dy, dz), half in PIECES:
        # Clipped to the piece's own box: the gallery is one board, and a neighbour's solar wing reaching
        # over a plinth is a fact about the board rather than about the piece being photographed.
        cells = make()
        clip = (dx + min(c[0] for c in cells) - 4, dx + max(c[0] for c in cells) + 4,
                dy - 1, dy + max(c[1] for c in cells) + 2,
                dz + min(c[2] for c in cells) - 4, dz + max(c[2] for c in cells) + 4)
        iso.isometric(payload, f"{out}/{name}-iso.png", scale=7, clip=clip, title=name, quarter=2)
        iso.elevation(payload, f"{out}/{name}-front.png", face="north", scale=7, clip=clip,
                      title=f"{name} - north elevation")
        iso.exploded(payload, f"{out}/{name}-layers.png", scale=4, clip=clip, quarter=2,
                     title=f"{name} - one panel per sketch layer",
                     order=[l for l in payload["layers"] if l.startswith(f"{name}-L")])
    print("rendered", out)
