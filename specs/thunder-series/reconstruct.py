#!/usr/bin/env python3
"""Rebuild a Thunder-series map in the studio from its own traced geometry.

    python3 reconstruct.py thunder

Nothing here is drawn by eye. The land is the polygon `--island-sketch` derived from the world's cleaned
base; the spawn box and the wool room are the rectangles the map's own XML declares; the rotation centre is
the one the four spawns actually turn about. The plan is authored at **one block per cell** so those
rectangles land where the original put them rather than snapping to a five-block grid.

The two documents divide as follows. The **plan** states what a rectangle can state — the spawn, the wool
room, a rectangle cover inside each island for the compiler to derive an intent from, the build zones, the
maximum build height — and compiles to an intent. The **sketch** then throws away the compiler's rectangles
and puts the traced polygons in their place, because the shape of this land is the whole point and a
rectangle cover is not it. A light Bezier pass afterwards takes the Douglas-Peucker corners off, which is
what the original coasts look like: carved, not drawn.
"""
import json, math, os, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curves import controls_for, flatten, self_intersections, outward_normal

API = 'http://localhost:5189/api'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('THUNDER_OUT', HERE)
DESERT_BRICK = 2

# Ground height and build ceiling, read off each map rather than chosen: the y its spawns stand at and the
# <maxbuildheight> its XML declares.
GROUND = {'thunder': 7, 'thundershock': 13, 'thunderstorm': 10, 'thunderhead': 8}


def call(method, path, body=None, quiet=False):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data, {'Content-Type': 'application/json'}, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=2400)
        text = r.read().decode()
        if not quiet:
            print(f'  {method:5} {path:48} -> {r.status}')
        return r.status, (json.loads(text) if text else {})
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        print(f'  {method:5} {path:48} -> {e.code}  {text[:500]}')
        try:
            return e.code, json.loads(text)
        except Exception:
            return e.code, text


def desert_brick():
    st, row = call('GET', f'/room-styles/{DESERT_BRICK}/json', quiet=True)
    if st != 200:
        sys.exit('room-style library has no desert brick — run  dotnet run tools/seed-library.cs')
    return json.loads(row['styleJson'])


# ── the frame ────────────────────────────────────────────────────────────────────────────────────
def origin_of(centre):
    """The plan is authored about the cell grid's origin, so the map is moved until its own rotation centre
    sits there. Thunder turns about (0.5, 0.5) and the other two about a half block likewise — a cell grid
    cannot hold a half, so the shift is rounded and every image lands one block off true. Over a 240-block
    board that is invisible, and it is the only liberty taken with the original's coordinates."""
    return (int(math.floor(centre[0] + 0.5)), int(math.floor(centre[1] + 0.5)))


def moved(point, origin):
    return [point[0] - origin[0], point[1] - origin[1]]


# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
def assemble_plan(board, unit, pieces, origin):
    ground = GROUND[board]
    spawn = moved(unit['spawn'], origin)
    room = unit['wool_room']
    wool = next((w for w in [] if w), None)

    moved_pieces = []
    for piece in pieces:
        x, z, w, h = piece['rect']
        entry = {'id': piece['id'], 'role': piece['role'],
                 'rect': [x - origin[0], z - origin[1], w, h], 'surface': ground}
        if piece.get('mirrors') is False:
            entry['mirrors'] = False
        moved_pieces.append(entry)

    # One build zone over the unit and one over the axis island. The originals are more careful than this —
    # Thunder names five rectangles, Thunderstorm a circle and four bridges — but every one of them says the
    # same thing about this unit: the void between a team's own islands, and the void between them and the
    # middle, is bridgeable. The zone that says it is the unit's own extent.
    xs = [p['rect'][0] for p in moved_pieces] + [p['rect'][0] + p['rect'][2] for p in moved_pieces]
    zs = [p['rect'][1] for p in moved_pieces] + [p['rect'][1] + p['rect'][3] for p in moved_pieces]
    zones = [{'id': 'unit-court', 'rect': [min(xs) - 8, min(zs) - 8,
                                           max(xs) - min(xs) + 16, max(zs) - min(zs) + 16], 'holes': []}]

    spawn_piece = next(p for p in moved_pieces if p['role'] == 'spawn')
    room_piece = next(p for p in moved_pieces if p['role'] == 'wool-room')
    # The spawn marker rides the true spawn point; the wool marker the centre of the declared room. Both
    # offsets have to share a parity — the pad is square — so both are put on cell centres.
    spawn_at = [spawn[0] - spawn_piece['rect'][0], spawn[1] - spawn_piece['rect'][1]]
    spawn_at = [math.floor(spawn_at[0]) + 0.5, math.floor(spawn_at[1]) + 0.5]
    wool_at = [(room[0] + room[2]) / 2 - origin[0] - room_piece['rect'][0],
               (room[1] + room[3]) / 2 - origin[1] - room_piece['rect'][1]]
    wool_at = [math.floor(wool_at[0]) + 0.5, math.floor(wool_at[1]) + 0.5]

    return {
        'plan': 1,
        'meta': {'name': f'{board.capitalize()} (reconstruction)'},
        'globals': {'cell': 1, 'symmetry': 'rot_90', 'maxPlayers': 32,
                    'surface': ground, 'headroom': max(6, unit['maxbuild'] - ground),
                    'observerY': unit['maxbuild'] + 20},
        'pieces': moved_pieces,
        'zones': zones,
        'placements': {
            'spawns': [{'id': 'spawn-1', 'piece': spawn_piece['id'], 'at': spawn_at, 'facing': 'front'}],
            'wools': [{'id': 'wool-1', 'piece': room_piece['id'], 'at': wool_at}],
            'iron': [], 'destroyables': [], 'cores': [],
        },
        'walls': [], 'boxes': [],
    }


