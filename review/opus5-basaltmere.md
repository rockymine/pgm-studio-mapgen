# Basaltmere — the hill has no back to it

> A king-of-the-hill board in a black basalt bowl with one mere in it. The point stands on a stack in
> the middle of the water and can be entered from every quadrant at once.

**In one sentence:** there is exactly one piece of commanding ground on this board, it is an island,
and the four ways onto it — two dry causeways off the benches and two shingle spits off the east and
west flanks — arrive from four different directions, so holding it is holding a place with no back.

90 × 190 blocks, `rot_180`, three surfaces, maxPlayers 20, ground y9..y25, observer y62, score limit
750, one hill paying 1/second on a 6s capture.

## The arrangement

Three surfaces and three shapes: `strand` at 10 (the drowned shelf, crossing the centre and its own
image), `brink`+`bield` at 14 (the benches over the water), `staith` at 15 (the spawn). The board is
one continuous sheet of ground — no void seam — and the `deep` build zone covers the water, so the
one place a player may make ground is the mere.

The relief is four `area` marks and two `push`es. `pan` states the mere floor flat to its own outline,
and its ring **wanders between z 18 and z 34** rather than following the seam between two plan
rectangles — a rim that is a rectangle's own edge reads as a ruler laid across the board. `bench` and
`howe-flat` are the two flats the spawns come out onto; `apron` drops the east bench a hand lower so
the two flanks are not the same ground. The `crag` push raises the west bench seven blocks
(`amount/falloff` 0.44 against `crown`/half-width 0.44).

The stack is a shape with `relief_scope: "exclude"` and `keepClear: true`, so the mere floor and the
stack top meet at a face. A broken ring wall crowns it on a `kind: "made"` layer, with one gate on each
of the four approaches — east, south-east, west, north-west.

## What the reads say

| read | number |
|---|---|
| `03-slopes.txt` | 12 781 walked · 234 scrambled · **720 barrier**; 8 faces, largest 314 at x −45..25, z 2..42 |
| `06-claims.txt` | **placed 38, declined 1** |
| relief read | level **0.649**, largestField **0.477**, 4 faces, 1 cliff, landform *rolling*, **0 seams**, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **49.3 % dead**, 3 journeys — and the coverage walk cannot see a capture point, so this is not the empty-board fault (below) |
| `GET …/incline` | 47.2 % under 10° · 22.9 % teens · 16.5 % twenties · 5.3 % thirties · 8.1 % at 40°+ |
| `05-themes.txt` | basalt 64.2 % · weed 27.0 % · peat 5.8 % · stack 3.0 % |

## Against the fault catalogue

**Objective hidden — no.** `column (0, 0)` reads the pad (white stained clay) at y15 over six courses
of andesite, and nothing at all above it until the observer platform at y57. The crown wall's inner
face stands at radius 9.5 and the pad is 9 blocks across, so the wall is beside the point and not over
it.

**Spawn faces away — no.** Red spawns at (0, 87) with yaw 180 and the hill is at (0, 0), due −z. Zero
degrees off.

**Spawn faces a wall — no.** The spawn-to-board transect along z reads rises 0, falls 4, worst step 1,
0 barrier, 0 scramble, walked end to end.

**Stairs that end nowhere — no**, and this was measured per flight rather than assumed:
`walk from=40,4 to=0,0` (the east spit) is 47 blocks, **0 placed, 0 drops**; the west spit is 46 blocks,
1 placed, 0 drops. The two causeways run 35 blocks for a rise of 2 and the four beaches 12–16 blocks
for a rise of 4. `EL1` complains that `strand`–`brink` steps 4 blocks and is right about the plan and
silent about the board: the four beaches are authored flights and the plan tier walks the pieces flat.

**A straight frontline — no.** There is no frontline in the plan-rectangle sense; the boundary a player
reads is the waterline, and that is the `pan` mark's own wandering ring plus the pool's `shoreWander`.

**Stark contrast with no area separation — no.** The three grounds meet at things: black stack against
green weed at the stack's own face (74 + 54 border cells), and grit bench against weed at the
waterline (458 cells). Both boundaries are a face or a watercourse, not a colour change on flat ground.

**Flat, one theme, empty — no, and the dead figure is not the read it looks like.** Four themes, all on
the ground, none under 3 %. The relief is the healthiest of the four boards: 65 % of the ground under
ten degrees with 48 % of it in one connected field, no seams, no silent marks.

**`GET /coverage` cannot see a control point.** Capture points ride on the *intent*, not on the plan
the coverage walk reads, so on a KotH board the walk knows only the two spawns and has no objective to
travel to — `journeys: 3` where a two-objective destroy board reads ten or twenty-one. The 49.3 % it
reports is therefore not the empty-board fault; it is the read declining to answer. The numbers that do
answer here are the relief read, the incline distribution and the four measured ways onto the hill.

There is still a real question underneath it, and it is the author's rather than the tool's: **more than
half the ground this figure calls dead is open water.** Whether water in the middle of a board is dead
ground at all is a question about how a map plays, and it is in the run report rather than settled here.

## The peat pans, and what grows on this board

A basalt bowl is grit and black rock, and the first build stood eight of its ten stunted dark oaks on
coal ore, cobblestone or gray stained clay — a tree dropped on the rock rather than grown in it. Two
things fixed it. The bowl's flat band now carries **coarse dirt and podzol** among its grit, which is
what blows into a hollow; and two **greaves** — peat pans stated as `exclude` shapes at a fixed height,
so they are flat to their own lip — hold the scrub that used to stand on stone. They carry a fourth
theme, `peat`, at 5.8 % of the ground.

The count came down from ten to eight: the two that still seated on coal ore were removed rather than
moved, because the pans were full and a basalt strand with nothing growing on it is the honest answer.
Every remaining trunk was read back: coarse dirt at (32, 41) and (26, 62), podzol at (−8, 56), grass at
(34, 50), (34, 68) and (26, 73), gravel at (−38, 54) and (40, 38). No masonry, no ore, no stained clay.

## Limits

- 720 barrier cells (5.3 % of ground) in 8 faces. `RL2` reads 0.6 scrambles per barrier and calls the
  elevation ungraded. That is what a terraced bowl of black rock is, and the crossings are stated
  rather than left to be found — but a reader who wants rolling ground will not find it here.
- The water is `level`-stated and therefore carves: every column inside a pool's outline is emptied
  down to the water line unless the shape under it is marked `keepClear`. `DR-DRY` still reports 162
  open columns of dug ground the pool does not cover, which is a dry grit fringe rather than a trench.
