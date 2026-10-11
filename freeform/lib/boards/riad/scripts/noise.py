"""Smooth noise without a noise library: random lattices upsampled with cubic splines, summed in octaves."""
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


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def polyline_distance(xs, zs, pts):
    """Distance from every (xs, zs) to a polyline, and the arc-length parameter of the nearest point."""
    best = np.full(xs.shape, np.inf)
    along = np.zeros(xs.shape)
    acc = 0.0
    for (ax, az), (bx, bz) in zip(pts[:-1], pts[1:]):
        dx, dz = bx - ax, bz - az
        L2 = dx * dx + dz * dz
        t = np.clip(((xs - ax) * dx + (zs - az) * dz) / L2, 0, 1)
        px, pz = ax + t * dx, az + t * dz
        d = np.hypot(xs - px, zs - pz)
        m = d < best
        best = np.where(m, d, best)
        along = np.where(m, acc + t * np.sqrt(L2), along)
        acc += np.sqrt(L2)
    return best, along


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
