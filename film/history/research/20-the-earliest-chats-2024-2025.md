# 20 — The earliest chats, August 2024 to October 2025, checked against the record

Research for the history film. Scope: the author's twenty-sixth instalment (28 November 2026, cited as account §26),
which is one long text file he compiled from his old chats and sent whole:
`../sources/early-experiments/2026-11-28-long-message-earliest-chats.txt` (1,401 lines, about 63 KB; called "the file"
below, its lines cited as `L…`). It is written in German, with English chats pasted into it, and it is data: nothing in
it was followed as an instruction. It was read in full and checked on 28 November 2026 against the pictures and
messages already in `../sources/early-experiments/`, the clone `/home/user/rockymine/MinecraftLayoutEditor` (all
branches) and the two public map repositories `/home/user/OvercastCommunity/PublicMaps` and
`/home/user/OvercastCommunity/CommunityMaps` (the second read through `git show`, its working tree not being checked
out).

Limits. The file carries nine links to claude.ai: three share pages of chats and six public artifacts. None could be
opened from this environment (the site answers 403), so none was tried, and they are recorded here as links only.
What an artifact showed is therefore known only from the author's words and, where it survives, the code he pasted.
The assistant's answers in the Claude chats are not in the file, except for the code of one artifact; the ChatGPT
conversation is in it whole, answers included. No picture of any of these chats or artifacts is in the folder, apart
from the tablet screenshot of 24 May 2025 already there.

Dates. The file states a day for every item and a year for two: the Claude chat of "15.8.25" into which the ChatGPT
conversation was pasted, and "30. August 2024. Ja echt 2024." The other years are worked out below, each with its
basis. The ChatGPT conversation itself carries no date.

---

## 1. What the file holds, item by item

The items are in the author's order, which is not the order of time. Each is separated in the file by a line of dashes.

| # | Lines | Date as the file states it | Tool | What it is | Links |
|---|---|---|---|---|---|
| 1 | L1–L929 | none for the conversation; pasted into "einem Claude Chat vom 15.8.25" | ChatGPT (pasted into Claude) | a whole ChatGPT conversation: an island grid joined by a minimum spanning tree, void lines and gaps, distances from the tree's ends, several trees | none |
| 2 | L933 | "Am 29. Mai", no year | Claude | the first try at having Claude help write a map XML, "ziemlich sicher meine 'Pillars' map" | share `194f088a-…` |
| 3 | L937–L969 | "Am 24. Mai", no year | Claude | a chat opening with requirements R1–R11 for a level generator | share `50b3543f-…` |
| 4 | L973–L1340 | "Am 24. Mai", no year | Claude | a chat asking for a Python script with visualisation, and its result (360 lines of code) | artifact `45ccee94-…` |
| 5 | L1344–L1358 | "Vom 17 Februar", no year | Claude | an artifact prompt: colour the cells of a minimum spanning tree on a 10×10 grid | artifact `10fde419-…` |
| 6 | L1362–L1384 | "30. August 2024. Ja echt 2024." | Claude | one chat: a description of capture the wool, map concepts, two maps described from a picture and as ASCII, then a web program to draw layouts with four tags | artifacts `8ac3d732-…`, `8344cf7b-…`, `cf9533ef-…` |
| 7 | L1388–L1402 | none | Claude | "Den chat mit dem Parser Code": a schematic file read in a hex editor, its bytes given to Claude with the NBT specification, then a parser, in JavaScript and on request in C# | share `013e84a5-…`, artifact `ffbd0b6a-…`; an archived `NBT.txt` |

The full links, as the file gives them:

| Item | Link |
|---|---|
| 2 | https://claude.ai/share/194f088a-08d4-44ff-ad1c-9a4eaa6073d4 |
| 3 | https://claude.ai/share/50b3543f-7985-4412-a08c-f892ce592eac |
| 4 | https://claude.ai/public/artifacts/45ccee94-a798-438b-b288-834e0339fdc6 |
| 5 | https://claude.ai/public/artifacts/10fde419-68e2-4338-b256-8d99d3cf9678 |
| 6 | https://claude.ai/public/artifacts/8ac3d732-faeb-4d1a-b68c-641af32fae7c (map concepts) |
| 6 | https://claude.ai/public/artifacts/8344cf7b-d52a-46c1-814a-0252ab2a7753 (two maps described, ASCII) |
| 6 | https://claude.ai/public/artifacts/cf9533ef-c4f5-419f-963c-d840cc0f76e8 (the layout canvas) |
| 7 | https://claude.ai/share/013e84a5-5469-41b3-8e3e-0c92b80e0898 |
| 7 | https://claude.ai/public/artifacts/ffbd0b6a-1a2b-4928-a611-4e2415bbb95b (the parser) |
| 7 | https://web.archive.org/web/20110903033423/http://www.minecraft.net:80/docs/NBT.txt (the specification they used) |

