# Taking over a composed board

**A composed board is JSON, and taking one over is editing it.** `GET /api/compose` answers cards, `POST
/api/compose/pin` stores one and hands back an ordinary `PlanModel`, and from there nothing is special about
it. This card is one pinned board edited four ways. Open them in the studio as
`technique-composed-1-as-pinned` through `-4-taken-over`, or run `build.py`.

**Knowing which document an edit belongs to is most of the skill.** A height on a piece, a piece split, a
piece removed, a build zone and a wall are all edits to the **plan**. A void ring redrawn, a coast
chamfered, a theme, a road and a prop are edits to the **layout** the compiler answers with. And one edit —
an add over a hole — should not be made in either.

**What the composer will not tell you is what its arrangement is for.** Its holes, its corridors and its
interfaces are the *shape of the pieces*; no field names them, no gate defends them, and every finding on
this card arrives on a **200**. The author's own ruling is what has to do the work.

## The board

```
{"players": 10, "teams": 2, "symmetry": "rot_180", "cell": 4, "seed": 78,
 "composerVersion": "body-first-2", "schema": 1}
```

That descriptor reproduces `pinned.plan.json` exactly, and it is committed beside this file so the card
reads without a studio. Ten players, a `double-hole` hub and one `l` wool: **thirteen pieces on 80 × 160
blocks**, with two enclosed holes the hub's own shape makes and a neutral mid at the origin.

| variant | the edit | what compiled |
|---|---|---|
| `1-as-pinned` | none | 8 shapes: **2 polygons, 2 subtracts**, one height |
| `2-void-redrawn` | one void ring's corners taken off, in the **layout** | the same 8, and 32 blocks of hole that are now ground |
| `3-a-surface-per-piece` | a `surface` on every piece, in the **plan** | 13 shapes: **7 polygons over 7 heights**, subtracts intact |
| `4-taken-over` | + two pieces split into staircases, a piece replaced by a build zone, a coast chamfered, a bedrock wall, a deck on the mid, two roads, five themes, ten oaks | 17 shapes: **12 polygons over 9 heights**, 1 cut, **4 made layers**, 24 props |

## What a flat plan compiles to

**One merged polygon per component, not one per board.** `1-as-pinned` comes back as `hub-t1-9` — the team
unit's whole footprint as a single 14-vertex outline — and `mid-stone-0-9` for the neutral holm, because the
two never touch. Twelve of the thirteen pieces are inside that one outline and are not addressable
separately.

**And one subtract per enclosed void.** `void-1-cut` and `void-2-cut` are the hub's two slots, as plain
12 × 12 rings. A subtract beats every plain add on its layer whatever order the two are written in, so those
two squares are the board's own statement that there is nothing there.

**The holes can be found before the compile, and the predicate agrees with the compiler here.** A void cell
with land in all four directions within reach is a hole; run over the plan's own cells it names **four
regions of nine cells** — two in the authored half and their two images — and the compiler's two rings are
exactly those two. `holes.txt` has both answers side by side.

## What a hole is worth

**A plain add over a hole draws nothing, and the complaint is the only thing that says so.** Dropping a
12 × 12 rectangle on `void-1-cut` stores at **200** with `SK13`: *"'paved-over' draws nothing over 144
column(s) … because 'void-1-cut' takes them away … The shape is on the canvas and not in the world."* The
document now says something the world does not.

**An override add does fill it, and the complaint is still the only thing that says so.** The same rectangle
with `override: true` also stores at 200, and `SK13` changes its wording rather than its severity: *"fills
144 column(s) that 'void-1-cut' takes away … so the negative space the board states there is ground in the
world."* Nothing refuses it.

**So a hole is defended by nobody, and it is not scenery.** What the composer encircles is ground players go
round, and the walls a board hangs on it are drawn to guard exactly that ground; filling it makes them guard
nothing. That is the author's ruling and not a gate, which is why it is written here.

**Where the void wants to change shape, change the subtract.** `2-void-redrawn` takes four blocks off each
corner of `void-1-cut`'s ring and nothing else. The hole comes out an octagon and **32 of its 144 blocks are
ground**, with the same 32 at its mirror image, and no add was written for any of them.

