"""The layer document: a board stated as data and built in order, every step kept.

    doc = json.load(open("island.layers.json"))
    built = document.build(doc)            # built.world, built.H, built.land, built.water, built.steps
    for step in built.steps:               # one per layer, in the order they ran
        step.id, step.stage, step.changed  # what the layer is called, where it ran, the columns it changed

**A layer is one operation, its numbers and the areas it works in.** Every area of a layer does the same thing
with the same numbers; an area may state its own `rise` or `depth`. An area is a `circle`, an `ellipse`, a
`polygon`, a `rect`, a `line` with a width, or `board` for everywhere, and `rough` bends any of them. The
operation reads one distance from it, 0 at the centre or the deepest point and 1 on the rim, so any area carries
any operation.

**Four words say how a layer meets the ground and itself.** `mode` is set, lift or cut. `join` is the p by which
the areas of one layer melt into each other, 0 the plain maximum. `melt` is the k in blocks over which a form with
a surface of its own (a crater, a level top) rounds into the ground. `soft` is the outer share of each area over
which the change eases to nothing.

**The stages run in a fixed order:** `fields` (named noise), `ground` (heights), `paint` (the top, first layer
that applies wins), `lay`, `water`, `build` (paths' surfaces and steps, walls, hedges, fences), `dress` (trees, kept
`clear` blocks off everything built). A layer that names another (`near`) reads the area or line that layer was given.
"""
from dataclasses import dataclass, field as _field

import numpy as np
from scipy import ndimage

from . import field as F
from . import landform as LF
from . import noise
from . import route as RT
from . import shapes
from . import terrain as T
from .blocks import B
from .build import line_wall
from .world import World

STAGES = ("ground", "paint", "lay", "water", "build", "dress")


@dataclass
class Step:
    """One layer as it ran: its id, its stage, the heights after it (ground) and the columns it changed."""
    id: str
    stage: str
    op: str
    changed: np.ndarray
    H: np.ndarray = None
    note: str = ""


@dataclass
class Built:
    world: World
    H: np.ndarray
    land: np.ndarray
    water: np.ndarray
    X: np.ndarray
    Z: np.ndarray
    steps: list = _field(default_factory=list)
    lines: dict = _field(default_factory=dict)


def block(spec):
    """A block from "NAME" or ["NAME", data] or [id, data]."""
    if isinstance(spec, str):
        return (getattr(B, spec), 0)
    name, data = spec
    return (getattr(B, name) if isinstance(name, str) else int(name), int(data))


def _field(spec, shape, fields):
    """A named field, or one stated in place: {"fbm": {cell, octaves, seed}}, {"ridged": {...}}, a number."""
    if isinstance(spec, (int, float)):
        return np.full(shape, float(spec))
    if isinstance(spec, str):
        return fields[spec]
    (kind, a), = spec.items()
    if kind == "fbm":
        return noise.fbm(shape, a["cell"], a.get("octaves", 3), seed=a.get("seed", 0))
    if kind == "ridged":
        return noise.ridged(shape, a["cell"], a.get("octaves", 3), seed=a.get("seed", 0))
    if kind == "line":
        return noise.line(shape, a["along"], a["cell"], octaves=a.get("octaves", 2), seed=a.get("seed", 0),
                          amp=a.get("amp", 1.0), base=a.get("base", 0.0),
                          clip=tuple(a["clip"]) if "clip" in a else None)
    raise ValueError(f"unknown field {kind}")


