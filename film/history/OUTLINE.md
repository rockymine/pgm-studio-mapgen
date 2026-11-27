# A Rule Is Not a Design — outline for approval

The proposal for the history film, written for the author to approve before anything is built. It follows the
brief (`film/NEXT-history-film.md`) and uses only what the four research files under `film/history/research/`
record. Event numbers in square brackets, such as [13], are rows of `timeline.md`. Where the research contradicts
the brief, the outline follows the research, and the section *Contradictions with the brief* lists each case.

## Logline and through-line

In September 2025 a Minecraft PvP map maker asked Google's AI Studio for a capture-the-wool layout generator,
and it handed back a JSON file. Fourteen months, five repositories and more than 3,800 commits later (`01`, `02`,
`03`: 5 + 112 + 95 + 2,696 + 943), a studio on
pgmstudio.de describes itself to the models that drive it: its routes, its 125-plus rules, its 226 words. Opus,
Sonnet, Haiku, Fable and Grok have built well over a hundred boards on it, and they got visibly better. Then the
author built a map by hand, underground and inside a mountain. Every version the agents had made of that map
had passed some check, and none of them was the map. The film is the record of that year: what can be told to a
tool, and what still has to be seen by the person who plays.

**The through-line** is the author's own lesson, quoted from the fire-and-ice study and returned to at the end
of every act: *"a geometric rule is not a design."* (`sketches/fire-and-ice/study/LESSONS.md`). Each chapter
shows something that was turned into a rule, a measure or an endpoint, and then shows what that rule could not
catch.

## Shape

The film runs about **14 minutes** in ten chapters and three movements. Chapters 2–5 are the machine being
built, in the order the record dates it. Chapters 6–8 are the models using it: the lows, the API, the look.
Chapters 9–10 are the rethink and the hand-built map. A recurring device ties them together: **the activity
curve** (weekly commits, from `timeline.md`) grows across the bottom of the frame at each chapter card, with the
model band under it, so the viewer always knows where in the year they are.

| # | Working title | Length | Period |
|---|---|---|---|
| 1 | Cold open: Eleven ways to be wrong | 0:40 | Nov 2026 |
| 2 | A drawing that became blocks | 1:30 | Sep 2025 – Jun 2026 |
| 3 | The void, the graph and the boxes | 1:20 | Jun – Aug 2026 |
| 4 | How the machine composes a map | 1:50 | Jul – Oct 2026 |
| 5 | Houses work. Trees are hard. | 0:55 | Aug – Sep 2026 |
| 6 | Fifteen boards and a line | 1:25 | Aug – Sep 2026 |
| 7 | A tool the AI uses | 1:40 | Aug – Oct 2026 |
| 8 | The finish: five hours by hand, then real textures | 1:20 | Sep 2026 |
| 9 | Starting again | 1:25 | Oct – Nov 2026 |
| 10 | By hand | 1:55 | Oct – Nov 2026, and the names |
| | **Total** | **14:00** | |

---

## 1. Cold open: Eleven ways to be wrong (0:40)

**Claim.** The film opens at the end of the year, on the one map the tool did not make, to say what it is
about: a map can pass every check and still be wrong.

**Events.** [48] the composition of 2026-11-02 → 11-07; [50] the study of 2026-11-27.

**On screen.** The fire-and-ice viewer (the artifact `555b1fbe…`, offline copy in
`sketches/fire-and-ice/study/viewer/` on branch `claude/compassionate-cerf-fg7m17`), captured headless with its
own `check.js` harness. A slow orbit on the preset "Gelände und Untergrund", the loft lines in fire orange. Over
it, the rejection reasons from `LESSONS.md` type on one by one as white text and stack up the left edge. On the
last one the frame cuts to black and the quote holds. A hard cut to a JSON file scrolling in a 2025 browser
leads into chapter 2.

**Quotes, verbatim.** From `study/LESSONS.md`: "the surface was not closed" · "stairs stood exposed" · "the
mountains broke into separate pieces" · "a gorge was cut above the wool room" · "the map sat 8 blocks too high" ·
"a ramp led into the void" · "The lesson that carried over is that a geometric rule is not a design. Every one of
those failures passed some check that existed at the time."

**Interview slot.** None. The cold open belongs to the record.

## 2. A drawing that became blocks (1:30)

**Claim.** The studio began fourteen months ago as a JSON file. The first blocks came from a small self-built C#
editor, and the C# studio of June 2026 is a return to that language, not a first move to it.

