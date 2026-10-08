"""Draw the pictures that show Gullhaven: the studio's round-trip reads over the region files, true-scale
sections, isometric views of each part of the island, and the caves cut open.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "5"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "5"])
for name, args in [("10-section-west-east-z-32", ["--x", "-56", "55", "--z", "-32", "--ymin", "10", "--ymax", "64", "--depth", "1", "--scale", "5"]),
                   ("11-section-north-south-x22", ["--z", "-50", "68", "--x", "22", "--ymin", "10", "--ymax", "50", "--depth", "1", "--scale", "5"]),
                   ("12-section-the-caves-z-24", ["--x", "-56", "0", "--z", "-24", "--ymin", "14", "--ymax", "46", "--depth", "1", "--scale", "7"]),
                   ("13-section-the-sinkhole-x-20", ["--z", "-30", "12", "--x", "-20", "--ymin", "14", "--ymax", "36", "--depth", "1", "--scale", "7"]),
                   ("14-section-the-skerry-x-14", ["--z", "20", "68", "--x", "-14", "--ymin", "10", "--ymax", "36", "--depth", "1", "--scale", "7"])]:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-island-se.png"), 3, "se", None, 0, 72)
render_iso.render(ids, dat, x0, z0, o("31-iso-island-nw.png"), 3, "nw", None, 0, 72)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-town.png"), 5, "sw", (-4, -50, 52, 10), 0, 72)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-headland.png"), 5, "se", (-56, -50, -4, -10), 0, 72)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-harbour.png"), 5, "nw", (4, 4, 52, 50), 0, 72)
render_iso.render(ids, dat, x0, z0, o("35-iso-the-downs-and-skerry.png"), 4, "ne", (-56, -12, 12, 68), 0, 72)
render_iso.render(ids, dat, x0, z0, o("36-iso-the-caves-cut-at-24.png"), 6, "se", (-50, -36, -8, 10), 0, 24)
render_iso.render(ids, dat, x0, z0, o("37-iso-the-ravine.png"), 6, "sw", (-20, -50, 4, -14), 0, 50)

render_iso.render(ids, dat, x0, z0, o("38-iso-the-headland-cliffs-nw.png"), 6, "nw", (-56, -50, -8, -10), 0, 72)
render_iso.render(ids, dat, x0, z0, o("39-iso-the-east-cliffs-ne.png"), 5, "ne", (10, -50, 55, 20), 0, 72)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-the-north-shore.png"), (-56, -50, 55, -20), 12, 50, "south", 5)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-the-west-shore.png"), (-56, -50, -30, 68), 12, 50, "east", 5)
print("renders written to", out)
