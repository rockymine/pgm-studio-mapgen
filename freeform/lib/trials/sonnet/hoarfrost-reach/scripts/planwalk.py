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



def graph(R, bridge_keys=("pit", "w-steps", "e-steps"), barrier=True, leave_out=()):
    """The walk graph with diagonals and bridges, both now the library's (PlanRules.diagonals, graph(bridge=)).
    leave_out: piece keys not walked (the Ledges, reached by a fall and not a walk)."""
    walk_kinds = WALK - set(leave_out)
    cross = zone_mask(R, bridge_keys) if bridge_keys else np.zeros(R.H.shape, bool)
    if barrier:
        cross = cross | R.mask("barrier")
    return G.graph(R, walk_kinds, wall_kinds=("storewall",), rules=G.PlanRules(jumps=False, diagonals=True),
                   bridge=cross)


def reach(D, prev, E, cells):
    """The cheapest of a set of target cells: (cost, blocks bridged on the way, the path's cells), or
    (None, 0, []): the library's plangraph.measure, read for its bridged part."""
    cost, by, path = G.measure(D, prev, E, cells)
    if not path:
        return None, 0.0, []
    return cost, by.get("bridge", 0.0), path


def cells_of(R, *kinds, half=None):
    """The (x, z) cells of some kinds, on red's half (half="red"), blue's, or both."""
    m = R.mask(*kinds)
    out = [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(m)]
    if half == "red":
        out = [c for c in out if c[1] < 0]
    elif half == "blue":
        out = [c for c in out if c[1] >= 0]
    return out
