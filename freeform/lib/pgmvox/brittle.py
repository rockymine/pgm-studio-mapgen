"""The Brittlebush style: a board drawn as a blueprint of five-block cells and built in the look of Brittlebush I
and II, read block by block off those maps (boards/brittle-study/STYLE.md).

    cells = {(cx, cz): Cell("flat", 13), (cx + 1, cz): Cell("stair", 10, rises="w"), ...}
    build(w, cells, only=red_cells, rng=r, dye=14)      every block of the cells in `only`, read against all of them
    tower(w, (x0, z0, x1, z1), 13, [(5, 0), (5, 1), (4, 2)], dye=14, door="s")
    heart(w, x, y, z, dye, facing="s")

A cell is one of a handful of pieces, its y the floor block:

    flat      level ground; a flat piece that is a rectangle two cells or more each way is grass in its double ring
              of sandstone stairs, with a birch if wide enough; any other piece, one cell wide or not a rectangle,
              is sand
    keep      a spawn's floor: smooth sandstone, a ring of the team's clay
    tower     the ground under a tower, laid like flat ground; tower() builds the tower on it
    stacked   a piece with a deck at y; a cell of it with under=True is open beneath, a lower floor DECK under
              the deck, the deck's edge capped without black clay, a dark-oak pillar mid-way along a long open side
    stair     one level up, three blocks in five, toward `rises`, from a floor at y: a stone-brick slab and a stone-brick
              block in turn, half a block a row
    gap       void a player builds over: block 36 at y 0, and a cobweb mid-way along each edge it shares with void
    water     a gap with water at its foot, no kerb and no cobwebs: the water marks it, and PGM holds it still
    void      nothing

Every column of ground is four courses of stone over bedrock to y 3, an obsidian sheet at y 1 and 2, block 36 at
y 0. Its edge over anything two or more lower is the five-course cap: an upside-down spruce stair, brick, a dark-oak
slab, an upside-down dark-oak stair, black clay; every other cell along a face is the birch-stair panel, five wide,
framed in black clay that carries the band up round it. A piece's outline is one block: the rim where it falls
away, spruce planks where it meets a wall or a stair; inside it, at once, its field or its bed.

house() raises a wool room as Brittlebush I does: storeys of whole cells, each smaller than the one under it.
"""
from dataclasses import dataclass, replace

import numpy as np
from scipy import ndimage

from .blocks import B
from .orient import stair

CELL = 5
DIRS = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}
OPP = {"n": "s", "s": "n", "e": "w", "w": "e"}
CW = {"n": "e", "e": "s", "s": "w", "w": "n"}
SPRUCE_PLANKS = (B.PLANKS, 1)
DARK_OAK_SLAB = (B.WOOD_SLAB, 5)
BLACK_CLAY = (B.STAINED_CLAY, 15)
SB_SLAB = (B.SLAB, 5)
LAND = ("flat", "keep", "tower", "stacked", "stair")
DECK = 8                                 # a stacked piece's lower floor lies this far under its deck


@dataclass(frozen=True)
class Cell:
    kind: str
    y: int = None
    rises: str = None
    name: str = None
    under: bool = False                  # a stacked cell open under its deck, its lower floor DECK down
    section: str = None                  # the section it belongs to: a piece is cells of one height and one section


def turn_cells(cells, k=1):
    """A blueprint turned k quarters clockwise about the middle: cell (cx, cz) -> (-1 - cz, cx), a stair's rise
    turned with it."""
    out = cells
    for _ in range(k):
        out = {(-1 - cz, cx): (replace(c, rises=CW[c.rises]) if c.rises else c) for (cx, cz), c in out.items()}
    return out


def fan(unit, order=4):
    """A unit drawn once, with its images under quarter turns: ({cell: Cell}, {cell: the image it came from})."""
    cells, team = {}, {}
    for k in range(order):
        for c, v in turn_cells(unit, k).items():
            cells.setdefault(c, v)
            team.setdefault(c, k)
    return cells, team


