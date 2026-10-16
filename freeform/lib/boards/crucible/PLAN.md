# Crucible — the plan

**Two foundries dug into facing volcanoes across a lava rift, each hanging its crucible from a gantry over a casting
pit in front of the mountain and keeping its dye stock in the one cold room at the foundry's deepest level.** A
player remembers the crucible on its chains over the pit, the cliff of bedded rock with the foundry's front built
into its foot, and the blue-green cold store at the bottom of the ramps. The data is `scripts/plan.py` and
`scripts/land.py`; this page says why each piece is where it is.

## 1. The arrangement

**The board is 140 by 200, one island in the void, turned half round about (−0.5, −0.5).** Red holds z ≥ 0 and
blue its image. From the middle outward each half is the lava rift, the slag plain, and the mountain, whose cliff
foot stands at z 58 and whose crest reaches about y 95 at the back edge.

**The two teams' ground is joined by the rift and nothing else.** The rift is 17 to 23 blocks rim to rim (median
19), with the lava sea at y 6 and the kill height at y 18. Its floor is rock under the lava, so every column of it
is ground to PGM's void rule and the whole width is a build zone.

**The spawn stands inside the mountain at the back.** Red's crew hall (spawn) is at level 0, x −8..8, z 72..88,
24 blocks into the rock behind the cliff, with ways out west to the loading gate and east to the pour room.

**The crucible is the forward objective and stands off to one side.** It hangs over the casting pit at (20..24,
46..50, 43..47), 34° off the line from red's spawn to blue's, in front of the foundry's east half.

**The wool is the deep objective.** Red's lime wool lies on a quartz plinth in the cold store at level 2 (feet 28),
under the mountain's back-west corner, three ways in and 222 blocks of walk from blue's spawn.

**The two goals are separate.** A team wins by leaking the other's crucible and placing the other's wool; the
crucibles' casing turns to gold at 15 minutes and glass at 20 so a held core still ends. The pit is the hinge
between them: its floor opens into the furnace hall, which is one of the ways to the store.

## 2. The numbers

| Measure | Value | Target |
|---|---|---|
| red's walk to its own crucible (plan, octile) | 53 | 40 to 90 (GO4) |
| blue's walk to red's crucible, the rift bridged | 148 | 85 to 150 (GO3) |
| the two, enemy over own | 2.79 | 3 to 4 (GO1): **missed**, see §6 |
| the crucible off the spawn-to-spawn line | 34° | 20° or over |
| red's spawn to its own monument | 24 | under 40 |
| blue's walk to red's wool | 222 | over the walk to the crucible (1.50×) |
| rift crossing, narrowest / median | 17 / 19 | 16 or more |
| tip's end to the far rim | 15 | 12 or more |
| ramp legs | 1 in 2 | 1 in 2 or gentler |
| rock over the shallowest room (loading hall) | 2 | 2 or over |
| crucible over the pit floor | 6 of air | 3 or over |
| where its lava lands | y 40 | at or under the leak line y 40 |
| nearest lava of the land to the crucible | 38 | over 15 |

