# Revetment — a composed hillfort, and the six courses it is played over

**In one sentence:** the fort is made ground and the field in front of it is grown ground, and the
six-course revetment between them is the board.

Composed from `GET /api/compose?players=30&symmetry=rot_180&seed=2` — hub `double-hole`, frontline
`bar`, wools `i`/`i`, card score 0.278, 118 land cells, 100 × 170 blocks. The adapted plan is the
same size and evaluates at **score 0, valid**, against the card's 0.278.

## What the composer gave, and what was done with it

| the composer's | what shipped |
|---|---|
| twelve flat pieces at `globals.surface` 9 | two tiers stated per piece: the meadow at 11, the fort platform at 17 |
| a `double-hole` hub with two holes in it | the holes are kept and railed: two wells in the fort's floor |
| a spawn hung off the hub's west flank | the spawn moved to the fort's back centre, on the board's own axis |
| two `i` wools, one deep and one on the flank | two walled wards, one on each shoulder, equidistant by construction |
| `"walls": []` | four bedrock curtains, two per ward, leaving the middle seam of each open as its gate |
| a 6-cell frontline | a 10-cell meadow, and the only ground the relief touches |

**The spawn is what fixes the lopsided wool, and the reason is geometry rather than taste.** The
composer hangs the spawn off one flank of the hub. With a flank spawn, the set of points equidistant
from a team's own spawn *and* from the attacking one is the perpendicular bisector of the line
between the two spawns, and for a flank spawn that line runs diagonally and its bisector leaves the
half. So the two readings pull against each other and the composer resolves the tension in favour of
defence: `WL9`'s band holds and the attack ratio drifts. Put the spawn on the axis and both readings
are 1.000 by construction. Measured, off `GET …/plan/flow`:

| | composed (seed 2) | Revetment |
|---|---|---|
| attacker's walk, wool-a / wool-b | 153 / 138 blocks | **152 / 149** |
| attack ratio | 1.11 | **1.02** |
| defender's walk | 66 / 84 | **46 / 48** |
| defence ratio | 1.27 | **1.04** |

The plan is symmetric about `x = 0` because that is what the balance needs. **The board is not**, and
that is done downstream: the two wells are different sizes, the bastion sits off centre, the two
flights are cut at different places, one ward carries its tower north of its gate and the other
south, and the relief in the meadow is asymmetric.

## How it is meant to play

An attacker bridges the 50-block crossing and lands on the meadow, which is 60 × 25 blocks of ground
with a low knowe across it, a bench at the east end and two hollows at the wall's foot where nobody
on the parapet can see down. In front is a seventy-block wall six courses tall, painted as a battered
revetment — a `wallDiagonal` whose stripes shear by height, one of them a `teamTint`, so a player
reads whose fort they are under from the far bank. Two stairs are cut into it, each set in a
re-entrant sized to exactly the flight that fills it, and a bastion is pushed six blocks out over the
meadow between them so the ground in front of both is enfiladed.

Over the wall the fort is one platform with two shafts in it. Each wool stands in a walled ward on a
shoulder, and each ward faces the fort along three seams of which two carry bedrock and one is left
open. That open seam is the gate, and it is the only walk into either wool.

## The techniques, and what each one bought

**Per-piece `surface` is what makes a composed board paintable.** A flat composed plan compiles to
one merged polygon and a subtract; stating a height per piece ends the merge and gives one polygon
per height to key a theme on. Two heights here, two polygons, two themes, and the subtracts are the
two wells.

**`relief_scope: "exclude"` on the fort.** The whole platform is taken out of the solve, so the
grown ground arrives at it rather than being graded into it, and the six-course face is a face.
`hold` would have brought the meadow up to meet it and there would be nothing for a stair to do.

**Fifteen made layers, and every one of them is circles and rectangles.** Four runs of crenellated
parapet along the lip with the two stair mouths left open, a breastwork on the bastion, two drum
towers flanking the west stair, a tapered turret over the east one, one drum tower inside each ward
gate, and eight bars of rail round the two wells. All `kind: "made"` with `part_of: "revetment"`, so
`SK10`'s pair walk and `SK11`'s reachability walk leave them alone.

