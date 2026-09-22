# Emberhowe — the crater is the board, and going round it is the decision

> Capture the wool. Two horseshoes of rim facing each other across a pit nothing
> spans, joined only by twenty-four blocks of strait at each horn. A raider picks
> a hand there and lives with it: the far room is reached by walking the whole rim
> past the enemy spawn, and there is no way across.

## Where the four things are

| The thing | Where | Measured |
|---|---|---|
| west strait | `x -48..-28, z -12..12` | 24 blocks, `CT12` wants 15–40 |
| east strait | `x 28..48, z -12..12` | 24 blocks |
| west wool | `(-76, 28)`, room `x -84..-68` | three faces on void, one wall sixteen blocks in front |
| east wool | `(76, 40)`, room `x 68..84` | eight blocks further round the rim |
| spawn | `(-2, 73)` on the crest | door faces **left**, along the crest |
| the pit | `x -28..28`, the board's whole length | 896 cells, no build zone over any of it |

## The one decision the board is built on

**The pit carries no build zone, and that is what makes the two horns a choice
rather than two doors into the same room.** A zone is authored, and neither of
this board's two is over the middle — so the only ground between the teams is the
twenty-four blocks at each horn, and a player who crosses at the west cannot
change hands afterwards without walking the whole rim.

**That is `approaches.md`'s *around* at the scale of the whole board rather than
of one objective.** A hole in front of a goal makes two ways round it; a hole the
board is a ring about makes two ways round the *board*, and the far way runs past
the enemy's own spawn. `match-flow.md` §4.9 prices that choice at 76% of the
defender's reinforcement lane against 37%, and here the near way is the only short
one there is.

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
| west wool room | `(-76, 28)` | three faces on void, wall at `x -52`, in the lane |
| east wool room | `(76, 40)` | the same, eight blocks further round |
| spawn hall | `(-2, 73)` | 12 × 12, door west onto the crest |
| spatter cone | `(-50, 72)` | amount 5, falloff 10, crown 4 — ring centred over the void off the west coast |
| the lane west of the hall | `x -32..-12` at `z 60..84` | 20 blocks flat, `worst step 1` from the hall's wall to the shore |
| west wall | `(-53, 20)`–`(-51, 35)` | bedrock to y17, cobweb y18, **level end to end**, 3 courses proud |
| whole board | `168 × 168` | 10 812 walked · 12 scrambled · **0 barrier** · 0 faces, `rolling` at 0.29 |
| coverage | — | **2.9% dead**, 6 patches out of reach |
| dressing | — | 36 placed, **0 declined** |
