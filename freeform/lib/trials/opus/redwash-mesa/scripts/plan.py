"""Redwash Mesa: the plan. Destroy the monument, two a team.

Identity: two badlands mesas face each other across a bottomless seam; each is a high table cut by a dry canyon,
with the team's cliff house on a ledge at the canyon's head, one monument out on the table by a rock pool and one
in the plaza of the adobe town on the canyon floor, so every crossing is made at one of three heights.

Red holds the west (x < 0); blue's half is red's mirror image, x' = -1 - x, pgmvox's Symmetry("mirror_x").
Heights follow the library: H is the y of the floor block, a player stands at H + 1.

    the Table   62, the north and the west: monument A, the rock pool, the junipers
    the Shelf   52, a ledge along the canyon's north wall; the cliff house stands on it at the canyon's head
    the Wash    40-43, the canyon floor: Arroyo Town and monument B
    the Bench   52, the south: the Chimney butte, a stair down into the town
"""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")))   # freeform/lib
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))               # trials/opus (common)

import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402

import common  # noqa: E402
from pgmvox import landform as LF  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox import under as UL  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.noise import fbm, smoothstep, spline  # noqa: E402
from pgmvox.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import slope_deg  # noqa: E402

BOARD = "redwash-mesa"
X_MIN, X_MAX = -96, 95
Z_MIN, Z_MAX = -64, 63
SYM = Symmetry("mirror_x")
SEAM = 22                       # the build zone: |x| <= 22 over the void
MAX_BUILD = 82
TABLE, SHELF, BENCH = 62, 52, 52
WASH = [(-92, 20), (-76, 21), (-60, 25), (-44, 28), (-28, 28), (-12, 27), (-2, 27)]   # the canyon's line
WASH_FLOOR = (43, 40)           # its floor block at the head and at the seam
WASH_HALF = (6.0, 10.0)         # its floor's half width at the head and at the seam

SPAWN = (-81, 53, 11)           # feet on the cliff house's ledge, floor 52
LEDGE = ((-80, 10), 10.0, 5.5)  # the cliff house's ledge: centre, rx, rz, at the Shelf's 52
MONUMENTS = {"table": ((-56, -24), "Table Monument"), "wash": ((-47, 28), "Wash Monument")}
POOL = ((-30, -27), 6.5, 5.0, 58)          # the rock pool on the Table: centre, rx, rz, water surface
CHIMNEY = ((-34, 52), 6.0, 70)             # the butte on the Bench: centre, radius, top
HOODOOS = [((-80, -40), 3.0, 71), ((-68, -50), 3.5, 72), ((-44, -54), 2.5, 69), ((-74, -26), 2.5, 68),
           ((-72, 54), 3.0, 61), ((-54, 58), 2.5, 59), ((-18, 54), 2.5, 59)]   # needles of rock: cover, relief
JUNIPERS = [(-74, -56), (-36, -56), (-34, -40), (-60, -36), (-76, -42)]   # olive on the Table's north
LADDER = ((-69, 7), "n", 10)    # the stair cut up the cliff from the ledge to the Table: foot cell, rises, steps
HEAD = ((-76, 15), "n", 9)      # the stair from the ledge down to the canyon floor: top-foot cell, rises, steps
BENCH_STAIR = ((-38, 32), "s", 11)   # the stair from the town up onto the Bench
MINE = [(-38, 42, 22), (-38, 42, 16), (-38, 46, 10), (-38, 51, 4), (-43, 51, -2)]   # floor (lowest air) along it: straight
                                # up the rises (a stair climbs one way), the jog to the shaft on the level at the top
SHAFT = (-43, -4)               # the shaft from the gallery's end up onto the Table

PLACES = [("Cliff House", (-80, 2)), ("The Table", (-66, -14)), ("Table Monument", (-56, -30)),
          ("The Rock Pool", (-30, -27)), ("Juniper Stand", (-58, -48)), ("Arroyo Town", (-54, 36)),
          ("The Wash", (-24, 30)), ("The Shelf", (-48, 16)), ("The Bench", (-62, 52)), ("The Chimney", (-34, 52)),
          ("Silver Drift", (-36, 8)), ("The Gate", (-8, 30))]