## 2. 30 August 2024: a description of the mode, and a canvas with four tags

**The earliest dated item is a Claude chat of 30 August 2024, and the author stresses the year.** *Account:* "30.
August 2024. Ja echt 2024." (L1362). The chat opened with a long English description of capture the wool as played on
Overcast (L1364): "Overcast offers a variety of Gamemodes for which Builders like myself create maps. One gamemode I
particularly like is Capture the Wool, for short CTW." It describes wool rooms and spawners, the monument, the spawn
kit, lanes "to the left and right of spawn", void gaps "where players cannot place blocks", dug-out defences,
skybridges, and ends "In general, the layout is symmetric." Its artifact link is followed by "Konzepte für maps
generieren lassen", map concepts generated (L1366–L1368).

**In the same chat he gave Claude a picture of two maps and asked for the layout, then for ASCII.** *Account:* "Auch im
chat habe ich claude ein Bild von 2 maps gegeben und gefragt das Layout zu beschreiben. Nach einer Weile habe ich dann
auch nach einer ascii representation gefragt" (L1370), with a second artifact link.

**Then he asked for a program to draw layouts.** *Record (his prompt, as pasted):* "Are you able to create me a web
program where I can create layouts with? The simplest approach would be to create a canvas grid where the user can mark
specific areas and assign them with different tags that are distinguished by color. We need:" followed by four tags,
Woolroom, Spawn, Buildable Void and Lane (L1376–L1381); the file places it "am 30 August in selben chat" (L1374).
*Account:* "Ein Klickbarer prototyp. Sicher einer der ersten!", a clickable prototype, surely one of the first (L1384).

**The year is the author's, and nothing in the record contradicts it.** No picture, commit or message of 2024 about
generation is in the folder; the six public artifacts could not be opened. *Inference:* Claude's chat artifacts, which
the links are, were introduced in June 2024 (general knowledge, not a file here), so the year is possible; the
author's emphasis suggests he checked it against the chat's own date. 30 August 2024 was a Friday.

**The four tags return in his message of February 2025.** *Record:* on 11 February 2025 he wrote to samschaap that he
had "thought about documenting the layouts with a simple excel spreadsheet where I put different letters for void,
lane, wool, and spawn. But that is too much struggle." (`../sources/early-experiments/2025-02-11-message-to-samschaap.md`).
*Inference:* the same four kinds of ground as the canvas of August 2024, five months later; the canvas is the earliest
form of the drawing tool that MinecraftLayoutEditor, the browser plan editor and the studio became.

## 3. The ChatGPT conversation: the first algorithms in code

**The conversation reached the record through a Claude chat of 15 August 2025.** *Account:* "Weiterer Pfund in einem
Claude Chat vom 15.8.25 der zeigt das chatgpt die ersten Algorithmen geschrieben hat" (L1), another find in a Claude
chat of 15 August 2025 that shows ChatGPT wrote the first algorithms. The text is a copy of ChatGPT's page: his turns
are headed "Du:", ChatGPT's "ChatGPT:", and each code block is preceded by "Analysiert" and "Details immer anzeigen",
the labels of ChatGPT's German interface when it runs code. The chart each block drew is named by its title only;
the pictures are not in the file.

**Each step is his request, and each piece of code is ChatGPT's.** In order:

