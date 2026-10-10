"""Riftwater, ported onto pgmvox: the plan. A river valley split down the middle by a bottomless rift; on each
side a market town on a bluff, a mining village under a wooded ridge and wheat fields between them, and each
side's river pouring off the rift's lip as one of two facing waterfalls. Destroy the monument, two a team.

Everything here is written for red (west, x < 0); blue is the mirror image across the rift, x' = -1 - x, which is
pgmvox's Symmetry("mirror_x") about its default axis. The coordinates, heights and places are the original
board's (freeform/opus55-freeform-riftwater/scripts/plan.py, terrain.py, buildings.py, underground.py), as built
after its plan changed: the knoll at (-22, 74), the gaol on the square's corner, the town climbing to the square.

    land()        the red half's heightfield, water, outline and underside: what gen.py lays and the plan walks
    build()       the plan Raster over the whole board: kinds and floors, storey 1 the underground, storey 2 decks
    objectives()  teams, spawns, the four monuments and the observer point, drawn once for red
    houses()      every building as a pgmvox.build.House plus its footprint and door, read by plan and gen alike

Heights follow the library: H is the y of the floor block and a player stands at H + 1.
"""
import math
import os
import sys
from functools import lru_cache

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import landform as LF  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox import under as under_lib  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.noise import fbm, spline, smoothstep  # noqa: E402
from pgmvox import noise  # noqa: E402
from pgmvox import field as F  # noqa: E402
from pgmvox.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import island_bottom, slope_deg  # noqa: E402

BOARD = "riftwater"
X_MIN, X_MAX = -120, 119
Z_MIN, Z_MAX = -88, 87
SYM = Symmetry("mirror_x")                       # x' = -1 - x: the rift's middle is the seam between -1 and 0
RIFT = 16                                        # the build zone: |x| <= 16 (the rift's bays reach -16)
POND_LEVEL, RIVER_LEVEL, WEIR_X = 48, 45, -66

SPAWN = (-98, 60, -7)                            # feet in the watch house's hall, floor 59
SPAWN_AREA = Box(-108, 0, -14, -85, 127, -1)
MONUMENTS = {"square": ((-66, -44), 52, "Market Square Monument"),     # (x, z), the ground, the name
             "green": ((-66, 48), 50, "Winding Green Monument")}

# ---- places (red half): name and where, for the sketch and the annotated top-down -----------------------
PLACES = [
    ("The Watch House", (-98, -7)), ("The Ridge", (-112, 20)), ("North Wood", (-100, -45)),
    ("Woodcutter's Hut", (-104, -64)), ("Market Square", (-66, -44)), ("Market Town", (-40, -60)),
    ("The Old Bridge", (-10, -44)), ("The Chapel", (-46, -75)), ("The Falls Inn", (-28, -22)),
    ("The Gaol", (-52, -34)), ("Mill Pond", (-84, 20)), ("The Mill", (-62, 4)), ("Stone Bridge", (-36, 3)),
    ("The Falls", (-12, 0)), ("Ironhollow", (-88, 66)), ("The Headframe", (-84, 56)),
    ("Winding Green", (-66, 48)), ("The Fields", (-40, 57)), ("The Sinkhole", (-50, 40)),
    ("Lone Oak Knoll", (-22, 74)), ("The Cutting", (-110, 68)),
]
UNDERGROUND = [("Falls Cave mouth", (-11, 4)), ("Lake chamber", (-40, 14)), ("Pillar Hall", (-46, 26)),
               ("Smugglers' grotto", (-60, 6)), ("Gaol cellar", (-52, -34)), ("Ironhollow Mine", (-96, 30))]
NORTH_WOOD = [(-120, -88), (-74, -88), (-74, -74), (-82, -52), (-90, -30), (-104, -20), (-120, -24)]
RIVER = [(-74, 22), (-66, 17), (-56, 13), (-46, 7), (-36, 3), (-26, 1), (-17, 0), (-11, 0)]
FIELD = (-50, 45, -31, 69)                       # the wheat field: x0, z0, x1, z1

