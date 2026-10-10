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


@dataclass
class Ctx:
    """What an expression reads: the grid, the heights so far, the named fields, the lines and areas laid."""
    X: np.ndarray
    Z: np.ndarray
    H: np.ndarray
    fields: dict
    lines: dict
    land: np.ndarray = None
    water: np.ndarray = None


def expr(spec, c):
    """A number or a field, stated as data. A number is itself; "x", "z", "H" are the grid and the heights so far;
    any other name is a named field. A one-key object is an operation over its arguments:

    arithmetic  add, sub, mul, div, neg, abs, min, max, pow, exp, round, floor, clip [a, lo, hi]
    shaping     smoothstep [e0, e1, a], mix [a, b, w] (field.mix), where [mask, a, b]
    masks       lt, le, gt, ge [a, b], and, or, not, inside (an area: distance under 1)
    sources     fbm, ridged, line (noise; "along": "z" or "x" makes fbm one-dimensional along that axis),
                distance (an area's 0-to-1 distance), blocks (in blocks), terms {height, terms}, at [x, z] (the
                heights at a point), line_z {pts, spline, along: "x"} (a line's z at each x)
    """
    if isinstance(spec, bool):
        return spec
    if isinstance(spec, (int, float)):
        return float(spec)
    if isinstance(spec, str):
        named = {"x": c.X.astype(float), "z": c.Z.astype(float), "H": c.H, "W": c.water, "land": c.land}
        if spec in named:
            return named[spec]
        return c.fields[spec] if spec in c.fields else _missing(spec)
    (op, a), = spec.items()
    E = lambda v: expr(v, c)                                              # noqa: E731
    if op in ("fbm", "ridged", "line"):
        if op == "fbm" and a.get("along"):
            n = c.Z.shape[1] if a["along"] == "z" else c.X.shape[0]
            f = noise.fbm((n,), a["cell"], a.get("octaves", 3), seed=a.get("seed", 0))
            return np.broadcast_to(f[None, :] if a["along"] == "z" else f[:, None], c.X.shape)
        return _field({op: a}, c.X.shape, c.fields)
    if op == "add":
        out = E(a[0])
        for v in a[1:]:
            out = out + E(v)
        return out
    if op == "mul":
        out = E(a[0])
        for v in a[1:]:
            out = out * E(v)
        return out
    if op == "sub":
        return E(a[0]) - E(a[1])
    if op == "div":
        return E(a[0]) / E(a[1])
    if op == "neg":
        return -E(a)
    if op == "abs":
        return np.abs(E(a))
    if op == "min":
        return np.minimum.reduce([np.broadcast_to(E(v), c.X.shape) for v in a]) if len(a) > 2 else np.minimum(E(a[0]), E(a[1]))
    if op == "max":
        return np.maximum.reduce([np.broadcast_to(E(v), c.X.shape) for v in a]) if len(a) > 2 else np.maximum(E(a[0]), E(a[1]))
    if op == "pow":
        return E(a[0]) ** E(a[1])
    if op == "exp":
        return np.exp(E(a))
    if op == "round":
        return np.round(E(a))
    if op == "floor":
        return np.floor(E(a))
    if op == "clip":
        return np.clip(E(a[0]), E(a[1]) if a[1] is not None else None, E(a[2]) if a[2] is not None else None)
    if op == "smoothstep":
        return noise.smoothstep(E(a[0]), E(a[1]), E(a[2]))
    if op == "mix":
        return F.mix(E(a[0]), E(a[1]), E(a[2]))
    if op == "where":
        return np.where(E(a[0]), E(a[1]), E(a[2]))
    if op in ("lt", "le", "gt", "ge"):
        return {"lt": np.less, "le": np.less_equal, "gt": np.greater, "ge": np.greater_equal}[op](E(a[0]), E(a[1]))
    if op == "and":
        out = E(a[0])
        for v in a[1:]:
            out = out & E(v)
        return out
    if op == "or":
        out = E(a[0])
        for v in a[1:]:
            out = out | E(v)
        return out
    if op == "not":
        return ~E(a)
    if op == "inside":
        return area_distance(a, c.X, c.Z, c.fields, c.lines, c)[0] < 1
    if op == "distance":
        return area_distance(a, c.X, c.Z, c.fields, c.lines, c)[0]
    if op == "blocks":
        e, scale = area_distance(a, c.X, c.Z, c.fields, c.lines, c)
        return e * scale
    if op == "terms":
        return F.terms(c.X.astype(float), c.Z.astype(float), E(a["height"]), *_terms(a.get("terms", []), c))
    if op == "at":
        x, z = a
        return float(c.H[int(x) - int(c.X[0, 0]), int(z) - int(c.Z[0, 0])])
    if op == "line_z":
        pts = _line_pts(a, c)
        xs, zs = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
        order = np.argsort(xs)
        return np.interp(c.X.astype(float), xs[order], zs[order])
    if op == "dilate":
        return ndimage.binary_dilation(np.asarray(E(a[0]), bool), iterations=int(a[1]))
    if op == "near":
        return ndimage.distance_transform_edt(~np.asarray(E(a), bool))
    if op == "spread":
        n = int(a[1])
        return ndimage.grey_dilation(E(a[0]), size=(2 * n + 1, 2 * n + 1))
    if op == "hypot":
        return np.hypot(E(a[0]), E(a[1]))
    if op == "line_distance":
        return shapes.polyline(c.X.astype(float), c.Z.astype(float), _line_pts(a, c))[0]
    if op == "ellipse":
        return shapes.ellipse_distance(c.X.astype(float), c.Z.astype(float), tuple(a["at"]), a["rx"], a["rz"],
                                       angle=a.get("angle", 0.0))
    if op == "polygon":
        return shapes.inside(c.X.astype(float), c.Z.astype(float), [tuple(p) for p in a])
    if op == "full":
        return np.full(c.X.shape, float(E(a)))
    # the library's landforms, read with this layer's heights: each returns heights
    if op == "profile":
        steps = [LF.Step(E(st["start"]), E(st["end"]), st["top"] if st["top"] == "ground" else E(st["top"]))
                 for st in a["steps"]]
        return LF.profile(c.H, E(a["d"]), E(a["floor"]), steps, mode=a.get("mode", "set"))
    if op == "ridge":
        spurs = [(E(sp["d"]), E(sp["top"]), tuple(sp["reach"])) for sp in a.get("spurs", [])]
        return LF.ridge(c.H, E(a.get("coord", "x")), E(a["foot"]), a["reach"], E(a["crest"]),
                        rough=E(a.get("rough", 0.0)), spurs=spurs,
                        terrace=tuple(a["terrace"]) if "terrace" in a else None)
    if op == "level":
        return LF.level(c.H, E(a["e"]), a.get("top", "median") if a.get("top") == "median" else E(a["top"]),
                        inner=a.get("inner", 1.0), outer=a.get("outer", 1.5), mode=a.get("mode", "set"))
    if op == "blend":
        return LF.blend(c.H, E(a["to"]), E(a["mask"]), width=a.get("width", 8))
    if op == "spire":
        return LF.spire(c.H, c.X.astype(float), c.Z.astype(float), tuple(a["at"]), r=a["r"], top=E(a["top"]),
                        taper=a.get("taper", 1.6), jag=a.get("jag", 0.15), seed=a.get("seed", 0), rz=a.get("rz"),
                        angle=a.get("angle", 0.0))
    if op == "crater":
        return LF.crater(c.H, E(a["e"]), a["floor"], a["r"], flat=a.get("flat", 0.0), slope=a.get("slope", 1.0))
    if op == "mound":
        return LF.mound(c.H, E(a["e"]), a["rise"], power=a.get("power", 1.6), mode=a.get("mode", "lift"))
    raise ValueError(f"unknown expression {op}")


