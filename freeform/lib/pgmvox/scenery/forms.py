"""Forms: scenery built in three dimensions, block by block, where a heightfield cannot say it.

    tower(w, cx, cz, 28, 90, r=5, rock=lambda y, b: beds(y + int(4 * b)), rng=r, tree=pine)
    skirt(w, land, floor, rock=beds, rng=r)        # karst faces under a floating floor's rim
    root_vines(w, land, floor, bottom, rng=r)      # vines hanging from the tips of the roots
    span = sweep(w, [(-58, 0), (58, 0)], flare(68, 60, 2), flare(3.5, 7, 3), flare(3, 10, 2), flare(3, 22, 2.2),
                 rough=0.28)                     # a land bridge over a canyon, as a mask over the world
    horn = spike(w, [(0, 10, 0), (0, 40, 0), (8, 60, 6)], (6, 0, 1.2), flutes=(9, 0.3))   # a spike, any axis

**A tower is a stack of rings, and its rings are what make it read as built.** Each course is a disc whose radius
tapers from `taper[0]` to `taper[1]` of r up the tower; every `ledge_every` blocks a course juts out `ledge`
further, a ring of ledges round the stack; and every disc's edge is pushed in or out by three-dimensional noise,
so the faces bulge between the ledges. Rock laid by height shows its beds as courses round it.

A heightfield spire has none of this: one surface, its sides a single slope, no ledge and nothing overhanging.
The karst towers were drawn this way and a spire in their place read as plain terrain, so the recipe is kept here.

**A swept solid has no teeth.** `sweep` carries a cross-section along a path and states every size in it as a
smooth function of how far along the span it is, so a side can only bulge across many blocks; roughness comes from
smooth noise over (along, round the section), never from a choice per column. A box whose edge rows are dropped
column by column at random steps in and out by one block along its whole length.

**A spike is a body round any 3-D curve, tapering to a point,** so it stands, leans, curls or hangs: a tower's
rings only stand, and a heightfield spire can neither lean nor overhang. It ends where it is narrower than half a
block, and keeps only what is joined to its base, so a fine tip never leaves a pole or a floating block.

**A skirt turns a floating floor's box sides into a cliff,** never touching the walked top: rock bulges out under
the rim in ledges no higher than two under the floor, is cut back under it where the noise is low, carries moss,
and grass grows on its ledges.
"""
import numpy as np
from scipy import ndimage

from pgmvox.geom import noise
from pgmvox.core.blocks import B
from pgmvox.geom.noise import spline
from pgmvox.geom.shapes import distance_in, edge_depth, polyline

SIDES = ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1))       # (dx, dz, the vine bit that hangs it on the block back)


def tower(w, cx, cz, y0, top, r, rock, rng, taper=(1.15, 0.70), ledge_every=9, ledge=0.8, bulge=1.4, cell=4,
          seed=0, through=(B.AIR, B.STAINED_GLASS, B.GLASS), crown=(B.GRASS, 0), crown_r=0.7, tree=None, vines=6):
    """A tower from y0 to top round (cx, cz), radius r at its foot. rock(y, b) gives the block at height y, where b
    is the bulge there (a tilt for the beds). It is written only into blocks in `through`, so it rises through
    mist without cutting islands. The crown is `crown` out to crown_r of r, with tree(w, x, y, z, rng) on it;
    `vines` is the number of vine strings a block of radius, hung down the faces. Returns the blocks laid."""
    R0 = int(r * max(taper) + ledge + bulge + 2)
    span = top - y0 + 1
    field = noise.fbm((2 * R0 + 1, span, 2 * R0 + 1), cell, 2, seed=seed)
    n = 0
    for y in range(y0, top + 1):
        t = (y - y0) / max(1, top - y0)
        rr = r * (taper[0] + (taper[1] - taper[0]) * t) + (ledge if (y % ledge_every) == 0 else 0)
        for dx in range(-R0, R0 + 1):
            for dz in range(-R0, R0 + 1):
                b = field[dx + R0, y - y0, dz + R0]
                if dx * dx + dz * dz <= (rr + bulge * b) ** 2:
                    x, z = cx + dx, cz + dz
                    if w.inside(x, y, z) and w.id(x, y, z) in through:
                        w.set(x, y, z, *rock(y, b))
                        n += 1
    cr = int(r * crown_r)
    for dx in range(-cr, cr + 1):
        for dz in range(-cr, cr + 1):
            if dx * dx + dz * dz <= cr * cr and w.inside(cx + dx, top, cz + dz) and w.id(cx + dx, top, cz + dz) != 0 \
                    and w.id(cx + dx, top + 1, cz + dz) == B.AIR:
                w.set(cx + dx, top, cz + dz, *crown)
    if tree:
        tree(w, cx, top, cz, rng)
    for _ in range(int(r * vines)):                               # strings of vine down the faces
        a = rng.uniform(0, 2 * np.pi)
        ya = int(rng.integers(min(y0 + 12, top - 3), top - 2)) if top - 2 > y0 + 12 else top - 3
        for y in range(ya, ya - int(rng.integers(3, 12)), -1):
            for rad in range(R0 + 1, 0, -1):
                x, z = cx + int(round(rad * np.cos(a))), cz + int(round(rad * np.sin(a)))
                if not w.inside(x, y, z) or w.id(x, y, z) != B.AIR:
                    continue
                hung = False
                for dx, dz, bit in ((1, 0, 8), (-1, 0, 2), (0, 1, 1), (0, -1, 4)):
                    if w.inside(x + dx, y, z + dz) and w.id(x + dx, y, z + dz) not in (B.AIR, B.VINE) + through:
                        w.set(x, y, z, B.VINE, bit)
                        hung = True
                        break
                if hung:
                    break
    return n


