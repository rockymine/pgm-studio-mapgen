"""Buildings: a frame at any heading, the studio's roof field, a house, and the parts every board repeated.

    fr = Frame(cx=-20, cz=-6, heading=20)               # a house frame: u along its ridge, v across it
    house(w, House(-20, -6, 20, L=9, W=6, floor=31, storeys=2, style="plaster"))
    f = RoofField("hip", (0, 0, 8, 4), overhang=1, base_y=70)     # the studio's formulas, axis-aligned
    lay_roof(w, f, body=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5))

**The roof is the studio's.** `RoofField` is a port of `PgmStudio.Minecraft.Houses.RoofField`: one formula over
how far a cell stands from each wall line, six forms (gable, flat, hip, gambrel, shed, saltbox), whole or half
courses, an overhang that keeps falling to two courses below the wall top. The tests run it against
`data/roofs.json`, which `data/export_roofs.cs` writes from the studio's own class, so the two answer the same
crown, riser, slope and ridge for every cell. `lay_roof` lays it the way the studio's stamper does: stairs
climbing toward the higher neighbour, a slab on a one-wide ridge, the same stair hung upside down under a
column that overhangs.

**What the library adds is a heading.** A `Frame` places a building's own (u, v) on the board at any angle. A
block belongs to a shape when its centre falls inside it, so a 45 degree wall is a staircase one block at a time
and a 12 degree one a straight run with a jog. Walls are taken from eight neighbours, so a diagonal wall is
closed. `RoofField.framed` measures the same wall-line distances in the frame, so a turned roof is the studio's
roof turned, and at a heading of 0 or 90 it is the studio's roof exactly.

Block centres: block x spans x .. x+1 and its centre is x + 0.5. A frame centred on a whole number with an even
length covers exactly that many blocks; an odd length wants a centre on a half.
"""
import math
from dataclasses import dataclass, field as _field

import numpy as np

from .blocks import B
from .orient import DIRS, door as door_data, ladder as ladder_data, opposite, stair as stair_data, vec
from .shapes import boundary

FORMS = ("gable", "flat", "hip", "gambrel", "shed", "saltbox")
MAX_EAVE_DROP = 2                          # the studio's RoofField.MaxEaveDrop
_EAVE_FLOOR = -2 * MAX_EAVE_DROP
_ACROSS_Z_FIRST = ("n", "s", "w", "e")
_ACROSS_X_FIRST = ("w", "e", "n", "s")


# ---- the frame -------------------------------------------------------------------------------------------
class Frame:
    """A building's own axes on the board: u along `heading` (degrees from east, toward south), v across it."""

    def __init__(self, cx, cz, heading=0.0):
        self.cx, self.cz, self.heading = cx, cz, heading
        t = math.radians(heading)
        self.c, self.s = math.cos(t), math.sin(t)
        if abs(self.c) < 1e-12:
            self.c = 0.0
        if abs(self.s) < 1e-12:
            self.s = 0.0

    def local(self, x, z):
        """A world point (continuous) in the frame."""
        dx, dz = x - self.cx, z - self.cz
        return dx * self.c + dz * self.s, -dx * self.s + dz * self.c

    def world(self, u, v):
        return self.cx + u * self.c - v * self.s, self.cz + u * self.s + v * self.c

    def cell(self, u, v):
        """The block whose centre is nearest the frame point (u, v)."""
        x, z = self.world(u, v)
        return int(math.floor(x)), int(math.floor(z))

    def along(self, sign=1):
        """The cardinal nearest the frame's +u (or -u)."""
        return vec((sign * self.c, sign * self.s))

    def across(self, sign=1):
        return vec((-sign * self.s, sign * self.c))

    def box(self, L, W, margin=2):
        """World bounds (x0, z0, x1, z1) holding an L by W rectangle in the frame, with a margin."""
        r = math.hypot(L, W) / 2 + margin
        return (int(math.floor(self.cx - r)), int(math.floor(self.cz - r)),
                int(math.ceil(self.cx + r)), int(math.ceil(self.cz + r)))

    def grid(self, box):
        """World X, Z of the box's blocks and their centres' frame U, V."""
        x0, z0, x1, z1 = box
        X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
        dx, dz = X + 0.5 - self.cx, Z + 0.5 - self.cz
        return X, Z, dx * self.c + dz * self.s, -dx * self.s + dz * self.c

    def mask(self, L, W, box=None):
        """The blocks whose centres fall inside the frame's L by W rectangle: (mask, X, Z, U, V)."""
        box = box or self.box(L, W)
        X, Z, U, V = self.grid(box)
        eps = 1e-9
        return (np.abs(U) < L / 2 - eps) & (np.abs(V) < W / 2 - eps), X, Z, U, V

    def cells(self, L, W):
        m, X, Z, _, _ = self.mask(L, W)
        return {(int(x), int(z)) for x, z in zip(X[m], Z[m])}


