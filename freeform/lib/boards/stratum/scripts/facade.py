"""Brutalist masses with patterned faces.

A mass is a set of (x, z) cells extruded from y0 to y1. Its faces are the cells on its edge with exactly one
side open to the air; a cell open on two sides is a corner and is always left flush, so every edge stays a
crisp line. Each face cell, at each height, is put to a list of patterns in order. The first that has
something to say decides it:

  ("inset", material)  the face steps back one block here: this block becomes air and the one behind it
                       takes the material, so a band, a flute or a glyph is a recess, not a paint;
  ("accent", material) the face stays flush but in another material;
  None                 the next pattern is asked; if none answers, the face is the mass's concrete.

A pattern is given where the block falls on its face: `s` along the face (blocks from the run's start),
`run` the run's length, `t` up the face from y0, `h` the face's height. So a pattern is a function of the
face, not of the world, and the same pattern laid on a long wall and a short one comes out right on both.

Tops take a cornice or a parapet; undersides of floating masses are coffered: a grid of recesses with a
sea lantern in each.

The board is mirrored across x = -0.5, and a mass may cross it: a cell at x >= 0 counts as part of the mass
when its mirror image is, so the seam is never mistaken for a face.
"""
import numpy as np

from mc import B

SEA_LANTERN = 169
PRISMARINE = 168
CLAY = B.STAINED_CLAY
SMOOTH = (B.DSLAB, 8)                 # the seamless double stone slab
CONCRETE = (B.STONE, 0)
DARK_CONCRETE = (B.STONE, 6)          # polished andesite
GLYPHS = {
    "eye": [".###.", "#...#", "#.#.#", "#...#", ".###."],
    "step": ["#....", "##...", "###..", "####.", "#####"],
    "bars": ["#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#"],
    "cross": ["..#..", "..#..", "#####", "..#..", "..#.."],
    "key": ["#####", "#....", "#.###", "#.#.#", "###.#"],
    "chevron": ["..#..", ".#.#.", "#...#", "..#..", ".#.#."],
    "gate": ["#####", "#...#", "#.#.#", "#.#.#", "#.#.#"],
    "sun": ["#.#.#", ".###.", "##.##", ".###.", "#.#.#"],
}


# ---------------------------------------------------------------------------------------------------------
# patterns: each returns a function (s, run, t, h, rng) -> action or None

def band(t0, t1, mat, inset=True):
    return lambda s, run, t, h, n: (("inset" if inset else "accent"), mat) if t0 <= t <= t1 else None


def band_from_top(d0, d1, mat, inset=True):
    return lambda s, run, t, h, n: (("inset" if inset else "accent"), mat) if d0 <= h - t <= d1 else None


def courses(every, mat, offset=0):
    """Lift lines: a course of another concrete every so many, flush, as poured concrete shows its pours."""
    return lambda s, run, t, h, n: ("accent", mat) if (t + offset) % every == 0 and 0 < t < h else None


