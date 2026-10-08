"""Faces and floors with a pattern on them: insets, flutes, glyphs and words on a wall; borders, medallions and
diamonds on a floor.

**A face pattern is a function of where a block falls on its face**, not of the world:

    pattern(s, run, t, h, n) -> None | ("inset", block) | ("accent", block)

`s` counts blocks along the face from its left end as seen from outside, `run` is the face's length, `t` counts
up from the bottom course, `h` is the top course's t, and `n` numbers the face. "inset" sets the face back a
block, so the band or glyph is a recess and not a paint; "accent" keeps it flush in another block. The first
pattern in a list that answers decides a block, so a list reads as an order of precedence:

    extrude(w, cells, 40, 60, base=concrete(4), faces=[
        glyph_row(12, ["eye", "key"], DARK), word(4, "NORTH", DARK), flutes(4, 1, 2, 9), courses(5, DARK)],
        top="parapet", bottom="coffer")

The same pattern on a long wall and a short one comes out right on both. A corner, a cell open on two sides,
is always left flush so the mass's edges stay crisp. Faces are found along x and z; a mass at a heading is a
`build.Frame` shape and its faces are not patterned.

**A floor field is a function of where a cell falls in its rectangle:** `field(c) -> block or None`, where `c`
carries x, z, the offsets u, v from the middle, the half sizes hw, hh, and `edge`, the blocks to the nearest
side. `first_of` composes them, and `carpet` lays one.
"""
from dataclasses import dataclass

import numpy as np

from .blocks import B

CONCRETE = (B.STONE, 0)
DARK = (B.STONE, 6)                     # polished andesite
SMOOTH = (B.DSLAB, 8)                   # the seamless double stone slab

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

