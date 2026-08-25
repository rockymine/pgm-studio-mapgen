# Sandcaster II — a range around an open board, and the workings under it

`maps/opus5-sandcaster-ii` · `specs/opus5-sandcaster-ii` · **100 × 400 blocks**, 100 × 200 a side ·
destroy, two destroyables a team · `rot_180` · 24 players

The first Sandcaster answered "tunnels, two destroyables, 100 × 200 a side, organic border, three
landscapes, brush-painted, extreme relief, an uncanny underground". This one answers the two things that
were wrong with it: it was **cut into arms** by a chasm, which is not a playing ground, and it was **flat**,
because the relief was pinned rather than sculpted. Nothing else is a criticism of the first board — it
stays as it is.

## What changed, and why

**One landmass instead of two arms.** The plan is six nested rectangles down one half, mirrored: a strait
40 blocks deep at the front, a basin and a shelf at the full 100-block width, a holt narrowing behind
them, an apron and a spawn. They compile to **one shape**, whose outline is replaced by a wandering coast
(`shapePropsById`). There is no chasm, no gap link and no island pair — a player crossing the board never
meets an edge until the coast.

The widths are not all the same on purpose. Three collinear, land-joined pieces in a row make one chain,
and `LN2` measured it at **120 blocks** against a band of 25–110; giving the strait, the basin and the
shelf three different widths breaks the chain and costs nothing else. The board scores **1.369**, the same
as the first Sandcaster, with one soft violation.

**The range is drawn with pushes.** A relief mark is a constraint honoured exactly, with no falloff of any
kind: a `point` summit is a flat drum on a sheer wall and a `line` ridge is a wall with a flat top. Both
were built, on `showcase/19-mountain-range`, before this board was. A **push** takes a drawn ring and lifts
the solved surface inside it, and three of its fields are the landform — `amounts` per ring vertex so the
crest falls along the arc, `crown` (record default **0**) to lift the ring's own medial axis into a crest,
and `falloff` for the skirt. Six pushes make the range: a massif and a spur a side, plus a corrie bitten
out of each massif's inner flank by a **negative** crown.

**And four marks pin the rest.** The coast, the open floor down the middle, the goal's shelf and the
spawn's apron — every one of them ground a player has to walk. The first Sandcaster pinned all four of its
regions with `area` marks at their own heights, which is exactly why it was flat: a board with a mark on
every region is a table with bumps on it however tall the bumps are. Here the flanks carry no mark at all.

Read back: `low 21 · high 76 · relief 55 · symErr 0`, against the first board's relief of 23.

## The three landscapes

Painted, not cut. The board's own theme is `wash` — a dune field — and four region-scale strokes are laid
over it before the detail strokes: `crag` along each massif's own ribbon, `reef` over the east of the
middle, `holt` over the back. **Paint scopes to the smallest shape covering a cell**, so a region stroke is
a ground the detail is read against rather than a layer that hides it: the summits, scree, clefts, dune
crests, swales, pans, understorey and tracks are all smaller strokes over it, and each of them wins its own
cells.

Twenty-three themes on one hue axis. The reef is the cool pole and the wash the warm one; the holt is the
green that ties them; the range is the reef's own family stood on end — `crag`, `summit`, `shadow` — so a
mountain adds no fourth palette. The corridor under it all is the same value range gone cold and
institutional, and nothing on the board is saturated except one prismarine accent in the drained pool and
the obsidian goal.

Every stroke is placed **off a spine or a landform** rather than typed as a coordinate, so moving a massif
moves its paint, and every vertex is **clamped into the land**: a stroke reaching past the coast is the only
add on that column and builds a speck of bedrock standing over the void.

## The workings

| Thing | At | Reads |
|---|---|---|
| the corridor | `x −14..−2, z 62..148` | floor y0..6, air y7..14, lid y15..21 |
| the drained pool | `x −12..−4, z 79..93` | basin y0..3, two prismarine lanes |
| the cistern | `x −14..−2, z 102..124` | the goal at y11..13, on layer `under` |
| four bays | off the east wall at `z 72, 92, 112, 132` | five blocks square, one bench each |
| two light wells | `x −11..−7, z 70` and `z 138` | the only daylight, fifteen blocks over the floor |
| the south way in | ramp `z 32..62`, cutting `z 32..58` | y21 at the mouth falling one course every two blocks to y6 |
| the north way in | ramp `z 148..178`, cutting `z 152..178` | the same, coming up in the holt |

