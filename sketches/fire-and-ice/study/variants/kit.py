"""Shared kit for the terrain variants of the ice map.

The map as it stands, lofts from lines (the author's own construction: ordered lines, a ruled strip between each
consecutive pair), their blocks and low-poly triangles, the checks every variant reports, an iso render, and the
one export the 3D viewer reads. Coordinates are Minecraft blocks: x east, y up, z south.

    import sys; sys.path.insert(0, "sketches/fire-and-ice/study/variants"); import kit
"""
import collections
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.dirname(HERE)                 # the study folder
sys.path.insert(0, os.path.dirname(SCRATCH))   # the fire-and-ice sketch folder: loft.py
sys.path.insert(0, os.path.join(SCRATCH, "rec"))
import loft  # noqa: E402  curve(points, step) and resample(samples, n): centripetal Catmull-Rom

SHIFT = [0, 0]                          # how far the turned half is moved away, in blocks of x and z (set_shift)
PIVOT = (59.5, 86.5)                    # the map turns 180 degrees about this point: (x, z) -> (119 - x, 173 - z)
CUT = (75 / math.hypot(75, 29), -29 / math.hypot(75, 29))   # direction of the line between the two halves
NORMAL = (-CUT[1], CUT[0])              # across that line; the built half lies where across() < 0

WOOL = {"white": 0, "orange": 1, "magenta": 2, "lightblue": 3, "yellow": 4, "lime": 5, "pink": 6, "grey": 7,
        "lightgrey": 8, "cyan": 9, "purple": 10, "blue": 11, "brown": 12, "green": 13, "red": 14, "black": 15}
HEX = {0: "#e4e8e8", 1: "#e8761c", 2: "#b84db0", 3: "#4aaed6", 4: "#efc12f", 5: "#76b52a", 6: "#e892ad", 7: "#4a5053",
       8: "#9a9a92", 9: "#1f8d96", 10: "#7b35ab", 11: "#3a3f9e", 12: "#77502f", 13: "#58702a", 14: "#a8302b", 15: "#25272b"}


def set_shift(dx, dz):
    """Move the turned half `dx`, `dz` whole blocks (the built half stays where it is). The turn becomes
    (x, z) -> (119 + dx - x, 173 + dz - z), the pivot moves by half of that, and the gap between the halves widens by
    about dx * 0.36 + dz * 0.93 blocks. (0, 0) is the author's map as uploaded."""
    global PIVOT
    SHIFT[0], SHIFT[1] = int(dx), int(dz)
    PIVOT = ((119 + SHIFT[0]) / 2, (173 + SHIFT[1]) / 2)


def across(x, z):
    """Signed distance from the line between the halves (through the current pivot); negative on the built half's side."""
    return (x - PIVOT[0]) * NORMAL[0] + (z - PIVOT[1]) * NORMAL[1]


def turn(p):
    """A point or block of the built half carried onto the other half, with the current shift."""
    if len(p) == 2: return (119 + SHIFT[0] - p[0], 173 + SHIFT[1] - p[1])
    return (119 + SHIFT[0] - p[0], p[1], 173 + SHIFT[1] - p[2])


# ---------------------------------------------------------------- the map as it stands
_MAP = None


def existing(full=False):
    """{(x, y, z): (layer name, group)} of every block in the author's map (markers left out). `full` adds the turned
    half. Groups: Gelände, Untergrund, Bauwerke."""
    global _MAP
    if _MAP is None:
        d = json.load(open(os.path.join(SCRATCH, "viewer", "map.json")))
        L, P, B = d["layers"], d["palette"], d["blocks"]
        _MAP = {}
        for i in range(0, len(B), 4):
            layer = L[P[B[i + 3] >> 1][0]]
            if layer["key"] == "marks": continue
            _MAP[(B[i], B[i + 1], B[i + 2])] = (layer["name"], layer["group"])
        for c in _marker_blocks(_MAP): del _MAP[c]
    if not full: return dict(_MAP)
    out = dict(_MAP)
    for c, v in _MAP.items(): out[turn(c)] = v
    return out


