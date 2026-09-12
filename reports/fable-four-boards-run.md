# Fable 5.1 — four boards to the author's brief, and a second pass to the author's feedback

Four maps, each authored from one sentence, built through `tools/drive.py` and read back through the
API before any picture was opened. The brief this run was held to is the author's spoken one: think first,
keep each board simple, one ground and a handful of patches, few houses of one family, no grown trees, paths
solid and in three near colours, terrain as layers, the ground finished by its angle, and one attempt at an
underground passage planned bottom-up. The author then read the first build of each board and said what was
wrong with it, and the second half of this report is what changed and why.

| Folder | Mode | The sentence |
|---|---|---|
| `fable-ashcombe-delph` | dtm | a worked quarry on a moor: the monument on the bench above the face, the loading yard below it, and two tunnels through the face that meet under the bench and come up two stairs beside the monument |
| `fable-whinberry-ring` | ctw | composer seed 18 at sixteen players, taken over: three levels, a twin frontline with a bay, a stepping stone on the axis, a defence wall on each wool approach, and the outline pulled into heath by hand |
| `fable-saltwharf` | dtc · dtm | a stone quay under a grass headland: the core on a stepped stone plinth out on the quay, a flat-roofed warehouse either side, a beacon of end stone on the knoll in the corner, the spawn ten blocks up behind, two stone flights and a sandy bank down |
| `fable-hollin-tarn` | dtm | a snowed valley head: the monument on a green knoll off the axis behind a frozen tarn, a brook out of it, a crag on the east shore, spruce shoulders either side, the lodge at the head |

Every board exports with the gate OPEN and nothing declined. Each `specs/<slug>/build-spec.py` writes the
plan and the finish; the driver writes the rest.

## The numbers, before the pictures

| Board | 03-slopes (walked · scrambled · barrier) | 06-claims | own → goal | enemy → goal |
|---|---|---|---|---|
| Ashcombe Delph | 15309 · 1222 · 901, seventeen faces | 36 placed, 0 declined | 43, nothing placed | 163, the sound bridged |
| Whinberry Ring | 4126 · 0 · 0 | 12 placed, 0 declined | spawn → own wools 48 and 41 by `reach`, one block placed | spawn → far wool 130, 8 placed |
| Saltwharf | 10971 · 239 · 588, seven faces | 24 placed, 0 declined | core 46 with a ten-block drop off the headland, beacon 57 with nothing placed | core 116, beacon 133, the sound bridged |
| Hollin Tarn | 16285 · 95 · 222, two faces | 41 placed, 0 declined | 42, nothing placed | 140, the sound bridged |

The plan tier refuses nothing on three of the four. Saltwharf still carries `GO1` (ratio 2.47 against 3.0)
and `GO3` (cores 73 apart against 85): a core on the low ground in front of the spawn on a board this deep
cannot satisfy both, which is the open question at the end.

## What the author said, and what was done about it

**The destroy boards were squares.** They were: every piece a rectangle at one surface, and the only shape on
them the plan's own cells. Each of the three now has its outline pulled per vertex in `editShapes` — the
yard's coast on Ashcombe cracked with six inserts, the terrace's back corners cut off, the head's corners cut
on Hollin — and the pieces themselves are staggered so the frontline is not one line: Ashcombe's yard is four
pieces at four depths, Saltwharf's strand steps out past the quay. The build zone stayed at its width; it is
the ground either side of it that moves.

**Grass and stone met on a straight line.** On Ashcombe the moor and the quarry are no longer split by the
piece boundary. The face is a `scarp` whose `points` wander — in to `z -56` between the two mouths, out to
`z -46` east of them — so the grass comes down to the frontline in one bay and the stone reaches deep into
the bank in the next. The yard is themed as stone (a cell of gravel, andesite and cobblestone over rock,
no dirt under it), the moor as grass over dirt over rock by slope, and the seam between them is the face,
not a line on the plan.

**The tunnel wanted more of a network, and stairs toward the monument.** There are now two mouths in the
face — `(14, -56)` and `(34, -46)` — feeding one tunnel along the back of the bench at `z -70..-65`, and two
stairs up out of it: one west, landing at `(-37, -66)`, one in the middle, landing beside the monument at
`(-5, -48)`. All of it is planned from the rock up: a `below` layer of four rock slabs to 16 and four
override cuts to 12 through them, the bench's floor lifted to 16 over the rock, and the two stairs as
override polygons on the ground layer with `anchor_heights` from 12 to 20 over sixteen cells. The face line
sits one row inside the bench so the mouths open flat onto the yard: `column?at=14,-55` cobblestone at y11,
`?at=14,-56` stone at y16 over air to 12.