## What a surface per piece buys

**It ends the merge, which is what makes a composed board paintable.** A theme is stated on a *shape*, and a
flat plan has one shape per component — so `themeByHeight` has nothing to bind to until the heights exist.
Heights first, then paint.

**What it answers is one polygon per height per connected region.** On `3-a-surface-per-piece` each of the
seven heights happens to be one region, so seven polygons come back with plain names. The taken-over board
is where the difference shows: nine heights, twelve polygons, because the treads put 10, 11 and 12 on two
cross-pieces that do not touch — `hub-t1-10` and `hub-t1-10-2` are those two, and `themeById` addresses one
at a time.

**What it does not do is remove the hole.** Both subtracts survive — `PlanVoids` reads the void per
*component* rather than per surface, so the buffer is declared and the cut emitted either way. Measured in
the built world: every hole is 0 of 144 blocks under every variant but the redrawn one.

**And painting by height paints one component in as many themes as it has heights, which the studio remarks
on.** `SK27`, a complaint: *"component 'hub-t1' … compiles to 11 plateaus from surface 9 to 16 and they
state 4 different paints … one landform with a hard line at every riser, where a theme is a place."* A
terraced hub really is eleven plateaus; the cost is a hard line at each riser, and that is the author's to
want.

## Taking it over

**The heights are one decision and it is where the hard cut goes.** The front bar stays at the board's own
9, flat and low; everything behind it is raised to 13. That four-course step is a thing a defender shoots
over and an attacker climbs, and it is what gives the paint a boundary instead of a stripe.
`section-risers.png` is the cut.

**A piece split into treads is how a plan states a staircase.** A plan piece has one height, so a slope is a
run of pieces and nothing else. Each cross-piece between the bars is three cells deep, so cutting it at
every cell gives three one-cell treads at 10, 11 and 12 — four one-block risers between the bars, which
`walk` crosses **end to end with nothing placed**. `the-staircase.png` is the same three pieces cut through.

**A piece replaced by a build zone is the one edit here made for a reason the studio cannot check.** Looking
west out of the spawn the double-hole hub is three bars with a void between each pair, and `hub-t3` is the
far one — 12 × 12 blocks at the end of that view. `4-taken-over` takes it out of `pieces` and declares a
`zones` entry over its rect, which the compiler turns into the intent's own `build.areas`, fanned.

**The reason is the author's and belongs on the card as his.** The board is `rot_180` with one wool a team,
so both sides spawn, turn the same way and run past each other down the far lane. Taking that lane out and
declaring it buildable means an attacker either takes the lane nearer their own spawn or bridges a void gap
under fire, and the two teams meet instead of trading. Two bars could go; one is enough.

**And it changes which voids are holes without changing the ground.** With the far bar gone the void beside
it opens to the sea, so the compiler emits **one** cut instead of two and the merged outline states that
void by tracing round it — 0 of its 144 blocks come out as ground either way. A subtract is wanted where a
void is enclosed; everywhere else the outline already says it.

**A bedrock wall is a feature, and the read that calls it a barrier is the thing to argue with.** A `walls`
entry across the wool approach's own interface stamps four courses of bedrock a defender can build on and
cannot lose, low enough that an attacker bridges it. `walk` answers *"barrier +4 at (−14, 67)"* and reaches
the room past it with three blocks placed; the word is about walking, and reading it as a fault is the
author's account of why so few maps have ever carried one of these walls.

**A coast is as editable as a void, and where the corner goes is a rule.** The back bar's outer corner at
(28, 56) is taken back six blocks, in the layout, the same kind of edit as redrawing a subtract. It is not
on an edge a build zone or the front line attaches to: a diagonal there leaves a bridger a triangle of
ground nobody can build on, so those corners stay square.

**Two roads, and both arrive somewhere.** `spine` leaves the spawn, climbs the spawn's own staircase onto
the back bar, runs its length and climbs the approach to the wool room's doorstep; `sally` drops off it down
the middle staircase to the brink facing the mid, which is this board's front — the seed composed no
frontline piece, so the front is the bridge. Both run down the **middle** of a corridor and never across
one, because a stroke repaints the top block of every column it crosses and a corridor's lip is its rim.

