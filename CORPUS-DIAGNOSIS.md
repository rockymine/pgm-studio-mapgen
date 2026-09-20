# What an agent reads before it makes a map, and why it is wrong

A handover. Every number here was measured on 2026-09-19 against the repository as it
stands, and nothing in it needs re-measuring before work starts. The recommendation at
the end is an opinion and is marked as one.

The subject is not any single document. It is the whole body of text an agent loads
before it draws anything, and the question is what of it should be loaded at all.

**Its measurements are kept as measured and most of what it recommends has since
landed.** The reading list is gone and `AUTHORING-BRIEF.md` §4 is a question table;
`capabilities.md` is retired; `GENERATION-NOTES.md` is shortened and points at cards;
the map log is `BOARDS-BUILT.md` with a gate over it; and `pgm-board-warmup`'s budget
is remeasured — §2 below is what it used to say, and it no longer says it. What has not
changed is the reason any of it was worth doing, which is the rest of this document.

---

## 1. The measurements

### `GENERATION-NOTES.md` is well-formed per paragraph and unusable per document

The file is 1,869 lines: 330 prose paragraphs, 209 bold claims or headings, 54 table
rows. It **passes** `tools/prose-check.py` with zero paragraphs over the cap and a
median of 53 words. Nobody wrote it badly. There are simply 330 correct findings in a
row, with no priority and nothing marking which are law.

### Its largest section duplicates the skill

| Section | Lines | Share |
|---|---:|---:|
| Reading the world back | 800 | 42% |
| Authoring the layout | 541 | 28% |
| Dressing density | 146 | 7% |
| Before a plan is posted | 98 | 5% |
| Buildings | 55 | 2% |
| After the intent, and at the export | 50 | 2% |
| Paths | 20 | 1% |
| five one-off headings | 143 | 7% |

`Reading the world back` covers the same subject as the `pgm-board` skill's lookup
table, which does it in about thirty rows with a *what not to use instead* column. The
raw form and the distilled form sit beside each other and a run loads both.

### It is not an API reference, and the redundancy is not with the API

Only 4% of the file is fenced code or route lines. It names 29 routes against the live
API's 174 paths, and its own title is *what the API does not say*. The hypothesis that
it redundantly documents a findable API does not survive measurement.

### It names 21 past maps, 44 times

The technique cards name none. A document read first that cites `opus5-tarnfell`,
`fable-millrace-revamp` and nineteen others by slug is an invitation to go and open
them, and each one costs a context window it does not have.

### The reading list is a whole context window

`AUTHORING-BRIEF.md` §4 tells an agent to read ten documents before drawing.

| Document | Words |
|---|---:|
| `pgm-studio/docs/tools/sketch.md` | 31,684 |
| `pgm-studio/docs/generator/model.md` | 20,505 |
| `pgm-studio/docs/world-export/decoration.md` | 17,352 |
| `pgm-studio/docs/world-export/relief.md` | 16,037 |
| `pgm-studio/docs/tools/plan.md` | 12,374 |
| `pgm-studio/docs/gameplay/match-flow.md` | 12,199 |
| `pgm-studio/docs/tools/library.md` | 11,292 |
| `pgm-studio/docs/tools/capabilities.md` | 9,418 |   ← retired since; see below
| `pgm-studio/docs/gameplay/approaches.md` | 3,899 |
| `pgm-studio/docs/tools/flow.md` | 3,530 |
| **total** | **138,289** |

That is roughly 180,000 tokens, before `GENERATION-NOTES.md`, before the skills, and
before a single request is made.

**`capabilities.md` no longer exists.** It was retired in `pgm-studio` as `RP23`: what the system
can be asked for is answered by `/api/openapi/v1.json`, `GET /api/rules` and
`GET /api/map/{slug}/state`, and the three things only it held moved to `flow.md`, `plan.md` and
`tools/seeds/README.md`. Its row above is left as measured.

### The budget an agent is handed is itself wrong

`pgm-board-warmup` states the documents come to *"~82k tokens — 41% of a 200k window"*.
The list above is about twice that. An agent told to plan against 82k and then handed
180k has been given a false premise as its first fact.

### The technique cards are the format that works

The six that predate this session come to 349 lines and 3,986 words between them,
under an eighth of `sketch.md` alone. Each states its variants side by side in one
world, commits the text reads that prove its claims, names zero past runs, and carries
a section headed **The one mistake**.

| Card | Lines | Words |
|---|---:|---:|
| relief-on-shapes | 127 | 1,393 |
| combined-shapes | 50 | 615 |
| flat-ground | 53 | 574 |
| polylines | 44 | 495 |
| curved-outlines | 37 | 459 |
| ramp-and-stair | 38 | 450 |
| hollows *(added 2026-09-19)* | 225 | 2,676 |

---

## 2. The diagnosis: three problems, not one

### Volume: the reading list is larger than the context it is read into

An agent that obeys the brief spends most or all of its window before it has a plan.
Everything it then learns competes with what it was told to memorise.

### Form: these are reference works, organised by subject

`sketch.md` and the rest are written for a person who browses to the part they need,
so they are complete and ordered by tool. An agent reads in one gulp and needs answers
in the order the work happens, which is a different document.

### Provenance: law, measurement and anecdote are unmarked and interleaved

Nothing in `GENERATION-NOTES.md` says whether a paragraph is a rule that always holds,
a number measured once, or a story about one board. A reader cannot tell what to obey,
and neither can its author — the file is past the size at which anyone knows what is
in it.

---

## 3. What is *not* the problem

**The long documents are good and should not be deleted.** They are accurate, they are
the whitepaper's source, and the fault is that they sit on a reading list rather than
that they exist.

