"""Coldbore's sketch: the plan drawn before anything is built — the board from above with its roads, places and
objectives, each level of the station on its own panel, a section down the gate's axis, and the checker's numbers.

    python3 sketch.py ../renders/00-plan-sketch.png
"""
import io
import sys
from contextlib import redirect_stdout

import numpy as np

import land
import plan as P
from pgmvox.plan.raster import Raster
from pgmvox.read.sketch import TEAM, SectionPanel, Sheet

with redirect_stdout(io.StringIO()):
    import plan_check as C

H, X, Z = land.heights()
top = np.round(H).astype(int)
SURF = Raster((land.X0, land.X1), (land.Z0, land.Z1), ["snow", "rock", "lava", "forecourt"], 0, "snow", P.SYM)
SURF.H[:] = top
from pgmvox.surface.terrain import slope_deg  # noqa: E402
SURF.K[slope_deg(top) > 40] = SURF.kinds["rock"]
SURF.K[top <= land.LAVA] = SURF.kinds["lava"]
f = land.FORECOURT
SURF.rect(f["x0"], f["x1"], f["z0"], f["z1"] - 1, land.GROUND, "forecourt")
COL = {"snow": (232, 238, 244), "rock": (120, 124, 130), "lava": (226, 104, 30), "forecourt": (170, 160, 150)}
LEVEL_COL = {"hall": (196, 120, 70), "room": (176, 140, 100), "corridor": (150, 120, 96), "link": (150, 120, 96),
             "vault": (90, 150, 210), "door": (40, 40, 40)}

S = Sheet("Coldbore - the plan")
red_half = lambda x, z: land.across(np.array([x], float), np.array([z], float))[0] < 0   # blue's half drawn paler

m = S.map(land.X0, land.Z0, land.X1, land.Z1, scale=4, title="THE BOARD",
          legend="snow white, rock grey, lava orange, forecourt brown; roads dashed; C core, W wool, M monument, "
                 "S spawn; blue's half paler")
m.raster(SURF, COL, image_half=red_half)
for road in P.ROADS:
    m.line(road, colour=(90, 80, 70), width=3, dash=True, both=True)
m.objectives(P.objectives().markers())
m.place(-40, 40, "snowfield", both=True)
m.place(0, 82, "red's station (plateau)")
m.place(*P.SYM.point(0, 82), "blue's station")
m.callout(-1, 0, "the bore's stump in the lava", dx=60, dz=-30)
m.callout(-44, 30, "the culvert into red's barracks", dx=-10, dz=40)
m.callout(-17, 45, "vent hatch: ladder to the reactor", dx=-70, dz=-30)
m.callout(-1, 13, "the broken road bridge", dx=50, dz=26)
m.callout(-58, 26, "crevasse", dx=10, dz=-40)