def _missing(name):
    raise KeyError(f"no field named {name}")


def _terms(terms, c):
    parts = []
    for t in terms:
        (kind, a), = t.items()
        if kind == "ramp":
            parts.append(F.Ramp(a["along"], a["from"], a["to"], a["rise"]))
        elif kind == "gauss":
            parts.append(F.Gauss(tuple(a["at"]), a["r"], a["rise"], rz=a.get("rz"), angle=a.get("angle", 0.0)))
        elif kind == "tilt":
            parts.append(F.Tilt(a["dx"], a["dz"], tuple(a.get("at", (0, 0)))))
        elif kind == "noise":
            parts.append(F.Noise(expr(a["field"], c), a["rise"]))
    return parts


def _line_pts(a, c):
    """A line's points: its own `pts`, splined at `spline` blocks unless it is false, kept to x_max if stated,
    or another layer's line by `near`."""
    if "near" in a:
        return c.lines[a["near"]]["pts"]
    pts = [tuple(p) for p in a["pts"]]
    if a.get("spline", 1.0):
        pts = noise.spline(pts, a.get("spline", 1.0))
    if "x_max" in a:
        pts = [p for p in pts if p[0] <= a["x_max"]]
    return pts


def area_distance(area, X, Z, fields, lines, c=None):
    """(e, scale): 0 at the area's centre or deepest point, 1 on its rim, over 1 outside; `scale` is how many
    blocks one unit of e spans, for an operation that measures in blocks."""
    Xf, Zf = X.astype(float), Z.astype(float)
    (kind, a), = ((k, v) for k, v in area.items() if k not in ("rough", "rise", "depth", "top", "plus"))
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
        pts = lines[a["near"]]["pts"] if "near" in a else _line_pts(a, None)
        d, _ = shapes.polyline(Xf, Zf, pts)
        half = a.get("width", lines[a["near"]]["width"] if "near" in a else 2) / 2
        e, scale = d / half, float(half)
    else:
        raise ValueError(f"unknown area {kind}")
    if "rough" in area:
        r = area["rough"]
        e = e + r.get("amp", 0.12) * noise.fbm(X.shape, r.get("cell", 6), 2, seed=r.get("seed", 0))
    if "plus" in area:
        e = e + expr(area["plus"], c or Ctx(X, Z, None, fields, lines))
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


