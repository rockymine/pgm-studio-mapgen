"""Everything somebody built (red half): the houses, the square, the spawn terrace and its steps, the towers, the
mill with its wheel and weir, the stone bridge, the Old Bridge's broken stub, the headframe, the engine stack,
the smithy, the well, the streets and lanes with the outlet footbridge.

The houses are pgmvox.build.house on pgmvox.build.site; the square is a pgmvox.facade carpet; the terrace steps
are pgmvox.build.stairs; the watch tower's battlement is pgmvox.build.parapet; the roads are pgmvox.route.pave
over the plan's graded lines (through a guard, since pave has no mask of what it must not touch). The towers,
the bridges, the mill, the headframe and the stack are local: the library has no prop for any of them.
"""
import math

import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox import build as BLD
from pgmvox import facade as F
from pgmvox import route
from pgmvox.orient import door as door_data, ladder as ladder_data, stair, torch

R_ = rng(P.BOARD, "works")
HARD = ((B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0))
SOFT = ((B.DIRT, 1), (B.DIRT, 0), (B.GRAVEL, 0))
FOREST = ((B.DIRT, 2), (B.DIRT, 1), (B.DIRT, 0))
FLOOR = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]


class Guarded:
    """A world that refuses writes to protected columns: what route.pave is handed, so a street laid past a
    house does not take its wall out (pave clears three blocks over every cell it lays)."""

    def __init__(self, w, protect):
        self.w, self.protect = w, protect

    def set(self, x, y, z, bid, d=0):
        if (x, z) not in self.protect:
            self.w.set(x, y, z, bid, d)

    def id(self, x, y, z):
        return self.w.id(x, y, z)


def top(w, x, z):
    return w.top(x, z)


# ---- the houses --------------------------------------------------------------------------------------------
def houses(w):
    hs = P.houses()
    for key, b in hs.items():                                    # every site first: a later site's eased ring
        BLD.site(w, b["cells"], b["floor"], lambda x, z: top(w, x, z), margin=2,   # would cut an earlier wall
                 fill=(B.STONE, 0), top=(B.GRASS, 0))
    built = {}
    for key, b in hs.items():
        built[key] = BLD.house(w, b["house"], ground_at=lambda x, z: top(w, x, z),
                               rng=rng(P.BOARD, f"house {key}"))
        if built[key]["door"] and (built[key]["door"][0], built[key]["door"][1]) != b["door"]:
            raise RuntimeError(f"{key}: the library put the door at {built[key]['door'][:2]}, the plan at {b['door']}")
    for key, b in hs.items():                                    # shop signs beside the door
        if "sign" in b["spec"]:
            x, z, facing = built[key]["door"]
            dx, dz = facing                                      # the library's door facing is a (dx, dz)
            sx, sz = x + dx - dz, z + dz + dx                    # outside the wall, beside the door
            w.sign(sx, b["floor"] + 3, sz, [b["spec"]["sign"], "", "", ""], wall_facing=ladder_data((-dx, -dz)))
    return built


