# 04 — The hand-built map: the "fire and ice" experiment

Research for the history film, beat "the newest experiment". Read on 2026-11-27.

**Where it was read.** Branch `claude/compassionate-cerf-fg7m17` exists only in **pgm-studio-mapgen**
(`git ls-remote` on pgm-studio returned nothing). Fetched fresh and read at commit
**`4486636d9d62139cc87b8dc2dd7ba4748bfc442b`** (2026-11-27 00:50:46 UTC) with `git show FETCH_HEAD:<path>`; the
working tree was not touched. The fetch moved the remote ref from `92ee7f55` to `4486636d`, so the last commit
had landed shortly before. The branch forks from main at `fc3f9254` (merge of PR #40, 2026-10-27). The
illustrating artifact (https://claude.ai/code/artifact/555b1fbe-f6ae-4b8b-b195-06643ab38297, page title
"Feuer und Eis Ebenen") was read with the Artifact tool; its five files (`index.html`, `map.json`,
`variants.json`, `labels.json`, `compare.json`) have the same byte sizes as the branch's
`sketches/fire-and-ice/study/viewer/` files, so the artifact is that folder published.

Everything below is from those two sources unless marked **[inferred]** (my reading, not stated in the record)
or **[uncertain]**.

---

## 1. What the map is

**A CTW + DTC hybrid built by the author (rockymine) as one half, turned 180°.** The branch's README calls it "a CTW
and DTC hybrid for a fire-and-ice contest: a bunker set into a mountain with the core in its face, an underground
wool lane under a flat shelf of terrain, and a valley floor between them" (`sketches/fire-and-ice/README.md`).

**It is now an ice map, and the contest is off.** `study/LESSONS.md` lists, among facts the agents could not
derive: "The contest the map was first made for had been cancelled, and the map is an ice map." The variant brief
opens: "It is an ice map: cold tundra, perhaps with hot springs, or lava caves with lakes underground."
(`study/variants/BRIEF.md`). The film's working phrase "fire and ice contest" is the origin, not the current state.

**Both halves are the same, not fire against ice.** "Both team halves are built from the same blocks. The map is
one design turned 180°, not two materials or two themes facing each other." (`BRIEF.md`). One agent had drawn the
halves as fire against ice; it is listed in LESSONS as a guess.

**The author builds in colour-coded wool with a loft tool.** "A surface is an ordered sequence of lines, each of a
few points, with a ruled mesh between each consecutive pair" (`BRIEF.md`); the simplification sheet for the author
says "Jede Linie: erster Punkt Linksklick, die weiteren Rechtsklicks" — first point left-click, the rest
right-clicks (`study/simplify/eismulde-schlank.txt`). Which in-game tool or plugin this is is not named
**[uncertain — interview question]**. The colours are semantic: light grey = flat walkable floor, yellow = "the
flatter terrain that connects", light blue = "the hillier ground: mountains, knolls", lime/green = retaining walls
front/back (`BRIEF.md`). The author's story for the walls: "workers dug out the slope, and retaining walls hold the
terrain back."

### Two stages, two coordinate frames

The record has **two different author worlds**, in two frames. Do not mix their numbers.

| Stage | World | Frame | Pivot of the 180° turn |
|---|---|---|---|
| A. the sketch (2026-11-02 → 11-07) | the author's "hand-built sketch world", uploaded as four region files, with floating reference copies of bunker and lane | `compose.py`: half x −60…68, z −110…48 | block (24, 48) |
| B. the author's own build (before 2026-11-27) | "the author's own download" of a hand-built half | study / viewer | (59.5, 86.5): (x, z) → (119 − x, 173 − z) |

Neither world is in any repository: "The source world is not in the repository. It is the author's, uploaded to a
session as its four region files" (README) and "The author's world is not in the repository. It is the author's
own download, read as untrusted data" (`study/README.md`).

### The author's half (stage B), as the study measures it

Derived by me from `viewer/map.json` **[inferred arithmetic]**: the half's blocks span **x −15…104, y 0…91,
z −56…101** (marker blocks excluded); turned about the pivot, the whole map's bounding box is **x −15…134 (150
blocks) by z −56…229 (286 blocks)**. 66,754 blocks are exported in the half including 639 marker blocks. A middle
variant may shift the turned half by a few blocks, which changes these.

