"""The Claywork style for pgmvox.grammar: grey stone and white clay, the team's colour inlaid. A board on bedrock,
its faces deep and dressed, its floors cut into sections each laid in its own pattern.

    STYLE = clay.style(dye=14, rng=r, faced=lambda x, z: ...)     # faced: a column whose face shows the base
    grammar.lay(w, ground, STYLE, face_of=...)

    the face        twelve courses from the rim: stone brick, its foot in polished andesite; a bay every section
                    side, centred on it, of two chiseled pilasters round a panel sunk one block, the team's clay at its
                    back with a quartz diamond on it; a shallow face keeps its plain courses
    the flank       the plain courses alone, for a flight's sides, whose top changes every tread
    the body        stone through with andesite and gravel, two of bedrock, then on a face the team's band and a
                    lattice of obsidian and black wool to the floor of the world; block 36 at y 0
    the outline     stone brick where the ground falls, polished andesite between sections
    the fills       checker (three-by-three paces of a level's pair), squares (rings of diorite round clay, in stone
                    grout, inside a band of double slab), paving (bands across the section's short side), inlay
                    (rings of diorite and stone round a clay field), plate (polished diorite framed in stone brick, for an arrow), flight
                    (a stepped section: a lip behind each rise, a runner of clay up its middle, a nosing of stairs)
    the motifs      arrow: a head and a shaft in the team's wool on a plate, one in from its frame
"""
from . import grammar as G
from .blocks import B
from .orient import stair

CLAY, STONE, DSLAB, SMOOTH = (B.CLAY, 0), (B.STONE, 0), (B.DSLAB, 0), (B.DSLAB, 8)
BRICK, CHISELED, ANDESITE, DIORITE = (B.STONEBRICK, 0), (B.STONEBRICK, 3), (B.STONE, 6), (B.STONE, 4)
DEPTH = 12                                       # a face's courses: the rim and eleven under it
PAIRS = {"front": (CLAY, STONE), "apron": (CLAY, STONE), "hub": (STONE, CLAY), "wing": (STONE, CLAY),
         "rostrum": (DSLAB, STONE), "walk": (DSLAB, STONE), "spawn": (DSLAB, CLAY), "terrace": (DSLAB, CLAY),
         "kiln": (SMOOTH, CLAY), "under": (BRICK, (B.STONEBRICK, 2)), "stone": (ANDESITE, ANDESITE)}
PANEL = 6                                        # a bay: a pilaster, a panel six wide, a pilaster
DIAMOND = {(a, b) for a in range(PANEL) for b in range(5) if abs(a - (PANEL - 1) / 2) + abs(b - 2) <= 1.5}


def _key(lot):
    return (lot.section.name or "").split("-")[0]


def _ring(lot, x, z):
    """How far in from the lot's own box a column lies: 0 its outer ring."""
    x0, z0, x1, z1 = lot.box
    return min(x - x0, x1 - x, z - z0, z1 - z)


