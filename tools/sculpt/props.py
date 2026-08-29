"""Structures written in the sketch's own shapes — circles, polygons and rectangles on a layer.

This is the other half of the answer, and the half that could become a tool. `layers.py` compiles a voxel
model into rectangles, which is general and unreadable; everything here emits **the shapes an author would
have drawn**, so what lands in the document is a handful of circles with a floor and a height, editable in
the Draw phase afterwards.

Three facts about a layer make it possible, and all three are law rather than tricks:

**The taller add wins the column outright, floor included.** So a layer is not a flat slab — it is one
arbitrary *height field*, `(floor, top)` per column, written as a stack of shapes ordered so that the one
meant to win is the tallest. A solid dome is concentric discs whose tops rise inward; a hollow one is the
same discs with their floors rising too, which is what leaves a shell. `SK9` names a pair only where one
shape's floor sits at or above another's top, so nested discs sharing a floor, or rising by less than the
shell is thick, say nothing.

**An outline is filled even-odd, so a ring is one polygon.** Run the outer circle, slit inward, run the
inner circle the other way and close: the interior is crossed twice and falls outside the fill, and the slit's
two coincident edges cancel. That is `annulus` below, and it is why nothing here hollows a shape with a
subtract — a subtract states the *board's* negative space and `SK13` refuses any add over one, on any layer,
so the deck a tower stands on and the roof over it both collide with the subtract that hollowed it.

**An override add replaces the column it lands on whatever its height.** The ordinary adds settle among
themselves by height and the override adds then overwrite them, so a layer carries two height fields, one
masking the other. That is what puts a floor inside a wall and a threshold through a doorway.

Every emitter returns layers ready to drop into a document, and takes the theme id its shapes paint with.
"""
import math


class LayerBuilder:
    """One layer under construction: shapes get their ids here, and the group is closed at the end so a
    whole structure can be turned off the mirror in one flag."""

    def __init__(self, layer_id, name=None, base_y=0, mirrors=False, tag=None):
        self.id = layer_id
        self.name = name or layer_id
        self.base_y = base_y
        self.mirrors = mirrors
        self.tag = tag or layer_id
        self.shapes = []

    def add(self, shape):
        shape.setdefault("id", f"{self.tag}-{len(self.shapes)}")
        shape.setdefault("operation", "add")
        shape.setdefault("keepClear", True)
        self.shapes.append(shape)
        return shape

    def disc(self, cx, cz, r, floor, height, theme, **rest):
        return self.add({"type": "circle", "center_x": cx, "center_z": cz, "radius": r,
                         "floor": floor, "base_height": height, "theme": theme, **rest})

    def rect(self, x0, z0, x1, z1, floor, height, theme, **rest):
        return self.add({"type": "rectangle", "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
                         "floor": floor, "base_height": height, "theme": theme, **rest})

    def poly(self, points, floor, height, theme, **rest):
        return self.add({"type": "polygon", "vertices": [[p[0], p[1]] for p in points],
                         "floor": floor, "base_height": height, "theme": theme, **rest})

    def done(self):
        return {"id": self.id, "name": self.name, "base_y": self.base_y,
                "layout": {"shapes": self.shapes,
                           "groups": [{"id": f"{self.id}-body", "name": self.name,
                                        "mirrors": self.mirrors,
                                        "shapeIds": [s["id"] for s in self.shapes]}]}}


def ellipse(cx, cz, rx, rz, points=64, rotate=0.0, reverse=False):
    """An ellipse as a polygon ring. The sketch has a circle primitive and no ellipse, so this is what an
    ellipse is: the outline an author would place by hand, at whatever resolution the shape deserves."""
    turn = math.radians(rotate)
    order = range(points - 1, -1, -1) if reverse else range(points)
    out = []
    for i in order:
        a = 2 * math.pi * i / points
        x, z = rx * math.cos(a), rz * math.sin(a)
        out.append((cx + x * math.cos(turn) - z * math.sin(turn),
                    cz + x * math.sin(turn) + z * math.cos(turn)))
    return out


def annulus(cx, cz, rx, rz, thickness, points=64, rotate=0.0):
    """A ring as **one** outline: the outer ellipse, a slit inward, the inner ellipse the other way round,
    and back. Even-odd fill puts the middle outside the shape, and the slit's two coincident edges cancel —
    so an annulus costs one shape and no subtract, which is what keeps `SK13` out of every hollow form."""
    outer = ellipse(cx, cz, rx, rz, points, rotate)
    inner = ellipse(cx, cz, max(0.5, rx - thickness), max(0.5, rz - thickness), points, rotate, reverse=True)
    return outer + [outer[0]] + inner + [inner[0]]


# ── the round forms ───────────────────────────────────────────────────────────────────────────────────────

