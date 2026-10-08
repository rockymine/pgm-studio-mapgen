"""Draw Loomfall: the studio's round-trip reads, the carpets over the city, the stack from two sides, each carpet
from above, and the stack in section.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

import cutaway
import render_iso

build, root, rt = sys.argv[1], sys.argv[2], sys.argv[3]
region = os.path.join(root, "world", "region")
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)


def run(args):
    r = subprocess.run(rt.split() + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", " ".join(args), r.stderr[-600:])


def o(name):
    return os.path.join(out, name)


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "3"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3"])
cutaway.cut(build, o("10-cutaway-north-south.png"), [(0, -60), (0, 60)], ymin=0, ymax=210, scale=4,
            title="10. NORTH TO SOUTH at x 0, true scale: the five carpets, the kill height's gap, the city")
cutaway.cut(build, o("11-cutaway-west-east.png"), [(-60, 2), (60, 2)], ymin=0, ymax=210, scale=4,
            title="11. WEST TO EAST at z 2, true scale")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-the-carpets-over-the-city.png"), 2, "sw", None, 0, 229)
render_iso.render(ids, dat, x0, z0, o("31-iso-the-stack-sw.png"), 5, "sw", (-30, -30, 30, 30), 120, 200)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-stack-ne.png"), 5, "ne", (-30, -30, 30, 30), 120, 200)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-city.png"), 3, "sw", None, 0, 110)
for k, y in enumerate((196, 182, 166, 148, 128)):
    render_iso.render(ids, dat, x0, z0, o(f"4{k}-iso-carpet-{k + 1}.png"), 6, "sw", (-30, -30, 30, 30), y, y)
print("renders written to", out)