def _whole(d):
    """A frame distance from a wall line's block centres, in whole blocks: a block whose centre lies inside the
    line's outer face counts 0 or more, the test `Frame.mask` uses, so a wall and its roof never disagree by
    half a block. Exact on the axis-aligned case, where every distance is whole."""
    return int(math.ceil(d + 0.5 - 1e-9)) - 1


# ---- the roof field --------------------------------------------------------------------------------------
class RoofField:
    """A roof as a height field over its plan, as the studio's RoofField answers it.

    box: the wall line (x0, z0, x1, z1), inclusive blocks. base_y: the course over the wall line, one above the
    wall's last. pitch: rise per block inward, in whole courses, or in half courses with halves=True. front: the
    wall a shed falls to and a saltbox turns its steep side toward ("n", "s", "w", "e"). ridge_along_x: which
    way the ridge runs, or None to take it across the shorter side.
    """

    def __init__(self, form, box, overhang=1, base_y=0, pitch=1, front="s", halves=False, ridge_along_x=None,
                 frame=None):
        if form not in FORMS:
            raise ValueError(f"no roof form {form!r}; one of {FORMS}")
        self.form, self.box = form, box
        self.x0, self.z0, self.x1, self.z1 = box
        self.overhang, self.base_y, self.pitch = max(0, overhang), base_y, max(1, pitch)
        self.front, self.halves, self.frame = front, halves, frame
        span_x, span_z = self.x1 - self.x0, self.z1 - self.z0
        self.across_z = ridge_along_x if ridge_along_x is not None else span_z <= span_x
        self.short_span = max(1, round(min(span_x, span_z)) + 1)
        self._cells = self._cover()
        crowns = [self.crown(x, z) for x, z in self._cells]
        self.peak, self.trough = max(crowns), min(crowns)

    @classmethod
    def framed(cls, form, frame, L, W, overhang=1, base_y=0, pitch=1, front="s", halves=False,
               ridge_along_u=None):
        """The same roof over an L by W rectangle in a frame: u is the field's x, v its z, and front names a
        side in the frame ("s" is +v)."""
        return cls(form, (-L / 2 + 0.5, -W / 2 + 0.5, L / 2 - 0.5, W / 2 - 0.5), overhang, base_y, pitch, front,
                   halves, ridge_along_u, frame)

    @property
    def ridge_along_x(self):
        return self.across_z

    # where a cell stands in the field's own axes
    def _ab(self, x, z):
        if self.frame is None:
            return x, z
        return self.frame.local(x + 0.5, z + 0.5)

    def _dist(self, x, z, smooth=False):
        """Blocks from the west, east, north and south wall lines. In a turned frame these are whole blocks, or
        with smooth (a half-course roof) the true distance, so the slope is measured to the half block."""
        a, b = self._ab(x, z)
        d = (a - self.x0, self.x1 - a, b - self.z0, self.z1 - b)
        if self.frame is None or smooth:
            return d
        return tuple(_whole(v) for v in d)

    def _cover(self):
        if self.frame is None:
            o = self.overhang
            return [(x, z) for x in range(self.x0 - o, self.x1 + o + 1) for z in range(self.z0 - o, self.z1 + o + 1)]
        L, W = self.x1 - self.x0 + 1, self.z1 - self.z0 + 1
        bx = self.frame.box(L + 2 * self.overhang, W + 2 * self.overhang)
        return [(x, z) for x in range(bx[0], bx[2] + 1) for z in range(bx[1], bx[3] + 1) if self.covers(x, z)]

    def cells(self):
        return list(self._cells)

    def covers(self, x, z):
        return min(self._dist(x, z)) >= -self.overhang

    def over_walls(self, x, z):
        """Inside the wall line: what a column hanging outside the building is not."""
        return min(self._dist(x, z)) >= 0

    def _rise(self, x, z):
        west, east, north, south = self._dist(x, z, smooth=self.halves and self.frame is not None)
        lo, hi = (north, south) if self.across_z else (west, east)
        from_front = {"n": north, "s": south, "w": west}.get(self.front, east)
        step = self.pitch if self.halves else 2 * self.pitch
        f = self.form
        if f == "flat":
            r = 0
        elif f == "shed":
            r = min(from_front, self.short_span - 1) * step
        elif f == "hip":
            r = min(west, east, north, south) * step
        elif f == "gambrel":
            span = (self.z1 - self.z0 if self.across_z else self.x1 - self.x0) + 1
            brk = max(1, int(round(span)) // 4)
            inward = min(lo, hi)
            r = inward * (step + 1) if inward <= brk else brk * (step + 1) + (inward - brk) * step
        elif f == "saltbox":
            front_high = self.front == "s" if self.across_z else self.front == "e"
            steep, shallow = (hi, lo) if front_high else (lo, hi)
            r = min(steep * (step + 1), shallow * step)
        else:
            r = min(lo, hi) * step
        return max(_EAVE_FLOOR, int(math.floor(r + 0.5 + 1e-9)))

    def crown(self, x, z):
        """The course the column's topmost block sits at (a slab's own course where half() says so)."""
        return self.base_y + (1 + self._rise(x, z)) // 2

    def half(self, x, z):
        return self.halves and self._rise(x, z) % 2 == 1

    def riser(self, x, z):
        """How many courses the column writes, to close the step down to its lowest covered neighbour."""
        c, drop = self.crown(x, z), 0
        for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if self.covers(x + dx, z + dz):
                below = self.crown(x + dx, z + dz)
                if below < c:
                    drop = max(drop, c - below + (1 if self.half(x + dx, z + dz) else 0))
        return max(1, drop)

    def underside(self, x, z):
        return self.crown(x, z) - self.riser(x, z) + 1

    def _order(self):
        return _ACROSS_Z_FIRST if self.across_z else _ACROSS_X_FIRST

    def upslope(self, x, z):
        """The side the slope climbs toward from this cell, or None on a ridge, a hip line or a lid."""
        toward, highest = None, self._rise(x, z)
        for e in self._order():
            dx, dz = DIRS[e]
            if self.covers(x + dx, z + dz):
                r = self._rise(x + dx, z + dz)
                if r > highest:
                    toward, highest = e, r
        return toward

    def steps_down(self, x, z):
        up = self.upslope(x, z)
        if up is None:
            return False
        dx, dz = DIRS[opposite(up)]
        return self.covers(x + dx, z + dz) and self._rise(x + dx, z + dz) < self._rise(x, z)

    def on_ridge(self, x, z):
        return self.form != "flat" and self.crown(x, z) == self.peak

    def ridge_partner(self, x, z):
        if not self.on_ridge(x, z):
            return None
        for e in self._order()[:2]:
            dx, dz = DIRS[e]
            if self.covers(x + dx, z + dz) and self.crown(x + dx, z + dz) == self.peak:
                return e
        return None

    def along_ridge_outward(self, x, z):
        """The way along the ridge from the roof's middle to the nearer gable end."""
        a, b = self._ab(x, z)
        if self.frame is not None:
            mid_a = mid_b = 0.0
            if self.across_z:
                return self.frame.along(1 if a >= mid_a else -1)
            return self.frame.across(1 if b >= mid_b else -1)
        o = self.overhang
        if self.across_z:
            return "w" if 2 * x < (self.x0 - o) + (self.x1 + o) else "e"
        return "n" if 2 * z < (self.z0 - o) + (self.z1 + o) else "s"

    def past_verge(self, x, z):
        """Past a wall line the ridge runs out to: the raked end, whose overhang stays open beneath."""
        if self.form in ("flat", "hip"):
            return False
        west, east, north, south = self._dist(x, z)
        return min(west, east) < 0 if self.across_z else min(north, south) < 0


def lay_roof(w, field, body, stair=None, slab=None, verge=None, ridge_cap=False, inside=None, lowest=None):
    """Lay a roof field into the world as the studio's stamper does.

    body: the roof's (id, data). stair: the stair id its slope steps in, or None for a roof of cubes. slab: the
    (id, data) a half course and a one-wide ridge take. verge: the (id, data) of the roof's outer ring and,
    with ridge_cap, its ridge. inside(x, z): the building's own footprint, where nothing is hung under a
    column; by default the field's wall line. lowest: no roof block below this course."""
    verge = verge or body
    inside = inside or field.over_walls
    rim = {c for c in field.cells() if any(not field.covers(c[0] + dx, c[1] + dz)
                                           for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    laid = []
    for x, z in field.cells():
        crown = field.crown(x, z)
        mat = verge if (x, z) in rim or (ridge_cap and field.on_ridge(x, z)) else body
        half = field.half(x, z)
        top = _stair_top(field, stair, slab, x, z) if stair is not None and not half else None
        lo = max(field.underside(x, z), lowest if lowest is not None else -1)
        for y in range(lo, (crown - 1 if half or top else crown) + 1):
            w.set(x, y, z, *mat)
        if top and crown >= lo:
            w.set(x, crown, z, top[0], top[1])
        if half and crown >= lo:
            s = slab or mat
            w.set(x, crown, z, s[0], s[1] & 7)
        if (not inside(x, z) and field.riser(x, z) == 1 and crown - 1 >= lo
                and w.id(x, crown - 1, z) == B.AIR):
            if top and (not top[2] or field.steps_down(x, z)):
                w.set(x, crown - 1, z, *top[3])
            elif half and field.steps_down(x, z):
                s = slab or mat
                w.set(x, crown - 1, z, s[0], (s[1] & 7) | 8)
        laid.append((x, z, lo, crown))
    return laid


def _stair_top(field, stair, slab, x, z):
    """(id, data, on the slope, (id, data) hung under it), or None for a cube."""
    up = field.upslope(x, z)
    if up is not None:
        return stair, stair_data(up), True, (stair, stair_data(opposite(up), True))
    if not field.on_ridge(x, z):
        return None
    partner = field.ridge_partner(x, z)
    if partner is not None:
        return stair, stair_data(partner), False, (stair, stair_data(opposite(partner), True))
    if slab is None:
        return None
    return slab[0], slab[1] & 7, False, (stair, stair_data(opposite(field.along_ridge_outward(x, z)), True))


# ---- the house -------------------------------------------------------------------------------------------
STYLES = {
    # walls of the ground storey and the upper ones (a mix), the frame's log wood (None: no timber frame),
    # gable, floor, roof body, its stair and slab, door, window
    "town": dict(ground=[(B.COBBLE, 0), (B.STONE, 5), (B.STONE, 0)], upper=[(B.PLANKS, 1)], post=0,
                 gable=(B.PLANKS, 1), floor=(B.PLANKS, 0), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS,
                 slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.PANE, 0)),
    "plaster": dict(ground=[(B.STONE, 0), (B.STONE, 5)], upper=[(B.STAINED_CLAY, 0)], post=1,
                    gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 1), stair=B.SPRUCE_STAIRS,
                    slab=(B.WOOD_SLAB, 1), door=B.SPRUCE_DOOR, window=(B.PANE, 0)),
    "brick": dict(ground=[(B.BRICK, 0)], upper=[(B.PLANKS, 2)], post=0, gable=(B.PLANKS, 1),
                  floor=(B.PLANKS, 0), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5),
                  door=B.OAK_DOOR, window=(B.PANE, 0)),
    "stone": dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2)], upper=[(B.STONEBRICK, 0)],
                  post=None, gable=(B.COBBLE, 0), floor=(B.PLANKS, 1), roof=(B.COBBLE, 0),
                  stair=B.COBBLE_STAIRS, slab=(B.SLAB, 3), door=B.DARK_OAK_DOOR, window=(B.IRON_BARS, 0)),
}


