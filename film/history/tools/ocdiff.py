import json, glob, csv, collections, sys
csvp = sys.argv[1]
M = {}
for f in glob.glob('pages/p100_*.json'):
    for m in json.load(open(f, encoding='utf-8')):
        M[m['matchId']] = m
ms = sorted(M.values(), key=lambda m: m['createdAt'])
print('api matches', len(ms), ms[0]['createdAt'], ms[-1]['createdAt'])
rows = list(csv.DictReader(open(csvp, encoding='utf-8')))
ids = {r['match_id'] for r in rows}
lo, hi = '2026-05-31T14:50', '2026-11-27T18:40'
win = [m for m in ms if lo <= m['createdAt'] <= hi]
print('api in window', len(win), 'csv rows', len(rows))
print('csv ids not in api', len(ids - set(M)))
by = collections.Counter((m['serverName'], m['matchId'] in ids) for m in win)
for k, v in sorted(by.items()): print(k, v)
st = collections.Counter((m['serverName'], m['status']) for m in win if m['matchId'] not in ids)
print(st)
miss = [m for m in win if m['matchId'] not in ids and m['serverName'] in ('server-1','server-2')]
with open('missing-public.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['server','created_utc','started_utc','ended_utc','status','match_id','map','map_slug','teams','participants','winner','series'])
    for m in miss:
        n = len({p['user']['userUuid'] for t in m['teams'] for p in t.get('participations', [])}) if m['teams'] and 'participations' in m['teams'][0] else ''
        wt = m.get('winnerTeam'); wt = wt['name'] if isinstance(wt, dict) else (m.get('winnerUser') or {}).get('username', '') if isinstance(m.get('winnerUser'), dict) else ''
        w.writerow([m['serverName'], m['createdAt'], m['startedAt'], m['endedAt'], m['status'], m['matchId'], m['map']['name'], m['map']['mapSlug'], len(m['teams']), n, wt, (m['series'] or {}).get('name')])
print('server-2 missing', len(miss))