**Events.** [1] 2025-09-28 the AI Studio app; [2] 2025-10-01 its generator; [3] 2025-10-03 "Download JSON" and
the last commit; [4] 2025-10-10/11 MinecraftLayoutEditor; [5] 2025-10-12 the first `.schematic`; [6] 2025-11-06
"(claude & grok)"; [7] 2026-05-31 the Python scaffold; [9] 2026-06-07 the loadable map folder; [10] 2026-06-12
03:24 and 17:21; [11] 2026-06-13 the port in one day.

**On screen.**
- Four screen recordings, one per era, made by a headless browser (Playwright, as `capture.cjs` already does):
  CTW-Layout-Generator under Vite with its sliders, its step-wise editor and "Download JSON";
  MinecraftLayoutEditor placing nodes, mirroring a half, drawing an edge as Bresenham blocks, and "download
  schematic"; pgm-map-studio's Flask editor; pgm-studio at `7b30744a` if it builds, else its file tree.
- The `.schematic` the 2025 editor writes, loaded as a world and rendered with the eye renderer (`eye/eye.cs`):
  the first AI-adjacent blocks, as the game draws them.
- The two timestamps of 2026-06-12 as a split screen of two `git log` lines, 03:24 and 17:21. Committer emails
  are masked in every `git log` shown in the film.
- The activity curve's first frame: three short bursts in 2025–26, a gap of five and a half months, then the
  studio's first week.

**Quotes, verbatim.** "An automated system to generate balanced, tactically diverse battlefield layouts for
Minecraft Capture the Wool … within a void-based architecture" (`CTW-Layout-Generator/metadata.json`) · "change
node highlight, add schematic creation and download" (`d961f6a`) · "working import of .leveldat and .mca files
(claude & grok)" (`d2c4bc3`) · "A from-scratch ASP.NET Core rewrite of the Python `pgm-map-studio` … which stays
in place as the behavioural reference" (`CLAUDE.md` at `7b30744a`).

**Interview slots.** rockymine Q1 (the first blocks on screen) after the schematic render; the answers to the
research's open questions on why Python and why back to C# (`01` §4, Q7–Q8) after the 06-12 split screen.

## 3. The void, the graph and the boxes (1:20)

**Claim.** Capture-the-wool came first because it is the most structured mode: the void decides where players
can go, so a map reads like a graph. The graph was the oldest idea in the record; it was written up and dropped in
23 minutes, and the model that replaced it — hub, wool approaches, frontline, middle — is deliberately narrow.

**Events.** [8] 2026-06-05 the pamphlet; [12] 2026-06-20 "0 neutral mid pieces"; [13] 2026-07-02 14:31 and 14:54;
[15] 2026-07-04 recorded play; [16] 2026-07-10 → 07-21 the boxes; [17] 2026-07-15 DTM/DTC a month later; [18]
2026-08-09 match flow; [28] 2026-08-15 the Thunder limit.

**On screen.**
- A corpus CTW map rendered top-down with the eye renderer, its void in black; then the same map's islands
  redrawn as nodes and edges, morphing out of the terrain (a diagram, labelled as one).
- The same document twice, 23 minutes apart: `git show 845ccb0a:docs/contracts/layout-generation.md` against
  `313ae96b`, as a diff that wipes "Layer A — the plan (topology graph)" away. A clock overlay counts 14:31 →
  14:54.
- The 2025 node types (`types.ts`: `HUB`, `WOOL_ENTRY`, `FRONT_LINE`) laid beside the 2026 box kinds (`spawn`,
  `hub`, `wools`, `frontline`, `mid`): the same words, nine months apart.
- The `model.md` §1 pipeline figure as a title card.
- The limit: an organic map from the corpus (one of the Thunder series, if the author names one) beside a
  generator card from `/generator`, with the `model.md` quote over both.

**Quotes, verbatim.** "The ground plane is not just terrain — it is the map's navigational grammar."
(`ctw-map-pamphlet.md`) · "a thinned skeleton cannot represent side contact … and biases generation toward thin
maps" (`313ae96b`) · "a void anywhere else is uncrossable at every height" (`b34cf7eb`) · "Boxes are a model of how
an author works, not a property of maps." (`model.md`) · "That is a limitation rather than a defect, it is the
author's stated position, and it stays." (`model.md`, `0d8f68e7`).

**Interview slots.** rockymine Q2 (when the graph stopped being enough) over the 23-minute diff; Q3 (what holding
the line cost) after the Thunder comparison; the research question on why CTW before DTM/DTC (`01` §4, Q9) opens
the chapter.

## 4. How the machine composes a map (1:50)

