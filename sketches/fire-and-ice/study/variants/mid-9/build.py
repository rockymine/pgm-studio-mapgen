"""mid-9 — Pingo-Furt: a shallow trough between the two valley floors, with one ice dome (pingo) standing in it on
either side of the centre, so the crossing between the halves bends round two pieces of large cover.

Built on the built half's side, then turned with kit.symmetric. Shift (3, 8): the turned half moves almost straight
across the line between the halves (8.5 blocks), not along it, so the gap keeps its skew and gains room for a
channel on both sides of each dome.
"""
import json
import math
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kit

kit.set_shift(3, 8)
HERE = os.path.dirname(os.path.abspath(__file__))

GAP = kit.middle_gap()
SPAN = kit.span()
HALF_TOP = kit.tops(kit.existing())          # the built half only: where a line meets the author's front edge
TROUGH = 14.0                                 # height of the trough along the line between the halves
REACH = 1.2                                   # how far a line's end runs past the span boundary, under the ground beside it


def at(along, across, y):
    """(x, y, z) of a point given in the frame of the line between the halves."""
    x = kit.PIVOT[0] + along * kit.CUT[0] + across * kit.NORMAL[0]
    z = kit.PIVOT[1] + along * kit.CUT[1] + across * kit.NORMAL[1]
    return (round(x, 2), round(y, 2), round(z, 2))


def inside(along, across):
    x, _, z = at(along, across, 0)
    return kit._inside(SPAN, x, z)


def reach(along):
    """The stretch of the built half's side of the span at `along`, as (outer across, inner across), each end on the
    span boundary: the inner end is the line between the halves where the span reaches it, else the boundary."""
    ks = [-k / 4 for k in range(0, 160)]
    hits = [a for a in ks if inside(along, a)]
    if not hits: return None
    inner = hits[0]
    outer = inner
    for a in ks:
        if a > inner: continue
        if not inside(along, a): break
        outer = a
    return outer, inner


def ground(along, across, fallback):
    """Top of the author's ground at or just beyond (along, across), looking up to 3 blocks further out."""
    for k in range(0, 13):
        x, _, z = at(along, across - k / 4, 0)
        c = (math.floor(x + 0.5), math.floor(z + 0.5))
        if c in HALF_TOP and c not in GAP: return HALF_TOP[c]
    return fallback


# ---------------------------------------------------------------- the floor: one line across the half every 4 blocks, every 2 in the narrow ends
floor_lines = []
for along in [-40.8, -40] + list(range(-36, 37, 4)) + [40, 42, 44, 46, 46.8]:
    r = reach(along)
    if r is None: continue
    outer, inner = r
    top = ground(along, outer - REACH, None)
    if top is None: top = TROUGH + 1                  # the span's slanted end, no author ground beside it
    end = inner + (REACH if inner < 0 else 0)
    end_y = TROUGH if inner == 0 else TROUGH + 0.5
    width = end - outer
    floor_lines.append([at(along, outer - REACH, top),
                        at(along, outer + width * 0.25, TROUGH + (top - TROUGH) * 0.5),   # falls off the edge,
                        at(along, outer + width * 0.65, TROUGH + (top - TROUGH) * 0.12),  # then lies almost flat
                        at(along, end, end_y)])


floor_blocks = {b for b in kit.loft_blocks(floor_lines) if (b[0], b[2]) in GAP}
floor_piece = {"name": "Talsohle", "wool": 8, "lofts": [floor_lines], "blocks": floor_blocks,
               "note": "Flache Mulde zwischen den beiden Talböden, tiefste Linie y 14 auf der Mittellinie."}
floor_full = kit.symmetric([floor_piece])[0]["blocks"]
FLOOR_TOP = kit.tops(floor_full)


# ---------------------------------------------------------------- the pingo: rings round a dome, summit hollow
P_ALONG, P_ACROSS = 18.0, -3.0               # its centre; the copy stands at (-18, +3)
TILT = math.radians(18)                      # long axis turned off the line between the halves


