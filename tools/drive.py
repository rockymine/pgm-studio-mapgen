#!/usr/bin/env python3
"""Drive a plan + finish document through the pgm-studio API to an exported world, and say what the
pipeline said on the way.

    tools/drive.py <specdir> "<Map Name>" --out <worlddir> [--renders <dir>] [--slug <slug>] [--dry]

<specdir> holds <base>.plan.json and EITHER <base>.finish.json, OR a hand-drawn <base>.layout.json and
<base>.intent.json -- the shape the Sketch tool writes, whose geometry is authored rather than compiled.
The either/or is exact: a spec carrying a finish is compiled from its plan on every run, and the layout
and intent beside it are what the last run posted rather than anything it reads. A drawn spec's layout
and intent are its input and are never written over, so it states in its intent's own meta what a finish
would otherwise say about it -- `authors` and `created`. <base> is the directory's own name and, unless
--slug says otherwise, the slug the map is stored under. Both shapes take the same road from here: the
same grid, flow, declines and renders. The finish carries everything a plan cannot state, keyed onto the
compiled layout:

  themeByHeight   {"11": "gyp-bench", ...}   theme per compiled shape, by the height it stands at
  themeById       {"s3": "gyp-rake"}          theme per compiled shape id (wins over the height rule)
  shapePropsByHeight {"11": {"relief_scope": "exclude"}, ...}   fields merged onto a compiled shape
  shapePropsById  {"s3": {...}}
  bendShapes      {"s0": {"k": 0.22, "wander": 3, "step": 10, "seed": 5}}  the compiled outline drawn
                  as a coast: resampled along its long edges, each inserted point pulled inward by a
                  wander, and Bezier handles over the result. The plan's own vertices never move
  addShapes       [SketchShape, ...]          authored shapes appended to the first group
  addLayers       [{id, name, base_y, shapes, groups, below?, kind?, part_of?, seat?}]  stacked slabs;
                  `below` puts one under the compiled ground, where the painter's bottom-up order
                  needs it. `kind: "made"` marks a made thing — out of the stacking rules, painted
                  over its own span; `part_of` names the thing a run of layers is sliced from and `seat:
                  "ground"` settles them onto the terrain together
  relief          {"<groupId>": {...}} or {"*": {...}} applied to every group
  themes          the theme registry;  mapTheme  the map default (first key unless stated)
  biome           SketchLayout's own biome field: {"kind": "cell"|"noise"|"solid", ...}. The byte each
                  chunk carries, which tints grass, leaves and water. Absent is plains everywhere
  roomStyles      {"cage": ..., "spawn": ...}; a "@name" string loads tools/styles/<name>.json
  dressing        {"props": [...]};  a house prop's "style" takes the same "@name"
  goalLayers      {"destroyable-1": "under"}   which storey a goal stands on, by its plan marker id
  voidEnforcement true -> patch intent.build.voidEnforcement (voidExclusions for the rects to spare)
  authors         ["Opus 5"], or [{"name", "uuid", "role", "contribution"}] -> the <authors> block. PGM
                  takes a person as an account OR a pseudonym, so a bare name is a valid author
  created         "2026-08-25" -> intent.meta.created -> <created>. The studio cannot know when a map was
                  made and invents nothing, so a board that states none carries none

The whole map is stored in ONE call — POST /map/from-documents takes the plan, the patched layout and
the patched intent together, rasterizes the drawing, projects the intent into the map document and
applies the authors. The slug is stated, so re-driving a corrected spec REPLACES the map it had rather
than leaving a second one beside it, and a hand edit made in the Sketch tool between runs is replaced
rather than merged: the spec is what the map is.

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
        png(name, "GET", f"/map/{slug}/{route}")

    # And the board in the round. Every read above is a plan — a diagram of one question, drawn from above —
    # and a plan cannot say whether a thing has the bulk it should: a ship is a ship-shaped patch of planks
    # until it is seen with its masts up. The picture is drawn here rather than fetched because the studio
    # answers columns, not cameras; `tools/render/iso.py` turns the one into the other, off the same payload
    # the decline list was read from, so what is drawn is what was built.
    _, columns = call("POST", f"/map/{slug}/sketch/columns", layout, fatal=False)
    if isinstance(columns, dict) and columns.get("cols"):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "render"))
        import iso
        for name, quarter in (("world-iso.png", 0), ("world-iso-turned.png", 1)):
            blocks, faces, size = iso.isometric(
                columns, os.path.join(into, name), scale=3, margin=30, quarter=quarter,
                title=None, caption=f"{slug} - isometric, {'south-east' if quarter == 0 else 'south-west'}")
            written.append(name)
            print(f"  ISO   {name:<44} {blocks} blocks, {faces} drawn, {size[0]}x{size[1]} px")

        # What the board holds that is covered — a chamber, a house interior, the air under a ledge — with
        # the blocks it lies between. The scan runs on every board because it costs one pass over a payload
        # already in hand and answers a question no other read does: `render/section` needs the coordinate
        # in advance and `world-iso` above draws a gaol under a meadow as a meadow. A void marked SEALED is
        # a finding on its own — a space nothing can walk into.
        voids = iso.cavities(iso.voxels(columns))
        for entry in voids[:6]:
            print(f"  VOID  {entry['cells']:>6} cells  {'SEALED' if entry['sealed'] else 'open  '}  "
                  f"x {entry['min'][0]}..{entry['max'][0]}  y {entry['min'][1]}..{entry['max'][1]}  "
                  f"z {entry['min'][2]}..{entry['max'][2]}")
        print(f"  VOID  {len(voids)} roofed void(s), "
              f"{sum(1 for entry in voids if entry['sealed'])} of them sealed")
        # And the x-ray, only where there is something in it to see. Below the floor the view draws the
        # same board the two isometrics already drew, one shade paler, which is a picture that costs a
        # reader a look and answers nothing.
        if voids and voids[0]["cells"] >= XRAY_FLOOR:
            # The storeys the veil may not touch. A layer of `kind: "made"` is a made thing, and a made
            # thing standing in a room is the subject of the picture rather than what hides it — but it
            # stands between the camera and the air behind it like any other block, so the sight-line
            # rule cannot tell it from a ceiling. The document can, and this is the caller that holds it.
            made = [layer["id"] for layer in (layout.get("layers") or [])
                    if layer.get("kind") == "made" and layer.get("id")]
            for name, quarter in (("world-xray.png", 0), ("world-xray-turned.png", 1)):
                iso.xray(columns, os.path.join(into, name), scale=3, margin=30, quarter=quarter,
                         title=None, keep=made or None)
                written.append(name)
                print(f"  XRAY  {name:<44} veiled to the largest of {len(voids)} void(s)")

    print(f"    {len(written)} render(s) -> {into}")
    return columns, written


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

    written, summaries = textreads.write_all(into, slug, intent, layout, fetch)
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
    shapes, groups = inner["shapes"], inner["groups"]
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
        groups[0]["shapeIds"].append(extra["id"])
    if finish.get("addShapes"):
        print(f"    +{len(finish['addShapes'])} authored shapes onto group '{groups[0]['id']}'")
    for extra in finish.get("addLayers") or []:
        layers = layout["layers"]
        slab = {"id": extra["id"], "name": extra.get("name") or extra["id"],
                "base_y": extra["base_y"],
                # What the layer holds, and how it meets the ground. A made thing states `kind: "made"`,
                # which takes it out of the stacking rules and paints it over its own span; `part_of` names the
                # thing its layers belong to, and `seat` settles them onto the terrain as a unit.
                **{key: extra[key] for key in ("kind", "part_of", "seat") if key in extra},
                "layout": {"shapes": extra["shapes"], "groups": extra["groups"]}}
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
              f"{len(extra['shapes'])} shape(s), {len(extra['groups'])} group(s)")

    relief = finish.get("relief")
    if relief:
        if "*" in relief:
            # `*` is the ground's, not the board's: it names every group the compile emitted, and a
            # key stated beside it — a layer added here — keeps its own.
            wildcard = {key: value for key, value in relief.items() if key != "*"}
            relief = {**{group["id"]: relief["*"] for group in groups}, **wildcard}
        layout["relief"] = relief
    themes = finish.get("themes")
    if themes:
        layout["themes"] = themes
        layout["mapTheme"] = finish.get("mapTheme") or next(iter(themes))
    if "biome" in finish:
        # A strict pass-through of `SketchLayout.biome`, which is the one top-level layout key a finish
        # could not state. The field is documented as raw JSON of type BiomeField -- `solid`, `cell` or
        # `noise`, keyed on `kind` -- and nothing here reads it, defaults it or validates it; the export
        # does that through BiomeScope. Absent is plains everywhere, which is what every board that
        # states none already exports as.
        layout["biome"] = finish["biome"]
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


def patch_intent(intent, finish):
    """Everything the finish says about the compiled intent.

    `created` is the map's own date, which the studio has no way to derive: it rides on the intent's meta
    and is the author's to state. `voidEnforcement` fills the board's void with the barrier PGM enforces,
    sparing the rects `voidExclusions` names. `goalLayers` names the storey a goal stands on, by the plan
    marker id it was stated under: a stacked board carries a surface per storey and a placement naming none
    takes the top, which on a roofed goal is the roof. The word is keyed onto every orbit image of the
    marker, because a goal and its mirror stand on the same storey."""
    if created := finish.get("created"):
        intent.setdefault("meta", {})["created"] = created
        print(f"    created {created}")
    elif (intent.get("meta") or {}).get("created"):
        print(f"    created {intent['meta']['created']}")
    else:
        print("    ! nothing states a `created` date, so the map will carry no <created> element")
    if finish.get("voidEnforcement"):
        intent.setdefault("build", {})["voidEnforcement"] = \
            {"exclusions": finish.get("voidExclusions", [])}
    for unit, layer in (finish.get("goalLayers") or {}).items():
        for kind in ("destroyables", "cores"):
            for goal in intent.get(kind) or []:
                if (goal.get("stamp") or {}).get("unit") == unit:
                    goal["layer"] = layer
        print(f"    goal '{unit}' stands on layer '{layer}'")
    return intent


def main():
    specdir, name = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    into = sys.argv[sys.argv.index("--renders") + 1] if "--renders" in sys.argv else None
    dry = "--dry" in sys.argv
    base = os.path.basename(specdir.rstrip("/"))
    slug = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else base
    with open(f"{specdir}/{base}.plan.json") as handle:
        plan = json.load(handle)
    # A board drawn in the Sketch tool has no finish: its geometry IS the layout, authored by hand and
    # not derivable from the plan. Such a spec carries `<base>.layout.json` and `<base>.intent.json`
    # instead, and the compile below is skipped rather than run over the top of them. Everything after
    # this point -- the grid, the flow, the declines and every render -- is the same for both shapes of
    # spec, which is the whole reason this branch is here rather than in a second driver.
    #
    # **The finish is what decides which shape this spec is, and it has to be**: the run ends by writing
    # the layout and intent it posted back into the spec directory, under exactly the names a drawn spec
    # uses. Reading those back as a drawing on the next run would apply the finish a second time, and
    # `addLayers`, `addShapes` and `bendShapes` are all appends -- two storeys called 'under', a ring
    # bent twice. So a spec with a finish is compiled from its plan every run, and the layout beside it
    # is the run's output rather than its input.
    finish = {}
    if os.path.exists(f"{specdir}/{base}.finish.json"):
        with open(f"{specdir}/{base}.finish.json") as handle:
            finish = json.load(handle)
    drawn_layout = drawn_intent = None
    if not finish and os.path.exists(f"{specdir}/{base}.layout.json") \
            and os.path.exists(f"{specdir}/{base}.intent.json"):
        with open(f"{specdir}/{base}.layout.json") as handle:
            drawn_layout = json.load(handle)
        with open(f"{specdir}/{base}.intent.json") as handle:
            drawn_intent = json.load(handle)
    if not finish and drawn_layout is None:
        raise SystemExit(f"{specdir}: needs {base}.finish.json, or a drawn {base}.layout.json "
                         f"and {base}.intent.json beside the plan")

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
        print(f"    group gap: {json.dumps(gap)}   (CT12 wants 15-40 on a direct strait)")
    for run in inspected.get("frontlineRuns") or []:
        print(f"    frontline run: {json.dumps(run)}")
    for structure in inspected.get("structures") or []:
        if structure.get("kind") == "wall":
            print(f"    wall: {json.dumps(structure)}")
    if dry:
        raise SystemExit(0)

    # ── compile, and the finish a plan cannot state ──────────────────────────────────────────
    # The compile takes the plan itself and no map row, so both documents are whole before anything is
    # stored — which is what lets the store be one call.
    if drawn_layout is not None:
        print("== the drawn layout, taken as authored")
        layout, intent = drawn_layout, drawn_intent
        print(f"    {len(layout.get('layers') or [])} layer(s), "
              f"{sum(len(l['layout']['shapes']) for l in layout.get('layers') or [])} shape(s) — not compiled")
    else:
        print("== compile, and the finish")
        _, compiled = call("POST", "/plan/compile", plan)
        layout, intent = compiled["layout"], compiled["intent"]
    layout = patch_layout(layout, finish)
    intent = patch_intent(intent, finish)

    # ── the map, from the three documents it is made of ──────────────────────────────────────
    # One call stores the plan, rasterizes the drawing into geometry, projects the intent into the map
    # document and applies the authors. The slug is stated rather than minted, so a spec re-driven after
    # a correction replaces the map it had instead of leaving a second one beside it; the authors ride
    # in the body, so nothing has to be written after the projection that would overwrite them.
    print("== the map, from its three documents")
    _, loaded = call("POST", "/map/from-documents", {
        "slug": slug, "name": name, "plan": plan, "layout": layout, "intent": intent,
        # A drawn spec has no finish to state its authorship in, so it states it where the rest of what
        # it says about itself already lives: the intent's own meta.
        "authors": finish.get("authors") or (intent.get("meta") or {}).get("authors")})
    slug = loaded["slug"]
    print(f"    slug={slug}  {'replaced' if loaded.get('replaced') else 'new'}  "
          f"cells={loaded.get('cells')}  groups={loaded.get('groups')}")

    # ── everything wrong with the stored map, including what no other read answers ───────────
    # `Findings.Complaints` keeps `Severity.Complaint` alone, and `SK9` is the one `Severity.Decline`
    # the sketch layout check raises — so the gate that knows a storey is missing reaches no other
    # route: not the store above, not `sketch/columns`, not `relief/read`, not the `Pgm-Warnings`
    # header. A stacked board can store at 200, raise nothing anywhere, open the export gate, and have
    # a floor that is not in the world with a wall bridging the trench where it was. This read is the
    # only one that says so, which is why it is asked on every run.
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
    if finish.get("relief") and not read.get("groups"):
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
        pictures = into or os.path.join(specdir, "renders")
        _columns, written = renders(pictures, slug, finish, layout, drawn, flow)
        # ── the same board as text, which is the shape a reader subtracts from rather than gauges ──
        print("== the board as text: transects through every feature, and the routes")
        written += text_reads(pictures, slug, intent, layout)
        sweep(pictures, written)
    # A compiled spec's documents are the run's output and are written beside its plan; a drawn spec's
    # are its input and are left exactly as authored, so re-driving one is byte-identical by
    # construction rather than by the finish being empty.
    if drawn_layout is None:
        with open(f"{specdir}/{base}.layout.json", "w") as handle:
            json.dump(layout, handle, indent=1)
        with open(f"{specdir}/{base}.intent.json", "w") as handle:
            json.dump(intent, handle, indent=1)
    print(f"DONE slug={slug}")


if __name__ == "__main__":
    main()
