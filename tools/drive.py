#!/usr/bin/env python3
"""Drive a plan + finish document through the pgm-studio API to an exported world, and say what the
pipeline said on the way.

    tools/drive.py <specdir> "<Map Name>" --out <worlddir> [--force] [--dry]

<specdir> holds <base>.plan.json and <base>.finish.json, where <base> is the directory's own name.
The plan is a PlanModel. The finish carries everything a plan cannot state, keyed onto the compiled
layout:

  themeByHeight   {"11": "gyp-bench", ...}   theme per compiled shape, by the height it stands at
  themeById       {"s3": "gyp-rake"}          theme per compiled shape id (wins over the height rule)
  shapePropsByHeight {"11": {"relief_scope": "exclude"}, ...}   fields merged onto a compiled shape
  shapePropsById  {"s3": {...}}
  addShapes       [SketchShape, ...]          authored shapes appended to the first island
  relief          {"<islandId>": {...}} or {"*": {...}} applied to every island
  themes          the theme registry;  mapTheme  the map default (first key unless stated)
  roomStyles      {"cage": ..., "spawn": ...}; a "@name" string loads tools/styles/<name>.json
  dressing        {"props": [...]};  a house prop's "style" takes the same "@name"
  voidEnforcement true -> patch intent.build.voidEnforcement (voidExclusions for the rects to spare)
  authors         ["Opus 5"], or [{"name", "uuid", "role", "contribution"}] -> the <authors> block. PGM
                  takes a person as an account OR a pseudonym, so a bare name is a valid author

Nothing here computes a placement, a clearance or a validation: it posts documents and prints what
came back. Every finding the pipeline raises is printed with its rule id, including the dressing
declines, which are the ones no other route shows an agent.
"""
import json, sys, io, zipfile, urllib.request, urllib.error, os, shutil

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
STYLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")


def call(method, path, body=None, raw=False, fatal=True):
    """One request. Returns (status, payload). A non-2xx is printed with its findings and, unless
    fatal is False, stops the run — a refusal is a fault to fix, not a step to skip."""
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=1800) as response:
            payload = response.read()
            print(f"  {method:5} {path:46} {response.status}")
            if raw:
                return response.status, payload
            return response.status, (json.loads(payload) if payload else {})
    except urllib.error.HTTPError as error:
        text = error.read().decode()
        print(f"  {method:5} {path:46} {error.code}")
        try:
            body = json.loads(text)
        except Exception:
            body = text
        report(body if isinstance(body, dict) else {}, "  ")
        if isinstance(body, dict) and body.get("message"):
            print(f"    {body['message']}")
        elif not isinstance(body, dict):
            print(f"    {text[:600]}")
        if fatal:
            raise SystemExit(1)
        return error.code, body


def findings(payload):
    """Every finding shape the studio answers in, under the four keys it uses."""
    out = []
    if not isinstance(payload, dict):
        return out
    for key in ("findings", "warnings", "violations", "lint"):
        entries = payload.get(key)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            # an evaluator violation wraps the finding beside its term id and distance
            inner = entry.get("finding")
            out.append((key, inner if isinstance(inner, dict) else entry))
    return out


def report(payload, indent="  "):
    for key, entry in findings(payload):
        rule = entry.get("rule") or entry.get("id") or key
        severity = entry.get("severity") or key
        message = entry.get("message") or entry.get("detail") or json.dumps(entry)
        print(f"{indent}  [{severity:9}] {rule:8} {message}")


def resolve(style):
    """A '@name' string is tools/styles/<name>.json. Anything else is the document itself."""
    if isinstance(style, str) and style.startswith("@"):
        with open(os.path.join(STYLES, style[1:] + ".json")) as handle:
            return json.load(handle)
    return style


