"""Crucible's foundry inside red's mountain: every space and ramp carved, each lined by its style, and the two
facades built across the cliff's foot.

The styles give each room its identity:

    hall      the loading hall: pilasters of smooth double slab stepped out a block every five, panels of nether brick
              sunk a block between them, an orange band sunk under the cornice, iron beams across the ceiling
    crew      the crew hall (spawn): dark oak posts and beams, panels of the team's clay sunk between the posts,
              a dark oak floor with the team's runner
    pour      the pour room and its loggia: iron pilasters, a smooth deck floor, the monument on its desk
    furnace   the furnace hall: a row of furnaces in sunk bays along its back wall, iron pilasters, a hopper line
    store     the cold store: prismarine walls between dark prismarine pilasters, sea lanterns sunk in panels,
              a quartz floor with a water channel round the wool's plinth
    run, tunnel, gate, door   cut rock with stone-brick ribs every five blocks, a paved floor

    bunker.build(w) -> the mask of every space's air, world indexed
"""
import numpy as np

import land
import palette as P
import plan as PL
from pgmvox import B

STONEBRICK = (B.STONEBRICK, 0)
CHISELED = (B.STONEBRICK, 3)
POL_ANDESITE = (B.STONE, 6)
SMOOTH = (B.DSLAB, 0)
NETHER = (B.NETHER_BRICK, 0)
ORANGE = (B.STAINED_CLAY, 1)
IRON = (B.IRON_BLOCK, 0)
TEAM_CLAY = (B.STAINED_CLAY, 14)
DARK_OAK_LOG = (B.LOG2, 1)
DARK_OAK = (B.PLANKS, 5)
PRISMARINE_BRICK = (B.PRISMARINE, 1)
DARK_PRISMARINE = (B.PRISMARINE, 2)
QUARTZ = (B.QUARTZ, 0)
QUARTZ_PILLAR = (B.QUARTZ, 2)
LANTERN = (B.SEA_LANTERN, 0)
GLOW = (B.GLOWSTONE, 0)


def _set(w, x, y, z, b):
    w.set(x, y, z, b[0], b[1])


class Carver:
    def __init__(self, w):
        self.w = w
        self.air = np.zeros(w.ids.shape, bool)

    def mark(self, x, y, z):
        if self.w.inside(x, y, z):
            self.air[x - self.w.x0, y, z - self.w.z0] = True

    def is_air(self, x, y, z):
        return self.w.inside(x, y, z) and self.air[x - self.w.x0, y, z - self.w.z0]

    def carve_box(self, x0, x1, y0, y1, z0, z1):
        self.w.fill(x0, y0, z0, x1, y1, z1, B.AIR)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(y0, y1 + 1):
                    self.mark(x, y, z)


def solid(w, x, y, z):
    return w.id(x, y, z) not in (B.AIR, B.WATER, B.LAVA)


# --- the spaces ------------------------------------------------------------------------------------------------
def carve(C):
    for s in PL.SPACES:
        C.carve_box(s.x0, s.x1, s.feet, s.feet + s.h - 1, s.z0, s.z1)
    for r in PL.RAMPS:
        for x, z, f in r.cells():
            lo = int(np.floor(f)) + (1 if f % 1 else 0)
            C.carve_box(x, x, lo, int(np.floor(f)) + r.h, z, z)


def ramp_floors(w, C):
    """Each ramp cell's tread: a full block where the feet stand on a whole block, a bottom slab where they stand a
    half block up; stone brick, the landings in the deck's smooth slab."""
    for r in PL.RAMPS:
        for leg in r.legs:
            level = leg.feet0 == leg.feet1
            for x, z, f in leg.cells():
                if f % 1:
                    n = int(np.floor(f))
                    w.set(x, n, z, B.SLAB, 5)
                    _set(w, x, n - 1, z, STONEBRICK)
                else:
                    _set(w, x, int(f) - 1, z, SMOOTH if level else STONEBRICK)
    for x, z0, z1 in PL.RAMP_WALLS:                    # the wall between the loading ramp's legs, over the slag run
        for z in range(z0, z1 + 1):
            for y in range(PL.L1 + PL.TUNNEL_H, PL.L0 + 6):
                if not C.is_air(x, y, z) or y >= 45:
                    _set(w, x, y, z, STONEBRICK)
                    C.air[x - w.x0, y, z - w.z0] = False
    # the furnace ramp's lower leg runs open along the hall: a parapet where it stands two over the hall's floor
    leg = PL.RAMPS[1].legs[2]
    for x, z, f in leg.cells():
        if x == leg.x0 and f - PL.L1 >= 2:
            n = int(np.floor(f))
            if f % 1:
                _set(w, x, n, z, STONEBRICK)
                w.set(x, n + 1, z, B.SLAB, 5)
            else:
                _set(w, x, n, z, STONEBRICK)
            C.air[x - w.x0, n:n + 2, z - w.z0] = False