# ---- reading the blueprint as blocks ---------------------------------------------------------------------
def heights(cells):
    """Per block column: G, the ground's top (an underfloor's, under a deck), and T, the top (a deck's); -1 off the
    land. Returned as dicts keyed (x, z)."""
    G, T = {}, {}
    for (cx, cz), c in cells.items():
        if c.kind not in LAND:
            continue
        for i in range(CELL):
            for k in range(CELL):
                x, z = cx * CELL + i, cz * CELL + k
                if c.kind == "stair":
                    r = _row(c.rises, i, k)
                    h = c.y + 1 + min(r, 3) // 2 + (1 if r == 4 else 0)
                    G[(x, z)] = T[(x, z)] = h
                elif c.kind == "stacked" and c.under:
                    G[(x, z)], T[(x, z)] = c.y - DECK, c.y
                else:
                    G[(x, z)] = T[(x, z)] = c.y
    return G, T


def _row(rises, i, k):
    """A stair column's row counted from its low side, 0 to 4."""
    return {"e": i, "w": CELL - 1 - i, "s": k, "n": CELL - 1 - k}[rises]


def pieces(cells):
    """The pieces: flat cells (flat, keep, tower, a stacked piece's deck) joined to their neighbours of the same kind,
    height and section, so a board cut into sections gets each its own outline, as
    {cell: piece number}, and each piece's theme, 'inlay' if it holds two cells by two, else 'sand'."""
    flat = {c for c, v in cells.items() if v.kind in ("flat", "keep", "tower", "stacked")}
    label, theme, n = {}, {}, 0
    for c in sorted(flat):
        if c in label:
            continue
        comp, todo = set(), [c]
        while todo:
            p = todo.pop()
            if p in comp or p not in flat or cells[p].y != cells[c].y or cells[p].section != cells[c].section or \
                    (cells[p].kind == "keep") != (cells[c].kind == "keep"):
                continue
            comp.add(p)
            todo += [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
        for p in comp:
            label[p] = n
        theme[n] = "inlay" if any({(x, z), (x + 1, z), (x, z + 1), (x + 1, z + 1)} <= comp for x, z in comp) \
            else "sand"
        n += 1
    return label, theme


# ---- the pieces of the look ------------------------------------------------------------------------------
def cap(w, x, z, h, inward, panel=None):
    """A ground edge, top down: an upside-down spruce stair, its full side inward; brick; a dark-oak slab; an
    upside-down dark-oak stair; black clay. Every other cell along a face is a panel the cell's five wide: its
    middle three (panel "inner") swap the brick, the slab and the dark-oak stair for black clay over three birch
    stairs, and its two outer columns (panel "side") are black clay all the way down. So the black clay is one
    unbroken band along the board's edge, at the foot of the plain cells, rising round each panel and over it."""
    w.set(x, h, z, B.SPRUCE_STAIRS, stair(inward, upside_down=True))
    if h - 4 < 3 and panel != "deck":
        raise ValueError(f"a cap at {h} reaches under y 3, into the obsidian and the build marker: raise the floor")
    if panel == "deck":                                     # a deck's edge over open air: no black clay
        w.set(x, h - 1, z, B.BRICK)
        w.set(x, h - 2, z, *DARK_OAK_SLAB)
        w.set(x, h - 3, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=True))
    elif panel == "side":
        for y in range(h - 4, h):
            w.set(x, y, z, *BLACK_CLAY)
    elif panel == "inner":
        w.set(x, h - 1, z, *BLACK_CLAY)
        w.set(x, h - 2, z, B.BIRCH_STAIRS, stair(inward))
        w.set(x, h - 3, z, B.BIRCH_STAIRS, stair(inward))
        w.set(x, h - 4, z, B.BIRCH_STAIRS, stair(inward, upside_down=True))
    else:
        w.set(x, h - 1, z, B.BRICK)
        w.set(x, h - 2, z, *DARK_OAK_SLAB)
        w.set(x, h - 3, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=True))
        w.set(x, h - 4, z, *BLACK_CLAY)


def ground(w, x, z, h, fill=(B.STONE, 0)):
    """Under a floor at h: four courses of stone, bedrock to y 3, obsidian at y 1 and 2, block 36 at y 0."""
    for y in range(max(3, h - 4), h):
        w.set(x, y, z, *fill)
    for y in range(3, h - 4):
        w.set(x, y, z, B.BEDROCK)
    w.set(x, 2, z, B.OBSIDIAN)
    w.set(x, 1, z, B.OBSIDIAN)
    w.set(x, 0, z, 36)


