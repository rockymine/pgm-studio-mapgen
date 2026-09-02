# Mossgill — half of Millrace's box, a new layout, and the revamp's techniques stated from the start

`specs/fable-mossgill`, driven 2026-09-02. **130 × 120 blocks**, `rot_180`, 24 players, one destroyable a
team. Where Millrace is a walled canal between two masses with an island in the middle, Mossgill is **one
moor split by a beck**: a gill cut eight courses into the ground on a shallow diagonal through the centre,
crossed once by a plank bridge between two quays. Each team spawns on a crag in its own corner at 27, walks
down a graded brow at 22 onto an apron at 20 where its monument stands in a low sheepfold, and the moor falls
from there to the beck at 6. Nothing here was drawn in the browser: the plan is five rectangles, and the rest
is a finish over what they compile to.

It is the board `review/fable-millrace-revamp.md` was written to make possible. Every technique the hand
revamp of Millrace measured out is stated here at the outset rather than restated over an older build, and
every one of the corrections the two Millrace builds taught is in from the first drive.

## What it carries

| thing | how it is stated |
|---|---|
| the tiers | five plan pieces at four surfaces — crag 27, brow 22, apron 20, bank and shoulder 14 — each an `area` mark drawn inside its piece so the solve grades a slope between them, and a `line` ramp down each seam the roads take |
| the beck | a `line` mark at 6 seven wide along `z = x / 8`, a `scarp` along its north lip (high 14, low 7, face 2, band 4) traced east to west so its shelf is the bank, whose image is the south lip, and a `water` channel two deep over it with a gravel-and-sand bank |
| the bed | a polygon the width of the gill at the bank's own height carrying the `bed` theme and no geometry of its own — the smaller shape wins a contested cell's paint, so the beck floor is coarse dirt, spruce plank, gravel and prismarine without a shape being cut for it |
| the sheepfold | two `path` arcs of quay wall at radius six round the monument, open east and west, `height_mode: level` three over a floor at 19 so they stand two courses proud of the apron |
| the quays | one `path` along the beck's north lip at the crossing, its image the south quay, a course over the bank |
| the bridge | a layer of its own, `spans`: a spruce deck at 15 seven wide across the gill and two dark-oak rails, a group that does not mirror because it stands on the axis |
| the stone body | one `cell` material, nine across and five tall, whose palette is four `turbulence` mixes of the six stones seven across and four tall and two smaller `cell` fields five across — the Millrace revamp's `#vor[7]` of `#turb[5]` as one nested volume |
| the earth | three courses under every surface: a `layered` depth stack, the top mix one course over a `noise` of coarse dirt, spruce plank and dirt with a rise of eight |
| the trees | eleven copied recipes a side out of `showcase/tree-showcase`, each a body of its own — the tall acacia-and-birch conifers on the brow, the dense oaks on the apron's west end, the bank and the shoulder, the small conifers on the bank |
| the roads | three `stroke` props in granite, polished granite and jungle plank, `rough`, following the two ramps and the bank |
| the grass | three `flora` areas at coverage 0.88, half of it fern |
| the biome | a `cell` field over forest, jungle, beach and birch forest, twelve blocks a cell |

## What the plan tier says about a board this small

`POST /plan/evaluate` scores it **0.50, valid**, with two soft goal terms and nothing hard. The three goal
bands cannot all hold at once on half a box: with the doors 134 blocks apart, `GO1` wants the goal 27–34
blocks from its own door, `GO4` at least 40, and `GO3` wants the two goals at least 85 apart, which is at most
24 from the door. The plan tier walks the pieces flat — the gill and the one bridge lengthen no route it
measures — so the goal stands 33 from its own door, `GO1` in band at 3.4, `GO4` seven short and `GO3` seven
short, and the built board decides the walk: there, every enemy route goes by the bridge.
`GENERATION-NOTES.md` carries the arithmetic.

`EL1` and `SP8` name the seams between the tiers as steps a player cannot walk — which is what the plan's flat
rectangles are, and what the two ramp marks in the relief exist to grade.

## What the build says

