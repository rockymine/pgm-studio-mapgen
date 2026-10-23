"""Hollowstack's laid passages, from pgmvox's segment kit: the Undercroft in stone on two levels and the Workings in
timber on one, each a few fixed pieces (rooms, stairs, wells, ports onto the chasm) joined by a network the search
writes, and the throats that carry a port's opening out through the rock to the chasm's face.

    undercroft(w, rng)     the dungeon: the vault, a library, a prison, a crypt, a hall, two stairs, three wells
    workings(w, rng)       the mine: the pithead, the keep well up into the yard, two galleries to the chasm, the
                           gallery to the descent cave
    descent(w)             the winding cave from the Workings down into the Underwood's back
"""
import layout as L
from pgmvox import B
from pgmvox.built import segments as S
from pgmvox.volume import under as U


def grid_of(spec):
    return S.Grid(spec["x0"], spec["y0"], spec["z0"], L.CELL, L.STOREY)


def _design(spec, plan, need, levels, rng, loops=0.12, spurs=0.5, avoid=()):
    """Join the plan's fixed pieces: on each level a network through the free cells reaching every needed cell."""
    taken = plan.taken()
    for l in levels:
        free = {(i, j, l) for i in range(spec["cols"]) for j in range(spec["rows"])} - taken - set(avoid)
        want = {c for c in need if c[2] == l}
        links = S.network(free | want, want, rng, loops=loops, spurs=spurs)
        missing = want - {c for e in links for c in e}
        assert not missing or len(want) == 1, f"level {l}: the network does not reach {sorted(missing)}"
        plan.links_of(tuple(e) for e in links)
    return plan


def _wells_avoid(g, spec, levels):
    """The cells a well from the Tops would pass through, which a network keeps out of."""
    out = set()
    for wx, wz, wr in (L.LIGHT_WELL, L.PLUNGE):
        for i in range(spec["cols"]):
            for j in range(spec["rows"]):
                x, _, z = g.corner(i, j, 0)
                if abs(x + 2 - wx) < 2 + wr + 1 and abs(z + 2 - wz) < 2 + wr + 1:
                    out |= {(i, j, l) for l in levels}
    return out


def undercroft(w, rng):
    g = grid_of(L.UNDERCROFT)
    p = S.Plan()
    vi0, vj0, vi1, vj1 = L.VAULT
    p.room("gallery", 0, 2, 2, 5, 0, "hall", tall=2)            # the arcade hall on the chasm, where attackers land
    p.room("vault", vi0, vj0, vi1, vj1, 0, "vault", tall=2)      # the wool's room, at the back by the keep well
    p.room("crypt", 6, 5, 7, 6, 0, "crypt")
    p.room("prison", 7, 0, 8, 1, 0, "prison")
    p.room("library", 4, 0, 5, 1, 1, "library")
    p.room("hall", 10, 1, 11, 2, 1, "hall")
    p.stair((4, 3, 0), "e")                                  # up into (5, 3, 1)
    p.stair((9, 3, 0), "w")                                  # up into (8, 3, 1)
    gi, gj = L.GATEHOUSE
    p.shaft(gi, gj, 1, 3, "e")                               # up into the Underwood's court
    di, dj = L.DEEP_SHAFT
    p.shaft(di, dj, -2, 0, "e")                              # down into the Deep's grotto
    ki, kj = L.KEEP_WELL
    top = L.WORKINGS_LEVEL + 3
    p.shaft(ki, kj, 1, top, "e")                             # the keep well: the Undercroft to the yard
    p.port((ki, kj, L.WORKINGS_LEVEL), "w", "open")          # through the Workings on its way
    pl = L.POSTERN_LEVEL                                     # the postern: from the well west into the Underwood
    for i in range(ki - 3, ki):
        p.link((i, kj, pl), (i + 1, kj, pl))
    p.port((ki - 3, kj, pl), "w", "arch")
    p.port((ki, kj, top), "w", "open")                       # out into the yard from the well house
    for j in range(2, 6):
        for l in (0, 1):
            p.port((0, j, l), "w", "open")                   # the gallery's arcade onto the chasm
    p.port((0, 0, 1), "w", "arch")                           # balconies onto the chasm
    p.port((0, 7, 1), "w", "arch")
    p.port((gi, gj, 3), "w", "arch")                         # the gatehouse's doors into the court
    p.port((gi, gj, 3), "n", "arch")
    p.port((gi, gj, 3), "s", "arch")
    p.port((di, dj, -2), "w", "open")                        # into the grotto
    doors = [((3, 3, 0), (2, 3, 0)), ((3, 4, 0), (2, 4, 0)), ((3, 3, 0), (4, 3, 0)),     # the gallery, a stair's foot
             ((10, 3, 0), (9, 3, 0)), ((7, 4, 0), (7, 5, 0)), ((7, 2, 0), (7, 1, 0)), ((9, 6, 0), (10, 6, 0)),
             ((13, 6, 0), (13, 7, 0)), ((13, 6, 0), (12, 6, 0)),
             ((3, 2, 1), (2, 2, 1)), ((6, 3, 1), (5, 3, 1)), ((7, 3, 1), (8, 3, 1)), ((6, 3, 1), (6, 4, 1)),
             ((6, 1, 1), (5, 1, 1)), ((12, 2, 1), (11, 2, 1)), ((1, 0, 1), (0, 0, 1)), ((1, 7, 1), (0, 7, 1)),
             ((12, 3, 1), (13, 3, 1)), ((11, 4, 1), (11, 5, 1))]
    need = {a for a, _ in doors}
    _design(L.UNDERCROFT, p, need, (0, 1), rng)
    for a, b in doors:
        p.link(a, b)
    laid = S.lay(w, g, p, S.DUNGEON, rng)
    throats(w, g, p)
    return g, p, laid


