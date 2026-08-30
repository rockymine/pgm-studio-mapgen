# 24 — a room underground, and the wall that is one polygon

**The technique: a hollow space under the landmass. A floor, a wall that is a single even-odd ring, a
doorway that is an override add and a ceiling on its own layer — and the rule that decides where the
wall's `floor` goes, which is the difference between a room and a wall standing over a trench.**

This forks `02-theme` through `20-undercroft`: the lift and the rock are `20`'s and unchanged, and what
is new is what stands *inside* the hollow. `20` states a hall as a hole in the rock. This states a
**built** room — masonry walls, a doorway, its own vault — in a rock-cut chamber, and dresses it.

## The board

The plan is `02-theme`'s with one number, exactly as `20-undercroft` has it:

```json
"globals": { "surface": 22 }
```

and the finish thins that slab to its top eight courses so the fourteen under it are free:

```json
"shapePropsByHeight": { "22": { "floor": 14, "base_height": 8 } }
```

Landmass `y14..21`. Rock `y0..13`. Everything below is drawn in the fourteen courses between.

## What a hollow space is made of

A layer keeps **one span per column**, so a room with air in it is never one layer. It is a floor, a wall
and a roof distributed over as many layers as the busiest column has spans — and here that is **two**:

| Layer | Order | Holds | Spans |
|---|---|---|---|
| `under` | first (`below: true`) | the rock, the chamber floor, the cell wall, the two door thresholds | `y0..13` rock · `y0..5` floor · `y0..11` wall |
| `vault` | second (`below: true`) | the cell's own ceiling | `y12..13` |
| `ground` | the compiled plan | the landmass, and the flight cut through it | `y14..21` |

**Both storeys are listed before the compiled ground and in bottom-up order.** `drive.py`'s `below: true`
does `layers.insert(0, …)` for each, so the finish lists them **top-down** — `vault` then `under` — and the
posted stack comes out `under, vault, ground`. The painter walks the stack in document order and each pass
paints its whole column, so a storey listed after one standing over it finds no stone left to paint.

**The chamber's ceiling is the landmass's own underside.** Nothing states it: the rock stops at `y13`, the
landmass starts at `y14`, and the eight courses between are the room. A storey's headroom is the gap
between two spans and needs no field.

### The three height words, measured

`floor` is where a shape's base sits, `base_height` is how many blocks it is, `base_y` shifts the whole
layer. The span is `[floor, floor + base_height)` — `base_height` is a **block count**, so `floor 0,
base_height 6` is `y0..y5` and is stood on at `y6`.

`base_y` and `floor` are interchangeable and agree to the block. Measured on a probe board, a lid stated
`base_y: 12, floor: 0, base_height: 2` and one stated `base_y: 0, floor: 12, base_height: 2` both build
at **`y12..13`**. Use `base_y: 0` and absolute floors when the storeys have to be reasoned about against
each other, which underground they always do.

`override` decides which pass a shape is laid in: the algebra is
`((adds − subtracts) ∪ override-adds) − override-subtracts` per layer, so an override add overwrites the
column it lands on *whatever its height is*. That is what a doorway is.

`subtract` is the one that cannot be used here at all, and the next section is why.

## The rock: adds banded round the hole, never a subtract

`20-undercroft`'s finding, reproduced here because it is the first thing that stops an author: a subtract
is a claim about **the whole stack**, not about one layer. Cutting the chamber out of a full-board slab is
refused twice over:

```
POST /map/from-documents   422
SK13  's0' fills 1536 column(s) that 'cut' takes away — from (-24, -16) — 's0' is on layer 'ground'
      and the subtract on 'under', and a subtract reaches only the layer it is on
SK13  'descent' fills 64 column(s) that 'cut' takes away — from (-20, -14)
```

So the rock is four rectangles banded round the excavation, and the excavation is an add:

