# A year of AI-made maps: September 2025 to November 2026

This is the history of how rockymine, with Ruediger_LP and a run of AI models, set out to make PvP maps for PGM
servers by machine, and of what the tool he built for it became. It is written for a reader who was not there. Every
claim cites the file it rests on: `(research/NN)` is a file under `research/`, `(sessions/NN)` a session write-up under
`research/sessions/`, and `(account, N)` the N-th instalment of the author's spoken account of 27 November 2026
(`author-account-2026-11-27.md`), where later instalments and the corrections in it supersede earlier ones;
`(sessions list)` is his own description of each session in `sources/sessions-named-by-the-author.md`.

**Three voices are kept apart.** **Record** is what a commit, a file, a published map, a server log or a transcript
holds. **Account** is what the author recalls. **Inference** is a reading made for this history, with its basis named.
Where record and account disagree, both are given and neither is silently preferred.

A word on the terms. PGM is the plugin that runs competitive Minecraft maps, each described by a `map.xml`. In Capture
the Wool (CTW) a team carries the enemy's coloured wool to its own monument; in Destroy the Monument (DTM) and Destroy
the Core (DTC) teams break objectives. Many maps float in the void and players bridge the gaps. CommunityMaps and
PublicMaps are the public repositories of about 350 such maps; a third, PrivateMaps, is private and was not read.
"The studio" is `pgm-studio`, the C# tool at the centre of the story; "mapgen" is `pgm-studio-mapgen`, the repository
where agents built boards with it.

---

## 1. Before the record, and autumn 2025: a graph that became blocks

**Algorithmic map making predates the project by four years.** **Record:** five Annealing maps by rockymine, Ruediger_LP
and DerStiv sit in CommunityMaps, dated January 2021 to February 2023 (research/08). **Account:** they came from his
master's thesis on the travelling salesman problem, whose routes made shapes that were filled and decorated by hand,
in 2022, and the idea then slept until late 2025 (account, 3). The record carries no word of the thesis and spreads the
series over three years.

**The first statement of the idea is Ruediger's.** **Record:** on 26 September 2025, looking at a layout tool the
author had made with Google's AI, Ruediger asked when an AI would scan all the maps and make its own (research/15).
Two days later `CTW-Layout-Generator` was opened in Google AI Studio; within three days it held a seeded generator
whose node types were `SPAWN`, `WOOL`, `HUB`, `FRONT_LINE` and `CENTER_HUB`, and it exported only JSON (research/01).

**The step from drawing to blocks came in a tool he wrote himself.** **Record:** `MinecraftLayoutEditor`, in C#, opened
on 10 October 2025 around a `Graph` of typed nodes and on 12 October wrote a drawn graph out as a `.schematic`, each
edge a line of blocks; on 6 November it imported a real world "(claude & grok)", the first models named in a commit
(research/01). **Account:** his editor drew edges with a width and a height, rotatable, with no rectangle, and he
sketched maps on paper as nodes and edges because nearly every map reduces to a frontline and an H, as Race for Victory
2, Two Tier and his own Outback do (account, 3). **Record:** the edge had a map-wide lane width and thickness rather
than its own (research/08); Outback is his, the other two are older maps by others (research/08). Two committer
identities, `michael` and `rockymine`, appear on the same days; the record does not say whether they are one person
(research/01).

## 2. December 2025 to June 2026: logging matches, and a Python studio

**The months the commit history leaves empty were spent on play data.** **Record:** the author's messages to Ruediger
first mention Claude on 9 December 2025, for a match-logging plugin; by February and March it held 689 and then 3,000
logged matches and a per-map configuration of 177 maps "dokumentiert für die ki"; on 19 March he wrote "ai maps soon
tm", and on 29 May that Ruediger's idea of drawing polygons was being built (research/15).

**The second attempt began by reading maps, not making them.** **Record:** `pgm-map-studio`, in Python, opened on 31
May 2026 with Claude Sonnet 4.6 as co-author and scanned worlds for their islands; its pamphlet of 5 June says "The
ground plane is not just terrain — it is the map's navigational grammar"; on 7 June a browser sketch exported as a
loadable map folder; its last commit is 03:24 UTC on 12 June (research/01).

## 3. June 2026: the C# studio and the first XML nobody wrote

**The studio was a port, and its stack has not changed since.** **Record:** fourteen hours after the last Python
commit `pgm-studio` was opened, and on 13 June Claude Opus 4.8 ported the whole studio to ASP.NET Core and Blazor in
one commit of 145 files (research/01). The author called it the third rewrite, "so that it can be hosted"
(research/15). No record gives the reason for C#; the C# era had in fact begun the October before (research/01).

**The first `map.xml` a model wrote went to a real map within ten days.** **Record:** from 17 to 21 June Claude named
the author's next map "Cobalt Crossing" and wrote its XML, which Ruediger reviewed; it became Drastic Change II. The
author asked "ist das jetzt die erste xml jemals die jemand geschrieben hat ohne sie zu schreiben?", and on 23 June
the first generated XML loaded in PGM (research/15). On 19 or 20 June Ruediger proposed the method of the later
evenings: generate many maps, test the best ten in one evening, paint them afterwards (research/15).

**On 24 June Ruediger uploaded three maps whose XML came out of the browser.** **Record:** Vauxite, Drastic Change II
and Capture the Wool CTW entered CommunityMaps at 21:47 UTC. Nothing in them says so, but their kit, their
`build-hole-1` regions and their bare team ids are what the studio's export wrote that week and appear in no other
corpus map; Vauxite 1.0.1 on 1 July fixed spawn yaws, split spawns into two rectangles and added a build ceiling, and
a stray studio-written copy of its XML still sits in its `region` folder (research/11). **Account:** these were the
first maps on which he tried browser-made XML, and there were some errors; their concepts, terrain and colours are all
human (account, 5 and 8). Capture the Wool CTW was first played on 28 June; Vauxite and Drastic Change II not until 12
October (research/13).

