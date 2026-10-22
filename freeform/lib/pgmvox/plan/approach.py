"""A goal's approach as the studio's generator builds one: rectangles of corridor cells, each named for what it does,
ending in the room the goal stands in; read back from its cells alone; walled where a defence holds it.

    a = emit("donut")                         # the template, its parts in order, the room last
    a.cells(), a.room, a.entry                # (i, j) corridor cells; the room's cells; the docking cells
    classify(a.cells(), a.room)               # "donut", read off the geometry, not the name
    doors(a)                                  # 1 or 2: the ways in from the host, edge-disjoint
    walls(a)                                  # the seams a bedrock wall stands on, one per way in
    a.scaled(5)                               # the same in blocks, a corridor five wide

**The approach is the ground walked from a host to its room, and its form is what that walk does.** The forms are
the studio's (`pgm-studio/docs/generator/model.md` §4.6): I, L, Z, scythe, clamp, U, H and donut, an escalation
in which each step adds one feature. A cell is one corridor wide; the host lies beyond the mouth, the edge the
`entry` part docks on.

| Form | Template | Reads as |
|---|---|---|
| I | entry, room | a lane caps the room |
| L | entry, run, room | one bend |
| Z | entry, bar, room-run, room | a staircase of two opposing bends |
| scythe | entry, entry-run, bar, room-run, room | a fold round an open bay beside the room |
| clamp | entry, entry, room | the room bridges two bars: take it away and the ground splits |
| U | bar, entry, entry, room | two legs meet a crossbar, the room flush on it |
| H | bar, entry, entry, room-run, room | the same with the room lifted on a stub |
| donut | entry, entry-bar, leg, leg, room-bar, room | ground ringing a void: two ways in |

**A part is a template position, not a property of the rectangle.** Every form emits a stable piece count in a
stable order, so "the entry" is a name a rule can hold to.

**The form is read back from the cells, strongest signal first,** as `ShapeClassifier` reads it: no ground at
the room is isolated, an enclosed void is a donut, a room that is a cut cell is a clamp, and otherwise the bends
of the outline decide, a branch telling U and H from the scythe and Z.

**A defence wall stands on a seam a way in must cross, with void past both its ends** (§5.14). A wall with
ground running past an end is walked round rather than crossed. It stands two to four cells before the room,
nearest three (ten to twenty blocks at a corridor of five, nearest fifteen); an approach with two ways in takes
a pair, each closing one.
"""
from dataclasses import dataclass, field

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass
class Part:
    name: str
    i0: int
    j0: int
    i1: int
    j1: int

    def cells(self):
        return {(i, j) for i in range(min(self.i0, self.i1), max(self.i0, self.i1) + 1)
                for j in range(min(self.j0, self.j1), max(self.j0, self.j1) + 1)}


@dataclass
class Approach:
    form: str
    parts: list
    mouth: str                         # the side the host is on: "n" (j < 0), "s", "w" (i < 0) or "e"
    knobs: dict = field(default_factory=dict)

    def cells(self):
        out = set()
        for p in self.parts:
            out |= p.cells()
        return out

    @property
    def room(self):
        return self.parts[-1].cells()

    @property
    def entry(self):
        """The cells that dock on the host: the entry parts' cells on the mouth's edge."""
        cells = set().union(*(p.cells() for p in self.parts if p.name == "entry"))
        edge = {"n": min, "w": min, "s": max, "e": max}[self.mouth]
        axis = 1 if self.mouth in "ns" else 0
        at = edge(c[axis] for c in cells)
        return {c for c in cells if c[axis] == at}

    def host(self):
        """The cells just past the mouth, where the host stands."""
        d = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[self.mouth]
        return {(i + d[0], j + d[1]) for i, j in self.entry}

    def part_of(self, cell):
        for p in reversed(self.parts):
            if cell in p.cells():
                return p.name
        return None

    def scaled(self, n):
        """The parts in blocks, each corridor cell n blocks square: [(name, x0, z0, x1, z1)]."""
        return [(p.name, min(p.i0, p.i1) * n, min(p.j0, p.j1) * n, (max(p.i0, p.i1) + 1) * n - 1,
                 (max(p.j0, p.j1) + 1) * n - 1) for p in self.parts]


def _p(name, i0, j0, i1=None, j1=None):
    return Part(name, i0, j0, i0 if i1 is None else i1, j0 if j1 is None else j1)


