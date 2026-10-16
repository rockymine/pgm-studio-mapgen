"""Rimeglow Rift's pictures: the plan's names drawn over the built world, pgmvox's flat-colour overviews, and the studio's
textured renderer for the shots the board is judged on."""
import os
import sys

from plan import PLACES, SOUTH_NAMES, objectives
from pgmvox import World
from pgmvox.read import render
from pgmvox.read.sketch import Sheet, TEAM

build, root = sys.argv[1], sys.argv[2]
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)
w = World.load(build)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "flat-iso-nw.png"), 3, "nw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "flat-iso-se.png"), 3, "se")
render.trim(os.path.join(out, "flat-iso-nw.png"))
render.trim(os.path.join(out, "flat-iso-se.png"))

S = Sheet("Rimeglow Rift - as built")
m = S.map(-70, -100, 69, 99, scale=5, title="FROM ABOVE",
          legend="names are the plan's; C the cores, S the spawns; the rift runs east to west across the middle")
m.built(w)
for name, (x, z) in PLACES.items():
    m.place(x, z, name, size=11)
    m.place(-1 - x, -1 - z, SOUTH_NAMES.get(name, name), size=11)
m.objectives(objectives().markers())
S.save(os.path.join(out, "00-annotated-topdown.png"))

if os.environ.get("MINECRAFT_JAR"):
    W, H = 1800, 1300
    FULL = (-70, 5, -100, 69, 100, 99)
    shots = {
        "tx-01-outside-north.png": dict(box=FULL, yaw=0, pitch=58),
        "tx-02-outside-oblique.png": dict(box=FULL, yaw=-60, pitch=32),
        "tx-03-outside-from-below.png": dict(box=FULL, yaw=-30, pitch=-18),
        "tx-04-rift-section.png": dict(box=(-52, 30, -20, -26, 70, 20), yaw=90, pitch=8),
        "tx-05-causeway.png": dict(box=(-14, 38, -34, 14, 90, 30), yaw=-35, pitch=22),
        "tx-06-rime-hall.png": dict(box=(-3, 68, -95, 30, 95, -55), yaw=170, pitch=22),
        "tx-07-ember-hall.png": dict(box=(-33, 68, 55, 4, 95, 95), yaw=-10, pitch=22),
        "tx-08-hall-inside.png": dict(box=(-3, 66, -92, 30, 77, -70), yaw=10, pitch=40),
        "tx-09-rimewatch-core.png": dict(box=(32, 66, -62, 60, 100, -34), yaw=160, pitch=28),
        "tx-10-emberwatch-core.png": dict(box=(-61, 66, 33, -33, 100, 61), yaw=-20, pitch=28),
        "tx-11-frostmere.png": dict(box=(-42, 45, -62, 22, 85, -26), yaw=10, pitch=38),
        "tx-12-cinder-mere.png": dict(box=(-23, 45, 25, 41, 85, 61), yaw=170, pitch=38),
        "tx-13-gate-rime.png": dict(box=(-14, 55, -34, 14, 85, -10), yaw=-20, pitch=20),
        "tx-14-gate-ember.png": dict(box=(-14, 55, 9, 14, 85, 33), yaw=160, pitch=20),
        "tx-15-woodcutters-rest.png": dict(box=(-56, 50, -76, -24, 85, -44), yaw=150, pitch=35),
        "tx-16-orchard-keeper.png": dict(box=(23, 50, 43, 55, 85, 75), yaw=-30, pitch=35),
        "tx-17-lava-ledge-stones.png": dict(box=(-36, 30, -16, -4, 62, 16), yaw=50, pitch=28),
        "tx-18-ember-seams-and-frozen-falls.png": dict(box=(10, 30, -22, 50, 66, 22), yaw=-70, pitch=20),
    }
    jobs = [dict(out=os.path.join(out, name), fov=40, w=W, h=H, **kw) for name, kw in shots.items()]
    print(render.textured(build, jobs))
