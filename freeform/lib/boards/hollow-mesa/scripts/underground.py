"""Inside the mesa: the Throat — a cavern in the banded clay whose floor opens into a hole that falls through
the island into the void, the core on a stub of rock at the hole's lip — and the ways to it: the shaft from
the plateau, the Bench Adit from the canyon wall, the Chimney from the canyon floor. Two old drifts besides:
the Old Workings off the cavern, and the South Drift at the tram's far end.
"""
import numpy as np

import plan as P
from mc import B
from noise import spline

RNG = np.random.default_rng(4321)
FLOOR = 47                     # where a player stands in the Throat
CHIMNEY = [(-30, 41, -14, 1.9), (-36, 41, -13, 2.1), (-43, 42, -14, 2.3), (-50, 43, -15, 2.1),
           (-57, 45, -15, 2.2), (-63, 46, -16, 2.4), (-67, 47, -18, 2.6)]
WORKINGS = [(-80, 47, -20, 2.0), (-86, 47, -14, 1.8), (-90, 47, -8, 1.8), (-92, 47, -2, 2.2)]
ADIT = [(-48, 57, -34), (-52, 56, -34), (-56, 54, -34), (-59, 52, -33), (-61, 50, -33)]
SHAFT = (-78, -30)


def carve_ellipsoid(w, L, cx, cy, cz, r, rv, floor_y, allow_surface=False, rz=None):
    rz = rz or r
    for x in range(int(np.floor(cx - r)), int(np.ceil(cx + r)) + 1):
        for z in range(int(np.floor(cz - rz)), int(np.ceil(cz + rz)) + 1):
            if x >= -1 or not w.inside(x, 0, z):
                continue
            ix, iz = x - L.x0, z - L.z0
            ground = L.H[ix, iz]
            for y in range(int(np.floor(floor_y)), int(np.ceil(cy + rv)) + 1):
                if ((x - cx) / r) ** 2 + ((z - cz) / rz) ** 2 + ((y - cy) / rv) ** 2 > 1:
                    continue
                if not allow_surface and y > ground - 3:
                    continue
                w.set(x, y, z, B.AIR)


def carve_tube(w, L, pts, allow_surface_first=0):
    sp = spline([(p[0], p[2]) for p in pts], 0.4)
    arc = np.concatenate([[0], np.cumsum([np.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts[:-1], pts[1:])])])
    sarc = np.concatenate([[0], np.cumsum([np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(sp[:-1], sp[1:])])])
    sarc *= arc[-1] / max(sarc[-1], 1e-6)
    floors = np.interp(sarc, arc, [p[1] for p in pts])
    radii = np.interp(sarc, arc, [p[3] for p in pts])
    for (x, z), fy, r, s in zip(sp, floors, radii, sarc):
        carve_ellipsoid(w, L, x, fy + r * 0.8 * 0.55, z, r, r * 0.8, fy, allow_surface=s < allow_surface_first)


def cavern(w, L):
    """The Throat: a wide low cavern, its floor dished toward the hole, the hole itself to the void."""
    cx, cz = P.CAVERN
    carve_ellipsoid(w, L, cx, FLOOR + 3.5, cz, 12, 7.5, FLOOR, rz=10)
    carve_ellipsoid(w, L, cx - 4, FLOOR + 2.5, cz + 4, 7, 5.0, FLOOR, rz=6)
    # the floor: hardened clay and gravel, laid one block below where a player stands
    for x in range(cx - 13, cx + 14):
        for z in range(cz - 11, cz + 12):
            if w.id(x, FLOOR, z) == B.AIR and w.id(x, FLOOR - 1, z) != B.AIR:
                r = RNG.random()
                w.set(x, FLOOR - 1, z, *((B.GRAVEL, 0) if r < 0.35 else (B.HARDENED_CLAY, 0) if r < 0.75 else (B.DIRT, 1)))
    # the hole: straight down through the island into the void
    tx, tz, tr = P.THROAT
    for x in range(int(tx - tr - 1), int(tx + tr + 2)):
        for z in range(int(tz - tr - 1), int(tz + tr + 2)):
            d = np.hypot(x - tx, z - tz)
            if d < tr + 0.25 * RNG.standard_normal():
                for y in range(0, FLOOR + 1):
                    w.set(x, y, z, B.AIR)
    L.throat = P.THROAT


