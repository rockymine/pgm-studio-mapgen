# Opus 5.5 — nine grey boards finished by painters who chose their own reading

## What was asked

**Nine boards whose ground the author had already reviewed were finished by one painter each, and the painter
chose what to read.** The five capture boards are from `reports/opus55-collab-1.md` and the four destroy boards
from `reports/opus55-dtm-terrain.md`. Each came to its painter grey: no paint, its rooms in the studio's
default shell, nothing dressed.

**The brief named the board, the job and where the reading lives, and nothing else.** It gave no block list,
no card to follow and no reading order: `CLAUDE.md` is the index, everything under this repository and
`pgm-studio/docs/` is open, and `techniques/README.md` lists the cards. The ground, the plan and the intent
were the author's and stayed as they were. Painters worked at high effort, side by side in one studio, and
wrote no repository file.

## How the paint is kept

**Each board's paint is `specs/<slug>/paint.json`, and `build-spec.py` lays it over the ground's finish.** It
holds the keys the painter changed, each the batched form of the route the painter called: `themes`,
`mapTheme`, `biome`, `roomStyles`, `dressing`, and where a board needed them `themeById` and `addShapes`.
Millbank themes its room yards by id; Clasp adds a forest-floor patch and Cinderhowe six ash and cinder
patches. The paint's `dressing` replaces the ground finish's whole, so Millbank's river is carried in it.

**Every board was rebuilt from its spec and compared with the board the painter left.** Each was driven under
a throwaway slug and its stored layout and intent compared field by field with the painted ones: all nine
identical. The rebuild is what put `yard` on Millbank's room rectangles, which `drive.py` passed over until a
theme named by id was let reach a projected room: the route paints them, so the key does too.

## The nine at a glance

| Board | Biome | Themes (map default first) | Buildings | Dressing |
|---|---|---|---|---|
| Millbank | Extreme hills | dale, holm, yard | one timber style, the gable in the team colour; a cottage by the spawn | the river, four earth paths, two oaks, ground cover |
| Clasp | Cold taiga | snowfield, spruce-floor | timber lodges: spruce infill, dark-oak posts and laid-log courses | nine strokes, two spruces, a boulder, ground cover |
| Redcut | Mesa | mesa | dark-oak posts and beams, spruce infill, a dark-oak slab gable | four strokes, two trees |
| Lymedown | Extreme hills | downs | flint walls between brick, a hay-bale thatch | six strokes, two trees, ground cover |
| Sedgefall | Swampland | fen | brick in a dark-oak frame, a hay-thatch gable | seven strokes, three trees, ground cover |
| Kelderfell | Extreme hills | fell | white clay over a rubble plinth, a slate roof; a two-wing farmhouse | a tarn, seven strokes, six boulders, ten trees, ground cover |
| Twingill | Extreme hills | fell | a whitewashed farmhouse and a barn | eight pools, four strokes, eleven trees, four erratics, ground cover |
| Scarbutte | Mesa plateau F | mesa | grey stone and dark oak, a wool band; a lookout | two roads and a canyon wash, six trees, four boulders, ground cover |
| Cinderhowe | Extreme hills | heath, ash, cinder | brick with spruce posts and a clay band | four paths, six volcanic bombs, six olives, ground cover |

**Five of nine chose Extreme hills, every one for its muted grey-green grass**, against grey rock on
Millbank, for a fell on Kelderfell and Twingill, and for a volcanic highland on Cinderhowe. Every board houses its rooms in a style its painter wrote, and a build of
any of them raises no `WX14`.

## What the painters read

**All nine opened the same four first, because the index says to:** `ORDER-OF-WORK.md`,
`WHAT-A-BOARD-IS-MADE-OF.md`, the `pgm-board` skill and, for eight, `AUTHORING-BRIEF.md`. Every one then read
two cards, `theme-buckets` and `a-house-style`, and the board's section of its run report.

**Past those, the reading followed the board.** Eight read `GENERATION-NOTES.md` and the tree rows of
`corpus/README.md`; five read `pgm-studio/docs/gameplay/approaches.md`, all four destroy painters among them;
four read `painting-a-patch`, three `water` and two `painting-with-a-stroke`. Only two opened
`techniques/README.md` itself; the others went to the cards by name.

