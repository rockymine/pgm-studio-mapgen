"""Draw the pictures that show Frostholm: the studio's round-trip reads over the written region files, and
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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--map", mapxml, "--scale", "4"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "4", "--contour", "3", "--water"])
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "4"])
SECTIONS = [
    ("10-section-beacon-z-67", ["--x", "-40", "10", "--z", "-67", "--ymin", "36", "--ymax", "96", "--depth", "1", "--scale", "8"]),
    ("11-section-holmstein-lake-z-20", ["--x", "-90", "-40", "--z", "-20", "--ymin", "36", "--ymax", "76", "--depth", "1", "--scale", "8"]),
    ("12-section-diagonal-spawn-to-spawn-z0", ["--x", "-90", "89", "--z", "0", "--ymin", "30", "--ymax", "90", "--depth", "1", "--scale", "4"]),
    ("13-section-hall-z-64", ["--x", "-90", "-40", "--z", "-64", "--ymin", "40", "--ymax", "90", "--depth", "1", "--scale", "8"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-red-home.png"), 4, "se", (-90, -90, -10, -10), 40)
render_iso.render(ids, dat, x0, z0, o("33-iso-skarvik-tingholm.png"), 5, "se", (-42, -40, 6, 8), 40)
render_iso.render(ids, dat, x0, z0, o("34-iso-beacon-whaler.png"), 5, "se", (-44, -76, 0, -30), 40)
render_iso.render(ids, dat, x0, z0, o("35-iso-kaldvatn-holmstein.png"), 5, "se", (-90, -48, -44, -4), 40)
render_iso.render(ids, dat, x0, z0, o("36-iso-hall-crags.png"), 5, "se", (-90, -90, -46, -50), 40)
render_iso.render(ids, dat, x0, z0, o("37-iso-kraakodde.png"), 5, "se", (16, -80, 60, -36), 40)
render_iso.render(ids, dat, x0, z0, o("38-iso-board-sw.png"), 2, "sw")
render_iso.elevation(ids, dat, x0, z0, o("50-elev-beacon-from-south.png"), (-32, -69, -2, -40), 40, 96, "north", 6)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-hall-from-east.png"), (-80, -76, -40, -52), 44, 90, "west", 6)
print("renders written to", out)
