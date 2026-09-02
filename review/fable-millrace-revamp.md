# Millrace, revamped by hand and restated in the studio — the measured diff, and every gap

`maps/rockymine-ruediger-millrace` is `maps/opus5-millrace` after five hours of WorldEdit and Arceon by the
author and Ruediger_LP, and it is the first board in this repository that a person finished rather than the
studio. `review/rockymine-ruediger-millrace.md` is their own account with the commands. This is the other
half: the two worlds read block by block against each other and against the original's provenance sidecar,
what each command turned out to have done, which of it the studio can already state, and what it cannot.
`maps/fable-millrace-revamp` is the restatement — the same layout, driven again with the author's palette,
their trees and their builds — and the last section is what that build says about the gaps.

**The one number that makes the diff readable: 29,954 of 35,610 columns keep their surface height exactly.**
The terrain, the water, the canal walls, the bridges, the cairn walls and the boulders are the studio's,
unmoved, and the hand work sits on and inside them. That is why a provenance-keyed diff works at all, and it
is the property the author was happiest about.

## The studio reproduces its own map

Before the diff, the control: `specs/opus5-millrace` driven again through today's studio, weeks of changes
later, against the committed world.

| | blocks |
|---|---|
| committed `maps/opus5-millrace` | 1,060,630 |
| rebuilt from its documents | 1,062,420 |
| cells that differ | **4,020 (0.4%)** |

Every differing cell is one of three things, and none is terrain: **trees** — the grower changed since
(`tree-corpus.md` made its findings law), so every grown crown is a different crown; **608 masonry cells** at
the two spawn terraces (`x −100..−90, z 100..110` and the mirror) where the spawn hall's shell now lays stone
brick where the older stamp left stone; and **448 house cells** at the same two terraces, the crofts' walls
and roofs under the building programme that landed since. Not one column of ground, water, wall, bridge,
boulder or cairn moved. The determinism the specs promise is real, and it is what lets the rest of this
document be read as a statement about the hand work rather than about drift.

## What the hand work did, by provenance and depth

Both worlds were read into one grid, every column classed by the original's `provenance.json` (`ground`,
`prop`, `structure`, `made`), and every block of a column whose surface did not move filed by its depth under
that surface. What each original block became, on ground columns:

| where | original | became |
|---|---|---|
| surface | grass `2:0` (5,885) | grass 42%, coarse dirt 25%, **polished granite 15%**, dirt 8%, granite 5%, jungle planks 4%, podzol 1% |
| surface | dirt `3:0` (3,464) | coarse 40%, dirt 17%, grass 15%, polished granite 14%, jungle planks 8%, podzol 4% |
| 1–3 under | stone `1:0` (7,279 at one course) | **coarse dirt 60%, spruce planks 25%, dirt 15%** — the same three at every one of the three courses |
| 4 and deeper | stone `1:0` (164,175 at 7+) | andesite 24%, stone 21%, polished andesite 20%, mossy cobble 15%, **emerald ore 13%**, **cyan clay 7%**, prismarine <1% |
| 4 and deeper | cobble `4:0` (59,818) | the same six, in the same shares — cobble itself is gone: 165,809 blocks to 890 |
| canal wall | stone brick `98:x` (19,722) | **double stone slab 35%, light-grey wool 11%, smooth double slab 11%**, stone brick 19%, the stone body 17% — on the faces a player sees, double slab 53%, wool 18%, smooth 17% |
| bridge masonry (28,154) · terrace masonry (114,130) | stone brick | **unchanged** |
| race bed, under the water (6,740) | dirt 60% / coarse 16% | coarse 28%, spruce planks 26%, gravel 14%, mossy cobble 9%, andesite 8%, prismarine 8% |
| boulders (`prop` surface, 928 mossy cobble) | mossy cobble | mossy 43%, **prismarine 36%**, cobble 8%, emerald ore 6%, andesite 6% |
| house roofs (`structure` surface, 412 brick) | brick | brick 36%, **brick stairs 60%** |

Three readings follow from the table, and each is a command in the author's list.

