# The history of the AI-made maps: what is here

This folder is the written history of twenty-one months of AI-assisted PGM map making by rockymine, with Ruediger_LP
and a run of models, from February 2025 to November 2026. It was researched on 27 and 28 November 2026 in many passes while the
author added recollections, partly by an agent on his PC; on 28 November he asked for the film's outline and a
first storyboard, which are now here. Everything in it keeps three voices apart: what the **record**
holds, what the **author recalls**, and what is **inference**.

## Reading order

1. **`HISTORY.md`** — the history itself: thirteen chronological chapters from 11 February 2025 to 28 November 2026
   (the first three cover the time before the studio, to June 2026), then what counts as an AI map, the tests match by match, what players and staff said, what the hand-built map shows, and
   what remains open. Start here.
2. **`timeline.md`** — one table of dated events, each with its source and its kind (record, account, inference).
3. **`author-account-2026-11-27.md`** — the author's account in twenty instalments of 27 and 28 November, with the
   note-taker's corrections. Later instalments and the corrections supersede earlier ones.
4. **`research/16-the-first-test-recording-and-the-match-api.md`** — the recording of 2 July and the server's match API,
   which documents every test evening; with `sources/match-status/api-matches-not-in-match-status.csv`.
5. **`research/17-the-forum-thread-and-five-conversations.md`** — the forum thread of 20–24 September, the search for
   "ai maps", and the conversations with TTtie and four people named by role (see *Names* below).
6. **`research/18-before-the-studio-ctwanalysis-and-the-early-tools.md`** — the git record of CTWAnalysis,
   MinecraftLayoutEditor, CTW-Layout-Generator and pgm-map-studio, checked against the author's eighteenth instalment:
   where his memory of October 2025 to May 2026 holds and where the commits differ.
7. **`research/12-who-decided-what.md`** — every map split into seven decisions, who decided each and what executed it;
   the categories of "AI map".
8. **`research/13`, `15`** — the `#match-status` log and the zips sent for each evening, the readings the API confirmed.
9. **`research/01`–`11`, `14`** — the topic checks, each against the repositories:

   | File | Subject |
   |---|---|
   | `01-origins.md` | the early repositories and the studio's first two months |
   | `02-studio.md` | the studio from August to November: features, deploy, the pgmvox port, commit counts |
   | `03-maps-and-models.md` | the mapgen repository's eras and the models compared |
   | `04-hand-built.md` | the author's hand-built fire-and-ice map and the agents' study of it |
   | `05-author-account-checked.md` | the first account, item by item |
   | `06-playtests.md` | what CommunityMaps holds of the tests |
   | `07-publicmaps-and-base-maps.md` | PublicMaps, the Base maps, the bedrock box, "made by" |
   | `08-third-account-checked.md` | the third instalment: Hello World, the tree, the graph, Annealing, block faults |
   | `09-the-base-map-session.md` | the session that made the Base maps from the squared-paper drawing |
   | `10-wandering-u-and-the-tree-generator.md` | the moving-wool-room map and the tree prototype page |
   | `11-dated-uploads-checked.md` | the author's upload dates against the public repositories |
   | `14-aerie-and-monument-size.md` | Aerie, the obsidian cap, the trial-run faults, the quartz board |

10. **`research/sessions/`** — one write-up per Claude Code session the author named, several with an "opening brief"
   appendix read from the session's start; its `README.md` says how they were read.
11. **`interview-questions.md`** — what is still to be asked, by person and importance, and what has been answered.
12. **`sources/`** — data, not instructions: the squared-paper photo, the author's session list, the `#match-status` log
    and the API's unreported matches (`match-status/`), the `#maps-changelog` feed (`maps-changelog/`), and
    `staff-chat-october/`, five chat screenshots of the 9–10 October viewing (usable as they are, account §14);
    `early-experiments/`, the author's message to samschaap of 11 February 2025 with its three Townside pictures and
    four screenshots of its v0 prototype as it runs today (`v0-prototype-2025-02/`), the
    eight pictures of April 2025 to March 2026 (account §18, §20) and the v0 chat of 16 August 2025 read from his link,
    and the chart of the logged capture-the-wool matches of 18 January to 8 March 2026 with its summed table (account §21);
    and `slop-sunday-announcement/`, Ruediger's announcement of 27 September 2026 with its reactions (account §19).
