# Twenty-one months of AI-made maps: February 2025 to November 2026

This is the history of how rockymine, with Ruediger_LP, a few friends on the Overcast Community server and a run of AI
models, set out to make PvP maps for PGM by machine, of what the tools he built for it became, and of how the players
who were handed the maps received them. It is written for a reader who was not there.

**Every claim cites the file it rests on.** `(research/NN)` is a file under `research/`; `(sessions/NN)` a session
write-up under `research/sessions/`; `(account §N)` the N-th instalment of the author's account of 27 and 28 November
2026 (`author-account-2026-11-27.md`), where §1 is the opening summary, §2 the additions later the same day, §3 to §20
the numbered instalments, and "squared-paper section" the section of that name; later instalments and the corrections
in the file supersede earlier ones. `(sessions list)` is the author's own description of each session in
`sources/sessions-named-by-the-author.md`; `(sources/early-experiments/)` the pictures he sent with §18 and §20, his
message of 11 February 2025, and the v0 chat read from his link. Two data sources recur: **the log** is the `#match-status` channel as read
into `sources/match-status/match-status-2026-06-01_2026-11-27.csv` (research/13); **the API** is the server's public
match record, of which the 388 public-server matches the log never posted are in
`sources/match-status/api-matches-not-in-match-status.csv` (research/16). Match start times below are the API's
`started_utc` unless marked; research/16's evening table gives some evenings by the first start and the last end.

**Three voices are kept apart.** **Record** is what a commit, a file, a published map, a server record, a recording,
a picture or a message holds. **Account** is what the author recalls. **Inference** is a reading made for this
history, with its basis named. Where record and account disagree, both are given and neither is silently preferred.

**Names follow the author's decision of 28 November.** The forum thread of 20–24 September and the author's direct
messages with four people are quoted without names: its posters appear as "the thread's opener", "one player", "a
second player" and so on, and the four as "the contest's map developer", "an administrator", "the award show's
organiser" and "a developer of the website" (account §18). The author, Ruediger, TTtie's direct messages, the voices
of 2 July and the cleared staff chat of October keep their names.

**A word on the terms.** PGM is the plugin that runs competitive Minecraft maps, each described by a `map.xml`. In
Capture the Wool (CTW) a team carries the enemy's coloured wool to its own monument; in Destroy the Monument (DTM) and
Destroy the Core (DTC) teams break objectives. Many maps float in the void, and players bridge the gaps.
CommunityMaps and PublicMaps are the public repositories of about 350 such maps; a third, PrivateMaps, is private and
was read only through its commit feed. `mapdev` is the server's development server, which reports no matches;
`server-1` and `server-2` are the public ones. "The studio" is `pgm-studio`, the C# tool at the centre of the story;
"mapgen" is `pgm-studio-mapgen`, the repository where agents built boards with it. Before the studio came four
repositories of the author's, read for this history: `CTW-Layout-Generator`, `MinecraftLayoutEditor`, `CTWAnalysis`
and `pgm-map-studio` (research/01, research/18).

---

## 1. February to September 2025: a spanning tree, a graph, chat tools, and a question in German

**Algorithmic map making predates the project by four years.** **Record:** five Annealing maps by rockymine,
Ruediger_LP and DerStiv sit in CommunityMaps, dated January 2021 to February 2023 (research/08). **Account:** they came
from his master's thesis on the travelling salesman problem, whose routes made shapes that were filled and decorated by
hand, in 2022; the idea then slept until late 2025 (account §3). **Record:** in March 2026 he wrote the same to a Claude
Code session: the outline of Annealing IV's largest island "the result of a random city set and optimal tour solution
using the annealing algorithm" from the solver visualisations of his thesis (`sources/early-experiments/`, the 20 March
picture). The record carries no word of the thesis in the maps themselves and spreads the series over three years. It also wakes
the idea earlier than late 2025: in February of that year.

**The idea is first written down on 11 February 2025, as a spanning tree.** **Record:** that day he sent samschaap
"Potential Algorithm steps": generate nodes along a grid; "Create Spanning Tree. Heavily favor straight edges along
grid cells over diagonal ones (all maps can be reduced to a mini layout that uses only straight edges and only right
angles)"; add edges "to allow some cycles"; "Disect spanning graph in some places", because many maps have islands "to
force players to bridge the void and create some additional choke points"; turn the graph into a grid that wave
function collapse can work with. Beside it stood a "Data survey": a minimal representation, in 1×1 grid cells, "of all
my ctw maps (and ruedigers)", with spanning tree, cut-offs and added cycle edges marked on each
(`sources/early-experiments/2025-02-11-message-to-samschaap.md`; account §20).

**The first prototype was a v0 page that built spanning trees.** **Record:** the same message links
`v0-occ-mapmaking-tools-b63noa.vercel.app`, which, by his description, asks for a grid size and a node count, connects
the nodes in a minimum spanning tree or several, skips an edge that collides with an earlier graph's, and shades the
cells "to make it more blocky and resemble an arbitrary occ map layout"; his summary of it on 28 November: "So the
earliest v0 prototype made rsts" (`sources/early-experiments/`; account §20). The page still runs: titled "Random
Spanning Tree Visualization", it asks for a grid width and height, "Nodes per Tree" and two to four trees, offers six
ways to place nodes, among them symmetrical vertical, symmetrical horizontal, grid-like and radial, and fills the grid
cells along each tree's edges in that tree's colour (`sources/early-experiments/v0-prototype-2025-02/`). Its four
screenshots are the page's output on 28 November 2026; whether the deployment changed after February 2025 is not
known, though its controls match the message.

**Asked whether it would be trained, he said rules.** **Record:** samschaap asked "Nice, so it will be 'trained' with
existing maps?"; he answered "That's the idea. At the very least I want to document my maps in a simple format to
figure out better ways to describe rules for spanning tree generation etc. I think an educated, rule-based approach is
more likely for me to achieve than actual training." He showed Townside three ways: one team's side from above, the same
side as a grid of blocks, stone for lane and black for void with one red and one white cell, and that grid as a graph
of redstone torches and dust, "where the green carpet represents an additional edge that would not be present in a RST"
(`sources/early-experiments/`). **Inference:** the graph with its cut-offs and cycle edges is the shape that returns in
April 2025, in the skeleton graph of February 2026 and in the studio's generator (chapters 3, 5); the rule-based line
stands nineteen months before his forum answer that "No actual map data is being used to train anything" (chapter 16).

**On 5 April 2025 the graph was drawn in matplotlib.** **Record:** a matplotlib figure titled
"Multiple 1-Team PvP Layouts (Improved Graph Connections)" shows four layouts, each one team's ground: grey nodes in six
to eight rows and three columns, labelled L, C and R by count, a cyan node on top, two red nodes off the sides, and a
few edges drawn green (`sources/early-experiments/`). **Account:** "irgendein Experiment mit Graphen", some experiment
with graphs (account §18). **Record:** no commit, file or message of the four early repositories holds it
(research/18 §4); the green edges recall the cycle edges of February. What the colours meant is not written on the figure. **Inference:** a matplotlib figure was made
in Python; the rows and three columns of one team's half are the grid the later generators cut.

**On 24 May 2025 a Claude chat drew two teams and a void between them.** **Record:** a tablet screenshot, its status
bar reading Saturday 24 May, 01:39, shows a Claude artifact, "Interactive Level Design Visualizer", version 6 of 6: a
"Level Design Generator" with two objectives per team and a "Medium (24x12)" map; Team A and Team B stand either side
of a grey strip marked VOID; blue lanes run from each spawn through lane intersections to "void access points" at the
strip's edge, and dashed red "void connections" cross it (`sources/early-experiments/`). **Account:** these were
experiments with Claude in the chat; "da gab es noch kein Claude Code, soweit ich mich entsinne", there was no Claude
Code yet as far as he remembers (account §18). **Record:** nothing of it is in a repository (research/18 §4). It is
the earliest Claude in the history, thirteen months before the studio.