def core(w, L):
    """The core: an obsidian shell with lava inside, floating five over the plateau a dozen east of the shaft's
    head, where it is seen from the fort's road. Under it a well two wide drops through the mesa into the Throat
    and on through its hole to the void, so lava let out of the core's foot falls clear: the leak. A ring of the
    Throat's dark clay marks the well's lip; the shaft is still the way up to it from the cavern."""
    c = P.CORE
    for x in range(c["x0"], c["x1"] + 1):
        for z in range(c["z0"], c["z1"] + 1):
            for y in range(c["y0"], c["y1"] + 1):
                inner = c["x0"] < x < c["x1"] and c["z0"] < z < c["z1"] and c["y0"] < y < c["y1"]
                w.set(x, y, z, B.LAVA if inner else B.OBSIDIAN)
    g = int(L.H[c["x0"] + 1 - L.x0, c["z0"] + 1 - L.z0])
    for x in range(c["x0"] + 1, c["x1"]):
        for z in range(c["z0"] + 1, c["z1"]):
            for y in range(FLOOR, g + 1):
                w.set(x, y, z, B.AIR)
    for x in range(c["x0"], c["x1"] + 1):
        for z in range(c["z0"], c["z1"] + 1):
            if not (c["x0"] < x < c["x1"] and c["z0"] < z < c["z1"]):
                w.set(x, g, z, B.STAINED_CLAY, 12)
    L.core_ground = g


def catwalk(w, L):
    """The miners' catwalk: planks on log brackets round the north and east walls at the adit's level,
    a stair down to the floor at the west end, and a hoist frame over the hole with its chain hanging in."""
    y = 50
    cx, cz = P.CAVERN
    tx, tz, tr = P.THROAT
    path = [(x, cz - 8) for x in range(cx - 7, cx + 10)] + [(cx + 9, z) for z in range(cz - 8, cz + 5)]
    for (x, z) in path:
        for dz in (0, 1):
            X, Z = (x, z + dz) if z == cz - 8 else (x - dz, z)
            if w.id(X, y - 1, Z) == B.AIR:
                w.set(X, y - 1, Z, B.PLANKS, 5)
                for yy in range(y, y + 3):
                    if w.id(X, yy, Z) not in (B.AIR,):
                        w.set(X, yy, Z, B.AIR)
        # the rail on the open side, a bracket below every fourth plank
        rx, rz = (x, z + 2) if z == cz - 8 else (x - 2, z)
        if w.id(rx, y - 1, rz) == B.AIR:
            w.set(rx, y, rz, B.DARK_OAK_FENCE)
        if (x + z) % 4 == 0:
            for yy in range(FLOOR, y - 1):
                bx, bz = (x, z + 1) if z == cz - 8 else (x - 1, z)
                if w.id(bx, yy, bz) == B.AIR:
                    w.set(bx, yy, bz, B.LOG2, 1)
    # stairs down from the catwalk's west end to the floor
    sx, sz = cx - 8, cz - 7
    for i in range(y - FLOOR):
        for dz in (0, 1):
            w.set(sx - i, y - 1 - i, sz + dz, B.SPRUCE_STAIRS, 0)
            for yy in range(y - i, y - i + 3):
                if w.id(sx - i, yy, sz + dz) not in (B.AIR,):
                    w.set(sx - i, yy, sz + dz, B.AIR)
    # no hoist over the hole any more: the core's well comes down through the roof there, and lava falls clear
    # lamps: glowstone hung from the roof on fence
    for (lx, lz) in ((cx - 3, cz - 3), (cx + 4, cz + 5), (cx - 7, cz + 4), (cx + 6, cz - 6)):
        roof = next((yy for yy in range(FLOOR + 3, FLOOR + 14) if w.id(lx, yy, lz) != B.AIR), None)
        if roof:
            w.set(lx, roof - 1, lz, B.DARK_OAK_FENCE)
            w.set(lx, roof - 2, lz, B.GLOWSTONE)


