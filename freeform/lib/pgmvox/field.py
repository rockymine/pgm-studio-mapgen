"""Heightfields stated as terms: a base height plus ramps, mounds, tilts and noise, summed in the order given, and
two fields mixed by a weight. The numbers stay the board's; this is the vehicle, not a recipe.

    h = terms(X, Z, 48.5, Ramp("x", -14, -64, 3.5), Gauss((-44, -78), 16, 4.5, rz=11))
    h = mix(town, hills, smoothstep(-70, -80, X))         # the town's ground eased into the hills' westward
    h = terms(X, Z, h, Noise(small, 0.8), Noise(big, 1.2))

A term is a value at every column; `terms` adds them to the base one after another, so a board that summed the
same terms by hand gets the same numbers to the last bit.
"""
from dataclasses import dataclass

import numpy as np

from .noise import smoothstep


@dataclass
class Ramp:
    """`rise` blocks eased in along an axis ("x" or "z") from `frm` to `to` (smoothstep): 0 before `frm`, `rise`
    past `to`. `frm` above `to` makes a ramp that rises toward lower coordinates."""
    along: str
    frm: float
    to: float
    rise: float

    def value(self, X, Z):
        return self.rise * smoothstep(self.frm, self.to, X if self.along == "x" else Z)


@dataclass
class Gauss:
    """A mound `rise` blocks high at `at`, falling off as exp(-(d ** power)) with d measured in radii `r` (along x)
    and `rz` (along z), the ellipse turned `angle` degrees from east toward south. A negative rise is a hollow."""
    at: tuple
    r: float
    rise: float
    rz: float = None
    power: int = 2
    angle: float = 0.0

    def value(self, X, Z):
        cx, cz = self.at
        rz = self.r if self.rz is None else self.rz
        u, v = X - cx, Z - cz
        if self.angle:
            a = np.radians(self.angle)
            u, v = u * np.cos(a) + v * np.sin(a), -u * np.sin(a) + v * np.cos(a)
        return self.rise * np.exp(-((u / self.r) ** self.power + (v / rz) ** self.power))


@dataclass
class Tilt:
    """A plane: `dx` blocks of rise per block east and `dz` per block south, zero at `at`."""
    dx: float
    dz: float
    at: tuple = (0, 0)

    def value(self, X, Z):
        return self.dx * (X - self.at[0]) + self.dz * (Z - self.at[1])


@dataclass
class Noise:
    """A field the board drew (fbm, ridged, a line) scaled by `rise`."""
    field: object
    rise: float

    def value(self, X, Z):
        return self.rise * self.field


def terms(X, Z, base, *parts):
    """`base` (a height or a field) plus each term's value, added in the order given."""
    total = base
    for part in parts:
        total = total + part.value(X, Z)
    return total


def mix(a, b, weight):
    """`a` where the weight is 0, `b` where it is 1, in proportion between: a * (1 - weight) + b * weight."""
    return a * (1 - weight) + b * weight
