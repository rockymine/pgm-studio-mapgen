# Opus 5.5 — four destroy landscapes, relief only

## What I set out to build

Four destroy boards, their ground and nothing else: no theme, no dressing, no buildings beyond the spawn
shell. The method was the author's. Take a simple plan at one height, reshape its outline, then state the
ground in layers of relief until each board reads as a different kind of place. A destroy board offers more
room than a capture board, so each one carries a landform the capture boards could not hold at their width.

| Board | The one sentence |
|---|---|
| Kelderfell | a fellside falling to the strait, broken by a scarp with a pass in it |
| Twingill | a dale between two ridges, with its gill falling from the spawn's head to the strait |
| Scarbutte | a tableland whose rim breaks onto a bench of buttes, split by a slot canyon |
| Cinderhowe | a caldera on the board's axis, breached twice, with the monument in its floor |

## The method, the same on all four

**The plan is a spawn and one field at y20, with a 32-block build zone between the teams.** The plan uses
`rot_180` with team 0 on x < 0, one pillar-3 obsidian monument a team, and 16 players. The compile fuses the
two pieces into one shape, `field-20`.

**The outline is reshaped point by point, never restated.** Each `build-spec.py` states the vertex moves and
inserts as `editShapes`. The moves run first; the inserts then run edge by edge from the last edge back, so
every index an op names is still correct when it runs. A bend with `side: out` then rounds the result. The
strait edge is left straight, following the author's ruling that a lip is never pulled in.

**The relief is stated in layers, each with its own job.** Each board's layers are, in this order:

1. a **frame of marks** that pins where players stand: the spawn's bench, the lip at the strait, and the
   monument's shelf or terrace;
2. the **board's one big landform**: a scarp, a dale floor, a rim or a crater;
3. **large pushes** for the mass: a fell, ridges, cones;
4. **carving and detail**: negative pushes for hollows, coombes, a gill or a canyon, and small knolls or
   buttes.

## The four boards, where each feature is

Coordinates are team 0's, in blocks; team 1 has the same ground turned about (0, 0).

### Kelderfell

| Feature | Instrument | Where | Height |
|---|---|---|---|
| spawn bench | area mark | x −136…−108, z −14…14 | 36 |
| scarp, north runs | two `scarp` marks | (−114, −84) → (−98, −40) → (−92, −14) | 34 over 22 |
| the pass | nothing: the ground between the runs grades | x −92…−88, z −14…8 | 34 → 22 |
| scarp, south runs | two `scarp` marks | (−88, 8) → (−80, 36) → (−64, 84) | 34 over 22 |
| stair up the south face | `line`, h per vertex | (−70, 22) → (−92, 22) | 22 → 34 |
| monument shelf | area mark | centre (−68, −18), r 8 | 22 |
| fell massif | push, crown 16 | centre (−134, −86), off the coast | peak y68 |
| south headland | push, crown 7 | centre (−98, 68) | +9 |
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
| tableland | spawn bench and the rim's high band | x < −90 | 38 |
| rim | four `scarp` marks | (−98, −84) (−100, −40) (−88, −10) · (−92, 12) (−84, 40) (−100, 84) | 38 over 26 |
| the road down | nothing: the rim is open between runs | x −95…−70, z −10…12 | 38 → 26 |
| bench | area mark | from the rim's foot to x −36 | 26 |
| canyon, north reach | push −12, falloff 1, band ±5 | (−60, −84) (−66, −50) (−56, −24) (−62, −8) | y14 |
| canyon, south reach | the same | (−60, 8) (−54, 26) (−62, 54) (−58, 84) | y14 |
| the crossing | the bench left whole | x about −62, z −8…8 | 26 |
| buttes | crownless pushes, falloff 2–3 | (−36, −32) +12 · (−30, 34) +10 · (−42, 10) +8 · (−78, −50) +9 | |
| monument | on the bench | (−72, −12) | 26 |

### Cinderhowe

| Feature | Instrument | Where | Height |
|---|---|---|---|
| crater floor | area mark | centre (−70, 0), r 14 | 13 |
| rim | one closed `line`, r 4, 24 vertices at radius 26 | about (−70, 0) | 38 |
| west breach | the rim's heights at 180° | (−96, 0) | 24, shoulders 31 |
| east breach | the rim's heights at 15° | (−45, 7) | 15, shoulders 27 |
| parasitic cones | pushes with crowns | (−112, −46) +20 · (−34, −54) +12 · (−40, 56) +15 | |
| lava tongue | push +4 | centre (−30, 18), out of the east breach | |
| monument | in the floor | (−66, 4) | 13 |

