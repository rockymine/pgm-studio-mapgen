# Session 11: the Sonnet 5 "five new maps" run, and Kilnholt Cut

## 1. Header

| | |
|---|---|
| Session | `session_015yVFHGt6eLzrN6oTXTcHez` |
| Title in the studio | "Five new maps with design guidelines" |
| Created / last updated (UTC) | 2026-09-11 23:32:54 to 2026-09-12 11:23:06 |
| Model | `claude-sonnet-5` ("Claude Sonnet 5" in the commit trailer), effort `high`, permission mode `auto`. This is Sonnet 5, not 4.x and not 5.5; the 5.5 boards are a later run (2026-09-29 onward, `BOARDS-BUILT.md`). |
| Origin | `android` (the author started it from his phone) |
| Repositories | `pgm-studio` (branch `claude/studio-maps-tasks-tw091p`) and `pgm-studio-mapgen` (`main`); outcome branch `claude/five-new-maps-4jjo32` on both |
| Size | 868,746 output tokens, about $73.73, context 303,398 of 1,000,000 used |
| Shape | One orchestrating Sonnet that wrote a shared brief and ran five builders, one per map, in parallel. The transcript interleaves the five builders' tool traffic with the orchestrator's, roughly 70 events per minute at the busiest. |

## 2. What the author asked for

I could not read his opening message. The transcript is paged newest-first, and the stretch around 00:11 to 00:30 UTC alone costs about one page per 70 seconds of the run; I stopped at 00:11:34 UTC with about 40 minutes of the session above me unread. What I can say about the brief comes from three places.

The closing request, the only user text I read, is at 2026-09-12 11:22:04 UTC:

> "Please send the top down and iso renders to me (dont think you showed them to me yet; they were done already with the drive script) with a short description of each map and a self-reflection on how the additional very long prose comment of myself at the beginning helped or hurt you."

Gloss: send the renders and say whether the long opening message helped.

The model's own self-reflection (11:23:04 UTC, final turn) describes that opening message: long, voice-dictated, a "run-on" that restated the same idea "three or four ways in a row". It names "ground trees" (the model took it as "grown trees") and "ready of hold mode" (relief hold mode) as dictation artefacts. The content it extracted was a set of rules "that aren't written down anywhere in the repo's docs":

- house footing must stay null;
- a beam course needs a plain log course too;
- checker-pattern logs must be two species;
- no shed roofs;
- solid three-colour path triads;
- never mix grass and podzol;
- finish terrain by slope angle, not height;
- the plan is rectangles only, and the real shape is drawn in the sketch one vertex at a time.

The commit message of `f8593017` (2026-09-12 00:30:26 UTC) repeats the same rules as "the author's material, path and house-construction rules", and adds that every board "avoids the removed procedural tree".

So the brief was rich in finishing rules (material, path, house, ground) and, going by the model's account, thin or absent on layout. The model says it "compressed your message into one shared brief" before any builder touched the API. That shared brief is not in the repository and I did not find it in the transcript.

Whether the author named "a quarry", "an estuary" and so on, or the model chose the five places, I could not establish. The same day two other model sessions of the project produced boards "to the author's brief" with overlapping themes. Haiku 4.5's `732b364d` (2026-09-12 05:22 UTC) lists a "Quarry Clash" and a "Harbor District"; Fable 5.1's `b54841e4` (00:14 UTC) has "a quarry with an adit" (`fable-ashcombe-delph`) and a quay. That points to a shared prompt that suggested such places, but it is an inference.

## 3. What was built

Five boards, one commit (`f8593017`, 2026-09-12 00:30:26 UTC, `Co-Authored-By: Claude Sonnet 5`), each with `specs/<slug>/` (a `build-spec.py` that generates plan and finish documents), `maps/<slug>/` (world), `reports/<slug>.md` and `review/<slug>.md`. The branch was merged into `main` at 18:56:52 +0200 on 12 September (`1717c988`). The specs then moved to `specs/archive/` (`5a869dca`, 23:02 +0200). On 10 October worlds were re-filed as `maps/<mode>/<name>/` (`d9c2d891`).

| Board | Mode | World now |
|---|---|---|
| `sonnet5-kilnholt-cut` | destroy the monument, two a side | `maps/dtcm/kilnholt_cut/` |
| `sonnet5-sable-reach` | capture the wool | `maps/ctw/sable_reach/` |
| `sonnet5-fellgrave-hollow` | destroy the monument | `maps/dtcm/fellgrave_hollow/` |
| `sonnet5-talltimber-yard` | destroy the core | `maps/dtcm/talltimber_yard/` |
| `sonnet5-emberwood-vale` | capture the wool | `maps/ctw/emberwood_vale/` |

