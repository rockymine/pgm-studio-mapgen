# Run 6 — a teaching library, and one map built out of it

## What I set out to build

Not a map, first. Eighteen **showcases**: one folder per technique, each a complete map whose only reason to
exist is the one thing its README names, so that an agent or a person who wants to know *how a cliff is
stated* can read the eleven lines that state it instead of finding the cliff inside a thousand-line finish.
Then one full map built out of them, so the library has an answer to "and what is all this for".

They live in `showcase/`, deliberately not in `maps/`, because they are documentation that happens to be
loadable rather than boards anybody should put in a rotation.

**The organising rule is that every showcase forks one board and changes one thing.** `01-base-board` is the
smallest capture board the evaluator accepts — score 0, no violation, no lint — so anything a showcase's own
evaluation reports is about its technique. That makes the diff the lesson, and it makes eighteen documents
comparable with each other.

Nine were authored by hand; nine were handed to sonnet subagents against a written brief once the pattern was
established, and every one of those was reviewed against its own renders and column reads before it was
committed. One of the nine needed correcting: `12-underpass` reported that a rasterized column carries one
span, full stop, and the scope was missing — `SketchRasterizer` skips a span pair that shares a **layer**,
which only means anything because two layers can share a cell, and a genuine undercroft is `addLayers`. Two
boards in this repository already measure that. The claim was right about what it tested and wrong about the
system, which is the failure the deliverables rule names, and it survived one review before a source read
caught it.

## What I could not say

**There is no way to delete a map.** `POST /api/plan` derives a slug from the name and makes it unique against
what is stored, so every rebuild of the same board mints `foo-2`, `foo-3`, `foo-4`. Over an authoring session
that iterates twenty times, the slug the README cites is not the slug the last build used. Looked for
`DELETE /api/map/{slug}` in `GET /api/openapi/v1.json`: there are thirteen `DELETE` routes and none of them is
a map — the closest is `DELETE /api/map/{slug}/sketch/discard-if-empty`. **Missing from the system**, and the
workaround (`delete from map` against the database) is the wrong shape and unsafe with more than one author
working at once. A `DELETE /api/map/{slug}` would close it; so would letting `POST /api/plan` take a slug and
replace, the way `POST /map/from-documents` already does.

**A relief mark's fields are not covered by `RQ3`.** `RQ3` names every field of a posted document that went
unread, by JSON path, and it is the single most useful thing in the whole surface. A relief mark's *inside* is
resolved past that walk: `08-cliff` posted a `scarp` carrying `h` and `width` — a `line` mark's field names —
and the reader took neither. `ScarpMark.High` and `.Low` defaulted to **0**, the mark pinned the middle of the
board to bedrock, and the export gate stayed OPEN. The only witness was `relief/read`'s `low`. **Out of reach
from where I was standing** rather than missing: the mechanism exists and the mark reader is simply not
walked by it.

**Nothing measures whether a step can be walked up.** `WalkGround.Steps` asks only whether the vertical span
fits under the clearance over the lower place, and its own docstring says so: *"On a board with nothing
stacked over it every place has open sky, so this never refuses a step."* It models a player who can place
blocks, which is right for a strait crossed by bridging and wrong as a test of whether a stair is a stair.
`05-steps` shipped a flight of two-block risers past `evaluate`, `inspect`, `preflight`, `traversability` and
`coverage`, all green. **Missing from the system** — and the honest form of the gap is narrow: a walkability
read that names the steepest single rise along each route between waypoints would have caught every instance
of it in this run, including the four-block wall at the head of a haul road on the full map.

**A theme cannot be keyed on elevation.** A `layered` stack's axis is `depth` or `inward`, a pattern's `rise`
makes its field three-dimensional rather than selecting by altitude, and there is no bucket that reads height.
So a solved hill is one material to its summit, and rock above a treeline is a second *shape* rather than a
second bucket. Confirmed by reading `TerrainTheme.cs` and `TerrainPatterns.cs` rather than by failing to find
a field. **Missing**, and arguably correctly: `10-landform-shapes` shows the shape answer working, and a
height-keyed bucket would be a second way to say the same thing.

**`axis: "inward"` cannot ring an inset shape.** Its own docstring describes *"a cobble rim then two rings of
stone brick then a field"*, but the distance it reads is `BucketContext.Inset` — *"how many steps in from the
landmass's void-facing edge"* — computed once per column over the whole island. A court standing three blocks
in from the coast reads inset 3 everywhere inside it. **Out of reach**: the mechanism is right for an island's
own shore and there is no per-shape equivalent. `rimEdges: "boundary"` looks like the other answer and is not:
a plateau is a height grouping, so an override-add at the same height is the same plateau.

## What I got wrong

