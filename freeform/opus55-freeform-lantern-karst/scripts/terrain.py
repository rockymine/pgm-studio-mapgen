"""The karst islands of Lantern Karst, on red's half (z < 0); gen.py turns them onto blue's.

Every island is its plan polygon at its floor height, exactly: the walked top is the plan, so the gaps the
plan measured are the gaps in the world. Under the floor:

  the slab     floor-1 .. floor-5, stone with andesite courses, a vertical cliff face;
  the course   floor-6, bedrock under all but the island's outermost ring, so a dug pit stops there;
  the root     below that, a karst cone tapering to a point in the mist, deeper the further a column is from
               the island's edge, fluted by noise. Nobody plays on it.

Where two pieces meet at different heights the join is made walkable: one block is a row of slabs on the lower
side; two blocks is a flight of stairs (the whole width of a run up to 14, else a flight of 10 in its middle,
the rest a retaining wall of stone brick); more is a wall.

Then the two marks the author asked a floating board to carry: block 36 at y 0 under every column a player may
build in, and a line of redstone along every island edge that faces a build zone.
"""
import numpy as np
from scipy import ndimage

import geometry as G
import plan as P
from mc import B
from noise import fbm

NX, NZ = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
XS = np.arange(P.X_MIN, P.X_MAX + 1); ZS = np.arange(P.Z_MIN, P.Z_MAX + 1)
X, Z = np.meshgrid(XS.astype(float), ZS.astype(float), indexing="ij")
RED = Z < 0


def ix(x):
    return x - P.X_MIN


def iz(z):
    return z - P.Z_MIN


def piece_floor(p):
    """The floor height over the board for one piece: its y, or a climb, or a ramp."""
    m = G.inside(X, Z, p["poly"]) & RED
    if "hole" in p:
        m &= ~G.inside(X, Z, p["hole"])
    H = np.full(X.shape, -1, int)
    if p["key"] == "road":                       # flat past the Rows, then a block a stretch up to the room
        y = np.select([Z >= -58, Z >= -66, Z >= -78], [66, 67, 68], 69)
        H[m] = y[m]
    elif p["key"] == "drying":                   # rises from the hub to the road, a block every six
        y = np.select([X <= 37, X <= 43], [66, 67], 68)
        H[m] = y[m]
    elif p["key"].startswith("neck"):            # the spawn's exits: 67 off the hub, 68 under the terrace
        H[m] = np.where(Z >= -82, 67, 68)[m]
    else:
        H[m] = p["y"]
    return m, H


class Field:
    """The board's floors and masks, red's half only."""

    def __init__(self):
        self.H = np.full(X.shape, -1, int)
        self.key = np.full(X.shape, "", object)
        self.kind = np.full(X.shape, "", object)
        for p in P.PIECES + [P.BELL_ROCK]:
            m, H = piece_floor(p)
            self.H = np.where(m, H, self.H)
            self.key = np.where(m, p["key"], self.key)
            self.kind = np.where(m, p.get("kind", "rock"), self.kind)
        self.land = self.H >= 0
        self.zone = np.zeros(X.shape, bool)
        for zn in P.BUILD_ZONES:
            self.zone |= G.inside(X, Z, zn["poly"])
        self.zone &= RED
        # distance into the land from its edge, for the roots' depth
        self.depth_in = ndimage.distance_transform_edt(self.land)
        self.noise = fbm(X.shape, 9, 3, seed=11)
        self.flute = fbm(X.shape, 3, 2, seed=12)
        self.strata = fbm(X.shape, 14, 2, seed=13)
        self.spire = fbm(X.shape, 4, 1, seed=14) - 0.25
        self.bulge = fbm(X.shape, 5, 2, seed=15)
        self.paint = {}                         # (x, z) -> (id, data) of the top block, set by dressing


# The karst's beds, by world height (they follow the ground, tilted a little by the strata noise): stone carries
# them, andesite in courses, a dark bed of cyan stained clay (dark grey in this version), a pale bed of light grey
# stained clay, and a thin seam of gravel. One rock read in several tones, never two rocks.
BEDS = [(B.STONE, 0)] * 3 + [(B.STONE, 5)] * 2 + [(B.STAINED_CLAY, 9)] + [(B.STONE, 0)] * 2 + \
       [(B.STONE, 5)] + [(B.STAINED_CLAY, 8)] + [(B.STONE, 0)] * 3 + [(B.STAINED_CLAY, 9)] * 2 + [(B.STONE, 5)]


