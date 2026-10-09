"""The Brittlebush style: a board drawn as a blueprint of five-block cells and built in the look of Brittlebush I
and II, read block by block off those maps (boards/brittle-study/STYLE.md).

    cells = {(cx, cz): Cell("flat", 13), (cx + 1, cz): Cell("stair", 10, rises="w"), ...}
    build(w, cells, only=red_cells, rng=r, dye=14)      every block of the cells in `only`, read against all of them
    tower(w, (x0, z0, x1, z1), 13, [(5, 0), (5, 1), (4, 2)], dye=14, door="s")
    heart(w, x, y, z, dye, facing="s")

A cell is one of a handful of pieces, its y the floor block:

    flat      level ground; a flat piece one cell wide is sand, one with two cells by two in it is inlay
    keep      a spawn's floor: smooth sandstone, a ring of the team's clay
    tower     the ground under a tower, laid like flat ground; tower() builds the tower on it
    stacked   a deck at y over an underfloor at y - 3, on dark-oak posts at the deck's corners
    stair     one level up, three blocks in five, toward `rises`, from a floor at y: a stone-brick slab and a stone-brick
              block in turn, half a block a row
    gap       void a player builds over: block 36 at y 0 and a cobweb on the floor of the void
    water     a gap with water at its foot, kerbed in bedrock where it meets open void or a dry gap, a cobweb over it
    void      nothing

Every column of ground is four courses of stone over bedrock to y 3, an obsidian sheet at y 1 and 2, block 36 at
y 0. Its edge over anything two or more lower is the five-course cap: an upside-down spruce stair, brick, a dark-oak
slab, an upside-down dark-oak stair, black clay; every other cell along a face is the birch-stair panel, five wide,
framed in black clay that carries the band up round it. A piece is framed: the rim on its edge, a band of spruce planks inside it, then its
field.
"""
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Cell:
    kind: str
    y: int = None
    rises: str = None
    name: str = None


def turn_cells(cells, k=1):
    """A blueprint turned k quarters clockwise about the middle: cell (cx, cz) -> (-1 - cz, cx), a stair's rise
    turned with it."""
    out = cells
    for _ in range(k):
        out = {(-1 - cz, cx): (Cell(c.kind, c.y, CW[c.rises], c.name) if c.rises else c) for (cx, cz), c in out.items()}
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
                elif c.kind == "stacked":
                    G[(x, z)], T[(x, z)] = c.y - 3, c.y
                else:
                    G[(x, z)] = T[(x, z)] = c.y
    return G, T


def _row(rises, i, k):
    """A stair column's row counted from its low side, 0 to 4."""
    return {"e": i, "w": CELL - 1 - i, "s": k, "n": CELL - 1 - k}[rises]


