"""Overgrowth: a team-deathmatch board in a walled jungle valley. A four-tier ziggurat stands in the middle with a
tunnel through its heart and a chamber on top; two gorges with a shallow stream cut the valley's north and south, with
rope bridges across, and beyond them a jungle terrace a team can run the length of; four watchtowers stand on the
terraces. Each team spawns in a walled court at its end of the valley, with three gates.

Red holds the west (x < 0). Blue is red's mirror across the ziggurat, x' = -1 - x: pgmvox's Symmetry("mirror_x").
H is the y of the floor block; a player stands at H + 1.

    land()        the heightfield (the valley, the gorges, the terraces, the rim), red drawn and mirrored
    build()       the plan Raster: ground storey, and storey 1 for the tunnel and the tower platforms
    cover()       the ruined walls, crates and statues, placed and measured
    objectives()  teams, spawns and the observer
"""
import math
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.noise import fbm, smoothstep  # noqa: E402
from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.terrain import slope_deg  # noqa: E402

BOARD = "overgrowth"
X_MIN, X_MAX = -64, 63
Z_MIN, Z_MAX = -48, 47
SYM = Symmetry("mirror_x")
VALLEY = 60
STRIP = 64
STREAM_Y = 55                                  # the stream bed's floor block; water to 56
KILL_Y = 20
MAX_BUILD = 110

SPAWN_AT = (-56, 67, 0)
SPAWN_AREA = Box(-63, 0, -10, -48, 127, 9)
COURT = (-62, -9, -49, 8)                      # the court's walls included
COURT_Y = 66
GATES = [("e", -49, -2, -49, 2), ("n", -57, -9, -53, -9), ("s", -57, 8, -53, 8)]       # (side, x0, z0, x1, z1) of the gap

TIERS = [("tier1", (-20, -18, 19, 17), 61), ("tier2", (-16, -14, 15, 13), 65), ("tier3", (-12, -10, 11, 9), 69),
         ("tier4", (-8, -6, 7, 5), 73)]
CHAMBER = (-6, -4, 5, 3)                       # the chamber's walls on the top tier
CHAMBER_DOORS = [(-6, -1, -6, 0), (5, -1, 5, 0), (-1, -4, 0, -4), (-1, 3, 0, 3)]
TUNNELS = [(-16, -10, 15, -6), (-16, 5, 15, 9), (-2, -10, 1, 9)]      # the passages through the mass at floor 61: an H
HEART = (0, 0)                                  # the ladder from the H's crossing up into the chamber (its image at -1)
TOWERS = [(-36, -43, -32, -39), (-36, 38, -32, 42)]       # red's: x0, z0, x1, z1 (five square), N and S terraces
TOWER_Y = STRIP
TOWER_TOP = 78                                  # the platform's floor block
BRIDGES_X = (-44, -12)                          # red's bridge centres; blue's are the mirror
BRIDGE_W = 3

KINDS = ["void", "valley", "bank", "ford", "strip", "court", "wall", "gate", "tier1", "tier2", "tier3", "tier4",
         "stair", "tunnel", "chamber", "door", "tower", "platform", "cover", "bridge", "rim", "ladder"]
COLOURS = {"void": (20, 24, 20), "valley": (96, 150, 72), "bank": (126, 150, 96), "ford": (70, 140, 200),
           "strip": (70, 120, 70), "court": (190, 190, 170), "wall": (100, 110, 90), "gate": (200, 190, 150),
           "tier1": (170, 180, 150), "tier2": (156, 170, 140), "tier3": (142, 160, 130), "tier4": (210, 190, 120),
           "stair": (190, 190, 180), "tunnel": (90, 100, 90), "chamber": (230, 200, 120), "door": (230, 210, 150),
           "tower": (90, 100, 90), "platform": (160, 120, 80), "cover": (120, 130, 100), "bridge": (160, 120, 80),
           "rim": (60, 90, 60), "ladder": (200, 160, 80)}
WALK = {"valley", "bank", "ford", "strip", "court", "gate", "tier1", "tier2", "tier3", "tier4", "stair", "tunnel",
        "chamber", "door", "platform", "bridge", "ladder"}

PLACES = [("Jaguar Court", (-56, 0)), ("the Ziggurat", (0, 0)), ("the Processional Passage", (-8, 0)),
          ("the Sun Chamber", (0, 0)), ("North Gorge", (-24, -32)), ("South Gorge", (-24, 31)),
          ("North Terrace", (-24, -42)), ("South Terrace", (-24, 41)), ("Heron Tower", (-34, -41)),
          ("Jackal Tower", (-34, 40)), ("North Bridges", (-44, -32)), ("South Bridges", (-12, 31)),
          ("the Valley", (-36, 0))]

