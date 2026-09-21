# Sluicehead — a core out on the open floor

A destroy-the-core board in a frozen glacial trough. Each team's core stands on the sluice
floor rather than behind anything, with a moraine ridge over each shoulder and a cut leat
running past it.

**The sentence it was authored to:** *a frozen sluice works where the core stands out on the
open ice with ground all round it, and the ways at it come down two ridges, along a channel
and through a building.*

## Why a core stands where this one stands

**A core is breached where it stands, so it belongs where it will be fought over** — the
author's ruling, and the reason this board puts nothing between the core and the middle. It
is the opposite decision from a wool, which has to be fetched and therefore belongs behind.

**And the casing wants ground all round it.** A core on a group in open sky has nothing to
catch its lava: a breach near an edge ends the objective at once. Block **(20, −64)** stands
fifteen blocks clear of the board's east edge and twenty-one clear of the head's face, so a
breach anywhere on the casing still has terrain under it for the lava to fall to.

`float` 6 and `leak` 5 are stated together because they are one knob — their difference is
how far players must dig — and both are the defaults that make a core completable at all.

## Where it differs from Kilnbrow

The two destroy boards were authored together so the second would not be the first in
different blocks. Kilnbrow is a **terrace over a pan** with the objective on a shelf and the
landforms to one side; Sluicehead is a **trough** — high ground on *both* flanks, a flat
floor down the middle, the objective out on it.

| | Kilnbrow | Sluicehead |
|---|---|---|
| shape | terrace, then pan | ridge, floor, ridge |
| objective | on a shelf, off-axis west | on the open floor, off-axis east |
| from above | one hill | two moraines |
| from below | a worked pit | a cut leat |
| ground family | warm — clay and dry turf | pale — snow over packed ice |
| biome | Mesa `#90814d` | Cold taiga `#80b497` |

## What the ground is made of

Three themes: `ice` the frozen floor (63.1%), `works` the made stone of the head and the
quay (28.9%), `moraine` the rubble the glacier left (8.0%).

**The biome is a palette decision and not a line added at the end.** Snow and ice are blocks,
so a snowfield on a summer biome has a meadow running through it; Cold taiga is what makes
the two agree.

**The bands cut at 30° and 45°, read off this board's own `incline`** — 53.8% under 10° and
13.6% in the 40–49° bucket, so the rock band starts above that population rather than through
it and the moraines carry a bare crest.

## The leat

A `channel`, `form: "canal"`, naming its **layer** — a water prop with none carves against
the top of the stack — stating **no level**, because the floor it crosses is ground that is
already there and the line is found, and kept **level along its whole run**, because a
channel carried down a fall is trenched by the fall's whole height. Its east bank carries a
polyline revetment: a cut leat is walled, and four clicked points spline into that curve.

## The numbers

| Read | Answer |
|---|---|
| `03-slopes.txt` | 10 936 walked · 840 scrambled · 224 barrier; 6 faces, largest 80 at x −18…20, z −87…−85 |
| `06-claims.txt` | 24 placed, **1 declined** — see below |
| `GET …/coverage` | reached 11 153 · decorated 369 · dead 478 of 12 000 = **4.0% dead** |
| `POST …/sketch/relief/read` | group `team`: 4 550 cells, 8…24, relief 16, symmetry error 0 |
| `GO1` | own 58 · enemy 185 · ratio **3.19** |
| `GET …/preflight` | **export gate OPEN**, per team |

## What is outstanding

**One boulder, `rock-w1`, is declined `DR-KEEP`** — it rests at (5, −67), inside the
keep-out of the leat revetment added in the last pass. The fix is a position off
`POST …/sketch/seats`; it had not been applied when this board was committed. The board
exports and plays without it; the prop is simply not in the world.

## What went wrong

**The head did not hold the height it was drawn at, and the ramps stood three blocks proud
of it.** A solved shape's own `base_height` decides nothing about where its ground ends up —
the relief replaces the top of every column it solves. Excluding the head from the solve is
what fixed it, and the transect is the proof:

```
west ramp, x −22 from z −97 to −76
rises 2, falls 4, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
```

Before the exclude the same line read `BARRIER +3 at (−22, −93)`.

**A push lifts everything inside its ring plus its falloff, whatever a mark states there.**
The west moraine's skirt reached the west ramp's foot and left a six-block barrier off the
end of it. Nothing attributes that wall to the push — the surface reports it as terrain —
and the only way to find it was to transect the ramp.

**The board came out grey on the first build, on a board whose whole identity is pale ice.**
Two moraines at `falloff` 12 covered about half the ground and both are rock; the leat's
banks were gravel; the head was bare stone brick. Shrinking both landforms, freezing the
terrace's surface and making the leat's banks ice rather than grit is what recovered it. A
landform is a landform, not the ground.

**A building cannot stand in a channel.** Both houses were first drawn over the leat and both
came back `DR-CLAIM`: a water prop claims the cells it carves, and its claim is its radius
plus its shore, with the shore wandering.

## Coordinates

| Thing | At |
|---|---|
| core (red) | (20, −64) |
| core (blue) | (−20, 64) |
| spawn (red) | (0, −110), door +z |
| west moraine crest | ≈ (−25, −51) |
| east moraine crest | ≈ (27, −36) |
| leat | (−6, −80) → (−4, −44), radius 3 |
| sluice house | x 4…18, z −82…−75 |
| winding house | x 5…15, z −44…−37 |
| west ramp | x −27…−17, z −93…−81 |
| east ramp | x 20…30, z −93…−81 |
| build zone over void | x −35…35, z −20…20 |
