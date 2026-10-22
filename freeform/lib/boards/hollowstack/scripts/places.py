"""Hollowstack's places: what stands in the hollows and on the Tops once the rock and the passages are cut.

    underwood(w, floor, roof, rng)   trees under the roof, ground cover, vines down the walls, glowstone stars in
                                     the roof, lilies on the pond, a path from the gatehouse to the spur
    shrine(w)                        the Grove Shrine on the spur: a ruined round of pillars and its altar
    vault(w)                         the Vault's dais at the back of the Undercroft's front room
    deep(w, caves, rng)              huge mushrooms in the grotto, glowstone over the lava hall
    tops(w, S, rng)                  the wood on the Tops, the path from the keep's gate to the brink
    keep(w, S)                       the keep: a curtain wall with four towers round the yard, its gate to the
                                     west, the well house in the yard, the monuments' plinths
    watch(w, S)                      the broken watch tower at the brink
    face(w, rng)                     moss and vines on the chasm's face

Every function draws blue's half; the half turn copies it.
"""
import math

import numpy as np

import layout as L
from pgmvox import B
from pgmvox.built import build as BLD
from pgmvox.geom import noise as N
from pgmvox.scenery import green as GR
from pgmvox.scenery import trees as TR

VINE_SIDE = {(0, 1): 1, (-1, 0): 2, (0, -1): 4, (1, 0): 8}          # the vine's bit for the solid on that side


def _vines(w, cells, rng, length=(3, 10)):
    """A strand of vines down from each (x, y, z) that has rock beside it, as long as the rock goes on beside it."""
    n = 0
    for x, y, z in cells:
        for (dx, dz), bit in VINE_SIDE.items():
            if w.id(x + dx, y, z + dz) not in (B.AIR, B.WATER, B.VINE, B.LEAVES, B.LEAVES2) and w.id(x, y, z) == B.AIR:
                for k in range(int(rng.integers(*length))):
                    if w.id(x, y - k, z) != B.AIR or w.id(x + dx, y - k, z + dz) in (B.AIR, B.WATER):
                        break
                    w.set(x, y - k, z, B.VINE, bit)
                    n += 1
                break
    return n


