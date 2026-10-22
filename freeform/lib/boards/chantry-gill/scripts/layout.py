"""Chantry Gill's layout: the land in the void, one team's half drawn, the other its half turn.

Blue holds the south (z > 0), red is blue's image under (x, z) -> (-1 - x, -1 - z). Each team has a main island,
the fell with the town, and a side island, the Scar, east of it; between them runs the Gill, a gorge, not void.
Between the two teams lies the void, crossed by a build zone the board's whole width.
"""
import math

# the main island: the fell, the town on its east rim over the gill, the spawn under the knott at its back
MAIN = [(-78, 40), (-70, 22), (-52, 13), (-30, 16), (-12, 11), (6, 14), (20, 20), (27, 30), (26, 46), (29, 62),
        (27, 78), (30, 92), (22, 106), (4, 116), (-20, 118), (-44, 112), (-62, 100), (-76, 80), (-82, 60)]
# the side island: the Scar, its leaning brow facing west over the gill, the tarn at its front
SIDE = [(40, 24), (52, 15), (68, 17), (80, 30), (84, 50), (79, 70), (72, 88), (58, 100), (44, 98), (39, 84),
        (40, 66), (38, 50), (41, 36)]
# the gill: the gorge between them, its floor 9 under the main island's rim
GILL = [MAIN[7], MAIN[8], MAIN[9], MAIN[10], MAIN[11], (36, 98), (44, 98), SIDE[9], SIDE[10], SIDE[11], SIDE[12],
        SIDE[0], (31, 22)]
# scenery: the edge down the west and the knott across the back, high ground fenced off from play by its own
# faces; it frames the board and nobody fights on it
# the highlands: one band of high ground along the main island's west and back coast, its inner edge wandering
# (DEPTH, blocks in from the coast, varied by HIGH_NOISE), cut into pieces round seeds the way a puzzle is: each
# column belongs to the nearest seed, the distances bent by noise so neighbours interlock. A seed is (x, z, rise,
# name); a rise over 12 is scenery fenced off by its faces, the rest foothills that are played on.
HIGH_CENTRE = (-14, 66)
HIGH_SECTOR = (70, 205)                      # degrees, from east toward south, round HIGH_CENTRE
DEPTH = (18, 26)                             # base and swing of the band's depth from the coast
SEEDS = [
    (-80, 46, 16, "west tor"), (-78, 66, 24, "edge"), (-58, 60, 10, "edge bench"),
    (-66, 86, 28, "south pike"), (-48, 80, 8, "pike knoll"), (-44, 104, 20, "knott"), (-30, 94, 6, "knott foot"),
    (-14, 112, 26, "high knott"), (-12, 98, 5, "spawn knoll"),
]
SCENERY_RISE = 12
BUILD_Z = (-14, 13)                       # the build zone over the void between the teams, the board's whole width
X_RANGE = (-90, 89)

PLACES = {                                 # name: (x, z, what it is)
    "spawn": (4, 94, "the spawn, at the foot of the knott, the hall behind it"),
    "town monument": (-14, 58, "the town monument: three obsidian over the market square in the middle of the town"),
    "scar monument": (58, 84, "the Scar monument: three obsidian on the plateau behind the brow"),
    "square": (-4, 60, "the market square, stalls along its west edge"),
    "chapel": (-8, 74, "the chapel on the square's south side, the crypt under it, the ladder up into its nave"),
    "town": (-30, 66, "the town: houses on the main street and a lane, the wall broken on its west"),
    "front gate": (-6, 26, "the north gate, where the street leaves the town for the front"),
    "fields": (-44, 46, "the byre, its field and the flower meadow, between the edge and the town"),
    "brig": (33, 36, "the brig: a stone arch over the gill, from the front of the town to the tarn"),
    "tarn": (60, 30, "the tarn on the Scar's front, its beach to the north, the beck running in from the gill"),
    "brow": (46, 70, "the Scar's brow: its face leaning out over the gill, over the brig and the back bridge"),
    "shelter": (40, 66, "the shelter worn into the brow's foot on the gill floor; the adit runs on from it"),
    "plateau": (68, 66, "the plateau behind the brow, reached up a slope at its north end"),
    "back brig": (34, 91, "a timber bridge over the gill behind the brow: the spawn's way to the Scar"),
    "chimney": (44, 74, "a chimney in the rock from the shelter up to the plateau, a ladder in it"),
}
SPAWN = PLACES["spawn"][:2]
MONUMENTS = [PLACES["town monument"][:2], PLACES["scar monument"][:2]]
MONUMENT = MONUMENTS[0]

