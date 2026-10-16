"""Crucible's renders: the board in the library's flat colours (two corners, red's front, the foundry x-rayed, sections
through the pit and down the store), and the same places drawn in the game's own textures by the studio's renderer
when MINECRAFT_JAR names the 1.8.9 client.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from PIL import Image  # noqa: E402

from pgmvox import World  # noqa: E402
from pgmvox.read import render  # noqa: E402

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)


def iso(name, **kw):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, **kw)
    render.trim(p)


iso("10-iso-board-se.png", scale=2, corner="se", ymin=0)
iso("11-iso-board-nw.png", scale=2, corner="nw", ymin=0)
iso("12-xray-red-foundry.png", scale=4, corner="nw", box=(-66, 50, 46, 99), ymin=20, ymax=66, xray=True)
render.cutaway(w, os.path.join(out, "13-section-pit.png"), [(22, 10), (22, 99)], ymin=20, ymax=110, scale=4,
               title="down the crucible's axis, x 22: the plain, the pit and the crucible under the gantry, the furnace "
                     "hall under the pour room, the mountain")
render.cutaway(w, os.path.join(out, "14-section-store.png"), [(-66, 89), (10, 89)], ymin=10, ymax=110, scale=4,
               title="across the cold store, z 89: the flank cave's end, the store, the deep ramp's landing, the crew "
                     "hall")

jar = os.environ.get("MINECRAFT_JAR")
if jar and os.path.isfile(jar):
    T = dict(fov=40, w=1800, h=1300)
    shots = [
        ("20-board-from-red-corner.png", dict(box=(-70, 0, -100, 69, 110, 99), yaw=150, pitch=38)),
        ("21-board-from-blue-corner.png", dict(box=(-70, 0, -100, 69, 110, 99), yaw=-30, pitch=38)),
        ("22-red-front.png", dict(box=(-70, 30, 0, 69, 110, 99), yaw=0, pitch=24)),
        ("23-blue-front.png", dict(box=(-70, 30, -100, 69, 110, -1), yaw=180, pitch=24)),
        ("24-red-pit.png", dict(box=(-6, 30, 22, 52, 80, 70), yaw=-35, pitch=28)),
        ("25-red-pit-floor.png", dict(box=(4, 38, 30, 42, 56, 62), yaw=-20, pitch=35)),
        ("26-red-gate.png", dict(box=(-58, 40, 38, -4, 82, 75), yaw=-15, pitch=12)),
        ("27-rift-and-tip.png", dict(box=(-45, 0, -16, 25, 60, 24), yaw=55, pitch=28)),
        ("28-flow-lavafall.png", dict(box=(-70, 0, 0, -18, 80, 70), yaw=-60, pitch=26)),
        ("30-cut-level-0.png", dict(box=(-55, 45, 55, 40, 57, 95), yaw=0, pitch=68)),
        ("31-cut-level-1.png", dict(box=(-55, 30, 55, 40, 45, 95), yaw=0, pitch=68)),
        ("32-cut-cold-store.png", dict(box=(-54, 20, 74, -26, 33, 96), yaw=25, pitch=52)),
        ("33-cut-loading-hall.png", dict(box=(-56, 38, 60, -16, 61, 82), yaw=-30, pitch=40)),
        ("34-cut-crew-hall.png", dict(box=(-12, 50, 70, 12, 58, 92), yaw=20, pitch=50)),
        ("35-cut-furnace-hall.png", dict(box=(0, 37, 63, 34, 46, 80), yaw=15, pitch=40)),
        ("36-cut-pour-room.png", dict(box=(6, 49, 50, 36, 58, 74), yaw=15, pitch=45)),
    ]
    render.textured(build, [dict(out=os.path.join(out, n), **s, **T) for n, s in shots])
    for n, _ in shots:                                   # keep each picture under two megabytes
        p = os.path.join(out, n)
        if os.path.isfile(p) and os.path.getsize(p) > 1_900_000:
            Image.open(p).convert("RGB").quantize(256).save(p, optimize=True)