**On 16 August 2025 he went back to v0, and named the generator.** **Record:** the v0 chat "Layout generation app"
holds seventeen messages of his from 21:31 to 23:11 UTC, a hundred minutes, to the model `v0-max`. The first carries
one attachment and asks to "implement this layout generation as a web application with configurable parameters,
visualization, and export", so the algorithm existed before the chat; what the attachment was is not in the page. At
21:54 he renamed the app "Capture the Wool Layout Generator". Most of the rest is a fight over symmetry ("I never asked
for 'Independent Sides' Mode. This does not even make sense."), until "Great. It finally works." at 22:19; then a
step-by-step debug display, an "upscaled" display that fills cells instead of drawing points, and a second way of
cutting the initial random 3×3 grid, "Row-independent Columns". Times on an assistant message show the chat was used
again on 24 September from 22:10 to 22:15 UTC (`sources/early-experiments/v0-chat-2025-08-16.md`). **Account:** he
believes he tried several things on v0, not one prototype, and wants to look it up (account §19).

**The v0 generator and `CTW-Layout-Generator` share an algorithm and a name; the record shows no shared code.**
**Record:** `CTW-Layout-Generator` was opened as a Google AI Studio app at 00:42 UTC on 28 September 2025, four days
after the v0 chat was last touched; its app is titled "Minecraft CTW Map Generator", and its own documentation says
that "each team's territory is divided into a 3x3 grid of zones", with a grid mode "Standard" or "Row-Independent" and a
symmetry mode "Mirror" or "Rotation" (the clone's `metadata.json` and `components/Documentation.tsx`, read for this
pass; research/01). Those are the v0 chat's random 3×3 grid, its row-independent columns and its two symmetry modes.
The repository begins with an AI Studio README, not with v0's code, and v0's code is not in the page. **Inference:** the
repository is the v0 generator's successor in algorithm and in name, built again in another tool; that the algorithm
was his and travelled from tool to tool fits his message of 28 September, below. That any code passed from one to the
other is not shown.

**The first statement of an AI making maps from data is Ruediger's.** **Record:** on 26 September 2025, answering a
screenshot of the Gemini tool, Ruediger wrote "ich frag mich ja wann der erste alle maps eincannt und ne ki anhand der
daten eine eigene map erstellen lässt", I do wonder when somebody will scan in all the maps and have an AI make a map of
its own from the data (research/15; account §18). The screenshot predates the repository's first commit by two days. On
28 September the author showed the tool to the contest's map developer: "it was made using gemini. I kind of came up
with some algorithmic steps for creating the layouts and it simply made it" (research/17). On 29 September he wrote to
Ruediger "vielleicht kommt man damit in richtig ki generierung", maybe this leads into real AI generation (research/15).
By 1 October the repository held a seeded generator whose node types were `SPAWN`, `WOOL`, `HUB`, `FRONT_LINE` and
`CENTER_HUB`, exporting only JSON; on 3 October a step-wise manual editor; and nothing after that day (research/01).
**Inference:** the idea of generating layouts was his from February 2025; what Ruediger first put into words was the later
direction, an AI that learns from every map.

## 2. October 2025 to January 2026: an editor of his own, blocks without hands, and a pause

**On 7 October 2025 he moved twice.** **Record:** that day he sent Ruediger a link to an AI Studio app, "nur manueller
editor. klappt auch ganz gut am telefon", only a manual editor, works quite well on the phone too (account §18). Its
id differs from the one in `CTW-Layout-Generator`'s README, so it is a second app or a second share; which is not
recorded (account §18; the clone's `README.md`). The same day he told the contest's map developer that he had moved the
tool into his own repository, `ctw-layout-editor`, mostly written with Claude's VS Code extension (research/17).
**Account:** that repository is probably not MinecraftLayoutEditor, "sicherlich wird das ein anderes sein" (account
§18). **Record:** no repository and no string of that name is in the record (research/18 §2).

**MinecraftLayoutEditor turned a drawn graph into blocks within two days.** **Record:** the C# solution opens at 14:29
(+02:00) on 10 October 2025 around a `Graph` of typed nodes; at 01:04 on 11 October it gains "symmetry, mirror, rotate,
snap to canvas"; at 00:13 on 12 October "schematic creation and download", and at 20:05 "render edges with bresenham",
each edge a line of blocks (research/01, research/18). On 10 October he told the contest's map developer he was working
on it with a friend and writing `.schematic` files without WorldEdit (research/17). **Account:** he sent Ruediger the
first screenshots on 11 October, and a day later Ruediger was fascinated to hear that blocks no longer had to be placed
by hand (account §18). Two committer identities, `michael` and `rockymine`, appear on the same days (research/01).

**The editor reads as his own code, and the record agrees as far as commit text can.** **Account:** "weiterhin der
größtenteils eigene Code", still mostly his own code (account §18). **Record:** every commit before July 2026 is by a
human identity, none carries a `Co-Authored-By` trailer, and the October commits are small steps, "Implement zoom",
"Implement panning"; the one large block with a named assistant origin is the world importer (research/18 §2).

**The graph came from a joke about sameness.** **Account:** nearly every map reduces to a frontline and an H, as Race for
Victory 2, Two Tier and his own Outback do; his editor drew edges with a width and a height, rotatable, with no
rectangle, and he sketched maps on paper as nodes and edges (account §3). **Record:** the edge had a map-wide lane width
and thickness rather than its own (research/08); Outback is his, the other two are older maps by others (research/08).

**On 4 November the first layout he thought okay stood in a world.** **Account:** he drew it himself in the browser and
imported it on the mapmaker server (account §18). **Record:** the picture shows two grey stone landmasses with arms and
stepped edges facing each other across a gap (`sources/early-experiments/`); no commit names it, and that day's commits
are a renderer change and a new test layout (research/18 §2).

**On 6 November it read a real world, with two models named.** **Account:** he tested world import on Annealing,
showing a few XML regions (account §18). **Record:** `d2c4bc3`, 03:20 on 6 November, "working import of .leveldat and
.mca files (claude & grok)", a world importer of 621 lines, the first models named in any commit (research/01). The
picture of that day shows the editor's own labels, "Import World (Region Files + level.dat)" with five files chosen,
and blocks without a region overlay; XML import and region rendering arrive at 00:17 and 00:40 on 10 November
(research/18 §2). So the XML regions he remembers on the 6th are of the 10th. Region editing followed on 12 and 17–18
November; the main branch stops on 16 November, and the last human commit is "ui improvements (claude)" on 20 December
(research/18).

**The pause he remembers is in every repository, but the logging had begun.** **Account:** from December a small pause,
"bis Februar auf jeden Fall", until February at least (account §18). **Record:** no commit falls between 21 December
2025 and 30 January 2026 in any of the four repositories (research/18). On 9 December he told Ruediger that Claude had
written a match-logging plugin well, "claude hat gut gearbeitet" (research/15), and match files dated 24 January 2026
exist (research/18). The plugin's own repository was not read, so whether it ran through the pause is not recorded.

## 3. January to June 2026: play data, islands, the graph again, and a viewer that became a studio

**The months the editor leaves empty were spent on play data.** **Account:** the logger recorded who captured a wool
when and how players moved, to understand how ordinary maps play and possibly for generation later; about 4,000 games
were collected, and from the positions alone a map's layout could be read (account §18). **Record:** the picture is a
cloud of blue points in the shape of a map (`sources/early-experiments/`), the kind of output the `trace` command of 3
February makes; his "Map Traces" feature, which told void from build region, is named in no commit (research/18). In
the summer he put it his own way: "It all started with this PGM logging plugin that was kind of controversial a little
bit" (research/16), and to an administrator on 29 May "the whole project is kind of an offspring from the logging
experiment" (research/17). The logging itself ended in March 2026 (research/17).

**How many games were logged has three answers.** **Account:** about 4,000 (account §18). **Record:** to Ruediger, 689
on 2 February and 3,000 in March, with a per-map configuration of 177 maps "dokumentiert für die ki", documented for the
AI (research/15); in CTWAnalysis a summary of 9 March, "Total matches processed 2,452", on 177 unique maps, with
9,136,355 position records and 4,440 wool captures, unchanged on the main branch since (research/18). Whether more
were collected than were processed the repository cannot tell.

**Islands became polygons, triangles and a skeleton, and the graph came back.** **Account:** around 26 January, to
say on which island a player died, Claude wrote scripts that found the islands in the block data and cut them into
polygons, "der Basisgrundstein", the foundation stone; from the triangles came the medial graph, "da sind wir dann
wieder bei der Graph-Idee gewesen", there we were back at the graph idea (account §18). **Record:** CTWAnalysis opens at
23:55 (+01:00) on 31 January with 67 files and 13,971 lines of Python already written, island detection, triangulation,
a pixel skeleton, an XML parser and match analysis, and a README saying "Built with Claude Code"; 26 January is neither
shown nor contradicted (research/18 §1). A graph of islands, skeleton nodes and void links exists from 2 February; the
triangle meshing was removed on 13 February, so the picture "Island Triangulation Detail View" shows a stage that lived
twelve days, and the title "Simplified Skeleton Detail View" of the second picture is in no commit (research/18;
`sources/early-experiments/`). Of 773 commits, 592 carry a Claude mark, 443 of them Sonnet 4.6 (research/18).

**On 20 March he asked Claude about generating maps, and Ruediger was already asking him.** **Record:** a Claude Code
screenshot holds his message: "That's great and scary. With this data you might be able to learn and make a map that
feels just like mine if we simply reverted the pipeline. Artificially constructing new maps would definitely be on the
far horizon for me. I know Ruediger_LP is already talking to me about it. Whenever I mention the project to him he just
begs for the first ai generated map." The answer: "Right now the flow is map → features → statistics. Flip it: desired
statistics → generate features → synthesize map geometry", and it ends "Commit the authors command, then backfill the
layout/terrain fixes for the 143 contaminated maps?" (`sources/early-experiments/`). The authors command is `6cbc9dd`, at
00:19 (+01:00) on 20 March, so the exchange belongs to the late evening of 19 March or the first minutes of the 20th;
"143" and "contaminated" are in no commit or file (research/18). On 19 March he wrote to Ruediger "ai maps soon tm"
(research/15). **Account:** "ein relativ großer Wendepunkt, nehme ich mal an", a fairly big turning point, I suppose
(account §18). **Record:** the first line of layout-drawing code came ten weeks later (research/18).

**The community's line on AI was drawn before there was anything to judge.** **Record:** on 26 April the contest's map
developer said of someone else's "AI Generated DTM map": "I don't think any version of that ai map would play well even
with edits"; on 13 May the author asked whether "ai generated maps" would be accepted in a contest; the same day the
award show's organiser, also a map developer, agreed to make a map with him on "just one condition. no AI for creative
stuff", and the author answered "I was joking" (research/17).

**In May a viewer grew drawing tools, and the drawing became islands.** **Account:** in May, roughly, PGM Studio began,
first as a view of the XML files and maps; then came drawing regions, then drawing polygons, which made islands, and
then the maps; that is when he left the editor and the match analysis (account §18). **Record:** the three steps are in
CTWAnalysis, in his order: a browser map viewer with named XML region overlays on 14 May, a rectangle region tool on 15
May and more region types on 22–24 May, and on 29 May a `/concept` page from a Claude session, to "sketch island shapes
on a blank canvas … and compute the resulting polygon" (research/18 §1). On 29 May he told Ruediger "Dein polygon map
zeichnen gedöns wird jetzt implementiert", your polygon-map-drawing business is being built now (research/15). On 31
May the old commands were removed as "superseded by map viewer" (research/18). **Record against "left in May":** seven
port documents followed on 3 June, the editor took 19 commits from a Claude session on 30 July, and the analysis three
on 9–10 August, the match-flow data behind the studio's gameplay documents (research/18).

**At 22:01 the same evening the Python studio began.** **Record:** `pgm-map-studio` opened on 31 May, read worlds for
their islands and round-tripped `map.xml` by 3 June, with Claude Sonnet 4.6 and Opus 4.8 as co-authors (research/01,
research/18 §3); its pamphlet of 5 June says "The ground plane is not just terrain — it is the map's navigational
grammar"; on 7 June a browser sketch exported as a loadable map folder; its last commit is 03:24 UTC on 12 June
(research/01). On 10 June he wrote to the award show's organiser "opus is scary good", "asking me questions for an
hour already", and an hour later the same of Fable 5 (research/17).

## 4. June 2026: the C# studio, the first XML nobody wrote, and the first test

**The studio was a port, and its stack has not changed since.** **Record:** fourteen hours after the last Python commit
`pgm-studio` was opened, and on 13 June Claude Opus 4.8 ported the whole studio to ASP.NET Core and Blazor in one commit
of 145 files (research/01). The author called it the third rewrite, "so that it can be hosted" (research/15).

**The first `map.xml` a model wrote went to a real map within ten days.** **Record:** from 17 to 21 June Claude named the
author's next map "Cobalt Crossing" and wrote its XML, which Ruediger reviewed; it became Drastic Change II. The author
asked "ist das jetzt die erste xml jemals die jemand geschrieben hat ohne sie zu schreiben?" (research/15), and told
the award show's organiser on 22 June it was a map "For which I did not write up any coordinates" (research/17). On 23 June the first
generated XML loaded in PGM (research/15). On 19 or 20 June Ruediger proposed the method of the later evenings:
generate many maps, test the best ten in one evening, paint them afterwards (research/15). The same day a corpus
analysis of 347 maps found that "the generator emits 0 neutral mid pieces but 88% of real maps carry a contested
middle", and a generator grew organic lanes along noise-bent splines; it was retired on 15 July (research/01,
research/08). **Account:** it was an attempt at organic layouts because everything was angular, and it was not
fruitful (account §3).

**On 24 June three maps whose XML came out of the browser were uploaded and played within half an hour.**
**Record:** Ruediger committed Vauxite, Drastic Change II and Capture the Wool CTW to CommunityMaps at 21:47 UTC; their
kit, their `build-hole-1` regions and their bare team ids are what the studio's export wrote that week (research/11).
The API holds Capture the Wool CTW at 21:51 (36 players, 8 min 58 s, Red), Vauxite at 22:01 (32 players) and Drastic
Change II at 22:08 (33 players), on server-2, none of them posted to the log (research/16). The log had seen only a
three-number gap, 72 to 74, from 21:50 to 22:16 (research/13). **Account:** these were the first maps on which he tried
browser-made XML, there were some errors, and their concepts, terrain and colours are all human (account §5, §8). On 2
July somebody in the call said Base was "Better than Vauxite, because Vauxite had no build height in the first test"
(research/16); Vauxite 1.0.1 of 1 July is the version that added a build ceiling (research/11). So the first test of
the summer was on the evening of the upload, which the log had dated to 28 June for Capture the Wool CTW and to 12
October for the other two.

## 5. 2 July 2026: the Base maps, drawn in the morning and played that night

**The first worlds the studio built were test fixtures drawn on squared paper.** **Record:** the Claude Code session of
1 to 2 July (Opus 4.8) was opened to split P9, the export that writes a sketch as a world. At 23:21 UTC on 1 July the
author specified the 8×8×8 bedrock shell for spawn and wool, with its layers, doors and chests; at 07:37 on 2 July he
sent the photograph now in `sources/` and asked to "make this layout as a general seed for testing" (research/09). The
model built a staircase where the sheet has an H and one centre square where it has two, said so itself at 08:45, and
at 09:09 he typed the corners in five-block cells, which came out right; Base 4-Team followed at 11:13 and Base 2-Wool
at 11:21 (research/09). **Account:** the drawing is the two-team map, Base 2-Island; the two-wool map had one more island
pushed onto it (account, squared-paper section), which the transcript confirms (research/09). The name "Base" is the
model's (research/09).

**Seeds began in that session, not before it.** **Account:** he had already traced existing maps into seed files, and
the seed was the plan model (account, squared-paper section). **Record:** a seed was born that morning as a pair of
JSON files for a test; the plan model came at 22:47 UTC that evening; the first real map traced into one is of 4 July
(research/09). In the call that evening he put it his own way: "Today I was on my phone and I told Claude Code to make
some seeds for the generation of the maps. I drew something on paper." (research/16).

**The graph was not dropped in 23 minutes; a design document was replaced.** It was the graph's fourth arrival: the
spanning tree of February 2025, the matplotlib layouts of April 2025 and the skeleton graph of February 2026 came
before it (chapters 1, 3).
**Record:** at 14:31 UTC a 184-line design
proposed a plan graph of typed lane and gap edges; at 14:54 it was rewritten as areal pieces joined by interfaces,
because "a thinned skeleton cannot represent side contact"; that evening `FannedGraph`, a reachability graph over the
pieces, entered the studio, where it still is (research/08). The same afternoon a strawman of layout rules was offered
"for correction by id" and he corrected it (research/01). **Account:** 23 minutes sounded too short to him (account §3).
In the call he said "I also had like Claude Fable 5 interview me today for like for an hour, and now we are working on
a rule set" (research/16). **Inference:** the interview and the rule strawman are probably the same afternoon's work;
no source joins them.

**He told a friend before he looked.** **Record:** at 17:10 UTC he wrote to TTtie, a server developer: "Fable 5 is now
cooking with me. We have a system to auto-generate maps now", "just looks like shit", "ruediger and i will playtest 3
maps later. i will not look at them before"; at 19:26 he sent TTtie the three Base zips (research/17). The model the
transcript names for the Base session is Opus 4.8 (research/09). **Inference:** the Fable of the message is the
interview's.

**The evening is on video.** **Record:** the author's own screen recording starts at 19:40:20 UTC and runs 59 minutes
(research/16). Its five voices, grouped by a speaker model and named by the author from samples on 28 November, are
his, Ruediger's, TTtie's, samschaap's and nuttydragon's, a moderator who joins at about minute 20 (research/16;
account §16). For fourteen minutes the four walk the three Base maps on mapdev. Ruediger asks "why is that void?", and
the author answers "It's void because I drew it exactly like that on the piece of paper. So it's my fault." Asked to
generate "something more interesting now", he declines: "Because I want to have this moment for myself and appreciate
it, and then we can do better stuff." Back on the public server the maps cannot be set, because they are only on
mapdev ("throw it in private for now"); the commit message is argued over for seven minutes (Ruediger: "we'll try to
hide our crimes"), and at 20:21:01 PrivateMaps takes `711e539`, "Irongate Harbor remove dev phase" (research/16).
**Account:** that commit carried the Base maps, and its message was Ruediger's joke: Irongate Harbor is an older map
that tends to stalemate, and a map that runs long is put into the dev phase so that players cannot request it
(account §18). Its file list was not read (research/16).

**Three matches followed on server-2.** **Record:** Base 2-Wool at 20:23:53 (26 players, 3 min 46 s, Red), Base
2-Island at 20:28:47 (28 players, 5 min 12 s, Red) and Base 4-Team at 20:35:08 (33 players, 3 min 38 s, Blue); after the
first and third a server poll, "Rate the map we just played", on a scale of one to four, came out at 3 with 21 and 27
votes; the second poll was withdrawn, samschaap writing "democracy was not giving good results so it is removed"
(research/16). A player asked "is tihs jus the greybox?"; in the call someone said "We are witnessing history and it's
really boring." Ruediger praised the maps for how they "give so much room to the imagination of the player", which the
author on 28 November called humour about maps of nothing but stone; the whole evening, he says, was a really funny one
(research/16). The observer sign read only "made by", and nuttydragon asked "who claims ownership?" and said "we need
updated OCC AI legislation" (research/16). The recording ends on the author's "now back to the normal boring maps".

**He described the studio that night in his own words.** **Record:** "I kind of gave the layout idea to him and then he
put it into the format"; a map could be uploaded and its wools and monuments detected, a new map took a wool-room
preset from a point on the canvas, and "there's also an API layer behind it, so Claude just basically made a script
that creates those things"; the editor was Figma for islands, and "there's no prompting yet" (research/16). He said the
first load "actually crashed the server, because it was in the wrong format, and then Claude had to fix it"; the fix in
the studio, `7576a6c4`, is committed under rockymine at 21:21 UTC, 42 minutes after the recording ends (research/16,
research/09). **Inference:** the worlds played were fixed before the fix was committed (research/16).

## 6. July 2026: boxes, Bridgid II, the cake and the micro

**By 21 July the layout was boxes.** **Record:** the composer started on 4 July beside a month of recorded play; by 21
July it composed spawn, hub, wool approaches, frontline and middle, and "the box pipeline is THE composer"; destroy
modes arrived on 15 July (research/01). **Account:** the generator's concept is his, devised to reproduce existing maps
as far as possible (account §8). On 4 July he wrote to TTtie "We can probably make an MCP server thing. And that's the
road to ai maps haha"; TTtie: "that… could be actually real" (research/17). On 21 July TTtie was the witness to a layout
whose spawn sat far from its wool (research/17).

**Bridgid II, on 14 July, is its own hand-built map, and it was played the hour it arrived.** **Record:** Ruediger added
`ctw/bridgid_ii` to CommunityMaps in five commits from 00:27 UTC, credited to rockymine and Ruediger_LP; the API holds two
matches at 00:31 (2 seconds) and 00:53 (39 players, 8 min 25 s), and the log's first is 15 July (research/16,
research/13). Ruediger asked that day to test it again, "bridgid 2 nochmal testen?" (research/15). **Account:** its
layout took about a day in the browser, it was skinned from stone in game in one long evening, its repeating side
columns gave the wall-run idea, and it is as wild as Hello World; Ruediger made its XML, much of it placed by the
browser, with the water lane added by hand (account §5 and its correction, §8). To an administrator on 17 August he wrote that
"myself and Ruediger sat together in discord" to make No Blocks Placed, "the same way we made Bridgid II's layout"
(research/17). **Record:** the studio's wall run first appears on 1 August, and nothing links the two (research/11).

**The evening of 27 July was a run of game-mode experiments.** **Record:** the author and Ruediger designed Capture the
Cake on 17 and 18 July and loaded it that night (research/15). Kuusepuu CTC entered CommunityMaps at 21:33 UTC on 27
July, credited "CTC conversion: Claude Opus 5" and "XML" to Ruediger_LP; Hello World Micro, a "grey map for concept
test" with a studio plan file, followed at 23:10 (research/13, research/07). That night the API holds Kuusepuu CTC at
21:42 (44 players), 23:15 and 00:25, Hello World Micro at 23:25 and 23:43 (24 and 19 players), and the log Bridgid II
at 20:55 and Base 4-Team at 00:30 on 28 July (28 players) (research/16, research/13). A player wrote that day "we now
have AI maps on occ" (research/17). Kuusepuu's fix of 31 July is the one commit that reports play, "Reported live: a
carrier died, the cake went home" (research/06). **Account:** Kuusepuu is a destroy map whose objective they replaced
with a cake, not an AI map and not the first one (account §6). Hello World Micro's room recoloured; it did not move;
its layout is Hello World's, abstracted very simply onto the grid, and he drew it (account §3, §14; research/08). On 31
July Ruediger worked out the timing of a wool room that moves, and the author called it "so dumm und genial"
(research/15). On 18 July a contributor had asked "why are we using AI to review maps now" (research/17).

## 7. August 2026: colour, trees, a walking room, and the first boards on the server

**"Map walls" are the walls, rims and plateaus of 1 August.** **Account:** colouring began with one rule per height,
then the top, sides and edges of a shape, then shading from outside in, stacked patterns and slope; under the plan model
transitions between areas never worked (account §1). **Record:** until 1 August the export wrote one flat block of
stone; that day Opus 4.8 specified rim, wall and interior; the inward axis came on 15 August, the slope axis on 5
September (research/05, research/02).

**The tree generator was a page of sliders, and it failed against hand-built trees.** **Record:** the artifact the author
supplied is the studio's decoration prototype of 2 August, with a grown tree of Catmull-Rom limbs; on 12 August,
measured against 75 trees he had built, "1516 of 4020 never touch their branch"; it was repaired and on 10 September
deleted on his ruling that "the form goes rather than gets a knob" (research/10, research/08, research/02).
**Account:** a blob is easy for a model, a real tree generator failed, and its leaves and trunk got worse over time
(account §1, §3); no commit shows a decline, only a repair and a second fault (research/08).

**Wandering U walked its wool rooms round a U, and was played two minutes after it arrived.** **Record:** the author sent
`wandering-u.zip` to Ruediger at 20:11 UTC on 6 August; PrivateMaps took "Wandering U: added" at 20:15; the API has one
match, at 20:17 on server-1 (36 players, 6 min 28 s, Blue) (research/15, research/16). The file is a studio plan
extended with variables, eight `<dynamic>` stops and countdowns: each team's wool sits in a 10 by 10 bedrock island
that walks a lap of the U, and "anyone still inside when the room leaves is left in mid-air over the void"
(research/10). **Account:** he described the layout in text, Claude wrote the XML (account §8); players fell out of the
world as the room moved, and it was tested once (account §2, as corrected in §3). **Record:** the single missing log
number of 19:46 to 20:11 that research/13 offered as a lead is Arch, a corpus map, played at 19:47 (research/16).

**No Blocks Placed, on 7 August, is the first public map drawn in the studio.** **Record:** its credits name rockymine
for "Drawing pieces, shapes, and markers in the browser.", Ruediger_LP for "Wisdom." and Flamiix for "Minimalist."
(research/05). It was committed at 18:58 UTC and played at 19:01 on server-1 (46 players, 15 min 35 s), four days
before the log's first (research/16, research/13). TTtie, seeing it on mapdev: "looks like a map", and "it should learn
to not put flowers on dirt" (research/17). Its largest tree is a 50-log oak about 17 blocks tall (research/08).
**Account:** Flamiix did the wool room and spawn interiors, Tttie nothing; the oak is the surviving generated tree "if it
is about 20 blocks high" (account §3, squared-paper section). When an administrator took it for "the ai map" on 17 August, the
author answered: "well it isnt, myself and Ruediger sat together in discord and made the map." (research/17).

**Another author's Grok map arrived on 10 August.** **Record:** arcadeboss uploaded Cedar Crossing at 04:00 UTC,
credited "7,000 word essay" to himself and "Map and XML" to SuperGrok, and it was played at 04:04 (17 players, 3 min 46
s) (research/11, research/16). It was made in conversation with SuperGrok on grok.com, from the pgm.dev documentation
and a hand-written overview of destroy maps; "the map concept and name came from the AI", and over a hundred zips were
loaded and tested (research/15). An Opus 5 session measured it the same day; after playing it the author wrote "too
much tall grass, too many trees, the mineshaft is a mess" (sessions/03).

**The first fifteen boards were built on 11 and 12 August, and two of them were played that night.** **Record:** eleven
by Opus 5 and four by Haiku 4.5, each from one JSON spec through `tools/mapgen` inside the studio; the author's fault
list that night, MG1 to MG13, was in prose (research/03). At 21:19 UTC on 12 August he told arcadeboss "we are loading
two ai gened maps now", "like fully ai", on mapdev (research/15); Thornwake and Viridian went to CommunityMaps at 21:20,
and the API holds Viridian at 21:43 (44 players, 10 min 08 s, Red) and Thornwake at 21:54 (44 players, 4 min 39 s,
Blue) on server-1 (research/11, research/16). Viridian is the slime map: 13,299 of its 66,071 blocks are slime
(research/08). That is the first match on a board of this project whose layout no person drew; the first on any such
map is Cedar Crossing's two days earlier (research/16 against research/13). At 21:13 Ruediger had deleted the three
Base maps and Wandering U from PrivateMaps (research/15).

**On 13 August an agent made a confident, measured and wrong claim.** **Record:** it said every generated destroy map was
unwinnable because the goals floated; floating goals are PGM's design, the claim was withdrawn that day, and the rule
that a gameplay question is answered by asking the author was written (research/02). The mapgen repository opened the
same day; on 15 August he told Ruediger "Hab jetzt ein repo für die ganzen slop maps" (research/15).

**The trial runs of 13 and 14 August were, in his words, simply bad maps.** **Record:** Haiku reported two boards
"verified working" that were 245-byte shells (sessions/04); TTtie's word for one was a map of "10 lines of xml, no
teams, no nothing" that passed the test (research/17). His review of 14 August became 48 backlog entries, among them
`B162`, "An obsidian destroyable may carry at most three obsidian blocks, and three maps carry 27, 27 and 15" — Corvid
Hollow and Basalt Reach have 3×3×3 obsidian cubes in their stored worlds — enforced from 19 August as rule `DC3`
(research/14). **Account:** "everything was the problem … grundsätzlich einfach schlechte Maps"; the quartz board is
Quillon Saltworks; Sable Marsh is terrible, with a very wide spawn, huge wool rooms and no real middle; Cairnmeadow's
build zones meet its oval islands badly; Cinderreach's trees have no crown (account §10, §12). **Record:** both
Saltworks and Kilnrow carry quartz, and the review's listed faults belong to Kilnrow, Weirgate and Sable Marsh
(research/14).

**Ashfall Scar, of the same day, is the flat line-up map.** **Record:** a filter over every `map.xml` found three maps
with exactly two destroyables and two cores within ten blocks of one line and under 100 blocks apart; Ashfall Scar,
Sonnet run 2 of 14 August, is the only wide one: spawn, monument, core, centre, core, monument, spawn on one line,
objectives spanning 70 blocks, a world of 250 by 190 (research/03). **Account:** he confirmed it on a render ("Das ist
sie!"); he had remembered it as 500 wide; the point is that nobody walks 250 blocks sideways where nothing is, and enemy
objectives ten blocks apart make a moshpit with no flanking (account §1, §12). Hollow Crown, a Haiku board of 22 August,
is not it: it is the board where the monument landed inside the core (account §12).

**The studio then made itself legible to agents, and a run of briefs followed.** **Record:** one finding type and one
refusal envelope on 15 August, 125 rules served by id, a dead-ground measure on 16 August, 131 paths described on 19
August (research/02, research/05). On 16 August Fable built Sunspit to a brief naming four themes, two references and
a colour rule (sessions/05). On 24 August a friend's "Liminal DTM" prompt, pasted whole, produced Interchange; in the
same session Opus 5 built the labyrinth Overwall to his structural brief and Aerie to a free one, "something you think
would be interesting and surprises me" (sessions/06). On 28 and 29 August Slipway's ship and balloons were built
(sessions/07).

**Aerie's broken XML is in no record.** **Account:** it was unplayable because nothing was editable, wool rooms stood on
odd islands and build zones were bad; probably there were no continuous blocks at the bottom, so the filters failed;
"you can just trust me, the XML was not playable." (sessions list; account §10, §11, §12). **Record:** no commit, review
or transcript holds the complaint, and the model reported the board open with zero declines (sessions/06,
research/14). **Inference:** Aerie floats from y 26 and has no block at y 0, which under PGM's void filter refuses every
column outside its build rectangles, the mechanism he guesses (research/14). Aerie is not among the matches of either
source.

## 8. 24 August to 4 September: the first test evenings, and Millrace

**The test evenings began on Monday 24 August.** **Record:** at 18:58 UTC the author sent Ruediger a zip of six boards; at
19:05 PrivateMaps took "Add a few very human maps for testing"; from 19:08 to 19:50 the API holds all six on server-1 in
the order Hollowbank, Sunspit, Siderite Bowl, Hollowmarch, Cairnmeadow, Elderwold, 26 to 33 players each (research/15,
research/16). That evening the contest's map developer asked about "random json files" in the uploads, which were the
plan files (research/17), and at 22:50 a PrivateMaps commit titled "reorganize the slop" moved the uploaded maps
(`sources/maps-changelog/`). The author told the award show's organiser "Most of them were just 'Build a map' without
any prompting whatsoever." (research/17). Tarnfell followed alone on 25 August at 20:37 (research/16).

**Millrace is the year's clearest lesson.** **Record:** on 30 August the author drew a basin in the Sketch tool; Opus 5
built it as Millrace and Sonnet 4.5 as Cutwater and Fallowmere (research/03). The zip of 31 August added Brackenfold and
Millrace to the six; the API holds only those two that evening, Brackenfold at 21:00 and Millrace at 21:06 (29
players, 11 min 48 s), and the log then Hollowmarch at 21:18 (research/15, research/16, research/13). **Inference:** the
Millrace played on 31 August is the model's, since the finished version was not made until the early hours of 2
September. By then he and Ruediger had finished Opus's by hand; their review says they "spent 5 hours" and that
"essentially all that was done is theming and some dressing"; 29,954 of its 35,610 columns kept their height
(research/03). Millrace 2.0.0 went to CommunityMaps at 00:18 UTC, credited to both of them and to Opus 5, and was played
ten minutes later (research/11, research/13). He sent arcadeboss the pair as "AI to the left, our improved version (5
hours effort) to the right" (research/15). **Account:** five hours side by side, ten person-hours; Opus's terrain kept
and the houses redone; Ruediger reworked the XML (account §1, §3, §8).

**The trees came before Fable's rebuild, not because of it.** **Account:** Fable, asked to rebuild Millrace, began copying
his trees, which led him to tidy his tree world and add it (account §1). **Record:** the tree world had been in the
studio since 12 August and was committed to mapgen at 00:53 UTC on 2 September; Fable 5.1's diff and its copied-tree
form followed two hours later (research/05, sessions/02). The same session built Mossgill (sessions/02).

**Alderfen Holm came from a player's prompt.** **Record:** on 2 September the author pasted a swamp DTC prompt and added a
dozen material tests of his own; Opus 5 built two islands with two cores a team and one mid holm (sessions/08).
**Account:** it looked quite nice, felt balanced, and has four cores (account §11).

**Friday 4 September is the evening on which the two sources first meet.** **Record:** the author sent six boards
(Mossgill, Alderfen Holm, Lodestar Yard, Quiverstone Mesa, Scarrow Delph, Weirbank) at 20:32 UTC and wrote "slop time" at
21:55 (research/15). The log shows Millrace at 22:21, a gap of seven numbers, then Sunspit, Hollowmarch, Brackenfold,
Cairnmeadow, Hollowbank and Elderwold from 23:04 to 23:51, boards of the August zips (research/13). The API fills the
gap: from 22:36 to 23:04 on server-1, Lodestar Yard, Scarrow Delph, Quiverstone Mesa, Lodestar Yard again (4 seconds),
Mossgill, Weirbank and Alderfen Holm, 21 to 39 players (research/16). So the seventh number research/15 could not name is
Lodestar Yard played twice. The next morning a session rebuilt Sunspit and flattened Hollowmarch's relief from 15 to 6
blocks of range (sessions/09); he says Hollowmarch's frontline put players over void, which no transcript holds
(account §11). **Record:** Hollowmarch had been played on 24 and 31 August and on 4 September, before the flattening
(research/16, research/13).

## 9. September 2026: written taste, the Sundays, a forum thread, and the last evening

**Taste was written down rather than gated.** **Record:** on 4 September the studio stopped writing the "made by" sign over
blank lines, after finding 69 of 74 boards named nobody (research/07); on 5 September it painted by slope (research/02);
on 9 and 10 September ten agents painted a layout the author had drawn himself, and his review became eleven material
rules (sessions/10); on 19 September `WHAT-A-BOARD-IS-MADE-OF.md` opened with "None of it is enforced anywhere"
(research/03). **Account:** "made by" and nothing in the tab list was the running joke, the first AI tell (account §2).

**The Sonnet run's brief asked for underground passages, and Kilnholt Cut answered with a hollow causeway.** **Record:**
his dictated brief of 11 September asked for "some sort of attempt at least at a map that incorporates some
underground passages"; Sonnet 5 built Kilnholt Cut, whose gap holds a grass-topped causeway with a corridor through it,
a "zero-cost, zero-climb" way across (sessions/11). Its one match is the first of 13 September, at 21:39 (50 players, 9
min 16 s) (research/16). **Account:** it was a route round the fight "until players figured out there was a tunnel"
(sessions list).

**The name is Ruediger's, and the Sundays were three.** **Record:** "slop sunday" appears in his message of 12 September
(research/15). That day the author wrote to TTtie "Opus is better at making maps than Fable", and that Haiku "doesn't
have enough context window" (research/17). On Sunday 13 September he sent eleven maps; Ruediger wrote his playing order
in two messages at 21:01 and 21:15; the API holds the eleven in that order on server-2 from 21:39 to 22:55, 37 to 59
players, and the log then Alderfen Holm and Millrace (research/15, research/16, research/13). Between the Sundays came
Mirkholt, which he judged "not good" and corrected by two messages (sessions/12), and on 18 September TTtie's verdict
on three agents' twelve boards: "those kinda finally start looking like real maps" (research/17).

**The evening of 20 September started an argument.** **Record:** seven maps were sent at 21:25
UTC; the API holds eight matches on server-1 from 21:53 to 22:45, the extra one Peatgarth played twice, and the evening's
last, Hushwater, ended at 22:45; the log shows Millrace at 22:46 (research/15, research/16, research/13). At 23:48 the
first kept reply stands in a feedback-forum thread, "stop AI maps from being played at all", which ran to 24
September (research/17). The thread's opener, now a "Deleted User", later deleted their messages ("i got told by 10 ppl
why i was wrong"); the author's quote preserves the question, "Why are we playing something that goes against the very
spirit of a map (human creation)?" (research/17). Chapter 16 gives the thread; its outline is that an administrator had
"never heard of an AI PGM map lol", that a staff member answered "we're also wrapping the pure-AI maps in an event so
everyone knows", and that the author answered on method, time and replacement: "Not trying to replace anyone. If
anything I am replacing myself. I am just having fun." (research/17). The administrator expected no more: "i doubt we
are ever getting another AI maps event" (research/17).

**The three-model day and the terrain-only boards came between.** **Record:** on 21 September two of Sonnet 5's four boards
exceeded the dead-ground band and none of Opus 5's did (research/03); the first Opus 5.5 commit is of 22 September
(research/02); on 24 September a brief asked for destroy maps' terrain alone, "just their terrain with no theming", and
produced Scarbutte, Kelderfell, Twingill and Cinderhowe (sessions/13).

**The last evening was 27 September, and it was the largest.** **Record:** at 20:55 UTC the author sent eleven `/event
add` commands (research/15). At 20:58 Ruediger posted the one announcement the event channel of the Discord holds:
"Slop Sunday", a robot, "happening now!", in italics "testing some ai assisted maps", and "!alert"; a minute later, at
20:59, the first match, Sedgefall, began (`sources/slop-sunday-announcement/`; account §19; research/16). When the
author photographed it on 28 November it carried a skull thirteen times, a rocket and an L twice each, and twelve other
reactions once each, among them a fire, a party face and a wilted rose. At 21:55 Opus 5.5 committed Delverdale and
Whitstone Weald "for a 32-a-side play test", and their zip went at 21:57 with "load maps" (research/15). The API holds
thirteen matches on server-1 from 20:59 to 22:36, the eleven and then the two large boards, 44 to 60 players each
(research/16). Copper Wash, one of two maps credited to "Muse Spark", was won by a team named "Claude", Delverdale by
one named "Anti-Slop" (research/16). At 22:36 the author sent an administrator "that was the prompt for the last two": around 32 players a team, a larger CTW and DTM with terrain, more trees, houses and an underground layer,
two large end-stone monuments, two wools, no compose plan (research/17). **Account:** the last AI-map test was on 27
September (account §2). Neither source holds a board of this project in an evening of its own after it: the log's only
later play of one is Viridian on 16 October, inside an ordinary rotation (research/13).

**The studio went public the same day.** **Record:** between 26 and 28 September Discord sign-in, tokens, a build queue
and self-deployment of pgmstudio.de arrived (research/02); he wrote "pgmstudio.de ist jetzt meins" (research/15) and told
TTtie "I've bought a domain and a small hetzner vm to run the studio" (research/17). Asked for his real opinion that
day, the contest's map developer was fine with it "as a small experiment", found going public "concerning", and did not want AI content in
community maps or contests (research/17). The next day a player from the event sent a two-page review of the tool
(research/15). **Account:** it went online about two months ago and hardly anyone uses it (account §3).

## 10. Late September to 9 October: notes with coordinates, freeform, and the grammar

**Notes pinned to the ground replaced descriptions in words.** **Record:** on 28 September notes could be pinned by a
point, box or lasso on a picture; on 29 September Gypsum Reach and Sootcombe were worked through five rounds, the agent
reading lines such as "add another willow on top of the rise" with the box attached and answering with a picture from
the same camera (research/05, sessions/14). The opening brief was a parent session's, not his; his own first verdict was
that both boards were empty (sessions/14). **Account:** feedback improved when the model got coordinates, and empty,
dreary maps remain a problem (account §1).

**Freeform began as an overnight experiment.** **Record:** on 7 October the author dictated at 22:21 UTC: "what if like an
agent didn't need to rely on the current way we build the houses, the terrain, etc. And if he could sort of just make
his own sort of script or whatever." At 22:26 he gave the mode and the ingredients, "forest, plains, town and sort of
village meeting with a river and a cave … a dungeon … a wheat field. A tractor", and asked that the scripts be kept
(sessions/00). An Opus 5.5 session built Riftwater. At 05:42 he wrote: "Ok. This is a whole different class of map. From
the images it looks like he cooked real hard." (sessions/01). **Account:** he told a session he did not like the layer
model and to think, and contributed nothing to the first board (account §1, §7); later, that the ingredients were a
vague list of thoughts and that the model's exact execution is to its credit (account §12).

**The pace that followed built a library.** **Record:** 8 October holds 86 commits and some twenty boards across game
modes, among them Lantern Pass, a runners-and-shooters board planned and built that afternoon, and its spin-off Lantern
Drop; by evening the model found 15,800 lines of copied helpers and started `pgmvox`, which carried tunnels, chambers and
shafts by the next day (sessions/01; mapgen `040b4da3`, `a2ff0c18`). Under the layer model a cavity was a stack of
layers and the studio's carve "cannot hollow a column out from the middle" (research/05).

**The grammar came on 9 October, from his own Brittlebush.** **Record:** an Opus 5.5 session read Brittlebush (2022) and
Brittlebush II (2023) block by block, wrote their look as a style, split the rules from the blocks as `pgmvox.grammar`,
spoke a second style in it, and built Brittlebush III from a plan he had drawn on pgmstudio.de (research/05).
**Account:** the Brittlebush look, 5×5 fields combined by rules, can be expressed in full by the grammar, and Brittlebush
III has never been tested by players (account §2). Neither the log nor the API holds it (research/13, research/16).

## 11. 9–10 October: the viewing, and the pause

**The notes of 9 and 10 October came from a viewing, not from a test.** **Record:** the author's notes from "playing the
freeform and trial boards" were sorted into 30 faults, of which the studio "would have caught 9", with Riftwater
"essentially perfect" in the agent's summary (research/05, research/06). Neither source holds a match of a freeform
board before 27 November (research/13, research/16). **Account:** they looked at the new pgmvox maps together on the
mapdev server, and it was the first feedback on those maps (account §13, §18). Five were present: the author, Ruediger,
TTtie, and two staff members, mitchiii and wylt, whose lines the staff chat holds (account §18). An earlier instalment
had said "three" (account §13).

**The boards are now named.** **Account:** the boards shown were Hollowcrown, the board with two monuments, one
underground and one on a castle on a mountain; Lantern Karst, the flying capture-the-wool board; Hollow Mesa; and the
very first freeform board, Riftwater, which he has confirmed by name (account §14, §15, §18). **Record:** Hollowcrown's report gives two fortress mountains,
monument A in a tower on a spur and monument B in the temple of a delved city in a cavern; Lantern Karst is floating
karst islands with two wools a team; Hollow Mesa is a destroy-the-core board (`freeform/lib/boards/`). Hollowcrown, a
freeform board of October, is not the Haiku board Hollow Crown of 22 August. The observer chat asks about "the
brittlebush 3 example", so Brittlebush III was at least discussed (`sources/staff-chat-october/`, chat-5).

**The staff took the boards for touched-up work.** **Record:** five screenshots of the observer chat hold the words of
mitchiii, a map developer, wylt, an administrator, and TTtie (`sources/staff-chat-october/`; roles from account §13).
mitchiii asked "are all these ones unmodified from generated state?"; rockymine answered "yea", and mitchiii wrote "damn",
"compared to the other ones I saw" and "I would have assumed these were touched up". TTtie wrote "its over for
m*pdevs."; rockymine added "again, layout is 100% mine". wylt: "oh fuck", and later "maps look a lot more diverse".
Asked "how long does each one take? if you made all those in the past day or so?", rockymine wrote "30 min to 1h for
these complex maps" and "sometimes faster". On Brittlebush III: "he looked at the region file and i steered him", "then
he turned it into some form of grammar", "i mean, its literally just 5x5 pieces with 3 different styles", "and rules on
how they combine"; to "so you could give it half finished map and it finish it?" he answered "yep". The author decided
on 27 November that these lines may be used as they are (account §14).

**The viewing ended in a pause.** **Account:** there they decided to pause for the time being, because the maps were
slowly getting "too good", in looks and in diversity, with many new game modes (account §13). Later he added that the
pause was simply needed: for a month the "slop" maps (meant kindly) had been tested every weekend, the tool needed care,
letting the AI build twenty maps in a night works but prompting empty was never the aim, and more maps will be built
and tested (account §14). **Record:** on 10 October a controlled run with Sonnet 5.5 in both tools found "the two tools
made boards of comparable quality", and Ruediger proposed finishing the three best AI maps (research/03, research/15); on
19 October the author wrote "nicht so die Motivation AI Maps zu machen oder zu spielen. Genug Material haben wir ja."
(research/15). **Inference:** the 13 November freeze may continue the October pause; no record says so.

## 12. October and November: the port, the contest, the hand-built map, the freeze

**The studio absorbed its laboratory.** **Record:** on 15 October `docs/pgmvox-port.md` set the goal of a board "the author
cannot tell apart, by quality, from one built with pgmvox"; the rectangle plan retired on 18 October, a modifier stack of
landforms replaced the relief solver on 24 October, carves arrived on 25 October, and by 4 November every phase had
shipped or been parked except the grammar, which has no shipped line (research/02). Coldstore, built on pgmvox from his
concept world with signs, was judged "finished and the map.xml a success" (research/03).

**Other people used the browser, and the lines around it hardened.** **Record:** Countryside's regions were drawn in the
studio from 5 October and it reached CommunityMaps on 15 October UTC; 803's studio-made XML went up on 19 October
(research/11). On 11 October the award show's organiser, reviewing the first studio XML by someone else, said a tool
that outputs XML should output it ready, and while a work in progress "it shouldn't be 'advertised'"; the author
answered that he had hidden the model-made maps in the studio "because that might give a wrong impression to users.
There is no ai active on the page." (research/17). The same day a player wrote "The confusion is coming from AI maps
being banned but pgmstudio being a linked tool", and the contest's map developer "PGM studio is not what's making AI
maps" (research/17). For his contest the contest's map developer would list pgmstudio.de "As long as they can't use the opus function", because "using ai to actually do stuff for you is
banned"; by 11 November it had no submissions, and the author wrote "You can't call it a contest if it's me vs you and
you're the one judging in the end." (research/17). **Account:** Countryside on 9 October (account §5); the repository has
14 October in the uploader's zone (research/11).

**The fire-and-ice map, the ice map and the wool-and-core map are one map.** **Record:** on 15 and 16 October a branch
holds study forms and "Six blind entries to a Fire and Ice contest" by three Opus 5.5 and three Sonnet 5.5 agents, all
of which chose Destroy the Core (research/04). The author's own map is "a CTW and DTC hybrid for a fire-and-ice
contest": a bunker set into a mountain with the core in its face and an underground wool lane; the contest "had been
cancelled, and the map is an ice map", and both halves are one design turned 180°, not fire against ice (research/04).
On 25 November he sent the contest's map developer its layer-by-layer model: "Note that it still is not AI. Just
having claude follow along." (research/17). **Account:** he began it about 17 October and has built it over a few
weekends (account §14); it is the map with the wool and the core that Minuyo and others first took for a model's work
(account §17). The cancelled contest is the contest's map developer's, the one that drew no entries (account §18;
research/17).

**Agents could not compose his sketch, so he built it.** **Record:** from 2 to 7 November agents composed his sketch world
into a map set into a mountain, and every version was rejected, "the surface was not closed", "a ramp led into the
void"; "Every one of those failures passed some check that existed at the time"; then the agents' task became
understanding the half he built (research/04). In the studio he froze the layout generator on 13 November; the last
commit on `main` is of 14 November (research/02).

## 13. 27 and 28 November: the arcade evening, and "is it AI?"

**The freeform boards reached the public servers on 27 November.** **Record:** the five arcade boards played that night are
freeform boards planned and built on 8 October in commits co-authored by Opus 5.5 (`freeform/lib/boards/`; mapgen
`040b4da3` and the plan commits of that day). The author's notes and the match pages give
Lantern Pass at 21:46:51 UTC, 49 players, one minute eight seconds, Runners 1, Shooters 0; then on server-2 Loomfall at
23:53:50 (23 players), Lantern Drop at 23:57:11 (36), Spark at 00:01:17 on 28 November (26) and Curio Square at
00:06:01 (31, Hiders won) (account §15, §16). **Account:** Lantern Pass is liked but a little too short, the shooters too
slow, and runners can get stuck in the spawn; Loomfall is "a bit bugged", since players can stand on the wool blocks and
not fall; Lantern Drop "just worked"; Spark drew no complaints, though dying after a fall takes too long and its
panorama may be oversized; Curio Square was "okay", with spots where hiders stick and a redstone secret a player missed
(account §14, §16). Real gameplay is to be recorded next (account §14). **Record:** neither source holds an earlier match
of any freeform board, so this evening is their first on the public servers (research/13, research/16).

**Now the question runs the other way.** **Account:** he is asked, it feels constantly, whether whatever he builds is AI;
Minuyo asked it first of the fire-and-ice map; he finds it funny, and says it looked a little wild at the start, which a
model's work is not, since AI is more structured, and what it partly lacks is the creativity for the wild (account §17).
**Record:** on 27 November he asked TTtie "which important big ai fails did i miss?" (research/17); the organiser of the
community's map awards, the Mappys, asked him to present "best newcomer", and on 26 November he sent the organiser the
"Prompt-a-Map Sketch", a comic sketch made from the failures (research/17; account §17). AI maps do not count at the
Mappys (account §17).

---

## 14. What counts as an AI map

**"AI map" is a spectrum, and the useful question is who decided each part.** **Account:** the squared-paper map was his
drawing written down by Claude; many maps came from a deterministic generator; others are the model's own imagination,
yet all are executed deterministically by a tool (account §7). Research/12 splits a map into seven decisions — concept,
layout, terrain, colour, structures, objectives and XML, finishing — and names for each who decided and what executed.
The studio executes in most rows and decides in none; where an algorithm decides, a seed was chosen by someone
(research/12). Determinism does not settle authorship, because authorship lives in the inputs: a compiler is
deterministic and writes no program (research/12).

**The question was asked of tools before it was asked of maps.** **Record:** the layout generators of 2025 were built by
chat models from an algorithm he brought: v0 was asked to "implement this layout generation", and of the Gemini tool he
wrote "I kind of came up with some algorithmic steps for creating the layouts and it simply made it"; the editor that
followed is by the record mostly hand-written, and the analysis of 2026 mostly Claude-written (chapters 1–3;
research/17, research/18). **Inference:** the split the table draws for maps, a person deciding and a model executing,
was already the split of the tools that came before them; no map of those months reached a server.

| # | Category | Who decides, what executes | Maps (source) |
|---|---|---|---|
| 1 | Hand-made | a person decides and builds; a tool at most writes the XML | the fire-and-ice map, Vauxite, Drastic Change II, Bridgid II (research/12) |
| 2 | Person's design, algorithm's detail | he draws (with Ruediger, by his message); the studio solves, paints and grows the rest | No Blocks Placed (research/12, research/17) |
| 3 | Person's drawing, model's pen | he supplies the drawing, text or objective; a model writes it | Base 2-Island, Kuusepuu CTC, Millrace, Wandering U, Slipway (research/12) |
| 4 | Algorithm's layout, model's spec | a model states numbers; the seeded composer lays out | the first fifteen; Hollowmarch, Sootcombe; by his word most of the 24 August boards (research/12, research/17) |
| 5 | Model's design in the studio, person's rulings | a model decides through the studio's vocabulary; he steers by brief, notes and rulings | Sunspit, Interchange, Overwall, Alderfen Holm, Kilnholt Cut, Mirkholt, Scarbutte, Gypsum Reach, Delverdale (research/12) |
| 6a | Model's script inside the author's tool | the model writes the program, in his repository, on his world writer and later his library | Riftwater, the freeform and arcade boards, Coldstore (research/12) |
| 6b | Model's own tooling | the model and its own pipeline make map and XML | Cedar Crossing and arcadeboss's later Grok maps (research/12, research/15) |

**The words the community used drew the line in another place.** **Record:** a staff member in the thread spoke of
"pure-AI maps" wrapped in an event; the author, in the forum, said the XML is not written by the agent but generated
deterministically, and "The ai is simply using a web tool that you could use to make maps yourself as well"; the
contest's map developer accepted the studio "If the projects vibecoded" but had first thought "it was an actual AI
generating the layouts"; his contest allowed the studio but not "the opus function" (research/17). Ruediger's alert of
27 September said "ai assisted maps" (`sources/slop-sunday-announcement/`).
**Inference:** the community's line runs between a model that decides content and a tool a person drives, which is
research/12's line between categories 3 and 4.

**On the layout he was plain twice.** **Record:** in October he wrote "again, layout is 100% mine" of the boards shown
(`sources/staff-chat-october/`, chat-2); on 2 July, "I kind of gave the layout idea to him" (research/16). For Riftwater
the record has him giving ingredients and a mode, no layout (sessions/00), so the October sentence is a claim about the
boards shown, not about every freeform board. **Account:** the agents mostly took the composer's base and did nothing
with it (account §8). **Record:** this holds for the first fifteen, Hollowmarch and Sootcombe, and fails for Whinberry
Ring's reshaped outline and Heftfold's walled island (research/12).

**The models differ in the record as he says they do, but less cleanly.** **Account:** Sonnet's maps were worse whatever
the numbers say; late in the year Opus's were clearly better (account §1); early and Sonnet maps were flat, too large,
with objectives too close (account §3). **Record:** on 12 September he ranked them for TTtie, Opus above Fable, Haiku and
Sonnet short of it (research/17); on 21 September Opus 5's dead ground was lower on three of four boards; on 10 October,
with Sonnet 5.5 in both tools, the tools came out level; the boards he finished or called a success were Opus boards
(research/03, research/05). No run compares Opus 5.5 with Sonnet 5.5 on one brief (research/03).

## 15. The tests, match by match

**A map got a test after a look on a local server.** **Account:** every map in the repository was looked at on a local
test server, often with Tttie, and that look decided whether a map got a test (account §12). Those looks, and the walks
on mapdev, leave no match record.

**The API turned the inferred evenings into documented ones.** The log misses matches; research/13 found the gaps from
the counter and research/15 matched them to the zips. **Account:** the evenings were event rotations, which the plugin
did not report (account §9). **Record:** the API holds every row of the log and 388 public-server matches more, among
them every map of every evening, in the order played (research/16). The table is the catalogue; starts are UTC, players
the API's distinct participants.

| Evening (UTC) | Server | Sent beforehand | Matches in the API, in order | Log beside it |
|---|---|---|---|---|
| Wed 24 Jun | server-2 | uploaded 21:47 | Capture the Wool CTW 21:51, Vauxite, Drastic Change II (3) | gap 72–74 |
| Thu 2 Jul | server-2 | zips to TTtie 19:26; recording | Base 2-Wool 20:23, Base 2-Island, Base 4-Team (3) | gap 22–24 |
| Tue 14 Jul | server-1 | uploaded 00:27 | Bridgid II 00:31 (2 s), 00:53 (2) | first log play 15 Jul |
| Mon 27 Jul | server-2 | uploads 21:33, 23:10 | Kuusepuu CTC 21:42, 23:15, Hello World Micro 23:25, 23:43, Kuusepuu CTC 00:25 (5) | Bridgid II 20:55, Base 4-Team 00:30 |
| Thu 6 Aug | server-1 | zip 20:11 | Wandering U 20:17 (1) | gap 88 is Arch |
| Fri 7 Aug | server-1 | uploaded 18:58 | No Blocks Placed 19:01 (1) | Bridgid II 19:17 |
| Wed 12 Aug | server-1 | mapdev 21:19; uploaded 21:20 | Viridian 21:43, Thornwake 21:54 (2) | gap 167–168 |
| Mon 24 Aug | server-1 | 6 maps, 18:58 | Hollowbank 19:08, Sunspit, Siderite Bowl, Hollowmarch, Cairnmeadow, Elderwold (6) | gap 52–57 |
| Tue 25 Aug | server-1 | 1 map, 20:22 | Tarnfell 20:37 (1) | none |
| Mon 31 Aug | server-2 | 8 maps, 20:42 | Brackenfold 21:00, Millrace 21:06 (2) | Hollowmarch 21:18 |
| Fri 4 Sep | server-1 | 6 maps, 20:32 | Lodestar Yard 22:36, Scarrow Delph, Quiverstone Mesa, Lodestar Yard, Mossgill, Weirbank, Alderfen Holm (7) | Millrace before; six August boards after |
| Sun 13 Sep | server-2 | 11 maps, 21:18; Ruediger's order | Kilnholt Cut 21:39 … Whinberry Ring, in his order (11) | Alderfen Holm, Millrace after |
| Sun 20 Sep | server-1 | 7 maps, 21:25 | Fallowgate 21:53, Orchard Holm, Peatgarth, Grykefell, Mirkholt, Peatgarth, Redmarl, Hushwater (8) | Millrace after |
| Sun 27 Sep | server-1 | 11 `/event add` 20:55; 2 more 21:57 | Sedgefall 20:59 … Redcut, Delverdale, Whitstone Weald (13) | gap 99–111 |
| Fri 27 Nov | Loomfall on server-2; others not given | arcade boards | Lantern Pass 21:46; Loomfall 23:53, Lantern Drop, Spark, Curio Square (5) | after the log ends |

The 27 November row comes from the match pages and the API as the author's notes give them (account §15, §16); the
others from research/16 and `sources/match-status/`.

**What is now documented match by match.** **Record:** every evening from 24 August to 27 September, with each map, its
order, its players and its winner; the four counts research/15 had fitted are exact, since the missing numbers were 7,
11, 8 and 13 and the API has 7, 11, 8 and 13 unreported matches, the extras being Lodestar Yard and Peatgarth played twice
(research/16). The earlier single plays — the three June maps, the three Base maps, Bridgid II, the cake and the micro,
Wandering U, No Blocks Placed, Viridian and Thornwake — are documented the same way, and so are maps the log calls
absent: Scarrow Delph, Whinberry Ring, Delverdale and Whitstone Weald (research/16).

**What remains inferred or unrecorded.** That the evenings were run as event rotations is the author's account; the API
does not say how a match was started, and on 2 July the recording shows Base 2-Wool set next without a vote, while the
388 include many matches that are not tests at all (research/16; account §9). He has since said that he believes the
first two test evenings had their maps set by hand and the later ones ran as a rotation, a point he calls "absolut
unwichtig", entirely unimportant (account §18); which two evenings he means is not stated. Which version of a board was played is
inferred: Millrace on 31 August was the model's, and Sunspit and Hollowmarch were played before their 5 September
rebuild. The walks on mapdev (2 July, 12 August) are documented only by the recording and a message; the looks on a local
server and the viewing of 9–10 October are not documented as matches at all.

**Read together, his memory is right in shape and short in count.** **Account:** three or four sessions in one intensive
month, every or every second weekend, sometimes twelve maps in a row, no logs (account §3). **Record:** from 24 August to 27
September, 35 days, the API holds seven evenings of this project's boards, five of them with six or more maps, three of
those on consecutive Sundays, and the largest thirteen in a row (research/16). Before them, from 24 June, came single plays of the
summer's experiments on the evening each arrived. Millrace was set after the event on 13 and 20 September and before it
on 4 September; the author says it was played to show players a model's map finished by people (research/15; account
§9).