def _marker_blocks(blocks):
    """The author's centre-line markers (the lapis and the 2x2 stone at the pivot): tiny clusters of at most 8 blocks
    within 30 blocks of the line between the halves. They mark the line only, so the map is read without them."""
    left, out = set(blocks), []
    while left:
        seed = left.pop(); comp, todo = [seed], [seed]
        while todo:
            x, y, z = todo.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        q = (x + dx, y + dy, z + dz)
                        if q in left: left.remove(q); comp.append(q); todo.append(q)
        if len(comp) <= 8 and all(abs((c[0] - 59.5) * NORMAL[0] + (c[2] - 86.5) * NORMAL[1]) <= 30 for c in comp):
            out += comp
    return out


def tops(blocks):
    """{(x, z): highest y} over a block set or dict."""
    out = {}
    for x, y, z in blocks:
        if y > out.get((x, z), -999): out[(x, z)] = y
    return out


LANE_CORNER = (97, 53)                  # where the wool lane runs out of the underground on the gap's east end


def along(x, z):
    """Position along the line between the halves, measured from the current pivot."""
    return (x - PIVOT[0]) * CUT[0] + (z - PIVOT[1]) * CUT[1]


def _inside(poly, x, y):
    hit = False
    for k in range(len(poly)):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): hit = not hit
    return hit


def span():
    """The polygon the middle may fill, as a list of (x, z) corners: the built half's edge that faces the other half,
    the turned copy of that edge, and the two straight lines joining their outermost points. The facing edge is every
    column on the half's front (the one nearest the line at each place along it) from which a straight look across the
    line meets the other half; its east end is the corner where the wool lane runs out of the underground."""
    half = {(x, z) for x, y, z in existing()}
    turned = {turn(c) for c in half}
    reach = 34 + max(0, SHIFT[0] * NORMAL[0] + SHIFT[1] * NORMAL[1])
    front = {}
    for x, z in half:
        b = round(along(x, z)); a = across(x, z)
        if b not in front or a > front[b][0]: front[b] = (a, (x, z))
    def sees(c):
        return any((round(c[0] + NORMAL[0] * k), round(c[1] + NORMAL[1] * k)) in turned for k in range(1, int(reach) + 1))
    edge = [front[b][1] for b in sorted(front) if sees(front[b][1])]
    corner = along(*LANE_CORNER)
    edge = [c for c in edge if along(*c) < corner] + [LANE_CORNER]
    return edge + [turn(c) for c in edge]


def middle_gap(reach=None):
    """Columns the middle is to fill: every column inside `span()` that holds no block of either half. This is the
    whole of the middle; nothing beside it, and no hole in the author's own ground, belongs to it."""
    poly = span()
    occupied = {(x, z) for x, y, z in existing(full=True)}
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    cells = {(x, z) for x in range(int(min(xs)), int(max(xs)) + 1) for z in range(int(min(zs)), int(max(zs)) + 1)
             if (x, z) not in occupied and _inside(poly, x, z)}
    return {c for c in cells | {turn(c) for c in cells} if c not in occupied}     # symmetric where the test rounds


# ---------------------------------------------------------------- lofts: lines in, surface out
def strip_grid(lines, step=1.0):
    """The loft through `lines` (each an ordered list of (x, y, z) points, consecutive lines joined by a ruled strip)
    as rows of points: every line is splined through its points and resampled by arc length to one shared count."""
    curves = [loft.curve(l, step=0.3) if len(l) > 1 else [tuple(map(float, l[0]))] for l in lines]
    length = max(sum(math.dist(a, b) for a, b in zip(c, c[1:])) for c in curves)
    n = max(2, math.ceil(length / step) + 1)
    return [loft.resample(c, n) if len(c) > 1 else c * n for c in curves]


def loft_tris(lines, step=2.0):
    """Low-poly triangles of the loft: about one quad per `step` blocks along the lines, one per strip across."""
    rows = strip_grid(lines, step)
    tris = []
    for r0, r1 in zip(rows, rows[1:]):
        for (p0, q0), (p1, q1) in zip(zip(r0, r1), zip(r0[1:], r1[1:])):
            tris += [(p0, q0, p1), (q0, q1, p1)]
    return tris


