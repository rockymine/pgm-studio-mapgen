# Lantern Karst — the plan

A capture-the-wool board, planned and not yet built. This is the second version, after the author's review
of the first; it is for a go or no-go.

## The board in one sentence

**Karst pillars stand in a void of mist, terraced for tea and hung with lanterns. Each team defends two
wools, each reached more than one way: the Pillar Shrine on a pillar floating between the two arms of an F,
and the Tea Store at the head of a short road that two terraces and a chain of islets all feed.**

What a player remembers: the shrine on its pillar with bridges reaching for it from three sides, the
lanterns along the Store Road, and the Bell Rock in the middle of the chasm where the staircases meet.

![plan sketch](renders/00-plan-sketch.png)

The first version's sketch is `renders/00-plan-sketch-v1.png`, drawn by `scripts/sketch_v1.py`.

**How to read the sketch.** The number on each piece is its floor height in blocks (y). Yellow dots are
void that may be built over; everything dark without dots cannot be. The table in the second panel is the
walking distances below, each with the rule it is held to.

## How the plan changed

| The review said | What changed |
|---|---|
| The spawn is large, so it cannot be flat | Three terraces up from the hub (70, 72, 74), a pool, a karst outcrop and two lantern towers |
| The Store is too isolated: a long L that ends in a choke, with one way in | The road is the long stroke of an F; two terraces reach it from the hub and two islets from the band |
| Pull the Store in by about 16 | The room moved in 18; its road alone, after the last way joins it, is 8 blocks |
| The Pillar's area is too big; make it an F of three rectangles | The Long Terrace and two Arms; the pillar floats between the Arms |
| The flank should land on the F's long stroke and be more grid-like | The Mist Steps are four islets on a 12-block grid, 6-block gaps, onto the Long Terrace |
| Bring the frontline closer, legs wider and shorter | The Stairs are 18 wide and 11 long (were 12 by 19); the bar is 8 nearer the band |
| Steps like the Mist Steps would also suit the Store Road | The Tea Steps, two islets from the band's east end to the road's foot |
| A floating map needs a bedrock floor and an obvious build area | A bedrock course under every island; block 36 at y 0 under every buildable column |

**The second review joined the steps to the band and the Rows.**

| The review said | What changed |
|---|---|
| The band meets each chain of steps only at a corner, which cannot be crossed well | The band is 96 wide (was 80); it runs under the first column of steps on each side and shares an edge with their zone |
| The Tea Steps' zone meets only the Store Road | The zone is widened west to meet the Tea Rows along 14 blocks |
| Add a small piece off the Tea Rows to step onto | The Tea Landing, 6 × 3 off the Rows, in line with the first Tea Step and 6 from it |

**No lane on the board is longer than 46 blocks, and none is a dead end.** The longest is the Long Terrace,
and both its ends lead somewhere: the Near Arm meets the hub, and the Far Arm stands over the pit.

## What already exists, and what I took from it

**I read the account of how capture matches are played and the rules the generator holds capture boards
to.** The account is `pgm-studio/docs/gameplay/match-flow.md`, measured over 333 recorded matches. The rules
are `generator/rules.md` (SP, WL, LN, HB) and `gameplay/approaches.md`. Six community capture maps were
rendered from their region files and read.

| Map | What it does with its wools |
|---|---|
| Celestial Islands | island chains in the void; each wool on an isolated island at the end of a chain; spawns on ships |
| Chles Great Wall | radial symmetry; four round pods off a central spine, two wools a team, each pod reached by one arm |
| Geometric Domination | compact; an L-shaped lane to each wool ending in a narrow corridor; a half-disc in the middle |
| Bridgid II | a grid of square blocks; wools in the corners, two faces on void |
| Golden Drought VI | an H: two long lanes per team, a wool at each lane's end, the spawn between them, bridges across the middle |
| After Hours | a short board, two wools per team at the ends of their lanes |

**The account's lessons decided the plan.**

- **The late game is in the sky.** Teams staircase up from the band, a sky network forms at the build
  height, and the ground stops mattering once a wool's defenders have dug their pit. So the board's voids
  should be the kind that stay uncrossable at any height except where a build zone says otherwise.
- **A void in the hub buys a choice.** A ring hub lets an attacker take the far side and cross only 37% of
  the defender's lane instead of 76%. The Tea Court is a ring for that reason, and the Store's F is a second ring.
- **A two-legged frontline gives more attack routes.** 97% of objectives behind one have more than one way
  in, against 38% behind a plain bar. The Gate Terrace stands on two wide Stairs for that reason.
- **The arrangement the built maps converge on** is spawn at the back, wools left and right. That is this
  board's arrangement.
- **The rules this plan is held to:**
  - a room in a corner with two faces on void;
  - one bedrock wall per approach, narrow enough to be a line;
  - every gap beside a goal 16 or more across, so it cannot be jumped;
  - approaches climbing a block at a time;
  - wools comparably far from the spawn, at least 59 from the band, 46 to 143 apart;
  - the spawn at least 55 from the band.