def skirt(w, land, floor, rock, rng, bulge=None, reach=(0.05, 0.3), moss=0.12, grass=0.5, undercut=-0.25,
          keep=None, seed=15):
    """Karst faces under the rim of floating floors (land: a world-grid mask; floor: each column's floor y).
    Outside the rim, where the bulge noise is high, rock juts out a block or two as ledges, their tops no higher
    than floor - 2 (so the walked edge and the plan's gaps are untouched), with `moss` of it mossy and grass on
    `grass` of the ledges; on the rim, where the noise is under `undercut`, the face is cut back from floor - 5
    to floor - 3. `keep` is a mask of rim cells never undercut (a wool room's wall, a pillar)."""
    near = distance_in(~land, "euclid")
    Hn = ndimage.maximum_filter(np.where(land, floor, -1), size=5)
    b = noise.fbm(land.shape, 5, 2, seed=seed) if bulge is None else bulge
    X, Z = w.grid()
    n = 0
    for i, k in np.argwhere(~land & (near <= 2.2) & (Hn >= 0)):
        v = b[i, k]
        if near[i, k] > (v > reach[0]) + (v > reach[1]):
            continue
        x, z, h = int(X[i, k]), int(Z[i, k]), int(Hn[i, k])
        top = h - 2 - int(near[i, k]) - (1 if v < 0.2 else 0)
        bot = h - 6 - int(4 * max(0, v)) - int(rng.integers(0, 3))
        for y in range(bot, top + 1):
            w.set(x, y, z, *((B.MOSSY, 0) if rng.random() < moss else rock(y)))
            n += 1
        if rng.random() < grass and w.id(x, top + 1, z) == B.AIR:
            w.set(x, top + 1, z, B.TALLGRASS, 2 if rng.random() < 0.5 else 1)
    rim = land & (edge_depth(land) == 0) & (b < undercut)
    if keep is not None:
        rim &= ~keep
    for i, k in np.argwhere(rim):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        for y in range(h - 5, h - 2):
            w.set(x, y, z, B.AIR)
    return n


def root_vines(w, land, floor, bottom, rng, chance=0.05, under=9, length=(3, 10), keep=None):
    """Vines hanging from the lower part of floating roots: on each side of a land column, with `chance`, a string
    starting a few blocks above the root's tip (bottom: each column's lowest y) and never higher than `under`
    below the floor, hung on the root wherever it has a face. They trail below the islands, where nobody reaches
    them from a floor."""
    X, Z = w.grid()
    cells = land if keep is None else land & ~keep
    n = 0
    for i, k in np.argwhere(cells):
        x, z, h, lo = int(X[i, k]), int(Z[i, k]), int(floor[i, k]), int(bottom[i, k])
        for dx, dz, bit in SIDES:
            if rng.random() > chance:
                continue
            top = min(h - under, lo + int(rng.integers(3, 12)))
            for y in range(top, max(lo, top - int(rng.integers(*length))), -1):
                if w.id(x, y, z) not in (B.AIR, B.VINE) and w.inside(x + dx, y, z + dz) \
                        and w.id(x + dx, y, z + dz) == B.AIR:
                    w.set(x + dx, y, z + dz, B.VINE, bit)
                    n += 1
    return n


