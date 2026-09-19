# Marks and pushes

A relief is solved in two steps and the whole card is that fact: **the marks negotiate with each other and
are solved first; the push is added to the answer.** A mark is a constraint — this cell *is* this height —
and a push is an arithmetic lift applied afterwards to whatever the solve produced, which means a push cannot
see a mark, cannot be kept off one, and does not flatten what it raises. Open it in the studio as
`technique-marks-and-pushes`, or run `build.py`.

**Row 1 is one dale and one push, the push in two places.** Row 2 is the other half of the same question —
how much of a panel to pin — with the same push on all three. Every panel is a 96×76 island and the push is
byte for byte identical in the four that carry it, so the read returns the same two grades, 1.33 and 0.83,
every time.

## The document

Six groups on the `ground` layer, each `mirrors: false`, on a board whose `setup.mirror_mode` is `none`.

| panel | states | what it built |
|---|---|---|
| `dale` | `land` at 20 over the panel, `holm` at 12 inside it, `bevel` 6 | 20 wall to wall, 12 in the holm — `relief` 8, `plain`, 90% level |
| `push-on-it` | the same, plus `fell` centred on the holm | a hill whose summit runs 33…38 — `relief` 18, `rolling` |
| `push-beside-it` | the same, plus `fell` twenty cells west | the holm's floor reads 27, 20, 12 across ten cells — `relief` 33, `hills` |
| `pinned` | `coast` 10, `holm` 20, `shelf` 30 as bands tiling the panel, plus `fell` | three plates — `relief` 45, **`mountain`**, 45% level |
| `free-flanks` | the same three heights pinned only where a player stands, plus `fell` | ground that flows — `relief` 34, `hills`, 19% level, `RL5` |
| `reach` | `free-flanks`' document with `reach: 16` | the shelf and the fell come apart — `relief` 25, 24% level, `RL5` |

The dale needs **two** marks and not one. A lone constraint has nothing to negotiate with and the smoothest
field through it is the constant one, so a single `holm` at 12 flattens the whole panel to 12 rather than
cutting a dale into it.

```json
"push-beside-it": {"base": 20, "reach": 0, "step": 1,
  "marks":  [{"id": "land", "kind": "area", "h": 20, "bevel": 0, "ring": <the panel, inset 3>},
             {"id": "holm", "kind": "area", "h": 12, "bevel": 6, "ring": <a lobed ring, radius 14>}],
  "pushes": [{"id": "fell", "ring": <a lobed ring, radius 13>, "amount": 16, "falloff": 12,
              "crown": 9, "roughness": 0, "seed": 1}]}
```

## A push is added to the solve, so it carries the ground rather than replacing it

**`push-on-it` puts the fell's ring exactly over the holm's, and the hollow does not fill in — it goes up.**
The dale under the ring falls 20 → 12; the summit above it runs 38 at the rim down to 33 in the middle and
back to 37. Twenty cells of summit, none of it flat, and the shape it carries is the dale's.

**Nothing in the document or the read says so.** The group reads `relief` 18, `landform: rolling`, one push
with two sane grades and no finding at all — which is true of the numbers and says nothing about a hilltop
with a bowl in it. A transect across the ring is the only thing that answers it.

**So a landform meant to have a flat top needs flat ground under it.** Pin what the push will stand on, or
accept the shape the solve left there; a `crown` cannot iron it out, because the crown is added to the same
sum rather than levelling it.

## A push cannot be kept off a mark — only its ring and its falloff can

**`push-beside-it` moves the same push twenty cells west, clear of the holm's ring, and the holm still comes
up.** Along z −45 the mark states 12 and the ground reads **27 at x 106**, **20 at x 110** and its stated
**12 only at x 115** — five cells east of the holm's own centre. The `dale` panel reads 12 at all three.

**The skirt is what did it, and the skirt is not a keep-out.** `falloff` 12 outside a radius-13 ring reaches
twenty-five cells from the push's centre, and every cell inside that radius gets its eased share added —
pinned or not. A mark is honoured in the solve and then has arithmetic done to it.

**There is no field that says otherwise, so the only control is distance.** Ring plus `falloff` is the
push's whole extent: keep that circle off the ground a mark has to deliver, or state the mark at the height
you want *after* the push has been added, which is guessing.

## How much of a board to pin, and the read that says when you are wrong

**`pinned` states every region as a mark and builds three plates.** Coast 10, holm 20, shelf 30, each a band
across the panel: north to south the ground holds 30 for twenty-three cells, ramps nine to 20, holds that
for fifteen, ramps nine more to 10 and holds it to the south edge. The only thing on the panel that is not a
plate or a ramp between two plates is the push.

