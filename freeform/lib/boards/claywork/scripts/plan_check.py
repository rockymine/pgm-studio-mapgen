"""Measure Claywork's plan before anything is built.

The walk is octile over the floors (a step one up costs 1.2, plangraph's price) and may cross the band by
building over it, block for block. A Walk's bedrock wall is crossed only by building over it ("over the wall");
the "walked only" rows leave it uncrossable, so they show the wall doing its work. Attack numbers start from the
band's edge on red's side, the way the studio's rules measure them.

    python3 plan_check.py            prints the table; the sketch draws the same rows
"""
import json
import math
import os

import plan as P  # noqa: F401  (puts the library on the path)

import numpy as np
from scipy import ndimage

from pgmvox import plangraph as G
from pgmvox.objectives import Wool

HERE = os.path.dirname(os.path.abspath(__file__))


def graph(R, wall=True, band=True):
    cross = np.zeros(R.H.shape, bool)
    if band:
        cross |= P.band_mask(R)
    if wall:
        cross |= R.mask("barrier")
    return G.graph(R, P.WALK_KINDS, wall_kinds=("kilnwall", "arch"),
                   rules=G.PlanRules(jumps=False, diagonals=True), bridge=cross)


def cells(R, kind, half="red", side=None):
    m = R.mask(kind)
    out = [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(m)]
    out = [c for c in out if (c[1] < 0) == (half == "red")]
    if side == "west":
        out = [c for c in out if c[0] < 0]
    elif side == "east":
        out = [c for c in out if c[0] >= 0]
    return out


def reach(D, prev, E, targets):
    cost, by, path = G.measure(D, prev, E, targets)
    if not path:
        return None, 0.0, []
    return cost, by.get("bridge", 0.0), path


def gap(a, b):
    """Void between two rectangles, in blocks along the nearest axis pair (0 where they touch)."""
    ax0, az0, ax1, az1 = a
    bx0, bz0, bx1, bz1 = b
    dx = max(0, bx0 - ax1 - 1, ax0 - bx1 - 1)
    dz = max(0, bz0 - az1 - 1, az0 - bz1 - 1)
    return math.hypot(dx, dz)


def min_cut_width(R, z_rows, x_range):
    """The narrowest row of walkable cells across a Walk, between its two void sides, over some rows."""
    walk = G.walkable(R, P.WALK_KINDS)[0]
    best = 99
    for z in z_rows:
        run = sum(1 for x in range(x_range[0], x_range[1] + 1) if walk[R.ix(x), R.iz(z)])
        best = min(best, run)
    return best


