# Made ground meets grown

A shape is either **part of** the ground or **standing in** it, and the document says which with one of two
fields. `relief_scope` says how a shape that is ground takes part in the solve; `height_mode` says the shape
stands out of the field and is applied over ground the relief has already made. They are alternatives rather
than a pair, and 1,332 shapes in this repository's `specs/` state both. Open the card in the studio as
`technique-made-ground`, or run `build.py`.

**Every panel carries the same hillside and the same piece in the same place, so the difference between two
panels is the words on the piece.** The relief falls 26 at the north edge to 10 at the south over a 96×76
island; the piece is a 34×26 rectangle in the middle stating `base_height` 24. Row 1 is the four scopes, row
2 the three skirts and the one panel that states both fields.

## The document

Eight groups on the `ground` layer, each `mirrors: false`. Each group holds two shapes — the island at
`base_height` 44 and the piece at 24 — and a relief of two `area` marks, `brae` at 26 along the north edge and
`strand` at 10 along the south, neither with a `bevel`.

| panel | the words on the piece | what it built |
|---|---|---|
| `inherit` | none | the hillside, untouched — the piece leaves no trace at all |
| `hold` | `relief_scope: "hold"` | a shelf held at **24** across 30 cells, the land re-graded to arrive at it |
| `follow` | `relief_scope: "follow"` | a pad at **18**, which is nothing the document states |
| `exclude` | `relief_scope: "exclude"` | a plinth at **44**, which is the *island's* `base_height` |
| `sheer` | `height_mode: "level"`, `skirt: 0` | a plate at 24, 26 cells of it, with a ten-block drop off its south edge |
| `skirt-6` | the same, `skirt: 6` | 15 cells of plate, eased into the hill either side |
| `skirt-14` | the same, `skirt: 14` | **2 cells** of plate — the skirt ate it |
| `both-words` | `height_mode` **and** `relief_scope: "hold"` | identical to `sheer`, in all 7,296 columns |

```json
{"id": "piece", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 24,
 "theme": "moor", "min_x": -17, "min_z": -13, "max_x": 17, "max_z": 13,
 "relief_scope": "hold"}
```

## The four scopes, and what each of them actually pins

**A shape with no word is a footprint and nothing else.** The `inherit` panel's profile is the bare
hillside, 26 down to 10 without a step in it: the piece stated `base_height` 24 and the island stated 44, the
taller add won every column, and the relief ran through the footprint as if it were not drawn.

**`hold` pins the height the shape states and the surrounding field is solved knowing where it has to
arrive.** The pad holds 24 across 30 cells — four wider than the piece, because the relaxation flattens
just outside a rigid mark — and the approach above it is compressed into nineteen cells against the bare
hillside's eleven. The land was re-graded to meet the shelf, which is the point of the word.

**`follow` does not mean the terrain is left alone: it seats the shape and then solves the group again.**
The pad comes out at 18, which appears nowhere in the document — `SeatOf` reads the field just outside the
footprint on every edge and takes the **median**, then pins that as a rigid mark and re-solves. So the ground
around a `follow` shape is re-graded exactly as `hold`'s is, and the only difference is who chose the height.

**`exclude` keeps the raw column, and the raw column is not the excluded shape's.** The piece states 24 and
the plinth came out at **44** — the island's `base_height`, because the taller add still wins the column and
`exclude` only says the *relief* may not answer for it. Rebuilt with the island at 30, the plinth reads 30.
A shape wanting a plinth at its own height has to be the tallest add over its cells, or say `height_mode`.

## `skirt` is the whole of whether an erected shape is a landform or a monument

**`height_mode: "level"` cuts a flat top at an absolute height and the skirt decides what its edge does.**
All three panels of row 2 state the same top, 24, over a hillside standing at 22 at the piece's north edge
and 14 at its south — so the plate is a two-block step up on one side and a ten-block drop on the other.

**A `skirt` eases linearly from the ground just outside the outline to the shape's own surface, and it is
paid for out of the plate.** `skirt: 0` leaves all 26 cells of plate; `skirt: 6` leaves 15; `skirt: 14`
leaves **2**, because fourteen cells in from each of two edges twenty-six apart is twenty-eight and there is
nothing left in the middle. The same arithmetic governs a mark's `bevel`.

