# opus5, run 8 — a mountain range, and Sandcaster II

The board's author looked at the first Sandcaster in the studio's 3-D preview and said two things: it has
scattered holes through the surface, and it is extremely flat — *I asked for mountains and am seeing none of
that*. The instruction was to work out how to get a range on a small board first, keep the first Sandcaster
as it is, and then combine the range with the underground in a second version on an **elderwold-shaped**
layout, because *the many cut out areas make not for the best dtm experience — it has to be an open playing
ground*.

Both halves of the diagnosis were right, and both had a cause I had written down wrongly.

## What the flatness was

**A relief mark is a constraint.** It pins the ground at a height, honoured exactly, with no falloff of any
kind. That reads as a modelling detail and it decides what terrain can be authored at all: a `point` summit
at `h 47, r 8` does not build a mountain, it builds a **drum** — a flat disc eight blocks across standing on
a twenty-block sheer wall — because nothing between the disc and the ground round it is under any statement
except the relaxation, and the relaxation has one cell to make the transition in. A `line` mark with
per-vertex heights is the same object stretched: a ridge-shaped wall with a flat top.

I built exactly that first, on `showcase/19-mountain-range`, and it produced correct numbers over the wrong
landform: `low 11 · high 55 · symErr 0`, gate open, and a 3-D preview of five white-capped oil drums.

The instrument is the **push**. It takes a drawn ring and lifts the *solved* surface inside it, and three of
its fields are the shape:

- **`amounts`** — one lift per ring vertex, interpolated along the arc and wrapped, so the crest falls along
  the ring the way it was drawn. A massif's spine is six numbers.
- **`crown`** — how much higher the middle stands than the edge, where the middle is the ring's own **medial
  axis**: a point on a round ring (a dome), a line on a long one (a crest). Its record default is **0**, so a
  push authored without touching it is a plateau. This one field is the difference between a mountain and a
  mesa.
- **`falloff`** — the skirt, measured from the ring across the land, and the number that decides how much of
  the board the range eats. At 20 on a 90-block board the two skirts met in the middle and there was no
  valley; at 11 the flat ground runs 33 blocks wide the length of the board.

**And the second half is the marks not written.** The first Sandcaster pinned all four of its regions with
`area` marks at their own heights — which run 7's report listed under *what worked first time*, because no
seam appeared anywhere. It is true that no seam appeared. It is also why the board is flat: a board with a
mark on every region is a table with bumps on it however tall the bumps are, and the bumps were 3–7 blocks
on a 400-block board. `19-mountain-range` pins four things — the coast, the dale floor, the goal's shelf and
the spawn's apron, every one of them ground a player walks — and the flanks carry no mark at all.

Two smaller things fell out of the same experiment. An `area` mark's ring is a **shape**, so written as a
rectangle it builds a mesa with four sheer sides, visible in the heightmap as a literal square; the same mark
on a nine-vertex lobed ring is indistinguishable from ground. And `reach: 0` matters, because a finite reach
pulls the flanks back toward the base between two distant marks and the range becomes a row of hills.

## What the holes were

A brush stroke reaching past the land is the only add on that column, so it builds a **speck of bedrock
standing over the void**. Before clamping the strokes into the board's tiered outline, `/coverage` on
`19-mountain-range` reported `141 cells at (-24, 91), 364 blocks from used ground` — a disconnected island
made of paint. Every stroke on both new boards is now clamped, and placed off a spine rather than typed as a
coordinate, so moving a massif moves its paint with it.

## Sandcaster II

`maps/opus5-sandcaster-ii`, 100 × 400. One landmass — six nested rectangles mirrored, compiled to a single
shape with a wandering coast, no chasm and no gap link. Two massifs, two spurs and two corries a side, drawn
as six pushes. Four marks. Three landscapes painted at region scale with the detail strokes read against
them, because paint scopes to the smallest shape covering a cell. The workings under the middle of it: a
corridor, four bays, a drained pool, a cistern chamber holding the second goal, two light wells and two
ramped cuttings.

`score 1.369 · symErr 0 · low 21 · high 76 · relief 55 · gate OPEN · 8.9% dead · nothing declined`, and
`render/traversability` answers one component with all four goal markers connected. `review/opus5-sandcaster-ii.md`
is the record.

Three findings paid for by this board:

**`LN2` measures a chain of collinear, land-joined pieces.** Six nested rectangles all the same width made
one 120-block chain against a band of 25–110. Giving three of them three different widths broke the chain and
cost nothing, and it is also the elderwold silhouette.

**Among the shapes of one layer, the taller override-add wins the column — not the later one.** An end wall
drawn as one rectangle across the mouth of a ramp is 15 courses where the ramp is 7, so the wall wins every
column they share and the way down ends in solid rock. `(−8, 60)` read solid `y0..21` with no air in it.
Fixed by drawing each end wall in halves either side of the ramp, and the same shape had shipped on the first
Sandcaster — its spec is fixed and its world rebuilt.

**A cheap filter beats hand-tuned coordinates.** Five rules can decline a prop and none is visible in a plan
view: `DR-SITE`, `OB19`, `DR-KEEP`, `DR-CLAIM`, `DR-ROAD`. Four rounds of moving copses by hand each traded
one decline for another. Stating where the woods are and letting a distance filter decide which stands are
actually planted got to *nothing declined* in one round.

## What I got wrong, and how long it took to see

**I wrote the wrong explanation for `SK11` in run 7 and shipped it.** Its complaint on the corridor floor was
recorded as a quirk of the check — "`SK11` appears to ask its question inside a layer" — and part of it was a
real plug that a single column read would have found. The review is corrected.

**I called the region hold marks a success in run 7.** They are the reason the board the author called flat is
flat. The measurement (no seam) was right and the conclusion drawn from it was too narrow.

**I chased a corrupted build for four runs.** One run of Sandcaster II exported a completely flat world while
`relief/read` reported a range: the stored sketch's ground island had been renamed, so the relief keyed on
`team` matched no island. Re-running from clean produced the correct board and the corruption has not
recurred; what it cost was two hours of reading the rasterizer for a bug that was not there. The cheap check
I did not do first is the one that settled it in the end — post the same layout to a fresh map and read a
column.

**The 3-D preview draws a stacked board flat**, which is what the author was looking at. The world has the
range and so does the payload the preview itself posts. Filed against the studio as `TS29` rather than worked
around here.

## Open gameplay questions

Whether 8.9% dead ground is acceptable when all of it is mountain flank — scenery a player looks at rather
than walks — or whether a range should carry a route over it. Not derivable from the corpus or the code.
