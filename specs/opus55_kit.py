"""The authoring kit the 2026-09-28 run's boards are written with — materials, themes, props.

Every function here writes a piece of a finish document and nothing else: none of it reads a built world,
computes a placement or checks anything. The studio does all of that. What lives here is what six
`build-spec.py` files would otherwise each spell out again — how a slope-banded ground is stacked, how a
copied tree's recipe is carried, how a path is paved.

A copied tree's body is fetched once from `GET /api/tree-styles/{id}/json` and cached beside the spec as
`trees.json`, so a board rebuilds from the repository alone after its first run.
"""
import json, math, os, urllib.request

API = os.environ.get("PGM_STUDIO_API", "https://pgmstudio.de/api")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── materials ────────────────────────────────────────────────────────────────────────────────────────────

def S(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def cell(palette, size=2, seed=1, rise=None):
    """Even shares of every entry. A wall or fill needs `rise` (PT4); a surface needs size 2 or more (PT3)."""
    out = {"kind": "cell", "cellSize": size, "seed": seed, "palette": palette}
    if rise:
        out["rise"] = rise
    return out


def noise(stops, scale=2, seed=1):
    """A ramp over a smooth field: the middle stops join into the ground and the end stops come out as
    patches inside it, so the main set goes in the middle and the patch sets at the ends."""
    return {"kind": "noise", "scale": scale, "seed": seed, "stops": stops}


def depth(top, under, n_top=1, n_under=2):
    """A top course over what lies under it."""
    return {"kind": "layered", "stack": {"ending": "repeat", "bands": [
        {"material": top, "thickness": n_top}, {"material": under, "thickness": n_under}]}}


def beds(pairs, start=-40, reach=16, beyond=None):
    """Strata that follow the ground averaged `reach` cells either side, from `start` blocks under it.
    The last band claims everything past the stack, so `pairs` is written out bed by bed."""
    out = {"kind": "layered", "axis": "height", "from": start, "follow": 100, "reach": reach,
           "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in pairs]}}
    if beyond:
        out["beyond"] = beyond
    return out


def by_slope(*bands):
    """A surface finished by its angle: (degrees, material) from level upward."""
    return {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
        {"thickness": t, "material": m} for t, m in bands]}}


def by_height(pairs, start):
    """A stack pinned to world Y from `start` — a façade's courses. Written out band by band."""
    return {"kind": "layered", "axis": "height", "from": start,
            "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in pairs]}}


def theme(surface, wall, fill, depth_=3, rim=None, rim_edges="void"):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": rim_edges,
            "rim": {"enabled": rim is not None, "depth": 1, "material": rim or S(1)},
            "wallEnabled": True, "wallOnTerrainFaces": True, "wall": wall, "fill": fill,
            "surface": {"enabled": True, "depth": depth_, "material": surface}}


def one(material, rim_edges="boundary"):
    """A theme answering one material in every bucket — a made thing too thin to have a core."""
    return theme(material, material, material, depth_=1, rim=material, rim_edges=rim_edges)


# The rock under every board unless it says otherwise: stone and andesite, cobblestone at a quarter.
ROCK = cell([S(1), S(1, 5), S(1), S(4)], size=2, seed=8, rise=2)


# ── shapes and outlines ─────────────────────────────────────────────────────────────────────────────────

def ring(cx, cz, rx, rz, n=28, wobble=0.0, lobes=3, phase=0.0, turn=0.0):
    """An outline pulled in and out as it goes round, optionally turned by `turn` degrees."""
    out, t = [], math.radians(turn)
    for k in range(n):
        a = 2 * math.pi * k / n
        f = 1 + wobble * math.cos(lobes * a + phase)
        x, z = rx * f * math.cos(a), rz * f * math.sin(a)
        out.append([round(cx + x * math.cos(t) - z * math.sin(t), 1),
                    round(cz + x * math.sin(t) + z * math.cos(t), 1)])
    return out


def patch(pid, points, theme_id, height, group=None, layer=None):
    """A patch of different ground: a polygon at the height of the ground it lies on, with its own theme
    and no relief_scope, so it paints the cells it forms the surface of and nothing else."""
    shape = {"id": pid, "type": "polygon", "operation": "add", "vertices": points,
             "base_height": height, "theme": theme_id}
    if group:
        shape["group"] = group
    if layer:
        shape["layer"] = layer
    return shape


# ── props ───────────────────────────────────────────────────────────────────────────────────────────────

def path(pid, seed, points, pave, radius=1.5, wander=2, bend=14):
    return {"kind": "stroke", "id": pid, "seed": seed, "style": "solid", "radius": radius,
            "claimsGround": True, "wander": wander, "wanderLength": bend, "pave": pave, "points": points}


def tree(pid, x, z, style, seed=0):
    return {"kind": "tree", "id": pid, "x": x, "z": z, "style": style, "seed": seed}


def boulder(pid, x, z, style, seed=0):
    return {"kind": "boulder", "id": pid, "x": x, "z": z, "style": style, "seed": seed}


def house(pid, style, corners, front=None, storeys=None, seed=0, form=None):
    wing = {"corners": corners}
    spec = {}
    if storeys:
        spec["storeysHigh"] = storeys
    if form:
        spec["form"] = form
    if spec:
        wing["spec"] = spec
    out = {"kind": "house", "id": pid, "style": style, "seed": seed, "wings": [wing]}
    if front:
        out["front"] = front
    return out