def rock(y, tilt, rng):
    bed = BEDS[(y + int(4 * tilt)) % len(BEDS)]
    r = rng.random()
    if bed == (B.STONE, 0) and r < 0.06:
        return (B.COBBLE, 0)
    if bed == (B.STONE, 5) and r < 0.08:
        return (B.GRAVEL, 0) if r < 0.02 else (B.STONE, 0)
    return bed


def root_bottom(F):
    """The lowest y of each land column: a cone under the course, deeper inland, fluted, with spires."""
    d = F.depth_in
    drop = 3.2 * d ** 0.85 * (1.0 + 0.35 * F.noise) + 4.5 * F.flute + 9.0 * np.maximum(F.spire, 0)
    bottom = F.H - 7 - np.maximum(drop, 0)
    return np.where(F.land, np.maximum(bottom, 26), 999).astype(int)


def write(w, F):
    """The islands' rock: slab, bedrock course, root."""
    bottom = root_bottom(F)
    rng = np.random.default_rng(5)
    for i, j in zip(*np.nonzero(F.land)):
        x, z = int(XS[i]), int(ZS[j])
        h = int(F.H[i, j])
        edge = F.depth_in[i, j] <= 1.0
        for y in range(int(bottom[i, j]), h + 1):
            if y == h - 6 and not edge:
                bid, dd = B.BEDROCK, 0
            else:
                bid, dd = rock(y, F.strata[i, j], rng)
            if edge and y > h - 6 and rng.random() < 0.18:
                bid, dd = B.MOSSY, 0
            w.set(x, y, z, bid, dd)
        # the top: grass over dirt by default; dressing repaints it
        w.set(x, h, z, B.GRASS)
        w.set(x, h - 1, z, B.DIRT)
    skirt(w, F, rng)


def skirt(w, F, rng):
    """Karst faces, not box sides: rock bulges out under the rim as ledges (never above floor-2, so the walked
    top and the plan's gaps are untouched), and the face is undercut where the bulge noise is low."""
    near = ndimage.distance_transform_edt(~F.land)
    Hn = ndimage.maximum_filter(np.where(F.land, F.H, -1), size=5)
    out = (~F.land) & RED & (near <= 2.2) & (Hn >= 0)
    for i, j in zip(*np.nonzero(out)):
        b = F.bulge[i, j]
        reach = 1 if b > 0.05 else 0
        reach += 1 if b > 0.3 else 0
        if near[i, j] > reach:
            continue
        x, z, h = int(XS[i]), int(ZS[j]), int(Hn[i, j])
        top = h - 2 - int(near[i, j]) - (1 if b < 0.2 else 0)
        bot = h - 6 - int(4 * max(0, b)) - int(rng.integers(0, 3))
        for y in range(bot, top + 1):
            w.set(x, y, z, *((B.MOSSY, 0) if rng.random() < 0.12 else rock(y, F.strata[i, j], rng)))
        if rng.random() < 0.5 and w.id(x, top + 1, z) == B.AIR:
            w.set(x, top + 1, z, B.TALLGRASS, 2 if rng.random() < 0.5 else 1)
    # undercuts: the rim cell's rock between floor-2 and floor-5 cut back where the noise is low
    rim = F.land & RED & (F.depth_in <= 1.0) & (F.bulge < -0.25) & (F.kind != "wool")
    for i, j in zip(*np.nonzero(rim)):
        x, z, h = int(XS[i]), int(ZS[j]), int(F.H[i, j])
        for y in range(h - 5, h - 2):
            w.set(x, y, z, B.AIR)