def tower(w, x0, z0, x1, z1, f, height, spire=True):
    """A masonry tower: stone brick with polished andesite corners, a plank floor, belfry openings and a
    pyramid spire (or a battlement), a ladder up the inside."""
    topy = f + height
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(min(f, top(w, x, z)) - 2, topy + 1):
                if edge or y <= f:
                    corner = x in (x0, x1) and z in (z0, z1)
                    w.set(x, y, z, *((B.STONE, 6) if corner else (B.STONEBRICK, 0)))
                else:
                    w.set(x, y, z, B.AIR)
            if not edge:
                w.set(x, f, z, B.PLANKS, 5)
    mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
    for y in (topy - 4, topy - 3, topy - 2):
        for d in (-1, 0, 1):
            w.set(mx + d, y, z0, B.AIR); w.set(mx + d, y, z1, B.AIR)
            w.set(x0, y, mz + d, B.AIR); w.set(x1, y, mz + d, B.AIR)
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            w.set(x, topy - 5, z, B.PLANKS, 5)
    for y in range(f + 1, topy - 4):
        w.set(x0 + 1, y, z0 + 1, B.LADDER, ladder_data("n"))
    w.set(x0 + 1, topy - 5, z0 + 1, B.LADDER, ladder_data("n"))
    if spire:
        w.set(mx, topy - 1, mz, B.FENCE)
        w.set(mx, topy - 2, mz, B.GOLD_BLOCK)                    # the bell
        for k in range(4):
            for x in range(x0 - 1 + k, x1 + 2 - k):
                for z in range(z0 - 1 + k, z1 + 2 - k):
                    if x in (x0 - 1 + k, x1 + 1 - k) or z in (z0 - 1 + k, z1 + 1 - k):
                        w.set(x, topy + 1 + k, z, B.PLANKS, 5)
        w.set(mx, topy + 5, mz, B.FENCE); w.set(mx, topy + 6, mz, B.FENCE)
    else:
        for x in range(x0 + 1, x1):
            for z in range(z0 + 1, z1):
                w.set(x, topy, z, B.PLANKS, 5)
        BLD.parapet(w, BLD.edge_cells({(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}), topy + 1,
                    (B.STONEBRICK, 0), crenel=(B.SLAB, 5))
        w.set(x0 + 1, topy, z0 + 1, B.LADDER, ladder_data("n"))
    return topy


def chapel(w, built):
    f = P.houses()["chapel"]["floor"]
    _, x0, z0, x1, z1, hgt = P.TOWERS[0]
    BLD.site(w, {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}, f, lambda x, z: top(w, x, z), 1)
    t = tower(w, x0, z0, x1, z1, f, hgt)
    for y in (f + 1, f + 2):                                     # into the nave, and from the lane
        w.set(x1, y, -76, B.AIR); w.set(x1 + 1, y, -76, B.AIR)
        w.set(x0 + 2, y, z1, B.AIR)
    w.set(x0 + 2, f + 1, z1, B.DARK_OAK_DOOR, door_data("s"))
    w.set(x0 + 2, f + 2, z1, B.DARK_OAK_DOOR, door_data("s", upper=True))
    for x in range(-48, -41, 2):                                 # pews and an altar
        for z in (-77, -76, -74, -73):
            w.set(x, f + 1, z, B.SPRUCE_STAIRS, stair("e"))
    w.set(-40, f + 1, -76, B.QUARTZ); w.set(-40, f + 1, -75, B.QUARTZ)
    return t


def watch(w):
    """The spawn: the framed watch house (a library house) and its stone tower, the terrace, steps to the lane,
    and the team's wool hung from the tower."""
    f = P.houses()["watch"]["floor"]
    _, x0, z0, x1, z1, hgt = P.TOWERS[1]
    t = tower(w, x0, z0, x1, z1, f, hgt, spire=False)
    for y in (f + 1, f + 2):
        w.set(x1, y, -7, B.AIR); w.set(x1 + 1, y, -7, B.AIR)
    for z in range(z0, z1 + 1):
        if z % 2 == 0:
            for y in (t - 3, t - 2):
                w.set(x0 - 1, y, z, B.WOOL, 14)
    # the terrace: a stone floor in front of the door, a low wall along its edge
    F.carpet(w, -93, -12, -86, -2, f, F.tiles(1, FLOOR[0], FLOOR[2]))
    for x in range(-93, -85):
        for z in range(-12, -1):
            for y in range(f + 1, f + 6):
                w.set(x, y, z, B.AIR)
            for y in range(top(w, x, z), f):
                if w.id(x, y, z) == B.AIR:
                    w.set(x, y, z, B.STONE)
    for z in range(-13, 0):
        if z not in (-8, -7, -6):
            w.set(-85, f + 1, z, B.COBBLE_WALL)
    for x in range(-93, -85):
        w.set(x, f + 1, -13, B.COBBLE_WALL); w.set(x, f + 1, -1, B.COBBLE_WALL)
    # the steps down to Spawn Lane: a flight climbing west
    g = top(w, -78, -7)
    n = f - g
    if n > 0:
        BLD.stairs(w, -85 + n, -6, "w", g + 1, n, B.STONEBRICK_STAIRS, width=3, under=(B.STONE, 0))
        for k in range(n):
            for z in (-8, -7, -6):
                for y in range(g + 2 + k, f + 4):
                    w.set(-85 + n - k, y, z, B.AIR)
    return t


# ---- the river ---------------------------------------------------------------------------------------------
def mill(w, L):
    """The race beside the river, the dark oak wheel turning in it, and the weir's stone sill."""
    f = P.houses()["mill"]["floor"]
    for x in range(-68, -53):
        for z in (9, 10, 11):
            g = top(w, x, z)
            for y in range(42, max(g, 46) + 4):
                w.set(x, y, z, B.AIR)
            w.set(x, 41, z, B.GRAVEL)
            for y in range(42, 46):
                w.set(x, y, z, B.WATER)
        for z in (8, 12):
            g = top(w, x, z)
            if g > 46:
                for y in range(41, g + 1):
                    w.set(x, y, z, B.STONEBRICK, 0)
    cx, cy = -62, 46
    for a in np.linspace(0, 2 * np.pi, 64, endpoint=False):
        for rr in (4.0, 4.6):
            w.set(cx + int(round(rr * np.cos(a))), cy + int(round(rr * np.sin(a))), 10, B.PLANKS, 5)
    for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        for rr in np.arange(1, 4, 0.5):
            w.set(cx + int(round(rr * np.cos(a))), cy + int(round(rr * np.sin(a))), 10, B.LOG2, 1 | 12)
    for z in range(8, 12):
        w.set(cx, cy, z, B.LOG2, 1 | 8)
    zc = int(round(np.interp(-67, [p[0] for p in P.RIVER], [p[1] for p in P.RIVER])))
    for z in range(zc - 5, zc + 6):
        i, k = -67 - P.X_MIN, z - P.Z_MIN
        if L.water[i, k] > 0 or abs(z - zc) <= 3:
            for y in range(L.H[i, k], 48):
                w.set(-67, y, z, B.STONEBRICK, 0)
            w.set(-67, 48, z, B.WATER)
    w.set(-60, f + 1, 3, B.DSLAB, 0); w.set(-60, f + 2, 3, B.SLAB, 0)
    for x in (-65, -64):
        w.set(x, f + 1, 2, B.HAY, 0)


def stone_bridge(w, L):
    """A hump-backed bridge: one arch over the river with a keystone, its deck climbing in stairs to the crown."""
    x0, x1, zN, zS, zc = P.STONE_BRIDGE
    half = 6.5
    dy_ = lambda z: P.deck_y(L, z)                               # noqa: E731
    for z in range(zN, zS + 1):
        dy, prev, nxt = dy_(z), dy_(z - 1), dy_(z + 1)
        t = (z - zc) / half
        soffit = int(round(45 + 5.2 * math.sqrt(1 - t * t))) if abs(t) < 1 else None
        climbing = (nxt > dy and z < 1) or (prev > dy and z > 1)
        for x in range(x0, x1 + 1):
            ground = P.at(L, x, z)
            lo = (soffit + 1) if soffit is not None else min(ground, dy) - 1
            for y in range(lo, dy):
                ring = soffit is not None and y == soffit + 1
                w.set(x, y, z, B.STONEBRICK, 3 if ring and abs(z - zc) < 1 else (0 if (y * 3 + z) % 9 else 2))
            if soffit is not None:
                for y in range(46, soffit + 1):
                    w.set(x, y, z, B.AIR)
            if climbing:
                w.set(x, dy, z, B.STONEBRICK, 0)
                w.set(x, dy + 1, z, B.STONEBRICK_STAIRS, stair("s" if z < 1 else "n"))
            else:
                w.set(x, dy, z, *FLOOR[(x + z) % 4])
            if x not in (x0, x1):
                for y in range(dy + (2 if climbing else 1), dy + 5):
                    w.set(x, y, z, B.AIR)
            else:
                tp = dy + (2 if climbing else 1)
                w.set(x, tp, z, B.STONEBRICK, 0)
                w.set(x, tp + 1, z, B.SLAB, 5)
                for y in range(tp + 2, tp + 4):
                    w.set(x, y, z, B.AIR)
    for pz in (zc - 7, zc + 7):
        for x in (x0 - 1, x1 + 1):
            for y in range(min(P.at(L, x, pz), 44), 49):
                w.set(x, y, pz, B.STONEBRICK, 0)
            w.set(x, 49, pz, B.SLAB, 5)
    for z, x in ((zN, x0), (zN, x1), (zS, x0), (zS, x1)):
        y = dy_(z) + 2
        w.set(x, y, z, B.STONEBRICK, 0); w.set(x, y + 1, z, B.FENCE); w.set(x, y + 2, z, B.GLOWSTONE)


def old_bridge(w, L):
    """Main Street carried out over the rift on a half-arch from the face, broken off where the span fell."""
    zc, face, end = P.OLD_BRIDGE
    deck = P.at(L, face - 3, zc)
    r = np.random.default_rng(17)
    for x in range(face - 3, end + 1):
        for z in range(zc - 3, zc + 4):
            edge = abs(z - zc) == 3
            k = (x - face) / (end - face)
            if x >= end - 1 and r.random() < (0.45 if x == end else 0.2) + (0.3 if edge else 0):
                continue
            soffit = int(round(deck - 2 - 9 * (1 - k) ** 2)) if x >= face else deck - 12
            for y in range(soffit, deck):
                if x < face and w.id(x, y, z) != B.AIR:
                    continue
                w.set(x, y, z, B.STONEBRICK, 0 if (y + z + x) % 5 else 2)
            if edge:
                if not (x >= end - 2 and r.random() < 0.6):
                    w.set(x, deck, z, B.STONEBRICK, 0)
                    w.set(x, deck + 1, z, B.SLAB, 5)
            else:
                w.set(x, deck, z, *FLOOR[(x * 7 + z * 3) % 4])
                for y in range(deck + 1, deck + 4):
                    w.set(x, y, z, B.AIR)
    for z in (zc - 1, zc + 1):
        for y in range(deck - 4, deck):
            w.set(end + 1, y, z, B.IRON_BARS)
    for z in (zc - 3, zc + 3):
        w.set(face - 2, deck + 1, z, B.STONEBRICK, 0)
        w.set(face - 2, deck + 2, z, B.FENCE); w.set(face - 2, deck + 3, z, B.GLOWSTONE)


# ---- Ironhollow --------------------------------------------------------------------------------------------
def headframe(w, g):
    """Four spruce legs leaning in to a head 17 over the shaft, braced, with the winding wheel on top."""
    sx, sz = P.SHAFT
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if max(abs(dx), abs(dz)) >= 2:
                for y in range(g + 1, g + 4):
                    w.set(sx + dx, y, sz + dz, B.AIR)
                w.set(sx + dx, g, sz + dz, B.PLANKS, 1)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(sx + dx, g, sz + dz, B.AIR)
    w.set(sx, g, sz + 1, B.LADDER, 2)
    tp = g + 17
    for dx, dz in ((-3, -3), (-3, 3), (3, -3), (3, 3)):
        for y in range(g + 1, tp + 1):
            k = (y - g) // 6
            w.set(sx + dx - int(np.sign(dx)) * k, y, sz + dz - int(np.sign(dz)) * k, B.LOG, 1)
    for y in (g + 5, g + 10, tp):
        r = 3 - (y - g) // 6
        for d in range(-r, r + 1):
            for X, Z, ax in ((sx + d, sz - r, 4), (sx + d, sz + r, 4), (sx - r, sz + d, 8), (sx + r, sz + d, 8)):
                w.set(X, y, Z, B.LOG, 1 | ax)
    cy = tp + 3
    for a in np.linspace(0, 2 * np.pi, 48, endpoint=False):
        w.set(sx + int(round(2.6 * np.cos(a))), cy + int(round(2.6 * np.sin(a))), sz, B.PLANKS, 5)
    for d in (-2, -1, 1, 2):
        w.set(sx + d, cy, sz, B.DARK_OAK_FENCE); w.set(sx, cy + d, sz, B.DARK_OAK_FENCE)
    w.set(sx, cy, sz, B.LOG2, 1 | 8)
    for y in range(tp + 1, cy - 2):
        w.set(sx, y, sz, B.DARK_OAK_FENCE)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(sx + dx, tp, sz + dz, B.PLANKS, 1)
    for y in range(g + 1, tp):
        w.set(sx - 1, y, sz - 3, B.LOG, 1)
        w.set(sx - 1, y, sz - 2, B.LADDER, 3)
    w.set(sx - 1, tp, sz - 2, B.AIR)
    return tp


def ironhollow(w, built):
    hs = P.houses()
    f = hs["engine"]["floor"]                                    # the engine house's brick stack
    for y in range(f + 1, f + 19):
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(-74 + dx, y, 50 + dz, B.BRICK)
    for dx in (-1, 0, 1, 2):
        for dz in (-1, 0, 1, 2):
            if dx in (-1, 2) or dz in (-1, 2):
                w.set(-74 + dx, f + 18, 50 + dz, B.BRICK)
    w.set(-74, f + 18, 50, B.AIR); w.set(-73, f + 18, 51, B.AIR)
    f = hs["smithy"]["floor"]                                    # the forge, open to its lane
    for z in range(60, 64):
        for y in range(f + 1, f + 4):
            w.set(-78, y, z, B.AIR)
    w.set(-75, f + 1, 61, B.ANVIL, 0)
    w.set(-73, f + 1, 60, B.FURNACE, 4); w.set(-73, f + 1, 61, B.FURNACE, 4)
    w.set(-73, f + 1, 63, B.CAULDRON, 3)
    # the well on the village road
    x, z = -87, 46
    y = top(w, x, z)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for yy in range(y + 1, y + 5):
                w.set(x + dx, yy, z + dz, B.AIR)
            w.set(x + dx, y, z + dz, B.COBBLE)
            if dx or dz:
                w.set(x + dx, y + 1, z + dz, B.COBBLE_WALL)
            w.set(x + dx, y + 3, z + dz, B.WOOD_SLAB, 1)
    for yy in range(y - 6, y + 1):
        w.set(x, yy, z, B.WATER)
    for dx, dz in ((-1, -1), (1, 1)):
        w.set(x + dx, y + 2, z + dz, B.SPRUCE_FENCE)
    # the spoil heap's rubble, its heights already in the plan
    L = P.land()
    for i, k in np.argwhere(L.spoil):
        x, z = P.X_MIN + int(i), P.Z_MIN + int(k)
        g = int(L.H[i, k])
        for yy in range(g - 6, g + 1):
            if w.id(x, yy, z) in (B.DIRT, B.GRASS, B.STONE):
                c = R_.random()
                w.set(x, yy, z, *((B.GRAVEL, 0) if c < 0.5 else (B.COBBLE, 0) if c < 0.75 else (B.STONE, 5)))
        if w.id(x, g - 1, z) == B.AIR:
            w.set(x, g - 1, z, B.COBBLE)


# ---- streets and lanes ---------------------------------------------------------------------------------------
def roads(w, L, protect):
    """Every route's surface along its graded line; over the pond's outlet Spawn Lane south is a plank deck
    with rails, and trestle legs are added under it."""
    X, Z = w.grid()
    water = np.zeros((w.sx, w.sz), bool)
    water[:L.water.shape[0], :] = L.water > 0
    G = Guarded(w, protect)
    bridges = []
    for n, r in enumerate(L.routes):
        H = w.heightmap()
        town = r["kind"] == "street" or r["name"] == "North Lane"
        surf = HARD if town else FOREST if r["kind"] == "path" else SOFT
        s, p = r["profile"]
        br = route.pave(G, H, X, Z, r["line"], width=r["width"], surface=surf, weights=(0.5, 0.3, 0.2),
                        water=water, deck=(B.PLANKS, 1), rail=(B.SPRUCE_FENCE, 0), seed=n,
                        level=lambda q, s=s, p=p: max(float(np.interp(q, s, p)), P.POND_LEVEL + 1))
        bridges += br
    for x, y, z in bridges:                                      # trestle legs every four blocks to the bed
        if z % 4 == 2:
            yy = y - 1
            while yy > 0 and w.id(x, yy, z) in (B.WATER, B.WATER_FLOW, B.AIR):
                w.set(x, yy, z, B.LOG, 1)
                yy -= 1
    return bridges


def square(w, L):
    """Market Square: a built floor of stone brick and andesite, a kerb of stone brick."""
    field = F.first_of(F.border(1, (B.STONEBRICK, 0)), F.tiles(3, (B.STONE, 6), (B.STONE, 5)))
    sq = L.square
    F.carpet(w, -76, -53, -57, -35, 52, lambda c: field(c) if sq[c.x - P.X_MIN, c.z - P.Z_MIN] else None)
    for i, k in np.argwhere(sq):
        x, z = P.X_MIN + int(i), P.Z_MIN + int(k)
        for y in range(53, 58):
            if w.id(x, y, z) in (B.TALLGRASS, B.FLOWER, B.DANDELION):
                w.set(x, y, z, B.AIR)


def lamps(w, L, protect):
    """A lamp post every ten blocks along the town's streets: a fence post carrying glowstone."""
    for r in L.routes:
        if r["kind"] != "street":
            continue
        pts = r["line"]
        for j in range(5, len(pts) - 3, 10):
            (x, z), (x2, z2) = pts[j], pts[j + 1]
            dx, dz = x2 - x, z2 - z
            n = math.hypot(dx, dz) or 1
            px, pz = int(round(x - dz / n * 3.5)), int(round(z + dx / n * 3.5))
            if (px, pz) in protect or px >= -12:
                continue
            g = top(w, px, pz)
            if w.id(px, g + 1, pz) != B.AIR:
                continue
            w.set(px, g + 1, pz, B.FENCE); w.set(px, g + 2, pz, B.FENCE); w.set(px, g + 3, pz, B.GLOWSTONE)


def protected():
    """The columns roads must not write: every house's footprint and the towers."""
    out = set()
    for b in P.houses().values():
        out |= set(b["cells"])
    for _, x0, z0, x1, z1, _ in P.TOWERS:
        out |= {(x, z) for x in range(x0 - 1, x1 + 2) for z in range(z0 - 1, z1 + 2)}
    return out


def build(w, L, shaft_top):
    prot = protected()
    sq = {(P.X_MIN + int(i), P.Z_MIN + int(k)) for i, k in np.argwhere(L.square)}
    roads(w, L, prot | sq | {(x, z) for x in range(-93, -84) for z in range(-13, 0)})
    square(w, L)
    built = houses(w)
    chapel(w, built)
    watch(w)
    mill(w, L)
    stone_bridge(w, L)
    old_bridge(w, L)
    tp = headframe(w, shaft_top)
    ironhollow(w, built)
    lamps(w, L, prot)
    return dict(built=built, headframe_top=tp)
