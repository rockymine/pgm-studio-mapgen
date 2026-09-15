# Tunnel mouths

`tunnels` states a bore and leaves every one of its roofs a landmass nobody can reach. This card is the other
half: the four ways a bore meets the sky — a cut with a flight running down it, a terrace in front of a
portal, a slot in the ceiling, and a well with a stair in it. Open it in the studio as
`technique-tunnel-mouths`, or read `tunnel-mouths.layout.json`.

The stack is the one `tunnels` sets out and this card assumes: `base` at `floor` 0 four courses (the bore's
floor, top block y3), `walls` at `floor` 4 four courses, `lid` at `floor` 8 four courses, so the bore is the
four courses y4–y7 the walls layer left alone and the board's surface stands at y11. **Eight courses separate
a bore from the sky over it**, and every plot here spends them differently.

Every plot is its own group on every layer it draws on, `mirrors: false`, on a board whose `mirror_mode` is
`none`. Flights are oak planks so a tread is legible in a section; the rest is `tunnels`' own palette.

| Plot | Where | What it shows |
|---|---|---|
| `descent` | x 0–30, z 0–56 | a ramp down into the north mouth, a stair of one rectangle a tread up out of the south |
| `terrace` | x 40–70, z 0–56 | the base and the lid shifted: an apron under open sky, and the mouth in the wall behind it |
| `skylight` | x 0–30, z 66–106 | the lid banded round a slot — light into the bore, and nothing else |
| `stairwell` | x 40–70, z 66–106 | a well in the lid halfway along, the bore widened under it, one flight climbing out |

## A cut is where the lid is not drawn

`descent` runs one bore from z0 to z56 and roofs only the middle of it. Read along x 14, the plot is five
stretches:

```
z 0–5     solid to y11          the approach — base, walls and lid at full width
z 6–13    the ramp              base only: no walls, no lid, open sky
z 14–33   the bore              base, then four courses of air, then the lid
z 34–49   the stair             base only, one rectangle a tread
z 50–55   solid to y11          the far approach
```

Nothing is subtracted and nothing is overridden. The cut is drawn by **banding the walls and the lid around
it** — where `descent`'s lid would be one rectangle it is seven, and the two stretches over the cuts reach
only as far as the rock either side:

```json
{ "id": "de-lid-cut-w", "floor": 8, "base_height": 4, "min_x":  0, "max_x": 12, "min_z": 6, "max_z": 14 }
{ "id": "de-lid-cut-e", "floor": 8, "base_height": 4, "min_x": 17, "max_x": 30, "min_z": 6, "max_z": 14 }
```

**The walls are banded the same way, and that is not tidiness.** On one layer the taller surface wins the
column outright, whichever was written first, so a wall drawn as one rectangle across the mouth of a cut
plugs it: on `opus5-sandcaster-ii` a 15-course end wall over a 7-course ramp left `(−8, 60)` reading solid
y0–y21 with no air in it, a three-block plug sealing both mouths, and an `SK11` that was easy to write off
(`GENERATION-NOTES.md`, *the taller override-add wins the column*). `descent`'s rock is therefore
`de-wall-w` and `de-wall-e`, one either side of the cut, and never one rectangle across it.

The ramp down is **one polygon**, thickness 12 at its head and 4 at its foot over eight blocks:

```json
{ "id": "de-ramp", "type": "polygon", "floor": 0,
  "vertices":       [[12, 6], [17, 6], [17, 14], [12, 14]],
  "anchor_heights": [12.5, 12.5, 4.5, 4.5] }
```

The stair up is **eight rectangles**, each two blocks deep and a course thicker than the last — `floor` 0
with `base_height` 5, 6, 7 … 12, so the treads top out at y4, y5, y6 … y11. Both forms are here because both
are drawn: a polygon states the grade in one shape, and a run of rectangles states every tread outright,
which is what an even stair authored on the canvas comes out as — the canvas rounds anchor heights to whole
blocks, so the half-block form a two-deep polygon stair needs can only be written into the document
(`techniques/ramp-and-stair`). The section along x 14 prints the two side by side, one character a block:

```
grnd   cccccccba98765cccccccccccccccccccc5566778899aabbcccccccc
       ↑ approach ↑ ramp  ↑ the bore, roofed  ↑ stair, two deep a tread
```

The ramp's anchors differ by eight over a run of eight, which is what makes it one course a block:
`columns.txt` reads y11 at z6, y8 at z9 and y4 at z13, and `walks.txt` walks it for nothing in both
directions. `techniques/tunnels` measures what happens to a flight whose anchors and run disagree.

## A terrace is the same eight courses, spent as sky

`terrace` draws its base over the whole plot and starts its walls and its lid at z20. The eight courses that
would have been rock and ceiling are simply not there, so z0–z19 is a flat apron at the bore's own floor
level with open sky over it, and the wall at the back of it stands from y4 to y11 with the bore's mouth cut
through it — five blocks wide, four courses tall.

```json
{ "id": "te-base",   "floor": 0, "base_height": 4, "min_x": 40, "max_x": 70, "min_z":  0, "max_z": 56 }
{ "id": "te-rock-w", "floor": 4, "base_height": 4, "min_x": 40, "max_x": 52, "min_z": 20, "max_z": 56 }
{ "id": "te-rock-e", "floor": 4, "base_height": 4, "min_x": 57, "max_x": 70, "min_z": 20, "max_z": 56 }
{ "id": "te-lid",    "floor": 8, "base_height": 4, "min_x": 40, "max_x": 70, "min_z": 20, "max_z": 56 }
```

