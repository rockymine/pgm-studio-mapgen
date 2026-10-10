"""Walk the built Saltgate as the match unfolds. For each stage the gates of the stages already done are opened
in a copy of the built blocks (the same boxes map.xml fills with air) and, for the attackers, the defenders'
posterns are shut. Then each team's spawn for that stage is walked to that stage's objectives on foot, every drop
allowed; and before each stage the next objective is checked unreachable to the attackers.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import gen as G
import plan as P
import render_iso
import walk_core as W

POSTERNS = [(36, 37, 23, 25), (-38, -37, 23, 25)]


def world_at(ids, x0, z0, done, team):
    ids = ids.copy()
    for stage in done:
        for bx0, by0, bz0, bx1, by1, bz1 in G.GATE_REGIONS[stage]:
            ids[bx0 - x0:bx1 - x0 + 1, by0:by1 + 1, bz0 - z0:bz1 - z0 + 1] = 0
    if team == "attackers":
        for px0, px1, pz0, pz1 in POSTERNS:
            ids[px0 - x0:px1 - x0 + 1, 31:34, pz0 - z0:pz1 - z0 + 1] = 101   # shut to them, as the region is
    return ids


def walker(ids, x0, z0):
    passable, water, ladder, solid = W.grid(ids)
    st = W.standable(passable, water, solid) | (ladder & passable)
    return lambda start: W.bfs(st, ladder, water, passable, [start], x0, z0)


def spawn(team, stage):
    x, y, z, _ = P.SPAWNS[team][stage]
    return (int(np.floor(x)), y, int(np.floor(z)))


def at(d, x0, z0, p, r=2):
    v = W.nearest(d, x0, z0, *p, r=r)
    return "NOT REACHED" if v is None else str(v)


def main(build):
    x0, z0, ids0, dat = render_iso.load(build)
    out = []
    cp = P.CONTROL
    cpp = ((cp["box"][0] + cp["box"][1]) // 2, cp["y"] + 1, (cp["box"][2] + cp["box"][3]) // 2)
    mons = {m["key"]: (m["monument"][0], m["floor"] + 1, m["monument"][2] - 1) for m in P.MAGAZINES}
    wx, wy, wz = P.WOOL["at"]
    banner = (wx, wy, wz - 1)
    mx, my, mz = P.WOOL["monument"]
    slot = (mx, my, mz + 1)
    # before the warm-up ends, the attackers are on their ships
    w = walker(world_at(ids0, x0, z0, set(), "attackers"), x0, z0)
    out.append(f"warm-up: from the flagship the attackers reach the beach: {at(w(spawn('attackers', '1')), x0, z0, (0, 22, -40), 3)}")
    # stage A
    done = {"warmup"}
    wa = walker(world_at(ids0, x0, z0, done, "attackers"), x0, z0)
    wd = walker(world_at(ids0, x0, z0, done, "defenders"), x0, z0)
    da, dd = wa(spawn("attackers", "1")), wd(spawn("defenders", "1"))
    out.append(f"A, the Sea Gate: attackers {at(da, x0, z0, cpp, 3)}, defenders {at(dd, x0, z0, cpp, 3)}; the stores to the attackers "
               f"before it falls: " + ", ".join(f"{k} {at(da, x0, z0, p, 1)}" for k, p in mons.items()))
    # stage B
    done = {"warmup", "A"}
    wa = walker(world_at(ids0, x0, z0, done, "attackers"), x0, z0)
    wd = walker(world_at(ids0, x0, z0, done, "defenders"), x0, z0)
    da, dd = wa(spawn("attackers", "2")), wd(spawn("defenders", "2"))
    out.append("B, the Powder Stores: " + "; ".join(f"{k}: attackers {at(da, x0, z0, p, 1)}, defenders {at(dd, x0, z0, p, 1)}"
                                                     for k, p in mons.items()) +
               f"; the banner to the attackers before they fall: {at(da, x0, z0, banner, 1)}")
    # stage C
    done = {"warmup", "A", "B"}
    wa = walker(world_at(ids0, x0, z0, done, "attackers"), x0, z0)
    wd = walker(world_at(ids0, x0, z0, done, "defenders"), x0, z0)
    da, dd = wa(spawn("attackers", "3")), wd(spawn("defenders", "3"))
    carry = wa(banner)
    out.append(f"C, the Banner: attackers {at(da, x0, z0, banner, 1)}, defenders {at(dd, x0, z0, banner, 1)}; "
               f"the carry to the Sea Gate {at(carry, x0, z0, slot, 1)}; defenders to the Sea Gate {at(dd, x0, z0, slot, 1)}")
    # the three ways into the Sea Gate, each walked with the others shut
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
