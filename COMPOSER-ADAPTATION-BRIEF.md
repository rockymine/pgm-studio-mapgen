# Composer adaptation brief

A composed board is a **suggestion**, not a plan. This brief is what the repository's author stated about
that gap, what was measured off the running composer to confirm it, and what an authoring agent is
therefore expected to do with a board it pulls off `GET /api/compose`.

It **overrides one line of `AUTHORING-BRIEF.md`** — *"Do not author from a composed board"* — for this run
and this run only. The reason that line exists is the fifteen boards that looked like each other, and the
answer here is not to avoid the composer but to refuse its output as a finished thing.

---

## 1. What the composer is for, and where it stops

**What it buys.** The composer knows how a CTW board is put together: a hub with a spawn hung off it, one
or two wool approaches hanging off the hub's real free surface, a frontline fronting it, a mid band between
the two fanned images with a row of stepping stones in it, and a land budget that keeps a wool board about
a third land. That arrangement is
the thing that is hard to invent and easy to get wrong, and a board drawn from scratch that ignores it
comes out illogical in ways no gate catches. **Take the arrangement.**

**Where it stops.** Every one of these was stated by the author and every one is visible in the documents:

| The composer does not | So the board arrives |
|---|---|
| vary the crossing's ground | the mid now carries a row of up to three stones astride the axis, funded from the units' own land — but the row is one lateral line at one depth, so there is no tiered island, no staggered pair and no stone off the band's own centre line |
| place defence walls | `"walls": []`, always. A defence wall is authored, never composed |
| state any elevation | no piece carries a `surface`; the whole board is flat at `globals.surface` 9 |
| draw anything but rectangles | every piece is an axis-aligned cell rect; there is no curve, no spur, no taper anywhere in the document |
| model an intra-team build zone | exactly **one** zone, the mid band. No encased pad between a team's own islands, no defender-egress bridge |
| carry layers | the plan tier has no storeys at all. No bottom lane, no top lane, no tunnel, no undercroft |
| make four-team boards | `GET /api/compose` answers **400** for `rot_90` and for `teams=4` |
| balance its own wools | see below — this is the one that bites |

And the one sentence that matters more than the table: **it emits a plan, not a layout.** The plan is where
the board's *arrangement* lives. Everything that makes a place — the shape of the ground, the second storey,
the edge that is not a straight line, the wall, the island — is downstream of it and is yours.

## 2. The lopsided wool, measured

This is the author's observation and it is real. On a two-wool board the two wools are routinely **not**
equidistant from the spawn that has to attack them. Straight-line cell distance from the attacking (enemy)
spawn to each wool room, off boards pinned from the live composer:

| Request | seed | wool-a → enemy spawn | wool-b → enemy spawn | worst ratio |
|---|---|---|---|---|
| p20 `rot_180` | 0 | 138 blocks | 94 blocks | **1.47×** |
| p20 `rot_180` | 1 | 132 | 98 | **1.35×** |
| p20 `rot_180` | 2 | 142 | 93 | **1.53×** |
| p30 `rot_180` | 0 | 138 | 99 | **1.39×** |
| p30 `rot_180` | 3 | 129 | 100 | **1.29×** |
| p20 `rot_180` | 3 | 127 | 118 | 1.08× (this one is fine) |

The shape of the fault is always the same: **wool-a is seated deep behind the hub at the far end of the
board, wool-b is a short spur off the hub's flank near the front line.** One wool is a raid and the other is
a walk-in. `GO1`'s band does not catch it — it is measured per goal against that goal's own spawn, and each
of them passes on its own.

**Fixing it is adaptation work, not a nudge.** Moving the near wool further out, moving the deep wool in,
re-hanging one of them off a different face of the hub, giving the near one a wall and the far one a
shortcut — all legitimate. What is not legitimate is shipping the 1.5× and not mentioning it.
`GET /api/map/{slug}/plan/flow` is the read that says what the board asks of each side, in prose, off the
plan alone — run it before and after.

