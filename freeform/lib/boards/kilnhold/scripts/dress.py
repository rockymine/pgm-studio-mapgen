"""Dressing: what stands on the Crown besides the objectives (a sunken court for the beacon, pillboxes, cover, a cooling
basin, the mast on its podium) and what lies on the caldera floor (boulders, bare trees, lamp posts).

Everything is decided from the plan's claims first: the ways players walk and the ground the objectives cover are kept
clear, and cover keeps its distance from a goal.
"""
import math

import numpy as np

import kit
import plan as P
from kit import (AIR, ANDESITE, BARS, BLACK, COAL, COBBLE, GLOW, GREY, IRON, LAVA, LOG_DARK, ORANGE, PAND, RSMOOTH,
                 SB, SBCHISEL, SEA, STONE, TEAM_WOOL, WATER, put, fill)
from pgmvox import B, rng
from pgmvox.scenery import trees

WALL = (B.COBBLE_WALL, 0)
Y = P.CROWN


def disc(cx, cz, r):
    """The cells within r of the point (cx, cz), cx and cz at block centres."""
    return [(x, z) for x in range(int(cx - r) - 1, int(cx + r) + 2) for z in range(int(cz - r) - 1, int(cz + r) + 2)
            if math.hypot(x + 0.5 - cx, z + 0.5 - cz) <= r]


# ---------------------------------------------------------------------------------------------------------------
def beacon_court(w):
    """A court sunk a block into the deck round the beacon, three steps down at its rim, the team's wool inlaid; the
    monument floats four blocks over its floor."""
    bx, bz = P.BEACON_AT
    cx, cz = bx + 0.5, bz + 0.5
    for x, z in disc(cx, cz, 6.5):
        r = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
        if r <= 4.6:
            put(w, x, Y, z, AIR)
            put(w, x, Y - 1, z, PAND if r > 1.9 else TEAM_WOOL)
            if abs(x + 0.5 - cx) < 0.6 or abs(z + 0.5 - cz) < 0.6:
                put(w, x, Y - 1, z, TEAM_WOOL)
        elif r <= 5.6:
            put(w, x, Y, z, RSMOOTH)
        else:
            put(w, x, Y, z, SB if (x + z) % 2 else PAND)
    # four stairs down into the court, one on each side
    for dx, dz, rises in ((5, 0, "e"), (-5, 0, "w"), (0, 5, "s"), (0, -5, "n")):
        pass


def pillbox(w, cx, cz, door="n"):
    """A stone brick pillbox seven by five, two high inside under a slab roof, slits on its front, a door at the back."""
    x0, x1, z0, z1 = cx - 3, cx + 3, cz - 2, cz + 2
    fill(w, x0, Y + 1, z0, x1, Y + 4, z1, SB)
    fill(w, x0 + 1, Y + 1, z0 + 1, x1 - 1, Y + 3, z1 - 1, AIR)
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            put(w, x, Y + 1, z, kit.SBCHISEL if x in (x0, x1) else SB)
        put(w, x, Y + 4, z0, (B.SLAB, 5))
        put(w, x, Y + 4, z1, (B.SLAB, 5))
    for x in range(x0, x1 + 1):                                   # the roof, a slab over the walls and the span
        for z in range(z0, z1 + 1):
            put(w, x, Y + 4, z, SB if (x in (x0, x1) or z in (z0, z1)) else PAND)
    front = z1 if door == "n" else z0                              # the side that faces the front (+z) has the slits
    for x in (cx - 2, cx, cx + 2):
        put(w, x, Y + 2, z1, AIR)
        put(w, x, Y + 3, z1, AIR)
    back = z0
    for y in (Y + 1, Y + 2):
        put(w, cx, y, back, AIR)
    put(w, cx, Y + 3, back, kit.SBCHISEL)
    for x in range(x0 + 1, x1):
        put(w, x, Y + 1, z0 + 1, (B.SLAB, 5)) if x in (x0 + 1, x1 - 1) else None
    put(w, cx, Y + 3, cz, GLOW)