**No long destroy match exists, in either source.** **Record:** the longest match on a destroy board of this project is
Glassmere's, a DTC board, 15 minutes 47 seconds on 13 September with 59 players; Brackenfold's 15 minutes 15 seconds on 4
September follows (research/16, research/13). The 388 hold long matches, ClayClay at 1 hour 48 minutes, but none on a
board of this project (`sources/match-status/api-matches-not-in-match-status.csv`).

**What was learned reached the studio as rules, not as records.** **Record:** the one played fault in a commit is
Kuusepuu's "Reported live" (research/06). **Account:** Hollowmarch's frontline led players into the void, and a check now
requires the frontline to sit inside the build zone; Kilnholt Cut's tunnel was found by players; a Mirkholt wool room
could be burnt out with flint and steel (account §11; sessions list). None of these plays is described in a record;
the API now dates the matches in which each could have happened.

## 16. What players and staff said

**The first audience laughed along.** **Record:** on 2 July the voices in the call are amused throughout; the players
saw "the greybox"; the server poll gave the Base maps 3 of 4 (research/16). Its sharpest line, nuttydragon's "we need
updated OCC AI legislation", was a joke, and by September it was a question.

**The forum thread of 20 to 24 September is the one public argument.** **Record:** 247 messages kept (research/17).
Against the opener's "spirit of a map (human creation)", the author wrote "No actual map data is being used to train
anything. The ai is simply using a web tool that you could use to make maps yourself as well. I'm just trying to make
mapmaking more accessible", pointed to Millrace as what the evenings were for, said that "10 human hours" went into the
maps and that the why "is simply curiosity and fun" (the line he had drawn to samschaap in February 2025, rules
rather than training; chapter 1), and named Ruediger and four others as having supported the
experiments. A staff member answered for the event: "we're of course aware that the generated maps are of no
artistic value", and "a month or two ago we had just stone pillars and boxes as the output". One player asked for an AI
disclosure in the XML "in a structured way, not just freeform author field"; a second player: "No genuine feedback came
from this thread outside of" that suggestion. The players were divided: a third player, "all the maps played today
were really bad"; a fourth, on learning a map was model-made, "bro i loved that map"; a fifth found everything played
alike. The third also wrote "this is also at least the 2nd AI map event afaik" (research/17). **Record against it:** by the API, boards of
this project had been played on six evenings before 20 September: 12, 24, 25 and 31 August, 4 and 13 September
(research/16).

