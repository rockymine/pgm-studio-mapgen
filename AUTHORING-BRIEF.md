# Authoring brief

You are authoring PGM maps by driving the pgm-studio system directly. Several runs have done this before you.
`README.md` lists what each produced and `reports/` carries each one's own account; read the most recent
before you start, because the errata it measured is what will save you build cycles.

**Two things about this apparatus are worth knowing before anything else.**

**You are given art direction.** The last three runs were asked for "a map of your own design" and produced,
three times over, the same map: a roughly square board, one street of identical houses behind the spawn, a
palette nobody checked, and the objectives wherever the plan rectangles happened to fall. That is what an open
brief gets, because the fastest defensible answer is always the generic one. So **`ART-DIRECTION.md` is now
law** — how a board should look, stated as rules with the shipped counter-example beside each — and
**`MAP-BRIEFS.md` names the maps to author**, each with a stated identity, a stated composition, and the one
thing it is a test of.

**Your board is reviewed by a different agent.** A previous report described two empty 245-byte shells as
*"compiled, sketched, finished, exported successfully"* with *"2 destroyables"*, and claimed to have verified
two capabilities it never attempted. No instruction to self-review catches that. A reviewer agent now works
from `REVIEWER-BRIEF.md`, measures your board against the same checklist you are authoring under, and **does
not read your report until it has finished measuring.** Your report is therefore not where you defend the
board. It is where you say what you could not do.

**The map is still only half the deliverable.** The other half is the honest, specific list of what you could
not say and why. A capability that is missing is worth more written down than worked around — and the last
run's largest single failure was reporting brief requirements as impossible when they were documented on the
page it was quoting from.

---

## The loop, and the two calls whose order is load-bearing

**Drive it with `tools/drive.py`**, which `tools/README.md` documents. It takes two authored files —
`specs/<slug>/<slug>.plan.json` and `<slug>.finish.json` — and prints **every finding the pipeline raises,
with its rule id**, at the four places one can appear. Six earlier drivers each read the status code and
threw the findings away, which is why the same declines were re-discovered by hand every run.

```
POST  /plan/evaluate   <plan>      score, valid, the hard/soft terms, the WHOLE lint table — no map row
POST  /plan/inspect    <plan>      goalDistances (GO1's 3.0–4.0), islandGaps (CT12's 15–40), the wall rects
POST  /plan  ·  PUT /map/{slug}/plan
POST  /plan/compile    <plan>      → {layout, intent}. Read the SHAPE IDS here and key the finish on them
      ── patch the compiled layout: themes, relief_scope, controls, addShapes, relief, rooms, dressing ──
PUT   /map/{slug}/sketch/from-plan          → {ok, orphaned, warnings}
POST  /map/{slug}/sketch/relief/read        cells, low, high, symmetry error, per island
POST  /map/{slug}/sketch/finish
PUT   /map/{slug}/intent/from-plan
POST  /map/{slug}/sketch/columns            the DR-* declines        ← AFTER the intent
PATCH /map/{slug}/metadata {name, authors}                            ← AFTER the intent
GET   /map/{slug}/export
```

**Both of those last two come after the intent, and neither is obvious.** `DR-KEEP` reads the spawn doors'
approaches and the goal rings, which come off the intent — asked earlier, `sketch/columns` answers a shorter
list. And storing an intent **projects the map document from the intent's own `meta`**, whose authors a
compiled intent leaves empty, so a name PATCHed earlier is overwritten. **A bare name is a valid author** —
PGM takes a person as an account or a pseudonym, so `{"authors": ["Opus 5"]}` writes `<author>Opus 5</author>`
and is the right form when there is no Minecraft account behind the name.

**Two gates are heard for the first time at the export, at 409, after the whole world is built.** `OB17` —
a goal overhanging void, in a spawn, or in a wool room — and `OB19` — a tree, boulder or building inside a
goal's clearance, which is a **10-block square about the anchor, tested against a footprint plus its eaves
and against every orbit image**. Nothing earlier predicts either. Compute `OB19`'s box and keep it empty, and
cut the holes before placing the goal, or budget a build cycle each (`RP4` in the studio is the pre-flight
that does not exist yet).

## Where things are

