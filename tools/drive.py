#!/usr/bin/env python3
"""Drive a plan + refinement document through the pgm-studio API to an exported world, and say what the
pipeline said on the way.

    tools/drive.py <specdir> "<Map Name>" --out <worlddir> [--renders <dir>] [--slug <slug>]
                   [--note "<what this pass is>"] [--after <change>] [--discard <change>,...] [--dry]

<specdir> holds <base>.plan.json and EITHER <base>.refinement.json, OR a hand-drawn <base>.layout.json and
<base>.intent.json -- the shape the Sketch tool writes, whose geometry is authored rather than compiled.
The either/or is exact: a spec carrying a refinement is compiled from its plan on every run, and the layout
and intent beside it are what the last run stored rather than anything it reads. A drawn spec's layout
and intent are its input and are never written over, so it states in its intent's own meta what a
refinement would otherwise say about it -- `authors` and `created`. <base> is the directory's own name and,
unless --slug says otherwise, the slug the map is stored under. Both shapes take the same road from here:
the same grid, flow, declines and renders.

**The refinement is the studio's own document, and the studio applies it.** It carries everything a plan
cannot state, keyed onto the compiled layout, and `PUT /map/{slug}/source` compiles the plan, applies the
refinement onto what the plan compiled to, and stores the result as one change
(`pgm-studio/docs/tools/flow.md`, *A map's source is the way in*). Nothing here applies a key.

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

**Four keys address the compiler's own output.** `themeById`, `shapePropsById`, `editShapes` and
`bendShapes` name a shape by the id the compiler mints, which is its component's first piece and the surface
it stands at — `bahnhof-30`, and `bahnhof-30-2` where one surface fuses into two. A piece inserted, renamed or
moved to another height renames what it anchors, and the key then names nothing: the studio answers `SR2`
for such a key with the ids the board does have, which is what a re-key is done from.

What each key states:

  themeByHeight   {"11": "gyp-bench", ...}   theme per compiled shape, by the height it stands at
  themeById       {"s3": "gyp-rake"}          theme per compiled shape id (wins over the height rule)
  shapePropsByHeight {"11": {"relief_scope": "exclude"}, ...}   fields merged onto a compiled shape
  shapePropsById  {"s3": {...}}
  editShapes      {"garth-14": [{"after": 1, "x": 92, "z": -70}, {"index": 4, "x": 80, "z": -60},
                  {"remove": 7}]}  the outline reshaped one point at a time, in order, before any bend.
                  `after` inserts a point on that edge (at its midpoint when no x/z is stated), `index`
                  moves the point there, `remove` drops it; every other point of the outline stays exactly
                  where it was drawn, and each op is stated against the ring as the ops before it left it.
                  An op naming none or more than one of the three refuses the whole source (`SR4`)
  bendShapes      {"bahnhof-30": {"tension": 0.22, "wander": 3, "step": 10, "seed": 5, "side": "out"}}
                  the compiled outline drawn as a coast, after every point edit. The outline's own vertices
                  never move; `tension` is the Bezier handle's length as a fraction of its edge (0.22 where
                  absent); `side` is "out" (the default -- the slight bloat that reads as land), "in" (keeps
                  the plan's footprint) or "both"
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
  roomStyles      {"wool": ..., "spawn": ...} -- the two members SketchRoomStyles carries; a "@name"
                  string loads tools/styles/<name>.json, resolved here before the refinement is sent. It
                  was "cage" until 2026-09-07. A key
                  neither of those names is answered RQ3 by the whole-layout write below, and a
                  kind left unbound stands in the built-in bedrock box, which every build answers
                  WX14
  dressing        {"styles": ..., "props": [...]};  a house prop's "style" takes the same "@name",
                  resolved the same way.
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

The whole map is stored in ONE call — `PUT /map/{slug}/source` takes the plan and the refinement (a drawn
spec: the plan, its layout and its intent), compiles, applies, rasterizes the drawing, projects the intent
into the map document and applies the authors, and keeps the run as one change of the map. The change
carries where the spec was built — the repository, the commit, the spec's folder, and whether the working
tree differed from the commit — and `--note`, a sentence saying what this pass is. The slug is stated, so
re-driving a corrected spec REPLACES the map it had rather than leaving a second one beside it. The answer
names every edit the run made to the documents the map held; `--dry` asks the studio the same question with
`?dry=true` and stores nothing.

**A run over a change the spec has not seen is refused, and the change is handed over.** A person editing the
board in the Sketch tool between runs — fixing a coast, showing how — or another writer's source makes a change
after the one this spec was applied as, and the studio answers the next run `409` with one `SR1` per edit that
change made, each carrying the edit as the refinement would state it. Take the edits into the spec and pass
`--after <change>`, the change taken in; or pass `--discard <change>,...` to replace them, which the change
the run lands as records. A board whose source states no refinement is its drawing, and is never refused.

Nothing here computes a placement, a clearance or a validation: it posts documents and prints what
came back. Every finding the pipeline raises is printed with its rule id and the JSON path it is
about — a refusal's `findings`, the evaluator's `violations` and `lint`, and, on every 2xx, the
`warnings` a success carries. That last one is the half a driver reading only the status code throws
away: a decline says one piece of the posted document is not in the world, `RQ3` names a field that
went unread, and `SK3`/`SK4` name a shape that drew no ground. `GET /api/rules?rule=<id>` answers what
any of those means and how to fix it.

`GET /map/{slug}/findings` is asked on every run beside those, because it is the only read that
answers `SK9` — the gate that knows two shapes on one layer stacked and the lower one is not in the
world. It is a decline, the channel every other route publishes on keeps complaints alone, and so a
board can store at 200 with a floor missing under its walls and nothing anywhere says so.

It also takes every picture the studio will draw for what was authored — a swatch per theme, a plan and a
section per house, the coverage map, the board read back from every angle, and the grid and flow as text —
into `<specdir>/renders`, or into `--renders <dir>`. Taking a picture is not the same as looking at one;
what it removes is the excuse.

Two of those pictures are drawn here rather than fetched, because the studio answers columns and not
cameras: `world-iso` and, where the board holds a covered space, `world-xray`, which washes out whatever
stands between the camera and a roofed void so a chamber under a hill is in the picture at all. The void
scan behind it prints on every board — how much covered space there is, between which blocks, and which
of it is SEALED, meaning nothing can walk into it.

The pictures and the provenance sidecar land beside the documents rather than in the exported world, because
`--out` is what a server is handed: it holds `region/`, `level.dat` and `map.xml`, and nothing a match does
not read.
"""
import collections, concurrent.futures, json, math, multiprocessing, re, sys, io, time, zipfile, urllib.request, \
    urllib.error, urllib.parse, os, shutil, subprocess
