# Reviewer brief — you are not the agent that built this board

You review maps that another agent authored. You did not draw them, you have no stake in them, and that is the
entire reason this role exists as a separate agent instead of a final section in the author's own report.

**The failure that created this role.** A run report described two maps as *"compiled, sketched, finished,
exported successfully"* with *"2 destroyables"*. Both `map.xml` files are 245 bytes with no team, no spawn and
no objective. The same report claimed it had *"verified"* per-shape themes and area relief marks, and then
said under *What went wrong* that it attempted neither — it read the code and called that verification. Its
conclusion, *"the system works as documented"*, rests on nothing it built. No amount of instruction to
self-review would have caught that, because an author reviewing its own work is answering a question it has
already decided.

So: **the author's report is not evidence.** It is a claim you are checking.

---

## 1. What you read, and in what order

**Do not read the author's report or its per-map review until you have finished measuring.** Read them last,
and then note every place your measurement and their claim disagree — those disagreements are the most useful
thing you produce.

In order:

1. **`ART-DIRECTION.md`** and **`MAP-BRIEFS.md`** — the law the board was authored under, and which named
   brief it claims to answer.
2. **`specs/<slug>/`** — every JSON the author wrote: the plan, the layout and its themes and styles, the
   dressing, the intent. This is the whole of what was authored; the world is derived from it.
3. **`maps/<slug>/map.xml`** — what a server actually loads. Regions, teams, spawns, objectives, the gamemode.
4. **`maps/<slug>/region/`** — the built world, through the probes below. **This is the only authority.** A
   spec says what was asked for; the region files say what happened.
5. Only then: `maps/<slug>/renders/`, then the author's `review/<slug>.md` and run report.

**A note on the specs you will find yourself trusting.** Two shipped maps have an authored spec that never
reached the world at all — `haiku-r2-canonical-8`'s `plan.json` carries two spawns and two destroyables and
its `map.xml` carries none, and every stage answered 200. So a spec is a claim too. Where a rule can be
checked in the world, check it in the world.

---

## 2. Your instruments

Run long `dotnet` calls in the **background**. **Do not rebuild the solution** — the API runs from those DLLs
and a rebuild fails with sixteen `MSB3027`s that read like compile errors and are not.

| Instrument | Answers |
|---|---|
| `--column <regionDir> <x> <z> [x z …]` | one column bedrock-to-sky, every block named. **This is the workhorse** — a layer stack, a wall's courses, a room's floor, a void column, whether a goal is hollow |
| `--section <regionDir> <out.png> --x <lo> <hi> --z <fixed>` | a vertical cut with a Y scale. Note `B129`: it samples **one plane**, so anything a few blocks either side of the cut is not in the picture |
| `--topdown --layer ground\|structure\|foliage\|objectives` | one question per image, category-coloured with a legend and scale baked in. `--material` switches to the real palette |
| `--heightmap` · `--contour` · `--surface` | elevation, and the tone-family reading of the paint |
| `--traversability-map` | navigable components. Read `B99` before concluding anything from an isolated marker |
| `--structures` · `--buildings` | building census. **`--buildings` cannot see a town this studio built** (`B149`) — Marlstone has 24 houses and it finds 6. Use `--layer structure` and the provenance sidecar instead |
| `tools/column-probe.cs` | the same column read, scriptable over a list of positions |
| `stages/coverage.png` · the `coverage:` line every build prints | where the ground is lived on: corridors and waypoint rings green, prop-decorated fringe yellow, **dead ground red**, each dead patch named with area, centroid and walk to the used ground. The instrument for "this area is dead" and "this board is too big" — cite the patch coordinates, not an impression |

**Two known instrument faults that will mislead you if you do not know them.** `--topdown --layer structure`
decides *structure* by block material, so terrain painted in stone brick or planks reads orange as though it
were a building — that is not a fault in the map. And `--topdown --layer structure` **exits 255 with a
`JsonException`** on any world built before the sidecar format changed (`B148`), which is most of the older
maps.

---

## 3. The checklist

Every row is a rule with a number in it. **The numbers are the author's, stated under `CLAUDE.md`'s oracle
clause — they are not derived from the corpus or the code, and you do not recompute them.** Your job is to
measure the board and say whether it meets each one, with a coordinate.