def masonry_tower(w, x0, z0, x1, z1, y0, height, wall=((B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2)),
                  corner=(B.STONEBRICK, 3), floor=(B.PLANKS, 5), slit=(B.IRON_BARS, 0), door=B.DARK_OAK_DOOR,
                  door_side="s", crown=(B.STONEBRICK, 0), crenel=(B.COBBLE_WALL, 0), light=(B.GLOWSTONE, 0), rng=None,
                  ladder_on="n"):
    """A hollow masonry tower over (x0, z0)-(x1, z1) on the floor at y0: walls from y0 + 1 to y0 + height on a
    three-course footing, a floor every five courses, a ladder up the inside of the `ladder_on` wall through a hatch
    in each floor, iron-barred slits on every face, a door at the foot on `door_side`, a crenellated crown with a
    light in it. Returns the ladder's cell."""
    from pgmvox.core.orient import door as door_data, ladder as ladder_data
    rng = rng or np.random.default_rng(1)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            at_corner = x in (x0, x1) and z in (z0, z1)
            for y in range(y0 - 3, y0 + 1):
                w.set(x, y, z, B.STONEBRICK, 0)
            for y in range(y0 + 1, y0 + height + 1):
                if at_corner:
                    w.set(x, y, z, *corner)
                elif edge:
                    t = y - y0
                    if t % 5 in (3, 4) and ((x - x0 + z - z0) % 3 == 1) and t > 2:
                        w.set(x, y, z, *slit)
                    else:
                        w.set(x, y, z, *wall[int(rng.integers(len(wall)))])
                else:
                    w.set(x, y, z, B.AIR)
            if not edge:
                w.set(x, y0, z, *floor)
                for t in range(5, height, 5):
                    w.set(x, y0 + t, z, *floor)
                w.set(x, y0 + height, z, *floor)
    lx, lz = (x0 + x1) // 2, (z0 + z1) // 2
    px, pz = {"n": (lx, z0 + 1), "s": (lx, z1 - 1), "w": (x0 + 1, lz), "e": (x1 - 1, lz)}[ladder_on]
    for y in range(y0 + 1, y0 + height + 1):
        w.set(px, y, pz, B.LADDER, ladder_data(ladder_on))
    for t in range(5, height + 1, 5):
        w.set(px, y0 + t, pz, B.LADDER, ladder_data(ladder_on))
    dx_, dz_ = {"n": (lx, z0), "s": (lx, z1), "w": (x0, lz), "e": (x1, lz)}[door_side]
    w.set(dx_, y0 + 1, dz_, door, door_data(door_side))
    w.set(dx_, y0 + 2, dz_, door, door_data(door_side, upper=True))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                w.set(x, y0 + height + 1, z, *crown)
                if (x + z) % 2 == 0:
                    w.set(x, y0 + height + 2, z, *crenel)
    w.set(lx, y0 + height + 1, lz, B.NETHER_FENCE, 0)
    w.set(lx, y0 + height + 2, lz, *light)
    return (px, pz)


def _along_span(curve, t):
    if callable(curve):
        return curve(t)
    crown, end, power = curve
    return int(round(crown + (end - crown) * t ** power))


def flare(crown, end, power):
    """A size along a span: `crown` in the middle, growing to `end` at both ends as |2t - 1| ** power, t from 0 to
    1. A higher power keeps the middle at the crown's size longer and grows it nearer the ends."""
    return lambda t: crown + (end - crown) * np.abs(2 * np.asarray(t, float) - 1) ** power


