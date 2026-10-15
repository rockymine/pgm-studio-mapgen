"""Volcano studies: shapes only, every form built from pgmvox's ground operations and shaded in three tones by slope.

    python3 volcanoes.py [name ...]      # all of them by default; renders into ../renders/round1
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.geom import noise                                                 # noqa: E402
from pgmvox.geom.noise import smoothstep                                      # noqa: E402
from pgmvox.geom.shapes import polyline, ellipse_distance                     # noqa: E402
from pgmvox.ground import landform as L                                       # noqa: E402
from pgmvox.ground.field import mix                           # noqa: E402
from pgmvox.read import render                                                # noqa: E402
from pgmvox.surface.terrain import slope_deg                                  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "round1")
SIZE, SY, BASE = 300, 256, 10
TONES = ((B.WOOL, 0), (B.WOOL, 8), (B.WOOL, 7))            # gentle, steep, cliff: three greys


def grid():
    w = World(-SIZE // 2, -SIZE // 2, SIZE, SIZE, sy=SY)
    X, Z = w.grid()
    return w, X.astype(float), Z.astype(float)


def plain(X, seed=1, rise=4):
    """Rolling low ground the volcano stands on."""
    return BASE + rise * (0.5 + 0.5 * noise.fbm(X.shape, 60, 4, seed=seed))


def radius(X, Z, c=(0, 0)):
    return np.hypot(X - c[0], Z - c[1])


def gullies(X, Z, c, count, depth, r0, r1, seed, width=3.0):
    """The depth landform.gullies cuts, as a field to subtract."""
    return -L.gullies(np.zeros(np.shape(X)), X, Z, c, count, depth, r0, r1, sharpness=width, seed=seed)


def cone(X, Z, c, r, top, power, base):
    """A cone from `base` at radius r to `top` at the centre: power > 1 is concave like a stratovolcano's flanks."""
    d = radius(X, Z, c)
    return base + (top - base) * np.clip(1 - d / r, 0, 1) ** power


def summit_crater(H, X, Z, c, r, depth, flat=0.35, slope=1.6):
    d = radius(X, Z, c)
    rim = float(H[np.unravel_index(np.argmin(np.abs(d - r)), H.shape)])
    floor = rim - depth
    shaped = L.crater(H, d, floor, r, flat=flat * r, slope=slope)
    return np.where(d <= r + 6, L.smooth_min(H, shaped, 3), H)              # round the lip, leave the rest


def flow(H, X, Z, pts, width, thick, seed):
    """A lava flow lobe: a tongue `thick` blocks over the ground along pts, a steep blunt front at the end."""
    d, along = polyline(X, Z, pts)
    total = float(along.max())
    edge = width * (0.75 + 0.35 * noise.fbm(X.shape, 10, 2, seed=seed))
    across = smoothstep(edge, edge - 2.5, d)
    front = smoothstep(total + 1, total - 4, along)
    lump = 1 + 0.35 * noise.fbm(X.shape, 6, 2, seed=seed + 3)
    return H + thick * across * front * lump


# --- the studies ------------------------------------------------------------------------------------------------

def stratovolcano(X, Z):
    """Fuji-like: one tall concave cone, radial gullies, a summit crater, a parasitic cone on the flank."""
    H = plain(X)
    c = (0, 0)
    body = cone(X, Z, c, 145, 140, 1.5, BASE)
    body -= gullies(X, Z, c, 26, 6, 18, 135, seed=4)
    H = L.smooth_max(H, body, 6)
    H = summit_crater(H, X, Z, c, 13, 16)
    pc = (62, 36)
    H = H + 15 * np.clip(1 - radius(X, Z, pc) / 20, 0, 1) ** 0.9          # a cone built onto the flank, not on a plinth
    H = summit_crater(H, X, Z, pc, 5, 5, slope=1.2)
    return H


