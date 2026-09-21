# Ambertor — the shortest way at the monument is to climb something

> Destroy the monument. A gold limestone pavement with one tor standing against
> the west edge of the contested ground. Its crest is fifteen blocks over the pan
> the goal floats on, so a raider who climbs it bridges *down* onto the objective
> and the defender has to watch the sky as well as the one open lane.

## Where the four things are

| The thing | Where | Measured |
|---|---|---|
| monument | `(12, 62)`, `pillar-3` obsidian, float 4 | own walk **51**, enemy **173**, `GO1` **3.39** |
| the tor | `(-12, 48)`, ring 10 + falloff 10 | crest ≈ y34 against the pan's y14 |
| the flight | `(9, 26)` → `(-8, 54)` | 33 blocks of run for a rise of 15 |
| the east lane | `x 7..24` | 17 blocks wide, `LN1`'s floor is 10 |
| mid band | `x -24..24, z -16..16` | 32 blocks of void, build zone over all of it |
| spawn | `(-2, 104)` on a shelf ten blocks up | three cut ramps off it |

## The one decision the board is built on

**The tor stands against the board's west edge rather than on its centre line,
and that is what makes the two ways at the goal differ in dimension.** A crag
with a lane each side needs a board wide enough for three things and gives two
approaches that differ only in hand; a crag against the edge needs a board wide
enough for two, and what remains is the open east lane or the climb.

**`GO1` is arithmetic at the plan stage rather than a thing found later.** With
the spawns 208 apart along the lane and the monument 45 blocks from its own, the
ratio falls out at 3.39 against a band of 3–4, `GO4` at 45 against [40, 90] and
`GO3` at 127 against [85, 150]. All three were right on the first evaluate.

## What the ground is made of

Three themes. The pavement carries 65.7% of the board's cells and is finished on
the **slope** axis, cut at **20° and 32°** off this board's own `incline` — which
reads 43.2% under 10°, 14.5% to 19°, 11.8% to 29°, a trough of 10.9% across
30–39° and 22.8% at 40° or steeper. The clints (19.0%) are four bare-rock patches,
each an `addShapes` polygon carrying its own theme, and the garth (15.4%) is the
spawn's yard.

The biome is **Savanna** (`#bfb755`), asked of `GET /api/terrain/biomes` rather
than assumed: a tinted block takes its colour from the chunk's biome byte and
nothing else on a board does, so a gold ground wants a dry gold grass rather than
a summer one running through it.

## The techniques, and what each one bought

**A push's two grades must stay inside twice each other.** The tor grades its
skirt at 1.6 blocks a cell and its crown at 0.9 — 1.78× apart. At falloff 13
against a crown of 10 they were 2.1× and `RL6` said the landform stepped at its
own outline.

**A line mark is how a riser is cut, and it wants a tread.** The garth stands ten
blocks over the fell; three line marks six wide grade it, and each carries
`tread: 2` because two marks that pin their bands exactly put the whole difference
between them in one cell — without it `RL3` read five-block steps where the ramps
met the pan and the spawn's own apron.

**A flight is `height_mode: level` with a material rather than a theme.** A stair
is a thing somebody built and a theme is a place. It runs 33 blocks for a rise of
15 and it is the one walked way onto the crag.

## What went wrong

**`EL1` and `SP8` stand on this board and are right about the plan.** They walk
the plan's pieces flat and cannot see a ramp cut into a riser at all. The transect
is the read that answers: down the east ramp, `rises 0, falls 10, worst step 1: 0
barrier, 0 scramble | walked end to end`. The spawn ramp reads the same.

**Fourteen props of twenty had no ground under them.** The board was narrowed
from 80 wide to 48 across two passes of `G8`, and the dressing kept the old
board's coordinates — `DR-SITE` on nine of them at once. Everything is placed off
`POST …/sketch/seats` now.

**The garth has three free columns on it, and the claims raster said so before a
drive did.** A spawn shelf 24 deep carrying a 12 × 12 hall, its door approach and
an iron cube has no room for a second building. The board carries one barn, alone
out on the pavement, and a karst pavement is bare ground on purpose.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| monument | `(12, 62)` | `GO1` 3.39 · `GO3` 127 · `GO4` 45 |
| tor crest | `(-12, 48)` | ≈ y34, fifteen over the monument's underside |
| flight foot / head | `(12, 28)` / `(-8, 54)` | anchors 11 → 26, `skirt: 0`, `keepClear` |
| east ramp | `x 14, z 91..77` | worst step 1, walked end to end |
| field barn | `(-8, 68)` | the one free-standing house |
| whole board | `48 × 232` | 8 056 walked · 818 scrambled · 466 barrier · 14 faces |
| coverage | — | **7.2% dead** |
| dressing | — | 30 placed, **0 declined** |
