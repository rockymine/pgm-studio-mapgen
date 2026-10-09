"""Brittlebush III: capture the wool for four teams, one wool each, from the plan its author drew in the studio's
planner (plan.json, saved from the map untitled-plan-8, "Brittebush III"), built in the Brittlebush style.

The plan is one team's part, turned a quarter three times (rot_90). pgmvox.studioplan reads it as the author drew
it: a later piece lies over an earlier one, a piece named stair... is a stair cell, and a piece named double... is a
deck, open beneath it where UNDER says. Where no piece lies, a zone named water... is water ground and any other
zone a bare build zone, cobwebs on its outline toward the void. Heights are the plan's own (LIFT 0): the lowest decks
stand at 9, and their lower floors run into the floor of the world at 1.

    cells()         the whole board: ({cell: Cell}, {cell: the team whose part it is})
    objectives()    four teams; each keeps one wool in its room and captures the other three
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import brittle as BR  # noqa: E402
from pgmvox import studioplan as SP  # noqa: E402
from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Symmetry  # noqa: E402

BOARD = "brittlebush-iii"
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = SP.load(os.path.join(HERE, "..", "plan.json"))
LIFT = 0                                    # the plan's own heights: the lowest decks at 9, their lower floors at 1
# the cells open under the double-layered pieces' decks, Brittlebush I's under-sections: the middle island hollow
# one cell deep along its side toward the centre; a tunnel through the middle of the two-by-three island, open to
# the water at both ends; the wool's approach island hollow along its side toward the lane
UNDER = {(-2, -3), (-1, -3), (-2, -8), (-2, -7), (-2, -11), (-1, -11)}
SYM = Symmetry("rot_90")
TEAMS = [("red-team", "Red", "red", 12), ("blue-team", "Blue", "blue", 12), ("green-team", "Green", "green", 12),
         ("yellow-team", "Yellow", "yellow", 12)]
DYES = [14, 11, 13, 4]                      # the teams' clay and wool
KEEPS = ["yellow", "orange", "pink", "purple"]   # the wool each team keeps, the colours of Brittlebush II's
KEEP_DYES = [4, 1, 6, 10]
MAX_BUILD = 40


def cells():
    unit = SP.unit(PLAN, lift=LIFT, under=UNDER)
    return BR.fan(unit)


def extent(cs):
    xs = [c[0] for c in cs]
    zs = [c[1] for c in cs]
    r = max(max(xs) + 1, -min(xs), max(zs) + 1, -min(zs))
    return -r * BR.CELL, r * BR.CELL - 1


SPAWN_AT, SPAWN_BOX, SPAWN_REC = SP.placement(PLAN, "spawns", LIFT)[0]
WOOL_AT, _, WOOL_REC = SP.placement(PLAN, "wools", LIFT)[0]
# the wool's house takes its whole piece, two cells by two, as Brittlebush I's do: the first storey all four cells,
# the second an L lacking the front cell toward the centre, where the door is, and one cell on top behind it
_wx, _wz, _ww, _wh = next(p for p in PLAN["pieces"] if p["id"] == WOOL_REC["piece"])["rect"]
WOOL_BOX = (_wx * BR.CELL, _wz * BR.CELL, (_wx + _ww) * BR.CELL - 1, (_wz + _wh) * BR.CELL - 1)
WOOL_LAYERS = [[(_wx, _wz), (_wx + 1, _wz), (_wx, _wz + 1), (_wx + 1, _wz + 1)],
               [(_wx, _wz), (_wx + 1, _wz), (_wx + 1, _wz + 1)],
               [(_wx, _wz)]]
WOOL_DOOR = ((_wx, _wz + 1), "s")
SPAWN_DOOR = SP.facing(SPAWN_REC)          # the side the spawn house opens on: west, toward the lane
SPAWN_Y = SPAWN_AT[1]                       # the keep's floor
WOOL_Y = WOOL_AT[1]                         # the wool room's floor
# red's three monuments, on the ground south of its keep (piece-9), a slot for each wool it takes
MONUMENTS = [(32, -36), (35, -36), (38, -36)]


def turned(p, k):
    x, z = p
    for _ in range(k):
        x, z = SYM.point(x, z)
    return int(x), int(z)


def turned_box(box, k):
    x0, z0, x1, z1 = box
    a, b = turned((x0, z0), k), turned((x1, z1), k)
    return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])


def room(k):
    """Team k's wool room: inside the walls of the building on the wool's footprint."""
    x0, z0, x1, z1 = turned_box(WOOL_BOX, k)
    return Box(x0 + 1, WOOL_Y + 1, z0 + 1, x1 - 1, WOOL_Y + 5, z1 - 1)


def objectives():
    """Four teams spawning in their keeps; each team's wool in its room, captured by the other three at their
    monuments."""
    O = Objectives(Teams(*TEAMS))
    yaw = {"w": 90, "e": 270, "n": 180, "s": 0}[SPAWN_DOOR]
    for k, (team, *_) in enumerate(TEAMS):
        x, z = turned((SPAWN_AT[0], SPAWN_AT[2]), k)
        bx0, bz0, bx1, bz1 = turned_box(SPAWN_BOX, k)
        O.add(Spawn(team, (x, SPAWN_Y + 1, z), yaw=(yaw + 90 * k) % 360, kit="spawn-kit",
                    area=Box(bx0, 0, bz0, bx1, 127, bz1)), mirror=False)
    for k, (taker, *_) in enumerate(TEAMS):
        others = [j for j in range(4) if j != k]
        for n, j in enumerate(others):
            sx, sz = turned(MONUMENTS[n], k)
            fx, fz = turned((WOOL_AT[0], WOOL_AT[2]), j)
            O.add(Wool(taker, KEEPS[j], slot=(sx, SPAWN_Y + 1, sz), found=(fx, WOOL_Y + 1, fz), room=room(j),
                       keeper=TEAMS[j][0]), mirror=False)
    O.add(Observer((0, 50, 0)), mirror=False)
    return O