Four shapes, and three of them are `tunnels`' own anatomy with `min_z` moved twenty blocks. **The shift is the
whole technique**: a portal is not a shape, it is the place two of the four pieces stop short of the third.

The flight up the wall face is the fourth. It stands on the `walls` layer — the base layer is already spoken
for under it, y0 to y3 — as a polygon at `floor` 4 with anchors `[0.5, 0.5, 8.5, 8.5]`, so its treads top out
at y4 … y11 over eight blocks and the last one arrives level with the roof at z20. Read at x 44, `(44, 12)`
tops at y4, one step up off the terrace, and `(44, 19)` tops at y11, level with the ground it joins. That
landing is what `SK26` asks for: a flight whose climb ends at a drop is not a way up anything.

## A skylight is a way for light and not for players

`skylight` bands its lid round a slot over the bore — four rectangles, the same way `tunnels`' corner bands
its rock:

```json
{ "id": "sk-lid-n", "min_x":  0, "max_x": 30, "min_z": 66, "max_z":  82 }
{ "id": "sk-lid-w", "min_x":  0, "max_x": 12, "min_z": 82, "max_z":  90 }
{ "id": "sk-lid-e", "min_x": 17, "max_x": 30, "min_z": 82, "max_z":  90 }
{ "id": "sk-lid-s", "min_x":  0, "max_x": 30, "min_z": 90, "max_z": 106 }
```

The hole is x12–16, z82–89 — the bore's own width, eight blocks of it — and it reaches from y8 to the sky.
The column at (14, 85) reads four blocks and stops at y3: no lid at any height. Next door at (14, 75) the
same bore is roofed.

It is the one plot here that leaves a complaint standing, and the complaint is the technique stated back:

```
SK11  1160 place(s) of standable ground around (0, 66) @13 …
SK11   200 place(s) of standable ground around (12, 66) @5 …
```

1160 is the roof, which no flight reaches. 200 is 5 × 40 — **the whole bore floor**, not the forty cells under
the slot: the slot gives that floor open sky, and sky-lit ground with no route onto it is what `SK11` counts.
The studio is saying, exactly, that a hole in a ceiling is not a door. The other three plots raise nothing.

The same slot splits the plot's covered space in two. `voids.txt` reports the bore as **320 cells at z66–81
and 320 more at z90–105**, with nothing between them, because the cells under the slot are not roofed and a
covered-space scan only counts what is.

## A well is a mouth in the middle of a run

`stairwell` puts the way in halfway along instead of at an end. Three things happen in the same eight blocks
of z:

- the lid is banded round a well at x58–65, z82–87;
- the east rock is interrupted over the same z, so the bore widens from x52–56 out to x57;
- one flight climbs east out of the widening, `floor` 4 and anchors `[0.5, 8.5, 8.5, 0.5]` — rising along x
  rather than z, which is the only difference between this polygon and `terrace`'s.

Read across at z 85, the flight's foot at x58 tops at y4 — one step up off the bore floor at x57, whose own
column carries the four courses of air the bore is — x59 tops at y5, and the head at x65 tops at y11, level
with the roof at x66. `walks.txt` walks the whole of it: from (68, 85) on the roof at y12, down the flight,
into the bore and south to (46, 104) — 30 blocks, no drop, worst step 0.

**A widening is the walls layer not drawn, exactly as a bore is.** There is no shape for the chamber.

## The reads that settle it

Every walk on this card answers `worst step 0`, and that is the only proof a mouth is a mouth. A ramp is
one shape and a picture of it is a wedge whether or not it rasterizes evenly; the walk is what says a player
gets down it. Three of them are worth reading in full:

| Walk | Answers |
|---|---|
| `(14, 2, 12) → (14, 54)` | `descent` end to end — over the approach, down the ramp, through the bore, up the stair: 52 blocks, 0 drops |
| `(44, 4, 4) → (44, 30)` | `terrace`'s flight, from the apron onto the roof |
| `(68, 85, 12) → (46, 104)` | `stairwell` from the roof into the bore |

**The `y` in `from=x,z,y` is not decoration.** A stacked column has a place at more than one height and the
read picks one. At (14, 20), where the bore's floor is y3 and the roof's is y11, `from=14,20` with no `y`
starts at **y4** — the bore — and so does `from=14,20,4`. State `from=14,20,12` and the same read starts on
the roof and answers `drop -7 at (14, 34)`, where it walks into the stair cut. Two of those three are the
route somebody meant, and only the `y` says which.

- `voids.txt` — five roofed voids, none sealed. Two of them are `skylight`'s one bore, cut in half by its
  slot; the 400 cells at x12–16, z14–33 are exactly `descent`'s roofed middle, its two cuts being open sky
  and therefore absent.
- `columns.txt` — nineteen columns: the ramp course by course, the terrace under open sky beside the mouth
  behind it, the lit floor under the slot beside the roofed floor next to it, the flight head and foot.
- `section.txt` — eight cuts. Every mouth on this card is invisible in a heightmap and unmistakable in a
  section.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west) — where the cuts, the slot and the well all
read from above as holes in a lawn; `xray.png`, which is where the bores under them appear; and `layers.png`,
one isometric per layer, in which `descent`'s seven lid rectangles and `skylight`'s four are the picture.