| Thing | Where |
|---|---|
| The studio (code, docs) | `/home/user/pgm-studio` |
| The live API | `http://localhost:7894/api` — already running, **do not restart it** |
| Where your maps go | `/home/user/pgm-studio-mapgen` |
| The art direction, the briefs, the reviewer | `ART-DIRECTION.md` · `MAP-BRIEFS.md` · `REVIEWER-BRIEF.md` |
| The errata an author needs beside the docs | `GENERATION-NOTES.md` |
| Every board, its specs and its review | `maps/` · `specs/` · `review/` |
| Hand-authored examples by the repo's author | `/home/user/pgm-studio/tools/seeds/ruediger.{plan,layout,intent}.json` |

`dotnet` is at `/usr/bin/dotnet`. MariaDB is running and migrated. Run long `dotnet` calls as **background**
bash commands. **Do not rebuild the solution** — the API runs from those DLLs and a rebuild fails with sixteen
`MSB3027`s that read like compile errors and are not.

---

## Required reading, in this order

Do not skip and do not skim. Every wrong claim the previous runs made was information already sitting in
their context.

1. **`/home/user/pgm-studio/CLAUDE.md`** — the project's rules.
2. **`ART-DIRECTION.md`** — *read this in full before you draw anything.* It is the strongest instruction in
   this brief. Every rule in it was broken on a shipped board and measured.
3. **`MAP-BRIEFS.md`** — what to author. Pick your two named briefs and **announce them at the top of your
   report before authoring**.
4. **`REVIEWER-BRIEF.md`** — the checklist your board will be measured against. Read it as the specification
   it is; a rule you know about before you build is a fault you do not ship.
5. **`GENERATION-NOTES.md`** — the traps, each of which cost an earlier run a build cycle. **§17 is the
   most recent and the densest**: the ordering above, `OB19`'s real box, the six material field names a guess
   gets wrong, and why an erected shape cannot be an unbridgeable wall.
6. **`tools/README.md`** — the one driver, and what its two files carry.
7. **`docs/tools/flow.md`** — the four levels a map is described at (plan → layout → intent → world), which
   tool owns which, and the five hand-offs. This is the map over everything else.
8. **`docs/tools/capabilities.md`** — what the system can be *asked* for at each stage. Read the section on
   **set algebra and void** especially closely: a `subtract` removes ground entirely and is the instrument for
   cutting a channel; **no relief mark of any kind cuts a hole.**
9. **`docs/tools/plan.md`** — including *"Driving it without the UI"*, which a previous agent called the single
   most useful page in the repository.
10. **`docs/tools/sketch.md`** — the ground: shapes, heights, relief, paint, dressing. Dressing is **authored,
   not scattered**: there is no density pass and no "fill this island with forest".
11. **`docs/tools/library.md`** — themes, materials, house parts, room styles.
12. **`docs/gameplay/approaches.md`** — *read this in full.* Every claim in it is marked `[author]` and
    settled, so it is law rather than advice. **It has been amended since the last run** — see below.
13. **`docs/gameplay/match-flow.md`** — how a CTW map is actually played, from recorded matches. §4 and §6 are
    the parts that will change your board.
14. **`docs/world-export/relief.md`** and **`decoration.md`** — the height model and the prop rules.
15. **`docs/generator/model.md`** — read for the **box model** as *vocabulary*: what a body is, how a hub, a
    lane, a frontline and a dock relate, what a wool approach is made of. **Do not author from a composed
    board** — see below.

Then the previous runs' accounts: `AGENT-REPORT.md`, `AGENT-REPORT-2.md`, `FINDINGS.md`, and the seven files
in `reports/`. Read `reports/haiku-run2.md` knowing what it is: a report describing two maps that do not exist
as working. It is on the reading list as a warning about reports, not as a source.

---

## What changed since the last run

**`approaches.md` is amended, and it is the document that caused the fault.** The guidance about cutting a
void hole in the **middle of terrain** on a `dtm`/`dtc` board is **withdrawn** and replaced by a **depression
or a pond**. Void still belongs at the seam between the two teams' lands. `tallow-kilnrow` is the shipped
counter-example: an 88-block cut across 65% of the board's width sat between its own objectives and the
middle, while the mid band where the two sides meet stayed solid ground — the hole was where the join belongs
and the join was where the hole belongs. An agent reading the old text was being told to build that.

