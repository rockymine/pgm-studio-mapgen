# Hollowmarch — a composed board given its ground

> A CTW board taken from the composer at 32 players, shifted to make room for a middle island, and
> then given every one of its heights by relief. Nothing on it is a wall or a rim: the cliff you see
> from the void is the surface stack, and under that the fill.

**In one sentence:** a green downland board on three islands — a double-hole hub, a frontline that
splits into two prongs, four wool rooms and two spawns standing on pads pre-raised above the ground
so the relief runs up to meet them — with seven rock crags folded into it, each one leaning the same
way: a face that melts into the terrain on its own side and a cliff facing the attack.

110 × 220 blocks, `rot_180` about the origin, base surface 14, ground y10..y27, build zone
x −40..40 · z −30..30. Three landmasses: one island a team, one on the axis between them.

## The board came out of the composer

`GET /api/compose?players=32&symmetry=rot_180&hub=double-hole&front=twin&wools=u` — seed **1233**,
score **0**, `{"wools": ["l","u"], "hub": "double-hole", "frontline": "twin"}`. That is the ask:
a hub made of two holes, and a frontline that is a bar with two prongs off it, which is the U opening
forward. (The composer has no `u` *frontline* — `u` is a wool family, and `twin` is the split form.)

The pinned plan was opened and changed in four ways, and in no others:

| Change | What | Why |
|---|---|---|
| shift | every piece `+4` cells of z (**+20 blocks**) | to clear a middle island inside the build zone |
| add | `mid-isle`, `[-4, -3, 8, 6]`, `mirrors: false` | the island on the axis; its own `rot_180` image |
| raise | `globals.surface` 9 → **14** | the composer flattens at 9, and 9 is the surface depth: a rim cut into it leaves two blocks of ground |
| raise | seven pads to 16 · 17 · 18 | the spawn and the two wool approaches, each pad **exactly one block over the pad it is reached from** |

| Piece | Cells | Blocks | Surface |
|---|---|---|---|
| `spawn-t1` · `spawn-room` | `[4,12,2,3]` · `[6,12,2,3]` | x 20..40, z 60..75 | 17 → 18 |
| `wool-a-t1` · `wool-a-room` | `[-7,18,6,2]` · `[-5,20,2,2]` | x −35..−5, z 90..110 | 17 → 18 |
| `wool-b-t1` · `-t2` · `-room` | `[-9,11,2,2]` … | x −55..−35, z 40..75 | 16 → 17 → 18 |
| everything else | — | — | 14 |

The seven raised pads are `relief_scope: hold` shapes. A held shape keeps its own level and the
surface around it is solved knowing where it has to arrive — which is the whole point of raising
them. **Two held pads side by side cannot be ramped by a relief mark**, because both are held; that
is why the ladder is one block a pad rather than a jump to the room.

## Every height is relief

`globals.surface` is flat at 14 and no piece but the seven pads states a height. Everything else is
two relief documents — one for the team island, one for the neutral — and nothing else.

**Team island** (`base 14`, `reach 24`, `step 1`, `stairs`, grain 1.2 @ 12): eight marks and four
pushes. `front-flat` holds the frontline at 13, flat, because that is the ground a bridge launches
from; `front-bank` is a line at 18–20 behind it, which is what the frontline looks over; `hub-floor`
is the lowest ground on the island at 12, between the hub's two holes; `west-shoulder`,
`north-swell` and `east-bench` are the three raised backs the wool lanes climb. Read back: **cells
3358, y12..27, relief 15, symmetry error 0**.

**Neutral island** (`base 14`, `reach 16`): a `saddle` at 13 across the crossing, a `horn`/`step`
pair either side, and the pond — `pond-rim` at 12 and `pond-floor` at 10, both centred on the origin
so the ring is its own `rot_180` image and one statement serves both teams. Read back: **cells 1675,
y10..19, relief 9, symmetry error 0**.

**A line mark's `width` reaches either side of the line.** `front-bank` at width 12 wrote over the
frontline flat down to z 38 and a push stacked on it — a seven-block wall across the necks of the
two prongs, which is the launch ground. The readback called that "places 5" and nothing else
mentioned it. Width 5 at z 54..60, and the two front pushes moved north to z 60, is the fix.

## The outline is faceted, not curved

`s0` (the team island) went from **18 authored vertices to 49**, `s8` (the neutral) from 14 to 32,
by cutting every edge into runs of about five blocks and stepping the joints ±3 along the edge
normal, alternating sign. No Bézier handles anywhere. Three seam spans — the two frontline faces and
the coast beside the wool-b room — are held straight, because a faceted edge across a seam is a
faceted edge that does not match its mirror. Self-intersections: **0**. Neutral-island symmetry
error: **0.000**.

## The crags

Seven `addShapes`, all `height_mode: raise`, all in one theme (`scar` — chalk rubble over stone),
all seven-or-eight-vertex irregular rings with no handles, and **all leaning the same way**.

