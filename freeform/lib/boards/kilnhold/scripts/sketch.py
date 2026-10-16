"""Kilnhold's sketch: the plan drawn and annotated before anything is built, with the checker's numbers on the sheet.

    python3 sketch.py renders/00-plan-sketch.png
"""
import sys

import numpy as np

import plan as P
import plan_check as C
import terrain
from pgmvox.read.sketch import TEAM, MapPanel, SectionPanel, Sheet

ASH, CROWNC, GATEC, DEEPC = (46, 42, 44), (196, 190, 178), (160, 168, 178), (214, 130, 70)
GALC, WATERC = (130, 138, 150), (70, 120, 210)
m = C.measure()
S = Sheet("Kilnhold - the plan")

# 1. the board from above
X0, X1, Z0, Z1 = P.X_MIN, P.X_MAX, P.Z_MIN, P.Z_MAX
mp = S.map(X0, Z0, X1, Z1, scale=5, title="THE BOARD", symmetry=P.SYM, bg=(34, 36, 44),
           legend="red's half drawn, blue's its half turn (paler); grey the Crown's roof deck, blue-grey the gate level, "
                  "orange the deep level; S spawn, M monuments, F flag; arrows the routes the plan states")
L = terrain.land()
land = [(x, z) for x in range(X0, X1 + 1) for z in (Z0,)]
mp.rect(-66, -97, 65, 96, fill=ASH, outline=(80, 80, 90))
mp.rect(*[P.DECK_BOX[i] for i in (0, 2, 1, 3)], fill=CROWNC, outline=(90, 90, 90), both=True)
mp.rect(P.APRON_BOX[0], P.APRON_BOX[2], P.APRON_BOX[1], P.APRON_BOX[3], fill=GATEC, outline=(70, 70, 80), both=True)
for name, (x0, x1, z0, z1, floor, h) in P.ROOMS.items():
    fill = DEEPC if floor == P.DEEP else GATEC
    mp.rect(x0, z0, x1, z1, fill=fill, outline=(30, 30, 40), width=2, both=True)
for nm, pa in P.PASSAGES.items():
    if "parts" in pa:
        for x0, x1, z0, z1 in pa["parts"]:
            mp.rect(x0, z0, x1, z1, fill=DEEPC, outline=(30, 30, 40), both=True)
    else:
        mp.rect(pa["x"][0], pa["z"][0], pa["x"][1], pa["z"][1], fill=DEEPC if pa["floor"] == P.DEEP else GALC,
                outline=(30, 30, 40), both=True)
tx, tz = P.TOWER
mp.poly([(tx + 9.5 * np.cos(a), tz + 9.5 * np.sin(a)) for a in np.linspace(0, 6.283, 40)], fill=(110, 110, 116),
        outline=(40, 40, 40), both=True)
mp.rect(*[P.PIT_BOX[i] for i in (0, 2, 1, 3)], fill=(90, 80, 70), outline=(40, 40, 40), both=True)
mp.poly([(19.5 * np.cos(a), 19.5 * np.sin(a)) for a in np.linspace(0, 6.283, 48)], fill=(120, 70, 50), outline=(40, 40, 40))
mp.poly([(6.2 * np.cos(a), 6.2 * np.sin(a)) for a in np.linspace(0, 6.283, 32)], fill=(240, 130, 30), outline=(40, 40, 40))
for name, pts in (("spawn to the Crown Beacon", "spawn to the Crown Beacon"),
                  ("spawn to the Pump Hall Monument", "spawn to the Pump Hall Monument"),
                  ("spawn to the flag", "spawn to the flag")):
    mp.line(P.ROUTES[pts], TEAM["red"], 2, arrow=True, both=True)
mp.line(P.ROUTES["enemy spawn to the Pump Hall Monument by the culvert"], (60, 60, 200), 2, dash=True, arrow=True)
mp.line(P.ROUTES["enemy spawn to the Crown Beacon by the west ramp"], (60, 60, 200), 2, dash=True, arrow=True)
for name, (x, z) in P.PLACES:
    mp.place(x, z, name, size=10, both=False)
mp.objectives(P.objectives().markers())



mp.callout(-23, -34, "the apron's ramps are at its ends", dx=-50, dz=34)

# 2. the levels
def level_map(title, legend, rooms, passages):
    p = MapPanel(-66, -97, 65, -2, scale=3, title=title, legend=legend, bg=(34, 36, 44))
    p.rect(-66, -97, 65, -2, fill=(44, 42, 46), outline=(80, 80, 90))
    for x0, x1, z0, z1, colour in rooms:
        p.rect(x0, z0, x1, z1, fill=colour, outline=(30, 30, 40), width=2)
    for x0, x1, z0, z1, colour in passages:
        p.rect(x0, z0, x1, z1, fill=colour, outline=(30, 30, 40))
    return p


def rooms_of(floor):
    return [(x0, x1, z0, z1, DEEPC if floor == P.DEEP else GATEC) for k, (x0, x1, z0, z1, f, h) in P.ROOMS.items() if f == floor]


crown_level = level_map("THE CROWN (77)", "the roof deck over the bunker: the beacon's court, pillboxes, the cooling basin, "
                        "the mast; the ramps from the field and from the gallery arrive at the front",
                        [(-58, 57, -93, -55, CROWNC)], [])
