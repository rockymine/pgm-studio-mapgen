# Peatgarth — every edge on the board is a cut somebody made

> A destroy-the-monument board on a worked peat moss. Each team's Peat Store stands on a stripped
> bench with a face on three sides and a tramway ramp up the fourth.

**In one sentence:** attacking this board is choosing which of four ways onto a cut bench you take —
the open moor from the front, the tramway ramp up its south face, a flooded cutting on the east flank
that arrives below the monument, or the knott on the east front that arrives above it.

80 × 200 blocks, `rot_180`, four pieces at two surfaces, maxPlayers 20, ground y10..y23, observer y56.

## The arrangement

Four pieces, and only two surfaces between them: `fore` and `garth` at 13, `stage` and `staith` at 14.
The board's shape is therefore the relief's and not the piece list's — the plan states where the
ground is and nothing about what it looks like. A 20-block void seam runs the full width at z ±10 and
the `pass` build zone bridges it, so the crossing is a decision.

The relief is four `area` marks and two `push`es, and each does something only it can. `moor-flat` and
`back-flat` are the two flats a player fights on; `hag-e` is the flooded cutting east of the bench and
`hag-w` a dry peat hag on the west front, both stated as marks because a hag is ground and not a
structure. The `knott` push raises the east front six blocks over the moor — `amount / falloff` 0.33
against `crown` over the ring's half-width 0.33, which is the agreement `RL6` reads — and `rigg` puts
a low swell on the west so the moor is not one plane.

The bench itself is **not** a mark. It is a shape carrying `relief_scope: "exclude"`, which takes its
footprint out of the solve, so the moor and the bench top meet at a face rather than the relief ramping
one up to the other. That face is the whole point of a cut peat bench — and it carries the **`works`
theme**, so the surface, the face and the andesite ramp up it all say the same thing. A raised disk
painted in the moor's own theme reads as more moor with a cut edge round it, which is not what a
stripped bench is. `column (−24, 48)` reads andesite over stone; `column (−6, 60)` polished andesite
over stone over cobble.

Only the scald on top of it is soil: `bench-scald` carries the `cutting` theme, which is the cut peat
spread on the stage to dry.

## What the reads say

| read | number |
|---|---|
| `03-slopes.txt` | 11 790 walked · 74 scrambled · **296 barrier**; 4 faces, largest 142 at x −1..27, z −69..−43 |
| `06-claims.txt` | **placed 30, declined 0** |
| relief read | level **0.431**, largestField **0.167**, 0 seams, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **25.3 % dead**, 10 journeys; largest patches 691 cells at (−32, 33) and 689 at (30, −35), both **1 block** from used ground |
| `GET …/incline` | 41.3 % under 10° · 30 % teens · 17.3 % twenties · 6.7 % thirties · 4.7 % at 40°+ |
| `05-themes.txt` | moss 91.4 % · works 5.7 % · cutting 2.9 % |

## Against the fault catalogue

**Objective hidden — no.** `column (−12, 52)` reads ground at y18, the goal at y23–25, and nothing
between it and the sky marker at y54. The four-block float is PGM's own convention and is what keeps a
destroyable off the ground where it would be trivially covered.

**The goal is a `cube-3` in ender stone** — the author's call, about how it plays: this goal stands
40–42 blocks from its own door with 11 blocks of lateral offset, and a `pillar-3` is three blocks of
obsidian at that range. A cube is 3 × 3 × 3 with the studio's own 1 × 1 × 1 bedrock centre, so **26
breakable blocks**; `column` at the corners reads solid end stone y23–25 and at the middle end stone,
bedrock, end stone. The material follows the size rather than the palette: `DC3` reads obsidian as
worth at most three blocks and names ender stone, gold or emerald for a cube, and a cube declared
obsidian is built in ender stone anyway with a complaint attached. Declaring it is the honest form.

**Spawn faces away — no.** Red spawns at (0, 92) with yaw 180; the bearing from there to the enemy
store at (11, −53) is 176°. Four degrees.

**Spawn faces a wall — no.** The spawn transect along z reads rises 0, falls 4, worst step 1, 0 barrier,
0 scramble, walked end to end.

**Stairs that end nowhere — no.** The tramway ramp is stated as a flight (`height_mode: "level"`,
`anchor_heights` 14 → 19, `skirt: 0`, a material rather than a theme) and runs 14 blocks for a rise of
5, which is nearly three times the rise.

**A straight frontline — no.** The `fore-13` ring is bent (`k` 0.24, wander 4, step 8), so the front is
drawn rather than left over from a rectangle's edge.

**Flat, one theme, empty — the one open question on this board.** The coverage is the good pattern:
25.3 % dead in four flank corners, every one of them a block from used ground, which is Glassmere's
shape and not Ruddle Brink's. The relief's `level` of 0.431 is well clear of `RL5`'s 0.30 bar and the
incline distribution has no spike in it. **The theme census is 91.4 % one theme**, and the moor's
theme is carried on the **slope** axis — its flat, its shoulder and its rock face are three different
stacks of one theme, so the top-down is a map of the board's own angle rather than a flat sheet. That
is the Glassmere case rather than the Ruddle Brink one. Giving the bench the `works` theme doubled the
stone on the ground (2.9 % → 5.7 %) and put it where a player fights rather than behind the spawn.

## The two buildings at the head of the tramway

There is no stone pad behind the spawn any more. It was an 11 × 16 slab carrying one house, hard
against the spawn's own footprint, which made a flat stone rectangle that was not a place and put two
different house styles eleven blocks apart. The ground there was already flat under `back-flat`, so
the pad is gone — `column (−22, 86)` now reads podzol over dirt — and the store is rebuilt in the
**spawn's own shell** at x −30..−20, z 70..82, matched in storey heights (clear 5 then 4 under a gable)
so the two buildings read as one family. It seats clear of the spawn door's approach, which declined
it at (−26, 86) on the first try.

## Limits

- The relief read answers 0 faces and 0 cliffs while the built world carries 296 barrier cells in four
  faces. Both are right: the bench is an `exclude` shape and stands outside the relief solve, so the
  face it makes is terrain the relief never claimed. Read `03-slopes.txt` for the board's steps, not
  the relief read.
- Trees here are `template` spruce rather than copied bodies, which is the one place this board is
  behind the other three in its set.
