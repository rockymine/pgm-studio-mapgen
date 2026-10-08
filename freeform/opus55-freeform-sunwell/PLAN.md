# Sunwell — the plan

A water drop board, planned and waiting on a review before anything is built. Players race down a jungle sinkhole
two hundred blocks deep, from shelf to shelf, to the lake at its foot. Every drop is twenty-two blocks and kills
unless it ends in water: a pool hit, a bucket placed in time, or the waterfall ridden down. The first player to
reach the lake three times wins.

![plan sketch](renders/00-plan-sketch.png)

## What the water drop maps in PublicMaps do

**Eight of the arcade maps are this game, built in two ways.**

- **Sunrise over Paradise** is a chain of floating islands falling from y 206 to 23, about twenty at a time,
  mirrored about its middle. Its islands carry no water: every landing is a bucket placed on the way down.
- **Water Drop II** is one glass shaft, about 250 tall, whose walls step in and out as it falls.

**The rules are nearly the same everywhere.**

- **Kit:** three water buckets, locked in place. Some maps swap them for barriers outside the drop areas and give
  them back inside.
- **Health:** fall damage is on, often with two hearts taken away (`health boost -2`), so a fall of about
  nineteen kills.
- **Placing:** water may be placed and taken back up, block physics are off so it never flows, and nothing else
  can be built.
- **Winning:** a score box at the foot gives a point and a portal sends the player back to the top. The limit is
  one, two or three points; Sunrise is three.
- **Resetting:** in some maps a locked potion of harming kills a player stuck on a ledge.

## The fall, in numbers

**A drop's targets are placed by how far each way of leaving an edge carries a player.** I modelled Minecraft
1.8's fall a tick at a time: gravity, air drag, and the push of a sprint or a jump. Over a drop of twenty-two:

| Way of leaving the edge | Carried out | Fall time |
|---|---|---|
| stepping off | 1.3 | 1.35 s |
| running off | 7.3 | 1.35 s |
| sprint-jumping | 10.7 | 1.60 s |

**A player can always land short of their reach by letting go, never beyond it.** So the near side of a pool
decides the gentlest way that hits it. A pool one to three out takes a careful step; one four to seven out a run;
one eight to eleven out a sprint jump, and nothing further is reachable.

**Unbroken, the fall does nineteen damage against sixteen health.** Every drop on the board is one that kills.

## The board

**The shaft is round, 43 across, and 200 deep.** Nine shelves, four blocks thick, jut from alternate sides,
twenty-two apart from 236 down to 60. Each runs to just past the shaft's middle, so it overhangs the next by five.
The lake fills the foot at 38.

**A player drops off a shelf's edge, lands on the shelf below, walks back under the overhang to that shelf's edge,
and drops again.** The edge is walled by a low rim, open only where something lies beyond: a pool, a shaft or
the falls. Crossing the shelf to the opening you want is part of every choice.

| What lies beyond an opening | What it takes | On a miss |
|---|---|---|
| **a near pool**, 3 × 3, one to three out | a careful step off | death |
| **a middle or far pool**, 5 × 4, four to eleven out | a run, or a sprint jump | death |
| **the bare shelf** | a bucket placed under you as you land | death |
| **the falls**, down the side wall into a basin | riding falling water down: safe, about five seconds a drop | — |
| **a shaft**, a 3 × 3 hole through the shelf below | a run or a sprint jump into the hole, then braking in the air over a 7 × 7 pool two shelves down, 66 below | death |

**The pools and shafts move from drop to drop.** The near pool sits left of the middle on one shelf and right on
the next, so the quickest line crosses each shelf. The falls change wall every drop. Each shaft's pool is a pool of
the shelf it lands on, so a player who takes a shelf the slow way can still use it.

## What a lap costs

**Each habit has its own lap, top to lake.** The checker takes the quickest line for each, choosing the opening at
every drop, walking across and back under each shelf (`renders/plan-check.txt`):

| Habit | A lap |
|---|---|
| the falls every time | 101 s |
| the pools every time | 30 s |
| the bucket every time | 23 s |
| the bucket, and every shaft | 19 s |

**The safe way is five times slower than the bucket.** That is the game: a player who cannot place a bucket under
pressure can still finish, and one who can wins. The shafts are the last four seconds, for whoever threads a
hole twenty-two down and then stops their drift over the pool beneath.

**Nothing overlaps.** Every pool, hole and basin is on its shelf, beyond the edge above it, and clear of every
other one.

## The match

| Setting | Value |
|---|---|
| players | free for all, up to 30 |
| kit | three water buckets, locked; given back on every shelf; sixteen health; three seconds of resistance at spawn |
| placing | water only, anywhere below the top shelf; it never flows; nothing else |
| winning | the lake scores a point and sends a player back to the top shelf; three points wins; a seven-minute clock, the most points winning if it runs out |
| dying | back to the top shelf, at once |

## What I would like a ruling on

- **The theme.** A cenote in the jungle: a sinkhole whose rim is forest, with roots and vines hanging down the
  walls, waterfalls pouring in, ruins on the shelves, and sunlight falling to the lake.
- **Placed water.** In the PublicMaps maps it stays where it was placed, so a puddle left on a shelf saves the next
  player. A renewable can wash it away after some seconds. Leave it, or wash it away?
- **Three laps**, as Sunrise has, with the falls always there for anyone who wants to finish.