# --- lining a box room by its walls ----------------------------------------------------------------------------
def sides(s):
    """The four walls of a space: (cells along the wall as (x, z), the outward step (dx, dz))."""
    return [([(x, s.z0) for x in range(s.x0, s.x1 + 1)], (0, -1)),
            ([(x, s.z1) for x in range(s.x0, s.x1 + 1)], (0, 1)),
            ([(s.x0, z) for z in range(s.z0, s.z1 + 1)], (-1, 0)),
            ([(s.x1, z) for z in range(s.z0, s.z1 + 1)], (1, 0))]


def wall_whole(w, C, x, z, d, y0, y1):
    """True where the wall behind (x, z) in direction d is rock (not another space) for every course y0..y1."""
    return all(solid(w, x + d[0], y, z + d[1]) and not C.is_air(x + d[0], y, z + d[1]) for y in range(y0, y1 + 1))


def line(w, C, s, wall, floor, ceiling, period=5, pilaster=None, panel=None, band=None, base=None, recess=True):
    """Line a space: the floor (a function of x, z), the ceiling, and every wall course by course. A pilaster stands
    a block into the room every `period`, from floor to ceiling, where the wall behind it is whole; between them a
    panel is sunk a block from the second course to four under the ceiling, and a band sunk at three under."""
    top = s.feet + s.h - 1
    for x, z in s.cells():
        if not C.is_air(x, s.feet - 1, z):
            b = floor(x, z)
            if b:
                _set(w, x, s.feet - 1, z, b)
        if ceiling and not C.is_air(x, top + 1, z):
            b = ceiling(x, z)
            if b:
                _set(w, x, top + 1, z, b)
    for cells, d in sides(s):
        n = len(cells)
        for k, (x, z) in enumerate(cells):
            wx, wz = x + d[0], z + d[1]
            corner = k == 0 or k == n - 1
            whole = wall_whole(w, C, x, z, d, s.feet, top)
            for y in range(s.feet, top + 1):
                if C.is_air(wx, y, wz) or not solid(w, wx, y, wz):
                    continue
                t = y - s.feet
                _set(w, wx, y, wz, wall(x, y, z, t, k))
                if base and t == 0:
                    _set(w, wx, y, wz, base)
            m = k % period
            bx, bz = wx + d[0], wz + d[1]
            if pilaster and whole and n > 6 and m == 0 and not corner and s.h > 4:
                for y in range(s.feet, top + 1):
                    _set(w, x, y, z, pilaster(y - s.feet))
                    C.air[x - w.x0, y, z - w.z0] = False
                continue
            if not recess or not whole or corner or n <= 6:
                continue
            if panel and 2 <= m <= period - 2 and s.h > 5:
                for y in range(s.feet + 1, top - 3):
                    if solid(w, bx, y, bz) and not C.is_air(bx, y, bz):
                        w.set(wx, y, wz, B.AIR)
                        _set(w, bx, y, bz, panel(x, y, z, y - s.feet))
            if band and s.h > 5:
                y = top - 2
                if solid(w, bx, y, bz) and not C.is_air(bx, y, bz):
                    w.set(wx, y, wz, B.AIR)
                    _set(w, bx, y, bz, band)


def floor_set(name, seed=0):
    def f(x, z):
        u = P.cells(np.array([x]), np.array([z]), 2, seed)[0]
        i, d = P.pick(name, np.array([u]))
        return (int(i[0]), int(d[0]))
    return f


