#!/usr/bin/env python3
"""Drive a board's spec through the pgm-studio API to an exported world, and say what the pipeline said on
the way.

    tools/drive.py <specdir> "<Map Name>" [--slug <slug>] [--world <name>] [--out <worlddir>] [--no-world]
                   [--note "<what this pass is>"] [--after <change>] [--discard <change>,...] [--dry]

**A run starts with the board's own script.** Where `<specdir>` holds a `build-spec.py`, it is run first and
the documents it writes are the ones driven, so a pass can never send the documents the previous pass left
behind. It is run against the studio being driven, through `PGM_STUDIO_API`.

**A spec is a sketch source: a drawing, what it is played for, and what is stated on top of it.**
<specdir> holds <base>.layout.json and <base>.intent.json -- the two documents the Sketch tool and Configure
write -- and, where anything is stated on top of them, <base>.refinement.json. All three are the spec's
input and are never written over. A spec with no refinement states in its intent's own meta what a
refinement would otherwise say about it -- `authors` and `created`. <base> is the directory's own name and,
unless --slug says otherwise, the slug the map is stored under.

**A spec written as a plan is imported, once per run.** A frozen spec holds <base>.plan.json beside its
refinement instead of a drawing; its plan is compiled by `POST /plan/compile` into a layout and an intent,
the refinement is stated on top of those, and the layout and intent the studio stored are written back
beside the plan as the run's output. The plan is the only thing such a spec's drawing is read from, so a
layout beside it is never read as input.

**The refinement is the studio's own document, and the studio applies it.** It carries everything a drawing
does not state, keyed onto the layout, and `PUT /map/{slug}/source` applies it onto the layout and intent it
is stated over and stores the result as one change (`pgm-studio/docs/tools/flow.md`, *A map's source is the
way in*). Nothing here applies a key.

**Every key below is the batched form of one studio route, and the route is what the key means.** The
studio addresses each part of a stored layout on its own — a layer, a group, a shape, a theme, a relief, a
prop, a room shell, the biome — and a spec-driven build states the whole document in one call instead,
because the layout is derived from this file on every run and there is nothing incremental to edit. So the
refinement is a translation, not a second language: where a key and its route disagree about what a word
means, the route is right and this file is wrong. Each row names its route.

  key                 the one studio call it batches
  ---                 ------------------------------
  addShapes           POST   /map/{slug}/sketch/layers/{layerId}/shapes?group={groupId}
  addLayers           PUT    /map/{slug}/sketch/layers/{layerId}
  themeById           PATCH  /map/{slug}/sketch/shapes/{shapeId}   {"theme": ...}
  themeByHeight       the same, over every compiled shape standing at that height
  shapePropsById      PATCH  /map/{slug}/sketch/shapes/{shapeId}
  shapePropsByHeight  the same, by height
  editShapes          PATCH/POST/DELETE /map/{slug}/sketch/shapes/{shapeId}/vertices[/{index}]
  bendShapes          POST   /map/{slug}/sketch/shapes/{shapeId}/bend
  relief              PUT    /map/{slug}/sketch/relief/{groupId}
  themes              PUT    /map/{slug}/sketch/themes/{themeId}
  mapTheme            PUT    /map/{slug}/sketch/map-theme
  roomStyles          PUT    /map/{slug}/sketch/room-styles/{part}
  dressing            POST   /map/{slug}/sketch/props
  biome               PUT    /map/{slug}/sketch/biome
  authors · created   PUT    /map/{slug}/intent

**Four keys address a shape by its id.** `themeById`, `shapePropsById`, `editShapes` and `bendShapes` name
a shape of the layout. In a drawn layout the id is whatever the drawing states; in a compiled plan it is the
id the compiler mints, its component's first piece and the surface it stands at — `bahnhof-30`, and
`bahnhof-30-2` where one surface fuses into two. A key naming no shape is answered `SR2` with the ids the
board does have, which is what a re-key is done from.

What each key states:

  themeByHeight   {"11": "gyp-bench", ...}   theme per compiled shape, by the height it stands at
  themeById       {"s3": "gyp-rake"}          theme per compiled shape id (wins over the height rule)
  shapePropsByHeight {"11": {"relief_scope": "exclude"}, ...}   fields merged onto a compiled shape
  shapePropsById  {"s3": {...}}
  editShapes      {"garth-14": [{"after": 1, "x": 92, "z": -70}, {"index": 4, "x": 80, "z": -60},
                  {"remove": 7}, {"pulls": {"0": [[0.5, 2]]}}]}  every outline carrying the id -- a
                  shape's vertices, an area mark's or push's ring, a stroke's, fluid's or flora's points --
                  reshaped one point at a time, in order, before any bend. `after` inserts a point on that
                  edge (at its midpoint when no x/z is stated), `index` moves the point there, `remove`
                  drops it, `pulls` moves points a fraction along an edge in or out; every other point stays
                  exactly where it was drawn, and each op is stated against the ring as the ops before it
                  left it. An op naming none or more than one of the four refuses the whole source (`SR4`);
                  a pull on a stroke or a fluid channel, which is a line, is a complaint
  bendShapes      {"bahnhof-30": {"tension": 0.22, "wander": 3, "step": 10, "seed": 5, "side": "out"}}
                  every ring carrying the id drawn as a coast, after every point edit. The outline's own vertices
                  never move; `tension` is the Bezier handle's length as a fraction of its edge (0.22 where
                  absent); `side` is "out" (the default -- the slight bloat that reads as land), "in" (keeps
                  the drawn footprint) or "both"
  addShapes       [SketchShape + layer? + group?, ...]  authored shapes, each onto the layer and group it
                  names -- the studio's POST /map/{slug}/sketch/layers/{layerId}/shapes?group={id}. A shape
                  naming neither takes the compiled ground's first group
  addLayers       [{id, name, base_y, shapes, groups, below?, kind?, part_of?, seat?}]  stacked slabs;
                  `below` puts one under the compiled ground, which is also the layer a shape
                  naming none joins. `kind: "made"` marks a made thing — out of the stacking rules, painted
                  over its own span; `part_of` names the thing a run of layers is sliced from and `seat:
                  "ground"` settles them onto the terrain together
  relief          {"<groupId>": {...}} or {"*": {...}} applied to every group
  themes          the theme registry;  mapTheme  the map default (first key unless stated)
  biome           SketchLayout's own biome field: {"kind": "cell"|"noise"|"solid", ...}. The byte each
                  chunk carries, which tints grass, leaves and water. Absent is plains everywhere
  roomStyles      {"wool": ..., "spawn": ...} -- the two members SketchRoomStyles carries, each a style
                  or {"library": "<name>"}, a row of the studio's room library with any changes laid
                  beside the name. It was "cage" until 2026-09-07. A key
                  neither of those names is answered RQ3 by the whole-layout write below, and a
                  kind left unbound stands in the built-in bedrock box, which every build answers
                  WX14
  dressing        {"styles": ..., "props": [...]};  a house prop's "style" names a library row the
                  same way, and a copied tree is the recipe the studio's tree library answers.
                  A style in "styles" is a discriminated PropStyle: a house is
                  {"kind": "house", "shell": <HouseStyle>}, and a bare HouseStyle is refused DR-DOC
  shops           [{"id", "name", "keeper": {"name", "mob"}, "categories": [...]}] -> intent.shops. The
                  menu only: where the keepers stand is the studio's, one per shop at every team's spawn
  spawners        [{"id", "at": {x,y,z}, "pad", "reach", "protect", "delay", "maxEntities", "drops"}]
                  -> intent.spawners. The generators that mint what a board is played for beyond its kit.
                  `at` names a square of ground, not a point: the block it is the centre of where it is a
                  block centre, the four it corners where it is a whole number -- so a 2x2 pad on a board's
                  own centre line is stated as a whole number and a 1x1 as a .5
  authors         ["Opus 5"], or [{"name", "uuid", "role", "contribution"}] -> the <authors> block. PGM
                  takes a person as an account OR a pseudonym, so a bare name is a valid author
  created         "2026-08-25" -> intent.meta.created -> <created>. The studio cannot know when a map was
                  made and invents nothing, so a board that states none carries none

The whole map is stored in ONE call — `PUT /map/{slug}/source` takes the layout, the intent and the
refinement, applies the refinement, rasterizes the drawing, projects the intent
into the map document and applies the authors, and keeps the run as one change of the map. The change
carries where the spec was built — the repository, the commit, the spec's folder, and whether the working
tree differed from the commit — and `--note`, a sentence saying what this pass is. The slug is stated, so
re-driving a corrected spec REPLACES the map it had rather than leaving a second one beside it.

**Every run shows what it would change before it changes it.** The same source is sent with `?dry=true`
first, and every edit it would make to the documents the map holds is printed before the store; `--dry`
stops there.

**A run over a change the spec has not seen is refused, and the change is handed over.** A person editing the
board in the Sketch tool between runs — fixing a coast, showing how — or another writer's source makes a change
after the one this spec was applied as, and the studio answers the next run `409` with one `SR1` per edit that
change made, each carrying the edit as the refinement would state it. Take the edits into the spec and pass
`--after <change>`, the change taken in; or pass `--discard <change>,...` to replace them, which the change
the run lands as records. A board whose source states no refinement is its drawing, and is never refused.

Nothing here computes a placement, a clearance or a validation: it posts documents and prints what
came back. Every finding the pipeline raises is printed with its rule id and the JSON path it is
about — a refusal's `findings`, and, on every 2xx, the
`warnings` a success carries. That last one is the half a driver reading only the status code throws
away: a decline says one piece of the posted document is not in the world, `RQ3` names a field that
went unread, and `SK3`/`SK4` name a shape that drew no ground. `GET /api/rules?rule=<id>` answers what
any of those means and how to fix it.

**What was built is read back in one request.** `GET /map/{slug}/report` builds the stored board once and
answers the three numbers it is wrong or right by, then every reading a run used to ask for one at a time —
the findings, the relief, the declines, pre-flight, coverage, the heightmap and the
slopes, a transect each way through every thing on the board and a walk from every spawn to every goal,
the census, the claims, the seats and the void scan — each beside the route that answers it alone. The run
prints the numbers and the short readings, and writes the whole report to `out/reports/<slug>.txt`.

**One picture a board is kept, beside its documents.** `<base>.png` is the board seen from its long side
through the studio's own eye, in the game's block sprites; the export's `map.png` lands in the world folder. Every other picture stays in the studio, drawn again from the board as it stands — the report names
each one by its route — so a board's old `renders/` folder is cleared when it is driven.

**The world lands in `maps/<mode>/<name>/`**, the folder `maps/INDEX.md` names for the slug: `region/`,
`level.dat`, `map.xml` and `map.png`, which is what a server is handed. A slug the index does not name yet is added
under its map's name and game mode (`tools/worlds.py`); `--world <name>` names the folder where that name is
another board's. `--out` writes somewhere else instead, and `--no-world` writes no world. The provenance sidecar
lands beside the documents.
"""
import json, re, sys, io, time, zipfile, urllib.request, urllib.error, urllib.parse, os, shutil, subprocess
import studio_token
import worlds