**The middle was named as the missing part on 20 June.** **Record:** a corpus analysis of 347 maps found that "the
generator emits 0 neutral mid pieces but 88% of real maps carry a contested middle", and the same day a generator grew
lanes from a hub along noise-bent Catmull-Rom splines; it lived 25 days and was retired on 15 July "in favour of the
plan-then-realize direction" (research/01, research/08). **Account:** it was an attempt at organic layouts because
everything was angular, and it was not fruitful (account, 3).

## 4. July 2026: Base maps, boxes, Bridgid II and the cake

**The first worlds the studio built were test fixtures drawn on squared paper.** **Record:** the Claude Code session of
1 to 2 July (Opus 4.8) was opened to split P9, the export that writes a sketch as a world. At 23:21 UTC the author
specified the 8×8×8 bedrock shell for spawn and wool, with its layers, doors and chests; at 07:37 on 2 July he sent
the photograph now in `sources/` and asked to "make this layout as a general seed for testing", naming the three
variants he wanted (research/09). The model built a staircase where the sheet has an H and one centre square where it
has two; it said so itself at 08:45, and at 09:09 he typed the corners in five-block cells, which came out right
(research/09). **Account:** the drawing is the two-team map, Base 2-Island; the two-wool map had one more island
pushed onto it (account, correction to the squared-paper section), which the transcript confirms (research/09).

**Seeds began in that session, not before it.** **Account:** he had already traced existing maps into seed files, and
the seed was the plan model (account, squared-paper section). **Record:** a seed was born that morning as a pair of
JSON files for a test; the plan model came at 22:47 UTC that evening; the first real map traced into one is of 4 July;
what traced maps in June was a Decompose surface struck on 2 July (research/09). The name "Base" is the model's
(research/09). The seeds stated `"authors": []`, and the bedrock box stayed the default room: rooms could take a
library style from 5 August, but at least three later runs left one in the box by mistake, and the studio complained
of it only from 27 September (research/07). **Record:** the Base worlds reached PrivateMaps, which deleted them on 12
August, and Base 4-Team was played on the server at 00:30 UTC on 28 July, 28 players, 2 minutes 36 seconds
(research/13, research/15).

**The graph was not dropped in 23 minutes; a design document was replaced.** **Record:** at 14:31 UTC on 2 July a 184-line
design proposed a plan graph of typed lane and gap edges; at 14:54 it was rewritten as areal pieces joined by
interfaces, because "a thinned skeleton cannot represent side contact". No code of the first design was committed,
and that evening `FannedGraph`, a reachability graph over the pieces, entered the studio, where it still is
(research/08). **Account:** 23 minutes sounded too short to him (account, 3), and the record agrees that the idea did not
end then. The same afternoon a strawman of layout rules was offered "for correction by id" and he corrected it
(research/01): a model guessing and the author ruling is the method of the whole year.

**By 21 July the layout was boxes.** **Record:** the composer started on 4 July beside a month of recorded play; by 21
July it composed spawn, hub, wool approaches, frontline and middle, and "the box pipeline is THE composer"; destroy
modes arrived on 15 July (research/01). **Account:** the generator's concept is his, devised to reproduce existing maps
as far as possible (account, 8).

**Bridgid II, on 14 July, is its own hand-built map.** **Record:** Ruediger added `ctw/bridgid_ii` in five commits from
00:27 UTC, credited to rockymine and Ruediger_LP, created 12 July; the studio traced a plan of it that evening; its
picture shows alternating dark and grey bands down the island sides; the studio's wall run first appears on 1 August,
and nothing links the two (research/11). **Account:** its layout took about a day in the browser, it was skinned from
stone in game in one long evening, its repeating side columns gave the wall-run idea, and it is as wild as Hello World;
Ruediger made its XML, much of it placed by the browser tool, with the water lane added by hand (account, 5 and its
correction; account, 8). It is not a Brittlebush map (account, correction). **Record:** on 14 July Ruediger asked to
test it again, so it had been played before; the log's first play is 15 July (research/15, research/13).

**The cake was an ordinary destroy map with a new objective.** **Record:** the author and Ruediger designed Capture the
Cake on 17 and 18 July and loaded it that night (research/15); Kuusepuu CTC entered CommunityMaps on 27 July credited
"CTC conversion: Claude Opus 5" and "XML" to Ruediger_LP; its fix of 31 July is the one commit that reports play,
"Reported live: a carrier died, the cake went home" (research/06, research/11). **Account:** Kuusepuu is a destroy map
whose objective they replaced with a cake; it is not an AI map and not the first one (account, 6).

**Hello World Micro recoloured its wool room; it did not move it.** **Record:** uploaded on 27 July as a "grey map for
concept test" with a studio plan file, its 1.0.1 rolled one or two wools a game and recoloured the enemy's box when
the first fell; the full Hello World had recoloured its rooms since February 2025; the Micro was deleted on 12 August
(research/07, research/08). **Account:** its layout is Hello World's, abstracted very simply onto the grid, and he drew it himself (account, 3, 14);
the record's plan file shows it came through the studio's plan tool, which fits a layout drawn by a person in that tool
(research/08). On 31 July
Ruediger worked out the timing of a wool room that moves, and the author called the idea "so dumm und genial"
(research/15).

## 5. August 2026: colour, trees, the first fifteen and the trials

