# Opus 5.5 — four destroy landscapes, relief only

## What I set out to build

Four destroy boards, their ground and nothing else: no theme, no dressing, no buildings beyond the spawn
shell. The method was the author's. Take a simple plan at one height, reshape its outline, then state the
ground in layers of relief until each board reads as a different kind of place. A destroy board offers more
room than a capture board, so each one carries a landform the capture boards could not hold at their width.

| Board | The one sentence |
|---|---|
| Kelderfell | a fellside falling to the strait, broken by a curved scarp with a pass in it |
| Twingill | a dale between two ridges, with its gill falling from the spawn's head to the strait |
| Scarbutte | a tableland whose rim breaks onto a rolling bench of buttes, split by a canyon |
| Cinderhowe | a caldera on the board's axis, breached twice, with the monument in its floor |

The boards were built twice. The second pass follows the author's review, and its own section below says
what changed and why.

## The method, the same on all four

**The plan is a spawn and one field at y20, with a 32-block build zone between the teams.** The plan uses
`rot_180` with team 0 on x < 0, one pillar-3 obsidian monument a team, and 16 players. The compile fuses the
two pieces into one shape, `field-20`.

**The outline is reshaped point by point, never restated.** Each `build-spec.py` states the vertex moves and
inserts as `editShapes`. The moves run first; the inserts then run edge by edge from the last edge back, so
every index an op names is still correct when it runs. A bend with `side: out` then rounds the result. The
strait edge is left straight, following the author's ruling that a lip is never pulled in.

**The relief is stated in layers, each with its own job.** Each board's layers are, in this order:

1. a **frame of small marks** that pins only what must be level or at a height: the spawn's footing, the
   monument's shelf, and a lip line that wanders in course and height;
2. the **board's one big landform**: a scarp, a dale floor, a tableland or a crater;
3. **large pushes** for the mass: a fell, ridges, cones, swells;
4. **carving and detail**: negative pushes for hollows, coombes, a gill or a canyon, and small knolls or
   buttes.

No board carries grain. The third pass removed it, and its section says why.

## The second pass, after the author's review

**The review found three faults, and all three were the same cause: too much of each board was pinned.**
Scarbutte's bench, its canyon floor and its monument's ground were flat; every board's front ended in a flat
strip; and long slopes read as smeared ramps or staircases. `GENERATION-NOTES.md` now carries each finding in
the relief chapter, from *Grain never moves a marked cell* to *What the relief cannot say*.

**Grain never moves a marked cell, and every board had a large marked cell.** Scarbutte's bench was one `area`
mark at 26, and every board had a rectangle band pinned flat across its lip. The bench is now unpinned and
rolls over two swells and a pan; its `level` fell from 0.64 to 0.24 and its largest flat field from a quarter
of the group to 0.08.

**Every lip is now a line a few blocks in from the strait, wandering eight to ten blocks in x and about five
in height.** Twingill needs none at all: its dale floor ends at the lip at 12, and the ridges' skirts carry the
ground to the edge.

**Scarbutte's canyon is now two negative pushes, not one.** A trough (−4, ±9, falloff 3) runs the whole length,
and a slot (−8, ±4, falloff 3) sits inside it in two reaches. Each wall therefore steps once. Both carry
`roughness` 0.5, so the walls wander, and the floor follows the bench's swells rather than lying at one height.

**Scarbutte's rim is now a push, not four scarps.** The tableland is one push of 12 over a spline ring with its
back off the board, falloff 4 and roughness 0.5. The rim follows a curve, and the top carries a swell.
The pass is `amounts` falling to 3 near (−102, −42).

**Kelderfell's scarp is ten short runs rather than four.** The runs turn 10–16° at each corner, curving behind
the monument's shelf and bowing out to the south. Transects through six corners fall monotonically, so there
is no corner ridge. The lower slope carries a spur and two swales, so its contours bend rather than running
parallel.

**Cinderhowe's rim crest wanders between 33 and 44 and its radius between 23 and 29.** Its floor mark shrank
from a disc 28 across to a bevelled lobe round the monument, so the crater dishes rather than lying flat.

## The third pass: the grain was noise

**The author found Scarbutte better and worse at once: the grain added too much noise.** Grain of 1.5 blocks
over 14 drew a scatter of one-block bumps and pits over the tableland and the bench. The three other boards
carried 1.0 over 16. The grain is now 0 on all four, and the swells, spurs, swales and canyon carry the shape
alone.

**The tableland still blotched without grain, and a crown fixed it.** Its top sat within a block of one
height, so it rounded to either side cell by cell. A `crown` of 5 on the tableland push gives it a fall of
about a block in nine toward the back, and the contours now run as lines. The spawn still stands level at 41.
`RL6` now names that crown against the cliff's skirt, which is the cliff being a cliff.