def underwood(w, floor, roof, rng):
    X, Z = w.grid()
    cut = floor >= 0
    f = L.UNDERWOOD_FLOORS
    s = L.SHRINE
    spur = (X >= s["x0"] - 1) & (X <= s["x1"] + 1) & (Z >= s["z0"] - 1) & (Z <= s["z1"] + 1)
    gx, _, gz = L.cell_box(L.UNDERCROFT, *L.GATEHOUSE, 3)
    court = np.hypot(X - gx - 2, Z - gz - 2) < 7
    pond = np.hypot((X - 37) / 8.0, (Z + 9) / 5.5) < 1.1
    rx, rz, rr = L.ROOT_WELL
    well = np.hypot(X - rx, Z - rz) < rr + 2
    grass = np.zeros(X.shape, bool)
    for i, k in np.argwhere(cut):
        grass[i, k] = w.ids[i, floor[i, k], k] == B.GRASS
    room = roof - floor
    zone = grass & ~spur & ~court & ~pond & ~well & (room > 9) & (X > 20)
    kinds = TR.kinds(TR.library())
    x0, z0 = w.x0, w.z0

    def ground(x, z):
        return int(floor[x - x0, z - z0])

    def fits(x, z, t):
        h = max(b[1] for b in t.blocks) + 1
        rc = int(math.ceil(t.crown / 2)) + 1
        for dx in range(-rc, rc + 1):
            for dz in range(-rc, rc + 1):
                i, k = x + dx - x0, z + dz - z0
                if not (0 <= i < w.sx and 0 <= k < w.sz) or roof[i, k] < 0:
                    return False
                if floor[x - x0, z - z0] + h + 1 >= roof[i, k]:
                    return False
        return True
    planted = []
    n = TR.scatter(w, zone, kinds, {"tiny-oak": 4, "small-olive": 1.5, "dark-oak": 1.2, "tiny-spruce": 1.2,
                                    "olive": 1}, rng, spacing=0.95, tries=900, planted=planted, ok=fits, ground=ground)
    n += TR.scatter(w, zone & (np.hypot((X - 37) / 11.0, (Z + 9) / 8.0) < 1), kinds, {"willow": 1}, rng, spacing=0.9,
                    tries=200, planted=planted, ok=fits, ground=ground)
    cells = [(int(X[i, k]), int(floor[i, k]), int(Z[i, k])) for i, k in np.argwhere(grass & ~court & ~well)
             if rng.random() < 0.55]
    GR.ground_cover(w, cells, rng, {"grass": 5, "fern": 4, "tall_grass": 1.5, "large_fern": 1.5, "bush": 0.6},
                    low=lambda x, z: s["x0"] - 2 <= x <= s["x1"] + 2 and s["z0"] - 2 <= z <= s["z1"] + 2)
    for i, k in np.argwhere(grass & ~court):                      # mushrooms where it is darkest, under the trees
        if rng.random() < 0.02 and w.ids[i, floor[i, k] + 1, k] == B.AIR:
            w.ids[i, floor[i, k] + 1, k] = B.BROWN_MUSHROOM if rng.random() < 0.6 else B.RED_MUSHROOM
    for i, k in np.argwhere(cut & pond):                          # lilies and reeds on the pond
        y = f["water"]
        if w.ids[i, y, k] == B.WATER and w.ids[i, y + 1, k] == B.AIR and rng.random() < 0.08:
            w.ids[i, y + 1, k] = B.LILY
    stars, strands = [], []
    for i, k in np.argwhere(cut & (room > 6)):                    # the roof: glowstone stars, vines from its rim
        y = roof[i, k] + 1
        if w.ids[i, y, k] not in (B.AIR,) and rng.random() < 0.035:
            w.ids[i, y, k], w.dat[i, y, k] = B.GLOWSTONE, 0
            stars.append((i, k))
            if rng.random() < 0.3 and w.ids[i, y - 1, k] == B.AIR:
                w.ids[i, y - 1, k] = B.GLOWSTONE
        if rng.random() < 0.06:
            strands.append((int(X[i, k]), int(roof[i, k]), int(Z[i, k])))
    v = _vines(w, strands, rng, (4, 14))
    for x, y, z in _path_cells([(gx + 2, gz - 1), (40, 0), (28, 2), (s["x1"] + 1, 0)]):
        i, k = x - x0, z - z0
        if 0 <= i < w.sx and 0 <= k < w.sz and floor[i, k] >= 0 and w.ids[i, floor[i, k], k] == B.GRASS:
            w.ids[i, floor[i, k], k], w.dat[i, floor[i, k], k] = (B.GRAVEL, 0) if rng.random() < 0.4 else (B.DIRT, 1)
            if w.ids[i, floor[i, k] + 1, k] in (B.TALLGRASS, B.DOUBLE_PLANT):
                w.ids[i, floor[i, k] + 1, k] = 0
                if w.ids[i, floor[i, k] + 2, k] == B.DOUBLE_PLANT:
                    w.ids[i, floor[i, k] + 2, k] = 0
    return {"trees": n, "stars": len(stars), "vines": v}


def _path_cells(pts, width=1.6):
    out = set()
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        n = int(max(abs(bx - ax), abs(bz - az))) + 1
        for t in range(n + 1):
            x, z = ax + (bx - ax) * t / n, az + (bz - az) * t / n
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if math.hypot(dx, dz) <= width:
                        out.add((int(round(x + dx)), 0, int(round(z + dz))))
    return sorted(out)