**Three maps did not parse and are now fixed.** A board carrying two objective kinds shipped
`<gamemode>dtm dtc</gamemode>`, and PGM's `Gamemode` is a **closed 25-value enum** matched with no splitting,
so the parse threw. PGM wants the element **repeated**. `tallow-kilnrow`, `ashfall-scar` and `basalt-reach`
have been corrected by hand; the writer fix is `B155`. If you author a board carrying both a destroyable and a
core, **check the `map.xml` your export writes before you commit it.**

**Forty-eight findings from the last runs are filed** as `B141`–`B188` in `pgm-studio/BACKLOG.md`, bucketed
for the agents fixing them. Twenty of them are rules the author states and nothing checks — which is exactly
the list in `ART-DIRECTION.md` and `REVIEWER-BRIEF.md`. **Do not work around a fault by adding a capability;
check whether it is already filed, and if it is, author within it and say so.**

**One live hazard, unfixed, that will waste your time.** A rebuild writes over a region directory it never
clears (`B102`), so an `.mca` a previous build left behind survives into the new map and reads back as part of
it. **Always export each build into a fresh, empty directory.** If two builds of the same map disagree in a
way that makes no sense, this is why.

---

## The rules this run is held to

Each exists because breaking it is what produced the mess the last run was cleaning up.

- **No capability is added in `tools/`.** If you need something the system cannot do, you **file it and author
  the map without it**. A tool may compose, drive and report; a refusal, a placement rule, a sampler or a
  validation living in a tool is the exact defect two shipped tasks were spent undoing. A thin script posting
  JSON to the documented endpoints is fine — anything computing a placement, a clearance or a validation is
  not.
- **No second format.** Author `PlanModel`, `SketchLayout` and `MapIntent` as they are.
- **Nothing is scattered.** Every prop is placed because there is an answer to *why here*. If you cannot
  answer it, leave the ground bare and say so.
- **Layers are not used.** The ground layer only, per `sketch.md`.
- **Every stage is looked at before the next consumes it.** This is not optional and it is the rule broken
  hardest: fifteen boards were once judged from one top-down at the end, and *every* appearance fault in the
  review was visible in an image nobody rendered. Use the preview endpoints — they answer a theme, a material,
  a prop or a plan without building a world — and the read-back renderers listed in `REVIEWER-BRIEF.md` §2.
  **Look at the picture and then say what you see in it**, before the next stage is laid on top. One model
  rendered one image per board across three boards, and produced the two worst boards in the repository.
- **An image is a check, not a source of meaning.** A render answers *whether* what you authored came out; the
  document underneath answers *what it is*. The plan render colours by **role** — blue is a build zone or a
  water lane, never water.
- **A gameplay conclusion is not derived from a measurement.** This session has **no human oracle**, which is
  deliberate. When you hit a question about how a map *plays* that `approaches.md` does not settle: make your
  best judgement, **build it**, and **record the question explicitly** in your report as an open question
  rather than filing it as a fact. One confident, wrong, invented gameplay claim from a correct measurement is
  already committed to this repository's history.
- **Do not start from a composed board.** `/generator` composes whole boards from a player count, a symmetry
  and a seed, and you are not to author from one. Understand the box model from `model.md` — that is why it is
  on the reading list — but painting a theme onto a composed board is what produced fifteen boards that look
  like each other. **Draw your own board**, informed by the model rather than emitted by it.

---

## What to author

**What a run authors is stated when the run is commissioned**, and it has differed: run 3 took the control
plus two named briefs; run 4's three models took four briefs each, and one of them authored four boards of
its own design, one per objective shape the system carries (`ctw`, `dtm`, `dtc`, and one board carrying two
kinds). `MAP-BRIEFS.md` has the named briefs.

The **control** (§0) is the canonical destroy brief, identical for every model and every run, and carries **no
art direction**. It is authored whenever a run is asked for it. It exists so boards stay comparable across models and so the effect of everything in
`ART-DIRECTION.md` can be seen by comparing an art-directed board against it. Author it as the brief reads.

The **named briefs** are §1–§8. Prefer ones no run has answered. Announce yours at the top of your report
before you author anything.

Two of the eight named briefs exist because they have **never been attempted here**: there has never been a
desert map, and never a four-team board. Both are fully expressible — `HousePresets.Desert` is a worked desert
style and `rot_90` fans an orbit to order 4 with a red/blue/yellow/green slot palette already in
`PlanCompiler` — and either is worth more than a ninth variation on something that has been done.

