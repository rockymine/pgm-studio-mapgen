"""Cut a box out of a world into a voxel model a spec can carry as a made thing.

    python3 tools/lift.py <region> <name> --box x0 y0 z0 x1 y1 z1 --out specs/<slug>/models
                          [--against <region>] [--ground-below <y>] [--drop 8,9,18] [--keep-trees]
                          [--cost] [--plan]

The model is written as `<out>/<name>.json`, rows of `[x, y, z, id, data]` in world coordinates, which is
the shape a spec's `build.py` reads back with `model()` and hands to `tools/sculpt/layers.py` as
`addLayers`. Water and trees are dropped unless asked for, because a build is cut out of a world that has
both around it. `--against` keeps only the blocks the other world does not have at the same position —
what the person added — which is how a statue is cut out of the island it stands on. `--ground-below`
drops the terrain body at and under a height, for a build whose footing sits in ground the other world
also has. `--cost` compiles the model with the run-index compiler and prints what it costs in layers and
shapes, which is the number that decides whether the thing is worth carrying. `--plan` prints the box as
a plan of top blocks, one character per column, for both worlds, so a build can be read before it is cut.
"""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from anvil import World, TREE, WATER, name  # noqa: E402

GROUND = {1, 2, 3, 4, 12, 13, 48, 129, 159, 168, 5}
PLAN_CHARS = {0: ".", 98: "b", 45: "B", 5: "p", 108: "r", 109: "r", 43: "S", 44: "s", 126: "s", 1: "a",
              4: "k", 42: "I", 35: "w", 7: "X", 139: "|", 30: "~", 85: "f", 17: "L", 18: "l", 162: "L",
              161: "l", 2: "g", 3: "d", 20: "G", 102: "G", 160: "G", 95: "G", 54: "C", 47: "K", 171: "c",
              140: "o", 144: "h", 64: "D", 96: "T", 53: "r", 134: "r", 135: "r", 67: "r", 156: "r", 24: "n",
              49: "O", 89: "*", 50: "!", 72: "_", 101: "#", 65: "H", 129: "e", 159: "C", 48: "m", 41: "$",
              8: "≈", 9: "≈"}


def option(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def plan(world, box, title):
    x0, y0, z0, x1, y1, z1 = box
    print(f"\n{title}: x {x0}..{x1} across, z {z0}..{z1} down, top block between y {y0} and {y1}")
    print("  key: X spawn room  b/B/p masonry, brick, planks  r stairs  s slabs  w wool  L/l trees  g/d ground  . nothing")
    for z in range(z0, z1 + 1):
        line = ""
        for x in range(x0, x1 + 1):
            top = None
            for y in range(y1, y0 - 1, -1):
                block = world.get(x, y, z)
                if block[0] and block[0] not in TREE:
                    top = block
                    break
            line += PLAN_CHARS.get(top[0], "?") if top else "."
        print(f"  z{z:5} {line}")


def main():
    if len(sys.argv) < 3 or "--box" not in sys.argv:
        raise SystemExit(__doc__)
    region, model_name = sys.argv[1], sys.argv[2]
    at = sys.argv.index("--box")
    box = [int(v) for v in sys.argv[at + 1:at + 7]]
    x0, y0, z0, x1, y1, z1 = box
    out_dir = option("--out")
    if not out_dir:
        raise SystemExit("lift: --out <dir> is required — a spec's models/, never a map's own folder")
    against = option("--against")
    ground_below = option("--ground-below")
    dropped = {int(v) for v in option("--drop", "").split(",") if v}
    dropped |= WATER
    if "--keep-trees" not in sys.argv:
        dropped |= TREE

    world = World(region)
    other = World(against) if against else None
    if "--plan" in sys.argv:
        plan(world, box, f"{region}")
        if other:
            plan(other, box, f"{against}")

    body = {}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(y0, y1 + 1):
                block = world.get(x, y, z)
                if block[0] == 0 or block[0] in dropped:
                    continue
                if other is not None and other.get(x, y, z) == block:
                    continue
                if ground_below is not None and y <= int(ground_below) and block[0] in GROUND:
                    continue
                body[(x, y, z)] = block
    if not body:
        raise SystemExit(f"{model_name}: nothing in the box after the drops")
    counted = Counter(body.values())
    xs = [p[0] for p in body]
    ys = [p[1] for p in body]
    zs = [p[2] for p in body]
    print(f"\n{model_name}: {len(body)} blocks, x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} z{min(zs)}..{max(zs)}")
    print("  " + ", ".join(f"{name(b)} {n}" for b, n in counted.most_common(12)))

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{model_name}.json")
    rows = [[x, y, z, i, d] for (x, y, z), (i, d) in sorted(body.items(), key=lambda kv: (kv[0][1], kv[0][2], kv[0][0]))]
    with open(path, "w") as handle:
        json.dump(rows, handle)
    print(f"  wrote {path}")

    if "--cost" in sys.argv:
        sys.path.insert(0, os.path.join(HERE, "sculpt"))
        from layers import compile_layers, stats  # noqa: E402
        voxels = {p: f"m-{i}-{d}" for p, (i, d) in body.items()}
        layers = compile_layers(voxels, prefix=model_name + "-", layer_prefix=model_name + "-L", part_of=model_name)
        cost = stats(voxels, layers)
        print(f"  as a made thing: {cost['blocks']} blocks, {cost['layers']} layers, {cost['shapes']} shapes,"
              f" {cost['materials']} materials")


if __name__ == "__main__":
    main()