def sweep(w, path, centre_y, half_width, above, below, power=3.0, rough=0.0, cell=14, seed=0):
    """A solid swept along `path` (x, z points), as a boolean mask over the world (w.ids' shape). At each point a
    cross-section: `half_width` across, rising `above` over `centre_y` and hanging `below` under it, a
    superellipse of `power` (2 an ellipse, higher squarer: a flatter deck and straighter sides). Each size is a
    number or a function of t, 0 to 1 along the path (flare). `rough` pushes the surface in and out by smooth
    noise, features `cell` blocks along and a twelfth of the way round; zero keeps it exact. The path's ends may
    run into rock: write the mask where the world is air and the bridge grows out of the walls."""
    size = lambda f, t: np.asarray(f(t) if callable(f) else np.full(np.shape(t), float(f)), float)   # noqa: E731
    ts = np.linspace(0, 1, 101)
    reach = float(np.max(size(half_width, ts))) * (1 + rough) + 2
    xs, zs = [p[0] for p in path], [p[1] for p in path]
    i0 = max(0, int(np.floor(min(xs) - reach)) - w.x0)
    i1 = min(w.sx, int(np.ceil(max(xs) + reach)) - w.x0 + 1)
    k0 = max(0, int(np.floor(min(zs) - reach)) - w.z0)
    k1 = min(w.sz, int(np.ceil(max(zs) + reach)) - w.z0 + 1)
    lo = float(np.min(size(centre_y, ts) - size(below, ts) * (1 + rough))) - 2
    hi = float(np.max(size(centre_y, ts) + size(above, ts) * (1 + rough))) + 2
    y0, y1 = max(0, int(np.floor(lo))), min(w.sy, int(np.ceil(hi)) + 1)
    out = np.zeros(w.ids.shape, bool)
    if i0 >= i1 or k0 >= k1 or y0 >= y1:
        return out
    X, Z = np.meshgrid(np.arange(w.x0 + i0, w.x0 + i1, dtype=float), np.arange(w.z0 + k0, w.z0 + k1, dtype=float),
                       indexing="ij")
    d, along, side = polyline(X, Z, path, side=True)
    total = max(float(along.max()), 1e-6)
    t = np.clip(along / total, 0, 1)
    cy, hw, up, dn = (size(f, t)[:, None, :] for f in (centre_y, half_width, above, below))
    ys = np.arange(y0, y1, dtype=float)[None, :, None]                   # integer x, y, z are block centres, as in shapes
    u = np.where(side > 0, d, -d)[:, None, :] / np.maximum(hw, 1e-6)
    v = ys - cy
    v = np.where(v > 0, v / np.maximum(up, 1e-6), v / np.maximum(dn, 1e-6))
    shape = np.abs(u) ** power + np.abs(v) ** power
    if rough:
        n_along, n_round = max(4, int(total / cell) + 4), 12
        rng = np.random.default_rng(seed)
        field = ndimage.zoom(rng.uniform(-1, 1, (n_along, n_round)), (4, 4), order=3, mode="grid-wrap")
        field += 0.5 * ndimage.zoom(rng.uniform(-1, 1, (n_along * 2, n_round * 2)), (2, 2), order=3, mode="grid-wrap")
        ang = (np.arctan2(v, u) / (2 * np.pi)) % 1
        coords = [np.broadcast_to(t[:, None, :] * (field.shape[0] - 1), shape.shape), ang * field.shape[1]]
        shape = shape * (1 - rough * ndimage.map_coordinates(field, coords, order=1, mode="grid-wrap"))
    out[i0:i1, y0:y1, k0:k1] = shape < 1
    return out


