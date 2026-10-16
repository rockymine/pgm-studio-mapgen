"""Hoarfire's sketch: the plan drawn and annotated before anything is built, the checker's numbers on it.

    python3 sketch.py ../renders/00-plan-sketch.png
"""
import contextlib
import io
import math
import sys

import numpy as np

import plan as P
from pgmvox.plan import graph as G
from pgmvox.read.sketch import TEAM, SectionPanel, Sheet

with contextlib.redirect_stdout(io.StringIO()):
    import plan_check as C

R = P.build()
S = Sheet("Hoarfire - the plan (Rowan north, Sloe its mirror south)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="THE BOARD",
          legend="kinds by colour, lit by height; Sloe's half paler; S spawn, M Rime Monument (packed ice), "
                 "C Ember Core; red routes Rowan's walks to its own goals, dashed Rowan's attack on Sloe's",
          symmetry=R.symmetry)
m.raster(R, P.COLOURS, image_half=lambda x, z: z >= 0)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
for cells in (C.MON, C.CORE):
    D, prev = C.D["red"]
    _, _, p = G.measure(D, prev, C.E, cells)
    m.route(p[::2] + [p[-1]], TEAM["red"], width=3)
for cells in (C.image(C.MON), C.image(C.CORE)):
    D, prev = C.D["red"]
    _, _, p = G.measure(D, prev, C.E, cells)
    m.line([(x + 0.5, z + 0.5) for x, z in p[::3] + [p[-1]]], TEAM["red"], width=2, dash=True, arrow=True)
m.objectives(P.objectives().markers())
m.callout(-46, -63, "snout cliff, 9 over the shelf, 13 from the monument", dx=60, dz=-50)
m.callout(52, -54, "terrace 12 from the core, 9 above it", dx=-40, dz=-60)
m.callout(-50, -14, "Ice Cave: tarn bank to a ledge in the Rift's cliff", dx=40, dz=40)
m.callout(1, -10, "the Thaw falls into the void", dx=60, dz=30)
m.zone(R.mask("rift"), (240, 230, 120), style="dots", step=6)
m.callout(-62, 0, "the Rift: void, a build zone edge to edge; 16 at its narrowest", dx=60, dz=-6)

x_sec = SectionPanel(R.x_min, R.x_max, P.KILL_Y - 4, 82, scale=5, title="ACROSS ROWAN'S HALF",
                     legend="along x at z -50: the monument's shelf, the Thaw, the core's pit, Kiln Hill; true scale")
x_sec.raster(R, "x", -50, P.COLOURS)
x_sec.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
x_sec.callout(-36, P.MONUMENT_BOX.y1 + 1, "monument floats 3 over the shelf", dx=20, dy=-20)
x_sec.callout(38, P.CORE_BOX.y1 + 1, "core over the Ember Pit", dx=-30, dy=-20)
z_sec = SectionPanel(R.z_min, R.z_max, P.KILL_Y - 4, 82, scale=4, title="DOWN THE THAW",
                     legend="along z at x 0: lodge, court, the dell, the falls, the Rift, Sloe's half; true scale")
z_sec.raster(R, "z", 0, P.COLOURS)
z_sec.level(P.KILL_Y, "kill")
S.row(x_sec, z_sec)
S.table(C.rows, width=m.img.width)
S.save(sys.argv[1])
