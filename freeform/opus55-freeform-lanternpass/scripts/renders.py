"""Draw Lantern Pass: the studio's round-trip reads, the whole pass from two corners, each stretch close, the
ridges in section, the gorge along its crossings, the bell tower.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

import cutaway
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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "3"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "3"])
cutaway.cut(build, o("10-cutaway-across-the-market-z90.png"), [(-64, 90), (63, 90)], ymin=0, ymax=50, scale=6,
            title="10. ACROSS THE MARKET at z 90, true scale: a walkway's ridge, the void, the lane's ridge under the stalls and the arcade, the void, the other walkway")
cutaway.cut(build, o("11-cutaway-across-the-gorge-z250.png"), [(-40, 250), (40, 250)], ymin=0, ymax=56, scale=7,
            title="11. ACROSS THE GORGE at z 250, true scale: the rope bridge, a stepping pillar from far below, the gallery on its arch")
cutaway.cut(build, o("12-cutaway-the-gorge-along-the-arch.png"), [(8, 220), (8, 280)], ymin=0, ymax=50, scale=7,
            title="12. ALONG THE ARCH at x 8, true scale: down into the gallery, across under its roof, up the far side")
cutaway.cut(build, o("13-cutaway-up-the-stairs.png"), [(0, 270), (0, 374)], ymin=20, ymax=72, scale=6,
            title="13. UP THE GREAT STAIR at x 0, true scale: the torii, the court, the bell tower and the hall")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-the-pass-from-the-boathouse.png"), 2, "sw", (-64, -44, 63, 410), 0, 89)
render_iso.render(ids, dat, x0, z0, o("31-iso-the-pass-from-the-temple.png"), 2, "ne", (-64, -44, 63, 410), 0, 89)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-boathouse-and-the-harbour.png"), 5, "sw", (-34, -12, 33, 62), 0, 60)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-market.png"), 5, "sw", (-34, 58, 33, 118), 0, 60)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-terraces.png"), 5, "sw", (-34, 112, 33, 172), 0, 60)
render_iso.render(ids, dat, x0, z0, o("35-iso-the-bamboo.png"), 5, "sw", (-34, 168, 33, 228), 0, 60)
render_iso.render(ids, dat, x0, z0, o("36-iso-the-bamboo-under-its-crown-cut-at-39.png"), 6, "sw", (-14, 168, 13, 228), 0, 39)
render_iso.render(ids, dat, x0, z0, o("37-iso-the-gorge.png"), 5, "sw", (-34, 222, 33, 280), 0, 66)
render_iso.render(ids, dat, x0, z0, o("38-iso-the-stairs-and-the-temple.png"), 4, "sw", (-34, 272, 33, 374), 0, 80)
render_iso.render(ids, dat, x0, z0, o("39-iso-the-bell-tower.png"), 9, "sw", (-10, 346, 9, 365), 45, 66)
print("renders written to", out)
