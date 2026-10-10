"""Run the Riftwater port's gen.py steps in-process, snapshotting the world after each."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, os, pickle, numpy as np
B = os.path.join(ROOT, "freeform/lib/ports/riftwater/scripts")
sys.path.insert(0, B); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
os.chdir(B)
import dress, ground, plan as P, under, works
from pgmvox import B as BL, World, props, terrain
from pgmvox.blocks import COLOURS
from pgmvox.orient import turn_world
SNAPS, prev = [], {}
def top_colours(w):
    solid = w.ids != 0
    top = np.where(solid.any(axis=1), w.ids.shape[1] - 1 - np.argmax(solid[:, ::-1, :], axis=1), -1)
    i, k = np.indices(top.shape); t = np.clip(top, 0, None)
    col = COLOURS[w.ids[i, t, k], w.dat[i, t, k]].astype(float)
    shade = np.clip(1 + 0.06 * (np.roll(top, 1, 0) - top) + 0.04 * (np.roll(top, 1, 1) - top), 0.6, 1.25)
    col = np.clip(col * shade[..., None], 0, 255); col[top < 0] = (24, 26, 34)
    return col.astype(np.uint8), top
def snap(label, w, extra=None):
    col, top = top_colours(w)
    if "ids" in prev:
        changed = ((prev["ids"] != w.ids) | (prev["dat"] != w.dat)).any(axis=1)
        below = (((prev["ids"] != w.ids) | (prev["dat"] != w.dat)) & (np.arange(w.sy)[None, :, None] < top[:, None, :] - 1)).any(axis=1)
        n = int(((prev["ids"] != w.ids) | (prev["dat"] != w.dat)).sum())
    else:
        changed = (w.ids != 0).any(axis=1); below = np.zeros_like(changed); n = int((w.ids != 0).sum())
    SNAPS.append(dict(label=label, colours=col, changed=changed, below=below, blocks=n, extra=extra))
    prev["ids"], prev["dat"] = w.ids.copy(), w.dat.copy()
# the paint layers: which layer laid each column's top
captured = {}
real_lay, real_fill = ground.lay, ground.fill_water
def lay(w, H, mask=None, **kw):
    deg = real_lay(w, H, mask, **kw)
    winner = np.full(H.shape, -1)
    for i, k in np.argwhere(mask):
        for n, layer in enumerate(kw.get("paint") or []):
            if layer.applies(i, k, deg[i, k]):
                winner[i, k] = n; break
    captured["paint"] = winner; captured["layers"] = kw.get("paint")
    snap("lay", w, dict(winner=winner))
    return deg
def fill_water(*a, **kw):
    n = real_fill(*a, **kw); snap("fill_water", w); return n
ground.lay, ground.fill_water = lay, fill_water
real_crop, real_crow = props.crop_field, props.scarecrow
def crop_field(*a, **kw):
    snap("dress_before_field", w); r = real_crop(*a, **kw); return r
def scarecrow(*a, **kw):
    r = real_crow(*a, **kw); snap("crop_field", w); return r
props.crop_field, props.scarecrow = crop_field, scarecrow
L = P.land()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
snap("empty", w)
ground.lay_ground(w, L)
ground.falls(w, L); snap("waterfall", w)
u = under.build(w, L); snap("under", w)
k = works.build(w, L, u["shaft_top"]); under.gaol_ladder(w); snap("works", w)
sq_x, sq_z = L.X[L.square], L.Z[L.square]
west = int(sq_x.min()) + 2
props.stalls(w, [(west, z) for z in range(int(sq_z.min()) + 3, int(sq_z.max()) - 1)], 52, "e"); snap("stalls", w)
d = dress.build(w, L); snap("dress", w)
X, _ = w.grid()
turn_world(w, "mirror_x", X < 0, recolour={(BL.WOOL, 14): (BL.WOOL, 11)}); snap("mirror", w)
O = P.objectives(); O.stamp(w); snap("objectives", w)
import hashlib, json
want = json.load(open(os.path.join(ROOT, "freeform/lib/check/boards.json")))["ports/riftwater"]["volume.bin"]
w.save(os.path.join(OUT, "build"), "Riftwater", (0, 90, 0))
got = hashlib.sha256(open(os.path.join(OUT, "build", "volume.bin"), "rb").read()).hexdigest()
print("same world as the recorded hash:", got == want)
layers = [dict(block=str(l.block), slope=l.slope, where=l.where is not None, values=len(l.values)) for l in captured["layers"]]
pickle.dump(dict(snaps=SNAPS, layers=layers, x0=w.x0, z0=w.z0), open(sys.argv[1], "wb"))
print([(s["label"], s["blocks"]) for s in SNAPS])