# ── the sketch ───────────────────────────────────────────────────────────────────────────────────
def soften(poly, amplitude=0.14, cap=4.0, min_edge=8.0):
    """Take the corners off a Douglas-Peucker outline without moving it. The traced polygon is already the
    right shape — this only rounds it, so the amplitude is a fraction of what an invented coast gets and the
    bulge is capped at four blocks. The corner rule still holds: a handle runs along the edge it leaves and
    never past its far end, so a bow is a corner rather than a loop, and the result is checked for
    self-intersection per polygon rather than assumed."""
    bulges = []
    for i in range(len(poly)):
        j = (i + 1) % len(poly)
        (x1, z1), (x2, z2) = poly[i], poly[j]
        length = math.hypot(x2 - x1, z2 - z1)
        if length < min_edge:
            bulges.append(0.0)
            continue
        wobble = ((hash((tuple(poly[i]), i)) >> 3) % 200) / 100.0 - 1.0
        bulges.append(round(max(-cap, min(cap, length * amplitude * wobble)), 2))
    if not any(bulges):
        return None
    controls, _ = controls_for(poly, bulges)
    return None if self_intersections(flatten(poly, controls)) else controls


def lay_polygons(layout, unit, origin, ground, spec):
    """Replace the compiler's rectangle cover with the traced outlines. The role shapes — the spawn rooms
    and the wool cages — are left exactly as compiled: they are the objectives, not the land."""
    shapes = layout['layout']['shapes']
    roles = [s for s in shapes if s.get('role')]
    land, groups = [], {'team': [], 'neutral': []}
    index = 0

    def add(island, group, theme):
        nonlocal index
        verts = [moved(v, origin) for v in island['vertices']]
        shape = {'id': f't{index}', 'type': 'polygon', 'operation': 'add', 'vertices': verts,
                 'base_height': ground, 'relief_scope': 'hold', 'theme': theme}
        controls = soften(verts, **spec.get('soften', {}))
        if controls:
            shape['controls'] = controls
        land.append(shape)
        groups[group].append(shape['id'])
        index += 1
        for hole in island['holes']:
            shape = {'id': f't{index}', 'type': 'polygon', 'operation': 'subtract',
                     'vertices': [moved(v, origin) for v in hole]}
            land.append(shape)
            groups[group].append(shape['id'])
            index += 1

    by_theme = spec['themeByRank']
    for rank, island in enumerate(unit['unit']):
        add(island, 'team', by_theme[min(rank, len(by_theme) - 1)])
    for island in unit['axis']:
        add(island, 'neutral', spec['axisTheme'])

    layout['layout']['shapes'] = land + roles
    layout['layout']['islands'] = [
        {'id': 'neutral', 'name': 'Neutral', 'mirrors': False, 'shapeIds': groups['neutral']},
        {'id': 'team', 'name': 'Team island', 'mirrors': True, 'shapeIds': groups['team']},
    ]
    return len(land)


