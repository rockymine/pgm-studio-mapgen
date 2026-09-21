# Turbary Cut — destroy-the-core

**In one sentence:** a cut-over peat moor where each team's core stands on a raised turbary island with
ground all round its casing to catch the leak, a drained cutting into one flank and alder scrub on the
other, the two teams' banks joined only by a build zone over the open bog.

208 × 64 blocks, `rot_180`, `maxPlayers` 8, base surface 8, biome **Swampland** (set after the drive, via
`PUT /sketch/biome`, then re-exported — the finish document's driven keys carry no biome field, so this
is the one step outside `drive.py`'s loop).

## Where the plan puts things

The same two-piece skeleton as `white-scarp` — `spawn`, `field`, an 8-cell build-zone strait — reused
because the arrangement had already cleared `GO1`/`GO3`/`GO4`/`CT12` there and a core asks the plan tier
for nothing a destroyable does not.

The core keeps the vocabulary's own defaults (`lava: 3`, `lavaHeight: 3`, `float: 6`, `leak: 5`,
`openTop: false`) rather than restating them: 44 blocks from its own spawn, 146 from the enemy's, ratio
3.32, 102 blocks between the two cores — the same geometry as `white-scarp`, because the same lane
satisfies the same four bands.

**The core floats by design.** At `float: 6` the casing stands six blocks clear of the ground the relief
actually leaves under its column, which is what lets the lava fall and leak rather than pool with no
floor under it (`techniques/objectives-and-clearances`). Nothing here overrides that default — a core on
the bare ground cannot leak at all.

## The ground

One theme, `peat-moor`: podzol-over-dirt on the flat, coarse dirt on the shoulder, gravel-over-dirt on
the face, banded on **slope**. The wall bucket is coarse dirt rather than a rock, so a cut bank reads as
turned earth instead of quarried stone — the deliberate difference from `white-scarp`'s sandstone wall,
so the two boards' cut faces do not read as the same material in two colours.

The drained cutting is an `area` mark sunk to y2; the turbary mound is a `push`, `amount: 4`. A worn
track runs spawn to core. Four birch "alder" scrub on the mound, three andesite (mossy) erratics near
the cutting.

## What checks it

`03-slopes.txt`: 9644 walked, 8 scrambled, 12 barrier, 2 faces (largest 6 cells). `06-claims.txt`: 18
props placed, **0 declined**. `preflight`: export gate **OPEN**.

`coverage`: 43.0% dead — higher than `white-scarp`'s 27.4% despite the identical footprint, because the
core's larger clearance box (a 5×5×5 casing against a destroyable's 1×1 pillar) removes more of the
reached area around the goal itself; not chased further, per the same reasoning as `white-scarp`.

## What went wrong

Nothing at the plan or store tier — the geometry was proven on `white-scarp` first. The one real question
was **where the biome lives**: it is a `SketchLayout` field (`biome`/`biomeSource`), readable and
writable at `GET`/`PUT /map/{slug}/sketch/biome`, but it is not one of the keys `tools/README.md` lists
for a driven finish document, so `drive.py` never patches it from `sonnet5b-turbary-cut.finish.json`. It
was set with one extra `PUT` after the drive and the world re-exported (and re-unzipped) by hand rather
than through a second `drive.py` pass, which would have overwritten the whole stored layout — including
the biome just set — from the finish document again.
