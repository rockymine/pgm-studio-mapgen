"""Land bridges: one canyon, six crossings, each a `forms.sweep` but the first, which is built the way a box arch
was built before sweep, column by column with its edge rows dropped at random, so the two can be compared.

    z -160  the column arch            a box six wide, its outer rows dropped per column: teeth on its sides
    z  -96  arch                       thin at the crown, thick where it grows out of the walls
    z  -32  curving                    a wide walkable deck bending across, flaring into buttresses
    z   32  window fin                 a tall fin, a great opening under it and a window through it
    z   96  broken                     two horns reaching out, open air between their tips
    z  160  twin                       a high thin arch over a broad low bridge, crossing at an angle

The generator prints every crossing's teeth: per 100 blocks of side edge, the columns whose outermost block sits
further out, or further in, than both its neighbours'.
"""
import sys

import numpy as np

from pgmvox import B, World  # noqa: E402
from pgmvox.geom import noise  # noqa: E402
from pgmvox.ground import landform as LF  # noqa: E402
from pgmvox.scenery.forms import flare, sweep  # noqa: E402
from pgmvox.surface.terrain import slope_deg  # noqa: E402

RIM, FLOOR = 70, 22
CROSSINGS = {"column arch": -160, "arch": -96, "curving": -32, "window fin": 32, "broken": 96, "twin": 160}
w = World(-100, -200, 200, 400, sy=100)
X, Z = (a.astype(float) for a in w.grid())

# the canyon: two mesas, the gap between them 62 to 82 wide, its walls stepped once and ragged
H = RIM + 3 * noise.fbm(X.shape, 60, 3, seed=1)
rim = 36 + 5 * noise.fbm((w.sz,), 50, 3, seed=2)[None, :]
centre = 6 * noise.fbm((w.sz,), 70, 2, seed=3)[None, :]
H = LF.profile(H, np.abs(X - centre), floor=FLOOR, floor_ground=FLOOR + 2 * noise.fbm(X.shape, 20, 2, seed=5),
               steps=[LF.Step(rim - 8, rim - 5, 46), LF.Step(rim - 1, rim + 2, "ground")],
               jag=2.0 * noise.fbm(X.shape, 6, 2, seed=4), talus=(5, 7), mode="cut")
top = np.round(H).astype(int)
ground = np.arange(w.sy)[None, :, None] <= top[:, None, :]


def column_arch(z):
    """A box six wide over the span, deck and underside curves along x, each outer row dropped per column."""
    rng = np.random.default_rng(0)
    m = np.zeros(w.ids.shape, bool)
    for x in range(-56, 57):
        tt = abs(x + 0.5) / 50.5
        deck = int(round(RIM + 2 - 2 * tt * tt))
        under = int(round(deck - 4 - 18 * tt * tt))
        for zz in range(z - 4, z + 4):
            edge = zz in (z - 4, z + 3)
            if edge and rng.random() < 0.6:
                continue
            m[x - w.x0, max(under + edge, 0):deck - edge + 1, zz - w.z0] = True
    return m


def bridges():
    z = CROSSINGS
    yield "column arch", column_arch(z["column arch"])
    yield "arch", sweep(w, [(-58, z["arch"]), (58, z["arch"])], flare(RIM - 2, RIM - 10, 2), flare(3.5, 7, 3),
                        flare(3, 10, 2), flare(3, 22, 2.2), rough=0.28, seed=3)
    c = z["curving"]
    path = [(-62, c - 26), (-26, c - 16), (0, c), (26, c + 14), (62, c + 22)]
    yield "curving", sweep(w, path, lambda t: RIM - 3 - 2.5 * np.sin(np.pi * t), flare(4.5, 11, 3), flare(2.5, 8, 2.5),
                           flare(5, 26, 2.4), power=3.4, rough=0.18, cell=18, seed=5)
    f = z["window fin"]
    fin = sweep(w, [(-58, f + 4), (58, f - 4)], RIM - 8, flare(2.5, 6, 3), flare(9, 12, 2), flare(6, 30, 1.8),
                power=3.6, rough=0.22, seed=7)
    ys = np.arange(w.sy)[None, :, None]
    yield "window fin", fin & ~((((X - 18) / 6.5) ** 2)[:, None, :] + ((ys - (RIM - 5)) / 4.0) ** 2 < 1)
    b = z["broken"]
    yield "broken", (sweep(w, [(-60, b + 2), (-4, b)], lambda t: RIM - 4 - 1.5 * t, lambda t: 6.5 - 4 * t ** 1.3,
                           lambda t: 7 - 4.5 * t, lambda t: 20 - 16 * t ** 0.8, rough=0.22, seed=9)
                     | sweep(w, [(5, b), (60, b - 2)], lambda t: RIM - 6 + t, lambda t: 2.6 + 4 * t ** 1.3,
                             lambda t: 2.5 + 4.5 * t, lambda t: 4 + 16 * t ** 1.25, rough=0.22, seed=10))
    t2 = z["twin"]
    yield "twin", (sweep(w, [(-60, t2 - 22), (60, t2 + 22)], flare(RIM - 1, RIM - 8, 2), flare(3, 6, 3),
                         flare(2.5, 8, 2), flare(2.5, 14, 2), rough=0.25, seed=11)
                   | sweep(w, [(-58, t2 + 26), (58, t2 - 20)], 46, flare(6, 10, 3), flare(2, 4, 2), flare(5, 18, 2),
                           power=3.2, rough=0.2, seed=12))


def teeth(m):
    """Per 100 blocks of side edge, the (x, y) columns whose outermost block on a side sits further out, or
    further in, than both neighbours' along the span."""
    idx = np.arange(w.sz)[None, None, :]
    occ = m.any(axis=2)
    spikes = total = 0
    for edge in (np.where(m, idx, w.sz).min(axis=2), np.where(m, idx, -1).max(axis=2)):
        e = np.where(occ, edge, np.nan)
        a, b, c = e[:-2], e[1:-1], e[2:]
        ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
        spikes += int((ok & (((b > a) & (b > c)) | ((b < a) & (b < c)))).sum())
        total += int(ok.sum())
    return 100.0 * spikes / max(total, 1)


deg = slope_deg(top)
w.ids[...] = np.where(ground, B.WOOL, 0)
w.dat[...] = np.where(ground, np.array([0, 8, 7], np.uint8)[np.where(deg < 30, 0, np.where(deg < 50, 1, 2))][:, None, :], 0)
for name, m in bridges():
    m = m & ~ground
    print(f"{name}: {int(m.sum())} blocks, {teeth(m):.1f} teeth per 100 blocks of side edge")
    above = np.ones_like(m); above[:, :-1] = ~m[:, 1:] & ~ground[:, 1:]
    below = np.ones_like(m); below[:, 1:] = ~m[:, :-1] & ~ground[:, :-1]
    w.ids[m] = B.WOOL
    w.dat[m] = np.where(above, 0, np.where(below, 7, 8))[m]
w.save(sys.argv[1], "Bridges", (-60, RIM + 1, 0))
print("generated")
