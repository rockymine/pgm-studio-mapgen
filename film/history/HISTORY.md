# A year of AI-made maps: September 2025 to November 2026

This is the history of how rockymine, with Ruediger_LP and a run of AI models, set out to make PvP maps for PGM
servers by machine, and of what that tool became. It is written for someone who was not there. It rests on seven
research files beside it (`research/01` to `research/07`) and on the author's spoken account of 27 November 2026
(`author-account-2026-11-27.md`). Every date, number and quotation below comes from one of those, and each paragraph
says which kind of source it rests on. **The record** is a commit, a file or a published map. **The author's account**
is his recollection, given on one evening, and it is marked as such wherever it carries a claim the record does not.

A word on the terms. PGM is the plugin that runs competitive Minecraft maps, each described by a `map.xml`.
Capture the Wool (CTW) is the mode where a team carries the enemy's coloured wool back to its own monument;
Destroy the Monument (DTM) and Destroy the Core (DTC) set teams to break objectives. Many PGM maps float in the
void, and players bridge the gaps with blocks. CommunityMaps and PublicMaps are the public repositories of about 350
such maps, and the studio treats them as its corpus: the measure of what authors actually build.

---

## 1. Autumn 2025: a drawing that became blocks

The record begins on 28 September 2025 with a repository called `CTW-Layout-Generator`, made in Google's AI Studio.
Within three days it held a seeded generator of capture-the-wool layouts whose node types were `SPAWN`, `WOOL`,
`HUB`, `FRONT_LINE` and `CENTER_HUB`. That vocabulary would return nine months later as the backbone of the studio.
The app described itself as making layouts "within a void-based architecture". It drew a graph and exported JSON,
and it stopped after six days.

The step from drawing to blocks came in a second repository the author built himself, in C#. `MinecraftLayoutEditor`
opened on 10 October 2025 around a `Graph` of typed nodes, gained symmetry the next day, and on 12 October committed
"add schematic creation and download": a graph drawn in the browser became a `.schematic` file, each edge rasterised
as a line of blocks. The author's brief places this realisation "at the start of the year"; the record dates it to
that October, and research `01` notes the discrepancy. On 6 November the editor learned to import a real world,
"(claude & grok)", which is the first time an AI model is named in a commit message. It stopped on 16 November.

Two identities commit to these repositories, `michael` and `rockymine`, on the same days. The record does not say
whether they are one person, and the history does not assume it.

## 2. Spring 2026: reading maps before writing them

Five and a half months pass with nothing in the record. On 31 May 2026 a Python project, `pgm-map-studio`, opened
with Claude Sonnet 4.6 as co-author. It began by reading rather than generating: it scanned existing worlds and found
their islands. On 5 June its pamphlet put the idea that underlies everything after it into one sentence: "The ground
plane is not just terrain — it is the map's navigational grammar." On 7 June a sketch drawn in its browser editor
exported as "a complete, PGM-loadable map folder". The last Python commit is at 03:24 on 12 June.

## 3. June and July 2026: the studio, the graph that went, and the boxes

Fourteen hours after that last Python commit, `pgm-studio` was opened, and on 13 June Claude Opus 4.8 ported the
whole Python studio to ASP.NET Core and Blazor in one commit of 145 files. The brief says the author moved to C#
because it is a language he can read; the record holds no reason, and research `01` points out that the C# era had
in fact begun the October before. The stack chosen that day, MariaDB under an HTTP API with a browser client,
is the one still running.

The studio's first two months were spent deciding what a map is. On 20 June a corpus analysis of 347 maps found
that "the generator emits 0 neutral mid pieces but 88% of real maps carry a contested middle". On 2 July the oldest
idea in the record, the map as a graph, was written up as an architecture at 14:31 and abandoned at 14:54, because
"a thinned skeleton cannot represent side contact". The same afternoon a strawman of layout rules was offered "for
correction by id", and the author corrected it. That pattern, a model guessing and the author ruling, is the method
of the whole year.

