# Goldbank Quarry — ground that people cut away

A destroy board that is one worked limestone quarry. Both destroyables stand on the floor of it,
under everybody: the rim is at y32, the pit floor between y15 and y22, and the two goals sit on the
pit's two ends with the deep sump between them.

Slug `opus5-goldbank-quarry` · 104 × 224 blocks · rot_180 · 20 a side · destroy.

## How it is meant to play

The quarry is cut into a grassed fell that rises behind each spawn and off the back of the map. A
team leaves its hut on the brow, crosses the rim, and goes down — either by scrambling the benches,
which are 3-block risers, or by the haul road, which is the only walked way and puts a player in
the open for its whole length. The pit is entered through one of two notches, one on each team's
side; everywhere else its face is sheer and you get in by dropping and cannot get out again.

That is the board's whole argument. An attacker commits: the walk from the far spawn is 139 blocks
with no drops, and the last of it is a descent into a hole with two ways out, both behind the
defender. The goal is `cube-4` ender stone floating 4 over the floor at y26–30, so it cannot be
covered from above and cannot be reached from the benches.

## What the ground is made of

Three tone families, named before anything was painted, and none of them borrows from another:

- **ground** — pale gold oolitic limestone. Buff sandstone, smooth and chiselled sandstone, end
  stone, sand and gravel. Warm, never grey: this is the run's warm-pale board.
- **built** — the quarry plant. Spruce over iron on a stone-brick footing, dark against the ground
  it stands on.
- **accent** — rust. One bed of hardened clay in the strata, and one course of it in the winding
  house's upper wall.

Three themes, and the census reads `goldmoor` 48.7% · `quarrypit` 37.6% · `quarryface` 13.8%, with
borders between all three.

Every ground theme's surface is a `layered` stack on the **slope** axis, so the cut is finished by
its angle and not by its height. `incline` read 61.9% of the board under 10° and 7.5% at 40° or
steeper, and the cuts were set to that: turf to 18°, soil and rubble to 42°, bare limestone above.
The fell is at 39° by construction, which keeps it the one grassed thing on the board.

The strata are one stack shared as the `wall` **and** the `fill` of every theme, so each bench face
shows the same beds in the same order and a column read runs them bedrock to top:

    (-32, -49)  y19-20 Gravel · y16-17 End Stone · y13-15 Sandstone · y12 Hardened Clay
                y8-11 Smooth Sandstone · y1-7 Sandstone · y0 Bedrock

A stack stated in `surface` alone would have banded the top four courses and left the face plain,
and the face is the entire point of a quarry.

## The techniques, and what each one bought

| | |
|---|---|
| `push`, one, behind the spawn | the unworked fell. Its ring sits past the coast at z −112, so the crest is off the map and what is on it is one uninterrupted climb. 16 over a falloff of 20 is 0.80 courses a block; crown 10 over a half-width of 12 is 0.83. The two agree, so there is no step at the ring |
| `area` marks, five | the rim, two benches, the spawn apron, and the hut's own pad. Only ground a player walks |
| `step: 3` | the benches. The marks are spaced with gaps, and the gap is where the terracing happens: the relaxation grades, the quantum snaps it into risers |
| `line` mark with `tread` and `batter` | the haul road. A 3-cell tread is the running surface; `batter: 34` cuts the bank either side of it in degrees rather than letting it spread over the whole band |
| `sink`, `skirt: 1`, notched | the deep cut. `anchor_heights` on a sink state depth per vertex, and the ring is its own rot_180 image, so the fan lays it back over itself instead of beside itself. Two of its twelve vertices carry depth 1 and their images carry 1 too — one shallow ramp in on each team's side |
| `sink`, `base_height: 1` | the three worked-bench patches and the spoil heap. A theme patch has to be a *standing* shape or it owns no columns at all (below) |

## What went wrong

**The worked-ground theme painted nothing, and nothing said so.** The first build's census read two
themes over 23,296 cells; `quarryface` was in the registry, keyed onto three `addShapes` polygons,
and absent from the world. An `add` with no `height_mode` is "the flat one-block behaviour at y=0",
so it never wins a cell whose ground is twelve blocks tall, and a theme scope it does not win is a
theme that paints nothing. There is no warning for this — the store answers 200, the gate opens.
`05-themes.txt` is the only thing on the board that reports it. Declaring `height_mode` made the
shapes standing and the census went to three themes.