**A cliff where the house is, melted in.** The crag on the west bench is a `level` polygon at 34 with a
skirt of eight, so it rises fourteen over the bench and eases into the moor rather than standing on it;
the house sits at its foot.

**Cover that is not boulders, and no stone boulders on stone.** Two low walls of stone brick, two courses
high, stand on the yard and on the bench — `height_mode: raise` rectangles, so they add to whatever ground
they cross. The three boulders are on the moor, on grass; none is on the yard.

**A stair between the grassy and stony ground that reads as structure.** The terrace-to-bench stair is one
override polygon in the `stair` theme, stone brick the whole way, `anchor_heights [20, 20, 26, 26]` over
thirteen rows, standing over the relief's own bevel so the foot lands on the bench at 20 with nothing
between.

**More elevation across the yard.** The yard's west half is an `area` mark at 16 and its east half at 12,
so the pit falls four blocks west to east under the face, and the tunnel mouths open on the low side.

**Hollin's path stops short, and the monument sits on the axis.** The monument moved ten blocks off the axis
to `(-10, -49)`, on its knoll; the track now runs from the lodge door round the west shore to the hut and
on to the build zone, one solid stroke of gravel, andesite and cobblestone; a brook of packed ice runs out of
the tarn's west end to the board's edge as a `level` polyline at 11; a crag at 20 with a skirt of six stands
on the east shore for the height the author asked for. The board is one cell deeper each side than it was,
because with the monument off the axis the walk from its own spawn read 39 against `GO4`'s 40, and pulling it
toward the centre broke `GO1`'s 3.0 the other way — the arithmetic is in the open questions.

**Saltwharf was not liked, and most of it changed.** A second objective: a destroyable of end stone,
`pillar-3`, on the east knoll at `(29, -56)`, so the map is played for two things and `map.xml` carries
`dtm` and `dtc` both. The core stands on a plinth of three stone-brick plates, 13, 15 and 17, so it is a
made thing rather than a block on a floor, and each riser is two courses — a scramble, not a wall. The
houses are a flat-roofed warehouse style built as two wings, a tall one and a lower one, in stone with
chiseled-stone-brick posts, one each side of the quay. The strand is at 10 where the quay is at 12 — a
`strand-floor` mark at 9 with a bevel — so the quay has an edge, and a pier runs out into the sound so the
sea wall is not one line. A road runs from the spawn house down the east flight to the sand. The flora is
denser and the biome is a noise field over plains, forest and birch forest, so the grass tint varies.

**Whinberry was cute and had too many trees.** Two of the three oaks are gone; the one right of the spawn
exit stays. The wool room is three storeys where the spawn is two, so it stands taller.

## Ashcombe Delph — the tunnels, read back

| Read | Answer |
|---|---|
| `column?at=14,-56` | Stone y16 over air y12..15 over Stone y11 — the west mouth |
| `column?at=34,-46` | the east mouth, the same section |
| `column?at=-30,-70` | Stone Bricks y12..16 — the west stair, mid-climb |
| `column?at=-5,-50` | Stone Bricks y14..18 — the middle stair, near its head |
| `walk?from=14,-50&to=14,-67` | 17 blocks, 0 placed — in at the west mouth |
| `walk?from=14,-67&to=-5,-67` | 19 blocks, 0 placed — along the tunnel |
| `walk?from=-5,-66&to=-5,-48` | 18 blocks, 0 placed — up the middle stair |
| `walk?from=34,-40&to=34,-67` | 27 blocks, 0 placed — in at the east mouth |
| `walk?from=0,-100&to=2,-58` | 43 blocks, 0 placed — from the spawn down the terrace stair to the monument |

The walker prefers the face to the tunnel when both reach the same place, because the face is a
three-block wall with a scramble above it and the tunnel is longer; so the table walks the tunnel in
segments rather than asking for a route and hoping.

**Words.** This report says *house* where the first draft said *office*, *tunnel* where it said *adit* or
*gallery*, *mouth* for where a tunnel meets the face, *stair* for a flight, and *step* for what the first
draft called a jog in an outline. The quarry words were exact and were not understood, which is the worse
of the two.

## Whinberry Ring — a composed board taken over

