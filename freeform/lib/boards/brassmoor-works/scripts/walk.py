"""Read Brassmoor Works back from the built world: the objectives and the wools in their rooms, every block's
footing, ground over the kill height off the decks, and from each spawn on foot and by building.

    on foot     the world as built: the spawn's own monuments, and that neither its own rooms nor the enemy's
                are reached (its own are walled off by rule, the enemy's by the band and the bedrock lines)
    building    pgmvox.walk with MoveRules(build=...): a player may stand in the air of a build zone or over a
                bedrock line, between the kill height and the build height

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox.objectives import DYES, Spawn, Wool

t0 = time.time()
w = World.load(sys.argv[1])
R = P.build()
O = P.objectives()
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
missing = [o.color for o in O.of(Wool) if w.get(*o.found) != (B.WOOL, DYES[o.color])]
out.append(f"wools missing from their rooms: {len(missing)} {missing if missing else ''}")
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
kinds = {}
for x, y, z, why in foot:
    kinds.setdefault(why, []).append((x, y, z))
for why, cells in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
    out.append(f"   {len(cells):4d}  {why}  e.g. {cells[:3]}")
X, Z = w.grid()
decks = R.piece != R.kinds["void"]
stand = walk.no_stand_above(w, P.KILL_Y, np.ones(X.shape, bool), decks)
out.append(f"columns off the decks with ground over the kill height: {len(stand)} {stand[:6]}")

mask = P.zone_mask(R) | P.wall_mask(R)
foot_rules = walk.MoveRules(max_drop=3, kill_y=P.KILL_Y)
build_rules = walk.MoveRules(max_drop=3, kill_y=P.KILL_Y, build=(mask, (P.KILL_Y + 1, P.MAX_BUILD)))
for o in O.of(Spawn):
    team, at = O.teams.short(o.team), o.at
    d = walk.walk(w.ids, [at], w.x0, w.z0, foot_rules)
    db = walk.walk(w.ids, [at], w.x0, w.z0, build_rules)
    out.append(f"from {team}'s spawn {at}: {int((d >= 0).sum())} places on foot")
    for wl in O.of(Wool):
        if wl.team == o.team:
            v = walk.nearest(d, w.x0, w.z0, *wl.slot, r=1)
            out.append(f"  on foot to its own {wl.color} monument: {v if v is not None else 'NOT REACHED'}")
            v = walk.nearest(d, w.x0, w.z0, *wl.found, r=2)
            vb = walk.nearest(db, w.x0, w.z0, *wl.found, r=2)
            out.append(f"  to the enemy's {wl.color} wool: on foot {v if v is not None else 'not reached'}; "
                       f"building {vb if vb is not None else 'NOT REACHED'}")
        else:
            v = walk.nearest(d, w.x0, w.z0, *wl.found, r=2)
            out.append(f"  on foot into its own room, to the {wl.color} wool: {v if v is not None else 'not reached'}"
                       f" (the rule keeps it out; the walk does not know the rule)")
out.append(f"[{time.time() - t0:.0f}s]")
print("\n".join(out))