def windows(period=3, rows=((2,), (2, 3)), margin=1.5):
    """The window rhythm every board used: one in every `period` blocks along a wall, clear of its ends, on the
    given courses of the ground storey and of the upper ones. A function (run, span, t, storey) -> bool."""
    def f(run, span, t, storey):
        on_row = t in (rows[0] if storey == 0 else rows[-1])
        return on_row and margin < run < span - margin and abs((run % period) - period / 2) < 0.6
    return f


@dataclass
class House:
    """A house at any heading. L along the ridge, W across; floor is the y of the plate; door is the long side
    the door is on (+1 the frame's +v, -1 its -v). Square to the board, the centre is snapped so an odd side
    stands on a half block and an even one on a whole."""
    cx: float
    cz: float
    heading: float = 0.0
    L: int = 9
    W: int = 6
    floor: int = 64
    storeys: int = 2
    storey: int = 4                       # three courses of wall and the laid course at its head
    style: object = "town"
    jetty: bool = False
    door: int = 1
    chimney: bool = True
    roof: str = "gable"
    pitch: int = 1
    overhang: int = 1
    windows: object = _field(default_factory=windows)


def house(w, h, ground_at=None, rng=None):
    """Build one house. ground_at(x, z) gives the ground's height, so the plate is filled down to it. Returns
    the door (x, z, facing), the footprint cells, the eave course and the roof field."""
    st = STYLES[h.style] if isinstance(h.style, str) else h.style
    rng = rng or np.random.default_rng(int(abs(h.cx * 31 + h.cz * 17 + h.heading)))
    square = h.heading % 90 == 0
    cx, cz = h.cx, h.cz
    if square:                                   # an odd side wants its centre on a half block, an even one whole
        along_x = h.heading % 180 == 0
        lx, lz = (h.L, h.W) if along_x else (h.W, h.L)
        cx = math.floor(cx) + (0.5 if lx % 2 else 0)
        cz = math.floor(cz) + (0.5 if lz % 2 else 0)
    fr = Frame(cx, cz, h.heading)
    n, sh, f = h.storeys, h.storey, h.floor
    jetty = h.jetty and n >= 2
    dims = [(h.L, h.W + (2 if jetty and s > 0 else 0)) for s in range(n)]
    box = fr.box(h.L + 2 * h.overhang + 2, h.W + 2 * h.overhang + 4)

    def pick(mats):
        return mats[int(rng.integers(len(mats)))]

    storeys = []
    for Ls, Ws in dims:
        m, X, Z, U, V = fr.mask(Ls, Ws, box)
        storeys.append((m, boundary(m, diagonal=True), Ls, Ws))
    base, base_wall = storeys[0][0], storeys[0][1]
    eave = f + n * sh
    # the plate, what is under it, and the inside cleared
    for i, k in zip(*np.nonzero(base)):
        x, z = int(X[i, k]), int(Z[i, k])
        g = ground_at(x, z) if ground_at else f
        for y in range(min(g, f), f):
            w.set(x, y, z, *((B.STONE, 0) if rng.random() < 0.7 else (B.COBBLE, 0)))
        w.set(x, f, z, *(st["ground"][0] if base_wall[i, k] else st["floor"]))
        for y in range(f + 1, eave + 1):
            w.set(x, y, z, B.AIR)
    # the storeys
    for s, (m, wall, Ls, Ws) in enumerate(storeys):
        y0 = f + s * sh
        mats = st["ground"] if s == 0 else st["upper"]
        for i, k in zip(*np.nonzero(m)):
            x, z, u, v = int(X[i, k]), int(Z[i, k]), U[i, k], V[i, k]
            if not wall[i, k]:
                if s > 0:
                    w.set(x, y0, z, *st["floor"])
                continue
            corner = abs(u) > Ls / 2 - 1 and abs(v) > Ws / 2 - 1
            long_wall = abs(v) > Ws / 2 - 1
            run, span = (u + Ls / 2, Ls) if long_wall else (v + Ws / 2, Ws)
            frame_line = long_wall and abs(((run + 1.5) % 4) - 2) < 0.5 and not corner
            post = st["post"] is not None and (corner or (frame_line and s > 0))
            dx, dz = (fr.c, fr.s) if long_wall else (-fr.s, fr.c)
            for y in range(y0 + 1, y0 + sh + 1):
                if post:
                    blk = (B.LOG, st["post"])
                elif y == y0 + sh and st["post"] is not None:
                    blk = (B.LOG, st["post"] | (4 if abs(dx) >= abs(dz) else 8))
                elif h.windows(run, span, y - y0, s):
                    blk = st["window"]
                else:
                    blk = pick(mats)
                w.set(x, y, z, *blk)
        if jetty and s == 1:                                     # the joists showing under a jettied storey
            for i, k in zip(*np.nonzero(m & ~base)):
                w.set(int(X[i, k]), y0, int(Z[i, k]), B.LOG, (st["post"] or 0) | (4 if abs(fr.s) >= abs(fr.c) else 8))
    # the door, in the middle of its long wall
    cands = [(abs(U[i, k]), int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(base_wall))
             if h.door * V[i, k] > h.W / 2 - 1 and abs(U[i, k]) < h.L / 2 - 1.5]
    door_at = None
    if cands:
        _, x, z = min(cands)
        facing = fr.across(h.door)
        w.set(x, f + 1, z, st["door"], door_data(facing))
        w.set(x, f + 2, z, st["door"], door_data(facing, upper=True))
        door_at = (x, z, facing)
    # the roof
    mt, wt, Lt, Wt = storeys[-1]
    top_cells = {(int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(mt))}
    # square to the board the roof is the studio's, in stairs; turned, stairs can only face the four ways and
    # the slope reads ragged, so it is laid in cubes and slabs measured to the half block
    field = RoofField.framed(h.roof, fr, Lt, Wt, h.overhang, eave + 1, h.pitch if square else 2 * h.pitch,
                             "s" if h.door > 0 else "n", halves=not square)
    for x, z in field.cells():                                   # the attic cleared before the roof is laid
        for y in range(eave + 1, field.crown(x, z) + 1):
            if (x, z) in top_cells:
                w.set(x, y, z, B.AIR)
    lay_roof(w, field, st["roof"], st["stair"] if square else None, st["slab"],
             inside=lambda x, z: (x, z) in top_cells)
    for i, k in zip(*np.nonzero(wt)):                            # gable walls up to the roof's underside
        x, z = int(X[i, k]), int(Z[i, k])
        for y in range(eave + 1, field.underside(x, z)):
            w.set(x, y, z, *st["gable"])
    if h.chimney and h.roof != "flat":
        x, z = fr.cell(Lt / 4, Wt / 4)
        top = field.crown(x, z) + 2
        for y in range(f + 1, top + 1):
            w.set(x, y, z, *((B.COBBLE, 0) if y < top else (B.COBBLE_WALL, 0)))
    return dict(door=door_at, footprint=fr.cells(h.L, h.W + (2 if jetty else 0)), eave=eave, roof=field)


