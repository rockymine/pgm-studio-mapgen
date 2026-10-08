"""Drop's sketch: the course from above with every link drawn from take-off to where the fall comes down, the
course unrolled as a true-scale section, and the audit against its targets.

    python3 sketch.py renders/00-plan-sketch.png
"""
import sys

from plan import COLOURS, HEALTH, KILL_Y, build
from pgmvox.sketch import TEAM, MapPanel, SectionPanel, Sheet

HOW = {"walk": (90, 90, 90), "step off": (40, 150, 60), "run off": (220, 140, 30), "sprint jump": (200, 40, 40)}
C = build()
R = C.raster(list(COLOURS))
rows = C.audit(HEALTH)

m = MapPanel(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="THE COURSE",
             legend="numbers: steps; arrows: take-off to landing")
m.raster(R, COLOURS)
m.heights(R, size=10)
for r in rows:
    colour = HOW.get(r["how"], (255, 0, 255))
    m.line([r["take_off"], r["lands"]], colour, 2, arrow=True)
    if r["damage"]:
        m.label(r["lands"][0] + (3 if r["lands"][0] >= 0 else -3), r["lands"][1], f"-{r['damage']}",
                (200, 40, 40), 10)
for p in C.pieces:                                   # each step's number beside its piece, out of the heights' way
    if p.side != "image":
        x0, z0 = min(x for x, _ in p.cells), min(z for _, z in p.cells)
        m.marker(x0 - 2, z0, str(p.step + 1), TEAM["neutral"], r=7)

main = [p for p in C.pieces if p.side != "image"]
pts = [p.centre() for p in sorted(main, key=lambda p: p.step)]
length = int(sum(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 for a, b in zip(pts, pts[1:])))
s = SectionPanel(0, length, KILL_Y - 2, 128, scale=4, title="THE FALL", legend="unrolled down the left way")
s.along(R, pts, COLOURS, depth=3)
s.level(KILL_Y, f"kill below y {KILL_Y}")
acc = 0.0
for k, p in enumerate(sorted(main, key=lambda p: p.step)):
    if k:
        a, b = pts[k - 1], pts[k]
        acc += ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    s.callout(acc, p.y + 1, f"{p.step + 1} {p.name} {p.y}", dx=8, dy=-12, size=10)

legend = ";  ".join(f"{k}" for k in HOW)
S = Sheet("Drop - the plan")
S.row(m, s)
S.table([(f"{sum(r['how'] is None for r in rows)}", "links nothing clears", "none", not any(r["how"] is None for r in rows)),
         (f"{sum(r['lethal'] for r in rows)}", f"lethal links at {HEALTH} health", "none", not any(r["lethal"] for r in rows)),
         (f"{sum(not r['on_piece'] for r in rows if r['how'])}", "landings off the piece", "none",
          all(r["on_piece"] for r in rows if r["how"])),
         (f"{max(r['damage'] for r in rows)}", "the worst fall's damage", f"under {HEALTH // 2}",
          max(r["damage"] for r in rows) < HEALTH // 2),
         f"arrow colours: grey walk, green step off, orange run off, red sprint jump"],
        width=m.img.width + s.img.width + 16)
S.save(sys.argv[1])