**The API does not need documenting again.** `/api-docs`, `/api/openapi/v1.json`,
`GET /api/rules` and `GET /api/rules/terms` answer the routes, the fields, the rule
texts and every scored term's band. An agent that knows those four exist does not need
them transcribed.

**The prose gate is working and should stay.** `tools/prose-check.py` is why no
paragraph in the corpus is bloated. It governs paragraphs and cannot govern documents,
which is exactly the gap this handover describes.

---

## 4. Opinion: split the corpus by *when it is needed*, not by subject

This section is a recommendation rather than a measurement.

### Tier one is a page, and it is the only thing preloaded

What must be in context before the first decision is the order of work, not an
explanation of any instrument. The author's own sequence is its spine: **gamemode,
name, size, the idea of the place, then the plan, then the relief, then the features.**
It does not need to say what relief is; it needs to say when relief is decided.

### Tier two is fetched on demand and nothing else

The four live routes above, plus the tool documents as things to open when a specific
question arises. A reading list becomes a lookup.

### Tier three is the cards, and there are not enough of them

Seven exist, covering outlines, overlapping shapes, polylines, flights, relief scope
and hollows. Missing at least: building on and into a slope, water, the objectives and
their clearances, and what a theme's four buckets do.

### The first task is classification, not rewriting

Go through `GENERATION-NOTES.md` and mark each paragraph **law**, **measurement**, or
**one run's story**. It can be done from the 209 bold lines alone. Until it exists
nobody knows what the file contains, and any rewrite is guesswork.

### The map names go regardless of what else happens

Forty-four citations of twenty-one slugs, in the document read first, is the one change
that needs no further thought.

---

## 5. What this session's three boards demonstrated

Three destroy boards were authored by agents against three different briefs. The
failures were **opposite** and the cause was the same: nothing told them what a map is
or in what order to decide it.

### `opus5-whitegape` — over-commitment

Fifteen shapes, two made layers, five relief marks, three pushes, five themes, ten
dressing styles and nineteen props on 60×88 blocks. Every instrument the agent had
learned about was used once.

**Fourteen of its fifteen shapes are `level` + `relief_scope: "exclude"`.** Every yard,
dock, flight, ramp, revetment and kerb is a plate pinned at a stated absolute height
and held out of the solve; the fifteenth is a `sink`. Nothing could ever sit lower than
anything else, which is why the board reads as objects laid on terrain rather than as a
place.

### `opus5-fallowgate`, first pass — under-commitment

Given a hard instrument budget it spent 14 of 25 and the board came out inert: no coast
edits, no bend, two relief marks producing one gradient, and a heightmap printing
byte-identical rows thirteen times.

The budget had constrained the wrong things alongside the right ones. Cutting props,
layers and houses was correct; capping the coast and the relief was not, because those
two are what makes ground read as ground and neither is what made Whitegape bad.

### `opus5-fallowgate`, second pass — the size line was the brief's error

The brief said *eighty by eighty blocks of ground* and meant per side. Read as the whole
footprint it left each team 35 blocks deep and put `GO3` and `GO4` structurally out of
reach. At 56×160 the same plan evaluates at score 0 with an empty violations array.

With the coast and relief ceilings raised the hillside's sixteen rows became sixteen
distinct rows. The board is still dull, which is the honest cost of very few words.

### The lesson for tier one

A budget is a real instrument and it worked. It must be expressed as *what the board
needs*, not as a count of keys, because a count cannot distinguish an instrument that
adds clutter from one that adds shape.

---

## 6. Studio defects found while doing this

These are filed in `pgm-studio`'s `BACKLOG.md`. They belong here because they are the
kind of thing the notes file should hold instead of run anecdotes, and because two of
them are reasons an authored board silently comes out wrong.

| Id | What it is |
|---|---|
| `WE128` | **Fixed and shipped.** A wool room whose only seam was under the ten-block corridor minimum got no entrance line and no cage door, because two sites re-derived a predicate that exists. |
| `WE129` | A house seats on the **lowest** column of its footprint and the footprint is then excavated to it, unbounded. A plan reaching into a pit sinks the whole building; `DR-SLOPE` measures the rise against the building's own height and stays silent. |
| `WE130` | `POST /sketch/seats` reports the yard beside a quarry as a legal seat, because the rules that read the built world belong to the dressing pass and not to the query. |
| `RP72` | **The most serious.** One unbindable field discards the *entire* intent at 200 with no finding and no warning header, and `preflight` then answers `exportReady: true` on a map with no teams, no spawns and no objectives. |
| `RP73` | `crown` is signed in world space, so on a negative push a positive crown fills the floor back in. The docstring is written from a raising push, and the editor defaults it to 2 where the record defaults to 0. |

`RP72` is worth restating because it is the corpus problem in one line: a document that
spends 138,000 words before an agent draws is also a document that never gets round to
saying *check that what you posted came back*.

---

## 7. What to keep

**The prose gate.** One paragraph, one claim, claim first, enforced by a script.

**The technique card format.** Short, variants side by side in one world, committed
text reads, no run references, and a section naming the one mistake.

**The recording proxy.** `scratchpad/setup/proxy.py` logs every call to JSONL. An
agent's self-report and its wire trace are different documents and only one is evidence.

**The three stopping points.** Report after the massing, after relief and paint, and
after the first build. Two of this session's four known failures were caught inside a
run rather than after it.

**Measuring before keeping.** `POST …/sketch/relief?heights=true` answers the solved
surface without a build, so an instrument's worth can be asked in seconds rather than
in four drives.
