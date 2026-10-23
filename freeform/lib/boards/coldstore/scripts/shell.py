"""Coldstore's shell: the bunker as rock, island and void, in the drawn quarter.

    plan()           every column of the quarter as ROCK (bedrock from the floor to the roof), ISLAND or VOID
    shell(w)         the box, the roof, the rock with its skin, the islands, the plinths and cornices, the vent tunnels

**Rock is bedrock and nothing else is under its skin.** A wall, a pillar or the wool block is bedrock from y 7 to the
roof, and the face a player sees is one block of stone brick laid on it, so there is nothing in a wall to hide in or
tunnel along: the concept's two-block walls were the one place a player could. Under every island and every void
there is nothing at all down to the world's floor.
"""
import numpy as np

import layout as L
from pgmvox import B

VOID, ISLAND, ROCK = 0, 1, 2
U0, U1, V0, V1 = L.OUTER_U, -1, 0, L.OUTER_V
SKIN = (B.STONEBRICK, 0)
STRIPES = {12: (B.STAINED_CLAY, 9), 13: (B.SANDSTONE, 2), 37: (B.SANDSTONE, 2), 38: (B.STAINED_CLAY, 9)}
PLINTH, CORNICE = (B.STONE, 0), (B.STONE, 0)
DECK = (B.DSLAB, 8)                        # an island's top: smooth stone
TUNNEL_FLOOR = (B.STONE, 6)                      # polished andesite


def plan():
    """The quarter's columns: a 2D array over u U0..U1, v V0..V1 of VOID, ISLAND or ROCK."""
    k = np.zeros((U1 - U0 + 1, V1 - V0 + 1), np.uint8)

    def put(r, kind):
        u0, u1, v0, v1 = r
        k[u0 - U0:u1 - U0 + 1, v0 - V0:v1 - V0 + 1] = kind
    for r in L.ISLANDS:
        put(r, ISLAND)
    for r in L.WALLS:
        put(r, ROCK)
    for p in L.PILLARS:
        put(p["box"], ROCK)
    put((U0, U1, L.INNER[3] + 1, V1), ROCK)
    return k


def at(k, u, v):
    if u > U1 or v < V0:                         # past a mirror line: the image of the column this side of it
        u = -1 - u if u > U1 else u
        v = -1 - v if v < V0 else v
    if u < U0 or v > V1:
        return ROCK
    return k[u - U0, v - V0]


def faces(k, u, v):
    """The four sides of a column that look onto a column of another kind with air over it."""
    return [(du, dv) for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1)) if at(k, u + du, v + dv) != ROCK]


def shell(w):
    k = plan()
    for u in range(U0, U1 + 1):
        for v in range(V0, V1 + 1):
            kind = k[u - U0, v - V0]
            if kind == ROCK:
                w.column(u, v, L.FLOOR, L.ROOF[1], B.BEDROCK)
                if faces(k, u, v):
                    for y in range(L.PLINTH[1] + 1, L.ROOF[0]):
                        w.set(u, y, v, *STRIPES.get(y, SKIN))
            elif kind == ISLAND:
                w.column(u, v, L.FLOOR, L.FLOOR + 1, B.BEDROCK)
                w.column(u, v, L.FLOOR + 2, L.TOP - 1, B.STONE)
                w.set(u, L.TOP, v, *DECK)
                if any(at(k, u + du, v + dv) == VOID for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    for y in range(L.PLINTH[1] + 1, L.TOP):
                        w.set(u, y, v, *STRIPES.get(y, SKIN))
            w.column(u, v, L.ROOF[0], L.ROOF[1], B.BEDROCK)
    # the plinth and the cornice: a block proud of every face over the void, at the island's foot and the roof's
    for u in range(U0, U1 + 1):
        for v in range(V0, V1 + 1):
            if k[u - U0, v - V0] != VOID:
                continue
            near = [at(k, u + du, v + dv) for du, dv in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(n != VOID for n in near):
                w.column(u, v, L.FLOOR, L.FLOOR + 1, B.BEDROCK)
                w.column(u, v, *L.PLINTH, *PLINTH)
            if any(n == ROCK for n in near):
                w.column(u, v, L.CEIL - 1, L.CEIL, *CORNICE)
    for p in L.PILLARS:
        if "tunnel" in p:
            tunnel(w, p)
    return k


def tunnel(w, p):
    """A vent tunnel through a pillar: four wide, seven tall, its floor y 27, open at both ends onto the void, a frame
    of walls round each mouth like the cover of a vent."""
    u0, u1, v0, v1 = p["box"]
    a, b = p["tunnel"]["at"]
    y0, y1 = L.TUNNEL
    along_v = p["tunnel"]["axis"] == "v"
    lo, hi = (v0, v1) if along_v else (u0, u1)

    def put(s, t, y, block):
        u, v = (t, s) if along_v else (s, t)
        if u <= U1:                              # past the mirror line is the image's
            w.set(u, y, v, *block)
    for s in range(lo, hi + 1):
        for t in range(a - 1, b + 2):
            inside = a <= t <= b
            put(s, t, y0, TUNNEL_FLOOR if inside else SKIN)
            for y in range(y0 + 1, y1 + 1):
                put(s, t, y, (B.AIR, 0) if inside else SKIN)
            put(s, t, y1 + 1, SKIN)
    for end in (lo - 1, hi + 1):
        for t in range(a - 1, b + 2):
            post = t in (a - 1, b + 1)
            for y in range(y0, y1 + 2):
                if post or y in (y0, y1 + 1):
                    put(end, t, y, (B.COBBLE_WALL, 0))
