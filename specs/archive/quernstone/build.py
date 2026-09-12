#!/usr/bin/env python3
"""Coldharbour v2 — plan to exported world, with the sketch work a plan cannot state.

The plan states the board. This attaches, onto the compiled layout: three terrain themes assigned by the
height each fused shape stands at; Bezier controls on the coasts only; per-vertex anchor heights that
shelve the two frontline tips into the mid; a relief that leaves the hub free and pins everything else;
the two room shells; and the dressing.
"""
import json, math, sys, urllib.request, urllib.error
sys.path.insert(0, '/tmp/claude-0/-home-user/90385ead-9b04-5309-9f26-9268d4a8ba5e/scratchpad/v3')
from curves import controls_for, flatten, self_intersections, outward_normal, _inside

API = 'http://localhost:5189/api'
HERE = '/tmp/claude-0/-home-user/90385ead-9b04-5309-9f26-9268d4a8ba5e/scratchpad/v3'

# A fused shape's only handle is the height it stands at. The contested ground — the neutral stone and the
# two frontline tips — is bare scoured rock; the wool runs are the wooded flanks; everything else is turf.
THEME_BY_HEIGHT = {10: 'grit', 12: 'grit', 16: 'hag'}
MAP_THEME = 'moor'
FREE_HEIGHTS = {14}          # the hub takes the relief; every other surface is pinned


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data, {'Content-Type': 'application/json'}, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=1800)
        text = r.read().decode()
        print(f'  {method:5} {path:44} -> {r.status}')
        return r.status, (json.loads(text) if text else {})
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        print(f'  {method:5} {path:44} -> {e.code}  {text[:400]}')
        try:
            return e.code, json.loads(text)
        except Exception:
            return e.code, text


# ── the organic pass ─────────────────────────────────────────────────────────────────────────────
# Only the coasts are bowed. An edge that another shape stands against is a seam a player walks, and a
# curved seam is a gap; those are left dead straight. Amplitude differs west of the axis from east, so the
# two wool approaches are not the same walk mirrored.
def _seam(edge_mid, normal, others):
    probe = (edge_mid[0] + normal[0] * 3, edge_mid[1] + normal[1] * 3)
    return any(_inside(p, *probe) for p in others)


def wall_rects(plan):
    """The stamped walls, from the plan's own inspect feed. A wall spans a seam whose width was fixed at
    compile; bowing the coast beside it widens the lane past the wall's ends and hands players a way round
    — which is exactly what happened on the first organic pass (ground at x37 and x56 either side of a wall
    running x40..55). So the edges near one are left straight."""
    st, feed = call('POST', '/plan/inspect', plan)
    return [(s['minX'], s['minZ'], s['maxX'], s['maxZ'])
            for s in (feed.get('structures') or []) if s.get('kind') == 'wall']


def _near_wall(mid, walls, margin=10.0):
    return any(w[0] - margin <= mid[0] <= w[2] + margin and w[1] - margin <= mid[1] <= w[3] + margin
               for w in walls)


def bow_the_coasts(layout, walls, min_edge=12.0):
    shapes = [s for s in layout['layout']['shapes']
              if not s.get('role') and s.get('operation') != 'subtract' and s.get('vertices')]
    polys = {s['id']: [[v[0], v[1]] for v in s['vertices']] for s in shapes}
    curved = 0
    for shape in shapes:
        sid = shape['id']
        poly = polys[sid]
        others = [p for i, p in polys.items() if i != sid]
        bulges = []
        for i in range(len(poly)):
            j = (i + 1) % len(poly)
            (x1, z1), (x2, z2) = poly[i], poly[j]
            length = math.hypot(x2 - x1, z2 - z1)
            n = outward_normal(poly, i, j)
            mid = ((x1 + x2) / 2, (z1 + z2) / 2)
            if length < min_edge or _seam(mid, n, others) or _near_wall(mid, walls):
                bulges.append(0.0); continue
            # deterministic, varied, and asymmetric about the axis: the west coast is eroded softer than
            # the east, so the two approaches read differently without either being unfair.
            wobble = ((hash((sid, i)) >> 3) % 100) / 100.0
            amplitude = (0.16 if mid[0] < 0 else 0.10) + 0.09 * wobble
            bulges.append(round(min(length * amplitude, 7.0), 2))
        if not any(bulges):
            continue
        controls, clamped = controls_for(poly, bulges)
        hits = self_intersections(flatten(poly, controls))
        if hits:
            print(f'    !! {sid} would self-intersect at {hits[:3]} — left straight')
            continue
        shape['controls'] = controls
        curved += 1
        print(f'    {sid}: {sum(1 for b in bulges if b)} of {len(bulges)} edges bowed'
              + (f', {len(clamped)} clamped' if clamped else '') + ', 0 self-intersections')
    return curved