def shield(X, Z):
    """Mauna-Loa-like: a broad low dome, a caldera with pit craters, two rift zones and lava flow lobes."""
    H = plain(X, seed=2)
    c = (0, 0)
    e = ellipse_distance(X, Z, c, 140, 115, angle=25)
    H = L.mound(H, e, 52, power=2.2)                                      # a convex dome
    for a, b in (((-10, 0), (-140, -70)), ((10, 0), (140, 60))):         # rift zones: a raised spine, gone at the foot
        d, _ = polyline(X, Z, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 12), b])
        H = H + 6 * smoothstep(14, 0, d) * smoothstep(1.0, 0.6, e)
    d = ellipse_distance(X, Z, (0, 0), 30, 22, angle=25)
    H = L.smooth_min(H, L.crater(H, d * 30, float(H[150, 150]) - 18, 30, flat=20, slope=4), 2)   # the caldera
    for pc, r, depth in (((-30, -14), 8, 10), ((-55, -26), 6, 8), ((40, 20), 9, 12), ((66, 32), 5, 6)):
        d = radius(X, Z, pc)
        H = L.crater(H, d, float(H[150 + pc[0], 150 + pc[1]]) - depth, r, flat=r * 0.4, slope=3)
    for k, pts in enumerate([[(20, 30), (40, 75), (35, 110), (55, 140)],
                             [(-25, 25), (-55, 60), (-70, 105)],
                             [(-30, -40), (-20, -85), (-45, -125)],
                             [(45, -15), (95, -30), (130, -65)]]):
        H = flow(H, X, Z, pts, 9 + 2 * k % 5, 3, seed=30 + k)
    return H


def caldera_lake(X, Z):
    """Crater-Lake-like: a truncated massif, a wide caldera ringed by stepped fault cliffs, a young cone inside."""
    H = plain(X, seed=3)
    c = (0, 0)
    body = cone(X, Z, c, 140, 120, 1.35, BASE) - gullies(X, Z, c, 30, 5, 70, 135, seed=8)
    H = L.smooth_max(H, body, 6)
    d = radius(X, Z, c) * (1 + 0.08 * noise.fbm(X.shape, 30, 3, seed=9))
    jag = 2.5 * noise.fbm(X.shape, 8, 2, seed=10)
    H = L.profile(H, d, floor=34, steps=[L.Step(44, 50, 62), L.Step(56, 64, "ground")], jag=jag,
                  talus=(5, 8), mode="cut")
    isle = (-14, 10)
    H = L.smooth_max(H, np.where(radius(X, Z, isle) < 16, cone(X, Z, isle, 16, 58, 0.9, 30), -1e9), 3)
    H = summit_crater(H, X, Z, isle, 4, 4, slope=1.3)
    return H


def cinder_field(X, Z):
    """A field of steep cinder cones, two breached with a lava tongue out of the breach."""
    H = plain(X, seed=4, rise=8)
    cones = [((0, 0), 34, 46, None), ((-70, -50), 22, 28, (-1, 1)), ((60, -60), 18, 22, None),
             ((80, 45), 26, 34, (1, 1)), ((-60, 70), 14, 16, None), ((-100, 10), 11, 12, None), ((20, 95), 12, 13, None)]
    for k, (c, r, rise, breach) in enumerate(cones):
        base = float(H[150 + c[0], 150 + c[1]])
        d = radius(X, Z, c) * (1 + 0.05 * noise.fbm(X.shape, 10, 2, seed=40 + k))
        body = base + rise * np.clip(1 - d / r, 0, 1) ** 0.85              # straight-sided, about 33 degrees
        H = L.smooth_max(H, np.where(d < r, body, -1e9), 3)
        cr = 0.32 * r
        H = L.crater(H, radius(X, Z, c), base + rise * 0.55, cr + 0.18 * r, flat=0.25 * cr, slope=1.4)
        if breach:
            out = (c[0] + breach[0] * r * 1.4, c[1] + breach[1] * r * 1.4)
            H = L.canyon(H, X, Z, [c, out], width=0.6 * r, depth=0.45 * rise, floor=0.3, wall=1.4, downhill=True,
                         lowest=base + 1)
            far = (c[0] + breach[0] * r * 3.4, c[1] + breach[1] * r * 2.6)
            H = flow(H, X, Z, [c, out, far], 0.35 * r, 3, seed=50 + k)
    return H


