# Aerie — six crags, a strait, and no ground at all

> A small mixed board — a wool **and** a core to a team — chosen to build three things the studio had
> never been asked for here: a core, `teamTint`, and a board where every crossing is a bridge
> somebody builds.

**In one sentence:** three crags hanging in open sky at each end of the board — the spawn's, a bare
spire carrying the core, and a walled fold carrying the wool — with ten to sixteen blocks of nothing
between each pair and a **twenty-four block strait** between the two halves.

**72 × 128 blocks**, `rot_180` about the origin, ground from **y26 to y38** over void everywhere
else, **1,523 cells** of it, symmetry error **0**. Each crag is a slab ten courses thick.

## The gaps are the map, so they are what was drawn first

The first build put a fourth crag in the middle and left six-block gaps between everything, and the
critic answered on every pair: `G2` (a corridor under ten wide), `G5` (a hop outside 10–20) and
`CT12` on all nine straits. It was right. **A six-block gap is a running jump, not a crossing**, and
a board of nine crags and eight running jumps has no bridging in it at all.

| Strait | Blocks | |
|---|---|---|
| home → spike | 16 | `G5`'s 10–20 |
| home → fold | 10 | `G5`'s 10–20 |
| spike → fold | 16 | |
| **the strait** | **24** | `CT12`'s 15–40, and the only way to the other team |

Four build zones, one per gap, and nothing else on the board is buildable — `deny(void)` closes
everything outside a build area, so the zone list *is* the list of places a bridge may go.

## The core is forward and the wool is deep

The first build had it the other way round and `WL10` named it: a wool eight blocks behind the
frontline is the first thing an attacker lands on, which is not a capture board.

**A core is the one objective that wants to be contested.** It cannot be carried anywhere; it is
breached where it stands, so it belongs on the crag nearest the strait. The wool has to be fetched
and brought home, so it belongs behind. Swapping them moved `WL10` from 8 to **14** and made the
board read the way it plays.

| | Where | What |
|---|---|---|
| **the core** | the spike, `(-20, 20)`, y34 | 5 × 5 × 5 obsidian over lava, floating 6, `leak` 5 |
| **the wool** | the fold, `(20, 27)`, y26 | a 16 × 10 room, `@ae-fold` |
| the spawn | the home crag, `(0, 54)`, y30 | `@ae-lodge` |

**A core on a crag in open sky has nothing to catch its lava.** Escaping lava free-falls, and on this
board it falls forever — so a breach anywhere near the casing's edge is the end of it. That is why
the casing stands in the middle of its crag with eight blocks of rock all round: a hole punched on
the inward side spills onto its own stone, and only the outward faces are quick.

## `teamTint`, which is what a wool crag is for

`teamTint` resolves to the owning team's colour where a cell belongs to a team and to a stated
neutral where it does not — one material, both sides, no per-team theme. It is used twice:

- one course of stained clay in the **fold**'s surface stack, under the turf, so the wool crag is
  quietly its team's colour and a rim of it caps the edge;
- the top course of the fold room's own wall, so the pen says whose it is from a bridge.

Where a cell has no team it falls to podzol and mossy cobble, which is what the neutral is for.

## A `rim` mark is for a board whose islands are level with each other

The obvious way to make a crag *crown* — pin its edge a course under its middle — is a `rim` mark,
and it is the wrong instrument here: **it states one height for every island in the relief**, and
these three stand at 26, 30 and 34.

What works instead is `base`. Each crag's top is stated by an `area` over its plan rectangle, and its
polygon is drawn wider than that rectangle; the fringe between the two is unpinned and decays toward
`base`, which is set at **24 — under every crag**. So every edge falls a course or two before the
drop, on all three, at their own heights.

`rimEdges: "drop"` then caps that edge with coarse dirt, and the `wall` bucket paints what hangs
below it: turf, two soil, three stone, two andesite, three of a stone-cobble-gravel noise, two mossy
cobble. On a board of islands the underside is half of what anyone sees, so it is where the material
goes.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror and traversability clean —
*"spawn ↔ objective chain connected across the build geometry"*, which on this board means connected
by the zones and by nothing else.

Buildability reports **four placements over open void** — both spawns and both wools. They are on
solid crags; what is under the crags is void, because the crags are floating. It is the honest
reading of a sky board and not a fault.

The dressing pass takes 11 prop documents and **declines none**.

`GET …/coverage`: **6.1 % dead** — 185 of 3,046 cells, all of it the outward margins of the two
crags nobody has a reason to walk to the far side of.

`GET …/plan/flow`: the attacker walks **94** blocks to the wool and the defender **34**.

## Where it departs, and why

**`GO1` reads 2.02 on the core** (own 42, enemy 85). A forward objective is a low ratio by
construction, and that is what was chosen: the whole point of putting the core one strait from the
enemy is that it is fought over rather than defended. `GO1`'s band is written for a goal a team sits
on.

**`WL10` reads 14 against a band of 19.** The band is calibrated for full-size capture boards; here a
team's whole half is 52 blocks deep, and a wool fourteen blocks behind the front is proportionally as
deep as one forty blocks back on a 300-long map.

**Nothing stands on the spike or the fold.** A core's clearance takes most of a 24 × 16 crag and the
fold is a room with two blocks of margin round it — five props were declined `OB19` and `DR-KEEP`
before that was accepted. A bare spire and a walled pen are what those crags are; turf is all they
get.