**A rail is drawn as the complement of the shaft.** `SK13` reads the compiled subtract as the
board's negative space and refuses any add that fills it, so the well rails are four bars standing on
the land round each well rather than a ring over it.

**The ground is finished by its angle.** One `layered` stack on the `slope` axis carries the
meadow's turf under 14°, its coarse shoulder to 28° and its sandstone face above that. `incline`
reads 81% of the board under 10° and 3.3% at 40° or steeper, which is a fort board: the flat is the
fort and the steep is its own wall.

**Numbers.** `preflight` ends `export gate OPEN`. `coverage` is 8200 reached, **0.0% dead**.
`03-slopes.txt`: 7052 walked, 94 scrambled, 172 barrier, 8 faces, the largest 61 cells — that run is
the revetment. The relief read: `level` 0.325, `largestField` 0.055, range 4 over 1030 cells,
`faceCount` 0, `symmetryError` 0, three seams all of step 2. Themes: revet 54.1%, lea 28.1%,
garth 17.8%.

## What went wrong

**A push on a meadow this narrow puts a pit at a stair's foot.** A push is applied after every
constraint, so the first `knowe` — ring 14, falloff 9, centred (−4, 25) — lifted the ground beside
the west stair to 15 while the flight's own anchor held its first tread at 11. The transect at
(−13, 27) read `DROP −4`. Nothing else on the board reported it: the flight walked end to end, the
gate was open, the relief read had no seam. The fix was arithmetic — the ring plus the falloff has to
clear the foot — and the knowe now sits at (0, 15) with ring 11 and falloff 8, 18.4 blocks from the
nearer tread.

**A board with no push is a table and a board with a big one is a ramp.** With marks alone the
meadow read `level` 0.679 and `largestField` 0.514; with the first push it read 0.287 and `RL5` fired
at the 30% bar. The third try — amount 2, falloff 8, crown 2, so the skirt and the crown climb at
0.25 and 0.22 — reads 0.325.

**Five made things were stamped through the bedrock curtains.** `SK18` named each pair with its
first column: the parapet, a drum tower and its crown all shared courses with the wall at x −26..−24.
Neither pass reads the other. The runs now stop short of those columns, which is also the honest
reading — the bedrock *is* the parapet where it stands.

**The fort had no room for a house.** `POST …/sketch/seats?kind=house&width=7&depth=5` answered two
seats on the whole platform and neither survived the towers. The one building on the board is
therefore a timber byre out on the meadow, which is cover halfway across the ground an assault has
to cross — the only reason to put a building there.

## Standing complaints, and why they stand

- **`EL1` ×2**, `hub-t2`–`frontline-t1` and `hub-t6`–`frontline-t1`, six blocks. The plan tier walks
  pieces flat and cannot see an authored flight. Both crossings measure `rises 8, falls 0, worst
  step 2, 0 barrier, walked end to end` on a transect at x −13 and x 19; the only step-2 is the well
  rail at the stair head, which is a parapet and is meant to be climbed over.
- **`SK27`**: the component compiles to two plateaus stating two paints. The rule's own sentence is
  that a theme is a place and the change belongs "where a player crosses from one part of the map to
  another". On this board that line is the revetment, which is the one thing the map is about. The
  alternative the rule offers — two components — would put a ditch between the meadow and the wall
  and take the strait outside `CT12`'s band.
- **`RL4`** ×2: the compiler's own wool-room pads pin no cell, because the ground they would pin is
  inside the excluded fort and is already flat at 17.

## Coordinates

| thing | at |
|---|---|
| the revetment's face | z = 35, x −35..35, six courses |
| west stair | x −18..−8, z 26..39, 11 → 17 |
| east stair | x 14..24, z 26..39, 11 → 17 |
| the bastion | x −6..6, out to z 29 |
| west well | x −15..0, z 45..55 |
| east well | x 10..20, z 45..55 |
| west ward gate (open seam) | x = −25, z 45..55 |
| east ward gate (open seam) | x = 25, z 45..55 |
| bedrock curtains | x ±(24..26), z 35..45 and 55..65 |
| spawn | x −10..10, z 75..85 |
| wools | (−40, 50) and (40, 50) |
