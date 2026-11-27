# The author's account, 27 Nov 2026 (rockymine, spoken, in German; summarized)

Status: brainstorm. Do NOT build the film yet. First research and write the history down properly; the author
reflects with Ruediger tonight and will add more. He wants active questions.

- "Map walls" = how a large shape is coloured. First prototype: one rule per Y level for a whole surface (y 0 =
  bedrock). Then the insight that for a big block one can compute what is its top, its sides, its edges; then
  surfaces shaded from outside in, patterns stacked. The grammar came with the Python attempt (pgmvox): a look
  defined once for a whole map — e.g. the Brittlebush look he designed — a formula that transfers to any map.
  WorldEdit has replace commands but no such grammar; no building plugin does this. Blending colours is still
  hard. Angle-based (slope) colouring was an important step: it tells a story where plain layers do not. Under the
  plan model, one area had one pattern and another area another, and real transitions never worked.
- The "500-wide" map: could be either candidate; he remembers one core and one monument per team; must look
  in game. The point: flat, nobody walks 250 blocks sideways where nothing is; enemy objectives ~10 blocks
  apart make a moshpit with no flanking.
- Tttie: a mapmaker, not an active contributor like Ruediger, but they talked often and ran the map tests
  together — "Slop Sundays" on the server, about two hours of playing the AI maps. Early maps looked and played
  alike.
- Sonnet's maps were de facto worse, whatever the numbers say (instructions or model, unknown). Late in the year
  Opus maps are clearly better: verification steps, and model progress, which stays a black box.
- Feedback got better with the review tool: early on he described faults in words and the model lacked
  coordinates. Two maps were extremely empty; maps that look and feel empty and dreary remain a problem. Good
  terrain shapes are possible now, thanks to the Python rework ("freeform" in the repo; first board a floating
  island with two villages, "Riverside" or similar).
- Why the rework: the purely layer-based definition hit a hard limit; cavities were very hard because cave walls
  had to be defined one by one; noise-based shaping is easier but has its own limits (the new hand-built
  experiment cannot be expressed in it either). He told a Claude session he did not like it and to think; Python
  came first (in the mapgen repo, usable), then its functions went into the C# studio and the website.
- Trees: a vanilla-like blob or disc is easy for an LLM to code; a real tree generator failed. One generated tree
  survives in the map "No Blocks Placed" — a CTW map made mainly in the web editor, authors rockymine, Ruediger
  and Tttie; a few blocks were placed by hand after all. Brittlebush III's layout was made in the editor but its
  colouring entirely in game (things still not expressible).
- Millrace: he drew the layout in the browser; an agent made the landscape (tried Sonnet and Opus, kept Opus's
  terrain). He and Ruediger finished it together: 5 hours side by side, 10 person-hours. Then Fable was asked
  to rebuild it as faithfully as possible; it began copying the trees, which led him to tidy his world of custom
  trees (under 100) and add them to the repository. Tree building is "a religion"; a boulder or a house is easier
  because it is not organic. Of the AI's work, the landscape stayed (hills, rock shapes); settlements and houses
  were redone and trees added.
- The browser tool is fast for trying layouts, which is the main problem of mapping; flying around in game is
  slow. Concept maps such as the labyrinth were his ideas, built 1:1 to probe limits. Is the JSON a
  domain-specific language? It limits, and how the LLM exploits it was interesting.
- Maps got prettier at the end through texture rules and telling the model where ground is dead — but "dead" is
  subjective: his own hand-built map has a dead area that makes sense. Its files come later.
- The server is small, a niche project; the UI is not much used; he finds the level-design question interesting.

- Added later the same day: the last AI map test was, as far as he can see, on 27 September 2026. The tests should show in the commit messages of the CommunityMaps repository, because Ruediger always uploaded the maps.
- Added later: the tested maps may have gone to PublicMaps, or to the private maps repository (no access). Brittlebush III has never been tested by players. The Brittlebush style CAN be expressed in full — that was the aha moment of the grammar: the map is 5x5 fields combined by rules, a simple building style.
- The "Base" maps (Base to Rule, Base for Teams; he thinks three): he drew layouts on squared paper and gave them to the AI; out came a stone world with different heights — the first map made this way, before the Brittlebush layout. Bedrock floor, stone fill to a height, a bedrock block for the wool and for the spawn. That bedrock box stayed long, and because it is still the default, later agents sometimes left the spawn unstyled.
- None of the AI maps had an author, so the tab list showed "Made by" and nothing: the running joke was "another map made by", the first AI tell.
- Capture the Cake and Hello World Micro were game-mode experiments in XML, outside the storyline. Hello World Micro's layout was AI-made; its wool room moves; it was tested once and players fell out of the world as the room moved from under them.

