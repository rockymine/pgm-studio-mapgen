# Pushes

A push is the one instrument that builds a landform. It takes a drawn ring, lifts the solved surface inside
it by `amount`, and grades that lift back to the ground over `falloff` cells outside it — so unlike a mark,
which pins cells and leaves the relaxation to invent everything between them, a push states a hill and the
hill has sides. The card is eight panels: four outlines of one push, and four arrangements of several. Open
it in the studio as `technique-pushes`, or run `build.py`.

**A push has four knobs and the landform is all four of them.** `amount` is the lift inside the ring,
`falloff` the width of the skirt outside it, `crown` a second lift climbing from the outline to the shape's
own middle, and `amounts` one lift per position round the ring in place of the single one.

## The document

Eight groups on the `ground` layer, each `mirrors: false`, on a board whose `setup.mirror_mode` is `none`.
Each panel is a 96×76 rectangle at `base_height` 52, and every relief states `base: 8`, `reach: 0` and no
marks at all — so the ground each push rises out of is a plain at 8 and nothing but the push is speaking.

| panel | what it states | what it built |
|---|---|---|
| `plateau` | `mesa`: a lobed ring, radius ≈19, `amount` 22, `falloff` 14, `crown` 0 | a flat top at 30, skirt 8→30 across twelve cells |
| `dome` | `fell`: a round ring, radius 20, `amount` 16, `falloff` 14, `crown` 14 | outline at 24, cap at 38 |
| `ridge` | `edge`: a 68×12 ring, `amount` 16, `falloff` 12, `crown` 6 | outline at 24, crest at 30 — along a line |
| `amounts` | `spur`: a 56×26 ellipse of 40 positions, lifts 6…26, `falloff` 14 | 14 at the west end, 34 at the east |
| `stack` | `massif` +10 f13, `bench` +8 f9, `tor` +6 f5 crown 4, concentric | three terraces at 18, 26 and 36 |
| `overlap` | `west` and `east`: radius-16 rings twenty apart, `amount` 14, `falloff` 12 | 22 under each alone, **36** where they cross |
| `crater` | `cone` radius 22 +20 f14, then `caldera` radius 11 **−14** f5 | rim at 28, floor at 14 |
| `disagree` | `stack-of-two`: radius 19, `amount` 24, `falloff` **8**, `crown` 8 | outline at 32 in eight cells, cap at 40 over seventeen |

```json
"stack": {"base": 8, "reach": 0, "step": 1, "marks": [],
  "pushes": [{"id": "massif", "ring": <54x54, turned 12>, "amount": 10, "falloff": 13, "crown": 0,
              "roughness": 0, "seed": 1},
             {"id": "bench",  "ring": <36x26, turned 12>, "amount":  8, "falloff":  9, "crown": 0, "…": …},
             {"id": "tor",    "ring": <18x12, turned 12>, "amount":  6, "falloff":  5, "crown": 4, "…": …}]}
```

## The ring is the flat part and `falloff` is everything else

**Inside the ring every cell gets the full `amount`, and the grade lives wholly outside it.** The `plateau`
panel is 8 across the plain, 30 over fifty-odd cells of top, and the whole transition happens in the twelve
cells between — `falloff` 14 eased by a smoothstep, which flattens at both ends so the skirt leaves the plain
level and meets its own outline without a crease.

**So the shape of the ring is the shape of the flat part, and nothing else in the document says it.** The
`plateau` ring is a five-lobed outline and the mesa it builds reads as ground; the `stack` panel's rings are
four-vertex rectangles and its terraces read as rectangles, which is the same fact used on purpose.

**`amount / falloff` is the skirt's grade in blocks a cell, and it is the number to choose the pair by.**
`relief-read.json` reports it per push: 0.77 on the `stack`'s outer ring, 1.57 on the `plateau`, 3.00 on
`disagree`. Below about 1.0 the skirt is walkable, at 1.5 it scrambles, and at 3.0 it is a face.

## `crown` climbs to the ring's medial axis, which is a point or a line

**`crown` is a second lift, added on top of `amount`, that is zero at the outline and full at the set of
points furthest inside the ring.** The `dome` panel states 16 and 14: the ring's edge builds at 24 and the
middle at 38, the two numbers added exactly. Between them the crown's own smoothstep makes a shoulder at the
outline and a cap at the top, which is what a hill looks like and what a plateau does not.

**On a long ring that furthest set is a line, so the same `crown` builds a crest instead of a peak.** The
`ridge` panel is a 68×12 ring at `crown` 6: cut across, the ground climbs 8 → 30 in sixteen cells and falls
again in seventeen; cut along, it walks the whole ninety without ever stepping more than two. Nothing in the
document chose a ridge — the outline did.

**The crown's own grade is `crown / deepest`, where `deepest` is half the ring's narrow width.** The `dome`
reads 0.71 (14 over 20) and the `ridge` 0.94 (6 over ~6). A crown on a wide ring is gentle however large the
number, and a crown on a narrow one is steep however small.

## `amounts` is read at the nearest ring point, so it cuts the interior into wedges

**One lift per position round the ring replaces `amount` everywhere, and each interior cell takes the lift of
the ring point nearest it.** That partition is the ring's medial axis, so a ring of few positions builds that
many wedges with a step down every seam between them. A 40×40 square carrying `[26, 26, 6, 6]` builds two
wedges at 34 and two at 14 with a **20-block cliff along both diagonals**, measured two cells wide.

**Two things remove the seam, and a spur wants both.** Enough positions that neighbours differ by little —
the `amounts` panel states forty — and a form long enough that the two sides facing each other across the
middle carry the same lift, which is why the lifts here are a function of position *along* the ellipse rather
than of angle round it. The panel falls 34 → 14 end to end with no barrier step anywhere on the line.

