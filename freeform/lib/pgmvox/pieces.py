"""A course plan: a board made of pieces in order, and the links a player takes from one to the next.

    C = Course(Symmetry("mirror_x"))
    C.add("the bell court", box(-8, 8, 0, 16), 240, spawn=True)          # crosses the axis: one, in the middle
    C.add("the torii beams", box(-13, -9, 22, 30), 233)                  # off it: this and its mirror image
    C.add("the great pagoda", box(-6, 6, 51, 65), 198, water=box(-3, 3, 52, 57))
    for row in C.audit():
        print(row)                       # each link: the gap, the drop, how it is cleared, the damage, lethal

A raster plan is a board seen as columns; a course is a board seen as a sequence, as a water drop, a parkour run
or a wool run is played. Each `add` is one step of the course. A piece off the symmetry axis brings its image with
it, marked "image"; one whose image overlaps it is the middle. A piece links to every piece of the next step on
its own side or in the middle.

**Every link is judged with the 1.8 tick model** (`move`). Dropping, the fall carries a player out from the edge
by an amount that depends on how they left it: stepping off, running off, or sprint-jumping. Level or climbing,
only a sprint jump clears a gap. The audit names the gentlest way that clears each link, or none; follows the
fall to the cell it comes down in, so it can say whether that is water and whether it is still on the piece; and
gives the fall damage, which only water where the player lands cancels.

`raster()` paints the course into a `Raster`, so the walk graph, sight and the sketch read a course as they read
any board. Data given as a set of cells (water, a hill) is carried through the symmetry with the piece.
"""
import math
from dataclasses import dataclass, field

import numpy as np

from . import move
from .plan import Raster

WAYS = ("walk", "step off", "run off", "sprint jump")
WIDTH = 0.6                                       # a player's width, counted as walk.gap_cleared counts it


def box(x0, x1, z0, z1):
    """The cells of a rectangle, inclusive."""
    x0, x1 = sorted((x0, x1)); z0, z1 = sorted((z0, z1))
    return {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}


@dataclass
class Piece:
    name: str
    cells: set
    y: int                                        # the top: the block a player stands on
    kind: str = "floor"
    step: int = 0
    side: str = "main"                            # "main", "image" or "middle"
    data: dict = field(default_factory=dict)

    @property
    def label(self):
        return self.name + (" (image)" if self.side == "image" else "")

    def centre(self):
        a = np.array(sorted(self.cells), float)
        return tuple(a.mean(axis=0) + 0.5)