Read at `(−8, 112)`, in the cistern: `y0..7` floor · **`y11..13` the goal** · `y15..21` lid. Read at
`(−8, 70)`, under a light well: `y0..6` and open sky. Read down the south ramp every two blocks:
`21 21 20 19 18 17 16 15 14 13 12 11 10 9 8` — 15 courses over 30 blocks, **one-block treads the whole
way**, because a slope of one course a cell builds as treads of two and a two-block rise is a placed block
to climb.

**The end walls are drawn in halves, clear of the ramp between them.** This is the bug that cost this board
three builds and that the first Sandcaster shipped with. Among the shapes of one layer the **taller**
override-add wins the column — not the later one — so a wall drawn across a ramp does not lose to it, it
**plugs** it. Measured on this board before the fix: `(−8, 60)` read solid `y0..21` with no air in it, a
three-block plug at `z 59..61` sealing both mouths, and `SK11` reporting 676 and 294 places of standable
ground with no route onto them. The same fix is now in the first Sandcaster's spec.

## What it measures

```
score 1.369 · valid true · symErr 0
goal destroyable-1 (The Beacon)  own 95 enemy 322 ratio 3.389   (GO1 wants 3.0–4.0)
goal destroyable-2 (The Cistern) own 89 enemy 312 ratio 3.506
island team: cells 10996 · low 21 · high 76 · relief 55
export gate OPEN · <maxbuildheight> 96 · 4 region files
coverage: reached 24022 · dead 2362 of 26424 = 8.9%, every patch 1 block from used ground
provenance: tree 40 · boulder 18 · flora 10 · stroke 4 · destroyable 4 · spawn 2 · ironcube 2
dressing: nothing declined
```

Transect at `z = 96`, every fourth block from `x = −48`:

```
-- 66 68 67 65 76 75 40 21 21 21 21 21 21 21 21 24 36 48 59 57 58 56 -- --
```

Thirty-two blocks of dead-flat floor down the middle with a range on each side of it. `render/traversability`
answers **one component**, all four goal markers connected, and that includes the workings.

## What it refuses, and what that costs

**`G8`, fill-ratio 0.775 against a band of `[0.201, 0.542]`.** The only violation, and it is the shape of an
open board: a landmass with no holes in it fills its bounding box, and the band was learned from boards that
have holes. The alternative is cutting the middle up, which is what this map was asked not to be.

**`WX4`**, one complaint: the spawn pad shifts inward to keep wall clearance and the exported spawn point
moves with it. Informational.

**8.9% dead ground is the range.** Every dead patch is one block from used ground and all four of the big
ones are mountain flank — a mountain is scenery, and scenery is ground no journey passes. It is the honest
price of the technique, and at 400 blocks long it is a frame round a playing field rather than half the
field, which is what the same pushes cost on a 90-block board (24%).

## Two readings, not faults

**The Sketch tool's 3-D preview draws this board flat.** The world has the range — `/column` reads 66..76
on the flanks against 21 in the middle, and `render/heightmap` draws the contours — and the preview's own
`POST …/sketch/columns` payload carries tops in the forties, but the WebGL canvas renders one level.
Filed as a question against pgm-studio rather than answered here; the boards to compare are this one
(stacked) and `showcase/19-mountain-range` (one layer), where the same preview shows the relief.

**`SK11` on the first Sandcaster's workings, and not on this one's.** The same end-wall fix cleared it here
and did not clear it there, while both boards' `render/traversability` answers one component and both
boards' ramps read continuous block by block. What is certain is that the plug it pointed at on this board
was real. What it is still pointing at on the other one is not something a column read or a traversability
render will confirm, and it is written up as a reading rather than a fault.
