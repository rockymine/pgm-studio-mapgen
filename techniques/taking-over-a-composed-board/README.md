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
| `2-void-redrawn` | one void ring's corners taken off, in the **layout** | the same 8, and 32 blocks of new ground |
| `3-a-surface-per-piece` | a `surface` on every piece, in the **plan** | 16 shapes: **10 polygons over 6 heights**, subtracts intact |
| `4-taken-over` | + a piece removed for a build zone, a piece split, a coast chamfered, a gated barrier, two roads, a theme a height, fifteen oaks | 17 shapes, 6 themes, **1** cut left, 34 props |

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
corner of `void-1-cut`'s ring and nothing else. The hole comes out an octagon, the board gains **32 blocks**
of ground it now states, and no add was written: 5,436 land cells against `1-as-pinned`'s 5,372.

## What a surface per piece buys

**It ends the merge, which is what makes a composed board paintable.** A theme is stated on a *shape*, and a
flat plan has one shape per component — so `themeByHeight` has nothing to bind to until the heights exist.
Heights first, then paint.

**What it answers is one polygon per height per connected region, not one per height.**
`3-a-surface-per-piece` gives thirteen pieces at six heights as **eleven** polygons: `hub-t1-9`,
`hub-t1-9-2`, `hub-t1-10`, `hub-t1-10-2`, `hub-t1-10-3` and so on. The suffix is where one height fuses into
several, and `themeById` is what addresses them one at a time.

**What it does not do is remove the hole.** Both subtracts survive — `PlanVoids` reads the void per
*component* rather than per surface, so the buffer is declared and the cut emitted either way. Measured in
the built world: both holes are 0 of 144 blocks under every variant but the redrawn one.

**And painting by height paints one component in as many themes as it has heights, which the studio remarks
on.** `SK27`, a complaint: *"component 'hub-t1-east' … compiles to 10 plateaus from surface 9 to 13 and they
state 5 different paints … one landform with a hard line at every riser, where a theme is a place."* A
terraced hub really is ten plateaus; the cost is a hard line at each riser, and that is the author's to want.

## Taking it over

**A piece replaced by a build zone is the one edit here made for a reason the studio cannot check.** Looking
west out of the spawn the double-hole hub is three bars with a void between each pair, and `hub-t3` is the
far one — 12 × 12 blocks at the end of that view. `4-taken-over` takes it out of `pieces` and declares a
`zones` entry over its rect; the compiler turns that into the intent's own
`build.areas: [{-32,32 .. -20,44}, …]`, fanned.

**The reason is the author's and belongs on the card as his.** The board is `rot_180` with one wool a team,
so both sides spawn, turn the same way and run past each other down the far lane. Taking that lane out and
declaring it buildable means an attacker either takes the lane nearer their own spawn or bridges a void gap
under fire, and the two teams meet instead of trading. Two bars could go; one is enough.

**And it changes which voids are holes.** With the far bar gone that void opens to the sea, so the compiler
emits **one** cut instead of two and the merged outline traces round what is left — 13 of the old hole's 144
blocks come out as ground. `holes.txt` has all four variants side by side.

**A piece split in three gives the wool approach its own mouth.** `hub-t1` runs nine cells and the approach
leaves it from the middle three; cut there and the mouth can step up to 10 to meet the climb instead of the
whole bar having to. The split is a plan edit and costs nothing but three rects where there was one.

**A barrier belongs on the approach and not in the hub, and a `walls` entry will not do it.** The approach
is an L of three pieces in a line, so every interface in it *is* the route: a `walls` entry stamped across
the middle of it stood four courses over the ground either side with no way through, and `walk` answered
*"barrier +4 at (−9, 67)"* with the wool unreachable. A `walls` entry closes an interface; it has no gate.

**So the barrier is drawn instead, in the layout, with six blocks of gate on the road's line.** Two override
adds either side, both `keepClear` so the dressing pass sees them and both `height_mode: "level"` with
`skirt: 0` so the relief leaves their tops alone. `walk` up the road reads **walked end to end, 0 placed**;
four blocks east of it reads **barrier +4**. `walk.txt` is both.

**A coast is as editable as a void, and the vertices are in the layout.** The bar facing the mid compiled as
a plain rectangle, so `4-taken-over` takes six blocks off each of its two outer corners — the same kind of
edit as redrawing a subtract, on an add instead.

**Two roads, and both arrive somewhere.** `spine` leaves the spawn, turns down the hub's far bar, climbs the
approach through the gate and ends on the wool room's own doorstep; `sally` drops off it through the middle
cross-piece to the brink facing the mid, which is this board's front — the seed composed no frontline piece,
so the front is the bridge. Both run down the **middle** of a corridor and never across one, because a
stroke repaints the top block of every column it crosses and a corridor's lip is its rim.

**Six themes, one a height, and the board stops looking composed.** `census.txt`: `ring` 51.2%, `arm` 17.6%,
`inner` 11.2%, `keep` 8.3%, `mid` 7.8%, `camp` 3.9% over 4,920 ground cells, with the borders between them
counted. `rimEdges: "void"` caps every piece all the way round, because a composed piece stands over nothing
on every side.

## Where a prop may stand is computed, and the search is only as good as what it searched