## What the studio got wrong, and what became of it

| Finding | Board | Now |
|---|---|---|
| `{"biome": 3}` stored plains with a 200 — the field is `id` | Lymedown | `RQ3` names the field (`TS111`) |
| The eye's text said `pitch -10` with no word for which way, and the first views looked at the sky | Millbank, Redcut | it says `up` or `down` (`WS78`) |
| The band ending was described as "hold", which is refused | Redcut, Sedgefall | the description says what `repeat` does (`WS78`) |
| A small wool room's picture aimed at the sky marker over it | Redcut | framed on its walls (`TS110`) |
| A monument's picture aimed at its sky marker — 99% sky | Kelderfell, Scarbutte, Cinderhowe | framed on the monument's box, from the air where no ground sees it (`TS112`) |
| A storey `deck` written as a band stack answered 500 on every read of the dressing | Scarbutte | `DR-DOC` naming `shell.storeys[1].deck` (`TS113`) |
| A room left in the built-in shell ships with no finding | none of these; the author's ruling | `WX14` on every build (`WE140`) |
| `ending: repeat` holds the last band, it does not cycle the stack | Lymedown, Sedgefall, Scarbutte, Cinderhowe | the author's call: renaming it needs every stored theme migrated |
| A paint patch past the coast grew the island by 54 cells with a 200 | Cinderhowe | not yet looked at |

**The dead ground two painters worried about is the ground's.** Grey Lymedown read 3.4% where painted reads
2.4%, and grey Scarbutte 58.1% where painted reads 54.5%.

## The boards

Each section is the painter's own account of what it decided and what it would ask, as it reported them.

### Millbank (`opus55-millbank`, from collab-1)

**Millbank is finished: paint, biome, room buildings and dressing are all in.** The relief, the plan setup, the groups, every shape's outline and the intent compare equal to the grey version, and the river prop is the same; the only shape field that changed is `theme`, on the holm and the six room pieces. Pre-flight is OPEN on all four checks. The export answered 200, with only `DR-BANK` from the river and the `ST4` the author already accepted. Coverage reads 1.1% dead: two patches of about 60 cells at (−47, 81) and (45, −82), with nothing placed nearby.

**Decided.**

- **Biome:** Extreme hills: its soft grey-green grass sits well with grey rock, which suits a dale.
- **Ground:** three themes. `dale` covers the map, graded by slope: grass over two dirt up to 40°, then dirt and coarse dirt to 46°, then stone and andesite with cobble at 20% (the incline read is 53% under 10° and the scarp faces are 40–60°, which is where the cuts are). The rim is off. `holm` is the same ground, but everything below y8 is a gravel, clay and andesite riverbed. `yard` is a paved floor of polished andesite, andesite, stone and gravel on the spawn and wool-room pieces.
- **Buildings:** one timber style: spruce-log posts and beams, cream stained-clay walls, dark oak roof, no footing. The gable end takes the owning team's colour, so a player can read whose building it is from across the map. The spawn hall is two storeys; the wool rooms are one storey with a lower roof pitch. One extra cottage in the corner beside the spawn, in the same style; the seat search found almost nowhere else on the hub where a house fits.
- **Dressing:** four earth paths drawn over the 45° stairs (spawn to the lip down each stair, and to each wool room). One large oak in the empty hub corner and one small oak in front of the hole. Light ground cover over the whole board: 18% coverage, 5% tall grass. Nothing on the frontline, and no buildings or trees on the holm.

**What cost time.**

- No route adds a tree or house recipe on its own, so styles and props went in as one whole-layout `PUT`.
- `pitch` counts upward as negative, so the first views looked at the sky.
- Two path mixes failed on screen: hardened clay reads as large salmon patches, and podzol only works as a small share.
- A floating 3×3×3 wool cube stands about 26 blocks above each wool room, at y42–44. It was there on the grey board and isn't in `map.xml`, so it was left alone.

**For the author.**