def spike(w, axis, radius, sides=0, flutes=(0, 0.0), twist=0.0, ledges=(0, 0.0), rough=0.0, cell=8, seed=0):
    """A spike round `axis` (x, y, z points from base to tip, splined through when there are more than two), as a
    mask over the world. `radius` is a function of t, 0 at the base and 1 at the tip, or (base, tip, power):
    tip + (base - tip) * (1 - t) ** power, so a power under 1 swells and over 1 needles. `sides` 0 is round, 3 or
    more a polygon whose corners reach the radius; `flutes` (count, depth) grooves it along its length; `twist` turns the
    section that many degrees from base to tip; `ledges` (every, out) rings it every so many blocks along it;
    `rough` moves its surface by smooth noise, features `cell` blocks along it and a twelfth of the way round. It
    ends where it is under half a block across, and only what is joined to its base is kept."""
    if not callable(radius):
        base, tip, p = radius
        radius = lambda t, b=base, e=tip, q=p: e + (b - e) * (1 - np.asarray(t, float)) ** q   # noqa: E731
    pts = np.array(spline([tuple(a) for a in axis], 1.0) if len(axis) > 2 else axis, float)
    seg = pts[1:] - pts[:-1]
    seg_len = np.linalg.norm(seg, axis=1)
    keep = seg_len > 1e-6
    pts = np.vstack([pts[:1], pts[1:][keep]])
    seg, seg_len = seg[keep], seg_len[keep]
    cum = np.concatenate([[0], np.cumsum(seg_len)])
    total = cum[-1]
    tan = seg / seg_len[:, None]
    ref = np.array([1.0, 0, 0]) if abs(tan[0, 0]) < 0.9 else np.array([0, 0, 1.0])
    normals = np.zeros_like(tan)
    n = ref - tan[0] * (ref @ tan[0])
    for i, tv in enumerate(tan):                                          # a frame carried along without spinning
        n = n - tv * (n @ tv)
        n /= np.linalg.norm(n)
        normals[i] = n
    binormals = np.cross(tan, normals)
    reach = float(np.max(radius(np.linspace(0, 1, 51)))) * (1 + rough) + ledges[1] + 2
    lo, hi = np.floor(pts.min(0) - reach).astype(int), np.ceil(pts.max(0) + reach).astype(int)
    i0, i1 = max(lo[0] - w.x0, 0), min(hi[0] - w.x0 + 1, w.sx)
    j0, j1 = max(lo[1], 0), min(hi[1] + 1, w.sy)
    k0, k1 = max(lo[2] - w.z0, 0), min(hi[2] - w.z0 + 1, w.sz)
    out = np.zeros(w.ids.shape, bool)
    if i0 >= i1 or j0 >= j1 or k0 >= k1:
        return out
    gx, gy, gz = np.meshgrid(np.arange(w.x0 + i0, w.x0 + i1), np.arange(j0, j1), np.arange(w.z0 + k0, w.z0 + k1),
                             indexing="ij")
    P = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], -1).astype(float)
    best, s_at, which = np.full(len(P), np.inf), np.zeros(len(P)), np.zeros(len(P), int)
    for i in range(len(seg)):
        tt = np.clip(((P - pts[i]) @ seg[i]) / seg_len[i] ** 2, 0, 1)
        d2 = ((P - pts[i] - tt[:, None] * seg[i]) ** 2).sum(1)
        nearer = d2 < best
        best = np.where(nearer, d2, best)
        s_at = np.where(nearer, cum[i] + tt * seg_len[i], s_at)
        which = np.where(nearer, i, which)
    t = s_at / total
    o = P - (pts[which] + tan[which] * (s_at - cum[which])[:, None])
    theta = np.arctan2((o * binormals[which]).sum(1), (o * normals[which]).sum(1)) + np.radians(twist) * t
    r = radius(t)
    if sides >= 3:
        k = 2 * np.pi / sides
        r = r * np.cos(np.pi / sides) / np.cos((theta % k) - k / 2)
    if flutes[0]:
        r = r * (1 - flutes[1] * (0.5 + 0.5 * np.cos(flutes[0] * theta)))
    if ledges[0]:
        r = r + ledges[1] * ((s_at % ledges[0]) < 1.0)
    if rough:
        rng = np.random.default_rng(seed)
        na, nr = max(4, int(total / cell) + 4), 12
        field = ndimage.zoom(rng.uniform(-1, 1, (na, nr)), (4, 4), order=3, mode="grid-wrap")
        field += 0.5 * ndimage.zoom(rng.uniform(-1, 1, (na * 2, nr * 2)), (2, 2), order=3, mode="grid-wrap")
        r = r * (1 + rough * ndimage.map_coordinates(
            field, [t * (field.shape[0] - 1), ((theta / (2 * np.pi)) % 1) * field.shape[1]], order=1, mode="grid-wrap"))
    inside = ((np.sqrt(best) < r) & (r >= 0.5)).reshape(gx.shape)
    parts, _ = ndimage.label(inside)
    based = np.unique(parts[inside & (t.reshape(gx.shape) < 0.05)])
    out[i0:i1, j0:j1, k0:k1] = inside & np.isin(parts, based[based > 0])
    return out


def arch(w, cells, t, deck, thick, rock, into=None, clear=0, ground=None):
    """A natural arch over `cells` (x, z): `t[(x, z)]` is where a cell lies along the span, 0 at the crown and 1
    at the ends. Its deck stands at deck(t) and rock hangs thick(t) blocks under it; each is (crown, end, power),
    crown + (end - crown) * t ** power rounded, or a function of t. rock(x, y, z, k) is the block k under the deck
    (0 is the deck itself). The deck is always laid; the rock under it fills only blocks in `into` (any, where
    None), never at or below ground(x, z) where that is given, so the ground under the arch stays the ground.
    `clear` blocks over the deck are emptied. Returns the deck's height at each cell."""
    tops = {}
    for x, z in cells:
        s = t[(x, z)]
        y = _along_span(deck, s)
        floor = -1 if ground is None else ground(x, z)
        w.set(x, y, z, *rock(x, y, z, 0))
        for k in range(1, _along_span(thick, s) + 1):
            if y - k <= floor:
                break
            if into is None or w.id(x, y - k, z) in into:
                w.set(x, y - k, z, *rock(x, y - k, z, k))
        for yy in range(y + 1, y + 1 + clear):
            if w.id(x, yy, z) != B.AIR:
                w.set(x, yy, z, B.AIR)
        tops[(x, z)] = y
    return tops