**Claim.** This is how the studio makes a map today, shown once in full, one step at a time, in one map: a request
with no geometry becomes boxes, then ground, then landforms, then paint, then buildings, then dressing.

**Events.** [15] 2026-07-04 the composer; [16] 2026-07-21 the box pipeline; [21] 2026-08-12 the relief solver;
[47] 2026-10-24 the modifier stack. The September library of composed boards (TG1, 2026-09-28) and the
hand-over as a sketch (TG7, 2026-10-18) are named in narration (`02` Beat 1).

**On screen: the generator time-lapse.** One map built on the session's own studio, captured at every step from
one fixed camera with `render/isometric` and a closing `render/eye`, then played as a time-lapse:
1. **Request** — a title card: players per team, symmetry, seed. No geometry.
2. **Compose** — a `/generator` card (`GET /compose?players=&symmetry=`); `POST /compose/map` makes it a map. The
   boxes appear as coloured rectangles named as the hand-over names them (`hub-9`, `wool-a-9`).
3. **Layout** — spawns, wool rooms and goals dropped onto the ground (Sketch, Draw → Layout).
4. **Terraform** — the modifier stack one operation at a time, using `?step=` on `sketch/relief` and
   `sketch/columns`, one frame per modifier, with the modifier's name (Hill, Ridge, Canyon, River) as a caption.
5. **Paint** — the band stack applied (`POST …/sketch/paint`), flat colours first.
6. **Structures** — houses on the rooms (`POST …/sketch/seats`).
7. **Dressing** — copied trees, boulders and paths (`POST …/sketch/dressing`).
8. **Build** — `POST …/sketch/finish`, then the camera drops to a player's eye with `render/eye`.

The gate is shown as the composer's own loop: the `model.md` figure, with a counter on "reject → resample" (the
model allows sixty attempts). A short insert contrasts the two terrain designs: the August relief's contours
(`1296cbc7`) against the October modifier list in the Terraform phase.

**Quotes, verbatim.** "It is an intentional abstraction whose product is a low-fidelity prototype of a layout"
(`model.md`) · "The group relief is retired: the modifier stack is the only terraforming" (`16864f7f`).

**Interview slot.** None inside the time-lapse, which runs on music and narration. rockymine's answer to the
research's question about freezing the generator (`02`, Q5) is held for chapter 9.

## 5. Houses work. Trees are hard. (0:55)

**Claim.** A house is geometry with rules, and it became a parametric system in a week. A tree is not, and after
it was measured against the author's own trees the generated tree was deleted and the author's were copied.

**Events.** [19] 2026-08-11 six roofs and storeys; [20] 2026-08-12 75 trees measured; [32] 2026-09-02 the copied
tree; [35] 2026-09-10 the grown tree removed.

**On screen.**
- The six roof forms (Flat, Gable, Hip, Gambrel, Shed, Saltbox) as library cards from `/library/{Kind}`, drawn in
  block sprites, flicking past at a beat each, ending on a row of the 61 styles.
- The tree-showcase world (`pgm-studio-mapgen/corpus/tree-showcase`) rendered with the eye renderer.
- A grown tree beside a hand-built one, both rendered. The grown tree needs a rebuild of the studio before
  `6b0b3f09`; if that fails, the narration carries the numbers over the hand-built tree alone, and the film does
  not fake a broken tree.
- The measurement as an overlay: 30.3% of leaves against wood (hand-built) versus 18.7% (grown).

**Quotes, verbatim.** "Hand-built puts 30.3% of leaves against wood and 10.6% on a diagonal … The grower manages
18.7% and 0.5% at 13.1 neighbours — a solid mass held on at a few points rather than lace." (`c9ea46d6`) ·
"`TreeForm.Grown` built its trees from a recursive skeleton and they came out broken; the author's ruling is that
the form goes rather than gets a knob." (`6b0b3f09`).

**Interview slot.** rockymine Q7 (what a good tree is) closes the chapter.

## 6. Fifteen boards and a line (1:25)

**Claim.** The first AI-made boards were bad in ways that were funny, and in one way that was dangerous: a model
reported confident success, or confident failure, without having checked. The rules and the human oracle grew out
of those lows, and the record does not measure which rule caused which gain.

**Events.** [22] 2026-08-11/12 the first fifteen and MG1–MG13; [24] 2026-08-13 the floating goal; [25]
2026-08-14 the 245-byte shells; [14] 2026-07-02 rules corrected by id; [34] 2026-09-09 fourteen findings to six.

