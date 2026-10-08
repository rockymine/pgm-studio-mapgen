"""The sketch of a plan, drawn before anything is built: the board from above, true-scale sections through it,
routes and jumps over it, and the checker's own numbers beside it, so the review reads the same board the
checker measured.

    S = Sketch(title="Calcite — the plan")
    S.board(R, colours={"floor": (200, 196, 180), ...}, scale=5)      # panel 1: from above, hillshaded
    S.routes(R, [cells, ...], colour)                                 # drawn over the last board
    S.section(R, axis="x", at=0, y_range=(8, 30))                     # a true-scale cut
    S.text(lines)                                                     # the checker's numbers
    S.save(path)

Panels stack top to bottom in the order they are added; each is titled, and every scale is true, a block a
block, so a section shows the real steepness of a climb.
"""
import numpy as np
from PIL import Image, ImageDraw

BG = (30, 32, 40)
_PLAIN = {"\u2014": " - ", "\u2013": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00d7": "x"}


def plain(s):
    """The default bitmap font draws Latin-1 only: dashes, curly quotes and the times sign become plain ones."""
    for a, b in _PLAIN.items():
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")
INK = (235, 235, 235)
DIM = (150, 155, 165)


class Sketch:
    def __init__(self, title="", width=None):
        self.title = title
        self.panels = []                                          # (image, title)
        self.width = width
        self._last = None

    # --- the board from above ------------------------------------------------------------------------
    def board(self, R, colours, scale=5, title="from above", shade=True, labels=None):
        """Each column in its kind's colour, lit from the north-west by the height, so steps and drops read."""
        img = Image.new("RGB", (R.nx * scale, R.nz * scale), BG)
        d = ImageDraw.Draw(img)
        H = R.H.astype(float)
        if shade:
            gx = np.zeros_like(H); gz = np.zeros_like(H)
            gx[1:, :] = H[1:, :] - H[:-1, :]
            gz[:, 1:] = H[:, 1:] - H[:, :-1]
            light = np.clip(1.0 + 0.09 * (gx + gz), 0.55, 1.25)
        hmin, hmax = H.min(), max(H.max(), H.min() + 1)
        for i in range(R.nx):
            for j in range(R.nz):
                c = colours.get(R.names[int(R.K[i, j])], (255, 0, 255))
                k = (0.8 + 0.2 * (H[i, j] - hmin) / (hmax - hmin)) * (light[i, j] if shade else 1.0)
                c = tuple(int(max(0, min(255, v * k))) for v in c)
                d.rectangle([i * scale, j * scale, (i + 1) * scale - 1, (j + 1) * scale - 1], fill=c)
        for (x, z), rises in R.stair.items():                     # a tick on every stair toward its top
            if R.inside(x, z):
                cx, cz = (R.ix(x) + 0.5) * scale, (R.iz(z) + 0.5) * scale
                dx, dz = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}[rises]
                d.line([(cx, cz), (cx + dx * scale * 0.4, cz + dz * scale * 0.4)], fill=(40, 40, 40))
        for text, (x, z) in (labels or {}).items():
            d.text((R.ix(x) * scale + 2, R.iz(z) * scale + 2), text, fill=(20, 20, 20))
        self.panels.append((img, title))
        self._last = (img, R, scale)
        return img

    def routes(self, R, paths, colour=(220, 60, 60), width=2):
        """Lines along routes (lists of (x, z) cells) over the last board."""
        img, R0, scale = self._last
        d = ImageDraw.Draw(img)
        for p in paths:
            pts = [((R.ix(x) + 0.5) * scale, (R.iz(z) + 0.5) * scale) for x, z in p]
            if len(pts) > 1:
                d.line(pts, fill=colour, width=width)

    def jumps(self, R, jumps, colour=(60, 120, 220)):
        """Dashed arcs for jumps ((x, z), (x, z), gap) over the last board."""
        img, R0, scale = self._last
        d = ImageDraw.Draw(img)
        for a, b, g in jumps:
            ax, az = (R.ix(a[0]) + 0.5) * scale, (R.iz(a[1]) + 0.5) * scale
            bx, bz = (R.ix(b[0]) + 0.5) * scale, (R.iz(b[1]) + 0.5) * scale
            for s in range(0, 10, 2):
                t0, t1 = s / 10, (s + 1) / 10
                d.line([(ax + (bx - ax) * t0, az + (bz - az) * t0), (ax + (bx - ax) * t1, az + (bz - az) * t1)],
                       fill=colour, width=1)

    # --- true-scale sections -------------------------------------------------------------------------
    def section(self, R, axis="x", at=0, y_range=None, scale=5, title=None, colours=None, marks=()):
        """A cut through the raster along x (at z = at) or along z (at x = at), true scale: each column drawn
        solid up to its floor. marks are (position, y, label) drawn as ticks, e.g. a kill height."""
        if axis == "x":
            cols = [(x, R.h(x, at), R.kind(x, at)) for x in range(R.x_min, R.x_max + 1)]
        else:
            cols = [(z, R.h(at, z), R.kind(at, z)) for z in range(R.z_min, R.z_max + 1)]
        y0, y1 = y_range or (min(c[1] for c in cols) - 3, max(c[1] for c in cols) + 4)
        img = Image.new("RGB", (len(cols) * scale, (y1 - y0 + 1) * scale), BG)
        d = ImageDraw.Draw(img)
        for k, (p, h, kind) in enumerate(cols):
            if h < y0:
                continue                                         # a column below the range: nothing to draw
            c = (colours or {}).get(kind, (180, 175, 160))
            top = max(0, (y1 - h) * scale)
            d.rectangle([k * scale, top, (k + 1) * scale - 1, img.height - 1], fill=c)
        for y in range(y0, y1 + 1, 5):                           # a height scale every five
            yy = (y1 - y) * scale
            d.line([(0, yy), (6, yy)], fill=DIM)
            d.text((8, yy - 6), str(y), fill=DIM)
        for p, y, label in marks:
            yy = (y1 - y) * scale
            d.line([(0, yy), (img.width, yy)], fill=(220, 70, 60))
            d.text((img.width - 8 * len(label) - 4, yy - 12), label, fill=(220, 70, 60))
        name = title or (f"section along x at z {at}" if axis == "x" else f"section along z at x {at}")
        self.panels.append((img, name + ", true scale"))
        return img

    # --- words ----------------------------------------------------------------------------------------
    def text(self, lines, title="the check"):
        lines = list(lines)
        w = max([len(s) for s in lines] + [20]) * 7 + 20
        img = Image.new("RGB", (w, 18 * len(lines) + 12), BG)
        d = ImageDraw.Draw(img)
        for k, s in enumerate(lines):
            d.text((10, 6 + 18 * k), plain(s), fill=INK)
        self.panels.append((img, title))
        return img

    def image(self, img, title=""):
        self.panels.append((img, title))

    def save(self, path, pad=20):
        width = self.width or max(p[0].width for p in self.panels) + 2 * pad
        height = 40 + sum(p[0].height + 30 for p in self.panels) + pad
        out = Image.new("RGB", (width, height), BG)
        d = ImageDraw.Draw(out)
        d.text((pad, 12), plain(self.title), fill=INK)
        y = 40
        for img, title in self.panels:
            d.text((pad, y), plain(title), fill=DIM)
            out.paste(img, (pad, y + 16))
            y += img.height + 30
        out.save(path)
        return path
