# Quatrefoil — the run

## What I set out to build

A four-team capture board from a plan handed over as JSON, on the palette handed over with it: five muted
colours — a sage teal, a camel, a pale oak, a green-grey and a dark coffee. The brief attached to them was
that the terrain should be **terraformed naturally**, and that the middle island should be its opposite —
**angular and obviously made** — with natural blocks softening its edges.

So: four wooded corner quarters over a mossy grey-green moor, four pale sand spits on the axes, and a
stepped stone keep in the middle that every route crosses and nobody owns. The quarters are rolled by
pushes and carry no rim at all; the keep is flat, sheer, kerbed on every drop, and has beds of podzol cut
into its deck with flowers and birches growing out of them.

The board is `maps/opus5-quatrefoil`, the documents are `specs/opus5-quatrefoil/`, and what it is and how
it is meant to play is `review/opus5-quatrefoil.md`.

## What I got wrong

**I believed a `symmetryError` of 0 for four builds.** The board is `rot_90`. `relief/read` answered
`symErr 0` every time, `preflight` passed the mirror check every time, and the heightmap looked wrong in a
way I first read as noise. It was not noise: **two of the four quarters had no relief at all.** Measured
with the read that is not a projection —

```
GET /map/{slug}/column?at=-78,-45   →  y 17   (the swell)
GET /map/{slug}/column?at=45,-78    →  y  8   (its rot_90 image: the shape's flat base height)
GET /map/{slug}/column?at=78,45     →  y 16   (its rot_180 image: the swell again)
```

`SketchRasterizer.RasterizeLayout` fans a relief-bearing group by mirroring its shapes onto each orbit
axis and then reading each image cell's height back out of the group's own solved field. It read the
image back through **the same axis that placed it**. Every mirror and the half-turn are their own inverse,
so that was correct for every board the studio had built; a quarter-turn is not, and a `rot_90` image read
back through `rot_90` lands on the `rot_180` image's ground, which the field does not cover — so the copy
fell through to its shapes' flat base heights.

The reason nothing said so is worth writing down: **`relief/read` measures the one solved field, not the
four copies of it.** `symErr 0` is a true statement about a field that only two of the four teams were
standing on. Nothing else on the board is asymmetric — shapes, paint, props and structures all fan
correctly — so every render except the heightmap looks right, and the heightmap looks like weather.

Fixed in the studio as `WE75`: `Symmetry.Inverse` names the axis that undoes a given one, and the
rasterizer's mirrored read-back takes it. `SketchRasterizerTests` gains a `rot_90` orbit case asserting
all four images carry the same solved height; 1,199 Pgm tests and 260 Geom tests pass.

**Before I found it, I "fixed" it in the spec, and the fix was worse than the bug.** I authored every mark
and push twice — once as stated and once a quarter-turn on — which does put terrain under all four teams
and is exactly the wrong shape of answer: the second copy lands in a different quadrant of the authored
unit, so once the studio was fixed each push applied twice at the same place and every amount doubled. A
workaround for a symmetry bug is indistinguishable from a design decision three commits later.

**I read a six-block wall as a bug in the shapes.** A transect down `x = −72` read `8 · 8 · 8 · 14` where
a hillside was meant to be, and I spent two passes moving the building that stood on it. The building was
innocent: `swell-south` had crown 4 over a falloff of 8 on a 9-vertex ring with wobble 0.2, which is 0.63
courses a block outside the ring against 0.5 inside it — and with a ring that irregular, some directions
got no skirt at all. Widening the skirt to 11, dropping the crown to 3 and taking the ring to 13 vertices
at wobble 0.10 took the relief read from **221 scrambled / 18 barrier** to **36 / 10**. A range is a wall
unless its two gradients agree, and `GENERATION-NOTES.md` says so; I authored the numbers before I read it.

