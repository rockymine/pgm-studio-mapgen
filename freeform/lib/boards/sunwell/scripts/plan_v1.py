"""Sunwell — a water drop plan: a race down a jungle sinkhole two hundred deep, shelf by shelf, to the lake at its foot.

Every player spawns on the top shelf with three water buckets and sixteen health. Nine rock shelves jut from
alternate sides of the shaft, twenty-two apart; each overhangs the next by five, so a player drops off a shelf's
edge onto the shelf below, then walks back under it to that shelf's edge, and drops again. A fall of twenty-two
kills unless it ends in water. The lake at the foot scores a point and sends the player back to the top; the
first to three points wins.

Every drop offers the same choice in different places:

    a pool        water set into the shelf below, near the edge and small, or far and only reached by a sprint
                  jump: safe if it is hit, death if it is missed
    the bucket    the bare shelf: place water under you before you land
    the falls     a waterfall off the shelf's side into a basin: safe and slow
    a shaft       on four shelves, a hole through the shelf below over a pool two shelves down: two drops in one,
                  for whoever threads it

The plan is the shaft, the shelves as boxes with their pools, holes and falls, and a fall model: Minecraft's own
per-tick physics for a body stepping, running or sprint-jumping off an edge. The checker reads, for every drop,
how far each way of leaving the edge carries a player, and so which targets each way can hit.

    y is the top of a shelf, the block a player stands on: 236 the top, then every twenty-two down to 60; the
    lake's surface 38
"""
import math

R_SHAFT = 21                                   # the shaft's radius, to the face of its walls
TOP = 236
DROP = 22
N_SHELVES = 9
LAKE_Y = 38
EDGE = 2                                       # a north shelf's edge at z +2, a south shelf's at z -2
THICK = 4
HEALTH = 16                                    # twenty, less two hearts
SPEED = 5.6                                    # a sprint, blocks a second


def shelf_y(k):
    return TOP - DROP * k


def side(k):
    """'N': the shelf runs from the north wall to z +2 and drops to the south; 'S' the other way."""
    return "N" if k % 2 == 0 else "S"


def edge_dir(k):
    return 1 if side(k) == "N" else -1          # the way a player falls off it, along z


def in_shaft(x, z):
    return (x + 0.5) ** 2 + (z + 0.5) ** 2 <= R_SHAFT ** 2


def on_shelf(k, x, z):
    if not in_shaft(x, z):
        return False
    return z <= EDGE if side(k) == "N" else z >= -EDGE


def s_of(k, z):
    """How far a block on shelf k + 1 lies beyond shelf k's edge, along the fall."""
    return (z - EDGE) if side(k) == "N" else (-EDGE - z)


def z_of(k, s):
    return EDGE + s if side(k) == "N" else -EDGE - s


# For each drop k (off shelf k onto shelf k + 1): its targets on the shelf below, in the drop's own frame:
# s from the edge along the fall, x across. A pool is (name, x0, x1, s0, s1); the falls run down the side wall
# at x; a shaft is a hole in shelf k + 1 over a pool on shelf k + 3.
DROPS = [
    dict(pools=[("the near pool", -2, 0, 1, 3), ("the far pool", 3, 7, 7, 10)], falls=-17),
    dict(pools=[("the near pool", 1, 3, 1, 3), ("the middle pool", -6, -2, 4, 7)], falls=17, shaft=(0, 2, 8, 10)),
    dict(pools=[("the near pool", -1, 1, 2, 4), ("the far pool", -7, -3, 8, 11)], falls=-17),
    dict(pools=[], falls=17),                                   # its pool is the first shaft's
    dict(pools=[("the near pool", 0, 2, 1, 3), ("the far pool", -6, -2, 7, 10)], falls=-17, shaft=(4, 6, 6, 8)),
    dict(pools=[("the near pool", -3, -1, 1, 3), ("the middle pool", 3, 7, 4, 7)], falls=17),
    dict(pools=[("the far pool", -9, -5, 8, 11)], falls=-17),    # and the second shaft's pool beside it
    dict(pools=[("the near pool", 1, 3, 1, 3), ("the middle pool", -6, -2, 5, 8)], falls=17, shaft=(-6, -4, 10, 12)),
    dict(pools=[], falls=None, lake=True),                       # the last drop: into the lake, anywhere
]
SHAFT_POOL_MARGIN = 2                                           # the pool two shelves down runs past its hole


def gaps(k):
    """Where a player can leave shelf k: its edge is walled by a rim except over its targets. Each gap is
    (kind, x0, x1, s0 of what lies beyond): an opening a block wider than the pool, shaft or falls behind it."""
    d = DROPS[k]
    if d.get("lake"):
        return [("the lake", -R_SHAFT, R_SHAFT, 1)]
    out = [("pool", x0 - 1, x1 + 1, s0) for name, x0, x1, s0, s1 in pools(k)]
    if "shaft" in d:
        x0, x1, s0, s1 = d["shaft"]
        out.append(("shaft", x0 - 1, x1 + 1, s0))
    if d.get("falls") is not None:
        fx = d["falls"]
        out.append(("falls", min(fx, fx - 3 * (fx // abs(fx))), max(fx, fx - 3 * (fx // abs(fx))), 1))
    return out


def pools(k):
    """Drop k's pools, with the pool of a shaft cut two drops earlier, which lands on the same shelf."""
    out = list(DROPS[k]["pools"])
    if k >= 2 and "shaft" in DROPS[k - 2]:
        x0, x1, s0, s1 = DROPS[k - 2]["shaft"]
        m = SHAFT_POOL_MARGIN
        out.append(("the shaft's pool", x0 - m, x1 + m, s0 - m, s1 + m))
    return out
FALLS_SPEED = 4.0                                               # blocks a second, riding falling water down
SPAWN = dict(x=(-4, 4), z=(-17, -11))


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


def lake_box():
    return (-R_SHAFT, R_SHAFT, -R_SHAFT, R_SHAFT)
