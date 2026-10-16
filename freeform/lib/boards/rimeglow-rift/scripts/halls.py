"""The spawn halls: a great hall at the back of each half, a paved court before it, and the stair down to the roads.
The hall is the library's house in each half's own style; the court, porch and furniture are written through the
stamp."""
import numpy as np

from pgmvox import B
from pgmvox.built import build as BLD
from stamp import AIR, Stamp
import gates as GT

FLOOR = 71                                   # the court's level
HALL = dict(cx=13.5, cz=-81.5, L=23, W=9)    # x 2..24, z -86..-78
HALL_SOUTH = -78                             # the south wall's row
COURT = (-1, -77, 27, -64)                   # x0, z0, x1, z1 of the paved court

RIME = dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONE, 5)], upper=[(B.PLANKS, 1)], post=1,
            gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS,
            slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.STAINED_PANE, 3), chimney=(B.STONEBRICK, 0))
EMBER = dict(ground=[(B.NETHER_BRICK, 0)], upper=[(B.STAINED_CLAY, 12)], post=0, gable=(B.PLANKS, 5),
             floor=(B.PLANKS, 5), roof=(B.BRICK, 0), stair=B.BRICK_STAIRS, slab=(B.SLAB, 4), door=B.DARK_OAK_DOOR,
             window=(B.STAINED_PANE, 1), chimney=(B.NETHER_BRICK, 0))