def area_distance(area, X, Z, fields, lines):
    """(e, scale): 0 at the area's centre or deepest point, 1 on its rim, over 1 outside; `scale` is how many
    blocks one unit of e spans, for an operation that measures in blocks."""
    Xf, Zf = X.astype(float), Z.astype(float)
    (kind, a), = ((k, v) for k, v in area.items() if k not in ("rough", "rise", "depth", "top"))
    if kind == "board":
        e, scale = np.zeros(X.shape), 1.0
    elif kind == "circle":
        e, scale = np.hypot(Xf - a["at"][0], Zf - a["at"][1]) / a["r"], float(a["r"])
    elif kind == "ellipse":
        e = shapes.ellipse_distance(Xf, Zf, tuple(a["at"]), a["rx"], a["rz"], angle=a.get("angle", 0.0))
        scale = float(max(a["rx"], a["rz"]))
    elif kind in ("polygon", "rect"):
        poly = a if kind == "polygon" else [(a[0], a[1]), (a[2], a[1]), (a[2], a[3]), (a[0], a[3])]
        inside = shapes.inside(Xf, Zf, [tuple(p) for p in poly])
        depth = shapes.distance_in(inside, "euclid")
        scale = float(max(depth.max(), 1.0))
        e = np.where(inside, 1 - depth / scale, 1 + shapes.edge_distance(Xf, Zf, [tuple(p) for p in poly]) / scale)
    elif kind == "line":
        pts = lines[a["near"]]["pts"] if "near" in a else noise.spline([tuple(p) for p in a["pts"]], 1.0) \
            if a.get("spline", True) else [tuple(p) for p in a["pts"]]
        d, _ = shapes.polyline(Xf, Zf, pts)
        half = a.get("width", lines[a["near"]]["width"] if "near" in a else 2) / 2
        e, scale = d / half, float(half)
    else:
        raise ValueError(f"unknown area {kind}")
    if "rough" in area:
        r = area["rough"]
        e = e + r.get("amp", 0.12) * noise.fbm(X.shape, r.get("cell", 6), 2, seed=r.get("seed", 0))
    return e, scale


def _ground_layer(L, H, X, Z, fields, lines, land):
    """The heights after one ground layer, and the water it holds (or None)."""
    op, mode = L["op"], L.get("mode")
    Xf, Zf = X.astype(float), Z.astype(float)
    if op == "base":
        parts = []
        for t in L.get("terms", []):
            (kind, a), = t.items()
            if kind == "ramp":
                parts.append(F.Ramp(a["along"], a["from"], a["to"], a["rise"]))
            elif kind == "gauss":
                parts.append(F.Gauss(tuple(a["at"]), a["r"], a["rise"], rz=a.get("rz"), angle=a.get("angle", 0.0)))
            elif kind == "tilt":
                parts.append(F.Tilt(a["dx"], a["dz"], tuple(a.get("at", (0, 0)))))
            elif kind == "noise":
                parts.append(F.Noise(_field(a["field"], X.shape, fields), a["rise"]))
        return F.terms(Xf, Zf, float(L["height"]), *parts), None
    if op == "river":
        pts = [tuple(p) for p in noise.spline([tuple(p) for p in L["line"]], 0.5)]
        lines[L["id"]] = dict(pts=pts, width=L.get("width", 6))
        H2, river = LF.watercourse(H, Xf, Zf, pts, width=L.get("width", 6), depth=L.get("depth", 3),
                                   water=L.get("water", 2), bank=L.get("bank", 2))
        return H2, np.where(river.mask & land, river.surface, 0).astype(int)
    if op == "path":
        pts = [tuple(p) for p in noise.spline([tuple(p) for p in L["line"]], 1.0)]
        H2, prof = LF.grade(H, Xf, Zf, pts, width=L.get("width", 3), max_grade=L.get("max_grade", 0.25),
                            shoulder=L.get("shoulder", 2))
        lines[L["id"]] = dict(pts=pts, width=L.get("width", 3), profile=prof)
        return H2, None
    areas = L.get("areas", [{"board": {}}])
    changes, es = [], []
    for area in areas:
        e, scale = area_distance(area, X, Z, fields, lines)
        es.append(e)
        if op == "mound":
            rise = area.get("rise", L["rise"])
            c = np.where(e < 1, rise * (1 - np.clip(e, 0, 1) ** L.get("power", 1.6)), 0.0)
        elif op == "crater":
            bowl = L["floor"] + L.get("slope", 1.0) * np.maximum(0, e * scale - L.get("flat", 0.0))
            bowl = bowl + np.where(e > 1, 1000 * (e - 1), 0)          # nothing past the rim but the seam
            c = LF.smooth_min(H, bowl, L.get("melt", 0)) - H
        elif op == "level":
            top = area.get("top", L.get("top", "median"))
            c = LF.level(H, e, top, inner=L.get("inner", 1.0), outer=L.get("outer", 1.5), mode=mode or "set") - H
        elif op == "noise":
            c = np.where(e < 1, L["rise"] * _field(L["field"], X.shape, fields), 0.0)
        else:
            raise ValueError(f"unknown ground op {op}")
        changes.append(c)
    cut = all((c <= 0).all() for c in changes) and any((c < 0).any() for c in changes)
    if op in ("mound", "crater") and len(changes) > 1:
        change = LF.join(changes, p=L.get("join", 0), cut=cut)
    else:
        change = changes[0] if len(changes) == 1 else np.where(np.abs(changes[0]) >= np.abs(changes[1]),
                                                               changes[0], changes[1])
        for c in changes[2:]:
            change = np.where(np.abs(change) >= np.abs(c), change, c)
    if "soft" in L:
        change = change * noise.smoothstep(1.0, 1.0 - L["soft"], np.minimum.reduce(es))
    if mode == "lift":
        change = np.maximum(change, 0)
    elif mode == "cut":
        change = np.minimum(change, 0)
    return H + change, None