# Routes: polylines a player walks. kind: street (hard), lane (soft), path (forest)
ROUTES = [
    dict(name="Spawn Lane", kind="lane", pts=[(-84, -7), (-78, -12), (-74, -24), (-72, -36)]),
    dict(name="Spawn Lane south", kind="lane", pts=[(-78, -12), (-74, 0), (-71, 12), (-70, 22), (-70, 34), (-68, 40)]),
    dict(name="Main Street", kind="street", pts=[(-56, -44), (-44, -45), (-32, -43), (-20, -44), (-12, -44)]),
    dict(name="Bridge Street", kind="street", pts=[(-42, -44), (-40, -32), (-36, -20), (-36, -11)]),
    dict(name="North Lane", kind="lane", pts=[(-56, -53), (-56, -59), (-50, -63), (-40, -66), (-26, -64), (-16, -70)]),
    dict(name="Mill Lane", kind="lane", pts=[(-38, -10), (-48, -4), (-56, -2), (-62, -2)]),
    dict(name="Field Road", kind="lane", pts=[(-36, 15), (-40, 22), (-46, 30), (-56, 40), (-61, 46)]),
    dict(name="Farm Track", kind="lane", pts=[(-61, 52), (-58, 60), (-56, 66), (-46, 79), (-34, 80), (-24, 76)]),
    dict(name="Falls Walk", kind="lane", pts=[(-34, 12), (-26, 11), (-18, 9), (-14, 7)]),
    dict(name="Spring Path", kind="lane", pts=[(-96, 0), (-100, 12), (-99, 28), (-93, 34), (-89, 38), (-88, 44)]),
    dict(name="Village Road", kind="lane", pts=[(-88, 44), (-80, 46), (-72, 47), (-62, 48)]),
    dict(name="Forest Path", kind="path", pts=[(-90, -14), (-88, -26), (-94, -40), (-96, -52), (-100, -60)]),
    dict(name="Clearing Path", kind="path", pts=[(-99, 64), (-102, 68), (-108, 68)]),
]
WIDTH = {"street": 5, "lane": 3, "path": 2}

# ---- buildings (red half): the footprint with walls, storeys, which side the door is on ------------------
HOUSES = [
    # the market town
    dict(key="hall", rect=(-74, -64, -59, -56), storeys=2, door="s", style="town", floor=52),
    dict(key="h1", rect=(-54, -56, -48, -48), storeys=2, door="s", style="town"),
    dict(key="shop1", rect=(-46, -55, -41, -48), storeys=3, door="s", style="town", sign="Chandler"),
    dict(key="h2", rect=(-36, -56, -29, -48), storeys=2, door="s", style="town"),
    dict(key="bakery", rect=(-27, -54, -22, -48), storeys=2, door="s", style="town", sign="Bakery"),
    dict(key="h3", rect=(-20, -55, -15, -48), storeys=2, door="s", style="town"),
    dict(key="h4", rect=(-37, -40, -30, -33), storeys=2, door="n", style="town"),
    dict(key="shop2", rect=(-27, -40, -21, -34), storeys=2, door="n", style="town", sign="Cooper"),
    dict(key="h5", rect=(-18, -40, -14, -35), storeys=1, door="n", style="town"),
    dict(key="gaol", rect=(-56, -38, -48, -30), storeys=2, door="w", style="stone", floor=52, inside=True),
    dict(key="h6", rect=(-49, -26, -43, -19), storeys=2, door="e", style="town"),
    dict(key="h7", rect=(-48, -15, -43, -11), storeys=1, door="e", style="town"),
    dict(key="inn", rect=(-33, -28, -24, -17), storeys=2, door="w", style="town", sign="The Falls Inn"),
    dict(key="h8", rect=(-34, -78, -28, -70), storeys=2, door="s", style="town"),
    dict(key="h9", rect=(-24, -80, -18, -73), storeys=2, door="s", style="town"),
    dict(key="shop3", rect=(-69, -80, -61, -72), storeys=1, door="s", style="town", sign="Saddler"),
    dict(key="chapel", rect=(-50, -80, -38, -71), storeys=2, door="s", style="stone", chimney=False),
    # the spawn and the woods
    dict(key="watch", rect=(-102, -11, -94, -3), storeys=2, door="e", style="town", floor=59, inside=True),
    dict(key="hut", rect=(-107, -67, -102, -62), storeys=1, door="e", style="village"),
    # the river
    dict(key="mill", rect=(-67, 1, -58, 7), storeys=2, door="n", style="mill"),
    # Ironhollow
    dict(key="c1", rect=(-98, 38, -92, 44), storeys=1, door="e", style="village"),
    dict(key="tall", rect=(-99, 49, -92, 55), storeys=2, door="e", style="village"),
    dict(key="wing", rect=(-98, 45, -93, 48), storeys=1, door="n", style="village", floor_of="tall", chimney=False),
    dict(key="c2", rect=(-97, 61, -91, 68), storeys=1, door="e", style="village"),
    dict(key="big", rect=(-90, 71, -82, 76), storeys=2, door="n", style="village"),
    dict(key="lean", rect=(-95, 72, -91, 76), storeys=1, door="n", style="village", floor_of="big"),
    dict(key="c3", rect=(-79, 69, -74, 75), storeys=1, door="n", style="village"),
    dict(key="engine", rect=(-80, 49, -75, 55), storeys=1, door="w", style="stone", chimney=False),
    dict(key="smithy", rect=(-78, 59, -72, 64), storeys=1, door="w", style="village", chimney=False),
]
TOWERS = [  # masonry towers the library's house does not make: (key, x0, z0, x1, z1, height over the floor)
    ("belfry", -55, -79, -51, -73, 20),
    ("watch tower", -107, -10, -103, -4, 16),
]
BARN = (-32, 72, -26, 78)                         # x0, z0, x1, z1 (dressing: the farm's barn)

