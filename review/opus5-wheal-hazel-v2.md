# Wheal Hazel v2 — the same works, rebuilt around what the ground is for

**In one sentence:** the v1 board with three of its measurements taken seriously — a neutral bar no wider
than the window that reaches it, a front of two legs with a bay between them, and a second wool at the end
of each spur so a team has two ways out and two things to fetch.

140 × 180 blocks, `rot_180` about the origin, base surface 9, build ceiling 34, ground y 6..14.
Two islands: `team` (5 348 cells, y6..14, symmetry error 0) and `neutral`, the bar (528 cells, y9..11).

**This does not replace `opus5-wheal-hazel`.** v1 stays as it shipped, because it is the evidence for the
measurement that produced v2.

## What was wrong with v1, in one number

Coverage read v1 at **33.4% dead ground**, and 488 of its bar's 811 cells — **60.2%** — were ground no
journey reaches. The bar ran `x −40..40` and the build zone that crossed it ran `x −10..10`: every journey
over the bar was a bridge through a twenty-block window, so the corridor claimed that window plus its
six-block margin and nothing else. The overhang was thirty blocks a side and the margin bought back six.

Nothing in the pipeline said so, because every gate the board passed — `CT12` on the strait, traversability,
the goal ratios — asks whether ground is *reachable*. Coverage is the only read that asks whether a journey
goes there, and no driver called it.

## The three moves

**The bar is now exactly as wide as the build zone.** `x −25..25` against a build zone of `x −25..25`. A
mid-board stepping stone is used across the width of the window that reaches it and not one block further,
so the honest size for it is that width.

**The front is two legs with a bay between them.** The two shapes that carry the works — one holding the
stream, one holding the depression the floor was cut into — moved so their *outer* edges sit on the bar's
outer edges, leaving a void bay between them centred on `x = 0`. Each was then pushed back ten blocks with
the rest of the team's ground and extruded ten blocks back toward the middle, so they stand proud of the
body as two legs. One build zone spans both leg fronts, which is what turns one mouth into two.

**Each team has two wools, one at the end of each spur.** v1's board was too large for a single wool. The
west spur — the arm that carried the wheel house and nothing else — was pushed further out and capped with
a wool room, and the east side was rebuilt to match at the same distance from spawn. Leg west leads to one,
leg east to the other.

## The board, in the units it is written in

`tools/board.py` renders a plan's cell rectangles as a grid. The whole of v1's defect is one line of it —
`M`, the bar, is sixteen cells wide; `N`, the build zone under it, is four:

```
  -1 |    MMMMMMMMMMMMMMMM    |        v1
   0 |    MMMMMMMMMMMMMMMM    |
   1 |          NNNN    OOOO  |
```

and v2's answer is the same two rows agreeing:

```
  -1 |         AAAAAAAAAA         |   v2 — A the bar
   0 |         AAAAAAAAAA         |
   1 |         PPPPPPPPPP         |   P the build zone, the same ten cells
```

The full grids are `renders/00-board.txt` in each map's folder. Reading a board as a picture is what let the
v1 mismatch survive: a render makes a long bar look handsome, and a grid puts its width directly above the
width of the thing that reaches it.

## What it measures

| | v1 | v2 |
|---|---|---|
| ground cells | 9 798 | 11 276 |
| dead share | **33.4%** | **11.3%** |
| dead on the bar | **60.2%** (488 of 811) | **29.2%** (149 of 511) |
| wools per team | 1 | 2 |
| frontline runs per team | 1 × 20 blocks | **2 × 15 blocks** |
| traversability | 1 component, 0 isolated | 1 component, 0 isolated |
| preflight | pass | pass |
| dressing declines, final build | none | none |
| plan refusals | none | none |
| plan complaints | 6 × `EL1`, `WX4` | 1 × `EL1`, `WX4` |

**The last two rows are the finding.** Traversability and preflight cannot tell these boards apart: both
read one component, nothing isolated, and all four preflight checks green. A board with a third of its
ground unused and a board with an eighth pass every gate identically, and the only read that separates them
is the one that was not being called.

The bar's remaining 29% is the strip behind the bay, `x ≈ −8..8`. It is dead **to the measure** and not in
play: the bay is a water lane, and coverage does not route through a lane because a lane sits outside the
build slice and therefore outside the navigable set. At forty-five minutes the bay floods and the middle of
the bar becomes the approach to it. This is the measure's blind spot, stated rather than chased to zero.

## Geometry, to check in-game

| Thing | Where | Read at |
|---|---|---|
| the bar | `x −25..25, z −5..5`, `mirrors: false` | `map.xml` — the build zone is the same `x −25..25` |
| build zone | `x −25..25, z 5..20` | `<rectangle min="-25,5" max="25,20"/>` |
| strait | bar `z = 5` to leg front `z = 20` | 15 blocks — `CT12` wants 15–40 |
| leg west (the stream) | `x −25..−10, z 20..40` | frontline run `x −25..−10` at `z 20`, 15 wide |
| leg east (the depression) | `x 10..25, z 20..40` | frontline run `x 10..25` at `z 20`, 15 wide |
| the bay | `x −10..10, z 20..30`, void until 45m | `<cuboid id="water-lanes-1" min="-10,0,20" max="10,1,30"/>` |
| west wool | room `x −70..−55, z 65..80` | wool `orange` at `(−63, 72)` |
| east wool | room `x 45..60, z 65..80` | wool `red` at `(52, 72)` |
| the leat | path shape, r 2.5, `x −62..55` along `z ≈ 51` | one step over the yard, linking the two spurs |
| the shaft | circle r4 at `(−30, 44)` | beside the leat, not under it — v1's crossed its own hole and plugged it |

## What the wools do to the shape of a match

Two wools per team, in opposite corners of the enemy half, each behind a walled approach at the end of a
spur. The two are the same distance from spawn — `WL9` refuses a board where they are not, and refused the
first draft of this one at a ratio of 2.22 against a cap of 1.23. So neither wool is the cheap one, and a
defence cannot sit on both.

The leat is what makes that a decision rather than a coin toss: a diorite causeway one step above the works,
running the width of the yard and linking the head of one spur to the head of the other. A defender rotates
along it without walking the front; an attacker who takes it is walking in the open above the yard.

## Limits

The wool rooms are stamped from v1's cage style and the buildings from v1's five house styles, unchanged —
this run rebuilt the layout, not the dressing. The bar carries one boulder and its `rot_180` image and
nothing else; a neutral middle wants more reason to stand on it than that. And `EL1` still complains that
the spawn sits an odd number of levels above the base: a spawn one step above its own apron is what `SP8`
asks for, and the two rules cannot both be satisfied here.
