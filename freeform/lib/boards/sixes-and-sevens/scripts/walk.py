"""Walk Sixes and Sevens as built, on foot and placing nothing: from each spawn, the moves to every monument, to the
upper floor and to the shelf, and the four goal walks against the plan's bands.

    python3 walk.py <build-dir>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import plan as P  # noqa: E402
from pgmvox import World  # noqa: E402
from pgmvox.read.walk import MoveRules, nearest, walk  # noqa: E402

w = World.load(sys.argv[1])
sym = P.SYM.point
rules = MoveRules(max_drop=None, kill_y=P.LAVA + 1)
spawn = {"red": (*P.SPAWN,), "blue": tuple(int(v) for v in sym(*P.SPAWN))}
places = {"red reactor": (*P.REACTOR, P.FIELD + 1), "red pump": (*P.PUMP, P.FIELD + 1),
          "red gallery": (-68, P.UPPER + 1, 0), "red corridor": (-78, P.UPPER + 1, 20), "shelf": (-10, P.SHELF + 1, 75)}
for k in ("red reactor", "red pump", "red gallery", "red corridor"):
    x, z, y = places[k] if len(places[k]) == 3 and k.endswith(("reactor", "pump")) else (places[k][0], places[k][2], places[k][1])
    bx, bz = (int(v) for v in sym(x, z))
    places[k.replace("red", "blue")] = (bx, y, bz)
for k in list(places):
    if k.endswith(("reactor", "pump")) and len(places[k]) == 3 and places[k][2] == P.FIELD + 1:
        x, z, y = places[k]
        places[k] = (x, y, z)

dist = {}
for team, (x, z) in spawn.items():
    dist[team] = walk(w.ids, [(x, P.FIELD + 1, z)], w.x0, w.z0, rules)


def moves(team, place, r=2):
    x, y, z = place
    return nearest(dist[team], w.x0, w.z0, x, y, z, r)


print("moves from each spawn, on foot, placing nothing:")
for name, place in places.items():
    print(f"  {name:14s} {str(place):18s} red {moves('red', place)!s:>5}   blue {moves('blue', place)!s:>5}")
print()
for team, other in (("red", "blue"), ("blue", "red")):
    for goal in ("reactor", "pump"):
        own, enemy = moves(team, places[f"{team} {goal}"]), moves(other, places[f"{team} {goal}"])
        ratio = f"{enemy / own:.2f}" if own and enemy else "-"
        print(f"  {team} {goal}: own spawn {own} (40 to 90), enemy over own {ratio} (3 to 4)")