def emit(form, depth=2, reach=2, mouth=None):
    """The template for `form`, its parts in order and the room last. `depth` is how far the approach runs from
    the mouth, `reach` how far across it; both in cells, both the studio's `run` knobs."""
    d, r = max(depth, 1), max(reach, 1)
    if form == "I":
        return Approach("I", [_p("entry", 0, 0, 0, d), _p("room", 0, d + 1)], mouth or "n")
    if form == "L":
        return Approach("L", [_p("entry", 0, 0, 0, d), _p("run", 1, d, r, d), _p("room", r + 1, d)], mouth or "n")
    if form == "Z":
        return Approach("Z", [_p("entry", 0, 0, 0, d - 1), _p("bar", 0, d, r, d), _p("room-run", r, d + 1, r, 2 * d),
                              _p("room", r, 2 * d + 1)], mouth or "n")
    if form == "scythe":
        w = r + 2
        return Approach("scythe", [_p("entry", 0, 0), _p("entry-run", 1, 0, 1, d + 1), _p("bar", 2, d + 1, w, d + 1),
                                   _p("room-run", w, 1, w, d), _p("room", w, 0)], mouth or "n")
    if form == "clamp":
        return Approach("clamp", [_p("entry", 0, 0, 0, d), _p("entry", 2, 0, 2, d), _p("room", 1, 0)], mouth or "s")
    if form == "U":
        w = 2 * r
        return Approach("U", [_p("bar", 0, 1, w, 1), _p("entry", 0, 2, 0, d + 1), _p("entry", w, 2, w, d + 1),
                              _p("room", r, 0)], mouth or "s")
    if form == "H":
        w = 2 * r
        return Approach("H", [_p("bar", 0, 2, w, 2), _p("entry", 0, 3, 0, d + 2), _p("entry", w, 3, w, d + 2),
                              _p("room-run", r, 1), _p("room", r, 0)], mouth or "s")
    if form == "donut":
        w, h = r + 2, d + 1
        return Approach("donut", [_p("entry", 0, 0), _p("entry-bar", 1, 0, w, 0), _p("leg", 1, 1, 1, h - 1),
                                  _p("leg", w, 1, w, h - 1), _p("room-bar", 1, h, w, h), _p("room", w + 1, h)],
                        mouth or "w")
    raise ValueError(f"no form {form!r}")


FORMS = ("I", "L", "Z", "scythe", "clamp", "U", "H", "donut")


# ---- reading a form back ------------------------------------------------------------------------------------------

def _neighbours(c, cells):
    return [(c[0] + a, c[1] + b) for a, b in DIRS if (c[0] + a, c[1] + b) in cells]


def _connected(cells):
    cells = set(cells)
    if not cells:
        return True
    start = next(iter(cells))
    seen, todo = {start}, [start]
    while todo:
        for n in _neighbours(todo.pop(), cells):
            if n not in seen:
                seen.add(n)
                todo.append(n)
    return seen == cells


def holes(cells):
    """Empty cells the ground encloses: not reached from outside its bounding box by stepping through empty cells."""
    i0, i1 = min(c[0] for c in cells) - 1, max(c[0] for c in cells) + 1
    j0, j1 = min(c[1] for c in cells) - 1, max(c[1] for c in cells) + 1
    out = {(i0, j0)}
    todo = [(i0, j0)]
    while todo:
        c = todo.pop()
        for a, b in DIRS:
            n = (c[0] + a, c[1] + b)
            if i0 <= n[0] <= i1 and j0 <= n[1] <= j1 and n not in cells and n not in out:
                out.add(n)
                todo.append(n)
    return {(i, j) for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)} - cells - out


def bends(cells):
    """Reflex corners of the outline: grid vertices with three of the four cells round them filled."""
    vs = {(i + a, j + b) for i, j in cells for a in (0, 1) for b in (0, 1)}
    return sum(1 for vi, vj in vs
               if sum((vi - a, vj - b) in cells for a in (0, 1) for b in (0, 1)) == 3)


def classify(cells, room):
    """The form of the ground `cells` ending in `room`, read off the geometry alone."""
    cells, room = set(cells), set(room)
    ground = cells - room
    if not any(n in ground for c in room for n in _neighbours(c, cells | {c})):
        return "isolated"
    if holes(cells):
        return "donut"
    if not _connected(ground):
        return "clamp"
    b = bends(ground)
    if b == 0:
        return "I"
    if b == 1:
        return "L"
    i0, i1 = min(c[0] for c in ground), max(c[0] for c in ground)
    j0, j1 = min(c[1] for c in ground), max(c[1] for c in ground)
    rmid = (sum(c[0] for c in room) / len(room), sum(c[1] for c in room) / len(room))
    edges = {"w": [(i0, j) for j in range(j0, j1 + 1)], "e": [(i1, j) for j in range(j0, j1 + 1)],
             "n": [(i, j0) for i in range(i0, i1 + 1)], "s": [(i, j1) for i in range(i0, i1 + 1)]}
    room_edge = min(edges, key=lambda k: min(abs(rmid[0] - c[0]) + abs(rmid[1] - c[1]) for c in edges[k]))
    branch = False
    for k, line in edges.items():
        if k == room_edge:
            continue
        runs, inside = 0, False
        for c in line:
            if c in ground and not inside:
                runs += 1
            inside = c in ground
        branch = branch or runs >= 2
    if branch:
        touching = [n for c in room for n in _neighbours(c, ground)]
        flush = any(len(_neighbours(n, ground)) >= 2 for n in touching)
        return "U" if flush else "H"
    rows = {}
    for i, j in ground:
        rows.setdefault(j, []).append(i)
    cols = {}
    for i, j in ground:
        cols.setdefault(i, []).append(j)

    def split(v):
        v = sorted(v)
        return any(b - a > 1 for a, b in zip(v, v[1:]))
    if any(split(v) for v in rows.values()) or any(split(v) for v in cols.values()):
        return "scythe"
    return "Z"


