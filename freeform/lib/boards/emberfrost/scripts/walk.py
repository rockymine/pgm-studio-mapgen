"""Read Emberfrost back from the built world: the objectives check clean, every block has its footing, water stands against nothing that is
not a bank, and each team reaches both of its own cores and both of the enemy's on foot and by the caves, the three crossings and the
gorge's floor.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World
from pgmvox.core import blocks as K
from pgmvox.play.objectives import Core, Spawn
from pgmvox.read import audit, walk

w = World.load(sys.argv[1])
O = P.objectives()
spawns = {o.team: o.at for o in O.of(Spawn)}
cores = O.of(Core)
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:12]]
loose = audit.loose_water(w)
out.append(f"water against air (audit.loose_water): {len(loose)}")
out += [f"   {f}" for f in loose[:8]]

ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0
rules = walk.MoveRules(max_drop=3, jumps=False)
jump_rules = walk.MoveRules(max_drop=None, jumps=True, max_gap=3)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(ids, [at], w.x0, w.z0, rules)
    d[:, :P.KILL_Y + 1, :] = -1
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in cores:
        b = o.box
        cx, cz = (b.x0 + b.x1) // 2, (b.z0 + b.z1) // 2
        floor = (P.land.RIME_LEVEL if "rime" in o.id else P.land.FORGE_LEVEL)
        best = None
        for r in (3, 5, 7):
            v = walk.nearest(d, w.x0, w.z0, cx, floor + 1, cz, r=r)
            if v is not None:
                best = (r, v)
                break
        mine = "its own" if o.team == team else "the enemy's"
        out.append(f"  on foot to {mine} {o.id}: {best[1] if best else 'NOT REACHED'}" + (f" (within {best[0]})" if best else ""))

d = walk.walk(ids, [P.SPAWN_AT], w.x0, w.z0, rules)
d[:, :P.KILL_Y + 1, :] = -1
spots = [("Blue Cave mouth", (-44, 65, -37)), ("Blue Cave hall", (-47, 63, -55)), ("Blue Cave undercroft", (-35, 65, -50)),
         ("Slag Run mouth", (29, 66, -36)), ("Slag Run hall", (36, 55, -54)), ("Forge undercroft", (40, 55, -60)),
         ("Frostspan, north end", (-41, 66, -16)), ("Frostspan, middle", (-41, 66, -1)), ("Frostspan, south end", (-41, 66, 16)),
         ("Cinder Span, middle", (0, 65, -1)), ("Cinder Span, south end", (0, 65, 16)),
         ("Brimstone Bridge, middle", (40, 65, -1)), ("Brimstone Bridge, south end", (40, 65, 16)),
         ("the bar under the Cinder Span", (0, 50, 0)), ("the Shingle, west bank", (-30, 48, -5)), ("Beacon Hill's crown", (4, 74, -37)),
         ("the Mirror's shore", (-36, 65, -28)), ("Forge plinth", (40, 67, -50)), ("Rime plaza, south", (-35, 73, -43)),
         ("blue's spawn", P.SPAWN_AT[:1] + (67,) + (75,))]
for name, (x, y, z) in spots:
    v = walk.nearest(d, w.x0, w.z0, x, y, z, r=2)
    out.append(f"  red's spawn to {name}: {v if v is not None else 'NOT REACHED'}")
dj = walk.walk(ids, [P.SPAWN_AT], w.x0, w.z0, jump_rules)
dj[:, :P.KILL_Y + 1, :] = -1
out.append(f"places reached with every running jump and any drop: {int((dj >= 0).sum())} (on foot {int((d >= 0).sum())})")
print("\n".join(out))
