# Studio 2.0: a map as a recipe of operations

How a pgmvox board could live in the studio without losing what made it good, and without losing what the studio
gives a person who wants to see, edit and diff what an agent did. Options are weighed in §3; the recommendation
is §4; the API and the model's loop are §5 and §6; the order of work is §8.

## 1. What each side gives a reader

**The studio gives a person the map as documents.** A plan of pieces on a five-block grid compiles to a sketch
layout of shapes, relief, paint and dressing; an intent states the play; the world and `map.xml` are compiled from
the three. Each level is stored, versioned as numbered changes, rendered, read back and editable in the browser,
and a hand edit made in the browser is handed to the next agent run as an `SR1` finding rather than overwritten.
A person can see what an agent did at every level, change any of it, and diff two changes.

**pgmvox gives an agent the map as a program.** `plan.py` holds the board as data (a per-block raster with
storeys, the objectives as objects, routes as polylines), and `gen.py` turns it into blocks with library calls
and local code. Nothing between the plan and the world is a document: the terrain is the state of a numpy array
after fifteen calls, a town is a loop over house records, a mill wheel is forty lines of `w.set`. A person sees
the plan sketch and the renders, and can read the code.

**What made the boards better is exactly what makes them opaque.** Every cause in the report's short answer (the
open substrate, landform operations in a chosen order, the grammar, angled frames, props with a reason) lives in
the code path between plan and world, which is the path the studio shows as documents and pgmvox does not show at
all.

## 2. The friction, item by item

| # | Friction | Why it bites |
|---|---|---|
| F1 | Code is not a document | The browser cannot edit a Python call, a diff of code says nothing about the ground, and no intermediate state exists to render unless someone instruments the run. |
| F2 | Running code on the server | An agent's Python on the deployed studio is arbitrary code on a shared 4 GB, two-core machine. |
| F3 | Two sources of play | pgmvox writes its own `map.xml` from `objectives.py`; the studio writes it from the intent. One map would have two answers to "where is the red monument". |
| F4 | Two plan granularities | The studio plan is rectangles on a five-block grid; pgmvox's is per block, with polygons and storeys. Brittlebush III shows they meet: a brittle cell is five blocks, so a studio plan *is* a grammar blueprint. |
| F5 | Library as data against library as code | The studio stores themes, patterns, house styles and trees as rows a person can open; pgmvox's styles are Python dicts and functions (`brittle.STYLE`, `clay`, `build.STYLES`). |
| F6 | Bespoke things | A mill wheel, a ship's hull, a headframe, a broken bridge. No schema will name all of them in advance, and the boards' quality depends on them. |
| F7 | Reads only on stored maps | The studio's read-backs need a stored map; pgmvox's run offline on any world. |
| F8 | Stamps and gates do not run on a made world | Markers, outlines, wool rooms, defence walls, kit pairing and the export gate run inside `WorldBuilder` and never see a pgmvox world. |
| F9 | Parameters that cannot be seen | The studio's relief marks are constraints solved together: a point mark with reach 0 lifts the whole footprint, a reach of 15 or 45 changes the hill's size and how it meets the edge, and a push's skirt and crown can disagree into a cliff (`RL6`). Nothing shows what one mark did until the whole field is solved. pgmvox's landforms each do one named thing, but only the code says which. |

## 3. Four ways to hold a pgmvox board

**A · Upload the world.** pgmvox runs in the agent's container, writes the world, and the studio imports it as it
imports a corpus map; Configure then states the play over it. It costs almost nothing, since the import and the
scan exist, and it closes F3, F7 and F8 at once (the studio's intent becomes the one source of play, its reads
work, its stamps can run over the import). It answers F1 not at all: the ground is a blob, and a person can neither
see how it was made nor change one landform.

**B · Store the code.** The map stores `plan.py` and `gen.py`, and the studio runs them in a sandbox. It keeps all
of pgmvox's power and answers F1 only for someone who reads Python. It makes F2 the studio's problem permanently,
and a person in the browser still cannot move a hill.

