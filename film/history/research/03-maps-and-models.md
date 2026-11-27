# Research 03: the maps and the models over time

Scope: `pgm-studio-mapgen` (git history from 2026-08-13, 943 commits on `mappies-film` at the time of reading), plus
the `tools/mapgen` history in the local `pgm-studio` clone, because the first fifteen boards came from there.
Everything below was read from the files and from `git log` / `git show`. Where a number was measured for this
document, the method is given. Where the record is ambiguous, it says so. Nothing was modified except this file.

Conventions: **hash** is the short commit hash in `pgm-studio-mapgen` unless marked **(studio)**, which means the
`pgm-studio` repository. **Committer names are not authorship.** Most commits are by "Claude" or "rockymine" as the
git author, and the model that wrote the content is named in the `Co-Authored-By:` trailer. Where the film names a
model, it should use the trailer or the run's own write-up, never the git author.

---

## 1. Eras of the repository

### Era 0: the first fifteen, through `tools/mapgen` (11–13 August 2026)

**The first fifteen boards were built on 11–12 August by a tool inside the studio, `pgm-studio/tools/mapgen`, from
one JSON spec each.** `BOARDS-BUILT.md` (line 18): *"Fifteen boards were built on 11–12 August 2026, each from a
single JSON spec. The spec form itself was a day old and there was nowhere to commit one, so only the world was
saved."* The tool entered the studio in (studio) `5897944a` on 2026-08-12: *"tools/mapgen builds a whole map from
one spec: the board (composed, or a literal plan), the paint, the interior elevation, the trees, the buildings, and
the houses the wool and spawn rooms are raised as."*

- Eleven are credited to Opus 5 and four to Haiku 4.5 (`BOARDS-BUILT.md`, the `hk1_*`/`hk2_*` folders; (studio)
  `dc7e177f` "Name the four maps an agent designed after the agent that designed them"). Every spec in the studio's
  history still carries `"authors": ["mapgen"]`, which is why `spinebreak`'s `map.xml` says `<author>mapgen</author>`.
- One of the fifteen, `thornwake`, went upstream into `CommunityMaps/ctw`, and `hk1_viridian` (Haiku 4.5) is
  recorded as the pre-merge draft of upstream `CommunityMaps/ctw/viridian` (`BOARDS-BUILT.md` line 22). Not
  verified against the CommunityMaps repository here.
- **The nine destroy boards all declare `<gamemode>ctw</gamemode>` with no wool on them** (`BOARDS-BUILT.md` line 25),
  because a destroy board was made by *retargeting* a composed capture board's wool markers into monuments. (Studio)
  `b95f3d07` (2026-08-14), deleting the retarget: *"rewriting a capture board's wool markers into monuments put every
  goal at the back of a corridor it never wanted."*
- The author's fault list against them was written the same night: (studio) `1ffb7728` 2026-08-12 *"Write down where
  the first fifteen maps fall short (MG1-MG13)"*, now `pgm-studio/docs/tools/mapgen-review.md`.
- The worlds moved into this repository on 2026-08-15 (`6d2e12e9`, `ea8dc104`).

**Correction to the record, worth a line in the film.** `BOARDS-BUILT.md` says of the fifteen that *"none is
recoverable"*, and `6d2e12e9` says the documents *"are gone"*. The specs themselves are not gone: all fifteen JSON
specs (plus `corvale`, `duskfell`, `openfield`, `voidwatch`) are in the studio's history at `tools/mapgen/specs/`,
readable at (studio) `f7b8cb82^`. Whether those JSON files are exactly what produced the committed worlds is not
established.

### Era 1: the re-implementation diagnosed, and the move to driving the real API (13–22 August)

**The repository opens on 13 August with a recreation that found the tool was a second, weaker copy of the
studio.** The first commit is `7a6c15c1` (ClayClay, traced from the world), and `aa429eb3` (same day, Opus 5) is the
agent's account, now `reports/clayclay-recreation-report.md`:

> "**The deeper problem is that `tools/*` is a reimplementation, not a caller.** `mapgen`'s `Forest`, `Village` and
> `Preset` are a second implementation of placement — a `random.Next` over ground cells with a keep-out mask —
> sitting beside a dressing pass that already places props…" (line 58)
>
> "The system is good and the spec in front of it is not, and the fastest thing anyone could do for an agent
> authoring maps here is to delete the reimplementation and point it at `docs/tools/*.md` and the endpoints those
> describe." (lines 183–186)

The trial runs of 14 August drove the HTTP endpoints rather than `tools/mapgen` (Sonnet run 1 report, line 5:
*"never through `tools/mapgen` and never from a composed board"*). Grok's account the next day (`grok-experience.md`):
*"The earlier parallel `tools/mapgen` re-implementation was correctly diagnosed as a dead end."* Fable's architecture
read (`fable-run3-architecture.md`, 2026-08-16) found that *"`tools/mapgen` re-implements the export leg and drops
three of its four gates"*. The tool was deleted in (studio) `12b364fd` on 2026-08-20 ("RP13: the studio has one front
door": *"the last authoring run made fifteen calls and never touched it"*). On 2026-08-22 `6506b0a2` cut the
authoring apparatus to one brief: *"Six root documents (1,490 lines) became two (612)"*, deleting the art-direction,
map-brief and reviewer-agent documents introduced on 14 August (`7107785c`).

### Era 2: the model trial runs (14 August – 21 September)

Runs 1–5 (14–22 August) put Opus, Sonnet, Haiku, Fable and Grok on the same or similar briefs. From 22 August Opus 5
built most boards one at a time, each after review of the last (Elderwold onward), with a large showcase library on
25–27 August. Model trials resumed in September: Haiku 4.5's five specs (12 Sep), Sonnet 5's five boards (12 Sep),
an orchestrated three-agent Opus run (14 Sep), and the same-day four-board runs of Haiku 4.5, Sonnet 5 and Opus 5 on
21 September. Section 2 has the numbers.