def shrine(w):
    """The Grove Shrine: a floor of stone bricks on the spur, eight pillars round it, two still carrying their
    lintel, a slab roof fallen in, and the altar in the middle where the wool lies."""
    s = L.SHRINE
    y = s["floor"]
    cx, cz = (s["x0"] + s["x1"]) // 2, (s["z0"] + s["z1"]) // 2
    for x in range(s["x0"] + 1, s["x1"]):
        for z in range(s["z0"] + 1, s["z1"]):
            d = math.hypot(x - cx, z - cz)
            if d <= 4.6:
                w.set(x, y, z, *((B.STONEBRICK, 3) if d < 1 else (B.STONEBRICK, 1) if (x * 3 + z) % 5 == 0
                                 else (B.STONEBRICK, 0) if d < 3.8 else (B.STONE, 6)))
                for yy in range(y + 1, y + 8):
                    if w.id(x, yy, z) in (B.TALLGRASS, B.DOUBLE_PLANT, B.LEAVES):
                        w.set(x, yy, z, B.AIR)
    heights = [5, 3, 5, 2, 5, 4, 1, 5]
    for n, a in enumerate(range(0, 360, 45)):
        px = cx + round(4 * math.cos(math.radians(a)))
        pz = cz + round(4 * math.sin(math.radians(a)))
        for k in range(heights[n]):
            w.set(px, y + 1 + k, pz, *((B.STONEBRICK, 3) if k in (0, 4) else (B.COBBLE_WALL, 1) if k == 3 and heights[n] == 4
                                       else (B.STONEBRICK, 0) if k % 2 == 0 else (B.STONEBRICK, 1)))
    for x in range(cx - 3, cx + 4):                               # what is left of the lintel over the east side
        w.set(x, y + 6, cz - 4, B.SLAB, 5)
    for z in range(cz - 3, cz + 1):
        w.set(cx + 4, y + 6, z, B.SLAB, 13)
    w.set(cx, y + 1, cz, B.STONEBRICK, 3)                         # the altar; the wool lies on it
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        w.set(cx + dx, y + 1, cz + dz, B.STONEBRICK_STAIRS, {(1, 0): 1, (-1, 0): 0, (0, 1): 3, (0, -1): 2}[(dx, dz)])
    return (cx, y + 2, cz)


def shrine_room():
    s = L.SHRINE
    return (s["x0"], s["floor"] + 1, s["z0"], s["x1"], s["floor"] + 9, s["z1"])


def vault(w):
    """The Vault's dais against its east wall, between two lamp pillars, the wool on it."""
    vi0, vj0, vi1, vj1 = L.VAULT
    x0, y, z0 = L.cell_box(L.UNDERCROFT, vi0, vj0)
    x1, _, z1 = L.cell_box(L.UNDERCROFT, vi1, vj1)
    x, z = x1 + L.CELL - 3, (z0 + z1 + L.CELL - 1) // 2
    for dz in (-1, 0, 1):
        w.set(x, y + 1, z + dz, B.STONE, 6)
    w.set(x, y + 1, z, B.STONEBRICK, 3)
    w.set(x + 1, y + 1, z, B.STONEBRICK, 3)
    for dz in (-2, 2):
        for k in range(1, 4):
            w.set(x + 1, y + k, z + dz, *((B.STONE, 6) if k < 3 else (B.GLOWSTONE, 0)))
    return (x, y + 2, z)


def vault_room():
    vi0, vj0, vi1, vj1 = L.VAULT
    x0, y0, z0 = L.cell_box(L.UNDERCROFT, vi0, vj0)
    x1, _, z1 = L.cell_box(L.UNDERCROFT, vi1, vj1)
    return (x0 + 1, y0 + 1, z0 + 1, x1 + L.CELL - 2, y0 + 2 * L.STOREY - 2, z1 + L.CELL - 2)


def huge_mushroom(w, x, y, z, h, red, rng):
    """A huge mushroom on the floor at y: a stem h high and a cap, a dome of red or a flat plate of brown."""
    cap = B.RED_CAP if red else B.BROWN_CAP
    for k in range(1, h + 1):
        w.set(x, y + k, z, cap, 10)
    if red:
        for k in range(h - 2, h + 1):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    edge = max(abs(dx), abs(dz)) == 2
                    if (edge and abs(dx) + abs(dz) < 4) and k < h:
                        w.set(x + dx, y + k, z + dz, cap, 14)
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                w.set(x + dx, y + h + 1, z + dz, cap, 14)
    else:
        r = 3
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) < 2 * r - 1:
                    w.set(x + dx, y + h + 1, z + dz, cap, 14)


def deep(w, caves, rng):
    X, Z = w.grid()
    g, gf, gt = caves["grotto"]
    spots = [(64, 4, 6, True), (70, 12, 7, False), (77, 2, 5, True), (66, 13, 4, True), (79, 9, 6, False)]
    for x, z, h, red in spots:
        i, k = x - w.x0, z - w.z0
        if g[i, k] and gt[i, k] - gf[i, k] > h + 3:
            huge_mushroom(w, x, int(gf[i, k]), z, h, red, rng)
    for i, k in np.argwhere(g):
        if rng.random() < 0.08 and w.ids[i, gf[i, k] + 1, k] == B.AIR:
            w.ids[i, gf[i, k] + 1, k] = B.RED_MUSHROOM if rng.random() < 0.5 else B.BROWN_MUSHROOM
    for name in ("hall", "pool", "grotto"):
        m, f, t = caves[name]
        for i, k in np.argwhere(m):
            if rng.random() < (0.05 if name == "hall" else 0.03) and w.ids[i, t[i, k] + 1, k] != B.AIR:
                w.ids[i, t[i, k] + 1, k], w.dat[i, t[i, k] + 1, k] = B.GLOWSTONE, 0
        strands = [(int(X[i, k]), int(t[i, k]), int(Z[i, k])) for i, k in np.argwhere(m) if rng.random() < 0.05]
        if name != "hall":
            _vines(w, strands, rng, (2, 7))