**I measured a stair every two blocks and called it walkable.** On the full map, four haul roads sampled at
two-block intervals reported "max step 2", which is one block per block and fine. Sampled every block, one of
them had a genuine two-block riser at the head. A two-block riser and two one-block risers are the same
number at two-block resolution. The wrong claim looked right because the sampling was invisible in the answer.

**Then I wrote three ground-finders and two of them were wrong.** "The topmost solid block" reads a roof.
"The topmost block that is not a leaf or a log" reads a plank roof, and it also skips the ground when the
ground is Stone *Bricks* and the filter matches on `"Bricks"`. "The top of the contiguous run from bedrock"
walks up a tree trunk, because a trunk sits directly on the ground. The one that works is the contiguous run
with logs and leaves removed first. Three wrong readings all produced plausible tables.

**I told seven agents not to clear the database and then cleared it myself**, mid-run, to get a clean slug for
the full map. One reported its map no longer queryable. Its artifacts were captured while it was live, so
nothing was lost, but the instruction was right and I broke it.

**I assumed a defence wall's chest side was still authored.** It is derived now, and the plan field is gone;
writing `side` is silently ignored. Reading `docs/tools/plan.md` first would have been faster than reasoning
from the older map specs in this repository, several of which still carry the retired field.

## What worked first time

- **`POST /plan/evaluate` and `/plan/inspect` as an iteration loop.** Both answer with no map row and no
  build, so a board's whole shape can be decided in seconds. The full map went through five topologies before
  anything was compiled; every refusal named a rule id and every rule id answered `GET /api/rules?rule=<id>`
  with the measurement behind it. `FR6`, `LN2`, `WL9`, `WL10` and `ST9` between them rewrote that board, and
  each one was right.
- **`GET …/plan/ascii` and `…/plan/flow`.** The grid is the only view that puts two rectangles on the same
  rows, and the flow account said *"the defence arrives from behind the objective while the attack arrives at
  its front"* off the plan alone, before a world existed.
- **`shapePropsById` carrying `vertices` and `controls`.** Replacing a compiled ring with a drawn one and
  bending it with Catmull-Rom handles turned a rectangle into a coastline in one key, and the dead share
  *fell* from 3.3% to 1.9% — a wandering coast adds ground where routes already run.
- **The room-style binding.** `"@name"` loading `tools/styles/<name>.json` is what keeps a finish short enough
  to be an example. Forking two shipped presets took one pass and both stamped correctly first time.
- **`relief/read`'s `symmetryError`.** Zero on all nineteen boards, unprompted. It is the only preview that
  says whether terrain is any good without an eye.
- **The dressing pass's declines.** `DR-SITE`, `DR-CLAIM` and `DR-KEEP` caught every prop that would have been
  wrong, named the coordinate, and never once refused something that was right.

## Open gameplay questions

Decided rather than derived, and recorded as questions.

- **Is a wool at the bottom of a pit a fair objective?** Whinnymoor's sump sits eight blocks below the moor
  that overlooks it. A defender on the lip has a clear shot into the approach and an attacker in the sump has
  nowhere to retreat to. Built as is.
- **Should a chasm be bridgeable along its length or only at the mid band?** Whinnymoor's is buildable only
  under the mid band, so a team's two flanks are joined by its back line rather than across the working. That
  makes the board a horseshoe and gives the defence an interior line. The alternative is a shortcut.
- **How many one-block treads is a stair rather than a slope?** `05-steps` uses four over twenty blocks and
  `06-ramp-and-slant` eight over the same twenty. Both are walkable and they read completely differently; no
  rule distinguishes them.

## What the library is worth

Nineteen boards, eighteen of them one idea each, every number in every README copied from a response. The
part that will age is the numbers; the part that will not is the section every document has on **what went
wrong first**, because each of those is a mechanism that is still there.

---

# Run 7 — a destroy board on two storeys

## What I set out to build

A DTM lane, 100 × 200 a side, with **tunnels**; an organic border; **three land regions** — sandy, rocky,
forest — in one board; the surface painted with a brush rather than one pattern per region; relief taken as
far as it goes while keeping walkable ground; and an **uncanny** underground that surfaces. Two destroyables
a team, one of them down there.

It is `maps/opus5-sandcaster`, and `review/opus5-sandcaster.md` is what it became.

## What I took from another agent's branch rather than rediscovering

`claude/liminal-dtm-map-wr16sr` built a four-storey liminal DTM and found what a stacked board needs. Two of
its findings are capabilities this branch's driver did not have, and I took the implementations **verbatim**
so the two branches merge without a conflict:

- **`addLayers` `"below": true`.** The painter walks the stack in document order and each pass paints its
  whole column, so a storey listed after one standing over it finds no stone left. A compiled plan emits
  `layers[0] = ground`, which is not the bottom of a board with an undercroft.