# ---- the underground (red half): (x, floor y, z, radius); the floor is the lowest air ---------------------
CAVE = {
    "gallery": [(-9, 36, 2, 2.6), (-14, 36, 3, 3.0), (-20, 35, 5, 3.4), (-27, 34, 8, 3.2), (-34, 33, 11, 3.6),
                (-40, 32, 14, 4.0)],
    "south": [(-40, 32, 14, 3.0), (-44, 33, 20, 2.8), (-47, 35, 27, 2.6), (-49, 37, 33, 2.8), (-50, 39, 38, 3.0)],
    "north": [(-40, 32, 14, 3.0), (-43, 32, 7, 2.6), (-46, 33, 0, 2.6), (-49, 35, -8, 2.8), (-52, 37, -15, 2.6),
              (-53, 40, -21, 2.5), (-53, 42, -27, 2.2)],
    "grotto": [(-46, 33, 0, 2.2), (-50, 33, 2, 2.0), (-54, 33, 4, 2.4), (-58, 33, 5, 2.2)],
    "west": [(-49, 37, 33, 2.4), (-53, 38, 35, 2.2), (-57, 39, 37, 2.0)],
}
CHAMBERS = [  # (x, floor y, z, rx, height, name): ellipsoid halls with a level floor
    (-40, 31, 15, 8.5, 4.8, "lake chamber"), (-43, 31, 12, 5.5, 4.0, None),
    (-46, 34, 26, 7.5, 4.2, "pillar hall"), (-43, 34, 23, 5.0, 3.6, None),
    (-60, 33, 6, 3.6, 3.0, "grotto"),
    (-18, 35, 9, 2.2, 2.0, None), (-26, 34, 2, 2.0, 2.0, None), (-31, 33, 15, 2.4, 2.0, None),
    (-48, 36, 31, 2.0, 2.0, None), (-50, 35, -6, 2.0, 2.0, None),
]
LAKE = (-40, 31, 15)
MINE = [(-104, 59, 5), (-104, 57, 11), (-103, 53, 23), (-100, 50, 31), (-95, 47, 40), (-89, 45, 48), (-84, 45, 56),
        (-76, 44, 52), (-68, 42, 46), (-62, 40, 41), (-57, 39, 37)]
SHAFT = (-84, 56)
CELLAR = (-55, 43, -37, -49, -31)                # x0, floor y (lowest air), z0, x1, z1: walls included
GAOL_LADDER = (-50, -33)
SINKHOLE = ((-50, 38), 38, 10.5)                 # centre, the floor block at the bottom, radius
SPOIL = ((-101, 79), 7, 6)                       # centre, radius, height
STONE_BRIDGE = (-38, -34, -10, 14, 3)            # x0, x1, z north end, z south end, z of the keystone
OLD_BRIDGE = (-44, -12, -5)                      # z of the middle, the face x, the broken end x
FOOTBRIDGE_ROUTE = "Spawn Lane south"

KINDS = ["void", "grass", "wood", "rock", "water", "street", "lane", "path", "square", "green", "field",
         "house", "inside", "door", "stair", "sinkhole", "deck", "cave", "mine", "cellar", "shaft"]
COLOURS = {"void": (30, 32, 44), "grass": (140, 182, 92), "wood": (64, 112, 58), "rock": (128, 124, 116),
           "water": (62, 108, 205), "street": (128, 128, 134), "lane": (168, 140, 98), "path": (118, 92, 60),
           "square": (196, 190, 176), "green": (170, 212, 120), "field": (220, 196, 92), "house": (150, 92, 70),
           "inside": (205, 172, 140), "door": (240, 220, 170), "stair": (150, 150, 150), "sinkhole": (110, 98, 82), "deck": (182, 176, 166),
           "cave": (92, 84, 98), "mine": (134, 98, 62), "cellar": (110, 110, 120), "shaft": (60, 50, 40)}
WALK = {k for k in KINDS if k not in ("void", "house")}


