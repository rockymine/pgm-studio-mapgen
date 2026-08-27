# Liminal DTM II — one run, three storeys, and what the system could not say

## What I set out to build

A board to a brief from outside this repository: **Liminal DTM II**, a destroy map for 24 v 24 on a
point-symmetric desert. A walled village on a plateau is the battlefield; an oval river rings it; a
Desert Pyramid spawn and a Snowy Taiga sit on each long edge; a Liminal Poolroom and a Backroom maze
run under all of it; a Stronghold sits under the village; and eight floating islands hang over the
water. Three monuments a team, one on each of three storeys.

The instruction beside the brief was **begin very simple**, so the run is staged: the footprint
first, then the vertical stack, then the village. Each stage was rendered in the Sketch tool's own
3-D preview and looked at before the next was authored.

## What I could not say

### A stairwell cannot be a hole with a stair climbing through it (`SK13`)

**What I wanted:** a well cut through the desert with a flight rising out of the undercroft into it —
`opus5-interchange`'s own technique, and the obvious way to state a stairwell.

**What I tried, in order:**

1. A `subtract` on the compiled ground layer over the stair's footprint, with the treads on the
   `under` layer. Refused, 24 findings: *"'st1' fills 6 column(s) that 'sh1' takes away … 'st1' is on
   layer 'under' and the subtract on 'ground', and a subtract reaches only the layer it is on."*
