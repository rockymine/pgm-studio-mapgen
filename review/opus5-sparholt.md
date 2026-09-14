# Sparholt — nothing is raised, and the objectives are sunk

> A king-of-the-hill board that is an alabaster-cutting works on two storeys. The centre point is
> inside a roofed shed entered by its four doors; the two flank points lie in open sawpits ten courses
> down, and a tramway undercroft joins the two pits without passing under the middle.

**In one sentence:** every other board in this set is a landscape with things on it, and this one is a
building with a board in it — the structure *is* the terrain, and the only relief on it is two loading
banks a stone yard would actually have.

80 × 150 blocks, `rot_180`, cell 5, `maxPlayers` 24, deck y26, tramway floor y16, observer y56.
Three plan pieces, no build zones, **two** relief marks, no pushes, five authored shapes, five layers
carrying 65 shapes between them, four themes, three capture points at a score limit of 750.
`score 0`, `valid true`, **nothing declined**.

## Two storeys, and how the lower one is stated

The ground slab is thinned to its top courses and a `below` layer carries the rock under it, the way
`showcase/20-undercroft` states a storey: the rock is stated over **every** column the board has and
the tramway is the shorter span inside it. A storey drawn as its rooms leaves the ground above it
floating.

```
shapePropsByHeight  { "24": { "floor": 20, "base_height": 4 }, "25": { … } }

rock   floor 0, base_height 20   five bands: north, south, west, east, and a CORE at
                                 x −20..20, z −12..12 — solid under the cutting shed
adit   floor 0, base_height 16   four shorter spans making one rectangle round that core
```

The core is what "without passing the middle" means: the tramway is a ring, and there is no way
through the middle of it at any height. A straight walk from one pit to the other at y16 reads
`BARRIER +10 at (19, 0)` — it is *supposed* to. The way between them is round, north or south.

`VOID` scan on the built world:

| cells | state | extent |
|---|---|---|
| 5 840 | open | x −16..15, y 20..36, z −16..15 — the cutting shed |
| 2 848 | open | x −33..32, y 16..28, z −20..−6 — the tramway's north half |
| 2 848 | open | x −33..32, y 16..28, z 5..19 — its south half |
| 1 101 | open | each spawn room |

The tramway reads as two regions rather than one because the scan lists **roofed** void and the two
sawpits are open to the sky between them. Nine roofed voids, two of them sealed, and neither of the
sealed two is a place a player goes.

## The pits are not holes anybody dug

A `sink` will not make one: a sink brings the top down and writes ground the whole way to the shape's
floor, which fills the storey underneath. Measured on the first build, `column at (26, 0)` read solid
from y21 to bedrock and the tramway came back `SEALED`.

The pit is a **`subtract` over exactly the deck's four courses** — `floor 20, base_height 4`. What is
left in the column is the tramway's own void, already open from y16, so the pit floor is the tramway
floor and the pit is ten courses deep. `column at (26, 0)` now:

```
y 63   35:0  White Wool    the studio's marker
y 29   42:0  Iron Block    a saw-frame span, one course
y 15   159:0 White Stained Clay   the pit floor — a player stands at y16
```

Nothing else between y16 and y62. The objective is at the bottom of an open cut with one iron beam
over it, which is what a sawpit looks like and is not a roof.

## Getting in, which took three builds

`SK13` reads a subtract as the board's negative space and refuses any add that fills it, on any layer.
So a stair **inside** the pit is not available at any floor below the deck, and the way in is cut in
the deck beside it.

Two things had to be measured rather than reasoned:

**One ramp, not two.** A ramp beside the west pit and a ramp beside the east pit land in each other's
columns under `rot_180` — the image of one is the other, running the other way — and two opposed
ramps in one set of columns resolve to a **V with its floor four courses over the pit**. Measured at
x 17: `26 23 22 21 20 21 22 23 26`. One ramp is stated and its image is the other pit's.

**An override add cannot put its top below its own layer's floor.** The ramp is cut to `ADIT` (16)
and arrives at **y20**, because the deck layer's floor is y20. The four courses between are closed by
two steps on the *under* layer, at `floor 0, base_height 18` — an add whose top stops at or below a
hole's floor is the ground under the void, which is the one add `SK13` allows there.

**And `x1` is exclusive when a polygon rasterizes**, which left one column of deck standing at x 19
between the ramp foot and the step — a six-block wall across the only way into the lower storey,
storing at 200 and pre-flighting OPEN. It reads as `ground 26` between two columns at 20 and 18 and
nothing but a transect says so.

The descent now, read at x 18 from z −16 to z 6, ground only:

```
26 26 26 25 25 24 24 23 23 22 22 21 21 20 20 20 20 …   then east: 20 20 18 18 16 16 …
```

Fourteen blocks of run for six of fall down the ramp, then two two-block scrambles into the pit. The
`BARRIER` entries in that transect's summary are the saw-frame spans at y29–30, which a player walks
under; the read computes its step on `surface` and the gantry is the surface.