**The stone body is a voronoi of turbulences, and the placeholders were how WorldEdit expressed nesting.**
`//r 22 #vor[7][35,22]` twice, `//r 35 #vor[7][35,22]`, then `#vor[5]` over the remainder, `#turb[5]` inside
two of the wool classes, and six replaces of the wool placeholders by the six stones. Read off the world, the
body is cells about seven blocks across, each one a two- or three-stone turbulent mix, and the six stones
fall in the shares above. The studio states that as **one material**: a `cell` whose palette is `turbulence`
materials, each of those a two-stone mix. The placeholder dance is the nesting the studio's materials already
have. Of the 76,582 emerald ore and 50,880 cyan clay, 2,506 and 2,420 have a face to air or water: the body
shows on every cut — the canal, the quarry, the cliffs — at about three per cent of what is exposed.

**The earth is three courses, and exactly three.** `//replace #below[2,3][3] #frac[4][3,3:1,5:1]` put coarse
dirt, spruce planks and dirt under every grass and dirt block to a depth of three, and the depth profile
confirms it: courses one to three under the surface are the earth mix on 84% of ground columns, course four is
the stone body. The studio's `layered` surface says the same thing as a stack: the top mix one course, the
earth three, then the fill. `PT1` refuses a surfacing block deeper than a course, which this respects.

**The canal wall is the one masonry that changed, and it changed only where it is seen.** The pattern
`#cell[4][43:8,43,35:8]` is on the two lip walls and nowhere else; the viaduct, the holm bridge, the terrace
and the cairn walls keep their stone brick. Stated as a `quay` theme on the three wall shapes and `masonry`
on the rest, which is what scoping a theme to a shape is for.

## What was added, what was removed

Every block one world has and the other does not, clustered into things (26-connected, six blocks or more):
244 things added, 129 removed. The large ones, with their coordinates:

| added | blocks | where | what |
|---|---|---|---|
| fill under the north canal wall | 6,870 ×2 | `x −125..−16, y 0..19, z 46..76` | cracked stone brick and the stone body |
| fill under the spawn stair | 4,608 ×2 | `x −97..−86, y 0..23, z 80..95` | cracked stone brick, 192 columns × 24 |
| fill under the south canal wall | 2,724 ×2 | `x −125..−16, y 0..11, z 29..43` | the same |
| fill under the three cairn walls | 1,368 + 1,248 ×2 each | `x −111..−105, y 0..23, z 3..29` and two more arcs | the same |
| the statue | 5,811 ×2 | `x −60..−30, y 31..71, z −74..−39` | red clay 1,491, grey wool 706, red wool 639, cyan clay 348, light-grey wool 300, smooth double slab 177, obsidian 48, **diamond block 19**; blue clay and wool on the other half |
| the balloon | 3,120 | `x −15..14, y 67..121, z −15..14` | red, white and blue wool, acacia planks, black wool; the observer's platform at y70 inside its basket |
| the tug | 1,383 | `x −112..−85, y 24..42, z 49..63` | black wool hull 628, cyan and red clay, slabs, gold block 30 |
| the spawn quarter | 2,220 | `x −111..−62, y 41..65, z 94..122` | two houses moved back and west, a third built, iron blocks 138, bookshelves, cobweb chimneys, flower pots, a wall of slabs round the terrace |
| beacon frames | 72 ×4 | `x −92..−88, y 72..80, z 16..20` and the three others | fence posts, a cobble-wall collar, iron block base, a beacon under a red pane |
| the wool dress | 12 ×2 | `x −91..−89, y 37..39, z 17..19` | a cross of red and grey wool round each obsidian pillar, inside its region and not obsidian |
| tall grass and ferns | 3,090 | every grass-topped column | 3,090 plants on 3,289 grass blocks: fern 50%, tall grass 47% |
| paths | 2,700 cells | `x −111..110, z −113..112` | granite, polished granite and jungle planks laid with a boulder brush |

