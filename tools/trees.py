"""Hand-built trees: catalogue a world's, match planted ones back to their originals, cut bodies for a spec,
and verify a built world planted them block for block.

    python3 tools/trees.py catalogue <region> [--min 8] [--json <out>]
    python3 tools/trees.py match <catalogue-region> <planted-region> [--against <original-region>] [--min 20]
    python3 tools/trees.py bodies <region> --row <z>=<prefix> [--row ...] [--all] --out <trees.json>
    python3 tools/trees.py verify <region> <trees.json> [--min 20]

A tree is a 26-connected body of wood, leaves and the carpentry a hand-built tree carries (slabs, stairs,
fences, vines), whose foot is its lowest log. `catalogue` lists every tree standing in a world — a showcase
of trees on platforms, or a finished board — with its foot, its box, its block count and its log count.
`match` takes every tree body in a planted world that the original world lacks (or every body, with no
`--against`) and finds the catalogue tree it is, comparing leaf shapes alone under the eight symmetries of
the square, so a tree pasted with a rotation is still found; the match is a Jaccard score, and 0.99 or
better is the same tree. `bodies` cuts a showcase row into copied-tree bodies keyed `<prefix>-<n>` west to
east, each as `[dx, dy, dz, id, data]` from its foot, which is the `body` a `copied` tree recipe carries;
`--all` cuts every tree as `tree-<n>` instead. `verify` finds every tree body in a built world and reports
whether it is one of the file's bodies block for block, under identity or a half turn, and what data bits
the leaves carry, which is how a drive is checked to have planted what the spec named.

`pgm-studio/tools/seed-trees.cs` cuts the same bodies straight into the studio's library; this tool makes
the file a spec's `build.py` reads, and the reads a review needs.
"""
import json
import os
import sys
from collections import Counter, deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anvil import World, WOOD, LEAF, CARPENTRY, name  # noqa: E402

TREE_BLOCKS = WOOD | LEAF | CARPENTRY | {35}
N26 = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0)]
SYMMETRIES = {"none": lambda x, z: (x, z), "rot 90": lambda x, z: (-z, x), "rot 180": lambda x, z: (-x, -z),
              "rot 270": lambda x, z: (z, -x), "mirror x": lambda x, z: (-x, z), "mirror z": lambda x, z: (x, -z),
              "diagonal": lambda x, z: (z, x), "antidiagonal": lambda x, z: (-z, -x)}


def option(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def bodies_in(voxels, minimum, against=None, blocks=TREE_BLOCKS):
    """Every tree body in `voxels`, as lists of cells, west to east by row. With `against`, only the blocks the
    other world does not carry at that position count, so grown trees the original had are not bodies;
    `blocks` is what counts as a tree — wood and leaves alone when a world also holds builds in wool, fences
    and slabs, which would otherwise read as trees with no leaves."""
    tree = {p: v for p, v in voxels.items() if v[0] in blocks and (against is None or against.get(p) != v)}
    seen = set()
    found = []
    for start in tree:
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        cells = []
        while queue:
            point = queue.popleft()
            cells.append(point)
            for dx, dy, dz in N26:
                neighbour = (point[0] + dx, point[1] + dy, point[2] + dz)
                if neighbour in tree and neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        if len(cells) >= minimum:
            found.append(cells)
    found.sort(key=lambda cells: (min(p[2] for p in cells), min(p[0] for p in cells)))
    return found


def foot_of(cells, voxels):
    logs = [p for p in cells if voxels[p][0] in WOOD]
    return min(logs or cells, key=lambda p: (p[1], p[0], p[2]))


def leaf_shape(cells, voxels, turn=SYMMETRIES["none"]):
    """The leaf cells of a body, turned and normalised to their own corner: what two trees are compared on."""
    points = []
    for (x, y, z) in cells:
        if voxels[(x, y, z)][0] in LEAF:
            tx, tz = turn(x, z)
            points.append((tx, y, tz))
    if not points:
        return frozenset()
    mx = min(p[0] for p in points)
    my = min(p[1] for p in points)
    mz = min(p[2] for p in points)
    return frozenset((x - mx, y - my, z - mz) for x, y, z in points)


def jaccard(a, b):
    return len(a & b) / max(1, len(a | b))


def describe(k, cells, voxels):
    foot = foot_of(cells, voxels)
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    zs = [p[2] for p in cells]
    counted = Counter(voxels[p] for p in cells)
    logs = sum(1 for p in cells if voxels[p][0] in WOOD)
    return {"k": k, "foot": list(foot), "box": [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)],
            "blocks": len(cells), "logs": logs,
            "census": {name(b): n for b, n in counted.most_common()}}