def lining(w, C):
    floor = floor_set("floor", 3)
    deck = floor_set("deck", 5)
    haul = floor_set("haul", 7)

    def plain_wall(x, y, z, t, k):
        return POL_ANDESITE if t == 0 else STONEBRICK

    def hall_ceiling(x, z):
        return IRON if (x - PL.SPACES[1].x0) % 5 == 2 else (GLOW if (z % 4 == 0 and x % 5 == 0) else SMOOTH)

    for s in PL.SPACES:
        if s.style == "hall":
            line(w, C, s, plain_wall, floor, hall_ceiling, pilaster=lambda t: CHISELED if t == s.h - 1 else SMOOTH,
                 panel=lambda x, y, z, t: NETHER, band=ORANGE, base=POL_ANDESITE)
        elif s.style == "crew":
            def crew_floor(x, z):
                return (B.CARPET, 14) if False else DARK_OAK
            line(w, C, s, lambda x, y, z, t, k: POL_ANDESITE if t in (0, s.h - 1) else STONEBRICK, crew_floor,
                 lambda x, z: DARK_OAK_LOG if (z - s.z0) % 4 == 0 else (GLOW if (x % 4 == 0 and z % 4 == 2) else DARK_OAK),
                 period=4, pilaster=lambda t: DARK_OAK_LOG, panel=lambda x, y, z, t: TEAM_CLAY, band=None,
                 base=POL_ANDESITE)
        elif s.style in ("pour", "loggia"):
            line(w, C, s, plain_wall, deck, lambda x, z: GLOW if (x % 4 == 0 and z % 3 == 0) else SMOOTH,
                 pilaster=lambda t: IRON, panel=lambda x, y, z, t: NETHER, band=ORANGE, base=POL_ANDESITE)
        elif s.style == "furnace":
            def furnace_panel(x, y, z, t):
                return (B.FURNACE + 1, 2) if t == 1 else NETHER
            line(w, C, s, plain_wall, floor, lambda x, z: IRON if (x - s.x0) % 5 == 2 else
                 (GLOW if z % 4 == 1 and x % 5 == 0 else SMOOTH), pilaster=lambda t: IRON,
                 panel=lambda x, y, z, t: NETHER, band=ORANGE, base=POL_ANDESITE)
        elif s.style == "store":
            line(w, C, s, lambda x, y, z, t, k: QUARTZ if t == 0 else PRISMARINE_BRICK,
                 lambda x, z: QUARTZ, lambda x, z: LANTERN if (x % 4 == 0 and z % 4 == 0) else QUARTZ,
                 period=4, pilaster=lambda t: DARK_PRISMARINE, panel=lambda x, y, z, t: LANTERN if t == 3 else
                 DARK_PRISMARINE, band=None, base=QUARTZ)
        else:                                            # tunnels: cut rock, a paved floor, ribs every five
            for x, z in s.cells():
                if not C.is_air(x, s.feet - 1, z):
                    _set(w, x, s.feet - 1, z, haul(x, z))
    ribs(w, C)
    furnaces(w, C)
    store(w, C)
    crew(w, C)
    pour(w, C)


def ribs(w, C):
    """A stone-brick rib every five blocks along each tunnel and ramp: the walls' course and the ceiling's."""
    for s in PL.SPACES:
        if s.style not in ("tunnel", "run"):
            continue
        along_x = (s.x1 - s.x0) >= (s.z1 - s.z0)
        top = s.feet + s.h
        if along_x:
            for x in range(s.x0, s.x1 + 1):
                if (x - s.x0) % 5 != 2:
                    continue
                for z in (s.z0 - 1, s.z1 + 1):
                    for y in range(s.feet, top):
                        if not C.is_air(x, y, z) and solid(w, x, y, z):
                            _set(w, x, y, z, STONEBRICK if y > s.feet else POL_ANDESITE)
                for z in range(s.z0 - 1, s.z1 + 2):
                    if not C.is_air(x, top, z):
                        _set(w, x, top, z, STONEBRICK)
        else:
            for z in range(s.z0, s.z1 + 1):
                if (z - s.z0) % 5 != 2:
                    continue
                for x in (s.x0 - 1, s.x1 + 1):
                    for y in range(s.feet, top):
                        if not C.is_air(x, y, z) and solid(w, x, y, z):
                            _set(w, x, y, z, STONEBRICK if y > s.feet else POL_ANDESITE)
                for x in range(s.x0 - 1, s.x1 + 2):
                    if not C.is_air(x, top, z):
                        _set(w, x, top, z, STONEBRICK)
    # the ramps: walls of stone brick on every block beside their air
    for r in PL.RAMPS:
        for x, z, f in r.cells():
            lo, hi = int(np.floor(f)), int(np.floor(f)) + r.h
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                for y in range(lo, hi + 1):
                    if not C.is_air(x + dx, y, z + dz) and solid(w, x + dx, y, z + dz):
                        _set(w, x + dx, y, z + dz, STONEBRICK if (x + z) % 5 else POL_ANDESITE)
            if not C.is_air(x, hi + 1, z):
                _set(w, x, hi + 1, z, SMOOTH)


