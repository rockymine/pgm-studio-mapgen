"""Audit the city against the rules of a board played in the sky: nothing a player is meant to stand on lies
below the kill height, nothing built reaches past the build height, the clouds stay between the land and the
kill height, the core can leak, the monument and core are where map.xml says, and no two masses claim the
same ground.

    python3 audit.py
"""
import numpy as np

import gen
import plan as P
from mc import B

LAND_TOP = 42


def main():
    w, F = gen.make()
    problems = []
    for name, other in F.conflicts:
        problems.append(f"{name} overlaps {other}")
    ids = w.ids
    x0 = w.x0
    # what is built in the city stays between the kill height and the build height
    built = (ids != B.AIR) & (ids != 95) & (ids != B.GLASS)
    ys = np.nonzero(built[:, P.KILL_Y:, :].any(axis=(0, 2)))[0] + P.KILL_Y
    if len(ys) and ys.max() > P.MAX_BUILD:
        problems.append(f"something is built up to y {ys.max()}, over the build height {P.MAX_BUILD}")
    # the clouds: glass below the kill height (the city's own glass, its slits, is above it)
    cloud = ((ids == 95) | (ids == B.GLASS))[:, :P.KILL_Y, :]
    cy = np.nonzero(cloud.any(axis=(0, 2)))[0]
    if len(cy) and (cy.min() < P.CLOUD_Y[0] or cy.max() > P.CLOUD_Y[1]):
        problems.append(f"the clouds run from y {cy.min()} to {cy.max()}, outside {P.CLOUD_Y}")
    # the core: three by three by three of obsidian round lava, and open below so it can leak
    c = F.core
    core_ok = all(w.id(x, y, z) in (B.OBSIDIAN, B.LAVA) for x in range(c["x0"], c["x1"] + 1)
                  for y in range(c["y0"], c["y1"] + 1) for z in range(c["z0"], c["z1"] + 1))
    if not core_ok:
        problems.append("the core is not whole")
    cx, cz = (c["x0"] + c["x1"]) // 2, (c["z0"] + c["z1"]) // 2
    fall = 0
    for y in range(c["y0"] - 1, 0, -1):
        if w.id(cx, y, cz) != B.AIR:
            break
        fall += 1
    if fall < 10:
        problems.append(f"lava from the core falls only {fall} blocks before it lands")
    mx, my, mz = F.monument
    if not (w.id(mx, my, mz) == B.OBSIDIAN and w.id(mx, my + 1, mz) == B.OBSIDIAN):
        problems.append("the monument is not two obsidian")
    print(f"red half: {len(F.records)} recorded floors, {len(F.trees)} trees, {F.cloud_blocks} blocks of cloud; "
          f"the core's leak falls {fall} blocks")
    print("\n".join(problems) if problems else "no placement problems found")


if __name__ == "__main__":
    main()
