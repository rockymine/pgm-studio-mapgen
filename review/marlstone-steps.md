# Marlstone Steps — a CTW board built out of tiers rather than relief

**In one sentence:** a white marl hillside cut into five terraces and split by two void ravines, with dark
olive scrub on the flanking shoulders, an orchard on a deliberate grid down the middle, red-tiled houses
lined along two frontage streets, and a team's two wools cellared at opposite ends of the hill — one high
and far, one low and near.

152 × 204 blocks, `rot_180` about the origin, base surface 10, build ceiling 40. One landmass; the two halves
overlap across `z = ±14`, so the mid is walked rather than bridged.

## The board, tier by tier

Every height below is the **top block**, which is one less than the `base_height` the document states.

| Tier | Shape(s) | `base_height` | Top | Theme | What it is |
|---|---|---|---|---|---|
| mid | `strand` | 10 | y9 (relief to y13) | `marl-strand` | the contested low ground, the only tier the relief reaches |
| — | `outcrop` | `raise` 6 | ~y15 | `marl-rock` | a limestone knuckle breaking the sightline across the mid |
| lower | `low-west`, `low-east` | 14 | y13 | `marl-terrace` | the first terrace, retaining face in a `wallRun` of quartz courses |
| — | `low-mid` | 13 | y12 | `marl-street` | the street between them, one block sunk |
| middle | `terr-west`, `terr-east` | 18 | y17 | `marl-scrub` | the scrub shoulders, rim **off** |
| — | `terr-mid` | 18 | y17 | `marl-orchard` | the orchard terrace |
| — | `gate-pan` | `sink` 2 | y15 | `marl-street` | a sunken court behind the gate wall |
| upper | `shelf` | 22 | y21–22 | `marl-shelf` | the town shelf, tilted by `anchor_heights` |
| — | `cistern` | `sink` 3 | y17 (water) | `marl-cistern` | a rainwater cistern beside the west wool cellar |
| top | `crest` | 26 | y25 | `marl-crest` | the crown, spawn hall at its centre |
| joins | `ramp-a`…`ramp-d` | `level` + tilt | — | `marl-street` | four paved ramps, alternating flanks |

Nine themes over sixteen shapes. The rim is **off** on the two grown surfaces (`marl-strand`, `marl-scrub`,
`marl-rock`) and **on** for every built tier, which is the single decision that most changes how the board
reads: with it on everywhere, each contour of the mid takes a lip and the whole hill terraces itself.

## Where the objectives are

| Objective | Position | Ground | Reached by |
|---|---|---|---|
| red wool (`red`) | `(-55, 21, 60)` | `shelf` west spur, y21 | the shelf street, then a spur past the cistern |
| red wool (`orange`) | `(65, 13, 30)` | `low-east` east lobe, y13 | the lower street, through the terrace village |
| red monuments | `(-8, 27, 77)` and `(7, 27, 77)` | inside the spawn hall | — |
| blue | `rot_180` images of the above | | |

`<gamemode>ctw</gamemode>` and "Capture the enemies' wools!" — correct on this board, and worth stating
because `MetaGenerator` now derives both from the objective modules the intent carries rather than from a
constant. A destroy board built on this revision would say so.

## The two ravines, which are the design

Two void slots, each 10 blocks wide, cut down the hillside from `z ≈ 24` to `z ≈ 50` at `x −35..−25` and
`x 25..35`. Probed at `(−30, 40)`: **0 solid blocks at any height**. They divide the middle three tiers into
three ribs that meet only at the mid below and the shelf above, so getting from the centre spine to a
shoulder costs either a descent, a climb over the top, or a bridge. Both ravines carry a build zone, so
bridging is permitted and visible — the commitment `approaches.md` describes rather than the impossibility.

The evaluator's `G8 fill-ratio` came in at 0.695 against an authored band of `[0.201, 0.496]`, i.e. the board
is still much more land than void by the corpus's standard. Cutting the two ravines took it from 0.789 and
trimming the mid took it to 0.695; going further would have meant a board this hillside cannot be. Recorded
as a deliberate deviation rather than fixed.

## How it is meant to play

**The two wools are unlike in every dimension**, which is the whole shape of the board.