def ring_wall(layer_id, cx, cz, outer, thickness, floor, height, theme, doors=(), inner_floor=None,
              points=64, **kw):
    """A hollow cylinder — the roundhouse wall, as one annulus polygon.

    `inner_floor` lays a slab inside it, as an override add: the override plane beats the ordinary one
    whatever their heights, so a one-block floor sits inside a twelve-block wall without either shape being
    cut against the other. `doors` are `(bearing_degrees, width)` pairs measured clockwise from north, each
    an override add across the wall at the same level — a threshold, which is what a doorway is."""
    layer = LayerBuilder(layer_id, **kw)
    layer.poly(annulus(cx, cz, outer, outer, thickness, points), floor, height, theme)
    if inner_floor is not None:
        layer.disc(cx, cz, outer - thickness + 0.5, floor, 1, inner_floor, override=True)
    for bearing, width in doors:
        a = math.radians(bearing)
        dx, dz = math.sin(a), -math.cos(a)
        px, pz = cx + dx * (outer - thickness / 2), cz + dz * (outer - thickness / 2)
        nx, nz = -dz, dx
        reach = thickness + 2
        layer.poly([(px + nx * width / 2 - dx * reach, pz + nz * width / 2 - dz * reach),
                    (px - nx * width / 2 - dx * reach, pz - nz * width / 2 - dz * reach),
                    (px - nx * width / 2 + dx * reach, pz - nz * width / 2 + dz * reach),
                    (px + nx * width / 2 + dx * reach, pz + nz * width / 2 + dz * reach)],
                   floor, 1, inner_floor or theme, override=True)
    return layer.done()


def ellipse_wall(layer_id, cx, cz, rx, rz, thickness, floor, height, theme, rotate=0.0, inner_floor=None,
                 points=64, **kw):
    """The hollow ellipse — the same annulus with two radii. The inner ring is the outer one shrunk along
    both axes rather than offset along its normal, which is what an author dragging the transform box would
    get, and for an ellipse of moderate eccentricity the two agree to a block."""
    layer = LayerBuilder(layer_id, **kw)
    layer.poly(annulus(cx, cz, rx, rz, thickness, points, rotate), floor, height, theme)
    if inner_floor is not None:
        layer.poly(ellipse(cx, cz, rx - thickness + 0.5, rz - thickness + 0.5, points, rotate),
                   floor, 1, inner_floor, override=True)
    return layer.done()


def dome(layer_id, cx, cz, radius, floor, theme, thickness=None, squash=1.0, steps=None, **kw):
    """A dome, solid or hollow, as **one layer**.

    Concentric discs whose tops rise inward, so the taller add wins each ring of columns outright. Hollow is
    the same discs with their floors rising by the shell's own curvature — the span each column keeps is then
    the shell's thickness at that radius, which is what a dome is.

    `squash` below 1 flattens it into a saucer; above 1 draws it out into an onion."""
    layer = LayerBuilder(layer_id, **kw)
    steps = steps or max(3, int(radius))
    inner_radius = None if thickness is None else max(0.0, radius - thickness)
    for i in range(steps):
        # The crown is a disc rather than a vanishing one: a ring narrower than a block draws nothing, and
        # what that leaves is a hole in the top of the dome.
        r = max(1.0, radius * (1 - i / steps))
        rise = math.sqrt(max(0.0, radius * radius - r * r)) * squash
        if inner_radius is None:
            base = floor
        else:
            under = math.sqrt(max(0.0, inner_radius ** 2 - r * r)) * squash
            base = floor + int(round(under))
        top = floor + int(round(rise)) + 1
        if top - base < 1:
            continue
        layer.disc(cx, cz, r, base, top - base, theme)
    return layer.done()


def spire(layer_id, cx, cz, radius, floor, height, theme, steps=None, sides=None, **kw):
    """A cone or a pyramid, again one layer: discs (or regular polygons) narrowing as they rise, each taller
    than the ring it stands inside."""
    layer = LayerBuilder(layer_id, **kw)
    steps = steps or max(3, int(height))
    for i in range(steps):
        r = max(1.0, radius * (1 - i / steps))
        top = floor + int(round(height * i / steps)) + 1
        if sides:
            layer.poly(ellipse(cx, cz, r, r, points=sides, rotate=180 / sides), floor, top - floor, theme)
        else:
            layer.disc(cx, cz, r, floor, top - floor, theme)
    return layer.done()


def ziggurat(layer_id, cx, cz, half, floor, tiers, tier_height, inset, theme, **kw):
    """A stepped mound: squares narrowing as they rise. The plainest case of the same rule, and the one worth
    reading first — four rectangles on one layer, each taller than the one around it."""
    layer = LayerBuilder(layer_id, **kw)
    for tier in range(tiers):
        reach = half - tier * inset
        layer.rect(cx - reach, cz - reach, cx + reach, cz + reach,
                   floor, tier_height * (tier + 1), theme)
    return layer.done()


