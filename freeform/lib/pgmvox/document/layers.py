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

**The stages run in the fixed order of `STAGES`:** the made blueprint, `fields` (named fields), `ground` (heights),
`paint` (the top, first layer that applies wins), `lay`, `water`, `faces` (courses on every drop of the grown
ground), `made` (the grammar), `volume`, `structures`, `build` (paths' surfaces and steps, walls, hedges, fences),
`dress` (trees, kept `clear` blocks off everything built) and `symmetry`. A layer that names another (`near`) reads
the area or line that layer was given.

**A board may stand on more than one floor.** `levels` are grounds of their own over an outline, each built from
its own ground layers and painted, watered and dressed apart from the board's, resting on what is under them or
hanging over it. `carve` cuts tunnels, chambers, rooms and shafts out of the laid ground, and an `arch` volume is a
deck over whatever it spans. Each of these publishes a `Surface`, and a trees layer stands on the one it names
(`on`), the board's own ground where it names none.
"""
import math
from dataclasses import dataclass, field as _field

import numpy as np
from scipy import ndimage

from pgmvox.ground import field as F
from pgmvox.ground import landform as LF
from pgmvox.geom import noise
from pgmvox.routes import route as RT
from pgmvox.geom import shapes
from pgmvox.surface import terrain as T
from pgmvox.core.blocks import B
from pgmvox.built.build import line_wall
from pgmvox.core.world import World

STAGES = ("made blueprint", "fields", "ground", "paint", "lay", "water", "levels", "carve", "faces", "made", "volume",
          "structures", "build", "dress", "symmetry")


@dataclass
class Step:
    """One layer as it ran: its id, its stage, the heights after it (ground) and the columns it changed; `level`
    names the level a layer belongs to, empty for the board's own ground."""
    id: str
    stage: str
    op: str
    changed: np.ndarray
    H: np.ndarray = None
    note: str = ""
    level: str = ""


@dataclass
class Surface:
    """A floor a player stands on: `top` is the y of its top block in each column, -1 where it is not. `kind` is
    ground, level, deck or floor; `water` its water surfaces and `ceiling` the lowest block over it, where known."""
    id: str
    kind: str
    top: np.ndarray
    water: np.ndarray = None
    ceiling: np.ndarray = None


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
    surfaces: list = _field(default_factory=list)

    def surface(self, id):
        """The surface of that id."""
        return next(s for s in self.surfaces if s.id == id)


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
    if op == "gullies":
        return LF.gullies(c.H, c.X.astype(float), c.Z.astype(float), tuple(a["at"]), a["count"], E(a["depth"]),
                          a["r0"], a["r1"], wander=a.get("wander", 0.9), sharpness=a.get("sharpness", 3.0),
                          seed=a.get("seed", 0))
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
        return np.asarray(F.terms(Xf, Zf, float(L["height"]), *parts), float) + np.zeros(X.shape), None
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
    from pgmvox.grammar import brittle as BR
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
    from pgmvox.grammar import brittle as BR
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


def _course(spec):
    """A face course from data: a block, null to keep the ground's, {"block", "back", "out"} (a block with one behind
    it or one outside it over air: {"block": "AIR", "back": ...} is an inset), {"stair": NAME, "upside_down": true,
    "toward": "in" | "out" | "end"} (turned by the face, or rising to the nearer end of its run) or {"mix": [[block,
    weight], ...]}."""
    from pgmvox.grammar import rules as G
    from pgmvox.core.orient import stair
    if spec is None:
        return None
    if isinstance(spec, dict) and ("back" in spec or "out" in spec):
        return G.Course(_course(spec.get("block", "AIR")), back=_course(spec.get("back")), out=_course(spec.get("out")))
    if isinstance(spec, dict) and "mix" in spec:
        return G.Mix(tuple((block(b), wt) for b, wt in spec["mix"]))
    if isinstance(spec, dict) and "stair" in spec:
        bid, down, toward = getattr(B, spec["stair"]), spec.get("upside_down", False), spec.get("toward", "in")
        if toward == "end":
            return G.Toward(bid, down)
        return lambda inward: (bid, stair(G.OPP[inward] if toward == "out" else inward, upside_down=down))
    if isinstance(spec, dict) and "block" in spec:
        return block(spec["block"])
    return block(spec)


def face(spec):
    """A grammar Face from a faces layer: its `courses`; an `accent` bay whose `inner` is a stack, or {"per_pos":
    [stack, ...]} one per inner column; or a `panel`, every straight run framed: {"ends": [stack, ...], "middle":
    stack}."""
    from pgmvox.grammar import rules as G
    stack = lambda st: [_course(c) for c in st]                                          # noqa: E731
    a = spec.get("accent")
    accent = None
    if a:
        inner = a["inner"]
        if isinstance(inner, dict):
            stacks = [stack(st) for st in inner["per_pos"]]
            inner_ = lambda pos: stacks[pos - 1]                                        # noqa: E731
        else:
            inner_ = stack(inner)
        accent = G.Accent(a["module"], frame=stack(a["frame"]), inner=inner_, every=a.get("every", 2),
                          phase=a.get("phase", 0), min_air=a.get("min_air", 5), align="grid", margin=a.get("margin", 0))
    p = spec.get("panel")
    panel = G.Panel([stack(st) for st in p["ends"]], stack(p["middle"]), p.get("min_run", 3)) if p else None
    return G.Face(stack(spec.get("courses", [])), accent, floor=0, panel=panel)


def below(spec):
    """What a face lays under its courses, from data: {"block"}, {"lattice": {"period", "a", "b"}} or
    {"bands": {"blocks", "width", "y0"}}, any of them with "else" for where it answers nothing; null keeps the
    ground's beds."""
    from pgmvox.grammar import rules as G
    if not spec:
        return None
    if "lattice" in spec:
        a = spec["lattice"]
        fn = G.lattice(a.get("period", 8), block(a["a"]), block(a["b"]))
    elif "bands" in spec:
        a = spec["bands"]
        fn = G.bands([block(b) for b in a["blocks"]], a.get("width", 1), a.get("y0", 0))
    else:
        one = block(spec["block"])
        fn = lambda x, y, z: one                                                         # noqa: E731
    if "else" not in spec:
        return fn
    other = block(spec["else"])
    return lambda x, y, z: fn(x, y, z) or other


BLOCK_KEYS = ("block", "a", "b", "recess", "light", "course")


def _pattern(spec):
    """A facade face pattern or floor field from data: {"flutes": {"period": 4, ...}} -> facade.flutes(...),
    its block arguments given as block names; "blocks" is a list of them."""
    from pgmvox.built import facade as FA
    (name, a), = spec.items()
    kw = {k: (block(v) if k in BLOCK_KEYS else [block(b) if b is not None else None for b in v] if k == "blocks"
              else v) for k, v in a.items()}
    return getattr(FA, name)(**kw)


def house_style(spec, doc=None):
    """A house's style: a name from pgmvox's styles or from the document's own `styles`, or an object naming a
    `base` style and the keys it changes, its blocks written as anywhere else in the document."""
    from pgmvox.built import build as BLD
    if isinstance(spec, str):
        if doc is not None and spec in doc.get("styles", {}):
            return house_style(doc["styles"][spec], doc)
        return spec
    st = dict(BLD.STYLES[spec.get("base", "town")])
    for k, v in spec.items():
        if k == "base":
            continue
        if k in ("ground", "upper"):
            st[k] = [block(b) for b in v]
        elif k in ("stair", "door", "sill", "hood"):
            st[k] = getattr(B, v)
        elif k == "verge":
            st[k] = {"roof": block(v["roof"]), "slab": block(v["slab"]), **({"stair": getattr(B, v["stair"])}
                                                                           if "stair" in v else {})}
        elif k == "roof_bands":
            st[k] = int(v)
        elif k in ("quoins", "chimney_top"):
            st[k] = [block(b) for b in v]
        elif k == "sill_in":
            st[k] = [getattr(B, n) for n in v]
        elif k == "log":
            st[k] = getattr(B, v)
        elif k == "stack":
            st[k] = {"block": block(v["block"]), "cap": block(v.get("cap", "COBBLE_WALL")),
                     "base": getattr(B, v.get("base", "COBBLE_STAIRS"))}
        elif k in ("post", "beam_ends", "windows", "plain_turned", "joists_along", "slab_roof", "ridge_slab"):
            st[k] = v
        else:
            st[k] = block(v)
    return st


def _footprint(L, X, Z):
    x0, z0, x1, z1 = L["rect"]
    return [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]


def ground(doc, X=None, Z=None, share=None, level=""):
    """The fields and ground stages alone: (ctx, steps). The board's grid is its x and z range unless given. With
    `share` (the board's ctx) a level's ground is built on the board's fields and lines, starting at its own
    `floor`, and its steps carry the level's id."""
    bd = doc["board"]
    if X is None:
        (x0, x1), (z0, z1) = bd["x"], bd["z"]
        X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
    floor = float(doc.get("floor", bd.get("floor", 40)))
    c = Ctx(X, Z, np.full(X.shape, floor), dict(share.fields) if share else {}, share.lines if share else {},
            np.ones(X.shape, bool), np.zeros(X.shape, int))
    c.laid = np.zeros(X.shape, bool)
    if share is None and "made" in doc:
        c.cells = made_cells(doc["made"])
        c.fields["made"], c.fields["made_top"] = made_mask(c.cells, X, Z)
    for k, v in ({} if share else doc.get("fields", {})).items():
        c.fields[k] = expr(v, c) if isinstance(v, dict) and next(iter(v)) not in ("fbm", "ridged", "line") \
            or isinstance(v, dict) and v.get("fbm", {}).get("along") else _field(v, X.shape, c.fields)
    steps = []
    for L in doc.get("ground", []):
        before, wet_before = c.H.copy(), c.water.copy()
        op = L["op"]
        if op == "outline":
            if "area" in L or "where" in L:
                c.land = np.ones(X.shape, bool)
                if "area" in L:
                    c.land &= area_distance(L["area"], X, Z, c.fields, c.lines, c)[0] < 1
                if "where" in L:
                    c.land &= np.asarray(expr(L["where"], c), bool)
            else:
                ins = {k: (expr(v, c) if isinstance(v, (dict, str)) else v) for k, v in L.get("insets", {}).items()}
                c.land = shapes.island(X, Z, tuple(L["box"]), **ins)
            steps.append(Step(L["id"], "ground", "outline", c.land.copy(), c.H.copy(), L.get("note", ""), level))
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
        steps.append(Step(L["id"], "ground", op, changed, c.H.copy(), L.get("note", ""), level))
    if share is not None:
        share.fields.update({k: v for k, v in c.fields.items() if k not in share.fields})
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
    T.lay(w, np.where(land, Hi, -1), land, top=TOP, bands=T.beds(ROCK, Hi, seed=3), paint=paint, bottom=bottom,
          soil=tuple(tuple(v) for v in lay["soil"]) if "soil" in lay else T.SOIL, ledges=lay.get("ledges", True))
    out.steps.append(Step("lay", "lay", "lay", land.copy(), Hi.copy(), f"{len(paint)} paint layers"))
    if (water > 0).any():
        bed = [_paint_layer(P, X, Z, fields, lines, Hi) for P in doc.get("water", {}).get("bed", [])] or (B.GRAVEL, 0)
        T.fill_water(w, Hi, np.where(land, water, 0), bed=bed, mask=land)
        out.steps.append(Step("water", "water", "fill_water", (water > 0) & land, Hi.copy()))
    out.surfaces.append(Surface("ground", "ground", np.where(land, Hi, -1), np.where(land, water, 0),
                                np.full(X.shape, w.sy)))
    for L in doc.get("levels", []):
        _level(L, doc, w, c, out)
    if "carve" in doc:
        _carve(doc["carve"], w, out, bd.get("seed", 0))
    tops = {(int(X[i, k]), int(Z[i, k])): int(Hi[i, k]) for i, k in np.argwhere(land)}
    for L in doc.get("faces", []):
        from pgmvox.grammar import rules as G
        where = None
        if "area" in L:
            e, _ = area_distance(L["area"], X, Z, fields, lines)
            where = lambda x, z, e=e: e[x - x0, z - z0] < 1                             # noqa: E731
        got = G.dress(w, tops, face(L), min_drop=L.get("min_drop", 2), below=below(L.get("below")),
                      foot=(block(L["foot"][0]), L["foot"][1]) if "foot" in L else None, where=where,
                      rng=np.random.default_rng(L.get("seed", bd.get("seed", 0))))
        laid = np.zeros(X.shape, bool)
        for x, z in got:
            laid[x - x0, z - z0] = True
        out.steps.append(Step(L["id"], "faces", "face", laid, Hi.copy(), L.get("note", "")))
    rng = np.random.default_rng(bd.get("seed", 0))
    built_on = np.zeros(X.shape, bool)
    if "made" in doc:
        import random
        from pgmvox.grammar import brittle as BR
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
    from pgmvox.scenery import forms as FO
    from pgmvox.built import facade as FA
    for L in doc.get("volume", []):
        laid = np.zeros(X.shape, bool)
        if L["op"] == "box":
            before = w.ids.copy()
            FO.placed_box(w, L["at"][0], L["at"][1], tuple(L["size"]), Hall, yaw=L.get("yaw", 0.0),
                          tilt=L.get("tilt", 0.0), sink=L.get("sink", 0.3), on=L.get("on", "lowest"),
                          paint=_paint_spec(L.get("paint", {})), hole=L.get("hole"))
            laid = (w.ids != before).any(axis=1)
        elif L["op"] == "arch":
            laid = _arch(L, w, out)
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
    floors = {}
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
            stair_of = lambda k: getattr(B, L[k]) if k in L else None                        # noqa: E731
            got = line_wall(w, Hi, X, Z, pts, height=L.get("height", 2), width=L.get("width", 1),
                            courses=[[block(c[0]), block(c[1])] if isinstance(c, list) and len(c) == 2
                                     and not isinstance(c[1], int) else block(c)
                                     for c in L["courses"]] if "courses" in L else None,
                            crenel_stair=stair_of("crenel_stair"), step_stair=stair_of("step_stair"),
                            step_slab=block(L["step_slab"]) if "step_slab" in L else None,
                            ruin=tuple(L["ruin"]) if "ruin" in L else None,
                            crown=L.get("crown", "follow"), run=L.get("run", 6), max_grade=L.get("max_grade", 1.0),
                            blocks=[block(b) for b in L.get("blocks", ["COBBLE"])], weights=L.get("weights"),
                            cap=block(L["cap"]) if "cap" in L else None,
                            crenel=block(L["crenel"]) if "crenel" in L else None,
                            gap=tuple(L["gap"]) if "gap" in L else None, closed=L.get("closed", False),
                            keep=~land, rng=rng)
            for x, z, _, _ in got:
                laid[x - x0, z - z0] = True
        elif L["op"] == "house":
            from pgmvox.built import build as BLD
            hx, hz = L["at"]
            r = int(max(L.get("L", 9), L.get("W", 6)) / 2) + 1
            under = Hi[max(hx - r - x0, 0):hx + r - x0 + 1, max(hz - r - z0, 0):hz + r - z0 + 1]
            h = BLD.House(hx, hz, L.get("heading", 0.0), L=L.get("L", 9), W=L.get("W", 6), floor=int(under.max()),
                          storeys=L.get("storeys", 2), style=house_style(L.get("style", "town"), doc), jetty=L.get("jetty", False),
                          door=L.get("door", 1), chimney=L.get("chimney", True), roof=L.get("roof", "gable"),
                          **{k: L[k] for k in ("storey", "pitch", "overhang") if k in L})
            floors[L["id"]] = h.floor
            got = BLD.house(w, h, ground_at=lambda x, z: int(Hi[x - x0, z - z0]),
                            rng=np.random.default_rng(L.get("seed", bd.get("seed", 0))))
            for x, z in got["footprint"]:
                laid[x - x0, z - z0] = True
            if "walk" in L and got["door"] is not None:
                _door_path(w, Hi, got["door"], L["walk"], lines, x0, z0, built_on | laid, rng)
        elif L["op"] == "stall":
            from pgmvox.built import props as PR
            sx, sz = L["at"]
            for x, z in PR.market_stall(w, sx, int(Hi[sx - x0, sz - z0]), sz, L.get("facing", "s"),
                                        tuple(L.get("colours", [14, 0])), L.get("width", 5),
                                        counter_stair=getattr(B, L["counter_stair"]) if "counter_stair" in L else None,
                                        post=block(L.get("post", "FENCE")), banners=L.get("banners", False),
                                        sides=L.get("sides", False), foot=block(L["foot"]) if "foot" in L else None,
                                        goods=tuple(block(g) for g in L["goods"]) if "goods" in L else
                                        ((B.PUMPKIN, 3), (B.MELON, 0), (B.HAY, 0))):
                laid[x - x0, z - z0] = True
        elif L["op"] == "posts":
            for px, pz in L["at"]:
                g = int(Hi[px - x0, pz - z0])
                for j, b in enumerate(L["stack"]):
                    w.set(px, g + 1 + j, pz, *block(b))
                laid[px - x0, pz - z0] = True
        elif L["op"] == "round_tower":
            from pgmvox.built import build as BLD
            tx, tz = L["at"]
            r = L.get("r", 3.5)
            R = L["half"] if "half" in L else int(np.ceil(r))
            under = Hi[tx - R - x0:tx + R - x0 + 1, tz - R - z0:tz + R - z0 + 1]
            y0 = L.get("y", int(under.max()))
            got = BLD.round_tower(w, tx, tz, r, y0, L.get("height", 10), wall=block(L.get("wall", "STONEBRICK")),
                                  quoins=[block(b) for b in L["quoins"]] if "quoins" in L else None,
                                  floor=block(L.get("floor", ["PLANKS", 1])), crenel=block(L.get("crenel", "STONEBRICK")),
                                  door_side=L.get("door", "s"),
                                  openings=[(a, oy + (y0 if L.get("openings_from") == "floor" else 0))
                                            for a, oy in L.get("openings", [])],
                                  ground_at=lambda x, z: int(Hi[x - x0, z - z0]), slit=block(L.get("slit", "AIR")),
                                  half=L.get("half"), string=block(L["string"]) if "string" in L else None,
                                  plinth=block(L["plinth"]) if "plinth" in L else None, cut=L.get("cut", True),
                                  crenel_stair=getattr(B, L["crenel_stair"]) if "crenel_stair" in L
                                  else None)
            for x, z in got:
                laid[x - x0, z - z0] = True
        elif L["op"] == "boulders":
            from pgmvox.scenery import green as GR
            g_at = lambda x, z: int(Hi[x - x0, z - z0])                                     # noqa: E731
            rr = np.random.default_rng(L.get("seed", bd.get("seed", 0)))
            for spec in L["at"]:
                bx, bz, r = spec[:3]
                kw = spec[3] if len(spec) > 3 else {}
                for x, z in GR.boulder(w, bx, bz, g_at, r, rr, rz=kw.get("rz"), height=kw.get("height"),
                                       angle=kw.get("angle", 0.0), sink=L.get("sink", 0.3),
                                       rock=tuple(block(b) for b in L.get("rock", ["STONE", ["STONE", 5]])),
                                       accent=block(L.get("accent", "COBBLE")), accent_share=L.get("accent_share", 0.25),
                                       rough=L.get("rough", 0.35), shape=kw.get("shape", L.get("shape", 3.0))):
                    if 0 <= x - x0 < laid.shape[0] and 0 <= z - z0 < laid.shape[1]:
                        laid[x - x0, z - z0] = True
        elif L["op"] in ("hedge", "small_trees", "flowers", "crops"):
            from pgmvox.scenery import green as GR
            g_at = lambda x, z: int(Hi[x - x0, z - z0])                                     # noqa: E731
            rr = np.random.default_rng(L.get("seed", bd.get("seed", 0)))
            if L["op"] == "hedge":
                from pgmvox.geom.shapes import walk_cells
                pts = lines[L["near"]]["pts"] if "near" in L else [tuple(p) for p in L["line"]]
                if "offset" in L:
                    pts = _offset(pts, L["offset"])
                got = GR.hedge(w, walk_cells([(int(round(x)), int(round(z))) for x, z in pts]), g_at, rr,
                               leaves=block(L.get("leaves", ["LEAVES", 4])), modules=L.get("modules", 1),
                               drop=L.get("drop", 0.15), grass=L.get("grass", False))
            elif L["op"] == "small_trees":
                got = []
                for tx, tz in L["at"]:
                    got += GR.round_oak(w, tx, tz, g_at, rr, trunk=L.get("trunk", 3), log=block(L.get("log", ["LOG", 0])),
                                        leaves=block(L.get("leaves", ["LEAVES", 4])), bite=L.get("bite", 0.35))
            else:
                e, _ = area_distance(L["area"], X, Z, fields, lines)
                where = [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere((e < 1) & land & (water == 0))]
                if L["op"] == "crops":
                    got = GR.crop_rows(w, where, g_at, [block(c) for c in L["crops"]], rr, angle=L.get("angle", 0.0),
                                       rows=L.get("rows", 6), ditch=L.get("ditch", 3))
                    for sx, sz in L.get("scarecrows", []):
                        from pgmvox.built import props as PR
                        PR.scarecrow(w, sx, sz, L.get("facing", "n"))
                else:
                    got = GR.flower_rows(w, where, g_at, [block(f) for f in L["flowers"]], along=L.get("along", "x"),
                                         rows=L.get("rows", 2), angle=L.get("angle", 0.0))
            for x, z in got:
                if 0 <= x - x0 < laid.shape[0] and 0 <= z - z0 < laid.shape[1]:
                    laid[x - x0, z - z0] = True
        elif L["op"] == "paving":
            e, _ = area_distance(L["area"], X, Z, fields, lines)
            cell = L.get("cell", 3)
            pave = [block(b) for b in L["blocks"]]
            pick = np.random.default_rng(L.get("seed", bd.get("seed", 0))).integers(
                len(pave), size=(X.shape[0] // cell + 2, X.shape[1] // cell + 2))
            for i, k in np.argwhere((e < 1) & land & (water == 0)):
                y = int(Hi[i, k])
                w.set(int(X[i, k]), y, int(Z[i, k]), *pave[pick[i // cell, k // cell]])
                if w.ids[i, y + 1, k] in (B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT):
                    w.ids[i, y + 1, k] = 0
                laid[i, k] = True
        elif L["op"] == "graves":
            from pgmvox.built import props as PR
            g_at = lambda x, z: int(Hi[x - x0, z - z0])                                     # noqa: E731
            rr = np.random.default_rng(L.get("seed", bd.get("seed", 0)))
            flowers = [block(f) for f in L.get("flowers", [["FLOWER", 0]])]
            for gx, gz in L["at"]:
                fl = flowers[int(rr.integers(len(flowers)))] if rr.random() < L.get("flowered", 0.4) else None
                for x, z in PR.grave(w, gx, gz, g_at, L.get("facing", "e"), block(L.get("stone", ["STONE", 6])),
                                     block(L.get("cap", ["SLAB", 5])), block(L.get("soil", ["DIRT", 1])), fl):
                    laid[x - x0, z - z0] = True
        elif L["op"] == "field":
            from pgmvox.built import props as PR
            a0, b0, a1, b1 = L["rect"]
            y = L["y"] if "y" in L else int(np.median(Hi[a0 - x0:a1 - x0 + 1, b0 - z0:b1 - z0 + 1]))
            PR.crop_field(w, (a0, b0, a1, b1), y, [block(c) for c in L.get("crops", [["WHEAT", 7]])],
                          np.random.default_rng(L.get("seed", bd.get("seed", 0))), rows=L.get("rows", 9),
                          ditch=L.get("ditch", 4), fence=L.get("fence", "w"), gate=L.get("gate"))
            for sx, sz in L.get("scarecrows", []):
                PR.scarecrow(w, sx, sz, L.get("facing", "n"))
            laid[a0 - x0:a1 - x0 + 1, b0 - z0:b1 - z0 + 1] = True
        elif L["op"] == "blocks":
            boxes = L["boxes"]
            if "rel" in L:                                       # heights over the floor of the house it names
                dy = floors[L["rel"]]
                boxes = [dict(b, box=[b["box"][0], b["box"][1] + dy, b["box"][2], b["box"][3], b["box"][4] + dy,
                                      b["box"][5]]) for b in boxes]
            for x, _, z in _props(w, boxes):
                laid[x - x0, z - z0] = True
        built_on |= laid
        out.steps.append(Step(L["id"], "build", L["op"], laid, Hi.copy(), L.get("note", "")))
    for L in doc.get("dress", []):
        laid = np.zeros(X.shape, bool)
        if L["op"] == "trees":
            from pgmvox.scenery import trees as TR
            e, _ = area_distance(L["area"], X, Z, fields, lines)
            clear = ndimage.binary_dilation(built_on, iterations=L.get("clear", 3))
            on = L.get("on", "ground" if any(sf.kind in ("level", "deck") for sf in out.surfaces) else None)
            stand = ok = None
            if on is None:
                zone = (e < 1) & land & (water == 0) & ~clear
            else:
                sf = out.surface(on)
                if sf.kind == "deck":
                    clear = ndimage.binary_dilation(built_on & (sf.top < 0), iterations=L.get("clear", 3))
                zone = (e < 1) & (sf.top >= 0) & ~clear & (True if sf.water is None else sf.water == 0)
                stand, ok = _standing(sf, x0, z0)
            kinds = TR.kinds(TR.library())
            weights = {k: v for k, v in L["kinds"].items() if k in kinds}
            planted = []
            TR.scatter(w, zone, kinds, weights, np.random.default_rng(L.get("seed", 0)), tries=L.get("tries", 400),
                       planted=planted, ok=ok, ground=stand, spacing=L.get("spacing", 0.85))
            for x, z, _ in planted:
                laid[x - x0, z - z0] = True
        out.steps.append(Step(L["id"], "dress", L["op"], laid, Hi.copy(), L.get("note", "")))
    for L in doc.get("snow", []):
        e = area_distance(L["area"], X, Z, fields, lines)[0] < 1 if "area" in L else np.ones(X.shape, bool)
        if "where" in L:
            e &= np.asarray(expr(L["where"], Ctx(X, Z, Hi.astype(float), fields, lines, land, water)), bool)
        n = T.smooth_snow(w, L.get("smoothness", 6), mask=e, on={block(b)[0] for b in L["on"]} if "on" in L else None,
                          added=L.get("added", 0.4), overlay=L.get("overlay", False), max_depth=L.get("max_depth"),
                          under=block(L["under"]) if "under" in L else None)
        out.steps.append(Step(L["id"], "snow", "smooth_snow", e.copy(), Hi.copy(), f"{n} columns covered"))
    if "biome" in bd:
        w.biome[:] = int(bd["biome"])
    for L in doc.get("symmetry", []):
        from pgmvox.core.orient import turn_world
        cx = Ctx(X, Z, Hi.astype(float), fields, lines, land, water)
        keep = np.asarray(expr(L["keep"], cx), bool)
        recolour = {block(a): block(b) for a, b in L.get("recolour", [])}
        turn_world(w, L["op"], keep, recolour=recolour or None)
        for sf in out.surfaces:
            for name in ("top", "water", "ceiling"):
                if getattr(sf, name) is not None:
                    setattr(sf, name, _turned(getattr(sf, name), L["op"], keep, x0, z0))
        out.steps.append(Step(L["id"], "symmetry", L["op"], ~keep, Hi.copy(), L.get("note", "")))
    out.H, out.land, out.water = Hi, land, water
    return out


TOP = T.by_angle([(55, (B.GRASS, 0)), (90, (B.STONE, 0))])
ROCK = T.Strata([((B.STONE, 0), 3, 6), ((B.STONE, 5), 1.4, 3)], length=60, seed=7, start=-300)


def _below(surfaces, H):
    """Under each column, the highest surface whose top lies under H; -1 where none does."""
    lower = np.full(H.shape, -1)
    for sf in surfaces:
        lower = np.maximum(lower, np.where((sf.top >= 0) & (sf.top < H), sf.top, -1))
    return lower


def _level(L, doc, w, share, out):
    """A level: its own ground over its own outline, laid into a world of its own and copied in where it holds a
    block, so the ground under it stands. Its underside tapers as an island's does; where that leaves less than
    `clear` blocks over the surface below, the level rests on it instead and buries it, its soil with it. Its water may fall off
    its edge at each of `falls`: the columns off the level within `r` of `at`, from the nearest water's surface down
    to the surface under them."""
    X, Z = share.X, share.Z
    bd = doc["board"]
    sub = {"board": bd, "floor": L.get("floor", bd.get("floor", 40)), "ground": L["ground"]}
    c, steps = ground(sub, X, Z, share=share, level=L["id"])
    out.steps.extend(steps)
    land = c.land
    water = np.where(land, c.water, 0)
    H = np.round(c.H).astype(int)
    H = np.where(water > 0, np.minimum(H, water - 1), H)
    lower = _below(out.surfaces, H)
    u = L.get("underside", {})
    if "bottom" in u:                                        # an underside stated as a field: a face that leans
        bottom = np.round(np.asarray(expr(u["bottom"], c), float) + np.zeros(X.shape)).astype(int)
    else:
        bottom = T.island_bottom(H, land, np.zeros(X.shape, bool), taper=tuple(u.get("taper", (4, 0.9))),
                                 rough=u.get("rough", 0) * noise.fbm(X.shape, 12, 2, seed=u.get("seed", 0)))
    rests = land & (lower >= 0) & (bottom <= lower + u.get("clear", 4))
    bottom = np.where(rests, lower - 3, bottom)
    tmp = World(w.x0, w.z0, w.sx, w.sz, sy=w.sy)
    paint = [_paint_layer(P, X, Z, c.fields, c.lines, H) for P in L.get("paint", [])]
    T.lay(tmp, np.where(land, H, -1), land, top=TOP, bands=T.beds(ROCK, H, seed=3), paint=paint, bottom=bottom,
          dirt_depth=L.get("soil"))
    if (water > 0).any():
        bed = [_paint_layer(P, X, Z, c.fields, c.lines, H) for P in L.get("water", {}).get("bed", [])] \
            or (B.GRAVEL, 0)
        T.fill_water(tmp, H, water, bed=bed, mask=land)
    held = tmp.ids != 0
    w.ids[held], w.dat[held] = tmp.ids[held], tmp.dat[held]
    for sf in out.surfaces:
        sf.top = np.where(rests & (sf.top == lower), -1, sf.top)
        if sf.ceiling is not None:
            sf.ceiling = np.where(land & ~rests & (sf.top >= 0) & (sf.top < bottom),
                                  np.minimum(sf.ceiling, bottom), sf.ceiling)
    fell = 0
    for f in L.get("falls", []):
        (fx, fz), r = f["at"], f.get("r", 1.5)
        d = np.hypot(X - fx, Z - fz)
        wet = land & (water > 0) & (d <= r + 4)
        if not wet.any():
            raise ValueError(f"level {L['id']}: no water within {r + 4} blocks of the fall at {f['at']}")
        lip = int(water[wet].max())
        for i, k in np.argwhere((d <= r) & ~land):
            for y in range(max(int(lower[i, k]) + 1, 1), lip + 1):
                if w.ids[i, y, k] == 0:
                    w.ids[i, y, k], w.dat[i, y, k] = B.WATER_FLOW, 8
                    fell += 1
    out.surfaces.append(Surface(L["id"], "level", np.where(land, H, -1), water, np.full(X.shape, w.sy)))
    out.steps.append(Step(L["id"], "levels", "level", land.copy(), H.copy(),
                          f"rests on {int(rests.sum())} columns, {fell} blocks of fall", L["id"]))


def _standing(sf, x0, z0):
    """(ground, ok) for trees on a surface: they stand on its top, and only where their crown clears its ceiling."""
    top, ceiling = sf.top, sf.ceiling

    def ground(x, z):
        i, k = x - x0, z - z0
        return int(top[i, k]) if 0 <= i < top.shape[0] and 0 <= k < top.shape[1] else -1

    def ok(x, z, tree):
        if ceiling is None:
            return True
        return ground(x, z) + 1 + max(b[1] for b in tree.blocks) < ceiling[x - x0, z - z0]
    return ground, ok


def _turned(a, op, keep, x0, z0):
    """A per-column array after the symmetry: the kept columns copied onto their images."""
    from pgmvox.core.orient import turn_xz
    out = a.copy()
    si, sk = np.nonzero(keep)
    for i, k in zip(si, sk):
        x, z = turn_xz(int(i) + x0, int(k) + z0, op)
        ii, kk = int(x) - x0, int(z) - z0
        if 0 <= ii < a.shape[0] and 0 <= kk < a.shape[1]:
            out[ii, kk] = a[i, k]
    return out


def _arch(L, w, out):
    """A natural arch along `line`, `width` across: its deck at `deck` (crown, end, power) along the span, falling
    `camber` blocks to its sides, `thick` blocks of rock under it; laid only where the deck stands over the
    highest surface (or water) under it. The deck is a surface of its own. Returns the columns it laid."""
    from pgmvox.scenery import forms as FO
    X, Z = out.X, out.Z
    x0, z0 = int(X[0, 0]), int(Z[0, 0])
    pts = _line_pts(L["line"], Ctx(X, Z, None, {}, out.lines))
    d, arc = shapes.polyline(X.astype(float), Z.astype(float), pts)
    total = float(arc.max()) or 1.0
    half = L.get("width", 7) / 2
    t = np.abs(2 * arc / total - 1)
    crown, end, power = L["deck"]
    deck = np.round(crown + (end - crown) * t ** power - L.get("camber", 0) * (d / half) ** 2).astype(int)
    tc, te, tp = L.get("thick", [4, 12, 1.5])
    thick = np.round(tc + (te - tc) * t ** tp).astype(int)
    lower = np.full(X.shape, -1)
    for sf in out.surfaces:
        floor = np.where(sf.top >= 0, np.maximum(sf.top, sf.water if sf.water is not None else -1), -1)
        lower = np.maximum(lower, np.where(floor < deck, floor, -1))
    span = (d <= half) & (deck > lower + 1)
    top_b, under_b, rock_b = block(L.get("top", "GRASS")), block(L.get("under", "DIRT")), block(L.get("rock", "STONE"))
    rock = lambda x, y, z, k: top_b if k == 0 else under_b if k <= 2 else rock_b          # noqa: E731
    tops = np.full(X.shape, -1)
    for i, k in np.argwhere(span):
        x, z = int(X[i, k]), int(Z[i, k])
        got = FO.arch(w, [(x, z)], {(x, z): float(t[i, k])}, deck=lambda _, y=int(deck[i, k]): y,
                      thick=lambda _, n=int(thick[i, k]): n, rock=rock, clear=L.get("clear", 3),
                      ground=lambda _x, _z, g=int(lower[i, k]): g)
        tops[i, k] = got[(x, z)]
    for sf in out.surfaces:
        if sf.ceiling is not None:
            sf.ceiling = np.where(span & (sf.top >= 0) & (sf.top < tops), np.minimum(sf.ceiling, tops - thick),
                                  sf.ceiling)
    ceiling = np.full(X.shape, w.sy)
    out.surfaces.append(Surface(L["id"], "deck", tops, None, ceiling))
    return span


def _carve(layers, w, out, seed):
    """The carve stage: tunnels, chambers, rooms and shafts cut into the laid ground in order. Every carve keeps
    `cover` blocks under the ground the board stood with before the stage (the top of each column's lowest solid
    run), so a cave under a level that overhangs is guarded by the ground it is under, not the level. Each publishes
    its floor as a surface; a tunnel never cuts a room's blocks unless it is a `breach`, and dressing a cave never
    touches them."""
    from pgmvox.volume import under as UN
    X, Z = out.X, out.Z
    x0, z0 = int(X[0, 0]), int(Z[0, 0])
    roof = np.argmax(w.ids[:, 1:, :] == 0, axis=1)
    rng = np.random.default_rng(seed)
    made = set()

    def ground(x, z):
        i, k = x - x0, z - z0
        return int(roof[i, k]) if 0 <= i < roof.shape[0] and 0 <= k < roof.shape[1] else None

    def kept(x, y, z):
        return (x, y, z) in made
    for L in layers:
        before = w.ids.copy()
        top = np.full(X.shape, -1)
        op, cover = L["op"], L.get("cover", 3)
        if op == "tunnel":
            pts = [tuple(p) for p in L["pts"]]
            mouths = [pts[i] for i in L.get("mouths", [])]

            def guard(x, z, mouths=mouths):
                if any(math.hypot(x - mx, z - mz) <= mr + 1.5 for mx, _, mz, mr in mouths):
                    return None
                return ground(x, z)
            _, floor = UN.tunnel(w, pts, ground=guard, cover=cover, keep=None if L.get("breach") else kept,
                                 lift=L.get("lift", 0.45))
            r = max(p[3] for p in pts)
            box = (int(min(p[0] for p in pts) - r - 1), int(max(p[0] for p in pts) + r + 1),
                   int(min(p[2] for p in pts) - r - 1), int(max(p[2] for p in pts) + r + 1),
                   int(min(p[1] for p in pts)) - 1, int(max(p[1] for p in pts) + 2 * r + 2))
        elif op == "chamber":
            cx, fy, cz = L["at"]
            UN.chamber(w, cx, fy, cz, L["rx"], L["h"], rz=L.get("rz"), ground=ground, cover=cover, keep=kept)
            floor = lambda x, z, fy=fy: fy                                                # noqa: E731
            box = (int(cx - L["rx"] - 1), int(cx + L["rx"] + 1), int(cz - L.get("rz", L["rx"]) - 1),
                   int(cz + L.get("rz", L["rx"]) + 1), fy - 1, fy + L["h"] + 1)
        elif op == "rooms":
            floors = _rooms(L, w, ground, cover, made, np.random.default_rng(L.get("seed", seed)))
            for (x, z), f in floors.items():
                top[x - x0, z - z0] = f - 1
        elif op == "shaft":
            x, z = L["at"]
            head = ground(x, z) if L.get("top", "ground") == "ground" else int(L["top"])
            UN.shaft(w, x, z, L["bottom"], head, ladder_on=L.get("ladder_on", "s"),
                     **{k: block(L[k]) for k in ("wall", "post") if k in L})
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    for y in range(L["bottom"] - 1, head + 1):
                        made.add((x + dx, y, z + dz))
        else:
            raise ValueError(f"unknown carve op {op}")
        changed = (w.ids != before).any(axis=1)
        if op in ("tunnel", "chamber"):
            for i, k in np.argwhere(changed):
                f = floor(int(X[i, k]), int(Z[i, k]))
                if w.ids[i, f, k] == 0:
                    top[i, k] = f - 1
            if L.get("dress"):
                dr = L["dress"]
                UN.dress_cave(w, box, np.random.default_rng(dr.get("seed", seed)), ground=ground, keep=kept,
                              ores=dr.get("ores", 300), stalagmites=dr.get("stalagmites", 900),
                              stalactites=dr.get("stalactites", 0.05), mushrooms=dr.get("mushrooms", 0.015))
        if op != "shaft":
            out.surfaces.append(Surface(L["id"], "floor", top, None, None))
        out.steps.append(Step(L["id"], "carve", op, changed, None, L.get("note", "")))


def _rooms(L, w, ground, cover, made, rng):
    """A dungeon: `rooms` (rect [x0, z0, x1, z1], floor, h) and the `halls` between them (from, to, width, h, via
    "x" or "z" first), lined with `lining` (wall, floor, ceiling: a block or [[block, weight], ...]) wherever the
    rock is solid, lit by `light` torches on the room walls and furnished with `props` (a box of a block). A hall
    leaves each room at its floor and climbs or falls a block a step at most, on a stair, in its middle. Returns
    the floor of every column carved, {(x, z): y}."""
    from pgmvox.core.orient import stair as stair_data, torch as torch_data, vec
    rooms = {r["id"]: r for r in L["rooms"]}
    floors, high = {}, {}
    stairs = []

    def in_room(x, z, r):
        a0, b0, a1, b1 = r["rect"]
        return a0 <= x <= a1 and b0 <= z <= b1
    for r in rooms.values():
        a0, b0, a1, b1 = r["rect"]
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                floors[(x, z)], high[(x, z)] = r["floor"], r.get("h", 5)
    for hl in L.get("halls", []):
        a, b = rooms[hl["from"]], rooms[hl["to"]]
        ca = ((a["rect"][0] + a["rect"][2]) // 2, (a["rect"][1] + a["rect"][3]) // 2)
        cb = ((b["rect"][0] + b["rect"][2]) // 2, (b["rect"][1] + b["rect"][3]) // 2)
        corner = (cb[0], ca[1]) if hl.get("via", "x") == "x" else (ca[0], cb[1])
        path = _manhattan(ca, corner) + _manhattan(corner, cb)[1:]
        outside = [p for p in path if not in_room(*p, a) and not in_room(*p, b)]
        rise = b["floor"] - a["floor"]
        if len(outside) < abs(rise) + 2:
            raise ValueError(f"hall {hl['from']}-{hl['to']} is {len(outside)} long for a rise of {rise}")
        s0, sign = (len(outside) - abs(rise)) // 2, int(np.sign(rise))
        f_at = {p: a["floor"] + sign * int(np.clip(j - s0, 0, abs(rise))) for j, p in enumerate(outside)}
        width, h = hl.get("width", 3), hl.get("h", 4)
        for j, p in enumerate(outside):
            nxt = outside[min(j + 1, len(outside) - 1)]
            prv = outside[max(j - 1, 0)]
            dx, dz = vec((nxt[0] - prv[0], nxt[1] - prv[1])) if nxt != prv else (1, 0)
            across = [(p[0] - dz * o, p[1] + dx * o) for o in range(-(width // 2), width - width // 2)]
            if p == corner:
                across = [(p[0] + u, p[1] + v) for u in range(-(width // 2), width - width // 2)
                          for v in range(-(width // 2), width - width // 2)]
            for q in across:
                floors.setdefault(q, f_at[p])
                high.setdefault(q, h)
            if j + 1 < len(outside) and f_at[nxt] != f_at[p]:
                low, up = (p, nxt) if f_at[nxt] > f_at[p] else (nxt, p)
                nx_, nz_ = vec((up[0] - low[0], up[1] - low[1]))
                ldx, ldz = vec((nxt[0] - p[0], nxt[1] - p[1]))
                for o in range(-(width // 2), width - width // 2):
                    stairs.append((low[0] - ldz * o, f_at[low], low[1] + ldx * o, stair_data((nx_, nz_))))
    air = set()
    for (x, z), f in floors.items():
        g = ground(x, z)
        for y in range(f, f + high[(x, z)]):
            if g is not None and y > g - cover:
                continue
            if w.inside(x, y, z) and w.id(x, y, z) not in (B.WATER, B.WATER_FLOW):
                air.add((x, y, z))
    lining = L.get("lining", {})
    pick = {part: _mix(lining.get(part, "STONEBRICK"), rng) for part in ("wall", "floor", "ceiling")}
    for x, y, z in list(air):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    c = (x + dx, y + dy, z + dz)
                    if c in air or c in made or not w.inside(*c) or w.id(*c) in (B.AIR, B.WATER, B.WATER_FLOW):
                        continue
                    part = "floor" if (c[0], c[1] + 1, c[2]) in air else \
                        "ceiling" if (c[0], c[1] - 1, c[2]) in air else "wall"
                    w.set(*c, *pick[part]())
                    made.add(c)
    for c in air:
        w.set(*c, B.AIR)
        made.add(c)
    for x, y, z, d in stairs:
        if (x, y, z) in air:
            w.set(x, y, z, getattr(B, L.get("stair", "STONEBRICK_STAIRS")), d)
    light = L.get("light")
    if light:
        for r in rooms.values():
            a0, b0, a1, b1 = r["rect"]
            y = r["floor"] + light.get("y", 2)
            mx, mz = (a0 + a1) // 2, (b0 + b1) // 2
            for (x, z), side, wall in (((mx, b0), "n", (mx, b0 - 1)), ((mx, b1), "s", (mx, b1 + 1)),
                                       ((a0, mz), "w", (a0 - 1, mz)), ((a1, mz), "e", (a1 + 1, mz))):
                if (x, y, z) in air and (wall[0], y, wall[1]) not in air and w.id(wall[0], y, wall[1]) != B.AIR:
                    w.set(x, y, z, B.TORCH, torch_data(side))
    made |= _props(w, L.get("props", []))
    return {(x, z): f for (x, z), f in floors.items() if (x, f, z) in air}


def _door_path(w, Hi, door, spec, lines, x0, z0, built, rng):
    """A path one block wide from a house's door straight out until it meets the line `spec["to"]` names (within
    its width), laid in `blocks` a third each at random, with a low hedge of `leaves` beside it on its `side` (left
    or right of the way out), a gap left in it by chance `gaps`."""
    from pgmvox.core.orient import vec as vec_
    from pgmvox.geom.shapes import polyline
    x, z, facing = door
    dx, dz = vec_(facing)
    ln = lines[spec["to"]]
    pts = ln["pts"]
    blocks = [block(b) for b in spec.get("blocks", [["DIRT", 1], "GRAVEL", ["DIRT", 0]])]
    side = {"left": (dz, -dx), "right": (-dz, dx)}.get(spec.get("side", "left"))
    leaves = block(spec["leaves"]) if "leaves" in spec else None
    for k in range(1, spec.get("max", 16)):
        a, b = x + dx * k, z + dz * k
        if not (0 <= a - x0 < Hi.shape[0] and 0 <= b - z0 < Hi.shape[1]):
            break
        d, _ = polyline(np.array([[a + 0.5]]), np.array([[b + 0.5]]), pts)
        if float(d[0, 0]) < ln["width"] / 2:                      # where the paving of that line begins
            break
        y = int(Hi[a - x0, b - z0])
        w.set(a, y, b, *blocks[int(rng.integers(len(blocks)))])
        if w.id(a, y + 1, b) in (B.TALLGRASS, B.FLOWER, B.DANDELION):
            w.set(a, y + 1, b, B.AIR)
        if leaves is not None and side is not None and k > 1:
            ha, hb = a + side[0], b + side[1]
            if 0 <= ha - x0 < Hi.shape[0] and 0 <= hb - z0 < Hi.shape[1] and not built[ha - x0, hb - z0] \
                    and rng.random() >= spec.get("gaps", 0.2):
                w.set(ha, int(Hi[ha - x0, hb - z0]) + 1, hb, *leaves)


def _props(w, props):
    """Each prop's `box` (x0, y0, z0, x1, y1, z1) filled with its `block`, in order. Returns the blocks set."""
    laid = set()
    for pr in props:
        a0, y0, b0, a1, y1, b1 = pr["box"]
        one = block(pr["block"])
        for x in range(min(a0, a1), max(a0, a1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(b0, b1), max(b0, b1) + 1):
                    w.set(x, y, z, *one)
                    laid.add((x, y, z))
    return laid


def _manhattan(a, b):
    """The cells from a to b along one axis, a and b included."""
    (ax, az), (bx, bz) = a, b
    if ax != bx:
        step = 1 if bx > ax else -1
        return [(x, az) for x in range(ax, bx + step, step)]
    step = 1 if bz > az else -1
    return [(ax, z) for z in range(az, bz + step, step)]


def _mix(spec, rng):
    """A block drawn each call from a block or [[block, weight], ...]."""
    if isinstance(spec, list) and spec and all(isinstance(e, list) for e in spec):
        blocks = [block(b) for b, _ in spec]
        p = np.array([wt for _, wt in spec], float)
        p /= p.sum()
        return lambda: blocks[int(rng.choice(len(blocks), p=p))]
    one = block(spec)
    return lambda: one


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
