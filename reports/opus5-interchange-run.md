# Opus 5 — Interchange: a liminal DTM board, and the first one authored on four storeys

## What I set out to build

A brief arrived from outside this repository, from a person who had never authored a PGM map. In
their words: a **Liminal DTM** — an ordinary overall theme at the centre, branching out toward the
edges into familiar environments and structures, made as detailed as possible while feeling
*slightly strange or unsettling*; three to five obsidian monuments to find and destroy, each in its
own area with its own layout and colour scheme; areas not necessarily on the ground — underground,
high in the sky, or somewhere else unusual. **Repetition and exploration** as the two ideas the map
is for. Named devices: one theme recurring across several similar-looking spaces; heavy use of
corridors and stairways that loop back into places already visited; glass between spaces so areas
are visible from each other in ways nobody meant; one or two small structures repeated as decoration
across every area; occasional very large or very narrow spaces, kept brief. Within 200 × 400, and
smaller if it works. Five monuments a team, of one or two blocks each.

What I set out to build from that: **a municipal transit interchange folded onto itself** — a
concourse over a drained swimming pool and under an empty car deck, a corridor of doors that loops
back on itself, a lawn visible through glass and unreachable from the corridor that crosses it, and
the same kiosk standing in every room. 124 × 248, four storeys, ten obsidian monuments of one or two
blocks.

The board is `maps/opus5-interchange`, the documents `specs/opus5-interchange/`, the account of what
it is and how it plays `review/opus5-interchange.md`.

## The one prediction that did not come true

The brief warned that a **hidden obsidian destroyable underground** would hit an export error, and
offered a backlog entry (`B249`, a per-call override past the gates) as the way through it.

**It did not hit one.** `The Deep End` stands at `(30, 6, 78)` in the bottom of a drained pool, under
the concourse slab, on the `under` layer, and the export gate answered **OPEN** on the first build
that had a walkable route to it. Nothing in `MapExportComposer` objects to a goal below a roof:
`OB17` asks whether a goal's footprint stands on land, in a spawn, or in a wool room, and `IsLand`
is a set of `(x, z)` over *every* layer's columns, so an underground column is land like any other.
`EX1` is the check that could have refused it, and it did not, because the walk that decides
traversability reads the rasterizer's own spans — a cell on two layers answers twice — so the
undercroft is a place the walk can stand in and the stairwell joins it to the rest of the board.

`B249` was therefore not pulled up and no gate was overridden. The entry stays where it is.

What *did* refuse the underground room, twice, was the map being wrong rather than the studio being
strict, and both times the finding named the fault exactly:

- **`SK11`, 3,336 places around `(16, 56) @3`** — the whole undercroft, with sky over none of it and
  no route onto it. The stairwell existed; its last two columns had zero and one block of headroom
  under the concourse it passed beneath, so nothing could walk it. The concourse's mouth had to stay
  open until the ramp was three courses clear of the soffit.
- **`SK11`, 1,738 places around `(12, 44) @19`** — the corridor of doors, sealed. I had drawn glass
  panels *in* the doorways instead of beside them; a stained-glass shape is terrain, so the two
  doors into the loop were glazed shut.

Both are complaints rather than refusals, which is right — a detached mass may be an island the
author meant — and both are the reason to read `warnings` on a 200. A driver reading status codes
alone would have shipped a board with an unreachable pool and called it done.

## What I could not say

**A plan cannot state which storey a goal stands on.** `DestroyablePlacement` and `CorePlacement`
have `piece`, `at`, `style`, `materials`, `float` and `name`, and no `layer`; `DestroyableIntent`
and `CoreIntent` have `Layer`, as do the other four intent placements and `PlacedProp`. So the word
exists everywhere the export reads it and nowhere the plan writes it, and a plan-built goal on a
stacked board always resolves against `SurfaceTop`, which is the highest layer — a monument stated
for a pool lands on the deck roofing it. Four of this board's five goals need the word.

Checked before filing: `GET /api/openapi/v1.json` carries `layer` on `MapIntent`'s six placements
and on the prop schema, and carries no such property on either plan placement schema. **Missing from
the system**, and small: the field is a string on a record the compiler already builds.