def catalogue():
    world = World(sys.argv[2])
    voxels = world.voxels()
    minimum = int(option("--min", 8))
    found = bodies_in(voxels, minimum)
    print(f"{len(found)} trees of {minimum}+ blocks in {sys.argv[2]}")
    listed = []
    for k, cells in enumerate(found):
        row = describe(k, cells, voxels)
        listed.append(row)
        box = row["box"]
        print(f"{k:3} foot ({row['foot'][0]},{row['foot'][1]},{row['foot'][2]})"
              f"  {box[3] - box[0] + 1}x{box[4] - box[1] + 1}x{box[5] - box[2] + 1}"
              f"  blocks {row['blocks']:4}  logs {row['logs']:3}  "
              + ", ".join(f"{b} {n}" for b, n in list(row["census"].items())[:4]))
    if out := option("--json"):
        with open(out, "w") as handle:
            json.dump(listed, handle, indent=0)
        print(f"wrote {out}")


def match():
    catalogue_world = World(sys.argv[2])
    planted_world = World(sys.argv[3])
    original = World(against).voxels() if (against := option("--against")) else None
    minimum = int(option("--min", 20))
    catalogue_voxels = catalogue_world.voxels()
    planted_voxels = planted_world.voxels()
    reference = []
    for k, cells in enumerate(bodies_in(catalogue_voxels, minimum)):
        reference.append({"k": k, "foot": foot_of(cells, catalogue_voxels), "blocks": len(cells),
                          "logs": sum(1 for p in cells if catalogue_voxels[p][0] in WOOD),
                          "shapes": {label: leaf_shape(cells, catalogue_voxels, turn) for label, turn in SYMMETRIES.items()}})
    planted = bodies_in(planted_voxels, minimum, original, WOOD | LEAF)
    print(f"{len(reference)} catalogue trees; {len(planted)} planted bodies of wood and leaves"
          f"{' the original does not have' if original else ''}")
    used = Counter()
    for cells in planted:
        shape = leaf_shape(cells, planted_voxels)
        best = (0.0, None, None)
        for tree in reference:
            for label, candidate in tree["shapes"].items():
                score = jaccard(candidate, shape)
                if score > best[0]:
                    best = (score, tree, label)
        score, tree, label = best
        foot = foot_of(cells, planted_voxels)
        logs = sum(1 for p in cells if planted_voxels[p][0] in WOOD)
        if tree is None or not shape:
            print(f"  planted at ({foot[0]},{foot[1]},{foot[2]}) blocks {len(cells):4} logs {logs:3}  no leaves to match on")
            continue
        used[tree["k"]] += 1
        print(f"  planted at ({foot[0]:4},{foot[1]:2},{foot[2]:4}) blocks {len(cells):4} logs {logs:3}"
              f"  -> catalogue #{tree['k']:2} at {tuple(tree['foot'])} blocks {tree['blocks']:4} logs {tree['logs']:3}"
              f"  {label:12} match {score:.2f}")
    print("catalogue trees used, by index: " + ", ".join(f"#{k} x{n}" for k, n in sorted(used.items())))


