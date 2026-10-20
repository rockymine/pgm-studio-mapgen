"""Seamworks' assets as forms: each function builds one kind of thing into a world and asks a look what every block of it
is, by the role the block plays (a panel's plate, rib or cap; a building's wall, band or sill). The map and the asset
sheet both build through these, so what is judged on the sheet is what the map gets.

A site is described to a function by callables rather than arrays: `ground(x, z)` the crust's walking level, `feet(x,
z)` a cut floor's walking level, `is_floor(x, z)` whether a column is cut floor."""
import math

import numpy as np

from pgmvox import B
from pgmvox.core.orient import ladder as ladder_data, stair as stair_data

DIRS = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}
STOREY = 5                               # a storey's floor slab and four of air


def pip(pt, poly):
    x, y = pt
    inside = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def poly_cells(poly):
    """The columns whose centres lie inside a polygon."""
    xs = [p[0] for p in poly]
    zs = [p[1] for p in poly]
    return {(x, z) for x in range(math.floor(min(xs)), math.ceil(max(xs)) + 1)
            for z in range(math.floor(min(zs)), math.ceil(max(zs)) + 1) if pip((x + .5, z + .5), poly)}


def seg_dist(px, pz, a, b):
    vx, vz = b[0] - a[0], b[1] - a[1]
    t = min(max(((px - a[0]) * vx + (pz - a[1]) * vz) / (vx * vx + vz * vz), 0), 1)
    return math.hypot(px - a[0] - t * vx, pz - a[1] - t * vz)


# ---- a works building ---------------------------------------------------------------------------------------------------
def building(w, poly, base, sections, look, skylights=False):
    """A building on a floor at `base` (the walking level of its lowest storey): `sections` as (cells, storeys,
    (ladder cell, wall side)), each section its own height, a ladder through its slabs. The look is asked for
    "wall", "window band" (the two courses the windows sit in), "corner", "band" (the outside of each slab), "base"
    (the course under the lowest storey), "cornice" and
    "parapet" (the roof's edge), "roof", "skylight", "floor", "light", "window" and "sill"."""
    cells = poly_cells(poly)
    storeys = {}
    for sec_cells, n, _ in sections:
        for c in sec_cells & cells:
            storeys[c] = n
    for (x, z) in cells:
        n = storeys.get((x, z), 0)
        if not n:
            continue
        roof = base + n * STOREY
        out = [storeys.get((x + a, z + b), 0) for a, b in DIRS.values()]
        corner = (out[0] < n or out[1] < n) and (out[2] < n or out[3] < n)
        for y in range(base - 1, roof + 1):
            w.set(x, y, z, *look.building(x, y, z, "corner" if corner else "wall"))
        w.set(x, base - 1, z, *look.building(x, base - 1, z, "base" if min(out) < n else "floor"))
        for level in range(n):
            floor_y = base + level * STOREY
            outside = min(out) == 0 or any(r <= level for r in out)
            if outside:
                if level > 0 and not corner:
                    w.set(x, floor_y - 1, z, *look.building(x, floor_y - 1, z, "band"))
                    for y in (floor_y + 1, floor_y + 2):
                        w.set(x, y, z, *look.building(x, y, z, "window band"))
                if not corner and (x + z) % 4 == 0 and level > 0:
                    for a, b in DIRS.values():
                        if storeys.get((x + a, z + b), 0) <= level and w.id(x + a, floor_y + 1, z + b) == B.AIR \
                                and w.id(x + a, floor_y + 2, z + b) == B.AIR:
                            w.set(x, floor_y, z, *look.building(x, floor_y, z, "sill"))
                            w.column(x, z, floor_y + 1, floor_y + 2, *look.building(x, floor_y + 1, z, "window"))
                continue
            w.column(x, z, floor_y, floor_y + STOREY - 2, B.AIR)
            if level > 0:
                w.set(x, floor_y - 1, z, *look.building(x, floor_y - 1, z, "floor"))
            if (x * 3 + z) % 7 == 0:
                w.set(x, floor_y + STOREY - 1, z, *look.building(x, floor_y + STOREY - 1, z, "light"))
        edge = min(out) == 0 or any(r < n for r in out)
        if edge:
            w.set(x, roof, z, *look.building(x, roof, z, "cornice"))
            w.set(x, roof + 1, z, *look.building(x, roof + 1, z, "parapet"))
        else:
            role = "skylight" if skylights and z % 5 == 0 else "roof"
            w.set(x, roof, z, *look.building(x, roof, z, role))
    for _, n, ((lx, lz), side) in sections:
        a, b = DIRS[side]
        for y in range(base, base + (n - 1) * STOREY + 1):
            w.set(lx, y, lz, B.LADDER, ladder_data((a, b)))
        w.column(lx + a, lz + b, base, base + (n - 1) * STOREY + 1, *look.building(lx + a, base, lz + b, "wall"))
    return cells


