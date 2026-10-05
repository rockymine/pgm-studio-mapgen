# Opus 5.5 — Sciara, an agentic board on the deployed studio after the rules language and the glossary

## What I set out to build

**A destroy-the-core board on a volcano's flank, warm rather than grey, whose made ground is the point.** Two
hill villages face each other across a ravine. Each defends a core floating over the paved threshing floor
(the aia) at the top of its olive terraces. The approaches are an olive grove on one side (through), the
sciara, an old black lava flow, on the other (above), a quarry pit in front (below), and open ground up a
retaining wall (straight). The village and its campanile stand behind.

The run was also a field test of what the studio says when something is wrong, after the shared finding
record, the rule catalogue's `means`/`fix`/`category` and `GET /api/glossary` landed. The glossary was read
once at the start (226 terms). `GET /api/rules?rule=<id>` was used for every rule that fired: `PT4`,
`DR-DOC`, `DR-PASS`, `DR-KEEP`, `ST9`.

Driven against **pgmstudio.de** with the environment's credential. Eleven stored changes on slug
`opus55-sciara`, the last of them the one exported. The board is `review/opus55-sciara.md`.

## What I could not say, or what the studio said wrongly

| # | What happened | Where | Verdict |
|---|---|---|---|
| 1 | A refinement stating `"biome": {"name": "Savanna"}` is stored at **200 with no warning**: no `RQ3` for `refinement.biome.name`. Every later read of the board — `report`, `slopes`, `render/heightmap`, `themes/census`, `preflight` — then answers **400 `RQ1` "is not stated, or is not a kind that exists"** with `field: "serializerErrors"`. Reproduced dry: `PUT /map/{slug}/source?dry=true` with only the biome changed answers 200 | `Refinement.biome`, `PUT …/source` | **defect** — the store accepts a document every read refuses, and the refusal names no field. The wire form is `{"kind": "solid", "id": 35}`, which `BiomeField` documents |
| 2 | A named material nested inside another named material (`materials["sciara-top"].stops[1] = {"use": "lava-rock"}`) is left unresolved. On a **new** map it was stored so, verified in the stored sketch at `themes.sciara.surface.material.stops[1]`. On an **existing** map the dry run refuses with the same field-less `RQ1` | `Refinement.materials`, `StatedName` | **defect** — `StatedName` says a `use` may stand "for a material wherever one is stated", and inside `materials` it is not resolved; worked round by inlining |
| 3 | The walk read routes across the centre line **over** the observer platform: `walk?from=-8,-14&to=-8,14` answers `61 placed, worst step 39` (platform at y60), while `from=-30,-14&to=-30,14` answers `19 placed, worst step 0`. With the platform at the default y37 the same route stepped 16 | `GET …/walk`, the report's `routes` headline | **defect in the read** — one height per column, so the read cannot pass under the platform. Every board whose spawn-to-enemy-goal line crosses the centre reports a worst step that is the platform |
| 4 | The report's header read `props 44 placed, 1 declined` while its `declines` reading listed one `DR-PASS` **complaint** and every prop was in the world | `GET …/report?format=text` | **defect** — the header counts a complaint as a decline |
| 5 | `HouseProp.front` takes `negZ`/`posZ`/`negX`/`posX`; `SketchShape.doors` and the intent's spawn `doors` spell the same directions `-z`/`+z`. `DR-DOC` answered `` `front` … is not a value its field takes `` without the values | `RoomEdge` vs the doors' words | one concept, two words, against "one concept, one shape"; and a refusal on a closed set that does not list the set |
| 6 | `DR-PASS` names the group's box but not which side is short or how wide it is; finding the failing side took three drives | `DR-PASS` finding | **mistaken by me first, then unreachable**: the side and the width are what the fix needs |
| 7 | `ST9` reads "is 22 by 10 blocks, more than 20 by 20 blocks" for a room only one of whose sides is over | `ST9` message | wording — "22 blocks across, more than 20" says the measured fault |
| 8 | `RL4` complains of `mark 'spawn-red' pins no cell` — the studio's own pin for the spawn room, on a yard the author excluded from the relief | `POST …/sketch/relief/read` | a complaint no author can act on |
| 9 | `tools/loop.py --candidates casa-west …` tested four positions for a house and all four answered the original cell, because a house is placed by its wing corners and not by `x`/`z` | this repository's `loop.py` | **out of reach** — a house is re-sited by its `wings` and re-driven |

