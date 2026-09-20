# Marks and pushes

A relief is solved in two steps and the whole card is that fact: **the marks negotiate with each other and
are solved first; the push is added to the answer.** A mark is a constraint — this cell *is* this height —
and a push is an arithmetic lift applied afterwards to whatever the solve produced, which means a push cannot
see a mark, cannot be kept off one, and does not flatten what it raises. Open it in the studio as
`technique-marks-and-pushes`, or run `build.py`.

**Row 1 is one hillside and one push, the push in two places.** Row 2 is the other half of the same question
— how much of a panel to pin — with the same push on all three. The push is byte for byte identical in the
five panels that carry it, so the read returns the same skirt, 0.55, and the same 536 cells every time.

## The document

Six groups on the `ground` layer, each `mirrors: false`, on a board whose `setup.mirror_mode` is `none`.
Every panel is a 120×96 rectangle at `base_height` 60.

| panel | states | what it built |
|---|---|---|
| `dale` | `brae` 30 along the north edge, `strand` 14 along the south, `holm` 10 cut into the fall between | a hillside falling 30 → 14 with a hollow in it — `relief` 20, `level` 0.40 |
| `push-on-it` | the same, plus `fell` centred on the holm | a summit running 27 → 22 → 26 — `relief` **17**, `level` 0.36 |
| `push-beside-it` | the same, plus `fell` twenty-four cells west | the holm's floor reads 22, 12, 10 across eight cells — `relief` 25 |
| `pinned` | `coast` 10, `holm` 20, `shelf` 30 as bands tiling the panel, plus `fell` | three plates — `relief` 32, `level` **0.51** |
| `free-flanks` | the same three heights pinned only where a player stands, plus `fell` | ground that flows — `relief` 21, `level` **0.30** |
| `reach` | `free-flanks`' document with `reach: 16` | the north half sags eleven blocks — `relief` 24, `level` 0.33 |

**Two of the row-1 marks are long and face each other, and that is not decoration.** A field pinned only in
patches relaxes into fans radiating from each patch, which paint as a spray of contour streaks across
otherwise flat ground; a field pinned along two opposite edges relaxes into the ramp between them. Three
scattered pins and two facing bands were built side by side before this card was cut, and the bands are what
a hillside is made of.

**Neither band carries a `bevel`, because a bevel would have eaten them.** A bevel is paid for out of the
mark's own floor from every side at once, so a nine-cell band with a `bevel` of 4 pins nothing at all — and
`relief/read` does not call it silent, because the ring does cover cells. The panel simply comes out at
whatever else is speaking, which on the first cut of this card was the holm, and the whole hillside was flat
at 8.

```json
"push-beside-it": {"base": 18, "reach": 0, "step": 1,
  "marks":  [{"id": "brae",   "kind": "area", "h": 30, "bevel": 0, "ring": <the north edge, 9 deep>},
             {"id": "strand", "kind": "area", "h": 14, "bevel": 0, "ring": <the south edge, 9 deep>},
             {"id": "holm",   "kind": "area", "h": 10, "bevel": 5, "ring": <a lobed ring, radius 13>}],
  "pushes": [{"id": "fell", "ring": <a lobed ring, radius 13>, "amount": 12, "falloff": 22,
              "crown": 0, "roughness": 0, "seed": 1}]}
```

## A push is added to the solve, so it carries the ground rather than replacing it

**`push-on-it` puts the fell's ring exactly over the holm's, and the hollow does not fill in — it goes up.**
Along z −55 the dale under the ring reads 15 → 10 → 14 and the summit above it reads **27 → 22 → 26**: the
same shape plus twelve, block for block, because `crown` is 0 and the lift inside a ring is one number.

**Nothing in the document or the read says so.** The group reads `rolling`, one push, a skirt of 0.55 and no
finding at all — and its `relief` is **17** against the bare hillside's 20, because filling a hollow's
neighbourhood shortened the range. A landform was added and the read reported less relief.

**So a landform meant to have a flat top needs flat ground under it.** Pin what the push will stand on, or
accept the shape the solve left there; a `crown` cannot iron it out, because a crown adds most where the ring
is deepest, which is usually exactly where the hollow is.

## A push cannot be kept off a mark — only its ring and its falloff can

**`push-beside-it` moves the same push twenty-four cells west, clear of the holm's ring, and the holm still
comes up.** Along z −55 the mark states 10 and the ground reads **22 at x 136**, **12 at x 141** and its
stated **10 only at x 144**. The `dale` panel reads 10 at all three.

**The skirt is what did it, and the skirt is not a keep-out.** `falloff` 22 outside a radius-13 ring reaches
thirty-five cells from the push's centre, and every cell inside that circle gets its eased share added —
pinned or not. A mark is honoured in the solve and then has arithmetic done to it.

**There is no field that says otherwise, so the only control is distance.** Ring plus `falloff` is the push's
whole extent: keep that circle off the ground a mark has to deliver, or state the mark at the height you want
*after* the push has been added, which is guessing.

## How much of a board to pin, and the number that says when you are wrong

**`pinned` states every region as a mark and builds three plates.** Coast 10, holm 20, shelf 30, each a band
across the panel: north to south on a line clear of the fell, the ground holds 30 for thirty cells, ramps
eleven to 20, holds that for twenty, ramps eleven more to 10 and holds it to the edge. The only thing on the
panel that is not a plate or a ramp between two plates is the push.