**On screen.**
- **The comedy spot: Spinebreak.** `maps/dtcm/spinebreak`, 145 × 420, rendered for the first time (no render
  exists). A long drone flight down the single ridge with a counter ticking off the eight objective markers in a
  row, then a top-down where the whole board is a thin strip. `<author>mapgen</author>` from its `map.xml` as a
  lower third. The film calls it what the record calls it, "one long 145×420 ridge, an objective at each end", and
  does not call it 500 wide unless the author confirms a different map.
- **The 245-byte map**: `maps/ctw/haiku_r2_canonical/map.xml` opened in full on screen, every byte of it, under
  the report's "plan through export, verified working".
- **The floating core**: a corpus core rendered a few blocks above its ground, the false claim typed and then
  struck through, and the `CLAUDE.md` paragraph "Gameplay decisions have a human oracle" scrolling under it.
- **The rules**: `/rules` filtered by family, one refusal JSON with its id; a counter falling from 14 to 6.
- A title card for the unmeasured: "Which rule made which map better: not measured." Over it, `pgmvox-port.md`'s
  playtest tally.

**Quotes, verbatim.** "rewriting a capture board's wool markers into monuments put every goal at the back of a
corridor it never wanted" (`b95f3d07`) · "no teams, no spawns and no objectives, over region files that are
largely empty" (`README.md`) · "Run 1's core failure was not a system limitation, but a reading failure." (Haiku run
2) · "The corpus says what authors did and the code says what the tool does; neither says what is correct."
(`6eec9b8b`) · "Rules are numbered for correction by id ("WL3: no, 15")." (`10137274`) · "Of the faults the author
found on 10 October, the studio would have caught nine, partly caught four, and not caught or could not have
built seventeen" (`pgmvox-port.md`).

**Interview slots.** rockymine Q4 (the floating core) after the strike-through; Q10 (one rule that helped, one that
harms) at the unmeasured card; Tttie Q8 (the low point) and Q5 (what an outsider gets wrong) as the comic button.

## 7. A tool the AI uses (1:40)

**Claim.** The studio's real user became a model. The API was made to describe itself, so that a model that hits
a refusal can ask what it means; and the models differ most in whether they read before they claim.

**Events.** [23] 2026-08-13 "a reimplementation, not a caller"; [26] 2026-08-15 one Finding, the rules API; [27]
2026-08-15 Grok blind; [29] 2026-08-19 OpenAPI, "the seventh driver"; [30] 2026-08-20 one front door; [32]
2026-09-02 text twins; [37] 2026-09-21 the same-day comparison; [38] 2026-09-22 Opus 5.5; [40] 2026-09-26 → 28
pgmstudio.de live; [41] 2026-09-30 → 10-04 `PUT source`, `kit.py`, glossary.

**On screen.**
- **The words a model must read**, as an animated visualisation from `timeline.md`'s word counts: a column of
  document pages for each date, falling from 11,030 words to 3,267 on 2026-08-22, growing back to 16,505, then the
  whole 39,860 with the skills and the gameplay documents. Beside it, the warm-up skill's warning about the two
  layout files ("397k · 367k" tokens, "Either one ends the run") as two pages too tall for the frame. The model
  logos sit at the foot of the stack.
- **A refusal and its answer**: a real refusal from the session's studio, then `GET /api/rules?rule=<id>`
  answering it, then `/api-docs` in the browser, then the header of `GET /api/kit.py`.
- **A picture and its twin**: `render/eye` and its `?format=text` reading side by side.
- **The 21 September comparison** as a catalogue table on screen (the eight boards' walked · scrambled · barrier ·
  dead from `03` §2, and the four Haiku specs' refusals), each board's top-down rendered beside its row.
- **pgmstudio.de**: its home page and `/maps` recorded headless; the account menu's *Tokens* page with no token on
  screen; a `429` with `Retry-After` from the queue, shown as JSON.
- The activity curve's **second peak**, W40, with its annotation.

**Quotes, verbatim.** "The deeper problem is that `tools/*` is a reimplementation, not a caller." (`aa429eb3`) ·
"tools/drive.py is the seventh driver written against the API and its README says what the six before it did: read
the status code and threw the findings away." (`88bc0baa`) · "every fault below is one the author could not have
seen, because each of them answers 200" (quoted in `88bc0baa`) · "I did not have a running studio (no .NET 10, no
MariaDB)." (`grok-experience.md`) · "It is what lets a Claude Code session drive the deployed studio" (FEATURES,
RP76).

