"""Tamarisk Wash: a destroy-the-monument board in a walled desert basin. A dry wash runs north to south down the
middle, sixteen blocks deep, crossed by two graded ghats a side and a ruined aqueduct whose two halves stop nine
blocks short of each other. Each team holds the plateau on its side of the wash with two monuments: the Obelisk,
forward on Table Rock (a mesa a short walk from the wash), and the Sunstone, back in the Souk beside the spawn.

Red holds the west (x < 0). Blue is red's mirror across the wash, x' = -1 - x, which is pgmvox's Symmetry("mirror_x").
H is the y of the floor block; a player stands at H + 1.

    land()        heights, water and the underside's rim for the whole board, red drawn and mirrored
    build()       the plan Raster: kinds and floors; storey 1 holds the aqueduct, the arch, the roof of the
                  caravanserai, the qanat and the mine
    houses()      every building as a pgmvox.build.House with its footprint and door
    objectives()  teams, spawns and the monuments, drawn once for red
"""
import math
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox import landform as LF  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox import under as under_lib  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.noise import fbm, ridged, smoothstep, spline  # noqa: E402
from pgmvox.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import slope_deg  # noqa: E402

BOARD = "tamarisk-wash"
X_MIN, X_MAX = -100, 99
Z_MIN, Z_MAX = -64, 63
SYM = Symmetry("mirror_x")
PLATEAU = 62
WASH_FLOOR = 46
POND_Y = 61
KILL_Y = 6
MAX_BUILD = 104

SPAWN = (-87, 67, -4)                     # feet in the kasbah's hall, floor 66
SPAWN_AREA = Box(-99, 0, -16, -80, 127, 6)

TABLE = (-58, -28)                        # Table Rock's centre
TABLE_R, TABLE_TOP = 8, 70
ZIGG = (-26, -46)                         # the stepped rock the arch springs from
ZIGG_TOP = 70
ARCH = [(-28, -45), (-40, -38), (-52, -31)]       # the arch's deck line, ziggurat top to Table Rock's top
SQUARE = (-68, 16, -57, 26)               # the Souk's square: x0, z0, x1, z1
STONE_AT = (-63, 21)                      # the Sunstone's column
OBELISK_AT = TABLE
WELL = (-69, 30)                          # the well house's shaft
CISTERN = (-66, 52, 28)                   # the chamber under the square: x, floor y, z
SERAI = (-47, 24, -27, 40)                # the caravanserai's outer ring
SERAI_WALL = 4                            # the ring's thickness
GATES = ((-47, 31, 3), (-27, 31, 3))      # the two gates: x, z centre, width
ARCADE = (-26, -2, -5, 1)                 # the aqueduct's red half: x0, z0, x1, z1
DECK_Y = 63

# the mouth opens in the wash at z 23 and runs under the south ghat at x -20..-15 with three or more blocks of rock over it; at z 30
# it had cut the ghat's lower third in two
QANAT = [(-7, 47, 23, 2.6), (-20, 47, 24, 2.6), (-31, 48, 29, 2.8), (-42, 50, 30, 2.8), (-52, 52, 29, 2.8),
         (-60, 52, 28, 2.6), (-64, 52, 28, 2.6)]
MINE = [(-74, 63, -34), (-70, 63, -34), (-64, 66, -34), (-64, 66, -28), (-63, 66, -28)]
MINE_SHAFT = (-63, -28)                   # the ladder up to Table Rock's top

KINDS = ["void", "sand", "steep", "water", "road", "lane", "grove", "square", "yard", "house", "inside", "door",
         "wash", "mesa", "deck", "stair", "qanat", "mine", "rim"]
