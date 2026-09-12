#!/usr/bin/env python3
"""Author a new unit in the series' own language, and hand it back in the form a traced one comes in.

The language is not rooms. Measured off the three maps, a Thunder island is a **ribbon**: a band of ground
between eight and twenty-eight blocks wide that wanders, swells and narrows, thirty-odd vertices long and
about a quarter as compact as a disc. Nothing in the series is a corridor meeting a plaza; nothing in it has
a hub. The centre island of every one of the three is a quad of eighty-five to a hundred and thirteen blocks
— four or five vertices, near-square — and that is all it is.

So an island is authored here as a **centreline with a half-width at each point**, one or more strokes to a
island. Strokes are laid down at one block, the union carved along a noise field so the coast is bays and
headlands rather than offsets, its boundary walked, and the ring reduced by Douglas-Peucker at the tolerance
`IslandSimplifier` uses. What comes out is a simplified polygon of the same kind `--island-sketch` returns
for a real map, and it goes down the identical path afterwards.

    python3 author_unit.py thunderhead
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOLERANCE = 1.6


# ── strokes ──────────────────────────────────────────────────────────────────────────────────────
def stroke_cells(points):
    """A centreline swept by its half-width, as a set of blocks. Swept rather than offset: a disc is stamped
    at every step along the line, so a bend cannot pinch the inside of the turn or leave a notch on the
    outside, and the width may change between one point and the next without a seam."""
    cells = set()
    for i in range(len(points) - 1):
        (x1, z1, w1), (x2, z2, w2) = points[i], points[i + 1]
        span = max(1, int(math.dist((x1, z1), (x2, z2)) * 2))
        for step in range(span + 1):
            t = step / span
            cx, cz, r = x1 + (x2 - x1) * t, z1 + (z2 - z1) * t, w1 + (w2 - w1) * t
            for dz in range(-int(r) - 1, int(r) + 2):
                for dx in range(-int(r) - 1, int(r) + 2):
                    if dx * dx + dz * dz <= r * r:
                        cells.add((int(cx) + dx, int(cz) + dz))
    return cells


def _noise(x, z, scale, seed):
    """Value noise on a lattice, smoothstepped between corners. Deterministic in the coordinate, so a coast
    is the same every run."""
    def at(ix, iz):
        h = (ix * 374761393 + iz * 668265263 + seed * 1274126177) & 0xFFFFFFFF
        h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((h ^ (h >> 16)) & 0xFFFF) / 0xFFFF * 2 - 1
    fx, fz = x / scale, z / scale
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    sx, sz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    top = at(ix, iz) * (1 - sx) + at(ix + 1, iz) * sx
    bot = at(ix, iz + 1) * (1 - sx) + at(ix + 1, iz + 1) * sx
    return top * (1 - sz) + bot * sz


def carve(cells, reach=6, scale=13, seed=1):
    """Move the coast in and out along a smooth field. A swept stroke has a machined edge; a Thunder island
    does not. Only the band within `reach` of the boundary is touched, so a stroke cannot be severed."""
    def grow(seed_cells, times):
        out = set(seed_cells)
        for _ in range(times):
            out |= {(c[0] + dx, c[1] + dz) for c in out for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        return out

    def shrink(seed_cells, times):
        out = set(seed_cells)
        for _ in range(times):
            out = {c for c in out
                   if all((c[0] + dx, c[1] + dz) in out for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        return out

    depth = {}
    layer = set(cells)
    for step in range(1, reach + 1):                       # positive: how deep inside the stroke
        nxt = shrink(layer, 1)
        for cell in layer - nxt:
            depth[cell] = step
        layer = nxt
    core = layer
    layer = set(cells)
    for step in range(1, reach + 1):                       # negative: how far outside it
        nxt = grow(layer, 1)
        for cell in nxt - layer:
            depth[cell] = -step
        layer = nxt

    out = set(core)
    for cell, d in depth.items():
        if d > _noise(cell[0], cell[1], scale, seed) * reach:
            out.add(cell)
    if not out:
        return cells
    centre = (sum(c[0] for c in cells) / len(cells), sum(c[1] for c in cells) / len(cells))
    start = min(out, key=lambda c: (c[0] - centre[0]) ** 2 + (c[1] - centre[1]) ** 2)
    seen, queue = {start}, [start]
    while queue:
        cell = queue.pop()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cell[0] + dx, cell[1] + dz)
            if nxt in out and nxt not in seen:
                seen.add(nxt); queue.append(nxt)
    return seen


# ── outline ──────────────────────────────────────────────────────────────────────────────────────
def outline(cells):
    """Every ring of the boundary. A cell contributes its four unit edges; an edge two cells share cancels;
    what is left is followed corner to corner, straight ahead where possible."""
    edges = {}
    for x, z in cells:
        for a, b in (((x, z), (x + 1, z)), ((x + 1, z), (x + 1, z + 1)),
                     ((x + 1, z + 1), (x, z + 1)), ((x, z + 1), (x, z))):
            if (b, a) in edges:
                del edges[(b, a)]
            else:
                edges[(a, b)] = True
    outgoing = {}
    for a, b in edges:
        outgoing.setdefault(a, []).append(b)
    rings = []
    while any(outgoing.values()):
        start = min(k for k, v in outgoing.items() if v)
        ring, here, came = [start], outgoing[start].pop(0), start
        while here != start:
            ring.append(here)
            options = outgoing.get(here) or []
            if not options:
                break
            direction = (here[0] - came[0], here[1] - came[1])
            order = [(direction[1], -direction[0]), direction, (-direction[1], direction[0])]
            nxt = next((c for step in order
                        for c in [(here[0] + step[0], here[1] + step[1])] if c in options), options[0])
            options.remove(nxt)
            came, here = here, nxt
        rings.append([list(p) for p in ring])
    return rings


def area_of(ring):
    return abs(sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1]
                   for i in range(len(ring))) / 2)


def simplify(ring, tolerance=TOLERANCE):
    """Douglas-Peucker, the reduction `IslandSimplifier` applies to a scanned island."""
    def run(points):
        if len(points) < 3:
            return points
        (x0, z0), (x1, z1) = points[0], points[-1]
        worst, at = 0.0, 0
        for i in range(1, len(points) - 1):
            x, z = points[i]
            span = math.dist((x0, z0), (x1, z1))
            gap = abs((x1 - x0) * (z0 - z) - (x0 - x) * (z1 - z0)) / span if span else math.dist((x, z), (x0, z0))
            if gap > worst:
                worst, at = gap, i
        if worst <= tolerance:
            return [points[0], points[-1]]
        return run(points[:at + 1])[:-1] + run(points[at:])
    out = run(ring + [ring[0]])
    return out[:-1]


def compactness(ring):
    perimeter = sum(math.dist(ring[i], ring[(i + 1) % len(ring)]) for i in range(len(ring)))
    return 4 * math.pi * area_of(ring) / perimeter ** 2 if perimeter else 0


def collides(islands):
    """Does the unit run into its own quarter-turn image? Under rot_90 a piece at (x, z) has one at (z, −x),
    and a unit that reaches along an axis meets itself. Checked on the cells, not on the bounding boxes."""
    cells = set()
    for island in islands:
        xs = [v[0] for v in island['vertices']]; zs = [v[1] for v in island['vertices']]
        for z in range(int(min(zs)), int(max(zs)) + 1):
            for x in range(int(min(xs)), int(max(xs)) + 1):
                if _inside(island['vertices'], x + 0.5, z + 0.5):
                    cells.add((x, z))
    for turn in (1, 2, 3):
        image = cells
        for _ in range(turn):
            image = {(c[1], -c[0]) for c in image}
        if cells & image:
            return len(cells & image)
    return 0


def _inside(poly, x, z):
    hit = False
    for i in range(len(poly)):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % len(poly)]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1:
            hit = not hit
    return hit


def main():
    board = sys.argv[1]
    source = json.load(open(f'{HERE}/{board}.author.json'))
    islands = []
    for spec in source['islands']:
        if 'vertices' in spec:                              # stated outright: the centre quad
            ring = [[float(v[0]), float(v[1])] for v in spec['vertices']]
            holes = []
        else:
            cells = set()
            for line in spec['strokes']:
                cells |= stroke_cells([tuple(p) for p in line])
            cells = carve(cells, seed=spec.get('seed', 1))
            rings = sorted(outline(cells), key=area_of, reverse=True)
            ring = simplify(rings[0])
            holes = [simplify(r) for r in rings[1:] if area_of(r) >= 30]
        islands.append({'id': f'a{len(islands) + 1}_island',
                        'vertices': [[float(v[0]), float(v[1])] for v in ring],
                        'holes': [[[float(v[0]), float(v[1])] for v in h] for h in holes],
                        'carries': spec.get('carries', []), 'rank': len(islands), 'axis': bool(spec.get('axis'))})
        print(f'  {spec["id"]:12s} area {area_of(ring):7.0f}  {len(ring):3d}v  '
              f'compact {compactness(ring):.3f}  {len(holes)} hole(s)'
              + ('  [axis]' if spec.get('axis') else '')
              + (f'  carries {",".join(spec.get("carries", []))}' if spec.get('carries') else ''))

    unit = {'board': board, 'team': 'blue', 'centre': source['centre'], 'maxbuild': source['maxbuild'],
            'spawn': source['spawn'], 'spawn_box': source['spawn_box'], 'wool_room': source['wool_room'],
            'unit': [i for i in islands if not i['axis']],
            'axis': [i for i in islands if i['axis']]}
    hits = collides(unit['unit'])
    print(f'  rot_90 self-collision: {"none" if not hits else str(hits) + " CELLS — FIX THE UNIT"}')
    json.dump(unit, open(f'{HERE}/{board}.unit.json', 'w'), indent=1)
    print(f'{board}: {len(unit["unit"])} unit island(s) + {len(unit["axis"])} axis → {board}.unit.json')


if __name__ == '__main__':
    main()
