"""Thawline's places, each written once in Frost's coordinates and built on both halves through a `Side`.

    roads(w)          the roads paved, bridged over the beck: gravel, andesite and cobble for Frost; coarse dirt,
                      dirt and spruce planks for Ember
    rimehall(w)       the spawn's terrace, its face and flight, the hall on its back, lamps at its front
    green(w)          Lantern Green: the paved terrace, its rose, its face and flights, the four lamps
    kettle(w)         the Kettle's floor, the four spires on its rim, the Culvert from Coldwater
    hamlet(w)         Hoarstead (Frost) and Kilnstead (Ember): four houses, two domes, a yard, woodpiles, a wheel
    watch(w)          the ruined tower on the Knoll and its beacon
    erratics(w)       the boulders the ice left in the middle field
    stack(w)          the Rimefire Stack in the rift, built once: half ice and half fire
    edges(w)          icicles under Frost's coast
"""
import math

import numpy as np

import plan as P
from pgmvox import B
from pgmvox.built import build as BLD
from pgmvox.core import orient as OR
from pgmvox.geom import noise, shapes
from pgmvox.geom.shapes import distance_in, edge_depth
from pgmvox.scenery import forms
from season import SIDES

FROST, EMBER = SIDES


def g(x, z):
    return P.g(x, z)


def inside_board(x, z):
    return P.X_MIN <= x <= P.X_MAX and P.Z_MIN <= z <= P.Z_MAX


def land(x, z):
    return inside_board(x, z) and bool(P.LAND[x - P.X_MIN, z - P.Z_MIN])


def wet(x, z):
    return inside_board(x, z) and bool(P.WET[x - P.X_MIN, z - P.Z_MIN])


def clear_above(w, side, x, y, z, n=1):
    """Clear snow and plants from the n blocks over a floor at y."""
    for k in range(1, n + 1):
        if side.get(w, x, y + k, z)[0] in (B.SNOW_LAYER, B.TALLGRASS, B.DEADBUSH, B.DOUBLE_PLANT,
                                             B.BROWN_MUSHROOM, B.RED_MUSHROOM, B.FLOWER, B.DANDELION):
            side.set(w, x, y + k, z, B.AIR)


# ---- roads ----------------------------------------------------------------------------------------------------
def road_lines():
    from pgmvox.geom.noise import spline
    return {name: spline(pts, 1.0) for name, pts in P.land.ROADS.items()}


def roads(w, rng):
    """Every road paved three wide, a third each of the side's three path blocks; a deck of planks over the beck
    where a road crosses it, with fence rails along its sides."""
    X, Z = P.X, P.Z
    paved = 0
    bridges = 0
    near = np.full(X.shape, np.inf)
    for name, line in road_lines().items():
        near = np.minimum(near, shapes.polyline(X, Z, line)[0])
    band = (near <= 1.55) & P.LAND & ~P.MADE & (Z < 0)
    rail = (near > 1.55) & (near <= 2.3) & P.LAND & (Z < 0)
    for side in SIDES:
        r = np.random.default_rng(7 if side.ember else 6)
        for i, k in np.argwhere(band):
            x, z = int(X[i, k]), int(Z[i, k])
            h = g(x, z)
            if P.WET[i, k]:
                level = h + 1
                while side.get(w, x, level + 1, z)[0] in (B.WATER, B.ICE, B.WATER_FLOW):
                    level += 1
                side.set(w, x, level + 1, z, *side.m("planks"))
                clear_above(w, side, x, level + 1, z, 2)
                bridges += 1
                continue
            side.set(w, x, h, z, *side.m("path", r))
            clear_above(w, side, x, h, z)
            if not side.ember and near[i, k] > 1.1 and r.random() < 0.45:
                side.set(w, x, h + 1, z, B.SNOW_LAYER, 0)
            paved += 1
        # rails along a deck
        for i, k in np.argwhere(rail):
            x, z = int(X[i, k]), int(Z[i, k])
            if not P.WET[i, k]:
                continue
            dk = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if band[x + dx - P.X_MIN, z + dz - P.Z_MIN]
                  and P.WET[x + dx - P.X_MIN, z + dz - P.Z_MIN]]
            if not dk:
                continue
            level = g(x, z) + 1
            while side.get(w, x, level + 1, z)[0] in (B.WATER, B.ICE, B.WATER_FLOW):
                level += 1
            side.set(w, x, level + 1, z, *side.m("planks"))
            side.set(w, x, level + 2, z, *side.m("fence"))
    return paved // 2, bridges // 2


