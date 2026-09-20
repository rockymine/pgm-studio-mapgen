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

---

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

### A core is the forward objective and a wool is the deep one

A core cannot be carried anywhere; it is breached where it stands, so it belongs where it will be
fought over. A wool has to be fetched and brought home, so it belongs behind. Drafted the other way round,
`WL10` reads a wool-front-distance of 8.

Two things about a core in particular: `float` and `leak` are one knob (the lava free-falls to the
terrain at `float` below the casing and leaks a course below `leak`), and **a core on a group in
open sky has nothing to catch its lava** — so the casing wants ground all round it, or a breach
anywhere near an edge ends it at once.

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

The instrument for cutting a hole *through* ground is a layout `subtract`, which is downstream. Shape the
**pieces** to shape a coast, and cut the holes in the layout.

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

On a 20 x 20 piece whose shell is the piece inset one and five in front of the door, that ring is the
five-block door apron and nothing else: the cube fills it, three blocks of cube and two of air, and anywhere
in the hall is unplaceable.

Shrinking the building widens the ring, which is what makes a seat beside the door possible at all — and
`/plan/room` hands it over rather than being guessed at.

### A `walls` entry closes an interface, not a route

A plan wall stamps bedrock two thick and three tall across the interface it names, over that
interface's full width, on the attack side — so it closes exactly one seam. On a plan whose pieces
enclose something, that is not the same as closing the way through: a `donut` wool box has a lane
down **each** side of its hole, and a wall on one is walked past on the other.

Count the ways round the thing before counting the walls. Where the plan has no seam at the place a
wall is needed, **split a piece to make one**: cutting a ring's two long arms in two level with the middle
of its hole takes twelve pieces to fourteen, which puts one interface in each lane facing the other across
the yard and gives both walls somewhere to stand.

### On a bridging board the gaps are the design, so state them first

Six-block gaps between groups answer `G2` (a corridor under ten wide), `G5` (a hop outside 10–20)
and `CT12` (a strait outside 15–40) on every pair, and they are right: a six-block gap is a running
jump. Fix the four numbers — the hops and the strait — and fit the groups round them.

---

## A board somebody else arranged

What the composer answers, what it does not, and what taking one of its boards over costs.

### A composed board's own proportions, counted

`GET /api/compose?players=24&symmetry=rot_180&wools=i`, pinned through `POST /compose/pin`, answers a
`PlanModel` whose team unit is **142 proxy cells** — hub 66, frontline 30 + 14, spawn 6 and its room 6, two
wools 10 each — on a **22 × 36** bbox. Both halves and the mid together come to about **0.36** fill,
comfortably inside the `fill-ratio` band of [0.201, 0.542] the term reports under `G8`. That term measures a
**wool** board and answers `null` for any other kind, so the number is not a judgement about a destroy
board's density and never will be.

The shape that gets there is not symmetry about the centre line. The unit spans `x −11..3` of a board running
`−11..11`: it is **offset**, its own `rot_180` image takes the other side, and the two interlock so that each
row is about half land. A unit authored symmetric about `x = 0` fills its own bounding rectangle and is
refused at **0.774**, with `FR6` on the 24-cell frontline that shape produces and `LN2` on its chain. All
three name symptoms; the cause is the arrangement.

---

### Browsing the composer is a four-call loop, and a scan is what tells you its vocabulary

`GET /compose?players=&symmetry=&seedStart=&count=` returns cards carrying the descriptor that
reproduces each board, its score, a structural read and a board SVG; `POST /compose/pin` stores one
from that descriptor; `GET /plans/{id}/png` renders it as an image; `POST /plan/{id}/author` makes a
map row. Ninety-six seeds, eleven pins and two contact sheets is a few minutes.

Two things a scan says that nothing else does. **The cell is a drawing scale, and the composer draws on four
blocks** — every width it builds to is stated in blocks and divided by the cell, so cells 3 through 6 all
compose and only cell 3 at nano comes back `exhausted`.

And **10 and 12 players give identical boards**, because the count names a size band rather than a budget of
its own, and both counts are nano.

Hub forms observed in 48 seeds at 16 players: `bar`, `ring`, `single`, `twin`, `g`, `double-hole`, `p`; wool
shapes `i`, `l` and — five times in forty-eight — `donut`, which is five pieces round a hole.

### A composed board is JSON, and taking it over is four edits

`GET /api/compose?players=&symmetry=&seedStart=&count=&hub=&front=&wools=` answers cards carrying a
descriptor and an SVG; `POST /api/compose/pin` stores one and returns its `planJson`. That plan is an
ordinary `PlanModel` and everything after that is editing it:

```python
for piece in plan["pieces"]: piece["rect"][1] += 4      # shift every piece 4 cells (20 blocks) of z
for box   in plan["boxes"]:  box["rect"][1]  += 4       # the boxes travel with their members
plan["pieces"].append({"id": "mid-isle", "role": "piece",
                       "rect": [-4, -3, 8, 6], "mirrors": False})
```

The vocabulary the filter takes: hubs `ring|bar|double-hole|twin|P|G|single`, frontlines
`twin|single|bar|none`, wools `i|l|donut|u|h|clamp`.

**There is no `u` frontline** — `u` is a wool family, and the frontline that reads as a U opening forward is
`twin`, a bar with two prongs off it.

### The composer's holes are made by arrangement, and nothing marks them

A double-hole hub's two slots and a U wool's notch are the *shape of the pieces*, not a region. An
add-shape dropped on one fills it in, no gate says a word, and the layout that was filtered for is
gone. The predicate to check a ring against, before using it:

```python
def is_hole(x, z, reach=16):
    """A void cell with land in all four directions within reach. Open sea is void with nothing
    beyond it, and a shape may hang over that; a hole is not."""
    if land(x, z) is not None: return False
    return all(any(land(x + dx*k, z + dz*k) is not None for k in range(1, reach))
               for dx, dz in ((1,0),(-1,0),(0,1),(0,-1)))
```

### A *flat* composed plan compiles to one merged polygon per component and a subtract per enclosed void

Thirteen pieces go into `POST /plan/compile` and two `add` polygons come out — the team unit's whole
footprint as one outline, and the neutral mid as another, because the two never touch — plus one `subtract`
per **enclosed** void. A void the outline can trace around needs no cut: on one micro board the predicate
named a twelve-cell region the compiler emitted nothing for, and the built world had it void anyway.

Every piece inside that one outline is unaddressable: there is no shape to hang a theme, a relief or a
`shapePropsById` on until the merge is over.

**A hole is never scenery, and nothing but this sentence defends one.** What the composer encircles — the
middle of a `donut` wool room, the yard of a `clamp` or a ring — is ground players go round, and the walls a
board hangs on it are drawn to guard exactly that ground. Filling it makes them guard nothing (the author's
ruling).

**Both ways of filling one store at 200, and `SK13` only changes its wording.** A plain add over a cut
*"draws nothing over 144 column(s) … because 'void-1-cut' takes them away … The shape is on the canvas and
not in the world"*; the same rectangle with `override: true` *"fills 144 column(s) that 'void-1-cut' takes
away … so the negative space the board states there is ground in the world"*. Neither is refused.

**Where the void wants to change shape, change the subtract.** A compiled subtract is the board's
statement of its own negative space: it may be redrawn — rounded off, narrowed, moved — but never
deleted and never papered over with an add. Measured: four blocks off each corner of one 12 × 12 ring gave
the board 32 further cells of ground and no add was written.

**Stating a surface per piece does not remove the hole.** It stops the compiler merging the pieces
into one polygon, which is what makes a composed board paintable — but `PlanVoids` reads the void per
**component** rather than per surface, so the buffer is declared and the subtract emitted either way.
Measured on a thirteen-piece board: both cuts survive, and both holes are 0 of 144 blocks in the world.

**What the surfaces answer is one polygon per height per connected region, not one per height.** Thirteen
pieces at six heights came out as **eleven** polygons — `hub-t1-9`, `hub-t1-9-2`, `hub-t1-10`,
`hub-t1-10-2` — the suffix marking where one height fuses into several, and `themeById` is what addresses
them singly.

That is also the only way a composed board can be painted in more than one theme: a theme is stated **on a
shape**, a flat plan has one shape, and `themeByHeight` therefore has nothing to bind to until the heights
exist. Heights first, then paint.

**And painting by height paints one component in as many themes as it has heights, which `SK27` remarks
on.** *"component 'hub-t1' … compiles to 11 plateaus from surface 9 to 16 and they state 4 different paints
… one landform with a hard line at every riser, where a theme is a place."* A complaint, not a fault: a
terraced hub really is eleven plateaus, and the hard line at each riser is the author's to want.
`techniques/taking-over-a-composed-board` is the worked card, one pinned board edited four ways.

**A height per piece is also how a plan states a staircase, because one piece is one height.** A climb a
player walks is a run of pieces and nothing else: a cross-piece three cells deep, cut at every cell and
stepped 10, 11, 12 between a bar at 9 and a bar at 13, gives four one-block risers that `walk` crosses end
to end with nothing placed. Unsplit, the same climb is one four-block face.

### A contested middle wants a structure, and a structure is one made layer per span

