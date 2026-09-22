# Emberhowe — the crater is the board, and the plug in it is what both teams want

> Capture the wool. Two horseshoes of rim facing each other across a crater, with
> a neutral plug standing in the middle of it and sixteen blocks of void between
> the plug and each limb. Every crossing on the board is the same sixteen blocks:
> the two onto the plug, and the one inside a team's own half that joins its two
> wool rooms.

## Where the things are

| The thing | Where | Measured |
|---|---|---|
| the plug | `x -48..48, z -12..12` | 2 304 cells of neutral ground, fanned by nothing |
| the middle | `z -28..28` | 56 blocks between the two lands, 16 of void either side of the plug |
| north crossings | `x -48..-28` and `x 28..48` at `z 12..28` | 16 blocks, `CT12` wants 15–40 |
| the causeway | `x -28..-8` and `x 8..28` at `z 32..44` | a team's own two rooms joined, with 16 blocks of void between the halves |
| west wool | `(-76, 44)`, room `x -84..-68` | three faces on void, one wall sixteen blocks in front |
| east wool | `(76, 44)`, room `x 68..84` | the same room at the same z — the halves are mirrors |
| spawn | `(-2, 73)` on the crest | door faces **left**, along the crest |
| the bays | `x -28..28` at `z 28..32` and `z 44..60` | the void a team's own rim rings |

## The one decision the board is built on

**The middle is 56 blocks across and there is ground standing in it.** Team land
ends at `z 28`, the plug spans `z -12..12`, and a team bridges 16 blocks off
either limb to reach it. A middle both teams can stand on is what the board is
contested over; a bare strait is two lands taking turns at each other.

**A board with one way out of spawn is a board with one fight.** From the hall a
player goes left or right along the crest and that is the whole of the decision —
so the rim's two halves are joined across the team's own bay at the rooms' own
z, broken by 16 blocks of void. A rotation from the red wool to the orange is a
bridge somebody can be shot off rather than a walk round the whole rim, and land
all the way across would have taken the danger out of it (author).

**The board is symmetric twice over, and that is ordinary practice.** `rot_180`
between the teams, and each team's own half mirrored down `x = 0`, so both rooms
sit at one z and cost the same walk from the hall — 88 blocks west and 92 east.
`WL9` reads that as a ratio of 1 and passes it since amendment 44, where its band
used to start at 1.031 and call perfect balance a fault.

## What the ground is made of

Three themes. The rim is the board's one ground and carries 61.8% of its cells,
finished on the **slope** axis so that the ash flat, the scoria shoulder and the
crater face are three grounds on one hillside rather than one colour from above.
The drifts (22.0%) and the yards (16.1%) are the two places made of something
else, each a shape carrying its own theme.

The band edges are cut off this board's own `incline`, which reads **51.5% under
10°, 28% to 19° and 9.6% at 40° or steeper**. Cuts at 20 and 40 fall between three
real populations. The fill is a voronoi of stone and andesite, which is where a
voronoi belongs: it draws a diagram, and the body of the rock is the one place
nobody sees one.

## The techniques, and what each one bought

**A hole is made by arrangement.** No mark and no subtract cuts this pit: nine
pieces ring a gap and none covers it, and the compile declares it a `void-N`
buffer by itself.

**`LN2` is a lane rule, not a size rule.** The rim was 176 blocks long on the
first cut and read as one lane against a band topping at 110 — a lane is measured
to its next junction, and a crest with the arms joining only at its ends has none.
The board is 160 × 168 now and the cap runs 96.

**A spawn door wants somewhere to open onto.** Three of the spawn piece's four
sides are the pit or the outer coast, so the door faces **left**, along the crest.
Stated `front` it opened onto the pit and `SP9` read nought blocks of ground.

**One push, and its two grades inside twice each other.** The spatter cone climbs
its skirt at 0.5 and its crown at 0.4; past twice apart `RL6` says the ground
steps at the push's own outline.

**The cone is centred over the water, and what stands on the board is its seaward
flank.** A wool board's lane is thin — the land west of the spawn is 36 blocks
from the coast at `x -48` to the hall's wall at `x -12` — so a 20-block landform
anywhere inside it is the whole width of the way to the board's left side. At the
shore the bank rises 8 blocks over 16, which transects as *worst step 1, walked
end to end*, and leaves 20 blocks of flat crest beside the hall.

## What went wrong

