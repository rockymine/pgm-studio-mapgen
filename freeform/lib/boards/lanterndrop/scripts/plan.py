"""Lantern Drop — a water drop plan, a spin-off of Lantern Pass: the pass broken into floating pieces and run backwards,
from the bell court among the snowy peaks down through roofs, gates, bamboo, bridges and terraces to the harbour,
every player against every other.

The course runs one way, south along z, falling from 240 to 26 over three hundred blocks. Every piece is a fragment
of the pass hanging in the void: a player drops from one piece's far edge to the next piece below and ahead, runs
across it, and drops again. The course splits into a left and a right way, mirror images, and they meet again on
the middle pieces. A punch anywhere can put a player in the void, which kills.

Fourteen hills sit on landing pieces, as Limbo II has them: five mirrored pairs, three on the middle line, and the
last on the barge in the harbour, worth three times the others. A hill is taken at a touch and scores every second
for its holder until another player touches it, alive or not. From the harbour the slipway sends a player back to
the bell court. The most points when the clock runs out wins.

A drop of nineteen or more kills unless it ends in water: a cistern or a paddy set into the piece below, the
harbour, or a bucket placed on the way down. Shorter drops only hurt.

The plan is the course as pieces, each a box with its top, its theme, its hill and its water, given for the left
way and mirrored; the links between consecutive pieces; and a fall model: Minecraft's own per-tick physics for a
body running or sprint-jumping off an edge, which says whether each link can be jumped at all.

    y is the top of a piece, the block a player stands on
"""
import math

HEALTH = 16                                    # twenty, less two hearts
SPEED = 5.6                                    # a sprint, blocks a second
POINTS = dict(hill=1, last=3)
TIME = "5m"
HILL = 5

# The course, in order. Each group is one piece on the middle line or a pair (given on the left, x < 0, mirrored).
#   (name, theme, x0, x1, z0, z1, y, extras)       extras: hill=True; water=(x0, x1, z0, z1) set into the top
COURSE = [
    ("the bell court", "court", -8, 8, 0, 16, 240, dict(spawn=True)),
    ("the torii beams", "torii", -13, -9, 22, 30, 233, {}),
    ("the drum towers", "roof", -16, -10, 36, 44, 218, dict(hill=True)),
    ("the great pagoda", "pagoda", -6, 6, 51, 65, 198, dict(hill=True, water=(-3, 3, 52, 57))),
    ("the lantern lines", "beam", -10, -8, 71, 83, 190, {}),
    ("the bamboo crowns", "bamboo", -14, -8, 89, 97, 178, dict(hill=True)),
    ("the shrine roof", "roof", -5, 5, 104, 114, 168, {}),
    ("the rope bridge", "rope", -1, 1, 120, 144, 160, dict(hill=True)),
    ("the first pillar", "pillar", -6, -5, 149, 150, 155, {}),
    ("the second pillar", "pillar", -7, -6, 154, 155, 153, {}),
    ("the third pillar", "pillar", -6, -5, 159, 160, 151, {}),
    ("the gallery roofs", "gallery", -12, -6, 166, 180, 131, dict(hill=True, water=(-11, -7, 166, 170))),
    ("the terrace", "terrace", -10, 10, 187, 199, 115, dict(hill=True, water=(-9, 9, 188, 198))),
    ("the market awnings", "awning", -14, -8, 205, 215, 103, {}),
    ("the stall roofs", "roof", -16, -10, 221, 227, 94, dict(hill=True)),
    ("the arcade roof", "arcade", -6, 6, 234, 248, 80, {}),
    ("the crow's nests", "nest", -8, -6, 254, 256, 66, dict(hill=True)),
    ("the boathouse roof", "boathouse", -8, 8, 262, 274, 50, {}),
    ("the barge", "barge", -6, 6, 282, 296, 30, dict(hill=True, last=True, harbour=True)),
]
HARBOUR = dict(x=(-22, 22), z=(276, 316), y=27)    # the harbour's water, its surface at 27, round the barge
SLIPWAY = dict(x=(-4, 4), z=(312, 316))            # at the harbour's far end: back to the bell court


def pieces():
    """Every piece: (index, name, theme, x0, x1, z0, z1, y, extras, side)."""
    out = []
    for i, (name, theme, x0, x1, z0, z1, y, ex) in enumerate(COURSE):
        if x0 <= 0 <= x1:
            out.append((i, name, theme, x0, x1, z0, z1, y, ex, "middle"))
        else:
            out.append((i, name, theme, x0, x1, z0, z1, y, ex, "left"))
            m = dict(ex)
            if "water" in ex:
                a, b, c, d = ex["water"]
                m["water"] = (-b, -a, c, d)
            out.append((i, name, theme, -x1, -x0, z0, z1, y, m, "right"))
    return out


def links():
    """Each piece to the next group's on its own side, or to the middle; the middle to both sides."""
    ps = pieces()
    by = {}
    for p in ps:
        by.setdefault(p[0], []).append(p)
    out = []
    for i in range(len(COURSE) - 1):
        for a in by[i]:
            for b in by[i + 1]:
                if a[9] == "middle" or b[9] == "middle" or a[9] == b[9]:
                    out.append((a, b))
    return out


def gap(a, b):
    """The void a player must clear from a's far edge to b: along the course, and across it."""
    along = b[5] - a[6] - 1
    across = max(b[3] - a[4] - 1, a[3] - b[4] - 1, 0)
    return along, across


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
