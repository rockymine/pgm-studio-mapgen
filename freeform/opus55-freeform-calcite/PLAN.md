# Calcite — the plan

A King of the Hill board, planned and not yet built; this page is for a go or no-go. It is a white marble
quarry cut in square benches round a flooded pit, with three hills: the Middle on an island in the pit, paying
double, and a side hill on the north and the south bench, paying single.

![plan sketch](renders/00-plan-sketch.png)

## What already exists, and what I took from it

**Mush is the reference, read from its region files and XML.** It is about 109 blocks across, with three
8 × 8 hills on one diagonal and the two spawns on the other. Its rotations are carried by ten jump pads, and
its XML turns fall damage off for a player who has just used one. Each hill scores a point a second, with a
5-second capture, no decay, and nobody owning a hill at the start.

**PGM's jump pad is one line.** `<apply region=… velocity="x,y,z"/>` sets a player's velocity as they step into
the region, each axis clamped to ±3.9 blocks a tick, and 1.8's physics carries them from there. Each tick
moves the player by the velocity, then `vy = (vy − 0.08) × 0.98` and the horizontal speed falls by 0.91.
`scripts/pad.py` runs those steps. Run on Mush's pads, it lands them where Mush built the platforms for them,
so this board's pads are designed by simulation rather than by trial.

**Mush Pit, the author's own five-point map, was read from its region files and XML.** It is about 70 × 87, a
ring of roofed corridors round void with a cross and one diagonal running through a round middle. The floors
are stacked two and three deep under giant mushroom caps at the corners. Its points are rooms on the ring's
sides and the middle, each capture region a plus-shaped union of cuboids that takes in the room's doorways,
and every fall off a corridor is into the void (`renders/ref-mushpit-topdown.png`).

**What I take from Mush Pit:** a capture region shaped to its room and its thresholds rather than a bare
square, floors stacked over each other so a fight has an above and a below, a diagonal that breaks the grid,
and a low ground that kills: Mush Pit's void is Calcite's lava.

**The 5CP variant was read and set aside.** In the include, captures go in order, the middle point needs your
own second point, and spawns move as points fall. That is a tournament format, and this board is the usual
three hills; the bowl could carry 5CP later with two more points on the benches.

## The board

| Level | Height | What it is |
|---|---|---|
| The pit | 10 | lava, 46 × 38: a fall into it is the end |
| The Ledge | 16 | the low ground: a ring 6 wide round the lava; the causeways, the hills' front stairs and the Spring's tunnels meet on it |
| The apron | 19 | the Middle's island, 18 × 18, round the stepped hill |
| The Bench | 22 | the middle ground: a ring 8 wide, broken only by the side hills' alcoves |
| The Middle | 22 | 8 × 8 on top of two rings of steps; the Spring under it |
| The side hills | 23 | 8 × 8 in an alcove cut into the Rim's face, walled on three sides, open toward the Middle, the same from either side |
| The Rim | 28 | the high ground: a ring 8 wide round the top; the spawns open onto it |
| The wall | 40 | the quarry face round everything; nobody leaves the bowl |

**The three grounds are joined by stairs everywhere a fight would want to change level.** Between the Ledge
and the Bench there is a well on each team's axis, a stair at every corner and a stair at either side of each
hill. Between the Bench and the Rim there is a notch on each team's axis and a stair at every corner. A drop
of six goes the other way anywhere. The sections in the sketch are drawn at true scale, so a stair reads as a
stair and only the drops read as walls.

**The board is 120 × 96, and blue's half is red's turned half a circle.** Red spawns in the west wall and
blue in the east. Turning makes the North hill the side hill nearer red's tunnel and the South hill blue's,
and each side hill is mirrored about its own middle, so both are 82 to 83 blocks from either spawn on foot.

## The routes, and what each is for

**Every route has a job, and a moment in the match when it is the right one.** Lengths are red's, walked on the
plan by `scripts/plan_check.py`; blue's are the same turned.