**A structure is four made layers, because a sketch layer is one span per column.** The mid is the one
piece both teams bridge to, and a flat stone island is nothing to arrive at — so it carries a double deck:
four cobble legs, a floor at y11 with three clear under it and a roof at y16 with four clear between. A leg
passing a floor would be two spans in one column, so the legs are cut at each floor instead and each span
gets its own `kind: "made"` layer.

**It is a height nobody is given and anybody can take.** `walk` prices the lower floor at `barrier +4` from
the holm and the roof at `barrier +9`, both built up from ground a player has just bridged to. Its footprint
is odd in both axes about the origin, so it is its own `rot_180` image and needs no mirror — a board whose
middle is one block off-centre is one team's middle.

**Five themes, cut at the risers, and the board stops looking composed.** `census.txt`: `front` 29.1%,
`back` 28.3%, `stair` 17.4%, `approach` 17.4%, `mid` 7.7% over 4,956 ground cells, with the borders between
them counted. `rimEdges: "void"` caps every piece all the way round, because a composed piece stands over
nothing on every side.

**And every one of those themes puts a `teamTint` in its wall bucket, which is the one paint on this board
that reads the map rather than the ground.** A composed board is all rim — every piece stands over void —
so the wall is not a hidden stratum here, it is the course a player sees from the next piece across. The
tint resolves per canonical island and falls back to the theme's own `neutral` where nobody owns the land.

**So one material answers three ways, and `tint.txt` reads all three.** Red's half comes out red stained
clay (103 columns in the sweep), blue's blue (92), and the neutral holm keeps the sandstone its theme
states (77 ground columns, none tinted). `section-tint.png` is the cut where the three sit side by side.

**A board with no void in it never gets the third answer.** `PT5` fires where a tint has one island to
resolve over and the whole map wears one team's colour; this board has three islands because its halves are
joined by build zones rather than by ground. `techniques/theme-buckets` is where the bucket and the rule
are worked, on a board that has no teams to tint for.

## Where a prop may stand is computed; how many stand there is not

**On a board of corridors there is no landscape to judge by eye, so the legal places are searched for.**
Keep a cell whose eight neighbours are all ground at the same height, none of them claimed, three clear of
every paved cell — and require the same of the cell's own `rot_180` image, because a prop is judged at every
image of its orbit. It answers **1,062 cells and 34 spaced sites**.

**Planting all 34 is a forest, and this board is ten-block corridors.** Legality is computed and composition
is not: the search says where a tree *may* go, and which of those places takes one is the author's. Ten are
planted here, twenty with the orbit, and the rules they follow are his.

**A tree goes toward the outside of a piece, never down its middle.** With no road on it a player still runs
down the centre of a corridor, so trees along the rim read as an alley and trees in the middle read as an
obstacle course. Two stand on the front bar's rim in front of each hole; the mid-facing brink stays empty,
because that is the edge the front line is bridged from.

**Nothing stands where a build zone is arrived at.** Three oaks eight blocks off the far lane's north shore
meant a player who crossed the lane landed in them. The pair that stays is on the bar's far side, which is
also the run from the spawn — and a tree on a rim is what puts a crown over the void, which is the one thing
that spoils a walk of the crossing.

**The approach in front of the wall is clear, and the studio keeps it that way.** The wall's own keep-out
plus the road leave **0 legal cells** on the whole approach, and 0 on both staircases and the spawn shelf as
well: a one-cell tread can never hold a prop, because its eight neighbours are at another height by
construction. One tree stands in the corner behind the wall, in front of the room.

**And nothing stands on the mid.** A contested holm is where a structure goes, not scenery; its 106 legal
cells are left to the deck and to the ground under it.

**Three stand along the road, and they are outside what the search offers.** The search keeps a cell whose
eight neighbours are ground at one height, so it refuses every **rim** cell on the board — beyond a rim is
void, and a neighbour that is not ground fails the test. The studio asks something narrower, and the back
bar's outer rim passes all of it: ground under the trunk, three clear of the paving, unclaimed, not kept
clear. `props.txt` has the whole stretch probed a candidate at a time.