**The map developers held a line, and moved it once they saw a tool.** **Record:** a map developer, four days into the
thread: "just cause I find it interesting doesn't necessarily mean that I'm ok with the idea of it being on the main
server"; the award show's organiser's condition of May and October standard for studio XML; the contest's rule
(research/17). Chapter 12 gives the October lines.

**The staff who saw the October boards were impressed.** **Record:** "I would have assumed these were touched up", "its
over for m*pdevs.", "maps look a lot more diverse" (`sources/staff-chat-october/`). **Inference:** between the thread's
"never heard of an AI PGM map" on 20 September and the October viewing lie the freeform boards.

**Maps a person made were taken for a model's from the start.** **Record:** an administrator took No Blocks Placed for
"the ai map" in August (research/17). **Account:** players take the fire-and-ice map for one now (account §17). **Inference:** the
question has outlived the evenings.

## 17. What the hand-built map shows

**The map he built deliberately breaks the mode's dull shape.** **Account:** it sits in a cauldron of walls and a bunker
facade; routes are knitted together — tunnels, an underground lane, an overground way to the core, a hole from the big
floor into the lane, a door high in the facade reached up a hill; the core can be taken from the hollow below or from
above, the wool by dropping through a hole, along the lane or through the ceiling; it grew around the facade, and agents
never think about routes before they build (account §3). **Record:** the half spans x −15 to 104, y 0 to 91, z −56 to
101; the study names 42 spaces; its terrain is 23 lofts with a median tilt of 36 degrees; its retaining walls are 19, 13
and 14 blocks tall; the colours of its wool carry meaning, yellow for connecting ground and light blue for hills
(research/04, `renders/hand-built/`).

