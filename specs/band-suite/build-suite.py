#!/usr/bin/env python3
"""The band suite — one composed board per size band, finished with one shared document.

The composer sizes a board from the band its player count falls in (nano 6-13, micro 14-21, milli
22-31, centi 32-47, hecto 48+), and each band carries its own measured land budget and corridor
width. This writes six spec directories — two nano, two micro, one milli, one centi — whose plans
come **straight off the composer with nothing adapted**, and whose finish is the same document on
every one of them. What differs between the six boards is therefore the composer's own output and
nothing else, which is the point: the look is held fixed so the layout can be read.

    python3 specs/band-suite/build-suite.py          # writes specs/opus5-<slug>/ for each board
    tools/drive.py specs/opus5-quernstone "Quernstone" --out maps/opus5-quernstone

The ground is finished by its **angle** rather than its height: one `layered` material on the
`slope` axis, so the same stack finishes the flat, the shoulder and the face of a hill. Relief is
deliberately light — a low grain plus a handful of point marks seated on the plan's own pieces and
mirrored through the board's symmetry, so both halves read alike and no mark lands off its ground.
"""
import json, os, urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")
HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.dirname(HERE)

# One board per band, with a second at the two bands wide enough to show a range inside themselves.
# The seed is the board: a request reproduces its plan byte for byte. The six between them carry every
# hub form the sampler reaches, every wool family it draws and all three frontlines, so the suite reads
# as the composer's range rather than as six draws of its favourite.
BOARDS = [
    ("opus5-quernstone",    "Quernstone",    8,  2, "rot_180",  1),   # ring   · clamp        · twin
    ("opus5-hollowbeck",    "Hollowbeck",   12,  2, "mirror_z", 9),   # G      · i, U         · single
    ("opus5-sallowmere",    "Sallowmere",   16,  2, "rot_180",  6),   # ring   · donut, donut · bar
    ("opus5-thrushgate",    "Thrushgate",   20,  2, "mirror_z", 5),   # ring   · i, clamp     · twin
    ("opus5-oxenholme",     "Oxenholme",    24,  2, "rot_180",  3),   # twin   · L, U        · bar
    ("opus5-stavelbridge",  "Stavelbridge", 32,  2, "rot_180",  1),   # G      · i, i, donut  · twin
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
    """The composer's own plan for this request, and the band it was built to. Pinning is how a
    composed board's plan is read back; the stored row is dropped again, since the spec is what the
    map is."""
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
    """The ground read by its angle. A thickness on the slope axis is a span of degrees, so one
    stack finishes the meadow, the shoulder and the crag of the same hill; each band carries a depth
    stack of its own so the turf stays one course over its soil.

    The cuts are read off `GET …/incline`, which answers how much ground stands in each ten degrees.
    A composed board is flat ground with marks pushed into it, so most of it sits under ten and the
    bands are cut low: the turf ends where the mark shoulders begin."""
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


# ── relief, seated on the plan's own ground ───────────────────────────────────────────────────────

def centre(piece, cell):
    x, z, w, h = piece["rect"]
    return (int((x + w / 2) * cell), int((z + h / 2) * cell))


def relief_marks(plan, cell, reach):
    """Low point marks on the plan's biggest pieces, each stating a height that rises with how far its
    ground sits from the symmetry axis: the mid is the low ground and a team's own back is the high,
    which is the shape a CTW board is fought up and down.

    A relief group holds one team's ground and the symmetry fans what it builds, so the marks are
    stated once, on the authored unit — a mark placed at a piece's mirror image lands off the group
    and pins nothing (RL4).

    A point mark pins every cell of its band exactly, so two whose bands touch describe a wall between
    them rather than a slope (RL3) — and `tread`, which grades that, is a line mark's field and is read
    off a point mark not at all. So the marks are chosen to stand clear of one another, and the group's
    own reach is what blends the ground between them."""
    base = plan["globals"]["surface"]
    axis = 1 if plan["globals"]["symmetry"] in ("rot_180", "mirror_z", "rot_90") else 0
    pieces = sorted((p for p in plan["pieces"] if p["role"] == "piece"),
                    key=lambda p: p["rect"][2] * p["rect"][3], reverse=True)

    # take the biggest pieces whose bands stand clear of one another, biggest first. Two bands that
    # touch is what RL3 names, and nothing about a point mark grades that seam -- tread is a line's
    # field. Clear of each other, the group's reach is what blends between them, which is smooth.
    placed = []
    for piece in pieces:
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
    """Ground cover over the biggest pieces — ferns and grass scattered by noise rather than placed,
    so nothing is judged at a site and nothing is declined. The points are a piece's own corners, so
    the patch is exactly the ground the plan drew."""
    pieces = [p for p in plan["pieces"] if p["role"] == "piece"]
    pieces.sort(key=lambda p: p["rect"][2] * p["rect"][3], reverse=True)
    props = []
    for index, piece in enumerate(pieces[:6]):
        x, z, w, h = (v * cell for v in piece["rect"])
        props.append({
            "id": f"cover-{index}", "kind": "flora", "seed": 90 + index,
            "spec": {"coverage": 0.55, "scale": 9, "octaves": 3, "fernShare": 0.40,
                     "flowerShare": 0.06, "flowerScale": 14, "tallShare": 0.10},
            "points": [[x, z], [x + w, z], [x + w, z + h], [x, z + h]],
        })
    return props


def finish(plan, name, cell):
    reach = 22 + 4 * plan["globals"]["maxPlayers"] // 8
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-16",
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
            json.dump(finish(plan, name, cell), handle, indent=1)
        print(f"  {name:14} {spend['band']:6} p{players:<3} {symmetry:9} seed {seed}  "
              f"land {spend['landCells']}/{spend['budgetCells']:.0f} cells  "
              f"hub {structure['hub']}  wools {','.join(structure['wools'])}  "
              f"front {structure['frontline']}")


if __name__ == "__main__":
    main()
