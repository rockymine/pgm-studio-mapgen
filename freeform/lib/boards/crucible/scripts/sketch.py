"""Crucible's sketch: the plan drawn before anything is built — the board from above with its roads, places and
objectives, each level of red's foundry on its own panel, a section down the crucible's axis, and the checker's
numbers.

    python3 sketch.py ../renders/00-plan-sketch.png
"""
import io
import os
import sys
from contextlib import redirect_stdout

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import land  # noqa: E402
import plan as P  # noqa: E402
from pgmvox.plan.raster import Raster  # noqa: E402
from pgmvox.read.sketch import TEAM, SectionPanel, Sheet  # noqa: E402
from pgmvox.surface.terrain import slope_deg  # noqa: E402

with redirect_stdout(io.StringIO()):
    import plan_check as C

H = np.round(land.heights()).astype(int)
SURF = Raster((land.X0, land.X1), (land.Z0, land.Z1), ["ash", "rock", "lava", "pit", "flow", "cone", "void"], 0,
              "ash", P.SYM)
SURF.H[:] = H
X, Z = land.grid()
lobe = land.sym(land.flow()[0] & (Z >= 0))
SURF.K[lobe] = SURF.kinds["flow"]
cone = land.sym(np.hypot(X - land.CONE[0], Z - land.CONE[1]) < land.CONE[2])
SURF.K[cone] = SURF.kinds["cone"]
e, _ = land.pit_polar(X, Z)
SURF.K[land.sym((e <= 1.0) & (Z >= 0))] = SURF.kinds["pit"]
SURF.K[slope_deg(H) > 45] = SURF.kinds["rock"]
SURF.K[(H <= land.LAVA) | land.lava_channel()] = SURF.kinds["lava"]
SURF.K[~land.inside()] = SURF.kinds["void"]
COL = {"ash": (96, 78, 66), "rock": (128, 132, 140), "lava": (226, 104, 30), "pit": (176, 170, 160),
       "flow": (52, 48, 50), "cone": (140, 72, 58), "void": (40, 44, 56)}
STYLE_COL = {"hall": (196, 120, 70), "crew": (170, 110, 80), "pour": (200, 180, 150), "loggia": (200, 180, 150),
             "furnace": (210, 140, 60), "store": (90, 180, 190), "run": (150, 120, 96), "tunnel": (150, 120, 96),
             "gate": (150, 120, 96), "door": (60, 60, 60)}

S = Sheet("Crucible - the plan")
red_half = lambda x, z: z < 0                                     # blue's half drawn paler
m = S.map(land.X0, land.Z0, land.X1, land.Z1, scale=4, title="THE BOARD",
          legend="ash brown, rock grey, lava orange, pit pale, black flow dark, cinder cone red; roads dashed; "
                 "C crucible, W monument, w wool, S spawn; blue's half paler")
m.raster(SURF, COL, image_half=red_half)
for road in land.ROADS:
    m.line(road, colour=(230, 220, 200), width=3, dash=True, both=True)
m.objectives(P.objectives().markers())
m.place(0, 80, "red's foundry (in the mountain)")
m.place(*P.SYM.point(0, 80), "blue's foundry")
m.callout(-12, 8, "the slag tip", dx=-50, dz=-26)
m.callout(-6, 30, "the sinkhole: the lava tube", dx=-70, dz=10)
m.callout(47, 38, "the cinder cone", dx=30, dz=-30)
m.callout(22, 45, "the casting pit, the gantry", dx=40, dz=40)
m.callout(-44, 30, "the black flow", dx=-30, dz=-30)
m.callout(-30, 58, "the loading gate", dx=-40, dz=30)
m.callout(-60, 46, "the flank cave", dx=-10, dz=40)
m.callout(-11, 54, "the cooling pond", dx=10, dz=40)

