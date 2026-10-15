"""Round two: the studies the author kept, every outline warped so nothing is a perfect circle or a ruled line, every
form footed into rolling ground, and the fissure and the tuya rebuilt from the notes.

    python3 round2.py [name ...]      # renders into ../renders/round2
"""
import os
import sys

import numpy as np

import volcanoes as V
from volcanoes import L, noise, smoothstep, polyline, ellipse_distance, mix, render, grid, gullies, flow

V.OUT = OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "round2")


# --- the wiggle ---------------------------------------------------------------------------------------------------

warp = noise.warp


def r_at(Xw, Zw, c, stretch=1.0, angle=0.0):
    """Distance from c in the warped frame, as an ellipse `stretch` long across z, turned `angle` degrees."""
    dx, dz = Xw - c[0], Zw - c[1]
    if angle:
        a = np.radians(angle)
        dx, dz = dx * np.cos(a) + dz * np.sin(a), -dx * np.sin(a) + dz * np.cos(a)
    return np.hypot(dx, dz / stretch)


def ground(X, seed, rise=14, base=10):
    """Rolling ground with real relief: broad swells and smaller knolls, so a form has something to melt into."""
    return base + rise * (0.5 + 0.5 * noise.fbm(X.shape, 90, 4, seed=seed)) + 3 * noise.fbm(X.shape, 25, 3, seed=seed + 9)


def foot(H, form, k=14):
    """A form grown out of the ground with a wide rounded foot."""
    return L.smooth_max(H, form, k)


def at(H, x, z):
    return float(H[150 + int(round(x)), 150 + int(round(z))])


def crater_in(H, d, depth, r, flat, slope, k=4, rough=None):
    """A crater cut at the rim height found at radius r of the distance field d, its floor `depth` under that rim."""
    rim = float(np.median(H[np.abs(d - r) < 1.5]))
    floor = rim - depth if rough is None else rim - depth + rough
    return np.where(d <= r + 2 * k, L.smooth_min(H, L.crater(H, d, floor, r, flat=flat, slope=slope), k), H)  # lip only


lumps = L.lumps


# --- the studies ---------------------------------------------------------------------------------------------------

def stratovolcano(X, Z):
    """The cone, now leaning: its summit off centre, its foot wandering, gullies that bend, a shoulder on one side
    where an older vent was buried, and a flank cone growing out of the slope."""
    H = ground(X, 1)
    Xw, Zw = warp(X, Z, 200, big=18, small=5)
    c = (-6, 4)
    d = r_at(Xw, Zw, c, stretch=0.88, angle=20)
    d = d * (1 + 0.12 * np.clip((X - c[0]) / 150, -1, 1))                  # the summit sits off centre: east is longer
    body = 12 + 128 * np.clip(1 - d / 150, 0, 1) ** 1.55
    body -= gullies(Xw, Zw, c, 24, 7, 20, 140, seed=4, width=2.5)
    sh = r_at(Xw, Zw, (-48, -38), stretch=0.7, angle=-30)                  # a buried older vent: a shoulder
    body = L.join([body - 12, 82 * np.clip(1 - sh / 55, 0, 1) ** 1.3], p=5) + 12
    H = foot(H, body, 18)
    H = crater_in(H, r_at(Xw, Zw, c, 0.85), 15, 12, 4, 1.5, rough=2 * noise.fbm(X.shape, 6, 2, seed=5))
    pc = (64, 40)
    pr = r_at(Xw, Zw, pc, 0.8, 50)
    H = H + 15 * np.clip(1 - pr / 22, 0, 1) ** 1.1
    H = crater_in(H, pr, 6, 5, 1, 1.2, k=2)
    return H