def pieces(cells):
    """The pieces: flat cells (flat, keep, tower) joined to their neighbours of the same kind and height, as
    {cell: piece number}, and each piece's theme, 'inlay' if it holds two cells by two, else 'sand'."""
    flat = {c for c, v in cells.items() if v.kind in ("flat", "keep", "tower")}
    label, theme, n = {}, {}, 0
    for c in sorted(flat):
        if c in label:
            continue
        comp, todo = set(), [c]
        while todo:
            p = todo.pop()
            if p in comp or p not in flat or cells[p].y != cells[c].y or \
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
    if h - 4 < 3:
        raise ValueError(f"a cap at {h} reaches under y 3, into the obsidian and the build marker: raise the floor")
    if panel == "side":
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
def build(w, cells, only=None, rng=None, dye=14):
    """Every block of the cells in `only` (default all), each read against the whole blueprint, so a face on the
    edge of one team's part is right where it meets another's. `dye` colours the keep's ring."""
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
            if c.kind == "water":
                for x, z in cols:
                    shore = any(cells.get(cell_of(x + dx, z + dz), Cell("void")).kind in ("void", "gap")
                                and cell_of(x + dx, z + dz) != (cx, cz) for dx, dz in DIRS.values())
                    w.set(x, 1, z, *((B.BEDROCK, 0) if shore else (B.WATER, 0)))
                w.set(x0 + 2, 2, z0 + 2, B.COBWEB)
            else:
                w.set(x0 + 2, 1, z0 + 2, B.COBWEB)
            continue
        if c.kind not in LAND:
            continue
        for x, z in cols:
            h = g(x, z)
            ground(w, x, z, h, fill=(B.STONEBRICK, 0) if c.kind == "stair" else (B.STONE, 0))
            out = [d for d, (dx, dz) in DIRS.items() if g(x + dx, z + dz) < h - 1]
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
            if out:
                along = (z // CELL) if out[0] in ("e", "w") else (x // CELL)
                pos = (z - z0) if out[0] in ("e", "w") else (x - x0)
                cap(w, x, z, h, OPP[out[0]],
                    panel=None if along % 2 else "inner" if 1 <= pos <= 3 else "side")
        if c.kind == "stair":
            continue
        if c.kind == "stacked":
            _stacked(w, c, x0, z0, cells, T)
            continue
        # the frame and the field of a flat piece
        n = label[(cx, cz)]
        field = []
        for x, z in cols:
            h = g(x, z)
            if any(g(x + dx, z + dz) < h - 1 for dx, dz in DIRS.values()):
                continue                                                   # the rim, laid with the cap
            dd = depth(x, z)
            if dd <= 1:
                w.set(x, h, z, *SPRUCE_PLANKS)
            elif c.kind == "keep":
                w.set(x, h, z, *((B.STAINED_CLAY, dye) if dd == 2 else (B.SANDSTONE, 2)))
            else:
                field.append((x, z))
        if field:
            sand(w, field, c.y, rng)
    # the inlay's beds, filling a piece's inside up to the plank band: one bed for a piece that is a rectangle of
    # cells, else one to each two cells by two of it
    if any(t == "inlay" for t in theme.values()):
        used = set()
        for (cx, cz) in sorted(only):
            c = cells[(cx, cz)]
            if c.kind != "flat" or theme[label[(cx, cz)]] != "inlay" or (cx, cz) in used:
                continue
            n = label[(cx, cz)]
            comp = [p for p, v in label.items() if v == n]
            xs, zs = [p[0] for p in comp], [p[1] for p in comp]
            rect = len(comp) == (max(xs) - min(xs) + 1) * (max(zs) - min(zs) + 1)
            if rect and all(p in only and cells[p].kind == "flat" for p in comp):
                block = comp
            else:
                block = [(cx, cz), (cx + 1, cz), (cx, cz + 1), (cx + 1, cz + 1)]
                if not all(b in label and label[b] == n and b not in used and b in only and cells[b].kind == "flat"
                           for b in block):
                    continue
            used |= set(block)
            inner = [(x, z) for bx, bz in block for x in range(bx * CELL, bx * CELL + CELL)
                     for z in range(bz * CELL, bz * CELL + CELL) if depth(x, z) >= 2]
            xs, zs = [p[0] for p in inner], [p[1] for p in inner]
            if inner and max(xs) - min(xs) >= 5 and max(zs) - min(zs) >= 5:
                bed(w, min(xs), min(zs), max(xs), max(zs), c.y, rng)


def _stacked(w, c, x0, z0, cells, T):
    """A deck at c.y over the underfloor at c.y - 3: spruce planks, the rim where the deck stands over lower
    ground, dark-oak posts at the cell's corners under it; the underfloor floored in spruce planks."""
    u = c.y - 3
    for i in range(CELL):
        for k in range(CELL):
            x, z = x0 + i, z0 + k
            w.set(x, u, z, *SPRUCE_PLANKS)
            out = [d for d, (dx, dz) in DIRS.items() if T.get((x + dx, z + dz), -1) < c.y]
            if out:
                w.set(x, c.y, z, B.SPRUCE_STAIRS, stair(OPP[out[0]], upside_down=True))
            else:
                w.set(x, c.y, z, *SPRUCE_PLANKS)
    for i, k in ((0, 0), (0, CELL - 1), (CELL - 1, 0), (CELL - 1, CELL - 1)):
        for y in range(u + 1, c.y):
            w.set(x0 + i, y, z0 + k, B.LOG2, 1)


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