def patch_layout(layout, finish):
    """Everything the finish says about the compiled layout, applied in one pass."""
    inner = layout["layout"]
    shapes, islands = inner["shapes"], inner["islands"]
    by_height = finish.get("themeByHeight") or {}
    props_by_height = finish.get("shapePropsByHeight") or {}
    by_id = finish.get("themeById") or {}
    props_by_id = finish.get("shapePropsById") or {}
    for shape in shapes:
        if shape.get("role") is not None:
            continue                       # a projected spawn/wool rectangle is not terrain
        height = shape.get("base_height")
        key = None if height is None else str(int(height))
        if key in by_height:
            shape["theme"] = by_height[key]
        if key in props_by_height:
            shape.update(props_by_height[key])
        if shape["id"] in by_id:
            shape["theme"] = by_id[shape["id"]]
        if shape["id"] in props_by_id:
            shape.update(props_by_id[shape["id"]])
    for extra in finish.get("addShapes") or []:
        shapes.append(extra)
        islands[0]["shapeIds"].append(extra["id"])
    if finish.get("addShapes"):
        print(f"    +{len(finish['addShapes'])} authored shapes onto island '{islands[0]['id']}'")
    relief = finish.get("relief")
    if relief:
        if "*" in relief:
            relief = {island["id"]: relief["*"] for island in islands}
        layout["relief"] = relief
    themes = finish.get("themes")
    if themes:
        layout["themes"] = themes
        layout["mapTheme"] = finish.get("mapTheme") or next(iter(themes))
    if "roomStyles" in finish:
        layout["roomStyles"] = {k: resolve(v) for k, v in finish["roomStyles"].items()}
    if "dressing" in finish:
        for prop in finish["dressing"].get("props", []):
            if prop.get("kind") == "house":
                prop["style"] = resolve(prop.get("style", {}))
        layout["dressing"] = finish["dressing"]
    painted = {}
    for shape in shapes:
        if shape.get("role") is None:
            painted[shape.get("theme") or layout.get("mapTheme")] = \
                painted.get(shape.get("theme") or layout.get("mapTheme"), 0) + 1
    print(f"    themes on shapes: {painted}")
    return layout


