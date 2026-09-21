"""Shared authoring helpers for the opus5c run's four boards.

Materials, the two ring generators the relief marks are drawn with, and the
library fetch for a copied tree body. It writes no document of its own: each
board's build-spec states its own plan, relief, themes, shapes and dressing.
"""
import json
import math
import os
import urllib.request

API = os.environ.get("PGM_STUDIO_API", "http://localhost:7894/api")


# ---------------------------------------------------------------- materials

def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def cells(seed, size, rise, palette, jitter=45, warp=1):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "rise": rise, "palette": palette}


def field(seed, scale, octaves, stops, rise=0, kind="noise"):
    return {"kind": kind, "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def voronoi(seed, size, bands, rise=4):
    """The fill's own pattern. It draws a diagram — a grid of lines with cells
    reading off it — so it belongs in the body of the rock nobody sees until a
    wall is cut, and it is made of stone.

    `bands` is (depth, material) pairs: a VoronoiBand states both, and a band
    carrying a bare material is PT2. `rise` is the vertical period that gives a
    face its grain, and a fill sampled in the plane alone resolves every block
    of a column alike and reads as vertical stripes, which is PT4."""
    return {"kind": "voronoi", "seed": seed, "cellSize": size,
            "bands": [{"material": m, "depth": d} for d, m in bands],
            "rise": rise}


def band(thickness, material):
    return {"thickness": thickness, "material": material}


def stack(axis, bands, frm=None):
    out = {"kind": "layered", "axis": axis,
           "stack": {"ending": "repeat", "bands": bands}}
    if frm is not None:
        out["from"] = frm
    return out


def soil(top, under, depth=2):
    """One course of a surfacing block over `depth` of soil, which is what a
    depth stack owes a surface that has to stay one course thick."""
    return stack("depth", [band(1, top), band(depth, under)])


def slope_stack(bands):
    """A surface finished by the ground's angle. `bands` is (degrees, material)
    lowest first; a thickness on this axis is a span of degrees, so one stack
    finishes the flat, the shoulder and the face of the same hill."""
    out, last = [], 0
    for edge, mat in bands:
        out.append(band(edge - last, mat))
        last = edge
    return stack("slope", out)


# ---------------------------------------------------------------- geometry

def rng(seed):
    state = [seed * 6364136223846793005 + 1442695040888963407]

    def nxt():
        state[0] = (state[0] * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return ((state[0] >> 33) & 0xFFFFFF) / float(0xFFFFFF)
    return nxt


def blob(cx, cz, radius, points=11, wobble=0.18, seed=1, squash=1.0):
    """A closed lobed ring. A rectangle marks ground with square sides; a ring
    of this shape is not tellable from terrain."""
    nxt = rng(seed)
    out = []
    for i in range(points):
        a = 2.0 * math.pi * i / points
        r = radius * (1.0 + wobble * (nxt() * 2.0 - 1.0))
        out.append([round(cx + r * math.cos(a), 2),
                    round(cz + r * math.sin(a) * squash, 2)])
    return out


def wander_rect(x0, z0, x1, z1, wobble=3.0, seed=1, per_side=4):
    """A rectangle walked as a wandering ring — an area mark that has to cover
    a rectangle without reading as one."""
    nxt = rng(seed)
    pts = []

    def run(ax, az, bx, bz):
        for i in range(per_side):
            t = i / per_side
            pts.append([round(ax + (bx - ax) * t + wobble * (nxt() * 2 - 1), 2),
                        round(az + (bz - az) * t + wobble * (nxt() * 2 - 1), 2)])
    run(x0, z0, x1, z0)
    run(x1, z0, x1, z1)
    run(x1, z1, x0, z1)
    run(x0, z1, x0, z0)
    return pts


def arc_ring(cx, cz, r_in, r_out, a0, a1, steps=14, wobble=2.0, seed=1):
    """A closed ring following an annular sector — out along the outer radius
    from a0 to a1 and back along the inner. It is what draws a mark over a
    board whose ground is a horseshoe, where a rectangle would cover the pit."""
    nxt = rng(seed)
    pts = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        r = r_out + wobble * (nxt() * 2 - 1)
        pts.append([round(cx + r * math.cos(a), 2), round(cz + r * math.sin(a), 2)])
    for i in range(steps + 1):
        a = a1 + (a0 - a1) * i / steps
        r = r_in + wobble * (nxt() * 2 - 1)
        pts.append([round(cx + r * math.cos(a), 2), round(cz + r * math.sin(a), 2)])
    return pts


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


# ---------------------------------------------------------------- library

def tree_body(name, cache):
    """A copied recipe's body out of the studio's own tree library. A body is
    cut from a world and cannot be re-derived, so the answer is cached into the
    spec directory beside the documents that use it."""
    if name in cache:
        return cache[name]
    with urllib.request.urlopen(f"{API}/tree-styles") as fh:
        rows = json.load(fh)
    by_name = {r["name"]: r["id"] for r in rows}
    if name not in by_name:
        raise SystemExit(f"no tree recipe named {name}")
    with urllib.request.urlopen(f"{API}/tree-styles/{by_name[name]}/json") as fh:
        answer = json.load(fh)
    cache[name] = json.loads(answer["styleJson"]) if "styleJson" in answer else answer
    return cache[name]


def load_cache(path):
    return json.load(open(path)) if os.path.exists(path) else {}


def save_cache(path, cache):
    json.dump(cache, open(path, "w"))


def write(path, doc):
    json.dump(doc, open(path, "w"), indent=1)
    print(f"wrote {path}")