1. "Room for houses in front": does that mean the lower frontline below the scarp, or the crest above it? Both have room for a house, but either would change the fight, so none was placed.
2. Should the holm carry a mill on each bank, which the name suggests? That would put cover and high ground on the crossing.
3. The `orchard-east` mark suggests an orchard, but the only open ground there is inside the orange wall. Do you want trees there?
4. The river runs out through both ends of the holm, and the dressing pass reports a three-block carve (`DR-BANK`). Is that intended?

### Clasp (`opus55-clasp`, from collab-1)

**Clasp is finished.** It is painted, set in a cold taiga biome, its rooms are timber lodges, and it is dressed. The ground did not move: after every drive, the heightmap and slopes reads came back byte-identical to the author's run (8635 walked, 422 scrambled, 236 barrier). The final drive declined nothing, pre-flight said `export gate OPEN`, the export raised no warnings, and 0.4% of the board is dead.

**Decided.**

- **Ground:** biome Cold taiga (30). The ground is snow. On the slope axis it turns to stone, andesite and 20% cobble at 33°, read off `incline` (58% of the ground is under 10°). The coast walls are the same rock. A third band of bare earth between snow and rock outlined every hollow and canyon in brown contour lines, so it was removed.
- **Grove patch:** snow will not root a tree (`DR-ROOT` refused 6655 cells), so a forest-floor patch (grass under podzol) sits on the hub's back edge east of the back wool, on ground no route crosses.
- **Buildings:** one timber language: spruce plank infill, upright dark-oak posts, courses of laid dark-oak log, a dark-oak roof, light-blue glass panes as the accent. The wool rooms are one storey; the spawn is a two-storey hall with beam ends. The clamp room keeps a door at each end, so the author's run-through still works.
- **Dressing, per side:** one tall and one small spruce, an andesite boulder, ferns only in the grove; paths 3 wide of coarse dirt, podzol and spruce planks from the spawn to the hub, the back wall, the west flight and the clamp's back door; the three relief stairs laid in stone brick.

**What cost time.**

- Brown overload: the earth band plus six paths read as a web from above, which took two rebuilds to fix.
- The storeys list meaning the whole building.
- There is no snow-layer block, so the look is snow blocks rather than snow over grass.
- The eye camera lands inside tree crowns at close range.
- Style previews come back as 72-pixel images.

**For the author.**

1. Should trees or cover go in the clamp? It was left bare, because it is where you said attackers group and shoot at the back wall.
2. Should the two neutral islands stay bare snow, or carry a small structure?
3. The clamp's back door opens about four blocks above the hollow floor, so arriving from the back approach is a scramble. Is that intended?
4. Only two trees a side: enough taiga, or should the corner hill by the spawn carry a stand, even though the walk to the back wool crosses it?

### Redcut (`opus55-redcut`, from collab-1)

**Redcut is painted, has its Mesa biome, has both room shells bound and is dressed.** Pre-flight reads `export gate OPEN`, coverage is 1.0% dead, `findings` is empty, and none of the writes came back with warnings. The ground, plan, intent and relief were left alone. The export was not run.

**Decided.**

- **Ground:** one theme, `mesa`, over the whole board, with the biome set to Mesa (37). Surface by slope angle, cut at 30° and 48° (incline read 71% of the ground at 0–9°, 5% at 20–29° and 3% at 40° or steeper). Flat ground is an orange set (red sand, red sandstone, orange stained clay, a third each); a noise lays dirt/coarse-dirt patches ringed with hardened clay into it, and hardened-clay patches apart from them. Shoulders are hardened clay with orange; faces are strata. The wall and fill are one set of clay strata pinned to world height, so every cliff and void face shows the same beds. The rim is off.
- **Buildings:** a fork of `darkwood`: dark oak log posts, beams and a laid-log course, spruce plank infill, a stone-brick base course, and a dark-oak slab gable roof. An andesite plate and a four-grey floor. No footing. The spawn has two storeys and the wool house one, so they read as the same builder at two sizes. The built family (dark timber and grey stone) is deliberately outside the orange ground's tones.
- **Dressing:** two granite, polished granite and brick paths per side (spawn door → butte → west stair → along the bench → east stair → lip, and spawn → down the slope → wool-room entry); the path is the one material on both stairs. Two acacias per side, each on a worn dirt patch because `DR-ROOT` refuses a trunk on sand or clay. No boulders and no flora: there is no grass for flora, and no rock that is not either grey or the ground's own set.

