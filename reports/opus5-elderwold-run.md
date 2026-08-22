# Opus 5 — Elderwold: the relief tool taken as far as it goes

## What I set out to build

A destroy board, 120 blocks across and 150 a team side, from **as few plan pieces as possible** — the
board's shape stated once as a single polygon and then shaped in the sketch rather than assembled out of
rectangles. One endstone destroyable a side. A dense oak wood, a path, a river, houses. Hills with flat
plateaus and depressions that step down. One theme for the whole surface, with the **path tool used as a
texturing brush** to give the board dedicated ground without a second theme.

The board is `maps/opus5-elderwold`, the documents are `specs/opus5-elderwold/`, and
`review/opus5-elderwold.md` is what it measures.

## What worked first time

- **Three plan pieces at one surface fuse into one shape.** The compile emitted exactly one terrain
  polygon and one island (`team`), which is what made "author the coast as one ring" possible at all.
- **Replacing that shape's `vertices` and `controls` through `shapePropsById`.** Nothing in
  `tools/README.md` says the merge reaches geometry — it lists `relief_scope`, `controls`,
  `anchor_heights`, `height_mode` — but it is a plain dict update, and a 24-vertex ring with a full
  handle table went through with no `RQ3`.
- **A destroyable with an empty `piece` and an absolute `at`.** No rectangle had to be manufactured to
  carry the goal; it stands on ground the relief made. Documented in `plan.md`, and it is the single
  biggest reason the plan stayed at three pieces.
- **`point` marks as flat-topped hills.** A point mark pins a *disc*, so a radius-8 point is a 16-wide
  flat top with the field falling away around it. That is a hill with a plateau in one line of JSON, and
  it needed no `area` mark on top.
- **Nested `area` marks as a stepped basin.** Three rings, outer first, each at a lower height. "A later
  mark wins a contested cell" is the whole mechanism; the transect reads y3 → y6 → y9 → y11.
- **The `scarp` as the composition of the objective.** One mark, and the plateau has a face nobody walks
  up and one end they do. `relief/read`'s `acrossZ` said `onFoot 0, withBlock 0, descended 13` — a
  one-way face — without my having to measure anything.
- **The symmetry fold.** `symmetryError: 0` on every build, never touched.

## What I got wrong

**The Bézier recipe made a gear.** `GENERATION-NOTES.md` gives a per-edge handle construction —
`c1 = p0 + d·t + n·bulge` — with two constraints that keep an edge from cusping. Both constraints held
and the coastline still came out as twenty-four points around a blob, because the recipe constrains each
edge *against itself* and says nothing about the two edges meeting at a vertex. Every edge bulging
outward meets its neighbour at a corner. A closed organic outline wants tangent continuity instead:
Catmull-Rom converted to Bézier (`c1 = P1 + (P2−P0)/6`). The claim looked right because the constraints
were satisfied — that is exactly why it took a render to catch.

**I believed a 200 for two rounds.** My scratch loop posted the layout with `PUT …/sketch/from-plan`,
which merges — and a relief is carried across a merge under its own rule. So an edited relief answered
200, `relief/read` reported the *new* numbers (it reads the posted body) and `render/heightmap` drew the
*old* terrain (it builds the stored document). Two reads of the same map disagreeing, both correct. The
plain `PUT …/sketch` replaces and is what a scratch loop wants; `from-plan` is right for `drive.py`
because it runs against a fresh map row.

**I designed a ford the water pass cannot build.** See below.

**I over-tightened the tree placer twice.** First to Euclidean 3.5 (declines), then to a flat Chebyshev 5
(the wood fell from 60 trees to 23). The claim is height-dependent and seed-dependent; guessing a single
number in either direction costs either warnings or half the forest.

## What I could not say

**A ford, to the water prop.** I wanted the river bed to rise at the crossing so the road runs over a
shallow bar. The relief states that — a `line` mark takes `h` per vertex, and the bed reads
`[6,6,6,7,9,7,6,6,6]`. The water prop cut it flat regardless: `(0, 0)` came out y3 with two blocks of
water. This is **in the system and named**: `relief.md` §9 and §16 are `S46`, "water does not read the
relief", with the depression-filled routing and per-pool levels designed and not built. I looked for a
per-vertex depth or a bed-height field on the water prop and there is none — `radius`, `depth`, `form`,
`edge`, `shore`, `shoreWander`, `bank`. **Out of reach from where I stood, not missing from the design.**
The workaround is geometric rather than a capability: author one arm, stop it short of the axis, and let
the rot_180 fan draw the other, so the gap between them is the ford. That only works because the
centreline is odd-symmetric about the origin, which a mirror-axis river can be made to be.

