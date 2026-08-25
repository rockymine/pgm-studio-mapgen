#!/usr/bin/env python3
"""Drive a plan + finish document through the pgm-studio API to an exported world, and say what the
pipeline said on the way.

    tools/drive.py <specdir> "<Map Name>" --out <worlddir> [--renders <dir>] [--force] [--dry]

<specdir> holds <base>.plan.json and <base>.finish.json, where <base> is the directory's own name.
The plan is a PlanModel. The finish carries everything a plan cannot state, keyed onto the compiled
layout:

  themeByHeight   {"11": "gyp-bench", ...}   theme per compiled shape, by the height it stands at
  themeById       {"s3": "gyp-rake"}          theme per compiled shape id (wins over the height rule)
  shapePropsByHeight {"11": {"relief_scope": "exclude"}, ...}   fields merged onto a compiled shape
  shapePropsById  {"s3": {...}}
  bendShapes      {"s0": {"k": 0.22, "wander": 3, "step": 10, "seed": 5}}  the compiled outline drawn
                  as a coast: resampled along its long edges, each inserted point pulled inward by a
                  wander, and Bezier handles over the result. The plan's own vertices never move
  addShapes       [SketchShape, ...]          authored shapes appended to the first island
  addLayers       [{id, name, base_y, shapes, islands, below?}]  stacked slabs; `below` puts one
                  under the compiled ground, where the painter's bottom-up order needs it
  relief          {"<islandId>": {...}} or {"*": {...}} applied to every island
  themes          the theme registry;  mapTheme  the map default (first key unless stated)
  roomStyles      {"cage": ..., "spawn": ...}; a "@name" string loads tools/styles/<name>.json
  dressing        {"props": [...]};  a house prop's "style" takes the same "@name"
  goalLayers      {"destroyable-1": "under"}   which storey a goal stands on, by its plan marker id
  voidEnforcement true -> patch intent.build.voidEnforcement (voidExclusions for the rects to spare)
  authors         ["Opus 5"], or [{"name", "uuid", "role", "contribution"}] -> the <authors> block. PGM
                  takes a person as an account OR a pseudonym, so a bare name is a valid author

Nothing here computes a placement, a clearance or a validation: it posts documents and prints what
came back. Every finding the pipeline raises is printed with its rule id and the JSON path it is
about — a refusal's `findings`, the evaluator's `violations` and `lint`, and, on every 2xx, the
`warnings` a success carries. That last one is the half a driver reading only the status code throws
away: a decline says one piece of the posted document is not in the world, `RQ3` names a field that
went unread, and `SK3`/`SK4` name a shape that drew no ground. `GET /api/rules?rule=<id>` answers what
any of those means and how to fix it.

It also takes every picture the studio will draw for what was authored — a swatch per theme, a plan and a
section per house, the coverage map, the board read back from every angle, and the grid and flow as text —
into `<specdir>/renders`, or into `--renders <dir>`. Taking a picture is not the same as looking at one;
what it removes is the excuse.

The pictures and the provenance sidecar land beside the documents rather than in the exported world, because
`--out` is what a server is handed: it holds `region/`, `level.dat` and `map.xml`, and nothing a match does
not read.
"""
import json, math, sys, io, zipfile, urllib.request, urllib.error, os, shutil

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
STYLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")


def call(method, path, body=None, raw=False, fatal=True):
    """One request. Returns (status, payload). A non-2xx is printed with its findings and, unless
    fatal is False, stops the run — a refusal is a fault to fix, not a step to skip.

    A 2xx is printed with its `warnings` too, here rather than at the call sites, because a success is
    not a promise that everything posted survived: a decline says one piece of the document is not in
    the world, and `RQ3` names a field that went unread. The `Pgm-Warnings` header carries the same
    count and rule ids, so the status line says how much there is before the body is parsed."""
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=1800) as response:
            payload = response.read()
            carried = response.headers.get("Pgm-Warnings")
            print(f"  {method:5} {path:46} {response.status}"
                  f"{'   ! ' + carried if carried else ''}")
            if raw:
                return response.status, payload
            answered = json.loads(payload) if payload else {}
            complaints(answered)
            return response.status, answered
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