def ring(along_semi, across_semi, y, count, lean=0.0, sink=None):
    """A closed ring of `count` points round the pingo's centre, moved `lean` blocks toward the far end."""
    pts = []
    for i in range(count):
        t = 2 * math.pi * i / count
        u, v = along_semi * math.cos(t), across_semi * math.sin(t)
        a = P_ALONG + lean + u * math.cos(TILT) - v * math.sin(TILT)
        c = P_ACROSS + u * math.sin(TILT) + v * math.cos(TILT)
        if sink is not None:                    # on the floor: take the floor's own height there
            x, _, z = at(a, c, 0)
            yy = FLOOR_TOP.get((math.floor(x + 0.5), math.floor(z + 0.5)), TROUGH) - sink
        else:
            yy = y
        pts.append(at(a, c, yy))
    return pts + [pts[0]]


pingo_lines = [
    ring(13.0, 10.0, None, 13, lean=-1.5, sink=0.2),  # foot, on the floor; its long tail runs toward the centre
    ring(9.0, 7.0, 17.6, 11, lean=0.0),                # shoulder
    ring(5.5, 4.4, 21.0, 8, lean=1.0),                # upper flank
    ring(2.8, 2.3, 22.4, 6, lean=1.5),                # rim of the summit hollow
    [at(P_ALONG + 1.5, P_ACROSS, 21.3)],              # floor of the hollow
]
pingo_blocks = {b for b in kit.loft_blocks(pingo_lines) if (b[0], b[2]) in GAP}
pingo_piece = {"name": "Pingo", "wool": 3, "lofts": [pingo_lines], "blocks": pingo_blocks,
               "note": "Eisgefüllter Hügel, 8 Blöcke über der Mulde, mit flacher Kuhle oben; der Gegenhügel steht gedreht."}
floor_piece["blocks"] = floor_blocks - pingo_blocks

pieces = kit.symmetric([floor_piece, pingo_piece])
# the copies of both pieces meet the originals; keep each block in one piece only
pieces[0]["blocks"] -= pieces[1]["blocks"]

if __name__ == "__main__":
    allb = set().union(*(p["blocks"] for p in pieces))
    res = kit.checks(allb)
    print(json.dumps(res))
    sym = all(kit.turn(b) in allb for b in allb)
    print("symmetric", sym, "blocks", len(allb), "gap", len(GAP))
    for p in pieces:
        lines = sum(len(ls) for ls in p["lofts"]); pts = sum(len(l) for ls in p["lofts"] for l in ls)
        print(p["name"], "lofts", len(p["lofts"]), "lines", lines, "points", pts, "blocks", len(p["blocks"]))
    surf = len(kit.tops(allb))
    pts = sum(len(l) for p in pieces for ls in p["lofts"] for l in ls)
    print("surface", surf, "points/100", round(100 * pts / surf, 1))
    top = kit.tops(allb)
    pk = max(top.items(), key=lambda kv: kv[1]); print("highest", pk, "lowest", min(top.values()))
    kit.write("mid-9", "middle", "Pingo-Furt",
              "Eine flache Mulde verbindet die beiden Talböden ohne Bruch; ihre tiefste Linie liegt auf y 14 genau "
              "zwischen den Hälften. In ihr steht auf jeder Seite der Mitte ein eisgefüllter Hügel, acht Blöcke "
              "hoch, um den man von zwei Seiten herumläuft. Wer die Mitte quert, geht eine S-Kurve zwischen den beiden "
              "Hügeln und hat dabei immer Deckung gegen eine Seite.",
              pieces, absolute=True)
    if "render" in sys.argv:
        new = {b: p["wool"] for p in pieces for b in p["blocks"]}
        kit.render(new, HERE + "/render_q0.png", q=0)
        kit.render(new, HERE + "/render_q2.png", q=2)
        kit.render(new, HERE + "/crop_q1.png", q=1, scale=5, box=(10, 115, 0, 40, 45, 140))
        kit.render(new, HERE + "/crop_q3.png", q=3, scale=5, box=(10, 115, 0, 40, 45, 140))