# three wide and five high, top row first
LETTERS = {
    "A": ["###", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": ["###", "#..", "#..", "#..", "###"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
    "G": ["###", "#..", "#.#", "#.#", "###"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", "###"],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"], "N": ["##.", "#.#", "#.#", "#.#", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"], "P": ["###", "#.#", "###", "#..", "#.."],
    "Q": ["###", "#.#", "#.#", "###", "..#"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": ["###", "#..", "###", "..#", "###"], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "W": ["#.#", "#.#", "###", "###", "#.#"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."], "Z": ["###", "..#", ".#.", "#..", "###"],
    "0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", ".##", "..#", "###"],
    "4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
    "6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", ".#.", ".#.", ".#."],
    "8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
    " ": ["...", "...", "...", "...", "..."], "-": ["...", "...", "###", "...", "..."],
}


# ---- face patterns ---------------------------------------------------------------------------------------
def band(t0, t1, block, inset=True):
    """A horizontal band from course t0 to t1."""
    return lambda s, run, t, h, n: (("inset" if inset else "accent"), block) if t0 <= t <= t1 else None


def band_from_top(d0, d1, block, inset=True):
    return lambda s, run, t, h, n: (("inset" if inset else "accent"), block) if d0 <= h - t <= d1 else None


def courses(every, block, offset=0):
    """A flush course of another block every so many, as poured concrete shows its pours."""
    return lambda s, run, t, h, n: ("accent", block) if (t + offset) % every == 0 and 0 < t < h else None


def flutes(period, width, t0, t1, block=DARK, phase=0):
    """Vertical grooves: `width` of every `period` blocks set back, clear of the face's ends."""
    def f(s, run, t, h, n):
        if t0 <= t <= min(t1, h) and 0 < s < run - 1 and (s + phase) % period < width:
            return ("inset", block)
        return None
    return f


def panels(period, t0, t1, block=DARK):
    """Whole panels alternately flush and set back, the run divided evenly about its middle."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= min(t1, h)) or s == 0 or s == run - 1:
            return None
        return ("inset", block) if ((s - (run % period) // 2) // period) % 2 == 1 else None
    return f


def slits(period, t0, t1, block=(B.STAINED_GLASS, 15), phase=None):
    """Narrow flush windows, one in every `period`, centred on the run."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= t1) or s < 2 or s > run - 3:
            return None
        p = period // 2 if phase is None else phase
        return ("accent", block) if (s - (run % period) // 2) % period == p else None
    return f


def checker(t0, t1, block, size=2):
    """A field of inset squares: a pattern for a large blank face."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= t1) or s == 0 or s == run - 1:
            return None
        return ("inset", block) if ((s // size) + (t // size)) % 2 == 0 else None
    return f


def _bitmap_row(t0, bitmaps, block, gap, min_run, inset, centre=True):
    """Bitmaps (lists of rows, top first) laid side by side along the face, centred on the run."""
    widths = [len(b[0]) for b in bitmaps]
    total = sum(widths) + gap * (len(bitmaps) - 1)
    rows = len(bitmaps[0])

    def f(s, run, t, h, n):
        if run < max(min_run, total + 2) or not (t0 <= t < t0 + rows):
            return None
        k = s - ((run - total) // 2 if centre else 1)
        for b, wd in zip(bitmaps, widths):
            if 0 <= k < wd:
                return (("inset" if inset else "accent"), block) if b[rows - 1 - (t - t0)][k] == "#" else None
            k -= wd + gap
        return None
    return f


def glyph_row(t0, names, block, spacing=8, min_run=7, inset=True):
    """Five-by-five glyphs inlaid along the face: as many as fit at `spacing`, centred, cycling through `names`
    and starting at a different one on every face."""
    rows = {}

    def f(s, run, t, h, n):
        if (run, n) not in rows:
            count = max(1, (run - 1) // spacing)
            rows[run, n] = _bitmap_row(t0, [GLYPHS[names[(k + n) % len(names)]] for k in range(count)], block,
                                       spacing - 5, min_run, inset)
        return rows[run, n](s, run, t, h, n)
    return f


def word(t0, text, block, gap=1, inset=True):
    """A word in the three-by-five letters, centred on the face and read left to right from outside."""
    return _bitmap_row(t0, [LETTERS[c] for c in text.upper()], block, gap, 0, inset)


def windows(period, t0, t1, block=(B.PANE, 0), width=1):
    """Flush windows `width` wide, one in every `period`, centred, from course t0 to t1."""
    def f(s, run, t, h, n):
        if not (t0 <= t <= t1) or s == 0 or s == run - 1:
            return None
        return ("accent", block) if (s - (run % period) // 2) % period < width else None
    return f


# ---- the mass --------------------------------------------------------------------------------------------
def faces(cells, has=None):
    """The face runs of a set of cells: (normal (dx, dz), [cells left to right seen from outside]). A cell open
    on exactly one side is a face; one open on two or more is a corner, returned apart and left flush."""
    cells = set(cells)
    has = has or (lambda x, z: (x, z) in cells)
    by_line, corners = {}, set()
    for x, z in cells:
        opens = [(dx, dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not has(x + dx, z + dz)]
        if len(opens) == 1:
            dx, dz = opens[0]
            by_line.setdefault((dx, dz, x if dx else z), []).append(z if dx else x)
        elif len(opens) >= 2:
            corners.add((x, z))
    runs = []
    for (dx, dz, line), alongs in sorted(by_line.items()):
        rx, rz = dz, -dx                                   # the viewer's right, facing the face from outside
        alongs.sort(key=lambda a: a * (rz if dx else rx))
        cur = [alongs[0]]
        for a in alongs[1:]:
            if abs(a - cur[-1]) == 1:
                cur.append(a)
            else:
                runs.append(((dx, dz), [(line, c) if dx else (c, line) for c in cur]))
                cur = [a]
        runs.append(((dx, dz), [(line, c) if dx else (c, line) for c in cur]))
    return runs, corners


def extrude(w, cells, y0, y1, base=CONCRETE, faces_=(), top=None, bottom=None, has=None, fill=True, top_block=SMOOTH):
    """Pour a mass from y0 to y1 over a set of cells and pattern its faces. base is a block or a function
    (x, y, z) -> block. top: "cornice", "parapet" or "parapet-slotted"; bottom: "coffer". Returns the faces."""
    cells = set(cells)
    has = has or (lambda x, z: (x, z) in cells)
    get = base if callable(base) else (lambda x, y, z: base)
    if fill:
        for x, z in cells:
            for y in range(y0, y1 + 1):
                w.set(x, y, z, *get(x, y, z))
    runs, _ = faces(cells, has)
    H = y1 - y0
    for n, ((dx, dz), run_cells) in enumerate(runs):
        run = len(run_cells)
        for s, (x, z) in enumerate(run_cells):
            for t in range(H + 1):
                act = next((a for a in (p(s, run, t, H, n) for p in faces_) if a), None)
                if not act:
                    continue
                kind, block = act
                if kind == "accent":
                    w.set(x, y0 + t, z, *block)
                elif kind == "inset" and has(x - dx, z - dz):
                    w.set(x, y0 + t, z, B.AIR)
                    w.set(x - dx, y0 + t, z - dz, *block)
    if top:
        top_course(w, cells, y1, top, top_block, has)
    if bottom == "coffer":
        coffer(w, cells, y0, has=has)
    return runs


def top_course(w, cells, y, kind, block=SMOOTH, has=None):
    """A cornice thrown out a block all round, a slab thick; or a parapet a block high, slotted every third."""
    cells = set(cells)
    has = has or (lambda x, z: (x, z) in cells)
    edge = [(x, z) for x, z in cells if any(not has(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    if kind == "cornice":
        for x, z in edge:
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if not has(x + dx, z + dz):
                        w.set(x + dx, y, z + dz, B.SLAB, 8)
    elif kind in ("parapet", "parapet-slotted"):
        for x, z in edge:
            if kind == "parapet" or (x + z) % 3:
                w.set(x, y + 1, z, *block)


def coffer(w, cells, y, period=4, size=2, rim=2, recess=(B.STAINED_CLAY, 8), light=(B.SEA_LANTERN, 0), has=None):
    """The underside cut into recesses `size` square on a grid of `period`, a light at the heart of every other
    one, a rim left whole."""
    cells = set(cells)
    has = has or (lambda x, z: (x, z) in cells)
    lo = (period - size) // 2
    for x, z in cells:
        if any(not has(x + dx, z + dz) for dx in range(-rim, rim + 1) for dz in range(-rim, rim + 1)):
            continue
        if lo <= x % period < lo + size and lo <= z % period < lo + size:
            w.set(x, y, z, B.AIR)
            lit = x % period == lo and z % period == lo and ((x // period) + (z // period)) % 2 == 0
            w.set(x, y + 1, z, *(light if lit else recess))


def concrete(every=4, block=CONCRETE, course=DARK):
    """Board-formed concrete: a course of a darker block every `every`."""
    return lambda x, y, z: course if y % every == 0 else block


# ---- floor fields ----------------------------------------------------------------------------------------
@dataclass
class Cell:
    x: int
    z: int
    u: float            # from the rectangle's middle
    v: float
    hw: float           # its half sizes
    hh: float
    edge: int           # blocks to the nearest side: 0 on the border
    x0: int
    z0: int


def border(width, block, at=None):
    """The outer `width` rows; or, with at, only the ring `at` blocks in."""
    if at is not None:
        return lambda c: block if c.edge == at else None
    return lambda c: block if c.edge < width else None


def medallion(r0, r1, block):
    """A diamond medallion: where |u|/hw + |v|/hh lies between r0 and r1."""
    return lambda c: block if r0 <= abs(c.u) / max(c.hw, 1) + abs(c.v) / max(c.hh, 1) < r1 else None


def corners(size, block, inset=6):
    """Quarter medallions in the four corners, `inset` in from each side."""
    return lambda c: block if abs(abs(c.u) - c.hw + inset) + abs(abs(c.v) - c.hh + inset) < size else None


def diamonds(period, r, block, along="z"):
    """A chain of diamonds down the middle, one every `period` blocks along x or z."""
    def f(c):
        s, q = ((c.z - c.z0), c.u) if along == "z" else ((c.x - c.x0), c.v)
        return block if abs((s % period) - period / 2) + abs(q) < r else None
    return f


def steps(width, blocks):
    """Kilim bands across the rectangle, stepped: bands `width` wide in turn through `blocks`."""
    def f(c):
        band = (c.x - c.x0) // width
        return blocks[band % len(blocks)]
    return f


def stepped_line(width, period, block):
    """The kilim's zigzag: a line stepping across every other band."""
    def f(c):
        band = (c.x - c.x0) // width
        st = abs(((c.z - c.z0) % period) - period // 2)
        return block if band % 2 and (c.x - c.x0) % width == st % width else None
    return f


def star(r, block):
    """An eight-pointed star in the middle: 0.7 of the larger offset and 0.3 of the smaller under r."""
    return lambda c: block if max(abs(c.u), abs(c.v)) * 0.7 + min(abs(c.u), abs(c.v)) * 0.3 < r else None


def stripes(period, width, block, axis="x"):
    return lambda c: block if ((c.x if axis == "x" else c.z) % period) < width else None


def tiles(size, a, b):
    """A checker of two blocks, `size` square."""
    return lambda c: a if ((c.x // size) + (c.z // size)) % 2 == 0 else b


def cross(width, block):
    """Two bands crossing at the middle, the garden carpet's water."""
    return lambda c: block if abs(c.u) < width or abs(c.v) < width else None


def first_of(*fields, default=None):
    """The first field that answers; `default` where none does."""
    def f(c):
        for g in fields:
            b = g(c)
            if b is not None:
                return b
        return default
    return f


def carpet(w, x0, z0, x1, z1, y, field):
    """Lay a floor field over a rectangle at course y. Returns the blocks laid by kind, for a legend."""
    cx, cz, hw, hh = (x0 + x1) / 2, (z0 + z1) / 2, (x1 - x0) / 2, (z1 - z0) / 2
    count = {}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c = Cell(x, z, x - cx, z - cz, hw, hh, min(x - x0, x1 - x, z - z0, z1 - z), x0, z0)
            b = field(c)
            if b is not None:
                w.set(x, y, z, *b)
                count[b] = count.get(b, 0) + 1
    return count


def rect_cells(x0, z0, x1, z1):
    return {(x, z) for x in range(min(x0, x1), max(x0, x1) + 1) for z in range(min(z0, z1), max(z0, z1) + 1)}


def poly_cells(poly):
    from .shapes import inside
    xs, zs = [p[0] for p in poly], [p[1] for p in poly]
    x0, x1, z0, z1 = int(np.floor(min(xs))) - 1, int(np.ceil(max(xs))) + 1, int(np.floor(min(zs))) - 1, int(np.ceil(max(zs))) + 1
    X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    m = inside(X + 0.0, Z + 0.0, poly)
    return {(int(x), int(z)) for x, z in zip(X[m], Z[m])}