SPECDIR = None

# Where the studio answers is a fact about the machine, not about this repository, and it has been a
# different port on every environment the boards here were built on. So it is DISCOVERED rather than
# defaulted: `PGM_STUDIO_API` wins outright and is not probed, and with nothing stated the candidates
# below are asked `GET /api/health` in turn. A wrong constant is worse than no constant -- it fails at
# the first call with a connection error that says nothing about what to set.
CANDIDATES = ["http://localhost:7894/api", "http://localhost:5189/api", "http://localhost:5000/api"]
_api = None


def signed(headers):
    """`headers` with the token `PGM_STUDIO_TOKEN` holds, where it holds one (`studio_token`)."""
    return {**headers, **studio_token.authorization(endpoint())}


def endpoint():
    """The studio's base URL, resolved once and printed when it was found rather than told."""
    global _api
    if _api is not None:
        return _api
    stated = os.environ.get("PGM_STUDIO_API")
    if stated:
        _api = stated.rstrip("/")
        print(f"  studio at {_api}" + ("  (signed in by PGM_STUDIO_TOKEN)" if signed({}) else ""))
        return _api
    for candidate in CANDIDATES:
        try:
            with urllib.request.urlopen(candidate + "/health", timeout=2) as response:
                if response.status == 200:
                    _api = candidate
                    print(f"  studio at {candidate}  (set PGM_STUDIO_API to state one)")
                    return _api
        except Exception:
            continue
    raise SystemExit("no studio answered GET /api/health at " + ", ".join(CANDIDATES) +
                     "\n  Set PGM_STUDIO_API to the endpoint, e.g. "
                     "PGM_STUDIO_API=http://localhost:1234/api")