**C · A recipe of operations.** The map stores an ordered list of operations (terrain operations with their
parameters, carves, grammar sections, placements of houses, props and trees, each with an id) and the studio runs
them deterministically, keeping each step's output. A person scrubs the steps, sees what each one changed, edits a
parameter, and diffs two changes as operations rather than as code or voxels. It answers F1, F2, F5, F7, F8 and F9.
It does not answer F6: whatever the operation vocabulary cannot name cannot be built, which is the studio's own
limit moved one level down.

**D · A recipe with made things.** C, plus one operation that places a **made thing**: a block volume with an
anchor, a footprint and a turn, uploaded by the agent together with the source that generated it. The studio
treats it as an object: it can be moved, turned, replaced and inspected, and its source is kept for provenance,
but the studio does not run that source. A made thing the second board needs becomes a library prop with
parameters, exactly the rule pgmvox already follows ("a thing written twice belongs in the library").

| | A upload | B code | C recipe | D recipe + made |
|---|---|---|---|---|
| A person sees how the ground was made | no | as code | step by step | step by step |
| A person can edit one landform | no | no | yes | yes |
| A diff says what changed | voxels | code | operations | operations |
| Bespoke things | yes | yes | no | yes, as objects |
| Arbitrary code on the server | no | yes | no | no |
| Stamps, gates, intent, reads | yes | if wired | yes | yes |
| Cost to build | days | weeks | months | months |

