# Wetherslack — the second way at the core is under it

> Destroy the core. A wooded gill with a beck down it, and the core standing on a
> vaulted terrace built out over the gill's west side. The deck is flush with the
> shoulder behind it, so from the west a player walks straight on; from the gill
> floor the way at it is the undercroft underneath, and the shaft in the deck
> comes up four blocks from the casing.

## Where the four things are

| The thing | Where | Measured |
|---|---|---|
| core | `(-4, 62)`, `layer: vault-deck` | own walk **53**, enemy **175**, `GO1` **3.30** |
| the deck | `x -16..8, z 52..72`, base_y 21 | top block y21, one over the shoulder's y20 |
| the undercroft | `x -14..6, z 54..70` | **nine courses of air**, y12–y20 |
| the shaft | `x -12..-8, z 56..60` | four blocks no deck rectangle covers |
| the two mouths | `z 60..64` east, `x -6..-2` south | onto the beck and onto the strand |
| the flight | `(-24, 40)` → `(-12, 58)` | anchors 21 → 12, the shoulder to the bench |

## The one decision the board is built on

**The undercroft is ground nobody drew on, and that is why it exists at all.** An
opening is a gap between shapes rather than a subtract — `SK13` reads a subtract
as the board's negative space and refuses any add that fills it — so the walls are
six rectangles with two mouths left between them and the shaft is four blocks the
deck's own four rectangles are drawn around.

**The deck is flush with the shoulder by one course, and that is the whole of the
upper approach.** The shoulder is marked at h21 and tops at y20; the deck rests at
base_y 21 and tops at y21. A player steps up one and is on the terrace. Nothing
else joins them, and a raider on the gill floor cannot see either.

## What the ground is made of

Three themes. The gill carries 69.6% of the board's cells and is finished on the
**slope** axis, cut at 18° and 34° off an `incline` reading 54.5% under 10°, 15.2%
to 19° and 7.7% at 40° or steeper. The flush (13.3%) is the beck's shingle and the
garth (17.2%) the spawn's yard.

The biome is **Roofed forest** (`#79c05a`) and the palette states **no podzol**.
The two are a colour distance rather than a prohibition: podzol meets a tint on
`Mesa` or `Swampland` and fights one this green, and a pattern mixing them would
read as neither ground.

## The techniques, and what each one bought

**A layer holds one span per column, and the air between two is the feature.**
The walls stand on the bench at base_y 12 and run nine courses to a segment top of
21; the deck rests at 21. The column at `(-8, 64)` reads stone brick at y21, then
nothing at all until gravel at y11.

**A goal on a stacked board names its layer.** Stated with none, the core took the
terrain under the terrace — casing at y18 over ground at y11, hanging in the
undercroft's own airspace with the deck running through it at y21. With
`layer: "vault-deck"` it seats on the deck: chest at y22, casing y28, lava y29–31,
lid y32.

**A bevel grades inward from both edges of a mark's ring.** A bevel of 5 on a
strip ten blocks wide leaves no flat core at all, and `RL4` read the west shoulder
as a mark that pinned nothing. At twelve wide and a bevel of 2 it pins six.

**A channel's width is decided by its mark's tread.** The beck's line mark grades
its own shoulder, so only `2 × (half-width − tread)` blocks in the middle are
pinned flat; at tread 3 a channel of radius 3 reached into the lofted part and
`DR-BANK` read a straight-sided wall three courses over the water's own line.

## What went wrong

**The gill carried two shoulders and the board is 48 blocks wide.** Two ten-wide
rims left the beck's own band nothing to sit in, and the second won the cells
beside the water and stood a rim on the bank the channel was about to be carved
into. One shoulder — a scar west, a bank grading away east — is what a gill cut
into a dipping bed looks like anyway.

**`RL2` read 226 steps taller than a player can scramble before the flight was
authored**, and named the cause itself: *the elevation is there and was never
graded.* A relief graded across the seam would have deleted the boundary; the
flight states it.

**`RL3` still stands, and it is the terrace's own face.** The bench and the west
shoulder meet on a three-block step over 27 cells of boundary, which is where the
vault's west wall is built. It is the made-ground-meets-grown-ground seam that
`WHAT-A-BOARD-IS-MADE-OF.md` asks for rather than a fault to grade away.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| core | `(-4, 62)` | casing y28, lava y29–31, lid y32, on the deck's y21 |
| undercroft | `(-8, 64)` | deck y21, **nine courses of air**, ground y11 |
| shaft | `(-10, 58)` | ground y11 and **no deck over it** |
| west shoulder | `(-22, 62)` | tops at y20, one under the deck |
| the void scan | — | **42 roofed voids, 0 SEALED**, largest 2 969 cells |
| whole board | `48 × 240` | 8 272 walked · 200 scrambled · 202 barrier · 6 faces |
| coverage | — | **4.6% dead** |
| dressing | — | 34 placed, **0 declined** |