COLOURS = {"void": (20, 20, 28), "sand": (222, 190, 140), "steep": (176, 112, 76), "water": (60, 130, 200),
           "road": (200, 164, 110), "lane": (186, 150, 106), "grove": (98, 150, 70), "square": (232, 214, 180),
           "yard": (218, 200, 160), "house": (236, 230, 220), "inside": (210, 170, 130), "door": (80, 150, 170),
           "wash": (196, 150, 112), "mesa": (190, 90, 60), "deck": (210, 205, 190), "stair": (170, 150, 120),
           "qanat": (80, 120, 150), "mine": (130, 100, 70), "rim": (150, 90, 70)}
WALK = {"sand", "steep", "road", "lane", "grove", "square", "yard", "inside", "door", "wash", "mesa", "deck",
        "stair", "qanat", "mine"}

PLACES = [("The Kasbah", (-89, -4)), ("The Souk", (-62, 21)), ("The Sunstone", (-63, 21)),
          ("Table Rock", TABLE), ("The Obelisk", (-58, -28)), ("The Stepped Rock", ZIGG),
          ("The Arch", (-38, -39)), ("The Caravanserai", (-37, 32)), ("The Oasis", (-64, 44)),
          ("The Wash", (-3, 20)), ("The Arches", (-14, 0)), ("North Ghat", (-14, -28)),
          ("South Ghat", (-14, 24)), ("The Well House", (-57, 29)), ("Old Salt Mine", (-52, -36))]

OASIS = ((-64, 44), 8.5)
GROVE = [(-78, 34), (-50, 34), (-48, 56), (-60, 61), (-82, 56)]
SPIRES = [(-76, -44, 5, 69), (-86, 24, 4, 68)]       # small buttes for cover: x, z, radius, top

ROUTES = [
    dict(name="Caravan Road", kind="road", width=5, grade=0.3,
         pts=[(-79, -3), (-74, 4), (-70, 10), (-67, 15)]),
    dict(name="Wash Road", kind="road", width=5, grade=0.3,
         pts=[(-79, -5), (-70, -8), (-58, -8), (-44, -6), (-32, -8), (-24, -8)]),
    dict(name="North Ghat", kind="road", width=4, grade=0.6,
         pts=[(-24, -8), (-19, -16), (-14, -26), (-10, -34)]),
    dict(name="South Ghat", kind="road", width=4, grade=0.6,
         pts=[(-22, 12), (-19, 18), (-15, 28), (-10, 36)]),
    dict(name="Serai Road", kind="road", width=4, grade=0.3, pts=[(-58, 25), (-55, 31), (-50, 32), (-47, 31)]),
    dict(name="Gate Road", kind="road", width=4, grade=0.3, pts=[(-26, 31), (-22, 26), (-22, 12)]),
    dict(name="Table Lane", kind="lane", width=3, grade=0.3, pts=[(-58, -8), (-58, -14), (-58, -18)]),
    dict(name="Arch Lane", kind="lane", width=3, grade=0.4, pts=[(-30, -16), (-26, -30), (-28, -38)]),
    dict(name="Mine Lane", kind="lane", width=3, grade=0.4, pts=[(-58, -8), (-66, -22), (-72, -30), (-76, -34)]),
    dict(name="Arcade Road", kind="road", width=4, grade=0.3, pts=[(-44, -6), (-34, -2), (-27, -1)]),
    dict(name="Oasis Path", kind="lane", width=3, grade=0.3, pts=[(-57, 33), (-57, 38), (-58, 41)]),
    dict(name="Dune Path", kind="lane", width=3, grade=0.3, pts=[(-56, 44), (-46, 50), (-36, 50)]),
]