**Eleven props of thirty-five were declined on the first pass, and every one of
them was placed by eye.** `POST …/sketch/seats` answers a raster of the cells a
footprint's minimum corner may sit on, and `tools/loop.py --candidates` answers
whether a given try lands, in twenty seconds rather than ten minutes. Placed off
those two, the board declines none.

**A 20-block limb cannot hold a building.** `DR-PASS` wants eight blocks of
passable ground on every side that is not a coast, and both arms are 20 wide, so
a 10-wide shed leaves at most nine. The board carries one works shed, on the
crest's east corner, and the limbs are bare — which is what they are fought over.

**A made thing and a stamp do not read each other.** The rim parapet ran past the
spawn and shared the courses of six columns with its iron cube; `SK18` is the only
thing that says so, and only on the export's header. It is two runs now, and the
hall is the gap between them.

**A revetment runs the pit's own width and stops there.** Carried out to the limbs
it stands across the mouth each limb opens off the cap at, which is the lane every
journey on this board runs along, and two courses there is a step every walk out
of the hall pays. The walk to the west room read `barrier +6 at (-34, 62)` with
the parapet and a tree's crown stacked on the line; it is `worst step 4` and four
placed blocks now, against the east's five.

**Eight trees stood on gravel, stone, hardened clay and diorite, because the board
had no soil on it at all.** `DR-ROOT` is the rule that now says so, and the fix is
the paint rather than the position: coarse dirt joins the ash on the flat band and
the drift's own cells, which makes 421 of the board's 10 824 cells seat a tree
against 4 832 for a boulder. Every scrub came off that mask.

**Both walls were buried under the ground they were meant to bar, and the author read the first build and
found them.** That one is a studio bug and is fixed: `StampWall` took its height from the surface the
*plan* drew rather than the one the relief solved, so a mark that lifted the seam left the bedrock
underground — with its own defence chest standing correctly on the ground above it, because the chest reads
the solved surface and the wall did not (`rules.md` amendment 43).

**Both also sat where they could be jumped round, and that one is this board's.** The wall stood on the
limb's own edge, where the limb runs 24 blocks past its ends, so its ground wraps the corner:
`(-48, 36)` to `(-50, 35)` is a running jump that lands behind it.

**The answer to the second was four blocks.** Each spur gained a `mouth` piece where it opens off the limb
and the wall moved onto the approach↔mouth seam, so both its ends are now bounded by the pit and going
round it means leaving the ground. The rooms moved out with it, which also put the wall on the shelf's own
flat: it stood **six** courses proud on ground falling 11 → 14, and stands three on ground a transect reads
`worst step 0` end to end. `PL17` and `ST4` are the two complaints that now say both of those out loud.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| west wool room | `(-76, 44)` | three faces on void, wall at `x -52`, in the lane |
| east wool room | `(76, 44)` | the same room at the same z |
| spawn hall | `(-2, 73)` | 12 × 12, door west onto the crest |
| the plug | `x -48..48, z -12..12` | pinned at 14 with a benched top, `plain` at 0.10 for its own size |
| plug crossings | `x -48..-28` and `x 28..48` at `z 12..28` | 16 blocks of void, both teams' |
| the causeway's gap | `x -8..8` at `z 32..44` | 16 blocks, and 12 deep because `G2` refuses a corridor under 10 |
| spatter cone | `(-50, 72)` | amount 5, falloff 10, crown 4 — ring centred over the void off the west coast |
| rim parapet | `x -28..-14` · `x 14..28` at `z 61` | the pit's own width, clear of both limb mouths |
| spawn → west wool | `(-2, 73)`–`(-76, 44)` | 88 blocks, 5 placed, worst drop 5 |
| spawn → east wool | `(-2, 73)`–`(76, 44)` | 92 blocks, 4 placed — a ratio of 1.05, which `WL9` now passes |
| wool → wool, over the causeway | `(-20, 38)`–`(20, 38)` | 115 blocks and **0 placed** the long way round, against 16 placed straight across |
| west wall | `(-53, 36)`–`(-52, 51)` | level end to end, 3 courses proud |
| whole board | `168 × 168` | 12 748 walked · 52 scrambled · **0 barrier** · 0 faces |
| the evaluator | — | **score 0, valid True** — no refusal and no complaint |
| coverage | — | **0.2% dead** over 21 journeys |
| dressing | — | 36 placed, **0 declined** |
