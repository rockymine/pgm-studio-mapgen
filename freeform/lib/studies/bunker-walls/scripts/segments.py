"""A grammar for bunker walls and floors: a face cut into segments, each segment a rectangle peeled side by side
into strips, every strip or core painted by a material that may fade, sit back or show what is behind it.

    seg = Segment([Peel("top", BLUE), Peel("right", ORANGE), Peel("top", RED), Peel("left", RED),
                   Peel("top", GREEN)], core=YELLOW)
    wall(w, cells, base=4, heights=24, seg=seg, outside=lambda x, z: z > 9)

What the grammar reads:

    a segment   W by H cells, s from the left as seen from outside, t up from the bottom; peeled in order, each
                peel taking `width` rows or columns off one side of what is left, the core the rest
    a material  (u, v, along, key) -> (face block, back block): u and v run 0..1 across the strip or core, along
                runs the strip's length (left to right on a top or bottom strip, bottom to top on a side one)
    a face      every straight run of wall columns open to the outside, cut into segments as near the module as
                the run allows; a column open on two sides is the left end of the face it starts, so an outward
                corner wears the next segment's left leg on both of its sides, and an inward corner is where one
                segment's right leg meets the next one's left
    a tier      a face's height cut the same way into rows of segments, stacked

A floor is the same segment laid flat: s along x, t along z, no back.
"""
import math
from dataclasses import dataclass

from pgmvox.core.blocks import B
from pgmvox.core.orient import stair

DIRS = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
LEFT = {"s": (1, 0), "n": (-1, 0), "e": (0, -1), "w": (0, 1)}   # a face's left-to-right seen from outside it

AIR = (B.AIR, 0)
STONE = (B.STONE, 0)
ANDESITE = (B.STONE, 5)
POL_ANDESITE = (B.STONE, 6)
COBBLE = (B.COBBLE, 0)
COBBLE_WALL = (B.COBBLE_WALL, 0)
NETHER_BRICK = (B.NETHER_BRICK, 0)
BEDROCK = (B.BEDROCK, 0)
OBSIDIAN = (B.OBSIDIAN, 0)
GRAY_WOOL = (B.WOOL, 7)
LIGHT_GRAY_WOOL = (B.WOOL, 8)
BLACK_WOOL = (B.WOOL, 15)
COAL = (B.COAL_BLOCK, 0)
CLAY = (B.CLAY, 0)
CYAN_CLAY = (B.STAINED_CLAY, 9)
GRAY_GLASS = (B.STAINED_GLASS, 7)
IRON_BARS = (B.IRON_BARS, 0)
DSLAB = (B.DSLAB, 0)                    # double stone slab: the seam on its sides, the rimmed plate on top
SMOOTH_DSLAB = (B.DSLAB, 8)             # the rimmed plate on every side
TOP_SLAB = {"stone": (B.SLAB, 8), "cobble": (B.SLAB, 11), "stonebrick": (B.SLAB, 13), "nether": (B.SLAB, 14)}
LOW_SLAB = {"stone": (B.SLAB, 0), "cobble": (B.SLAB, 3), "stonebrick": (B.SLAB, 5), "nether": (B.SLAB, 6)}