| removed | blocks | where | what |
|---|---|---|---|
| the diorite statue | 1,094 ×2 | `x −36..−25, y 34..62, z 91..100` | diorite 864, stone brick |
| the lighter | 187 + 64 + 29 ×2 | `x −111..−103, y 27..47, z 51..62` | white wool sail, spruce deck |
| the two crofts on the terrace | 347 + 112 ×2 | `x −78..−65, z 94..107` and `x −79..−72, z 111..120` | rebuilt elsewhere on the terrace |
| every grown tree | 36 bodies | the eighteen `oak-*` and `fir-*` and their images | replaced in place |
| the observer platform | 52 | `(−3..2, 24..25, −3..2)` | moved into the balloon at y70 |
| a stray pillar | 40 | `(−119, 0..39, 7)` | one column of stone and cobble standing alone; a rasterizer speck |

**The four biggest additions are not decoration.** They are fills under the canal walls, the spawn stair and
the cairn walls — 25,000 blocks — where the studio's build left the column void from the wall's floor down to
bedrock. An override add overwrote the column it landed on, floor included, so a wall stated at `floor: 12`
over a bed at 17 stood on nothing. The author called it "holes in the bottom of the world" and filled them by
hand. `pgm-studio` now keeps the ground under an override add that stands in it (`TS77`), and the restated
board carries no fill because it needs none.

## The trees

The revamp planted sixteen of the author's showcase trees, and every planted body was matched against the
75 of `showcase/tree-showcase` by its leaf set under the eight symmetries of the square:

| planted at | body | showcase tree | turned | match |
|---|---|---|---|---|
| `(−4, 32, −107)` | 773 blocks, 61 logs | dense oak row z −75, foot `(154, 2, −75)` | none | 1.00 |
| `(53, 39, −121)` | 679, 58 | the same row, foot `(134, 2, −75)` | rot 270 | 1.00 |
| `(−64, 29, 70)` | 731, 62 | foot `(28, 2, −75)` | rot 270 | 1.00 |
| `(−107, 31, 84)` | 468, 39 | foot `(7, 2, −75)` | rot 90 | 0.99 |
| `(−52, 30, −67)` | 258, 30 | tall conifer row z −242, foot `(113, 1, −242)` | rot 270 | 1.00 |
| `(−100, 36, −7)` | 259, 30 | the same tree | rot 90 | 1.00 |
| `(−66, 31, −43)` | 74, 15 | small conifer row z −368, foot `(7, 1, −368)` | none | 1.00 |
| `(−115, 37, 7)` | 59, 15 | foot `(29, 1, −368)` | rot 180 | 1.00 |

Forty-two standalone bodies, every one of them a showcase tree at 0.99 or better, and two groves where three
oaks grew into one body and match only as a whole. The trees come from three rows: the dense oaks at z −75
(the row with the most and the tightest leaves), four of the eight tall acacia-and-birch conifers at z −242,
and four of the five small ones at z −368. The oaks carry 4 to 13 more logs than their showcase originals —
the trunks extended down to meet the ground where a paste at a fixed height left them short — and each
stands within a block or three of the grown tree it replaced. The leaf data differ only in the game's check
bit.

That is the case for the tree form the studio now has. A **copied** recipe carries the body block for block
and is placed like any other tree: seated on its foot's column, turned round the symmetry with its stairs and
log axes turned, its leaves written no-decay, its footprint claimed and its standoff from a road kept. It is
not a made thing on layers — a lacy crown is many runs per column, an oak would cost ten layers, and a tree
is a click and a recipe rather than a drawing. `pgm-studio/tools/seed-trees.cs` cut all 74 standing trees of
the showcase into the library; `specs/fable-millrace-revamp/trees.json` is the three rows, twenty-two trees,
keyed as the placements name them, and the board plants seventeen of them.

## The commands, and what the studio says instead

