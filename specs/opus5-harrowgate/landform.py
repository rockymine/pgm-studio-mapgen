"""Plan-form and profile generators for relief marks.

A mark's ring and polyline are taken verbatim by the solver — nothing splines them — so a landform's
plan is whatever the author types. These build the coordinate lists a landform actually has.

The wander numbers are measured: for a drop of H blocks, a plan-form displacement at wavelength 2.5H
and amplitude 1.0-1.4H takes the share of steep cells lying on a straight run of 60+ blocks from 91%
to 0% on a scarp and from 73% to 0% on a bevelled area, at the same drop and the same steepness.
"""
import math, random


def densify(points, spacing):
    """The polyline resampled to a vertex every `spacing` blocks along its own length."""
    out = []
    for (ax, az), (bx, bz) in zip(points, points[1:]):
        run = math.dist((ax, az), (bx, bz))
        steps = max(1, int(round(run / spacing)))
        for k in range(steps):
            t = k / steps
            out.append([ax + (bx - ax) * t, az + (bz - az) * t])
    out.append([float(points[-1][0]), float(points[-1][1])])
    return out


def _normals(points):
    """Unit perpendicular at each vertex, from the chord through its neighbours."""
    out = []
    for i, (x, z) in enumerate(points):
        ax, az = points[max(0, i - 1)]
        bx, bz = points[min(len(points) - 1, i + 1)]
        dx, dz = bx - ax, bz - az
        length = math.hypot(dx, dz) or 1.0
        out.append((-dz / length, dx / length))
    return out


def cap_segments(points, longest=10.0):
    """The polyline with every segment split until none is longer than `longest`.

    Displacing a trace perpendicular to itself moves neighbouring vertices apart as well as sideways,
    so a trace sampled every 6 blocks can carry a 17-block segment once it has wandered — and a
    straight segment is exactly what the wander exists to remove. The cap is applied after the
    displacement for that reason.
    """
    out = []
    for start, end in zip(points, points[1:]):
        run = math.dist(start, end)
        steps = max(1, math.ceil(run / longest))
        for k in range(steps):
            t = k / steps
            out.append([round(start[0] + (end[0] - start[0]) * t, 1),
                        round(start[1] + (end[1] - start[1]) * t, 1)])
    out.append([float(points[-1][0]), float(points[-1][1])])
    return out


def wander(points, drop, amplitude=1.2, spacing=None, seed=1, jitter=0.3, longest=10.0):
    """A break of slope displaced perpendicular to its own trend, so it scallops into spurs and
    re-entrants instead of running straight.

    `drop` is the height the break carries, and everything else is stated in units of it: the
    wavelength is 2.5x drop, the displacement `amplitude` x drop, a vertex every wavelength/6.
    `jitter` varies each wavelength by that fraction, because real spacing is quasi-periodic —
    an exactly periodic scallop reads as a machined edge from the other direction.
    """
    wavelength = 2.5 * drop
    dense = densify(points, spacing or max(2.0, wavelength / 6))
    normals = _normals(dense)
    rng = random.Random(seed)

    # One phase accumulator walked along the line, so the wavelength can vary between lobes while
    # the displacement stays continuous across each of them.
    phases, phase = [], 0.0
    for i, point in enumerate(dense):
        if i:
            step = math.dist(point, dense[i - 1])
            local = wavelength * (1 + jitter * (rng.random() * 2 - 1))
            phase += 2 * math.pi * step / local
        phases.append(phase)

    swell = rng.uniform(0.7, 1.3)
    out = []
    for (x, z), (nx, nz), angle in zip(dense, normals, phases):
        # Two components an octave apart: the lobe, and the notch cut into its face.
        push = math.sin(angle) + 0.35 * math.sin(2.3 * angle + 1.7)
        offset = amplitude * drop * swell * push / 1.35
        out.append([round(x + nx * offset, 1), round(z + nz * offset, 1)])
    return cap_segments(out, longest)


def wander_ring(ring, drop, amplitude=1.0, spacing=None, seed=1, jitter=0.3, longest=10.0):
    """The same, closed: a bench or plateau outline that wraps without a seam at the join."""
    closed = list(ring) + [ring[0]]
    walked = wander(closed, drop, amplitude, spacing, seed, jitter, longest)
    # The first and last vertex are the same place on the ring, so drop the duplicate and let the
    # ring close on the shorter of the two displacements rather than on a step between them.
    return walked[:-1]


def concave_fall(top, bottom, count):
    """Heights down a channel, distributed the way a river's long profile actually falls: the
    headwater quarter of the length carries about half the total drop, the lower half a fifth.
    A channel of constant gradient is the fluvial twin of a constant-angle hillside."""
    fall = top - bottom
    out = []
    for i in range(count):
        t = i / max(1, count - 1)
        out.append(round(top - fall * (1 - (1 - t) ** 2.2), 1))
    return out


def hillside(crest, toe, run):
    """Where to pin the three marks of a hillside so the solver fills a sigmoid rather than a ramp.

    Returns (along, height) for the convex crest, the straight midslope and the concave footslope:
    the crest holds the top 20% of the run at a shallow angle, the midslope 40% at the steep one,
    the footslope the last 40% decaying to nearly level.
    """
    fall = crest - toe
    return [
        (round(run * 0.15), round(crest - fall * 0.10)),
        (round(run * 0.45), round(crest - fall * 0.55)),
        (round(run * 0.80), round(crest - fall * 0.92)),
    ]
