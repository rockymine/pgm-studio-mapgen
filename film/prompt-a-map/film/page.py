#!/usr/bin/env python3
# Build the artifact page from the film's own data. Usage: page.py <video url> <poster url>
import json, os, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(ROOT + '/timeline.json')); info = json.load(open(ROOT + '/filminfo.json')); cams = json.load(open(ROOT + '/cams.json'))
VIDEO, POSTER = (sys.argv + ['', ''])[1:3]
t0 = {s['id']: s['t0'] for s in info['shots']}; dur = {s['id']: s['dur'] for s in info['shots']}
tc = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
e = html.escape
SHOTS = [
 ('s01', 'Cold open', 'Black and white. Dale’s map is rejected for low quality. A player sprints past his statue without looking.'),
 ('s02', 'The product', 'Colour slams in. The Pitchman, the logo, the Machine, and “No taste required!”'),
 ('s03', 'The prompt', 'Dale types one line and presses Enter.'),
 ('s04', 'The machine room', 'A dolly toward the Machine’s face while its log scrolls. Every log line is a real finding.'),
 ('s05', 'Fifteen maps', 'The Machine fires out the real first fifteen. Fourteen worlds survive; the last card reads “world not found”.'),
 ('s10', 'Feature 1: an entire village', 'Twelve buildings, one design. Two players admire a house, then the next, then notice.'),
 ('s11', '…with nothing in it', 'Inside the spawn barn: 256 blocks of floor and three blocks of furniture.'),
 ('s12', 'Feature 2: indoor gardening', 'A birch through the porch in front of the door, and another growing in a living room.'),
 ('s13', 'Feature 3: the express exit', 'Players walk out of the spawn door, cross one block of kerb and drop off the world.'),
 ('s14', 'Feature 4: objectives with a view', 'The core hangs in the air seven blocks off the coast.'),
 ('s15', 'Feature 5: extended play', 'The monument’s obsidian drops when mined, so the defender puts it back. Forever.'),
 ('s16', 'Feature 6: bridging', '“You may not build here.” The build zone starts eight blocks out over the void.'),
 ('s20', 'But wait', 'The Machine tests its own maps. Verified working.'),
 ('s21', 'The verified map', 'Three grass slabs in the sky and a 243-byte map file.'),
 ('s30', 'The twist', 'Dale takes the WorldEdit wand off the Machine.'),
 ('s31', 'Five hours later', 'The studio’s Millrace wiped to the hand-finished one, on three matching cameras.'),
 ('s40', 'Legal', 'The fastest reader in the community.'),
 ('s50', 'Back to the show', 'The host, a trophy and the title card.'),
]
script = []
for sid, title, action in SHOTS:
    lines = ''.join(f'<div class="cue">{e(l["name"])}</div><p class="dlg">{e(l["text"])}</p>' for lid, l in tl['lines'].items() if l['shot'] == sid)
    script.append(f'<div class="slug">{e(title)}<span>{tc(t0[sid])}</span></div><p class="act">{e(action)}</p>{lines}')
