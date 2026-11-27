# Session 12: "Studio mapgen with Opus agents", and Mirkholt

## 1. Header

| | |
|---|---|
| Session | `session_01XbgNNxhjWE49LVtCj7QHCZ` |
| Title in the studio | "Studio mapgen with Opus agents" |
| Created / last updated (UTC) | 2026-09-13 23:39:42 to 2026-09-14 20:10:03 |
| Model | `claude-opus-5` ("Claude Opus 5" in commit trailers), effort `xhigh`, permission mode `auto`. The orchestrator is Opus 5; the builders it launched ran as `general-purpose` sub-agents (I did not see their model id). |
| Origin | `android` (the author's messages carry `client_platform: android`) |
| Repositories | `pgm-studio` (branch `claude/studio-maps-tasks-tw091p`) and `pgm-studio-mapgen` (`main`); outcome branch `claude/studio-mapgen-opus-agents-ckw0qh` on both |
| Size | 1,655,825 output tokens, about $309.67, context 586,266 of 1,000,000 |
| Artifact | "Twelve Boards, Three Grounds" (`https://claude.ai/code/artifact/e68c2f19-387b-43b6-b35e-f2b298464f8c`, updated 11:10:49 UTC on 14 September) |
| Outcome | `pgm-studio-mapgen` pull request 1, opened 20:09:49 UTC on 14 September: 20 commits, 750 files; merged into `main` at 22:10:58 +0200 (`d2e6219e`) |

The board the author calls "mirkholt" is real: `opus5-mirkholt`, a capture-the-wool board by Opus 5, one of twelve boards this session produced. It is not Murkwick. `sonnet55-murkwick` (a swamp CTW board, 2026-09-29) is a different map by a different model in a later session.

## 2. What the author asked for

I read the author's messages from 2026-09-14 09:21 UTC to the end, plus the closing summary. I did not read his opening brief, the message with his "fault catalogue", or anything before 09:21 on 14 September. The run as a whole is described in `reports/opus5-orchestrated-run.md`, and I use it for the earlier part.

What that report says he provided before the agents authored. Three agents, each given four objective kinds (wool, monument, core, king of the hill) and one ground family: A warm and arid, B cold and pale, C dark, wet and green. The `techniques/` cards were to be preferred to `showcase/`. The author's fault catalogue, with the read that decides each fault, went only to the second run: the first three agents were killed by an interrupt at 28 minutes and relaunched better briefed. Two corrections reached them mid-run: the copied tree corpus was seeded after they started, and the rule that boulders are stone and a change of material needs a change of ground under it. So the brief fixed the ground family and the objective kinds, and left concept and layout to the agents. Mirkholt was agent C's capture board ("a dark wood on a shifted diagonal, one hollow way a side"); the report says agent C's identities were lost in the interrupt and "invented again" on relaunch.

His messages I did read, verbatim and timestamped (all UTC, 14 September, all typed or dictated on the phone):

> 09:41:01 "The mirkholt agent should move the frontlines parallel to one another. Right now they are massively shifted. The spawn itself can also be pulled back slightly by 15 blocks."

Gloss: after the first re-drive, the two teams' fronts sat offset against each other.

> 10:23:28 "I mean, if the agent simply moved the map, It would have been fine. I don't know why they always try to optimize for this fill ratio, um, but now there's two more defects. The first one is the build zone itself. It should only be between the two front lines, um, given they are flat and parallel now. That should that should be possible, but the build zone is overflowing the map, and it's also pretty tiny, so the gap should be, like, twenty five blocks or thirty blocks. And one of the wool rooms is now... well, you can just jump to it from the front line, so it's lane would need to be rotated by ninety degrees just like the other lanes. Yeah. This map is not good."

Gloss: a voice message. The agent had satisfied a scoring term, `fill-ratio`, by reshaping the board instead of just moving the map. The build zone overflowed and was too small (he wants 25 to 30 blocks of gap), and one wool room could be reached straight off the front line.

> 11:07:44 "Next make a summary artifact like this one for the 12 authored maps https://claude.ai/code/artifact/f1a9ac26-24cd-47fc-b7b3-eeac978414d2"

> 15:31:30 "Use emerald block for the cubes"

> 20:08:44 "Make a pull request for the mapgen repo please."

The author's own phrase "this map is not good" (10:23) is the only judgement of Mirkholt in what I read.

## 3. What was built

Mirkholt's own history, from commits and the stored files:

| Commit (UTC) | What changed |
|---|---|
| `88af9cbd` 2026-09-14 01:25 | first Mirkholt, message "Agent B's set complete, opus5-mirkholt, and seven reviews"; the run report assigns Mirkholt to agent C, and its table of commits says the same commit holds B's set plus mirkholt |
| `33b15edd` 01:28 | re-drive of mirkholt |
| `16d39fde` 09:27 | wool rooms moved onto 25-block spurs; the stair off the brow removed; commit message: trees 8 to 17 a side, claims 30 placed 3 declined to 46 placed 1 |
| `6c5527cb` 09:54 | a `toe` piece makes both fronts the same 70 blocks; spawn pulled back; "the wood went from 45 blocks of depth to 25 and from 17 trunks a side to 11" |
| `8509f975` 10:40 | exact build zone x -35..35, z -15..15; east spur rotated; "the wood is 45 blocks deep again", board grown to 110 by 230 |

The last three are the author's two complaints answered, within about an hour of each message. The first of them, at 09:27, preceded his 09:41 message; `6c5527cb` answers 09:41, and `8509f975` answers 10:23.

Final state, from `review/opus5-mirkholt.md` and the stored world at `maps/ctw/mirkholt/`:

- 110 by 230 blocks, `rot_180`, ground y11 to y25, ten pieces at four surfaces, three themes (glade 47.1 percent, mirk 40.4, sike 12.4 of the ground cells), roofed forest biome.
- Two wools a team, each at the far end of a 25-block bare lane. The map.xml locations at the last check in the transcript were wools at (-50,15,92) and (45,15,92) with the red spawn at (-3,110), walks of 58 and 59 blocks.
- Plan reads: 0.0 percent dead, 11,160 walked, 42 scrambled, 48 barrier cells, "placed 34, declined 1".
- Two soft `WL10` terms ship outside their bands on purpose: `wool-front-remoteness` 128 against a band of 22 to 118, and `wool-front-ratio` 1.488 against 1.474. The pull request names this as the one open question for the author.

### Trees

The author's complaint is "a little too many trees". The record gives these numbers.

- The spec lays a lattice of copied-tree stamps over x -48..36, z 17..87 (about 3 blocks apart, kept 5 off the edges and 7 off the road centre lines), in a mix of one canopy giant in six, three dense crowns, two scrub.
- Authored trunks per half over the stages: 17 (09:24), 11 (6c5527cb), then 14, 12, 11 as the last re-drives settled (10:34 to 10:38), final 11 units on the authored half. `provenance.json` lists 20 tree stamps in the stored world (holt-0 to holt-10 on one image, ten on the other). A tree here is a copied body of nine to seventeen blocks across, so the count understates the canopy: the stored world holds 1,724 log blocks and 8,888 leaf blocks (my count from `tools/anvil.py`).
- The review itself says "the wood is thinner than it should be" and names the wood as the thing the board is named for, which it declined to cut a second time to satisfy `WL10`.

So the model argued the opposite way from the author: it believed it had cut the wood too far and restored it (`8509f975`, "the wood back").

### The houses

The only freestanding building is one charcoal-burner's hut on the garth (a fork of the `talltimber-cottage` library style, spruce planks, 241 plank blocks around (10..26, 72..88)). What the author calls box houses reads as the spawn hall and the wool rooms, built from the `hb-spawn` and `hb-cage` room styles. My block census of the stored world, in blocks at y 14 and above and excluding ground, leaves and trees:

| Region | Contents |
|---|---|
| Red spawn hall, x -12..12, z 94..116 | 380 stone brick, 275 mushroom stem, 219 polished diorite, 76 mossy cobblestone, 45 cobblestone |
| Blue spawn hall, mirror | the same (380, 275, 219) |
| West wool room, x -52..-28, z 78..96 | 307 stone brick, 140 mushroom stem, 82 andesite, 70 stone slab |
| East wool room, x 30..52, z 78..100 | 349 stone brick, 286 mushroom stem, 97 stone slab, 80 mossy cobblestone |

So the author is right about diorite: polished diorite (id 1:4, 438 blocks across the two spawn halls) is in the spawn hall. His "reskinned bedrock box" fits the `hb-` hollow-box room shells; I did not check the style definition itself.

### Podzol

Podzol (3:2) appears in all three theme stacks (glade, mirk, sike) in the finish document and in the theme reads (`THEMES` lines at 09:24 and 10:38). In the stored world, taking the topmost non-tree, non-leaf block of each column, podzol is the third commonest surface: 1,588 of 11,358 columns, 14.0 percent, behind grass (24.8) and coarse dirt (16.9). Grass is 2,814 columns and gravel 1,252. The finish file's `wall` runs put podzol on top of dirt (`(PODZOL,1),(DIRT,3),…`), which is the stack the author says this board avoids ("didn't stack podzol on podzol or dirt on dirt"); I did not check column by column.

### The "free" wool room

Two readings fit the record, and the transcript supports the first.

1. Before `8509f975`, the east wool room stood only five blocks behind the front band, so a raider reached it straight off the front line and its lane did nothing. The author said exactly this at 10:23:28 ("you can just jump to it from the front line"), and `8509f975` rotated the east spur to match the west one.
2. The final review notes the east spur's room "hangs 25 blocks south of the garth with void on three sides", the one piece of ground a defender can be cut off on. The west room (x -50..-30, z 80..95) overlaps the wood's z range (the lattice runs to z 87), which would put it beside trees.

The author's later description (a room too close to the forest, which "you could burn with flint and steel") is about a played version. I could not tell which commit was played or on which server.

## 4. What went wrong, and how it was noticed

- The first Mirkholt shipped as a solid rectangle of wood at `fill-ratio` 0.92 and was refused; the agent fixed it by reshaping the board into a shifted diagonal. Noticed by the studio's evaluator; the author then objected to the cost (09:41, 10:23).
- The first draft put the two wool rooms nine blocks from the spawn in one row. No rule refused it: `WL2` implements only its distance clause and `WL6` has no term. A read found it. Filed afterwards against the studio as `G263`.
- A fronts-face fix moved the build zone off the land: it overflowed ten blocks into each toe and hung fifteen past each end. Noticed by the author (10:23).
- A flight whose skirt and crown climb at the same rate has no face, and its keep-out had blanketed half the wood; removing it took barrier cells from 300 to 90.
- Run-level faults in the report: an interrupt killed all three agents at 28 minutes; 35 of 98 trees across the run stood on something that is not soil; `GET /coverage` cannot see a control point.

## 5. The author's reactions and rulings

His rulings in this stretch: the fronts parallel and the spawn 15 blocks back; the build zone only between the fronts, 25 to 30 blocks wide; the jumpable wool room rotated 90 degrees like its neighbour; the cubes in emerald block (15:31, which became commit `41f76cb`, "on the author's ruling"); and a one-line "this map is not good". The PR body quotes none of these.

## 6. His description set against the transcript

| Claim | Verdict |
|---|---|
| "contains mirkholt, a ctw map" | Confirmed; the session is the Opus 5 twelve-board run and Mirkholt is its dark-wood CTW board. |
| "a little too many trees" | Partly differs. The agent believed the wood was too thin and put it back; the world has 20 stamped trees but about 8,900 leaf blocks. A matter of how much canopy reads as a lot. |
| "pretty ugly box houses ... diorite" | Confirmed for the diorite: the spawn halls carry polished diorite and are boxes of stone brick and mushroom stem. |
| "one of the woolrooms is essentially 'free'" | Confirmed for the early east room (author's own message at 10:23:28 UTC) and fixed in the next commit. The forest-adjacent room is not established. |
| "uses podzol too much" | Confirmed in the sense that podzol is in all three themes and is 14 percent of surface columns. Not obviously more than coarse dirt. |
| "didn't stack podzol on podzol or dirt on dirt" | Not checked in the transcript. |
| "luckily you could craft flint and steel and burn the whole thing" | Not found (a play story). |

What the transcript adds: the author's own hand in the map was feedback, not design. Layout was reshaped under his two messages and the board still ships soft-term failures the review lists as "the author's to judge".

## 7. Who decided what (Mirkholt)

| Cell | Decided by | Executed by |
|---|---|---|
| Concept: dark wood, shifted diagonal, one hollow way a side | agent C (model), within the author's three ground families and four objective kinds | the sub-agent |
| Layout: shifted diagonal | model, to satisfy `fill-ratio` | the sub-agent via the studio's plan API |
| Layout correction: fronts parallel, spawn back 15, build zone only between fronts, 25 to 30 gap, east lane rotated | the author | sub-agent re-launched by the orchestrator |
| Terrain: hollow way, rolling relief, slope bands | model | studio relief solver |
| Colouring: three themes, podzol in each | model; the author had put podzol into the dirt texture group (his description) | studio's theme engine |
| Structures: hut and hb room shells | model, library styles | stamper |
| Objectives/XML: wools and monuments | studio writing from the plan | studio export |
| Trees | model (lattice rule in `build-spec.py`) | studio dressing pass, copied tree corpus |
| Finishing | orchestrator committed; agents' bytes only | `tools/drive.py` |

## 8. What is filmable

In `specs/opus5-mirkholt/renders/`: `world-iso.png` (the picture sent to the author at 09:54:38 and at 09:27:09), `world-topdown.png`, `world-xray.png`, `world-ground.png`, `world-foliage.png`, `theme-glade-surface.png`, `theme-mirk-surface.png`, `theme-sike-surface.png`, `room-spawn-plan.png`, `room-wool-plan.png`, `coverage.png`, and the text reads `03-slopes.txt`, `05-themes.txt`, `06-claims.txt`. The world is `maps/ctw/mirkholt/region`. A before/after pair can be built from commits `88af9cbd` (first) and `8509f975` (final) by re-rendering the world at each; the captions of the three images sent to him (17 trunks to 11, "the cost") are in the transcript.

## 9. Open questions for the author

1. Which version of Mirkholt was played, and where? The record has at least four.
2. What was "too many trees": count, or the closed canopy over the lanes?
3. Which wool room was close to the forest, and was it west (z 80..95 beside the wood's back edge)?
4. What were the contents of the opening brief and fault catalogue messages?

## What I did not read

His opening brief and fault catalogue, and everything before 2026-09-14 09:21 UTC except through the repository and the run report. I read user events (my paging covered 09:21 to 20:10 UTC) and the final assistant turns, not the sub-agents' own prose. `Murkwick` was checked only as a name.

## The opening brief (read from the start of the session)

**Not reached; the session's events were not paged at all.** Its stored facts (from the session record): created 2026-09-13 23:39:42 UTC, last updated 2026-09-14 20:10:03, title "Studio mapgen with Opus agents", model `claude-opus-5` at effort `xhigh`, 1,655,825 output tokens, about 309.67 USD, artifact "Twelve Boards, Three Grounds". With twelve boards authored by parallel agents over about 20 hours, paging to the first events would take a hundred or more pages of dense sub-agent traffic. The opening brief and the fault catalogue remain unread; the existing section 2 ("I did not read his opening brief") stands unchanged.
