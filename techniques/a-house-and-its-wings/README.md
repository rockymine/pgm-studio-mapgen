# A house and its wings

**A house is a prop stating a list of touching rectangles, and nothing in it is named by an author.** Which
rectangle is the hall and which is the cross wing follows from the ridges and the edge they share: the
hall's ridge runs *along* that edge and the wing's runs *into* it. Twelve pads carry twelve plans under one
style — `bothy`, taken whole from `specs/opus5-glassmere` — and eleven of them are buildings. Open it in
the studio as `technique-a-house-and-its-wings`, or run `build.py`.

**The five bare pads are the point rather than a gap.** A plan the joint rules refuse is declined, not
built: nothing stands where a finding points, and the yard is left showing so the panel can be told from one
that was never drawn on.

**Row 1 is one hall and one cross wing at the same height, met three ways.** The corpus already has the
different-height case — `opus5-glassmere`'s bothy and `opus5-burgage-terrace`'s `plot-c` both hang a
`storeysHigh: 1` wing off a taller range — and what it does not have is the pair that differ in one boolean.

## The document

Sixteen groups, one gravel yard per panel so a footprint reads against the grass, and sixteen `house` props
under one style. A wing is two opposite corners and a `spec`.

```json
{"id": "projecting", "kind": "house", "layer": "ground", "seed": 5, "front": "negZ", "style": "bothy",
 "wings": [{"corners": [[32, -76], [43, -69]], "spec": {"ridge": "alongX"}},
           {"corners": [[36, -68], [41, -61]], "spec": {"ridge": "alongZ", "projects": true}}]}
```

| panel | the plan | what it built |
|---|---|---|
| `one-range` | one rectangle | a plain range: 140 blocks |
| `marching` | hall + cross wing, same height | the wing's roof stops at the seam |
| `projecting` | the same, `projects: true` | the wing's roof crosses the hall and gables on its far wall |
| `lower-wing` | the same, `storeysHigh: 1` | the wing tucked under, which is the corpus's case |
| `a-t-plan` | a hall with a wing either side | one building, 252 blocks |
| `side-by-side` | both ridges along the shared edge | **`HJ3`** — two ranges meeting in a gutter |
| `end-to-end` | both ridges into it | **`HJ4`** — one longer range, drawn as two |
| `wing-overtops` | a wing 14 along an 8-deep hall | **`HJ5`** — its roof stands taller than the one it meets |
| `overlapping` | the rectangles share three rows | **`HJ1`** — a plan states its ground once |
| `partial-edge` | they touch over 3 blocks of edge | **`HJ2`** — half the wing's end is over open ground |
| `apart` | four blocks between them | built: two buildings under one prop |
| `a-u-plan` | a hall with two wings off one edge | one building, 252 blocks |
| `flat-hall` | hall `form: "flat"`, lower gable wing | a flat lid at y18; the wing's ridge at y17 runs into a **wall** |
| `flat-wing` | gable hall, wing `form: "flat"` | a flat lid on the wing at y13, one storey down |
| `shed-wing` | gable hall, wing `form: "shed"` | a lean-to: one plane climbing to the hall |
| `shallow-wing` | gable hall, wing `pitch: 1` | the same gable, its ridge at y15 instead of y17 |

## Marching and projecting

**Marching and projecting are the two things a wing can do where it runs into a hall, and only the first
stops at the seam.** A marching wing's roof steps into the hall's and ends there. A projecting wing carries
its roof across the hall to the hall's **far** wall and shows a second gable standing on it.

**The two panels state the same hall and the same wing, and differ in one boolean.** At the hall's far wall
on the wing's axis, `marching` reads dark oak planks at **y18** over stone bricks — the hall's own roof over
its own wall — and `projecting` reads a spruce verge at **y22** over planks at y20: four courses higher, and
the gable is the wing's.

**A projection lengthens the roof without raising it.** Over the middle of the hall both panels read the
identical ridge, spruce log at y23 and y24. The extension is the roof's *plan* alone, taken along the wing's
own ridge — the axis a gable's rise is not measured over — so nothing about the hall's height changes.

**And the walls stay where the author drew them.** The hall's far wall is still the hall's; the gable simply
stands on it. One cell past that wall `marching` has the hall's own eave at y16 and `projecting` has the
projecting gable's verge at y21 and y22, overhanging.

**A wing at a lower storey count is the other way to vary the pair, and it is not the same thing.**
`lower-wing` states `storeysHigh: 1` and marches: the roof is a separate, lower volume laid beside the
hall's rather than an extension of it. A building's roof is the union of its wings' roofs and never a max of
their crowns, which is what keeps a low wing's slope from dragging material down the tall wing's wall.

## Two roofs on one building