def gallery(w, L, pts, width=1, torches=True, rails=True):
    """A timbered drift through straight runs between points: three wide, three tall, sets every four."""
    path = []
    for (ax, ay, az), (bx, by, bz) in zip(pts[:-1], pts[1:]):
        n = int(max(abs(bx - ax), abs(bz - az), 1))
        for i in range(n):
            t = i / n
            path.append((ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t))
    path.append(pts[-1])
    clean = []
    for x, y, z in path:
        p = (int(round(x)), int(round(y)), int(round(z)))
        if clean and (p[0], p[2]) == (clean[-1][0], clean[-1][2]):
            continue
        if clean:
            p = (p[0], clean[-1][1] + int(np.clip(p[1] - clean[-1][1], -1, 1)), p[2])
        clean.append(p)
    for i, (x, y, z) in enumerate(clean):
        nxt = clean[min(i + 1, len(clean) - 1)]
        prv = clean[max(i - 1, 0)]
        along_x = abs(nxt[0] - prv[0]) >= abs(nxt[2] - prv[2])
        for k in range(-width, width + 1):
            ox, oz = (0, k) if along_x else (k, 0)
            for dy in (0, 1, 2):
                w.set(x + ox, y + dy, z + oz, B.AIR)
            w.set(x + ox, y - 1, z + oz, B.GRAVEL if RNG.random() < 0.4 else B.HARDENED_CLAY)
        if nxt[1] < y:
            sd = (1 if nxt[0] < x else 0) if along_x else (3 if nxt[2] < z else 2)
            for k in range(-width, width + 1):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y - 1, z + oz, B.COBBLE)
                w.set(nxt[0] + ox, nxt[1], nxt[2] + oz, B.COBBLE_STAIRS, sd)
        elif rails and nxt[1] == y and prv[1] == y:
            w.set(x, y, z, B.RAIL, 1 if along_x else 0)
        if i % 4 == 2:
            for k in (-width - 1, width + 1):
                ox, oz = (0, k) if along_x else (k, 0)
                for dy in (0, 1):
                    w.set(x + ox, y + dy, z + oz, B.LOG2, 1)
            for k in range(-width - 1, width + 2):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y + 2, z + oz, B.LOG2, 1 | (8 if along_x else 4))
            if torches and i % 8 == 2:
                tx, tz = (x, z + width) if along_x else (x + width, z)
                w.set(tx, y + 1, tz, B.TORCH, 4 if along_x else 2)
    # gold in the walls of the drift
    for x, y, z in clean[::3]:
        ox, oy, oz = int(RNG.integers(-2, 3)), int(RNG.integers(0, 3)), int(RNG.integers(-2, 3))
        if w.id(x + ox, y + oy, z + oz) not in (B.AIR, B.LOG2, B.RAIL, B.TORCH):
            w.set(x + ox, y + oy, z + oz, B.GOLD_ORE if RNG.random() < 0.5 else B.IRON_ORE)
    return clean


def portal(w, x, y, z, facing_x=True):
    """A timber frame round a drift's mouth in a cliff."""
    for k in (-2, 2):
        for dy in range(0, 4):
            if facing_x:
                w.set(x, y + dy, z + k, B.LOG2, 1)
            else:
                w.set(x + k, y + dy, z, B.LOG2, 1)
    for k in range(-2, 3):
        if facing_x:
            w.set(x, y + 3, z + k, B.LOG2, 1 | 8)
        else:
            w.set(x + k, y + 3, z, B.LOG2, 1 | 4)


