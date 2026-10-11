"""Audit placements against the ground they should stand on: every building's floor, every claimed thing's
footprint, every tree's foot. A thing whose floor has air under it, that stands in water, or that two
builders both claimed, is in the wrong place.

    python3 audit.py
"""
import numpy as np

import gen
from mc import B

SOLIDISH = lambda i: i not in (B.AIR, B.WATER, B.LEAVES, B.LEAVES2, B.TALLGRASS, B.SNOW_LAYER)


def column_gap(w, x, z, y):
    """How many blocks of air lie directly under y before the ground: 0 means it stands on something."""
    gap, yy = 0, y - 1
    while yy > 0 and not SOLIDISH(w.id(x, yy, z)) and gap <= 40:
        gap += 1
        yy -= 1
    return gap


def main():
    import terrain
    F0 = terrain.build(terrain.Field())
    H0 = F0.H.copy()
    w, F = gen.make()
    problems = []
    for r in F.records:
        x0, z0, x1, z1, f = r["x0"], r["z0"], r["x1"], r["z1"], r["floor"]
        under = [column_gap(w, x, z, f) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
        wet = int(F.water[x0 - F.x0:x1 - F.x0 + 1, z0 - F.z0:z1 - F.z0 + 1].sum())
        tag = f"{r['kind']:9} ({x0},{z0})-({x1},{z1}) floor {f}"
        if max(under) > 0:
            problems.append(f"{tag}: air under its floor, up to {max(under)} blocks")
        if wet and r["kind"] != "boathouse":         # a boathouse stands out over the water on purpose
            problems.append(f"{tag}: {wet} of its columns stand in the water")
    for name, other, box in F.conflicts:
        problems.append(f"{name} at {box} overlaps {other}")
    afloat = ("the whaler", "the Old Bridge", "landing stage", "pier", "monument clearance")   # the knoll is the point
    for name, (x0, z0, x1, z1) in F.things:
        if name in afloat:
            continue
        sub = H0[x0 - F.x0:x1 - F.x0 + 1, z0 - F.z0:z1 - F.z0 + 1]
        dry = ~(F0.water | F0.lake)[x0 - F.x0:x1 - F.x0 + 1, z0 - F.z0:z1 - F.z0 + 1]
        land = sub[(sub > 0) & dry]
        if land.size and land.max() - land.min() > 6:
            problems.append(f"{name} at {(x0, z0, x1, z1)} was set into ground that rose {land.max() - land.min()} blocks across it (a cliff?)")
    for (x, z, c) in F.trees:
        if F.water[x - F.x0, z - F.z0] or F.lake[x - F.x0, z - F.z0]:
            problems.append(f"tree at ({x},{z}) stands in water")
    print(f"{len(F.records)} buildings, {len(F.things)} placed things, {len(F.trees)} trees audited (red's half)")
    print("\n".join(problems) if problems else "no placement problems found")


if __name__ == "__main__":
    main()
