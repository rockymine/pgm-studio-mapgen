# Generation notes — what the API does not say

Everything here was learned by driving the live API and reading a column back. `ORDER-OF-WORK.md` is the page
that comes first and says *when* each decision is made; this is what none of the studio's own answers can say
about the instruments, in thirteen chapters in that same order. Open the chapter for the stage being worked
on rather than the file.

**What the studio can state about itself is not repeated here**: the routes and their fields are in
`GET /api/openapi/v1.json`, every rule id is in `GET /api/rules` with what it means and how to fix it, and a
posted field that went unread comes back as `RQ3` naming its own JSON path.

This file is only what none of those can say — a fact about how two correct mechanisms interact, a number a
gate does not check, a read-back that lies.

**A fault the studio has since fixed does not belong here.** An entry naming a task id as an open gap is a
debt that comes due the moment the task ships, and it then reads as a limitation the studio no longer has —
so every claim is checked against the running API, and against the source where two answers disagree, before
it is kept. This file carries no task ids for that reason.

**And what a technique card demonstrates is not repeated here either.** `techniques/` is twenty-two cards,
each one instrument worked through on a committed board with the reads that prove it, so where a card exists
this file states the claim in a sentence and points at it. What stays is what a card cannot be: the fact that
two correct instruments interact, the number no gate checks, the read-back that lies, and the author's own
rulings — those last are `WHAT-A-BOARD-IS-MADE-OF.md`'s where they are about how a board should look.

---

## The board, before anything is drawn

What is decided before a shape exists, and what cannot be recovered by deciding it later.

### Construction before dressing: a coherent terrain first, platforms as layers

The plan states the board's **arrangement** — which ground is where, at what height, next to what. It is not
the board's shape, and cutting it into more pieces to get a shape is the failure this section exists to name.

The worked failure is **13 plan pieces at 6 surface heights**, then
`themeByHeight` mapping each of those 6 heights to a theme. The theme partition is therefore the height
partition, which is the piece partition — the board's look is decided by how it happened to be cut up rather
than by any reading of the terrain, and it comes out chopped instead of coherent.

The order that works is the other way round. Author the terrain the map is played on as **one shape**, or as
few as the arrangement genuinely needs, and reshape it per vertex until it reads as ground. Then put the
platforms a match needs — a monument shelf, a middle plateau — on **layers over it**, which is what a layer
is for: `addLayers` with a `base_y`, a footprint, and its own theme. Those 13 pieces are one terrain shape
plus two platforms.

A plan piece earns its place by stating something the arrangement needs: a height a lane climbs, a room a
building is seated in, a footprint the symmetry fans. A piece that exists only so a theme can be hung on it
is a piece that should have been a shape scope.

---

## The plan

The plan states the board's arrangement — which ground is where, at what height, next to what — and every rule here is about a relation between two rectangles.

### The board is written in cells, so read it as cells

`tools/board.py` renders a plan's rectangles as an ASCII grid off the plan file, and
`GET /api/map/{slug}/plan/ascii` does the same off the stored plan. Take one before posting anything.

The faults that cost the most are **relations between two rectangles**, and a grid is the only view that puts
two rectangles on the same rows:

```
  -1 |    MMMMMMMMMMMMMMMM    |     M = a neutral bar, sixteen cells wide
   1 |          NNNN    OOOO  |     N = the build zone that reaches it, four
```

Sixteen against four is a landform most of which no journey reaches, and it is one glance. The renders that
get looked at instead — the ground map, the heightmap, the theme swatches — are pictures of a *world*, and a
picture makes a long bar look like a good idea. Nothing in the picture states the width of the window that
reaches it. The same grid catches the rest of the family: a wool room touching the spawn apron (`LN1`), an
approach whose wall can be walked round because the ground reaches past it, a spur that connects to nothing.

### On half a box the goal bands cannot all hold at the plan tier

Four terms measure where a goal stands and every one of them is a band with two ends. The ratio of the enemy
walk to the author's own wants **[3.0, 4.0]**; the walk from its own spawn wants **[40, 90]** blocks; two
goals of one team want **[35, 65]** between them; and the two teams' goals want **[85, 150]**.

With the doors 134 blocks apart on a 130 × 120 board and a goal a distance `d` along the line between them,
that is `d` in [27, 34], `d` ≥ 40 and `134 − 2d` ≥ 85 — three of them with no common point. A board too small
cannot satisfy them, and neither can one whose halves are too far apart to be reached.

The plan tier walks the pieces flat, so a gill cut eight courses deep or a single bridge lengthens no route it
measures.

The terms are soft, and a board may take `d` = 33 — the ratio in band, the other two read and left —
because it is the built board that decides the walk, and there the beck makes every enemy route go by the
bridge.

### Reachable is not used, and every gate before coverage measures the first one

`CT12` on the strait, the traversability components, the goal ratios, the group symmetry error — every gate a
board passes before it exports asks whether ground **can be got to**. None asks whether any journey **goes
there**. A board can pass all of them while carrying whole landforms no player has a reason to walk.

`GET /api/map/{slug}/coverage` is the read that answers the other question, and
`GET /api/map/{slug}/plan/flow` is the same question off the plan alone, before a world exists to measure.
Two builds of one board differing in a single decision read **27.2%** of their ground dead and **0.8%**.
The first spanned its neutral bar `x −40..40` while the build zone crossing it spanned `x −10..10`, so every
journey over the bar was a bridge through that twenty-block window and the ground either side of it was dead
by construction. The second cut the bar to the build zone's own width.

The general shape of the mistake: **a mid-board stepping stone is used only across the width of the build zone
that reaches it**, and the corridor margin buys back six blocks and no more.

A water lane buys back none — a lane sits outside the build slice and therefore outside the navigable set, so
no route is walked through one.

Coverage is a **measurement, not a gate**: nothing refuses on it, which is exactly why a run that does not
read it lets a board ship with a third of its ground unused.

### A plan carries holes by arrangement, not by subtraction

**There is no way to cut a hole inside a piece from a plan.** A `buffer` drawn over a generating piece is
inert — it can declare a void but never destroy ground — so the fill ratio does not move and no hole appears.
A hole in a plan is made by **arrangement**: pieces ring a gap, no piece covers it, and `PlanVoids.Declare`
names every such gap a `void-N` buffer on every compile whether or not the author drew one.

The instrument for cutting a hole *through* ground is a layout `subtract`, and the compiler is what supplies
one: every declared `void-N` comes back as a polygon subtract named `void-N-cut`. Shape the **pieces** to
shape a coast, and cut any further holes in the layout. `techniques/cutting-a-hole` is the worked card.

This is also why `POST /api/plan/evaluate`'s `G8 fill-ratio` reads a board denser than it is built: it
measures the plan's rectangles, which do not know about a layout `subtract`.

**A wool board is where holes belong.** Over 400 boards composed at `players=32`, `rot_180`, 63% of hubs are
`ring` or `double-hole`, 19% of frontlines are `twin`, and 10% of wool approaches are `donut` — all bodies
with a void in them. Of the 98 shape cards, 73 are donuts. `examples/generator-32/` holds six of those boards
as plans and as grids; `docs/gameplay/match-flow.md` §3.2 is what the holes are for.

### A piece at a lower surface, enclosed by higher ones, is not a cut

The compiler traces **one outline per connected component**, and the rasterizer gives a contested column to
the taller add. So a `beck` piece at surface 7 with hub pieces at 12 either side compiles to a shape that
exists — `barn-7`, four vertices, listed in its group — and never appears in the world. Measured: a transect
across it read `11 11 12 12 13 13 14` straight over the top, the water prop drawn for its bed sat on the
surface like a puddle, and `GET …/preflight` answered **export gate OPEN**.

What cuts it is an `addShapes` entry with **`override: true`**, which moves the shape into the second pass of
`((adds − subtracts) ∪ override-adds) − override-subtracts` and overwrites the column it lands on outright.
The plan then states one piece for the ground and the cut is made downstream, which is the right division
anyway: a piece is a room or a corridor, and a cut is a shape.

### The plan tier's frontline is the pieces a **build zone** touches

`FannedGraph.Build` sets `Frontline` to the nodes that touch a fanned build zone, and `SP1` asks
whether a wool is reachable from a frontline node without crossing a spawn. A plan with `zones: []`
therefore has no frontline at all, and every wool on it refuses with *"only reachable through a spawn
piece"* however open the board is. The canonical two-wool seed carries a `mid-band` zone for exactly
this reason.

### Raising the terrain under a stamped room is the plan's statement to make

A piece states its `surface`. Lifting the ground with an override add instead leaves the room correctly
seated on the higher ground and its spawn marker at the height the plan still states, inside the mass — both
spawns then leave the objective chain and `EX1` refuses the export.

### A wool room must abut ground, not sit inside a piece

A `wool-room` piece drawn inside a larger `piece` rectangle shares no edge with it, and the plan tier
answers `WX6 — wool room is unreachable: no land seam and no abutting build zone to enter by`. Split
the surrounding piece into rectangles that tile around the room instead.

### A wool room's foundation is bedrock to y 0, so it needs land on all four sides

A stamped wool room fills its whole piece and fills **downward in bedrock**: the column under
such a room reads floor at `y 25` and bedrock from `y 24` to `y 0`. Nothing about that is visible
in a plan view, in the relief read-back, or at the export gate. It is visible in the world as a 25-course
bedrock cliff wherever the cell beside the room is void or lower, which on a board where the room piece is the
full width of the spur it hangs off is every cell of two of its four sides.

So a room piece gets a piece of ordinary ground either side of it and one behind, and the pad mark is drawn
wide enough to cover all of them at the same height. Thornfell's rooms sit in a band of five pieces —
`ledge-w · room-w · ledge-wi` across, `crag-w` behind, `spur-w` in front — and the `roompad` ring is 22 × 10
rather than the room's own 14 × 10 for that reason. Read back, the ground either side of the room is `y 25`
and the room's own wall starts at `y 25`: the plinth is under the land rather than beside it.

The gate that hides the fault is that **a push is applied after every constraint**, so a range whose skirt
crosses the room lifts the pad the room is stamped on and the plinth grows by exactly as much. Before the
ranges were set back, the same room read floor at `y 43` over 42 courses of bedrock, with void either side.

### A spawn hall's doors come from what its piece touches, not from the facing

A spawn is cut with a door on each wall its piece meets more board on, at most two — the same derivation a
wool cage has always used, capped. So the number of exits is not something a plan states: it follows from
where the piece was drawn. A corner piece with a neighbour on two sides gets two doors and a piece with one
neighbour gets one, and there is no way to ask for three.

Two things follow. `facing` is a **direction only** and takes eight values, the four walls plus the four
corners — `back-right` on a corner hall points the player between its two exits and yaws `315`, which names
no wall at all. And the **march between two rooms becomes an approach the dressing keeps clear at both
ends**: `DR-KEEP` declined a tree at four separate positions along one before it was moved off the march
entirely. Read `06-claims.txt` before seating a prop near a room, not after.

### `POST /plan/room` is where the spawn's marker, building and iron all come from

The route answers *what room does this piece carry*, for the piece **as the document states it**: it reads
the placement's `facing` and its `footprint` and answers `{at, footprint, iron}`, all piece-relative block
offsets. Asked with a 12 x 12 hall stated in a 20 x 20 spawn piece it gives
`{"at":[7,7],"footprint":[1,1,12,12],"iron":[3.5,16.5]}` — the marker at the hall's own centre, the
footprint back verbatim, and the cube beside the door on the player's right as they leave.

**State the building, then copy the answer.** Sizing the hall by hand and then guessing the marker or the
cube is three numbers that can disagree; asking is one read that cannot. A piece with no placement yet
answers for the drawing defaults instead — a front door and the room the piece affords.

### The iron cube stands OUTSIDE the room shell

`WX8` reads *"inside the piece"* and it is easy to read that as *inside the room*. The cube is `IronSpan`
square, stands **in the ring between the shell and the piece edge**, and holds `IronGap` blocks of clear air
to the wall.

On a 20 × 20 piece whose shell is the piece inset one and five in front of the door, that ring is the
five-block door apron and nothing else: the cube fills it, three blocks of cube and two of air, and anywhere
in the hall is unplaceable. Shrinking the building widens the ring, and `/plan/room` hands it over rather than
being guessed at.

**The same `placements.iron` entry builds two different structures, and the piece it rides decides which.**
An iron marker on a piece that also carries a spawn never reaches the standalone loop: it rides
`SpawnIntent.Iron`, is resolved beside the framed room, and comes out a **3 × 3 × 3** block sized to the slot
the framing carved for it. On any other piece it falls through to the standalone path and stamps a plain
**4 × 4 × 4** cube.