**`free-flanks` pins the same three heights only where a player stands on them and leaves the rest to the
relaxation.** The coast becomes a nine-cell strip at the panel's edge, the holm a radius-17 ring, the shelf a
radius-11 one, and the ground between them falls continuously — 25 at the north to the holm's pinned 20 to
the coast's 10, with no plate anywhere but the holm.

**`relief` cannot tell those two apart, and reads the staircase as the bigger landform**: 32 on `pinned`
against 21 on `free-flanks`. `level` is the field that can — **0.51** against **0.30** — and it is the one to
steer by.

**0.30 is where the read starts complaining, so `free-flanks` is sitting on the line.** `RL5` fires under a
third level ground: *the elevation was graded everywhere and left nowhere to stand.* One more cell of grade
on that panel and it raises. Neither 0.51 nor 0.30 is the answer; a board is pinned where it is played and
free where it is looked at, and the read gives the number for the argument.

## `reach` decides whether unpinned ground is terrain or a sag

**`reach: 16` on the same document pulls every cell more than sixteen from a constraint back toward `base`.**
Down x 146, clear of the fell, the north half of the panel reads **11 rising to 13** where `free-flanks` at
the matching x 12 reads **25 falling to 20** — the shelf pinned at 30 no longer reaches that line at all, and
the field has settled a few blocks above its `base` of 6.

**Built, that is the difference between one landform and three.** The shelf and the fell stand as separate
mounds on low ground in the `reach` panel and are joined by flowing flank in `free-flanks`.

**`reach: 0` is therefore the default a board wants, and a finite reach is an instrument for isolating
something.** An island meant to read as one massif needs its marks to talk to each other across the whole
group; a knoll meant to sit alone on a plain is what a finite reach makes.

## Where the bands cut is read off the board, not remembered

**This card's ground is banded at 25° and 45° where the other cards band at 15° and 40°, because
`incline.txt` says so.** The board holds 38.2% of its ground under 10°, 29.3% between 10 and 19 and only
5.8% at 40° or steeper: a cut at 15 runs through the second-largest population and stripes every gentle flank
green-brown row by row, and a cut at 40 leaves the one landform on the board with no scree at all.

**The other cards' 15 and 40 are right for their boards for the same reason.** `pushes` and `winding-roads`
put their landforms on flat ground, so their cells are either level or on a skirt and hold 25.3% and 22.6% at
40° or steeper. One theme, four surface blocks, and `census.txt` reports them all under it.

**A push's skirt is gentler than its stated grade implies at the ends and steeper in the middle.** The
smoothstep a `falloff` eases with is half again as steep at its midpoint, so the read's 0.55 peaks at 0.82 —
39°, which is scree. A skirt the read calls 1.33 peaks at 2.0, which is 63°, and the slope stack paints the
whole landform as crag whatever it was meant to be.

## The recipe

**Pin the ground a player stands on, leave the flanks free, and keep `reach` at 0.** Then put the push where
its ring *and its falloff* clear every pin it must not lift:

```json
"relief": {"<group>": {"base": <the low ground>, "reach": 0, "step": 1,
  "marks":  [{"id": "holm",  "kind": "area", "h": 20, "bevel": 5, "ring": <where the dale floor is walked>},
             {"id": "shelf", "kind": "area", "h": 30, "bevel": 4, "ring": <where the objective stands>},
             {"id": "coast", "kind": "area", "h": 10, "bevel": 0, "ring": <the water's edge>}],
  "pushes": [{"id": "fell", "ring": <on the free flank>, "amount": 12, "falloff": 22, "crown": 0,
              "roughness": 0, "seed": 1}]}}
```

- **a push's extent is `radius + falloff`**, and anything inside that circle is lifted whatever states it.
- **two marks minimum, and long ones facing each other beat scattered small ones** — a field pinned in
  patches fans, a field pinned along two edges ramps.
- **a `bevel` wider than half a mark's narrow dimension pins nothing**, and nothing reports it.
- **read `level` rather than `relief`** — `relief` read the staircase as the bigger landform, and `RL5`'s
  threshold is 0.30.

**A push on unmarked ground is the `pushes` card**, where the instrument is isolated and its four knobs are
each swept. This card is what happens once there is a board under it.

## What checks it

- `relief-read.json` — the six groups: `relief`, `landform`, `level` and the steps, and the same push's
  skirt and cell count in five of them.
- `transects.txt` — row 1 west to east through the holm, the hillside north to south, and row 2's three
  profiles on lines clear of the fell.
- `slopes.txt` — 68,506 cells walked, 598 scrambled, 16 barrier; four faces, the largest 4 cells.
- `incline.txt` — how much ground stands in each ten degrees, which is what the band edges were cut against.
- `census.txt` — one theme, four surface blocks.
- `marks-and-pushes.layout.json` — the one document the board was stored from, posted to
  `POST /api/map/from-documents` with an empty intent and no plan.

Renders: `ordering-row.png` (dale, push on it, push beside it), `pinning-row.png` (pinned, free flanks,
reach) and `iso.png` (all six).
