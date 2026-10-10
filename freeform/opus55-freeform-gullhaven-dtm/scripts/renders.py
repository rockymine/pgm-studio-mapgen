"""Draw Gullhaven DTM: the studio's round-trip reads over the region files, the whole board from two corners,
each monument close, the Skerry between the islands, and a section down the strait.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "opus55-freeform-gullhaven", "scripts"))
import render_iso  # noqa: E402

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


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "4"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "4"])
run(["--section", region, o("10-section-the-strait-x-19.png"), "--z", "-50", "165", "--x", "-19", "--ymin", "10",
     "--ymax", "50", "--depth", "1", "--scale", "4"])
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-board-se.png"), 2, "se", None, 0, 72)
render_iso.render(ids, dat, x0, z0, o("31-iso-board-nw.png"), 2, "nw", None, 0, 72)
render_iso.render(ids, dat, x0, z0, o("32-iso-red-harbour-monument.png"), 8, "nw", (22, 18, 40, 34), 0, 40)
render_iso.render(ids, dat, x0, z0, o("33-iso-red-beach-monument.png"), 8, "se", (-58, 0, -44, 16), 0, 40)
render_iso.render(ids, dat, x0, z0, o("34-iso-the-skerry-between.png"), 5, "se", (-40, 36, 2, 80), 0, 50)
render_iso.render(ids, dat, x0, z0, o("35-iso-blue-island.png"), 3, "nw", (-93, 46, 20, 165), 0, 72)
print("renders written to", out)
import cutaway  # noqa: E402
cutaway.cut(build, o("11-cutaway-the-axis.png"), [(16, -62), (16, -39), (-19, 57.5), (-54, 154), (-54, 177)],
            title="11. THE AXIS, true scale: red's back (left) over the sea, red's town, the Skerry, blue's town, blue's back (right)")
cutaway.cut(build, o("12-cutaway-red-back-z-47.png"), [(-68, -47), (67, -47)], scale=6,
            title="12. WEST TO EAST at z = -47, red's back: the Headland's cliff, the Ravine's mouth, the town on its sea wall")
render_iso.render(ids, dat, x0, z0, o("36-iso-red-back-from-the-north.png"), 5, "ne", (-68, -62, 67, -28), 0, 60)
print("cutaways written")