def squares(n, tile=4):
    """One axis of the squares across a span of n: 'm' margin, 'g' grout, 'r' a square's ring, 'c' its middle;
    as many whole squares as fit with the margins equal, so the row reads the same from either end."""
    k = max(0, (n + 1) // (tile + 1))
    while k > 0 and (n - (k * (tile + 1) - 1)) % 2:
        k -= 1
    used = k * (tile + 1) - 1 if k else 0
    left = (n - used) // 2
    out = ["m"] * n
    for t in range(k):
        for j in range(tile):
            out[left + t * (tile + 1) + j] = "r" if j in (0, tile - 1) else "c"
        if t < k - 1:
            out[left + t * (tile + 1) + tile] = "g"
    return out


def style(dye=14, rng=None, faced=None):
    """Claywork's blocks for the grammar, in the team's `dye`; `faced(x, z)` says whether a column stands on a face
    (its body shows the team's band and the lattice). Course blocks with a little wear are drawn from `rng`."""
    import random
    r = rng or random.Random(0)
    team = (B.STAINED_CLAY, dye)

    def worn(inward):
        return B.STONEBRICK, 2 if r.random() < 0.08 else 0

    plain = [BRICK] + [worn] * 8 + [ANDESITE] * 3
    pilaster = [BRICK, BRICK, CHISELED] + [BRICK] * 5 + [CHISELED] + [ANDESITE] * 3

    def panel(pos):
        col = pos - 1
        return [BRICK, BRICK, BRICK] + [G.Sunk((B.QUARTZ, 1) if (col, d) in DIAMOND else team) for d in range(5)] + \
            [BRICK] + [ANDESITE] * 3

    # a bay is laid whole or not at all: its panel six wide and a pilaster of plain stone either side, eight
    # columns of face at one height, every one with the panel's depth of air before it
    face = G.Face(plain, G.Accent(PANEL + 2, frame=pilaster, inner=panel, every=1, min_air=9, align="section"),
                  floor=1)
    flank = G.Face(plain, floor=1)

    def body(w, x, z, h):
        for y in range(h - DEPTH + 1, h):
            c = r.random()
            w.set(x, y, z, *((B.STONE, 5) if c < 0.12 else (B.GRAVEL, 0) if c < 0.15 else STONE))
        base = h - DEPTH
        for y in range(1, base + 1):
            w.set(x, y, z, B.BEDROCK)
        stripe = base - 2
        if faced and faced(x, z) and stripe >= 1:
            w.set(x, stripe, z, *team)                               # the team's band, flush with the face
            for y in range(1, stripe):                               # the lattice under it
                u = x + z
                if (u + y) % 8 == 0:
                    w.set(x, y, z, B.OBSIDIAN)
                elif (u - y) % 8 == 0:
                    w.set(x, y, z, B.WOOL, 15)
        w.set(x, 0, z, 36)

    def checker(w, lot, rng):
        a, b = PAIRS.get(_key(lot), (STONE, CLAY))
        x0, z0, _, _ = lot.box
        for x, z in lot.cols:
            w.set(x, lot.y, z, *(a if ((x - x0) // 3 + (z - z0) // 3) % 2 == 0 else b))
        return True

    def square_fill(w, lot, rng):
        x0, z0, x1, z1 = lot.box
        sx, sz = lot.size
        if min(sx, sz) < 6:
            return False
        ax, az = squares(sx - 2), squares(sz - 2)
        for x, z in lot.cols:
            if _ring(lot, x, z) == 0:
                w.set(x, lot.y, z, *DSLAB)
                continue
            a, b = ax[x - x0 - 1], az[z - z0 - 1]
            blk = DSLAB if "m" in (a, b) else STONE if "g" in (a, b) else DIORITE if "r" in (a, b) else CLAY
            w.set(x, lot.y, z, *blk)
        return True

    def paving(w, lot, rng):
        x0, z0, x1, z1 = lot.box
        sx, sz = lot.size
        across_x = sx <= sz                                          # the bands run across the short side
        for x, z in lot.cols:
            if _ring(lot, x, z) == 0:
                w.set(x, lot.y, z, *DIORITE)
                continue
            t = (z - z0) if across_x else (x - x0)
            w.set(x, lot.y, z, *(SMOOTH if t % 3 else STONE))
        return True

    def inlay(w, lot, rng):
        if not lot.is_rect or min(lot.size) < 5:
            return False
        for x, z in lot.cols:
            d = _ring(lot, x, z)
            w.set(x, lot.y, z, *(DIORITE if d == 0 else STONE if d == 1 else CLAY if d % 2 == 0 else SMOOTH))
        return True

    def plate(w, lot, rng):
        for x, z in lot.cols:
            w.set(x, lot.y, z, *(BRICK if _ring(lot, x, z) == 0 else DIORITE))
        return True

    def flat(w, lot, rng):
        for x, z in lot.cols:
            w.set(x, lot.y, z, *SMOOTH)
        return True

    def flight(w, lot, rng):
        g = lot.ground
        x0, z0, x1, z1 = lot.box
        rise = next((t[5:] for t in lot.section.tags if t.startswith("rise-")), "n")
        lo, hi = (x0, x1) if rise in "ns" else (z0, z1)
        third = (hi - lo + 1) / 3
        for x, z in lot.cols:
            h = g.top(x, z)
            across = x if rise in "ns" else z
            up = [d for d, (dx, dz) in G.DIRS.items() if g.top(x + dx, z + dz) == h + 1]
            down = [d for d, (dx, dz) in G.DIRS.items() if g.top(x + dx, z + dz) == h - 1 and (x + dx, z + dz) in
                    g.owner and g.owner[(x + dx, z + dz)] == lot.index]
            if lo + third <= across < hi + 1 - third:                 # the runner, the team's at each rise
                w.set(x, h, z, *(team if up else CLAY))
            else:
                w.set(x, h, z, *(SMOOTH if down else BRICK))
            if up:
                w.set(x, h + 1, z, B.STONEBRICK_STAIRS, stair(up[0]))      # the nosing, before each rise
        return True

    def arrow(w, lot, rng, d="n"):
        """A head and a shaft on the lot's plate, one in from its frame, pointing d, in the team's wool: the head
        rows widen by two from the tip's one (or two) to the plate's width, the shaft a third of it, both centred."""
        x0, z0, x1, z1 = lot.box
        x0, z0, x1, z1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1
        across, length = (x1 - x0 + 1, z1 - z0 + 1) if d in "ns" else (z1 - z0 + 1, x1 - x0 + 1)
        tip = 1 if across % 2 else 2
        shaft = across - 2 * (across // 3)
        head = (across - tip) // 2 + 1                               # rows of the head, the last as wide as the lot
        cols = set(lot.cols)
        for i in range(length):                                      # i rows back from the tip
            width = tip + 2 * i if i < head else shaft
            a0 = (across - width) // 2
            for j in range(a0, a0 + width):
                x, z = {"n": (x0 + j, z0 + i), "s": (x0 + j, z1 - i), "w": (x0 + i, z0 + j),
                        "e": (x1 - i, z0 + j)}[d]
                if (x, z) in cols:
                    w.set(x, lot.y, z, B.WOOL, dye)

    return G.Style(
        "claywork",
        body=body,
        faces={"edge": face, "flank": flank},
        seam=ANDESITE,
        fills={"checker": checker, "squares": square_fill, "paving": paving, "inlay": inlay, "plate": plate,
               "flat": flat, "flight": flight},
        choose=lambda sec, lot: ["squares", "paving", "flat"],
        motifs={"arrow": arrow},
        params={"dye": dye})