def furnaces(w, C):
    """The furnace hall's back wall: a lit furnace in every sunk bay, at the course over the base."""
    s = next(s for s in PL.SPACES if s.name == "furnace hall")
    z = s.z1 + 2                                        # the bay's back, behind the sunk panel
    for x in range(s.x0 + 1, s.x1):
        if w.id(x, s.feet + 1, s.z1 + 1) == B.AIR and w.id(x, s.feet + 1, z) == B.NETHER_BRICK:
            w.set(x, s.feet + 1, z, B.FURNACE + 1, 2)
    # the casting line: cauldrons on a plinth along the front, between the doors
    for x in range(s.x0 + 2, s.x1 - 1, 3):
        if C.is_air(x, s.feet, s.z0 + 2) and all(abs(x - c) > 2 for c in (16, 24)):
            w.set(x, s.feet, s.z0 + 2, B.CAULDRON, 3)


def store(w, C):
    """The cold store's plinth and its water channel: a ring of water round a quartz plinth, prismarine under it."""
    s = PL.STORE
    cx, cy, cz = PL.WOOL_AT
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            r = max(abs(x - cx), abs(z - cz))
            if r == 3:
                w.set(x, s.feet - 1, z, B.WATER)
                w.set(x, s.feet - 2, z, B.PRISMARINE, 0)
            elif r == 2:
                w.set(x, s.feet - 1, z, B.PRISMARINE, 2)
    w.set(cx, s.feet, cz, B.QUARTZ, 1)                  # the plinth, the wool on it
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        w.set(cx + dx, s.feet, cz + dz, B.QUARTZ_STAIRS, {(1, 0): 1, (-1, 0): 0, (0, 1): 3, (0, -1): 2}[(dx, dz)])
    for x, z in ((cx - 1, cz - 1), (cx + 1, cz - 1), (cx - 1, cz + 1), (cx + 1, cz + 1)):
        w.set(x, s.feet, z, B.SLAB, 7)
    # bridges over the channel on the four sides
    for dx, dz in ((3, 0), (-3, 0), (0, 3), (0, -3)):
        w.set(cx + dx, s.feet - 1, cz + dz, B.QUARTZ, 0)


def pour(w, C):
    """The pour room: the monument on a pedestal of quartz stairs at its middle, and the control desk along its back
    wall, polished andesite topped with levers, an iron block at each end."""
    s = next(s for s in PL.SPACES if s.name == "pour room")
    mx, my, mz = PL.MONUMENT
    for (dx, dz), d in (((1, 0), 1), ((-1, 0), 0), ((0, 1), 3), ((0, -1), 2)):
        w.set(mx + dx, s.feet, mz + dz, B.QUARTZ_STAIRS, d)
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        w.set(mx + dx, s.feet, mz + dz, B.SLAB, 7)
    z = s.z1
    for x in range(s.x0 + 3, s.x1 - 2):
        if abs(x - mx) <= 2:
            continue
        end = x in (s.x0 + 3, s.x1 - 3) or abs(x - mx) == 3
        _set(w, x, s.feet, z, IRON if end else POL_ANDESITE)
        if not end and x % 2 == 0:
            w.set(x, s.feet + 1, z, B.LEVER, 5)


def crew(w, C):
    """The crew hall: the team's runner down its middle, benches along its walls."""
    s = next(s for s in PL.SPACES if s.name == "crew hall")
    for z in range(s.z0 + 1, s.z1):
        for x in (-1, 0):
            w.set(x, s.feet, z, B.CARPET, 14)
    for z in range(s.z0 + 2, s.z1 - 1):
        if z % 4 in (1, 2):
            for x, d in ((s.x0 + 1, 0), (s.x1 - 1, 1)):
                if C.is_air(x, s.feet, z):
                    w.set(x, s.feet, z, B.DARK_OAK_STAIRS, d)