import studio_token

STYLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")

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


# Requests already on the wire, keyed by what they ask. **The studio answers reads side by side, and a run
# asks forty of them of one stored board**, so `ahead` sends the ones whose paths are known as soon as they
# are, and the `call` that asks for one later waits on it rather than sending its own. The printing stays
# in `call`, so the run reads in the order it always did; only the waiting overlaps.
_sent = {}
_wire = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def ahead(requests):
    """Send every `(method, path)` or `(method, path, body)` now, to be answered by the `call` asking it.
    Only reads go ahead: a write's order is part of what it means."""
    for method, path, *body in requests:
        data = None if not body or body[0] is None else json.dumps(body[0]).encode()
        if (method, path, data) not in _sent:
            _sent[(method, path, data)] = _wire.submit(_exchange, method, path, data)


def call(method, path, body=None, raw=False, fatal=True):
    """One request. Returns (status, payload). A non-2xx is printed with its findings and, unless
    fatal is False, stops the run — a refusal is a fault to fix, not a step to skip.

    A 2xx is printed with its `warnings` too, here rather than at the call sites, because a success is
    not a promise that everything posted survived: a decline says one piece of the document is not in
    the world, and `RQ3` names a field that went unread. The `Pgm-Warnings` header carries the same
    count and rule ids, so the status line says how much there is before the body is parsed."""
    data = None if body is None else json.dumps(body).encode()
    pending = _sent.pop((method, path, data), None)
    status, payload, carried = pending.result() if pending else _exchange(method, path, data)
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


# The band a measure is judged against and the sentence a rule is stated in are the studio's, read once
# per run: a number restated here is the number every future run is told after the author has moved it.
# `/rules/terms` answers the enforced band through the scorer's own resolution; `/rules` answers the rule.
_terms, _claims = {}, {}


def band(term):
    """`(low, high, source)` for a scored term, or None where the term carries no band."""
    if not _terms:
        _, answered = call("GET", "/rules/terms", fatal=False)
        for row in answered if isinstance(answered, list) else []:
            _terms[row.get("term")] = row
    stated = (_terms.get(term) or {}).get("band")
    return (stated[0], stated[1], (_terms.get(term) or {}).get("bandSource")) if stated else None


def wants(term, rule):
    """What to print beside a measure: the rule's own band where it has one, and the rule id alone
    where it does not — never a number written down here."""
    stated = band(term)
    return f"({rule} wants {stated[0]}-{stated[1]}, {stated[2]})" if stated else f"({rule})"


def rule_claim(rule):
    """A rule's own claim — the first bold sentence of what `GET /rules` says it means, which is where
    every rule states its number."""
    if rule not in _claims:
        _, answered = call("GET", f"/rules?rule={rule}", fatal=False)
        means = (answered[0].get("means") if isinstance(answered, list) and answered else "") or ""
        stated = re.search(r"\*\*(.+?)\*\*", means)
        _claims[rule] = stated.group(1).strip() if stated else rule
    return _claims[rule]


def text(path, fatal=False):
    """One GET whose answer is `text/plain` rather than a document — the grid and the flow account.
    Returns the body as a string, or None where the read failed; the status line is printed either
    way, so a read that 404s is visible rather than absent."""
    status, payload = call("GET", path, raw=True, fatal=fatal)
    return payload.decode("utf-8", "replace") if isinstance(payload, bytes) and status < 300 else None


