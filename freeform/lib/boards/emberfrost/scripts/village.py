"""The houses and what stands round them: the Hearth yard with its lodge, Amberford with Beacon Hill, the Foundry in the Caldera, and a
lodge on the ice lane. Every house is the library's own, in a style named for where it stands: hearth (spruce over stone), maple
(acacia planks under red sandstone), forge (nether brick under iron bars), pine (spruce over stone brick)."""
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.built import build as BL
from pgmvox.built.props import brazier, lamp
from util import claim_cells, claim_disc, disc, pick, stairs

STYLES = {
    "hearth": dict(ground=[(B.STONEBRICK, 0), (B.COBBLE, 0), (B.STONE, 5)], upper=[(B.PLANKS, 1)], post=1, gable=(B.PLANKS, 1),
                   floor=(B.PLANKS, 1), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR,
                   window=(B.PANE, 0), chimney=(B.COBBLE, 0)),
    "maple": dict(ground=[(B.STONE, 5), (B.COBBLE, 0)], upper=[(B.PLANKS, 4)], post=1, gable=(B.PLANKS, 4), floor=(B.PLANKS, 4),
                  roof=(B.RED_SANDSTONE, 2), stair=B.RED_SANDSTONE_STAIRS, slab=(B.RED_SANDSTONE_SLAB, 0), door=B.ACACIA_DOOR,
                  window=(B.PANE, 0), chimney=(B.BRICK, 0)),
    "forge": dict(ground=[(B.NETHER_BRICK, 0)], upper=[(B.STONEBRICK, 0), (B.NETHER_BRICK, 0)], post=None, gable=(B.STONEBRICK, 0),
                  floor=(B.STONEBRICK, 0), roof=(B.NETHER_BRICK, 0), stair=B.NETHER_STAIRS, slab=(B.SLAB, 6), door=B.DARK_OAK_DOOR,
                  window=(B.STAINED_PANE, 1), chimney=(B.NETHER_BRICK, 0)),
    "pine": dict(ground=[(B.STONEBRICK, 0), (B.STONE, 5)], upper=[(B.PLANKS, 1)], post=1, gable=(B.PLANKS, 1), floor=(B.PLANKS, 1),
                 roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.STAINED_PANE, 3),
                 chimney=(B.STONEBRICK, 0)),
}

from sites import HOUSES


JETTIED = {"lodge", "bakehouse", "press", "chapel", "pinewatch", "foundry"}


def site_floor(cx, cz, heading, L, W):
    fr = BL.Frame(cx, cz, heading)
    cells = fr.cells(L, W)
    hs = [P.g(x, z) for x, z in cells]
    return max(hs), min(hs), cells


def houses(w, rng, stats):
    placed = {}
    for key, cx, cz, heading, L, W, storeys, style, door, name in HOUSES:
        hi, lo, cells = site_floor(cx, cz, heading, L, W)
        stats[f"site {key}"] = hi - lo
        out = BL.house(w, BL.House(cx, cz, heading, L, W, floor=hi, storeys=storeys, style=STYLES[style], door=door, roof="gable", jetty=(storeys >= 2 and key in JETTIED)),
                       ground_at=P.g, rng=rng)
        claim_cells(out["footprint"], 1)
        placed[key] = out
    return placed


def yard(w, rng):
    """The Hearth yard: flagstone, gravel and packed earth in patches, a well, two standards, braziers at the corners, hay and logs."""
    cx, cz = 0, -76
    level = land.SPAWN_LEVEL
    for x, z, d in disc(cx, cz, 12.5):
        if x < -12 or x > 12:
            continue
        if d > 11.4 and rng.random() < 0.5:
            continue
        if P.g(x, z) != level and abs(P.g(x, z) - level) > 1:
            continue
        if d < 9.0:
            blk = pick(rng, [((B.COBBLE, 0), 4), ((B.STONEBRICK, 0), 3), ((B.STONE, 5), 3), ((B.STONEBRICK, 2), 1)])
        else:
            blk = pick(rng, [((B.DIRT, 1), 4), ((B.COBBLE, 0), 2), ((B.GRAVEL, 0), 2), ((B.STONE, 5), 1)])
        w.set(x, P.g(x, z), z, *blk)
    claim_disc(cx, cz, 13)
    # the well
    wx, wz = -7, -75
    y = P.g(wx, wz)
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            ring = (ddx, ddz) != (0, 0)
            w.set(wx + ddx, y, wz + ddz, *((B.STONEBRICK, 0) if ring else (B.WATER, 0)))
            if ring:
                w.set(wx + ddx, y + 1, wz + ddz, B.COBBLE_WALL)
            else:
                w.set(wx + ddx, y - 1, wz + ddz, B.STONE)
    for ddx, ddz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        w.set(wx + ddx, y + 2, wz + ddz, B.SPRUCE_FENCE)
        w.set(wx + ddx, y + 3, wz + ddz, B.SPRUCE_FENCE)
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            w.set(wx + ddx, y + 4, wz + ddz, B.WOOD_SLAB, 5)
    # standards either side of the lodge's door and braziers at the yard's corners
    for sx in (-4, 4):
        yy = P.g(sx, -82)
        for k in range(1, 6):
            w.set(sx, yy + k, -82, B.SPRUCE_FENCE)
        w.banner(sx, yy + 6, -82, 1, [("bs", 15), ("ss", 1)], rot=0)
    for bx, bz in ((-10, -71), (10, -71), (-10, -83), (10, -83)):
        brazier(w, bx, P.g(bx, bz), bz, light=(B.NETHERRACK, 0), height=2)
        w.set(bx, P.g(bx, bz) + 4, bz, B.FIRE)
    # the carpet from the lodge door to the spawn, in the team's colour
    for z in range(-83, -76):
        for x in (-1, 0, 1):
            w.set(x, P.g(x, z) + 1, z, B.CARPET, 14)
    # logs and hay by the woodshed and the stable
    for k, (hx, hz) in enumerate(((-17, -80), (-17, -83), (-16, -81), (18, -79), (18, -82))):
        y = P.g(hx, hz)
        w.set(hx, y + 1, hz, *((B.HAY, 0) if hx > 0 else (B.LOG, 1 | 4 + 0)))
        if k % 2 == 0:
            w.set(hx, y + 2, hz, *((B.HAY, 0) if hx > 0 else (B.LOG, 1 | 4)))