def caldera_lake(X, Z):
    """The caldera, unruled: an outline that bulges and pinches, a rim that dips to a notch, cliffs that are sheer in
    one stretch and broken into benches in the next, slump blocks fallen to the floor, the island off to one side."""
    H = ground(X, 3)
    Xw, Zw = warp(X, Z, 210, big=12, small=4)
    c = (0, 0)
    d0 = r_at(Xw, Zw, c, 0.9, 30)
    body = 12 + 108 * np.clip(1 - d0 / 145, 0, 1) ** 1.35 - gullies(Xw, Zw, c, 30, 6, 70, 135, seed=8)
    H = foot(H, body, 16)
    theta = np.arctan2(Zw, Xw)
    notch = 14 * np.exp(-((np.angle(np.exp(1j * (theta - 2.3)))) / 0.25) ** 2)   # the rim's low point
    H = H - notch * smoothstep(80, 55, d0) * smoothstep(30, 55, d0)
    dc = r_at(Xw, Zw, c, 0.82, 30) * (1 + 0.1 * noise.fbm(X.shape, 40, 3, seed=9))
    width = 6 + 6 * (0.5 + 0.5 * noise.fbm(X.shape, 60, 2, seed=11))        # cliffs wider (gentler) in places
    jag = 3 * noise.fbm(X.shape, 9, 2, seed=10)
    floor = 30 + 4 * noise.fbm(X.shape, 30, 2, seed=12)
    H = L.profile(H, dc, floor=30, floor_ground=floor, steps=[L.Step(42, 42 + width, 58),
                                                              L.Step(52 + width * 0.6, 58 + width, "ground")],
                  jag=jag, talus=(6, 9), mode="cut")
    inside = dc < 48
    H = lumps(H, X, Z, 26, (-50, -45, 50, 45), (3, 8), (3, 8), seed=13, mask=inside & (dc > 30))   # slump blocks
    isle = (-18, 14)
    ir = r_at(Xw, Zw, isle, 0.75, 70)
    H = foot(H, np.where(ir < 17, 30 + 26 * np.clip(1 - ir / 17, 0, 1) ** 0.95, -1e9), 4)
    H = crater_in(H, ir, 5, 4, 1, 1.3, k=2)
    return H


def horseshoe(X, Z):
    """The blown-out cone, its amphitheatre now a steep slope rather than a wall, falling into a chute that pours the
    rubble down the breach, across the foot and out over the plain in streams of elongated hummocks."""
    H = ground(X, 6)
    Xw, Zw = warp(X, Z, 220, big=14, small=4)
    c = (0, 25)
    d = r_at(Xw, Zw, c, 0.9, -15)
    body = 12 + 118 * np.clip(1 - d / 130, 0, 1) ** 1.6 - gullies(Xw, Zw, c, 22, 6, 30, 120, seed=12)
    H = foot(H, body, 16)
    amph = ellipse_distance(Xw, Zw, (2, -8), 30, 56, angle=-8)               # the scar, opening north
    floor = 66 + 0.5 * (Zw - 20)                                          # its floor falls away north
    scar = floor + 70 * np.clip(amph - 0.35, 0, None) ** 1.25             # walls at about 40 to 55 degrees
    H = np.where(amph < 1.25, L.smooth_min(H, scar, 8), H)
    dome = r_at(Xw, Zw, (2, 14), 0.8, 20) / 13
    H = L.mound(H, dome + 0.2 * noise.fbm(X.shape, 4, 2, seed=14), 14, power=2.5)
    rng = np.random.default_rng(15)
    out = Zw < -20
    for k, (x0, angle) in enumerate([(-30, 100), (0, 90), (28, 78), (-55, 110)]):   # streams of hummocks
        for j in range(18):
            t = rng.uniform(0, 1)
            z = -25 - t * 120
            x = x0 + (z + 25) * np.cos(np.radians(angle)) * 0.6 + rng.normal(0, 7)
            if not -145 < x < 145:
                continue
            size = 9 * (1 - 0.55 * t)
            e = ellipse_distance(X, Z, (x, z), size * rng.uniform(0.4, 0.7), size, angle=90 - angle + rng.uniform(-20, 20))
            e = e + 0.3 * noise.fbm(X.shape, 4, 2, seed=300 + 20 * k + j)
            H = L.mound(H, e, rng.uniform(3, 9) * (1 - 0.5 * t), power=1.7)
    H = lumps(H, X, Z, 30, (-35, -40, 35, 10), (3, 6), (2, 5), seed=16, mask=amph < 1.0)   # rubble left in the chute
    return H


