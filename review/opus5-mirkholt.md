# Mirkholt — the lane is blind and the brow is where you are seen

> A capture-the-wool board in a dark wood laid on a shifted diagonal. One hollow way a side runs from
> the clearings down to the strait; the brow over it is the only ground the whole run is visible from.

**In one sentence:** a wool run here is a choice between the sunk lane, which is roofed by the canopy
and blind in both directions, and the brow above it, from which you can see the whole run and be seen
making it.

100 × 200 blocks, `rot_180`, seven pieces at four surfaces, maxPlayers 24, ground y11..y25, observer
y66. Two wools a team, the spawn between them.

## The arrangement, and why it is shifted

The side is offset **west**: the wood runs from each team's own back corner down to a `toe` at the
strait, and `rot_180` lays the other team's across the opposite diagonal. What neither side fills —
the two far quarters — is the board's device rather than its margin.

That is not decoration. `G8`'s `fill-ratio` term measures a **wool board and no other kind**: filled
land over the bounding box of the land, band [0.201, 0.542], learned from the seeds, because
capture-the-wool geometry *is* a closure with lanes through it, technical voids between them and a
strait a raider crosses. The first draft of this board was a solid rectangle of wood at **0.92** and
was refused. The shifted plan reads **inside the band**, and the composer's own read agrees with the
shape: `CT12` names a 20-block strait (band 15–40) and a **70-block frontline on an `offset`
profile**, which is the case that rule is written to pass.

Four surfaces: the `toe` at 13 (the wet flat the crossing is made from), `holt` 14, `brow` 15, and
`garth` with the three back rooms at 16 — one course apart everywhere, so no seam on this board needs a
flight to cross it, and the third theme sits on ground rather than being registered and painting
nothing.

## The hollow way

A `line` relief mark of reach 12 with `tread` 1, running (−40, 76) → (−38, 60) → (−32, 44) →
(−24, 30) → (−14, 20) → (−2, 16) at heights 13, 11, 10, 10, 11, 12. The narrow tread is what makes it
a lane rather than a ridge: five blocks are held flat down the middle and the rest of the band lofts
back up to the wood, so the lane has banks and not walls. It ends on the `toe`, which is the ground
the crossing is made from — the lane delivers a raider to the strait rather than stopping short of it.

A `worn` stroke paints the lane's floor, and the wood is planted clear of it: a hollow way roofed at
its edges and open down the middle is what makes it read as a lane.

## What the reads say

| read | number |
|---|---|
| `03-slopes.txt` | 9 980 walked · 220 scrambled · **300 barrier**; 8 faces, largest 80 at x 13..20, z −47..−27 |
| `06-claims.txt` | **placed 30, declined 3** |
| relief read | level **0.459**, largestField **0.166**, 2 faces, 0 cliffs, landform *rolling*, **0 silent marks**, symmetry error **0** |
| `GET …/coverage` | **0.0 % dead**, 21 journeys — two wools a team with the spawn between them puts every piece of ground on somebody's way somewhere |
| `GET …/incline` | 46.9 % under 10° · 28.5 % teens · 11.1 % twenties · 8 % thirties · 5.4 % at 40°+ |
| `05-themes.txt` | mirk 51.4 % · glade 37.1 % · sike 11.4 % |
| `GET …/preflight` | traversability **pass**, `componentCount` 1 — all six spawn and wool points on one component |

## Against the fault catalogue

**Objective hidden — no, in the sense a wool room is roofed by design.** `column (−41, 90)` and
`column (16, 90)` both read the room's own shell (stone brick courses, spruce posts, mushroom-stem
infill) with the wool block on the floor inside and no terrain over it. The wools resolve to
(−39, 15, 90) and (14, 17, 90); the two rooms of a side sit two courses apart because the east one
stands outside the `court-flat` mark's ring and takes the grain instead, which is a difference a
player reads as ground and not as a fault.

**Spawn faces away — no.** Red spawns at (−13, 92) with yaw 180 — due −z. The two enemy rooms it is
running for stand at (−16, −90) and (41, −90), which bear 1° and 17° off that line.

**Spawn faces a wall — no.** The transect out of the door reads flat at y16 for the first fifteen
blocks, 0 barrier, 0 scramble.

**Stairs that end nowhere — no.** Two authored flights: `brow-stair` runs 20 blocks for a rise of 9
off the push's crown into the lane, and `glade-gate` 14 blocks for a rise of 2 out of the clearing.
Both are `height_mode: "level"` with `anchor_heights`, `skirt: 0` and a material rather than a theme.

**A straight frontline — no.** The frontline is the strait, and it is `offset`: the two sides face
each other across 41 blocks of overlap at a 20-block gap, which is a crossing and not a doorway. The
one complaint the evaluate keeps is `FR9` on the `toe`'s `+x` side — a 10-block face where a crossing
wants 15 — and it is a side face rather than the front.

**Stark contrast with no area separation — no.** Three themes, all on the ground: the wood's leaf
litter, the clearings' lit grass, and the wet flat at the strait. Wood meets clearing over 130 border
cells at a bench (`court-flat` is stated with a `tread`), and wood meets the sike over 40 at a
one-course step.

**Flat, one theme, empty — no, but the wood is thinner than it should be** (below).

## Limits

- **The wood stands eight trunks a side and wants thirty.** The cause is measured rather than guessed:
  the wood is 40 blocks wide, the hollow way and `DR-ROAD`'s three-block trunk standoff take 14 of
  them, and a copied canopy tree is 15–17 blocks across, so about four trunks fit across the lane's
  two banks and eight or nine down its length. Widening the `holt` piece would fix the wood and put
  the fill ratio back outside `G8`'s band; the honest fix is a second lane and a second gill, which is
  a different plan.
- `04-reach.txt` reports the whole opposite half as `no-build-zone` unreachable while `preflight`
  reports one traversable component containing all six spawn and wool points, and `coverage` reports
  0 % dead over 21 journeys. Two of the three reads say the board is joined and one says it is not;
  the strait is 21 blocks of void inside a build zone that spans z −20..20, which is a bridge a player
  builds. Worth an author's eye.
- `largestField` 0.166 is above `RL5`'s bar but the lowest of this set: the flat on this board is in
  several patches rather than one, which is what a wood cut by a lane is.
