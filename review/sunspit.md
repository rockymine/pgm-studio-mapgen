# sunspit — measured record

CTW, summer beach. `rot_180`, cell 5, 16 players, board **120 × 200**. Two shores facing each other over an
open sea gap; each team: a palm village terrace, a walled bluff wool east, an isolated pier wool west over
a 10-block hop, dunes and a lagoon between village and strand. **Evaluator score 0 — no violations.**

## The numbers

| Measure | Rule | Measured |
|---|---|---|
| Spawn → bluff wool | WL2 ≥20 | **43.7** — spawn (−2.5, 97.5), wool (35, 75) |
| Spawn → pier wool | WL9 ratio ≤1.231 | **54.2**, ratio **1.24** — at the authored cap |
| Wool ↔ wool | WL7 ≥~45 | **90.6** |
| Spawn interposed | match-flow §6.4 | 4.3 blocks off the wool–wool line, t=0.42 along it |
| Mid gap | G5 10–20/hop | 20, one hop over the sandbar zone; tidal water lane opens at 45m |
| Wool approaches | WL8 | bluff: single walled chokepoint (wall 20/14 blocks out); pier: isolated, bridge + `zone-pier` entry |

## What it exercises

- **The water-lane export fix, end to end**: `map.xml` carries the `water-lanes` region (4 references) —
  run 2's silent drop is gone.
- An `i`-family walled wool and an `isolated` wool on one board — the two ends of the approach spectrum.
- Water props as sea: a 5-radius `natural` lagoon along each foreshore, a `stream` tide pool, banks in sand.
- `laidLog` birch pier deck (the pattern that cannot be shown as a colour swatch — reads `bend`), spruce-log
  pile rim; `cell` dune-grass patches; sand/sandstone `noise` strand (rise 2 so risers stay sandy).
- `townside on stilts` as the wool cage (a pier building on a pier), `terrace` flat-roof spawn villa,
  a marching-wing cottage in the village row.
- A Bézier `subtract` cove and a Bézier tideflat spit — the silhouette is organic on both flanks.

## Faults on the way

- The first draft filled the mid with a `shoal` piece — the "sea" was land and the water lane covered
  terrain. Redrawn as a true void gap; the lane now reads `WL1`-clean over the void.
- b3 stood on one of its own street's *drawn points* (author error, caught by the provenance census).
- Provenance: `spawn 4 · roomfloor 4 · wool 4 · redstoneline 4 · house 6 · wall 2` — everything authored
  is standing.