# A studio that is building as many worlds as it builds at once answers 429 `RQ11` with a `Retry-After`,
# which is a turn not yet had rather than a fault, so the request is asked again after that wait. Ten
# tries is about two minutes behind other callers' builds before the run stops on it.
BUSY_TRIES = 10


def _exchange(method, path, data):
    """One request on the wire: `(status, payload, Pgm-Warnings)` on a 2xx, `(status, text, None)` on an
    HTTP refusal. Anything else — a refused connection, a timeout — raises, as it always has."""
    for attempt in range(BUSY_TRIES):
        req = urllib.request.Request(endpoint() + path, data=data, method=method,
                                     headers=signed({"Content-Type": "application/json"} if data else {}))
        try:
            with urllib.request.urlopen(req, timeout=1800) as response:
                return response.status, response.read(), response.headers.get("Pgm-Warnings")
        except urllib.error.HTTPError as error:
            text = error.read().decode()
            wait = error.headers.get("Retry-After")
            if error.code != 429 or not (wait or "").isdigit() or attempt == BUSY_TRIES - 1:
                return error.code, text, None
            print(f"  {method:5} {path:46} 429   the studio is busy, asking again in {wait} s")
            time.sleep(int(wait))


def call(method, path, body=None, raw=False, fatal=True):
    """One request. Returns (status, payload). A non-2xx is printed with its findings and, unless
    fatal is False, stops the run — a refusal is a fault to fix, not a step to skip.

    A 2xx is printed with its `warnings` too, here rather than at the call sites, because a success is
    not a promise that everything posted survived: a decline says one piece of the document is not in
    the world, and `RQ3` names a field that went unread. The `Pgm-Warnings` header carries the same
    count and rule ids, so the status line says how much there is before the body is parsed."""
    data = None if body is None else json.dumps(body).encode()
    status, payload, carried = _exchange(method, path, data)
    if status < 300:
        print(f"  {method:5} {path:46} {status}"
              f"{'   ! ' + carried if carried else ''}")
        if raw:
            return status, payload
        answered = json.loads(payload) if payload else {}
        complaints(answered)
        return status, answered
    text = payload
    print(f"  {method:5} {path:46} {status}")
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
    return status, body