**So the number to choose is the skirt against the lift, not the skirt on its own.** Ten blocks of drop with
`skirt: 0` is a plinth, with a skirt near half the lift is a lip crossed with a placed block, and with a
skirt at or over the lift is a landform walked onto from any side — and `skirt: 0` is what 1,738 of the 1,802
erected shapes in `specs/` state.

## A shape stating both fields has the scope ignored, and nothing says so

**`both-words` states `height_mode: "level"` with `skirt: 0` *and* `relief_scope: "hold"`, and comes out
identical to `sheer`, which states only the first.** Compared column by column over both panels' 7,296
columns: **not one differs in height, and none differs in material** once the rock band's `cell` pattern is
allowed for — the 92 cells that read stone against cobblestone are the pattern's world phase, since the two
panels stand 330 blocks apart.

**The mechanism is one line: `ScopeOf` returns `Inherit` for any shape that declares a `height_mode`.** A
`height_mode` shape is applied after the solve, so the field bound without ever being asked about it; the
scope is not overridden or merged, it is never read.

**Nothing refuses it, and nothing complains.** The store answers 200, the relief read reports no finding
against the group, and `RQ3` does not fire because the field *was* read — it was read and discarded. The only
way to see it is to build the shape twice.

## What the relief read can and cannot see

**`relief` reads 16 on all eight groups and `landform` reads `rolling` on all eight**, which is the
hillside's own range, while the built worlds run from a bare slope to a 44-block plinth. An erected shape is
applied after the solve, so the readback measures ground that does not contain it; an excluded one is out of
the group, so its cells are not counted either.

**`level` sees a `relief_scope` and is blind to a `height_mode`.** It reads 0.18 on `inherit` and on all
three erected panels, 0.44 on `hold`, 0.35 on `exclude` and 0.32 on `follow` — so the three words that enter
the solve move it and the three skirts do not.

**`RL5` fires on five of the eight groups, `sheer` among them**, saying the group *presents no face at all —
it is a ramp end to end*. That is true of the solve and false of the world: the `sheer` panel has a ten-block
cliff round a plate on it. A complaint about faces is a complaint about the relief, and an erected shape is
not in the relief.

## The recipe

**Pick the field by asking whether the thing is ground.** A terrace, a shelf, a dale floor, a walled town's
platform — those are ground, and take a `relief_scope`. A plinth, a pad, a flight, a built plate — those
stand in the terrain, and take a `height_mode` with a `skirt`.

```json
"a shelf the valley runs up to":   {"relief_scope": "hold"}
"a floor that keeps level wherever the land puts it": {"relief_scope": "follow"}
"a citadel on its own plinth":     {"relief_scope": "exclude", "base_height": <taller than the island>}
"a built plate":                   {"height_mode": "level", "skirt": 0}
"an outcrop belonging to the terrain": {"height_mode": "level", "skirt": <at or over the lift>}
```

- **never both on one shape** — the scope is read and discarded, silently.
- **`follow` re-solves the group**, so it is not the gentle option: it re-grades the land as much as `hold`.
- **`exclude` gives the island's height**, not the shape's, unless the shape is the taller add.
- **a `skirt` is paid for from both sides**, so a skirt over half the piece's narrow dimension leaves no top.
- **read `level`, not `relief`** — and neither of them sees an erected shape at all.

## What checks it

- `transects.txt` — one line north to south through each panel, crossing the piece.
- `relief-read.json` — the eight groups: `relief` 16 and `landform: rolling` on every one, `level` moving
  only with the scopes, and the five `RL5` complaints.
- `slopes.txt` — 57,431 cells walked, 357 scrambled, 580 barrier; five faces, the largest 236 cells at
  x 147…182, z −59…−32, which is the `exclude` panel's plinth.
- `incline.txt` — 55.6% of the board stands between 10° and 19°, which is why the bands are cut at 25° and
  45° here rather than the 15° and 40° the flat-ground cards use.
- `census.txt` — one theme, four surface blocks.
- `made-ground.layout.json` — the one document the board was stored from, posted to
  `POST /api/map/from-documents` with an empty intent and no plan.

Renders: `scope-row.png` (inherit, hold, follow, exclude), `erected-row.png` (sheer, skirt 6, skirt 14, both
words) and `iso.png` (all eight).