# ---- the land ---------------------------------------------------------------------------------------------
class Land:
    """The red half's grids, indexed [i, k] with x = X_MIN + i (x < 0 only) and z = Z_MIN + k."""


def _rift_edge(nz):
    """The rift's lip, x of the last land column at each z: ragged, bitten into bays where nothing stands, held
    straight under the town's houses, at the Old Bridge and at the falls."""
    zz = np.arange(Z_MIN, Z_MAX + 1)
    edge_n = fbm((nz,), 10, 2, seed=21)
    bays = 4.5 * (0.5 + 0.5 * fbm((nz,), 22, 2, seed=25))
    hold = np.maximum.reduce([np.exp(-((zz + 45) / 16.0) ** 4), np.exp(-((zz - 1) / 6.0) ** 4)])
    return -11 + np.round(edge_n * 1.2).clip(-1, 0) - np.round(bays * (1 - hold))


@lru_cache(maxsize=1)
def land():
    """The red half: heights H (floor block y), water surface (0 where dry), the land mask, the underside's
    bottom, the river's distance, the routes' graded footprints. Cached: plan, sketch and gen all read one."""
    L = Land()
    xs, zs = np.arange(X_MIN, 0), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    n_small, n_big = fbm(sh, 12, 3, seed=11), fbm(sh, 40, 3, seed=12)

    # the outline: the rift's ragged lip and the board's inset edges
    land = shapes.island(X, Z, (X_MIN, Z_MIN, -1, Z_MAX), east=-1 - _rift_edge(sh[1])[None, :],
                         west=noise.line(sh, "z", 16, seed=22, amp=4, base=2, clip=(0, 6)),
                         north=noise.line(sh, "x", 16, seed=23, amp=5, base=2, clip=(0, 7)),
                         south=noise.line(sh, "x", 16, seed=24, amp=5, base=2, clip=(0, 7)))

    # the open ground: the town climbs from the rift to the square; fields rise to the south and the ridge
    course = spline(RIVER, 0.5)
    cx_, cz_ = np.array([p[0] for p in course]), np.array([p[1] for p in course])
    order = np.argsort(cx_)
    zr = np.interp(Xf, cx_[order], cz_[order])
    north = Z < zr
    h_n = F.terms(Xf, Zf, 48.5, F.Ramp("x", -14, -64, 3.5), F.Ramp("x", -74, -96, 2.0),
                  F.Gauss((-44, -78), 16.0, 4.5, rz=11.0))
    h_s = F.terms(Xf, Zf, 47.2, F.Ramp("z", 25, 80, 1.8), F.Ramp("x", -64, -98, 4.5))
    h_w = F.terms(Xf, Zf, 52.5, F.Ramp("x", -80, -98, 2.5), F.Ramp("z", -10, 30, -1.5), F.Ramp("z", 30, 60, 1.0))
    h = F.mix(np.where(north, h_n, h_s), h_w, smoothstep(-70, -80, Xf))
    h = F.terms(Xf, Zf, h, F.Noise(n_small, 0.8), F.Noise(n_big, 1.2))

    # the river valley: a bluff on the town side, a gentle bank on the field side, the valley floor a block
    # over each reach's water; then pgmvox's watercourse cuts the channel and finds the weir as a fall
    d_r, _ = shapes.polyline(Xf, Zf, course)
    in_reach = Xf > -75
    w = 3.0 + 0.6 * smoothstep(-60, -15, Xf)
    level = np.where(Xf < WEIR_X, POND_LEVEL, RIVER_LEVEL)
    bluff = LF.profile(h, d_r, level + 1, [LF.Step(w, w + 7, "ground")], mode="cut")
    bank = LF.profile(h, d_r, level + 1.3, [LF.Step(w, w + 14, "ground")], mode="cut")
    h = np.where(in_reach, np.where(north, bluff, bank), h)
    h = np.where(in_reach & (d_r <= w), level + 1, h)

    # the mill pond, with a spit from its south-west shore
    pn = fbm(sh, 8, 2, seed=31)
    pr = np.hypot((Xf + 84) / 12.5, (Zf - 20) / 9.5) + 0.12 * pn
    spit, _ = shapes.polyline(Xf, Zf, [(-92, 30), (-86, 24), (-83, 21)])
    pond = (pr < 1.0) & ~(spit < 1.6)
    shore = smoothstep(1.0, 1.5, pr)
    h = np.where(pr < 1.5, np.minimum(h, POND_LEVEL + 1 + (h - POND_LEVEL - 1) * shore), h)
    h = np.where(spit < 1.6, np.maximum(h, POND_LEVEL + 1), h)
    pond_bed = POND_LEVEL - 1 - 3.5 * (1 - pr.clip(0, 1) ** 2)

    # the ridge: its foot wanders, its crest is ridged noise, two spurs reach east; cut into 3-block terraces
    foot = noise.line(sh, "z", 24, seed=40, amp=4, base=-100)
    spur_n, _ = shapes.polyline(Xf, Zf, [(-114, -68), (-98, -74), (-82, -80)])
    spur_s, _ = shapes.polyline(Xf, Zf, [(-114, 70), (-100, 76), (-88, 82)])
    crest = noise.line(sh, "z", 30, seed=41, amp=5, base=73) + 4 * np.exp(-((Zf + 72) / 18) ** 2)
    t = smoothstep(foot, foot - 15, Xf)
    ridge_n = fbm(sh, 10, 3, seed=42)
    crag = 1 - np.abs(fbm(sh, 7, 2, seed=43))
    ridge = h + (crest - h).clip(0) * t + t * (2.5 * ridge_n + 4 * smoothstep(0.75, 0.95, crag))
    for d, top in ((spur_n, 66), (spur_s, 63)):
        arm = top - 0.25 * np.abs(Xf + 100) + 2 * ridge_n
        ridge = np.maximum(ridge, h + (arm - h).clip(0) * smoothstep(14, 3, d))
    ridge = LF.terraces(ridge, t > 0.25, step=3, riser=0.45)
    h = np.where(ridge > h, ridge, h)
    h -= 7 * smoothstep(-114, -120, Xf)

    # the spawn shoulder: an oval spur at the ridge's foot, its top levelled at 59 for the watch house
    sd = shapes.ellipse_distance(Xf, Zf, (-97, -7), 12.0, 9.5) + 0.12 * fbm(sh, 6, 2, seed=44)
    h = LF.level(h, sd, 59, inner=1.0, outer=1.55, mode="lift")

    # the square and the green: level where the monuments stand, eased into the ground over eight blocks
    for (mx, mz), lvl, _ in MONUMENTS.values():
        r = 11 if mz < 0 else 9
        h = LF.blend(h, np.full(sh, float(lvl)), np.hypot(Xf - mx, Zf - mz) < r + 8, width=8)

    # Lone Oak Knoll: a round rise by the rift
    h = LF.spire(h, Xf, 74 + (Zf - 74) / 1.25, (-22, 74), r=16, top=float(h[-22 - X_MIN, 74 - Z_MIN]) + 6.5,
                 taper=0.7, jag=0.0)

    # the river channel: the valley floor is level + 1 along the line, so four down is a bed three under the
    # water; the weir is where the bed falls three
    H = h.copy()
    riv = [p for p in course if p[0] <= -10]
    H, river = LF.watercourse(H, Xf, Zf, riv, width=2 * 3.3, depth=4, water=3, bank=1, fall_min=2, reach_min=4)
    channel = river.mask & in_reach & land

    Hi = np.round(H).astype(int)
    water = np.zeros(sh, int)
    water[channel] = river.surface[channel].astype(int)
    water[pond] = POND_LEVEL
    Hi[pond] = np.floor(pond_bed[pond]).astype(int)
    outlet = (np.hypot(Xf + 74, Zf - 22) < 4) & (d_r < w + 0.5)
    water[outlet] = POND_LEVEL
    Hi[outlet] = np.minimum(Hi[outlet], POND_LEVEL - 2)
    Hi = np.where(water > 0, np.minimum(Hi, water - 1), Hi)

    # the routes, graded into the ground in order, none re-grading one laid before it
    laid = np.zeros(sh, bool)
    L.routes = []
    for r in ROUTES:
        pts = spline(r["pts"], 1.0)
        wdt = WIDTH[r["kind"]]
        Hn, prof = LF.grade(Hi.astype(float), Xf, Zf, pts, width=wdt, max_grade=0.25, shoulder=2,
                            water=water > 0, keep=laid)
        Hi = np.where(water > 0, Hi, np.round(Hn).astype(int))
        L.routes.append(dict(r, line=pts, profile=prof, width=wdt))
        laid |= shapes.polyline(Xf, Zf, pts)[0] <= wdt / 2

    # the square: a built floor at 52 with rounded corners; the green at 50
    sq = shapes.inside(Xf, Zf, [(-76, -53), (-56, -53), (-56, -34), (-76, -34)])
    corner = np.hypot(np.maximum.reduce([-73 - Xf, 0 * Xf, Xf + 60]), np.maximum.reduce([-50 - Zf, 0 * Zf, Zf + 38]))
    L.square = sq & (corner <= 3.2)
    Hi[L.square] = 52
    L.green = shapes.disc(Xf, Zf, -66, 48, 8.5) & (water == 0)
    Hi[L.green] = 50

    # the sinkhole: concentric one-block steps from the cave's floor to the field
    (sx_, sz_), floor, rad = SINKHOLE
    d = np.hypot(Xf - sx_, Zf - sz_)
    funnel = np.round(floor + np.maximum(0, d - 1.5)).astype(int)        # a block a block: climbable
    L.sinkhole = (d <= rad) & (funnel < Hi)
    Hi = np.where(L.sinkhole, funnel, Hi)
    # the spoil heap behind Ironhollow
    (px_, pz_), pr_, ph_ = SPOIL
    dd = np.hypot((Xf - px_) / pr_, (Zf - pz_) / (pr_ * 0.8))
    L.spoil = (dd < 1) & land
    Hi = np.where(L.spoil, Hi + np.round(ph_ * (1 - dd.clip(0, 1) ** 1.6)).astype(int), Hi)

    # the underside: sheer under the rift for about thirty blocks, tapering everywhere else
    bottom = island_bottom(Hi, land, X > -14, taper=(4, 0.9), sheer_taper=(26, 1.2), rough=4 * fbm(sh, 9, 3, seed=51),
                           floor=4 + 3 * fbm(sh, 16, 2, seed=52))

    L.X, L.Z, L.H, L.water, L.land, L.north, L.bottom = X, Z, np.where(land, Hi, -1), np.where(land, water, 0), \
        land, north, np.where(land, bottom, 0)
    L.d_river, L.river, L.falls = d_r, channel, river.falls
    L.forest = (shapes.inside(Xf, Zf, NORTH_WOOD) | (Xf < -100)) & land
    L.slope = slope_deg(L.H, land)
    return L


