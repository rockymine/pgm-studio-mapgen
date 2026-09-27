# Whitstone Weald — a large destroy board for a 32-a-side play test

## What I set out to build

**A wooded mining weald where each team keeps two pale end-stone stones: one on a bench under a crag with a
wood on its outer flank, one on a village green with a hamlet behind it and a drift mine under the ground in
front of it.** That was the one sentence, written before the plan.

The author's brief was a destroy-the-monument board for 32 a side, larger than the eleven small boards in the
same play test. It asked for real relief, and for more trees and more houses than the recent destroy boards
here, which carry one or two houses and six to eleven trees a team. It also asked for an underground section players
can use, and a plan authored rather than taken from the composer.

**The author's ruling during the run was two monuments a team, four in all, each end stone and clearly larger
than the usual obsidian pillar.** How the two stand relative to each other and to the spawn was mine to
decide, and the next two sections say how.

Slug `whitstone-weald`, map name **Whitstone Weald**, credited to Claude. `specs/whitstone-weald/build-spec.py`
writes the plan and the finish; `maps/whitstone-weald/` is the world.

## How the board was sized

**The board's distances come from the destroy maps of the two corpora at this head count, not from a
guess.** Neither corpus is on this machine, so I cloned both without blobs and checked out only the `map.xml`
of every `dtcm/`, `dtm/` and `mixed/` map: 342 files. A throwaway script in the scratchpad read team caps,
spawn regions and destroyable regions out of them.

**Sixteen maps declare 28 to 40 a side and parse cleanly**; three more read their two spawns under 60 blocks
apart, which this parse cannot trust, and are left out. The figures are straight lines between region centres.

| measure, 28–40 a side | p25 | median | p75 | this board |
|---|---|---|---|---|
| spawn to spawn | 236 | 283 | 312 | 276 |
| own spawn to its goal | 66 | 77 | 103 | 67 straight, 71 by walk |
| a team's two goals apart (10 maps with two or more) | 53 | 100 | 115 | 72 |
| nearest opposing goals | 106 | 153 | 245 | 162 straight, 195 by the plan's walk |

Over all 34 maps at 24 to 48 a side, two goals a team is nearly as common as one (14 against 16).

**Two studio bands disagree with that corpus and I followed the corpus.** `GO2` wants a team's goals 35–65
apart by walk and `GO3` wants opposing goals 85–150; neither is scaled by head count. The notes say the four
goal bands cannot all hold on a board this far across the lane, and `GO1`, the ratio, is the one I kept in
band. By walk it reads 71 and 232 blocks, a ratio of 3.27 against the band 3.0–4.0.

**The land budget is larger than a capture board's by design.** The CTW size ladder puts 32 a side at about
8,700 blocks² of land a team; destroy boards are landscape boards with far more ground, and this one holds
about 19,000 a team. The coverage read says how much of that is used, below.

## The board, where each thing is

Every coordinate is team red's; blue's is the rot_180 image, block `(x, z)` to `(−x−1, −z−1)`. The board is
296 × 144 blocks: x −148…148, z −72…72, with the build zone over void at x −16…16 spanning the full width.

### The objectives and the spawns

| Thing | Material and size | Blocks (x, y, z) | Stands on |
|---|---|---|---|
| Red Crag Stone | `cube-4` end stone round a 2×2×2 bedrock core, 56 breakable | x −83…−80, y 31…34, z −37…−34 | a bench at y26, float 4 |
| Red Green Stone | the same | x −83…−80, y 24…27, z 35…38 | a green at y19, float 4 |
| Blue Crag Stone | the same | x 79…82, y 31…34, z 33…36 | its bench |
| Blue Green Stone | the same | x 79…82, y 24…27, z −39…−36 | its green |
| Red spawn | a two-storey brick-and-timber hall, doors +x and −z | hall x −145…−131, z −9…9; point (−138, 0) | a bench at y31 |
| Blue spawn | the same, doors −x and +z | point (138, 0) | its bench |

The `map.xml` declares `materials="ender stone"`, four destroyables with the kit's iron pickaxe, a mode
ladder at 15 and 20 minutes, and `<maxbuildheight>44</maxbuildheight>`.

### The mine, under the south ground

