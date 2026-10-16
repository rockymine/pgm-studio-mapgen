"""Thawline's sketch: the plan drawn and annotated before anything is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import sys

import checks
import plan as P
from pgmvox.read.sketch import MapPanel, SectionPanel, Sheet

FROST, EMBER = (90, 170, 230), (235, 120, 40)
R = P.build()
rows, routes = checks.measure()
EMBER_HALF = lambda x, z: z >= 0                                      # noqa: E731


def markers(m):
    for o in P.objectives().items:
        mk = o.marker()
        if not mk:
            continue
        team = getattr(o, "team", None)
        colour = FROST if team == "frost-team" else EMBER if team == "ember-team" else (220, 190, 60)
        m.marker(mk[0], mk[1], mk[2], colour)


S = Sheet("Thawline - the plan")
m = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=6, title="THE BOARD",
          legend="green ground, grey too steep, blue water; number: floor height; S spawn, C core, M monument; "
                 "Ember's half (south) drawn paler; the dark band is the Thawline, crossed by building")
m.raster(R, P.COLOURS, image_half=EMBER_HALF)
m.heights(R, kinds=["ground"], min_cells=40, both=False)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=12)
for name, pts in P.land.ROADS.items():
    m.line(pts, (120, 95, 60), 2, both=True)
m.zone(P.RIFT, (200, 70, 30), "dots", step=3)
for name, _, top, d, rim, steps in P.flights():
    x, y, z = steps[len(steps) // 2]
    m.callout(x, z, f"{name}, {top} down to {steps[-1][1]}", dx=34, dz=18)
m.callout(P.CULVERT[1][0], P.CULVERT[1][1], "the Culvert: under the rim to the Kettle's floor", dx=-40, dz=30)
m.callout(-55, -55, "the Crag Path, up to 60 over the Heart", dx=40, dz=-40)
m.callout(0, 4, "the Stack: island at 44, gap 5 to each lip", dx=60, dz=24)
markers(m)

r = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=6, title="THE ROUTES",
          legend="each team's cheapest walk: blue Frost to its own goals, orange Ember to Frost's (across the rift "
                 "by building); Ember's walks to its own goals are the images")
r.raster(R, P.COLOURS, image_half=EMBER_HALF)
r.dim(0.5)
for name, path in routes.items():
    cells = [c[:2] for c in path]
    r.route(cells, FROST if name.startswith("frost") else EMBER, 3)
markers(r)
S.row(m, r)

top = SectionPanel(P.Z_MIN, P.Z_MAX, 8, 90, scale=5, title="ALONG THE BOARD",
                   legend="a section at x 0, true scale, Frost's back at the left: the Glacier, Rimehall's terrace, "
                          "the field, the Thawline and the Stack, Ember's half")
top.raster(R, "z", 0, P.COLOURS)
top.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
top.level(P.LAVA_Y, f"lava at {P.LAVA_Y}", colour=(235, 120, 40))
top.callout(-84, P.land.SPAWN_Y + 1, "Rimehall 53", dx=10, dy=-20)
top.callout(0, P.land.STACK_Y + 1, "the Stack 44", dx=10, dy=-20)
across = SectionPanel(P.X_MIN, P.X_MAX, 30, 70, scale=5, title="ACROSS THE GOALS",
                      legend="a section at z -55, true scale: Hoarcrag, the Kettle under the Heart, the field, "
                             "Lantern Green, the beck, the hamlet")
across.raster(R, "x", -55, P.COLOURS)
across.callout(-36, P.CORE_BOX.y1, "the Heart hangs 8 over the Kettle's floor", dx=10, dy=-24)
across.callout(31, P.LANTERN_BOX.y1, "the Lantern, 4 over the green", dx=10, dy=-24)
S.row(top, across)
S.table(rows, width=m.img.width * 2 + 16)
S.save(sys.argv[1])
