"""Blastworks' blue half laid: the concept set down block for block, the board's additions in the Foundry grammar,
the spawn's second way out, the hub, the front and the middle, and the redstone round every build zone.

    concept(w)      the author's concept, from assets/concept.npz, untouched
    land(w)         the spawn's second way out round the corner into the hub, the hub, the front and the middle
    zones()         every build zone, blue's and its images, as rectangles
    markers(w)      a line of redstone two blocks out from every edge of a zone that faces the void (the studio's
                    rule ST5), as the concept marks its own
"""
import random

import numpy as np

import layout as L
from pgmvox import B
from pgmvox.grammar import foundry
from pgmvox.grammar import rules as G
from pgmvox.play.objectives import build_marker

STYLE = foundry.style(dye=11)


def concept(w):
    a = np.load(L.CONCEPT)
    ids, dat, (ox, oy, oz) = a["ids"], a["dat"], a["origin"]
    dx, dy, dz = L.CONCEPT_AT
    for i, y, k in np.argwhere(ids != 0):
        w.set(int(i + ox + dx), int(y + oy + dy), int(k + oz + dz), int(ids[i, y, k]), int(dat[i, y, k]))


def land(w):
    secs = [G.Section((box,), h, name, fill) for name, box, h, fill in L.LAND]
    for name, (x0, z0, x1, z1), lo, hi, side in L.FLIGHTS:
        if side in "ns":
            n, at = z1 - z0 + 1, (lambda x, z: z - z0) if side == "n" else (lambda x, z: z1 - z)
        else:
            n, at = x1 - x0 + 1, (lambda x, z: x - x0) if side == "w" else (lambda x, z: x1 - x)
        tops = tuple(((x, z), hi - at(x, z) * (hi - lo + 1) // n) for x in range(x0, x1 + 1)
                     for z in range(z0, z1 + 1))
        secs.append(G.Section(((x0, z0, x1, z1),), hi, name, STYLE.fills["flight"], tops=tops))
    G.lay(w, G.Ground(secs), STYLE, rng=random.Random(7))


def image(r):
    x0, z0, x1, z1 = r
    return (-1 - x1, -1 - z1, -1 - x0, -1 - z0)


def zones():
    out = list(L.ZONES)
    return out + [image(r) for r in L.ZONES if image(r) not in out]


def markers(w):
    """Redstone round the build zones, laid once the whole board stands so its terrain pulls the lines back."""
    build = {(x, z) for x0, z0, x1, z1 in zones() for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}
    solid = (w.ids[:, 1:, :] != 0).any(axis=1)
    terrain = {(int(i) + w.x0, int(k) + w.z0) for i, k in np.argwhere(solid)}
    build -= terrain
    cells = build_marker(build, terrain)
    for x, z in cells:
        if w.inside(x, L.MARKER_Y, z):
            w.set(x, L.MARKER_Y, z, B.REDSTONE_WIRE)
    return len(cells)
