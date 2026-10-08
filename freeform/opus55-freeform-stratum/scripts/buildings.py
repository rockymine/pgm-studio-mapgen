"""The city: every mass on red's half, poured and patterned with facade.py.

The Atrium (spawn) and its pylons to the land; the skyways; the Obelisk's plaza, the Obelisk, its stair and the
monument's balcony; the Reactor, its gallery, its shaft and the core hung over it; the Columns and their stairs;
the Forum and its colonnades; the Gate; the Lens; the Ziggurat; the Cantilever. Each claims its cells; a
claim on a cell already claimed is a conflict.
"""
import math

import numpy as np

import facade as Fa
import geometry as G
import plan as P
from mc import B

ORANGE = (B.STAINED_CLAY, 1)
BLACK = (B.STAINED_CLAY, 15)
GREY = (B.STAINED_CLAY, 7)
LIGHT = (B.STAINED_CLAY, 8)
WHITE = (B.STAINED_CLAY, 0)
TEAM = (B.STAINED_CLAY, 14)          # red; the mirror turns red clay and wool to blue
QUARTZ = (B.QUARTZ, 0)
RNG = np.random.default_rng(1969)
RECORDS = []


def claim(F, name, cells):
    hit = {F.occ[c] for c in cells if c in F.occ and F.occ[c] != name}
    for o in hit:
        F.conflicts.append((name, o))
    for c in cells:
        F.occ.setdefault(c, name)


