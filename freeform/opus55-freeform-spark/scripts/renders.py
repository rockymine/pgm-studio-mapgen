"""Draw Spark: the studio's round-trip reads, the spark among its mountains, the spark alone from two corners and
close, and a section through the hub and two rays.

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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "2"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "2"])
cutaway.cut(build, o("10-cutaway-west-to-east-z0.png"), [(-56, 0), (56, 0)], ymin=30, ymax=80, scale=6,
            title="10. WEST TO EAST at z 0, true scale: two rays, the hub and its eye, the underside, the kill height at 40 below")
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-the-spark-among-its-mountains.png"), 2, "sw", None, 0, 199)
render_iso.render(ids, dat, x0, z0, o("31-iso-the-spark-sw.png"), 5, "sw", (-52, -52, 52, 52), 30, 70)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-spark-ne.png"), 5, "ne", (-52, -52, 52, 52), 30, 70)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-hub-close.png"), 10, "sw", (-16, -16, 16, 16), 48, 70)
print("renders written to", out)


def trim(path, pad=16):
    """Cut the empty sky round an isometric render."""
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))).save(path)


for name in ("30-iso-the-spark-among-its-mountains.png", "31-iso-the-spark-sw.png", "32-iso-the-spark-ne.png",
             "33-iso-the-hub-close.png"):
    trim(o(name))
