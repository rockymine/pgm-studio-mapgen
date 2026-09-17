#!/usr/bin/env python3
"""The crossing suite — six composed boards chosen for what their middles are, finished with one document.

The composer funds the mid out of the units' own land and lays a row of stones astride the symmetry axis
inside the band. A stone sitting on the axis has its own fanned image abut it, so the pair is **one shared
island** both teams reach at once rather than a stone each — which is the thing these six are picked to
show. Between them they carry one shared stone, none, one shared, a mirrored pair, three on a mirror and
three islands from two authored stones on a rotation, at all five size bands.

A board asking for a **split band** takes the empty crossing and no stone, because the bay between the
split's two legs is meant to be the island. `Cleftmoor` is that case: its frontline offered no split the
carve would take, the legs are one band, and the crossing is plain void — the contrast the other five are
read against.

    python3 specs/crossing-suite/build-suite.py       # writes specs/opus5-<slug>/ for each board
    tools/drive.py specs/opus5-stannerford "Stannerford" --out maps/opus5-stannerford

The plans come **straight off the composer with nothing adapted**, and the finish is the same document on
every one of them, so what differs between the boards is the composer's own output and nothing else.

The ground is finished by its **angle** rather than its height: one `layered` material on the `slope` axis,
so the same stack finishes the flat, the shoulder and the face of a hill. Relief is deliberately light — a
low grain plus a handful of point marks seated on the plan's own pieces, chosen so their bands stand clear
of one another, because a point mark pins every cell of its band exactly and two whose bands touch describe
a wall rather than a slope. The mid stones are left out of that choice and take the ground theme level: they
are the crossing's own ground and what the suite is for is seeing where they sit.
"""
import json, os, urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.dirname(HERE)

# The id every mid stone carries, so the finish can tell the crossing's ground from a team unit's.
STONE_PREFIX = "mid-stone-"

# One board per kind of middle. The seed is the board: a request reproduces its plan byte for byte.
BOARDS = [
    ("opus5-stannerford", "Stannerford",  8, 2, "rot_180",  6),   # nano  · one shared stone, twin front
    ("opus5-cleftmoor",   "Cleftmoor",    8, 2, "rot_180",  2),   # nano  · a split band asked for, no stone
    ("opus5-ringmere",    "Ringmere",    16, 2, "rot_180",  1),   # micro · one stone, three wools with a donut
    ("opus5-twyford",     "Twyford",     24, 2, "rot_180",  0),   # milli · a mirrored pair, two islands
    ("opus5-threapland",  "Threapland",  32, 2, "mirror_z", 0),   # centi · three stones, MD6's maximum
    ("opus5-broadstang",  "Broadstang",  52, 2, "rot_180",  7),   # hecto · three islands from two authored
]


def get(path):
    with urllib.request.urlopen(API + path, timeout=180) as response:
        return json.load(response)


def post(path, body):
    request = urllib.request.Request(
        API + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


def delete(path):
    request = urllib.request.Request(API + path, method="DELETE")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response.read()
    except Exception:
        pass


def compose(players, teams, symmetry, seed):
    """The composer's own plan for this request. Pinning is how a composed board's plan is read back; the
    stored row is dropped again, since the spec is what the map is."""
    page = get(f"/compose?players={players}&teams={teams}&symmetry={symmetry}"
               f"&seedStart={seed}&count=1")
    if not page["cards"]:
        raise SystemExit(f"nothing composed at players={players} seed={seed}")
    card = page["cards"][0]
    pinned = post("/compose/pin", {**card["descriptor"], "index": 0})
    plan = json.loads(pinned["planJson"])
    delete(f"/plans/{pinned['id']}")
    return plan, card["spend"], card["structure"]


# ── the shared finish ─────────────────────────────────────────────────────────────────────────────

def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def depth_stack(*courses):
    """A depth stack: the top course, then what lies under it, handing over to stone below."""
    return {"kind": "layered", "axis": "depth", "beyond": solid(1),
            "stack": {"ending": "handOver",
                      "bands": [{"thickness": t, "material": m} for t, m in courses]}}


def moor_surface():
    """The ground read by its angle. A thickness on the slope axis is a span of degrees, so one stack
    finishes the meadow, the shoulder and the crag of the same hill; each band carries a depth stack of its
    own so the turf stays one course over its soil.

    The cuts are read off `GET …/incline`, which answers how much ground stands in each ten degrees. A
    composed board is flat ground with marks pushed into it, so most of it sits under ten and the bands cut
    low: the turf ends where the mark shoulders begin."""
    return {"kind": "layered", "axis": "slope", "beyond": solid(1),
            "stack": {"ending": "repeat", "bands": [
                # the flat and the gentle roll: turf over two of dirt
                {"thickness": 12, "material": depth_stack((1, solid(2)), (2, solid(3)))},
                # the shoulder: coarse dirt showing through, the turf broken
                {"thickness": 10, "material": depth_stack((1, solid(3, 1)), (2, solid(3)))},
                # the face: stone and cobble, mottled so a crag is not one flat grey
                {"thickness": 68, "material": depth_stack(
                    (2, {"kind": "voronoi", "seed": 11, "cellSize": 7,
                         "bands": [{"weight": 3, "material": solid(1)},
                                   {"weight": 2, "material": solid(4)},
                                   {"weight": 1, "material": solid(98)}]}),
                    (3, solid(1)))},
            ]}}


def moor_theme():
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": solid(4)},
        "surface": {"enabled": True, "depth": 3, "material": moor_surface()},
        "fill": solid(1),
    }