def door(w, line, bottom, look, height=3):
    """A doorway three high through a wall, framed: a jamb past each end and a lintel over the opening."""
    for x, z in line:
        w.column(x, z, bottom, bottom + height - 1, B.AIR)
    (x0, z0), (x1, z1) = line[0], line[-1]
    dx, dz = (1, 0) if z0 == z1 else (0, 1)
    for jx, jz in ((x0 - dx, z0 - dz), (x1 + dx, z1 + dz)):
        for y in range(bottom, bottom + height + 1):
            w.set(jx, y, jz, *look.door(jx, y, jz, "jamb"))
    for x, z in line:
        w.set(x, bottom + height, z, *look.door(x, bottom + height, z, "lintel"))


def chimney(w, box, height, look, drift=(1, 0), plume=11):
    """A chimney over a roof: a stack ringed every fourth course, a crown of wall round its top, and a plume of glass
    smoke drifting downwind, thinning as it rises. The look is asked for "stack", "ring", "crown" and "smoke"."""
    x0, z0, x1, z1 = box
    top = max(w.top(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(w.top(x, z) + 1, top + height + 1):
                role = "ring" if (y - top) % 4 == 0 else "stack"
                w.set(x, y, z, *look.chimney(x, y, z, role))
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            if x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1):
                w.set(x, top + height, z, *look.chimney(x, top + height, z, "crown"))
    cx, cz = (x0 + x1) / 2 + .5, (z0 + z1) / 2 + .5
    rim = top + height + 1
    for h in range(plume):
        r = 0.9 + h * 0.18
        px = cx + drift[0] * h * 0.7 + math.sin(h * 1.3) * 0.5
        pz = cz + drift[1] * h * 0.7 + math.cos(h * 1.1) * 0.5
        for x in range(math.floor(px - r), math.ceil(px + r) + 1):
            for z in range(math.floor(pz - r), math.ceil(pz + r) + 1):
                d = math.hypot(x + .5 - px, z + .5 - pz) / r
                keep = 0.95 - h / plume * 0.55
                if d <= 1 and ((x * 31 + z * 17 + h * 7) % 100) / 100 < keep * (1.1 - d * 0.5):
                    w.set(x, rim + h, z, *look.chimney(x, rim + h, z, "smoke"))


# ---- the panels -----------------------------------------------------------------------------------------------------
def panels(w, quads, base_of, rise_of, is_floor, keep_out, ground, look):
    """Panels as quads standing on a floor and leaning back into the earth: each (a, b, n, (lean at a, lean at b),
    shade). `base_of(a, b, n)` is the floor they stand on and `rise_of(a, b, n, base)` how high they climb. Each is
    two blocks thick and the wedge between its foot and its face is cleared. Where two panels of different walls
    reach the same blocks, the shorter is left out, so the rock shows there instead of two panels passing through each
    other; between neighbours on one wall a shared block goes to the nearer foot. Nothing is laid where
    `keep_out(x, z)` holds. The look is asked for each block with where it sits on its panel: "along" and "up" in
    blocks, the panel's "length" and "rise", its "shade" and how deep into it the block is ("k")."""
    solids, clears = [], []
    for a, b, n, (l0, l1), shade in quads:
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        base = base_of(a, b, n)
        rise = rise_of(a, b, n, base)
        solid, cleared = {}, set()
        for s in np.arange(0, 1.0001, 0.2 / max(length, 1)):
            bx, bz = a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s
            lean = math.tan(math.radians(l0 + (l1 - l0) * s))
            for t in np.arange(0, 1.0001, 0.2 / rise):
                y = math.floor(base + t * rise)
                back = lean * t * rise
                for o in np.arange(0, back, 0.4):
                    cleared.add((math.floor(bx + n[0] * o), y, math.floor(bz + n[1] * o)))
                for k in np.arange(0, 2.0, 0.4):
                    c = (math.floor(bx + n[0] * (back + k)), y, math.floor(bz + n[1] * (back + k)))
                    if c not in solid:
                        solid[c] = dict(along=s * length, up=t * rise, length=length, rise=rise, shade=shade, k=k)
        solids.append(solid)
        clears.append(cleared)
    walls = [(round(q[2][0], 3), round(q[2][1], 3)) for q in quads]
    reach = {}
    for i, solid in enumerate(solids):
        for c in solid:
            reach.setdefault(c, []).append(i)
    shared = {}
    for c, who in reach.items():
        for i in who:
            for j in who:
                if i < j and walls[i] != walls[j]:
                    shared[(i, j)] = shared.get((i, j), 0) + 1
    dropped = set()
    for (i, j), count in sorted(shared.items(), key=lambda kv: -kv[1]):
        if count >= 3 and i not in dropped and j not in dropped:
            dropped.add(i if len(solids[i]) < len(solids[j]) else j)
    kept = [i for i in range(len(quads)) if i not in dropped]
    owner = {}
    for i in kept:
        a, b = quads[i][0], quads[i][1]
        for c in solids[i]:
            near = seg_dist(c[0] + .5, c[2] + .5, a, b)
            if c not in owner or near < owner[c][0]:
                owner[c] = (near, i)
    for i in kept:
        for c in clears[i] - owner.keys():
            if c[1] < ground(c[0], c[2]) and not is_floor(c[0], c[2]) and not keep_out(c[0], c[2]):
                w.set(*c, B.AIR)
    for c, (_, i) in owner.items():
        if not keep_out(c[0], c[2]):
            w.set(*c, *look.panel(*c, solids[i][c]))
    return owner, sorted(dropped)


def fallen_panel(w, a, b, n, reach, h0, h1, floor_y, is_floor, look):
    """A panel lying nearly flat where it fell: its foot at a-b, `reach` out along n, h0 over the floor at the foot and
    h1 at the far end. Whatever it fell on stays under it."""
    laid = {}
    for s in np.arange(0, 1.0001, 0.05):
        for t in np.arange(0, 1.0001, 0.03):
            x = math.floor(a[0] + (b[0] - a[0]) * s + n[0] * reach * t)
            z = math.floor(a[1] + (b[1] - a[1]) * s + n[1] * reach * t)
            if is_floor(x, z):
                laid[(x, z)] = (round(floor_y + h0 + (h1 - h0) * t), s, t)
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    for (x, z), (y, s, t) in laid.items():
        w.column(x, z, y, y + 6, B.AIR)
        w.set(x, y, z, *look.panel(x, y, z, dict(along=s * length, up=t * reach, length=length, rise=reach, shade=0,
                                                 k=0)))


# ---- the seam -------------------------------------------------------------------------------------------------------
def seam_trench(w, cells, seam_y, look):
    """A trench under plates down to the seam: lava at its foot, its rock scorched near the heat. `cells` is
    [(x, z, top)] with top the course the plates lie in."""
    seam_y = max(seam_y, 3)
    open_cells = {(x, z) for x, z, _ in cells}
    for x, z, top in cells:
        w.column(x, z, seam_y + 1, top - 1, B.AIR)                       # the plates' own course is the strip's
        w.set(x, seam_y, z, B.LAVA)
        w.column(x, z, seam_y - 2, seam_y - 1, *look.seam(x, seam_y - 1, z))
    for x, z, top in cells:
        for a, b in DIRS.values():
            if (x + a, z + b) not in open_cells:
                for y in range(seam_y, min(seam_y + 4, top)):
                    if w.id(x + a, y, z + b) != B.AIR:
                        w.set(x + a, y, z + b, *look.seam(x + a, y, z + b))


def plated_strip(w, lo, hi, width, rows, missing, feet, is_floor, seam_y, look):
    """Plates in two columns along lo -> hi over a trench to the seam; the plates of `missing` (row, column) gone.
    Returns the columns it covers."""
    run = math.hypot(hi[0] - lo[0], hi[1] - lo[1])
    ax = ((hi[0] - lo[0]) / run, (hi[1] - lo[1]) / run)
    edges = np.cumsum([0] + rows)
    xs = [lo[0], hi[0]]
    zs = [lo[1], hi[1]]
    covered, trench = set(), []
    for x in range(math.floor(min(xs) - width), math.ceil(max(xs) + width) + 1):
        for z in range(math.floor(min(zs) - width), math.ceil(max(zs) + width) + 1):
            u = (x + .5 - lo[0]) * ax[0] + (z + .5 - lo[1]) * ax[1]
            v = -(x + .5 - lo[0]) * ax[1] + (z + .5 - lo[1]) * ax[0]
            if not (0 <= u <= sum(rows) and abs(v) <= width / 2 and is_floor(x, z)):
                continue
            covered.add((x, z))
            row = min(int(np.searchsorted(edges, u, side="right") - 1), len(rows) - 1)
            col = 0 if v < 0 else 1
            top = feet(x, z) - 1
            if abs(v) <= width / 2 - 1.2:
                trench.append((x, z, top))
            if (row, col) not in missing:
                # a plate's border course reads as its frame
                inner_u = u - edges[row]
                rim = inner_u < 1 or inner_u > rows[row] - 1 or abs(v) > width / 2 - 1 or abs(v) < 0.6
                w.set(x, top, z, *look.plate(x, top, z, "rim" if rim else "plate"))
            else:
                w.set(x, top, z, B.AIR)
    seam_trench(w, trench, seam_y, look)
    return covered


# ---- spoil ----------------------------------------------------------------------------------------------------------
def spoil(w, toe, crest, peak, feet, is_floor, look):
    """A heap from its toe outline up to its crest line, `peak` over the floor at the crest."""
    cells = [c for c in poly_cells(toe) if is_floor(*c)]
    edge = lambda x, z: min(seg_dist(x, z, toe[i], toe[(i + 1) % len(toe)]) for i in range(len(toe)))  # noqa: E731
    ridge = lambda x, z: min(seg_dist(x, z, crest[i], crest[i + 1]) for i in range(len(crest) - 1))  # noqa: E731
    for x, z in cells:
        a, b = edge(x + .5, z + .5), ridge(x + .5, z + .5)
        h = int(round(peak * (a / (a + b + 1e-9)) ** 0.8))
        for y in range(feet(x, z), feet(x, z) + h):
            w.set(x, y, z, *look.spoil(x, y, z))
    return set(cells)


# ---- tunnels, ladders, stairs, wear ---------------------------------------------------------------------------------------
def bore(w, path, y0, y1, is_floor, look, width=2):
    """A drift four high along a path, its floor from y0 to y1, timbered every six blocks: posts at both sides, a beam
    over them and a light in the rock above the beam."""
    lengths = [math.hypot(path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) for i in range(len(path) - 1)]
    total = sum(lengths)
    done = 0.0
    frames = []
    for i, seg in enumerate(lengths):
        a, b = path[i], path[i + 1]
        ux, uz = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
        for s in np.arange(0, seg, 0.4):
            y = round(y0 + (y1 - y0) * (done + s) / total)
            px, pz = a[0] + ux * s, a[1] + uz * s
            for o in np.arange(-width, width + 0.01, 0.4):
                x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                if is_floor(x, z):
                    continue
                w.column(x, z, y, y + 3, B.AIR)
                w.set(x, y - 1, z, *look.tunnel_floor(x, z))
            if int(done + s) % 6 == 3 and (not frames or done + s - frames[-1] > 5):
                frames.append(done + s)
                for o in (-width - 0.2, width + 0.2):
                    x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                    if not is_floor(x, z):
                        w.column(x, z, y, y + 2, *look.timber("post"))
                for o in np.arange(-width - 0.2, width + 0.21, 0.4):
                    x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                    if not is_floor(x, z):
                        w.set(x, y + 3, z, *look.timber("beam"))
                w.set(math.floor(px), y + 4, math.floor(pz), *look.light())
        done += seg


def ladder_bay(w, x, z, side, bottom, ground, look):
    """A ladder up a cut wall from a floor at `bottom` to the crust: a rock backing behind it and a gap cut through
    whatever stands over the wall's lip."""
    dx, dz = DIRS[side]
    top = ground(x + dx, z + dz)
    w.column(x, z, bottom, top + 3, B.AIR)
    for y in range(bottom, top):
        w.set(x + dx, y, z + dz, *look.rock(x + dx, y, z + dz))
        w.set(x, y, z, B.LADDER, ladder_data((dx, dz)))
    for k in range(1, 7):
        for o in (-1, 0, 1):
            cx, cz = x + dx * k + (o if dx == 0 else 0), z + dz * k + (o if dz == 0 else 0)
            here = ground(cx, cz)
            w.column(cx, cz, here, here + 4, B.AIR)
            if k > 1 and w.id(cx, here - 1, cz) == B.AIR:
                w.set(cx, here - 1, cz, *look.crust(cx, cz))


def stairs(w, cells, feet, is_floor, uphill, look):
    """A stair on every one-block rise among `cells`, facing the neighbour one higher that lies most nearly uphill."""
    for x, z in cells:
        ux, uz = uphill(x, z)
        best = None
        for sx, sz in DIRS.values():
            if is_floor(x + sx, z + sz) and feet(x + sx, z + sz) == feet(x, z) + 1:
                score = sx * ux + sz * uz
                if best is None or score > best[0]:
                    best = (score, (sx, sz))
        if best:
            w.set(x, feet(x, z), z, *look.stair(x, z, stair_data(best[1])))


def wear(w, cells, feet, level_of, look):
    """Lumps worn into a floor: `level_of(x, z)` is 0, 1 (half a block) or 2 (a block) over the floor. A lump is kept
    within half a block of each neighbour, so the floor is walked without a jump."""
    level = {c: level_of(*c) for c in cells}
    for _ in range(3):
        for (x, z), v in list(level.items()):
            low = min(level.get((x + a, z + b), 0) for a, b in DIRS.values())
            level[(x, z)] = min(v, low + 1)
    worn = 0
    for (x, z), v in level.items():
        y = feet(x, z)
        if v and w.id(x, y, z) == B.AIR:
            w.set(x, y, z, *look.lump(x, z, v))
            worn += 1
    return worn


def crust_hollow(w, cells, ground, look, depth=4):
    """Ground slumped out from behind a wall that gave way: the crust lowered by `depth` over those columns."""
    for x, z in cells:
        top = ground(x, z)
        w.column(x, z, top - depth, top - 1, B.AIR)
        w.set(x, top - depth - 1, z, *look.spoil(x, top - depth - 1, z))


def lay_crust(w, x, z, ground, look):
    """A column's overburden and the crust on it: the orange beds from the stone up, then the crust's top, as many
    blocks lower as the look sinks it."""
    top = ground(x, z) - 1
    for depth in range(1, look.thickness(x, z) + 1):
        w.set(x, top - depth, z, *look.overburden(x, top - depth, z, depth))
    for _ in range(look.sunk(x, z)):
        w.set(x, top, z, B.AIR)
        top -= 1
    w.set(x, top, z, *look.crust(x, z))


ROCKY = {B.STONE, B.COBBLE, B.STAINED_CLAY, B.CLAY}


def rock_faces(w, floor_cells, feet, keep_out, lean, notch, look, reach=3, open_beyond=8):
    """Bare rock walls made to overhang and be undercut, never climbed. A face is a rock column beside a floor whose
    block over the floor is rock. Over the floor up to `reach` out from a face the face's own column is carried
    across, from a height that rises with the distance out to the column's top, so the jutting rock is unbroken up to
    the crust and starts at least three over the floor, and only where the floor runs on `open_beyond` past it, so no
    gap across a cut is narrowed to a jump; `lean(face)` (0 to 1) says how far a face juts. At the foot of
    a face where `notch(face)` is high the rock is hollowed two or three high, one or two deep. Returns the columns
    jutted over and the columns hollowed."""
    floor_set = set(floor_cells)
    faces = {}
    for x, z in floor_set:
        if keep_out(x, z):
            continue
        for a, b in DIRS.values():
            c = (x + a, z + b)
            if c in floor_set or keep_out(*c) or c in faces:
                continue
            block = w.get(c[0], feet(x, z) + 1, c[1])
            if block[0] in ROCKY and not (block[0] == B.STONE and block[1] == 6):
                faces[c] = (feet(x, z), (-a, -b))
    # how far out each floor column lies from a face, and which face
    reached, frontier = {}, []
    for c, (f, _) in faces.items():
        for a, b in DIRS.values():
            n = (c[0] + a, c[1] + b)
            if n in floor_set and not keep_out(*n) and n not in reached:
                reached[n] = (1, c)
                frontier.append(n)
    for d in range(2, reach + 1):
        nxt = []
        for cell in frontier:
            for a, b in DIRS.values():
                n = (cell[0] + a, cell[1] + b)
                if n in floor_set and not keep_out(*n) and n not in reached:
                    reached[n] = (d, reached[cell][1])
                    nxt.append(n)
        frontier = nxt
    jutted = set()
    for (x, z), (d, s) in reached.items():
        r = int(lean(*s) * (reach + 1))
        if d > r:
            continue
        a, b = faces[s][1]
        if not all((s[0] + a * k, s[1] + b * k) in floor_set for k in range(d, d + open_beyond + 1)):
            continue                       # a jut over a narrow cut would leave a gap a player could jump
        f = feet(x, z)
        top = w.top(*s)
        h = f + max(3, int((top - f) * 0.55)) + (d - 1) * 2
        if h >= top:
            continue
        for y in range(h, top + 1):
            w.set(x, y, z, *w.get(s[0], y, s[1]))
        jutted.add((x, z))
    hollowed = set()
    for c, (f, (a, b)) in faces.items():
        v = notch(*c)
        if v < 0.62:
            continue
        high = 2 if v < 0.82 else 3
        for k in (0, 1) if v > 0.74 else (0,):
            x, z = c[0] + a * k, c[1] + b * k
            if w.top(x, z) < f + high + 3:
                continue
            w.column(x, z, f, f + high - 1, B.AIR)
            w.set(x, f - 1, z, *look.cut_floor(x, z))
            hollowed.add((x, z))
    return jutted, hollowed