def tree(w, x, y, z, rng=None, height=5):
    """A round birch over the floor at y: a trunk `height` high and a crown of leaves."""
    top = y + height + 1
    for yy in range(y + 1, top):
        w.set(x, yy, z, B.LOG, 2)
    for yy in range(top - 2, top + 2):
        r = 2 if yy < top + 1 else 1
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + (1 if yy < top else 0) and w.get(x + dx, yy, z + dz)[0] == B.AIR:
                    w.set(x + dx, yy, z + dz, B.LEAVES, 2 | 4)


def bed(w, x0, z0, x1, z1, y, rng, trees=True):
    """A bed of grass inside two rings of sandstone stairs, as Brittlebush lays every one: the outer ring rising
    inward, the inner ring rising outward, so the two meet in a ridge; sandstone at the inner ring's corners. In
    the grass, birch-leaf bushes level with it and tall grass; a birch at its middle when the grass is four or more
    across."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):                       # the outer ring, rising inward
                d = "e" if x == x0 else "w" if x == x1 else "s" if z == z0 else "n"
                w.set(x, y, z, B.SANDSTONE_STAIRS, stair(d))
            elif x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1):     # the inner ring, rising outward
                if x in (x0 + 1, x1 - 1) and z in (z0 + 1, z1 - 1):
                    w.set(x, y, z, B.SANDSTONE)
                else:
                    d = "w" if x == x0 + 1 else "e" if x == x1 - 1 else "n" if z == z0 + 1 else "s"
                    w.set(x, y, z, B.SANDSTONE_STAIRS, stair(d))
            else:
                c = rng.random()
                if c < 0.18:
                    w.set(x, y, z, B.LEAVES, 2 | 4)
                else:
                    w.set(x, y, z, B.GRASS)
                    if c < 0.40:
                        w.set(x, y + 1, z, B.TALLGRASS, 1)
                    elif c < 0.45:
                        w.set(x, y + 1, z, B.FLOWER, 2)
    if trees and min(x1 - x0, z1 - z0) - 4 >= 3:
        tx, tz = (x0 + x1) // 2, (z0 + z1) // 2
        w.set(tx, y, tz, B.GRASS)
        w.set(tx, y + 1, tz, B.AIR)
        tree(w, tx, y, tz, rng)


def sand(w, cells_xz, y, rng, stairs=0.25):
    """A sand field as Brittlebush lays it: sand mixed with upside-down sandstone stairs, whose grainy tops read
    as the same ground, about one in four; then, on pure sand only, dead bushes and cacti one to three high with
    pure sand and nothing standing on every side of them."""
    cells_xz = list(cells_xz)
    for x, z in cells_xz:
        if rng.random() < stairs:
            w.set(x, y, z, B.SANDSTONE_STAIRS, stair("nsew"[int(rng.random() * 4)], upside_down=True))
        else:
            w.set(x, y, z, B.SAND)
    for x, z in cells_xz:
        if w.id(x, y, z) != B.SAND:
            continue
        c = rng.random()
        if c < 0.02:
            w.set(x, y + 1, z, B.DEADBUSH)
        elif c < 0.035:
            clear = all(w.id(x + dx, y, z + dz) == B.SAND and w.id(x + dx, y + 1, z + dz) == B.AIR
                        for dx, dz in DIRS.values())
            if clear:
                for yy in range(y + 1, y + 2 + int(rng.random() * 3)):
                    w.set(x, yy, z, B.CACTUS)


# ---- the build -------------------------------------------------------------------------------------------
def build(w, cells, only=None, rng=None, dye=14, fill=None):
    """Every block of the cells in `only` (default all), each read against the whole blueprint, so a face on the
    edge of one team's part is right where it meets another's. `dye` colours the keep's ring. fill(piece's cells,
    cells) may choose a rectangle's fill: "bed" (grass and its birch, the default), "grass" (no tree) or "sand"."""
    import random
    rng = rng or random.Random(0)
    only = set(cells) if only is None else set(only)
    G, T = heights(cells)
    label, theme = pieces(cells)

    def g(x, z):
        return G.get((x, z), -1)

    def cell_of(x, z):
        return (x // CELL, z // CELL)

    # where each column of a flat piece lies in its piece: blocks in from the piece's edge
    piece_mask, piece_d = {}, {}
    for n in set(label.values()):
        cs = [c for c, v in label.items() if v == n]
        xs = [c[0] for c in cs]
        zs = [c[1] for c in cs]
        bx0, bz0 = min(xs) * CELL - 1, min(zs) * CELL - 1
        m = np.zeros(((max(xs) - min(xs) + 1) * CELL + 2, (max(zs) - min(zs) + 1) * CELL + 2), bool)
        for cx, cz in cs:
            m[cx * CELL - bx0:(cx + 1) * CELL - bx0, cz * CELL - bz0:(cz + 1) * CELL - bz0] = True
        d = ndimage.distance_transform_cdt(m, metric="chessboard") - 1
        piece_mask[n], piece_d[n] = (bx0, bz0), d

    def depth(x, z):
        n = label[cell_of(x, z)]
        bx0, bz0 = piece_mask[n]
        return int(piece_d[n][x - bx0, z - bz0])

    for (cx, cz) in sorted(only):
        c = cells[(cx, cz)]
        x0, z0 = cx * CELL, cz * CELL
        cols = [(x0 + i, z0 + k) for i in range(CELL) for k in range(CELL)]
        if c.kind in ("gap", "water"):
            for x, z in cols:
                w.set(x, 0, z, 36)
            if c.kind == "water":                  # water marks itself: no cobwebs, no kerb; PGM holds it still
                for x, z in cols:
                    w.set(x, 1, z, B.WATER)
            else:                                                          # a cobweb mid-edge where it meets void
                for d, (dx, dz) in DIRS.items():
                    if cells.get((cx + dx, cz + dz), Cell("void")).kind == "void":
                        ex = x0 + (CELL - 1 if dx > 0 else 0 if dx < 0 else 2)
                        ez = z0 + (CELL - 1 if dz > 0 else 0 if dz < 0 else 2)
                        w.set(ex, 1, ez, B.COBWEB)
            continue
        if c.kind not in LAND:
            continue
        if c.kind == "stacked" and c.under:
            _under(w, c, x0, z0, cells, G, T, rng)
        for x, z in cols:
            h = T[(x, z)]
            if not (c.kind == "stacked" and c.under):
                ground(w, x, z, h, fill=(B.STONEBRICK, 0) if c.kind == "stair" else (B.STONE, 0))
            out = [d for d, (dx, dz) in DIRS.items() if T.get((x + dx, z + dz), -1) < h - 1]
            if c.kind == "stair":
                side = [d for d in out if d not in (c.rises, OPP[c.rises])]
                if side:                                                   # its side: the ground's own edge,
                    cap(w, x, z, h, OPP[side[0]])                          # stepping down with the rows
                    continue
                r = _row(c.rises, x - x0, z - z0)
                top = SB_SLAB if r % 2 == 0 else (B.STONEBRICK, 0)
                w.set(x, h, z, *top)
                if r == 4:                                                 # the last half step, a slab on a block
                    w.set(x, h - 1, z, B.STONEBRICK)
                continue
            if c.kind == "stacked" and c.under:
                if out:                                                    # a deck's edge: the cap, no black clay
                    cap(w, x, z, h, OPP[out[0]], panel="deck")
                continue
            if c.kind == "stacked" and any(cells.get(cell_of(x + dx, z + dz), Cell("void")).under
                                           for dx, dz in DIRS.values()):
                w.set(x, h - 4, z, *BLACK_CLAY)                            # the line under the deck, on its wall
            if out:
                along = (z // CELL) if out[0] in ("e", "w") else (x // CELL)
                pos = (z - z0) if out[0] in ("e", "w") else (x - x0)
                dx, dz = DIRS[out[0]]
                open_face = T.get((x + dx, z + dz), -1) <= h - 5               # room for the whole panel
                cap(w, x, z, h, OPP[out[0]],
                    panel=None if along % 2 or not open_face else "inner" if 1 <= pos <= 3 else "side")
        if c.kind == "stair":
            continue
        # the frame and the field of a flat piece
        n = label[(cx, cz)]
        field = []
        for x, z in cols:
            h = T[(x, z)]
            if any(T.get((x + dx, z + dz), -1) < h - 1 for dx, dz in DIRS.values()):
                continue                                                   # the rim, laid with the cap
            dd = depth(x, z)
            if dd == 0:                                                    # the outline against a wall or a stair:
                w.set(x, h, z, *SPRUCE_PLANKS)                             # one block, as the rim is elsewhere
            elif c.kind == "keep":
                w.set(x, h, z, *((B.STAINED_CLAY, dye) if dd == 1 else (B.SANDSTONE, 2)))
            else:
                field.append((x, z))
        if field:
            sand(w, field, c.y, rng)
    # the inlay's beds, filling a piece's inside up to its outline: one bed for a piece that is a rectangle of
    # cells; a piece of any other shape keeps its sand
    if any(t == "inlay" for t in theme.values()):
        used = set()
        for (cx, cz) in sorted(only):
            c = cells[(cx, cz)]
            if c.kind not in ("flat", "stacked") or theme[label[(cx, cz)]] != "inlay" or (cx, cz) in used:
                continue
            n = label[(cx, cz)]
            comp = [p for p, v in label.items() if v == n]
            xs, zs = [p[0] for p in comp], [p[1] for p in comp]
            rect = len(comp) == (max(xs) - min(xs) + 1) * (max(zs) - min(zs) + 1)
            if not (rect and all(p in only and cells[p].kind in ("flat", "stacked") for p in comp)):
                continue                                                    # not a rectangle: sand only
            block = comp
            used |= set(block)
            how = (fill(comp, cells) if fill else None) or "bed"
            if how == "sand":
                continue
            inner = [(x, z) for bx, bz in block for x in range(bx * CELL, bx * CELL + CELL)
                     for z in range(bz * CELL, bz * CELL + CELL) if depth(x, z) >= 1]
            xs, zs = [p[0] for p in inner], [p[1] for p in inner]
            if inner and max(xs) - min(xs) >= 5 and max(zs) - min(zs) >= 5:
                bed(w, min(xs), min(zs), max(xs), max(zs), c.y, rng, trees=(how == "bed"))
    for p in sorted(only):                                                 # the under-sections' pillars, last
        c = cells[p]
        if c.kind == "stacked" and c.under:
            _pillars(w, c, p[0] * CELL, p[1] * CELL, cells)


def _under(w, c, x0, z0, cells, G, T, rng):
    """A stacked cell open under its deck, as Brittlebush I builds one: the deck four courses thick (its surface
    laid with the piece, stone under it); four blocks of air; a lower floor DECK under the deck that runs into the
    floor of the world without the full cap. Its edge is the rim, brick and black clay; its middle is sand on sand;
    along the island's wall at its back lie planks on brick; bedrock under all of it to y 1, block 36 at y 0. A
    lower floor low in the world keeps as many of those courses as fit over y 0, down to its top alone at y 1. Its
    pillars are _pillars', laid once every under cell is."""
    lower = c.y - DECK
    if lower < 1:
        raise ValueError(f"a deck at {c.y} puts its lower floor on the build marker at y 0: raise the floor")
    sandy = []
    for i in range(CELL):
        for k in range(CELL):
            x, z = x0 + i, z0 + k
            for y in range(c.y - 3, c.y):
                w.set(x, y, z, B.STONE)
            for y in range(lower + 1, c.y - 3):
                w.set(x, y, z, B.AIR)
            for y in range(1, lower - 1):
                w.set(x, y, z, B.BEDROCK)
            w.set(x, 0, z, 36)
            out = [d for d, (dx, dz) in DIRS.items() if G.get((x + dx, z + dz), -1) < lower - 1]
            if out:                                                  # the short cap, into the floor
                w.set(x, lower, z, B.SPRUCE_STAIRS, stair(OPP[out[0]], upside_down=True))
                if lower - 1 >= 1:
                    w.set(x, lower - 1, z, B.BRICK)
                if lower - 2 >= 1:
                    w.set(x, lower - 2, z, *BLACK_CLAY)
            elif any(G.get((x + dx, z + dz), -1) > lower for dx, dz in DIRS.values()):
                w.set(x, lower, z, *SPRUCE_PLANKS)                   # along the island's wall at its back
                if lower - 1 >= 1:
                    w.set(x, lower - 1, z, B.BRICK)
            else:
                if lower - 1 >= 1:
                    w.set(x, lower - 1, z, B.SAND)
                sandy.append((x, z))
    sand(w, sandy, lower, rng)


def _pillars(w, c, x0, z0, cells):
    """Where an under cell's open side runs two cells or more, a pillar two wide at the run's middle: dark-oak
    planks, a dark-oak stair and an upside-down one in turn, from under the deck down into the lower floor's edge.
    Laid after every under cell, since the middle of an even run is a cell's edge."""
    lower = c.y - DECK
    # the pillars: on each open side whose run of open cells is two or more, once, at the run's middle
    cx, cz = x0 // CELL, z0 // CELL

    def open_side(p, dx, dz):
        nb = cells.get((p[0] + dx, p[1] + dz))
        return not (nb and nb.kind in ("stacked", "flat", "keep", "tower", "stair") and nb.y is not None
                    and nb.y >= c.y - DECK + 2)
    for d, (dx, dz) in DIRS.items():
        if not open_side((cx, cz), dx, dz):
            continue
        ax, az = abs(dz), abs(dx)                                  # along the side
        run = [(cx, cz)]
        for sgn in (1, -1):
            p = (cx + ax * sgn, cz + az * sgn)
            while cells.get(p) and cells[p].kind == "stacked" and cells[p].under and open_side(p, dx, dz):
                run.append(p)
                p = (p[0] + ax * sgn, p[1] + az * sgn)
        first = min(run, key=lambda q: q[0] * ax + q[1] * az)
        if len(run) < 2 or first != (cx, cz):
            continue
        mid = (first[0] * ax + first[1] * az) * CELL + len(run) * CELL // 2
        ex = x0 + CELL - 1 if dx > 0 else x0 if dx < 0 else None
        ez = z0 + CELL - 1 if dz > 0 else z0 if dz < 0 else None
        for a in (mid - 1, mid):
            px, pz = (ex, a) if ex is not None else (a, ez)
            for n, y in enumerate(range(c.y - 4, max(lower - 2, 0), -1)):
                if n % 3 == 0:
                    w.set(px, y, pz, B.PLANKS, 5)
                else:
                    w.set(px, y, pz, B.DARK_OAK_STAIRS, stair(OPP[d], upside_down=(n % 3 == 2)))


# ---- buildings -------------------------------------------------------------------------------------------
def storey(w, plate, base_y, top, dye, door=None, panels=True):
    """One storey of a tiered tower: walls of black clay one in from its plate (x0, z0, x1, z1), a band of `dye`
    two under the plate, brick under the plate, birch-stair panels two high every three on a wall five or more
    high; doors, each (side, (a, b)) or a list of them, three high; the plate at `top` with the ground's own edge
    and dark-oak brackets."""
    doors = [door] if door and isinstance(door[0], str) else list(door or [])
    x0, z0, x1, z1 = plate
    a0, b0, a1, b1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1
    for x in range(a0, a1 + 1):
        for z in range(b0, b1 + 1):
            if not (x in (a0, a1) or z in (b0, b1)):
                continue
            along = z if x in (a0, a1) else x
            side = "w" if x == a0 else "e" if x == a1 else "n" if z == b0 else "s"
            corner = x in (a0, a1) and z in (b0, b1)
            for y in range(base_y + 1, top):
                v = top - y
                if any(side == d[0] and d[1][0] <= along <= d[1][1] for d in doors) and y <= base_y + 3 and not corner:
                    w.set(x, y, z, B.AIR)
                elif v == 1:
                    w.set(x, y, z, B.BRICK)
                elif v == 2:
                    w.set(x, y, z, B.WOOL, dye)
                elif panels and not corner and along % 3 == 1 and v in (3, 4) and top - base_y >= 5:
                    w.set(x, y, z, B.BIRCH_STAIRS, stair(OPP[side], upside_down=(v == 3)))
                else:
                    w.set(x, y, z, *BLACK_CLAY)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                inward = "e" if x == x0 else "w" if x == x1 else "s" if z == z0 else "n"
                w.set(x, top, z, B.SPRUCE_STAIRS, stair(inward, upside_down=True))
                if not (x in (x0, x1) and z in (z0, z1)):
                    w.set(x, top - 1, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=True))
            else:
                w.set(x, top, z, *SPRUCE_PLANKS)


def tower(w, box, base_y, tiers, dye, door=None, crown=(B.GOLD_BLOCK, 0)):
    """A tiered tower on the ground at base_y over box (x0, z0, x1, z1): tiers [(height, inset), ...] from the
    bottom, each storey's plate stepped in by its inset from the box; a crown of sandstone stairs round `crown` on
    the top plate. The first storey's doors are `door`: (side, (a, b)) or a list of them. A spawn's house is the
    same building with its doors where its stairs lead out. Returns the top plate's y and middle."""
    x0, z0, x1, z1 = box
    y = base_y
    for n, (h, inset) in enumerate(tiers):
        plate = (x0 + inset, z0 + inset, x1 - inset, z1 - inset)
        storey(w, plate, y, y + h, dye, door=door if n == 0 else None)
        y += h
    px0, pz0, px1, pz1 = plate
    cx, cz = (px0 + px1) // 2, (pz0 + pz1) // 2
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            d = "e" if x == cx - 1 else "w" if x == cx + 1 else "s" if z == cz - 1 else "n" if z == cz + 1 else None
            if d and (x, z) != (cx, cz):
                w.set(x, y, z, B.SANDSTONE_STAIRS, stair(d))
            else:
                w.set(x, y, z, *crown)
    return y, (cx, cz)


def house(w, layers, floor, dye, door=None, cobwebs=True, floor_block=(B.PLANKS, 0)):
    """A building as Brittlebush I raises its wool rooms: storeys of whole cells, five blocks each, every storey
    over part of the one under it, as a block of two cells by two, an L of three over it, and one cell on top.

    layers is a list of storeys from the bottom, each a list of cells (cx, cz); door is (cell, side) or a list of
    them, each three wide and three high in that cell's middle on the first storey, with cobwebs one block inside it
    unless `cobwebs` is False, as a spawn's house wants. floor_block is the first storey's floor, or None to keep
    the ground's own, as a keep's ring of the team's clay. A storey's wall is the
    ground's edge again, read bottom up: black clay, an upside-down dark-oak stair, a dark-oak stair, brick; and
    every other cell along a face the birch panel framed in black clay, `dye` tucked under the eave over it. Its
    plate overhangs by one, in eaves of planks and upside-down spruce stairs and slab; where the next storey does
    not stand on it, its roof is a terrace of sand in a ring of spruce stairs, on a ceiling of sandstone lit by sea
    lanterns. A one-cell top storey holds a beacon
    on gold, shining through glass of `dye`. The storeys over the first are hollow."""
    doors = [] if door is None else [door] if isinstance(door[1], str) else list(door)
    doors = {(tuple(c), d) for c, d in doors}
    for k, layer in enumerate(layers):
        base, top = floor + 5 * k, floor + 5 * k + 5
        above = set(layers[k + 1]) if k + 1 < len(layers) else set()
        cols = {(cx * CELL + i, cz * CELL + j) for cx, cz in layer for i in range(CELL) for j in range(CELL)}
        roof = {(x, z) for x, z in cols if (x // CELL, z // CELL) not in above}

        def outside(x, z, region=cols):
            return [d for d, (dx, dz) in DIRS.items() if (x + dx, z + dz) not in region]

        def diagonal_out(x, z, region=cols):
            return any((x + dx, z + dz) not in region for dx in (-1, 1) for dz in (-1, 1))

        # the walls, and the hollow inside them
        for x, z in cols:
            outs = outside(x, z)
            if not outs and not diagonal_out(x, z):
                for y in range(base + 1, top):
                    w.set(x, y, z, B.AIR)
                if k == 0 and floor_block:
                    w.set(x, base, z, *floor_block)
                continue
            if len(outs) != 1:                                          # a corner, outer or inner
                for y in range(base + 1, top):
                    w.set(x, y, z, *BLACK_CLAY)
                continue
            d = outs[0]
            inward = OPP[d]
            along, pos = ((z // CELL), z % CELL) if d in "ew" else ((x // CELL), x % CELL)
            panel = along % 2 == 0
            for y in range(base + 1, top):
                v = top - y
                if panel and pos in (0, 4):
                    w.set(x, y, z, *BLACK_CLAY)
                elif v == 1:
                    w.set(x, y, z, B.BRICK)
                elif panel:
                    w.set(x, y, z, B.BIRCH_STAIRS, stair(inward, upside_down=(v == 4)))
                elif v == 4:
                    w.set(x, y, z, *BLACK_CLAY)
                else:
                    w.set(x, y, z, B.DARK_OAK_STAIRS, stair(inward, upside_down=(v == 3)))
            if panel and pos not in (0, 4):                             # the wool's colour under the eave
                dx, dz = DIRS[d]
                if w.id(x + dx, top - 1, z + dz) == B.AIR:
                    w.set(x + dx, top - 1, z + dz, B.WOOL, dye)
            if k == 0 and ((x // CELL, z // CELL), d) in doors and pos in (1, 2, 3):
                dx, dz = DIRS[d]
                for y in range(base + 1, base + 4):
                    w.set(x, y, z, B.AIR)
                    if cobwebs:
                        w.set(x - dx, y, z - dz, B.COBWEB)
        # the plate: the next storey's floor, or a terrace of sand in a ring of spruce stairs
        for x, z in cols:
            if (x, z) not in roof:
                w.set(x, top, z, *SPRUCE_PLANKS)
                continue
            outs = outside(x, z, roof)
            if len(outs) > 1 or (not outs and diagonal_out(x, z, roof)):
                w.set(x, top, z, *SPRUCE_PLANKS)
            elif outs:
                w.set(x, top, z, B.SPRUCE_STAIRS, stair(outs[0]))
            else:
                w.set(x, top, z, B.SAND)
                inner = not outside(x + 1, z, roof) and not outside(x - 1, z, roof) and \
                    not outside(x, z + 1, roof) and not outside(x, z - 1, roof)
                w.set(x, top - 1, z, *((B.SEA_LANTERN, 0) if inner else (B.SANDSTONE, 2)))  # the ceiling under it
        # the eaves, one out all round
        ring = {(x + dx, z + dz) for x, z in cols for dx in (-1, 0, 1) for dz in (-1, 0, 1)} - cols
        for x, z in ring:
            if w.id(x, top, z) != B.AIR:
                continue
            ins = [d for d, (dx, dz) in DIRS.items() if (x + dx, z + dz) in cols]
            if len(ins) != 1:
                w.set(x, top, z, *SPRUCE_PLANKS)
                continue
            pos = z % CELL if ins[0] in "ew" else x % CELL
            end = ("n" if pos < 2 else "s") if ins[0] in "ew" else ("w" if pos < 2 else "e")
            if pos in (0, 4):
                w.set(x, top, z, *SPRUCE_PLANKS)
            elif pos == 2:
                w.set(x, top, z, B.WOOD_SLAB, 1 | 8)
            else:
                w.set(x, top, z, B.SPRUCE_STAIRS, stair(end, upside_down=True))
    # the beacon in a one-cell top storey
    last = layers[-1]
    if len(last) == 1:
        cx, cz = last[0]
        mx, mz = cx * CELL + 2, cz * CELL + 2
        base, top = floor + 5 * (len(layers) - 1), floor + 5 * len(layers)
        for x in range(mx - 1, mx + 2):
            for z in range(mz - 1, mz + 2):
                w.set(x, base + 1, z, B.WOOL, 15)
                w.set(x, base + 2, z, B.WOOL, 15)
                w.set(x, base + 3, z, B.GOLD_BLOCK)
                w.set(x, base + 4, z, B.SANDSTONE, 2)
        w.set(mx, base + 4, mz, B.BEACON)
        w.set(mx, top, mz, B.STAINED_GLASS, dye)


HEART = [".XX.XX.",
         "XXXXXXX",
         "XXXXXXX",
         ".XXXXX.",
         "..XXX..",
         "...X..."]


def heart(w, x, y, z, dye, facing="s", hang=None):
    """A heart seven wide and six high in `dye`, outlined and backed in black wool, standing upright over (x, z)
    with its bottom at y, its face toward `facing`; with hang, a pane of `dye` down to that y."""
    fx, fz = DIRS[facing]
    ax, az = -fz, fx                                          # across the heart
    rows = len(HEART)
    filled = {(i - 3, rows - 1 - j) for j, row in enumerate(HEART) for i, ch in enumerate(row) if ch == "X"}
    outline = {(u + du, v + dv) for u, v in filled for du in (-1, 0, 1) for dv in (-1, 0, 1)} - filled
    for u, v in filled | outline:
        px, pz = x + ax * u, z + az * u
        w.set(px, y + v + 1, pz, *((B.WOOL, dye) if (u, v) in filled else (B.WOOL, 15)))
        w.set(px - fx, y + v + 1, pz - fz, B.WOOL, 15)
    if hang is not None:
        for yy in range(hang, y + 1):
            w.set(x - fx, yy, z - fz, B.STAINED_PANE, dye)