def main():
    specdir, name = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    force = "--force" in sys.argv
    dry = "--dry" in sys.argv
    base = os.path.basename(specdir.rstrip("/"))
    with open(f"{specdir}/{base}.plan.json") as handle:
        plan = json.load(handle)
    with open(f"{specdir}/{base}.finish.json") as handle:
        finish = json.load(handle)

    # ── read the board before anything exists ────────────────────────────────────────────────
    print("== the board, before a map row exists")
    _, evaluated = call("POST", "/plan/evaluate", plan, fatal=False)
    print(f"    score {evaluated.get('score')}  valid {evaluated.get('valid')}")
    report(evaluated)
    _, inspected = call("POST", "/plan/inspect", plan, fatal=False)
    for goal in inspected.get("goalDistances") or []:
        print(f"    goal {goal.get('id')} ({goal.get('kind')}): own {goal.get('ownSpawnBlocks')} "
              f"enemy {goal.get('enemySpawnBlocks')} ratio {goal.get('ratio')}"
              f"   (GO1 wants 3.0-4.0)")
    for gap in inspected.get("islandGaps") or []:
        print(f"    island gap: {json.dumps(gap)}   (CT12 wants 15-40 on a direct strait)")
    for run in inspected.get("frontlineRuns") or []:
        print(f"    frontline run: {json.dumps(run)}")
    for structure in inspected.get("structures") or []:
        if structure.get("kind") == "wall":
            print(f"    wall: {json.dumps(structure)}")
    if dry:
        raise SystemExit(0)

    # ── originate, store, compile ────────────────────────────────────────────────────────────
    print("== originate, store, compile")
    _, created = call("POST", "/plan", {"name": name})
    slug = created["slug"]
    print(f"    slug={slug}")
    call("PUT", f"/map/{slug}/plan", plan)
    _, compiled = call("POST", "/plan/compile", plan)
    report(compiled)
    layout, intent = compiled["layout"], compiled["intent"]

    # ── the finish a plan cannot state ───────────────────────────────────────────────────────
    print("== the finish")
    layout = patch_layout(layout, finish)
    query = "?force=true" if force else ""
    _, stored = call("PUT", f"/map/{slug}/sketch/from-plan{query}", layout)
    report(stored)

    # ── look at the ground before building it ────────────────────────────────────────────────
    print("== the ground, read back")
    _, read = call("POST", f"/map/{slug}/sketch/relief/read", layout)
    for island in read.get("islands") or []:
        print(f"    island {island.get('island') or island.get('id')}: cells={island.get('cells')} "
              f"low={island.get('low')} high={island.get('high')} "
              f"relief={island.get('relief')} symErr={island.get('symmetryError')}")
    if finish.get("relief") and not read.get("islands"):
        raise SystemExit("    relief/read answered no islands and a relief was stated — "
                         "the shapes are not rasterizing (GENERATION-NOTES §1). Stop.")

    # ── build ────────────────────────────────────────────────────────────────────────────────
    print("== build")
    _, finished = call("POST", f"/map/{slug}/sketch/finish")
    report(finished)
    if finish.get("voidEnforcement"):
        intent.setdefault("build", {})["voidEnforcement"] = \
            {"exclusions": finish.get("voidExclusions", [])}
    call("PUT", f"/map/{slug}/intent/from-plan", intent)
    # After the intent, not before. Storing an intent projects the map document from the intent's own
    # `meta`, which a compiled intent leaves empty — `intent/from-plan` carries authors from a *previously
    # stored intent*, and a first build has none. A metadata PATCH before this point is overwritten.
    if authors := finish.get("authors"):
        call("PATCH", f"/map/{slug}/metadata", {"name": name, "authors": authors}, fatal=False)
    # ── every prop the dressing pass declined ────────────────────────────────────────────────
    # After the intent, deliberately: DR-KEEP reads the spawn door's approach and the goal rings,
    # which do not exist on a map that carries only a sketch, so the same call before this point
    # answers a shorter list.
    print("== what the dressing pass declined")
    _, columns = call("POST", f"/map/{slug}/sketch/columns", layout, fatal=False)
    if findings(columns):
        report(columns)
    else:
        print("    nothing declined")
    # ── where the board is actually lived on ─────────────────────────────────────────────────
    # The last read, and the one no earlier driver took. Every gate up to this point asks whether
    # ground is *reachable* — the strait width, the traversability components, the goal ratios — and
    # a board can pass all of them while carrying whole regions no journey crosses. Coverage walks a
    # route between every pair of waypoints and classes the rest: ground within reach of a route or
    # an objective is `reached`, ground near a prop is `decorated`, and everything else is `dead`.
    # A named dead patch is a landform that has no reason to exist at the size it is.
    print("== where the ground is lived on")
    _, coverage = call("GET", f"/map/{slug}/coverage", fatal=False)
    if coverage.get("haveRoutes"):
        print(f"    reached {coverage['reachedCells']}  decorated {coverage['decoratedCells']}  "
              f"dead {coverage['deadCells']}  of {coverage['groundCells']}  "
              f"= {coverage['deadShare'] * 100:.1f}% dead")
        for patch in (coverage.get("deadPatches") or [])[:5]:
            print(f"    dead patch {patch['area']:>5} cells at "
                  f"({patch['centroidX']}, {patch['centroidZ']}), "
                  f"{patch['nearestReachedBlocks']} blocks from used ground")
    _, zip_bytes = call("GET", f"/map/{slug}/export", raw=True)
    if out:
        if os.path.isdir(out):
            shutil.rmtree(out)          # B102: never export over a region dir that was not cleared
        os.makedirs(out)
        zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(out)
        print(f"    world -> {out}")
    # the documents that were actually posted, beside the ones that were authored
    with open(f"{specdir}/{base}.layout.json", "w") as handle:
        json.dump(layout, handle, indent=1)
    with open(f"{specdir}/{base}.intent.json", "w") as handle:
        json.dump(intent, handle, indent=1)
    print(f"DONE slug={slug}")


if __name__ == "__main__":
    main()
