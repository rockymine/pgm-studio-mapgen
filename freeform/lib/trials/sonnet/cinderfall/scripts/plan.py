"""Cinderfall: a destroy-the-core board on a floating volcanic island. A caldera sits dead centre with a lava
lake in its floor; the two teams' ground runs to its two mouths. Each team defends one core, standing forward of
its spawn and a little north of the line to the enemy, and each core has five ways onto it that are not the same
way twice: across the open ash from the caldera (around), down off the Slag Ridge (above), up out of a blowhole
by a lava tube (below), through the Foundry Row (through) and out of the Charred Wood (unseen).

Red holds the west (x < 0). Blue is red's half turn, (x, z) -> (-1 - x, -1 - z), which is pgmvox's Symmetry("half").
All heights follow the library: H is the y of the floor block, a player stands at H + 1.

    land()        heights, lava, outline and underside over the whole board, red drawn and turned
    build()       the plan Raster: kinds and floors, storey 1 the vent tunnel
    houses()      every building as a pgmvox.build.House with its footprint and door
    objectives()  teams, spawns and cores, drawn once for red
"""
import math
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402

from pgmvox import landform as LF  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.noise import fbm, smoothstep, spline  # noqa: E402
from pgmvox.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import slope_deg  # noqa: E402

BOARD = "cinderfall"
X_MIN, X_MAX = -90, 89
Z_MIN, Z_MAX = -60, 59
SYM = Symmetry("half")
PLAIN = 58                               # the ash plain
LAVA_Y = 47                              # the ravine's lava surface (the top lava block)
COAST_Y = 47                             # the ravine's shore: its floor block, level with the lava's top block
BRIDGE_Y = 58                            # the Slag Bridge's floor block, level with the plain
RAV_DRIFT = 3.0                          # the ravine's centre line drifts this far east to the south and west to the north
RAV_WALL = 3.5                           # blocks across the face, from the shore to the rim
RAV_NECK = 9.0                           # half width at the neck, as wide as the old lake (17)
RAV_BULGE = (12.5, 26.0, 9.0)            # extra half width where it swells: how much, at what |z|, how spread
KEYSTONE = (-1, -1)                      # the stack in mid-channel the bridge's two spans meet on (its own image)
PIT_R = 3.4                              # the lava pit under the core
PIT_BED, PIT_LAVA_Y = 38, 55             # its floor block and its lava's top block, three under the plinth's 58
KILL_Y = 10
MAX_BUILD = 100

SPAWN = (-74, 64, 12)                    # feet in the Ember Hold's hall, floor 63
SPAWN_AREA = Box(-82, 0, 3, -63, 127, 29)
CORE_AT = (-48, -10)                     # the plinth's centre; the core floats FLOAT over it
PLINTH_Y = 58
FLOAT = 7
CORE_BOX = Box(CORE_AT[0] - 2, PLINTH_Y + FLOAT, CORE_AT[1] - 2, CORE_AT[0] + 2, PLINTH_Y + FLOAT + 4, CORE_AT[1] + 2)
PLINTH_R = 7.5

BLOWHOLE = ((-60, -10), 54, 7.0)          # centre, the floor block at the bottom, radius
PIT = ((-22, 17), 54, 7.0)               # the Cinder Pit, the tube's other mouth
VENT = [(-22, 55, 17, 2.6), (-27, 51, 15, 2.8), (-34, 49, 12, 3.0), (-42, 49, 7, 3.0), (-50, 50, 2, 3.0),
        (-55, 52, -4, 2.8), (-60, 55, -10, 2.6)]          # (x, floor y = lowest air, z, radius)

RIDGE_TOP = 74
BEACON_Y = 71                           # the beacon tower's floor, on the crest
RIDGE_LINE = [(-80, -33), (-64, -31), (-46, -31), (-28, -34)]
BEACON = (-50, -44, -46, -40)            # the beacon tower on the ridge: x0, z0, x1, z1