## Third instalment, same day (answers to the follow-up questions)

- Flamiix helped a little on No Blocks Placed (interior of the wool room and the spawn building); he happened to be on the mapmaking server and became an author. Tttie did nothing on that map.
- The surviving generated tree on No Blocks Placed is a larger tree fairly far forward on the map, beside ordinary ones. The tree editor then was spline-based: number of main trunks, how branched, and so on. Leaf distribution and the central trunk got worse over time; Millrace's first trees were meant as pines but had leaves only at the sides, like a fir with every tier cut off but the lowest. So the generator was removed in favour of plain typical trees and the hand-built ones. Not every generated tree was broken, but most were.
- Slop Sundays: three or four, in one intensive month, every or every second weekend, sometimes twelve maps in a row. No documentation, no logs. The maps were most likely uploaded to the PRIVATE maps repository by Ruediger, whose role is map developer (rockymine is a builder). There are three map repositories: PublicMaps, CommunityMaps, PrivateMaps.
- The 500-wide map: he wants both candidates rendered so he can say which.
- For fixed-scope research Sonnet agents are enough.
- The hand-built map: the artifact already shows every block, so the world files should not be needed. The likely "dead" area is the back, around the wool room and the hills. The map sits in a cauldron, enclosed by walls and by the bunker facade; from a team's side it drops to the right into the wool lane. Many routes are knitted together: tunnels, the underground lane, the overground part to the core, from the spawn room onto the big floor and through the hole down to the lane, a door high in the facade reached up the left hill. The core can be attacked from the hollow below (building up) or from above via the flank and tunnel; the wool by dropping into a hole, by the lane (meant as the main way), or through the hole in the ceiling. Routes are formed by the terrain. Agents never think about routes beforehand; the path is only computed afterwards. He did not plan it all either: the map grew around the bunker facade; the lookout that will hold the wool existed, he wanted it underground, then added the stairwell to connect it. It deliberately breaks the mode's basic form, which had grown dull: fights end up on a second level of player-built sky bridges and the wool room is always at the end of something.
- Why CTW first: nearly all maps break down to the same shape — the joke is that all maps are the same — a frontline and e.g. an H form: Race for Victory 2, Two Tier, Outback. Hence the idea of a graph of nodes and edges; nodes are where players meet. His own first tool (MinecraftLayoutEditor) drew edges with a width and height in a web editor, rotatable, with no concept of a rectangle; he sketched on paper as nodes and edges. The Google AI Studio tool also worked with edges and could trace an existing map. The plan to digitize every existing layout for an LLM failed because complex maps (his concept maps, the "annealing" maps) do not fit the model.
- The annealing maps: 2022, from his master's thesis on the travelling salesman problem; the routes made interesting shapes, which were filled and cast into maps — the first algorithmic map making, traced and decorated by hand. The idea then slept until late 2025 / early 2026.
- The "graph idea dropped after 23 minutes" sounds too short to him. In between there was also an attempt at organic layouts from randomized, combined splines, because everything was very angular; it was not fruitful and the format unappealing.
- Millrace: finished after 5 hours together, two people, so 10 person-hours.
- Brittlebush look: generic; reducible to 5x5 fields; a 10x5 field looks different from a 5x5; a tree needs a 10x10 field; the surface breaks into rectangles separated by lines; layers and sides are built from varied panels.
- What made early (and Sonnet) maps worse: totally flat, too large, objectives so close the fight made no sense. In the first tested maps, which all looked alike and used an early layout generator: buildings turned toward the void so players fell out, terrain continuing under buildings leaving gaps, bedrock slabs meant for a wool room carrying a monument and being deformed by the terrain. Block choice: despite a prepared list of greens, every green landed on one map; a map made mostly of slime blocks (ugly, bad to play, laggy, broken instantly); quartz with end stone as a strange desert. Now maps can look good; whether they play well is another matter and depends on layout, size and the number of routes. A flat map with one way to the objective fails; a monument or core needs an approach from above and from below.
- pgmstudio.de went online about two months ago; hardly anyone uses it; who does is not important.
- The squared-paper drawings should still exist; he will look on his phone.
- Hello World Micro is not the moving-wool-room map: there the room changes colour; its layout he made by hand as a small version of Hello World, built earlier with Ruediger without algorithms, deliberately bizarre (lava floating in water); Brittlebush II is similarly wild. A different, late map — built by him, probably in CommunityMaps or PublicMaps — has the wool room that moves.
- Trivia, unrelated: New Life CTW / Old Life CTW (contest around 2020–21; eight wools, each team needing only certain ones, placed at an enemy team; nobody understood it; they came last; the XML was changed to a standard map = Old Life; the contest was won by a map built with school children).