## What I got wrong

- **I first blamed the field-less `RQ1` on the nested `use`**, inlined it, re-drove, and the board still
  would not read. The cause that stopped it was the biome. Both turned out to be faults (items 1 and 2), and
  the dry probes at the end are what separated them.
- **A surface stack three courses deep paints the whole of a three-block terrace face as soil.** I expected
  the theme's `wall` to own the face. A one-course grass rim is what hands the face below it to the wall.
- **The house was placed by eye on a 20-block yard** and drew `DR-KEEP`, then `DR-PASS` three times. The yard
  could never hold an 8-block passage both front and back. Adding the back lane changed the spawn's second
  door from `-x` to `-z`, which also cleared the first fault.
- **The sciara's crest stood level with the casing's lowest course**, at 37 against obsidian at y37. A
  transect showed it, and the lift went from 6 to 8.

## What worked first time

- The plan: `GO1` 3.33 on the first evaluate, from the arithmetic in `ORDER-OF-WORK.md` §1. It reads 3.23
  now that the spawn hall is 16 × 12.
- **Every flight**, all seven, with half-riser anchors and a run of twice the rise: each walked end to end at
  worst step 0 on its first build.
- `relief_scope: "exclude"` terraces stood at their own heights, because each states a `base_height` taller
  than the compiled ground's 22.
- `refinement.outlines` lobed rings for the push and the two paint patches. The paint patches at the
  landmass's own `base_height` took their cells (census: sciara 15%).
- `POST /plan/room` answered the spawn hall's marker for a stated footprint in one call.
- The copied olives from the library, credited to their builder in `map.xml` without being asked.
- The rules catalogue: every rule looked up answered with a `fix` that was the change actually made.

## Open gameplay questions, decided without an oracle

1. **A 4-block lava-stone wall across the front of the aia, with one flight in it at `x 18..23`.** I read it
   as the defence's prepared line: open ground exposes the attacker, and the wall is climbed or built up.
   Is a wall directly in front of a core right on a destroy board, or does it turn the front into one queue
   at the stair?
2. **The cava is about 30 blocks of tunnel from the core.** Is an entrance from below that far out still an
   approach, or scenery?
3. **Coverage reads 48% dead.** The grove and the sciara are approaches no shortest route takes, and the
   flow read says so in its own words. I read a dead share on a destroy board as a note rather than a fault
   (`match-flow.md` §10). Is a flank that exists to be the long way round dead ground?
4. **The sciara's crest stands two blocks over the casing's bottom course, 28 blocks from it.** Is that far
   still "from above" in the sense `approaches.md` means?

## Timings, on the deployed studio

Every drive — dry run, store, the report read back in one request — took **12 to 15 seconds** wall clock.
The export and the board's picture added under a second. `loop.py` dressing passes took about 3 seconds.
Nothing was refused 429.

## The instrument count

reliefs 1 · marks 3 (`line`) · pushes 2 (the sciara up, the cava down) · `level` flights 7 · made ground 5
(`exclude`) plus the compiled yard · polylines 0 · made layers 2 (the campanile) · copied trees 4 recipes, 11
placed a side · boulders 2 · strokes 5 · flora 1.

## Where the board is

`specs/opus55-sciara/` (the spec and its two documents), `maps/opus55-sciara/` (the world), `review/opus55-sciara.md`
(what it is). On the deployed studio it is the map `opus55-sciara`.

