"""Loomfall — a wool run plan: five flying carpets stacked over a desert city at night, falling away under every step.

Every player starts on the top carpet. A block of wool a player steps on turns white and drops out from under them,
so standing still is falling; a player who falls lands on whatever carpet lies below, or, under the last one, falls
past the kill height into the city's lights and is out. The last player standing wins.

The carpets are laid crossways, each a different shape and turned the other way from the one above it, so the ends
of every carpet hang over something different: the next carpet, a carpet two down, or nothing. Moth holes are worn
through two of them. Where a hole or an end lies over nothing, falling there is death; where it lies over a carpet
further down, it is a shortcut to fresh wool.

The plan is the carpets as rectangles with their holes and patterns, and the checker reads, for every cell of every
carpet, what a player falling from it lands on.

    y is the height of a carpet's single sheet of wool
"""
_FULL = [  # the carpets as first drawn: name, x0, x1, z0, z1, y, holes [(x0, x1, z0, z1)]
    ("the sultan's carpet", -20, 19, -14, 13, 196, []),
    ("the runner", -11, 10, -26, 25, 182, []),
    ("the kilim", -26, 25, -11, 10, 166, []),
    ("the garden carpet", -18, 17, -24, 23, 148, [(-15, -14, -20, -19), (13, 14, -20, -19), (-15, -14, 18, 19),
                                                   (13, 14, 18, 19), (-1, 0, -1, 0)]),
    ("the great carpet", -23, 22, -23, 22, 128, [(-20, -18, -20, -18), (17, 19, -20, -18), (-20, -18, 17, 19),
                                                 (17, 19, 17, 19)]),
]
SCALE = 0.7                                    # after the playtest each carpet is 0.7 of its length and width: half the area


def _scaled(c):
    name, x0, x1, z0, z1, y, holes = c
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    wx, wz = max(2, 2 * round((x1 - x0 + 1) * SCALE / 2)), max(2, 2 * round((z1 - z0 + 1) * SCALE / 2))
    nx0, nz0 = round(cx * SCALE - (wx - 1) / 2), round(cz * SCALE - (wz - 1) / 2)
    nh = []
    for a, b, c0, d in holes:                                      # a hole keeps its size, at its scaled place
        hx, hz = round((a + b) / 2 * SCALE - (b - a) / 2), round((c0 + d) / 2 * SCALE - (d - c0) / 2)
        nh.append((hx, hx + b - a, hz, hz + d - c0))
    return (name, nx0, nx0 + wx - 1, nz0, nz0 + wz - 1, y, nh)


CARPETS = [_scaled(c) for c in _FULL]
KILL_Y = 116                                   # below this a player is out
SPAWN = dict(x=(-8, 7), z=(-6, 5))
RUN = 7.0                                      # cells a running player tramples a second
WOOL_DELAY = 10                                # ticks before trampled wool falls


def cells(c):
    name, x0, x1, z0, z1, y, holes = c
    out = set()
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not any(a <= x <= b and c0 <= z <= d for a, b, c0, d in holes):
                out.add((x, z))
    return out


def below(k, x, z):
    """What a player falling from carpet k at (x, z) lands on: the index of a carpet further down, or None."""
    for j in range(k + 1, len(CARPETS)):
        if (x, z) in cells(CARPETS[j]):
            return j
    return None


# ---- the patterns: each carpet woven in its own colours, never white (white wool is what falls) ---------------
WOOL = dict(orange=1, magenta=2, light_blue=3, yellow=4, lime=5, pink=6, gray=7, silver=8, cyan=9, purple=10,
            blue=11, brown=12, green=13, red=14, black=15)


def pattern(k, x, z):
    """The colour of carpet k's wool at (x, z): borders, a field, and the carpet's own figure."""
    name, x0, x1, z0, z1, y, holes = CARPETS[k]
    cx, cz = (x0 + x1) / 2.0, (z0 + z1) / 2.0
    u, v = x - cx, z - cz                                         # from the middle
    w, h = (x1 - x0) / 2.0, (z1 - z0) / 2.0
    edge = min(x - x0, x1 - x, z - z0, z1 - z)
    c = WOOL
    if k == 0:                                                   # the sultan's carpet: red, a gold medallion
        if edge == 0:
            return c["black"]
        if edge <= 3:
            return c["yellow"] if (x + z) % 4 == 0 and edge == 2 else c["blue"]
        d = abs(u) / w + abs(v) / h
        if d < 0.28:
            return c["yellow"] if d > 0.18 else c["orange"]
        if d < 0.36:
            return c["blue"]
        if abs(abs(u) - w + 6) + abs(abs(v) - h + 6) < 4:          # quarter medallions in the corners
            return c["yellow"]
        return c["red"]
    if k == 1:                                                   # the runner: diamonds down its length
        if edge == 0:
            return c["brown"]
        if edge <= 2:
            return c["orange"]
        period = 10
        m = abs(((z - z0) % period) - period / 2.0) + abs(u)
        if m < 3:
            return c["cyan"] if m < 1.5 else c["light_blue"]
        if m < 4:
            return c["orange"]
        return c["blue"]
    if k == 2:                                                   # the kilim: stepped bands across it
        if edge == 0:
            return c["black"]
        band = (x - x0) // 4
        step = abs(((z - z0) % 8) - 4)
        if ((x - x0) % 4 == step % 4) and band % 2:
            return c["black"]
        return [c["orange"], c["brown"], c["red"], c["yellow"]][band % 4]
    if k == 3:                                                   # the garden carpet: four gardens, water between
        if edge == 0:
            return c["brown"]
        if edge <= 2:
            return c["red"]
        if abs(u) < 1.6 or abs(v) < 1.6:
            return c["cyan"]
        if (int(abs(u)) % 6 == 3) and (int(abs(v)) % 6 == 3):
            return c["pink"] if (x + z) % 2 else c["yellow"]        # flowers
        if (int(abs(u)) + int(abs(v))) % 6 == 0:
            return c["lime"]
        return c["green"]
    if k == 4:                                                   # the great carpet: a star on deep blue
        if edge == 0:
            return c["black"]
        if edge <= 3:
            return c["purple"] if edge != 2 else c["magenta"]
        r = max(abs(u), abs(v)) * 0.7 + min(abs(u), abs(v)) * 0.3
        if r < 4:
            return c["yellow"]
        if r < 7:
            return c["purple"]
        if r < 8:
            return c["magenta"]
        return c["blue"]
    return c["red"]