def cover_block(w, x0, z0, nx, nz, hgt=2):
    fill(w, x0, Y + 1, z0, x0 + nx - 1, Y + hgt, z0 + nz - 1, SB)
    for x in range(x0, x0 + nx):
        for z in range(z0, z0 + nz):
            put(w, x, Y + hgt, z, PAND if (x + z) % 2 else SB)
    for x in range(x0, x0 + nx):
        put(w, x, Y + 1, z0, SBCHISEL)
        put(w, x, Y + 1, z0 + nz - 1, SBCHISEL)


def basin(w):
    """A cooling basin: stone brick walls round a pool, a catwalk across it."""
    x0, x1, z0, z1 = 26, 42, -90, -79
    fill(w, x0 - 1, Y, z0 - 1, x1 + 1, Y, z1 + 1, RSMOOTH)
    fill(w, x0, Y - 3, z0, x1, Y, z1, AIR)
    fill(w, x0, Y - 4, z0, x1, Y - 4, z1, kit.OBSIDIAN)
    fill(w, x0, Y - 3, z0, x1, Y - 1, z1, WATER)
    for x in range(x0 - 1, x1 + 2):
        for z in (z0 - 1, z1 + 1):
            put(w, x, Y + 1, z, SB)
    for z in range(z0 - 1, z1 + 2):
        for x in (x0 - 1, x1 + 1):
            put(w, x, Y + 1, z, SB)
    for x in range(x0, x1 + 1):                                   # a catwalk across, on a pier at each end
        put(w, x, Y, -85, PAND if x % 2 else SB)
        put(w, x, Y, -84, PAND if x % 2 else SB)
        put(w, x, Y + 1, -86, BARS)
        put(w, x, Y + 1, -83, BARS)
    for x in (x0 + 5, x0 + 11):
        for z in (-85, -84):
            for yy in range(Y - 3, Y):
                put(w, x, yy, z, SB)
    # the ways in: a gap in the wall at each end of the catwalk
    for z in (-85, -84):
        put(w, x0 - 1, Y + 1, z, AIR)
        put(w, x1 + 1, Y + 1, z, AIR)


def podium_and_mast(w):
    """The mast on a three-step podium: a stone brick pier, an iron shaft, a lantern."""
    for k, half in enumerate((6, 5, 4)):
        for x in range(-half, half):
            for z in range(-76 - half + 1, -76 + half + 1):
                put(w, x, Y + 1 + k, z, SB if (x + z) % 2 else PAND)
    for x in range(-1, 1):
        for z in range(-77, -75):
            for y in range(Y + 4, Y + 11):
                put(w, x, y, z, SB if y > Y + 4 else SBCHISEL)
    for y in range(Y + 11, Y + 24):
        put(w, -1, y, -77, IRON)
        put(w, 0, y, -77, IRON)
    put(w, -1, Y + 24, -77, SEA)
    put(w, 0, Y + 24, -77, SEA)


def battery(w):
    """The east battery: gun pits sunk in the deck, an iron breech and barrel in each, a low wall behind."""
    for cx in (34, 40):
        for x in range(cx - 2, cx + 3):
            for z in range(-66, -61):
                put(w, x, Y, z, AIR)
                put(w, x, Y - 1, z, kit.BLACK)
        for z in (-67, -60):
            for x in range(cx - 3, cx + 4):
                put(w, x, Y + 1, z, SB)
        for x in (cx - 3, cx + 3):
            for z in range(-67, -59):
                put(w, x, Y + 1, z, SB)
        for z in range(-65, -62):                                  # breech and barrel
            put(w, cx, Y, z, IRON)
        put(w, cx, Y + 1, -64, IRON)
        put(w, cx, Y + 1, -63, IRON)


def crown(w):
    beacon_court(w)
    for cx, cz in ((-12, -62), (11, -62)):
        pillbox(w, cx, cz)
    for cx, cz in ((-45, -64), (44, -64)):
        pillbox(w, cx, cz)
    for x0, z0, nx, nz in ((-22, -75, 4, 2), (19, -75, 4, 2), (-50, -78, 2, 4), (49, -78, 2, 4), (-10, -86, 5, 2),
                           (6, -86, 5, 2), (-26, -88, 3, 3), (22, -66, 3, 2), (-20, -64, 3, 2)):
        cover_block(w, x0, z0, nx, nz)
    basin(w)
    podium_and_mast(w)
    battery(w)