def at(L, x, z):
    """The red half's H at a world column (x < 0)."""
    return int(L.H[x - X_MIN, z - Z_MIN])


# ---- the buildings ----------------------------------------------------------------------------------------
STYLES = {
    # the town: brick ground storey, spruce posts with white clay infill above, a dark oak roof
    "town": dict(ground=[(45, 0)], upper=[(159, 0)], post=1, gable=(5, 1), floor=(5, 1), roof=(5, 5),
                 stair=164, slab=(126, 5), door=193, window=(102, 0), chimney=(45, 0)),
    # Ironhollow: spruce plank walls in spruce posts, a spruce roof, oak gables
    "village": dict(ground=[(5, 1)], upper=[(5, 1)], post=1, gable=(5, 0), floor=(5, 0), roof=(5, 1),
                    stair=134, slab=(126, 1), door=193, window=(102, 0), chimney=(4, 0)),
    # stone: stone brick under a dark oak roof (the gaol, the chapel, the engine house)
    "stone": dict(ground=[(98, 0), (98, 0), (98, 2)], upper=[(98, 0)], post=None, gable=(98, 0), floor=(5, 5),
                  roof=(5, 5), stair=164, slab=(126, 5), door=197, window=(101, 0), chimney=(98, 0)),
    # the mill: a stone ground storey with a spruce plank one over it
    "mill": dict(ground=[(98, 0), (4, 0)], upper=[(5, 1)], post=1, gable=(5, 1), floor=(5, 1), roof=(5, 5),
                 stair=164, slab=(126, 5), door=197, window=(102, 0)),
}


