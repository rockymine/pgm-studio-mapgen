"""Draw the pictures that show Riad: the studio's round-trip reads over the region files, true-scale sections
through each post and down the axis, isometric views, and elevations.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

import render_iso

build, root, rt = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(root, "..", "..", "tools"))
import worlds  # noqa: E402
world = worlds.of(root)
region = os.path.join(world, "region")
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
for name, args in [("10-section-north-south-x0", ["--z", "-61", "61", "--x", "0", "--ymin", "4", "--ymax", "40", "--depth", "1", "--scale", "5"]),
                   ("11-section-west-east-z0", ["--x", "-49", "48", "--z", "0", "--ymin", "4", "--ymax", "40", "--depth", "1", "--scale", "6"]),
                   ("12-section-swim-column-z2", ["--x", "-12", "12", "--z", "2", "--ymin", "8", "--ymax", "30", "--depth", "1", "--scale", "10"]),
                   ("13-section-porch-stairs-x-26", ["--z", "-20", "20", "--x", "-26", "--ymin", "10", "--ymax", "30", "--depth", "1", "--scale", "8"]),
                   ("14-section-spawn-house-x0", ["--z", "36", "61", "--x", "0", "--ymin", "10", "--ymax", "40", "--depth", "1", "--scale", "8"]),
                   ("15-section-arcade-x11", ["--z", "-61", "61", "--x", "11", "--ymin", "10", "--ymax", "32", "--depth", "1", "--scale", "5"])]:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-riad-se.png"), 3, "se", None, 0, 40)
render_iso.render(ids, dat, x0, z0, o("31-iso-riad-nw.png"), 3, "nw", None, 0, 40)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-cistern.png"), 7, "se", (-16, -16, 16, 16), 0, 30)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-mirador.png"), 6, "sw", (-49, -18, -14, 18), 0, 30)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-minaret.png"), 6, "se", (16, -18, 48, 18), 0, 30)
render_iso.render(ids, dat, x0, z0, o("35-iso-blue-half.png"), 4, "nw", (-37, 14, 37, 61), 0, 40)
render_iso.render(ids, dat, x0, z0, o("36-iso-blue-spawn-cut-at-31.png"), 7, "nw", (-15, 42, 15, 60), 0, 31)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-the-mirador-from-the-south.png"), (-49, -20, -15, 20), 10, 32, "north", 8)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-the-court-from-blue.png"), (-30, -16, 30, 30), 10, 32, "north", 6)
print("renders written to", out)
