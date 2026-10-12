"""The canyon and its six crossings from above the south-east, each crossing close from two corners, and each from
the side with nothing but the bridge in the cut."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pgmvox import World  # noqa: E402
from pgmvox.read import render  # noqa: E402

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-canyon.png"), 2, "se", ymin=18)
CROSSINGS = {"column-arch": (-160, 12), "arch": (-96, 12), "curving": (-32, 30), "window-fin": (32, 12),
             "broken": (96, 12), "twin": (160, 30)}
for k, (name, (z, half)) in enumerate(CROSSINGS.items()):
    box = (-62, z - 32, 62, z + 32)
    near, far = ("sw", "ne") if half > 12 else ("se", "nw")
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, f"{31 + k}-iso-{name}.png"), 5, near, box, 18)
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, f"{31 + k}-iso-{name}-{far}.png"), 5, far, box, 18)
    render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, f"{41 + k}-side-{name}.png"),
                     (-64, z - half, 64, z + half), 18, 82, look="north", scale=5)
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