**Interview slots.** rockymine Q8 (who you pictured using it) over pgmstudio.de; Tttie Q6 (have you used it); the
shared Q4 (one sentence of advice to the next model) as the chapter's last line, one answer per person.

## 8. The finish: five hours by hand, then real textures (1:20)

**Claim.** Opus 5's Millrace had the right ground and looked wrong; two people fixed it in five hours, and almost
all of it was theming. What the flat pictures could not show the model was the look, and real block textures were
the turning point.

**Events.** [31] 2026-09-02 Millrace by hand; [33] 2026-09-05 the slope axis; [36] 2026-09-19 "None of it is
enforced anywhere"; [39] 2026-09-27 real textures and the painted boards.

**On screen.**
- **Millrace three ways**, one camera, three worlds: `maps/dtcm/millrace` (Opus 5), `maps/dtcm/millrace_by_hand`
  (rockymine and Ruediger_LP), `maps/dtcm/millrace_revamp` (Fable 5.1 restating the hand work), as a wipe across
  the same frame. The overlay: "29,954 of 35,610 columns keep their surface height exactly."
- **Flat against textured**: `render/eye?flat=1` and `render/eye` of the same frame, which the studio draws as a
  built-in before and after, then `render/topdown?subject=ground` beside it.
- **The slope axis**: one hillside painted by height bands, then by slope, from `GET …/incline?format=text`.
- **Map walls**: held until the author says what the phrase means (see the asks). If it is the void-facing wall
  runs, a render along one board's wall; if not, the shot is cut.