def somma(X, Z, young_r=26, young_top=92, seed=7):
    """The broken rim, the favourite: an old caldera wall standing round the north, ragged, notched, its inner face a
    cliff and its outer face gullied; a small young cone inside, sitting low in the moat, with a lava flow that ran
    out through the gap where the southern rim was buried."""
    H = ground(X, seed)
    Xw, Zw = warp(X, Z, 230 + seed, big=14, small=4)
    c = (0, 0)
    d = r_at(Xw, Zw, c, 0.9, 10)
    old = 12 + 138 * np.clip(1 - d / 148, 0, 1) ** 1.6 - gullies(Xw, Zw, c, 36, 7, 60, 142, seed=16)
    old = foot(H, old, 16)
    dc = d * (1 + 0.07 * noise.fbm(X.shape, 25, 3, seed=18))
    jag = 4 * noise.fbm(X.shape, 7, 2, seed=19)
    cut = L.profile(old, dc, floor=50, floor_ground=48 + 3 * noise.fbm(X.shape, 20, 2, seed=21),
                    steps=[L.Step(46, 54, "ground")], jag=jag, talus=(6, 12), mode="cut")
    theta = np.arctan2(Zw, Xw)
    keep = smoothstep(-0.3, 0.45, -np.sin(theta + 0.4) + 0.45 * noise.fbm(X.shape, 28, 3, seed=17))
    buried = np.minimum(cut, foot(H, 12 + 58 * np.clip(1 - d / 148, 0, 1) ** 1.2, 16))
    H = mix(buried, cut, keep)
    H = H - 10 * np.exp(-((np.angle(np.exp(1j * (theta + 2.9)))) / 0.12) ** 2) * smoothstep(72, 58, d) * smoothstep(38, 50, d) * keep  # a notch
    yc = (8, 12)
    yr = r_at(Xw, Zw, yc, 0.85, 35)
    young = 48 + (young_top - 48) * np.clip(1 - yr / young_r, 0, 1) ** 1.2 - gullies(Xw, Zw, yc, 12, 2.5, 6, young_r, seed=20)
    H = foot(H, np.where(yr < young_r, young, -1e9), 6)
    H = crater_in(H, yr, 9, 0.24 * young_r, 1, 1.4, k=3)
    H = flow(H, X, Z, [(yc[0], yc[1] + 0.6 * young_r), (20, 70), (5, 110), (25, 145)], 11, 3, seed=24)
    return H


def somma_low(X, Z):
    """The same broken rim, with the young cone smaller still: a mound in the moat, below the rim's top."""
    return somma(X, Z, young_r=20, young_top=72, seed=8)


def maar(X, Z):
    """The deep holes, now rough inside: outlines that wander, walls slumped into benches of different heights,
    fallen blocks and scree cones at the foot of the walls, a hummocky floor and a second crater nested in the
    first."""
    H = ground(X, 9, rise=10) + 26
    Xw, Zw = warp(X, Z, 240, big=10, small=4)
    for k, (c, r, ring, depth, stretch, ang) in enumerate([((-20, 0), 56, 16, 40, 0.82, 25),
                                                          ((80, 72), 26, 10, 22, 0.7, -40),
                                                          ((84, -70), 19, 7, 15, 0.85, 10)]):
        d = r_at(Xw, Zw, c, stretch, ang) * (1 + 0.08 * noise.fbm(X.shape, 14, 3, seed=90 + k))
        lean = 1 + 0.5 * np.clip((X - c[0]) / (2.5 * r), -0.6, 1)           # ejecta thrown farther east
        H = H + ring * np.exp(-((d - r) / (0.4 * r * lean)) ** 2) * (d > 0.6 * r)
        rough = 6 * noise.fbm(X.shape, 12, 3, seed=95 + k)                  # a floor with relief
        rim = float(np.median(H[np.abs(d - r) < 1.5]))
        steep = 1.8 + 1.2 * (0.5 + 0.5 * noise.fbm(X.shape, 30, 2, seed=97 + k))   # walls steeper in places
        bowl = rim - depth + rough + steep * np.maximum(0, d - 0.45 * r)
        H = np.where(d < r, np.minimum(H, bowl), H)
        steps = (4 + 3 * (0.5 + 0.5 * noise.fbm(X.shape, 25, 2, seed=99 + k))).round()
        bench = rim - depth + np.floor((H - (rim - depth)) / steps) * steps
        H = np.where((d < r) & (d > 0.5 * r), H + (bench - H) * 0.7 * (noise.fbm(X.shape, 18, 2, seed=101 + k) > -0.2), H)
        H = lumps(H, X, Z, int(r * 0.9), (c[0] - r, c[1] - r, c[0] + r, c[1] + r), (2, 0.14 * r), (2, 0.12 * r),
                  seed=110 + k, mask=(d < 0.95 * r) & (d > 0.35 * r))     # slumps and scree on the walls and floor
    inner = r_at(Xw, Zw, (-34, 10), 0.8, 60)
    H = crater_in(H, inner, 10, 13, 3, 1.6, k=3)                          # a younger crater nested in the floor
    return H