def flora(pid, points, coverage=0.3, scale=10, fern=0.25, flowers=0.08, flower_scale=12, tall=0.05, seed=0,
          dead_bush=0.0, cactus=0.0):
    """Ground cover over a drawn area. On sand and clay it grows only what 1.8 lets stand there: `cactus` is
    the share of the cover on sand that is a cactus, one to four tall, and `dead_bush` the share of the rest
    that is a dead bush."""
    return {"kind": "flora", "id": pid, "seed": seed, "points": points,
            "spec": {"coverage": coverage, "scale": scale, "octaves": 2, "fernShare": fern,
                     "flowerShare": flowers, "flowerScale": flower_scale, "tallShare": tall,
                     "deadBushShare": dead_bush, "cactusShare": cactus}}


def chest(pid, x, z, items, facing="negZ", y=None):
    """A chest on the ground at (x, z), or at world `y` where one is stated — on a deck or a platform. `items`
    is `[(item, count, enchantments, slot)]`: enchantments `[(name, level)]` by PGM's names (`power`), and the
    slot 0 at the top left to 26 at the bottom right, or None for the next free one."""
    def stack(item, count, ench, slot):
        out = {"item": item, "count": count}
        if ench:
            out["enchantments"] = [{"name": name, "level": level} for name, level in ench]
        if slot is not None:
            out["slot"] = slot
        return out
    out = {"kind": "chest", "id": pid, "x": x, "z": z, "facing": facing,
           "items": [stack(*entry) for entry in items]}
    if y is not None:
        out["y"] = y
    return out


def pool(pid, points, depth=3, shelf=4, shore=2, bank=None, level=None, layer="ground", edge=1.5, fluid="water"):
    out = {"kind": "fluid", "id": pid, "shape": "pool", "form": "natural", "layer": layer, "points": points,
           "radius": shelf, "depth": depth, "shore": shore, "shoreWander": True, "edge": edge, "fluid": fluid}
    if bank:
        out["bank"] = bank
    if level is not None:
        out["level"] = level
    return out


def channel(pid, points, radius=3, depth=2, shore=1, bank=None, form="stream", level=None, layer="ground"):
    out = {"kind": "fluid", "id": pid, "shape": "channel", "form": form, "layer": layer, "points": points,
           "radius": radius, "depth": depth, "shore": shore, "shoreWander": True, "edge": 1.5}
    if bank:
        out["bank"] = bank
    if level is not None:
        out["level"] = level
    return out


# ── recipes ─────────────────────────────────────────────────────────────────────────────────────────────

def house_style(name, **repaint):
    """A shipped house style from tools/styles, as a dressing recipe."""
    shell = json.load(open(os.path.join(ROOT, "tools", "styles", f"{name}.json")))
    shell.update(repaint)
    return {"kind": "house", "shell": shell}


def boulder_style(rock, form="round", size=3, mossy=False):
    return {"kind": "boulder", "form": form, "size": size, "rock": rock, "mossy": mossy}


def copied_trees(specdir, names):
    """The copied tree recipes a board plants, by library name (`birch-2`), cached in
    `<specdir>/trees.json` so the board rebuilds without the network. Returns {name: recipe}."""
    cache_path = os.path.join(specdir, "trees.json")
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    missing = [n for n in names if n not in cache]
    if missing:
        rows = json.load(urllib.request.urlopen(f"{API}/tree-styles"))
        ids = {r["name"]: r["id"] for r in rows}
        for n in missing:
            got = json.load(urllib.request.urlopen(f"{API}/tree-styles/{ids[n]}/json"))
            cache[n] = json.loads(got["styleJson"])
        json.dump(cache, open(cache_path, "w"), separators=(",", ":"))
    return {n: cache[n] for n in names}


def made(layers, part_of, seat=None):
    """`tools/sculpt/props.py` layers as `addLayers` entries: a made thing, painted over its own span,
    all of one `part_of`, optionally settled onto the ground as a unit."""
    out = []
    for layer in layers if isinstance(layers, list) else [layers]:
        entry = {"id": layer["id"], "name": layer["name"], "base_y": layer["base_y"], "kind": "made",
                 "part_of": part_of, "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
        if seat:
            entry["seat"] = seat
        out.append(entry)
    return out


def _inside(ring_, x, z):
    """Whether (x, z) lies inside the ring, by the even-odd rule."""
    hit = False
    for i in range(len(ring_)):
        (x1, z1), (x2, z2) = ring_[i], ring_[(i + 1) % len(ring_)]
        if (z1 > z) != (z2 > z) and x < x1 + (z - z1) * (x2 - x1) / (z2 - z1):
            hit = not hit
    return hit


def coast_edits(ring_, edges, seed=1):
    """`editShapes` ops that insert points along named edges of a compiled ring, each pulled a few blocks
    inward — a coast drawn point by point, leaving every edge not named (a seam, a frontline) exactly as the
    plan cut it. `edges` maps an edge's starting vertex index in the ORIGINAL ring to a list of
    (t, inward) pairs: t the fraction along the edge, inward the blocks pulled toward the ring's centre.
    Returns the ops in order, with indices stated against the ring as it stands after each insert."""
    pts = [list(p) for p in ring_]
    ops, shift = [], 0
    for start in sorted(edges):
        a, b = ring_[start], ring_[(start + 1) % len(ring_)]
        at = start + shift
        for t, inward in sorted(edges[start]):
            x, z = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            # pull perpendicular to the edge, toward the inside. The inside is the side a point just off the
            # edge falls in the ring, not the side the centroid is on: on a ring that is not convex the
            # centroid can lie across an edge, and a pull toward it pushes the coast out.
            ex, ez = b[0] - a[0], b[1] - a[1]
            px, pz = -ez, ex
            pn = math.hypot(px, pz) or 1
            px, pz = px / pn, pz / pn
            if not _inside(ring_, x + px * 0.5, z + pz * 0.5):
                px, pz = -px, -pz
            ops.append({"after": at, "x": round(x + px * inward, 1), "z": round(z + pz * inward, 1)})
            at += 1
            shift += 1
    return ops
