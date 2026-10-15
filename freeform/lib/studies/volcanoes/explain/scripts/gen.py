"""Data for the caldera explainer: the caldera-lake study run step by step, every combination of five layers switched
on and off, the fields it is made of, and two iso renders. Writes data.json beside this file."""
import base64
import itertools
import json
import os
import sys
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import volcanoes as V                                                        # noqa: E402
import round2 as R                                                          # noqa: E402
from volcanoes import L, noise, smoothstep, grid, gullies                    # noqa: E402
from PIL import Image                                                       # noqa: E402

SCALE = 3                                                                   # heights stored in thirds of a block


def pack(a, lo=None, hi=None):
    """A field as base64 zlib bytes, z rows by x columns: heights in thirds of a block, or a field mapped to 0..255."""
    a = np.asarray(a, float).T
    if lo is None:
        q = np.clip(np.round(a * SCALE), 0, 255)
    else:
        q = np.clip(np.round((a - lo) / (hi - lo) * 255), 0, 255)
    return base64.b64encode(zlib.compress(q.astype(np.uint8).tobytes(), 9)).decode()


def caldera(X, Z, warp=True, gully=True, notch=True, wall=True, floor=True, snaps=None, fields=None):
    """round2.caldera_lake with five layers that can be switched off, recording a snapshot after each step."""
    snap = (lambda name, H: snaps.append((name, H.copy()))) if snaps is not None else (lambda name, H: None)
    H = R.ground(X, 3)
    snap("ground", H)
    Xw, Zw = R.warp(X, Z, 210, big=12, small=4) if warp else (X, Z)
    c = (0, 0)
    d0 = R.r_at(Xw, Zw, c, 0.9, 30)
    g = gullies(Xw, Zw, c, 30, 6, 70, 135, seed=8)
    cone = 12 + 108 * np.clip(1 - d0 / 145, 0, 1) ** 1.35
    H = R.foot(H, cone - (g if gully else 0) * 0, 16) if snaps is not None else H
    if snaps is not None:
        snap("cone", H)
        H = R.ground(X, 3)
    body = cone - (g if gully else 0)
    H = R.foot(H, body, 16)
    if snaps is not None:
        snap("gullies", H)
    theta = np.arctan2(Zw, Xw)
    cut = 14 * np.exp(-((np.angle(np.exp(1j * (theta - 2.3)))) / 0.25) ** 2)
    if notch:
        H = H - cut * smoothstep(80, 55, d0) * smoothstep(30, 55, d0)
    snap("notch", H)
    wobble = 0.1 * noise.fbm(X.shape, 40, 3, seed=9)
    dc = R.r_at(Xw, Zw, c, 0.82, 30) * (1 + (wobble if wall else 0))
    width_f = 6 + 6 * (0.5 + 0.5 * noise.fbm(X.shape, 60, 2, seed=11))
    width = width_f if wall else np.full(X.shape, 9.0)
    jag_f = 3 * noise.fbm(X.shape, 9, 2, seed=10)
    jag = jag_f if wall else 0.0
    floor_f = 30 + 4 * noise.fbm(X.shape, 30, 2, seed=12)
    fl = floor_f if floor else 30.0
    H = L.profile(H, dc, floor=30, floor_ground=fl, steps=[L.Step(42, 42 + width, 58),
                                                         L.Step(52 + width * 0.6, 58 + width, "ground")],
                  jag=jag, talus=(6, 9), mode="cut")
    snap("caldera", H)
    if floor:
        H = R.lumps(H, X, Z, 26, (-50, -45, 50, 45), (3, 8), (3, 8), seed=13, mask=(dc < 48) & (dc > 30))
    snap("slumps", H)
    isle = (-18, 14)
    ir = R.r_at(Xw, Zw, isle, 0.75, 70)
    H = R.foot(H, np.where(ir < 17, 30 + 26 * np.clip(1 - ir / 17, 0, 1) ** 0.95, -1e9), 4)
    snap("island", H)
    H = R.crater_in(H, ir, 5, 4, 1, 1.3, k=2)
    snap("crater", H)
    if fields is not None:
        fields.update(gullies=g, width=width_f, jag=jag_f, floor=floor_f, wobble=wobble, notch=cut, dc=dc, d0=d0)
    return H


def octaves(shape, cell, n, seed):
    """fbm's octaves one at a time, as fbm sums them."""
    rng = np.random.default_rng(seed)
    out, amp = [], 1.0
    for o in range(n):
        c = max(1, int(round(cell / (2 ** o))))
        out.append(amp * noise.lattice(shape, c, rng))
        amp *= 0.5
    return out


def iso_png(H, name, corner="se"):
    w, top, _ = V.build(H)
    path = os.path.join(HERE, f"{name}.png")
    V.render.iso(w.ids, w.dat, w.x0, w.z0, path, scale=2, corner=corner)
    V.render.trim(path)
    im = Image.open(path).convert("RGB")
    im = im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(path, optimize=True)
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


def main():
    _, X, Z = grid()
    snaps, fields = [], {}
    H = caldera(X, Z, snaps=snaps, fields=fields)
    ref = R.caldera_lake(X, Z)
    assert np.allclose(H, ref), "the explainer's recipe drifted from round2.caldera_lake"
    out = dict(size=X.shape[0], scale=SCALE, x0=int(X[0, 0]), z0=int(Z[0, 0]))
    out["steps"] = [dict(id=n, h=pack(h)) for n, h in snaps]
    names = ["warp", "gully", "notch", "wall", "floor"]
    combos = {}
    for bits in itertools.product([1, 0], repeat=5):
        flags = dict(zip(names, map(bool, bits)))
        combos["".join(map(str, bits))] = pack(caldera(X, Z, **flags))
    out["combos"] = combos
    oct_ = octaves(X.shape, 90, 4, seed=3)
    total = sum(oct_) / sum(0.5 ** o for o in range(4))
    out["octaves"] = [pack(o, -1, 1) for o in oct_] + [pack(total, -1, 1)]
    wx = [12 * noise.fbm(X.shape, 90, 3, seed=210), 12 * noise.fbm(X.shape, 90, 3, seed=211),
          4 * noise.fbm(X.shape, 22, 2, seed=212), 4 * noise.fbm(X.shape, 22, 2, seed=213)]
    Xw, Zw = R.warp(X, Z, 210, big=12, small=4)
    assert np.allclose(Xw, X + wx[0] + wx[2]) and np.allclose(Zw, Z + wx[1] + wx[3])
    out["warp"] = [pack(w / (12 if k < 2 else 4), -1, 1) for k, w in enumerate(wx)]
    out["fields"] = dict(gullies=pack(fields["gullies"], 0, 6), width=pack(fields["width"], 6, 12),
                         jag=pack(fields["jag"], -3, 3), floor=pack(fields["floor"], 26, 34),
                         notch=pack(fields["notch"], 0, 14))
    out["iso_on"] = iso_png(H, "iso-on")
    out["iso_off"] = iso_png(caldera(X, Z, warp=False, gully=False, notch=False, wall=False, floor=False), "iso-off")
    json.dump(out, open(os.path.join(HERE, "data.json"), "w"))
    print("steps", [n for n, _ in snaps], "bytes", os.path.getsize(os.path.join(HERE, "data.json")))


if __name__ == "__main__":
    main()