What I did instead is the thinnest patch that is not a second format: `tools/drive.py` gained a
`goalLayers` key, `{"destroyable-1": "under"}`, which writes `layer` onto every orbit image of that
marker in the compiled intent before it is stored, matching on `stamp.unit`. It computes nothing;
it copies an authored word onto a document.

**A layer's paint depends on where its entry sits in `layers[]`, and nothing says so.**
`TerrainPainter.Paint` iterates `SurfaceByLayer` in document order and each pass paints its whole
column from the bedrock course up to that layer's surface; the stone-only invariant is what stops
two passes treading on each other. So a storey listed *after* one that stands over it finds no stone
left. A compiled plan emits `layers[0] = ground`, and `drive.py` appended slabs to the end, so the
undercroft was painted by whichever ground-layer shape was smallest over each column: the drained
pool came out in the corridor-of-doors' brown clay, and a 2 × 4 glass door panel painted its whole
column, twenty-six courses, yellow.

Measured at `(20, 70)` before the fix: yellow stained glass from y0 to y25 in one column. After
inserting the `under` layer at index 0: `y5..y3` white clay (the pool deck's checker), `y2..y1`
hardened clay, and the corridor's brown from y12 up. `docs/tools/sketch.md` says a column carries
one theme *per layer* and `FEATURES.md`'s `TS23` entry says the scope is keyed `(layer, cell)` —
both true — but neither says the painting is order-dependent, and the order that works is not the
order a compiled document arrives in. **Out of reach from where I was standing** rather than
missing: the document can express it, and a one-line `below` flag in the driver was enough. It would
be safer as a sort in `TerrainPainter.Paint` — ascending by the layer's own floor — since document
order is an authoring accident on any board whose ground came from a compile.

**A slope of one course per cell builds as treads of two.** A `ramp` polygon over 12 cells with
`anchor_heights` falling 18 → 6 rasterized as `18 16 16 14 14 12 12 10 10 8 8`, and a two-block rise
costs a placed block in the walk's model, so the stairwell could be walked down and not up
(`…/walk?aim=reach` answered `blocks 3` bottom-to-top). The same shape at 20 cells for the same 12
courses reads one course a cell and walks both ways for nothing. The up-ramp, 20 courses over 32
cells, was right first time and is what the correction was measured against. **Not a defect I can
demonstrate** — the rounding may be correct and my slope simply on the boundary — but it is a number
worth having: **run at least twice the rise** for a stair meant to be climbed.

**A prop's keep-out mask does not know about storeys.** `DR-CLAIM` declined `kiosk-deck`, on the
`deck` layer at y38, as "claimed by the building `kiosk-hall`" on the `ground` layer at y18, twenty
blocks below it. The claim is footprint overlap in `(x, z)`, and `PlacedProp.Layer` exists and is
read for *seating* the prop but not for deciding whether two props are in each other's way. **In the
design as it stands**, and defensible for trees and boulders whose canopies hang; wrong for two
buildings on different storeys. I moved the kiosks apart in plan, which is not what an author of a
stacked board wants to have to do.

**`render/topdown?layer=` means two different things and a board can only have one.** The word
selects a *sketch layer* by id on a stacked board, and the category isolations the authoring brief
recommends — `?layer=structure`, `?layer=foliage`, `?layer=objectives` — answer **422 `RQ4`**: "this
board has no layer 'structure' — it carries ground, under, catwalk, roofs, deck". The refusal is
clear and lists the alternatives, so nothing is hidden; but the three per-category reads the driver
takes on every board are unavailable on any board that names its own layers, and they are the reads
that answer *did the props land where I put them*. **In the design**, as one query word doing two
jobs, and the collision is total rather than partial.

**Nothing places a light source.** The service level and the pool hall are enclosed by construction
and there is no block in the palette, no theme bucket and no prop that lights them. Two light wells
cut through the concourse and the core's glass floor are the whole of the daylight underground. On
this board the dark is on-theme; on a board that wanted a lit basement it is a hard stop. **Missing
from the system**, and it is the one gap that would change what a stacked board can be.

**`GET /api/map/{slug}/column` is the read that settled every disagreement**, and it is worth saying
plainly because it is not the read a picture points you at. Nine of the ten faults in this run were
found by reading a column and counting courses; the renders confirmed them afterwards. `?at=x,z`
repeated is the whole interface, and the 400 it answers a caller who writes `?x=&z=` names the right
form.

## What I got wrong

**I put the glass in the doorways.** The two openings from the spine into the corridor loop, and
the four "doors" of the door-rank, were authored as glass-themed shapes in the gaps I had left for
them. A theme is paint on terrain, not an absence of terrain: the shapes built solid and the room
was sealed. The tell was `SK11` naming 1,738 places, which I first read as a complaint about a
roofscape. Glass is now *beside* the doors, and the wall is written as a run of
`(z0, z1, theme-or-None)` where `None` is the gap — which is the form that makes a door visible in
the source at all.

**I sized the basin so there was nothing to paint.** A two-course basin is one course of bedrock and
one of fill, so the surface stack never runs and a "drained pool" came out in the hardened clay of
whatever theme owned the column. Three courses gives the stack two to work with, and the pool floor
reads as light-blue clay streaked cyan over prismarine.

**I read `GO1` off `/plan/inspect` and believed it.** The five markers answered 2.19–5.31 there, and
I moved the spawn and re-spread the goals twice to improve numbers that describe a board without
walls. The plan is five rectangles; every corridor, wall, gate and stair on this map lives in the
sketch, and the real walk answers 1.70–2.77 — *lower* than the plan's reading, not higher, because
the maze lengthens the defender's own walk more than the raider's. The plan-level distance reads are
a floor and nothing more on a board authored this way, and I should have gone straight to
`…/walk?aim=reach` over the built world.

**I assumed the export's zip had no top-level folder.** `drive.py` moved `provenance.json` out of
`<out>/region/`, and the archive extracts to `<out>/<slug>/region/`, so the sidecar shipped inside
the world folder on every run in this session until I noticed. Fixed to take whichever of the two
shapes is on disk.

## What worked first time

- **The up-ramp.** 20 courses over 32 cells, `anchor_heights [26, 26, 6, 6]` at `floor 12`, meeting
  the car deck's west edge at exactly y38 on adjacent columns. One-block treads the whole way, no
  placed blocks, no `SK10`.
- **A goal naming its storey.** Once `layer` reached the intent, all four off-ground monuments
  landed on the surface they were stated for, first build, with no adjustment to `float`.
- **`voidEnforcement` with no exclusions.** One flag, and `<apply block-place="deny(void)"
  region="void-enforcement-area"/>` over `<everywhere/>`.
- **The house-style gate.** Both forked styles were refused at `POST /room-styles/preview-snapshot`
  with `RQ1` naming `$.doorway.head.form` and the enum it could not read — before a world existed —
  and answered 200 the moment the word was one the reader has.
- **The glass crossing.** The spine passing through the garden court with panes both sides and no
  door was authored once and measured 52 blocks of walking to get 16 blocks sideways, which is
  exactly what it was drawn for.
- **`SK9` staying silent.** Every wall on this board is the same slab carried higher — floor 12,
  thickness 14 instead of 6 — and the gate that names two adds stacking on one layer never fired,
  which is the confirmation that the idiom is the right one.

## Open gameplay questions

Three, decided without an oracle and recorded here rather than filed as facts.

**Should a five-goal board hold every goal to `GO1`'s band?** The rule's 3.0–4.0 is stated per goal.
Five goals on one lane cannot all sit in it unless they sit at one depth, and putting them at one
depth throws away the reason to have five. I built a **front-to-back gradient** — 1.70 on the car
deck, 2.77 behind the court's two gates — so a raid has an order to it, and left every number in the
review for the author to overrule.

**Should a room's walls be climbable?** Every wall here is eight courses over the concourse, so
`aim=travel` finds routes over them for 7–17 placed blocks against 82–156 blocks of walking. I read
that as the intended shape — corridors are free, roofs are priced — and did not raise the walls,
because a maze nobody can leave is not more liminal, only more tedious. Someone who thinks the
corridor of doors should have to be walked would raise them to sixteen.

**Is a one-way drop a route?** The two light wells fall twelve blocks from the concourse into the
service level. They are a fast way in and no way out, which is what a hole in a floor is, and the
stairwell is the return. I kept them because a shortcut that costs health and commitment is a real
decision; a board that wanted every route reversible would close them.
