# Hollows

A hollow is ground lower than what is around it, with a floor things stand **in** rather than on. The studio
offers three instruments that could cut one and they are not interchangeable. The card holds all three side
by side: a negative relief **push** at x −32, a **sink** shape at x 32, and an **area mark** at x 96, each
asked for the same 36×36 floor twelve blocks down. Open it in the studio as `technique-hollows`, or read
`hollows.layout.json`.

**The short answer is that a push is the hollow instrument and the other two are something else.** A push
states the floor and grades the wall outside it; a sink stamps a flat plate through whatever the ground is
doing; an area mark states a height for the ground to arrive at, which is a basin rather than a pit and which
takes the whole island with it when it is stated alone.

## The document

Three groups on the `ground` layer, each `mirrors: false`, on a board whose `setup.mirror_mode` is `none`.
Each plot is a 56×56 rectangle at `base_height` 32; the centres are 64 blocks apart. The ground theme carries
a `layered` surface on the **`slope`** axis — 0–30° grass over dirt, 30–45° gravel, 45–90° cobble over stone —
so the wall each instrument makes paints itself.

| Plot | Group | What states the hollow | Built floor | Built wall |
|---|---|---|---|---|
| `push` x −60…−4 | `push` | a push, `amount` −12, `falloff` 6, `crown` 0, over a 36×36 ring | x −50…−15, 36 cells | x −55…−51, `31 29 26 23 21` |
| `sink` x 4…60 | `sink` | a 36×36 rectangle, `height_mode: "sink"`, `base_height` 12, `skirt` 0 | x 14…49, 36 cells | none — `32` then `20` |
| `mark` x 68…124 | `mark` | a `land` area mark at `h` 32 and a `basin` area mark at `h` 20, `bevel` 4 | x 82…109, 28 cells | x 78…81, `30 28 24 22` |

The `push` and `mark` plots each carry a `land` area mark holding their own ground at 32, and the `sink` plot
needs none because its hollow is stamped after the solve. Nothing else stands on any of the three floors: a
hollow is terrain, and the card is a reading of terrain.

```json
"push": {"base": 32, "reach": 0, "step": 1,
  "marks": [{"id": "land--32", "kind": "area", "h": 32, "bevel": 0,
             "ring": [[-60, -28], [-4, -28], [-4, 28], [-60, 28]]}],
  "pushes": [{"id": "pit", "ring": [[-50, -18], [-14, -18], [-14, 18], [-50, 18]],
              "amount": -12, "falloff": 6, "crown": 0, "roughness": 0, "seed": 1}]}
```

## A push's ring is its floor, and `falloff` is the wall outside it

**A negative push gets exactly the depth it asks for and nothing clamps it.** Swept from −1 to −48 on a
fixed ring, depth achieved equals the amount asked at every value and the floor is dead flat — all 961 cells
of a 32×32 ring at the floor's own level. Past the base it keeps going: the solved field reaches y0 at −32
and **y−16** at −48, because a push is applied to the solved surface rather than constrained into it.

**There is no ring too small for it either.** A 2×2 ring is a one-cell floor twelve blocks down; a 48×48 ring
is 2,209 flat cells at the same depth. The wall lies wholly outside the ring in both.

**`falloff` decides how far out the mouth stands and how steep the wall is, and never touches the floor.**
The grade is `amount / falloff` blocks a cell, so −12 over 6 is the `21 23 26 29 31` this board builds; at
`falloff` 0 or 1 the drop is sheer in one cell, and at 12 or more it is a bowl. **A push's mouth is therefore
its ring grown by `falloff`** — 36 cells of floor under a 46-cell mouth here.

**The wall's worst step is what an author is really choosing, and the three plots read 3, 12 and 4.**
`transects.txt` names them: the push's `falloff` 6 wall is `2 barrier, 2 scramble, worst step 3`, the
sink's sheer wall is one `DROP -12`, and the mark's `bevel` 4 wall is `worst step 4`. A hollow players
have to climb out of wants a wider `falloff` or a ramp cut into it.

## `crown` domes upward even when the amount is negative

