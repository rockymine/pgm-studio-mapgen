"""mid-8 — Gletscherzungen am Eissee.

The author's ground already leans across the middle: at its west end the built half's floor comes down off the
plateau at y 20 while the turned half lies at y 15, and at the east end it is the other way round. The middle takes
that lean and finishes it. Each team's slope runs on into the middle as a glacier tongue (a convex spur, crest
y 20 -> 17), and the two tongues end, from opposite sides, in a shallow frozen lake at the pivot (bottom y 11,
floor y 15-16 around it). Flat floor runs along both edges and past both ends of the lake.

Built in the frame of the cut line: s along it (from the pivot), a across it (negative on the built half). The
height field H(s, a) is 180-degree symmetric by construction, H(s, a) == H(-s, -a); the lines sample it, the lofts
carry the surface. Only the built half (a <= 0) is lofted; kit.symmetric adds the turned copy.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import kit  # noqa: E402

kit.set_shift(3, 8)                     # ~8.5 blocks wider, almost purely across the cut line (along drift -0.1)
GAP = kit.middle_gap()
CUT, NORMAL = kit.CUT, kit.NORMAL


def xz(s, a):
    return (kit.PIVOT[0] + s * CUT[0] + a * NORMAL[0], kit.PIVOT[1] + s * CUT[1] + a * NORMAL[1])


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- the built half's facing edge, read off the map
HALF_TOP = kit.tops(kit.existing())
_edge = []                              # (s, a, top) of every built-half column touching the gap
for (x, z), y in HALF_TOP.items():
    if kit.across(x, z) < 0 and any((x + dx, z + dz) in GAP for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        _edge.append((kit.along(x, z), kit.across(x, z), y))


def edge_a(s):
    near = [e for e in _edge if abs(e[0] - s) <= 2.0 and e[1] < -8]
    return max(e[1] for e in near) if near else -16.0


def edge_h(s):
    if s < -35: return 20.0                                    # the plateau's foot at the west corner
    near = [e for e in _edge if abs(e[0] - s) <= 2.0 and e[1] < -8]
    return sum(e[2] for e in near) / len(near) if near else 16.0


FLOOR = 15.4                            # top block y 15, the author's valley floor
BOTTOM = 11.3                           # top block y 11, the lake's ice
LAKE_HALF = 7.0                         # the lake is a capsule along the cut line: centre segment s = -7 .. 7
LAKE_R = 3.5                            # flat ice out to 3.5 from the segment
LAKE_SLOPE = 9.0                        # shore width: ~4 down over 9


def floor(s, a):
    """Flat floor meeting both edges at their own height (6-block run-out from each edge)."""
    ea, eb = edge_a(s), -edge_a(-s)
    ha, hb = edge_h(s), edge_h(-s)
    wa = 1 - smooth((a - ea) / 6.0)
    wb = 1 - smooth((eb - a) / 6.0)
    return FLOOR + (ha - FLOOR) * wa + (hb - FLOOR) * wb


ROOT, TIP = (-42.0, -13.0), (-16.0, -6.0)   # the built half's tongue: crest from the plateau's foot to its snout


def tongue(s, a):
    """The built half's glacier tongue: convex cross-section, crest falling y 20.2 -> 17.4, rounded snout."""
    vx, va = TIP[0] - ROOT[0], TIP[1] - ROOT[1]
    t = ((s - ROOT[0]) * vx + (a - ROOT[1]) * va) / (vx * vx + va * va)
    tc = min(1.0, max(0.0, t))
    d = math.hypot(s - (ROOT[0] + tc * vx), a - (ROOT[1] + tc * va))
    crest = 20.2 - 2.8 * tc
    width = 9.5 - 2.5 * tc
    u = d / width
    return FLOOR + (crest - FLOOR) * (1 - u * u) ** 2 if u < 1 else -99.0