```json
{ "id": "rk-n", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 14,
  "theme": "rock", "min_x": -50, "min_z": -50, "max_x": 50, "max_z": -16 },
{ "id": "rk-s", … "min_x": -50, "min_z":  16, "max_x":  50, "max_z":  50 },
{ "id": "rk-w", … "min_x": -50, "min_z": -16, "max_x": -24, "max_z":  16 },
{ "id": "rk-e", … "min_x":  24, "min_z": -16, "max_x":  50, "max_z":  16 },
{ "id": "cham", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 6,
  "theme": "floor", "min_x": -24, "min_z": -16, "max_x": 24, "max_z": 16 }
```

A rectangle's `max` is **exclusive**, so bands sharing an edge tile exactly. Counted rather than looked at:
over the board's **10,000 columns, none is bare and none is without a span at `y = 0`** — the second is what
keeps every placement off "over open void".

## The wall: one polygon, and the thickness it actually gives

A hollow ring cannot be a rectangle minus a rectangle — that is a subtract, and `SK13` reads a subtract as
the board's negative space on every layer. It is **one polygon** that traces its outer ring, slits inward,
traces the inner ring the other way round and closes. The fill rule is even-odd, so a ray into the middle
crosses two boundaries and lands outside the fill, and the slit's two coincident edges cancel:

```json
{ "id": "cell", "type": "polygon", "operation": "add", "floor": 0, "base_height": 12,
  "theme": "gaol", "keepClear": true,
  "vertices": [[-8,-6], [8,-6], [8,6], [-8,6], [-8,-6],
               [-5,-3], [-5,3], [5,3], [5,-3], [-5,-3]] }
```

The vertex list is `outer + [outer[0]] + inner_reversed + [inner[0]]`. Nothing special reads it — it is a
vertex list like any other.

**The stated thickness is the built thickness, exactly.** Three rings side by side on one probe board and
the shipped cell beside them, each an `under`-layer add under a landmass, transected across the middle:

| stated | outer box | built west band | built interior | built east band |
|---|---|---|---|---|
| 1 | 12 × 12 | `x −22..−22` (1) | 10 | `x −11..−11` (1) |
| 2 | 12 × 12 | `x −8..−7` (2) | 8 | `x 2..3` (2) |
| 3 (the cell) | 16 × 12 | `x −8..−6` (3) | 10 | `x 5..7` (3) |
| 4 | 16 × 12 | `x 6..9` (4) | 8 | `x 18..21` (4) |

No off-by-one, no gap where the slit runs, and a **one-block** ring closes. The probe's three rings, one
character a column from `x −24` to `x 23` (`#` wall, `.` floor):

```
..############..############..################..     z −14   (all three north bands)
..#..........#..##........##..####........####..     z  −8   (thickness 1, 2 and 4)
................................................     z  −2   (past every outer box: max is exclusive)
```

## Where the wall's `floor` goes, and the gate that will not tell you

The wall is stated `floor 0, base_height 12` — from the **chamber floor's own floor**, not from its top —
and that one number is the whole difference between a room and a fault.

Both shapes are ordinary adds on one layer, so the taller wins each column *floor included*. Where they
share a footprint the wall is taller, so the wall's `[0, 12)` replaces the floor's `[0, 6)` — which is
harmless, because the wall starts where the floor starts and the column is solid either way. Inside the
ring the wall is absent and the floor stands alone. That is the whole construction; no `override` is
needed for the floor.

**State the wall from the floor's top instead and it stands over a trench.** `floor 6, base_height 6` over
a floor of `floor 0, base_height 6` builds this at `(−7, 0)`:

```
GET …/column?at=-7,0     (wall at floor 6)
  y 13..6   Bricks
  (nothing below — no floor, no bedrock)
```

A six-course trench runs round the whole cell block and the wall bridges it. **The board stores at 200,
the export gate opens, and no warning is printed anywhere.** `SK9` is raised — three times — and it does
not reach the wire:

```
GET /api/map/{slug}/findings
  decline SK9  'cham' and 'cell' stack over the same ground on layer 'under', and a layer holds one
               span per column — the world keeps 'cell' and 'cham' is not in it
  decline SK9  'door-n' and 'cell' …
  decline SK9  'door-s' and 'cell' …
```