**What cost time.**

- The `render/eye` pitch sign: negative looks up. The listed `wool-0` view points at the floating wool marker, so it draws sky.
- The band `ending` is `handOver`, not `hold` (a 400).
- The wool path broke at the room's keep-out band round the entry, so it now stops at the entry.
- `render/eye?format=text` does not state which way the pitch points.

**For the author.**

1. Is a dark-timber outpost right for a mesa, or should the buildings be warmer (acacia or sandstone)?
2. Are acacias on the butte wanted at all, and is the one in front of the hole in the way of play?
3. Should the rim of the butte top carry grass, like a vanilla forested mesa plateau?
4. Both wools have `monuments: []` in the intent. Is that deliberate?

### Lymedown (`opus55-lymedown`, from collab-1)

**Lymedown's paint, biome, both room buildings and dressing are finished.** The ground is untouched: the heightmap after the work matches the one saved first, character for character. Pre-flight's export gate is OPEN, the dressing places 17 props and declines none, and the only finding is FR9, which the author already ruled not valid on this board. The export was not run.

**Decided.**

- **Biome:** Extreme hills: its grass (#8ab689) is a muted grey-green, paler than Plains.
- **Ground:** one theme, `downs`: grass over one course of dirt and coarse dirt, then chalk (diorite, polished diorite, clay). The cliffs over the void are chalk with a dark flint course at y5 and y10; that white cliff is what makes the board pale. Turf runs to 30°; chalk shows only on true faces (30°+, under 2% of the ground). A cut at 20–30° put single white specks along every one-block terrace step, so it was dropped.
- **Buildings:** one style for spawn and wool, forked from `cottage`: flint walls between a brick plinth and a brick band under the eaves, brick corners, a brick floor, a hay-bale thatch gable, no footing. Grey and brick against white and green, so they never read as ground.
- **Dressing:** chalk tracks from spawn → hub → a fork both ways round the dene → the 24-block front, and spawn → hub-t5's lip, hub → wall face, wall → wool door; the walks confirm players go that way. One beech-like oak on each down's crest, plus a hawthorn-sized oak in the hub's corner. Low flower cover over the whole board.

**What cost time.**

- Wall seams: a two-band height stack (chalk 4, flint 1, repeat) laid flint on every course above the first flint band instead of repeating; writing the bands out in full worked.
- Biome field: `PUT …/sketch/biome` accepted `{"biome":3}` with a 200 and no RQ3, and stored Plains. The field is `id`.
- Re-running the theme script restored a first-draft theme, which then went up with the dressing; `column` caught it.

**For the author.**

1. The beech's leaves hang over the west-branch track at y20–23, six blocks above the path at (-31, 41). Is a canopy over a fork route acceptable, or should the tree be smaller?
2. A three-block red and blue wool column stands at y37–39 above each wool room, with any room style. What is it for?
3. Chalk downs have thin soil, so one soil course was used where your rule for a meadow says two. Is that right?
4. Coverage now reads 2.4% dead, all in down corners one block from used ground, e.g. (-17, 85) and (-35, 27). The earlier run reported 0.0%.

### Sedgefall (`opus55-sedgefall`, from collab-1)

**Sedgefall is finished and the ground is untouched.** Layers, relief, setup, plan and intent are identical to how the painter found them, and the heightmap text matches. Pre-flight says `export gate OPEN`, the export answers 200 with no warnings, and the dressing pass placed 21 of 21 with nothing declined.

**Decided.**

- **Biome:** Swampland (6), so podzol reads as leaf litter.
- **Ground:** one theme, `fen`, banded on slope. Flat ground up to 30° is grass with five-block podzol patches over dirt; above 30° is peat, dirt and coarse dirt half and half. The body is stone and andesite with some cobble; the void-facing faces show peat over one clay course over rock. A first cut at 22° turned the bank's one-block treads brown, reading as tracks across the fen; at 30° the treads are grass and earth shows on the risers.
- **Buildings:** one fork of `darkwood` at two heights, so the three buildings read as a row. Two-storey spawn halls, one-storey wool sheds. Brick walls in a dark-oak frame with a laid-log beam course, dark-oak stair-lattice windows, an arched door and a hay-thatch gable. No footing. Ground olive, built brick and dark timber, thatch the accent.
- **Dressing** (red side authored, fanned onto blue): seven paths along the measured walks (spawn door, both fronts, over each wall to its wool) in coarse dirt, spruce planks and dirt at cell size 1 — a first podzol mix at cell size 2 read as tiles. One willow on the east flank of the bank at (11, 46), olives in the north corners at (-20, 81) and (8, 79). One sparse ferny ground cover over the whole board. Nothing on the lip, the wall approaches, the forecourts or the spawn. A willow in the north corner hung leaves over the back wall's end at (-12, 88), a way over the wall, so it became an olive.
- **No water:** the reed-pool dip sits against the coast at (-24..-12, 32), on the bridging brink.

**What cost time.**

- A map's tree recipes could only be sent as part of the whole layout through `PUT /sketch`; the painter sent the stored layout back with the dressing added and diffed it to prove the ground had not moved.
- `BandEnding` is `repeat` or `handOver`; `hold` was guessed first and got an RQ1.
- The blue half renders a brighter green than the red half, though the exported world is Swampland in all 58 chunks: vanilla 1.8 swamp grass switches between `#6a7039` and `#4c763c` by position. `GET /terrain/biomes` lists only the first colour.

**For the author.**

1. Should the reed pool hold shallow water even though it sits on the bridging edge?
2. Swamp grass comes out in two greens and one half happens to read greener. Keep Swampland, or change it?
3. Coverage reads 1.9% dead, in the far corners of the orange and light-blue forecourts at (-51, 61) and (48, -62). Not confirmed whether the paths are the cause.
4. Is thatch right for the accent, or would you rather a darker roof?

### Kelderfell (`opus55-kelderfell`, from dtm-terrain)

**Kelderfell is finished.** It stored at 200 with no warnings. The dressing pass placed 52 props (26 authored, each fanned onto its rot_180 image) and declined none. Pre-flight passes all four checks and ends `export gate OPEN`, and `GET /xml` answers 200 with no warnings. The export was not run. Only paint, biome, room style and dressing changed.

**Decided.**

- **Biome:** Extreme hills, a muted fell green.
- **Ground:** one theme, finished by angle. Grass over two dirt runs to 48°, then scree (stone, gravel, andesite) to 58°, then crag (andesite and stone, some cobble). Exposed faces get a stone wall with a vertical grain; the rim is off. Grass was cut at 48° rather than the skill's 30° because a 30–40° dirt band turned the fell's flanks brown.
- **Paths:** a solid track of gravel, andesite and stone, about four blocks wide, from the hall door through the pass to the monument and on to the strait, with a branch to the stair head and one to the farm. The south stair is laid in stone bricks, polished andesite and andesite; the ground round the monument is worn dirt and coarse dirt.
- **Tarn:** a pool at level 6 fills the tarn hollow, with a shingle bank.
- **Buildings:** one style, "steading": walls of white stained clay over a rubble plinth, dark oak posts, a slate roof of cyan clay, no footing. The spawn hall has a team-tint course. Behind the scarp stands a single farmhouse of two wings: a two-storey house and a one-storey byre.
- **Trees and rock:** small spruce, with birch at the water only. Pale diorite erratics at the scarp foot and on the fell, and a cairn on the knoll. Ground cover is low and heavy on fern.

**What cost time.**

- House placement: two separate buildings on the bench were declined for `DR-PASS` and `DR-DIG`; the two-wing version was then refused for `HJ4` until each wing stated its own ridge.
- The seats read counted the painter's own flora and strokes as claims, so it showed the whole bench as unseatable; it had to be asked again against a layout with no dressing.
- Boulders: `DR-TONE` complained that boulders cut from the ground's own rock were lumps. Granite looked like pink cubes, so diorite.
- A non-empty `storeys` list replaces `wall` on the ground floor, learned from a column read, not from a document.
- The studio's suggested view of the monument drew 99% sky.

**For the author.**

1. Should the tarn hold water? It sits on the flank approach to the monument.
2. Is a small spruce and birch wood on the south flank the right "forest on one side" for this monument?
3. Is the fell massif right as mostly bare crag? Its slopes are 50° and steeper, so a 48° grass cut cannot green it.
4. Does the pinkish white clay read as limewash to you, or would quartz be better?

### Twingill (`opus55-twingill`, from dtm-terrain)

**Twingill is finished.** It exports at 200 with no warnings, pre-flight reports the export gate OPEN, and the dressing pass places everything with 0 declines. The ground did not move: slopes still read 24 025 walked · 1 745 scrambled · 108 barrier, the same as before. The spawn walks to its monument, and to the north bridgehead, end to end.

**Decided.**

- **Biome:** Extreme hills (#8ab689), a muted fell green, because the names (gill, holm, knott, fell) are Lakeland.
- **Ground:** one theme, `fell`, banded by slope: up to 38° grass over dirt and coarse dirt; 38–50° grass with rock showing through in patches of about a quarter; above 50° bare rock (stone and andesite, cobble 20%), with the same rock in the cliff faces. The cuts come from the incline read (21% of the ground under 10°, 21% at 40° or steeper).
- **Buildings:** a whitewashed farmhouse (quartz) with dark-oak posts, beams and a laid-log course, and a dark-oak slab roof. The spawn hall is the two-storey version; a one-storey barn in the same style stands at the dale head, so they read as one farmstead.
- **Monument surroundings:** a stone-flagged court across the terrace under the floating monument, joining two paved paths: spawn → monument → south lip, and spawn → north lip over the holm — two bridgeheads.
- **Composition, from `approaches.md`:** the monument stands in the open, with a small oak-and-birch wood to its south-east (outside the clearance), the south fell beside it, and the farmstead behind.
- **Other dressing:** oak and birch only, 11 trees a side, on the edges of the dale, in the coombes and round the farm; four granite erratics; light ground cover over the whole board (22%, ferns 45%, tall grass 4%); eight small stream pools, each on a flat stretch of the gill.

**What cost time.**

- Water on the falling gill: a stream carves down to its lowest point, so the gill cannot hold a continuous stream. Pools were the answer, but four lost water at their lower ends and had to be shortened.
- Grey boulders were flagged as "the ground standing up" because the fell's rock is grey. Granite passes, so the grey rock and the summit cairns were dropped.
- Two theme refusals cost a round each: a one-block pattern period, and a band-ending word that does not exist.
- Three trees landed on rock-painted slopes and had to be moved.
- The first path (coarse dirt, dirt and gravel) came out as blocky patches of two colliding tones.

**For the author.**

1. Do the gill's pools belong in the dressing, or are they a change to the ground? They cut a block or so into the gill bed.
2. Is the south fell's face too grey? Rock above 50° turns it into a crag.
3. Are pink granite erratics right for this board?
4. Should the wood south-east of the monument, which gives cover within about 12 blocks of it, stay?

### Scarbutte (`opus55-scarbutte`, from dtm-terrain)

**Scarbutte is finished.** It is painted, has a biome, its buildings are styled and it is dressed. Pre-flight reads OPEN, and the dressing pass places all 31 props (both orbit images) with none declined. The ground, outline, relief, plan and intent were not touched.

**Decided.**

- **Ground.** One theme, `mesa`, with biome Mesa plateau F (grass tint #90814d) so the grass reads as dry scrub. The surface is banded by slope, cut against `incline`, which has a trough at 30–39°.
- Under 32°: grass over one dirt, then hardened clay, a thin soil so the taller risers show clay. 32–44°: red sand, hardened clay and red sandstone, a third each. Above 44°: terracotta strata by height. The same strata sit in the wall bucket, so the island's outer cliffs are banded too, and there is no rim.
- **Buildings.** Grey stone and dark oak, so they read against the warm ground, with the team colour as a wool band. The spawn is a gabled hall with dark-oak posts, a laid-log course and a floor laid from four stones.
- One two-storey lookout stands at (−81..−76, 2..7), watching the canyon crossing, 15+ blocks from the monument. A gatehouse at the pass was dropped: no site there clears both `DR-PASS` and `DR-SLOPE`.
- **Dressing.** A podzol, coarse-dirt and dirt road runs spawn door → pass → monument, and a second runs monument → crossing → lip. A red-sand wash lies on the two canyon-slot reaches.
- A grove of three acacias and one olive sits on the rim foot by the pan, the monument's "forest" side, and two acacias stand on the tableland. Four grey boulders stand at butte feet. Ground cover has coverage 0.33 and tallShare 0.03.

**What cost time.**

- **Height bands.** A height band stack does not repeat: with `ending: repeat` the last band held above y24, so every cliff came out white. I wrote the strata out explicitly up to y65.
- **A 500 on the dressing read.** A storey `deck` given as a band stack returned a 500 (`RQ2`) on the dressing read, with no field named. `preview-snapshot` gave the real error, and `deck` turned out to be a plain material.
- **Two instructions disagree.** Noise ground patches came out as rectangles, so the flats are plain grass. The first boulders were cut from the cliff clay, which `DR-TONE` flagged against the author's ruling ("a boulder in the ground's own set is a lump").
- **Flora coverage is nonlinear.** 0.14 covered 116 cells, 0.30 covered 1,461 and 0.45 covered 6,061.

**For the author.**

1. Grey erratics or terracotta talus? Talus is the true geology here; `DR-TONE` and your ruling say grey.
2. Should the canyon floor be a red-sand wash, or grass like the bench?
3. Coverage still reads 54.5% dead ground, with four ~3,000-cell patches on the bench flanks, centred near (−66, −43) and (−64, 42) and at their mirror images. Dressing cannot fix that without changing the ground.
4. The rim at (−86, 0) is a 4-block one-way drop. Defenders walk back to spawn only through the pass at (−100, −42). Is that intended?

### Cinderhowe (`opus55-cinderhowe`, from dtm-terrain)

**Cinderhowe is finished.** It is painted, housed and dressed, and the ground is exactly as it was: the heightmap text matches the one read before the first write, with 32,338 ground cells both times. Pre-flight answers "export gate OPEN", and the dressing pass places all 34 props with none declined.

**Decided.**

- **Paint, three places.** *Heath* (the map default): grass to 46°, then stone and andesite with cobblestone at one noise end. The cut faces carry volcanic strata of stone and andesite with thin grey- and black-clay beds.
- *Ash*, over the caldera and the three parasitic cones: grey stained clay with black and brown clay patches, up to 58°.
- *Cinder*, over the crater floor round the monument and the lava tongue out of the east breach: black clay with coal-block patches. The cuts came from `incline`; at 42° and then 50° the crater bowl came out light grey, like a quarry.
- **Biome.** I tried Mesa (the olives looked dead) and Swampland (the grass renders in two blotchy greens), and chose Extreme Hills: its sage grass and grey-green leaves suit a volcanic highland.
- **Buildings.** A destroy board has no wool rooms, so only the spawn hall: brick with spruce posts and a laid-log course, a team-tinted clay band under the eaves, a dark-oak gable with slabs, and a wide arched door. There is no footing. Brick keeps it out of both ground families.
- **Paths.** They come from `walk`, which showed players going through the crater. An axis path runs spawn → west breach → floor, a second runs floor → east breach → strait, and one flank path runs round each side of the rim. All four are laid in andesite, polished andesite and gravel.
- **Dressing.** Six dark volcanic bombs sit on the heath where attackers climb to the rim, never on the ash. Five olives (corpus `r10`) stand beside the spawn and one by the south path. One low ground-cover pass covers the red half.

**What cost time.**

- `ending: repeat` holds the last band rather than cycling the stack. A column showed twelve blocks of black clay, so the strata had to be written out band by band.
- The NW cone's patch overshot the coast. It added 54 ground cells and re-solved the relief, and the store answered 200; only the heightmap diff caught it. I clipped every patch inside the built coast.
- Two suggested views are unusable: `destroyable-0` frames the sky marker at y53–55. A hand-placed `from` inside a rim puts the eye inside the ground.
- One olive's crown ran into a cone flank (`DR-CUT`), so I removed it.

**For the author.**

1. Should the crater's steepest inner faces stay bare grey rock under ash, or be ash to the top?
2. Is a stylised black rock (coal block and black clay) right for volcanic bombs, or should the boulder be the board's own stone?
3. The paths read as bright grey lines from above. Are they too road-like for a volcanic heath?