KINDS = ["void", "ground", "steep", "lava", "road", "track", "wood", "plinth", "yard", "house", "inside", "door",
         "ridge", "pit", "stair", "tunnel", "bridge", "stack"]
COLOURS = {"void": (24, 22, 28), "ground": (118, 116, 118), "steep": (86, 82, 84), "lava": (236, 100, 30),
           "road": (150, 140, 128), "track": (130, 112, 96), "wood": (60, 70, 60), "plinth": (70, 62, 66),
           "yard": (170, 150, 120), "house": (130, 60, 44), "inside": (214, 170, 120), "door": (240, 210, 150),
           "ridge": (100, 98, 108), "pit": (60, 52, 56), "stair": (170, 170, 170), "tunnel": (116, 80, 110), "bridge": (190, 170, 150), "stack": (150, 110, 90)}
WALK = {"ground", "steep", "road", "track", "wood", "plinth", "yard", "inside", "door", "ridge", "pit", "stair",
        "tunnel", "bridge", "stack"}

PLACES = [("The Ember Hold", (-74, 12)), ("Slag Road", (-62, 6)), ("The Core Plinth", (-52, -16)),
          ("Slag Ridge", (-62, -38)), ("The Beacon", (-52, -44)), ("Charred Wood", (-33, -16)),
          ("Foundry Row", (-50, 15)), ("The Blowhole", (-60, -3)), ("The Cinder Pit", (-22, 24)),
          ("The Slag Bridge", (-8, -1)), ("The Ravine", (-4, -24))]

NORTH_WOOD = [(-42, -29), (-22, -31), (-13, -17), (-24, -3), (-37, -9)]
FOUNDRY = [(-62, 6), (-28, 6), (-28, 32), (-62, 32)]
# The hop chain is drawn once, across the north bulge, west shore to east shore: A B C on red's side and D E F on blue's,
# every gap between the caps about three blocks. The south bulge's chain is its image run the other way. Red's half holds
# A B C and the images of D E F; the half turn gives the rest. (x, z, radius, top, where): lava-standing or shore-standing.
CHAIN = [(-16, -29, 3.0, 61, "shore"), (-10, -31, 2.6, 62, "lava"), (-5, -27, 2.2, 63, "lava"), (1, -27, 2.2, 63, "lava"),
         (7, -29, 2.6, 63, "lava"), (13, -31, 2.8, 62, "shore")]
NEEDLES = [(-10, -19, 2.4, 70, "lava"), (-6, -40, 2.4, 72, "lava"), (-10, -36, 2.6, 64, "shore"), (-9, 37, 2.4, 68, "lava"),
           (-5, 14, 2.0, 66, "lava")]
STACKS = sorted([s for s in CHAIN if s[0] < 0] + [(-1 - x, -1 - z, r, t, wh) for x, z, r, t, wh in CHAIN if x >= 0]
                + NEEDLES)