**The first worlds the studio built were three grey boards called Base.** On 2 July Opus 4.8 shipped the export
that writes a world folder, and drove three seeds through it the same morning: Base 2-Island, Base 2-Wool and Base
4-Team, "The most basic CTW design: two team islands + a contested centre", on a cell of five blocks. Each came out as
the author remembers: a bedrock floor at y 0, stone to each island's height, and spawn and wool in "a hollow 8×8×8
bedrock shell". In his account they were his layouts, drawn on squared paper, and he names them "Base to Rule" and
"Base for Teams"; the record holds the names 2-Wool and 4-Team, which sound much the same, and no drawing. That
bedrock box became the default room. Rooms could be given a library style from 5 August, but an unbound room still
stood in the box, and the reviews of at least three later runs say a spawn or wool room was left in it by mistake.
From 27 September the studio complains of it (rule `WX14`). The seeds also stated `"authors": []`, which is where the
nameless maps of chapter 6 begin (research `07`).

By 21 July the model had settled into boxes: every board a spawn, a hub, wool approaches, a frontline and a middle,
composed in that order, and "the box pipeline is THE composer". Destroy modes arrived on 15 July, a month after
capture the wool. The model was written down as `docs/generator/model.md`, which on 15 August gained its own
boundary: organic maps such as the Thunder series cannot be expressed, and "That is a limitation rather than a
defect, it is the author's stated position, and it stays."

## 4. August 2026: colour, trees, and the first maps on a server

**The colouring began on 1 August, and it began as walls.** Until then the studio exported "one flat block of stone"
over bedrock at y 0. On 1 August Opus 4.8 specified terrain painting under the title "walls, rims, plateaus": the rim
is the top block of an edge column, the wall is "the exposed riser between bedrock and rim", and the interior is the
grass top. In the author's account, "map walls" is his name for exactly this, how a large shape is coloured, and his
account of its growth matches the record's order. A rule per height came first: research `05` finds it in the
authoring specs' `themeByHeight` key, which hands one theme to every tier at one height. Then a shape's top, sides
and edges (1 August), shading from the outside in (the inward axis, 15 August), stacked patterns, and later the
slope. Themes could be scoped to one piece, so one area had one pattern and its neighbour another. The author's
account says real transitions between them never worked.

**The first tree was grown and failed.** A recursive brancher on 1 August "read as a fractal, not a tree"; on 2
August it was rebuilt as limbs swept along Catmull-Rom splines; on 5 August a separate vanilla tree, a trunk under a
canopy of known profile, was split off. On 12 August the grown tree was measured against 75 trees the author had
built by hand on a showcase world, one tree per platform, and failed: "1516 of 4020 never touch their branch". The
author's account puts it simply: a vanilla-like blob is easy for a model to code, and a real tree generator failed.
The vanilla tree is still in the studio. The grown one was deleted on 10 September on his ruling that "the form goes
rather than gets a knob".

**The first map credited to the studio reached a public server on 7 August.** It is called *No Blocks Placed*, a capture
the wool map for two teams of 28, committed to CommunityMaps that evening by Ruediger. Its `map.xml` credits
rockymine for "Drawing pieces, shapes, and markers in the browser.", Ruediger_LP for "Wisdom." and Flamiix for
"Minimalist." The author recalls Tttie as its third author. The record names Flamiix, and shows TTtie adding the
map's creation date on 15 August. The author's account also says one generated tree still stands on it. Research
`05` finds trees there in mirrored pairs, the largest a body of 320 blocks with 50 logs, which reads as the grown
limb tree of that week. Which body he means wants his eye in game. The studio itself kept the map as its own worked
example for the Configure tool from 13 August.