def loft_blocks(lines, thickness=2, step=0.35):
    """Blocks of the loft: each sample of the surface marks its block and the `thickness - 1` below it."""
    rows = strip_grid(lines, step)
    out = set()
    for r0, r1 in zip(rows, rows[1:]):
        for p, q in zip(r0, r1):
            m = max(1, int(math.dist(p, q) / step))
            for k in range(m + 1):
                t = k / m
                x, y, z = (p[i] + (q[i] - p[i]) * t for i in range(3))
                bx, by, bz = math.floor(x + 0.5), math.floor(y + 0.5), math.floor(z + 0.5)
                for d in range(thickness): out.add((bx, by - d, bz))
    return out


# ---------------------------------------------------------------- checks every variant reports
def checks(new_blocks, full=True, region=None):
    """The readings a variant is judged on, as a dict:
    overlap   new blocks inside existing ones (a collision with the author's build), with up to 12 positions
    steps     histogram of height steps between 4-neighbouring columns of the new ground's top surface
    walls     columns where the new top drops 4 or more to a neighbour: the vertical walls the author rejects
    void      columns of `region` (default: the middle gap) the new ground leaves open
    seams     height difference where the new top meets an existing top next to it: histogram
    outside   columns of the new ground that lie outside `region` (for the middle: ground spread sideways beyond the
              space between the two halves, which the author rules out); 0 when `region` is empty
    """
    old = existing(full)
    new = set(new_blocks)
    hit = sorted(new & set(old))
    top = tops(new)
    steps, walls = collections.Counter(), []
    for (x, z), y in top.items():
        for dx, dz in ((1, 0), (0, 1)):
            o = top.get((x + dx, z + dz))
            if o is None: continue
            steps[abs(o - y)] += 1
            if abs(o - y) >= 4: walls.append((x, y, z))
    old_top = tops(old)
    seams = collections.Counter()
    for (x, z), y in top.items():
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            o = old_top.get((x + dx, z + dz))
            if o is not None and (x + dx, z + dz) not in top: seams[abs(o - y)] += 1
    region = middle_gap() if region is None else set(region)
    void = sorted(c for c in region if c not in top)
    outside = sorted(c for c in top if region and c not in region)
    return {"outside": len(outside), "outside_at": outside[:12],"overlap": len(hit), "overlap_at": hit[:12], "steps": dict(sorted(steps.items())),
            "walls": len(walls), "walls_at": walls[:12], "void": len(void), "void_at": void[:12],
            "seams": dict(sorted(seams.items()))}


def exposed(cover):
    """For the cover: faces of the main building that still see the sky with `cover` laid on it, as
    {"top": n, "side": n, "at": [up to 20 block positions]}. Faces toward the facade and the labelled openings, the
    designed roofs (checkerboard at y 59 and up, the black roof) and the antenna (above y 72) are not counted; every
    other face that stays open is a wall, stairwell or slab the cover leaves bare."""
    old = existing()
    labels = json.load(open(os.path.join(SCRATCH, "labels", "labels.json")))["labels"]
    front = set()
    for l in labels:
        if l["kind"] in ("facade", "opening"):
            c = l["cells"]; front |= {(c[i], c[i + 1], c[i + 2]) for i in range(0, len(c), 3)}
    building = {c for c, (n, g) in old.items() if g == "Bauwerke" and -16 <= c[0] <= 53 and -23 <= c[2] <= 48
                and not (n == "Schwarz" or (n == "Hellgrau und Ton" and c[1] >= 59) or c[1] > 72)}
    solid = set(old) | set(cover)
    top = tops(solid)
    out, at = collections.Counter(), []
    for x, y, z in building:
        for d in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
            n = (x + d[0], y + d[1], z + d[2])
            if n in solid or n in front: continue
            if top.get((n[0], n[2]), -999) < n[1]:
                out["top" if d[1] else "side"] += 1; at.append((x, y, z))
    return {"top": out["top"], "side": out["side"], "at": sorted(set(at))[:20]}


