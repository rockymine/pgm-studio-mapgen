"""Audit placements against the ground they should stand on: every building's floor, every tree's foot,
every prop. A thing whose floor has air under it, or rock over its roof, is in the wrong place.

    python3 audit.py <build-dir>

Run from gen.py's world (it rebuilds the red half in memory and reads the records the builders kept).
"""
import sys

import numpy as np

import plan as P
from mc import World, B
import terrain
import underground
import buildings
import dressing

SOLIDISH = lambda i: i not in (B.AIR, B.WATER, B.WATER_FLOW, B.LEAVES, B.LEAVES2, B.TALLGRASS, B.DEADBUSH)


def column_gap(w, x, z, y):
    """How many blocks of air lie directly under y before the ground: 0 means it stands on something."""
    gap = 0
    yy = y - 1
    while yy > 0 and not SOLIDISH(w.id(x, yy, z)):
        gap += 1
        yy -= 1
        if gap > 40:
            break
    return gap


def main():
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
    L = terrain.Land()
    terrain.build_heights(L); terrain.build_underside(L); terrain.write_land(w, L)
    terrain.write_falls(w, L); terrain.sky_arch(w, L)
    import gen
    L.green = gen.green_mask(L)
    H0 = L.H.copy()
    underground.build(w, L)
    buildings.build(w, L)
    dressing.build(w, L)
    problems = []
    arch = set(L.arch_top)
    for r in L.records:
        x0, z0, x1, z1, f = r["x0"], r["z0"], r["x1"], r["z1"], r["floor"]
        under = [column_gap(w, x, z, f) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
        on_arch = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if (x, z) in arch]
        above = sum(1 for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)
                    if any(w.id(x, y, z) in (B.STAINED_CLAY, B.HARDENED_CLAY) for y in range(f + 12, f + 30)))
        tag = f"{r['kind']:9} ({x0},{z0})-({x1},{z1}) floor {f}"
        if max(under) > 0:
            problems.append(f"{tag}: air under its floor, up to {max(under)} blocks")
        if on_arch:
            problems.append(f"{tag}: stands under or on the Sky Arch at {on_arch[:3]}")
        if above:
            problems.append(f"{tag}: rock over {above} of its columns")
    for name, other, box in L.conflicts:
        problems.append(f"{name} at {box} overlaps {other}")
    for name, (x0, z0, x1, z1) in L.things:
        sub = H0[x0 - L.x0:x1 - L.x0 + 1, z0 - L.z0:z1 - L.z0 + 1]
        if sub.size and sub.max() - sub.min() > 5:
            problems.append(f"{name} at {(x0, z0, x1, z1)} was set into ground that rose {sub.max() - sub.min()} blocks across it (a cliff?)")
        # anything tall under the arch must clear its underside
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if (x, z) in arch:
                    tallest = max((y for y in range(40, 100) if w.id(x, y, z) not in (B.AIR,) and y < L.arch_top[(x, z)] - 12), default=0)
    for (x, z, c) in L.trees:
        g = int(L.H[x - L.x0, z - L.z0])
        if (x, z) in arch:
            problems.append(f"tree at ({x},{z}) is under the arch")
    for name, (x0, z0, x1, z1) in L.things:
        if any((x, z) in arch for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)) and name != "Gilt Spring plaza":
            problems.append(f"{name} at {(x0, z0, x1, z1)} stands under the Sky Arch")
    print(f"{len(L.records)} buildings, {len(L.things)} placed things, {len(L.trees)} trees audited")
    print("\n".join(problems) if problems else "no placement problems found")


if __name__ == "__main__":
    main()
