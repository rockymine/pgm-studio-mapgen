"""Draw the pictures that show Cloudhaven: the studio's round-trip reads over the written region files, and
the isometric and elevation views over the generated volume.

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
mapxml = os.path.join(world, "map.xml")
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)


def run(args):
    r = subprocess.run(rt.split() + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", " ".join(args), r.stderr[-400:])


def o(name):
    return os.path.join(out, name)


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--map", mapxml, "--scale", "3"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3", "--contour", "4"])
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "3"])
SECTIONS = [
    ("10-section-spawn-to-spawn-z0", ["--x", "-132", "131", "--z", "0", "--ymin", "20", "--ymax", "120", "--depth", "1", "--scale", "3"]),
    ("11-section-lantern-isle-z-60", ["--x", "-100", "-40", "--z", "-60", "--ymin", "30", "--ymax", "100", "--depth", "1", "--scale", "6"]),
    ("12-section-gardens-z59", ["--x", "-100", "-40", "--z", "59", "--ymin", "20", "--ymax", "90", "--depth", "1", "--scale", "6"]),
    ("13-section-albatross-x-40", ["--z", "-70", "10", "--x", "-40", "--ymin", "40", "--ymax", "100", "--depth", "1", "--scale", "5"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-board-sw.png"), 2, "sw")
render_iso.render(ids, dat, x0, z0, o("33-iso-red-half.png"), 3, "se", (-132, -100, -1, 99))
render_iso.render(ids, dat, x0, z0, o("34-iso-highmoor-keep.png"), 5, "se", (-132, -26, -86, 26), 40)
render_iso.render(ids, dat, x0, z0, o("35-iso-lantern-isle-gazebo.png"), 6, "se", (-90, -78, -54, -42), 40)
render_iso.render(ids, dat, x0, z0, o("36-iso-hanging-gardens.png"), 5, "se", (-96, 34, -52, 78), 20)
render_iso.render(ids, dat, x0, z0, o("37-iso-port-albatross.png"), 4, "se", (-76, -66, -20, 26), 30)
render_iso.render(ids, dat, x0, z0, o("38-iso-concord.png"), 5, "se", (-34, -16, 33, 15), 40)
render_iso.render(ids, dat, x0, z0, o("39-iso-north-flank-balloons.png"), 5, "se", (-34, -90, 34, -58), 30)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-board-from-south.png"), (-132, -100, 131, 99), 10, 120, "north", 3)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-concord-from-south.png"), (-34, -8, 33, 8), 50, 100, "north", 6)
print("renders written to", out)
