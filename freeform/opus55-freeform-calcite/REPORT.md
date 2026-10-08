# Calcite — what was built

A King of the Hill board, built from the plan in `PLAN.md` after three rounds of review: a white marble
quarry cut in three grounds round a lava pit, with the Middle on an island paying double and a side hill in a
walled alcove on the north and the south paying single.

![the quarry](renders/30-iso-quarry-se.png)

## How it was made

**The world is built from the plan's own raster.** `scripts/plan.py` holds every column's floor height and
kind; `plan_check.py` walked it, `sketch.py` drew it, and `gen.py` builds each column to exactly that floor. A
stair the checker climbed is a quartz stair in the world, facing the way the raster says it rises.

**What a raster cannot hold is built on top.** That covers the Spring under the Middle with its two stairwells,
the glass tunnels under the lava that fork to a trench either side of each side hill's front stair, the spawn
tunnels inside the quarry wall, the spawn huts, the slime pads, the hills' wool rings and the derricks. Each
is built for red and turned for blue.

**Each ground has its own floor tone.** The Ledge is andesite, the Bench diorite and the Rim quartz, three
blocks a third each in cells of three, so a player knows their level by what is under their feet. The cut
faces run in courses of diorite and polished diorite with a darker course of stone and a drill line of
andesite every fourth column.

## What the built world measures

`renders/walks.txt` walks the built blocks on foot from each spawn, with no pads and no jumps:

| From red's spawn | Blocks |
|---|---|
| the Middle's top | 49 |
| the North hill, the South hill | 82, 83 |
| the Spring, the golden apples | 56 |
| the Spring's tunnel, at its fork under the lava | 78 |
| a side hill's west window, east window | 76, 87 |
| the arrows in the north-east corner | 94 |
| red's tunnel mouth on the Ledge | 40 |

**Blue's walks are red's, turned.** Blue's spawn reaches the Middle in 50 and the two side hills in 84 and
83, and both spawns reach the same 6,970 standing cells.

**Every pad was flown again against the built blocks.** The walk runs 1.8's physics from each pad and its turned
twin and reports the first block the player's body meets:

| Pad | Comes down on |
|---|---|
| apron, north-west and north-east, and their twins | the Bench at (∓13.5, ∓29.5), y 23, after 13 ticks |
| the Ledge's corner, and its twin | the Middle's apron at (∓7.4, ∓6.4), y 20, after 18 ticks |

**That second flight is why one pad changed.** The plan's checker tested where a pad comes down but not what
it passes on the way. In the world the corner pad up to the Rim met the Bench's face in three ticks, and no
velocity both cleared that face and landed on the Rim. It now crosses the lava onto the Middle, the corner's
answer to the diagonal steps in the other two corners.

## The renders

- `00-plan-sketch.png`: the approved plan; `-v1` and `-v2` are the earlier versions.
- `01`, `02`: the studio's top-down and height reads of the region files.
- `10`–`15`: true-scale sections: west to east, north to south through all three hills, along a Spring
  tunnel, through a stairwell, across the North hill's alcove, and down red's spawn tunnel.
- `30`–`36`: isometric views of the quarry, the North hill, the Middle, the Spring cut open, a corner and a
  spawn.
- `50`, `51`: elevations of the North hill from the Middle and of the Middle from the west.

## What I wanted, how hard it was, and what a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| Routes each with a purpose, measured before building | Moderate: a height raster, a walker with stairs, drops, tunnels and pads, and a length for every named route | A route layer on the plan: named waypoints, walked and measured on every edit |
| Only the jumps I planned | Moderate: a search for every gap of one to three blocks in any direction, with corner hops filtered out | A jump audit on the plan, listing every jumpable gap so an accident shows before it is built |
| Jump pads that land where they are meant to | Easy to simulate; the lesson was to fly them through the built blocks, not over a height map | A pad tool: pick a target, solve the velocity, and draw the flight against the real geometry |
| A board symmetric for teams, with each side hill mirrored about itself | Moderate: half-turn for the teams, a mirror per hill, mirrored pad velocities | A symmetry setting per piece, not only per board |
| Tunnels under lava, in glass | Easy: a carved run whose walls and roof turn to glass where they meet the lava | A tunnel piece that knows what it passes through and lines itself to match |
| Stairs between three grounds that read as stairs | Easy once the sections were drawn at true scale | True-scale sections in the plan view by default |
| Hill regions and wool rings that match the hill | Easy by hand from the plan's boxes | Hill pieces that write their capture, progress and captured regions with the hill |
| Validation of a KOTH map | Not attempted here; the XML follows PGM's source and Mush's | KOTH support in the studio's round-trip, so a hill's regions are read back against the world |