**Then the fix flattened the benches.** The replacement patch was one polygon across the whole bench
band. A standing shape reads the median ground under its own footprint, so a patch laid across a
slope comes out a flat plate — the transect down x −20 read `29 29 29 29 28 28 … 26 25 25`, which is
a ramp where three 3-block benches had been. The patch is now one per bench **tread**, on ground
that is flat, and the same transect reads `32 32 32 32 … 28 28 28 27 26 26 25 25`.

**The spawn met the world with a wall of bedrock.** `WX11` named it exactly: the hut stood 3 blocks
above the ground beside it at (−11, −81), and a stamped shell fills the column under its whole
footprint and levels it at the footprint's highest. The apron's lobed ring had left three cells of
the camp's west side outside it. A `roompad` area mark drawn wider than the hut on all four sides
cleared it.

**`GO1` and the board's identity pull against each other, and the rule won.** A destroy goal is to
sit three to four times as far from the enemy's spawn as from its own; goals in the middle of a
shared pit cannot. The first arrangement measured 1.13. Lengthening the board to 224 and moving each
goal to its own end of the pit brought it to 3.37 without taking either goal off the quarry floor.
The cost is that the pit's deepest ground, at y15, is the contested middle rather than where the
goals stand — the sink's depth interpolates inward to its medial axis, so notching two opposite
sides makes a bowl rather than a flat-floored box.

**Standing complaints, not faults.** `RL3` twice: `bench`/`roompad` and `haul`/`roompad` meet on a
3-block step. The rule says so itself — *"Where the step is what the map is for, a `scarp` states a
drop outright and is not reported here"* — and a quarry bench is that step. The routes measure
`walked end to end`.

**`relief.stairs` is not a field.** Every build of this board stated `stairs: true`, which
`GENERATION-NOTES` describes as the instrument that cuts a way up out of terraced ground. The studio
answered `RQ3` — `SketchReliefJson` carries `base`, `reach`, `step`, `landform`, `grain`, `marks`
and `pushes` and nothing else. The key was taken out of the spec after this board's last drive
rather than before it, so the committed spec differs from the document that was driven by exactly
that one line; the world is identical, because the field was never read. The quarry therefore has no
automatic ways up out of its benches, and the haul road and the two notches are all there is — which
is the board it should have been anyway, but it is so by accident and the reader should know.

**An anomaly I could not attribute.** A cross of three red wool blocks stands at y70–72 over red's
destroyable at (−32, −49) — (−32,−49) y70/71/72 and (−33,−49), (−31,−49), (−32,−48), (−32,−50) at
y71. Blue's goal at (31, 48) has none. It is above the y65 build ceiling, it is in no region in
`map.xml`, the compiled intent is symmetric and states nothing of the kind, and the section renderer
classes it as `destroyable/core`. I did not find the rule that puts it there and have not guessed
at one.

## Numbers

    03-slopes   21,136 walked · 828 scrambled · 1,332 barrier · 20 faces, largest 368 at x -51..-14 z -60..42
    06-claims   placed 50, declined 0
    relief      group team  cells 15,892  low 26  high 32  symErr 0
    coverage    55.7% reached · 11.5% decorated · 30.6% dead · 2.2% route
    incline     0-9° 61.9% · 10-19° 14% · 20-29° 10% · 30-39° 6.7% · 40°+ 7.5%
    preflight   round-trip · mirror · buildability · traversability all pass — gate OPEN
    walk        own spawn door (-2,-76) -> goal: 41 blocks, 0 placed, 0 drops, walked end to end
                enemy spawn (2,76)  -> goal: 139 blocks, 0 placed, 0 drops, walked end to end

`04-routes.txt` reports `barrier +11` and `drop -12` on every route. That is the sweep starting on
the spawn hut's roof: it walks from the spawn point's x,z, which resolves to the top of the column,
and the shell is 11 courses. `04-reach.txt` names the same 49 cells at y43 as unreachable standing
ground, and they are the shell's footprint exactly. The walks above, taken from outside the door,
are what the crossing actually costs.

## Coordinates to check in game

| what | where |
|---|---|
| red's goal, floating over the pit floor | region y26–30 at (−33,−50)–(−29,−46); ground y21–22 |
| the pit's deepest floor | (0, 0) reads y15 Sand |
| the north-west notch, the way down | the pit ring between (−20,−52) and (0,−44) |
| the haul road's tread | (−10,−52) → (44,−76), 3 cells wide, battered at 34° |
| the strata, bedrock to top | `column?at=-32,-49` |
| the unexplained wool | (−32, 70..72, −49) and the four cells around it at y71 |
