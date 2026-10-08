"""Draw Saltgate: the studio's round-trip reads, the board from four corners, each stage close, the cutaway down
the middle from the flagship to the keep, and the treasury cut open.

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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "5"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "5"])
cutaway.cut(build, o("10-cutaway-down-the-middle-x0.png"), [(0, -72), (0, 63)], ymin=10, ymax=58, scale=5,
            title="10. DOWN THE MIDDLE, true scale: the flagship, the landing, the gate under the wall walk, the yard, the terraces, "
                  "the citadel's portcullis, the keep and the treasury")
cutaway.cut(build, o("11-cutaway-the-sea-wall-z-30.png"), [(-48, -30), (47, -30)], ymin=12, ymax=40, scale=6,
            title="11. ALONG THE SEA WALL, true scale: the towers, the walk, the gate's passage under it")
cutaway.cut(build, o("12-cutaway-the-culvert-x-14.png"), [(-14, -44), (-14, -16)], ymin=12, ymax=34, scale=10,
            title="12. THE CULVERT, true scale: from the beach under the wall into the yard")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-saltgate-sw.png"), 3, "sw", None, 0, 64)
render_iso.render(ids, dat, x0, z0, o("31-iso-saltgate-se.png"), 3, "se", None, 0, 64)
render_iso.render(ids, dat, x0, z0, o("32-iso-stage-a-the-sea-gate.png"), 6, "sw", (-24, -60, 24, -18), 0, 45)
render_iso.render(ids, dat, x0, z0, o("33-iso-stage-b-the-town.png"), 4, "sw", (-48, -20, 47, 26), 0, 50)
render_iso.render(ids, dat, x0, z0, o("34-iso-west-powder-store-cut-at-31.png"), 9, "sw", (-26, -8, -10, 9), 0, 31)
render_iso.render(ids, dat, x0, z0, o("35-iso-stage-c-the-citadel.png"), 4, "sw", (-48, 20, 47, 63), 0, 58)
render_iso.render(ids, dat, x0, z0, o("36-iso-the-treasury-cut-at-40.png"), 8, "sw", (-14, 42, 13, 62), 0, 40)
print("renders written to", out)