def findings(payload, keys=("findings",)):
    """Every finding shape the studio answers in, under the keys it uses. `warnings` is read on its own,
    by `complaints` at the point of the call, so a complaint is printed once and beside the request that
    raised it rather than at whichever site remembered to ask."""
    out = []
    if not isinstance(payload, dict):
        return out
    for key in keys:
        entries = payload.get(key)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            out.append((key, entry))
    return out


def report(payload, indent="  ", keys=("findings",)):
    for key, entry in findings(payload, keys):
        rule = entry.get("rule") or entry.get("id") or key
        severity = entry.get("severity") or key
        message = entry.get("message") or entry.get("detail") or json.dumps(entry)
        # A finding names what it is about as `field` on the request routes and as `subjects` on
        # `GET /map/{slug}/findings`, which judges shapes rather than a posted document.
        field = entry.get("field") or ", ".join(entry.get("subjects") or [])
        print(f"{indent}  [{severity:9}] {rule:8} {message}"
              f"{'   @ ' + field if field else ''}")
        # A finding that states its edit says what to change in the document's own words: which document,
        # the path, the operation and the value. Printed under the sentence so it is applied rather than
        # re-derived from the rule's prose.
        if isinstance(edit := entry.get("edit"), dict):
            print(f"{indent}    edit  {edit.get('document')}.{edit.get('path')}  {edit.get('op')}: "
                  f"{edit.get('says')}")
            print(f"{indent}          {json.dumps(edit.get('value'), separators=(',', ':'))}")