**An iron marker beside a spawn takes a bite out of the building rather than adding to it.** Measured on one
board: the spawn cube framed 18 blocks wide with the marker absent and 14 with it present, and the four blocks
given up are exactly where the armoury stands.

**`ST2` complains about an iron marker outside the spawn piece and keeps it.** `/plan/evaluate` still answers
`valid: true`, so a standalone cube is a deliberate choice rather than a mistake the gate caught — and only
the spawn-bound one is wired to regrow in the `map.xml` the studio writes.


### A `walls` entry closes an interface, not a route

A plan wall stamps bedrock two thick and three tall across the interface it names, over that interface's full
width, on the attack side — so it closes exactly one seam. On a plan whose pieces enclose something that is not
the same as closing the way through: a `donut` wool box has a lane down **each** side of its hole, and a wall
on one is walked past on the other.

Count the ways round the thing before counting the walls. Where the plan has no seam at the place a wall is
needed, **split a piece to make one**: cutting a ring's two long arms in two level with the middle of its hole
takes twelve pieces to fourteen, which puts one interface in each lane facing the other across the yard.

**Two refusals bound where a wall may stand, and both are 422 rather than lint.** `PL11` names a pair with no
shared land border, and `PL13` names the wool room's own interface — a wall there stamps through the room it
defends. A pair that is both answers both in one response, so isolating `PL11` takes a pair that touches
nothing and has no room in it.

**Which face opens for the chests is not a field, and a `side` was removed because the geometry answers it.**
The wall is two blocks thick, so exactly one face can be opened without breaching it, and
`ContactGraph.ApproachSide` takes the side further from the wool — the side both the raiders and the defence
reach the line across. It is carried as a **piece** rather than a compass direction so that it survives the
orbit, and `GET /api/plan/inspect` reports the resolved answer as `wallChest` before anything is built.

**The chests are two, on the approach column, at a third and two-thirds along the interface.** The defence
face one block over carries none: the wall does not have two faces with a chest each, it has one face with
two.


### `PL17` compares the two pieces a wall names, so a wall at a T is passed and flanked

The rule asks whether the pieces either side of a wall are the same width, and nothing else. An arm sixteen
blocks deep walled against a hub side sixteen deep passes it, while the hub's pieces in front of and behind that
side run on past both ends of the wall, and a player rounds it off either corner of the junction.

**Put a neck between them and wall the neck's seam.** A piece one cell long and as deep as the arm, walled on
its seam with the arm, has void past both ends of the wall. The room still wants its fifteen or so blocks behind
the wall (`ST8`), so the arm grows by the neck's length.


### On a bridging board the gaps are the design, so state them first

Six-block gaps between groups answer `G2` (a corridor under ten wide), `G5` (a hop outside 10–20)
and `CT12` (a strait outside 15–40) on every pair, and they are right: a six-block gap is a running
jump. Fix the four numbers — the hops and the strait — and fit the groups round them.

---

## A board somebody else arranged

What the composer answers, what it does not, and what taking one of its boards over costs.
**`techniques/taking-over-a-composed-board` is the worked card** — one pinned board edited four ways, with
the compile, the holes, the heights, the build zone, the wall and the planting all measured on it. What is
here is what the card does not carry: how to browse the composer at all, and the rulings.

### Browsing the composer is a four-call loop, and a scan is what tells you its vocabulary

`GET /compose?players=&symmetry=&seedStart=&count=&hub=&front=&wools=` returns cards carrying the descriptor
that reproduces each board, its score, a structural read and an SVG; `POST /compose/pin` stores one from that
descriptor and hands back an ordinary `PlanModel`; `GET /plans/{id}/png` renders it; `POST /plan/{id}/author`
makes a map row. Ninety-six seeds, eleven pins and two contact sheets is a few minutes.

The vocabulary it filters on: hubs `ring|bar|double-hole|twin|P|G|single`, frontlines `twin|single|bar|none`,
wools `i|l|donut|u|h|clamp`. **There is no `u` frontline** — `u` is a wool family, and the frontline that
reads as a U opening forward is `twin`, a bar with two prongs off it.

**The cell is a drawing scale and the composer draws on four blocks**, so every width it builds to is stated
in blocks and divided by the cell: cells 3 through 6 all compose, and only cell 3 at nano comes back
`exhausted`. **10 and 12 players give identical boards**, because the count names a size band rather than a
budget of its own.

Hub forms seen in 48 seeds at 16 players: `bar`, `ring`, `single`, `twin`, `g`, `double-hole`, `p`; wool
shapes `i`, `l`, and `donut` five times in forty-eight — five pieces round a hole.

### A composed unit is offset, not symmetric about the centre line

`players=24&symmetry=rot_180&wools=i` pins a team unit of **142 proxy cells** — hub 66, frontline 30 + 14,
spawn 6 and its room 6, two wools 10 each — on a **22 × 36** bbox, and both halves with the mid come to about
**0.36** fill, inside the `fill-ratio` band of [0.201, 0.542] that `G8` reports. That term measures a **wool**
board and answers `null` for any other kind, so it is not a judgement about a destroy board's density.

The shape that gets there spans `x −11..3` of a board running `−11..11`: the unit is **offset**, its own
`rot_180` image takes the other side, and the two interlock so that each row is about half land. A unit
authored symmetric about `x = 0` fills its own bounding rectangle and is refused at **0.774**, with `FR6` on
the 24-cell frontline that shape produces and `LN2` on its chain. All three name symptoms; the cause is the
arrangement.

### The composer's holes are made by arrangement, and nothing marks them

A double-hole hub's two slots and a U wool's notch are the *shape of the pieces*, not a region: no field
names them and no gate defends them. The predicate to find one before the compile is a void cell with land in
all four directions within reach — open sea is void with nothing beyond it, and a shape may hang over that.