| Part | Where (red) | Heights |
|---|---|---|
| Quarry pit, open to the strait | x −30…−17, z 48…65 | floor top y11, rim y17 |
| Cart ramp into the pit | x −34…−23, z 48…51 | 18 down to 12, one course every two blocks |
| Gallery, roofed | x −60…−31, z 55…59 | gravel floor y11, air y12…15, stone ceiling y16…17 |
| Chamber, roofed, two pillars | x −76…−61, z 52…63; pillars x −72…−71 and −66…−65, z 57…58 | as the gallery |
| Cutting up to the green | x −70…−66, z 34…51 | 12 up to 20 over 18 blocks, open to the sky |

**It walks end to end with nothing placed:** from inside the gallery at (−45, 57, y12) to the cutting's head at
(−67, 32) is 43 blocks; from the pit floor at (−22, 60) to the chamber at (−68, 58) is 47. In the final world
the column at (−45, 57) and its blue image at (44, −58) both read gravel at y11, air from y12 to y15 and
stone at y16 and y17, with the engine house's floor at y20 above.

### The buildings and the made things

| Building | Style | Footprint (red) |
|---|---|---|
| Farmhouse, two wings | brick ground storey, birch-planked upper storey in a dark-oak frame, dark-oak roof | x −127…−118, z −46…−38 (two storeys) and x −127…−122, z −37…−32 (one storey, ridge turned) |
| Barn | brick plinth, laid dark-oak course, dark-oak weatherboard, spruce roof | x −114…−103, z −53…−47 |
| West cottage | the weald style, one storey | x −120…−112, z 52…60 |
| Hall cottage | the weald style, two storeys | x −104…−94, z 50…60 |
| East cottage | the weald style, one storey | x −89…−82, z 54…61 |
| Engine house, over the gallery | the barn's style | x −52…−42, z 54…61 |
| Chimney | a brick stack, 16 tall, seated on the ground | x −56…−54, z 55…57 |
| Mill stump on the crag | a brick ring, outer radius 4.5, 8 tall, a doorway to the south-east | centre (−60, −53) |

Six buildings, a hall, a chimney and a ruin a team, against one house a team on the recent destroy boards.

### Trees, rock and water

| Kind | Where (red) |
|---|---|
| Oak (`showcase-r12`) | (−134, −63), (−117, −62), (−100, −66) — the wood on the north flank |
| Great oak (`showcase-r14-1`) | (−135, 58), at the hamlet's west end |
| Birch (`showcase-r13`) | (−92, −58), (−78, −55), (−136, −44), (−141, −35), (−48, −63), (−38, −55), (−110, 43), (−137, 38), (−106, 18) |
| Young oak (`showcase-r6`) | orchard (−140, 20), (−130, 20), (−120, 26), (−140, 31), (−130, 31); (−120, 44), (−112, 34) |
| Diorite erratics | (−48, −38), (−66, −47), (−40, −62), (−36, 36) |
| Pond | a pan at y14 round (−43, 2), radius 9, filled to its rim |

Twenty trees a team, forty on the board, of two species. The nearest trunk to the Crag Stone is about 19
blocks off; nothing stands inside a goal's ten-block square.

## How each stone is come at

**The two stones are approached differently on purpose, following `approaches.md`.** Each stands in the open
with a different ground on each side of it.

| Stone | Around | Above | Below | Through |
|---|---|---|---|---|
| Crag Stone | the pond at the front centre splits the direct run | the crag tops out at y37 at (−62, −53); its shoulder at (−66, −50) stands at y36, about 21 blocks from the stone and over its top course at y34; the bench bank is a scramble on the front | — | the oak-and-birch wood on the north flank |
| Green Stone | the pond, from the other side | only weakly: the spur's crest at (−90, 4) stands at y29, ten over the green but about 32 blocks off | the mine, from the quarry at the strait to the cutting's head 15 blocks east of the stone | the hamlet behind it, which is the defenders' side |

## The reads and renders, and what each one changed

- **The corpus `map.xml` measurement** set the spawn at x −138, the stones at x −82, 72 apart across the lane,
  and a 32-block strait.
- **`/plan/evaluate` and `/plan/inspect`** gave `GO1` 3.28 and 3.32 on the first plan; `GO2`, `GO3`, `LN2` and
  `G8` stayed outside their bands and are explained below.
