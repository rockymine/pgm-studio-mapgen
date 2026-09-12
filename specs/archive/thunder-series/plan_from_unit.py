#!/usr/bin/env python3
"""Turn a traced unit into a plan document at one block per cell.

The plan and the sketch describe the same ground in two languages. The sketch speaks polygons and gets the
traced outline verbatim; the plan speaks rectangles and cannot. So the plan is not a drawing here — it is the
*statement* layer: the two rectangles the original map declares in its XML (the spawn box and the wool room)
placed exactly where the original put them, and enough rectangle inside each island for the compiler to
derive an intent from — teams, wools, monuments, build zones, maximum build height.

Those filling rectangles are found rather than chosen: each island's polygon is rasterized at one block,
the two declared rectangles are cut out of it, and the largest axis-aligned rectangle left is taken, then
the next largest, until what remains is too small to be a piece. That is a cover, not a decomposition — it
does not have to be exact, because the land the player walks on comes from the polygon.

    python3 plan_from_unit.py thunder
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_PIECE = 16            # blocks: below this a rectangle is a sliver, not a piece
MAX_PIECES = 30           # per island


def inside(poly, x, z):
    hit = False
    for i in range(len(poly)):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % len(poly)]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1:
            hit = not hit
    return hit


def rasterize(poly, holes, cuts):
    """The island as a grid of one-block cells, with the declared rectangles cut out of it."""
    xs = [v[0] for v in poly]
    zs = [v[1] for v in poly]
    x0, x1 = int(min(xs)), int(max(xs))
    z0, z1 = int(min(zs)), int(max(zs))
    grid = []
    for z in range(z0, z1):
        row = []
        for x in range(x0, x1):
            on = inside(poly, x + 0.5, z + 0.5) and not any(inside(h, x + 0.5, z + 0.5) for h in holes)
            if on and any(cx0 <= x < cx1 and cz0 <= z < cz1 for cx0, cz0, cx1, cz1 in cuts):
                on = False
            row.append(1 if on else 0)
        grid.append(row)
    return grid, x0, z0


def largest_rect(grid):
    """Largest all-ones axis-aligned rectangle, by the stack-of-histograms method. Returns
    (x, z, w, h) in grid coordinates, or None."""
    if not grid or not grid[0]:
        return None
    width = len(grid[0])
    heights = [0] * width
    best = (0, None)
    for z, row in enumerate(grid):
        for x in range(width):
            heights[x] = heights[x] + 1 if row[x] else 0
        stack = []
        for x in range(width + 1):
            height = heights[x] if x < width else 0
            start = x
            while stack and stack[-1][1] >= height:
                left, tall = stack.pop()
                area = tall * (x - left)
                if area > best[0]:
                    best = (area, (left, z - tall + 1, x - left, tall))
                start = left
            stack.append((start, height))
    return best[1]


def cover(grid, x0, z0, limit=MAX_PIECES, floor=MIN_PIECE):
    rects = []
    for _ in range(limit):
        found = largest_rect(grid)
        if not found:
            break
        gx, gz, w, h = found
        if w * h < floor:
            break
        rects.append((x0 + gx, z0 + gz, w, h))
        for z in range(gz, gz + h):
            for x in range(gx, gx + w):
                grid[z][x] = 0
    return rects


def touching(a, b):
    """Two rects share a border of positive length (LN4: a corner is not a join)."""
    ax0, az0, aw, ah = a
    bx0, bz0, bw, bh = b
    ax1, az1, bx1, bz1 = ax0 + aw, az0 + ah, bx0 + bw, bz0 + bh
    overlap_x = min(ax1, bx1) - max(ax0, bx0)
    overlap_z = min(az1, bz1) - max(az0, bz0)
    if overlap_x > 0 and (az1 == bz0 or bz1 == az0):
        return True
    if overlap_z > 0 and (ax1 == bx0 or bx1 == ax0):
        return True
    return overlap_x > 0 and overlap_z > 0


def keep_connected(named, seeds=()):
    """Drop any rectangle not reachable from the seeds — or, with no seeds, from the largest one. A plan
    piece hanging in the void is a structural error and the compiler is right to refuse it; the polygon
    still carries that ground either way.

    The seeds are the declared rectangles, and seeding matters: the spawn box and the wool room are the two
    things this plan exists to state, so the component that survives has to be the one holding them, never
    whichever happens to be biggest."""
    if not named:
        return []
    picked = [i for i, (name, _) in enumerate(named) if name in seeds]
    if not picked:
        picked = [max(range(len(named)), key=lambda i: named[i][1][2] * named[i][1][3])]
    seen = set(picked)
    changed = True
    while changed:
        changed = False
        for i in range(len(named)):
            if i in seen:
                continue
            if any(touching(named[i][1], named[j][1]) for j in seen):
                seen.add(i); changed = True
    return [named[i] for i in sorted(seen)]


def main():
    board = sys.argv[1]
    unit = json.load(open(f'{HERE}/{board}.unit.json'))
    surface = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    spawn_box = tuple(unit['spawn_box'])
    wool_room = tuple(unit['wool_room'])

    pieces = []
    for island in unit['unit']:
        cuts = [spawn_box, wool_room] if island['carries'] else []
        grid, x0, z0 = rasterize(island['vertices'], island['holes'], cuts)
        rects = cover(grid, x0, z0)
        stem = island['id'].split('_')[0]
        named = [(f'{stem}-{n}', r) for n, r in enumerate(rects)]
        if 'spawn' in island['carries']:
            named.append(('spawn', (spawn_box[0], spawn_box[1],
                                    spawn_box[2] - spawn_box[0], spawn_box[3] - spawn_box[1])))
        if 'wool-room' in island['carries']:
            named.append(('wool-room', (wool_room[0], wool_room[1],
                                        wool_room[2] - wool_room[0], wool_room[3] - wool_room[1])))
        for name, rect in keep_connected(named, seeds={'spawn', 'wool-room'}):
            role = 'spawn' if name == 'spawn' else 'wool-room' if name == 'wool-room' else 'piece'
            pieces.append({'id': name, 'role': role, 'rect': list(rect), 'surface': surface})

    for island in unit['axis']:
        grid, x0, z0 = rasterize(island['vertices'], island['holes'], [])
        stem = island['id'].split('_')[0]
        for name, rect in keep_connected([(f'{stem}-{n}', r) for n, r in enumerate(cover(grid, x0, z0, floor=40))]):
            pieces.append({'id': name, 'role': 'piece', 'rect': list(rect),
                           'surface': surface, 'mirrors': False})

    print(f'{board}: {len(pieces)} pieces at cell 1')
    for p in pieces:
        print(f"  {p['id']:12s} {p['role']:10s} {p['rect']}")
    json.dump(pieces, open(f'{HERE}/{board}.pieces.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