def tops(w, S, rng):
    """The wood on the Tops, kept off the keep's hill, the brink and the paths; ground cover between."""
    X, Z = w.grid()
    kx0, kz0, kx1, kz1 = L.KEEP
    lx, lz, lr = L.LIGHT_WELL
    keep = (X >= kx0 - 4) & (X <= kx1 + 2) & (Z >= kz0 - 4) & (Z <= kz1 + 4)
    path = np.zeros(X.shape, bool)
    for x, _, z in _path_cells([(kx0 - 1, 0), (52, 2), (34, -2), (19, 0)], 1.6) + _path_cells([(46, 1), (lx + 4, lz + 2)]):
        i, k = x - w.x0, z - w.z0
        if 0 <= i < w.sx and 0 <= k < w.sz:
            path[i, k] = True
    for i, k in np.argwhere(path & (X >= 0)):
        y = int(S[i, k])
        if w.ids[i, y, k] == B.GRASS:
            w.ids[i, y, k], w.dat[i, y, k] = (B.GRAVEL, 0) if rng.random() < 0.5 else (B.DIRT, 1)
    land = (X >= 18) & (X <= L.BACK - 2) & (np.abs(Z) <= L.SIDE - 5)
    well = np.hypot(X - lx, Z - lz) < lr + 3
    glade = N.fbm(X.shape, 14, 2, seed=63) > 0.18                  # clearings the wood leaves open
    gate = (X >= kx0 - 14) & (X < kx0) & (np.abs(Z) <= 7)            # the ground before the keep's gate kept open
    zone = land & ~keep & ~path & ~well & ~glade & ~gate
    for i, k in np.argwhere(zone):
        if w.ids[i, int(S[i, k]), k] != B.GRASS:
            zone[i, k] = False
    kinds = TR.kinds(TR.library())
    planted = []

    def ground(x, z):
        return int(S[x - w.x0, z - w.z0])
    n = TR.scatter(w, zone, kinds, {"oak": 3, "birch": 2.5, "dense-oak": 1, "tiny-oak": 1.5}, rng, spacing=1.35,
                   tries=500, planted=planted, ground=ground)
    cells = [(int(X[i, k]), int(S[i, k]), int(Z[i, k])) for i, k in np.argwhere(land & ~keep & ~path)
             if rng.random() < 0.3]
    GR.ground_cover(w, cells, rng, {"grass": 6, "fern": 2, "tall_grass": 2, "large_fern": 0.6, "bush": 0.5})
    return n