def flutes(period, width, t0, t1, mat=None, phase=0):
    """Vertical grooves: `width` of every `period` blocks set back."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= min(t1, h)):
            return None
        if 0 < s < run - 1 and (s + phase) % period < width:
            return ("inset", mat or DARK_CONCRETE)
        return None
    return f


def panels(period, t0, t1, mat=None):
    """Whole panels alternately flush and set back, the run divided evenly about its middle."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= min(t1, h)) or s == 0 or s == run - 1:
            return None
        k = (s - (run % period) // 2) // period
        return ("inset", mat or DARK_CONCRETE) if k % 2 == 1 else None
    return f


def glyph_row(t0, names, mat, spacing=8, min_run=7):
    """A row of five-by-five glyphs inlaid along the face, centred on the run, each set back and dark."""
    def f(s, run, t, h, n):
        if run < min_run or not (t0 <= t < t0 + 5):
            return None
        count = max(1, (run - 1) // spacing)
        start = (run - (count * spacing - (spacing - 5))) // 2
        k, off = divmod(s - start, spacing)
        if s < start or k >= count or off >= 5:
            return None
        g = GLYPHS[names[(k + n) % len(names)]]
        return ("inset", mat) if g[4 - (t - t0)][off] == "#" else None
    return f


def slits(period, t0, t1, mat=(95, 15), phase=None):
    def f(s, run, t, h, n):
        if not (t0 <= t <= t1) or s < 2 or s > run - 3:
            return None
        p = period // 2 if phase is None else phase
        return ("accent", mat) if (s - (run % period) // 2) % period == p else None
    return f


def checker(t0, t1, mat, size=2):
    """A field of inset squares in a checker: a pattern for a large blank face."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= t1) or s == 0 or s == run - 1:
            return None
        return ("inset", mat) if ((s // size) + (t // size)) % 2 == 0 else None
    return f


# ---------------------------------------------------------------------------------------------------------
# the mass

class Mass:
    def __init__(self, cells, y0, y1, seam=False):
        self.cells = set(cells)
        self.y0, self.y1 = y0, y1
        self.seam = seam

    def has(self, x, z):
        if self.seam and x >= 0:
            return (-1 - x, z) in self.cells
        return (x, z) in self.cells

    def faces(self):
        """Face runs: lists of cells along a straight edge with the same outward normal, in order."""
        by_key = {}
        corners = set()
        for (x, z) in self.cells:
            if x >= 0:
                continue
            opens = [(dx, dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not self.has(x + dx, z + dz)]
            if len(opens) == 1:
                dx, dz = opens[0]
                line = x if dx else z                     # the face's plane
                along = z if dx else x
                by_key.setdefault((dx, dz, line), []).append(along)
            elif len(opens) >= 2:
                corners.add((x, z))
        runs = []
        for (dx, dz, line), alongs in by_key.items():
            alongs.sort()
            cur = [alongs[0]]
            for a in alongs[1:]:
                if a == cur[-1] + 1:
                    cur.append(a)
                else:
                    runs.append((dx, dz, line, cur))
                    cur = [a]
            runs.append((dx, dz, line, cur))
        return runs, corners


def build(w, mass, base=CONCRETE, faces=(), top=None, bottom=None, rng=None, fill=True, seed=0):
    """Pour the mass and pattern it. base is a block or a function (x, y, z) -> block."""
    rng = rng or np.random.default_rng(seed)
    y0, y1 = mass.y0, mass.y1
    H = y1 - y0
    get = base if callable(base) else (lambda x, y, z: base)
    if fill:
        for (x, z) in mass.cells:
            if x >= 0:
                continue
            for y in range(y0, y1 + 1):
                w.set(x, y, z, *get(x, y, z))
    runs, corners = mass.faces()
    for n_run, (dx, dz, line, alongs) in enumerate(runs):
        # walk the run so that s grows the same way on every face seen from outside
        order = alongs if (dx == 1 or dz == -1) else alongs[::-1]
        if dx != 0:
            order = alongs if dx == 1 else alongs[::-1]
        run = len(order)
        for s, a in enumerate(order):
            x, z = (line, a) if dx else (a, line)
            for t in range(0, H + 1):
                y = y0 + t
                act = None
                for p in faces:
                    act = p(s, run, t, H, n_run)
                    if act:
                        break
                if not act:
                    continue
                kind, mat = act
                if kind == "accent":
                    w.set(x, y, z, *mat)
                elif kind == "inset" and mass.has(x - dx, z - dz):
                    w.set(x, y, z, B.AIR)
                    w.set(x - dx, y, z - dz, *mat)
    if top:
        top_course(w, mass, top, get)
    if bottom == "coffer":
        coffer(w, mass)
    return runs


def top_course(w, mass, kind, get):
    y = mass.y1
    edge = [(x, z) for (x, z) in mass.cells if x < 0 and
            any(not mass.has(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    if kind == "cornice":
        # a course thrown out a block all round, a slab's thickness
        for (x, z) in edge:
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                X, Z = x + dx, z + dz
                if X < 0 and not mass.has(X, Z):
                    w.set(X, y, Z, B.SLAB, 8)
    elif kind == "parapet":
        for (x, z) in edge:
            w.set(x, y + 1, z, *SMOOTH)
    elif kind == "parapet-slotted":
        for (x, z) in edge:
            if (x + z) % 3:
                w.set(x, y + 1, z, *SMOOTH)


def coffer(w, mass):
    """The underside cut into recesses on a grid of four, two by two each, a sea lantern at the heart of every
    other one; a rim of two blocks left whole."""
    y = mass.y0
    for (x, z) in mass.cells:
        if x >= 0:
            continue
        rim = any(not mass.has(x + dx, z + dz) for dx in (-2, -1, 0, 1, 2) for dz in (-2, -1, 0, 1, 2))
        if rim:
            continue
        if (x % 4) in (1, 2) and (z % 4) in (1, 2):
            w.set(x, y, z, B.AIR)
            light = (x % 4 == 1 and z % 4 == 1 and ((x // 4) + (z // 4)) % 2 == 0)
            w.set(x, y + 1, z, *((SEA_LANTERN, 0) if light else (CLAY, 8)))


# ---------------------------------------------------------------------------------------------------------
# shapes

def rect_cells(x0, z0, x1, z1):
    return {(x, z) for x in range(min(x0, x1), max(x0, x1) + 1) for z in range(min(z0, z1), max(z0, z1) + 1)}


def poly_cells(poly):
    import geometry as G
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    x0, x1 = int(np.floor(min(xs))) - 1, int(np.ceil(max(xs))) + 1
    z0, z1 = int(np.floor(min(zs))) - 1, int(np.ceil(max(zs))) + 1
    X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    m = G.inside(X + 0.0, Z + 0.0, poly)
    return {(x0 + i, z0 + k) for i, k in zip(*np.nonzero(m))}


def concrete(every=4):
    """Board-formed concrete: stone with a course of polished andesite every `every`, as pours show."""
    def f(x, y, z):
        return DARK_CONCRETE if y % every == 0 else CONCRETE
    return f