COVER_FLOOR = 48        # walk level of the highest exit in the facade (the opening over the core, floor block y 47)
FLAT_ROOF = 59          # the checkerboard roof's top
PENTHOUSE = (8, 30, 21, 47)   # x0, x1, z0, z1 under the black roof
ROOF_OUTLINE = (12, 32, -22, 20)   # x0, x1, z0, z1 of the main checkerboard roof, its slots included


def cover_rules(cover):
    """The author's rules for the cover, as readings. The map is hollow: every stairwell and room behind the facade is
    later sunk into solid ground, so the cover is one surface laid over the whole building.
    below_floor   building columns behind the facade whose surface lies under COVER_FLOOR, or whose highest block is
                  building rather than ground (the author's or the cover's): the building pokes up bare — must be 0
    roof_seam     histogram of the cover's height minus FLAT_ROOF where it meets the checkerboard roof — 0 is flush
    mountain_seam histogram of height differences where the cover meets the author's light-blue mountain — 0–1 flush
    penthouse     cover blocks at y 61 or above within one block of the black-roofed penthouse — must be 0
    """
    old = existing()
    new = set(cover)
    new_top, old_top = tops(new), tops(old)
    roof = {(x, z) for (x, y, z), (n, g) in old.items() if n == "Hellgrau und Ton" and y >= FLAT_ROOF}
    house = {(x, z) for x in range(PENTHOUSE[0], PENTHOUSE[1] + 1) for z in range(PENTHOUSE[2], PENTHOUSE[3] + 1)}
    behind = {(x, z) for (x, y, z), (n, g) in old.items()
              if g == "Bauwerke" and -16 <= x <= 25 and -23 <= z <= 48 and y <= 72} - roof - house
    ground_top = tops({b for b, (n, g) in old.items() if g == "Gelände"} | new)
    below = []
    for c in sorted(behind):
        top = max(new_top.get(c, -999), old_top.get(c, -999))
        # covered: the highest block there is ground (the author's or the cover's), at COVER_FLOOR or above
        if top < COVER_FLOOR or ground_top.get(c, -999) < old_top.get(c, -999):
            below.append(c)
    near = lambda c: [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)]
    roof_seam, mountain_seam = collections.Counter(), collections.Counter()
    blue = {(x, z): y for (x, y, z), (n, g) in old.items() if n == "Hellblau" and y >= old_top.get((x, z), -999)}
    for c, y in new_top.items():
        for n in near(c):
            if n in roof and n not in new_top: roof_seam[y - FLAT_ROOF] += 1
            if n in blue and n not in new_top: mountain_seam[abs(blue[n] - y)] += 1
    wrap = [c for c in new if c[1] >= 61 and PENTHOUSE[0] - 1 <= c[0] <= PENTHOUSE[1] + 1 and PENTHOUSE[2] - 1 <= c[2] <= PENTHOUSE[3] + 1]
    return {"below_floor": len(below), "below_floor_at": below[:15], "roof_seam": dict(sorted(roof_seam.items())),
            "mountain_seam": dict(sorted(mountain_seam.items())), "penthouse": len(wrap), "penthouse_at": sorted(wrap)[:10], "behind_columns": len(behind)}


# ---------------------------------------------------------------- pictures
def render(new, path, q=0, scale=3, box=None, full=True, colours=None):
    """Iso picture of the author's map with `new` ({(x, y, z): wool data} or a set, drawn white) on it. `q` turns the
    view by quarters; `box` = (x0, x1, y0, y1, z0, z1) crops."""
    tools = os.path.normpath(os.path.join(SCRATCH, "..", "..", "..", "tools"))
    sys.path.insert(0, tools); sys.path.insert(0, os.path.join(tools, "render"))
    from png import Canvas, write_png
    from iso import turned, _visible, iso_bounds, draw_iso, BACKGROUND
    grey = {"Gelände": (150, 160, 150), "Untergrund": (120, 110, 105), "Bauwerke": (95, 95, 100)}
    blocks = {c: grey[g] for c, (n, g) in existing(full).items()}
    for c in new:
        d = new[c] if isinstance(new, dict) else 0
        h = HEX[d]; blocks[c] = tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    if box: blocks = {c: v for c, v in blocks.items() if all(box[2 * i] <= c[i] <= box[2 * i + 1] for i in range(3))}
    b = turned(blocks, q); W, H, K = scale, scale // 2 or 1, scale
    sh = {c: b[c] for c in _visible(b)}
    u0, u1, v0, v1 = iso_bounds(sh, W, H, K)
    cv = Canvas(int(u1 - u0) + 40, int(v1 - v0) + 40, BACKGROUND); draw_iso(cv, sh, (20 - u0, 20 - v0), W, H, K)
    write_png(path, cv)