The neutral holm both teams bridge to is the piece most worth building on, and a flat island is nothing to
arrive at. What it wants is a **double deck**: four legs at the corners, a floor with three blocks clear
under it and a roof with four clear between, so the same piece is a height to hold and a room to hide in
(the author's ruling).

**A leg passing a floor is two spans in one column, which one layer cannot hold.** A sketch layer is one
`[floor, floor + base_height)` per column, so the legs are cut at each floor instead — under the lower one,
then between the two — and every span gets its own layer marked `kind: "made"`. Four layers and ten
rectangles built the one measured here.

**Make the footprint odd in both axes about the centre, and it is its own image.** A deck spanning columns
−8..8 by −4..4 maps onto itself under `rot_180` and needs no mirror; an even span is one block off-centre,
which on a rotational board is one team's middle.

**A field with `rise: 0` on a fill is refused by `PT4`.** A plane-sampled pattern resolves every block of a
column alike, so a leg of it comes out in vertical stripes. Two courses of vertical period is enough for
anything a deck is made of.

### A piece taken out for a build zone is the cheapest edit that changes how a board is fought over

A plan's `zones` is what it says about the void, and the compiler turns an entry there into the intent's own
`build.areas`, fanned with everything else. So replacing a piece is two edits: drop it from `pieces`, and
add a zone over the rect it had.

**And it changes which voids are holes, without changing the ground.** A void bounded by the piece that
came out is no longer *enclosed*, so the compiler emits one cut fewer and the merged outline states that
void by tracing round it instead. Measured on a double-hole hub with its far bar removed: two subtracts
became one, and 0 of that hole's 144 blocks came out as ground.

**Ask a hole whether it is ground with `transect`, not with a render payload.** `ground` is null on a void
column, which is the question being asked; a payload of blocks answers a different one, because a crown
leaning over the rim and a marker block under it are both blocks in that column. Counting those reported
a hole 13/144 filled that is void to the block.

**Why to do it at all is a gameplay decision and belongs to the author.** On a `rot_180` board with one
wool a team, both sides spawn, turn the same way and run past each other down whichever lane is furthest
from their own spawn; taking that lane out and declaring it buildable means an attacker takes the near lane
or bridges a gap under fire, and the two teams meet instead of trading (the author's ruling).

### A composed board is corridors, so compute where a prop may stand

Every piece is ten blocks wide with a road down the middle, and there is no landscape around them —
what is not a piece is void. Placing props by eye on one gave fourteen declines, half of them
`DR-SITE — has no ground`. Given the piece rectangles, the roads with their radii, the buildings and
the doorways and the wall seams, a search over every block of the authored half is instant and
returns the truth: on
one composed board it is **nine** places in a half.

Two of the rules that search has to know. **A road's standoff is measured to its paved cells, not its
centreline** — clear the stroke's radius *plus* the kind's standoff, three for a tree and two for a boulder.

And **an approach wall's interface is kept clear the way a doorway is**, so the seam a `walls` entry names
belongs in the keep-out list beside the rooms.

**The search is only as good as what it searched against, and two things are easy to leave out.** The rooms,
the doors and the spawns are not in the claims map until the compiled **intent is stored**: run before that,
one board's search answered 1,398 cells and 52 sites, and four of the first twenty were then declined
`DR-KEEP`. Run with the intent but without testing each cell's **orbit image** it answered 1,274 and 45 —
no decline on that board, and still not optional, since the orbit is what the last 212 cells cost.

**Ask the search about a board with no props on it.** A tree raises its own column's top and claims every
cell its crown covers, so a layout that already carries one is a different board to search: the same board
answered 1,062 cells with the props stripped out and 748 with seven of them standing. Strip every prop but
the strokes, search, then place.

**What the search answers is where a prop MAY stand, and how many stand there is the author's** (his
ruling). Planting every site a legal field offers is a forest, and a board of ten-block corridors has no
room for one: 34 spaced sites on that board came down to **ten** planted. The rules the ten follow are
worth more than the list.

**Toward the OUTSIDE of a piece, never down its middle.** With no road on it a player still runs down the
centre of a corridor, so a line of trees along the rim reads as an alley and the same trees in the middle
read as an obstacle course. Two in front of each hole, on the rim between the ground and the void.

**Nothing where a build zone is ARRIVED at, and nothing on the brink it is bridged from.** A player who
crosses a lane and lands in three trees has been given an obstacle the arrangement never asked for; a tree
two blocks off a bridging edge crowds the edge itself. Both belong on the far side of the piece.

**Nothing on the approach in front of a wall, and nothing on a contested middle.** The first the studio
enforces on its own — a wall's keep-out plus a road left **0** legal cells on a whole wool approach — and
the second is a place for a structure rather than for scenery. One tree in the corner behind the wall, in
front of the room, is what that approach carries.

**A search is narrower than the studio, so a site is checked against the DRESSING PASS.** A filter that
keeps only cells with eight level neighbours refuses every **rim** cell on a board, because beyond a rim is
void and a neighbour that is not ground fails the test. What the studio asks is ground under the trunk,
three clear of the paving, unclaimed and not kept clear.

**The rim passes all four, and a road often leaves nothing else.** On a bar twelve deep with a five-wide
road down it, three clear of the paving is the rim or nowhere — so the search's silence there is
conservatism and not a refusal. Probe the stretch a candidate at a time and read the rule each one hits.

**A prop on a rim hangs a crown over the void, and the walk stands on it.** A leaf course over a void column
is a standing place for `walk` while `column` and `transect` both call that column void, so a route will
climb through a canopy and report a `barrier +8` that no player meets. Which read is wrong is
`pgm-studio`'s `WS71`, parked on the question; keeping trees off the rims beside a void is the authoring
answer either way.

**A `walls` entry stamps a barrier with no gate, and that barrier is the feature.** Four courses of
bedrock over the ground either side, two columns deep, along the whole interval the two pieces share: a
defender builds on it and cannot lose it, and four courses is what an attacker bridges. It goes on the
approach and not in the hub — on the seam between the two approach pieces, or on the outer one where the
approach meets the board (`PlanValidator` refuses the wool room's own interface).

**`walk` calls it `barrier +4`, and that is the read being literal about walking.** A walk prices a walk
and has no word for a wall that is bridged rather than walked, so the number reads as a fault on a thing
the map states deliberately — the author's account of why so few maps have ever carried one of these walls.
Filed against the studio as `WS69` and `WS70`; the route past it is reached, with the blocks placed
counted.

**Never chamfer a corner a build zone or the front line attaches to.** Taking a compiled outline's corner
back is an ordinary layout edit, but a diagonal on an edge somebody bridges from leaves them a triangle of
ground nobody can build on. Take the corner off the outer coast, away from the fighting, where a coast is
only a coast.

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

A relief mark is a **constraint**: the ground here *is* this height, honoured exactly, with no falloff of any
kind. That reads as a modelling detail and it decides what terrain can be authored at all. *A point mark's
radius pins a flat disc* above is the same fact met from the other end, and the two remedies are for two
jobs: a small radius left to `reach` is how a mark stops terracing ground it is only meant to sit on, and a
push is the only thing that builds a landform.

A `point` mark at `h 47, r 8` therefore does not build a summit. It builds a **drum** — a flat disc eight
blocks across standing on a twenty-block sheer wall — because nothing between the disc and the ground round it
is under any statement except the relaxation, and the relaxation has one cell of room to make the transition
in.

A `line` mark with per-vertex heights is the same object stretched along an arc: a ridge-shaped wall with a
flat top.

Both produce correct relief numbers — `low 11 · high 55`, `symErr 0`, gate OPEN — over a landform that
reads as a row of oil drums.

A **push** is the other operation. It takes a drawn ring and lifts the solved surface inside it, and three of
its fields are the landform:

- **`amounts`** — one lift per position round the ring, in place of the single `amount`. The positions are
  spaced by **arc**: index `i` is read at fraction `i / count` of the perimeter, which coincides with the
  drawn vertices only where every side is the same length.
- **`crown`** — how much higher the middle stands than the edge, where the middle is the ring's **medial
  axis**: a point for a round ring (a dome), a line for a long one (a crest). **The record's default is `0`**,
  so a push authored without touching it is a plateau. This one field is the difference between a mountain and
  a mesa.
- **`falloff`** — the skirt, measured from the ring across the land. This is the number that decides how much
  of the board the range eats. On a 90-block-wide board, `falloff: 20` put the two massifs' skirts into each
  other and left a 20-block ditch down the middle; `falloff: 11` left flat ground from `x −18` to `x +15`.

`roughness` wobbles the skirt against a noise field so it is not a clean offset of the outline, and a
**negative crown** dishes the ring rather than doming it — a corrie, a quarry floor, a pond basin.

`techniques/pushes` is the worked card: four outlines of one push side by side, four arrangements of several,
and the two grades read back per push. `techniques/marks-and-pushes` is the same instrument once there is a
board under it.

**The second half is what is *not* written.** Pinning a region with an `area` mark because it should be about
that height leaves the solver nothing to solve, and a board with a mark on every region is a table with bumps
on it however tall the bumps are. A range that reads pins four things — the coast, the dale floor, the
goal's shelf and the spawn's apron, every one of them ground a player walks — and the flanks carry no mark
at all. A board that pins all four of its regions is flat for exactly that reason.

`reach: 0` goes with it: a finite reach pulls ground back toward `base` at that distance from any constraint,
which between two distant marks means the flanks decay to the base and the range becomes separate hills.

One last shape note, cheap to fix and expensive to see: an `area` mark's ring is a **shape**, and a rectangle
looks like one. `shelf` and `apron` written as four-vertex rectangles built two mesas with sheer sides,
visible in the heightmap as literal squares; the same marks on nine- and eleven-vertex lobed rings are
indistinguishable from ground.

### Three ordering facts about a relief, and each one hides a landform

**A push is applied to the solved surface, so a push over a hollow fills the hollow in.** A push and
an `area` mark are not two statements about the same field: the marks are solved first and the pushes
are added to the answer. A twenty-radius push laid across a bench meant to be five blocks down lifted
it six, and a `sink` cut from that ground came out shallow with nothing complaining.

**A later mark wins a contested cell, so a mark written over a bench replaces it.** That is the
mechanism the stacked-hollow idiom depends on — nested `area` rings written outward-in — and it is
the same mechanism that silently overrode a bench with a knoll written after it and left a
**21-block** face into a pit that no one authored.

**And a push over a pan lowers the pan.** A `slack` push reaching a sough's tail lowered the ground the
south flight was anchored to arrive on, and the flight came out landing **two blocks proud** of it — visible
in `…/walk` and in nothing else, because the flight is correct and the ground is correct and only the join is
wrong.

The rule under all three is one line: **a push is added to the solved surface and marks negotiate with each
other.** Where a landform has to agree with something already stated — a pan, a pad, the head of a flight —
state it as a mark.

**A push carries the ground rather than replacing it, so a landform wanting a flat top needs flat ground
under it.** A hillside reading 15 → 10 → 14 under a push's ring, lifted 12 with `crown` 0, came out as a
summit reading **27 → 22 → 26** — the same shape plus twelve, block for block, with a hollow on its top. The
group read `rolling`, one push, a sane skirt and no finding, and its `relief` came out *lower* than the bare
hillside's because filling a hollow's neighbourhood shortened the range.

**A push cannot be kept off a mark: only its ring and its `falloff` can.** With the same push moved
twenty-four cells clear of a holm pinned at 10, the holm read **22**, **12** and its stated **10** across
eight cells. Ring plus falloff is the push's whole extent, and every cell inside that circle is lifted
whatever states it.

**How much of a board to pin is one dial, and `level` is the reading.** Pinning every region built three
plates at `level` **0.51**; pinning only the ground a player stands on built flowing terrain at **0.30**,
which is exactly where `RL5` begins — *graded everywhere and left nowhere to stand*. `relief` cannot tell a
range from a staircase and called the staircase the bigger landform, 32 against 21.

**`reach: 0` is what a board wants, and a finite reach is an instrument for isolating something.** The same
document at `reach: 16` sagged its unpinned north half from 25…20 to 11…13 — within a few blocks of its
`base` — and a shelf pinned at 30 stopped reaching a line twenty-two cells away from it. Built, a shelf and a
fell that had been one flowing landform came apart into two mounds on low ground.

**A field pinned only in patches relaxes into fans radiating from each patch; a field pinned along two
opposite edges relaxes into the ramp between them.** The fans paint as a spray of contour streaks over ground
that is otherwise flat, which is what an island carrying three small scattered `area` marks and nothing else
looks like. Two long marks facing each other are what a hillside is made of.

**A `bevel` wider than half a mark's narrow dimension pins nothing, and `relief/read` calls it silent.** A
bevel is paid for out of the mark's own floor from every side at once, so a nine-cell band at `bevel` 5 has
no floor left and the group comes out at whatever else is speaking — measured, a panel carrying that band
and one other pad reads `relief` 0 and `silentMarks: ["crest"]`.

**A push's skirt is gentler than its stated grade at the ends and half again steeper in the middle.** The
smoothstep a `falloff` eases with peaks at 1.5× the average, so a skirt the read calls 0.55 reaches 39° and
one it calls 1.33 reaches 63°. That is the difference between a landform the slope bands paint as scree and
one they paint as crag.

### Pushes add to each other, so a massif is several of them

**Every push in a group is summed into one lift field**, which makes a smaller ring inside a larger one a
terrace on it rather than a replacement for it. Three concentric rings at `+10`, `+8` and `+6` on a plain at
8 build terraces at 18, 26 and 36 — each the running total, each with its own skirt down to the one below.
One ring with a large crown is a single cone whose only shape is its outline.

**Two rings that cross give the sum in the crossing, not the larger of the two.** Two radius-16 rings twenty
apart at `amount` 14 each read 22 under either alone and **36** where both contain the cell.

**The skirts add as well, and that is where the unauthored steep ground comes from.** On that same pair the
relief read counts 112 barrier steps, and the cells sit north and south of the waist between the two rings —
x −62…−49 at z 22…28 and again at z 60…67 — not one of them inside either ring. Two grades of 1.17 meeting
there make 2.34.

**A negative push inside a positive one cuts the hill after it is raised, and the order they are written in
changes nothing.** `+20` over a radius-22 ring and `−14` over a radius-11 ring inside it build a rim at 28
and a floor at 14, six blocks above the plain the cone rose from. A sum has no sequence: what makes the
caldera a hollow is that its ring lies inside the cone's.

### `amounts` is read at the nearest ring point, so it cuts the interior into wedges

**Each interior cell takes the lift of the ring position nearest it**, and that partition is the ring's
medial axis — so a ring of few positions builds that many wedges with a step down every seam between them. A
40×40 square carrying `[26, 26, 6, 6]` builds two wedges at 34 and two at 14 with a **20-block cliff along
both diagonals**, two cells wide, which nothing in the document or the read names.

**Two things remove the seam and a spur wants both.** Enough positions that neighbours differ by little, and
a form long enough that the two sides facing each other across the middle carry the same lift — which means
stating the lifts as a function of position *along* the form rather than of angle round it.

None of the three shows up in the document, in a warning, or in a top-down. Each is one
`GET /map/{slug}/column?at=…` transect across the join. Take one across every place two landforms
share ground, before believing the JSON.

### A pin inside a push's ring applies the push twice

A room, a goal or a held shape standing inside a negative push takes the whole island down with it. The group
is solved once without the room, the floor is read off that solve and the room is pinned at it — and that pin
is then the group's only constraint, so the second field relaxes to a constant at the room's height and the
push subtracts its whole amount from that.

Measured on a pit meant to read rim 32 and floor 20: with a room inside the ring and nothing else pinned, the
rim reads **20** and the floor **8**, with the room standing on a twelve-block plinth in the middle.

**The threshold is one pin, and nothing refuses.** The store answers 200, the export gate opens, and the
relief read calls the group `rolling` with a relief of 12 — true of the numbers and wrong about the board.

**One `area` mark holding the land at the surrounding height fixes it exactly**, and the profile is then
station-for-station identical to the same push with no room in it at all.

### A relief is solved on the group's primary half, and its surface is copied through the mirror

A mark on the far half constrains cells the solve never visits and is overwritten by the image of the near
half. State every mark on the side the plan's pieces are authored on, and pin a footprint that straddles the
axis on both sides.

### A mark pins its own cells and the relaxation slopes everything within `reach`

Two regions at different heights with nothing between them come out as one long ramp, so a floor that must
stay level next to a lower one needs a verge pinned at its own height. Otherwise a wall's footing, and the
gate in it, follow the neighbour down.

### A point mark's radius pins a flat disc, so a radius is a mesa and not a summit

`PointMark.Pins` yields **every** cell inside its radius at the stated height, and those cells are
constraints — the relaxation only shapes what is left between them. Marks placed at radius 16–32 on
a 176-wide board nearly tile it, and the ground builds as stacked plateaus with vertical faces.

Measured off `…/sketch/relief/read`, the same thirty marks at two radii: at 16–32 the board is terraced
throughout, with a cliff at every mark's edge; at 3–6 it is **95.1%** walkable at one-block steps, its
largest place holds 86.5% of that, and six cliffs remain on the whole board.

**The rolling is the relaxation's**; a radius is how much of the landform you are refusing to let it
do. Keep a summit at three to six and let `reach` spread it. An `area` mark is the other instrument
and is right where flat is the point — a lake pan, a spawn terrace, a shelf under a goal.

### A range is a wall unless its two gradients agree

A push has two slopes in it and they are set by different pairs of fields. Outside the ring the ground climbs
over the skirt, at `amount / falloff` courses a block. Inside it the ground climbs from the ring's edge to its
medial axis, at `crown / half` — `half` being the half-width the ribbon was drawn at. Where the two disagree
the landform has a step in it at its own outline, and a range with a large `amount` and a short `falloff` is a
cliff with a hill on top of it whatever its height.

Measured behind a spawn: `amount 26 · falloff 8` against `crown 10 · half 7` is 3.25
courses a block for ten blocks and then 1.4, and the section at `x 0` reads as a sheer face standing directly
on the building's back wall. The same range at `amounts 13–17 · falloff 10` against `crown 12 · half 7` — 1.7
either side — reads as one mountainside from the wall to the board's back edge.

**The height a range can be is decided by the ground in front of it, not by taste.** What is available is the
distance from whatever stands in front to the coast behind, and a peak more than about 1.7 courses a block
above that distance has to buy the difference somewhere, which it does by putting a step at the ring. Behind
Thornfell's spawn there are 20 blocks between the building's back wall and the coast, and 20 blocks at 1.7 is
what makes `high 52` on a board whose ground is 26. Wanting 80 there is wanting a wall.

The other half of the same arithmetic is where the summit goes. Setting the spine **past the coast** puts the
medial axis off the board, so what is on the board is one uninterrupted climb and the crest reads as being
behind the map. That costs the strokes that are placed from the spine — a summit blob centred past the coast
has nothing to clamp to and collapses onto its own centre — so those are taken from a crest point inside the
outline rather than from the spine itself.

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

### A line mark's reach is either side of the line, and its name is `r`

Not a half-width and not a one-sided band. A `line` at z 50 with `r: 12` writes over everything from z 38 to
z 62, so a mark drawn to make a bank behind a frontline erases the frontline — and a push stacked on that
band makes a seven-block wall across the necks of the launch ground. Halve every reach that was reasoned
about as a corridor.

`width` is the same number under an older name, read on the way in and never written back, so a document
saved through the studio comes out spelling `r`.

**`tread` is how much of the band is flat**, in cells either side of the centreline, and the rest is a loft:
a cell out past the tread takes a straight ramp between the two treads' edges instead of snapping to
whichever pass of the line is nearer. That is what turns a serpentine or a spiral haul road from flat road
and vertical wall into flat road and graded batter.

**`batter` states how steeply that shoulder falls**, in degrees from level, and may only be steeper than the
run allows — a gentler angle would not have arrived by the next tread, so it is raised to what the gap needs.
Two passes `pitch` apart falling `drop` between them grade over `pitch − 2·tread`.

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

### Two flat marks butted together build two terraces and a step at the seam

A `line` mark at y8 with radius 7 and another at y14 with radius 6, their bands touching, transected
`7 7 7 7 [+5] 12 13 13`: a five-course wall right round a lake that was meant to shelve. Seven blocks of
unpinned ground between them and the same two marks read `7 7 7 7 9 11 12 13 13`.

**The gap between two marks is not a gap in the design; it is where the design happens.**

**One cell of gap halves the wall and hides it from the read.** A ring covers the cells whose centres fall
inside it, so two bands stated one apart leave exactly one cell pinned by neither, and the relaxation puts
it midway: a 12-block butted step becomes +6 and +6. `seams` then comes back **empty**, because a seam is
measured between a cell one mark last claimed and a neighbour the other did, and there is no longer such a
pair. The ground is still a barrier and nothing says so.

**A group whose marks all state one height comes out at that height everywhere.** A landform is a fall, and
the fall is either a second mark at another height or a finite `reach` — one ring at 30 over a `base` of 8
with `reach` 0 reads `low` 30, `high` 30, `relief` 0.

`techniques/marks-and-seams` is the worked card: one pair of pads meeting four ways, a `scarp` beside three
marks that pinned nothing anybody can see, and four fields from four statements.

### A pad meets its neighbour on a step unless it states how far in to grade

`relief_scope: hold` keeps a shape at its own level and the surrounding surface is solved knowing where it
has to arrive, which is the pre-raise a spawn or a wool room wants. Stated to its own outline it meets
whatever is beside it on a face, so a room pad at 18 beside an approach pad at 14 is a hundred cells of floor
nobody can walk onto, and `relief/read` reports it only as a rise in the place count.

**A held shape's `skirt` is how far inside its ring the height gives way**, read as the bevel of the mark it
becomes: the pins near the edge are soft and the relaxation pulls them toward the neighbour, so the pad keeps
its flat core and arrives on a grade. An `area` mark states the same thing directly as `bevel`.

A floor wants none of it and ground wants all of it. Where two pads must stay flat to their own edges, each
still climbs one block over the pad it is reached from — 16 → 17 → 18.

### `step` is the instrument for a quarry, and the terracing that ruins a hillside

`step` snaps the finished surface to a quantum, which is what turns a board's hills into stacked plateaus. A
worked pit **wants** that: state the rim and the floor as two `area` marks, let the relaxation solve a smooth
bowl between them, and set `step` to the bench height. Four marks and `step 4` give six benches where thirty
marks gave a hillside nobody wanted.

**A mark states its own `step`**, and ground no mark claimed takes the group's — so a worked terrace and a
walkable ramp state different quanta and share one island. A cell takes the step of the last mark to claim
it.

Every stated level must be a multiple of the step or the knob rounds it away. **Nothing repairs what the
terracing strands**: a pit with no way out of it is a pit, and the walk is what says so — `EX1` where the
board is no longer one place, and the steepness tiers short of that.

### Water fills whatever is level, so the pan is the size of the pool

An `area` mark 34 × 30 at the sump's height is a 34 × 30 lake however small the `water` prop inside
it. Draw the mark at the size of the water and let the surrounding floor sit a few courses over it.

### A water prop fills its own band, not the level it finds

`form: "canal"` holds its stated width: a centreline down the middle of a fifteen-wide hole at radius
3 is a six-wide channel with dry ground either side of it, however flat the pan under it. The band
**is** the pond and the radius is the knob. It is the same fact met from the other end, where an oversized
flat `area` mark becomes an oversized lake: a water prop is a stroke
that carves, not a fluid that finds its level.

**`radius` is half the width on a channel and the *shelf* on a pool** — how far in from the shore the bed
reaches full depth — so the same number means two things and which it means is `shape`. **`shore` is the
beach**, in blocks, and 0 is a hard edge where the water meets the grass.

**With no `level` the line is found and with one it is stated, and only a stated line fills dug ground.** A
pool on flat ground at 21 came out at 21 with nothing saying so; a basin cut with a `height_mode: "sink"`
shape has no surface up at the line for a derived one to find, so a dock or a harbour can only be stated. The
author then owns the rim: water rises to the line inside the prop's footprint and nowhere else.

**A water prop's bank is counted against the theme of the ground it carved.** A board of two themes came back
from `themes/census` with eight distinct surface blocks, gravel and sand among them, because the bank is a
material the prop lays rather than a theme the document scopes.

**A sea is a pool whose ring is drawn past the edge of the land, so the water fills to the board's rim.** A
ring kept inside the island stops in a basin with a lip round it, which reads as a tank; `opus5-millrace`
draws its ring to x −132 on a board whose bbox ends at −130, and the last column before the void comes back
as water. `shore` is a bank band a few cells wide and not a beach — a shore that should read as sand for
twenty cells wants a theme of its own on the ground under it.

### Relief is keyed by group id across the whole stack, and `*` is the ground's alone

`SketchRasterizer.ReliefFields` walks every layer and looks each of its groups up in the one
`relief` dictionary, adding that layer's `base_y` to the field it solves. So a stacked board can give
each storey its own landscape — `{"team": …, "walls": …}` — and a layer's marks are stated in **its
own frame**, not the board's. `drive.py`'s `"*"` expands over the groups the *compile* emitted, so a
key stated beside it survives and names a layer added in the finish.

### `relief_scope: exclude` takes a tier out of the elevation model entirely

A five-tier board of ~19 000 ground cells reports 4 294 cells to `relief/read` — the one tier that is neither
`hold` nor `exclude`. Everything above the base tier is outside the solve, so its variation has to come from
shapes: `raise` landforms, `sink` basins, `anchor_heights` tilts and ramps. Budget for that when designing a
stepped board, because "add relief" is not available as a later fix.

`hold` and `exclude` differ in how the join reads, not in whether the shape stays flat: `hold` lets the ground
ramp up to meet the shape, `exclude` meets the tier below at a face. A terrace wants `exclude`.

### A flight's anchor is an absolute height, and the relief does not know about it

`anchor_heights` on a `height_mode: "level"` polygon states world heights, so a flight arrives where it was
told rather than where the ground is. Where the relief left a bank two courses above the anchor, the crossing
read `BARRIER +3 at (−10, 51)`: the flight correct, the ground correct, the join unwalkable.

The fix is an `area` mark pinning the ground flat at each end of the crossing, and it is that instrument's own
case. An area pins a flat disc and is right **where flat is the point** — the ground a bridge lands on, the
pan a sough discharges into, the shelf a goal stands on, the two banks of a ford. Everywhere else is a `point`
at radius 4–6 with the relaxation between them.

---

## Shapes

A shape is drawn on a layer and resolved against every other shape there. Its height, its edge and its footprint are three separate statements, and each has its own field.

### `base_height: N` puts the top block at `y = N−1`

Confirmed at every tier on every board that has traced a real map. Any plan matching absolute heights is one
low until this is applied.

### Among the shapes of one layer, the taller override-add wins the column — not the later one

`RasterGroup` resolves a layer as `((adds − subtracts) ∪ override-adds) − override-subtracts`, and both the
plain adds and the override-adds are accumulated through `MergeCell`, where **the taller surface wins**.
Only the *set* an override-add belongs to is privileged; within that set, document order decides nothing.

That reads as an implementation detail and it is the difference between a tunnel and a sealed one. An end
wall drawn as one rectangle across the mouth of a ramp is 15 courses tall where the ramp under it is 7, so
the wall wins every column they share — and the way down ends in solid rock. Measured on
one board before the fix: `(−8, 60)` read solid `y0..21` with no air in it, a three-block plug at
`z 59..61` sealing both mouths, with `SK11` reporting 676 and 294 places of standable ground with no route
onto them.

**So a wall that meets a ramp is drawn in halves, one either side of it.** The general form: on one layer,
*anything shorter than what crosses it is not in the world there*, which is the same fact `SK9` reports for
a shorter shape inside a taller one and the same reason a room with a sunken floor is drawn as rectangles
clamped **around** the sunken part rather than under it. Ordering the document does not fix it, because
order is not what is read.

The cheap check is a column transect down the way in. A ramp that works reads one course of fall every two
blocks the whole way; a plugged one reads a solid run where the air should be, and nothing else on the board
says so — the export gate stays open, `render/traversability` can still answer one component, and the only
complaint is an `SK11` that is easy to write off as a quirk of a stacked board.

### A ring is one polygon, and it is what a floor that rises or a surface that falls is drawn with

Nesting settles a contest by height — the taller add wins the column and brings its own floor — so nested
shapes write any field that **rises** inward from one shared floor with no subtraction and no complaint. A
ziggurat, a cone and a solid dome are all that one move.

**Give the nested shapes a rising floor and the world is right but the report is not.** Every nested pair is
then a span the layer had to drop: eleven discs shaped as a hollow dome on radius 11 raise **sixteen** `SK9`,
and a board carrying sixteen complaints it means has no gate left for one it does not.

**Give them a falling surface and it comes out wrong and says nothing.** Eleven nested discs sized as an
amphitheatre build a **flat plate 22 cells across at one height**, with no `SK9`, no `SK10` and no finding of
any kind, because the disc that should keep only its own ring is the tallest thing over the middle too.

**What both cases want is shapes that do not overlap, which is what a ring is.** An outline is filled
even-odd, so one polygon — the outer circle, a slit inward, the inner circle the other way round, and back —
is an annulus with no subtract in it; the same eleven tiers stated as rings raise nothing and build the dome
and the bowl alike. `techniques/sculpture-with-layers` is the worked card.

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

One measurement covers the whole range, probed on flat ground. A `skirt` of **0** builds the edge as one
sheer step of the whole lift and reads as a monolith. A skirt of about **half the lift** builds two-block
risers — a lip crossed with a placed block rather than on foot. A skirt **at or over the lift** builds
one-block risers all the way round, which is a landform walked onto from any side.

So `raise 7, skirt 10` is an outcrop a player strolls up and `raise 7, skirt 0` is a standing stone,
from the same two fields. A shape meant to belong to the terrain wants the third row and a theme in
the ground's own family — plain stone under a grass meadow — rather than an accent.

**Grass painted back over it is the rest of the merge, and it is free.** A path prop replaces the
surface finish and adds no cell, so two to five `worn` brushes with a grass pave, drawn as tongues
over a crag's shoulders at different angles, let the rock show through the grass instead of the
grass stopping dead at the shape's outline. The crag stays one plain theme and the seam disappears.

**`skirt` is one number for the whole outline**, so an outcrop is uniformly walkable or uniformly
steep; `anchor_heights` tilts the *top*, not the edge. There is no per-vertex skirt.

### An erected shape is the pillar idiom, and its theme has to go in `fill`

`height_mode: raise` with `skirt: 0` and `floor: 0` is one abstract monolith: the top stands a stated
amount over whatever ground the footprint covers, the face is sheer on every side, and the plan is
whatever polygon was drawn. `anchor_heights` slants that top per vertex — measured on flat ground at
y11, a raise of 10 with no anchors tops at y21 everywhere, and the same shape with
`anchor_heights: [4, 4, 16, 16]` runs y19 → y25 across its own footprint. Leave `controls` off
entirely and the corners stay sharp, which is what makes a stone read as broken rock rather than as
a small group.

This is a **different device** from a stack of plates at successive `base_height` — the way
`tools/seeds/ruediger.layout.json` builds its steps — and both are right for what each does. Plates
are a staircase; a raise is a thing standing in the terrain.

**Put the pillar theme's `layered` stack in `fill` as well as `surface`.** The surface bucket is the
top few courses, so a stack stated only there bands the head of a 30-block monolith and leaves the
whole face plain — and the face is the entire point. Stated in `surface`, `wall` and `fill`, a column
read runs the strata bedrock to top.

**And take the pillar out of the ground's tone family.** On a board whose exposed ground is stone,
a pillar painted andesite, polished andesite and cobble is terrain wearing a different seed:
`render/surface` shows it as ground. The rule the brief states for a building — never the same family
as what it stands on — is the rule for an erected landform too.

### `height_mode: sink` is a quarry, and its anchors are its depth

`sink` with `skirt: 1` cuts sheer faces and a flat floor — measured, a lift of 6 on flat y11 ground
gives a clean 6-block drop to y5 and back. `anchor_heights` on a sink states the **depth** per
vertex, so a ring whose corners read 2, 3, 6, 6 comes out four down on average and tilted.

**Notch it rather than tilt it.** Setting most of the ring to full depth and the two vertices on one
side to 1 gives a pit that is sheer nearly all the way round with a single shallow ramp in; a linear
tilt across the same ring turns the whole shallow half into a bowl and the cut stops reading as a
cut. Without a way in, the floor is a **stranded walkable place** — `relief/read` reports it as an
extra `places` entry with the largest share below 1, which is the only thing on the board that says
so; a top-down cannot show it.

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

They are alternatives rather than a pair. A `height_mode` says the shape stands **out** of the field — it is
applied over ground the relief has already made, so the solve never had an opinion about its top. A
`relief_scope` says how a shape that is part of the ground **takes part** in the solve. A shape stating both
has the scope ignored, silently, because the field bound and was simply not consulted.

The scope has four words and the fourth goes unused. `follow` takes the height the field settles on under the
shape and holds it flat there, so the shape moves with the terrain and keeps a level floor — which is what a
room wants, since a plan states its piece's height before any ground exists. `hold` pins the stated height
against the relief, `exclude` takes the footprint out of the solve, and absent is `inherit`: the shape is
part of the group's ground.

**Measured, a shape stating both comes out identical to the same shape stating only the `height_mode`** — a
`level` plate at `skirt` 0 with and without `relief_scope: "hold"`, compared column by column over both
panels, differs in not one of 7,296. `ScopeOf` returns `Inherit` for any shape declaring a `height_mode`, so
the field bound without being asked. Nothing refuses it and `RQ3` does not fire, because the field was read
and discarded rather than left unread. `techniques/made-ground` is the worked card.

**`follow` is not the gentle option: it seats the shape and then solves the group a second time.** `SeatOf`
reads the field just outside the footprint on every edge and takes the **median** of it, pins that as a rigid
`AreaMark` and re-solves — so the land around a `follow` shape is re-graded to arrive at it exactly as
`hold`'s is, and the only difference between the two words is who chose the height. On a hillside falling 26
to 10, a piece stating 24 came out at **18**, which is in no document.

**`exclude` keeps the raw column, and the raw column is not the excluded shape's.** A piece stating
`base_height` 24 inside an island stating 44 built a plinth at **44**: the taller add still wins the column,
and the word only says the relief may not answer for those cells. Rebuilt with the island at 30 the plinth
reads 30. A shape wanting a plinth at its own height has to be the taller add over its cells, or say
`height_mode`.

**A `skirt` is paid for from every side at once, so one over half the shape's narrow dimension leaves no
top.** On a 26-deep plate: `skirt` 0 leaves all 26 cells at the stated height, `skirt` 6 leaves 15, and
`skirt` 14 leaves **2**. It is the same arithmetic that empties a mark whose `bevel` is wider than half its
band.

**The relief read cannot see an erected shape at all, and `RL5` will say so out loud.** Eight panels
differing only in these words all read `relief` 16 and `landform: rolling`, while the built worlds ran from a
bare hillside to a 44-block plinth; `level` moved with the three scopes (0.18, 0.44, 0.35, 0.32) and not at
all with the three skirts. `RL5` fired on the panel carrying a ten-block sheer plate, saying it *presents no
face at all — it is a ramp end to end*, which is true of the solve and false of the world.

**A `cell` pattern is anchored in world space, so one shape built at two places on a board does not paint
alike.** Two panels identical in every column stood 330 blocks apart and disagreed on 92 cells, every one of
them in the rock band, each reading stone where the other read cobblestone.

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

A `ramp` polygon falling 18 → 6 over **12** cells rasterized as `18 16 16 14 14 12 12 10 10 8 8` —
six steps of two — and `…/walk?aim=reach` answered `blocks 3` climbing it, because the walk prices a
rise of δ at δ−1 placed blocks. The same 12 courses over **20** cells reads one course a cell and
walks both ways for nothing. The rule to author by: **run at least twice the rise** on any stair
meant to be climbed rather than fallen down. (A 20-course ramp over 32 cells was right first time.)

**A flight is one shape, and the gradient is the whole of what decides it.** A polygon carries a height per
vertex and the rasterizer interpolates between them, so a tilted quad *is* a stair — the courses are what a
sloped surface rasterizes to. At 1:1 the worst step is two blocks; at 2:1 and 3:1 it is one. Where the ratio
holds, a flight is a single polygon with `height_mode: "level"`, `skirt: 0` and a thickness per vertex, in
place of one rectangle a course.

**Where the space is fixed, one rectangle a course is the only correct form.** A shaft 24 blocks long that
must fall 24 courses cannot be 2:1, and neither can a slipway climbing 8 courses out of a river 16 wide.
Those stay per-course, and so does anything **clipped round an obstacle** — rectangles can be cut round a
rectangle with plain arithmetic and a single tilted polygon cannot.

### Three points and a plane is how you tilt a shape deliberately

`anchor_heights` is per-vertex, which is one number too many to pose by hand and one too few to be a
gesture. Stating three and solving for the rest is the gesture:

```python
def plane3(ring, pts):
    """pts is three (index, height) pairs. Solves a*x + b*z + c = h through them, fills the rest."""
    (i0,h0),(i1,h1),(i2,h2) = pts
    (x0,z0),(x1,z1),(x2,z2) = ring[i0], ring[i1], ring[i2]
    det = (x1-x0)*(z2-z0) - (x2-x0)*(z1-z0)
    a = ((h1-h0)*(z2-z0) - (h2-h0)*(z1-z0)) / det
    b = ((h2-h0)*(x1-x0) - (h1-h0)*(x2-x0)) / det
    return [max(0, round(a*x + b*z + (h0 - a*x0 - b*z0))) for x, z in ring]
```

Pick the three by the axis the lean should run along — the two furthest downwind at 0, the one
furthest upwind at the lift — and every shape on the board leans together instead of each being its
own accident. On a `rot_180` board that gives each team the cliff and its own side the ramp for free.

### `rot_180` maps a shape centred on the origin onto itself, so a central lake may be any shape

The mirror does not force a circle; assuming it does is what produces one. Any outline with a
half-turn in it is already symmetric, so a profile of radii covering **half** a turn, repeated at
θ+180°, gives a lobed, elongated or kidney-shaped water that fans without error. Smoothstep between
the profile's entries or the outline comes out faceted, and give the helper a `swell` so an outer
ring can depart from a circle less than the waterline while staying the same shape — that is what
keeps a beach an even band round a shore that is nowhere an arc.

### A made layer is built once unless its group says it mirrors

A layer's shapes are fanned onto the symmetry's orbit axes only where the group carrying them has
`mirrors: true`. A group is the unit, not the layer and not the shape, and `SketchGroup.Mirrors` defaults
to `true` on the wire — but `tools/sculpt/props.py`'s `LayerBuilder` defaults it to **`false`**, which is
right for a landmark seated on the symmetry centre and wrong for everything a team owns. Every factory in
that module forwards `**kw`, so `mirrors=True` is how a per-team structure asks to be fanned.

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

The three routes that do it are `PATCH /map/{slug}/sketch/shapes/{id}/vertices/{index}` (move one point),
`POST …/vertices` with `{"after": n, "x": …, "z": …}` (add one on that edge, and the answer says the index it
landed at) and `DELETE …/vertices/{index}`.

**Every other point of the outline is exactly where it was drawn after each of them.** That is the property
the whole thing exists for: a board's shapes abut, and an edit that drags a ring's other points opens ground
between two that were flush.

State the point in the insert rather than splitting first and moving second: the one call is atomic, so a
point that would fold the ring leaves the outline untouched, where the two-call form leaves the midpoint
behind. Omitting `x`/`z` is the other case and is the midpoint anchor — a corner half way along a wall,
placed before it is decided where it goes. Nine such calls take a one-piece plan's compiled rectangle
(4 vertices, 24,000 blocks²) to a 12-point outline of 28,084, **+17%**, with all four of the compile's own
corners still exactly where the plan put them.

**A spec states them under `editShapes`**, an ordered list per shape replayed after the store and **before**
any bend, since a bend resamples whatever ring it is given. Each op names exactly one index — `after` inserts
a point on that edge, `index` moves the point there, `remove` drops it — and one naming none or two stops the
run rather than guessing. The indices shift as the ring grows and shrinks, which is why the run prints where
each point landed:

```json
"editShapes": {"garth-14": [{"after": 1, "x": 92, "z": -70},
                            {"index": 4, "x": 80, "z": -60},
                            {"remove": 7}]}
```

A hand works at a larger scale than a bend does. One board's four
ground shapes are the plan's four rectangles reshaped by hand, each grown from four vertices to between six
and eleven, and 14,250 blocks² of compiled rectangle became 16,008 drawn — **+12.3%**, with every one of the
four larger than the rectangle it came from.

Every one grew. Of the 36 drawn vertices, 19 sit **outside** the rectangle they came from by 2 to 20 blocks,
7 sit inside by 4 to 8, and 10 stay on the edge. The document carries **no Bézier handles at all**. A reshape
that far outward and that uneven is not reachable by any whole-ring transform, and it is reachable one point
at a time.

A board inheriting those shapes **vertex for vertex** adds no handles either — its curves are `path` shapes,
which is the layout's other curve and the one nothing has to author.

The three canal walls are `wall-s`, `wall-n-w` and `wall-n-e`: three or four clicked points, `radius 1`,
`stroke_edge: solid`. The rasterizer runs a polyline's points through a centripetal Catmull-Rom spline at
eight samples a segment before offsetting the band, so four points become a twenty-five-point centreline and
the wall draws as a curve. `cairn-wall-0`–`2` are the same shape at nine or ten points over about twenty
blocks.

Reach for a polyline wherever a wall, a lane or a watercourse should flow; reach for `controls` only on a
closed ring of ground.

### The bend is the studio's, and the side is the author's

`POST /map/{slug}/sketch/shapes/{shapeId}/bend` draws a compiled outline as a coast, and `drive.py`'s
`bendShapes` calls it once the board is stored. **The outline's own vertices never move** — that is the rule
that makes one safe, and it is the studio's.

Which way the cut points go is `side`: `out` is the default and is the slight bloat that makes a compiled
rectangle read as land, `in` keeps the plan's footprint where shapes abut on a measured strait, and `both`
wanders across the line the plan drew.

The side is decided by offering each inserted point both perpendiculars and taking the one that lands where it
was asked to — right for a ring wound either way and for a concave stretch as readily as a convex one, which a
shoelace sign is not.

Measured on two rings compiled against each side: one at 9,750 blocks² bent to 11,033 outward and 8,467
inward, the other at 4,800 to 5,477 and 4,123 — **+1,283 against −1,283**, and **+677 against −677**. The
same magnitude with the sign reversed is the whole of what the side chooses. The studio's outward
coast is vertex-for-vertex the coast every bent board in `specs/` was authored against, so those boards
re-drive to the ground their props were placed on.

### A vertex insert names the edge leaving that vertex, and the index moves under it

`POST …/sketch/shapes/{id}/vertices {"after": n}` inserts on the edge from vertex *n* to *n+1*, so the index
to state is the one **before** the edge wanted — and after a run of inserts it is not the index that edge
started at. Ten inserts on a six-vertex ring put the west flank at index 9 rather than 8, and `{"after": 8}`
landed on the board's own back edge and folded the ring.

A folded ring refuses nothing. The store answered 200, the export answered 200, `preflight` answered **export
gate OPEN**, and the world carried **ten blocks of void inside the landmass** at `x −30, z 40..49`. A transect
is what found it. Count the indices as the ring grows, or read back the index each insert answers with.

### Bézier `controls` — the semantics, and where the curve actually is

`controls` is keyed by **vertex index as a string**, and the handles are **absolute board coordinates**:

```json
"controls": { "5": { "in": [77, 25], "out": [77, 35] } }
```

The edge from vertex *i* to *j* is the cubic `p0 = V[i]`, `c1 = controls[i].out`, `c2 = controls[j].in`,
`p3 = V[j]`. So a vertex's **`out` bends the edge after it and its `in` bends the edge before it** — one
vertex's handles belong to two different edges. A missing handle falls back to the endpoint itself.

**The extremum sits between vertices, never at one.** Probing the vertex is the natural check and it is
worthless — the vertex is a fixed point of the curve. Probe near `t = 0.5`.

**A handle that travels further away from its edge than along it makes a lobe, not a corner.** Place every
handle as `c1 = p0 + d·t + n·bulge`, `c2 = p3 − d·t + n·bulge`, with `d` the edge vector, `n` its outward unit
normal and `t` a forward fraction (0.3 works). Two constraints keep it a corner: `t·|d| ≥ bulge`, so the
handle travels further along the edge than away from it, and `bulge ≤ 0.35·|d|`, because a short edge cannot
carry a big bulge.

Break the first and the cubic doubles back into a cusp, and past that a self-intersecting loop that rasterizes
as a detached scrap of land. Break the second — an 8-block handle on a 15-block edge — and you get a deep U
hanging off the shape, which flattens without self-intersecting and still reads as a bulb. Flatten the
finished ring and test every non-adjacent segment pair for intersection before posting: a curve that *looks*
right in numbers can still cross itself.

**And keep the curve away from two things.** A **seam** a player walks — bow it and the two pieces stop
touching. And a **wall**: its width was fixed at compile from the plan's seam, so bowing the coast beside it
widens the lane past the wall's ends and hands players a way round it. The wall rects are in
`POST /api/plan/inspect`'s structures feed; veto every edge within 10 blocks of one.

### A corner recipe does not make a coastline: a closed ring wants tangent continuity

The handle construction above — `c1 = p0 + d·t + n·bulge`, with `t·|d| ≥ bulge` and
`bulge ≤ 0.35·|d|` — is the recipe for **one** corner, and it is correct for one. Applied to every edge
of a closed outline it constrains each edge against itself and says nothing about the two edges meeting
at a vertex, so every edge bows outward and meets its neighbour in a cusp. A 24-vertex group authored
that way, with both constraints satisfied and no self-intersection, rasterizes as a **gear**: twenty-four
points around a blob.

An organic outline is a smoothness constraint between edges, not a bulge on each. Catmull-Rom converted
to Bézier gives it in one line and is tangent-continuous at every vertex by construction:

```
c1 = P1 + (P2 − P0)/6        # controls[i].out,  edge i → j
c2 = P2 − (P3 − P1)/6        # controls[j].in
```

with `P0`/`P3` the ring neighbours. Raising the divisor flattens the curve toward the polygon; 6 is a
natural coastline at a 12–20 block vertex spacing.

**Leave the seam edge alone.** On a `rot_180` board the edge a shape shares with its own image — the run
along `z = 0` — takes no handles at all: straight, the mirror lands on it exactly, and the two halves are
one group. That is the same warning the entry above gives about bowing a seam, and it is the one edge of
the ring that must be excluded from whichever construction is used.

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

A layer's span is inclusive of its top, so an upper layer sitting exactly at the lower one's top shares that
course and is the ordinary seam. Past it the two build as one solid mass and the gap the layers were drawn to
have is not in the world there.

A bridge deck at `base_y 11` lapped two blocks onto banks topping at y11 read `SK10 — driven 2 block(s) into
each other over 24 column(s), deepest at (−26, 62)`. The same deck sized to the cut's own columns exactly, one
course thick, laps nothing, sits flush with both banks and leaves four courses of air under it.

**The seam sits where it does because a layer's segment top is `base_y + base_height` while its built top
block is one lower.** A court stating `base_height` 14 has its top block at y13, so a one-course deck at
`base_y` **14** rests on it, shares one course by the gate's arithmetic and raises nothing.

**One lower than that is `SK10`, and the slab is absorbed exactly where the layer below reaches it.** A
gallery's roof set one course into its wall heads left mossy brick on top of the wall line and no plank
anywhere in that column, while inside the gallery — away from the walls — the same roof stood a course lower
with its storey intact. The fault is local, the world is built, the column is valid, and the gate at the door
is the only thing that reports it.

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

`TerrainBuilder.SurfaceTops` keeps the **maximum** `YTop` per `(x, z)`, and that single grid is what
the painter, the structure floors, the placements, the dressing and every 2-D render consume. Four
consequences, all measured:

- **A placement climbs onto the upper layer by itself.** A destroyable stated in plan cells with
  `float: 4` landed at y34 over a terrace and at y19 on the same plan with the layers stripped.
  Putting an objective on a deck is not stated anywhere — it follows from drawing the deck over it.
- **The covered ground keeps its own paint.** `TerrainPainter.Paint` orders the layers by lowest
  surface and paints each over its own span, so a court under a deck and the same court beside it come
  back block for block alike — measured on a theme whose `fill` is deliberately a different block from
  its surface, which is what makes the two tellable apart at all.
- **A covered floor is not in `themes/census`.** The census counts each column's *top* surface, so a
  board stating four themes reported three: every cell of the fourth had a roof over it.
- **The covered ground cannot be dressed.** A tree stated at `(8, 53)`, where the ground is a hall
  floor at y14, stood at y28 on the roof. No decline mentions it.
- **Theme scope is per layer.** `ShapeScopeOwners` keys on `(layer, x, z)`, so a shape owns the paint
  only on its own storey and ground under a slab keeps whatever its own layer states.

### A ground ramp meets an upper slab by touching it, and nothing else is needed

Where a relief-solved ground top equals an upper layer's top, the two columns merge into one solid mass and
the join is a single one-block rise. The failure is one column wide: a causeway whose band reached x ±19
beside a terrace drawn to x ±18 left one column of hall floor between them — a twelve-block slot, and the deck
a group in the air.

**Overlap the two footprints by a column**, or arrive one course under the slab, which is enough: a causeway
climbing to y17 beside a deck at y18 joins it on a one-block rise. Check it with a transect either way.

**`SK11` at the store door is what reports the miss, and it is silent on the join.** The same causeway stopped
one column short left a single column of court five below the deck, and the store answered *2,912 place(s) of
standable ground … have open sky over them and no route onto them from the rest of the board* for both the
deck and the court it sits over — and said nothing about the panel that met. `traversability` and
`WorldColumns.Membership` still both discard Y, so those two go on calling a layered board one component.

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

**This is the one sentence most of a water prop's behaviour follows from**, and `DR-BANK` is the rule that
says it: *the line is the lowest surface the body crosses and every column over it is emptied down to it*.

**So a channel run down a fall is built as a trench, not as a beck.** One drawn from a head at 30 to a foot
at 16 took 16 as its line and reported *cut **14 course(s)** of ground away above its own line — a
straight-sided wall from y16 to y29*. Keep a run within a course or two of level, state a `level` and accept
the rim, or break it into reaches that each cross flat ground — a reach left dry still lays its bank
materials, which is worth having where the board can afford to call it a sink.

**A bridge is bitten through only when the prop names no layer, and naming one is the whole fix.** A water
prop carves against `DressingContext.GroundFor`, which is the ground of the layer it **names**; with none it
takes the top of the stack, so a beck under a deck at y25 read the deck as its own ground and cut *6
course(s) … from y20 to y25*. The same beck with `"layer": "ground"` builds planks at y25 with water at y19
under them and declines nothing.

**So a board can have the water and the bridge, and every prop kind takes the field.** This is the prop rule
met where it matters most rather than a rule about water, because water is the one prop that changes the
ground it is placed on.

`techniques/water` is the worked card, with both cases side by side.

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

Every prop kind takes `layer` and `DressingContext.GroundFor` reads it — a house, a tree and a boulder all
seat on the storey they name; measured, a kiosk stated for a pool hall stands with
its roof at y10 under a concourse whose floor is y12, and an oak stated for the car deck stands at y42.

**A stroke does not.** Two lane markings carrying `"layer": "under"` came back from `POST …/sketch/dressing`
with `"y": 25` and `"y": 17` — the corridor wall's coping and the corridor floor, over the basin they were
drawn for — and a worn track stated for a hall at y18 came back at `"y": 37`, on the deck roofing it.

Nothing declines, because `DR-LAYER` fires on a layer the board does not have and these are layers it has.

**Mark a covered floor with a shape instead**: a rectangle of that floor's own `floor` and
`base_height` carrying a different `theme`. The geometry is unchanged and the theme scope resolves
per layer, so it lands exactly where it is drawn. Both of the pool's lanes are three-wide rectangles
of the basin's own two courses, themed dark prismarine.

---

## Painting

A theme is stated on a shape and a cell goes to one of them. What decides which is not what decides the column's height, and the two answers differ more often than they agree.

### Height and paint resolve overlaps by *different* rules

- **Height**: `RasterGroup`/`MergeCell` — *the taller add-shape wins* the column.
- **Paint**: `ShapeScopeOwners` — *the smallest-area shape wins* the cell (the most specific scope).

The documented way to make an organic tier is to let the tier below **run under** it, so the upper one can
pull inward without opening a hole. But where the lower tier is the *smaller* shape, it keeps the paint while
the upper tier keeps the height — a band of the wrong material laid across the top of the upper terrace, as
deep as the underlap.

Measured on a five-tier board at `x = 0`, with `shelf` (`base_height 22`, quartz, ~3 300 cells) overlapping
`terr-mid` (`base_height 18`, grass over sandstone, ~1 500 cells):

Three columns down one line tell the whole story. Where the shelf stands alone it reads y21 and quartz,
which is right; where `terr-mid` stands alone it reads y17 over grass, dirt and sandstone, also right; and
where the two overlap it reads **y21** — the shelf's height — under **grass, dirt and sandstone**, which is
`terr-mid`'s paint on the shelf's blocks.

**Check which way round each join sits before building.** Where the upper tier is the smaller shape the
problem does not arise at all. Where it is not, author the two edges to overlap by two to four blocks and the
seam reads as a transition rather than a stripe.

**It reaches made things too, and there it is worse.** A hill's outer ring crossing a town wall leaves the
wall built to its own twenty-seven courses and finished in the hill's grass-over-dirt, sides included,
because the hill theme's wall material is dirt. `SK15` names the pair, both themes and the columns they
contest; before it, a column read was the only thing that saw it.

**Cut a mound out of what it may not land on** rather than trusting the heights to sort it.

### A shape owns the paint on a cell only where its own drawn top is the tallest drawn top there

Scoping a theme to a patch of ground is an authored shape carrying a `theme`, and whether that shape owns
any of the paint it carries is decided by one comparison. `SketchRasterizer.ShapeScopeOwners` gives a cell to
the smallest shape whose own top **equals** the tallest one on it —
`scopes && (standing || top == held.Ground) && area < held.Area`.

**A shape stating no height at all is one course at bedrock, not "no opinion".** `RasterShape` takes its floor
from `Floor ?? 0` and its thickness from `HeightFn`, whose last line is `double bh = s.BaseHeight ?? 1`. So a
brush drawn thinner than the landmass under it reaches no surface, owns nothing, and reports nothing.

**`override: true` does not rescue a brush that is too short.** Only the *set* an override-add belongs to is
privileged in `((adds − subtracts) ∪ override-adds) − override-subtracts`; the ownership test inside that set
is the same one. It is, however, the one form the store complains about, as `SK14`.

**So the form a patch takes is the ground's own `floor` and `base_height`, and the relief settles the
height.** `RasterizeLayout` writes the solved surface back over every cell of a solved group's footprint, so
a twelve-course patch on a plain that solves to y7 is built at y7 and differs from its neighbours only in
paint.

**A shape declaring `height_mode` is a candidate whatever its height, and is never flush.** `Erect` settles a
cell at `datum + rise * Math.Max(1, floor(surface))`, so a `raise` of zero stands one course above the datum
and a `sink` of zero one below. The datum for both is the **median** of the ground under the footprint, read
once, which turns a brush drawn across a flank into a bench.

**Where the relief never solved, nothing writes a height back and an override stays one course on bedrock.**
A shape carrying `relief_scope: "exclude"` takes its cells out of the group's footprint, and an override
stroke over such ground punches a hole to y0 rather than repainting anything.

**A shape on a second layer never enters that contest at all, and that is why it is not paint.**
`ShapeScopeOwners` keys by `(layer, x, z)`, so the shape owns its own layer outright and what is *seen* is
settled afterwards by which layer's top block is higher. A twelve-course patch on a layer at `base_y: 0` is a
slab that buries itself in the terrain — `SK10`, "driven 9 blocks into each other … they build as one solid
mass" — and over a hill the ground wins most of it.

**The one second-layer form that behaves like paint is a single course at the ground's own top**, `base_y`
set to the surface below plus one. `base_y` is one constant for a whole layer, so it works exactly as far as
that ground is level, and giving the layer its own relief makes it worse: two fields solved over two
footprints do not agree.

**`GET .../themes/census` is the only witness either way**, because a patch that owns nothing builds a world
that looks exactly right. `techniques/painting-a-patch` is the worked card: twelve statements of one outline
under one paint, of which eight land.

This is the instrument a detailed surface is painted with — a drift of sand against rock, scree at the foot of
a crag, mud in a hollow — and it is what a single large `voronoi` over a whole region is a substitute for.

### A fill pattern is a plane until it states a `rise`, and the gate now refuses one without

**`PT4` refuses a fill or wall pattern that states no `rise`** — *fill samples its field in the plane only,
so every block of a column resolves alike and it reads as vertical stripes. A rise is the vertical period
that gives a face its grain.* The board does not store until it is added, so this is no longer a trap to
remember.

**`PT1` refuses a surfacing block as a band's whole material** — *a surfacing block is exactly one course
thick and what is under it is soil*. So every band of a `height`, `slope` or `inward` stack is itself a small
`depth` stack: one course of the surfacing block over earth. Both refusals are at the store door and name the
exact JSON path.

Every area pattern — `cell`, `voronoi`, `noise`, `turbulence`, `electric` — samples the plane by default
(`TP15`): a column resolves to one block, so the pattern decides the ground and nothing else. On a surface a
course or three deep that is right and cheap.

On a **fill** it is a cliff of vertical stripes: a six-stone body stated as a `cell` of `turbulence` mixes
with `rise` at its default builds with every cut face striped floor to sky, one cell's stone the whole
height of the column.

State a `rise` and the field is a volume — but a cell as tall as it is wide still reads as a column on a cut,
because a cut face shows a cell's width and its height side by side and a square blob of stone is a post. A body
stated as cells of 7 with a rise of 7 still reads as vertical runs on every cut face.

Make the cells wider than tall. A body stated as a `cell` nine across with a rise of five, over turbulences
seven across with a rise of four, builds runs of one
material down a column are 40% one block long, 23% two and 16% three, a mean of **2.5** — a blob, not a
stripe.

The earth is the other way: three courses deep, so a rise of eight there makes each column's earth one
material (64% of columns) and the mix shows across the ground rather than down it, which is what a cut through
soil looks like.

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

### A cliff's strata belong in the `wall` bucket, because a cliff is what that bucket paints

**The wall is the column's body at an edge, not a coat on a slope**, so nothing of it shows from above: it
replaces the fill from the bottom of the surface down, wherever the column stands on a void-facing edge or —
with `wallOnTerrainFaces` — on a terrain face. Measured on one board that was 440 columns, 244 round the
island's rim and **196 inland** on a mesa's own skirt. A wall and a fill are read on a cut.

**`rimEdges` decides how much the rim claims and the difference is large.** `void` caps only the landmass's
true outside; `boundary` caps every plateau boundary in it, which on the same board was **1,310 further
cells**, 1,244 of them inland. `techniques/theme-buckets` switches the four buckets on one at a time over one
ground.


A band stack takes one of four axes — `depth` down the column, `inward` from the void-facing edge, `height`
up from a stated world Y, and `slope` by the ground's angle. A `wall` stack on `depth` is read from the top
of the face, so on a board whose drops all begin at one shelf, banding by depth **is** banding by altitude
and `height` is not needed. One stack shared as the wall material of every theme makes every cut on the board
the same rock in the same order, and puts those colours nowhere else.

**A `height` stack leaves everything under its own `from` to the bucket beneath, and one block is enough.**
A stack stated `from: 8` over a plain topping at y7 read back as the fill's own block — the whole plain
unpainted for an off-by-one — and nothing reports it.

The counterpart: **`wallRun` stands vertical**, because its stripes wrap the perimeter and are
constant up a column. A weathered cliff is bedded and a sawn one is scored, and the two are one
bucket and two materials.

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

`HP3` names the cap in its refusal — *"the wings cover 232 blocks, past the 192 a placed building may
take"* — so an L of a 16×9 hall and an 8×11 wing is refused and one of 14×8 + 7×10 is not. Draw the
plan shapes to fit it: a U of a 16×7 hall and two 5×7 wings is 182.

A **storey** carries `clear + 1` courses of wall (the top storey carries none extra, the roof being its
lid), so a wall stack longer than that is silently truncated: a seven-band brick/checker/spruce stack
on a storey of clear 3 builds four courses of brick and checker and no spruce at all, and the section
reads as one flat mass. Size each storey's own stack to its own clear — which is also what makes a
three-storey building read as three rooms rather than as one tall wall.

**`POST /terrain/prop-preview` is the read for a multi-wing house.** It takes the prop — wings and all —
plus a theme, and answers plan and section as PNG at `?format=png&view=…&scale=8`.
`room-styles/preview-snapshot` draws the style on a default box, which for an L or a U is not the
building being placed.

### `DR-SLOPE` is gated on the building's own height, not on the wall it stands against

A house straddling the rim of a pit eats the wall. The decline fires at a rise of `wallCourses + 2 × roof
pitch` — 7 for a one-storey shell, 13 for a two-storey one — so **the taller the building, the deeper the
pit wall it may quietly carve away**. A one-storey shell is refused at rises of 11 and 12 where a two-storey
one is allowed all three.

Built, the column under such a house has lost every course above its floor while the column one cell outside
the footprint is whole. Check a footprint against the rim it sits on rather than against the rule.

### Wing corners are inclusive, and the joint roles are ridge-derived

An `AuthoredWing`'s `corners` name cells inclusively: `[[0,6],[9,10]]` covers row 6 *and* row 10. Two wings
sharing a coordinate row therefore **overlap** (`HJ1`); a touching wing starts one row past its hall
(`maxZ` 77 → wing `minZ` 78).

**Which rectangle is the hall and which the wing follows from the ridges**, not from your drawing — the wing's
ridge runs *into* the shared edge. So an explicit `ridge` stated to dodge an `HJ3` tie can silently swap the
roles, and checking a rule against the rectangle you *drew* as the wing reads a firing `HJ5` as satisfied. The
refusal names the derived roles ("the wing (rectangle 1)…"): read the indices in the message, not your drawing.

**A roughly square hall ties its ridge `AlongX`, which is `HJ4` waiting to happen.** A square-ish hall meeting
a wing on a vertical shared edge ties toward x, the wing then also runs into that edge, and both-into-it is
`HJ4`. State the **hall's** ridge along the shared edge (`AlongZ` for a vertical seam) and the wing's into it.

`POST /api/terrain/prop-preview` answers all of this before a build — but its body is `{propJson, themeJson}`
with the documents as **strings**, and a house prop's `style` must be the resolved `HouseStyle`, not a library
reference.

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

An authored `addShapes` polygon is ground, not a prop, so a building drawn over one stands inside it and is
reported by nothing — *unless the shape sets* `keepClear`, which makes it a real dressing keep-out with no
margin. A wall, a market cross or a stair flight authored as terrain and marked that way declines what leans
on it by name.

Test every footprint against every *unmarked* authored shape's ring yourself. *Measured:
`b-berm-e rests on (35, 32), which is kept clear for a stated structure` — a boulder declined for leaning on
a `keepClear` town wall.*

**Without the flag a prop does not stand beside the shape, it stands on top of it, and that is what nothing
reports.** Measured on two identical six-course walls: the marked one declined both props by `DR-KEEP`, and
on the unmarked one an oak's trunk began at y14 — the wall's own top course, six over the meadow — with a
boulder bedded into the head beside it. Only a column read says so.

**And an authored shape needs a field for each pass it crosses.** `height_mode: "level"` with `skirt: 0` is
what the relief wants — without it `SK14` fires and the wall comes out level with the ground — and
`keepClear` is what the dressing pass wants. Neither substitutes for the other.

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

A `copied` tree recipe carries `body: [[x, y, z, id, data], …]` from its foot, and the placement is a point
and a seed like any other tree.

The registry key minted for one stated inline counts its blocks (`copied-716`), so state the recipes under
names in `dressing.styles` — `oak-dense-2`, `fir-tall-6` — and let the placements name those.

The bodies come out of a world with `pgm-studio/tools/seed-trees.cs`, which files them in the library under
`<world>-r<row>-<n>`, and a spec's own tree file keys them the way its placements name them.

A body is written block for block, so its seat is its foot's column and a crown overhanging a slope is cut
where it meets it, exactly as a grown one.

**A body's foot is every cell of its lowest course, and that is what a standoff is measured from.** Measured
on two `tree-showcase` recipes: `r2-1` rests on one cell and `r3-1` on **nine**, spanning x 0..3 and z −1..3.
Anchored at the same three blocks off one road the slender one stood and the buttressed one was declined,
the message naming a foot cell rather than the anchor.

**And a hand-built crown is not a disc, not symmetric, and not even solid.** `r2-1` covers 144 plan cells
spanning x −9..+7 and z −7..+8, and its own trunk row reads `#######..####` — the cells at (1, 0) and (2, 0)
are holes in it. Which answer a neighbour gets depends on the cell its foot lands in and not on the
distance: a second copy two blocks east found the hole and was placed, and one three blocks east landed on
a written cell and was declined.

For scale against a template: those two bodies cover 144 and 147 plan cells where an `oak` of height 14
covers **67**.

### A prop is tested at its lowest course and claims everything it covers, and every distance follows

`Decorator.Seats` walks only the cells a prop rests on — `prop.Min(cell => cell.Y)` and nothing above it —
so a tree is judged by its **trunk** and a boulder by its **footprint**. What a placed prop then registers
is every cell it covered, crown and all.

**So what two trees need between them is one crown and not two.** The second oak is declined exactly where
its trunk falls inside the first one's claimed canopy, which makes the distance the *larger* of the two
crowns rather than the sum. Measured with one seed pair down each ladder, stepping along x only: a pair of
nines is refused at 1, 2 and 3 and stands at **4**; a pair of fourteens is refused at 2, 3 and 4 and stands
at **5**.

The crown is still hash-keyed off the prop's `seed` — `Decorator.CanopyRadius` measures what the build
writes — so a rung right on the threshold is not stable across an edit that shifts seeds. Four for a nine
and five for a fourteen are the measured floors; add one where a board is going to be revised.

**And a boulder's standoff is measured from its body, so its centre owes the standoff plus its own reach.**
A size-3 erratic stated 3 blocks off a road was declined at (−62, −68) for a road cell at (−63, −69): the
prop was two blocks out and its footprint was one.

Dart-throwing beats a jittered lattice here. A lattice at the spacing either reads as a grid (no jitter) or
breaks its own minimum (with jitter, which is what the rule charges for); thrown points accept right up
against it. Forty-five darts on a 53 × 45 pad were all taken, and the same box packs 98 at the limit.
`techniques/trees-and-boulders` is the worked card, every rule of it a ladder.

### DR-CLAIM between props is footprint overlap, not a standoff

`claims.Holds(x, z)` — a prop is declined for resting on a cell another prop has claimed, and that is
the whole rule. Reserving three blocks around each boulder cost twelve trees on a board that had
three hundred plantable cells; `body + size + 1` is the real margin. Two size-3 erratics three apart
contest and the same two nine apart do not.

**The order the pass runs in is by kind, and the document's order is the order only within a kind.**
`Decorator` walks water, then strokes, then houses, then boulders, then trees, then flora, so a rock always
beats a tree for a contested cell whatever the props array says. Measured: the same rock-and-oak overlap
stated twice with the order opposite declined **both** oaks. A wood grows round a rock because it cannot do
anything else, and the only order an author controls is between two rocks or between two trees.

### A path's band follows the spline, not your polyline

`Centerline.Of` runs the drawn points through a **Catmull-Rom spline** before the band is derived, and a
Catmull-Rom overshoots the outside of every corner — by several blocks when the segments are long. The band
does not turn a building away for merely touching it (the road runs to the porch), but it decides where the
*road itself* runs and what the scatter is refused over, so margin arithmetic against the polyline is
arithmetic against the wrong line.

**A building may end a road and never stand across one (`DR-CROSS`).** Drop a house on the pavement and the
road ends at its wall, which is what a road running to a door is. Drop one in the *middle* of a road and the
whole building is declined: the paving carries on out the other side, so what was one way through the board
is two dead ends facing a wall. Draw the road **to** the door rather than through the house.

Chamfer every sharp corner with two bracketing points — the spline then has nothing to overshoot — and read
`region/dressing-report.json` after a build, where a prop the band refused is named with its colliding cell.

---

### DR-ROAD measures to the cells a stroke claims, and a wide brush is still a road

`PlacePath` claims exactly what `StrokeFill.Cells(points, radius, style, coverage, seed)` lays, and
`RouteStandoff` is 3 for a tree and 2 for a boulder off any of them.

Two consequences that pull opposite ways: a `worn` stroke under partial coverage claims a scattered subset, so
a keep-out computed at `radius × coverage` lets props through that the gate then declines; and a stroke
wanders to its full radius, so a keep-out at `radius + standoff` is right — and twenty-one path props over a
110 × 220 board with that keep-out leave **eleven** plantable cells on the whole map.

**A `solid` band has a constant edge and a `rough` one does not, so a rough brush's keep-out is a range.**
Measured off the claims map: a radius-2 `solid` road was 4 cells wide at every one of its 57 columns, while
a radius-8 `rough` brush beside it ran **11 to 18 cells wide** and reached 5 to 10 either side of its
centreline. Four oaks all stated eleven off that centreline came back three placed and one declined, which
is the wander and not a threshold — budget a rough brush from its wide end.

Texture brushes are paths. Budget them like roads: one tongue per feature, radius 3–4, not two at 6–7.

### `DR-STEEP` is a rock's rule and nobody else's, and it complains rather than refusing

`PlaceBoulder` asks it and `PlaceTree` does not, so a face that keeps an oak without a word keeps the
boulder beside it with a note: *"stands at (131, 105) on ground inclined 63°, and the theme painting that
cell calls the ground a face"*. The rock is in the world; the pass has said it looks wrong.

**The angle it compares against is the theme's own cliff band, not a constant.** Measured on one board
whose `meadow` put grass under 35° and coarse dirt to 55°: a 51° face raised nothing at all and a 63° one
raised the complaint. The same rock on the same grade is quiet under a theme whose bands cut higher.

A six-course wall five cells deep has no flat ground on its head at all — every cell of it is an edge, and
a boulder placed there came back at 56°. At eleven cells deep the middle of the head reads 0°.

### A texture path is an exclusion zone as wide as itself

Using the path prop as a brush — a wide `rough` or `worn` band whose `pave` says what a stretch of ground *is*
— is the way to get dedicated ground out of a single theme, and `DR-ROAD` prices it: a tree keeps **three**
blocks from the nearest paved cell and a boulder **two**, measured from the prop's resting cells, so a
radius-10 brush is a 26-wide strip nothing can stand in. A paved forest floor is an empty forest.

Brush the ground that is meant to be open — the fighting ring round a goal, a quarry pan, a trampled heath, a
shore — and leave the wood's floor to the theme and the flora overlay.

### Only `worn` spends `coverage` — `rough` fills its band solid

`StrokeFill` decides a cell's membership in two steps: a half-width the style shapes, and then a per-cell
gate. Only `worn` has that gate — `PatternNoise.Unit(x, z, seed + 11) < coverage`.

`rough` spends its knob on the band's *edge* instead, wandering the half-width by ±45% over a 7-block scale
and filling everything inside it. So `style="rough", coverage=0.26` is a **solid belt**, not a freckle, and
sixteen seam strokes written that way turn every boundary on a board into a stripe of a third material laid
over the join.

**A stroke prop takes five styles and a polyline shape takes three.** The prop's are `solid`, `worn`,
`rough`, `tapered` and `stones` — discs at intervals along the arc with gaps between them, spaced on arc
length so the spacing stays even round a bend, which is the stepping-stone crossing nothing else draws. A
polyline shape's `stroke_edge` is `solid`, `rough` or `tapered`: it is an outline, and an outline cannot
express a gap or a per-cell dice.

**A seam wants two tongues with their bands left whole, and the mixing belongs in the pave rather than in
the brush** (the author's ruling). A `rough` stroke of the shore's material reaching up and a second reaching
down give a zone instead of a line, and where one of them should read as a gradient its pave is a small
`cell` pattern over both grounds' own blocks. The same move is what weathers a road: `worn` takes the band
apart, and a cell pattern mixing the path's stones with the meadow's grass does not.

### A pave is a full terrain material, but a stroke answers only one of its four axes

`PlaceStroke` resolves the pave at `new BucketContext(x, top - 1, z, TerrainBucket.Surface, 0)` — a world
coordinate, the surface bucket, and nothing else. So a `height` stack **works**, and bands the path by
altitude; `depth` and `slope` are handed 0 and always resolve to the stack's first band; and `inward` is
handed `Inset` of **−1**, which `LayeredMaterial.Resolve` answers with the `beyond` material on every cell.

**So a path cannot be banded across its own width by its material — it takes two strokes.** A wide stroke in
the verge's material with a narrow one over it in the path's, on one centerline, is the ring an `inward`
stack cannot give. Nothing reports the failed stack: a board whose road came out entirely in its `beyond`
block looks deliberate.

### A stroke is turned away by `keepClear`, and by a stamped block, and by nothing else

The keep-out mask is about things that *stand* on ground and a stroke stands on nothing, so a road runs
through a spawn's protection and up to a door. What stops it is a shape marked `"keepClear": true` — a
causeway, a town wall, a crop bed, a flight of steps — whose columns it skips exactly, with no margin, so
the way runs to it and resumes beyond it. `DressingPalette.IsStamp` covers the rest for free: bedrock,
obsidian, wool, gold, iron, emerald, chests and stained glass are never a road's to take.

**A bridge needs no marking, because it is not on the layer the stroke names.** A deck with air under it is
one course on a layer of its own, and `PlaceStroke` reads `context.GroundFor(path)` — the surface of the
prop's own layer. So a ground-layer way across a bridged gorge paves the **gorge floor** under the deck and
never touches it, and paving the deck takes a stroke drawn on the bridge's layer. A causeway is the other
thing: ground, solid to the bedrock, and indistinguishable from the bank it joins until it is marked.

**And a deck lands on its banks only if the marks that cut the gorge share their boundary coordinate.** A
ring covers the cells whose centres fall inside it, so a bank band stopping one short of the cut leaves that
cell pinned by neither mark: the relaxation splits the difference into a one-cell ledge halfway down, and
the deck spanning the stated gap ends over air. Stated as abutting bands the walk reads worst step 0 from
bank to deck to bank.

`techniques/painting-with-a-stroke` is the worked card: a strand feathered into a meadow, a serpentine paved
four ways, the same verge with and without a claim, and one bridge crossed twice.

---

## The export

Two gates are heard for the first time at the export, after the whole world is built, and nothing earlier predicts them.

`techniques/objectives-and-clearances` is the worked card: one island with a monument, a core and a wool on
it, and the same board exported again with one fault in it at a time.

### `float` is geometry and `leak` is an attribute, and a goal at float 0 is not a goal

**A goal's base is the standing level plus its `float`.** Over ground topping at y11 a `pillar-3` starts at
y16 at `float` 4 and at y20 at `float` 8; a core's casing sits at y27 over a bank topping at y19 at `float` 6.

**At `float` 0 a destroyable comes out as one obsidian block and a core loses its floor.** The monument's
lower courses are where its chest and the ground already are, and the core reads three lava with a lid and
no casing under them — nowhere for the lava to fall, which is the whole of what a core is. The four and the
six are not clearance; they are what makes the goal completable.

**`leak` changes no block at all.** Exported at 0, 5 and 10 with `float` held, the core's column is
identical; the number is an attribute on the `<core>` element, and the studio writes it only when it is not
PGM's own default of 5. A question about a leak is answered by the map.xml and never by a column.

### `OB17` refuses at 409 and `OB19` warns at 200

**`OB17` names which of its three places the goal hit** — over the void, inside a spawn's protection, inside
a wool room — each in its own words, and it refuses the whole export. Nothing earlier sees it: the board
stores clean and finishes clean.

**`OB19` is a decline rather than a refusal.** A tree, boulder or building inside the ten-block square about
a marker is left out and the world is built anyway, at 200 with a `Pgm-Warnings` header — *a goal is what the
map is for, and a prop is removable*. Measured: a boulder six blocks off the marker is declined, the same
boulder sixteen off is built.

### A placement carrying `"stamp": null` voids the whole intent PUT

The call answers **200** with an empty body and stores nothing — not the placement, not the teams, not
`maxPlayers`. Omit the field rather than stating it null. It is the only call in the studio that reports
success for having done nothing.

### `OB19`'s keep-out is bigger than it sounds, and it is the first thing a prop hits

A **10-block square about the goal's anchor** — 441 cells reaching Chebyshev 10 — tested against a prop's
footprint **plus its eaves**, and against **every orbit image** of it. For a goal at `(0, 45)` the box is
`x −10..10, z 35..55`, and a building drawn at `x −12..−1, z 54..61` is refused on its eave. Measured with a
ladder of oaks round one destroyable: 9 and 10 declined, 11 and 12 placed, so eleven off the anchor is the
first clear ring.

**`Seats` asks `context.AllowsProp` before any other claim, so the clearance answers on the dressing read
rather than at the export.** It arrives as a decline on a 200 — *"rests on (48, 70), inside a goal's
clearance"* — which is early enough to fix and quiet enough to miss. Compute the box, add one for the
overhang, and keep buildings, trees and boulders out of it; `techniques/trees-and-boulders` reads the rule
from the prop's end and `techniques/objectives-and-clearances` from the goal's.

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

Every other read is a projection. Probe the coordinate you already expect something at.

A column through the middle of a house reads floor, air, roof — the walls are at the perimeter. That is a
correct building, not a broken one.

### `walk` is the read that says what ground costs

`traversability` answers whether a board joins up. `walk` answers what crossing it charges, between two
stated cells, in four units at once: whether it can be reached, how far in blocks, how many blocks a player
must **place** — a rise of Δ costing Δ−1, void bridged one a cell — and how many falls over three the way
takes. `aim` picks the route: `travel` the shortest, `reach` the one placing fewest blocks, `comfort` the
least edge-hugging of the routes within ten blocks of the shortest. `render/walk` shades the same field over
the whole board with the route on it.

**Ask it in mirrored pairs.** A single journey says what a journey costs; the same journey against its own
image under the plan's `symmetry` says whether the board is fair, and that is the question no other read
answers.

`render/mirror` compares blocks, and two halves can be block-identical while the ground between them charges
one team eleven blocks the other does not pay.

Measured on a `rot_180` board whose spawn-to-goal lines agree to within one block: the river corridor does
not, with `(−24, −16)` river bed at y5 against `(24, 16)` bank top at y17, which the walk turns into 11
placed blocks for one team and 0 for the other.

The relief mark's own point list is rotationally symmetric; what moves the edge is what is laid over it
unmirrored — the `grain` field and the water props' `shoreWander`.

**The field is one-sided, and the picture does not say so.** `render/walk` measures from one `from`; a cell
shaded cheap is cheap *from there*. Two teams do not share a picture. Read one per spawn before concluding
anything about a board's balance from a colour.

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
