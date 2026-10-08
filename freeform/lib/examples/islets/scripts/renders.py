"""Islets' renders: the board among its mountains, and the islands close."""
import os
import sys

from pgmvox import World, render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-board.png"), 2, "sw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-the-islands.png"), 6, "sw", (-30, -16, 29, 15), 15, 45)
render.cutaway(w, os.path.join(out, "10-cutaway-x.png"), [(-32, 0), (32, 0)], 0, 45, 6, title="along x at z 0")
for n in ("30-iso-the-board.png", "31-iso-the-islands.png"):
    render.trim(os.path.join(out, n))

# the plan's names and markers over what was built, to show it landed where the plan said
from plan import build as plan  # noqa: E402
from pgmvox.sketch import TEAM, Sheet  # noqa: E402

R = plan()
S = Sheet("Islets - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=12, title="FROM ABOVE",
          legend="the built world's top blocks, with the plan's names over them",
          symmetry=R.symmetry)
m.built(w, ymin=15)
m.place(-20, -7, "Red's island")
m.place(*R.symmetry.point(-20, -7), "Blue's island")
m.marker(-24, 0, "S", TEAM["red"], both=True)
m.marker(-1, 2, "A", TEAM["neutral"])
m.ghost([(-28, -9), (-14, -12), (-11, -2), (-14, 9), (-26, 10)], (255, 255, 255), both=True)
S.save(os.path.join(out, "05-topdown-annotated.png"))
