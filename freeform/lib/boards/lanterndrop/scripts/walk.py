"""Read the built Lantern Drop back, on the blocks.

1. THE JUMPS. For every link, the air a player crosses from one piece's far edge to the next piece: across both
   pieces' widths, from the lower piece's top to over the higher's, holds nothing to hit or be caught by; and the
   first rows of the landing are clear to land on.
2. THE RUNS. On every piece a player can walk from its near edge to its far edge.
3. THE WATER. Every cistern three deep, every paddy one deep, the round harbour six deep round the barge.
4. THE HILLS. Every hill's border of white clay where it is not water.
5. THE VOID. Nothing within reach of the course but its own pieces and the harbour: a block standing beside a piece
   would catch a player knocked off it, which is the one thing this board must not do.

    python3 walk.py <build-dir>
"""
import sys
from collections import deque

import numpy as np

import gen as G
import plan as P
import render_iso
import walk_core as W

CATCH = {65, 106, 30}                                           # ladders, vines, cobweb


def main(build):
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = W.grid(ids)

    def at(x, y, z):
        return int(ids[x - x0, y, z - z0])

    def free(x, y, z):
        return passable[x - x0, y, z - z0] and at(x, y, z) not in CATCH

    out = []
    # ---- the jumps --------------------------------------------------------------------------------------
    blocked = []
    for a, b in P.links():
        lo, hi = min(a[3], b[3]), max(a[4], b[4])
        for x in range(lo, hi + 1):
            for z in range(a[6] + 1, b[5]):
                for y in range(b[7] + 1, a[7] + 4):
                    if not free(x, y, z):
                        blocked.append((a[1], b[1], x, y, z, at(x, y, z)))
        for x in range(b[3], b[4] + 1):
            for z in range(b[5], min(b[5] + 3, b[6] + 1)):
                for y in (b[7] + 1, b[7] + 2):
                    if not free(x, y, z) and at(x, y, z) != 8:
                        blocked.append((a[1], b[1], x, y, z, at(x, y, z)))
    out.append(f"blocks in the air of a jump or on a landing's first rows: {len(blocked)}" + (f" {blocked[:5]}" if blocked else ""))
    # ---- the runs -----------------------------------------------------------------------------------------
    stuck = []
    for p in P.pieces():
        i, name, theme, px0, px1, pz0, pz1, y, ex, sd = p
        seen = flood(passable, water, solid, x0, z0, y, px0, px1, pz0, pz1)
        if not any((x, pz1) in seen for x in range(px0, px1 + 1)):
            stuck.append(f"{sd} {name}")
    out.append(f"pieces a player cannot run across, near edge to far: {len(stuck)}" + (f" {stuck}" if stuck else ""))
    # ---- the water --------------------------------------------------------------------------------------
    dry = []
    for p in P.pieces():
        if "water" not in p[8]:
            continue
        a0, a1, b0, b1 = p[8]["water"]
        deep = 1 if p[2] == "terrace" else 3
        cells = [(x, z) for x in range(a0, a1 + 1) for z in range(b0, b1 + 1) if at(x, p[7], z) in (8, 9)]
        if not cells or any(at(x, yy, z) not in (8, 9) for x, z in cells for yy in range(p[7] - deep + 1, p[7] + 1)):
            dry.append(f"{p[9]} {p[1]}")
        elif deep == 3 and len(cells) < (a1 - a0 + 1) * (b1 - b0 + 1):
            dry.append(f"{p[9]} {p[1]} only {len(cells)} of its cells")
    h = P.HARBOUR
    barge = [p for p in P.pieces() if p[8].get("last")][0]
    cx, cz = sum(h["x"]) / 2.0, sum(h["z"]) / 2.0
    rx, rz = (h["x"][1] - h["x"][0]) / 2.0 + 0.5, (h["z"][1] - h["z"][0]) / 2.0 + 0.5
    hw = [(x, z) for x in range(h["x"][0], h["x"][1] + 1) for z in range(h["z"][0], h["z"][1] + 1)
          if ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1.0
          and not (barge[3] <= x <= barge[4] and barge[5] <= z <= barge[6])
          and not (P.SLIPWAY["x"][0] <= x <= P.SLIPWAY["x"][1] and z >= P.SLIPWAY["z"][0])]
    shallow = sum(1 for x, z in hw if any(at(x, yy, z) not in (8, 9) for yy in range(h["y"] - 5, h["y"] + 1)))
    out.append(f"water not as planned: {len(dry)} {dry}; harbour cells round the barge under six deep: {shallow} of {len(hw)}")
    # ---- the hills ---------------------------------------------------------------------------------------
    nohill = []
    for p in P.pieces():
        if not p[8].get("hill"):
            continue
        hx0, hx1, hz0, hz1 = G.hill_box(p)
        border = [(x, z) for x in range(hx0, hx1 + 1) for z in range(hz0, hz1 + 1) if x in (hx0, hx1) or z in (hz0, hz1)]
        if any(at(x, p[7], z) not in (8, 9, 159) for x, z in border):
            nohill.append(f"{p[9]} {p[1]}")
    out.append(f"hills whose border is not white clay: {len(nohill)} {nohill}")
    # ---- the void ----------------------------------------------------------------------------------------
    inside = np.zeros((ids.shape[0], ids.shape[2]), bool)
    for p in P.pieces():
        inside[p[3] - x0:p[4] - x0 + 1, p[5] - z0:p[6] - z0 + 1] = True
    inside[h["x"][0] - 2 - x0:h["x"][1] + 3 - x0, h["z"][0] - 2 - z0:h["z"][1] + 3 - z0] = True
    catchers = []
    for x in range(-34, 35):
        for z in range(-10, 323):
            if inside[x - x0, z - z0]:
                continue
            ys = np.nonzero(ids[x - x0, :, z - z0])[0]
            if len(ys):
                catchers.append((x, int(ys.max()), z, at(x, int(ys.max()), z)))
    out.append(f"blocks beside the course that would catch a player knocked off it: {len(catchers)}" + (f" {catchers[:6]}" if catchers else ""))
    print("\n".join(out))
    return out


def flood(passable, water, solid, x0, z0, y, px0, px1, pz0, pz1):
    def ok(x, yy, z):
        i, j = x - x0, z - z0
        return (solid[i, yy, j] or water[i, yy, j]) and passable[i, yy + 1, j] and passable[i, yy + 2, j]

    starts = [(x, yy, pz0) for x in range(px0, px1 + 1) for yy in (y, y + 1, y - 1, y - 2) if ok(x, yy, pz0)]
    seen = set(starts)
    q = deque(starts)
    while q:
        x, yy, z = q.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not (px0 <= x + dx <= px1 and pz0 <= z + dz <= pz1):
                continue
            for dy in (0, 1, -1, -2):
                n = (x + dx, yy + dy, z + dz)
                if y - 3 <= n[1] <= y + 1 and n not in seen and ok(*n):
                    seen.add(n)
                    q.append(n)
                    break
    return {(x, z) for x, yy, z in seen}


if __name__ == "__main__":
    main(sys.argv[1])
