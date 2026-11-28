import json, sys, time, urllib.request, os
D = sys.argv[1]
def page(p, size=100):
    f = os.path.join(D, f"p{size}_{p:05d}.json")
    if os.path.exists(f): return json.load(open(f, encoding="utf-8"))
    req = urllib.request.Request(f"https://api.oc.tc/api/v2/matches/?page={p}&size={size}", headers={"User-Agent": "history-research"})
    d = json.load(urllib.request.urlopen(req, timeout=60)); time.sleep(0.5)
    json.dump(d, open(f, "w", encoding="utf-8")); return d
target = sys.argv[2]  # ISO
lo, hi = 1, 2000
while lo < hi:
    mid = (lo + hi) // 2; d = page(mid)
    t = (d[-1]["startedAt"] or d[-1]["createdAt"]) if d else ""
    print(mid, (d[0]["startedAt"] or d[0]["createdAt"]) if d else None, t, flush=True)
    if d and t > target: lo = mid + 1
    else: hi = mid
print("page", lo)
