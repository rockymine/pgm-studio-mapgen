"""Passages built from a kit of pieces on a grid: corridors, corners, junctions, dead ends, stairs, ladder shafts and
rooms, each laid in detail from a kit's blocks and placed by a plan a network search can write.

    g = Grid(x0, y0, z0)                                  # cell (0, 0, 0)'s corner block, its floor; 5 across, 6 high
    p = Plan()
    p.link((0, 0, 0), (1, 0, 0))                          # a passage between neighbours on one level
    p.stair((2, 0, 0), "e")                               # climbs from (2, 0, 0) east into (3, 0, 1)
    p.shaft(0, 2, 0, 1)                                    # a ladder from level 0 to level 1 in column (0, 2)
    p.room("hall", 4, 0, 5, 1, 0)                          # cells (4..5, 0..1) on level 0 as one room
    p.port((0, 0, 0), "w")                                 # an opening from a cell to whatever is outside
    links = network(free, need, rng)                      # a tree through `free` reaching every cell in `need`
    lay(w, g, p, DUNGEON, rng)

**Every piece keeps three blocks of air over every place a player stands.** A cell's passage is four high, its
vault and its lights sit in the ceiling course, and a stair is a well two cells long and two levels high, so the
air over its lowest step reaches the upper ceiling. A ceiling detail that hangs into the passage would meet the
head of a player jumping in it, so none does.

**A cell is five blocks across and six high.** Its walls are the outer ring, its passage the three by three inside,
the floor the lowest course and the ceiling the sixth. Two neighbours that are not linked keep two blocks of wall
between them, and a level keeps two between its ceiling and the floor over it.

**A stair takes four cells.** It climbs from cell a along a direction into the next cell one level up, so the cell
over a and the cell under that next one are its well and nothing else may use them. It is entered at a's back wall
and left at the far cell's front wall.
"""
from dataclasses import dataclass, field

import numpy as np

from pgmvox.core.blocks import B
from pgmvox.core.orient import ladder as ladder_data, stair as stair_data, torch as torch_data

DIRS = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}
OPP = {"e": "w", "w": "e", "s": "n", "n": "s"}


def _mix(spec):
    """A weighted list [[block, weight], ...] or a single block, as (blocks, cumulative shares)."""
    if isinstance(spec, tuple) or (isinstance(spec, list) and spec and isinstance(spec[0], int)):
        return [tuple(spec)], np.array([1.0])
    blocks = [tuple(b) for b, _ in spec]
    p = np.cumsum([wt for _, wt in spec], dtype=float)
    return blocks, p / p[-1]


def _pick(mix, rng):
    blocks, p = mix
    return blocks[int(np.searchsorted(p, rng.random()))]


DUNGEON = {
    "name": "dungeon",
    "floor": [[(B.STONEBRICK, 0), 6], [(B.STONEBRICK, 2), 1.2], [(B.STONEBRICK, 1), 1], [(B.STONE, 5), 1.2]],
    "wall": [[(B.STONEBRICK, 0), 8], [(B.STONEBRICK, 1), 1.4], [(B.STONEBRICK, 2), 1.4]],
    "ceiling": [[(B.STONEBRICK, 0), 6], [(B.STONEBRICK, 2), 1]],
    "base": [[(B.STONE, 5), 3], [(B.COBBLE, 0), 1]],            # the course at the foot of a wall
    "pillar": (B.STONE, 6),
    "cap": (B.STONEBRICK, 3),
    "vault": B.STONEBRICK_STAIRS,
    "step": B.STONEBRICK_STAIRS,
    "medallion": (B.STONEBRICK, 3),
    "light": "torch",
    "glow": (B.GLOWSTONE, 0),
    "shaft_wall": [[(B.STONEBRICK, 0), 6], [(B.STONEBRICK, 1), 1]],
    "hatch": (B.STONEBRICK, 0),
    "ends": ("bars", "web", "shelf", "cauldron"),
}