# ---- cover (red's half): small crates 2 x 2 x 2, ruined walls (long, 3 high), statues (1 x 1 x 5) ------------
COVER = [
    dict(kind="crate", rect=(-44, -14, -43, -13), h=2), dict(kind="crate", rect=(-44, 13, -43, 14), h=2),
    dict(kind="crate", rect=(-30, -5, -29, -4), h=2), dict(kind="crate", rect=(-30, 4, -29, 5), h=2),
    dict(kind="crate", rect=(-24, -22, -23, -21), h=2), dict(kind="crate", rect=(-24, 21, -23, 22), h=2),
    dict(kind="wall", rect=(-40, -12, -33, -12), h=3), dict(kind="wall", rect=(-40, 11, -33, 11), h=3),
    dict(kind="wall", rect=(-37, -3, -37, 3), h=3), dict(kind="wall", rect=(-27, -16, -27, -10), h=3),
    dict(kind="wall", rect=(-27, 9, -27, 15), h=3),
    dict(kind="statue", rect=(-23, -8, -23, -8), h=5), dict(kind="statue", rect=(-23, 7, -23, 7), h=5),
    dict(kind="statue", rect=(-46, -4, -46, -4), h=5), dict(kind="statue", rect=(-46, 3, -46, 3), h=5),
    dict(kind="wall", rect=(-56, -44, -48, -44), h=3), dict(kind="wall", rect=(-56, 43, -48, 43), h=3),
    dict(kind="crate", rect=(-28, -42, -27, -41), h=2), dict(kind="crate", rect=(-28, 41, -27, 42), h=2),
    dict(kind="wall", rect=(-20, -41, -14, -41), h=3), dict(kind="wall", rect=(-20, 40, -14, 40), h=3),
    # baffles inside the court: nobody on the outside sees the floor through a gate
    dict(kind="baffle", rect=(-52, -6, -51, 5), h=5), dict(kind="baffle", rect=(-59, -6, -52, -6), h=5),
    dict(kind="baffle", rect=(-59, 6, -52, 6), h=5),
]
# a colonnade of ruined pillars across the valley and more crates on the terraces: red's, the image is the mirror
for _x in (-47, -39, -31, -23):
    for _z in (-19, -11, -3, 5, 13, 20):
        if abs(_z + 0.5) <= 4 and _x < -40:
            continue
        COVER.append(dict(kind="pillar", rect=(_x, _z, _x, _z), h=4))
for _x in (-60, -50, -40, -22, -12):
    for _z in (-45, 44):
        COVER.append(dict(kind="crate", rect=(_x, _z, _x + 1, _z + 1), h=2))



def sym(a):
    return 0.5 * (a + a[::-1, :])


def mir(a):
    return a[::-1, :]


def profile(dz):
    """The valley's height by distance from the long axis (z = -0.5): the valley, the bank, the stream's bed, the
    terrace's wall and the terrace. dz is |z + 0.5|."""
    return np.interp(dz, [0, 23.5, 26.5, 29.5, 30.5, 32.5, 33.5, 35.5, 37.5, 43.5, 47.5],
                     [VALLEY, VALLEY, 59, 57, STREAM_Y, STREAM_Y, 57, 62, STRIP, STRIP, STRIP + 2])


