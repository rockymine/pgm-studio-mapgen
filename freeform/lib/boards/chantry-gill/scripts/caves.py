"""Chantry Gill's caves: passages worn through the rock, never straight, as carve layers in blue's half.

    carve()      the Hollin cave from the fell's front cliff under the town, a chamber where it forks, one way up to a
                 swallow hole by the byre and one on to the old adit; the tarn cave from a mouth just over the tarn
                 through the Scar to the bench under the brow; the side cave from the Scar's east cliff into it

A cave is a few stated points [x, floor y, z]; between them it wanders, a slow swing sideways and a width that
breathes, every three blocks a waypoint, so no passage is a pipe. The floor runs straight between the stated
points, so a player walks it.
"""
import math

import numpy as np

from layout import FLOOR


def wander(points, r=(2.2, 3.2), swing=2.2, step=3.0, seed=0, mouth=None):
    """Waypoints [x, floor y, z, radius] along the stated points: the plan swung sideways by two sine waves of
    random phase, faded to nothing at every stated point so a mouth or a joint stays where it is said to be. A
    `mouth` radius opens the first point that wide and narrows to the passage over the next three."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 2 * math.pi, 4)
    out = []
    for (x0, y0, z0), (x1, y1, z1) in zip(points, points[1:]):
        d = math.hypot(x1 - x0, z1 - z0)
        n = max(2, int(round(d / step)))
        nx, nz = -(z1 - z0) / d, (x1 - x0) / d
        for j in range(n):
            t = j / n
            s = len(out) * step
            fade = math.sin(math.pi * t)
            off = swing * fade * (0.65 * math.sin(s / 7.0 + ph[0]) + 0.35 * math.sin(s / 3.1 + ph[1]))
            rad = r[0] + (r[1] - r[0]) * (0.5 + 0.5 * math.sin(s / 5.3 + ph[2]) * math.cos(s / 8.9 + ph[3]))
            out.append([round(x0 + (x1 - x0) * t + nx * off, 2), round(y0 + (y1 - y0) * t, 2),
                        round(z0 + (z1 - z0) * t + nz * off, 2), round(rad, 2)])
    x, y, z = points[-1]
    out.append([x, y, z, r[0]])
    if mouth:
        for j in range(min(4, len(out))):
            out[j][3] = round(max(out[j][3], mouth - (mouth - out[j][3]) * j / 3), 2)
    return out


F = FLOOR
HOLLIN_FRONT = [(-41, F - 10, 9), (-39, F - 10, 19), (-31, F - 11, 28), (-22, F - 12, 38)]
HOLLIN_FORK = (-22, F - 12, 38)
HOLLIN_EAST = [HOLLIN_FORK, (-8, F - 13, 47), (6, F - 14, 56), (16, F - 14, 66), (24, F - 14, 75)]
HOLLIN_UP = [HOLLIN_FORK, (-32, F - 8, 44), (-41, F - 3, 48), (-50, F + 2, 51)]
TARN_CAVE = [(59, F - 5, 45), (64, F - 5, 50), (68, F - 2, 56), (68, F + 2, 62), (66, F + 6, 68), (63, F + 9, 73)]
SIDE_CAVE = [(88, F - 7, 37), (80, F - 6, 40), (73, F - 4, 45), (66, F - 4, 52)]
DRESS = {"ores": 40, "stalagmites": 24, "stalactites": 0.04, "mushrooms": 0.02}


def carve():
    return [
        {"id": "hollin-front", "op": "tunnel", "cover": 4, "pts": wander(HOLLIN_FRONT, (2.4, 3.4), seed=1, mouth=4.8),
         "dress": dict(DRESS, seed=31), "note": "the Hollin cave from its mouth in the fell's front cliff in under the town"},
        {"id": "hollin-hall", "op": "chamber", "at": list(HOLLIN_FORK), "rx": 6, "rz": 5, "h": 6, "cover": 4,
         "dress": dict(DRESS, seed=32), "note": "the hall where the Hollin cave forks"},
        {"id": "hollin-east", "op": "tunnel", "cover": 4, "pts": wander(HOLLIN_EAST, (2.0, 3.0), seed=2),
         "dress": dict(DRESS, seed=33), "note": "east under the square and the brig road into the old adit"},
        {"id": "hollin-up", "op": "tunnel", "cover": 4, "mouths": [-3, -2, -1], "pts": wander(HOLLIN_UP, (2.0, 2.8), seed=3),
         "dress": dict(DRESS, seed=34), "note": "up west to a swallow hole on the fell by the byre"},
        {"id": "tarn-cave", "op": "tunnel", "cover": 3, "mouths": [0, -3, -2, -1], "pts": wander(TARN_CAVE, (2.2, 3.0), 1.6, seed=4, mouth=4.6),
         "dress": dict(DRESS, seed=35), "note": "from just over the tarn through the Scar, out under the brow on the bench"},
        {"id": "side-cave", "op": "tunnel", "cover": 3, "pts": wander(SIDE_CAVE, (2.0, 2.8), seed=5, mouth=3.6),
         "dress": dict(DRESS, seed=36), "note": "from the Scar's east cliff into the tarn cave"},
    ]
