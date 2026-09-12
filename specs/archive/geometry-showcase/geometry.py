"""The shape vocabulary this board is drawn with.

Every construct here is a sketch shape and nothing else: a rectangle, a polygon with per-vertex
anchor heights, a polyline with heights along its arc. The one fact the whole file turns on is how
the rasterizer reads a height: it samples the interpolated surface at the cell centre and takes
`Math.Round` of it, so the anchors a flight is stated with decide whether its treads come out one
course apart or two.
"""
import math

BIAS = 0.02          # breaks Math.Round's half-to-even tie upward, deterministically


def grade(t_start, t_end, cells):
    """The two anchor values a flight of `cells` cells needs to run from top block `t_start` to
    top block `t_end`, one value per end of the run.

    The sampler reads thickness = Round(h(cell centre)) and a column's top block is thickness - 1.
    Wanting cell i to top out at t_start + i*step means h(i + 0.5) = t_start + 1 + i*step, so the
    line is anchored half a step below the run's first cell."""
    if cells < 2:
        raise ValueError("a flight is at least two cells")
    step = (t_end - t_start) / (cells - 1)
    a0 = t_start + 1 - 0.5 * step + BIAS
    return a0, a0 + step * cells


def treads(t_start, t_end, cells):
    """What `grade` will actually build, cell by cell — the same arithmetic the rasterizer does,
    used to state a landing's height rather than guess it."""
    step = (t_end - t_start) / (cells - 1)
    a0 = t_start + 1 - 0.5 * step + BIAS
    return [math.floor(a0 + step * (i + 0.5) + 0.5) - 1 for i in range(cells)]


def rect(id, x0, z0, x1, z1, floor, height, **kw):
    return dict(id=id, type="rectangle", operation="add",
                min_x=x0, min_z=z0, max_x=x1, max_z=z1,
                floor=floor, base_height=height, **kw)


def flight(id, x0, z0, x1, z1, axis, t_start, t_end, **kw):
    """A quad whose surface tilts along one axis — a stair, a ramp, a bank. `axis` is the axis it
    climbs along, and `t_start`/`t_end` are the top blocks of its first and last cell in the
    direction of increasing x or z; state them the other way round to make it descend."""
    cells = (x1 - x0) if axis == "x" else (z1 - z0)
    lo, hi = grade(t_start, t_end, cells)
    if axis == "x":
        verts = [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]
        anchors = [lo, hi, hi, lo]
    else:
        verts = [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]
        anchors = [lo, lo, hi, hi]
    return dict(id=id, type="polygon", operation="add", floor=0,
                vertices=verts, anchor_heights=anchors, **kw)


def stroke(id, points, heights, radius, **kw):
    """A polyline: the drawn points are splined and the band offset either side of the result, and
    the heights interpolate along the arc rather than over an enclosed area."""
    return dict(id=id, type="polyline", operation="add", floor=0,
                vertices=[[p[0], p[1]] for p in points],
                anchor_heights=list(heights), radius=radius, **kw)


def ring(id, cx, cz, r_out, r_in, floor, height, gaps=(), points=72, **kw):
    """A hollow ring as ONE polygon: the outer circle, a slit inward, the inner circle traced the
    other way round, and back along the slit. The fill rule is even-odd, so the doubly-wound middle
    falls outside the shape and the annulus stands — no subtract, so nothing for SK13 to refuse.

    `gaps` are (from, to) bearings in degrees left open, which turns the ring into arcs."""
    def arc(a0, a1, r, n):
        return [(cx + r * math.cos(math.radians(a)), cz + r * math.sin(math.radians(a)))
                for a in [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]]

    spans, at = [], 0.0
    for g0, g1 in sorted(gaps):
        if g0 > at:
            spans.append((at, g0))
        at = g1
    if at < 360:
        spans.append((at, 360.0))
    if not gaps:
        spans = [(0.0, 360.0)]

    out = []
    for a0, a1 in spans:
        n = max(6, int(points * (a1 - a0) / 360))
        verts = arc(a0, a1, r_out, n) + list(reversed(arc(a0, a1, r_in, n)))
        out.append(dict(id=f"{id}-{len(out)}", type="polygon", operation="add",
                        vertices=[[round(x, 3), round(z, 3)] for x, z in verts],
                        floor=floor, base_height=height, **kw))
    return out


def spiral(cx, cz, r0, r1, turns, start_deg=0.0, samples=9):
    """The clicked points of an Archimedean spiral — a radius that shrinks as it winds, so
    successive turns lie beside one another instead of over one another. A polyline whose radius
    were constant would be a helix, and a helix cannot be one shape: a layer keeps one span per
    column and every turn would contest the same cells."""
    n = int(samples * turns)
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(start_deg) + 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((round(cx + r * math.cos(a), 2), round(cz + r * math.sin(a), 2)))
    return pts


def rot180(shape):
    """The rot_180 image of a shape about the origin: (x, z) -> (-x, -z). Heights are untouched,
    because a rotation about the vertical axis does not move anything in y, and the vertex order a
    ring was wound in survives it, so the anchors still line up with the points they were stated
    for."""
    s = dict(shape)
    s["id"] = shape["id"].replace("-r-", "-b-") if "-r-" in shape["id"] else shape["id"] + "-b"
    if s.get("min_x") is not None:
        s["min_x"], s["max_x"] = -shape["max_x"], -shape["min_x"]
        s["min_z"], s["max_z"] = -shape["max_z"], -shape["min_z"]
    if s.get("center_x") is not None:
        s["center_x"], s["center_z"] = -shape["center_x"], -shape["center_z"]
    if s.get("vertices"):
        s["vertices"] = [[-x, -z] for x, z in shape["vertices"]]
    return s


def spiral_arcs(id, cx, cz, r0, r1, turns, t_start, t_end, band,
                start_deg=0.0, per_turn=24, arcs_per_turn=2, **kw):
    """A spiral ramp, as one polyline per part-turn rather than one polyline for the whole coil.

    A single polyline would be wrong, and measurably so: the band is offset either side of the
    centreline into ONE ring, and a ring is filled even-odd, so wherever a coil's band laps the
    turn beside it the two windings cancel and the lap comes back as void. Split into arcs that
    cannot lap themselves, the laps become two shapes contesting a column, where the taller add
    wins and the coil is continuous.

    The heights are read off the whole spiral's arc length, so the seams carry the same course on
    both sides and the flights below run one continuous gradient."""
    n = int(per_turn * turns)
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(start_deg) + 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))

    run = [0.0]
    for a, b in zip(pts, pts[1:]):
        run.append(run[-1] + math.dist(a, b))
    # +1 on the thickness: a column's top block is its thickness less one, so a flight arriving at
    # top block `t_end` is a thickness of t_end + 1.
    height = [t_start + 1 + (t_end - t_start) * c / run[-1] for c in run]

    step = max(2, int(per_turn / arcs_per_turn))
    out = []
    for s in range(0, n, step):
        e = min(n, s + step)
        out.append(dict(id=f"{id}-{len(out)}", type="polyline", operation="add", floor=0,
                        vertices=[[round(x, 3), round(z, 3)] for x, z in pts[s:e + 1]],
                        anchor_heights=[round(h, 3) for h in height[s:e + 1]],
                        radius=band, stroke_edge="solid", **kw))
    return out
