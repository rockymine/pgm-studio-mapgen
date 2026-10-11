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

**The third review set the widths.** Lanes are 12 to 16 wide, gaps between steps about 12, the pillar
14 to 18 off everything, and every hole between 14 × 16 and 40 × 40.

| The review said | What changed |
|---|---|
| The Store Road and its ways in are too thin | The Store Road is 14 wide (was 10); the Tea Rows and the Drying Floor are 12 (were 8) |
| The Long Terrace 14, its Arms 10 | The Long Terrace is 14 (was 10), the Arms 10 (were 6) |
| The pillar 14 to 18 off | 16 off each Arm and off the Terrace (were 13, 13 and 18) |
| The Arms and the pit run past the pillar into space no one uses | Both now end level with the pillar's far side |
| Holes 14 × 16 at least, 40 × 40 at most | The sinkhole is 16 × 16, the void inside the Store's F 16 × 18, the Pillar's pit 40 × 24 |
| Steps about 12 apart, and further toward the middle | All gaps between steps are 11 or 12 (were 6); each chain's first column stands over the band's end |
| Two more steps in front of the pillar, twenty down, a secret way | The West and East Ledges at 46, three blocks off the pillar's foot; drop, then pillar up |

**The fourth review trimmed the Ledges and widened the band again.**

| The review said | What changed |
|---|---|
| No pool on the Ledges: players carry water buckets, and the drop is the skill | The pools are gone; the kit carries a water bucket |
| The Ledges reach too far toward the pillar; half the length | 6 × 7 each (were 6 × 13), 8 off the pillar's foot |
| Widen the band to the middle of each chain of steps | The band is 114 wide (was 100), ending between each chain's two columns |

**The board grew to hold the widths: 224 × 256 blocks (was 192 × 224).** The Tea Landing is gone, because
the wider Tea Rows now stand right over the first Tea Step.

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

**Capture the wool, two wools a team, sixteen a side.** The board is 224 × 256 blocks. Red holds the north
and blue the south, and blue's half is red's turned half a circle. So on each side of the board one team's
Pillar faces the other team's Tea Store: the west side carries red's Pillar and blue's Store, the east the
reverse.

## The pieces (red; blue's are the half-turn)

Width is across the way a player walks, length along it.

| Piece | Width × length | Floor | What it is |
|---|---|---|---|
| The Pavilion of Arrival | 20 × 10 | 74 | the top terrace: a two-storey pavilion, its hall open to the terrace below |
| The Pool Terrace | 32 × 12 | 72 | the spawn point; a one-deep pool with stepping stones, a karst outcrop with a pine |
| The Monument Terrace | 40 × 12 | 70 | the monuments between the two exits, tea beds, a lantern tower at each end |
| The West and East Lantern Steps | 12 × 8 each, 16 apart | 68 | the spawn's two exits, a block a step down to the hub: one toward the Pillar, one toward the Store |
| The Tea Court | 64 × 40, a ring round a 16 × 16 sinkhole | 66 | the hub: 12 of ground in front of and behind the sinkhole, 24 at each side |
| The Gate Terrace | 56 × 12 | 65 | the frontline's bar, a gate pavilion over its middle |
| The West and East Stairs | 18 × 15 each | 64 | the frontline's legs down to the band, 20 of void between them |
| The band and the Bell Rock | 114 × 22 of void, a 10 × 10 islet | 68 | the build band across the chasm; a bell pavilion on the islet |
| The Long Terrace | 14 × 60, west out of the hub | 66 | the Pillar's F, its long stroke |
| The Near and Far Arms | 10 × 24 each | 67 | the F's short strokes, ending level with the pillar's far side; the Near Arm touches the hub |
| **The Pillar Shrine** | 8 × 8 on a pillar | 74 | **lime wool**: an open shrine, 16 off each Arm and off the Terrace, 7 above |
| The West and East Ledges | 6 × 7 each | 46 | the secret way: twenty below the Terrace's edge, 8 off the pillar's foot |
| The Mist Steps | four 6 × 6 islets, 12 apart | 63–65 | the Pillar's flank: from the band's west end onto the Long Terrace |
| The Tea Rows | 12 × 18, east out of the hub | 66 | the Store's F, its south short stroke |
| The Drying Floor | 12 × 18, east out of the hub | 67 | the Store's F, its north short stroke; tea laid out on mats |
| The Store Road | 14 × 58, north | 66 → 70 | the F's long stroke: flat past the Rows, then a block every nine |
| The bedrock wall | 14 across the road, 2 thick, 3 of bedrock and 1 of cobweb | — | the Store's entry line, 3 after the Drying Floor joins and 13 before the room |
| **The Tea Store** | 20 × 14 at the road's head | 70 | **yellow wool**: a timber storehouse, two faces on void, chests of better gear |
| The Tea Steps | two 6 × 6 islets, 12 apart | 64–65 | the Store's flank: one under the Tea Rows, one under the road's foot |