# ── the dressing ─────────────────────────────────────────────────────────────────────────────────
# Placed from the traced geometry rather than by hand: a road that walks the island from the spawn to the
# wool room, houses on ground that is provably well inside the coast, and scrub over what is left. Hand
# coordinates were what made the first attempt at this series wrong — they described a board I had drawn
# rather than the one on disk — so nothing here is typed in.
def interior(island, origin, inset):
    """The island's cells that lie at least `inset` blocks from its coast, as a set, plus its bounds."""
    from plan_from_unit import inside as pin
    verts = [moved(v, origin) for v in island['vertices']]
    holes = [[moved(v, origin) for v in h] for h in island['holes']]
    xs = [v[0] for v in verts]; zs = [v[1] for v in verts]
    x0, x1, z0, z1 = int(min(xs)), int(max(xs)), int(min(zs)), int(max(zs))
    land = {(x, z) for z in range(z0, z1) for x in range(x0, x1)
            if pin(verts, x + 0.5, z + 0.5) and not any(pin(h, x + 0.5, z + 0.5) for h in holes)}
    for _ in range(inset):
        land = {c for c in land
                if all((c[0] + dx, c[1] + dz) in land for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    return land


def walk(land, start, goal, step=6):
    """A road, as the shortest path across the island's own cells, thinned to a polyline. Breadth-first, so
    it goes round a bay instead of through it — which is the whole reason not to draw a straight line."""
    if start not in land or goal not in land:
        start = min(land, key=lambda c: (c[0] - start[0]) ** 2 + (c[1] - start[1]) ** 2)
        goal = min(land, key=lambda c: (c[0] - goal[0]) ** 2 + (c[1] - goal[1]) ** 2)
    seen = {start: None}
    queue = [start]
    while queue:
        cell = queue.pop(0)
        if cell == goal:
            break
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cell[0] + dx, cell[1] + dz)
            if nxt in land and nxt not in seen:
                seen[nxt] = cell
                queue.append(nxt)
    if goal not in seen:
        return []
    path, cell = [], goal
    while cell is not None:
        path.append(list(cell)); cell = seen[cell]
    path.reverse()
    thinned = path[::step]
    if thinned[-1] != path[-1]:
        thinned.append(path[-1])
    return thinned


def dress(unit, origin, house):
    """Road, houses, trees, scrub — all keyed to the traced land."""
    props = []
    main = next(i for i in unit['unit'] if 'spawn' in i['carries'] or i is unit['unit'][0])
    room = unit['wool_room']
    spawn = moved(unit['spawn'], origin)
    road_land = interior(main, origin, 2)
    if road_land:
        route = walk(road_land, (int(spawn[0]), int(spawn[1])),
                     (int((room[0] + room[2]) / 2) - origin[0], int((room[1] + room[3]) / 2) - origin[1]))
        if len(route) > 2:
            props.append({'kind': 'stroke', 'id': 'island-road', 'seed': 11, 'radius': 3,
                          'style': 'worn', 'coverage': 0.8, 'points': route,
                          'pave': {'kind': 'voronoi', 'seed': 21, 'cellSize': 4, 'bands': [
                              {'material': {'kind': 'solid', 'id': 24, 'data': 1}, 'depth': 1},
                              {'material': {'kind': 'solid', 'id': 24, 'data': 2}, 'depth': 2}]}})

    # Houses go on ground eight blocks clear of every coast, spaced apart, and never on the road.
    on_road = {tuple(p) for p in (props[0]['points'] if props else [])}
    seat = 0
    for island in unit['unit']:
        pad = interior(island, origin, 5)
        placed = []
        for cell in sorted(pad):
            if any(abs(cell[0] - p[0]) < 30 and abs(cell[1] - p[1]) < 30 for p in placed):
                continue
            if any(abs(cell[0] - r[0]) < 8 and abs(cell[1] - r[1]) < 8 for r in on_road):
                continue
            if not all((cell[0] + dx, cell[1] + dz) in pad for dx in range(7) for dz in range(7)):
                continue
            placed.append(cell)
            props.append({'kind': 'house', 'id': f'house-{seat}', 'seed': 81 + seat, 'front': 'PosZ',
                          'style': house, 'wings': [[[cell[0], cell[1]], [cell[0] + 7, cell[1] + 7]]]})
            seat += 1
            if len(placed) >= 1:
                break

    # Scrub over each island's own inset area, and one acacia per house.
    for n, island in enumerate(unit['unit']):
        pad = interior(island, origin, 4)
        if len(pad) < 200:
            continue
        xs = [c[0] for c in pad]; zs = [c[1] for c in pad]
        props.append({'kind': 'flora', 'id': f'scrub-{n}', 'seed': 61 + n,
                      'points': [[min(xs), min(zs)], [max(xs), min(zs)], [max(xs), max(zs)], [min(xs), max(zs)]],
                      'spec': {'coverage': 0.22, 'scale': 9, 'octaves': 2, 'fernShare': 0.06,
                               'flowerShare': 0.04, 'flowerScale': 14, 'tallShare': 0.02}})
    for n, prop in enumerate([p for p in props if p['kind'] == 'house']):
        corner = prop['wings'][0][0]
        props.append({'kind': 'tree', 'id': f'acacia-{n}', 'seed': 31 + n,
                      'x': corner[0] - 5, 'z': corner[1] + 4,
                      'form': 'template', 'species': 'acacia', 'height': 8})
    return {'props': props}


def main():
    board = sys.argv[1]
    unit = json.load(open(f'{HERE}/{board}.unit.json'))
    pieces = json.load(open(f'{HERE}/{board}.pieces.json'))
    themes = json.load(open(f'{HERE}/themes.json'))
    themes.pop('_', None)
    spec = json.load(open(f'{HERE}/{board}.sketch.json'))
    house = desert_brick()
    origin = origin_of(unit['centre'])
    ground = GROUND[board]

    print(f'== {board}: unit of team {unit["team"]}, centre {unit["centre"]} → plan origin {origin}')
    plan = assemble_plan(board, unit, pieces, origin)
    json.dump(plan, open(f'{HERE}/{board}.plan.json', 'w'), indent=1)

    st, ev = call('POST', '/plan/evaluate', plan)
    print(f'  score {ev.get("score")}  valid {ev.get("valid")}'
          + ''.join(f'\n    {v.get("ruleId")} {v.get("termId")}: {v.get("message","")[:110]}'
                    for v in ev.get('violations', [])))
    st, r = call('POST', '/plan', {'name': plan['meta']['name']})
    slug = r['slug']
    call('PUT', f'/map/{slug}/plan', plan)
    st, c = call('POST', '/plan/compile', plan)
    if st != 200:
        print(json.dumps(c, indent=1)[:1500]); sys.exit(1)
    print(f'  warnings: {c.get("warnings")}')
    layout, intent = c['layout'], c['intent']

    laid = lay_polygons(layout, unit, origin, ground, spec)
    print(f'  laid {laid} traced shape(s) over {len(pieces)} plan rectangles')

    dressing = dress(unit, origin, house)
    print('  dressing: ' + ', '.join(f'{k}×{sum(1 for p in dressing["props"] if p["kind"] == k)}'
                                     for k in ('path', 'house', 'tree', 'flora')))
    layout['themes'] = themes
    layout['mapTheme'] = spec.get('mapTheme', 'dune')
    layout['relief'] = {'team': spec['relief']}
    layout['roomStyles'] = {'cage': house, 'spawn': house}
    layout['dressing'] = dressing
    json.dump(layout, open(f'{OUT}/{board}.layout.json', 'w'), indent=1)
    json.dump(intent, open(f'{OUT}/{board}.intent.json', 'w'), indent=1)

    call('PUT', f'/map/{slug}/sketch/from-plan?force=true', layout)
    st, _ = call('POST', f'/map/{slug}/sketch/finish')
    if st != 200:
        sys.exit(1)
    call('PUT', f'/map/{slug}/intent/from-plan', intent)
    try:
        with urllib.request.urlopen(f'{API}/map/{slug}/export', timeout=2400) as resp:
            open(f'{OUT}/{slug}.zip', 'wb').write(resp.read())
        print(f'  GET   /map/{slug}/export -> 200')
    except urllib.error.HTTPError as e:
        print(f'  GET   /map/{slug}/export -> {e.code}  {e.read().decode()[:600]}')
    print(f'SLUG {slug}')


main()
