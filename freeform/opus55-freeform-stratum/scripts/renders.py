"""Draw the pictures that show Stratum: the studio's round-trip reads over the written region files, the
isometric views of the city and of the land with the city and the clouds lifted off it, and elevations of
the faces, which are where the patterns show.

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
    ("10-section-spawn-to-spawn-z0", ["--x", "-100", "99", "--z", "0", "--ymin", "0", "--ymax", "127", "--depth", "1", "--scale", "3"]),
    ("11-section-obelisk-z-50", ["--x", "-100", "99", "--z", "-50", "--ymin", "0", "--ymax", "127", "--depth", "1", "--scale", "3"]),
    ("12-section-reactor-x-56", ["--z", "30", "66", "--x", "-56", "--ymin", "20", "--ymax", "100", "--depth", "1", "--scale", "6"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-city-only-se.png"), 3, "se", ymin=56)
render_iso.render(ids, dat, x0, z0, o("33-iso-land-only-se.png"), 3, "se", ymax=43)
render_iso.render(ids, dat, x0, z0, o("34-iso-atrium.png"), 5, "se", (-100, -20, -60, 20), 56)
render_iso.render(ids, dat, x0, z0, o("35-iso-obelisk.png"), 5, "se", (-74, -66, -38, -34), 60)
render_iso.render(ids, dat, x0, z0, o("36-iso-reactor-and-cantilever.png"), 5, "se", (-70, 34, -10, 66), 56)
render_iso.render(ids, dat, x0, z0, o("37-iso-forum.png"), 5, "se", (-30, -14, 29, 14), 70)
render_iso.render(ids, dat, x0, z0, o("38-iso-gate-ziggurat.png"), 4, "se", (-40, -60, 39, -34), 56)
render_iso.render(ids, dat, x0, z0, o("39-iso-columns.png"), 5, "nw", (-52, -24, -34, 24), 56)
render_iso.render(ids, dat, x0, z0, o("40-iso-fragments-in-the-land.png"), 3, "sw", (-100, -72, -1, 71), 0, 43)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-atrium-south-face.png"), (-95, 13, -65, 40), 72, 92, "north", 10)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-obelisk-south-face.png"), (-64, -60, -48, -30), 76, 124, "north", 9)
render_iso.elevation(ids, dat, x0, z0, o("52-elev-obelisk-east-face-balcony.png"), (-60, -56, -40, -43), 76, 124, "west", 9)
render_iso.elevation(ids, dat, x0, z0, o("53-elev-cantilever-south.png"), (-37, 50, -12, 70), 60, 92, "north", 8)
render_iso.elevation(ids, dat, x0, z0, o("54-elev-forum-north.png"), (-28, -30, 27, -9), 70, 94, "south", 7)
render_iso.elevation(ids, dat, x0, z0, o("55-elev-gate-south.png"), (-16, -60, 15, -30), 64, 98, "north", 7)
render_iso.elevation(ids, dat, x0, z0, o("56-elev-reactor-north.png"), (-68, 20, -44, 38), 62, 100, "south", 8)
render_iso.elevation(ids, dat, x0, z0, o("60-elev-board-from-south.png"), (-100, -72, 99, 71), 0, 127, "north", 3)
print("renders written to", out)