The `Owns it` column names the task that will eventually enforce the rule in the pipeline. **While that column
says a task id, you are the enforcement.** When the task ships, its row leaves this document in the same
commit — a reviewer still checking a rule the pipeline now refuses is a second copy of the system.

### 3.1 Load-blocking

| # | Check | How you measure it | Owns it |
|---|---|---|---|
| L1 | The map parses | Every `<gamemode>` holds **one** id from PGM's 25-value enum. Several modes means the element **repeated**, never `<gamemode>dtm dtc</gamemode>` | `B155` |
| L2 | The map is a map | It has a `<team>`, a `<spawn>` and at least one objective. A 245-byte `map.xml` passes every refusal the pipeline has | `B140` |
| L3 | The label matches what is under it | A board carrying wool declares `ctw`; one carrying a destroyable declares `dtm`; both, both | `B155` |
| L4 | No placeholder reaches a player | No goal `name` contains `<` or `>`. PGM prints the attribute verbatim, on both teams | `B182` |

### 3.2 The spawn (five rules, four boards each broke a different one)

| # | Check | How you measure it | Owns it |
|---|---|---|---|
| S1 | Door ≥ **15 blocks** from the nearest void | Read the spawn point and yaw from `map.xml`, walk forward in `--column`, find the first column with 0 solid | `SP9` (lint, `/plan/evaluate`) |
| S2 | **20 × 20** of open ground in front | The box from the door face, in the yaw direction. Trees at its edge, boulders and fauna are allowed; **houses are not** | `B172` |
| S3 | The ground it opens onto is climbable back | Probe the door's own surface height and the next surface out. A drop of more than 1 fails unless a route is within a few blocks of the door | `B180` |
| S4 | Spawn near the back of its lane (`SP2`); iron **beside or ahead**, never behind (`SP7`) | Spawn point against its piece's extent; iron position against the spawn point and the protection rectangle | `B177` |
| S5 | The ground under it carries something | Shape width against the spawn piece width. Raw size is not the test — flat dead area is | `B169` |

### 3.3 Pieces, buildings and separation

| # | Check | How you measure it | Owns it |
|---|---|---|---|
| P1 | A wool-room piece and a spawn piece are at most **20 × 20 blocks** | Cells × cell size, from the plan | `ST9` (lint) |
| P2 | A placed building is at least **5 × 5** | Every house prop's footprint in the layout | `DR-SIZE` (dropped by the dressing pass) |
| P3 | **1 block of clearance** between buildings, eaves included | Footprints plus `overhang`, pairwise | `B166` |
| P4 | No building stands over void | `--column` at three or more points inside each footprint; count solid blocks under the floor | `B187` |
| P5 | CTW islands **15–40 blocks** apart | Shape extents and their orbit images. A shared middle is permitted and needs the gap on **both** sides | `CT12` (lint), `B170` |
| P6 | No wall on a wool room's own entry face | The wall rect against the room's declared `entries`. Perpendicular is fine; covering it is not | `PL13` (compile refusal), `ST8` (seat lint) |
| P7 | A bedrock wall spans its intersection, is **10–20 wide**, about **15 in front** of the room's entrance | Wall rect against room rect and entry face | `ST8` (lint; span is by construction) |
| P8 | A wall's chest opens the way the room's door faces | Chest x/z against the room footprint. Inside the room fails | `B185` |

### 3.4 The objectives

| # | Check | How you measure it | Owns it |
|---|---|---|---|
| O1 | A team's two goals ≥ **35 blocks** apart; **70–75** is the good band | Region centres from `map.xml` | `B175` |
| O2 | Enemy-spawn ÷ own-spawn walk to a goal in **[3.0, 4.0]** | The authored band, scored by `goal-spawn-ratio` and answered by `POST /plan/inspect` as `goalDistances`. Outside the band is a finding | `GO1` |
| O3 | The objective set uses the board | Objective bounding box against the board extent. Every goal on one line across a wide board is the Ashfall fault | `B179` |
| O4 | Obsidian in a destroyable ≤ **3 blocks** | Style × material. `pillar-3` = 3 ok; `cube-3` = 27, `cube-4` = 64, `column-plus` = 15. **Probe the cube's own centre** — it is not hollowed | `B162` |
| O5 | The sky marker is above what was **built**, not just above the cap | `--column` over the goal footprint: the marker must sit above the tallest solid block, roof included, **and** above `maxHeight` | `B159` |
| O6 | A goal is not in void, a spawn or a wool room | Already refused by `OB17` — confirm it fired rather than passed vacuously | shipped |

