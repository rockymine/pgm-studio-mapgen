"""An isometric look at the built volume, the read the round-trip tool does not have: every exposed block a
small cube in an approximate texture colour, seen from one of four corners, cropped to a box.

    python3 render_iso.py <build-dir> <out.png> [--scale 2] [--corner se|sw|ne|nw]
                          [--box x0 z0 x1 z1] [--ymin Y] [--cut]

`--cut` draws only blocks below y = ymax of the box (`--ymax`), so a building's rooms or a cave show.
"""
import argparse
import struct

import numpy as np
from PIL import Image

from mc import B

# approximate block colours (top face), by id then data
BASE = {
    1: (125, 125, 125), 2: (100, 150, 60), 3: (134, 96, 67), 4: (110, 110, 110), 5: (160, 130, 80),
    7: (60, 60, 60), 8: (50, 90, 200), 9: (50, 90, 200), 10: (210, 100, 20), 11: (210, 100, 20),
    12: (219, 207, 163), 13: (136, 126, 126), 14: (143, 140, 125), 15: (136, 130, 127), 16: (115, 115, 115),
    17: (102, 81, 51), 18: (60, 120, 40), 20: (200, 220, 230), 24: (216, 203, 155), 26: (150, 30, 30),
    30: (220, 220, 220), 31: (90, 140, 50), 35: (220, 220, 220), 37: (230, 220, 40), 38: (200, 40, 40),
    39: (150, 110, 80), 40: (190, 30, 30), 41: (250, 220, 70), 42: (220, 220, 220), 43: (160, 160, 160),
    44: (160, 160, 160), 45: (150, 75, 60), 47: (110, 80, 50), 48: (90, 110, 90), 49: (20, 18, 30),
    50: (255, 220, 100), 53: (160, 130, 80), 54: (160, 110, 40), 58: (120, 80, 50), 59: (200, 180, 60),
    60: (110, 75, 45), 61: (100, 100, 100), 63: (160, 130, 80), 64: (140, 110, 60), 65: (150, 120, 70),
    66: (120, 110, 100), 67: (110, 110, 110), 68: (160, 130, 80), 72: (160, 130, 80), 78: (240, 250, 250),
    82: (160, 165, 180), 83: (110, 170, 80), 85: (140, 110, 60), 86: (210, 120, 20), 89: (240, 200, 110),
    91: (220, 140, 30), 96: (130, 100, 60), 98: (122, 121, 122), 101: (100, 100, 100), 102: (200, 220, 230),
    106: (60, 110, 30), 107: (140, 110, 60), 108: (150, 75, 60), 109: (122, 121, 122), 111: (40, 120, 40),
    118: (60, 60, 60), 125: (160, 130, 80), 126: (160, 130, 80), 134: (110, 80, 50), 139: (110, 110, 110),
    140: (120, 60, 40), 71: (200, 200, 200), 141: (60, 150, 40), 142: (60, 150, 40), 144: (200, 200, 200), 145: (60, 60, 60),
    155: (235, 230, 225), 159: (210, 180, 170), 161: (50, 100, 30), 162: (60, 45, 30), 164: (60, 45, 30),
    170: (190, 160, 40), 171: (200, 200, 200), 172: (150, 92, 66), 173: (20, 20, 20), 175: (90, 150, 50),
    95: (236, 240, 246), 160: (236, 240, 246), 168: (100, 160, 150), 169: (210, 235, 225), 183: (110, 80, 50), 188: (110, 80, 50), 191: (60, 45, 30), 193: (110, 80, 50), 197: (60, 45, 30),
}
PLANKS = [(160, 130, 80), (110, 80, 50), (195, 180, 125), (155, 110, 80), (170, 92, 50), (65, 45, 25)]
LOGS = [(102, 81, 51), (60, 45, 28), (215, 215, 205), (85, 68, 25)]
STONE = [(125, 125, 125), (150, 105, 85), (155, 115, 100), (190, 190, 190), (195, 195, 195), (132, 132, 134), (135, 135, 138)]
WOOL = [(230, 230, 230), (230, 125, 55), (180, 70, 190), (100, 140, 210), (195, 180, 40), (65, 175, 55),
        (210, 130, 155), (65, 65, 65), (155, 160, 160), (45, 115, 140), (125, 55, 180), (45, 55, 150),
        (80, 50, 30), (55, 75, 30), (160, 45, 40), (25, 25, 25)]
CLAY = [(210, 178, 161), (162, 84, 38), (150, 88, 109), (113, 109, 138), (186, 133, 35), (104, 118, 53),
        (162, 78, 79), (58, 42, 36), (135, 107, 98), (87, 92, 92), (118, 70, 86), (74, 60, 91), (77, 51, 36),
        (76, 83, 42), (143, 61, 47), (37, 23, 17)]
