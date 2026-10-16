"""The core's site: a ruined ring-tower on the butte, a pit in its middle, and the core held over the pit in a cage of
beams. Stated once for the north half, written through the stamp for each."""
import math

import numpy as np

from pgmvox import B
from stamp import AIR, Stamp

CX, CZ = 46, -48                   # the core's centre column
LEVEL = 73                          # the butte's top
PIT_R = 3.7
PIT_FLOOR = 66
CORE_Y = LEVEL + 1                  # the lowest block of the core


def build(w, H, south, seed=3):
    S = Stamp(w, south)
    rng = np.random.default_rng(seed)
    # the ring: stone brick at the foot and for crenelled walls, broken where the roads come in (south and east)
    for x in range(CX - 11, CX + 12):
        for z in range(CZ - 11, CZ + 12):
            r = math.hypot(x - CX, z - CZ)
            if r <= 11:
                S.foot(H, x, z, LEVEL, "rock")
                S.set(x, LEVEL, z, ("pave_a", "pave_b", "pave_c")[((x // 2) + (z // 2)) % 3] if r < 10.2 else "plinth")
                S.clear(x, LEVEL + 1, z, x, LEVEL + 22, z)
    # the pit
    for x in range(CX - 5, CX + 6):
        for z in range(CZ - 5, CZ + 6):
            r = math.hypot(x - CX, z - CZ)
            if r <= PIT_R:
                for y in range(PIT_FLOOR + 1, LEVEL + 1):
                    S.set(x, y, z, AIR)
                S.set(x, PIT_FLOOR, z, "wall" if r < PIT_R - 1.4 else "hot")
                for y in range(PIT_FLOOR - 3, PIT_FLOOR):
                    S.set(x, y, z, "rock")
            elif r <= PIT_R + 1.2:                          # the kerb: the pit's lip stands a course proud
                S.set(x, LEVEL, z, "wall")
                if (x + z) % 2 == 0:
                    S.set(x, LEVEL + 1, z, "slab_stone")
    # the ring-wall: radius 8 to 9, heights drawn per run, gaps south and east
    for ang in np.arange(0, 360, 1.5):
        a = math.radians(ang)
        for rr in (8.0, 8.8):
            x = int(round(CX + rr * math.cos(a) - 0.0)); z = int(round(CZ + rr * math.sin(a)))
            gap_s = 55 < ang < 125        # south: z grows
            gap_e = -22 < ang < 22 or ang > 338
            if gap_s or gap_e:
                continue
            run = int(ang // 22)
            hgt = 4 + (run * 7 + 3) % 4
            for y in range(LEVEL + 1, LEVEL + 1 + hgt):
                S.set(x, y, z, "wall" if y < LEVEL + hgt else "wall_b")
            if int(ang / 1.5) % 6 in (0, 1) and hgt >= 6:
                S.set(x, LEVEL + hgt + 1, z, "post")
    # four corner posts, beams across, and chains of bars down to the core's corners
    for sx in (-1, 1):
        for sz in (-1, 1):
            px, pz = CX + 5 * sx, CZ + 5 * sz
            for y in range(LEVEL + 1, LEVEL + 12):
                S.log(px, y, pz)
            S.set(px, LEVEL + 12, pz, "light")
    for x in range(CX - 5, CX + 6):
        for sz in (-1, 1):
            S.log(x, LEVEL + 11, CZ + 5 * sz, "x")
    for z in range(CZ - 5, CZ + 6):
        for sx in (-1, 1):
            S.log(CX + 5 * sx, LEVEL + 11, z, "z")
    for dx in range(-5, 6):
        S.log(CX + dx, LEVEL + 10, CZ, "x")
    for dz in range(-5, 6):
        S.log(CX, LEVEL + 10, CZ + dz, "z")
    for sx in (-1, 1):
        for sz in (-1, 1):
            for y in range(CORE_Y + 3, LEVEL + 10):
                S.set(CX + sx, y, CZ + sz, (B.IRON_BARS, 0))
    return S
