# Opus 5.5 — two boards on the deployed studio, and the questions left on them as notes

## What I set out to build

**Two boards unlike each other, built on the deployed studio at pgmstudio.de, with every decision that is the
author's left on the board as a note rather than decided.** The run tests the notes loop end to end: the
author answers the notes, adds their own, and the next session works them.

The two sentences, written together before either plan:

- **`opus55-gypsum-reach`, dtm** — a pale desert lane where each team's obsidian monument stands in the open,
  with a dry wash in front of it (in from below), a mesa off its flank (in from above) and two stone houses
  behind it (in through).
- **`opus55-sootcombe`, ctw** — an ash-field combe from a composed plan: a brick hamlet on a terrace over each
  hub, falling to a flat frontline and a flat slag stone in the band.

**The tone families were checked across the pair.** Gypsum Reach is pale ground (sand), grey built (stone
brick) and a warm accent (granite and brick). Sootcombe is dark ground (grey and black stained clay), warm built
(brick) and the same granite accent.

## The notes left for the author

**Ten notes, five a board, each written with the token and so standing at `needs-info`.** Every picture note is
pinned by `render/eye/pick` on a picture uploaded to `POST /notes/pictures`, and each says what the board keeps
if the author does not mind.

| id | board | tag | pinned to | asks |
|---|---|---|---|---|
| 1 | gypsum-reach | gameplay | point (−46, 13, −10), view *Monument across the wash* | is the wash, rim 18 blocks from the monument, close enough to be the way in from below? |
| 2 | gypsum-reach | gameplay | point (−68, 26, −34), view *The mesa over the monument* | is the mesa, 12 over the shelf and 18 blocks off, too strong a perch? |
| 3 | gypsum-reach | gameplay | box of 985 columns on the north flank, view *The whole board* | should anything bring players to the 40% dead flanks? |
| 4 | gypsum-reach | terrain | the whole map | flat pan, or low dunes (level 0.58)? |
| 5 | gypsum-reach | look | point (−73, 29, −34), view *The mesa over the monument* | is the orange stained-clay bed too loud? |
| 6 | sootcombe | look | point (4, 8, 25), view *Mid stone over the band* | the ash reads as chocolate brown and the black as holes: light grey instead? |
| 7 | sootcombe | gameplay | point (5, 10, 7), view *Mid stone over the band* | should the mid stone rise, or stay flat and 12 blocks out? |
| 8 | sootcombe | gameplay | point (−18, 19, 79), view *West wool from the slag heap* | is the heap too good a perch over the west wool's approach? |
| 9 | sootcombe | terrain | point (−3, 10, 52), view *Hub from the terrace* | graded hub, or a retaining wall with flights? |
| 10 | sootcombe | look | point (29, 17, 72), view *The orange wool* | should wool rooms look different from the spawn? |

**Note 10 carries a correction as its second message.** The first described the style's materials wrongly
(dark oak and polished andesite, where they are brown stained clay and chiselled stone brick); the reply
corrects them and leaves the thread at `needs-info`.

**Five views are kept so they sit in the author's gallery**: two on Gypsum Reach (*Monument across the wash*,
*The mesa over the monument*) and three on Sootcombe (*West wool from the slag heap*, *Mid stone over the
band*, *Hub from the terrace*). The pictures the notes were written on are copied into each spec's
`renders/close/`.

## The deployed studio

**A whole drive took 48 seconds on the deployed studio**, from the evaluate to the last text read, for the
248 × 96 destroy board. No request was refused 429, so the driver never waited on a `Retry-After`.

**Nine drives in all, seven of Gypsum Reach and two of Sootcombe**, two of them refused at the store, plus the reads and pictures the notes
needed. Two composed plans were pinned: seed 21 is the one used. Pinning writes a plan row, idempotent by
content hash, and that row is left on the studio.

**One studio fault, with its coordinates.** `DestroyablePlacement.at` is documented in `openapi.json` as *an
[x, z] offset in half-blocks*, and the evaluator reads it in blocks. Posting `[88, 72]` for a monument meant to
stand at (−60, −16) on a field whose corner is (−104, −48) put it 44 blocks further on, at the frontline edge,
refused `OB17` as overhanging the void. `[38, 32]` put it at (−66, −16) as meant.

## What I got wrong

**The strata were wrong twice before they were right.** A height stack with `from: 4` and `follow` sat
entirely above the ground and the fill came out stone; `ending: repeat` then gave one orange bed forty blocks
deep, because the last band claims everything past the stack. The cycle is now written out bed by bed from 40
below the ground, which is what `techniques/made.py` says and I had not read closely.

**I stated a house style as `"@hw-stonehouse"` in `dressing.styles`**, which the store refused `DR-DOC` at 400.
A style there is `{"kind": "house", "shell": <HouseStyle>}`; `tools/README.md` says so.

**I opened another board's spec to learn the `follow` syntax**, three lines of `whitstone-weald`'s build script.
The brief keeps specs out of an authoring run; the field was in `GET /api/terrain/patterns` and the working
`from` value was the one thing it did not say.

**Sootcombe's first drive was refused `PT3` and twice `PT4`**: a cell of size one, and a wall and fill with no
`rise`. Each refusal named its JSON path.

## What worked first time

- The plan tier's `GO1` arithmetic from `ORDER-OF-WORK.md` §1: the monument at `L/4` from its spawn gave a ratio
  of 3.36 on the second placement, after the `at` unit was found.
- The composed plan, taken whole, drove clean: preflight OPEN, 0.0% dead, both walls three courses over the
  ground they stand on.
- `render/eye/pick` answered the same block for a pixel on every call, and every note posted on the first try.

## What I could not say

**Nothing was missing from the system in this run.** Every capability reached for was found by its field in
`openapi.json`, and the one discrepancy found is the `at` unit above: the mechanism exists and is documented in
the wrong unit.

## Open gameplay questions

**None were decided alone.** Every gameplay question this run met is one of notes 1–3 and 7–9, built with the
default each note names, and waiting on the author.
