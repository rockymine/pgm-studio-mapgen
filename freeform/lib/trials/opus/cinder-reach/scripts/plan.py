"""Cinder Reach: the plan. Destroy the core, one a team.

Identity: two grey ash shelves face each other across a smoking fissure, and each team's core hangs in the open
over the vent of a breached cinder cone forward of its lodge, reached around a hot pond, down off a basalt ridge,
up a lava tube under a scorched wood, and through a quarrymen's hamlet.

Everything is drawn for red (west, x < 0); blue's half is red's turned half a circle, (x, z) -> (-1 - x, -1 - z),
pgmvox's Symmetry("half"). Heights follow the library: H is the y of the floor block, a player stands at H + 1.

    land()        the red half's heights, water, outline, underside and places, cached: plan, sketch, gen read one
    build()       the plan Raster over the whole board: storey 0 the ground, storey 1 the lava tube
    objectives()  the teams, red's spawn and core (blue's are their images), the observers' point
    houses()      the hamlet and the lodge as library Houses with their footprints and doors
"""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")))   # freeform/lib
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))               # trials/opus (common)

import numpy as np  # noqa: E402

import common  # noqa: E402,F401
from pgmvox import landform as LF  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.noise import fbm, ridged, smoothstep, spline  # noqa: E402
from pgmvox import noise  # noqa: E402
from pgmvox import field as F  # noqa: E402
from pgmvox.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import island_bottom, slope_deg  # noqa: E402

BOARD = "cinder-reach"
X_MIN, X_MAX = -104, 103
Z_MIN, Z_MAX = -72, 71
SYM = Symmetry("half")
RENT = 24                       # the build zone: |x| <= 24, the whole fissure and nothing of either shelf's interior
MAX_BUILD = 80

# ---- the objectives (red's) ----------------------------------------------------------------------------------
SPAWN = (-84, 58, -6)           # feet on the lodge terrace, floor 57
TERRACE = (-90, -13, -78, 1)    # x0, z0, x1, z1: the paved terrace, floor 57
TERRACE_Y = 57
CORE = (-51, 24)                # the core's centre column; its box is 5 x 5 x 5
CORE_Y = 55                     # the casing's lowest course: four over the bowl's top, over a stone platform
BOWL_Y = 50                     # the bowl's floor
VENT_BOTTOM = 47                # the platform under the casing, three below the bowl's top: lava falls onto it
RIM_Y = 56                      # the cone's crest
LEAK = 5

# ---- the places (red's), each a reason to go there ------------------------------------------------------------
POND = ((-23, 27), 6.5, 5.0, 50)          # centre, rx, rz, water surface: Steam Pond, in front of the core
SPINE = [(-10, 46), (-26, 45), (-40, 46), (-50, 47)]   # the ridge's crest line, rising west
SPINE_TOP = 67                            # its crag at the west end, over the cone: eight over the casing's top (59)
SINK = ((-36, 6), 7.5, 43)                # the sinkhole in the wood: centre, radius, floor block
TUBE = [(-8, 46, 4, 2.6), (-14, 45, 4, 2.8), (-22, 44, 5, 3.0), (-30, 44, 6, 2.8), (-35, 44, 6, 2.4)]
CAIRN = (-30, -38)                        # the ruined watch tower on the north flats, on the tallest knoll
KNOLLS = [((-30, -38), 10, 8), ((-56, -38), 9, 6), ((-36, -57), 8, 5)]   # centre, radius, rise
WOOD = [(-50, -12), (-20, -12), (-18, 12), (-28, 16), (-44, 12), (-52, 2)]   # the Scorch Wood, acacia
POOLS = [((-92, -33), 3.0), ((-85, -39), 2.4)]          # the ember pools at the wall's foot, by the lodge

PLACES = [("The Lodge", (-89, -20)), ("Pumice Row", (-73, 6)), ("The Breach", (-51, 33)),
          ("Steam Pond", (-23, 27)), ("The Spine", (-34, 51)), ("The Scorch Wood", (-44, -6)),
          ("The Sinkhole", (-36, 6)), ("The Cairn", (-30, -44)), ("The Landing", (-14, -24)),
          ("Caldera Wall", (-98, -30)), ("Ember Pools", (-86, -45))]

