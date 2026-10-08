"""Draw the pictures that show Hollow Mesa: the studio's round-trip reads over the written region files, and
the isometric, x-ray and elevation views over the generated volume.

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
        print("FAILED", " ".join(args), r.stderr[-400:])


def o(name):
    return os.path.join(out, name)


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--map", mapxml, "--scale", "3"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3", "--contour", "4", "--water"])
run(["--topdown", region, o("03-topdown-objectives.png"), "--map", mapxml, "--scale", "3"])
run(["--underground", region, o("04-underground.png"), "--scale", "3", "--band", "36", "60"])
SECTIONS = [
    ("10-section-throat-core-z-24", ["--x", "-95", "-40", "--z", "-24", "--ymin", "0", "--ymax", "80", "--depth", "1", "--scale", "6"]),
    ("11-section-throat-x-71", ["--z", "-40", "-8", "--x", "-71", "--ymin", "30", "--ymax", "80", "--depth", "1", "--scale", "8"]),
    ("12-section-adit-z-34", ["--x", "-66", "-36", "--z", "-34", "--ymin", "40", "--ymax", "80", "--depth", "1", "--scale", "8"]),
    ("13-section-chimney-z-14", ["--x", "-72", "-20", "--z", "-14", "--ymin", "34", "--ymax", "80", "--depth", "2", "--scale", "6"]),
    ("14-section-shaft-x-78", ["--z", "-40", "-18", "--x", "-78", "--ymin", "40", "--ymax", "92", "--depth", "1", "--scale", "8"]),
    ("15-section-canyon-z0-arch", ["--x", "-130", "129", "--z", "0", "--ymin", "0", "--ymax", "100", "--depth", "1", "--scale", "3"]),
    ("16-section-main-street-x-22", ["--z", "-98", "-10", "--x", "-22", "--ymin", "36", "--ymax", "72", "--depth", "8", "--scale", "5"]),
    ("17-section-tipple-z26", ["--x", "-30", "0", "--z", "26", "--ymin", "36", "--ymax", "66", "--depth", "3", "--scale", "8"]),
    ("18-section-wash-trestle-x-29", ["--z", "36", "68", "--x", "-29", "--ymin", "38", "--ymax", "64", "--depth", "2", "--scale", "8"]),
    ("19-section-fort-z4", ["--x", "-130", "-90", "--z", "4", "--ymin", "66", "--ymax", "100", "--depth", "4", "--scale", "6"]),
]
for name, args in SECTIONS:
    run(["--section", region, o(name + ".png")] + args)

x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se")
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw")
render_iso.render(ids, dat, x0, z0, o("32-iso-red-half.png"), 3, "se", (-130, -100, -1, 99))
render_iso.render(ids, dat, x0, z0, o("33-iso-gilt-centre.png"), 5, "se", (-50, -60, 30, 30), 30)
render_iso.render(ids, dat, x0, z0, o("34-iso-main-street.png"), 5, "se", (-45, -100, 0, -20), 30)
render_iso.render(ids, dat, x0, z0, o("35-iso-adobe-quarter-wash.png"), 5, "se", (-60, 8, 10, 90), 30)
render_iso.render(ids, dat, x0, z0, o("36-iso-fort.png"), 6, "se", (-130, -20, -88, 26), 60)
render_iso.render(ids, dat, x0, z0, o("37-iso-olive-grove-needles.png"), 4, "se", (-110, -100, -40, -20), 60)
render_iso.render(ids, dat, x0, z0, o("38-iso-rancho-acacias.png"), 4, "se", (-130, 40, -40, 99), 60)
render_iso.render(ids, dat, x0, z0, o("40-xray-throat.png"), 5, "se", (-100, -46, -24, 0), ymax=64, xray=True)
render_iso.render(ids, dat, x0, z0, o("41-xray-throat-sw.png"), 5, "sw", (-100, -46, -24, 0), ymax=64, xray=True)
render_iso.render(ids, dat, x0, z0, o("42-iso-throat-cutaway.png"), 7, "se", (-86, -38, -54, -10), 30, 52)
render_iso.elevation(ids, dat, x0, z0, o("50-elev-throat-z-24.png"), (-95, -24, -40, -23), 0, 84, "north", 6)
render_iso.elevation(ids, dat, x0, z0, o("51-elev-canyon-arch-z0.png"), (-130, -1, 129, 0), 0, 100, "north", 3)
render_iso.elevation(ids, dat, x0, z0, o("52-elev-main-street-west-row.png"), (-34, -100, -22, -20), 38, 72, "east", 5)
render_iso.elevation(ids, dat, x0, z0, o("53-elev-canyon-wall-red-from-east.png"), (-60, -100, -26, 99), 30, 100, "west", 3)
render_iso.elevation(ids, dat, x0, z0, o("54-elev-tipple-trestle-from-east.png"), (-34, 14, -14, 70), 36, 66, "west", 7)
print("renders written to", out)
