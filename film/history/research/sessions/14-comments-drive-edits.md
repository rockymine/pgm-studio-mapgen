# Session 14: the map-notes trial, and how notes drove edits

## 1. Header

| | |
|---|---|
| Session | `session_01KQ111EpBd2SkcJMxiJGguv` |
| Title in the studio | "Map notes trial: build boards, ask the author" |
| Created / last updated (UTC) | 2026-09-28 22:41:01 to 2026-09-29 18:08:58 |
| Model | `claude-opus-5-5` ("Opus 5.5"), permission mode `auto` |
| Origin | `claude_code_mcp_seed`: it was started by another session, `session_01WNnpA2sH4NswnAGjPf5ApW`, titled "Map notes implementation" (also Opus 5.5, 2026-09-28 19:37 to 22:56 UTC, which built the notes feature in `pgm-studio`) |
| Repository and branch | `pgm-studio-mapgen`, branch `ccr-a2674ec6-o0vxga`; revision `ccr-a2674ec6-o0vxga` (no `pgm-studio` checkout) |
| Size | 746,739 output tokens, about $93.15, context 632,549 of 1,000,000 |
| Outcome | pull request 17, "Eight boards on the deployed studio, and Sootcombe and Gypsum Reach worked through five rounds of notes": 13 commits rebased onto `main` and merged at 20:44:53 +0200 on 29 September (`f4a533af`) |

The session ran on the deployed studio at pgmstudio.de, not a local one. Two phases: a first, autonomous build run (22:41 to about 23:55 UTC on 28 September), and a second, in which the author reviewed two boards through the notes feature and the agent worked his notes in rounds (15:38 to 17:54 UTC on 29 September). About 15 hours separate them.

## 2. What the author asked for

I could not read the opening prompt. It came from the parent session; the transcript is paged newest-first, and I stopped about 17:41 UTC on 29 September, with the intervening hours unread. What the record says of it:

- `reports/opus55-notes-run.md` states the purpose: "Two boards unlike each other, built on the deployed studio at pgmstudio.de, with every decision that is the author's left on the board as a note rather than decided. The run tests the notes loop end to end: the author answers the notes, adds their own, and the next session works them."
- The first two boards were given as one-sentence concepts the agent wrote itself ("The two sentences, written together before either plan"): Gypsum Reach, a pale desert lane (destroy the monument); Sootcombe, an ash-field combe from composed plan 12, seed 21 (capture the wool). So the agent chose the places, within a brief that asked for two boards unlike each other and for tone families checked across the pair.
- The brief kept specs out of an authoring run: the report records as a fault that the agent "opened another board's spec to learn the `follow` syntax".

The author's messages I did read, all with `client_platform: web_claude_ai` (UTC, 29 September):

> 17:28:41 "Sootcombe received a fourth round of feedback."
> 17:37:13 "Gypsum Reach received a fourth round of feedback."
> 17:43:38 "Sootcombe received a fifth round of feedback."
> 18:00:56 "okay, these two maps are now in a good state. summarize what wasnt possible so that i can relay it to  another agent that can work on the studio."
> 18:07:37 "create a PR for the mapgen changes."

Gloss: the chat message is only a nudge. The feedback itself is in the notes, which the agent reads from the studio. The first-round review ("empty") was given in chat, before the second pass. The report paraphrases it: the relief is fine and nothing hurts the eye, but "the desert is sand over twenty blocks of sandstone with no stone under it, there is no dirt or grass for a tree to stand in, two houses stand by a path, the frontlines are bare, and the outlines were never shaped"; the boards were to be reworked and four more built. The report adds that the author said a note paraphrasing it was not necessary. I did not read that message, so I cannot give its words. I did not read the stretch from 22:41 to 23:55 on 28 September, so any author message in it is unseen.

## 3. How a note reached the agent

This is the answer to the film question. The mechanism, from `pgm-studio/docs/tools/sketch.md` ("Notes", under Review) and `MapNoteDtos.cs`, confirmed against what the transcript shows:

