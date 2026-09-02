"""The built board as text: a heightmap, a slope grid, two sections, a transect through every feature and a
profile along every route — the reads a model can subtract from, beside the pictures it can only gauge.

    python3 tools/render/textreads.py specs/<slug> <worldDir> [--into <dir>] [--slug <slug>] [--every N]

`drive.py` runs the same pass after every export and prints the summaries inline; this entry re-reads a
driven board without driving it again. It reads the exported world (`tools/anvil.py`), the provenance
sidecar beside the spec, the intent and the layout the drive wrote, and asks the API for
`sketch/columns` (the ground under everything, per column) and `walk` (each team's route to each goal).

A picture encodes a height as a shade and asks a reader to estimate it; a character grid states it, so two
neighbouring cells are subtracted rather than judged. Every file here states its scale and its key on its
first lines, and every step a player cannot walk is marked where it is rather than left to be noticed.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from anvil import World, TREE, WOOD, WATER, PLANT  # noqa: E402

SCRAMBLE, BARRIER, FALL = 2, 3, 4          # a step of 2 wants a block, 3 is not climbed, 4 down is damage
BANDS = "0123456789abcdefghijklmnopqrstuvwxyz"
OWNER_CHAR = {"tree": "T", "boulder": "o", "house": "H", "water": "~", "stroke": "=", "flora": ",",
              "spawn": "S", "destroyable": "!", "core": "O", "wool": "W", "iron": "i"}


# ── what the drive already holds, decoded once ────────────────────────────────────────────────────────
def decode(payload):
    """Off `sketch/columns`: `{(x, z): ground y}` — the top of the runs the ground layer drew, which is the
    terrain under whatever stands on it; `{(x, z): [(y_top, y_bottom, layer)]}`, every run with the sketch
    layer that drew it (-1 for a thing standing on the board rather than being it); and `{(x, z): surface
    y}` — the top of the highest storey any layer drew, which is what a walker stands on where a deck spans
    a gill. Layer 0 is the compiled ground; a board built from no layer stack answers every run as -1, and
    then the topmost run is the best reading of the ground there is."""
    cols = payload.get("cols") or []
    layered = bool(payload.get("layers"))
    tops, runs, surfaces = {}, {}, {}
    i = 0
    while i < len(cols):
        x, z, count = cols[i], cols[i + 1], cols[i + 2]
        i += 3
        ground = surface = None
        held = []
        for _ in range(count):
            y_top, y_bottom, _slot, layer = cols[i:i + 4]
            i += 4
            held.append((y_top, y_bottom, layer))
            if (layer == 0) if layered else True:
                ground = y_top if ground is None else max(ground, y_top)
            if layer >= 0 or not layered:
                surface = y_top if surface is None else max(surface, y_top)
        if ground is not None:
            tops[(x, z)] = ground
        if surface is not None:
            surfaces[(x, z)] = surface
        runs[(x, z)] = held
    return tops, runs, surfaces


def claims(provenance_path):
    """`{(x, z): (pass, kind, unit)}` off the sidecar: which pass claimed each column and for what."""
    if not provenance_path or not os.path.exists(provenance_path):
        return {}
    with open(provenance_path) as handle:
        provenance = json.load(handle)
    owners = provenance["owners"]
    claimed = {}
    for run in provenance["runs"]:
        which = run.get("pass")
        owner = owners[run["owner"] - 1] if "owner" in run else None
        for x in range(run["MinX"], run["MaxX"] + 1):
            claimed[(x, run["Z"])] = (which, owner["kind"] if owner else None, owner["unit"] if owner else None)
    return claimed


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
    for kind in ("destroyables", "cores", "wools"):
        for goal in intent.get(kind) or []:
            at = goal.get("anchor") or goal.get("location") or goal.get("point") or {}
            if "x" not in at:
                continue
            unit = (goal.get("stamp") or {}).get("unit") or goal.get("name") or kind
            image = (goal.get("stamp") or {}).get("image", 0)
            found.append((f"{unit}-{image}", kind[:-1], (at["x"] - 4, at["z"] - 4, at["x"] + 4, at["z"] + 4)))
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


# ── the grids ─────────────────────────────────────────────────────────────────────────────────────────
def heightmap(tops, claimed, intent, every):
    """The ground as one character per `every` blocks: the height band above the board's lowest ground,
    with the spawns, goals, houses and water overprinted so a height is read beside what stands there."""
    if not tops:
        return "(no ground to draw)\n"
    xs = [x for x, _z in tops]
    zs = [z for _x, z in tops]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    low = min(tops.values())
    high = max(tops.values())
    band = max(1, math.ceil((high - low + 1) / len(BANDS)))
    marks = {}
    for (x, z), (which, kind, _unit) in claimed.items():
        if kind in ("house", "water", "destroyable", "core", "wool", "iron"):
            marks[(x, z)] = OWNER_CHAR[kind]
    for spawn in intent.get("spawns") or []:
        p = spawn.get("point") or {}
        if "x" in p:
            marks[(p["x"], p["z"])] = "@"
    for kind in ("destroyables", "cores", "wools"):
        for goal in intent.get(kind) or []:
            at = goal.get("anchor") or goal.get("location") or goal.get("point") or {}
            if "x" in at:
                marks[(at["x"], at["z"])] = "!"
    lines = [f"HEIGHTMAP  1 char = {every}x{every} blocks (the top-left block of each)  x {x0}..{x1} across, z {z0}..{z1} down",
             f"KEY  char = ground height above y{low} in bands of {band} block(s): 0 = y{low}..{low + band - 1}, "
             f"1 = y{low + band}.., ... ; H house  ~ water  @ spawn point  ! goal  space = void",
             "     " + "".join(str(abs(x) // 10 % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1, every))]
    for z in range(z0, z1 + 1, every):
        row = []
        for x in range(x0, x1 + 1, every):
            mark = next((marks[(x + dx, z + dz)] for dx in range(every) for dz in range(every) if (x + dx, z + dz) in marks), None)
            if mark:
                row.append(mark)
                continue
            y = tops.get((x, z))
            row.append(" " if y is None else BANDS[min(len(BANDS) - 1, (y - low) // band)])
        lines.append(f"{z:4} " + "".join(row))
    lines.append(f"low y{low}, high y{high}, range {high - low}")
    return "\n".join(lines) + "\n"


def slopes(tops, every):
    """Where the ground steps: per sampled cell the largest rise to a neighbour inside it — `.` walked (0-1),
    `:` scrambled with a block (2), `#` a barrier (3 or more), space void. Cliffs read as lines of #."""
    if not tops:
        return "(no ground to draw)\n"
    xs = [x for x, _z in tops]
    zs = [z for _x, z in tops]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    step = {}
    for (x, z), y in tops.items():
        worst = 0
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            other = tops.get((x + dx, z + dz))
            if other is not None:
                worst = max(worst, abs(other - y))
        step[(x, z)] = worst
    lines = [f"SLOPES  1 char = {every}x{every} blocks, the worst step to a neighbour inside it  x {x0}..{x1} across, z {z0}..{z1} down",
             f"KEY  . walked (rise 0-{SCRAMBLE - 1})  : scrambled with a block (rise {SCRAMBLE})  # barrier (rise {BARRIER}+)  space void",
             "     " + "".join(str(abs(x) // 10 % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1, every))]
    counts = {".": 0, ":": 0, "#": 0}
    for z in range(z0, z1 + 1, every):
        row = []
        for x in range(x0, x1 + 1, every):
            cells = [step.get((x + dx, z + dz)) for dx in range(every) for dz in range(every)]
            cells = [c for c in cells if c is not None]
            if not cells:
                row.append(" ")
                continue
            worst = max(cells)
            char = "#" if worst >= BARRIER else ":" if worst >= SCRAMBLE else "."
            counts[char] += 1
            row.append(char)
        lines.append(f"{z:4} " + "".join(row))
    lines.append(f"cells: {counts['.']} walked, {counts[':']} scrambled, {counts['#']} barrier")
    return "\n".join(lines) + "\n"


def section_char(block, y, ground, runs, claim):
    """One block of a cut as a character: what it is by its id, else which layer drew it, else whose column
    it stands in."""
    block_id = block[0]
    if block_id == 0:
        return "."
    if block_id in WATER:
        return "~"
    if block_id in WOOD:
        return "I"
    if block_id in TREE:
        return "T"
    if block_id == 7:
        return "X"
    if ground is not None and y <= ground:
        return "#"
    for y_top, y_bottom, layer in runs or ():
        if y_bottom <= y <= y_top and layer >= 1:
            return "L"
    which, kind, _unit = claim if claim else (None, None, None)
    if kind in ("house", "spawn", "destroyable", "core", "wool", "iron", "boulder"):
        return OWNER_CHAR[kind]
    if which == 1:
        return "H"
    if which == 2:
        return "M"
    return "o"


def section(world, tops, runs, claimed, axis, at, lo, hi, every=1):
    """A vertical cut as characters, one per block, from the highest block found down to the lowest, with a
    y axis on the left and the ground's height under each column beneath it."""
    stations = list(range(lo, hi + 1, every))
    cells = [(at, s) if axis == "x" else (s, at) for s in stations]
    columns = []
    for x, z in cells:
        col = [(y, i, d) for y, i, d in world.columns().get((x, z), [])]
        columns.append({y: (i, d) for y, i, d in col})
    ys = [y for col in columns for y in col]
    if not ys:
        return f"(nothing on the cut at {'x' if axis == 'x' else 'z'}={at})\n"
    top, bottom = max(ys) + 1, max(0, min(ys) - 1)
    other = "z" if axis == "x" else "x"
    lines = [f"SECTION  cut at {'x' if axis == 'x' else 'z'}={at}, {other} {lo}..{hi} across ({every} block per char), "
             f"y{top} at the top row down to y{bottom}",
             "KEY  # ground  L a storey over it  ~ water  I log  T leaves  H house or hall  M made thing  o prop  "
             "S spawn  ! goal  X bedrock  . air"]
    for y in range(top, bottom - 1, -1):
        row = []
        for (x, z), col in zip(cells, columns):
            row.append(section_char(col.get(y, (0, 0)), y, tops.get((x, z)), runs.get((x, z)), claimed.get((x, z))))
        label = f"y{y:3} " if y % 4 == 0 else "     "
        lines.append(label + "".join(row))
    axis_line = "".join(str(abs(s) // 10 % 10) if s % 10 == 0 else " " for s in stations)
    lines.append("     " + axis_line)
    ground_line = "".join(("." if tops.get(c) is None else BANDS[min(35, max(0, tops[c] - bottom))]) for c in cells)
    lines.append("grnd " + ground_line + f"   (ground height as a band above y{bottom}: 0-9, a-z)")
    return "\n".join(lines) + "\n"


def transect(tops, claimed, world_columns, cells, title, surfaces=None):
    """Along a line of cells: the ground under each, what stands on it, and the step from the one before,
    with every step a player cannot walk named where it is. The summary line is what the drive prints."""
    lines = [title, "  station        ground  top  standing            step"]
    previous = None
    rises = falls = barriers = scrambles = drops = 0
    worst = 0
    events = []
    for (x, z) in cells:
        ground = tops.get((x, z))
        storey = surfaces.get((x, z)) if surfaces else None
        if storey is not None and ground is not None and storey > ground:
            ground = storey
        column = world_columns.get((x, z), [])
        top = column[-1][0] if column else None
        claim = claimed.get((x, z))
        standing = ""
        if storey is not None and tops.get((x, z)) is not None and storey > tops[(x, z)]:
            standing = f"storey over y{tops[(x, z)]}"
        elif claim and claim[1]:
            standing = f"{claim[1]} {claim[2]}"
        elif top is not None and ground is not None and top > ground:
            standing = "something" if not any(i in TREE for _y, i, _d in column if _y > ground) else "tree"
        if column and any(i in WATER for _y, i, _d in column):
            standing = (standing + " " if standing else "") + "water"
        word = ""
        if ground is not None and previous is not None:
            delta = ground - previous
            if delta >= BARRIER:
                word = f"BARRIER +{delta}"
                barriers += 1
            elif delta >= SCRAMBLE:
                word = f"scramble +{delta}"
                scrambles += 1
            elif delta <= -FALL:
                word = f"DROP {delta}"
                drops += 1
            elif delta:
                word = f"{delta:+d}"
            rises += max(0, delta)
            falls += max(0, -delta)
            worst = max(worst, abs(delta))
            if word and (delta >= SCRAMBLE or delta <= -FALL):
                events.append(f"{word} at ({x},{z})")
        elif ground is None:
            word = "void"
        lines.append(f"  ({x:4},{z:4})   {'' if ground is None else ground:>5}  {'' if top is None else top:>3}  {standing:18} {word}")
        previous = ground if ground is not None else previous
    summary = (f"rises {rises}, falls {falls}, worst step {worst}: {barriers} barrier, {scrambles} scramble, "
               f"{drops} drop" + (f" — {'; '.join(events[:6])}" if events else " — walked end to end"))
    lines.append(f"  {len(cells)} stations: {summary}")
    return "\n".join(lines) + "\n", summary


def route_profile(tops, surfaces, claimed, world_columns, walk, from_id, to_id):
    """The walk's own route as a transect, plus what stands within two blocks of it: the read for a thing
    thrown in the way of the players."""
    cells = [(c[0], c[1]) for c in walk.get("cells") or []]
    if not cells:
        return f"route {from_id} -> {to_id}: no route\n", f"  {from_id} -> {to_id}: unreachable"
    body, summary = transect(tops, claimed, world_columns, cells,
                             f"ROUTE {from_id} -> {to_id} (aim {walk.get('aim')}): {walk.get('distance')} blocks, "
                             f"{walk.get('blocks')} placed, {walk.get('drops')} drop(s), worst drop {walk.get('worstDrop')} "
                             f"(the walk's own count)",
                             surfaces)
    summary = f"  route {from_id} -> {to_id}: {walk.get('distance')} blocks, {summary}"
    beside = {}
    for (x, z) in cells:
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                claim = claimed.get((x + dx, z + dz))
                if claim and claim[1] in ("tree", "boulder", "house", "water", "spawn", "destroyable", "core", "wool"):
                    beside.setdefault(f"{claim[1]} {claim[2]}", (x + dx, z + dz))
    if beside:
        body += "  within two blocks of the route: " + ", ".join(f"{k} at {v}" for k, v in beside.items()) + "\n"
        summary += f"; beside it: {', '.join(beside)}"
    return body, summary


# ── the pass ──────────────────────────────────────────────────────────────────────────────────────────
def write_all(into, world_dir, provenance_path, intent, layout, columns_payload, walk_for, every=None):
    """Every text read, written into `into` and the summaries returned for the drive to print.
    `walk_for(from_xz, to_xz)` answers the API's walk, or None."""
    os.makedirs(into, exist_ok=True)
    world = World(os.path.join(world_dir, "region"))
    world_columns = world.columns()
    tops, runs, surfaces = decode(columns_payload)
    claimed = claims(provenance_path)
    written, summaries = [], []
    if tops:
        xs = [x for x, _z in tops]
        zs = [z for _x, z in tops]
        width = max(xs) - min(xs) + 1
        depth = max(zs) - min(zs) + 1
        every = every or max(1, math.ceil(max(width, depth) / 90))
    else:
        every = every or 2

    def put(name, text):
        with open(os.path.join(into, name), "w") as handle:
            handle.write(text)
        written.append(name)

    put("02-heightmap.txt", heightmap(tops, claimed, intent, every))
    put("03-slopes.txt", slopes(tops, every))
    if tops:
        x0, x1 = min(x for x, _z in tops), max(x for x, _z in tops)
        z0, z1 = min(z for _x, z in tops), max(z for _x, z in tops)
        cut_every = max(1, math.ceil(max(x1 - x0, z1 - z0) / 200))
        put("world-section-x0.txt", section(world, tops, runs, claimed, "x", 0, z0, z1, cut_every))
        put("world-section-z0.txt", section(world, tops, runs, claimed, "z", 0, x0, x1, cut_every))

    for feature_id, kind, (bx0, bz0, bx1, bz1) in features(intent, layout):
        cx, cz = (bx0 + bx1) // 2, (bz0 + bz1) // 2
        pad = 8
        along_x = [(x, cz) for x in range(bx0 - pad, bx1 + pad + 1)]
        along_z = [(cx, z) for z in range(bz0 - pad, bz1 + pad + 1)]
        body_x, summary_x = transect(tops, claimed, world_columns, along_x,
                                     f"TRANSECT {feature_id} ({kind}) along x at z={cz}, x {bx0 - pad}..{bx1 + pad}")
        body_z, summary_z = transect(tops, claimed, world_columns, along_z,
                                     f"TRANSECT {feature_id} ({kind}) along z at x={cx}, z {bz0 - pad}..{bz1 + pad}")
        put(f"transect-{feature_id}.txt", body_x + "\n" + body_z)
        summaries.append(f"  {feature_id:18} along x: {summary_x}")
        summaries.append(f"  {'':18} along z: {summary_z}")

    if walk_for is not None:
        goals = []
        for kind in ("destroyables", "cores", "wools"):
            for goal in intent.get(kind) or []:
                at = goal.get("anchor") or goal.get("location") or goal.get("point") or {}
                if "x" in at:
                    unit = (goal.get("stamp") or {}).get("unit") or kind
                    goals.append((f"{unit}-{(goal.get('stamp') or {}).get('image', 0)}", (at["x"], at["z"])))
        routes = []
        for spawn in intent.get("spawns") or []:
            point = spawn.get("point") or {}
            if "x" not in point:
                continue
            for goal_id, goal_at in goals:
                walk = walk_for((point["x"], point["z"]), goal_at)
                if walk is None:
                    continue
                body, summary = route_profile(tops, surfaces, claimed, world_columns, walk, f"spawn-{spawn.get('team')}", goal_id)
                routes.append(body)
                summaries.append(summary)
        if routes:
            put("04-routes.txt", "\n".join(routes))
    return written, summaries


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    sys.path.insert(0, os.path.dirname(HERE))
    import drive  # noqa: E402
    specdir, world_dir = sys.argv[1], sys.argv[2]
    base = os.path.basename(specdir.rstrip("/"))
    slug = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else base
    into = sys.argv[sys.argv.index("--into") + 1] if "--into" in sys.argv else os.path.join(specdir, "renders")
    every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else None
    with open(f"{specdir}/{base}.layout.json") as handle:
        layout = json.load(handle)
    with open(f"{specdir}/{base}.intent.json") as handle:
        intent = json.load(handle)
    _, payload = drive.call("POST", f"/map/{slug}/sketch/columns", layout, fatal=False)

    def walk_for(from_xz, to_xz):
        status, answer = drive.call("GET", f"/map/{slug}/walk?from={from_xz[0]},{from_xz[1]}&to={to_xz[0]},{to_xz[1]}", fatal=False)
        return answer if status == 200 and isinstance(answer, dict) else None

    written, summaries = write_all(into, world_dir, os.path.join(specdir, "provenance.json"), intent, layout,
                                   payload, walk_for, every)
    print("\n".join(summaries))
    print(f"{len(written)} text read(s) -> {into}: {', '.join(written)}")


if __name__ == "__main__":
    main()