**The read calls it a mountain.** `relief` 45 and `landform: mountain`, because the numbers see a 45-block
range and cannot see that the range is a staircase. `level` is the field that does see it: **0.45**, against
0.90 on the flat `dale` and 0.19 on `free-flanks`.

**`free-flanks` pins the same three heights only where a player stands on them and leaves the rest to the
relaxation.** The coast becomes an eight-cell strip at the panel's edge, the holm a radius-15 ring, the shelf
a radius-10 one, and the ground between them flows. `relief` 34, `landform: hills`, and the fell now rises
out of terrain instead of off a plate.

**And the read complains about that too, which is the actual trade.** `RL5` fires on `free-flanks` — 19%
level ground, the largest run of it 7% of the group, against five faces: *the elevation was graded everywhere
and left nowhere to stand.* Neither 0.45 nor 0.19 is the answer; `level` is the dial, and a board is pinned
where it is played and free where it is looked at.

## `reach` decides whether unpinned ground is terrain or a sag

**`reach: 16` on the same document pulls every cell more than sixteen from a constraint back toward `base`.**
Down the panel's unpinned middle at x 0 against x 110, the same forty cells fall 23 → 18 under `reach: 0`
and hold 12 → 15 under `reach: 16` — the field has sagged to within a few blocks of its `base` of 6.

**Built, that is the difference between one landform and three.** The shelf and the fell stand as separate
mounds on low ground in the `reach` panel and are joined by flowing flank in `free-flanks`; `relief` falls
from 34 to 25 and `level` rises from 0.19 to 0.24, because a sag is level ground too.

**`reach: 0` is therefore the default a board wants, and a finite reach is an instrument for isolating
something.** An island meant to read as one massif needs its marks to talk to each other across the whole
group; a knoll meant to sit alone on a plain is what a finite reach makes.

## What the slope axis makes of it

**One `layered` surface on the `slope` axis finishes all six panels — grass to 15°, coarse dirt to 40°, a
cell of stone and cobble beyond — and the paint is a reading of which panel is a plate.** `pinned` shows
grass plates with dirt ramps between them; `free-flanks` shows dirt across most of its flank because most of
its flank is a grade. `census.txt` reports four blocks under one theme.

**The board holds 19.5% of its ground at 40° or steeper**, which is the fell's own skirt and very little
else — `incline.txt` is the histogram, and `slopes.txt` counts 39,381 cells walked against 157 barrier over
the whole board.

## The recipe

**Pin the ground a player stands on, leave the flanks free, and keep `reach` at 0.** Then put the push where
its ring *and its falloff* clear every pin it must not lift:

```json
"relief": {"<group>": {"base": <the low ground>, "reach": 0, "step": 1,
  "marks":  [{"id": "holm",  "kind": "area", "h": 20, "bevel": 5, "ring": <where the dale floor is walked>},
             {"id": "shelf", "kind": "area", "h": 30, "bevel": 4, "ring": <where the objective stands>},
             {"id": "coast", "kind": "area", "h": 10, "bevel": 3, "ring": <the water's edge>}],
  "pushes": [{"id": "fell", "ring": <on the free flank>, "amount": 16, "falloff": 12, "crown": 9,
              "roughness": 0, "seed": 1}]}}
```

- **a push's extent is `radius + falloff`**, and anything inside that circle is lifted whatever states it.
- **two marks minimum**, or the solve has nothing to negotiate and returns a constant.
- **read `level` rather than `relief`** — `relief` cannot tell a range from a staircase, and `landform` called
  three plates a mountain.
- **`RL5` and a plate-flat board are the two ends of one dial.** Somewhere near half pinned is a board that
  is both walkable and worth looking at; the read gives the number, and the balance is the author's.

**A push on unmarked ground is the `pushes` card**, where the instrument is isolated and its four knobs are
each swept. This card is what happens once there is a board under it.

## What checks it

- `relief-read.json` — the six groups: `relief`, `landform`, `level` and the steps, the same push's two
  grades in four of them, and the two `RL5` complaints.
- `transects.txt` — row 1 west to east through the holm, row 2 north to south across the three heights, and
  the two lines under the fell that `reach` moves.
- `slopes.txt` — 39,381 cells walked, 4,238 scrambled, 157 barrier; nineteen faces, the largest 61 cells.
- `incline.txt` — how much ground stands in each ten degrees.
- `census.txt` — one theme, four surface blocks.
- `marks-and-pushes.layout.json` — the one document the board was stored from, posted to
  `POST /api/map/from-documents` with an empty intent and no plan.

Renders: `ordering-row.png` (dale, push on it, push beside it), `pinning-row.png` (pinned, free flanks,
reach) and `iso.png` (all six).