def _paint_layer(P, X, Z, fields, lines, H):
    where = None
    if "area" in P:
        e, _ = area_distance(P["area"], X, Z, fields, lines)
        where = e < 1
    values = []
    if "noise" in P:
        n = P["noise"]
        values.append((_field(n["field"], X.shape, fields), n.get("lo"), n.get("hi")))
    if "height" in P:
        lo, hi = P["height"]
        values.append((H, lo, hi))
    return T.Paint(block(P["block"]), slope=tuple(P["slope"]) if "slope" in P else None, where=where,
                   values=values)


def build(doc):
    """Build a layer document: every stage in order, every layer recorded as a Step."""
    bd = doc["board"]
    (x0, x1), (z0, z1) = bd["x"], bd["z"]
    w = World(x0, z0, x1 - x0 + 1, z1 - z0 + 1, sy=bd.get("height", 128))
    X, Z = w.grid()
    fields = {k: _field(v, X.shape, {}) for k, v in doc.get("fields", {}).items()}
    lines = {}
    land = np.ones(X.shape, bool)
    H = np.full(X.shape, float(bd.get("floor", 40)))
    water = np.zeros(X.shape, int)
    out = Built(w, H, land, water, X, Z, lines=lines)
    for L in doc.get("ground", []):
        before = H.copy()
        if L["op"] == "outline":
            ins = {k: (_field(v, X.shape, fields) if isinstance(v, (dict, str)) else v)
                   for k, v in L.get("insets", {}).items()}
            land = shapes.island(X, Z, tuple(L["box"]), **ins)
            out.steps.append(Step(L["id"], "ground", "outline", land.copy(), H.copy(), L.get("note", "")))
            continue
        H, wet = _ground_layer(L, H, X, Z, fields, lines, land)
        if wet is not None:
            water = np.where(wet > 0, wet, water)
        out.steps.append(Step(L["id"], "ground", L["op"], (np.abs(H - before) > 0.5) & land, H.copy(),
                              L.get("note", "")))
    Hi = np.round(H).astype(int)
    Hi = np.where(water > 0, np.minimum(Hi, water - 1), Hi)
    paint = [_paint_layer(P, X, Z, fields, lines, Hi) for P in doc.get("paint", [])]
    lay = doc.get("lay", {})
    bottom = None
    if "underside" in lay:
        u = lay["underside"]
        bottom = T.island_bottom(Hi, land, np.zeros(X.shape, bool), taper=tuple(u.get("taper", (4, 0.9))),
                                 rough=u.get("rough", 0) * noise.fbm(X.shape, 12, 2, seed=u.get("seed", 0)))
    rock = T.Strata([((B.STONE, 0), 3, 6), ((B.STONE, 5), 1.4, 3)], length=60, seed=7, start=-300)
    T.lay(w, np.where(land, Hi, -1), land, top=T.by_angle([(55, (B.GRASS, 0)), (90, (B.STONE, 0))]),
          bands=T.beds(rock, Hi, seed=3), paint=paint, bottom=bottom)
    out.steps.append(Step("lay", "lay", "lay", land.copy(), Hi.copy(), f"{len(paint)} paint layers"))
    if (water > 0).any():
        bed = [_paint_layer(P, X, Z, fields, lines, Hi) for P in doc.get("water", {}).get("bed", [])] or (B.GRAVEL, 0)
        T.fill_water(w, Hi, np.where(land, water, 0), bed=bed, mask=land)
        out.steps.append(Step("water", "water", "fill_water", (water > 0) & land, Hi.copy()))
    rng = np.random.default_rng(bd.get("seed", 0))
    built_on = np.zeros(X.shape, bool)
    for L in doc.get("build", []):
        laid = np.zeros(X.shape, bool)
        if L["op"] == "surface":
            ln = lines[L["near"]]
            surf = [block(b) for b in L.get("blocks", ["GRAVEL"])]
            RT.pave(w, Hi, X, Z, ln["pts"], width=ln["width"], surface=surf,
                    weights=L.get("weights", [1] * len(surf)), seed=bd.get("seed", 0))
            if L.get("steps") == "stairs":
                RT.steps(w, Hi, X, Z, ln["pts"], block=getattr(B, L.get("stair", "COBBLE_STAIRS")), width=ln["width"])
            elif L.get("steps") == "half":
                band, lvl, _ = RT.halfstep_levels(X, Z, ln["pts"], ln["profile"], ln["width"], within=land)
                RT.halfsteps(w, Hi, X, Z, band, lvl, surf, block(L.get("slab", ["SLAB", 0])), rng,
                             fill=surf[0])
            laid = shapes.polyline(X.astype(float), Z.astype(float), ln["pts"])[0] <= ln["width"] / 2
        elif L["op"] == "wall":
            pts = lines[L["near"]]["pts"] if "near" in L else [tuple(p) for p in L["line"]]
            if "offset" in L:
                pts = _offset(pts, L["offset"])
            got = line_wall(w, Hi, X, Z, pts, height=L.get("height", 2), width=L.get("width", 1),
                            crown=L.get("crown", "follow"), run=L.get("run", 6), max_grade=L.get("max_grade", 1.0),
                            blocks=[block(b) for b in L.get("blocks", ["COBBLE"])], weights=L.get("weights"),
                            cap=block(L["cap"]) if "cap" in L else None,
                            crenel=block(L["crenel"]) if "crenel" in L else None,
                            gap=tuple(L["gap"]) if "gap" in L else None, closed=L.get("closed", False),
                            keep=~land, rng=rng)
            for x, z, _, _ in got:
                laid[x - x0, z - z0] = True
        built_on |= laid
        out.steps.append(Step(L["id"], "build", L["op"], laid, Hi.copy(), L.get("note", "")))
    for L in doc.get("dress", []):
        laid = np.zeros(X.shape, bool)
        if L["op"] == "trees":
            from . import trees as TR
            e, _ = area_distance(L["area"], X, Z, fields, lines)
            clear = ndimage.binary_dilation(built_on, iterations=L.get("clear", 3))
            zone = (e < 1) & land & (water == 0) & ~clear
            kinds = TR.kinds(TR.library())
            weights = {k: v for k, v in L["kinds"].items() if k in kinds}
            planted = []
            TR.scatter(w, zone, kinds, weights, np.random.default_rng(L.get("seed", 0)), tries=L.get("tries", 400),
                       planted=planted)
            for x, z, _ in planted:
                laid[x - x0, z - z0] = True
        out.steps.append(Step(L["id"], "dress", L["op"], laid, Hi.copy(), L.get("note", "")))
    out.H, out.land, out.water = Hi, land, water
    return out


def _offset(pts, by):
    """A polyline moved `by` blocks to its left (negative: right), each point along its segments' mean normal."""
    pts = np.asarray(pts, float)
    out = []
    for j in range(len(pts)):
        a, b = pts[max(j - 1, 0)], pts[min(j + 1, len(pts) - 1)]
        t = b - a
        n = np.array([-t[1], t[0]]) / (np.hypot(*t) or 1)
        out.append(tuple(pts[j] + by * n))
    return out