def h01(*key):
    """A fixed number in [0, 1) for a key: the same block draws the same way on every run."""
    n = 2166136261
    for k in key:
        n = ((n ^ (int(k) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 13
    n = (n * 0x5BD1E995) & 0xFFFFFFFF
    n ^= n >> 15
    return n / 4294967296.0


# ---- materials ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Solid:
    """One block at the face, `back` behind it (None leaves the wall's body)."""
    block: tuple
    back: tuple = None

    def at(self, u, v, along, key, inward=None):
        return self.block, self.back


@dataclass(frozen=True)
class Fade:
    """Blocks blended along one axis: stops [(block, t), ...] with t rising, a block drawn between the two stops
    either side of a cell's t. `noise` 0 cuts sharp at the midpoint, 1 dithers the whole span linearly. `axis` is
    "along", "u", "v" or "y" (world height between `y_range`)."""
    stops: tuple
    axis: str = "along"
    noise: float = 0.6
    back: tuple = None
    y_range: tuple = None
    flip: bool = False

    def t(self, u, v, along, key):
        if self.axis == "y":
            y0, y1 = self.y_range
            return (key[1] - y0) / max(1, y1 - y0)
        t = {"along": along, "u": u, "v": v}[self.axis]
        return 1 - t if self.flip else t

    def at(self, u, v, along, key, inward=None):
        t = min(1.0, max(0.0, self.t(u, v, along, key)))
        stops = self.stops
        if t <= stops[0][1]:
            return stops[0][0], self.back
        for (a, ta), (b, tb) in zip(stops, stops[1:]):
            if t <= tb:
                f = (t - ta) / max(1e-9, tb - ta)
                p = min(1.0, max(0.0, 0.5 + (f - 0.5) / max(self.noise, 1e-3)))
                return (b if h01(*key, 7) < p else a), self.back
        return stops[-1][0], self.back


@dataclass(frozen=True)
class Nook:
    """An upside-down stair with its full half at the back: a top slab at the face over a half-block nook that runs
    unbroken along the course."""
    stairs: int = B.STONEBRICK_STAIRS
    back: tuple = None

    def at(self, u, v, along, key, inward=None):
        return (self.stairs, stair(inward, upside_down=True)), self.back


@dataclass(frozen=True)
class Courses:
    """A core in rows: `top` are its rows read down from its top, `rest` every row under them, so a taller core
    stretches at its foot."""
    top: tuple
    rest: object


# ---- segments -----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Peel:
    """`width` rows (top, bottom) or columns (left, right) off one side of what is left, in `material`."""
    side: str
    material: object
    width: int = 1


@dataclass(frozen=True)
class Segment:
    """A rectangle peeled in order, the core what is left. `overlays` are (s, t, w, h) -> material or None, laid
    over everything: a slit, a glyph across the whole segment."""
    peels: tuple
    core: object
    overlays: tuple = ()
    name: str = "segment"

    def cells(self, w, h):
        """{(s, t): (material, u, v, along)} for a w by h segment."""
        out = {}
        s0, s1, t0, t1 = 0, w - 1, 0, h - 1
        for p in self.peels:
            for _ in range(p.width):
                if s0 > s1 or t0 > t1:
                    break
                if p.side in ("top", "bottom"):
                    t = t1 if p.side == "top" else t0
                    for s in range(s0, s1 + 1):
                        a = (s - s0) / max(1, s1 - s0)
                        out[(s, t)] = (p.material, a, 0.0, a)
                    t1, t0 = (t1 - 1, t0) if p.side == "top" else (t1, t0 + 1)
                else:
                    s = s0 if p.side == "left" else s1
                    for t in range(t0, t1 + 1):
                        a = (t - t0) / max(1, t1 - t0)
                        out[(s, t)] = (p.material, 0.0, a, a)
                    s0, s1 = (s0 + 1, s1) if p.side == "left" else (s0, s1 - 1)
        cw, ch = s1 - s0 + 1, t1 - t0 + 1
        for s in range(s0, s1 + 1):
            for t in range(t0, t1 + 1):
                m = self.core
                if isinstance(m, Courses):
                    down = t1 - t
                    m = m.top[down] if down < len(m.top) else m.rest
                u, v = (s - s0) / max(1, cw - 1), (t - t0) / max(1, ch - 1)
                out[(s, t)] = (m, u, v, v)
        for overlay in self.overlays:
            for (s, t), cell in list(out.items()):
                m = overlay(s, t, w, h)
                if m is not None:
                    out[(s, t)] = (m, cell[1], cell[2], cell[3])
        return out


def cuts(n, module, minimum=3):
    """n cut into runs as near `module` as can be, the longer ones from both ends inward: [(a, b), ...]."""
    k = max(1, round(n / module))
    while k > 1 and n // k < minimum:
        k -= 1
    q, r = divmod(n, k)
    sizes = [q] * k
    i = 0
    while r >= 2 and i < k - 1 - i:
        sizes[i] += 1
        sizes[k - 1 - i] += 1
        r -= 2
        i += 1
    if r:
        sizes[k // 2] += 1
    out, a = [], 0
    for size in sizes:
        out.append((a, a + size - 1))
        a += size
    return out


# ---- laying a segment on a face -----------------------------------------------------------------------------
def lay_segment(w, seg, columns, side, y0, h, back_ok=None):
    """Lay `seg` over face columns [(x, z), ...] left to right seen from outside, rows y0..y0+h-1, the face
    looking `side`. A back lands one column inward where back_ok(x, z) allows."""
    inward = OPP[side]
    ix, iz = DIRS[inward]
    for (s, t), (m, u, v, along) in seg.cells(len(columns), h).items():
        x, z = columns[s]
        y = y0 + t
        face, back = m.at(u, v, along, (x, y, z), inward)
        w.set(x, y, z, *face)
        if back is not None and (back_ok is None or back_ok(x + ix, z + iz)):
            w.set(x + ix, y, z + iz, *back)


def faces(cells, outside):
    """Every straight run of wall columns open to the outside: [(side, [(x, z), ...] left to right)]. A column
    open on two sides belongs to the face whose left end it is."""
    open_sides = {}
    for x, z in cells:
        sides = [d for d, (dx, dz) in DIRS.items() if (x + dx, z + dz) not in cells and outside(x + dx, z + dz)]
        if sides:
            open_sides[(x, z)] = sides
    owner = {}
    for c, sides in open_sides.items():
        if len(sides) == 1:
            owner[c] = sides[0]
            continue
        for d in sides:                                     # the side whose run this column starts
            lx, lz = LEFT[d]
            prev = (c[0] - lx, c[1] - lz)
            if d not in open_sides.get(prev, ()):
                owner[c] = d
                break
        else:
            owner[c] = sides[0]
    by = {}
    for (x, z), d in owner.items():
        by.setdefault((d, x if d in ("e", "w") else z), []).append((x, z))
    out = []
    for (d, _), cs in sorted(by.items()):
        lx, lz = LEFT[d]
        cs.sort(key=lambda c: c[0] * lx + c[1] * lz)
        run = [cs[0]]
        for c in cs[1:]:
            if (c[0] * lx + c[1] * lz) - (run[-1][0] * lx + run[-1][1] * lz) == 1:
                run.append(c)
            else:
                out.append((d, run))
                run = [c]
        out.append((d, run))
    return out


@dataclass
class Opening:
    """A hole in a face: the columns in xs (or zs on an east or west face) on `side`, rows y0..y1, laid by
    lay(w, columns, side, y0, y1) instead of segments; the segments round it are cut to the module that is left.
    `line` is the face's z (or x on an east or west face) when more than one face looks that way."""
    side: str
    lo: int
    hi: int
    y0: int
    y1: int
    lay: object = None
    line: int = None


def wall(w, cells, base, heights, seg, outside, module=6, tier=8, body=COBBLE, segment_of=None, openings=(),
         top=None):
    """A wall over plan `cells` (a set of (x, z)), its body `body` from `base` to its height, every face open to
    the outside cut into segments `module` wide and `tier` tall. `heights` is one number or {(x, z): h}; a face
    splits where its height changes. segment_of(side, i, j, run) may choose a segment for bay i, tier j of a run.
    `top(w, side, columns, y)` lays what stands on a run's rim. An opening's segments over it are asked for with
    tier "over"."""
    hof = (lambda c: heights) if isinstance(heights, int) else (lambda c: heights[c])
    for x, z in cells:
        w.column(x, z, base, base + hof((x, z)) - 1, *body)
    runs = []
    for side, run in faces(cells, outside):
        part = [run[0]]
        for c in run[1:]:
            if hof(c) == hof(part[-1]):
                part.append(c)
            else:
                runs.append((side, part))
                part = [c]
        runs.append((side, part))
    back_ok = lambda x, z: (x, z) in cells
    for side, run in runs:
        h = hof(run[0])
        line = run[0][1] if side in ("n", "s") else run[0][0]
        holes = [o for o in openings if o.side == side and o.line in (None, line) and any(
            o.lo <= (c[0] if side in ("n", "s") else c[1]) <= o.hi for c in run)]
        pieces = [run]
        for o in holes:
            nxt = []
            for p in pieces:
                key = (lambda c: c[0]) if side in ("n", "s") else (lambda c: c[1])
                left = [c for c in p if not o.lo <= key(c) <= o.hi]
                inside = [c for c in p if o.lo <= key(c) <= o.hi]
                if not inside:
                    nxt.append(p)
                    continue
                k = p.index(inside[0])
                a, b = p[:k], p[k + len(inside):]
                nxt += [q for q in (a, b) if q]
                bays = cuts(len(inside), module)
                if o.y0 > base:                             # the segments under the opening's sill
                    for (t0, t1) in cuts(o.y0 - base, tier):
                        for (a, b) in bays:
                            lay_segment(w, seg, inside[a:b + 1], side, base + t0, t1 - t0 + 1, back_ok)
                above = base + h - 1 - o.y1
                for (t0, t1) in (cuts(above, tier) if above > 0 else []):
                    for i, (a, b) in enumerate(bays):
                        s = segment_of(side, i, "over", inside) if segment_of else seg
                        lay_segment(w, s, inside[a:b + 1], side, o.y1 + 1 + t0, t1 - t0 + 1, back_ok)
                if o.lay:
                    o.lay(w, inside, side, o.y0, o.y1)
            pieces = nxt
        for p in pieces:
            for i, (a, b) in enumerate(cuts(len(p), module)):
                for j, (t0, t1) in enumerate(cuts(h, tier)):
                    s = segment_of(side, i, j, p) if segment_of else seg
                    lay_segment(w, s, p[a:b + 1], side, base + t0, t1 - t0 + 1, back_ok)
        if top:
            top(w, side, run, base + h)
    return runs


# ---- the crown: a band that follows a stepped roof -----------------------------------------------------------
def crown(rise=3, step=1, plinth=POL_ANDESITE, nook=Nook(), fill=STONE, under=ANDESITE, roof=BLACK_WOOL,
          shape="gable", body=COBBLE, rows=3):
    """A top(...) for wall(): plinth and nook in the face, then `rows` of fill and a band two under the roof, both a
    block back, under a roof in the face that steps up `step` every `rise` columns: one way ("lean") or to the
    middle and down ("gable"). The roof is the only overhang: over the inset, and a block past each end."""
    def lay(w, side, columns, y):
        n = len(columns)
        inward = OPP[side]
        ix, iz = DIRS[inward]
        lx, lz = LEFT[side]
        for s, (x, z) in enumerate(columns):
            if shape == "gable":
                k = min(s, n - 1 - s) // rise
            else:
                k = s // rise
            top = y + 2 + rows + 2 + k * step
            for yy in range(y, top + 1):
                w.set(x + ix, yy, z + iz, *body)
                w.set(x + 2 * ix, yy, z + 2 * iz, *body)
            w.set(x, y, z, *plinth)
            face, _ = nook.at(0, 0, 0, (x, y + 1, z), inward)
            w.set(x, y + 1, z, *face)
            for yy in range(y + 2, top):                   # fill and band a block back, under the roof
                w.set(x, yy, z, B.AIR)
                w.set(x + ix, yy, z + iz, *(under if yy >= top - 2 else fill))
            w.set(x, top, z, *roof)
            w.set(x + ix, top, z + iz, *roof)
        for s, (x, z) in ((-1, columns[0]), (n, columns[-1])):
            k = 0 if shape == "gable" else max(0, n - 1) // rise
            top = y + 2 + rows + 2 + k * step
            ex, ez = x + (lx if s == n else -lx), z + (lz if s == n else -lz)
            w.set(ex, top, ez, *roof)
            w.set(ex + ix, top, ez + iz, *roof)
    return lay


# ---- floors ---------------------------------------------------------------------------------------------------
def floor(w, box, y, seg, module=6, align=None):
    """A floor of segments laid flat over box (x0, z0, x1, z1), `module` a side, counted from `align` (x, z)
    when given so the tiles line up with a wall's bays."""
    x0, z0, x1, z1 = box
    ax, az = align or (x0, z0)
    xs = list(range(x0, x1 + 1))
    zs = list(range(z0, z1 + 1))
    def bands(vals, a):
        out, cur = [], [vals[0]]
        for v in vals[1:]:
            if (v - a) % module == 0:
                out.append(cur)
                cur = [v]
            else:
                cur.append(v)
        out.append(cur)
        return out
    for bx in bands(xs, ax):
        for bz in bands(zs, az):
            for (s, t), (m, u, v, along) in seg.cells(len(bx), len(bz)).items():
                x, z = bx[s], bz[len(bz) - 1 - t]
                block, _ = m.at(u, v, along, (x, y, z), "n")
                w.set(x, y, z, *block)


# ---- lofted planes ---------------------------------------------------------------------------------------------
def _level(strips, y):
    """Where the plane y cuts a chain of edges: the polyline [(x, z), ...] and, for each of its points, the bottom
    edge it lies over (k, f) as an index and a share. A quad whose far edge ends under y is cut along its top."""
    pts, over = [], []
    for k, ((b0, t0), (b1, t1)) in enumerate(zip(strips, strips[1:])):
        def on_edge(b, t):
            f = (y - b[1]) / max(1e-9, t[1] - b[1])
            return (b[0] + (t[0] - b[0]) * f, b[2] + (t[2] - b[2]) * f) if 0 <= f <= 1 else None
        p0, p1 = on_edge(b0, t0), on_edge(b1, t1)
        if p0 is None and p1 is None:
            continue
        if p0 is None or p1 is None:                         # the quad's top crosses y between its edges
            g = (y - t0[1]) / (t1[1] - t0[1])
            if not 0 <= g <= 1:
                continue
            pt = (t0[0] + (t1[0] - t0[0]) * g, t0[2] + (t1[2] - t0[2]) * g)
            p0, f0 = (pt, g) if p0 is None else (p0, 0.0)
            p1, f1 = (pt, g) if p1 is None else (p1, 1.0)
        else:
            f0, f1 = 0.0, 1.0
        if not pts or math.dist(pts[-1], p0) > 1e-6:
            pts.append(p0)
            over.append((k, f0))
        pts.append(p1)
        over.append((k, f1))
    return pts, over


def loft(w, strips, material, thick=3, behind=None, reach=30, marks=()):
    """Ruled walls between pairs of 3-D edges, the way a loft tool spans a plane: `strips` is a chain of
    (bottom, top) points [((x, y, z), (x, y, z)), ...], each pair the edge the next plane starts from, the face
    looking to the left of the chain's direction. Edges may differ in height, so a wall can fall toward its end.
    At every height the face is where that height cuts the planes; `thick` blocks behind it are wall, painted by
    material.at(u, v, along, key) with u the distance along the face and v the share of the wall's height there,
    and everything further behind, up to `reach` from the face, is behind(x, y, z) where it answers. `marks` are
    (u0, v0, bitmap rows top first, scale, block): inlays on the face, v0 in blocks over the lowest foot. Returns
    the face blocks."""
    ys = [p[1] for e in strips for p in e]
    ylo, yhi = min(ys), max(ys)
    face_cells = {}
    for y in range(ylo, yhi + 1):
        pts, over = _level(strips, y)
        if len(pts) < 2:
            continue
        acc = [0.0]
        for p, q in zip(pts, pts[1:]):
            acc.append(acc[-1] + math.dist(p, q))
        xs = [p[0] for p in pts]
        zs = [p[1] for p in pts]
        for x in range(int(min(xs)) - thick - reach, int(max(xs)) + thick + reach + 1):
            for z in range(int(min(zs)) - thick - reach, int(max(zs)) + thick + reach + 1):
                best = None
                for k, (p, q) in enumerate(zip(pts, pts[1:])):
                    dx, dz = q[0] - p[0], q[1] - p[1]
                    L2 = dx * dx + dz * dz
                    if L2 < 1e-9:
                        continue
                    raw = ((x + 0.5 - p[0]) * dx + (z + 0.5 - p[1]) * dz) / L2
                    tt = min(1.0, max(0.0, raw))
                    cx, cz = p[0] + tt * dx, p[1] + tt * dz
                    nx, nz = -dz / math.sqrt(L2), dx / math.sqrt(L2)        # the face's outward normal
                    sd = (x + 0.5 - cx) * nx + (z + 0.5 - cz) * nz
                    d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
                    beyond = (k == 0 and raw < 0) or (k == len(pts) - 2 and raw > 1)   # past an end: cut square
                    if best is None or d < best[0]:
                        if beyond:
                            best = (d, None, 0, 0, 0)
                            continue
                        (ka, fa), (kb, fb) = over[k], over[k + 1]
                        e, f = (ka, fa + (fb - fa) * tt) if ka == kb else (kb, fb * tt)
                        best = (d, sd, acc[k] + tt * math.sqrt(L2), e, f)
                if best is None or best[1] is None:
                    continue
                d, sd, u, e, f = best
                top = strips[e][1][1] + (strips[e + 1][1][1] - strips[e][1][1]) * f
                foot = strips[e][0][1] + (strips[e + 1][0][1] - strips[e][0][1]) * f
                if -thick <= sd <= 0.0 and d <= thick + 0.5:
                    v = min(1.0, max(0.0, (y - foot) / max(1.0, top - foot)))
                    block, _ = material.at(u, v, v, (x, y, z))
                    w.set(x, y, z, *block)
                    if sd > -1.0:
                        face_cells[(x, y, z)] = u
                elif sd < -thick and behind is not None and d < reach:
                    b = behind(x, y, z)
                    if b is not None:
                        w.set(x, y, z, *b)
    for (u0, v0, rows, scale, block) in marks:
        H = len(rows) * scale
        for (x, y, z), u in face_cells.items():
            du = int(math.floor(u - u0))
            dv = y - ylo - v0
            if 0 <= du < len(rows[0]) * scale and 0 <= dv < H:
                if rows[len(rows) - 1 - dv // scale][du // scale] == "#":
                    w.set(x, y, z, *block)
    return face_cells


# ---- panels shifted out of line --------------------------------------------------------------------------------
def staggered(w, x0, z0, seg, bays, tiers, shift_bay=0, shift_tier=0, back=None, base=0, module=6, tier=8,
              body=COBBLE):
    """A south face of `bays` by `tiers` segments, each one set out of line with its neighbours: bay i stands
    i * shift_bay blocks further south (forward) and tier j j * shift_tier further, so 1 per bay runs the wall on
    a diagonal, -1 per tier leans it back, and both slant it two ways at once. Every panel has the wall's two
    blocks behind its face, and solid body back to z = `back`. The step each shift leaves shows a panel's end."""
    zs = [z0 + i * shift_bay + j * shift_tier for i in range(bays) for j in range(tiers)]
    back = min(zs) - 2 if back is None else back
    for i in range(bays):
        for j in range(tiers):
            zf = z0 + i * shift_bay + j * shift_tier
            xa = x0 + i * module
            y0 = base + j * tier
            w.fill(xa, y0, back, xa + module - 1, y0 + tier - 1, zf, *body)
            lay_segment(w, seg, [(xa + s, zf) for s in range(module)], "s", y0, tier)