**On 11 and 12 August the first fifteen AI boards were built,** eleven by Opus 5 and four by Haiku 4.5, each from a
single JSON spec through a tool inside the studio, `tools/mapgen`. Two of them went to CommunityMaps on 12 August,
Thornwake and Viridian. The author's first review was written that night, in words: thirteen faults, MG1 to MG13.
Spinebreak belongs to this batch. It is a ridge 145 blocks wide and 405 long, with eight objectives strung along it.

**On 13 August an agent made a confident, measured and wrong claim,** that every generated destroy map was
unwinnable because the goals floated above the ground. Floating goals are PGM's design. The claim was withdrawn the
same day, and the studio's instructions gained the rule that a question about how a map plays is answered by asking
the author. The same day `pgm-studio-mapgen`, this repository, opened, and its first report, by Opus 5, told the
author to delete the agent's own shortcut: `tools/*` "is a reimplementation, not a caller". The tool was deleted on
20 August, and from then on every model went through the studio's one HTTP front door.

**The second half of August was the model trials.** Haiku, Sonnet, Opus, Fable and Grok were given the same kind of
brief. Haiku 4.5 reported two boards as "verified working" that were 245-byte `map.xml` shells. Grok wrote three maps
for a studio it could not run, and all three layouts "rasterize to no ground". On 22 August Haiku 4.5 built Hollow
Crown, a test board 100 by 120 blocks. It holds one monument and one core a team on flat ground, and each team's core
shares its cuboid with the enemy's monument. Meanwhile the studio made itself legible to agents. It answered with one
kind of finding and one refusal envelope, served its 125 rules by id, and on 19 August described its own 131 paths.
On 16 August it began to measure **dead ground**, the share of a board no route between objectives crosses. The
measure's tolerance was calibrated against the author's own reading of one board, Wheal Hazel, piece by piece.

## 5. Late August and September: Millrace, by hand

**The year's clearest lesson came from one map.** On 30 August the author drew a basin in the studio's Sketch tool.
The same day three agents built it out: Opus 5 as `opus5-millrace`, a walled water course with a sluice and a viaduct,
and Sonnet 4.5 twice, as Cutwater (flooded and bridged) and Fallowmere (left open). The author's account remembers
Sonnet and Opus being tried and Opus's terrain kept, and the record agrees, with a third board he did not name.

By the early hours of 2 September he and Ruediger_LP had finished Opus's Millrace by hand. Their own review, the only one in the
repository in the author's voice, says they "spent 5 hours". The author's account gives the same figure as five hours
side by side, ten person-hours. "The terrain, spawn platform, spawn house, objetives, canal walls, water levels,
bridges, boulders, and most house placements were kept intact … essentially all that was done is theming and some
dressing." The houses and their interiors were redesigned, a tug replaced the ship, and the eighteen grown trees were
replaced by sixteen of the author's showcase trees. Fable 5.1 later measured that 29,954 of the 35,610 columns kept
their surface height exactly. Ruediger committed it to CommunityMaps the same day as Millrace 2.0.0, credited to
rockymine for "layout, terrain, block palette, beautification", Ruediger_LP for "interior design, houses,
beautification" and Opus 5 for "layout composition, initial draft, sculptures, bridges".

**Then Fable was asked to rebuild it.** The author's account says Fable began copying the trees, and that this led him
to tidy his world of custom trees and add it to the repository. The record keeps a different order. The tree world had
been in the studio since 12 August. It was committed here at 00:53 UTC on 2 September, before the revamp itself, and
Fable 5.1's work followed about two hours later. In the studio Fable built a new form, the *copied tree*, "cut out of a world
and planted as a recipe". In this repository it diffed the two Millraces and restated the revamp as studio documents.
The world grew afterwards, to 86 trees on 20 September and 95 on 1 October, and it is the tree corpus the studio plants
from today: 95 author-built trees in 20 bands, under a hundred as he says. In his words tree building is "a
religion"; a boulder or a house is easier because it is not organic. The houses had in fact become a parametric
system in one week of August, six roof forms from one formula, and by October the library held 61 styles.

