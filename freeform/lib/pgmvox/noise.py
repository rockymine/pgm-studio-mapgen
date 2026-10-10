"""Smooth noise without a noise library: random lattices upsampled with cubic splines, summed in octaves.

    fbm(shape, cell, octaves, seed)   rolling noise in about [-1, 1], features `cell` blocks across
    ridged(shape, cell, octaves, seed) crests: 1 - |fbm|, sharp where the noise crosses zero, in [0, 1]
    line(shape, along, cell, ...)     a wandering offset that varies along one axis of a grid and not the other
    smoothstep(e0, e1, x)             a smooth 0..1 ramp between two edges
    spline(pts, step)                 a Catmull-Rom curve through points
"""
import numpy as np
from scipy import ndimage


def lattice(shape, cell, rng):
    """One octave: a random lattice every `cell` blocks, cubic-upsampled to `shape`, values in about [-1, 1]."""
    gs = [max(2, int(np.ceil(s / cell)) + 3) for s in shape]
    g = rng.uniform(-1, 1, gs)
    zoom = [cell] * len(shape)
    up = ndimage.zoom(g, zoom, order=3, mode="reflect")
    sl = tuple(slice(cell, cell + s) for s in shape)
    return up[sl]


def fbm(shape, cell, octaves=4, seed=0, gain=0.5):
    rng = np.random.default_rng(seed)
    total = np.zeros(shape)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        c = max(1, int(round(cell / (2 ** o))))
        total += amp * lattice(shape, c, rng)
        norm += amp
        amp *= gain
    return total / norm


def line(shape, along, cell, octaves=2, seed=0, amp=1.0, base=0.0, clip=None):
    """A wandering line over a grid of `shape` (x, z): base + amp * fbm drawn along the `along` axis ("x" or "z")
    and the same across the other, shaped to broadcast against the grid. `clip` (lo, hi) bounds it. A foot, an
    edge or an inset that wanders by `amp` about `base`."""
    n = shape[1] if along == "z" else shape[0]
    f = fbm((n,), cell, octaves, seed=seed)
    f = f[None, :] if along == "z" else f[:, None]
    out = base + amp * f
    return out if clip is None else out.clip(*clip)


def ridged(shape, cell, octaves=4, seed=0, gain=0.5, sharpness=1.0):
    """Ridges: 1 - |fbm|, raised to `sharpness`; mountains are crests where it is near 1."""
    return (1.0 - np.abs(fbm(shape, cell, octaves, seed, gain))) ** sharpness


def smoothstep(e0, e1, x):
    """0 at e0, 1 at e1, eased between. Edges given high to low make a falling ramp (smoothstep(-14, -64, x) is 1
    below -64 and 0 above -14); equal edges make a step, 0 below the edge and 1 from it on."""
    span = np.subtract(e1, e0)
    if np.any(span == 0):
        t = np.where(span == 0, np.greater_equal(x, e0) * 1.0, np.clip((x - e0) / np.where(span == 0, 1, span), 0, 1))
    else:
        t = np.clip((x - e0) / span, 0, 1)
    return t * t * (3 - 2 * t)


def spline(pts, step=1.0):
    """Centripetal-ish Catmull-Rom through pts, sampled about every `step` blocks."""
    pts = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = (np.array(p, float) for p in pts[i - 1:i + 3])
        n = max(2, int(np.linalg.norm(p2 - p1) / step))
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)))
    out.append(tuple(pts[-2]))
    return out