**"Map walls" are the walls, rims and plateaus of 1 August.** **Account:** colouring began with one rule per height,
then the top, sides and edges of a shape, then shading from outside in, stacked patterns and slope; under the plan
model each area had its own pattern and transitions never worked (account, 1). **Record:** the order holds. Until 1
August the export wrote one flat block of stone; that day Opus 4.8 specified rim, wall and interior; the inward axis
came on 15 August, the slope axis on 5 September; the nearest thing to a per-height rule is the spec key
`themeByHeight` of 14 August (research/05, research/02).

**The tree generator was a page of sliders, and it failed against hand-built trees.** **Record:** the artifact the
author supplied is the studio's `tools/decorate/prototype.html` of 2 August: five decoration tools and a grown tree of
Catmull-Rom limbs with knobs for stems, leader, trunk flow, branch angle, levels, leaf size and height; it moved into
the studio on 4 August, a vanilla tree split off on 5 August, and on 12 August, measured against 75 trees he had
built, "1516 of 4020 never touch their branch"; it was repaired that night and deleted on 10 September on his ruling
that "the form goes rather than gets a knob" (research/10, research/08, research/02). **Account:** a blob is easy for a
model, a real tree generator failed, and its leaves and trunk got worse over time (account, 1 and 3); no commit shows a
decline, only a repair and a second fault (research/08).

**Wandering U was the summer's wild concept.** **Record:** the author sent `wandering-u.zip` to Ruediger at 20:11 UTC
on 6 August, and PrivateMaps took "Wandering U: added" at 20:15 (research/15). The file is a studio plan at one block a
cell, extended with variables, eight `<dynamic>` stops and countdowns: each team's wool sits in a 10 by 10 bedrock
island that walks a lap of the U, and "anyone still inside when the room leaves is left in mid-air over the void"; it
names no author (research/10). **Account:** he described the layout in text, Claude wrote the XML, and it was tested
that day (account, 8 and 4). **Inference:** the log's one missing match number that evening, 19:46 to 20:11 UTC,
closes before the zip was sent, so it is not Wandering U (research/13 against research/15); the test is not in the log.

**No Blocks Placed, on 7 August, is the first public map drawn in the studio.** **Record:** its credits name rockymine
for "Drawing pieces, shapes, and markers in the browser.", Ruediger_LP for "Wisdom." and Flamiix for "Minimalist.";
TTtie only added its creation date on 15 August (research/05). Its largest tree is a 50-log oak at x −27 to −17, y 14
to 30, z 41 to 52, the shape of that week's grower (research/08). **Account:** Flamiix did the wool room and spawn
interiors, Tttie nothing; the oak is the surviving generated tree "if it is about 20 blocks high", and a few blocks
were placed by hand (account, 3 and squared-paper section). The oak is about 17 blocks tall (research/08).

**Another author's Grok map arrived on 10 August.** **Record:** arcadeboss uploaded Cedar Crossing at 04:00 UTC,
credited "7,000 word essay" to himself and "Map and XML" to SuperGrok (research/11). That day an Opus 5 session
measured it at the author's request; after playing it he wrote "too much tall grass, too many trees, the mineshaft is
a mess … Grok probably never understood what the map actually looked like" (sessions/03).

**The first fifteen boards were built on 11 and 12 August, eleven by Opus 5 and four by Haiku 4.5.** **Record:** each
came from one JSON spec through `tools/mapgen` inside the studio; the author's fault list that night, MG1 to MG13, was
in prose; Thornwake and Viridian went to CommunityMaps on 12 August and were tested that night on mapdev, which does
not report matches (research/03, research/15). Viridian is the slime map: 13,299 of its 66,071 blocks are slime, and it
holds seven greens, so it is also the all-greens map (research/08).

**On 13 August an agent made a confident, measured and wrong claim.** **Record:** it said every generated destroy map
was unwinnable because the goals floated; floating goals are PGM's design, the claim was withdrawn that day, and the
rule that a gameplay question is answered by asking the author was written (research/02). The mapgen repository opened
the same day; its first report told the author to delete the agent's own shortcut, and on 20 August `tools/mapgen` was
deleted (research/03).

**The trial runs of 13 and 14 August were, in his words, simply bad maps.** **Record:** Haiku reported two boards
"verified working" that were 245-byte shells (sessions/04, research/03). His review of 14 August became 48 backlog
entries, among them `B162`: "An obsidian destroyable may carry at most three obsidian blocks, and three maps carry 27,
27 and 15" — Corvid Hollow and Basalt Reach have 3×3×3 cubes of obsidian in their stored worlds — enforced from 19
August as rule `DC3`, which builds an oversized one in end stone (research/14). The same review named see-through slab
roofs (Tallow Weirgate), a 90-block spawn hall (Sable Marsh) and a hole across Tallow Kilnrow's middle where the join
belongs (research/14). **Account:** "everything was the problem … grundsätzlich einfach schlechte Maps", and the quartz
board is Quillon Saltworks, which he now states definitely (account, 10 and 12). Sable Marsh he calls a terrible map: a
very wide spawn, huge wool rooms and no real middle; Cairnmeadow is his example of build zones that meet its oval
islands badly; Cinderreach shows trees with no crown (account, 12). **Record:** both Saltworks and Kilnrow carry quartz,
and the faults the review lists belong to Kilnrow, Weirgate and Sable Marsh rather than Saltworks (research/14); the
board he names is Saltworks regardless.