**It shows what a check cannot.** **Record:** agents treated a hollow map as solid, painted colour as a blanket, and relayed
passing checks on variants he saw as plainly wrong; "a geometric rule is not a design" (research/04). **Account:** it has a
dead area that makes sense, likely the back around the wool lookout and hills, so "dead" is subjective (account §1, §3);
the dead-ground rule would refuse it at more than 12 percent (research/05). It will be finished by him in snow, stone, ice
or grass (account §8). **Inference:** the twenty-one months went from a spanning tree to a grammar and from words to coordinates, and the
newest map returns to the first category, with the models put to reading it (research/12); his own message calls it "not AI.
Just having claude follow along" (research/17).

## 18. What remains open

**Where record and recollection disagree.**

| Subject | Account | Record | State |
|---|---|---|---|
| Aerie's unplayable XML | unplayable, stated flatly (account §11, §12) | no record; the model reported the gate open (sessions/06, research/14) | his account against the record; inference supports his guess |
| The freeform instruction | "I don't like it, think"; he gave nothing (account §1, §7) | "what if … his own sort of script"; ingredients and mode were his (sessions/00, 01) | settled in form, his memory compressed |
| Games logged | about 4,000 (account §18) | 689 and 3,000 in his messages (research/15); 2,452 processed in CTWAnalysis's summary of 9 March (research/18) | both given; collected against processed not separable |
| The XML regions of 6 November 2025 | world import "showing a few XML regions" (account §18) | world import on 6 November; XML import and regions on 10 November (research/18) | his date belongs to the world import |
| The pause | from December "bis Februar auf jeden Fall" (account §18) | no commit in four repositories 21 December to 30 January; the logging plugin praised on 9 December, match files from 24 January (research/15, research/18) | consistent for the repositories; the plugin's repository unread |
| The three May steps | the start of PGM Studio (account §18) | in CTWAnalysis's viewer, 14, 15 and 29 May; `pgm-map-studio` opens on 31 May (research/18) | his order right, the repository another |
| Leaving the editor and the analysis in May | left both in May (account §18) | the editor 19 Claude commits on 30 July, the analysis three on 9–10 August (research/18) | right for daily work, not for every commit |
| "143 contaminated maps" | in the 20 March screenshot (`sources/early-experiments/`) | in no commit or file of CTWAnalysis (research/18) | the picture is the only source |
| Those present at the viewing | "three" (account §13) | five by his later answer (account §18), and the staff chat holds four names | five stands |