| Route | Length | One way? | What it is for, and when it is used |
|---|---|---|---|
| **The main lane:** Rim notch, Bench well, causeway, apron | 50 to the Middle | no | the straight push onto the Middle at the start and after a wipe; the causeway is four wide over the lava, so it is also where a held Middle is defended |
| **A front stair:** up from the Ledge, eight wide, straight onto a side hill | 88 from the spawn by the tunnel | no | the frontal attack on a side hill, in the open line from the Middle; where the parkour and both of the Spring's trenches arrive |
| **A side stair and window,** one in each wall: up the outside of the wall, through it, a drop of four | 83 to 84 from the spawn along the Bench | yes, the drop | the flank onto a held side hill from the Bench, from either end, past the walls that hide it from the Bench |
| **The Rim, dropping onto a side hill** | 92 | yes, the drop is 5 | the high flank, long, ending on top of the hill's holders; the route when the hill is held and the Bench is watched |
| **The spawn tunnel** to the Ledge's corner | 88 to a side hill | no | the covered way down to the low ground; for a team under fire from the Rim |
| **The pads from the apron,** two to each side hill, mirrored, landing beside either side stair | 32 and 33 from the Middle | yes | the rotation from the Middle to either flank of a side hill; how the team holding the Middle contests a side hill without giving it up |
| **The parkour:** two pillars from the Ledge onto the apron over the lava, gaps 2, 2 and 2, each a block higher | 30 from a side hill | no, but up is the point | a side hill's way back to the Middle, fast and exposed; a miss is death |
| **The diagonal steps:** three pillars from the arrows' corner of the Ledge to the apron's corner, gaps of two by one | 40 from the arrows to the Middle | no, but up is the point | the corner's way onto the Middle, mirroring the pad in the opposite corner: restock arrows, then jump in |
| **The Spring:** down a stairwell from the apron, past the golden apples, under the lava in a glass tunnel that forks, up either trench beside a side hill's front stair | 65 from the Middle to a side hill | no | the covered rotation: slower than a pad or the parkour, out of sight and through the apples; the attackers' way to arrive at a hill's front stair unseen |
| **The pad from the Ledge's corner** over the lava onto the Middle's apron | 18 ticks of flight | yes | the corner's way onto the Middle, in the two corners without arrows, answering the diagonal steps in the other two |
| **The drops** from the Rim to the Bench, 6, all round | — | yes | a flank anywhere; costs a heart and a half, never a route back |

**The Middle is the hub, as it should be in King of the Hill.** The shortest way from a spawn to a side hill
is through the Middle and one of its pads (70 to 71), and a side hill's quickest way to the other is through
the Middle as well (58 to 59). Holding the Middle is the rotation, not only the points.

**The jumps are only the ones planned.** The checker looks for every gap of one to three blocks, in any
direction, that a player can cross landing no higher than a block up and that saves more than a few steps of
walking. It finds the two parkour lines, the two lines of diagonal steps, and two hops across the top of the
corner stairs, and nothing else.

**The pads were tuned in the simulator.** Each was given a target, and a search over velocities found one that
lands within a block of it.

| Pad | Velocity | Lands | Flight |
|---|---|---|---|
| apron, west, to the Bench by the North hill's west stair | −1.08, 0.75, −2.74 | (−13.5, −29.5), y 23 | 23 out, 13 ticks, apex 23.5 |
| apron, east, to the Bench by the North hill's east stair | 1.08, 0.75, −2.74 | (13.5, −29.5), y 23 | its mirror exactly |
| Ledge corner onto the Middle's apron | 2.21, 0.90, 1.88 | the apron at (−7.4, −6.4), y 20 | 18 ticks, apex 21.9 |

No pad lands lower than it starts, so none costs fall damage. The XML will still clear fall damage
after a pad as Mush does, in case a player is pushed off course.

## The hills

- **No cover on a hill.** Each is an 8 × 8 top of polished stone with a ring of wool that shows who holds it.
  It is held with players, and fought for from the steps round it.
- **The Middle is stepped:** two rings of single steps round it on every side, from the apron at 19 to its
  top at 22. It is attacked from every side: two causeways, two parkour lines, two lines of diagonal steps,
  and from below out of the Spring.
