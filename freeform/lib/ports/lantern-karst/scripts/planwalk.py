"""The plan walk of a capture board: pgmvox.plangraph's graph, with two things a CTW board needs that it lacks.

    diagonal steps   plangraph walks four ways, so its distances are Manhattan; the original's checker walked
                     octile, and its targets (SP10, WL9, WL10e) were set against octile numbers. A diagonal
                     step is added where both cells it cuts past are walkable and the rise is at most one.
    bridges          a build zone is void a player may build over, at any height: every zone cell is joined to
                     its eight neighbours that are zone or walkable floor, cost 1 or 1.41, tagged "bridge". The
                     Store's bedrock wall is crossed the same way, tagged "over the wall".

    E = graph(R, bridge_keys=("pit", "w-steps", "e-steps"))
    D, prev = plangraph.dijkstra(E, starts)
    cost, bridged, cells = reach(D, prev, E, targets)
"""
import math

import plan  # noqa: F401  (puts the library on the path)

import numpy as np

from pgmvox import plangraph as G
from plan import WALK, zone_mask

DIAG = math.sqrt(2)


def graph(R, bridge_keys=("pit", "w-steps", "e-steps"), barrier=True, leave_out=()):
    """The walk graph with diagonals and bridges. leave_out: piece keys not walked (the Ledges, reached by a
    fall and not a walk)."""
    walk_kinds = WALK - set(leave_out)
    E = G.graph(R, walk_kinds, wall_kinds=("storewall",), rules=G.PlanRules(jumps=False))
    walk = R.mask(*walk_kinds)
    extra = []
    for i, k in np.argwhere(walk):                                  # diagonal steps
        for di, dk in ((1, 1), (1, -1)):
            a, b = i + di, k + dk
            if not (0 <= a < R.nx and 0 <= b < R.nz) or not walk[a, b]:
                continue
            if not (walk[i + di, k] and walk[i, k + dk]):
                continue
            hs = [R.H[i, k], R.H[a, b], R.H[i + di, k], R.H[i, k + dk]]
            if max(hs) - min(hs) > 1:
                continue
            p, q = (int(R.X[i, k]), int(R.Z[i, k])), (int(R.X[a, b]), int(R.Z[a, b]))
            extra += [(p, q, DIAG, "walk"), (q, p, DIAG, "walk")]
    cross = zone_mask(R, bridge_keys) if bridge_keys else np.zeros(R.H.shape, bool)
    over = R.mask("barrier") if barrier else np.zeros(R.H.shape, bool)
    for m, tag in ((cross, "bridge"), (over, "over the wall")):
        for i, k in np.argwhere(m):
            p = (int(R.X[i, k]), int(R.Z[i, k]))
            for di in (-1, 0, 1):
                for dk in (-1, 0, 1):
                    a, b = i + di, k + dk
                    if (di, dk) == (0, 0) or not (0 <= a < R.nx and 0 <= b < R.nz):
                        continue
                    if not (m[a, b] or walk[a, b]):
                        continue
                    if di and dk and not ((m[i + di, k] or walk[i + di, k]) and (m[i, k + dk] or walk[i, k + dk])):
                        continue
                    q = (int(R.X[a, b]), int(R.Z[a, b]))
                    c = DIAG if di and dk else 1.0
                    extra.append((q, p, c, tag))                 # onto the zone cell
                    if not m[a, b]:
                        extra.append((p, q, c, tag))             # and off it onto the floor
    for a, b, c, tag in extra:
        E.setdefault(a, []).append((b, c, tag))
    return E


def reach(D, prev, E, cells):
    """The cheapest of a set of target cells: (cost, blocks bridged on the way, the path's cells), or
    (None, 0, []). plangraph.route returns the tags of the moves but not how much of the way each move was."""
    got = [c for c in cells if c in D]
    if not got:
        return None, 0.0, []
    c = min(got, key=D.get)
    path = G.path(prev, c)
    bridged = 0.0
    for u, v in zip(path, path[1:]):
        tag = prev[v][1]
        if tag in ("bridge", "over the wall"):
            bridged += next(cost for w, cost, t in E[u] if w == v and t == tag)
    return D[c], bridged, path


def cells_of(R, *kinds, half=None):
    """The (x, z) cells of some kinds, on red's half (half="red"), blue's, or both."""
    m = R.mask(*kinds)
    out = [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(m)]
    if half == "red":
        out = [c for c in out if c[1] < 0]
    elif half == "blue":
        out = [c for c in out if c[1] >= 0]
    return out