def keep(w):
    """The keep on its hill: a curtain wall two thick and seven high with crenels, a square tower at each corner,
    the gate in the west wall, the yard paved, the monuments' plinths by the well house."""
    kx0, kz0, kx1, kz1 = L.KEEP
    y = L.KEEP_Y
    for x in range(kx0, kx1 + 1):                                # the yard
        for z in range(kz0, kz1 + 1):
            w.set(x, y, z, *((B.STONEBRICK, 0) if (x + z) % 7 else (B.STONE, 6)))
            for yy in range(y + 1, y + 12):
                if w.id(x, yy, z) not in (B.AIR,):
                    w.set(x, yy, z, B.AIR)
    X, Z = w.grid()
    H = np.full(X.shape, y, float)
    ring = [(kx0, kz0), (kx1, kz0), (kx1, kz1), (kx0, kz1)]
    courses = [(B.COBBLE, 0), (B.STONE, 5), (B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 0),
               (B.STONEBRICK, 0), (B.STONEBRICK, 0)]
    gate = (kx0, -1, 1)
    for (ax, az), (bx, bz) in zip(ring, ring[1:] + ring[:1]):
        for t in range(max(abs(bx - ax), abs(bz - az)) + 1):
            x = ax + (t if bx > ax else -t if bx < ax else 0)
            z = az + (t if bz > az else -t if bz < az else 0)
            for k, b in enumerate(courses):
                if x == gate[0] and gate[1] <= z <= gate[2] and k < 4:
                    continue
                w.set(x, y + 1 + k, z, *b)
            inward = (x - (1 if x == kx1 else -1 if x == kx0 else 0), z - (1 if z == kz1 else -1 if z == kz0 else 0))
            if inward != (x, z):
                w.set(*inward[:1], y + 7, inward[1], B.SLAB, 5)                  # the wall walk
            if (x + z) % 2 == 0:
                w.set(x, y + 8, z, B.SLAB, 5)                                     # crenels
    for cx, cz in ring:
        BLD.round_tower(w, cx, cz, 3, y, 12, wall=(B.STONEBRICK, 0), quoins=[(B.STONE, 5), (B.STONE, 6)],
                        crenel=(B.SLAB, 5), door_side="e" if cx == kx0 else "w", half=3, cut=False,
                        string=(B.STONE, 6), plinth=(B.COBBLE, 0), ground_at=lambda x, z: y)
    for x, _, z in L.MONUMENTS:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(x + dx, y, z + dz, B.STONEBRICK, 3 if dx == dz == 0 else 0)
    for z in (-2, 2):                                             # the gate's piers and lamps
        for k in range(1, 6):
            w.set(kx0 - 1, y + k, gate[1] - 1 if z < 0 else gate[2] + 1, B.STONE, 6)
        w.set(kx0 - 1, y + 6, gate[1] - 1 if z < 0 else gate[2] + 1, B.GLOWSTONE)


def watch(w, S):
    """The broken watch tower at the brink, over the chasm, north of the path."""
    x, z = 20, -12
    y = int(S[x - w.x0, z - w.z0])
    BLD.round_tower(w, x, z, 3.5, y, 9, wall=(B.STONEBRICK, 0), quoins=[(B.STONEBRICK, 1), (B.STONEBRICK, 2)],
                    crenel=(B.STONEBRICK, 1), door_side="e", ground_at=lambda a, b: int(S[a - w.x0, b - w.z0]))
    rng = np.random.default_rng(61)
    for dx in range(-4, 5):                                       # broken down on its chasm side
        for dz in range(-4, 5):
            for yy in range(y + 3, y + 12):
                lean = (-dx) * 0.9 + 0.8 * rng.random()
                if dx < 0 and yy - y > 9 - 2 * lean:
                    w.set(x + dx, yy, z + dz, B.AIR)
    for dx, dz in ((-5, 2), (-6, -1), (-4, 4)):                    # fallen blocks
        yy = int(S[x + dx - w.x0, z + dz - w.z0])
        w.set(x + dx, yy + 1, z + dz, B.STONEBRICK, 2)


def face(w, rng):
    """Moss on the chasm's face and vines down it."""
    X, Z = w.grid()
    strands = []
    for k in range(w.sz):
        for y in range(4, L.SY - 2):
            row = w.ids[:, y, k]
            xs = np.nonzero(row[-w.x0:] != 0)[0]
            if not len(xs):
                continue
            i = -w.x0 + int(xs[0])
            if rng.random() < 0.05 and row[i] == B.STONE:
                w.ids[i, y, k], w.dat[i, y, k] = B.MOSSY, 0
            if rng.random() < 0.012:
                strands.append((int(X[i - 1, k]), y, int(Z[i - 1, k])))
    return _vines(w, strands, rng, (3, 12))


def settle(w):
    """Nothing that falls is left over air: gravel becomes cobble and sand sandstone where the block under is open."""
    ids = w.ids
    loose = np.isin(ids[:, 1:, :], (B.GRAVEL, B.SAND)) & np.isin(ids[:, :-1, :], (B.AIR, B.WATER, B.TALLGRASS,
                                                                                  B.VINE, B.TORCH))
    i, y, k = np.nonzero(loose)
    sand = ids[i, y + 1, k] == B.SAND
    ids[i, y + 1, k] = np.where(sand, B.SANDSTONE, B.COBBLE)
    w.dat[i, y + 1, k] = 0
    held = {3: (0, -1), 2: (0, 1), 5: (-1, 0), 4: (1, 0)}           # a ladder's data: the side its wall is on
    for li, ly, lk in np.argwhere(ids == B.LADDER):
        dx, dz = held.get(int(w.dat[li, ly, lk]), (0, 0))
        if not (0 <= li + dx < w.sx and 0 <= lk + dz < w.sz) or ids[li + dx, ly, lk + dz] in (B.AIR, B.WATER):
            ids[li, ly, lk] = B.AIR
    return len(i)