**The leak is read off PGM, not guessed.** `CoreMatchModule` counts a lava block whose centre lies within ±15 of
the core's bounds and at or below `min.y − leak`, which is a block at `y ≤ min.y − leak − 1`
(`pgm-studio/docs/pgm/destroyables-and-cores.md`, OB2). The casing's floor is y 46 and the leak 5, so the line is
y 40. The pit's floor top is y 39, so lava let out of a breach lands at y 40 and leaks at once; nothing has to be
dug (float 6, leak 5: the corpus's default pair).

## 3. The levels and the ramps

| Level | Feet | Spaces |
|---|---|---|
| 0 | 52 | loading gate, loading hall, west corridor, crew hall (spawn), east corridor, pour link, pour room, loggia |
| 1 | 40 | the pit's floor and apron, the two pit doors, the furnace hall, the slag run |
| 2 | 28 | the store passage, the cold store, its two doors |

**Every change of level inside is a ramp of two legs at one in two, turning on a level landing.** The loading ramp
(L0→L1) is a U-turn in its own shaft west of the loading hall, a wall between its legs; the furnace ramp (L0→L1)
runs east from the east corridor and turns down along the furnace hall's east wall, a parapet on its open side;
the deep ramp (L1→L2) leaves the slag run south and turns west to the store passage.

## 4. The places and how each is reached

**The casting pit** is an ellipse 34 by 26 sunk 11 blocks into the plain at the cliff's foot. Its floor (y 39) is
paved as the foundry's floors are, with sand-filled moulds either side of the crucible; a haul ramp spirals down
its west wall from the plain at y 47 to the floor, and a bench at y 44 runs round its east side under the cone.

**The gantry** spans the pit at y 55 on a pier at its west end; its east end rests on the cinder cone's shoulder,
a single step from the cone's slope. The crucible hangs from its trolley on two iron chains, so the floating core
reads as hung, not floating.

**The crucible has four approaches, and they differ in direction.**

- *Around*: the haul ramp from the plain round the pit's west wall to the floor, in full view of the loggia.
- *Below*: the lava tube from the sinkhole on the plain (x −6, z 30, six deep), its walls glazed black, opening on
  the pit floor under the haul ramp's arch.
- *Above*: up the cinder cone's west flank onto the gantry, along the girder and down onto the casing's top.
- *Through*: the loading gate, the loading ramp, the slag run and the furnace hall's two pit doors; or the
  loggia's open end, the pour room and the furnace ramp.

**The defenders' places** are the loggia, an arcade over the pit at level 0 with a parapet a block high, and the
furnace hall behind the pit's apron. The crucible's top is in sight from the loggia.

**The cold store has three ways in.** The front door from the store passage (the deep ramp, from the slag run
either way: the loading gate or the pit); and the west door, where the flank cave arrives from the west spur's
face (x −60, z 45) after 55 blocks of descent through the beds with a chamber halfway. Its shell is kept from
digging by a zone, so the doors are the ways in.

**The monument** stands on the pour room's desk at (21, 53, 67), 24 blocks of walk from the spawn and in sight from
the loggia, so a carrier coming up from the pit finds it.

**The plain** carries the slag road from the loading gate to the tip, the pit's road to the tip, two slag heaps by
the road, two hornitos with glowing throats, the sinkhole, the cinder cone in the east and the black flow in the
west: a cooled lobe three blocks high with a lava channel down it, fed by a lavafall from the cliff and pouring
into the rift at the rim.

**The tip** is a dark oak trestle over the rift where the slag carts empty, five blocks out from red's rim, with
slag spilt down the wall under it. It shortens the crossing to 15 at one place on each side.

## 5. The look, decided now

**The biome is Mesa**, so the few tinted blocks are dry. The three families:

- **Ground**: the plain's ash in grey stained clay (renders dark brown) with black and brown clay patches; the
  cone's scoria in netherrack and brown clay; the black flow in black clay and coal. The rock beds of every cliff,
  cut and tunnel are slate (cyan clay), basalt (black clay and coal), tuff (grey and brown clay), grey
  (andesite and stone) and a thin red bed (netherrack and hardened clay), dipping gently and rising with the land.
- **Built**: stone brick and polished andesite, pilasters of smooth double slab stepped a block out, panels of
  nether brick sunk a block, an orange clay band sunk under each cornice, iron for the machines.
- **Accent**: lava, the teams' glass in the facade windows, the crew hall's team clay and runner, and the cold
  store's quartz, prismarine and sea lanterns, the one cool room on the board.

**Each room has its own identity.** The loading hall has double-slab pilasters, nether-brick panels, iron ceiling
beams and the slag line's rails; the crew hall dark oak posts and beams, red clay panels and a red runner; the pour
room iron pilasters, a smooth deck, the monument's quartz pedestal and a lever desk; the furnace hall a lit
furnace in every sunk bay and cauldrons on the casting line; the cold store dark prismarine pilasters, sea lantern
panels and a water channel round the plinth; the tunnels cut rock with stone brick ribs every five blocks.

## 6. What the build adds that the plan does not show

The facades' depth, the chimneys on the mountain over the furnace hall, the cooling pond of lava at the cliff's
foot between the facades (thirty blocks from the crucible and above its leak line), the lavafalls, the tip's slag
talus and the rails are dressing; none stands on a route.

**GO1 is missed and stays missed.** On a board 200 long with the spawns in the mountain, the enemy's walk to a
crucible cannot reach 3× the owner's while staying under GO3's 150: the spawn was moved five blocks forward to
bring GO3 from 153 to 148, and the ratio then reads 2.79. A defender who drops from the loggia reaches the
crucible's floor in 35 moves.