# ── relief, seated on the team unit's own ground ──────────────────────────────────────────────────

def unit_pieces(plan):
    """The team unit's terrain, largest first. A mid stone is generating terrain like any other piece and
    the one piece that sits across the axis, so a relief seated on one would be pinning the crossing."""
    pieces = [p for p in plan["pieces"]
              if p["role"] == "piece" and not p["id"].startswith(STONE_PREFIX)]
    pieces.sort(key=lambda p: p["rect"][2] * p["rect"][3], reverse=True)
    return pieces


def centre(piece, cell):
    x, z, w, h = piece["rect"]
    return (int((x + w / 2) * cell), int((z + h / 2) * cell))


def relief_marks(plan, cell, reach):
    """Low point marks on the unit's biggest pieces, each stating a height that rises with how far its
    ground sits from the symmetry axis: the mid is the low ground and a team's own back is the high, which
    is the shape a CTW board is fought up and down.

    A relief group holds one team's ground and the symmetry fans what it builds, so the marks are stated
    once, on the authored unit — a mark placed at a piece's mirror image lands off the group and pins
    nothing (RL4).

    A point mark pins every cell of its band exactly, so two whose bands touch describe a wall between them
    rather than a slope (RL3) — and `tread`, which grades that, is a line mark's field and is read off a
    point mark not at all. So the marks are chosen to stand clear of one another, and the group's own reach
    is what blends the ground between them."""
    base = plan["globals"]["surface"]
    axis = 1 if plan["globals"]["symmetry"] in ("rot_180", "mirror_z", "rot_90") else 0

    placed = []
    for piece in unit_pieces(plan):
        x, z = centre(piece, cell)
        radius = max(9, min(reach - 4, int(min(piece["rect"][2], piece["rect"][3]) * cell * 1.1)))
        if all((x - px) ** 2 + (z - pz) ** 2 > (radius + pr + 6) ** 2 for px, pz, pr in placed):
            placed.append((x, z, radius))
        if len(placed) == 4:
            break

    marks = []
    for rank, (x, z, radius) in enumerate(sorted(placed, key=lambda m: abs(m[axis]))):
        marks.append({"id": f"swell-{rank}", "kind": "point", "at": [x, z],
                      "r": radius, "h": base + 3 + 3 * rank})
    return marks


def flora(plan, cell):
    """Ground cover over the unit's biggest pieces — ferns and grass scattered by noise rather than placed,
    so nothing is judged at a site and nothing is declined. The points are a piece's own corners, so the
    patch is exactly the ground the plan drew."""
    props = []
    for index, piece in enumerate(unit_pieces(plan)[:6]):
        x, z, w, h = (v * cell for v in piece["rect"])
        props.append({
            "id": f"cover-{index}", "kind": "flora", "seed": 90 + index,
            "spec": {"coverage": 0.55, "scale": 9, "octaves": 3, "fernShare": 0.40,
                     "flowerShare": 0.06, "flowerScale": 14, "tallShare": 0.10},
            "points": [[x, z], [x + w, z], [x + w, z + h], [x, z + h]],
        })
    return props


def finish(plan, cell):
    reach = 22 + 4 * plan["globals"]["maxPlayers"] // 8
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-17",
        "voidEnforcement": True,
        "mapTheme": "moor",
        "themes": {"moor": moor_theme()},
        "roomStyles": {"spawn": "@showcase-hall", "wool": "@showcase-cage"},
        "dressing": {"props": flora(plan, cell)},
        "relief": {"*": {
            "base": plan["globals"]["surface"],
            "step": 1,
            "reach": reach,
            "grain": {"amplitude": 1, "scale": 15, "seed": 7},
            "marks": relief_marks(plan, cell, reach),
        }},
        "biome": {"kind": "solid", "biome": 1},
    }


def stones(plan):
    """The crossing's own stones, as the plan states them — the row this suite exists to show."""
    return [p for p in plan["pieces"] if p["id"].startswith(STONE_PREFIX)]


def main():
    print(f"studio at {API}\n")
    for slug, name, players, teams, symmetry, seed in BOARDS:
        plan, spend, structure = compose(players, teams, symmetry, seed)
        plan["meta"]["name"] = name
        cell = plan["globals"]["cell"]
        directory = os.path.join(SPECS, slug)
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, f"{slug}.plan.json"), "w") as handle:
            json.dump(plan, handle, indent=1)
        with open(os.path.join(directory, f"{slug}.finish.json"), "w") as handle:
            json.dump(finish(plan, cell), handle, indent=1)
        row = stones(plan)
        shapes = " ".join(f"{p['rect'][3]}x{p['rect'][2]}" for p in row) or "—"
        print(f"  {name:13} {spend['band']:6} p{players:<3} {symmetry:9} seed {seed}  cell {cell}  "
              f"unit {spend['unit']['cells']}/{spend['unit']['budgetCells']:.0f}  "
              f"mid {spend['mid']['cells']}/{spend['mid']['budgetCells']:.0f}  "
              f"stones {len(row)} {shapes:14} hub {structure['hub']}  "
              f"wools {','.join(structure['wools'])}  front {structure['frontline']}")


if __name__ == "__main__":
    main()