def made_mask(w, plans, margin=1):
    """Every block within `margin` of a cell a laid plan takes, as a mask over the world: what a carve keeps off."""
    m = np.zeros(w.ids.shape, bool)
    for g, p in plans:
        for c in p.taken():
            x, y, z = g.corner(*c)
            m[max(x - margin - w.x0, 0):x + g.cell + margin - w.x0, max(y - margin, 0):y + g.height + margin,
              max(z - margin - w.z0, 0):z + g.cell + margin - w.z0] = True
    return m


ROCK = (B.STONE, B.DIRT, B.GRASS, B.COAL_ORE, B.IRON_ORE, B.GOLD_ORE, B.MOSSY, B.GRAVEL)


def pocks(w, made, rng, n=110):
    """The cheese: hollows worn into the chasm's face and the walls' sides, each a flattened ball pressed into the
    rock from where the face stands, its floor level so a player can stand in it; never into a laid passage."""
    X, Z = w.grid()
    out = 0
    for _ in range(n * 4):
        if out >= n:
            break
        y = int(rng.integers(8, 92))
        on_side = rng.random() < 0.22
        if on_side:                                              # the board's sides, z at the wall's edge
            x = int(rng.integers(22, L.BACK - 4))
            sign = 1 if rng.random() < 0.5 else -1
            col = w.ids[x - w.x0, y, :]
            zs = np.nonzero(col != 0)[0]
            if not len(zs):
                continue
            z = int(Z[0, zs[-1] if sign > 0 else zs[0]])
            cx, cz = x, z - sign * int(rng.integers(1, 3))
        else:
            z = int(rng.integers(-L.SIDE + 3, L.SIDE - 3))
            row = w.ids[-w.x0:, y, z - w.z0]
            xs = np.nonzero(row != 0)[0]
            if not len(xs):
                continue
            cx, cz = int(xs[0]) + int(rng.integers(1, 3)), z
        big = rng.random() < 0.15
        rx, ry, rz = (rng.uniform(4.5, 7.0), rng.uniform(3.0, 4.5), rng.uniform(4.5, 7.0)) if big else \
            (rng.uniform(2.0, 4.6), rng.uniform(1.8, 3.4), rng.uniform(2.0, 4.6))
        box = [(xx, yy, zz) for xx in range(int(cx - rx - 1), int(cx + rx + 2))
               for yy in range(y, int(y + ry + 2)) for zz in range(int(cz - rz - 1), int(cz + rz + 2))]
        cells = [(xx, yy, zz) for xx, yy, zz in box
                 if ((xx - cx) / rx) ** 2 + ((yy - y) / (ry * 1.6)) ** 2 + ((zz - cz) / rz) ** 2 < 1]
        if any(not (0 <= xx - w.x0 < w.sx and 0 <= zz - w.z0 < w.sz) or made[xx - w.x0, yy, zz - w.z0]
               or xx < 0 for xx, yy, zz in cells):
            continue
        if any(w.id(xx + a, yy + b, zz + c) in (B.WATER, B.LAVA) for xx, yy, zz in cells
               for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0))):
            continue
        for xx, yy, zz in cells:
            if w.id(xx, yy, zz) in ROCK:
                w.set(xx, yy, zz, B.AIR)
        for xx, yy, zz in cells:                                 # its floor: what stands under it, rough
            if w.id(xx, y - 1, zz) in ROCK and rng.random() < 0.3:
                w.set(xx, y - 1, zz, *((B.GRAVEL, 0) if rng.random() < 0.5 else (B.COBBLE, 0)))
        out += 1
    return out