ROUTES = [  # polylines a player walks: road (granite, 4 wide) or path (3 wide)
    dict(name="Lodge Road", kind="road", pts=[(-77, -6), (-71, -1), (-67, 5), (-63, 11), (-60, 15)]),
    dict(name="Flats Road", kind="road", pts=[(-77, -9), (-64, -15), (-48, -19), (-32, -23), (-14, -24)]),
    dict(name="Breach Road", kind="road", pts=[(-45, 22), (-38, 17), (-30, 15), (-20, 14), (-12, 14)]),
    dict(name="Cairn Path", kind="path", pts=[(-38, -22), (-36, -30), (-33, -35)]),
    dict(name="Spine Path", kind="path", pts=[(-21, 15), (-17, 24), (-15, 34), (-13, 42)]),
    dict(name="Wood Path", kind="path", pts=[(-52, -18), (-48, -8), (-42, 0), (-38, 2)]),
]
WIDTH = {"road": 4, "path": 3}

# the houses: (key, rect x0 z0 x1 z1, storeys, door side, style)
HOUSES = [
    ("lodge", (-94, -23, -83, -16), 2, "s", "lodge"),
    ("smith", (-83, 3, -77, 9), 1, "e", "row"),
    ("cutter", (-70, -12, -64, -7), 1, "s", "row"),
    ("long", (-80, 13, -72, 18), 1, "e", "row"),
]

KINDS = ["void", "ash", "rock", "water", "road", "path", "bowl", "terrace", "house", "door", "sink", "tube", "stair"]
COLOURS = {"void": (30, 32, 44), "ash": (150, 148, 140), "rock": (104, 100, 98), "water": (62, 108, 205),
           "road": (196, 120, 96), "path": (170, 128, 104), "bowl": (70, 66, 70), "terrace": (205, 160, 140),
           "house": (140, 70, 50), "door": (240, 220, 170), "sink": (96, 84, 80), "tube": (180, 90, 50),
           "stair": (150, 150, 150)}
WALK = {k for k in KINDS if k not in ("void", "house")}


class Land:
    """The red half's grids, [i, k] with x = X_MIN + i (x < 0 only) and z = Z_MIN + k."""