**D is the destination and A is the first step.** A is days of work and makes every freeform board safe to play
(the studio's stamps, gates and intent over it). D is where a person can actually see and shape what an agent
built. C alone would rebuild the studio's limit at a lower level, and B gives up on the person in the browser.

## 4. The recommendation: the recipe

### 4.1 One document, operations in order

A map gains one stored document, the **recipe**, between the plan and the world. Its steps run in order over a
shared state, and each step reads and writes named things in it:

- `H`, the heightfield, and further named heightfields for undersides and storeys
- named masks: `sea`, `river`, `roads`, a build zone, a footprint claimed by a house
- the block volume, with tile entities
- named point and polyline sets: places, routes, the objectives' anchors

Every operation is a pure function of its parameters and the state it reads, so a step's output is keyed by a
hash of its parameters and its inputs, and editing step *k* re-runs from *k* only.

### 4.2 The operation families

| Family | Operations | Comes from |
|---|---|---|
| `field` | `noise` (fbm, ridged, tilt terms), `solve` (the studio's relief marks and pushes, unchanged), `blend` | pgmvox `noise`; studio `ReliefSolver` |
| `landform` | `scarp`, `butte`, `spire`, `terraces`, `canyon`, `watercourse`, `lake`, `coast`, `grade`, `hold` | pgmvox `landform` |
| `route` | `find`, `network`, `pave`, `steps` | pgmvox `route` |
| `paint` | `lay` (top by angle, soil by slope, snow line), `beds` (strata that dip and fold), `theme` (the studio's band stacks, unchanged) | pgmvox `terrain`; studio painting |
| `form` | `underside`, `skirt`, `tower`, `cloud_deck`, `mountain_ring` | pgmvox `terrain`, `forms` |
| `carve` | `tunnel`, `chamber`, `gallery`, `shaft`, `dress_cave` | pgmvox `under` (answers TS140) |
| `grammar` | `from_plan` (a studio plan read as a blueprint), `sections`, `lay` with a style | pgmvox `grammar`, `studioplan` |
| `place` | `house` (heading, storeys, style), `trees` (scatter with spacing), `prop` (library props with a facing), `made` (a made thing) | pgmvox `build`, `trees`, `props` |
| `play` | the intent, as today, and its stamps | studio `MapIntent`, `WorldBuilder` |

The studio's relief solver is one operation in this list, not a thing replaced: a board can start with marks
where the author wants control and add landforms after them. The studio's pushes are already operations applied
after the solve; the landforms are more of the same kind.

### 4.3 Styles stay data

A grammar style (body, faces with their courses, accents with module, period, phase and margin, seams, fills in
order, motifs) and a house style (about ten material slots and the archetype that fixes the framing) are library
rows, as themes are today. The Brittlebush and Claywork styles become the first two rows. What stays code is the
grammar's rules (a bay laid whole or not at all, fills that decline) and the house archetypes' framing, which is
why their output looks good whatever materials are chosen.

### 4.4 The upload road survives

An imported world is a recipe of one step: `place.made` covering the whole board. Configure works over it exactly
as today. A person who uploads a map and draws its regions never sees the recipe.

### 4.5 The plan road gets shorter

A plan drawn in the planner compiles, as today, into the recipe's first steps. With a grammar style bound, its
pieces become sections in one step (`grammar.from_plan`, which is what `studioplan` already does), so the coloured
map appears from the plan at once, as Brittlebush III did.

### 4.6 The recipe, measured on a real board

**The Vale's whole terrain is a 2,438-byte recipe, and running it reproduces the library's own result exactly.**
`recipe/vale.recipe.json` states the Vale's twelve steps (one `field.noise` with three terms, eight landforms, two
routes, a hold). An interpreter of about seventy lines, mapping each operation name onto one pgmvox call, runs it
to a heightfield identical in all 40,000 columns to what `examples/vale/scripts/land.py` produces.

**Every step but the routes runs in under forty milliseconds; the two route steps take about ten seconds each.**
The landform steps are numpy over a 200 × 200 grid. Route finding is a search over the ground and dominates the
run, which is why a step's output is cached by the hash of its parameters and inputs: an edit to the canyon re-runs
the canyon and what follows it, and an edit to the paint re-runs nothing above it.

**A diff needs two layers, and the second is the one a person needs warned about.** Version B of the recipe moves
the butte fifteen blocks west and widens the canyon. Two steps' parameters changed; six steps' *effect* changed,
because the ground under them moved. The roads re-routed over 3,261 columns and the footpath over 358, though
nobody touched either. A diff that lists only edited parameters reports a two-line change to a board whose road
network moved.

**The vocabulary a model speaks is 61 operations with 403 parameters**, most of them with defaults
(`recipe/op-catalog.md`). The studio's Russetford, for comparison, stores a 378 KB layout and a 357 KB refinement
(themes 44 KB, made layers 51 KB, dressing 59 KB), generated by a 426-line `build-spec.py`. A recipe states a
landform where a layout states its result, which is why it is two orders of magnitude smaller.

## 5. The API

The map's source call gains the recipe, and the recipe gets its own calls for working on one step:

| Call | Body | Answers |
|---|---|---|
| `PUT /api/map/{slug}/source[?dry=true]` | `{plan?, recipe, intent, refinement?}` | the change, per-step summaries (cells raised and cut, blocks placed), findings; a dry run stores nothing |
| `GET /api/map/{slug}/recipe` | | the recipe with step ids, and each step's state hash |
| `POST /api/map/{slug}/recipe/steps` | `{after, step}` | inserts a step; answers the new change |
| `PUT /api/map/{slug}/recipe/steps/{id}` | `{params}` | replaces one step's parameters; re-runs from it |
| `POST /api/map/{slug}/recipe/steps/{id}/preview` | `{params}` | the step's output with the parameters given, stored nowhere |
| `GET /api/map/{slug}/recipe/steps/{id}/render` | `?view=height\|top\|iso\|section&box=&line=` | a picture of the state after that step |
| `GET /api/map/{slug}/recipe/steps/{id}/delta` | `?format=text` | what the step changed: a mask of cells raised and cut, blocks set by kind, named things it wrote |
| `GET /api/map/{slug}/recipe/diff` | `?from=&to=` | steps added, removed and changed (with parameter diffs), and per changed step a before and after |
| `POST /api/map/{slug}/made` | a block volume, an anchor, a footprint, the generating source | a made-thing id a `place.made` step names |
| the existing reads | `?step=` added | `column`, `transect`, `slopes`, `incline`, `walk` taken after any step, not only on the finished world |

Every step answers findings in the studio's one shape, with the step's id as the subject, so a refusal names the
operation and the parameter that caused it.

## 6. How the model works with it

The order of work stays the one `ORDER-OF-WORK.md` gives, and each phase is a range of steps the agent posts and
then reads back before the next:

1. **Plan the places** on the land's outline, with numbers and targets. The plan is the studio's plan document,
   grown to carry polygons, storeys and per-piece heights (§8, stage 4).
2. **Post the terrain steps** (`field`, `landform`, `route`), read `slopes`, `incline` and `walk` after the last
   one, and post again until the numbers meet their targets. A dry run costs seconds.
3. **Post the carves**, read the x-ray render and the walk across storeys.
4. **Post the made ground** (`grammar` or houses and props), read the renders by step.
5. **State the play** (the intent), and let the stamps and the export gate run.
6. **Hand over.** The person opens the inspector, scrubs the steps, changes a parameter or leaves a note on a
   step. The next agent run receives each hand edit as an `SR1` naming the step and the parameter, as it receives
   hand edits today.

A board that needs something the operations cannot say generates it locally with pgmvox, uploads it as a made
thing, and says so in its report. The made things that recur are the backlog for new operations.

## 7. What a person sees: the inspector

The prototype published beside the report shows the shape of it on the Vale, the library's terrain example:

- **a timeline of steps** on one side, each named by its operation and id;
- **the view** of the state after the selected step, top-down shaded with contours, with the cells that step
  changed washed red (cut) and blue (raised), and a section along any line;
- **the step's parameters** as the agent sent them, editable;
- **a noise playground** that draws each octave of an `fbm` term and their sum, so a reader sees what `cell`,
  `octaves` and `gain` do before choosing them.

## 8. The order of work

1. **Stamps over a made world.** Import a pgmvox world with its intent; run `WorldBuilder`'s stamp pass and the
   export gate over it. Fix the two house defects in pgmvox (door before windows; the cell outside a door at any
   heading). Add the playtest's gates to pgmvox's read-back.
2. **The recipe as a document**, with `place.made` and the step reads, storing and rendering steps that pgmvox
   computed. The studio holds and shows the recipe before it can run one.
3. **The operations in the studio**, family by family, in the order the boards used them: `field` and
   `landform`, `paint.lay` and `beds`, `carve`, `place.house` with a heading, `grammar`, `route`. Each family
   ported is one the studio runs itself, and one fewer the agent uploads.
4. **One plan**: the studio's plan document carries polygons, storeys and per-piece heights, and its
   numbers-with-targets become rules.

## 9. What this does not decide

- **Where the engine runs while the operations are ported.** Running pgmvox as a worker beside the studio would
  make stage 2 run recipes at once, but it is a second implementation of every operation the studio later ports,
  which the repository's rule against two shapes of one concept forbids for long. The recommendation is that pgmvox
  computes and the studio stores and shows, until each family is ported.
- **How much of a house style is data.** The ten-slot archetype is what made pgmvox's houses look right; the
  studio's 57 styles are what make its houses varied. The archetype as a library row, with the studio's styles
  mapped onto archetypes, is the obvious meeting point and has not been tried.

## 10. What the studio already does better, and keeps

The merge runs both ways. These are the studio's, measured in the same investigation, and each is an operation or
a rule pgmvox takes rather than the other way round.

- **Strata that follow the land (TP26).** A band datum raised by a share of the ground averaged over `reach`
  cells carries beds along the broad tilt while a hill cuts through them. pgmvox's beds are either level with a
  dip and fold or locked to the surface; its `bed_offset` becomes `follow × mean(H over ±reach)`.
- **The eye view.** Mojang's textures, a camera aimed by name, and a text twin. pgmvox has no textured render.
- **The window/door rule and wings.** `HouseWindows` drops a seat beside a doorway; houses have L, T and U
  wings and porches. pgmvox has neither.
- **The relief solver.** Marks are the right tool where an author wants an exact height at an exact place; it
  stays as the `field.solve` operation and pgmvox's landforms follow it.
- **The stamps, the gates and the codec**, as §8 stage 1 says.

## 11. Why the studio's noise reads grainy

The studio's relief grain and pgmvox's `fbm` are the same kind of noise (lattice values, interpolated, summed in
octaves). Ported side by side and swapped, the algorithm made little difference and the settings made all of it:
the grain's default scale of 9 with three octaves halves to cells of 9, 4 and 2 blocks, so its finest octave varies
at the size of a block step, and amplitude over feature size above about 0.3 turns rounding into a field of steps
(grain 14 at scale 9: 23% of neighbouring columns two or more apart). The smoothstep interpolation adds a smaller,
second effect, contours running square to the lattice at large scales, which a cubic spline or gradient noise
removes. The recipe's `field.noise` should carry `cell`, `octaves` and `gain` explicitly and refuse a finest octave
under about five blocks on ground meant to be walked.