def main():
    plan = json.load(open(f'{HERE}/quernstone.plan.json'))
    themes = json.load(open(f'{HERE}/themes.json'))
    rooms = json.load(open(f'{HERE}/room-styles.json'))
    relief = json.load(open(f'{HERE}/relief.json'))
    dressing = json.load(open(f'{HERE}/dressing.json'))
    slopes = {}          # the two frontline tips are tilted below, by shape height rather than by id
    for prop in dressing['props']:
        if prop['kind'] == 'house':
            prop['style'] = rooms['cage']

    print('== originate, store, compile')
    st, r = call('POST', '/plan', {'name': plan['meta']['name']})
    slug = r['slug']
    call('PUT', f'/map/{slug}/plan', plan)
    st, c = call('POST', '/plan/compile', plan)
    if st != 200:
        print(json.dumps(c, indent=1)[:1000]); sys.exit(1)
    print(f'  warnings: {c.get("warnings")}')
    layout, intent = c['layout'], c['intent']

    print('== the sketch work')
    painted, held, curved, tilted = {}, 0, 0, 0
    for shape in layout['layout']['shapes']:
        if shape.get('role'):
            continue
        sid, height = shape['id'], shape.get('base_height')
        if height in THEME_BY_HEIGHT:
            shape['theme'] = THEME_BY_HEIGHT[height]
        if shape.get('operation') != 'subtract' and height not in FREE_HEIGHTS:
            shape['relief_scope'] = 'hold'; held += 1
        # a frontline tip shelves from its hub edge down to its mid edge: the two lowest-z vertices take
        # 10 and the two highest 12, found by z rather than by a hand-written id list.
        if height == 12 and len(shape.get('vertices') or []) == 4:
            zs = [v[1] for v in shape['vertices']]
            mid_z = (min(zs) + max(zs)) / 2
            shape['anchor_heights'] = [10 if v[1] < mid_z else 12 for v in shape['vertices']]
            tilted += 1
        painted[shape.get('theme', MAP_THEME)] = painted.get(shape.get('theme', MAP_THEME), 0) + 1
    walls = wall_rects(plan)
    print(f'  walls to keep clear of: {walls}')
    curved = bow_the_coasts(layout, walls)
    print(f'  themes {painted} | hold {held} | curved {curved} | tilted {tilted}')

    layout['themes'] = themes
    layout['mapTheme'] = MAP_THEME
    layout['relief'] = {'team': relief}
    layout['roomStyles'] = {'cage': rooms['cage'], 'spawn': rooms['spawn']}
    layout['dressing'] = dressing
    json.dump(layout, open(f'{HERE}/quernstone.layout.json', 'w'), indent=1)
    json.dump(intent, open(f'{HERE}/quernstone.intent.json', 'w'), indent=1)

    print('== build')
    call('PUT', f'/map/{slug}/sketch/from-plan?force=true', layout)
    st, _ = call('POST', f'/map/{slug}/sketch/finish')
    if st != 200:
        sys.exit(1)
    call('PUT', f'/map/{slug}/intent/from-plan', intent)
    try:
        with urllib.request.urlopen(f'{API}/map/{slug}/export', timeout=1800) as resp:
            open(f'{HERE}/{slug}.zip', 'wb').write(resp.read())
        print(f'  GET   /map/{slug}/export -> 200')
    except urllib.error.HTTPError as e:
        print(f'  GET   /map/{slug}/export -> {e.code}  {e.read().decode()[:600]}')
    print(f'SLUG {slug}')


main()