## The squared-paper drawing (sent the same day)

`sources/base-map-squared-paper-drawing.jpg` is the author's photo of the layout he drew on squared paper for a Base map: pencil outlines of rectangular pieces, a green-filled middle, a vertical axis line with a centre point, two orange and two blue dots at the four ends, the whole figure point-symmetric about the centre. Which of the three seeds it is has not been confirmed (it looks like the two-team, two-wool one committed as "H with centre spine", pgm-studio `febb21ce`, 2 July 2026). By his account the model did not read the photo well; he then expressed the layout as the coordinates of its corners, and that worked. He found the chat and the branch; the chat is https://claude.ai/code/cshk_014BYG9EwhkDRUmRP1FYLBk2UvyCeMdb7XutVXPSixGeqX (not read here).
Confirmed by the author afterwards: the drawing is Base 2-Wool. The pencil outlines are the islands, the green area the build region, the line the centre line and the grey dot the centre point; the orange dots were the spawns and the blue the wools, "or the other way round". No drawings exist for the other two Base maps; the four-team one is simply four of these islands.
Corrected by the author a little later: the drawing is the TWO-TEAM base map (the record's "Base 2-Island"), not Base 2-Wool; the two-wool map simply had one more island pushed onto it. The chat is the Claude Code session `session_014BYG9EwhkDRUmRP1FYLBk2` ("P9 backlog task breakdown", created 2026-07-01 22:10 UTC, Opus 4.8, started from Android, branch `claude/p9-task-breakdown-ufx0s9` of pgm-studio). He recalls that at that time he had already traced existing maps with the tool and stored them as seed files — the seed concept was the plan model (rectangles and heights) — that tracing other maps' islands into one data format proved too varied, and that these Base maps were probably the first maps actually built that way.
Later still: the map whose wool room moves is called "Wandering U" (as heard; spelling unconfirmed). Checked the same day: no path and no commit message in CommunityMaps or PublicMaps contains "wander", so it is not in either public repository under that name. The author takes the 50-log oak on No Blocks Placed (x -27..-17, y 14..30, z 41..52; about 17 blocks tall) to be the surviving generated tree, "if it is about 20 blocks high".

## Fourth instalment, same day

- The map with the wandering wool room ("Wandering U") was tested on 6 August 2026; he supplied it as a zip (kept outside git: it comes from the private maps repository).
- He checked: the test maps all ended up in PrivateMaps, by decision, because they are experiments and twelve at a time got out of hand; there they are easy to delete. A Discord bot records when maps were uploaded, and a server log records which map was played when; he can look both up by hand, which takes a while.
- Another artifact, https://claude.ai/artifact/JvGM5hGiW8L3t4Ni8S6Amj, contains the tree generator: by his account the point at which a map's decoration came into being, and what the later decoration is based on.

## Fifth instalment, same day: dates the author read off the private repository and Discord

Voice-transcribed; map names in quotes are as heard and need checking. All 2026.
- 24 June: Ruediger added "Drastic Change 2", "Walkside"/"Vauxite" (unclear) and a capture-the-wool map; their XML was made in the browser — the first maps on which the author tried that. It worked, with some errors that should show in the commits.
- 2 July: more maps added by Ruediger (unspecified).
- 14 July: the Brittlebush map (heard as "Bridget") added; built in practically one day — layouts used to take months of disagreement; in the browser it was quick — then "skinned" from stone in one long evening. Its repeating colour columns on the sides are where the wall-run pattern idea came from, later a studio feature.
- 27–28 July: the cake map (Capture the Cake) and Hello World Micro (the wool room that changes colour), tested briefly.
- 6 August: Wandering U uploaded — an outlier, wild concepts they wanted to try.
- 7 August: No Blocks Placed — the first map made public on which all the decoration was tested.
- 10 August: Cedar Crossing by Arcade Boss appeared in CommunityMaps — by the author's account the first AI map there, made with Grok (blocks and XML), without a system like the studio, from a long Word document.
- 12 August: "a lot happened", among it Viridian, which also reached CommunityMaps.
- 24 August, 25 August, 31 August: maps uploaded (private).
- 2 September: the reworked Millrace.
- 13 September, 20 September: maps added (private).
- 27 and 28 September: Ruediger added maps to PrivateMaps, among them Delverdale and Whitstone; tests presumably took place.
- 9 October: Alphaboy uploaded Countryside to CommunityMaps — the first map by another person who used the web interface to upload a map and draw its regions (browser-made XML). Later the updated map "803" also had its regions made in the browser. So two maps by others so far.

Typed by the author afterwards: the map added on 14 July was "Bridgid II" (his spelling).

CORRECTION to this file (the note-taker's error, not the author's): "Bridgid II" is a map of its own, not a Brittlebush map. CommunityMaps has it as `ctw/bridgid_ii`, added on 2026-07-14 by RuedigerLP (`a842b0bd` "Bridgid II: added", then `fe035adf`, `ce45916a`, `5701b66d`, `ae4d8f9e` the same day). Wherever the sections above say that "Brittlebush III's layout was made in the editor but its colouring entirely in game", that the 14 July map was "the Brittlebush map", or that "Brittlebush II is similarly wild", read BRIDGID II: its layout was made in the browser editor in about a day, it was skinned from stone in game in one long evening, its repeating colour columns on the sides gave the idea for the wall-run pattern, and the author calls it as wild as Hello World. The Brittlebush maps are separate: their look (5x5 fields combined by rules) is what the colouring grammar was built from, and Brittlebush III has never been tested by players.

## Sixth instalment, same day

- A Claude agent in the author's browser is reading the server's Discord match-status channel since June; each match post links to statistics (when played, players, winning team, duration). The result will be filtered for the AI maps and sent on.
- Kuusepuu is an ordinary destroy-the-monument map whose objective they replaced with a cake (that is Capture the Cake / "Kuusepuu CTC"); it is not an AI map and not the first one. He believes other AI maps came before it, and that nothing happened before June because the tool was not far enough along.
- Countryside: the regions were drawn in the browser earlier than the upload; errors in them had to be corrected, by him or by Claude, and then it was uploaded. 19 October may be the update of 803 — a side note, not an AI map; that day the tool also got fixes because the wool-to-team and monument assignments were wrong.

## Seventh instalment, same day: what makes a map an "AI map"

The author's point: it is a spectrum. The squared-paper map was his drawing, written into a map by Claude with the tool of the day; many maps came from the generator, which produces deterministic layouts; others are the model's own imagination, e.g. the first freeform board, to which he contributed nothing — yet all of it is executed deterministically by a tool. Cedar Crossing (Arcade Boss) is different again: made in an ordinary chat, where Grok wrote some script and a zip with map and XML came out, with no tool in between. He asks for a breakdown: where a human is involved, what is tool, what is algorithmic, and what is really AI.

Framework proposed in reply (to be filled from the record): split each map into decisions — concept, layout, terrain shape, colouring, structures and decoration, objectives and XML, finishing — and for each say WHO DECIDED (a person, a model, or an algorithm with a seed) and WHAT EXECUTED it (the studio deterministically, a script the model wrote, or hands in game). The studio always executes; what varies is who decides.

## Eighth instalment, same day: answers to the "unknown" cells, and the match log

- Briefs (first fifteen, Gypsum Reach, Heftfold): he offers to find the sessions if given the dates. Dates from the record: the first fifteen 11–12 August 2026 (pgm-studio `tools/mapgen` begins 12 Aug 20:05 UTC, `5897944a`); Heftfold first committed 12 Sep 06:41 UTC (`fc91b3be`); Gypsum Reach 28 Sep 23:00 UTC (`ae025473`).
- Wandering U: he described the layout in text; Claude wrote the XML.
- Vauxite, Drastic Change II, Bridgid II: all concepts, terrain and colours are human. Bridgid II's XML was made by Ruediger, though much of it came with the browser tool, which then (the plan model) placed things automatically; only adjustments such as the water lane were added by hand — he believes the water lane was the only one.
- Millrace: Ruediger reworked the XML of the published version, as far as he remembers.
- The ice map: he will build it to the end himself; materials undecided — snow, stone, ice, grass; a cold map.
- Cedar Crossing: he may be able to answer from his chat history later.
- Overwall: no hand finishing.
- The layout generator: the concept of the algorithm is his, devised to reproduce existing maps as far as possible. What comes out is generic, as limited as it is, but a base to work on — and the agents mostly took the base and did nothing with it, not even adjusting other aspects of the layout.
- The match-status log, read from Discord by an agent in his browser, is on this branch under `sources/match-status/` (commits `1d4470ea`, `444745e6`). He notes that some maps do not appear in it (the moving-wool-room map is not found), that there is clear evidence of one test session with several maps played in a row on one server, and that there should be more such sessions; he asks for a cross-check.

## Ninth instalment, same day: why match numbers are missing

The author's explanation: the missing matches were the tests. On the server one can start an event with an event rotation — maps are put in and run through — and matches played that way are apparently not tracked: a fault of the plugin the server uses, so nothing is sent to the match-status channel. On 20/21 September the gap ends with Millrace, which they set again afterwards. So the gaps of 8, 11 and 13 fit tests of that many maps, but which maps is not recorded; he could work it out from what he sent Ruediger each time.

## Tenth instalment, same day: on the write-ups of the trial-run session

- The criticism of the map with unplayable XML (Aerie) and the 27-block monuments is in the logs and commits; at some point oversized monuments were prevented. That the labyrinth concept is not verbatim does not matter; it was probably at the unread start.
- The quartz map is probably Quillon Saltworks, not Kiln Row. Every board built in that session was of poor quality — "everything was the problem": the blocks used; how the houses were built; pitched roofs made of top slabs one can see through; spawn areas and spawn buildings too large; a layout that did not fit, with a huge hole in the middle where nobody can build and every player has to walk round, left or right. "Grundsätzlich einfach schlechte Maps."

## Eleventh instalment, same day

- Sunspit looked quite good from the start; the problems named were fixed in later iteration.
- Alderfen has four cores, nothing else; the Discord log does not record core leaks, so a "fifth" in the log is not something he can explain (the match page behind the link may tell a different story).
- Aerie's broken XML: he can only guess — probably because there are no continuous blocks at the bottom, so the filters did not work. Later the studio took buildability ("editable") as a variable and checks concretely whether a core can be broken at all; that is marked in the web interface and told to the agent. Aerie was never converted to the newest format, but in it the map, or its XML, would raise the alarm.
- The Hollowmarch session: he is fairly sure Hollowmarch was adjusted there too, not only Sunspit. He never said in it that a playtest had taken place — he did not need to. The fact is that the ground, then called "relief", was too high, and that there were the problems at the frontline, for which a check now exists: the frontline must sit entirely inside the build zone.
- He allows the start of the trial-run session to be read. An agent on his PC has also looked at which maps were sent to Ruediger for the tests; a commit may have arrived.

## Twelfth instalment, same day

- "Muse Spark": Tttie made a map with it; the author believes it is a model from Facebook (Meta). Unverified here.
- Quillon Saltworks IS the quartz map. Sable Marsh is a terrible map: a very wide spawn, huge wool rooms, no real middle.
- Aerie: "you can just trust me, the XML was not playable."
- How maps reached a test: they (often with Tttie, who is interested in the project) looked at every map in the repository on a LOCAL test server, and decided from that whether a map got a test.
- Riftwater: he did supply the ingredients — a vague description, more a list of thoughts; that the model carried it out so exactly is to its credit.
- Hollow Crown is the map where the monument landed inside the core — only Haiku managed that. Spinebreak is a different case: cores in the void on a capture-the-wool layout with monuments where the wool was, and for no reason the same core-and-monument design twice.
- Cairnmeadow is the perfect example of bad build zones: they meet the oval islands very badly. Cinderreach shows the utterly broken trees with no crown.
- The "500" map is neither of the two: it must have spawn, monuments and cores on one line, all cores and monuments within less than 100 blocks, and exactly two monuments and two cores.

Checked the same day against every map.xml under maps/ (objectives resolved through their regions): fifteen maps have exactly two destroyables and two cores; three of them have all four within ten blocks of one line and under 100 blocks apart — Ashfall Scar (Sonnet run 2, 14 August; world 250 x 190; objectives span 70 blocks; both spawns on the same line), Hollow Crown (100 x 120; span 65) and Haiku DTM Tower (90 x 120; span 40). Ashfall Scar is the only wide one: a flat board whose whole game runs down one line through the middle, with wings on both sides. It is 250 wide, not 500. Offered to the author as the candidate; not yet confirmed.

Confirmed by the author on seeing the render: Ashfall Scar is the map he meant ("Das ist sie!"). It is 250 x 190, not 500 wide.

## Thirteenth instalment, same day: the viewing of 9–10 October

The notes of 9–10 October were not a test on the real server: three of them looked at the maps together. It was the first feedback on the new pgmvox maps. There they decided to take a pause for the time being, because the maps were slowly getting "too good" — in looks and in diversity, now that many new game modes exist too. Quotes from the staff team come from that viewing: `sources/staff-chat-october/` (mitchiii, a map developer who has built many maps; wylt, a server admin; TTtie, a developer).

## Fourteenth instalment, same day

- The ice map: begun about 17 October 2026 and built on a few weekends since; he takes his time because he needs inspiration.
- The maps in the chat screenshots were the new pgmvox maps. The talk was mostly on the map with two monuments, one underground and one on a castle on a mountain; they also looked at the flying capture-the-wool map and the mesa map. The comments were about the maps' progress in general.
- Hello World Micro's layout is simply Hello World's, abstracted very simply onto the grid; he drew it.
- The staff quotes may be used as they are.
- Which map filled the extra match numbers he cannot know, the data being missing.
- Today (27 November) they are testing some of the arcade maps again. Lantern Pass has just been played: players like it, but it is a little too short, the shooters are too slow, and runners can get stuck in the spawn. Tomorrow they plan to record real gameplay on a few maps, among them some of the newest.
- The pause: it was simply needed — for a month they had tested the "slop" maps (meant kindly) every weekend, and the tool needed some care again. It is also not interesting forever to let the AI build twenty maps in a night: it works, but one needs inspiration and ideas; prompting empty is possible but was never the aim — it should stay controlled. More maps will be built and tested before long; for now there are still plenty to test.

Added on 27 November: besides Lantern Pass, the arcade boards still to be tested that day are Curio Square, Lantern Drop, Spark and Loomfall.

## Fifteenth instalment, same day

- The boards at the 9–10 October viewing, confirmed: Hollowcrown (the two monuments, one underground, one on the castle), Lantern Karst (the flying capture-the-wool board) and Hollow Mesa; the very first freeform board was shown too.
- Lantern Pass, tested 27 November 2026: match https://oc.tc/matches/112edd. Read from that page the same evening: "Casual Match", Season 41, status "Match over", duration 01:08, score Runners 1 – Shooters 0; top kills 4, top deaths 1, top damage dealt 57.56 hearts, top arrows shot 39; no authors shown on the page, no absolute date, no player count. (The author's notes on it are in the fourteenth instalment: liked, a little too short, shooters too slow, runners can get stuck in spawn.)
- Match ids on oc.tc are not sequential (e.g. a486f4, aa2409 on one day), so the pages of matches missing from the log cannot be found by counting.
