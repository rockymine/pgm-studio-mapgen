#!/usr/bin/env python3
"""Coldharbour v2 — plan to exported world, with the sketch work a plan cannot state.

The plan states the board. This attaches, onto the compiled layout: three terrain themes assigned by the
height each fused shape stands at; Bezier controls on the coasts only; per-vertex anchor heights that
shelve the two frontline tips into the mid; a relief that leaves the hub free and pins everything else;
the two room shells; and the dressing.
"""
import json, sys, urllib.request, urllib.error

API = 'http://localhost:5189/api'
HERE = '/tmp/claude-0/-home-user/90385ead-9b04-5309-9f26-9268d4a8ba5e/scratchpad/v2'

# A fused shape's only handle is the height it stands at. The contested ground — the neutral stone and the
# two frontline tips — is bare scoured rock; the wool runs are the wooded flanks; everything else is turf.
THEME_BY_HEIGHT = {10: 'chalk-yard', 12: 'chalk-yard', 16: 'chalk-hanger'}
MAP_THEME = 'chalk-down'
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


def main():
    plan = json.load(open(f'{HERE}/coldharbour_v2.plan.json'))
    themes = json.load(open(f'{HERE}/themes.json'))
    rooms = json.load(open(f'{HERE}/room-styles.json'))
    relief = json.load(open(f'{HERE}/relief.json'))
    dressing = json.load(open(f'{HERE}/dressing.json'))
    curves = json.load(open(f'{HERE}/curves.json'))
    slopes = json.load(open(f'{HERE}/slopes.json'))
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
        if sid in curves:
            shape['controls'] = curves[sid]; curved += 1
        if sid in slopes and len(slopes[sid]) == len(shape.get('vertices') or []):
            shape['anchor_heights'] = slopes[sid]; tilted += 1
        painted[shape.get('theme', MAP_THEME)] = painted.get(shape.get('theme', MAP_THEME), 0) + 1
    print(f'  themes {painted} | hold {held} | curved {curved} | tilted {tilted}')

    layout['themes'] = themes
    layout['mapTheme'] = MAP_THEME
    layout['relief'] = {'team': relief}
    layout['roomStyles'] = {'cage': rooms['cage'], 'spawn': rooms['spawn']}
    layout['dressing'] = dressing
    json.dump(layout, open(f'{HERE}/coldharbour_v2.layout.json', 'w'), indent=1)
    json.dump(intent, open(f'{HERE}/coldharbour_v2.intent.json', 'w'), indent=1)

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
