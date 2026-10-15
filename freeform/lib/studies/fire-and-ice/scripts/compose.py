"""A fire-and-ice board composed from the stamps: a layout places each form on a shared ground at a centre, a turn,
a size and a crop, and the composer adds their relief, lays the snowfield over the result, and fills every hollow
with the liquid of the form that shaped it most: lava in the fissure and the somma, water in the caldera and the
maar, ice on the snowfield, water anywhere else.

    python3 compose.py [layout.json]            # the default layout when none is given; renders into ../renders
    python3 compose.py [layout.json] --world    # and writes maps/other/studies_fire_and_ice

A layout is the JSON the composer page copies:

    {"width": 160, "length": 300,
     "features": [{"kind": "fissure", "x": 80, "z": 150, "angle": 90, "scale": 0.8, "crop": [300, 300]}, ...]}

`x` and `z` are the form's centre in board blocks, `angle` turns it clockwise in degrees, `scale` shrinks it and its
heights together, and `crop` is the part of its 300 by 300 stamp that is laid, in stamp blocks. Every step is
whole-array arithmetic that composer.html repeats in the browser, so the page shows what this writes.
"""
import heapq
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
from pgmvox import B, World  # noqa: E402
from pgmvox.read import render  # noqa: E402
from pgmvox.surface.terrain import slope_deg  # noqa: E402

STAMPS = os.path.join(HERE, "..", "stamps.npz")
OUT = os.path.join(HERE, "..", "renders")
BASE, FEATHER, HALF = 30.0, 18.0, 150
LIQUID = {"fissure": "lava", "somma_low": "lava", "caldera_lake": "water", "maar": "water", "snowfield": "ice"}
ROCK = ((B.WOOL, 8), (B.WOOL, 7), (B.WOOL, 15))                     # gentle, steep, cliff: light grey to black
DEFAULT = {"width": 160, "length": 300, "features": [
    {"kind": "fissure", "x": 80, "z": 150, "angle": 90, "scale": 0.85, "crop": [300, 300]},
    {"kind": "somma_low", "x": 40, "z": 85, "angle": 0, "scale": 0.5, "crop": [300, 300]},
    {"kind": "caldera_lake", "x": 45, "z": 225, "angle": 0, "scale": 0.4, "crop": [300, 300]},
    {"kind": "maar", "x": 128, "z": 236, "angle": 0, "scale": 0.45, "crop": [300, 300]},
    {"kind": "snowfield", "x": 122, "z": 92, "angle": 0, "scale": 1.0, "crop": [80, 150]},
]}


def rnd(a):
    """Half up, the way the page rounds."""
    return np.floor(a + 0.5).astype(int)


def sample(stamp, iu, iv):
    """The stamp at fractional cells, bilinear; NaN where any of the four cells is NaN or the point is off it."""
    n = stamp.shape[0]
    i0, k0 = np.floor(iu).astype(int), np.floor(iv).astype(int)
    fu, fv = iu - i0, iv - k0
    ok = (i0 >= 0) & (k0 >= 0) & (i0 < n - 1) & (k0 < n - 1)
    i0, k0 = np.clip(i0, 0, n - 2), np.clip(k0, 0, n - 2)
    a, b = stamp[i0, k0], stamp[i0 + 1, k0]
    c, d = stamp[i0, k0 + 1], stamp[i0 + 1, k0 + 1]
    got = (a * (1 - fu) + b * fu) * (1 - fv) + (c * (1 - fu) + d * fu) * fv
    return np.where(ok, got, np.nan)


def place(f, X, Z):
    """Where a form's stamp lands: its weight on every board cell (1 inside, falling to 0 over FEATHER stamp blocks
    at the crop's edge) and the stamp cell each board cell reads."""
    a = np.radians(f["angle"])
    dx, dz = X - f["x"], Z - f["z"]
    u = (dx * np.cos(a) + dz * np.sin(a)) / f["scale"]
    v = (-dx * np.sin(a) + dz * np.cos(a)) / f["scale"]
    cw, cl = f["crop"]
    edge = np.minimum(cw / 2 - np.abs(u), cl / 2 - np.abs(v))
    t = np.clip(edge / FEATHER, 0, 1)
    return t * t * (3 - 2 * t), u + HALF, v + HALF


def fill_basins(top):
    """Every hollow filled to the level it spills at, by priority flood from the board's edge."""
    n, m = top.shape
    filled = top.copy()
    seen = np.zeros(top.shape, bool)
    heap = []
    for i in range(n):
        for k in range(m):
            if i in (0, n - 1) or k in (0, m - 1):
                heap.append((int(top[i, k]), i * m + k))
                seen[i, k] = True
    heapq.heapify(heap)
    while heap:
        level, c = heapq.heappop(heap)
        i, k = divmod(c, m)
        for a, b in ((i + 1, k), (i - 1, k), (i, k + 1), (i, k - 1)):
            if 0 <= a < n and 0 <= b < m and not seen[a, b]:
                seen[a, b] = True
                filled[a, b] = max(top[a, b], level)
                heapq.heappush(heap, (int(filled[a, b]), a * m + b))
    return filled