**A wing states its own roof, not only its own height.** `WingSpec` carries a `form`, a `pitch` and a
`roofSlab` beside its `storeysHigh` and its `ridge`, and a building's roof is the union of its wings' roofs
— so one plan can wear two forms without being two houses.

**A flat-topped range is the case a gable hall cannot give: the wing meets a wall.** `flat-hall`'s hall is
`form: "flat"` and its lid is dark oak at **y18**; the lower gable wing's ridge stands at **y17**, under it.
Nothing of the wing's roof runs into anything — it stops against masonry, which is what a lean-to against a
warehouse looks like.

**The other way round, the wing is the one that changes.** `flat-wing` puts a flat lid at y13 on a wing one
storey down, `shed-wing` gives it a single climbing plane, and `shallow-wing` keeps the gable but states
`pitch: 1`, which drops the same wing's ridge from y17 to **y15**. All four are the same hall.

**The five forms are `gable`, `flat`, `hip`, `gambrel`, `shed` and `saltbox`**, and `flat` is the only one
that can carry a hole — which is why a wool room and a spawn have always worn it.

## What the ridges decide

**Nothing tells the studio which rectangle is the hall; the ridges do.** The hall's ridge runs along the
shared edge and the wing's runs into it, and that is the only reading that makes one a range and the other a
cross wing.

**Both along it is two ranges side by side** — `HJ3`, *"meeting in a gutter no roof form covers"*. Turn one
wing a quarter, or draw the two as one rectangle.

**Both into it is one longer range** — `HJ4`, *"and stating them separately asks for a seam through the
middle of a roof"*. Draw it as one rectangle.

**And a wing reaching further along the shared edge than its hall reaches across it overtops the roof it
meets** — `HJ5`. `wing-overtops` puts a 14-long wing against an 8-deep hall: a roof's height comes from its
span, so the wing's roof stands taller than the hall's and runs out the far side instead of into it.

## The three ways two rectangles are not one plan

**Wings touch and never overlap.** `overlapping` slides the wing three rows into the hall and draws `HJ1`:
*"a plan states its ground once, and two wings claiming the same cells have no single answer for what stands
there"*.

**And the touching has to be whole.** `partial-edge` offsets the wing so that three of its eight end blocks
are over the hall and the rest hangs over open ground — `HJ2`, and neither joint can happen along it.

**Two rectangles four blocks apart are simply two buildings, and the studio builds them.** `apart` is not
refused: it comes back as 220 blocks under one prop id, two ranges standing near each other. A gap is a
plan an author meant or a mistake nothing will catch.

## What else a plan has to fit inside

**`HP3` caps a placed building at 192 blocks of footprint**, and it is the first thing a plan of several
rectangles runs into: a 14 × 10 hall with an 8 × 10 cross wing is 220 and makes no building. Every plan on
this board is drawn inside the cap — a 12 × 8 hall of 96 leaves room for one cross wing of 48 or two of 40.

## The recipe

```json
{"kind": "house", "style": "<one style for the whole building>", "front": "negZ",
 "wings": [{"corners": [["…the hall…"]], "spec": {"ridge": "alongX"}},
           {"corners": [["…the cross wing…"]], "spec": {"ridge": "alongZ", "projects": false}}]}
```

- **the hall's ridge runs along the shared edge and the wing's into it** — anything else is `HJ3` or `HJ4`.
- **share the whole of the shorter edge**, and never a block more: `HJ1` and `HJ2` are the two halves of
  that one rule.
- **keep the wing no longer along the edge than the hall is deep across it**, or `HJ5`.
- **`projects: true` for a cross gable on the hall's far wall**, and leave it out for a wing that stops at
  the seam. It lengthens the roof and never raises it.
- **a lower wing is `storeysHigh`, not a second house** — one style, one prop, one roof union.
- **192 blocks, total**, before anything else is judged.
- **a wing may state its own `form` and `pitch`** — a flat range with a gable wing against its wall, or a
  gable range with a flat, shed or shallower wing, are all one building.

## What checks it

- `dressing.json` — eleven buildings and five declines, each naming its own `HJ` rule and its own subject.
- `columns.txt` — twelve columns: the hall's ridge, its far wall and one cell past that wall, in the
  marching panel and the projecting one; and the four roofs of row 4 against the standard wing's ridge.
- `census.txt` — two themes, because everything in the pictures above the gravel is a prop rather than
  terrain.
- `a-house-and-its-wings.layout.json` — the sixteen plans, and `bothy.style.json` beside it, which is the
  style copied whole out of `specs/opus5-glassmere`.
- `incline.txt` · `slopes.txt` — flat pads, so nothing in the roofs is the ground's doing.

Renders: `joint.png` — marching and projecting side by side at the same scale; `row1-joint.png`,
`row2-ridges.png`, `row3-joints.png` and `row4-roofs.png` for the four rows; `iso.png` for all sixteen.
