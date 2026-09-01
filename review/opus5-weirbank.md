# Weirbank — half of Millrace's box, and what that half could not keep

Two L-shaped headlands over a gulf, each carrying a tarn, their necks reaching east to quays that face
each other across twenty blocks of void with one level bridge between them.
130 × 120 blocks against Millrace's 250 × 240 — half the bounding box, a quarter of the area — and the
same art direction: three grounds, each a two-shade noise pair of one family, every edge between two
of them drawn rather than sampled, everything built in one masonry, the landforms in the relief rather
than in the piece list.

**No grown trees, and every one a spruce.** `TreeForm` has exactly two values and this board uses the
other one: `template`, the vanilla tree of a named species. Fifteen of them in four copses — on the
west slope, behind the spawn, along the neck, and on the tarn's far shore — all spruce, which is a
notched cone on a leader climbing almost the whole height, and the silhouette a taiga wants. Heights
run 9 to 15 against the species' own natural 13; listed at an oak's height a spruce grows a stalk under
a canopy that never widens.

A tree's **log and leaf cannot be separated**. `TreeWood` is one row binding both — `("acacia", Log2,
0, Leaves2, 0)` — a template reads `species` (which carries wood, canopy profile and proportions) and a
grown tree reads `wood`; neither has a log or leaf field. Tested against `POST /terrain/prop-preview`:
a spruce with `wood: "acacia"`, and a spruce with invented `log`/`leaves` overrides, both render byte
for byte identical to a plain spruce. **They are accepted with a 200 and no warning**, so an invented
field here fails silently. A specific log-and-leaf pairing means building the tree as a made layer out
of shapes — a trunk of one and a canopy of another — which is a thing this board deliberately does not
do: the only layer over the compiled ground is the bridge, and every tree here is a `template` prop.

## What the half could not keep

Millrace's shape does not survive being halved, and three refusals say so.

A shelf presenting its whole length to the cut is **`FR6`**, frontline-width 24 against a band of
[1, 16]. One shelf 120 blocks deep is **`LN2`**, max-chain-length 120 against [25, 110] — and
splitting the piece does not help, because the chain is measured over contiguous ground rather than
per rectangle. And with the spawns at the corners of a board this size, **`GO1`**'s ratio ceiling puts
the goal at most L/4 ≈ 39.5 blocks from its own spawn while **`GO4`** demands at least 40: at that
spawn separation the two bands **have no common solution**, so no goal position exists anywhere on the
board and the shape itself has to change.

The L answers all three. The quay narrows the frontage to six cells; the neck puts a junction in what
was a single lane; and routing the walk around the headland lengthens L until GO1 and GO4 overlap.
Final plan: goal **41** blocks from its own spawn (GO4 [40, 90]), ratio **3.22** (GO1 [3.0, 4.0]),
opposing goals **93** apart (GO3 [85, 150]), no violations, no lint, score 0.

**Recorded rather than resolved.** The repository's author reads FR6's frontage band and LN2's lane
length as the model's opinion rather than a fault — a long wide lane is not bad for a destroy board.
This board took the reshape because the gates refuse without it; a future board may be right to argue
instead. GO1 against GO4 is the harder one, and that one is arithmetic rather than taste.

## Millrace's water, and where it had to go

Millrace's race is water on a bed, and a bed is a floor: it joins the two halves with ground a player
walks. The brief's ruling is that the sides meet over a build zone above void and never by a land
connection, so on Weirbank the cut is a true chasm and the water came inland as a tarn on each
headland.

**The weir the board is named for is not on it.** A dam across the tarn's outflow and a flight of steps
down its landward face were drawn while the water was still a sheet lying on the moor, where something
had to explain why it stayed there. Once the basin was cut with `height_mode: "sink"` the water sits in
a dish of its own, and both became furniture for a problem that no longer existed: a wall standing
beside a pond that does not need holding back, and a stair into water a player can walk into. Both are
gone. The name is left as it is — a place keeps its name after the works go — but it now describes
something the board does not contain, which is worth stating rather than quietly leaving.

Two attempts at that tarn were wrong, and neither was reported by any gate:

- **A pool's `radius` is its *shelf*** — how far in from the shore the bed reaches full depth, not the
  pool's size. Set to 15 on a pool 10 half-wide it shelves the whole way and never digs.
- **A relief `area` mark grades; it does not excavate.** It pulls the ground *toward* a height and
  `step: 1` caps how fast it may fall, so a mark at `h 19` under a bank of 29 arrived at **24** and the
  water lay on it as a one-block film. What takes terrain away is **`height_mode: "sink"`**, which
  holds a shape a fixed amount *below* the ground under it. The basin is a sink shape cut six courses
  with a ten-block skirt, floored in its own `bed` theme; the water prop then fills what was dug.

**And then I measured it wrong and shipped a pit.** Reading single columns *inside* the basin gave
"6 blocks deep" and I reported the board as fixed. Six was the water column; the wall was not.
A transect across the whole tarn — which is the read I should have taken — showed the bank at **y38**
and the water at **y25**: a sheer **13-course drop, 16 blocks in two columns**, found in-game and not
by me. Two faults compounded: `brow-north` had been moved off the spawn and straight onto the tarn,
where amount 4 with crown 4 lifts the bank by eight, while the water prop carved its own bed six below
a *stated* line of 25 regardless of what the bank above it was doing. Now: bank **30**, water **27**,
bed **23** — a three-course lip and a shelf running 25 → 23 → 24 → 26.

## The six things a gate did not catch

Every one of these passed every gate. Three were found in a section, one in the plan grid, and **two
only in the game** — which is the honest count, and the reason the last two are listed at all.

| What | How it read | The instrument |
|---|---|---|
| The revetment cut a flat line across a rolling bank, and hung over the chasm with nothing below `y6` | a wall floating | `height_mode: "raise"` holds its cap a fixed amount over the ground under it so the run follows the incline; `floor: 0` carries it to the world's bottom |
| The bridge deck sat at `y30` over a quay at `y23` — seven courses of climb onto a twenty-block crossing | a viaduct nobody asked for | the deck is level *with* the ground it leaves, not level in the abstract: `DECK` set to the quay's measured height |
| The obelisk's base was written at an absolute `y29` over ground the relief had taken to `y22` | a pillar standing in seven courses of air | `seat: "ground"` on the made layers settles the whole run onto the terrain as one unit. The obelisk was later cut for an unrelated reason, so nothing on the board seats this way now — but the fault and the field are both real |
| The spawn terrace held `y34` while the brow beside it stood at `y39` | a platform sunk into the hillside | the fix is not the piece — `PL4` refuses two overlapping pieces with different surfaces, and the spawn nests inside the moor. What sank it was a `push` standing a landform under a stated platform |
| The terrace was `x −64..−46, z 44..60` around a hall measuring `x −60..−51` | eighteen by sixteen of masonry for a ten-block house | the platform is the building's footprint and a little more: `x −62..−49, z 47..60` |
| The flight off the terrace fell `y37 → y29` while the moor beside it stood at `y36` | a masonry trench running *down* into the hill, dead-ending where the ground rose back — it ate the path it was meant to be | a stair is drawn for the fall that is *there*: terrace `y33` to moor `y30`, three courses over six blocks of run, measured after the brow was removed rather than assumed from `BANK` |

A shape declaring a `height_mode` must **not** also carry `relief_scope: "exclude"` — raise and sink
read the ground under their own footprint to know where to stand, and an excluded footprint has none.

## Where the wall meets the bridge

A rectangle's max edge is exclusive, so the bridge's parapets — written `z1..z1+1` and `z0-1..z0` —
are **one column each**, at `z 4` and `z −5`, with the deck between them at `z −4..3`. The revetment
runs along the quay's face at `x −11` and originally stopped at `z ±5`, which left exactly one bare
column beside each parapet: a one-block gap you can only see standing on the crossing. The two runs
now reach `z −4` and `z 4`, so each abuts its parapet's corner.

Moving the wall also uncovered an oak at `(−12, −4)` standing at the bridge head, whose canopy had been
swallowing the whole junction and spilling onto the deck's own fencing — it read as leaves in every
column along the wall line. It stands at `(−16, −11)` now. **A prop at a chokepoint hides the geometry
it stands on**, which is its own argument for keeping the approach to a crossing clear.

## The board is tinted, not painted

`SketchLayout.biome` is the byte each chunk carries — what the client reads to tint grass, leaves and
water — so a board varies in colour without one extra block. It takes three kinds, keyed on `kind`:
`solid`, `cell` and `noise`. Weirbank takes **`cell`**, which the field's own documentation calls the
kind to reach for first, because jittered regions are the shape a biome map actually has: a `cellSize`
of 36 blocks puts two or three regions across each headland, and the edges are jittered cell
boundaries rather than chunk lines.

The palette is **taiga (5) against cold beach (26)**. Taiga is in the studio's named table; cold beach
is not, because that table lists "the ones whose tint an author would reach for" and says a field may
name any id whatever is there — so the palette carries the raw vanilla id.

Read back out of the exported region files rather than trusted: across 46 chunks, **59.2% taiga and
40.8% cold beach, and nothing else**. That check matters, because a `BiomeField` whose properties fail
to bind deserializes to an empty palette and silently answers plains for every column — a wrong biome
looks exactly like an unstated one.

## The objective is 26 fast blocks, not 3 slow ones

The default destroyable is `pillar-3` in obsidian: **three blocks**, each of them among the slowest
breaks in the game. On a board this size that is a coarse progression and it rewards a defender simply
for arriving — three lumps of health, and the walk from spawn is 41 blocks.

`GET /api/objectives/vocabulary` answers the whole vocabulary: six styles — `pillar-1` (1x1x1),
`pillar-2` (1x2x1), `pillar-3` (1x3x1, the default), `cube-3` (3x3x3), `cube-4` (4x4x4) and
`column-plus` (a 3x3 plus-section column, 5 blocks a layer) — and four materials: `obsidian`,
`emerald block`, `gold block`, `ender stone`.

Weirbank takes **`cube-3` in ender stone**. Measured in the built world: End Stone at `y35..37` across
the full 3x3, with **bedrock at `y36` in the centre column** — the documented 1x1x1 hollow core — so it
is **26 breakable blocks**, nine times `pillar-3`'s granularity, each of them quick. The attack now
shows as it accumulates rather than in three lumps. It floats 4 blocks over the ground, which is the
default and is not zero on purpose: a destroyable sitting on the ground is trivially covered.

**The author's ruling, recorded:** obsidian's break time against the distance a defender covers is a
gameplay question with no oracle here. The reasoning taken is that a small board wants a soft goal,
because the defence reaches it quickly and a slow material turns that into a stalemate rather than a
contest.

## The bay nobody drew

The quay reached `z −15..15` while the neck behind it reached only `z −10..10`, so a five-block notch
opened either side of the landing: an inlet that was not a design decision but a leftover of two
rectangles disagreeing. It is invisible in a top-down of the built world, where both are terrain, and
obvious in `tools/board.py`'s cell grid, where the quay's row reads `CEEEEc` against the neck's
`BBBBBBB`. The neck now carries the crossing's own frontage inland: the width stays and it continues
into the map.

## What the board is made of

`moor` is grass over a stone-and-andesite body and is the map default. `worn` is coarse dirt over the
same body and is **one lane**, drawn as a path rather than as polygons: it leaves the spawn terrace,
falls south down the moor, passes the goal, crosses the throat where the moor arm meets the neck, and
runs the length of the neck onto the bridge. That is the route, end to end, and the only route there
is. It was three detached patches before — one down to the goal, one at the throat, one at the landing
— with untrodden grass between them, which reads as dirt spilled on the map rather than as a way
across it. **A lane that stops at the objective says the objective is where people stop going.**

Two things were breaking it and neither is visible from above. The **goal-pad** — a shape carrying a
`height_mode`, drawn to flatten the ground under the monument — wins the theme over a plain patch, so
it painted moor back over the lane for the whole stretch past the goal; measured, that pad is no longer
needed at all, because the `brow-north` push behind the original `WX11` is gone. And **two trees stood
in the lane itself**, their canopies covering the very ground they were meant to stand beside.

`holm` is podzol over mossy stone and is the tarn's shore. The tarn's bed is gravel shot through with
coarse dirt — it is stated on the water prop's own `bank` rather than as a theme, because the bed is
the water's business and not the ground's — and it is not grass, because water over a lawn is water
nobody dug for. Everything built — revetment, spawn terrace, bridge — is one `masonry`, and that is now
the whole built palette: `pale` was the obelisk's shaft and went with it.

The rim is off on every theme. A rim caps every fall with a band and turns a relief's rolling ground
into contour lines; it belongs on an edge that was made rather than solved, and nothing here has one.

**One croft, not two.** Both stood on the neck, and two houses within thirty blocks of the only
crossing is a village at a chokepoint. The one nearer the bridge went. **Three erratics, not five**: the
moor arm is 40 × 50 and already carries a spawn terrace and its door's approach, a goal's clearance, a
tarn and its channel's claim, and every third and fourth site tried fell inside one of them. A rock
placed where it fits rather than where it belongs is the scatter the brief rules out.

## What is still wrong

**Nothing the studio names.** The final drive answers no refusal, no decline and no complaint —
`RL2` went with `brow-north`, which was the push doing most of the damage: two pushes are enough for a
headland 40 by 50, and the third was standing on the water.

**Coverage 6.4% dead**, in small patches at the headlands' outer lips and the far corners of the
terraces.

**The board has one croft**, in the neck's south-west corner, and getting it to stand there cleanly
took four attempts that each failed differently:

1. **At the lip.** A house's stamped footprint runs a block proud of the corners it is given, so
   corners at `x −49, z −14` reach the neck's own edge and the foundation fills that face in bedrock —
   29 courses, 22 of them over the void.
2. **On a padded lip.** The pad drawn a block past the edge built *its own ground* over the void: a
   one-block grass ledge at **y9** hanging off the headland, which is what `WX11` then measured
   against rather than the house.
3. **On a skirted pad.** A `skirt` eases the pad back into the ground over its outer blocks, so with
   the house one block inside the pad its walls stood on that slope and `DR-SLOPE` read ten blocks of
   rise across the footprint. One course of lift wants a kerb, not a ramp: `skirt: 0`.
4. **Inset, on a pad that runs past it.** The house sits at `x −47..−39, z −12..−4` on a pad reaching
   out to the neck's edge. Every side of the building stands on level pad, the two-course kerb belongs
   to the pad rather than to a foundation, and nothing is reported.

The style drops its **cobble footing**. `Foundation.footing` is "the course ringing the plate one block
proud, or null — the default — for a building that meets the ground without one", and a ring of cobble
at the sill is the one part of this style that reads as a plinth rather than as a house.

**The observers were watching from inside the bridge.** `PlanGlobals.observerY` is "where the observers
watch from, or absent for the derived height (surface + 15)" — and derived, on this board, is y24,
which is the middle of the arch's own masonry. It is stated at **y44** now, twenty over the deck.

The **obelisk moved off the lane, and then went entirely.** At `(−19, −5)` it stood inside
`worn-landing`, the approach to the only crossing on the board — a monument in the middle of the one
route across it — so it moved into the grass of the neck's south strip. That fixed where it stood and
not what it was. A dressed pale-stone pillar is a monument, and **this board has nothing that would
have raised one**: no settlement, no order, no war it commemorates, one croft and a bridge. It read as
an ornament set down on the moor rather than as something the place contains.

Its job — a landmark on the neck, where the two routes meet — is done by a **standing rock**. `cairn` is
the only `BoulderForm` that tapers: three shrinking lobes stacked, against a rounded mass (`round`),
that mass broken up (`angular`), and a low spread (`outcrop`). A boulder takes no aspect, only `size`,
and the proportions arrive with the form — at 6 it stands about twelve courses on a base five across,
and at 8 the base overruns the neck's own lip. It is cut from the same mossy gneiss as the other two
erratics, so it reads as the third of a set the ice left rather than as a fourth idea.

Cutting the obelisk also took the last `kind: "made"` layer off the board. The bridge is the only thing
built over the compiled ground now, and it is a plain layer rather than a made one.

One house, three erratics and the copses are still a thin set of placement ideas for a board this size,
and the moor arm has room for another once something is found that has a reason to stand there.

## Coordinates

| Thing | Red | Blue (rot_180 image) |
|---|---|---|
| Spawn point | (−55, 29, 55) | (55, 29, −55) |
| Monument (`cube-3`, ender stone) | (−40, 29, 20), blocks y35..37 | (39, 29, −21) |
| Spawn terrace, top | y 31, x −62..−49, z 47..60 — one course over the moor, no flight | — |
| Bridge deck | y 27, level with the quay, x −10..0 fanned to 0..10, z −4..4 | — |
| Tarn: bank / water / bed | (−34, 38) — bank y 30, water y 27, bed y 23 | (34, −38) |
| Standing rock (`err-stone`, cairn, size 6) | (−26, −8) | (26, 8) |
| Croft pad | y 27, x −49..−37, z −15..−2, skirt 0 | — |
| Observer | (0, 44, 0) — stated, not derived | — |
| Croft (no cobble footing) | x −47..−39, z −12..−4 | (47..39, 12..4) |
| Lane (`worn`) | path, radius 3, (−55, 46) → (−10, 0) | mirrored |
| Cut (void) | x −10..10, the board's full length | — |
| Build zone | x −10..10, z −15..15 | — |

Gates: plan valid, score 0, **no violations, no lint, no declines and no complaints**; export gate
OPEN; 4 region files; two monuments, one a team; traversability connected across the build geometry.