## Revision 2 — the author's review, and what it changed

**The author read revision 1 as empty and flat, and was right.** Five houses had been called two villages,
the terraces were square three-block steps of grass with nothing on them, the threshing floor was a disc of
paving with no edge, and the pit gave nobody a reason to go there. The ruling on how a terraced slope should
look is now `WHAT-A-BOARD-IS-MADE-OF.md`, *A terraced hillside*. How it is drawn without spilling is in
`GENERATION-NOTES.md`, *Shapes*.

**What the board is now** is `review/opus55-sciara.md`:
- nine tilted polygon terraces in four rows, sharing their contours, every made face a cobbled wall with a
  course on top, and twelve flights;
- a town of thirteen houses and a church on three tiers, with streets, a well and a campanile, the spawn moved
  twelve blocks back into it;
- a kerbed threshing floor with two market stalls;
- the pit opening into a tunnel under the aia;
- a lookout, a shrine, crates, a second lava lobe, and the boulders moved to the flows' feet.

`GO1` reads 3.15, 94 props are placed with no decline, and the dead share fell from 48.0% to 38.6%.

**The board stopped being called a lane in `ORDER-OF-WORK.md` §1**, which had stated that a destroy board *is*
a lane. It now says what a destroy board must hold (`GO1`) and that a lane is one arrangement among several.

### Was the village hard to make? Yes, by one rule, and the rule is precise

**`DR-PASS` is the whole of it, and it is not about houses being close together.** Houses within a passage of
each other are one group, and a group may be as dense as an author likes. What the rule asks is that the
group's **bounding rectangle** carry eight blocks of ground with no other building on every side, and it
excuses a side only where the void begins at the very first block past the eaves (`Passage.Blocks` in
`PgmStudio.Minecraft/Dressing/Passage.cs`).

**Three things follow, and each cost a build to find:**
- A house two to four blocks from the coast is short on that side, however much ground lies elsewhere; it
  has to stand flush or eight clear.
- A spawn hall within eight blocks of a group's side makes that side short, because the hall is a building.
- A made tier drawn one block past the plan's coast moves the coast out by that block, so a row stated
  flush becomes a row one block short. A coast that `bendShapes` wanders cannot hold a flush row at all.

**The finding names the group's rectangle and not the side**, so the side was found by elimination: a dressing
pass with one house left in says whether that house is the one (`tools/loop.py` on a copy of the refinement).
Two changes would make a village much cheaper to place, and both are the author's to decide:
- excuse a side whose ground runs out to the coast within the band, not only one flush against it;
- name the short side, and its width, in the finding.

### What I got wrong in revision 2

- **Every terrace first built seven to ten blocks low.** My helper stated a ring's back edge in the same
  direction as its front, so each ring crossed itself and the even-odd fill left its middle to the relief. The
  store answered 200. `GET …/sketch/shapes/{id}?format=text` showed it, the edge from `(−6, −70)` jumping to
  `(−27, −90.73)`.
- **The parapets took three tries.** A polyline with random extra height read as black teeth. A polyline
  moved a block back in `z` still spilled over slanting edges as cobble posts down the faces. Only a thin
  polygon strip set inside the terrace holds none.
- **I wrote that the sciara's crest stands over the casing** and then measured it level with it (38 against
  the casing's lowest course at 38), because the threshing floor rose a block and took the casing with it.

### The open gameplay questions now

1. **The pit was not an approach**, in the author's reading, because nothing drew a player to it. It now
   opens into a three-high tunnel reaching seven blocks under the aia toward the core. Is that enough reason
   to go there?
2. **The lookout at the grove's front** gives the defence a deck at y32 over the lip at 22. Is a structure that
   high at the front line a fair one, or does it hold the landing ground too easily?
3. **The town's coastal faces are cobble** from y23 up, which reads as a town wall along the cliff. Is that
   right for a hill town, or should the coast stay the mountain's rock to the top?
