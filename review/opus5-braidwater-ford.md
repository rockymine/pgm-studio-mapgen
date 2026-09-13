# Braidwater Ford — a wide braided river

The two sides meet at three fords and nowhere else. Between them the cut bank is a face a player
cannot walk up, and the river braids around shingle bars in the 32 blocks between.

Slug `opus5-braidwater-ford` · 104 × 224 blocks · rot_180 · 20 a side · destroy.

## How it is meant to play

Each team comes off a wooded terrace — the carr — down a gentle valley side onto the haugh, the low
flat beside the water. From there the river is 32 blocks of braid at y13–15, and the bank drops to
it over two blocks. Three crossings cut through that bank: a wide one on the centre line with a
bluff over it, and a narrow pair at x ∓36 with alder on one hand.

The goal sits back on the carr at (−26, −58), so an attacker's whole journey is: cross the haugh in
the open, choose a ford, wade it, climb the far bank, and then still have 40 blocks of terrace to
cross. Fifty blocks from its own spawn and 167 from the enemy's.

## The three fords, and why two of them are one shape

**This is the board's honest limitation and it is a symmetry result rather than a choice.** Under
`rot_180`, a crossing of an on-axis river is either its own image (one, on the centre line) or one
of an image pair. Three fords are therefore at most **two** authored characters: the centre one, and
the pair at x ∓36. There is no arrangement of three crossings on one axis that gives three.

What can be made different is what each crossing *costs*, and that is done off the axis rather than
on it. The centre ford is wide — an 11-cell reach with a 7-cell tread — long, and overlooked by a
bluff push whose skirt stops 5 blocks short of the lip. The pair are narrow: a 6-cell reach, a
3-cell tread. And the alder copse is authored on the **west** ford's north bank only, so its
rot_180 image lands on the **east** ford's south bank: crossing west you enter cover and leave in
the open, crossing east you do the reverse. Two crossings out of one authored shape that are not the
same way round drawn twice — but two, not three, and the review should say so rather than claim
otherwise.

## The techniques, and what each one bought

**The scarp's trace direction is the whole cut bank.** A `scarp` pins `high` on one side of its line
and `low` on the other, and which is which is the order the points are written in. The high band's
normal is (−dz, dx): a lip traced **east to west** puts high to the north. `lip-n` runs from
(50, −17) to (−50, −18) for exactly that reason — traced the other way the shelf would land in the
river and the drop on the bank, which cost a previous board 418 barrier steps against 268. Under
`rot_180` the image reverses with the original, so one lip traced the right way is both banks.

`face: 2` is what makes the bank a bank. A face of 6 grades into a walk-up; 2 is a drop a player
takes downward and cannot climb, which is the entire reason the fords are the crossings.

**A push skirt grades whatever it reaches, so both pushes are held clear of the lip.** A push is
added after the marks solve. The valley-side push reaches z −38, twenty blocks short of the lip; the
bluff that overlooks the centre ford reaches z −23, five blocks short. Near enough to loom, far
enough to leave the bank sharp.

**The fords are `line` marks stated after the scarp**, so they win the cells the lip would otherwise
have walled — bank, shallows, bed, shallows, bank, with a `tread` that grades the rest of the band.
**Both banks of every ford** then carry an `area` mark, which is that instrument's own case: flat is
the point where a crossing lands.

**The channels are reaches between the fords and never across one.** Water is the one prop that
changes the ground: a channel reads the surface top and carves down from it, so a channel laid over
a ford would cut the crossing to its own bed depth and the ford would stop being wadeable. Four
authored reaches become eight under the fan, each sized to the water it holds.

## What the ground is made of

- **ground** — ochre and brown floodplain silt. Coarse dirt and podzol in one surfacing course, over
  dirt, over clay and the gravel the river laid down. Finished on the **slope** axis.
- **built** — pale birch on cobble footings, the one light thing on a brown board.
- **accent** — the shingle: gravel and sand bars between the braids, 3.4% of the ground.

The biome is **Swampland** (`#6a7039`), chosen before any block was placed. A tinted block's family
is the biome's to decide: podzol against Plains grass (`#91bd59`) reads as neither ground, and
against this one the pair is a single damp, leaf-littered floor — which is what a floodplain is.

Census: `silt` 80.2% · `carr` 16.3% · `bar` 3.4%, with borders, and `9:0 Water` in two of the three.

## What went wrong

**`PT1` refused the first build outright.** The carr's surface put podzol one course under grass. A
surfacing block is exactly one course thick and what is under it is soil, so grass and podzol now
share one top course as a two-block patchwork instead of stacking.

