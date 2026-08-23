# Opus 5 — Hollowmarch: a composed board taken over and given its ground by relief

## What I set out to build

The fourth board, and the first that does not start from a plan I drew. The brief was:

- take a **composed CTW board from the composer at 32 players**, with a **hole hub** and a **U
  frontline**, filtered for;
- **shift the layout** to make room for a middle island inside the build zone;
- reshape the outline the way the earlier boards were reshaped, but with **sharp and shallow lines
  rather than Bézier**;
- do **all height elevation with relief**, and **pre-raise the spawn and wool pieces** so the relief
  has something to attach to;
- **disable wall and rim on the islands**, so the land is the surface stack and the fill and nothing
  else;
- the previous board's boulder idiom again, but **angled one way by three stated points** — one face
  smooth into the terrain, the other raised and falling off about seven blocks.

Mid-build the author added two: the lowest ground was at y2, so **raise the terrain about five
blocks everywhere** rather than let a 9-deep surface be cut down to two; and put **a small pond in
the middle of the middle island**.

`maps/opus5-hollowmarch`, `specs/opus5-hollowmarch/`, `review/opus5-hollowmarch.md`.

## What worked first time

- **The composer answers the filter directly.** `hub=double-hole&front=twin&wools=u` at 32 players
  returns seed 1233 at score 0. `u` is a *wool* family, not a frontline; the frontline that reads as
  a U opening forward is `twin` — a bar with two prongs off it.
- **A pinned plan is just JSON, and shifting it is four edits.** `+4` cells of z on every piece and
  box, one new `mid-isle` piece with `mirrors: false`, `globals.surface` 9 → 14, and a per-piece
  `surface` on seven of them. Nothing else in the composed board was touched.
- **`relief_scope: hold` is exactly the pre-raise the brief asked for.** A held shape keeps its own
  level and the surface around it is solved knowing where it has to arrive, so the terrain runs up to
  the spawn pad rather than being cut away from it.
- **Faceting replaces Bézier cleanly.** Cutting every edge into ~5-block runs and stepping the joints
  ±3 along the edge normal, alternating sign, took the team island from 18 vertices to 49 with zero
  self-intersections. Seam spans are emitted on the original line, so a mirrored edge still matches.
- **Three points and a plane is the right shape for "leaning one way".** `plane3` solves
  `a·x + b·z + c = h` through three stated `(vertex, height)` pairs and fills the rest; picking the
  two highest-z vertices at 0 and the lowest-z at the lift makes every crag turn its cliff to the
  attack and its ramp to its own side, without any of them being individually posed.
- **Turning the plan piece off the mirror and stating the partner by hand.** The middle island does
  not mirror — it is its own `rot_180` image by construction — so its shapes are stamped once. Its
  second crag is the first one's image, written out: `[[-x, -z] for x, z in ring]` with the same
  anchor heights, which turns the plane with the ring and puts a raised face toward each team.

## What I got wrong

**The default surface is a depth, not a floor.** The composer flattens a board at 9 and the theme's
surface stack is 9 deep, so a rim cut one block into it leaves the coast standing on two blocks of
ground. The author caught it before I did. `globals.surface` 14 and every relief mark five blocks
higher is the whole fix, and it is a fact about the *stack*, not about the plan.

**A `hold` pad is not reachable just because it is next to another one.** The wool-b room pad went in
at 18 beside a 14 approach; `relief/read` reported "places 7" and nothing else. A hundred cells of
room floor that nobody could walk onto. Two held shapes side by side cannot be ramped by a relief
mark — both are held — so the pads have to climb one block at a time by their own stated surfaces:
16 → 17 → 18.

**A line mark's `width` reaches either side of the line.** `front-bank` at width 12 sitting at z 50
wrote over the frontline flat all the way down to z 38, and a push stacked on top of that: a
seven-block wall across the necks of the two frontline prongs, which is the ground an attack launches
from. Width 5, moved back to z 54..60, with both front pushes moved north to z 60.

