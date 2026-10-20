# Pithead — plan

**Pithead is Seamworks' dig turned into a capture-the-wool board.** Each half is a body of ground standing on the
bedrock, and its play is dug down into it. Its stone floors are cut through orange ground with soot lying in black
patches on top. Dark steel panels and bare rock hold the cuts back, brick works stand in them, and plated strips
cover a seam of lava under the hub.

**`scripts/plan.py` is the board.** It reads the composer's layout and intent from `composed-layout.json` and
`composed-intent.json`, moves them onto the grid, and states everything taken over or changed for team red. Team
blue's half is its half turn about the middle. The blocks are Seamworks' own: `gen.py` loads Seamworks' `assets.py`
and `look.py` and decides nothing its plan does not state.

## The layout it was taken from

**The layout is the composer's micro board, seed 96, under the half turn, composer walled-5.** It is drawn for
fourteen players, seven a side. A local compose reproduces the library's card exactly, and the two JSON files are
that compose. A composed point (x, z) of red's half lies at (x + 60, z + 120) on the grid.

**Each half is the composer's pieces round a hub.** The hub is 48 by 48 with its two back corners cut off. The spawn
hangs off its back, 16 wide, and the frontline, 32 by 24, stands in front of it. Each wool lies at the end of an L
off one side of the hub: a corridor 12 wide leading to a body 12 wide, with the wool room at the body's far end.

**The composer's play structure is kept.** That covers the spawn room, both wool rooms and their doors, and the
redstone line on each room's entry row. It also covers one bedrock defence wall across each wool corridor, three
courses high, with its two defence chests.

## What was changed

**The pieces are cuts, not islands.** The ground runs four to eight blocks past every cut and down to the bedrock,
and stops flush with the frontline's open edge over the middle. Its surface walks at y 36, twelve over the hub. The
outer cliff shows the orange beds over the banded stone.

**The surface is out of reach.** Every cut wall rises at least seven blocks, and no block may be placed at y 32 or
higher. No player stands higher than y 33 anywhere but inside the spawn hall, which `walk.py`'s reach confirms. The
cuts are therefore the only ways from one place to another, and each wool approach stays its own lane.

**The halves stand fourteen blocks off the board's long axis, each the other way.** Red's frontline is centred at
x 60 and blue's at x 88. Each faces its own island across ten blocks of void.

**The middle is two islands, crossed sideways.** Each team's island, 26 by 18, stands in front of its frontline.
The two overlap by eight rows along z, with eight blocks of void between them along x. The route is frontline to own
island, sideways across to the other island, then on to the other frontline.

**The wool corridors meet the hub ten blocks nearer the spawn.** Red's runs z 186–197 off the hub's west wall and
orange's z 190–201 off its east wall. Each body is lengthened back to meet it, so a wool room lies some 30 blocks
down its body from the corridor.

**Each wool body stands a ledge five over its corridor.** Half the ledge is bare rock with a ladder up it. On the
other half a panel is leaned against the rock and stands three over the body's floor. The ladder is the only way up
on foot. Red's ladder is at (28, 24, 188) and orange's at (99, 24, 192).

**The composer's shaft is floored over.** Where it was, a plated strip ten wide and twelve long covers a trench down
to the seam's lava on the bedrock. Two plates are missing from it. A second strip, six wide, crosses the hub's front
east corner, one plate missing. A headframe stands over the middle strip: four legs leaning in as they rise
eighteen blocks, ringed in iron bars, with two sheave wheels on its deck.

**Rock and furniture break up each open floor.** A rock boss four high stands at the front of each frontline,
splitting the bridge toward the island into two lanes. An outcrop five high stands on each island's far corner. A hut
stands against the hub's west wall.

## What the floors carry

**The stone is marked in the team's colour.** A course of red or blue clay runs wherever the floor meets a wall.
Chevrons point the way: off the frontline toward the island, into each wool corridor, down each body toward its
room, and across each island toward the other. A diamond emblem lies in each hub's front.

**Every plated strip is ringed in hazard stripes**, yellow and black clay in pairs. **Every monument's pedestal is
ringed in its wool's colour**, so a carrier sees where each wool goes.