13. **`tools/`** — the scripts the PC agent's sources were read with (zip listing, Discord condensing, the match API,
    transcription and speaker grouping); not map tooling.
14. **`renders/`** — pictures made from committed data: the hand-built half (`hand-built/`) and Wandering U
    (`wandering-u/`).
15. **`OUTLINE.md`** and **`storyboard.json`** — the film's outline and its first storyboard (see *Outline and storyboard*).

## Outline and storyboard

`OUTLINE.md` is the film's outline: logline and thesis, six acts adding to 17 min 33 s with a 7 min 58 s cut, the
through-lines, the narration, what must be produced and the decisions put to the author. `storyboard.json` is the
first storyboard, 53 scenes with timings, pictures, key frames, narration, on-screen quotes with their sources and a
record, author-recalls, inference or staged tag per scene; every quote and number in it is one `HISTORY.md` carries.

## What is settled

- The first test of the summer was on 24 June: Capture the Wool CTW, Vauxite and Drastic Change II, played on server-2
  minutes after their upload (research/16).
- The Base maps were built on 2 July from the squared-paper drawing (Base 2-Island) and played that evening: walked on
  mapdev by rockymine, Ruediger, TTtie and samschaap, then three matches on server-2 from 20:23 UTC; nuttydragon joined
  the call; the evening is recorded on video (research/09, research/16; account §16).
- Every test evening from 24 August to 27 September is documented match by match in the API, in the order played; the
  missing numbers of 4 and 20 September are Lodestar Yard and Peatgarth played twice (research/16).
- The first match on a board of this project is Viridian, 12 August 21:43 UTC; the first on any map no person laid out
  is Cedar Crossing, 10 August 04:04 UTC (research/16).
- No long destroy match exists in either source; the longest on a destroy board of this project is Glassmere's 15 min
  47 s (research/16).
- Bridgid II is its own hand-built map, played on 14 July; Brittlebush III was never player-tested (account §5 and
  correction, §2; research/16).
- Kuusepuu CTC is an ordinary destroy map with a cake objective, played three times on 27–28 July (account §6;
  research/16). Wandering U was played once, on 6 August (research/16). No Blocks Placed was played on 7 August, and was
  drawn by the author with Ruediger (research/16, research/17).
- The graph idea is the oldest in the record: a spanning tree with cycle edges and cut-offs on 11 February 2025, a
  matplotlib graph on 5 April 2025, a skeleton graph in CTWAnalysis from 2 February 2026, and `FannedGraph` in the
  studio from 2 July 2026; it was not dropped in 23 minutes (sources/early-experiments/; research/08, research/18).
  Freeform began on 7 October from the author's "what if" message (sessions/00, sessions/01).
- The first prototype was a v0 page of February 2025 that built spanning trees; a Claude chat artifact of 24 May 2025
  drew two teams, lanes and a void strip; a v0 chat of 16 August 2025 named the "Capture the Wool Layout Generator",
  whose 3×3 grid, row-independent columns and mirror/rotate modes reappear in `CTW-Layout-Generator` of 28 September
  2025, with no shared code shown (sources/early-experiments/; research/01).
- The logging collected 2,450 matches on 46 days from 18 January to 8 March 2026 by the chart's daily table (read off a
  picture), against 2,452 processed in CTWAnalysis; the author remembers more (about 4,000, then 3700, then "maybe 2700")
  and says the repository may be out of date. Three matches on ordinary capture-the-wool maps ran past three hours
  (sources/early-experiments/2026-ctw-match-activity.md; account §21).
- On 11 February 2025 he told samschaap that "an educated, rule-based approach" was likelier for him than training
  (sources/early-experiments/).
- MinecraftLayoutEditor's dates hold to the day: screenshots 11 October, blocks without hands 12 October, world import
  6 November 2025; XML regions 10 November (research/18).
