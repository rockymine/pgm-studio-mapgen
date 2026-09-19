# Marks and seams

**Two marks never negotiate.** Each pins its own cells to its own height, and what happens between them is
decided entirely by how much ground neither one claimed. Twelve panels: one pair of pads meeting four ways,
the mark that states a step on purpose beside three that state nothing anybody can see, and what a mark's
shape and its fall-back do to the field. Open it in the studio as `technique-marks-and-seams`, or run
`build.py`. The high ground is north in every panel, because the camera looks from the south-east and
ground that rises toward it hides its own face.

**A ring covers the cells whose centres fall inside it, so a boundary coordinate is a statement.** Two bands
stated to share one leave no cell between them; two stated one apart leave exactly one, and the relaxation
has to answer for it. That one cell is the difference between row 1's first two panels.

**`POST /sketch/relief/read` is the only thing that reports any of this, and it is not enough.** Its
`seams` names every pair of marks whose ground meets on more than a one-block step, worst first, with a
coordinate; its `silentMarks` names the marks that pinned nothing. It catches three of this board's five
faults and is blind to the other two.

## The document

Twelve groups on the `ground` layer, one theme, and one relief each — a `base` of 8 and between one and
three marks. Row 1's four panels state the *same* two pads at the *same* two heights.

| panel | what it states | what it solved to |
|---|---|---|
| `butted` | two pads sharing their boundary | **one 12-block wall**, and `seams` names it |
| `one-apart` | the same, one cell apart | **two steps of 6** — and `seams` is **empty** |
| `gapped` | the same, ten cells apart | a block a cell: a walkable grade |
| `bevelled` | butted, `bevel: 6` on the upper pad | the grade inside the pad: two a cell over seven |
| `a-scarp` | one `scarp`: `high` 20, `low` 8, `face` 2 | three steps of 4, authored, and no seam |
| `bevel-too-wide` | a nine-cell band at `bevel: 5` | nothing: the panel is the other mark's 8 |
| `off-the-land` | the butted pair, plus a ring off the footprint | the same wall; the third mark is **silent** |
| `half-off` | a ridge traced 26 blocks past the coast | the strip pinned at 26, the crest off the map, **nothing reported** |
| `one-height` | one ring at 30, `reach: 0` | the whole panel at 30 — `relief` 0 |
| `a-summit` | a `point` at 30, `r: 6`, `reach: 24` | a cone, y11 to y30 |
| `a-plateau` | a ring of radius 20 at 30, `reach: 24` | a flat top and a skirt, y17 to y30 |
| `facing` | two bands at 30 and 8, `reach: 0` | the ramp between them, y8 to y30 |

```json
{"base": 8, "reach": 0, "step": 1, "pushes": [], "marks": [
  {"id": "low",  "kind": "area", "h": 8,  "bevel": 0, "ring": ["…the north band…"]},
  {"id": "high", "kind": "area", "h": 20, "bevel": 6, "ring": ["…the south band…"]}]}
```

## One pair of pads, four meetings

**Butted, two pads build two terraces and a wall.** `butted`'s transect reads twenty for ten cells, then
**−12**, then eight: a sheer twelve-block face right across the panel. `relief/read` names it exactly —
`{"a": "high-butted", "b": "low-butted", "step": 12, "x": -209, "z": -91, "cells": 88}` — a pair, a step, a
coordinate to stand at, and how far the boundary runs.

**One cell of unpinned ground between them halves the wall and hides it from the read.** `one-apart` reads
twenty, then **14**, then eight — two six-block steps, because the relaxation has one free cell to answer
for and puts it midway. Its `seams` is
**empty**: a seam is measured between a cell one mark last claimed and a neighbour the other did, and there
is no longer any such pair. The ground is still a barrier and nothing says so.

**Ten cells of it is a grade, and that is where the design happens.** `gapped` falls a block a cell — 19,
18, 17, 16, 15, 13, 12, 11, 10, 9, 8 — which is ground a player walks down. The two pads are identical in all three panels; the gap is the whole
instrument.

**A `bevel` buys the same grade out of the mark's own floor.** `bevelled` is butted again with `bevel: 6` on
the upper pad, and the fall happens inside that pad's footprint: 20, 18, 17, 15, 13, 11, 10, 8. Six cells
against a twelve-block rise is two blocks a cell, so **a bevel wants to be at least the rise it is
absorbing** for one-block steps — and it is paid for out of the pad's flat top, from every side at once.

**So the choice is where the grade is allowed to live.** Outside both marks, it is a gap; inside the upper
one, it is a bevel; and a floor that must stay flat to its own edge gets neither and meets its neighbour on
a face. `row1-sections.png` is the four of them cut through the same place.

## The step you meant

