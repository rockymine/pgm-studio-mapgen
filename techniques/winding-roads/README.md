# Winding roads

A line mark that comes back past itself is the instrument for a haul road, a switchback and a spiral ramp.
It has one failure and one fix, and the difference between them is a single field. The card holds six panels
in one world: the top row is one serpentine stamped three ways, and the bottom row is what three other
windings do. Open it in the studio as `technique-winding-roads`, or read `winding-roads.layout.json`.

Each panel is a flat island carrying one group and one relief. The only mark on five of them is the road
itself, so nothing else is shaping the ground.

## The road, and the band around it

`r` is the half-width of the band: a cell within it takes a pin. **`tread` is how much of that band is the
road** — flat, pinned at the line's height — and what is left between the tread and the reach is the
**shoulder**. `batter` is the angle the shoulder falls at.

**Left alone, a winding line builds vertical walls.** With no `tread` the whole band is road, so there is no
shoulder to grade and two passes meet on a step carrying the entire drop between them. Measured across the
three limbs:

```
r 14, no tread          32 ×22                      21 ×26                     10 ×23
r 14, tread 3           32 ×13  31 31 30 30 29 28   28 27 27 26 26 …  11 11 10 ×11
r 14, tread 3, b 78     32 ×12  30 25   21 ×26      19 14   10 ×30
```

The first is three terraces and two walls. The second is one continuous grade. The third is flat treads with
a steep face and a **bench at the toe**, because a batter steeper than the gap requires finishes its fall
early and holds at the lower tread's height.

The relief read says the same thing in one number — the walkability of the same geometry, three ways:

| panel | scramble | barrier |
|---|---:|---:|
| no tread | 136 | **194** |
| tread 3 | 0 | **0** |
| tread 3, batter 78 | 127 | **344** |

A tread turns 194 cells of wall into none. A batter puts more back, on purpose: a worked face is not meant
to be walked.

## The window a pitch has to sit in

**The loft runs only where the two bands meet**, which between parallel windings means the pitch is no more
than `2r`. Wider than that the passes never see each other and the gap is not stated at all — it is left to
the relaxation, which on bare ground is a smooth slope and on ground another mark has pinned is whatever that
mark put there.

**And the ramp needs run to grade in.** The gap it is drawn across is `pitch − 2·tread`, so a pitch under
twice the tread leaves nothing to grade.

**The `pitch-ladder` panel is the numeric case** and is read rather than looked at: limbs 22, 16, 11 and 7
apart at `r 8, tread 3`, which is a window of `6 < pitch ≤ 16`. Across all four gaps it reads

```
34 ×10  33 33 32 32 31 31 31 30 30 29 29 29 28 28  27 ×8  26 26 25 24 24 23 22 22 21
 20 ×8  19 18 18 17 16 15  15 ×7  9  8 ×9
```

— fourteen cells of relaxed slope at pitch 22, where the bands never met; nine and six cells of stated loft
at 16 and 11; and at pitch 7 a gap of one cell carrying the whole six-block drop, because `2·tread` has
eaten the run. The difference between the first gap and the rest is not the look but the authority: a loft
is stated outright, and relaxed ground is not.

**The grade across the gap is the fall per limb over that gap**, which is the number that decides whether a
road reads as road. At pitch 14 and tread 3 the gap is 8 cells, and a 30-block fall over three limbs puts a
56° face there — rock, not road. At pitch 26 the gap is 20 and the same fall grades at 24°.

**A spiral's pitch is `(r0 − r1) / turns`** and is fixed before anything is drawn. This card's spiral runs
radius 34 to 4 over four turns, a pitch of 7.5 against `r 6`.

## What a hairpin's apex does

**A second pass is one at least `2r` away measured along the line**, which is what tells a neighbouring
winding from the far side of a bend. At a hairpin the two limbs are joined by the turn itself, so until
`2r` of arc separates them they are one pass and **the apex does not grade**. The batter running down each
limb stops dead at the bend.

That is correct rather than broken — the far side of a tight corner is close in plan and close along the
line. It does mean a turn tighter than `2r` of arc is a flat pad.

## Finishing it by angle, which is most of why it reads

**A stepped road painted by depth is a grass staircase.** The surface stack follows the surface, so the top
courses of every column are soil whatever the ground is doing: a riser shows rock only below the stack's own
depth, and a riser shorter than that shows none at all.

**The fix is the `slope` axis**, where a band's thickness is a span of **degrees**. This card's ground states
three: grass to 15°, coarse dirt to 40°, and a cell of stone and cobble beyond. One stack finishes the flat
tread, the graded shoulder and the batter's face, and `census.txt` reports all four blocks on one theme.

**Where the bands cut is the decision, and 45° is the worst place to make it.** A gap lofted at one course a
cell stands at 45° exactly, so a rock band starting there paints every graded shoulder as cliff and the same
geometry reads either way. `incline.txt` answers what the board actually holds — 12.7% at 40° or steeper —
which is what the 40 was chosen against.

## Seating it in ground somebody else pinned

**Outside the tread the shoulder states its height softly**, at full weight against the tread's edge and
nothing at the reach's, so where the band crosses ground another mark has pinned the two grade into one
another instead of meeting on a step. The `seated` panel is the road crossing an upper fell and a lower holm,
each an `area` mark: 5 barrier cells over the whole panel.

**A cell between two windings is stated outright**, at full weight and with no softening. The ramp there is
the line's own business, and a mark drawn earlier may not reach up between two passes of a road.

## Two smaller things the panels carry

**Grain is off, and stays off.** It is noise laid over everything the marks decide, and on a road it reads as
damage rather than as weathering.

**The forms are turned 12° off the grid.** On the grid a riser lands as a straight band one cell wide; a few
degrees off it and every step is a stair of its own, which is what ground cut by a road actually looks like.

## What checks it

- `relief-read.json` — the walkability of all six panels, which is the table above.
- `transects.txt` — the three serpentine profiles, the pitch ladder's four gaps, the spiral across its pit,
  and the seated road.
- `incline.txt` — how much ground stands in each ten degrees, which is what the slope bands were cut against.
- `slopes.txt` — where the board steps, walked against scrambled against barrier.
- `census.txt` — one theme, four surface blocks, which is the slope stack painting all three bands.

Renders: `serpentine-row.png` (the three treatments), `forms-row.png` (spiral, pitch ladder, seated) and
`iso.png` (all six).