def shaft(w, L):
    """From the plateau down to the Throat's floor: a timber-lined well with a ladder on its north side."""
    sx, sz = SHAFT
    top = int(L.H[sx - L.x0, sz - L.z0])
    for y in range(FLOOR, top + 3):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(sx + dx, y, sz + dz, B.AIR)
        for dx, dz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            if y <= top:
                w.set(sx + dx, y, sz + dz, B.LOG2, 1)
        for d in (-1, 0, 1):
            for (ox, oz) in ((d, -2), (d, 2), (-2, d), (2, d)):
                if y <= top and w.id(sx + ox, y, sz + oz) != B.AIR or y < top - 30:
                    pass
                if y <= top:
                    w.set(sx + ox, y, sz + oz, B.PLANKS, 5)
        if y <= top:
            w.set(sx, y, sz - 1, B.LADDER, 3)
    # the shaft's foot opens into the cavern: clear the lining on the cavern side below the roof
    for y in range(FLOOR, FLOOR + 3):
        for d in (-1, 0, 1):
            w.set(sx + 2, y, sz + d, B.AIR)
            w.set(sx + d, y, sz + 2, B.AIR)
    L.shaft_top = top


def chimney(w, L):
    """The Chimney: a water-cut crack from the foot of the canyon wall, climbing inside the rock to the
    Throat's floor. Its mouth opens on the canyon floor; the rest stays under the rock."""
    carve_tube(w, L, CHIMNEY, allow_surface_first=3)
    # its mouth: a narrow cleft up the wall face so it reads from the street
    x, y, z = CHIMNEY[0][0], CHIMNEY[0][1], CHIMNEY[0][2]
    for dy in range(0, 9):
        for dx in (0, -1, -2):
            if RNG.random() < 0.85 - dy * 0.06:
                w.set(x + dx, y + dy, z, B.AIR)


def workings(w, L):
    """The Old Workings: a drift off the Throat's west side to where the gold ran out, a chest left there."""
    clean = gallery(w, L, [(p[0], p[1], p[2]) for p in WORKINGS], width=1)
    ex, ey, ez = clean[-1]
    w.chest(ex, ey, ez - 1, [(0, "minecraft:gold_ingot", 4, 0), (1, "minecraft:golden_apple", 1, 0),
                             (2, "minecraft:arrow", 24, 0), (13, "minecraft:iron_pickaxe", 1, 0)], facing=3)
    # join it to the cavern
    carve_ellipsoid(w, L, -79, FLOOR + 1.5, -21, 3.0, 2.2, FLOOR)


def adit(w, L):
    clean = gallery(w, L, ADIT, width=1)
    x, y, z = ADIT[0]
    portal(w, x, y, z, facing_x=True)
    # the drift breaks out onto the catwalk
    carve_ellipsoid(w, L, -61, 51.5, -32, 2.5, 2.0, 50)
    return clean


def south_drift(w, L):
    """The South Drift: the tram's far end, a short drift the miners gave up on, an ore cart and a chest."""
    z = 80
    x0 = int(round(P.canyon_x(z) - P.FLOOR_HALF - P.LOWER_CLIFF - P.BENCH_WIDTH)) - 1
    pts = [(x0 + 1, P.BENCH_Y, z), (x0 - 8, P.BENCH_Y, z), (x0 - 12, P.BENCH_Y, z + 3)]
    clean = gallery(w, L, pts, width=1)
    portal(w, x0, P.BENCH_Y, z, facing_x=True)
    ex, ey, ez = clean[-1]
    w.chest(ex - 1, ey, ez, [(0, "minecraft:gold_ingot", 3, 0), (1, "minecraft:bread", 6, 0),
                             (2, "minecraft:tnt", 2, 0), (13, "minecraft:iron_helmet", 1, 0)], facing=5)
    # an ore cart: a cauldron of gold ore on the last rail
    w.set(ex + 3, ey, ez - 1, B.CAULDRON)
    L.drift_mouth = (x0, P.BENCH_Y, z)


def build(w, L):
    cavern(w, L)
    chimney(w, L)
    L.adit_path = adit(w, L)
    workings(w, L)
    catwalk(w, L)
    shaft(w, L)                     # after the catwalk, whose stair ran through it: the ladder climbs whole
    core(w, L)
    south_drift(w, L)