def volcanic_neck(X, Z):
    """Shiprock-like: the eroded throat of a volcano, a ragged fluted plug on its talus, dikes radiating out as
    standing walls, and the last mesas of the plateau that once buried it."""
    H = plain(X, seed=5, rise=8)
    for k, (c, r, top) in enumerate([((-110, -95), 26, 52), ((115, -105), 20, 44), ((-120, 110), 16, 38)]):
        H = L.butte(H, X, Z, c, r, top, cliff=2, talus=10, talus_height=0.35, jag=0.18, seed=110 + k)
    H = L.mound(H, ellipse_distance(X, Z, (0, 0), 60, 52) + 0.15 * noise.fbm(X.shape, 12, 3, seed=6), 22, power=1.2)
    plug = H.copy()
    rng = np.random.default_rng(61)
    for k in range(9):                                                    # a cluster of pinnacles: a jagged crown
        ang, dist = rng.uniform(0, 2 * np.pi), (0 if k == 0 else rng.uniform(5, 16))
        c = (dist * np.cos(ang), dist * np.sin(ang))
        top = 150 if k == 0 else rng.uniform(85, 135)
        plug = L.spire(plug, X, Z, c, 22 if k == 0 else rng.uniform(8, 14), top, taper=1.5 if k == 0 else 1.15,
                       jag=0.35, seed=60 + k)
    theta = np.arctan2(Z, X)
    flutes = (1 - np.abs(np.sin(theta * 18 + 1.2 * noise.fbm(X.shape, 20, 2, seed=64)))) ** 3
    rise = plug - H
    H = H + rise * (1 - 0.18 * flutes * smoothstep(5, 30, rise))          # columns down the plug's sides
    for k, (pts, height) in enumerate([([(0, 0), (40, 35), (90, 50), (145, 95)], 20),
                                       ([(0, 0), (-50, 25), (-125, 42)], 15),
                                       ([(0, 0), (15, -60), (5, -140)], 12)]):
        d, along = polyline(X, Z, pts)
        total = float(along.max())
        crest = height * (1 - 0.6 * along / total) + 4 * noise.ridged(X.shape, 6, 2, seed=70 + k, sharpness=2)
        broken = smoothstep(-0.45, -0.25, noise.fbm(X.shape, 16, 2, seed=80 + k))  # eroded through in places
        wall = crest * smoothstep(3.0, 1.0, d) * broken * smoothstep(8, 22, along)
        H = np.maximum(H, H + wall)
    return H


def horseshoe(X, Z):
    """St-Helens-like: a cone whose north flank blew out, a horseshoe crater, a dome inside, hummocks in the fan."""
    H = plain(X, seed=6)
    c = (0, 20)
    body = cone(X, Z, c, 125, 150, 1.7, BASE) - gullies(X, Z, c, 22, 5, 30, 120, seed=12)
    H = L.smooth_max(H, body, 6)
    open_n = ellipse_distance(X, Z, (0, -12), 28, 52)                      # the blown-out amphitheatre
    floor = 70 + 0.45 * (Z - 20)                                          # its floor falls away north
    wall = 1 + 0.12 * noise.fbm(X.shape, 10, 2, seed=13)
    H = np.where(open_n < wall, np.minimum(H, floor + 60 * np.clip(open_n - 0.55, 0, 1) ** 1.6), H)
    H = L.smooth_min(H, H, 0)
    dome = ellipse_distance(X, Z, (0, 12), 14, 12) + 0.15 * noise.fbm(X.shape, 4, 2, seed=14)
    H = L.mound(H, dome, 18, power=4)                                      # a squat lava dome
    rng = np.random.default_rng(15)
    for k in range(70):                                                   # debris avalanche hummocks
        x, z = rng.normal(0, 38), rng.uniform(-145, -55)
        e = ellipse_distance(X, Z, (x, z), rng.uniform(3, 9), rng.uniform(3, 7), angle=rng.uniform(0, 180))
        H = L.mound(H, e, rng.uniform(2, 7), power=2)
    return H


def somma(X, Z):
    """Vesuvius-like: the broken rim of an old caldera half round a young cone, a moat valley between them."""
    H = plain(X, seed=7)
    c = (0, 0)
    old = cone(X, Z, c, 145, 150, 1.6, BASE) - gullies(X, Z, c, 34, 6, 60, 140, seed=16)
    old = L.smooth_max(H, old, 6)
    d = radius(X, Z, c) * (1 + 0.05 * noise.fbm(X.shape, 12, 2, seed=18))
    cut = L.profile(old, d, floor=52, steps=[L.Step(46, 56, "ground")], jag=2 * noise.fbm(X.shape, 6, 2, seed=19),
                    talus=(4, 10), mode="cut")
    theta = np.arctan2(Z, X)
    keep = smoothstep(-0.35, 0.35, -np.sin(theta + 0.4) + 0.3 * noise.fbm(X.shape, 30, 2, seed=17))   # rim kept north
    buried = np.minimum(cut, L.smooth_max(H, cone(X, Z, c, 145, 70, 1.2, BASE), 6))  # the south rim long buried
    H = mix(buried, cut, keep)
    yc = (6, 10)
    young = cone(X, Z, yc, 40, 140, 1.15, 50) - gullies(X, Z, yc, 14, 3, 10, 38, seed=20)
    H = L.smooth_max(H, np.where(radius(X, Z, yc) < 40, young, -1e9), 5)
    H = summit_crater(H, X, Z, yc, 9, 12, slope=1.5)
    return H