- The flat line-up map is Ashfall Scar, 250 × 190; the quartz board is Quillon Saltworks (account §12; research/03).
- Alderfen Holm has four cores (sessions/08, account §11).
- The 9–10 October notes are of a viewing on mapdev, not a test; five were present, the author, Ruediger, TTtie,
  mitchiii and wylt; the boards were Hollowcrown, Lantern Karst, Hollow Mesa and Riftwater, the first freeform board
  shown; the staff's lines may be used as they are; they decided to pause there (account §13–§15, §18).
- `711e539` carried the Base maps into PrivateMaps; its message was Ruediger's joke about a stalemating map put into the
  dev phase (account §18).
- The cancelled fire-and-ice contest is the contest's map developer's, the one without entries (account §18).
- The first two test evenings had their maps set by hand and later ones ran as a rotation, by the author's belief,
  which he calls unimportant (account §18).
- Ruediger announced the last evening at 20:58 UTC on 27 September, a minute before the first match
  (sources/slop-sunday-announcement/).
- The fire-and-ice map, the hand-built ice map and the wool-and-core map players took for AI are one map, begun about 17
  October (research/04, research/17; account §14, §17).
- On 27–28 November five arcade freeform boards were played, the first freeform boards on the public servers: Lantern
  Pass, Loomfall, Lantern Drop, Spark, Curio Square (account §14–§16).
- The forum thread of 20–24 September, "stop AI maps from being played at all", is the one public argument about the
  maps (research/17).
- Claude was used from May 2025, in a chat artifact (sources/early-experiments/); Claude Code wrote most of CTWAnalysis
  from February 2026 (research/18).

## What is open

Whether any v0 code reached `CTW-Layout-Generator`; what the
April 2025 experiment was written with beyond matplotlib (the author: perhaps ChatGPT); whether the 7 October 2025 AI Studio link is a second app;
whether a repository `ctw-layout-editor` exists (the author thinks it differs from MinecraftLayoutEditor; the record
holds none), who `michael` is and who the friend of 10 October 2025 was; whether the author's local data holds more than the
2,452 matches the repository processed; what the "143 contaminated maps" were (he does not know; perhaps the server's tracking logs); whether Bridgid II's "nochmal" refers to the matches of 14 July;
which two evenings were set by hand; who opened the forum thread; Aerie's unplayable XML, which the author states and no
record holds; whether the 50-log oak is the generated tree; the briefs of the first fifteen, Heftfold and Whinberry
Ring; which model "Muse Spark" is; who may be quoted beyond the staff chat. `HISTORY.md` chapter 18 and
`interview-questions.md` carry them.

## Names

By the author's decision of 28 November 2026 (account §18), two groups of sources carry no names anywhere in this
folder: the forum thread of 20–24 September, whose posters, staff and event host included, are quoted as "the thread's
opener", "a staff member", "one player", "a second player" and so on; and the author's direct messages with four people,
who appear as "the contest's map developer", "an administrator", "the award show's organiser" and "a developer of the
website". The author, Ruediger, TTtie's direct messages, the five voices of 2 July, the cleared staff chat of October
(where the administrator and a map developer appear under their names, and nothing from the thread or the messages is
attached to them) and names that are public facts, such as map credits and commit authors, keep their names. The author
confirmed on 28 November that this level is enough, naming the role or "staff", and that the branch history need not be
cleaned; earlier commits on the `mappies-film` branch still hold the names (account §21).

## What was not read

- **Session starts that could not be paged to**: sessions 2, 4, 5, 7, 10 and 12 (their write-ups say so at the end);
  session 14's opening was a parent session's text, known only from a summary; session 1's middle.
- **Assistant text in most sessions**: the write-ups read the author's messages and turn-closing summaries.
- **The private maps repository (PrivateMaps)**: only its commit feed in `#maps-changelog` and the zips; the file list
  of `711e539` was not read.
- **The early repositories beyond their git record**: the logger plugin's repository (`pgmlogger`) was not cloned; the
  v0 prototype page of February 2025 was seen only as it runs today (`sources/early-experiments/v0-prototype-2025-02/`);
  only the v0 chat's previews of 16 August 2025 were read.
- **Material the PC agent read but did not commit**: the 2 July recording and its transcript, the forum thread, the
  direct messages (research/15, research/17) and the saved API pages; they are quoted briefly in research/16 and 17.
- Also not read: PGM's source (so the tab list's "made by" was not checked); the studio's local database and scanned
  corpus output; several artifacts linked from the documents; the match pages' per-player statistics beyond what
  account §15 transcribes.

