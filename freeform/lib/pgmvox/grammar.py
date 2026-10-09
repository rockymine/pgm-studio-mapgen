"""A grammar for structural boards: surfaces cut into rectangular sections, each outlined and filled by rule, and
every face where the ground falls away dressed in courses by rule. The rules are the grammar; the blocks they lay
are a Style, so one board's plan can be spoken in more than one style, and one style over many boards.

    secs = grammar.split((x0, z0, x1, z1), 3, 2, y=20, name="forecourt")     # a box cut into sections
    g = grammar.Ground(secs, tops=stairs)            # every column's top, its section and its depth in it
    grammar.lay(w, g, STYLE, rng=rng)                # the ground under, the faces, the outlines, the fills

What the grammar reads, for every column of a section:

    depth       blocks in from its section's edge: 0 is the outline, 1 the fill's first ring
    drop        how far the ground falls beside it, on its lowest side; a face is laid where it falls two or more
    along, pos  which bay of the face it stands in, counted on the style's module from the world's origin, and where
                in the bay: an accent is laid every so many bays, only where enough air lies beside it

What a Style answers:

    body        what lies under a surface: courses of stone, bedrock to the floor, the build marker
    faces       the courses of a face, top down, from the rim at the surface; its accent bay and the air it needs
    seam        the outline where a section meets anything but a drop: another section, a wall, a stair's head
    fills       recipes that lay a section's inside, tried in the order the style's chooser gives
    motifs      marks laid into a fill afterwards: an arrow, a disc, a team's sign

A section is a set of boxes, usually one: a rectangle. A section that is no rectangle still works, but the fills
that need one (rings, beds, squares) decline it, and the chooser's next fill is tried.
"""
from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage

from .blocks import B

DIRS = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}