def fronts(w):
    """What is built into the chasm's face: the Undercroft's front, two arcades one over the other before the
    Vault; stone balconies under the Undercroft's upper ports; timber stages under the Workings' galleries."""
    vx, vy, vz = L.cell_box(L.UNDERCROFT, 0, 2)
    z0, z1 = vz, vz + 4 * L.CELL - 1
    x0, x1 = L.FACE, vx - 1
    for x in range(x0, x1 + 1):                                  # the loggias behind the front, two levels
        for z in range(z0, z1 + 1):
            for y in range(vy, vy + 2 * L.STOREY):
                level = (y - vy) % L.STOREY
                if level == 0:
                    w.set(x, y, z, *((B.STONEBRICK, 0) if (x + z) % 4 else (B.STONE, 6)))
                elif level == 5:
                    w.set(x, y, z, B.STONEBRICK, 0)
                else:
                    w.set(x, y, z, B.AIR)
    openings = {vz + j * L.CELL + q for j in range(4) for q in (1, 2, 3)}
    for z in range(z0 - 1, z1 + 2):                              # the front: piers between arches, a cornice
        for y in range(vy - 1, vy + 2 * L.STOREY + 1):
            level = (y - vy) % L.STOREY
            pier = z not in openings or z in (z0 - 1, z1 + 1)
            if y < vy or y >= vy + 2 * L.STOREY or level in (0, 5) or pier:
                b = (B.STONEBRICK, 3) if level == 0 and pier else (B.STONEBRICK, 1 if (z * 7 + y) % 9 == 0 else 0)
                w.set(x0, y, z, *b)
            elif level == 4 and (z - 1) in openings and (z + 1) in openings:
                w.set(x0, y, z, B.STONEBRICK, 0)                   # the arch's key over the middle
            elif level == 4:
                w.set(x0, y, z, B.STONEBRICK_STAIRS, 4 | (3 if (z - 1) not in openings else 2))
            elif level == 1 and y > vy + L.STOREY:
                w.set(x0, y, z, B.COBBLE_WALL, 0)                  # the upper arcade's rail
    for j in (0, 7):                                             # balconies under the upper ports
        _, by, bz = L.cell_box(L.UNDERCROFT, 0, j, 1)
        for z in range(bz, bz + L.CELL):
            for x in range(L.FACE, L.FACE + 3):
                if w.id(x, by, z) == B.AIR:
                    w.set(x, by, z, B.STONEBRICK, 0)
            if w.id(L.FACE, by + 1, z) == B.AIR:
                w.set(L.FACE, by + 1, z, B.COBBLE_WALL, 0)
        for x in range(L.FACE, L.FACE + 3):                      # a corbel under it
            for k, b in ((1, (B.STONEBRICK_STAIRS, 5)), (2, (B.STONEBRICK_STAIRS, 5))):
                for z in (bz + 1, bz + 3):
                    if w.id(x, by - k, z) == B.AIR and x - L.FACE < 3 - k:
                        w.set(x, by - k, z, *b)
    for j in (1, 6):                                             # timber stages under the Workings' galleries
        _, my, mz = L.cell_box(L.WORKINGS, 0, j)
        for z in range(mz, mz + L.CELL):
            for x in range(L.FACE - 2, L.FACE + 6):
                if w.id(x, my, z) == B.AIR:
                    w.set(x, my, z, B.PLANKS, 1)
            for x in (L.FACE - 2,):
                if w.id(x, my + 1, z) == B.AIR:
                    w.set(x, my + 1, z, B.SPRUCE_FENCE)
        for z in (mz, mz + L.CELL - 1):                          # struts down into the rock
            for k in range(1, 7):
                x = L.FACE - 2 + k // 2
                if w.id(x, my - k, z) == B.AIR:
                    w.set(x, my - k, z, B.LOG, 1)


def stubs(w, rng):
    """The broken bridge: a natural arch's stump reaching from blue's brink eight blocks into the chasm, its top
    flush with the Tops, thick at the face and thinning, ragged at its end; the half turn gives red the other, and
    eight blocks of chasm are left between them, the shortest crossing on the board."""
    y0 = L.TOPS - 3
    for x in range(L.FACE - 8, L.FACE + 4):
        t = (L.FACE + 4 - x) / 12.0                             # 0 at the face, 1 at the broken end
        half = 3.2 - 1.2 * t
        under = 6 - 4 * t
        for z in range(-5, 6):
            for y in range(int(y0 - under - 2), y0 + 2):
                d = abs(z) / half
                top = y0 + (1 if abs(z) < half - 1 else 0)
                bottom = y0 - under * math.sqrt(max(0, 1 - d * d))
                if d < 1 and bottom <= y <= top and not (t > 0.85 and rng.random() < 0.4):
                    w.set(x, y, z, *((B.GRASS, 0) if y == top and abs(z) < half - 1.5 else (B.STONE, 0)))
