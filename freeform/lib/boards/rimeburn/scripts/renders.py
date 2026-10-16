"""Rimeburn's renders: the flat-colour reads (the board from above with the plan over it, sections) and the
studio's textured pictures, the ones a player's eye sees.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import land as LD
import plan as P
from pgmvox import World
from pgmvox.read import render
from pgmvox.read.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
out = os.path.join(root, "renders")
w = World.load(build)

R = P.build()
S = Sheet("Rimeburn - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="FROM ABOVE",
          legend="the built world's top blocks with the plan's places and objectives over them; Frost north, Ember south",
          symmetry=R.symmetry)
m.built(w, ymin=20)
for name, (x, z) in P.PLACES.items():
    m.place(x, z, name)
    if name != "the Thaw":
        m.place(*R.symmetry.point(x, z), name)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
render.cutaway(w, os.path.join(out, "10-section-hearth.png"), [(LD.HEARTH[0], -96), (LD.HEARTH[0], 95)], 4, 80, 3,
               title=f"along z at x {LD.HEARTH[0]}: the Hearth, the Vent's barrow, the seam, Ember's land")
render.cutaway(w, os.path.join(out, "11-section-across.png"), [(-64, LD.SHELF[1]), (63, LD.SHELF[1])], 4, 80, 4,
               title=f"along x at z {LD.SHELF[1]}: Frost's Hearth Hollow, the burn, the Rime Shelf")

if os.environ.get("MINECRAFT_JAR"):
    hx, hz = LD.HEARTH
    sx, sz = LD.SHELF
    ex, ez = LD.SYM.point(hx, hz)
    ix_, iz_ = LD.SYM.point(sx, sz)
    shots = [
        dict(out="20-board.png", box=(-64, 0, -96, 63, 95, 95), yaw=215, pitch=40),
        dict(out="21-board-from-frost.png", box=(-64, 0, -96, 63, 95, 95), yaw=20, pitch=32),
        dict(out="22-frost-half.png", box=(-64, 0, -96, 63, 95, -10), yaw=160, pitch=35),
        dict(out="23-ember-half.png", box=(-64, 0, -1, 63, 95, 95), yaw=340, pitch=35),
        dict(out="30-frost-hearth.png", box=(hx - 18, 25, hz - 16, hx + 14, 70, hz + 16), yaw=150, pitch=30),
        dict(out="31-ember-hearth.png", box=(ex - 14, 25, ez - 16, ex + 18, 70, ez + 16), yaw=330, pitch=30),
        dict(out="32-frost-icestone.png", box=(sx - 16, 25, sz - 16, sx + 16, 70, sz + 18), yaw=200, pitch=28),
        dict(out="33-ember-icestone.png", box=(ix_ - 16, 25, iz_ - 18, ix_ + 16, 70, iz_ + 16), yaw=20, pitch=28),
        dict(out="34-the-thaw.png", box=(-26, 20, -30, 25, 70, 29), yaw=100, pitch=25),
        dict(out="35-frost-hold.png", box=(-22, 30, -96, 26, 80, -66), yaw=180, pitch=22),
        dict(out="36-ember-hold.png", box=(-27, 30, 65, 21, 80, 95), yaw=0, pitch=22),
        dict(out="37-rimecroft.png", box=(30, 25, -48, 63, 70, -14), yaw=130, pitch=30),
        dict(out="38-embercroft.png", box=(-64, 25, 13, -31, 70, 47), yaw=310, pitch=30),
        dict(out="39-the-anvil.png", box=(-64, 25, -54, -30, 70, -22), yaw=150, pitch=22),
        dict(out="40-the-vent.png", box=(-40, 20, -56, -18, 39, -18), yaw=120, pitch=35),
        dict(out="41-ember-ground.png", box=(-30, 30, 25, 30, 70, 70), yaw=330, pitch=55),
        dict(out="42-frost-ground.png", box=(-30, 30, -70, 30, 70, -25), yaw=150, pitch=55),
    ]
    for s in shots:
        s["out"] = os.path.join(out, s["out"])
        s.setdefault("fov", 40)
        s.setdefault("w", 1800)
        s.setdefault("h", 1300)
    print(render.textured(build, shots))