## 3. Four teams are reachable — the composer is what refuses, not the studio

Measured, on this branch, against the running API:

```
plan-p20-rot_180-s0.json  with  globals.symmetry  "rot_180" → "rot_90"
POST /api/plan/compile    → 200, no warnings, no findings
POST /api/plan/evaluate   → score 0.024, valid true, no warnings, no hard term firing
```

The plan tier takes `rot_90` and fans the authored unit into four images; `Symmetry.Order("rot_90")` is 4.
What refuses four teams is `GET /api/compose`, at the endpoint, before composition. So a four-team board is
**an adaptation of a composed unit**, not something that has to be drawn from nothing.

Two things go with it. The authored unit has to actually fit a quadrant — a unit 75 cells long fanned four
ways will collide with its own images, so the unit is reshaped before the symmetry is flipped, not after.
And **destroy objectives are order-2 only**: a `rot_90` board is CTW and cannot carry a destroyable or a core.

## 4. What to do with the board you pulled

The composer gives a direction. These are the instruments that turn a direction into a place. Reach for
them by name; every one of them is documented and none of them is new.

**Deform the footprint.** A compiled rectangle is reshaped one point at a time.
`PATCH …/sketch/shapes/{id}/vertices/{index}` moves one vertex and leaves every other exactly where it was,
`POST …/vertices {"after": n}` adds one, and `DELETE` takes one out; a spec states them as `editShapes`, an
ordered list per shape replayed before any bend.

**`bendShapes` is the roughener.** It moves every cut point at once, so `side: out|in|both` decides whether
the outline bloats, holds its footprint or wanders.

Widen an approach, taper a spur, eat a bite out of a hub flank, make one edge read as a coast.

**Do not add a second shape on top to enlarge the first, and do not `subtract` into it to shrink it.** That
is the move that produces a board nobody can read.

**Cut with `subtract`, and cut in the plan with `buffer`.** A `subtract` removes ground entirely and is the
instrument for a channel or a chasm. No relief mark of any kind cuts a hole. At the plan tier the `buffer`
role declares a void the compiler would have declared anyway, and it is how a hole is made by *arrangement*.

**Add the mid the composer did not.** `zones` takes more than one entry. A centre island is a `piece` seated
in the mid band with build zone either side of it; stepping stones are the same idea at a smaller grain.
A `water-lane` zone is closed at the first tick and opens 45 minutes in, which is a second crossing that
arrives late — it can never be the connection the lint reads a board as joined by.

**Add the intra-team build zone.** This is the thing `CT4` calls a **team transient-link** and `BZ5` calls
the **defender-egress bridge**: a build region every interfacing component of which touches only *one*
team's islands — the encased pad between a team's own islands, the bridge off the back of the spawn. It is
measured, as the `team-stepping-count` term under `CT4`, band **[0, 2]**. The composer models none; a board
that chops a piece off its own team's ground and bridges it back has one. It is a lane a defender owns and
an attacker cannot flank, and it changes how a team rotates between its two wools.

**Add the wall.** `walls: [{"a": "<piece>", "b": "<piece>"}]` marks an interface that carries a pre-built
approach wall — bedrock, two thick, three courses, across the full interface width, stamped on the attack
side. It is an error on a pair that shares no land interface (`PL11`) and on the wool room's own interface
(`PL13`) — the device belongs an approach out, around 15 blocks from the room.

**Add the second dimension.** `addLayers` is `[{id, name, base_y, shapes, groups, below?}]`: the storeys a
plan cannot state. A tunnel, an underpass, a bottom lane, a deck over a lower street, a bridge a raider
walks out along are all of them this.

**The stack is written bottom-up and the painter walks it in document order.** A storey listed after one
that stands over it finds no stone left to paint. An undercroft goes *before* the compiled ground, and
`below` is what puts it there.

**A placement names its storey with `layer`.** Naming none takes the top surface, which on a roofed goal is
the roof.