**What I am adding that the survey does not have:** a wool on a pillar floating between the two arms of an F,
bridged to from three sides, beside a wool at the head of a short road that three ways feed. Both have more
than one way in; they differ in where the ways meet. The Pillar's meet only at the shrine, the Store's at
one wall eight blocks before the room.

## Mode and size

**Capture the wool, two wools a team, sixteen a side.** The board is 192 × 224 blocks. Red holds the north
and blue the south, and blue's half is red's turned half a circle. So on each side of the board one team's
Pillar faces the other team's Tea Store: the west side carries red's Pillar and blue's Store, the east the
reverse.

## The pieces (red; blue's are the half-turn)

| Piece | Footprint | Floor | What it is |
|---|---|---|---|
| The Pavilion of Arrival | 18 × 8 | 74 | the top terrace: a two-storey pavilion, its hall open to the terrace below |
| The Pool Terrace | 28 × 10 | 72 | the spawn point; a one-deep pool with stepping stones, a karst outcrop with a pine |
| The Monument Terrace | 36 × 10 | 70 | the monuments either side of the steps, tea beds, a lantern tower at each end |
| The Lantern Steps | 10 × 8 | 68 | the spawn's neck, a block a step down to the hub |
| The Tea Court | 60 × 32 ring round a 16 × 14 sinkhole | 66 | the hub: tea terraces, a well, lanterns; every crossing has a near and a far side |
| The Gate Terrace | 56 × 10 | 65 | the frontline's bar, a gate pavilion over its middle |
| The West and East Stairs | 18 × 11 each | 64 | the frontline's legs down to the band, 20 of void between them |
| The band and the Bell Rock | 96 × 22 of void, a 10 × 10 islet | 68 | the build band across the chasm; a bell pavilion on the islet |
| The Long Terrace | 46 × 10 west out of the hub | 66 | the Pillar's F, its long stroke |
| The Near and Far Arms | 6 × 32 each, back from the Terrace | 67 | the F's short strokes; the Near Arm also touches the hub |
| **The Pillar Shrine** | 8 × 8 on a pillar | 74 | **lime wool**: an open shrine, 13 off each Arm, 18 off the Terrace, 7 above |
| The Mist Steps | four 6 × 6 islets on a grid | 63–65 | the Pillar's flank: from the band's west end onto the Long Terrace |
| The Tea Rows | 18 × 8 east out of the hub | 66 | the Store's F, its south short stroke |
| The Drying Floor | 18 × 8 east out of the hub | 67 | the Store's F, its north short stroke; tea laid out on mats |
| The Store Road | 10 × 43, north | 66 → 70 | the F's long stroke: flat past the Rows, then a block every five |
| The bedrock wall | 10 across the road, 4 high | — | the Store's prepared line, 3 after the Drying Floor joins and 4 before the room |
| **The Tea Store** | 16 × 13 at the road's head | 70 | **yellow wool**: a stone storehouse, two faces on void, chests of better gear |
| The Tea Steps | two 6 × 6 islets | 64–65 | the Store's flank: from the band's east end to the road's foot |
| The Tea Landing | 6 × 3 off the Tea Rows | 66 | where the first Tea Step leads, so a climber need not go to the road |

**The monuments stand on the Monument Terrace either side of the steps**, where a carrier coming home
cannot miss them: lime on the left, yellow on the right.

## The spawn, in relief

**The spawn climbs from the hub in three terraces, two blocks apiece, so it reads as a place and not a
yard.** A player arrives on the Pool Terrace at 72 and looks down over the Monument Terrace to the hub.

- **The Pavilion of Arrival** stands on the top terrace at 74: two storeys of spruce and dark oak, its roof
  ridge at 84, its hall open to the terrace below.
- **The Pool Terrace** carries a pool one block deep with a path of stepping stones across it, and a karst
  outcrop four high with a pine on top.
- **The Monument Terrace** carries the two monuments, beds of tea either side of the steps, and a lantern
  tower at each end. The west tower looks out over the Pillar, the east over the Store.
- **Each terrace edge is a step of one block or a stair**, so the spawn is walked straight down with no
  jumps.

## The two wools

**The Pillar Shrine floats between the two arms of an F.** The Long Terrace leaves the hub's west face, and
the Near and Far Arms run back from it. The pillar stands in the pit between them, which is a build zone, so
a bridge may start from either Arm or from the Terrace.

**Its three bridges are 13, 13 and 18 blocks, and then 7 blocks up.** The Near Arm also touches the hub, so
the shortest attack walks out of the hub's corner and bridges 13. The Far Arm is the long way round, along
the Long Terrace.

**The Mist Steps are the Pillar's fourth way in.** Four islets on a grid climb from the band's west end
onto the Long Terrace, 6-block gaps each, and the attacker who takes them never passes the hub.

**The Tea Store stands at the head of a short road with three ways onto it.** The Tea Rows and the Drying
Floor both leave the hub's east face and meet the Store Road, with 16 of void between them, so the attacker
chooses a side as at the hub. The Tea Steps bring a third way from the band's east end, to the road's foot or to the Tea Landing on the
Rows.

