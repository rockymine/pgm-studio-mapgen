"""Cut the board's two species out of rockymine's hand-built tree showcase (corpus/tree-showcase), each as
its blocks relative to its foot, so dressing.py can plant them whole. Run once; writes trees.json.

    python3 cut_trees.py <pgm-studio-mapgen root> <out.json>

Cloudhaven takes two species for a fantastical sky board: the willow (r17), whose hanging crown reads as
a floating island's beard, and the dense oak (r11), whose full crowns sit on the small islands.
"""
import json
import os
import sys

root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "tools"))
from anvil import World, WOOD  # noqa: E402
from trees import bodies_in, foot_of, TREE_BLOCKS  # noqa: E402

KINDS = {
    "willow": [87, 88, 89, 90, 91],
    "dense-oak": [50, 51, 52, 53, 56, 57, 58],
    "small-dense-oak": [54, 55],
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
