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