def along_noise(along, cell, seed, lo, hi):
    """A value wandering between lo and hi along a path: smooth 1-D noise indexed by distance along it."""
    n = int(along.max()) + 2
    f = noise.fbm((n,), cell, 3, seed=seed)
    f = (f - f.min()) / max(f.max() - f.min(), 1e-6)
    return lo + (hi - lo) * np.interp(along, np.arange(n), f)


def fissure(X, Z):
    """A rift with layers: three segments stepped sideways, each bending, each dying out at its ends into a narrow
    crack; a valley that swells and pinches, deep in one reach and shallow in the next; one wall a sheer drop and the
    other stepping down over a bench, the two trading places along it; shoulders lifted either side; ground high in
    one stretch and low in the next; cones strewn unevenly along the crack, clustered and merged in some reaches,
    absent in others."""
    H = ground(X, 10, rise=10) + 24
    H = H + 18 * noise.fbm(X.shape, 120, 3, seed=401)                     # plateaus and basins along the rift
    segments = [[(-150, -95), (-120, -78), (-85, -70), (-55, -42), (-30, -36)],
                [(-60, -10), (-25, 4), (10, 2), (40, 24), (70, 30)],
                [(45, 62), (80, 66), (105, 88), (150, 100)]]
    for s, pts in enumerate(segments):
        line = noise.spline(pts, 2.0)
        d, along, side = polyline(X, Z, line, side=True)
        total = float(along.max())
        t = np.clip(along / total, 0, 1)
        end = np.sin(np.pi * t) ** 0.6                                    # the rift dies out at both ends
        width = along_noise(along, 30, 420 + s, 6, 30) * end + 2
        depth = along_noise(along, 45, 430 + s, 5, 22) * end
        swap = along_noise(along, 60, 440 + s, -1, 1)                       # which side is sheer, changing along it
        sheer_side = np.where(swap > 0, side > 0, side < 0)
        wall = np.where(sheer_side, along_noise(along, 25, 450 + s, 1.2, 3.5), along_noise(along, 25, 460 + s, 6, 16))
        bench = np.where(sheer_side, 0, along_noise(along, 35, 470 + s, 0.3, 0.6))    # a bench part way down
        reach = 0.5 * width + wall
        jag = 2.2 * noise.fbm(X.shape, 6, 2, seed=480 + s)
        u = np.clip((d + jag - 0.5 * width) / np.maximum(wall, 0.5), 0, 1)
        u = u * u * (3 - 2 * u)
        u = np.where(bench > 0, np.where(u < 0.45, u * (1 - bench) / 0.45 * 0.45, (1 - bench) * 0.45 +
                                          (u - 0.45) / 0.55 * (1 - (1 - bench) * 0.45)), u)
        cut = H - depth * (1 - u)
        H = np.where(d + jag < reach, np.minimum(H, cut), H)
        H = H + 5 * end * np.exp(-((d - reach - 8) / 9) ** 2)               # the shoulders lifted beside it
        crack = d < 1.0 + 1.2 * (0.5 + 0.5 * noise.fbm(X.shape, 5, 1, seed=490 + s))
        H = np.where(crack & (end > 0.05), H - 4 - 6 * end, H)              # the open crack, deepest mid-segment
        rng = np.random.default_rng(500 + s)
        spots = []
        for centre in rng.uniform(0.15, 0.85, 2):                          # clusters, not a row
            spots += list(np.clip(rng.normal(centre, 0.05, rng.integers(2, 6)), 0.05, 0.95))
        rises = []
        for k, tt in enumerate(spots):
            idx = np.argmin(np.abs(along - tt * total) + 1000 * (d > 1.5))
            cx, cz = X.flat[idx] + rng.normal(0, 2.5), Z.flat[idx] + rng.normal(0, 2.5)
            r = rng.uniform(6, 16)
            rr = ellipse_distance(X, Z, (cx, cz), r, r * rng.uniform(0.55, 1.0), angle=rng.uniform(0, 180))
            rr = rr + 0.18 * noise.fbm(X.shape, 4, 2, seed=510 + 10 * s + k)
            rises.append(np.where(rr < 1, 1.0 * r * rng.uniform(0.7, 1.3) * np.clip(1 - rr, 0, 1) ** 0.85, 0))
            spots[k] = (cx, cz, r)
        if rises:
            H = H + L.join(rises, p=2.5)                                  # neighbours melt into ramparts
        for cx, cz, r in spots:
            if rng.random() < 0.75:
                H = crater_in(H, np.hypot(X - cx, Z - cz), 0.4 * r, 0.3 * r, 0.3, 1.3, k=1)
    for k, pts in enumerate([[(-15, 0), (-35, 40), (-25, 85), (-55, 140)], [(90, 75), (120, 30), (140, -40)],
                             [(-90, -70), (-110, -120)]]):
        H = flow(H, X, Z, noise.spline(pts, 2.0), 11 + 3 * k, 3, seed=550 + k)
    return H


