# Stacking layers

A layer is a slab keeping one span per column, so a cell may be on several and **the air between them is the
feature**. Row 1 is that gap and the two ways to lose it; row 2 is getting onto a deck and what a third
storey costs. Open the card in the studio as `technique-stacking-layers`, or run `build.py`.

**Every panel is the same 96×76 court with the same one-course deck oversailing it, and the only difference
is the deck's layer.** The court's top block is y13 everywhere; a deck is a rectangle on a layer of its own,
and where that layer's `base_y` sits is the whole of row 1.

## The document

Eight layers: one `court` at `base_y` 0 carrying all six islands and the two causeways, and one layer per
deck, written in `base_y` order because that is the order the world builds them in and `SK20` complains
otherwise.

| panel | the deck's layer | what it built |
|---|---|---|
| `air` | `base_y` 18 | deck at y18 over a court at y13 — **four courses of air** |
| `seam` | `base_y` 14 | deck at y14 resting on the court: no air, and no complaint |
| `driven` | `base_y` 13 | `SK10`, and **no deck course anywhere** — the transect is flat end to end |
| `ramp-meets` | 18, plus a causeway | a one-block rise onto the deck, and `SK11` silent |
| `ramp-short` | the same, a column short | one column of court five below the deck; `SK11` on both masses |
| `three-storeys` | 18 and 24 | spruce at y24, spruce at y18, sandstone at y13 — two gaps in one column |

**A layer's segment top is `base_y + base_height` and its built top block is one lower, which is what decides
where the seam falls.** The court states `base_height` 14 and its top block is y13; a deck at `base_y` 14
rests on it and shares one course by the gate's arithmetic, which is the ordinary seam. One lower than that
is `SK10`.

```json
"layers": [
 {"id": "court", "name": "Court", "base_y": 0,  "layout": {"shapes": [ … ], "groups": [ … ]}},
 {"id": "air",   "name": "air",   "base_y": 18,
  "layout": {"shapes": [{"id": "deck-air", "type": "rectangle", "operation": "add",
                         "floor": 0, "base_height": 1, "theme": "gantry",
                         "min_x": -162, "min_z": -59, "max_x": -58, "max_z": -31}],
             "groups": [{"id": "deck-air", "mirrors": false, "shapeIds": ["deck-air"]}]}}]
```

## The gap, and the one course that is allowed to be shared

**`air` puts the deck four courses clear and the column comes back with the hole in it.** At (−110, −45) the
column reads spruce at y18, then nothing, then sandstone at y13 — and the transect across it steps `BARRIER
+5` onto the deck and `DROP -5` off the other side. The gap survives because `TerrainPainter.Paint` writes
only over stone; that one invariant is what makes stacking work at all.

**`seam` sets `base_y` to the court's own `base_height` and the deck lands on it.** Spruce at y14 directly on
sandstone at y13: no air, one course shared by the gate's reckoning, nothing complained of, and the transect's
worst step is 1. This is the boundary, and it is the last value that is not a fault.

**`driven` is one lower, and the deck is not in the world at all.** `SK10` says *layers 'court' and 'driven'
are driven 2 block(s) into each other over 2,688 column(s)*, and the built column at (110, −45) is fourteen
blocks of court with no spruce in it anywhere. The transect down that panel reads **rises 0, falls 0, worst
step 0** — a flat court, as though the layer had never been written.

**So the only thing that reports a lost storey is the gate at the door.** Nothing downstream can: the world
is built, the column is valid, and a reader looking at the panel sees a court.

## A deck stands on nothing, and the court under it keeps its own paint

**Every deck here oversails its court by four columns, and out there a column is one block.** At (−160, −45)
the column reads a single course of spruce at y18 — no fill, no bedrock, nothing under it to the void.
`TerrainBuilder` plates bedrock under a column whose own floor is the bedrock course or the first block over
it, and a slab standing at a `base_y` of its own is neither.

**The court under a deck is painted exactly as the court beside it.** At (−110, −45), covered, and at
(−110, −78), open to the sky, both columns read sandstone at y13, chiseled sandstone at y12 and stone below.
The court's theme states `fill` as a different block from its surface precisely so that this could be read
off one block, and the two are identical.