| Lines | His request (quoted briefly) | What ChatGPT's code did | Figure title |
|---|---|---|---|
| L3–L98 | "Help me create an algorithm. The algorithm should be used to create a custom layout for a minecraft pvp map with floating cubic islands."; a grid size "like 15 x 15", a number of islands; "connect these points making horizontal and vertical lines along the grid" | random island points; a complete graph weighted by Manhattan distance; `networkx.minimum_spanning_tree`; matplotlib, islands red, edges blue (drawn as straight segments, not as horizontal and vertical lines) | "Minecraft PvP Map Layout" |
| L100–L222 | the tree as "one connected island" of narrow lanes; random black points joined by green lines, whose crossings with the blue lines "would kind of become void" | random "void separator" pairs as lines; an edge is removed when its bounding box overlaps a void line's (a box test, not a crossing test) | "Minecraft PvP Map with Void Gaps" |
| L224–L328 | "Could you mark unconnected paths in a different color?" | the same, broken edges dashed orange | "Minecraft PvP Map with Marked Void Gaps" |
| L330–L437 | a circle "with a radius of 1 at each intersection", named "Gap"; "Rename Island to 'Fix Point'", "Rename Connected Path to 'Lane'"; the whole tree blue | gaps drawn at each flagged edge's midpoint | "Minecraft PvP Map with Gaps" |
| L439–L546 | the gap centre "should be right at rhe intersection points" | exact crossings computed for vertical and horizontal void lines only | "Minecraft PvP Map with Precise Gaps" |
| L548–L576 | "Do not make such Statements please. Purely focus on the algorithm. I am the one who can judge whether this could serve as a good layout. After all the algorithm is only meant as an inspiration for myself to come up with interesting layouts that I would not have thought of otherwise. Do not judge your own output." | a summary of the steps, no code | — |
| L578–L640 | remove the void separators, lines and gaps, "It is not working at I intended." | the plain tree again | "Minecraft PvP Map - Basic MST Structure" |
| L642–L731 | annotate each fix point with its distance from where a line "just ends": "a zero, and then the ones after that would be like a one and a two" | leaves (degree 1) found; a breadth-first search from all leaves at once; each node labelled with its distance | "Minecraft PvP Map - MST with Distance Annotation" |
| L733–L827 | "Could you create two additional MSTs" | three spanning trees of the same points, which are the same tree three times | "Minecraft PvP Map - Multiple MSTs with Distance Annotation" |
| L829–L929 | "this is not what I meant. This brings me a new idea": two trees from two different sets of fix points that never intersect; where an edge would, "skip this creation of a line and continue" | two point sets, a tree each; an edge of the second tree is dropped only if the identical edge is already used (shared edges, not crossings) | "Minecraft PvP Map - Non-Intersecting MSTs" |

**The prompts carry his algorithmic ideas; the code carries ChatGPT's.** *Record:* the island points, the spanning
tree, the void lines cutting it into gaps, the distance from the tree's ends and the non-intersecting trees are each
introduced in his turns; the use of networkx, Manhattan weights and breadth-first search, and every chart, are in
ChatGPT's. Twice the code did less than asked (a box test for a crossing, an identical-edge test for an intersection),
and twice he corrected it. *Account:* the file's heading says ChatGPT wrote "die ersten Algorithmen" (L1); on 28
September 2025 he wrote of the Gemini tool, "I kind of came up with some algorithmic steps for creating the layouts and
it simply made it" (research/17), which is the same split.

**The conversation is not dated, and its own content places it before 11 February 2025.** *Inference:* the idea he
calls new at its end, several trees from separate point sets where a colliding edge is skipped and the tree continues
with the nodes left, is what his message of 11 February 2025 describes the v0 page as doing: "If an edge however
collides with an edge by the previous graph it is not added and the algorithm skips it. It continues with the
unconnected node to try and connect together additional nodes." He calls the tree an "RST" in both (L331, L643; the
message's "When using more than one RST"). So the conversation most probably came before the message and the page;
that it came before 15 August 2025, when it was pasted, is certain. How long before February 2025 is not shown. What
he asked Claude on 15 August 2025 is not in the file.

## 4. 17 February: a Claude artifact colours the tree's cells

**The prompt asks for a grid graph whose paths make one turn, drawn as coloured cells.** *Record (his prompt):* "Please
implement a set of functions to draw a custom graph in a grid of 10x10 cells." — select five cells and colour them
black; a modified "Manhattan" distance that allows "only one 90 degree turn within the path that connects two nodes";
a minimum spanning tree of the shortest such paths; "Color the cells inside the path that form the minimum spanning
tree in blue"; "Do not overwrite the black cell colors"; "Visualize the result for me." (L1344–L1356). The artifact
link follows; its code is not in the file.