def made_cells(made):
    """The blueprint of a `made` stage as brittle cells, {(cx, cz): Cell}: each entry a rectangle of cells
    [cx0, cx1, cz0, cz1] of one kind at one floor y, its section, its stair's rise and whether a deck is open under."""
    from . import brittle as BR
    cells = {}
    for e in made.get("cells", []):
        cx0, cx1, cz0, cz1 = e["rect"]
        for cx in range(cx0, cx1 + 1):
            for cz in range(cz0, cz1 + 1):
                cells[(cx, cz)] = BR.Cell(e["kind"], e.get("y"), rises=e.get("rises"), name=e.get("name"),
                                          under=e.get("under", False), section=e.get("section"))
    return cells


def made_mask(cells, X, Z):
    """(mask, top): the columns of made land and their tops (-1 off it), as the grammar will lay them."""
    from . import brittle as BR
    _, T = BR.heights(cells)
    x0, z0 = int(X[0, 0]), int(Z[0, 0])
    top = np.full(X.shape, -1.0)
    for (x, z), t in T.items():
        if 0 <= x - x0 < X.shape[0] and 0 <= z - z0 < X.shape[1]:
            top[x - x0, z - z0] = t
    return top >= 0, top


def _paint_spec(spec):
    """A block-painting rule for a placed box, from data: {"block"}, or {"bands": {"along": "ly", "width": 2,
    "blocks": [...]}}, with an optional "cap" block on its top course."""
    if "bands" in spec:
        b = spec["bands"]
        blocks = [block(x) for x in b["blocks"]]
        axis = {"u": 0, "ly": 1, "lz": 2}[b.get("along", "ly")]
        base = lambda u, ly, lz, s: blocks[int(((u, ly, lz)[axis] + s[axis] / 2) // b.get("width", 2)) % len(blocks)]   # noqa: E731
    else:
        one = block(spec.get("block", "STONE"))
        base = lambda u, ly, lz, s: one                                              # noqa: E731
    if "cap" not in spec:
        return base
    cap = block(spec["cap"])
    return lambda u, ly, lz, s: cap if ly > s[1] / 2 - 1 else base(u, ly, lz, s)


BLOCK_KEYS = ("block", "a", "b", "recess", "light", "course")


def _pattern(spec):
    """A facade face pattern or floor field from data: {"flutes": {"period": 4, ...}} -> facade.flutes(...),
    its block arguments given as block names; "blocks" is a list of them."""
    from . import facade as FA
    (name, a), = spec.items()
    kw = {k: (block(v) if k in BLOCK_KEYS else [block(b) if b is not None else None for b in v] if k == "blocks"
              else v) for k, v in a.items()}
    return getattr(FA, name)(**kw)


def _footprint(L, X, Z):
    x0, z0, x1, z1 = L["rect"]
    return [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]


def ground(doc, X=None, Z=None):
    """The fields and ground stages alone: (ctx, steps). The board's grid is its x and z range unless given."""
    bd = doc["board"]
    if X is None:
        (x0, x1), (z0, z1) = bd["x"], bd["z"]
        X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    c = Ctx(X, Z, np.full(X.shape, float(bd.get("floor", 40))), {}, {}, np.ones(X.shape, bool),
            np.zeros(X.shape, int))
    c.laid = np.zeros(X.shape, bool)
    if "made" in doc:
        c.cells = made_cells(doc["made"])
        c.fields["made"], c.fields["made_top"] = made_mask(c.cells, X, Z)
    for k, v in doc.get("fields", {}).items():
        c.fields[k] = expr(v, c) if isinstance(v, dict) and next(iter(v)) not in ("fbm", "ridged", "line") \
            or isinstance(v, dict) and v.get("fbm", {}).get("along") else _field(v, X.shape, c.fields)
    steps = []
    for L in doc.get("ground", []):
        before, wet_before = c.H.copy(), c.water.copy()
        op = L["op"]
        if op == "outline":
            ins = {k: (expr(v, c) if isinstance(v, (dict, str)) else v) for k, v in L.get("insets", {}).items()}
            c.land = shapes.island(X, Z, tuple(L["box"]), **ins)
            steps.append(Step(L["id"], "ground", "outline", c.land.copy(), c.H.copy(), L.get("note", "")))
            continue
        if op == "set":
            value = expr(L["height"], c)
            c.H = np.where(expr(L["where"], c), value, c.H) if "where" in L else np.asarray(value, float) + 0 * c.H
        elif op == "round":
            c.H = np.round(c.H)
        elif op == "water":
            c.water = np.where(expr(L["where"], c), np.asarray(expr(L["level"], c)).astype(int), c.water)
        elif op == "watercourse":
            pts = _line_pts(L["line"], c)
            c.lines[L["id"]] = dict(pts=pts, width=L.get("width", 6))
            c.H, river = LF.watercourse(c.H.copy(), c.X.astype(float), c.Z.astype(float), pts,
                                        width=L.get("width", 6), depth=L.get("depth", 2), water=L.get("water", 1),
                                        bank=L.get("bank", 4), fall_min=L.get("fall_min", 2),
                                        reach_min=L.get("reach_min", 10))
            c.fields[L["id"] + ".surface"] = river.surface
            c.fields[L["id"] + ".mask"] = river.mask
        elif op == "grade":
            pts = _line_pts(L["line"], c)
            wet = c.water > 0
            Hn, prof = LF.grade(c.H.astype(float), c.X.astype(float), c.Z.astype(float), pts,
                                width=L.get("width", 3), max_grade=L.get("max_grade", 0.25),
                                shoulder=L.get("shoulder", 2), water=wet, keep=c.laid)
            c.H = np.where(wet, c.H, np.round(Hn))
            c.lines[L["id"]] = dict(pts=pts, width=L.get("width", 3), profile=prof)
            c.laid |= shapes.polyline(c.X.astype(float), c.Z.astype(float), pts)[0] <= L.get("width", 3) / 2
        else:
            c.H, wet = _ground_layer(L, c.H, X, Z, c.fields, c.lines, c.land)
            if wet is not None:
                c.water = np.where(wet > 0, wet, c.water)
        changed = ((np.abs(c.H - before) > 0.5) | (c.water != wet_before)) & c.land
        steps.append(Step(L["id"], "ground", op, changed, c.H.copy(), L.get("note", "")))
    return c, steps


def build(doc):
    """Build a layer document: every stage in order, every layer recorded as a Step."""
    bd = doc["board"]
    (x0, x1), (z0, z1) = bd["x"], bd["z"]
    w = World(x0, z0, x1 - x0 + 1, z1 - z0 + 1, sy=bd.get("height", 128))
    X, Z = w.grid()
    c, steps = ground(doc, X, Z)
    fields, lines, H, water = c.fields, c.lines, c.H, c.water
    made = fields.get("made", np.zeros(X.shape, bool))
    land = c.land & ~made
    out = Built(w, H, land, water, X, Z, steps=steps, lines=lines)
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
    if "made" in doc:
        import random
        from . import brittle as BR
        md = doc["made"]
        fills = {e["section"]: e["fill"] for e in md.get("cells", []) if e.get("section") and e.get("fill")}
        fill = (lambda piece, cs: fills.get(cs[piece[0]].section)) if fills else None
        grown = {(int(X[i, k]), int(Z[i, k])): int(Hi[i, k]) for i, k in np.argwhere(land)}
        BR.build(w, c.cells, rng=random.Random(bd.get("seed", 0)), dye=md.get("dye", 14), fill=fill, grown=grown)
        out.steps.append(Step("made", "made", "grammar", made.copy(), Hi.copy(),
                              f"{len(c.cells)} cells in the {md.get('style', 'brittle')} grammar"))
        for n, hs in enumerate(md.get("houses", [])):
            BR.house(w, [[tuple(cc) for cc in layer] for layer in hs["layers"]], hs["floor"], hs.get("dye", 14),
                     door=(tuple(hs["door"][0]), hs["door"][1]) if "door" in hs else None)
            m = np.zeros(X.shape, bool)
            for cx, cz in hs["layers"][0]:
                m[(X // BR.CELL == cx) & (Z // BR.CELL == cz)] = True
            built_on |= m
            out.steps.append(Step(hs.get("id", f"house-{n}"), "made", "house", m, Hi.copy(), hs.get("note", "")))
    Hall = np.where(made, fields.get("made_top", Hi), Hi).astype(int) if "made" in doc else Hi
    from . import forms as FO, facade as FA
    for L in doc.get("volume", []):
        laid = np.zeros(X.shape, bool)
        if L["op"] == "box":
            before = w.ids.copy()
            FO.placed_box(w, L["at"][0], L["at"][1], tuple(L["size"]), Hall, yaw=L.get("yaw", 0.0),
                          tilt=L.get("tilt", 0.0), sink=L.get("sink", 0.3), on=L.get("on", "lowest"),
                          paint=_paint_spec(L.get("paint", {})), hole=L.get("hole"))
            laid = (w.ids != before).any(axis=1)
        built_on |= laid
        out.steps.append(Step(L["id"], "volume", L["op"], laid, Hi.copy(), L.get("note", "")))
    for L in doc.get("structures", []):
        laid = np.zeros(X.shape, bool)
        cells = _footprint(L, X, Z)
        under = [int(Hall[x - x0, z - z0]) for x, z in cells]
        if L["op"] == "mass":
            y0 = L["y0"] if isinstance(L.get("y0"), int) else (max(under) if L.get("on") == "highest" else min(under)) \
                + 1 + L.get("offset", 0)
            if L.get("pour", True):                                     # down to the ground under every column
                for (x, z), g in zip(cells, under):
                    for y in range(max(g + 1, 1), y0):
                        w.set(x, y, z, *block(L.get("base", "STONE")))
            FA.extrude(w, cells, y0, y0 + L["height"] - 1, base=block(L.get("base", "STONE")),
                       faces_=[_pattern(p) for p in L.get("faces", [])], top=L.get("top"), bottom=L.get("bottom"))
        elif L["op"] == "carpet":
            y = L["y"] if "y" in L else max(under)
            x0r, z0r, x1r, z1r = L["rect"]
            FA.carpet(w, x0r, z0r, x1r, z1r, y, FA.first_of(*[_pattern(p) for p in L["fields"]]))
        for x, z in cells:
            laid[x - x0, z - z0] = True
        built_on |= laid
        out.steps.append(Step(L["id"], "structures", L["op"], laid, Hi.copy(), L.get("note", "")))
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
    for L in doc.get("symmetry", []):
        from .orient import turn_world
        cx = Ctx(X, Z, Hi.astype(float), fields, lines, land, water)
        keep = np.asarray(expr(L["keep"], cx), bool)
        recolour = {block(a): block(b) for a, b in L.get("recolour", [])}
        turn_world(w, L["op"], keep, recolour=recolour or None)
        out.steps.append(Step(L["id"], "symmetry", L["op"], ~keep, Hi.copy(), L.get("note", "")))
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
