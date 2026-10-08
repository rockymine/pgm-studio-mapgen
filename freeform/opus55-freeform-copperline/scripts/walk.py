"""Read the built Copperline back: the rails as PGM will trace them, and each leg walked on the real blocks.

1. THE TRACK. Every rail in the built volume (plain, detector or powered) is collected with its data, and each
   leg is traced from its payload's `location` by `track.py`, PGM's Track over a dict. The trace must be the
   leg as planned, cell for cell, and no rail on the board may be left that a leg's trace could run into.
2. THE LEGS. For each leg the gates of the legs already done are opened in a copy of the blocks (the boxes
   map.xml fills with air) and each team's spawn for the leg is walked, on foot, every drop allowed, to the
   cart, the leg's middle and its end. Before the warm-up ends the attackers must not leave their shed.
3. THE VALLEY. Everything any spawn can reach with every gate open, looked at for a place that stands on a
   mountain: a column the plan gives to rock, outside the rooms carved into it.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import gen as G
import plan as P
import render_iso
import track as T
import walk_core as W

RAIL_IDS = (27, 28, 66)


def rails(ids, dat, x0, z0):
    out = {}
    for bid in RAIL_IDS:
        for i, y, k in zip(*np.nonzero(ids == bid)):
            out[(int(i) + x0, int(y), int(k) + z0)] = int(dat[i, y, k])
    return out


def world_at(ids, x0, z0, done):
    ids = ids.copy()
    for stage in done:
        for bx0, by0, bz0, bx1, by1, bz1 in G.GATE_REGIONS[stage]:
            ids[bx0 - x0:bx1 - x0 + 1, by0:by1 + 1, bz0 - z0:bz1 - z0 + 1] = 0
    return ids


def walker(ids, x0, z0):
    passable, water, ladder, solid = W.grid(ids)
    st = W.standable(passable, water, solid) | (ladder & passable)
    return st, (lambda start: W.bfs(st, ladder, water, passable, start, x0, z0))


def spawn(team, stage):
    x, y, z, _ = P.SPAWNS[team][stage]
    return (int(np.floor(x)), int(y), int(np.floor(z)))


def at(d, x0, z0, p, r=2):
    v = W.nearest(d, x0, z0, *p, r=r)
    return "NOT REACHED" if v is None else str(v)


def main(build):
    x0, z0, ids0, dat = render_iso.load(build)
    out = []
    # ---- the track ----------------------------------------------------------------------------------------
    rs = rails(ids0, dat, x0, z0)
    used = set()
    for leg in P.LEGS:
        want = [(x, hh + 1, z) for x, z, hh, d in P.lay(leg)]
        s = want[0]
        got = T.trace(rs, s)
        used |= set(got)
        same = got == want
        n_curve = sum(rs[p] >= 6 for p in got)
        n_slope = sum(2 <= rs[p] <= 5 for p in got)
        out.append(f"track {leg['key']}: payload at {s}, traced {len(got)} rails ({n_curve} curves, {n_slope} sloped) "
                   f"to {got[-1]}: {'as planned' if same else 'NOT AS PLANNED'}")
    powered = [p for p, d in rs.items() if d > 9]
    near = [p for p in rs if p not in used and any(abs(p[0] - q[0]) + abs(p[2] - q[2]) <= 2 and abs(p[1] - q[1]) <= 2
                                                   for q in used)]
    out.append(f"rails on the board: {len(rs)}, {len(used)} in the three legs, {len(rs) - len(used)} elsewhere "
               f"(the shed's road, the adit's line, the tramway); within two blocks of a leg: {len(near)}; data over 9: {len(powered)}")
    # ---- spawns ---------------------------------------------------------------------------------------------
    full = world_at(ids0, x0, z0, ["warmup", "A", "B"])
    st_full, wf = walker(full, x0, z0)
    bad = [f"{t} {s}" for t, ss in P.SPAWNS.items() for s in ss
           if not st_full[spawn(t, s)[0] - x0, spawn(t, s)[1], spawn(t, s)[2] - z0]]
    out.append(f"spawn points that do not stand on ground with headroom: {len(bad)} {bad}")
    # ---- the warm-up ---------------------------------------------------------------------------------------
    _, w0 = walker(world_at(ids0, x0, z0, []), x0, z0)
    d = w0([spawn("attackers", "1")])
    a0 = P.lay(P.LEGS[0])[0]
    out.append(f"warm-up: the attackers reach their cart before the shed opens: {at(d, x0, z0, (a0[0], a0[2] + 1, a0[1]), 3)}")
    # ---- the legs ----------------------------------------------------------------------------------------------
    order = ["warmup", "A", "B"]
    for n, leg in enumerate(P.LEGS):
        done = order[:n + 1]
        _, wk = walker(world_at(ids0, x0, z0, done), x0, z0)
        cells = P.lay(leg)
        pts = [cells[0], cells[len(cells) // 2], cells[-1]]
        pts = [(x, hh + 1, z) for x, z, hh, dd in pts]
        da = wk([spawn("attackers", str(n + 1))])
        dd = wk([spawn("defenders", str(n + 1))])
        out.append(f"leg {leg['key']}, {leg['name']}: attackers {at(da, x0, z0, pts[0])} to the cart, {at(da, x0, z0, pts[1])} "
                   f"to its middle, {at(da, x0, z0, pts[2])} to the end; defenders {at(dd, x0, z0, pts[0])}, "
                   f"{at(dd, x0, z0, pts[1])}, {at(dd, x0, z0, pts[2])}")
    # ---- the ways the plan walked ----------------------------------------------------------------------------
    _, wk = walker(world_at(ids0, x0, z0, order), x0, z0)
    for name, way, a, b, L in P.CONNECTORS:
        ya = int(G.GROUND[P.ix(a[0]), P.iz(a[1])]) + 1
        if name == "the north ladder":
            ya = G.RIVER_BED + 1
        da = wk([(a[0], ya, a[1])])
        yb = int(G.GROUND[P.ix(b[0]), P.iz(b[1])]) + 1 if name != "the adit" else 37
        out.append(f"{name} ({way}): from its foot to its head on the blocks {at(da, x0, z0, (b[0], yb, b[1]), 2)} (the plan's cost {L})")
    # ---- the valley ------------------------------------------------------------------------------------------
    starts = [spawn(t, s) for t, ss in P.SPAWNS.items() for s in ss]
    dist = wf(starts)
    reach = dist >= 0
    rock = (P.build().K == P.KINDS["rock"])
    esc = []
    for i, k in zip(*np.nonzero(rock)):
        x, z = int(i) + P.X_MIN, int(k) + P.Z_MIN
        if G.in_mountain_room(x, z, 1) or abs(z - P.HEAP["c"][1]) <= 2 and x >= P.HEAP["box"][1] \
                or (x <= -51 and -15 <= z <= -9) or (x >= 52 and -13 <= z <= -11):   # the river's cave, the falls' slot

            continue
        ys = np.nonzero(reach[i, :, k])[0]
        if len(ys) and ys.max() > G.GROUND.max() - 100 and ys.max() > 13:
            if ys.max() > 40 or not any(abs(x - a) <= 4 and abs(z - b) <= 4 for a, b in G.ADIT_XZ):
                esc.append((x, int(ys.max()), z))
    out.append(f"places standing on a mountain that a spawn reaches: {len(esc)} {esc[:40]}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