class Course:
    def __init__(self, symmetry=None):
        self.symmetry = symmetry
        self.pieces = []
        self.steps = 0

    def _image(self, cells):
        return {tuple(int(round(v)) for v in self.symmetry.point(x, z)) for x, z in cells}

    def add(self, name, cells, y, kind="floor", same_step=False, **data):
        """One step of the course (or another piece of the last step, with same_step). Returns its pieces."""
        if not same_step or not self.pieces:
            self.steps += 1
        step = self.steps - 1
        cells = set(cells)
        out = []
        if self.symmetry is None:
            out.append(Piece(name, cells, y, kind, step, "main", data))
        else:
            img = self._image(cells)
            if img & cells:
                merged = {k: (v | self._image(v)) if isinstance(v, set) else v for k, v in data.items()}
                out.append(Piece(name, cells | img, y, kind, step, "middle", merged))
            else:
                out.append(Piece(name, cells, y, kind, step, "main", data))
                mapped = {k: self._image(v) if isinstance(v, set) else v for k, v in data.items()}
                out.append(Piece(name, img, y, kind, step, "image", mapped))
        self.pieces += out
        return out

    def step(self, i):
        return [p for p in self.pieces if p.step == i]

    def links(self):
        """(a, b) for each piece and each piece of the next step on its side or in the middle."""
        out = []
        for i in range(self.steps - 1):
            for a in self.step(i):
                for b in self.step(i + 1):
                    if "middle" in (a.side, b.side) or a.side == b.side:
                        out.append((a, b))
        return out

    def raster(self, kinds=None, margin=4, base_h=0, base_kind="void"):
        """The course as a Raster: every piece's cells at its top, in its kind. Images are already pieces, so
        nothing is drawn twice; the Raster keeps the symmetry for the sketch's paler half."""
        xs = [x for p in self.pieces for x, _ in p.cells]
        zs = [z for p in self.pieces for _, z in p.cells]
        kinds = kinds or [base_kind] + sorted({p.kind for p in self.pieces} - {base_kind})
        R = Raster((min(xs) - margin, max(xs) + margin), (min(zs) - margin, max(zs) + margin), kinds, base_h,
                   base_kind, self.symmetry)
        for p in self.pieces:
            for x, z in p.cells:
                R.cell(x, z, p.y, p.kind, both=False)
        return R

    def audit(self, health=20):
        """Every link judged: a dict of names, gap, drop, the gentlest way that clears it (or None), the carry it
        has to spare, the damage, whether water breaks the fall, and whether it kills."""
        rows, done = [], {}
        for a, b in self.links():
            drop = a.y - b.y
            twin = done.get((a.name, _swap(a.side), b.name, _swap(b.side)))
            if twin and "image" in (a.side, b.side):              # the image of a link already judged: mirrored
                g, how, spare = twin["gap"], twin["how"], twin["spare"]
                take_off, landing = self._point(twin["take_off"]), self._point(twin["landing"])
                lands = self._point(twin["lands"]) if twin["lands"] else None
            else:
                g, take_off, landing = gap(a, b)
                how, spare = clears(g, drop)
                lands = lands_at(take_off, landing, g, drop, how) if how else None
            pool = b.data.get("water")
            water = isinstance(pool, set) and lands in pool
            dmg = 0 if water else move.fall_damage(drop) if drop > 0 else 0
            rows.append(dict(a=a.label, b=b.label, gap=g, drop=drop, how=how, spare=spare, damage=dmg, water=water,
                             lethal=dmg >= health, take_off=take_off, landing=landing, lands=lands,
                             on_piece=lands in b.cells if lands else False))
            done[(a.name, a.side, b.name, b.side)] = rows[-1]
        return rows

    def _point(self, c):
        return tuple(int(round(v)) for v in self.symmetry.point(*c))


def _swap(side):
    return {"main": "image", "image": "main"}.get(side, side)


def gap(a, b):
    """The clear distance over the void between two pieces, edge to edge (0 if they touch), with the take-off
    and landing cells it is measured between."""
    A = np.array(sorted(a.cells)); Bc = np.array(sorted(b.cells))
    dx = np.maximum(np.abs(A[:, None, 0] - Bc[None, :, 0]) - 1, 0)
    dz = np.maximum(np.abs(A[:, None, 1] - Bc[None, :, 1]) - 1, 0)
    d = np.hypot(dx, dz)
    i, j = np.unravel_index(np.argmin(d), d.shape)
    return float(d[i, j]), tuple(int(v) for v in A[i]), tuple(int(v) for v in Bc[j])


def lands_at(take_off, landing, g, drop, how):
    """The cell a player comes down in, leaving take_off's edge toward landing the given way: the edge is half a
    block out from the take-off cell's centre, and the fall carries on from there."""
    if how == "walk":
        return landing
    dx, dz = landing[0] - take_off[0], landing[1] - take_off[1]
    n = math.hypot(dx, dz) or 1.0
    ux, uz = dx / n, dz / n
    edge = 0.5 / max(abs(ux), abs(uz))                    # from the centre to the block's side along that line
    carry = move.fall(drop, how)[1] if drop > 0 else move.jump_reach(-drop, how)
    x = take_off[0] + 0.5 + ux * (edge + carry)
    z = take_off[1] + 0.5 + uz * (edge + carry)
    return int(math.floor(x)), int(math.floor(z))


def clears(g, drop):
    """The gentlest way across a gap of g blocks onto a piece `drop` blocks lower (negative: higher), and how
    much carry it has to spare; (None, shortfall) if nothing clears it."""
    if g <= 0 and -1 <= drop <= 1:
        return "walk", 0.0
    best = None
    for how in WAYS[1:]:
        if drop > 0:
            carry = move.fall(drop, how)[1]
        elif how == "sprint jump":
            carry = move.jump_reach(-drop, how)
        else:
            continue
        spare = carry - g - WIDTH
        if spare >= 0:
            return how, round(spare, 2)
        best = spare if best is None else max(best, spare)
    return None, round(best if best is not None else -g, 2)