**A `scarp` is one mark that states both sides and the face between them, so the step is authored rather
than left over.** `a-scarp` states `high: 20`, `low: 8`, `face: 2`, `band: 14` and builds **three steps of four**
where the butted pads built one of twelve — the drop spread across the width the face asks for.

**And its `seams` is empty, which is correct and worth knowing.** A seam is a fault between *two* marks; one
mark that states a step has no pair to be reported against. The read is quiet because there is nothing
wrong, not because nothing is there.

## Three marks that said nothing

**A bevel wider than half a mark's narrow dimension eats its own floor, and the mark pins nothing.** A bevel
is paid for from every side at once, so `bevel-too-wide`'s nine-cell band at `bevel: 5` has no flat left:
the panel comes out at 8 — the low pad's height — with `relief` **0**. `relief/read` does list it under
`silentMarks`, so this one is caught.

**A ring drawn wholly off the footprint is silent too, and that is what the reading is for.**
`off-the-land` carries the butted pair plus a ring forty blocks north of the island. The pair's wall is
reported as before and the third mark comes back as `silentMarks: ["elsewhere-off-the-land"]`.

**A mark that runs out through the coast is the one nothing catches.** A mark is *clipped* to the footprint
rather than confined to it, so `half-off`'s ridge — traced 26 blocks past the south edge with a radius of
14 — pins the strip it does cross at its own heights and leaves its crest outside the board. The panel's
edge stands at **y26** instead of decaying to `base`, there is no seam and no silent mark, and the only
thing that shows it is the profile.

## What a mark falls to

**A group whose marks all state one height comes out at that height everywhere.** `one-height` states a
twenty-radius ring at 30 with `reach: 0`, and the whole panel is 30: `low` 30, `high` 30, **`relief` 0**. A
landform is a fall, and a fall needs something to fall to.

**`reach` is that something: how far a mark's influence travels before the field returns to `base`.**
`a-summit` and `a-plateau` state the same height, the same base and `reach: 24`, and differ only in the
shape of the mark — and that is the difference between a summit and a mesa.

**A point mark makes a cone.** `a-summit` is a `point` at 30 with `r: 6`: its profile climbs from 14 at the
panel's edge to 30 over twenty-eight cells, holds its apex for the **twelve** an `r: 6` disc pins, and falls
the same way back. The read calls it `rolling`, y11 to y30.

**The same height over a wide ring makes a mesa, and the radius is the whole difference.** `a-plateau` is a
twenty-radius ring: a flat top **forty** cells across with a fourteen-cell skirt off each side, y17 to y30.
Nothing about the statement changed but the size of the patch it covers.

**Two marks at two heights need no `reach` at all, and two long ones facing each other are what a hillside
is made of.** `facing` states a band at 30 along the north edge and one at 8 along the south, and the panel
between them is a single even ramp, 30 down to 8 over forty cells — a block every two.

## The recipe

**Decide where the grade lives before stating either mark.**

```json
{"base": 8, "reach": 0, "marks": [
  {"id": "shelf", "kind": "area", "h": 8,  "ring": ["…"]},
  {"id": "fell",  "kind": "area", "h": 20, "ring": ["…, stated a gap away…"]}]}
```

- **ground wants a gap between its marks** — the ramp is what the gap is for, and ten cells buys twelve
  blocks at one a cell.
- **a floor wants a `bevel`, at least as wide as the rise** it has to absorb, and it pays for it out of its
  own flat.
- **a step you meant is a `scarp`**, not two pads butted; `face` is how wide the drop runs.
- **bands that must touch share their boundary coordinate.** One apart is a cell nobody claimed, and it
  halves the wall instead of removing it — invisibly.
- **give the field something to fall to**: a second mark at another height, or a finite `reach`.
- **read `seams` and `silentMarks` after every relief change** — then read the heightmap, because a mark
  hanging off the coast is in neither list.

## What checks it

- `relief-read.json` — twelve readings. One seam on `butted` and one on `off-the-land` with their
  coordinates; `silentMarks` on `bevel-too-wide` and `off-the-land`; and `relief` 0 on `bevel-too-wide` and
  on `one-height`, for two different reasons.
- `transects.txt` — eleven profiles, the first four cell by cell through the same place in four panels.
- `incline.txt` — 75.3% of this board's ground under 10° and 3.5% at 40° or steeper, which is what a board
  of pads and ramps is; the slope bands cut at 35° and 55°.
- `slopes.txt` — what the four meetings cost the walk.
- `census.txt` — one theme, so nothing in the pictures is the paint.
- `marks-and-seams.layout.json` — the one document the board was stored from. It stores and builds with no
  finding at all. Five of the twelve carry a fault an author would want told; the reading catches three of
  them and is blind to `one-apart` and to `half-off`.

Renders: `row1-sections.png`, `row2-sections.png` and `row3-sections.png` — the profiles cut through each
panel, which is the only view a step in the ground reads in; `row1-seams.png` and `iso.png` for the board.