MINE = {
    "name": "mine",
    "floor": [[(B.GRAVEL, 0), 3], [(B.STONE, 0), 2], [(B.STONE, 5), 1.5], [(B.COBBLE, 0), 1.5]],
    "wall": [[(B.STONE, 0), 7], [(B.STONE, 5), 1.6], [(B.COBBLE, 0), 0.8], [(B.COAL_ORE, 0), 0.5],
             [(B.IRON_ORE, 0), 0.3]],
    "ceiling": [[(B.STONE, 0), 7], [(B.STONE, 5), 1.6], [(B.COBBLE, 0), 0.6]],
    "base": None,
    "post": (B.LOG, 1),
    "beam": (B.LOG, 1),
    "step": B.COBBLE_STAIRS,
    "rails": True,
    "light": "post",
    "shaft_wall": [[(B.PLANKS, 1), 1]],
    "shaft_post": (B.LOG, 1),
    "hatch": (B.PLANKS, 1),
    "ends": ("cart", "web", "ore"),
}


@dataclass
class Grid:
    """Cell (i, j, level)'s floor block starts at (x0 + i * cell, y0 + level * height, z0 + j * cell)."""
    x0: int
    y0: int
    z0: int
    cell: int = 5
    height: int = 6

    def corner(self, i, j, l):
        return self.x0 + i * self.cell, self.y0 + l * self.height, self.z0 + j * self.cell

    def centre(self, i, j, l):
        x, y, z = self.corner(i, j, l)
        return x + self.cell // 2, y + 1, z + self.cell // 2


@dataclass
class Room:
    id: str
    i0: int
    j0: int
    i1: int
    j1: int
    level: int
    kind: str = "hall"
    tall: int = 1

    def cells(self):
        return {(i, j, self.level + k) for i in range(self.i0, self.i1 + 1) for j in range(self.j0, self.j1 + 1)
                for k in range(self.tall)}


@dataclass
class Plan:
    links: set = field(default_factory=set)
    stairs: list = field(default_factory=list)
    shafts: list = field(default_factory=list)
    rooms: list = field(default_factory=list)
    ports: list = field(default_factory=list)
    cells: set = field(default_factory=set)

    def link(self, a, b):
        assert a[2] == b[2] and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, (a, b)
        self.links.add(frozenset((tuple(a), tuple(b))))
        self.cells |= {tuple(a), tuple(b)}

    def links_of(self, links):
        for a, b in links:
            self.link(a, b)

    def stair(self, a, d):
        self.stairs.append((tuple(a), d))

    def shaft(self, i, j, l0, l1, ladder_on="n"):
        self.shafts.append((i, j, l0, l1, ladder_on))

    def room(self, id_, i0, j0, i1, j1, level, kind="hall", tall=1):
        self.rooms.append(Room(id_, min(i0, i1), min(j0, j1), max(i0, i1), max(j0, j1), level, kind, tall))

    def port(self, cell, d, kind="open"):
        self.ports.append((tuple(cell), d, kind))
        self.cells.add(tuple(cell))

    def stair_cells(self, a, d):
        """The four cells a stair takes: its foot, the well over it, the cell under its head, its head."""
        dx, dz = DIRS[d]
        i, j, l = a
        b = (i + dx, j + dz, l + 1)
        return a, (i, j, l + 1), (b[0], b[1], l), b

    def taken(self):
        """Every cell a piece of this plan stands in."""
        out = set(self.cells)
        for a, d in self.stairs:
            out |= set(self.stair_cells(a, d))
        for i, j, l0, l1, _ in self.shafts:
            out |= {(i, j, l) for l in range(l0, l1 + 1)}
        for r in self.rooms:
            out |= r.cells()
        return out