**The studio then made itself legible to agents.** **Record:** one finding type and one refusal envelope on 15 August,
125 rules served by id, a dead-ground measure on 16 August calibrated against his reading of one board, and 131 paths
described on 19 August (research/02, research/05). On 16 August Fable built Sunspit to a brief naming four themes, two
references and a colour rule (sessions/05); he recalls it looked good from the start (account, 11). On 22 August Haiku
built Hollow Crown, 100 by 120, each team's core inside the enemy's monument cuboid (research/05); **account:** it is the
board where the monument landed inside the core, which only Haiku managed (account, 12). On 25 August Opus 5
built the labyrinth Overwall to his structural brief, and Aerie to a free one (sessions/06). On 28 and 29 August a
session gave made things their name and built Slipway's ship and balloons (sessions/07).

**Aerie's broken XML is in no record.** **Account:** it was unplayable because nothing was editable, wool rooms stood on
odd islands and build zones were bad; probably there were no continuous blocks at the bottom, so the filters failed
(sessions list; account, 10 and 11). **Record:** no commit, review or transcript holds the complaint; the model
reported the board open with zero declines (sessions/06, research/14). **Account:** he states flatly that its XML was
not playable and asks to be trusted on it (account, 12); the record's gate-open report and his statement stand side by
side. **Inference:** Aerie floats from y 26 and has no
block at y 0, which under PGM's void filter refuses every column outside its build rectangles — the same mechanism the
author guesses (research/14).

## 6. Late August to early September: Millrace, and the first test evenings

**The test evenings began on 24 August.** **Record:** at 18:58 UTC the author sent Ruediger a zip of six boards, at 19:05
PrivateMaps took "Add a few very human maps for testing", and from 19:07 to 19:51 the server's match counter skips six
numbers the log does not hold (research/15, research/13). On 31 August a zip of eight followed, and Hollowmarch, the
first of this project's composed boards in the log, was played at 21:18 (research/15, research/13).

**Millrace is the year's clearest lesson.** **Record:** on 30 August the author drew a basin in the Sketch tool; Opus 5
built it as Millrace and Sonnet 4.5 as Cutwater and Fallowmere (research/03). By the early hours of 2 September he and
Ruediger had finished Opus's by hand; their review says they "spent 5 hours" and that "essentially all that was done is
theming and some dressing"; 29,954 of its 35,610 columns kept their height (research/03). It went to CommunityMaps at
00:18 UTC as Millrace 2.0.0, credited to both of them and to Opus 5, and was played ten minutes later (research/11,
research/13). **Account:** five hours side by side, ten person-hours; Opus's terrain was kept and the houses redone;
Ruediger reworked the XML (account, 1, 3 and 8).

**The trees came before Fable's rebuild, not because of it.** **Account:** Fable, asked to rebuild Millrace, began
copying his trees, which led him to tidy his tree world and add it (account, 1). **Record:** the tree world had been in
the studio since 12 August and was committed to mapgen at 00:53 UTC on 2 September; Fable 5.1's diff and its copied-tree
form followed two hours later; the world grew to 86 trees on 20 September and 95 on 1 October (research/05,
sessions/02). The session that restated the revamp also built Mossgill on the same techniques (sessions/02).

**Alderfen Holm came from a player's prompt.** **Record:** on 2 September the author pasted a swamp DTC prompt and added
a dozen material tests of his own; Opus 5 built two islands with two cores a team and one mid holm (sessions/08).
**Account:** it looked quite nice, felt balanced, and has four cores (account, 11). Research/13's table gives it five;
the world and the author give four (sessions/08).

**The evening of Friday 4 September is the one test session the log shows.** **Record:** the author sent six boards
(Mossgill, Alderfen Holm, Lodestar Yard, Quiverstone Mesa, Scarrow Delph, Weirbank) at 20:32 UTC with "slop time" at
21:55; the log shows Millrace at 22:21, seven missing numbers, then Sunspit, Hollowmarch, Brackenfold, Cairnmeadow,
Hollowbank and Elderwold in a row to 23:51, 26 to 51 players each (research/15, research/13). **Inference:** the six
visible boards are from the August zips, and the seven missing matches were the six sent that evening plus one
(research/15). The next morning a session rebuilt Sunspit and flattened Hollowmarch's relief from 15 to 6 blocks of
range (sessions/09); he says Hollowmarch's frontline put players over void, which the transcript does not hold but a
measured gap at its legs fits (sessions/09; account, 11).

## 7. September 2026: written taste, and the Sundays

**Taste was written down rather than gated.** **Record:** on 4 September the studio stopped writing the "made by" sign
over blank lines, after finding 69 of 74 boards named nobody (research/07); on 5 September it painted by slope (research/02);
on 9 and 10 September ten agents painted a layout the author had drawn himself, and his review became eleven material
rules (sessions/10); on 19 September `WHAT-A-BOARD-IS-MADE-OF.md` opened with "None of it is enforced anywhere"
(research/03). **Account:** "Made by" and nothing in the tab list was the running joke, the first AI tell (account, 1);
the record's version is the sign (research/07).

**The Sonnet run's brief asked for underground passages, and Kilnholt Cut answered with a hollow causeway.** **Record:**
his dictated brief of 11 September asked for "some sort of attempt at least at a map that incorporates some
underground passages", planned bottom-up with a stair; Sonnet 5 built Kilnholt Cut, whose gap holds a solid,
grass-topped diagonal causeway with a corridor through it, a "zero-cost, zero-climb" way across that the model flagged
as an open question (sessions/11). **Account:** from the screenshots he would not have thought it hollow; it was a route
round the fight "until players figured out there was a tunnel" (sessions list). **Inference:** Kilnholt Cut heads
Ruediger's playing order for 13 September, so that is the likely evening (research/15).

