#!/usr/bin/env python3
"""Read a Thunder-series map as the studio sees it, and hand back the unit a rot_90 plan is authored from.

Two inputs, neither of them an image:

  * `<map>.islands.json` — the output of `PgmStudio.RoundTrip --island-sketch`, which walks the world's
    cleaned base, runs the island detector over it and pushes every island's outline through
    Douglas-Peucker. That is the map's real land: one simplified polygon per island, in block coordinates.
  * `<map>/map.xml` — read for the rectangles that are not shapes but statements: each team's spawn point
    and spawn-protect box, its wool room, and its monument row.

The series is rot_90 about a centre, so the board is one team's islands plus whatever sits on the axis.
This picks that unit: every island assigned to the chosen team (by which of the four rotational sectors its
centroid falls in), plus the centre island, and reports each one's role — which island the spawn stands on,
which the wool room is cut into — so a plan can place the two rectangles it must place exactly where the
original put them.
"""
import json, math, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


# ── map.xml ──────────────────────────────────────────────────────────────────────────────────────
def read_xml(path):
    """The declared rectangles. Only what a plan has to reproduce: spawn points, spawn boxes, wool rooms,
    monuments. Regions are `min`/`max` pairs in either order, so both are normalised here."""
    text = open(path, encoding='utf-8', errors='replace').read()
    out = {'spawns': {}, 'wool_rooms': {}, 'spawn_boxes': {}, 'monuments': defaultdict(list),
           'wools': [], 'centre': (0.0, 0.0), 'maxbuild': None}

    for team, body in re.findall(r'<spawn team="([\w-]+)"[^>]*>(.*?)</spawn>', text, re.S):
        pt = re.search(r'base="(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)"', body) \
             or re.search(r'<block>(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)</block>', body)
        if pt:
            out['spawns'][team] = (float(pt.group(1)), float(pt.group(3)))

    for rid, a1, a2, b1, b2 in re.findall(
            r'<rectangle id="([\w-]+)" min="(-?\d+),(-?\d+)" max="(-?\d+),(-?\d+)"/>', text):
        rect = (min(int(a1), int(b1)), min(int(a2), int(b2)),
                max(int(a1), int(b1)), max(int(a2), int(b2)))
        if rid.endswith('-wool'):
            out['wool_rooms'][rid[:-5]] = rect
        elif rid.endswith('-spawn') or rid.endswith('-spawn-protect'):
            out['spawn_boxes'][rid.split('-spawn')[0]] = rect

    # Thunderstorm cuts its wool rooms as a <complement> — an outer box with the corners chamfered off by a
    # stack of further rectangles. The first rectangle is the box, and the box is what a plan states.
    for rid, body in re.findall(r'<complement id="([\w-]+)">(.*?)</complement>', text, re.S):
        first = re.search(r'<rectangle min="(-?\d+),(-?\d+)" max="(-?\d+),(-?\d+)"/>', body)
        if first and rid.endswith('-wool-room'):
            a1, a2, b1, b2 = (int(g) for g in first.groups())
            out['wool_rooms'].setdefault(rid[:-10], (min(a1, b1), min(a2, b2), max(a1, b1), max(a2, b2)))

    for team, colour, x, y, z in re.findall(
            r'<wool team="([\w-]+)" color="([\w ]+)" location="(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)"', text):
        out['wools'].append({'team': team, 'color': colour, 'at': (float(x), float(z))})

    for block in re.findall(r'<monument>\s*<block>(-?\d+),(-?\d+),(-?\d+)</block>', text):
        out['monuments']['all'].append((int(block[0]), int(block[2])))

    height = re.search(r'<maxbuildheight>(\d+)</maxbuildheight>', text)
    out['maxbuild'] = int(height.group(1)) if height else None

    if out['spawns']:
        xs = [p[0] for p in out['spawns'].values()]
        zs = [p[1] for p in out['spawns'].values()]
        out['centre'] = (round(sum(xs) / len(xs), 1), round(sum(zs) / len(zs), 1))
    return out


# ── islands ──────────────────────────────────────────────────────────────────────────────────────
def read_islands(path):
    layout = json.load(open(path))
    out = []
    for shape in layout['layout']['shapes']:
        if shape.get('operation') == 'subtract':
            continue
        verts = [[float(v[0]), float(v[1])] for v in shape['vertices']]
        out.append({'id': shape['id'], 'vertices': verts,
                    'holes': [], 'area': abs(shoelace(verts)), 'centroid': centroid(verts)})
    for shape in layout['layout']['shapes']:
        if shape.get('operation') != 'subtract':
            continue
        verts = [[float(v[0]), float(v[1])] for v in shape['vertices']]
        stem = shape['id'].split('_')[0]
        for island in out:
            if island['id'].split('_')[0] == stem:
                island['holes'].append(verts)
    return out