**`themes/census` sees both storeys and the seam between them**: 29,760 court cells against 15,408 gantry,
two surface blocks, and 1,016 cells of `court | gantry` border. Theme scope is per layer — `ShapeScopeOwners`
keys on `(layer, x, z)` — so a deck owns the paint on its own storey and nothing below it.

## Getting onto a deck, and the gate that says you cannot

**A causeway meets a deck by arriving one course under it.** `ramp-meets` is a tilted plane on the *court's*
layer — `height_mode: "level"` with `anchor_heights` climbing from 14 at its south end to 19 at its north —
and the transect reads 19 across the deck, then 18, 17, 16, 15, 14 down the ramp. The join is a single
one-block rise and needs nothing else.

**`ramp-short` stops one column early and leaves a slot nothing in the geometry hints at.** The same transect
reads 19 across the deck, **14** at z 59, then 18 back up the causeway: `DROP -5` and `BARRIER +4` a block
apart. `slopes.txt` finds the largest face on the board there, 246 cells at x −48…47, z 58…67.

**`SK11` is what names it, and it is silent on the panel that works.** The store answers *2,912 place(s) of
standable ground … have open sky over them and no route onto them from the rest of the board* for
`ramp-short`'s deck and its court, and says nothing at all about `ramp-meets`. A layered board's
`traversability` still reports one component, because that read discards Y; the gate at the door does not.

## A third storey is two gaps in one column

**`three-storeys` puts a mezzanine at `base_y` 18 and a roof at 24, the roof offset north so half the
mezzanine is still open to the sky.** The column at (110, 35) reads spruce at y24, spruce at y18 and sandstone
at y13 — three spans and two holes, which is the feature stated as plainly as it can be.

**The transect down that panel is a staircase of drops**: `BARRIER +11` onto the roof, `DROP -6` from the roof
to the mezzanine and `DROP -5` from the mezzanine to the court. Everything downstream reads one number per
column — `TerrainBuilder.SurfaceTops` keeps the **maximum** — so a goal, a prop or a placement over this panel
lands on the roof unless it names a layer.

**`xray.png` is the only view any of it appears in**, and it carries the count: *4 roofed void(s), 0 sealed,
largest 21,712 cells at x 58…161, y 14…23, z 25…58.* Four, not six — `seam` and `driven` roof nothing.

## The recipe

**Put the upper thing on its own layer, and set `base_y` at least two above the lower layer's top block.**

```json
{"id": "deck", "name": "Deck", "base_y": <lower top block + 2 or more>,
 "layout": {"shapes": [{"id": "deck-slab", "type": "rectangle", "operation": "add",
                        "floor": 0, "base_height": 1, "theme": "<the deck's own>"}],
            "groups": [{"id": "deck-slab", "mirrors": false, "shapeIds": ["deck-slab"]}]}}
```

- **`base_y` = the lower top block + 1 is the seam**, which is a deck resting on the ground and is legal.
- **one lower loses the slab entirely**, and only `SK10` says so.
- **write the layers in `base_y` order** — the list is what a reader walks and `SK20` complains otherwise.
- **draw the way up**, or `SK11` reports the deck as ground nothing can reach.
- **a covered floor is marked with a shape, not a stroke** — a stroke ignores `layer` and comes back on the
  roof; a rectangle of that floor's own `floor` and `base_height` carrying its own theme lands where drawn.

**A card about layers is finished by what its storeys are made of, not by their angle.** Both themes here are
depth stacks — sandstone over chiseled sandstone for the court, one course of spruce for the deck — because
the `slope` axis answers a landform's question and a deck does not have one.

## What checks it

- `columns.txt` — eight columns, one per claim: the gap, the same court covered and open, the oversail
  standing on nothing, the seam, the deck that is not there, the two gaps, and both sides of the slot.
- `transects.txt` — one line down each panel, with the steps named.
- `slopes.txt` — 43,360 cells walked, 28 scrambled, 1,780 barrier; ten faces, the largest 246 cells in the
  `ramp-short` slot.
- `census.txt` — two themes, two surface blocks, 1,016 cells of border between them.
- `stacking-layers.layout.json` — the one document the board was stored from, posted to
  `POST /api/map/from-documents` with an empty intent and no plan. The store answers with `SK10` once and
  `SK11` seven times, which is most of what this card claims.

Renders: `section-row1.png` and `section-row2.png` (the two rows in orthographic section, which is the
picture a stacked board actually wants), `xray.png` (the roofed voids, with the count) and `iso.png`.