### Era 3: the author's basin, and Millrace finished by hand (30 August – 2 September)

**The author drew a basin in the Sketch tool, three agents built it, and the author and Ruediger_LP finished one
of them by hand.** `f956c846` (2026-08-30) is the author's "Map Experiment" plan; `bb7c8a7f` (2026-08-30) the three
boards (`opus5-millrace`, `sonnet-cutwater`, `sonnet-fallowmere`). `11d926f1` (2026-09-02) adds the hand revamp,
`maps/dtcm/millrace_by_hand`. The author's own review, `review/rockymine-ruediger-millrace.md`, verbatim:

> "myself (rockymine) and Ruediger_LP spent 5 hours to complete Millrace.
>
> the map authored by the agent provided a great basis. the terrain, spawn platform, spawn house, objetives, canal
> walls, water levels, bridges, boulders, and most house placements were kept intact."
>
> "essentially all that was done is theming and some dressing. the redesign of the houses and their interior as well
> as adding a different ship, statue and observer spawn play a big part too. but most comes simply down to better
> theming and using the custom trees."

Fable 5.1 then diffed the two worlds and restated the revamp as studio documents (`dc2efbd0`, `review/fable-millrace-revamp.md`):
*"29,954 of 35,610 columns keep their surface height exactly."* Mossgill (`774b3f22`) is the same techniques on a new
layout. This is also the day the `pgm-board` skill and `CLAUDE.md` arrive (`49085da9`, 2026-09-02).

### Era 4: rules, reading discipline and texture (3 September – 27 September)