The drive is `python3 tools/drive.py specs/fable-mossgill "Mossgill" --out maps/fable-mossgill`, and it goes
through in one pass. The plan tier scores the board 0.50 and calls it valid, refusing nothing hard: `GO3` reads
the goals 78 apart against its 85 and `GO4` the goal 33 from its spawn against its 40, both the arithmetic
above, and `EL1` and `SP8` name the flat seams (brow–apron 2, apron–bank 6, crag–brow 5, crag–apron 7) that
the two ramp marks grade. The compiled map stores 9,021 cells. The relief read answers **6 to 27** over the
group, 21 blocks of range, and counts **268** barrier steps and no cliff: the two faces of the gill, eight
blocks over a face of two, and nothing else, with every north–south row crossed on foot and thirteen of the
fourteen east–west rows only descended, which is the gill doing what it was drawn to do. The gill has an exit
at each end where the scarp stops short of the map's edge and the bed grades up onto the far bank over six
blocks, so a player who drops into the beck walks sixty blocks to climb out on the enemy's side rather than
being kept.

The dressing pass places **42** props a side and declines **none**: eleven copied trees, one shelf boulder,
the bothy and the barn, three roads, three meadows and the beck. It complains twice, `WX11`, that the bothy's
foundation shows a three-block face at `(−53, −40)`, which is the bench's north edge against the spawn hall's
own footing; nobody walks between them. The export gate is **open**: the intent generates two teams, seven
regions and four apply rules, the codec round-trips with no field lost, both spawns and both monuments stand on
solid ground, and the spawn-to-objective chain is connected across the built geometry.

Coverage reads **26.1% dead** of 8,893 cells — worse than Millrace's 17.8%, and the two patches that make it
are the ends of the bank beyond the shoulder, 921 cells at `(45, 5)` and 905 at `(−48, −7)`, one block from
used ground: the strip east of the barn where the gill runs along the footprint's edge, and its image. They are
the flank a player takes out of the gill, which coverage cannot see because nothing it counts as a journey
passes there, and on a board this small there is no objective left to put in them. The three small patches
are the crag's back corner and the two moor corners behind the aprons.

The body probes the way the revamp does: runs of one material down a column in the stone are **40%** one
block, 22% two, 16% three, a mean of 2.6 — a blob on every cut, where the first Millrace build read as
stripes and the second as columns. The earth, three courses deep with a rise of eight, is one material in 69%
of its columns and two in 30%, so the coarse-dirt-and-plank mix shows across the ground rather than down it.
Every leaf of the twenty-two copied trees is written no-decay, and each stands on its foot's column where it
was clicked.

## What Millrace taught, applied

Seven things, each a line in `build.py` that would not be there without the Millrace diff.

**A pattern is a plane until it states a `rise`, and a cell as tall as it is wide is a column.** The stone
body's cells are nine across and five tall, the turbulences inside them seven across and four tall, the
earth's noise eight tall over three courses. Millrace's first build had none of these and its cliffs were
striped floor to sky; its second had cells seven and seven and still read as columns on a cut.

**An override add standing in ground keeps the ground under it** (`TS77`), so the sheepfold arcs and the quays
state a floor a few courses under the ground they stand in and leave no shaft to bedrock beneath.

**A theme is scoped by shape, and the smaller shape wins.** The beck's bed is a polygon at the bank's own
height with the bed theme and nothing else, which is a cheaper statement than a relief mark carrying a theme
would be, and one the sketch already had.

**A copied tree is a recipe and a click.** Eleven placements a side each name one of the sixteen bodies the
author planted in Millrace, and each stands where its foot's column is — a slope clips a crown by a block, the
way it does the author's.

**A prop keeps 21 blocks off a goal and off a spawn** (`OB19`, `DR-KEEP`), so the fold has no tree inside it
and the crag's trees stand on its outer edge; and **a house's claim reaches a block past its footprint**, so
the bothy and the barn stand nine blocks apart rather than eight.

**A made thing over a goal reads as inside it** (`TS79`), so this board carries no beacon frames.

**A scarp's shelf is on the +z hand of the direction its lip is traced**, so the beck's north lip is traced east
to west. Traced the other way the bank north of the beck solved at 8 against its 14 and the relief read counted
418 barrier steps; reversed, 268, which is the two faces of the gill and nothing else.

## What to look at

`GET /map/fable-mossgill/column?at=-29,-28` reads the monument over the apron's earth and body;
`at=-31,-22` the fold's south arc; `at=0,0` the bridge deck over the beck; `at=-55,-50` the spawn hall's
floor on the crag; `at=-8,-6` the north quay standing a course over the bank with the gill beyond it.
`render/section?axis=z&at=-30&from=-62&to=0` cuts the crag, the brow, the apron and the gill in one picture,
which is the picture the board was composed for.