**The remaining jitter was the pushes' `roughness`, and 0.5 is where it stops.** Scarbutte's pushes carried
1–2, which on its steep faces reads as single-block chatter. Every push on the board now carries 0.5.

## The four boards, where each feature is

Coordinates are team 0's, in blocks; team 1 has the same ground turned about (0, 0).

### Kelderfell

| Feature | Instrument | Where | Height |
|---|---|---|---|
| spawn bench | area mark | x −136…−108, z −14…14 | 36 |
| scarp, north arm | five `scarp` marks | (−118, −88) (−108, −66) (−100, −50) (−95, −37) (−92, −25) (−92, −14) | 35 over 23 |
| the pass | nothing: the ground between the arms grades | x −92…−88, z −14…8 | 35 → 21 |
| scarp, south arm | five `scarp` marks | (−88, 8) (−84, 20) (−79, 33) (−78, 47) (−81, 61) (−84, 72) | 33 over 21 |
| stair up the south face | `line`, h per vertex | (−70, 22) → (−92, 22) | 21 → 33 |
| monument shelf | area mark | centre (−68, −18), r 8 | 22 |
| lip | `line`, r 2 | x −18…−28 wandering | 10–15 |
| fell massif | push, crown 16 | centre (−134, −86), off the coast | peak y69 |
| south headland | push, crown 7 | centre (−98, 68) | +16 |
| spur | push +3, crown 2 | centre (−50, −2), 48 × 10 | |
| swales | pushes −3 | (−60, 36) and (−66, −52) | |
| tarn hollow | push −7 | centre (−42, 30) | floor about y6 |
| knoll | push, crown 4 | centre (−52, −46) | +10 |

### Twingill

| Feature | Instrument | Where | Height |
|---|---|---|---|
| dale floor | `line`, r 8, h per vertex | (−104, 0) (−94, 10) (−76, −4) (−58, 8) (−40, −6) (−24, 4) (−8, 0) | 29 → 12 |
| the gill | push −4, falloff 2, band ±3 on the same course | from (−94, 10) to the lip | 4 below the floor |
| north ridge | push, crown 8 | centre (−78, −60), 108 × 22 | +22 |
| coombes | pushes −6 | (−90, −46) and (−54, −48) | |
| south fell · knott | pushes, crowns 8 and 6 | (−100, 48) and (−44, 64) | +24 · +18 |
| monument terrace | area mark | centre (−66, 20) | 24 |
| holm | area mark | centre (−38, −24) | 17 |
| spawn bench | area mark | x −136…−110, z −14…14 | 30 |

### Scarbutte

| Feature | Instrument | Where | Height |
|---|---|---|---|
| spawn footing | area mark, lifted by the tableland | x −136…−108, z −14…14 | 41 |
| tableland and rim | push +12, crown 5, falloff 4, roughness 0.5, over a spline ring | rim (−100, −100) (−96, −70) (−104, −46) (−96, −26) (−86, −8) (−88, 10) (−80, 30) (−90, 52) (−98, 76) (−94, 100) | 38–49 |
| the pass | `amounts` falling from 12 to 3 within 18 blocks | (−102, −42) | about 29 → 25 |
| table swell | push +4, crown 3 | centre (−126, 50) | |
| monument shelf | area mark, bevel 3 | centre (−72, −12) | 26 |
| lip | `line`, r 2 | x −18…−29 wandering | 20–25 |
| bench swells · pan | pushes +5, +4, −3 | (−46, −44), (−42, 40), (−78, 34) | |
| canyon trough | push −4, falloff 3, band ±9 | (−60, −84) (−66, −50) (−56, −24) (−62, −4) (−54, 26) (−62, 54) (−58, 84) | 4 below the bench |
| canyon slot | push −8, falloff 3, band ±4, in two reaches | the same course, broken at z −8…8 | 12 below the bench |
| the crossing | the trough alone | x about −62, z −8…8 | |
| buttes | crownless pushes, falloff 2–3, roughness 0.5 | (−36, −32) +12 · (−30, 34) +10 · (−42, 10) +8 · (−78, −50) +9 | |
| monument | on its shelf | (−72, −12) | 26 |

### Cinderhowe

| Feature | Instrument | Where | Height |
|---|---|---|---|
| crater floor | area mark, bevel 2 | lobed ring round (−66, 3), about 18 × 16 | 13 |
| rim | one closed `line`, r 3, 24 vertices at radius 23–29 | about (−70, 0) | 33–44 |
| west breach | the rim's heights at 180° | (−97, 0) | 24, shoulders 31 |
| east breach | the rim's heights at 15° | (−46, 6) | 15, shoulders 27 and 33 |
| lip | `line`, r 2 | x −17…−28 wandering | 12–17 |
| parasitic cones | pushes with crowns | (−112, −46) +20 · (−34, −54) +12 · (−40, 56) +15 | |
| lava tongue | push +4 | centre (−30, 18), out of the east breach | |
| monument | in the floor | (−66, 4) | 13 |