**The positions are spaced by arc, not attached to the drawn vertices.** `AmountAt` reads index `i` at
fraction `i / count` of the perimeter, so the two coincide only on a ring whose sides are all the same
length. On any other outline a lift written for a corner lands somewhere along an edge.

## Pushes add, which is what makes a massif

**Every push in a group is summed into one lift field, so a smaller ring inside a larger one is a terrace on
it rather than a replacement for it.** The `stack` panel states three concentric rings at +10, +8 and +6 with
a crown of 4 on the innermost, and builds terraces at 18, 26 and 36 — each the running total, each with its
own skirt grading down to the one below.

**Two rings that cross give the sum in the crossing, not the larger of the two.** The `overlap` panel is two
radius-16 rings twenty apart at `amount` 14 each: 22 under either alone, 36 where both contain the cell.

**The skirts add as well, so the steep ground on that panel is ground neither push states.** The read counts
112 barrier steps in the group and `slopes.txt` puts the cells at x −62…−49, z 22…28 and again z 60…67 —
north and south of the waist between the two rings, not one of them inside either ring. Two grades of 1.17
meeting there make 2.34.

**A negative push inside a positive one cuts the hill after it is raised, and the order they are written in
changes nothing.** The `crater` panel states +20 over a radius-22 ring and −14 over a radius-11 ring inside
it: rim 28, floor 14, and the floor stands six blocks above the plain the cone rose from. A sum has no
sequence — what makes the caldera a hollow is that its ring lies inside the cone's, not that it comes second.

## The one arrangement the read refuses to like

**`RL6` fires when a push's two grades are more than twice apart, because the ground then steps at the push's
own outline.** The `disagree` panel states `amount` 24 over `falloff` 8 — a skirt of 3.0 — against `crown` 8
over a radius of 19, a crown of 0.44: 6.9× apart, and the read names it.

**Built, it is a cliff with a hill on top.** The transect climbs 8 → 32 in eight cells and then 32 → 40 over
the next seventeen, and the break is exactly at the ring. `RL2` fires beside it: 776 of the group's steps are
taller than a player can scramble, against 296 on the `plateau` and none at all on the `stack`, the `dome` or
the `ridge`.

**The fix is the ratio rather than either number.** Widen the `falloff` until the skirt comes down to the
crown, or lower the `crown` until it comes up to the skirt; a push with no crown states one rate and is not
read here at all.

## What the slope axis makes of them

**The ground is finished by its angle, so every push paints its own skirt without the theme knowing a push
exists.** One `layered` surface on the `slope` axis — grass to 15°, coarse dirt to 40°, a cell of stone and
cobble beyond — puts turf on every flat top, scree on the `stack`'s terraced flanks, and rock on the
`plateau`'s and `disagree`'s banks. `census.txt` reports all four blocks under one theme.

**The board holds 25.3% of its ground at 40° or steeper, and that is the number the bands were cut against.**
`incline.txt` is the histogram. A push at a skirt of 0.77 never reaches the rock band and one at 3.0 is
nothing but rock, which means the paint is a reading of the knobs: a board where every landform is grey is a
board whose `falloff`s are all too small.

## The recipe

**A hill is a lobed ring, a crown about two-thirds of the amount, and a falloff wide enough to keep the two
grades within twice each other.** On a plain at 8:

```json
"relief": {"<group>": {"base": 8, "reach": 0, "step": 1, "marks": [],
  "pushes": [{"id": "fell", "ring": <a lobed ring, radius r>,
              "amount": 16, "falloff": 14, "crown": 14, "roughness": 0, "seed": 1}]}}
```

- **`crown: 0` is a mesa and a crown is a hill** — the field's default is 0, so a push authored without
  touching it has a flat top.
- **keep `amount / falloff` and `crown / r` within twice each other**, or `RL6` says the landform steps at
  its own edge.
- **a ring of four vertices builds a square**, whatever else is right about the numbers.
- **`roughness` stays 0.** It wobbles the skirt's distance against a noise field, which on a landform meant
  to be read as ground looks like damage rather than weathering.

**Make a massif out of several pushes rather than one.** Concentric rings each add their own lift and their
own skirt, so three rings are three terraces and the author picks each step; one ring with a big crown is a
single cone whose only shape is its outline.

**Cut hollows into raised ground with a negative push inside the positive one, and into flat ground on its
own** — that second case, its depth, its wall and what a floor costs, is the `hollows` card.

**Every panel here states its push against an unmarked field at `reach: 0`, which is not how a board uses
one.** Of the 216 pushes in this repository's `specs/`, 137 have a mark's ring under them and only 38 of the
79 groups carrying a push state `reach: 0`; the knobs are legible here because the ground under them says
nothing. What a push does to ground a mark has already pinned is the `marks-and-pushes` card.

## What checks it

- `relief-read.json` — every push's two grades and cell count, per group, and the two complaints on
  `disagree`. Nothing else on the board raises anything.
- `transects.txt` — one line through each panel, plus the one across the ridge, with the steps named.
- `slopes.txt` — 48,228 cells walked, 8,014 scrambled, 2,126 barrier; twenty faces, the largest 864 cells on
  the `disagree` panel.
- `incline.txt` — how much ground stands in each ten degrees, which is what the slope bands were cut against.
- `census.txt` — one theme, four surface blocks, which is the slope stack painting flat, graded and face.
- `pushes.layout.json` — the one document the board was stored from, posted to `POST /api/map/from-documents`
  with an empty intent and no plan. A terrain card needs neither a spawn nor an objective: the renders read
  the stored layout through `POST /sketch/columns`.

Renders: `shapes-row.png` (the four outlines), `combining-row.png` (stack, overlap, crater, disagree) and
`iso.png` (all eight).
