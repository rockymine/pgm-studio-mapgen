"""Spark — a knockback plan after Knockout Stick Fight, its floor the Claude spark: a terracotta starburst of twelve
rays of uneven length, hung in the sky over a sea of cloud. Everyone has a stick whose knockback grows: one, two at
a minute, three at two, ten at four. One life; the last player on the spark wins.

The floor is flat. Between the rays, and past their rounded tips, is nothing: a player knocked off is out. The hub
where the rays meet is the widest ground and the safest; the further out a ray, the narrower it runs, and a hit
from the side there throws a player off. There is nothing to hide in, only a few blocks of cream stone to brace
against, none taller than two, and a small hole in the hub.

The plan is the rays as tapered strokes from the centre, the hub as a disc, the blocks as boxes; and a knockback
model from Minecraft 1.8's own code, which says, at every knockback level, how far a hit carries a player.

    the floor is at y 64; the kill height at 40; the cloud sea at 20
"""
import math

FLOOR_Y = 64
KILL_Y = 40
CLOUD_Y = 20
LEVELS = [(0, 1), (60, 2), (120, 3), (240, 10)]                 # seconds into the match, knockback on the stick
TIME = "5m"

HUB_R = 12.5
RAYS = [  # angle in degrees (0 east, 90 south), length from the centre, width at the hub, width at the tip
    (4, 45, 11.0, 6.0), (33, 35, 9.5, 5.0), (61, 48, 11.5, 6.5), (92, 38, 9.5, 5.0),
    (118, 44, 11.0, 6.0), (150, 32, 8.5, 4.5), (178, 46, 11.5, 6.0), (208, 36, 9.5, 5.0),
    (237, 42, 10.0, 5.5), (266, 33, 8.5, 4.5), (295, 48, 11.5, 6.5), (326, 39, 10.0, 5.0),
]
HOLES = [  # cx, cz, rx, rz: the void through the floor
    (0, 0, 2.2, 2.2),                                            # the eye of the spark
]
CRATES = [  # x0, x1, z0, z1, height: blocks of cream stone to brace against
    (6, 6, -4, -3, 1), (-6, -5, 4, 4, 2), (-3, -3, -9, -9, 1), (7, 8, 6, 6, 1), (-9, -9, -3, -2, 1),
    (19, 19, 1, 1, 2), (12, 12, 17, 18, 1), (-17, -16, 0, 0, 1), (1, 1, -20, -20, 2), (-13, -13, -16, -15, 1),
    (15, 15, -10, -10, 1), (-3, -3, 17, 17, 1),
    (28, 28, 2, 2, 1), (15, 15, 26, 26, 2), (-13, -13, 24, 24, 1), (-29, -29, 1, 1, 1), (-14, -14, -22, -22, 2),
    (13, 13, -27, -27, 1), (18, 18, 12, 12, 1), (-20, -20, -11, -11, 1),
]
SPAWN_R = 8.5                                                    # players spawn round the hub, facing out


def in_ellipse(x, z, cx, cz, rx, rz, ang=0.0):
    dx, dz = x - cx, z - cz
    c, s = math.cos(ang), math.sin(ang)
    u, v = dx * c + dz * s, -dx * s + dz * c
    return (u / rx) ** 2 + (v / rz) ** 2 <= 1.0


def ray_at(x, z):
    """The ray a column lies on: a stroke from the centre, tapering from its hub width to its tip width, with a
    rounded end; or None."""
    for k, (a, length, w0, w1) in enumerate(RAYS):
        t = math.radians(a)
        u = x * math.cos(t) + z * math.sin(t)                    # along the ray
        v = -x * math.sin(t) + z * math.cos(t)                   # across it
        end = length - w1 / 2
        if 0 <= u <= end:
            w = w0 + (w1 - w0) * u / end
            if abs(v) <= w / 2:
                return k
        elif u > end and math.hypot(u - end, v) <= w1 / 2:
            return k
    return None


def on_spark(x, z):
    return math.hypot(x, z) <= HUB_R or ray_at(x, z) is not None


def is_floor(x, z):
    """A block of the floor: on the spark, outside every hole."""
    return on_spark(x, z) and not any(in_ellipse(x, z, *h) for h in HOLES)


def surface(x, z):
    return "clay"


def crate_at(x, z):
    for x0, x1, z0, z1, h in CRATES:
        if x0 <= x <= x1 and z0 <= z <= z1:
            return h
    return 0


# ---- the knockback model -----------------------------------------------------------------------------------
SLIP = dict(clay=0.6)


def knock(level, surf="clay", sprint=True):
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
