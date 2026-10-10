"""Draw Copperline: the studio's round-trip reads, the board from two corners with the mountains cut away, each leg
close, the track's long section and the cuts through the gorge, the heap and the mine.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

import cutaway
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
cutaway.cut(build, o("10-cutaway-the-trestle-x16.png"), [(16, 8), (16, -40)], ymin=8, ymax=50, scale=8,
            title="10. NORTH OVER THE TRESTLE at x 16, true scale: the brow, the gorge and the river, the trestle, the cutting, the depot")
cutaway.cut(build, o("11-cutaway-the-heap-z36.png"), [(-20, 36), (55, 36)], ymin=18, ymax=64, scale=6,
            title="11. EAST ACROSS THE TOWN at z 36, true scale: Station Road's houses, Main Street, the slag heap, the old adit in the mountain")
cutaway.cut(build, o("12-cutaway-the-shelf-z38.png"), [(24, -38), (-30, -38)], ymin=20, ymax=60, scale=8,
            title="12. WEST ALONG THE SHELF at z 38, true scale: the cart climbing eight, the gantry over it, the adit under it")
cutaway.cut(build, o("13-cutaway-the-mine-x-12.png"), [(-12, -30), (-12, -72)], ymin=20, ymax=70, scale=8,
            title="13. NORTH INTO THE MINE at x -12, true scale: the north bank, the shelf, the yard, the portal, the hall and the line's end")
cutaway.cut(build, o("14-cutaway-the-adit.png"), [(-16, -30), (-16, -50), (-30, -50), (-30, -66)], ymin=20, ymax=60, scale=8,
            title="14. ALONG THE ADIT, true scale: from the shelf's face under the yard and up into the mine hall's floor")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-copperline-sw.png"), 3, "sw", None, 0, 99)
render_iso.render(ids, dat, x0, z0, o("31-iso-copperline-se.png"), 3, "se", None, 0, 99)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-valley-cut-at-46.png"), 4, "sw", None, 0, 46)
render_iso.render(ids, dat, x0, z0, o("33-iso-leg-a-main-street.png"), 6, "sw", (-36, 12, 30, 71), 0, 44)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-slag-heap.png"), 6, "nw", (14, 16, 55, 60), 0, 60)
render_iso.render(ids, dat, x0, z0, o("35-iso-leg-b-the-gorge.png"), 6, "sw", (-34, -30, 30, 14), 0, 44)
render_iso.render(ids, dat, x0, z0, o("36-iso-leg-c-the-mine-head.png"), 6, "sw", (-40, -60, 30, -22), 0, 62)
render_iso.render(ids, dat, x0, z0, o("37-iso-the-mine-hall-cut-at-42.png"), 8, "sw", (-34, -72, 10, -56), 20, 42)
render_iso.render(ids, dat, x0, z0, o("38-iso-the-engine-shed-cut-at-30.png"), 8, "sw", (16, 56, 36, 70), 18, 30)
render_iso.render(ids, dat, x0, z0, o("39-iso-the-trestle.png"), 9, "se", (6, -24, 26, 0), 8, 36)
print("renders written to", out)