@lru_cache(maxsize=1)
def land():
    L = type("Land", (), {})()
    xs, zs = np.arange(X_MIN, X_MAX + 1), np.arange(Z_MIN, Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Xf, Zf = X.astype(float), Z.astype(float)
    sh = X.shape
    n1, n2 = sym(fbm(sh, 10, 3, seed=11)), sym(fbm(sh, 30, 3, seed=12))
    dz = np.abs(Zf + 0.5)
    h = profile(dz) + np.where(dz < 23.5, 0.7 * n1, 0) + np.where(dz > 37.5, 0.9 * n1 + 0.6 * n2, 0)
    # the ziggurat's tiers, the spawn courts
    for _, (x0, z0, x1, z1), y in TIERS:
        m = (Xf >= x0) & (Xf <= x1) & (Zf >= z0) & (Zf <= z1)
        h = np.where(m, y, h)
    cx0, cz0, cx1, cz1 = COURT
    court = (Xf >= cx0) & (Xf <= cx1) & (Zf >= cz0) & (Zf <= cz1)
    h = np.where(court, COURT_Y, h)
    # the rim: the board's edge rises to a wall of hill
    e = np.maximum(np.abs(Xf + 0.5) / 64.0, np.abs(Zf + 0.5) / 48.0)
    h = h + 10 * smoothstep(0.93, 1.0, e)
    H = np.round(h).astype(int)
    H = np.where(Xf < 0, H, mir(H))
    water = (H <= STREAM_Y + 1) & (dz > 28) & (dz < 34)
    L.X, L.Z, L.H, L.Xf, L.Zf = X, Z, H, Xf, Zf
    L.water = water
    L.slope = slope_deg(H)
    L.court = np.where(Xf < 0, court, mir(court))
    L.dz = dz
    return L


def at(L, x, z):
    return int(L.H[x - X_MIN, z - Z_MIN])


def _rect(R, K, H, box, h, kind, both=True):
    x0, z0, x1, z1 = box
    R.rect(x0, x1, z0, z1, h, kind, both)


@lru_cache(maxsize=1)
def build():
    L = land()
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    k_ = R.kinds
    K = np.full(L.H.shape, k_["valley"])
    K[L.dz > 23.5] = k_["bank"]
    K[(L.dz > 35.5)] = k_["strip"]
    K[L.water] = k_["ford"]
    edge = (L.X <= X_MIN + 1) | (L.X >= X_MAX - 1) | (L.Z <= Z_MIN + 1) | (L.Z >= Z_MAX - 1)
    K[edge] = k_["rim"]
    R.H[:] = L.H
    R.K[:] = K
    # the tiers (both halves: the ziggurat is its own image)
    for key, box, y in TIERS:
        _rect(R, K, L.H, box, y, key)
    # the court: floor, walls with three gates a side
    cx0, cz0, cx1, cz1 = COURT
    for x in range(cx0, cx1 + 1):
        for z in range(cz0, cz1 + 1):
            ring = x in (cx0, cx1) or z in (cz0, cz1)
            R.cell(x, z, COURT_Y, "wall" if ring else "court")
    for side, x0, z0, x1, z1 in GATES:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                R.cell(x, z, COURT_Y, "gate")
    # the flights: down from the court's three gates to the valley, up the ziggurat's tiers
    R.flight((-43, 0), "w", width=(-2, 2), h0=61, n=6)
    R.flight((-55, -15), "s", width=(-2, 2), h0=61, n=6)
    R.flight((-55, 14), "n", width=(-2, 2), h0=61, n=6)
    for (_, (x0, z0, x1, z1), y) in TIERS[:3]:
        h0 = y + 1
        ledge = 4
        R.flight((x0, 0), "e", width=(-2, 2), h0=h0, n=ledge)
        R.flight((-6, z0), "s", width=(-1, 1), h0=h0, n=ledge)
        R.flight((-6, z1), "n", width=(-1, 1), h0=h0, n=ledge)
    # the chamber's walls and doors on the top tier
    x0, z0, x1, z1 = CHAMBER
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            R.cell(x, z, 73, "wall" if ring else "chamber")
    for bx0, bz0, bx1, bz1 in CHAMBER_DOORS:
        for x in range(bx0, bx1 + 1):
            for z in range(bz0, bz1 + 1):
                R.cell(x, z, 73, "door")
    # the cover
    for c in COVER:
        x0, z0, x1, z1 = c["rect"]
        R.rect(x0, x1, z0, z1, R.h(x0, z0) + c["h"], "cover")
    # the towers: a footprint of wall, a ladder cell inside, a platform on storey 1
    U = R.storey(1)
    for (x0, z0, x1, z1) in TOWERS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                ring = x in (x0, x1) or z in (z0, z1)
                R.cell(x, z, TOWER_Y, "tower" if ring else "ladder")
        U.rect(x0, x1, z0, z1, TOWER_TOP, "platform")
    # the rope bridges over each gorge
    for bx in BRIDGES_X:
        for sgn in (-1, 1):
            for z in range(26, 38):
                zz = sgn * z if sgn > 0 else sgn * z - 1
                y = 60 if z <= 27 else 61 if z <= 33 else {34: 62, 35: 63}.get(z, 64)
                for dx in range(-(BRIDGE_W // 2), BRIDGE_W // 2 + 1):
                    R.cell(bx + dx, zz, y, "bridge")
    # the tunnel through the mass, floor 61, on storey 1 (under the tiers)
    for tx0, tz0, tx1, tz1 in TUNNELS:
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                U.cell(x, z, 61, "tunnel", both=False)
    R.cell(HEART[0], HEART[1], 73, "ladder")
    return R


def tower_ladder(box):
    x0, z0, x1, z1 = box
    return ((x0 + x1) // 2, z1 - 1)


def links():
    """The towers' ladders from their foot to their platform, both ways, both halves."""
    out = []
    hp = HEART
    for p in (hp, tuple(int(v) for v in SYM.point(*hp))):
        out += [(p, p + (1,), 12, "heart ladder"), (p + (1,), p, 12, "heart ladder")]
    for box in TOWERS:
        a = tower_ladder(box)
        for p in (a, tuple(int(v) for v in SYM.point(*a))):
            out += [(p, p + (1,), TOWER_TOP - TOWER_Y, "ladder"), (p + (1,), p, TOWER_TOP - TOWER_Y, "ladder")]
    return out


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=270, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Observer((0, 100, 0), yaw=90), mirror=False)
    return O