- **`goalLayers`.** `DestroyablePlacement` carries no `layer`, so a plan-built goal on a stacked board always
  resolves against the top surface — a monument stated for a corridor lands on the reef roofing it.

Plus its measured rules: a ramp needs **run at least twice its rise** or it builds as treads of two; a prop's
keep-out mask is 2-D and does not read `layer`; `render/topdown?layer=` names a sketch layer.

Where I departed from it deliberately: that board's colours are loud and unrelated between rooms. This one
puts everything on **one hue axis** — a cool pole, a warm pole, a green that ties them, and the underground
as the same value range gone cold — with exactly two saturated blocks on the whole board.

## What I could not say

**There is still no way to delete a map.** Twelve full builds of a 110 × 400 board, each minting a new slug.
Filed against the surface in run 6; unchanged.

**A brush stroke's safe form is not discoverable.** A shape carrying a `theme` and no height reads as "paint
this, leave the height alone" and is nothing of the sort: `RasterShape` gives it one course at bedrock. On
flat ground and on ordinary solved ground the override form works anyway, because the relief writes the
solved surface back over the cell — so the failure only appears where a `relief_scope: "exclude"` shape owns
the ground, and then it is a hole twenty courses deep with no warning of any kind. **Out of reach rather than
missing**: the correct form exists (`operation: "add"`, one course, no override) and nothing names it.
`RQ3` cannot help — every field posted was read.

**Nothing pictures a stacked board from the side.** `render/section` cuts one plane and `render/topdown
?layer=` draws one storey flat; neither shows a tower standing on a lid over a corridor. **Out of reach
rather than missing**: the studio *has* an isometric WebGL preview — the Sketch tool's 3-D canvas,
`js/studio/render/iso-webgl.js`, fed by `POST /map/{slug}/sketch/columns` — and no endpoint exposes it. I
drove it in a headless browser instead: `renders/iso-*.png`. The one thing that made it possible is worth
recording because it wasted twenty minutes first: **the host serves the Blazor client only in
`Development`**; started with `ASPNETCORE_ENVIRONMENT` unset, every page under `/` is a 404 while `/api`
answers fine.

**`SK11` appears to ask its question inside one layer.** A roofed corridor reports 608 places of standable
ground with "open sky over them and no route onto them" while `render/traversability` reads one component
with all four goal markers connected and pre-flight opens the gate. Both cannot be describing the same board.
Recorded as a reading rather than filed as a defect, because I did not read the check.

## What I got wrong

**I wrote a `GENERATION-NOTES` entry that was half true and then met its other half.** The entry said an
override-add with no height follows the solved surface — measured, on a board where every cell was in a
solved footprint. It cost eleven holes on this board before I read `SketchRasterizer` and found the actual
mechanism. The correction is in the file; the lesson is that a measurement on one board is a measurement on
one board.

**I put the tunnel under the wrong region twice.** First under the wash, whose landforms are dunes carved
*into* the ground — which a flat lid erases; then with the goal still on the wash after the tunnel moved to
the reef, so the Cistern sat 80 blocks from the chamber named after it. The under-layer render is what
showed it: a clean corridor with the goal marker nowhere near it.

**I told seven agents not to clear the shared database in run 6 and then cleared it myself. In this run I did
it twelve more times** — this time with no other agent running, which makes it defensible rather than right.

**Three wrong ground-finders in run 6, and a fourth here**: "the top of the contiguous run from bedrock"
walks up a tree trunk. The rule that works is that run with logs and leaves removed first.

## What worked first time

- **`POST /plan/evaluate` + `/plan/inspect` as a search.** Five board topologies and a grid search over two
  goal positions, all before a map row existed. `FR6` refused a 28-cell frontline and taught me that a
  frontline is either split or 6–8 cells wide; `WL9` refused a spawn at one end with a goal beside it; `LN2`,
  `WL10` and `ST9` each rewrote something. Every one was right.
- **The under layer, first build.** Floor, walls, lid, ramps, bays, pool and chamber all landed at the
  heights they were authored at, verified by column reads. The `below` flag and `goalLayers` did exactly what
  the other branch's notes said they would.
- **Region hold marks.** Four `area` marks at four heights, written after the rim and before the landforms,
  hold a four-tier board flat and let everything else be written over them. No seam anywhere on the board.
- **The dressing pass.** Every prop that would have been wrong was named with its coordinate: `DR-SITE` for a
  boulder hanging its footprint over a coast, `DR-ROAD` and `DR-CLAIM` for trees on a road or on each other,
  `DR-KEEP` for one in the spawn's door approach, `OB19` for one in a goal's clearance. The final build
  declines nothing.

## Open gameplay questions

In `review/opus5-sandcaster.md`: whether a goal in a sealed underground room with one door is fair, whether
the chasm should be bridgeable, and whether a one-way drop into the corridor reads as a shortcut or as the
way in. All three were decided and none was derived.