ROUTES = [  # trails a player walks, laid in the ground's own warm set
    dict(name="Table Path", kind="trail", pts=[(-70, -4), (-64, -12), (-56, -20), (-46, -22), (-32, -16), (-16, -14)]),
    dict(name="Junipers Path", kind="trail", pts=[(-64, -12), (-62, -28), (-56, -40), (-44, -46)]),
    dict(name="Wash Trail", kind="trail", pts=[(-76, 25), (-66, 26), (-56, 28), (-44, 29), (-28, 29), (-12, 28)]),
    dict(name="Bench Path", kind="trail", pts=[(-46, 44), (-40, 46), (-26, 46), (-14, 46)]),
]
WIDTH = {"trail": 3}

# the houses: (key, rect x0 z0 x1 z1, storeys, door side); the cliff house is two, on the ledge
HOUSES = [
    ("cliff", (-88, 4, -79, 9), 2, "s"),
    ("cliff2", (-77, 3, -72, 7), 1, "s"),
    ("adobe1", (-67, 19, -61, 23), 1, "s"),
    ("adobe2", (-48, 19, -43, 23), 2, "s"),
    ("adobe3", (-64, 29, -59, 33), 1, "e"),
    ("adobe4", (-50, 33, -45, 37), 2, "n"),
    # the mesa tops: a homestead on the Table's west edge, two on its east side, two on the Bench; each stands on flat
    # ground (a block either way), five or more blocks off every trail and thirty off a monument
    ("mesa1", (-88, -16, -84, -12), 1, "e"),
    ("mesa2", (-24, -44, -20, -40), 2, "s"),
    ("mesa3", (-22, 2, -18, 6), 1, "w"),
    ("bench1", (-82, 44, -78, 48), 1, "e"),
    ("bench2", (-66, 44, -62, 48), 1, "s"),
]

KINDS = ["void", "table", "shelf", "wash", "rock", "water", "trail", "plaza", "house", "door", "stair", "mine"]
COLOURS = {"void": (30, 32, 44), "table": (196, 120, 70), "shelf": (186, 110, 70), "wash": (214, 150, 100),
           "rock": (150, 84, 60), "water": (62, 108, 205), "trail": (230, 190, 140), "plaza": (236, 220, 170),
           "house": (230, 214, 160), "door": (120, 70, 40), "stair": (200, 180, 140), "mine": (110, 80, 50)}
WALK = {k for k in KINDS if k not in ("void", "house")}


class Land:
    """The red half's grids, [i, k] with x = X_MIN + i (x < 0) and z = Z_MIN + k."""


def _ragged(n, cell, amp, seed):
    return np.round(amp * (0.5 + 0.5 * fbm((n,), cell, 2, seed=seed))).astype(int)


