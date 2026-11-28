#!/usr/bin/env python3
# Build the reading page from film/history. Usage: build.py  (writes out/index.html and out/img/*)
import json, os, re, html, hashlib
import markdown
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/user/pgm-studio-mapgen/film/history'
REPO = '/home/user/pgm-studio-mapgen'
OUT = HERE + '/out'
os.makedirs(OUT + '/img', exist_ok=True)
e = html.escape
files = {}


def md(text):
    h = markdown.markdown(text, extensions=['tables', 'sane_lists'])
    h = re.sub(r'<table>', '<div class="scroll"><table>', h).replace('</table>', '</table></div>')
    for word, cls in (('Record', 'rec'), ('Account', 'acc'), ('Inference', 'inf'), ('Record against it', 'rec')):
        h = h.replace(f'<strong>{word}:</strong>', f'<span class="v v-{cls}">{word}</span>')
    return h


def thumb(path, width=1100):
    """Copy a repo picture into out/img as a resized JPEG; return its published path or None."""
    full = path if path.startswith('/') else os.path.join(REPO, path)
    if not os.path.isfile(full):
        full2 = os.path.join(SRC, path)
        if not os.path.isfile(full2):
            return None
        full = full2
    name = hashlib.sha1(full.encode()).hexdigest()[:10] + '.jpg'
    dst = OUT + '/img/' + name
    if not os.path.isfile(dst):
        im = Image.open(full).convert('RGB')
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(dst, 'JPEG', quality=80, optimize=True)
    files['img/' + name] = dst
    return 'img/' + name


def tc(sec):
    return f'{int(sec) // 60}:{int(sec) % 60:02d}'


# ---------- history ----------
hist = open(SRC + '/HISTORY.md').read()
hist_title = re.match(r'# (.+)', hist).group(1)
parts = re.split(r'\n## ', hist)
intro_md = re.sub(r'^# .+\n', '', parts[0]).replace('\n---\n', '\n')
FIGS = {
    1: [('sources/early-experiments/2025-02-11-townside-grid-and-graph.png', 'Townside as a grid of blocks and as a graph of redstone torches, sent on 11 February 2025.'),
        ('sources/early-experiments/v0-prototype-2025-02/rst-gridlike-4.png', 'The first v0 prototype, "Random Spanning Tree Visualization", as it runs today.'),
        ('sources/early-experiments/aistudio-ctw-map-generator-2025/01-generator-two-teams.png', 'The AI Studio generator of late September 2025, built from the author\'s export.')],
    2: [('sources/early-experiments/2025-11-04-first-okay-layout-in-game.png', '4 November 2025: the first reasonably okay layout, drawn in the browser and imported on the mapmaker server.'),
        ('sources/early-experiments/2025-11-06-layout-editor-world-import.png', '6 November 2025: MinecraftLayoutEditor with world import.')],
    3: [('sources/early-experiments/2026-ctw-match-activity-18jan-08mar.png', 'The logged capture-the-wool matches, 18 January to 8 March 2026.'),
        ('sources/early-experiments/2026-01-simplified-skeleton-detail.png', 'Islands reduced to a skeleton graph in CTWAnalysis.')],
    5: [('sources/base-map-squared-paper-drawing.jpg', 'The squared-paper drawing behind Base 2-Island: orange for spawn, blue for wool, green for the build region.')],
    7: [('renders/wandering-u/02-whole-map.jpg', 'Wandering U, rendered from the world file.')],
    9: [('sources/slop-sunday-announcement/2026-09-27-slop-sunday-announcement.jpg', 'The announcement of 27 September 2026 in the event channel.')],
    17: [('renders/hand-built/01-whole-from-west.jpg', 'The hand-built fire-and-ice map, rendered from its blocks.'),
         ('renders/hand-built/05-facade-and-core.jpg', 'Its facade and core.')],
}
chapters = []
for p in parts[1:]:
    head, _, body = p.partition('\n')
    m = re.match(r'(\d+)\.\s*(.+)', head)
    num, title = (int(m.group(1)), m.group(2)) if m else (0, head)
    figs = ''
    for path, cap in FIGS.get(num, []):
        t = thumb('film/history/' + path)
        if t:
            figs += f'<figure><img src="{t}" alt="{e(cap)}" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>'
    if figs:
        figs = f'<div class="figs">{figs}</div>'
    chapters.append((num, title, md(body), figs, len(body.split())))
toc = ''.join(f'<li><a href="#history-{n}" data-ch="{n}"><b>{n}</b><span>{e(t)}</span></a></li>' for n, t, *_ in chapters)
hist_html = ''.join(f'<section class="chapter" id="ch-{n}"><p class="chno">Chapter {n} · about {max(1, round(w / 230))} min read</p><h2>{e(t)}</h2>{f}{b}</section>' for n, t, b, f, w in chapters)
words = sum(c[4] for c in chapters)

