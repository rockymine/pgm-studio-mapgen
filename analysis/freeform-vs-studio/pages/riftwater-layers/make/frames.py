"""The pictures: every recorded step drawn in the map style, the base terms one by one, the close-ups of the
sinkhole and the spoil heap, and the heights the page reads under the pointer."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import pickle, numpy as np, json, base64
from PIL import Image
from scipy import ndimage
h = pickle.load(open(f"{OUT}/stack.pkl", "rb")); wd = pickle.load(open(f"{OUT}/world.pkl", "rb"))
land = h["land"]; S = 4; X_MIN, Z_MIN = h["X_MIN"], h["Z_MIN"]
from style import VOID, hypso, ramp, shade, up as _up, contours as _contours, outline as _outline
def up(rgb, s=S): return _up(rgb, s)
def contours(img, H, mask, step=2, major=10, s=S, dark=0.55): return _contours(img, H, mask, step, major, s, dark)
HL = np.array([255, 64, 160]); LO, HI = 36, 82
def outline(img, ch, colour=HL, s=S, tint=0.25): return _outline(img, ch, s, colour, tint)
def save(img, name):
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).transpose(1, 0, 2)).save(f"{OUT}/img/{name}.png"); return name
def b64(H, mask):
    a = np.where(mask, np.clip(np.round(H), 1, 255), 0).astype(np.uint8)
    return base64.b64encode(a.T.tobytes()).decode()       # row-major in picture order: z rows, x columns
def relief(H, mask=land, step=2):
    img = up(np.where(mask[..., None], hypso(H) * shade(H), VOID))
    return contours(img, H, mask, step)

frames, prev = [], None
for label, a in h["stack"]:
    if label == "outline":
        img = up(np.where(a.astype(bool)[..., None], np.array([150, 160, 120]), VOID))
        frames.append(dict(id=label, img=save(img, label), changed=int(a.sum()), w=land.shape[0])); continue
    if label == "underside":
        depth = np.where(land, h["H"] - a, 0)
        t = np.clip(depth / 40, 0, 1)[..., None]
        img = up(np.where(land[..., None], np.array([230, 220, 200]) * (1 - t) + np.array([90, 50, 40]) * t, VOID))
        img = contours(img, depth, land, step=4, major=20)
        frames.append(dict(id=label, img=save(img, label), changed=int(land.sum()), deepest=int(depth.max()),
                           w=land.shape[0], h=b64(depth, land), unit="tief"))
        continue
    ch = None if prev is None else (np.abs(a - prev) > 0.5) & land
    img = outline(relief(a), ch)
    frames.append(dict(id=label, img=save(img, label), changed=int(ch.sum()) if ch is not None else int(land.sum()),
                       w=land.shape[0], h=b64(a, land), unit="y"))
    prev = a

# the terms of the base step, each one's own contribution
POS, NEG = np.array([[244, 240, 232], [214, 150, 90], [150, 70, 40]], float), np.array([[244, 240, 232], [110, 150, 200], [40, 80, 150]], float)
names = {0: "nördlich des Flusses", 1: "südlich des Flusses", 2: "im Westen (ab x −70 eingeblendet)", 3: "überall"}
terms = []
for g, (base, parts) in enumerate(h["terms"]):
    for j, (kind, args, v) in enumerate(parts):
        top = float(np.abs(v).max()) or 1.0
        stops = NEG if args.get("rise", 1) < 0 else POS
        img = up(np.where(land[..., None], ramp(np.abs(v), 0, top, stops), VOID), 2)
        img = contours(img, v, land, step=1, major=1000, s=2, dark=0.7)
        nm = f"term-{g}-{j}"
        a = {k: (list(x) if isinstance(x, tuple) else x) for k, x in args.items()}
        terms.append(dict(img=save(img, nm), kind=kind, args=a, group=names[g], base=base if isinstance(base, float) else None,
                          lo=round(float(v[land].min()), 2), hi=round(float(v[land].max()), 2)))

# Erdfall and Halde: before and after, close up, with the area that drives them
def crop(label_before, label_after, at, r, area_mask, name):
    st = dict(h["stack"])
    i0, k0 = at[0] - X_MIN, at[1] - Z_MIN; R = int(r) + 6
    sl = (slice(max(i0 - R, 0), i0 + R + 1), slice(max(k0 - R, 0), k0 + R + 1))
    out = []
    for lab in (label_before, label_after):
        a = st[lab][sl]; m = land[sl]
        img = up(np.where(m[..., None], hypso(a) * shade(a), VOID), 10)
        img = contours(img, a, m, step=1, major=10, s=10, dark=0.6)
        img = outline(img, area_mask[sl], colour=np.array([255, 64, 160]), s=10, tint=0.0)
        out.append(save(img, f"{name}-{lab}"))
    row = i0 - sl[0].start
    prof = [[int(st[label_before][sl][x, k0 - sl[1].start]), int(round(st[label_after][sl][x, k0 - sl[1].start]))]
            for x in range(st[label_before][sl].shape[0])]
    return dict(before=out[0], after=out[1], x0=int(sl[0].start + X_MIN), z=int(at[1]), profile=prof)
X, Z = h["X"].astype(float), h["Z"].astype(float)
(sx, sz), floor, rad = h["sinkhole"]
sink = (np.hypot(X - sx, Z - sz) <= rad) & land
(px, pz), pr, ph = h["spoil"]
spoil = (np.hypot((X - px) / pr, (Z - pz) / (pr * 0.8)) < 1) & land
shapes = dict(sinkhole=crop("plazas", "sinkhole", (sx, sz), rad, sink, "crop-sink"),
              spoil=crop("sinkhole", "spoil", (px, pz), pr, spoil, "crop-spoil"))

Hred = h["H"]; Hfull = np.concatenate([Hred, Hred[::-1]]); lfull = np.concatenate([land, land[::-1]])
red = slice(0, land.shape[0])
for s in wd["snaps"][1:]:
    rgb = s["colours"].astype(float)
    full = s["label"] in ("mirror", "objectives")
    view = rgb if full else rgb[red]
    ch = s["below"] if s["label"] == "under" else s["changed"]
    ch = ch if full else ch[red]
    if s["label"] == "mirror": ch = ch & (np.arange(ch.shape[0])[:, None] >= land.shape[0])
    img = outline(up(view), ch if s["label"] != "lay" else None)
    frames.append(dict(id="w-" + s["label"], img=save(img, "w-" + s["label"]), changed=int(ch.sum()), blocks=s["blocks"],
                       w=view.shape[0], h=b64(Hfull if full else Hred, lfull if full else land), unit="Boden y"))
    if s["label"] == "lay":
        win = s["extra"]["winner"][red]
        pal = np.array([[233, 196, 106], [140, 140, 140], [122, 88, 58], [170, 170, 170], [110, 110, 110], [92, 70, 52],
                        [200, 200, 200], [150, 150, 160], [90, 90, 96]], float)
        rgb2 = np.where((win >= 0)[..., None], pal[np.clip(win, 0, 8)], np.where(land[..., None], np.array([96, 140, 72]), VOID))
        img = contours(up(rgb2 * shade(Hred)), Hred, land)
        frames.append(dict(id="w-paint", img=save(img, "w-paint"), changed=int((win >= 0).sum()), w=land.shape[0],
                           h=b64(Hred, land), unit="Boden y"))
legend = [[y] + [int(c) for c in hypso(np.array(y))] for y, t in [(y, 0) for y in range(36, 83, 2)]]
places = [(n, int(x), int(z)) for n, (x, z) in h["places"]]
json.dump(dict(frames=frames, terms=terms, shapes=shapes, legend=legend, places=places, X_MIN=X_MIN, Z_MIN=Z_MIN,
               nz=int(land.shape[1]), S=S), open(f"{OUT}/frames.json", "w"))
print(len(frames), len(terms), [(f["id"], f["changed"]) for f in frames][:5])
