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
| `4-taken-over` | + two pieces split into staircases, a piece replaced by a build zone, a coast chamfered, a bedrock wall, two roads, five themes, thirty-four oaks | 17 shapes: **12 polygons over 9 heights**, 1 cut, 72 props |

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
over and an attacker climbs, and it is what gives the paint a boundary instead of a stripe — `section-risers.png`
is the cut.

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

**Five themes, cut at the risers, and the board stops looking composed.** `census.txt`: `front` 29.1%,
`back` 28.3%, `stair` 17.4%, `approach` 17.4%, `mid` 7.7% over 4,956 ground cells, with the borders between
them counted. `rimEdges: "void"` caps every piece all the way round, because a composed piece stands over
nothing on every side.

## Where a prop may stand is computed, and the search is only as good as what it searched

**On a board of corridors there is no landscape to judge by eye, so the sites are searched for.** Keep a
cell whose eight neighbours are all ground at the same height, none of them claimed, three clear of every
paved cell — and require the same of the cell's own `rot_180` image, because a prop is judged at every image
of its orbit. It answers **1,150 cells and 34 sites**, and all 34 take an oak.

**Every pass that left something out was wrong, and the card keeps the numbers.** Against the layout alone
it answers 1,494 cells and 52 sites, and four of the first twenty are then refused `DR-KEEP`: the rooms, the
doors and the spawns are not in the claims map until the compiled **intent is stored**. With the intent but
without the orbit it answers 1,370 and 45. The orbit pass refuses nothing here and is still not optional.

**The search is asked of the board without the props on it.** A tree raises its own column's top and claims
the cells its crown covers, so a list searched over a layout that already carries one is a list about a
different board — which on this board cuts the field from 1,150 cells to 222.

**It is also re-run after every edit that moves ground.** Every reshaping on this card invalidated the list
before it; a list carried over from one of them left sites the pass then refused. A site is an answer about
a board, not about a plan.

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

## Limits

**Four maps, not one board.** Every other card puts its variants side by side in one world; these cannot be,
because a compiled composed layout carries `mirror_mode: rot_180` and a group that `mirrors`, so two
variants translated apart would be fanned onto each other. `four-ways.png` is the contact sheet that does
the job a grid does elsewhere.

**A subtract is not the only thing that states a void, and this board shows both.** The far bar's removal
leaves a void the compiler emits no cut for, and the built world has it void anyway: the merged outline
traces round it. So read the outline as well as the cuts — a void needs a subtract only where it is
*enclosed*.

**Two of this board's reads have to be argued with, and both are filed.** `walk` calls the stated bedrock
wall a `barrier +4` (`WS69`, and `WS70` for a `beside` that cannot name it), and a crown leaning over the
far lane makes a crossing of that build zone read as a climb of seven blocks where the same crossing from
the front bar is level (`WS71`). `walk.txt` carries both, with the coordinates.

## What checks it

- `compiles.txt` — the four compiles as a table, then every shape of `3-a-surface-per-piece` and of
  `4-taken-over` with its height and the theme it paints.
- `holes.txt` — the board's negative space three ways: the predicate over the plan's cells, the compiler's
  own rings, and how many of each hole's 144 blocks carry ground in each of the four built worlds, asked
  with `transect` because a render payload counts a crown over the rim as if it stood on something.
- `findings.txt` — the two `SK13` wordings for a plain add and an override add over the same hole, and the
  `SK27` the painted board raises. All three on a 200.
- `props.txt` — the search's three passes, the thirty-four sites the last one returned, and the five placed
  by eye with the rule each one hit.
- `columns.txt` — twelve columns: an oak the search sited, a road's paving, two treads and the front bar
  under them, the bedrock wall and the ground short of it, the surviving hole and its rim, the far lane, the
  mid, and a spawn room's floor.
- `walk.txt` — five walks: the two staircases, the build zone crossed from either side, and the approach
  through the wall.
- `census.txt` — five themes over 4,956 cells, and the borders between them.
- `pinned.plan.json` — the composer's own answer, committed. `1-as-pinned.plan.json`,
  `3-a-surface-per-piece.plan.json`, `4-taken-over.plan.json` and `4-taken-over.finish.json` are what
  `build.py` writes from it.

Renders: `1-as-pinned.png`, `2-void-redrawn.png`, `3-a-surface-per-piece.png`, `4-taken-over.png` and
`four-ways.png`, the four together; `section-risers.png` — the board cut along x−2, where the mid, the front
bar, the treads and the back bar each stand at their own height; and `the-staircase.png`, the three treads
cut through off the road, 13 down to 9.