`Findings.Complaints` filters to `Severity.Complaint` on purpose, `SK9` is the only `Severity.Decline` in
`SketchLayoutCheck`, and every publisher hands the channel that narrowed list. So `SK9` is invisible on
`POST /map/from-documents`, on `sketch/columns`, on `relief/read` and in the `Pgm-Warnings` header, and
readable only at `GET /api/map/{slug}/findings` — which no driver asks for. Filed as `TS68`.

**Ask `GET …/findings` after every stacked build.** It is the only read that answers this one.

## The doorway: an override add at the floor's own height

A gap in the ring would be a second polygon. A threshold is one rectangle:

```json
{ "id": "door-n", "type": "rectangle", "operation": "add", "override": true,
  "floor": 0, "base_height": 6, "theme": "floor",
  "min_x": -2, "min_z": -6, "max_x": 2, "max_z": -3 }
```

The override plane is laid after the ordinary one, so it overwrites the wall's column outright and leaves
the floor's own span in its place. Measured across `z = −5`, the north wall band, `air` below `y14`:

```
x   −6  −5  −4  −3  −2  −1   0   1   2   3   4
    ——  ——  ——  ——  6-11 6-11 6-11 6-11  ——  ——  ——
```

**Four columns wide and six courses tall**, exactly the rectangle stated. The doors are `−z` and `+z`
because the storey covers the whole board and is stamped once (`mirrors: false`): the pair is its own
`rot_180` image, which is what a layer that is not fanned has to be.

## The ceiling: its own layer, and what it costs

The vault is one rectangle on a layer of its own, because a ceiling over a floor is a second span in the
same column:

```json
{ "id": "vault", "base_y": 0, "below": true,
  "shapes": [ { "id": "vault", "type": "rectangle", "operation": "add",
                "floor": 12, "base_height": 2, "theme": "gaol",
                "min_x": -8, "min_z": -6, "max_x": 8, "max_z": 6 } ] }
```

`y12..13`, resting on the wall's own top course, so the cell keeps **six** courses of headroom (`y6..11`)
where the chamber outside it keeps eight (`y6..13`). Drive it two courses into the wall and `SK10` says so
— this one *is* a complaint and does reach the wire:

```
POST /map/from-documents   200  ! 1 SK10
SK10  layers 'under' and 'vault' are driven 3 block(s) into each other over 108 column(s)
      — deepest at (-8, -6) — so they build as one solid mass where they meet
```

108 columns, not 132: the two door thresholds took 24 of the ring's columns back.

**A lid repaints the room under it.** A terrain layer's pass resolves its bands from the bedrock course to
its own top, and the stone-only invariant is all that stops it, so the vault's `fill` claims every *stone*
course beneath it. Measured inside the cell at `(0, 0)`:

```
y 5..4   Coarse Dirt     the chamber floor's own surface band — untouched
y 3..1   Bricks          the vault's fill, reaching down through the floor it stands over
```

The surface band always survives, so this is only visible where the room's floor is thicker than its
`surface.depth`. The remedy is `"kind": "prop"` on the lid layer, which paints it over its own span alone
(`WE56`); re-measured, `y3..1` comes back **Stone**. The trade is that a `prop` layer is also out of
`SK10`'s pair walk and `SK11`'s, so the board loses the gate above. This one keeps the gate.

## The way down

The flight is `20-undercroft`'s, re-anchored. One override-add polygon on the **ground** layer, cut
through the landmass, falling a course a cell:

```json
{ "id": "descent", "type": "polygon", "operation": "add", "override": true, "keepClear": true,
  "floor": 6, "base_height": 16, "theme": "gaol", "height_mode": "level", "skirt": 0,
  "vertices":       [[-20,-14], [-16,-14], [-16,2], [-20,2]],
  "anchor_heights": [    17,        17,       1,       1   ] }
```

`x −18`, head to foot:

```
z  −14 −13 −12 −11 −10  −9  −8  −7  −6  −5  −4  −3  −2  −1   0   1
y   21  20  19  18  17  16  15  14  13  12  11  10   9   8   7   6
```

**Fifteen risers of exactly one course, no repeat** — the head flush with the meadow at `y21`, the foot one
step above the chamber floor at `y5`. An anchor of 17 over a 16-cell run is what removes the doubled tread
`20-undercroft` records; 16 over 16 leaves one, because the surface is sampled at the cell's **centre** and
floored.

Its `floor` is 6 — the first air course over the chamber floor — so the two storeys meet rather than drive
into each other. The flight is on the mirrored `team` group, so there are two of them, one per team.

## What reaches a room under a hill

**A prop has no height of its own. `layer` is the only vertical control there is** — `PlacedProp` carries
`Id`, `Layer`, `Seed` and its own knobs, and nothing else; `DressingContext.GroundFor` answers that layer's
surfaces and `SurfaceTop` where none is named. Measured on this board and one probe beside it:

| prop | stated | built at | says |
|---|---|---|---|
| boulder `(−14,−10)` | `layer: "under"` | cobble **y5..7** | seats on the chamber floor, half-buried |
| boulder `(−14, 10)` | *no layer* | cobble **y21..23** | seats on the meadow over the room |
| boulder `(14, −6)` | `layer: "cellar"` | — | `DR-LAYER` *and* `DR-SITE` at `(13, −7)` — two declines for one prop |
| tree, oak, height 12, `(13, 0)` | `layer: "under"` | log **y6..13**, leaves **y12..13** | seats on the floor; **cut off flat at the rock** and nothing says so |
| flora ring, cell interior | `layer: "under"` | grass at **y6** | grows on the coarse-dirt floor |
| stroke, worn, `z = 10` | `layer: "under"` | cobble at **y5** | **a stroke honours `layer`** — the meadow at `y21` is untouched |
| water pool, `level: 5` | `layer: "under"` | water **y3..5** over gravel **y2** | a sump dug into the cave floor |
| boulder `(0, 14)` | `layer: "under"` | — | `OB19` — *"rests on (0, 13), inside a goal's clearance"* |

Four of those kinds are on the shipped board, at coordinates of their own: straw in the cell, a rubble
boulder in the yard, a worn track from the flight to the door, and a flooded sump in the north-east.
**Nothing is declined and every prop is fanned to both teams.**

Three of those rows are worth stating as rules.

**A stroke honours `layer` now.** `GENERATION-NOTES.md` records the opposite off `opus5-interchange` —
*"a stroke ignores `layer`, so a floor with a roof over it is marked with a shape"* — and `PlaceStroke`
calls `context.GroundFor(path)` like every other placement. A `worn` stroke stated `"layer": "under"` for
`(−6,10) → (6,10)` paves `y5`, the chamber floor's own top course, and leaves the grass at `y21` alone.
The workaround that entry recommends is no longer needed.

**The keep-out mask is 2-D and the claim book is not.** `GroundClaims` is keyed on the layer, so two props
collide only where they share a storey — but `DressingScope.KeptClearAt` is `(x, z)` with no layer at all,
and `SketchRasterizer.KeepClearCells` gathers marked shapes "over every layer". Two consequences, both
measured: a goal's 21-block clearance reaches straight down into the cave (`OB19` above, on a column
sixteen courses under the monument), and a lid marked `keepClear` keeps the whole room under it clear —
a flora field inside the cell placed **0 cells** with the vault marked and **13** without, with no
finding either way. Filed as `TS69`. **Mark the wall, never the roof.**

**`seat: "ground"` does not reach a cellar.** A made-thing layer (`kind: "prop"`, `seat: "ground"`) drawn
inside the chamber at `floor 30` settled to **`y21..23`** — on the meadow — and cut a course out of the
grass under it. `SketchRasterizer.Seat` takes `groundTop` as the **maximum** `YTop` over every non-thing
layer at a cell, and under a landmass that maximum is always the roof. A seated thing cannot be put in a
room; state its floors absolutely. The control proves the other half: the same layer without `seat` stayed
at `y30..32`, exactly where it was drawn.

