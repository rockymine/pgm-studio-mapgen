"""Shared authoring helpers for the opus5b run's four boards.

Materials, lobed rings and the two small arithmetic helpers every one of the
four build-specs needs. It writes no document of its own; each board's
build-spec states its own plan, relief, themes and dressing.
"""
import json
import math
import os
import urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:5189/api")


# ---------------------------------------------------------------- materials

def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def cells(seed, size, rise, palette, jitter=45, warp=1):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "rise": rise, "palette": palette}


def field(seed, scale, octaves, stops, rise=0, kind="noise"):
    return {"kind": kind, "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def band(thickness, material):
    return {"thickness": thickness, "material": material}


def stack(axis, bands, frm=None):
    out = {"kind": "layered", "axis": axis,
           "stack": {"ending": "repeat", "bands": bands}}
    if frm is not None:
        out["from"] = frm
    return out


def soil(top, under, depth=2):
    """One course of a surfacing block over `depth` of soil — what PT1 wants."""
    return stack("depth", [band(1, top), band(depth, under)])


# ---------------------------------------------------------------- geometry

def lobe(cx, cz, radius, points=11, wobble=0.18, seed=1, squash=1.0):
    """A closed lobed ring. Rectangles build mesas with sheer square sides;
    a ring of this shape is indistinguishable from ground."""
    rnd = _rng(seed)
    ring = []
    for i in range(points):
        a = 2.0 * math.pi * i / points
        r = radius * (1.0 + wobble * (rnd() * 2.0 - 1.0))
        ring.append([round(cx + r * math.cos(a), 2),
                     round(cz + r * math.sin(a) * squash, 2)])
    return ring


def lobed_rect(x0, z0, x1, z1, wobble=3.0, seed=1, per_side=4):
    """A rectangle walked as a wandering ring — for a strand, an apron, a
    bench: an area mark that has to cover a rectangle without reading as one."""
    rnd = _rng(seed)
    pts = []

    def run(ax, az, bx, bz):
        for i in range(per_side):
            t = i / per_side
            jx = wobble * (rnd() * 2.0 - 1.0)
            jz = wobble * (rnd() * 2.0 - 1.0)
            pts.append([round(ax + (bx - ax) * t + jx, 2),
                        round(az + (bz - az) * t + jz, 2)])
    run(x0, z0, x1, z0)
    run(x1, z0, x1, z1)
    run(x1, z1, x0, z1)
    run(x0, z1, x0, z0)
    return pts


def _rng(seed):
    state = [seed * 6364136223846793005 + 1442695040888963407]

    def nxt():
        state[0] = (state[0] * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return ((state[0] >> 33) & 0xFFFFFF) / float(0xFFFFFF)
    return nxt


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


# ---------------------------------------------------------------- library

def tree_body(name, cache):
    """A copied recipe's body, out of the studio's own tree library.

    A body cannot be re-derived from anything, so the answer is cached into the
    spec directory beside the documents it is used in."""
    if name in cache:
        return cache[name]
    with urllib.request.urlopen(f"{API}/tree-styles") as fh:
        rows = json.load(fh)
    by_name = {r["name"]: r["id"] for r in rows}
    if name not in by_name:
        raise SystemExit(f"no tree recipe named {name}")
    with urllib.request.urlopen(f"{API}/tree-styles/{by_name[name]}/json") as fh:
        answer = json.load(fh)
    # the route answers the stamper's own JSON under styleJson
    cache[name] = json.loads(answer["styleJson"]) if "styleJson" in answer else answer
    return cache[name]


def load_cache(path):
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return {}


def save_cache(path, cache):
    with open(path, "w") as fh:
        json.dump(cache, fh)


def write(path, doc):
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {path}")
