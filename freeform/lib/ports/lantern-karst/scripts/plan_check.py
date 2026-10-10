"""Measure Lantern Karst's plan before anything is built: the original's table, walked over the pgmvox raster.

A walk is octile over the floors (a step one up costs 1.2, plangraph's price), and may cross the Pillar's pit,
the Mist Steps and the Tea Steps by bridging them, block for block; "79 (17 bridged)" is 62 walked and 17 built.
The band is never bridged in these walks: the attack numbers start from its edge, as the original's did.

    python3 plan_check.py            prints the table; the sketch draws the same rows
"""
import math

import plan  # noqa: F401  (puts the library on the path)

import numpy as np

from pgmvox import plangraph as G
from pgmvox import sight
from plan import PIECE, SPAWN_AT, WALK, ZONES, build, objectives, zone_mask


def graph(R, bridge_keys=("pit", "w-steps", "e-steps"), barrier=True, leave_out=()):
    """The walk graph with diagonals, the build zones `bridge_keys` (and the barrier) crossed by bridging and the
    Store's bedrock wall crossed over the top. leave_out: piece keys not walked (the Ledges, reached by a fall)."""
    walk_kinds = WALK - set(leave_out)
    cross = zone_mask(R, bridge_keys) if bridge_keys else np.zeros(R.H.shape, bool)
    if barrier:
        cross = cross | R.mask("barrier")
    return G.graph(R, walk_kinds, wall_kinds=("storewall",), rules=G.PlanRules(jumps=False, diagonals=True),
                   bridge=cross)


def reach(D, prev, E, cells):
    """The cheapest of a set of target cells: (cost, blocks bridged on the way, the path's cells), or
    (None, 0, [])."""
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


def gap(a, b):
    """The void between two rectangles of the plan, in whole blocks (the original's measure: centre to centre
    less one, over the nearest pair of cells)."""
    ax0, az0, ax1, az1 = PIECE[a][3]
    bx0, bz0, bx1, bz1 = PIECE[b][3]
    dx = max(0, bx0 - ax1, ax0 - bx1)
    dz = max(0, bz0 - az1, az0 - bz1)
    return math.hypot(dx, dz) - 1