def complaints(payload):
    """What a 2xx did not do. A decline means one piece of the document is not in the world and ignoring
    it does not put it back; a complaint means nothing was lost and something is worth saying anyway."""
    report(payload, keys=("warnings",))


def origin(specdir):
    """Where the spec was built, as the change the run lands as keeps it: the repository, the commit, the
    spec's folder, and whether the folder held changes the commit does not — in which case the commit alone
    does not rebuild what was stored. None where the spec is not in a git checkout."""
    def git(*arguments):
        done = subprocess.run(["git", "-C", specdir, *arguments], capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else None

    root, commit = git("rev-parse", "--show-toplevel"), git("rev-parse", "--short", "HEAD")
    if not root or not commit:
        return None
    remote = git("remote", "get-url", "origin") or ""
    repo = "/".join(re.sub(r"\.git$", "", remote.rstrip("/")).split("/")[-2:]) or None
    return {"repo": repo, "commit": commit,
            "path": os.path.relpath(os.path.abspath(specdir), root),
            "dirty": bool(git("status", "--porcelain", "--", "."))}


def changed(answer):
    """What the source changed in the documents the map held, as the studio answered it: a new map states
    every document for the first time, so it is counted; a replaced one is listed edit by edit, because that
    is what the run did to the board somebody may have been reading."""
    edits = answer.get("edits") or []
    if not answer.get("replaced"):
        print(f"    a new map: {len(edits)} member(s) of its layout, intent and refinement stated for the first time")
        return
    if not edits:
        print("    nothing changed: the map already held what the spec states")
        return
    print(f"    {len(edits)} edit(s) to what the map held:")
    for edit in edits[:40]:
        print(f"      {edit.get('document'):7} {edit.get('op'):6} {edit.get('path')}  {edit.get('says')}")
    if len(edits) > 40:
        print(f"      … and {len(edits) - 40} more — GET /map/{{slug}}/diff?format=text has them all")


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Where the report a run reads back is written: under `out/`, which is not committed, because the report is the
# studio's to draw again from any change and a copy here would be a second, stale one.
REPORTS = os.path.join(ROOT, "out", "reports")
# The readings short enough to print whole after a store; the rest are in the report file.
PRINTED = ("findings", "declines", "preflight", "coverage")
# The picture a board keeps, in pixels: wide enough to read a board's length at a glance.
PICTURE = (1280, 720)


def stated(specdir):
    """What a spec states: `(plan, layout, intent, refinement)`. A sketch spec's layout and intent are its own
    files and its plan is None; a frozen plan spec's plan is compiled by `POST /plan/compile`, and the layout
    beside it is the last run's output rather than anything read. The refinement is None where none is stated."""
    base = os.path.basename(specdir.rstrip("/"))

    def document(suffix):
        path = f"{specdir}/{base}.{suffix}.json"
        if not os.path.exists(path):
            return None
        with open(path) as handle:
            return json.load(handle)

    refinement = document("refinement")
    plan = document("plan") if refinement is not None else None
    if plan is not None:
        print("== the plan, imported")
        _, compiled = call("POST", "/plan/compile", plan)
        complaints(compiled)
        return plan, compiled["layout"], compiled["intent"], refinement
    layout, intent = document("layout"), document("intent")
    if layout is None or intent is None:
        raise SystemExit(f"{specdir}: needs {base}.layout.json and {base}.intent.json, "
                         f"or {base}.plan.json beside {base}.refinement.json")
    return None, layout, intent, refinement


def build_spec(specdir):
    """Run `<specdir>/build-spec.py` where there is one, against the studio being driven, so the documents
    sent are the ones the script writes now. A script that fails stops the run."""
    script = os.path.join(specdir, "build-spec.py")
    if not os.path.exists(script):
        return
    print("== the spec, written by its script")
    done = subprocess.run([sys.executable, os.path.abspath(script)], cwd=specdir, env={**os.environ, "PGM_STUDIO_API": endpoint()})
    if done.returncode != 0:
        raise SystemExit(f"    {script} exited {done.returncode}: the spec was not written, so nothing is sent")


def read_back(slug):
    """The stored board read back in one request: the three numbers and the short readings printed, the whole
    report written to `out/reports/<slug>.txt`."""
    print("== the board, read back")
    status, payload = call("GET", f"/map/{slug}/report?format=text", raw=True, fatal=False)
    if status >= 300:
        return
    report_text = payload.decode("utf-8", "replace")
    os.makedirs(REPORTS, exist_ok=True)
    written = os.path.join(REPORTS, f"{slug}.txt")
    with open(written, "w") as handle:
        handle.write(report_text)
    sections = report_text.split("\n== ")
    for line in sections[0].splitlines()[2:]:
        print(f"  {line.strip()}")
    for section in sections[1:]:
        head, _, body = section.partition("\n")
        if head.split("   ")[0] in PRINTED:
            print(f"  -- {head}")
            for line in body.rstrip("\n").splitlines():
                print(f"    {line}")
    print(f"    {len(sections) - 1} readings -> {os.path.relpath(written, ROOT)}")


def picture(slug, specdir, base):
    """The board seen from its long side through the studio's eye, kept beside its documents as `<base>.png`.
    A studio without the block sprites draws none, and says why."""
    print("== the board's picture")
    _, views = call("GET", f"/map/{slug}/views", fatal=False)
    if not isinstance(views, dict):
        return
    if views.get("undrawable"):
        print(f"    none kept: {views['undrawable']}")
        return
    overview = next((view for view in views.get("views") or [] if view.get("id") == "overview"), None)
    if overview is None:
        print("    none kept: the board has no ground to frame")
        return
    width, height = PICTURE
    status, png = call("GET", f"/map/{slug}/render/eye?{overview['query']}&width={width}&height={height}",
                       raw=True, fatal=False)
    if status >= 300:
        return
    with open(os.path.join(specdir, f"{base}.png"), "wb") as handle:
        handle.write(png)
    print(f"    {base}.png  — {overview.get('name')}, {width}×{height}")


def clear_renders(specdir):
    """A board's old debug renders go: the studio draws every picture again from the board as it stands, and
    the report names each one by its route."""
    renders = os.path.join(specdir, "renders")
    if os.path.isdir(renders):
        shutil.rmtree(renders)
        print("    renders/ cleared — the studio draws every picture on request (GET /map/{slug}/report names them)")


def home(slug, zip_bytes, chosen):
    """The world folder for `slug`: the one maps/INDEX.md names, else a new row under the exported map's name and
    game mode (or `chosen`, where that name is taken)."""
    known = worlds.of(slug)
    if known is not None:
        return known
    archive = zipfile.ZipFile(io.BytesIO(zip_bytes))
    xml = next((archive.read(entry).decode("utf-8", "replace") for entry in archive.namelist()
                if entry.endswith("map.xml")), "")
    place = worlds.place(xml)
    if place is None:
        raise SystemExit(f"the export of {slug} states no map name; pass --world <name> or --out <dir>")
    if chosen:
        place = f"{place.split('/')[0]}/{worlds.snake(chosen)}"
    source = os.path.relpath(SPECDIR, worlds.ROOT) if SPECDIR else ""
    worlds.register(place, slug, source)
    print(f"    maps/INDEX.md: {slug} -> maps/{place}")
    return os.path.join(worlds.WORLDS, place)


def main():
    def option(flag):
        return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None

    specdir, name = sys.argv[1], sys.argv[2]
    global SPECDIR
    SPECDIR = os.path.abspath(specdir)
    out = option("--out")
    note = option("--note")
    after = int(option("--after")) if option("--after") else None
    discard = option("--discard")
    dry = "--dry" in sys.argv
    base = os.path.basename(specdir.rstrip("/"))
    slug = option("--slug") or base

    build_spec(specdir)
    plan, layout_in, intent_in, refinement = stated(specdir)

    # ── the map, from its source ─────────────────────────────────────────────────────────────
    # One call applies the refinement, stores the documents as one change, rasterizes the drawing, projects
    # the intent and applies the authors. It is asked dry first, so what it would change is on the screen
    # before it is changed.
    source = {"name": name, "layout": layout_in, "intent": intent_in, "origin": origin(specdir), "note": note,
              "after": after}
    if refinement is not None:
        source["refinement"] = refinement
    # A change the spec has not seen — a hand edit in the Sketch tool, another writer's source — refuses the
    # run 409, printed with the edit each SR1 hands over; `--after` takes it in, `--discard` drops it.
    dropping = f"discard={urllib.parse.quote(discard)}" if discard else ""
    print("== what the run would change")
    _, would = call("PUT", f"/map/{slug}/source?dry=true{'&' + dropping if dropping else ''}", source)
    changed(would)
    if dry:
        raise SystemExit(0)
    print("== the map, from its source")
    _, stored = call("PUT", f"/map/{slug}/source{'?' + dropping if dropping else ''}", source)
    print(f"    slug={slug}  change {stored.get('change')}  "
          f"{'replaced' if stored.get('replaced') else 'new'}  "
          f"cells={stored.get('cells')}  islands={stored.get('islands')}")
    _, layout = call("GET", f"/map/{slug}/sketch")
    _, intent = call("GET", f"/map/{slug}/intent")
    if not (intent.get("meta") or {}).get("created"):
        print("    ! nothing states a `created` date, so the map will carry no <created> element")

    read_back(slug)

    if "--no-world" not in sys.argv:
        print("== the world")
        _, zip_bytes = call("GET", f"/map/{slug}/export", raw=True)
        if not out:
            out = home(slug, zip_bytes, option("--world"))
        if os.path.isdir(out):
            shutil.rmtree(out)          # never export over a region dir that was not cleared
        os.makedirs(out)
        zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(out)
        # The archive wraps the world in a directory named for the slug. `--out` is the world directory
        # itself — region/, level.dat, map.xml and map.png at its top — so the wrapper is unwrapped rather
        # than left for a caller to notice.
        held = os.listdir(out)
        if len(held) == 1 and os.path.isdir(os.path.join(out, held[0])):
            wrapper = os.path.join(out, held[0])
            for entry in os.listdir(wrapper):
                shutil.move(os.path.join(wrapper, entry), os.path.join(out, entry))
            os.rmdir(wrapper)
        print(f"    world -> {out}")
        # The provenance sidecar is a read-back aid — which pass claimed which column — so it travels with
        # the documents rather than with the world a server is handed.
        recorded = os.path.join(out, "region", "provenance.json")
        if os.path.exists(recorded):
            shutil.move(recorded, os.path.join(specdir, "provenance.json"))
            print(f"    provenance -> {specdir}/provenance.json")
        picture(slug, specdir, base)
        clear_renders(specdir)
    # A plan spec's documents are the run's output and are written beside its plan; a sketch spec's are its
    # input and are left exactly as authored, so re-driving one is byte-identical by construction.
    if plan is not None:
        with open(f"{specdir}/{base}.layout.json", "w") as handle:
            json.dump(layout, handle, indent=1)
        with open(f"{specdir}/{base}.intent.json", "w") as handle:
            json.dump(intent, handle, indent=1)
    print(f"DONE slug={slug}")


if __name__ == "__main__":
    main()
