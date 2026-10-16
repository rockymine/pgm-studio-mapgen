"""Rimefire's plan as a raster: the shaped ground, the bridge decks at the level, the lava channel as water, and the
walk graph over it."""
import numpy as np

import land as LND
from pgmvox.plan import graph as G
from pgmvox.plan.raster import Raster, Symmetry
from pgmvox.surface import terrain as T

KINDS = ["ground", "steep", "lava", "ice", "bridge"]
COLOURS = {"ground": (150, 140, 100), "steep": (110, 100, 90), "lava": (230, 90, 30), "ice": (170, 210, 235),
           "bridge": (120, 80, 50)}
WALK = {"ground", "ice", "bridge"}


def build():
    g = LND.ground()
    H, X, Z, land = g["H"].copy(), g["X"], g["Z"], g["land"]
    R = Raster((int(X[0, 0]), int(X[-1, 0])), (int(Z[0, 0]), int(Z[0, -1])), KINDS, 0, "ground", Symmetry("half"))
    R.H[:] = H
    deg = T.slope_deg(H, land)
    R.K[(deg > 46) & land] = R.kinds["steep"]
    d, hw, south = g["d"], g["hw"], g["south"]
    floor = g["seam"] & (d < hw - 0.4) & land
    chan = floor & (d > 3.3) & (d < 5.7)
    for name, pts in g["ramps"]:
        for x in range(int(pts[0][0]) - 6, int(pts[0][0]) + 7):
            chan[x - LND.X0, :] &= ~(np.abs(d[x - LND.X0, :]) < 99) if False else True
    from seam import ford_near
    for i, k in np.argwhere(chan):
        x = int(X[i, k])
        side = "south" if south[i, k] else "north"
        if ford_near(x, side, g):
            continue
        R.K[i, k] = R.kinds["ice" if south[i, k] else "lava"]
    for cx, hwid in LND.BRIDGES.values():
        for sgn_x in range(int(np.floor(cx - hwid / 2 + 0.5)), int(np.floor(cx - hwid / 2 + 0.5)) + (6 if cx == -0.5 else 4)):
            c = float(LND.centre(cx))
            for z in range(int(round(c)) - 15, int(round(c)) + 16):
                i, k = sgn_x - LND.X0, z - LND.Z0
                if abs(z - c) <= 11 or H[i, k] < LND.LEVEL:
                    R.H[i, k] = LND.LEVEL
                    R.K[i, k] = R.kinds["bridge"]
    return R, g


def graph(R):
    return G.graph(R, WALK, rules=G.PlanRules(jumps=False, max_drop=3))