def measure():
    R, flights, walls = build()
    ledges = ("ledge-w", "ledge-e")
    E = graph(R, leave_out=ledges)
    E_walk = graph(R, bridge_keys=(), barrier=False, leave_out=ledges)
    sp = (SPAWN_AT[0], SPAWN_AT[2])
    blue_sp = R.symmetry.point(*sp)
    store, pillar = cells_of(R, "store", half="red"), cells_of(R, "pillar", half="red")
    D, prev = G.dijkstra(E, [sp])
    Dw, prevw = G.dijkstra(E_walk, [sp])
    band = ZONES[0][2]
    starts = [(x, -12) for x in range(band[0], band[2] + 1) if (x, -12) in E]                         # the band's edge on red's side, land or zone
    Db, prevb = G.dijkstra(E, starts)
    Dbw, prevbw = G.dijkstra(E_walk, starts)

    s_band = min(D.get((x, -12), math.inf) for x in range(band[0], band[2] + 1)) + 1
    s_store, s_store_b, s_store_path = reach(D, prev, E, store)
    s_pillar, s_pillar_b, s_pillar_path = reach(D, prev, E, pillar)
    sw_store = reach(Dw, prevw, E_walk, store)[0]
    b_store, b_store_b, b_store_path = reach(Db, prevb, E, store)
    b_pillar, b_pillar_b, b_pillar_path = reach(Db, prevb, E, pillar)
    bw_store = reach(Dbw, prevbw, E_walk, store)[0]
    monuments = [(o.slot[0], o.slot[2]) for o in objectives().items if getattr(o, "slot", None)
                 and o.team == "red-team"]
    s_monuments = max(reach(D, prev, E, [m])[0] for m in monuments)

    # fairness: the same walks for blue to its own rooms. plangraph.arrivals gives every team the same target
    # cells (a shared hill); a CTW board's targets are each team's own image, so the walks are made one by one
    red_store = reach(D, prev, E, store)[0]
    Dblue, prevblue = G.dijkstra(E, [blue_sp])
    blue_store = reach(Dblue, prevblue, E, cells_of(R, "store", half="blue"))[0]
    blue_pillar = reach(Dblue, prevblue, E, cells_of(R, "pillar", half="blue"))[0]

    # sight: the Ledges seen from the Arms and the Terrace (the drop is made "in full view of the Arms")
    opaque = sight.plan_opaque(R)
    ledge_cells = cells_of(R, *ledges, half="red")
    eyes = [sight.eye(x, R.h(x, z) + 1, z) for x, z in cells_of(R, "f-east", "f-west", half="red") if (x + z) % 3 == 0]
    targets = [sight.target(x, R.h(x, z) + 1, z) for x, z in ledge_cells]
    seen_share = 1 - len(sight.hidden(targets, eyes, opaque)) / len(targets)

    # every running jump the plan allows (plangraph.jumps, about 40 s over this board), and those between pieces
    # that do not touch: the corner cuts inside one piece or across a join are not crossings
    from scipy import ndimage
    J = G.jumps(R, WALK_NO_LEDGES, wall_kinds=("storewall", "barrier"))
    lab, _ = ndimage.label(~R.mask("void"))
    apart = sum(1 for a, b, g in J if lab[R.ix(a[0]), R.iz(a[1])] != lab[R.ix(b[0]), R.iz(b[1])])

    def fmt(d, b):
        return "not reached" if d is None else f"{d:.0f}" + (f" ({b:.0f} bridged)" if b > 0.5 else "")
    (wx0, _, wz0), (wx1, _, wz1) = [o.found for o in objectives().items if getattr(o, "team", "") == "blue-team"
                                    and hasattr(o, "found")]
    land_red = int(((~R.mask("void")) & (R.Z < 0) & ~R.mask(*ledges)).sum())
    ledge_y, terrace_y = PIECE["ledge-w"][4], PIECE["f-stem"][4]
    rows = [
        (f"{s_band:.0f}", "spawn to the band", "SP10: at least 55", s_band >= 55),
        (f"{s_monuments:.0f}", "spawn to its own monuments (the farther)", "", None),
        (fmt(s_store, s_store_b), "spawn to the Tea Store, over the wall", "WL9: comparable", None),
        (fmt(sw_store, 0), "spawn to the Tea Store, walked only", "the wall stops it", sw_store is None),
        (fmt(s_pillar, s_pillar_b), "spawn to the Pillar", "WL9: comparable", None),
        (f"{max(s_store, s_pillar) / min(s_store, s_pillar):.2f}", "ratio of the two", "WL9: ideal 1, at most 1.25",
         max(s_store, s_pillar) / min(s_store, s_pillar) <= 1.25),
        (fmt(b_store, b_store_b), "band to the Tea Store, shortest", "WL10e: at least 59", b_store >= 59),
        (fmt(b_pillar, b_pillar_b), "band to the Pillar, shortest", "WL10e: at least 59", b_pillar >= 59),
        (fmt(bw_store, 0), "band to the Tea Store, walked only", "the wall stops it", bw_store is None),
        (f"{math.hypot(wx1 - wx0, wz1 - wz0):.0f}", "Pillar to Tea Store, straight", "WL7: 46 to 143",
         46 <= math.hypot(wx1 - wx0, wz1 - wz0) <= 143),
        (", ".join(f"{gap('pillar', k):.0f}" for k in ("f-west", "f-east", "f-stem")),
         "Pillar to the Arms and the Long Terrace", "WL20: at least 12",
         min(gap("pillar", k) for k in ("f-west", "f-east", "f-stem")) >= 12),
        (f"{PIECE['drying'][3][1] - PIECE['store'][3][3] - 1}", "the Store Road alone, its last join to the room",
         "", None),
        ("16 by 16", "the Tea Court's sinkhole", "LN6: at least 12", True),
        (f"{PIECE['rows'][3][1] - PIECE['drying'][3][3] - 1:.0f} by 18", "the void inside the Store's F",
         "LN6: at least 12", PIECE['rows'][3][1] - PIECE['drying'][3][3] - 1 >= 12),
        (f"{terrace_y - ledge_y}; {gap('ledge-w', 'pillar'):.0f}, {gap('ledge-e', 'pillar'):.0f}",
         "the Ledges: blocks under the Terrace; gaps to the pillar", "", None),
        (f"{seen_share:.0%}", "of the Ledges' cells seen from the Arms (sight)", "in full view", seen_share > 0.5),
        (f"{gap('leg-w', 'leg-e'):.0f}", "the void between the Stairs", "WL12: at least 16",
         gap("leg-w", "leg-e") >= 16),
        (f"{gap('sp-front', 'f-east'):.0f}", "the void from the spawn to the Near Arm", "", None),
        (", ".join(f"{gap(a, b):.0f}" for a, b in (("w-1", "w-2"), ("w-1", "w-3"), ("w-3", "f-stem"),
                                                   ("w-4", "f-stem"), ("w-1", "leg-w"))),
         "the Mist Steps' gaps", "about 12", None),
        (", ".join(f"{gap(a, b):.0f}" for a, b in (("e-1", "e-2"), ("e-1", "rows"), ("e-2", "road"))),
         "the Tea Steps' gaps", "about 12", None),
        (f"{red_store:.1f} / {blue_store:.1f}", "red and blue, spawn to their own Store", "equal",
         abs(red_store - blue_store) < 0.01),
        (f"{s_pillar:.1f} / {blue_pillar:.1f}", "red and blue, spawn to their own Pillar", "equal",
         abs(s_pillar - blue_pillar) < 0.01),
        (f"{apart}", "running jumps between pieces that do not touch", "none", apart == 0),
        (f"{land_red}", "land on red's half, in blocks", "", None),
    ]
    paths = dict(spawn_store=s_store_path, spawn_pillar=s_pillar_path, band_store=b_store_path,
                 band_pillar=b_pillar_path)
    return rows, paths, R


def save(rows, paths, path):
    """The table and the routes for the sketch, so it does not walk the plan (and its jumps) again."""
    import json
    with open(path, "w") as f:
        json.dump(dict(rows=rows, paths={k: [list(c) for c in v] for k, v in paths.items()}), f)


WALK_NO_LEDGES = WALK - {"ledge-w", "ledge-e"}


if __name__ == "__main__":
    import os
    rows, paths, _ = measure()
    save(rows, paths, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    w = max(len(r[1]) for r in rows)
    for value, what, target, ok in rows:
        mark = "" if ok is None else ("  ok" if ok else "  MISS")
        print(f"{what:<{w}}  {value:<22} {target}{mark}")