# ---------------------------------------------------------------------------------------------------------------
def boulder(w, x, z, r, rg):
    base = w.top(x, z)
    if base < 1:
        return
    rx, rz, rh = r * rg.uniform(0.8, 1.2), r * rg.uniform(0.8, 1.2), r * rg.uniform(0.6, 0.9)
    for dx in range(-int(rx) - 1, int(rx) + 2):
        for dz in range(-int(rz) - 1, int(rz) + 2):
            e = (dx / rx) ** 2 + (dz / rz) ** 2
            if e > 1.0:
                continue
            hh = int(round(rh * math.sqrt(max(0.0, 1.0 - e)) + (rg.random() * 0.8 - 0.4)))
            gx, gz = x + dx, z + dz
            g = w.top(gx, gz)
            for yy in range(g - 1, g + max(hh, 0)):
                if yy >= g:
                    k = rg.random()
                    blk = STONE if k < 0.34 else ANDESITE if k < 0.64 else COBBLE if k < 0.82 else (B.STAINED_CLAY, 15)
                    put(w, gx, yy, gz, blk)


def lamp_post(w, x, z):
    g = w.top(x, z)
    for y in range(g + 1, g + 5):
        put(w, x, y, z, SB if y > g + 1 else SBCHISEL)
    put(w, x, g + 5, z, GLOW)


def field(w, L, stats):
    """Boulders, bare trees and lamp posts on the caldera floor of red's half, kept off the ways."""
    rg = rng(P.BOARD, "field")
    X, Z = w.grid()
    nx, nz = L.H.shape
    claimed = np.zeros((nx, nz), bool)

    def claim_box(x0, x1, z0, z1, pad):
        claimed[max(0, x0 - pad - P.X_MIN):x1 + pad - P.X_MIN + 1, max(0, z0 - pad - P.Z_MIN):z1 + pad - P.Z_MIN + 1] = True

    claim_box(*P.APRON_BOX[:2], *P.APRON_BOX[2:], 6)
    claim_box(P.PIT_BOX[0], P.PIT_BOX[1], P.PIT_BOX[2], P.PIT_BOX[3], 6)
    tx, tz = P.TOWER
    claimed |= np.hypot(X + 0.5 - tx, Z + 0.5 - tz) < 15
    for key in ("west", "east", "tower_entry", "pit_entry"):
        for x, z, _, _ in stats["roads"][key]:
            claim_box(x, x, z, z, 3)
    rr = np.hypot(X + 0.5, Z + 0.5)
    claimed |= rr < 27
    claimed |= L.deck
    claimed |= ~L.land
    claimed |= (L.d_in < 4)
    claimed |= L.slope > 42
    placed = []
    n_boulder = n_tree = 0
    cand = [(x, z) for x in range(-62, 62) for z in range(-56, -2)]
    order = rg.permutation(len(cand))
    for idx in order:
        x, z = cand[idx]
        if claimed[x - P.X_MIN, z - P.Z_MIN]:
            continue
        if n_boulder < 24 and (n_boulder <= n_tree * 0.7 or n_tree >= 38):
            r = float(rg.uniform(2.0, 4.0))
            if any(math.hypot(x - px, z - pz) < pr + r + 4 for px, pz, pr in placed):
                continue
            boulder(w, x, z, r, rg)
            placed.append((x, z, r))
            n_boulder += 1
        elif n_tree < 38:
            if any(math.hypot(x - px, z - pz) < pr + 5 for px, pz, pr in placed):
                continue
            g = w.top(x, z)
            trees.dead_tree(w, x, g, z, rg, int(rg.integers(4, 8)), log=B.LOG, kind=1)
            placed.append((x, z, 1.5))
            n_tree += 1
        else:
            break
    stats["boulders"], stats["trees"] = n_boulder, n_tree
    # lamp posts along the apron's front and by the pit and tower entries
    for x in (-24, -16, 15, 23):
        lamp_post(w, x, -33)
    for x in (-47, -44):
        lamp_post(w, x, -23)
    for x in (44, 47):
        lamp_post(w, x, -23)


def build(w, L, stats):
    crown(w)
    field(w, L, stats)