# ---------- timeline ----------
tl = open(SRC + '/timeline.md').read()
tl_head, _, tl_rest = tl.partition('\n|')
tl_intro = md(re.sub(r'^# .+\n', '', tl_head))
rows = [r for r in ('|' + tl_rest).split('\n') if r.startswith('|')]
cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
hdr, body_rows = cells[0], [c for c in cells[2:] if len(c) >= 4]


def inline(s):
    s = e(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s


def kind_cls(k):
    k = k.lower()
    return 'rec' if k.startswith('record') else 'acc' if 'account' in k[:20] or k.startswith('author') else 'inf' if k.startswith('inference') else 'rec'


tl_rows = ''
year = None
for c in body_rows:
    y = c[0][:4]
    if y != year and y.isdigit():
        year = y
        tl_rows += f'<tr class="yr"><td colspan="4">{y}</td></tr>'
    tl_rows += f'<tr><td class="d" data-l="Date">{inline(c[0])}</td><td data-l="Event">{inline(c[1])}</td><td class="s" data-l="Source">{inline(c[2])}</td><td class="k" data-l="Kind"><span class="v v-{kind_cls(c[3])}">{inline(c[3])}</span></td></tr>'

# ---------- outline ----------
outline_md = open(SRC + '/OUTLINE.md').read()
outline_title = re.match(r'# (.+)', outline_md).group(1) if outline_md.startswith('# ') else 'Outline'
outline_html = md(re.sub(r'^# .+\n', '', outline_md))

# ---------- questions ----------
q = open(SRC + '/interview-questions.md').read()
q_open, _, q_ans = q.partition('\n## Answered')
q_open_html = md(re.sub(r'^# .+\n', '', q_open))
q_ans_html = md('## Answered' + q_ans) if q_ans else ''

# ---------- storyboard ----------
sb_path = SRC + '/storyboard.json'
sb = json.load(open(sb_path)) if os.path.isfile(sb_path) else None
PICTO = {
    'animate': '<g transform="translate(34 62)"><rect x="6" y="0" width="16" height="16"/><rect x="4" y="18" width="20" height="24"/><rect x="-6" y="18" width="8" height="24"/><rect x="26" y="18" width="8" height="24"/><rect x="4" y="44" width="9" height="24"/><rect x="15" y="44" width="9" height="24"/></g>',
    'render': '<g transform="translate(22 78)"><polygon points="0,20 34,4 68,20 34,36"/><polygon points="0,20 34,36 34,58 0,42"/><polygon points="68,20 34,36 34,58 68,42"/></g>',
    'record': '<g transform="translate(30 66)"><rect x="0" y="6" width="44" height="32" rx="3"/><polygon points="46,16 62,8 62,36 46,28"/><circle cx="12" cy="-6" r="5" class="dot"/></g>',
    'from-pc': '<g transform="translate(26 66)"><rect x="0" y="0" width="60" height="40" rx="3"/><rect x="24" y="42" width="12" height="8"/><rect x="12" y="50" width="36" height="5"/></g>',
    'exists': '<g transform="translate(34 60)"><polygon points="0,0 34,0 46,12 46,62 0,62"/><polyline points="34,0 34,12 46,12"/><line x1="8" y1="26" x2="38" y2="26"/><line x1="8" y1="36" x2="38" y2="36"/><line x1="8" y1="46" x2="28" y2="46"/></g>',
}


def wrap(text, n=22, lines=4):
    out, cur = [], ''
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur: out.append(cur)
    if len(out) > lines:
        out = out[:lines]; out[-1] = out[-1][:n - 1] + '…'
    return out


def sketch(text, footage):
    ls = wrap(text)
    y0 = 96 - (len(ls) - 1) * 11
    t = ''.join(f'<text x="118" y="{y0 + i * 22}">{e(l)}</text>' for i, l in enumerate(ls))
    return f'<svg class="sk" viewBox="0 0 320 180" role="img" aria-label="{e(text)}"><rect class="bg" width="320" height="180"/><g class="grid">' + ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="180"/>' for x in range(20, 320, 20)) + ''.join(f'<line x1="0" y1="{y}" x2="320" y2="{y}"/>' for y in range(20, 180, 20)) + f'</g><g class="pic">{PICTO.get(footage, PICTO["exists"])}</g><g class="hand">{t}</g></svg>'


FOOT = {'exists': 'exists', 'render': 'to render', 'animate': 'to animate', 'record': 'to record', 'from-pc': 'from the PC'}
KIND = {'record': 'rec', 'author recalls': 'acc', 'inference': 'inf', 'staged': 'stg'}
sb_html = actbar = sb_facts = ''
if sb:
    total = sb['runtime_seconds']
    scenes_all = [s for a in sb['acts'] for s in a['scenes']]
    have = sum(1 for s in scenes_all if s['footage'] == 'exists')
    counts = {}
    for s in scenes_all: counts[s['footage']] = counts.get(s['footage'], 0) + 1
    actbar = '<ol class="actbar">' + ''.join(f'<li style="flex-grow:{a["dur"]}"><a href="#storyboard" data-act="{e(a["id"])}"><b>{e(a["id"])}</b><span class="t">{e(a["title"])}</span><span class="tc">{tc(a["start"])} · {tc(a["dur"])}</span></a></li>' for a in sb['acts']) + '</ol>'
    sb_facts = f'<div class="facts"><span><b>{tc(total)}</b> running time</span><span><b>{len(sb["acts"])}</b> acts</span><span><b>{len(scenes_all)}</b> scenes</span>' + ''.join(f'<span><b>{n}</b> {FOOT.get(k, k)}</span>' for k, n in sorted(counts.items(), key=lambda kv: -kv[1])) + '</div>'
    for a in sb['acts']:
        cards = ''
        for s in a['scenes']:
            img = thumb(s['frame']['image']) if s['frame'].get('image') else None
            frame = f'<img src="{img}" alt="{e(s["frame"].get("sketch", s["title"]))}" loading="lazy">' if img else sketch(s['frame'].get('sketch') or s['title'], s['footage'])
            ons = ''.join(f'<blockquote><p>{e(o["text"])}</p><cite>{e(o.get("who", ""))}{" · " + e(o["source"]) if o.get("source") else ""}</cite></blockquote>' for o in s.get('onscreen', []))
            vo = f'<p class="vo">{e(s["vo"])}</p>' if s.get('vo') else '<p class="vo none">No narration.</p>'
            todo = f'<p class="todo"><b>To do</b> {e(s["todo"])}</p>' if s.get('todo') else ''
            snd = f'<p class="snd"><b>Sound</b> {e(s["sound"])}</p>' if s.get('sound') else ''
            src = ', '.join(s.get('sources', []))
            cards += f'''<article class="scene" data-foot="{e(s["footage"])}"><div class="frame {"" if img else "is-sketch"}">{frame}<span class="chip tcchip">{tc(s["start"])} · {s["dur"]}s</span></div>
<div class="sbody"><p class="sid">{e(s["id"])} <span class="v v-{KIND.get(s["kind"], "rec")}">{e(s["kind"])}</span> <span class="foot f-{e(s["footage"])}">{FOOT.get(s["footage"], s["footage"])}</span></p>
<h4>{e(s["title"])}</h4><p class="pic">{e(s["picture"])}</p>{vo}{ons}{snd}{todo}<p class="src">{e(src)}</p></div></article>'''
        sb_html += f'<section class="act" id="act-{e(a["id"])}"><header><p class="chno">{e(a["id"])} · {tc(a["start"])}–{tc(a["start"] + a["dur"])}</p><h3>{e(a["title"])}</h3><p class="lede2">{e(a["summary"])}</p></header><div class="scenes">{cards}</div></section>'
else:
    sb_html = '<p class="lede2">The storyboard is being written.</p>'

page = open(HERE + '/page.tmpl.html').read()
rep = {
    '{{HIST_TITLE}}': e(hist_title), '{{INTRO}}': md(intro_md), '{{TOC}}': toc, '{{HISTORY}}': hist_html, '{{WORDS}}': f'{round(words, -2):,}',
    '{{READMIN}}': str(round(words / 230)), '{{NCH}}': str(len(chapters)),
    '{{TL_INTRO}}': tl_intro, '{{TL_ROWS}}': tl_rows, '{{NTL}}': str(len(body_rows)),
    '{{OUTLINE}}': outline_html, '{{OUTLINE_TITLE}}': e(outline_title),
    '{{Q_OPEN}}': q_open_html, '{{Q_ANS}}': q_ans_html,
    '{{ACTBAR}}': actbar, '{{SB_FACTS}}': sb_facts, '{{STORYBOARD}}': sb_html,
    '{{FILM_TITLE}}': e(sb['title']) if sb else 'The film', '{{LOGLINE}}': e(sb['logline']) if sb else '', '{{NARRATION}}': e(sb.get('narration', '')) if sb else '',
}
for k, v in rep.items(): page = page.replace(k, v)
left = re.findall(r'\{\{[A-Z_]+\}\}', page)
open(OUT + '/index.html', 'w').write(page)
json.dump(files, open(OUT + '/files.json', 'w'), indent=0)
print('page', len(page) // 1024, 'KB; images', len(files), 'total', sum(os.path.getsize(v) for v in files.values()) // 1024, 'KB; chapters', len(chapters), 'words', words, 'timeline rows', len(body_rows), 'unfilled', left)
