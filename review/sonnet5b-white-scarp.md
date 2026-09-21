# White Scarp — destroy-the-monument

**In one sentence:** a wind-scoured chalk down where each team's beacon monument stands alone on open
sward, a quarry cut into one flank and a stand of wind-bent pines guarding the other, the two teams'
ground joined only by a build zone over void.

208 × 64 blocks (after narrowing from an initial 208 × 80 to cut the flank's dead share), `rot_180`,
`maxPlayers` 8, base surface 10.

## Where the plan puts things

Two pieces a side — `spawn` and `field` — and an 8-cell (32-block) build-zone strait between the two
team islands. The monument sits inside `field`, 44 blocks from its own spawn by walk and 146 from the
enemy's, a ratio of 3.32 — inside `GO1`'s 3.0–4.0 band on the first geometry that also cleared `GO3`
(102 blocks between the two monuments, inside 85–150) and `GO4` (44, inside 40–90).

No manual retuning beyond nudging the monument's `at` twice against `plan/inspect`'s own numbers.

## The ground

One theme, `chalk-down`: grass-over-dirt on the flat, coarse dirt on the shoulder, sandstone-over-stone
on the face — a `layered` material on the **slope** axis, cut at 20°/40° against the board's own
`incline` read (78.9% under 10°, 12.4% at 10–19°, 8.7% at 20°+).

The quarry is a single `area` relief mark sunk to y4 against the base of y10, `bevel: 5` so its rim
grades rather than walls; the pine knoll is a `push`, `amount: 5`, `crown: 0` after a first pass with
`crown: 2` drew an `RL6` seam where the push's skirt and crown met at different rates.

A worn dirt/coarse-dirt/spruce-plank path (a `cell`-patterned stroke) runs from the spawn door to the
monument. Four spruce on the knoll, three andesite erratics near the quarry rim and the cut. A spawn hall
forked from the `desert brick` preset: footing left null, wall rebanded to chiseled stone brick over
sandstone, roof to stone brick and smooth sandstone.

## What checks it

`03-slopes.txt`: 9644 walked, 12 scrambled, 8 barrier, 2 faces (largest 4 cells). `06-claims.txt`: 18
props placed, **0 declined**. `preflight`: export gate **OPEN**.

`coverage`: 27.4% dead, four patches of 600–700 cells each at the quarry/knoll flank corners, one block
from used ground — the two flank features (quarry, knoll) are reachable but off the spawn↔monument
route, which the board accepts as the approach diversity the flanks are for rather than as a fault to
route around. `plan/evaluate`'s own `G8` (`dead-share`) term reads 0.328 against an authored `[0, 0.12]`
band; per the run's brief this term has no export gate and the number is reported rather than chased,
since the alternative is deleting the quarry and the pines.

## What went wrong

The first pass's spawn piece (40×48 blocks) tripped `ST9`/`ST10` — a spawn footprint over 20×20 and a
spawn piece over 20×30 — both complaints rather than refusals, fixed by shrinking the piece to 20×24 and
stating an explicit 16×12 footprint. The push's `crown: 2` against its `falloff`-driven skirt produced an
`RL6` seam at the knoll's own outline; setting `crown: 0` removed it. Both were caught by
`plan/evaluate`'s lint and `sketch/relief/read`'s complaint list before any picture was opened.