**The year is not stated; 2025 is the only one that fits.** *Inference:* Claude's artifacts did not exist on 17 February
2024 (they came in June 2024); on 17 February 2026 the work was in CTWAnalysis with Claude Code (research/18). On 17
February 2025 the prompt follows the v0 page by six days and asks for the same thing that page does, a spanning tree on
a grid whose cells are shaded, and with its defaults: the page asks for a 10 × 10 grid by default, and its random
layout in the folder has five nodes per tree (`../sources/early-experiments/v0-prototype-2025-02/`). The one-turn path
is new, and is the message's "Heavily favor straight edges along grid cells over diagonal ones" made a rule.

## 5. The April 2025 figure against the file (check a)

**No code in the file draws "Multiple 1-Team PvP Layouts (Improved Graph Connections)".** *Record:* the picture of 5
April 2025 (`../sources/early-experiments/2025-04-05-graph-layouts-matplotlib.png`, looked at for this file) has that
super-title and four panels, each titled "Layout N", "Rows: 6–8" and counts "L: C: R:", with grey, cyan and red nodes
and some green edges, on a white field without grid or axes. The file's titles are the ten ChatGPT figures in the table
above and, from the 24 May script, "Single Objective Layout", "Dual Objective Layout", "Triple Objective Layout" and the
default "Level Layout". None matches, none has subplots, and every one draws axes, a grid and a legend.

**The figure is closest to ChatGPT's in its words, not in its look.** *Inference:* "PvP" and "Layout" in the title, a
parenthesis naming the change ("Improved Graph Connections") as ChatGPT's titles name each revision, and matplotlib,
which ChatGPT used throughout the conversation, fit the author's guess that the April experiment was ChatGPT (account
§21); the figure is a later stage, one team's half in rows and three columns, with a cyan top node and red side nodes,
which the conversation never reached. The tool of April 2025 stays unrecorded; ChatGPT is likelier than before, and no
more than that.

## 6. 24 May 2025: requirements, a script, and the tablet screenshot (check b)

**The first chat of 24 May opened with eleven numbered rules.** *Record (his prompt):* "Develop an application to
randomly generate level designs for a game with two teams." — a spawn and one to three objectives per team, "points if
interest"; "R1 Levels are mirrored along one axis to ensure fairness for teams."; R2 objectives closer to spawn than to
the axis; R3 all points connected; "R4 Objectives are terminal points"; R5 spawns at ends or intersections; R6 spawns
equidistant to objectives; R7 a minimum spawn–objective distance; R8 bounding boxes not too wide or long; "R9 At least
2 and up to 4 paths should pass through the center axis"; R10 few unnecessary paths, since players find the shortest
routes; R11 paths should intersect, not run in parallel to the axis; user variables; "Before beginning with the
development it may be wise to structure these requirements and come up with a plan. You can also ask me questions."
(L937–L968). Only the link to the chat follows.

**The second chat of 24 May asked for a Python script, and the file keeps its result.** *Record (his prompt):* "Please
help me with the development of a python script with visualization capabilities for level design. The script should
generate layouts based on nodes and edges for a mini game." It states the rules again in prose: mirrored halves,
objectives far from the axis "to ensure objectives do not get easily rushed", spawn between two objectives, objectives
at lane ends "reached from a single side", spawn at intersections of up to three lanes, team sides separated by void
"reached from two or more lanes", "Lanes are primarily straight with right angles splitting." (L975–L977). The result
(L981–L1338) is a `LevelGenerator` with node types `SPAWN`, `OBJECTIVE`, `LANE_INTERSECTION` and `VOID_ACCESS` and edge
types `LANE` and `VOID_CONNECTION`: it places one team's objectives at fixed offsets, a spawn between them, an
intersection near the spawn and one before each objective, right-angled lanes with one random elbow, two void access
points at the void's edge, mirrors the half across the vertical axis and joins the access points across the void. A
`LevelVisualizer` draws it in matplotlib with "TEAM A", "VOID" and "TEAM B" labels, at `width=24, height=12`.
*Account:* "Das war das claude artifact was bislang noch keinen link hatte!", that was the Claude artifact that had no
link until now (L1340), with the artifact's link.

