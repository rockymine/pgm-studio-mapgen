# Six generator boards at 32 players, as grids

`GET /api/compose?players=32&teams=2&symmetry=rot_180&count=6`, seeds 0–5, pinned to plans and rendered
with `tools/board.py`. The plans are beside each grid. These are here as **examples**, which is the thing a
hand-authoring agent has least of: the composer states the board vocabulary in the same cell rectangles a
hand-written plan uses, so its output is the reference for what a plan of this size is supposed to look like.

| seed | hub | frontline | wools | enclosed void cells |
|---|---|---|---|---|
| 0 | ring | twin | i + i | 20 |
| 1 | bar | single | l + l | 0 |
| 2 | double-hole | bar | i + i | 20 |
| 3 | ring | bar | i + l | 6 |
| 4 | double-hole | single | i + i | 8 |
| 5 | ring | bar | i + i | 12 |

## Holes are the normal case, not an exotic one

**Five of six carry an enclosed void, and the census says that is the mix.** Over 400 boards at
`players=32`, `rot_180`:

| | |
|---|---|
| hubs | ring 54% · bar 22% · double-hole 10% · twin 7% · G 3% · P 3% · single 2% |
| frontlines | bar 48% · single 20% · **twin 19%** · none 13% |
| wool approaches | I 92% · L 36% · **donut 10%** · U 2% · H 2% · clamp 1% |

`ring` and `double-hole` alone are **63% of hubs**, and both are bodies with a hole in them. Add `P` and `G`
and it is 70%. A `donut` wool approach rings a void of its own, and a `twin` frontline is two legs with a
void between them. And the shape library agrees: of its 98 cards, **73 are donuts**, and four of the six hub
shapes enclose something.

**A hole in a plan is made by arrangement, never by subtraction.** Pieces ring a gap and no piece covers it;
`PlanVoids.Declare` then names every such gap a `void-N` buffer on *every* compile, whether or not anyone
drew one. A `buffer` piece drawn over a generating piece is inert by design — it can declare a void but
never destroy ground — so the way to get a hole is to leave one, not to cut one.

Seed 0's hub is the worked example. Four pieces ring a two-cell gap:

```
   7 |      BBBBBBBBIIJJ|     B  hub-t2   x -3..5
   9 |      CCCCooDD    |     C  hub-t3   x -3..1
  10 |   FFECCCCooDD    |     D  hub-t4   x  3..5
  11 |   FFEAAAAAAAA    |     A  hub-t1   x -3..5
                              oo         the ring's hole, x 1..3
```

and its frontline is the same idea at the entrance:

```
   2 |      LLoooMM     |     L, M  the two legs of a twin frontline
   4 |      KKKKKKKK    |     ooo    the void between them
```

## What the void is for, in the author's own measurements

`docs/gameplay/match-flow.md` §3.2 names three positions and says what each buys:

- **At the entrance** — the legs of a two-legged frontline and the mid band enclose a void, so the crossing
  forks before an attacker has touched the defender's land. **97%** of objectives behind a two-legged
  frontline have more than one attack route, against **38%** behind a plain bar.
- **In the middle** — a hub that encloses a void offers two ways across when its doors straddle the hole.
  Ring hubs deliver that on 163 of 224 spawn-to-wool crossings and 203 of 209 wool-to-wool rotations.
  *Solid and branched hubs never do.* §4.9 prices it: the far way round covers **37%** of the defender's
  reinforcement lane against **76%** for the short way, and reduces the collision on 74% of boards offering
  the choice.
- **At the objective** — the bay of a U, H or clamp approach is the same mechanism a third time.

And the sentence that indicts a solid middle outright: *"A large rectangular hub spreads players out without
giving them a choice, and over a long match that degenerates into push and pull along one shortest line."*

## The other thing these six say

**Not one of them puts a neutral stepping stone in the middle.** In all six the middle is void crossed by a
build band, and the band's width matches the frontline it serves — identical in three, within a cell in two.
`opus5-wheal-hazel`'s bar was invented, and then sized to nothing (`GENERATION-NOTES.md` §18): a mid piece
80 blocks wide against a 20-block band, 60% of it dead.
