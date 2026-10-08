"""Minecraft 1.8 player movement, a tick at a time: the one copy of the model five boards each wrote.

Every tick a flying player moves by its velocity, then vy = (vy - 0.08) * 0.98 and the horizontal speed is
multiplied by 0.91 in the air, or by the footing's slipperiness times 0.91 on the ground. Everything here is
built from that:

    fly(p, v, land)             a flight from a set velocity (a launch pad, a knockback) until `land` says stop
    fall(dy, how)               ticks to fall dy after leaving an edge, and how far out it carries
    fall_damage(dy)             hearts lost (half-hearts, as health points) for a drop
    jump_reach(rise, how)       the longest gap a jump clears to land `rise` blocks higher (or lower)
    knockback(level, ...)       how far a hit carries a player, on a footing
    solve_launch(start, target, land)   a pad velocity that lands within reach of a target

The models are upper bounds: a player who steers against a fall or a hit goes less far.
"""
import math

GRAVITY = 0.08
DRAG_Y = 0.98
AIR = 0.91
SLIP = {"default": 0.6, "ice": 0.98, "packed_ice": 0.98, "slime": 0.8}
EYE = 1.62                                                       # a standing player's eye over their feet
HEIGHT = 1.8

# how a player leaves an edge: (horizontal speed, vertical speed, air acceleration per tick)
LEAVES = {
    "step off": (0.13, 0.0, 0.0),
    "run off": (0.28, 0.0, 0.026),
    "sprint jump": (0.48, 0.42, 0.026),
    "jump": (0.28, 0.42, 0.02),
}


def fly(p, v, land=None, ticks=400):
    """A flight from position p = (x, y, z) with velocity v = (vx, vy, vz), no input.

    land(t, x, y, z, prev_y) is asked every tick and returns something to stop with (a landing) or None.
    Returns (landing or None, path), the path a list of (t, x, y, z); apex is max(y for path)."""
    x, y, z = p
    vx, vy, vz = v
    path = [(0, x, y, z)]
    prev_y = y
    for t in range(1, ticks):
        x += vx; y += vy; z += vz
        path.append((t, x, y, z))
        if land is not None:
            r = land(t, x, y, z, prev_y)
            if r is not None:
                return r, path
        prev_y = y
        vy = (vy - GRAVITY) * DRAG_Y
        vx *= AIR; vz *= AIR
    return None, path


def land_at(y_floor):
    """A land() for flat ground at height y_floor (the top of the floor block): stops when the feet come down
    through it."""
    def land(t, x, y, z, prev_y):
        if y <= y_floor <= prev_y + 1e-9 and y < prev_y:
            return dict(t=t, x=x, y=y_floor, z=z)
        return None
    return land


def fall(dy, how="run off"):
    """Ticks to fall dy blocks after leaving an edge the given way, and how far out from the edge it carries."""
    vx, vy, acc = LEAVES[how]
    x = y = 0.0
    t = 0
    while y > -dy:
        x += vx
        y += vy
        vy = (vy - GRAVITY) * DRAG_Y
        vx = (vx + acc) * AIR
        t += 1
        if t > 2000:
            break
    return t, x


def fall_damage(dy, feather_falling=0):
    """Health points (half-hearts) lost to a drop of dy blocks: none up to three, one a block after."""
    dmg = max(0, math.ceil(dy - 3))
    if feather_falling:
        dmg = math.floor(dmg * (1 - min(0.8, 0.12 * feather_falling)))
    return dmg


def jump_reach(rise=0, how="sprint jump"):
    """The horizontal distance a jump carries before the feet come back down to `rise` blocks over the take-off
    (negative for lower); a gap is cleared when it is shorter than this less the player's width (0.6)."""
    vx, vy, acc = LEAVES[how]
    x = y = 0.0
    best = 0.0
    for _ in range(400):
        x += vx
        y += vy
        vy = (vy - GRAVITY) * DRAG_Y
        vx = (vx + acc) * AIR
        if vy < 0 and y < rise:
            return best
        best = x
    return best


def knockback(level=0, sprint=False, slip=SLIP["default"], vy=0.4):
    """How far a hit carries a player standing on footing of slipperiness `slip`: 1.8 sets the victim's
    horizontal speed to 0.4 and adds 0.5 for every level of knockback, sprinting counting as one, and lifts
    them 0.4; air drag 0.91 a tick while up, the footing's slip times 0.91 once down."""
    vx = 0.4 + 0.5 * (level + (1 if sprint else 0))
    x = y = 0.0
    air = True
    for _ in range(600):
        x += vx
        y += vy
        if air:
            vy = (vy - GRAVITY) * DRAG_Y
            vx *= AIR
            if y <= 0:
                air = False
        else:
            vx *= slip * AIR
            if vx < 0.003:
                break
    return x


def solve_launch(start, target, land, vy_range=(0.6, 2.0, 0.05), vh_range=(0.4, 3.0, 0.05), apex_weight=0.05,
                 accept=lambda r: True):
    """Search pad velocities for one that lands nearest the target (x, z): start is (x, y, z), land is a land()
    callback; accept(landing) filters landings (e.g. on walkable floor, not into a wall). Returns
    (score, (vx, vy, vz), landing, apex) or None."""
    best = None
    px, py, pz = start
    ang = math.atan2(target[1] - pz, target[0] - px)
    vy = vy_range[0]
    while vy <= vy_range[1] + 1e-9:
        vh = vh_range[0]
        while vh <= vh_range[1] + 1e-9:
            v = (round(vh * math.cos(ang), 2), round(vy, 2), round(vh * math.sin(ang), 2))
            r, path = fly(start, v, land)
            if r is not None and accept(r):
                apex = max(p[2] for p in path)
                score = math.hypot(r["x"] - target[0], r["z"] - target[1]) + apex_weight * (apex - py)
                if best is None or score < best[0]:
                    best = (score, v, r, apex)
            vh += vh_range[2]
        vy += vy_range[2]
    return best