**I authored the board at the scale it was handed to me.** The plan came in at `cell: 1` — 98 × 98 blocks,
every gap 6 to 8 across. `/plan/evaluate` refused it twice on hard terms (`G2` corridor width, `G5` gap
hop) and I spent a while trying to widen individual gaps before noticing that every one of the five
complaints was the same complaint: the board was half the size the geometry rules describe. `cell: 2`,
nothing moved, and the board came back `valid` at the first ask.

## What I could not say

**Missing from the system — a prop that hangs a block on a vertical face.** The brief asked for vines on
the keep. A theme's `wall` bucket paints the *solid* blocks of an exposed face, so a vine stated there
replaces terrain and leaves a hole; the dressing pass has `tree`, `boulder`, `house`, `stroke`, `flora`
and `water`, and `flora` sets one block into the air cell at `SurfaceTop` — always on top, never on a
side. Nothing in `openapi.json` places a wall-attached block. What the keep got instead is planted beds
cut into its deck and flora over them, which is a different answer to the same brief and not the one that
was asked for.

**Out of reach, not missing — the relief fold under a quarter-turn.** `ReliefSolver.Fold` discriminates
`mirror_x` and `mirror_z` and treats everything else as a half-turn. On this board the fold is a no-op
(no group spans the axis with its own image inside its own footprint) so nothing is wrong in the world,
but a `rot_90` group that *did* straddle the origin would have its field folded onto a half rather than a
quarter. The mechanism exists and the mode is not among the ones it names. Filed here rather than as a
fault, because I could not build a board that shows it.

**`GET /map/{slug}/coverage` answered `500 RQ2` once**, on a board whose objectives are wools and whose
plan had just changed, and answered 200 on the next run with the same documents. I could not reproduce it
and have no more to say than that it happened.

**`04-routes.txt` is never written on a wool board.** The driver's text sweep ends `no route between a
spawn and a goal` on every run of this board, so the third of *the three numbers* is missing by
construction — on a board where the whole question is what a raid costs. The read itself is there and
answers fine by hand:

```
GET /map/{slug}/walk?from=-86,-79&to=40,-40&aim=reach&format=text
  ROUTE 153 blocks, 19 placed, 2 drop(s), worst drop 10
```

Out of reach rather than missing: `walk` is the read `04-routes.txt` is made of, and something between a
wool intent and the route enumeration does not pair a spawn with a wool.

**`WX8`'s iron cube stands *outside* the room shell, in the ring between the shell and the piece edge.**
I read "inside the piece" and put the marker in the middle of the hall three times. The rule's own text
says it plainly and I did not read it until the third refusal; the fix was `GET /api/rules?rule=WX8`,
which is the first thing the brief tells you to do.

**`POST /plan/room` does not answer for the facing.** It returned `{"at":[10,12],"footprint":[1,5,18,14]}`
for a spawn whatever `facing` the plan stated, while the compiled shell moved with the facing — so a
footprint copied from that answer pins the door apron to the `−z` side of a room whose door opens `+z`.
Stating no footprint at all is the honest thing: `WX1`'s default follows the facing.

## What the loop cost

Five full drives and eleven `loop.py` passes. The loop is the difference between the two: a drive is ten
minutes and answers everything, `loop.py --candidates <prop> x,z x,z …` is twenty seconds and answers the
only question a drive was being run for. Eleven declines — `DR-ROAD`, `DR-CLAIM`, `DR-KEEP`, `DR-SITE`,
`DR-CROSS` — were cleared by naming six candidate positions and reading which stood, and the board ships
at **placed 132, declined 0**. The claims raster says where to try; the candidates pass says whether the
try lands, and guessing costs a build each time.

The other thing worth its place: **`GET /api/rules` is 147 rows and reading it first is cheaper than
meeting them one build at a time.** Every refusal this board hit was in that list with its number in it —
`ST10`'s 20 × 30 region cap, `G5`'s 10–20 hop, `WL11`'s Δ1 at a room's door, `BZ6`'s ban on a mid zone
touching a wool piece. The ones that cost me a cycle are the ones I had read and not believed.