panels = []
for name, feet, extra in [("LEVEL 0 (feet 72): the gate, the hall, the ramp into the mountain", P.L0, None),
                          ("LEVEL 1 (feet 52): the turn hall, the reactor, the barracks, the drop", P.L1, None),
                          ("LEVEL 2 (feet 34): the vault, the service corridor, the gallery, the cave", P.L2, None)]:
    p = S.map(-75, -10, 74, 99, scale=4, title=name,
              legend="red's half; halls orange, rooms tan, corridors brown, the vault blue, doors black; stairs "
                     "dotted with the feet at their ends")
    p.raster(SURF, COL)
    p.dim(0.35)
    for s in P.SPACES:
        if s.feet == feet:
            p.rect(s.x0, s.z0, s.x1, s.z1, fill=LEVEL_COL[s.kind], outline=(20, 20, 20))
            if (s.x1 - s.x0) * (s.z1 - s.z0) > 30:
                p.label((s.x0 + s.x1) / 2, (s.z0 + s.z1) / 2, s.name, size=10)
    for fl in P.FLIGHTS:
        if min(fl.feet0, fl.feet1) <= feet + 14 and max(fl.feet0, fl.feet1) >= feet - 1:
            p.rect(fl.x0, min(fl.z0, fl.z1), fl.x1, max(fl.z0, fl.z1), fill=(210, 190, 120), outline=(20, 20, 20))
            p.label(fl.x1 + 6, fl.z0, str(fl.feet0), size=10)
            p.label(fl.x1 + 6, fl.z1, str(fl.feet1), size=10)
    ring = P.helix_ring()
    p.poly(ring, outline=(240, 220, 120), width=2)
    for x, z, door_feet in P.DOORS:
        if door_feet == feet:
            p.marker(x, z, "D", colour=(30, 30, 30), r=6)
    if feet == P.L1:
        p.rect(P.CORE.x0, P.CORE.z0, P.CORE.x1, P.CORE.z1, fill=(40, 30, 60), outline=(250, 120, 40), width=2)
        p.label(-1, 55, "core", colour=(255, 255, 255), size=10)
        p.marker(P.LADDER["x"], P.LADDER["z0"], "L", colour=(30, 30, 30), r=6)
        p.rect(P.DROP["x0"], P.DROP["z0"], P.DROP["x1"], P.DROP["z1"], fill=(70, 120, 200), outline=(20, 20, 20))
        p.line([(x, z) for x, _, z, _ in P.CULVERT], colour=(120, 100, 80), width=6)
    if feet == P.L2:
        g = P.gallery_cells()
        p.zone(set(g) and [(x, z) for x, z in g], colour=(196, 120, 70), style="fill") if False else None
        xs = [x for x, z in g]
        p.rect(min(xs), min(z for x, z in g), max(xs), P.GALLERY["z1"], fill=(196, 120, 70), outline=(20, 20, 20))
        p.label(0, 18, "fissure gallery", size=10)
        p.rect(P.POOL["x0"], P.POOL["z0"], P.POOL["x1"], P.POOL["z1"], fill=(60, 110, 190), outline=None)
        p.marker(P.WOOL_AT[0], P.WOOL_AT[2], "W", colour=(240, 140, 30), r=7)
        p.rect(P.VAULT_DOOR.x0, P.VAULT_DOOR.z0, P.VAULT_DOOR.x1, P.VAULT_DOOR.z1, fill=(20, 20, 20))
        for passage in P.CAVE:
            p.line([(x, z) for x, _, z, _ in passage], colour=(130, 115, 95), width=7)
        for x, _, z, r in P.LAVA_PONDS:
            p.rect(x - r, z - r, x + r, z + r, fill=(226, 104, 30), outline=None)
        p.label(-45, 36, "cave, lava ponds", size=10)
    panels.append(p)

# a section down the gate's axis, x = 0, true scale
sec = SectionPanel(-30, 99, 10, 112, scale=4, title="DOWN THE GATE'S AXIS",
                   legend="x 0, south (the fissure) at left; rock brown, rooms orange, the vault blue, lava red; "
                          "the leak height dashed")
sec.profile([(z, top[0 - land.X0, z - land.Z0]) for z in range(-30, 100)])
for s in P.SPACES:
    if s.x0 <= 0 <= s.x1:
        sec.band(s.z0, s.z1 + 1, s.feet, s.feet + s.h, fill=(90, 150, 210) if s.kind == "vault" else (196, 120, 70),
                 text=s.name if s.z1 - s.z0 > 8 else None)
for fl in P.FLIGHTS:
    if fl.x0 <= 0 <= fl.x1:
        for x, z, feet in fl.cells():
            if x == 0:
                sec.band(z, z + 1, feet, feet + fl.h, fill=(210, 190, 120))
g = [z for x, z in P.gallery_cells() if x == 0]
sec.band(min(g), P.GALLERY["z1"] + 1, P.L2, P.L2 + P.GALLERY["h"], fill=(196, 120, 70), text="gallery")
sec.band(P.CORE.z0, P.CORE.z1 + 1, P.CORE.y0, P.CORE.y1 + 1, fill=(40, 30, 60), text="core")
sec.band(P.HATCH.z0, P.HATCH.z1 + 1, P.HATCH.y0, P.HATCH.y0 + 1, fill=(20, 20, 20))
sec.level(P.LEAK_Y, f"leak at y {P.LEAK_Y} and under", dash=True)
sec.level(land.LAVA, "lava", colour=(220, 70, 30))
S.row(sec)



S.table(C.rows, width=m.img.width)
S.save(sys.argv[1])