| the command | what it did | in the studio |
|---|---|---|
| `//r 1,48,4,168,129,98 22` … six `#vor`/`#turb` passes … `//r hand 129` × 6 | the stone body as cells of turbulent two-stone mixes | one `cell` material whose palette is `turbulence` materials, each with a `rise` so the field is a volume — the `BODY` of `specs/fable-millrace-revamp/build.py`. WorldEdit's patterns are volumes by nature; the studio's are planes until told (`TP15`) |
| `//replace #below[2,3][3] #frac[4][3,3:1,5:1]` | three courses of earth under every soil block | a `layered` surface, depth 4: the top mix one course over the earth mix three |
| `//gmask 2&#below[air][1]` · `#frac[4][2,2,2,3,3:1,3:2]` | the grass surface mixed with dirt and podzol | the top band of the `moor` theme, a `noise` at scale 4 |
| `//gmask 3&#below[air][1]` · `#frac[4][3,3:1,3:2]` twice | the dirt surface, then grass specks | the top band of `wold` |
| `//replace 3 #frac[4][3,3:1,5:1,13,1:5]` | the race bed | the `bed` theme on the basin shape `s0` |
| `//replace #cell[4][43:8,43,35:8]` on the lips | the canal wall | the `quay` theme on `wall-s`, `wall-n-w`, `wall-n-e` |
| `//brush boulder 22 7,9 …` · `//replace 22 #frac[3][4,48,129,168]` | new rocks in the race bed, and every rock re-laid | a boulder recipe whose `rock` is a `noise` of the four; **the new rocks in the race are refused** (below) |
| `//brush boulder 41 3,4 …` · `#frac[4][1:1,1:2,5:3]` | paths laid as blobs of granite and jungle planks | `stroke` props with that `noise` as `pave`, `rough` edge, `route: true` |
| `//gmask 0&#above[2][1]` · `//s #frac[4][0,31:1,31:2,175:3]` | ferns and tall grass on 94% of grass | `flora` props over the three grounds at coverage 0.92, fern share 0.5 |
| `//replace #vor[8][[#biome[4],#biome[21]],[#cell[3][…]]]` | four biomes in cells | the layout's `biome`: a `cell` field over `[4, 21, 16, 4, 27]` — one level of nesting where the command has two |
| paste × 36, rotated | the sixteen showcase trees | `copied` tree recipes, placed at the same feet |
| copy from Automaton, recolour, diamond | the statue, red on one island and blue on the other | two made things, `statue-red` and `statue-blue`, neither mirroring — a fanned image cannot change colour |
| copy from Slipway, raise to y70, cage | the balloon holding the observer spawn | one made thing on the centre with the observer at `(0, 70, 0)`; the six-by-six its platform stamps is cut out of the basket |
| built by hand | the tug | one made thing, mirroring |
| built by hand | the beacon frames | two made things at absolute floors, mirroring |

## What the studio cannot state, measured on the restated build

Each of these was tried, and the line says what happened.

1. **A rock in the race.** Four boulders stated in the bed: `race-rock-1` at `(−110, 55)` refused `DR-CLAIM`
   by the channel `race-water`, `race-rock-2` at `(−70, 52)` refused `DR-KEEP` by the quay wall's band, and
   the other two the same way. A water prop claims every column of its bed and a wall keeps its band clear,
   so nothing stands in the water. The author brushed about twenty rocks into the bed; the studio plants none.
2. **A boulder's rock is one material for all its faces**, so the author's mossy-prismarine-emerald mix is
   stated, but the moss flag then lays moss over it again on the sky-lit faces.
3. **The wool dress round each obsidian pillar.** Twelve blocks of wool in the destroyable's own region,
   inside its 2×2 footprint at `(−89, 18)`. A made thing there is ground under the monument stamp and lifts
   the pillar by its own height, and a prop declines in the goal's clearance (`OB19`). There is no decoration
   a destroyable can wear; the pillar stands bare.
4. **A frame over a goal reads as inside it.** The beacon frames at y72–80 stand over the pillars at y37–40,
   and `SK18` names each of their seven layers as standing "in" the destroyable, twice, because the
   provenance it reads is per column and carries no course. Fourteen complaints, all of them wrong about a
   thing forty courses up.
5. **The spawn quarter's halls are over the cap.** The author's west hall is 13 × 23 and the back hall
   29 × 12; `HP3` holds a placed building to 192 covered cells, so the restated board carries a 12 × 13 croft,
   a 12 × 12 croft and a 16 × 10 hall. Their roofs are stepped in stairs, their chimneys are cobble walls under
   cobweb, their rooms are furnished, and the terrace is walled in slabs — none of which a `HouseStyle` states.
   `WX11` also says why the west croft could not stand where the author's does: at `x −110` its foundation
   would have filled forty courses of bedrock down the terrace's void face.
6. **A spawn protection is at most 20 × 30 (`ST10`).** The author protected the whole terrace, 50 × 31; the
   restated board protects the hall and the ground in front of it.
