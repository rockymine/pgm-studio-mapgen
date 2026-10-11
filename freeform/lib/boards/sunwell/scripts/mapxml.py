"""Write Sunwell's map.xml from the plan: every hill's box, the spawn shelf, the spring, the water the board is built
with (which nobody may scoop up), all from the plan's own numbers. Every box here is (x0, y0, z0, x1, y1, z1) with
an exclusive max, as a PGM cuboid reads it.

    python3 mapxml.py > map.xml
"""
import os
import sys

import gen as G
import plan as P

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from pgmvox.play.objectives import Box, Objectives, Observer, Portal, Spawn, TouchPoint  # noqa: E402
from pgmvox.play.rules import Build, Effect, Item, Kit, Map, Match, Zone, terrain_of  # noqa: E402


def box(b):
    """An exclusive-max box as the library's inclusive one."""
    x0, y0, z0, x1, y1, z1 = b
    return Box(x0, y0, z0, x1 - 1, max(y1 - 1, y0), z1 - 1)


def hill_boxes():
    """(id, name, points, (x0, y0, z0, x1, y1, z1)) for every hill: five by five, from two under the shelf's top to
    three over it, so a swimmer in its pool and a runner over it both touch it."""
    out = []
    n = 0
    for k, d in enumerate(P.DROPS):
        y = P.ISLET["y"] if d.get("lake") else P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.hills(k):
            n += 1
            za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
            pts = P.POINTS["last" if d.get("lake") else "hill"]
            label = f"{name.replace('the ', '').title()}" + ("" if sd == "middle" else f" ({sd})")
            out.append((f"hill-{n}", f"{k + 1}. {label}", pts, (x0, y - 2, za, x1 + 1, y + 4, zb + 1)))
    return out


def built_water():
    """Boxes over the water the board is built with: pools, basins, falls, streams, the lake."""
    out = []
    for k, d in enumerate(P.DROPS):
        if d.get("lake"):
            continue
        y = P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.pools(k) + P.falls(k):
            za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
            out.append((x0, y - 3, za, x1 + 1, y + 1, zb + 1))
        for name, x0, x1, s0, s1, sd in P.falls(k):
            za, zb = sorted((P.z_of(k, 1), P.z_of(k, 2)))
            out.append((x0, y, za, x1 + 1, P.shelf_y(k) + 1, zb + 1))
            ze = P.EDGE if P.side(k) == "N" else -P.EDGE
            zs = sorted((ze, ze + (-5 if P.side(k) == "N" else 5)))
            out.append((x0, P.shelf_y(k) - 1, zs[0], x1 + 1, P.shelf_y(k) + 1, zs[1] + 1))
    out.append((-G.R - 4, G.LAKE_FLOOR, -G.R - 4, G.R + 5, P.LAKE_Y + 1, G.R + 9))
    return out


def main():
    sx0, sx1 = P.SPAWN["x"]
    sz0, sz1 = P.SPAWN["z"]
    top = P.TOP + 1
    shelf = box((sx0, top, sz0, sx1 + 1, top, sz1 + 1))                    # where players come in
    x0, x1 = P.SPRING["x"]
    z0, z1 = P.SPRING["z"]
    O = Objectives()
    O.add(Spawn(None, (sx0, top, sz0), kit="players", spread=shelf))
    O.add(Observer((0, P.TOP + 12, -15)))
    O.add(Zone("spawn-shelf", [box((-32, P.TOP - P.THICK, -32, 32, 256, 32))], place=False, damage=False))
    O.add(Zone("built-water", [box(b) for b in built_water()], place=False, break_=False,
               message="This water belongs to the well."))
    O.add(Portal("spring", box((x0, P.LAKE_Y - 2, z0 + 1, x1 + 1, P.LAKE_Y + 4, z1 + 5)), yaw=0, to_box=shelf))
    for hid, name, pts, b in hill_boxes():
        O.add(TouchPoint(hid, name, box(b), points=pts))
    kit = Kit(*[Item("water bucket", slot, locked=True, name="`b`lWater Drop") for slot in range(3)],
              id="players", clear=True, effects=[Effect("resistance", "3s", 5), Effect("health boost", "oo", -2)],
              game_mode="survival", remove=["bucket"])
    M = Map("Sunwell", "1.0.0", "Drop down the sinkhole and hold the most hills when the clock runs out.", "arcade",
            terrain=terrain_of(__file__),
            includes=[], players=(1, 40),
            rules=["Every drop kills unless it ends in water: hit a pool, place a bucket, or ride the falls.",
                   "Touch a hill to take it; it scores for you until someone else touches it, even after you die.",
                   "The spring in the lake takes you back to the top."],
            objectives=O, kit=kit,
            build=Build(only=("water", "stationary water"), physics=False),
            match=Match(time=int(P.TIME.rstrip("m")) * 60))
    print(M.xml())


if __name__ == "__main__":
    main()
