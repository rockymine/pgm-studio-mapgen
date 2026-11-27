#!/usr/bin/env python3
# Write the shooting script, the dub sheet and the receipts from the timeline.
import json, csv, os
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = '/home/user/mappies-sketch/'
tl = json.load(open(ROOT + '/timeline.json')); info = json.load(open(ROOT + '/filminfo.json'))
t0 = {s['id']: s['t0'] for s in info['shots']}; dur = {s['id']: s['dur'] for s in info['shots']}
def tc(t): return f'{int(t // 60)}:{t % 60:04.1f}'
SHOTS = [
 ('s01', 'COLD OPEN — a build server, black and white', 'Millrace (the hand-finished world)', 'Sad piano. DALE stands on a bridge under a statue he clearly spent weeks on. Chat: "[Map Review] dale_ctw_final_v7 — Result: REJECTED, reason: low quality". A red REJECTED stamp slams on. A player sprints past behind him without looking.'),
 ('s02', 'THE PRODUCT — infomercial studio', 'built set', 'Colour slams in. THE PITCHMAN on a gold podium. Logo slam and confetti on "Prompt-a-Map!". THE MACHINE (an orange robot) pops up and waves. Bursts: NO WORLDEDIT! NO XML! NO TASTE REQUIRED! Dale walks in.'),
 ('s03', 'THE PROMPT — a screen', 'UI', 'Dale types: "make me a ctw map. 2 teams. pretty. no bugs pls". Enter.'),
 ('s04', 'THE MACHINE ROOM', 'built set', 'Dolly down a hall of lamps and bookshelves toward the Machine\'s face. The log scrolls (every line is a real finding): reusing the capture-the-wool layout for everything · monument placed where the wool was · core placed two cells along · houses: 12, designs: 1 · leaves on this map: 17,629 · leaves on the next map: 173 · placing trees inside houses · WARNING: monument floats, every map is unwinnable · withdrawn: it floats on purpose · teams: 0, spawns: 0, objectives: 0 · verified working. Green stamp: VERIFIED WORKING.'),
 ('s05', 'FIFTEEN MAPS', 'built set + real thumbnails', 'The Machine fires out fifteen map cards: the real first fifteen (fourteen worlds survive; the fifteenth card reads WORLD NOT FOUND). Counter: 15 MAPS.'),
 ('s10', 'FEATURE 1 — AN ENTIRE VILLAGE', 'Ridgeway, August 2026', 'Aerial: 12 buildings, 1 design. On the lawn two players point at one house, then the next, then notice.'),
 ('s11', '…with nothing in it', 'Ridgeway, the blue spawn', 'Inside the spawn barn: 256 blocks of floor, three blocks of furniture.'),
 ('s12', 'FEATURE 2 — INDOOR GARDENING', 'Ridgeway', 'A birch grows through the porch roof in front of the door, in one of the porch\'s two gaps. Cut inside the next house: a birch in the living room, and the Kid loves it.'),
 ('s13', 'FEATURE 3 — THE EXPRESS EXIT', 'Quatrefoil, September 2026 (yellow spawn)', 'Side-on to the spawn door: one block of kerb, then the drop. Players walk out and fall one after another; chat fills with "fell out of the world". One stops on the kerb; the Kid barges through and takes them both off. The last one stays in the doorway.'),
 ('s14', 'FEATURE 4 — OBJECTIVES WITH A VIEW', 'Goldhollow, August 2026', 'Two players at the edge of the land look for the core. It hangs in the air seven blocks off the coast. Insert: aerial with THE MAP and THE CORE labelled. The Machine pops up to explain.'),
 ('s15', 'FEATURE 5 — EXTENDED PLAY', 'Scarrow Delph, September 2026', 'The attacker mines the obsidian monument; the block drops; the defender picks it up and puts it back. Then fast: break, place, break, place, the match clock running to 3:47, day and night passing.'),
 ('s16', 'FEATURE 6 — BRIDGING', 'Gypsum Reach, September 2026', 'A player tries to bridge from the coast: "You may not build here", three times. The build zone lights up — eight blocks out, over the void.'),
 ('s20', 'BUT WAIT — studio', 'built set', 'BUT WAIT! burst. The Machine raises a hand; green VERIFIED WORKING stamp.'),
 ('s21', 'THE VERIFIED MAP', 'Haiku R2 CTW Mid, August 2026', 'The whole world: three grass slabs in the sky. Its entire 243-byte map.xml on a card. Dale turns around looking for anything.'),
 ('s30', 'THE TWIST — on Millrace as the studio built it', 'Millrace (AI world)', 'Dale walks up to the Machine and takes the WorldEdit wand off it.'),
 ('s31', 'FIVE HOURS LATER', 'Millrace: studio world wiped to the hand-finished one, same cameras', 'Three matching cameras, each wiped from the AI build to the hand-finished build: the plank raft becomes a steam tug, the bare islands get a balloon and statues, the hut becomes a wizard. Caption counts 0:00 to 5:00 of WorldEdit. Logo and tagline.'),
 ('s40', 'LEGAL', 'card', 'Blue card, logo, NOT ELIGIBLE stamp, fine print lighting up line by line.'),
 ('s50', 'BACK TO THE SHOW — awards stage', 'built set', 'The HOST, in front of a gold trophy, glances off at whatever that was. Title card: THE MAPPIES.'),
]
md = ['# Prompt-a-Map™ — shooting script', '', f'Running time {tc(info["total"])}. Timecodes are from the rendered cut; the voice lines are a synthetic scratch track meant to be replaced.', '']
for sid, title, where, action in SHOTS:
    md += [f'## {title}', f'`{tc(t0[sid])} – {tc(t0[sid] + dur[sid])}` · {where}', '', action, '']
    for lid, l in tl['lines'].items():
        if l['shot'] == sid: md.append(f'- `{tc(t0[sid] + l["t0"])}` **{l["name"].upper()}** — {l["text"]}')
    md.append('')
open(OUT + 'script.md', 'w').write('\n'.join(md))
with open(OUT + 'dub-sheet.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['line', 'start', 'end', 'seconds', 'character', 'text'])
    for lid, l in sorted(tl['lines'].items(), key=lambda kv: t0[kv[1]['shot']] + kv[1]['t0']):
        a = t0[l['shot']] + l['t0']; b = t0[l['shot']] + l['t1']; w.writerow([lid, tc(a), tc(b), round(b - a, 2), l['name'], l['text']])
print(open(OUT + 'script.md').read()[:600])