**`RL5`: 27% level ground against a bar of 30.** Four area marks each carried a `bevel`, and a bevel
grades a mark's shoulder into its neighbour — so a bevel on every mark is a board of nothing but
shoulders, walkable end to end with nowhere to stand. The two big flats, the terrace and the haugh,
are meant to be flat to their edge and now carry none.

**`RL3`: the room pad and the compiler's own spawn mark disagreed by ten courses** over 72 cells of
boundary. The valley-side push's skirt had reached the spawn and lifted the ground the shell is
stamped on, while the shell stands where the plan put it. Moving the push's ring south until its
skirt stops short of the shell settled it — the same "a push is added after the marks solve" fact
that the scarp had to be protected from, met at the other end of the board.

**`DC3`: hardened clay is not a material this studio builds.** The goal was built in ender stone
whatever the document said, which is the kind of substitution that is invisible in a render.

**`DR-DRY` on all four braids, and the shore was not the cause.** *"The basin is dug to the water's
own depth and holds none… where the hollow reaches further, the difference is a dry trench beside
the water."* Narrowing the shore barely moved it. Reading the coordinates instead of the prose —
`first at (-27, 15, -17)`, and 15 was the water line — showed the real cause: the **scarp** cuts the
whole river bed to its `low`, and `low` was *below* the water line, so every bar between the braids
was dug ground under a water surface standing proud of it. Putting the bars one course above the
water line and carving the channels out of them took the four complaints of 110, 132, 58 and 56 dry
columns down to one of **2**, at the map's west edge where a channel runs off the board.

**And then the board did not do the one thing it is for.** With the bank finished, the read that
matters is whether the two sides meet anywhere but a ford. They did:

    across the centre ford (x 0)      rises 4, falls 4, worst step 2: 0 barrier, walked end to end
    between fords     (x -18)         rises 5, falls 5, worst step 2: 0 barrier, walked end to end
    between fords     (x  20)         rises 6, falls 5, worst step 2: 0 barrier, walked end to end

A bank of five courses over a `face` of 2 is two steps of two, which is a scramble, not a wall — the
haugh was at 18 and the bars cannot go below 13 because they have to stand above the water. So the
haugh went up to 22 and the terrace behind it to 26: nine courses over a face of 2 is a drop a
player takes downward and cannot climb, and the fords become the crossings the board's sentence
claims. Nothing in the plan tier, the gate or any render said otherwise — three transects did.

**The claim, finally measured.** With the haugh raised and the bank marks moved outside the ford
ramps, the walk read answers the board's sentence directly:

| crossing | costs |
|---|---|
| the centre ford, x 0 | 68 blocks, **0 placed**, 0 drops |
| the west ford, x −36 | 68 blocks, **0 placed**, 0 drops |
| the east ford, x 36 | 68 blocks, **0 placed**, 0 drops |
| between fords, x −18 | 80 blocks, 0 placed — the router walks 12 blocks *to a ford* |
| between fords, x 20 | 78 blocks, **7 placed**, 1 drop — forcing it costs seven blocks |

Crossing at a ford is free; crossing anywhere else is a detour to a ford or seven placed blocks.
That is the board.

## Numbers

    03-slopes   21,467 walked · 807 scrambled (3.5%) · 1,022 barrier (4.4%) · 20 faces
    06-claims   placed 60, declined 4 — three DR-BANK and one DR-DRY, all on water channels
    relief      group team  cells 11,648  low 13  high 41  symErr 0
    coverage    58.9% reached · 9.8% decorated · 28.8% dead · 2.5% route
    preflight   round-trip · mirror · buildability · traversability all pass — gate OPEN

**What is still wrong.** Raising the haugh to 22 also raised the ground the braids run through where
they pass near a ford's band, so three reaches carve a straight-sided trench — *"braid-a is 3 deep
and its carve cut 8 course(s) of ground away above its own line, a wall from y13 to y20"*. The water
is there (`column` reads `y12 Water` across the braids, and the census carries `9:0 Water`), but
those banks are cut rather than shelved. The fix is to move the braids' x ranges clear of the ford
bands; it wants a seventh drive and did not get one.

## Coordinates to check in game

| what | where |
|---|---|
| the cut bank, high to the north | the `lip-n` scarp along z ≈ −17, high 18 low 13, face 2 |
| the wide ford | x 0, crossing z −26..26, an 11-cell reach with a 7-cell tread |
| a narrow ford | x −36, same crossing, a 6-cell reach with a 3-cell tread |
| the bluff that overlooks the centre | push ring about (−24, −44), skirt stopping at z −23 |
| the goal, back on the carr | (−26, −58) |