# ---- the parts every board repeated ----------------------------------------------------------------------
def edge_cells(cells):
    """The cells of a set with a four-neighbour outside it."""
    cells = set(cells)
    return {(x, z) for x, z in cells if any((x + dx, z + dz) not in cells for dx, dz in DIRS.values())}


def parapet(w, cells, y, block, crenel=None, rhythm=None):
    """A parapet round the edge of a set of cells at course y, and a crenel on top where rhythm(x, z) says so
    (default every other block)."""
    rhythm = rhythm or (lambda x, z: (x + z) % 2 == 0)
    for x, z in edge_cells(cells):
        w.set(x, y, z, *block)
        if crenel is not None and rhythm(x, z):
            w.set(x, y + 1, z, *crenel)


def site(w, cells, floor_y, ground_at, margin=2, fill=(B.STONE, 0), top=(B.GRASS, 0), under=(B.DIRT, 0),
         clear=12):
    """Level the ground under a footprint to floor_y and ease the ground round it back over `margin` blocks:
    fill below, air above, the eased ring topped like ground."""
    cells = set(cells)
    for x, z in cells:
        g = ground_at(x, z)
        for y in range(min(g, floor_y) - 1, floor_y + 1):
            w.set(x, y, z, *fill)
        for y in range(floor_y + 1, floor_y + clear):
            w.set(x, y, z, B.AIR)
    ring, frontier = {}, set(cells)
    for d in range(1, margin + 1):
        nxt = {(x + dx, z + dz) for x, z in frontier for dx, dz in DIRS.values()} - cells - set(ring)
        for c in nxt:
            ring[c] = d
        frontier = nxt
    for (x, z), d in ring.items():
        g = ground_at(x, z)
        y = int(round(floor_y + (g - floor_y) * d / (margin + 1)))
        for yy in range(min(g, y) - 1, y):
            w.set(x, yy, z, *under)
        w.set(x, y, z, *top)
        for yy in range(y + 1, max(g, y) + clear):
            w.set(x, yy, z, B.AIR)


