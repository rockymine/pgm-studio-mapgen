# Stacking layers

A layer is a slab keeping one span per column, so a cell may be on several and **the air between them is the
feature**. Every panel here is a gallery — a court, a layer holding its walls, a roof over them — so the
document's stack is the structure, and what the layers made can be read off the board rather than out of an
x-ray. Open it in the studio as `technique-stacking-layers`, or run `build.py`.

**Row 1 is one gallery at three roof heights and row 2 is the way onto it.** Each gallery is 56 long, six
cells deep and open along its south and east sides, because a 2:1 isometric sees about two cells in for every
course of height: a deeper room is a roof with a shadow under it and has to be x-rayed to be read at all.

## The document

Fifteen layers: one `court` at `base_y` 0 carrying all six islands, their paving and the two stairs, then a
`walls-*` and a `roof-*` for every storey, written in `base_y` order because that is the order the world
builds them in and `SK20` complains otherwise.

| panel | walls | roof | what it built |
|---|---|---|---|
| `open` | `base_y` 14, 5 courses | `base_y` 19 | five courses of headroom — the gallery |
| `low` | `base_y` 14, 1 course | `base_y` 15 | one course of headroom. Legal, and nothing says it is useless |
| `driven` | `base_y` 14, 5 courses | `base_y` 18 | `SK10` — and on the wall line there is no roof at all |
| `stair-meets` | as `open` | as `open` | a stair climbing onto the roof, and `SK11` silent |
| `stair-short` | as `open` | as `open` | the same stair a column short: one column of court between |
| `two-storeys` | 14 and 20 | 19 and 25 | planks at y25, planks at y19, andesite at y13 |

**A layer's segment top is `base_y + base_height` and its built top block is one lower, which is what decides
where a seam falls.** The court states `base_height` 14 and its top block is y13, so the walls at `base_y` 14
rest on it and share one course; the walls run five courses to a segment top of 19, so the roof at `base_y` 19
rests on them. Both seams are ordinary and neither raises anything.

```json
{"id": "walls-open", "name": "walls-open", "base_y": 14,
 "layout": {"shapes": [{"id": "back-open",  "type": "rectangle", "operation": "add", "floor": 0,
                        "base_height": 5, "theme": "masonry", "min_x": -106, "min_z": -39,
                        "max_x": -50, "max_z": -35},
                       {"id": "west-open", "…": "…"}],
            "groups": [{"id": "walls-open", "mirrors": false,
                        "shapeIds": ["back-open", "west-open"]}]}}
```

## What one course too low costs, and where it costs it

**`open` is the gallery that works, and its column is the claim.** At (−78, −32), inside it: spruce planks at
y19, then nothing at all, then polished andesite at y13. Five courses of air, and the gap survives because
`TerrainPainter.Paint` writes only over stone — that one invariant is what makes stacking work.

**On the wall line the roof rests on the wall's top course, and that is the seam.** At (−78, −37) the column
reads planks at y19 on mossy stone brick at y18: two layers meeting on one course, which is what a layer's
span being inclusive of its top means.

**`driven` sets the roof one lower and loses it exactly where the wall is.** At (78, −37) the same column
reads mossy stone brick at y18 and **no plank anywhere**: the roof's only course is inside the wall's span and
the wall won it. `SK10` names it — *driven 2 block(s) into each other over 248 column(s)* — and 248 is the
wall line, not the gallery.

**Inside that gallery the roof is still there, at y18, with four courses under it.** So the fault is local and
looks like nothing: a reader sees a gallery, the world is built, and the only thing that reports the missing
roof course is the gate at the door.

**`low` is legal and nobody says a word.** One course of wall gives one course of headroom, the transect steps
`scramble +2` onto the roof rather than the `BARRIER +6` the open gallery gives, and no rule fires. A gallery
too low to walk into is not a thing the studio has an opinion about.

## The floor under a roof, and what the census can see

**A covered floor is marked with a shape, not a stroke.** The gallery's paving is a rectangle of the court's
own courses carrying its own theme, on the court's own layer; theme scope is per layer — `ShapeScopeOwners`
keys on `(layer, x, z)` — so it lands exactly where it is drawn. A stroke would ignore `layer` and come back
on the roof.

**The court under the roof's overhang keeps its own paint.** At (−107, −35), roofed but outside the paving,
the column reads sandstone at y13 — the same two blocks as the open court at (−78, −10). The court's theme
states `fill` as a third block on purpose so this could be read off one block, and covered and open are
identical.

