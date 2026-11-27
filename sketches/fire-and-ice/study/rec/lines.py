"""The author's terrain rebuilt the way the loft tool builds it: ordered lines, a mesh between each consecutive pair.

A piece is read as stations across it, and at each station its extent splits into intervals, one line each. A line
starts as its two ends and the author's markers near it, and takes a point wherever the curve through those strays
more than three quarters of a block from the piece. Stations go first where the markers are, then where the outline
bends, then where the surface between two lines strays from the piece. Consecutive lines are joined where they
overlap; where a piece forks, each arm is lofted onto its own stretch of the line it meets. A layer lying over the
main one, such as the free lofts covering a staircase, is split off and rebuilt the same way.
"""
import collections
import math
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))          # loft.py, terrain.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loft
from reconstruct import frame, to_frame, from_frame


def layers(cells, fr):
    """The main layer as (u, v) -> mean offset, and the cells of every layer lying off it."""
    grid = collections.defaultdict(list)
    for c in cells:
        u, v, w = to_frame(c, fr); grid[(round(u), round(v))].append((w, c))
    clusters = {}
    for key, items in grid.items():
        items.sort()
        groups = [[items[0]]]
        for item in items[1:]:
            if item[0] - groups[-1][-1][0] > 2.5: groups.append([item])
            else: groups[-1].append(item)
        clusters[key] = groups
    single = {k: sum(w for w, _ in g[0]) / len(g[0]) for k, g in clusters.items() if len(g) == 1}
    main, extra = {}, []
    for key, groups in clusters.items():
        if len(groups) == 1:
            main[key] = single[key]; continue
        near = [single[(key[0] + a, key[1] + b)] for a in range(-3, 4) for b in range(-3, 4) if (key[0] + a, key[1] + b) in single]
        ref = sorted(near)[len(near) // 2] if near else groups[0][0][0]
        best = min(groups, key=lambda g: abs(sum(w for w, _ in g) / len(g) - ref))
        main[key] = sum(w for w, _ in best) / len(best)
        for g in groups:
            if g is not best: extra += [c for _, c in g]
    return main, extra


def components(cells, minimum=8):
    left, out = set(cells), []
    while left:
        seed = left.pop(); comp, todo = [seed], [seed]
        while todo:
            p = todo.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        q = (p[0] + dx, p[1] + dy, p[2] + dz)
                        if q in left: left.remove(q); comp.append(q); todo.append(q)
        if len(comp) >= minimum: out.append(comp)
    return out


def joins(lines0, lines1):
    """Which lines on one station a loft carries on to on the next: each line to the one it overlaps most, and to
    any other it shares half its own length with, so a piece that forks keeps both arms and two arms side by side
    are never joined across the gap between them."""
    def overlap(l0, l1):
        return min(l0[-1][0], l1[-1][0]) - max(l0[0][0], l1[0][0])
    def span(l): return max(1.0, l[-1][0] - l[0][0])
    out = set()
    for i, l0 in enumerate(lines0):
        scores = [(overlap(l0, l1), j) for j, l1 in enumerate(lines1)]
        best = max(scores)
        if best[0] > -2: out.add((i, best[1]))
        out |= {(i, j) for o, j in scores if o >= 0.5 * min(span(l0), span(lines1[j]))}
    for j, l1 in enumerate(lines1):
        best = max((overlap(l0, l1), i) for i, l0 in enumerate(lines0))
        if best[0] > -2: out.add((best[1], j))
    return [(lines0[i], lines1[j]) for i, j in sorted(out)]


def shares(pairs):
    """Each join with the stretch of either line it covers: a line joined to one other is used whole, and a line
    where a piece forks is cut at the middle of each gap between its partners, so each arm lofts onto its own
    stretch of it rather than onto the whole of it."""
    def cut(line, partners):
        if len(partners) == 1: return {id(partners[0]): (line[0][0], line[-1][0])}
        partners = sorted(partners, key=lambda l: l[0][0])
        edges = [line[0][0]] + [(p[-1][0] + q[0][0]) / 2 for p, q in zip(partners, partners[1:])] + [line[-1][0]]
        edges = [min(max(e, line[0][0]), line[-1][0]) for e in edges]
        return {id(p): (edges[k], edges[k + 1]) for k, p in enumerate(partners)}
    by_line0, by_line1 = collections.defaultdict(list), collections.defaultdict(list)
    for l0, l1 in pairs: by_line0[id(l0)].append(l1); by_line1[id(l1)].append(l0)
    out = []
    for l0, l1 in pairs:
        r0 = cut(l0, by_line0[id(l0)])[id(l1)]
        r1 = cut(l1, by_line1[id(l1)])[id(l0)]
        if r0[1] - r0[0] > 0.1 or r1[1] - r1[0] > 0.1: out.append((l0, r0, l1, r1))
    return out


class Lofts:
    """One piece's lines in one orientation: `along` is the axis a line runs on, `across` the axis stations step on."""

    def __init__(self, surface, markers, along, spacing=5, pairing="arc"):
        self.along, self.spacing, self.pairing = along, spacing, pairing
        self.surface = {(k[along], k[1 - along]): w for k, w in surface.items()}      # (a, b) -> w
        self.markers = [((m[along], m[1 - along]), m[2]) for m in markers]
        self.by_b = collections.defaultdict(list)
        for (a, b) in self.surface: self.by_b[b].append(a)
        bs = sorted(self.by_b)
        self.bmin, self.bmax = bs[0], bs[-1]
        stations = {self.bmin, self.bmax}
        for b in sorted(round(b) for (a, b), w in self.markers):      # markers within two blocks share a line
            if self.bmin <= b <= self.bmax and all(abs(b - s) > 2 for s in stations): stations.add(b)
        self.stations = sorted(stations)
        self.from_markers = len(self.stations) - 2

    def intervals(self, b):
        found = sorted(self.by_b.get(b, ()))
        out = []
        for a in found:
            if out and a - out[-1][1] <= 3: out[-1][1] = a
            else: out.append([a, a])
        return out

    def height(self, a, b):
        """The piece's offset at (a, b): its own cell where it has one, the nearest of its row's cells otherwise."""
        key = (round(a), round(b))
        if key in self.surface: return self.surface[key]
        row = self.by_b.get(round(b), ())
        nearest = min(row, key=lambda x: abs(x - a), default=None)
        return self.surface[(nearest, round(b))] if nearest is not None else 0.0

    def line(self, b, a0, a1, tolerance=0.75):
        """One line across the interval: its two ends and the markers near it, then a point at a time where the curve
        through them strays furthest from the piece, until it strays nowhere by more than `tolerance`."""
        if a1 - a0 < 1:
            a0, a1 = a0 - 0.5, a1 + 0.5
        pts = {a0: self.height(a0, b), a1: self.height(a1, b)}
        for (am, bm), wm in self.markers:
            if abs(bm - b) <= 1.5 and a0 - 1 <= am <= a1 + 1 and all(abs(am - k) >= 1.5 for k in pts):
                pts[am] = wm
        row = [a for a in self.by_b.get(b, ()) if a0 <= a <= a1]
        while True:
            samples = loft.curve([(a, b, pts[a]) for a in sorted(pts)], step=0.5)
            def strays(a):
                nearest = min(samples, key=lambda p: abs(p[0] - a))
                return abs(nearest[2] - self.surface[(a, b)])
            free = [a for a in row if all(abs(a - k) >= 1 for k in pts)]
            worst = max(free, key=strays, default=None)
            if worst is None or strays(worst) <= tolerance: break
            pts[worst] = self.surface[(worst, b)]
        return [(a, b, pts[a]) for a in sorted(pts)]

    def strips(self):
        """Every pair of overlapping intervals on consecutive stations, as two lines to be joined."""
        rows = [(b, [self.line(b, a0, a1) for a0, a1 in self.intervals(b)]) for b in self.stations]
        rows = [(b, ls) for b, ls in rows if ls]
        pairs = []
        for (b0, lines0), (b1, lines1) in zip(rows, rows[1:]):
            pairs += shares(joins(lines0, lines1))
        return pairs, rows

    def edge_error(self, b):
        """How many of the piece's cells at station-free row `b` the strips either side of it miss or overreach,
        within a block: the measure of whether the lines' ends follow the edge there."""
        below = max((s for s in self.stations if s < b), default=None)
        above = min((s for s in self.stations if s > b), default=None)
        if below is None or above is None: return 0
        t = (b - below) / (above - below)
        covered = set()
        stand_in = lambda b_: [[(a0,), (a1,)] for a0, a1 in self.intervals(b_)]
        for l0, l1 in joins(stand_in(below), stand_in(above)):
            (a0,), (a1,) = l0; (c0,), (c1,) = l1
            lo, hi = a0 + (c0 - a0) * t, a1 + (c1 - a1) * t
            covered |= set(range(math.ceil(lo - 0.5), math.floor(hi + 0.5) + 1))
        actual = set(self.by_b.get(b, ()))
        miss = sum(1 for a in actual if not ({a - 1, a, a + 1} & covered))
        over = sum(1 for a in covered if not ({a - 1, a, a + 1} & actual))
        return miss + over

    def follow_edges(self, tolerance=2, budget=200):
        """Lines added where the outline bends: the row whose cells the strips get most wrong, until none is off by
        more than `tolerance` cells."""
        for _ in range(budget):
            worst = max((b for b in self.by_b if b not in self.stations), key=self.edge_error, default=None)
            if worst is None or self.edge_error(worst) <= tolerance: return
            self.stations = sorted(self.stations + [worst])

    def rungs(self, l0, r0, l1, r1):
        """The straight segments a strip between two lines is made of: points matched along each line's stretch
        `r0`, `r1` by the same share of its length (arc), or of its run along the axis (axis)."""
        c0, c1 = loft.curve(l0, step=0.3), loft.curve(l1, step=0.3)
        c0 = [p for p in c0 if r0[0] - 1e-6 <= p[0] <= r0[1] + 1e-6] or c0[:1]
        c1 = [p for p in c1 if r1[0] - 1e-6 <= p[0] <= r1[1] + 1e-6] or c1[:1]
        n = max(len(c0), len(c1), 2)
        if self.pairing == "arc":
            return list(zip(loft.resample(c0, n) if len(c0) > 1 else c0 * n, loft.resample(c1, n) if len(c1) > 1 else c1 * n))
        def at(samples, a):
            j = min(range(len(samples)), key=lambda k: abs(samples[k][0] - a)); return samples[j]
        return [(at(c0, r0[0] + (r0[1] - r0[0]) * k / (n - 1)), at(c1, r1[0] + (r1[1] - r1[0]) * k / (n - 1))) for k in range(n)]

    def sheet(self, step=0.5):
        """The lofted surface in the frame, as (a, b) -> mean offset over the samples landing in each cell."""
        acc = collections.defaultdict(list)
        pairs, _ = self.strips()
        for l0, r0, l1, r1 in pairs:
            for p, q in self.rungs(l0, r0, l1, r1):
                m = max(1, int(math.dist(p, q) / step))
                for k in range(m + 1):
                    t = k / m
                    acc[(round(p[0] + (q[0] - p[0]) * t), round(p[1] + (q[1] - p[1]) * t))].append(p[2] + (q[2] - p[2]) * t)
        return {key: sum(ws) / len(ws) for key, ws in acc.items()}

    def follow_heights(self, tolerance=1.0, allowed=2, budget=200):
        """Lines added where the surface between two lines strays from the piece: the row with the most cells more
        than `tolerance` off, until no row has more than `allowed` of them."""
        for _ in range(budget):
            sheet = self.sheet()
            bad = collections.Counter(b for (a, b), w in self.surface.items()
                                      if b not in self.stations and ((a, b) not in sheet or abs(sheet[(a, b)] - w) > tolerance))
            bad = [(n, b) for b, n in bad.items() if n > allowed]
            if not bad: return
            self.stations = sorted(self.stations + [max(bad)[1]])

    def to_uvw(self, a, b, w):
        return (a, b, w) if self.along == 0 else (b, a, w)

    def build(self, fr, window, step=0.35):
        out = set()
        pairs, _ = self.strips()
        for l0, r0, l1, r1 in pairs:
            for p, q in self.rungs(l0, r0, l1, r1):
                gap = math.dist(p, q); m = max(1, int(gap / step))
                for k in range(m + 1):
                    s = k / m
                    a, b, w = (p[0] + (q[0] - p[0]) * s, p[1] + (q[1] - p[1]) * s, p[2] + (q[2] - p[2]) * s)
                    u, v, w = self.to_uvw(a, b, w)
                    o = window[0]
                    while o <= window[1] + 1e-9:
                        x, y, z = from_frame(u, v, w + o, fr)
                        out.add((math.floor(x + 0.5), math.floor(y + 0.5), math.floor(z + 0.5)))
                        o += 0.5
        return out

    def count(self):
        pairs, rows = self.strips()
        lines = [l for _, ls in rows for l in ls]
        return len(lines), sum(len(l) for l in lines)


def near(c, s):
    return any((c[0] + a, c[1] + b, c[2] + e) in s for a in (-1, 0, 1) for b in (-1, 0, 1) for e in (-1, 0, 1))


def fit_lofts(cells, markers_world, goal=0.97, rounds=40, pairing="arc"):
    """The lines for one sheet: both orientations tried, stations added where the most blocks are missed."""
    cells = set(cells)
    fr = frame(list(cells))
    surface, extra = layers(cells, fr)
    main_cells = cells - set(extra)
    markers = [to_frame(p, fr) for p in markers_world]
    best = None
    for along in (0, 1):
        lofts = Lofts(surface, markers, along, pairing=pairing)
        lofts.follow_edges()
        lofts.edge_lines = len(lofts.stations) - 2 - lofts.from_markers
        lofts.follow_heights()
        lofts.height_lines = len(lofts.stations) - 2 - lofts.from_markers - lofts.edge_lines
        for _ in range(rounds):
            built = lofts.build(fr, (-0.25, 0.25))
            missed = [c for c in main_cells if not near(c, built)]
            surplus = [c for c in built if not near(c, cells)]
            recall = 1 - len(missed) / len(main_cells)
            precision = 1 - len(surplus) / max(1, len(built))
            if recall >= goal and precision >= goal: break
            by_b = collections.Counter()
            for c in missed + surplus:
                u, v, w = to_frame(c, fr); by_b[round((u, v)[1 - along])] += 1
            candidates = [b for b, _ in by_b.most_common() if b not in lofts.stations]
            if not candidates: break
            lofts.stations = sorted(lofts.stations + [candidates[0]])
        lines, points = lofts.count()
        fit = min(recall, precision)
        if best is None or (fit, -points) > (best[0], -best[3]):
            best = (fit, lofts, lines, points)
    recall, lofts, lines, points = best
    offsets = sorted(to_frame(c, fr)[2] - surface.get((round(to_frame(c, fr)[0]), round(to_frame(c, fr)[1])), 0) for c in main_cells)
    centre = offsets[len(offsets) // 2]
    window = max(((centre - w / 2, centre + w / 2) for w in (0.0, 0.5, 1.0, 1.5)),
                 key=lambda win: (lambda b: len(b & main_cells) / len(b | main_cells))(lofts.build(fr, win)))
    return {"frame": fr, "lofts": lofts, "window": window, "lines": lines, "points": points,
            "markers": len(markers), "extra": extra, "marker_lines": lofts.from_markers, "edge_lines": lofts.edge_lines, "height_lines": lofts.height_lines}
