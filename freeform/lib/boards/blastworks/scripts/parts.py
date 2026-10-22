"""Blastworks' made pieces, in the board's grammar (style.py): the box with the concept's room and doors, the
bridge, the descent, the raised east block with its tunnel and arm, the stairs, the exit's lanes, the spawn's hall; and the concept's
bedrock in each of them.

    lay(w)      every made piece of blue's half
"""
import random

import layout as L
import style as S
from pgmvox import B
from pgmvox.core.orient import stair
from pgmvox.grammar import rules as G


def _flight(name, rect, top):
    x0, z0, x1, z1 = rect
    tops = tuple(((x, z), top(x, z)) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    return G.Section((rect,), max(t for _, t in tops), name, S.style().fills["flight"], tops=tops)


def sections():
    up = {6: 12, 5: 12, 4: 13, 3: 13, 2: 14, 1: 14, 0: 15, -1: 15, -2: 16, -3: 16, -4: 17, -5: 17, -6: 18, -7: 18}
    down = {6: 12, 5: 12, 4: 11, 3: 10, 2: 9, 1: 8, 0: 7, -1: 6}
    return [
        G.Section((L.BOX,), L.DECK_H, "box", "plain"),
        G.Section((L.BRIDGE,), L.DECK_H, "bridge", "lanes"),
        G.Section((L.EAST,), L.EAST_TOP, "east", "plain"),
        G.Section((L.HALL,), L.HALL_H, "hall", "plain"),
        _flight("descent", L.DESCENT, lambda x, z: L.FRONT_H - round((-41 - x) * 9 / 18)),
        _flight("up-stair", L.UP_STAIR, lambda x, z: up[z]),
        _flight("down-stair", L.DOWN_STAIR, lambda x, z: down[z]),
        _flight("east-stair", L.EAST_STAIR, lambda x, z: L.FRONT_H + 1 + (-34 - x)),
    ] + [G.Section((r,), L.SPAWN_H, f"exit-{n}", "lanes") for n, r in enumerate(L.EXIT)]


def face_of(ground):
    """The storey's face where a piece stands high enough for it, the low one elsewhere."""
    return lambda x, z: "edge" if ground.top(x, z) >= 13 else "low"


def lay(w):
    g = G.Ground(sections())
    G.lay(w, g, S.style(), rng=random.Random(5), face_of=face_of(g))
    bridge(w)
    box(w)
    east(w)


def bridge(w):
    """The bridge stands over the void: a slab of bedrock under three courses of deck, and nothing under it."""
    x0, z0, x1, z1 = L.BRIDGE
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(0, L.SLAB[0]):
                w.set(x, y, z, B.AIR)
            for y in range(L.SLAB[0], L.SLAB[1] + 1):
                w.set(x, y, z, B.BEDROCK)


def box(w):
    """The concept's box inside the grammar's: the room, its floor falling to the side door, the doors of end stone,
    and the slits at y 5, 8 and 11 through its walls, so the room is seen and shot into but not walked into. The walls
    are the concept's bedrock up to y 13, and a line of bedrock across the top marks where the defenders may not
    stand."""
    bx0, bz0, bx1, bz1 = L.BOX
    for x in range(bx0, bx1 + 1):
        for z in range(bz0, bz1 + 1):
            if x in (bx0, bx1) or z in (bz0, bz1):
                for y in range(0, L.WALL_TOP + 1):
                    w.set(x, y, z, B.BEDROCK)
            if x == L.EDGE_X:
                for y in range(L.ROOM[5] + 1, L.DECK_H + 1):
                    w.set(x, y, z, B.BEDROCK)
    x0, z0, x1, z1, y0, y1 = L.ROOM
    floor = {x: (4 if x <= -88 else 3 if x <= -86 else 2 if x <= -84 else 1) for x in range(x0, x1 + 1)}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(1, y1 + 1):
                w.set(x, y, z, *((B.AIR, 0) if y > floor[x] else S.DIORITE if y == floor[x] else (B.BEDROCK, 0)))
    for y in (5, 8, 11):
        for x in range(bx0, bx1 + 1):
            for z in (bz0, bz1):
                if x0 <= x <= x1:
                    w.set(x, y, z, B.AIR)
        for z in range(bz0, bz1 + 1):
            if z0 <= z <= z1:
                w.set(bx0, y, z, B.AIR)
    for (a0, b0, a1, b1, c0, c1) in (L.ROOF_DOOR, L.SIDE_DOOR):
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                for y in range(c0, c1 + 1):
                    w.set(x, y, z, B.END_STONE)
    a0, b0, a1, b1, _, c1 = L.ROOF_DOOR
    for x in range(a0, a1 + 1):                          # the roof door lies a block under the deck
        for z in range(b0, b1 + 1):
            w.set(x, c1 + 1, z, B.AIR)


def east(w):
    """The tunnel through the east block, open at both ends and framed in quartz, and the arm on its top. The face
    over the void is the concept's bedrock up to the bridge's slab."""
    x0, z0, x1, z1 = L.EAST
    for z in range(z0, z1 + 1):
        for y in range(0, L.EAST_FACE[1] + 1):
            w.set(L.EAST_FACE[0], y, z, B.BEDROCK)
    f, top = L.TUNNEL
    for x in range(x0, x1 + 1):
        for z in range(L.TUNNEL_Z[0], L.TUNNEL_Z[1] + 1):
            w.set(x, f, z, *S.DIORITE)
            for y in range(f + 1, top + 1):
                w.set(x, y, z, B.AIR)
        for z in (L.TUNNEL_Z[0] - 1, L.TUNNEL_Z[1] + 1):
            if x in (x0, x1):
                for y in range(f + 1, top + 1):
                    w.set(x, y, z, *S.QPILLAR)
    a0, b0, a1, b1 = L.ARM
    for x in range(a0, a1 + 1):
        for z in range(b0, b1 + 1):
            edge = z in (b0, b1) or x == a0
            w.set(x, L.EAST_TOP, z, *(S.QUARTZ if edge else S.SPRUCE))
            if edge:
                inward = (0, 1) if z == b0 else (0, -1) if z == b1 else (1, 0)
                w.set(x, L.EAST_TOP - 1, z, B.SPRUCE_STAIRS, stair(inward, upside_down=True))