# --- the facades ------------------------------------------------------------------------------------------------
def facade(w, C, f, ground, openings, windows=()):
    """A facade across the cliff's foot: a mass from the ground to `top` over z0..z1, its face at z0 facing the
    plain. Pilasters of smooth slab stand a block out every five, panels of nether brick are sunk a block between
    them, an orange band is sunk under the cornice, and the cornice steps out on upside-down stairs. `openings`
    are (x0, x1, y0, y1) cut through the mass; `windows` are (x0, x1, y0, y1) of the team's glass in the panels."""
    x0, x1, z0, z1, top = f["x0"], f["x1"], f["z0"], f["z1"], f["top"]
    for x in range(x0, x1 + 1):
        g = ground[x]
        for z in range(z0, z1 + 1):
            for y in range(g, top + 1):
                if not C.is_air(x, y, z):
                    _set(w, x, y, z, STONEBRICK if (y - g) % 6 else POL_ANDESITE)
        for y in range(top + 1, top + 4):                  # nothing of the cliff hangs over the cornice's front
            if w.id(x, y, z0) != B.AIR and y <= top + 1:
                _set(w, x, y, z0, STONEBRICK)
        k = x - x0
        pil = k % 5 == 0 or x == x1
        for y in range(g, top + 1):
            if any(a <= x <= b and c <= y <= d for a, b, c, d in openings):
                continue
            if pil:
                if y < top - 1:
                    _set(w, x, y, z0 - 1, SMOOTH if y > g else POL_ANDESITE)
                elif y == top - 1:
                    _set(w, x, y, z0 - 1, CHISELED)
            elif y == top - 3:
                w.set(x, y, z0, B.AIR)
                _set(w, x, y, z0 + 1, ORANGE)
            elif g + 2 <= y <= top - 5 and k % 5 in (2, 3) or (g + 2 <= y <= top - 5 and k % 5 in (1, 4)
                                                                and x1 - x0 > 8):
                if not any(a - 1 <= x <= b + 1 and c - 1 <= y <= d + 1 for a, b, c, d in openings):
                    win = any(a <= x <= b and c <= y <= d for a, b, c, d in windows)
                    w.set(x, y, z0, B.AIR)
                    if win:
                        w.set(x, y, z0 + 1, B.STAINED_GLASS, 14)
                    else:
                        _set(w, x, y, z0 + 1, NETHER)
        # the cornice: a course stepped out on upside-down stairs, the top course over it
        if not pil:
            w.set(x, top, z0 - 1, B.STONEBRICK_STAIRS, 6)
        _set(w, x, top + 1, z0, STONEBRICK)
        w.set(x, top + 1, z0 - 1, B.SLAB, 5) if pil else None
    for a, b, c, d in openings:
        for x in range(a, b + 1):
            for y in range(c, d + 1):
                for z in range(z0 - 1, z1 + 1):
                    if w.id(x, y, z) not in (B.AIR,):
                        w.set(x, y, z, B.AIR)
                        C.mark(x, y, z)
        for x in range(a - 1, b + 2):                       # an iron lintel over each opening, its jambs of smooth slab
            _set(w, x, d + 1, z0 - 1, IRON)
            _set(w, x, d + 1, z0, IRON)
        for y in range(c, d + 1):
            for x in (a - 1, b + 1):
                _set(w, x, y, z0 - 1, SMOOTH)


def ground_line(w, f):
    """The lowest top in front of a facade, column by column."""
    out = {}
    for x in range(f["x0"] - 1, f["x1"] + 2):
        tops = [w.top(x, z) for z in (f["z0"] - 2, f["z0"] - 1)]
        out[x] = min(t for t in tops if t >= 0) + 1 if any(t >= 0 for t in tops) else PL.L0
    return out


def facades(w, C):
    gate = next(s for s in PL.SPACES if s.name == "loading gate")
    fg = PL.FACADE_GATE
    gl = ground_line(w, fg)
    facade(w, C, fg, gl, [(gate.x0, gate.x1, gate.feet, gate.feet + gate.h - 1)],
           windows=[(fg["x0"], fg["x1"], 57, 60)])
    fp = PL.FACADE_PIT
    gp = ground_line(w, fp)
    lg = next(s for s in PL.SPACES if s.name == "loggia")
    doors = [s for s in PL.SPACES if s.name.endswith("pit door")]
    facade(w, C, fp, gp, [(lg.x0, lg.x1, lg.feet, lg.feet + lg.h - 1)] +
           [(d.x0, d.x1, d.feet, d.feet + d.h - 1) for d in doors])
    # the loggia's arcade: piers every four along its open front, a parapet a block high between them, the floor
    # carried out to the face
    for x in range(lg.x0, lg.x1 + 1):
        _set(w, x, lg.feet - 1, fp["z0"] - 1, SMOOTH)
        if (x - lg.x0) % 4 == 0:
            for y in range(lg.feet, lg.feet + lg.h):
                _set(w, x, y, fp["z0"] - 1, SMOOTH)
                C.air[x - w.x0, y, fp["z0"] - 1 - w.z0] = False
        else:
            w.set(x, lg.feet, fp["z0"] - 1, B.STONEBRICK_STAIRS, 3)
    # the lower front over the apron: the band of the furnace doors, rusticated in polished andesite courses
    for x in range(fp["x0"], fp["x1"] + 1):
        for y in range(gp[x], lg.feet - 1):
            if not C.is_air(x, y, fp["z0"]) and w.id(x, y, fp["z0"]) != B.AIR and (y - gp[x]) % 2 == 0:
                _set(w, x, y, fp["z0"], POL_ANDESITE)


def build(w):
    C = Carver(w)
    carve(C)
    lining(w, C)
    ramp_floors(w, C)
    facades(w, C)
    return C