2. No subtract at all — the four plan pieces redrawn to leave the well as a gap no piece covers,
   which `docs` calls the right way to make a hole ("*A plan carries holes by arrangement, not by
   subtraction*"). `tools/board.py` drew the gap and named it correctly: *"o = enclosed void — 16
   cells the board rings and nothing covers."* Refused identically, because **`PlanVoids.Declare`
   compiles an enclosed gap into a subtract** — so arrangement and subtraction reach the same place.

**Is it missing from the system, or was it out of reach from where I was standing?** Out of reach.
The instrument is the **override add**, which `docs/tools/capabilities.md` states plainly — *"an
override-add is how ground is put back inside a hole"* — and which no refusal message points at.
Twenty-four one-block treads at `floor 6` with `override: true` replace the desert's `floor 18`
column outright, and the shaft is the air left over them. It built first time.

**What is worth recording is that `SK13` is newer than the board that taught me the technique.**
`opus5-interchange` carries `cut1` (a `subtract` on `ground`) with `dn1` (a plain add on `under`)
passing straight through it — the exact pair `SK13` refuses. I could not confirm it would be refused
today, because its spec no longer reaches that gate: see below.

### `opus5-interchange`'s committed spec no longer re-drives

Driving `specs/opus5-interchange` unchanged against this build stops at `POST /map/from-documents`
with **400 `HS3`** — *"roofSlab is stone and the roof it steps in halves is quartz"* — once for
`roomStyles.spawn.roofSlab` and once for each of five `dressing.props[*].style.roofSlab`. The board
in `maps/opus5-interchange` therefore cannot be rebuilt from the documents beside it. Nothing in the
repository says so, and nothing would have found it: no gate re-drives a committed spec.

### A water channel cuts anything above its water line, on every layer

`WaterProp` carves a bed and then *"cuts any bank above the line back to air"*. That read is over
`SurfaceTops`, which is the **maximum** per column across every layer, so a slab on a higher layer
inside the channel's band is not a bank — it is simply removed. Measured: skyblocks drawn at
`floor 50` over the river came back with **no ground at all** from `x 74` outward (the channel's
edge is at 73), and the ones just outside it had the channel's **bank material laid on their grass**
— sand on top of a skyblock 26 blocks above the water.

**Out of reach rather than missing:** `PlacedProp.Layer` is on the base record, so `"layer":
"ground"` on the water prop confines the carve to the storey it was drawn for. With it the eight
islands come back whole and grass-topped. Nothing said so — `GENERATION-NOTES.md` records that a
**stroke** ignores `layer`, which reads as a warning about strokes and left me assuming water was
fine.

### A spawn marker's protection is the whole piece it stands on, and that can disconnect a board

`PlanCompiler` comments it exactly — *"Protect the whole spawn piece the marker sits on, not just the
stamped spawn cube"* — and it is easy to author a piece that is a sixth of the map. Mine was
36 × 80. The consequence is not a big region: it is **`EX1` at the export with every objective
isolated for every team**, whose message points at protection regions but not at which one or why.
Every direct read disagreed with it while it was wrong: `POST …/walk?team=red` answered
`reachable: true, blocks: 0` from the spawn to each goal, and the whole-map traversability put all
eight gating points in component 1. Splitting a 20 × 20 `role: "spawn"` piece out of the region
cleared it with no other change.

**Not a gap in the system** — the piece is the documented unit — but the refusal cannot be acted on
from what it says.

### The 3-D preview lists no storeys on a stacked board

`POST …/sketch/columns` answers `layers: ["under","lid","ground","bridge","sky"]`, the client posts
all five and meshes all five, and `sketch-bridge.js` fires `OnIsoLayers` with those names. **No
`LayerChip` appears**, so a storey cannot be taken off in the editor. `fireTo` swallows a failed
invoke by design, so nothing is logged. I have not proven the cause; `SketchTool.OnIsoLayers`
deserializes the camelCase message with default `JsonSerializer` options where the rest of the
client uses web options, which would explain it.

The per-storey read that does work is the server's: `GET …/render/topdown?layer=under` draws the
undercroft and nothing over it, and `render/section` is the only other read that keeps Y.

### A ring on the symmetry centre cannot have a door

The End Portal Room stands on the origin, so `rot_180` maps its wall ring onto itself — and the
image of a wall covers the gap the author left. A door authored on the east side is filled in by the
image of the west side's wall. Both doors have to be stated, and each is then the other's image.
Nothing refuses this: the room simply builds sealed, and `SK11` says so afterwards as *"standable
ground with no route onto it"*. The same rule caught the Village Monument's well rim, which read to
`SK11` as an unreachable 6 × 6 and to a player as a box.

### `WX11` names the cell, not the cause

*"house blacksmith stands 9 blocks above the cell beside it"* is a building whose footprint shares a
column with something tall — here a wall stair the **other** face's flight fans onto — and the
building seats on the highest ground it covers. The finding names the low cell rather than the high
one, so the coordinate it gives is the one place the problem is not.

### A prop's keep-out was 2-D, and a channel eleven courses down claimed the ground over it

`DR-CLAIM` declined an oak standing on a Small Hill at y36 as *"claimed by the channel
'main-pool'"* — a pool in the undercroft at y12 — and the same rule declined three of the four oaks
authored for the skyblocks, 26 courses over the river. That is not a placement to work around: props
already carry a `layer`, `DressingContext.GroundFor` already answers that layer's own surfaces, and
`GroundClaims` was the one reader in the pass still keyed on `(x, z)` alone.

Fixed upstream as `WE49`: the claim book is keyed on the layer as well as the cell and each placement
is handed one storey's view of it (`GroundClaims.On(prop.Layer)`), so two props collide only where
they share ground. The pass now declines nothing on this board.

### A storey read drew the storey over it, and the pictures were wrong for four stages

`GET …/render/topdown?layer=under` drew the desert — its houses, its trees, its river — under the
undercroft's name, and so did `?layer=lid`. `?layer=sky` and `?layer=bridge` were right, which is what
made it look like a provenance fault rather than a geometry one: a claim is recorded per column and
carries no course, so a house at y36 was being attributed to the cellar floor under it.

It was both, and the geometry half was the one that mattered. A `ColumnSegment` is half-open —
`[YFloor, YTop)` — and `WorldStorey` compared the next layer's floor against it as a **closed** range.
Rasterizing this board's own layout says why that only shows on some columns:

```
(8,-70)  under[1..18]  ground[18..28]      ← 18 > 18 is false: no layer found above, storey = the world
(0,-70)  under[1..12]  lid[16..18]  ground[18..28]   ← 16 > 12: storey ends at 15, correct
```

The mass meets the landmass at y18 with no gap, which is the whole point of stating it, and that is
exactly the case the comparison got wrong. Every storey with air over it read correctly and every
storey that abutted the one above it swallowed the rest of the world.

Fixed upstream as `WS18`: the comparison is `>=`, a layer's last drawn course is `YTop - 1`, and the
provenance record is narrowed with the world — at or below the layer's own top a block is the
rasterizer's terrain and reads `Ground`, above it the recorded claim is kept only where the storey
shows the column's own top. The picture's legend now follows what the render read rather than what it
was handed.

**What to take from it:** a picture that looks plausible is not a read. Four stages of committed
`*-under-topdown.png` renders in this map's `renders/` are that fault, and none of them looked wrong
— the undercroft's maze lattice was drawn over the surface and read as an undercroft with a lattice
in it. The brief's author caught it by knowing what could not be there: *there are no houses inside
the backrooms layer and also no trees or river.*

### A road and a river both ate the things the map was built out of

Two symptoms, one cause, both spotted by the brief's author in a render. The road inside the village
was laid straight onto the Farm's beds — cobblestone at `(48, 25)`, `(50, 25)`, `(53, 25)`, one course
down inside the plot. And the river had **hollowed the Town Wall out**: at `(71, -44)` the stone brick
stopped at y24 with sand at y25 and water at y26–27, a twenty-course hole through the wall, mirrored.

Neither is the water or the stroke misbehaving. `PlaceStroke` swaps the top block of every column it
crosses; `PlaceWater` takes the **lowest** surface its band crosses as the water line and cuts every
other column in the band down to it. Both already skip a column whose top block `IsStamp` — and
neither guard fires here, because a wall drawn as an override add on the ground layer *is terrain*:
the painter writes it with a theme like any other ground. There was no way for the tool to tell a
thing built out of ground from the ground.

Fixed upstream as `TS34`: `keepClear` on a sketch shape, which puts its own columns in the dressing
keep-out — exactly, with no margin, so a road still runs through a gate. 54 of this board's 125 ground
shapes carry it now. Read back after: the wall is 45 solid blocks to y44 and none of 47 sampled
columns of its east face is water or sand-capped; the beds are dirt and coarse dirt again.

**What to take from it:** a keep-out stops a prop, it does not route one. The road east had to be
redrawn to run south of the Farm as well, or it would simply have a plot-shaped notch in it — and
moving it put a hilltop oak inside its standoff, which is `DR-ROAD` and one more hill to move.
Circulation is authored before scenery for exactly this reason.

### A water prop makes a river, and a pool wants a shape

The brief's author saw it before I did: the Poolrooms *read organic when they are not*. Four
`WaterProp`s made two pools — a swept disc along a polyline, plus a second prop down the middle to
fill what the sweep missed — and a swept disc gives a room's pool an outline no room has: lobed where
the discs overlap, rounded at the corners, depth following the sweep.

A pool is a rectangle whose **theme** puts water in its surface bucket: same span as the deck around
it, `surface.depth: 4`, block 9 on top and prismarine under. `(59, 8)` is deck at y11 and `(60, 8)` is
water from y8 — a one-block edge, four courses everywhere, no prop involved. The Farm's furrow went
the same way.

The rule, stated once: **a channel is for water that found its shape; a themed rectangle is for water
somebody built.** Two things follow. Depth is the theme's number rather than the shape's — a shorter
shape would be a hole in the floor, not water in it. And a room nested inside a room is two spans in
the same columns unless the outer one is banded round it, which is the same care the rock already
takes with its holes.

### A relief flattened every made thing on the board, and nothing said so

Adding twenty-eight relief marks to give the village its four-block roll silently removed the Town
Wall. Read back at `(71, 8)`: stone brick to **y35** where it had stood to y44 — nine courses gone, and
the same for both flights, the six Small Hills, the Farm's rim and the Desert Well's. Nothing was
refused. `SK11` did not fire, the gate stayed open, and the only visible symptom was the spawns
leaving the objective chain for an unrelated reason.

The cause is one sentence in `docs/tools/sketch.md` that I had read as being about landforms:
`height_mode` — `level`, `raise`, `sink` — *"makes a shape stand out of the solved field rather than be
part of it"*. **An `override: true` add is not that.** Override decides who wins the column among the
shapes on a layer; it says nothing about the relief, and the solved surface then replaces the column's
top whatever the shape asked for. A made thing keeps its stated top only if it says
`"height_mode": "level"` with `"skirt": 0` — level for an absolute top, skirt zero for a sheer face,
which is right for a built thing and wrong for a landform. All 135 of this board's ground shapes carry
it now.

Two more, both about where a relief is *solved*:

**A relief is solved on the island's primary half and its surface copied through the mirror.** Marks
stated on the far half are not a second constraint — they are constraints on cells the solve never
visits, and the image of the near half overwrites them. Half my knolls and three of five house
plateaus were dead for that reason, and a house straddling the axis needs its plot pinned **twice**,
once each side, or the half the solve never visits comes back sloped.

**A mark pins its own cells; everything within `reach` of one slopes.** The river region is pinned at
y28 and the village at y36, so with nothing between them the village's edge was drawn down into the
trench: `(70, 32)` and `(68, 32)` came out at **y28**, inside the wall, and the east gate was eight
courses below the bridge landing in it. A twelve-block verge pinned at the surface is what holds the
wall's footing.

**And raising terrain under a stamped room needs the plan to say so.** The Pyramid's platform started
as an override add lifting the ground four courses; the room stamped on it correctly and the spawn
marker stayed at the height the plan still stated, four courses down inside the mass — both spawns
isolated, `EX1`, export refused. A piece states `"surface"` and the compiler seats the spawn on it.
The showcase board `20-undercroft` measures the same thing at thirteen courses.

### Two words differ between a preview and a snapshot, and the error says neither

`POST /room-styles/preview` takes the library's **save request**, where `storeys` is a count; a
serialized `HouseStyle`, where `storeys` is a list, goes to `/room-styles/preview-snapshot`. Posting
a style to the first answers **400 `RQ1`**: *"Cannot get the value of a token type 'StartArray' as a
number. Path: $.storeys"*, which is true and does not name the endpoint that would have taken it.

### A `NoiseMaterial` with no `stops` is a 500, not a refusal

Writing `palette` where `noise` wants `stops` — the word `cell` uses — answered **500 `RQ2`** out of
`TerrainThemeValidation.Blocks`, an `ArgumentNullException` on a null `SelectMany` source. `RQ3`
would have named the unread field had the request survived to answer.

### `<timelock>` is not a thing the studio writes

The brief asks for time to run rather than be held. `grep -rn "timelock" src/` over the whole studio
answers nothing: no intent field, no generator, no element. **Missing from the system**, not out of
reach — a hand edit of the exported `map.xml` is the only way to get one, and that is a second
format by another name.

### The build ceiling is an output, not an input

The brief measures `<maxbuildheight>` from the highest Skyblock Monument — y67 on this board.
`BuildIntent.MaxHeight` is a documented, settable intent field that becomes `<maxbuildheight>`, so I
added a `maxHeight` passthrough to `drive.py`, stated y67, drove it, and the map came out at **y74**.

`WorldBuilder` overwrites it, deliberately and with the reason written above the line: *"twenty
blocks over the highest ground the map actually built… written back onto the intent so the
`<max-build-height>` the XML declares and the altitude these markers are stamped at are one number
rather than two agreeing by habit."* So on any board that builds a world, `MaxHeight` is what the
export **answers**, not what an author asks for, and a driver key for it does nothing. I took the
passthrough back out rather than ship one that reads as a knob.

**Missing from the system**, then, in the sense that matters: a board cannot state its own ceiling.
On this board the derived answer is eight courses over the brief's, because the derivation measures
from the skyblocks' grass rather than from the monument standing on it.

**A standalone chest cannot be authored.** The brief's islands each want the vanilla skyblock's tree
*and chest*. The studio places a chest at exactly two places, both in `Minecraft/Stamping`:
`WoolChests` fills a wool room, and `DefenseChest.Embed` sets one into a bedrock approach wall or on
the ground beside a monument (`StructureStamper.StampPlatform`). So the island carrying the Skyblock
Monument has a chest already — read back at `(74, 22)`: obsidian y56–57, **chest y54**, grass y53 —
and the other seven cannot have one. There is no prop kind, no document field and no endpoint for a
chest that is not a wool room's or a goal's.

**A goal's prop standoff is wider than a skyblock.** `DressingScope.GoalStandoff` is 10, so a goal
holds a 21-block square against every placed prop and `OB19` declines anything inside it. The widest
island on this board is eight blocks across, so the brief's "monument beside the oak" cannot be
stated: six of the eight islands carry an oak and the two with monuments are bare. Widening the
island past 21 blocks makes it a platform rather than a skyblock, so this is the author's call.

## What I got wrong

**I read a stale `intent.json` and spent a diagnosis on it.** `drive.py` writes `<slug>.layout.json`
and `<slug>.intent.json` beside the spec, but a run that stops at a refusal leaves the previous run's
files there. I read a spawn at `(100, 36, 56)` off one, reasoned carefully about why the compiler had
moved my marker twelve blocks, and was reasoning about the *first* stage's plan. `GET
/map/{slug}/intent` answers the stored document and is the read to trust.

**I assumed the river's 8-block drop was the same on both banks.** It is not: the village's bank is
where the Town Wall stands, so a flight cut into it is a pit against a wall rather than a way out of
the water. The ways out are on the outer banks only.

**I read `maxPlayers` as the board's cap and shipped a 48 v 48 map.** `PlanGlobals.MaxPlayers` says
"shared player cap for every generated team", which is per team, and `48` came out as
`<team max="48">` twice. The brief's 24 v 24 is `maxPlayers: 24`. Nothing checks it, because nothing
can: both readings are legal boards.

**I drew the undercroft as rooms and left the rest of it as vacuum.** A sketch layer carries one span
a column, so stating the Poolroom's floor and its walls and nothing else leaves every other column of
the lower half with no span at all — the landmass stands on nothing and the sandy places read as
slabs hanging over a hole. The brief's author saw it in the first 3-D render and named it before I
did. The fix is not more rooms: it is to state the **rock** over the whole board and cut the rooms
out of it, which is 355 rectangles of mass against 18 of room. Two rules bite the moment it is one
mass rather than many rooms — a board-wide shape has its own `rot_180` image lying over it (`SK9`),
so the rock goes in an island stated `mirrors: false` with its holes named for both teams; and a
tiling that misses a column is invisible in every render, so it is checked in the generator (bare 0,
doubly covered 0) rather than looked at.

**Filling the rock sealed the stairwell, and I nearly diagnosed it from the wrong read.** The shaft
down from the Pyramid was a hole in the *ground* layer that had never needed to be a hole in anything
else, because there had been nothing else. With the mass stated it filled to y17 and the flight
descended twenty-three courses onto solid stone six blocks over the corridor it was for; both spawns
left the objective chain and `EX1` refused the export. What nearly cost the diagnosis was
`GET …/walk`: `aim=travel` returns the **shortest** route and prices the blocks it places along it,
so a spawn walking out of its own open door read as "6 placed blocks" because a diagonal through the
wall was two blocks shorter. `aim=reach` is the one that answers *can this be walked*, and the
component the traversability verdict floods over is the zero-block, two-way one.

**I put three Small Hills on top of the roads.** Circulation is authored before scenery for exactly
this reason, and I drew both in one pass; `DR-ROAD` and `DR-CLAIM` declined three oaks and named the
cells. Moving the hills off the four diagonals cleared it.

## What worked first time

- **The layer stack.** Five layers written bottom-up — `under`, `lid`, `ground`, `bridge`, `sky` —
  built with no finding beyond the eight `SK11`s the floating islands are supposed to raise. One
  column reads *oak deck y34–35 · water y24–27 · sand y23 · sandstone y18–22 · poolroom y6–11*.
- **`goalLayers`.** Three monuments, three storeys, no argument: The Deep End resolved into the
  Poolroom at y15, The Floating Garden onto its island at y56.
- **One-block treads.** Every flight on this board is stated as one rectangle per course rather than
  as a ramp, so nothing rasterized into treads of two and every climb walks both ways for nothing.
- **The water ring.** One `WaterProp` polyline, the east half of an oval, fanned by `rot_180` into a
  closed moat.
- **A maze that is its own mirror.** Thirteen runs on a 20-block pitch, links dropped by
  `(2k + 1 + 2m) % 3 == 0`. The naive `(k + m) % 3` is *not* symmetric: a link is indexed by the run
  on its low side, so negating both indices shifts it by one and the two teams get different mazes.
  Doubling the indices and centring the link's own coordinate makes the test even under negation.
- **The 3-D preview through Playwright.** Chromium's software WebGL draws it; the toggle is
  `button.canvas-mode-toggle`, the wait is `.canvas-iso-busy` going to `display: none`, and the
  rotate is `button[title="Rotate the preview 90°"]`.

## Open gameplay questions

Five were put to the brief's author during the run and answered. The first three settled the board:

| Question | Answer |
|---|---|
| The brief's 220 × 145 leaves the Pyramid Spawn 24 blocks of depth, and a vanilla desert pyramid is 21 × 21. Grow the map, keep the numbers, or shrink the village? | **Grow the map to 248 × 160.** |
| The Poolroom and Skyblock monuments sit near their own spawn by the brief's design, which puts `GO1` at 6.4 and 4.5. Keep them deep, or pull them in? | **Pull them toward the middle.** They now measure 3.03 / 3.14 / 3.53. |
| The river is 8 blocks below everything around it and cannot be climbed out of. Hazard, or a lane you can leave? | **A few ways out** — stepped slipways cut into the outer banks beside each crossing. |

Two more were put to the author and answered:

**Nothing walks up to an island.** `…/walk?aim=reach` prices the nearest one at **11 placed blocks**
from a Pyramid's floor and the next at **25**. **Answered: an island does not need to be connected —
players build up to it.**

**The Skyblock Monument cannot stand beside an oak.** A goal holds a 21-block square against every
placed prop and the widest island is eight blocks across, so the two islands carrying a monument are
bare and the other six have their oak. **Answered: the monument keeps its bare island.**

Two are decided and unasked, and stated so they can be overruled: **the Backrooms are unlit**
(nothing in the studio places a light source), and **seven of the eight islands have no chest**
(the studio places a chest only in a wool room or beside a monument, so the monument's island has
one and no other island can).
