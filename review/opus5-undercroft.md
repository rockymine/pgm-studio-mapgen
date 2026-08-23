# Undercroft — what a second layer is for

> A destroy board built to find out what the sketch tool's **layers** do. Three slabs: the ground,
> a terrace twenty blocks over it carrying the monument, and two bridges across the strait. The
> ground under the terrace stays walkable — that hall is the whole point of the feature.

**In one sentence:** a small DTM board whose objective stands on a stone terrace that is a *separate
layer* rather than raised terrain, so the ground it covers survives underneath it as a nine-block
hall — the one shape the studio can build no other way.

80 × 180 blocks, `rot_180` about the origin, base surface 14, ground y13..27, terrace y24..30,
bridges y14..15. Three layers, two islands, one destroyable a team.

## What a layer is

A layer is a slab with its own `base_y`, its own shapes, its own islands and its own relief. A cell's
column is that layer's `[floor, top]` shifted by `base_y`, and the **same `(x, z)` may appear on
several layers** — which is the entire feature: two solid spans in one column with air between them.

| Layer | `base_y` | Shapes | Solid span at the middle |
|---|---|---|---|
| `Ground` | 0 | the compiled plan, one island | y0..14 under the terrace, y0..26 on the causeways |
| `Terrace` | 20 | one rectangle, `floor 4`, its own relief | y24..27 |
| `Spans` | 14 | two rectangles, `floor 0`, no relief | y14..15 |

`floor` is the **underside**, measured inside the layer, so the terrace's soffit is `20 + 4 = 24`.
The slab's thickness is its solved surface minus that floor: four blocks here. Everything else about
a layer — relief, themes, the mirror — behaves exactly as it does on the ground.

## The hall

Read across the board at z 47, the shape the whole board exists to make:

| x | column | |
|---|---|---|
| −35 … −21 | `[0..26]` | the west causeway, one solid mass |
| **−20** | `[0..27]` | causeway and terrace **merged** — the step on, one block |
| −19 … 19 | `[0..14]` · `[24..27]` | the hall: floor at 14, soffit at 24, **nine blocks of headroom** |
| **20** | `[0..27]` | merged again |
| 21 … 35 | `[0..26]` | the east causeway |

The causeways are `line` marks on the *ground's* relief — points at `(±27, 36/47/60)`, heights
`16/28/16`, width 8 — climbing one block a cell from the front of the keep to its middle and down
again. Where a causeway's top meets the terrace's top the two columns merge and the join is a single
one-block rise; that is why the terrace was widened from x ±18 to x ±20, because at ±18 one column
of hall floor stood between them and the terrace was an island in the air.

The hall is open at the **back** (the terrace ends at z 57, the floor runs on to z 68 with a worst
step of 2) and looks out over the **void court** at the front: the terrace's first four blocks,
z 36..40, overhang nothing at all.

## Where the objective went

`destroyable-1` is stated at `at: [0, 8]` — cell coordinates, so x 0, z 40 — with `float: 4`, and
nothing in the plan mentions the terrace. It lands at **y34..36**: the terrace's surface at that cell
is y29, the first air above it y30, plus the float. On the same plan with the layers removed the same
destroyable lands at y19..21 on the bare ground. **A placement snaps to the surface top, and the
surface top of a stacked cell is the highest layer's** — so putting an objective on an upper deck is
not stated anywhere; it is a consequence of drawing the deck over it.

`plan/inspect` scores **0**: goal-spawn ratio **3.89** inside `GO1`'s band, the strait **20** blocks
inside `CT12`'s, and the fill ratio inside `G8`'s once the board grew a void court and a split front.

## The bridges

Two slabs, `base_y 14`, `floor 0`, `base_height 2` — so they are two blocks thick with their deck at
y15, level with the front lobes the ground's relief holds flat at 16 (`landing-w`/`landing-e`). They
carry `mirrors: false` and are drawn as an explicit pair about the origin, because a slab on the
symmetry axis is its own `rot_180` image and mirroring would double it onto itself.

They cost one thing, and it is written into the world: **`TerrainBuilder` lays a bedrock course at
y0 under every footprint cell of every layer**, so each bridge leaves a 20 × 20 plate of bedrock in
the void beneath it — `(-32..-12, -10..10)` and `(12..32, -10..10)`, at y0. The terrace's four
overhanging rows do the same over the court. There is no knob for it; the theme's own `bedrock`
value is `0` on both layers and the painter never sees those cells, because it only overwrites stone.

## Three things a layer does to the rest of the pipeline

**Paint is one column per cell.** `TerrainProfile` is built from the surface-top grid — one entry per
`(x, z)` — so a stacked cell resolves *one* band stack, from bedrock up to the highest layer's top.
The ground under the terrace therefore gets no turf, no rim and no wall: its cells fall inside the
`fill` band and come out as fill. Under this board's hall that is stone brick from y0 to y14, which
happens to read as a paved undercroft — but it is not a choice, it is the band arithmetic.

**Theme scope is 2-D.** `ShapeThemeOwners` maps a cell to the smallest-area themed shape covering it,
across every layer, so the terrace's `flag` theme owns the ground beneath it as well. That is what
paves the hall; a ground shape and an upper shape cannot be themed independently where they overlap.

**Dressing lands on the roof.** Every prop resolves against the same surface-top grid. `hall-oak` is
stated at `(8, 53)`, where the ground is the hall floor at y14; the tree stands at **y28..37**, rooted
on the terrace. Nothing can be placed under an overhang, and no decline says so — the prop is simply
somewhere else. The two bridge paths land on the bridges for exactly the same reason, which is what
makes them work.

## What no read shows

Every 2-D read the studio has — `topdown`, `heightmap`, `surface`, `traversability`, `coverage`, and
`relief/read`'s walk — projects the world to one height per column. The hall does not exist in any of
them. `traversability` calls the whole board one component while saying nothing about nine blocks of
covered ground; `coverage` counts the hall's cells as the terrace's. **The only two reads that show a
layer are the isometric preview and `render/section`** — `renders/sec-hall.png` is the cut at z 47,
and it is the picture of this map.

`relief/read` does answer per island, so the terrace's own relief is reported: `island terrace,
cells 880, y28..30, relief 2, symmetry error 0` beside `island team, cells 3550, y13..27, relief 14`.
Heights come back already shifted into world Y.

## What it costs

- `preflight`: codec parity, mirror check on spawn/protection and build, both placements on solid
  ground, spawn↔objective chain connected. **Export gate open.** Nothing declined.
- `coverage`: reached 4990, dead 2915 of 8220 = **35.5%**. The board's arms and its bridges are on
  nobody's journey — each team's objective is on its own island, so the crossing is optional. The
  hall's own cells are not in that count at all, for the reason above.