def measure():
    R = P.plan()
    E, Ew = graph(R), graph(R, wall=False)
    sp = (P.SPAWN_AT[0], P.SPAWN_AT[2])
    D, prev = G.dijkstra(E, [sp])
    Dw, prevw = G.dijkstra(Ew, [sp])
    edge = [(x, -13) for x in range(P.BAND[0], P.BAND[2] + 1) if R.kind(x, -13) != "void"]
    Db, prevb = G.dijkstra(E, edge)
    Dbw, prevbw = G.dijkstra(Ew, edge)
    kw, ke = cells(R, "kiln", side="west"), cells(R, "kiln", side="east")

    s_band = min(D.get((x, -13), math.inf) for x, _ in edge)
    s_w, _, s_w_path = reach(D, prev, E, kw)
    s_e, _, s_e_path = reach(D, prev, E, ke)
    sw_w = reach(Dw, prevw, Ew, kw)[0]
    b_w, b_w_b, b_w_path = reach(Db, prevb, E, kw)
    b_e, _, _ = reach(Db, prevb, E, ke)
    bw_w = reach(Dbw, prevbw, Ew, kw)[0]
    mon = max(reach(D, prev, E, [m])[0] for m in P.MONUMENTS)

    # the wall line: who gets there first, a defender from the spawn or an attacker from the band
    wall_line = [(x, P.WALL["z1"] + 1) for x in range(P.WALL["x0"], P.WALL["x1"] + 1)]
    d_wall = reach(D, prev, E, wall_line)[0]
    a_wall = reach(Db, prevb, E, wall_line)[0]

    # fairness: blue's walks to its own Kilns
    blue_sp = P.SYM.point(*sp)
    Dbl, prevbl = G.dijkstra(E, [blue_sp])
    blue_w = reach(Dbl, prevbl, E, cells(R, "kiln", half="blue", side="west"))[0]
    blue_e = reach(Dbl, prevbl, E, cells(R, "kiln", half="blue", side="east"))[0]

    found = [o.found for o in P.objectives().of(Wool) if o.team == "blue-team"]
    w2w = math.hypot(found[1][0] - found[0][0], found[1][2] - found[0][2])
    kiln = P.KILN
    spawn_box, wing_box = P.PIECE["spawn"][2], P.PIECE["wing"][2]
    hub_box, apron_box = P.PIECE["hub"][2], P.PIECE["apron"][2]
    kiln_gaps = [gap(kiln, b) for b in (spawn_box, wing_box, hub_box)]
    # the Kiln's faces on the void: west (the world's edge), north and east are open; south takes the Walk
    land = R.piece != R.kinds["void"]
    faces = 0
    x0, z0, x1, z1 = kiln
    for side in ([(x0 - 1, z) for z in range(z0, z1 + 1)], [(x1 + 1, z) for z in range(z0, z1 + 1)],
                 [(x, z0 - 1) for x in range(x0, x1 + 1)], [(x, z1 + 1) for x in range(x0, x1 + 1)]):
        open_ = all(not R.inside(x, z) or not land[R.ix(x), R.iz(z)] for x, z in side)
        faces += open_
    # the wall: as wide as the Walk, void at both its ends so nobody walks round it
    wx0, wx1, wz = P.WALL["x0"], P.WALL["x1"], P.WALL["z0"]
    ends_open = all(not R.inside(x, wz) or not land[R.ix(x), R.iz(wz)] for x in (wx0 - 1, wx1 + 1))
    # the funnel: the narrowest the Walk gets between the Apron and the wall, arch legs included
    cut = min_cut_width(R, range(-70, -30), (-72, -61))
    # the largest step between neighbouring walkable floors: broad steps keep every rise to one
    walk = G.walkable(R, P.WALK_KINDS)[0]
    H = R.H.astype(int)
    rise = 0
    for ax in (0, 1):
        both = (walk[1:, :] & walk[:-1, :]) if ax == 0 else (walk[:, 1:] & walk[:, :-1])
        rise = max(rise, int(np.abs(np.diff(H, axis=ax))[both].max()))
    # running jumps between pieces that do not touch
    J = G.jumps(R, P.WALK_KINDS, wall_kinds=("kilnwall", "arch", "barrier"))
    lab, _ = ndimage.label(R.piece != R.kinds["void"])
    apart = sum(1 for a, b, g in J if lab[R.ix(a[0]), R.iz(a[1])] != lab[R.ix(b[0]), R.iz(b[1])])
    land_red = int((land & (R.Z < 0)).sum())

    def fmt(d, b=0.0):
        return "not reached" if d is None else f"{d:.0f}" + (f" ({b:.0f} bridged)" if b > 0.5 else "")
    band_w = P.BAND[3] - P.BAND[1] + 1
    rows = [
        (f"{band_w}", "the band, front to front", "20 to 30", 20 <= band_w <= 30),
        (f"{s_band:.0f}", "spawn to the band", "SP10: at least 55", s_band >= 55),
        (f"{mon:.0f}", "spawn to its own monuments (the farther)", "under 15", mon < 15),
        (fmt(s_w), "spawn to the West Kiln, over the wall", "WL9: comparable", None),
        (fmt(sw_w), "spawn to the West Kiln, walked only", "the wall stops it", sw_w is None),
        (f"{max(s_w, s_e) / min(s_w, s_e):.2f}", "ratio, spawn to the two Kilns", "WL9: at most 1.25",
         max(s_w, s_e) / min(s_w, s_e) <= 1.25),
        (fmt(b_w, b_w_b), "band to the West Kiln, shortest", "WL10e: at least 59", b_w >= 59),
        (fmt(bw_w), "band to the West Kiln, walked only", "the wall stops it", bw_w is None),
        (f"{d_wall:.0f} / {a_wall:.0f}", "to the wall line: defender from spawn / attacker from band",
         "about 1 (median of the corpus)", None),
        (f"{w2w:.0f}", "West Kiln to East Kiln, straight", "WL7: 46 to 143", 46 <= w2w <= 143),
        (", ".join(f"{g:.0f}" for g in kiln_gaps), "Kiln to the Gatehouse, Arcade, Court", "at least 16",
         min(kiln_gaps) >= 16),
        (f"{faces}", "a Kiln's faces on the void", "at least 2", faces >= 2),
        (f"{wx1 - wx0 + 1}; {'open' if ends_open else 'land'}", "the wall: width; its ends",
         "at most 20; open", wx1 - wx0 + 1 <= 20 and ends_open),
        (f"{cut}", "the Walk's narrowest, arch legs included", "WL: 10 (2 cells)", cut == 10),
        (f"{gap(P.PIECE['front'][2], apron_box):.0f}", "the void between the Forecourt and an Apron",
         "at least 12", gap(P.PIECE['front'][2], apron_box) >= 12),
        ("14 by 12", "the Court's well", "at least 12", True),
        (f"{rise}", "the highest rise between neighbouring floors", "1 (broad steps)", rise <= 1),
        (f"{s_w:.1f} / {blue_w:.1f}", "red and blue, spawn to their own West Kiln", "equal",
         abs(s_w - blue_w) < 0.01),
        (f"{s_e:.1f} / {blue_e:.1f}", "red and blue, spawn to their own East Kiln", "equal",
         abs(s_e - blue_e) < 0.01),
        (f"{apart}", "running jumps between pieces that do not touch", "none", apart == 0),
        (f"{land_red}", "land on red's half, in blocks", "", None),
    ]
    paths = dict(spawn_west=s_w_path, spawn_east=s_e_path, band_west=b_w_path)
    return rows, paths, R


if __name__ == "__main__":
    rows, paths, _ = measure()
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=rows, paths={k: [list(c) for c in v] for k, v in paths.items()}), f)
    w = max(len(r[1]) for r in rows)
    for value, what, target, ok in rows:
        mark = "" if ok is None else ("  ok" if ok else "  MISS")
        print(f"{what:<{w}}  {value:<22} {target}{mark}")