`BOARDS-BUILT.md` (section "Sonnet 5, five boards, each one its own place") adds that "the place was decided first and the mechanism second".

### Kilnholt Cut in detail

Sources: `reports/sonnet5-kilnholt-cut.md`, `review/sonnet5-kilnholt-cut.md`, `specs/archive/sonnet5-kilnholt-cut/build-spec.py`, the renders in that folder, and the stored world read with `tools/anvil.py`.

The board is 80 by 188 blocks, `rot_180` about the origin, base surface 16. Each team has one landmass with its spawn fused to a quarry excavation. The two landmasses are separated by a permanent void gap, x -40..40, z -16..16, which is also the build zone. Two obsidian destroyables a side stand on the excavation floor at (-19,-50) and (19,-50) for red, and the mirror image for blue. The ground has one theme finished by slope: grass below 28 degrees, coarse dirt and andesite from 28 to 44, bare stone above, measured 67.9 / 6.3 / 25.7 percent. There is one winch shed, a path and six spruce.

The hollow structure, which the report calls "the adit" or "tunnel":

- It is a diagonal run from the red portal at (-30,-22) to the blue portal at (30,22). It is a straight line through the origin, so it is its own `rot_180` image and was authored once.
- It is built bottom-up in layers: an `override` cavity on the ground layer with the floor at y1, side walls on `tunnel-walls` at base_y 1, a roof on `tunnel-cover` at base_y 4, and two more blocks of rock on `tunnel-resume` at base_y 6. A stair rises 11 blocks from the tunnel floor to the surface at the red end.
- The report's probe at the middle of the gap, `column?at=0,0`, reads bedrock y0, open air y1 to y3, solid from y4.

What the stored world shows when I read it (my own read, not in the transcript):

| Column | Contents |
|---|---|
| (0,0) | bedrock y0, air y1-3, stone y4-5, dirt y6, grass y7 |
| (-30,-22), the red portal | bedrock y0, stone y4-5, a top at y6; y1-3 empty |
| (-20,-15), (-10,-7), (5,4), (15,11), (25,18) | the same pattern: bedrock y0, open y1-3, stone y4-5, grass top at y7 |
| (30,22), the blue portal | bedrock y0 only |
| (0,-12), (0,12), (±10,0) | empty void |

Along z=0 the body spans x -6 to 6 (13 wide) and the hollow is x -2 to 2, about 5 wide. So the structure in the gap is a solid, grass-topped diagonal causeway about 8 blocks high with a corridor running through it, floating in the void between the two halves. Seen from outside it reads as a bridge, and the corridor inside is invisible. That matches the author's account. I did not verify whether the grass top at y7 is reachable on foot from either side. The apron at the void edge is y6, and I read no connecting cells.

The render `renders/world-section-x0.png` (a cut at x=0) shows exactly this: a small grey block with a green cap and a hollow base, alone in the void. In the isometric and x-ray renders (`world-iso.png`, `world-xray.png`) the gap between the halves looks empty except for two red build-zone lines, and the structure is not obvious from the camera height. The model's caption for the picture it sent the author reads "the iso shows the mine adit's west portal cutting under that gap". The report and review describe the corridor as "under the gap" and "under the west flank", while the world has it standing in the gap. That is a difference in wording between the model's account and the block data.

The report also records that "the only zero-cost, zero-climb way across this board is through the tunnel": the walk from red's spawn to blue's deep mark reads `rises 0, falls 0, worst step 0`. The model flagged the free flanking route as an open gameplay question ("Should the tunnel cost something?") and did not decide it. It described the brief as calling the tunnel a reward "for whoever is bold enough to use it".

## 4. What went wrong, and how it was noticed

All from `reports/sonnet5-kilnholt-cut.md` and `review/sonnet5-kilnholt-cut.md`; I did not read the builder's turns.

- The first excavation was 104 blocks wide. `coverage` read 30.3 percent dead before any picture was looked at; narrowing to 80 blocks gave 9.4 percent. Caught by a check.
- A `subtract` for the walkway on a new layer was refused with `SK13`, because the rule compares the document's shapes, not the resolved world. The model replaced it with two plain `add` strips. Caught by the store's refusal.
- The stair's `anchor_heights` were in the wrong vertex order and produced a twisted ramp; found by probing the column at the portal.
- Moving the destroyables to fix `GO2` broke `GO1`, then `GO4`; `/plan/inspect` after each move caught each one. Final read: GO1 3.31 and 3.41, GO2 38.
- Left open: `SK11` still names 350 cells of standable ground near the west portal "with no route onto them". The model said it did not trace them.
- A studio gap found along the way: `EX6` ("the map names no author") fires on every drive although `authors` is in the exported `map.xml`.
- The hidden fault, noticed only by players: the tunnel is a free route round the fight. The report notices the free crossing as a design question and does not call it a defect.