**September turned taste into instructions without turning it into gates.** On 5 September the studio learned to
paint by slope, "the only thing in the model that tells a 45-degree hillside from a flat field". The author's account
calls this an important step, because angle tells a story where plain layers do not. On 19 September the author's
rulings on look were written into `WHAT-A-BOARD-IS-MADE-OF.md`, whose opening admits that "None of it is enforced
anywhere". On 21 September Haiku 4.5, Sonnet 5 and Opus 5 built the same four-objective brief on the same day. No Haiku
board built, and two of Sonnet's four carried more dead ground than the studio's band allows. On 27 September the
studio first drew a board "from a player's eye" in Minecraft's own block textures. The commit says why that mattered:
"two noisy blocks of one colour are one calm grey in a flat picture and static on the ground".

## 6. July to September: the tests on the server

**The AI maps reached the server through Ruediger, and the record of it is CommunityMaps.** Research `06` reads that
repository's whole history. Every AI- or studio-made map it holds was committed by RuedigerLP, in four batches. The
first came on the night of Monday 27 July: Kuusepuu CTC, an existing map of the author's turned into a capture-the-cake
game and credited "CTC conversion: Claude Opus 5", and an hour later Hello World Micro, a plan from the studio's
plan editor, which reached the server ten days before No Blocks Placed but credits rockymine alone. Both were
revised until past two in the morning. Kuusepuu's fix of 31 July is the one commit whose text
reports play: "Reported live: a carrier died, the cake went home, and he still came back holding a usable cake".
No Blocks Placed followed on 7 August. On 12 August Hello World Micro was deleted and Thornwake and Viridian added
five minutes later. Millrace came on 2 September. Six maps in all; five are still there.

**After 2 September the tests leave CommunityMaps.** Ruediger commits nothing there until a map of his own in
mid-October, and no board of this project is uploaded again. The later tests are recorded in this repository. On
Sunday 27 September, from 21:55 UTC, Opus 5.5 committed Delverdale and Whitstone Weald as "two large boards for a
32-a-side play test", beside "the eleven small boards in the same play test". That is the date the author gives for
the last test, and it is a Sunday. The record shows the boards made ready, and was still changing them after
midnight; it does not show the session. The October rounds on the freeform boards were committed on a Friday night and
a Saturday, 9 and 10 October, and none of those boards went to CommunityMaps.

**They did not go to PublicMaps either.** The author thought the later tests might be there. Research `07` reads its
whole history: no AI-made map entered PublicMaps between June and November, Ruediger has not committed there since
February 2025, and the repository has no commit on 27 September. A private maps repository, which the author also
names, cannot be read. The batches of about fifteen he recalls are this project's own: fifteen boards on 11 and 12
August, and thirteen for the test of 27 September.

**Two of the summer uploads were game-mode experiments in XML.** Kuusepuu CTC came with the body "Capture the Cake
prototype!": the author's destroy map with its monuments removed and a cake to eat, carry home and place. Hello World
Micro was a "grey map for concept test" from a studio plan, the same stone-and-bedrock kind as the Base seeds. Its
1.0.1 rolled, per game, whether a team needed one wool or two, and when the first fell the enemy's wool box was
recoloured and the server announced "Wool Room Switched". In the author's account the room moved, and in its one test
players fell out of the world as it moved from under them. No version in CommunityMaps moves a room or takes a block
from under a player, and no commit reports that test. It was deleted on 12 August.

**And on the studio's own boards, the map was made by nobody.** None of the six uploads lacks an author. The boards
built through the studio did: the observer platform carries a sign that reads "made by" over the authors, and on 4
September the studio found that "69 of those 74 carried 'made by' over three blank lines, which reads as a map whose
author is called nothing". From then the sign is left off and the build complains (`EX6`). The author remembers it in
the tab list, and as the first tell of an AI map. The two large boards of the 27 September test were credited to
Opus 5.5 after midnight that night, and on 28 September every exported board was credited to the studio.

## 7. Late September: the studio goes public, and the maps are empty