def bodies():
    world = World(sys.argv[2])
    voxels = world.voxels()
    out = option("--out")
    if not out:
        raise SystemExit("bodies: --out <trees.json> is required")
    rows = [(int(spec.split("=")[0]), spec.split("=")[1]) for i, spec in enumerate(sys.argv) if sys.argv[i - 1] == "--row"]
    found = bodies_in(voxels, 8)
    standing = []
    for cells in found:
        foot = foot_of(cells, voxels)
        rests = any(voxels.get((foot[0], foot[1] - k, foot[2]), (0, 0))[0] not in TREE_BLOCKS | {0} for k in (1, 2))
        if rests and any(voxels[p][0] in WOOD for p in cells):
            standing.append((foot, cells))
    written = {}

    def cut(key, foot, cells):
        body = sorted([[c[0] - foot[0], c[1] - foot[1], c[2] - foot[2], voxels[c][0], voxels[c][1]] for c in cells],
                      key=lambda r: (r[1], r[2], r[0]))
        written[key] = {"foot": list(foot), "body": body}
        print(f"  {key}: foot {foot}, {len(body)} blocks, {max(r[1] for r in body) + 1} tall")

    if "--all" in sys.argv:
        for n, (foot, cells) in enumerate(sorted(standing, key=lambda t: (t[0][2], t[0][0])), 1):
            cut(f"tree-{n}", foot, cells)
    for band, prefix in rows:
        row = sorted([t for t in standing if abs(t[0][2] - band) <= 3], key=lambda t: t[0][0])
        print(f"row z={band} as {prefix}-*: {len(row)} trees")
        for n, (foot, cells) in enumerate(row, 1):
            cut(f"{prefix}-{n}", foot, cells)
    if not written:
        raise SystemExit("bodies: nothing cut — state --row <z>=<prefix> for each showcase row, or --all")
    with open(out, "w") as handle:
        json.dump(written, handle)
    print(f"wrote {out}: {len(written)} bodies out of {len(standing)} standing trees")


def verify():
    world = World(sys.argv[2])
    with open(sys.argv[3]) as handle:
        named = json.load(handle)
    minimum = int(option("--min", 20))
    voxels = world.voxels()
    turns = {"none": SYMMETRIES["none"], "rot 180": SYMMETRIES["rot 180"]}

    def normalised(rows, turn):
        points = []
        for (x, y, z), (i, d) in rows:
            tx, tz = turn(x, z)
            points.append((tx, y, tz, i, d & 7 if i in LEAF else d))
        mx = min(p[0] for p in points)
        my = min(p[1] for p in points)
        mz = min(p[2] for p in points)
        return frozenset((x - mx, y - my, z - mz, i, d) for x, y, z, i, d in points)

    reference = {}
    for key, tree in named.items():
        rows = [((x, y, z), (i, d)) for x, y, z, i, d in tree["body"]]
        for label, turn in turns.items():
            reference[(key, label)] = normalised(rows, turn)
    planted = bodies_in(voxels, minimum, blocks=WOOD | LEAF)
    exact = 0
    print(f"{len(planted)} bodies of wood and leaves in {sys.argv[2]}")
    for cells in planted:
        got = normalised([(p, voxels[p]) for p in cells], turns["none"])
        (key, label), shape = max(reference.items(), key=lambda kv: jaccard(kv[1], got))
        score = jaccard(shape, got)
        exact += score >= 0.999
        foot = foot_of(cells, voxels)
        print(f"  at ({foot[0]:4},{foot[1]:2},{foot[2]:4}) blocks {len(cells):4}  {key:14} {label:8} {score:.3f}"
              f"{'' if score >= 0.999 else '   (a grove, or clipped)'}")
    print(f"exact copies: {exact} of {len(planted)}")
    leaves = [v[1] for v in voxels.values() if v[0] in LEAF]
    no_decay = sum(1 for d in leaves if d & 4)
    check = sum(1 for d in leaves if d & 8)
    print(f"leaves: {len(leaves)}, no-decay {no_decay}, carrying the check bit {check}")


COMMANDS = {"catalogue": catalogue, "match": match, "bodies": bodies, "verify": verify}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in COMMANDS:
        raise SystemExit(__doc__)
    COMMANDS[sys.argv[1]]()
