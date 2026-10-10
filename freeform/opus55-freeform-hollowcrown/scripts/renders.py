"""Draw the pictures that show Hollowcrown: the studio's round-trip reads over the written region files, and
the isometric, x-ray and elevation views over the generated volume.

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
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3", "--contour", "4", "--water"])
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "3"])
run(["--underground", region, o("04-underground.png"), "--scale", "3", "--band", "15", "40"])
SECTIONS = [
    ("10-section-crown-town-vale-z-18", ["--x", "-120", "10", "--z", "-18", "--ymin", "10", "--ymax", "120", "--depth", "1", "--scale", "4"]),
    ("11-section-deep-stair-x-86", ["--z", "-50", "30", "--x", "-86", "--ymin", "10", "--ymax", "115", "--depth", "1", "--scale", "4"]),
    ("12-section-eyrie-goat-stair-z-66", ["--x", "-75", "-20", "--z", "-66", "--ymin", "40", "--ymax", "112", "--depth", "2", "--scale", "6"]),
    ("13-section-river-bend-z30", ["--x", "-30", "30", "--z", "30", "--ymin", "30", "--ymax", "60", "--depth", "1", "--scale", "8"]),
    ("14-section-falls-z52", ["--x", "-80", "-30", "--z", "52", "--ymin", "40", "--ymax", "80", "--depth", "2", "--scale", "7"]),
    ("15-section-deepmere-hall-z14", ["--x", "-110", "-50", "--z", "14", "--ymin", "8", "--ymax", "50", "--depth", "1", "--scale", "7"]),
    ("16-section-delving-z0", ["--x", "-60", "59", "--z", "0", "--ymin", "10", "--ymax", "60", "--depth", "1", "--scale", "4"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-board-sw.png"), 2, "sw")
render_iso.render(ids, dat, x0, z0, o("33-iso-wendholm-se.png"), 4, "se", (-74, -36, -14, 40), 40)
render_iso.render(ids, dat, x0, z0, o("34-iso-wendholm-ne.png"), 4, "ne", (-74, -36, -14, 40), 40)
render_iso.render(ids, dat, x0, z0, o("35-iso-crownhold.png"), 5, "se", (-110, -46, -60, 4), 70)
render_iso.render(ids, dat, x0, z0, o("36-iso-eyrie-goat-stair.png"), 5, "se", (-72, -86, -20, -50), 40)
render_iso.render(ids, dat, x0, z0, o("37-iso-wendfoot-three-angles.png"), 7, "se", (-34, 16, -2, 48), 38)
render_iso.render(ids, dat, x0, z0, o("38-iso-wendfoot-three-angles-nw.png"), 7, "nw", (-34, 16, -2, 48), 38)
render_iso.render(ids, dat, x0, z0, o("39-iso-kingsbridge.png"), 6, "sw", (-20, -12, 19, 11), 30)
render_iso.render(ids, dat, x0, z0, o("40-iso-river-bend-and-mill.png"), 5, "se", (-34, 30, 6, 74), 25)
render_iso.render(ids, dat, x0, z0, o("41-iso-tarn-and-falls.png"), 4, "se", (-108, 30, -36, 70), 40)
render_iso.render(ids, dat, x0, z0, o("42-iso-market-cross.png"), 7, "se", (-50, -12, -30, 14), 55)
render_iso.render(ids, dat, x0, z0, o("43-iso-fields-north.png"), 5, "se", (-30, -66, 0, -18), 35)
render_iso.render(ids, dat, x0, z0, o("50-xray-underhall.png"), 4, "se", (-120, -40, -40, 36), ymax=46, xray=True)
render_iso.render(ids, dat, x0, z0, o("51-xray-underhall-nw.png"), 4, "nw", (-120, -40, -40, 36), ymax=46, xray=True)
render_iso.render(ids, dat, x0, z0, o("52-iso-underhall-cutaway.png"), 5, "se", (-112, -30, -48, 34), 12, 38)
render_iso.render(ids, dat, x0, z0, o("53-xray-delving-and-gallery.png"), 4, "se", (-60, -20, 59, 19), ymax=30, xray=True)
render_iso.elevation(ids, dat, x0, z0, o("60-elev-board-from-south.png"), (-120, -96, 119, 95), 10, 128, "north", 3)
render_iso.elevation(ids, dat, x0, z0, o("61-elev-wendholm-from-east.png"), (-74, -36, -10, 40), 40, 110, "west", 5)
render_iso.elevation(ids, dat, x0, z0, o("62-elev-eyrie-from-east.png"), (-70, -86, -20, -54), 40, 112, "west", 5)
print("renders written to", out)
