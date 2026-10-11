"""Cloudhaven's plan: an archipelago in the sky. Islands of every size float at different heights over the
void, some joined by rope bridges and stairs, others only by building. Hot-air balloons hang between them,
and airships are moored at their docks. A great double-ended airship, the Concord, floats at the centre as
the crossing between the teams.

Red holds the west (x < 0), blue the east; blue's half is red's turned half a circle about the centre,
(x, z) -> (-1 - x, -1 - z). Coordinates are world x, z (north is -z); `top` is the y of an island's grass.
"""

X_MIN, X_MAX = -132, 131
Z_MIN, Z_MAX = -100, 99


def rot(x, z):
    return -1 - x, -1 - z


SPAWN = (-92, 0)
MON_A = (-60, -50)          # Lantern Isle: the monument under the stone gazebo
MON_B = (-59, 49)           # the Hanging Gardens: the monument in the sunken garden

# Each island: centre, radius, the height of its grass, how deep its rock hangs (times r), its outline's
# raggedness, and what is on it.
ISLANDS = [
    dict(key="highmoor", name="Highmoor", at=SPAWN, r=16, top=92, deep=1.6, rag=0.18,
         what="Red's spawn: a keep with a gate to the east, a waterfall off its north rim", why="spawn"),
    dict(key="windmill", name="Windmill Isle", at=(-70, -24), r=8, top=86, deep=1.4, rag=0.25,
         what="a windmill, its sails turning nowhere", why="the step from the spawn to Lantern Isle"),
    dict(key="lantern", name="Lantern Isle", at=MON_A, r=11, top=78, deep=1.5, rag=0.2,
         what="a stone gazebo over the monument, lanterns on posts round it", why="RED MONUMENT A"),
    dict(key="sentinel", name="Sentinel Rock", at=(-80, 26), r=7, top=78, deep=1.8, rag=0.3,
         what="a crag with a lookout platform", why="the step from the spawn down to the Gardens"),
    dict(key="gardens", name="the Hanging Gardens", at=(-62, 46), r=12, top=60, deep=1.3, rag=0.2,
         what="terraced gardens, willows trailing over the rim, a sunken garden round the monument", why="RED MONUMENT B"),
    dict(key="port", name="Port Aerie", at=(-46, 4), r=13, top=72, deep=1.5, rag=0.2,
         what="the harbour: a dock with an airship moored at its pier, a warehouse, a crane", why="the forward base"),
    dict(key="gate", name="Gate Rock", at=(-26, 0), r=5, top=74, deep=1.6, rag=0.25,
         what="a rock with a gangway onto the Concord", why="the way onto the centre ship"),
    dict(key="cloudstep", name="Cloudstep", at=(-30, -44), r=7, top=70, deep=1.6, rag=0.3,
         what="a small rock at the moored airship's bow", why="the north flank"),
    dict(key="northreach", name="North Reach", at=(-19, -60), r=8, top=64, deep=1.5, rag=0.25,
         what="the north flank's last rock, a ruined arch", why="the north crossing"),
    dict(key="fernrock", name="Fernrock", at=(-30, 38), r=7, top=66, deep=1.6, rag=0.3,
         what="a mossy rock with a dovecote", why="the south flank"),
    dict(key="southreach", name="South Reach", at=(-19, 60), r=8, top=58, deep=1.5, rag=0.25,
         what="the south flank's last rock, a beacon brazier", why="the south crossing"),
]

# Little rocks drifting between the islands: parkour, cover, and the look of a broken sky.
DEBRIS = [(-78, -46, 82, 3), (-52, -28, 80, 2), (-84, 48, 70, 2), (-44, 56, 62, 3), (-22, 22, 70, 2),
          (-58, 22, 74, 2), (-104, -26, 96, 2), (-40, -60, 72, 2), (-26, -22, 78, 2), (-100, 30, 88, 2)]

# Rope bridges and stairs: (from island, to island). Every other gap is crossed by building.
BRIDGES = [("highmoor", "windmill"), ("windmill", "lantern"), ("highmoor", "sentinel"), ("sentinel", "gardens"),
           ("highmoor", "port"), ("port", "gate"), ("port", "fernrock"), ("cloudstep", "northreach"),
           ("fernrock", "southreach")]

# Hot-air balloons: (x, z, the basket's floor). Two hang in each flank's gap as stepping stones.
BALLOONS = [(-5, -63, 68, "flank"), (-5, 60, 62, "flank"), (-54, -36, 88, "free"), (-60, 26, 74, "free"),
            (-102, -18, 104, "tethered")]

# The Concord: a double-ended airship along x across the centre, its deck at y 74, symmetric under the
# half-turn so each team builds its half. The Albatross: moored along z at Port Aerie's pier.
CONCORD = dict(x0=-19, x1=18, zc=-0.5, deck=74, half=4.5)
ALBATROSS = dict(x=-33, z0=-34, z1=-12, deck=72, half=3.5)

# ---- the first build found too little ground: red had 3,500 blocks of grass for sixteen players. Every
# position above is scaled out by 1.2 from the centre and every island's radius by 1.3, so the islands grow
# more than the gaps between them do.
S_POS, S_R = 1.2, 1.3


def _p(x, z):
    return int(round(x * S_POS)), int(round(z * S_POS))


SPAWN, MON_A, MON_B = _p(*SPAWN), _p(*MON_A), _p(*MON_B)
for _i in ISLANDS:
    _i["at"] = _p(*_i["at"])
    _i["r"] = int(round(_i["r"] * S_R))
DEBRIS = [(*_p(x, z), y, r + 1) for x, z, y, r in DEBRIS]
BALLOONS = [(*_p(x, z), y, k) for x, z, y, k in BALLOONS]
CONCORD = dict(CONCORD, x0=int(round(CONCORD["x0"] * S_POS)), x1=-1 - int(round(CONCORD["x0"] * S_POS)))
ALBATROSS = dict(ALBATROSS, x=int(round(ALBATROSS["x"] * S_POS)), z0=int(round(ALBATROSS["z0"] * S_POS)),
                 z1=int(round(ALBATROSS["z1"] * S_POS)))

PLACES = [dict(key=i["key"], name=i["name"], at=i["at"], what=i["what"], why=i["why"]) for i in ISLANDS] + [
    dict(key="concord", name="the Concord", at=(-0.5, -0.5), what="the great airship at the centre", why="the middle crossing"),
    dict(key="albatross", name="the Albatross", at=(ALBATROSS["x"], (ALBATROSS["z0"] + ALBATROSS["z1"]) // 2), what="an airship moored at Port Aerie's pier",
         why="the way from the port to Cloudstep, and cover over the gap"),
]
