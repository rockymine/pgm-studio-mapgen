#!/usr/bin/env python3
"""Draw a plan document as ASCII so its structure can be read as a shape."""
import json, sys

GLYPH = {'spawn': 'S', 'wool-room': 'W', 'buffer': '.', 'piece': None}


def draw(path, mirror=False):
    p = json.load(open(path))
    g = p.get('globals', {})
    pieces = [q for q in p['pieces']]
    zones = p.get('zones', [])
    xs = [q['rect'][0] for q in pieces] + [q['rect'][0] + q['rect'][2] for q in pieces]
    zs = [q['rect'][1] for q in pieces] + [q['rect'][1] + q['rect'][3] for q in pieces]
    for z in zones:
        xs += [z['rect'][0], z['rect'][0] + z['rect'][2]]
        zs += [z['rect'][1], z['rect'][1] + z['rect'][3]]
    if mirror:                                        # show the rot_180 image too
        xs += [-v for v in xs]; zs += [-v for v in zs]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)

    grid = [[' '] * (x1 - x0) for _ in range(z1 - z0)]
    letters = {}
    nxt = [0]

    def put(rect, ch, over=False):
        rx, rz, rw, rh = rect
        for z in range(rz, rz + rh):
            for x in range(rx, rx + rw):
                if 0 <= z - z0 < len(grid) and 0 <= x - x0 < len(grid[0]):
                    if over or grid[z - z0][x - x0] == ' ':
                        grid[z - z0][x - x0] = ch

    for q in pieces:
        role = q.get('role', 'piece')
        ch = GLYPH.get(role)
        if ch is None:
            pool = '0123456789ABCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvxyz'
            ch = pool[nxt[0] % len(pool)]; nxt[0] += 1
        letters[ch] = f"{q['id']} s{q.get('surface', g.get('surface'))}"
        put(q['rect'], ch)
    if mirror:
        for q in pieces:
            rx, rz, rw, rh = q['rect']
            put([-rx - rw, -rz - rh, rw, rh], '#')
    for zn in zones:
        ch = '~' if zn.get('kind') == 'water-lane' else '+'
        put(zn['rect'], ch)
        letters[ch] = f"zone {zn['id']} ({zn.get('kind','build')})"

    print(f"== {path}   cell {g.get('cell')} sym {g.get('symmetry')} surface {g.get('surface')} "
          f"players {g.get('maxPlayers')}  |  x {x0}..{x1}  z {z0}..{z1}  "
          f"({(x1-x0)*g.get('cell',5)} x {(z1-z0)*g.get('cell',5)} blocks)")
    for i, row in enumerate(reversed(grid)):           # +z up the page
        print(f"{z1 - 1 - i:4} |{''.join(row)}|")
    print(f"     {' ' * 1}{''.join('|' if (x - x0) % 10 == 0 else ' ' for x in range(x0, x1))}")
    print('      ' + f'x from {x0} to {x1}')
    for ch, name in sorted(letters.items()):
        print(f"   {ch} = {name}")
    ground = sum(q['rect'][2] * q['rect'][3] for q in pieces if q.get('role') != 'buffer')
    print(f"   ground cells {ground}  bbox cells {(x1-x0)*(z1-z0)}  fill {ground/((x1-x0)*(z1-z0)):.3f}")
    for key in ('placements', 'walls'):
        if p.get(key):
            print(f"   {key}: {json.dumps(p[key])[:400]}")


if __name__ == '__main__':
    draw(sys.argv[1], '--mirror' in sys.argv)