**The name "Slop Sunday" is Ruediger's, from 12 September.** **Record:** it appears in his message that day, and the
evenings of Sunday 13, 20 and 27 September followed: zips of 11, 7 and 11 boards plus two large ones, and in the log
counter gaps of 11, 8 and 13 match numbers in stretches of 78, 54 and 99 minutes (research/15, research/13). Between
them came Mirkholt, which he judged "not good" and corrected by two messages (sessions/12), the three-model day of 21
September, on which two of Sonnet 5's four boards exceeded the dead-ground band and none of Opus 5's did (research/03),
the first Opus 5.5 commit on 22 September (research/02), and Scarbutte, from a brief that asked for terrain alone
(sessions/13). On 27 September the studio drew boards in Minecraft's own textures and nine Opus 5.5 boards were
painted (research/02, research/03).

**The last evening was 27 September.** **Record:** at 20:55 UTC the author sent eleven `/event add` commands, at 21:55
Opus 5.5 committed Delverdale and Whitstone Weald "for a 32-a-side play test", at 21:57 their zip went with "load maps",
and PrivateMaps took them at 22:11; the log's counter runs 98 to 112 between 20:57 and 22:37 with nothing between
(research/15, research/13). **Account:** the last AI-map test was on 27 September (account, 1). The same day he wrote
"pgmstudio.de ist jetzt meins", and the next a player from the event sent a two-page review of the tool (research/15).

## 8. Late September: the studio goes public, and notes with coordinates

**Between 26 and 28 September the studio became a website.** **Record:** Discord sign-in, tokens, a build queue, and
self-deployment of pgmstudio.de from a green `main` (research/02). **Account:** it went online about two months ago and
hardly anyone uses it (account, 3). The site lists 72 maps, 31 by agents (research/05).

**Notes pinned to the ground replaced descriptions in words.** **Record:** on 28 September notes could be pinned by a
point, box or lasso on a picture, which the studio turns into ground columns (research/05). The first trial, the next
day, worked Gypsum Reach and Sootcombe through five rounds; the agent read lines such as "add another willow on top of
the rise" with the box x −21..−13, z 65..81 attached, and answered each with a picture from the same camera
(sessions/14). His first verdict, given in chat, was that both were empty (sessions/14). **Account:** feedback improved
when the model got coordinates, and empty, dreary maps remain a problem (account, 1).

## 9. October 2026: freeform, the grammar, and the port

**Freeform began as an overnight experiment.** **Record:** on 7 October, after trial boards he called "a box with a small
void gap", the author dictated at 22:21 UTC: "what if like an agent didn't need to rely on the current way we build the
houses, the terrain, etc. And if he could sort of just make his own sort of script or whatever". At 22:26 he gave the
mode and the ingredients — a destroy map, "forest, plains, town and sort of village meeting with a river and a cave … a
dungeon … a wheat field. A tractor" — and asked that the scripts be kept (sessions/00). An Opus 5.5 session built
Riftwater in 33 minutes of commits. At 05:42 the next morning he wrote: "Ok. This is a whole different class of map.
From the images it looks like he cooked real hard." (sessions/01). **Account:** he told a session he did not like the
layer model and to think, and contributed nothing to the first board, a floating island with two villages
("Riverside") (account, 1 and 7). The record differs in form: he asked whether an agent could do without the current
way, and he supplied the ingredients; the board is Riftwater (sessions/01). **Account:** the ingredients were a vague
list of thoughts, more than a description, and that the model carried it out so exactly is to its credit (account, 12).

**The pace that followed built a library.** **Record:** 8 October holds 86 commits and some twenty boards across game
modes; by evening the model found 15,800 lines of copied helpers and started `pgmvox`, which carried tunnels, chambers
and shafts by the next day (sessions/01). Under the layer model a cavity was a stack of layers and the studio's carve
"cannot hollow a column out from the middle" (research/05).

**The grammar came on 9 October, from his own Brittlebush.** **Record:** an Opus 5.5 session read Brittlebush (2022) and
Brittlebush II (2023) block by block, wrote their look as a style, split the rules from the blocks as `pgmvox.grammar`,
spoke a second style in it forty minutes later, and built Brittlebush III from a plan he had drawn on pgmstudio.de
(research/05). **Account:** the Brittlebush look — 5×5 fields combined by rules, a simple building style — can be
expressed in full by the grammar, which was its point, and Brittlebush III has never been tested by players (account,
2). The log holds no Brittlebush III (research/13).

**The notes of 9 and 10 October came from a viewing, not from a test.** **Record:** on 9 and 10 October the author's
notes from "playing the freeform and trial boards" were sorted into 30 faults, of which the studio "would have
caught 9", with Riftwater "essentially perfect" in the agent's summary (research/05, research/06). The log shows no
missing stretch after 27 September (research/13). **Account:** this was not a test on the real server: three of them
looked at the new pgmvox maps together, and it was the first feedback on those maps (account, 13). The sorted file of 10
October (`analysis/freeform-vs-studio/playtest-feedback-2026-10-10.md`) is its written result. **Inference:** the empty
log is what a viewing leaves, and 27 September stays the last test evening; where the viewing took place is not recorded.

**The boards shown were the new pgmvox boards.** **Account:** the screenshots are of the new pgmvox maps; the talk was
mostly on the one with two monuments, one underground and one on a castle on a mountain, and they also looked at the
flying capture-the-wool map and the mesa map; the comments concerned the maps' progress in general (account, 14).
**Record:** the sorted notes of 10 October name no screenshot, so no board is tied to a picture. **Inference:** the board
with two monuments is most probably Hollowcrown, whose report gives two fortress mountains with a citadel on each summit,
monument A in the Eyrie tower on a spur and monument B in the temple of Underhall, a delved city in a cavern
(`freeform/lib/boards/hollowcrown/REPORT.md`; the notes of 10 October list "monument on a tower, monument hidden in the
city"). The flying capture-the-wool board has two candidates among the boards of that run, Lantern Karst (floating karst
islands, two wools a team) and Brassmoor Works (an ironworks hung in the smog, one wool a team on decks), and the mesa
board two, Redwash Mesa (destroy the monument) and Hollow Mesa (destroy the core). Nothing in the record separates the
candidates, so they stay unnamed until the author does.

