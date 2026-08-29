"""Themes, the document a sculpture is posted as, and the calls that build and read it back.

A sculpture's material is a **terrain theme**, because a theme is the only thing a sketch shape can say about
what it is made of. That is not a workaround: a theme's five buckets — bedrock, fill, wall, surface, rim —
are a free shading model for a built form. `surface` is the top course, `wall` the exposed riser and `rim` the
edge cap, so three blocks in one theme give a shape a lit top, a body and an outline with nothing else stated.
`solid` is the flat version for a part that wants one block everywhere.
"""
import json
import urllib.error
import urllib.request

API = "http://localhost:7894/api"


def solid(block, data=0):
    """One block in every bucket, and no bedrock course under it."""
    material = {"kind": "solid", "id": block, "data": data}
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "boundary",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": material},
        "surface": {"enabled": True, "depth": 1, "material": material},
        "wall": material,
        "wallEnabled": True,
        "fill": material,
    }


def shaded(surface, wall, rim=None, fill=None, rim_edges="boundary"):
    """A three-tone theme: `surface` on the top course, `wall` down every exposed riser, `rim` capping the
    edges. Each argument is `(id, data)`. This is what makes a stamped form read as a form — a solid mass of
    one block has no edges in a screenshot."""
    def material(spec):
        return {"kind": "solid", "id": spec[0], "data": spec[1]}
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": material(rim or surface)},
        "surface": {"enabled": True, "depth": 1, "material": material(surface)},
        "wall": material(wall),
        "wallEnabled": True,
        "fill": material(fill or wall),
    }


def layout(layers, themes, map_theme=None, mirror="none", centre=(0, 0), relief=None, dressing=None,
           room_styles=True):
    """The sketch document itself. `mirror` of `none` is the right default for a gallery board: a sculpture
    is drawn where it stands, and a fan would put a second one across the axis."""
    xs, zs = [], []
    for layer in layers:
        for shape in layer["layout"]["shapes"]:
            if "min_x" in shape:
                xs += [shape["min_x"], shape["max_x"]]
                zs += [shape["min_z"], shape["max_z"]]
            elif "vertices" in shape:
                xs += [v[0] for v in shape["vertices"]]
                zs += [v[1] for v in shape["vertices"]]
            elif "center_x" in shape:
                xs += [shape["center_x"] - shape["radius"], shape["center_x"] + shape["radius"]]
                zs += [shape["center_z"] - shape["radius"], shape["center_z"] + shape["radius"]]
    document = {
        "setup": {
            "mirror_mode": mirror,
            "center": {"cx": centre[0], "cz": centre[1]},
            "bbox": {"min_x": min(xs) - 8, "max_x": max(xs) + 8,
                     "min_z": min(zs) - 8, "max_z": max(zs) + 8},
        },
        "layers": layers,
        "themes": themes,
        "mapTheme": map_theme or next(iter(themes)),
    }
    # An explicit null is "no building at all" — a pad on open ground — where absent would stamp the
    # built-in bedrock shell. A gallery wants the pad.
    if room_styles is None:
        document["roomStyles"] = {"spawn": None}
    if relief:
        document["relief"] = relief
    if dressing:
        document["dressing"] = dressing
    return document


def intent(name, created="2026-08-29", spawn=None, observer=None):
    """The smallest intent a **exportable** map needs. A gallery board is played for nothing and states no
    objective, but `EX2` refuses an export of a map with no spawn at all — "no player and no observer can
    enter it" — so a board meant to be walked round declares one visitor team and one pad."""
    x, y, z = spawn or (0, 10, 0)
    ox, oy, oz = observer or (x, y + 40, z)
    return {
        "meta": {"name": name, "created": created},
        "teams": [{"id": "visitors", "name": "Visitors", "color": "aqua"}],
        "maxPlayers": 8,
        "spawns": [{"layer": None, "team": "visitors", "point": {"x": x, "y": y, "z": z},
                    "protection": [{"minX": x - 8, "minZ": z - 8, "maxX": x + 8, "maxZ": z + 8}],
                    "yaw": 180, "iron": []}],
        "observer": {"point": {"x": ox, "y": oy, "z": oz}, "yaw": 180},
        "build": {"maxHeight": None, "areas": [], "holes": [], "voidEnforcement": None},
        "wools": [], "destroyables": [], "cores": None,
    }


def call(method, path, body=None, expect=(200, 201)):
    """One API call, with every finding the pipeline raised printed rather than swallowed. A 2xx is not a
    promise that everything posted survived: `warnings` names what did not."""
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"{API}{path}", data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            payload = response.read()
            status = response.status
            header = response.headers.get("Pgm-Warnings")
    except urllib.error.HTTPError as fault:
        payload, status, header = fault.read(), fault.code, fault.headers.get("Pgm-Warnings")

    answer = json.loads(payload) if payload else {}
    flag = f"  ! {header}" if header else ""
    print(f"{status:>4} {method:<5} {path}{flag}")
    for finding in (answer.get("warnings") or []) + (answer.get("findings") or []):
        print(f"       {finding.get('rule', '?')}  {finding.get('message', finding)}")
    if status not in expect:
        raise SystemExit(f"refused: {json.dumps(answer)[:900]}")
    return answer


def store(slug, name, document, authors=("Opus 5",), spawn=None, observer=None):
    return call("POST", "/map/from-documents",
                {"layout": document, "intent": intent(name, spawn=spawn, observer=observer),
                 "name": name, "slug": slug, "authors": list(authors)})


def export(slug, out):
    """The world a server loads — `region/`, `level.dat`, `map.xml` — unzipped into `out`. A gallery is worth
    exporting for the same reason a map is: a picture is a claim about a world and the world is the thing."""
    import io
    import os
    import shutil
    import urllib.request
    import zipfile

    with urllib.request.urlopen(f"{API}/map/{slug}/export", timeout=900) as response:
        blob = response.read()
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        archive.extractall(out)
    inner = [e for e in os.listdir(out) if os.path.isdir(os.path.join(out, e))]
    if inner == [slug] or (len(inner) == 1 and "region" in os.listdir(os.path.join(out, inner[0]))):
        nested = os.path.join(out, inner[0])
        for entry in os.listdir(nested):
            shutil.move(os.path.join(nested, entry), os.path.join(out, entry))
        os.rmdir(nested)
    # The provenance sidecar is a record of what each pass placed, not something a server reads.
    sidecar = os.path.join(out, "region", "provenance.json")
    print(f" exp {slug} -> {out}  ({len(blob) // 1024} KiB)")
    return sidecar if os.path.exists(sidecar) else None


def columns(slug, document):
    """The built world as per-column runs — the real build, not a preview of the drawing."""
    return call("POST", f"/map/{slug}/sketch/columns", document)
