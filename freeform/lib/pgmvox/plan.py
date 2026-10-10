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
    """How a board's parts relate: "half" (a half turn), "mirror_x" or "mirror_z" for two teams, "cw" (a quarter
    turn clockwise, (x, z) -> (-1 - z, x) about the default axis) for four; the studio's names "rot_180" and
    "rot_90" are taken for "half" and "cw". The default axis (-0.5, -0.5) lies between blocks -1 and 0, so
    (x, z) -> (-1 - x, -1 - z) under a half turn. `order` is how many images a part has, itself included."""

    NAMES = {"rot_180": "half", "rot_90": "cw"}

    def __init__(self, op="half", axis=(-0.5, -0.5)):
        op = self.NAMES.get(op, op)
        assert op in ("half", "mirror_x", "mirror_z", "cw"), op
        self.op, self.axis = op, axis
        self.order = 4 if op == "cw" else 2

    def point(self, x, z):
        """The image of a point. A block (whole numbers) lands on a block; a point between blocks, such as a label
        or a route's bend at a block's centre, lands exactly on its image rather than rounded to a block."""
        if float(x).is_integer() and float(z).is_integer():
            return turn_xz(int(x), int(z), self.op, self.axis)
        cx, cz = self.axis
        dx, dz = OPS[self.op](x - cx, z - cz)
        return cx + dx, cz + dz

    def direction(self, d):
        dx, dz = vec(d)
        return NAMES[vec(OPS[self.op](dx, dz))]

    def image(self, a):
        """The image of a field over a board grid whose middle is the axis, indexed (x, z): where every column's
        value goes under the symmetry. A quarter turn needs a square grid."""
        a = np.asarray(a)
        if self.op == "half":
            return a[::-1, ::-1]
        if self.op == "mirror_x":
            return a[::-1, :]
        if self.op == "mirror_z":
            return a[:, ::-1]
        assert a.shape[0] == a.shape[1], "a quarter turn of a field needs a square grid"
        return a[:, ::-1].T

    def field(self, a, keep=None):
        """A field made symmetric: the mean of it and its images, or, on a two-team board with `keep` (a mask of
        the columns drawn, such as red's half), those columns as they are and every other one from the image."""
        if keep is not None:
            assert self.order == 2, "a quarter-turn board keeps a quarter, not a half"
            return np.where(keep, a, self.image(a))
        if self.order == 2:
            return 0.5 * (a + self.image(a))
        total, turned = np.array(a, float), np.asarray(a)
        for _ in range(self.order - 1):
            turned = self.image(turned)
            total = total + turned
        return total / self.order

    def whole(self, half):
        """A two-team board's field from the half drawn (the low x half for "half" and "mirror_x", the low z half
        for "mirror_z"), its image laid beside it."""
        if self.op == "half":
            return np.concatenate([half, half[::-1, ::-1]], axis=0)
        if self.op == "mirror_x":
            return np.concatenate([half, half[::-1]], axis=0)
        if self.op == "mirror_z":
            return np.concatenate([half, half[:, ::-1]], axis=1)
        raise ValueError("a quarter-turn board is not drawn as a half")


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

    @classmethod
    def from_heights(cls, H, x0, z0, water=None, steep=None, symmetry=None):
        """A plan read off a heightfield (a terrain board's shaped ground, before any world is written): every
        column's floor at H, kind "ground", "water" where the mask says, and "steep" where the slope as the studio
        reads it passes `steep` degrees. The walk graph and the sketch then read a terrain board as any plan."""
        from .terrain import slope_deg
        H = np.asarray(np.round(H)).astype(int)
        R = cls((x0, x0 + H.shape[0] - 1), (z0, z0 + H.shape[1] - 1), ["ground", "steep", "water"], 0, "ground",
                symmetry)
        R.H[:] = H
        if steep is not None:
            R.K[slope_deg(H) > steep] = R.kinds["steep"]
        if water is not None:
            R.K[np.asarray(water, bool)] = R.kinds["water"]
        return R

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
        if kind not in self.kinds:
            raise ValueError(f"kind {kind!r} is not one of this raster's kinds {list(self.kinds)}")
        for a, b in self._images(x, z, both):
            if self.inside(a, b):
                self.H[self.ix(a), self.iz(b)] = h
                self.K[self.ix(a), self.iz(b)] = self.kinds[kind]

    def box(self, x0, z0, x1, z1, h, kind="floor", both=True):
        """A rectangle by its corners, (x0, z0) to (x1, z1) inclusive: the order every other module takes."""
        self.rect(x0, x1, z0, z1, h, kind, both)

    def rect(self, x0, x1, z0, z1, h, kind="floor", both=True):
        """A rectangle by its ranges, x0..x1 and z0..z1 inclusive (the older order; box takes corners)."""
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
