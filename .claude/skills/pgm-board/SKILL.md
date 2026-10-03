--- name: pgm-board description: Author, revise or read a PGM map in this repository through the pgm-studio
API — a destroy/capture/core board, a spec under specs/, a world under maps/. Use whenever the task is to
build a map, change one, diagnose one that built wrong, or read an existing PGM world. Carries the
read-before-you-believe procedure and the lookup table from question to the read that answers it, distilled
from 27 Opus 5 runs. ---

# Authoring a board here

`ORDER-OF-WORK.md` is the order a board is decided in, `WHAT-A-BOARD-IS-MADE-OF.md` is how one should look,
and `AUTHORING-BRIEF.md` is the run it is authored in. This is how not to lose a build finding out.

Everything below is measured off the run reports in `reports/opus5-*.md`. Each rule cost at least one
build, most of them more than one, and several were paid twice by different runs.

**Read the budget before the table.** This repository is larger than any context window: the documents
the brief points at are ~241k tokens, every text render of one board is 30–57k, and two `*.layout.json`
files exceed 200k each. `pgm-board-warmup` carries the limits and the never-open list. A layout is queried
with `jq` and never `cat`-ed, and a one-line verdict is a `grep` rather than a file read.

**And a board's spec is not opened to learn how a board is made** — `techniques/` is where a technique
is read, one instrument to a card, citing no past map. `specs/` answers what a past board did, which is a
different question; `pgm-board-warmup` carries the rule and what it costs to break.

---

## 1. The lookup table — the question, and the read that already answers it

**Reach for a row before you write anything that computes an answer.** The single most-repeated
sentence in the reports is a variant of *"the instrument I should have used exists and I did not know
about it."*

