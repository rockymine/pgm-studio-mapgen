# Mirkholt — the lane is blind and the brow is where you are seen

> A capture-the-wool board in a dark wood laid on a shifted diagonal. One hollow way a side runs from
> the clearings down to the strait; the brow over it is the only ground the whole run is visible from.

**In one sentence:** a wool run here is a choice between the sunk lane, which is roofed by the canopy
and blind in both directions, and the brow above it, from which you can see the whole run and be seen
making it — and neither room is a step out of the spawn door: each is 53 blocks down a bare spur of
its own.

100 × 200 blocks, `rot_180`, nine pieces at four surfaces, maxPlayers 24, ground y11..y25, observer
y66. Two wools a team, each at the far end of its own lane.

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

- **the west spur** — `lodge` (x −5..20) → `west-lane` (x −30..−5, **25 blocks**) → `west-cage`
  (x −50..−30), all in the z 80..95 band.
- **the east spur** — off the garth's east side, running south into the quarter the shift left empty:
  `east-lane` (x 20..35, z 55..80, **25 blocks**) → `east-cage` (x 20..35, z 35..55).

The wools resolve to (−44, 15, 87) and (27, 15, 45) and the spawn to (7, 90). The walk to each is
**53 blocks, 0 drops** (2 blocks placed on the west, none on the east) — balanced to the block, which
is `WL9` satisfied by construction rather than by tuning, and 82 blocks apart, inside `WL7`'s 46–143.

**Both lanes are bare, and that is the point.** `column` at (−12, 87), (−20, 87), (−28, 87), (27, 60),
(27, 68) and (27, 76) reads grass block with nothing standing on any of them. No tree, no boulder, no
paving: the tree lattice excludes the two lane rectangles outright, the understorey flora stops at
z 80, and the four remaining boulders are in the wood and on the brow. A lane is a way to walk, and
emptiness is what makes the room at its end a place a raider has to commit to reaching.

Adding two spurs is adding land, so `fill-ratio` was re-read rather than assumed: it came back **0.55**,
just outside `G8`'s band, and the plan was trimmed — the toe from 6 cells to 5, the brow from 10 to 8,
the garth from 11 to 10 — until the evaluate scored **0** again.

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
| `03-slopes.txt` | 9 912 walked · 98 scrambled · **90 barrier**; 4 faces, largest 23 at x 10..18, z −60..−56 |
| `06-claims.txt` | **placed 46, declined 1** |
| relief read | level **0.457**, largestField **0.343**, 0 faces, 0 cliffs, landform *rolling*, **0 seams**, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **0.1 % dead** — two wools a team, each down its own spur, puts every piece of ground on somebody's way somewhere |
| `GET …/incline` | 46.7 % under 10° · 25.9 % teens · 17.8 % twenties · 7.9 % thirties · 1.7 % at 40°+ |
| `05-themes.txt` | glade 48.2 % · mirk 44.4 % · sike 7.4 % |
| `GET …/preflight` | traversability **pass**, `componentCount` 1 — all six spawn and wool points on one component |

## Against the fault catalogue

**Objective hidden — no, in the sense a wool room is roofed by design.** Both rooms read as their own
shell (stone brick courses, spruce posts, mushroom-stem infill) with the wool block on the floor inside
and no terrain over it, and both now sit at **y15** — the `glade` and `spur` marks hold the back band
and the east spur at the same course, so the two wools of a side are level with each other.

**Spawn faces away — no.** Red spawns at (7, 90) with yaw 180 — due −z. The two enemy rooms it is
running for stand at (44, −87) and (−27, −45), which bear 12° and 10° off that line.

**Spawn faces a wall — no.** The transect out of the door reads flat for the first fifteen blocks,
0 barrier, 0 scramble.

**Stairs that end nowhere — none to end nowhere.** One authored flight remains: `glade-gate`, 14 blocks
for a rise of 2 out of the clearing, `height_mode: "level"` with `anchor_heights`, `skirt: 0` and a
material rather than a theme. The stair off the brow went with the restructure: a push whose skirt and
crown climb at the same rate has no face, and a flight is for a face. The relief read agrees —
**0 faces, 0 cliffs, 0 seams** — and the board is down to 90 barrier cells from 300.

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

- **The wood stands seventeen trunks a side**, which it did not before the restructure. Three things
  bought that: the hollow way moved to hug the wood's east edge so the plantable mass is one strip
  rather than two slivers, its reach came down from 12 to 9, and the brow's stair — which blanketed a
  20-block swathe of the wood in keep-out — is gone. Seventeen a side is a wood a player cannot see
  across; it is not the closed canopy the board's own sentence implies, and a wider `holt` is the only
  thing that would buy it.
- `04-reach.txt` reports the opposite half as `no-build-zone` unreachable while `preflight` reports
  one traversable component containing all six spawn and wool points, and `coverage` reports 0.1 %
  dead. Two of the three reads say the board is joined and one says it is not; the strait is 21 blocks
  of void inside a build zone that spans z −20..20, which is a bridge a player builds. Worth an
  author's eye.
- `SP2` still complains that the spawn is not near the back of its lane. The lodge sits at the east end
  of the back band with the lane running west out of it, which is the back of that lane; the rule's own
  text says the lint approximates "back" per-piece.
- The east spur's room is the one piece of ground on the board a defender can be cut off on: it hangs
  25 blocks south of the garth with void on three sides. That is what a spur is for, but it is worth an
  author's eye on how it plays.
