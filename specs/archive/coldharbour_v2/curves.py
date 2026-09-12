#!/usr/bin/env python3
"""Bezier handles for a compiled layout's coasts — and the rule that stops one becoming a loop.

`controls` is keyed by vertex index as a string and the handles are ABSOLUTE board coordinates
(GENERATION-NOTES §3). The edge from vertex i to vertex j is the cubic

    p0 = V[i]    c1 = controls[i].out    c2 = controls[j].in    p3 = V[j]

**The undocumented half is which side of the vertex a handle may sit on.** A cubic doubles back on
itself — a cusp, and past that a self-intersecting loop that rasterizes as a detached scrap of land —
whenever a handle projects *backwards* along its own edge. That is exactly what a hand-placed handle does
if you think of it as "push the corner outward": pushing it outward without also pushing it *along* the
edge puts c1 behind p0.

So every handle here is built as

    c1 = p0 + d·t + n·bulge          c2 = p3 − d·t + n·bulge

with `d` the edge vector, `t` a forward fraction and `n` the outward unit normal. The forward term is what
makes it a corner rather than a loop, and the two constraints that keep it one are

    t·|d| ≥ bulge          and          bulge ≤ 0.35·|d|

— the handle must travel further along the edge than it travels away from it, and a short edge cannot
carry a big bulge. Both are checked, and the finished ring is flattened and tested for self-intersection
before anything is posted.
"""
import json, math

T = 0.30                      # forward fraction of the edge each handle takes
MAX_BULGE_FRACTION = 0.35


def _signed_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly)))


def _inside(poly, x, z):
    hit = False
    for i in range(len(poly)):
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % len(poly)]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1:
            hit = not hit
    return hit


def outward_normal(poly, i, j):
    """The unit normal of edge i→j pointing out of the polygon."""
    (x1, z1), (x2, z2) = poly[i], poly[j]
    dx, dz = x2 - x1, z2 - z1
    length = math.hypot(dx, dz) or 1.0
    nx, nz = dz / length, -dx / length
    mx, mz = (x1 + x2) / 2, (z1 + z2) / 2
    if _inside(poly, mx + nx * 0.5, mz + nz * 0.5):
        nx, nz = -nx, -nz
    return nx, nz


def controls_for(poly, bulges):
    """bulges[i] = how far edge i→i+1 bows outward, in blocks. 0 leaves the edge straight."""
    controls, clamped = {}, []
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        bulge = bulges[i]
        if not bulge:
            continue
        (x1, z1), (x2, z2) = poly[i], poly[j]
        dx, dz = x2 - x1, z2 - z1
        length = math.hypot(dx, dz)
        cap = min(MAX_BULGE_FRACTION * length, T * length)
        if bulge > cap:
            clamped.append((i, round(bulge, 1), round(cap, 1)))
            bulge = cap
        nx, nz = outward_normal(poly, i, j)
        c1 = [round(x1 + dx * T + nx * bulge, 2), round(z1 + dz * T + nz * bulge, 2)]
        c2 = [round(x2 - dx * T + nx * bulge, 2), round(z2 - dz * T + nz * bulge, 2)]
        controls.setdefault(str(i), {})['out'] = c1
        controls.setdefault(str(j), {})['in'] = c2
    return controls, clamped


def flatten(poly, controls, steps=14):
    """The ring the rasterizer will see, so it can be tested before it is posted."""
    out = []
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        p0, p3 = poly[i], poly[j]
        c1 = controls.get(str(i), {}).get('out', p0)
        c2 = controls.get(str(j), {}).get('in', p3)
        for s in range(steps):
            t = s / steps
            u = 1 - t
            out.append([u*u*u*p0[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t*t*t*p3[0],
                        u*u*u*p0[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t*t*t*p3[1]])
    return out


def _crosses(a, b, c, d):
    def side(p, q, r):
        return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    d1, d2, d3, d4 = side(c, d, a), side(c, d, b), side(a, b, c), side(a, b, d)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def self_intersections(ring):
    n = len(ring)
    hits = []
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if _crosses(ring[i], ring[(i+1) % n], ring[j], ring[(j+1) % n]):
                hits.append((i, j))
    return hits