def workings(w, rng):
    g = grid_of(L.WORKINGS)
    p = S.Plan()
    ki, kj = L.KEEP_WELL
    p.room("pithead", 8, 5, 9, 6, 0, "hall")
    p.port((0, 1, 0), "w", "open")
    p.port((0, 6, 0), "w", "open")
    p.port((4, 7, 0), "s", "open")                           # to the descent cave
    p.port((ki - 1, kj, 0), "e", "open")                     # into the keep well, laid with the Undercroft
    doors = [((8, 4, 0), (8, 5, 0)), ((10, 6, 0), (9, 6, 0))]
    need = {a for a, _ in doors} | {(0, 1, 0), (0, 6, 0), (4, 7, 0), (ki - 1, kj, 0)}
    avoid = _wells_avoid(g, L.WORKINGS, (0,)) | {(ki, kj, 0)}
    _design(L.WORKINGS, p, need, (0,), rng, loops=0.1, spurs=0.6, avoid=avoid)
    for a, b in doors:
        p.link(a, b)
    laid = S.lay(w, g, p, S.MINE, rng)
    throats(w, g, p)
    return g, p, laid


def throats(w, g, p, reach=14):
    """Carry each port facing west out through the rock until it meets open air (the chasm, a cavern): the
    opening's three by four continued that way, its floor kept under it, for at most `reach` blocks."""
    for c, d, kind in p.ports:
        if d != "w":
            continue
        x, y, z = g.corner(*c)
        for zz in range(z + 1, z + L.CELL - 1):
            for xx in range(x - 1, x - 1 - reach, -1):
                if all(w.id(xx, y + dy, zz) == B.AIR for dy in range(1, 5)):
                    break
                for dy in range(1, 5):
                    w.set(xx, y + dy, zz, B.AIR)
                if w.id(xx, y, zz) == B.AIR:
                    w.set(xx, y, zz, B.STONE, 0)


def descent(w):
    """The winding cave from the Workings' south gallery down into the Underwood's back terrace."""
    g = grid_of(L.WORKINGS)
    x, y, z = g.corner(4, 7, 0)
    pts = U.wander([(x + 2, y + 1, z + L.CELL), (x + 6, y - 2, z + 6), (x + 12, y - 5, z + 5),
                    (x + 22, y - 10, z + 1), (x + 28, y - 15, z - 5), (x + 24, y - 20, z - 11), (x + 19, y - 22, z - 13)],
                   (2.0, 2.6), swing=1.4, seed=51)
    U.tunnel(w, pts)
    return pts