# The smallest roofed void worth an x-ray: a room six blocks square with six courses of headroom. Under
# it the view draws what the plain isometric already drew, one shade paler.
XRAY_FLOOR = 200
# The widest grid worth printing at 1:1. Past it the board is downsampled, because a wall of characters
# nobody reads is the same as no read at all.
GRID_WIDTH = 110
# What a grid row spends on its frame: the z label, the two bars and the spaces around them. Only the
# characters between them are the board.
GRID_FRAME = 10


def grid(slug):
    """The stored plan as a grid of characters. Asked at 1:1 first — a route or a seam one cell wide is
    sampled away by any other step — and re-asked at the ratio the board actually turns out to need rather
    than at a guess about its size.

    Width is measured on the grid's own rows, which are the lines that close with the frame's right bar. The
    key under them wraps at its own width whatever the board does, so measuring the whole render measures the
    key and no board ever reads as wide."""
    drawn = text(f"/map/{slug}/plan/ascii")
    if drawn is None:
        return None
    widest = max((len(line) for line in drawn.splitlines() if line.rstrip().endswith("|")), default=0)
    if widest <= GRID_WIDTH:
        return drawn
    every = -(-(widest - GRID_FRAME) // (GRID_WIDTH - GRID_FRAME))
    return text(f"/map/{slug}/plan/ascii?every={every}")


def findings(payload, keys=("findings", "violations", "lint")):
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
            # an evaluator violation wraps the finding beside its term id and distance
            inner = entry.get("finding")
            out.append((key, inner if isinstance(inner, dict) else entry))
    return out


def report(payload, indent="  ", keys=("findings", "violations", "lint")):
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


def resolve(style):
    """A '@name' string is tools/styles/<name>.json. Anything else is the document itself."""
    if isinstance(style, str) and style.startswith("@"):
        with open(os.path.join(STYLES, style[1:] + ".json")) as handle:
            return json.load(handle)
    return style


def pictures(slug, layout, intent=None):
    """Every picture the studio will draw for what was authored, as `(file, method, path, body)`.

    The reads are the same ones the brief asks an author to look at, and the reason they are taken here is
    the reason the grid and the flow are printed here: a read nobody is refused for skipping is the read
    nobody takes. A theme swatch, a house in section and the coverage map each answer a question no
    top-down of the finished world can — and the section is the one every shipped roof fault was visible in."""
    asked = []

    # Two views a theme, because they answer different questions and neither substitutes. The section is
    # the column — rim over wall over fill, the pairing most easily got wrong. The surface is the swatch,
    # and it is the only view a pattern is legible in: a section through a voronoi is one block wide.
    for theme_id, theme in (layout.get("themes") or {}).items():
        for view in ("surface", "section"):
            asked.append((f"theme-{theme_id}-{view}.png", "POST",
                          f"/terrain/theme-preview?format=png&view={view}", theme))

    # Every distinct house the board stands up: the stamped rooms, and each house prop's own style. Keyed by
    # the style document rather than by where it was named, so one style used twice is drawn once.
    #
    # The key is serialized in the author's own key order, NOT sorted: a material's `kind` is read
    # positionally and has to come first, so sorting the keys of a style that previews at 200 turns it into a
    # 400 naming a kind that is right there (TL2).
    houses = {}
    for room_id, style in (layout.get("roomStyles") or {}).items():
        houses.setdefault(json.dumps(style), f"room-{room_id}")
    for prop in ((layout.get("dressing") or {}).get("props") or []):
        if prop.get("kind") == "house" and isinstance(prop.get("style"), dict):
            houses.setdefault(json.dumps(prop["style"]), f"house-{prop.get('id', len(houses))}")
    for style_json, house_id in houses.items():
        for view in ("plan", "section"):
            asked.append((f"{house_id}-{view}.png", "POST",
                          f"/room-styles/preview-snapshot?format=png&view={view}", json.loads(style_json)))

    asked.append(("coverage.png", "GET", f"/map/{slug}/coverage?format=png", None))

    # The world itself, read back through the routes that answer it. These are the reads an author is meant
    # to look at after building and the ones nobody ever took, because until they answered over HTTP an agent
    # had to know a .NET binary existed. `column` is the workhorse and is not here: it answers one coordinate
    # and the coordinates worth asking about are the author's, not a driver's.
    for name, route in (
        ("world-topdown.png", "render/topdown"),
        ("world-ground.png", "render/topdown?layer=ground&material=1"),
        # `subject` is the category asked about; `layer` is the sketch storey. A board whose storeys are a
        # ground plus a made thing's runs has no storey called "structure", so asking by `layer` for one is
        # `RQ4` and no picture at all.
        ("world-structure.png", "render/topdown?subject=structure"),
        ("world-made.png", "render/topdown?subject=made"),
        ("world-foliage.png", "render/topdown?subject=foliage"),
        ("world-objectives.png", "render/topdown?subject=objectives"),
        ("world-heightmap.png", "render/heightmap"),
        ("world-surface.png", "render/surface"),
        ("world-traversability.png", "render/traversability"),
        ("world-mirror.png", "render/mirror"),
        ("world-section-x0.png", "render/section?axis=x&at=0&from=-120&to=120"),
        ("world-section-z0.png", "render/section?axis=z&at=0&from=-120&to=120"),
    ):
        asked.append((name, "GET", f"/map/{slug}/{route}", None))

    # The board where a player stands, in the game's own textures: every other picture here draws a block as
    # one colour, which is where two noisy blocks of one colour read as calm ground and are static in the
    # game. Each is framed on something the documents place, so no camera is guessed; a studio without the
    # textures answers 503 and the picture is skipped like any other refusal.
    asked += [(name, "GET", f"/map/{slug}/render/eye?{query}", None) for name, query in eye_views(layout, intent)]
    return asked


def eye_views(layout, intent):
    """`(file, query)` for each thing worth seeing at eye height: every spawn facing its own team's objective,
    every objective, and the first boulders and houses the dressing places."""
    views = []
    intent = intent or {}
    goals = {}
    for goal in (intent.get("destroyables") or []) + (intent.get("cores") or []):
        at = goal.get("anchor") or goal.get("location") or {}
        if "x" in at and "z" in at:
            goals.setdefault(goal.get("owner"), (int(at["x"]), int(at["z"])))
    for index, spawn in enumerate(intent.get("spawns") or []):
        point = spawn.get("point") or {}
        if "x" not in point or "z" not in point:
            continue
        stand = f"{int(point['x'])},{int(point['z'])}"
        # A spawn point is inside its room, so the eye stands four blocks out of the room's first door.
        box, doors = spawn.get("footprint"), spawn.get("doors") or []
        if box and doors:
            middle_x, middle_z = (box["minX"] + box["maxX"]) // 2, (box["minZ"] + box["maxZ"]) // 2
            stand = {"+z": f"{middle_x},{box['maxZ'] + 4}", "-z": f"{middle_x},{box['minZ'] - 4}",
                     "+x": f"{box['maxX'] + 4},{middle_z}", "-x": f"{box['minX'] - 4},{middle_z}"}.get(doors[0], stand)
        if spawn.get("team") in goals:
            gx, gz = goals[spawn["team"]]
            views.append((f"eye-spawn-{index}.png", f"from={stand}&look={gx},{gz}"))
    for owner, (gx, gz) in goals.items():
        views.append((f"eye-goal-{owner}.png", f"look={gx},{gz}"))
    placed = [prop for prop in ((layout.get("dressing") or {}).get("props") or [])
              if prop.get("kind") in ("boulder", "house") and prop.get("x") is not None and prop.get("z") is not None]
    for prop in placed[:4]:
        views.append((f"eye-{prop['kind']}-{prop.get('id', len(views))}.png", f"look={int(prop['x'])},{int(prop['z'])}"))
    return views


def renders(into, slug, layout, drawn, flow, round_drawn, intent=None):
    """Every picture the studio drew for what was authored, written to disk, and the board in the round
    that `in_the_round` drew beside them — `round_drawn` is the future it answers on.

    Taking a picture is not the same as looking at one. What this removes is the excuse."""
    os.makedirs(into, exist_ok=True)
    written = []

    for name, text_body in (("00-board.txt", drawn), ("01-flow.txt", flow)):
        if text_body:
            with open(os.path.join(into, name), "w") as handle:
                handle.write(text_body)
            written.append(name)

    for name, method, path, body in pictures(slug, layout, intent):
        status, payload = call(method, path, body, raw=True, fatal=False)
        if status >= 300 or not isinstance(payload, bytes):
            continue
        with open(os.path.join(into, name), "wb") as handle:
            handle.write(payload)
        written.append(name)

    if round_drawn is not None:
        lines, drawn_round = round_drawn.result()
        for line in lines:
            print(line)
        written += drawn_round

    print(f"    {len(written)} render(s) -> {into}")
    return written


def in_the_round(columns, into, slug, layout):
    """The board in the round, drawn from the `sketch/columns` answer: two isometrics, the void scan and,
    where there is a room worth seeing, the x-ray. Returns the lines to print and the files written, and
    prints nothing itself — it is drawn beside the run's reads rather than after them.

    Every read the studio answers is a plan — a diagram of one question, drawn from above — and a plan
    cannot say whether a thing has the bulk it should: a ship is a ship-shaped patch of planks until it is
    seen with its masts up. The picture is drawn here rather than fetched because the studio answers
    columns, not cameras; `tools/render/iso.py` turns the one into the other, off the same payload the
    decline list was read from, so what is drawn is what was built."""
    lines, written = [], []
    if not (isinstance(columns, dict) and columns.get("cols")):
        return lines, written
    os.makedirs(into, exist_ok=True)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
    import iso

    # The four views are independent pictures of one payload, so each is drawn in a process of its own —
    # spawned rather than forked, because this process has the run's reads in flight on other threads.
    views = concurrent.futures.ProcessPoolExecutor(
        max_workers=min(4, os.cpu_count() or 1), mp_context=multiprocessing.get_context("spawn"))
    with views:
        isometrics = [(name, views.submit(
            iso.isometric, columns, os.path.join(into, name), scale=3, margin=30, quarter=quarter,
            title=None, caption=f"{slug} - isometric, {'south-east' if quarter == 0 else 'south-west'}"))
            for name, quarter in (("world-iso.png", 0), ("world-iso-turned.png", 1))]

        # What the board holds that is covered — a chamber, a house interior, the air under a ledge — with
        # the blocks it lies between. The scan runs on every board because it costs one pass over a payload
        # already in hand and answers a question no other read does: `render/section` needs the coordinate
        # in advance and `world-iso` draws a gaol under a meadow as a meadow. A void marked SEALED is a
        # finding on its own — a space nothing can walk into.
        voids = iso.cavities(iso.voxels(columns))

        # And the x-ray, only where there is something in it to see. Below the floor the view draws the
        # same board the two isometrics already drew, one shade paler, which is a picture that costs a
        # reader a look and answers nothing.
        xrays = []
        if voids and voids[0]["cells"] >= XRAY_FLOOR:
            # The storeys the veil may not touch. A layer of `kind: "made"` is a made thing, and a made
            # thing standing in a room is the subject of the picture rather than what hides it — but it
            # stands between the camera and the air behind it like any other block, so the sight-line
            # rule cannot tell it from a ceiling. The document can, and this is the caller that holds it.
            made = [layer["id"] for layer in (layout.get("layers") or [])
                    if layer.get("kind") == "made" and layer.get("id")]
            xrays = [(name, views.submit(
                iso.xray, columns, os.path.join(into, name), scale=3, margin=30, quarter=quarter,
                title=None, keep=made or None))
                for name, quarter in (("world-xray.png", 0), ("world-xray-turned.png", 1))]

        for name, drawn in isometrics:
            blocks, faces, size = drawn.result()
            written.append(name)
            lines.append(f"  ISO   {name:<44} {blocks} blocks, {faces} drawn, {size[0]}x{size[1]} px")
        for entry in voids[:6]:
            lines.append(f"  VOID  {entry['cells']:>6} cells  {'SEALED' if entry['sealed'] else 'open  '}  "
                         f"x {entry['min'][0]}..{entry['max'][0]}  y {entry['min'][1]}..{entry['max'][1]}  "
                         f"z {entry['min'][2]}..{entry['max'][2]}")
        lines.append(f"  VOID  {len(voids)} roofed void(s), "
                     f"{sum(1 for entry in voids if entry['sealed'])} of them sealed")
        for name, drawn in xrays:
            drawn.result()
            written.append(name)
            lines.append(f"  XRAY  {name:<44} veiled to the largest of {len(voids)} void(s)")
    return lines, written


def headline(into):
    """The three numbers a board is wrong or right by, printed last, from the files just written.

    The text reads have been written beside the pictures since the pass existed and the run reports say
    they go unread: a picture is one look and a 90 × 200 character grid is a question about which rows.
    So the run ends with the three lines that need no slicing — how much of the ground steps further
    than a player walks, whether every prop the document names is in the world, and the worst step on
    any route between a spawn and a goal. Each names the file the rest of the answer is in."""
    def line(name, match, fallback=None):
        try:
            with open(os.path.join(into, name)) as handle:
                rows = [row.rstrip("\n") for row in handle]
        except OSError:
            return None
        hit = [row for row in rows if match(row)]
        return hit[-1].strip() if hit else fallback

    slopes = line("03-slopes.txt", lambda row: row.startswith("cells:"))
    claims = line("06-claims.txt", lambda row: row.startswith("placed "))
    worst, route = 0, None
    try:
        with open(os.path.join(into, "04-routes.txt")) as handle:
            heading = None
            for row in handle:
                if row.startswith("## "):
                    heading = row[3:].strip()
                elif "worst step" in row:
                    step = re.search(r"worst step (\d+)", row)
                    if step and int(step.group(1)) >= worst:
                        worst, route = int(step.group(1)), f"{heading}: {row.split(':', 1)[-1].strip()}"
    except OSError:
        pass
    print("== the three numbers, before the pictures")
    print(f"  03-slopes.txt   {slopes or 'not written'}")
    print(f"  06-claims.txt   {claims or 'not written'}")
    print(f"  04-routes.txt   {route or 'no route between a spawn and a goal'}")


def text_reads(into, slug, intent, layout):
    """The board as text, beside the pictures: the API's own text reads — the heightmap, the slope grid,
    the two axis sections, the theme census and the dressing pass's claims — and, at an extent the
    documents decide, a transect through every feature and a profile along every route. A picture asks a
    reader to gauge a height; these state it, so a wall, a floor over falling ground or a step a player
    cannot walk is a number to subtract rather than a shade to estimate. The summaries are printed here;
    the files carry every station."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
    import textreads

    def fetch(method, path, body=None):
        status, payload = call(method, path, body, raw=True, fatal=False)
        return payload.decode("utf-8", "replace") if isinstance(payload, bytes) and status < 300 else None

    written, summaries = textreads.write_all(into, slug, intent, layout, fetch, ahead=ahead)
    for line in summaries:
        print(line)
    print(f"    {len(written)} text read(s) -> {into}")
    return written


def sweep(into, written):
    """**What this run did NOT write goes.** The pictures are keyed by what the board holds — a theme per id,
    a house per distinct style, a transect per feature — so a theme renamed, a style dropped or a prop
    removed would leave its old picture beside the new ones, and a README would go on pointing at it. A
    subdirectory is not touched, which is where a hand-taken picture belongs."""
    swept = [name for name in sorted(os.listdir(into))
             if os.path.isfile(os.path.join(into, name)) and name not in set(written)]
    for name in swept:
        os.remove(os.path.join(into, name))
    if swept:
        print(f"    swept {len(swept)}: {', '.join(swept)}")


def resolved(refinement):
    """The refinement as the studio takes it: every `@name` room style and house style loaded from
    tools/styles/. The rest is sent as the spec states it."""
    refinement = json.loads(json.dumps(refinement))
    if "roomStyles" in refinement:
        refinement["roomStyles"] = {part: resolve(style) for part, style in refinement["roomStyles"].items()}
    for prop in (refinement.get("dressing") or {}).get("props", []):
        if prop.get("kind") == "house":
            prop["style"] = resolve(prop.get("style", {}))
    return refinement


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
        print(f"    a new map: {len(edits)} member(s) of its plan, layout and intent stated for the first time")
        return
    if not edits:
        print("    nothing changed: the map already held what the spec states")
        return
    print(f"    {len(edits)} edit(s) to what the map held:")
    for edit in edits[:40]:
        print(f"      {edit.get('document'):7} {edit.get('op'):6} {edit.get('path')}  {edit.get('says')}")
    if len(edits) > 40:
        print(f"      … and {len(edits) - 40} more — GET /map/{{slug}}/diff?format=text has them all")


def main():
    specdir, name = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    into = sys.argv[sys.argv.index("--renders") + 1] if "--renders" in sys.argv else None
    note = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None
    after = int(sys.argv[sys.argv.index("--after") + 1]) if "--after" in sys.argv else None
    discard = sys.argv[sys.argv.index("--discard") + 1] if "--discard" in sys.argv else None
    dry = "--dry" in sys.argv
    base = os.path.basename(specdir.rstrip("/"))
    slug = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else base
    with open(f"{specdir}/{base}.plan.json") as handle:
        plan = json.load(handle)
    # A board drawn in the Sketch tool has no refinement: its geometry IS the layout, authored by hand
    # and not derivable from the plan. Such a spec carries `<base>.layout.json` and `<base>.intent.json`
    # instead, and the studio stores them as they are rather than compiling the plan over the top of
    # them. Everything after the store -- the grid, the flow, the declines and every render -- is the
    # same for both shapes of spec, which is the whole reason this branch is here rather than in a
    # second driver.
    #
    # **The refinement is what decides which shape this spec is, and it has to be**: the run ends by
    # writing the layout and intent the studio stored back into the spec directory, under exactly the
    # names a drawn spec uses. Reading those back as a drawing on the next run would apply the refinement
    # a second time, and `addLayers`, `addShapes` and `bendShapes` are all appends -- two storeys called
    # 'under', a ring bent twice. So a spec with a refinement is compiled from its plan every run, and the
    # layout beside it is the run's output rather than its input.
    refinement = {}
    if os.path.exists(f"{specdir}/{base}.refinement.json"):
        with open(f"{specdir}/{base}.refinement.json") as handle:
            refinement = json.load(handle)
    drawn_layout = drawn_intent = None
    if not refinement and os.path.exists(f"{specdir}/{base}.layout.json") \
            and os.path.exists(f"{specdir}/{base}.intent.json"):
        with open(f"{specdir}/{base}.layout.json") as handle:
            drawn_layout = json.load(handle)
        with open(f"{specdir}/{base}.intent.json") as handle:
            drawn_intent = json.load(handle)
    if not refinement and drawn_layout is None:
        raise SystemExit(f"{specdir}: needs {base}.refinement.json, or a drawn {base}.layout.json "
                         f"and {base}.intent.json beside the plan")

    # ── read the board before anything exists ────────────────────────────────────────────────
    print("== the board, before a map row exists")
    _, evaluated = call("POST", "/plan/evaluate", plan, fatal=False)
    print(f"    score {evaluated.get('score')}  valid {evaluated.get('valid')}")
    report(evaluated)
    _, inspected = call("POST", "/plan/inspect", plan, fatal=False)
    goal_ratio = wants("goal-spawn-ratio", "GO1")
    for goal in inspected.get("goalDistances") or []:
        print(f"    goal {goal.get('id')} ({goal.get('kind')}): own {goal.get('ownSpawnBlocks')} "
              f"enemy {goal.get('enemySpawnBlocks')} ratio {goal.get('ratio')}   {goal_ratio}")
    for gap in inspected.get("islandGaps") or []:
        print(f"    group gap: {json.dumps(gap)}   (CT12: {rule_claim('CT12')})")
    for run in inspected.get("frontlineRuns") or []:
        print(f"    frontline run: {json.dumps(run)}")
    for structure in inspected.get("structures") or []:
        if structure.get("kind") == "wall":
            print(f"    wall: {json.dumps(structure)}")

    # ── the map, from its source ─────────────────────────────────────────────────────────────
    # One call compiles the plan, applies the refinement onto what it compiled to — the outlines reshaped
    # and bent in the document — stores the three documents as one change, rasterizes the drawing,
    # projects the intent and applies the authors. The slug is stated rather than minted, so a spec
    # re-driven after a correction replaces the map it had instead of leaving a second one beside it.
    source = {"name": name, "plan": plan, "origin": origin(specdir), "note": note, "after": after}
    if drawn_layout is not None:
        source.update(layout=drawn_layout, intent=drawn_intent)
    else:
        source["refinement"] = resolved(refinement)
    # A change the spec has not seen — a hand edit in the Sketch tool, another writer's source — refuses the
    # run 409, printed above with the edit each SR1 hands over; `--after` takes it in, `--discard` drops it.
    dropping = f"discard={urllib.parse.quote(discard)}" if discard else ""
    if dry:
        print("== what the run would change, stored nowhere")
        _, would = call("PUT", f"/map/{slug}/source?dry=true{'&' + dropping if dropping else ''}", source)
        changed(would)
        raise SystemExit(0)
    print("== the map, from its source")
    _, stored = call("PUT", f"/map/{slug}/source{'?' + dropping if dropping else ''}", source)
    print(f"    slug={slug}  change {stored.get('change')}  "
          f"{'replaced' if stored.get('replaced') else 'new'}  "
          f"cells={stored.get('cells')}  islands={stored.get('islands')}")
    changed(stored)

    # Everything below reads the board as the studio stored it: the previews take the layout as a body,
    # the pictures are keyed on what it holds, and the spec's own copy is written out from it.
    _, layout = call("GET", f"/map/{slug}/sketch")
    _, intent = call("GET", f"/map/{slug}/intent")
    painted = collections.Counter(shape.get("theme") or layout.get("mapTheme")
                                  for layer in layout.get("layers") or []
                                  for shape in layer["layout"]["shapes"] if shape.get("role") is None)
    print(f"    themes on shapes: {dict(painted)}")
    if not (intent.get("meta") or {}).get("created"):
        print("    ! nothing states a `created` date, so the map will carry no <created> element")

    # ── everything wrong with the stored map, including what no other read answers ───────────
    # `Findings.Complaints` keeps `Severity.Complaint` alone, and `SK9` is the one `Severity.Decline`
    # the sketch layout check raises — so the gate that knows a storey is missing reaches no other
    # route: not the store above, not `sketch/columns`, not `relief/read`, not the `Pgm-Warnings`
    # header. A stacked board can store at 200, raise nothing anywhere, open the export gate, and have
    # a floor that is not in the world with a wall bridging the trench where it was. This read is the
    # only one that says so, which is why it is asked on every run.
    # Every read from here to the end asks the stored board, and nothing below writes to it, so they are
    # all sent now and the studio answers them side by side; each is still printed where it is asked.
    render_dir = into or os.path.join(specdir, "renders")
    ahead([("GET", f"/map/{slug}/findings"), ("GET", f"/map/{slug}/plan/ascii"),
           ("GET", f"/map/{slug}/plan/flow"), ("POST", f"/map/{slug}/sketch/relief/read", layout),
           ("POST", f"/map/{slug}/sketch/columns", layout), ("GET", f"/map/{slug}/preflight"),
           ("GET", f"/map/{slug}/coverage"), ("GET", f"/map/{slug}/export")]
          + ([(method, path, body) for _, method, path, body in pictures(slug, layout, intent)] if out else []))

    print("== everything wrong with the stored map")
    _, verdict = call("GET", f"/map/{slug}/findings", fatal=False)
    if findings(verdict):
        report(verdict)
    else:
        print("    nothing")
    for gate in (verdict.get("unasked") or []):
        print(f"    not judged yet: {gate.get('gate'):16} -> {gate.get('ask')}")

    # ── the board as a grid, and how it is come at ───────────────────────────────────────────
    # Two reads that cost no build and raise no finding, which is exactly why they are easy to forget.
    # Both read the STORED plan, so they sit after the store rather than at the first step.
    #
    # The grid is the only render a caller with no image reader can act on, and it answers what no
    # picture of a built world can: a plan is a list of rectangles measured in cells, and most of what
    # goes wrong with one is a RELATION between two of them — a landform wider than the band that
    # reaches it, a wall on the only throat. A grid puts the two on the same rows. The flow says why
    # ground is dead where the coverage read at the end says only that it is.
    print("== the board as a grid, and how it is come at")
    drawn = flow = None
    if (drawn := grid(slug)) is not None:
        print(drawn.rstrip("\n"))
    if (flow := text(f"/map/{slug}/plan/flow")) is not None:
        print(flow.rstrip("\n"))

    # ── look at the ground that was built ────────────────────────────────────────────────────
    print("== the ground, read back")
    _, read = call("POST", f"/map/{slug}/sketch/relief/read", layout)
    for group in read.get("groups") or []:
        print(f"    group {group.get('group') or group.get('id')}: cells={group.get('cells')} "
              f"low={group.get('low')} high={group.get('high')} "
              f"relief={group.get('relief')} symErr={group.get('symmetryError')}")
    if layout.get("relief") and not read.get("groups"):
        raise SystemExit("    relief/read answered no groups and a relief was stated — the shapes are "
                         "drawing no ground. Read the SK3/SK4 complaints on the store above: SK3 "
                         "names something the document names and the studio does not have, SK4 a shape "
                         "with no area. Stop.")

    # ── every prop the dressing pass declined ────────────────────────────────────────────────
    # DR-KEEP reads the spawn door's approach and the goal rings, which the intent carries — so this is
    # asked after the store, where a map carrying only a sketch would answer a shorter list.
    print("== what the dressing pass declined")
    _, columns = call("POST", f"/map/{slug}/sketch/columns", layout, fatal=False)
    if not (columns.get("warnings") if isinstance(columns, dict) else None):
        print("    nothing declined")
    # The board in the round is drawn from these columns while the reads below are answered — unless the
    # pictures go inside the world directory, which the export clears first.
    drawer = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    inside_out = out and os.path.commonpath([os.path.abspath(render_dir), os.path.abspath(out)]) \
        == os.path.abspath(out)
    round_drawn = drawer.submit(in_the_round, columns, render_dir, slug, layout) \
        if out and not inside_out else None

    # ── the export's own verdict, before the export ──────────────────────────────────────────
    # `GET /export` refuses a board it cannot walk with EX1, at 409, after the whole world is built.
    # Pre-flight runs that same `Traversability.Check` — per-team, so a goal behind an oversized spawn
    # protection is named with the team it bars — plus the codec round-trip, the mirror and buildability,
    # and says outright whether the export gate is open. The verdict is the same one; only the cost of
    # hearing it differs.
    print("== the export gate, asked before the export")
    _, preflight = call("GET", f"/map/{slug}/preflight", fatal=False)
    for line in (preflight.get("log") or []):
        print(f"    {line}")
    for isolated in ((preflight.get("traversability") or {}).get("isolated") or []):
        barred = f" (for {isolated['for']})" if isolated.get("for") else ""
        print(f"    isolated: {isolated.get('kind')} {isolated.get('name')}{barred}")
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
    else:
        # Silence here reads as "nothing dead", which is the opposite of what it means: the walk found
        # no route to class the ground against, so the share was never computed.
        print(f"    no routes to walk, so no dead share — {coverage.get('groundCells', 0)} ground cells "
              f"unclassed. A board with no two waypoints to join carries no traffic to read.")
    _, zip_bytes = call("GET", f"/map/{slug}/export", raw=True)
    if out:
        if os.path.isdir(out):
            shutil.rmtree(out)          # B102: never export over a region dir that was not cleared
        os.makedirs(out)
        zipfile.ZipFile(io.BytesIO(zip_bytes)).extractall(out)
        # The archive wraps the world in a directory named for the slug. `--out` is the world directory
        # itself — region/, level.dat, map.xml at its top — so the wrapper is unwrapped rather than left
        # for a caller to notice, which is what a slug that drifted between runs makes easy to miss.
        held = os.listdir(out)
        if len(held) == 1 and os.path.isdir(os.path.join(out, held[0])):
            wrapper = os.path.join(out, held[0])
            for entry in os.listdir(wrapper):
                shutil.move(os.path.join(wrapper, entry), os.path.join(out, entry))
            os.rmdir(wrapper)
        print(f"    world -> {out}")
        # The world directory holds what a server loads and nothing else: region/, level.dat, map.xml.
        # The provenance sidecar is a read-back aid — which pass claimed which column — so it travels
        # with the documents rather than with the world a server is handed.
        recorded = os.path.join(out, "region", "provenance.json")
        if os.path.exists(recorded):
            shutil.move(recorded, os.path.join(specdir, "provenance.json"))
            print(f"    provenance -> {specdir}/provenance.json")
        # After the extraction, which clears the directory it writes into.
        print("== the pictures of what was authored")
        round_drawn = round_drawn or drawer.submit(in_the_round, columns, render_dir, slug, layout)
        written = renders(render_dir, slug, layout, drawn, flow, round_drawn, intent)
        # ── the same board as text, which is the shape a reader subtracts from rather than gauges ──
        print("== the board as text: transects through every feature, and the routes")
        written += text_reads(render_dir, slug, intent, layout)
        sweep(render_dir, written)
        headline(render_dir)
    # A compiled spec's documents are the run's output and are written beside its plan; a drawn spec's
    # are its input and are left exactly as authored, so re-driving one is byte-identical by
    # construction rather than by the refinement being empty.
    if drawn_layout is None:
        with open(f"{specdir}/{base}.layout.json", "w") as handle:
            json.dump(layout, handle, indent=1)
        with open(f"{specdir}/{base}.intent.json", "w") as handle:
            json.dump(intent, handle, indent=1)
    print(f"DONE slug={slug}")


if __name__ == "__main__":
    try:
        main()
    finally:
        # A run stopped by a refusal leaves reads it will never ask for; they are dropped, not waited on.
        _wire.shutdown(wait=False, cancel_futures=True)