## What is played for

**Capture the other team's two wools and place them in your own spawn yard.** Red keeps red and orange, blue keeps
blue and light blue. Each wool lies on the floor of a works building at the end of its approach. A spawner there
gives it to an attacker standing in the room every second and a half. A team may not enter its own wool rooms.

**Every wool and monument below can be checked in the game:**

| team | wool | lies at | room (inclusive) | placed at |
|---|---|---|---|---|
| red keeps | red | (22, 29, 164) | x 16–27, y 29–37, z 160–167 | blue's yard (92, 26, 20) |
| red keeps | orange | (106, 29, 168) | x 100–111, y 29–37, z 164–171 | blue's yard (83, 26, 20) |
| blue keeps | blue | (125, 29, 75) | x 120–131, y 29–37, z 72–79 | red's yard (55, 26, 219) |
| blue keeps | light blue | (41, 29, 71) | x 36–47, y 29–37, z 68–75 | red's yard (64, 26, 219) |

**Red's defence walls are at x 32 over z 186–197 and x 95 over z 190–201**, with two defence chests on each wall's
hub side. Blue's are their half turns, at x 115 and x 52.

**Spawns are in the hall at the back of each half.** Red spawns at (60, 26, 228) facing the hub, inside a room of 16
by 8, x 52–67 by z 224–231, kept to red. Blue spawns at (87, 26, 11). The match runs 25 minutes, and anyone below
y 16 is sent into the void.

**A golden apple appears on each island's dais every forty-five seconds.** Red's dais is at x 54–59 by z 122–127.
Everyone spawns with an iron sword, bow and arrows, an Efficiency II iron pickaxe, an iron axe, shears, two stacks of
wood and two golden apples.

**Building over the void is allowed only across the middle's gaps.** The zones are x 42–77 by z 133–145 between red's
frontline and its island, x 68–79 by z 114–125 between the islands, and their half turns.

## The ground and the buildings

**Every column of ground is banded stone from the bedrock up.** Under the surface lie five to eight blocks of orange
beds and a crust of red sand and red sandstone with sunk soot patches. The stone carries Seamworks' beds of cyan clay
and pale clay.

**Each cut floor sits at its own level.** The hub and the wool corridors are at y 24, and the frontline two lower,
up a flight of wandering steps. The spawn yard is two higher, up a flight between the hub's cut corners, and the wool
bodies five higher. Each island is three lower than the hub.

**Each cut wall is panels or bare rock.** Panels stand along the frontline's sides, the hub's east wall and cut west
corner, red's corridor's ledge, and the inner side of each wool body. Every other wall is bare rock, made to
overhang and be undercut so it cannot be climbed.

**No orange shows at a panel's end.** An orange block beside a panel and open to the cut is rock, and red sand open at
its side is red sandstone.

**The works are Seamworks' brick works.** The spawn hall over each spawn room is three storeys with skylights and a
chimney. Each wool room is two storeys, its door three wide on the side its body comes up. Every roof carries
cooling units, vents and an antenna. Dead leaves and two bare olives a side lie on the surface, which is mesa with
swamp under its soot.

## Walks

**Every walk below is read back by `walk.py` from the built world.** It counts moves from a spawn with the other
spawn closed. The two halves answer the same.

| from red's spawn | moves |
|---|---|
| its monument for blue | 10 |
| its monument for light blue | 9 |
| the red wool it keeps, walls standing / opened | unreached / 87 |
| the orange wool it keeps, walls standing / opened | unreached / 93 |
| its frontline's edge over the middle | 80 |
| its own island, bridging | 101 |
| blue's island, bridging sideways | 122 |
| blue's frontline, bridging | 145 |

**A wool is unreached on foot while its wall stands, by design.** The wall is the defence's prepared line, and an
attacker builds or breaks over it. With the ladders taken out a wool body is unreached even with the walls open, so
the ladder is its only way up. Every footing holds, and every objective's own check passes.

## Building it

```
python3 -m pgmvox.run /path/to/freeform/lib/boards/pithead
```

**The world is `maps/ctw/pithead`.** With the 1.8.9 client jar in `MINECRAFT_JAR`, the renders include the
textured views.