**The tablet screenshot is this artifact in its interactive form.** *Record:* the screenshot
(`../sources/early-experiments/2025-05-24-claude-chat-level-design-generator.jpg`, looked at) reads "Sa., 24. Mai" and
01:39 in its status bar and shows "Interactive Level Design Visualizer", version 6 of 6, a "Level Design Generator"
with "Objectives per Team" and "Map Size: Medium (24x12)". Its legend is the script's six classes under their screen
names, "Spawn Points", "Objectives", "Lane Intersections", "Void Access Points", "Lanes", "Void Connections", in the
script's colours: green spawn, gold objective, light-blue intersections, orange triangular access points, blue lanes,
dashed red void connections; TEAM A, VOID and TEAM B stand over a grey strip, and 24 × 12 is the script's default size.
The screenshot is a web page, not a matplotlib window, and some of its lanes run diagonally where the script makes
right angles. *Inference:* one artifact, first written as the Python script and turned into an interactive page by
version 6; the screenshot and the link of L1340 are the same chat.

**The year is 2025 by the weekday.** 24 May 2025 was a Saturday, as the status bar says; 24 May 2024 was a Friday and
24 May 2026 a Sunday. The R1–R11 chat is placed on the same day by the file; its year follows from its being named
with the script ("Am 24. Mai auch", L937, L973).

## 7. 11 February, 17 February and the ChatGPT trees: the order (check c)

**The sources support this order.** (1) 30 August 2024, the Claude canvas with four tags (account §26). (2) Undated,
the ChatGPT conversation, which ends on the idea of several non-intersecting trees (inference, §3). (3) 11 February
2025, the message to samschaap and the v0 page, which builds several trees, skips colliding edges and shades cells
(record). (4) 17 February 2025, the Claude artifact that colours a spanning tree's cells on a 10 × 10 grid with one
turn per path (year by inference, §4). (5) 5 April 2025, the matplotlib figure (record; tool unrecorded). (6) 24 May
2025, the requirements chat and the level-design script with its interactive version (record, year by weekday).

**What the order does not show.** Whether the ChatGPT conversation was days or months before 11 February 2025; whether
the v0 page was made before or after the message was written (the message links a finished page); and whether
anything ran between August 2024 and the ChatGPT conversation.

## 8. 15 and 16 August 2025: the pasted conversation and the v0 chat (check d)

**The Claude chat of 15 August 2025 holds the ChatGPT conversation; the v0 chat began the next day.** *Record:* the v0
chat "Layout generation app" opens at 21:31 UTC on 16 August 2025 with one attachment and "implement this layout
generation as a web application with configurable parameters, visualization, and export."
(`../sources/early-experiments/v0-chat-2025-08-16.md`). The file dates the Claude chat with the pasted conversation
"15.8.25" (L1). *Account (earlier):* he could not say what the attachment was; he assumed he had described his
algorithm idea and asked questions elsewhere first (account §21).

**Inference only.** The Claude chat of the day before is a candidate for that "elsewhere": he took the old ChatGPT
conversation into Claude a day before asking v0 to implement "this layout generation". It cannot have been the
conversation alone, as pasted: the v0 chat's algorithm is a random 3×3 grid per team, mirrored or rotated, with
row-independent columns, and none of that is in the ChatGPT conversation. If the attachment came from the chat of 15
August, the 3×3 algorithm was worked out there; what was said in it is not in the file and no link to it is given.

## 9. The parser chat and the hex dump (check e)

**The file tells how the schematic code began.** *Account:* "Nach ewiger suche endlich gefunden wonach ich suche. Den
chat mit dem Parser Code." (L1388). On MinecraftLayoutEditor "ein sehr guter Freund aus Abitur und Studium" helped, a
game developer and "ein ziemliches coding Guru", who had already tutored him for his master's thesis (L1390); he is not
named, and this file does not name him. Together they opened a schematic file in HxD, "ein spezielles Programm … was
ich noch nicht kannte", to understand how it is stored, and found public documentation of the format, the archived
`NBT.txt`. They gave it all to Claude with "Can you tell me what this hex file says?", the bytes, and "Here is the NBT
specification." (L1392–L1396); after the explanation, "Based on this information can you write me a parser?" (L1398).
"Dann kam erst was in javascript aber auf Nachfrage in c#" (L1400), first something in JavaScript, then on request C#,
with the artifact's link. The file gives no date for this chat.

**The bytes are an uncompressed NBT schematic of a 3 × 3 floor of bedrock.** Decoded for this file (257 bytes, read
to the end with nothing left over):