@lru_cache(maxsize=1)
def land():
    L = Land()
    xs, zs = np.arange(X_MIN, 0), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    nb, ns = fbm(sh, 36, 3, seed=11), fbm(sh, 10, 2, seed=12)

    # the outline: the fissure's lip ragged with bays; the island's other edges inset; the far corners cut
    lip = -8 - noise.ragged(sh, "z", 9, 7, seed=21)
    land = shapes.island(X, Z, (X_MIN, Z_MIN, -1, Z_MAX), east=-1 - lip,
                         west=2 + noise.ragged(sh, "z", 14, 5, seed=22),
                         north=3 + noise.ragged(sh, "x", 16, 6, seed=23), south=3 + noise.ragged(sh, "x", 16, 6, seed=24),
                         cuts=[([(-104, 58), (-70, 58), (-58, 72), (-104, 72)], 2 * fbm(sh, 8, 2, seed=25)),   # nobody's corner
                               ([(-104, -72), (-50, -72), (-62, -56), (-80, -48), (-104, -44)],
                                2 * fbm(sh, 8, 2, seed=26))])     # the far north-west: nobody's either

    # the ash shelf: 51 by the fissure, rising gently west to the hamlet's 53-54
    h = F.terms(Xf, Zf, 51, F.Noise(nb, 3.2), F.Noise(ns, 0.6), F.Ramp("x", -58, -86, 2.5))
    h = np.where(np.hypot(Xf - CORE[0], Zf - CORE[1]) < 20, 51 + 0.6 * ns, h)    # the cone sits on even ground

    # the cinder knolls on the north flats: the staging ground's cover, the Cairn on the tallest
    for (kx_, kz_), r, rise in KNOLLS:
        base = float(np.median(h[np.hypot(Xf - kx_, Zf - kz_) < r]))
        h = LF.spire(h, Xf, Zf, (kx_, kz_), r=r, top=base + rise, taper=0.9, jag=0.1, seed=int(r * 7))
        h = np.where(np.hypot(Xf - kx_, Zf - kz_) < 2.5, np.round(base + rise - 1), h)   # a flat crown

    # the Caldera Wall at the back: a ridged crest 70-78 over twelve blocks, cut into 3-block terraces
    foot = noise.line(sh, "z", 20, seed=30, amp=3, base=-93)
    crest = 70 + 6 * ridged(sh, 18, 3, seed=31) + 3 * np.exp(-((Zf + 40) / 20) ** 2)
    h = LF.ridge(h, Xf, foot, 11, crest, terrace=(3, 0.5, 0.2))

    # the lodge terrace: an oval shelf at the wall's foot, levelled at 57 and eased into the shelf
    tz = np.hypot((Xf + 85) / 11.0, (Zf + 7) / 11.0) + 0.1 * fbm(sh, 6, 2, seed=32)
    h = LF.blend(h, np.full(sh, TERRACE_Y + 0.0), tz < 1.0, width=6)
    h = np.where(tz < 0.7, TERRACE_Y, h)

    # the Spine: a basalt ridge rising west along its crest line to a crag over the cone
    d_sp, s_sp = shapes.polyline(Xf, Zf, spline(SPINE, 1.0))
    sl = shapes.length(spline(SPINE, 1.0))
    top = 52 + (SPINE_TOP - 52) * (s_sp / sl) ** 1.3 + 1.5 * fbm(sh, 6, 2, seed=33)
    prof = np.clip(1 - d_sp / 8.0, 0, 1) ** 0.6
    end = np.hypot(Xf - SPINE[-1][0], Zf - SPINE[-1][1])
    prof = np.where(Xf < SPINE[-1][0], prof * smoothstep(5.5, 2.0, end), prof)   # the crag's sheer west end
    h = np.maximum(h, h + (top - h).clip(0) * prof)

    # the cone: a level floor round the core, a crest at 56, a sheer inner face (a drop in, not a climb out),
    # an outer slope a block a block; two breaches, toward the hamlet and toward the pond
    cx, cz = CORE
    dc = np.hypot(Xf - cx, Zf - cz)
    ang = np.degrees(np.arctan2(Zf - cz, Xf - cx))
    outer = RIM_Y - (dc - 11)                                    # a block down for every block out
    cone = np.where(dc < 9, BOWL_Y, np.where(dc < 11, RIM_Y, np.maximum(h, outer)))
    breach = (np.abs(((ang + 135) + 180) % 360 - 180) < 13) | (np.abs(ang) < 13)
    ramp = np.minimum(BOWL_Y + np.maximum(0, dc - 8.5), h)       # out of the bowl a block a block
    cone = np.where(breach, np.where(dc < 9, BOWL_Y, ramp), cone)
    h = np.where(dc < 18, cone, h)
    L.bowl = dc < 9
    L.breach = breach & (dc < 18)

    # Steam Pond: an ellipse of water at 50, its bed three under, banks a block over the water
    (px, pz), rx, rz, wl = POND
    pe = np.hypot((Xf - px) / rx, (Zf - pz) / rz) + 0.08 * fbm(sh, 5, 2, seed=34)
    pond = pe < 1.0
    h = np.where(pe < 1.6, np.minimum(h, wl + 1 + (h - wl - 1) * smoothstep(1.0, 1.6, pe)), h)
    bed = wl - 1 - 2.5 * (1 - np.clip(pe, 0, 1) ** 2)

    # the sinkhole in the wood: one-block rings down to the tube's floor
    (kx, kz), kr, kf = SINK
    dk = np.hypot(Xf - kx, Zf - kz)
    funnel = kf + np.maximum(0, np.floor(dk - 1.0))
    L.sink = (dk <= kr) & (funnel < h)

    Hi = np.round(h).astype(int)
    Hi = np.where(L.sink, funnel.astype(int), Hi)
    water = np.zeros(sh, int)
    water[pond] = wl
    Hi[pond] = np.floor(bed[pond]).astype(int)

    # the routes, graded in order, none re-grading one laid before it
    laid = np.zeros(sh, bool)
    L.routes = []
    for r in ROUTES:
        pts = spline(r["pts"], 1.0)
        wd = WIDTH[r["kind"]]
        Hn, prof_ = LF.grade(Hi.astype(float), Xf, Zf, pts, width=wd, max_grade=0.34, shoulder=2,
                             water=water > 0, keep=laid | L.bowl | (dc < 13))
        Hi = np.where(water > 0, Hi, np.round(Hn).astype(int))
        L.routes.append(dict(r, line=pts, profile=prof_, width=wd))
        laid |= shapes.polyline(Xf, Zf, pts)[0] <= wd / 2

    # the terrace floor, held at 57 under its paving
    x0, z0, x1, z1 = TERRACE
    L.terrace = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    Hi[L.terrace] = TERRACE_Y

    # the underside: sheer under the fissure, tapering elsewhere
    bottom = island_bottom(Hi, land, X >= -30, taper=(5, 0.9), sheer_taper=(30, 1.0), rough=4 * fbm(sh, 9, 3, seed=51),
                           floor=6 + 3 * fbm(sh, 16, 2, seed=52))

    L.X, L.Z, L.land = X, Z, land
    L.H = np.where(land, Hi, -1)
    L.water = np.where(land, water, 0)
    L.bottom = np.where(land, bottom, 0)
    L.pond = pond & land
    L.dc = dc
    L.wood = shapes.inside(Xf, Zf, WOOD) & land & ~L.sink
    L.slope = slope_deg(L.H, land)
    L.lip = lip
    return L


