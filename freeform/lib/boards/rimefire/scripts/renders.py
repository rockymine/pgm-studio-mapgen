"""Rimefire's renders: the board whole from both ends and from above, each objective inside and out, each place close,
the seam; flat colour first, then the studio's textured renderer."""
import os
import sys

os.environ.setdefault("PGM_STUDIO_ROOT", "/home/user/pgm-studio")
os.environ.setdefault("MINECRAFT_JAR", "/home/user/mc/client-1.8.9.jar")

import land as LND
import plan as PLAN
from pgmvox import World
from pgmvox.read import render
from pgmvox.read.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)

render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-flat-sw.png"), 3, "sw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-flat-ne.png"), 3, "ne")
for n in ("30-iso-flat-sw.png", "31-iso-flat-ne.png"):
    render.trim(os.path.join(out, n))

fx, fz = LND.FURNACE
ix, iz = -1 - fx, -1 - fz
WHOLE = (-70, 30, -105, 70, 115, 100)
shots = [
    ("01-outside-from-the-ice-end.png", WHOLE, 35, 32),
    ("02-outside-from-the-fire-end.png", WHOLE, -145, 32),
    ("03-from-above.png", WHOLE, 0, 72),
    ("04-the-seam-from-the-fire-rim.png", (-45, 38, -26, 45, 85, 26), 0, 35),
    ("05-the-seam-from-the-ice-rim.png", (-45, 38, -26, 45, 85, 26), 180, 35),
    ("06-the-furnace-fire-core.png", (fx - 16, 60, fz - 16, fx + 18, 100, fz + 16), -70, 32),
    ("07-the-furnace-section.png", (fx - 15, 56, fz - 1, fx + 15, 90, fz + 1), 0, 12),
    ("08-the-furnace-pit.png", (fx - 14, 64, fz - 14, fx + 14, 82, fz + 14), -90, 52),
    ("09-the-cold-hearth-ice-core.png", (ix - 18, 60, iz - 16, ix + 16, 100, iz + 16), 110, 32),
    ("10-the-cold-hearth-section.png", (ix - 15, 56, iz - 1, ix + 15, 90, iz + 1), 180, 12),
    ("11-ashfall-lodge-fire-spawn.png", (-32, 60, -92, 4, 82, -64), 180, 35),
    ("12-rimehold-ice-spawn.png", (-5, 60, 63, 31, 82, 91), 0, 35),
    ("13-rustwater-fire-hamlet.png", (-62, 48, -62, -18, 85, -28), 20, 32),
    ("14-frostholm-ice-hamlet.png", (17, 48, 27, 61, 85, 61), 200, 32),
    ("15-the-keystone-bridge.png", (-14, 40, -14, 14, 75, 14), 90, 28),
    ("16-the-west-span-and-stair.png", (-60, 38, -26, -22, 80, 22), -30, 30),
    ("17-the-overlook-tower-fire.png", (-24, 60, -52, 8, 100, -22), 30, 30),
    ("18-the-overlook-tower-ice.png", (-9, 60, 21, 23, 100, 51), 210, 30),
]
specs = [dict(out=os.path.join(out, n), box=b, yaw=yaw, pitch=pitch, fov=40, w=1800, h=1300) for n, b, yaw, pitch in shots]
print(render.textured(build, specs))

# the plan's names and markers over what was built, to show it landed where the plan said
S = Sheet("Rimefire - as built")
m = S.map(LND.X0 + 10, LND.Z0 + 10, LND.X0 + LND.NX - 11, LND.Z0 + LND.NZ - 11, scale=5, title="FROM ABOVE",
          legend="the built world's top blocks with the plan's names over them; the south half is the north half turned",
          symmetry=None)
m.built(w, ymin=30)
for label, (x, z) in {"Ashfall Lodge": LND.SPAWN, "The Furnace": LND.FURNACE, "Rustwater": (-38, -44),
                      "The Overlook": LND.OVERLOOK, "Waystation": (-26, -38)}.items():
    m.place(x, z, label, size=12)
    m.place(-1 - x, -1 - z, {"Ashfall Lodge": "Rimehold", "The Furnace": "The Cold Hearth", "Rustwater": "Frostholm",
                              "The Overlook": "Icewatch", "Waystation": "Rime Shelter"}[label], size=12)
m.place(-0.5, -0.5, "THE SEAM", size=14)
m.objectives(PLAN.objectives().markers())
S.save(os.path.join(out, "19-topdown-annotated.png"))