**On a board of corridors there is no landscape to judge by eye, so the sites are searched for.** Keep a
cell whose eight neighbours are all ground at the same height, none of them claimed, three clear of every
paved cell — and require the same of the cell's own `rot_180` image, because a prop is judged at every image
of its orbit.

**Every pass that left something out was wrong, and the card keeps the numbers.** Against the layout alone
it answered **512** cells: the rooms, the doors and the spawns are not in the claims map until the compiled
**intent is stored**. With the intent but without the orbit it answered **404**, and a tree landed two
blocks from another tree's image. With both it answered **272**, fifteen once an oak's crown is spaced for,
and all fifteen sites took a tree.

**It is also re-run after every edit that moves ground.** An earlier list on this card was searched before
the far lane came out and the roads were redrawn, and six of its twenty sites were then refused. A site is
an answer about a board, not about a plan.

**And two roads is most of a corridor board gone.** 886 paved cells on 5,145 of land, each owing a tree
three blocks, leaves 272 — which is the whole reason the notes say to budget a texture brush like a road.

**Beside them, five placed the way an author places props on a board that looks like a landscape.** On the
road, three blocks off it, over a hole, in the doorway of the wool room, and on one jamb of the gate — and
between them they name four rules: `DR-CLAIM`, `DR-ROAD`, `DR-SITE`, and `DR-KEEP` twice with its two
different wordings. `props.txt` is the table.

## The recipe

**Know which document you are editing before you edit it.**

- **the plan** takes a `surface` per piece, a piece split, a piece removed, a `zones` entry, a `walls`
  entry, a shifted rect. Heights first: nothing can be painted until the merge is over.
- **the layout** takes a void ring redrawn, a coast's corner chamfered, a barrier with a gate in it, a
  theme on a shape, a relief, props. It is the compiler's answer and editing it is ordinary authoring.
- **a barrier you have to pass is drawn, not stated.** A `walls` entry closes an interface and has no gate,
  so on an approach that is one corridor it closes the route as well — `walk` is what says so.
- **a road runs along a corridor and arrives somewhere**: the spawn to the wool room, and a branch to the
  front. A road that stops in the middle of a board is a road nobody uses.
- **take a lane out where the arrangement plays badly.** A build zone over a removed piece is the cheapest
  edit that changes how a board is fought over, and it is a gameplay decision — the author's, not a gate's.
- **never an add over a hole.** A plain one draws nothing and an override one fills it; both store at 200,
  and neither is what the arrangement was filtered for. Redraw the subtract instead.
- **store the compiled intent before you search for anything**, and search again after anything that moves
  ground. The rooms, doors and spawns are keep-outs that do not exist until the intent is there.
- **test every candidate's orbit image**, not just the candidate.
- **a road goes along a corridor**, and a texture brush is a keep-out as wide as itself — on a board of
  ten-block pieces there may be nothing left to stand on.

## Limits

**Four maps, not one board.** Every other card puts its variants side by side in one world; these cannot be,
because a compiled composed layout carries `mirror_mode: rot_180` and a group that `mirrors`, so two
variants translated apart would be fanned onto each other. `four-ways.png` is the contact sheet that does
the job a grid does elsewhere.

**The predicate and the compiler agree on this board and do not always.** On a micro board probed while
writing this — 16 players, seed 72, a `ring` hub and a `donut` wool — the predicate named a twelve-cell
region the compiler emitted no cut for, and the built world had it void anyway: the merged outline simply
traced around it. A void needs a subtract only where it is *enclosed*, so read the outline as well as the
cuts.

## What checks it

- `compiles.txt` — the four compiles as a table, and every shape of `3-a-surface-per-piece` with its height.
- `holes.txt` — the board's negative space three ways: the predicate over the plan's cells, the compiler's
  own rings, and how many of each hole's 144 blocks came out as ground in each of the four built worlds.
- `findings.txt` — the two `SK13` wordings for a plain add and an override add over the same hole, and the
  `SK27` the painted board raises. All three on a 200.
- `props.txt` — the search's three passes, the twenty sites the last one returned, and the five placed by
  eye with the rule each one hit.
- `columns.txt` — eight columns: an oak the search sited, the spine's paving, a cell inside the surviving
  hole, the hole's rim, the mid with the bedrock observer platform over it, the gate and a jamb beside it,
  and a spawn room's floor.
- `walk.txt` — the approach walked three ways: through the gate (end to end, nothing placed), four blocks
  east of it (barrier +4), and the whole way from the spawn.
- `census.txt` — six themes over 4,920 cells, and the borders between them.
- `pinned.plan.json` — the composer's own answer, committed. `1-as-pinned.plan.json`,
  `3-a-surface-per-piece.plan.json`, `4-taken-over.plan.json` and `4-taken-over.finish.json` are what
  `build.py` writes from it.

Renders: `1-as-pinned.png`, `2-void-redrawn.png`, `3-a-surface-per-piece.png`, `4-taken-over.png` and
`four-ways.png`, the four together; `section-risers.png` — the board cut along x0, where the wool rooms,
the hub's bars and the mid each stand at their own height, which is the only view a riser reads in; and
`approach-and-gate.png`, the barrier cut through at z66–69 with its six blocks of gate.