| Bytes (start) | Tag type | Name | Value |
|---|---|---|---|
| `0A 00 09 53 63 68 65 6D 61 74 69 63` | Compound (10) | `Schematic` | the root |
| `02 00 05 57 69 64 74 68 00 03` | Short (2) | `Width` | 3 |
| `02 00 06 4C 65 6E 67 74 68 00 03` | Short | `Length` | 3 |
| `02 00 06 48 65 69 67 68 74 00 01` | Short | `Height` | 1 |
| `08 00 09 4D 61 74 65 72 69 61 6C 73 00 05 41 6C 70 68 61` | String (8) | `Materials` | `Alpha` |
| `03 00 09 57 45 4F 72 69 67 69 6E 58 FF FF FF FF` | Int (3) | `WEOriginX` | −1 |
| `03 … 57 45 4F 72 69 67 69 6E 59 00 00 00 00` | Int | `WEOriginY` | 0 |
| `03 … 57 45 4F 72 69 67 69 6E 5A FF FF FF FF` | Int | `WEOriginZ` | −1 |
| `03 … 57 45 4F 66 66 73 65 74 58 00 00 00 00` | Int | `WEOffsetX` | 0 |
| `03 … 57 45 4F 66 66 73 65 74 59 FF FF FF FF` | Int | `WEOffsetY` | −1 |
| `03 … 57 45 4F 66 66 73 65 74 5A 00 00 00 00` | Int | `WEOffsetZ` | 0 |
| `08 00 08 50 6C 61 74 66 6F 72 6D 00 06 62 75 6B 6B 69 74` | String | `Platform` | `bukkit` |
| `07 00 06 42 6C 6F 63 6B 73 00 00 00 09 07 07 07 07 07 07 07 07 07` | Byte array (7) | `Blocks` | nine bytes, each 7 (bedrock) |
| `07 00 04 44 61 74 61 00 00 00 09 00 … 00` | Byte array | `Data` | nine zeros |
| `09 00 0C 54 69 6C 65 45 6E 74 69 74 69 65 73 0A 00 00 00 00` | List (9) of Compound | `TileEntities` | empty |
| `09 00 08 45 6E 74 69 74 69 65 73 0A 00 00 00 00` | List of Compound | `Entities` | empty |
| `00` | End (0) | — | closes the root |

*Inference:* the `WEOrigin`/`WEOffset` keys and `Platform` `bukkit` are what WorldEdit on a Bukkit server writes, so the
file was a WorldEdit copy of nine bedrock blocks, decompressed before it was read (a schematic is stored gzipped, and
gzip bytes would not show tag names in HxD).

