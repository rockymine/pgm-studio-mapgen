# Fable 5.1 — four boards to the author's brief

Four maps, each authored from one sentence, built through `tools/drive.py` and read back through the
API before any picture was opened. The brief this run was held to is the author's spoken one: think first,
keep each board simple, one ground and a handful of patches, few houses of one family, no grown trees, paths
solid and in three near colours, terrain as layers, the ground finished by its angle, and one attempt at an
underground passage planned bottom-up.

| Folder | Mode | The sentence |
|---|---|---|
| `fable-ashcombe-delph` | dtm | a worked quarry on a moor: the monument on the bench above the face, the loading yard below it, and an adit through the face that comes up a flight beside the monument |
| `fable-whinberry-ring` | ctw | composer seed 18 at sixteen players, taken over: three levels, a twin frontline with a bay, a stepping stone on the axis, a defence wall on each wool approach, and the outline pulled into heath by hand |
| `fable-saltwharf` | dtc | a stone quay under a grass headland: the core out on the quay in the open, a warehouse either side, the spawn ten blocks up behind it, two stone flights and a sandy bank down |
| `fable-hollin-tarn` | dtm | a snowed valley head: the monument on a green knoll behind a frozen tarn, spruce shoulders either side, the lodge at the head |

Every board exports with the gate OPEN and nothing declined. Each `specs/<slug>/build-spec.py` writes the
plan and the finish; the driver writes the rest.

## The numbers, before the pictures

| Board | 03-slopes (walked · scrambled · barrier) | 06-claims | own → goal | enemy → goal |
|---|---|---|---|---|
| Ashcombe Delph | 17104 · 408 · 488, six faces | 28 placed, 0 declined | 40 (plan) — the built walk runs the terrace road and the haul ramp | 147 (plan), ratio 3.7 |
| Whinberry Ring | 4126 · 0 · 0 | 16 placed, 0 declined | spawn → own wools 48 and 41 by `reach`, one block placed | spawn → far wool 130, 8 placed |
| Saltwharf | 12376 · 60 · 564, four faces | 22 placed, 0 declined | 46, no block placed, one 10-block drop | 106 by `travel` (20 bridged) · 167 by `reach` (11 placed) |
| Hollin Tarn | 15942 · 58 · 0, no face | 39 placed, 0 declined | 38, nothing placed | 177 by `reach`, 14 placed (the sound bridged and the far knoll) — 127 at the plan tier, ratio 3.2 |

## Ashcombe Delph — the adit

The board is three plan pieces per half at three surfaces — yard 12, bench 20, terrace 26 — and a build zone
over twenty blocks of void between the halves. The face between yard and bench is a `scarp` (`high 20`,
`low 12`, `face 3`), so the yard-to-bench step is a five-block wall: not crossed in a fight, climbed with
blocks, walked round by the haul ramp at the west end (a `line` mark, `r 4`, `tread 1`), or gone under.

**The adit is what the brief asked for, and it is built bottom-up.** The bench shape's floor is lifted to 16
(`shapePropsById`), and a `below` layer carries the rock under it as three `add` bands round a corridor
five wide: rock to 16, the corridor slab to 12. The corridor floor is therefore the yard's own level, its
headroom is the four courses between 12 and the bench's floor, and its mouth is simply where the corridor
meets the face — the bench's column above it is one course thick there, which is the lintel. At the far end
an override-add flight on the ground layer (`floor 12`, anchors 1 → 8 over sixteen cells, `keepClear`)
opens a slot up through the bench and lands twenty blocks east of the monument.

| Read | Answer |
|---|---|
| `column?at=20,-31` | Andesite y16 over air y12..15 over Gravel y11 — the mouth |
| `column?at=20,-45` | Grass y19, Dirt, Dirt, Andesite y16, air, Gravel y11 — the tunnel under the bench |
| `column?at=20,-56` | Stone Bricks y15..12 — the flight, mid-climb |
| `walk?from=20,-20&to=20,-66&aim=travel` | **46 blocks, 0 placed** — yard to bench through the adit |
| `walk?from=0,-15&to=0,-52&aim=reach` | 77 blocks, 0 placed — round by the ramp |
| `walk?from=0,-15&to=0,-52&aim=travel` | 37 blocks, 5 placed — straight up the face |