## What the board is made of

| theme | share | what it is |
|---|---|---|
| `yard` | 65.1% | the deck: quartz, white and light-grey clay laid in courses, the `wall` bucket a sawn face |
| `rock` | 26.1% | the storey below, visible exactly where the pits and the tramway open it |
| `bank` | 6.4% | the two loading banks, worn pale clay two courses over the deck |
| `adit` | 2.4% | the tramway floor — stone brick, cracked brick, andesite and iron |

Borders: `rock | yard 480 cells`, `bank | yard 100`, `adit | yard 84`. Every one of them is a cut
face or a bench; there is no boundary on this board that is a line drawn on a plane.

**The angle distribution is the opposite of a landscape's, and that is the board:**

```
00-09° 78.6%   10-19° 3.6%   20-29° 0.9%   30-39° 0.3%
40-49° 0.7%    50-59° 13.3%  60-69° 2.6%
14 080 cells; 16.6% at 40° or steeper
```

Bimodal — a flat deck and vertical cut faces, with almost nothing between. On a terrain board that
spike would be the board reporting its own `step` quantum; here it is the pits, the bank edges and
the board's own rim, and the absence of a 10–40° population is the statement that nothing on this
board was graded by a relief.

`03-slopes.txt`: **12 834 walked, 68 scrambled, 1 178 barrier, 3 faces**, the largest 908 at
x −41..40 z −76..75 — the board's rim.

## The fault-catalogue reads

**Objective hidden — no, and the roof is the reason to check.** The cutting shed is roofed, but the
roof is a **ring** with a louvre open over the pad. `column at (0, 0)`: ground y25, and the next solid
above it is the observer platform at y65. A transect through the shed's south door at x 0:

```
(0,16) ground 26  surface 26        outside
(0,15) ground 26  surface 34        the doorway — the roof overhead, nothing underfoot
(0,14) ground 27  surface 39        inside, on the plinth
(0, 4) ground 26  surface 26  top 67   the pad, open sky
```

Walked end to end. The `BARRIER` figures that transect reports are the roof, five and eight courses
over a head.

**Spawn faces a wall — no.** (0,67) → (0,53), straight out of the lodge door:
`rises 0, falls 0, worst step 0: 0 barrier, 0 scramble, 0 drop | walked end to end`.

**Spawn faces away** — not decidable the way the other three boards decide it: a capture board's
objectives are all in front of both spawns and the plan places no goal for a bearing to be taken
against. The spawn faces the works down the centre line, and the centre point is on that line.

**Stairs that end nowhere** — the one authored flight is the pit ramp, measured above; it arrives on
the step and the step arrives on the pit floor.

**Flat, one theme, empty** — four themes, and the structure above. But see below.

## The one number that cannot be read on this board

`GET …/coverage` reports **72.1% dead, one patch of 10 151 cells at (−1, −1)** — which is the whole
middle of the board, including all three capture points.

That is a measurement artefact and not a finding. Coverage walks journeys between the places a **plan**
states, and a capture board states none: `controlPoints` ride on the intent, because the compiler fans
spawns, destroyables and cores and a board that wants hills states every one of them already fanned.
The drive says so itself in `01-flow.txt` — *"This plan states no objective, so there is no journey to
read and nothing to call dead"* — and `PL3` raises the same thing as a complaint at evaluate time:
*"this plan has no objective — no wool, destroyable or core, so nothing wins the match."*

**So the empty-board fault cannot be decided on this board by the read that decides it elsewhere.**
What can be said is what is there: a shed with four doors and 5 840 cells of interior, two ten-course
pits, a tramway ring of 5 696 cells joining them, six saw gantries, fourteen block stacks, two loading
banks and four tramway strokes on the deck. Whether that is enough is a judgement the numbers do not
make.

## The gate

```
round-trip       pass
mirror check     pass   spawn/protection ✓  build ✓
buildability     pass
traversability   pass   spawn ↔ objective chain connected across the build geometry
export gate      OPEN
06-claims.txt    placed 8, declined 0
capture points   The Cutting Shed (2) · West Sawpit (1) · East Sawpit (1), score limit 750
```

## What is open

- **Eight props on a 14 080-cell board.** The deck carries four tramway strokes and nothing else that
  the dressing pass placed; everything else on it is a layer. A works yard wants clutter it does not
  have.
- **The deck stands at y26, not the y24 the plan asked for**, and the ramp's anchors had to be cut to
  the height the board actually has rather than the height the plan stated. Why the relief settles two
  courses over `base` on a board whose only marks are at `SILL` and away from the middle is not
  something this run measured.
- **A question for the author, not a claim:** the centre point is worth two and each pit one, and the
  pits are joined to each other but not to the middle. A team that holds both pits holds two points
  and can move between them out of sight; a team that holds the shed holds two points and is
  surrounded. Is that the right trade on a three-point board, or does it make the shed a place nobody
  contests? Nothing in the corpus or in the rules answers it.
