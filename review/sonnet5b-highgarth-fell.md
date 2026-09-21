# Highgarth Fell — a wool and a monument at once

**In one sentence:** a red-earth hill-fort where each team must both hold a beacon standing exposed on
the open yard and carry a wool out of a stone grain-store tucked behind a prepared wall, so the defence
is split between a goal that cannot be moved and one that must be walked home.

240 × 144 blocks, `rot_180`, `maxPlayers` 8, base surface 11.

## Where the plan puts things

`ropeworks-quay`'s four-piece skeleton — `spawn`, `yard`, `approach`, `wool-room`, one wall on
`approach`↔`yard` — carrying a `destroyable` inside `yard` as well as the `wool` in its room.

The first geometry reused `ropeworks-quay`'s own block coordinates verbatim and immediately showed why a
combined board is not two boards glued together: with the beacon at the position that had worked for a
destroy-only lane, `GO1`'s ratio came out **7.32** (band 3.0–4.0) and `GO3`'s separation **278** (band
85–150) — the yard built for a CTW strait is far longer than a destroy lane wants, so the same `at`
offset that is 44 blocks from a CTW spawn is nowhere near in band once the spawn itself sits 166 blocks
from the strait.

The fix was arithmetic on `plan/inspect`'s own numbers twice: first moving the beacon from 44 to 80
blocks out (which cleared `GO1` and `GO4` but left `GO3` at 206, since the two beacons still had to close
a strait-length gap no beacon position alone can shorten), then shrinking the whole spawn-to-strait depth
from 166 to 94 blocks so all three bands become simultaneously satisfiable — after which the beacon at
48 blocks own-side, 174 enemy-side, ratio 3.625, separation 126, cleared `GO1`, `GO3` and `GO4`
together, and `plan/evaluate` returned an empty lint and a score of exactly 0.

## The ground

One theme, `fell`: grass-over-dirt on the flat, coarse-dirt-over-red-sand on the shoulder,
red-sandstone-over-stone on the face — the same slope-banded shape as the other three boards, in the
run's fourth and reddest tone family (red sand, red sandstone, chiseled stone brick), set against a
grass-tinted default biome rather than a special one, so the warm ground carries the colour rather than
the sky. No relief marks — flat yard, per the same "built not landscape" reasoning as `ropeworks-quay`.

A solid dirt/coarse-dirt/red-sand road runs spawn to beacon; a worn version runs approach to store. Two
acacia "wind-bent" trees, three andesite boulders. Both rooms fork `counting house`: the grain-store
keeps its hip roof, the spawn hall turns it gable and rebands the wall to red sandstone over oak.

## What checks it

`03-slopes.txt`: 13472 walked, **0 scrambled, 0 barrier**, 0 faces. `06-claims.txt`: 16 props placed,
**0 declined** (one pass declined `DR-KEEP` twice running — a boulder at (-97,-8) then (-96,9), each
time inside the spawn door's kept-clear approach; the third position, 25 blocks off both the door and the
beacon's clearance box, placed). `preflight`: export gate **OPEN**. `coverage`: **1.2% dead**, the
lowest of the run.

## What went wrong, and the open question it leaves

A `HouseStyle` forked with an acacia-stair doorway head and a sandstone slab fill refused at the store as
`HS4` — "the two corners and the line between them are one head, so they are cut from one material" —
fixed by matching the fill to an Acacia Wood Slab.

The larger lesson is the one named above: **a combined board's numeric bands are not the union of its
two gamemodes' bands taken separately**, because the plan geometry (a CTW-length yard) that satisfies
`CT12` interacts with the geometry (a short lane) that satisfies `GO1`/`GO3`/`GO4`, and the two only
agree at a length neither gamemode's own worked examples land on by default.

Whether a real combined-objective map should therefore prefer a shorter strait (nearer `CT12`'s floor)
so the destroy geometry has more room, or a longer approach chain so the wool room sits properly "behind"
per `approaches.md`, is a question about how this specific gamemode pairing is meant to play that this
run answered by arithmetic rather than by asking; it is recorded as an open question in
`reports/sonnet5b-run1.md` rather than filed as a rule.