def ground(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def stair_dir(dx, dz):
    """Stairs data for a stair that rises in the direction (dx, dz)."""
    return {(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}[(dx, dz)]


def ring_path(x0, z0, x1, z1):
    """The cells round a rectangle's outline, in order, clockwise from its north-west corner."""
    out = [(x, z0) for x in range(x0, x1 + 1)]
    out += [(x1, z) for z in range(z0 + 1, z1 + 1)]
    out += [(x, z1) for x in range(x1 - 1, x0 - 1, -1)]
    out += [(x0, z) for z in range(z1 - 1, z0, -1)]
    return out


def wound_stair(w, F, x0, z0, x1, z1, y_from, y_to, start=0, mat=(B.DSLAB, 8), stair=B.STONEBRICK_STAIRS):
    """A stair of single blocks wound round the outside of a rectangular shaft, rising a block each step,
    cantilevered from the shaft's face with nothing on its outer edge. Corners are landings."""
    path = ring_path(x0 - 1, z0 - 1, x1 + 1, z1 + 1)
    n = len(path)
    steps = []
    y = y_from
    i = start
    while y <= y_to:
        x, z = path[i % n]
        nx, nz = path[(i + 1) % n]
        px_, pz_ = path[(i - 1) % n]
        corner = (nx - x, nz - z) != (x - px_, z - pz_)
        w.set(x, y, z, *mat)
        if not corner and y < y_to:
            # the next block is a step up: lay this one as a stair rising toward it
            w.set(x, y, z, stair, stair_dir(nx - x, nz - z))
        for k in (1, 2, 3):
            if w.id(x, y + k, z) not in (B.AIR,) and (x, z) not in [(s[0], s[1]) for s in steps[-3:]]:
                w.set(x, y + k, z, B.AIR)
        steps.append((x, z, y))
        if not corner:
            y += 1
        i += 1
    return steps


# ---------------------------------------------------------------------------------------------------------
# the Atrium

def atrium(w, F):
    outer = Fa.rect_cells(-93, -13, -67, 13)
    court = Fa.rect_cells(-87, -7, -73, 7)
    ring = Fa.Mass(outer - court, 76, 88)
    faces = [Fa.band_from_top(2, 2, TEAM),                                   # the team's colour, set back, under the cornice
             Fa.glyph_row(4, ["gate", "eye", "step", "key", "sun", "chevron"], BLACK, spacing=7),
             Fa.flutes(3, 1, 1, 2),
             Fa.courses(4, Fa.DARK_CONCRETE)]
    Fa.build(w, ring, base=Fa.concrete(), faces=faces, top="cornice", bottom="coffer")
    floor = Fa.Mass(court, 76, P.COURT_Y)
    Fa.build(w, floor, base=Fa.concrete(), faces=[], bottom="coffer")
    # the court's floor: a field of light and dark squares, the spawn's square in team colour at the middle
    cx, cz = P.SPAWN
    for (x, z) in court:
        q = ((x - cx) // 2 + (z - cz) // 2) % 2
        w.set(x, P.COURT_Y, z, *(Fa.SMOOTH if q else Fa.DARK_CONCRETE))
        if abs(x - cx) <= 1 and abs(z - cz) <= 1:
            w.set(x, P.COURT_Y, z, *TEAM)
    # gates: north and south near the east end, toward the skyways, and one east toward the middle
    gates = []
    for gx0, gx1, gz0, gz1 in ((-76, -72, -13, -8), (-76, -72, 8, 13), (-73, -67, -2, 2)):
        for x in range(gx0, gx1 + 1):
            for z in range(gz0, gz1 + 1):
                for y in range(P.COURT_Y + 1, P.COURT_Y + 6):
                    w.set(x, y, z, B.AIR)
                w.set(x, P.COURT_Y, z, *Fa.SMOOTH)
                gates.append((x, z))
    # a flight up the west wall of the court to the roof
    for k in range(8):
        x, z = -86 + k, -7
        w.set(x, P.COURT_Y + 1 + k, z + 0, B.STONEBRICK_STAIRS, 0)
        for y in range(P.COURT_Y + 1, P.COURT_Y + 1 + k):
            w.set(x, y, z, *Fa.DARK_CONCRETE)
        for y in range(P.COURT_Y + 2 + k, P.COURT_Y + 5 + k):
            if y <= 88:
                w.set(x, y, z, B.AIR)
    # a chest of blocks for bridging
    w.chest(cx - 4, P.COURT_Y + 1, cz + 5, [(0, "minecraft:planks", 64, 0), (1, "minecraft:stone", 64, 0)], facing=2)
    claim(F, "the Atrium", outer)
    F.spawn = (cx, P.COURT_Y + 1, cz)
    # the pylons, down through the cloud to the land
    for p in P.PYLONS:
        (x0, z0), (x1, _), (_, z1) = p[0], p[1], p[2]
        cells = Fa.rect_cells(x0, z0, x1, z1)
        g = min(ground(F, x, z) for x, z in cells)
        m = Fa.Mass(cells, g - 3, 75)
        Fa.build(w, m, base=Fa.concrete(), faces=[Fa.flutes(2, 1, 0, 200), Fa.band(75 - (g - 3) - 6, 75 - (g - 3) - 6, ORANGE)])
        claim(F, "the Atrium", cells)            # under the Atrium: one mass with it
    RECORDS.append(dict(kind="the Atrium", floor=P.COURT_Y, cells=court | set(gates)))


def skyway(w, F, s):
    """A beam of concrete along a polyline, five wide, its deck graded from one end's height to the other,
    a slab parapet on each edge, an orange line along its sides, a dark course under it."""
    pts = s["pts"]
    X, Z = np.meshgrid(np.arange(-100, 0), np.arange(P.Z_MIN, P.Z_MAX + 1), indexing="ij")
    d, along = G.polyline(X, Z, pts)
    L = G.length(pts)
    y0, y1 = s["y"]
    cells = []
    for i, k in zip(*np.nonzero(d <= s["half"] + 0.5)):
        x, z = -100 + i, P.Z_MIN + k
        if (x, z) in F.occ:
            continue
        t = along[i, k] / L
        y = int(round(y0 + (y1 - y0) * t))
        edge = d[i, k] > s["half"] - 0.5
        w.set(x, y, z, *Fa.SMOOTH)
        w.set(x, y - 1, z, *(ORANGE if edge else Fa.CONCRETE))
        w.set(x, y - 2, z, *Fa.DARK_CONCRETE)
        if edge and 0.04 < t < 0.96:
            w.set(x, y + 1, z, B.SLAB, 0)
        cells.append((x, z))
    claim(F, s["name"], set(cells))


# ---------------------------------------------------------------------------------------------------------
# the Obelisk

def obelisk(w, F):
    plaza = Fa.Mass(Fa.poly_cells(P.PLAZA), 72, 78)
    Fa.build(w, plaza, base=Fa.concrete(), faces=[Fa.band(4, 4, ORANGE), Fa.flutes(4, 2, 0, 2)],
             top="parapet-slotted", bottom="coffer")
    claim(F, "the plaza", plaza.cells)
    # the plaza's top: long bands of light and dark running toward the Obelisk
    for (x, z) in plaza.cells:
        w.set(x, 78, z, *(Fa.SMOOTH if (z % 4) in (0, 1) else Fa.DARK_CONCRETE))
    (x0, z0), (x1, _), (_, z1) = P.OBELISK[0], P.OBELISK[1], P.OBELISK[2]
    shaft = Fa.Mass(Fa.rect_cells(x0, z0, x1, z1), 78, P.OBELISK_TOP)
    names = ["eye", "key", "sun", "step", "gate", "chevron", "cross", "bars"]
    faces = [Fa.glyph_row(t0, names[k:] + names[:k], BLACK, spacing=6, min_run=4) for k, t0 in enumerate(range(5, 40, 8))]
    faces.append(Fa.courses(8, LIGHT, offset=1))
    Fa.build(w, shaft, base=lambda x, y, z: QUARTZ if y % 8 else Fa.SMOOTH, faces=faces)
    # the pyramidion
    for k, r in enumerate((2, 1, 0)):
        cx0, cz0 = (x0 + x1) / 2, (z0 + z1) / 2
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if abs(x - cx0) <= r + 0.5 and abs(z - cz0) <= r + 0.5:
                    w.set(x, P.OBELISK_TOP + 1 + k, z, *(QUARTZ if k < 2 else (B.GOLD_BLOCK, 0)))
    # the stair wound round it: from the plaza at 78 up to the top, passing the balcony at 100 on the east
    # choose where the stair starts so that it passes the middle of the east face at the balcony's height
    path = ring_path(x0 - 1, z0 - 1, x1 + 1, z1 + 1)
    n = len(path)

    def lands(start):
        y, i = 79, start
        while y <= P.MONUMENT_Y - 1:
            x, z = path[i % n]
            nx, nz = path[(i + 1) % n]
            px_, pz_ = path[(i - 1) % n]
            if y == P.MONUMENT_Y - 1:
                return x == x1 + 1 and z0 + 1 <= z <= z1 - 1
            if (nx - x, nz - z) == (x - px_, z - pz_):
                y += 1
            i += 1
        return False
    start = next(s for s in range(n) if lands(s))
    steps = wound_stair(w, F, x0, z0, x1, z1, 79, P.OBELISK_TOP, start=start, mat=Fa.SMOOTH)
    # the balcony on the east face: a slab thrown out three, the monument in a niche cut two into the shaft
    by = P.MONUMENT_Y - 1
    east = x1
    for x in range(east + 1, east + 5):
        for z in range(z0 + 1, z1):
            w.set(x, by, z, *Fa.SMOOTH)
            w.set(x, by - 1, z, *Fa.DARK_CONCRETE)
            for y in range(by + 1, by + 4):
                if w.id(x, y, z) not in (B.AIR,) and not any(s[0] == x and s[1] == z for s in steps):
                    pass
    mz = (z0 + z1) // 2
    for x in (east, east - 1):
        for z in (mz, mz + 1):
            for y in range(by + 1, by + 4):
                w.set(x, y, z, B.AIR)
    w.set(east - 1, by + 1, mz, B.OBSIDIAN)
    w.set(east - 1, by + 2, mz, B.OBSIDIAN)
    w.set(east - 1, by + 1, mz + 1, *TEAM)
    w.set(east - 1, by + 2, mz + 1, *TEAM)
    F.monument = (east - 1, by + 1, mz)
    claim(F, "the plaza", shaft.cells | {(s[0], s[1]) for s in steps})   # the Obelisk stands on its plaza
    F.obelisk_steps = steps
    RECORDS.append(dict(kind="the plaza", floor=78, cells=plaza.cells))


# ---------------------------------------------------------------------------------------------------------
# the Reactor

def reactor(w, F):
    cx, cz = -56, 48
    shell = Fa.Mass(Fa.poly_cells(P.REACTOR), 66, 96)
    faces = [Fa.slits(3, 6, 26, mat=(95, 0)), Fa.band(4, 4, ORANGE), Fa.band_from_top(3, 3, TEAM),
             Fa.courses(4, Fa.DARK_CONCRETE)]
    Fa.build(w, shell, base=Fa.concrete(), faces=faces, top="parapet", bottom="coffer")
    claim(F, "the Reactor", shell.cells)
    gallery = 80
    for (x, z) in shell.cells:
        d = math.hypot(x - cx, z - cz)
        if d < 7.0:
            for y in range(gallery + 1, 97):
                w.set(x, y, z, B.AIR)
        if d < 3.3:
            for y in range(66, gallery + 1):
                w.set(x, y, z, B.AIR)                     # the shaft, open to the void
        elif d < 7.0:
            w.set(x, gallery, z, *(Fa.SMOOTH if int(d) % 2 else Fa.DARK_CONCRETE))
    # the core, hung over the shaft on four beams
    c0 = gallery + 1
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            for y in range(c0, c0 + 3):
                w.set(x, y, z, *((B.LAVA, 0) if (x, y, z) == (cx, c0 + 1, cz) else (B.OBSIDIAN, 0)))
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for k in range(2, 5):
            w.set(cx + dx * k, gallery, cz + dz * k, *Fa.DARK_CONCRETE)
    F.core = dict(x0=cx - 1, x1=cx + 1, y0=c0, y1=c0 + 2, z0=cz - 1, z1=cz + 1)
    # doors: north (the skyway), east and south
    for (dx, dz) in ((0, -1), (1, 0), (0, 1)):
        for k in range(6, 12):
            for s in (-1, 0, 1):
                x, z = cx + dx * k + (s if dz else 0), cz + dz * k + (s if dx else 0)
                if (x, z) in shell.cells:
                    for y in range(gallery + 1, gallery + 5):
                        w.set(x, y, z, B.AIR)
                    w.set(x, gallery, z, *Fa.SMOOTH)
    RECORDS.append(dict(kind="the Reactor", floor=gallery, cells={c for c in shell.cells if 3.3 <= math.hypot(c[0] - cx, c[1] - cz) < 7}))


# ---------------------------------------------------------------------------------------------------------
# the Columns, the Forum, the Gate, the Lens, the Ziggurat, the Cantilever

def columns(w, F):
    for k, c in enumerate(P.COLUMNS):
        x, z = c["c"]
        h = P.COLUMN_HALF
        m = Fa.Mass(Fa.rect_cells(x - h, z - h, x + h, z + h), 62, c["top"])
        Fa.build(w, m, base=Fa.concrete(), faces=[Fa.flutes(2, 1, 0, 200), Fa.band_from_top(2, 2, ORANGE)], top="cornice")
        steps = wound_stair(w, F, x - h, z - h, x + h, z + h, 68, c["top"], start=3 * k, mat=Fa.SMOOTH)
        claim(F, f"column {k}", m.cells | {(s[0], s[1]) for s in steps})


def forum(w, F):
    x0, z0, x1, z1 = -26, -9, 25, 8
    m = Fa.Mass(Fa.rect_cells(x0, z0, x1, z1), 74, P.FORUM_Y, seam=True)
    Fa.build(w, m, base=Fa.concrete(), faces=[Fa.panels(4, 1, 4, GREY), Fa.band(5, 5, ORANGE)], top=None, bottom="coffer")
    claim(F, "the Forum", {c for c in m.cells if c[0] < 0})
    # the sunken court, its floor a mosaic of glyphs
    cx0, cz0, cx1, cz1 = -10, -4, 9, 3
    for x in range(cx0, 0):
        for z in range(cz0, cz1 + 1):
            for y in (P.FORUM_Y, P.FORUM_Y - 1):
                w.set(x, y, z, B.AIR)
            w.set(x, P.FORUM_Y - 2, z, *Fa.SMOOTH)
    names = ["eye", "sun", "gate", "key"]
    for gi, gx in enumerate((-9, -4)):
        g = Fa.GLYPHS[names[gi]]
        for r in range(5):
            for c in range(5):
                if g[r][c] == "#":
                    w.set(gx + c, P.FORUM_Y - 2, cz0 + 1 + r, *BLACK)
    for x in range(cx0, 0):
        w.set(x, P.FORUM_Y - 1, cz0 - 0, B.STONEBRICK_STAIRS, 2) if False else None
    # steps down into the court at its west end
    for z in range(cz0, cz1 + 1):
        w.set(cx0, P.FORUM_Y - 1, z, B.STONEBRICK_STAIRS, 1)
    # the colonnades: 2 x 2 piers every six along both long edges, an architrave over them
    for zz in ((z0, z0 + 1), (z1 - 1, z1)):
        for x in range(x0, 0):
            if (x - x0) % 6 in (0, 1):
                for z in zz:
                    for y in range(P.FORUM_Y + 1, P.FORUM_Y + 9):
                        w.set(x, y, z, *Fa.concrete()(x, y, z))
        arch = Fa.Mass(Fa.rect_cells(x0, zz[0], x1, zz[1]), P.FORUM_Y + 9, P.FORUM_Y + 12, seam=True)
        Fa.build(w, arch, base=Fa.SMOOTH, faces=[Fa.flutes(2, 1, 1, 2, mat=GREY)], top="parapet-slotted")


def gate(w, F):
    g = P.GATE
    b = g["bar"]
    cells = set()
    for x in range(g["x0"], 0):
        for y in range(g["y0"], g["y1"] + 1):
            inner = (g["x0"] + b <= x <= g["x1"] - b) and (g["y0"] + b <= y <= g["y1"] - b)
            if inner:
                continue
            for z in range(g["z0"], g["z1"] + 1):
                face = z in (g["z0"], g["z1"])
                # on the big faces an inset line runs round the frame a block in from its edges
                ring = (x in (g["x0"] + 1, g["x1"] - 1) and g["y0"] + 1 <= y <= g["y1"] - 1) or \
                       (y in (g["y0"] + 1, g["y1"] - 1) and g["x0"] + 1 <= x) or \
                       (x in (g["x0"] + b - 2,) and g["y0"] + b - 2 <= y <= g["y1"] - b + 2) or \
                       (y in (g["y0"] + b - 2, g["y1"] - b + 2) and x >= g["x0"] + b - 2)
                if face and ring:
                    w.set(x, y, z, B.AIR)
                    w.set(x, y, z + (1 if z == g["z0"] else -1), *ORANGE)
                elif w.id(x, y, z) == B.AIR or not face:
                    w.set(x, y, z, *(Fa.DARK_CONCRETE if y % 4 == 0 else Fa.CONCRETE))
                cells.add((x, z))
    # the foot is a bridge: its top laid smooth
    for x in range(g["x0"], 0):
        for z in range(g["z0"], g["z1"] + 1):
            w.set(x, g["y0"] + b - 1, z, *Fa.SMOOTH)
    claim(F, "the Gate", cells)


def lens(w, F):
    L = P.LENS
    (ox0, oz0), (ox1, _), (_, oz1) = L["outer"][0], L["outer"][1], L["outer"][2]
    (ix0, iz0), (ix1, _), (_, iz1) = L["inner"][0], L["inner"][1], L["inner"][2]
    cells = Fa.rect_cells(ox0, oz0, ox1, oz1) - Fa.rect_cells(ix0, iz0, ix1, iz1)
    m = Fa.Mass(cells, L["y0"], L["y1"], seam=True)
    Fa.build(w, m, base=Fa.concrete(2), faces=[Fa.band(2, 2, ORANGE), Fa.checker(0, 1, GREY)], top="parapet-slotted",
             bottom="coffer")
    claim(F, "the Lens", {c for c in cells if c[0] < 0})


def ziggurat(w, F):
    cx, cz = P.ZIGGURAT["c"]
    allc = set()
    for k, (r, y0, y1) in enumerate(P.ZIGGURAT["tiers"]):
        m = Fa.Mass(Fa.rect_cells(cx - r, cz - r, cx + r, cz + r), y0, y1)
        Fa.build(w, m, base=Fa.concrete(), faces=[Fa.band(1, 1, ORANGE if k % 2 == 0 else GREY), Fa.flutes(2, 1, 2, 3)],
                 bottom="coffer" if k == 0 else None)
        allc |= m.cells
    # a straight flight up the east face, tier to tier
    tiers = P.ZIGGURAT["tiers"]
    for k in range(len(tiers) - 1):
        r, y0, y1 = tiers[k]
        r2 = tiers[k + 1][0]
        for step in range(1, 5):
            x = cx + r - (step - 1)
            for z in (cz - 1, cz, cz + 1):
                y = y1 + step
                if x > cx + r2:
                    w.set(x, y, z, B.STONEBRICK_STAIRS, 1)
                    for yy in range(y1 + 1, y):
                        w.set(x, yy, z, *Fa.CONCRETE)
    claim(F, "the Ziggurat", allc)


def cantilever(w, F):
    C = P.CANTILEVER
    (x0, z0), (x1, _), (_, z1) = C["core"][0], C["core"][1], C["core"][2]
    core = Fa.Mass(Fa.rect_cells(x0, z0, x1, z1), *C["core_y"])
    Fa.build(w, core, base=Fa.concrete(), faces=[Fa.panels(3, 2, 22, GREY), Fa.band_from_top(1, 1, ORANGE),
                                                  Fa.glyph_row(14, ["sun", "eye", "key"], BLACK, spacing=6)],
             top="cornice", bottom="coffer")
    (ax0, az0), (ax1, _), (_, az1) = C["arm"][0], C["arm"][1], C["arm"][2]
    arm = Fa.Mass(Fa.rect_cells(ax0, az0, ax1, az1), *C["arm_y"])
    Fa.build(w, arm, base=Fa.concrete(2), faces=[Fa.band(2, 2, ORANGE), Fa.slits(2, 1, 3, mat=GREY)],
             top="parapet-slotted", bottom="coffer")
    # a stair up the core's west face from its foot to its head
    steps = wound_stair(w, F, x0, z0, x1, z1, 68, C["core_y"][1], start=20, mat=Fa.SMOOTH)
    claim(F, "the Cantilever", core.cells | arm.cells | {(s[0], s[1]) for s in steps})


def build(w, F):
    F.occ, F.conflicts = {}, []
    RECORDS.clear()
    atrium(w, F)
    obelisk(w, F)
    reactor(w, F)
    columns(w, F)
    forum(w, F)
    gate(w, F)
    lens(w, F)
    ziggurat(w, F)
    cantilever(w, F)
    for s in P.SKYWAYS:
        skyway(w, F, s)
    F.records = RECORDS
    print(f"  {len(F.conflicts)} conflicts: {F.conflicts[:6]}")