FLOWERS = [(200, 30, 30), (40, 140, 210), (180, 110, 210), (220, 225, 230), (210, 50, 40), (230, 120, 40),
           (230, 230, 230), (230, 150, 190), (230, 230, 200)]
TRANSPARENT = {0, 36, 55, 78, 31, 37, 38, 39, 40, 50, 59, 83, 106, 141, 142, 175, 30, 32, 6, 65, 66, 27, 63, 68, 69, 77, 143}


def colour_table():
    t = np.zeros((256, 16, 3), dtype=np.float32)
    for i in range(256):
        c = BASE.get(i, (255, 0, 255))
        t[i, :, :] = c
    for d in range(16):
        t[5, d] = PLANKS[d % 6]; t[125, d] = PLANKS[d % 6]; t[126, d] = PLANKS[d % 6]
        t[17, d] = LOGS[d & 3]; t[1, d] = STONE[d % 7]; t[35, d] = WOOL[d]; t[159, d] = CLAY[d]
        t[171, d] = WOOL[d]; t[160, d] = WOOL[d]; t[38, d] = FLOWERS[d % 9]
    t[162, 0] = t[162, 4] = t[162, 8] = t[162, 12] = (105, 100, 90)
    t[18, :] = (70, 125, 45)
    for d in (2, 6, 10, 14):
        t[18, d] = (110, 150, 70)   # birch
    for d in (1, 5, 9, 13):
        t[18, d] = (55, 95, 55)     # spruce
    t[3, 1] = (120, 85, 60); t[3, 2] = (90, 65, 30)
    t[79, :] = (150, 185, 235); t[80, :] = (242, 248, 252); t[174, :] = (165, 195, 240); t[78, :] = (240, 246, 250)
    t[12, 1] = (190, 102, 40); t[179, :] = (184, 98, 42); t[180, :] = (184, 98, 42); t[24, :] = (216, 203, 155)
    t[81, :] = (20, 110, 30); t[32, :] = (120, 90, 50); t[163, :] = (170, 92, 50); t[192, :] = (170, 92, 50)
    t[186, :] = (65, 45, 25); t[2, :] = (110, 150, 85)
    t[98, 1] = (110, 120, 100); t[98, 2] = (115, 115, 115); t[98, 3] = (120, 120, 120)
    t[43, 4] = t[44, 4] = t[44, 12] = (150, 75, 60)
    t[43, 5] = t[44, 5] = t[44, 13] = (122, 121, 122)
    t[44, 3] = t[44, 11] = (110, 110, 110)
    t[24, 2] = (220, 210, 165)
    t[55, :] = (200, 20, 20); t[36, :] = (205, 220, 235)
    t[18, 3] = t[18, 7] = (60, 135, 40)       # tea
    t[168, 0] = (99, 156, 151); t[168, 1] = (99, 171, 158); t[168, 2] = (59, 88, 75)
    t[164, :] = (66, 43, 20); t[162, 1] = t[162, 5] = t[162, 9] = t[162, 13] = (60, 45, 30)
    t[95, :] = (236, 240, 246); t[95, 8] = (190, 195, 200); t[7, :] = (40, 40, 40); t[89, :] = (250, 210, 120)
    return t


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


def load(build_dir):
    with open(f"{build_dir}/volume.bin", "rb") as f:
        assert f.read(4) == b"RWV1"
        x0, y0, z0, sx, sy, sz = struct.unpack("<6i", f.read(24))
        n = sx * sy * sz
        ids = np.frombuffer(f.read(n * 2), dtype="<u2").reshape(sx, sy, sz)
        dat = np.frombuffer(f.read(n), dtype=np.uint8).reshape(sx, sy, sz)
    return x0, z0, ids, dat


def render(ids, dat, x0, z0, out, scale=2, corner="se", box=None, ymin=0, ymax=None, xray=False):
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
    table = colour_table()
    trans = np.zeros(256, bool)
    trans[list(TRANSPARENT)] = True
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("build"); ap.add_argument("out")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--corner", default="se")
    ap.add_argument("--box", type=int, nargs=4)
    ap.add_argument("--ymin", type=int, default=0)
    ap.add_argument("--ymax", type=int)
    ap.add_argument("--xray", action="store_true")
    a = ap.parse_args()
    x0, z0, ids, dat = load(a.build)
    render(ids, dat, x0, z0, a.out, a.scale, a.corner, a.box, a.ymin, a.ymax, a.xray)


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
    table = colour_table()
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