def at(L, x, z):
    return int(L.H[x - X_MIN, z - Z_MIN])


# ---- the buildings --------------------------------------------------------------------------------------
STYLES = {
    # Pumice Row: brick ground storey, dark oak posts, spruce plank upper and gable under a dark oak roof
    "row": dict(ground=[(45, 0)], upper=[(5, 1)], post=1, gable=(5, 1), floor=(5, 1), roof=(5, 5),
                stair=164, slab=(126, 5), door=193, window=(102, 0), chimney=(45, 0)),
    # the lodge: the same family, two storeys, granite plinth courses
    "lodge": dict(ground=[(45, 0), (45, 0), (1, 1)], upper=[(5, 1)], post=1, gable=(5, 1), floor=(5, 1),
                  roof=(5, 5), stair=164, slab=(126, 5), door=193, window=(102, 0), chimney=(45, 0)),
}


def spec(rect, door):
    x0, z0, x1, z1 = rect
    nx, nz = x1 - x0 + 1, z1 - z0 + 1
    if door in "ns":
        return dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=0, L=nx, W=nz, door=1 if door == "s" else -1)
    return dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=90, L=nz, W=nx, door=1 if door == "w" else -1)


def door_cell(s):
    """Where pgmvox.build.house will put a spec's door (the library decides it only while building)."""
    fr = Frame(s["cx"], s["cz"], s["heading"])
    m, X, Z, U, V = fr.mask(s["L"], s["W"])
    wall = shapes.boundary(m, diagonal=True)
    c = [(abs(U[i, k]), int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(wall))
         if s["door"] * V[i, k] > s["W"] / 2 - 1 and abs(U[i, k]) < s["L"] / 2 - 1.5]
    _, x, z = min(c)
    return x, z


@lru_cache(maxsize=1)
def houses():
    L = land()
    out = {}
    for key, rect, storeys, door, style in HOUSES:
        s = spec(rect, door)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        f = TERRACE_Y if key == "lodge" else int(np.median([at(L, x, z) for x, z in cells]))
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=f, storeys=storeys,
                   style=STYLES[style], door=s["door"], chimney=True)
        out[key] = dict(house=hs, cells=cells, door=door_cell(s), floor=f, side=door)
    return out