def spec(h):
    """A HOUSES entry as the library's House: its centre on the snapping the library wants, the ridge along the
    side the door is not on, and the door's sign (+1 the frame's +v)."""
    x0, z0, x1, z1 = h["rect"]
    nx, nz = x1 - x0 + 1, z1 - z0 + 1
    if h["door"] in "ns":
        heading, Lh, W, sign = 0, nx, nz, (1 if h["door"] == "s" else -1)
    else:                                           # heading 90: u runs south, +v points west
        heading, Lh, W, sign = 90, nz, nx, (1 if h["door"] == "w" else -1)
    return dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=heading, L=Lh, W=W, door=sign)


def door_cell(s):
    """Where pgmvox.build.house will put the door of a spec: the wall cell on the door side nearest the middle.
    The library does not say until it has built the house, so the plan works it out the same way."""
    fr = Frame(s["cx"], s["cz"], s["heading"])
    m, X, Z, U, V = fr.mask(s["L"], s["W"])
    wall = shapes.boundary(m, diagonal=True)
    cands = [(abs(U[i, k]), int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(wall))
             if s["door"] * V[i, k] > s["W"] / 2 - 1 and abs(U[i, k]) < s["L"] / 2 - 1.5]
    _, x, z = min(cands)
    return x, z


@lru_cache(maxsize=1)
def houses():
    """Every building: the House the library builds, its footprint cells and its door cell, keyed."""
    L = land()
    out = {}
    for h in HOUSES:
        s = spec(h)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        if "floor" in h:
            f = h["floor"]
        elif "floor_of" in h:
            f = out[h["floor_of"]]["house"].floor
        else:
            f = int(np.median([at(L, x, z) for x, z in cells]))
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=f, storeys=h["storeys"],
                   style=STYLES[h["style"]], door=s["door"], chimney=h.get("chimney", True))
        out[h["key"]] = dict(spec=h, house=hs, cells=cells, door=door_cell(s), floor=f)
    return out