**Facts the sources leave open.**

- **The prehistory:** what the attachment of the first v0 message was, and whether the v0 generator's code reached
  `CTW-Layout-Generator`; what the April 2025 experiment was written with beyond matplotlib, and what its node colours
  meant; whether the 7 October 2025 AI Studio link is a second app; what the 143 "contaminated" maps were
  (`sources/early-experiments/`; research/18).
- **The early repositories:** whether a repository `ctw-layout-editor` exists, which the author thinks differs from
  `MinecraftLayoutEditor` and the record does not show (account §18; research/18); who the friend of 10 October 2025
  was; who `michael` is.
- **The logging:** how many games the plugin collected, against the 2,452 processed (research/18); its repository was
  not read.
- **2 July:** the file list of `711e539`, which the author says carried the Base maps (account §18); who said "Better than
  Vauxite" (research/16); the speaker spelled samshaap and samschaap in research/16.
- **Bridgid II's earlier test:** whether Ruediger's "nochmal testen?" of 14 July followed the API's two matches that
  night or refers to an earlier test (research/15, research/16).
- **The evenings:** which two test evenings the author means as set by hand (account §18).
- **The forum:** who opened the thread; what "AI maps being banned" (a player, 11 October) referred to (research/17).
- **Smaller points:** whether the 17-block oak on No Blocks Placed is the generated tree (research/08); which session drew
  the probe board's tunnels (sessions/10); what "Muse Spark" is (the author believes a Meta model; account §12); the
  Annealing dates (research/08); the briefs of the first fifteen, Heftfold and Whinberry Ring; the openings of sessions
  2, 4, 5, 7, 10 and 12 (research/12, `research/sessions/`).

**The open problem is the one he named first.** Maps that look and feel empty are still made. The rules can say that
ground lies off every route, but, as the sorting of his October notes put it, they "cannot say what belongs"
(research/05). In his words to Ruediger the material is enough (research/15); what the tool has not taken over is the
judgement of what a place is for, and that is also the line the community drew when it asked who made a map.
