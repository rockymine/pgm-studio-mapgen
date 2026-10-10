"""Abbeymoor's ground: heights over the whole board, symmetric under the half turn (x, z) -> (-1 - x, -1 - z), so red's
half is drawn and blue's is its image. Every landform takes this board's numbers; the places that follow are in plan.py.

    a high moor, rolling, held at about 66 over a ragged outline (void beyond it)
    the ridge behind each spawn, rising 12 toward the board's end
    the abbey hill: a plateau at 80 and slopes of about 38 degrees down to the moor
    the orchard village's valley, levelled to 66; Hall Farm's hollow behind each spawn
    the peat bog across the middle: a basin 4 under the moor, seven pools held at level 61 with banks
    a beck from the east moor into the bog, in reaches and falls
"""
import numpy as np

from pgmvox import landform as L, noise
from pgmvox.noise import smoothstep

X0, Z0 = -100, -132
NX, NZ = 200, 264
MOOR = 66
PLATEAU = 80
BOG_LEVEL = 61
HILL = (-42, -72)                       # the abbey hill's centre, red's; blue's is its image
HILL_PLATEAU_R, HILL_BASE_R = 14, 34
VILLAGE = (30, -70)
FARM = (0, -118)
BECK = [(72, -108), (70, -90), (66, -70), (60, -50), (50, -32)]
FLANK = (-68, -17)                      # the flank hamlet's centre, red's; its image stands on the other side of the bog
TARNS = [(-58, -30, 4), (-84, -8, 3), (-6, -48, 3)]          # small tarns on the moor, red's: x, z, radius (held at MOOR - 2)
POOLS = [(-22, -14, 6, 5), (12, -17, 7, 5), (-34, -9, 5, 4), (24, -9, 5, 4), (-8, -9, 4, 3)]   # red's: x, z, rx, rz
BECK_POOL = (46, -26, 6)


def grid():
    return np.meshgrid(np.arange(X0, X0 + NX), np.arange(Z0, Z0 + NZ), indexing="ij")


def sym(f):
    """A term drawn for red and carried to blue by the half turn."""
    def g(X, Z):
        return f(X, Z) + f(-1 - X, -1 - Z)
    return g


def symnoise(shape, cell, octaves, seed):
    a = noise.fbm(shape, cell, octaves, seed=seed)
    return (a + a[::-1, ::-1]) / 2


def bog_field(X, Z):
    """How far in from the bog's outline a column is (below 1: inside). An ellipse about the middle with its edge pushed in and out by
    noise, and a fen channel running east and west through the middle that wanders about the axis; both are carried to the half turn
    by building from half-turn-symmetric noise and an odd centreline."""
    xc, zc = X + 0.5, Z + 0.5
    warp = symnoise(X.shape, 22, 3, 71)
    main = np.hypot(xc / 50, zc / 29) * (1 + 0.26 * warp) + 0.10 * symnoise(X.shape, 7, 2, 72)
    centre = 7 * np.sin(xc / 17.0)
    lobe = np.hypot(xc / 88, (zc - centre) / 7.5) * (1 + 0.2 * symnoise(X.shape, 9, 2, 73))
    return main, lobe


def land_mask(X, Z):
    n = symnoise(X.shape, 14, 3, 91)
    ex = (np.abs(X + 0.5) - 90) + 4 * n
    ez = (np.abs(Z + 0.5) - 127) + 4 * n
    return (ex < 0) & (ez < 0)


def hill_term(X, Z):
    d = np.hypot(X - HILL[0], Z - HILL[1])
    t = 1 - smoothstep(HILL_PLATEAU_R, HILL_BASE_R, d)
    return (PLATEAU - MOOR) * t


def ridge_term(X, Z):
    return 12 * smoothstep(-124, -131, Z) * (0.7 + 0.5 * noise.fbm(X.shape, 18, 2, seed=5))


def ground():
    """(X, Z, H, land, waters, extras): heights as ints (0 outside the land), the waters laid, and what plan.py reads."""
    X, Z = grid()
    land = land_mask(X, Z)
    n1 = symnoise(X.shape, 30, 3, 3)
    n2 = symnoise(X.shape, 9, 2, 4)
    H = MOOR + 2.4 * n1 + 1.1 * n2
    H = H + sym(hill_term)(X, Z) + sym(ridge_term)(X, Z)
    # the plateau is flat: Abbey Hill's top at 80 exactly, with a ragged edge
    edge = 1.2 * noise.fbm(X.shape, 6, 2, seed=8)
    for cx, cz in (HILL, (-1 - HILL[0], -1 - HILL[1])):
        d = np.hypot(X - cx, Z - cz) + edge
        H = np.where(d <= HILL_PLATEAU_R, PLATEAU, H)
    # the valley and the farm: levelled with a blend, so a house stands on flat ground
    for (cx, cz), r, rr, level in ((VILLAGE, 30, 20, MOOR), (FARM, 42, 28, MOOR + 2), (FLANK, 17, 11, MOOR)):
        for sx, sz in ((cx, cz), (-1 - cx, -1 - cz)):
            d = np.hypot((X - sx) / 1.0, (Z - sz) / 0.8)
            t = 1 - smoothstep(rr, r, d)
            if (cx, cz) == FARM or (-1 - cx, -1 - cz) == (cx, cz):
                t = t * (smoothstep(-126, -121, Z) if sz < 0 else smoothstep(124, 119, Z))
            H = H * (1 - t) + (level + 0.6 * n2) * t
    # the bog: a basin across the middle
    main, lobe = bog_field(X, Z)
    dig = np.maximum(4.5 * (1 - smoothstep(0.5, 1.0, main)), 3.0 * (1 - smoothstep(0.45, 1.0, lobe)))
    H = H - dig * (1 + 0.3 * n2)
    H = np.where(land, H, 0)
    waters = []
    for (px, pz, rx, rz) in POOLS:
        H, wat = L.lake(H, X, Z, (px, pz), rx, BOG_LEVEL, depth=3, shore=3, rz=rz, jag=0.25, seed=int(abs(px) + abs(pz)))
        waters.append(wat)
    H, wat = L.lake(H, X, Z, BECK_POOL[:2], BECK_POOL[2], BOG_LEVEL, depth=3, shore=3, jag=0.2, seed=7)
    waters.append(wat)
    for k, (tx, tz, tr) in enumerate(TARNS):
        H, tarn = L.lake(H, X, Z, (tx, tz), tr, MOOR - 3, depth=2, shore=3, jag=0.3, seed=20 + k)
        waters.append(tarn)
    H, beck = L.watercourse(H, X, Z, BECK, width=3, depth=2, bank=3, fall_min=2, reach_min=10, lowest=BOG_LEVEL - 1, into=wat)
    waters.append(beck)
    H = L.hold(H, *waters)
    red = Z < 0                                                  # red's half is drawn; blue's is its image under the half turn
    H = np.where(red, H, H[::-1, ::-1])
    waters = [L.Water(np.where(red, w_.mask, w_.mask[::-1, ::-1]), np.where(red, w_.surface, w_.surface[::-1, ::-1]), w_.falls or [])
              for w_ in waters]
    H = np.where(land, np.round(H), 0).astype(int)
    wet = np.zeros(H.shape, bool)
    for wat in waters:
        wet |= wat.mask
    return X, Z, H, land, waters, wet
