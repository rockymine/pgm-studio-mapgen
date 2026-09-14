# Mirkholt — the lane is blind and the brow is where you are seen

> A capture-the-wool board in a dark wood laid on a shifted diagonal. One hollow way a side runs from
> the clearings down to the strait; the brow over it is the only ground the whole run is visible from.

**In one sentence:** a wool run here is a choice between the sunk lane, which is roofed by the canopy
and blind in both directions, and the brow above it, from which you can see the whole run and be seen
making it — and neither room is a step out of the spawn door: each is 53 blocks down a bare spur of
its own.

100 × 220 blocks, `rot_180`, ten pieces at four surfaces, maxPlayers 24, ground y11..y25, observer
y66. Two wools a team, each at the far end of its own lane.

## The front faces, the back is offset

Under `rot_180` a frontline spanning `[a, b]` is faced by one spanning `[−b, −a]`, so the two are
opposite each other **only where the edge is symmetric about x = 0**. There is no other arrangement.
The board's first shape put red's front at x −50..15 and blue's at x −15..50 — parallel, offset by 35,
sharing 30 blocks of a 65-block width, so most of each team's front looked across at void.

So the **front band alone is symmetric** and everything behind it stays on the diagonal. `toe` runs
x −35..35 at z 10..30 and its image x −36..34, and `GET /rules?rule=CT12` reports both frontline runs
as `x1: −35 … x2: 35` — 70 blocks, facing over 69 of them. The wood, the brow, the garth, the lanes,
the cages and the spawn are all where the shift put them, which is what keeps the two far quarters
void.

**That was the thing to check rather than assume**, because `AUTHORING-BRIEF.md` warns that a team unit
drawn symmetric about x = 0 cannot reach `fill-ratio`'s band at any size. The warning is about the
whole unit, and only the front is symmetric here: the evaluate scores **0** with the fronts facing.
Land added at the front came off the back — the wood dropped from 45 blocks of depth to 25 and then
took 5 blocks of width back out of the headroom the longer board left.

That is not decoration. `G8`'s `fill-ratio` term measures a **wool board and no other kind**: filled
land over the bounding box of the land, band [0.201, 0.542], learned from the seeds, because
capture-the-wool geometry *is* a closure with lanes through it, technical voids between them and a
strait a raider crosses. The first draft of this board was a solid rectangle of wood at **0.92** and
was refused. The shifted plan reads **inside the band**, and the composer's own read agrees with the
shape: `CT12` names a 20-block strait (band 15–40) and a **70-block frontline on an `offset`
profile**, which is the case that rule is written to pass.

Four surfaces: the `toe` at 13 (the wet flat the crossing is made from), `holt` 14, `brow` 15, and
`garth` with the back band and both spurs at 16 — one course apart everywhere, so no seam on this board
needs a flight to cross it, and the third theme sits on ground rather than being registered and
painting nothing.

## Each wool room is the far end of a spur

The first draft put `west-cage`, `lodge` and `east-cage` in one row sharing edges, so the two rooms
stood **9 blocks** from the spawn's footprint with no lane anywhere between them. Nothing refused it:
`WL2`'s text asks for a room *on a different lane than the spawn* and only its distance clause is
implemented — and that clause passes easily, because a room wide enough puts its wool block 25 blocks
away while the rooms still touch. `WL6` ("each wool on a distinct lane") has no term at all. It was
wrong and no read said so.

It is now built the way the composer builds one, which is why every wool unit it reports carries
`boxes: 2` — the room *and* its lane — against `boxes: 1` for a spawn or a hub. `opus5-coinfall` is the
shape: `camp` → `run` → `plinth`.

- **the west spur** — `apron` (x −5..20) → `west-lane` (x −30..−5, **25 blocks**) → `west-cage`
  (x −50..−30), all in the z 80..95 band.
- **the east spur** — off the garth's east side, running south into the quarter the shift left empty:
  `east-lane` (x 20..35, z 55..80, **25 blocks**) → `east-cage` (x 20..35, z 35..55).

The spawn stands 15 blocks further back again, at z 95..110, on its own piece behind the `apron`. It
shares an edge with the apron and with nothing else, so it is two pieces from either lane root and
touches no wool room — and it is joined along an edge rather than at a corner, which `PC-C` reads as no
connection at all.

The wools resolve to (−44, 15, 87) and (27, 15, 45) and the spawn to (7, 105). The walk to each is
**63 and 68 blocks, 0 placed, 0 drops** — `WL9`'s spread is 5 blocks over runs of that length — and the
two are 82 blocks apart, inside `WL7`'s 46–143.

