"""Draw the pictures that show Penstock: the studio's round-trip reads over the region files, cutaway isometric
views at each level, plan slices and elevations.

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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "4"])   # the studio does not parse TDM maps
for name, args in [("10-section-long-z0", ["--x", "-72", "71", "--z", "-1", "--ymin", "0", "--ymax", "40", "--depth", "1", "--scale", "4"]),
                   ("11-section-across-hall-x-20", ["--z", "-50", "49", "--x", "-20", "--ymin", "0", "--ymax", "40", "--depth", "1", "--scale", "5"]),
                   ("12-section-penstock-z-26", ["--x", "-72", "71", "--z", "-26", "--ymin", "0", "--ymax", "40", "--depth", "1", "--scale", "4"]),
                   ("13-section-score-boxes-x-58", ["--z", "-50", "49", "--x", "-58", "--ymin", "10", "--ymax", "40", "--depth", "1", "--scale", "5"])]:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-station-se.png"), 3, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-cut-at-the-catwalks-se.png"), 3, "se", ymax=30)
render_iso.render(ids, dat, x0, z0, o("32-iso-cut-at-the-floor-sw.png"), 3, "sw", ymax=26)
render_iso.render(ids, dat, x0, z0, o("33-iso-red-half-cut-sw.png"), 5, "sw", (-72, -50, 6, 49), 0, 33)
render_iso.render(ids, dat, x0, z0, o("34-iso-gatehouse-and-boxes.png"), 6, "se", (-72, -42, -40, 41), 0, 31)
render_iso.render(ids, dat, x0, z0, o("35-iso-exciter-and-generators.png"), 6, "se", (-32, -26, 31, 25), 12, 35)
render_iso.render(ids, dat, x0, z0, o("36-iso-penstocks-only.png"), 5, "se", (-72, -50, 71, 49), 0, 19)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-back-wall-from-the-hall.png"), (-60, -48, -44, 47), 18, 37, "west", 6)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-hall-across.png"), (-44, -48, 43, 47), 18, 37, "north", 5)
render_iso.elevation(ids, dat, x0, z0, o("60-elev-station-outside.png"), (-72, -50, 71, 49), 0, 40, "north", 4)
print("renders written to", out)