The board-by-board Opus 5 work continues (Lindenkreuz, Quatrefoil, Tiefkreuz, the relief runs), and the
repository's instructions are rebuilt: `specs/` split into 15 flat and 111 archived (`5a869dca`, 2026-09-12:
*"The cheapest thing a model does is imitate whatever it opens first"*); a warm-up skill that prices reading
(`bfa21189`); a whitepaper (`65cdb9ea`, 2026-09-18); `ORDER-OF-WORK.md` and `WHAT-A-BOARD-IS-MADE-OF.md`
(`ddeeec05`, `6c138ecb`, 2026-09-19); and the one-paragraph-one-claim rule (`f2ce9b57`). Opus 5.5 first appears on
22 September (`opus55-millbank`, a collaboration run, `b544c291`). Textured pictures and the author's texturing
rulings land on 27 September (PR #5, `9a973906`: *"Texturing rulings from the textured question sheets and the
painted trial boards; eye-height pictures in drive.py"*), and the nine grey Opus 5.5 boards are painted the same day
(`656bd09f`).

### Era 5: the deployed studio (28 September – 2 October)

`d9b3e803` (2026-09-28) *"Drive the deployed studio with a token, when the chat says to"* and `0d07c728` (the token
held as the environment's credential) open the pgmstudio.de runs. Opus 5.5 builds six boards there with questions
left as map notes (`ae025473`, `reports/opus55-notes-run.md`); Sonnet 5.5 builds a jungle and a swamp board
(`9fce7ba2`) and then two boards through the generated Python kit `GET /api/kit.py` (`06d5c037` Pippin Coomb,
`84e4cb10` Halcyon Cays).

### Era 6: freeform and pgmvox (7 October – 12 October)

**On 7 October an Opus 5.5 session stopped driving the studio and wrote voxels directly, from a plan that was drawn
and walked before building.** `2169c018` (Riftwater freeform, 2026-10-07) is the first. On 8 October alone there are
86 commits: some twenty freeform boards across new game modes, the shared library `pgmvox` (`57da19de` part 1, then
versions 0.2.0 to 0.10.0 the same day), and ten trial boards built on it by a second Opus session and a Sonnet session
(`eb8cda8f`, `1c9dbcf6` … `a9956a9b`). `freeform/QUALITY-LEAP.md` is the repository's own account of why the boards
looked better: *"The leap came from moving the decisions the studio makes for an author back into the author's
hands, and from a loop that checked them."* On 10 October a controlled experiment (Sonnet 5.5, same briefs, studio
against pgmvox) found *"the two tools made boards of comparable quality"* (`analysis/freeform-vs-studio/experiment/RESULTS.md`),
and every world was re-filed as `maps/<mode>/<name>/` (`d9c2d891`).

### Era 7: the most recent maps (22 – 27 October), and after

Five Opus 5.5 boards on pgmvox, three of them from the author's concept world: Chantry Gill (`019da8dd`), Hollowstack
(`87f02bab`), Coldstore (`4c8b792c`, revised after review `8139182b`, `7fbed2de`), Frostvault (`e49f3343`) and
Blastworks (`ded3ef3e`), all 2026-10-22/23. pgmvox becomes an installed package (`2bccf438`, 2026-10-23). The studio
replaces relief marks with a modifier stack and Sonnet 5.5 rewrites every instruction for it (`98bc4b8d`, 2026-10-24).
After that: `693f8c29` (2026-11-14, a place's look planned with its position) and the film briefs (2026-11-27).

### Dated timeline (verified rows)

| Date | Hash | What happened |
|---|---|---|
| 2026-08-12 | (studio) `5897944a` | `tools/mapgen` enters the studio: a whole map from one JSON spec |
| 2026-08-12 | (studio) `47228726` | Ridgeway, Hollowmere and Spinebreak specs: "ground stated rather than scattered" (B78) |
| 2026-08-12 | (studio) `dc7e177f` | four boards renamed after the agent that designed them (the Haiku `hk*` specs) |
| 2026-08-12 | (studio) `1ffb7728` | the author's fault list on the first fifteen, MG1–MG13 |
| 2026-08-13 | `7a6c15c1` | first commit of this repository: ClayClay traced from the world |
| 2026-08-13 | `aa429eb3` | the ClayClay report: `tools/*` "is a reimplementation, not a caller" (Opus 5) |
| 2026-08-14 | `644b383f` | Ashen Quarry, the first destroy board authored rather than traced |
| 2026-08-14 | (studio) `738d81fb` | the two documents agents were handed join the studio docs; `approaches.md` is born |
| 2026-08-14 | (studio) `b95f3d07` | the retarget (wool markers turned into monuments) is deleted |
| 2026-08-14 | `82192b0d` | Haiku 4.5 run 1: three boards |
| 2026-08-14 | `43874f3e` | Sonnet run 1: Holdfast, Briarlock, Cinderreach |
| 2026-08-14 | `78c7e4d2` | Opus run 1: the three Quillon boards, through the studio's own endpoints |
| 2026-08-14 | `c24f2702` | Opus 5 run 2 checks the overnight claims: "Three models filed nine boards overnight and their reports disagree" |
| 2026-08-14 | `7573c380` | Haiku run 2: the two boards later found to be 245-byte shells |
| 2026-08-14 | `7107785c` | art direction, named briefs and a reviewer agent |
| 2026-08-15 | `500f5065` | Grok: three maps authored blind, driven for the first time |
| 2026-08-15 | `aafa6119` | Quernstone, four teams round one millstone |
| 2026-08-15 | `6d2e12e9` / `ea8dc104` | the first fifteen's worlds moved in from `CommunityMaps/ctw` |
| 2026-08-16 | `f9b0dc30` | Fable run 3: four themed boards through the live API |
| 2026-08-16 | `819405e5` | the architecture read (Fable): one distance canon, seven shapes of refusal |
| 2026-08-18 | `949b691d` | Opus 5 run 4: four boards and the driver `drive.py` |
| 2026-08-18 | `9520281c` | "Wheal Hazel's bar is 60% dead": the first dead-ground measurement |
| 2026-08-18 | `d1df2512` | Wheal Hazel v2 |
| 2026-08-20 | (studio) `12b364fd` | `tools/mapgen` deleted |
| 2026-08-22 | `6506b0a2` | six root documents become two; reviewer and art-direction agents retired |
| 2026-08-22 | `08e38688` | run 5 (Fable, Haiku, Sonnet), and the driver takes the pictures |
| 2026-08-22 | `ae5e2705` | Elderwold: one shape, everything else relief |
| 2026-08-30 | `f956c846` | the author's basin (Map Experiment) |
| 2026-08-30 | `bb7c8a7f` | three boards off the basin: Millrace, Cutwater, Fallowmere |
| 2026-09-02 | `11d926f1` | rockymine and Ruediger_LP's hand revamp of Millrace |
| 2026-09-02 | `dc2efbd0` | Fable 5.1 diffs Millrace against the revamp and restates it |
| 2026-09-02 | `49085da9` | the `pgm-board` skill and `CLAUDE.md` |
| 2026-09-02 | `d29ec3df` | Lindenkreuz, to a German brief from the author |
| 2026-09-03 | `636990a0` | Quatrefoil, a four-team board from a handed-over plan |
| 2026-09-12 | `5a869dca` | `specs/` split: fifteen flat, 111 archived |
| 2026-09-12 | `63d127cb` | Haiku 4.5's five specs, kept and labelled for what stopped them |
| 2026-09-12 | `b54841e4` | Fable 5.1: four boards to the author's spoken brief |
| 2026-09-12 | `bfa21189` | the warm-up skill that prices reading |
| 2026-09-14 | `d2e6219e` | PR #1: twelve boards from three concurrent Opus agents |
| 2026-09-19 | `ddeeec05` | `ORDER-OF-WORK.md` |
| 2026-09-19 | `6c138ecb` | `WHAT-A-BOARD-IS-MADE-OF.md` leaves the brief |
| 2026-09-21 | `32c77ef7` | "Record the Haiku run honestly: four specs, no board" |
| 2026-09-21 | `a8ea873e` / `b1c90b8f` | Sonnet 5 and Opus 5 four-board runs, same day |
| 2026-09-23 | `b544c291` | Opus 5.5 collaboration run 1 |
| 2026-09-27 | `9a973906` | PR #5: texturing rulings and eye-height pictures |
| 2026-09-27 | `656bd09f` | the nine Opus 5.5 boards painted |
| 2026-09-27 | `d274c0ae` | Delverdale and Whitstone Weald for a 32-a-side play test |
| 2026-09-28 | `d9b3e803` | drive the deployed studio with a token |
| 2026-09-28 | `ae025473` | Opus 5.5: boards on pgmstudio.de, questions left as notes |
| 2026-09-29 | `9fce7ba2` | Sonnet 5.5: jungle and swamp on the deployed studio |
| 2026-10-02 | `06d5c037` | Sonnet 5.5: Pippin Coomb through the generated kit |
| 2026-10-07 | `2169c018` | Riftwater, the first freeform board (Opus 5.5) |
| 2026-10-08 | `57da19de` | pgmvox, the shared freeform library, part 1 |
| 2026-10-10 | `0e90bfe6` | the studio-against-pgmvox experiment (Sonnet 5.5 builds) |
| 2026-10-10 | `d9c2d891` | every world stored as `maps/<mode>/<name>/` |
| 2026-10-22 | `4c8b792c` | Coldstore, the author's bunker concept, finished |
| 2026-10-22 | `ded3ef3e` | Blastworks finished |
| 2026-10-24 | `98bc4b8d` | relief removed in the studio; the instructions rewritten for the modifier stack (Sonnet 5.5) |
| 2026-11-14 | `693f8c29` | a place's look planned with its position |
| 2026-11-27 | `d590b682` | the Prompt-a-Map sketch and the history-film brief |

Commit density for the edit: 8 commits on 08-13, 34 on 08-25, 52 on 09-19, **86 on 10-08** and 92 on 10-10 are the
busiest days; 10-24 to 11-27 has 5 commits in total.

---

## 2. The models compared

**Board counts** are rows in `BOARDS-BUILT.md` that name the model in their author column, counted with a script for
this document. They include written-up non-boards (Haiku's specs that never built) and exclude 46 Opus 5 slugs listed
as "not yet written up" and the freeform boards outside `BOARDS-BUILT.md`. Treat them as orders of magnitude.

| Model (as the record names it) | Active (dates in the record) | Rows in `BOARDS-BUILT.md` | Note |
|---|---|---|---|
| Opus 5 (incl. "Opus") | 2026-08-12 → 2026-10-01 | 78 + 6 | plus 46 unwritten slugs; 11 of the first fifteen |
| Opus 5.5 | 2026-09-22 → 2026-10-23 | 17 + 5 shared with the author | plus most of the 44 freeform board folders |
| Sonnet (unversioned) / 4.5 / 5 / 5.5 | 08-14 / 08-22 → 09-02 / 09-12 → 09-21 / 09-29 → 10-24 | 10 / 4 / 9 / 8 | plus 5 pgmvox trial boards and 2 pgmvox experiment boards |
| Haiku (unversioned) / Haiku 4.5 | 2026-08-12 → 2026-09-21 | 5 / 10 | 4 of the first fifteen; most later rows are not maps |
| Fable / Fable 5.1 | 2026-08-16 → 2026-09-12 | 4 / 7 | the run-3 commit's trailer reads "Fable 5"; `BOARDS-BUILT.md` names Fable 5.1 from run 5 (08-22) |
| Grok | 2026-08-15 | 3 | authored with no running studio |

### Opus 5

**Runs:** the first fifteen (11 of them), run 1 and 2 (14 Aug), the method boards (Coldharbour, Quernstone), run 4
(18 Aug), the board-at-a-time series from Elderwold (22 Aug), the showcase library, Millrace, Lindenkreuz, Quatrefoil,
the relief runs, the orchestrated run (12 boards, 14 Sep), the four-board runs of 21 Sep.

**What the record says.** Run 2 corrected the other models' overnight reports (`c24f2702`: *"three claims were wrong
when filed"*). The repository's own measurement history is mostly Opus 5's: Wheal Hazel *"27.2% dead ground → 0.8%"*
(v1 to v2); the four-board run of 3 September, *"1% dead ground against 28.8%, 36.7% and 40.1%"* for the one board
whose layout a rule forced; Quatrefoil *"5 904 walked · 0 scrambled · 0 barrier, 0% dead"*.

**Typical failures, from its own reports.** Building inside a standing stone (`opus5-hoarstone-run.md`: *"I let a
building stand inside a standing stone."*); misdiagnosing a studio fault as the contract's (`opus5-run4.md`, the
author-name row: *"missing, and I misdiagnosed it as the contract's"*); mistaking an evaluator's `"kind": "hard"` for
a refusal and rebuilding Quatrefoil at twice the scale (`BOARDS-BUILT.md` line 325).

**Best board, by the author's own words:** `opus5-millrace`, the one the author chose to finish: *"the map authored
by the agent provided a great basis."* By the numbers: `opus5-quatrefoil` (0 scrambled, 0% dead).

### Opus 5.5

**Runs:** collaboration run with the author (22–23 Sep), four destroy landscapes (24 Sep), the nine painted boards
and the two 32-a-side boards (27 Sep), six boards on pgmstudio.de (28 Sep onward), the freeform boards and pgmvox
(7–10 Oct), the October concept boards (22–23 Oct).

**What the record says.** The first two deployed-studio boards were judged barren by the author, given in chat and
recorded as a paraphrase, not verbatim (`reports/opus55-notes-run.md` lines 104–110: *"there is no dirt or grass for
a tree to stand in, two houses stand by a path, the frontlines are bare, and the outlines were never shaped"*). The
playtest of the freeform and trial boards (`analysis/freeform-vs-studio/playtest-feedback-2026-10-10.md`, author's
wording summarised by the agent): *"Praise: Riftwater "essentially perfect", Gullhaven pair cute, Curio "what I
always wanted", Stratum's aesthetic, Penstock great looking, Sandreach a fun mix."* The same table lists 30 faults
across the boards; it counts *"The studio would have caught 9, partly caught 4, and not caught or could not have
built 17."*

**Typical failures:** density and scale (*"far too many trees"*, *"carpets ~50% too large"*), discoverability
(*"core fully underground, impossible to find"*), stairs and joins (*"well shaft does not open onto its tunnel"*).
These rows mix Opus 5.5 freeform boards and the Sonnet trial boards; the table names boards, not models.

**Best board:** Riftwater (`freeform/lib/boards/riftwater`, `maps/dtcm/riftwater`), the board the playtest calls
"essentially perfect". The repository's own caution: Riftwater took *"Opus, hours per board rather than minutes,
rounds of the author's review, and bespoke code (Riftwater is 3,379 lines …)"* (`experiment/RESULTS.md`).

### Sonnet (4.5, 5, 5.5)

**Runs:** run 1 and 2 (14 Aug), run 4 (18 Aug), Fellgate Moor in run 5 (Sonnet 4.5, 22 Aug), Cutwater and
Fallowmere off the basin (Sonnet 4.5, 30 Aug), Fellmoor Common (Sonnet 4.5), five boards (Sonnet 5, 12 Sep), four
boards (Sonnet 5, 21 Sep), the deployed studio (Sonnet 5.5, 29 Sep), the kit boards (2 Oct), five pgmvox trial
boards (8 Oct), the four experiment boards (10 Oct), and the modifier-stack rewrite of the instructions (24 Oct).

**What the record says.** Run 1 found a real defect, an exception surfacing as a 500 (`sonnet-run1.md` line 46). Run 4,
measured by Opus 5 (`opus5-run4.md` §9): *"Sonnet built the two briefs nothing here had ever attempted"*: the first
four-team board (`sonnet-compass`) and the first desert. Sonnet 4.5 in run 5: *"Nothing in this run turned out to be a
genuine capability gap."* The author on Sonnet 5.5's experiment boards (`experiment/REVIEW-1.md`, the author's points
written down by the agent): Abbeymoor studio *"comes a lot closer to a map that reads like a place"*; Abbeymoor pgmvox
*"really looks like a place, with a nice style and a few flaws"*; Slatefold pgmvox *"The houses near the spawn stand
all in one line"*, *"too much stone in general"*.

**Honest numbers, the 21 September run (same day as Opus 5 and Haiku 4.5):**

| Board | Model | walked · scrambled · barrier | dead |
|---|---|---|---|
| `sonnet5b-white-scarp` | Sonnet 5 | 9644 · 12 · 8 | 27.4% |
| `sonnet5b-turbary-cut` | Sonnet 5 | 9644 · 8 · 12 | 43.0% |
| `sonnet5b-ropeworks-quay` | Sonnet 5 | 22688 · 0 · 0 | 3.3% |
| `sonnet5b-highgarth-fell` | Sonnet 5 | 13472 · 0 · 0 | 1.2% |
| `opus5b-chalkmere` | Opus 5 | 9 324 · 382 · 0 | 9.6% |
| `opus5b-slakefell` | Opus 5 | 8 558 · 608 · 52 | 6.7% |
| `opus5b-ochredrift` | Opus 5 | 11 118 · 318 · 128 | 0.0% |
| `opus5b-alderquay` | Opus 5 | 8 440 · 90 · 0 | 1.6% |

All eight exported with the gate open. The studio's own band for dead share is `[0, 0.12]` (`32c77ef7`); two of the
four Sonnet 5 boards are outside it. Low scramble counts on the Sonnet boards read as flatter ground; that is an
inference from the counts, not a claim the record makes.

**Typical failures:** large dead flanks on destroy lanes; mislabelled game mode in the earliest runs (the `ctw*` rows);
in the pgmvox trial the author flagged Overgrowth's *"far too many trees for TDM"* and Hoarfrost Reach's *"fences
inside the spawn"* (playtest table; which Sonnet version built the trial boards is not stated, see section 5).

**Best board:** by the author's words, `exp-abbeymoor-pgmvox` (*"really looks like a place"*); by novelty,
`sonnet-compass`, the first four-team board.

### Haiku (4.5)

**Runs:** four of the first fifteen (12 Aug), run 1 and 2 (14 Aug), run 4 (18 Aug), Hollow Crown in run 5
(22 Aug), five specs (12 Sep), four specs (21 Sep).

**What the record says.** Run 1 reported two capabilities missing that existed; run 2's own summary corrected that
(*"Run 1's core failure was not a system limitation, but a reading failure."*) and then shipped two boards it called
*"plan through export, verified working"* that were 245-byte `map.xml` files: *"no teams, no spawns and no objectives,
over region files that are largely empty"* (`README.md` line 166). `maps/ctw/haiku_r2_canonical/map.xml` is 245 bytes
on disk today. Run 4, measured by Opus 5: themes bound **0 · 0 · 0 · 0**, props placed **0 · 0 · 0 · 0**, renders
**0** (`opus5-run4.md` §9), and *"the whole distance travelled since the run that described two empty 245-byte shells
as verified"* is that its report said so. Run 5: Hollow Crown is *"honest about being a test"*, one central piece
*"and nothing else"*.

**The September runs did not produce a board.** 12 September, five specs *"written at once in about five minutes,
against roughly half an hour a board for the others"*; four state `"plan": 1` and are refused `PL15`, four carry no
placements at all (`BOARDS-BUILT.md` §"Haiku 4.5 — five specs"). 21 September, four specs, every one refused:

| Spec | dead share (band 0–0.12) | GO3 (band 85–150) | other refusals |
|---|---|---|---|
| `haiku45-scarp` | 0.766 | 7 | RQ2 (studio crash) |
| `haiku45-moor` | 0.833 | — | PL12, PL9 |
| `haiku45-bastion` | 0.806 | 7 | PL4, PL9 |
| `haiku45-cistern` | 0.854 | 7 | RQ2 (studio crash) |

`32c77ef7`: *"Removed three worlds that each predated their own spec by twenty minutes, and three reviews asserting
"built and exported successfully, 0 declined props, OPEN export gate" about boards that refuse."* A GO3 of 7 means
*"both teams' objectives are stacked in the middle of the board."*

**Typical failures:** claiming success it had not checked; missing placements; dropped keys (`themeByHeight`) taken
as stated; game modes asserted in docstrings rather than built.

**Best board:** `hk1_viridian` (`maps/ctw/viridian`), recorded as the draft of a board that went upstream to
CommunityMaps. After the first fifteen, no Haiku board in the record carries a theme or a prop.

### Fable (5 / 5.1)

**Runs:** run 3 (16 Aug: Firnline, Kerbstone, Sunspit, Tanglewold), the architecture review (16 Aug), Whitebarrow
Down in run 5 (22 Aug), the Millrace revamp restated and Mossgill (2 Sep), four boards to the author's spoken brief
with a second pass (12 Sep).

**What the record says.** Fable's run 3 is titled *"four maps through the live API, and the fixes made along the
way"*; its architecture read named `tools/mapgen` as dropping three of four export gates, which preceded the tool's
deletion. Whitebarrow: *"200 at every step of the final run, nothing declined, all 37 props landed"*. The four boards
of 12 September: *"Every board exports with the gate OPEN and nothing declined"*, with Whinberry Ring reading
`4126 · 0 · 0` and Ashcombe Delph `15309 · 1222 · 901, seventeen faces`.

**Typical failures:** Saltwharf still carries `GO1` 2.47 against 3.0 and `GO3` 73 against 85 after the run
(`fable-four-boards-run.md`). The revamp restatement left holes the author called *"holes in the bottom of the
world"* (`review/fable-millrace-revamp.md` line 108).

**Best board:** `fable-millrace-revamp` / `fable-mossgill`, the two boards that carried the hand revamp's techniques
back into the studio.

### Grok

**One run, 15 August, three maps written from the documents with no running studio** (`reports/grok-run1.md`):
*"the plans were nearly right and two of three were refused for arithmetic; the layouts were wrong in a way that
builds nothing and says nothing; the dressing was authored in the wrong unit."* All three layouts *"rasterize to no
ground"*. On the other side: *"all six styles stamp"*, six complete buildings. Grok's own account
(`grok-experience.md`) opens: *"I did not have a running studio (no .NET 10, no MariaDB)."*

**Best board:** `grok-ridge` (`maps/ctw/grok_ridge`), the only capture board, with
`specs/archive/grok-ridge/renders/00-plan-as-grok-authored.png` showing the plan as Grok wrote it.

### The cross-model reading the record supports

Two controlled comparisons exist, and both are narrower than "which model is best". **Run 4 (18 Aug)** gave Sonnet and
Haiku the same kind of brief and measured both (table in `opus5-run4.md` §9). **21 September** ran Haiku 4.5, Sonnet 5
and Opus 5 on the same four-objective brief the same day: no Haiku board built, all eight Sonnet and Opus boards
exported, and the Opus boards' dead share was lower on three of four. **10 October** held the model fixed (Sonnet 5.5)
and varied the tool, and found the tools comparable. No controlled run compares Opus 5.5 with Sonnet 5.5 on the same
brief in the same tool; the Riftwater-against-Russetford pairing was found not to be the same brief
(`analysis/freeform-vs-studio/agent-reports/same-brief-comparison.md`).

---

## 3. The context a model must read

**Method.** For each date, the last commit before 23:59 of that day on this branch was taken, and each document was
measured with `git show <commit>:<file> | wc -w`. The "must-read" set is what that commit's own entry document said to
read before the first request; the skills and the two gameplay documents are given separately because the record
says they are loaded at a question or "once". Before 14 August the documents lived in the studio; that row is measured
at (studio) `738d81fb^`.

| Date | Commit | Must-read set (words each) | Must-read words | Plus skills | Plus the two gameplay docs |
|---|---|---|---|---|---|
| 2026-08-13 | (studio) `738d81fb^` | `tools/mapgen/surface.md` 6676 · `review.md` 5944 | 12,620 | — | — |
| 2026-08-14 | `c80ea2c1` | AUTHORING-BRIEF 2635 · ART-DIRECTION 4987 · MAP-BRIEFS 3408 | 11,030 | (reviewer agent: REVIEWER-BRIEF 3320) | approaches.md 2479 (studio) |
| 2026-08-16 | `7e01e5c9` | AUTHORING-BRIEF 2657 · ART-DIRECTION 1793 · MAP-BRIEFS 3411 | 7,861 | — | — |
| 2026-08-19 | `a1e55873` | AUTHORING-BRIEF 3439 · ART-DIRECTION 1793 · MAP-BRIEFS 3411 | 8,643 | — | — |
| 2026-08-22 | `4e1d56ab` | AUTHORING-BRIEF 3267 ("the only brief"); its reading order adds GENERATION-NOTES 5979 | 3,267 (9,246) | — | — |
| 2026-08-26 | `a3ea1137` | AUTHORING-BRIEF 4862 | 4,862 | — | — |
| 2026-09-02 | `b4cb7ac8` | CLAUDE.md 267 · AUTHORING-BRIEF 5059 · pgm-board skill 1773 | 7,099 | (included) | — |
| 2026-09-13 | `f301402e` | CLAUDE.md 467 · AUTHORING-BRIEF 7283 · pgm-board 4215 · warm-up 1808 | 13,773 | (included) | — |
| 2026-09-20 | `3702005b` | CLAUDE.md 942 · ORDER-OF-WORK 1969 · WHAT-A-BOARD 4066 · AUTHORING-BRIEF 3841 | 10,818 | 17,407 | — |
| 2026-09-30 | `467a802e` | CLAUDE.md 1350 · ORDER 2091 · WHAT 7169 · BRIEF 4119 | 14,729 | 22,155 | — |
| 2026-10-12 | `9ac0195c` | CLAUDE.md 1377 · ORDER 2628 · WHAT 8125 · BRIEF 4248 | 16,378 | 23,920 | — |
| 2026-11-27 | `1e86f019` | CLAUDE.md 1377 · ORDER 2721 · WHAT 8134 · BRIEF 4273 | 16,505 | 23,629 | 39,860 (match-flow 12,199 · approaches 4,032) |

Four readings of the table for the film:

- **The load fell twice on purpose and grew back each time.** 14 August (11,030 words, three documents) to 22 August
  (3,267, one), and the brief's 7,283 words on 13 September split into three documents on 19 September. By November
  the must-read set is 16,505 words, half of it the author's look rulings (`WHAT-A-BOARD-IS-MADE-OF.md`, 8,134).
- **The repository prices itself in tokens, and its figures are lower than the word counts.** The warm-up skill says
  the three must-read documents *"come to ~13k tokens, and the two skills to ~9k"*, and `CLAUDE.md` says the three are
  *"about 12k tokens together"*. Measured today they are 15,128 words, and words rarely come in under tokens, so the
  token figures are probably from an earlier, shorter state. Treat the token claims as dated.
- **What may never be read is part of the context too.** The warm-up skill: two layout files are *"397k · 367k"*
  tokens and *"Either one ends the run."* A whole text report of one board is *"30–57k"*.
- **A session in this environment also loads the studio's `CLAUDE.md`** when both repositories are present (6,893
  words in the studio clone read here; 3,736 on 14 August). Whether each historical run had it loaded is not in the
  record.

Other root documents existed beside the must-read set and were not counted: `GENERATION-NOTES.md` (peak 21,469
words), `README.md` (peak 12,885 on 13 Sep, 2,495 now), `BOARDS-BUILT.md` (24,102 now). All counts are `wc -w` over
Markdown source, tables and code included.

---

## 4. Side-by-side candidates

Twelve entries in time order, with two lows. "World" is the path in this repository; the date is when the board was
built or committed. A "—" in the renders column means no render exists in the repository. `tools/render/` (`iso.py`,
`png.py`) can draw any world on disk; nothing was rendered for this document.

| # | Board | Date | Model | World | One line | Existing renders |
|---|---|---|---|---|---|---|
| 1 | Emberfall | 11–12 Aug | Opus 5 (via `tools/mapgen`) | `maps/ctw/emberfall` | four wools over cinder terraces; one of the first fifteen, no spec, no review | — |
| 2 | **Spinebreak (low)** | 12 Aug | Opus 5 (via `tools/mapgen`, author "mapgen") | `maps/dtcm/spinebreak` | "One long ridge, a monument and a core at each end of it": 145 × 420, eight objectives strung along one axis | — |
| 3 | **Haiku R2 Canonical (low)** | 14 Aug | Haiku 4.5 | `maps/ctw/haiku_r2_canonical` | reported "verified working"; a 245-byte `map.xml` with no teams, no spawns, no objectives | — |
| 4 | Quillon Barrow | 14 Aug | Opus | `maps/dtcm/quillon_barrow` | the canonical brief: barrow in the open, wood west, crag east, village behind, channel in front | `specs/archive/quillon-barrow/renders/02-topdown.png`, `09-topdown-objectives.png` |
| 5 | Sonnet Holdfast | 14 Aug | Sonnet | `maps/dtcm/sonnet_holdfast` | the same canonical brief, 268 × 360 | `specs/archive/sonnet-holdfast/renders/holdfast_topdown.png` |
| 6 | Grok Ridge | 15 Aug | Grok | `maps/ctw/grok_ridge` | authored blind, built afterwards; three terraces and a crest | `specs/archive/grok-ridge/renders/00-plan-as-grok-authored.png`, `10-topdown-material-painted.png` |
| 7 | Wheal Hazel → v2 | 18 Aug | Opus 5 | `maps/ctw/wheal_hazel` (v1); v2's region files were not found in the tree (`specs/archive/opus5-wheal-hazel-v2/map.xml` only) | the first board judged by dead ground: 27.2% → 0.8% | `specs/archive/opus5-wheal-hazel/renders/03-topdown.png`, `06-coverage.png`; `specs/archive/opus5-wheal-hazel-v2/renders/06-coverage.png` |
| 8 | Millrace: agent, by hand, restated | 30 Aug / 2 Sep / 2 Sep | Opus 5 / rockymine and Ruediger_LP / Fable 5.1 | `maps/dtcm/millrace`, `maps/dtcm/millrace_by_hand`, `maps/dtcm/millrace_revamp` | the basin flooded and walled; five hours of hand theming over the studio's world; the hand work restated as documents | `specs/opus5-millrace/renders/world-iso.png`; hand world —; `specs/fable-millrace-revamp/renders/world-iso.png` |
| 9 | Quatrefoil | 3–4 Sep | Opus 5 | `maps/ctw/quatrefoil` | four teams, nine landmasses, 5 904 walked · 0 scrambled · 0% dead | `specs/archive/opus5-quatrefoil/renders/world-iso.png` |
| 10 | Gypsum Reach | 28 Sep → | Opus 5.5 (deployed studio, six passes on the author's notes) | `maps/dtcm/gypsum_reach` | a pale desert lane, the board the "barren" remark reworked | `specs/opus55-gypsum-reach/renders/world-iso.png`, `eye-goal-red.png` |
| 11 | Riftwater | 7 Oct | Opus 5.5 (freeform) | `maps/dtcm/riftwater` | the playtest's "essentially perfect" | `freeform/lib/boards/riftwater/renders/30-iso-board-se.png`, `05-topdown-annotated.png` |
| 12 | Coldstore | 22–23 Oct | Opus 5.5 (pgmvox, the author's concept) | `maps/ctw/coldstore` | a bunker under an ice field, 208 × 112, a bedrock roof over void | `freeform/lib/boards/coldstore/renders/50-board.png`, `51-board-se.png` |

Alternates if one fails on screen: Sonnet 5.5's `exp-abbeymoor-pgmvox` (renders under
`freeform/lib/boards/exp-abbeymoor-pgmvox/renders/`), Opus 5's `opus5-elderwold`
(`specs/archive/opus5-elderwold/renders/world-topdown.png`), Blastworks
(`freeform/lib/boards/blastworks/renders/50-board.png`).

### The "500-wide" low: Spinebreak, most probably

**Spinebreak is the best match in this repository, and it is 420 blocks long rather than 500.** The evidence:

- **Size.** `tools/anvil.py maps/dtcm/spinebreak/region` reads bounds `x −72..72, z −210..209`: 145 × 420 blocks, and
  `BOARDS-BUILT.md` says *"one long 145×420 ridge, an objective at each end"*. The only world here with a longer chunk
  extent is `arcade/lantern_pass` (128 × 464 by chunk, a runners-and-shooters arcade map, not a destroy board).
- **The objectives are in a row.** The `map.xml` places four monuments and four cores: monuments at x ±50, z ∓200
  and x ±40, z ∓60; cores at x ±70, z ∓200 and x ±60, z ∓60. All eight sit inside a 145-wide strip and spread over 400
  blocks of z. A principal-axis fit of the objective positions, run for this document over the 23 worlds whose
  objective cuboids a regex could read, gives Spinebreak a minor-to-major ratio of 0.144 (0 is a perfect line). It
  is the fourth most line-like and by far the largest: the three ahead of it are `dtcm/hollow_crown` (0.003, 100 × 120),
  `dtcm/ashfall_scar` (0.039) and `dtcm/obsidian_keep` (0.070).
- **Nothing beside them.** The spec's only relief is one `line` mark down the long axis (points z 20 → 200), and the
  void rule allows building only in `x −20..20, z −10..10`.
- **It was a known fault at the time.** (Studio) `cc7edea9`/`802b4b13` (13 Aug): *"three of the seven shipped destroy
  specs (`goldhollow`, `mourncrag`, `spinebreak`) are refused by B82's void check"*, because the core offset *"walks the
  core off the land"*. (Studio) `42b8b91b` (15 Aug), B99: *"`goldhollow` and `spinebreak` rendered four and eight
  objective markers isolated from the board's navigable component"*.
- **Why it happened.** It was a 15-a-side composed capture board with its wool markers *retargeted* into a monument
  and a core (`"objective_mode": "dtcm"`), the mechanism (studio) `b95f3d07` deleted for putting *"every goal at the
  back of a corridor it never wanted"*.

**Uncertain.** The author remembers "roughly 500 wide" and "nothing outside". Spinebreak has no render, so the author
should confirm it from a fresh one. **The runner-up is Haiku 4.5's Hollow Crown** (`maps/dtcm/hollow_crown`,
22 Aug): its objectives are the most exactly in line of any world here (0.003), and `BOARDS-BUILT.md` describes it as
*"two spawns at opposite ends, one central reach piece carrying the objectives, and nothing else"*. That matches
"nothing outside", but it is only 100 × 120 blocks. A board fitting the memory better could sit in the studio's own database, its
scanned output folder, or the deployed studio, none of which were read here.

---

## 5. Open questions for the author

1. **Is Spinebreak the line-up map you remember?** It is 145 × 420 with eight objectives on one axis. Or is it Hollow
   Crown (100 × 120, objectives exactly in line, nothing else on it), or a board in the studio's database or on
   pgmstudio.de that this repository does not hold?
2. **The first fifteen's specs survive in `pgm-studio` history (`tools/mapgen/specs/*.json`), though this repository
   calls them unrecoverable.** Are they the specs the committed worlds were built from? If so, they are the earliest
   artefact the film can show being turned into a world.
3. **Did `thornwake` and `viridian` really ship in `CommunityMaps/ctw`, and were either of them changed by hand before
   merging?** That would make a Haiku 4.5 board the first AI map to go upstream.
4. **Who actually built the first fifteen in the sense of choosing them:** you running `tools/mapgen` with an agent,
   or agents running it alone? The specs name "mapgen"; `BOARDS-BUILT.md` names Opus 5 and Haiku 4.5.
5. **Which Sonnet built the pgmvox trial boards of 8 October** (Cinderfall, Tamarisk Wash, Hoarfrost Reach,
   Overgrowth, Whitecliff Cistern)? The commits carry the orchestrator's Opus 5.5 trailer, and the world says only
   "Claude (pgmvox trial)".
6. **The playtest of 10 October is recorded as a summary of your wording.** Are "essentially perfect" (Riftwater)
   and "what I always wanted" (Curio Square) your exact words, and may the film quote them as such?
7. **Which reviews in `review/` are yours?** Only `rockymine-ruediger-millrace.md` is in your own voice. The rest read
   as agent-written, with your rulings folded in. The film brief calls `review/` "the human author's reviews".
8. **The barren remark on the first two deployed-studio boards (28 Sep) was given in chat and is only paraphrased.**
   Do you remember the wording?
9. **Grok and Fable:** how were they run (which product, which access), and why did each stop after a few runs? The
   record says only that Grok had no studio, and that Fable is "Fable 5" in one trailer and "Fable 5.1" elsewhere.
10. **Is the reading-load curve the one you experienced?** The repository's own token figures (~12–13k) look older
    than its present word counts (15,128 words for the three must-read documents). Did a model ever visibly run out
    of context on a board, and which one?
11. **The 21 September same-day run is the cleanest three-model comparison in the record.** Was it set up as a
    comparison, or did it happen to land on one day?
12. **Ruediger_LP's part in the Millrace revamp:** what did each of you do in the five hours, and which change mattered
    most to you? The review credits *"better theming and using the custom trees"*.
13. **Between 24 October and 14 November this repository has almost no commits.** Was that the move to the
    fire-and-ice hand-built experiment, or to the studio branch, or a pause?
