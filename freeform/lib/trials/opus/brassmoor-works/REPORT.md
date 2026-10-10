# Brassmoor Works — capture the wool

**An ironworks hung in the smog, its decks of stone-brick paving joined by iron.** Each team spawns at a gatehouse
over its marshalling yard. It keeps one wool in a boiler house and one under a water tower, at the far ends of two
lanes walled with bedrock, and crosses to the other works over a band of open air with a crane standing in it.
The board is 176 by 224 blocks, symmetric by a half turn, two wools a team, teams of sixteen.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/brassmoor-works --build <scratch>/brassmoor-works --skip write
```

The run takes about 95 seconds, nearly all of it the read-back's four voxel walks; generation takes under a
second.

## How it plays

**Each half is a hub with two lanes to two wool rooms behind it and two quays in front of it.** Red holds the
north. The Gatehouse (the spawn, at 70) stands at the back of the Yard (the hub, at 66), which has a void in its
middle, the Turntable Pit, so the hub can be crossed either side. From the Yard the Gantry runs west to the Boiler
House and the Spur runs east to the Water Tower. Two quays at 64 run forward to the band.

**The spawn stands on the line between its two wools.** The two rooms are 141 apart and the spawn is 10 off the
line between them, the interposed spawn `match-flow.md` §6.4 finds on 62 of 87 maps. A team's rotation from one
room to the other runs past its own spawn.

**The band is 22 blocks of build zone between the quays, with the Crane Island in its middle.** It is the only
join between the two works, as the look ruling asks: no corridor of land, only a crossing a team pays for. The
crane's tower and its jib stand on the island as the board's landmark.

**Each wool room is a brick hall at the end of its lane, three of its faces on the void.** The lane is the
funnel, 11 and 10 wide. A bedrock line, three high with a course of web, stands across each lane four blocks
before the room's door, the prepared line `approaches.md` asks for. The lane's edges are void, so nobody walks
round the line's ends.

**Each room has a second door on its south face, toward a build zone with a stepping stone in it.** The Boiler
Flats and the Tank Flats are build zones beside the rooms, each holding a heap (the Slag Heap, the Coal Stage) 12
blocks off the quay and 21 to 23 blocks off the room. A three-row strip along each lane is left out of the zone,
so a bridge cannot be run along the lane to step round the bedrock line.

### The ways onto a wool, and the walks

| Walk | Plan (octile; bridged blocks in brackets) | Target |
|---|---|---|
| Spawn to the band (SP10) | 88 | at least 55 |
| Spawn to its own monuments | 9, 8 | near and in sight |
| Spawn to its own Boiler House / Water Tower, red and blue | 72.3 / 68.9, the same for both | WL9: at most 1.25 apart (1.05) |
| Band to red's Boiler House, shortest | 81 (51) | WL10e: at least 59 |
| ... by the lane, over the bedrock line | 96 (40) | within 1.3 of the shortest |
| ... by the flats, by the Slag Heap | 81 (34) | within 1.3 of the shortest |
| Band to red's Water Tower, shortest | 76 (40) | WL10e: at least 59 |
| ... by the lane, over the bedrock line | 92 (32) | within 1.3 of the shortest |
| ... by the flats, by the Coal Stage | 76 (30) | within 1.3 of the shortest |
| Either room on foot, no block placed | none: the bedrock line stops it | none |
| Boiler wool to Water Tower wool, straight (WL7) | 141 | 46 to 143 |

**The two ways onto a room cost within a fifth of each other, so the defence has two lines to hold.** The lane is
the walk past the defenders' spawn and over a prepared line. The flats are two bridges, the second one long and in
full view of the room's south windows.

**The built world's walk, building, reaches each enemy wool in 227 and 232 moves from the spawn, for both teams.**
That walk lets a player stand in any build zone's air between the kill height and the build height, and counts
every block climbed, so it runs far over the plan's octile walk.

## Renders

| File | What it shows |
|---|---|
| `renders/00-plan-sketch.png` | the plan (v2): the board, the routes onto red's wools, two cuts, the flats way unrolled, the check |
| `renders/00-plan-sketch-v1.png` | the first plan, with the quays outside the Yard's width |
| `renders/05-topdown-annotated.png` | the built top-down with the plan's names and markers |
| `renders/30-iso-board-se.png`, `31-iso-board-nw.png` | the board from two corners, the smog under it |
| `renders/32-iso-red-half-sw.png` | red's works: the Gatehouse, the Yard, both lanes and rooms, the quays |
| `renders/33-iso-gatehouse-and-yard-se.png` | the spawn's canopy, the monuments, the steps, the rails and wagons |
| `renders/34-iso-boiler-house-and-gantry-se.png` | the Boiler House with its chimney, the gantry, the Slag Heap |
| `renders/35-iso-water-tower-and-spur-sw.png` | the Water Tower with its tank, the Spur, the Coal Stage |
| `renders/36-iso-band-and-crane-se.png` | the band and the crane |
| `renders/10-section-boiler-to-tower-z-78.png` | a cut through both rooms, both bedrock lines and the Yard |
| `renders/11-section-spawn-to-band-x-34.png` | a cut from red's Gantry to blue's Yard |
| `renders/50-elev-boiler-house-from-the-gantry.png` | the Boiler House's door face |

## Read-back

- **`Objectives.check`:** no problems; every wool is in its room and every monument slot is open over bedrock.
- **`audit.footing`:** 0 problems.
- **Ground over the kill height off the decks:** 62 columns, all the crane's jib at 88 over the band. It runs
  across the band, not toward the other team, so it is a perch somebody builds to and not a crossing.
- **Into a team's own rooms on foot:** not reached, because the team's own bedrock line stands in the lane; the
  defenders hold the line from their side and the map.xml keeps them out of their rooms anyway.
- **The studio's reader:** valid, 2 teams, 2 spawns, 4 wools, 4 spawners, 2 renewables, 2 kits, 12 apply rules, no
  issues.
- **The build:** 148,651 blocks, 8 tile entities (the banners and the rooms' chests).

## The plan

**The places on each half:**

| Place | What it is | Why a player goes there |
|---|---|---|
| The Gatehouse | the spawn deck at 70 under a canopy, the monuments on its front edge, iron to mine | the spawn; the monuments |
| The Yard and Turntable Pit | the hub at 66, rails, two wagons as cover, a void in the middle | every walk crosses it; the pit makes two ways round |
| The Gantry and the Boiler House | the west lane under a crane gantry, a bedrock line, a brick hall with a chimney | the first wool |
| The Spur and the Water Tower | the east lane at 64, a bedrock line, a brick hall with a tank on its roof | the second wool |
| The Quays | the front at 64, bollards and crate stacks | the way to the band |
| The Flats, the Slag Heap, the Coal Stage | build zones beside the rooms, each with a heap | the second way onto each room |
| The band and the Crane Island | the build zone between the teams, the crane | the crossing |

**The look.** Every deck is a built floor of stone brick, polished andesite, andesite and stone, a quarter each in
cells of three. The buildings are red brick with stone brick pilasters and iron-barred windows, so they never
read as the deck. Under each deck run girders of stone brick and brick with iron hanging at their crossings, and
piers go down into a smog of grey glass and wool far under the kill height. The accent is hazard stripes of yellow
and black clay on every edge a bridge leaves from, and the banners.

**The kill height is 50, the smog lies at 28 to 42, the build height is 92.** Block 36 marks every deck and
zone column at y 0, so the void filter lets a team build there and nowhere else.

## Decisions, and why

- **A built board, not a landscape.** A capture board's ground is structure; an ironworks makes its decks, lanes
  and rooms read as made things, and the half turn is the shape 74% of corpus boards take.
- **Rooms in the back corners with three faces on the void.** A room defended from its corner gives the defence
  lines to hold and the attack two to choose from; a room in a field gives neither.
- **A three-row strip kept out of each flats zone.** Without it, a bridge along the lane's flank walks round the
  bedrock line, which is the failure `approaches.md` names.
- **The jib kept over the band.** A crane without its jib is not a crane, and the jib runs along the band.

## What went wrong, and how it was found

- **The lanes met their rooms at a corner.** The first rooms sat behind the Yard's back edge, so each lane touched
  its room's corner by four rows. Printing the plan's heights round the Boiler House showed it; the rooms moved
  forward so each lane meets its room's face.
- **The flats were unreachable from the quays.** The flats zones stopped a column short of the quays' edges, so
  the plan's cheapest walk to the stepping stone went through the room and back out. The route's cells showed it.
- **The flats way cost 1.5 times the lane.** The check found it; the stepping stones and the south doors moved
  toward each other.
- **The quays stood outside the Yard's width.** Their head stairs were laid over the void and joined the Yard at a
  corner. The read-back's count of ground off the decks found 98 columns; the quays moved inside the Yard's width.
- **The wall-to-room distance read -5.** The checker's formula had its sign wrong; the plan was right.

## What the plan missed

- **That a piece joins the next one along an edge, not a corner.** A plan row "each join at least 4 cells wide"
  would have caught both the rooms and the quays before the sketch.
- **That a build zone must touch the floor a bridge starts from.** A row "each stepping stone reached from its
  quay by building" (the plan walk to it, not through the room) would have caught it.

## Friction log

### What the library lacked, written locally

- **A wall one block thick with a pattern.** `facade.extrude` takes a cell open on two sides as a corner, so a
  room's one-block walls get no pattern at all. The walls, pilasters and windows are a local loop.
- **The joins between pieces as a check.** `plangraph` walks a corner join as readily as an edge join; no measure
  says how wide each join is.
- **Zones with strips kept clear.** A zone is a box less a strip, both turned by hand through the symmetry
  (`common.image_box`); `Symmetry.point` turns each corner, which is right now that it keeps half blocks.
- **The capture rules as a table.** SP10, WL7, WL9, WL10e and the bays are each measured in the checker by hand; the
  Lantern Karst port measured the same rows the same way.
- **The build markers.** Block 36 at y 0 under every deck and zone column is one line, but it is the rule every
  capture board must follow and no library call says so.

### Bugs and surprises, with reproductions

**A waypoint walk can pass through its own target.** `common.via` (and any route priced by a waypoint) found the
cheapest way to the stepping stone through the room it was meant to reach. Nothing in `plangraph` offers a walk
that avoids a set of cells, so the fix was in the plan, not the measure.

**`facade.extrude` patterns nothing on a one-block ring:**

```python
from pgmvox import World, B
from pgmvox import facade as F
w = World(0, 0, 10, 10, sy=8)
ring = {(x, z) for x in range(1, 8) for z in range(1, 8) if x in (1, 7) or z in (1, 7)}
runs = F.extrude(w, ring, 1, 5, base=(B.BRICK, 0), faces_=[lambda s, r, t, H, n: ("accent", (B.STONE, 0))])
print(len(runs), sum(1 for y in range(8) for x in range(10) for z in range(10) if w.id(x, y, z) == B.STONE))   # 0 0
```

### What in the guide was unclear

- **What "WL10e: at least 59" is measured from.** The Lantern Karst port measures from the band's edge; the guide
  names the rule and not its start.

### Wanted, how hard, what it would take

| What I wanted | How hard it was | What a library or studio feature would need |
|---|---|---|
| Brick halls with pilasters and windows | 15 lines, after finding extrude does nothing | `facade.walls(cells, ...)` for walls one block thick, or `extrude` treating a ring's cells as faces |
| A capture board's rules measured | 120 lines of checker | `plangraph.capture_rows(R, zones, spawns, rooms, band)` giving SP10, WL7, WL9, WL10e and the bays |
| Joins measured | not done | `plan.joins(R)` listing each pair of touching pieces with the width they share |
| A walk to a waypoint that avoids its goal | not done | `dijkstra(edges, starts, avoid=cells)` |
| The build markers | 1 line | `objectives.BuildArea(mask)` stamping block 36 and writing the void filter together |

## After the playtest

**Every platform is now four blocks of stone brick under its floor with a bedrock layer under that.** Floors stay at their plan heights, and the slab went from two blocks (the floor and one brick) to four, with bedrock as the bottom course. The girders and iron bars hang from the bedrock instead of the slab, and the piers run up to it. A player cannot dig a deck away, since survival cannot break bedrock.

**Read back from the built world, all 8,154 deck columns and 108 stair cells carry it.** Each deck column holds four solid blocks from its floor down and bedrock under them, on both halves; the 60 columns where the plan's floor reads 66 are the Quays' head stairs at 65, which carry their stair, three brick and bedrock. The Crane Island, laid after the turn, has floor 66, three brick and bedrock at 62, and its tower's legs now stop under it. Objectives with a problem 0, footing problems 0.

**The wool rooms' chests are the studio's wool-room loot.** `props.wool_chests` is called once per room, before the half turn, with the inside box and the floor (68 for the Boiler House, 66 for the Water Tower), so each room has two stacked chests in each inner corner and the turn gives blue's rooms the same. That is 32 chests of 27 stacks each across the four rooms, where there were two small gear chests. Every chest faces along the axis of its room's door wall, and the turned chests read the opposite way round.

**Nothing the chests stand in front of is in their way.** The boilers along the Boiler House's back wall moved one block east (x -76 to -69) and the Water Tower's pumps two (x 63 to 66), so no corner chest faces a machine. The tower's south door moved from x 61-63 to 62-64, so its corner chest is not on the doorway's first cell. The wool, its spawner point and every door cell are clear of a chest.

**The walks are unchanged.** Spawn to its own monuments reads 9 and 8, and building across the band to the enemy's wools 217 and 212, the same as this board built before the change on the current library (the committed 0.10 figures were 232 and 227). The door move changed one plan-check row, the lane over the wall to the tower room, from 92 with 32 bridged to 95 with 3 bridged, and every row still passes. The written map.xml reads valid with no issues.