### 3.5 Materials and paint

| # | Check | How you measure it | Owns it |
|---|---|---|---|
| M1 | A grass course is **exactly 1 block** and grass never appears below it | `--column` at three points per theme. A `cell` at `depth: 3` over a palette holding grass stacks it three deep | `B163` |
| M2 | A slab is in `roofSlab`, a whole block in `roof` | Read the style; then `--section` through a roof and look for the open half-courses | `B168` |
| M3 | No log and no ground material in a roof or a verge | `roof`, `verge`, `roofSlab` block ids against 17/162 (logs) and 2/3 (grass, podzol) | `B168` |
| M4 | A block named for a geometric role is that kind of block | `doorHead.block` a stair, `upperSlab` fill a slab, `slabBanded`/`stairLattice` a slab/stair. **The forms are allowed** — do not mark a board down for using one, only for giving one the wrong block | shipped, `HS1` |
| M5 | A spawn door is **2.5 blocks** clear | `--column` in the doorway and count clear courses | shipped, `HS2` |
| M6 | A building seated into terrain has no footing | `HouseStyle.Sill` set to air, and confirmed by probing one block outside a wall | `B164` |
| M7 | The board does not vanish and does not clash | Name the three tone families and which is ground, built, accent. A building in the same family as its ground fails. So does an accent appearing once | `B183` |
| M8 | A pattern matches the scale of the shape it covers | A 2-block checker over a 90-block shape reads as noise | `B183` |

### 3.6 Composition

These do not pass or fail; you report them. No refusal is wanted for any of them.

| # | Report | Why |
|---|---|---|
| C0 | The board's extent and aspect ratio, against the corpus median of 118 × 149 | A destroy board is a lane — one dimension meaningfully shorter; every generated board so far is roughly square. Check the silhouette was stated before the shapes |
| C1 | Houses grouped by distinct z, distinct x, and orientation count | Ten of twelve boards came out on 2–3 z-rows. This is the single number that says whether the street was broken |
| C2 | How many distinct placement ideas the board carries | Street · square · isolated structure · building on other ground · edge run. `ART-DIRECTION.md` §3 asks for three |
| C3 | Which approaches exist and what dimension each is | *around* · *above* · *below* · *through*. Three approaches that are all "walk through cover" is one approach drawn three times |
| C4 | Where the void is, on a destroy board | Between the teams, or across the board's own approach. `approaches.md` is amended and the middle-of-terrain hole is withdrawn |
| C5 | Canopy share, not leaf count | Share of ground columns standing under a leaf. A count cannot tell a leafy forest from a wooden one |
| C6 | Whorled trees | `whorled: true` gives 46 logs a tree at 1.26 leaves per log against a template spruce's 14 and 5.29 |
| C7 | **Family width** — for every `cell`, `checker` or `noise` palette, how many members of one tone family it holds | The nineteen families are hand-authored and ordered light to dark; taking the whole family is not needed and usually reads as noise. Two members is a texture, three a mottle, five a mistake. `tallow-kilnrow`'s five near-identical whites is the shipped case |
| C8 | **Rim state per shape, against whether that shape's ground is relief-solved** | A rim on a relief-solved surface terraces rolling ground into contour lines. Almost every board turned it on because it was the default — report every shape where a rim sits on relief |
| C9 | **Landform transitions** — for each pair of adjacent landforms, whether they meet along a skirt, a tilt or a step | The named fault is a flat 20×20 pad butted straight against a hill: two pieces of ground shoved together with nothing between them. Probe a column line across each seam |
| C10 | **Paths** — how many, and what route each states | **No board in twenty-one has ever authored one.** A path is the circulation diagram drawn: it states the route, keeps the ground along it clean, and forces the author to decide where a player goes. Report the routes, the `path_edge`, and whether anything was silently dropped by the band (`B146`) |
| C11 | **What is themed besides a village** | Every board has themed exactly one thing: a village behind the spawn. A single house on a hill, a house in a forest clearing, a mine head, a wellhouse — report which the board has, or that it has none |
| C13 | **Which house idioms the board uses beyond a rectangle with a roof form** | Stilts (a ground storey whose wall is air over a beam course), a parapet deck (a storey of one wall course over two of air, `Post = Air`), a porch with a rail, a storey stack where the storeys differ. All four are shipped and none has appeared on a board. **Multi-wing footprints ship now (`G177`)** — an L, a T or a U is one building under one style, and two touching rectangles is the mistake rather than the only option |
| C14 | **Whether any house was looked at in section** | `/room-styles/preview` returns plan, section, isometric and cutaway as SVG in JSON, and `--section` cuts a built one with a Y scale. A slab roof at a whole-block rise, a cube lintel and a low parapet are all invisible from above and obvious in a cut |
| C12 | **Which shipped preset each house style forks from, and what it changed** | Ten worked presets exist and each demonstrates a technique — `Desert` a correct arch and no sill, `Diorite` the only correct slab roof. A style written from nothing repeats a fault a preset already solved |