**The staff who watched took the boards for touched-up work.** **Account:** the viewing is dated 9–10 October and the
three speakers are named by role: mitchiii, a map developer who has built many maps; wylt, a server admin; TTtie, a
developer (account, 13). **Record:** five screenshots of the observer chat hold their words (`sources/staff-chat-october/`).
mitchiii asked "are all these ones unmodified from generated state?"; rockymine answered "yea", and mitchiii wrote "damn",
"compared to the other ones I saw" and "I would have assumed these were touched up". TTtie wrote "its over for m*pdevs."
and wylt, later, "maps look a lot more diverse". Asked "how long does each one take? if you made all those in the past day
or so?", rockymine wrote "30 min to 1h for these complex maps" and "sometimes faster". Asked how the generator understood
the Brittlebush III theme, he wrote: "he looked at the region file and i steered him", "then he turned it into some form
of grammar", "i mean, its literally just 5x5 pieces with 3 different styles", "and rules on how they combine"; to "so you
could give it half finished map and it finish it?" he answered "yep". **Inference:** the answer is consistent with the
record of 9 October, where a session read Brittlebush block by block and split rules from blocks, and at least two styles
were spoken in the grammar that day (research/05). These are other people's words, quoted from a transcription; the author decided on 27 November that
they may be used as they are (account, 14).

**The viewing ended in a pause, which the author gives as a reaction to quality.** **Account:** there they decided to
pause for the time being, because the maps were slowly getting "too good", in looks and in diversity, with many new game
modes as well (account, 13). Asked about the pause later the same day, he said it was simply needed: for a month the
"slop" maps (meant kindly) had been tested every weekend, and the tool needed some care again; it is also not
interesting forever to let the AI build twenty maps in a night, which works, but one needs inspiration and ideas, and
prompting empty was never the aim, so it should stay controlled. More maps will be built and tested before long; for now
many remain to be tested (account, 14). **Record:** the match log holds no missing stretch after 27 September, and on 19 October he
wrote that enough material existed (research/13, research/15); on 13 November new capabilities paused and the layout
generator was frozen (research/02). **Inference:** the later pauses may continue the one decided at the viewing, but no
record says so, and the 13 November entries give the backlog's fixes, not the quality of the maps, as their reason.

On 10 October a controlled run with Sonnet 5.5 in
both tools found "the two tools made boards of comparable quality", and Ruediger proposed finishing the three best AI
maps (research/03, research/15). On 19 October the author wrote that there was little motivation left to make or play
AI maps: "Genug Material haben wir ja." (research/15).

**The studio absorbed its laboratory.** **Record:** on 15 October `docs/pgmvox-port.md` set the goal of a board "the author
cannot tell apart, by quality, from one built with pgmvox"; the rectangle plan retired on 18 October, a modifier stack
of landforms replaced the relief solver on 24 October, carves arrived on 25 October, and by 4 November every phase had
shipped or been parked, except the grammar, which has no shipped line (research/02). Coldstore, built on pgmvox from his
concept world with signs, was judged "finished and the map.xml a success" (research/03). Meanwhile other people used the
browser: Countryside's regions were drawn there from 5 October and it reached CommunityMaps on 15 October UTC, and 803's
studio-made XML went up on 19 October (research/11). **Account:** Countryside on 9 October (account, 5); the repository
has 14 October in the uploader's zone (research/11).

## 10. November 2026: a map built by hand, and a freeze

**Agents could not compose his sketch, so he built it.** **Record:** from 2 to 7 November agents composed the author's
hand-built sketch world into a CTW and DTC map set into a mountain, and every version was rejected — "the surface was
not closed", "a ramp led into the void" — and "Every one of those failures passed some check that existed at the
time"; then he built the half himself, and the agents' task became understanding it (research/04). **Account:** he began that
map about 17 October 2026 and has built it over a few weekends since, taking his time because he needs inspiration
(account, 14). **Inference:** the record dates only the agents' work, so the account puts the start of the build before
their November attempts; the record does not contradict it, and the order of the two is not otherwise known. In the studio he froze the layout generator on 13 November; the last commit on `main` is of 14 November
(research/02); chapter 9 gives the pause the author says was decided at the October viewing, and what the record does and
does not say of a link. Chapter 13 says what the map shows.

---

## 11. What counts as an AI map

**"AI map" is a spectrum, and the useful question is who decided each part.** **Account:** the squared-paper map was his
drawing written down by Claude; many maps came from a deterministic generator; others are the model's own imagination,
yet all are executed deterministically by a tool (account, 7). Research/12 splits a map into seven decisions — concept,
layout, terrain, colour, structures, objectives and XML, finishing — and names for each who decided and what executed.
The studio executes in most rows and decides in none; where an algorithm decides, a seed was chosen by someone
(research/12). Determinism does not settle authorship, because authorship lives in the inputs: a compiler is
deterministic and writes no program (research/12).