def network(free, need, rng, loops=0.0, spurs=0.0, turn=0.6, jitter=0.5):
    """Links on one level through the cells `free` [(i, j, l)], joining every cell in `need`: from one needed cell
    the network grows to the nearest needed cell it does not reach yet by the cheapest way through free cells, each
    step costing 1 plus up to `jitter` drawn at random and a turn costing `turn` more, so passages run straight and
    meet rather than winding round each other. Then a share `spurs` of the free cells beside it are taken in as dead
    ends one cell deep, and a share `loops` of the neighbour pairs both in it are linked, closing rings. Cells in
    `need` the free cells do not join are left out; check what comes back."""
    import heapq
    free = {tuple(c) for c in free}
    need = sorted({tuple(c) for c in need} & free)
    if not need:
        return set()
    cost = {c: 1 + jitter * rng.random() for c in free}
    edges, kept = set(), {need[0]}
    todo = set(need[1:])
    while todo:
        best, prev, heap = {}, {}, []
        for c in kept:
            best[(c, None)] = 0.0
            heapq.heappush(heap, (0.0, c, None))
        hit = None
        while heap:
            d, c, came = heapq.heappop(heap)
            if c in todo:
                hit = (c, came)
                break
            if d > best.get((c, came), float("inf")):
                continue
            for name, (dx, dz) in DIRS.items():
                n = (c[0] + dx, c[1] + dz, c[2])
                if n not in free:
                    continue
                nd = d + cost[n] + (turn if came is not None and came != name else 0.0)
                if nd < best.get((n, name), float("inf")):
                    best[(n, name)] = nd
                    prev[(n, name)] = (c, came)
                    heapq.heappush(heap, (nd, n, name))
        if hit is None:
            break
        state = hit
        while state in prev:
            p = prev[state]
            edges.add(frozenset((state[0], p[0])))
            kept.add(state[0])
            state = p
        kept.add(hit[0])
        todo.discard(hit[0])
    for c in sorted(kept):
        for dx, dz in DIRS.values():
            n = (c[0] + dx, c[1] + dz, c[2])
            if n in free and n not in kept and rng.random() < spurs / 4:
                edges.add(frozenset((c, n)))
                kept.add(n)
    if loops:
        for c in sorted(kept):
            for dx, dz in ((1, 0), (0, 1)):
                n = (c[0] + dx, c[1] + dz, c[2])
                e = frozenset((c, n))
                if n in kept and e not in edges and rng.random() < loops:
                    edges.add(e)
    return edges


# ---- laying -------------------------------------------------------------------------------------------------------