**A hole is never scenery, and nothing but this sentence defends one.** What the composer encircles is ground
players go round, and the walls a board hangs on it are drawn to guard exactly that ground; filling it makes
them guard nothing (the author's ruling). Both ways of filling one store at **200** with `SK13` — a plain add
draws nothing, an override add fills it — so the complaint is the whole of the defence. Where the void wants
to change shape, **redraw the subtract** rather than writing an add over it.

### Three rulings about taking a board over, which are the author's and not a gate's

**A piece taken out for a build zone is the cheapest edit that changes how a board is fought over.** Drop it
from `pieces`, add a `zones` entry over its rect, and the compiler turns that into the intent's own
`build.areas`. On a `rot_180` board with one wool a team both sides spawn, turn the same way and run past each
other down the lane furthest from their own spawn; taking that lane out means an attacker takes the near lane
or bridges under fire, and the two teams meet instead of trading.

**A `walls` entry stamps a barrier with no gate, and that barrier is the feature.** Four courses of bedrock
over the ground either side, two columns deep, along the whole interval two pieces share: a defender builds on
it and cannot lose it, and four courses is what an attacker bridges. It goes on the approach and not in the
hub — on the seam between two approach pieces, or on the outer one where the approach meets the board, since
`PlanValidator` refuses the wool room's own interface.

**Never chamfer a corner a build zone or the front line attaches to.** Taking a compiled outline's corner back
is an ordinary layout edit, but a diagonal on an edge somebody bridges from leaves them a triangle of ground
nobody can build on. Take the corner off the outer coast, where a coast is only a coast.

### A contested middle wants a structure, and a structure is one made layer per span

The neutral holm both teams bridge to is the piece most worth building on, and a flat island is nothing to
arrive at. What it wants is a **double deck** — four legs at the corners, a floor with three blocks clear
under it and a roof with four clear between — so the same piece is a height to hold and a room to hide in
(the author's ruling).

**A leg passing a floor is two spans in one column, which one layer cannot hold.** Cut the legs at each floor
instead and give every span its own layer marked `kind: "made"`. Make the footprint **odd in both axes about
the centre** and it is its own `rot_180` image; an even span is one block off-centre, which on a rotational
board is one team's middle.

### On a composed board the props are searched for, and the search is not the authority

Every piece is ten blocks wide with a road down the middle and void around it, so there is no landscape to
place by eye — fourteen declines on one board, half of them `DR-SITE — has no ground`. A search over the
authored half is instant and answers the truth, and three things decide whether it answers about the board
you have.

**Store the compiled intent first**, because the rooms, the doors and the spawns are not in the claims map
until then. **Test every candidate's `rot_180` image** as well as the candidate. And **ask it of a board with
no props on it**, because a tree raises its own column's top and claims the cells its crown covers.

**What it answers is where a prop MAY stand, and how many stand there is the author's.** Planting every site a
legal field offers is a forest, and a board of ten-block corridors has no room for one.
`WHAT-A-BOARD-IS-MADE-OF.md` §where a tree stands carries his rules, and the card carries the worked field
region by region — including the two the studio enforces by itself, a wall's approach and a one-cell tread,
which answer **0** legal cells without being asked.

**A search is also narrower than the studio, so check a site against the dressing pass.** A filter that keeps
only cells with eight level neighbours refuses every **rim** cell, because beyond a rim is void and a
neighbour that is not ground fails the test; what the studio asks is ground under the trunk, three clear of
the paving, unclaimed and not kept clear. On a bar twelve deep with a five-wide road down it the rim is the
only row left, so the search's silence there is conservatism and not a refusal.

---

## The compile

What the plan becomes, and what a finish is keyed onto.

### The compiler groups groups by mirror, not by landmass

Every fanned piece lands in one group called `team` however many separate rocks they are, and every
on-axis piece in `neutral`. An archipelago of a team group plus a flanking skerry is therefore **one**
relief keyed `team` covering two landmasses — which works, because the relaxation only ever steps onto
land and a mark on one says nothing to the other across the void.

Two consequences worth having before authoring one. **Nothing on `neutral` is mirrored for you**: a non-fanned
group's relief is stated once and used once, so every mark on it has to be authored as an explicit pair about
the origin or the two teams play different ground in the middle.

And **an authored shape naming no group joins the first one**, which on a compiled board is the fanned one,
so it is fanned. That is right for a shape meant to be a team's, and right for one on an on-axis group **only
if that group is its own rot_180 image** — authoring such a ring as half its points plus their negations makes
it exactly that, at no cost. A shape that belongs somewhere else names its group.

### `shapePropsById` reaches a compiled shape's geometry, not only its knobs

`tools/README.md` lists the mergeable fields as `relief_scope`, `controls`, `anchor_heights` and
`height_mode`. The merge is a plain dict update over the compiled shape, so **`vertices` merges too** —
which is what lets a plan of three rectangles compile to one polygon and that polygon be replaced by a
hand-authored ring with a full handle table. A 24-vertex ring and 24 control entries posted this way draw
no `RQ3`. Pieces at one `surface` fuse into one shape, so keeping every generating piece at the same
height is what makes there be exactly one shape to replace.

### `addShapes` lands on the group the compile emitted, which is called `team`

A relief keyed to any other name answers `SK3 — a relief is stated for group 'x', which the layout
does not carry`, and then `relief/read` answers no groups at all. `{"*": {...}}` is the key for a
board of one group, and the driver's own guard stops the run there rather than building a flat
world.

### A relief posted to `sketch/from-plan` loses to the one already stored

`from-plan` merges, and a relief is carried across the merge under its own rule. On a map that already holds
one, posting a **changed** relief answers 200 and builds the terrain that was already there.

The two reads disagree and both are correct: `POST …/sketch/relief/read` measures the layout in the request
body, so it reports the new numbers, while `GET …/render/heightmap` builds the stored document, so it draws
the old ground. An iteration loop that watches the readback sees its edits land and an iteration loop that
watches the render does not.

The merge is no longer silent about it — one `SK1` complaint per group whose posted relief was replaced rides
back on the 200 — but the terrain still comes from the stored one.

`PUT …/sketch` replaces the blob verbatim and is what an edit loop wants; `from-plan` merges — it carries a
stored finish, relief and structural height onto the freshly compiled board, and refuses at 409 with `SK1`
where the recompile leaves an authored relief with no group to land on. `?force=true` accepts that loss; it
does not make a posted relief beat a stored one. A spec-driven build wants neither, because it posts a whole
layout every time: `drive.py` stores through `POST /map/from-documents`, which replaces the map at the slug
outright, and the merge rules above never come into it.

---

## Relief

The relief is the ground's own shape. A mark is a constraint and a push is a landform, and nearly everything that goes wrong with terrain is one being asked to do the other's job.

### A mountain is a push. No mark can be one.

A relief mark is a **constraint**: the ground here *is* this height, honoured exactly, with no falloff. A
`point` mark at `h 47, r 8` therefore builds a **drum** — a flat disc on a twenty-block sheer wall — and a
`line` mark with per-vertex heights is the same object stretched along an arc. Both produce correct relief
numbers and a gate that opens over a landform reading as a row of oil drums.

A **push** takes a drawn ring and lifts the solved surface inside it, and three of its fields are the
landform. **`amounts`** is one lift per position round the ring, spaced by **arc** rather than by vertex.
**`crown`** is how much higher the middle stands than the edge, where the middle is the ring's medial axis —
**the record's default is `0`**, so a push authored without touching it is a plateau, and this one field is
the difference between a mountain and a mesa. **`falloff`** is the skirt measured from the ring across the
land, and it decides how much of the board the range eats.

`roughness` wobbles the skirt against a noise field, and a **negative crown** dishes the ring — a corrie, a
quarry floor, a pond basin. `techniques/pushes` is the worked card and `techniques/marks-and-pushes` the same
instrument with a board under it.

**The second half is what is *not* written.** Pinning a region with an `area` mark because it should be about
that height leaves the solver nothing to solve, and a board with a mark on every region is a table with bumps
on it. A range that reads pins the coast, the dale floor, the goal's shelf and the spawn's apron — every one
of them ground a player walks — and the flanks carry no mark at all.

`reach: 0` goes with it: a finite reach pulls ground back toward `base` at that distance from any constraint,
so between two distant marks the flanks decay and the range becomes separate hills.

**An `area` mark's ring is a shape, and a rectangle looks like one.** Marks written as four-vertex rectangles
build mesas with sheer sides, visible in the heightmap as literal squares; the same marks on nine- and
eleven-vertex lobed rings are indistinguishable from ground.


### Three ordering facts about a relief, and each one hides a landform

**A push is applied to the solved surface, so a push over a hollow fills the hollow in.** The marks are solved
first and the pushes are added to the answer. A twenty-radius push laid across a bench meant to be five blocks
down lifted it six, and a `sink` cut from that ground came out shallow with nothing complaining.

**A later mark wins a contested cell, so a mark written over a bench replaces it.** That is the mechanism the
stacked-hollow idiom depends on — nested `area` rings written outward-in — and the same mechanism that
overrode a bench with a knoll written after it and left a **21-block** face into a pit nobody authored.

**And a push over a pan lowers the pan**, so a flight anchored to arrive on that pan lands proud of it —
visible in `…/walk` and in nothing else, because the flight is correct and the ground is correct and only the
join is wrong. The rule under all three: **a push is added to the solved surface and marks negotiate with each
other.** Where a landform has to agree with something already stated, state that as a mark.

**A push carries the ground rather than replacing it**, so a landform wanting a flat top needs flat ground
under it: a hillside reading 15 → 10 → 14 lifted 12 with `crown` 0 came out 27 → 22 → 26, the same shape plus
twelve, with a hollow on its summit.

**A push cannot be kept off a mark: only its ring and its `falloff` can.** Ring plus falloff is its whole
extent, and every cell inside that circle is lifted whatever states it — a holm pinned at 10 twenty-four cells
clear of a push still read 22, 12 and its stated 10 across eight cells.

**How much of a board to pin is one dial, and `level` is the reading.** Pinning every region built three plates
at `level` **0.51**; pinning only the ground a player stands on built flowing terrain at **0.30**, which is
where `RL5` begins. **`reach: 0` is what a board wants**: at `reach: 16` the same document sagged its unpinned
half to within a few blocks of `base`, and one flowing landform came apart into two mounds.

**A field pinned only in patches relaxes into fans radiating from each patch; a field pinned along two opposite
edges relaxes into the ramp between them.** The fans paint as a spray of contour streaks over ground that is
otherwise flat. Two long marks facing each other are what a hillside is made of.

**A push's skirt is gentler than its stated grade at the ends and half again steeper in the middle.** The
smoothstep a `falloff` eases with peaks at 1.5× the average, so a skirt the read calls 0.55 reaches 39° and one
it calls 1.33 reaches 63° — the difference between scree and crag to the slope bands.


### Pushes add to each other, so a massif is several of them

**Every push in a group is summed into one lift field**, so a smaller ring inside a larger one is a terrace on
it rather than a replacement for it, and two rings that cross give the sum in the crossing. Three concentric
rings at `+10`, `+8` and `+6` on a plain at 8 build terraces at 18, 26 and 36.

**The skirts add as well, and that is where the unauthored steep ground comes from.** Two grades of 1.17
meeting between two rings make 2.34: on one measured pair, 112 barrier steps, none of them inside either ring.

**A negative push inside a positive one cuts the hill after it is raised, and the order they are written in
changes nothing.** A sum has no sequence: what makes a caldera a hollow is that its ring lies inside the
cone's. `techniques/pushes` has the arrangements side by side.


### `amounts` is read at the nearest ring point, so it cuts the interior into wedges

**Each interior cell takes the lift of the ring position nearest it**, and that partition is the ring's medial
axis — so a ring of few positions builds that many wedges with a step down every seam between them. A 40×40
square carrying `[26, 26, 6, 6]` builds two wedges at 34 and two at 14 with a **20-block cliff along both
diagonals**, two cells wide, which nothing in the document or the read names.

**Two things remove the seam and a spur wants both**: enough positions that neighbours differ by little, and
a form long enough that the two sides facing each other across the middle carry the same lift — which means
stating the lifts as a function of position *along* the form rather than of angle round it. A transect across
every place two landforms share ground is what finds this, before believing the JSON.


### A pin inside a push's ring applies the push twice

A room, a goal or a held shape standing inside a negative push takes the whole island down with it. The group
is solved once without the room, the floor is read off that solve and the room is pinned at it — and that pin
is then the group's only constraint, so the second field relaxes to a constant at the room's height and the
push subtracts its whole amount from that.

Measured on a pit meant to read rim 32 and floor 20: with a room inside the ring and nothing else pinned, the
rim reads **20** and the floor **8**. The threshold is one pin and nothing refuses — the store answers 200 and
the read calls the group `rolling`. **One `area` mark holding the land at the surrounding height fixes it
exactly.**


### A relief is solved on the group's primary half, and its surface is copied through the mirror

A mark on the far half constrains cells the solve never visits and is overwritten by the image of the near
half. For a team's ground that is the side the plan's pieces are authored on, because a mirrored group's
footprint is that one unit.

**A group that straddles the axis is solved on its `z < 0` half.** A neutral holm under `rot_180` is one
footprint across the centre, and the half-turn keeps the cells north of the centre and copies them south, so a
mark stated south of it is discarded without a finding. Measured: a 32-block holm with a bank, a knoll and an
edge stated on its south half and a bed across the centre solved flat at the bed's 7 over all 1,024 cells, and
the relief read listed no silent mark. The same marks turned through the centre built 7 to 13.

### A mark pins its own cells and the relaxation slopes everything within `reach`

Two regions at different heights with nothing between them come out as one long ramp, so a floor that must
stay level next to a lower one needs a verge pinned at its own height. Otherwise a wall's footing, and the
gate in it, follow the neighbour down.

### A point mark's radius pins a flat disc, so a radius is a mesa and not a summit

`PointMark.Pins` yields **every** cell inside its radius at the stated height, and those cells are constraints
— the relaxation only shapes what is left between them. Marks at radius 16–32 on a 176-wide board nearly tile
it, and the ground builds as stacked plateaus with vertical faces.

Measured off `…/sketch/relief/read`, the same thirty marks at two radii: at 16–32 the board is terraced
throughout with a cliff at every mark's edge; at 3–6 it is **95.1%** walkable at one-block steps and six
cliffs remain on the whole board.


### A range is a wall unless its two gradients agree

A push has two slopes and they are set by different pairs of fields: outside the ring the ground climbs over
the skirt at `amount / falloff` courses a block, inside it from the ring's edge to its medial axis at
`crown / half`. Where the two disagree the landform has a step at its own outline, and a range with a large
`amount` and a short `falloff` is a cliff with a hill on top of it whatever its height.

Measured behind a spawn: `amount 26 · falloff 8` against `crown 10 · half 7` is 3.25 courses a block for ten
blocks and then 1.4, and the section reads as a sheer face on the building's back wall. The same range at
`amounts 13–17 · falloff 10` against `crown 12 · half 7` — 1.7 either side — reads as one mountainside.

**The height a range can be is decided by the ground in front of it, not by taste.** What is available is the
distance from whatever stands in front to the coast behind, and a peak more than about **1.7 courses a block**
above that distance buys the difference with a step at the ring. Twenty blocks at 1.7 is what makes `high 52`
on a board whose ground is 26; wanting 80 there is wanting a wall.

**Setting the spine past the coast puts the medial axis off the board**, so what is on the board is one
uninterrupted climb and the crest reads as being behind the map. Strokes placed from the spine then have
nothing to clamp to, so take those from a crest point inside the outline instead.


### A relief mark's own fields are resolved past `RQ3`, so a wrong field name defaults to nought

`RQ3` names an unread field on a posted document's own path, and a mark's inside is resolved past that walk —
so a `scarp` written with a `line` mark's field names takes `high` and `low` as **0** and pins the middle of
the board to bedrock. The relief read answered `low 0 · high 20 · relief 20` and the export gate stayed
**OPEN**.

**Check a relief against `POST …/sketch/relief/read`'s `low` before building.** A `low` that is not roughly
the group's `base` is a mark that did not land, and it is the only thing that says so.

### A scarp's shelf is on the +z hand of the direction its lip is traced

A `scarp` pins `high` on one side of its line and `low` on the other, and which side is which is the order the
points are written in: the `high` band is the side toward which `z` increases when the line is walked from its
first point to its last — **south** of a lip traced west to east, **north** of one traced east to west.

The field carries no `side` word, so a lip drawn along a beck's north bank with `x` increasing puts the shelf
in the beck and the drop on the bank.

Measured: with a lip traced west to east the bank north of the beck solved at **8–9**
against the 14 it states and the relief read counted **418** barrier steps; the same points reversed put the
bank at 13–14 and the count at 268, which is the two scarp faces and nothing else.

Under `rot_180` the image reverses with the original, so one lip traced the right way is both.

### A scarp with a corner stands a ridge past it, so a zigzag is one scarp per run

**A cell past a corner that points at the low side is nearest the corner itself, and the scarp takes its side
from one of the two runs meeting there.** That run's line, carried on past the corner, puts a thin wedge of
low ground on its high side, and the band pins it high. The wedge comes out as a ridge one block wide, running
diagonally out from the corner at the full height of the face, and nothing reports it: the relief read names
no seam, because it is one mark.

Measured: a lightning scarp of five runs from 12 to 19, turning 45° at each corner, stood a ridge at 19 across
three cells of ground at 12 below its corner at (−6, 42) — (−3, 38), (−4, 39), (−4, 40) — and its image
under the half-turn.

**Stated as one scarp per straight run, the ground past each corner is in neither band and grades between the
two.** The same line split that way solved to no ridge anywhere, and the ground just past each corner came out
a couple of graded blocks — 18, 17, 19 — rather than a column.

### A line mark's reach is either side of the line, and its name is `r`

Not a half-width and not a one-sided band. A `line` at z 50 with `r: 12` writes over everything from z 38 to
z 62, so a mark drawn to make a bank behind a frontline erases the frontline. Halve every reach that was
reasoned about as a corridor. `width` is the same number under an older name, read on the way in and never
written back, so a document saved through the studio comes out spelling `r`.

**`tread` is how much of the band is flat** and **`batter` how steeply the shoulder falls**, which is what
turns a serpentine haul road from flat road and vertical wall into flat road and graded batter.
`techniques/winding-roads` is the worked card, with the pitch window a pass needs.


### A `rim` mark states one height for **every** group in the relief

It is the right instrument for a board whose groups are level with each other and the wrong one
otherwise. To shoulder groups that stand at different heights, draw each one's polygon wider than
the `area` mark that states its top and set `base` **under all of them**: the fringe between polygon
and area is unpinned and decays toward base, so every edge falls a course or two before its drop, at
its own height.

### A relief mark's centre may lie outside the land, and that is how a map edge cuts a mountain

`PointMark.Pins` iterates **its own** bounding box and keeps whichever cells `footprint.Inside`
answers for; `LineMark.Pins` walks `footprint.Land()` and measures each cell's distance to a
polyline that may lie anywhere. So a ridge traced twelve blocks past the coast with a radius of
fourteen pins the coastal strip at its own heights and leaves the crest off the map — and the
board's edge is a mountainside cut through rather than ground decaying to `base`.

On one board three mountain marks lay entirely outside its polygon and a fourth ran out through both ends
of it; every contour band in its heightmap closed on the frame rather than inside it. A mark placed *wholly* out of reach does nothing and raises nothing — no `SK3`, no warning — so
the check is the heightmap, not the document.

### A push's ring has to hold land, or it lifts nothing

A push's falloff is measured from its ring **across the land**, so a ring lying wholly over the void — even one
whose edge touches the coast — has nothing to measure from and moves no cell. No finding is raised;
`POST …/sketch/relief/read` answers each push's `cells`, and zero is a push that landed nowhere. Measured: a
swell of 3 with a 6-block falloff, its ring drawn on the void side of a coast, left the ground under it level,
and the same ring moved to straddle the coast with two rows of land inside rose to the brink and eased out over
six blocks.

**That is the instrument for ground that rises or dips toward an edge**: a swell on a coast, a tilt toward a
spawn along a wall's seam, a lip dipping into a hole. The ring follows the edge two blocks proud of it, on the
land side.

### A held shape's `skirt` is read as the bevel of the mark it pins with

So a pad stated `relief_scope: "hold"` with a skirt is soft at its edge and rigid in its middle, and the
ground arrives on a grade rather than at a face. An `area` mark states the same thing directly as `bevel`,
and two `hold` pads side by side can therefore be ramped between.

### Two flat marks butted together build two terraces and a step at the seam

Two `area` marks at different heights with no gap between them pin their own cells and leave the relaxation
nowhere to make the transition, so the join is a face as tall as the difference. What grades it is a
**`bevel`** on each mark, or a gap between them for the relaxation to slope through.

`techniques/marks-and-seams` is the worked card — what two marks do to the ground they share, and the two
faults the relief read cannot see.


### `step` is the instrument for a quarry, and the terracing that ruins a hillside

`step` quantises a mark's own ground to that interval, which is what a quarry floor and a bench are made of
and what ruins a hillside asked to flow. `techniques/hollows` is the worked card — a negative push, a `sink`
shape and an `area` mark, each cutting the same floor.


### Grain never moves a marked cell, so every pinned area stays machined flat

**`grain` is added after the solve and is not allowed to override a mark**, so it textures only the ground no
mark claims. An `area` mark over a bench, a rectangle band along a lip or a wide pad under a spawn comes out
flat to the block however much grain the group states, and reads as a table set into grown ground.

Measured on one board: a bench pinned by one `area` mark read `level` **0.64** with its largest flat field a
quarter of the group. With the bench unpinned and held up by two low swells, grain of 1.5 over 14 blocks and
three small marks for the spawn, the goal's shelf and the lip, it read **0.24** and **0.08**, and the
heightmap showed rolling ground where it had shown one colour.

**Keep the marks that must be level small, and give every other height to the relaxation, the pushes and the
grain.** The goal's shelf wants a bevelled lobed ring a few cells across rather than a pad, and a spawn's
footing wants the protection region's size rather than the bench's.

### The lip is pinned with a line that wanders, not with a band across the board

**A rectangle band across a destroy board's lip is a flat strip the full width of the board**, and every
contour coming down from the back of the board ends against it at once. It reads as the terrain stopping
rather than meeting the void.

**The build zone is straight; the ground in front of it need not be.** A `line` mark a few blocks inside the
lip, `r` 2, with its course wandering eight to ten blocks in `x` and its heights five blocks in `h`, holds the
lip's height where bridging starts. It also lets the contours run out to the edge at their own angle. A dale
whose floor line ends at the lip needs no lip mark at all: the ridges' skirts and the floor carry the ground
to the edge.

### Two facing bands build a ramp, and at `step` 1 a ramp reads as a staircase

**A constant grade between two long marks is quantised to equal treads**, one block high and as deep as the
grade allows. From above that is evenly spaced parallel contours across the whole slope, which reads as a
smeared ramp or a flight of stairs rather than as ground.

**Low pushes on the slope give it somewhere to drain.** A spur of +3 on an elongated ring five cells wide,
and swales of −3 the same size, each with a falloff of 10–12, bend the contours round them. The slope then
reads as ground with a direction. Grain alone does not do it, because it moves each tread by a block and
leaves the rhythm.

### A line mark does not cut a channel; a negative push along its course does

**A `line` mark pins its band and the relaxation carries the ground either side down to it**, so a canyon or
a gill stated as a line comes out as a valley whose whole width falls to the line's height. Measured: a canyon
line at 14 through a bench otherwise pinned only by a scarp's low band at 28 graded the bench from 36 at the
rim to 14 at the line over about 40 blocks, and there was no canyon to see.

**Carve the channel after the solve, with a push over the band's outline.** Offset the course either side
into a closed ring and push it negative: `falloff` 1–3 is the wall, and the floor follows whatever the solve
left under it, grain included.

**Two bands make a canyon with a ledge.** A wide shallow trough the whole length (±9, −4, falloff 3) with a
narrow slot inside it (±4, −8, falloff 3) steps each wall once. Where the slot is left out the trough alone is
a crossing. A `roughness` of 1.5–2 on both wanders the walls, so they read as eroded rather than extruded.

### A cliff that has to curve is a push, because a scarp is straight

**A `scarp` is straight within one mark, and a corner stands a ridge**, so a curved scarp is several short
runs. It holds where each run turns ten to sixteen degrees from the last.

**A push whose ring is the curve is the other way, and the one that also textures the top.** A spline ring
with its back run off the board, `amount` 12, `falloff` 4 and `roughness` 2, is a rim that follows any course,
with a face that wanders. Its top is the solved ground lifted, so it carries the grain and any swell under
it.

**Lowering the rim for a pass with `amounts` sags a wedge, not a notch.** Each interior cell takes the lift of
its nearest ring point, so a spawn 34 blocks in from a pass whose lift fell off over 26 blocks stood at 30
rather than 38. The pass has to sit where nothing that must stay level has it as its nearest rim point, and
its fall-off radius wants to be short: 18 blocks, forty-five from the spawn, left the spawn at 38.

**The relief read reports that lift as a seam against the spawn room.** It compares the footing mark's
pre-push height with the room, which is seated on the finished surface, and names a step the size of the
lift at the room's edge. A transect across it reads level, so the transect is the one to believe.

### What the relief cannot say

- **A line mark's band is flat across its reach.** A crater rim or a ridge line stated as one is a flat-topped
  ribbon unless its per-vertex heights vary, and nothing grades its top.
- **A push has one `falloff` all the way round.** A landform that is a cliff on one side and a slope on the
  other is two pushes, or a push against a mark.
- **`roughness` moves a skirt's outline and nothing inside the ring.** The top of a push is exactly the
  ground under it plus the lift.
- **Nothing textures a marked cell**, so every level surface that has to be level is flat to the block.

### Water fills whatever is level, so the pan is the size of the pool

An `area` mark 34 × 30 at the sump's height is a 34 × 30 lake however small the `water` prop inside
it. Draw the mark at the size of the water and let the surrounding floor sit a few courses over it.

### A water prop fills its own band, not the level it finds

A water prop states the level it fills to, and it fills **its own band** rather than the pan it stands in: a
level above the ground around it floods outward to wherever that level still holds, and a level below the
bed's own floor fills nothing. The bed is carved first and the fill is stated second.

`techniques/water` is the worked card — five bodies of water and five ways to lose one.


### Relief is keyed by group id across the whole stack, and `*` is the ground's alone

`SketchRasterizer.ReliefFields` walks every layer and looks each of its groups up in the one
`relief` dictionary, adding that layer's `base_y` to the field it solves. So a stacked board can give
each storey its own landscape — `{"team": …, "walls": …}` — and a layer's marks are stated in **its
own frame**, not the board's. `drive.py`'s `"*"` expands over the groups the *compile* emitted, so a
key stated beside it survives and names a layer added in the finish.

### `relief_scope: exclude` takes a tier out of the elevation model entirely

An excluded shape is not ground: the solve does not see it, nothing grades to it, and the tier below meets it
at a face. That is what a made platform wants and what a hillside must never say.
`techniques/made-ground` is the worked card — `relief_scope` against `height_mode`, and which of the two a
shape is actually read for.


### A flight's anchor is an absolute height, and the relief does not know about it

A flight states the height it starts from as a number, and the relief solve knows nothing about that number:
move the ground under it and the flight stays where it was told, landing proud of the pan or buried in it.
`…/walk` is the read that says so. `techniques/ramp-and-stair` is the worked card — a tilted polygon against a
stack of plates, and which one walks.


---

## Shapes

A shape is drawn on a layer and resolved against every other shape there. Its height, its edge and its footprint are three separate statements, and each has its own field.

### `base_height: N` puts the top block at `y = N−1`

Confirmed at every tier on every board that has traced a real map. Any plan matching absolute heights is one
low until this is applied.

### Among the shapes of one layer, the taller override-add wins the column — not the later one

`RasterGroup` resolves a layer as `((adds − subtracts) ∪ override-adds) − override-subtracts`, and both sets
are accumulated through `MergeCell`, where **the taller surface wins**. Only the *set* an override-add belongs
to is privileged; within that set, document order decides nothing.
`techniques/combined-shapes` is the worked card.

**So a wall that meets a ramp is drawn in halves, one either side of it.** An end wall drawn as one rectangle
across the mouth of a ramp is 15 courses where the ramp under it is 7, so the wall wins every column they share
and the way down ends in solid rock — measured, a three-block plug sealing both mouths, with `SK11` reporting
676 and 294 places of standable ground with no route onto them. The general form: on one layer, anything
shorter than what crosses it is not in the world there.

The cheap check is a column transect down the way in. A ramp that works reads one course of fall every two
blocks the whole way; a plugged one reads a solid run where the air should be, and the export gate stays open
either way.


### A subtract's `floor` and `base_height` are not read: the whole column goes

`RasterGroup` resolves the subtract side of a group as a **set of columns to delete**, so the shape's own
height never enters the calculation — `base_height: 1` and `base_height: 40` on one footprint carve the same
channel. Only the shape's own bounds are checked, and `SK5` complains about a height past the world roof
while carving exactly as before.

Relief moves a surface and a subtract removes it. What puts ground back over a cut is an override add at a
floor **above** the subtract's, which bridges it; the same shape at the cut's own floor refills it.
`techniques/cutting-a-hole` is the worked card.

### A ring is one polygon, and it is what a floor that rises or a surface that falls is drawn with

Nesting settles a contest by height — the taller add wins the column and brings its own floor — so nested
shapes write any field that **rises** inward from one shared floor with no subtraction and no complaint. A
ziggurat, a cone and a solid dome are all that one move.

**A rising floor is right in the world and wrong in the report** (every nested pair is a span the layer had to
drop: eleven discs as a hollow dome raise **sixteen** `SK9`), and **a falling surface is wrong in the world and
silent** (eleven nested discs as an amphitheatre build a flat plate 22 cells across, with no finding of any
kind).

**What both cases want is shapes that do not overlap, which is what a ring is.** An outline is filled even-odd,
so one polygon — the outer circle, a slit inward, the inner circle the other way round, and back — is an
annulus with no subtract in it. `techniques/sculpture-with-layers` is the worked card.


### An override add is still part of its group's relief

Override decides who wins the column among the shapes on a layer and says nothing about the solve, so a
relief's surface replaces the top of a wall, a flight, a hill or a rim as readily as it does bare ground.

A made thing keeps its stated top with `"height_mode": "level"` and `"skirt": 0` — level for an absolute
top, skirt zero for a sheer face — because an erected shape is applied over ground the relief has already
made. A shape with no `height_mode` says the same thing as `relief_scope: "exclude"`, which takes its
footprint out of the solve. One or the other, never both.

`SK14` names an override add carrying neither, which is what leaves a twenty-seven-course wall level with the
ground beside it.

### An override add standing in ground keeps the ground under its floor

An override add overwrites the column it lands on, and where the ground's ordinary span reaches the override's
floor the built column runs from the ground's floor to the override's top. So a wall traced along a lip may
state a floor a few courses under the bed — `floor: 12` against a bed at 17 — and the bed is still under it.

A deck stated above the ground's top keeps the air beneath it, and a slab over open void still lays the
bedrock plate below.

Measured: canal walls, a spawn stair and cairn walls standing over a void from y0 to their floors cost
25,000 blocks of hand fill under them, where the same layout with the ground kept costs none.

### `skirt` decides whether an erected shape is a landform or a monument

Probed on flat ground: a `skirt` of **0** builds the edge as one sheer step of the whole lift, a skirt of about
**half the lift** builds two-block risers, and a skirt **at or over the lift** builds one-block risers all the
way round. So `raise 7, skirt 10` is an outcrop a player strolls up and `raise 7, skirt 0` is a standing stone,
from the same two fields.

**`skirt` is one number for the whole outline**, so an outcrop is uniformly walkable or uniformly steep;
`anchor_heights` tilts the *top*, not the edge, and there is no per-vertex skirt.

**Grass painted back over it is the rest of the merge, and it is free.** A path prop replaces the surface
finish and adds no cell, so two to five `worn` brushes with a grass pave, drawn as tongues over a crag's
shoulders, let the rock show through instead of the grass stopping dead at the shape's outline.


### An erected shape is the pillar idiom, and its theme has to go in `fill`

`height_mode: raise` with `skirt: 0` and `floor: 0` is one abstract monolith: the top stands a stated amount
over whatever ground the footprint covers, the face is sheer on every side, and `anchor_heights` slants that
top per vertex. Leave `controls` off entirely and the corners stay sharp, which is what makes a stone read as
broken rock. This is a **different device** from a stack of plates at successive `base_height`: plates are a
staircase, a raise is a thing standing in the terrain.

**Put the pillar theme's `layered` stack in `fill` as well as `surface`.** The surface bucket is the top few
courses, so a stack stated only there bands the head of a 30-block monolith and leaves the whole face plain —
and the face is the entire point.

**And take the pillar out of the ground's tone family.** On a board whose exposed ground is stone, a pillar
painted andesite and cobble is terrain wearing a different seed, and `render/surface` shows it as ground. The
rule the brief states for a building is the rule for an erected landform too.


### `height_mode: sink` is a quarry, and its anchors are its depth

`sink` cuts the footprint into the ground it stands on and `anchor_heights` states how deep, so a quarry, a
dock and a sunken yard are one shape rather than a subtract and a refill. `techniques/hollows` is the worked
card — a negative push, a `sink` shape and an `area` mark, each cutting the same floor.


### `height_mode: raise` measures from the median ground under its whole footprint

`relief.md` §7 states it: the top is a fixed amount above "the ground under it, **read at the covered
cells' median**". One number for the shape, not a value per cell. The consequence is the one that bites
on a slope — the median is the middle of the range the footprint straddles, so an outcrop lying across
a terrain step stands `median + anchor` high while its foot on the low side is much lower, and the face
a player meets there is the lift **plus the step**. A crag with a lift of 7 across a nine-block step
read as a fourteen-block wall, and no readback mentions it.

Level the footprint first — an `area` mark at the shape's own ring, grown about 1.3× — and the median
is the pad, so the whole face is the anchor plane where it was stated, with the pad's own edge left to
the solver's one-block stairs.

### A raise over void builds from its own floor

Past the coast there is no ground to read, so the column falls back to the shape's `floor` and a ring
that overhangs the sea by two cells builds two seven-block stubs at bedrock beside the group. It is
terrain, so nothing declines it. Audit every ring for sea cells as well as hole cells before using it.

### A mark cannot make a vertical-sided spire, and an excluded shape can

Every mark is a constraint the relaxation smooths *through*, so a point mark makes a cone. A shape carrying
`relief_scope: "exclude"` and no `height_mode` leaves the field entirely — the solver bends round it as it
bends round the void — and keeps the column it was drawn with: a flat crown on vertical sides, joined to
nothing. A `height_mode` of `level` states the same crown at an absolute height and is the other way to ask.

### `relief_scope` is not read on a shape that declares a `height_mode`

They are alternatives rather than a pair. A `height_mode` says the shape stands **out** of the field, applied
over ground the relief has already made; a `relief_scope` says how a shape that is part of the ground takes
part in the solve. A shape stating both has the scope ignored silently — `ScopeOf` returns `Inherit` for any
shape declaring a height mode, so the field binds and is never consulted, and `RQ3` does not fire because it
was read and discarded.

The scope's words: `follow` takes the height the field settles on under the shape and holds it flat there,
`hold` pins the stated height against the relief, `exclude` takes the footprint out of the solve, and absent
is `inherit`. `techniques/made-ground` is the worked card.

**`follow` is not the gentle option: it seats the shape and then solves the group a second time.** `SeatOf`
takes the **median** of the field just outside the footprint, pins that as a rigid `AreaMark` and re-solves,
so the land around a `follow` shape is re-graded to arrive at it exactly as `hold`'s is. On a hillside falling
26 to 10, a piece stating 24 came out at **18**, which is in no document.

**`exclude` keeps the raw column, and the raw column is not the excluded shape's.** The taller add still wins
the column; the word only says the relief may not answer for those cells. A shape wanting a plinth at its own
height has to be the taller add there, or say `height_mode`.

**A `skirt` is paid for from every side at once, so one over half the shape's narrow dimension leaves no top.**
On a 26-deep plate: `skirt` 0 leaves all 26 cells at the stated height, `skirt` 6 leaves 15, and `skirt` 14
leaves **2**. Same arithmetic as a mark whose `bevel` is wider than half its band.

**The relief read cannot see an erected shape at all, and `RL5` will say so out loud.** Eight panels differing
only in these words all read `relief` 16 and `landform: rolling` while the built worlds ran from a bare
hillside to a 44-block plinth — and `RL5` fired on the one carrying a ten-block sheer plate, calling it a ramp
end to end, which is true of the solve and false of the world.


### A ramp between two tiers is four fields and works first time

`height_mode: "level"` plus `anchor_heights` is a tilted plane — vertices in order, one height each:

```json
{ "id": "ramp-d", "type": "polygon", "operation": "add", "floor": 0,
  "base_height": 22, "height_mode": "level", "skirt": 0,
  "vertices": [[-46,68],[-34,68],[-34,82],[-46,82]], "anchor_heights": [22,22,26,26] }
```

Measured down `x = −40`, joining a shelf at 22 to a crest at 26: z66 → y20, z70 → y22, z74 → y23, z80 → y25.
A path prop laid over it paves the slope, so the ramp reads as a built stair. Four of these turn a stack of
terraces from a series of one-way drops into a zigzag climb.

### A ramp at one course a cell builds as treads of two, and a two-block rise is a placed block

A ramp falling one course per cell rasterises as treads of two, because a cell is two blocks and the fall is
taken once per cell: what a player meets is a two-block rise, which is a placed block rather than a walk.
**Run at least twice the rise** and the treads come out one course each. `techniques/ramp-and-stair` is the
worked card, with the same climb built both ways.


### Three points and a plane is how you tilt a shape deliberately

`anchor_heights` states a height per vertex, and three points define the plane the rest of the shape is fitted
to — so a deliberate tilt is three anchors chosen for the plane you want rather than a number per corner
adjusted until it looks right. `techniques/ramp-and-stair` is the worked card.


### `rot_180` maps a shape centred on the origin onto itself, so a central lake may be any shape

The mirror does not force a circle; assuming it does is what produces one. Any outline with a
half-turn in it is already symmetric, so a profile of radii covering **half** a turn, repeated at
θ+180°, gives a lobed, elongated or kidney-shaped water that fans without error. Smoothstep between
the profile's entries or the outline comes out faceted, and give the helper a `swell` so an outer
ring can depart from a circle less than the waterline while staying the same shape — that is what
keeps a beach an even band round a shore that is nowhere an arc.

### A made layer is built once unless its group says it mirrors

A layer's shapes are fanned onto the symmetry's orbit axes only where the group carrying them has
`mirrors: true`. A group is the unit, not the layer and not the shape, and both `SketchGroup.Mirrors` on the
wire and `tools/sculpt/props.py`'s `LayerBuilder` default it to `true`, so everything a team owns is fanned
without asking. Every factory in that module forwards `**kw`, so `mirrors=False` is how a landmark seated on
the symmetry centre says it is already its own image.

**Nothing reports the difference.** The store answers 200, `preflight` opens, and its mirror check reads
spawns, wool rooms and build zones rather than made geometry, so a curtain wall, a gatehouse or a cloister
built for one team and no other passes every gate the pipeline has. On a `rot_90` board three of the four
teams simply have no castle; on `rot_180` one side has one and the other does not.

`GET /api/map/{slug}/column` is what sees it, and the image coordinate has to be exact: the reflection of
block `z` is **`−z−1`**, not `−z`, so under `mirror_z` the image of `(x, z)` is `(x, −z−1)`, under `rot_180`
it is `(−x−1, −z−1)`, and under `rot_90` it is `(−z−1, x)`. Probing `(x, −z)` lands one block off the
image and reports a difference on a board that is exactly symmetric.

A structure that *is* its own image — one centred on the origin under `rot_180`, or on `z = 0` under
`mirror_z` — keeps `mirrors: false`, and then its own shapes have to be symmetric too: eight causeway
trestles at `z −10, −5, 1, 6` are not, and the deck above them is, so the two teams meet a neutral
crossing propped at different spacings.

### A group that does not mirror stamps its shapes once; its dressing still fans

Two different rules, and they are easy to swap. `SketchRasterizer` mirrors a shape only when its
**group meta** says `mirrors`, so a middle group built as its own `rot_180` image stamps each of
its shapes exactly once — a second crag on the far lobe has to be written out,
`[[-x, -z] for x, z in ring]` with the same anchor heights, which turns the plane with the ring.
`Decorator` fans **every prop over the map's symmetry order** regardless, so a stand of trees on one
lobe is already the stand on the other, and scattering a second one there finds no room.

### Bending is a roughener; reshaping is per vertex

A bend moves every cut point on a ring at once by a formula. That is right where a whole edge should read
rougher and wrong where one place should differ from the others — pulling a bay, widening one flank, cutting
the notch a lane runs through. Those are one point each, and a bend does them by making the entire outline
uniformly wobbly and the one place unchanged.

The three routes are `PATCH …/shapes/{id}/vertices/{index}` (move one point), `POST …/vertices` with
`{"after": n, "x": …, "z": …}` (add one on that edge; the answer says the index it landed at) and
`DELETE …/vertices/{index}`. **Every other point of the outline is exactly where it was drawn after each of
them**, which is the property the whole thing exists for: a board's shapes abut, and an edit that drags a
ring's other points opens ground between two that were flush. `techniques/flat-ground` is the worked card.

State the point in the insert rather than splitting first and moving second: the one call is atomic, so a point
that would fold the ring leaves the outline untouched. Omitting `x`/`z` is the midpoint anchor — a corner half
way along a wall, placed before it is decided where it goes.

**A spec states them under `editShapes`**, an ordered list per shape replayed after the store and **before**
any bend, since a bend resamples whatever ring it is given. Each op names exactly one index — `after` inserts,
`index` moves, `remove` drops — and one naming none or two stops the run rather than guessing. The indices
shift as the ring grows, which is why the run prints where each point landed.

**A hand works at a larger scale than a bend does.** One board's four ground shapes, reshaped by hand from four
vertices to between six and eleven, grew 14,250 blocks² of compiled rectangle into 16,008 drawn — and of the 36
drawn vertices, 19 sit outside the rectangle they came from by 2 to 20 blocks. That is not reachable by any
whole-ring transform, and it is reachable one point at a time.


### The bend is the studio's, and the side is the author's

`POST …/shapes/{shapeId}/bend` draws a compiled outline as a coast. **The outline's own vertices never move** —
that is the rule that makes one safe, and it is the studio's.

Which way the cut points go is `side`: `out` is the default and is the slight bloat that makes a compiled
rectangle read as land, `in` keeps the plan's footprint where shapes abut on a measured strait, and `both`
wanders across the line the plan drew. The side is decided by offering each inserted point both perpendiculars
and taking the one that lands where it was asked to — right for a ring wound either way and for a concave
stretch as readily as a convex one, which a shoelace sign is not.


### A vertex insert names the edge leaving that vertex, and the index moves under it

`POST …/sketch/shapes/{id}/vertices {"after": n}` inserts on the edge from vertex *n* to *n+1*, so the index
to state is the one **before** the edge wanted — and after a run of inserts it is not the index that edge
started at. Ten inserts on a six-vertex ring put the west flank at index 9 rather than 8, and `{"after": 8}`
landed on the board's own back edge and folded the ring.

A folded ring refuses nothing. The store answered 200, the export answered 200, `preflight` answered **export
gate OPEN**, and the world carried **ten blocks of void inside the landmass** at `x −30, z 40..49`. A transect
is what found it. Count the indices as the ring grows, or read back the index each insert answers with.

### Bézier `controls` — the semantics, and where the curve actually is

`controls` is per vertex and states the handles of the curve leaving that vertex, so a ring's curve lies
between its points rather than through them: the drawn outline is what the vertices *suggest*, and the built
coast bulges outside the ring on a convex stretch and inside it on a concave one. Anything measured against the
authored polygon — a prop's footprint, a strait's width — is measured against the wrong line.

`techniques/curved-outlines` is the worked card, with the tangent continuity a closed ring needs and what each
handle length does to the coast.


### A corner recipe does not make a coastline: a closed ring wants tangent continuity

Handles chosen per corner give a ring that is smooth at each vertex and kinked between them. What a coastline
wants is the handles of the edge arriving and the edge leaving to be collinear at every vertex, which is one
rule over the whole ring rather than a recipe per corner. `techniques/curved-outlines` is the worked card.


---

## Layers

A layer is a slab keeping one span per column, so a cell may be on several and the air between them is the feature. What reads a stacked board reads one number per column, and that is where the surprises are.

### A layer is a slab with its own base_y, and the air between two of them survives

`layers[]` replaces the legacy single `layout`: each entry is `{id, name, base_y, layout:{shapes,
groups}}`, and a cell's column is that layer's `[floor, top]` shifted by `base_y`. The same `(x, z)`
may appear on several layers, which is the whole feature — two solid spans in one column with air
between them.

```python
if not layout.get("layers"):                     # the compiled document carries `layers: null`
    layout["layers"] = [{"id": "ground", "name": "Ground",
                         "base_y": 0, "layout": layout.pop("layout")}]
layout["layers"].append({"id": "terrace", "name": "Terrace", "base_y": 20,
                         "layout": {"shapes": [...], "groups": [...]}})
```

**Pop the old `layout` key.** `SketchRasterizer.ResolveLayers` reads `layers` *or* `layout` and
returns on the first, but `SketchLayout.IslandIds` reads both without an early return, so leaving it
behind doubles every group id.

**`floor` is the underside**, measured inside the layer: `base_y 20` + `floor 4` is a soffit at y24, and the
slab's thickness is its solved surface minus that.

**Relief solves per layer**, keyed by group id, and `ReliefFields` shifts the result into world Y before
returning it — so `relief/read` answers an upper group in world coordinates.

**The gap survives because `TerrainPainter.Paint` writes only over stone.** Its band stack runs
bedrock-to-top and would fill the air between two slabs; the stone-only invariant is the one line
that makes stacking work.

### The order a stack is written in decides which layer an unnamed shape joins, and nothing else

`TerrainPainter.Paint` orders the layers by the lowest surface each one carries and paints each over its
own span, so a storey's bands stop at its own floor and the document's order is a tiebreak between layers
standing at one height. A storey listed after one that stands over it is painted correctly either way.

What the order still decides is where a shape naming no layer lands: the first one. `drive.py`'s `addLayers`
takes `"below": true` to insert a storey under the compiled ground, which moves that target, so a finish
adding an undercroft states the layer its shapes belong to rather than relying on the position.

**`SK20` complains where the list is not in the order the world builds.** The list is what a reader and the
storey strip walk and `base_y` is what the world is built from, so the two disagreeing is worth saying even
though nothing is lost. A sculpture drawn out of layers has no stacking order to be in, which is what
`kind: "made"` says.

### Two layers may share one course and no more

A layer's segment top is `base_y + base_height` while its built top block is one lower, so two layers whose
spans meet exactly share one course and build correctly. **One lower than that is `SK10`**, and the slab is
absorbed exactly where the layer below reaches it. `techniques/stacking-layers` is the worked card — two solid
spans in one column, and the three ways the air between them is lost.


### `kind: "made"` and `seat: "ground"` are what a layer says when it is a thing rather than terrain

A layer with no `kind` is ground, and every stacking rule is written for ground: `SK10` reads two layers
whose spans meet as a lost gap and `SK11` reads an overhang as standable ground nothing reaches. Neither is
true of a sculpture, and `kind: "made"` is what takes the layer out of both walks. Measured on one board of
twenty made things, all fourteen `SK11` findings were ground layers — a torus on edge, a hollow sphere and a
wheel raised none between them.

**`seat: "ground"` is what puts one on the ground, and it reads the ground itself.** A shape on an ordinary
layer states an absolute floor, so on a grade it is buried at one end or hanging at the other whatever
number is chosen. A seated layer is dropped until its lowest floor is one above the lowest ground under its
footprint, and the terrain under that footprint is then **cut to that course**, so the thing beds in rather
than perching on the uphill side.

Measured on one grade: a crate stated at `base_y` 15 — read off `POST …/sketch/columns` as the highest ground
under it — came out brick y15–19 over a gap at y14 and grass at y13. The same crate ten blocks away stating
no height at all came out brick y12–16 on grass at y11, where the grade beside it tops at y13.

**`part_of` is what keeps a thing in one piece.** A sculpture is one thing to an author and many layers to
the rasterizer, and layers naming the same `part_of` are seated together over the union of what they cover —
without it a two-layer wheel would be seated twice, by different amounts, and come apart at its run boundary.

### A thing that cannot be drawn is written as a solid and compiled, and the layer count is then measured

`tools/sculpt/solid.py` states a model — boxes, ellipsoids, frusta, tori, revolves, swept tubes, lifted
sheets, and union, intersect, difference and shell over them — and `tools/sculpt/layers.py` compiles
`{(x, y, z): material}` into layers by run index. Nothing states a layer count: a column's blocks split into
maximal runs of one material, the n-th run of every column goes on layer n, and the stack is as deep as the
busiest column is complicated.

**On a shape a hand would have drawn it draws exactly that**, which is why it is the top of one ladder rather
than a second system: a 32 × 2 × 7 wall written as a `box` compiled to **one layer and one rectangle**, the
same rectangle the hand states. A torus on edge came out two layers and 116 shapes from 1,472 blocks; a
hollow sphere two thick, two layers and 190 shapes — two runs is what a hollow ball has, whatever its radius.

**What it costs is editability and `SK23`.** A compiled document is rectangles that happen to look like a
wheel, where a drawn one is a circle with a radius an author can still drag; and every compiled shape is a
thin strip, so 217 of one board's 240 `SK23` shapes were the compiled four of twenty panels. A compiled
thing wants a solid theme or a material, never five buckets. `techniques/sculpture-with-layers` is the
worked ladder, one shape to a compiled solid.

### What a made thing costs in layers is its columns, not its palette

A layer holds one span per column and a run of one block is what a span is, so the question a layer count
answers is how many separately-painted runs the busiest column of a thing passes through.

Measured on one box, 12 × 12 and nine courses: one paint is **one** layer; the same box in three horizontal
bands is **three**, because its column reads sandstone, then stone brick, then planks, and a layer cannot
hold three; three paints as three boxes side by side is **one**, because no column passes through two of
them. A solid with one run per column is one layer of geometry and as many of colour as it has bands.

### Everything downstream of a stacked cell reads one number: the surface top

Every read and every pass past the rasterizer takes a cell's **surface top** and nothing else, which has four
consequences. **A placement climbs onto the upper layer by itself.** **The covered ground keeps its own
paint**, because the painter hands each layer its own floor. **A covered floor is not in `themes/census`**, so
a board's paint figures are about its roofs. And **the covered ground cannot be dressed** — the pass seats on
the surface top, so nothing can be placed under a deck.


### A ground ramp meets an upper slab by touching it, and nothing else is needed

**Overlap the two footprints by a column** and the ramp arrives: no join, no shared course, no field to state.
**`SK11` at the store door is what reports the miss**, and it is silent on the join itself — a ramp that lands
one block short reads as standable ground with no route onto it.


### Lifting the ground to make room for a storey under it is a plan edit as well as a finish edit

`shapePropsByHeight` moves the landmass's **floor** and leaves its surface where it was, which is what makes
room for a storey underneath. The plan states where the spawns and the goals sit, so moving the finish alone
leaves every marker at its old height under ground that has risen — thirteen courses under, on one measured
board — and the buildability check then reports every placement as over open void.

**A placement reads as over open void unless its column has a span at Y = 0.** A storey resting at `floor: 1`
leaves the whole board without one, so the board that looks right in a section answers wrong at the gate.

### The bedrock floor goes under what rests on it, and under nothing else

`TerrainBuilder.Build` writes bedrock at y0 under a column whose own floor is the bedrock course or the
first block over it. A bridge slab across a strait, a deck overhanging a court and any layer standing at a
`base_y` of its own stand on nothing and are plated with nothing, so the fall under them stays void and those
columns stay out of the Y0 set a void filter reads.

A one-thick slab at `floor: 0` writes no stone at all and the bedrock is its whole ground, which is why the
test reads the floor rather than what the fill wrote.

Measured on a deck oversailing its court by four columns: out past the court's edge the column is **one solid
block** — the deck's own course, no fill under it and no bedrock. `techniques/stacking-layers` is the worked
card for all of this.

### A channel's line is the lowest surface its band crosses, and everything over that line is emptied to it

**This is the one sentence most of a water prop's behaviour follows from.** The body takes the lowest surface
its band crosses and empties every column over that line down to it, so **a channel run down a fall is built as
a trench, not as a beck**. **A bridge is bitten through only when the prop names no layer**, and naming one is
the whole fix — every prop kind takes the field. `techniques/water` is the worked card.


### A prop's claim is a claim of one storey

`GroundClaims` is keyed on the layer as well as the cell and each placement is handed one storey's
view of it, so two props are in each other's way only where they share ground: a building on the
`deck` layer at y38 and one on `ground` at y18 do not collide, and neither does an oak on a floating
group and the river under it. `DR-CLAIM` and `DR-ROAD` both read that book, so the standoff to a
road is measured against roads on the prop's own storey. Two props on the **same** layer still have
to be moved apart in plan.

### A goal states its storey on the plan

`DestroyablePlacement` and `CorePlacement` carry `layer` beside `id · piece · at · style · materials ·
float · name`, and the compile carries it onto every orbit image. A goal naming none resolves against
`SurfaceTop` — the highest layer — so a monument stated for a hall lands on the deck roofing it, with
nothing declined:

```python
{"id": "destroyable-1", "at": [-16, 56], "layer": "under", "style": "pillar-2", "float": 2}
```

Naming a layer the board has no ground on is a `DR-LAYER` decline for a prop; for a goal it is the
top surface again. A wool's or a spawn's storey has no plan field yet and is still the intent's.

### A stroke ignores `layer`, so a floor with a roof over it is marked with a shape

A stroke reads the surface top of every column it crosses, whatever layer that top belongs to, so it cannot be
kept to one storey. **Mark a covered floor with a shape instead** — a shape states its layer and a stroke does
not.


---

## Painting

A theme is stated on a shape and a cell goes to one of them. What decides which is not what decides the column's height, and the two answers differ more often than they agree.

### Height and paint resolve overlaps by *different* rules

Height goes to the **taller** shape and paint to the **smallest themed** shape whose top is that tallest top,
so the shape that owns a cell's height and the shape that owns its paint need not be the same one. **Check
which way round each join sits before building.** `techniques/combined-shapes` is the worked card.


### A shape owns the paint on a cell only where its own drawn top is the tallest drawn top there

The paint of a cell goes to the smallest themed shape whose **drawn top** is the tallest drawn top there, so a
patch that is shorter than what it lies on paints nothing. **A shape stating no height at all is one course at
bedrock, not "no opinion"**, and **`override: true` does not rescue a brush that is too short** — override
decides a set, not a height.

**So the form a patch takes is the ground's own `floor` and `base_height`, and the relief settles the height.**
A shape declaring a `height_mode` is a candidate whatever its height and is never flush, which is why a patch
meant to lie in the ground must not declare one. `techniques/painting-a-patch` is the worked card.


### A fill pattern is a plane until it states a `rise`, and the gate now refuses one without

A sampled field with no vertical period resolves every block of a column alike, so a face of it comes out in
vertical stripes. **`PT4` refuses a fill or wall pattern that states no `rise`**, and two or three courses
against a `cellSize` of nine or ten is what the committed bodies use. **`PT1` refuses a surfacing block as a
band's whole material** — grass belongs on top of a stack, not inside it.


### A voronoi's bands are rings inward from a cell boundary, and the last one takes the rest

`VoronoiMaterial.Resolve` walks the band list and stops **one short**, returning `Bands[^1]` for
everything the earlier bands did not claim. The value it walks is the Worley `F2 − F1` gap — small
against a cell boundary, largest at a cell's centre — so the bands are **depths measured inward from
the boundary**, not weights over an area, and the last band's stated thickness is read by nothing.

So `voronoi(seed, 7, [(SAND, 4), (RED_SAND, 2), (GRAVEL, 1)])` is not *sand with a seventh of
gravel*; it is a **gravel bed with sand along the cracks**, because gravel takes every cell interior.
Write the ground the board is made of **last** and put the veining before it:
`[(GRAVEL, 1), (RED_SAND, 2), (SAND, 1)]` is a sand wadi with gravel in the cracks and a red margin
round each patch. A voronoi is a diagram, not a mixture.

### A theme has no bucket keyed on elevation, so rock above a treeline is a second shape

A relief moves the surface inside one shape and a theme is scoped to a shape, so nothing paints by altitude:
`layered`'s axis is `depth` or `inward`, and a pattern's `rise` makes its field three-dimensional rather than
selecting by height. Ground that changes material where it gets high is a second shape standing where the
high ground is, with `relief_scope: "hold"` and its own theme.

### A cliff's strata belong in the `wall` bucket, because a cliff is what that bucket paints

**The wall is the column's body at an edge, not a coat on a slope**: the bucket paints the face a drop
exposes, so a cliff's strata go there and nowhere else. **`rimEdges` decides how much the rim claims and the
difference is large** — `void` caps every edge over nothing, and a piece standing over void is rim all the way
round. **A `height` stack leaves everything under its own `from` to the bucket beneath**, and one block is
enough. `techniques/theme-buckets` is the worked card, one bucket at a time over one ground.


### A shape thinner than three cells has no interior column, so a theme paints it out of two buckets

A column is interior only where it has ground on all eight sides, so a wall two cells wide has none: every
column of it is an edge, the rim and the wall are the only buckets that reach it, and the theme's surface
stack is nowhere on the thing. `SK23` says so at the store door and names the layer and a coordinate.

Measured side by side on one board: a rectangle stated at ±1 comes out **two** cells wide and every column
reads chiseled brick over plain — rim, then wall — while a polyline of radius 1.5 beside it comes out
**three**, and its middle column reads mossy brick, plain brick, then stone: surface, then fill. One cell of
width is the difference between a theme using two buckets and one using four, which is why a thing thinner
than that is painted with a material instead.

### A shape that states a `material` and no `theme` is counted under the ground it stands on

`GET …/themes/census` files a cell by the theme of the group it belongs to, so a shape carrying only a
`material` never appears as its own entry. On one board of sixteen pads the ground theme came back with
**seven** distinct surface blocks — grass, sandstone, planks, stone and three bricks — because four
sculptures on it were painted by material rather than themed, and the themed ones accounted for the other
entry's two.

### `globals.surface` is a floor and the theme's `surface.depth` is a thickness

They are different numbers and they interact: a board flattened at 9 under a stack 9 deep has exactly
one stack's worth of ground, so a coast rim cut one block into it leaves two blocks standing over the
void. Raising the plan's surface is what buys the stack room to be a soil profile — turf, dirt,
gravel, rock — which is what a cliff face is made of when `rim` and `wall` are both off.

### A theme and a house style are snapshots, and `RQ3` does not reach inside them

Everywhere else, a field the studio did not read comes back named. A **theme** and a **house style** are
stored as opaque snapshots, so a misspelled field inside one is dropped in silence and the pattern renders as
a flat swatch at 200.

**`GET /api/terrain/patterns` is the field list** — fourteen kinds with their exact field names. The ones that
have been guessed wrong: `noise` takes `stops`, not `palette`; `voronoi` takes `bands` of `{material, depth}`,
not `palette`; `checker` takes `even`/`odd`, not `a`/`b`; `layered`'s axis is `axis`/`beyond` over a `stack`,
and there is no `inset`; `teamTint` takes `blockId` and `neutral`. Read the endpoint rather than the type name,
and preview what you wrote: `POST /api/terrain/material-preview?format=png` answers the pattern as an image.

**A theme's `fill` is what fills a tall shape; the surface is only its top courses.** A 44-block hoodoo banded
through `surface` alone comes out banded in its top four courses and plain below. Put the `layered` stack in
`fill` as well and the strata run the whole column.

**A style fork that repaints `wall` and not `storeys[*].wall` is half a fork.** The storey stack carries its
own wall, and on a two-storey preset the storey is most of what a section shows. The exception is `Stilts`,
whose whole idiom *is* storey 0's wall (air over a beam course) — repaint that and the stilts disappear.

---

## Buildings

A house is placed by hand rather than scattered, so the gates that filter a prop do not filter it.

### A room's building defaults to its piece, and `footprint` separates the two

`WX1` makes the shell the piece rect inset one block on every side where the placement says nothing, so
a **20 × 20** spawn piece stamps an **18 × 18** house — a hall, not a spawn hut. `WoolPlacement.footprint`
and `SpawnPlacement.footprint` state it instead, as `[x, z, w, h]` in blocks from the piece's minimum
corner; `WX12` refuses one that reaches outside its piece, and `ST9`'s cap reads the rectangle the export
actually stamps — the stated one, or `WX1`'s default. So a wide protected apron with a small house on it
*is* expressible, since the piece is still the protection region and the spawn's own ground.

*Measured: `[3, 3, 12, 8]` on an 18 × 14 piece, and `POST /plan/inspect` answered
`wool-cage minX -29 minZ 73 maxX -17 maxZ 81` before a map row existed.*

Watch the marker parity while shrinking it (`WX3`): a piece of an even number of cells takes a whole
`at`, an odd number takes a half, and mixing them refuses.

### A placed building is capped at 192 blocks of wing, and a storey wall at `clear + 1` courses

The cap is on the wing's own length, and a storey's wall is `clear + 1` courses whatever else the style says.
**`POST /terrain/prop-preview` is the read for a multi-wing house** — it answers the whole building against a
theme without building a world.


### `DR-SLOPE` is gated on the building's own height, not on the wall it stands against

A house straddling the rim of a pit eats the wall. The decline fires at a rise of `wallCourses + 2 × roof
pitch` — 7 for a one-storey shell, 13 for a two-storey one — so **the taller the building, the deeper the
pit wall it may quietly carve away**. A one-storey shell is refused at rises of 11 and 12 where a two-storey
one is allowed all three.

Built, the column under such a house has lost every course above its floor while the column one cell outside
the footprint is whole. Check a footprint against the rim it sits on rather than against the rule.

### Wing corners are inclusive, and the joint roles are ridge-derived

A wing's rect is inclusive at both ends, so a wing stated the way a rectangle usually is comes out a block
longer than intended. **Which rectangle is the hall and which the wing follows from the ridges**, not from the
order they are written: **a roughly square hall ties its ridge `AlongX`, which is `HJ4` waiting to happen.**
`techniques/a-house-and-its-wings` is the worked card, with all five `HJ` refusals.


---

### `roomStyles` has three states and the third one is silent

`roomStyles` binds a shell for `wool` and for `spawn`, and each of the three things it can say means
something different: an **object** is the bound style, an explicit **`null`** is open ground with no
building, and an **absent** key is that kind's built-in shell — a bedrock box.

The third is the one that costs a build, because nothing is wrong with the document. A board whose key the
studio does not bind stores at 200, pre-flights **OPEN**, exports at 200, and builds its rooms as the box:
`y24 Bedrock · y16 Bedrock` where the bound style reads `y26 Bricks · y16 Gravel`.

Two things now say so. The per-part route refuses an unknown part outright — 400, *"a map binds a shell for
wool and spawn, and nothing else"* — and the whole-layout write names the key under `RQ3`, because the
unread walk descends into the type and reports a property it has nowhere to keep. Read the `RQ3`s and a
mis-keyed shell cannot reach a world.

### A house style in a dressing document is not a house style

`roomStyles` takes a bare `HouseStyle`. `dressing.styles` takes a `PropStyle`, which is polymorphic — so the
same document two keys away needs the discriminator: `{"kind": "house", "shell": <HouseStyle>}`. Without it
`DressingJson.ParseStyles` throws and the answer is **500 / `RQ2`**, the studio's own fault rather than the
document's, with the field that caused it named only in the server log.

---

## Dressing

The dressing pass seats props against a book of claims. A decline arrives on a 200 and means the thing is not in the world, so what the pass will refuse is worth knowing before it is asked.

### A thing built out of terrain has to say so, or a road and a river will eat it

An override add on the ground layer — a town wall, a crop bed, a well's rim, a flight of stairs — is written
by the painter with a theme like any other ground, so nothing separates it from the sand beside it.

A stroke repaints the top block of every column it crosses, and a channel takes the *lowest* surface its band
crosses as its water line and cuts every other column in the band down to it: a wall standing seventeen
courses over a river comes out as a hole through the wall, filled with water.

Mark such a shape `keepClear` and its columns join the dressing keep-out exactly, with no margin, so a road
still runs through a gate. A keep-out **stops** a prop rather than routing one, so a stroke that would have
crossed the marked shape wants redrawing too.

### A standing stone is terrain, and `keepClear` is what makes the pass see it

An authored shape is ground as far as the dressing pass is concerned: **without `keepClear` a prop does not
stand beside the shape, it stands on top of it**, and nothing reports that. **An authored shape needs a field
for each pass it crosses** — `keepClear` for the props, and the same shape named by a stroke's own exclusions
for the paving.


### A prop is judged at every image of its orbit

A rock beside a building on an on-axis group is a rock inside that building's own rot_180 twin, and the pass
declines the whole prop rather than the image — so a site filter that tests only the authored cell is testing
half the map. Measured: three of one build's four declines were images rather than originals. Test `(x, z)`
and its orbit image against everything.

### The authored ring is not the coast

A Bézier edge bulges *outside* the vertex polygon on a convex stretch and *inside* it on a concave one, so
testing a footprint against the raw vertices rejects good sites and passes bad ones. One house corner sat 1.5
blocks inside the drawn polygon and 1 block past the built shore, and `DR-SITE` was the first thing to say so.

Flatten every ring at the rasterizer's own 16 samples per edge before testing anything against it.

### A decline and a complaint are two answers, and only one takes the prop out of the world

Both arrive in the dressing read's `declines` array on a 200, and the `severity` field is the whole
difference. A **decline** means the prop was never written; a **complaint** means it stands, minus what was
cut off it. Measured on one board of 124 props: 18 declines and 4 complaints among 22 entries.

**`DR-CUT` is the complaint that matters for a body.** *"seats clear of what it then reaches into: 70 of its
299 blocks are inside something already standing and were not written, and that cut 51 more off its own
footing, which stand in the air. 229 block(s) are in the world."* A prop seats on its **feet** and is then
written wherever it meets air, so standing clear of something is not the same as fitting beside it.

The count falls with separation and goes silent: measured on pairs of one 299-block tree, 70 blocks lost at
2 apart, 17 at 8, and nothing at 16.

### A copied tree is a recipe with a body, and the body is the whole of it

A `copied` style carries the blocks that were cut out of a world, so its footprint, its foot and its crown are
whatever was cut rather than whatever was asked for. **A body's foot is every cell of its lowest course**, and
that is what a standoff is measured from — a nine-cell foot owes three blocks from each of its nine.
**A hand-built crown is not a disc, not symmetric, and not even solid**, so what decides a spacing is
occupancy rather than distance. `techniques/trees-and-boulders` has both bodies measured against a template.


### A prop is tested at its lowest course and claims everything it covers, and every distance follows

The pass seats a prop by its **lowest course** and then claims every cell the whole prop covers, which is what
makes a crown a keep-out and a trunk a seat. **So what two trees need between them is one crown and not two**,
and **a boulder's standoff is measured from its body**, so its centre owes the standoff plus its own reach.
`techniques/trees-and-boulders` is the worked card, one ladder per rule.


### DR-CLAIM between props is footprint overlap, not a standoff

Two props contest only where their claimed cells overlap: there is no margin between them beyond their own
footprints. **The pass runs by kind** — water, strokes, houses, boulders, trees, flora — and the document's
order is the order only within a kind, so a rock written after an oak is still placed before it.


### A path's band follows the spline, not your polyline

A polyline's points are run through a centripetal Catmull-Rom spline at eight samples a segment before the
band is offset, so four clicked points become a twenty-five-point centreline and the band is wider of the
corners than the points suggest. **A building may end a road and never stand across one** (`DR-CROSS`).
`techniques/polylines` is the worked card.


---

### DR-ROAD measures to the cells a stroke claims, and a wide brush is still a road

The standoff is measured to the **paved cells**, not to the centreline, so a wide brush is a keep-out as wide
as itself plus the kind's standoff — three for a tree, two for a boulder. **A `solid` band has a constant edge
and a `rough` one does not**, so a rough brush's keep-out is a range rather than a number.
`techniques/trees-and-boulders` prices both against a measured ladder.


### `DR-STEEP` is a rock's rule and nobody else's, and it complains rather than refusing

Only a boulder is asked about the grade it stands on, and the answer is a **complaint**: the rock is in the
world, leaning. **The angle it compares against is the theme's own cliff band, not a constant**, so the same
face complains under one paint and not under another.


### Only `worn` spends `coverage` — `rough` fills its band solid

`coverage` is read by `worn` alone: `rough` fills its band solid and wanders the band's edge instead. **A
stroke prop takes five styles and a polyline shape takes three**, and `stones` spaces discs along arc length,
which is the stepping-stone crossing nothing else draws. **A seam wants two tongues with their bands left
whole**, and the mixing belongs in the pave rather than in the brush.
`techniques/painting-with-a-stroke` is the worked card.


### A pave is a full terrain material, but a stroke answers only one of its four axes

A `pave` takes any terrain material, but a stroke hands it only the **surface** axis, so a path cannot be
banded across its own width by its material — that takes two strokes, one inside the other.


### A stroke is turned away by `keepClear`, and by a stamped block, and by nothing else

A stroke repaints the top course of every column it crosses, and the only things that stop it are a shape
stating `keepClear` and a block a stamp has already placed. **A bridge needs no marking, because it is not on
the layer the stroke names** — a stroke ignores `layer` and reads the surface top, so a deck over a gorge is
out of its way by construction. **A deck lands on its banks only if the marks that cut the gorge share their
boundary coordinate.** `techniques/painting-with-a-stroke` is the worked card.


---

## The export

Two gates are heard for the first time at the export, after the whole world is built, and nothing earlier predicts them.

`techniques/objectives-and-clearances` is the worked card: one island with a monument, a core and a wool on
it, and the same board exported again with one fault in it at a time.

### `float` is geometry and `leak` is an attribute, and a goal at float 0 is not a goal

**A goal's base is the standing level plus its `float`**, so the float is what lifts a monument off the ground
and `leak` is a word about what happens when it is broken. A goal at `float` 0 is not a goal: a core on the
ground cannot leak and a destroyable on the ground is trivially covered.
`techniques/objectives-and-clearances` is the worked card — what `float` builds, where `leak` lives, and the
two gates heard only at the export.


### `OB17` refuses at 409 and `OB19` warns at 200

**`OB17` names which of its three places the goal hit** — over the void, inside a spawn's protection, inside a
wool room — and refuses the whole export at 409. **`OB19` is a warning at 200** about clearance, so a board
carrying one exports. Nothing earlier sees either: the board stores clean and compiles clean.


### A placement carrying `"stamp": null` voids the whole intent PUT

The call answers **200** with an empty body and stores nothing — not the placement, not the teams, not
`maxPlayers`. Omit the field rather than stating it null. It is the only call in the studio that reports
success for having done nothing.

### `OB19`'s keep-out is bigger than it sounds, and it is the first thing a prop hits

A **10-block square about the goal's anchor** — 441 cells reaching Chebyshev 10 — tested against a prop's
footprint **plus its eaves**, and against **every orbit image** of it. It is the first thing a prop near a
monument hits, and `techniques/objectives-and-clearances` has the ladder that finds its edge.


### A compile cannot see a layout `subtract`

A goal the plan gate passed can be refused at export. A destroyable placed on the centre of a plan piece, with
a sally port then cut through that piece in the layout, compiles at 200 and exports
`OB17 — is 1×1 and overhangs the void`. The plan gate judges rectangles; the export gate judges the ground the
rasterizer built.

**Cut the holes first, then place the goal.**

### A goal's `at` is in blocks, and naming no piece is not what loses its ratio

`DestroyablePlacement.at` and `CorePlacement.at` are described as *"an [x, z] offset in half-blocks"*. They are
read as **blocks** — from the piece's minimum corner where one is named, and from the symmetry centre where
none is. Measured against `/plan/inspect`'s `goalDistances`: a goal stating `piece: "fell"` with
`at: [38, 42]` and the same goal stating no piece with `at: [-22, -62]` both read 49 blocks from their own
spawn, 159 from the enemy's and a ratio of **3.24**. The same goal at `at: [-44, -124]` — the half-block
reading, twice as far out — answers `null` to all three, because that position is off the board.

The two readings are a factor of two apart and both answer 200, so the tell is the ratio rather than a
finding.

**A goal with no piece keeps its ratio perfectly well** — the `null`s in the third row are that position being
off the board, not the missing piece — so a `null` ratio is a coordinate to check and never a reason to add a
`piece`.

### The export does not object to a goal underground

`OB17` asks whether a goal stands over void, in a spawn or in a wool room, and its `IsLand` is the
set of `(x, z)` the rasterizer produced across **every** layer, so a column under a slab is land.
`EX1` reads the same spans and a cell on two layers answers twice, so an undercroft is a place the
walk can stand in. A monument sealed under a concourse exports at 200 as long as something walks to
it. Where that way in is a ramp without headroom, `SK11` names the places nothing can reach — 3,336 of
them on one measured board.

### An erected shape raises the build cap twenty blocks above itself

The ceiling is `BuildCeiling.Of(highestGround)` — the tallest **terrain** column plus 20 — and an erected
shape is a terrain column. Five hoodoos topping at y43 over ground topping at y14 wrote
`<maxbuildheight>64</maxbuildheight>`: twenty-one blocks of clear air over the picket they were meant to be
un-bridgeable above.

**Erected terrain cannot be used as an unbridgeable wall.** It is an obstacle nobody climbs; it is not one
nobody bridges. The same arithmetic means one tall shape hands the whole board a ceiling it did not want.

### A board whose ground crosses the origin gets a bedrock observer platform in its middle

The compiled intent puts the observer at `(0, observerY, 0)` and `observerY` defaults to `surface + 15` — a
bedrock pad over the centre of the board. `globals.observerY` is the only control a plan has over it; 55–60
keeps it out of the way.

---

## Reading it back

Every read but one is a projection. Which one to reach for is decided by what the question is about, and the picture is never the answer to a question about a number.

**Sixteen routes answer under `GET /api/map/{slug}/…`.** Seven draw pictures — `render/topdown`,
`render/section`, `render/heightmap`, `render/surface`, `render/traversability`, `render/structures`,
`render/mirror` and `render/walk`. The rest answer numbers: `column` at a coordinate, `transect` along a
line, `slopes` over the board as steps, `incline` over it as **angles**, `walk` and `reach` for what a
journey costs, `stroke` for a band, and `themes/census` for what the board is made of.

The schema names each route's own query words, and every summary says what it draws and where it is known to
mislead, so what follows is only what a summary cannot hold.

### `column` is the only honest answer

Every other read is a projection. Probe the coordinate you already expect something at — the `pgm-board`
skill's lookup table is the rest of this subject.


### `walk` is the read that says what ground costs

`traversability` answers whether a board joins up; `walk` answers what crossing it charges between two stated
cells — whether it can be reached, how far in blocks, how many blocks a player must **place**, and what it
falls. **A step it calls `barrier` is a step, not a verdict**: a four-course bedrock wall is bridged rather
than walked, and the read has no word for that (`pgm-studio`'s `WS69`). The `pgm-board` skill's table says
which read answers which question.


### Only two reads keep Y, and one of them is the section

`topdown`, `heightmap`, `surface`, `traversability`, `coverage` and `relief/read`'s walk all project
to one height per column, so a hall under a deck exists in none of them. The isometric preview stacks
layers, and `render/section` cuts a plane:

    GET /map/{slug}/render/section?axis=x&at=<z>&from=<x0>&to=<x1>&ymin=&ymax=

**`axis` names the direction the cut runs, so `at` is the other coordinate** — `axis=x` takes a z,
`axis=z` takes an x, and an `at` outside the world is refused with the range it could have taken.

### A section's horizontal lines are the renderer's, and its vertical divisions are the world's

The picture blends a Y scale over itself — a pale line every few blocks of height and a brighter one every
fifth. There are **no vertical gridlines at all**, so every vertical division in a section is a real block.
The two backgrounds are two different answers: pale is air inside a loaded chunk, near-black is no chunk at
all.

**It samples one plane unless `depth` says otherwise**, so a cut through a house that misses its walls reads
floor, air, roof — a correct reading of that plane rather than a broken building. `depth` projects that many
blocks behind the cut, each column taking the nearest block there, drawn dimmed by how far back it stands.

An `at` outside the world is refused, and the refusal names the range a cut can be taken at.

### The material top-down draws the top *solid* block, so water reads as its own bed

`render/topdown?material=1` over a lake shows sand, not water; the category read
(`render/topdown`, no `material`) has a `WATER` class and draws it cyan, and
`…/column?at=0,22` answers `y5 Water · y4 Water · y3 Water · y2 Sand`. When two pictures disagree,
`column` is the one that is not a projection.

### `render/topdown?layer=` names a sketch layer, so the category isolations are gone

On a board whose `layers[]` are named, `?layer=structure`, `?layer=foliage` and `?layer=objectives`
answer **422 `RQ4`**: *"this board has no layer 'structure' — it carries ground, under, catwalk,
roofs, deck"*. One query word does two jobs and the sketch layer wins. The per-storey read is the
better half of the trade — `?layer=under` draws the undercroft and nothing over it — but the three
reads that answer *did the props land where I put them* are unavailable on any stacked board.

### A storey read only reaches its own top where the spans are read half-open

`ColumnSegment` is `[YFloor, YTop)`. A board whose lower layer meets the one over it with no gap —
rock at `under[1..18]` under `ground[18..28]`, which is what stating the rock under a landmass looks
like — is the case a closed reading gets wrong: nothing is found above, the storey is handed the rest
of the world, and `?layer=under` draws the surface under the undercroft's name. A layer with air over
it reads correctly either way, so the half-open reading is what makes a storey read answer for the
board's lower layers at all.

The provenance record travels with it: a claim is recorded per column and carries no course, so under
a storey read it describes the column's top rather than the course being drawn. It is narrowed with
the world now — terrain at or below the layer's own top, the recorded claim only where the storey
shows the column's own top — and the picture's legend says which reading it used.

### The provenance sidecar records an intent to claim, not the blocks

A structure read says which reading it used — `STRUCTURE READING: RECORDED PROVENANCE` where the sidecar is
there, and the material estimate where it is not. Its owners list is a literal census of the dressing, and a prop
that landed nothing has no row at all:

```python
import json; from collections import Counter
p = json.load(open('specs/<slug>/provenance.json'))
print(Counter(o['kind'] for o in p['owners']))
```

The export writes it into the world's own `region/`; the driver moves it beside the documents, because
`maps/<slug>/` is what a game server is handed. A CLI read-back pointed at that region directory finds no
record and falls back to the material estimate, stating which reading it used on its scale line.

A claim is the walk that stamped it, so a structure is recorded at exactly the cells it fills. A wall read
from a render is the width it plays, which is what decides whether it can be built over.

---

## What an answer says

A 200 is not a promise that everything posted survived, and two documents are stored as snapshots no finding reaches inside.

### A field the intent does not carry is a 200 with an `RQ3` beside it

`PUT /map/{slug}/intent` stores what it reads and reports what it did not as `RQ3`, naming the JSON path — so
a key the record has no field for costs nothing, changes nothing, and answers 200. A board posted that way
**stores, pre-flights OPEN and exports a world missing whatever the key was for**, and the `RQ3` line is the
only report of it. Read the `RQ3`s on every intent write; they are the difference between a field that landed
and a field that was spelled at a version of the studio that no longer exists.

### A material's `kind` is written first, though it no longer has to be

The reader takes `kind` wherever it sits, so a style round-tripped through a formatter, a re-serializer or
`json.dumps(…, sort_keys=True)` still previews.

Write materials `kind` first anyway. It is what every committed theme and style here states, and a build
older than this one reads the discriminator positionally — where it does, moving the key and nothing else
turns a document that answers 200 into a **400 naming a kind that is right there**.

### Two words differ between a save request and a snapshot

`porch.edge: "front"` is a save-request word. On a **snapshot** — `preview-snapshot`, `roomStyles`, a dressing
`style` — the field is a nullable enum and the word for "the door wall" is **`null`**; `"front"` refuses with
`RQ1`. Same document, two layers, two vocabularies.

---