**So a site is checked against the dressing pass, and the search only proposes.** Its silence is
conservatism, not a refusal — which matters most where a road has taken everything else: on a bar twelve deep
with a five-wide road down it, three clear of the paving is the rim or nowhere.

**A crown hanging over the void is ordinary, and the map contract says so.** `template.xml`'s
`block-break-void-filter` allows breaking leaves and logs inside the void region and everything outside it,
so tree parts over a board's edge are breakable where the rest of the void is not. What the overhang does
change is a read: the walk offers a standing place in the canopy that `column` and `transect` both call void,
which is `WS71`.

**Every pass of the search that left something out was wrong, and the card keeps the numbers.** Against the
layout alone it answers 1,398 cells and 52 sites, and four of the first twenty are then refused `DR-KEEP`:
the rooms, the doors and the spawns are not in the claims map until the compiled **intent is stored**. With
the intent but without the orbit it answers 1,274 and 45. `props.txt` has all three, and the legal field
broken down by region.

**The search is asked of the board without the props on it.** A tree raises its own column's top and claims
the cells its crown covers, so a list searched over a layout that already carries one is a list about a
different board: the field is 1,062 cells stripped and 748 with seven of them standing.

**And two roads is most of a corridor board gone.** 916 paved cells, each owing a tree three blocks, take
out more ground than every keep-out on the board together — which is the whole reason the notes say to
budget a texture brush like a road.

**Beside them, five placed the way an author places props on a board that looks like a landscape.** On the
road, three blocks off it, over a hole, in the doorway of the wool room, and on the bedrock wall — and
between them they name four rules: `DR-CLAIM`, `DR-ROAD`, `DR-SITE`, and `DR-KEEP` twice with its two
different wordings. `props.txt` is the table.

## The recipe

**Know which document you are editing before you edit it.**

- **the plan** takes a `surface` per piece, a piece split, a piece removed, a `zones` entry, a `walls`
  entry, a shifted rect. Heights first: nothing can be painted until the merge is over.
- **the layout** takes a void ring redrawn, a coast's corner chamfered, a theme on a shape, a relief,
  props. It is the compiler's answer and editing it is ordinary authoring.
- **a staircase is a run of pieces.** One piece is one height, so a climb a player walks is three rects
  where there was one — and a `walk` that reports nothing placed is what says it worked.
- **a bedrock wall is meant to be there.** Four courses a defender builds on and an attacker bridges; the
  `barrier +4` a walk reports is the read being literal about walking, not a fault to route around.
- **never chamfer a corner a build zone or the front line attaches to.** The diagonal leaves a bridger a
  triangle of non-editable ground. Take the corner off the outer coast instead.
- **a road runs along a corridor and arrives somewhere**: the spawn to the wool room, and a branch to the
  front. A road that stops in the middle of a board is a road nobody uses.
- **take a lane out where the arrangement plays badly.** A build zone over a removed piece is the cheapest
  edit that changes how a board is fought over, and it is a gameplay decision — the author's, not a gate's.
- **never an add over a hole.** A plain one draws nothing and an override one fills it; both store at 200,
  and neither is what the arrangement was filtered for. Redraw the subtract instead.
- **store the compiled intent before you search for anything**, search the board without the props on it,
  and search again after anything that moves ground.
- **test every candidate's orbit image**, not just the candidate.
- **a texture brush is a keep-out as wide as itself** — on a board of ten-block pieces there may be nothing
  left to stand on.
- **a possible placement is not a required one.** The search says where a prop may stand; how many stand
  there is the author's. Plant to the outside of a piece, two in front of a hole, three along a road, none
  where a build zone is arrived at, none on the approach in front of a wall, none on a contested middle.
- **state `roomStyles`.** The composed board's spawn and wool room are the studio's built-in bedrock box,
  because a plan states no shell and a finish that states none keeps the default — at 200, with no finding.
  Every board on this card wears the box for the same reason, and none of them is about houses.