**Quotes, verbatim.** "myself (rockymine) and Ruediger_LP spent 5 hours to complete Millrace." · "the map
authored by the agent provided a great basis." · "essentially all that was done is theming and some dressing … but
most comes simply down to better theming and using the custom trees." (`review/rockymine-ruediger-millrace.md`) ·
"two noisy blocks of one colour are one calm grey in a flat picture and static on the ground, and that is the fault
authors keep making and no read could show." (`3be000d5`) · "None of it is enforced anywhere" (`WHAT-A-BOARD-IS-
MADE-OF.md`).

**Interview slots.** Ruediger Q2 (first look at Millrace), Q3 (who did what) and Q6 (the old-school dress) over
the three-way wipe; rockymine Q6 (why taste is written down, not enforced) closes.

## 9. Starting again (1:25)

**Claim.** In October a model stopped driving the studio and wrote the map directly, and the result was as good:
the gap was in what the studio let an author say. So the studio's first approach — rectangles on a grid — was
retired, and then the generator was frozen.

**Events.** [42] 2026-10-07/08 Riftwater and pgmvox, 86 commits in a day; [43] 2026-10-10 "comparable quality";
[44] 2026-10-15 the port programme; [46] 2026-10-18 the plan retires; [47] 2026-10-24 the modifier stack; [49]
2026-11-13 the freeze.

**On screen.**
- Riftwater (`freeform/lib/boards/riftwater/renders/30-iso-board-se.png`, and a fresh eye-renderer orbit of
  `maps/dtcm/riftwater`).
- The 10 October experiment as a pair: Abbeymoor in the studio and Abbeymoor in pgmvox, both Sonnet 5.5, side by
  side with the author's one-line verdict on each.
- The port's nine phases as a board of cards filling in, ending on "the pgmvox programme has shipped or parked
  every phase" (`bb53150a`).
- One board before and after: plan rectangles against a modifier-built sketch, as `render/isometric`.
- The freeze: the commit message `371e6935` alone on screen while the activity curve drops to its November
  floor (W45–W47: 19, 31, 0).

**Quotes, verbatim.** "The leap came from moving the decisions the studio makes for an author back into the
author's hands, and from a loop that checked them." (`freeform/QUALITY-LEAP.md`) · "the two tools made boards of
comparable quality" (`experiment/RESULTS.md`) · "The goal is a board built through the deployed studio that the
author cannot tell apart, by quality, from one built with pgmvox. Not the same board — the same ceiling."
(`pgmvox-port.md`) · "The author froze the layout generator: nothing changes what the composer makes."
(`371e6935`). The Abbeymoor verdicts are the author's points as an agent wrote them down (`REVIEW-1.md`), so they
appear as attributed paraphrase, not as the author's voice.

**Interview slots.** rockymine Q9 (relief or loss) after the experiment pair; the research's question on freezing
the generator (`02`, Q5) at the freeze.

## 10. By hand (1:55)

**Claim.** The newest map was built by a person, underground and inside a mountain, for a contest that was then
cancelled. Six AI entries had all made the same choice; the agents' compositions of the author's map were each
rejected; and what the study learned is the film's through-line. Then the year, side by side, and the people.

**Events.** [45] 2026-10-16 six blind entries; [48] 2026-11-02 → 11-07 the rejected compositions; [50] 2026-11-27
the study; and, as the present tense, [50]'s studio branch of 2026-11-23.

**On screen.**
- **The machines' entries**: the six 2026-10-16 boards (`maps/dtcm/{rimefire,emberfrost,rimeglow_rift,thawline,
  hoarfire,rimeburn}` on branch `claude/minecraft-bunker-walls-k90feq`) as a grid of six, each split into a winter
  half and an autumn half.
- **The human's entry**: the author's world, rendered with the eye renderer — the bunker in the mountain, the core
  in the facade, the wool lane under the shelf — and an x-ray cut down through its levels (wool lane y 4–8, hall
  y 23, core room y 47, roof y 59). This needs the author's world folder; without it, the viewer carries the shot.
- **The viewer's "Räume und Wege" preset** with the 42 labelled spaces lighting up; the retaining walls (19, 13
  and 14 blocks tall) outlined.
- **What a person can build**: the Eismulde as an agent drew it (49 lines, 158 points) beside the author's four
  long lines (27 points), as a diagram from `study/simplify/eismulde-schlank.txt` and `mid-7/eismulde-punkte.csv`.
- **The year side by side**: the twelve candidates of `03` §4 in time order, each rendered from one matched
  camera, sliding into a row — Emberfall, Spinebreak, Haiku R2, Quillon Barrow, Holdfast, Grok Ridge, Wheal Hazel,
  Millrace, Quatrefoil, Gypsum Reach, Riftwater, Coldstore — then the author's hand-built map last, set apart.
- **Where it stands now**: pgmstudio.de's home page and the newest branch's `TODO.md` diff, the board where author
  and agent talk.
- **The names**: rockymine, Ruediger_LP and Tttie as characters in their real skins, standing in the hand-built
  map, with the models named beside them as the credits roll.

**Quotes, verbatim.** "All six chose Destroy the Core … and all six split one ground into a winter half and an
autumn half." (`0e7acb64`) · "The author then built the map themselves, and the study's task became understanding
it rather than replacing it." · "The map is hollow, and agents treated it as solid." · "Checks that only advise get
passed over." · "A retaining wall does a big job or it is not there." · "How a map plays is the author's call; it
cannot be derived from the code." (`LESSONS.md`, `study/variants/BRIEF.md`) · and, last, "a geometric rule is not a
design."

**Interview slots.** rockymine Q11 (the moment you picked up the tool), Q12 (what a tool could learn) and Q13 (which
variant surprised you); Ruediger Q11 and Tttie Q4 and Q7 (the contest, hybrids); the shared Q1 (where the line is
now) and Q5 (one map to show) over the side by side; the closer about the verification pipeline as the film's last
spoken line before the credits.

---

## Where the interviews slot in

The interviews are not yet recorded, so every slot above is a place, not a promise. The film is cut first with the
narrator alone, and an answer replaces a line of narration only where it says the same thing better or says
something the record cannot. The map of questions to chapters:

| Questions | Chapter |
|---|---|
| rockymine Q1; research `01` Q1, Q3, Q7, Q8 | 2 |
| rockymine Q2, Q3; research `01` Q9, Q10 | 3 |
| rockymine Q7; Ruediger Q8 | 5 |
| rockymine Q4, Q10; Tttie Q5, Q8 | 6 |
| rockymine Q8; Tttie Q2, Q3, Q6; shared Q4 | 7 |
| rockymine Q5, Q6; Ruediger Q1–Q7, Q9, Q10 | 8 |
| rockymine Q9; research `02` Q5 | 9 |
| rockymine Q11–Q13 and closer; Ruediger Q11; Tttie Q1, Q4, Q7, Q9, Q10; shared Q1, Q2, Q3, Q5 | 10 |

Tttie Q1 (who you are in this) has to be answered before any of Tttie's other answers can be placed, because the
record holds nothing about Tttie.

## Needs from the author

Each is an ask that blocks a named shot or line.

1. **The hand-built world.** The world folder of the author's fire-and-ice half (stage B), and if possible the
   earlier sketch world (stage A, four region files). Neither is in any repository, and chapter 10's main plate
   depends on them.
2. **Which map is the 500-wide line-up?** Spinebreak is 145 × 420 with four monuments and four cores on one axis;
   Hollow Crown is 100 × 120 with its objectives exactly in line. A fresh render of each will be sent; the author
   names the one, or points to a board in the studio database or on pgmstudio.de.
3. **Who Tttie is**, and in what role the film should name them.
4. **Real skins and usernames** for rockymine, Ruediger_LP and Tttie (skin files or the usernames to fetch them
   from), and each person's consent to appear by name and skin.
5. **Who "michael" is** in the commit history. Every on-screen `git log` will mask emails either way.
6. **Logos.** The brief allows the model names and logos; confirm the set (Claude's Opus, Sonnet, Haiku and Fable;
   Grok; and Google AI Studio, which made the first repository) and whether the film may show product logos or
   should use name cards.
7. **The first day of pgmstudio.de.** The record only shows it ran on a hand-started script before 2026-09-28.
8. **"Then map walls."** What the phrase refers to: the painter's wall bucket and void-facing wall runs, the bedrock
   approach wall of 2026-10-16, or something else.
9. **Which tool draws the loft lines in game**, and the date the half was built.
10. **Quotes that are recorded only as paraphrase.** May the film quote "essentially perfect" (Riftwater) and "what
    I always wanted" (Curio Square) as the author's words, and what was the wording of the "barren" remark of
    2026-09-28? Until confirmed they appear as attributed paraphrase.
11. **Why C#**, in the author's words. "A language the author can read" is in the brief and nowhere in the record.
12. **Why the studio was not used for the fire-and-ice map.**
13. **A Thunder-series map** to stand for what the model cannot express, from the corpus clones.
14. **Voices.** Whether interview answers will come as recordings in the speakers' own voices, as text for the
    narrator, or as text on screen. The film will not put a synthetic voice in a real person's mouth.
15. **Recorded matches.** Whether the July traffic data (105 matches on ingwaz) may be shown as a heat map, and
    whether it carries player names that must be hidden.
16. **Approval** of the through-line, the ten chapters and the 14-minute length.

## Contradictions with the brief

| The brief remembers | The record says | Source |
|---|---|---|
| The CTW repository was made "at the start of the year" | First commit 2025-09-28, last 2025-10-03: autumn 2025 | `01` corrections |
| In the CTW repository, "something drawn in the browser could become downloadable blocks" | CTW-Layout-Generator exports only JSON ("Download JSON"). The first downloadable blocks are a `.schematic` in MinecraftLayoutEditor, 2025-10-12 (`d961f6a`) | `01` corrections |
| Python, "then the move to C#, a language the author can read" | MinecraftLayoutEditor was already C# (Blazor WebAssembly) in October 2025, so the C# era came before the Python one and pgm-studio is a return. No reason for C# is written anywhere | `01` corrections, §2 |
| A 500-block-wide map with monuments and core in one line | The best match is Spinebreak, 145 × 420, eight objectives along one 400-block axis; the runner-up is Hollow Crown, 100 × 120. Nothing 500 wide fits | `03` §4 |
| A "fire and ice contest" map | The contest was cancelled and the map is now an ice map; both halves are the same design turned 180°, not fire against ice | `04` §1 |
| Texturing: real textures, "then map walls" | Real textures are dated (2026-09-27). The phrase "map walls" does not occur in the studio's record | `02` Beat 3 |
| "Haiku and Sonnet still struggle" | True of Haiku: no Haiku board after the first fifteen carries a theme or a prop, and none built on 2026-09-21. Not plainly true of Sonnet: all four Sonnet 5 boards exported on 09-21, and on 10-10 the author said Sonnet 5.5's Abbeymoor in pgmvox "really looks like a place" (paraphrase recorded by an agent) | `03` §2 |
| The pgmvox port happened "because the first approach was limiting" | Partly. The 10 October experiment found the two tools "comparable"; the gap was put down to spend and pgmvox's open vocabulary, and the studio's plan as "rectangles on a 5-block grid; no reasons" | `02` Beat 6 |
| Find the hand-built branch with `git ls-remote` (the brief does not say which repository) | It exists only in pgm-studio-mapgen, not in pgm-studio | `04` |

One disagreement sits between two research files rather than with the brief: `02` dates the birth of
`docs/generator/model.md` to 2026-07-14 (`deb62961`), while `01` says that commit created
`docs/contracts/map-generation.md` and that `model.md` was born on 2026-07-27 (`3686ad38`). The outline follows
`01`, which names both commits, and the timeline avoids the date.

## Risks, and what is staged versus real

**Real.** Every Minecraft picture is a render of a real world folder with the game's own block sprites, through the
same eye renderer the previous film used; every document, diff and commit message on screen is the real text at
the real commit; the activity curve, the model band and the context visualisation plot the research's numbers;
the generator time-lapse is a real build on the session's own studio, compressed in time and nothing else; the
screen recordings are the old repositories running.

**Staged, and labelled as such where it could mislead.** The character rig scenes (rockymine, Ruediger_LP, Tttie
and the models as figures), the sets from `sets/sets.py`, the graph morph in chapter 3 (a diagram), the
eleven-reasons text sequence (real words, staged layout), and the narrator, which is a synthetic voice.

**Risks.**
- **The old repositories may not run.** MinecraftLayoutEditor pins `10.0.0-rc.1` WASM packages, pgm-map-studio's
  import needs a world, and pgm-studio at `7b30744a` or `f25a9249` needs .NET 10 and MariaDB. The fallback is the
  code and its file tree on screen, never a mock-up of a UI that did not run.
- **The grown-tree rebuild** before `6b0b3f09` may not be feasible; chapter 5 then shows the numbers, not a fake.
- **The hand-built world may not arrive.** Chapter 10 then relies on the viewer, which draws the lofts rather than
  blocks.
- **Attribution.** Many "author" lines are an agent's summary of the author. The film voices or quotes as the
  author only what is in the author's own words (`review/rockymine-ruediger-millrace.md`, the `[author]` paragraphs,
  and approved interview answers).
- **Privacy.** Committer emails appear in raw `git log`; every shot masks them. Tokens never appear.
- **The deployed studio is shared** (two cores, about 4 GB). It is filmed, not worked: every render and the
  time-lapse run on the session's own studio.
- **Textures need the 1.8.9 client jar with Mojang's EULA accepted** on the rendering machine; without it the
  eye renderer refuses (`RQ10`).
- **Length.** Ten chapters in fourteen minutes leaves little air; if a cut is needed, chapter 5 folds into 4 and the
  cold open shortens to 0:25.

## Build plan

The orchestrating session only organises; every phase below is done by Opus agents, several in parallel where
the phase allows. Sizes are in sessions.

**Phase 1 — Scouting (one session, four agents).** One agent stands up the session's own studio by
`pgm-studio/docs/cloud-setup.md`, accepts the texture EULA where allowed, and re-points `eye/eye.cs`, `plates.py`,
`vo.py`, `mix.py` and `docs.py` at a new `film/history/` tree. One tries to run the three early repositories and
pgm-studio at `7b30744a` and reports which can be recorded. One renders a still of each of the twelve side-by-side
worlds, plus Spinebreak and Hollow Crown for the author's ask 2. One checks out the fire-and-ice branch and
screenshots the viewer with `check.js`. Output: a plate inventory, and the renders sent to the author with the asks.

**Phase 2 — Script and quote sheet (one session, one agent).** The narration as `script.py` lines with target
timings per chapter, and a quote sheet giving every on-screen quote with its file and commit, checked against the
source. The author reviews this before any plate is final.

**Phase 3 — The generator time-lapse (one to two sessions, one agent).** One map through compose → layout →
terraform (`?step=` per modifier) → paint → seats → dressing → finish → `render/eye`, from one fixed camera, as a
frame sequence with a caption track.

**Phase 4 — Chapter plates (two to three sessions, four agents in parallel).** Chapters 2–3: the screen recordings,
the 23-minute diff, the node-types comparison. Chapters 5–6: houses and trees, Spinebreak's flight, the 245-byte
file, the struck-through claim, the rules. Chapters 7–8: the context visualisation and the activity curve (with the
`dataviz` skill), the API recordings, the 21 September table, Millrace three ways, flat against textured. Chapters
9–10: Riftwater, the Abbeymoor pair, the port board, the six contest entries, the viewer, the Eismulde diagram and
the year side by side. The hand-built world's renders wait for the author's files.

**Phase 5 — Animation and overlays (one to two sessions, one agent).** Shots in `film/shots/` order, the character
rig placed in the worlds with depth, the recurring activity curve, the chapter cards, the logos or name cards.

**Phase 6 — Voices and mix (one session, one agent).** `vo.py` records the narration and solves the timeline,
`capture.cjs` renders the frames, `mix.py` places voice, music and effects and writes the subtitles, ffmpeg joins
them. A clean-for-dub version is exported as before.

**Phase 7 — Interviews (after the answers arrive, one session).** Answers placed in the slots above, narration cut
where an answer replaces it, and the film re-mixed.

The order is 1 → 2 → (3 and 4 in parallel) → 5 → 6 → 7, with the author's review after phase 1 (the asks and the
renders) and after phase 2 (the script).
