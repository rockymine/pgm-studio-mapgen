"""mid-7: Eismulde — a shallow frozen basin between the two plazas.

The two halves' front floors (y 15-16, rising to 20 where each plateau's foot reaches the gap) flow down with no
break into a lens-shaped flat basin floor at y 11 centred on the pivot, and the basin closes again toward both ends
of the middle, so its floor never runs out to the map's edge. Built on the built half (across < 0) as lines across
the gap, ordered along it, and turned by kit.symmetric.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import kit  # noqa: E402

SHIFT = (4, 10)                 # widens the middle by about 10.7 blocks, almost purely across the cut line
kit.set_shift(*SHIFT)

FLOOR = 11.0                    # basin floor
FLOOR_HALF = 0.20               # half-width of the flat floor, as a fraction of the gap's width
FLOOR_TIP = 24.0                # the flat floor's lens closes at |along| = 24
DEPTH_FULL = 22.0               # the basin is at full depth for |along| <= 22 ...
DEPTH_END = 37.0                # ... and has risen back to the plazas' level at |along| = 37
STEP = 3.0                      # along-spacing of the cross lines
OVERHANG = 1.5                  # lines reach this far past the gap's edge, so the clip leaves no column open

gap = kit.middle_gap()
old = kit.existing()
old_full = kit.existing(full=True)
old_top = kit.tops(old_full)
half_cols = {(x, z) for x, y, z in old}


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- the gap's edges, as functions of along
lo = {}
for x, z in gap:
    u = round(kit.along(x, z)); v = kit.across(x, z)
    lo[u] = min(lo.get(u, 99.0), v)
U_MIN, U_MAX = min(lo), max(lo)
for k in range(U_MIN, U_MAX + 1):          # an along-bin no column rounds into takes its neighbours' mean
    if k not in lo:
        a = max(j for j in lo if j < k); b = min(j for j in lo if j > k)
        lo[k] = lo[a] + (lo[b] - lo[a]) * (k - a) / (b - a)


def edge_lo(u):
    """The gap's lower (built-side) bound in across, interpolated and lightly smoothed."""
    def raw(k):
        k = min(U_MAX, max(U_MIN, k)); return lo[k]
    k0 = math.floor(u); f = u - k0
    vals = [(raw(k0 + d) * (1 - f) + raw(k0 + 1 + d) * f) for d in (-1, 0, 1)]
    return (vals[0] + 2 * vals[1] + vals[2]) / 4 - 0.5


def edge_hi(u):
    return -edge_lo(-u)


# heights of the built half's ground along its front edge
samples = []
for x, z in gap:
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (x + dx, z + dz)
        if n in half_cols and n not in gap:
            samples.append((kit.along(*n), old_top[n]))
S_LO = min(s[0] for s in samples)                 # the built edge's west end; beyond it the bound is the map's edge
CORNER_U = kit.along(*kit.LANE_CORNER)


def height_lo(u):
    """Height of the existing ground along the gap's lower bound; along the map-edge part, a straight run from the
    built edge's west end to the turned copy of the lane corner."""
    if u < S_LO:
        h0 = height_lo(S_LO); h1 = height_lo(CORNER_U)
        return h1 + (h0 - h1) * (u + CORNER_U) / (S_LO + CORNER_U)
    near = [(abs(su - u), h) for su, h in samples if abs(su - u) <= 2.5]
    if not near: near = sorted((abs(su - u), h) for su, h in samples)[:3]
    w = [(1 / (0.5 + d), h) for d, h in near]
    return sum(a * h for a, h in w) / sum(a for a, _ in w)


def height_hi(u):
    return height_lo(-u)


# ---------------------------------------------------------------- the basin as a height field, point-symmetric
def floor_half(u):
    if abs(u) >= FLOOR_TIP: return 0.0
    return FLOOR_HALF * math.sqrt(1 - (u / FLOOR_TIP) ** 2)


def depth_weight(u):
    return 1 - smooth((abs(u) - DEPTH_FULL) / (DEPTH_END - DEPTH_FULL))


def height(u, v):
    a, b = edge_lo(u), edge_hi(u)
    t = (v - a) / max(1.0, b - a)
    tc = min(1.0, max(0.0, t))
    ground = height_lo(u) * (1 - smooth(tc)) + height_hi(u) * smooth(tc)
    half = floor_half(u)
    off = abs(tc - 0.5)
    dip = 1.0 if off <= half else smooth((0.5 - off) / (0.5 - half))
    return ground - (ground - FLOOR) * dip * depth_weight(u)


def point(u, v):
    x = kit.PIVOT[0] + u * kit.CUT[0] + v * kit.NORMAL[0]
    z = kit.PIVOT[1] + u * kit.CUT[1] + v * kit.NORMAL[1]
    return (round(x, 3), round(height(u, v), 3), round(z, 3))


