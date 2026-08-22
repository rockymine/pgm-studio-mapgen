# Authoring brief

You are authoring a PGM map by driving pgm-studio through its HTTP API. You decide what the map is; the
studio decides whether what you asked for can be built, and tells you, by name, when it cannot.

This is the only brief. There is no reviewer agent, no art-direction agent and no second author — one agent
takes a board from an idea to an exported world and writes down what it could not say.

---

## 1. The system describes itself, and that is where capabilities come from

**Do not learn the API from a document — including this one.** Four reads answer what can be asked for, what
each answer contains, and what every refusal means. They are generated from the routes and the types, so they
are current by construction; a hand-written capability list is a copy free to disagree with the thing it
describes.

| Read | Answers |
|---|---|
| `GET /api/openapi/v1.json` | every route, its request body, its answer, and the failure codes it declares. **120 paths, 151 operations, 291 schemas**, and every answered field carries a description |
| `/api-docs` | the same document as a browsable page, if you have a browser |
| `GET /api/rules` | the **111 rule ids** across 24 families, each with what it *means*, how to *fix* it, and the evidence behind its numbers. `?rule=GO1` and `?family=DR` filter it |
| the answer itself | a refusal names its rule ids; a success carries `warnings` for what it did not do |

Read `GET /api/rules` once at the start of a run. It is the whole vocabulary of every no the system can say,
and it is cheaper to read 111 rows now than to meet them one build at a time.

### What a refusal looks like

Every gate in the studio answers in one shape, so one parser reads all of them:

```json
{ "error": "invalid house style",
  "message": "doorHead.block (5) is not a stair. …",
  "findings": [ { "rule": "HS1", "message": "…", "severity": "refusal", "field": "doorHead.block" } ] }
```

`error` names the gate, `message` is the sentences joined, and `findings` is what to act on. A finding carries
a **rule id**, a **sentence with the measured numbers in it**, and where the fault is — a `field` naming the
JSON path, `subjects` naming the pieces or props an editor would highlight, or neither. When the sentence is
not enough, `GET /api/rules?rule=<id>` answers what the rule means and how to satisfy it.

Status codes are the gate's own: **400** a document wrong as posted · **404** a subject the studio does not
have · **409** well-formed but conflicting with the map's state · **422** cannot be processed · **500** the
studio's own fault. Each route declares which of those it answers — **96 of the 151 operations** name a 404,
409 or 422 in the schema — so what can go wrong is knowable before anything is posted.

### What a success carries

**A 200 is not a promise that everything you posted survived.** Three severities say how much was lost:

| Severity | Means |
|---|---|
| `refusal` | the work stopped; nothing was written |
| `decline` | the work happened and one piece of what you wrote is not in it — the tree, boulder or building the dressing pass could not seat is not in the world, and ignoring it does not put it back |
| `complaint` | the work happened and lost nothing; something is worth saying anyway |

**110 of the 2xx answers declare a `warnings` array**, and all 151 operations declare a `Pgm-Warnings`
response header — `6 RQ3 SK3 SK4` — which is written whenever the complaint channel collected anything, so
the count and the rule ids are readable without parsing the body. **Read the body either way**: an endpoint
that answers `warnings` as its own field — `/plan/evaluate` is one — fills the array without the header.

**Read them after every call.** A driver that reads only the status code is throwing away the half of the
answer that says what the map actually became.

### The one that retires most of the guesswork

**`RQ3` names every field of a posted document that went unread**, by its JSON path:

```
[complaint] RQ3  layout.shapes[1].x   field 'layout.shapes[1].x' was not read …
[complaint] SK3  layout.shapes[0].type
                 shape 'nokind' states kind '', which is not a kind the studio draws
                 — it has 5 (rectangle, circle, polygon, lasso, path) — so it draws no ground
[complaint] SK4  layout.shapes[1]     shape 'rectwh' is a rectangle with no area, so it draws no ground
```

Guessing a field name, nesting a block one level too deep, writing `x`/`z`/`w`/`h` where the rectangle wants
`min_x`/`min_z`/`max_x`/`max_z` — every one of those used to answer 200 and quietly build a smaller map.
They now come back named. **The check after each post is one line: did anything come back under `warnings`.**