**This is the one nobody can guess: `crown` is signed in world space rather than against the push's own
direction.** The floor's centre comes out at `base + amount + crown` exactly. A positive crown fills the
pit's middle back in, and at `crown` 12 against `amount` −12 the centre is level with the surrounding ground
and the hollow is a moat round an island.

**A pit wants `crown: 0` and the inspector's own default is 2.** At `crown` 2 only 477 of the 961 floor cells
are level; at 3.5, 285; at 6, 177. It dishes into a basin only when the crown is stated negative — `crown` −6
against `amount` −12 puts the centre six blocks below the floor's edge.

**Any non-zero crown raises `RL6` at this size, so the read agrees.** Over a 32-block ring the crown's grade
is measured to a medial axis about sixteen cells in, which cannot come within twice a skirt of 2 blocks a
cell whatever it is set to. `crown 0` is the only setting the relief read passes.

## A sink is a flat plate, not a landform

**`base_height` on a `sink` shape is the depth in blocks, and the floor is the median ground under the
footprint minus it.** A `base_height` of 0 still sinks one block. The word is read by the erect pass, which
runs after the relief is solved, so the surrounding ground is untouched and the mouth is exactly the outline
drawn.

**Unlike the push it is clamped, and the clamp is not the sink shape's own `floor`.** The erect pass writes
`max(column floor + 1, top)` against the *column's* floor, so `base_height` 31, 32, 40 and 64 all bottom out
at y1 on this board, and stating `floor` 10 or 20 on the sink changes nothing.

**A `skirt` on a sink grades inward and is paid for out of the floor.** `skirt` 2 takes 36 cells of floor to
32, `skirt` 8 takes it to 20; the mouth stays where it was drawn. That is the mirror image of a push's
`falloff`, which grades outward and costs the mouth instead.

**The relief read cannot see a sink at all.** `relief-read.json` reports the sink group as `relief: 0`,
`landform: "plain"`, `level: 1`, with no seams and nothing to complain of, while the world holds a
twelve-block sheer-walled pit. Everything that read says about faces, seams and level ground is said about
the solve, and a sink is not in it.

## An area mark states a height, and alone it moves the island

**One `area` mark at a low `h` does not make a hollow — it flattens the whole island to that height.** The
mark plot with `basin` alone reads 20 at every ground station across the plot, wall to wall. A relief's `base`
is what an unmarked field settles at rather than a rim the marks are cut into, and with a single constraint
the smoothest field is the constant one.

**A hollow needs a second mark holding the land, and then `bevel` grades the wall inward.** `land` at `h` 32
over the whole plot, then `basin` at `h` 20: `bevel` 0 is sheer, 2 costs four cells of floor, 4 costs eight,
8 costs sixteen. **`tread` does nothing on an area mark** — the profile with `tread: 8` is the `bevel: 0`
profile block for block.

**The bevel is the one wall of the three the relief read calls a seam.** The `mark` group reports
`basin | land-96`, step 2, 144 cells, at (78, −18) — two marks stating different heights along a shared edge,
which is what a seam is. The push's wall is one mark's own grade and raises nothing.

## What each is for, measured on tilted ground

**A push's hollow rides the ground it is cut into; a sink's does not; an area mark's replaces it.** With each
plot tilted from 40 in the west to 24 in the east and the same hollow asked for in the middle:

| | the floor came out |
|---|---|
| `push` amount −12 | falls from 26 at the ring's uphill edge to 14 at its downhill edge — the tilt minus twelve |
| `sink` base_height 12 | flat at 20 the whole way, the median minus twelve; uphill wall 18 deep, downhill wall 6 |
| `area` mark h 26 | flat at 26, with the whole tilt around it pulled into the grade that reaches it |

**So a push is a quarry whose floor drains one way, a sink is a pad, and an area mark is a valley floor.**
Choose by which of those three the map wants, not by which knob is nearest.

## The paint's slope axis sees every one of the three walls

**All three walls read as face and take the rock band, and so does the outermost cell of every floor.** The
incline in each `column` header, against the theme's 0–30 / 30–45 / 45–90 stack:

