# Opus 5 — Brackenfold: building the painting rules I had just written

## What I set out to build

A landscape destroy board authored strictly under the *What a board is painted with* section of
`AUTHORING-BRIEF.md`, written earlier the same session off measurements of the fifty-one boards in `specs/`.
The point of the run was not the map: it was to find out whether those rules can be followed, and whether
following them produces a board worth having. The identity, written before any shape: *a grass down falling
from each spawn to a peat working, with each team's monument on a cobbled fold above it.*

`maps/opus5-brackenfold`, 68 × 212, two landmasses of 5,297 cells joined by one build zone, zero declines,
export gate open, `review/opus5-brackenfold.md`.

## What the rules cost, one at a time

Every rule in that section was followable, and three of them were the reason the board came out simple.

**"A pattern takes two blocks, not a family"** is easy and it is *cheaper* than the alternative. There are two
patterns on the whole board and both carry exactly two entries. Filling a list from a family is one click in
the editor and one line in JSON; cutting it back down is the step that gets skipped, and the way to not skip
it is to never fill it — write the two blocks you mean.

**"A voronoi is never ground"** removed a decision rather than adding one. Put it in the fill and the only
question left is which two stones; put it on the surface and every cell size, jitter and warp is a knob to
guess at. The section render shows why the rule is right: at `cellSize` 14 in the fill it reads as the body
of the rock, and there is no arrangement of it on a grass surface that would not read as a diagram.

**"The shape goes in the relief"** is the one that did the most work. Four of five pieces stand at one
height; the board's whole character is a `grain` at scale 24 and one `area` mark. The plan stayed at five
pieces, so the theme count stayed at three without any discipline being required — **the theme-per-piece
habit is a consequence of the piece-per-landform habit**, and fixing the second fixes the first for free.

**"Three themes is a map"** was therefore never under pressure. I did not have to resist a fourth.

**"A building is never the ground it stands on"** needed a deliberate act: the shipped `ae-fold` style is
cobble and spruce, and the fold platform is cobble, so forking the style and repainting the walls spruce and
the roof dark oak was the whole of it. The rule is easy to *follow* and easy to *forget*, because a preset
that looks good in isolation is what puts a grey house on grey ground.

## What I could not say

- **Whether a brush is big enough, without building the world.** The brief tells an agent to render the
  theme and look. `POST /api/terrain/theme-preview` draws its sample plateau and answers five
  views — `section`, `rim`, `surface`, `wall`, `fill` — which told me everything about the fill and the coast
  wall. What it cannot tell me is what a theme sits *next to*: the sample terrain is grey stone, so the fold
  (cobble on stone) reads as one flat mass in the preview and is perfectly legible on the real board against
  grass. **Out of reach from where I was standing**, not missing — the preview draws one theme and a board is
  the argument between two. An `?against=` taking a second theme would answer it.
- **Nothing, on the theme preview.** I nearly filed one here and it was my own mistake — see below.
- **Whether 34.9% dead ground is bad on a board of this shape.** Coverage walks corridors between waypoints,
  and a destroy board with one goal a side has four waypoints where a CTW board has ten. The ground the
  corridors miss is the flanks, which is where the woods are — 2,784 cells count as *decorated* rather than
  reached. **Out of reach**: coverage cannot say whether a flank is dead ground or the scenery a lane is
  looked at across, and only an author can.

## What I got wrong

- **I put two monuments 28 blocks apart** and called it two objectives. On a 68-wide board that is one
  objective with two health bars. The author ruled it, and the fix — one monument — also moved `GO1` from
  3.09/3.27 to a better-centred 3.55.
- **I made the middle out of land.** I authored a peat cutting in the relief across a continuous board, which
  is a corridor rather than a decision, and the studio had already told me so and I had not heard it: `STRUCT`
  refused my *first* plan for mixing a non-fanned middle piece with the mirrored ones. I fixed that by
  deleting the piece and putting the cutting in the relief, when the finding was pointing at the shape of the
  board rather than at the piece list.
- **I nearly filed a defect against the theme preview that was my own misreading.** I asked it for two views,
  got byte-identical answers, and started writing that the `view` word did nothing. It does: the answers were
  identical because I was still asking for **JSON**, where `view` is irrelevant and every view comes back at
  once. Asked with `?format=png` the views differ, and the OpenAPI document publishes all five —
  `section`, `rim`, `surface`, `wall`, `fill` — as an enum on the route, which is one `GET /api/openapi/v1.json`
  away and which I had not read. The brief's own rule caught it: *a claim about a capability is checked before
  it is filed.* It was checked, and there was no claim to file.

- **I claimed a rule was followed by the numbers rather than by the picture.** The `fold` theme passed every
  rule I had written — two families, no pattern, a rim only where an edge was made — and its section preview
  reads as one grey slab. It is fine on the board. But "it satisfies the rule" and "it looks like something"
  are different claims and I made the first while meaning the second.

## What worked first time

- **The relief.** One `grain` at amplitude 2.2 / scale 24 and the moor rolled convincingly on the first
  build; the heightmap render showed long swells rather than static, which is exactly the difference the
  brief's brush-size rule is about.
- **`bendShapes`.** 8 compiled vertices to 24 drawn on both ground shapes, no tuning, and the coast stopped
  reading as the plan's rectangles.
- **`GO1` by arithmetic before authoring.** Solving `(208−d)/d ∈ [3,4]` for the monument's distance from its
  own spawn gave `d ∈ [42, 52]`, I placed it at 46, and `/plan/inspect` answered 3.09 on the first read. The
  ratio is derivable from the extent before a shape exists and nothing in the loop says so.
- **Every prop decline named its cell.** Four bad placements, four coordinates, four moves. The pass is the
  best-behaved surface in the studio.

## Open gameplay questions

- **A 48-block bridged gap.** Nothing states how far a team may be asked to bridge. I chose the distance the
  author named — the spoil heaps' line — rather than a number of my own. Recorded as the author's.
- **A full-width crossing costs a soft term.** With the gap open across all 68 blocks, `frontline-width`
  reads 22 cells against an authored band of [1, 16] on the wider first draft; narrowing the board to 68
  cleared it. I take the band as calibrated on capture boards, where a frontline is a face two teams contest,
  rather than on a destroy board where the whole front is the crossing. **Decided, not derived.**
- **`fill-ratio` 0.658 against a band topping at 0.542.** A continuous land board is inherently fuller than
  the island boards the band was measured on. Left as is.

## One thing the brief should say and does not

**The magenta block at the centre of every board is the observer platform's bedrock**, and bedrock has no
tone family on purpose — it is the map's floor and the shell of its walls. `SurfaceReport` legends an
unnamed full cube magenta so a block missing from a family reads as a fault, and this one is not. An agent
who does not know that will chase it. It is one sentence and it belongs beside the render advice.
