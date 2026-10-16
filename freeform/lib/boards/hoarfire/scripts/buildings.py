"""Hoarfire's buildings, one family of timber over stone: the Hearth Lodge (the spawn), Emberstead's barn and
farmhouse, and the Ice Hut on the Rime Tarn. Each is the library's house (posts at the corners, a laid course at
every storey's head, a gable or gambrel roof) and then what makes it this building: the lodge's porch, its open
doorway, beam ends and a hearth; the barn's wide doors and hay; the hut's stove pipe.

    everything(w, rng, stats)
"""
import math

import land
import plan as P
from pgmvox import B
from pgmvox.built import build as BLD
from pgmvox.core.orient import ladder, stair

LODGE = dict(ground=[(B.COBBLE, 0), (B.STONE, 5), (B.STONE, 0), (B.COBBLE, 0)], upper=[(B.PLANKS, 1)], post=1,
             gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS,
             slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.PANE, 0), chimney=(B.BRICK, 0),
             chimney_cap=(B.NETHER_FENCE, 0))
BARN = dict(LODGE, ground=[(B.PLANKS, 1)], upper=[(B.PLANKS, 1)], window=(B.SPRUCE_FENCE, 0))
FARM = dict(LODGE, ground=[(B.BRICK, 0)], upper=[(B.PLANKS, 1)])
HUT = dict(LODGE, ground=[(B.PLANKS, 1)], upper=[(B.PLANKS, 1)], roof=(B.PLANKS, 1), stair=B.SPRUCE_STAIRS,
           slab=(B.WOOD_SLAB, 1), gable=(B.PLANKS, 5))


def ground_at(w, floor):
    """The ground under a footprint's column, for the plate's fill: never below a few blocks under the floor, so a
    wall over a dip is underpinned and nothing hangs a column into the void."""
    from dress import top
    return lambda x, z: max(top(w, x, z), floor - 4)


def spec(key):
    return next(b for b in P.BUILDINGS if b[0] == key)


def centre(key):
    _, x0, z0, x1, z1, floor, _, _ = spec(key)
    return (x0 + x1 + 1) / 2, (z0 + z1 + 1) / 2, x1 - x0 + 1, z1 - z0 + 1, floor