Two things `RQ3` does not reach, and they are in `GENERATION-NOTES.md`: the inside of a **theme** and the
inside of a **house style**, both of which are stored as snapshots.

---

## 2. The loop

Drive it with `tools/drive.py`, which `tools/README.md` documents. It takes two authored files —
`specs/<slug>/<slug>.plan.json` and `<slug>.finish.json` — and prints every finding at every place one can
appear, including the ones only visible on a 200.

```
POST  /api/plan/evaluate    <plan>       score, valid, the hard/soft terms, the lint table — no map row yet
POST  /api/plan/inspect     <plan>       goalDistances (GO1), islandGaps (CT12), the wall rects, frontline runs
POST  /api/plan  ·  PUT /api/map/{slug}/plan
GET   /api/map/{slug}/plan/ascii         the board as a grid, one character per cell (?every=N)
GET   /api/map/{slug}/plan/flow          what the board asks of the two sides, in prose
POST  /api/plan/compile     <plan>       → {layout, intent}. Read the SHAPE IDS here and key the finish on them
      ── patch the compiled layout: themes, relief_scope, controls, addShapes, relief, rooms, dressing ──
PUT   /api/map/{slug}/sketch/from-plan
POST  /api/map/{slug}/sketch/relief/read cells, low, high, symmetry error, per island
POST  /api/map/{slug}/sketch/finish
PUT   /api/map/{slug}/intent/from-plan
POST  /api/map/{slug}/sketch/columns     the DR-* declines                     ← AFTER the intent
PATCH /api/map/{slug}/metadata           {name, authors}                       ← AFTER the intent
GET   /api/map/{slug}/coverage           where the ground is lived on, not merely reachable
GET   /api/map/{slug}/export             the world, into a fresh empty directory
```

**Two calls come after the intent and neither is obvious.** `DR-KEEP` reads the spawn doors' approaches and
the goal rings, which come off the intent — asked earlier, `sketch/columns` answers a shorter list. And
storing an intent projects the map document from the intent's own `meta`, whose authors a compiled intent
leaves empty, so a name PATCHed earlier is overwritten.

**Four reads raise no finding at all, which is exactly why they get skipped.** The grid and the flow read the
stored plan and cost no build; the relief read-back looks at the ground before it is built; coverage is the
only read that asks whether any journey *goes* somewhere rather than whether it *can*. All four are worth more
than the render you would have looked at instead.

**Two gates are heard for the first time at the export, at 409, after the whole world is built.** `OB17` — a
goal overhanging void, in a spawn, or in a wool room — and `OB19` — a tree, boulder or building inside a
goal's clearance. Nothing earlier predicts either. `GENERATION-NOTES.md` has `OB19`'s real box.

**A refusal is a fault to fix, not a step to work around.** Do not retry a refused call with a different
document until you have read why it was refused.

---

## 3. What to author

**A board of your own design.** Decide what the map is before you decide what it is made of, and write the
identity down in one sentence — if the sentence cannot be written, the board is not ready.

There are no named briefs and no worked examples on purpose. What the board is for, what it is made of and
where things stand are yours.

**Before any shape is authored**, write down: the extent, the aspect ratio, where each spawn sits, where each
objective sits, and the two routes between them. Five numbers and two lines are the board, and everything
after them is detail. A destroy board is a lane rather than a square — on a square board every goal is
equidistant from both spawns and the ratio flattens.

**Announce what you are building at the top of your report before you author anything**, so what you set out
to do can be read beside what you built.

### What the studio checks for you, and what it does not

The numbers a board is held to are in `GET /api/rules` — the goal-to-spawn walk ratio (`GO1`), the strait
between two teams' islands (`CT12`), the ground a spawn door opens onto (`SP8`, `SP9`), the clearance around a
goal (`OB19`), the passage past a building (`DR-PASS`), how two wings of a house meet (`HJ1`–`HJ5`). Meeting
them is not a design achievement; it is the floor.

What no gate asks is whether the board **looks** like anything, and that is where every previous run's boards
came apart. The observations below are measured off shipped boards and are enforced nowhere:

- **Two members of a tone family is a texture, three a mottle, five a mistake.** `TerrainPalette.Families` is
  nineteen hand-ordered families; taking a whole one puts five near-identical blocks on the same ground.
  Reach across **two** families for ground that reads as one thing but not one block.
- **A building is never in the same family as the ground it stands on.** Name three families out loud before
  painting: which is ground, which is built, which is the accent. An accent that appears once is not an accent.
- **Stained clay, wool and glass are shade rows, not ground** — a stated colour, never terrain.
- **The rim is off on ground a relief solved.** A rim caps every fall with a band and turns a rolling hill
  into contour lines; it belongs where an edge was *made* — a coast over void, a platform lip, a retaining
  wall's top course.
- **A landform meets its neighbour along an authored transition**, never a flat pad butted against a hill.
  The four fields are `skirt`, `anchor_heights`, `height_mode` and `relief_scope`.
- **Draw the routes as paths before the scenery.** Spawn door → objective, objective → flank, wool → hub. A
  path is the circulation diagram drawn: it states the route and keeps the ground along it clean.
- **A board carries more than one placement idea.** A village behind the spawn may be one of them; a single
  house on a hill, a house in an authored clearing, a mine head or a wellhouse whose style says its function,
  a run of buildings as a boundary are the others. Six footprints in one style is a settlement; one footprint
  in six materials is a swatch.
- **Nothing is scattered.** Every prop is placed because there is an answer to *why here*. Bare ground you
  chose beats dressing you did not.
- **Start a house style from a shipped preset and fork it.** Ten exist, each demonstrating a technique;
  `GET /api/room-styles/{id}/json` answers one as the stamper's own JSON. Repaint `storeys[*].wall` as well
  as `wall`, or the fork is half applied.
- **Look at a house in section before building a world.** `/api/room-styles/preview` answers plan, section,
  isometric and cutaway. Every shipped roof fault was visible in a section and invisible from above.

### The one thing that is not yours to decide

**A rule about the map as it is *played* has a human oracle, and this session does not have one.** When you
hit a question `docs/gameplay/approaches.md` does not settle — what an objective needs around it, whether a
channel should be bridgeable, how unequal two ways round may be — make your best judgement, **build it**, and
**record the question in your report as an open question** rather than filing it as a fact. A correct
measurement plus an invented conclusion is already committed to this repository's history.

---

## 4. Where things are

| Thing | Where |
|---|---|
| The studio (code, docs) | `/home/user/pgm-studio` |
| The live API | `http://localhost:7894/api` — already running, **do not restart it** |
| Where your map goes | `/home/user/pgm-studio-mapgen` |
| The errata the API cannot state | `GENERATION-NOTES.md` |
| The driver | `tools/README.md` · `tools/drive.py` · `tools/board.py` |
| Every board built here, its specs and its review | `maps/` · `specs/` · `review/` |
| Hand-authored examples by the repository's author | `/home/user/pgm-studio/tools/seeds/ruediger.{plan,layout,intent}.json` |

`dotnet` is at `/usr/bin/dotnet`. MariaDB is running and migrated. Run long `dotnet` calls as background
shell commands. **Do not rebuild the solution** — the API runs from those DLLs and a rebuild fails with
sixteen `MSB3027`s that read like compile errors and are not.

### Reading, in this order

1. **`GET /api/rules`** — the whole vocabulary of refusal, before anything else.
2. **`GENERATION-NOTES.md`** — what the API still cannot tell you. Short, and every entry cost a build cycle.
3. **`tools/README.md`** — the driver and what its two files carry.
4. **`/home/user/pgm-studio/docs/tools/flow.md`** — the four levels a map is described at (plan → layout →
   intent → world), which tool owns which, and the five hand-offs. This is the map over everything else.
5. **`docs/tools/capabilities.md`** — what the system can be asked for at each stage. The section on **set
   algebra and void** especially: a `subtract` removes ground entirely and is the instrument for cutting a
   channel; **no relief mark of any kind cuts a hole.**
6. **`docs/tools/plan.md`**, **`sketch.md`**, **`library.md`** — each has a *Driving it without the UI*
   section, which is the part that matters here.