| Element | Coordinates (study frame) | Source |
|---|---|---|
| Main building (core + spawn) | stone tops x −15…52, z −22…31, y 25–60 | BRIEF |
| Checkerboard roof (light-grey wool + clay) | y 59, x 12–32, z −22…20 | BRIEF |
| Black roof "penthouse" + antenna | y 66–72, x 8–30, z 21–47 | BRIEF |
| Core (obsidian + lava) | x 27–31, z 22–33, in the east facade | labels.json |
| Pit under the core | y 17, purple floor, open east to the ramp | labels.json |
| Core room | floor y 47, west of the core | labels.json |
| Facade's highest exit (over the core) | walk level y 48 | BRIEF, kit.py `COVER_FLOOR = 48` |
| Great hall (ground floor) | floor y 23, L-shaped x 3–32 / z −7…22, ceiling y 37, open east | labels.json |
| Wool lane (underground) | floor y 4–8, 12–25 wide; entries west (x 67–72, z 4–9) and south (z 23–27); a void hole x 89–94, z −2…3 | labels.json |
| Wool lane, open long side | white, around x 82–100, z 28–53, "the opening is deliberate" | BRIEF |
| Lane corner (east end of the middle) | (97, 53) | kit.py `LANE_CORNER` |
| Wool room "(?)" | y 50 on the slope, chests x 52–56, z −39, a beacon under glass at x 55, z −35 | labels.json (the label itself carries the question mark) |
| Spiral stair to the wool | 2 wide, y 10 → y 50, x 56–61, z −39…−23 | labels.json |
| Retaining wall 1 | x 29–76, y 23–42, z −27…−8, 19 tall, "holding the back mountain behind the plaza" | BRIEF |
| Retaining wall 2 | x 71–85, y 15–28, z 28–58, 13 tall, beside the wool lane | BRIEF |
| Retaining wall 3 | x 20–36, y 22–36, z 56–77, 14 tall, holding the plateau | BRIEF |
| Pivot marker | 2×2 plain stone at (59–60, 18, 86–87) — "only marks the pivot" | BRIEF |
| The middle (missing in the author's build) | the halves stand 22–26 blocks apart; 1,955 empty columns at shift (0, 0) | BRIEF |

**Levels.** Read off the labels, the half runs from the wool lane at y 4–8 underground, through the hall at y 23,
corridors at y 17, 24, 27 and 48, the core room at y 47, the roof at y 59, to the attic under the black roof at
y 61–67 **[inferred summary of labels.json]**. `labels.json` names **42 spaces**: rooms, tunnels, stairwells, one
facade and 16 openings. Several are marked "geschlossen, kein Zugang gefunden" (closed, no access found) — e.g. the
chamber west of the core (y 26), the room y 55 (north-west) — which the labeller could not connect
**[whether these are unfinished or intentional is a question for the author]**.

**Objectives.** One core and one wool room per half are labelled; the record does not state the final objective
count per team **[uncertain]**.

**Steepness of the author's ground** (`viewer/compare.json`): all author terrain, 23 lofts, 299 lines, 1,578
points over 13,555 blocks² — 11.6 points per 100 blocks², tilt median **36°**, 42% steeper than 45°. Light blue
(mountains): median 50°, 56% over 45°. Light-grey floor: median 17°.

### The sketch composition (stage A), as `compose.py` builds it

Frame of `compose.py`; from the README table and the 2026-11-07 commit.

| Piece | Where |
|---|---|
| Bunker | the floating copy moved by (−35, −61, −43) onto the original, "as its rough form"; the original's lava core kept |
| Roof plates | clay and light grey at y 67, carried back to x −28 in a six-block checker |
| Wool lane | walk at y 14 on bedrock, raised to y 20 at the south end |
| Flat roof over the underground | bedrock at y 29, "fifteen over the walk", to z −26 |
| Shelf | flat at y 50 |
| Core terrace | y 56 (`TERRACE_Y`, "the bunker's house is solid up to the core's terrace at y 56") |
| Turn | 180° about block (24, 48) |

Build report claims (commit 92ee7f55): "Closure: five openings, all entries; no exposed tunnel; mountain steps 0-2
save ten of 3." A build "takes about five seconds".

---

## 2. What the branch adds

46 files, 6,176 insertions (`git diff --stat main...FETCH_HEAD`). All under `sketches/fire-and-ice/` plus one line in
`README.md` ("`sketches/<name>/` scripts that compose an author's hand-built sketch world into a map, in wool").
**Nothing touches pgm-studio, and no PNG render is committed.**

**Stage A — the composition (superseded).**

| File | Is |
|---|---|
| `compose.py` (740 lines) | the composition, its parameters and point lists |
| `terrain.py` | thin-plate spline for the mountains |
| `loft.py` | curves, lofted surfaces and their voxels |
| `anvilw.py` | "a 1.8 Anvil region writer"; biome Ice Plains |
| `render.py`, `colours.py` | top-down and isometric pictures |
| `README.md` | the composition, its closure readings, colour key |

**Stage B — the study (`study/`).**

| Path | Is |
|---|---|
| `study/README.md`, `study/LESSONS.md` | the study; "what went wrong, and where the limits were" |
| `rec/` (`pieces.py`, `reconstruct.py`, `lines.py`, `run_lines.py`, `export_viewer.py`) | the author's terrain rebuilt as loft lines; the viewer export |
| `viewer/` (`index.html`, four JSON files, `check.js`) | the published artifact and a local screenshot harness |
| `labels/label.py`, `labels.json` | rooms, tunnels, stairwells, facade, openings "from the geometry" |
| `variants/kit.py`, `variants/BRIEF.md`, `variants/compare.py` | the agents' toolkit and gate, the one brief, the density/steepness comparison |
| `variants/mid-7`, `mid-8`, `mid-9`, `cov-2`, `cov-6` | five accepted variants (`build.py` + `variant.json`) |
| `simplify/` | the Eismulde reduced to four long lines |
| `markers/edit.py` | writes points into a copy of the author's world as marker blocks |
| `mid/` | first-round ravine and centre sketches, "superseded by the variants" |

**The reconstruction's number:** "Of the author's 18,801 terrain blocks, 3 lie more than a block from the
rebuild. Of the rebuild's 19,771 blocks, 46 lie more than a block from the author's." A thin-plate spline, the
first approach, "left 146 blocks more than one away" (`study/README.md`).

**The five accepted variants** (`study/README.md`; titles are German, as written by the agents):

| id | slot | title | shift | reading |
|---|---|---|---|---|
| mid-7 | middle | Die Eismulde | (4, 10) | lens basin at y 11, 4–5 below the rims; 10.5 points per 100 |
| mid-8 | middle | Gletscherzungen am Eissee | (3, 8) | a tongue off each plateau, frozen lake at y 11; 9.7 |
| mid-9 | middle | Pingo-Furt | (3, 8) | shallow trough at y 14, two offset pingos; 6.9 |
| cov-2 | cover | Bunker unterm Berg | – | ridge behind the roof; 5.8; fails the final cover rule on 84 columns |
| cov-6 | cover | Firnsattel über dem Bunker | – | firn saddle off the north mountain, flush with the roof; 12.3 |

"The author judged them, and the gate passes four of their builds as they stand." Which model ran the variant
agents is not stated on the branch **[uncertain]**; every commit carries `Co-Authored-By: Claude Opus 5.5`.

---

## 3. What it exposes — gaps and limits, verbatim

The branch never names pgm-studio. Section 3a is what the branch itself says went wrong; 3b sets that against what
pgm-studio's own documents say the studio models, and **3b is my juxtaposition [inferred]**, not a claim the record
makes.

### 3a. Stated on the branch

**Rules passed, design failed.** "Rebuilding the whole map from its structures' footprints failed on nearly every
judgement a player makes." The author rejected each version for, among others: "the surface was not closed",
"stairs stood exposed", "the mountains broke into separate pieces", "a 'floating island' taper had been added
under the terrain without being asked for", "a gorge was cut above the wool room", "the map sat 8 blocks too high",
"a ramp led into the void". Then: **"The lesson that carried over is that a geometric rule is not a design. Every
one of those failures passed some check that existed at the time."** (`study/LESSONS.md`)

**The human gave up on replacement and built it.** "The author then built the map themselves, and the study's task
became understanding it rather than replacing it." (`study/LESSONS.md`); "The composition was superseded once the
author built the map themselves." (`sketches/fire-and-ice/README.md`)

**A hollow map read as solid.** "The map is hollow, and agents treated it as solid. It holds only surfaces and the
empty mass between them. The stairwells and back rooms float in that void, and will be sunk into solid ground
later. Three of the first four covers drew planes low beside the building and left stairwells standing open above
them." (`study/LESSONS.md`)

**Checks read one thing, people see another.** "Every check read the blocks, and the viewer draws the lofts. Agents
clipped their blocks to the span, while their loft lines ran up to 29 blocks past it. The checks reported a pass on
variants the author saw as plainly wrong, and the reports were relayed without being looked at." And: "Checks that
only advise get passed over. Agents reported their numbers and delivered failing variants anyway."
(`study/LESSONS.md`)

**Facts the geometry cannot carry.** "Facts about the map that the agents could not derive had to be stated, or they
guessed." — the pivot stone read as ground height by "every middle agent", fire-versus-ice halves, the cancelled
contest. (`study/LESSONS.md`)

**Colour is meaning.** "Colour carries meaning, and agents painted it as a blanket. Yellow is the flatter ground
that connects; light blue is the hillier ground. A cover that is mostly one colour says nothing about its form."
(`study/LESSONS.md`)

**Scale of a feature.** "A retaining wall does a big job or it is not there. One middle variant dressed its spoil
heaps with small walls. The author's walls hold back a whole mountain or take up a real step: 19, 13 and 14 blocks
tall." (`study/LESSONS.md`)

**A rule worded too strongly.** "'Flat ground in the main flow' ruled out any ravine in the middle. The brief now says
the main flow stays walkable and readable, and need not be flat." (`study/LESSONS.md`)

**Where the middle is, is judged by eye.** "The east end of that span sits at the corner where the wool lane runs out
of the underground, which the author placed by eye." (`study/LESSONS.md`)

**What a person can build.** "A shape an agent builds is not a shape the author can set point by point. The Eismulde's
agent laid lines every 3 blocks across the gap: 49 lines and 158 points for one side. Four long lines along the gap
carry the same basin in 27 points, 96.6% of it within a block." (`study/LESSONS.md`)

**The inferred is not the author's.** "The lines found are not the author's lines. They reproduce the surface to
within a block, but the author's tool holds the true lines and their density." (`study/LESSONS.md`)

**Concepts handed to agents.** "Agents handed a concept produce that concept, so the author had them sent without
one." The first launch named a ravine "the author had liked before. The author stopped it, because the point was to
see what agents find on their own." (`study/LESSONS.md`)

**Exits.** "Sinking every opening behind the facade sank a real exit. … That blocked the south stairwell's west exit,
the one way out at the back that connects to the building's inside." (`study/LESSONS.md`)

**Environment.** "The cloud container could not reach the CDNs the published page loads from." "Agents never saw the
viewer. They judged their work from iso renders of the blocks, and those renders do not show the lofts."
(`study/LESSONS.md`)

**Gameplay stays the author's.** "How a map plays is the author's call; it cannot be derived from the code. … Keep
claims about gameplay modest and turn them into questions for the author." (`study/variants/BRIEF.md`)

### 3b. Against what the studio models [inferred juxtaposition]

1. **The layout model is CTW-shaped, and this map is a hybrid built around a building.** pgm-studio's
   `docs/generator/model.md` says its vocabulary — "hubs, lanes, frontline boxes, wool forms — is *one* way to think
   about a CTW board … an **intentional abstraction whose product is a low-fidelity prototype of a layout**", and
   that a map outside it "simply is not reachable through this model, and no compound should be invented to make it
   so". Here spawn and core share one bunker set in a mountain, and the wool lane runs underneath. In the corpus,
   CTW + DTC together are **3 of 742** objective maps (`docs/pgm/destroyables-and-cores.md`, OB15 table).
2. **Ground as columns versus ground as sheets.** The studio's carve is column-wise: "A subtract has no `y` at all —
   it is a set of `(x, z)` cells … so it cannot hollow a column out from the middle"; underground space is stated as
   "a roofed void" (`docs/tools/sketch.md` §subtract). The author's map "holds only surfaces and the empty mass
   between them" — stacked lofted sheets at y 4–8, 23, 47–59. The studio does have a `tunnel` carve on a line, with
   `cover` 3 (`docs/tools/sketch.md`, modifier table).
3. **No lofted surface.** A grep of all of `pgm-studio/docs/` for "loft" finds only a building's loft
   (`tools/sketch.md`, "The loft over it is one space"; `world-export/structures.md`), never a surface lofted
   through lines. The study had to write its
   own (`loft.py`, `rec/lines.py`) **[absence of a feature inferred from docs, not checked in code]**.
4. **Underground is in the author's law, not yet in the reads.** `docs/gameplay/approaches.md`: "A tunnel under the
   ground is not scenery beneath the board. It is a second way to an objective … a read that cannot see them is
   describing half of it." `match-flow.md` §10.5: "A point can be underground, and one point can stand over another."
5. **Look is not gated.** `WHAT-A-BOARD-IS-MADE-OF.md` (mapgen): "None of it is enforced anywhere — no gate asks
   whether a board looks like anything." The study's answer was to turn the author's rulings into a gate
   (`kit.write` "refuses a variant that breaks a hard rule") — and still: "a geometric rule is not a design".
6. **The studio was not used at all for this map.** Every step ran in standalone Python over 1.8 region files
   (`anvilw.py`, `markers/edit.py`), shown in a three.js page, not on pgmstudio.de **[inferred from the file list;
   the branch does not say why]**.

---

## 4. Timeline

All dates from commits on the branch (UTC) unless stated.

| Date | What | Ref |
|---|---|---|
| 2026-10-15 | **Prequel:** "Fire and ice: five study forms composed on one 160 by 300 board" — volcano and winter study forms as stamps, a composer page, world `maps/other/studies_fire_and_ice` | `d67e59a2`, on branch `claude/minecraft-bunker-walls-k90feq`, not on main |
| 2026-10-16 | **Prequel:** "Six blind entries to a Fire and Ice contest" — three Opus 5.5 and three Sonnet 5.5 agents; "All six chose Destroy the Core … and all six split one ground into a winter half and an autumn half." | `0e7acb64`, same branch; BOARDS-BUILT entry there |
| 2026-10-27 | main at `fc3f9254` (PR #40); the branch forks here | |
| 2026-11-02 23:43 | "Compose the fire-and-ice sketch into one map, in wool" — reads the author's hand-built CTW/DTC sketch world | `e85cc29a` |
| 2026-11-05 21:27 | "Close the fire-and-ice composition: solid ground, entries only" — the ground had been "hollow: every surface was a one-block sheet over open air" | `83c32ed6` |
| 2026-11-05 21:51 | "One continuous mountain band" — `band.py` | `f22023bb` |
| 2026-11-07 21:28 | "Rebuild the fire-and-ice composition from its structures' footprints"; `band.py` retired | `92ee7f55` |
| between 11-07 and 11-27 | the author builds the half themselves — **date not recorded** [uncertain] | LESSONS.md |
| 2026-11-26 00:44 UTC? | artifact version id `1795653894-0bda`; read as a Unix time it is this date [uncertain: may not be a timestamp] | Artifact |
| 2026-11-27 00:50 | "Fire-and-ice study: reconstruction, viewer, labels and gated variants" — the whole `study/` | `4486636d` |
| 2026-11-27 | the film brief names the branch and the artifact (`2d16be17`, `1e86f019` on `mappies-film`) | |

The commits on the branch name one Claude session (`session_011o9Htmiy2kLAu7qeQGQ2TC`) for all five.

---

## 5. What is filmable

| What | Where | Note |
|---|---|---|
| **The 3D viewer** (best single shot) | https://claude.ai/code/artifact/555b1fbe-f6ae-4b8b-b195-06643ab38297 | German UI. Toggles: Mesh/Blöcke, Ganze Karte/Hälfte, Linien (loft lines + points in fire orange), Netz (wireframe), Namen; presets "Nur Gelände", "Gelände und Untergrund", "Nur Bauwerke", "Räume und Wege"; variant pickers for Mitte (1–3) and Gebäude (1–2). Clicking a labelled space shows name and coordinates. A time-lapse is possible: layer by layer, then the variants swapped in the middle. |
| Viewer, offline | `sketches/fire-and-ice/study/viewer/` on the branch (`git worktree add /tmp/fireice FETCH_HEAD`) | needs a local server; `check.js` screenshots it with three.js r128 from `npm pack three@0.128.0` |
| Lines vs. dense lofts diagram | `study/simplify/eismulde-schlank.txt` (27 points), `study/variants/mid-7/eismulde-punkte.txt`/`.csv` (158 points) | "49 lines and 158 points" vs "27 points" — a clean before/after graphic |
| The "what went wrong" list | `study/LESSONS.md` §"The composition before the study" | eleven rejection reasons, good as on-screen text |
| Labelled building | `study/labels/labels.json` (42 spaces) | via the viewer's "Räume und Wege" preset |
| The composed sketch (stage A) | `compose.py` + `render.py` | **needs the author's sketch world**, which is not in any repo; render commands are in the README |
| The author's world | not in any repository | ask the author for the world folder (both the sketch and the build) — the main missing plate |
| Prequel boards (AI entries, 2026-10-16) | worlds `maps/dtcm/{rimefire,emberfrost,rimeglow_rift,thawline,hoarfire,rimeburn}`; renders `freeform/lib/boards/<name>/renders/` (17–26 PNGs each) | on branch `claude/minecraft-bunker-walls-k90feq` (`283f7140`) — a natural "AI entries vs. the human's entry" contrast |
| Prequel study board (2026-10-15) | `maps/other/studies_fire_and_ice`; `freeform/lib/studies/fire-and-ice/renders/iso-nw.png`, `iso-se.png`; `composer.html` | same branch |

No world folder, render or screenshot of the hand-built map is committed anywhere I could find.

---

## 6. Open questions for the author (feed into interviews)

- Which tool draws the loft lines in game, and when was the half actually built?
- Was the contest cancelled before or after the build started, and did that change the design?
- Is the "Wollraum (?)" at y 50 the wool room? How many wools and cores per team?
- Are the closed, unconnected rooms the labeller found unfinished, or meant to be sealed?
- Why was the studio not used for this map at all?
