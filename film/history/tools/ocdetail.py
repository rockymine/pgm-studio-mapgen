import csv, json, os, sys, time, urllib.request
src, D = sys.argv[1], sys.argv[2]
for x in csv.DictReader(open(src, encoding='utf-8')):
    f = os.path.join(D, x['match_id'] + '.json')
    if os.path.exists(f): continue
    for a in range(5):
        try:
            req = urllib.request.Request('https://api.oc.tc/api/v2/matches/' + x['match_id'], headers={'User-Agent': 'history-research'})
            d = json.load(urllib.request.urlopen(req, timeout=60)); break
        except Exception as e:
            print('retry', x['match_id'], e, flush=True); time.sleep(5 * (a + 1))
    json.dump(d, open(f, 'w', encoding='utf-8')); time.sleep(0.6)
print('done')
