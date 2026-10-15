"""Sunwell — a water drop plan: hills held on the way down a jungle sinkhole two hundred deep, every player against
every other.

Every player spawns on the top shelf with three water buckets, sixteen health and their fists. Nine rock shelves jut
from alternate sides of the shaft, twenty-two apart; each overhangs the next by five, so a player drops off a
shelf's edge onto the shelf below, walks back under it to that shelf's edge, and drops again. A fall of twenty-two
kills unless it ends in water. The board is two descents, left and right, mirror images of each other, that meet
on the middle of three shelves.

On the way down are hills: a box at a landing, taken the moment a player touches it and held, scoring every
second, until another player touches it, whether or not the holder is still alive. Each side's landings carry a
hill of their own; the shelves where the sides meet carry one hill both sides want; and an islet in the lake at the
foot carries the last hill, worth three times the others. From the lake the spring at its far side sends a player
back to the top. The most points when the clock runs out wins.

Every drop offers the same choices in different places, on each side:

    a pool        water set into the shelf below, near the edge and small, or far and only reached by a sprint
                  jump: safe if it is hit, death if it is missed
    the bucket    the bare shelf: place water under you before you land
    the falls     a waterfall down the side wall into a basin: safe and slow
    a shaft       on three shelves, a hole through the shelf below over a pool two shelves down: two drops in one

The plan is the shaft, the shelves with their pools, holes, falls and hills, given for the left side and mirrored,
and a fall model: Minecraft's own per-tick physics for a body stepping, running or sprint-jumping off an edge.

    y is the top of a shelf, the block a player stands on: 236 the top, then every twenty-two down to 60; the
    lake's surface 38, the islet 40
"""
import math

R_SHAFT = 21                                   # the shaft's radius, to the face of its walls
TOP = 236
DROP = 22
N_SHELVES = 9
LAKE_Y = 38
ISLET = dict(x=(-3, 3), s=(4, 10), y=40)       # in the last drop's frame
SPRING = dict(x=(-4, 4), z=(17, 21))           # the lake's far side: back to the top
EDGE = 2                                       # a north shelf's edge at z +2, a south shelf's at z -2
THICK = 4
HEALTH = 16                                    # twenty, less two hearts
SPEED = 5.6                                    # a sprint, blocks a second
HILL = 5                                       # a hill's box: five by five by five
POINTS = dict(hill=1, last=3)                  # points a second to the holder
TIME = "5m"


def shelf_y(k):
    return TOP - DROP * k


def side(k):
    """'N': the shelf runs from the north wall to z +2 and drops to the south; 'S' the other way."""
    return "N" if k % 2 == 0 else "S"


def in_shaft(x, z):
    """Inside the shaft's wall: a circle on the middle of block (0, 0), so the left side is the right's mirror."""
    return x ** 2 + z ** 2 <= R_SHAFT ** 2


def on_shelf(k, x, z):
    if not in_shaft(x, z):
        return False
    return z <= EDGE if side(k) == "N" else z >= -EDGE


def z_of(k, s):
    """The z of a block s beyond shelf k's edge, along the fall."""
    return EDGE + s if side(k) == "N" else -EDGE - s


# Each drop k, off shelf k onto shelf k + 1, in the drop's own frame: s from the edge along the fall, x across.
# Left-side things are given with x < 0 and mirrored to the right; a thing spanning x 0 is the middle's, one only.
#   pools  (name, x0, x1, s0, s1)        shaft (x0, x1, s0, s1): a hole in shelf k + 1 over a pool on shelf k + 3
#   hills  (name, x0, s0): a 5 x 5 box at the landing, from (x0, s0)
DROPS = [
    dict(pools=[("the near pool", -5, -3, 1, 3), ("the far pool", -11, -7, 7, 10)],
         hills=[("the far pool", -11, 6)]),
    dict(pools=[("the near pool", -9, -7, 1, 3), ("the sun pool", -2, 2, 4, 8)],
         hills=[("the sun pool", -2, 4)], shaft=(-12, -10, 8, 10)),
    dict(pools=[("the near pool", -4, -2, 2, 4), ("the far pool", -12, -8, 8, 11)],
         hills=[("the near pool", -5, 1)]),
    dict(pools=[], hills=[("the bare rock", -2, 2)]),                  # the shaft's pools either side
    dict(pools=[("the near pool", -3, -1, 1, 3), ("the far pool", -10, -6, 7, 10)],
         hills=[("the far pool", -10, 6)], shaft=(-14, -12, 5, 7)),
    dict(pools=[("the near pool", -9, -7, 1, 3), ("the moon pool", -2, 2, 4, 7)],
         hills=[("the moon pool", -2, 3)]),
    dict(pools=[("the far pool", -7, -5, 9, 11)], hills=[("the shaft's pool", -16, 4)]),
    dict(pools=[("the near pool", -4, -2, 1, 3), ("the middle pool", -10, -6, 5, 8)],
         hills=[("the middle pool", -10, 4)], shaft=(-8, -6, 11, 13)),
    dict(pools=[], hills=[("the islet", -2, 5)], lake=True),
]
FALLS_X = 17                                   # the falls run down both side walls on every drop
FALLS_SPEED = 4.0                              # blocks a second, riding falling water down
SHAFT_POOL_MARGIN = 2
SPAWN = dict(x=(-4, 4), z=(-17, -11))