# ---------------------------------------------------------------- the export the viewer reads
def _segment_distance(p, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / ((dx * dx + dz * dz) or 1)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dz)


def mesh_outside(pieces, slot, tolerance=2.0):
    """Points of the pieces' lofts (their surface as the viewer draws it, not only their blocks) that lie more than
    `tolerance` blocks outside where the slot may build: for the middle, outside `span()`; for the cover, away from
    the pieces' own block columns. Returns the list of offending (x, z)."""
    pts = [(p[0], p[2]) for piece in pieces for lines in piece["lofts"] for t in loft_tris(lines) for p in t]
    if slot == "middle":
        poly = span()
        return [p for p in pts if not _inside(poly, *p)
                and min(_segment_distance(p, poly[k], poly[(k + 1) % len(poly)]) for k in range(len(poly))) > tolerance]
    cols = {(x, z) for piece in pieces for x, y, z in piece["blocks"]}
    reach = int(math.ceil(tolerance))
    return [p for p in pts if not any((round(p[0]) + a, round(p[1]) + b) in cols
                                      for a in range(-reach, reach + 1) for b in range(-reach, reach + 1))]


DOORS = ("op-stair-south", "op-hall-east", "op-core-top", "op-core-pit")   # the building's real ways out


def doorways():
    """The mouths of the building's real exits: {(x, y, z): (dx, dz)}, an air cell of the opening and the direction
    in which it opens onto the outside."""
    old = existing()
    labels = {l["id"]: l for l in json.load(open(os.path.join(SCRATCH, "labels", "labels.json")))["labels"]}
    out = {}
    for name in DOORS:
        c = labels[name]["cells"]; cells = {(c[i], c[i + 1], c[i + 2]) for i in range(0, len(c), 3)}
        for x, y, z in cells:
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y, z + dz)
                if n not in old and n not in cells: out[(x, y, z)] = (dx, dz)
    return out


def door_blocks(cover, reach=3):
    """Cover blocks standing in a doorway of the building's real exits or within `reach` blocks in front of it, at the
    doorway's height: an exit the cover shuts or walls off. Must be empty."""
    new = set(cover)
    hits = set()
    for (x, y, z), (dx, dz) in doorways().items():
        for k in range(0, reach + 1):
            c = (x + dx * k, y, z + dz * k)
            if c in new: hits.add(c)
    return sorted(hits)


def gate(slot, pieces, absolute):
    """Every hard rule a variant must meet before it may be written, as a list of failures (empty = may be written)."""
    blocks = set().union(*[set(p["blocks"]) for p in pieces]) if pieces else set()
    fails = []
    if slot == "middle":
        if not absolute: fails.append("a middle variant is written with absolute=True")
        c = checks(blocks)
        for key in ("outside", "overlap", "walls", "void"):
            if c[key]: fails.append(f"{key} {c[key]}, e.g. {c[key + '_at'][:4] if key + '_at' in c else ''}")
        if any(turn(b) not in blocks for b in blocks): fails.append("not exactly 180-degree symmetric")
    else:
        if absolute or SHIFT != [0, 0]: fails.append("a cover variant is written with shift (0, 0) and absolute=False")
        c = checks(blocks, full=False, region=[])
        for key in ("overlap", "walls"):
            if c[key]: fails.append(f"{key} {c[key]}, e.g. {c[key + '_at'][:4]}")
        r = cover_rules(blocks)
        terrain = {3, 4, 5, 13}
        inroof = sorted(b for p in pieces if p["wool"] in terrain for b in p["blocks"]
                        if ROOF_OUTLINE[0] <= b[0] <= ROOF_OUTLINE[1] and ROOF_OUTLINE[2] <= b[2] <= ROOF_OUTLINE[3] and b[1] <= FLAT_ROOF)
        if inroof: fails.append(f"{len(inroof)} terrain blocks run into the checkerboard roof at roof level, e.g. {inroof[:4]}: "
                                "cover the roof from above or stop at its edge; close a slot in the roof as roof (light grey), never as terrain")
        for key in ("below_floor", "penthouse"):
            if r[key]: fails.append(f"{key} {r[key]}, e.g. {r[key + '_at'][:4]}")
        shut = door_blocks(blocks)
        if shut: fails.append(f"{len(shut)} cover blocks shut an exit of the building or stand in front of it, e.g. {shut[:4]}: "
                              "the exits in kit.DOORS stay open, with the terrain meeting their threshold")
    stray = mesh_outside(pieces, slot)
    if stray: fails.append(f"{len(stray)} loft points lie more than 2 blocks outside the allowed area, e.g. "
                           f"{[tuple(round(v, 1) for v in p) for p in stray[:4]]}: the lofts themselves, not only the "
                           "blocks, must stay inside")
    return fails