## What could not be got to work

- **A building inside the room.** A `house` prop with `"layer": "under"` seats and stamps like any other
  prop, but the two attempts here both died on the fan: `DR-CLAIM` — *"building 'h-under' stands on
  (−21, 3), claimed by the channel 'w-under'"* — where the water pool's `rot_180` image landed on the
  house. That is a placement problem, not a capability one; `opus5-interchange` has kiosks standing under
  a concourse. It is out of the shipped board because a 7 × 7 house plus its `StructureClearance` ring plus
  `DR-PASS`'s five-block passage does not fit beside a cell block in a 48 × 32 chamber.
- **A light source.** There is none. `GET /api/openapi/v1.json` has no prop kind for a lamp, a torch or a
  lantern, and `PlacedProp`'s six derived types are `stroke`, `water`, `tree`, `boulder`, `flora`, `house`.
  The gaol is dark, and so are the Backrooms of `maps/opus5-liminal-dtm-ii` for the same reason.
- **A tree that fits.** Nothing reads a room's headroom. A 12-block oak in an 8-course room builds as a
  trunk to the ceiling with two courses of leaves; the rest is simply not in the world.
- **`GO1` on a stacked board.** The plan tier measures a walk over rectangles and knows nothing about the
  storey, so the ratio this board reports is `02-theme`'s, unchanged: score **1.97**, `GO3` and `GO4`
  outside their bands on the base board too. Nothing about the storey moves a plan-level number.

## What to look at

| | |
|---|---|
| `renders/world-xray.png` · `world-xray-turned.png` | the x-ray: the board with everything between the camera and the chamber washed to a fifth of itself, so the gaol is in the picture. `world-iso.png` beside it is the same board and the same camera with nothing washed out, and is a meadow with two houses on it |
| `renders/section-room-z0.png` | the cut across the board — meadow, chamber, the cell block with its vault, the two shafts |
| `renders/section-cell-x0.png` | the cut through both doorways: the vault hanging over an open threshold |
| `renders/section-flight-x-18.png` | the flight, in the one view a grade exists in |
| `renders/under-topdown.png` | `?layer=under` — the storey alone: the ring, the straw, the two sumps, the tracks |
| `GET …/column?at=0,0` | brick fill `y1..3`, coarse dirt `y4..5`, air `y6..11`, vault `y12..13`, landmass `y14..21` |
| `GET …/column?at=-7,0` | the wall: brick `y1..13`, bedrock `y0` |
| `GET …/findings` | the read that answers `SK9`, and the only one that does. `drive.py` asks it on every run |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **1.97**, `valid: true` — `02-theme`'s own answer, unmoved by the storey |
| the storey's tiling | **10,000** columns: bare **0**, without a span at `y0` **0** |
| the chamber | 48 × 32 = **1,536** columns, **8** courses of headroom (`y6..13`) |
| the cell | 16 × 12 outer, wall **3**, interior 10 × 6, **6** courses of headroom (`y6..11`) |
| the doorways | **4** columns wide, **6** courses tall, both faces |
| the flight | **15** risers of **1** course, `y21 → y6`, no repeat |
| `GET …/findings` | **none** |
| the void scan | **6** roofed voids. The chamber is the largest: **10,156** cells at `x −24..23  y 6..13  z −16..15`. Two are `SEALED` — the spawn platforms, 2,176 cells each at `y28..39` |
| `POST …/sketch/dressing` | 8 placements (4 props × 2 images), **0 declines** |
| `GET …/preflight` | export gate **OPEN**, traversability connected, both teams |
| `GET …/coverage` | reached 3,979 · dead 6,021 of 10,000 = **60.2 %** dead — `02-theme`'s empty square, and the storey is under all of it |

```bash
python3 tools/drive.py showcase/24-underground "Gaolstone" --out showcase/24-underground/world
```
