"""The map style: a hypsometric ramp, light from the north-west, a contour every `step` blocks, a pink outline
for what a step changed, and five colours for the kinds of geometry a shape is written as."""
import numpy as np
from scipy import ndimage

VOID = np.array([24, 26, 34])
CHANGED = np.array([255, 64, 160])
HYPSO = [(36, (38, 70, 72)), (44, (66, 112, 82)), (48, (104, 144, 86)), (51, (150, 170, 92)), (54, (196, 186, 106)),
         (58, (206, 160, 96)), (64, (170, 118, 78)), (72, (198, 170, 140)), (82, (240, 234, 222))]
KIND = dict(ell=(214, 51, 108), line=(30, 110, 200), poly=(222, 120, 20), noise=(120, 60, 170), band=(70, 70, 70))


def hypso(H):
    ys = [y for y, _ in HYPSO]; cs = np.array([c for _, c in HYPSO], float)
    return np.stack([np.interp(H, ys, cs[:, c]) for c in range(3)], -1)


def ramp(H, lo, hi, stops):
    t = np.clip((H - lo) / ((hi - lo) or 1), 0, 1)[..., None]
    n = len(stops) - 1
    idx = np.clip(t * n, 0, n - 0.001); j = idx.astype(int)[..., 0]; f = idx - j[..., None]
    return stops[j] * (1 - f) + stops[j + 1] * f


def shade(H):
    """Light from the north-west, the top-left of every picture: faces turned toward it are lit."""
    gx, gz = np.gradient(H.astype(float))
    return np.clip(1 + 0.16 * (gx + gz), 0.6, 1.3)[..., None]


def up(rgb, s):
    return np.repeat(np.repeat(rgb, s, 0), s, 1)


def contours(img, H, mask, step=2, major=10, s=4, dark=0.55):
    """Darken the pixel edge between two cells whose heights fall in different `step` bands; doubled where a
    `major` band is crossed."""
    band, big = np.floor(H / step), np.floor(H / major)
    for axis in (0, 1):
        a, b = [slice(None)] * 2, [slice(None)] * 2
        a[axis], b[axis] = slice(0, -1), slice(1, None)
        cross = (band[tuple(a)] != band[tuple(b)]) & mask[tuple(a)] & mask[tuple(b)]
        heavy = cross & (big[tuple(a)] != big[tuple(b)])
        for i, k in zip(*np.nonzero(cross)):
            w = 2 if heavy[i, k] else 1
            if axis == 0: img[(i + 1) * s - w:(i + 1) * s + (w - 1), k * s:(k + 1) * s] *= dark
            else: img[i * s:(i + 1) * s, (k + 1) * s - w:(k + 1) * s + (w - 1)] *= dark
    return img


def outline(img, ch, s, colour=CHANGED, tint=0.25):
    if ch is None or not ch.any(): return img
    big = up(ch[..., None].astype(float), s)[..., 0] > 0.5
    edge = big & ~ndimage.binary_erosion(big, iterations=2)
    img[big] = img[big] * (1 - tint) + colour * tint
    img[edge] = colour
    return img


def relief(H, mask, s=4, step=2, major=10):
    img = up(np.where(mask[..., None], hypso(H) * shade(H), VOID), s)
    return contours(img, H, mask, step, major, s)