**A path under a tree.** Using the path tool as a texture brush is the right instrument and it cannot
reach the one place I most wanted it: the forest floor. `DR-ROAD` keeps a trunk three blocks off the
nearest paved cell, so a paved wood is an empty wood. There is no per-prop opt-out and I do not think
there should be — the rule reads a *kind*, deliberately, so a mask cannot be predicted per prop. Filed as
a shape of the design rather than a gap: **texture goes where props do not stand**, and the two sets
turned out to be the ones a designer wants bare anyway.

**A second theme scoped to the wood.** `TP10` scopes a theme to a *shape*, and the board has one shape by
construction. Choosing "one polygon" is choosing "one theme scope". An `addShapes` polygon over the wood
with `relief_scope: inherit` would have bought a second scope, at the cost of a second shape in an island
whose whole point was to have one. Not attempted; recorded as the trade.

**The claim distance of a tree.** `DR-CLAIM` names the pair after the fact and `GET /api/rules?rule=DR-CLAIM`
explains the priority order, but nothing answers *how far apart two oaks must stand* before placing them.
`Decorator.CanopyRadius` measures it off the built crown, and the crown is hash-keyed off the seed, so it
is genuinely per-prop rather than per-species. I fitted it from four builds — clash below Chebyshev
`(hₐ + h_b) / 5`, seeded variance either side — and used `/4.7` to sit clear of the fit. A
`POST /terrain/prop-preview`-style answer giving a placed prop's own ground claim would turn four builds
into one call. **Missing from the surface**, not from the system: the number exists, it is just not
answerable before a build.

**Whether a plan-space grid can show a 24-vertex coast.** `plan/ascii` renders the *plan*, which by then
is three rectangles; the coast lives one level down. Nothing pictures a sketch (`sketch.md`'s own
*Limits* says so). The reads I used instead — `relief/read`, `render/heightmap` on the sketch-stage map,
`render/section`, `column` — cover it, but the loop is "build the world to see the drawing".

## The board's real defect, measured

**57.0% of the ground is dead**: 15 907 of 27 900 cells sit off every route between the board's
waypoints, in two lobes at `(−22, 42)` and its mirror. `plan/flow` says the same thing off the plan
alone, before any world exists — 46% of blocks, at `(−40, 0)` and `(40, 0)`.

The cause is structural and not decorative. A destroy board with one objective a side and both spawns on
the axis has exactly four waypoints, and every route between them runs down the spine. The flanks — which
is where the wood, the hollow, the cape and the hamlet are — are reachable, pleasant, and on the way to
nothing. `coverage.png` shows it plainly: a green ribbon down the middle, orange where props are, red
everywhere else.

There is a fix and it is not more dressing. **Move the spawn off the axis and the monument the other
way**, so the two attack routes become two lanes rather than one. With the spawn at `x +22` and the
monument at `x −20`, red's attack runs down the east flank and blue's down the west, and each team's own
defence leg crosses its own half diagonally. It costs a re-check of `GO1` (the ratio moves with the
offset) and the shelf would want moving toward the axis to keep it. I did not do it: it re-composes the
board and the terrain work was the brief. It is the first thing I would change.

## Open gameplay questions

No oracle in this session; each was decided and built, and each is a question rather than a claim.

1. **Is a one-way scarp the right face for a destroy objective?** The shelf's south face measures
   `onFoot 0, withBlock 0, descended 13`. Attackers arrive by the east walk-up in the open, or by
   building. I judged that a good composition — one exposed approach the defence can watch, plus a
   buildable face that costs blocks — but a face nobody crosses on foot is a strong statement and
   `approaches.md` does not settle how strong is too strong.
2. **Should the ford be the only dry crossing?** The river is 12 wide, two deep, with one 18-block paved
   bar at the centre. Everywhere else is a swim in the open. That makes the middle of the board a single
   throat, which is either the map's best moment or its worst.
3. **106 oaks over a 40×50 wood — is that cover or is it a wall?** It is as dense as the pass allows
   without declining a tree, which was the brief; whether "as dense as the rule permits" is a playable
   density is not something the rule knows.
4. **Is 120 wide too wide for one objective a side?** The coverage number above is really this question.