@lru_cache(maxsize=1)
def land():
    L = Land()
    xs, zs = np.arange(X_MIN, 0), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    n1, n2 = fbm(sh, 24, 3, seed=71), fbm(sh, 8, 2, seed=72)

    # the outline: the seam's lip ragged, held straight where the canyon meets it (the Gate); the edges inset
    lip = -9 - _ragged(sh[1], 10, 6, 81)
    zz = np.arange(Z_MIN, Z_MAX + 1)
    lip = np.where(np.abs(zz - 27) < 10, -10, lip)
    land = X <= lip[None, :]
    land &= X >= X_MIN + 2 + _ragged(sh[1], 14, 5, 82)[None, :]
    land &= Z >= Z_MIN + 2 + _ragged(sh[0], 14, 5, 83)[:, None]
    land &= Z <= Z_MAX - 2 - _ragged(sh[0], 14, 5, 84)[:, None]
    for corner in ([(-96, -64), (-70, -64), (-84, -46), (-96, -40)], [(-96, 63), (-76, 63), (-88, 48), (-96, 44)]):
        land &= shapes.signed_distance(Xf, Zf, corner) > 2 * fbm(sh, 8, 2, seed=len(corner) + 88)   # far corners

    # the Table and the Bench: 62 north, 52 south of a banded cliff that runs east-west under the Chimney
    bench_line = 41 + 3 * fbm((sh[0],), 16, 2, seed=85)[:, None]
    t = smoothstep(bench_line - 1.5, bench_line + 1.5, Zf)
    ground = TABLE + 0.6 * n1 + (BENCH - TABLE) * t
    ground = np.where(t > 0.5, BENCH + 0.5 * n1 + 0.4 * n2, ground)

    # the Wash: a level floor stepping down east, a lower cliff to the Shelf at 52, the Shelf, an upper cliff
    line = spline(WASH, 1.0)
    d, s = shapes.polyline(Xf, Zf, line)
    frac = s / shapes.length(line)
    floor = np.round(WASH_FLOOR[0] + (WASH_FLOOR[1] - WASH_FLOOR[0]) * np.clip(frac * 1.6, 0, 1))
    hw = WASH_HALF[0] + (WASH_HALF[1] - WASH_HALF[0]) * np.clip(frac * 2, 0, 1) + 0.8 * n2
    lower = floor + (np.minimum(ground, SHELF) - floor) * smoothstep(hw, hw + 2.5, d)
    upper = SHELF + (ground - SHELF) * smoothstep(hw + 6.5, hw + 8.5, d)
    h = np.where(d < hw + 6.5, lower, np.where(ground > SHELF + 0.5, upper, lower))
    h = np.where(d > hw + 9, ground, h)
    L.wash = (d < hw) & land
    L.shelf = (d >= hw + 2.5) & (d < hw + 6.5) & (ground > SHELF + 0.5) & land
    L.floor = floor

    # the cliff house's ledge at the canyon's head, at the Shelf's height, eased into the cliff behind
    (lx, lz), rx, rz = LEDGE
    le = np.hypot((Xf - lx) / rx, (Zf - lz) / rz)
    h = np.where(le < 1.0, SHELF, h)
    L.ledge = (le < 1.0) & land

    # the rock pool on the Table: a basin four under, its water at 58
    (px, pz), prx, prz, pwl = POOL
    pe = np.hypot((Xf - px) / prx, (Zf - pz) / prz) + 0.06 * n2
    pool = pe < 1.0
    h = np.where(pe < 1.5, np.minimum(h, pwl + 1 + (h - pwl - 1) * smoothstep(1.0, 1.5, pe)), h)
    bed = pwl - 1 - 2 * (1 - np.clip(pe, 0, 1) ** 2)

    # the Chimney: a butte on the Bench, its top at 70
    (cx, cz), cr, ctop = CHIMNEY
    h = LF.butte(h, Xf, Zf, (cx, cz), cr, ctop, cliff=1.5, talus=4, talus_height=0.25, jag=0.12, seed=3)
    for j, ((hx, hz), hr, htop) in enumerate(HOODOOS):
        h = LF.spire(h, Xf, Zf, (hx, hz), r=hr + 2, top=htop, taper=2.4, jag=0.15, seed=40 + j)

    Hi = np.round(h).astype(int)
    water = np.zeros(sh, int)
    water[pool] = pwl
    Hi[pool] = np.floor(bed[pool]).astype(int)

    # the monuments' ground: level, a block either way of the floor round them
    for key, ((mx, mz), _) in MONUMENTS.items():
        dm = np.hypot(Xf - mx, Zf - mz)
        lvl = int(round(np.median(Hi[dm < 3])))
        Hi = np.where(dm < 6, lvl, Hi)
    L.plaza = (np.hypot(Xf - MONUMENTS["wash"][0][0], Zf - MONUMENTS["wash"][0][1]) < 6) & land

    # the trails, graded in order
    laid = np.zeros(sh, bool)
    L.routes = []
    for r in ROUTES:
        pts = spline(r["pts"], 1.0)
        wd = WIDTH[r["kind"]]
        Hn, prof = LF.grade(Hi.astype(float), Xf, Zf, pts, width=wd, max_grade=0.34, shoulder=1,
                            water=water > 0, keep=laid | L.plaza)
        Hi = np.where(water > 0, Hi, np.round(Hn).astype(int))
        L.routes.append(dict(r, line=pts, profile=prof, width=wd))
        laid |= shapes.polyline(Xf, Zf, pts)[0] <= wd / 2

    # the underside: sheer under the seam, tapering elsewhere
    void = ~land
    d_out = ndimage.distance_transform_edt(~(void & (X < -30)))
    d_seam = ndimage.distance_transform_edt(~(void & (X >= -30)))
    nn = fbm(sh, 9, 3, seed=86)
    thick = np.minimum(6 + 0.9 * d_out + 4 * nn, 34 + 1.0 * d_seam + 4 * nn)
    bottom = np.maximum(Hi - thick, 8 + 3 * fbm(sh, 16, 2, seed=87)).round().astype(int)

    L.X, L.Z, L.land = X, Z, land
    L.H = np.where(land, Hi, -1)
    L.water = np.where(land, water, 0)
    L.bottom = np.where(land, bottom, 0)
    L.pool = pool & land
    L.junipers = shapes.inside(Xf, Zf, JUNIPERS) & land
    L.slope = slope_deg(L.H, land)
    L.bench = (t > 0.5) & land & ~L.wash
    L.d_wash = d
    return L