def compose(layout, S):
    W, L = layout["width"], layout["length"]
    X, Z = np.meshgrid(np.arange(W, dtype=float), np.arange(L, dtype=float), indexing="ij")
    H = BASE + S["ground"][:W, :L].astype(float)
    reach = []                                                           # how much each form moves each cell
    for f in layout["features"]:
        w, iu, iv = place(f, X, Z)
        if f["kind"] != "snowfield":
            lift = w * f["scale"] * np.nan_to_num(sample(S[f["kind"]], iu, iv))
            H = H + lift
            reach.append(np.abs(lift))
        else:
            reach.append(np.where(w > 0.5, 1e9, 0.0))                      # snow owns what it covers
    weights = [place(f, X, Z)[0] for f in layout["features"]]
    rock, ice = H.copy(), np.full(H.shape, np.nan)
    for f, w in zip(layout["features"], weights):
        if f["kind"] == "snowfield":
            _, iu, iv = place(f, X, Z)
            r = np.nan_to_num(sample(S["snowfield_rock"], iu, iv))
            i = sample(S["snowfield_ice"], iu, iv)
            rock = rock + w * f["scale"] * r
            ice = np.where(np.isfinite(i) & (w > 0.2), H + w * f["scale"] * i, ice)
    rock = rnd(rock)
    ice = np.where(np.isfinite(ice), rnd(np.nan_to_num(ice)), -1)
    ice = np.where(ice > rock, ice, -1)
    top = np.maximum(rock, ice)
    level = fill_basins(top)
    wet = level > top
    owner = np.full(H.shape, -1)
    best = np.full(H.shape, 0.5)
    for j, r in enumerate(reach):
        owner = np.where(r > best, j, owner)
        best = np.maximum(best, r)
    from scipy import ndimage
    lab, n = ndimage.label(wet)
    kinds = np.full(H.shape, "", dtype=object)
    for b in range(1, n + 1):
        cells = lab == b
        votes = np.bincount(owner[cells] + 1, minlength=len(weights) + 1)
        votes[0] = 0
        j = int(np.argmax(votes)) - 1
        kinds[cells] = LIQUID[layout["features"][j]["kind"]] if votes.max() > 0 else "water"
    return {"rock": rock, "ice": ice, "level": np.where(wet, level, -1), "kind": kinds}


def build(c):
    rock, ice, level, kind = c["rock"], c["ice"], c["level"], c["kind"]
    W, L = rock.shape
    sy = int(max(rock.max(), ice.max(), level.max())) + 8
    w = World(0, 0, W, L, sy=sy)
    ys = np.arange(sy)[None, :, None]
    deg = slope_deg(rock)
    tone = np.where(deg < 30, 0, np.where(deg < 50, 1, 2))
    ground = ys <= rock[:, None, :]
    w.ids[...] = np.where(ground, B.STONE, 0)
    skin = ground & (ys > rock[:, None, :] - 3)
    w.ids[...] = np.where(skin, np.array([t[0] for t in ROCK], np.uint16)[tone][:, None, :], w.ids)
    w.dat[...] = np.where(skin, np.array([t[1] for t in ROCK], np.uint8)[tone][:, None, :], 0)
    body = (ice >= 0)[:, None, :] & (ys <= ice[:, None, :]) & ~ground
    w.ids[body] = B.PACKED_ICE
    w.ids[body & (ys >= ice[:, None, :] - 1)] = B.SNOW
    w.dat[body] = 0
    for name, block in (("water", B.WATER), ("lava", B.LAVA), ("ice", B.WATER)):
        sel = (kind == name) & (level >= 0)
        wet = sel[:, None, :] & (ys <= level[:, None, :]) & (w.ids == 0)
        w.ids[wet] = block
        if name == "ice":
            w.ids[sel[:, None, :] & (ys == level[:, None, :]) & (w.ids == block)] = B.ICE
    return w


def world_out(layout, w):
    """The board as a world beside the other study worlds, with a sign at the arrival naming its layout."""
    import importlib.util
    import tempfile
    spec = importlib.util.spec_from_file_location("study_worlds", os.path.join(HERE, "..", "..", "worlds.py"))
    SW = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(SW)
    x, y, z = SW.spawn(w, False)
    if w.get(x + 1, y, z)[0] == 0 and w.get(x + 1, y - 1, z)[0] != 0:
        w.sign(x + 1, y, z, ["fire and ice", f"{layout['width']} x {layout['length']}",
                             f"{len(layout['features'])} forms", "pgmvox study"], rot=4)
    folder = "other/studies_fire_and_ice"
    with tempfile.TemporaryDirectory() as build_dir:
        w.save(build_dir, "Studies: fire and ice", (x, y, z))
        said = SW.write(build_dir, os.path.join(SW.INDEX.WORLDS, folder))
    SW.index(folder, "freeform/lib/studies/fire-and-ice")
    print(f"{folder}: {said}  arrival {x} {y} {z}")


def main(path=None, world=False):
    layout = DEFAULT if path is None else json.load(open(path))
    from stamps import load
    S = load(STAMPS)
    c = compose(layout, S)
    w = build(c)
    os.makedirs(OUT, exist_ok=True)
    for corner in ("se", "nw"):
        p = os.path.join(OUT, f"iso-{corner}.png")
        render.iso(w.ids, w.dat, w.x0, w.z0, p, scale=3, corner=corner, ymin=0)
        render.trim(p)
    wet = c["level"] >= 0
    for name in ("water", "lava", "ice"):
        print(f"{name:6s} {int(np.sum(wet & (c['kind'] == name))):6d} columns")
    print(f"rock {c['rock'].min()}..{c['rock'].max()}  snow columns {int(np.sum(c['ice'] >= 0))}")
    if world:
        world_out(layout, w)
    return layout, c, w


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--world"]
    main(args[0] if args else None, "--world" in sys.argv)