**All three meet at one wall, eight blocks before the room.** That is the Store's prepared line, as a
capture room has one. What the first version lacked is that there are three ways to the line, and that the
line is near the room.

**The two are balanced by distance.** By walking the plan (octile, land, a build zone bridged at its
length):

| Measured | Lantern Karst | Rule |
|---|---|---|
| spawn to the band | 82 | SP10: at least 55 |
| spawn to the Tea Store, walked | 80 | WL9: comparable |
| spawn to the Pillar (13 of it bridged) | 75 | WL9: comparable |
| their ratio | 1.07 | WL9: ideal 1 |
| band to the Tea Store, shortest (12 of it bridged) | 62 | WL10e: at least 59 |
| band to the Tea Store, walked | 78 | — |
| band to the Pillar, shortest, by the Mist Steps (37 of it bridged) | 61 | WL10e: at least 59 |
| Pillar to Tea Store, straight | 106 | WL7: 46 to 143 |
| Pillar to the Arms and the Terrace | 13, 13, 18 | WL20: at least 12 |
| the Store Road alone, after its last join | 8 | — |
| the Tea Court's sinkhole | 16 × 14 | LN6: at least 12 |
| the void inside the Store's F | 16 | LN6: at least 12 |
| the void between the Stairs | 20 | WL12: at least 16 |
| the void from the spawn to the Near Arm | 12 | — |
| the Mist Steps' and Tea Steps' gaps | 6 each | — |
| land on red's half | 5,634 blocks | — |

`scripts/plan_check.py` prints this table from the plan's polygons.

## Heights, the void and the foundation

- **The base is y 64.** The hub is at 66, the spawn climbs to 74, the Store is at 70 by the road's climb,
  and the Pillar's top is at 74.
- **The build height is 92**, 28 over the base, room for the staircases and the sky network the late game
  is played on.
- **Below y 40 a fall kills**, by the instant-damage kit Stratum uses. A mist of glass lies at 28 to 38, so
  the void reads as depth rather than as nothing.

**Every island stands on a course of bedrock six blocks under its floor.** A defender who digs a pit in
front of a room stops there, so no lane is dug down to nothing. The karst goes on below the bedrock to the
mist, tapering, as rock no one plays on.

**Every column a player may build in carries block 36 at y 0.** PGM's void filter reads the block at
`(x, 0, z)`, and a column with block 36 there is not void. So the block 36 sheet is the build area, laid
under the islands and the four build zones and nowhere else.

**The build zones are drawn on the islands as well.** Where an island's edge meets a build zone, a line of
redstone runs along the edge's last row of blocks. A player standing at it knows the void ahead can be
bridged, and an edge with no line cannot.

**The four build zones are** the band, the Pillar's pit, the Mist Steps and the Tea Steps.
The Court's sinkhole, the void inside the Store's F, the void between the Stairs and the void round the
spawn stay uncrossable all match. That is the rule the account says makes a void's choice last.

## What `map.xml` will say

- `<wools>`: blue captures red's lime from the Pillar and red's yellow from the Store; red the reverse.
  `craftable="false"`.
- **Wool rooms:** a team may not enter its own rooms, and the rooms' blocks are protected. The Pillar's
  room is the shrine's top and the Store's room its interior.
- **Spawns:** entering the enemy's spawn is refused, and the spawn may not be edited.
- **Building:** `<void/>` denies placing where y 0 is empty, which the block 36 sheet decides. The bedrock
  courses and the wall cannot be broken.
- **The fall:** `<apply kit="fall-kill" region="the-fall"/>` on `<below y="40"/>`.
- **The kit:** sword, bow, pickaxe, axe, shears, wood and team-coloured wool for bridging, and a golden
  apple. The rooms' chests hold better armour, as the account says a room should.

## Theme and palette, decided now

- **Karst:** pillars of stone, andesite and a little mossy cobblestone, standing in mist. Their sides are
  ledged and hung with vines, and spruce grows on their tops and from their ledges.
- **Terraces:** tea in rows of leaves on grass, laid along the terraces' contours, with podzol paths between
  them.
- **Built:** pavilions of spruce and dark oak with roofs of dark oak stairs curved up at the eaves, and
  white and jade (prismarine) panels. Lanterns are glowstone hung from fences. Steps are stone brick and
  andesite.
- **Red and blue only on the teams':** banners on the Pavilion and wool rooms. The lacquer red of a real
  pavilion is left out, because it would read as a team.
- **The mist:** white and light grey stained glass far below, as Stratum's clouds.

## Decisions for you

1. **The two flanks are now the shortest ways from the band to each wool**, at 61 and 62 against a floor
   of 59. That is near the floor. Should the steps be pushed back a few blocks for margin?
2. **The arm nearest the hub touches it.** That makes the Pillar reachable straight from the middle, at 13
   blocks of bridge. Should that arm stand off the hub instead?
3. **The spawn is 12 blocks of void from the Near Arm.** An attacker there can shoot into the spawn's
   front terrace. Is that acceptable?
