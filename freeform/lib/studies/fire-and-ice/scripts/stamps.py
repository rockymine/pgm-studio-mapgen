"""The forms a fire-and-ice board is composed from, each as a stamp: what its study raises or cuts above its own
rolling ground, on the study's 300 by 300 grid, so it can be laid on any other ground at any turn and size.

    fissure        volcanoes round two: the stepped rift with its cones and flows
    somma_low      volcanoes round two: the broken rim with the low young cone
    caldera_lake   volcanoes round two: the caldera, its benches, slump blocks and island
    maar           volcanoes round two: the nested holes
    snowfield      winter: outcrops through drifted snow over ice, and the crevasses (two layers, rock and ice)

A stamp is stored in quarter blocks as int16, NaN as -32768, so the composer and its page read the same numbers.
A stamp's relief is the study's heights less the ground its study grew it from, so its edges fall to nothing and
two stamps add where they overlap. `ground` is the field every board starts from.

    python3 stamps.py      # writes ../stamps.npz
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIES = os.path.join(HERE, "..", "..")
sys.path[:0] = [os.path.join(STUDIES, "volcanoes", "scripts"), os.path.join(STUDIES, "winter", "scripts")]
import round2 as R  # noqa: E402
import winter as W  # noqa: E402
from volcanoes import grid, noise  # noqa: E402

OUT = os.path.join(HERE, "..", "stamps.npz")
LIQUID = {"fissure": "lava", "somma_low": "lava", "caldera_lake": "water", "maar": "water", "snowfield": None}


def own_ground(name, X):
    """The rolling ground each study grows its form from, computed exactly as the study does."""
    if name == "fissure":
        return R.ground(X, 10, rise=10) + 24 + 18 * noise.fbm(X.shape, 120, 3, seed=401)
    if name == "somma_low":
        return R.ground(X, 8)
    if name == "caldera_lake":
        return R.ground(X, 3)
    if name == "maar":
        return R.ground(X, 9, rise=10) + 26
    raise KeyError(name)


def stamps():
    X, Z = grid()[1:]
    out = {"ground": 6 * noise.fbm(X.shape, 90, 4, seed=700) + 2 * noise.fbm(X.shape, 25, 3, seed=701)}
    for name in ("fissure", "somma_low", "caldera_lake", "maar"):
        out[name] = getattr(R, name)(X, Z) - own_ground(name, X)
    lay = W.snowfield(X, Z)
    base = 26 + 14 * noise.fbm(X.shape, 110, 3, seed=1)
    out["snowfield_rock"] = lay.rock - base
    out["snowfield_ice"] = lay.ice - base                                  # NaN where rock shows or a crack is open
    return out


NAN = -32768


def quarter(v):
    """Heights in quarter blocks, NaN as NAN."""
    return np.where(np.isfinite(v), np.round(np.nan_to_num(v) * 4), NAN).astype(np.int16)


def load(path=OUT):
    """The stamps back as floats in blocks, NaN where stored as NAN."""
    return {k: np.where(v == NAN, np.nan, v / 4.0) for k, v in np.load(path).items()}


if __name__ == "__main__":
    got = stamps()
    np.savez_compressed(OUT, **{k: quarter(v) for k, v in got.items()})
    for k, v in got.items():
        f = v[np.isfinite(v)]
        print(f"{k:16s} min {f.min():7.1f}  max {f.max():7.1f}  edge |max| {np.nanmax(np.abs(np.r_[v[0], v[-1], v[:, 0], v[:, -1]])):5.1f}")