1. **The author writes a note on a picture, not with coordinates.** In the Sketch tool's Review phase a picture of the board is drawn from a saved camera (a "view"). He arms Point, Box or Lasso, marks the picture, and types a sentence. "Nobody types a coordinate: the anchor carries them."
2. **The studio converts the mark into ground.** `render/eye/pick` re-casts the ray through each marked pixel against the world the picture was drawn from. A point stores the block hit and the ground under it. A box or lasso stores every ground column hit, as `[x, y, z]`, and where the mark was over void, the empty cells under it (`overVoid`) at the level of the neighbouring ground. The note also stores the camera exactly, the picture's size, the change number of the board it saw, and the picture itself (WebP, by hash, `POST /api/notes/pictures`). Ground hidden behind a hill is not selected, because no ray reached it.
3. **The agent reads open notes.** Its helper prints each as a line of status, place and camera, with text and picture hash. What the agent saw at 17:28:51 on 29 September, after the nudge "Sootcombe received a fourth round of feedback", was (verbatim from the tool result):

```
== 64 open None box The whole board x -21..-13 z 65..81 y 12..17 {"x": 137.5, "y": 75.4, "z": 0.5, "yaw": 90, "pitch": 23.09, "fov": 70}
   [r42] add another willow on top of the rise.
== 70 open look point Straight down  {"x": 0.5, "y": 266.7, "z": 1.5, "yaw": 180, "pitch": 90, "fov": 70}
   [r42] another willow here.
== 71 open None box Straight down x 2..15 z -29..-21 y 6..12 {...straight-down camera...}
   [r42] a grass patch here.
```

   Notes already worked are listed as `answered` or `resolved` with no text. The `[r42]` is the board's revision when the note was written.
4. **The agent changes the board and replies in the thread, with a picture from the same camera.** The reply carries "the same camera drawn after its change", so before and after are a pair. If the note's own camera no longer sees its subject (note 33 and 35 on Sootcombe; 40 and 43 on Gypsum Reach), the reply attaches a kept view of the new thing and says so.
5. **The author closes the thread** (`resolved`). The agent never closes one.

`.claude/skills/pgm-board/SKILL.md` now carries this as "before the first change, read the open notes": a revision starts from `GET /notes?status=open`. Tokens issued with the notes permission can read and answer notes (`docs/access.md`).

## 4. What was built

First phase, 22:41 to about 23:55 UTC on 28 September:

| Commit (UTC) | |
|---|---|
| `ae025473` 23:00:46 | "Two boards on the deployed studio, with the author's questions left as notes": Gypsum Reach (dtm) and Sootcombe (ctw), notes 1 to 5 and 6 to 10 |
| `a9388203` 23:54:58 | "Six boards with ground under them: two reworked, four new, each with questions as notes": adds Sallowfen (dtm), Karnbeck (dtc), Rimeholt (ctw, composed seed 7), Quarrymoot (koth); notes 11 to 22 |

The ten first notes, as pinned: note 1 on Gypsum Reach was at point (-46, 13, -10) ("Monument across the wash"); note 2 at (-68, 26, -34) ("The mesa over the monument"); note 3 on a box of 985 columns on the north flank (should anything bring players to the 40 percent dead flanks?); on Sootcombe, note 6 at (4, 8, 25) asked whether the ash reads as chocolate brown and the black as holes. `reports/opus55-notes-run.md` has the full table. Three of the new pins landed on something in front of their subject (13, 16, 19), each corrected by a one-line second message.

Second phase, 15:38 to 17:54 UTC on 29 September, each commit named for the round of the author's notes it works:

| Commit (UTC) | Board and notes |
|---|---|
| `15adaebb` 15:38:46 | Sootcombe, notes 6, 8, 9, 10, 33 to 35 |
| `57da6d28` 16:13:49 | Gypsum Reach, notes 36 to 43 |
| `d0d19ebe` 16:31:15 | Sootcombe, second round, notes 33 and 44 to 50 |
| `4e1ce960` 16:57:35 | Gypsum Reach, second round, notes 51 to 60 |
| `75aa287c` 17:14:53 | Sootcombe, third round, notes 7, 10, 33, 61 to 64 |
| `1109fc9b` 17:26:54 | Gypsum Reach, third round, notes 56, 65 to 69 |
| `599ef554` 17:32:35 | Sootcombe, fourth round, notes 10, 64, 70, 71 |
| `eb0cb354` 17:42:30 | Gypsum Reach, fourth round, notes 72 to 74 |
| `d7e95fcb` 17:53:52 | Sootcombe, fifth round, notes 75 to 77 |