| The question | The read | Not |
|---|---|---|
| **What did the author say here?** | `GET /notes?status=open` across every map, or `GET /map/{slug}/notes` — each note's `anchor` is the place: a point's `hit` and `ground`, an area's `columns` as `[x, y, z]` and, where it was drawn over the void, `overVoid` — the empty cells it covers, at the level of the ground beside them — and the exact `camera`, which `render/eye?eye=x,y,z&yaw=&pitch=&fov=` draws again | a remark in chat turned into coordinates of your own choosing, which is the place guessed |
| What is actually at this coordinate? | `GET /map/{slug}/column?at=x,z` | any render — every other read is a projection |
| Does this climb? Is that step walkable? | `GET …/transect?points=x,z;x,z&beside=2&format=text`, or the report's `slopes` | eyeballing a heightmap shade |
| Does this **flight** actually walk? | the same transect across the crossing — rises, falls, worst step, walked end to end | `EL1` or `WL11`, which walk the pieces flat and cannot see an authored flight at all |
| Is the shape I authored in the world at all? | `GET …/column?at=x,z` at a cell it should own | the store's 200 and pre-flight's OPEN, neither of which looks |
| Did that structure land on **every** team's ground? | `GET …/column?at=x,z` at the exact image — the reflection of block `z` is **`−z−1`**, and a made layer is built once unless its group says `mirrors` | pre-flight, whose mirror check reads spawns, wool rooms and build zones and never made geometry |
| Where does the ground step, over the whole board? | the report's `slopes` (`slopes?format=text`) — `. walked · : scramble · # barrier`, plus a per-face summary | — |
| How high is the ground along this line? | `tools/loop.py --profile x=<x>,z=<a>..<b>,step=1` | your own arithmetic over the anchors |
| How **steep** is the ground, and where? | `GET …/incline?format=text` — the glyph is the tens of degrees, and under the grid, how much ground stands in each ten | the report's `slopes`, which answers a *step* (can it be walked) and not an *angle* (how should it be finished) |
| Is there anywhere to **stand**? | `POST …/sketch/relief/read` → `level` (share under 10°) and `largestField`; `RL5` fires under 30% | the walk tier, which answers one place and no ledge for a board that is one long ramp |
| Which two **marks** built that wall? | `POST …/sketch/relief/read` → `seams`, worst first, each naming the pair and the cell; `RL3` fires above a scramble | a face in the report's `slopes` or the relief read, which report the wall as terrain and attribute it to nothing |
| What does a column hold, layer by layer? | `tools/loop.py --column x,z` | reading a world file yourself |
| **Where may a prop stand at all?** | `POST …/sketch/seats?kind=tree\|boulder\|house[&width=&depth=]&format=text` — **the stored layout goes in the body** — a raster marking every cell a footprint's *minimum corner* may sit on, and a `refused` list of rule → cells, largest first | placing one by eye. Three runs declined 5–7 props a pass that way and 0 once every position came off this mask |
| May *this* prop stand *here*? | the report's `claims` (`POST …/sketch/dressing?format=text`), then `tools/loop.py --candidates <propId> x,z …` | placing it and reading the decline |
| What did the route actually cost? | `GET …/walk?from=&to=&aim=&format=text`, or the report's `route spawn-N to <goal>` | assuming the shortest line is the route |
| …and on a **stacked** board? | the same read, with **`from=x,z,y`** — the `y` picks which storey of the column is meant | `x,z` alone, which walks to the column *under* an elevated goal and calls it walked end to end |
| Is a lower storey still made of what I painted it? | `GET …/column?at=x,z` | the isometric, the census, or the 200 — none of the three sees it |
| Is the board joined up, per team? | `GET …/preflight` | the export, at 409, after a whole world is built |
| Is any ground unused — is it ground anybody **goes** to? | `GET …/coverage` (after) — reached / decorated / dead, with the five largest dead patches and their coordinates · `GET …/plan/flow` (before) | nothing — no gate asks this, and `preflight` asks only whether ground can be *reached* |
| What is the board made of, and what borders what? | the report's `themes` (`themes/census?format=text`) | counting your own theme dict |
| Does the finish **look** right where a player stands — do two blocks merge into one ground or into static? | `GET …/render/eye?look=x,z` — the board from a player's eye in the game's own block textures, framed on a thing the document places (a spawn, a goal, a boulder, a house); `from=x,z` stands the eye by hand; `?format=text` names the camera and what fills the frame | `render/surface`, a theme preview or the isometric, which all draw a block as one colour — two noisy blocks of one colour are calm grey there and static in the game |
| What is the plan's shape, before a map row exists? | `tools/board.py specs/<slug>/<slug>.plan.json` | a render of a built world |
| Is this section of the world what I think? | `GET …/render/section?axis=&at=&from=&to=&format=text` — **`axis` names the direction the cut runs, so `at` is the other coordinate** | a PNG section, which blends renderer gridlines over it |
| What fields does this pattern take? | `GET /api/terrain/patterns` — fourteen kinds with exact field names | guessing. One run invented **five field names out of five** |
| What does this refusal mean? | `GET /api/rules?rule=<id>` | inferring from the sentence |
| Is there a **number** for this, and what is the band? | `GET /api/rules/terms` — every evaluator term with its rule, its band and where the band came from | reading the rule prose, which states the mechanism and not the envelope |
| What does the house style build? | `POST /room-styles/preview-snapshot?format=png&view=section` (and `plan`; other views 400) | a top-down — every shipped roof fault was visible in a section and invisible from above |
| What does a whole multi-wing house build? | `POST /terrain/prop-preview` — the prop plus a theme | `preview-snapshot`, which draws a default box |
| How do I reshape a compiled outline? | `PATCH …/sketch/shapes/{id}/vertices/{index}` moves **one** point; `POST …/vertices {"after": n}` adds one at that edge's midpoint; `DELETE …/vertices/{index}`. A spec states them as `editShapes`, replayed before any bend | a second shape added on top to enlarge it, a subtract to eat into it, or a bend to move one corner |
| How do I make a whole edge read rougher? | `POST …/sketch/shapes/{id}/bend` with `side: out\|in\|both` (`out` is the default and is the bloat that reads as land) | restating the whole `vertices` array, which is a second copy of the coast |
| How do I build a facility, a landmark or any made structure that reads as **one thing**? | `techniques/designing-a-structure` — a module, one mass a layer, a façade as a `wallRun` of a `height`-axis stack, a door as a sill plus a lintel on a lintels layer | one shape per window, masses fused on one layer, or an override floored at a door's head — all three store at 200 and are wrong in `column` |
| How do I get a flowing wall, lane or watercourse? | a `polyline` **shape** — the rasterizer splines its points (centripetal Catmull-Rom, 8 samples a segment) before offsetting the band, so 4 clicked points draw as a curve. `stroke_edge`: `solid` \| `rough` \| `tapered` | a chain of rectangles, or hand-authored `controls` |