def monolith(X, Z):
    """The tall table with no volcano on it: a monolith rising out of rolling jungle hills to well above any canopy.
    Its outline is lobed and bitten into by bays, its walls come down in sheer drops broken by ragged benches at
    uneven heights, a steep talus skirt runs out into the hills, and its top is its own small landscape: tilted,
    a crag at the high end, gullies cut back from the rim, a sunk hollow. Two smaller towers stand beside it."""
    H = ground(X, 11, rise=18)
    for k, (c, r, top, stretch, ang, benches) in enumerate([
            ((0, 0), 50, 200, 0.62, 25, [(0.62, 3), (0.45, 4), (0.24, 6)]),
            ((92, 70), 17, 140, 0.8, -20, [(0.5, 3)]),
            ((-95, -62), 12, 112, 0.9, 40, [(0.55, 3)])]):
        Xw, Zw = warp(X, Z, 260 + 10 * k, big=7 + 0.18 * r, small=3, big_cell=50, small_cell=12)
        d = r_at(Xw, Zw, c, stretch, ang)
        theta = np.arctan2(Zw - c[1], Xw - c[0])
        bays = 0.18 * r * np.maximum(0, np.sin(theta * 5 + 1.7 * noise.fbm(X.shape, 40, 2, seed=265 + k))) ** 6
        d = d + bays                                                      # bays bitten into the outline
        base = float(np.median(H[np.abs(d - r) < 2]))
        tilt = 0.22 * ((X - c[0]) * 0.8 + (Z - c[1]) * 0.6)
        relief = 7 * noise.fbm(X.shape, 22, 4, seed=280 + k) + tilt
        crag = 26 * np.clip(1 - r_at(Xw, Zw, (c[0] + 0.5 * r, c[1] + 0.25 * r), 0.7, 30) / (0.32 * r), 0, 1) ** 1.3
        hollow = 14 * np.clip(1 - r_at(Xw, Zw, (c[0] - 0.35 * r, c[1] - 0.15 * r), 0.8) / (0.25 * r), 0, 1) ** 1.5
        surface = top + relief + crag - hollow * (k == 0)
        cuts = 16 * noise.ridged(X.shape, 6, 2, seed=290 + k, sharpness=5) * smoothstep(r - 16, r, d)
        surface = surface - cuts                                          # gullies cut back from the rim
        jag = 2.5 * noise.fbm(X.shape, 7, 2, seed=295 + k)
        steps, edge = [], r
        for frac, out in benches:                                         # each bench a level the wall steps out to
            level = base + frac * (top - base) + 5 * noise.fbm(X.shape, 30, 2, seed=300 + k + len(steps))
            steps.append(L.Step(edge, edge + 1.2, level))
            edge = edge + out * (0.6 + 0.8 * (0.5 + 0.5 * noise.fbm(X.shape, 25, 2, seed=310 + k + len(steps))))
        steps.append(L.Step(edge, edge + 1.5, "ground"))
        H = L.profile(H, d, floor=top, floor_ground=surface, steps=steps, jag=jag, mode="lift")
        skirt = base + 0.22 * (top - base) * np.clip(1 - (d - edge) / (0.7 * r + 12), 0, 1) ** 1.8
        skirt = skirt + 3 * noise.fbm(X.shape, 8, 2, seed=320 + k)
        H = np.maximum(H, np.where(d > edge - 2, skirt, -1e9))
    return H


STUDIES = [stratovolcano, caldera_lake, horseshoe, somma, somma_low, maar, fissure, monolith]
V.CORNER.update({"horseshoe": "nw", "fissure": "sw", "somma": "ne", "somma_low": "ne", "monolith": "sw"})


if __name__ == "__main__":
    V.STUDIES = STUDIES
    V.main(sys.argv[1:])