def joins(w, F):
    """Make every step between pieces walkable: slabs for one block, stairs for two, walls for more."""
    H = F.H
    runs = {}
    for i, j in zip(*np.nonzero(F.land)):
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < NX and 0 <= b < NZ and H[a, b] > H[i, j]:
                runs.setdefault((di, dj, int(H[a, b] - H[i, j]), int(H[i, j])), []).append((i, j))
    for (di, dj, d, ylo), cells in runs.items():
        # stairs data: ascending toward +x 0, -x 1, +z 2, -z 3
        data = {(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}[(di, dj)]
        # group the cells into straight runs along the join
        along = 1 if di else 0
        cells.sort(key=lambda c: (c[1 - along], c[along]))
        groups, cur = [], []
        for c in cells:
            if cur and (c[1 - along] != cur[-1][1 - along] or c[along] != cur[-1][along] + 1):
                groups.append(cur); cur = []
            cur.append(c)
        if cur:
            groups.append(cur)
        for g in groups:
            n = len(g)
            if d == 1:
                for i, j in g:
                    if w.id(int(XS[i]), ylo + 1, int(ZS[j])) == B.AIR:
                        w.set(int(XS[i]), ylo + 1, int(ZS[j]), B.SLAB, 5)
            elif d == 2:
                lo_, hi_ = (0, n) if n <= 14 else ((n - 10) // 2, (n - 10) // 2 + 10)
                for k, (i, j) in enumerate(g):
                    x, z = int(XS[i]), int(ZS[j])
                    xh, zh = x + di, z + dj
                    if lo_ <= k < hi_:
                        w.set(x, ylo + 1, z, B.STONEBRICK_STAIRS, data)
                        w.set(xh, ylo + 2, zh, B.STONEBRICK_STAIRS, data)
                    else:
                        w.set(xh, ylo + 2, zh, B.STONEBRICK)        # the retaining wall's top
                        w.set(xh, ylo + 1, zh, B.STONEBRICK)


def markers(w, F):
    """Block 36 at y 0 under every buildable column, red's half (the turn copies it)."""
    build = (F.land | F.zone) & RED
    for i, j in zip(*np.nonzero(build)):
        w.set(int(XS[i]), P.MARKER_Y, int(ZS[j]), 36)
    return int(build.sum())


def build_outline(w):
    """The build region's outline as the studio stamps it (rules.md ST5, BuildMarkerStamper): an unpowered
    redstone line at y 1, two blocks out from every void-facing edge of the build zones, one air block clear
    of the zones and of the terrain; at a convex corner the two lines turn into each other. Over both halves,
    from the zones and islands of both."""
    build = np.zeros((NX, NZ), bool)
    for zn in P.BUILD_ZONES:
        for poly in (zn["poly"], [P.rot(a, b) for a, b in zn["poly"]]):
            build |= G.inside(X, Z, poly)
    terr = np.zeros((NX, NZ), bool)
    for p in P.PIECES + [P.BELL_ROCK]:
        for poly in (p["poly"], [P.rot(a, b) for a, b in p["poly"]]):
            terr |= G.inside(X, Z, poly)
    # what the islands actually occupy at any height in play counts as terrain too (ledges of the skirt)
    terr |= (w.ids[:, 40:100, :] != 0).any(axis=1)          # the mist lies below 40
    sides = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    corners = [(0, 2), (0, 3), (1, 2), (1, 3)]
    marker = set()

    def ok(i, j):
        return 0 <= i < NX and 0 <= j < NZ
    for i, j in zip(*np.nonzero(build)):
        fv = []
        for dx, dz in sides:
            a, b = i + dx, j + dz
            fv.append(ok(a, b) and not build[a, b] and not terr[a, b])
        for k, (dx, dz) in enumerate(sides):
            if fv[k]:
                marker.add((i + 2 * dx, j + 2 * dz))
        for f, g in corners:
            if fv[f] and fv[g]:
                (ax, az), (bx, bz) = sides[f], sides[g]
                for st in (1, 2):
                    marker.add((i + ax * st + bx * 2, j + az * st + bz * 2))
                    marker.add((i + ax * 2 + bx * st, j + az * 2 + bz * st))
    crowd = ndimage.maximum_filter(build | terr, size=3)
    n = 0
    for i, j in marker:
        if ok(i, j) and not crowd[i, j]:
            w.set(int(XS[i]), 1, int(ZS[j]), 55, 0)
            n += 1
    return n


def vines(w, F, rng):
    """Vines on the roots only (below the course), where no one can reach them from a floor."""
    bottom = root_bottom(F)
    n = 0
    for i, j in zip(*np.nonzero(F.land & (F.kind != "wool"))):
        x, z, h = int(XS[i]), int(ZS[j]), int(F.H[i, j])
        for (dx, dz, bit) in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
            if rng.random() > 0.05:
                continue
            top = min(h - 9, int(bottom[i, j]) + int(rng.integers(3, 12)))
            ln = int(rng.integers(3, 10))
            for y in range(top, max(int(bottom[i, j]), top - ln), -1):
                if w.id(x, y, z) != B.AIR and w.id(x + dx, y, z + dz) == B.AIR:
                    w.set(x + dx, y, z + dz, B.VINE, bit)
                    n += 1
    return n


def mist(w):
    """The mist under the board, over both halves and no symmetry: white glass above, light grey below,
    a ragged rim of plain glass."""
    shape = (NX, NZ)
    gather = fbm(shape, 18, 3, seed=50) + 0.35 * fbm(shape, 6, 2, seed=51)
    base = 31 + 2.5 * fbm(shape, 22, 2, seed=52)
    n = 0
    for i in range(NX):
        for j in range(NZ):
            gv = gather[i, j]
            if gv < 0.02:
                continue
            thick = min(8, (gv - 0.02) * 24)
            if thick < 2.0:
                continue                                  # no single-layer sheets: mist is a body or nothing
            b = base[i, j]
            lo, hi = int(round(b - thick * 0.5)), int(round(b + thick * 0.5))
            lo, hi = max(lo, P.MIST_Y[0]), min(hi, P.MIST_Y[1])
            rim = False
            x, z = int(XS[i]), int(ZS[j])
            col = w.ids[i, :, j]
            for y in range(lo, hi + 1):
                if col[y] != B.AIR:
                    continue
                if rim:
                    if (x + y + z) % 2 == 0:
                        w.set(x, y, z, B.GLASS)
                elif y == lo:
                    w.set(x, y, z, 95, 8)
                else:
                    w.set(x, y, z, 95, 0)
                n += 1
    return n


def spires(w, rng):
    """Karst towers standing alone in the mist round the board: scenery, never play. Each stands at least 16
    blocks off any island or build zone of either half, rises from the mist to 60..96, ledged, vined, and
    carries a pine or two on its crown. No symmetry."""
    solid = np.zeros((NX, NZ), bool)
    for p in P.PIECES + [P.BELL_ROCK]:
        for poly in (p["poly"], [P.rot(a, b) for a, b in p["poly"]]):
            solid |= G.inside(X, Z, poly)
    for zn in P.BUILD_ZONES:
        for poly in (zn["poly"], [P.rot(a, b) for a, b in zn["poly"]]):
            solid |= G.inside(X, Z, poly)
    clear = ndimage.distance_transform_edt(~solid)
    sites = []
    tries = 0
    while len(sites) < 16 and tries < 4000:
        tries += 1
        i, j = int(rng.integers(4, NX - 4)), int(rng.integers(4, NZ - 4))
        r = float(rng.uniform(3, 7))
        if clear[i, j] < 16 + r or any(np.hypot(i - a, j - b) < r + q + 6 for a, b, q, _ in sites):
            continue
        top = int(rng.integers(60, 97))
        sites.append((i, j, r, top))
    import buildings
    n = 0
    for i, j, r, top in sites:
        bulge = fbm((int(2 * r + 9), 80, int(2 * r + 9)), 4, 2, seed=int(i * 31 + j))
        for y in range(28, top + 1):
            t = (y - 28) / max(1, top - 28)
            rr = r * (1.15 - 0.45 * t) + (0.8 if (y % 9) == 0 else 0)
            R = int(rr + 2)
            for dx in range(-R, R + 1):
                for dz in range(-R, R + 1):
                    b = bulge[dx + R if dx + R < bulge.shape[0] else -1, (y - 28) % 80, dz + R if dz + R < bulge.shape[2] else -1]
                    if dx * dx + dz * dz <= (rr + 1.4 * b) ** 2:
                        x, z = int(XS[i]) + dx, int(ZS[j]) + dz
                        if w.id(x, y, z) in (B.AIR, 95, B.GLASS):
                            w.set(x, y, z, *rock(y, b, rng))
                            n += 1
        cx, cz = int(XS[i]), int(ZS[j])
        cr = int(r * 0.7)
        for dx in range(-cr, cr + 1):
            for dz in range(-cr, cr + 1):
                if dx * dx + dz * dz <= cr * cr and w.id(cx + dx, top, cz + dz) == B.STONE:
                    w.set(cx + dx, top, cz + dz, B.GRASS)
        buildings.spruce(w, cx, top, cz, int(rng.integers(7, 12)), rng)
        if r > 5:
            buildings.spruce(w, cx + cr - 1, top, cz - 1, int(rng.integers(5, 8)), rng)
        # vines down the tower's faces
        for k in range(int(r * 6)):
            a = rng.uniform(0, 2 * np.pi)
            y0 = int(rng.integers(40, top - 2))
            for y in range(y0, y0 - int(rng.integers(3, 12)), -1):
                for rad in range(int(r + 3), 0, -1):
                    x, z = cx + int(round(rad * np.cos(a))), cz + int(round(rad * np.sin(a)))
                    if w.id(x, y, z) == B.AIR:
                        nb = [(x + 1, z, 8), (x - 1, z, 2), (x, z + 1, 1), (x, z - 1, 4)]
                        for xx, zz, bit in nb:
                            if w.id(xx, y, zz) == B.STONE:
                                w.set(x, y, z, B.VINE, bit)
                                break
                        else:
                            continue
                        break
    return len(sites), n
