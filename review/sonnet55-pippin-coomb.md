# Pippin Coomb — a cider valley on a chalk down, with an older thing under the yard

> A destroy board for two teams: the monument on an open shelf with the orchard terraces west, a hill east
> and the hamlet behind, a 24-to-32-block build zone over void the whole width, and a cellar under each
> yard that runs on into something older.

**In one sentence:** a late-summer cider-orchard valley in chalk downland, two farm hamlets facing each
other across a dry coomb, each with a cellar under its yard that breaks through into a barrow chamber, a
white horse cut into the down above it, and a bench under the old oak where you sit and watch the other side.

88 × 224 blocks, `mirror_z` about the origin (the image of block `z` is `−z−1`), base surface 34, y 0..58.
Two landmasses, 100 blocks of ground each, joined by a build zone 24 blocks across at the coomb and 32 at
the pulled notches of its rim. Slug `sonnet55-pippin-coomb`; the account of the run is
`reports/sonnet55-pippin-coomb.md`.

## How it is meant to play

**The monument stands exposed on a shelf at 32, 49 blocks of walk from its spawn and 165 from the enemy's.**
Attackers bridge 24 to 32 blocks of void from the lip, land on the apron at 24 under a chalk face, and climb
to the shelf through three kinds of ground: the orchard terraces to the west, the open slope between, and
Horse Hill to the east.

**The four approaches the gameplay account names are all on the board.** Around is the orchard, two rows
of apple trees on lynchets with a track through them. Above is Horse Hill, six blocks over the yard with a
cairn on it. Through is the hamlet, two houses and a barn. Below is the cellar: its ramp comes off the lane
behind the monument and the rooms run east under the yard.

**The undercroft is a sanctum, not an approach, and that is a decision I could not check.** It opens twenty
blocks behind the monument and ends in a chest of food, and nothing in it reaches the shelf. The question is
recorded in the report.

## What the ground is made of

**The biome is Savanna, and the ground is straw turf, brown earth and chalk.** Grass `#bfb755` and foliage
`#aea42a` make the turf sun-bleached and the orchard ripe. The turf is a slope-axis stack at 36 degrees,
dirt and coarse dirt to 45, chalk beyond, so a hillside and a meadow read differently from above.

**Chalk is quartz, polished diorite and diorite, three textures of one pale tone.** The cut faces show it
in beds that lie level from y0, a flint line every ten courses, in the fill, the wall and the rim alike, so
the coomb's two cliffs read white and bedded from across the gap.

**The built family is terracotta and brick, dark oak and spruce, and the accent is hay.** The cottages are the
library's `brick-roofed-terracotta-and-oak-house` in two plots a storey apart, the barn `hay-gambrel-barn`
and the spawn hall `oak-and-spruce-timbered-house`. The thatch is the one built thing in the ground's own
tone, and it is a roof, not a wall.

## The techniques, and what each one bought

| Technique | Where | What it bought |
|---|---|---|
| Relief pit + made roof | cellar, crawl, chamber | A real underground storey with three blocks of air, with no subtract and no stamped house over it |
| `line` mark ramp | `cellar-ramp` | A sunk way in, 34 down to 30, walked end to end |
| Scarp marks | two banks in the orchard | Terraces a player steps between, not a ramp |
| Push, positive and negative | Horse Hill, oak knoll, dew pond | A down, a knoll for the bench, a hollow for the water |
| Patches in their own theme | the white horse, the pond bed, the cellar floors | Chalk where chalk is cut, laid by shape |
| `made` layers with `seat: "ground"` | well, press, bench, ricks | Small things settled onto the grade |
| `FluidProp` basin + `Outline` | dew pond | Water in a hollow the relief dug, with a lobed edge |
| `FloraProp` with `lilyShare`, `mushroomShare` | pond, fairy ring | Lily pads and mushrooms, each where it is placed for a reason |
| `VertexEdit` pulls + `ShapeBend` | the rim of each hamlet | A coast along the coomb instead of a ruled line |

## What went wrong

**A stamped house cannot stand over a pit.** The barn seated its floor at the cellar's floor and dug 97 blocks
of ground out, so it stands north of the cellar yard instead.

**A yard mark's bevel at the board's edge removed the chamber's east wall.** The chamber was open to the sky
at its far end until the mark's ring was drawn past the edge. A render from inside found it and no number did.

**Both monuments carried the same name.** The default `Red Monument` and `Blue Monument` replaced it.

**The dead-ground read stays at 42.7%.** One monument a team on an 88-block lane cannot meet the band, and
the report says so.

## Coordinates

Team 0's, in blocks; team 1's is the image at `z′ = −z−1`.

| Thing | x | y | z |
|---|---|---|---|
| spawn hall | −11…7 | 35 | −111…−93 |
| monument | 8 | pillar y36–38 | −58 |
| cellar pit · roof slab top | 14…26 | floor 30 · 33 | −78…−69 |
| ramp mouth → cellar | 2 → 14 | 34 → 30 | −74 |
| crawl | 26…31 | floor 30 | −75…−73 |
| chamber · chest | 31…41 · 36 | floor 30 · 30 | −78…−70 · −74 |
| barrow mound centre | 36 | top 37 | −74 |
| well · cider press · bench | −6.5 · 19…24 · −38…−36 | — | −73 · −64…−61 · −27…−26 |
| white horse | 19…42 | on the south face | −41…−27 |
| dew pond · old oak | −22 · −38 | pit floor 23 · — | −39 · −34 |
| hayricks | −31, −24, −17 | — | −86, −88, −86 |
| standing stone · cairn | 36 · 30 | — | −85 · −46 |
