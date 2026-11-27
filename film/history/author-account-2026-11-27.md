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
