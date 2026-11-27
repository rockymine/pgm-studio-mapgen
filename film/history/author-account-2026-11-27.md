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