HOUSES = [
    dict(key="kasbah", rect=(-96, -12, -82, 2), storeys=2, door="e", style="kasbah", floor=66, inside=True),
    dict(key="h1", rect=(-77, 16, -72, 21), storeys=1, door="e", style="adobe"),
    dict(key="h2", rect=(-77, 23, -72, 29), storeys=2, door="e", style="adobe"),
    dict(key="h3", rect=(-53, 17, -48, 22), storeys=1, door="w", style="adobe"),
    dict(key="h4", rect=(-53, 24, -48, 28), storeys=2, door="w", style="adobe"),
    dict(key="h6", rect=(-63, 5, -56, 10), storeys=2, door="s", style="adobe"),
    dict(key="shop", rect=(-51, 8, -47, 12), storeys=1, door="s", style="tiled"),
    dict(key="minaret", rect=(-65, 33, -61, 37), storeys=1, door="n", style="tower", floor=62),
]
STYLES = {
    "kasbah": dict(ground=[(24, 2), (24, 0)], upper=[(159, 0), (24, 2)], post=None, gable=(24, 2), floor=(24, 2),
                   roof=(24, 2), stair=128, slab=(44, 1), door=196, window=(101, 0), chimney=(24, 2)),
    "adobe": dict(ground=[(159, 0), (159, 0), (24, 0)], upper=[(159, 0)], post=None, gable=(159, 0), floor=(24, 2),
                  roof=(24, 2), stair=128, slab=(44, 1), door=196, window=(160, 3), chimney=(24, 0)),
    "tiled": dict(ground=[(159, 0), (24, 0)], upper=[(159, 0)], post=None, gable=(159, 0), floor=(24, 2),
                  roof=(159, 9), stair=128, slab=(44, 1), door=196, window=(160, 3), chimney=(24, 0)),
    "tower": dict(ground=[(24, 0), (24, 2)], upper=[(24, 0)], post=None, gable=(24, 0), floor=(24, 2),
                  roof=(24, 0), stair=128, slab=(44, 1), door=196, window=(101, 0), chimney=(24, 0)),
}