def at(L, x, z):
    return int(L.H[x - X_MIN, z - Z_MIN])


# ---- the buildings: adobe, smooth sandstone walls, flat roofs ---------------------------------------------------
STYLE = dict(ground=[(24, 2), (24, 2), (24, 0)], upper=[(24, 2)], post=None, gable=(24, 2), floor=(5, 4),
             roof=(24, 2), stair=128, slab=(44, 1), door=196, window=(160, 9), chimney=(24, 2))


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
    for key, rect, storeys, door in HOUSES:
        s = spec(rect, door)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        f = SHELF if key.startswith("cliff") else int(np.median([at(L, x, z) for x, z in cells]))
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=f, storeys=storeys, style=STYLE,
                   door=s["door"], chimney=False, roof="flat", overhang=0)
        out[key] = dict(house=hs, cells=cells, door=door_cell(s), floor=f)
    return out


def mine_line():
    return UL.gallery_line(MINE)


@lru_cache(maxsize=1)
def build():
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    K = np.full(L.H.shape, R.kinds["void"])
    K[L.land] = R.kinds["table"]
    K[L.bench] = R.kinds["shelf"]
    K[L.shelf | L.ledge] = R.kinds["shelf"]
    K[L.wash] = R.kinds["wash"]
    K[L.land & (L.slope > 45)] = R.kinds["rock"]
    Xf, Zf = L.X.astype(float), L.Z.astype(float)
    for r in L.routes:
        on = (shapes.polyline(Xf, Zf, r["line"])[0] <= r["width"] / 2) & L.land
        K[on] = R.kinds["trail"]
    K[L.plaza] = R.kinds["plaza"]
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
    R.H[:] = common.full(H, "mirror_x")
    R.K[:] = common.full(K, "mirror_x")
    # the stairs cut into the cliffs, drawn for both halves
    for (fx, fz), rises, n in (LADDER, HEAD, BENCH_STAIR):
        if (fx, fz) == HEAD[0]:                                  # the head stair climbs north from the floor
            h0 = SHELF - n + 1
            R.flight((fx, fz + n - 1), rises, width=(-1, 1), h0=h0, n=n)
        elif rises == "s":
            R.flight((fx, fz), rises, width=(-1, 1), h0=at(L, fx, fz - 1) + 1, n=n)
        else:
            R.flight((fx, fz), rises, width=(-1, 1), h0=SHELF + 1, n=n)
    # storey 1: the Silver Drift's gallery
    U = R.storey(1)
    for x, y, z in mine_line():
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                U.cell(x + dx, z + dz, y - 1, "mine")
    return R


def links():
    """The shaft's ladder from the gallery's end up onto the Table, both ways, both halves."""
    x, y, z = mine_line()[-1]
    cost = TABLE - (y - 1)
    out = []
    for a in ((x, z), SYM.point(x, z)):
        out += [((a[0], a[1], 1), a, cost, "ladder"), (a, (a[0], a[1], 1), cost, "ladder")]
    return out


def zone(R):
    return (np.abs(R.X + 0.5) <= SEAM + 0.5) & R.mask("void")


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 20), ("blue-team", "Blue", "blue", 20)), SYM)
    (lx, lz), rx, rz = LEDGE
    O.add(Spawn("red-team", SPAWN, yaw=-90, kit="spawn-kit",
                area=Box(int(lx - rx + 2), SHELF + 1, int(lz - rz + 1), int(lx + rx - 2), SHELF + 6, int(lz + rz - 1))))
    L = land()
    for key, ((x, z), name) in MONUMENTS.items():
        g = at(L, x, z)
        O.add(Destroyable(f"red-{key}", name, "red-team", Box(x, g + 4, z, x, g + 5, z)))
    O.add(Observer((0, 90, 0), yaw=90), mirror=False)
    return O


def monument_ring(key, team="red"):
    (x, z), _ = MONUMENTS[key]
    if team == "blue":
        x, z = SYM.point(x, z)
    return [(x + dx, z + dz) for dx in range(-2, 3) for dz in range(-2, 3) if (dx, dz) != (0, 0)]