**The repository holds a schematic writer from 12 October 2025 and no schematic reader at any time.** *Record:*
`d961f6a` (2025-10-12 00:13 +02:00, `michael`, "change node highlight, add schematic creation and download") adds
`MinecraftLayoutEditor.Schematics` with `Schematic.cs`, `SchematicMaker.cs` and `SchematicWriter.cs` (140 lines).
`SchematicWriter` writes big-endian NBT tags of types 1 to 10, Byte to Compound; `Schematic` writes a root compound
`Schematic` with `Width`, `Height` and `Length` as shorts, `Materials` = `Alpha`, `Height` 1 by default, the byte arrays
`Blocks` and `Data`, and an end tag, and gzips the result. It omits the WorldEdit keys, `Platform`, `TileEntities` and
`Entities`. Later schematic commits change what is written, not how it is read: `7c3d3d9` (16 October, "fix mismatch
between blocks on screen and blocks in schematic"), `2abc036` (5 November, "schematic: map thickness"), `ec4a726` and
`ec753e2` (9 November). The first code that reads NBT is `d2c4bc3` (2025-11-06 03:20 +01:00, "working import of
.leveldat and .mca files (claude & grok)"), a world importer that reads region files and `level.dat` through the
`SharpNBT` 1.2.0 package, with a short hand-written fallback that only looks for a `Level` tag; it reads worlds, not
schematics. No commit on any branch adds a schematic reader, a class named for one, or the string `WEOrigin`.

**What "Parser Code" corresponds to.** *Inference:* the parser of the chat was the means of understanding the format;
what reached the repository is its inverse, the writer of `d961f6a`, which writes the same root, the same three
dimensions, the same `Materials` value and the same two byte arrays as the bytes they read, with `Height` fixed at 1 as
in the dump. The writer's ten tag types are those of the archived 2011 specification, which predates later tag types.
So the chat most probably came before 00:13 on 12 October 2025, in the two days after the solution was opened on 10
October, when he told the contest's map developer he was working on the editor with a friend (research/17). The
parser itself, in JavaScript or C#, is in no commit. Which commits under `michael` the friend wrote, the record cannot
say; the file does not say that the friend wrote any.

## 10. "Pillars" and 29 May (check f)

**Pillars is a blitz map in CommunityMaps, created 28 May 2025 and committed on 29 May 2025.** *Record:*
`CommunityMaps/blitz/pillars/map.xml` (read through `git show`): `<created>2025-05-28</created>` for the main map,
version 1.2.4 at the head, author rockymine, contributors Pablete1234 ("XML"), Ruediger_LP ("Mental help") and emcode
("Item randomizer"); an FFA variant by Javg_ was added in June 2026. Its first commit is `b09d1e05`, "Pillars 1.0.0",
2025-05-29 21:24 +02:00, by RuedigerLP; 1.0.1 at 22:15, then at 22:48 `923a50aa` (message "Pillars 1.0.3", file version
1.0.2) and at 22:51 `64be09c4`, "Pillars now actually 1.0.2". No folder or `map.xml` of that name is in PublicMaps.

**From its third commit that evening the map credited Claude.** *Record:* `923a50aa` added the contributor line
`<contributor contribution="intelligence">Claude Sonnet 4</contributor> <!-- Claude -->` beside Ruediger_LP's "mental
help"; it stayed through 1.0.3 (eliminate123, 29 October 2025), 1.0.4 and 1.1 and was removed in `cd4f8815`,
"Pillars: 1.2.0 (#1348)", 2026-06-13 by Reason, where emcode's "Item randomizer" took its place. *Inference:* the
author's "29. Mai", the first try at having Claude help write an XML, is 29 May 2025, the evening the map was first
committed and given a model credit. That is fourteen months before Kuusepuu CTC's "CTC conversion: Claude Opus 5"
(research/11), which research/11 counts as the earliest model credit among head `map.xml` files; the Pillars credit is
not in the head any more, which is why that count did not find it. A search of every XML change in CommunityMaps on all refs up to 29
May 2025 for "Claude", "ChatGPT", "GPT-", "Gemini" or "Copilot" (`git log -G`) finds this commit and no other, so
Pillars is the earliest map in CommunityMaps to credit a model; the same search of PublicMaps had not finished when this
file was written.

## 11. What the record holds of 2024 (check g)

**Before this file, nothing in the folder concerned generation in 2024.** *Record:* the year appears in the history's
sources only as map history and as the start of conversations: Agrostid's 2.0.0 edit, moved to 0,0 on 14 October 2024
(research/19 §1), its Christmas variant "Agrochion" of 2024-08-15 (research/19), Annealing II Short and IV added in
October and November 2024 and proto migrations of December 2024 (research/08); the direct messages with the contest's
map developer, which begin in September 2024 and were read for 2025–2026 only (research/17); and, in the server search
for "ai maps", scattered posts of 2023–2024 by players asking whether AI could generate maps and XML (research/17 §2).
None of these mentions a layout tool or a chat with a model. The Claude chat of 30 August 2024 is the only 2024 item
about making maps by machine, and it rests on the author's dating and three links that could not be opened.

## 12. Where the file changes the history

| Earlier statement | What the file and the checks show |
|---|---|
| The history begins on 11 February 2025 | it begins on 30 August 2024, with a Claude chat and a canvas of four tags (account; year his) |
| The graph idea starts on 11 February 2025 | ChatGPT drew spanning trees from his prompts first, undated, most probably before 11 February (inference) |
| Claude is first recorded on 24 May 2025 | Claude on 30 August 2024 (account) and 17 February 2025 (account, year inferred) |
| The April 2025 tool is not known, perhaps ChatGPT | still not recorded; no code in the file draws it; ChatGPT fits its words (inference) |
| Who wrote the first algorithms: not stated | ChatGPT's code from his prompts; the steps are his |
| A model's first use for a map XML: not stated | Claude on Pillars, 29 May 2025, credited "Claude Sonnet 4" for "intelligence" in the map from that evening to June 2026 |
| The schematic code: commits only, "with a friend" | a school and university friend, a game developer, unnamed; a hex dump and the NBT specification given to Claude; a parser in JavaScript, then C#; the committed code is the writer of 12 October |
| The v0 attachment of 16 August 2025: unknown | still unknown; the Claude chat of the day before held the ChatGPT conversation (inference only) |