**A world that is not a stored map** — a community map, a hand-finished world, anything with a
`map.xml` the studio did not write — is the one case none of the above reaches. `import-folder`
takes an **xml-less** folder under a configured `MapsRoots` only. Use `tools/anvil.py`, `probe.py`,
`trees.py`, `lift.py`, `world-diff.py`; they read Anvil in the standard library alone.

---

## 2. The three moments

A rule in a document does not fire. These are the three places to stop, and they are cheap.

**Before the first change, read the open notes.** The author leaves feedback as notes pinned to the board
in the Sketch tool's In game phase, and a revision starts from `GET /notes?status=open`. A note tagged `look`,
`terrain` or `gameplay` is work on that map; `studio` is a backlog task for the studio instead; `ruling` is a
gameplay decision for every map. An untagged note is read for what it is about, and the reply says which.

**Beside the notes, read what changed since your last run.** `GET /map/{slug}/changes?since=<the change your
last run landed as>&format=text` lists every change made to the board since, and `GET …/diff?from=&to=&format=text`
what each did. A hand edit there is the author showing what the board should be, and the next run over it is
refused `409` with the edit written as the refinement would state it (`SR1`). Take it into `build-spec.py` and
drive with `--after <change>`; drop one with `--discard <change>` only where the author said it goes.

**After `--dry`, before the first build.** Run `tools/board.py` on the plan and read the grid. A plan
is a list of rectangles and most of what goes wrong with one is a *relation between two of them*;
no render of a built world can show that, because by then they are terrain.

**After every drive, before you open a single picture.** The drive prints the three numbers the report opens
on; say them out loud:

```
ground   N walked, N scrambled, N barrier — N% steps further than a player walks
props    N placed, N declined      (and in `claims`: is the goal's clearance block empty?)
routes   worst step N, on route spawn-N to <goal>
```

Then look at the pictures the report names. The order is not taste: **a picture answers whether a thing came
out, a number answers whether it is right.** A one-block bump under a rail is one shade in a heightmap and
nothing at all in an isometric — the report's `slopes` names it with its coordinates, and it shipped in five
consecutive builds of one board because nobody opened the slope grid.

**After a drive, reply on every note it answered.** The reply names what changed, the change it landed as
and the number that moved ("dead share in this area 41% → 6%"). The studio draws the note's camera over the
board as stored and attaches it as the after picture whenever an answer on a picture note is written at the
latest change, so post the reply after the drive's last store and do not draw it yourself. The thread then
waits on the author, who resolves it; an agent never does.

**Where a note could mean two places or two things, the reply is the question.** Post it with
`"status": "needs-info"` and build nothing on a guess; a note declined is `"status": "wont-do"` with the reason
in the body. `pgm-studio/docs/tools/sketch.md`, *Answering the notes an author left*, has every route.

---

## 3. What you may write, and what you may not

**Write a `build-spec.py`.** A spec's plan and refinement are large structured documents with arithmetic in
them — bay grids, per-course stairs, voxel models, ramp anchors. Generating them from a script *is* the
authoring work, it is what every run here has done, and it is what makes a board re-buildable. Keep it
in `specs/<slug>/` beside the documents it writes.

**Do not write anything that reads the built world.** No ground-finder, no section renderer, no walk
checker, no clearance test, no site filter. Every one of those exists, and the home-made version has
been wrong every time it has been tried here:

> *"Then I wrote three ground-finders and two of them were wrong. 'The topmost solid block' reads a
> roof."* — `opus5-run6-7`
> *"I measured a stair every two blocks and called it walkable."* — `opus5-run6-7`
> *"I believed a 200 for two rounds. My scratch loop posted the layout with `PUT …/sketch/from-plan`"*
> — `opus5-elderwold` (a home-made driver silently lost every edit)

**The run rules say "no capability is added in `tools/`", and that wording has a hole in it.**
`opus5-lindenkreuz` complied with it exactly — nothing was added to `tools/` — while writing a section
renderer, a surface census and a column probe in a scratch directory instead. The rule is about
**second copies of the system**, wherever they live.

The one legitimate exception is §1's last row: a world that is not a stored map.

---

## 4. The failures that have each cost more than one run

### A picture that looks plausible is not a read

`opus5-thunder-series` reconstructed three boards from top-down renders and had to redo them.
`opus5-tarnfell` read `world-material.png`, saw sand, and concluded the lake was missing — the material
top-down draws the top **solid** block, so water reads as its own bed. `opus5-undercroft` read a transect
through a filter capped at y22 and concluded a causeway was six blocks low.

> *"`GET /api/map/{slug}/column` is the read that settled every disagreement."* — `opus5-interchange`

