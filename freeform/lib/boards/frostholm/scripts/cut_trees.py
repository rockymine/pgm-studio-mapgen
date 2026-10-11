"""Cut the board's two species out of rockymine's hand-built tree showcase (corpus/tree-showcase), each as
its blocks relative to its foot, so dressing.py can plant them whole. Run once; writes trees.json.

    python3 cut_trees.py <pgm-studio-mapgen root> <out.json>

Frostholm takes the cold board's two species: pine (r2, r3 large-pine) and spruce (r7 tall-spruce without
the sequoia, r4 tiny-spruce), the rows corpus/README.md names.
"""
import json
import os
import sys

root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "tools"))
from anvil import World, WOOD  # noqa: E402
from trees import bodies_in, foot_of, TREE_BLOCKS  # noqa: E402

KINDS = {
    "pine": [3, 4, 6, 7, 8],
    "spruce": [26, 27, 29, 30, 31, 32, 33],
    "tiny-spruce": [9, 10, 11, 12, 13],
}

world = World(os.path.join(root, "corpus", "tree-showcase", "region"))
vox = world.voxels()
found = bodies_in(vox, 8)
out = {}
for kind, idxs in KINDS.items():
    out[kind] = []
    for k in idxs:
        cells = found[k]
        fx, fy, fz = foot_of(cells, vox)
        blocks = [[x - fx, y - fy, z - fz, vox[(x, y, z)][0], vox[(x, y, z)][1]] for x, y, z in cells]
        reach = max(max(abs(b[0]), abs(b[2])) for b in blocks if b[3] in (18, 161))
        out[kind].append({"source": k, "blocks": blocks, "crown": reach,
                          "height": max(b[1] for b in blocks)})
        print(kind, k, len(blocks), "crown", reach)
with open(sys.argv[2], "w") as f:
    json.dump(out, f)