def beacon(w, rng):
    """Beacon Hill's crown: a fire in a ring of polished stone pillars, lit from a mile off."""
    cx, cz = land.BEACON
    y = land.BEACON_LEVEL
    for x, z, d in disc(cx, cz, 4.2):
        for yy in range(min(P.g(x, z), y) - 1, y):
            w.set(x, yy, z, B.STONE, 0)
        w.set(x, y, z, *pick(rng, [((B.STONE, 6), 3), ((B.STONEBRICK, 0), 3), ((B.STONE, 5), 2)]))
        for yy in range(y + 1, y + 12):
            w.set(x, yy, z, B.AIR)
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            w.set(cx + ddx, y, cz + ddz, B.NETHERRACK)
            w.set(cx + ddx, y + 1, cz + ddz, *((B.COBBLE_WALL, 0) if (ddx, ddz) != (0, 0) else (B.NETHERRACK, 0)))
    w.set(cx, y + 2, cz, B.FIRE)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        px, pz = cx + round(3.4 * math.cos(a)), cz + round(3.4 * math.sin(a))
        for yy in range(y + 1, y + 1 + [4, 3, 5, 3, 4, 2][k]):
            w.set(px, yy, pz, B.STONE, 6)
        w.set(px, y + 1 + [4, 3, 5, 3, 4, 2][k], pz, B.SLAB, 0)
    claim_disc(cx, cz, 6.5)


def pumpkins(w, rng):
    """A pumpkin patch behind the Bakehouse and hay stooks by the Mill Barn: made ground, claimed."""
    for x in range(-18, -9):
        for z in range(-72, -66):
            y = P.g(x, z)
            if abs(y - 67) > 2:
                continue
            w.set(x, y, z, B.DIRT, 2 if rng.random() < 0.7 else 1)
            if rng.random() < 0.28:
                w.set(x, y + 1, z, B.PUMPKIN, int(rng.integers(0, 4)))
            elif rng.random() < 0.25:
                w.set(x, y + 1, z, B.HAY, 0)
    claim_cells([(x, z) for x in range(-19, -8) for z in range(-73, -65)])
    for hx, hz in ((-22, -22), (-19, -19), (-24, -19)):
        y = P.g(hx, hz)
        for k in range(1, 4):
            w.set(hx, y + k, hz, B.HAY, 0)
        w.set(hx, y + 4, hz, B.SLAB, 5)
        claim_cells([(hx, hz)], 1)


def lamps_for(w, rng):
    """Lamp posts along the Drove Road, one each side in turn, warm glowstone under a cap."""
    pts = [(0, -76), (2, -68), (-1, -58), (2, -49), (-4, -44), (-7, -37), (-5, -28), (-1, -20)]
    from util import wander
    for k, (x, z) in enumerate(pts[1:], 1):
        sx = x + (3 if k % 2 else -3)
        y = P.g(sx, z)
        if abs(y - P.g(x, z)) <= 2:
            lamp(w, sx, y, z, height=3, post=(B.SPRUCE_FENCE, 0), light=(B.GLOWSTONE, 0), cap=(B.WOOD_SLAB, 5))
            claim_cells([(sx, z)], 1)


def build(w, rng, stats):
    placed = houses(w, rng, stats)
    yard(w, rng)
    beacon(w, rng)
    pumpkins(w, rng)
    lamps_for(w, rng)
    return placed