- **check a site against the dressing pass, not against your own filter.** A search that wants eight level
  neighbours refuses every rim cell, and a rim is often the only row a road leaves.
- **a structure is one made layer per span.** A leg passing a floor is two spans in one column, so cut the
  leg at each floor and give every span its own layer.

## Limits

**Four maps, not one board.** Every other card puts its variants side by side in one world; these cannot be,
because a compiled composed layout carries `mirror_mode: rot_180` and a group that `mirrors`, so two
variants translated apart would be fanned onto each other. `four-ways.png` is the contact sheet that does
the job a grid does elsewhere.

**A subtract is not the only thing that states a void, and this board shows both.** The far bar's removal
leaves a void the compiler emits no cut for, and the built world has it void anyway: the merged outline
traces round it. So read the outline as well as the cuts — a void needs a subtract only where it is
*enclosed*.

**One of this board's reads has to be argued with, and it is filed.** `walk` calls the stated bedrock wall
a `barrier +4` — right about walking, wrong about a wall that is bridged (`WS69`, with `WS70` for a `beside`
that cannot name it). A second finding is parked on a question rather than a fix: a crown hanging over a rim
is a standing place for the walk and a void column for every other read, which is `WS71`.

## What checks it

- `compiles.txt` — the four compiles as a table, then every shape of `3-a-surface-per-piece` and of
  `4-taken-over` with its height and the theme it paints.
- `holes.txt` — the board's negative space three ways: the predicate over the plan's cells, the compiler's
  own rings, and how many of each hole's 144 blocks carry ground in each of the four built worlds, asked
  with `transect` because a render payload counts a crown over the rim as if it stood on something.
- `findings.txt` — the two `SK13` wordings for a plain add and an override add over the same hole, and the
  `SK27` the painted board raises. All three on a 200.
- `props.txt` — the search's three passes, the legal field broken down by the region an author wants a tree
  in, the seven planted out of it with the reason for each, and the five placed by eye with the rule each
  one hit.
- `columns.txt` — thirteen columns: an oak on the front bar's rim, a road's paving, two treads and the
  front bar under them, the bedrock wall and the ground short of it, the surviving hole and its rim, the far
  lane, the mid under its deck, one of the deck's legs, and a spawn room's floor.
- `walk.txt` — nine walks: the two staircases, both build zones crossed, the approach through the wall, the
  deck's two floors, and the canopy hanging past the back bar's rim.
- `census.txt` — five themes over 4,956 cells, and the borders between them.
- `tint.txt` — the wall bucket over the whole board as a character map, the three counts, and one rim
  column of each owner, each taken from the sweep rather than chosen.
- **every variant is a plan and a finish, and `tools/drive.py` builds each from those two files alone.**
  `4-taken-over`'s finish carries the chamfer as an `editShapes` pair — one vertex moved back along the
  first edge and one inserted on the second — and `2-void-redrawn`'s carries the rounded void ring as eight
  ops, both computed by this card's own `chamfer` and `rounded` helpers rather than written out. The checks
  are the numbers already committed here: the census answering 4,956 cells, and hole-1 answering 32/144.
- `pinned.plan.json` is the one plan here with **no** finish beside it, which is what marks it as the
  composer's raw answer rather than a board. `tools/seed-studio.py` reads exactly that distinction.
- `pinned.plan.json` — the composer's own answer, committed. `1-as-pinned.plan.json`,
  `3-a-surface-per-piece.plan.json`, `4-taken-over.plan.json` and `4-taken-over.finish.json` are what
  `build.py` writes from it.

Renders: `1-as-pinned.png`, `2-void-redrawn.png`, `3-a-surface-per-piece.png`, `4-taken-over.png` and
`four-ways.png`, the four together; `section-tint.png` — the same cut carried the length of the board,
where blue's tinted pieces, the sandstone holm and red's sit in one picture;
`section-risers.png` — the board cut at x−6..−2, where the mid, the front
bar, the treads and the back bar each stand at their own height; `the-staircase.png`, the three treads cut
through off the road, 13 down to 9; and `the-mid-deck.png`, the holm's double deck on its four legs.