**And on a stacked board, a plain layer's bands run from the bedrock course whatever its `base_y`.** Only
`kind: "made"` is painted over its own span, so give every ground theme a `fill` that is not `1:0`, and
`column` a cell where two plain layers overlap before believing any render.

Draw a tunnel, a wall or an undercroft as the **complement of the space** — the solid around the hole —
rather than cutting it with a `subtract`: `SK13` reads a subtract as the board's negative space and refuses
any add that fills it, on any layer.

**Sculpt, where a landmark is wanted.** `tools/sculpt/props.py` emits `dome`, `spire`, `ring_wall`,
`ellipse_wall`, `tapered_tower`, `arch`, `colonnade`, `ziggurat`, `bowl`, `crenellated_wall`, `drum_tower`
and a composite `gatehouse` as ordinary sketch shapes — circles and polygons with a floor and a height, not
stamped block soup. Give the layer `kind: "made"` and a `part_of`, which keeps `SK10`'s pair walk and
`SK11`'s reachability walk off it.

**Flow with a polyline.** The rasterizer splines a polyline's points before offsetting the band, so four
points draw as a curve — a wall, a lane, a watercourse. Never a chain of rectangles.

## 4a. What the adaptation must not break

These are the repository author's rulings, and they bind. `pgm-studio/docs/gameplay/approaches.md` is where
they live in full; this is what they mean when a composed plan is being reshaped.

**Sixteen blocks is the floor for a bay touching a goal or a spawn.** Negative space between two pieces is
crossed by jumping long before it is crossed by building. A short gap between a frontline and a wool room, or
between a spawn and a wool room, lets a player tower at the near edge and jump straight in, and the approach
the board was built around stops mattering.

A plain hole in a team's own ground may be twelve.

**The number is in blocks, never in cells.** The composer's own floor is two cells, which is eight blocks at
the default scale and ten at cell 5, so a cell count is not the thing to copy.

Three of this run's boards went under it while reshaping: `opus5-quadrangle` left five cells-worth between its
spawn and the wool-b enclosure (six blocks in the built world), `opus5-medlock-drift` five between `clamp-head`
and its wool room, `opus5-sallyport` five between `hub-back` and `wool-a-s`. Measure every gap a move opens —
the composer never emits one under ten, so a short bay on an adapted board is always the adaptation's.

**A wool room is defended from its corner.** The room wants **two faces on void**: it sits in a corner, a
defender holds two lines, an attacker picks between two. Three faces open is the ordinary composed shape and
is fine.

**A room with ground on every side is the failure.** There is nothing to hold and nowhere for the fight to
be, and the room becomes a spot in a field rather than a place.

It happens by adding area around the room while reshaping the ground near it, so when a ring is bent or a
vertex moved near a wool room, check what the room still fronts onto.

A room at the end of a spur is the milder failure: defensible, and one queue.

**The defence wall is meant to be in the way.** A `walls` entry is bedrock across the interface it names, and
blocking the way into a wool is its entire purpose: it gives the defence a prepared line before it has built
anything and costs a tunneller the shortcut. Reading a walled approach as a wool that cannot be reached is
reading the wall as damage.

**One wall on one interface**, narrow enough to be a line rather than a barricade.

**No ground pulled out past its ends**, and this is the part reshaping breaks. A wall spans the interface it
is authored on, so terrain widened beyond that interface leaves an open shoulder beside it, and a wall
players stroll around is only in the defence's way. Reshape the interface with the approach.

## 5. Relief: the instrument, and the danger

**Relief is not the board.** The author's words: relief should be used, and *solid structural areas are
likewise important*; overdoing it is a danger. What that means concretely:

**Pick the areas.** Some areas of the board carry relief that reads as natural terrain: a rise, a bank, a
dale, a hillside.

**Other shapes are explicitly excluded from the relief**, and that exclusion is stated rather than left to
happen. A shape carrying `relief_scope: "exclude"` is taken out of the solve, so the made ground and the
grown ground meet at a **face** rather than being graded into each other. That face is the join, and it is
where a stair, a flight or a wall goes.