- **A side hill stands in an alcove.** Walls two blocks taller than the Rim close its two sides, and the Rim's
  face closes its back, so the Bench cannot see into it. Only its front is open, toward the Middle, and the
  Middle's top sees straight onto it.
- **A side hill is the same from either side.** It has the front stair from the Ledge, a side stair and window
  in each wall, the drop from the Rim behind it, and a pad from the Middle landing by each side stair. Either
  team can take either flank.

## The Spring

**The room under the Middle is a crossroads as well as a larder.** Two stairwells come down into it from the
apron's west and east sides, and two glass tunnels leave it north and south under the lava. Under each side
hill's front stair a tunnel forks and climbs two trenches of stairs onto the Ledge, one either side of the
stair. The golden apples spawn in the middle of the room, so every route through it passes them.

**The tunnels run under the lava in glass.** A player in one walks under a ceiling of lava, and a player on the
causeway sees them below.

## What `map.xml` will say

- `<king>`: three hills with a 5-second capture, a neutral start, no decay and points that do not grow. The
  Middle pays 2 a second and the side hills 1. First to 600, or the most points at 15 minutes.
- **Spawners:** golden apples in the Spring, one at a time, every 30 seconds; arrows in two diagonal inner
  corners of the Ledge, the north-east and the south-west, where the diagonal steps start.
- **The lava** kills as it is; nothing in the XML needs to.
- **No block interaction at all;** the kit is a stone sword, a bow, arrows, a golden apple and the conquest
  armour.
- **Pads:** each pad's region carries its velocity, and fall damage is denied until the player lands.
- **Spawns:** enemy entry denied; the spawn opens onto the Rim.

## Theme, decided now

- **A dimension-stone quarry:** walls cut in courses of diorite, polished diorite, stone and quartz, the
  bench faces drill-marked (a vertical line of andesite every few blocks), floors of polished stone and white
  dust (sand with a little gravel).
- **The pit:** lava, under glass where the Spring's tunnels cross it, lighting the bowl from below.
- **Made things:** timber derricks at the Rim's corners, as landmarks and as cover on the Rim; a stone
  hut at each spawn; iron-bar rails only where a fall is not the point.
- **Team colour** on the spawn huts and on the hills' wool rings only.

## How the plan changed after the review

| The review said | What changed |
|---|---|
| Use the room under the Middle as a route too, a tunnel under the water | The Spring has two stairwells in and two glass tunnels out, under the pool to the Ledge |
| The Ledge read as a wall; treat it as a ground, with stairs up from where the tunnel comes out | Stairs at every corner and either side of each hill; each hill has a front stair up from the Ledge; the sections are drawn at true scale |
| Arrow spawners in two diagonal inner corners | On the Ledge, north-east and south-west |
| Side hills encased: open toward the Middle, walled on three sides, a small stair in one wall to drop in | The alcove, walls two over the Rim, the side stair and window in the west wall, a drop of four |

## How the plan changed after the second review

| The review said | What changed |
|---|---|
| Make the pool dangerous: lava | The pit is lava; the ladders are gone; a miss on the parkour or the steps is death |
| The side hills must be mirrored so each team can enter from both sides | A side stair and window in both walls, a pad from the Middle to either flank, and the Spring's tunnel forking to a trench either side of the front stair |
| The jump pads mirrored | The apron's pads come in mirrored pairs, the east one the west one's exact mirror |
| Diagonal steps from the arrow spawner to the Middle, since the other corner has the pad | Three pillars from each arrows' corner to the apron's corner, gaps of two by one, each a block higher |

## Built

**The plan was built as approved, with one change.** The pad in the corners without arrows was to lift a
player from the Ledge to the Rim. Flown against the built blocks, the search found no velocity that clears the
Bench's face two blocks away and still lands on the Rim, so it now carries the player over the lava onto the
Middle instead.
`REPORT.md` has the rest.

## Decisions for you

None open: the scale and the corners were confirmed, and the board is built.