# the ways an attacker landing on this half comes at each monument
ROUTES = {
    "town: through": [(-6, 14), (-6, 26), (-10, 44), (-14, 58)],
    "town: around": [(-46, 16), (-52, 32), (-40, 50), (-14, 58)],
    "town: brig": [(46, 18), (44, 34), (33, 36), (20, 42), (2, 50), (-14, 58)],
    "town: below": [(46, 18), (33, 30), (34, 50), (38, 66), "adit", (-4, 72), "ladder", (-6, 70), (-14, 58)],
    "scar: front": [(62, 16), (74, 40), (72, 62), (64, 76), (58, 84)],
    "scar: chimney": [(46, 18), (33, 30), (34, 50), (40, 66), "chimney", (48, 72), (58, 84)],
}
DEFENCES = [[(4, 94), (0, 80), (-8, 66), (-14, 58)],
            [(4, 94), (30, 92), (44, 92), (58, 84)]]
DEFENCE = DEFENCES[0]
ADIT = [(39, 66, 33), (28, 68, 29), (10, 72, 29), (-4, 72, 33)]      # (x, z, floor y): shelter to crypt
CRYPT = (-14, 68, -2, 78)


def turn(p):
    return (-1 - p[0], -1 - p[1])


def length(pts):
    pts = [p for p in pts if not isinstance(p, str)]
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def grid(x_range=X_RANGE, z_range=(-130, 129)):
    import numpy as np
    xs, zs = np.arange(x_range[0], x_range[1] + 1), np.arange(z_range[0], z_range[1] + 1)
    return np.meshgrid(xs, zs, indexing="ij")


def mask(poly, X, Z):
    import numpy as np
    from matplotlib.path import Path
    return Path(poly).contains_points(np.c_[X.ravel() + 0.5, Z.ravel() + 0.5]).reshape(X.shape)


def highlands(X, Z):
    """The highlands as a partition of the grid: each column's piece, an index into SEEDS, or -1 off the band. The
    band runs DEPTH in from the main island's coast within HIGH_SECTOR; each column takes the nearest seed by a
    distance bent with noise, then a majority filter and a merge of strays leave each piece one region."""
    import numpy as np
    from scipy import ndimage
    from pgmvox.geom import noise as N
    inside = mask(MAIN, X, Z)
    coast = ndimage.distance_transform_edt(inside)
    ang = (np.degrees(np.arctan2(Z - HIGH_CENTRE[1], X - HIGH_CENTRE[0])) + 360) % 360
    a0, a1 = HIGH_SECTOR
    sector = np.clip(np.minimum(ang - a0, a1 - ang) / 25, 0, 1)
    depth = (DEPTH[0] + DEPTH[1] * (0.5 + 0.5 * N.fbm(X.shape, 18, 2, seed=41))) * sector
    band = inside & (coast < depth)
    wx, wz = 9 * N.fbm(X.shape, 16, 2, seed=42), 9 * N.fbm(X.shape, 16, 2, seed=43)
    d = np.stack([np.hypot(X + wx - sx, Z + wz - sz) for sx, sz, _, _ in SEEDS])
    piece = np.where(band, d.argmin(axis=0), -1)
    for _ in range(3):                                   # a majority filter: no splinters, no enclaves
        votes = np.stack([ndimage.uniform_filter((piece == k).astype(float), 5) for k in range(len(SEEDS))])
        piece = np.where(band, votes.argmax(axis=0), -1)
    for k in range(len(SEEDS)):                          # each piece one region: strays go to their neighbours
        lab, n = ndimage.label(piece == k)
        if n > 1:
            keep = np.argmax(ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))) + 1
            stray = (lab > 0) & (lab != keep)
            near = ndimage.grey_dilation(np.where(stray, -1, piece), size=5)
            piece[stray] = near[stray]
    return piece