KEY_R = 3.4                                # the keystone: a stack in mid-channel, its top level with the bridge
BRIDGE_X, BRIDGE_Z = (-12, 11), (-2, 1)    # the Slag Bridge's deck, rim pad to rim pad, four wide
ROUTES = [
    dict(name="Slag Road", kind="road", width=5, grade=0.3,
         pts=[(-64, 10), (-60, 3), (-50, -1), (-40, -4), (-30, -4), (-22, -2), (-14, -1)]),
    dict(name="Spawn Lane", kind="road", width=4, grade=0.3, pts=[(-64, 14), (-62, 20), (-50, 21), (-40, 19)]),
    dict(name="Row Lane", kind="track", width=3, grade=0.3, pts=[(-46, -1), (-46, 8), (-46, 19)]),
    dict(name="Core Path", kind="track", width=3, grade=0.3, pts=[(-48, -1), (-48, -4)]),
    dict(name="Wood Track", kind="track", width=3, grade=0.3, pts=[(-40, -6), (-32, -14), (-27, -20)]),
    dict(name="Pit Track", kind="track", width=3, grade=0.3, pts=[(-40, 19), (-34, 19), (-30, 19)]),
    dict(name="Ridge Stair", kind="road", width=4, grade=0.6, pts=[(-64, 4), (-64, -8), (-62, -22), (-59, -34),
                                                                  (-55, -39)]),
    dict(name="Ridge Back", kind="road", width=4, grade=0.6, pts=[(-30, -3), (-29, -14), (-31, -26), (-34, -37),
                                                                 (-40, -40)]),
    dict(name="Ridge Walk", kind="track", width=3, grade=0.6, pts=[(-55, -39), (-48, -37), (-40, -39)]),
    dict(name="North Shore Stair", kind="road", width=3, grade=0.6, pts=[(-30, -45), (-22, -46), (-13, -45), (-5, -44)]),
    dict(name="South Shore Stair", kind="road", width=3, grade=0.6, pts=[(-38, 36), (-30, 34), (-22, 33), (-12, 31)]),
]

# ---- buildings: footprint with walls, storeys, which side the door is on ----------------------------------
HOUSES = [
    dict(key="hold", rect=(-81, 6, -68, 18), storeys=2, door="e", style="hold", floor=63, inside=True),
    dict(key="smelter", rect=(-60, 9, -48, 17), storeys=2, door="e", style="foundry"),
    dict(key="shed1", rect=(-44, 10, -37, 16), storeys=1, door="w", style="foundry"),
    dict(key="shed2", rect=(-56, 25, -48, 30), storeys=1, door="n", style="foundry"),
    dict(key="cottage1", rect=(-43, 24, -37, 30), storeys=1, door="n", style="cottage"),
    dict(key="cottage2", rect=(-35, 10, -30, 16), storeys=1, door="w", style="cottage"),
    dict(key="cottage3", rect=(-34, 24, -29, 29), storeys=1, door="n", style="cottage"),
    dict(key="beacon", rect=BEACON, storeys=1, door="s", style="tower", floor=BEACON_Y),
]
STYLES = {
    # the hold: nether brick, a flat roof behind a parapet
    "hold": dict(ground=[(112, 0)], upper=[(112, 0), (45, 0)], post=None, gable=(112, 0), floor=(5, 5),
                 roof=(112, 0), stair=114, slab=(44, 6), door=197, window=(101, 0), chimney=(112, 0)),
    # the foundry: stone brick with iron-barred slits under a flat coal roof
    "foundry": dict(ground=[(98, 0), (98, 2), (1, 5)], upper=[(112, 0)], post=None, gable=(98, 0), floor=(1, 6),
                    roof=(173, 0), stair=109, slab=(44, 5), door=197, window=(101, 0), chimney=(98, 0)),
    "cottage": dict(ground=[(4, 0), (1, 5)], upper=[(5, 5)], post=1, gable=(5, 5), floor=(5, 5), roof=(5, 5),
                    stair=164, slab=(126, 5), door=197, window=(102, 0), chimney=(4, 0)),
    "tower": dict(ground=[(98, 0), (98, 2)], upper=[(98, 0)], post=None, gable=(98, 0), floor=(1, 6),
                  roof=(98, 0), stair=109, slab=(44, 5), door=197, window=(101, 0), chimney=(98, 0)),
}


def sym(a):
    """A field made symmetric under the half turn, so a red-only feature never leaves a seam at the middle."""
    return 0.5 * (a + a[::-1, ::-1])


def rot(a):
    return a[::-1, ::-1]