# ---- sections ------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Section:
    """A piece of surface at one height: boxes (x0, z0, x1, z1) inclusive, in blocks. `fill` names the recipe to
    lay inside it, or None for the style's choice; `tags` are free words a style's rules may read (front, back,
    team, lane ...); `motifs` are marks laid over the fill: (name, params)."""
    boxes: tuple
    y: int
    name: str = None
    fill: str = None
    tags: frozenset = frozenset()
    motifs: tuple = ()

    @property
    def box(self):
        xs = [b[0] for b in self.boxes] + [b[2] for b in self.boxes]
        zs = [b[1] for b in self.boxes] + [b[3] for b in self.boxes]
        return min(xs), min(zs), max(xs), max(zs)

    def columns(self):
        out = []
        for x0, z0, x1, z1 in self.boxes:
            out += [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
        return out

    @property
    def is_rect(self):
        x0, z0, x1, z1 = self.box
        return len(set(self.columns())) == (x1 - x0 + 1) * (z1 - z0 + 1)


def _cuts(lo, hi, n):
    """Cut lo..hi into n runs as near equal as can be, the longer ones first: [(a, b), ...] inclusive."""
    size = hi - lo + 1
    q, r = divmod(size, n)
    out, a = [], lo
    for i in range(n):
        b = a + q + (1 if i < r else 0) - 1
        out.append((a, b))
        a = b + 1
    return out


def split(box, nx, nz, y, name="section", **kw):
    """A box cut into nx by nz sections as near equal as the blocks allow, named name-i-j."""
    x0, z0, x1, z1 = box
    return [Section(((a, c, b, d),), y, f"{name}-{i}-{j}", **kw)
            for i, (a, b) in enumerate(_cuts(x0, x1, nx)) for j, (c, d) in enumerate(_cuts(z0, z1, nz))]


def tile(box, module, y, name="section", **kw):
    """A box cut into squares `module` a side, counted from its low corner; the last row and column take what is
    left over, so no section is narrower than half a module."""
    x0, z0, x1, z1 = box
    nx = max(1, round((x1 - x0 + 1) / module))
    nz = max(1, round((z1 - z0 + 1) / module))
    return split(box, nx, nz, y, name, **kw)


# ---- the ground the sections make ------------------------------------------------------------------------------
class Ground:
    """Every column's top, the section it belongs to and its depth in that section. `tops` adds columns that are
    land but in no section (a stair, a deck's edge): {(x, z): top}."""

    def __init__(self, sections, tops=None):
        self.sections = list(sections)
        self.T = dict(tops or {})
        self.owner = {}
        for n, s in enumerate(self.sections):
            for c in s.columns():
                self.T[c] = s.y
                self.owner[c] = n
        self._depth = {}
        for n, s in enumerate(self.sections):
            x0, z0, x1, z1 = s.box
            m = np.zeros((x1 - x0 + 3, z1 - z0 + 3), bool)
            for x, z in s.columns():
                m[x - x0 + 1, z - z0 + 1] = True
            d = ndimage.distance_transform_cdt(m, metric="chessboard") - 1
            self._depth[n] = (x0 - 1, z0 - 1, d)

    def top(self, x, z):
        return self.T.get((x, z), -1)

    def depth(self, x, z):
        n = self.owner[(x, z)]
        bx, bz, d = self._depth[n]
        return int(d[x - bx, z - bz])

    def falls(self, x, z, by=2):
        """The sides on which the ground beside falls `by` or more: [(side, drop), ...] in the order e w s n."""
        h = self.top(x, z)
        return [(d, h - self.top(x + dx, z + dz)) for d, (dx, dz) in DIRS.items()
                if self.top(x + dx, z + dz) <= h - by]

    def inside(self, n, at=1):
        """A section's columns `at` or more in from its edge."""
        return [c for c in self.sections[n].columns() if self.depth(*c) >= at]


# ---- faces ---------------------------------------------------------------------------------------------------
def spec(s, inward):
    """A course: (id, data), or a function of the face's inward side giving one."""
    return s(inward) if callable(s) else s


@dataclass
class Accent:
    """A bay laid instead of the plain courses every `every` bays of `module` along a face, starting at bay `phase`:
    its two end columns are `frame`, its middle `inner`, each top down from the rim. It is laid only where `min_air`
    blocks of air lie beside, so a shallow face never shows half of one."""
    module: int
    frame: list
    inner: list
    every: int = 2
    phase: int = 0
    min_air: int = 5


@dataclass
class Face:
    """The courses of a face, top down from the rim at the surface. `floor` is the lowest y a course may reach."""
    courses: list
    accent: Accent = None
    floor: int = 3

    def lay(self, w, x, z, h, inward, along=None, pos=None, air=0, accents=True):
        if h - len(self.courses) + 1 < self.floor:
            raise ValueError(f"a face at {h} reaches under y {self.floor}: raise the floor")
        a = self.accent
        stack = self.courses
        if accents and a and along is not None and along % a.every == a.phase and air >= a.min_air:
            stack = a.frame if pos in (0, a.module - 1) else a.inner
        for i, s in enumerate(stack):
            w.set(x, h - i, z, *spec(s, inward))

    def bay(self, x, z, side):
        """Which bay of the face a column stands in, and where in it: (along, pos)."""
        m = self.accent.module if self.accent else 1
        c = z if side in ("e", "w") else x
        return c // m, c % m


# ---- lots: what a fill is handed ---------------------------------------------------------------------------------
@dataclass
class Lot:
    """A section's inside as a fill sees it: its columns from depth 1, their box, its surface, the section, the
    ground and the style's free parameters (a team's dye ...)."""
    section: Section
    index: int
    cols: list
    y: int
    ground: Ground
    params: dict = field(default_factory=dict)

    @property
    def box(self):
        xs = [c[0] for c in self.cols]
        zs = [c[1] for c in self.cols]
        return min(xs), min(zs), max(xs), max(zs)

    @property
    def is_rect(self):
        """A rectangle, and the whole of its section's inside (not one team's part of a section that crosses)."""
        x0, z0, x1, z1 = self.box
        return self.section.is_rect and len(self.cols) == (x1 - x0 + 1) * (z1 - z0 + 1) == \
            len(self.ground.inside(self.index))

    @property
    def size(self):
        x0, z0, x1, z1 = self.box
        return x1 - x0 + 1, z1 - z0 + 1


# ---- styles ------------------------------------------------------------------------------------------------------
@dataclass
class Style:
    """The blocks a grammar is spoken in. `body(w, x, z, h)` lays what is under a surface; `faces` are named, "edge"
    the one laid where the ground falls; `seam` is the outline against anything but a fall; `fills` are named
    recipes fill(w, lot, rng) -> True when laid, False to decline; `choose(section, lot)` gives the names to try in
    order; `motifs` are named marks motif(w, lot, rng, **params)."""
    name: str
    body: object
    faces: dict
    seam: tuple
    fills: dict
    choose: object
    motifs: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)

    def fill(self, w, lot, rng):
        names = ([lot.section.fill] if lot.section.fill else []) + list(self.choose(lot.section, lot))
        for name in names:
            if self.fills[name](w, lot, rng):
                return name
        return None


def lay(w, ground, style, only=None, rng=None, face_of=None, params=None, where=None, bodiless=()):
    """Lay the sections of `ground` numbered in `only` (default all) in `style`: the body under every column, a face
    where the ground falls two or more (the rim its top course), the seam on the rest of the outline, then each
    section's fill and motifs. face_of(x, z) may name another of the style's faces for a column, or None to leave
    its face alone; where(x, z) limits the columns touched (one team's part of a section that crosses into
    another's: its fill then sees no rectangle); `bodiless` columns get no body (a hollow under a deck). Returns
    {section number: the fill laid}."""
    import random
    rng = rng or random.Random(0)
    params = {**style.params, **(params or {})}
    todo = range(len(ground.sections)) if only is None else only
    laid = {}
    for n in todo:
        sec = ground.sections[n]
        cols = [c for c in sec.columns() if where is None or where(*c)]
        for x, z in cols:
            h = ground.top(x, z)
            if (x, z) not in bodiless:
                style.body(w, x, z, h)
            falls = ground.falls(x, z)
            name = face_of(x, z) if face_of else "edge"
            if falls and name:
                side, drop = falls[0]
                face = style.faces[name]
                along, pos = face.bay(x, z, side)
                face.lay(w, x, z, h, OPP[side], along, pos, air=drop)
            elif not falls and ground.depth(x, z) == 0:
                w.set(x, h, z, *style.seam)
        inner = set(cols)
        lot = Lot(sec, n, [c for c in ground.inside(n) if c in inner], sec.y, ground, params)
        if lot.cols:
            laid[n] = style.fill(w, lot, rng)
            for mname, mparams in sec.motifs:
                style.motifs[mname](w, lot, rng, **dict(mparams))
    return laid
