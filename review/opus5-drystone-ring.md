# Drystone Ring — the road over the ring

> A CTW board adapted from the composed board `players=8 symmetry=mirror_z seed=183`
> (hub `bar`, frontline `none`, wool `donut`, score 0). The composed board rings its wool
> room with a five-piece donut and offers the attack two ways round the hole — both of them
> the same ten-block corridor, 139 blocks — and leaves 175 blocks of the ring's west end
> (4 %) on nobody's route at all.

**In one sentence:** a drystone ring round a thirty-by-fifteen hole, with a timber causeway
walked out seven blocks above its north bar — forty blocks of open deck with a ramp at each
end and nothing in between, which is the third way in and the only quick one.

90 × 100 blocks, `mirror_z`, the moor at surface 12, the spawn garth at 14, the deck at `y18`.

## What the composed board said and what was changed

| Composed | Here |
|---|---|
| north bar one piece `x −65..−20, z 15..25` | three: `bar-e` `x −45..−20, z 15..25` (ten deep, the taper), `bar-w` `x −60..−45, z 10..25` (**fifteen** deep, so the causeway over it leaves a lane beside rather than covering the corridor), `bar-nw` `x −70..−60, z 15..25` (ten deep, because a widened corner is a cul-de-sac) |
| stem `x −20..−10, z 15..30` | unchanged in extent and used as the causeway's ramp |
| west stub `x −65..−55` · room `x −65..−55, z 40..50` | pushed five blocks west to `x −70..−60`, which widens the wool yard |
| south bar `x −55..−20` | `x −60..−20`, so it meets the room's own face |
| spawn room 10 × 10 | 15 × 10 at `x 5..20`, the ring the iron cube needs (`WX8`) |
| no walls, no layers, no elevation | a polyline drystone wall, three made layers, and a two-block spawn garth |

The hole itself is untouched. `SK13` reads a composed subtract as the board's negative space
and refuses any add that fills it, on any layer, and it is right to: what the ring encircles
is the ground the two lanes exist to guard.

## The second storey, and what the storey is

Three made layers, and one authored flight at each end:

| Layer | `base_y` | Holds |
|---|---|---|
| `trestles` | 11 | eight 2 × 2 spruce trestles, `y11..y17` |
| `causey` | 18 | the deck, `x −62..−23, z 16..21`, one course at `y18` |
| `causey-rail` | 19 | the log rail along its north edge |

`ramp-up` is an override add on the ground layer, `x −22..−9, z 16..21`, fourteen blocks of
run for seven of rise, rising west off the hub and across the stem. `ramp-down` is its twin at
the far end, `x −68..−63, z 16..29`, dropping south onto the west stub ten blocks from the
wool room's door. Both `relief_scope: "exclude"`, `height_mode: "level"`, `skirt: 0`, a
material rather than a theme.

Measured: the void scan reads `892 cells open x −62..−23 y 12..17 z 16..21` — six clear
courses of lane under a forty-block deck. Transect up the east ramp, `(−4, 19) → (−28, 19)`:
`rises 7, worst step 1: 0 barrier, 0 scramble, walked end to end`, and at `(−28, 19)` the
station reads `ground 12, surface 19, standing: storey` — seven blocks of air under the
walker. Transect down the west ramp, `(−65, 14) → (−65, 36)`:
`rises 1, falls 6, worst step 1, 0 barrier, walked end to end`.

In gameplay terms the storey is a **committed route**. There is no way on or off the deck
between its two ramps: a raider who takes it gives up every turning for forty blocks and is
visible from the whole west half of the board while doing it, and arrives ten blocks from the
wool room's door instead of the sixty-five the ground route costs from the same point. The
defence's answer is not to hold the deck — it is to be at the far ramp when it lands.

## Relief

One group, base 12, reach 12, grain 1.1/14. This is a board of corridors, and a rolling
relief inside a ten-block lane is ground nobody can fight on, so the two lanes of the ring
and the crossing's landing strip are **stated flat** (`bar-flat`, `south-flat`, `hub-flat`,
`stub-flat`) and carry no tread. What rolls: a `point` knott on the wide west end (`r 5`,
`h 17`), a `point` brow on the hub's back half (`r 5`, `h 16`), a push north of the ring's
turn, and the garth behind the spawn, which is the one mark carrying a `tread` because it
would otherwise meet the hub on a two-block wall (`EL1` names that seam; the tread is the
answer and the transect walks it).