## The numbers

| Board | walked · scrambled · barrier | relief | level | dead | complaints |
|---|---|---|---|---|---|
| Kelderfell | 27 104 · 1 178 · 1 022 | 6–69 | 0.30 | 49.7% | `RL3`: the stair's side walls, 7 blocks at (−83, 19); `RL5` at 30% |
| Twingill | 24 025 · 1 745 · 108 | 9–49 | 0.22 | 51.5% | `RL5`: 22% level |
| Scarbutte | 22 463 · 1 848 · 2 750 | 11–49 | 0.24 | 58.1% | `RL2`: the rim, the canyon and the buttes are faces; `RL5` at 24%; `RL6`: the crown against the cliff; `RL3` at the spawn, which the transect contradicts |
| Cinderhowe | 29 970 · 2 186 · 182 | 12–51 | 0.15 | 70.9% | `RL5`: 15% level |

Every spawn walks to its monument end to end, and every board's export gate is OPEN. `GO1` is 3.0–3.4 on all
four. `G8` (dead share) and `LN2` (a chain of 120–136 blocks against 110) are refused by the evaluator on all
four. Both follow from a wide single-objective board, and I left them standing, because these are terrain
concepts rather than finished boards.

**`RL5` fires on all four after the second pass, and that is the trade the pass made.** Level ground fell
because the flat ground was the fault. The monument's shelf, the spawn's footing and the crossings are what
stay level.

## What I got wrong

**I added grain as texture, and at a feature size of 14–16 it is noise.** I read the heightmap for whether
the flat areas had gone and not for what replaced them.

**I pinned too much, which is the error the relief chapter already warns against.** A bench, a strand and a
wide crater floor each went in as an `area` mark because each should be *about* that height. Grain cannot
touch a marked cell, so each came out flat to the block. The author saw it at once in the renders, and the
relief read's `level` had said so: 0.64 on the first Scarbutte.

**I placed the first monument in half-blocks, and the offset is in blocks.** The schema's description of a
destroyable's `at` says half-blocks, but the compile reads blocks from the piece's corner. The first
Kelderfell monument stood at the lip. `POST /plan/compile`'s intent is where the anchor is read back.

**A line mark alone does not cut a channel.** Twingill's first gill and Scarbutte's first canyon were line
marks. The ground around each was otherwise unpinned, so the relaxation carried the whole valley or bench
down to the line's height and there was no channel to see.

**Three pushes lifted nothing, because reshaping the outline left their rings over the void.** The relief
read's per-push `cells` said 0, and nothing else said anything.

**A push beside the spawn's bench walled the spawn in.** A push adds to marked ground too, so Twingill's first
dale-head fell lifted part of the bench and stood the spawn hall in a pit.

**My first pass at Scarbutte's pass sagged the spawn by eight blocks.** `amounts` is read at the nearest ring
point, and the spawn's nearest rim point was the pass. The transect caught it: 30 where 38 was meant.

## What worked first time

**`PUT …/sketch/relief/{group}` on a stored map, then `GET …/render/heightmap`, is a three-second loop.** The
outline stays as stored, so a relief can be iterated without a drive. The heightmap render shows a flat
pinned area as one colour, which is exactly the fault the author named.

**A scarp broken into runs with an unpinned gap is a pass.** It needs no ramp: the relaxation grades it.

**A closed line mark with a height per vertex is a crater rim with breaches.**

**Crownless pushes on a falloff of 2–3 are buttes.**

## What I could not say

**Nothing the boards needed was missing from the system, but four limits shaped them.** They are written up
under *What the relief cannot say* in `GENERATION-NOTES.md`. A line mark's band is flat across its reach; a
push has one falloff all the way round; roughness moves only a push's outline; and nothing textures a marked
cell.

**One description is wrong.** `DestroyablePlacement.at` and `CorePlacement.at` are documented in `openapi.json`
as half-blocks from the piece's corner, and the compile reads them as blocks. That is a description fault in
`pgm-studio`, not a missing capability.

**One read misreports.** `RL3` names a seam between a pinned footing inside a push and the spawn room,
the size of the push's lift. The ground there is level. The read compares the footing before the lift with the
room after it.

## Open gameplay questions, decided without the author

| Question | What I decided |
|---|---|
| May a destroy monument stand on the board's centre line, in a crater? | Built on Cinderhowe; it is what gives the board 71% dead ground |
| Should a monument's only approach from the strait cross a canyon at one crossing? | Built on Scarbutte: the trough alone at z −8…8, and the monument on the defender's side |
| Is a caldera's inner wall a fair barrier, with only two breaches into the floor? | Built on Cinderhowe: attackers go through the east breach or build down from the rim |
| Is a 12-block scarp with a pass too much height advantage for the defender? | Built on Kelderfell: the monument stands below the scarp, so the high ground is the spawn's rather than the goal's |
