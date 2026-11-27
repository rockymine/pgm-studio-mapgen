# 02 — The studio's turning points, mid-August to late November 2026

Research for the history film. Subject: `rockymine/pgm-studio` (ASP.NET Core + Blazor WASM, MariaDB).
Read from the local clone at `/home/user/pgm-studio` on 2026-11-27: `main` at `5df92a35` (2026-11-14,
2,646 commits) and branch `origin/ccr-875c17a4-2yjgux` at `ed354f43` (2026-11-23, 2,696 commits). The first
commit is `f499ea88` "add README" on 2026-06-12. Every hash, date and quote below was read from `git log`,
`git show`, `FEATURES.md` or `docs/` in this session. Where a statement is my interpretation and not a
recorded fact, it says so ("reading:" or "uncertain").

Dates are author dates (`%ad`, short). The repository squash-merges pull requests into `main`, so many
events appear twice: once as a branch commit, once as the squashed PR on `main`. The timeline cites the
first.

---

## Timeline (verified events)

Two context rows from before mid-August come first, because the generator they name was built in July.

| Date | Commit | What happened | Why it mattered |
|---|---|---|---|
| 2026-07-04 | `7b4603cc` | "G32 first slice: composer envelope + team-unit grower" | Context. The composer (the layout generator) starts. 76 of the generator-related commit subjects fall in July, five in August. |
| 2026-07-14 | `deb62961` | "docs: consolidate map generation into one canonical doc" — `docs/generator/model.md` is born | Context. The hub / wool approach / frontline / mid model gets its single source of truth. |
| 2026-08-11 | `755ab378` | "A shell became a house — six roofs, a zoned floor, windows, a porch (G34d)" | Houses become a parametric system. Flat, Gable, Hip, Gambrel, Shed and Saltbox roofs come from one height-field formula. |
| 2026-08-11 | `3c82ff1a` | "G34g — a building is a stack of storeys" | Storeys. The start of the wings, porches and beams that followed. |
| 2026-08-12 | `c9ea46d6` | "Measure 75 hand-built trees, and find the grown crown hangs off nothing" | The tree-showcase world becomes ground truth, and the generated tree is measured as broken. |
| 2026-08-12 | `4cf8b107` | "The relief solver lands in Geom, and two claims about it were wrong (S41, S42)" | The relief (terrain heights solved from marks) arrives in the shared leaf that the browser also runs. |
| 2026-08-12 | `1296cbc7` | "The relief becomes visible: contours traced on the server (S45)" | Terrain gets pictures of its own. |
| 2026-08-13 | `6eec9b8b` | "A floating goal is the design, and gameplay questions have an oracle (B104)" | The **ask-the-author rule** is born from a false alarm: an agent claimed every generated destroy map was unwinnable. |
| 2026-08-13 | `d91b6be6`, `715f4f59` | "One document per tool, written from the ground up (B111)"; generator and shapes docs | `docs/tools/` is written: one document per tool, endpoints included, so an agent can act on it. |
| 2026-08-13 | `10bb8505` | "The instructions file keeps the instructions, and gains the rule against rot" | `CLAUDE.md` gets its "documents rot silently" rule. |
| 2026-08-14 | `738d81fb` (file creation) / `724e18d7` | `docs/gameplay/approaches.md`; "Two claims in approaches.md are the author's, not the review's" | The one document made of the author's claims about play, marked [author] or [review]. |
| 2026-08-15 | `50caa477` | "B191: one Finding, and one way every gate in the studio says no" | Seven finding types and six refusal envelopes collapse into one `Finding` and one `{error, message, findings[]}`. |
| 2026-08-15 | `f131ee21` | "Every rule the studio can cite can be asked about (B219)" — `GET /api/rules`, 125 rules | Rules become something a caller can ask about by id. |
| 2026-08-17 | `c673f675` | "B249: an author can force a build past its refusals, and an agent cannot" | The first explicit split between what an author may do and what an agent may do. (The override was later withdrawn as a question, `docs/backlog-strategy.md`.) |
| 2026-08-19 | `88bc0baa` | "The API describes itself…" — `GET /api/openapi/v1.json` and `/api-docs`: 131 paths, 167 operations, 61 schemas | **The API becomes self-describing.** The commit also records how hard the studio was for agents to drive. |
| 2026-08-19 | `86bfc2f2` (file creation) | `docs/architecture.md`, "How the studio is driven" | It names the two audiences: a person in the browser, an agent over `/api`. |
| 2026-08-22 | `8b0c24b3` | "WS6: the world read-backs answer over HTTP" | Every render of a built world becomes a route. Before this they were CLI flags only. |
| 2026-08-27 | `13c062ec` | "TL4, G158, B47: the library ships with six finishes, and seeds itself" | The material/theme library gets seeded content. |
| 2026-08-31 | `949e9b6c` | "The board's own reading: which entries are defects, and what order drains them" (`docs/backlog-strategy.md`) | The task board becomes something that is measured. |
| 2026-09-01 | `7e1c5a47` | "B200: the Theme phase authors a band stack, on the axis and the ending it states" | Band stacks (layered paint by depth, height and so on) can be authored in the UI. |
| 2026-09-02 | `378b2d58` | "WE72: a copied tree, cut out of a world and planted as a recipe" (co-author Fable 5.1) | The answer to "trees are hard": copy the author's hand-built trees block for block. |
| 2026-09-02 | `0976de79` | "The reads a model subtracts from: sections, transects, heightmaps, slopes, walks, themes and claims as text" | **Text twins of pictures**: `?format=text` on renders, so a model can read numbers instead of looking at an image. |
| 2026-09-05 | `1e7d9aa8`, `9710cd4a` | "WE97 — an angle mask: a band stack read by how steep the ground is"; "read the grade, not the stair" | **The slope axis.** Paint can tell a 45° hillside from a meadow. |
| 2026-09-09 | `43de43aa` | "A block is a texture as well as a colour, and the palette says so" | The first step from flat colours toward textures. |
| 2026-09-09 | `e6e9e231` | "Three rules stop reporting things that are not true" | Recorded example of rules raising false findings: one board went from 14 findings to 6. |
| 2026-09-10 | `6b0b3f09` | "Remove the grown tree: a recipe is a species or a body" | **The procedural tree is given up**: 496 lines of `Geom` deleted, and migration `M0035` drops its columns. |
| 2026-09-22 | `c99de32c` | First commit co-authored by "Claude Opus 5.5" ("TN22: PL17 passes a wall at a T") | Model change. From October, Opus 5.5 writes almost all commits. |
| 2026-09-25 | `75ee07a3` | "CI: run the repository's own gates on every pull request" | GitHub Actions CI starts: build, tests, e2e. |
| 2026-09-26 | `f7587f86` | "RP75: sign in with Discord, bound to a Minecraft account by invitation" | Accounts. |
| 2026-09-26 | `8c6655a6` (file creation) | `docs/access.md` | Who may write, and how a request is signed in. |
| 2026-09-27 | `3be000d5` | "WS76: the board from a player's eye, in the game's own textures" — `GET …/render/eye` | **Real block textures.** The 1.8.9 client jar is read with the EULA accepted, checked against its SHA-1 and never shipped. |
| 2026-09-27 | `a65ab7a9` | "TS110, WS78: the board in game, in the studio" | The eye view shows inside the browser tool. |
| 2026-09-28 | `de77dc1a`, `10fde9db` | "RP76: a token for a caller without a browser"; "a token acts as a member and issues no token" | **The agent gets a key.** A Claude Code session can drive the deployed studio. |
| 2026-09-28 | `71180895` | "RP79: builds wait their turn in a queue, and the thread pool starts at 16" | The build queue: 3 at once, 1 per caller, then 429 with `Retry-After`. |
| 2026-09-28 | `31033891` | "RP78: the studio deploys itself from a green main" (`docs/deployment.md`) | **pgmstudio.de deploys itself** from green `main`. Its message says the site "has run since RP76 on a deploy script that lived only on the server". |
| 2026-09-28 | `fd216dfd` | "TG1: the Generator browses a composed-board library" | The generator becomes a feed: 500 boards per size band and symmetry, composed ahead of time. |
| 2026-09-30 | `38267335` | "RP91: a map is stored from its source, and the refinement is the studio's" | `PUT /map/{slug}/source`, one headless authoring call. This is the core of agent-driven authoring. |
| 2026-10-01 | `a021d25d` | "RP95: the studio serves a Python kit written from its own schema" — `GET /api/kit.py` | The studio hands an agent its own client library. |
| 2026-10-01 | `6975a049` | "WS80: the board in the round is drawn by the studio — render/isometric, render/xray and the void scan" | Isometric and underground (x-ray) pictures. |
| 2026-10-02 | `92528268` | "TS139: CI sweeps the browser with Minecraft's block textures" | Textures become part of the gate. |
| 2026-10-04 | `c8a67337` | "RP99: every word the rules use is defined once, and served" — `GET /api/glossary` (226 terms per FEATURES) | A served vocabulary for agents and screens. |
| 2026-10-06 | `48a9a6de` | "Draw library houses, roofs, storeys, porches, trees and boulders with block sprites" | Library cards drawn in textures. |
| 2026-10-06 | `da272d55` | "Rebuild the home page on the Design A layout: in-game map pictures…" (first use of `render/picture`) | The front page shows maps as they look in game. |
| 2026-10-10 | `ad426a2b` | "A minimal rules policy, for measuring what the rules cost an author" (`Rules:Mode=minimal`) | A switch made to measure the rules' cost. Same date as the experiment `docs/pgmvox-port.md` cites. |
| 2026-10-13/14 | `36267d96`, `7c36bda5`, merged as `d9abee14` (PR #59, 2026-10-14) | Capture the Flag, conquest, score boxes and damage; "WS86: the walk takes a running jump" | Beyond CTW and DTC. Per `pgmvox-port.md`, this "closed most of the gap". |
| 2026-10-15 | `2ed975bc` | "The pgmvox port: a programme for bringing the freeform library into the studio" | **The rethink.** A nine-phase programme with the author's decisions D1–D23. |
| 2026-10-15 | `7782a958` | "Rules: a third level, the measure (RP128)" | A rule can now be a measure that never refuses, beside hard and hint. |
| 2026-10-15 | `16da48c1` | "Renders: the x-ray draws the underground, and both isometric reads take a box (WS90)" | Phase 0: a framed picture per place. |
| 2026-10-15–17 | `1fa91485`, `4af3da5a`, `c99dd49c` | Play pieces carry ids; "Every play piece is drawn, picked, dragged and turned in the sketch"; "WE166: a room's building is a house" | Phase 1: spawns and wool rooms become objects that can be dragged on the ground. |
| 2026-10-18 | `eb674bb5` | "TG7: the generator hands over a sketch, and pinning goes" | The composer's output becomes an ordinary sketch, one shape per box. |
| 2026-10-18 | `cc4cd3de`, `fcc426f6` | "The plan retires as a level (RP131)"; "RP131: a map's findings read its sketch, never its plan" | **The rectangle plan stops being a level.** The Plan tool goes, and stored plans are kept read-only as history. |
| 2026-10-19 | `cef55cae` | "Close Phase 1; open Phase 2 with the layer document on paper" | |
| 2026-10-23 | `49fe089a` | "pgmvox port: the ground as shapes, modifiers and placements (D16–D21)" | The new ground model is decided. |
| 2026-10-24 | `fbdbc862`, `16864f7f` | "The modifier stack runs over the built ground, and Terraform lists and edits it"; "The group relief is retired: the modifier stack is the only terraforming (TS206)" | **Terrain is rebuilt** as ordered landform operations (Hill, Ridge, Canyon, River, Lake…). The August relief solver gives way. |
| 2026-10-24 | `eedbe54e`, `d043601a` | "WE170: paint rules, first match winning"; "WE169: a theme's surface thins with the slope…" | Phase 3: the ground is painted by what it is. |
| 2026-10-25 | `1e10a4c6`, `c8fd98e5` | "TS140: carves — a tunnel, a chamber and a shaft"; "TS212: primitives in the block grid — box, wedge, cylinder, sphere, torus and the natural arch" | Phase 4: underground space and solids. |
| 2026-10-26 | `1f8845bb`, `c75dda50` | Phase 5 on the board; "Every stamp is switched per piece, and the float check is ported (WE174)" | |
| 2026-10-26 | `9e375306` | "Every screen text has one channel, one form and a gate (C108)" | UI language. |
| 2026-10-27 | `8f1f6c63`, `1f422e17` | "Phase 6 opens with the house fields…"; "WE179: wooden doors on houses and wool rooms" | Phase 6, houses. |
| 2026-10-28 | `5c73a5b7` | "C112–C114: Direction C — Geist, a zinc palette, a folding studio bar and narrow windows" | Visual redesign of the browser studio, with phone-width layouts. |
| 2026-10-29 | `db1a7958` | "Backlog audit: seven fixes…" — "Eight agents checked all 111 BACKLOG entries against the code" | The board is audited by parallel agents. This is on the newest branch. |
| 2026-11-04 | `bb53150a` (main `2e72a4a9`, PR #91) | "PG18 and the author's second answers: the board's focus is its bugs" — "the pgmvox programme has shipped or parked every phase" | The focus turns from capability to bugs. |
| 2026-11-13 | `96c8a868`, `371e6935` | "The author's third answers: the backlog's fixes before new capabilities"; "The author froze the layout generator" | **New capabilities pause, and the generator is frozen.** |
| 2026-11-14 | `5df92a35` (PR #98) | "Undo stays in its phase, Review opens Configure, room doors follow their style, house cards show their footprint, water steps down in reaches" | The last commit on `main`. |
| 2026-11-23 | `0ee7a8ad`, `ed354f43` | Branch only: "The board states the door and schematic rulings"; "Board: doors as the author means them; schematics backfill rule" | The newest rulings: hand-built props become labelled schematics, and a door appears only where it is stated. |

---

## Commit activity per week (the activity curve)

The counts cover all commits reachable from `origin/ccr-875c17a4-2yjgux`, which contains all of `main`. The
second column includes merge commits; the third excludes them. ISO weeks, Monday to Sunday.

| Week | Dates | Commits | Non-merge |
|---|---|---|---|
| W24 | Jun 08–14 | 35 | 35 |
| W25 | Jun 15–21 | 156 | 156 |
| W26 | Jun 22–28 | 63 | 63 |
| W27 | Jun 29–Jul 05 | 114 | 114 |
| W28 | Jul 06–12 | 60 | 60 |
| W29 | Jul 13–19 | 174 | 174 |
| W30 | Jul 20–26 | 105 | 105 |
| W31 | Jul 27–Aug 02 | 122 | 120 |
| W32 | Aug 03–09 | 103 | 103 |
| **W33** | **Aug 10–16** | **377** | **356** (the peak: houses, trees, relief, tool docs, one Finding, rules API) |
| W34 | Aug 17–23 | 176 | 176 |
| W35 | Aug 24–30 | 120 | 117 |
| W36 | Aug 31–Sep 06 | 169 | 168 |
| W37 | Sep 07–13 | 64 | 64 |
| W38 | Sep 14–20 | 61 | 60 |
| W39 | Sep 21–27 | 127 | 109 |
| **W40** | **Sep 28–Oct 04** | **261** | **215** (deploy, tokens, queue, kit.py, glossary) |
| W41 | Oct 05–11 | 95 | 71 |
| W42 | Oct 12–18 | 142 | 123 (pgmvox port begins; the plan retires) |
| W43 | Oct 19–25 | 50 | 40 (modifier stack, carves) |
| W44 | Oct 26–Nov 01 | 70 | 61 |
| W45 | Nov 02–08 | 19 | 14 |
| W46 | Nov 09–15 | 31 | 25 (freeze) |
| W47 | Nov 16–22 | 0 | 0 |
| W48 | Nov 23–29 | 2 | 2 (branch only) |

By month: June 258, July 513, August 861, September 469, October 543, November 52.

**Who wrote the commits** (the `Co-Authored-By` trailer, per month; rows of 3 or more):

| Month | Trailers |
|---|---|
| 2026-06 | Opus 4.8 255 |
| 2026-07 | Opus 4.8 312 · Fable 5 121 · Opus 5 73 · Opus 5 (1M) 4 |
| 2026-08 | Opus 5 461 · Opus 5 (1M) 187 · Opus 4.8 67 · bare "Claude" 47 · Sonnet 5 30 · Fable 5 26 · none 25 · "Claude Sonnet" 14 |
| 2026-09 | Opus 5 180 · Opus 5.5 176 · Opus 5 (1M) 74 · none 27 · Fable 5.1 9 |
| 2026-10 | Opus 5.5 414 · none 90 · Sonnet 5.5 32 · Sonnet 5.5 + Opus 5.5 7 |
| 2026-11 | Opus 5.5 36 · bare "Claude" 9 · none 7 |

Date ranges (first to last trailer): Fable 5 from 2026-07-02 to 2026-08-16; Opus 5 from 2026-07-25 to 2026-09-22;
Sonnet 5 from 2026-08-13 to 2026-08-29; Opus 5.5 from 2026-09-22 to 2026-11-23; Sonnet 5.5 from 2026-10-02 to
2026-10-25. Uncertain: "none" rows are mostly merge commits or human-made ones, and I did not separate the two.

---

## Beat 1 — The generator and the composer, and how a map is built step by step

**What the record says.** The composer was built in July (`7b4603cc`, 2026-07-04). By mid-August it was being
documented and refined rather than invented. `docs/generator/model.md` describes it. A request (players per
team, team count, symmetry, seed — no geometry) becomes a budget. The budget is allocated into typed box
footprints, and the boxes are filled hub first. The mid band is carved from the frontline faces, the board is
assembled into a plan, the plan is derived back into islands, links, enclosed voids and fronts, and a gate
judges the result. A rejection resamples the whole attempt, and sixty attempts are allowed. The figure in §1:

```
request → budget → allocate (boxes + joints) → fill (hub-first) → carve the mid
        → assemble → derive → gate ──accept──► plan → realize
                               └────reject───► resample
```

The vocabulary is hub, wool approach (the "wool" compound, §4.6), frontline box, mid band, crossing and
defence walls (§5.13–5.14). The model states its own limit, which is the "what that limits" of the brief.

**The rethink inside the generator's own history.**

- **2026-09-28 (TG1):** boards are composed ahead of time into a library, "500 for every size band and
  symmetry", and the Generator tool browses that feed.
- **2026-10-18 (TG7):** a candidate is handed over as a sketch with "one shape per box — the hub, the front
  line, each wool approach and the spawn, named `hub-9`, `wool-a-9`" (FEATURES).
- **2026-10-18 (RP131):** the plan level itself retires.
- **2026-11-13 (`371e6935`):** "The author froze the layout generator: nothing changes what the composer
  makes."

**Terrain on top of the layout went through two designs.**

1. **The relief solver (August).** Marks are solved together into heights (`4cf8b107`, 2026-08-12), with
   contours traced on the server (`1296cbc7`).
2. **The modifier stack (from 2026-10-24).** It replaces the relief: "The group relief is retired: the
   modifier stack is the only terraforming (TS206)". Ordered operations — Hill, Hollow, Level, Roughness,
   Ridge, Butte, Spire, Scarp, Canyon, Profile, River, Lake, Coast, Road, Lumps, Shatter, Gullies, Warp — run
   in list order over masks (`docs/pgmvox-port.md`). Carves (tunnel, chamber, shaft) and solids followed the
   next day.

**The pipeline a time-lapse could show**, as the studio now runs it. Sketch phases are from `docs/tools/sketch.md`,
hand-offs from `docs/tools/flow.md`.

| Step | What changes | What draws it |
|---|---|---|
| 0. Compose (optional) | a board from size, symmetry and seed | `/generator` feed (`GET /compose?players=&symmetry=&from=&count=`), each card's picture of the composer's pieces; `POST /compose/map` makes a map of a card. Shape vocabulary: `GET /shapes/catalog` (SVG per card), `GET /shapes/probe?family=&w=&h=…` |
| 1. Places | places with reasons, notes as threads | Sketch, Draw → *Places* step; `GET /map/{slug}/places` |
| 2. Ground | shapes on layers | Sketch, Draw → *Ground*; `POST /map/{slug}/sketch/columns`, 3-D preview |
| 3. Layout | spawns, wool rooms, goals, build areas, walls placed and dragged | Sketch, Draw → *Layout*; `GET /map/{slug}/intent/pieces` |
| 4. Terraform | modifier stack, one operation at a time | Sketch → *Terraform*. **`?step=` on the reads** (`sketch/relief?step=`, `sketch/columns?step=`) answers the ground after any one modifier, which is a natural time-lapse; `POST …/sketch/modifiers/changes` says what each modifier moved (TS207/TS208, 2026-10-24) |
| 5. Paint | themes, band stacks by depth, height, inward and slope, paint rules | Sketch → *Palette*; `POST …/sketch/paint`, `render/surface`, `themes/census` |
| 6. Structures | houses on rooms, wings, roofs, doors | Sketch → *Layout* (a room's house) and *Decoration*; `POST …/sketch/seats` |
| 7. Dressing | trees (copied), boulders, flora, paths | Sketch → *Decoration*; `POST …/sketch/dressing` |
| 8. Review | cameras, notes | Sketch → *Review* |
| 9. Build | rasterize to a world; configure the play | `POST …/sketch/finish`, then `/maps/{slug}/configure` |
| 10. Look and export | the world and `map.xml` | `render/topdown` (subjects ground, structure, made, foliage, objectives, combined), `render/heightmap`, `render/section`, `render/isometric`, `render/xray`, `render/eye`, `render/picture`, `render/walk`, `report`, `diff`; `GET /map/{slug}/xml`, `GET /map/{slug}/export` |

**Quotes.**

> "The vocabulary below — hubs, lanes, frontline boxes, wool forms — is *one* way to think about a CTW board
> … It is an **intentional abstraction whose product is a low-fidelity prototype of a layout** … A map whose
> form is organic rather than rectilinear falls outside it: the Thunder series is the worked case … **That is
> a limitation rather than a defect, it is the author's stated position, and it stays.**"
> — `docs/generator/model.md`, introduction

> "The author froze the layout generator: nothing changes what the composer makes."
> — commit `371e6935`, 2026-11-13

**What we could show.**

- The `model.md` §1 figure.
- `/generator` cards.
- `/catalog` shape cards.
- One map stepped through its modifier stack with `?step=`.
- `diff` between two changes of one map.
- `render/isometric`, plain and with `box=` framed on one place.

---

## Beat 2 — Houses work, trees are hard

**Houses.** The house became a parametric system in one week:

- **2026-08-11:** six roof forms from one formula, a zoned floor, windows and a porch (`755ab378`), and the
  building as a stack of storeys (`3c82ff1a`).
- **2026-08-12:** a village of five houses (`9061d433`).
- **2026-08-14/15:** wings with their own roof and joints (G172, G184–G186).

By 2026-10-15 the library held 61 house styles (`3bb36ca1`, "the library's house count is 61"; FEATURES: "yellow,
orange and brown clay cottages join the sixty-one"). Later steps:

- **2026-10-17:** a wool room's building is a house (WE166, `c99dd49c`).
- **2026-10-27:** wooden doors (WE179) and a head course on every storey (WE176).
- **2026-11-14:** a room's door width follows its style (WE152).
- **2026-11-23 (newest branch):** the door rule restated as the author means it: a door is placed "only where
  it is stated".

The pgmvox port's open question is about houses: "pgmvox's ten-slot archetype made its houses look right and the
studio's 61 styles make its houses varied; the archetype as a library row … has not been tried."

**Trees.**

1. **Early August:** the "grown tree", a recursive skeleton with Catmull-Rom limbs (`de4e2ba1`, `20c87902`,
   2026-08-02).
2. **2026-08-12:** 75 hand-built trees on the author's tree-showcase world are measured (`c9ea46d6`). The
   grower fails: "1516 of 4020 never touch their branch. Below height 12 the crown stops cohering entirely and
   42-76% of it floats free."
3. **2026-09-02:** the "copied" tree is added, cut out of a world block for block and planted as a recipe
   (WE72, `378b2d58`).
4. **2026-09-10:** the grown tree is deleted on the author's ruling (`6b0b3f09`).
5. **Today:** the corpus holds "95 author-built trees … in 20 bands" (`docs/world-export/tree-corpus.md`), and
   boards plant the author's own trees, crediting their builder rockymine (WE145, 2026-09-28).
6. **Newest ruling (branch, 2026-11-23, WE134):** "anything a model builds itself (a truck, a balloon) is a
   **schematic** … labelled as one".

**Quotes.**

> "`TreeForm.Grown` built its trees from a recursive skeleton and they came out broken; the author's ruling is
> that the form goes rather than gets a knob."
> — commit `6b0b3f09`, 2026-09-10

> "Hand-built puts 30.3% of leaves against wood and 10.6% on a diagonal, at 6.2 occupied neighbours each … The
> grower manages 18.7% and 0.5% at 13.1 neighbours — a solid mass held on at a few points rather than lace."
> — commit `c9ea46d6`, 2026-08-12

**What we could show.**

- `/library/{Kind}` pages for houses and trees, whose cards have been drawn in block sprites since
  2026-10-06 (`48a9a6de`).
- `render/eye?look=x,z` on a house.
- The tree-showcase world, which sits in `pgm-studio-mapgen/corpus/tree-showcase`.
- A side by side: a grown tree from git history before `6b0b3f09` against a copied one. This needs a rebuild
  at the old commit (uncertain whether it is feasible).

---

## Beat 3 — Texturing: from plain colours to real textures

**What the record says.** The paint system grew in four steps:

1. **2026-08-01:** terrain painting is designed with rim, wall, surface and fill "buckets" (G157), and
   unthemed ground stays stone.
2. **2026-08-27:** the library seeds six finishes.
3. **2026-09-01:** band stacks can be authored in the Theme phase.
4. **2026-09-05:** the slope axis (WE97/TP24). FEATURES says of it: "It is the only thing in the model that
   tells a 45-degree hillside from a flat field".

**The textures moment.**

- **2026-09-09:** "A block is a texture as well as a colour" (`43de43aa`).
- **2026-09-27 (`3be000d5`, WS76):** `GET …/render/eye` draws "the built world in perspective, from a player's
  eye height, with Minecraft's 1.8 block sprites". The sprites come from the 1.8.9 client jar, downloaded only
  once `Textures:AcceptMojangEula` is set, checked by SHA-1 and never shipped. A studio without them answers
  `RQ10` at 503.
- **2026-09-27, same day:** WS78 brings the eye view into the studio.
- **2026-10-02:** CI runs the browser sweep with real textures (TS139).
- **2026-10-06:** library cards and the home page show "in-game map pictures" (`render/picture`).
- **2026-10-24:** paint rules where the first match wins, and soil that thins with the slope (Phase 3).

**Why it mattered**, from the commit itself:

> "Every read the studio answers draws a block as one colour, which is right for a plan and wrong for a
> finish: two noisy blocks of one colour are one calm grey in a flat picture and static on the ground, and
> that is the fault authors keep making and no read could show."
> — commit `3be000d5`, 2026-09-27

**"Map walls" (uncertain).** The phrase does not occur in the studio repository or its docs. Three candidates:

- The painter's **Wall** bucket (`docs/world-export/terrain-painting.md` §2, "Wall — the exposed riser") and the
  "wall-runs that wrap the void-facing perimeter (TP13)".
- The approach wall as a line of bedrock at any angle (WE167, `682dd0bd`, 2026-10-16).
- Something in `pgm-studio-mapgen`.

Ask the author (see the questions at the end).

**What we could show.**

- `render/topdown?subject=ground` (flat colours) against `render/eye` of the same spot.
- `render/eye?flat=1` draws "the same frame one colour a block", which is a built-in before/after.
- `GET /map/{slug}/incline?format=text`.
- `themes/census`.
- The Palette phase at `/maps/{slug}/sketch`.

---

## Beat 4 — The API as the product

**What the record says.** The studio's documents describe two audiences: "A person drives it through a Blazor
client that renders panels and a canvas; an agent drives it through `/api` and a CLI, and everything it can
learn about the map it has to learn from a response body" (`docs/architecture.md`). The surface was built in
this order:

| Date | What | Commit |
|---|---|---|
| 2026-08-13 | one doc per tool, written "for an agent as much as a person", endpoints included | `d91b6be6` |
| 2026-08-15 | one `Finding` and one refusal envelope; `GET /api/rules` (125 rules) | `50caa477`, `f131ee21` |
| 2026-08-19 | `GET /api/openapi/v1.json` + `/api-docs` (131 paths, 167 operations, 61 schemas) | `88bc0baa` |
| 2026-08-22 | every world read-back as an HTTP route | `8b0c24b3` |
| 2026-09-02 | text twins (`?format=text`) of every picture read | `0976de79` |
| 2026-09-02 | a finding states its edit where the fix is mechanical | `29e7ae54` |
| 2026-09-28 | tokens for callers without a browser | `de77dc1a` |
| 2026-09-30 | `PUT /map/{slug}/source` — "The authoring call for a headless caller" (`flow.md`) | `38267335` |
| 2026-10-01 | `GET /api/kit.py`, a Python client generated from the schema | `a021d25d` |
| 2026-10-04 | `GET /api/glossary`, 226 terms | `c8a67337` |

**Why.** The same commit that made the API self-describing measured how undrivable it had been:

> "tools/drive.py is the seventh driver written against the API and its README says what the six before it
> did: read the status code and threw the findings away. … the brief requires fifteen documents read in order;
> the errata file is 47 KB. GENERATION-NOTES §11 is the sharpest line in it — 'every fault below is one the
> author could not have seen, because each of them answers 200'"
> — commit `88bc0baa`, 2026-08-19

> "A refusal carries an id and one sentence about the document it was refused over. The id is stable forever,
> which is what makes it worth keying on — and nothing answered the other question a reader has on meeting
> one: what is SP7."
> — commit `f131ee21`, 2026-08-15

**What we could show.**

- `/api-docs` in the browser.
- `/rules` and `/glossary`, which are client pages.
- One refusal JSON with its rule id.
- `render/eye` beside its `?format=text` twin.
- `GET /map/{slug}/report`.
- The header of `GET /api/kit.py`.
- `/tokens`, the account menu's token page.

---

## Beat 5 — Rules and validation

**Growth.**

- **2026-08-15:** the rules API answers 125 rules, 66 of them layout rules parsed from
  `docs/generator/rules.md` (`f131ee21`).
- **Now:** my rough count of rule-id-shaped constants (`public const string X = "AB12"`) across `src/` is
  247 unique ids. That is not a verified catalogue size; the live `GET /api/rules` would give the true number.
- **2026-10-15:** a third rule level, `measure`, which "never refuses" (RP128). It follows D4, which sorts the
  rules into hard ("valid XML and pieces, nothing built inside a house, a sensible goal, float and reach"), hint
  and measure ("walks, distances, gap widths, front lines").

**The ask-the-author rule.** It was born on 2026-08-13 (`6eec9b8b`) after an agent "produced a confident,
filed, committed claim that every generated destroy map was unwinnable" (`CLAUDE.md`). The measurement was
right, and floating goals are PGM's design.

> "B104's claim that every generated destroy map was unwinnable is withdrawn … CLAUDE.md gains the rule the
> mistake argues for: a question about how a map plays is answered by asking the author, before a task is
> filed. The corpus says what authors did and the code says what the tool does; neither says what is correct."
> — commit `6eec9b8b`, 2026-08-13

**Rules raising findings they should not.**

- **2026-09-09 (`e6e9e231`):** "Three rules stop reporting things that are not true … The board that found
  these reported fourteen findings across the two surfaces and now reports six".
- **2026-10-04 (`0bfe6855`):** "Findings blame the caller only for the caller's mistakes (RP110)".
- **2026-09-25 (`919e1641`):** a rule reverted the same day: "Revert WS73: the place-only bridging answer loses
  the middle of real maps".

**What is not measured.**

- **No phase adds a playtest check.** `docs/pgmvox-port.md` uses the 10 October playtest as a measure, not a
  work list: "Of the faults the author found on 10 October, the studio would have caught nine, partly caught
  four, and not caught or could not have built seventeen" — and "no phase of this programme adds a playtest
  check."
- **The rules' cost.** `Rules:Mode=minimal` (2026-10-10, `ad426a2b`) exists "for measuring what the rules cost
  an author". I found no committed result in the studio saying which rule produced which gain. The results
  may be in `pgm-studio-mapgen/experiment/`, which I did not read.
- **The generator audit.** `docs/generator/audit.md` records where code and model disagree, with measurements
  from a scratch probe "re-verified against the code on 2026-07-27".
- **The verified defects.** `docs/backlog-strategy.md` opens its defect section: "Every defect on this board
  passes every gate the repository has … a defect nobody can fail on is a defect that comes back."

**What we could show.**

- `/rules` with a family filter.
- The Sketch's *Problems* list (TS238).
- A refusal with its rule id.
- The `CLAUDE.md` paragraph "Gameplay decisions have a human oracle".

---

## Beat 6 — The pgmvox port

**What pgmvox is.** pgmvox is "the Python library for freeform boards in `pgm-studio-mapgen`
(`freeform/lib/pgmvox`, 0.30.0 on 15 October 2026)" (`docs/pgmvox-port.md`). It keeps its place as the
laboratory: an operation is tried there on real boards and moves into the studio once two boards use it or the
author asks for it.

**Why the rethink.** The doc gives two measures:

1. The experiment of 10 October found that, at equal model, brief and twenty minutes, "the two tools made
   boards of comparable quality". The gap was down to spend ("Opus, hours per board, the author's review rounds
   and bespoke code") and to pgmvox's open vocabulary.
2. The studio's plan was "rectangles on a 5-block grid; no reasons". The goal became "a board built through the
   deployed studio that the author cannot tell apart, by quality, from one built with pgmvox."

What the author would notice after Phase 1: "boards that stop looking alike because none of them starts as
rectangles."

**The phases and their state** (`docs/pgmvox-port.md`, the FEATURES lines, and `bb53150a`: "the pgmvox
programme has shipped or parked every phase", 2026-11-04):

| Phase | Content | State |
|---|---|---|
| 0 | framed isometric/x-ray (WS90), rule tiers (RP128) | shipped 2026-10-15 |
| 1 | the sketch is the one document: play pieces, places, generator emits a sketch, plan retires | shipped 2026-10-15 → 2026-10-19 (`cef55cae`) |
| 2 | shapes, modifiers, ground; migration M0086 | modifier stack shipped 2026-10-24; doc says placements ("the rest of it") are "not built yet" |
| 3 | paint rules, lay, water, layer underside | "Phase 3 has shipped" (2026-10-24) |
| 4 | carves, primitives, walk through carved space | carves and primitives shipped 2026-10-25; galleries, bores and dragging a solid out (TS212) parked |
| 5 | control point and wall pieces (TS213/214), per-piece stamps and float check (WE174) | shipped 2026-10-26; world upload TC23 parked |
| 6 | houses: doors (WE179) and head course (WE176) shipped; posts, jetty, chimney and heading in backlog | partial |
| 7 | the grammar (seven styles) | no FEATURES line and no board entry found. Uncertain whether filed |
| 8 | made things | made layers exist in the sketch (`SketchLayout.MadeKind`); the schematic ruling is open on the branch (WE134) |

The doc records that "All twenty-three [decisions] are taken". Examples:

- **D1:** port to C#, not a service.
- **D3:** no beta. The new ground reaches the live studio after a clean migration dry run.
- **D9:** "48 of 64 maps on pgmstudio.de hold one [plan]"; they are kept read-only.
- **D11:** none of mapgen's 174 plan specs move.

**Quote.**

> "The goal is a board built through the deployed studio that the author cannot tell apart, by quality, from
> one built with pgmvox. Not the same board — the same ceiling."
> — `docs/pgmvox-port.md`

**What we could show.**

- The concept page linked in the doc (https://claude.ai/artifact/PXyATVHg1XQ12BWoBmYaes, not opened here).
- Terraform's modifier list at `/maps/{slug}/sketch`.
- `render/xray` of a carved tunnel.
- A before/after of one board: plan rectangles against a modifier-built sketch.

---

## Beat 7 — The browser studio and deployment

**The client.** The client is Blazor WebAssembly hosted by the API, and it has been there since the initial
import (2026-06-13, `7b30744a`, "ASP.NET Core + Blazor WASM port of pgm-map-studio"). Its routes today, from
the `@page` directives in `src/PgmStudio.Client`:

| Route | Page |
|---|---|
| `/` | home |
| `/maps` | the maps list |
| `/maps/new` | import a world |
| `/maps/{Slug}/sketch` | Sketch: Identity, Draw (Places, Ground, Layout), Terraform, Palette, Decoration, Review, History |
| `/maps/{Slug}/configure` | Configure: Import, Identity, World, Teams, Build, Wools, Monuments, Cores, Flags, Score, Match, Export |
| `/generator` | the Generator |
| `/catalog` | the shape catalog |
| `/library`, `/library/{Kind}`, `/library/{Kind}/{Entry}` | the Library |
| `/rules` | rules |
| `/glossary` | glossary |
| `/tokens` | tokens |
| `/join` | sign-up |
| `/admin/users` | users (admin) |
| `/design` | design |

Two tools are gone. The **Plan** tool was retired on 2026-10-18 (RP131). `CLAUDE.md`'s prefix table still lists
`TE` → `docs/tools/edit.md`, but that file does not exist, so the edit tool has no document today (reading: it
was likely folded into the entity routes; `flow.md` says a finished map's document "is changed through the
entity routes").

**Going live, all within three days.**

| Date | Commit | What |
|---|---|---|
| 2026-09-25 | `75ee07a3` | CI on every pull request |
| 2026-09-26 | `f7587f86` | Discord sign-in by invitation (RP75) |
| 2026-09-28 | `de77dc1a` | tokens (RP76) |
| 2026-09-28 | `71180895` | the build queue (RP79) |
| 2026-09-28 | `31033891` | self-deploy (RP78) |

The RP78 message says pgmstudio.de "has run since RP76 on a deploy script that lived only on the server and was
started by hand". So the site was up by 2026-09-28. Uncertain: the exact first day the site answered is not in
this repository.

**The machine.** It is "one Hetzner Cloud VM … 2 vCPU and 3.8 GB of memory with no swap, running Ubuntu 26.04",
with Caddy, MariaDB and a timer that deploys a green `main` about five minutes after CI passes
(`docs/deployment.md`).

**Later access work.**

- People sign themselves up as `unapproved` (RP124).
- Agent-made maps are visible only to admins and their owner (RP123).
- Only an owner makes or unmakes an admin (RP85, 2026-09-30).

**The build queue**, in numbers (FEATURES RP79): "three at once on the studio and one per caller … holds 32
waiting and 8 of one caller's for up to 60 s, and refuses the rest `RQ11` at 429 … `/api/health` behind two
exports on two cores went from 3.3 s to 40 ms."

**Redesigns.**

- **2026-10-06:** "Design A" home page with in-game pictures.
- **2026-10-28:** "Direction C — Geist, a zinc palette, a folding studio bar and narrow windows" (`5c73a5b7`),
  with phone layouts.

**Quote.**

> "It is what lets a Claude Code session drive the deployed studio (`PGM_STUDIO_API`, and the token as its
> environment's API credential)."
> — FEATURES.md, RP76

**What we could show.**

- pgmstudio.de's home page.
- `/maps`.
- `/maps/{slug}/sketch` at each phase.
- `/maps/{slug}/configure`.
- `/generator`.
- `/library/houses` (uncertain: the exact Kind slug).
- `/api-docs`.
- A 429 with `Retry-After`.
- `git log` of `tools/deploy/`.

---

## Beat 8 — The newest branch, `ccr-875c17a4-2yjgux`

**How it relates to `main`.** The branch is a long-running session branch whose work reaches `main` as squashed
PRs.

- **Since 2026-10-29** it holds 50 commits not in `main`'s history. In content, `git diff main
  origin/ccr-875c17a4-2yjgux` touches **one file, `TODO.md`** (+18/−6).
- **Merged work, 2026-10-29 → 2026-11-14:** everything else came in as PRs #88–#98.
- **On the branch alone, 2026-11-23:** two commits that write the author's rulings onto the board (`0ee7a8ad`,
  `ed354f43`).

**What the branch's work did:**

- **Backlog audit (2026-10-29, `db1a7958`):** "Eight agents checked all 111 BACKLOG entries against the code",
  with seven fixes (RP121, TC14, C83, TS223, C110, RP107, TN16).
- **Three rounds of the author's answers:**
  - 2026-11-04 (`af72455e`): C122–C126.
  - 2026-11-04 (`bb53150a`): the focus becomes bugs; PG18 removes region draft steps, with migration M0091.
  - 2026-11-13 (`96c8a868`): new capabilities pause, and the generator is frozen.
- **The UI and bug fixes:**
  - a lapsed session closes the page's writes (RP132);
  - the scan follows moved rooms (TS178);
  - the seat preview (TS167);
  - a null material refused (RP98);
  - a copied tree states no species (TL35);
  - one inspector width of 420 px (TS164);
  - a readable Problems list (TS238);
  - kits keep every element (PG29);
  - houses stamp alike in every image;
  - outlines edit points one way (TS130);
  - spawns keep every region (PG31);
  - a room's chests and monument seats stated on its house (WE168);
  - undo stays in its phase;
  - Review opens Configure;
  - door width per style (WE152), with migrations M0095/M0096;
  - water steps down in reaches;
  - a PR template (`acfb2893`).
- **What only the branch adds:**
  - **WE134** — a hand-built prop is "a labelled schematic, stated inline or by reference". A migration
    backfills stored `copied` bodies: a body that matches a library tree becomes a reference to it, and
    everything else becomes a schematic, "since no tree is hand-built".
  - **WE181** — "A door is stated, not given to every narrow opening … `HS2` … keeps one job: every opening
    stays passable".

**The verification pipeline.** The author's note says it "is not yet where it should be". The record has no
single entry naming it. Related material: `backlog-strategy.md`, "Every defect on this board passes every
gate"; the "Problems list" work (TS238); and the TODO header "The author has paused new capabilities (November
2026): the backlog's fixes are worked first, then optimisation and the user experience."

**What we could show.** The `TODO.md` diff itself — the board as the place where author and agent talk. Also the
sequence of PR titles #88–#98 on GitHub.

---

## Open questions for the author

1. **Map walls.** What does "then map walls" refer to? The painter's Wall bucket and void-facing wall-runs, the
   bedrock approach wall (WE167, 2026-10-16), or something built in `pgm-studio-mapgen`? The phrase does not
   appear in the studio.
2. **Go-live date.** On what day did pgmstudio.de first answer publicly? The record only shows that it ran on a
   hand-started script before 2026-09-28.
3. **The 10 October experiment and `Rules:Mode=minimal`.** Was a rules-on versus rules-off comparison run, and
   is its result anywhere? I found no measured per-rule gain in the studio.
4. **Rules that still misfire.** Which rules still raise findings you consider wrong today? Only past fixes are
   recorded (`e6e9e231`, RP110).
5. **Freezing the generator (2026-11-13).** Why freeze it now: is it superseded by the sketch-first, pgmvox-style
   path, or simply finished?
6. **The pgmvox grammar.** Phase 7's seven grammar styles (Brittlebush, Claywork, …) have no FEATURES line and no
   board entry. Dropped, parked, or still to be filed?
7. **The grown tree.** It was removed with "the form goes rather than gets a knob". Was that a judgement on
   procedural trees in general, or on that algorithm?
8. **The verification pipeline.** What does "where it should be" mean concretely: in-game checks, playtests, a
   per-map score?
9. **The edit tool.** `docs/tools/edit.md` is named in `CLAUDE.md` but absent. Did the Edit tool retire, and when?
10. **Model switches.** Opus 5.5 took over from Opus 5 around 2026-09-22, and Sonnet 5.5 wrote 39 commits in
    October. Was the switch your choice, and did you notice a change in the studio work?
11. **Three days in September.** Discord sign-in, tokens, the queue and self-deploy all landed 26–28 September.
    Was there an external reason (other players, a deadline)?

## Not covered / blockers

- I did not read `pgm-studio-mapgen` (out of scope), so the experiment, the 500-wide map and the fire-and-ice
  branch are not cross-checked here. The "500-block-wide map with monuments and core in one line" is not
  mentioned in the studio repository.
- I did not open the artifact links in `docs/pgmvox-port.md`.
- The rule count of 247 is a rough grep, not the live `GET /api/rules`.