def H(s, a):
    h = max(floor(s, a), tongue(s, a), tongue(-s, -a))
    d = math.hypot(max(0.0, abs(s) - LAKE_HALF), a) - LAKE_R
    return BOTTOM + (h - BOTTOM) * smooth(d / LAKE_SLOPE) if d < LAKE_SLOPE else h


def P(s, a):
    x, z = xz(s, a)
    return (round(x, 2), round(H(s, a), 2), round(z, 2))


RIM = LAKE_R + LAKE_SLOPE


def rim_a(s):
    """The lake's shore on the built half at station s (a <= 0), or None outside it."""
    o = max(0.0, abs(s) - LAKE_HALF)
    return -math.sqrt(RIM * RIM - o * o) if o < RIM else None


# ---------------------------------------------------------------- station lines, cut against the span polygon
SPAN = [(kit.along(x, z), kit.across(x, z)) for x, z in kit.span()]   # the middle's polygon in the (s, a) frame


def span_interval(s):
    """The built-half part [a_lo, a_hi] of the span polygon on station s (a_hi <= 0), or None."""
    cross = []
    for (s1, a1), (s2, a2) in zip(SPAN, SPAN[1:] + SPAN[:1]):
        if (s1 <= s < s2) or (s2 <= s < s1):
            cross.append(a1 + (a2 - a1) * (s - s1) / (s2 - s1))
    cross.sort()
    parts = [(cross[k], min(cross[k + 1], 0.0)) for k in range(0, len(cross) - 1, 2) if cross[k] < 0]
    return max(parts, key=lambda p: p[1] - p[0]) if parts else None


def cut_end(sign):
    """Where the span's end line crosses the cut line, on the side of `sign`."""
    lo, hi = (0.0, 60.0)
    for _ in range(50):                                        # bisect: last station whose interval reaches a = 0
        mid = (lo + hi) / 2
        iv = span_interval(sign * mid)
        if iv and iv[1] > -1e-6: lo = mid
        else: hi = mid
    return sign * lo


S_CUT = cut_end(1)                      # +-S_CUT: the span's two end lines meet the cut line (symmetric pair)
CORNER = (kit.along(*kit.LANE_CORNER), kit.across(*kit.LANE_CORNER))


def station_line(s, n=6):
    a0, a1 = span_interval(s)
    r = rim_a(s)
    if r is not None and r < -0.01: a1 = r                    # ends on the lake shore
    if s > S_CUT - 1e-6 and a1 > -1e-6: a1 = 0.0
    near = [span_interval(s + k * 0.5) for k in range(-5, 6)]
    a0 = max(a0 - 1.5, min([a0] + [iv[0] for iv in near if iv]))   # the deepest notch of the front nearby, <= 1.5 out
    return [P(s, a0 + (a1 - a0) * k / (n - 1)) for k in range(n)]


SYM = [0.0, 4.5, 9.0, 13.5, LAKE_HALF + RIM, 23.0, 28.0, 33.0, 37.0, S_CUT]
STATIONS = sorted({-v for v in SYM} | set(SYM)) + [44.0]      # symmetric where a line ends on the cut line
west_tip = [P(-S_CUT, 0.0)]                                    # the west end line meets the cut: a single point
east_tip = [P(CORNER[0] - 0.4, CORNER[1] + 0.4)]               # the lane corner, where the east end line starts

SPLIT = -(LAKE_HALF + RIM)              # where the tongue meets the lake shore on the cut line
tongue_lines = [west_tip] + [station_line(s) for s in STATIONS if -S_CUT < s <= SPLIT]
floor_lines = [station_line(s) for s in STATIONS if s >= SPLIT] + [east_tip]