Three ways in, at three prices, which is the composition `approaches.md` asks for: around, above, below.

**Two things went wrong on the way.** The scarp's `points` were first written west to east, which put the
shelf on the *yard* side — the yard came out at 20 and the bench at 12, `RL3` named an eight-block seam
along 94 cells at `(-50, -37)`, and the route walk reported `barrier +3 at (0, 36)`. The high band is on the
+z hand of the drawn direction (`GENERATION-NOTES.md`, *A scarp's shelf*), so the line is drawn east to
west. And the face's line sat on the yard's last row, so the toe of the cliff was a two-block lip the tunnel
walk had to place a block on; moving the line one block into the bench put the whole face in the bank and
the walk dropped to nothing placed.

The office stood across the road on the first build (`DR-CROSS`) and was moved off it rather than the road
being redrawn round it; a spruce stood on the office's own ring on the second (`DR-CLAIM`).

## Whinberry Ring — a composed board taken over

`GET /compose?players=16&symmetry=rot_180` was walked for 24 seeds; seed 18 was pinned for its shape — a ring
hub with a hole, a spawn spur behind, two flank wools at different depths — and its plan is committed beside
the spec as `composed-seed-18.plan.json`. What the composer does not do is what was added:

- **Heights.** The back half of the ring and the spawn at 15, the front half and both wool approaches at 12,
  the frontline at 9. The compile then emits one shape per level, which is what makes the tiers paintable
  and reshapeable one at a time.
- **A twin frontline.** The composer's 4 × 4 block became two prongs ten wide with a fifteen-deep bay of void
  between them, open to the mid, so the landing is two places rather than one.
- **A stepping stone on the axis**, a piece stated once with `mirrors: false`, ten blocks off each prong
  (`G5` refused a five-block hop; the mid zone had to grow to the prongs' full width or `FR9` read them as
  five-block funnels — it still reads a ten-block prong as under its fifteen, and that is the twin form).
- **Two defence walls**, one per wool approach, each on a single ten-block interface (`ST8` complained about
  a wall split across two five-block seams, so the wool-a approach was moved so that it touches one hub
  piece only).
- **The outline reshaped per vertex, not bent.** `editShapes` inserts twenty points on the void-facing
  edges — the wool verges, the prong flanks, the spawn spur — and none on a seam or beside a wall. The
  spec computes each op against the compiled ring rather than hard-coding an index, so the list survives a
  recompile.

The wool-a approach came out at 15 on the first build: with `reach 0` an unpinned region beside a pinned
terrace is a plateau at the terrace's height, not a fall to base. An `area` mark at 12 with a bevel
pinned it, and the wall now stands on the 15/12 seam — bedrock to 17, cobweb at 18, two courses over the
terrace and five over the lea. The hub's grade was then too short (six blocks over eight cells reads as a
37° shoulder and paints coarse dirt), so the terrace mark stops at z 45 and the front mark at z 26 and the
hub falls at 17°, which is grass.

The oaks are the author's own — `oak-dense-1`, `-3` and `-4` from the tree showcase, carried as `copied`
bodies in `dressing.styles`, three a half.

## Saltwharf — a made thing beside a natural one

The quay is one compiled shape with `relief_scope: exclude` and its own theme; the headland behind it is
the relief-solved ground; the strand to the east is a third shape at 13 so it compiles apart from the quay
and takes the sand. Where the quay meets the headland the seam is a ten-block face; where the strand does,
it is a graded bank. The quay's paint is what the brief asked a structural area for: an `inward` stack —
a stone-brick kerb, a ring of `teamTint` clay, a stone-brick checker inside — and a `wallRun` on the sea
face of seven courses of stone brick to two of the team's colour.

The two flights are one override polygon each, `anchor_heights [12, 12, 22, 22]` over twenty cells, cut
as slots into the headland's front and landing flush: `column?at=-32,-59` reads stone bricks at y20 and
`?at=-32,-61` gravel at y21.

