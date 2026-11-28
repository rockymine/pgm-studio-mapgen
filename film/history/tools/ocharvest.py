import json, sys, time, urllib.request, os
D = sys.argv[1]; a, b = int(sys.argv[2]), int(sys.argv[3])
for p in range(a, b + 1):
    f = os.path.join(D, f"p100_{p:05d}.json")
    if os.path.exists(f): continue
    for attempt in range(5):
        try:
            req = urllib.request.Request(f"https://api.oc.tc/api/v2/matches/?page={p}&size=100", headers={"User-Agent": "history-research"})
            d = json.load(urllib.request.urlopen(req, timeout=90)); break
        except Exception as e:
            print("retry", p, e, flush=True); time.sleep(5 * (attempt + 1))
    json.dump(d, open(f, "w", encoding="utf-8"))
    print(p, (d[-1]["startedAt"] or d[-1]["createdAt"]) if d else None, flush=True)
    time.sleep(0.7)
