"""Read the built Sunwell back, on the blocks.

1. THE DROPS. Over every opening in every rim, the air a player falls through, from the shelf's top down to the
   shelf below and out as far as the target, holds nothing a player could hit or be caught by.
2. THE TARGETS. Every pool is water three deep; every falls' curtain is water from shelf to shelf over a basin two
   deep; every shaft is open from the shelf it cuts down to the pool or the lake under it; every hill's border is
   white clay where it is not water; the islet stands two over the lake.
3. THE SHELVES. Every rim is a wall too tall to step over, open only at its gaps; no shelf leaves a gap against the
   wall a player could fall through; and on every shelf a player who lands at any target can walk to every gap of
   the next drop.
4. THE SPRING. Water at the lake's level in a grotto, where map.xml's portal is.

    python3 walk.py <build-dir>
"""
import sys
from collections import deque

import numpy as np

import gen as G
import plan as P
import render_iso
import walk_core as W

CATCH = {65, 106, 30}                                          # ladders, vines, cobweb: they catch a falling player


def main(build):
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = W.grid(ids)

    def at(x, y, z):
        return int(ids[x - x0, y, z - z0])

    out = []
    # ---- the drops ---------------------------------------------------------------------------------------
    blocked = []
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        ya, yb = P.shelf_y(k), P.shelf_y(k + 1)
        for kind, gx0, gx1, s0, sd in P.gaps(k):
            if kind == "falls":
                continue
            reach = 12 if kind != "shaft" else s0 + 3
            for x in range(gx0, gx1 + 1):
                for s in range(1, reach + 1):
                    z = P.z_of(k, s)
                    if not P.in_shaft(x, z):
                        continue
                    for y in range(yb + 3, ya + 3):
                        b = at(x, y, z)
                        if not passable[x - x0, y, z - z0] or b in CATCH:
                            blocked.append((k + 1, kind, x, y, z, b))
    out.append(f"blocks in the air a player falls through, over every gap: {len(blocked)}" + (f" {blocked[:5]}" if blocked else ""))
    # ---- the targets --------------------------------------------------------------------------------------
    bad = []
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        ya, yb = P.shelf_y(k), P.shelf_y(k + 1)
        for name, a0, a1, s0, s1, sd in P.pools(k):
            for x in range(a0, a1 + 1):
                for s in range(s0, s1 + 1):
                    z = P.z_of(k, s)
                    if not all(at(x, y, z) in (8, 9) for y in (yb - 2, yb - 1, yb)):
                        bad.append(f"{k + 1} {sd} {name} not three deep at ({x}, {z})")
        for name, a0, a1, s0, s1, sd in P.falls(k):
            for x in range(a0, a1 + 1):
                z = P.z_of(k, 1)
                dry = [y for y in range(yb + 1, ya + 1) if at(x, y, z) not in (8, 9)]
                if dry:
                    bad.append(f"{k + 1} {sd} falls dry at ({x}, {z}) from {dry[0]}")
                if not all(at(x, y, P.z_of(k, s)) in (8, 9) for s in range(s0, s1 + 1) for y in (yb - 1, yb)):
                    bad.append(f"{k + 1} {sd} falls' basin not two deep at x {x}")
        for name, a0, a1, s0, s1, sd in P.shafts(k):
            land = P.LAKE_Y if k + 3 >= len(P.DROPS) else P.shelf_y(k + 3)
            for x in range(a0, a1 + 1):
                for s in range(s0, s1 + 1):
                    z = P.z_of(k, s)
                    shut = [y for y in range(land + 1, yb + 3) if not passable[x - x0, y, z - z0] or at(x, y, z) in CATCH]
                    if shut:
                        bad.append(f"{k + 1} {sd} shaft shut at ({x}, {shut[-1]}, {z}): {at(x, shut[-1], z)}")
                    if at(x, land, z) not in (8, 9):
                        bad.append(f"{k + 1} {sd} shaft lands on {at(x, land, z)} at ({x}, {land}, {z})")
    for k, d in enumerate(P.DROPS):
        y = P.ISLET["y"] if d.get("lake") else P.shelf_y(k + 1)
        for name, a0, a1, s0, s1, sd in P.hills(k):
            for x in range(a0, a1 + 1):
                for s in (s0, s1):
                    z = P.z_of(k, s)
                    if at(x, y, z) not in (8, 9, B_CLAY):
                        bad.append(f"{k + 1} {sd} {name}'s border at ({x}, {y}, {z}) is {at(x, y, z)}")
    k = len(P.DROPS) - 1
    islet = [at(x, P.ISLET["y"], P.z_of(k, s)) for x in range(*P.ISLET["x"]) for s in range(*P.ISLET["s"])]
    out.append(f"targets not as planned: {len(bad)}" + (f" {bad[:6]}" if bad else "")
               + f"; the islet's top solid: {all(b not in (0, 8, 9) for b in islet)}")
    # ---- the shelves ----------------------------------------------------------------------------------------
    rim_bad, leaks, cut_off = [], [], []
    for k in range(P.N_SHELVES):
        y = P.shelf_y(k)
        ze = P.EDGE if P.side(k) == "N" else -P.EDGE
        gaps = P.gaps(k)
        for x in range(-P.R_SHAFT, P.R_SHAFT + 1):
            if not P.on_shelf(k, x, ze):
                continue
            open_ = any(g[1] <= x <= g[2] for g in gaps)
            b = at(x, y + 1, ze)
            if open_ and b == 139:
                rim_bad.append((k + 1, x, "shut"))
            if not open_ and b != 139:
                rim_bad.append((k + 1, x, "open"))
        for x in range(-P.R_SHAFT - 1, P.R_SHAFT + 2):
            for z in range(-P.R_SHAFT - 1, P.R_SHAFT + 2):
                if P.on_shelf(k, x, z) or not G.on_side(k, z) or P.in_shaft(x, z):
                    continue
                if any(P.on_shelf(k, x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    if all(passable[x - x0, yy, z - z0] for yy in range(y - P.THICK + 1, y + 1)):
                        leaks.append((k + 1, x, z))
    # walking on each shelf: from every landing to every gap of the next drop
    for k in range(len(P.DROPS) - 1):
        shelf = k + 1
        y = P.shelf_y(shelf)
        ze = P.EDGE if P.side(shelf) == "N" else -P.EDGE
        seen = set()
        starts = []
        for name, a0, a1, s0, s1, sd in P.pools(k) + P.falls(k) + P.hills(k):
            starts.append(((a0 + a1) // 2, P.z_of(k, (s0 + s1) // 2), f"{sd} {name}"))
        for sx, sz, label in starts:
            reach = flood(passable, water, solid, x0, z0, y, sx, sz)
            for kind, gx0, gx1, s0, sd in P.gaps(shelf):
                if not any((x, ze) in reach for x in range(gx0, gx1 + 1)):
                    cut_off.append(f"shelf {shelf + 1}: from {label} to the {sd} {kind} gap")
    out.append(f"rim blocks wrong: {len(rim_bad)} {rim_bad[:5]}; gaps between a shelf and the wall: {len(leaks)} {leaks[:5]}")
    out.append(f"landings that cannot walk to a gap of the next drop: {len(set(cut_off))}" + (f" {sorted(set(cut_off))[:6]}" if cut_off else ""))
    # ---- the spring ----------------------------------------------------------------------------------------
    sx = (P.SPRING["x"][0] + P.SPRING["x"][1]) // 2
    sz = P.SPRING["z"][1] + 2
    out.append(f"the spring's grotto: water at the lake's level {at(sx, P.LAKE_Y, sz) in (8, 9)}, open over it "
               f"{at(sx, P.LAKE_Y + 2, sz) == 0}")
    print("\n".join(out))
    return out


B_CLAY = 159


def flood(passable, water, solid, x0, z0, y, sx, sz):
    """Where a player can walk on a shelf whose top is y: a cell is walkable if its top block is solid or water and
    the two over it are passable; a step of one up or down is allowed, as over a pool's lip."""
    def ok(x, yy, z):
        i, j = x - x0, z - z0
        if not (0 <= i < passable.shape[0] and 0 <= j < passable.shape[2]):
            return False
        return (solid[i, yy, j] or water[i, yy, j]) and passable[i, yy + 1, j] and passable[i, yy + 2, j]

    start = None
    for yy in (y, y - 1, y - 2, y + 1):
        if ok(sx, yy, sz):
            start = (sx, yy, sz)
            break
    if start is None:
        return set()
    seen = {start}
    q = deque([start])
    while q:
        x, yy, z = q.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (0, 1, -1, -2):
                n = (x + dx, yy + dy, z + dz)
                if y - 3 <= n[1] <= y + 1 and n not in seen and ok(*n):
                    seen.add(n)
                    q.append(n)
                    break
    return {(x, z) for x, yy, z in seen}


if __name__ == "__main__":
    main(sys.argv[1])