**Between 26 and 28 September the studio became a website.** It gained Discord sign-in by invitation, tokens for
callers without a browser, a build queue, and on 28 September pgmstudio.de deploying itself from a green `main`. An
agent could now drive the deployed studio with a key it never sees. Today the site lists 72 maps: 31 made by agents,
the rest by eleven people. One of the eleven is TTtie.

**The review tool arrived the same evening.** Map notes pinned "to the whole map, to the picture in view, or to ground
on it" landed at 20:30 UTC on 28 September, with a point, box or lasso drawn on a picture and projected onto the ground
the picture shows. The author's account says this is when feedback improved. Before, he described faults in words and
the model had no coordinates. The first run that used the notes is also where his "two extremely empty maps" are
recorded: Opus 5.5's Gypsum Reach and Sootcombe. His remark was given in chat and survives as a paraphrase. "There is
no dirt or grass for a tree to stand in, two houses stand by a path, the frontlines are bare … Empty is what players
dislike about maps like these." In his account empty, dreary maps remain a problem.

Opus 5.5 had written its first studio commit on 22 September, and from October it wrote almost all of them: 414 that
month against Sonnet 5.5's 32.

## 8. October: freeform, the grammar, and the rethink

**On the night of 7 October an Opus 5.5 session stopped driving the studio and wrote the voxels itself.** The board was
Riftwater, "one river valley split down the middle by a bottomless rift", floating from y 27, a market town and a
mining village on each side. In the author's account the first board of the Python rework was "a floating island with
two villages, 'Riverside' or similar". Riftwater is that board. His account says he had told a session that he did not
like what the layer model made and asked it to think; that instruction is not in the record. What the record shows is
the pace that followed. 8 October holds 86 commits: some twenty freeform boards, and the first versions of a shared
Python library, `pgmvox`, which by the end of the day carried tunnels, chambers, galleries and shafts. This is the
limit the author names. Under the layer model a cavity was built wall by wall, and the studio's carve "cannot hollow a
column out from the middle".

**The grammar came on 9 October, and it was his own look.** An Opus 5.5 session read the author's maps Brittlebush
(2022) and Brittlebush II (2023) block by block and wrote their signature as a style: "a bedrock block under a
five-course cap (spruce-stair rim, brick, dark-oak slab, dark-oak stair, black clay), one birch panel in each face's
middle". At 18:28 it separated the rules from the blocks, `pgmvox.grammar`, "the rules of a structural board apart
from its blocks". Nineteen minutes later a second style, Claywork, was "spoken in the grammar", and within the hour a
third board carried the Brittlebush style beside grown ground. This is the transferable look of the author's account,
defined once and laid on any map, which he says no building plugin offers. The layout of Brittlebush III was his,
drawn on pgmstudio.de as "Brittebush III". In his account its final colouring was done entirely in game because the
tool still could not express it, and that world is not in the record.

**A playtest and an experiment followed.** By 10 October the author had played the freeform and trial boards, and his
notes were sorted into 30 faults, of which the studio "would have caught 9, partly caught 4, and not caught or could
not have built 17". Riftwater was "essentially perfect", in the agent's summary of his words. In his account these
tests were "Slop Sundays", two hours on the server with the mapmaker Tttie, and early maps "looked and played alike".
The record never uses the name. It does hold a Sunday, the 32-a-side test prepared on 27 September (chapter 6); these
October results were committed late on a Friday and early on a Saturday. On 10 October a controlled experiment put
Sonnet 5.5 on the same briefs in both tools and found "the two
tools made boards of comparable quality". The difference lay in spend: Riftwater took "Opus, hours per board rather
than minutes, rounds of the author's review, and bespoke code".