def text(path, fatal=False):
    """One GET whose answer is `text/plain` rather than a document — the grid and the flow account.
    Returns the body as a string, or None where the read failed; the status line is printed either
    way, so a read that 404s is visible rather than absent."""
    status, payload = call("GET", path, raw=True, fatal=fatal)
    return payload.decode("utf-8", "replace") if isinstance(payload, bytes) and status < 300 else None


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
        field = entry.get("field")
        print(f"{indent}  [{severity:9}] {rule:8} {message}"
              f"{'   @ ' + field if field else ''}")


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


def renders(into, slug, finish, layout, drawn, flow):
    """Every picture the studio will draw for what was authored, written to disk.

    The reads are the same ones the brief asks an author to look at, and the reason they are taken here is
    the reason the grid and the flow are printed here: a read nobody is refused for skipping is the read
    nobody takes. A theme swatch, a house in section and the coverage map each answer a question no
    top-down of the finished world can — and the section is the one every shipped roof fault was visible in.

    Taking a picture is not the same as looking at one. What this removes is the excuse."""
    os.makedirs(into, exist_ok=True)
    written = []

    def png(name, method, path, body=None):
        status, payload = call(method, path, body, raw=True, fatal=False)
        if status >= 300 or not isinstance(payload, bytes):
            return
        with open(os.path.join(into, name), "wb") as handle:
            handle.write(payload)
        written.append(name)

    for name, text_body in (("00-board.txt", drawn), ("01-flow.txt", flow)):
        if text_body:
            with open(os.path.join(into, name), "w") as handle:
                handle.write(text_body)
            written.append(name)

    # Two views a theme, because they answer different questions and neither substitutes. The section is
    # the column — rim over wall over fill, the pairing most easily got wrong. The surface is the swatch,
    # and it is the only view a pattern is legible in: a section through a voronoi is one block wide.
    for theme_id, theme in (finish.get("themes") or {}).items():
        for view in ("surface", "section"):
            png(f"theme-{theme_id}-{view}.png", "POST",
                f"/terrain/theme-preview?format=png&view={view}", theme)

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
            png(f"{house_id}-{view}.png", "POST",
                f"/room-styles/preview-snapshot?format=png&view={view}", json.loads(style_json))

    png("coverage.png", "GET", f"/map/{slug}/coverage?format=png")

    # The world itself, read back through the routes that answer it. These are the reads an author is meant
    # to look at after building and the ones nobody ever took, because until they answered over HTTP an agent
    # had to know a .NET binary existed. `column` is the workhorse and is not here: it answers one coordinate
    # and the coordinates worth asking about are the author's, not a driver's.
    for name, route in (
        ("world-topdown.png", "render/topdown"),
        ("world-ground.png", "render/topdown?layer=ground&material=1"),
        ("world-structure.png", "render/topdown?layer=structure"),
        ("world-foliage.png", "render/topdown?layer=foliage"),
        ("world-objectives.png", "render/topdown?layer=objectives"),
        ("world-heightmap.png", "render/heightmap"),
        ("world-surface.png", "render/surface"),
        ("world-traversability.png", "render/traversability"),
        ("world-mirror.png", "render/mirror"),
        ("world-section-x0.png", "render/section?axis=x&at=0&from=-120&to=120"),
        ("world-section-z0.png", "render/section?axis=z&at=0&from=-120&to=120"),
    ):
        png(name, "GET", f"/map/{slug}/{route}")

    print(f"    {len(written)} render(s) -> {into}")


