"""A bunker drawn from a board the studio composed: the generator's layout under a roof, its land standing in the
void as islands, its holes turned to pillars, the world outside it turned to rock.

    c = bunker.load("composed.json")              # pgmvox/data/compose_board.cs wrote it
    b = bunker.draw(c, gap=2, moat=2)
    b.kind[i, j]                                  # VOID, ISLAND, ROCK or PILLAR at cell (b.x0 + i, b.z0 + j)
    b.rooms, b.spawns, b.walls, b.cuts, b.islands

**The generator's board is read as a bunker by four exchanges.** Its land is an island's deck over the void. A build
region is void, crossed by bridging under the roof. An enclosed void, the hole a ring or a donut leaves, is a pillar
of rock from the floor to the roof: it stops sight and movement the way the hole stopped walking. And the world
outside the board is rock, the bunker's walls, but for a moat of void `moat` cells wide along every shore.

**The generator draws few islands, and a bunker lives from its gaps, so the board is cut.** The generator's land is
one mass a team, joined from the spawn to every wool; in the concept every floor is an island and every way between
two is a bridge. The cut is the generator's own isolation cut (model.md §6.2): a box of kind `cut` (a wool's approach,
the frontline) is cut from every other box by `gap` cells of void on its own side, unless that leaves it fewer than
`least` cells.

**A wool room is a block of rock with its seal on the void.** The room's cells are rock, and the land in front of it
is cut back by `gap` cells, so the seal's face looks onto void and the room is reached by bridging to it. The room's
`face` is the way from the room to the land it was entered from. A spawn room is rock too, opening onto its land.

**A defence wall is rock from the floor to the roof.** The plan's walls (model.md §5.14) stand on a seam between two
pieces with void past both ends; under a roof a player goes round one only by bridging over that void.
"""
import json
from dataclasses import dataclass, field

import numpy as np

VOID, ISLAND, ROCK, PILLAR = 0, 1, 2, 3
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass
class Composed:
    """A composed board read back: cells in the composer's own cell coordinates."""
    cell: int
    filled: dict                     # (x, z) -> (piece id, image k)
    build: set
    voids: list                      # [(cells, class)]
    rooms: list                      # [dict(wool, k, cells, marker)]
    box_of: dict                     # piece id -> (box id, box kind)
    walls: list                      # [(piece a, piece b)]
    spawn_pieces: set
    room_pieces: set
    symmetry: str
    raw: dict = field(repr=False, default=None)


def load(path):
    d = json.load(open(path))
    filled = {(x, z): (o, k) for (x, z, k), o in zip(d["filled"], d["owners"])}
    plan = d["plan"]
    box_of = {}
    for b in plan.get("boxes", []):
        for m in b.get("members") or []:
            box_of[m] = (b["id"], b["kind"])
    rooms = [dict(wool=r["wool"], k=r["k"], cells={tuple(c) for c in r["cells"]}, marker=(r["mx"], r["mz"]))
             for r in d["woolRooms"]]
    return Composed(d["cell"], filled, {tuple(c) for c in d["build"]},
                    [({tuple(c) for c in v["cells"]}, v["cls"]) for v in d["voids"]], rooms, box_of,
                    [(w["a"], w["b"]) for w in plan.get("walls", [])], set(d["spawnOwners"]),
                    {p["id"] for p in plan["pieces"] if p["role"] == "wool-room"},
                    plan["globals"]["symmetry"], d)


@dataclass
class Bunker:
    x0: int
    z0: int
    kind: np.ndarray
    cell: int
    rooms: list = field(default_factory=list)      # [dict(cells, face, k, wool)]
    spawns: list = field(default_factory=list)     # [dict(cells, face, k)]
    walls: list = field(default_factory=list)      # [(cell a, cell b)]: a seam a wall stands on
    cuts: list = field(default_factory=list)       # [(box id, cells cut)]
    islands: list = field(default_factory=list)    # [set of cells]
    dropped: int = 0

    def at(self, c):
        i, j = c[0] - self.x0, c[1] - self.z0
        if 0 <= i < self.kind.shape[0] and 0 <= j < self.kind.shape[1]:
            return int(self.kind[i, j])
        return ROCK

    def put(self, c, k):
        self.kind[c[0] - self.x0, c[1] - self.z0] = k

    def cells(self, k):
        return {(int(i) + self.x0, int(j) + self.z0) for i, j in np.argwhere(self.kind == k)}


def _near(cells, other, r):
    """The cells of `cells` within `r` steps (Manhattan) of any cell of `other`."""
    out = set()
    for (x, z) in cells:
        if any((x + dx, z + dz) in other for dx in range(-r, r + 1) for dz in range(-r + abs(dx), r - abs(dx) + 1)):
            out.add((x, z))
    return out


def _components(cells):
    left, out = set(cells), []
    while left:
        seed = left.pop()
        comp, todo = {seed}, [seed]
        while todo:
            x, z = todo.pop()
            for dx, dz in DIRS:
                n = (x + dx, z + dz)
                if n in left:
                    left.remove(n)
                    comp.add(n)
                    todo.append(n)
        out.append(comp)
    return out