# ---------------------------------------------------------------- lines across the gap, ordered along it
def u_where_lo_is_zero():
    u = U_MIN
    while edge_lo(u) > 0: u += 0.05
    return u


u_tip = u_where_lo_is_zero()
grid = [k * STEP for k in range(-int(46 // STEP), int(46 // STEP) + 1)]
us = sorted(set([round(u, 3) for u in grid] + [round(u_tip, 3), round(-u_tip, 3)]))
us = [u for u in us if edge_lo(u) <= 0 and u <= U_MAX + 1]
us.append(U_MAX + 1.0)          # the east tip, past the lane corner, cut back to the gap by the clip

slope_lines, floor_lines = [], []
for u in us:
    a = edge_lo(u) - OVERHANG
    end = min(0.0, edge_hi(u) + OVERHANG) if edge_hi(u) < 0 else 0.0
    half = floor_half(u)
    if half > 0:
        b, c = edge_lo(u), edge_hi(u)
        foot = b + (0.5 - half) * (c - b)
        foot = min(foot, 0.0)
        slope_lines.append([point(u, a + (foot - a) * f) for f in (0, 0.38, 0.7, 1)])
        floor_lines.append([point(u, foot + (0 - foot) * f) for f in (0, 0.5, 1)])
    else:
        slope_lines.append([point(u, a + (end - a) * f) for f in (0, 0.3, 0.6, 1)])
        if abs(u) == FLOOR_TIP: floor_lines.append([point(u, 0.0)])

floor_lofts = [floor_lines]
slope_lofts = [slope_lines]


def blocks_of(lofts):
    out = set()
    for lines in lofts: out |= kit.loft_blocks(lines, thickness=2)
    return {c for c in out if (c[0], c[2]) in gap}


floor_blocks = blocks_of(floor_lofts)
slope_blocks = blocks_of(slope_lofts) - floor_blocks

pieces = [
    {"name": "Muldenboden", "wool": 8, "lofts": floor_lofts, "blocks": floor_blocks,
     "note": "Der flache Boden der Mulde auf y 11, eine Linse um den Drehpunkt."},
    {"name": "Muldenhang", "wool": 4, "lofts": slope_lofts, "blocks": slope_blocks,
     "note": "Sanfte Hänge vom Platzboden (y 15-16, am Plateaufuß 20) hinab in die Mulde; zu beiden Enden schließt sich die Mulde wieder."},
]
full = kit.symmetric(pieces)
full[1]["blocks"] = full[1]["blocks"] - full[0]["blocks"]     # a block both pieces claim stays with the floor

if __name__ == "__main__":
    allb = set()
    for p in full: allb |= p["blocks"]
    res = kit.checks(allb)
    print(json.dumps(res))
    sym = all(kit.turn(c) in allb for c in allb)
    print("symmetric", sym, "blocks", len(allb), "gap", len(gap))
    area = len({(x, z) for x, y, z in allb})
    for p in full:
        npts = sum(len(l) for ls in p["lofts"] for l in ls)
        nl = sum(len(ls) for ls in p["lofts"])
        cols = len({(x, z) for x, y, z in p["blocks"]})
        print(p["name"], "lofts", len(p["lofts"]), "lines", nl, "points", npts, "blocks", len(p["blocks"]),
              "cols", cols, "pts/100", round(100 * npts / max(1, cols), 1))
    tot = sum(sum(len(l) for ls in p["lofts"] for l in ls) for p in full)
    print("total points", tot, "surface", area, "per 100:", round(100 * tot / area, 1))
    top = kit.tops(allb)
    print("floor min/max", min(top.values()), max(top.values()))
    kit.write("mid-7", "middle", "Die Eismulde",
              "Die Platzböden beider Hälften fließen ohne Kante in eine flache Mulde, deren Boden auf y 11 als Linse "
              "um den Drehpunkt liegt; zu beiden Enden steigt sie wieder auf Platzhöhe, sodass ihr Boden nirgends ins "
              "Leere läuft. Wer die Mitte zu Fuß quert, steigt vier bis fünf Blöcke hinab und wieder hinauf, offen "
              "einsehbar von beiden Rändern; der kürzere, sichere Weg ist die Brücke darüber.",
              full, absolute=True)
    if "--render" in sys.argv:
        new = {}
        for p in full:
            for c in p["blocks"]: new[c] = p["wool"]
        kit.render(new, os.path.join(HERE, "render_q1.png"), q=1, box=(5, 120, -5, 45, 40, 145), scale=4)
        kit.render(new, os.path.join(HERE, "render_q3.png"), q=3, box=(5, 120, -5, 45, 40, 145), scale=4)