def maar(X, Z):
    """A maar and two tuff rings: a ring of ejecta, thrown farther downwind, round a crater cut far below the plain,
    its inner walls slumped into benches."""
    H = plain(X, seed=8) + 30
    wind = (0.8, 0.4)                                                     # ejecta thrown farther toward +x
    for k, (c, r, ring, depth) in enumerate([((-20, 0), 55, 16, 38), ((78, 72), 26, 10, 20), ((82, -70), 18, 7, 14)]):
        ground = float(H[150 + c[0], 150 + c[1]])
        d = radius(X, Z, c) * (1 + 0.06 * noise.fbm(X.shape, 16, 2, seed=90 + k))
        lean = ((X - c[0]) * wind[0] + (Z - c[1]) * wind[1]) / max(d.max(), 1) * 3
        reach = 0.35 * r * (1 + 0.6 * np.clip(lean, -0.5, 1))
        H = H + ring * np.exp(-((d - r) / reach) ** 2) * (d > r * 0.6)
        H = L.crater(H, d, ground - depth, r, flat=0.5 * r, slope=2.4)
        H = L.terraces(H, d < r * 0.97, step=5, riser=0.75)               # slump benches on the inner wall
    return H


def lava_dome(X, Z):
    """A lava dome: overlapping bulbous lobes of stiff lava, the crust cracked into blocks, a talus apron round
    the foot, and a spine thrust out of the top."""
    H = plain(X, seed=9)
    lobes = []
    for k, (c, rx, rz, a, rise) in enumerate([((0, 0), 52, 44, -20, 60), ((-34, 26), 34, 26, 40, 44),
                                              ((38, 18), 30, 24, -60, 38), ((10, -40), 28, 22, 10, 34)]):
        e = ellipse_distance(X, Z, c, rx, rz, angle=a) + 0.08 * noise.fbm(X.shape, 12, 3, seed=21 + k)
        lobes.append(rise * (1 - np.clip(e, 0, 1) ** 3.2))
    dome = L.join(lobes, p=4)
    crack = noise.ridged(X.shape, 8, 2, seed=25, sharpness=6)
    dome = dome - 5 * crack * smoothstep(8, 20, dome)
    apron = 12 * (1 - np.clip(ellipse_distance(X, Z, (0, 0), 95, 85, angle=-20), 0, 1) ** 1.2)
    H = H + np.maximum(dome, apron)
    H = L.terraces(H, H > 50, step=3, riser=0.7)
    H = L.spire(H, X, Z, (-6, 4), 10, 118, taper=1.1, jag=0.3, seed=23, rz=6, angle=35)
    return H


def fissure(X, Z):
    """A fissure eruption: a rift valley dropped between fault walls, the open crack down its floor, a row of
    spatter cones along it, some merged into ramparts, and lava flows out over the rim."""
    H = plain(X, seed=10, rise=6) + 30
    line = [(-150, -100), (-60, -40), (20, 10), (90, 60), (150, 105)]
    d, along = polyline(X, Z, line)
    jag = 2 * noise.fbm(X.shape, 8, 2, seed=101)
    H = L.profile(H, d, floor=float(H.mean()) - 14, steps=[L.Step(22, 27, "ground")], jag=jag, mode="cut")
    cones = []
    for k, s in enumerate(np.linspace(0.06, 0.94, 13)):
        idx = np.argmin(np.abs(along - s * along.max()) + 1000 * (d > 1.2))
        cx, cz = X.flat[idx], Z.flat[idx]
        r = 6 + 6 * abs(np.sin(k * 2.3))
        cones.append(((cx, cz), r, 0.85 * r))
    rises = [np.where(radius(X, Z, c) < r, h * np.clip(1 - radius(X, Z, c) / r, 0, 1) ** 0.9, 0) for c, r, h in cones]
    H = H + L.join(rises, p=3)                                            # neighbours melt into ramparts
    for c, r, h in cones:
        H = summit_crater(H, X, Z, c, 0.35 * r, 0.5 * h, slope=1.3)
    H = np.where(d < 1.5, H - 8, H)                                       # the open crack
    for k, pts in enumerate([[(20, 10), (-10, 60), (-40, 125)], [(-60, -40), (-20, -100), (10, -140)]]):
        H = flow(H, X, Z, pts, 13, 3, seed=100 + k)
    return H


