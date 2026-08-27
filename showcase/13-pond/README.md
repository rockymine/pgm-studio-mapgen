# 13 — a basin, and the water that sits in it

**The technique: a pond is two statements that have to agree — a `push` whose `crown` dishes the ground into a
bowl, and a `water` prop whose radius stays inside that bowl. Get the second wrong and the water carves a
cliff the relief never drew.**

The plan is `02-theme`'s, untouched, renamed **Kettlemere**. The finish gains a `relief` block on island
`team` and one `water` prop in `finish.dressing.props`.

## The document

```json
"relief": { "team": {
  "base": 9, "reach": 20, "step": 1, "stairs": true,
  "marks": [
    { "id": "coast",  "kind": "rim",  "h": 9, "depth": 1 },
    { "id": "strand", "kind": "line", "points": [[-40,18],[0,18],[40,18]], "h": [9,9,9], "width": 5 }
  ],
  "pushes": [
    { "id": "kettle", "ring": [[-38,-6],[-29,-8],[-26,2],[-27,14],[-33,20],[-39,12]],
      "amount": 0, "falloff": 10, "roughness": 0.35, "crown": -5, "seed": 7 }
  ] } },
"dressing": { "props": [
  { "kind": "water", "id": "kettlemere", "points": [[-33,-2],[-32,8],[-33,16]],
    "radius": 4, "depth": 3, "form": "natural", "edge": 0.5,
    "shore": 1.2, "shoreWander": true, "seed": 21 }
] }
```

`kettle` is the only landform mark beyond the standard coast/strand pair. It sits on the west flank, the same
strip `07-hill` and `09-mesa-and-hollow` use for their own landforms — the flank is 15 blocks of real ground
between the coast and the island's own interior void (§*What went wrong first*, below, on that void). `rot_180`
fans the one push to both teams, so Kettlemere is a matched pair, one per side, not a feature only one team
gets.

## A hollow wants a push, not an area — measured

`09-mesa-and-hollow` cuts its hollow with an `area` mark: every cell inside the ring pinned to one flat `h`.
The same instrument was tried here first, ring for ring, against a `push` whose `crown` is negative over an
identical outline — one basin on each flank of a throwaway comparison board, so a single section crosses both.

| | `area`, `h: 5` | `push`, `amount: 0`, `crown: -5` |
|---|---|---|
| floor | flat at y4 across the whole ring | y4 only at the medial axis; the rest slopes up from it |
| edge, measured one block either side of the ring outline | **y4 → y8**, a sheer wall | y8 → y7 → y6 → y4 over four blocks, a bank |
| reads as | a quarry floor, walled | a dish a player can walk down into |

The area mark states a height and stops; nothing about it says what happens at the ring's own edge, so the
relaxation outside it snaps straight back to the base and the wall is vertical. The push's `crown` is `Amount`
at the ring edge and `Amount + Crown` at the medial axis (§*Numbers*), so the interior is already a continuous
gradient from rim to floor — a pond's basin, not its foundation trench. The push is what shipped; the area
mark's own use — a bench, a floor with a rim — is `09`'s.

## The water level is derived, never authored

A `water` prop carries no field for how high the water sits. `WaterBed.Cells` carves a parabolic bed under the
drawn centerline — deepest on the line, one block at the edge of `radius` — and the dressing pass then reads,
across every cell that bed touches, the **lowest existing ground surface** among them: that minimum is the
water line for the whole prop. Every column under the bed fills from its own floor up to that line and stands
open above it; a column whose ground was higher than the line has that difference cut away to air, not
draped over. `depth` is not "how deep the water is" in isolation — it is how far the bed is cut *below the
line*, and the line itself is wherever the run's shallowest point already stood.

That is why `depth: 3` reaches bedrock at Kettlemere's own centre: the push's `crown: -5` already put the
deepest cell at field height 4 (block top y3), so the bed's floor is `waterLevel(3) - depth(3) = 0`, and y0
is bedrock. Deepen the push and the same `depth` leaves a floor of packed dirt instead; the two numbers are
read together, not separately.