def shoelace(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly))) / 2


def centroid(poly):
    area = shoelace(poly)
    if abs(area) < 1e-9:
        return [sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly)]
    cx = cz = 0.0
    for i in range(len(poly)):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % len(poly)]
        cross = x1 * z2 - x2 * z1
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    return [cx / (6 * area), cz / (6 * area)]


def inside(poly, x, z):
    hit = False
    for i in range(len(poly)):
        x1, z1 = poly[i]
        x2, z2 = poly[(i + 1) % len(poly)]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1:
            hit = not hit
    return hit


# ── the unit ─────────────────────────────────────────────────────────────────────────────────────
def sector(point, centre, index):
    """Which of the four quarter-turn sectors a point falls in, numbered anticlockwise from the one
    containing the given team's spawn."""
    angle = math.degrees(math.atan2(point[1] - centre[1], point[0] - centre[0])) - index
    return int(((angle + 45) % 360) // 90)


def unit_of(islands, xml, team, axis_area=400.0):
    """One team's islands plus the axis islands. An island whose centroid sits within `axis_area`-ish of the
    centre belongs to nobody and is authored once with mirrors:false; every other island belongs to the
    sector its centroid is in."""
    centre = xml['centre']
    spawn = xml['spawns'][team]
    base = math.degrees(math.atan2(spawn[1] - centre[1], spawn[0] - centre[0]))
    mine, axis = [], []
    for island in islands:
        offset = math.hypot(island['centroid'][0] - centre[0], island['centroid'][1] - centre[1])
        if offset < math.sqrt(island['area']):          # sits on the centre: an axis island
            axis.append(island)
        elif sector(island['centroid'], centre, base) == 0:
            mine.append(island)
    mine.sort(key=lambda i: -i['area'])
    return mine, axis


def roles(mine, xml, team):
    """Which island carries what. The spawn point and the wool room are the two rectangles a plan must
    state; this says which traced island each of them is cut into, so the plan's rects and the sketch's
    polygons describe the same piece of ground."""
    spawn = xml['spawns'][team]
    room = xml['wool_rooms'].get(team)
    room_mid = ((room[0] + room[2]) / 2, (room[1] + room[3]) / 2) if room else None
    for rank, island in enumerate(mine):
        island['rank'] = rank
        island['carries'] = []
        if inside(island['vertices'], *spawn):
            island['carries'].append('spawn')
        if room_mid and inside(island['vertices'], *room_mid):
            island['carries'].append('wool-room')
    return mine


def main():
    board = sys.argv[1]
    root = sys.argv[2]
    team = sys.argv[3] if len(sys.argv) > 3 else None
    xml = read_xml(os.path.join(root, 'map.xml'))
    islands = read_islands(os.path.join(HERE, f'{board}.islands.json'))
    team = team or sorted(xml['spawns'])[0]

    print(f'{board}: centre {xml["centre"]}  maxbuild {xml["maxbuild"]}  teams {sorted(xml["spawns"])}')
    print(f'  {len(islands)} islands, areas {sorted((round(i["area"]) for i in islands), reverse=True)}')
    mine, axis = unit_of(islands, xml, team)
    roles(mine, xml, team)
    print(f'  unit = team {team}: {len(mine)} island(s) + {len(axis)} axis island(s)')
    for island in mine:
        vs = island['vertices']
        print(f'    {island["id"]:12s} area {round(island["area"]):6d}  {len(vs):3d}v  '
              f'x {round(min(v[0] for v in vs))}..{round(max(v[0] for v in vs))}  '
              f'z {round(min(v[1] for v in vs))}..{round(max(v[1] for v in vs))}  '
              f'{",".join(island["carries"]) or "-"}')
    for island in axis:
        print(f'    {island["id"]:12s} area {round(island["area"]):6d}  {len(island["vertices"]):3d}v  ON AXIS')
    print(f'  spawn  {xml["spawns"][team]}  box {xml["spawn_boxes"].get(team)}')
    print(f'  wool   {xml["wool_rooms"].get(team)}')

    json.dump({'board': board, 'team': team, 'centre': xml['centre'], 'maxbuild': xml['maxbuild'],
               'spawn': xml['spawns'][team], 'spawn_box': xml['spawn_boxes'].get(team),
               'wool_room': xml['wool_rooms'].get(team),
               'unit': mine, 'axis': axis},
              open(os.path.join(HERE, f'{board}.unit.json'), 'w'), indent=1)
    print(f'  → {board}.unit.json')


if __name__ == '__main__':
    main()