## 5. The author's reactions and rulings

In this transcript there is only the final request (11:22:04). Everything else he says about the session is the later description below, in the sessions list. The commit message of `f8593017` credits "the author's" rules. `BOARDS-BUILT.md` records no ruling on Kilnholt itself.

## 6. His description set against the transcript

| Claim | Verdict |
|---|---|
| "some sonnet maps" | Confirmed: five boards, `claude-sonnet-5`. |
| "kilnholt cut ... fun and unexpected, but still ugly and basic" | A judgement; nothing in the transcript contradicts it. The report calls the board "deliberately simple and single-themed" (commit message). |
| "from the screenshots the model shared during design i would not have thought ... the diagonal bridge structure that connects red and blue teams halves was hollow" | Confirmed by the world. The diagonal structure is a solid, grass-topped body with a hollow corridor (section above). The only pictures the model sent him are the top-down and isometric renders (11:22 UTC), and the isometric caption speaks of a "portal cutting under that gap", so the corridor was never shown as the thing the bridge contains. Whether he saw the x-ray render is not in what I read. |
| "a quick route to the other team's side by avoiding fighting entirely" | Confirmed as a property of the geometry: a zero-cost, zero-climb walk through it from either spawn. The model had flagged this as an open question. His playtest story ("until players figured out there was a tunnel") is not in the transcript. |
| "surrounded by walls ... all the same angle, you can't walk on top of them" | The shipped design supports this reading: a rim held at y28-30 by `rim-w`/`rim-e` marks, and a cut face of 25.7 percent at 40 degrees or steeper. Not discussed in the transcript. |
| "a thousand times better ... mine is organic and intentional" | A comparison with his handmade experiment; not in this session. |

Correction to the description: the structure is not under anything. The report says "under the void gap" and "under the west flank"; the blocks put it in the gap. Also, the hollow run is diagonal across the whole gap, about 60 blocks end to end (portal to portal, 30 in x and 22 in z each side of the origin), and the report says the blue stair is the `rot_180` image of the red one, but the stored column at the blue portal (30,22) holds only bedrock; I did not trace the blue stair's cells.

## 7. Who decided what

| Board | Concept | Layout | Terrain | Colouring | Structures | Objectives / XML | Finishing |
|---|---|---|---|---|---|---|---|
| Kilnholt Cut | model (place), possibly from a suggestion in the brief (unread) | model; build-spec.py generates it; checks by the studio's `GO` bands | model through slope-banded relief marks | model, following the author's slope-axis rule | model: one forked cottage shed; the tunnel by layers | model placed the destroyables; the studio's `GO1`, `GO2`, `GO4` bands settled the distances | the studio's dressing and export, driven by `tools/drive.py` |
| the other four | model per board | same | same | same | model, three of five with forked house styles | same | same |

The author's hand in all five: the finishing rules (footing, checker, path triads, slope rule) and the review of the pictures after the run.

## 8. What is filmable

Under `specs/archive/sonnet5-kilnholt-cut/renders/`: `world-topdown.png`, `world-iso.png` (the pair the author was sent), `world-xray.png` (headed "17 roofed void(s)"), `world-section-x0.png` and `.txt` (the hollow body in the void), `world-section-z0.png`, `incline`/`slopes` readings in `03-slopes.txt`, `04-routes.txt`, `coverage.png`, `world-traversability.png`. The same folders hold equivalent renders for the other four boards. Worlds in `maps/dtcm/kilnholt_cut/region/`. For a before/after, `reports/` and `review/` carry the 30.3 to 9.4 percent coverage change as text only.

## 9. Open questions for the author

1. Did the opening message name the five places, or only the rules? The model's own account suggests it was mostly rules.
2. Did you see the x-ray render or the section? Which picture made you think the diagonal was solid?
3. When players found the tunnel: on the deployed server, in what round, and how was it noticed? (Not in any record I read.)
4. Is the grass top of the diagonal walkable, or was the tunnel the only way across?

## What I did not read

The opening message and everything before 2026-09-12 00:11:34 UTC (about 40 of the 60 minutes before the commit), and the sub-agents' individual turns. The transcript was read from the newest end down to 00:11:34 UTC, but of that range I read only the assistant text and the author's messages, not tool results.