7. **Iron is a cube three blocks off the room, one per point.** The author's iron is a 23 × 17 region of iron
   blocks under a renewable rule; the studio places two cubes a side.
8. **Kits are nobody's** (`docs/tools/flow.md`). The pickaxe keeps its efficiency enchantment, there is no
   `iron-bulkcrafting` include, and the build ceiling is derived (73) rather than the author's 70.
9. **A two-level biome pattern is one level.** `#vor[8][…,[#cell[3][…]]]` nests a cell field inside a voronoi
   cell; the studio's `cell` biome is one field over one palette, so the four biomes fall in one cell size.
10. **An intent's authors carry names only.** The uuids in `intent.meta.authors` answer `RQ3`; they reach the
    `map.xml` through the load's own `authors` body, which the driver passes.
11. **The chimneys, the flower pots, the player heads, the crates, the slab wall round the terrace, the smooth
    slabs at every rise of the bridge and the path, the broken pieces of cairn wall round the front monument**
    are all dressing at a grain no prop has: a block on a block. They are the "alive" the author was after, and
    each is a placement of one to twelve blocks by hand. A made thing carries the tug at 1,383 blocks in 11
    layers and 405 shapes, which is the wrong tool for a flower pot.

And one that is not a gap but a cost: **a made thing lifted out of a world is dear in layers.** The statue is
8 layers and 402 shapes, the balloon 7 and 1,181, the tug 11 and 405, a beacon frame 7 and 63 — every colour
change in a column is a run, and every run is a layer. `SCULPTING-WITH-LAYERS.md` §6's material keyed on
absolute Y is what would make a lifted body cheap.

## What the restated board is

`specs/fable-millrace-revamp/build.py` reads `specs/opus5-millrace`'s own layout and intent, re-themes the
fifteen ground shapes, drops the diorite statue and the lighter, appends the six made things, states 49 props
over 27 recipes — sixteen copied trees, three boulders, two crofts — and patches the intent: 28 a side, the
observer at `(0, 70, 0)`, the protections and the iron, four authors. `python3 tools/drive.py
specs/fable-millrace-revamp "Millrace" --out maps/fable-millrace-revamp` builds it.

**What the build says.** The plan is stored under the current form; the layout stores at 200 with the two
complaints the original's rebuild carries (`SK10` the holm bridge driven into the wold's swell over 890
columns, `SK11` the race bed) and nothing new; the export gate is **open**; coverage reads **17.8% dead**
against the original's 20.1%, the five dead patches the same five — the two western cliffs at
`(−114, 39)` and `(112, −41)`, the two back corners, the island knoll. The dressing pass declines nothing on
the final drive, and the fourteen `SK18` complaints are the beacon frames, every one of them a false reading
forty courses over the goal (`TS79`).

Read back off `maps/fable-millrace-revamp/region`: every standalone copied tree is its showcase body block
for block (fourteen exact of the thirty-eight bodies, the rest merged into groves or clipped by a slope by a
block or two), every leaf carries the no-decay bit and none the check bit, the tug, the balloon and the beacon
frames stand at the coordinates they were cut from, the red statue is red and the blue one blue, and the
columns under the quay walls, the spawn stair and the cairn walls run to bedrock — the 3,664 columns with
nothing at y0 are the holm bridge over its strait, the balloon over the centre and the clouds' overhang, all
of them drawn over void. The stone body varies down a column with a mean run of three blocks of one stone
against the author's 3.7, and a face read across the north quay at `z 60` shows the same blobs of andesite,
mossy cobble and cyan clay the author's face does, wider than they are tall.


## What to look at

`GET /map/fable-millrace-revamp/column?at=-58,72` reads the moor from the grass down through three courses
of earth into the six-stone body; `at=-70,54` the quay wall in double slab and grey wool over the bed;
`at=-100,57` the tug's hull over the water; `at=0,70` the balloon's basket with the studio's platform in it;
`at=-50,-52` the red statue's footing and `at=50,52` the blue one's. `render/topdown?subject=made` draws
the six made things; `render/topdown?subject=foliage` plots every copied tree as the circle its own leaves
measure.
