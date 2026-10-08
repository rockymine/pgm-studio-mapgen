"""Hollowcrown's two species, taken from the trees already cut from rockymine's tree showcase for the
earlier freeform boards: oak (r9/r12/r14) and tiny oak (r6) from Riftwater's cut, for the valley and the
town's gardens; spruce (r7 tall-spruce) and tiny spruce (r4) from Frostholm's cut, for the mountain.

    python3 cut_trees.py <freeform root> <out.json>
"""
import json
import os
import sys

root = sys.argv[1]
a = json.load(open(os.path.join(root, "opus55-freeform-riftwater", "scripts", "trees.json")))
b = json.load(open(os.path.join(root, "opus55-freeform-frostholm", "scripts", "trees.json")))
out = {"oak": a["oak"], "tiny-oak": a["tiny-oak"], "spruce": b["spruce"], "tiny-spruce": b["tiny-spruce"]}
json.dump(out, open(sys.argv[2], "w"))
print({k: len(v) for k, v in out.items()})
