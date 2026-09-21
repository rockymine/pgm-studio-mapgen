# Kilnbrow — one monument, four ways in

A destroy-the-monument board on a red clay firing-ground. Each team's monument stands alone
on an open shelf a short walk forward of its spawn; the two teams' lands never touch.

**The sentence it was authored to:** *a clay firing-ground where the monument stands out on
the open pan, and the ground around it offers four different ways at it rather than one.*

## Where the four approaches are

`docs/gameplay/approaches.md` is the law this board was composed against: an objective sits
exposed, and the ground round it is arranged so the ways in differ in **dimension**, not in
flavour. All four are on the map and each is one instrument.

| Approach | What it is | Where |
|---|---|---|
| from **above** | the spoil hill — climbed for height, bridged from toward the monument | a push, `amount` 8 / `falloff` 10 / `crown` 5, ring x 9…31, z −62…−39 |
| from **below** | the worked clay pit — dropped into, moved through, come up out of | a negative push, `amount` −7 / `falloff` 5 / `crown` 0, ring x −32…−13, z −48…−34 |
| **through** | the kiln row on the bench, fought through room by room | three houses, x −26…34, z −101…−92 |
| **open** | the shelf itself, pinned flat, which is what a goal wants round it | an `area` mark at 15, ring x −33…−8, z −73…−50 |

**The pit is a depression and not a hole, and that is the ruling rather than a preference.**
On a `dtm` board void belongs between the teams; a hole cut in a team's own ground funnels
play into the side channels and empties the ground the contest was meant to happen on. The
two lands here are joined by a build zone spanning the whole width over 40 blocks of void,
and there is no land connection anywhere.

## Where the monument stands, and why it is off the axis

Block **(−20, −70)**: 63 blocks from its own spawn by walk and 196 from the enemy's, a ratio
of **3.11** inside `GO1`'s 3–4 band, with the opposing pair 143 apart inside `GO3`'s.

**It sits twenty blocks off the centre line, and that is what makes the board's flanks
ground somebody crosses.** On the axis the same board read **44.6% dead**; moved out, it
reads **6.0%**. Nothing refuses a board for dead ground and `GET …/coverage` is the only
read that asks, which is exactly why it went unrun for three iterations here.

## What the ground is made of

Three themes, and each is a place: `moor` the firing-ground (61.7%), `works` the kiln bench
(35.4%), `pit` the worked clay floor (2.9%). Nothing is registered that painted nothing.

**The surface is banded on the `slope` axis, cut against this board's own `incline`.** 55.3%
of the ground stands under 10° and 10.1% at 40° or steeper, so the turf runs to 30°, the
worked shoulder to 50°, and bare red clay shows only on a genuine face. Cut at 20° instead —
which is where it was first written — the shoulder band swallowed the whole middle of the
pan and the board came out a brown sheet: a hill's gentle skirt is a flank by angle and a
meadow by eye.

**The ground family is warm.** Grass and coarse dirt over hardened clay, on a **Mesa** biome
(`#90814d`), where the grass tint comes to meet the clay instead of arguing with it. The
built family is pale sandstone, which is not the family under its feet, and the accent is
dark oak.

## Where made ground meets grown ground

The kiln bench is `relief_scope: "exclude"`, so it keeps the height it was drawn at and meets
the pan at an eight-block face rather than being graded into it. Two flights state that face
— sixteen blocks of run for eight of rise, `height_mode: "level"`, `skirt: 0`, `keepClear`,
and a **material** rather than a theme, because a stair is a thing somebody built and reads
as one stone the whole way up.

**`EL1` complains about that seam and is right about the plan and wrong about the board.**
The plan tier walks the pieces flat and cannot see an authored flight at all. The transect
through the west flight, x −27 from z −95 to −66:

```
rises 2, falls 5, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
```

## The numbers

| Read | Answer |
|---|---|
| `03-slopes.txt` | 12 298 walked · 574 scrambled · 528 barrier; 18 faces, largest 132 at x 1…34, z −107…−102 |
| `06-claims.txt` | **28 placed, 0 declined** |
| `GET …/coverage` | reached 12 170 · decorated 429 · dead 801 of 13 400 = **6.0% dead** |
| `POST …/sketch/relief/read` | group `team`: 4 200 cells, 5…26, relief 21, symmetry error 0 |
| `GET …/preflight` | **export gate OPEN**, per team |

## What went wrong

**The board was three times too long for its own buildings before `DR-PASS` said so.** A
building wants eight blocks of passable ground on a side and is seven deep itself, which is
23; the bench was 20. No amount of moving the row fixes that arithmetic, and the answer was
to deepen the bench to 30 rather than to shuffle houses.

**Two props were placed by eye and both were wrong.** A boulder on 56° ground came back
`DR-STEEP` *and* `DR-CUT` with half its body buried; a tree three blocks off a claimed road
came back `DR-ROAD`. `POST …/sketch/seats` answers where a kind may stand **forwards**, over
the whole board, and it was not run until the third pass.

**A patch drawn one course short of the ground under it paints nothing and says nothing.**
The pit floor was first written at `base_height` 7 against a landmass of 12. It builds, it
looks plausible, and `themes/census` is the only witness.

## One standing complaint, accepted

`SK27` reads the bench and the pan as one component carrying two paints with a hard line at
the riser. That line is the retaining face, it is the thing the board is composed around, and
it carries its own `wallRun` — so the complaint is noted rather than answered.

## Coordinates

| Thing | At |
|---|---|
| monument (red) | (−20, −70) |
| monument (blue) | (20, 70) |
| spawn (red) | (0, −115), door +z |
| spoil hill crest | ≈ (20, −50) |
| clay pit floor | ≈ (−22, −41) |
| kiln row | x −26…34, z −101…−92 |
| west flight | x −31…−23, z −88…−72 |
| east flight | x 13…21, z −88…−72 |
| build zone over void | x −35…35, z −20…20 |