def build(w, H, south):
    S = Stamp(w, south)
    style = EMBER if south else RIME
    sign = -1 if south else 1

    def hs(cx, cz):
        return (-1 - cx, -1 - cz) if south else (cx, cz)
    cx, cz = hs(HALL["cx"], HALL["cz"])
    heading = 180 if south else 0
    # the court and the pad under the hall are levelled and cleared first
    for x in range(COURT[0] - 3, COURT[2] + 4):
        for z in range(-95, COURT[3] + 3):
            for y in range(FLOOR + 1, FLOOR + 30):
                if S.get(x, y, z)[0] in (B.SNOW_LAYER, B.AIR):
                    pass
    for x in range(COURT[0], COURT[2] + 1):
        for z in range(-90, COURT[3] + 1):
            S.foot(H, x, z, FLOOR, "rock")
            S.clear(x, FLOOR + 1, z, x, FLOOR + 26, z)
    door = BLD.house(w, BLD.House(cx, cz, heading, L=HALL["L"], W=HALL["W"], floor=FLOOR, storeys=2, style=style, jetty=False,
                                  door=1, chimney=True, roof="gable", pitch=1, overhang=1,
                                  windows=BLD.window_rhythm(period=4, rows=((2, 3), (2, 3)), margin=2.0)),
                     ground_at=lambda x, z: int(H[x - w.x0, z - w.z0]))
    # the paved court: a quarter of four stones in cells of three, a border course, and a hearth ring in the middle
    x0, z0, x1, z1 = COURT
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            pick = ((x // 3) * 7 + (z // 3) * 13 + ((x * 3 + z * 5) % 7 == 0)) % 4
            S.set(x, FLOOR, z, "plinth" if edge else ("pave_a", "pave_b", "pave_c", "pave_d")[pick])
    mx, mz = 13, -70
    for dx in range(-3, 4):                                  # the hearth: a ring of stone round a bed of embers
        for dz in range(-3, 4):
            r = max(abs(dx), abs(dz))
            if r == 3 and abs(dx) + abs(dz) < 6:
                S.set(mx + dx, FLOOR, mz + dz, "wall")
                S.set(mx + dx, FLOOR + 1, mz + dz, "slab_stone")
            elif r == 2:
                S.set(mx + dx, FLOOR, mz + dz, "hot")
            elif r < 2:
                S.set(mx + dx, FLOOR, mz + dz, (B.NETHERRACK, 0))
                if r == 0:
                    S.set(mx + dx, FLOOR + 1, mz + dz, (B.FIRE, 0))
                elif (dx + dz) % 2 == 0:
                    S.set(mx + dx, FLOOR, mz + dz, (B.GLOWSTONE, 0))
    # the court's low wall: east and west sides, and the south edge with a gap for the stair
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            S.set(x, FLOOR + 1, z, "wall")
            S.set(x, FLOOR + 2, z, "post")
    for x in range(x0 + 1, x1):
        if 9 <= x <= 17:
            continue
        S.set(x, FLOOR + 1, z1, "wall")
        S.set(x, FLOOR + 2, z1, "post")
    for x in (x0, 5, 9, 17, 21, x1):                           # piers with a lit head
        for z in (z1,) if x not in (x0, x1) else (z0 + 1, z1):
            S.set(x, FLOOR + 1, z, "wall")
            S.set(x, FLOOR + 2, z, "wall")
            S.set(x, FLOOR + 3, z, "light")
    # the stair down through the gap, five wide, the rise carried on masonry
    for k in range(1, 7):
        for x in range(10, 17):
            S.stair(x, FLOOR - k, z1 + k, "wall", "n", False)
            for yy in range(FLOOR - k - 1, FLOOR - k):
                if S.get(x, yy, z1 + k)[0] in (0, B.SNOW_LAYER):
                    S.set(x, yy, z1 + k, "rock")
            S.clear(x, FLOOR - k + 1, z1 + k, x, FLOOR + 3, z1 + k)
    # the porch: a colonnade along the hall's south wall under a slab roof
    pz = HALL_SOUTH + 1
    for x in range(3, 24):
        S.set(x, FLOOR + 4, pz, "log", 4) if False else S.log(x, FLOOR + 4, pz, "x")
        S.set(x, FLOOR + 5, pz, "roof_slab")
        S.set(x, FLOOR + 5, pz - 1, "roof_slab")
    for x in range(3, 24, 4):
        for y in range(FLOOR + 1, FLOOR + 4):
            S.log(x, y, pz)
        S.set(x, FLOOR + 3, pz + 1, "light")

    # a cross-gabled pavilion over the door, and a louvred cupola on the ridge
    roof_style = style
    peak = door["roof"].peak
    def image(box):
        x0_, z0_, x1_, z1_ = box
        return (-1 - x1_, -1 - z1_, -1 - x0_, -1 - z0_) if south else box
    for x in (10, 16):
        for z in (-74,):
            for y in range(FLOOR + 1, FLOOR + 5):
                S.log(x, y, z)
            S.set(x, FLOOR + 4, z, "plank")
        S.set(x, FLOOR + 5, -74, "plank")
    for z in (-78, -77, -76, -75, -74):
        for x in (10, 16):
            S.log(x, FLOOR + 5, z, "z")
    pav = BLD.RoofField("gable", image((10, -78, 16, -74)), overhang=1, base_y=FLOOR + 6, ridge_along_x=False)
    BLD.lay_roof(w, pav, roof_style["roof"], roof_style["stair"], roof_style["slab"], inside=lambda x, z: False)
    for k in range(-1, 2):
        S.set(13, FLOOR + 5, -78 + 0, "log") if False else None
    for dx in (12, 14):
        for dz in (-83, -81):
            for y in range(peak - 1, peak + 4):
                S.log(dx, y, dz)
    for y in (peak + 1, peak + 2):
        for dx, dz in ((13, -83), (13, -81), (12, -82), (14, -82)):
            S.set(dx, y, dz, "pane")
    for dx in range(12, 15):
        for dz in range(-83, -80):
            S.set(dx, peak, dz, "plank")
    S.set(13, peak + 1, -82, "light")
    cup = BLD.RoofField("hip", image((12, -83, 14, -81)), overhang=1, base_y=peak + 4)
    BLD.lay_roof(w, cup, roof_style["roof"], roof_style["stair"], roof_style["slab"], inside=lambda x, z: False)
    GT.banner(S, 7, FLOOR + 1, -65)
    GT.banner(S, 19, FLOOR + 1, -65)

    # inside, a hall of two heights: the upper floor cut away but for a gallery round three walls, tie beams across, and
    # lamps hung from them
    f = FLOOR
    up = f + 4
    zn = -85
    for x in range(3, 24):
        for z in range(-85, -78):
            gallery = z <= -84 or x <= 4 or x >= 22
            if not gallery:
                S.set(x, up, z, AIR)
    for x in range(3, 24):                                        # the gallery's rail on its open edges
        S.set(x, up + 1, -83, "fence")
    for z in range(-83, -78):
        S.set(5, up + 1, z, "fence")
        S.set(21, up + 1, z, "fence")
    for x in (7, 11, 15, 19):
        for z in range(-85, -78):
            S.log(x, up, z, "z") if z > -84 else None
        S.set(x, up - 1, -81, "fence"); S.set(x, up - 2, -81, "fence"); S.set(x, up - 3, -81, "light")
    for k in range(4):
        S.stair(3 + k * 0, f + 1 + k, -79 - k, "plank", "n")
        for yy in range(f + 1, f + 1 + k):
            S.set(3, yy, -79 - k, "plank")
    S.clear(3, up, -81, 3, up, -79)
    # the table, its benches, and the hearth in the north wall
    zc = -81
    for x in range(7, 20):
        S.set(x, f + 1, zc, "slab")
        if x % 4 == 3:
            S.set(x, f, zc, "fence")
        elif not 11 <= x <= 15:                                   # the aisle from the door stays open
            S.stair(x, f + 1, zc - 2, "plank", "s")
            S.stair(x, f + 1, zc + 2, "plank", "n")
    for x in range(12, 15):                                       # the hearth: stone all round the fire
        for y in range(f + 1, f + 4):
            S.set(x, y, -85, "wall")
        S.set(x, f + 1, -85, "wall")
    S.set(13, f + 1, -85, (B.NETHERRACK, 0)); S.set(13, f + 2, -85, (B.FIRE, 0))
    S.set(12, f + 3, -85, "wall"); S.set(13, f + 3, -85, "wall"); S.set(14, f + 3, -85, "wall")
    for x in (12, 14):
        S.set(x, f + 2, -85, "wall")
    S.set(13, f, -85, "wall")
    # a rug before the hearth, and banners in the half's colour down the north wall between the windows
    base, edge = (3, 9) if not south else (1, 14)
    for x in range(10, 17):
        for z in (-84, -83):
            S.set(x, f + 1, z, (B.CARPET, edge if x in (10, 16) or z == -84 else base))
    for x in (5, 6, 7, 8, 9, 10, 16, 17, 18, 19, 20, 21):
        if S.get(x, f + 3, -86)[0] in (B.STAINED_PANE, B.AIR) or S.get(x, f + 2, -86)[0] in (B.STAINED_PANE, B.AIR):
            continue
        if any(S.get(x + dx, f + 3, -85)[0] == B.WALL_BANNER for dx in (-2, -1, 1, 2)):
            continue
        S.banner(x, f + 3, -85, 6 if not south else 14, [("bs", 15 if not south else 11), ("ts", 12 if not south else 4)],
                 wall_facing=3)
    for x in (5, 21):                                              # a weapon rack and a store of hay on the long walls
        S.set(x, f + 1, -85, "fence"); S.set(x, f + 2, -85, "fence")
        S.set(x + (1 if x == 5 else -1), f + 1, -85, (B.HAY, 0) if south else "slab")
    return S