RECEIPTS = [
 ('An entire village', 'Ridgeway', 'Aug 2026', 'All 12 buildings share one design at three sizes; the same roof recurs block for block 17 times across six of the first fifteen maps.', '“Every house is the same house… a dozen buildings of one silhouette is a barracks.”', 'review of the first fifteen, pgm-studio 56fc9d41'),
 ('…with nothing in it', 'Ridgeway', 'Aug 2026', 'The blue spawn barn’s 16×16 interior holds three blocks: bedrock, a sign and a pane of glass.', '“A house is empty. Buildings are shells with nothing inside.”', 'same review'),
 ('Indoor gardening', 'Ridgeway', 'Aug 2026', 'A birch stands in one of the porch’s two gaps at (−42, 6…18, −52), through the intact roof; another grows inside the next house.', '“Buildings stand inside buildings, trees grow inside trees, and trees grow through buildings.”', 'same review; fixed in pgm-studio 27280399'),
 ('The express exit', 'Quatrefoil', 'Sep 2026', 'Yellow’s hall has two doors. Each meets one block of kerb, then a 9-block cliff and the void.', '“…blue and green get one wall each pointing over the void, and yellow (south-east) gets both.”', 'pgm-studio d0843f0f'),
 ('Objectives with a view', 'Goldhollow', 'Aug 2026', 'A capture-the-wool layout re-used for destroy-the-core. The core sits at x 88…92 with nothing under it, 7 blocks of air from the nearest land.', '“…a shortcut that produced fifteen capture boards wearing three different hats.”', 'same review; pgm-studio e9ead0cd'),
 ('Extended play', 'Scarrow Delph', 'Sep 2026', 'As authored, the kit gave a diamond pickaxe and obsidian was not in the item-remove list, so a mined monument block could be picked up and replaced.', '“…the defending team could rebuild a monument with the obsidian the attacker’s own diamond pick had just dropped, for as long as the match ran.”', 'pgm-studio 0b3a514f'),
 ('Bridging', 'Gypsum Reach', 'Sep 2026', 'The coast was pulled back to x −25 but the build zone still began at x −16.', '“That left eight blocks of void that nobody could build across.”', 'pgm-studio-mapgen 298cc730'),
 ('Verified working', 'Haiku R2 CTW Mid', 'Aug 2026', 'Three 20×20 slabs and a 243-byte map.xml with no teams, spawns or objectives. The run report says “plan through export, verified working”.', '“A map with nothing on it satisfies every refusal the pipeline has.”', 'reports/haiku-run2.md; README at pgm-studio-mapgen ea8dc104'),
 ('“Every map is unwinnable”', 'machine-room log', 'Aug 2026', 'The AI measured a four-block gap under a floating monument and filed every destroy map as unwinnable. Goals float by design.', '“The measurement was right and the conclusion was invented.”', 'pgm-studio ccd8d7b0, withdrawn in 6eec9b8b'),
 ('17,629 leaves, then 173', 'machine-room log', 'Aug 2026', 'Tree density nobody chose.', '“…another at 173, which is a bare map with a shrub on it.”', 'same review'),
 ('Five hours later', 'Millrace', 'Sep 2026', 'The studio’s world and the hand-finished one share coordinates, so each camera is the same on both.', '“Millrace finished by hand, five hours of WorldEdit and Arceon over the studio’s world.”', 'BOARDS-BUILT.md'),
]
receipts = ''.join(f'<tr><td data-l="Gag"><b>{e(a)}</b></td><td data-l="Map">{e(b)}<br><small>{e(c)}</small></td><td data-l="What is true">{e(d)}</td><td data-l="Source"><i>{e(q)}</i><br><small>{e(s)}</small></td></tr>' for a, b, c, d, q, s in RECEIPTS)
USED = [('s01 / s30 / s31', 'mr_bridge_hand'), ('s10 aerial (start)', 'rw_wide_move'), ('s10 lawn', 'rw_ground'), ('s11', 'rw_barn'), ('s12 porch', 'rw_door_close'), ('s12 inside', 'rw_inside'),
        ('s13', 'qf_door'), ('s14 edge', 'gh_pov'), ('s14 aerial (start)', 'gh_wide_move'), ('s15', 'sc_mon'), ('s16', 'gyp_eye'), ('s21', 'hk_ground'), ('s31 boat', 'mr_boat_hand'), ('s31 aerial', 'mr_wide_hand')]
def tp(c): return f'/tp @s {c["x"]:g} {c["y"] - 1.62:.2f} {c["z"]:g} {c["yaw"]:g} {c["pitch"]:g}'
shots = ''.join(f'<tr><td data-l="Shot">{e(n)}</td><td data-l="World"><code>maps/{e(cams[k]["world"])}</code></td><td data-l="Stand here"><code>{e(tp(cams[k].get("cam") or cams[k]["from"]))}</code></td><td data-l="FOV">{(cams[k].get("cam") or cams[k]["from"]).get("fov", 70):g}°</td></tr>' for n, k in USED)
names = {}
for l in tl['lines'].values(): names.setdefault(l['name'], []).append(l)
cast = ''.join(f'<tr><td><b>{e(n)}</b></td><td>{len(ls)}</td><td>{sum(l["t1"] - l["t0"] for l in ls):.0f}</td></tr>' for n, ls in sorted(names.items(), key=lambda kv: -len(kv[1])))
video = f'<video controls playsinline preload="metadata" poster="{e(POSTER)}" src="{e(VIDEO)}"></video>' if VIDEO else '<div class="novid">The cut is attached in the chat as an MP4.</div>'
page = open(ROOT + '/page.tmpl.html').read()
for k, v in {'{{VIDEO}}': video, '{{RUNTIME}}': tc(info['total']), '{{SCRIPT}}': ''.join(script), '{{RECEIPTS}}': receipts, '{{SHOTS}}': shots, '{{CAST}}': cast, '{{NLINES}}': str(len(tl['lines']))}.items(): page = page.replace(k, v)
open(ROOT + '/../prompt-a-map.html', 'w').write(page)
print('page written', len(page))