@lru_cache(maxsize=1)
def land():
    """The whole board's heights H (floor block y), the water, the rim; red drawn and the whole mirrored."""
    L = type("Land", (), {})()
    xs, zs = np.arange(X_MIN, X_MAX + 1), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    n1, n2 = SYM.field(fbm(sh, 12, 3, seed=11)), SYM.field(fbm(sh, 36, 3, seed=12))
    dune = SYM.field(fbm(sh, 22, 2, seed=13))
    d = np.abs(Xf + 0.5)                                             # distance from the wash's axis

    # the plateau: dunes, a rise toward the back, a gentler fall to the wash
    base = PLATEAU + 1.5 * n1 + 2.0 * n2 + 1.2 * dune + 4 * smoothstep(-60, -94, Xf) * (Xf < 0)
    h = np.where(Xf < 0, base, SYM.image(base))

    # Table Rock (a mesa, its steps cut later), the Stepped Rock, two small buttes for cover
    h = LF.butte(h, Xf, Zf, TABLE, r=TABLE_R, top=TABLE_TOP, cliff=2.2, talus=7, talus_height=0.3, jag=0.1, seed=3)
    rings = [(10 - k * 0.9, 63 + k) for k in range(8)]
    h = LF.stage(h, Xf, Zf, ZIGG, [(r, y) for r, y in rings] + [(2.3, ZIGG_TOP)], jag=0.04, seed=4)
    for (sx_, sz_, rr, top) in SPIRES:
        h = LF.butte(h, Xf, Zf, (sx_, sz_), r=rr, top=top, cliff=1.5, talus=5, talus_height=0.35, jag=0.1, seed=5)

    # the aqueduct's anchor and the oasis rim
    anchor = (Xf >= ARCADE[0] - 4) & (Xf <= ARCADE[0] + 3) & (Zf >= ARCADE[1] - 3) & (Zf <= ARCADE[3] + 3)
    h = LF.blend(h, np.full(sh, float(PLATEAU)), anchor, width=3)
    h = np.where(Xf < 0, h, SYM.image(h))                                  # red drawn, mirrored again after the buttes

    # the Souk's square and the spawn terrace
    sq = (Xf >= SQUARE[0]) & (Xf <= SQUARE[2]) & (Zf >= SQUARE[1]) & (Zf <= SQUARE[3])
    h = LF.blend(h, np.full(sh, float(PLATEAU)), (Xf >= SQUARE[0] - 14) & (Xf <= SQUARE[2] + 14) &
                 (Zf >= SQUARE[1] - 14) & (Zf <= SQUARE[3] + 24), width=7)
    h = np.where(sq, PLATEAU, h)
    terr = (Xf >= -99) & (Xf <= -78) & (Zf >= -18) & (Zf <= 8)
    h = LF.blend(h, np.full(sh, 66.0), terr, width=6)
    h = np.where(terr & (Xf >= -97) & (Xf <= -80) & (Zf >= -14) & (Zf <= 4), 66, h)
    # the serai's yard is level
    sx0, sz0, sx1, sz1 = SERAI
    serai = (Xf >= sx0 - 1) & (Xf <= sx1 + 1) & (Zf >= sz0 - 1) & (Zf <= sz1 + 1)
    h = LF.blend(h, np.full(sh, float(PLATEAU)), (Xf >= sx0 - 6) & (Xf <= sx1 + 6) & (Zf >= sz0 - 6) & (Zf <= sz1 + 6),
                 width=5)
    h = np.where(serai, PLATEAU, h)

    # the oasis: a pond in a shallow bowl
    (ox, oz), orad = OASIS
    od = np.hypot(Xf - ox, Zf - oz) + 0.8 * fbm(sh, 5, 2, seed=14)
    bowl = POND_Y - 3 + np.clip((od - 5) * 0.8, 0, 6)
    h = np.where(od < 12, np.minimum(h, np.maximum(bowl, POND_Y - 3)), h)
    pond = od < orad - 1.0
    h = np.where(pond, POND_Y - 3 + np.round(1.6 * np.clip((od - 3) / 4, 0, 1)), h)
    L.pond = np.where(Xf < 0, pond, False)

    # the wash: a floor, a wall of cliff, ledges; cut under the plateau, closed again by the rim
    prof = np.interp(d, [0, 9, 10.5, 13, 16, 19, 22, 25], [WASH_FLOOR, WASH_FLOOR, 49, 53, 57, 60.5, 62.5, 63.5])
    prof = prof + 0.9 * n1 * (d < 9) + 1.5 * SYM.field(fbm(sh, 5, 2, seed=15)) * ((d > 9) & (d < 22))
    h = np.where(d < 25, np.minimum(h, prof), h)

    # the rim: the basin's walls rise toward the board's edge
    e = np.maximum(np.abs(Xf + 0.5) / 100.0, np.abs(Zf + 0.5) / 64.0)
    rim = 26 * smoothstep(0.80, 1.0, e) ** 1.3 + 8 * ridged(sh, 18, 3, seed=16) * smoothstep(0.84, 1.0, e)
    rim = SYM.field(rim)
    L.rim = e > 0.86
    h = h + rim

    # the oasis ground cover keeps its own height; the roads are graded in later
    H = np.round(h).astype(int)
    H = np.where(Xf < 0, H, SYM.image(H))
    water = np.zeros(sh, int)
    water[L.pond & (Xf < 0)] = POND_Y
    H = np.where(water > 0, np.minimum(H, POND_Y - 1), H)
    L.water = water

    # roads and lanes graded into the ground, the ghats cutting down the wash's wall
    laid = np.zeros(sh, bool)
    L.routes = []
    for rt in ROUTES:
        pts = spline(rt["pts"], 1.0)
        Hn, prof_ = LF.grade(H.astype(float), Xf, Zf, pts, width=rt["width"], max_grade=rt["grade"], shoulder=3,
                             water=water > 0, keep=laid)
        H = np.where(water > 0, H, np.round(Hn).astype(int))
        L.routes.append(dict(rt, line=pts, profile=prof_))
        laid |= shapes.polyline(Xf, Zf, pts)[0] <= rt["width"] / 2
    # the roads graded to the oasis cut its rim below the pond: hold every dry cell beside it at the pond's level,
    # so no water stands a block over its bank with air beside it
    from scipy import ndimage
    rim = ndimage.binary_dilation(water > 0, np.ones((3, 3), bool)) & (water == 0)
    H = np.where(rim, np.maximum(H, POND_Y), H)
    H = np.where(Xf < 0, H, SYM.image(H))
    L.water = np.where(Xf < 0, water, SYM.image(water))
    L.X, L.Z, L.H = X, Z, H
    L.Xf, L.Zf = Xf, Zf
    L.road_on = {}
    for rt in L.routes:
        on = shapes.polyline(Xf, Zf, rt["line"])[0] <= rt["width"] / 2
        L.road_on[rt["name"]] = np.where(Xf < 0, on, SYM.image(on))
    L.slope = slope_deg(H)
    grove = shapes.inside(Xf, Zf, GROVE) | (np.hypot(Xf - ox, Zf - oz) < 14)
    L.grove = np.where(Xf < 0, grove, SYM.image(grove)) & (L.water == 0)
    L.square = np.where(Xf < 0, sq, SYM.image(sq))
    L.wash = (d < 9.5)
    L.mesa = np.where(Xf < 0, (np.hypot(Xf - TABLE[0], Zf - TABLE[1]) < TABLE_R + 0.5) |
                      (np.hypot(Xf - ZIGG[0], Zf - ZIGG[1]) < 2.8), False)
    L.mesa = np.where(Xf < 0, L.mesa, SYM.image(L.mesa))
    return L


