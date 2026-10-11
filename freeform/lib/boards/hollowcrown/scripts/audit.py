"""Audit placements against the ground they stand on and the ways they must leave open: every house's plate,
every claim, the roads, the water, the monuments' surroundings, the clouds' height.

    python3 audit.py
"""
import math

import numpy as np

import gen
import plan as P
from mc import B

SOLIDISH = lambda i: i not in (B.AIR, B.WATER, B.WATER_FLOW, B.LEAVES, B.LEAVES2, B.TALLGRASS, B.VINE, B.FLOWER,
                               B.REEDS, B.SNOW_LAYER)
MAX_BUILD = 112


def main():
    w, F = gen.make()
    problems = []
    for r in F.records:
        f = r["floor"]
        hung = [c for c in r["cells"] if not SOLIDISH(w.id(c[0], f, c[1])) or not SOLIDISH(w.id(c[0], f - 1, c[1]))]
        if hung:
            problems.append(f"{r['kind']} (floor {f}): {len(hung)} of its plate's blocks have air under them")
        if r["kind"].startswith(("house", "the 0", "the 12", "the 45", "farmhouse", "the mill")):
            on_road = [c for c in r["cells"] if F.wend[c[0] - F.x0, c[1] - F.z0] < 2.6 or F.corr[c[0] - F.x0, c[1] - F.z0] < 0.6]
            wet = [c for c in r["cells"] if F.water_any[c[0] - F.x0, c[1] - F.z0]]
            if on_road:
                problems.append(f"{r['kind']}: stands on a road at {len(on_road)} blocks")
            if wet:
                problems.append(f"{r['kind']}: stands in water at {len(wet)} blocks")
    for name, other in F.conflicts:
        problems.append(f"{name} overlaps {other}")
    for (x, z, c) in F.trees:
        if F.water_any[x - F.x0, z - F.z0]:
            problems.append(f"tree at ({x},{z}) stands in water")
    for name, (mx, my, mz) in (("monument A", F.mon_a), ("monument B", F.mon_b)):
        for (x, z, c) in (F.trees if name == "monument A" else []):        # B is underground, under no tree
            if math.hypot(x - mx, z - mz) < c + 4:
                problems.append(f"a tree's crown at ({x},{z}) comes within four blocks of {name}")
        if my + 2 > MAX_BUILD:
            problems.append(f"{name} at y {my} is above the build height")
    cloud = (w.ids == 95) | (w.ids == B.GLASS)
    ys = np.nonzero(cloud.any(axis=(0, 2)))[0]
    if len(ys) and ys.min() <= MAX_BUILD:
        problems.append(f"a cloud comes down to y {ys.min()}, within the build height {MAX_BUILD}")
    houses = [r for r in F.records if r["kind"].startswith(("house", "delved", "the 0", "the 12", "the 45", "farmhouse", "the mill", "the keep"))]
    angles = sorted({round(r["heading"] % 90) for r in houses})
    print(f"{len(F.records)} buildings ({len(houses)} houses) and {len(F.trees)} trees audited on red's half")
    print(f"house headings, modulo 90 degrees: {angles}")
    print("\n".join(problems) if problems else "no placement problems found")


if __name__ == "__main__":
    main()