**When two reads disagree, `column` is the one that is not a projection.**

### Assumed instead of measured

> *"I drew a stair for a fall I had assumed rather than measured."*
> *"I assumed the river's 8-block drop was the same on both banks. It is not."* — `opus5-liminal-dtm-ii`
> *"I assumed water spreads to fill a level pan."* — `opus5-rimegarth` (a fluid fills its own band; the
> pan is the size of the pool)
> *"I read `maxPlayers` as the board's cap and shipped a 48 v 48 map."* — `opus5-liminal-dtm-ii`

The tell is always the same: a number you derived yourself, used as if it had been read back. If you
computed it, **transect the thing you computed** before building on it.

### A spec in this repository is dated evidence, not the current contract

`opus5-lindenkreuz` copied `"plan": 1` and the marker offsets in cells from the specs it read first, and
the compile refused: *version 2 states marker offsets in blocks from the piece corner.* Two spec
documents in `specs/` disagree with the API by exactly one cell size.

The same applied to `GENERATION-NOTES.md`, where nine entries described a fault the studio had since fixed.
It now carries no task id at all, which is the discipline that keeps it from happening again.

**Order of authority: the API's own answer › the schema in `openapi.json` › the notes › a committed
spec.** Read source only where two of those disagree, and then read the narrowest thing that settles it.

### "Missing from the system" is a claim about the surface until you check

`opus5-run2` had to correct two earlier reports: *"per-shape themed materials — missing from the
system"* — **false**; *"relief marks with area scope — missing"* — **false**. `opus5-run8` shipped a
wrong explanation of `SK11` and filed a wrong bug against the 3-D preview that the author caught.

Before writing that something is missing, look for it in `GET /api/openapi/v1.json` and say what you
found.

**missing** (no mechanism) · **unreachable** (exists, the surface hid it) · **mistaken** (exists,
documented, not found) are three different verdicts and only the first is a capability gap.

**Search the surface by what a thing would *do*, not by what you would call it.** `mistaken` is the usual
verdict because the surface is indexed by name and a capability is wanted by function, so one grep of the
obvious word answers nothing and reads as proof. Two gaps filed in one run, both wrong, neither caught by a
read:

- *Ground cover* — ferns, grass and flowers scattered over grass — was written up as absent. It is
  `FloraProp`, carrying a `FloraSpec` of `points`, `coverage`, `scale`, `octaves`, `fernShare`,
  `flowerShare`, `flowerScale` and `tallShare`, every one of them in `openapi.json`. The word **flora** was
  never searched, because the question had been phrased as *grass coverage*.
- The *intra-team build zone* was written up as something the composer does not model. It is on the wire
  three times over. `CT4` names it in a clause rather than in its summary — *"a stone whose every
  interfacing zone component touches only one team's islands is a **team transient-link**, not a mid stone —
  the encased pad between a team's own islands"*, with `rotate-wide-frontline`'s four 100-block corner pads
  cited; `BZ5` carries the same motif at the spawn as the **defender-egress bridge**; and it is *measured*,
  as the `team-stepping-count` term under `CT4`, band **[0, 2]**. Not one of the three contains the word
  **zone**, and the grep was for *zone*.

So run **three** searches before writing the word missing: the name you would give it, the sentence
describing what it would do to a board, and the term catalogue. `GET /api/rules` returns every rule with its
prose in one fetch and is greppable, `GET /api/rules/terms` is the second index and answers what is
*measured* rather than what is stated, and `openapi.json` is greppable for a field name.

Search a rule's prose and not only its summary: `CT4`'s summary is an island-size gradient and the sentence
wanted is six clauses in.

A gap filed against a surface that has the feature is worse than no gap — it is a capability the
next run also will not use, and nothing will ever contradict it.

### The plan tier cannot see what you authored downstream, in both directions

`EL1` and `WL11` walk the plan's pieces **flat**. A five-course seam with a flight cut into it reads to them
as a five-course seam, and the finding is right about the plan and says nothing about the board. The answer is
a transect, not a redesign: two boards of a recent run ship with standing `EL1` complaints whose crossings
measure `worst step 1, 0 barrier, 0 scramble, walked end to end`.

It runs the other way too, and that half is worse: **the plan tier passing says nothing about whether the
shape is in the world.** A piece the rasterizer discarded for a taller neighbour, a ring a vertex insert
folded, a room-style key the snapshot dropped — all three stored at 200 and pre-flighted **OPEN**. What sees
them is `column` and `transect`. Nothing else does.