# ---- the plan raster ----------------------------------------------------------------------------------------
def tube_cells():
    """The tube's floor cells: within 0.6 of its radius of the axis, the floor interpolated along it."""
    out = {}
    pts = TUBE
    for a, b in zip(pts, pts[1:]):
        n = int(max(abs(b[0] - a[0]), abs(b[2] - a[2])) * 2) + 1
        for j in range(n + 1):
            t = j / n
            x, y, z, r = (a[q] + (b[q] - a[q]) * t for q in range(4))
            rr = max(1.0, 0.6 * r)
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    c = (int(math.floor(x + dx)), int(math.floor(z + dz)))
                    d = math.hypot(c[0] + 0.5 - x, c[1] + 0.5 - z)
                    if d <= rr:
                        out[c] = int(round(y)) - 1
    return out


@lru_cache(maxsize=1)
def build():
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    K = np.full(L.H.shape, R.kinds["void"])
    K[L.land] = R.kinds["ash"]
    K[L.land & (L.slope > 40)] = R.kinds["rock"]
    Xf, Zf = L.X.astype(float), L.Z.astype(float)
    for r in L.routes:
        on = (shapes.polyline(Xf, Zf, r["line"])[0] <= r["width"] / 2) & L.land
        K[on] = R.kinds[r["kind"]]
    K[L.bowl] = R.kinds["bowl"]
    K[L.sink] = R.kinds["sink"]
    K[L.terrace] = R.kinds["terrace"]
    K[L.water > 0] = R.kinds["water"]
    H = np.where(L.water > 0, L.water, L.H)
    H = np.where(L.land, H, 0)
    for key, b in houses().items():
        for x, z in b["cells"]:
            K[x - X_MIN, z - Z_MIN] = R.kinds["house"]
            H[x - X_MIN, z - Z_MIN] = b["floor"] + 4 * b["house"].storeys
        dx, dz = b["door"]
        K[dx - X_MIN, dz - Z_MIN] = R.kinds["door"]
        H[dx - X_MIN, dz - Z_MIN] = b["floor"]
    # the core's casing stands over the bowl: its columns are not walked (the vent under it is shut by it)
    cx, cz = CORE
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            K[x - X_MIN, z - Z_MIN] = R.kinds["house"]
            H[x - X_MIN, z - Z_MIN] = CORE_Y + 4
    R.H[:] = SYM.whole(H)
    R.K[:] = SYM.whole(K)
    # storey 1: the lava tube from the fissure face to the sinkhole's floor
    U = R.storey(1)
    for (x, z), y in tube_cells().items():
        if not (R.inside(x, z) and x < 0 and L.land[x - X_MIN, z - Z_MIN]):
            continue
        if L.sink[x - X_MIN, z - Z_MIN]:                          # under the sinkhole's rings the carve opens
            R.cell(x, z, y, "sink")                               # them: the tube's floor is the ground there
            continue
        U.cell(x, z, y, "tube")
    return R


def zone(R):
    """Where a team builds over the void: the fissure, |x| <= RENT, wherever there is no land."""
    return (np.abs(R.X + 0.5) <= RENT + 0.5) & R.mask("void")


def tube_mouth():
    """The tube's first cells in the fissure face: what a bridge reaches to go under."""
    x, y, z, _ = TUBE[0]
    return [(x, z + dz, 1) for dz in (-1, 0, 1)]


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 20), ("blue-team", "Blue", "blue", 20)), SYM)
    x0, z0, x1, z1 = TERRACE
    O.add(Spawn("red-team", SPAWN, yaw=-90, kit="spawn-kit", area=Box(x0, TERRACE_Y + 1, z0, x1, TERRACE_Y + 6, z1)))
    cx, cz = CORE
    O.add(Core("red-core", "West Core", "red-team", Box(cx - 2, CORE_Y, cz - 2, cx + 2, CORE_Y + 4, cz + 2),
               leak=LEAK), name="East Core")
    O.add(Observer((0, 92, 0), yaw=90), mirror=False)
    return O


def core_ring(team="red"):
    """The cells a player stands on to break a core: the bowl floor next to the casing."""
    cx, cz = CORE if team == "red" else SYM.point(*CORE)
    box = [(x, z) for x in range(cx - 2, cx + 3) for z in range(cz - 2, cz + 3)]
    return common.ring(box, 1)
