# Riad — what was built

A King of the Flag board, built from the plan in `PLAN.md` after one review, which kept the middle post and the
bridge as they were. It is a walled palace water-garden floating over the void: one shared flag, three posts
of three kinds, and two spawn houses left by a drop into a pool.

![the riad](renders/30-iso-riad-se.png)

## How it was made

**The world is built from the plan's own rasters.** `scripts/plan.py` holds every column's floor height and
kind, and the roofs and decks over them. `plan_check.py` walked them, `sketch.py` drew them, and `gen.py`
builds each column to exactly that floor. A stair the checker climbed is a sandstone stair in the world, facing
the way the raster says it rises.

**What a raster cannot hold is built on top.** That covers the Cistern's tower and its two water columns caged
in light-blue glass, the Minaret's ladders, and the beacons under the posts. It covers the spawn houses' patios,
decks and rooms, the screen walls, the kiosks and fountain houses, and the fence round the board's edge.

**The flag's banner is a real banner.** PGM refuses a match whose flag has no banner block at its first post,
so the generator writes a standing banner at the Cistern as a tile entity: purple, with a white border and
roundel. `write_world.cs` gained a `Banner` tile kind for it, and the same writer hangs each team's banners on
its spawn house.

**`map.xml` carries the whole gamemode itself.** It writes out PublicMaps' conquest and kotf includes in full:
the kit, the carrier's kit and the drop kit, the `has-flag` spawn filter, the spectating respawn, the compass
on the carrier, and a score limit of 200. It runs on any PGM server without PublicMaps' includes.

## The paint

- **The court:** a check of smooth sandstone and smooth red sandstone round a ring of chiseled quartz, with the
  Cistern lined in prismarine and lit from its floor by sea lanterns.
- **The gardens:** grass edged in smooth sandstone, with hedges of oak leaves and cypresses of spruce leaves.
- **The back gardens and the balconies:** smooth sandstone ruled every six blocks in red.
- **The buildings:** red sandstone in courses with terracotta beneath, the arcades' quartz columns under a
  terracotta roof, the kiosk under a quartz dome, the fountain house in terracotta.
- **The teams:** red holds the north and blue the south, each in its wool. It runs along the board's edge under
  the fence, round the arcade roofs, in bands through the spawn house and the screens, and in a check on the
  patio and the deck. The middle band belongs to nobody, and its edge is quartz.
- **The carrier's line:** a band of purple wool across the board at z = ±32, the flag's own colour.

**Wool, not stained clay, carries the teams.** In the first build blue stained clay read purple beside the
flag's purple; blue wool does not.

## What the built world measures

`renders/walks.txt` walks the built blocks on foot from each spawn, with no jumps:

| From either spawn | Blocks |
|---|---|
| the pool under the spawn's hole | 7 |
| the canal's head at the court | 51 |
| the Cistern's top, by the water column | 82 |
| the Mirador's porch | 79 |
| the Mirador's pad, across the bridge | 95 |
| the Minaret's top, up a ladder | 87 |

**The two spawns are exactly even.** Each reaches 8,836 standing cells on foot and every place in the table in
the same number of steps, as the mirror says it should.

**Between the posts the Cistern is the hub.** From the Cistern's top the Minaret is 34 and the Mirador's pad
58; from one side post to the other is 80 to 88 through the court.

**The roofs are reached only by the parkour.** With running jumps allowed, a player from the spawn reaches the
arcade roof's far end in 52, and the walk gains 480 cells, all of them the roofs and the stones. On foot alone
the roofs are not reached at all.

**Nobody on the ground can get back into a spawn.** A walk from the Minaret's garden, with every drop and
ladder allowed, reaches neither spawn room.

**The plan's checks still hold.** `renders/plan-check.txt` finds no stair end without two cells of landing in
line. It finds no jump on the board but the three-stone climbs, and no post that sees either spawn's pool or
doors.

## The renders

- `00-plan-sketch.png`: the approved plan.
- `01`, `02`: the studio's top-down and height reads of the region files.
- `10`–`15`: true-scale sections down the axis, across the posts, through a water column, up the porch's
  stairs, through a spawn house and along an arcade.
- `30`–`36`: isometric views of the board, the Cistern, the Mirador, the Minaret, blue's half, and blue's spawn
  house cut open.
- `50`, `51`: elevations of the Mirador from the south and of the court from blue's side.
- `ref-desert-sanctuary-*.png`: the reference map, read from its region files.

## What I wanted, how hard it was, and what a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| A KotF board whose posts are each a different fight | Moderate: a raster for the ground and one for the roofs, with ladders and water columns as special edges | A post piece with its approach built in: a tower in a pool, a bridge to a pad, a pillar with ladders |
| The flag's banner in the world | Easy once known; PGM's source says the match fails without it | The studio placing the banner when it writes a flag's first post |
| A spawn left by a one-way drop into water | Easy: a hole in a deck over a pool three deep, and a walk that falls any height into water | A spawn piece with an exit kind: stair, drop, or pad |
| The carrier kept to the middle | Easy in XML: `enter="deny-flag-carrier"` over the back gardens and the roofs | A carrier zone drawn on the plan, and the XML written from it |
| No post seeing into a spawn | Moderate: a sightline cast over the raster from each post, and screen walls where it got through | A sightline check from every objective to every spawn exit, on the plan |
| Team colours a player can read | Easy, once it was clear stained clay was too dull | A theme's team-colour slot defaulting to wool |
| Validation of a KotF map | Not attempted here; the XML follows PGM's source and Desert Sanctuary's | KotF in the studio's round-trip: the posts read back against the world, the banner found |