**The goal bands do not meet on this board, and that is recorded rather than hidden.** The defender's walk
to the core is 46 blocks and takes the ten-block drop off the headland rather than either flight; the
attacker's is 106 with the twenty-block sound bridged. `GO1` wants 3.0–4.0 and reads 2.3; `GO4` wants at least
40 and reads 46; `GO3` reads 63 at the plan tier against 85. With the spawns about 150 apart by walk, a
goal 40 from its own spawn is at most 2.8 from the enemy's — the same arithmetic `reports/opus5-weirbank-run.md`
found — and the only cure is a deeper board, which on a quay is dead ground. The core stayed twelve blocks
behind the sea wall, where the bridges land, because that exposure is the board.

An oak was declined on the first build for standing in a door's approach nobody had drawn: a spawn piece
abutting board on three sides opens on two of them, and the second door here is the west wall.

## Hollin Tarn — the tarn is a plate

The plan is two levels — the dale at 12 and the head at 18 — and everything else is the relief: the knoll
the monument stands on is an `area` at 14 with a bevel, the head an `area` at 18 with a bevel of five, and
the two wooded shoulders are `pushes` (`amount 5`, `crown 5`, `falloff 20`; at `falloff 10` and `crown 4`
`RL6` named the skirt 2.5× steeper than the crown, a step at the push's own outline).

The frozen tarn took four tries, and the record is worth keeping. A one-course `add` carrying the ice
theme painted nothing: paint follows the shape that forms the surface, and a one-course patch does not
reach it. A `relief_scope: hold` plate at 11 cut the pan and still painted snow, because the dale shape
stated at 12 still reached the top in the owner test. A **`height_mode: level` plate** at 11 with `skirt 0`
is what a tarn is: a flat plane cut through the field, a one-block shore all round, and its own theme,
since a shape with a height mode is a candidate at its stated height. It still needs the field told:
a level plate is out of the solve, so the ground round it floated to 15 and the walk in off the sound read
`barrier +4`. An `area` mark at 12 on the plate's ring grown by a fifth, with a bevel of three, is the flat
shore the ice is set into — `column?at=0,-14` snow at y11, `?at=0,-26` packed ice at y10, `?at=0,-46` grass
at y13 on the knoll, and `walk?from=0,-12&to=0,-44` 32 blocks with nothing placed. Packed ice over gravel,
so it does not melt.

The surface is a `slope` stack under a cold-taiga biome (`{"kind": "solid", "id": 30}`): a cell of snow
block with a grass patch in four over two of dirt on the flat, grass and coarse dirt on the shoulders, rock
on the faces. The trees are `fir-tall-5`, `-6`, `-7` and `fir-small-1`, `-4` from the showcase — seven a
half on the shoulders and two behind the lodge, none nearer than 26 blocks to the monument. The lodge and
the hut on the west shore are one style: a stone footing course, spruce planks, a laid spruce-log course
the floor beams come out of, spruce-log posts, a gable roofed in dark oak with a laid-log verge.

## What the driver now does that it did not

`tools/drive.py` carries the finish's `authors` onto the intent's own `meta.authors`. The body of
`POST /map/from-documents` credits the map row, but the observer platform's authors board reads the intent
(`EX6`), and every drive here raised it until that line was added.

## Open questions for the author

- **Saltwharf's ratio.** A 150-deep board with the goal on the low ground in front of the spawn cannot
  satisfy `GO1` and `GO4` together. Is the 2.3 ratio a fault of the board, or is a core twelve blocks
  behind the sea wall the kind of board the bands were not written for?
- **Ashcombe's face.** The quarry face is a five-block wall with a two-block shoulder above it, so a player
  with a block reaches the bench anywhere along it. Is that the soft wall wanted, or should the face be
  sheer to 20 so the ramp and the adit are the only ways?
- **The composer's twin prong.** `FR9` reads a ten-block prong as a funnel. The composer's own `twin`
  frontline is two prongs; is ten the width a twin should have, or should the bay be narrower and the
  prongs fifteen?
