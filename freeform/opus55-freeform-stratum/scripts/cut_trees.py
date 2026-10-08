"""Cut the board's two species out of rockymine's hand-built tree showcase (corpus/tree-showcase), each as
its blocks relative to its foot, so dressing.py can plant them whole. Run once; writes trees.json.

    python3 cut_trees.py <pgm-studio-mapgen root> <out.json>

The kinds are the showcase's own rows (corpus/README.md): r6 tiny-oak, r9/r12/r14 oak, r20 large-oak,
r13 birch. The dense oaks (r11) are left out on purpose: their crowns are the widest in the corpus and read
as one mass when planted together.
"""
import json
import os
import sys

root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "tools"))
from anvil import World, WOOD  # noqa: E402
from trees import bodies_in, foot_of, TREE_BLOCKS  # noqa: E402

KINDS = {
    "tiny-oak": [17, 18, 19, 20, 21, 22, 23, 25],
    "oak": [41, 42, 43, 44, 59, 60, 62, 63, 64],
    "big-oak": [79, 99],
    "birch": [69, 70, 71, 72, 73, 74, 75, 76, 77, 78],
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