def colonnade(layer_id, cx, cz, radius, count, pillar, floor, height, theme, **kw):
    """A ring of pillars — one layer, because the discs never touch. What a peristyle is, and what a
    generated ruin wants."""
    layer = LayerBuilder(layer_id, **kw)
    for i in range(count):
        a = 2 * math.pi * i / count
        layer.disc(cx + radius * math.cos(a), cz + radius * math.sin(a), pillar, floor, height, theme)
    return layer.done()


def tapered_tower(layer_id, cx, cz, base_radius, top_radius, thickness, floor, height, theme, courses=None,
                  points=64, **kw):
    """A round tower that narrows as it rises: nested annuli whose tops rise inward, on **one** layer.

    The rings are disjoint in plan where the taper is shallower than the wall is thick, and where they do
    overlap the taller one wins, which is the same rule the dome is built on. So a tower costs one layer and
    one shape a course."""
    layer = LayerBuilder(layer_id, **kw)
    courses = courses or max(2, height // 4)
    for i in range(courses):
        t = i / courses
        radius = base_radius + (top_radius - base_radius) * t
        top = floor + int(round(height * (i + 1) / courses))
        layer.poly(annulus(cx, cz, radius, radius, thickness, points), floor, top - floor, theme)
    return layer.done()


def arch(layer_id, x0, x1, cz, thickness, floor, clear_height, rise, theme, steps=None, **kw):
    """A gateway: two piers and the voussoir over them, cut as one span per column. The arch's underside is a
    half-ellipse, so each column of the span has floor `clear_height + the curve` and a top at the crown —
    one span, one layer, and the piers are on it too since they share no column with the vault."""
    layer = LayerBuilder(layer_id, **kw)
    span = (x1 - x0) / 2
    mid = (x0 + x1) / 2
    steps = steps or max(4, int(span))
    layer.rect(x0 - thickness, cz - thickness / 2, x0, cz + thickness / 2, floor,
               clear_height + rise + 2, theme)
    layer.rect(x1, cz - thickness / 2, x1 + thickness, cz + thickness / 2, floor,
               clear_height + rise + 2, theme)
    for i in range(steps):
        half = span * (1 - i / steps)
        under = clear_height + rise * math.sqrt(max(0.0, 1 - (half / span) ** 2)) if span else clear_height
        base = floor + int(round(under))
        top = floor + clear_height + rise + 2
        layer.rect(mid - half, cz - thickness / 2, mid + half, cz + thickness / 2,
                   base, top - base, theme)
    return layer.done()


def bowl(layer_id, cx, cz, radius, rim_y, depth, theme, steps=6, seat=3, points=64, **kw):
    """An amphitheatre — the one form nesting cannot draw, and the reason the annulus matters.

    A dome's height field **rises** inward, so the shape meant to win a column is also the tallest and plain
    nesting settles it. A bowl's field **falls** inward, and a disc that should keep only its own ring is the
    tallest thing over the middle as well: nested discs come out as a flat plate. What a falling field needs
    is shapes that do not overlap at all — which is exactly what a ring is, so the tiers are annuli, and one
    layer holds the lot."""
    layer = LayerBuilder(layer_id, **kw)
    floor_y = rim_y - int(round(depth))
    layer.disc(cx, cz, radius * (1 - (steps - 1) / steps), floor_y - seat, seat, theme)
    for i in range(steps):
        outer = radius * (1 - i / steps)
        drop = depth * (1 - (outer / radius) ** 2) if radius else 0
        top = rim_y - int(round(drop))
        layer.poly(annulus(cx, cz, outer, outer, radius / steps, points), top - seat, seat, theme)
    return layer.done()


# ── the fortified forms ───────────────────────────────────────────────────────────────────────────────────

def crenellated_wall(layer_id, x0, z0, x1, z1, thickness, floor, height, theme, merlon=3, crenel=2,
                     parapet=3, **kw):
    """A curtain wall with a walkway and battlements, on one layer.

    **A merlon is a full-height shape, not a block sitting on the wall.** A layer holds one span per column
    and the taller add wins it *floor included*, so a merlon stated as `[wall top, wall top + parapet]`
    replaces the wall under it outright and the battlement comes out as a picket fence with daylight between
    the pales — which is exactly what `SK9` is for, and it names the pair. Stated from the wall's own floor
    to the merlon's top it is simply the taller shape over those columns, and the wall beneath survives."""
    layer = LayerBuilder(layer_id, **kw)
    along_x = abs(x1 - x0) >= abs(z1 - z0)
    lo, hi = (min(x0, x1), max(x0, x1)) if along_x else (min(z0, z1), max(z0, z1))
    cross = (min(z0, z1), max(z0, z1)) if along_x else (min(x0, x1), max(x0, x1))

    def place(a0, a1, b0, b1, base, thick):
        if along_x:
            layer.rect(a0, b0, a1, b1, base, thick, theme)
        else:
            layer.rect(b0, a0, b1, a1, base, thick, theme)

    place(lo, hi, cross[0], cross[1], floor, height)
    step = merlon + crenel
    at = lo
    while at < hi:
        end = min(at + merlon, hi)
        place(at, end, cross[0], cross[0] + thickness, floor, height + parapet)
        place(at, end, cross[1] - thickness, cross[1], floor, height + parapet)
        at += step
    return layer.done()


def drum_tower(layer_id, cx, cz, outer, thickness, floor, height, theme, merlons=10, parapet=3,
               inner_floor=None, points=64, **kw):
    """A round tower with a crenellated crown: the shaft is one annulus, the merlons are wedges of a second
    annulus standing above it, and a `merlons` of zero leaves a plain parapet. Two layers, because the crown
    stands on the shaft's own top rather than beside it."""
    shaft = LayerBuilder(layer_id, **kw)
    shaft.poly(annulus(cx, cz, outer, outer, thickness, points), floor, height, theme)
    if inner_floor is not None:
        shaft.disc(cx, cz, outer - thickness + 0.5, floor, 1, inner_floor, override=True)

    crest = dict(kw)
    crest["name"] = f"{crest.get('name', layer_id)} crown"
    # The crown is its own layer, because a merlon and the shaft below it would be two spans on one — the
    # same rule `crenellated_wall` gets round by stating each merlon full height. Here a second layer is the
    # cleaner answer: the shaft's walkway stays, and the crenels stand on it with air in between.
    crown = LayerBuilder(f"{layer_id}-crown", **crest)
    if merlons:
        for i in range(merlons):
            a0 = 2 * math.pi * i / merlons
            a1 = a0 + math.pi / merlons
            arc = [(cx + (outer + 0.4) * math.cos(a), cz + (outer + 0.4) * math.sin(a))
                   for a in (a0 + (a1 - a0) * k / 6 for k in range(7))]
            arc += [(cx + (outer - thickness) * math.cos(a), cz + (outer - thickness) * math.sin(a))
                    for a in (a1 - (a1 - a0) * k / 6 for k in range(7))]
            crown.poly(arc, floor + height, parapet, theme)
    else:
        crown.poly(annulus(cx, cz, outer, outer, thickness, points), floor + height, parapet, theme)
    return [shaft.done(), crown.done()]


def gatehouse(layer_id, cx, cz, span, floor, theme, roof_theme=None, wing=26, wall_height=11,
              tower_radius=8, tower_height=17, **kw):
    """Two drum towers and the curtain between them, with a gate arched through it — a composite of the
    emitters above, which is what a stamper in the tool would be. Six layers and about sixty shapes for a
    fifty-block frontage, all of them circles, polygons and rectangles an author can still drag."""
    half = span / 2
    out = []
    named = {k: v for k, v in kw.items() if k != "name"}
    out += drum_tower(f"{layer_id}-w", cx - half, cz, tower_radius, 2, floor, tower_height, theme,
                      inner_floor=theme, name=f"{layer_id} west tower", **named)
    out += drum_tower(f"{layer_id}-e", cx + half, cz, tower_radius, 2, floor, tower_height, theme,
                      inner_floor=theme, name=f"{layer_id} east tower", **named)
    out.append(arch(f"{layer_id}-gate", cx - half + tower_radius + 1, cx + half - tower_radius - 1, cz, 6,
                    floor, 8, 6, theme, steps=9, name=f"{layer_id} gate", **named))
    out.append(crenellated_wall(f"{layer_id}-parapet", cx - half + tower_radius - 3, cz - 3,
                                cx + half - tower_radius + 3, cz + 3, 1, floor + 16, 1, roof_theme or theme,
                                merlon=3, crenel=2, parapet=2, name=f"{layer_id} gate parapet", **named))
    out.append(crenellated_wall(f"{layer_id}-w-wall", cx - half - tower_radius - wing, cz - 2.5,
                                cx - half - tower_radius + 1, cz + 2.5, 1, floor, wall_height, theme,
                                name=f"{layer_id} west wall", **named))
    out.append(crenellated_wall(f"{layer_id}-e-wall", cx + half + tower_radius - 1, cz - 2.5,
                                cx + half + tower_radius + wing, cz + 2.5, 1, floor, wall_height, theme,
                                name=f"{layer_id} east wall", **named))
    return out
