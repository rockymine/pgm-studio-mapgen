"""Seamworks' finish: what each part of the board is made of, as functions of a block's position, so the generator
paints by asking rather than by deciding.

Three families. The ground is grey: the rock of the cuts (stone and andesite, cobblestone under a third) and the
ash of the crust (cyan clay with patches of black and of grey clay). What was built is white clay concrete banded
in light grey, and the steel that lines the cuts is rust. The accent is the hazard stripe, yellow and black, on
doors, and the seam's own orange."""
import numpy as np

import plan as P
from pgmvox import B
from pgmvox.geom.noise import fbm

W, H = P.W, P.H


def _sym(f):
    return (f + f[::-1, ::-1]) / 2


def _field(cell, seed, octaves=3):
    f = _sym(fbm((W, H), cell, octaves, seed=seed))
    return (f - f.min()) / (f.max() - f.min())


ROCK_A = _field(5, 11)                    # patches about five across
ROCK_B = _field(4, 12)
ASH = _field(5, 21)
WEAR = _field(6, 31)
STEP = _field(4, 41) * 2 - 1              # the wander of a flight's step edges, -1 to 1
RUST = _field(3, 51)


def _at(f, x, z):
    return f[min(max(x, 0), W - 1), min(max(z, 0), H - 1)]


def rock(x, y, z):
    """The rock of the cuts: stone with andesite patches, cobblestone in small patches under a third."""
    a = _at(ROCK_A, x, z) * 0.7 + ((x * 7 + y * 13 + z * 5) % 11) / 11 * 0.3
    b = _at(ROCK_B, (x + y * 3) % W, (z + y * 2) % H)
    if b > 0.72:
        return (B.COBBLE, 0)
    return (B.STONE, 5) if a < 0.42 else (B.STONE, 0)


def crust(x, z):
    """The ash: cyan clay, the one neutral grey the clays have, as the ground, with patches of black clay at one end
    of the stops and of the browner grey clay at the other."""
    v = _at(ASH, x, z)
    if v < 0.22:
        return (B.STAINED_CLAY, 7)
    if v > 0.8:
        return (B.STAINED_CLAY, 15)
    return (B.STAINED_CLAY, 9)


def cut_floor(x, z):
    """A worn cut floor, three blocks of one tone a third each in cells of about three."""
    k = ((x // 3) * 7 + (z // 3) * 13 + (x // 3) * (z // 3)) % 3
    return [(B.STONE, 5), (B.GRAVEL, 0), (B.STONE, 0)][k]


def built_floor(x, z):
    """A building's floor: stone bricks, polished andesite, andesite and stone, a quarter each in cells of three."""
    k = ((x // 3) * 5 + (z // 3) * 11 + (x // 3 + z // 3) * 3) % 4
    return [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)][k]


def rust(x, y, z, shade):
    """A panel's steel: streaks of brown and hardened clay running down its face, a little orange in them."""
    v = _at(RUST, x, (z + y // 4) % H) * 0.75 + (0.25 if shade else 0)
    if v > 0.86:
        return (B.STAINED_CLAY, 1)
    return (B.HARDENED_CLAY, 0) if v < 0.5 else (B.STAINED_CLAY, 12)


WALL = (B.STAINED_CLAY, 0)                # the works' concrete
BAND = (B.STAINED_CLAY, 8)                # its storey bands, corner posts and parapet
WINDOW = (B.IRON_BARS, 0)
SKYLIGHT = (B.GLASS, 0)
LIGHT = (B.GLOWSTONE, 0)
PLATE = (B.IRON_BLOCK, 0)
LUMP = (B.COBBLE, 0)
LUMP_SLAB = (B.SLAB, 3)                   # a cobblestone slab
SPOIL = [(B.DIRT, 1), (B.DIRT, 0)]
SEAM_ROCK = (B.NETHERRACK, 0)
HAZARD = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)]
CHIMNEY = (B.BRICK, 0)
TIMBER_POST = (B.SPRUCE_FENCE, 0)
TIMBER_BEAM = (B.PLANKS, 1)


def paint_rock(w):
    """Every block of plain stone on the board turned into the rock set, course by course."""
    xs = np.clip(np.arange(w.x0, w.x0 + w.sx), 0, W - 1)
    zs = np.clip(np.arange(w.z0, w.z0 + w.sz), 0, H - 1)
    XI, ZI = np.meshgrid(xs, zs, indexing="ij")
    a0 = ROCK_A[XI, ZI] * 0.7
    for y in range(1, w.sy):
        layer = w.ids[:, y, :]
        stone = (layer == B.STONE) & (w.dat[:, y, :] == 0)
        if not stone.any():
            continue
        grain = ((XI * 7 + y * 13 + ZI * 5) % 11) / 11 * 0.3
        b = ROCK_B[(XI + y * 3) % W, (ZI + y * 2) % H]
        cob = stone & (b > 0.72)
        andesite = stone & ~cob & (a0 + grain < 0.42)
        w.ids[:, y, :][cob] = B.COBBLE
        w.dat[:, y, :][cob] = 0
        w.dat[:, y, :][andesite] = 5