`stub-flat` was added after a transect read `BARRIER +7 at (−65, 30)` — the first build's
push stood exactly where the causeway's far ramp lands. A ramp with absolute anchors needs the
ground it lands on stated as well.

Relief read: level **0.639**, largestField **0.289**, 0 seams, 0 silent marks. Incline:
44.7 % under 10°, 30.1 % teens, 14.1 % twenties, 7.8 % thirties, 3.3 % at 40° or steeper.

## What it is painted with

Three themes, all on the ground: `moor` 80.9 %, `garth` 11.0 %, `scald` 8.1 %; borders
moor|scald 212 cells, garth|moor 20. The ground family is a cold dark moor — podzol, coarse
dirt and grass over gravel and clay on a `Taiga` tint — finished with a `layered` material on
the **`slope`** axis cutting at 20° and 34°. The built family is drystone: cobble, mossy
cobble and andesite, in the two ramps, the trestles and the wall. `scald` is the third:
two brushes on the ring's two lanes, worn bare where the board is actually walked, each
stated with `height_mode: "raise"`, `base_height: 0` so it is a scope candidate at all.

**The drystone wall is a `polyline`** — four points at `z ≈ 48` from `x −56` to `x −22`,
radius 1, `stroke_edge: "solid"`, `height_mode: "raise"`, `base_height: 2`. The rasterizer
splines the points before offsetting the band, so four clicks draw a curve rather than a chain
of chords, and the wall runs the south lane's outer edge as cover that is not a landform.

## The numbers

| Read | Answer |
|---|---|
| `/plan/evaluate` | score **0**, valid; `SP2` and one `EL1` at the garth seam |
| `/preflight` | **export gate OPEN** |
| `/coverage` | reached 4 488, decorated 60, dead 2 — **0.0 %** (composed: 4 %, and 9 % after the first widening) |
| `03-slopes.txt` | 4 222 walked, 242 scrambled, 86 barrier; 4 faces, largest 38 |
| `06-claims.txt` | placed 22, declined **0** |
| `/plan/flow` before | attacker **139**, defender **89**; 2 ways in, the other 1.04× the shortest |
| `/plan/flow` after | attacker **144**, defender **94**; 2 ways in at the plan tier — the third is the causeway, which the plan cannot state |
| relief read | level 0.639 / 0.289, 0 seams, 0 silent |

## What is not here, and why

**No building.** `POST …/sketch/seats` answers **eight** house seats on the whole board at
11 × 9 and none of them on this team's own ground. An eight-player ring is ten-block corridors;
an 8 × 8 footprint on the hub refuses `DR-PASS` because the spawn march claims `x 6..14` from
`z 21` back to the door and there is not eight blocks of passable ground on the other side.
What is built here is the causeway, its trestles and the drystone wall.

## What went wrong

**Widening the bar made the dead ground worse, not better.** The composed board leaves 4 % of
its ground off every route; widening the whole north bar to fifteen blocks — so the deck would
not cover the lane — took it to **9 %**, because the extra width at the ring's corner is a
cul-de-sac the route turns before reaching. Splitting the bar so only its middle third is wide
took it to 0.0 %. `GET …/plan/flow`'s *"what no journey reaches"* is the read that says so, and
it costs no build.

**Two paint refusals in one post.** `PT1`: podzol is a surfacing block and was sitting one
course below the top of a `layered` depth stack. `PT4`: the drystone wall's cell pattern stated
no `rise`, so every block of the wall's column resolved alike and it would have read as
vertical stripes. Both were one-line fixes and both were refusals rather than complaints.

**Three sites for one building, and then none.** `DR-KEEP` at `(6, −21)` was the enemy spawn's
own door approach reached by the `mirror_z` image of a building on the hub; moving it twice more
produced `DR-PASS`. The instrument that should have been used first is
`POST …/sketch/seats`, and when it answers eight seats the answer is that the board has no room.
