"""Draw the pictures that show Lantern Karst: the studio's round-trip reads over the written region files, and
isometric views and elevations of the volume.

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
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "3"])
SECTIONS = [
    ("10-section-spawn-to-spawn-x0", ["--z", "-127", "127", "--x", "0", "--ymin", "20", "--ymax", "100", "--depth", "1", "--scale", "3"]),
    ("11-section-pillar-z-94", ["--x", "-100", "-20", "--z", "-94", "--ymin", "20", "--ymax", "100", "--depth", "1", "--scale", "5"]),
    ("12-section-ledges-z-79", ["--x", "-100", "-20", "--z", "-79", "--ymin", "20", "--ymax", "100", "--depth", "1", "--scale", "5"]),
    ("13-section-store-road-x56", ["--z", "-112", "-20", "--x", "56", "--ymin", "20", "--ymax", "100", "--depth", "1", "--scale", "5"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-red-half-sw.png"), 4, "sw", (-100, -128, 70, -12), 25)
render_iso.render(ids, dat, x0, z0, o("33-iso-spawn.png"), 6, "se", (-24, -122, 22, -64), 55)
render_iso.render(ids, dat, x0, z0, o("34-iso-pillar-and-arms.png"), 6, "ne", (-96, -100, -28, -60), 30)
render_iso.render(ids, dat, x0, z0, o("35-iso-store-and-road.png"), 6, "sw", (26, -114, 70, -30), 50)
render_iso.render(ids, dat, x0, z0, o("36-iso-hub-and-gate.png"), 5, "se", (-34, -80, 32, -10), 50)
render_iso.render(ids, dat, x0, z0, o("37-iso-middle-and-steps.png"), 4, "se", (-72, -50, 71, 49), 30)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-store-from-the-road.png"), (44, -112, 69, -94), 66, 90, "north", 10)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-pavilion-from-the-pool.png"), (-12, -122, 11, -100), 70, 92, "north", 10)
render_iso.elevation(ids, dat, x0, z0, o("52-elev-pillar-from-the-terrace.png"), (-96, -98, -28, -60), 24, 90, "north", 6)
render_iso.elevation(ids, dat, x0, z0, o("53-elev-gate.png"), (-30, -40, 29, -24), 56, 84, "north", 8)
render_iso.elevation(ids, dat, x0, z0, o("60-elev-board-from-east.png"), (-112, -128, 111, 127), 20, 100, "west", 3)
print("renders written to", out)