- **`board.py` and the stored grid** confirmed the arrangement: a spawn and one field a team, one strait.
- **The first store answered `RQ4` 45 times**: I had guessed the fused field's id. The compile names it after
  the alphabetically first piece, which was the spawn, so the spawn piece became `yard` and the field
  `weald-20`.
- **`RQ1` refused eight vertex inserts** that folded the ring. The notch is now drawn from both mouths inward,
  with one temporary point moved home last.
- **Coverage** read 44% dead on the first build, with four patches on the outer flanks. I narrowed the board
  from ±76 to ±72, cut bays into both coasts and put the wood and the hamlet there; it reads 25.5% after the
  dressing.
- **Columns at the spawn and the shelves** showed that a mark's `h` is a column height, so the quarry rim and
  the cutting's head were each one course off; both were fixed.
- **The relief read** found `RL6` on two pushes, `RL3` between the mine cover and the quarry rim, and `level`
  moving from 0.40 to 0.35 to 0.41 as the landforms changed; each was fixed.
- **The isometric** showed a tilted field with contour lines and a conical fell. The spur, the Crag Stone's
  bench and a smaller fell went in.
- **`incline`** put the grass cut at 38° and bare rock above 52°.
- **The theme and style previews** checked the ground section and the three house styles before a build.
- **`HS4`** refused every building at the first painted build: a glass pane in a brick host. The pane now cuts
  wherever it fits.
- **`sketch/columns` declined 18 props on the first painted build** — `HJ1`, `DR-SLOPE`, `DR-CROSS`, `OB19`,
  `DR-CLAIM`, `DR-ROAD` — and later passes named `HJ3` and `DR-KEEP`. Each was re-laid until 86 props placed
  and none declined.
- **A transect across the farmyard** read 37 falling to 29 at 44°: the fell's skirt was added onto the yard's
  mark. Both fells were pulled into their corners.
- **The eye at the barn's east end** showed a house cut into the bench's skirt, so the barn moved and the bench
  shrank.
- **The seats read, re-asked with the trees taken off**, gave the tree sites. The raster the drive writes counts
  the trees already placed as claims.
- **The eye in the gallery** showed a dirt ceiling, so the ground over it was raised until the ceiling course is
  stone.
- **The eye on the tracks** showed podzol squares, so hardened clay replaced them.
- **Pond transects** showed water at y13 against a rim at y12, then a dry trench and a five-course bank. The
  pond became a pan the size of the water, with a pool that states no level.
- **`DR-TONE`** named grey erratics on grey ground, so they are diorite.
- **Columns through the crag** read its top at y32, level with the Crag Stone's lowest course, so it was no
  approach from above. It was raised to y37, and `DR-STEEP` then moved one erratic off its steeper skirt.
- **The eye at the spawn** showed the team band hidden under the eaves; it moved down to sit over the beams.
- **`walk`** measured each team's four routes and the two walks through the mine; `column` confirmed the
  monuments and the gallery on both sides.

## What the studio refused or complained about that is left

**`SK26` on the cart ramp stays.** It says the ramp's high end at (−34, 48), course 18, falls two within four
cells. The transect along z 48 and z 50 reads 18 at x −34 and 18 on every cell west of it, and the ramp walks
from 12 to 18 with no step over one. `SketchRasterizer.FlightsEndingAtADrop` reads the drawn tops of every
layer, so beside the ramp it sees the field's drawn height rather than the ground the relief solved.

**Four plan-tier soft terms stay outside their bands**: `GO2` 72, `GO3` 195, `LN2` 144 and `G8` 0.413. The
first two follow the corpus at 32 a side, as above; `LN2` is the length of a board this long.

**`G8` is the plan's flat measure, and the built board's coverage is the read that counts.** Coverage reads
25.5% dead, in four patches of about 2,300–2,550 cells on the outer flanks at (±92, ±57), each one block from
used ground. The wood and the hamlet stand there; for a destroy board a dead share is a note rather than a
fault.

**The store answers `SK10` and `SK11` once each, before the outline is edited, and neither is on the map
after it.** The compiled field covers the mine until the notch is cut. `GET …/findings` on the stored map
lists `SK26` alone, and the export answers 200 with no warnings header.

## What I could not say

