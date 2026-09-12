#!/usr/bin/env python3
"""Coldharbour — plan to exported world.

Every call is logged with its status. The plan, the themes, the room styles, the relief and the dressing
are all hand-authored JSON files beside this script; this only assembles them onto the compiled layout and
posts the chain, because the assembly is data-joining a shell cannot do cleanly.
"""
import json, sys, urllib.request, urllib.error

API = 'http://localhost:5189/api'
HERE = '/tmp/claude-0/-home-user/90385ead-9b04-5309-9f26-9268d4a8ba5e/scratchpad/authoring'


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data, {'Content-Type': 'application/json'}, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=1800)
        text = r.read().decode()
        print(f'  {method:5} {path:42} -> {r.status}')
        return r.status, (json.loads(text) if text else {})
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        print(f'  {method:5} {path:42} -> {e.code}  {text[:400]}')
        try:
            return e.code, json.loads(text)
        except Exception:
            return e.code, text


# The theme a fused shape takes. A compile fuses abutting pieces of equal height into one shape, so the
# only handle a compiled shape offers is the height it stands at — which is why the holloway was dropped to
# 10 in the plan: to have a shape of its own to paint.
THEME_BY_HEIGHT = {10: 'chalk-yard', 18: 'chalk-hanger'}
MAP_THEME = 'chalk-down'

# Which shapes keep their own top when the relief solves. The played surfaces are pinned; the two open
# bands (the frontline at 12 and the downland at 18) are left to the field so they roll.
HOLD_HEIGHTS = {10, 14, 16, 20}


def main():
    plan = json.load(open(f'{HERE}/coldharbour.plan.json'))
    themes = json.load(open(f'{HERE}/themes.json'))
    rooms = json.load(open(f'{HERE}/room-styles.json'))
    relief = json.load(open(f'{HERE}/relief.json'))
    dressing = json.load(open(f'{HERE}/dressing.json'))

    # every house wears the cage shell, so the yard byre and the wool cage are one building language
    for prop in dressing['props']:
        if prop['kind'] == 'house':
            prop['style'] = rooms['cage']

    print('== originate and store')
    st, r = call('POST', '/plan', {'name': plan['meta']['name']})
    slug = r['slug']
    print(f'  slug = {slug}')
    call('PUT', f'/map/{slug}/plan', plan)
    call('GET', f'/map/{slug}/layers')

    print('== compile')
    st, c = call('POST', '/plan/compile', plan)
    if st != 200:
        print(json.dumps(c, indent=1)[:1200]); sys.exit(1)
    print(f'  warnings: {c.get("warnings")}')
    layout, intent = c['layout'], c['intent']

    print('== the finish a plan cannot state')
    layout['themes'] = themes
    layout['mapTheme'] = MAP_THEME
    painted, held = {}, 0
    for shape in layout['layout']['shapes']:
        if shape.get('role'):
            continue                                    # structural annotation, not terrain
        height = shape.get('base_height')
        if height in THEME_BY_HEIGHT:
            shape['theme'] = THEME_BY_HEIGHT[height]
        if height in HOLD_HEIGHTS:
            shape['relief_scope'] = 'hold'
            held += 1
        painted[shape.get('theme', MAP_THEME)] = painted.get(shape.get('theme', MAP_THEME), 0) + 1
    print(f'  shapes per theme: {painted}; relief_scope=hold on {held}')
    layout['relief'] = {'team': relief}
    layout['roomStyles'] = {'cage': rooms['cage'], 'spawn': rooms['spawn']}
    layout['dressing'] = dressing
    json.dump(layout, open(f'{HERE}/coldharbour.layout.json', 'w'), indent=1)
    json.dump(intent, open(f'{HERE}/coldharbour.intent.json', 'w'), indent=1)

    print('== build')
    call('PUT', f'/map/{slug}/sketch/from-plan?force=true', layout)
    st, _ = call('POST', f'/map/{slug}/sketch/finish')
    if st != 200:
        sys.exit(1)
    call('PUT', f'/map/{slug}/intent/from-plan', intent)

    print('== export')
    try:
        with urllib.request.urlopen(f'{API}/map/{slug}/export', timeout=1800) as resp:
            open(f'{HERE}/{slug}.zip', 'wb').write(resp.read())
        print(f'  GET   /map/{slug}/export -> 200')
    except urllib.error.HTTPError as e:
        print(f'  GET   /map/{slug}/export -> {e.code}  {e.read().decode()[:500]}')
    print(f'SLUG {slug}')


main()