# ---- the ways in, and the walls across them -----------------------------------------------------------------------

def _edges(cells):
    return {frozenset((c, n)) for c in cells for n in _neighbours(c, cells)}


def _reaches(cells, cut, sources, targets):
    seen, todo = set(sources) & cells, list(set(sources) & cells)
    while todo:
        c = todo.pop()
        if c in targets:
            return True
        for n in _neighbours(c, cells):
            if n not in seen and frozenset((c, n)) not in cut:
                seen.add(n)
                todo.append(n)
    return False


def _regions(cells):
    out, seen = 0, set()
    for c in cells:
        if c in seen:
            continue
        out += 1
        seen.add(c)
        todo = [c]
        while todo:
            for n in _neighbours(todo.pop(), cells):
                if n not in seen:
                    seen.add(n)
                    todo.append(n)
    return out


def doors(a):
    """How many ways in the approach has (match-flow §3.1): one, and one more for every void the ways go round,
    counted with the host's edge drawn across the mouth, so legs that both stand on the host close a void with it."""
    host = a.host()
    axis = 0 if a.mouth in "ns" else 1
    lo, hi = min(c[axis] for c in host), max(c[axis] for c in host)
    other = next(iter(host))[1 - axis]
    line = {(v, other) if axis == 0 else (other, v) for v in range(lo, hi + 1)}
    return 1 + _regions(holes(a.cells() | line))


def _depth_from_room(cells, room):
    dist = {c: 0 for c in room}
    todo = list(room)
    while todo:
        nxt = []
        for c in todo:
            for n in _neighbours(c, cells):
                if n not in dist:
                    dist[n] = dist[c] + 1
                    nxt.append(n)
        todo = nxt
    return dist


def seams(a):
    """Every seam a wall may stand on: a step between two cells of a corridor one cell wide, with no ground beside
    either cell on either side of the step, so the wall's ends look onto void; never a step into the room."""
    cells, room = a.cells(), a.room
    out = []
    for e in _edges(cells):
        p, q = tuple(e)
        if p in room or q in room:
            continue
        di, dj = q[0] - p[0], q[1] - p[1]
        side = (dj, di)                                            # across the step
        ends = [(c[0] + s * side[0], c[1] + s * side[1]) for c in (p, q) for s in (1, -1)]
        if not any(x in cells for x in ends):
            out.append(e)
    return out


def walls(a, near=3, window=(2, 4)):
    """The defence walls: one seam closing the only way in, or for an approach with two ways in a pair that closes
    both while neither does alone; standing `window` cells before the room, as near `near` as there is a seam."""
    cells, room = a.cells(), a.room
    depth = _depth_from_room(cells, room)
    candidates = seams(a)

    def far(e):
        return max(depth.get(c, 0) for c in e)

    def score(es):
        return sum(abs(far(e) - near) for e in es) + sum(0 if window[0] <= far(e) <= window[1] else 10 for e in es)
    singles = [e for e in candidates if not _reaches(cells, {e}, a.entry, room)]
    if doors(a) <= 1 and singles:
        return [min(singles, key=lambda e: score([e]))]
    pairs = [(e, f) for k, e in enumerate(candidates) for f in candidates[k + 1:]
             if e not in singles and f not in singles and not _reaches(cells, {e, f}, a.entry, room)]
    legs = [(e, f) for e, f in pairs if all(a.part_of(c) == "leg" for c in e | f)]
    if legs:                                                   # a ring is held across its two legs first
        return list(min(legs, key=score))
    if pairs:
        return list(min(pairs, key=score))
    return [min(singles, key=lambda e: score([e]))] if singles else []


def funnel(a, cell=5):
    """The narrowest frontage between the host and the room, in blocks: the door count times a corridor's width."""
    return doors(a) * cell


def describe(a):
    """One line per approach: its form as emitted and as read back, its ways in, its walls, its parts."""
    w = walls(a)
    return (f"{a.form:7} reads {classify(a.cells(), a.room):7} doors {doors(a)}  walls "
            f"{[sorted(tuple(e)) for e in w]}  parts {' · '.join(p.name for p in a.parts)}")


def ascii(a):
    """The approach drawn as the studio draws it: t ground, w the room, h the host, # a cell a wall stands beside."""
    cells, room, host = a.cells(), a.room, a.host()
    wallcells = {c for e in walls(a) for c in e}
    allc = cells | host
    i0, i1 = min(c[0] for c in allc), max(c[0] for c in allc)
    j0, j1 = min(c[1] for c in allc), max(c[1] for c in allc)
    rows = []
    for j in range(j0, j1 + 1):
        row = ""
        for i in range(i0, i1 + 1):
            c = (i, j)
            row += "w" if c in room else "#" if c in wallcells else "t" if c in cells else "h" if c in host else "."
        rows.append(row)
    return "\n".join(rows)