def at(L, x, z):
    return int(L.H[x - X_MIN, z - Z_MIN])


# ---- buildings --------------------------------------------------------------------------------------------
def spec(h):
    x0, z0, x1, z1 = h["rect"]
    nx, nz = x1 - x0 + 1, z1 - z0 + 1
    if h["door"] in "ns":
        heading, Lh, W, sign = 0, nx, nz, (1 if h["door"] == "s" else -1)
    else:
        heading, Lh, W, sign = 90, nz, nx, (1 if h["door"] == "w" else -1)
    return dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=heading, L=Lh, W=W, door=sign)


def door_cell(s):
    fr = Frame(s["cx"], s["cz"], s["heading"])
    m, X, Z, U, V = fr.mask(s["L"], s["W"])
    wall = shapes.boundary(m, diagonal=True)
    cands = [(abs(U[i, k]), int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(wall))
             if s["door"] * V[i, k] > s["W"] / 2 - 1 and abs(U[i, k]) < s["L"] / 2 - 1.5]
    _, x, z = min(cands)
    return x, z


@lru_cache(maxsize=1)
def houses():
    L = land()
    out = {}
    for h in HOUSES:
        s = spec(h)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        f = h["floor"] if "floor" in h else int(np.median([at(L, x, z) for x, z in cells]))
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=f, storeys=h["storeys"],
                   style=STYLES[h["style"]], door=s["door"], chimney=False,
                   roof="flat" if h["style"] in ("kasbah", "adobe", "tower") else "hip")
        out[h["key"]] = dict(spec=h, house=hs, cells=cells, door=door_cell(s), floor=f)
    return out


