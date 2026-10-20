# Pithead — plan

**Pithead is Seamworks' dig turned into a capture-the-wool board.** The same works stand on the same ground: stone
floors cut down through orange ground with soot lying in black patches on it, dark steel panels holding the cut
back, brick works with their roofs fitted out. The ground here is not poisoned, so the orange surface is walked,
and the board floats over the void as islands the composer laid out.

**`scripts/plan.py` is the board.** It reads the composer's layout and intent from `composed-layout.json` and
`composed-intent.json`, moves them onto the grid, and states everything taken over or added for team red. Team
blue's half is its half turn about the middle. The blocks are Seamworks' own: `gen.py` loads Seamworks' `assets.py`
and `look.py` and decides nothing its plan does not state.

## The layout it was taken from

**The layout is the composer's micro board, seed 96, under the half turn, composer walled-5.** It is drawn for
fourteen players, seven a side. A local compose reproduces the library's card exactly, and the two JSON files are
that compose. The composed board's centre sits at (60, 120) on the grid, so a composed point (x, z) is (x + 60,
z + 120) here.

**Each half is six pieces round a donut hub.** The hub is 48 by 48 with a shaft of 16 by 16 through its middle. The
spawn hangs off its back, 16 wide. The frontline, 32 by 24, stands in front of it over the middle. Each wool's piece
is an L off one side of the hub: a corridor 12 wide leading to a body 12 wide, with the wool room at the body's far
end.

**The middle is a stone of 24 by 24 alone in the void.** Twelve blocks of void lie between it and each frontline,
and the build zone spans that gap, x 44 to 75 by z 96 to 143. Nothing else on the board may be built out over the
void.

**The composer's play structure is kept as it came.** That covers the spawn room, both wool rooms and their doors,
the redstone line on each room's entry row, one bedrock defence wall across each wool corridor, and its two defence
chests.

## What was adjusted

**The ground is cut at four levels where the composer has one.** The stone of the hub and the wool corridors is the
floor at y 34. The spawn yard stands two over it. The middle's stone lies three under. The surface, the orange
ground the diggers left, stands three over: it is the whole frontline and both wool bodies.

**A ramp is cut up through the surface wherever stone meets it.** Each ramp is stone stairs whose step edges
wander. The frontline's ramp is ten wide in its middle, and the frontline's face either side of it is panelled, so
the hub reaches the frontline only up that ramp. Each wool body is reached up a ramp the full width of its corridor,
just past the defence wall.

**The hub's two back corners stand undug.** Each is a bank of orange ground eleven by fourteen, six over the floor,
panelled toward the hub, with a bare olive on top. Between them the hub rises by a flight two blocks to the spawn
yard.

**The hub's shaft is the pithead.** Its lip is a collar of iron plates and smooth stone. A headframe stands on the
collar: four legs leaning in as they rise eighteen blocks, ringed in iron bars at six and twelve, and a deck carrying
two sheave wheels upright across the board.

**The land is pushed out up to two blocks past the composed outline.** The push follows a smooth noise, the same on
both halves. It never touches the build zone or the shaft, and stays five blocks clear of a defence wall's ends, so no
shoulder opens beside a wall.

**Rock and clutter break up each open area.** A rock boss four high stands at the front of each frontline, splitting
the bridge toward the middle into two lanes. Two outcrops five high stand on the middle's opposite corners. The hub
has a hut at the west corridor's mouth and a spoil heap of crust at the east one.

## What is played for

**Capture the other team's two wools and place them in your own spawn yard.** Red keeps red and orange, blue keeps
blue and light blue. Each wool lies on the floor of a works building at the end of its approach. A spawner there
gives it to an attacker standing in the room every second and a half. A team may not enter its own wool rooms.

**Each monument is a bedrock pedestal ringed in polished andesite, on the yard in front of the spawn hall.** Every
wool place below can be checked in the game:

| team | wool | lies at | room (inclusive) | placed at |
|---|---|---|---|---|
| red keeps | red | (22, 37, 164) | x 16–27, y 37–45, z 160–167 | blue's yard (64, 36, 20) |
| red keeps | orange | (106, 37, 168) | x 100–111, y 37–45, z 164–171 | blue's yard (55, 36, 20) |
| blue keeps | blue | (97, 37, 75) | x 92–103, y 37–45, z 72–79 | red's yard (55, 36, 219) |
| blue keeps | light blue | (13, 37, 71) | x 8–19, y 37–45, z 68–75 | red's yard (64, 36, 219) |

**Each wool corridor is crossed by a bedrock wall three courses over the floor.** Red's are at x 32 over z 176–187
and x 95 over z 180–191, with two defence chests on each wall's hub side. Blue's are their half turns, at x 87 and
x 24.

**Spawns are in the hall at the back of each half.** Red spawns at (60, 36, 228) facing the hub, inside a room of 16
by 8, x 52–67 by z 224–231, kept to red. Blue spawns at (59, 36, 11). The match runs 25 minutes, and anyone below
y 6 is sent into the void.

**A golden apple appears on the middle's dais every forty-five seconds.** The dais stands square on the board's
centre at the middle's floor. Everyone spawns with an iron sword, bow and arrows, an Efficiency II iron pickaxe, an
iron axe, shears, two stacks of wood and two golden apples.

## The ground and the buildings

**Under every floor is banded stone, thickest where the land is widest.** It runs from three blocks deep at an
island's edge to about sixteen in its middle, ragged underneath. Its faces carry Seamworks' beds of cyan clay and
pale clay, and under the surface the orange beds show over them.

**The works are Seamworks' brick works.** The spawn hall over each spawn room is three storeys with skylights and a
chimney. Each wool room is two storeys, its door three wide on the side its approach comes up. Every roof carries
cooling units, vents and an antenna, placed on red's and turned onto blue's.

**The surface is crust over orange beds.** It has soot patches sunk a block or two and is level within two of the
works and of every ramp. Dead leaves lie on it away from the paths. A bare olive stands on each bank and on each
frontline's flanks.

**The floor is worn and edged in the team's colour.** Stone lumps of half a block and a block are worn into the open
floor. A course of red or blue clay runs wherever the floor meets a wall. One pair of chevrons on each hub points
toward the other team.

## Walks

**Every walk below is read back by `walk.py` from the built world.** It counts moves from a spawn with the other
spawn closed. The two halves answer the same.

| from red's spawn | moves |
|---|---|
| its monument for blue | 10 |
| its monument for light blue | 9 |
| the red wool it keeps, walls standing / opened | unreached / 87 |
| the orange wool it keeps, walls standing / opened | unreached / 82 |
| its frontline's edge over the middle | 82 |

**A wool is unreached on foot while its wall stands, by design.** The wall is the defence's prepared line, and an
attacker builds or breaks over it. Every footing holds, and every objective's own check passes.

## Building it

```
python3 -m pgmvox.run /path/to/freeform/lib/boards/pithead
```

**The world is `maps/ctw/pithead`.** With the 1.8.9 client jar in `MINECRAFT_JAR`, the renders include the
textured views.