# ---- the plan raster --------------------------------------------------------------------------------------
def _tube_cells(pts, shrink=0.6):
    """The floor cells of a cave branch: within a share of its radius of its centre line, with the floor
    interpolated along it."""
    line = spline([(p[0], p[2]) for p in pts], 0.5)
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    best = {}
    for x, z in line:
        s = shapes.nearest_on([(p[0], p[2]) for p in pts], x, z)[1]
        fy = float(np.interp(s, arc, [p[1] for p in pts]))
        r = float(np.interp(s, arc, [p[3] for p in pts])) * shrink
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                c = (int(math.floor(x + dx)), int(math.floor(z + dz)))
                d = math.hypot(c[0] + 0.5 - x, c[1] + 0.5 - z)
                if d <= max(1.0, r) and d < best.get(c, (9e9,))[0]:
                    best[c] = (d, int(round(fy)) - 1)
    return {c: y for c, (_, y) in best.items()}


def mine_line():
    """The mine's galleries: one cell a block along the waypoints, the floor (lowest air) changing at most
    one a step, as gen.py carves them."""
    return under_lib.gallery_line(MINE)


def deck_y(L, z):
    """The stone bridge's deck: from the town bank's height over a crown a block over the higher bank, down to
    the field bank's."""
    x0, x1, zN, zS, _ = STONE_BRIDGE
    yN = int(np.median([at(L, x, zN - 1) for x in range(x0, x1 + 1)]))
    yS = int(np.median([at(L, x, zS + 1) for x in range(x0, x1 + 1)]))
    crown = max(yN, yS) + 1
    if z <= 1:
        return int(round(yN + (crown - yN) * (z - zN) / (1 - zN)))
    return int(round(crown - (crown - yS) * (z - 1) / (zS - 1)))