def stairs(w, x, z, rises, y0, n, block, width=1, under=None):
    """A straight flight of n stairs climbing toward `rises` from (x, y0, z), `width` wide to the right of the
    climb, with `under` (id, data) filled beneath each step if given."""
    dx, dz = vec(rises)
    rx, rz = -dz, dx
    for k in range(n):
        for j in range(width):
            X, Z, Y = x + k * dx + j * rx, z + k * dz + j * rz, y0 + k
            w.set(X, Y, Z, block, stair_data(rises))
            if under:
                for yy in range(y0, Y):
                    w.set(X, yy, Z, *under)


def ladder(w, x, z, y0, y1, on_wall):
    """A ladder from y0 to y1 on the wall at that side of the column."""
    for y in range(y0, y1 + 1):
        w.set(x, y, z, B.LADDER, ladder_data(on_wall))


class Claims:
    """What stands where, by layer, so overlaps are listed rather than overwritten unseen."""

    def __init__(self):
        self.by_layer = {}

    def claim(self, name, cells, layer="ground"):
        self.by_layer.setdefault(layer, []).append((name, set(cells)))

    def overlaps(self):
        out = []
        for layer, items in self.by_layer.items():
            for i, (a, ca) in enumerate(items):
                for b, cb in items[i + 1:]:
                    both = ca & cb
                    if both:
                        out.append((layer, a, b, len(both)))
        return out