# ---- made ground: a terrace's floor, face and flights ---------------------------------------------------------
def terrace(w, side, name, top, rng, floor_field):
    """A made terrace: its floor laid by `floor_field(x, z)` (a block, or None for the side's built floor), its rim
    a course of the side's trim, its face walled in the side's wall down to the ground where the ground outside
    lies lower, and its flights (plan.flights) set into the face, stairs one a block down to the ground. Frost's
    coordinates throughout."""
    X, Z = P.X, P.Z
    mask = P.terraces()[name]
    rim = mask & (edge_depth(mask) == 0)
    mine = [f for f in P.flights() if f[1] == name]
    flight_cells = {c for f in mine for c in f[4]}
    for i, k in np.argwhere(mask):
        x, z = int(X[i, k]), int(Z[i, k])
        blk = floor_field(x, z)
        side.set(w, x, top, z, *(blk or floor_cell(side, x, z)))
        clear_above(w, side, x, top, z, 2)
    for i, k in np.argwhere(rim):
        x, z = int(X[i, k]), int(Z[i, k])
        low = min((g(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if land(x + dx, z + dz) and not mask[x + dx - P.X_MIN, z + dz - P.Z_MIN]), default=top)
        if low >= top:
            continue
        for y in range(low - 1, top):
            side.set(w, x, y, z, *side.m("wall", rng))
        if (x, z) not in flight_cells:
            side.set(w, x, top, z, *side.m("trim"))
    for _, _, _, d, rim_cells, steps in mine:
        for x, y, z in steps:
            for yy in range(g(x, z), y):
                side.set(w, x, yy, z, *side.m("wall", rng))
            side.set(w, x, y, z, side.m("stair"), OR.stair(OR.opposite(d)))
            clear_above(w, side, x, y, z, 2)
        for x, z in rim_cells:
            side.set(w, x, top, z, *floor_cell(side, x, z))
    return int(mask.sum())


def floor_cell(side, x, z):
    """The built floor: the side's four blocks a quarter each, one to every cell of two by two."""
    v = (x // 2 * 73856093) ^ (z // 2 * 19349663)
    return side.pal["floor"][(v >> 3) % 4]


def lamp(w, side, x, z, y, height=3):
    """A lamp post on a floor at y: a plinth of the trim, a post of the side's fence, its light, a slab over it."""
    side.set(w, x, y + 1, z, *side.m("trim"))
    for k in range(2, 2 + height):
        side.set(w, x, y + k, z, *side.m("fence"))
    side.set(w, x, y + 2 + height, z, *side.m("light"))
    s = side.m("wood_slab")
    side.set(w, x, y + 3 + height, z, s[0], s[1])


# ---- Rimehall -------------------------------------------------------------------------------------------------
def rimehall(w, rng):
    """The spawn's terrace at 53, its floor in the built set with a band of the team's clay across its front, its
    face and its flight down to the Hall Road; the hall on its back, two storeys, its door on the terrace; lamps."""
    sy = P.land.SPAWN_Y
    out = {}
    for side in SIDES:
        r = np.random.default_rng(11 + side.ember)

        def floor(x, z):
            if abs(z - (-81)) < 0.5 and abs(x) <= 9:
                return side.m("team_clay")
            return None
        terrace(w, side, "hall", sy, r, floor)
        hall = P.HALL
        hx, hz = side.p(hall["cx"] + 0.5, hall["cz"] + 0.5)
        res = BLD.house(w, BLD.House(hx, hz, side.heading(hall["heading"]), L=hall["L"], W=hall["W"], floor=sy,
                                     storeys=2, style=side.house, door=1, chimney=True, roof="gable", pitch=1),
                        ground_at=lambda x, z: sy, rng=np.random.default_rng(21))
        out[side.name] = res
        if not side.ember:
            snow_roof(w, res["roof"])
        for lx in (-9, 8):
            lamp(w, side, lx, -80, sy)
        for bx in (-6, 5):                              # the team's banners either side of the hall's door
            x, z = side.c(bx, -86)
            w.banner(x, sy + 3, z, side.pal["banner"], [("bs", 0 if side.ember else 15), ("mc", 15 if not side.ember else 4)],
                     wall_facing=3 if not side.ember else 2)
        for bx in (-4, 3):                              # a brazier either side of the Hall Stair's head
            side.set(w, bx, sy + 1, -80, *side.m("trim"))
            if side.ember:
                side.set(w, bx, sy + 2, -80, B.NETHERRACK)
                side.set(w, bx, sy + 3, -80, B.FIRE)
            else:
                side.set(w, bx, sy + 2, -80, B.PACKED_ICE)
                side.set(w, bx, sy + 3, -80, B.SEA_LANTERN)
    return out


def snout(w):
    """Where the Rime Beck leaves the Glacier: an arch of packed ice over its first three blocks, snow on it; on
    Ember's side the spring comes out under an arch of black clay and coal."""
    x0, z0 = P.land.BECK[0]
    for side in SIDES:
        r = np.random.default_rng(151)
        for dz in (0, 1, 2):
            for dx in range(-3, 4):
                x, z = x0 + dx, z0 + dz
                h = g(x0, z0) + 1
                top = h + 3 - (1 if abs(dx) == 3 else 0) - dz // 2
                for y in range(h, top + 1):
                    inner = abs(dx) <= 1 and y < top - 0
                    if inner:
                        continue
                    if side.get(w, x, y, z)[0] in (B.AIR, B.SNOW_LAYER):
                        side.set(w, x, y, z, *((B.PACKED_ICE, 0) if not side.ember else
                                               ((B.COAL_BLOCK, 0) if r.random() < 0.5 else (B.STAINED_CLAY, 15))))
                if not side.ember and side.get(w, x, top + 1, z)[0] == B.AIR:
                    side.set(w, x, top + 1, z, B.SNOW_LAYER, 0)


def snow_roof(w, field):
    """A layer of snow on every cube of a Frost roof that has sky over it."""
    n = 0
    for x, z in field.cells():
        y = field.crown(x, z)
        if w.id(x, y, z) in (B.PLANKS, B.STONEBRICK, B.STONE, B.COBBLE) and w.id(x, y + 1, z) == B.AIR:
            w.set(x, y + 1, z, B.SNOW_LAYER, 0)
            n += 1
    return n


# ---- Lantern Green --------------------------------------------------------------------------------------------
def green(w, rng):
    """Lantern Green at 48: its floor a rose in the side's inlay over the built set (six arms for Frost, a snowflake;
    eight for Ember, a sun), its face where the field lies lower, two flights (west to the Green Road, south to the
    field), and four lamps round the monument at seven blocks."""
    gy = P.land.GREEN_Y
    gx, gz = P.land.GREEN
    cx, cz = gx + 0.5, gz + 0.5
    for side in SIDES:
        r = np.random.default_rng(31 + side.ember)
        arms = 6 if not side.ember else 8

        def rose(x, z):
            dx, dz = x + 0.5 - cx, z + 0.5 - cz
            d = math.hypot(dx, dz)
            if d < 1.6:
                return side.m("inlay")
            if 3.6 <= d < 4.6:
                return side.m("inlay2")
            a = math.atan2(dz, dx) * arms / (2 * math.pi)
            if 4.6 <= d < 8.2 and abs(a - round(a)) * 2 * math.pi * d / arms < 0.55:
                return side.m("inlay")
            if d >= 8.6:
                return side.m("wall_dark")
            return None
        terrace(w, side, "green", gy, r, rose)
        for lx, lz in P.LANTERN_POSTS:
            lamp(w, side, lx, lz, gy)


# ---- the Kettle -----------------------------------------------------------------------------------------------
def kettle(w, rng):
    """The Kettle's floor frozen for Frost (packed ice) and burnt for Ember (netherrack, coal and black clay), four
    spires on its rim, and the Culvert: a passage two wide and three high from Coldwater's north shore down to the
    Kettle's floor, cut through the rock, its walls glazed with ice for Frost and seamed with glowstone for Ember."""
    X, Z = P.X, P.Z
    kx, kz = P.land.KETTLE
    d = np.hypot(X - kx, Z - kz)
    floor = P.LAND & (d < 8) & (P.H <= P.land.KETTLE_FLOOR + 1)
    for side in SIDES:
        r = np.random.default_rng(41 + side.ember)
        for i, k in np.argwhere(floor):
            x, z = int(X[i, k]), int(Z[i, k])
            h = g(x, z)
            if side.ember:
                v = r.random()
                blk = (B.NETHERRACK, 0) if v < 0.4 else (B.COAL_BLOCK, 0) if v < 0.65 else (B.STAINED_CLAY, 15)
            else:
                blk = (B.PACKED_ICE, 0) if r.random() < 0.8 else (B.ICE, 0)
            side.set(w, x, h, z, *blk)
            clear_above(w, side, x, h, z)
        # the spires on the rim
        for n, (px, pz) in enumerate(P.KETTLE_PILLARS):
            y0 = g(px, pz)
            lean = (0.4 * (px - kx), 0.4 * (pz - kz))
            tall = 15 + (n * 3) % 6
            ax, az = side.p(px + 0.5, pz + 0.5)
            lx, lz = side.p(*lean)
            m = forms.spike(w, [(ax, y0 - 2, az), (ax + 0.4 * lx, y0 + tall * 0.55, az + 0.4 * lz),
                                (ax + lx, y0 + tall, az + lz)], (2.8, 0.3, 1.35), sides=0, flutes=(5, 0.12),
                            twist=20, rough=0.06, cell=7, seed=50 + n)
            mats = side.pal["spire"]
            idx = np.argwhere(m)
            for i, y, k in idx:
                if w.ids[i, y, k] in (0, B.SNOW_LAYER, B.TALLGRASS) or y >= y0:
                    blk = mats[int(r.integers(len(mats)))]
                    w.ids[i, y, k], w.dat[i, y, k] = blk
            if len(idx):
                top = idx[np.argmax(idx[:, 1])]
                i, y, k = (int(v) for v in top)
                w.ids[i, y, k], w.dat[i, y, k] = side.m("spire_cap")
                if side.ember:
                    w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.FIRE, 0
        # the Culvert
        pts = P.CULVERT
        for (x0, z0), (x1, z1), y0, y1 in zip(pts, pts[1:], P.CULVERT_FLOOR, P.CULVERT_FLOOR[1:]):
            n = max(abs(x1 - x0), abs(z1 - z0))
            for s in range(n + 1):
                x = round(x0 + (x1 - x0) * s / n)
                z = round(z0 + (z1 - z0) * s / n)
                y = round(y0 + (y1 - y0) * s / n)
                for dx in (0, 1):
                    for dz in (0, 1):
                        side.set(w, x + dx, y, z + dz, *((B.STONE, 5) if r.random() < 0.5 else (B.STONE, 0)))
                        for yy in range(y + 1, y + 4):
                            side.set(w, x + dx, yy, z + dz, B.AIR)
                for dx, dz in ((-1, 0), (2, 0), (0, -1), (0, 2), (-1, 1), (2, 1), (1, -1), (1, 2)):
                    for yy in range(y + 1, y + 5):
                        cur = side.get(w, x + dx, yy, z + dz)[0]
                        if cur not in (0, B.WATER, B.ICE) and r.random() < 0.18:
                            side.set(w, x + dx, yy, z + dz, *((B.PACKED_ICE, 0) if not side.ember else (B.GLOWSTONE, 0)))


# ---- the hamlet -----------------------------------------------------------------------------------------------
def hamlet(w, rng):
    """Four houses on their pads, each built for its side; two domes (Frost's ice houses, Ember's charcoal kilns);
    the yard (hay under snow, pumpkins); a woodpile against each house's gable."""
    out = []
    for side in SIDES:
        for key, cx, cz, heading, L, W, door, storeys, name in P.HOUSES:
            floor = g(cx, cz)
            hx, hz = side.p(cx + 0.5 * (L % 2 if heading % 180 == 0 else W % 2), cz + 0.5 * (W % 2 if heading % 180 == 0 else L % 2))
            res = BLD.house(w, BLD.House(hx, hz, side.heading(heading), L=L, W=W, floor=floor, storeys=storeys,
                                         style=side.house, door=door, chimney=storeys > 1, roof="gable", pitch=1),
                            ground_at=lambda x, z: P.g(x, z), rng=np.random.default_rng(hash(key) % 1000))
            if not side.ember:
                snow_roof(w, res["roof"])
            out.append((side.name, name, res["door"]))
        wheel(w, side)
        for n, (dx, dz) in enumerate(P.ICEHOUSES):
            dome(w, side, dx, dz, np.random.default_rng(60 + n + 10 * side.ember))
        x0, z0, x1, z1 = P.HAYYARD
        r = np.random.default_rng(70 + side.ember)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if (x + z) % 2 or r.random() < 0.3:
                    continue
                h = g(x, z)
                side.set(w, x, h + 1, z, *side.m("yard"))
                if not side.ember:
                    side.set(w, x, h + 2, z, B.SNOW_LAYER, 0)
    return out


def wheel(w, side):
    """The Mill House's wheel, standing in the beck against its west wall: a rim of logs five across, four spokes
    of fence and a hub, its axle through the wall. Ice holds Frost's still."""
    key, cx, cz, heading, L, W, door, storeys, name = P.HOUSES[3]
    wx = cx - L // 2 - 1
    h = g(cx, cz)
    log = side.m("log")
    for dy in range(-3, 4):
        for dz in range(-3, 4):
            r = math.hypot(dy, dz)
            y, z = h + 2 + dy, cz + dz
            if 1.8 < r <= 2.9:
                side.set(w, wx, y, z, log[0], log[1] | 4)
            elif (dy == 0 or dz == 0) and 0.5 < r <= 1.8:
                side.set(w, wx, y, z, *side.m("fence"))
            elif r <= 0.5:
                side.set(w, wx, y, z, log[0], log[1] | 4)
                side.set(w, wx + 1, y, z, log[0], log[1] | 4)


def dome(w, side, cx, cz, r):
    """A dome five high and three and a half in radius, its door to the south, a woodpile against its east side.
    Frost's is an ice house: a stone beehive under snow, packed ice stacked inside. Ember's is a charcoal clamp: an
    earth mound over a stack of coal, fire showing at its vent on top."""
    y0 = g(cx, cz)
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            d = math.hypot(dx, dz)
            x, z = cx + dx, cz + dz
            for k in range(0, 6):
                rr = 3.6 * math.sqrt(max(0.0, 1 - (k / 5.4) ** 2))
                if d <= rr:
                    shell = d > rr - 1.15 or k == 5
                    side.set(w, x, y0 + k, z, *(side.m("dome", r) if shell or k == 0 else (B.AIR, 0)))
    for k in (1, 2):                                    # the door
        side.set(w, cx, y0 + k, cz + 3, B.AIR)
        side.set(w, cx, y0 + k, cz + 2, B.AIR)
    side.set(w, cx - 1, y0 + 1, cz - 1, *side.m("dome_core"))
    side.set(w, cx, y0 + 1, cz - 1, *side.m("dome_core"))
    side.set(w, cx - 1, y0 + 2, cz - 1, *side.m("dome_core"))
    if side.ember:
        side.set(w, cx, y0 + 5, cz, B.NETHERRACK)
        side.set(w, cx, y0 + 6, cz, B.FIRE)
    # the woodpile: logs laid along z, three long and two high, against the dome's east side
    log = side.m("log")
    for dz in (-1, 0, 1):
        for k in (1, 2):
            side.set(w, cx + 5, y0 + k, cz + dz, log[0], log[1] | 8)
    side.set(w, cx + 5, y0 + 3, cz, log[0], log[1] | 8)
    if not side.ember:
        for dx in range(-4, 6):
            for dz in range(-4, 5):
                y = y0 + 7
                while y > y0 and side.get(w, cx + dx, y, cz + dz)[0] == 0:
                    y -= 1
                if side.get(w, cx + dx, y, cz + dz)[0] in (B.COBBLE, B.STONE, B.LOG) and \
                        side.get(w, cx + dx, y + 1, cz + dz)[0] == 0:
                    side.set(w, cx + dx, y + 1, cz + dz, B.SNOW_LAYER, 0)


# ---- the Knoll's tower ----------------------------------------------------------------------------------------
def watch(w, rng):
    """The ruined round tower on the Knoll: walls of the side's stone, three in radius, broken to a ragged top;
    a ladder inside on its north wall to a floor at nine with a hatch, and the beacon on that floor: a sea
    lantern caged in bars for Frost, a fire on netherrack for Ember. Its door faces its own spawn."""
    tx, tz = P.KNOLL_TOWER
    y0 = g(tx, tz)
    for side in SIDES:
        r = np.random.default_rng(81)
        top = {}
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                d = math.hypot(dx, dz)
                if d <= 3.4:
                    top[(dx, dz)] = y0 + 8 + int(3 * (0.5 + 0.5 * math.sin(math.atan2(dz, dx) * 2 + 0.7))) + int(r.integers(0, 2))
        for (dx, dz), ht in top.items():
            d = math.hypot(dx, dz)
            x, z = tx + dx, tz + dz
            gy = g(x, z)
            for y in range(min(gy, y0) - 1, y0 + 1):
                side.set(w, x, y, z, *side.m("wall", r))
            if d > 2.4:
                for y in range(y0 + 1, ht + 1):
                    side.set(w, x, y, z, *side.m("wall", r))
            else:
                for y in range(y0 + 1, y0 + 9):
                    side.set(w, x, y, z, B.AIR)
                side.set(w, x, y0 + 9, z, *side.m("planks"))
                for y in range(y0 + 10, y0 + 13):
                    side.set(w, x, y, z, B.AIR)
        # a battered plinth two courses high round its foot, and a timber hoarding round its top floor
        for dx in range(-5, 6):
            for dz in range(-5, 6):
                d = math.hypot(dx, dz)
                x, z = tx + dx, tz + dz
                if 3.4 < d <= 4.3:
                    for y in range(g(x, z), y0 + 2):
                        side.set(w, x, y, z, *side.m("wall", r))
                    side.set(w, x, y0 + 2, z, side.m("stair"), OR.stair((-dx, -dz) if abs(dx) != abs(dz) else (-dx, 0)))
                if 3.4 < d <= 4.5 and dz != -4 and not (abs(dx) <= 1 and dz < 0):
                    side.set(w, x, y0 + 9, z, *side.m("planks"))
                    if d > 3.9:
                        side.set(w, x, y0 + 10, z, *side.m("fence"))
        # the door, facing north (toward the side's own spawn), two high
        for y in (y0 + 1, y0 + 2, y0 + 3):
            for dz in (-4, -3, -2):
                side.set(w, tx, y, tz + dz, B.AIR)
        side.set(w, tx, y0 + 3, tz - 3, *side.m("trim"))
        # the ladder on the inside of the east wall, through a hatch in the floor
        for y in range(y0 + 1, y0 + 10):
            side.set(w, tx + 2, y, tz, B.LADDER, OR.ladder("e"))
        # slits
        for (dx, dz), y in (((-3, 0), y0 + 5), ((0, 3), y0 + 6), ((0, 3), y0 + 4), ((-2, 2), y0 + 7)):
            side.set(w, tx + dx, y, tz + dz, B.AIR)
        # the beacon
        side.set(w, tx, y0 + 10, tz, *side.m("trim"))
        side.set(w, tx, y0 + 11, tz, *side.m("beacon"))
        if side.ember:
            side.set(w, tx, y0 + 12, tz, B.FIRE)
        else:
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                side.set(w, tx + dx, y0 + 11, tz + dz, B.IRON_BARS)
            side.set(w, tx, y0 + 12, tz, *side.m("slab"))


# ---- erratics -------------------------------------------------------------------------------------------------
ERRATIC_ZONE = [(-34, -42), (28, -42), (32, -14), (-32, -14)]


def erratics(w, rng):
    """Boulders the ice dropped in the middle field, one rock each (stone and andesite, a little cobble), the
    largest four across; snow on Frost's, a speck of moss on Ember's. Off the roads, the water and the Knoll's top."""
    X, Z = P.X, P.Z
    near = np.full(X.shape, np.inf)
    for pts in P.land.ROADS.values():
        near = np.minimum(near, shapes.polyline(X, Z, pts)[0])
    zone = shapes.inside(X, Z, ERRATIC_ZONE) & P.LAND & (near > 4) & (distance_in(~P.WET, "euclid") > 4)
    zone &= np.hypot(X - P.KNOLL_TOWER[0], Z - P.KNOLL_TOWER[1]) > 8
    zone &= Z < -16
    sites = shapes.scatter_points(zone, 12, 9, np.random.default_rng(91), X, Z)
    shapes_ = []
    r0 = np.random.default_rng(92)
    for x, z in sites:
        rad = r0.uniform(1.6, 3.0)
        squash = r0.uniform(0.55, 0.8)
        ang = r0.uniform(0, math.pi)
        shapes_.append((x, z, rad, squash, ang))
    for side in SIDES:
        r = np.random.default_rng(93 + side.ember)
        for x0, z0, rad, squash, ang in shapes_:
            gy = g(x0, z0)
            R = int(math.ceil(rad)) + 1
            for dx in range(-R, R + 1):
                for dz in range(-R, R + 1):
                    u = dx * math.cos(ang) + dz * math.sin(ang)
                    v = -dx * math.sin(ang) + dz * math.cos(ang)
                    for dy in range(-1, R + 1):
                        e = (u / rad) ** 2 + (v / (rad * 0.8)) ** 2 + (dy / (rad * squash)) ** 2
                        if e <= 1.0:
                            v_ = r.random()
                            blk = (B.STONE, 0) if v_ < 0.45 else (B.STONE, 5) if v_ < 0.85 else (B.COBBLE, 0)
                            if side.ember and v_ > 0.97:
                                blk = (B.MOSSY, 0)
                            side.set(w, x0 + dx, gy + dy, z0 + dz, *blk)
            if not side.ember:
                for dx in range(-R, R + 1):
                    for dz in range(-R, R + 1):
                        x, z = x0 + dx, z0 + dz
                        for y in range(gy + R + 1, gy - 1, -1):
                            b = side.get(w, x, y, z)[0]
                            if b in (B.STONE, B.COBBLE):
                                if side.get(w, x, y + 1, z)[0] == 0:
                                    side.set(w, x, y + 1, z, B.SNOW_LAYER, 0)
                                break
                            if b != 0:
                                break
    return sites


# ---- the field walls -----------------------------------------------------------------------------------------
FIELD_WALLS = [[(-31, -23), (-20, -21), (-9, -22)], [(13, -37), (21, -34), (29, -31)], [(-12, -33), (-3, -36)]]


def field_walls(w, rng):
    """The old drystone walls of the fields the rift split, across the middle field: one rock (stone, andesite, a
    little cobble), a course high with every third stone a course higher, broken every seven blocks for two and
    wherever a road crosses. Snow lies on Frost's."""
    from pgmvox.geom.shapes import walk_cells
    near = np.full(P.X.shape, np.inf)
    for pts in P.land.ROADS.values():
        near = np.minimum(near, shapes.polyline(P.X, P.Z, pts)[0])
    laid = 0
    for line in FIELD_WALLS:
        cells = walk_cells(line)
        for side in SIDES:
            r = np.random.default_rng(141)
            for n, (x, z) in enumerate(cells):
                i, k = x - P.X_MIN, z - P.Z_MIN
                if not land(x, z) or P.WET[i, k] or near[i, k] <= 2.5 or n % 7 in (5, 6):
                    continue
                h = g(x, z)
                tall = 2 if n % 3 == 0 and r.random() < 0.7 else 1
                for y in range(h + 1, h + 1 + tall):
                    v = r.random()
                    side.set(w, x, y, z, *((B.STONE, 0) if v < 0.45 else (B.STONE, 5) if v < 0.85 else (B.COBBLE, 0)))
                if not side.ember:
                    side.set(w, x, h + 1 + tall, z, B.SNOW_LAYER, 0)
                laid += 1
    return laid // 2


# ---- the Stack ------------------------------------------------------------------------------------------------
def stack(w, rng):
    """The Rimefire Stack, built once since it stands on the axis. Its pillar rises out of the lava waisted and
    ledged, undercut where the lava has eaten it; its north face (Frost's) crusted with ice and snow, its south
    face (Ember's) seamed with netherrack and glowing. On the island's top a spire 36 high: the north half ice,
    packed ice inside clear ice with a sea lantern at its tip; the south half coal, obsidian and black clay with
    lava in its seams and a fire on its tip. The ring round the spire is ground to stand on."""
    X, Z = P.X, P.Z
    top = P.land.STACK_Y
    floor = P.RIFT_FLOOR
    sf = P.land.stack_field(X, Z)
    r = np.random.default_rng(101)
    wob = noise.fbm(X.shape, 3, 2, seed=171)
    # the pillar, carved from the island's solid column: a waist, ledges every five, the foot undercut
    for i, k in np.argwhere(P.STACK):
        x, z = int(X[i, k]), int(Z[i, k])
        for y in range(floor + 1, top - 2):
            t = (y - floor) / (top - floor)
            keep = 0.62 + 0.3 * t + 0.07 * math.sin(y / 2.3) + (0.06 if y % 5 == 0 else 0) + 0.06 * wob[i, k] \
                - 0.18 * (t < 0.15)
            if sf[i, k] > keep:
                w.set(x, y, z, B.LAVA if y <= P.LAVA_Y else B.AIR)
    # the crusts, on every exposed block of the pillar's faces
    for i, k in np.argwhere(P.STACK | (distance_in(~P.STACK, "euclid") <= 1)):
        x, z = int(X[i, k]), int(Z[i, k])
        for y in range(P.LAVA_Y + 1, top + 1):
            b = w.id(x, y, z)
            if b in (0, B.LAVA, B.LAVA_FLOW, B.SNOW_LAYER):
                continue
            if not any(w.id(x + dx, y, z + dz) == 0 for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue
            v = r.random()
            if z < 0:
                if v < 0.38:
                    w.set(x, y, z, *((B.PACKED_ICE, 0) if v < 0.25 else (B.SNOW, 0)))
            else:
                if v < 0.3:
                    w.set(x, y, z, *((B.NETHERRACK, 0) if v < 0.2 else (B.STAINED_CLAY, 15) if v < 0.27 else (B.GLOWSTONE, 0)))
    cy = top + 1
    m = forms.spike(w, [(0.0, cy - 1, 0.0), (0.5, cy + 14, -0.4), (-0.3, cy + 36, 0.3)], (4.2, 0.35, 1.15),
                    flutes=(6, 0.16), twist=50, rough=0.08, cell=7, seed=7)
    idx = np.argwhere(m)
    X0, Z0 = w.x0, w.z0
    for i, y, k in idx:
        x, z = i + X0, k + Z0
        if z < 0:
            surface = any(not m[i + di, y, k + dk] for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1))
                          if 0 <= i + di < m.shape[0] and 0 <= k + dk < m.shape[2])
            blk = (B.ICE, 0) if surface and r.random() < 0.55 else (B.PACKED_ICE, 0)
        else:
            v = r.random()
            blk = (B.COAL_BLOCK, 0) if v < 0.4 else (B.OBSIDIAN, 0) if v < 0.72 else (B.STAINED_CLAY, 15)
            if v > 0.94 and 2 < y - cy < 30:
                blk = (B.LAVA, 0)
        w.ids[i, y, k], w.dat[i, y, k] = blk
    if len(idx):
        hi = idx[idx[:, 1] >= idx[:, 1].max() - 1]
        for i, y, k in hi:
            z = k + Z0
            if z >= 0:
                w.ids[i, y, k], w.dat[i, y, k] = B.NETHERRACK, 0
                if w.ids[i, y + 1, k] == 0:
                    w.ids[i, y + 1, k] = B.FIRE
            else:
                w.ids[i, y, k], w.dat[i, y, k] = B.SEA_LANTERN, 0
    # the island's ground round the spire
    for i, k in np.argwhere(P.STACK):
        x, z = int(X[i, k]), int(Z[i, k])
        h = g(x, z)
        if w.id(x, h + 1, z) != 0:
            continue
        if z < 0:
            w.set(x, h, z, B.SNOW)
            w.set(x, h + 1, z, B.SNOW_LAYER, 0)
        else:
            v = r.random()
            w.set(x, h, z, *((B.COAL_BLOCK, 0) if v < 0.3 else (B.STAINED_CLAY, 15) if v < 0.75 else (B.NETHERRACK, 0)))
    return int(len(idx))


# ---- the coast ------------------------------------------------------------------------------------------------
def edges(w, bottom):
    """Icicles under Frost's coast: from the underside's lowest block at the rim, a short spike of packed ice
    tipped with ice, every so often."""
    X, Z = P.X, P.Z
    rim = P.LAND & (edge_depth(P.LAND) <= 1) & (distance_in(~P.RIFT, "euclid") > 12) & (Z < 0)
    r = np.random.default_rng(121)
    n = 0
    for i, k in np.argwhere(rim):
        if r.random() > 0.16:
            continue
        x, z = int(X[i, k]), int(Z[i, k])
        b = int(bottom[i, k])
        ln = int(r.integers(2, 7))
        for y in range(b - 1, b - 1 - ln, -1):
            if w.id(x, y, z) == 0:
                w.set(x, y, z, B.PACKED_ICE if y > b - ln else B.ICE)
        n += 1
    return n