`form` reshapes the same centerline without moving a point. `canal` holds the nominal `radius` the whole way.
`natural` wobbles the width by a value field, ± `edge` blocks — Kettlemere's `edge: 0.5` is a gentle ripple on
a four-block radius, not a ruled canal edge. `stream` beads the width along the arc, pinching to half `radius`
on a fixed interval and running shallower throughout, which reads as riffles rather than one even channel —
the form for a moving watercourse, not a still pond.

`shore` is the band **outside** the water that gets the `bank` material without being flooded — a beach, not a
kerb. `shoreWander` decides whether that band holds one even width or opens and closes along the run; either
way its inner edge is the water's own, so it hugs whatever shape the water takes. `bank` is not a block: it is
a full `TerrainMaterial`, so the bed floor and the beach can be a voronoi patchwork exactly the way the surface
painter tiles one — Kettlemere leaves it at the default (gravel, coarse dirt, sand), which is what the shore
column below shows.

## A closed ring does not fill — it moats

A `water` prop is a channel: the swept band of a drawn **centerline**, never an area. Tracing the basin's own
outline as a closed ring — points that return to their start — does not pond the interior; it floods a **band**
that follows the ring, leaving whatever is inside the loop untouched. On a throwaway variant of this same
basin, a ring of radius 3 produced a donut: the loop itself came up water, and its centre came up dry gravel,
because gravel is what the ring's own `shore` band painted onto ground the water never reached.

| Trace | at the basin's own centre | in the flooded band |
|---|---|---|
| a **line** through the basin (three points, radius 4) | water, y1–y3 | — |
| a **closed ring** around the basin (four points back to start, radius 3) | dry — Gravel at y3 | water, y1–y3 |

A pond wants the first: points that cross the basin, with `radius` reaching close to the basin's own half-width,
so the swept band covers the interior rather than skirting it.

## What went wrong first

The first `radius` was 6, sized to "cover the flank." `kettle`'s own half-width at the pond's centre row is
about **5.7 blocks** (measured from the ring's drawn vertices) — so a six-block radius, plus a two-block
`shore`, reached three to four blocks *past* the push's own footprint into ground the relief had never
touched, still standing at the ambient top y8. The carve does not know the difference: it flattens every
column under its reach to the derived water line regardless of how that column got there, so the untouched
ground just past the basin's edge was chopped down in one step.

Measured, one block apart:

| x (z = 45) | before (radius 6) | after (radius 4) |
|---|---|---|
| −37 | water, y3 | dry, Gravel at y6 |
| −38 | **y8, full ambient height** — a five-block cliff from the column beside it | dry, Grass at y7 |
| −39 | y8, ambient | y8, ambient |

Shrinking `radius` to 4 (and `shore` to 1.2) keeps the water's reach inside the push's own bowl, so the last
carved column sits on ground the relief had already sloped most of the way down — the water meets a bank
already descending toward it instead of a wall standing at full height beside a hole. **A water prop's radius
has to fit inside the landform that carries it; nothing checks that it does, and a radius drawn generously
against the *drawn* shape rather than the *solved* one is a cliff waiting one render away.**

## What to look at

| Picture | Says |
|---|---|
| `renders/world-topdown.png` | both ponds, one per team, oval and gravel-fringed — water is one of the five categories this render separates |
| `renders/world-heightmap.png` | the basins as the only "under water" (blue) patches on an otherwise flat board |
| `renders/section-x45.png` | a cut across the pond at its centre row — the sloped grass bank into a rock-walled bowl, water pooled at the floor |
| `renders/section-z-33.png` | a cut along the pond's own long axis — the two tapered ends, shallower than the middle |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| `POST …/sketch/relief/read` | cells 10 000 · low **4** · high 9 · relief 5 · symmetry error 0 |
| `GET …/column?at=-33,45` (pond centre) | y3 Water · y2 Water · y1 Water · y0 **Bedrock** — `depth` reached the floor |
| `GET …/column?at=-37,45` (pond shore) | y6 Gravel (bank) · y5–4 Dirt · y3–1 Stone · y0 Bedrock — dry, painted, not flooded |
| `GET …/coverage` | 3.3% dead — unchanged from `02-theme`; a pond moves ground and paints it, it does not add or remove any |
| `GET …/preflight` | export gate **OPEN** |