def write(variant_id, slot, title, summary, pieces, absolute):
    """Write <variants>/<variant_id>/variant.json.

    slot      "middle" or "cover": which missing part this variant fills
    title     two to five words, German, as the viewer's button shows it
    summary   two or three German sentences: the idea and what a player meets there
    pieces    [{"name": str, "note": str, "wool": data 0..15, "lofts": [[line, line, ...], ...], "blocks": {(x,y,z)}}]
              every loft is an ordered list of lines; "blocks" are the piece's blocks (normally the union of
              loft_blocks over its lofts, plus anything hand-placed)
    The current set_shift() is written with it; a cover variant must be written with shift (0, 0).
    absolute  True when the pieces already hold both halves (the middle, built symmetric); False when they hold the
              built half only and the viewer turns them onto the other half (the cover)
    Refuses to write (raises ValueError) while `gate()` reports a failure: only a correct variant is delivered.
    """
    fails = gate(slot, pieces, absolute)
    if fails:
        raise ValueError("variant not written, it breaks the author's rules:\n  - " + "\n  - ".join(fails))
    q = lambda p: [round(p[0] * 10), round((p[1] + 0.5) * 10), round(p[2] * 10)]   # drawn at the blocks' top face
    layers, blocks = [], []
    for index, piece in enumerate(pieces):
        meshes = []
        for lines in piece["lofts"]:
            tris = loft_tris(lines)
            curves = [loft.curve(l, step=1.0) if len(l) > 1 else l for l in lines]
            meshes.append({"tris": [v for t in tris for p in t for v in q(p)],
                           "lines": [[v for p in c for v in q(p)] for c in curves],
                           "points": [v for l in lines for p in l for v in q(p)]})
        layers.append({"name": piece["name"], "note": piece.get("note", ""), "colour": HEX[piece["wool"]], "wool": piece["wool"],
                       "blocks": len(piece["blocks"]), "meshes": meshes,
                       "lines": sum(len(ls) for ls in piece["lofts"]), "points": sum(len(l) for ls in piece["lofts"] for l in ls)})
        blocks += [[x, y, z, index] for x, y, z in sorted(piece["blocks"])]      # the last number is the piece's index
    os.makedirs(os.path.join(HERE, variant_id), exist_ok=True)
    out = {"id": variant_id, "surface": "top", "slot": slot, "title": title, "summary": summary, "absolute": absolute, "shift": list(SHIFT),
           "layers": layers, "blocks": [v for b in blocks for v in b]}
    json.dump(out, open(os.path.join(HERE, variant_id, "variant.json"), "w"), separators=(",", ":"))
    return os.path.join(HERE, variant_id, "variant.json")


def symmetric(pieces):
    """The pieces with their 180-degree copy added: lines and blocks turned onto the other half, blocks deduplicated."""
    out = []
    for piece in pieces:
        lofts = list(piece["lofts"]) + [[[turn(p) for p in line] for line in lines] for lines in piece["lofts"]]
        out.append(dict(piece, lofts=lofts, blocks=set(piece["blocks"]) | {turn(c) for c in piece["blocks"]}))
    return out