SOFT = (B.AIR, B.WATER, B.WATER_FLOW, B.TALLGRASS, B.FLOWER, B.DEADBUSH, B.DIRT, B.GRASS, B.STONE, B.SAND, B.GRAVEL,
        B.CLAY, B.STAINED_CLAY, B.HARDENED_CLAY)


def box_cells(at, size, yaw=0.0, tilt=0.0):
    """The blocks of a box turned `yaw` degrees about the vertical and tilted `tilt` degrees about its own long
    axis, centred at `at` (x, y, z): every block whose centre lies inside it, with its place in the box's own frame,
    (x, y, z, u, ly, lz), u along its width, ly up its height, lz along its depth, each from the box's middle."""
    import math
    cx, cy, cz = at
    w_, h_, d_ = size
    a, t = math.radians(yaw), math.radians(tilt)
    cyw, syw, ct, st = math.cos(a), math.sin(a), math.cos(t), math.sin(t)
    R = int(math.ceil(math.sqrt(w_ * w_ + h_ * h_ + d_ * d_) / 2)) + 1
    g = np.arange(-R, R + 1)
    DX, DY, DZ = np.meshgrid(g, g, g, indexing="ij")
    fx, fy, fz = math.floor(cx), math.floor(cy), math.floor(cz)
    px, py, pz = fx + DX + 0.5 - cx, fy + DY + 0.5 - cy, fz + DZ + 0.5 - cz
    u = px * cyw + pz * syw
    v = -px * syw + pz * cyw
    ly = py * ct + v * st
    lz = -py * st + v * ct
    inside = (np.abs(u) <= w_ / 2) & (np.abs(ly) <= h_ / 2) & (np.abs(lz) <= d_ / 2)
    return [(int(fx + DX[i]), int(fy + DY[i]), int(fz + DZ[i]), float(u[i]), float(ly[i]), float(lz[i]))
            for i in zip(*np.nonzero(inside))]


def placed_box(w, x, z, size, H, yaw=0.0, tilt=0.0, sink=0.3, on="lowest", paint=None, hole=None, over=SOFT):
    """A monolith, a slab or a ring set into the ground the way Stratum set its fragments: a box of `size`
    (width, height, depth) turned `yaw` and tilted `tilt`, its bottom `sink` of its upright height under the ground
    `on` its footprint (`lowest`, `centre` or a y). `paint(u, ly, lz, size)` gives each block from its place in the
    box's frame (a block for all, by default stone), `hole` (wall thickness) hollows it into a frame through its
    depth, and only blocks in `over` are written, so trees and earlier boxes stand. Returns the blocks laid."""
    import math
    w_, h_, d_ = size
    up = abs(h_ * math.cos(math.radians(tilt))) + abs(d_ * math.sin(math.radians(tilt)))
    x0, z0 = int(w.x0), int(w.z0)
    i, k = int(x) - x0, int(z) - z0
    if on == "lowest":
        r = int(math.ceil(max(w_, d_) / 2))
        foot = H[max(i - r, 0):i + r + 1, max(k - r, 0):k + r + 1]
        base = float(foot[foot >= 0].min()) if (foot >= 0).any() else float(H[i, k])
    elif on == "centre":
        base = float(H[i, k])
    else:
        base = float(on)
    cy = base + 1 + up / 2 - sink * up
    paint = paint or (lambda u, ly, lz, s: (B.STONE, 0))
    n = 0
    for bx, by, bz, u, ly, lz in box_cells((x + 0.5, cy, z + 0.5), size, yaw, tilt):
        if hole is not None and abs(u) < w_ / 2 - hole and abs(ly) < h_ / 2 - hole:
            continue
        if not (1 <= by < w.ids.shape[1]) or w.id(bx, by, bz) not in over:
            continue
        w.set(bx, by, bz, *paint(u, ly, lz, size))
        n += 1
    return n