**The east wool is low, near and fought through.** It sits at y13 on the lower terrace's east lobe, thirty
blocks from the mid. An attacker crossing the strand reaches it quickly and then has to work through a
terrace village with a street, houses and a retaining wall. It is the early objective, and it is cheap to
reach and expensive to hold.

**The west wool is high, far and fought from above.** It sits at y21 on the shelf's west spur, sixty blocks
in and four tiers up. Every route to it crosses at least one terrace face, and the defence holds the shelf
street above it. It is the late objective.

**Nothing runs straight up the middle.** The gate wall — one `walls` entry between `low-gate` and `mid-gate`
— is a two-thick bedrock line at `x −10..10, z 34..36`, `topY 18`, three courses proud of the attack side.
Behind it the `gate-pan` sinks two blocks, so a defender who drops into the court is below the lip and out of
sight from the street. The centre is therefore the one approach that has to be broken rather than walked
around, and the ravines either side of it are the two that do not.

**The four ramps are what make the hill playable both ways.** Without them a five-tier board is a series of
one-way drops: an attacker falls down it and a defender cannot rotate back up without building. `ramp-a`
(east, mid→lower), `ramp-b` (west, lower→middle), `ramp-c` (east, middle→shelf) and `ramp-d` (west,
shelf→crest) alternate flanks, so the walk from spawn to the mid is a zigzag across the whole width of the
board rather than a straight fall. Measured down `ramp-d` at `x = −40`: y20 at z66, y22 at z70, y23 at z74,
y25 at z80.

**Circulation was drawn before anything was planted.** Eleven paths state the movement — two crest streets
either side of the spawn hall, a shelf street running the width of the town to the west wool's door, three
lower streets, and one on each ramp. The trees are in the ground those runs and their margins left over.

## Techniques, and what each bought

**Tiers instead of relief.** Only `strand` takes the relief; the other fourteen shapes are `exclude`. The
readback reports **4 294 cells** of relief field on a board of roughly 19 000 ground cells — the mid alone.
Every level change above it is a shape: four `level` ramps, two `sink` basins, one `raise` outcrop and a
tilted shelf. This is the opposite of the "one relief over everything" answer and it is why the board has 16
blocks of fall in it without a single contour ring on a built surface.

**A tilted terrace.** `shelf` carries `anchor_heights` running 21 at its west spur to 23 across its middle,
so the town's ground is not a dead plane — it falls toward the wool cellar. Confirmed: `(30, 66)` reads y22
against `(−40, 66)`'s y20.

**Bézier corners.** `low-east` and `crest` carry `controls`. A/B against a build of the same vertices with
`controls` removed: `(73, 36)` and `(74, 36)` are void without and solid with; `(52, 89)` likewise. The east
lobe that carries the wool room and the two upper corners of the town are rounded rather than cut.

**An orchard on a grid, scrub that is not.** Twelve oaks at `x ±16, ±21` by `z 39, 45, 51` — a 4 × 3 grid
across the orchard terrace. Ten acacias on the two scrub shoulders at unrelated offsets. The dressing-aware
foliage render (`03-foliage.png`) shows the two side by side, and the difference is legible without a legend:
one is cultivated ground and the other is not. Placement alone says it.

**Twelve houses on two frontage lines**, three styles differing first in height and aspect — `merchant`
(wall extent 7, gabled, brick), `cottage` (extent 5, hipped, red clay), `workshop` (extent 6, shed, stone
brick and quartz). Crest row: south walls all on `z = 87`, four blocks clear of the street band. Shelf row:
north walls all on `z = 55`, three to six blocks clear. Nothing was dropped.

## What went wrong

**Sixteen shapes rasterized to nothing, and every stage said it was fine.** The first layout omitted `type`,
`operation` and `floor`. `PUT .../sketch` answered `{"ok": true}`, `GET .../sketch` returned all sixteen
shapes and the relief intact, and `POST .../sketch/relief/read` answered **200 with `{"islands": []}`** — the
only symptom, and one that reads as a relief fault rather than a geometry one. `SketchShape.Type` defaults to
`""` and `RingOf` returns `[]` for an unknown type, so nothing rasterized, so the island owned no cells, so
`SolveRelief` skipped it. Found by posting a known-good layout to the same endpoint and diffing the shape
objects. Full write-up in `GENERATION-NOTES.md` §1.

