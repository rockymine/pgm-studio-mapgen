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
| The Ledge | 16 | a ring 6 wide round the pool; the causeways leave from it |
| The apron | 19 | the Middle's island, 18 × 18, round the stepped hill |
| The Bench | 22 | a ring 8 wide; the side hills stand on it |
| The Middle | 22 | 8 × 8 on top of two rings of steps, the golden apples under it |
| The side hills | 23 | 8 × 8, one step up from the Bench, the whole Bench wide |
| The Rim | 28 | a ring 8 wide round the top; the spawns open onto it |
| The wall | 40 | the quarry face round everything; nobody leaves the bowl |

**The board is 120 × 96, and blue's half is red's turned half a circle.** Red spawns in the west wall and
blue in the east. Turning makes the North hill the side hill nearer red's tunnel and the South hill blue's,
while both side hills stay 74 to 75 blocks from either spawn on foot.

## The routes, and what each is for

**Every route has a job, and a moment in the match when it is the right one.** Lengths are red's, walked on the
plan by `scripts/plan_check.py`; blue's are the same turned.

| Route | Length | One way? | What it is for, and when it is used |
|---|---|---|---|
| **The main lane:** Rim notch, Bench well, causeway, apron | 50 to the Middle | no | the straight push onto the Middle at the start and after a wipe; the causeway is four wide, so it is also where a held Middle is defended |
| **The Bench round** | 73 to either side hill | no | the safe walk to a side hill along the Bench, under the Rim's eye; how a team that does not hold the Middle reaches a side hill |
| **The tunnel** to the Ledge's corner, then the side stair | 70 to the near side hill | no | the covered way to your near side hill, arriving on its flank from below; the route for a team under fire from the Rim |
| **The Rim, dropping onto a side hill** | 92 | yes, the drop is 5 | the high flank: long, but it ends on top of the hill's holders from above; the route when the hill is held and the Bench is watched |
| **The pad from the apron** to a side hill's flank | 29 from the Middle | yes | the rotation from the Middle to a side hill in 17 ticks; how the team holding the Middle contests a side hill without giving up the Middle |
| **The parkour:** two pillars from the Ledge onto the apron, gaps 2, 2 and 3, each a block higher | 29 from a side hill | no, but up is the point | the side hill's way back to the Middle, fast and exposed over the pool; a miss is a swim |
| **The pad from the Ledge's corner** up to the Rim's corner | 92 via the tunnel to a hill | yes | the way out of the low ground: from the tunnel's mouth or a ladder, up to the Rim and onto a drop |
| **The drops** from the Rim to the Bench, 6, all round | — | yes | a flank anywhere; costs a heart and a half of health, never a route back |
| **The ladders**, four a side out of the pool | — | up only | the price of falling off a causeway or missing the parkour |
| **The Spring:** two stairwells down from the apron to the golden apples under the Middle | — | no | the holders' regeneration; the attackers' reason to dive under the hill |

**The Middle is the hub, as it should be in King of the Hill.** The shortest way from a spawn to a side hill
is through the Middle and its pad (64), and a side hill's quickest way to the other is through it as well
(57 to 59). Holding the Middle is the rotation, not only the points.

**The jumps are only the ones planned.** The checker looks for every gap of one to three blocks a player can
cross landing no higher than a block up, and finds the parkour's six jumps on each side and nothing else.
No ledge or corner of the bowl gives a jump the plan did not draw.

**The pads were tuned in the simulator.** Each was given a target, and a search over velocities found one that
lands within a block of it.

| Pad | Velocity | Lands | Flight |
|---|---|---|---|
| apron to the North hill's flank | −0.62, 0.85, −2.42 | the Bench at (−13.5, −29.5), y 23 | 22 out, 17 ticks, apex 24.4 |
| Ledge corner to the Rim | −1.33, 1.55, −1.43 | the Rim at (−40.4, −37.4), y 29 | 19 out, 22 ticks, apex 29.9 |

Neither pad lands lower than it starts, so neither costs fall damage. The XML will still clear fall damage
after a pad as Mush does, in case a player is pushed off course.

## The hills

- **No cover on a hill.** Each is an 8 × 8 top of polished stone with a ring of wool that shows who holds it.
  It is held with players, and fought for from the steps round it.
- **The Middle is stepped:** two rings of single steps round it on every side, from the apron at 19 to its
  top at 22. It is attacked from four sides: two causeways and two parkour lines.
- **The side hills stand one step above the Bench,** with the Rim six over them on the outside and the Ledge
  seven under them on the inside. A side hill is attacked along the Bench from either end, from below by the
  side stairs, from the pad, and from above by the drop.

## What `map.xml` will say

- `<king>`: three hills with a 5-second capture, a neutral start, no decay and points that do not grow. The
  Middle pays 2 a second and the side hills 1. First to 600, or the most points at 15 minutes.
- **Spawners:** golden apples in the Spring, one at a time, every 30 seconds.
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

## Decisions for you

1. **Scale.** The playable bowl is 90 × 82 inside the quarry wall, against Mush Pit's 70 × 87 and Mush's 109.
   I can tighten it by narrowing the Bench and the Rim to 6. Keep it, or tighten?
2. **The pool or the void.** I chose a pool you climb out of over Mush Pit's void. Keep the pool, or make the
   low ground fatal?
3. **The Rim route is long (92).** It is the high flank and ends on top of the hill. Is that right for a flank,
   or should the spawn open a second door straight onto the north and south Rim?
4. **The Middle from a side hill** is reached only by the parkour or a long walk. Should a causeway run north
   and south too, or is the parkour the right price?
5. **Four pads against Mush's ten.** Should the side hills have pads back to the Middle as well, or should the
   way back stay on foot?