class _Lay:
    def __init__(self, w, g, plan, kit, rng):
        self.w, self.g, self.p, self.k, self.rng = w, g, plan, kit, rng
        self.mix = {n: _mix(kit[n]) for n in ("floor", "wall", "ceiling") if kit.get(n)}
        if kit.get("base"):
            self.mix["base"] = _mix(kit["base"])
        if kit.get("shaft_wall"):
            self.mix["shaft_wall"] = _mix(kit["shaft_wall"])
        self.air = set()                     # blocks this plan opened: nothing lined later fills them

    def put(self, x, y, z, b):
        self.w.set(x, y, z, *b)

    def pick(self, name):
        return _pick(self.mix[name], self.rng)

    def line_box(self, x0, y0, z0, x1, y1, z1):
        """Line a box's shell with floor, wall and ceiling, not touching what this plan already opened."""
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(y0, y1 + 1):
                    if (x, y, z) in self.air:
                        continue
                    edge = x in (x0, x1) or z in (z0, z1)
                    if y == y0:
                        self.put(x, y, z, self.pick("floor"))
                    elif y == y1:
                        self.put(x, y, z, self.pick("ceiling"))
                    elif edge:
                        self.put(x, y, z, self.pick("base") if y == y0 + 1 and "base" in self.mix else self.pick("wall"))

    def open_box(self, x0, y0, z0, x1, y1, z1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(y0, y1 + 1):
                    self.put(x, y, z, (B.AIR, 0))
                    self.air.add((x, y, z))


def _sides(plan, taken_by_room):
    """For every passage cell, the sides it opens to: linked neighbours, ports, a stair's ends, a shaft's openings."""
    out = {}
    for e in plan.links:
        a, b = tuple(e)
        for c, n in ((a, b), (b, a)):
            d = next(k for k, v in DIRS.items() if (c[0] + v[0], c[1] + v[1]) == (n[0], n[1]))
            out.setdefault(c, set()).add(d)
    for c, d, _ in plan.ports:
        out.setdefault(c, set()).add(d)
    return out


def lay(w, g, plan, kit, rng, decor=True):
    """Lay a plan in the world from a kit: every cell lined then opened, then each piece's detail. Returns the
    cells laid by kind: {"pass": [...], "room": {...}, "stair": [...], "shaft": [...]}."""
    L = _Lay(w, g, plan, kit, rng)
    C, H = g.cell, g.height
    room_of = {}
    for r in plan.rooms:
        for c in r.cells():
            room_of[c] = r
    stair_cells = {}
    for a, d in plan.stairs:
        for c in plan.stair_cells(a, d):
            stair_cells[c] = (a, d)
    shaft_cells = {}
    for s in plan.shafts:
        i, j, l0, l1, _ = s
        for l in range(l0, l1 + 1):
            shaft_cells[(i, j, l)] = s
    sides = _sides(plan, room_of)
    passes = sorted(c for c in plan.cells if c not in room_of and c not in stair_cells and c not in shaft_cells)
    # 1. line every piece's shell
    for c in passes:
        x, y, z = g.corner(*c)
        L.line_box(x, y, z, x + C - 1, y + H - 1, z + C - 1)
    for r in plan.rooms:
        x0, y0, z0 = g.corner(r.i0, r.j0, r.level)
        x1, _, z1 = g.corner(r.i1, r.j1, r.level)
        L.line_box(x0, y0, z0, x1 + C - 1, y0 + r.tall * H - 1, z1 + C - 1)
    for a, d in plan.stairs:
        lo = [g.corner(*c) for c in plan.stair_cells(a, d)]
        L.line_box(min(p[0] for p in lo), lo[0][1], min(p[2] for p in lo), max(p[0] for p in lo) + C - 1,
                   lo[0][1] + 2 * H - 1, max(p[2] for p in lo) + C - 1)
    for i, j, l0, l1, _ in plan.shafts:
        x, y, z = g.corner(i, j, l0)
        L.mix["_keep"] = L.mix["wall"]
        if "shaft_wall" in L.mix:
            L.mix["wall"] = L.mix["shaft_wall"]
        L.line_box(x, y, z, x + C - 1, g.corner(i, j, l1)[1] + H - 1, z + C - 1)
        L.mix["wall"] = L.mix.pop("_keep")
    # 2. open them
    for c in passes:
        x, y, z = g.corner(*c)
        L.open_box(x + 1, y + 1, z + 1, x + C - 2, y + 4, z + C - 2)
        for d in sides.get(c, ()):
            _open_side(L, g, c, d)
    for r in plan.rooms:
        x0, y0, z0 = g.corner(r.i0, r.j0, r.level)
        x1, _, z1 = g.corner(r.i1, r.j1, r.level)
        L.open_box(x0 + 1, y0 + 1, z0 + 1, x1 + C - 2, y0 + r.tall * H - 2, z1 + C - 2)
        for c in r.cells():
            for d in sides.get(c, ()):
                dx, dz = DIRS[d]
                if (c[0] + dx, c[1] + dz, c[2]) not in r.cells():
                    _open_side(L, g, c, d)
    for a, d in plan.stairs:
        _stair(L, g, a, d, plan)
    for s in plan.shafts:
        _shaft(L, g, s, sides)
    # 3. detail
    if decor:
        for c in passes:
            _detail(L, g, c, sides.get(c, set()), plan)
        for r in plan.rooms:
            _room(L, g, r)
        for c, d, kind in plan.ports:
            _port(L, g, c, d, kind)
    return {"pass": passes, "room": room_of, "stair": stair_cells, "shaft": shaft_cells}


def _frame(g, c, d):
    """(at(p, q, dy), C): the cell seen from inside looking toward side d: p across the face from 0 to C - 1,
    q into the cell from that face (0 is the face itself), dy up from the floor."""
    C = g.cell
    x, y, z = g.corner(*c)

    def at(p, q, dy):
        if d == "e":
            return x + C - 1 - q, y + dy, z + p
        if d == "w":
            return x + q, y + dy, z + C - 1 - p
        if d == "s":
            return x + C - 1 - p, y + dy, z + C - 1 - q
        return x + p, y + dy, z + q
    return at


def _open_side(L, g, c, d):
    at = _frame(g, c, d)
    for p in range(1, g.cell - 1):
        for dy in range(1, 5):
            x, y, z = at(p, 0, dy)
            L.put(x, y, z, (B.AIR, 0))
            L.air.add((x, y, z))


def _stair(L, g, a, d, plan):
    C, H = g.cell, g.height
    dx, dz = DIRS[d]
    x, y, z = g.corner(*a)
    ax_, az_ = (-dz, dx)                                    # across, to the stair's left of the climb

    def at(p, q, dy):                                       # p along the climb from a's back face, q across
        if d == "e":
            return x + p, y + dy, z + q
        if d == "w":
            return x + C - 1 - p, y + dy, z + C - 1 - q
        if d == "s":
            return x + C - 1 - q, y + dy, z + p
        return x + q, y + dy, z + C - 1 - p
    for p in range(1, 2 * C - 1):                           # the well: open from the lower floor to the upper ceiling
        for q in range(1, C - 1):
            for dy in range(1, 2 * H - 1):
                L.put(*at(p, q, dy), (B.AIR, 0))
                L.air.add(at(p, q, dy))
    for q in range(1, C - 1):                               # the two ends: in at the foot, out at the head
        for dy in range(1, 5):
            for p, oy in ((0, 0), (2 * C - 1, H)):
                L.put(*at(p, q, dy + oy), (B.AIR, 0))
                L.air.add(at(p, q, dy + oy))
    for p in range(1, 2 * C - 1):
        k = min(max(p - 1, 0), H)                           # the step's top over the lower floor
        top = H if p >= H + 1 else k
        for q in range(1, C - 1):
            for dy in range(1, top):
                L.put(*at(p, q, dy), L.pick("floor") if dy == top - 1 else L.pick("wall"))
                L.air.discard(at(p, q, dy))
            if 1 <= k < H and p < H + 1:
                L.put(*at(p, q, top), (L.k["step"], stair_data(d)))
                L.air.discard(at(p, q, top))
            elif top == H:
                L.put(*at(p, q, H), L.pick("floor"))
                L.air.discard(at(p, q, H))
    if L.k.get("light") == "torch":                         # a light on one side wall low and one high
        for p, dy in ((1, 3), (2 * C - 2, H + 3)):
            tx, ty, tz = at(p, 1, dy)
            wx, _, wz = at(p, 0, dy)
            L.put(tx, ty, tz, (B.TORCH, torch_data(_toward(tx, tz, wx, wz))))


def _toward(x, z, wx, wz):
    if wx > x:
        return "e"
    if wx < x:
        return "w"
    return "s" if wz > z else "n"


def _shaft(L, g, s, sides):
    i, j, l0, l1, on = s
    C, H = g.cell, g.height
    x, y0, z = g.corner(i, j, l0)
    top = g.corner(i, j, l1)[1]
    L.open_box(x + 1, y0 + 1, z + 1, x + C - 2, top + 4, z + C - 2)
    dx, dz = DIRS[on]
    lx, lz = x + C // 2 + dx * (C // 2 - 1), z + C // 2 + dz * (C // 2 - 1)
    for l in range(l0, l1 + 1):
        by = g.corner(i, j, l)[1]
        if l > l0:                                          # a hatch floor at each level, open over the ladder
            for u in range(1, C - 1):
                for v in range(1, C - 1):
                    if (x + u, z + v) != (lx, lz):
                        L.put(x + u, by, z + v, L.k["hatch"])
                        L.air.discard((x + u, by, z + v))
        for d in sides.get((i, j, l), ()):
            _open_side(L, g, (i, j, l), d)
    if "shaft_post" in L.k:
        for u, v in ((0, 0), (0, C - 1), (C - 1, 0), (C - 1, C - 1)):
            for yy in range(y0 + 1, top + H - 1):
                L.put(x + u, yy, z + v, L.k["shaft_post"])
    for yy in range(y0 + 1, top + 3):
        L.put(lx, yy, lz, (B.LADDER, ladder_data(on)))
    if L.k.get("light") == "torch":
        for l in range(l0, l1 + 1):
            by = g.corner(i, j, l)[1]
            tx, tz = x + C // 2 - dx * (C // 2 - 1), z + C // 2 - dz * (C // 2 - 1)
            if L.w.id(tx, by + 3, tz) == B.AIR and L.w.id(tx - dx, by + 3, tz - dz) not in (B.AIR,):
                L.put(tx, by + 3, tz, (B.TORCH, torch_data(OPP[on])))


def _detail(L, g, c, open_to, plan):
    """A passage cell's own detail by its shape: the vault in its ceiling course, lights, a medallion where three
    or four ways meet, and something at the end of a dead end."""
    C = g.cell
    x, y, z = g.corner(*c)
    along_x = open_to <= {"e", "w"} and open_to
    along_z = open_to <= {"n", "s"} and open_to
    k = L.k
    mid = C // 2
    if k["name"] == "dungeon":
        if along_x or along_z:                              # a straight run: chamfers in the ceiling course
            for side in (1, C - 2):
                for t in range(1, C - 1):
                    px, pz = (x + t, z + side) if along_x else (x + side, z + t)
                    rise = ("n" if side == 1 else "s") if along_x else ("w" if side == 1 else "e")
                    L.put(px, y + 5, pz, (k["vault"], stair_data(rise, upside_down=True)))
            for t in range(1, C - 1):
                px, pz = (x + t, z + mid) if along_x else (x + mid, z + t)
                L.put(px, y + 5, pz, (B.AIR, 0))
            if (c[0] + c[1]) % 2 == 0 and (x + mid, y + 6, z + mid) not in L.air:
                L.put(x + mid, y + 6, z + mid, k["glow"])
        elif len(open_to) >= 3:
            L.put(x + mid, y, z + mid, k["medallion"])
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                L.put(x + mid + dx, y, z + mid + dz, k["pillar"])
            L.put(x + mid, y + 5, z + mid, k["glow"])
        elif len(open_to) == 2:                            # a corner: a pillar in the corner it turns round
            closed = [d for d in DIRS if d not in open_to]
            px = x + (1 if "w" in closed else C - 2)
            pz = z + (1 if "n" in closed else C - 2)
            for dy in range(1, 5):
                L.put(px, y + dy, pz, k["pillar"] if dy < 4 else k["cap"])
            L.put(x + mid, y + 5, z + mid, k["glow"])
        if len(open_to) == 1:
            _dead_end(L, g, c, next(iter(open_to)))
        elif (c[0] * 3 + c[1]) % 4 == 1 and (along_x or along_z):   # a torch now and then on a wall
            if along_x:
                L.put(x + mid, y + 3, z + 1, (B.TORCH, torch_data("n")))
            else:
                L.put(x + 1, y + 3, z + mid, (B.TORCH, torch_data("w")))
    else:                                                   # the mine: a timber set in the walls, rails on the level
        if along_x or along_z:
            for t in range(0, C):
                px, pz = (x + mid, z + t) if along_x else (x + t, z + mid)
                axis = 8 if along_x else 4                  # the beam lies across the run
                L.put(px, y + 5, pz, (k["beam"][0], (k["beam"][1] & 3) | axis))
            for side in (0, C - 1):
                for dy in range(1, 5):
                    px, pz = (x + mid, z + side) if along_x else (x + side, z + mid)
                    L.put(px, y + dy, pz, k["post"])
            px, pz = (x + mid, z + 1) if along_x else (x + 1, z + mid)
            if (c[0] + c[1]) % 2 == 0:
                L.put(px, y + 3, pz, (B.TORCH, torch_data("n" if along_x else "w")))
            if k.get("rails"):
                for t in range(1, C - 1):
                    px, pz = (x + t, z + mid) if along_x else (x + mid, z + t)
                    L.put(px, y + 1, pz, (B.RAIL, 1 if along_x else 0))
        if len(open_to) == 1:
            _dead_end(L, g, c, next(iter(open_to)))


def _dead_end(L, g, c, d):
    """The far wall of a dead end, dressed by the kit's choices."""
    at = _frame(g, c, OPP[d])
    kind = L.k["ends"][int(L.rng.integers(len(L.k["ends"])))]
    C = g.cell
    if kind == "bars":                                      # a cell behind bars in the rock
        for p in range(1, C - 1):
            for dy in range(1, 4):
                L.put(*at(p, 0, dy), (B.IRON_BARS, 0))
                L.put(*at(p, -1, dy), (B.AIR, 0))
            L.put(*at(p, -1, 0), L.pick("floor"))
            L.put(*at(p, -1, 4), L.pick("ceiling"))
        L.put(*at(C // 2, -1, 1), (B.SKULL, 1))
    elif kind == "web":
        for p in (1, C - 2):
            L.put(*at(p, 1, 4), (B.COBWEB, 0))
        L.put(*at(C // 2, 1, 1), (B.COBWEB, 0))
    elif kind == "shelf":
        for p in range(1, C - 1):
            for dy in (1, 2):
                L.put(*at(p, 0, dy), (B.BOOKSHELF, 0))
        L.put(*at(C // 2, 1, 3), (B.TORCH, torch_data(OPP[d])))
    elif kind == "cauldron":
        L.put(*at(C // 2, 1, 1), (B.CAULDRON, 3))
        L.put(*at(C // 2, 0, 3), (B.STONEBRICK, 3))
    elif kind == "cart":
        L.put(*at(C // 2, 1, 1), (B.RAIL, 0 if d in "ns" else 1))
        L.put(*at(C // 2, 0, 1), (B.PLANKS, 1))
        L.put(*at(C // 2, 0, 2), (B.FENCE, 0))
    elif kind == "ore":
        for p in range(1, C - 1):
            L.put(*at(p, 0, 1 + int(L.rng.integers(3))), (B.IRON_ORE, 0) if L.rng.random() < 0.5 else (B.COAL_ORE, 0))


def _room(L, g, r):
    C, H = g.cell, g.height
    k = L.k
    x0, y0, z0 = g.corner(r.i0, r.j0, r.level)
    x1, _, z1 = g.corner(r.i1, r.j1, r.level)
    x1, z1 = x1 + C - 1, z1 + C - 1
    top = y0 + r.tall * H - 1
    inner = [(x, z) for x in range(x0 + 1, x1) for z in range(z0 + 1, z1)]
    ring = {(x, z) for x in range(x0, x1 + 1) for z in (z0, z1)} | {(x, z) for z in range(z0, z1 + 1) for x in (x0, x1)}
    if r.kind in ("hall", "vault", "crypt", "library", "prison"):
        for i in range(r.i0 + 1, r.i1 + 1):                 # pillars where four cells meet inside the room
            for j in range(r.j0 + 1, r.j1 + 1):
                px, _, pz = g.corner(i, j, r.level)
                for ox in (-1, 0):
                    for oz in (-1, 0):
                        for yy in range(y0 + 1, top):
                            L.put(px + ox, yy, pz + oz, k.get("pillar", (B.LOG, 1)) if yy < top - 1
                                  else k.get("cap", (B.LOG, 1)))
    if "glow" in k:
        for i in range(r.i0, r.i1 + 1):
            for j in range(r.j0, r.j1 + 1):
                cx, _, cz = g.corner(i, j, r.level)
                L.put(cx + C // 2, top, cz + C // 2, k["glow"])
    if r.kind == "library":
        for x, z in inner:
            if (x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1)) and not _by_door(L, x, y0, z, ring):
                for yy in range(y0 + 1, min(y0 + 4, top)):
                    L.put(x, yy, z, (B.BOOKSHELF, 0))
    elif r.kind == "prison":
        for x in range(x0 + 1, x1):
            if not _by_door(L, x, y0, z0 + 1, ring) and not _by_door(L, x, y0, z0 + 2, ring):
                for yy in range(y0 + 1, y0 + 4):
                    L.put(x, yy, z0 + 2, (B.IRON_BARS, 0))
    elif r.kind == "crypt":
        for i in range(r.i0, r.i1 + 1):
            for j in range(r.j0, r.j1 + 1):
                cx, _, cz = g.corner(i, j, r.level)
                L.put(cx + 2, y0 + 1, cz + 1, (B.STONEBRICK, 3))       # a tomb a block high: who climbs it
                L.put(cx + 2, y0 + 1, cz + 2, (B.STONEBRICK, 0))       # keeps four of air over him


def _by_door(L, x, y0, z, ring):
    """This floor cell inside a room stands beside an opening in the room's wall ring."""
    return any((x + dx, z + dz) in ring and L.w.id(x + dx, y0 + 1, z + dz) == B.AIR
               for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def _port(L, g, c, d, kind):
    """An opening to outside: open, a window of bars, or an arch framed in the kit's cap block."""
    at = _frame(g, c, d)
    C = g.cell
    if kind == "bars":
        for p in range(1, C - 1):
            for dy in range(1, 5):
                L.put(*at(p, 0, dy), (B.IRON_BARS, 0))
    elif kind == "arch" and "cap" in L.k:                   # jambs and a lintel, all outside the opening
        for dy in range(1, 6):
            for p in (0, C - 1):
                L.put(*at(p, 0, dy), L.k["cap"] if dy in (1, 5) else L.k["pillar"])
        for p in range(1, C - 1):
            L.put(*at(p, 0, 5), L.k["cap"] if p == C // 2 else (L.k["vault"], stair_data(_side_toward(
                d, -1 if p < C // 2 else 1), upside_down=True)))


def _side_toward(d, s):
    """The direction across a face looking along d: s -1 to its first edge (p 0), +1 to its last."""
    across = {"e": "s", "w": "n", "s": "w", "n": "e"}[d]
    return across if s > 0 else OPP[across]