# ---------------------------------------------------------------- the lake: shore arcs down to the ice, then the cut line
def arc(r, n_cap=2):
    """Half of a capsule outline of radius r on the built half, from (-7 - r, 0) round to (7 + r, 0)."""
    pts = []
    for k in range(n_cap + 1):                                 # west cap, 180 -> 270 degrees
        th = math.pi + (math.pi / 2) * k / n_cap
        pts.append((-LAKE_HALF + r * math.cos(th), r * math.sin(th)))
    pts.append((0.0, -r))
    for k in range(n_cap + 1):                                 # east cap, 270 -> 360 degrees
        th = 1.5 * math.pi + (math.pi / 2) * k / n_cap
        pts.append((LAKE_HALF + r * math.cos(th), r * math.sin(th)))
    return [P(s, a) for s, a in pts]


lake_lines = [arc(RIM), arc(LAKE_R + 6.0), arc(LAKE_R + 2.5), arc(LAKE_R),
              [P(-LAKE_HALF, 0.0), P(0.0, 0.0), P(LAKE_HALF, 0.0)]]     # the last line lies on the cut: self-symmetric

pieces = [
    {"name": "Gletscherzunge", "wool": 4,
     "note": "Gelb: der Hangfuss jeder Seite läuft als flache, gewölbte Zunge in die Mitte aus (Kamm y 20 -> 17) "
             "und endet am Eissee.",
     "lofts": [tongue_lines]},
    {"name": "Talboden", "wool": 8,
     "note": "Hellgrau: ebener Boden y 15-16 entlang beider Kanten und an beiden Enden des Sees vorbei.",
     "lofts": [floor_lines]},
    {"name": "Eissee", "wool": 9,
     "note": "Cyan, neue Bedeutung: gefrorener See in der Mitte, Eisfläche y 11, Ufer 4 Blöcke tief auf 9 Blöcke Breite.",
     "lofts": [lake_lines]},
]
for piece in pieces:
    piece["blocks"] = set().union(*(kit.loft_blocks(l) for l in piece["lofts"]))

pieces = kit.symmetric(pieces)

# one surface per column: the lake owns the shore it shares with the floor, the tongue the station line it shares;
# blocks outside the middle's columns are clipped off
owner = {}
for index in (2, 0, 1):
    for x, y, z in pieces[index]["blocks"]:
        owner.setdefault((x, z), index)
DROPPED = 0
for index, piece in enumerate(pieces):
    keep = {c for c in piece["blocks"] if (c[0], c[2]) in GAP and owner[(c[0], c[2])] == index}
    DROPPED += sum(1 for c in piece["blocks"] if (c[0], c[2]) not in GAP)
    piece["blocks"] = keep

if __name__ == "__main__":
    allb = set().union(*(p["blocks"] for p in pieces))
    turned = {kit.turn(c) for c in allb}
    print("symmetric:", turned == allb)
    res = kit.checks(allb)
    print(res)
    print('gate', kit.gate('middle', pieces, True))
    print('dropped at the edge', DROPPED)
    area = len(GAP)
    for p in pieces:
        pts = sum(len(l) for ls in p["lofts"] for l in ls)
        lines = sum(len(ls) for ls in p["lofts"])
        print(p["name"], p["wool"], "lofts", len(p["lofts"]), "lines", lines, "points", pts, "blocks", len(p["blocks"]))
    total = sum(len(l) for p in pieces for ls in p["lofts"] for l in ls)
    print("points", total, "area", area, "per 100:", round(100 * total / area, 1))
    title = "Gletscherzungen am Eissee"
    summary = ("Jede Seite schickt ihren Hangfuss als flache Gletscherzunge in die Mitte, und beide Zungen enden "
               "von entgegengesetzten Seiten in einem flachen, gefrorenen See am Drehpunkt. Wer die Mitte quert, "
               "geht über ebenen Talboden an den Seeenden vorbei, steigt sanft durch die Senke oder nimmt die Zunge "
               "als erhöhten Weg zum gegnerischen Wollausgang.")
    print(kit.write("mid-8", "middle", title, summary, pieces, True))
    col = {}
    for p in pieces:
        for c in p["blocks"]: col[c] = p["wool"]
    kit.render(col, os.path.join(HERE, "r_q0.png"), q=0)
    kit.render(col, os.path.join(HERE, "r_q2.png"), q=2)
