"""Audit placements against the islands they should stand on: every building's floor, every claimed thing,
every bridge's course, every tree's foot. A floor with air under it, a thing hanging off a rim, two claims on
one piece of ground, or a bridge through a building is in the wrong place.

    python3 audit.py
"""
import numpy as np

import gen
import terrain
from mc import B

SOLIDISH = lambda i: i not in (B.AIR, B.WATER, B.WATER_FLOW, B.LEAVES, B.LEAVES2, B.TALLGRASS, B.VINE, B.FLOWER)


def column_gap(w, x, z, y):
    gap, yy = 0, y - 1
    while yy > 0 and not SOLIDISH(w.id(x, yy, z)) and gap <= 40:
        gap += 1
        yy -= 1
    return gap


def main():
    F0 = terrain.build(terrain.Field())
    w, F = gen.make()
    problems = []
    for r in F.records:
        x0, z0, x1, z1, f = r["x0"], r["z0"], r["x1"], r["z1"], r["floor"]
        under = [column_gap(w, x, z, f) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
        off = sum(1 for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if not F0.land[x - F.x0, z - F.z0])
        tag = f"{r['kind']:16} ({x0},{z0})-({x1},{z1}) floor {f}"
        if max(under) > 0:
            problems.append(f"{tag}: air under its floor, up to {max(under)} blocks")
        if off:
            problems.append(f"{tag}: {off} of its columns hang off the island's rim")
    for name, other, box in F.conflicts:
        problems.append(f"{name} at {box} overlaps {other}")
    afloat = ("the Concord", "the Albatross", "the pier")
    for name, (x0, z0, x1, z1) in F.things:
        if name in afloat or name.startswith("balloon"):
            continue
        sub = F0.H[x0 - F.x0:x1 - F.x0 + 1, z0 - F.z0:z1 - F.z0 + 1]
        land = sub[sub > 0]
        if land.size and land.max() - land.min() > 5:
            problems.append(f"{name} at {(x0, z0, x1, z1)} was set into ground that rose {land.max() - land.min()} blocks across it")
    for b in F.bridges:
        steps = [abs(b["cells"][k + 1][2] - b["cells"][k][2]) for k in range(len(b["cells"]) - 1)]
        if max(steps) > 1:
            problems.append(f"bridge {b['a']}-{b['b']} has a step of {max(steps)} blocks")
    print(f"{len(F.records)} buildings, {len(F.things)} placed things, {len(F.bridges)} bridges, {len(F.trees)} trees audited (red's half)")
    print("\n".join(problems) if problems else "no placement problems found")


if __name__ == "__main__":
    main()
