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
SURF = Raster((land.X0, land.X1), (land.Z0, land.Z1), ["snow", "rock", "lava", "forecourt", "void"], 0, "snow", P.SYM)
SURF.H[:] = top
from pgmvox.surface.terrain import slope_deg  # noqa: E402
SURF.K[slope_deg(top) > 40] = SURF.kinds["rock"]
SURF.K[top <= land.LAVA] = SURF.kinds["lava"]
for f in land.COURTS:
    SURF.rect(f["x0"], f["x1"], f["z0"], f["z1"], land.GROUND, "forecourt", both=True)
SURF.K[~land.inside()] = SURF.kinds["void"]
COL = {"snow": (232, 238, 244), "rock": (120, 124, 130), "lava": (226, 104, 30), "forecourt": (170, 160, 150), "void": (40, 44, 56)}
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
m.callout(28, 39, "the store's fallen ceiling", dx=40, dz=-30)
m.callout(-40, 48, "the gate", dx=-40, dz=-30)
m.callout(34, 50, "the generator house", dx=40, dz=20)
m.callout(-1, 13, "the broken road bridge", dx=50, dz=26)
m.callout(-58, 26, "crevasse", dx=10, dz=-40)

panels = []
for name, feet in [("LEVEL 0 (feet 72): gate, entrance hall, spawn and iron rooms, generator house, balcony", P.L0),
                   ("LEVEL 1 (feet 58): the reactor hall's floor, the south corridor, the collapsed store", P.L1),
                   ("LEVEL 2 (feet 44): the gallery, the service corridor, the vault, the cave", P.L2)]:
    p = S.map(-75, -10, 74, 99, scale=4, title=name,
              legend="red's half; halls orange, rooms tan, corridors brown, the vault blue; ramps yellow with the "
                     "feet at their ends; decks grey")
    p.raster(SURF, COL)
    p.dim(0.35)
    for s in P.SPACES:
        if s.feet == feet or (s.name == "reactor hall" and feet == P.L0):
            p.rect(s.x0, s.z0, s.x1, s.z1, fill=LEVEL_COL[s.kind], outline=(20, 20, 20))
            if (s.x1 - s.x0) * (s.z1 - s.z0) > 30:
                p.label((s.x0 + s.x1) / 2, (s.z0 + s.z1) / 2, s.name, size=10)
    for d in P.DECKS:
        if d.feet == feet:
            p.rect(d.x0, d.z0, d.x1, d.z1, fill=(150, 150, 150), outline=(20, 20, 20))
    for r in P.RAMPS:
        for leg in r.legs:
            if min(leg.feet0, leg.feet1) <= feet + 1 and max(leg.feet0, leg.feet1) >= feet - 1:
                p.rect(leg.x0, leg.z0, leg.x1, leg.z1, fill=(210, 190, 120), outline=(20, 20, 20))
                p.label(leg.x0 - 3, leg.z0 - 2, f"{leg.feet0:g}", size=10)
                p.label(leg.x1 + 4, leg.z1 + 2, f"{leg.feet1:g}", size=10)
    if feet == P.L1:
        p.rect(P.PIT.x0, P.PIT.z0, P.PIT.x1, P.PIT.z1, fill=(30, 30, 30), outline=None)
        p.rect(P.CORE.x0, P.CORE.z0, P.CORE.x1, P.CORE.z1, fill=(40, 30, 60), outline=(250, 120, 40), width=2)
        p.label(-1, 72, "core over its pit", colour=(255, 255, 255), size=10)
        rh = P.ROOF_HOLE
        p.rect(rh["x0"], rh["z0"], rh["x1"], rh["z1"], fill=(230, 238, 244), outline=(20, 20, 20))
    if feet == P.L0:
        p.marker(P.SPAWN_AT[0], P.SPAWN_AT[2], "S", colour=TEAM["red"], r=7)
        p.marker(P.MONUMENT[0], P.MONUMENT[2], "M", colour=(40, 160, 200), r=7)
        for f in (P.FACADE, P.ANNEX):
            p.rect(f["x0"], f["z0"], f["x1"], f["z0"] + 1, fill=(70, 30, 30), outline=None)
    if feet == P.L2:
        g = P.gallery_cells()
        xs = [x for x, z in g]
        p.rect(min(xs), min(z for x, z in g), max(xs), P.GALLERY["z1"], fill=(196, 120, 70), outline=(20, 20, 20))
        p.label(0, 22, "fissure gallery", size=10)
        p.marker(P.WOOL_AT[0], P.WOOL_AT[2], "W", colour=(240, 140, 30), r=7)
        p.rect(P.VAULT_DOOR.x0, P.VAULT_DOOR.z0, P.VAULT_DOOR.x1, P.VAULT_DOOR.z1, fill=(20, 20, 20))
        for passage in P.CAVE:
            p.line([(x, z) for x, _, z, _ in passage], colour=(130, 115, 95), width=7)
        for x, _, z, r in P.LAVA_PONDS:
            p.rect(x - r, z - r, x + r, z + r, fill=(226, 104, 30), outline=None)
        p.label(-48, 40, "cave, lava ponds", size=10)
    panels.append(p)

# a section across the reactor hall and down to the gallery, x 0, true scale
sec = SectionPanel(-30, 99, 10, 116, scale=4, title="DOWN THE STATION'S AXIS",
                   legend="x 0, south (the fissure) at left; rooms orange, ramps yellow, the core dark; the leak "
                          "height dashed")
sec.profile([(z, top[0 - land.X0, z - land.Z0]) for z in range(-30, 100)])
for s in P.SPACES:
    if s.x0 <= 0 <= s.x1:
        sec.band(s.z0, s.z1 + 1, s.feet, s.feet + s.h, fill=(196, 120, 70), text=s.name if s.z1 - s.z0 > 8 else None)
g = [z for x, z in P.gallery_cells() if x == 0]
sec.band(min(g), P.GALLERY["z1"] + 1, P.L2, P.L2 + P.GALLERY["h"], fill=(196, 120, 70), text="gallery")
for r in P.RAMPS:
    for x, z, f in r.cells():
        if x == 0:
            sec.band(z, z + 1, f, f + r.h, fill=(210, 190, 120))
for d in P.DECKS:
    if d.x0 <= 0 <= d.x1:
        sec.band(d.z0, d.z1 + 1, d.feet - 1, d.feet, fill=(120, 120, 120))
sec.band(P.PIT.z0, P.PIT.z1 + 1, P.PIT.y0, P.PIT.y1 + 1, fill=(30, 30, 30))
sec.band(P.CORE.z0, P.CORE.z1 + 1, P.CORE.y0, P.CORE.y1 + 1, fill=(40, 30, 60), text="core")
sec.level(P.LEAK_Y, f"leak at y {P.LEAK_Y} and under", dash=True)
sec.level(land.LAVA, "lava", colour=(220, 70, 30))
S.row(sec)

S.table(C.rows, width=m.img.width)
S.save(sys.argv[1])