**Both lanes are bare, and that is the point.** `column` at (−12, 87), (−20, 87), (−28, 87), (27, 60),
(27, 68) and (27, 76) reads grass block with nothing standing on any of them. No tree, no boulder, no
paving: the tree lattice excludes the two lane rectangles outright, the ground cover is drawn as two
polygons neither of which reaches a lane, and the four boulders are in the wood and on the brow. A lane
is a way to walk, and emptiness is what makes the room at its end a place a raider has to commit to
reaching.

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
| `03-slopes.txt` | 11 372 walked · 88 scrambled · **90 barrier**; 4 faces, largest 23 at x 10..18, z −60..−56 |
| `06-claims.txt` | **placed 36, declined 0** |
| relief read | level **0.526**, largestField **0.357**, 0 faces, 0 cliffs, landform *rolling*, **0 seams**, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **0.1 % dead** — two wools a team, each down its own spur, puts every piece of ground on somebody's way somewhere |
| `GET …/incline` | 53.4 % under 10° · 26.2 % teens · 13.2 % twenties · 5.7 % thirties · 1.6 % at 40°+ |
| `05-themes.txt` | glade 48.7 % · mirk 27.1 % · sike 24.2 % |
| `GET /rules?rule=CT12` | both teams' frontline runs `x1 −35 … x2 35`, 70 blocks, across a 20-block strait |
| `GET …/preflight` | traversability **pass**, `componentCount` 1 — all six spawn and wool points on one component |

## Against the fault catalogue

**Objective hidden — no, in the sense a wool room is roofed by design.** Both rooms read as their own
shell (stone brick courses, spruce posts, mushroom-stem infill) with the wool block on the floor inside
and no terrain over it, and both now sit at **y15** — the `glade` and `spur` marks hold the back band
and the east spur at the same course, so the two wools of a side are level with each other.

**Spawn faces away — no.** Red spawns at (7, 105) with yaw 180 — due −z. The two enemy rooms it is
running for stand at (44, −87) and (−27, −45), which bear 11° and 9° off that line.

**Spawn faces a wall — no.** The transect out of the door reads flat for the first fifteen blocks,
0 barrier, 0 scramble.

**Stairs that end nowhere — none to end nowhere.** One authored flight remains: `glade-gate`, 14 blocks
for a rise of 2 out of the clearing, `height_mode: "level"` with `anchor_heights`, `skirt: 0` and a
material rather than a theme. The stair off the brow went with the restructure: a push whose skirt and
crown climb at the same rate has no face, and a flight is for a face. The relief read agrees —
**0 faces, 0 cliffs, 0 seams** — and the board is down to 90 barrier cells from 300.

**A straight frontline — the front is a straight *edge*, and here that is the requirement.** The two
sides have to meet the strait over the same x range or they look across at void, and under `rot_180`
that means the edge is symmetric about x = 0. What stops it reading as a ruler is what stands on it:
the `strandflat` mark wanders the wet ground between z 10 and z 30, the hollow way arrives through it
at x −10..−2, and the theme boundary a player sees is the mark's, not the rectangle's.

**Stark contrast with no area separation — no.** Three themes, all on the ground: the wood's leaf
litter, the clearings' lit grass, and the wet flat at the strait. Wood meets clearing over 130 border
cells at a bench (`court-flat` is stated with a `tread`), and wood meets the sike over 40 at a
one-course step.

**Flat, one theme, empty — no, but the wood is thinner than it should be** (below).

## Limits

- **The wood stands eleven trunks a side, and squaring the front is what cost it.** The symmetric
  front band takes 20 blocks of depth across the whole width, so the `holt` went from 45 deep to 25;
  widening it 5 blocks out of the longer board's headroom bought reach but no trunks, because the
  ground it added lies inside the hollow way's own exclusion. Eleven a side is a wood a player cannot
  see across, and it is thinner than the board's own sentence implies. The fronts facing is worth more
  than the trees, but it is a real trade and this is the number it cost.
- `04-reach.txt` reports the opposite half as `no-build-zone` unreachable while `preflight` reports
  one traversable component containing all six spawn and wool points, and `coverage` reports 0.1 %
  dead. Two of the three reads say the board is joined and one says it is not; the strait is 21 blocks
  of void inside a build zone that spans z −20..20, which is a bridge a player builds. Worth an
  author's eye.
- `SP2` still complains that the spawn is not near the back of its lane, and `FR9` now complains about
  both of the `toe`'s side faces rather than one. Both are complaints on a board scoring 0; the FR9
  figure did not move when the front band was deepened from 15 blocks to 20, so it is not measuring the
  face it reads as.
- The east spur's room is the one piece of ground on the board a defender can be cut off on: it hangs
  25 blocks south of the garth with void on three sides. That is what a spur is for, but it is worth an
  author's eye on how it plays.
