"""The built board as text, read off the API: a heightmap, a slope grid, two sections, a transect through
every feature, a profile along every route, the theme census and the dressing pass's claims — the reads a
model can subtract from, beside the pictures it can only gauge.

    python3 tools/render/textreads.py specs/<slug> [--into <dir>] [--slug <slug>] [--every N]

`drive.py` runs the same pass after every export and prints the summaries inline; this entry re-reads a
driven board without driving it again. Every grid is the studio's own answer on `?format=text` —
`render/heightmap`, `slopes`, `render/section`, `transect`, `walk`, `themes/census` and `sketch/dressing`
— so what a column carries, which layer drew it and what a goal keeps clear come from the build's own
record rather than from a sidecar. What this pass adds is the extent: a transect through every spawn,
goal, house, water prop, boulder and made thing on the board, its box taken from the documents, and a
route from every spawn to every goal, so the read whose extent is the feature's own is taken without
anyone asking for it.

A picture encodes a height as a shade and asks a reader to estimate it; a character grid states it, so two
neighbouring cells are subtracted rather than judged. Every file here states its scale and its key on its
first lines, and every step a player cannot walk is marked where it is rather than left to be noticed.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

# How far a transect overshoots a feature's own box on each side, so the approach to it is in the read.
OVERSHOOT = 8
# How far either side of a line the claims standing beside it are listed.
BESIDE = 2


def features(intent, layout):
    """Every thing on the board a transect is worth taking through: spawns, goals, houses, water, boulders,
    made things. Each as `(id, kind, (x0, z0, x1, z1))` in blocks."""
    found = []
    for spawn in intent.get("spawns") or []:
        rects = spawn.get("protection") or []
        point = spawn.get("point") or {}
        if rects:
            r = rects[0]
            box = (r["minX"], r["minZ"], r["maxX"], r["maxZ"])
        else:
            box = (point.get("x", 0) - 6, point.get("z", 0) - 6, point.get("x", 0) + 6, point.get("z", 0) + 6)
        found.append((f"spawn-{spawn.get('team')}", "spawn", box))
    for goal_id, kind, (x, z), _layer in goals(intent):
        found.append((goal_id, kind, (x - 4, z - 4, x + 4, z + 4)))
    for prop in (layout.get("dressing") or {}).get("props") or []:
        if prop.get("kind") == "house":
            corners = [c for wing in prop.get("wings") or [] for c in wing.get("corners") or []]
            if corners:
                xs = [c[0] for c in corners]
                zs = [c[1] for c in corners]
                found.append((prop["id"], "house", (min(xs), min(zs), max(xs), max(zs))))
        elif prop.get("kind") == "water":
            points = prop.get("points") or ([[prop["x"], prop["z"]]] if "x" in prop else [])
            if points:
                xs = [p[0] for p in points]
                zs = [p[1] for p in points]
                pad = int(prop.get("radius") or 4) + 2
                found.append((prop["id"], "water", (min(xs) - pad, min(zs) - pad, max(xs) + pad, max(zs) + pad)))
        elif prop.get("kind") == "boulder" and "x" in prop:
            found.append((prop["id"], "boulder", (prop["x"] - 4, prop["z"] - 4, prop["x"] + 4, prop["z"] + 4)))
    made = {}
    for layer in layout.get("layers") or []:
        if layer.get("kind") != "made":
            continue
        part = layer.get("part_of") or layer["id"]
        for shape in (layer.get("layout") or {}).get("shapes") or []:
            if "min_x" in shape and shape["min_x"] is not None:
                box = made.get(part)
                candidate = (shape["min_x"], shape["min_z"], shape["max_x"], shape["max_z"])
                made[part] = candidate if box is None else (min(box[0], candidate[0]), min(box[1], candidate[1]),
                                                             max(box[2], candidate[2]), max(box[3], candidate[3]))
    for part, box in made.items():
        found.append((part, "made", box))
    return [(feature_id, kind, tuple(int(round(v)) for v in box)) for feature_id, kind, box in found]


def goals(intent):
    """Every goal the intent states, as `(id, kind, (x, z), layer)` — the far end of every route, and the
    storey it stands on.

    A wool's position is its `spawn`: that is the pad the wool dispenses from, which is the place a raider
    walks to. It carries no `anchor`, so a board played for wools states its goals under a different key from
    a board played for monuments or cores.

    The `layer` rides along because `walk` takes `x,z,y` to pick which storey of a stacked column is meant,
    and without one a route to a goal on a viaduct is the route to the street under it."""
    found = []
    for kind in ("destroyables", "cores", "wools"):
        for goal in intent.get(kind) or []:
            at = goal.get("anchor") or goal.get("location") or goal.get("spawn") or goal.get("point") or {}
            if "x" not in at:
                continue
            unit = goal.get("color") or (goal.get("stamp") or {}).get("unit") or goal.get("name") or kind
            image = (goal.get("stamp") or {}).get("image", 0)
            found.append((f"{unit}-{image}", kind[:-1], (int(at["x"]), int(at["z"])), goal.get("layer")))
    return found


def storeys(layout):
    """Each layer's `base_y`, by the id a goal or a spawn names it with — what turns a `layer` into the `y`
    that picks a storey. A layer that named itself keeps its id; one that did not is under its position, the
    same name the studio gives it."""
    found = {}
    for at, layer in enumerate(layout.get("layers") or []):
        found[layer.get("id") or f"layer{at}"] = int(layer.get("base_y") or 0)
    return found


def at(point, layer, floors):
    """A `from=`/`to=` coordinate, carrying the storey where the thing names a layer the board has. The
    layer's own base is enough to pick it: a storey is the span above it, and naming any height inside one
    selects it."""
    x, z = point
    base = floors.get(layer) if layer else None
    return f"{x},{z}" if base is None else f"{x},{z},{base}"


def extent(heightmap_text):
    """The board's own extent off the heightmap's first line — `x a..b across, z c..d down` — which is what
    the axis sections and their sample step are cut to."""
    found = re.search(r"x (-?\d+)\.\.(-?\d+) across, z (-?\d+)\.\.(-?\d+) down", heightmap_text or "")
    return tuple(int(v) for v in found.groups()) if found else None


def summary_of(text):
    """The one line of a transect or a route a reader scans first: its totals and its events."""
    for line in (text or "").splitlines():
        if line.startswith("rises "):
            return line
    return (text or "").strip().splitlines()[0] if text else "(no answer)"


def write_all(into, slug, intent, layout, fetch, every=None):
    """Every text read, written into `into`, and the summaries returned for the drive to print.
    `fetch(method, path, body=None)` answers the API's `text/plain` body, or None."""
    os.makedirs(into, exist_ok=True)
    written, summaries = [], []
    step = f"&every={every}" if every else ""

    def put(name, text):
        if text is None:
            summaries.append(f"  {name}: no answer")
            return
        with open(os.path.join(into, name), "w") as handle:
            handle.write(text if text.endswith("\n") else text + "\n")
        written.append(name)

    heightmap = fetch("GET", f"/map/{slug}/render/heightmap?format=text{step}")
    put("02-heightmap.txt", heightmap)
    put("03-slopes.txt", fetch("GET", f"/map/{slug}/slopes?format=text{step}"))

    board = extent(heightmap)
    if board:
        x0, x1, z0, z1 = board
        cut_every = max(1, math.ceil(max(x1 - x0, z1 - z0) / 200))
        put("world-section-x0.txt",
            fetch("GET", f"/map/{slug}/render/section?axis=x&at=0&from={z0}&to={z1}&every={cut_every}&format=text"))
        put("world-section-z0.txt",
            fetch("GET", f"/map/{slug}/render/section?axis=z&at=0&from={x0}&to={x1}&every={cut_every}&format=text"))

    def within(x, z):
        """A point held inside the board's own extent — a transect through a feature at the edge would
        otherwise overshoot into cells the world has no chunk for, which the read refuses."""
        if not board:
            return x, z
        return min(max(x, board[0]), board[1]), min(max(z, board[2]), board[3])

    for feature_id, kind, (bx0, bz0, bx1, bz1) in features(intent, layout):
        cx, cz = (bx0 + bx1) // 2, (bz0 + bz1) // 2
        (xa, za), (xb, zb) = within(bx0 - OVERSHOOT, cz), within(bx1 + OVERSHOOT, cz)
        along_x = fetch("GET", f"/map/{slug}/transect?points={xa},{za};{xb},{zb}&beside={BESIDE}&format=text")
        (xa, za), (xb, zb) = within(cx, bz0 - OVERSHOOT), within(cx, bz1 + OVERSHOOT)
        along_z = fetch("GET", f"/map/{slug}/transect?points={xa},{za};{xb},{zb}&beside={BESIDE}&format=text")
        if along_x is None and along_z is None:
            summaries.append(f"  {feature_id:18} no answer")
            continue
        body = "\n".join(f"## {feature_id} ({kind}) {title}\n{text}"
                         for title, text in (("along x", along_x), ("along z", along_z)) if text)
        put(f"transect-{feature_id}.txt", body)
        summaries.append(f"  {feature_id:18} along x: {summary_of(along_x)}")
        summaries.append(f"  {'':18} along z: {summary_of(along_z)}")

    routes = []
    floors = storeys(layout)
    for spawn in intent.get("spawns") or []:
        point = spawn.get("point") or {}
        if "x" not in point:
            continue
        start = at((int(point["x"]), int(point["z"])), spawn.get("layer"), floors)
        for goal_id, _kind, where, layer in goals(intent):
            text = fetch("GET", f"/map/{slug}/walk?from={start}&to={at(where, layer, floors)}"
                                f"&beside={BESIDE}&format=text")
            if text is None:
                continue
            routes.append(f"## spawn-{spawn.get('team')} -> {goal_id}\n{text}")
            summaries.append(f"  spawn-{spawn.get('team')} -> {goal_id}: {summary_of(text)}")
    if routes:
        put("04-routes.txt", "\n".join(routes))

    put("05-themes.txt", fetch("GET", f"/map/{slug}/themes/census?format=text"))
    put("06-claims.txt", fetch("POST", f"/map/{slug}/sketch/dressing?format=text", layout))
    return written, summaries


def api_text(method, path, body=None):
    """The API's `text/plain` answer, or None where the read refused — the status line is printed by the
    call either way, so a refusal is visible rather than absent."""
    import drive  # noqa: E402
    status, payload = drive.call(method, path, body, raw=True, fatal=False)
    return payload.decode("utf-8", "replace") if isinstance(payload, bytes) and status < 300 else None


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    specdir = sys.argv[1]
    base = os.path.basename(specdir.rstrip("/"))
    slug = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else base
    into = sys.argv[sys.argv.index("--into") + 1] if "--into" in sys.argv else os.path.join(specdir, "renders")
    every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else None
    with open(f"{specdir}/{base}.layout.json") as handle:
        layout = json.load(handle)
    with open(f"{specdir}/{base}.intent.json") as handle:
        intent = json.load(handle)
    written, summaries = write_all(into, slug, intent, layout, api_text, every)
    print("\n".join(summaries))
    print(f"{len(written)} text read(s) -> {into}: {', '.join(written)}")


if __name__ == "__main__":
    main()
