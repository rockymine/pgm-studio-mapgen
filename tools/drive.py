#!/usr/bin/env python3
"""Drive a plan + finish document through the pgm-studio API to an exported world.

Usage: drive.py <mapdir> <slug-name> [--out <dir>] [--force]
Expects in <mapdir>: <name>.plan.json and <name>.finish.json where finish carries:
  themeByHeight:   {"9": "firn-valley", ...}      theme name per compiled tier height
  shapePropsByHeight: {"11": {"relief_scope": "exclude"}, ...}
  addShapes:       [SketchShape, ...]             authored shapes appended to the first island
  relief:          {"<islandId>": {...}} OR {"*": {...}} applied to every island
  themes:          the theme registry (first key becomes mapTheme unless mapTheme set)
  mapTheme:        explicit default theme name
  roomStyles:      {"cage": ..., "spawn": ...}
  dressing:        {"props": [...]}
  voidEnforcement: true -> patch intent.build.voidEnforcement = {exclusions: []}
"""
import json, sys, io, zipfile, urllib.request, urllib.error, os, shutil

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")

def call(method, path, body=None, raw=False):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req) as r:
            payload = r.read()
            print(f"  {method} {path}: {r.status}")
            if raw: return payload
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:600]
        raise SystemExit(f"FAIL {method} {path}: HTTP {e.code} {body}")

def main():
    mapdir, name = sys.argv[1], sys.argv[2]
    out = None
    force = "--force" in sys.argv
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    base = os.path.basename(mapdir.rstrip("/"))
    plan = json.load(open(f"{mapdir}/{base}.plan.json"))
    finish = json.load(open(f"{mapdir}/{base}.finish.json"))

    slug = call("POST", "/plan", {"name": name})["slug"]
    print(f"  slug={slug}")
    call("PUT", f"/map/{slug}/plan", plan)
    compiled = call("POST", "/plan/compile", plan)
    layout, intent = compiled["layout"], compiled["intent"]
    inner = layout["layout"]
    shapes, islands = inner["shapes"], inner["islands"]

    if tb := finish.get("themeByHeight"):
        for s in shapes:
            h = s.get("base_height")
            if s.get("role") is None and h is not None and str(int(h)) in tb:
                s["theme"] = tb[str(int(h))]
    if tid := finish.get("themeById"):
        for s in shapes:
            if s["id"] in tid: s["theme"] = tid[s["id"]]
    if props := finish.get("shapePropsByHeight"):
        for s in shapes:
            h = s.get("base_height")
            if s.get("role") is None and h is not None and str(int(h)) in props:
                s.update(props[str(int(h))])
    if pid := finish.get("shapePropsById"):
        for s in shapes:
            if s["id"] in pid: s.update(pid[s["id"]])
    if extra := finish.get("addShapes"):
        for s in extra:
            shapes.append(s)
            islands[0]["shapeIds"].append(s["id"])
        print(f"  +{len(extra)} authored shapes")
    if rel := finish.get("relief"):
        if "*" in rel:
            rel = {isl["id"]: rel["*"] for isl in islands}
        layout["relief"] = rel
    if themes := finish.get("themes"):
        layout["themes"] = themes
        layout["mapTheme"] = finish.get("mapTheme") or next(iter(themes))
    styledir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")
    def resolve(style):
        if isinstance(style, str) and style.startswith("@"):
            return json.load(open(os.path.join(styledir, style[1:] + ".json")))
        return style
    if "roomStyles" in finish:
        layout["roomStyles"] = {k: resolve(v) for k, v in finish["roomStyles"].items()}
    if "dressing" in finish:
        for prop in finish["dressing"].get("props", []):
            if prop.get("kind") == "house":
                prop["style"] = resolve(prop.get("style", {}))
        layout["dressing"] = finish["dressing"]

    q = "?force=true" if force else ""
    call("PUT", f"/map/{slug}/sketch/from-plan{q}", layout)

    # look at the ground before building it
    read = call("POST", f"/map/{slug}/sketch/relief/read", layout)
    for isl in read.get("islands", []):
        print(f"  relief/read: island={isl.get('id')} cells={isl.get('cells')} "
              f"low={isl.get('low')} high={isl.get('high')} symErr={isl.get('symmetryError')}")
    if finish.get("relief") and not read.get("islands"):
        raise SystemExit("  relief/read answered no islands - shapes are not rasterizing, stop")

    call("POST", f"/map/{slug}/sketch/finish")

    if finish.get("voidEnforcement"):
        b = intent.setdefault("build", {})
        b["voidEnforcement"] = {"exclusions": finish.get("voidExclusions", [])}
    call("PUT", f"/map/{slug}/intent/from-plan", intent)

    zip_bytes = call("GET", f"/map/{slug}/export", raw=True)
    if out:
        if os.path.isdir(out): shutil.rmtree(out)
        os.makedirs(out)
        zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(out)
        print(f"  world -> {out}")
    print(f"DONE slug={slug}")

if __name__ == "__main__":
    main()