### Coverage is the cheapest read on the board and the one nobody takes

Nothing refuses on it, which is exactly why it goes unrun. It is the only read that asks whether any journey
**goes** somewhere rather than whether it **can**.

Measured on one board across one edit: a destroy board with its monument on the centre line read **62.0%
dead** — four patches of about 2 000 cells each, every one of them one block from used ground. One objective
and one spawn a side make two journeys, and the flanks are on neither. Moving the monument twelve blocks off
the centre line and taking ten blocks off the board's width took it to **17.9%** with nothing else changed. A
board with two objectives a side and a spawn between them reads **0.0%** by construction.

### The plan was cut up so a theme would have somewhere to hang

A plan states the board's **arrangement** — which ground is where, at what height, next to what. It is not
the board's shape, and adding pieces to get a shape is the failure. `firnline` is the worked example:
**13 plan pieces at 6 surface heights**, then `themeByHeight` mapping each height to a theme, so the theme
partition is the piece partition and the board's look was decided by how it happened to be cut up. It reads
chopped rather than coherent, and no amount of dressing repairs it.

The same board is **one terrain shape plus two platforms**: author the ground the map is played on as one
shape (or as few as the arrangement genuinely needs), reshape it per vertex until it reads as ground, then
put the monument shelf and the middle plateau on `addLayers` slabs over it, each with its own `base_y` and
its own theme. A piece earns its place by stating something the arrangement needs — a height a lane climbs, a
room a building is seated in, a footprint the symmetry fans. A piece that exists only so a theme can be hung
on it should have been a shape scope.

**Construction comes before dressing, and a bad construction cannot be dressed out of.**

### The ground was finished by its height instead of its angle

A board painted one material per plan piece, or one per height band, comes out a flat sheet from above however
much relief is under it: the quarry, the graded terrace and the cut banks are all in the picture and none of
them is visible. Nothing in the geometry tells a 45° hillside from a meadow — such a surface has no exposed
riser, so the `wall` bucket never sees it and every other band axis paints the two alike.

**Give the ground theme's surface a `layered` material on the `slope` axis.** A thickness on that axis is a
span of **degrees**, so one stack finishes the flat, the shoulder and the face of the same hill, and each band
takes a depth stack of its own so grass stays one course over its soil:

```json
{"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
  {"material": <grass over two dirt>,       "thickness": 30},
  {"material": <dirt + coarse dirt, half and half, over two dirt>, "thickness": 15},
  {"material": <stone and andesite, cobblestone at most 30%>,      "thickness": 45}]}}
```

**The grass band's cut is usually too low.** Of 65 such stacks on 58 boards the grass ends at a median of 18°
and 20 end it at 12° or less, which leaves dirt along gentle edges that reads as unintended. The 30 above is a
start, and `incline` is what tunes it.

**A band's material is a set, not a block.** Each band here is one tone carried by two or three textures, and
a ground of several tones nests them — the main set in the middle of a `noise`'s stop list and the patch sets
at its ends, because the end stops come out as patches and the middle ones join into ground. Two stops never
make patches; a `cell` is how even shares are laid. `WHAT-A-BOARD-IS-MADE-OF.md` carries the rulings and the
measured shares.

**Read `incline` before choosing where the bands cut.** It answers how much ground stands in each ten degrees,
which is the only thing that says whether a cut lands where you think it does — and a distribution with a
*spike* in it is a board reporting its own `step` quantum rather than its shape. `opus5-scarp-mask` is the
worked example: 68% moor, 8% shoulder, 11% rock on ground that was 86% grass and nothing else.

### A tread on every mark builds a board with nowhere to stand

`tread` is the fix for the two faults below, and over-applying it is a fault of its own. A tread grades a
mark's shoulder into its neighbour, so a board whose every mark carries one is a board of nothing but
shoulders: no flat to fight on, and no face to decide where anyone goes. It reads as walkable — one connected
place, no ledge, every step within a jump — which is exactly why nothing else catches it.

`RL5` does, off `level` in the relief read: the share of an island under ten degrees, with 30% the bar.

**State a tread where two marks would otherwise meet on a wall, and leave it off the ground meant to be flat
to its edge.**

*`opus5-thwaite-ghyll`, five marks all carrying a tread: 25.4% level and no face at all. The same marks with
the treads off: 43.6% and 70 faces. Grain is not the difference — removing that moves it 0.5 points.*

