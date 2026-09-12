"""Load this board onto a studio under a slug of the run's own.

    BASE=http://localhost:7894 SLUG=probe-run-1 python3 load.py

A run writes to its own copy and never to the board it was copied from. `BASE` is whichever server the run
is against, so the same file serves a local studio and one in a container.
"""
import json, os, pathlib, urllib.request

here = pathlib.Path(__file__).parent
base = os.environ.get("BASE", "http://localhost:7894").rstrip("/")
slug = os.environ.get("SLUG", "probe-run-1")

docs = {kind: json.loads((here / f"rockymine-probe.{kind}.json").read_text())
        for kind in ("layout", "intent", "plan")}
docs["slug"] = slug
docs["name"] = f"Colour probe — {slug}"

request = urllib.request.Request(f"{base}/api/map/from-documents", json.dumps(docs).encode(),
                                 {"Content-Type": "application/json"})
answer = json.loads(urllib.request.urlopen(request).read().decode())
print(f"{answer['slug']}  cells {answer['cells']}  islands {answer['islands']}")
print("warnings: " + (", ".join(w["rule"] for w in answer.get("warnings") or []) or "none"))
print(f"  {base}/maps/{answer['slug']}/sketch")