**A goal larger than `cube-4`: missing.** `GET /api/objectives/vocabulary` names six styles and the largest
is a 4×4×4 cube; `DestroyablePlacement` has no size or height field. The destroyables document says the
studio stamps the small end of the end-stone family on purpose, since a monument over 200 blocks is a TNT
map. Sixty-four blocks of end stone is sixteen times a three-block pillar, and I judged that clearly larger.

**A roofed tunnel under relief-solved ground: not missing, but no single instrument says it.** It is three
statements: a notch in the field's outline, two roof shapes in the ground's own group with `floor` 16, and a
storey below holding the floors and the ramps. It built as designed the first time the notch went in.

**A relief or dressing preview of the whole spec before storing: out of reach from `loop.py`.** It compiles
and patches the plan but does not replay `editShapes`, so its layout has no notch and no coast. I posted
the stored layout with the new relief or props to `sketch/relief/read` and `sketch/dressing` instead, which
answered in seconds.

## What I got wrong

- **The field's id**: I assumed the main piece names it. The compile names the fused shape after the
  alphabetically first piece.
- **The order of the notch's points**: inserted in ring order, the chord closing the half-drawn notch crossed
  the gallery's wall.
- **The height of a mark**: I read `h` as a top block. It is a column height, as `base_height` is.
- **The pond as a push hollow with a pool laid in it**: the hollow and the water disagreed wherever the
  spur's skirt touched the hollow, which a column at the rim showed.
- **The farm on the fell's skirt**: a push is added to whatever the marks solved, so the yard's flat mark
  tilted to 44°.
- **The barn beside the bench**: `DR-DIG` reported four courses and I nearly left it as a bank barn. The eye
  showed a gable standing in a cut, which is a house in a hill.
- **Spacing trees by eye**: an oak's crown here reaches about ten blocks, so birches set six to eight away
  stood inside it.

## What worked first time

- The plan's `GO1` was in band on the first evaluate, because the goal positions were arithmetic from the
  corpus before any shape existed.
- The mine's two-storey construction: floors on a storey below, roofs in the ground group. The void scan read
  it as one open void, and `walk` went through it end to end.
- The made chimney and mill stump, seated on the ground, landed on both teams' sides.
- The copied trees, taken whole from the library into `trees.json`.
- The export gate was open on every run.

## Gameplay decisions taken without the author

Nobody could answer gameplay questions during this run. Each of these is built as stated and is open for the
author.

1. **The two stones of a team stand side by side across the lane, not one forward and one back.** Both sit 56
   blocks in front of their spawn at z ±36, so each has the same ratio. The spread of 72 is the lower
   quartile of the corpus at 28–40 a side; the median there is 100. Is 72 right for 32 defenders?
2. **The monument is `cube-4` end stone, 56 breakable blocks, float 4, with no TNT in the kit.** Is that the
   right amount of end stone for 32 attackers, split over two stones?
3. **The opposing stones are 195 blocks apart by walk**, over `GO3`'s 150 and near the corpus median of 153 in
   a straight line. Does that risk a stalemate on this board?
4. **The mine is open to the strait.** Attackers who bridge across can drop straight into the quarry, and it
   surfaces 15 blocks from the Green Stone in a cutting defenders can watch from the green. Should it open onto
   the strait, or only from land?
5. **The hamlet stands behind the Green Stone, on the defenders' side**, the "village behind" of
   `approaches.md`. It is cover for defenders coming from the spawn rather than an attack route.
6. **The wood keeps about 19 blocks off the Crag Stone.** `OB19` keeps every prop ten clear, and an oak's
   crown adds ten more. Is that close enough to be the forest approach?
7. **The pond is the depression at the front centre** that replaces a mid-board hole. It is a pan at y14 with
   water, not a dry drop.
8. **The spawn's doors are the studio's**: front and north for red, front and south for blue. Each side door
   leads toward that team's Crag Stone.

## Not done

**Three of the instrument counts are zero**: no `height_mode` shape, no made ground with `relief_scope`, and
no polyline. The ground is one relief with marks and pushes, and the joins are the mine's anchored flights
and the Crag Stone's bench. A walled spawn terrace or a flowing field wall would each add one of the missing
three.

The board has not been played. Its numbers are what the studio measures; the match is what the author will
see.
