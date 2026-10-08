"""Floe — a knockback plan after Knockout Stick Fight: five floes of lake ice hanging in the sky over a polar sea,
overlapping one another a step or two apart in height, holes cut through them, everyone with a stick whose knockback
grows: one, two at a minute, three at two, ten at four. One life; the last player on the ice wins.

The floor is flat but for the steps where one floe lies over the next. Under it, too far to fall and live, is the
sea: a player knocked through a hole or off an edge is out. There is nothing to hide in, only crates and blocks of
cut ice to brace against, none taller than two. Two kinds of footing share the floor: snow, which stops a knocked
player quickly, and bare blue ice, which lets them slide, so a hit on ice carries much further toward the holes.

The plan is the floes as broken circles, the holes as ellipses, the ice as patches, the crates as boxes; and a
knockback model from Minecraft 1.8's own code, which says, at every knockback level, how far a hit carries a player
on snow and on ice.

    the floes' tops are at y 64 to 66; the kill height at 40; the sea at 20
"""
import math

FLOOR_Y = 64
KILL_Y = 40
WATER_Y = 20
LEVELS = [(0, 1), (60, 2), (120, 3), (240, 10)]                 # seconds into the match, knockback on the stick
TIME = "5m"


FLOES = [  # cx, cz, radius, top y, phase: five floes, each a broken circle, the higher lying over the lower
    (0, 0, 15.5, 65, 0.0),
    (-21, -10, 13.0, 64, 1.7),
    (17, -16, 12.5, 66, 3.1),
    (19, 13, 13.5, 64, 4.4),
    (-14, 19, 12.0, 66, 5.6),
]


def floe_r(f, theta):
    cx, cz, r, y, ph = f
    return r + 1.3 * math.sin(3 * theta + ph) + 0.8 * math.sin(5 * theta + 2 * ph) + 0.5 * math.sin(9 * theta + ph)


def floe_at(x, z):
    """The floe a column belongs to: of those covering it, the highest; or None."""
    best = None
    for f in FLOES:
        if math.hypot(x - f[0], z - f[1]) <= floe_r(f, math.atan2(z - f[1], x - f[0])):
            if best is None or f[3] > best[3]:
                best = f
    return best


def top(x, z):
    f = floe_at(x, z)
    return f[3] if f else None


HOLES = [  # cx, cz, rx, rz: holes cut through the ice
    (-22, -10, 2.6, 2.0), (17, -16, 2.0, 2.6), (20, 14, 2.8, 2.0), (-14, 20, 2.2, 2.4),
    (6, -6, 1.6, 1.4), (-8, 6, 1.4, 1.8), (2, 13, 1.8, 1.4), (-28, -2, 1.6, 2.0), (29, 2, 1.5, 2.2),
]
ICE = [  # cx, cz, rx, rz, angle: patches of bare blue ice, the slides, each running toward a hole or an edge
    (-4, -4, 7, 2.5, 0.6), (8, 6, 6, 2.5, 0.6), (-16, -6, 6, 2.2, 0.3), (14, -11, 5, 2, 1.2),
    (24, 10, 2.5, 5, 0.2), (-10, 14, 5, 2.2, 2.2), (-26, -14, 3, 2, 0.4), (21, -21, 3, 2, 0.8),
]
CRATES = [  # x0, x1, z0, z1, height: crates and blocks of cut ice to brace against
    (-3, -2, -9, -9, 1), (4, 4, -1, 0, 2), (-7, -7, 0, 1, 1), (9, 10, -5, -5, 1), (-2, -1, 8, 8, 2),
    (-24, -23, -16, -16, 2), (-18, -18, -3, -2, 1), (-29, -29, -9, -9, 1),
    (14, 14, -21, -20, 1), (22, 23, -14, -14, 2), (11, 11, -12, -12, 1),
    (15, 15, 8, 9, 1), (25, 25, 17, 17, 2), (22, 23, 6, 6, 1),
    (-18, -18, 14, 15, 1), (-11, -10, 25, 25, 2), (-20, -20, 23, 23, 1),
]
SPAWN_R = 8.0                                                    # players spawn spread over every floe, as Knockout Stick Fight's circles


def in_ellipse(x, z, cx, cz, rx, rz, ang=0.0):
    dx, dz = x - cx, z - cz
    c, s = math.cos(ang), math.sin(ang)
    u, v = dx * c + dz * s, -dx * s + dz * c
    return (u / rx) ** 2 + (v / rz) ** 2 <= 1.0


def is_floor(x, z):
    """A block of the floor: on a floe, outside every hole."""
    if floe_at(x, z) is None:
        return False
    return not any(in_ellipse(x, z, *h) for h in HOLES)


def surface(x, z):
    return "ice" if any(in_ellipse(x, z, *p) for p in ICE) else "snow"


def crate_at(x, z):
    for x0, x1, z0, z1, h in CRATES:
        if x0 <= x <= x1 and z0 <= z <= z1:
            return h
    return 0


# ---- the knockback model -----------------------------------------------------------------------------------
SLIP = dict(snow=0.6, ice=0.98)


def knock(level, surf, sprint=True):
    """How far a hit carries a player: Minecraft 1.8 sets the victim's horizontal speed to 0.4 and adds 0.5 for
    every level of knockback, sprinting counting as one, and 0.4 up; then air drag of 0.91 a tick, and on the
    ground the footing's slipperiness times 0.91. An upper bound: a player who steers against it goes less far."""
    vx = 0.4 + 0.5 * (level + (1 if sprint else 0))
    vy = 0.4
    x = y = 0.0
    air = True
    for _ in range(600):
        x += vx
        y += vy
        if air:
            vy = (vy - 0.08) * 0.98
            vx *= 0.91
            if y <= 0:
                air = False
        else:
            vx *= SLIP[surf] * 0.91
            if vx < 0.003:
                break
    return x