**On 15 October the studio began to absorb its laboratory.** `docs/pgmvox-port.md` set the goal of "a board built
through the deployed studio that the author cannot tell apart, by quality, from one built with pgmvox". Nine phases
and 23 decisions followed. On 18 October the rectangle plan retired as a level. On 24 October the relief solver of
August gave way to a modifier stack of landforms, and paint rules and slope-thinned soil arrived the same day. Carves,
a tunnel, a chamber and a shaft, came on 25 October. By 4 November every phase had shipped or been parked. The grammar
phase has no shipped line.

The late-October boards were Opus 5.5's on pgmvox, three of them from the author's concept worlds. Of Coldstore, a
bunker under an ice field sent "with signs explaining each piece", the record says: "The author judged the board
finished and the map.xml a success."

## 9. November: building it by hand, and a freeze

**The newest work is a map the author built himself.** On a branch of this repository, agents spent 2 to 7 November
composing the author's hand-built sketch world into a CTW and DTC map set into a mountain, and every version was
rejected. The reasons ran from "the surface was not closed" to "a ramp led into the void". The branch's lesson is the
year's in one line: "a geometric rule is not a design. Every one of those failures passed some check that existed at
the time." He then built the half himself, on a date the record does not hold, and the agents' task became
understanding it. His account says this map has a dead area that makes sense, which is his reply to the dead-ground
rule: "dead" is subjective.

In the studio the author paused new capabilities, and on 13 November "froze the layout generator: nothing changes what
the composer makes". The last commit on `main` is of 14 November. The newest branch carries his rulings on doors and on
labelling anything a model builds itself as a schematic, and in his account the verification pipeline is "not yet where
it should be".

## 10. How the models compare

**The author's judgement and the record agree in direction and differ in kind.** In his account Sonnet's maps were "de
facto worse, whatever the numbers say", and late in the year Opus's were clearly better, through verification steps and
a model progress that stays a black box. The record has one controlled comparison of the two families. On 21 September
Opus 5's dead ground was lower on three of four boards and Sonnet 5 left two outside the band. It has one experiment
that held Sonnet fixed and found the tools level. And it records the author's best words for a Sonnet board, Abbeymoor
built on pgmvox, which "really looks like a place". It records no controlled run of Opus 5.5 against Sonnet 5.5. What
it does show is where his choices fell: the Millrace he finished, the Riftwater he called perfect and the Coldstore he
called a success were all Opus boards. After August's first fifteen, no Haiku board in this repository carries a theme or a prop.
The deployed studio holds two boards by Haiku 5.5 and two by Grok that no report discusses.

## 11. What remains open

**Several facts the author recalls are not in the record, and one is contradicted by it.** No Blocks Placed credits
Flamiix, not Tttie. The trees were in the studio before Fable's rebuild, not because of it. The "500-wide" map fits
Hollow Crown on objectives, flatness and closeness, and Spinebreak on length, and neither is 500 blocks across. The
tests show in CommunityMaps only from 27 July to 2 September, not to his last test of 27 September, which the record
holds in this repository instead, and they are not in PublicMaps. Hello World Micro's room changed colour in the
record, not place. The name "Slop Sundays", the instruction that started the Python rework, the squared paper behind
the Base maps, the fall from Hello World Micro and the in-game colouring of Brittlebush III are his account alone.

**Several questions the record cannot answer belong to him.** Which tree on No Blocks Placed is the generated one, and
how many blocks were placed by hand on a map named for placing none. Whether "map walls" is the walls-rims-plateaus
model of 1 August, and whether `themeByHeight` was the per-height prototype he remembers. What Tttie did on the tests,
who played and for how long, and whether the tests had a schedule. Which rule produced which gain. Why the grammar, which carried his own look onto
other maps, is the one phase of the port with nothing shipped.

**And the open problem is the one he named first.** Maps that look and feel empty and dreary are still made. The rules
can say that ground is off every route, but, as the sorting of his October notes put it, they "cannot say what
belongs". The year moved the tool from a graph to a grammar and from words to coordinates. In the author's view, and
in the branch where he built the map himself, what it has not moved is the judgement of what a place is for, which
stayed with the person who plays it.