| cell | incline | surface |
|---|---|---|
| push floor (−32, 0) | 0° | Grass Block |
| push floor's outermost cell (−50, 0) | 37° | **Gravel** |
| push wall (−53, 0) | 68° | **Cobblestone** |
| sink floor (32, 0) | 0° | Grass Block |
| sink floor's outermost cell (14, 0) | 72° | **Cobblestone** |
| sink rim lip (13, 0) | 72° | **Cobblestone** |
| mark floor (96, 0) | 0° | Grass Block |
| mark floor's outermost cell (82, 0) | 45° | **Cobblestone** |
| mark wall (80, 0) | 68° | **Cobblestone** |

**The buildable floor is therefore one cell smaller each way than the geometry says.** A sheer wall claims
two cells — the lip outside and the floor cell inside — and a graded one claims the floor's edge at the
shoulder band. Board-wide `incline` reads 68.1% at 0–9° and 22.6% at 40° or steeper.

## The recipe

**A pit you can build in is a negative push with `crown: 0`, a `falloff` of about half the depth, and an
area mark holding the land around it.** Twelve blocks down with a 36×36 floor, on ground standing at 32:

```json
"relief": {"<group>": {"base": 32, "reach": 0, "step": 1,
  "marks": [{"id": "land", "kind": "area", "h": 32, "bevel": 0, "ring": <the island>}],
  "pushes": [{"id": "pit", "ring": <the floor, 36x36>,
              "amount": -12, "falloff": 6, "crown": 0, "roughness": 0, "seed": 1}]}}
```

- **`crown: 0`** — a positive crown domes the floor up, a negative one dishes it, and either raises `RL6`.
- **`falloff` 6 at depth 12** is a 2-blocks-a-cell wall whose worst step is 3, and it paints from the
  45–90° band; 0 to 3 is a cliff, 12 or more is a bowl.
- **the `land` mark is not optional** the moment anything is pinned inside the ring.
- **the buildable floor is the ring less one cell each way**, because the outermost floor cells read as face.

**Use a `sink` shape instead wherever the floor has to be one flat plate whatever the ground does** — an
arena, a loading yard, a pad a building is seated on. `base_height` is the depth, `skirt` is paid for out of
the floor, and the erect pass runs after the solve so nothing can feed back into it.

**Do not reach for an `area` mark to make a pit.** It states a height for the ground to arrive at, which is a
basin or a valley floor; alone it takes the whole island with it, and it needs a second mark holding the land
before it makes a hollow at all.

**The `land` mark is load-bearing rather than tidy, because a pin inside the ring applies the push twice.**
`compare.txt` §8 is the probe: with a room inside the ring and no `land` mark the rim reads 20 and the floor
8, and the mark restores the profile station for station. The law is in `GENERATION-NOTES.md`, under relief.

## What checks it

- `transects.txt` — the three hollows along z 0, station by station with the steps named.
- `compare.txt` — the sweeps: push `amount` −1 to −48, `falloff` 0 to 48, `crown` −6 to 12 with the relief
  read's two gradients beside each, ring sizes 2×2 to 48×48, the sink's depth, clamp and skirt, the area
  mark's `bevel` and its do-nothing `tread`, the pin collapse and its fix, and all three on tilted ground.
- `columns.txt` — each floor, its outermost cell, its wall and its rim, with the incline in every header.
- `relief-read.json` — the three groups. `push` and `mark` read `relief` 12 over 3,136 cells; `sink` reads
  `relief` 0 and `landform: "plain"`, which is the read being blind to it. The only seam on the board is the
  `mark` group's bevel.
- `slopes.txt` — 7,580 cells walked, 816 scrambled, 1,012 barrier, three faces, the largest 476 cells.
- `incline.txt` and `census.txt` — the angle histogram, and one theme over 9,408 cells in three surface
  blocks.
- `hollows.layout.json` — the one document the board was stored from, posted to `POST
  /api/map/from-documents` with no plan and no intent. A terrain card needs neither: the renders read the
  stored layout through `POST /sketch/columns`.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