def tuya(X, Z):
    """A tuya, the fire-and-ice volcano: it erupted under a glacier, so it rose as a flat-topped table with sheer
    sides where the ice held it in, a talus apron below, and a small cone on top that broke through the ice."""
    H = plain(X, seed=11, rise=6)
    H = L.butte(H, X, Z, (0, 0), 62, 92, cliff=4, talus=26, talus_height=0.42, jag=0.14, seed=120, rz=48, angle=15)
    H = L.terraces(H, H > 40, step=7, riser=0.8)                           # the lava-delta benches in its walls
    top = (-10, 6)
    H = L.smooth_max(H, np.where(radius(X, Z, top) < 30, cone(X, Z, top, 30, 124, 1.1, 92), -1e9), 3)
    H = summit_crater(H, X, Z, top, 6, 6, slope=1.3)
    for k, c in enumerate([(90, 70), (-95, -60)]):                         # two smaller tuyas, one half eroded
        H = L.butte(H, X, Z, c, 22 - 6 * k, 46 - 8 * k, cliff=3, talus=12, talus_height=0.45, jag=0.2, seed=125 + k)
    return H


def floating(X, Z):
    """A floating volcanic island over the void: a cone on a ragged island, its crater breached toward a lava
    channel to the edge, and the island's underside hanging in tapering roots. Returns (top, bottom)."""
    from pgmvox.surface.terrain import root_depth
    land = ellipse_distance(X, Z, (0, 0), 130, 105, angle=-15) + 0.12 * noise.fbm(X.shape, 18, 3, seed=130) < 1
    H = np.full(X.shape, 120.0) + 4 * noise.fbm(X.shape, 30, 3, seed=131)
    c = (14, -10)
    body = cone(X, Z, c, 58, 190, 1.35, 118) - gullies(X, Z, c, 16, 4, 12, 56, seed=132)
    H = L.smooth_max(H, body, 5)
    H = summit_crater(H, X, Z, c, 9, 12)
    H = H + 12 * np.clip(1 - radius(X, Z, (-60, 40)) / 18, 0, 1) ** 0.9  # a small cone on the island's plain
    H = summit_crater(H, X, Z, (-60, 40), 4, 5, slope=1.3)
    H = L.canyon(H, X, Z, [c, (60, 30), (120, 60)], width=12, depth=9, floor=0.3, wall=1.6, downhill=True,
                 lowest=114)
    depth = root_depth(land, cone=1.6, power=0.95, rough=0.45, flutes=8, spires=30, cap=70, seed=133)
    bottom = np.where(land, 120 - depth, SY)
    return np.where(land, H, -1), bottom



STUDIES = [stratovolcano, shield, caldera_lake, cinder_field, volcanic_neck, horseshoe, somma, maar, lava_dome,
           fissure, tuya, floating]


def build(H, bottom=None):
    """Lay the heights as solid ground (from `bottom` up where given, nothing where the top is below 0), its top
    three blocks toned by slope."""
    w, X, Z = grid()
    land = H >= 0
    top = np.where(land, np.clip(np.round(H), 1, SY - 2), -1).astype(int)
    deg = slope_deg(np.where(land, top, 0), mask=land)
    tone = np.where(deg < 30, 0, np.where(deg < 50, 1, 2))
    ys = np.arange(SY)[None, :, None]
    t = top[:, None, :]
    b = (np.zeros_like(top) if bottom is None else np.round(bottom).astype(int))[:, None, :]
    w.ids[...] = np.where((ys <= t) & (ys >= b), B.STONE, 0)
    skin = (ys <= t) & (ys > t - 3) & (ys >= b)
    ids = np.array([TONES[k][0] for k in range(3)], dtype=np.uint16)[tone][:, None, :]
    dat = np.array([TONES[k][1] for k in range(3)], dtype=np.uint8)[tone][:, None, :]
    w.ids[...] = np.where(skin, ids, w.ids)
    w.dat[...] = np.where(skin, dat, 0)
    return w, top, deg