def lodge(w, r):
    cx, cz, L, W, floor = centre("lodge")
    out = BLD.house(w, BLD.House(cx, cz, 0, L=L, W=W, floor=floor, storeys=2, storey=4, style=LODGE, jetty=True,
                                 door=1, chimney=False, roof="gable", pitch=1, overhang=1),
                    ground_at=ground_at(w, floor), rng=r)
    _, x0, z0, x1, z1, _, _, _ = spec("lodge")
    eave = out["eave"]
    # the doorway: three wide and three high in the south wall, a laid spruce lintel over it
    for x in (-1, 0, 1):
        for y in range(floor + 1, floor + 4):
            w.set(x, y, z1, B.AIR)
        w.set(x, floor, z1, B.STONEBRICK, 0)
    for x in (-2, -1, 0, 1, 2):
        w.set(x, floor + 4, z1, B.LOG, 1 | 4)
    for x in (-2, 2):
        for y in range(floor + 1, floor + 4):
            w.set(x, y, z1, B.LOG, 1)
    # beam ends where the storeys meet: the laid course's logs run a block past every corner
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        sx = -1 if x == x0 else 1
        sz = -1 if z == z0 else 1
        w.set(x + sx, floor + 4, z, B.LOG, 1 | 4)
        w.set(x, floor + 4, z + sz, B.LOG, 1 | 8)
    # posts every four along the long walls on the ground storey too, standing a block proud of the stone
    for x in range(x0 + 4, x1 - 2, 4):
        for z, sz in ((z0, -1), (z1, 1)):
            if abs(x) <= 2 and z == z1:
                continue
            for y in range(floor + 1, floor + 4):
                w.set(x, y, z + sz, B.LOG, 1)
            w.set(x, floor, z + sz, B.STONEBRICK, 0)
    # the stoop: a stone-brick landing before the door under the jetty, two steps down to the court, and a post
    # with a lantern either side of it
    pz0, pz1 = z1 + 1, z1 + 3
    for x in range(-3, 4):
        for z in range(pz0, pz1 + 1):
            w.set(x, floor, z, B.STONEBRICK, 0)
            for y in range(floor + 1, floor + 4):
                w.set(x, y, z, B.AIR)
        w.set(x, floor, pz1 + 1, B.STONEBRICK_STAIRS, stair("n"))
    for x in (-4, 4):
        for y in range(floor + 1, floor + 3):
            w.set(x, y, pz1, B.SPRUCE_FENCE, 0)
        w.set(x, floor + 3, pz1, B.JACK, 0)
        w.set(x, floor, pz1, B.STONEBRICK, 0)
    # the team's banners either side of the door, and lanterns (jack-o-lanterns) on the porch posts
    for x in (-5, 5):
        w.banner(x, floor + 3, z1 + 1, 1, [("bs", 15), ("flo", 15)], wall_facing=3)
    # the chimney: a stack of brick on the east gable, rising past the ridge, a smoking crown of nether fence
    for y in range(floor - 1, floor + 16):
        for dz in (-1, 0):
            w.set(x1 + 1, y, (z0 + z1) // 2 + dz, B.BRICK, 0)
    w.set(x1 + 1, floor + 16, (z0 + z1) // 2, B.NETHER_FENCE, 0)
    w.set(x1 + 1, floor + 16, (z0 + z1) // 2 - 1, B.NETHER_FENCE, 0)
    # inside: the hearth on the east wall (lava behind iron bars in a brick surround), tables, light
    hz = (z0 + z1) // 2
    for dz in (-1, 0):
        w.set(x1 - 1, floor, hz + dz, B.NETHERRACK, 0)
        w.set(x1 - 1, floor + 1, hz + dz, B.LAVA, 0)
        w.set(x1 - 2, floor + 1, hz + dz, B.IRON_BARS, 0)
        w.set(x1 - 1, floor + 2, hz + dz, B.BRICK, 0)
        w.set(x1 - 2, floor + 2, hz + dz, B.BRICK_STAIRS, stair("e", upside_down=True))
    for x in range(x0 + 3, x1 - 3, 6):
        w.set(x, floor + 4, (z0 + z1) // 2, B.GLOWSTONE, 0)
    # two long tables against the back wall, benches of spruce stairs before them, the team's banner between
    for xa, xb in ((x0 + 3, -3), (3, x1 - 4)):
        for x in range(xa, xb + 1):
            w.set(x, floor + 1, z0 + 1, B.SPRUCE_FENCE, 0)
            w.set(x, floor + 2, z0 + 1, B.WOOD_SLAB, 1)
            w.set(x, floor + 1, z0 + 2, B.SPRUCE_STAIRS, stair("s"))
    w.banner(0, floor + 3, z0 + 1, 1, [("bs", 15), ("cr", 15)], wall_facing=3)
    # the upper floor's ladder, and a hatch in it, so the gallery over the hall is reached
    for y in range(floor + 1, floor + 5):
        w.set(x0 + 1, y, z0 + 1, B.LADDER, ladder("n"))
    w.set(x0 + 1, floor + 4, z0 + 1, B.LADDER, ladder("n"))
    return out


def barn(w, r):
    cx, cz, L, W, floor = centre("barn")
    out = BLD.house(w, BLD.House(cx, cz, 0, L=L, W=W, floor=floor, storeys=1, storey=5, style=BARN, door=1,
                                 chimney=False, roof="gambrel", pitch=1, overhang=1), ground_at=ground_at(w, floor), rng=r)
    _, x0, z0, x1, z1, _, _, _ = spec("barn")
    mx = (x0 + x1) // 2
    for x in range(mx - 1, mx + 2):
        for y in range(floor + 1, floor + 4):
            w.set(x, y, z1, B.AIR)
    for x in (mx - 2, mx + 2):
        for y in range(floor + 1, floor + 5):
            w.set(x, y, z1 + 1, B.LOG, 1)
    for x in range(mx - 2, mx + 3):
        w.set(x, floor + 4, z1 + 1, B.LOG, 1 | 4)
    # the barn's lower course in cobble, its hay inside, stacked against the back wall
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            if w.id(x, floor + 1, z) == B.PLANKS:
                w.set(x, floor + 1, z, B.COBBLE, 0)
    for z in (z0, z1):
        pass
    for x in range(x0 + 1, x1):
        for y in range(floor + 1, floor + 1 + (2 if x % 3 else 3)):
            w.set(x, y, z0 + 1, B.HAY, 0)
    return out


def farmhouse(w, r):
    cx, cz, L, W, floor = centre("farmhouse")
    return BLD.house(w, BLD.House(cx, cz, 0, L=L, W=W, floor=floor, storeys=2, storey=4, style=FARM, door=1,
                                  chimney=True, roof="gable", pitch=1, overhang=1), ground_at=ground_at(w, floor), rng=r)


def hut(w, r):
    from dress import top
    _, x0, z0, x1, z1, _, _, _ = spec("hut")
    floor = max(top(w, x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    cx, cz = (x0 + x1 + 1) / 2, (z0 + z1 + 1) / 2
    out = BLD.house(w, BLD.House(cx, cz, 0, L=x1 - x0 + 1, W=z1 - z0 + 1, floor=floor, storeys=1, storey=4,
                                 style=HUT, door=1, chimney=False, roof="gable", pitch=1, overhang=1),
                    ground_at=ground_at(w, floor), rng=r)
    # a stove pipe of cobble wall through the roof, and an ice-hole in the tarn beside the hut with a fence rail
    w.set(x1 - 1, floor + 1, z0 + 1, B.FURNACE, 4)
    for y in range(floor + 2, floor + 9):
        if w.id(x1 - 1, y, z0 + 1) in (0, B.PLANKS, B.WOOD_SLAB, B.SPRUCE_STAIRS):
            w.set(x1 - 1, y, z0 + 1, B.COBBLE_WALL, 0)
    return out


def everything(w, r, stats):
    for f in (lodge, barn, farmhouse, hut):
        f(w, r)
    stats["buildings"] = 4
