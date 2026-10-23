"""Coldstore's rooms cut into the rock: the wool block and the spawn.

    wool_block(w)    the wool room, the pane screen in front of it, the end stone monument in its glass case, the
                     window from the room onto the void, and the arrow on the block's face pointing to the enemy
    spawn(w)         the spawn hall in the west wall and its opening onto the hub
    monument()       the end stone capsule's blocks, for the destroyable

**The wool is reached through its monument.** The room has no door: its east wall is a screen of panes, and in front
of the screen stands a capsule of end stone in a glass case whose face is on the void. An attacker bridges to the
case, blows the end stone out with TNT, and when nine tenths of it is gone the middle of the screen, two wide and four
tall, is taken away (the map's trigger) and the room is open. This is Ender Blast's monument in front of Hot Dive's
wool room, as the concept's signs ask.
"""
import math

import layout as L
from pgmvox import B

ROOM_WALL = (B.STAINED_CLAY, 9)
SCREEN = (B.STAINED_PANE, 3)
CASE = (B.STAINED_GLASS, 3)


def monument():
    """The capsule's blocks: ten deep from its case back towards the room, six across, eleven tall, its ends rounded
    so it is deepest at its middle height."""
    u0, u1, v0, v1, y0, y1 = L.MONUMENT
    mid, half = (y0 + y1) / 2, (y1 - y0) / 2 + 0.5
    out = []
    for y in range(y0, y1 + 1):
        t = abs(y - mid) / half
        depth = round((u1 - u0 + 1) * math.sqrt(max(0.0, 1 - t ** 4)))
        for u in range(u1 - depth + 1, u1 + 1):
            for v in range(v0, v1 + 1):
                out.append((u, y, v))
    return out


def case():
    """The glass case: on the void in front of the capsule, and in the block's faces north and south of it."""
    mu0, mu1, mv0, mv1, my0, my1 = L.MONUMENT
    out = [(u, y, v) for u in range(mu0, L.CASE_U + 1) for y in range(my0 - 1, my1 + 2)
           for v in (mv0 - 2, mv0 - 1, mv1 + 1, mv1 + 2)]
    return out + [(L.CASE_U, y, v) for v in range(mv0, mv1 + 1) for y in range(my0 - 1, my1 + 2)]


def screen_door():
    """The two-wide, four-tall middle of the screen, opened when the monument is broken."""
    return [(L.SCREEN_U, y, v) for y in range(L.ROOM_FLOOR + 1, L.ROOM_FLOOR + 5) for v in range(L.DOOR_V[0], L.DOOR_V[1] + 1)]


def wool_block(w):
    u0, u1, v0, v1 = L.ROOM
    f = L.ROOM_FLOOR
    for u in range(u0 - 1, L.CASE_U + 1):                       # the room's walls and the capsule's hollow, in clay
        for v in range(v0 - 1, v1 + 2):
            for y in range(f, f + 6):
                w.set(u, y, v, *ROOM_WALL)
    for u in range(u0, u1 + 1):
        for v in range(v0, v1 + 1):
            w.set(u, f, v, B.DSLAB, 8)
            for y in range(f + 1, f + 5):
                w.set(u, y, v, B.AIR)
    for v in range(v0, v1 + 1):
        for y in range(f + 1, f + 5):
            w.set(L.SCREEN_U, y, v, *SCREEN)
            w.set(L.SCREEN_U + 1, y, v, B.AIR)                 # the gap between the screen and the end stone
    for u in range(u0, u1 + 1):                                 # a window from the room north onto the void
        for v in range(L.WALLS[3][2], v0):
            for y in range(f + 2, f + 5):
                w.set(u, y, v, *SCREEN)
    for p in case():
        w.set(*p, *CASE)
    for p in monument():
        w.set(*p, B.END_STONE)
    arrow(w)


def arrow(w):
    """The concept's arrow on the block's north face, set back behind a window: white wool pointing east, the way to
    the enemy's wool, and a square of the colour of the wool kept here. Drawn in the face at v 26, panes in v 25."""
    face = L.WALLS[3][2]
    u0, y0 = -88, 18
    rows = ["ffffffffffffffff",
            "ff222fffffff0fff",
            "ff222ff00000000f",
            "ff222fffffff0fff",
            "ffffffffffffffff"]
    for r, row in enumerate(rows):
        y = y0 + len(rows) - 1 - r
        for i, ch in enumerate(row):
            u = u0 + i
            w.set(u, y, face + 1, B.WOOL, int(ch, 16))
            w.set(u, y, face, *SCREEN)


def spawn(w):
    u0, u1, v0, v1 = L.SPAWN_ROOM
    for u in range(u0 - 1, u1 + 2):
        for v in range(max(v0, 0), v1 + 2):
            for y in range(L.TOP, L.TOP + 8):
                w.set(u, y, v, B.STONEBRICK, 0)
    for u in range(u0, u1 + 1):
        for v in range(max(v0, 0), v1 + 1):
            w.set(u, L.TOP, v, B.DSLAB, 8)
            for y in range(L.TOP + 1, L.TOP + 7):
                w.set(u, y, v, B.AIR)
        w.set(u, L.TOP + 7, 0, B.SEA_LANTERN)
    e0, e1, ev0, ev1 = L.SPAWN_EXIT
    for u in range(e0, e1 + 1):
        for v in range(max(ev0, 0), ev1 + 1):
            for y in range(L.TOP + 1, L.TOP + 5):
                w.set(u, y, v, B.AIR)
            w.set(u, L.TOP, v, B.DSLAB, 8)


ARROW_COLOURS = {(False, False): 10, (False, True): 4, (True, False): 1, (True, True): 5}


def paint_arrows(w):
    """After the mirrors: each wool block's arrow square in the colour of the enemy wool it points to, blue's
    purple (south) and yellow (north), red's orange and lime."""
    u0, u1, y0, y1 = L.ARROW_SQUARE
    face = L.WALLS[3][2] + 1
    for (east, north), dye in ARROW_COLOURS.items():
        for u in range(u0, u1 + 1):
            for y in range(y0, y1 + 1):
                x = -1 - u if east else u
                z = -1 - face if north else face
                w.set(x, y, z, B.WOOL, dye)