**A `raise` hands the ground's slope on to its own top.** The first `scar-front-w` stood across a
nine-block terrain step and read as a fourteen-block wall — the lift is seven, and the step is the
other seven. Levelling the footprint first with an `area` mark at the ring grown 1.3× puts the whole
face in the anchor plane, where it was stated. All five team crags and both isle crags now stand on
one.

**A `raise` over void builds from its own floor.** Two cells of `scar-hub-w` hung over the sea and
came out as seven-block cobble stubs at y0..y6 beside the island. Nothing declines it — the shape is
terrain, and terrain over void is a spur. The seating check now audits every ring for sea cells as
well as hole cells, and every crag comes back sea 0.

**The composed board's holes are made by arrangement.** The hub's two slots and the U wool's notch
are the shape of the pieces; no region marks them, so an add-shape dropped on one fills in the layout
that was asked for and nothing says a word. A void cell with land in all four directions within 16
blocks is the predicate; no crag may cover one.

**My keep-out model for the dressing was the wrong shape twice.** First too tight — DR-ROAD measures
to the cells a stroke actually *claims*, and I was measuring to a fraction of the band, so thirteen
props declined. Then too loose in the other direction: at full radius plus standoff, twenty-one path
props over a 110 × 220 board left **eleven** plantable cells in total. What fixed it was not a better
model but a smaller brush — one grass tongue per crag instead of two, and the two dirt smears cut
from radius 6–7 to 4–4.5.

**I let the boulders eat the woods.** Seating six boulders before the trees took twelve trees' worth
of ground, because DR-CLAIM only needs footprints not to overlap and I was reserving three blocks
around each. Three boulders and the real margin gives sixteen trees.

## What I could not say

**Whether a shape's footprint is on land.** There is no "does this ring stand on ground" call, so the
land model is rebuilt outside the studio from the compiled shapes and the faceted rings, and it can
disagree with the built coast — which is how the two sea cells got through the first check. A
`POST /sketch/probe-footprint` answering land · sea · hole for a ring would replace forty lines of
scratch and be right where mine was approximate. **Missing from the surface.**

**Which cells a path prop will actually claim.** `PathStroke.Cells` respects style, coverage and seed,
and none of that is reachable before an export. Every keep-out I computed was therefore a guess at a
stroke I could not see, and the correction loop was drive → read declines → move. A read-back of a
prop's claimed cells would close it. **Missing from the surface.**

**A per-vertex skirt.** Same gap the last board reported. `skirt` is one number for a whole outline,
so the *edge* cannot be steeper on one side; all the asymmetry available is `anchor_heights`, which
tilts the top. It happens to be enough here, because the flush face has no drop to step down — but
that is luck in the shape of this brief, not a mechanism.

**What relief does under an erected shape.** The pad trick works, and I found it by transect. Whether
a `raise` is *supposed* to inherit the ground's slope, or whether `floor` was meant to answer this,
is not written down anywhere I could find. **Undocumented**, and it is the single most surprising
behaviour on this board.

## Open gameplay questions

1. **Are the crags in the right place on a CTW board?** Five of the seven stand on the team island —
   two on the frontline bar, two at the hub, one behind. Each gives its own team a walk-up and the
   attacker a cliff, which is a defensive asset stated seven times. Whether that is a fair way to
   spend the terrain on a wool board, or just a defender's board, is the author's call.
2. **The frontline-to-middle strait is 15 blocks**, the bottom of `CT12`'s window. Short enough that
   the prongs are a real launch, and short enough that the middle island is contested immediately.
3. **The spawn pad is three blocks over the ground it looks out on** and the wool rooms five. That is
   what "pre-raise so the relief attaches" produces; whether a wool room wants to sit *above* its
   approach rather than at the end of it is a question about how the room is attacked.
4. **2.2 % dead by `coverage`**, in four small pockets behind crags. Recorded, not treated as a
   verdict.