def plan_view(top, out, title, scale=3):
    """The heights from above: hillshade lit from the north-west, tinted by height, contours every 10 blocks."""
    from PIL import Image, ImageDraw
    land = top >= 0
    h = np.where(land, top, np.nan).astype(float)
    gx, gz = np.gradient(np.nan_to_num(h, nan=0.0))
    az, alt = np.radians(315), np.radians(40)
    slope = np.arctan(np.hypot(gx, gz))
    aspect = np.arctan2(-gz, gx)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    lo, hi = np.nanmin(h), np.nanmax(h)
    tint = (h - lo) / max(hi - lo, 1)
    v = np.clip(0.25 + 0.75 * shade, 0, 1) * (0.72 + 0.28 * tint)
    img = np.stack([v * 235, v * 232, v * 226], -1)
    cont = (np.floor(h / 10) != np.floor(np.roll(h, 1, 0) / 10)) | (np.floor(h / 10) != np.floor(np.roll(h, 1, 1) / 10))
    img[cont & land] *= 0.55
    img[~land] = (32, 34, 44)
    im = Image.fromarray(np.nan_to_num(img).astype(np.uint8).transpose(1, 0, 2)).resize(
        (top.shape[0] * scale, top.shape[1] * scale), Image.NEAREST)
    ImageDraw.Draw(im).text((8, 6), f"{title}  (north up; contours every 10; y {int(lo)}..{int(hi)})", fill=(0, 0, 0))
    im.save(out)


CORNER = {"horseshoe": "nw", "fissure": "sw", "lava_dome": "sw", "somma": "ne"}


def sheet(names, out, cols=3):
    """Every study's iso render in a grid, captioned."""
    from PIL import Image, ImageDraw
    tiles = [Image.open(f"{OUT}/{n}-iso.png").convert("RGB") for n in names]
    tw = 600
    tiles = [t.resize((tw, int(t.height * tw / t.width))) for t in tiles]
    th = max(t.height for t in tiles) + 24
    rows = (len(tiles) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, rows * th), (205, 220, 235))
    d = ImageDraw.Draw(im)
    for k, (n, t) in enumerate(zip(names, tiles)):
        x, y = (k % cols) * tw, (k // cols) * th
        im.paste(t, (x, y + 22))
        d.text((x + 10, y + 6), f"{k + 1}. {n.replace('_', ' ')}", fill=(0, 0, 0))
    im.save(out)


def main(names):
    os.makedirs(OUT, exist_ok=True)
    done = []
    for f in STUDIES:
        if names and f.__name__ not in names:
            continue
        n = f.__name__
        X, Z = grid()[1:]
        got = f(X, Z)
        H, bottom = got if isinstance(got, tuple) else (got, None)
        w, top, deg = build(H, bottom)
        ymin = 0 if bottom is None else max(0, int(np.min(bottom[top >= 0])))
        render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-iso.png", scale=2, corner=CORNER.get(n, "se"), ymin=ymin)
        render.trim(f"{OUT}/{n}-iso.png")
        plan_view(top, f"{OUT}/{n}-plan.png", n)
        if bottom is not None:
            render.elevation(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-side.png", (w.x0, w.z0, w.x0 + SIZE - 1,
                             w.z0 + SIZE - 1), ymin, int(top.max()) + 4, look="north", scale=2)
        render.cutaway(w, f"{OUT}/{n}-section.png", [(-150, 0), (149, 0)], ymin=ymin,
                       ymax=int(top.max()) + 8, scale=2, step=1.0, title=f"{n}: section west to east along z 0")
        land = top >= 0
        print(f"{n:15s} top {top.max():4d}  floor {top[land].min():3d}  "
              f"steep>=30 {np.mean(deg[land] >= 30) * 100:4.1f}%  cliff>=50 {np.mean(deg[land] >= 50) * 100:4.1f}%")
        done.append(n)
    if not names:
        sheet(done, f"{OUT}/00-sheet.png")


if __name__ == "__main__":
    main(sys.argv[1:])