### A mark's band ends on a wall, and `tread` is the answer to both ways it happens

**A road drawn as a line walls itself.** A `line` mark pins every cell to whichever pass of the line is
nearest, so a serpentine, a switchback or a spiral haul road puts the cells either side of the midline between
two passes a whole winding apart in height.

State a **`tread`** narrower than `r` and the rest of the band lofts — a ramp between the two treads' edges.
Left alone it spreads over the whole run, `atan(drop / (pitch − 2·tread))`, and for a spiral the pitch is
`(r0 − r1) / turns`.

**`batter`**, in degrees, makes it steeper and puts a flat bench at the toe, which is what a worked quarry
looks like.

Work the pitch out before building — under `2·tread` there is no run to grade in, whatever is stated.

**Two different marks whose bands touch do the same thing**, and this one is easy to miss because neither mark
looks wrong on its own. The later one wins its cells outright and the seam is one cell carrying the whole
difference.

A `tread` on the later mark grades it: the shoulder states its height softly and blends into
whatever the earlier mark put there.

The shoulder's **width** sets the grade — 22 blocks over a 4-cell shoulder is 5.5 a cell, over 10 cells it
is 2 — so a gentler seam means a narrower tread or a longer reach.

**Do not go looking for these in a render.** `POST …/sketch/relief/read` answers `seams` per group — every
pair of marks whose ground meets on a step of more than a block, worst first, each with the coordinate to
stand at — and raises `RL3` where one is taller than a scramble. It also answers `silentMarks`, the marks that
pinned nothing at all because they were placed off their group's ground (`RL4`). A seam that grades reports
nothing, so the list is the fault and not the arrangement.

*`opus5-scarp-mask` at (14, −78): `crest` (r 18, h 33) and `terrace` (r 13, h 24) overlap, and the transect read
`33 33 33 DROP −9 24`. The read named it `crest | terrace, step 10 at (7, −80), 43 cells`. With `tread: 7` on
the terrace the transect reads `33 33 32 31 29 28 26 25 24` and the seam is gone. Board-wide, 1,006 barrier
cells became 480.*

### Dressing placed by eye is dressing declined

`opus5-hoarstone`: *"My site filter ignored the fan"* — a prop is judged at **every image of its orbit**;
and *"I tested footprints against the authored polygon instead of the built coast"* — a Bézier edge
bulges outside the vertex ring on a convex stretch and inside it on a concave one. `opus5-hollowmarch`:
*"My keep-out model for the dressing was the wrong shape twice"*. `opus5-smallboards`: four buildings
declined `DR-KEEP` at once.

The report's `claims` is the whole board as one raster of what claims each cell — free, route, structure,
tree, goal clearance, spawn keep-out.

**The raster says where to try; `loop.py --candidates` says whether the try lands**, eight candidates for
one pass. Neither costs a build.

**A placement that lands is not a placement that belongs, and that is the other half of the same mistake.**
A search over the board answers legality and says nothing about composition, so planting every site it
offers puts a forest on ten-block corridors; `WHAT-A-BOARD-IS-MADE-OF.md` §where a tree stands carries the
author's rules, and `techniques/taking-over-a-composed-board` is the worked case — 34 legal sites, ten
planted.

**A search is also narrower than the studio, so let the dressing pass decide.** A filter that keeps only
cells with eight level neighbours refuses every rim cell on a board, and a rim is often the only row a road
leaves; what the studio asks is ground under the trunk, three clear of paving, unclaimed and not kept
clear.

---

## 5. The order a board is built in

```
build-spec.py            write the plan and the refinement (drive.py runs it first)
tools/board.py           the grid — relations between rectangles
drive.py --dry           evaluate + inspect + what the run would change: score, GO1/GO3/GO4, CT12, the lint table
                         ── iterate here; this is where the board's shape is decided ──
drive.py --out …         the dry run, the store, one report read back, the export, the board's picture
the three numbers        the report's head, before the pictures it names
loop.py                  every placement question after the first drive — two seconds, and nothing stored
```

**A refusal is a fault to fix, not a step to work around.** Do not re-post a refused document with
different numbers until you have read why it was refused.

**Every 2xx carries `warnings`, and a `decline` means a piece of what you posted is not in the world.**
`SK9`, `SK10`, `SK15`, `WX11`, `HS7`, `DR-*` all arrive on a 200. The status code is half the answer.
