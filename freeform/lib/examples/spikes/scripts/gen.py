"""Spikes: forms.spike's kinds on one yard, in two rows, with the library's tower and heightfield spire beside them.

    row z -30   needle, leaning horn, crystal cluster (hexagonal), fluted pinnacle with ledges, twisted (three-sided),
                tusks curling toward each other
    row z  25   stone forest (38 small fluted spikes), stalactites under a swept bridge between two mesas, a curl,
                forms.tower and landform.spire for comparison

The generator prints the blocks each kind laid.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World  # noqa: E402
from pgmvox.ground import landform as L  # noqa: E402
from pgmvox.scenery import forms  # noqa: E402
from pgmvox.scenery.forms import spike  # noqa: E402

GROUND = 10


def bezier(p0, p1, p2, p3, n=24):
    t = np.linspace(0, 1, n)[:, None]
    return list(map(tuple, (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3))


def gallery():
    """Every kind on one yard, in two rows."""
    w = World(-140, -60, 280, 120, sy=140)
    w.fill(-140, 0, -60, 139, GROUND, 59, B.WOOL, 8)
    P = np.array
    kinds = []
    # row 1 (z -30)
    kinds.append(("needle", spike(w, [(-120, 6, -30), (-121, 50, -29), (-118, 96, -31)], (6, 0, 1.0), rough=0.12, seed=1)))
    kinds.append(("leaning horn", spike(w, bezier(P([-92, 6, -36]), P([-92, 40, -36]), P([-84, 70, -24]), P([-62, 84, -18])),
                                        (7, 0, 1.3), rough=0.15, seed=2)))
    cluster = np.zeros(w.ids.shape, bool)
    rng = np.random.default_rng(3)
    for k in range(7):
        a, lean, h = rng.uniform(0, 2 * np.pi), rng.uniform(0.05, 0.6), rng.uniform(22, 56)
        base = (-30 + 3 * np.cos(a), 6, -30 + 3 * np.sin(a))
        top = (base[0] + h * lean * np.cos(a), 6 + h, base[2] + h * lean * np.sin(a))
        cluster |= spike(w, [base, top], (rng.uniform(4.5, 7), 0, 0.8), sides=6, seed=10 + k)
    kinds.append(("crystal cluster", cluster))
    kinds.append(("fluted pinnacle", spike(w, [(8, 6, -30), (10, 50, -28), (8, 88, -31)], (9, 0, 1.25), flutes=(9, 0.32),
                                           ledges=(11, 1.0), rough=0.1, seed=4)))
    kinds.append(("twisted", spike(w, [(44, 6, -30), (44, 80, -30)], (10, 0, 1.0), sides=3, twist=360, seed=5)))
    tusks = spike(w, bezier(P([66, 6, -30]), P([66, 50, -30]), P([78, 72, -30]), P([92, 66, -30])), (5.5, 0, 1.4), rough=0.1, seed=6)
    tusks |= spike(w, bezier(P([122, 6, -30]), P([122, 46, -30]), P([110, 70, -30]), P([96, 60, -30])), (5.5, 0, 1.4), rough=0.1, seed=7)
    kinds.append(("tusks", tusks))
    # row 2 (z 25): stone forest, stalactites under a bridge, a curl, and the library's forms for comparison
    forest = np.zeros(w.ids.shape, bool)
    rng = np.random.default_rng(8)
    for k in range(38):
        x, z = rng.uniform(-132, -78), rng.uniform(8, 50)
        h, r = rng.uniform(10, 34), rng.uniform(2.2, 4.0)
        dx, dz = rng.normal(0, 0.15, 2) * h
        forest |= spike(w, [(x, 6, z), (x + dx, 6 + h, z + dz)], (r, 0, rng.uniform(0.9, 1.6)), flutes=(5, 0.25),
                        sides=int(rng.choice([0, 0, 5])), rough=0.2, cell=5, seed=20 + k)
    kinds.append(("stone forest", forest))
    deck = forms.sweep(w, [(-66, 25), (-6, 25)], 64, forms.flare(3, 7, 3), forms.flare(2.5, 6, 2), forms.flare(3, 10, 2),
                       power=3.2, rough=0.15, seed=30)
    rng = np.random.default_rng(31)
    for k in range(22):
        x, z = rng.uniform(-58, -14), 25 + rng.normal(0, 2.0)
        under = 64 - 3 - 7 * abs((x + 36) / 30) ** 2
        deck |= spike(w, [(x, under + 2, z), (x + rng.normal(0, 0.6), under - rng.uniform(5, 22), z)], (rng.uniform(1.2, 2.6), 0, 1.5),
                      rough=0.1, seed=40 + k)
    kinds.append(("stalactites", deck))
    curl = bezier(P([20, 6, 30]), P([20, 70, 30]), P([60, 90, 18]), P([46, 52, 24]), n=40)
    kinds.append(("curl", spike(w, curl, (8, 0.4, 1.1), rough=0.1, seed=50)))
    return w, kinds


def mesas(w):
    """Two rock mesas for the stalactite bridge to grow out of, from the library's butte."""
    X, Z = w.grid()
    H = np.full(X.shape, float(GROUND))
    for k, c in enumerate([(-72, 25), (0, 25)]):
        H = L.butte(H, X.astype(float), Z.astype(float), c, 9, 66, cliff=2, talus=8, talus_height=0.25, jag=0.12, seed=70 + k)
    for i, k in np.argwhere(H > GROUND):
        w.ids[i, GROUND + 1:int(H[i, k]) + 1, k] = B.WOOL
        w.dat[i, GROUND + 1:int(H[i, k]) + 1, k] = 8


def library_forms(w):
    """The library's own: forms.tower (rings, upright, a flat crown) and a heightfield spire (landform.spire)."""
    rock = lambda y, b: (B.WOOL, 0)                                          # noqa: E731
    forms.tower(w, 82, 30, GROUND, 80, 6, rock, np.random.default_rng(1), crown=(B.WOOL, 0), vines=0, seed=3)
    X, Z = w.grid()
    H = np.full(X.shape, float(GROUND))
    H = L.spire(H, X.astype(float), Z.astype(float), (118, 30), 10, 74, taper=1.6, jag=0.15, seed=5)
    for i, k in np.argwhere(H > GROUND):
        w.ids[i, GROUND + 1:int(H[i, k]) + 1, k] = B.WOOL
        w.dat[i, GROUND + 1:int(H[i, k]) + 1, k] = 0


def paint(w, vol):
    sel = vol & (w.ids == 0)
    w.ids[sel] = B.WOOL
    w.dat[sel] = 0


w, kinds = gallery()
mesas(w)
for name, vol in kinds:
    paint(w, vol)
    print(f"{name}: {int(vol.sum())} blocks")
library_forms(w)
w.save(sys.argv[1], "Spikes", (0, GROUND + 1, 0))
print("generated")