def bend(ring, k=0.22, wander=3.0, step=10, seed=5):
    """A compiled outline drawn as a coast: the plan's own ring, resampled along its long edges, each
    inserted point pulled INWARD by a deterministic wander, and Catmull-Rom handles over the result.

    The compiler emits a staircase of the plan's rectangles, which is the board's shape and not its
    coast. Redrawing the ring by hand states the coast twice — once in the plan and once in the finish,
    free to disagree — so the bend is taken over whatever the compile produced instead.

    **Inward only, and never at a corner.** A point moved outward can cross the mirror line, close the
    strait a capture board is measured on, or leave the plan's own footprint; a corner moved at all
    narrows the neck a spur hangs off, which is the one width a branching board cannot spare. So the
    plan's vertices stay exactly where they are and only the points between them move, and only into
    the land: the coast can lose a few blocks and can never gain one.
    """
    n = len(ring)
    area = sum(ring[i][0] * ring[(i + 1) % n][1] - ring[(i + 1) % n][0] * ring[i][1] for i in range(n))
    inward = 1.0 if area > 0 else -1.0        # which side of an edge the interior is on
    drawn = []
    for i in range(n):
        (ax, az), (bx, bz) = ring[i], ring[(i + 1) % n]
        drawn.append([float(ax), float(az)])
        length = math.hypot(bx - ax, bz - az)
        cuts = int(length // step)
        if cuts < 2:
            continue
        nx, nz = (bz - az) / length * inward, -(bx - ax) / length * inward
        for c in range(1, cuts):
            t = c / cuts
            px, pz = ax + (bx - ax) * t, az + (bz - az) * t
            # Two sines of incommensurate period over the point's own place on the board, so the coast
            # never repeats and the script re-runs identical.
            noise = 0.5 + 0.5 * math.sin(px / 13.7 + seed) * math.sin(pz / 21.3 + seed * 1.7)
            drawn.append([round(px + nx * wander * noise, 1), round(pz + nz * wander * noise, 1)])
    controls = {}
    m = len(drawn)
    for i, (x, z) in enumerate(drawn):
        px, pz = drawn[(i - 1) % m]
        nx2, nz2 = drawn[(i + 1) % m]
        tx, tz = (nx2 - px) * k, (nz2 - pz) * k
        controls[str(i)] = {"in": [round(x - tx, 2), round(z - tz, 2)],
                            "out": [round(x + tx, 2), round(z + tz, 2)]}
    return drawn, controls


def patch_layout(layout, finish):
    """Everything the finish says about the compiled layout, applied in one pass."""
    # A compiled layout is a stack of one: `layers[0]` is the ground the plan drew, and there is no
    # `layout` key beside it any more. The finish keys onto that layer's shapes and appends the
    # storeys the plan cannot state above it.
    inner = layout["layers"][0]["layout"]
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
    for shape_id, how in (finish.get("bendShapes") or {}).items():
        shape = next((s for s in shapes if s["id"] == shape_id), None)
        if shape is None or not shape.get("vertices"):
            print(f"    ! bendShapes names '{shape_id}', which the compile did not produce as a polygon")
            continue
        before = len(shape["vertices"])
        shape["vertices"], shape["controls"] = bend(shape["vertices"], **how)
        print(f"    bent '{shape_id}': {before} compiled vertices -> {len(shape['vertices'])} drawn")

    for extra in finish.get("addShapes") or []:
        shapes.append(extra)
        islands[0]["shapeIds"].append(extra["id"])
    if finish.get("addShapes"):
        print(f"    +{len(finish['addShapes'])} authored shapes onto island '{islands[0]['id']}'")
    for extra in finish.get("addLayers") or []:
        layers = layout["layers"]
        slab = {"id": extra["id"], "name": extra.get("name") or extra["id"],
                "base_y": extra["base_y"],
                "layout": {"shapes": extra["shapes"], "islands": extra["islands"]}}
        # `below` puts a storey under the compiled ground rather than over it. The painter walks the
        # stack in document order and each pass paints its whole column, so a storey listed above one
        # that stands lower has already had its blocks claimed by the time its own pass runs: the
        # stack has to be written bottom-up, and the compiled ground is not the bottom of every board.
        if extra.get("below"):
            layers.insert(0, slab)
        else:
            layers.append(slab)
        print(f"    +layer '{extra['id']}' at base_y {extra['base_y']}"
              f"{' (below the compiled ground)' if extra.get('below') else ''}: "
              f"{len(extra['shapes'])} shape(s), {len(extra['islands'])} island(s)")

    relief = finish.get("relief")
    if relief:
        if "*" in relief:
            # `*` is the ground's, not the board's: it names every island the compile emitted, and a
            # key stated beside it — a layer added here — keeps its own.
            wildcard = {key: value for key, value in relief.items() if key != "*"}
            relief = {**{island["id"]: relief["*"] for island in islands}, **wildcard}
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
    into = sys.argv[sys.argv.index("--renders") + 1] if "--renders" in sys.argv else None
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

    # ── the board as a grid, and how it is come at ───────────────────────────────────────────
    # Two reads that cost no build and raise no finding, which is exactly why they are easy to forget.
    # They sit here rather than at the first step because both read the STORED plan: there is nothing
    # to ask before the PUT above. Neither is about the world — a compile has not happened yet.
    #
    # The grid is the only render a caller with no image reader can act on, and it answers what no
    # picture of a built world can: a plan is a list of rectangles measured in cells, and most of what
    # goes wrong with one is a RELATION between two of them — a landform wider than the band that
    # reaches it, a wall on the only throat. A grid puts the two on the same rows. The flow says why
    # ground is dead where the coverage read at the end says only that it is, and it says it before a
    # world exists to measure.
    print("== the board as a grid, and how it is come at")
    drawn = flow = None
    if (drawn := grid(slug)) is not None:
        print(drawn.rstrip("\n"))
    if (flow := text(f"/map/{slug}/plan/flow")) is not None:
        print(flow.rstrip("\n"))

    _, compiled = call("POST", "/plan/compile", plan)
    layout, intent = compiled["layout"], compiled["intent"]

    # ── the finish a plan cannot state ───────────────────────────────────────────────────────
    print("== the finish")
    layout = patch_layout(layout, finish)
    query = "?force=true" if force else ""
    _, stored = call("PUT", f"/map/{slug}/sketch/from-plan{query}", layout)

    # ── look at the ground before building it ────────────────────────────────────────────────
    print("== the ground, read back")
    _, read = call("POST", f"/map/{slug}/sketch/relief/read", layout)
    for island in read.get("islands") or []:
        print(f"    island {island.get('island') or island.get('id')}: cells={island.get('cells')} "
              f"low={island.get('low')} high={island.get('high')} "
              f"relief={island.get('relief')} symErr={island.get('symmetryError')}")
    if finish.get("relief") and not read.get("islands"):
        raise SystemExit("    relief/read answered no islands and a relief was stated — the shapes are "
                         "drawing no ground. Read the SK3/SK4 complaints on the sketch PUT above: SK3 "
                         "names a shape kind the studio does not draw, SK4 one with no area. Stop.")

    # ── build ────────────────────────────────────────────────────────────────────────────────
    print("== build")
    _, finished = call("POST", f"/map/{slug}/sketch/finish")
    if finish.get("voidEnforcement"):
        intent.setdefault("build", {})["voidEnforcement"] = \
            {"exclusions": finish.get("voidExclusions", [])}
    # A stacked board carries a surface per storey and a placement may say which one it rests on;
    # naming none takes the top, which on a roofed goal is the roof. The plan has no field for it,
    # so the word is keyed onto the compiled intent by the marker id the plan did state — and onto
    # every orbit image of it, because a goal and its mirror stand on the same storey.
    for unit, layer in (finish.get("goalLayers") or {}).items():
        for kind in ("destroyables", "cores"):
            for goal in intent.get(kind) or []:
                if (goal.get("stamp") or {}).get("unit") == unit:
                    goal["layer"] = layer
        print(f"    goal '{unit}' stands on layer '{layer}'")
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
    if not (columns.get("warnings") if isinstance(columns, dict) else None):
        print("    nothing declined")

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
        renders(into or os.path.join(specdir, "renders"), slug, finish, layout, drawn, flow)
    # the documents that were actually posted, beside the ones that were authored
    with open(f"{specdir}/{base}.layout.json", "w") as handle:
        json.dump(layout, handle, indent=1)
    with open(f"{specdir}/{base}.intent.json", "w") as handle:
        json.dump(intent, handle, indent=1)
    print(f"DONE slug={slug}")


if __name__ == "__main__":
    main()