**`hold` is the other one and does the opposite.** It lets the relief bring the lower tier *up* to the
shape, and then there is no step and no reason for a stair.

A frontline that has to be fought over, a wool room's apron, a causeway, a keep's yard: those are ground
that should be flat and stated to be flat.

**Do not put a `tread` on every mark.** A tread grades a mark's shoulder into its neighbour, so a board
whose every mark carries one is a board of nothing but shoulders: no flat to fight on, no face to decide
where anyone goes.

It reads walkable, which is why nothing else catches it. `RL5` does, off `level` in the relief read, with
30% the bar.

State a tread **where two marks would otherwise meet on a wall**, and leave it off ground meant to be flat
to its edge.
*Measured: five marks all carrying a tread → 25.4% level, no face at all. The same marks with the treads off
→ 43.6% and 70 faces.*

**Finish the ground by its angle, not by its height.** A theme hung on plan pieces or on height bands paints
a board flat from above however much relief is under it. Give the ground theme's surface a `layered` material
on the **`slope`** axis — a thickness on that axis is a span of degrees, so one stack finishes the flat, the
shoulder and the face of the same hill. Read `GET …/incline?format=text` before choosing where the bands
cut: it answers how much ground stands in each ten degrees, which is the only thing that says whether a cut
lands where you think it does.

**Read what the marks did to each other.** `POST …/sketch/relief/read` is the only read that answers
`silentMarks` (marks that landed nowhere), `seams` (the pairs that meet on a step, worst first, each with a
coordinate), `level` and `largestField`. A seam naming a **shape** rather than a mark is a `relief_scope`
pinning ground the marks were meant to shape. Over about 0.45 `level` and 0.13 `largestField` the ground is
a table with edges.

## 6. What this branch added, and why it is worth using

The base is `claude/pgm-studio-backlog-review-gnnhvw`. Two things on it bear directly on this work.

**The player-flow read-backs are better.** `GET /api/map/{slug}/plan/flow` answers what the board asks of
the two sides in prose — each objective's two walks and the ratio between them, where the ways in part and
meet, whether the defence shares the attackers' road, and the ground no journey reaches. It reads off the
plan alone, so it costs no build, and it is the read that catches §2's lopsidedness before a world exists.
A plan-tier walk now knows *who* is walking, a defence has a second origin at the crossing, and every side
reads the board over its own ground. Run it after every plan edit.

**House placement is more restricted, so it blocks paths less.** `DR-PASS` complains rather than staying
silent, the passage is measured eight blocks past every side, a lane is not a way round, and a village is
one block of buildings. And `POST /api/map/{slug}/sketch/seats?kind=&width=&depth=` now answers the question
**forwards** — where a prop of that kind and footprint *may* stand, over the whole board, including the way
past a building and the groups the pass forms — instead of you guessing and reading the decline. Use it
before placing buildings, not after.

## 7. The bar

A board is finished when all of these are true, and each one is a read rather than an opinion:

- `GET …/preflight` ends **`export gate OPEN`**, per team.
- `GET …/plan/flow` says something you meant it to say, and §2's ratio is either near 1 or deliberately not.
- `03-slopes.txt`, `06-claims.txt` and `04-routes.txt` have been read **before** any picture was opened.
- `GET …/coverage` is not carrying a quarter of the board as dead ground. Nothing refuses on this, which is
  exactly why it goes unrun. One board went 62.0% dead → 17.9% by moving its objective twelve blocks off the
  centre line and taking ten blocks off the width.
- `05-themes.txt` has no theme registered that painted nothing, and none at a fraction of a percent.
- The instrument count over your own finish (`pgm-board-warmup` §4) is not four zeros.

And the one that is not a read: **the board is about something, and the sentence was written before the
first shape.**

## 8. Free

No topic is assigned. What the board is, what it is made of, where things stand, and what it is called are
the author's — yours. The only thing being directed is that the composed arrangement is a starting point
and the board that ships is not it.