7. **`docs/gameplay/approaches.md`** — read in full. Every claim in it is marked `[author]` and settled, so
   it is law rather than advice. **`docs/gameplay/match-flow.md`** §4 and §6 are what will change your board.
8. **`docs/world-export/relief.md`** and **`decoration.md`** — the height model and the prop rules.
9. **`docs/generator/model.md`** — read for the **box model as vocabulary**: what a body is, how a hub, a
   lane, a frontline and a dock relate, what a wool approach is made of.

**Do not author from a composed board.** `/generator` composes whole boards from a player count, a symmetry
and a seed. Understand the box model — that is why `model.md` is on the list — but painting a theme onto a
composed board is what produced fifteen boards that look like each other. Draw your own, informed by the
model rather than emitted by it.

---

## 5. The rules this run is held to

- **No capability is added in `tools/`.** If the system cannot do something, file it and author the map
  without it. A thin script posting JSON to documented endpoints is fine; anything computing a placement, a
  clearance, a sampler or a validation is a second copy of the system.
- **No second format.** Author `PlanModel`, `SketchLayout` and `MapIntent` as they are.
- **Layers are not used.** The ground layer only, per `sketch.md`.
- **Every stage is looked at before the next consumes it.** Fifteen boards were once judged from one top-down
  at the end, and every appearance fault in the review was visible in an image nobody rendered. Use the
  preview endpoints — they answer a theme, a material, a prop or a plan without building a world — and look
  at the picture, then say what you see in it.
- **An image is a check, not a source of meaning.** A render answers *whether* what you authored came out;
  the document underneath answers *what it is*. The plan render colours by **role** — blue is a build zone or
  a water lane, never water.
- **A picture shows what a board looks like; a grid shows what it is made of.** `GET /api/map/{slug}/plan/ascii`
  answers the plan as `text/plain`, one character per proxy cell, with a key. A plan is a list of rectangles
  and most of what goes wrong with one is a **relation between two of them** — a landform wider than the band
  that reaches it, a wall on the only throat, a room whose door opens onto its own apron. A top-down of the
  built world cannot show that, because by then they are terrain. `tools/board.py` is the same read off the
  plan file, before a map row exists.
- **Export into a fresh, empty directory every time.** A rebuild writes over a region directory it never
  clears (`B102`, open), so an `.mca` a previous build left behind survives into the new map. If two builds
  disagree in a way that makes no sense, this is why.

---

## 6. Deliverables

Into `/home/user/pgm-studio-mapgen`, on the branch this session was given:

- **`maps/<slug>/`** — `region/`, `level.dat`, `map.xml`, and `renders/` with the images you actually
  reviewed the map from **at each stage**, not one top-down at the end.
- **`specs/<slug>/`** — every JSON you authored: the plan and the finish. The world is derived from them.
- **`review/<slug>.md`** — what the board is, how it is meant to play, the techniques used, and what went
  wrong. Follow `review/tallow-mirefast.md` for shape.
- **`reports/<your-model>-<run>.md`** — one for the run:
  - **What you set out to build**, at the top, before anything else.
  - **What you could not say**, item by item. For each: what you wanted, what you tried, the exact endpoint
    or field you looked for, and whether it is **missing from the system** or merely **out of reach from
    where you were standing**. Those two are different and the difference is the point.
  - **What you got wrong**, once you found out, and why the wrong claim looked right.
  - **What worked first time.** Not padding: it is how the next reader knows what to trust.
  - **Open gameplay questions** you had to decide without an oracle, and what you decided.

**A claim about a capability is checked before it is filed.** An agent's account of what it could not do is
evidence about the *surface*, not about the system, and the two have diverged badly before: one run reported
five of six requirements as impossible while quoting the documentation describing two of them. Before writing
that something is missing, look for it in `GET /api/openapi/v1.json` and say what you found.

**Report a geometric finding with coordinates** — a per-item table with positions in it, so a claim can be
checked in-game. A prose summary of a geometric claim cannot be verified by the person who has to trust it.

**A name is not a slug.** The folder is `<your-run-prefix>-<something>`; the map's own name, which is what a
server shows and what `meta.name` carries, is yours to invent, and it never reuses an existing map's.
