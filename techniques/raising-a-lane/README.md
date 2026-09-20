# Raising a lane

**A composed lane arrives flat, and giving it height is a choice between tiers rather than between tricks.**
The plan says what ground is where and at what surface; the layout draws shapes on it; the relief solves a
field under all of them; a made layer puts a storey over the lot. Every tier can raise a lane, and what
separates them is what the climb costs. Open the card in the studio as `technique-raising-a-lane`, or run
`build.py`.

Nine panels, each the same lane — **12 blocks wide, 48 long, its foot at surface 9 and its head eight blocks
up at 17** — so the only difference between two of them is the instrument. Every read is taken down the same
centreline, foot to head.

| Panel | Tier | Stated as | `walk`, foot to head |
|---|---|---|---|
| `piece-steps` | plan | 5 bands of ground stepping by 2 | **4 × `scramble +2`**, 4 blocks placed |
| `piece-treads` | plan | 9 bands stepping by 1 | walked end to end, 0 placed |
| `tilted` | layout | one polygon, `anchor_heights` 9, 9, 17, 17 | walked end to end, 0 placed |
| `plates` | layout | 8 override plates over ground left at the foot | walked end to end, 0 placed |
| `raise-skirted` | layout | one `raise` of 8, `skirt` 5 | **2 × `scramble +2`**, 2 blocks placed |
| `raise-sheer` | layout | the same `raise`, `skirt` 0 | **`barrier +8`** |
| `marks` | relief | two `area` marks, the middle left unpinned | walked end to end, 0 placed |
| `push` | relief | one push of 8 over the head, `falloff` 16 | walked end to end, 0 placed |
| `deck` | layers | the lane untouched, a made layer over it | walked end to end — the lane never climbs |

## What each tier is actually good at

**The plan tier is coarse, and its own gate says so.** A plan piece is one height, so a lane climbing eight
blocks is a run of pieces: five of them stepping by 2, or nine stepping by 1. Only the second walks —
`piece-steps` answers four `scramble +2`, which is a climb a player pays for with a placed block at every
seam, and `EL1` names a land seam of 2 as un-walkable for exactly that reason.

**What it buys is that every step is its own shape.** Nine treads are nine polygons the compiler emits, so
`themeById` can paint each one and a relief can hold each one; the smooth answers below are one shape and one
paint. Height first, then paint, is that fact stated the other way round.

**The layout tier is exact, and invisible to the plan.** `tilted` is one polygon and four anchors — an anchor
is the shape's own **thickness** at that vertex rather than an offset from `base_height`, so a lane climbing
9 to 17 states 9, 9, 17, 17. It walks end to end. The plan tier walks pieces flat and cannot see an authored
flight at all, so a board built this way still reads its seam at the plan gate.

**A `raise` is a shelf, not a ramp, and `skirt` decides which.** With `skirt: 0` the lane jumps its whole
lift at the shelf's edge and `walk` calls it `barrier +8` — a wall across the lane. A skirt grades that edge
back down, but **it is paid out of the shape's own top from every side at once**, so a lane 12 wide can
afford 5 — and 8 blocks over 5 cells is 1.6 a cell, which is why `raise-skirted` still answers two
`scramble +2`. A raise makes a shelf reachable; it does not make a lane walkable.

**The relief tier grades what is between two statements rather than stating the ground.** `marks` pins the
first ten blocks at the foot and the last ten at the head and leaves the middle to the relaxation, which
climbs it one course at a time. `push` states no head at all: it lifts the far end by 8 and grades back over
`falloff` 16. Both walk. Neither can be kept off anything else in reach — a mark pins its own cells and
slopes everything within `reach`, and a push's ring plus its falloff is its whole extent.

**The layer tier does not raise the lane, which is sometimes the answer.** `deck` leaves the ground at 9 and
crosses a made storey over it at 16, on four legs with three clear underneath. The lane a player runs is
unchanged; what is new is a route over it and cover under it.

## What the profiles say that a picture does not

`profiles.txt` reads every panel down its centreline every two blocks. Three things are only there.

**`plates` and `piece-treads` are the same profile and not the same ground.** Both read 9, 10, 11 … 17. The
column under a plate at `(-46, -16)` reads grass at **y14 over dirt over stone** — the plate *is* the ground
now, because an **override add is a privileged set and wins the column whatever its height**, so a plate
replaces the lane under it rather than standing on it.

**`marks` and `push` start a course lower than everything else.** Both read 8 at the foot where the drawn
panels read 9: the relief's `base` is what unpinned ground settles at, and a shape's drawn height is only
what it was drawn at.

**`raise-sheer` is the only panel whose profile has a cliff in it**, and `raise-skirted`'s grade is visible
as 10, 12, 13, 14, 16, 17 — the twos are the scrambles.

## The recipe

- **a lane that has to be walked wants one course a seam.** Nine pieces, or one tilted polygon, or a relief
  that grades. Two is a placed block, and `EL1` says so before anything is built.
- **reach for the plan tier when the steps have to be addressable** — a theme, a relief scope or a prop
  keep-out per step. Reach for the layout tier when the climb has to be exact and nothing needs to name it.
- **never state a climb with a bare `raise`.** `skirt: 0` is a wall and a skirt wide enough to walk needs a
  shape at least twice the lift across. On a lane, that is a shelf beside the route, not the route.
- **an anchor is a thickness, not an offset**, and `SK22` refuses anchors on a rectangle — a rectangle states
  its bounds rather than the points a height is stated at, so anything that tilts is drawn as a polygon.
- **an override add wins the column whatever its height.** Use it where the plate *is* the new ground; a
  plain add taller than what it stands on is what stands on it.
- **the relief cannot be aimed at one lane.** A mark slopes everything within `reach` and a push lifts every
  cell inside its ring and falloff, so on a board of corridors the layout tier is the one that stays put.

## Limits

**The two plan panels are what a plan compiles to, not a plan.** A compiled plan carries its own
`mirror_mode` and a group that mirrors, so nine compiles cannot share a world —
`techniques/taking-over-a-composed-board` is the worked plan-driven case, where the same lane is cut into
three one-cell treads between two bars.

**The climb is eight blocks on a 48-block lane, and the numbers are about that lane.** A longer run at the
same rise walks at a shallower grade; a shorter one does not. What transfers is the rule, not the profile.

## What checks it

- `profiles.txt` — every panel's centreline, every two blocks, foot to head.
- `walks.txt` — `walk` over each one: the route, the blocks placed, and the word for each step that is not
  a plain walk.
- `columns.txt` — six columns, for the three facts a profile cannot carry: what is under an override plate
  against what is under a tread, the deck's own column, the sheer shelf's face, and the two relief panels'
  ungoverned middle.
- `raising-a-lane.layout.json` — what `build.py` writes: 31 ground shapes in nine groups, and two made
  layers for the deck.

Renders: `iso.png`, the nine lanes together; `profiles-west.png`, `profiles-middle.png` and
`profiles-east.png`, each column of panels cut through so the three climbs read as profiles — the cut runs
along z, so a panel's head is on its left.