| # | Category | Who decides, what executes | Maps (source) |
|---|---|---|---|
| 1 | Hand-made | a person decides and builds; a tool at most writes the XML | the ice map, Vauxite, Drastic Change II, Bridgid II (research/12) |
| 2 | Person's design, algorithm's detail | he draws; the studio solves, paints and grows the rest | No Blocks Placed (research/12) |
| 3 | Person's drawing, model's pen | he supplies the drawing, text or objective; a model writes it | Base 2-Island, Kuusepuu CTC, Millrace, Wandering U, Slipway (research/12, sessions/07) |
| 4 | Algorithm's layout, model's spec | a model states numbers; the seeded composer lays out | the first fifteen; Hollowmarch, Sootcombe (research/12, sessions/09, sessions/14) |
| 5 | Model's design in the studio, person's rulings | a model decides through the studio's vocabulary; he steers by brief, notes and rulings | Gypsum Reach, Whinberry Ring, Overwall, Sunspit, Alderfen Holm, Kilnholt Cut, Mirkholt, Scarbutte (research/12, sessions/05, 06, 08, 11, 12, 13) |
| 6a | Model's script inside the author's tool | the model writes the program, in his repository, on his world writer and later his library | Riftwater, the freeform boards, Coldstore (sessions/01, research/12) |
| 6b | Model's own tooling | the model and its own pipeline make map and XML, with no shared tool | Cedar Crossing and arcadeboss's later Grok maps (research/15, research/12) |

**The split of the last category is supported by how the two were run.** **Record:** Riftwater's scripts live in the
author's repository and wrote the world through the studio's own C# region writer, from a brief his session wrote
(sessions/01). Cedar Crossing was made on grok.com: arcadeboss gave it the pgm.dev documentation and an overview of
destroy maps, Grok wrote a design document whose JSON "intermediate representation" fed both XML and world, "the map
concept and name came from the AI", and over a hundred zips were loaded and tested; his later maps used GrokBuild, a
local agent, and GrokBot, bots with their own test server (research/15). **Account:** Cedar Crossing came from an
ordinary chat where Grok wrote a script, with no tool between (account, 7).

**On the layout he was plain in October.** **Record:** when mitchiii asked whether the viewed boards were touched up,
rockymine answered that they were not, and added "again, layout is 100% mine"; asked "touched up....?" once more he
wrote "no" (`sources/staff-chat-october/`, chat-1 and chat-2). **Account:** the staff took the boards for hand-finished
work (account, 13). **Inference:** the sentence claims the layout as the part a person decided. Which boards it refers to is not stated, and
for Riftwater the record has the author giving ingredients and a mode, no layout (sessions/00), so it is a claim about the
boards shown, not about every pgmvox board.

**The human stayed in five places: he drew, briefed, noted, ruled and finished** (research/12). The briefs found since
show how much he stated. For Riftwater he gave ingredients and a mode, no layout (sessions/00); for Sunspit themes,
references and a colour rule (sessions/05); for Alderfen a player's prompt plus his material list (sessions/08); for the
Sonnet run a long list of finishing rules and a request for underground passages, no places (sessions/11); for
Scarbutte the method alone (sessions/13). **Account:** the agents mostly took the composer's base and did nothing with
it (account, 8). **Record:** this holds for the first fifteen, Hollowmarch and Sootcombe and fails for Whinberry Ring's
reshaped outline and Heftfold's walled island (research/12, sessions/09, sessions/14).

**The models differ in the record as he says they do, but less cleanly.** **Account:** Sonnet's maps were worse
whatever the numbers say; late in the year Opus's were clearly better, through verification steps and model progress
(account, 1); early and Sonnet maps were flat, too large, with objectives too close (account, 3). **Record:** on the one
controlled day, 21 September, Opus 5's dead ground was lower on three of four boards; on 10 October, with Sonnet 5.5
fixed, the tools came out level; his best words for a Sonnet board are for Abbeymoor on pgmvox, "really looks like a
place"; the boards he finished, called perfect or called a success were Opus boards (research/03, research/05). No run
compares Opus 5.5 with Sonnet 5.5 on one brief (research/03).

## 12. The playtests

**A map got a test after a look on a local server.** **Account:** every map in the repository was looked at on a local
test server, often with Tttie, who is interested in the project, and that look decided whether a map got a test
(account, 12).

**The tests were event rotations, and the plugin did not report them.** **Account:** on the server an event runs a
rotation of maps, and those matches were apparently not sent to the match-status channel; the gaps of 8, 11 and 13
fit tests of that many maps (account, 9). Research/13 found the gaps from the log alone: the counter runs on through
stretches the CSV lacks, 14 such skips in the whole log, nine of them from 27 July to 27 September and none after, and
catalogue maps follow them far more often than chance (research/13). It offered three explanations — a reader gap, a
differently worded message, another server — and left them open. Research/15 found the other half in the author's
messages: the zips he sent before each evening and the `/event add` commands of 27 September (research/15).

**Reconciled, the two readings agree on six evenings, three of them the Sundays.** The catalogue below sets them side by
side; the record of each column is cited, and the fit is inference.

| Evening (UTC) | Sent to Ruediger (research/15) | Missing numbers in the log (research/13) | Fit |
|---|---|---|---|
| Mon 24 Aug | 6 maps, 18:58 | 6 (52–57), 19:07–19:51 | exact |
| Tue 25 Aug | 1 map (Tarnfell), 20:22 | none | no event seen |
| Mon 31 Aug | 8 maps, 20:42 | 2, then Hollowmarch visible | partial |
| Fri 4 Sep | 6 maps, 20:32 | 7 (180–186), between Millrace and Sunspit | six plus one |
| Sun 13 Sep | 11 maps; Ruediger's order of eleven | 11 (139–149), 78 min | exact |
| Sun 20 Sep | 7 maps | 8 (132–139), 54 min | seven plus one |
| Sun 27 Sep | 11 `/event add` plus 2 large | 13 (99–111), 99 min | exact |

