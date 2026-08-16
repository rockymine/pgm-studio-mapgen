# kerbstone — measured record

DTM, cityscape. `mirror_z`, cell 5, 16 players, board **95 × 201**. A street canyon: one avenue the length
of the board, elevated terrace rows either side, a civic court with a gold-block `cube-3` per team, spawn a
three-storey counting-house at the back corner. This is the run's wings-and-storeys testbed.

## The numbers

| Measure | Designed | Measured |
|---|---|---|
| Board | lane | 95 × 201 |
| Spawn → own monument | 25–50 | **36.1** — spawn (32.5, −92.5), monument (2.5, −72.5) |
| Enemy spawn → that monument | ~3× own | **166.7**, ratio **4.6** (inside p90 5.0) |
| Monument approaches | ≥ 2 | 4 — highstreet front (Δ1), west yard (Δ1), east yard (Δ1), backrow behind |
| Sightline down the avenue | broken | the two-tier octagonal bandstand (Δ1+Δ1 steps) at the axis |

## The buildings (the point of the map)

All from `region/provenance.json`, every prop standing:

| Prop | Style | Wings / storeys |
|---|---|---|
| `hall` | counting house | 13×9 hall, 3 storeys + **projecting** 7×4 wing capped `storeysHigh: 2`, `ridge: AlongZ` |
| `th2` | townside | 9×7 hall + 4×4 **marching** wing, forced `ridge: AlongZ` (proportions tie AlongX) |
| `th1` `th5` `th7` | townside | 2-storey rows on the frontage lines |
| `th8` | counting house | 3-storey west-row block |
| `th3` `th6` | workshop | shed-roof singles |
| `th4` `tower` | terrace | flat-roofed 2-storey; the tower seals the west canyon mouth |
| spawn shell | counting house | the compound at the back |

Probed (the record a claim can be checked against in-game):

| Column | Reads | Proves |
|---|---|---|
| (−8, −95) hall centre | floors y11 / y16 / y20, stone-brick hip at y26 | three storeys stand |
| (−8, −88) wing centre | floors y11 / y16, stone-brick slab roof at y21 | `storeysHigh: 2` honoured; the projecting wing's roof carries below the hall's y26 |

Composition failures on the way: an east-side wing fired `HJ5` in a configuration whose stated clauses it
appeared to satisfy (wing along edge 5 ≤ hall across 9, equal storeys) — repositioned to the south edge
rather than diagnosed to the root; **worth a read of `WingJointRules`' height clause**.

## Paint

`voronoi` flagstones (gravel seams / stone panels) on the avenue, finer cobble-seamed pale panels on the
terrace rows, `checker` polished-andesite/slab court with a **brick rim as the one warm accent**, stone-brick
canyon walls throughout, `voidEnforcement` on — nothing bridges out of the city.

## Faults carried to the report

- Streets on a grid still ate four houses via spline overshoot until every corner was chamfered
  (report fault 4; GENERATION-NOTES §12).
- `relief/read` answers `islands: []` for this (deliberately relief-less) board — indistinguishable from
  the §1 not-rasterizing trap without knowing why.
- Soft `fill-ratio` 0.79 accepted: a walled city is the densest thing the corpus band was never fit to.
