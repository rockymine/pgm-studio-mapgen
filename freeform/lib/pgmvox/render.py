"""Pictures of a built world, in the studio's colours: an isometric view from any corner, a straight-on
elevation, an x-ray of what lines its caves and rooms, a true-scale cutaway along any polyline, and the trim that
cuts the empty sky from a render.

    iso(w.ids, w.dat, w.x0, w.z0, "out.png", scale=4, corner="sw", box=(x0, z0, x1, z1), ymin=40, ymax=90)
    elevation(w.ids, w.dat, w.x0, w.z0, "out.png", box, ymin, ymax, look="north")
    cutaway(w, "out.png", [(x, z), ...], ymin, ymax)
    trim("out.png")
"""
import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from . import blocks as K

# what a render looks past to the block behind: everything a player walks through but water, and the invisible
SEE_PAST = (K.PASSABLE - {K.B.WATER, K.B.WATER_FLOW}) | {36}


def xray_shell(ids):
    """Keep only what lines a roofed void — a cave, a gallery, a cellar — and what stands in one."""
    solid = (ids > 0) & ~np.isin(ids, [8, 9])
    # roofed air: air with solid somewhere above it in its column
    above = np.flip(np.maximum.accumulate(np.flip(solid, axis=1), axis=1), axis=1)
    roof = np.zeros_like(solid); roof[:, :-1, :] = above[:, 1:, :]
    below_acc = np.maximum.accumulate(solid, axis=1)
    floor = np.zeros_like(solid); floor[:, 1:, :] = below_acc[:, :-1, :]
    cave = ~solid & roof & floor & (ids != 8) & (ids != 9)
    near = np.zeros_like(cave)
    for ax in (0, 1, 2):
        for sh in (1, -1):
            near |= np.roll(cave, sh, axis=ax)
    # drop the ceilings and the upper walls so the passages are seen into from above
    air_below = np.zeros_like(cave); air_below[:, 1:, :] = cave[:, :-1, :]
    air_below2 = np.zeros_like(cave); air_below2[:, 2:, :] = cave[:, :-2, :]
    keep = (near & solid & ~air_below & ~air_below2) | (cave & (ids > 0)) | ((ids == 9) & roof)
    out = np.where(keep, ids, 0).astype(ids.dtype)
    return out



def iso(ids, dat, x0, z0, out, scale=2, corner="se", box=None, ymin=0, ymax=None, xray=False):
    """Every exposed block a small cube in the studio's colour, seen from a corner, cropped to box
    (x0, z0, x1, z1) and to heights ymin..ymax; xray keeps only what lines a roofed void."""
    sx, sy, sz = ids.shape
    if box:
        bx0, bz0, bx1, bz1 = box
        ids = ids[bx0 - x0:bx1 - x0 + 1, :, bz0 - z0:bz1 - z0 + 1]
        dat = dat[bx0 - x0:bx1 - x0 + 1, :, bz0 - z0:bz1 - z0 + 1]
    if xray:
        ids = xray_shell(ids)
    if ymax is not None:
        ids = ids.copy(); ids[:, ymax + 1:, :] = 0
    if ymin:
        ids = ids.copy(); ids[:, :ymin, :] = 0
    # rotate so the camera always looks from +x +z
    if corner == "sw":
        ids, dat = ids[::-1, :, :], dat[::-1, :, :]
        ids, dat = np.transpose(ids, (2, 1, 0)), np.transpose(dat, (2, 1, 0))
    elif corner == "nw":
        ids, dat = ids[::-1, :, ::-1], dat[::-1, :, ::-1]
    elif corner == "ne":
        ids, dat = ids[:, :, ::-1], dat[:, :, ::-1]
        ids, dat = np.transpose(ids, (2, 1, 0)), np.transpose(dat, (2, 1, 0))
    nx, ny, nz = ids.shape
    table = K.COLOURS.astype(np.float32)
    trans = np.zeros(256, bool)
    trans[sorted(SEE_PAST)] = True
    solid = ~trans[ids]
    present = (ids > 0) & (ids != 36)                # block 36 marks the build area at y 0 and is invisible
    # exposed: something present whose top, +x or +z neighbour is see-through
    up = np.ones_like(solid); up[:, :-1, :] = ~solid[:, 1:, :]
    ex = np.ones_like(solid); ex[:-1, :, :] = ~solid[1:, :, :]
    ez = np.ones_like(solid); ez[:, :, :-1] = ~solid[:, :, 1:]
    vis = present & (up | ex | ez)
    X, Y, Z = np.nonzero(vis)
    I = ids[X, Y, Z]; D = dat[X, Y, Z]
    col = table[I, D & 15]
    # texture: a fixed per-block brightness jitter, so a wall of one block reads as blocks
    hsh = ((X * 73856093) ^ (Y * 19349663) ^ (Z * 83492791)) & 1023
    col = col * (0.93 + 0.14 * (hsh / 1023.0))[:, None]
    s = scale
    u = (X - Z) * s + (nz - 1) * s
    v = (X + Z) * s // 2 - Y * s + ny * s
    depth = X + Y + Z
    W = (nx + nz) * s + 2 * s
    Hh = ((nx + nz) * s) // 2 + ny * s + 3 * s
    img = np.zeros((Hh, W, 3), np.float32)
    img[:] = (205, 220, 235)
    zbuf = np.full((Hh, W), -1, np.int64)
    # height shading so the relief reads
    light = 0.82 + 0.18 * (Y / max(1, ny))
    # the cube sprite: top face s rows, then the +z (left) and +x (right) faces s rows
    keys, deps, cols = [], [], []
    for dy in range(2 * s):
        for dx in range(2 * s):
            if dy < s:
                shade = 1.0
            elif dx < s:
                shade = 0.78
            else:
                shade = 0.62
            if s >= 4 and (dx in (0, 2 * s - 1) or dy in (0, 2 * s - 1) or (dy == s and True)):
                shade *= 0.82
            py = v + dy; pxx = u + dx
            ok = (py >= 0) & (py < Hh) & (pxx >= 0) & (pxx < W)
            keys.append(py[ok] * W + pxx[ok])
            # a face is nearer than the top it hangs under, and a near block's face beats a far block's top
            deps.append(depth[ok] * 4 + (0 if dy < s else 1))
            cols.append(col[ok] * (shade * light[ok])[:, None])
    keys = np.concatenate(keys); deps = np.concatenate(deps); cols = np.concatenate(cols)
    order = np.argsort(deps, kind="stable")
    flat = img.reshape(-1, 3)
    # sorted far to near: assignment keeps the last write, so the nearest block wins each pixel
    flat[keys[order]] = cols[order]
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out)



