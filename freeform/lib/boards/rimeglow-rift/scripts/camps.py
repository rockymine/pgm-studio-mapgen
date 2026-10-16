"""Two camps on the wooded ridge's foot, each half's own: the woodcutters' rest in the north and the orchard keeper's
cabin and field in the south, one pad drawn once in the ground and written twice."""
import numpy as np

import land as LD
from pgmvox import B
from pgmvox.built import build as BLD
from stamp import AIR, Stamp

CABIN_N = dict(ground=[(B.PLANKS, 1)], upper=[(B.PLANKS, 1)], post=1, gable=(B.PLANKS, 1), floor=(B.PLANKS, 5),
               roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR,
               window=(B.STAINED_PANE, 3), chimney=(B.STONEBRICK, 0))
CABIN_S = dict(ground=[(B.STAINED_CLAY, 12)], upper=[(B.STAINED_CLAY, 12)], post=0, gable=(B.PLANKS, 5),
               floor=(B.PLANKS, 5), roof=(B.BRICK, 0), stair=B.BRICK_STAIRS, slab=(B.SLAB, 4), door=B.DARK_OAK_DOOR,
               window=(B.STAINED_PANE, 1), chimney=(B.NETHER_BRICK, 0))


def build(w, ctx):
    H = ctx["H"]
    cx, cz = LD.CAMP
    y = int(H[cx - w.x0, cz - w.z0])
    for south in (False, True):
        S = Stamp(w, south)
        ax, az = (-1 - cx, -1 - cz) if south else (cx, cz)
        for x in range(cx - 9, cx + 9):
            for z in range(cz - 7, cz + 7):
                S.set(x, y, z, (B.GRASS, 0) if south else (B.SNOW, 0))
                S.clear(x, y + 1, z, x, y + 12, z)
        BLD.house(w, BLD.House(ax - (-4 if south else 4) + 0.5 * 0, az + (4 if south else -4), 180 if south else 0,
                               L=7, W=5, floor=y, storeys=1, storey=4, style=CABIN_S if south else CABIN_N,
                               door=1, chimney=True, roof="gable", overhang=1,
                               windows=BLD.window_rhythm(period=3, rows=((2,), (2,)), margin=1.5)),
                  ground_at=lambda x, z: y)
        if south:
            field(S, cx + 1, cz - 5, y)
        else:
            woodpile(S, cx + 2, cz - 5, y)
        fire_ring(S, cx - 3, cz + 3, y)
    return cx, cz, y


def woodpile(S, x0, z0, y):
    for dz in range(5):
        for dy in range(3 - dz // 2):
            S.log(x0, y + 1 + dy, z0 + dz, "z")
            S.log(x0 + 1, y + 1 + dy, z0 + dz, "z") if dy < 2 else None
    S.log(x0 + 4, y + 1, z0 + 2); S.set(x0 + 4, y + 2, z0 + 2, "fence")
    for k in range(3):
        S.stair(x0 + 3 + k, y + 1, z0 + 5, "plank", "n") if k == 1 else None


def fire_ring(S, fx, fz, y):
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            if dx or dz:
                S.set(fx + dx, y + 1, fz + dz, "wall")
    S.set(fx, y, fz, (B.NETHERRACK, 0))
    S.set(fx, y + 1, fz, (B.FIRE, 0))
    for dx in (-3, 3):
        S.stair(fx + dx, y + 1, fz, "plank", "e" if dx < 0 else "w")


def field(S, fx0, fz0, y):
    """Rows of pumpkin and hay inside a fence with a gate, a scarecrow of hay at its head."""
    for x in range(fx0, fx0 + 8):
        for z in range(fz0, fz0 + 7):
            edge = x in (fx0, fx0 + 7) or z in (fz0, fz0 + 6)
            S.set(x, y, z, (B.GRASS, 0) if edge else (B.DIRT, 1))
            if edge:
                if not (x == fx0 + 3 and z == fz0 + 6):
                    S.set(x, y + 1, z, "fence")
            elif (x - fx0) % 2 == 0:
                r = (x * 3 + z * 7) % 5
                S.set(x, y + 1, z, (B.PUMPKIN, 0) if r < 3 else (B.HAY, 0) if r == 3 else AIR)
    S.set(fx0 + 3, y + 1, fz0 + 3, (B.HAY, 0)); S.set(fx0 + 3, y + 2, fz0 + 3, (B.HAY, 0))
    S.set(fx0 + 3, y + 3, fz0 + 3, (B.PUMPKIN, 0))
    S.set(fx0 + 2, y + 2, fz0 + 3, "fence"); S.set(fx0 + 4, y + 2, fz0 + 3, "fence")