## The numbers

| Board | walked · scrambled · barrier | relief | level | dead | complaints |
|---|---|---|---|---|---|
| Kelderfell | 27 160 · 1 150 · 994 | 6–68 | 0.37 | 49.7% | `RL3`: the stair's side walls, 7 blocks at (−83, 19) |
| Twingill | 24 051 · 1 723 · 104 | 8–48 | 0.20 | 51.5% | `RL5`: 20% level |
| Scarbutte | 24 197 · 306 · 2 558 | 14–38 | 0.64 | 58.1% | `RL2`: the rim, the canyon and the buttes are faces |
| Cinderhowe | 28 826 · 2 414 · 1 098 | 13–51 | 0.24 | 70.9% | `RL5`: 24% level |

Every spawn walks to its monument end to end, and every board's export gate is OPEN. `GO1` is 3.0–3.4 on all
four. `G8` (dead share) and `LN2` (a chain of 120–136 blocks against 110) are refused by the evaluator on all
four. Both follow from a wide single-objective board, and I left them standing, because these are terrain
concepts rather than finished boards.

## What I got wrong

**I placed the first monument in half-blocks, and the offset is in blocks.** The schema's description of a
destroyable's `at` says half-blocks, but the compile reads blocks from the piece's corner. The first
Kelderfell monument stood at the lip. `POST /plan/compile`'s intent is where the anchor is read back, and
I now check it before driving.

**A line mark alone does not cut a channel.** Twingill's first gill and Scarbutte's first canyon were line
marks. The ground around each was otherwise unpinned, so the relaxation carried the whole valley or bench
down to the line's height and there was no channel to see. A negative push along the same course,
carved after the solve, is what makes a channel. The ground either side needs a mark of its own (Scarbutte's
bench) or a push-built side (Twingill's ridges).

**Three pushes lifted nothing, because reshaping the outline left their rings over the void.** They were
Kelderfell's headland and Twingill's two dale-head fells. The relief read's per-push `cells` said 0, and
nothing else said anything. The headland moved to straddle the coast. The dale-head fells then held about ten
cells of land each, which `RL6` read as a crown of 4 blocks a block, so I removed them.

**A push beside the spawn's bench walled the spawn in.** A push adds to marked ground too, so Twingill's first
dale-head fell lifted part of the bench and stood the spawn hall in a pit. The rule is the one
`marks-and-pushes` states: keep the ring plus its falloff off any mark that has to hold.

**A spawn piece 24 × 32 builds a hall 18 × 30.** `ST9`/`ST10`/`WX13` said so. The spawn piece is now
20 × 16 on every board.

## What worked first time

**`editShapes` ordered last-edge-first.** Every op on all four outlines landed exactly where it was stated.

**A scarp broken into runs with an unpinned gap is a pass.** It needs no ramp: the relaxation grades it, and
on Kelderfell the spawn-to-monument walk goes through it with a worst step of 1.

**A closed line mark with a height per vertex is a crater rim with breaches.** It is one mark, and the breach
is simply a lower number at one vertex.

**Crownless pushes on a falloff of 2–3 are buttes.** Each stands off the bench on its own face.

## What I could not say

Nothing the boards needed was missing from the system. One description is wrong: `DestroyablePlacement.at`
and `CorePlacement.at` are documented in `openapi.json` as half-blocks from the piece's corner, and the
compile reads them as blocks. The spawn's `at` is documented as blocks and is read as blocks. That is a
description fault in `pgm-studio`, not a missing capability.

## Open gameplay questions, decided without the author

| Question | What I decided |
|---|---|
| May a destroy monument stand on the board's centre line, in a crater? | Built on Cinderhowe; it is what gives the board 71% dead ground |
| Should a monument's only approach from the strait cross a canyon at one ford? | Built on Scarbutte: a canyon with one crossing, and the monument on the defender's side of it |
| Is a caldera's inner wall a fair barrier, with only two breaches into the floor? | Built on Cinderhowe: attackers go through the east breach or build down from the rim |
| Is a 12-block scarp with a pass too much height advantage for the defender? | Built on Kelderfell: the monument stands below the scarp, so the high ground is the spawn's rather than the goal's |
