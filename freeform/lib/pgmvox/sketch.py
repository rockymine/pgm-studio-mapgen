"""The sketch: a plan drawn before anything is built, annotated so it can be reviewed, and the same annotation
drawn again over the built world afterwards.

A sheet is a stack of numbered panels. Each panel's title carries its legend, the way every board's sketch did
("1. THE BOARD - the number on each piece is its floor height; dots: build zones; ..."), so the picture explains
itself. Three kinds of panel:

    MapPanel      the board from above, in world coordinates: a plan raster filled by kind and hillshaded, or a
                  built world's top-down; then places, heights, markers, routes, zones and callouts over it
    SectionPanel  a true-scale cut, along x or z or unrolled along any polyline: the ground, bands for rooms and
                  water, levels such as the kill height, and callouts with leader lines
    TablePanel    the checker's measurements, each against its target, marked where it misses

    sheet = Sheet("Islets - the plan")
    m = sheet.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=8, title="THE BOARD",
                  legend="the number on each piece is its floor height; A the hill; S spawns")
    m.raster(R, COLOURS)                               # the image half of R.symmetry drawn paler
    m.heights(R)                                       # every piece's floor height
    m.marker(0, 0, "A", TEAM["neutral"])
    m.place(-22, -8, "Red's island")
    m.route(path, TEAM["red"], arrow=True)
    sheet.row(s1, s2)                                  # two sections side by side
    sheet.table([("22.4", "red to the hill", "at most 30", True), ...])
    sheet.save("renders/00-plan-sketch.png")

The annotated top-down of a built world is a MapPanel over `built(w)`: the plan's names and markers drawn on what
was built, to show it landed where the plan said.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import blocks as K

PAPER = (246, 244, 238)
INK = (24, 26, 30)
FAINT = (120, 124, 130)
HALO = (255, 255, 255)
TEAM = {"red": (200, 40, 40), "blue": (40, 80, 200), "neutral": (200, 150, 30), "green": (40, 150, 60),
        "yellow": (220, 180, 30)}
EMPTY = ("void", "gap")                         # kinds that are nothing: no shading, no height, no section
_FONTS = {}


def font(size=12):
    if size not in _FONTS:
        _FONTS[size] = ImageFont.load_default(size=size)
    return _FONTS[size]


def pale(c, k=0.45):
    """A colour washed toward white: the mirrored half of a symmetric board."""
    return tuple(int(v + (255 - v) * k) for v in c)


def dark(c, k=0.35):
    return tuple(int(v * (1 - k)) for v in c)


def _text(d, xy, s, fill=INK, size=12, halo=HALO, anchor="mm"):
    if halo is not None:
        d.text(xy, s, fill=fill, font=font(size), anchor=anchor, stroke_width=2, stroke_fill=halo)
    else:
        d.text(xy, s, fill=fill, font=font(size), anchor=anchor)


def _dashed(d, pts, fill, width, dash=6, gap=4):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        s = 0.0
        while s < L:
            e = min(L, s + dash)
            d.line([(ax + (bx - ax) * s / L, ay + (by - ay) * s / L), (ax + (bx - ax) * e / L, ay + (by - ay) * e / L)],
                   fill=fill, width=width)
            s = e + gap


def _arrowhead(d, a, b, fill, size=7):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - size * math.cos(ang - 0.45), b[1] - size * math.sin(ang - 0.45))
    p2 = (b[0] - size * math.cos(ang + 0.45), b[1] - size * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=fill)


class Panel:
    title = ""
    legend = ""

    def heading(self, n):
        t = f"{n}. {self.title}" if self.title else f"{n}."
        return t + (f"  -  {self.legend}" if self.legend else "")


# ---- the board from above ---------------------------------------------------------------------------------
class MapPanel(Panel):
    """A panel over world x, z: one block is `scale` pixels."""

    def __init__(self, x0, z0, x1, z1, scale=5, title="", legend="", bg=(40, 44, 56), symmetry=None):
        self.x0, self.z0, self.x1, self.z1, self.s = x0, z0, x1, z1, scale
        self.title, self.legend = title, legend
        self.img = Image.new("RGB", ((x1 - x0 + 1) * scale, (z1 - z0 + 1) * scale), bg)
        self.d = ImageDraw.Draw(self.img)
        self.symmetry = symmetry                                  # what both=True draws the image through

    def px(self, x, z):
        return ((x - self.x0 + 0.5) * self.s, (z - self.z0 + 0.5) * self.s)

    def _images(self, pts, both):
        out = [(list(pts), False)]
        if both and self.symmetry:
            out.append(([self.symmetry.point(*p) if len(p) == 2 else (*self.symmetry.point(p[0], p[1]), *p[2:])
                         for p in pts], True))
        return out

    # backgrounds
    def raster(self, R, colours, shade=True, symmetry=None, image_half=None, edges=True):
        """Each column in its kind's colour, lit from the north-west by height so steps read; with a symmetry, the
        image half (image_half(x, z) -> True, default x >= 0) washed paler, as every board drew blue's half."""
        self.symmetry = symmetry or R.symmetry
        H = R.H.astype(float)
        empty = np.isin(R.K, [R.kinds[k] for k in EMPTY if k in R.kinds])
        gx = np.zeros_like(H); gz = np.zeros_like(H)
        gx[1:, :] = np.where(empty[1:, :] | empty[:-1, :], 0, H[1:, :] - H[:-1, :])   # no light off the void's edge
        gz[:, 1:] = np.where(empty[:, 1:] | empty[:, :-1], 0, H[:, 1:] - H[:, :-1])
        light = np.clip(1.0 + 0.08 * (gx + gz), 0.6, 1.25) if shade else np.ones_like(H)
        half = image_half or (lambda x, z: x >= 0)
        s = self.s
        for i in range(R.nx):
            for j in range(R.nz):
                x, z = R.x_min + i, R.z_min + j
                if not (self.x0 <= x <= self.x1 and self.z0 <= z <= self.z1):
                    continue
                c = colours.get(R.names[int(R.K[i, j])], (255, 0, 255))
                c = tuple(int(max(0, min(255, v * light[i, j]))) for v in c)
                if self.symmetry and half(x, z) and not empty[i, j]:
                    c = pale(c, 0.3)
                a, b = (x - self.x0) * s, (z - self.z0) * s
                self.d.rectangle([a, b, a + s - 1, b + s - 1], fill=c)
        if edges:                                                 # a dark line where the floor height changes
            for i in range(R.nx):
                for j in range(R.nz):
                    x, z = R.x_min + i, R.z_min + j
                    a, b = (x - self.x0) * s, (z - self.z0) * s
                    if i + 1 < R.nx and (H[i, j] != H[i + 1, j] or R.K[i, j] != R.K[i + 1, j]):
                        self.d.line([(a + s - 1, b), (a + s - 1, b + s - 1)], fill=(30, 30, 34))
                    if j + 1 < R.nz and (H[i, j] != H[i, j + 1] or R.K[i, j] != R.K[i, j + 1]):
                        self.d.line([(a, b + s - 1), (a + s - 1, b + s - 1)], fill=(30, 30, 34))
        for (x, z), rises in R.stair.items():                     # a tick on every stair toward its top
            if self.x0 <= x <= self.x1 and self.z0 <= z <= self.z1:
                cx, cz = self.px(x, z)
                dx, dz = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}[rises]
                self.d.line([(cx - dx * s * 0.3, cz - dz * s * 0.3), (cx + dx * s * 0.35, cz + dz * s * 0.35)],
                            fill=(60, 50, 40), width=max(1, s // 5))
        return self

    def built(self, w, ymin=0, ymax=None):
        """A built world's top-down: the highest block of every column in the studio's colour, lit by height,
        the void left dark."""
        ids, dat = w.ids, w.dat
        if ymax is not None:
            ids = ids[:, :ymax + 1, :]
        see = K.mask(ids, (K.PASSABLE - {K.B.WATER, K.B.WATER_FLOW}) | {36})
        solid = ~see
        solid[:, :ymin, :] = False
        has = solid.any(axis=1)
        top = ids.shape[1] - 1 - np.argmax(solid[:, ::-1, :], axis=1)
        s = self.s
        H = np.where(has, top, 0).astype(float)
        gx = np.zeros_like(H); gz = np.zeros_like(H)
        gx[1:, :] = H[1:, :] - H[:-1, :]
        gz[:, 1:] = H[:, 1:] - H[:, :-1]
        light = np.clip(1.0 + 0.05 * (gx + gz), 0.65, 1.2)
        for x in range(self.x0, self.x1 + 1):
            for z in range(self.z0, self.z1 + 1):
                i, k = x - w.x0, z - w.z0
                if not (0 <= i < w.sx and 0 <= k < w.sz) or not has[i, k]:
                    continue
                y = top[i, k]
                c = K.COLOURS[int(ids[i, y, k]), int(dat[i, y, k]) & 15].astype(float) * light[i, k]
                a, b = (x - self.x0) * s, (z - self.z0) * s
                self.d.rectangle([a, b, a + s - 1, b + s - 1], fill=tuple(int(min(255, v)) for v in c))
        return self

    def dim(self, k=0.55, toward=(40, 44, 56)):
        """Wash the whole panel toward a dark tone, so the routes or zones drawn next stand out on it."""
        over = Image.new("RGB", self.img.size, toward)
        self.img = Image.blend(self.img, over, k)
        self.d = ImageDraw.Draw(self.img)
        return self

    # shapes
    def poly(self, pts, fill=None, outline=INK, width=1, both=False):
        for p, image in self._images(pts, both):
            self.d.polygon([self.px(x, z) for x, z in p], fill=pale(fill) if image and fill else fill,
                           outline=outline, width=width)

    def ghost(self, pts, colour=(150, 150, 160), both=False):
        """A faint outline: what lies above or below this panel's level, for orientation."""
        for p, _ in self._images(pts, both):
            q = [self.px(x, z) for x, z in p]
            self.d.line(q + q[:1], fill=colour, width=1)

    def rect(self, x0, z0, x1, z1, fill=None, outline=INK, width=1, both=False):
        self.poly([(x0, z0), (x1 + 1, z0), (x1 + 1, z1 + 1), (x0, z1 + 1)], fill, outline, width, both)

    def zone(self, mask_or_pts, colour=(230, 200, 60), style="dots", step=4, both=False):
        """Mark a zone without hiding what is under it: dots or diagonal hatching over a mask of the panel's
        columns, or a polygon."""
        if isinstance(mask_or_pts, np.ndarray):
            cells = [(self.x0 + i, self.z0 + k) for i, k in np.argwhere(mask_or_pts)]
        else:
            from .shapes import inside
            X, Z = np.meshgrid(np.arange(self.x0, self.x1 + 1), np.arange(self.z0, self.z1 + 1), indexing="ij")
            cells = []
            for p, _ in self._images(mask_or_pts, both):
                cells += [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(inside(X, Z, p))]
        s = self.s
        for x, z in cells:
            a, b = (x - self.x0) * s, (z - self.z0) * s
            if style == "dots":
                if (x + z) % max(1, step // 2) == 0:
                    self.d.ellipse([a + s / 2 - 1, b + s / 2 - 1, a + s / 2 + 1, b + s / 2 + 1], fill=colour)
            else:
                if (x - z) % step == 0:
                    self.d.line([(a, b + s - 1), (a + s - 1, b)], fill=colour)

    # lines
    def line(self, pts, colour=INK, width=2, dash=False, arrow=False, both=False):
        for p, image in self._images(pts, both):
            q = [self.px(*pp[:2]) for pp in p]
            c = pale(colour) if image else colour
            if dash:
                _dashed(self.d, q, c, width)
            else:
                self.d.line(q, fill=c, width=width, joint="curve")
            if arrow and len(q) > 1:
                _arrowhead(self.d, q[-2], q[-1], c, size=4 + 2 * width)

    def route(self, cells, colour=TEAM["red"], width=3, arrow=True, both=False):
        """A route from the checker (a list of (x, z) cells, start first), smoothed to its corners."""
        if len(cells) < 2:
            return
        keep = [cells[0]]
        for a, b, c in zip(cells, cells[1:], cells[2:]):
            if (b[0] - a[0], b[1] - a[1]) != (c[0] - b[0], c[1] - b[1]):
                keep.append(b)
        keep.append(cells[-1])
        self.line(keep, colour, width, arrow=arrow, both=both)

    def jumps(self, jumps, colour=(60, 120, 220), R=None, gaps=True):
        """Dashed lines for jumps ((x, z), (x, z), gap), each pair once. Given the raster, only the shortest jump
        between each two pieces is drawn, with its gap written on it: a board allows hundreds of jumps and the
        review needs to see which pieces they join."""
        if R is not None:
            from scipy import ndimage
            lab, _ = ndimage.label(~np.isin(R.K, [R.kinds[k] for k in EMPTY if k in R.kinds]))
            best = {}
            for a, b, g in jumps:
                pa, pb = lab[R.ix(a[0]), R.iz(a[1])], lab[R.ix(b[0]), R.iz(b[1])]
                if pa == pb:
                    continue
                key = (min(pa, pb), max(pa, pb))
                if key not in best or g < best[key][2]:
                    best[key] = (a, b, g)
            jumps = list(best.values())
        seen = set()
        for a, b, g in jumps:
            key = tuple(sorted((a, b)))
            if key in seen:
                continue
            seen.add(key)
            pa, pb = self.px(*a), self.px(*b)
            _dashed(self.d, [pa, pb], colour, 2 if R is not None else 1, 4, 3)
            if R is not None and gaps:
                _text(self.d, ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 - 8), f"{g:g}", colour, 10)

    # words and marks
    def label(self, x, z, text, colour=INK, size=12, halo=HALO, anchor="mm", both=False):
        for p, image in self._images([(x, z)], both):
            _text(self.d, self.px(*p[0]), text, pale(colour, 0.3) if image else colour, size, halo, anchor)

    def place(self, x, z, name, colour=INK, size=13, both=False):
        """A place's name, larger, centred on it."""
        self.label(x, z, name, colour, size, HALO, "mm", both)

    def heights(self, R, kinds=None, min_cells=3, colour=(30, 30, 30), size=11, both=True):
        """The floor height written on every piece: each connected run of one kind at one height, at the cell
        nearest its middle, once per piece."""
        from scipy import ndimage
        seen = np.zeros(R.H.shape, bool)
        names = kinds or [k for k in R.kinds if k not in EMPTY + ("wall",)]
        half = (lambda x, z: x >= 0)
        for k in names:
            km = R.K == R.kinds[k]
            for h in np.unique(R.H[km]):
                lab, n = ndimage.label(km & (R.H == h))
                for j in range(1, n + 1):
                    cells = np.argwhere(lab == j)
                    if len(cells) < min_cells:
                        continue
                    ci, ck = cells.mean(axis=0)
                    best = cells[np.argmin((cells[:, 0] - ci) ** 2 + (cells[:, 1] - ck) ** 2)]
                    x, z = R.x_min + int(best[0]), R.z_min + int(best[1])
                    if not both and R.symmetry and half(x, z):
                        continue
                    seen[best[0], best[1]] = True
                    self.label(x, z, str(int(h)), colour, size)

    def numbers(self, pts, colour=(90, 40, 0), size=10, dx=1, dz=-1):
        """Small numbers beside points (x, z, n): the height a route is graded to at each bend, a step count."""
        for x, z, n in pts:
            self.label(x + dx, z + dz, str(n), colour, size)

    def marker(self, x, z, text, colour=TEAM["red"], r=None, both=False):
        """A disc in a team's colour with a letter or number on it: an objective, a spawn, a stage."""
        r = r or max(6, int(self.s * 1.4))
        for p, image in self._images([(x, z)], both):
            cx, cz = self.px(*p[0])
            col = colour if not image else (TEAM["blue"] if colour == TEAM["red"] else pale(colour, 0.2))
            self.d.ellipse([cx - r, cz - r, cx + r, cz + r], fill=col, outline=HALO, width=2)
            _text(self.d, (cx, cz), text, HALO, max(10, int(r * 1.2)), None)

    def callout(self, x, z, text, dx=30, dz=-24, colour=INK, size=11):
        """A label set off from its point by a leader line: for a detail too small to write on."""
        cx, cz = self.px(x, z)
        tx, tz = cx + dx, cz + dz
        self.d.line([(cx, cz), (tx, tz)], fill=colour, width=1)
        self.d.ellipse([cx - 2, cz - 2, cx + 2, cz + 2], fill=colour)
        _text(self.d, (tx + (3 if dx >= 0 else -3), tz), text, colour, size, HALO, "lm" if dx >= 0 else "rm")


# ---- true-scale sections ----------------------------------------------------------------------------------
class SectionPanel(Panel):
    """A cut in elevation, true scale: s runs along the cut (blocks), y up; one block is `scale` pixels."""

    def __init__(self, s0, s1, y0, y1, scale=4, title="", legend="", sky=(205, 222, 236)):
        self.s0, self.s1, self.y0, self.y1, self.sc = s0, s1, y0, y1, scale
        self.title, self.legend = title, legend
        self.img = Image.new("RGB", ((s1 - s0 + 1) * scale + 34, (y1 - y0 + 1) * scale), sky)
        self.d = ImageDraw.Draw(self.img)
        for y in range(y0 - y0 % 10 + 10 if y0 % 10 else y0, y1 + 1, 10):   # a height scale every ten
            yy = self.py(y)
            self.d.line([(self.img.width - 34, yy), (self.img.width - 28, yy)], fill=FAINT)
            _text(self.d, (self.img.width - 4, yy), str(y), FAINT, 10, None, "rm")

    def px(self, s):
        return (s - self.s0) * self.sc

    def py(self, y):
        return (self.y1 - y) * self.sc

    def raster(self, R, axis="x", at=0, colours=None, symmetry_pale=False):
        """The raster's columns along x (at z = at) or along z (at x = at), each solid from its floor down."""
        rng = range(max(self.s0, R.x_min if axis == "x" else R.z_min), min(self.s1, R.x_max if axis == "x" else R.z_max) + 1)
        for s in rng:
            x, z = (s, at) if axis == "x" else (at, s)
            h, kind = R.at(x, z)
            if h is None or h < self.y0 or kind in EMPTY:
                continue
            c = (colours or {}).get(kind, (170, 160, 140))
            self.d.rectangle([self.px(s), self.py(h), self.px(s + 1) - 1, self.img.height - 1], fill=c)
        return self

    def along(self, R, pts, colours=None, step=0.5):
        """The raster unrolled along a polyline: s is the distance along it."""
        L = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
        total = sum(L)
        k, s = 0, 0.0
        while s <= total:
            seg, acc = 0, 0.0
            while seg < len(L) - 1 and acc + L[seg] < s:
                acc += L[seg]
                seg += 1
            t = (s - acc) / L[seg] if L[seg] else 0
            (ax, az), (bx, bz) = pts[seg], pts[seg + 1]
            x, z = math.floor(ax + (bx - ax) * t), math.floor(az + (bz - az) * t)
            h, kind = R.at(x, z)
            if h is not None and kind not in EMPTY and h >= self.y0:
                c = (colours or {}).get(kind, (170, 160, 140))
                self.d.rectangle([self.px(self.s0 + s), self.py(h), self.px(self.s0 + s + step), self.img.height - 1], fill=c)
            s += step
        return self

    def profile(self, pts, fill=(140, 125, 105), outline=(60, 50, 40)):
        """Ground as a profile of (s, y) points, filled down to the bottom."""
        q = [(self.px(s), self.py(y)) for s, y in pts]
        q += [(q[-1][0], self.img.height), (q[0][0], self.img.height)]
        self.d.polygon(q, fill=fill, outline=outline)

    def band(self, s0, s1, y0, y1, fill=(60, 55, 50), outline=None, text=None, colour=HALO):
        """A rectangle in the cut: a room, a cavern, water, a building."""
        self.d.rectangle([self.px(s0), self.py(y1), self.px(s1) - 1, self.py(y0) - 1], fill=fill, outline=outline)
        if text:
            _text(self.d, ((self.px(s0) + self.px(s1)) / 2, (self.py(y0) + self.py(y1)) / 2), text, colour, 10, None)

    def level(self, y, text="", colour=(210, 50, 40), dash=False):
        """A line across the whole cut at height y: the kill height, the water, a build limit."""
        yy = self.py(y)
        w = self.img.width - 34
        if dash:
            _dashed(self.d, [(0, yy), (w, yy)], colour, 1)
        else:
            self.d.line([(0, yy), (w, yy)], fill=colour, width=1)
        if text:
            _text(self.d, (4, yy - 7), text, colour, 11, HALO, "lm")

    def callout(self, s, y, text, dx=20, dy=-18, colour=INK, size=11):
        cx, cy = self.px(s), self.py(y)
        tx, ty = cx + dx, cy + dy
        self.d.line([(cx, cy), (tx, ty)], fill=colour, width=1)
        self.d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=colour)
        _text(self.d, (tx + (3 if dx >= 0 else -3), ty), text, colour, size, HALO, "lm" if dx >= 0 else "rm")

    def label(self, s, y, text, colour=INK, size=11):
        _text(self.d, (self.px(s), self.py(y)), text, colour, size, HALO, "mm")


# ---- the checker's numbers ------------------------------------------------------------------------------
class TablePanel(Panel):
    """Measurements against their targets: rows of (value, what, target, ok); ok None for a plain line. A row
    that misses its target is drawn in red, so the review sees it first."""

    def __init__(self, rows, title="THE CHECK", legend="each measurement with its target", width=None):
        self.title, self.legend = title, legend
        rows = list(rows)
        w = width or 760
        self.img = Image.new("RGB", (w, 20 * len(rows) + 14), (30, 33, 40))
        d = ImageDraw.Draw(self.img)
        for k, row in enumerate(rows):
            if isinstance(row, str):
                row = ("", row, "", None)
            value, what, target, ok = (list(row) + [None] * 4)[:4]
            y = 10 + 20 * k
            col = (235, 235, 235) if ok is None else (120, 210, 130) if ok else (240, 110, 100)
            _text(d, (110, y), str(value), col, 12, None, "rm")
            _text(d, (124, y), str(what), (235, 235, 235), 12, None, "lm")
            if target:
                _text(d, (w - 12, y), str(target), (160, 165, 175), 11, None, "rm")


# ---- the sheet --------------------------------------------------------------------------------------------
class Sheet:
    def __init__(self, title="", pad=16):
        self.title, self.pad = title, pad
        self.rows = []

    def map(self, *a, **k):
        p = MapPanel(*a, **k)
        self.rows.append([p])
        return p

    def section(self, *a, **k):
        p = SectionPanel(*a, **k)
        self.rows.append([p])
        return p

    def table(self, rows, **k):
        p = TablePanel(rows, **k)
        self.rows.append([p])
        return p

    def add(self, panel):
        self.rows.append([panel])
        return panel

    def row(self, *panels):
        """Panels side by side, numbered 3a, 3b, ..."""
        self.rows.append(list(panels))

    def save(self, path):
        pad = self.pad
        head = 34
        title_h = 22
        f = font(12)
        widths = [sum(max(p.img.width, f.getlength(p.heading("0a")) + 4) for p in r) + pad * (len(r) - 1)
                  for r in self.rows]
        width = int(max(widths + [400])) + 2 * pad
        height = head + sum(max(p.img.height for p in r) + title_h + pad for r in self.rows) + pad
        out = Image.new("RGB", (width, height), PAPER)
        d = ImageDraw.Draw(out)
        _text(d, (pad, 18), self.title, INK, 16, None, "lm")
        y = head
        for n, r in enumerate(self.rows, 1):
            x = pad
            for k, p in enumerate(r):
                num = f"{n}{'abcdefgh'[k]}" if len(r) > 1 else str(n)
                _text(d, (x, y + 9), p.heading(num), INK, 12, None, "lm")
                out.paste(p.img, (x, y + title_h))
                x += int(max(p.img.width, f.getlength(p.heading("0a")) + 4)) + pad
            y += max(p.img.height for p in r) + title_h + pad
        out.save(path)
        return path