`GET /compose?players=16&symmetry=rot_180` was walked for 24 seeds; seed 18 was pinned for its shape — a ring
hub with a hole, a spawn spur behind, two flank wools at different depths — and its plan is committed beside
the spec as `composed-seed-18.plan.json`. What the composer does not do is what was added: three heights
(the back of the ring and the spawn at 15, the front and the wool approaches at 12, the frontline at 9), a
twin frontline of two prongs with a bay of void between them, a stepping stone on the axis stated once with
`mirrors: false`, a bedrock wall on each wool approach, and the outline reshaped per vertex on the
void-facing edges. The spec computes each `editShapes` op against the compiled ring rather than hard-coding
an index, so the list survives a recompile.

The wool room is `shell([GROUND, LOFT, UPPER])` with beams and a stained-glass-pane door; the spawn is two
storeys of the same family. The one oak is `oak-dense-1` from the tree showcase, carried as a `copied` body.

## Saltwharf — a made thing beside a natural one

The quay is one compiled shape with `relief_scope: exclude` and its own theme: an `inward` stack — a
stone-brick kerb, a ring of `teamTint` clay, a stone-brick checker inside — and a `wallRun` on the sea face
of seven courses of stone brick to two of the team's colour. The headland behind it is the relief-solved
ground; the strand to the east is the same piece two blocks lower and takes the sand. The plinth's plates are
`level` rectangles in the `stair` theme; the two flights are one override polygon each, `anchor_heights
[12, 12, 22, 22]` over twenty cells, cut as slots into the headland's front.

`column?at=-19,-27` Stone Bricks y12 (the first plate) · `?at=29,-56` End Stone y33..35 over grass at y29
(the beacon on its knoll) · `?at=35,-38` Sand y12 over sandstone (the strand) · `walk?from=-32,-70&to=-22,-30`
44 blocks, 0 placed — from the spawn down the west flight to the plinth.

## Hollin Tarn — the tarn is a plate

The plan is two levels — the dale at 12 and the head at 18 — and everything else is the relief: the knoll
the monument stands on is an `area` at 14 with a bevel, the head an `area` at 18 with a bevel of five, and
the two wooded shoulders are `pushes` (`amount 5`, `crown 5`, `falloff 20`). The tarn is a `height_mode:
level` plate at 11 with `skirt 0` and its own theme — a flat plane cut through the field, a one-block shore
all round — with an `area` mark at 12 on its ring grown by a fifth, so the ground round it does not float.
The brook is the same plate drawn as a rough-edged polyline; the crag is a level polygon at 20 with a skirt.

`column?at=0,-26` Packed Ice y10 over gravel · `?at=-10,-49` obsidian y18..20 over the knoll · `?at=30,-20`
Snow Block y19 on the crag · `walk?from=0,-87&to=-9,-19` 72 blocks, 0 placed — the track from the lodge
to the hut · `walk?from=30,-20&to=-10,-49` 52 blocks, 0 placed — off the crag to the monument.

The surface is a `slope` stack under a cold-taiga biome: a cell of snow block with a grass patch in four over
two of dirt on the flat, grass and coarse dirt on the shoulders, rock on the faces. The lodge and the hut are
one style: a stone footing course, spruce planks, a laid spruce-log course the floor beams come out of,
spruce-log posts, a gable roofed in dark oak with a laid-log verge.

## What the driver now does that it did not

`tools/drive.py` carries the finish's `authors` onto the intent's own `meta.authors`. The body of
`POST /map/from-documents` credits the map row, but the observer platform's authors board reads the intent
(`EX6`), and every drive here raised it until that line was added.

## Open questions for the author

- **Saltwharf's bands.** A 150-deep board with the core on the low ground in front of the spawn cannot
  satisfy `GO1` and `GO4` together, and its two cores are 73 apart against `GO3`'s 85. Is the 2.5 ratio a
  fault of the board, or is a core twelve blocks behind the sea wall the kind of board the bands were not
  written for?
- **A goal off the axis costs depth.** With Hollin's monument ten blocks off the axis, the walk from its own
  spawn and the walk from the enemy's sum to the board's depth, and `GO4`'s 40 with `GO1`'s 3.0 need that sum
  to be 160. The board grew ten blocks to get there. Should a goal off the axis be allowed a shorter own
  walk, or is the deeper board the right answer?
- **Ashcombe's face.** The face is a three-block wall with a scramble above it, so a player reaches the
  bench anywhere along it and the walker prefers it to the tunnel. Is that the soft wall wanted, or should
  the face be sheer so the ramp and the tunnels are the only ways up?
