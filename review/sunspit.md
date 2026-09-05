# sunspit — measured record

CTW, summer beach. `rot_180`, cell 5, 16 players, board **120 × 200**. Two shores facing each other over an
open sea; each team a village terrace behind a spawn headland, a wool at the head of a walled lane east, an
isolated pier wool west over a 15-block strait, and a lagoon behind the beach bar. **Evaluator score 0,
valid.**

## The board

Thirteen pieces on the authored half. The shore is a bar the width of the board with **two legs extruding
from it** into the sea, ten blocks out and fifteen wide, and a build zone attaches flush against each leg's
tip and runs across to the enemy's leg at the same x — the composer's `frontline twin`, which is how a
two-legged front is drawn. The gap a team pays for is 20 blocks, tip to tip. Between the two legs the
channel is void until the tidal `water-lane` floods it, and it then opens a third way over, bar to bar,
that neither team's legs cover.

## The numbers

| Measure | Rule | Measured |
|---|---|---|
| Crossing frontline | FR8 span ≥ ⅓ · FR9 ≥ 15 blocks | four 15-block runs, straight, share **1.00** on the leg tips they dock against |
| Team ↔ team strait | CT12 15–40 | **20** |
| Pier ↔ mainland strait | CT12 15–40 | **15** |
| Spawn ↔ wool balance | WL9 ratio ≤ 1.232 | in band, and the band is a guideline (author) |
| Approach wall | — | 10 blocks, the spur's own width, halfway along it |
| Ground that steps | 03-slopes | 10726 walked, 262 scrambled, 40 barrier — **the two approach walls and nothing else**, 20 cells each |
| Dressing | 06-claims | **placed 45, declined 0** |
| Ground no journey reaches | coverage | **0.0% dead** — every cell of the board is on somebody's route |
| Export | preflight | **gate OPEN** — round-trip, mirror, buildability, traversability per team |

## What it exercises

- **A crossing that reads as one.** The land itself reaches out at the two places it may be crossed, and the
  build zone begins where that land stops, so a player standing on the beach can see where the front is
  rather than having to read the region list. A `worn` slipway in smooth sandstone runs the length of each
  leg to its tip.
- **A wool at the head of a walled spur, and the wall halfway along it.** The bluff is a ten-block spur —
  the same width as the pier room, so the board's two wools are one shape twice — cut into three pieces so
  the wall has an interface to stand on in the middle of it rather than at its mouth: a **ramp** climbing
  from the dune, the **wall**, then a **flat shelf** two blocks higher carrying the **room** at the board's
  back edge. The ramp is the shape's own `anchor_heights`, 11 at the dune and 13 at the wall's foot over ten
  blocks. Read back at `x = 30`: ground at y10 to z74, y11 to z78, bedrock to y15 at z79–80, y14 behind —
  three courses of wall from the attacker's side and one from the defenders', which is a parapet. The spur's
  flanks are cliffs, so the wall is the only way in and cannot be walked round.
- **A spawn sized for what stands in it.** A 15 × 20 piece carrying a stated 11 × 11 hall — two blocks of
  ground each side and behind, and the rest of the depth is the door apron, where the iron cube seats on the
  player's right as they leave. `POST /plan/room` answers the marker and the cube for the piece and the
  building as stated, and the plan states what it answered.
- **Ramps as shapes, not as relief.** Every tier above the strand is `relief_scope: exclude`, so a relief
  mark on one of its seams does nothing; the three Δ2 seams are tilted quads at 4:1 with `height_mode:
  level` and a thickness per vertex. `03-slopes.txt` reports no barrier anywhere on the board.
- Water props as sea: a `natural` lagoon behind the bar, a `stream` tide pool, banks in sand.
- `laidLog` birch pier deck, `cell` dune-grass patches, sand/sandstone `noise` strand.
- Five sea rocks in one `cell` of stone, andesite and cobblestone — grey against the sand rather than sand
  on sand.
- `@stilts-grass`, the stilts style forked with a grass plate, so the house standing on the village green
  keeps the green under it instead of laying a plank floor over it.

## Faults on the way

- The spec was version 1 and `PL15` refused it: marker offsets are blocks from the piece corner and version
  1 stated them in cells. Migrating them ×5 is the whole of that change.
- `themeById`/`shapePropsById` were keyed on `s7`, the positional id `TS82` replaced, so the pier deck's
  theme and its `relief_scope` were silently absent. Every key is now a compiled id.
- `FR8` measured the old crossings at **0.25** of the face they docked against — the funnel fault, and the
  reason the build zones could not be found from the ground. The first fix cut bays into the shore and put
  the zones in the gaps, which reads as the inverse of what a player expects: the author's correction is
  that a zone attaches against an extrusion, and `examples/generator-32/seed0` is the shape.
- `WX8` refused the old iron marker outright: a 15 × 10 spawn piece leaves a one-block ring around its
  shell, and a 3 × 3 cube with two blocks of air does not fit in one.
- `CT12` measured the pier strait at **10**, under the 15 a CTW crossing wants.
- `PT1` refused the backshore theme: a `cell` picking grass filled both surface courses with it, because a
  surfacing block is one course and what is under it is soil. It is a `layered` stack now.
- `walls[0].side` and `relief.team.stairs` were fields no part of either document has, and `RQ3` named both.
- The cottage stood in the spawn door's apron, which runs fourteen blocks down the middle of the village;
  the village row moved west of it and the cottage east of the road.
- The spawn's authors reached the map row but not the intent, so `EX6` left the observer platform's authors
  board off. `drive.py` now carries the list onto `meta.authors` as its own docstring always said it did.

## Read and left

- `WX11` on the approach wall's two ends and on each wool room's entrance redstone: all of them stand where
  the land stops, which is the ledge case the rule says to ignore. The wall's ends are at the lane's own
  cliffs on purpose, because that is what stops it being walked round, and a wool room at the head of a spur
  or on a pier meets the sea with the same bedrock face.
- `HS10` on the `@stilts` cage and on the village's stilt house: a wool cage needs the floor players stand
  on, and the house's plate is grass on purpose, which is the case the rule names as the one to keep.
- `EL1`/`SP8` still fire at the plan tier, which judges rectangles and cannot see a layout shape. The ramps
  are layout shapes; `03-slopes.txt` is the read that answers whether they walk, and it reports no barrier.

## Open questions for the author

- The defender pays blocks to get over their own approach wall to their own wool room, because an ST4 wall
  is bedrock and bars the lane for both sides. It is a parapet from that side rather than a cliff, but it is
  still a climb, and whether a defender should have a way round it is a question about how the map is played
  rather than one this repository can settle.
- The legs are cell-square because the shapes either side of them abut ground a player walks, and a bend
  would open those seams. Whether a squared-off headland is right on a beach is the author's call.
