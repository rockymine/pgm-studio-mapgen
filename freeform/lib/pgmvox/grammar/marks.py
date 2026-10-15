"""Marks laid into a section's floor, and fills drawn from a floor field: what every style of the grammar shares.

A motif is motif(w, lot, rng, **params), laid over a lot's fill; a section names it with its params,
`motifs=(("word", (("text", "RED"), ("block", (B.WOOL, 14)))),)`, and a style that names no motif of that name
lays this one. Every mark is centred in the lot (its inside, the outline already off it) `margin` blocks in, and read standing on the lot's
side away from `up`: up "n" reads from the south, its letters' tops toward the north.

    arrow       a head and a shaft pointing d, as wide as the lot allows
    word        a word in facade.LETTERS, three by five each, `scale` blocks a pixel
    glyph       one of facade.GLYPHS, five by five
    bitmap      any rows of "#" and ".", top row first

`field(f)` makes a fill of a facade floor field f(cell) -> block or None: the field is laid over the lot's box and
kept to its columns, and `under` lies where the field answers None.
"""
from pgmvox.built import facade
from pgmvox.core.blocks import B


def _place(lot, rows, up, margin, scale):
    """The columns of a bitmap centred in a lot, its top toward `up`: [((x, z), set), ...] for every pixel."""
    x0, z0, x1, z1 = lot.box
    x0, z0, x1, z1 = x0 + margin, z0 + margin, x1 - margin, z1 - margin
    hgt, wid = len(rows) * scale, len(rows[0]) * scale
    across, along = (x1 - x0 + 1, z1 - z0 + 1) if up in "ns" else (z1 - z0 + 1, x1 - x0 + 1)
    if wid > across or hgt > along:
        return None
    a0 = (across - wid) // 2
    b0 = (along - hgt) // 2
    out = []
    for r in range(hgt):
        for c in range(wid):
            on = rows[r // scale][c // scale] == "#"
            i, j = a0 + c, b0 + r                                   # j counts from the top, i from the left
            x, z = {"n": (x0 + i, z0 + j), "s": (x1 - i, z1 - j),
                    "e": (x1 - j, z0 + i), "w": (x0 + j, z1 - i)}[up]
            out.append(((x, z), on))
    return out


def bitmap(w, lot, rng, rows, block, up="n", margin=0, scale=1, ground=None):
    """Rows of "#" laid in `block`, "." in `ground` (or left as the fill laid them); False when it does not fit."""
    cells = _place(lot, rows, up, margin, scale)
    if cells is None:
        return False
    keep = set(lot.cols)
    for (x, z), on in cells:
        if (x, z) not in keep:
            continue
        if on:
            w.set(x, lot.y, z, *block)
        elif ground is not None:
            w.set(x, lot.y, z, *ground)
    return True


def word(w, lot, rng, text, block, up="n", margin=0, scale=1, gap=1, ground=None):
    """A word in the three-by-five letters, read standing on the side away from `up`."""
    letters = [facade.LETTERS[c] for c in text.upper()]
    rows = ["".join(lt[r] + ("." * gap if k < len(letters) - 1 else "") for k, lt in enumerate(letters))
            for r in range(5)]
    return bitmap(w, lot, rng, rows, block, up, margin, scale, ground)


def glyph(w, lot, rng, name, block, up="n", margin=0, scale=1, ground=None):
    """One of the five-by-five glyphs."""
    return bitmap(w, lot, rng, facade.GLYPHS[name], block, up, margin, scale, ground)


def arrow(w, lot, rng, d="n", block=(B.WOOL, 14)):
    """A head and a shaft pointing d, one in from the lot's edge: the head's rows widen by two from the tip's one
    (or two) to the lot's width, the shaft a third of it, both centred."""
    x0, z0, x1, z1 = lot.box
    x0, z0, x1, z1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1
    across, length = (x1 - x0 + 1, z1 - z0 + 1) if d in "ns" else (z1 - z0 + 1, x1 - x0 + 1)
    tip = 1 if across % 2 else 2
    shaft = across - 2 * (across // 3)
    head = (across - tip) // 2 + 1                                   # rows of the head, the last as wide as the lot
    cols = set(lot.cols)
    for i in range(length):                                          # i rows back from the tip
        width = tip + 2 * i if i < head else shaft
        a0 = (across - width) // 2
        for j in range(a0, a0 + width):
            x, z = {"n": (x0 + j, z0 + i), "s": (x0 + j, z1 - i), "w": (x0 + i, z0 + j),
                    "e": (x1 - i, z0 + j)}[d]
            if (x, z) in cols:
                w.set(x, lot.y, z, *block)


def field(f, under=None, name=None):
    """A fill laying the floor field f over the lot's box, kept to its columns; `under` where f answers None (else
    the column is left as it was). It never declines."""
    def fill(w, lot, rng):
        x0, z0, x1, z1 = lot.box
        cx, cz, hw, hh = (x0 + x1) / 2, (z0 + z1) / 2, (x1 - x0) / 2, (z1 - z0) / 2
        for x, z in lot.cols:
            c = facade.Cell(x, z, x - cx, z - cz, hw, hh, min(x - x0, x1 - x, z - z0, z1 - z), x0, z0)
            b = f(c)
            if b is None:
                b = under
            if b is not None:
                w.set(x, lot.y, z, *b)
        return True
    if name:
        fill.__name__ = name
    return fill


def flight(tread, nosing, cheek=None):
    """A fill for a stepped section (its `tops`): every column its tread at its own top, and on every row before a
    rise a `nosing` stair, an id, rising toward the next tread; with `cheek`, the lot's two outer columns along the
    rise carry that block instead, a cheek stepping up beside the stairs."""
    from pgmvox.core.orient import stair
    from pgmvox.grammar.rules import DIRS

    def fill(w, lot, rng):
        g = lot.ground
        x0, z0, x1, z1 = lot.box
        ups = {}
        for x, z in lot.cols:
            h = g.top(x, z)
            ups[(x, z)] = [d for d, (dx, dz) in DIRS.items() if g.top(x + dx, z + dz) == h + 1]
        rise = next((u[0] for u in ups.values() if u), "n")
        lo, hi = (x0, x1) if rise in "ns" else (z0, z1)
        for (x, z), up in ups.items():
            h = g.top(x, z)
            w.set(x, h, z, *tread)
            if up:
                side = (x if rise in "ns" else z) in (lo, hi)
                if cheek is not None and side:
                    w.set(x, h + 1, z, *cheek)
                else:
                    w.set(x, h + 1, z, nosing, stair(up[0]))
        return True
    fill.__name__ = "flight"
    return fill


MOTIFS = {"arrow": arrow, "word": word, "glyph": glyph, "bitmap": bitmap}
