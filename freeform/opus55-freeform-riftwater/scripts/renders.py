"""Draw the pictures that show the map: the studio's round-trip reads over the written region files, and the
isometric and x-ray views from render_iso.py over the generated volume.

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
    cmd = rt.split() + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", " ".join(args), r.stderr[-400:])


def o(name):
    return os.path.join(out, name)


# the plan views
run(["--topdown", region, o("01-topdown-material.png"), "--material", "--map", mapxml, "--scale", "3"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3", "--contour", "4", "--water"])
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "3"])
run(["--underground", region, o("04-underground.png"), "--scale", "3", "--band", "28", "50"])
# sections: through the falls and the cave mouth, along the river; through the cellar and gaol; the mine
# shaft and headframe; the stone bridge; Main Street's houses; the chapel; the watch house; the mill wheel
SECTIONS = [
    ("10-section-falls-cave-z3", ["--x", "-60", "8", "--z", "3", "--ymin", "20", "--ymax", "70", "--depth", "2"]),
    ("11-section-cave-north-x-52", ["--z", "-45", "45", "--x", "-52", "--ymin", "20", "--ymax", "75", "--depth", "2"]),
    ("12-section-cellar-gaol-x-52", ["--z", "-42", "-24", "--x", "-52", "--ymin", "36", "--ymax", "64", "--depth", "4", "--scale", "8"]),
    ("13-section-mine-shaft-z56", ["--x", "-100", "-60", "--z", "56", "--ymin", "36", "--ymax", "80", "--depth", "1", "--scale", "6"]),
    ("14-section-stone-bridge-x-36", ["--z", "-14", "18", "--x", "-36", "--ymin", "34", "--ymax", "60", "--depth", "1", "--scale", "8"]),
    ("15-section-main-street-z-52", ["--x", "-78", "-8", "--z", "-52", "--ymin", "44", "--ymax", "76", "--depth", "6", "--scale", "5"]),
    ("16-section-chapel-z-76", ["--x", "-60", "-34", "--z", "-76", "--ymin", "46", "--ymax", "82", "--depth", "3", "--scale", "6"]),
    ("17-section-watch-house-z-7", ["--x", "-112", "-70", "--z", "-7", "--ymin", "40", "--ymax", "80", "--depth", "4", "--scale", "6"]),
    ("18-section-mill-wheel-z10", ["--x", "-72", "-50", "--z", "10", "--ymin", "36", "--ymax", "64", "--depth", "1", "--scale", "8"]),
    ("19-section-sinkhole-x-50", ["--z", "20", "56", "--x", "-50", "--ymin", "28", "--ymax", "60", "--depth", "1", "--scale", "6"]),
    ("20-section-village-x-95", ["--z", "34", "84", "--x", "-95", "--ymin", "40", "--ymax", "72", "--depth", "6", "--scale", "5"]),
    ("21-section-mine-adit-x-103", ["--z", "-14", "40", "--x", "-103", "--ymin", "36", "--ymax", "84", "--depth", "2", "--scale", "5"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + (args if "--scale" in args else args + ["--scale", "6"]))

# isometric views over the volume
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-red-half.png"), 3, "se", (-120, -88, -1, 87))
render_iso.render(ids, dat, x0, z0, o("33-iso-town.png"), 5, "se", (-80, -88, -8, -10))
render_iso.render(ids, dat, x0, z0, o("34-iso-village.png"), 5, "se", (-112, 30, -60, 87))
render_iso.render(ids, dat, x0, z0, o("35-iso-river-mill.png"), 5, "se", (-100, -14, -8, 32))
render_iso.render(ids, dat, x0, z0, o("36-iso-spawn.png"), 6, "se", (-120, -30, -76, 12))
render_iso.render(ids, dat, x0, z0, o("37-iso-fields.png"), 5, "se", (-66, 20, -8, 87))
render_iso.render(ids, dat, x0, z0, o("38-iso-rift-falls.png"), 5, "sw", (-24, -60, 23, 30))
render_iso.render(ids, dat, x0, z0, o("40-xray-underground.png"), 4, "se", (-112, -42, -8, 62), xray=True)
render_iso.render(ids, dat, x0, z0, o("41-xray-underground-sw.png"), 4, "sw", (-112, -42, -8, 62), xray=True)
print("renders written to", out)