def elevation(ids, dat, x0, z0, out, box, ymin, ymax, look="north", scale=8):
    """An orthographic elevation of a box: the first block met looking `look` (north/south/east/west),
    shaded darker the further back it stands, so a facade, an arch or a cave mouth reads straight on."""
    bx0, bz0, bx1, bz1 = box
    sub = ids[bx0 - x0:bx1 - x0 + 1, ymin:ymax + 1, bz0 - z0:bz1 - z0 + 1]
    sd = dat[bx0 - x0:bx1 - x0 + 1, ymin:ymax + 1, bz0 - z0:bz1 - z0 + 1]
    if look == "north":      # viewer at +z looking toward -z: columns are x, depth runs z descending
        sub, sd = sub[:, :, ::-1], sd[:, :, ::-1]
    elif look == "south":
        sub, sd = sub[::-1, :, :], sd[::-1, :, :]
    elif look == "west":     # viewer at +x looking -x: columns are z (reversed), depth x descending
        sub, sd = np.transpose(sub[::-1, :, ::-1], (2, 1, 0)), np.transpose(sd[::-1, :, ::-1], (2, 1, 0))
    elif look == "east":
        sub, sd = np.transpose(sub, (2, 1, 0)), np.transpose(sd, (2, 1, 0))
    table = K.COLOURS.astype(np.float32)
    nu, ny, nd = sub.shape
    img = np.zeros((ny, nu, 3), np.float32); img[:] = (205, 220, 235)
    for u in range(nu):
        for y in range(ny):
            col = sub[u, y, :]
            nz = np.nonzero(col)[0]
            if len(nz) == 0:
                continue
            k = nz[0]
            c = table[col[k], sd[u, y, k] & 15] * (1.0 - min(0.6, k * 0.04))
            img[ny - 1 - y, u] = c
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((nu * scale, ny * scale), Image.NEAREST)
    im.save(out)


def cutaway(w, out, pts, ymin=4, ymax=60, scale=4, step=0.5, title=""):
    """A true-scale section along a polyline of (x, z) points: every block the line's vertical plane cuts, in
    its colour; columns off the world drawn dark."""
    x0, z0, ids, dat = w.x0, w.z0, w.ids, w.dat
    table = K.COLOURS
    L = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(L)
    n = int(total / step) + 1
    W, H = n * scale // 2 + 20, (ymax - ymin) * scale + 40
    im = Image.new("RGB", (W, H), (205, 222, 236))
    d = ImageDraw.Draw(im)
    for k in range(n):
        s = k * step
        seg, acc = 0, 0.0
        while seg < len(L) - 1 and acc + L[seg] < s:
            acc += L[seg]
            seg += 1
        t = (s - acc) / L[seg]
        (ax, az), (bx, bz) = pts[seg], pts[seg + 1]
        x, z = ax + (bx - ax) * t, az + (bz - az) * t
        i, j = int(math.floor(x)) - x0, int(math.floor(z)) - z0
        px = 10 + k * scale // 2
        if not (0 <= i < ids.shape[0] and 0 <= j < ids.shape[2]):
            d.rectangle([px, 20, px + scale // 2, H - 20], fill=(25, 25, 30))
            continue
        for y in range(ymin, min(ymax, ids.shape[1])):
            b = int(ids[i, y, j])
            if b == 0:
                continue
            c = tuple(int(v) for v in table[b, int(dat[i, y, j])])
            py = H - 20 - (y - ymin + 1) * scale
            d.rectangle([px, py, px + scale // 2, py + scale - 1], fill=c)
    for y in range(ymin, ymax, 4):
        py = H - 20 - (y - ymin) * scale
        d.line([(0, py), (6, py)], fill=(0, 0, 0))
        d.text((W - 18, py - 6), str(y), fill=(80, 80, 80))
    d.text((10, 4), title, fill=(0, 0, 0))
    im.save(out)

def trim(path, pad=16):
    """Cut the empty sky round a render."""
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad),
                 min(im.height, box[3] + pad))).save(path)
    return path