The lean is stated as the brief asked: **three points**, and a plane through them. `plane3` takes
three `(vertex, height)` pairs, solves `a·x + b·z + c = h` and fills every remaining vertex from it.
The three are picked by z: the **two highest-z vertices at 0**, so that face is flush with the ground
and melts into it, and the **lowest-z vertex at the lift**, so the face turned toward the attack is
the cliff. Every crag on the authored half therefore raises the same shoulder, and the `rot_180` fan
gives each team the cliff and its own side the ramp.

| crag | centre | ring | top y | raised face | smooth run | worst riser |
|---|---|---|---|---|---|---|
| `scar-front-w` | (−25, 54) | x −32..−19, z 45..64 | 25 | +9 over 6 | −4 over 16 | 2 |
| `scar-front-e` | (6, 54) | x −3..14, z 45..62 | 23 | +11 over 7 | −3 over 15 | 4 |
| `scar-hub-w` | (−28, 75) | x −33..−21, z 68..81 | 28 | +4 over 7 | −7 over 12 | 1 |
| `scar-hub-e` | (13, 73) | x 8..20, z 68..78 | 21 | +2 over 4 | −17 over 8 | 6 |
| `scar-back` | (−11, 79) | x −15..−7, z 74..83 | 25 | +12 over 7 | −3 over 8 | 5 |
| `scar-isle-w` | (−20, −4) | x −25..−14, z −11..1 | 16 | +5 over 7 | −4 over 11 | 3 |
| `scar-isle-e` | (20, 4) | x 14..25, z −1..11 | 17 | +5 over 10 | −6 over 6 | 3 |

Each row is one column transect down the ring's centre line, so it is a slice and not the whole
shape. `scar-hub-e`'s "−17 over 8" is the island's own coast falling away past the crag, not the
crag; its ring stops two cells short of the edge.

**A crag stands on a pad of its own.** A `raise` reads the ground under each cell and hands whatever
slope it finds on to the top, so the rise it makes at the foot is that slope *plus* the lift: the
first cut of `scar-front-w` stood on a nine-block terrain step and read as a fourteen-block wall.
Levelling the footprint first — an `area` mark at the crag's ring, grown 1.3× — puts the whole face
in one place, which is the anchor plane, and leaves the pad's own edge to the solver's one-block
stairs.

**A crag over void falls to its own floor.** A `raise` has no ground to read past the coast, so two
cells of `scar-hub-w` that hung over the sea built seven-block cobble stubs at y0..y6 beside the
island — visible from the map and from nothing else. Every ring is now checked against the land
model for hole cells and sea cells before it is used, and all seven come back **land ≥ 50, sea 0,
hole 0**.

**The composed board's holes are made by arrangement.** The hub's two slots and the U wool's notch
are the shape of the pieces, not a marked region, so nothing declines a shape dropped on one — it
simply fills it in and the layout the composer was asked for is gone. The seating check tests for
that explicitly: a void cell with land in all four directions within 16 blocks is a hole, and no
crag may cover one.

## Nothing is a wall and nothing is a rim

`rim.enabled: false`, `wallEnabled: false`, `wallOnTerrainFaces: false`. Every column on the board is
the **surface stack** down to its depth and the **fill** under it, which means the stack has to read
as a soil profile in section, because on this board a cliff face *is* the stack:

| band | thickness | material |
|---|---|---|
| turf | 1 | noise — grass · grass · coarse dirt |
| soil | 2 | dirt |
| subsoil | 1 | coarse dirt |
| pan | 2 | noise — gravel · stone · cobble |
| rock | 3 | stone |
| fill | rest | noise — stone · stone · andesite · cobble |

The islands stand fifteen blocks out of the void, so most of what is seen from the side is fill; a
single stone id there reads as a poured wall, which is why it is a noise.

## Dressing

37 props, **nothing declined**. Four roads (spawn to each wool, hub to each prong), seven grass
tongues drawn down each crag's smooth face, three texture brushes, the pond, three boulders, sixteen
trees in five stands, and three flora fields.

The pond is one `water` prop centred on the origin, so the traced line is its own `rot_180` image and
one statement fills the basin the relief dug: radius 3, depth 2, shore 2, over a voronoi bank of
clay · gravel · coarse dirt.

## What it costs

- `plan/inspect` score **0**, no hard terms. Two `CT12` island-gap notes: the frontline to the middle
  island is **15** blocks (the bottom of the 15–40 window) and frontline to frontline is 75, which is
  the strait the middle island sits in.
- `preflight`: codec parity, mirror check on spawn/protection, wool/room and build, all six
  placements on solid ground, spawn↔objective chain connected. **Export gate open.**
- `coverage`: reached 7806, dead **176** of 8025 = **2.2 %**, in four patches — 58 at (−27, −6) and
  its mirror at (24, 5), 34 at (19, −75) and its mirror at (−21, 74). All four are ground no journey
  passes through, each one block from ground that is used; none of them is unreachable.
