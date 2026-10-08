"""Draw the pictures that show Calcite: the studio's round-trip reads over the region files, isometric views,
true-scale sections through every route, and elevations.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

import render_iso

build, root, rt = sys.argv[1], sys.argv[2], sys.argv[3]
region = os.path.join(root, "world", "region")
mapxml = os.path.join(root, "world", "map.xml")
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)


def run(args):
    r = subprocess.run(rt.split() + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", " ".join(args), r.stderr[-600:])


def o(name):
    return os.path.join(out, name)


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "5"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "5"])
for name, args in [("10-section-west-east-z-1", ["--x", "-60", "59", "--z", "-1", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"]),
                   ("11-section-north-south-x-1", ["--z", "-48", "47", "--x", "-1", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"]),
                   ("12-section-spring-tunnel-x6", ["--z", "-48", "47", "--x", "6", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"]),
                   ("13-section-stairwell-z4", ["--x", "-60", "59", "--z", "4", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"]),
                   ("14-section-north-hill-z-30", ["--x", "-60", "59", "--z", "-30", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"]),
                   ("15-section-spawn-tunnel-x-50", ["--z", "-48", "47", "--x", "-50", "--ymin", "0", "--ymax", "32", "--depth", "1", "--scale", "5"])]:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-quarry-se.png"), 3, "se", None, 0, 27)
render_iso.render(ids, dat, x0, z0, o("31-iso-quarry-nw.png"), 3, "nw", None, 0, 27)
render_iso.render(ids, dat, x0, z0, o("32-iso-north-hill.png"), 6, "se", (-22, -46, 21, -14), 0, 27)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-middle.png"), 6, "sw", (-24, -24, 23, 23), 0, 22)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-spring-cut-at-18.png"), 6, "se", (-16, -28, 15, 27), 0, 12)
render_iso.render(ids, dat, x0, z0, o("35-iso-north-east-corner.png"), 6, "sw", (0, -42, 46, 0), 0, 27)
render_iso.render(ids, dat, x0, z0, o("36-iso-red-spawn.png"), 6, "se", (-52, -14, -32, 13), 0, 27)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-north-hill-from-the-middle.png"), (-20, -46, 19, -10), 6, 30, "north", 8)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-the-middle-from-the-west.png"), (-30, -24, 0, 23), 4, 26, "east", 8)
print("renders written to", out)