def ravine_axes(Xf, Zf):
    """The ravine's frame: (signed distance across its centre line, half width at the rim, z). The centre line is an odd
    function of z and the half width an even one, so the whole is its own image under the half turn."""
    u, v = Xf + 0.5, Zf + 0.5
    a = RAV_DRIFT * np.sin(np.pi * v / 38.0)
    hw = RAV_NECK + RAV_BULGE[0] * np.exp(-((np.abs(v) - RAV_BULGE[1]) / RAV_BULGE[2]) ** 2)
    return u - a, hw, v


def coast_width(v):
    """How wide the shore is on the west side at z = v; the east side's is this at -v, so the half turn holds."""
    return np.maximum(0.0, 3.2 + 3.6 * np.sin(v / 4.7 + 0.9))


@lru_cache(maxsize=1)
def land():
    """The whole board's heights H (floor block y), the lava, the outline, the underside, the routes graded in."""
    L = type("Land", (), {})()
    xs, zs = np.arange(X_MIN, X_MAX + 1), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    n1, n2 = sym(fbm(sh, 14, 3, seed=11)), sym(fbm(sh, 40, 3, seed=12))
    r = np.hypot(Xf + 0.5, Zf + 0.5)
    th = np.arctan2(Zf + 0.5, Xf + 0.5)
    mouth = np.exp(-(np.sin(th) / 0.42) ** 2)                      # the caldera is open to the east and the west

    # the outline: an ellipse with a ragged edge; the island floats
    e = np.hypot(Xf / 91.0, Zf / 53.0) + 0.07 * sym(fbm(sh, 12, 3, seed=21))
    land_m = e < 1.0

    # the plain, and the caldera profile by radius: floor, shore, inner wall, rim, outer skirt
    prof = np.interp(r, [0, 17, 22, 27, 31, 36, 42], [58, 58, 58, 67, 62, 58.5, 58])     # no basin: the ravine is the low ground
    base = PLAIN + 2.4 * n1 + 3.0 * n2
    cald = np.where(r > 17, PLAIN + (prof - PLAIN) * (1 - 0.8 * mouth * smoothstep(15, 23, r)), prof)
    blendk = smoothstep(40, 46, r)
    h = np.where(r < 12, PLAIN + 1.2 * n1, base * blendk + (cald + n1 * 1.5 * smoothstep(20, 30, r)) * (1 - blendk))

    # the back of red's island: slag hills behind the spawn, the shoulder levelled for the hold
    back = smoothstep(-66, -88, Xf) * (10 + 4 * n2)
    h = h + np.where(Xf < 0, back, 0)
    sd = np.hypot((Xf + 74) / 15.0, (Zf - 12) / 12.5) + 0.1 * fbm(sh, 6, 2, seed=44)
    k = smoothstep(1.0, 1.6, sd)
    h = np.where(sd < 1.6, 63 * (1 - k) + h * k, h)
    h = np.where(sd < 1.0, 63, h)

    # Slag Ridge: the ground north of its line lifted, a sheer face over a talus apron toward the core
    scarp = LF.scarp(h, Xf, Zf, RIDGE_LINE, height=RIDGE_TOP - 58 - 2, side=-1, cliff=3, talus=6,
                     talus_height=0.35, reach=22)
    ridge_m = (scarp > h + 0.5)
    crag = fbm(sh, 7, 2, seed=43)
    top = np.where(scarp > RIDGE_TOP - 4, RIDGE_TOP - (scarp < RIDGE_TOP - 1) * 1.0, scarp)    # a level crest to walk
    h = np.where(Xf < -10, top + np.where(ridge_m & (scarp < RIDGE_TOP - 4), 1.4 * crag, 0), h)
    L.ridge = ridge_m & (Xf < -10) & (Zf < -28)

    # the core's plinth, levelled and eased into the plain
    d = np.hypot(Xf - CORE_AT[0], Zf - CORE_AT[1])
    h = LF.blend(h, np.full(sh, float(PLINTH_Y)), d < 7.5 + 7, width=7)
    L.plinth = d <= 7.5
    h = np.where(L.plinth, PLINTH_Y, h)

    # the beacon's pad on the ridge top
    bx0, bz0, bx1, bz1 = BEACON
    pad = (Xf >= bx0 - 2) & (Xf <= bx1 + 2) & (Zf >= bz0 - 2) & (Zf <= bz1 + 3)
    h = LF.blend(h, np.full(sh, float(BEACON_Y)), (Xf >= bx0 - 6) & (Xf <= bx1 + 6) & (Zf >= bz0 - 6) & (Zf <= bz1 + 7),
                 width=4)
    h = np.where(pad, BEACON_Y, h)

    # the Foundry Row's yard, level where the houses stand
    fy = shapes.inside(Xf, Zf, FOUNDRY)
    h = np.where(fy, np.round(PLAIN + 0.5 * n1), h)
    L.foundry = fy

    # slag heaps: cones of waste, scenery that is also cover
    for (cx, cz, rr, hh) in ((-70, 34, 6, 5), (-30, 38, 5, 4), (-78, 24, 4, 4)):
        dd = np.hypot((Xf - cx) / rr, (Zf - cz) / (rr * 0.85))
        h = np.where(dd < 1, h + np.round(hh * (1 - dd.clip(0, 1) ** 1.5)), h)

    # funnels: the blowhole and the pit, a block a block down to the tube's mouth
    L.funnels = []
    for (cx, cz), floor, rad in (BLOWHOLE, PIT):
        d = np.hypot(Xf - cx, Zf - cz)
        funnel = np.round(floor + np.maximum(0, d - 1.5)).astype(int)
        m = (d <= rad) & (funnel < h)
        h = np.where(m, funnel, h)
        L.funnels.append(m)

    # the underside is read off the ground as it stood before the ravine, so the island keeps its shape; the ravine's
    # floor is held three over it
    red = X < 0
    hp = np.where(red, h, rot(h))
    land_p = np.where(red, land_m, rot(land_m))
    d_edge = ndimage.distance_transform_edt(land_p)
    nn = sym(fbm(sh, 9, 3, seed=51))
    thick = 5 + 1.15 * d_edge + 5 * nn
    bottom0 = np.maximum(np.round(hp) - thick, 14 + 3 * sym(fbm(sh, 16, 2, seed=52))).round().astype(int)

    # the lava pit under the core: a round well in the plinth, lava to three under its rim
    dpit = np.hypot(Xf - CORE_AT[0], Zf - CORE_AT[1])
    L.pit = dpit <= PIT_R
    h = np.where(L.pit, PIT_BED, h)

    # the ravine: across the island between the teams along z, swelling to two and a half lake widths where it
    # bulges. Across it: lava on a bowl-shaped bed, a shore of varying width, a steep face to the rim
    off, hw, v = ravine_axes(Xf, Zf)
    c = np.abs(off)
    cw = np.where(off < 0, coast_width(v), coast_width(-v))
    c2 = hw - RAV_WALL
    c1 = c2 - np.minimum(cw, 0.4 * c2)            # lava keeps at least a fifth of the floor, however wide the shore
    shore_noise = fbm(sh, 5, 2, seed=63)
    floor_min = bottom0 + 3
    bed = np.maximum(np.round(41 + 5 * (c / np.maximum(c1, 1.0)) ** 2), floor_min)
    coast = np.maximum(COAST_Y + (shore_noise > 0.25), floor_min)
    t_wall = np.clip((c - c2) / RAV_WALL, 0, 1)
    face = coast + (h - coast) * t_wall ** 1.6
    carved = np.where(c < c1, bed, np.where(c < c2, coast, np.where(c < hw, np.minimum(h, face), h)))
    h = np.where(land_m & (c < hw), carved, h)
    lava = (c < c1) & (bed < LAVA_Y) & land_m
    L.rav = dict(off=off, hw=hw, c=c, c1=c1, c2=c2)
    # the bridgeheads' pads: level with the plain, a little wider than the deck, so the span meets ground
    padw = (np.abs(v) <= 8) & (c >= hw - 0.5) & (c <= hw + 9)
    h = np.where(land_m, LF.blend(h, np.full(sh, float(BRIDGE_Y)), padw, width=3), h)
    pad = (np.abs(v) <= 3.5) & (c >= hw - 0.5) & (c <= hw + 6)
    h = np.where(pad & land_m, BRIDGE_Y, h)
    H = np.round(h).astype(int)
    L.lava = lava & land_m

    # the roads and tracks, graded into the ground in order, none re-grading one laid before it
    laid = np.zeros(sh, bool)
    L.routes = []
    for rt in ROUTES:
        pts = spline(rt["pts"], 1.0)
        Hn, prof_ = LF.grade(H.astype(float), Xf, Zf, pts, width=rt["width"], max_grade=rt["grade"], shoulder=3,
                             water=lava, keep=laid)
        H = np.where(lava, H, np.round(Hn).astype(int))
        L.routes.append(dict(rt, line=pts, profile=prof_))
        laid |= shapes.polyline(Xf, Zf, pts)[0] <= rt["width"] / 2

    # red's drawn and blue's its half turn
    red = X < 0
    H = np.where(red, H, rot(H))
    L.lava = np.where(red, L.lava, rot(L.lava))
    L.pit = np.where(red, L.pit, rot(L.pit))
    land_f = np.where(red, land_m, rot(land_m))
    L.plinth = np.where(red, L.plinth, rot(L.plinth))
    L.ridge = np.where(red, L.ridge, rot(L.ridge))
    L.foundry = np.where(red, L.foundry, rot(L.foundry))
    L.funnels = [np.where(red, m, rot(m)) for m in L.funnels]
    L.land = land_f
    L.road_on = {}
    for rt in L.routes:
        on = (shapes.polyline(Xf, Zf, rt["line"])[0] <= rt["width"] / 2) & land_f
        L.road_on[rt["name"]] = np.where(red, on, rot(on))

    # the underside: thick and ragged, cone-shaped, never lower than 14, as the ground stood before the ravine
    L.X, L.Z, L.H = X, Z, np.where(land_f, H, -1)
    L.bottom = np.where(land_f, bottom0, 0)
    wood = shapes.inside(Xf, Zf, NORTH_WOOD) & (L.rav["c"] > L.rav["hw"] + 2)
    L.wood = (wood | rot(wood)) & land_f
    L.slope = slope_deg(L.H, land_f)
    L.Xf, L.Zf = Xf, Zf
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
    """Red's buildings as the library's House with footprint and door cell, keyed. Blue's are the half turn."""
    L = land()
    out = {}
    for h in HOUSES:
        s = spec(h)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        f = h["floor"] if "floor" in h else int(np.median([at(L, x, z) for x, z in cells]))
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=f, storeys=h["storeys"],
                   style=STYLES[h["style"]], door=s["door"], chimney=h.get("chimney", h["style"] == "cottage"),
                   roof="flat" if h["style"] in ("foundry", "hold", "tower") else "gable")
        out[h["key"]] = dict(spec=h, house=hs, cells=cells, door=door_cell(s), floor=f)
    return out


