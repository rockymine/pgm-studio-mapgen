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
square, floors stacked over each other so a fight has an above and a below, and a diagonal that breaks the
board's grid. **What I leave:** its void. Calcite's low ground is a pool you climb out of, a slower price than
death, because a King of the Hill fight is about who stands on the hill longest.

**The 5CP variant was read and set aside.** In the include, captures go in order, the middle point needs your
own second point, and spawns move as points fall. That is a tournament format, and this board is the usual
three hills; the bowl could carry 5CP later with two more points on the benches.

## The board

| Level | Height | What it is |
|---|---|---|
| The pool | 10 | water, 46 × 38; falling in is safe, getting out takes a ladder |
| The Ledge | 16 | the low ground: a ring 6 wide round the pool; the causeways, the hills' front stairs and the Spring's tunnels meet on it |
| The apron | 19 | the Middle's island, 18 × 18, round the stepped hill |
| The Bench | 22 | the middle ground: a ring 8 wide, broken only by the side hills' alcoves |
| The Middle | 22 | 8 × 8 on top of two rings of steps; the Spring under it |
| The side hills | 23 | 8 × 8 in an alcove cut into the Rim's face, walled on three sides, open toward the Middle |
| The Rim | 28 | the high ground: a ring 8 wide round the top; the spawns open onto it |
| The wall | 40 | the quarry face round everything; nobody leaves the bowl |

**The three grounds are joined by stairs everywhere a fight would want to change level.** Between the Ledge
and the Bench there is a well on each team's axis, a stair at every corner and a stair at either side of each
hill. Between the Bench and the Rim there is a notch on each team's axis and a stair at every corner. A drop
of six goes the other way anywhere. The sections in the sketch are drawn at true scale, so a stair reads as a
stair and only the drops read as walls.

**The board is 120 × 96, and blue's half is red's turned half a circle.** Red spawns in the west wall and
blue in the east. Turning makes the North hill the side hill nearer red's tunnel and the South hill blue's,
so each team's near side hill is 75 blocks from its spawn on foot and the far one 83.

## The routes, and what each is for

**Every route has a job, and a moment in the match when it is the right one.** Lengths are red's, walked on the
plan by `scripts/plan_check.py`; blue's are the same turned.

| Route | Length | One way? | What it is for, and when it is used |
|---|---|---|---|
| **The main lane:** Rim notch, Bench well, causeway, apron | 50 to the Middle | no | the straight push onto the Middle at the start and after a wipe; the causeway is four wide, so it is also where a held Middle is defended |
| **The front stair:** up from the Ledge, eight wide, straight onto a side hill | 81 from the spawn by the tunnel | no | the frontal attack on a side hill, in the open line from the Middle; where the parkour, the Spring's tunnel and the Ledge all arrive |
| **The side stair and the window:** up the outside of a hill's west wall, through a window, a drop of four | 83 from the spawn along the Bench | yes, the drop | the flank onto a held side hill from the Bench, past the walls that hide it from the Bench's sightlines |
| **The Rim, dropping onto a side hill** | 92 | yes, the drop is 5 | the high flank, long, ending on top of the hill's holders; the route when the hill is held and the Bench is watched |
| **The spawn tunnel** to the Ledge's corner | 81 to the near side hill | no | the covered way down to the low ground, arriving below the near side hill; for a team under fire from the Rim |
| **The pad from the apron** to the Bench by the side stair | 36 from the Middle | yes | the rotation from the Middle to a side hill's flank; how the team holding the Middle contests a side hill without giving up the Middle |
| **The parkour:** two pillars from the Ledge onto the apron, gaps 2, 2 and 3, each a block higher | 30 from a side hill | no, but up is the point | the side hill's way back to the Middle, fast and exposed over the pool; a miss is a swim |
| **The Spring:** down a stairwell from the apron, past the golden apples, under the pool in a glass tunnel, up a trench onto the Ledge below a side hill | 69 from the Middle to a side hill | no | the covered rotation: slower than the pad or the parkour, but out of sight and through the apples; the holders' regeneration, and the attackers' way to arrive at a hill's front stair unseen |
| **The pad from the Ledge's corner** up to the Rim's corner | 97 via the tunnel to a hill | yes | the way out of the low ground: from the tunnel's mouth or a ladder, up to the Rim and onto a drop |
| **The drops** from the Rim to the Bench, 6, all round | — | yes | a flank anywhere; costs a heart and a half of health, never a route back |
| **The ladders**, four a side out of the pool | — | up only | the price of falling off a causeway or missing the parkour |