def _face(cells, land):
    """The way out of a room onto the land it touches most."""
    best, n = None, -1
    for d in DIRS:
        m = sum(1 for (x, z) in cells if (x + d[0], z + d[1]) in land and (x + d[0], z + d[1]) not in cells)
        if m > n:
            best, n = d, m
    return best


def draw(c, gap=2, moat=2, cut=("wool", "frontline"), least=12, smallest=6):
    rooms = [r for r in c.rooms]
    room_cells = set().union(*[r["cells"] for r in rooms]) if rooms else set()
    spawn_cells = {p for p, (o, k) in c.filled.items() if o in c.spawn_pieces}
    land = {p for p, (o, k) in c.filled.items() if p not in room_cells and p not in spawn_cells}
    pillars = set().union(*[v for v, _ in c.voids]) if c.voids else set()
    every = set(c.filled) | c.build | pillars
    xs, zs = [p[0] for p in every], [p[1] for p in every]
    pad = moat + 3
    x0, z0 = min(xs) - pad, min(zs) - pad
    kind = np.full((max(xs) - x0 + pad + 1, max(zs) - z0 + pad + 1), ROCK, np.uint8)
    b = Bunker(x0, z0, kind, c.cell)
    open_ = land | c.build
    near_open = _near({(i + x0, j + z0) for i, j in np.ndindex(*kind.shape)}, open_, moat)
    for p in near_open:
        b.put(p, VOID)
    for p in c.build:
        b.put(p, VOID)
    for p in land:                               # a stepping stone stands in its build region
        b.put(p, ISLAND)
    for p in pillars:
        b.put(p, PILLAR)
    # the isolation cuts: a wool's approach and the frontline, each cut from the boxes it touches
    box = {p: c.box_of.get(c.filled[p][0], ("?", "?")) for p in land}
    for bid, bkind in sorted({v for v in box.values()}):
        if bkind not in cut:
            continue
        for k in sorted({c.filled[p][1] for p in land}):
            mine = {p for p in land if box[p] == (bid, bkind) and c.filled[p][1] == k}
            others = {p for p in land if box[p][0] != bid and c.filled[p][1] == k}
            gone = _near(mine, others, gap)
            if gone and len(mine) - len(gone) >= least:
                for p in gone:
                    b.put(p, VOID)
                b.cuts.append((f"{bid}/{k}", len(gone)))
    # the wool rooms: rock, their seal's face on void cut back from the land in front of them
    for r in rooms:
        face = _face(r["cells"], land)
        for p in r["cells"]:
            b.put(p, ROCK)
        front = _near({p for p in land if b.at(p) == ISLAND}, r["cells"], gap)
        for p in front:
            b.put(p, VOID)
        b.rooms.append(dict(cells=r["cells"], face=face, k=r["k"], wool=r["wool"]))
    for k in sorted({c.filled[p][1] for p in spawn_cells}):
        cells = {p for p in spawn_cells if c.filled[p][1] == k and c.filled[p][0] in c.room_pieces | c.spawn_pieces}
        for p in cells:
            b.put(p, ROCK)
        b.spawns.append(dict(cells=cells, face=_face(cells, land), k=k))
    # the defence walls, on seams whose two sides are both still floor
    piece_cells = {}
    for p, (o, k) in c.filled.items():
        piece_cells.setdefault(o, set()).add(p)
    for a, bb in c.walls:
        for p in piece_cells.get(a, ()):
            for d in DIRS:
                q = (p[0] + d[0], p[1] + d[1])
                if q in piece_cells.get(bb, ()) and b.at(p) == ISLAND and b.at(q) == ISLAND:
                    b.walls.append((p, q))
    # islands too small to stand a fight on go to the void
    for comp in _components(b.cells(ISLAND)):
        if len(comp) < smallest:
            for p in comp:
                b.put(p, VOID)
            b.dropped += len(comp)
        else:
            b.islands.append(comp)
    return b


def ascii(b):
    """The bunker in text, a character a cell: '#' rock, 'P' pillar, '.' island, ' ' void, 'R' a wool room, 'S' a
    spawn, '|' a cell a wall stands on."""
    rooms = set().union(*[r["cells"] for r in b.rooms]) if b.rooms else set()
    spawns = set().union(*[s["cells"] for s in b.spawns]) if b.spawns else set()
    walls = {p for p, _ in b.walls}
    rows = []
    for j in range(b.kind.shape[1]):
        row = ""
        for i in range(b.kind.shape[0]):
            p = (i + b.x0, j + b.z0)
            row += "R" if p in rooms else "S" if p in spawns else "|" if p in walls else \
                {VOID: " ", ISLAND: ".", ROCK: "#", PILLAR: "P"}[int(b.kind[i, j])]
        rows.append(row.rstrip())
    return "\n".join(rows)