def _edge(cells):
    cells = set(cells)
    return {(x, z) for x, z in cells if any((x + a, z + b) not in cells for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


# ---- the plan raster --------------------------------------------------------------------------------------
def _tube_cells(pts, shrink=0.6):
    line = spline([(p[0], p[2]) for p in pts], 0.5)
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    best = {}
    for x, z in line:
        s = _arc_of(pts, x, z)
        fy = float(np.interp(s, arc, [p[1] for p in pts]))
        rr = float(np.interp(s, arc, [p[3] for p in pts])) * shrink
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                c = (int(math.floor(x + dx)), int(math.floor(z + dz)))
                d = math.hypot(c[0] + 0.5 - x, c[1] + 0.5 - z)
                if d <= max(1.0, rr) and d < best.get(c, (9e9,))[0]:
                    best[c] = (d, int(round(fy)) - 1)
    return {c: y for c, (_, y) in best.items()}


def _arc_of(pts, x, z):
    best, acc = (1e9, 0.0), 0.0
    for a, b in zip(pts, pts[1:]):
        L_ = math.hypot(b[0] - a[0], b[2] - a[2]) or 1e-9
        t = max(0.0, min(1.0, ((x - a[0]) * (b[0] - a[0]) + (z - a[2]) * (b[2] - a[2])) / L_ ** 2))
        d = math.hypot(x - (a[0] + t * (b[0] - a[0])), z - (a[2] + t * (b[2] - a[2])))
        if d < best[0]:
            best = (d, acc + t * L_)
        acc += L_
    return best[1]


@lru_cache(maxsize=1)
def build():
    """The plan raster: red drawn into arrays and blue its half turn, the tube on storey 1 for both."""
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    k_ = R.kinds
    K = np.full(L.H.shape, k_["void"])
    K[L.land] = k_["ground"]
    K[L.land & (L.slope > 45)] = k_["steep"]
    K[L.wood] = k_["wood"]
    K[L.ridge & L.land] = k_["ridge"]
    for rt in L.routes:
        K[L.road_on[rt["name"]]] = k_[rt["kind"]]
    K[L.plinth] = k_["plinth"]
    for m in L.funnels:
        K[m] = k_["pit"]
    K[L.lava | L.pit] = k_["lava"]
    H = np.where(L.land, L.H, 0)
    ty = (L.X >= -67) & (L.X <= -64) & (L.Z >= 8) & (L.Z <= 16) & (L.X < 0)
    K[ty] = k_["yard"]
    red = L.X < 0
    # red's buildings drawn on red's half, then the whole turned
    Kr, Hr = K.copy(), H.copy()
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
    for x in range(BRIDGE_X[0], 0):                                    # the Slag Bridge's red span, to the keystone
        for z in range(BRIDGE_Z[0], BRIDGE_Z[1] + 1):
            Kr[x - X_MIN, z - Z_MIN], Hr[x - X_MIN, z - Z_MIN] = k_["bridge"], BRIDGE_Y
    key = (L.X < 0) & (np.hypot(L.Xf + 0.5, L.Zf + 0.5) <= KEY_R)
    Kr[key], Hr[key] = k_["stack"], BRIDGE_Y
    for sx, sz, sr, top, _ in STACKS:
        m = (L.X < 0) & (np.hypot(L.Xf - sx, L.Zf - sz) <= 0.7 * sr)
        Kr[m], Hr[m] = k_["stack"], top
    K = np.where(red, Kr, rot(Kr))
    H = np.where(red, Hr, rot(Hr))
    R.H[:] = H
    R.K[:] = K
    U = R.storey(1)
    for (x, z), y in _tube_cells(VENT).items():
        if R.inside(x, z):
            U.cell(x, z, y, "tunnel")
    return R


def links():
    """The vent tube's two mouths: a pit floor cell joined to the tube cell under it, both ways, for both halves."""
    out = []
    for end in (VENT[0], VENT[-1]):
        a = (end[0], end[2])
        ia = SYM.point(*a)
        for p, q in (((a[0], a[1]), (a[0], a[1], 1)), ((int(ia[0]), int(ia[1])), (int(ia[0]), int(ia[1]), 1))):
            out += [(p, q, 1, "tube"), (q, p, 1, "tube")]
    return out


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN, yaw=270, kit="spawn-kit", area=SPAWN_AREA, protect=("iron ore",)))
    O.add(Core("red-core", "Red Core", "red-team", CORE_BOX, leak=5), name="Blue Core")
    O.add(Observer((0, 90, 0), yaw=90), mirror=False)
    return O