panels = []
for title, feet in [("LEVEL 0 (feet 52): the loading gate and hall, the crew hall, the pour room and its loggia", P.L0),
                    ("LEVEL 1 (feet 40): the pit's floor, the furnace hall, the slag run", P.L1),
                    ("LEVEL 2 (feet 28): the cold store, its passage, the flank cave's end", P.L2)]:
    p = S.map(-70, 0, 69, 99, scale=4, title=title,
              legend="red's half; rooms by style (the store blue), ramps yellow with the feet at their ends, the "
                     "caves brown")
    p.raster(SURF, COL)
    p.dim(0.45)
    for s in P.SPACES:
        if s.feet == feet:
            p.rect(s.x0, s.z0, s.x1, s.z1, fill=STYLE_COL[s.style], outline=(20, 20, 20))
            if (s.x1 - s.x0) * (s.z1 - s.z0) > 30:
                p.label((s.x0 + s.x1) / 2, (s.z0 + s.z1) / 2, s.name, size=10)
    for r in P.RAMPS:
        for leg in r.legs:
            if min(leg.feet0, leg.feet1) <= feet + 1 and max(leg.feet0, leg.feet1) >= feet - 1 or \
                    (min(leg.feet0, leg.feet1) < feet < max(leg.feet0, leg.feet1)):
                p.rect(leg.x0, leg.z0, leg.x1, leg.z1, fill=(210, 190, 120), outline=(20, 20, 20))
                p.label(leg.x0 - 3, leg.z0 - 2, f"{leg.feet0:g}", size=10)
                p.label(leg.x1 + 4, leg.z1 + 2, f"{leg.feet1:g}", size=10)
    if feet == P.L0:
        p.marker(P.SPAWN_AT[0], P.SPAWN_AT[2], "S", colour=TEAM["red"], r=7)
        p.marker(P.MONUMENT[0], P.MONUMENT[2], "W", colour=(130, 200, 60), r=7)
        g = P.GANTRY
        p.rect(g["x0"], g["z0"], g["x1"], g["z1"], fill=(220, 220, 220), outline=(20, 20, 20))
        p.label(g["x0"] + 6, g["z0"] - 3, f"gantry deck, feet {g['y'] + 1}", size=10)
    if feet == P.L1:
        c = P.CORE
        p.rect(c.x0, c.z0, c.x1, c.z1, fill=(40, 30, 60), outline=(250, 120, 40), width=2)
        p.label(22, 36, "the crucible over the pit floor", colour=(255, 255, 255), size=10)
        p.line([(x, z) for x, _, z, _ in P.TUBE], colour=(130, 115, 95), width=7)
        p.label(-6, 26, "lava tube", size=10)
    if feet == P.L2:
        p.marker(P.WOOL_AT[0], P.WOOL_AT[2], "w", colour=(130, 200, 60), r=7)
        p.line([(x, z) for x, _, z, _ in P.FLANK], colour=(130, 115, 95), width=7)
        for x, _, z, f in [(x, f, z, f) for x, f, z, _ in P.FLANK[::2]]:
            p.label(x + 6, z, f"{f}", size=10)
        p.label(-60, 40, "flank cave, feet 51 to 28", size=10)
    panels.append(p)

sec = SectionPanel(0, 99, 0, 112, scale=4, title="DOWN THE CRUCIBLE'S AXIS",
                   legend="x 22, the rift at left; rooms by style, the crucible dark, the gantry grey; the leak line "
                          "dashed")
sec.profile([(z, H[22 - land.X0, z - land.Z0]) for z in range(0, 100)])
for s in P.SPACES:
    if s.x0 <= 22 <= s.x1:
        sec.band(s.z0, s.z1 + 1, s.feet, s.feet + s.h, fill=STYLE_COL[s.style],
                 text=s.name if s.z1 - s.z0 > 6 else None)
for r in P.RAMPS:
    for x, z, f in r.cells():
        if x == 22:
            sec.band(z, z + 1, f, f + r.h, fill=(210, 190, 120))
c = P.CORE
sec.band(c.z0, c.z1 + 1, c.y0, c.y1 + 1, fill=(40, 30, 60), text="crucible")
g = P.GANTRY
sec.band(g["z0"], g["z1"] + 1, g["y"] - 1, g["y"] + 1, fill=(200, 200, 200))
sec.level(P.LEAK_Y, f"leak line y {P.LEAK_Y}", dash=True)
sec.level(land.LAVA, "lava sea", colour=(220, 70, 30))
sec.level(P.KILL_Y, f"kill height {P.KILL_Y}", colour=(120, 120, 120), dash=True)
S.row(sec)

S.table(C.rows, width=m.img.width)
S.save(sys.argv[1])