Also built or in the pull request: `specs/opus55_kit.py` (a shared set of finish helpers, with `coast_edits` fixed in `d0d19ebe` because it pulled coast points toward the centroid and pushed ground past the east wall's end on a non-convex ring; and `willow()`, a copied-tree recipe, because the studio's tree library has no willow). The pull request also carries `sonnet55-tanglecleft` and `sonnet55-murkwick`, boards from a Sonnet 5.5 session (see its own write-up; they are not this session's work).

World paths: `maps/dtcm/gypsum_reach/`, `maps/ctw/sootcombe/`, `maps/dtcm/sallowfen/`, `maps/dtcm/karnbeck/`, `maps/ctw/rimeholt/`, `maps/koth/quarrymoot/`; specs in `specs/opus55-*`. These worlds were re-exported later (the BOARDS-BUILT rows add a seventh and an eighth pass after the studio gained lava, a chest and a willow), so the stored worlds can run ahead of this session; I checked only things this session did.

## 5. Notes into changes: examples

From `reports/opus55-notes-run.md` (the "what the author said" column is the report's rendering), the commit messages, and my read of the stored worlds.

| Note | Author | What it asked | What changed |
|---|---|---|---|
| 64, box x -21..-13, z 65..81, y 12..17 | Sootcombe | "add another willow on top of the rise" | a small willow at (-18, 74). The stored world has a log column there, y18 to y24. |
| 71, box x 2..15, z -29..-21, y 6..12 | Sootcombe | "a grass patch here" | grass patches on the west half of each frontline's front (`599ef554`). Grass is the commonest top block in the box in the stored world. |
| 10, point on the orange wool at (18.5, 15.6, 68.5) | Sootcombe | "make the door 2 wide and 3 tall and place tinted glass" | doors 3 tall, wool-room doors filled with panes in the wool's colour; the width stays 4 and the note is left `needs-info`, because the studio cuts a room's door from its wall (`WX7`) |
| 36 | Gypsum Reach | flat frontlines not wanted; pull one side in, push the other out, add a middle island | frontline pushed out 4 to 7 south of the middle, pulled in 4 to 8 north; an 8 by 32 island on the axis at y18 |
| 37 | Gypsum Reach | spawn inside a corner by the oasis; players run along the oasis and turn right | plan re-cut; spawn in the south-west corner beside the oasis, oasis on the right; three houses moved |
| 38 | Gypsum Reach | the oasis should drop about 4 blocks | oasis floor mark at 16 against the field's 20 |
| 41 | Gypsum Reach | the arch looks like a laid-down pillar; build a real bridge, not sandstone | a spruce deck on three pairs of dark-oak posts with oak-fence rails |
| 42 (ruling) | Gypsum Reach | never add random structures with the layer tool to bring a number down | the mesa tower removed; grass, an acacia and two rocks on the top |
| 43 (ruling) | Gypsum Reach | emerald or ender stone on a board this size; emerald and gold are cubes; obsidian the only pillar | emerald `cube-3` monument |
| 74, a lasso over void | Gypsum Reach | "another island in the void to cross by" | `isle-south`, x 0..8, z -44..-28, fanned; the stored world has ground at (4, -36) and (4, -44) and none at (4, -28). The report notes it first read 7 blocks off the frontline when a transect reads 9, and a correction went into the thread. |
| 77 | Sootcombe | a dip with water that splits the lane, with lily pads | a push of -2 and a canal at x 16..18, coast to coast, four lily pads; the reply asks whether to leave a lip at each coast |
| 75 | Sootcombe | chamfer the middle island and the frontline slightly; extend the build zone into the land | three-block chamfers on the mid stone's four corners and the frontline's two front corners |

Cases where the first reading was wrong are recorded in the report and were caught by the attached pictures: note 40 ("no boxy boulders") was first read backwards, keeping the round boulder the author had pinned; the author's picture showed it before the reply went. Note 10's "tinted glass" was first read as windows. The studio-side finds from the rounds are in section 6.

## 6. What went wrong, and how it was noticed

- First-phase boards were empty (sand over twenty blocks of sandstone with nothing under it, two houses, bare fronts, unshaped outlines). Noticed by the author, in chat.
- `DestroyablePlacement.at` is documented in half-blocks and the evaluator reads blocks; posting `[88, 72]` put a monument 44 blocks past its mark and was refused `OB17`. Noticed by the studio's refusal.
- On `opus55-sallowfen`, while the stored layout carried an `HS10` complaint, every sketch write answered 200 and was dropped. Found by reading the stored sketch back.
- In the third pass the stored Sootcombe sketch was found reverted after two drives; the report's likely cause is that a browser tab open on the board saved the old board back when In game was entered. "An author reviewing a board while an agent rebuilds it can write the old board back over the new, and nothing on either side says so." Noticed by the agent, from the ETag and a world read.
- Two of the author's cameras no longer see their subject once the board changed (see section 3).
- A made layer's rectangle covers `x0 .. x1 - 1`; reading the count as inclusive drew nothing for the bridge posts (`SK4`).
- A channel over a door approach carved one column of water, because the studio keeps the approach clear and fills it without cutting; the claims raster and heightmap drew water, and `column` and a probe of the exported world did not.
- The author flagged a studio bug as a note: note 44, the render leaves out redstone and redstone paints the ground under it as fill.
- A request the studio could not do: lava in the wash (note 72). The pull request lists it as waiting on the author. Later passes added it, per `BOARDS-BUILT.md`.

## 7. The author's reactions and rulings

From what I read: two rulings in notes (42 and 43, the emerald cube and no structures to fix a number), the notes themselves, and the statement at 18:00:56 that "these two maps are now in a good state". The assistant's reply to that request (the list of what was not possible) was not read.

## 8. His description set against the transcript

"finally a session showing how the comment feature in the studio allowed the agents to manipulate and improve specific areas of a map."

Confirmed, with two corrections. First, "comment feature" is the notes feature in Review, and it was built hours earlier by the parent session the same day (PR 16 merged 2026-09-29 00:22 +0200). This session is its first trial, started 15 minutes before the parent went idle. Second, a note carries a spatial anchor the studio computes (ground columns, void cells, exact camera), so the agent works from coordinates the author never typed; the agent also answers with a before-and-after camera, which is what makes it a loop. Note ids run to 77 across the six Opus boards; the two boards worked through five rounds each.

## 9. Who decided what

| Cell | Gypsum Reach / Sootcombe |
|---|---|
| Concept | the agent, within a brief to make two unlike boards (Sootcombe's plan is a studio-composed layout, seed 21, taken whole) |
| Layout | the composer for Sootcombe (algorithm); the agent's plan for Gypsum Reach; then the author, by notes, for the frontlines, spawn corner, islands, oasis depth |
| Terrain | agent in the first phase; the author's notes redirected it |
| Colouring | agent first; the author directed materials by note (clay colours, ash pattern, hardened-clay lines, no orange, oak and jungle paths) |
| Structures | agent first; the author replaced them by note (houses stone brick and andesite with clay gables and jungle roofs, timber bridge, archer tower, no mesa tower, no engine house) |
| Objectives and XML | the agent placed; the author ruled (emerald cube) |
| Finishing | the agent through `drive.py` and the shared kit; the studio's export |

Executed by the agent's `build-spec.py` through the studio's HTTP API on pgmstudio.de.

## 10. What is filmable

- The first pictures sent to the author: `specs/opus55-gypsum-reach/renders/close/` has `eye-overview.png`, `note-view-1-wash.png`, `note-view-2-mesa.png`, `second-pass-oasis.png`, `second-pass-overview.png`; the notes' own pictures are kept per spec in `renders/close/`.
- Before and after for a single note: each reply in the studio thread carries the same camera drawn after the change. Those pictures live in the studio's notes store, not in the repository, except where copied to `renders/close/`.
- World folders listed in section 4.
- The notes feature itself is in the studio's Review phase, Notes step (`docs/tools/sketch.md`).

## 11. Open questions for the author

1. Which exact message started the first round on Gypsum Reach (the author's words, not just the notes)?
2. Was the "empty" review about all two boards in chat only, and when?
3. What did the agent's reply list as "not possible" at about 18:01, and which of those became the later passes (lava, chest, willow)?

## What I did not read

The opening prompt and everything in the first phase (22:41 to 23:55 UTC on 28 September) except through commits and reports. In the second phase I read the author's messages at 17:28 to 18:07 UTC and the agent's closing turns; I did not read the earlier rounds (15:38 to 17:20) from the transcript, only from commits and the report. I did not see the pictures attached to notes or replies, which live in the studio's picture store.
