"""The plan as rasters: every column's floor and what kind of floor it is, drawn once and read by the checker,
the sketch and the generator alike, so all three read the same board.

Heights: `H[x, z]` is the y of the **floor block**; a player stands at H + 1. A raster names this once, so a
board does not mean three things by "height" as the early boards did.

Symmetry is applied in the plan, not on the built world: a raster made with `Symmetry("half")` draws every
rectangle, cell, polygon and flight twice, the second time at its image, with stair directions turned.

    R = Raster((-60, 59), (-48, 47), kinds=["wall", "floor", "lava", "stair", "pad", "hill", "spawn"],
               base_h=28, base_kind="wall", symmetry=Symmetry("half"))
    R.rect(-40, -20, -10, 10, 13)                 # floor at 13, and its image
    R.flight((-20, -2), "e", width=(-2, 2), h0=14, n=3)
    R.poly([(...), ...], 17, "hill")
    R.storey(1).rect(-30, -26, -4, 4, 24, "roof")  # an upper storey: a roof walked over the floor at 13
"""
import numpy as np

from . import shapes
from .orient import OPS, NAMES, turn_xz, vec


class Symmetry:
    """How a board's two halves relate: "half" (a half turn), "mirror_x" or "mirror_z", about an axis; the
    default axis (-0.5, -0.5) lies between blocks -1 and 0, so (x, z) -> (-1 - x, -1 - z) under a half turn."""

    def __init__(self, op="half", axis=(-0.5, -0.5)):
        assert op in ("half", "mirror_x", "mirror_z")
        self.op, self.axis = op, axis

    def point(self, x, z):
        return turn_xz(x, z, self.op, self.axis)

    def direction(self, d):
        dx, dz = vec(d)
        return NAMES[vec(OPS[self.op](dx, dz))]


class Raster:
    def __init__(self, xs, zs, kinds, base_h=0, base_kind=None, symmetry=None):
        self.x_min, self.x_max = xs
        self.z_min, self.z_max = zs
        self.nx, self.nz = self.x_max - self.x_min + 1, self.z_max - self.z_min + 1
        self.kinds = {k: i for i, k in enumerate(kinds)} if not isinstance(kinds, dict) else dict(kinds)
        self.names = {i: k for k, i in self.kinds.items()}
        self.H = np.full((self.nx, self.nz), base_h, int)
        self.K = np.full((self.nx, self.nz), self.kinds[base_kind or next(iter(self.kinds))], int)
        self.stair = {}                                          # (x, z) -> the side the stair rises toward
        self.symmetry = symmetry
        self.X, self.Z = np.meshgrid(np.arange(self.x_min, self.x_max + 1), np.arange(self.z_min, self.z_max + 1),
                                     indexing="ij")
        self.storeys = [self]                                    # storey 0 is this raster; storey(n) adds more
        self.level = 0

    # --- storeys ---------------------------------------------------------------------------------------
    def storey(self, n=1):
        """The raster of the n-th storey over this one: the same extent, kinds and symmetry, with "none" where
        it has no floor. Draw on it with the same methods: R.storey(1).rect(..., 24, "roof"). A storey's
        floor must stand at least three over the floor under it for the floor under it to be walked."""
        while len(self.storeys) <= n:
            kinds = dict(self.kinds)
            if "none" not in kinds:
                kinds["none"] = max(kinds.values()) + 1
            up = Raster((self.x_min, self.x_max), (self.z_min, self.z_max), kinds, -1, "none", self.symmetry)
            up.storeys, up.level = self.storeys, len(self.storeys)
            self.storeys.append(up)
        return self.storeys[n]

    def has(self):
        """Where this storey has a floor (every cell, for storey 0)."""
        if self.level == 0:
            return np.ones(self.H.shape, bool)
        return self.K != self.kinds["none"]

    # --- coordinates -----------------------------------------------------------------------------------
    def ix(self, x):
        return x - self.x_min

    def iz(self, z):
        return z - self.z_min

    def inside(self, x, z):
        return self.x_min <= x <= self.x_max and self.z_min <= z <= self.z_max

    def h(self, x, z):
        return int(self.H[self.ix(x), self.iz(z)])

    def kind(self, x, z):
        return self.names[int(self.K[self.ix(x), self.iz(z)])]

    def mask(self, *kinds):
        return np.isin(self.K, [self.kinds[k] for k in kinds])

    # --- drawing ---------------------------------------------------------------------------------------
    def _images(self, x, z, both):
        yield x, z
        if both and self.symmetry:
            yield self.symmetry.point(x, z)

    def cell(self, x, z, h, kind="floor", both=True):
        for a, b in self._images(x, z, both):
            if self.inside(a, b):
                self.H[self.ix(a), self.iz(b)] = h
                self.K[self.ix(a), self.iz(b)] = self.kinds[kind]

    def rect(self, x0, x1, z0, z1, h, kind="floor", both=True):
        x0, x1 = sorted((x0, x1)); z0, z1 = sorted((z0, z1))
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                self.cell(x, z, h, kind, both)

    def where(self, m, h, kind="floor", both=True):
        """Every cell of a boolean mask over the raster."""
        for i, k in np.argwhere(m):
            self.cell(int(self.X[i, k]), int(self.Z[i, k]), h, kind, both)

    def poly(self, pts, h, kind="floor", both=True):
        self.where(shapes.inside(self.X, self.Z, pts), h, kind, both)

    def flight(self, start, rises, width=(0, 0), h0=0, n=1, kind="stair", both=True):
        """A flight of n stair cells climbing toward `rises` from `start` (x, z), the first at h0 and one up
        per cell; width (a, b) widens it across, a to b blocks either side of the line."""
        dx, dz = vec(rises)
        px, pz = -dz, dx                                         # across the flight
        for k in range(n):
            for w in range(width[0], width[1] + 1):
                x, z = start[0] + dx * k + px * w, start[1] + dz * k + pz * w
                self.cell(x, z, h0 + k, kind, False)
                self.stair[(x, z)] = NAMES[(dx, dz)]
                if both and self.symmetry:
                    a, b = self.symmetry.point(x, z)
                    self.cell(a, b, h0 + k, kind, False)
                    self.stair[(a, b)] = self.symmetry.direction((dx, dz))

    def at(self, x, z):
        """(h, kind) of a column, or (None, None) off the raster."""
        if not self.inside(x, z):
            return None, None
        return self.h(x, z), self.kind(x, z)