**A nine-block band of the wrong material across the top of the shelf.** Height resolves an overlap by *the
taller shape*; paint resolves it by *the smallest-area shape*. `terr-mid` (~1 500 cells) underlaps `shelf`
(~3 300 cells) so the shelf can pull its edge inward — the documented technique — and the result was that
`terr-mid` kept the paint over ground the shelf owned. Measured at `x = 0`: `(0, 70)` quartz, correct;
`(0, 58)` **y21 (the shelf's height) painted grass over dirt over sandstone (the orchard's palette)**;
`(0, 50)` orchard, correct. Reduced by pulling the three ribs' north edges to within two to four blocks of
the shelf's south edge; not eliminated, because the underlap is what stops the join opening a hole. It is a
real interaction between two documented rules and nothing warns about it — `GENERATION-NOTES.md` §2.

**`--buildings` said six roof components when twenty-four houses had stamped, and I reached for the wrong
tool.** The census finds roofs by material and then judges them against a timber convention this board does
not follow: `--roof 45:0` misses a roof surfaced in brick *slabs* (44:4) with a quartz-pillar verge;
`IsTerrain` includes `159`, so the cottages' red-clay roofs are classified as *ground* and discarded
(`--roof 159:14` returns **0**); and `CornerStems` wants a vertical log at each corner, which quartz-pillar
posts are not. All three compound, and relaxing the thresholds changed nothing.

The right instrument is **`--topdown --layer structure`**, which reads `region/provenance.json` — what the
passes actually placed. Its owners list is the census, and it is unambiguous:
`house 24, spawn 2, redstoneline 4, roomfloor 4, wool 4, wall 2`, with the houses named `h1`…`h12` twice
over. `02-structure.png` draws all of them. Nothing was ever missing.

Two lessons, and the second is the one that cost time: a measurement that disagrees with a picture is not
automatically the truth, and a tool built to read *unknown* worlds is the wrong one for a world this studio
just built and recorded.

**I probed the Bézier at the vertex and concluded it did nothing.** The vertex is a fixed point of the curve;
the bulge is between vertices. Two probe rounds wasted before computing `t = 0.5` and looking there.

**The spawn platform's interior is still raw stone.** `(0, 85)` reads `Stone` under the wool monument on a
board whose crest theme is quartz. Third independent map to report this; recorded as corroboration, not a
new finding.

## Open questions, decided without an oracle

**Is a five-tier board too vertical for CTW?** Sixteen blocks of fall from spawn to mid over about ninety
blocks of run, in four faces of three to four blocks each. I added the four ramps because a board that can
only be descended is not a board a defence can rotate on, but whether four faces is right, or two, or six, is
not something a column probe answers.

**Should a team's two wools be at different difficulties?** I made them deliberately unequal — one low, near
and quick, one high, far and slow — on the reading that `approaches.md`'s "the approaches should differ"
extends to the objectives themselves. The evaluator disagrees mildly: `WL9 spawn-wool-ratio` is 1.5 against
an authored band of `[1, 1.231]`. The corpus says a team's wools are usually comparable in distance. Left as
authored, and recorded.

**Are 10-block ravines wide enough to matter?** They cannot be jumped and they cost blocks to bridge, but
`approaches.md`'s illustrative figure for a void a player must go around is twenty. Mine are half that,
because the hillside they cut has to stay walkable across. Whether they read as a barrier or as a nuisance is
a question about feet.

## The renders, in the order they were looked at

`01-topdown` (the whole board, category colour, provenance-read structure), `02-structure` (**the building
census as a picture** — every house, both wool rooms, both gate walls and the spawn hall, straight from
`provenance.json`), `03-foliage` (the orchard grid against the scrub, drawn as points and crown radii),
`04-heightmap` (the five tiers as contours), `05-section-x0` (the spine, spawn to mid), `06-section-x-40`
(`ramp-d` as a diagonal between two flat tiers — the one image that proves a ramp), `07-traversability`
(4 components, 4 objective markers, **0 isolated**).