def mirror(x0, x1):
    return -x1, -x0


def both(items, xi=1):
    """Left-side items and their mirrors; an item spanning x 0 is the middle's, once."""
    out = []
    for it in items:
        it = list(it)
        x0, x1 = it[xi], it[xi + 1]
        if x0 <= 0 <= x1:
            out.append(tuple(it) + ("middle",))
            continue
        out.append(tuple(it) + ("left",))
        m = list(it)
        m[xi], m[xi + 1] = mirror(x0, x1)
        out.append(tuple(m) + ("right",))
    return out


def pools(k):
    """Drop k's pools on both sides, with the pools of the shafts cut two drops earlier."""
    out = both(DROPS[k]["pools"])
    if k >= 2 and "shaft" in DROPS[k - 2]:
        x0, x1, s0, s1 = DROPS[k - 2]["shaft"]
        m = SHAFT_POOL_MARGIN
        out += both([("the shaft's pool", x0 - m, x1 + m, s0 - m, s1 + m)])
    return out


def shafts(k):
    if "shaft" not in DROPS[k]:
        return []
    return both([("the shaft",) + DROPS[k]["shaft"]])


def hills(k):
    """Drop k's hills: (name, x0, x1, s0, s1, which side)."""
    return both([(name, x0, x0 + HILL - 1, s0, s0 + HILL - 1) for name, x0, s0 in DROPS[k]["hills"]])


def falls(k):
    """The falls' basins on shelf k + 1: four wide against each side wall, one to four out."""
    if DROPS[k].get("lake"):
        return []
    return [("the falls", -FALLS_X - 3, -FALLS_X, 1, 4, "left"), ("the falls", FALLS_X, FALLS_X + 3, 1, 4, "right")]


def gaps(k):
    """Where a player can leave shelf k: its edge is walled by a rim except over its targets."""
    if DROPS[k].get("lake"):
        return [("the lake", -R_SHAFT, R_SHAFT, 1, "middle")]
    out = [("pool", x0 - 1, x1 + 1, s0, sd) for name, x0, x1, s0, s1, sd in pools(k)]
    out += [("shaft", x0 - 1, x1 + 1, s0, sd) for name, x0, x1, s0, s1, sd in shafts(k)]
    out += [("falls", x0, x1, s0, sd) for name, x0, x1, s0, s1, sd in falls(k)]
    out += [("hill", x0, x1, s0, sd) for name, x0, x1, s0, s1, sd in hills(k)
            if not any(p[1] <= x0 and x1 <= p[2] for p in pools(k))]   # an opening over a hill on bare rock
    return out


# ---- the fall model -----------------------------------------------------------------------------------------
LEAVES = {  # how a player leaves an edge: (horizontal speed, vertical speed, air acceleration) per tick
    "step off": (0.13, 0.0, 0.0),
    "run off": (0.28, 0.0, 0.026),
    "sprint jump": (0.48, 0.42, 0.026),
}


def fall(dy, how):
    """Minecraft 1.8's fall, a tick at a time: ticks to fall dy, and the distance carried out from the edge."""
    vx, vy, acc = LEAVES[how]
    x = y = 0.0
    t = 0
    while y > -dy:
        x += vx
        y += vy
        vy = (vy - 0.08) * 0.98
        vx = (vx + acc) * 0.91
        t += 1
    return t, x


def damage(dy):
    return max(0, math.ceil(dy - 3))
