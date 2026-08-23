# Opus 5 — Undercroft: what the sketch tool's layers actually do

## What I set out to find out

The fourth board, and the only one whose subject is a feature rather than a look. The brief:

- find out **what the different layers inside the sketch tool do** — every board so far has used the
  ground layer alone;
- **shapes can also be raised up to stack them**, and how that meets relief and dressing is unknown;
- a **DTM** board, and a **simple** one, because the 2-D renders show only the top surface and the
  rest has to be read from the isometric.

`maps/opus5-undercroft`, `specs/opus5-undercroft/`, `review/opus5-undercroft.md`.

The board is a two-level destroy map: a ground island a team, a stone **terrace** twenty blocks over
its middle carrying the monument, a nine-block **hall** under the terrace, and two **bridges** across
the strait — three layers in all. A control run of the same plan with the layers stripped
(`Undercroft control`) is what every claim below is measured against.

## The mechanism, before the board

The docs say a layer is a slab with its own `base_y` and that an agent should author the ground layer
only. That last sentence is why nothing had ever been drawn on a second one, so the first work was
three throwaway probes on flat ground rather than a map.

- **The air gap survives painting.** `TerrainPainter` resolves one band stack per column, bedrock at
  the bottom and surface at the top, which would fill the gap between two slabs — except that it
  writes only where the world already holds *stone*, and the gap is air. The invariant is what makes
  layers work at all.
- **`floor` is the underside**, inside the layer, and the slab's thickness is its solved surface minus
  that floor. `base_y 20` + `floor 4` puts a soffit at y24 whatever the relief does above it.
- **Relief solves per layer** and comes back shifted into world Y. Two islands, two relief documents,
  and `relief/read` reports both.
- **`SurfaceTop` is the max over layers** — one number per cell — and every consumer downstream reads
  that grid: the painter, the structure floors, the placements, the dressing, and every 2-D render.

`tools/drive.py` grew one key for it, `addLayers`, which turns the compiled single-layer document
into `layers` and appends slabs. The compiled document carries `layers: null` beside its `layout`, so
`setdefault` is not the test; and the old `layout` key has to be *removed*, because `ResolveLayers`
reads one or the other while `IslandIds` reads both and would double every island.

## What worked first time

- **A ground ramp meets an upper slab exactly.** Where a causeway's solved top equals the terrace's
  top the two columns merge into one and the join is a single one-block rise. No special shape, no
  stitching: two layers whose spans touch are one solid mass.
- **The objective climbed onto the terrace by itself.** `destroyable-1` is stated in plan cells with
  `float: 4` and knows nothing about layers; it lands at y34 over the terrace, against y19 on the
  control. A placement snaps to the surface top and the surface top is the highest layer's.
- **Paths on a bridge pave the bridge.** Same rule, and here it is the one you want.
- **The editor shows layers.** The sidebar lists all three with their `base_y`, and the isometric
  stacks them. The 2-D canvas edits the active layer and ghosts the rest.

## What I got wrong

**A one-column chasm between the causeway and the terrace.** The terrace was drawn to x ±18 and the
causeway's `width 8` band reached x ±19, leaving one column of hall floor between them — a 12-block
slot, and the terrace an island in the air. Nothing reports it: `traversability` reads the top of
each column and calls the board one component. Widening the terrace to x ±20 so the two overlap is
the fix, and the check is a transect, not a picture.

**A four-block lip across the hall's only way out.** `back-rise`, a point mark, reached far enough
into the hall's mark to overwrite its northern rows, so the floor stepped 14 → 18 at the doorway —
enterable, not leaveable. Same lesson the last board taught from the other side: **a later mark wins
a contested cell**, so the mark that must hold its ground goes last.

**I read a transect through a filter that capped at y22** and concluded the causeway topped out six
blocks below the terrace. It tops out one block below. A measurement is only as good as the filter
over it, and a filter written to skip leaves and logs quietly skipped the answer.

**I stated a tree for the hall floor and got it on the roof**, which was the point of stating it —
but the first attempt landed inside the goal's clearance and was declined by `OB19` for a reason
that had nothing to do with layers, which took a re-place to separate.

## What layers cost

**A bedrock plate in the void.** `TerrainBuilder.Build` writes bedrock at y0 under every footprint
cell it fills, per layer, so a slab over open void leaves its own shadow at the bottom of the world:
here two 20 × 20 plates under the bridges at `(-32..-12, -10..10)` and `(12..32, -10..10)`, and the
terrace's four overhanging rows over the court. The theme's `bedrock` value is 0 on both layers and
changes nothing — the painter only overwrites stone, and bedrock is not stone. It also puts those
columns in the Y0 set a void filter reads.

**The covered ground is unpainted.** One column, one band stack: the ground under the terrace falls
inside the `fill` band and comes out as fill, with no turf, no rim and no wall. On this board that is
stone brick and reads as a paved undercroft, which is luck rather than a decision.

**The covered ground cannot be dressed.** Every prop resolves against the surface top, so nothing can
be put in the hall and nothing warns you — the prop lands on the roof and the census records it there.

**The covered ground is invisible to every 2-D read.** `topdown`, `heightmap`, `surface`,
`traversability`, `coverage` and `relief/read`'s walk all project to one height per column. Only the
isometric preview and `render/section` show a stack.

## What I could not say

**Whether a hall is reachable.** The reachability model is a heightmap: `relief/read` walks the
surface grid and `WorldColumns.Membership` discards Y outright — "the height is discarded here and
only there". Neither can answer whether a player can get under an overhang, and both answer
confidently that the board is one component. Every claim in the review about walking into the hall is
a hand transect. **Missing from the design**, and it is the gap that matters most: a layered board's
correctness is exactly the question its reads cannot ask.

**Whether two layers overlap in a way that closes a gap.** Nothing checks a slab's floor against the
terrain under it. A ground mark raised two blocks too far turns a nine-block hall into solid rock,
silently — it just merges. A "minimum headroom" read over the stacked columns would be one pass over
data the rasterizer already produces.

**How to theme a covered cell.** Theme scope is 2-D and the smallest-area shape wins, so an upper
shape's theme owns the ground beneath it. A hall floor cannot be given its own material while its
roof has another. **In the design**, and arguably right — one column, one theme — but it means the
undercroft's floor is the terrace's stone whether or not that was wanted.

**What `section` takes for `at`.** `axis=x` cuts along x, so `at` is a z; `axis=z` cuts along z and
`at` is an x. An out-of-range `at` returns a 200 with a blank image rather than a refusal, which cost
several attempts to notice. **A surface gap**: a coordinate outside the world is a fault, not a
picture.

## Open gameplay questions

1. **Is a hall under an objective good ground or dead ground?** It is covered, unlit, invisible from
   above, and on this board it is the only route between the court and the back that does not climb.
   Whether that reads as a flanking route or as a place nobody goes is not something the corpus or
   the code can say.
2. **Does an objective on a deck want a second way up?** There are two causeways, one a side, both
   walkable and both in the open. A ladder-free deck with two ramps may be too easy to hold.
3. **The bridges are on nobody's path** — each team's objective is on its own island, so crossing is
   optional and `coverage` calls them dead. That is the honest reading of a DTM with two goals; on a
   board with a shared middle objective they would be the map.