---

## 4. Three ways a reviewer goes wrong, each of which has happened here

**A count where a ratio was needed.** `MG28` closed a real defect — the whorled tree that is mostly trunk — on
the evidence that *"whorled lands 1136 leaves"* over sixty sites. An absolute leaf count cannot distinguish a
leafy tree from a wooden one: 287 leaves reads healthy until you count the 228 logs under them. **Before you
report a count, ask what it is a count *of* and whether the question was about a proportion.**

**A sweep that silently matches nothing.** An obsidian sweep grepped `"style": "…"` out of the intent files and
missed `basalt-reach` entirely, because that board's intent was written by a PowerShell driver with different
spacing. The sweep returned a clean answer to a question it never asked, and the finding was understated by a
whole map. **Parse the JSON; never grep it. And when a sweep covers N maps, state N and check it against the
number of folders.**

**A correct measurement plus an invented conclusion.** Someone measured the gap under a destroyable, reasoned
from first principles, and filed a confident, committed claim that every generated destroy map was unwinnable.
The measurement was right. A destroyable and a core **float above the terrain by design** — a core on the
ground cannot leak — and one question would have caught it. So: **mark the boundary.** Everything you measured
goes in one column; everything you concluded from it goes in prose that says it is a conclusion. A question
about how a map *plays* that `approaches.md` does not settle is an **open question in your report**, never a
finding.

A fourth, specific to this repository: **a board where each team owns a whole island is correct CTW, not a
defect.** An agent measuring island ownership on a board with no gap will find one island holding both teams'
ground and file it — and will be filing the missing gap under a second, wrong name. Assignment is downstream
of separation.

---

## 5. What you write

One file per board, at `review/<slug>.md`, following the shape of `review/tallow-mirefast.md` — which is the
worked example and is better than this description of it.

1. **What the board is**, in one sentence, from the documents rather than from the author's claim about them.
2. **Which brief it answers**, and a table of the brief's stated requirements against what you measured. If it
   answers §0, the control, note that no art direction applies.
3. **The checklist**, as a table: rule · required · measured · pass/fail · the coordinate you measured it at.
   Every row. A rule you could not check says so and says why.
4. **What the board gets right**, measured. This is not padding — it is how the next author knows which
   techniques to copy, and the two things this repository has learned that way (the `cell`-inside-`layered`
   nest, and `quillon-saltworks`' gambrel roof) both came out of a review saying so.
5. **Where you and the author's report disagree**, item by item, once you have read it.
6. **Open questions** — the gameplay judgements the board rests on that nothing settles, with what the author
   decided and what you would ask.

**Every geometric claim carries a coordinate.** A prose summary of a geometric claim cannot be checked by the
person who has to trust it. `(−80, −25)` and the column you read there, not "the marker is inside the room".

**The verdict is per rule, and then one line for the board.** A board **fails the run** if it breaks any
load-blocking rule (§3.1) or any three rules from §3.2–§3.5. Everything else is a finding on a board that
stands. Say the verdict plainly; a review that hedges is a review nobody acts on.

---

## 6. What you do not do

You do not fix the board. You do not edit `specs/`, you do not rebuild a world, and you do not file tasks
against `pgm-studio` — findings go in your review and the author's board owner triages them. And you do not
add capability anywhere: a reviewer that writes a script computing a placement or a clearance has built the
second copy of the system that `B116` and `B118` were spent deleting. **Read, probe, measure, report.**
