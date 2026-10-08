"""Draw Lantern Drop: the studio's round-trip reads, the whole course among its peaks, the course alone from both
sides, each stretch close, and the course's long section.

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
cutaway.cut(build, o("10-cutaway-the-left-way-x-8.png"), [(-8, -6), (-8, 318)], ymin=10, ymax=252, scale=3,
            title="10. DOWN THE LEFT WAY at x -8, true scale: every piece the left way lands on, the harbour at the foot")
cutaway.cut(build, o("11-cutaway-the-middle-x0.png"), [(0, -6), (0, 318)], ymin=10, ymax=252, scale=3,
            title="11. DOWN THE MIDDLE at x 0, true scale: the bell court, the pagoda, the shrine, the rope bridge, the terrace, the arcade, the boathouse, the barge")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-the-course-among-its-peaks.png"), 2, "sw", None, 0, 255)
render_iso.render(ids, dat, x0, z0, o("31-iso-the-course-alone-sw.png"), 3, "sw", (-30, -8, 30, 320), 0, 255)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-course-alone-ne.png"), 3, "ne", (-30, -8, 30, 320), 0, 255)
render_iso.render(ids, dat, x0, z0, o("33-iso-bell-court-to-pagoda.png"), 6, "sw", (-24, -6, 24, 70), 180, 252)
render_iso.render(ids, dat, x0, z0, o("34-iso-lantern-lines-to-rope-bridge.png"), 6, "sw", (-24, 66, 24, 148), 130, 200)
render_iso.render(ids, dat, x0, z0, o("35-iso-pillars-to-terrace.png"), 6, "sw", (-24, 146, 24, 202), 95, 165)
render_iso.render(ids, dat, x0, z0, o("36-iso-market-to-crows-nests.png"), 6, "sw", (-24, 202, 24, 258), 40, 110)
render_iso.render(ids, dat, x0, z0, o("37-iso-boathouse-and-harbour.png"), 5, "sw", (-26, 258, 26, 320), 10, 60)
print("renders written to", out)
