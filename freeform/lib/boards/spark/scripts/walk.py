"""Read Spark back from the built blocks.

1. THE FLOOR. Every cell the plan says is floor is terracotta at y 64 with two blocks of air over it, or a block of
   cream stone the plan put there; every cell the plan says is void, the eye and the gaps between the rays, is open
   from the sky to below the kill height.
2. NOWHERE TO WAIT. Inside the clear ring nothing stands above the kill height but the spark itself and its
   underside, which lies wholly under the floor; so a knocked player falls past everything to the kill height.
3. THE SPAWNS. Every spawn point in map.xml stands on the floor with headroom.
4. THE SCENERY. The highest block of the mountains, and how far the nearest block above the kill height lies from
   the spark's furthest tip.

    python3 walk.py <build-dir>
"""
import math
import re
import sys

import numpy as np

import gen as G
import plan as P
import render_iso

FLOOR = {35, 159}                                                # the wool and its clay rim


def main(build):
    x0, z0, ids, dat = render_iso.load(build)
    out = []
    y = P.FLOOR_Y
    R = P.REACH
    bad_floor, bad_void, crates = [], [], 0
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            col = ids[x - x0, :, z - z0]
            if P.is_floor(x, z):
                h = P.crate_at(x, z)
                if col[y] not in FLOOR:
                    bad_floor.append((x, z, "no floor"))
                elif h:
                    crates += 1
                    if not (all(col[y + 1:y + 1 + h] == 24) and not col[y + 1 + h:].any()):
                        bad_floor.append((x, z, "crate"))
                elif col[y + 1:].any():
                    bad_floor.append((x, z, "something on it"))
            elif col[P.KILL_Y:].any():
                bad_void.append((x, z))
    out.append(f"the floor: {len(bad_floor)} plan floor cells wrong {bad_floor[:5]}; {crates} crate columns as planned; "
               f"{len(bad_void)} plan void cells with anything over the kill height {bad_void[:5]}")

    # anything above the kill height inside the clear ring that is not the spark's own column
    sx, sy, sz = ids.shape
    xs, zs = np.meshgrid(np.arange(x0, x0 + sx), np.arange(z0, z0 + sz), indexing="ij")
    high = ids[:, P.KILL_Y + 1:, :].any(axis=1)
    spark = np.vectorize(P.is_floor)(xs, zs) if False else np.zeros_like(high)
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            spark[x - x0, z - z0] = P.is_floor(x, z)
    r = np.hypot(xs, zs)
    stray = np.argwhere(high & ~spark & (r < G.CLEAR))
    out.append(f"nowhere to wait: {len(stray)} columns inside {G.CLEAR} of the centre with anything over the kill height "
               f"but the spark's own")
    under_ok = True
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            if P.is_floor(x, z):
                col = ids[x - x0, P.KILL_Y + 1:y, z - z0]
                nz = np.nonzero(col)[0]
                if len(nz) and (nz.max() != len(col) - 1 or len(nz) != nz.max() - nz.min() + 1):
                    under_ok = False                             # the underside hangs in one piece from the floor
    out.append(f"the underside hangs in one piece under every floor cell: {under_ok}")

    xml = open("map.xml").read()
    pts = re.findall(r'<point yaw="[-\d]+">([-\d.]+),(\d+),([-\d.]+)</point>', xml)
    bad = []
    for px, py, pz in pts:
        bx, by, bz = math.floor(float(px)), int(py), math.floor(float(pz))
        if not (ids[bx - x0, by - 1, bz - z0] in FLOOR and ids[bx - x0, by, bz - z0] == 0 and ids[bx - x0, by + 1, bz - z0] == 0):
            bad.append((px, py, pz))
    out.append(f"the spawns: {len(pts)} points, {len(bad)} not standing on the floor with headroom {bad}")

    tips = max(math.hypot(x, z) for x in range(-R, R + 1) for z in range(-R, R + 1) if P.is_floor(x, z))
    above = np.argwhere(high & ~spark)
    near = min(math.hypot(i + x0, k + z0) for i, k in above) if len(above) else None
    top = int(np.nonzero(ids.any(axis=(0, 2)))[0].max())
    out.append(f"the scenery: the highest block at y {top}; the nearest block over the kill height lies "
               f"{near - tips:.0f} blocks beyond the furthest tip, against a sprinting knockback-ten hit's "
               f"reach of {P.knock(10):.0f}")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