crown_level.marker(*P.BEACON_AT, "M", TEAM["red"])
crown_level.place(-34, -76, "Crown Beacon", size=10)
crown_level.place(0, -66, "pillboxes and cover", size=10)
crown_level.place(34, -85, "cooling basin", size=10)
crown_level.place(0, -88, "mast on its podium", size=10)
crown_level.line(P.ROUTES["spawn to the Crown Beacon"][-4:], TEAM["red"], 2, arrow=True)
gate_level = level_map("THE GATE LEVEL (65, galleries 70)", "spawn, spine, gate hall with its galleries and the capture dais, the "
                       "workshop and command post; slab ramps go down to the deep level and up to the Crown",
                       rooms_of(P.GATE) + [(-12, 11, -94, -80, GATEC)],
                       [(-39 + 6, -16, -62, -59, GALC), (15, 32, -62, -59, GALC), (-37, -16, -58, -55, GALC),
                        (15, 36, -58, -55, GALC)])
gate_level.marker(*P.SPAWN[::2], "S", TEAM["red"])
gate_level.rect(-4, -66, 3, -58, fill=(210, 60, 60), outline=(30, 30, 40))
gate_level.place(0, -62, "capture dais", size=10)
deep_level = level_map("THE DEEP LEVEL (57)", "the pump hall under its monument, the turbine hall and the flag's shrine, the cross "
                       "gallery, and the culverts from the tower's court and the quarry pit",
                       rooms_of(P.DEEP) + [(52, 56, -70, -64, DEEPC)],
                       [(-33, 32, -70, -67, DEEPC)] + [(x0, x1, z0, z1, DEEPC) for x0, x1, z0, z1 in P.PASSAGES["culvert_w"]["parts"]]
                       + [(44, 47, -58, -44, DEEPC)])
deep_level.marker(*P.PUMP_AT, "M", TEAM["red"])
deep_level.marker(P.FLAG_POST[0], P.FLAG_POST[2], "F", TEAM["red"])
S.row(crown_level, gate_level, deep_level)

# 3. sections, true scale
H = L.H


def section_across(z, title, legend):
    sec = SectionPanel(X0, X1, 40, 100, scale=5, title=title, legend=legend)
    col = [int(H[x - X0, z - Z0]) for x in range(X0, X1 + 1)]
    sec.profile([(x, c) for x, c in zip(range(X0, X1 + 1), col)], fill=(96, 92, 92), outline=(50, 50, 50))
    return sec


a = section_across(-62, "ACROSS THE BUNKER AT Z -62", "true scale: the gate hall between the descents, the pump hall west, "
                   "the turbine hall east, the cross gallery under the nave, the Crown on top")
for name, (x0, x1, z0, z1, floor, h) in P.ROOMS.items():
    if z0 <= -62 <= z1:
        a.band(x0, x1 + 1, floor + 1, floor + h + 1, fill=DEEPC if floor == P.DEEP else GATEC, outline=(30, 30, 30), text=name)
a.band(-15, 15, P.GATE + 1, P.GATE + 11, fill=GATEC, outline=(30, 30, 30))
for xa, xb, fl in ((-33, -16, True), (15, 32, False)):                    # the descents, as ramps
    pts = [(xa, P.DEEP + 1), (xb + 1, P.GATE + 1)] if fl else [(xa, P.GATE + 1), (xb + 1, P.DEEP + 1)]
    a.d.polygon([(a.px(pts[0][0]), a.py(pts[0][1])), (a.px(pts[1][0]), a.py(pts[1][1])),
                 (a.px(pts[1][0]), a.py(pts[1][1] + 6)), (a.px(pts[0][0]), a.py(pts[0][1] + 6))], fill=GALC, outline=(30, 30, 30))
a.level(P.CROWN + 1, "the Crown, 77", (200, 90, 40), dash=True)
a.level(P.FIELD + 1, "the field, 62", (60, 160, 90), dash=True)
a.callout(-43, 70, "pump hall: the monument floats over the sump", dx=-10, dy=-22)
a.callout(0, 68, "gate hall, 10 high", dx=40, dy=-26)
b_x = P.Z_MIN
secz = SectionPanel(Z0, -1, 40, 100, scale=5, title="DOWN THE AXIS, X -1",
                    legend="true scale from the back wall to the middle: muster hall, spine, gate hall, the facade, the apron, the field, the crater")
colz = [int(H[-1 - X0, z - Z0]) for z in range(Z0, 0)]
secz.profile([(z, c) for z, c in zip(range(Z0, 0), colz)], fill=(96, 92, 92), outline=(50, 50, 50))
for name, (x0, x1, z0, z1, floor, h) in P.ROOMS.items():
    if x0 <= -1 <= x1 and floor == P.GATE:
        secz.band(z0, z1 + 1, floor + 1, floor + h + 1, fill=GATEC, outline=(30, 30, 30), text=name)
secz.band(-53, -45, P.GATE + 1, P.GATE + 9, fill=GATEC, outline=(30, 30, 30), text="gate")
secz.level(P.CROWN + 1, "the Crown, 77", (200, 90, 40), dash=True)
secz.level(P.FIELD + 1, "the field, 62", (60, 160, 90), dash=True)
secz.callout(-33, 66, "apron 65", dx=20, dy=-22)
secz.callout(-6, 60, "crater: lava lake, shelf 59", dx=-30, dy=-20)
S.row(a, secz)

# 4. the check
S.table(C.rows(m), width=mp.img.width)
S.save(sys.argv[1])