@lru_cache(maxsize=1)
def build():
    """The whole board as a plan raster: the ground storey from land() and the buildings, storey 1 the cave,
    the mine and the cellar, storey 2 the bridge decks. Blue's half is drawn as red's mirror."""
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    K = np.full(L.H.shape, R.kinds["void"])
    K[L.land] = R.kinds["grass"]
    K[L.forest] = R.kinds["wood"]
    K[L.land & (L.slope > 45)] = R.kinds["rock"]
    Xf, Zf = L.X.astype(float), L.Z.astype(float)
    for r in L.routes:
        on = (shapes.polyline(Xf, Zf, r["line"])[0] <= r["width"] / 2) & L.land
        K[on] = R.kinds[r["kind"]]
    x0, z0, x1, z1 = FIELD
    K[(L.X >= x0) & (L.X <= x1) & (L.Z >= z0) & (L.Z <= z1)] = R.kinds["field"]
    K[L.square] = R.kinds["square"]
    K[L.green] = R.kinds["green"]
    K[L.sinkhole] = R.kinds["sinkhole"]
    K[L.water > 0] = R.kinds["water"]
    H = np.where(L.water > 0, L.water, L.H)       # a swimmer's floor is the water's surface: a bank a block
    H = np.where(L.land, H, 0)                     # over it is a step out
    # the spawn terrace in front of the watch house
    K[(L.X >= -93) & (L.X <= -86) & (L.Z >= -12) & (L.Z <= -2)] = R.kinds["square"]
    H[(L.X >= -93) & (L.X <= -86) & (L.Z >= -12) & (L.Z <= -2)] = 59
    for key, b in houses().items():
        inside = b["spec"].get("inside")
        for x, z in b["cells"]:
            i, k = x - X_MIN, z - Z_MIN
            K[i, k] = R.kinds["inside" if inside else "house"]
            H[i, k] = b["floor"]
        if inside:
            for x, z in shapes_boundary(b["cells"]):
                K[x - X_MIN, z - Z_MIN] = R.kinds["house"]
        dx, dz = b["door"]
        K[dx - X_MIN, dz - Z_MIN] = R.kinds["door"]
    for _, tx0, tz0, tx1, tz1, _ in TOWERS:
        K[tx0 - X_MIN:tx1 - X_MIN + 1, tz0 - Z_MIN:tz1 - Z_MIN + 1] = R.kinds["house"]
    gx, gz = GAOL_LADDER
    K[gx - X_MIN, gz - Z_MIN] = R.kinds["shaft"]
    sx, sz = SHAFT                                 # the shaft's mouth in the headframe's collar
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            K[sx + ddx - X_MIN, sz + ddz - Z_MIN] = R.kinds["shaft"]
    R.H[:] = SYM.whole(H)
    R.K[:] = SYM.whole(K)
    # the steps from the terrace down to Spawn Lane: a flight climbing west, drawn for both halves
    g = at(L, -78, -7)
    n = 59 - g
    if n > 0:
        R.flight((-85 + n, -7), "w", width=(-1, 1), h0=g + 1, n=n)

    # storey 1: the underground
    U = R.storey(1)
    cells = {}
    for pts in CAVE.values():
        for c, y in _tube_cells(pts).items():
            cells.setdefault(c, ("cave", y))
    for cx, fy, cz, rx, _, _ in CHAMBERS:
        for x in range(int(cx - rx), int(cx + rx) + 1):
            for z in range(int(cz - rx), int(cz + rx) + 1):
                if math.hypot(x + 0.5 - cx, z + 0.5 - cz) <= rx * 0.8:
                    cells.setdefault((x, z), ("cave", fy - 1))
    for z in range(1, 10):                         # the ledge at the mouth, in the rift face
        for x in (-11, -10):
            if not (x == -10 and z < 4):
                cells[(x, z)] = ("cave", 35)
    for x, y, z in mine_line():
        for ddx in (-1, 0, 1):
            for ddz in (-1, 0, 1):
                cells[(x + ddx, z + ddz)] = ("mine", y - 1)
    cx0, cfy, cz0, cx1, cz1 = CELLAR
    for x in range(cx0 + 1, cx1):
        for z in range(cz0 + 1, cz1 + 4):
            cells[(x, z)] = ("cellar", cfy - 1)
    for (x, z), (kind, y) in cells.items():
        if R.inside(x, z):
            U.cell(x, z, y, kind)

    # storey 2: the decks over water and void
    D = R.storey(2)
    bx0, bx1, zN, zS, _ = STONE_BRIDGE
    for z in range(zN, zS + 1):
        for x in range(bx0 + 1, bx1):
            D.cell(x, z, deck_y(L, z), "deck")
    oz, face, end = OLD_BRIDGE
    deck = at(L, face - 3, oz)
    for x in range(face - 3, end + 1):
        for z in range(oz - 2, oz + 3):
            D.cell(x, z, deck, "deck")
    for r in L.routes:
        if r["name"] != FOOTBRIDGE_ROUTE:
            continue
        on = (shapes.polyline(Xf, Zf, r["line"])[0] <= r["width"] / 2) & (L.water > 0)
        s_of = shapes.polyline(Xf, Zf, r["line"])[1]
        for i, k in np.argwhere(on):
            D.cell(int(L.X[i, k]), int(L.Z[i, k]), int(round(np.interp(s_of[i, k], *r["profile"]))), "deck")
    return R


def shapes_boundary(cells):
    """The cells of a set with a four-neighbour outside it: a building's walls."""
    cells = set(cells)
    return {(x, z) for x, z in cells if any((x + a, z + b) not in cells for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def links():
    """The ladders the raster cannot see, as plan graph edges: the gaol's floor to its cellar, the headframe's
    collar to the gallery under it. Each both ways, and mirrored for blue."""
    hs = houses()
    gx, gz = GAOL_LADDER
    sx, sz = SHAFT
    out = []
    for (a, b, cost, tag) in [((gx, gz), (gx, gz, 1), hs["gaol"]["floor"] - CELLAR[1], "gaol ladder"),
                              ((sx, sz), (sx, sz, 1), 12, "shaft ladder")]:
        for p, q in ((a, b), (SYM.point(*a[:2]) + tuple(a[2:]), SYM.point(*b[:2]) + tuple(b[2:]))):
            out += [(p, q, cost, tag), (q, p, cost, tag)]
    return out


def objectives():
    """The teams of sixteen, red's spawn and its two monuments (blue's are their mirror images), and the
    observers' point over the rift. Read by map.xml, the sketch and the read-back alike."""
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN, yaw=270, kit="spawn-kit", area=SPAWN_AREA))
    for key, ((x, z), g, name) in MONUMENTS.items():
        O.add(Destroyable(f"red-{key}", name, "red-team", Box(x, g + 4, z, x, g + 5, z)))
    O.add(Observer((0, 80, 0), yaw=90), mirror=False)
    return O
