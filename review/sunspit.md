# sunspit — measured record

CTW, summer beach. `rot_180`, cell 5, 16 players, board **120 × 200**. Two shores facing each other over an
open sea; each team a village terrace behind a spawn headland, a walled bluff wool east, an isolated pier
wool west over a 15-block strait, and a lagoon behind the beach bar. **Evaluator score 0, valid.**

## The board

Sixteen pieces on the authored half. The sea is crossed at two **legs**: a 25-block bay cut into each
shore, with a 15-block build zone running the length of it from one team's bar to the other — 30 blocks of
void to bridge. Between the two legs a 10-block tongue faces its twin over 20 blocks, and that gap is the
tidal `water-lane`, which opens mid-match and is then the shortest crossing on the board.

## The numbers

| Measure | Rule | Measured |
|---|---|---|
| Crossing frontline | FR8 span ≥ ⅓ · FR9 ≥ 15 blocks | 15-block runs, share **1.00** on the face they dock against |
| Team ↔ team strait | CT12 15–40 | **30** |
| Pier ↔ mainland strait | CT12 15–40 | **15** |
| Walk to own bluff wool | — | 60 blocks, **7 placed** (over the approach wall) |
| Walk to own pier wool | — | 55 blocks, **22 placed** (the strait) |
| Walk to enemy bluff wool | — | 186 blocks, **32 placed** |
| Walk to enemy pier wool | — | 213 blocks, **50 placed** |
| Ground that steps | 03-slopes | 12086 walked, 242 scrambled, **0 barrier, 0 faces** |
| Dressing | 06-claims | **placed 45, declined 0** |
| Ground no journey reaches | coverage | **0.9% dead**, two patches at the board's back corners |
| Export | preflight | **gate OPEN** — round-trip, mirror, buildability, traversability per team |

## What it exercises

- **A crossing that reads as one.** Each leg is a bay dredged into the beach with the build zone running its
  whole length, so where the sea may be bridged is visible from the shore rather than only in the region list.
  The slipway at each bay's head is a `worn` stroke in smooth sandstone.
- **A wool room behind its wall rather than under it.** The bluff is five pieces — an apron, the room, a
  flank each side, a back — so the room has land on all four sides and no bedrock plinth, and the ST4 wall
  stands 20 blocks wide across the apron's front with the room ten blocks behind it. The bluff's only land
  seam is that wall: the 5-block slot between the village and the apron is void by arrangement, so the wall
  cannot be walked round.
- **A spawn sized for what stands in it.** A 20 × 20 piece carrying a stated 12 × 12 hall, so the ring
  around the shell is six blocks and the iron cube seats in the door apron on the player's right as they
  leave — `POST /plan/room` answers the marker and the cube, and the plan states what it answered.
- **Ramps as shapes, not as relief.** Every tier above the strand is `relief_scope: exclude`, so a relief
  mark on one of its seams does nothing; the three Δ2 seams are tilted quads at 4:1 with `height_mode:
  level` and a thickness per vertex. `03-slopes.txt` reports no barrier anywhere on the board.
- Water props as sea: a `natural` lagoon behind the bar, a `stream` tide pool, banks in sand.
- `laidLog` birch pier deck, `cell` dune-grass patches, sand/sandstone `noise` strand.
- Five sea rocks in one `cell` of stone, andesite and cobblestone — grey against the sand rather than sand
  on sand.

## Faults on the way

- The spec was version 1 and `PL15` refused it: marker offsets are blocks from the piece corner and version
  1 stated them in cells. Migrating them ×5 is the whole of that change.
- `themeById`/`shapePropsById` were keyed on `s7`, the positional id `TS82` replaced, so the pier deck's
  theme and its `relief_scope` were silently absent. Every key is now a compiled id.
- `FR8` measured the old crossings at **0.25** of the face they docked against — the funnel fault, and the
  reason the build zones could not be found from the ground.
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

- `WX11` on the approach wall's two ends and on the pier's entrance redstone: both stand where the land
  stops, which is the ledge case the rule says to ignore — the wall's ends are at the headland's cliffs on
  purpose, because that is what stops it being walked round.
- `HS10` on the `@stilts` cage and on the pier house: a wool cage needs the floor players stand on and a
  jetty wants its deck, which is the case the rule names as the one to keep.
- `EL1`/`SP8` still fire at the plan tier, which judges rectangles and cannot see a layout shape. The ramps
  are layout shapes; `03-slopes.txt` is the read that answers whether they walk, and it reports no barrier.

## Open questions for the author

- The defender pays 7 placed blocks to get over their own approach wall to their own wool room. That is
  what an ST4 wall costs both sides, and whether a defender should have a way round it is a question about
  how the map is played rather than one this repository can settle.
- The bays are cell-square because the pieces either side of them abut ground a player walks, and a bend
  would open those seams. Whether a dredged-looking channel is right on a beach is the author's call.