## Corrections log

Each place where an earlier version of these documents was wrong, and what replaced it. This is the one place in the
folder that records a change history. Chapter numbers in a row are those of its time: the pass that opened the history in February 2025
turned two chapters into three, so every later chapter moved up by one.

| Earlier claim | Where | Replaced by | Source |
|---|---|---|---|
| The 14 July map was a Brittlebush map ("Bridget") | account 5 | Bridgid II, a map of its own | account, correction; research/11 |
| Brittlebush III's colouring was done entirely in game | account 1; HISTORY; research/05; questions | that was Bridgid II; Brittlebush III was never player-tested and its look is expressible | account, correction and 2 |
| The squared-paper drawing is Base 2-Wool (an H with a centre spine) | account, squared-paper section | Base 2-Island, the two-team map | account, later correction; research/09 |
| The 8×8×8 bedrock shell was specified by Opus 4.8 | research/07 | specified by the author at 23:21 UTC on 1 July | research/09 |
| He had traced maps into seed files before the Base maps, and seeds were the plan model | account | seeds were born as test fixtures that day; the plan model came that evening | research/09 |
| The graph was dropped after 23 minutes | research/01; old timeline | a design document was replaced; `FannedGraph` was committed that evening and stayed | research/08 |
| Kuusepuu CTC was the first AI-map test on the server | earlier HISTORY and research files | Base 4-Team was played three days earlier; the author does not count Kuusepuu as an AI map | research/13; account 6 |
| Cedar Crossing was the first AI map in CommunityMaps | account 5 | Kuusepuu CTC credits a model thirteen days earlier; Cedar is the first by another uploader | research/11 |
| Every AI map was committed by Ruediger | research/06 | true of this project's maps only, not arcadeboss's | research/11 |
| Hello World Micro's wool room moves | account 1 | it recolours; the room that moves is Wandering U's | account 3, 4; research/08, research/10 |
| The moving-wool-room map is not in the record | research/08 | supplied as a zip; PrivateMaps commit of 6 August | research/10, research/15 |
| The 6 August missing match number is a lead for Wandering U | research/13 | it closes before the zip was sent | research/15 (inference) |
| No Blocks Placed's third author is Tttie | account 1 | Flamiix; Tttie did nothing on it | research/05; account 3 |
| Nothing is recorded about Tttie | first interview questions | CommunityMaps committer since 2023, with a pgmstudio.de account | research/05 |
| Fable's copying led to the tree world being added | account 1 | the world was in the studio from 12 August and committed before Fable's work | research/05 |
| The instruction that started freeform is not in the record | research/05; research/12 | dictated at 22:21 and 22:26 UTC on 7 October | sessions/00, sessions/01 |
| He contributed nothing to Riftwater | account 7 | he gave the mode and the ingredients, not the layout | sessions/01 |
| "Slop Sundays" appears nowhere / is his account alone | research/05, research/06; earlier HISTORY | Ruediger's name, in a message of 12 September | research/15 |
| The tests show in CommunityMaps / may be in PublicMaps | account, later additions | CommunityMaps holds them to 2 September; none in PublicMaps; the rest in PrivateMaps | research/06, research/07; account 4 |
| The private uploads of August and September, and Ruediger's 2 July, are unverifiable | research/11 | the PrivateMaps feed holds each, minutes after the zip | research/15 |
| The missing matches were a reader gap, a differently worded message or another server | research/13 | unreported event rotations | account 9; research/15 |
| Alderfen Holm has five cores | research/13 | four | sessions/08; account 11 |
| Tallow Kilnrow holds no quartz | sessions/04 | it does, in its palette | research/14 |
| No 27-block obsidian monument was found in the trial session | sessions/04 | `corvid-hollow`'s `cube-3` of obsidian, and the stored worlds | sessions/04 appendix; research/14 |
| The session of Overwall and Aerie opened with the labyrinth brief | sessions/06 | it opened with a friend's Liminal DTM prompt | sessions/06 appendix |
| The Sonnet run's brief was thin on layout and its places unknown | sessions/11 | the brief was read: rules and method, underground passages asked, places the model's | sessions/11 appendix |
| Thornwake and Viridian may not have reached CommunityMaps | research/03 | both did, on 12 August | research/05 |
| The 500-wide map is most probably Spinebreak | research/03 | Hollow Crown fits better on all but size; still open | research/05 |
| The 500-wide map is Spinebreak or Hollow Crown | research/05; HISTORY; interview questions; OUTLINE | Ashfall Scar, 250 × 190, found by filtering every `map.xml` and confirmed by the author on a render; Hollow Crown is the Haiku board with the monument inside the core, Spinebreak a capture-the-wool layout with cores in the void | account 12; research/03 |
| The quartz board is Quillon Saltworks or Tallow Kilnrow, unsettled | HISTORY; interview questions | Quillon Saltworks, which the author now states definitely | account 12 |
| "AI map" has six categories, the last one model's own script | research/12; earlier HISTORY | the last is split: a model's script inside the author's tool, and a model's own tooling | research/12; research/15 |
| The 9–10 October notes were a playtest on a server that does not report, so the last test is open against 27 September | HISTORY chapter 9 and 14; timeline; research/05, research/13, research/15 (inference) | three people looked at the new pgmvox boards together; the first feedback on them; not a test, and 27 September stands as the last test evening | account 13 |
| Who wrote Hello World Micro's layout was open | HISTORY chapter 4 and 14; timeline; interview questions | he drew it, Hello World's layout abstracted onto the grid | account 14 |
| The date he built his half is not recorded; he built it after the agents' failed compositions | HISTORY chapter 10, 14; timeline; research/04 | begun about 17 October and built over a few weekends; the record dates only the agents' study | account 14 |
| Which boards were shown at the viewing is not recorded | HISTORY chapter 9, 14; interview questions | the new pgmvox boards; three named by description, Hollowcrown inferred, two pairs of candidates | account 14; inference |
| The staff's words need each person's consent before use | HISTORY chapter 9; README | may be used as they are, the author's decision | account 14 |
| The pause was a reaction to the maps being "too good" | HISTORY chapter 9 | that, and a month of weekly testing, the tool needing care, and building in bulk never being the aim | account 14 |
| The author's pause after October is only visible as the 13 November freeze | HISTORY chapter 9, 10 | at the October viewing they decided to pause because the maps were getting "too good"; the link to 13 November is inference | account 13 |
| Capture the Wool CTW was first played on 28 June; Vauxite and Drastic Change II not until 12 October | HISTORY ch. 3; timeline; research/12 §3.2 | all three were played on server-2 on 24 June from 21:51 UTC, minutes after the upload; the log's dates are its own first rows | research/16 |
| Nothing showed the Base maps played, then Base 4-Team's 28 July match was the first; Kuusepuu CTC was played after it | HISTORY ch. 4; README; research/12 §3.6; interview questions | all three were walked on mapdev and played on server-2 on 2 July from 20:23 UTC, with a recording of the evening; Kuusepuu CTC was played on 27 July at 21:42, before Base 4-Team's second match | research/16 |
| Who was at the first test is not recorded | HISTORY ch. 4 (silent) | rockymine, Ruediger, TTtie and samschaap in the call; nuttydragon from about minute 20; voices named by the author | research/16; account §16 |
| Bridgid II's first play is 15 July | HISTORY ch. 5; timeline | 14 July, 00:31 and 00:53 UTC, minutes after the upload | research/16 |
| Wandering U's test is not in the log, and the one missing number of 6 August is not it | HISTORY ch. 5 (inference) | its match is in the API at 20:17 UTC, 36 players; the missing number is Arch, a corpus map | research/16 |
| No Blocks Placed was first played on 11 August; its concept is unknown | HISTORY ch. 5; research/12 §3.4 | played 7 August at 19:01 UTC; he and Ruediger made it together on Discord | research/16, research/17 |
| Thornwake and Viridian were tested on mapdev, which does not report | HISTORY ch. 5 | on mapdev and then on server-1 at 21:43 and 21:54 UTC | research/16 |
| The first match on a map no person laid out is Cedar Crossing at 23:53 on 10 August; this project's first is Hollowmarch on 31 August | HISTORY ch. 6; research/13 (cited) | Cedar Crossing at 04:04 on 10 August; this project's first is Viridian on 12 August; Hollowmarch was first played on 24 August | research/16 |
| Six evenings fit the zips, with "no event seen" on 25 August, a partial fit on 31 August, and one more number than maps on 4 and 20 September (inference) | HISTORY ch. 12; README; interview questions | every evening documented in the API: Tarnfell on 25 August, Brackenfold and Millrace on 31 August, Lodestar Yard and Peatgarth played twice | research/16 |
| The test evenings were event rotations the plugin did not report (stated as settled) | README | the event rotation is the author's account; the API shows the channel also missed many matches that were no tests, and does not record how a match was started | research/16; account §9 |
| Kilnholt Cut was probably played on 13 September (inference) | HISTORY ch. 7 | its one match is the first of 13 September, 21:39 UTC | research/16 |
| No long destroy match; the longest is Brackenfold's 15 min 15 s | HISTORY ch. 12; README; interview questions | still no long one; the longest is Glassmere's 15 min 47 s on 13 September, inside the event | research/16 |
| On 27 November no log or record of the arcade test exists yet | HISTORY ch. 12 | match pages and the API hold Lantern Pass, Loomfall, Lantern Drop, Spark and Curio Square, the first freeform boards on the public servers | account §15, §16 |
| The viewing's boards: Hollowcrown most probable; Lantern Karst or Brassmoor Works; Redwash Mesa or Hollow Mesa | HISTORY ch. 9, 14; README; interview questions | Hollowcrown, Lantern Karst, Hollow Mesa and Riftwater, confirmed | account §15 |
| Claude appears first in December 2025, for the logging plugin | HISTORY ch. 2 | the October 2025 rewrite of the layout tool was mostly written with Claude's VS Code extension, by his message to the contest's map developer | research/17 |
| The community's reception was the staff's surprise at the October boards | HISTORY ch. 9, 11 (by omission) | a public forum thread of 20–24 September opposed the evenings; the maps were framed as an event; a disclosure was proposed; players were divided; map developers set lines in May, September and October | research/17 |
| The hand-built ice map stands alone | HISTORY ch. 10, 13 | it is the fire-and-ice map, and the wool-and-core map players took for a model's work | account §17; research/17 |
| The Base export's crash was fixed by his own commit | research/12 §3.6 | the commit is under rockymine at 21:21 UTC; in the call he said "Claude had to fix it" (both kept) | research/16 |
| The history begins in autumn 2025; "a year" from September 2025 | HISTORY title and ch. 1; README; timeline | it begins on 11 February 2025 with the spanning-tree message to samschaap and a v0 prototype; twenty-one months | sources/early-experiments/; account §18, §20 |
| The first statement of the idea is Ruediger's (26 September 2025) | HISTORY ch. 1 | the layout idea is the author's from February 2025; Ruediger's remark is the first statement of an AI making maps from the data of all maps | sources/early-experiments/; research/15 |
| Claude was in the work from October 2025, earlier than the commits name it | HISTORY ch. 1; README | a Claude chat artifact drew a layout generator on 24 May 2025 | sources/early-experiments/; account §18 |
| `CTW-Layout-Generator` is the first generator | HISTORY ch. 1; research/01 (cited) | preceded by the February 2025 spanning-tree page and the v0 "Capture the Wool Layout Generator" of 16 August 2025, whose algorithm it shares; no shared code shown | sources/early-experiments/; the clone's `Documentation.tsx` |
| Whether `ctw-layout-editor` and `MinecraftLayoutEditor` are one repository is open | HISTORY ch. 17; README; questions | the author thinks not; the record holds no repository of that name | account §18; research/18 |
| Nothing filled the commit gap from December 2025 to June 2026 but messages | HISTORY ch. 2 | CTWAnalysis from 31 January 2026: islands, triangles, skeleton graph, 2,452 matches processed, the May viewer and drawing tools | research/18 |
| The logging held 3,000 matches by March | HISTORY ch. 2 | 689 and 3,000 in his messages; 2,452 processed in the committed summary; 2,450 in the chart's daily table; about 4,000 by his memory, later "maybe 2700" | research/15, research/18; account §18, §21 |
| The match logs begin on 24 January 2026; the plugin's run through the pause is not recorded | HISTORY ch. 2, 3; timeline | the chart's first match is 18 January and its last 8 March, so the logging ran through the pause | account §21; sources/early-experiments/ |
| The 24 May 2025 chat is the earliest Claude in the history | HISTORY ch. 1 | the earliest recorded use of Claude is 24 May 2025; the 5 April 2025 graph experiment may have been ChatGPT, the tool is not known | account §21 |
| No long destroy match exists, which could read as no long match at all | HISTORY ch. 12 | still none on a destroy board of the project; ordinary capture-the-wool matches of over three hours are in the logged data of early 2026 | sources/early-experiments/ |
| The first v0 attachment, the open question | HISTORY ch. 1; questions | not recoverable without much searching; he assumes it was his algorithm idea | account §21 |
| The second attempt began with `pgm-map-studio` on 31 May | HISTORY ch. 2 | the viewer, region drawing and polygon islands were built in CTWAnalysis from 14 May; `pgm-map-studio` opened that evening | research/18 |
| The graph returned in the studio on 2 July after a first life in 2025 | HISTORY ch. 4 (now 5) | its fourth arrival, after February 2025, April 2025 and February 2026 | sources/early-experiments/; research/18 |
| That `711e539` carried the Base folders is inferred from timing | HISTORY ch. 4 (now 5); timeline; README | the author states it did, and that its message is Ruediger's joke about a stalemating map put into the dev phase | account §18 |
| Three people were at the 9–10 October viewing, place not recorded | HISTORY ch. 10 (now 11), ch. 17; account §13; README; questions | five, on mapdev: the author, Ruediger, TTtie, mitchiii and wylt | account §18 |
| The cancelled contest may be the contest's map developer's (inference) | HISTORY ch. 11 (now 12), 17; timeline | it is, by the author | account §18 |
| Whether the evenings were all event rotations is open | HISTORY ch. 14 (now 15); README | the first two set by hand and later ones a rotation, by his belief | account §18 |
| Ruediger's alert of 27 September is a line in the search results | HISTORY ch. 8 (now 9) | the event channel's one announcement, 20:58 UTC, a minute before the first match, with its reactions | sources/slop-sunday-announcement/; account §19 |
| An inference joining a person of the staff chat to a person of the thread and the messages | HISTORY ch. 10, 15 | removed under the naming rule; nothing from the thread or the messages is attached to a staff-chat name | account §18 |
| The 20 September evening was hosted by TTtie, named with his thread posts | HISTORY ch. 8; timeline; research/17 | thread posts carry a role label; the host is not named from the thread | account §18 |
| Whether the AI Studio app changed after the repository's last commit was not known | HISTORY ch. 1 | the author's export of 28 November 2026 is identical to `ec9ca62` of 3 October 2025; the app calls no model (`sources/early-experiments/aistudio-ctw-map-generator-2025/`) |
| The 7 October 2025 AI Studio link was "a second app or a second share; which is not recorded" | HISTORY ch. 2 | a second project exists, "CTW Smart Map Editor", a manual graph editor with mirrored nodes and automatic node classes; the author confirms it is the 7 October link, and did not know of the unconnected Gemini analysis in it (account §24; `sources/early-experiments/aistudio-ctw-smart-map-editor-2025/`) |