**The monuments stand on the Monument Terrace between its two exits**, where a carrier coming home
cannot miss them: lime on the left, yellow on the right.

## The spawn, in relief

**The spawn climbs from the hub in three terraces, two blocks apiece, so it reads as a place and not a
yard.** A player arrives on the Pool Terrace at 72 and looks down over the Monument Terrace to the hub.

- **The Pavilion of Arrival** stands on the top terrace at 74: two storeys of spruce and dark oak, its roof
  ridge at 84, its hall open to the terrace below.
- **The Pool Terrace** carries a pool one block deep with a path of stepping stones across it, and a karst
  outcrop four high with a pine on top.
- **The Monument Terrace** carries the two monuments, beds of tea either side of the monuments, and a lantern
  tower at each end. The west tower looks out over the Pillar, the east over the Store.
- **Each terrace edge is a step of one block or a stair**, so the spawn is walked straight down with no
  jumps.

## The two wools

**The Pillar Shrine floats between the two arms of an F.** The Long Terrace leaves the hub's west face, and
the Near and Far Arms run back from it as far as the pillar's far side. The pillar stands in the pit between
them, which is a build zone, so a bridge may start from either Arm or from the Terrace.

**Its three bridges are 16 blocks each, and then 7 blocks up.** The Near Arm also touches the hub, so the
shortest attack walks out of the hub's corner and bridges 16. The Far Arm is the long way round, along the
Long Terrace.

**The Ledges are the secret way.** Two small shelves of karst stand twenty blocks below the Terrace's edge,
either side of the pillar and eight blocks off its foot. An attacker drops onto one, saves the fall with a
water bucket placed as they land, and builds up and across to the shrine in full view of the Arms.

**The drop is the skill.** There is no pool: a player who misses the bucket dies of the fall.

**The Mist Steps are the Pillar's fourth way in.** Four islets on a grid, 12 apart, climb from the band's
west end onto the Long Terrace, and the attacker who takes them never passes the hub.

**The Tea Store stands at the head of a short road with three ways onto it.** The Tea Rows and the Drying
Floor both leave the hub's east face and meet the Store Road, with 16 of void between them, so the attacker
chooses a side as at the hub. The Tea Steps bring a third way from the band's east end, onto the Rows or
the road's foot.

**All three meet at one wall, thirteen blocks before the room.** The wall is where an attacker enters:
once past it they are in the Store's yard, with the room's door ahead and a redstone line across it.

**The two are balanced by distance.** By walking the plan (octile, land, a build zone bridged at its
length; the Ledges left out, since they are reached by a fall):

| Measured | Lantern Karst | Rule |
|---|---|---|
| spawn to the band | 98 | SP10: at least 55 |
| spawn to the Tea Store, walked | 85 | WL9: comparable |
| spawn to the Pillar (17 of it bridged) | 79 | WL9: comparable |
| their ratio | 1.08 | WL9: ideal 1 |
| band to the Tea Store, shortest (27 of it bridged) | 86 | WL10e: at least 59 |
| band to the Tea Store, walked | 100 | — |
| band to the Pillar, shortest (64 of it bridged) | 80 | WL10e: at least 59 |
| Pillar to Tea Store, straight | 120 | WL7: 46 to 143 |
| Pillar to the Arms and the Terrace | 16, 16, 16 | WL20: at least 12 |
| the Ledges | 20 down, 8 off the pillar | — |
| the Store Road alone, after its last join | 18 | — |
| the Tea Court's sinkhole | 16 × 16 | LN6: at least 12 |
| the void inside the Store's F | 16 × 18 | LN6: at least 12 |
| the Pillar's pit | 40 × 24 | — |
| the void between the Stairs | 20 | WL12: at least 16 |
| the void from the spawn to the Near Arm | 12 | — |
| the gaps between steps | 11 to 12 | — |
| land on red's half | 7,946 blocks | — |

`scripts/plan_check.py` prints this table from the plan's polygons.

## Heights, the void and the foundation

- **The base is y 64.** The Ledges are at 46, the hub at 66, the spawn climbs to 74, the Store is at 70 by the road's climb,
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

**The build zones are outlined below the board, as the studio's generator does it.** An unpowered redstone
line lies at y 1, two blocks out from every void-facing edge of a build zone and one block clear of the zone
and of the islands, turning at the corners. It is read from below or in an editor, never from the play
surface.

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
- **The kit:** sword, bow, pickaxe, axe, shears, wood and team-coloured wool for bridging, a water bucket
  and a golden apple. The rooms' chests hold better armour, as the account says a room should.

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

**The last change before building gave the spawn two exits.** The single neck became the West and East
Lantern Steps, 12 wide each with 16 of void between them, so a player picks the exit nearer the wool they
are going to. The spawn now stands on the hub at two points instead of hanging from one.

## Decisions for you

None open. The author's go is to build after this revision.