**Read together, his memory is right in shape and short in count.** **Account:** three or four sessions in one intensive
month, every or every second weekend, sometimes twelve maps in a row, no logs (account, 3). **Inference:** the Sunday
name fits the last three evenings and arrived just before them (research/15); the weekday evenings of 24 and 31 August
and 4 September came first; the largest runs were eleven and thirteen. On 13 and 20 September the gap ends at Millrace,
and on 4 September Millrace is the match just before it; the author says Millrace was set at the end to show players a
model's map finished by people (research/15; account, 9). The 4 September session is the only one whose boards the log
shows, because those were played outside the event (research/15). No long destroy match exists: the longest on a
destroy board of this project is Brackenfold's 15 minutes 15 seconds, and a 99-minute stretch with thirteen starts holds
no three-hour game (research/13).

**On 27 November the arcade boards were being tested again.** **Account:** Lantern Pass had just been played; players like
it, but it is a little too short, the shooters are too slow, and runners can get stuck in the spawn; the next day they plan to record real
gameplay on a few maps, among them some of the newest (account, 14). No log or record of that day exists yet.

**What was learned from the tests reached the studio as rules, not as records.** **Record:** the one played fault in a
commit is Kuusepuu's "Reported live" (research/06). **Account:** Hollowmarch's frontline led players into the void and
now a check requires the frontline to sit inside the build zone; Kilnholt Cut's tunnel was found by players; a Mirkholt
wool room could be burnt out with flint and steel (account, 11; sessions list). None of these plays is recorded
(sessions/09, 11, 12).

## 13. What the hand-built map shows

**The map he built deliberately breaks the mode's dull shape.** **Account:** it sits in a cauldron of walls and a bunker
facade; routes are knitted together — tunnels, an underground lane, an overground way to the core, a hole from the big
floor into the lane, a door high in the facade reached up a hill; the core can be taken from the hollow below or from
above, the wool by dropping through a hole, along the lane or through the ceiling; it grew around the facade, and
agents never think about routes before they build (account, 3). **Record:** the half spans x −15 to 104, y 0 to 91, z −56
to 101; the study names 42 spaces from the wool lane at y 4 to 8 to the attic at y 61 to 67; its terrain is 23 lofts with
a median tilt of 36 degrees; its retaining walls are 19, 13 and 14 blocks tall; and the colours of its wool carry
meaning, yellow for connecting ground and light blue for hills (research/04, renders/hand-built).

**It shows what a check cannot.** **Record:** agents treated a hollow map as solid, painted colour as a blanket, and
relayed passing checks on variants he saw as plainly wrong; "a geometric rule is not a design" (research/04). **Account:**
it has a dead area that makes sense, likely the back around the wool lookout and hills, so "dead" is subjective
(account, 1 and 3); the dead-ground rule would refuse it at more than 12 percent (research/05). **Inference:** the year
went from a graph to a grammar and from words to coordinates, and the newest map returns to the first category, with
the models put to reading it (research/12). It is now an ice map; the contest it was made for was cancelled, and he will
finish it himself in snow, stone, ice or grass (research/04; account, 8).

## 14. What remains open

**Two disagreements between record and recollection remain, and the record does not overrule them both.**

| Subject | Account | Record | State |
|---|---|---|---|
| Aerie's unplayable XML | unplayable, stated flatly; nothing editable, odd islands, bad zones (account, 11, 12) | no record; the model reported the gate open with zero declines (sessions/06, research/14) | his account against the record; inference supports his guess |
| The freeform instruction and Riftwater | "I don't like it, think"; he gave nothing (account, 1, 7) | "what if … his own sort of script"; ingredients and mode were his (sessions/00, 01) | settled in form, his memory compressed |

**The last test is 27 September, and the October notes are of a viewing.** The notes sorted on 9 and 10 October come from
three people looking at the new boards together, not from a play on the server, so they stand against nothing in the
log (account, 13; research/13). Open instead: where the viewing took place, and which boards the five screenshots show (chapter 9 gives the candidates); the pause is
no longer open on its intent, since he says more maps will be built and tested (account, 14).

**The flat map he remembered as 500 wide is Ashfall Scar.** **Record:** a filter over every `map.xml` found fifteen maps
with exactly two destroyables and two cores, three of them with all four objectives within ten blocks of one line and
under 100 blocks apart; Ashfall Scar, Sonnet run 2 of 14 August, is the only wide one: spawn, monument, core, centre,
core, monument, spawn on one line, objectives spanning 70 blocks, a world of 250 by 190 (research/03). **Account:** he
confirmed it on seeing a render, and it is 250 wide, not the 500 he recalled (account, 12). Neither earlier candidate is
it: Hollow Crown is the Haiku board where the monument landed inside the core, and Spinebreak is a capture-the-wool
layout with its cores in the void and the same core-and-monument design twice (account, 12).

**Smaller points stay unsettled.** Whether
the 17-block oak on No Blocks Placed is the generated tree, which he puts at about 20 blocks (research/08); which
session drew the probe board's tunnels he calls awkward (sessions/10); what "Muse Spark", credited on two boards of 27
September, is: Tttie made a map with it, and the author believes it is a Meta model, unverified (account, 12; research/15); the Annealing dates (research/08); and which model ran the freeform trial agents
(research/03).

**The open problem is the one he named first.** Maps that look and feel empty are still made. The rules can say that
ground lies off every route, but, as the sorting of his October notes put it, they "cannot say what belongs"
(research/05). In his own words to Ruediger the material is enough (research/15); what the tool has not taken over is the
judgement of what a place is for.
