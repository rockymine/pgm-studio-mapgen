"""Write Lantern Drop's map.xml from the plan and the generator: the hills' boxes, the bell court, the slipway, the
board's own water that nobody may scoop up, and the void that kills, all from the plan's own numbers. Every box
here is (x0, y0, z0, x1, y1, z1) with an exclusive max, as a PGM cuboid reads it.

    python3 mapxml.py > map.xml
"""
import os
import sys

import gen as G
import plan as P

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

from pgmvox.play.objectives import Box, Objectives, Observer, Portal, Spawn, TouchPoint  # noqa: E402
from pgmvox.play.rules import Build, Effect, Item, KillHeight, Kit, Map, Match, Zone  # noqa: E402


def box(b):
    """An exclusive-max box as the library's inclusive one."""
    x0, y0, z0, x1, y1, z1 = b
    return Box(x0, y0, z0, x1 - 1, max(y1 - 1, y0), z1 - 1)


def hill_boxes():
    out = []
    n = 0
    for p in P.pieces():
        if not p[8].get("hill"):
            continue
        n += 1
        hx0, hx1, hz0, hz1 = G.hill_box(p)
        y = p[7]
        pts = P.POINTS["last" if p[8].get("last") else "hill"]
        label = p[1].replace("the ", "").title() + ("" if p[9] == "middle" else f" ({p[9]})")
        out.append((f"hill-{n}", label, pts, (hx0, y - 2, hz0, hx1 + 1, y + 4, hz1 + 1)))
    return out


def kill_boxes():
    """Under each group of pieces: the course's width, from the previous group's far edge (the court's own near
    edge for the first) to this group's far edge, from the world's floor to five under the group's top; the
    harbour's under its floor."""
    groups = {}
    for p in P.pieces():
        groups.setdefault(p[0], []).append(p)
    out, z_from = [], None
    for i in sorted(groups):
        g = groups[i]
        z0, z1, y = min(p[5] for p in g), max(p[6] for p in g), g[0][7]
        top = y - 5
        if g[0][8].get("harbour"):
            z1, top = P.HARBOUR["z"][1], min(top, P.HARBOUR["y"] - 8)
        out.append((-40, 0, (z0 - 10) if z_from is None else z_from, 40, top, z1))
        z_from = z1 + 1
    return out


def built_water():
    out = []
    for p in P.pieces():
        if "water" in p[8]:
            a0, a1, b0, b1 = p[8]["water"]
            out.append((a0, p[7] - 3, b0, a1 + 1, p[7] + 1, b1 + 1))
    h = P.HARBOUR
    out.append((h["x"][0], h["y"] - 6, h["z"][0], h["x"][1] + 1, h["y"] + 1, h["z"][1] + 1))
    return out


def main():
    court = [p for p in P.pieces() if p[8].get("spawn")][0]
    cx0, cx1, cz0, cz1, cy = court[3], court[4], court[5], court[6], court[7]
    floor = box((cx0 + 3, cy + 1, cz0 + 7, cx1 - 2, cy + 1, cz1 - 2))     # where players and observers come in
    s, hy = P.SLIPWAY, P.HARBOUR["y"]
    O = Objectives()
    O.add(Spawn(None, (cx0 + 3, cy + 1, cz0 + 7), kit="players", spread=floor))
    O.add(Observer((cx0 + 3, cy + 1, cz0 + 7), spread=floor))
    O.add(Zone("bell-court", [box((cx0 - 2, cy - 4, cz0 - 4, cx1 + 3, cy + 12, cz1 + 2))], place=False, damage=False))
    O.add(Zone("built-water", [box(b) for b in built_water()], place=False, break_=False,
               message="This water belongs to the pass."))
    O.add(Portal("slipway", box((s["x"][0], hy - 3, s["z"][0], s["x"][1] + 1, hy + 4, s["z"][1] + 2)), yaw=0,
                 to_box=floor))                                             # the harbour back to the bell court
    for hid, name, pts, b in hill_boxes():
        O.add(TouchPoint(hid, name, box(b), points=pts))
    minutes = int(P.TIME.rstrip("m"))
    # the kit, the water rule and the void are Water Drop: Limbo II's: boots of Protection V soften a landing the
    # bucket's water reached a tick late, and a player in the void has one heart
    kit = Kit(*[Item("water bucket", slot, locked=True, name="`b`lWater Drop") for slot in range(3)],
              Item("leather boots", color="7fcc19", locked=True, unbreakable=True,
                   enchant=[("protection environmental", 5)], wear="boots"),
              id="players", clear=True, effects=[Effect("resistance", "2s", 5), Effect("health boost", amplifier=-2)],
              game_mode="survival", remove=["bucket"])
    M = Map("Lantern Drop", "1.0.0", "Drop down the broken pass and hold the most hills when the clock runs out.",
            "arcade", includes=["void-death"], players=(1, 40),
            rules=["A drop of nineteen kills unless it ends in water: a cistern, the paddies, the harbour or your "
                   "bucket.", "Touch a hill to take it; it scores for you until someone else touches it, even after "
                   "you die.", "The slipway in the harbour takes you back to the bell court."],
            objectives=O, kit=kit,
            build=Build(only=("water", "stationary water"), physics=False),   # a bucket's water, never the world's
            # a box under every landing: a player who misses it falls in and is put under the world
            kill=[KillHeight(boxes=[box(b) for b in kill_boxes()], to=-150), KillHeight(-5, "portal")],
            match=Match(time=minutes * 60))
    print(M.xml())


if __name__ == "__main__":
    main()