def _edge(cells):
    cells = set(cells)
    return {(x, z) for x, z in cells if any((x + a, z + b) not in cells for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def serai_cells():
    """The caravanserai: the ring of rooms (walls, four thick), the courtyard, the two gates."""
    x0, z0, x1, z1 = SERAI
    t = SERAI_WALL
    ring, yard, gate = set(), set(), set()
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x < x0 + t or x > x1 - t or z < z0 + t or z > z1 - t:
                ring.add((x, z))
            else:
                yard.add((x, z))
    for gx, gz, gw in GATES:
        for dz in range(-(gw // 2), gw // 2 + 1):
            for dx in range(t):
                cx_ = gx + dx if gx == x0 else gx - dx
                gate.add((cx_, gz + dz))
    ring -= gate
    return ring, yard, gate


# ---- the plan raster --------------------------------------------------------------------------------------
def _tube_cells(pts, shrink=0.6):
    line = spline([(p[0], p[2]) for p in pts], 0.5)
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    best = {}
    for x, z in line:
        s = shapes.nearest_on([(p[0], p[2]) for p in pts], x, z)[1]
        fy = float(np.interp(s, arc, [p[1] for p in pts]))
        rr = float(np.interp(s, arc, [p[3] for p in pts])) * shrink
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                c = (int(math.floor(x + dx)), int(math.floor(z + dz)))
                d = math.hypot(c[0] + 0.5 - x, c[1] + 0.5 - z)
                if d <= max(1.0, rr) and d < best.get(c, (9e9,))[0]:
                    best[c] = (d, int(round(fy)) - 1)
    return {c: y for c, (_, y) in best.items()}


def arch_cells():
    """The arch's deck: three wide along ARCH, at ZIGG_TOP."""
    line = spline(ARCH, 0.5)
    cells = set()
    for x, z in line:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if math.hypot(dx, dz) <= 1.45:
                    cells.add((int(round(x)) + dx, int(round(z)) + dz))
    return cells


@lru_cache(maxsize=1)
def build():
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    k_ = R.kinds
    red = L.X < 0
    K = np.full(L.H.shape, k_["sand"])
    K[L.slope > 45] = k_["steep"]
    K[L.wash & (L.H <= WASH_FLOOR + 3)] = k_["wash"]
    K[L.mesa] = k_["mesa"]
    K[L.grove] = k_["grove"]
    for rt in L.routes:
        K[L.road_on[rt["name"]]] = k_[rt["kind"]]
    K[L.square] = k_["square"]
    K[L.water > 0] = k_["water"]
    K[L.rim & (L.slope > 25)] = k_["rim"]
    H = L.H.copy()
    H = np.where(L.water > 0, L.water, H)
    ring, yard, gate = serai_cells()
    Kr, Hr = K.copy(), H.copy()
    for x, z in ring:
        Kr[x - X_MIN, z - Z_MIN] = k_["house"]
        Hr[x - X_MIN, z - Z_MIN] = PLATEAU
    for x, z in yard | gate:
        Kr[x - X_MIN, z - Z_MIN] = k_["yard"]
        Hr[x - X_MIN, z - Z_MIN] = PLATEAU
    for key, b in houses().items():
        inside = b["spec"].get("inside")
        for x, z in b["cells"]:
            i, k = x - X_MIN, z - Z_MIN
            Kr[i, k] = k_["inside" if inside else "house"]
            Hr[i, k] = b["floor"]
        if inside:
            for x, z in _edge(b["cells"]):
                Kr[x - X_MIN, z - Z_MIN] = k_["house"]
        dx, dz = b["door"]
        Kr[dx - X_MIN, dz - Z_MIN] = k_["door"]
    # the well house's shaft: a way down, a stair-kind cell
    wx, wz = WELL
    for dx in (-2, -1, 0, 1, 2):
        for dz in (-2, -1, 0, 1, 2):
            Kr[wx + dx - X_MIN, wz + dz - Z_MIN] = k_["door"] if (dx, dz) == (2, 0) else \
                k_["house"] if max(abs(dx), abs(dz)) == 2 else k_["stair"]
            Hr[wx + dx - X_MIN, wz + dz - Z_MIN] = PLATEAU
    # the steps up Table Rock's south face: a flight, drawn in the raster and laid by the generator
    for (x, z), y in _tube_cells(QANAT).items():                      # where the tube breaks out of the wall the
        i, k = x - X_MIN, z - Z_MIN                                   # ground is its floor: a trench, not a roof
        if 0 <= i < Hr.shape[0] and 0 <= k < Hr.shape[1] and Hr[i, k] - y <= 5 and x < 0:
            Hr[i, k], Kr[i, k] = y, k_["qanat"]
    for x, y, z in under_lib.gallery_line(MINE):                      # the adit and the gallery's shallow reaches: where
        for dx in (-1, 0, 1):                                         # the ground is within the carve it is lowered
            for dz in (-1, 0, 1):
                i, k = x + dx - X_MIN, z + dz - Z_MIN
                if Hr[i, k] - (y - 1) <= 3:
                    Hr[i, k], Kr[i, k] = y - 1, k_["mine"]
    K = np.where(red, Kr, SYM.image(Kr))
    H = np.where(red, Hr, SYM.image(Hr))
    R.H[:] = H
    R.K[:] = K
    # a flight up the mesa's south face, one block a cell
    base = TABLE[1] + TABLE_R + 4
    g = at(L, TABLE[0], base)
    n = TABLE_TOP - g
    R.flight((TABLE[0], base), "n", width=(-1, 1), h0=g + 1, n=n, kind="stair")
    # the caravanserai's stair to its roof, in the courtyard along its north wall
    zr = SERAI[1] + SERAI_WALL
    R.flight((SERAI[0] + SERAI_WALL + 1, zr), "e", h0=PLATEAU + 1, n=4, kind="stair", width=(0, 1))
    U = R.storey(1)
    # the aqueduct, red's half: a deck at DECK_Y on its arcade, 4 wide
    ax0, az0, ax1, az1 = ARCADE
    for x in range(ax0, ax1 + 1):
        for z in range(az0, az1 + 1):
            U.cell(x, z, DECK_Y, "deck")
    for x, z in arch_cells():
        U.cell(x, z, ZIGG_TOP, "deck", both=True)
    for x, z in ring:                                                # the serai's roof
        U.cell(x, z, PLATEAU + SERAI_WALL, "deck")
    for (x, z), y in _tube_cells(QANAT).items():
        U.cell(x, z, y, "qanat")
    cx_, cy_, cz_ = CISTERN
    for x in range(cx_ - 4, cx_ + 5):
        for z in range(cz_ - 4, cz_ + 5):
            if math.hypot(x - cx_, z - cz_) <= 4.2:
                U.cell(x, z, cy_ - 1, "qanat")
    from pgmvox.under import gallery_line
    for x, y, z in gallery_line(MINE):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                U.cell(x + dx, z + dz, y - 1, "mine")
    return R


def links():
    """The ladders and mouths the raster cannot see: the wash's mouth into the qanat, the well's shaft down to the
    cistern, the mine's door and its ladder up. Both ways, and mirrored for blue."""
    out = []
    mx, _, mz, _ = QANAT[0]
    wx, wz = WELL
    sx, sz = MINE_SHAFT
    top = (sx, sz)
    ent = (MINE[0][0], MINE[0][2])
    pairs = [((mx, mz), (mx, mz, 1), 1, "qanat mouth"), ((wx, wz), (wx, wz, 1), 11, "well ladder"),
             (ent, (ent[0], ent[1], 1), 1, "mine door"), (top, (MINE[-1][0], MINE[-1][2], 1), 3, "mine ladder")]
    for a, b, c, tag in pairs:
        for p, q in ((a, b), (tuple(int(v) for v in SYM.point(*a[:2])) + tuple(a[2:]),
                              tuple(int(v) for v in SYM.point(*b[:2])) + tuple(b[2:]))):
            out += [(p, q, c, tag), (q, p, c, tag)]
    return out


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN, yaw=270, kit="spawn-kit", area=SPAWN_AREA))
    ox, oz = OBELISK_AT
    O.add(Destroyable("red-obelisk", "Red Obelisk", "red-team", Box(ox, TABLE_TOP + 4, oz, ox, TABLE_TOP + 6, oz)),
          name="Blue Obelisk")
    sx, sz = STONE_AT
    O.add(Destroyable("red-sunstone", "Red Sunstone", "red-team", Box(sx, PLATEAU + 4, sz, sx, PLATEAU + 5, sz),
                      material=(22, 0), materials="lapis block"), name="Blue Sunstone")
    O.add(Observer((0, 100, 0), yaw=90), mirror=False)
    return O