**`themes/census` cannot see the paving at all.** The board states four themes and the census reports three —
court 77.3%, deck 21.2%, masonry 1.5% — because it counts each column's *top* surface and every paved cell has
a roof over it. Everything downstream of a stacked cell reads one number, and `TerrainBuilder.SurfaceTops`
keeps the maximum.

## Getting onto a roof, and the gate that says you cannot

**`stair-meets` climbs from the court to one course under the roof and the join needs nothing else.** The
transect reads 15, 16, 17, 18, 19 up the flight and then 20 across the roof: **rises 6, no barrier**, walkable
end to end. The flight is a tilted plane on the court's own layer — `height_mode: "level"` with
`anchor_heights` — and it arrives against the roof's own southmost column.

**`stair-short` ends one column earlier and leaves a slot.** The same transect reads 19 at the stair's head,
**14**, then 20 on the roof: `DROP -5` and `BARRIER +6` a block apart, and `slopes.txt` finds the board's
largest face there, 322 cells at x −30…29, z 17…38.

**`SK11` is what names it, and it is silent on the panel that works.** The store answers *638 place(s) of
standable ground … have open sky over them and no route onto them from the rest of the board* for
`stair-short`'s roof and its court, and nothing at all for `stair-meets`. A layered board's `traversability`
still reports one component, because that read discards Y; the gate at the door does not.

## A second storey is a second gallery

**`two-storeys` sets walls at `base_y` 14 and 20 with a roof over each, and the column at (78, 26) reads
planks at y25, planks at y19 and andesite at y13.** Three spans and two holes, and every seam between them is
the ordinary one: 14 on the court's 14, 19 on the lower walls' 19, 20 on that roof's 20, 25 on the upper
walls' 25.

**The transect over it steps `BARRIER +12` onto the upper roof and `DROP -12` off the far side**, because
everything reading a stacked board reads the surface top. A goal, a prop or a placement anywhere over that
panel lands on the upper roof unless it names a layer.

## The recipe

**Give the floor, the walls and the roof a layer each, and set every `base_y` to the layer below's top block
plus one.** That is the seam, it is legal, and it is what makes the document's stack the structure.

```json
"layers": [
 {"id": "court", "base_y": 0,  "layout": {"…": "the ground, and the paving shape under the roof"}},
 {"id": "walls", "base_y": <court top block + 1>, "layout": {"…": "back and end walls, N courses"}},
 {"id": "roof",  "base_y": <walls base_y + N>,    "layout": {"…": "one course over them"}}]
```

- **one lower than the seam is `SK10`**, and the slab is absorbed where the layer below reaches it.
- **write the layers in `base_y` order** — the list is what a reader walks, and `SK20` complains otherwise.
- **draw the way up**, or `SK11` reports the roof as ground nothing can reach.
- **mark a covered floor with a shape**, never a stroke: a stroke ignores `layer`.
- **a covered floor is not in `themes/census`**, which counts the top surface per column.
- **keep a room shallow against its headroom** if it is to be seen from above at all.

**A card about layers is finished by what its storeys are made of, not by their angle.** Every stack here is a
depth stack — sandstone over chiseled sandstone for the court, mossy brick on stone brick for the walls, one
course of planks for a roof, polished andesite for a covered floor — because the `slope` axis answers a
landform's question and a building does not have one.

## What checks it

- `columns.txt` — eleven columns, one per claim: the gap, the seam on the wall line, the same line one course
  lower with no roof in it, the covered court against the open court, the two gaps, and both sides of the slot.
- `transects.txt` — one line through each gallery, with the steps named.
- `slopes.txt` — 15,192 cells walked, 292 scrambled, 1,412 barrier; five faces, the largest 322 cells in the
  `stair-short` slot.
- `census.txt` — three themes of the four stated, and the three borders between them.
- `stacking-layers.layout.json` — the one document the board was stored from, posted to
  `POST /api/map/from-documents` with an empty intent and no plan. The store answers `SK10` once and `SK11`
  eight times, which is most of what this card claims.

Renders: `section-row1.png` and `section-row2.png` — each an orthographic cut **through** the galleries, which
is the picture a stacked board wants; `iso.png`, where the paved floors show through the open side; and
`xray.png`, which is the only view that can see a roofed void whole.