**Every map gets its own theme and its own house styles, written for that map.** The materials system supports
it: any block by id and data, fourteen material kinds each nesting inside any other with no arity limit, a
theme with a rim band, a surface band with its own depth, a wall, a fill, and a **per-shape scope** so
different parts of the board are made of different things. Write your house styles yourself — a `HouseStyle`
carries a roof form and pitch, an overhang and a verge, a wall of stacked `RoomCourse` bands, a floor, posts, a
sill, window styles, gable windows, a door head, beams and a storey stack.

### Five things the last three runs never did, and the art direction is mostly about

Read `ART-DIRECTION.md` for the whole of it. These five are worth naming here because they are omissions rather
than mistakes, so nothing in a report ever flagged them:

- **Nobody planned the board's silhouette.** Decide the extent, the aspect ratio, where each spawn and each
  objective sits, and the two routes between them — five numbers and two lines — **before a shape is authored**.
  A destroy board is a lane; every board here is square, which is why the goal-distance ratios came out flat.
- **Nobody used a path.** Not once, in twenty-one boards. A path is the circulation diagram drawn: it states
  the route, keeps the ground along it clean, and forces you to decide where a player goes before you put
  things in the way. Draw spawn → objective and spawn → flank as paths, then place everything else clear of
  them. The old hazard is retired: a path never drops a building (the road runs to the porch), but the band
  refuses trees within 3 blocks and boulders within 2 of the paved edge (`DR-ROAD`), named in
  `dressing-report.json`.
- **Everyone took whole tone families.** The nineteen families are hand-authored and ordered light to dark, and
  a `cell` over all five members of one is five near-identical blocks fighting for the same ground. **Two
  members is a texture, three a mottle, five a mistake.**
- **Everyone turned the rim on**, because it was the default. On any shape whose ground is solved by a relief,
  a rim caps every fall with a band and turns a rolling hill into contour lines. **Off on grown ground.**
- **Nobody made landforms flow.** The named fault is a flat 20×20 pad butted straight against a hill. A `raise`
  or `sink` shape meets its neighbour along a **`skirt`**, and its surface **tilts** with `anchor_heights`;
  without those, two pieces of ground are just shoved together.

And one thing everybody themed and nobody varied: **the only built thing any board has ever had is a village
behind the spawn.** A single house on a hill, a house in a forest clearing, a mine head, a wellhouse — one
structure whose *style* says what it is beats a sixth cottage. Start from a shipped preset: ten exist, each
demonstrating a technique, and `HousePresets.Desert` and `Diorite` between them model two of the rules the
boards broke most often.

---

## Deliverables

Into `/home/user/pgm-studio-mapgen`, on the branch this session was given:

- **`maps/<slug>/`** — `region/`, `level.dat`, `map.xml`, and `renders/` with the images you actually reviewed
  the map from **at each stage**, not one top-down at the end.
- **`specs/<slug>/`** — every JSON you authored: the plan, the layout finish (themes, room styles, dressing),
  the intent. This is the whole of what was authored; the world is derived from it.
- **`review/<slug>.md`** — what the board is, how it is meant to play, the techniques used, and what went
  wrong. Follow `review/tallow-mirefast.md` for shape. **This is your own account and it does not replace the
  reviewer's** — write it knowing a second agent will measure the same board independently.
- **`reports/<your-model>-run3.md`**, one for the whole run:
  - **Your two chosen briefs**, at the top, before anything else.
  - **What you could not say**, item by item. For each: what you wanted, what you tried, the exact endpoint or
    field you looked for, and whether you concluded it is **missing from the system** or merely **out of reach
    from where you were standing**. Distinguish those two — the difference is the whole point.
  - **What you got wrong**, once you found out. The previous reports' most valuable sections are the ones
    admitting a wrong claim and diagnosing why it was made.
  - **What worked first time.** Not padding: it is how the next reader knows which parts of the system to
    trust.
  - **Open gameplay questions** you had to decide without an oracle, and what you decided.

**Report findings with coordinates** — a per-item table with positions in it, so a claim can be checked
in-game. A prose summary of a geometric claim cannot be verified by the person who has to trust it.

**And a name is not a slug.** The folder is `<your-run-prefix>-<brief-key>`; the map's own name, which is what
a server shows and what `meta.name` carries, is yours to invent, and it never reuses an existing map's.