**The Middle is the hub, as it should be in King of the Hill.** The shortest way from a spawn to its near side
hill is through the Middle and its pad (70), and a side hill's quickest way to the other is through the
Middle as well (58 to 59). Holding the Middle is the rotation, not only the points.

**The jumps are only the ones planned.** The checker looks for every gap of one to three blocks a player can
cross landing no higher than a block up, and finds the parkour's six jumps on each side and nothing else; hops across a stairwell cut into a floor are counted apart.
No ledge or corner of the bowl gives a jump the plan did not draw.

**The pads were tuned in the simulator.** Each was given a target, and a search over velocities found one that
lands within a block of it.

| Pad | Velocity | Lands | Flight |
|---|---|---|---|
| apron to the Bench by the North hill's side stair | −0.62, 0.85, −2.42 | the Bench at (−13.5, −29.5), y 23 | 22 out, 17 ticks, apex 24.4 |
| Ledge corner to the Rim | −1.33, 1.55, −1.43 | the Rim at (−40.4, −37.4), y 29 | 19 out, 22 ticks, apex 29.9 |

Neither pad lands lower than it starts, so neither costs fall damage. The XML will still clear fall damage
after a pad as Mush does, in case a player is pushed off course.

## The hills

- **No cover on a hill.** Each is an 8 × 8 top of polished stone with a ring of wool that shows who holds it.
  It is held with players, and fought for from the steps round it.
- **The Middle is stepped:** two rings of single steps round it on every side, from the apron at 19 to its
  top at 22. It is attacked from four sides: two causeways and two parkour lines, and from below out of the
  Spring.
- **A side hill stands in an alcove.** Walls two blocks taller than the Rim close its two sides, and the Rim's
  face closes its back, so the Bench cannot see into it. Only its front is open, toward the Middle, and the
  Middle's top sees straight onto it.
- **A side hill has four ways in:** the front stair from the Ledge, the side stair and window in its west wall,
  the drop from the Rim behind it, and the Bench's pad landing by that side stair. The east wall has no way
  through, so each hill has a blind side and a side with a door.

## The Spring

**The room under the Middle is a crossroads as well as a larder.** Two stairwells come down into it from the
apron's west and east sides, and two glass tunnels leave it north and south under the pool. Each tunnel climbs
a trench of stairs onto the Ledge beside a side hill's front stair. The golden apples spawn in the middle of
the room, so every route through it passes them.

**The tunnels run under the water in glass.** A player in one sees the pool above, and a player on the
causeway sees them below.

## What `map.xml` will say

- `<king>`: three hills with a 5-second capture, a neutral start, no decay and points that do not grow. The
  Middle pays 2 a second and the side hills 1. First to 600, or the most points at 15 minutes.
- **Spawners:** golden apples in the Spring, one at a time, every 30 seconds; arrows in two diagonal inner
  corners of the Ledge, the north-east and the south-west.
- **No block interaction at all;** the kit is a stone sword, a bow, arrows, a golden apple and the conquest
  armour.
- **Pads:** each pad's region carries its velocity, and fall damage is denied until the player lands.
- **Spawns:** enemy entry denied; the spawn opens onto the Rim.

## Theme, decided now

- **A dimension-stone quarry:** walls cut in courses of diorite, polished diorite, stone and quartz, the
  bench faces drill-marked (a vertical line of andesite every few blocks), floors of polished stone and white
  dust (sand with a little gravel).
- **The pool:** clear water over a floor of diorite, so its depth reads.
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

## Decisions for you

1. **Scale.** The playable bowl is 90 × 82 inside the quarry wall, against Mush Pit's 70 × 87. Keep it, or
   tighten it by narrowing the Bench and the Rim to 6?
2. **The pool or the void.** I kept the pool you climb out of. Keep it, or make the low ground fatal?
3. **The side stair is in the west wall of the North hill,** and by the turn in the east wall of the South hill.
   Is one door each the right number, or should the blind side have one too?
