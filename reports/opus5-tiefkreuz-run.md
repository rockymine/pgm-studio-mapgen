# Opus 5 — Tiefkreuz: a destroy board on four storeys, and what a rework of it measured

Two runs on one board. The first built it; the second reworked its geometry and its concept against a
list of measured faults from the author. Both accounts are here, because the second one only makes sense
beside what it changed, and several of the first one's capability findings are still the evidence for
what the surface does.

---

# Pass two — the rework

## What I set out to change

The board the first pass shipped read as a terminus station with a viaduct over it and four sheds on a
stone floor behind. The author's faults were geometric and every one carried a coordinate. Written down
before anything was authored:

> Make the deep line a **through** station whose rails run on into a tunnel at the back of the map. Put
> both monuments **on the line**, in the four-foot between the rails. Make every stair **45°** with a
> rail beside it, so no flight is a 1:2 ramp and no flight has a cliff for a side. Kerb every edge that
> is a drop. Make the rails sit **on** the ballast. Say what everything is **made of** rather than
> theming it. Turn the back of the map into a quarter that has a plan: an arterial road beside the
> elevated station, an avenue with planted verges, and a grid of tall flat-roofed blocks of which the
> spawn is one.

That is what was built. `maps/opus5-tiefkreuz` · `specs/opus5-tiefkreuz` · `review/opus5-tiefkreuz.md`.

## The three numbers, before and after

```
                        first pass                     rework
03-slopes.txt   11994 walked, 300 scrambled     11672 walked, 648 scrambled, 1632 barrier
                 1658 barrier
06-claims.txt   placed 28, declined 0           placed 26, declined 0
coverage        reached 11521, dead 1495        reached 12006, dead 1155
                = 10.7% dead                     = 8.3% dead
findings        HS7 x3, SK23 x4, WX11 x6        SK11 x3, SK18 x1, WX11 x2
```

The scrambled count went **up** on purpose. The first board's 300 were the trackway — a two-block climb
out of a track, which is what stopped a goal ever standing on one. Those are gone; the 648 are parapets,
which are two courses proud so that a player cannot step over them, and every one of them is drawn.

`POST /plan/evaluate`: **score 0, valid, no violations, no lint**. `POST /plan/inspect`: `GO1` 3.15 and
3.31, `GO4` 53 and 54, `GO2` 37, `GO3` 124 / 131 / 145, `CT12` 32. `GET …/preflight`: **export gate
OPEN**.

## What the new `material` word is for, measured

A shape may now state one `TerrainMaterial` in place of a theme, and the whole point of it is stated by
`SK23`: a theme is a recipe for ground, which of its five buckets a block takes is decided per column by
whether that column is an edge, and a shape with no interior column is all edge. The first pass raised
four `SK23` groups — 18 canopy stilts and 3 street kerbs themed `bahn`, 3 viaduct parapets themed
`ziegel`, and one concourse threshold — and every one of them built as one course of rim over wall with
the theme's own surface nowhere on it. This pass raises **none**: 38 shapes carry a theme and 367 state
a material.

Two things a material does that a theme cannot, both measured:

**A height band stack settles a rail.** `{"kind": "layered", "axis": "height", "from": 0, "stack":
{"bands": [gravel ×6, iron ×1], "ending": "repeat"}}` on one shape spanning `[0, 7)` reads back at
`(−13, 30)` as `y1–5 Gravel · y6 Iron Block` — the rail on the bed instead of the six-course iron pillar
the first board had. The same device gives a pier a plinth and an impost: `(−34, 62)` reads
`y3–32 Bricks · y33–38 Stone Bricks`, against `y1–38 brick` before.

**A road is a shape, not a stroke.** A `stroke` seats on whatever surface a column carries, so the first
board's avenue had to be drawn in two runs to avoid paving the viaduct. Drawn as an override add at the
street's own height with `material` and `keepClear`, it lands where it is drawn — `(0, 64)` reads
`y29 Black Stained Clay` under a viaduct whose soffit is at `y38` — and it keeps buildings off itself
with no margin.

**And one thing a material must not touch.** A verge is planted, and `keepClear` on it declined all six
avenue trees by name (`DR-KEEP … which is kept clear for a stated structure`). A road holds ground; a
verge is ground.

## What I got wrong

**I drew both trains with their axes swapped and neither was built.** A helper turned a *(along, across)*
pair into a rect and returned the two intervals the wrong way round, so the deep train was drawn at
`x 29..31, z 9..13` — over the chasm — and the elevated one at `x 62..66`, off the board. Nothing
refuses a shape drawn over void, and both `transect-Triebzug.txt` and `transect-Hochbahnzug.txt` read
`rises 0, falls 0, worst step 0 | walked end to end`, which is exactly what a thing that is not there
reads as. What found it was a `column` at a coordinate I expected a carriage side at: `(10, 30)` came
back six blocks of ballast. **A transect of nothing is indistinguishable from a transect of flat
ground; a column is not.**

**I ran an override add over a tunnel bore and filled it in.** The avenue's planted verges were drawn at
`x ±7..±11`, which is four columns of the two track strips, and an override add at `[0, 30)` beats the
ballast's `[0, 6)`: `(−11, 62)` read solid dirt from `y10` to the grass at `y29`, where the bore should
have been. `SK10` said so — *layers 'ground' and 'tunnel' are driven 19 block(s) into each other over
216 column(s)* — and 216 is exactly the two bores. The whole avenue is now sixteen blocks wide and sits
over the island platform's own footprint, so nothing it carries crosses a bore.

**A one-course balustrade is a step.** The rails beside each flight were drawn one course over their
tread, and `…/walk?aim=reach` from the platform to the spawn ran **up the balustrade** rather than up
the stair — a one-block rise is a walk. At two courses it is a wall, and the fall off the side of a
flight is fenced: `(3, 36)` is a balustrade topping at `y14` and `(4, 36)` is the platform at `y8`.

**A slab's hole and the flight in it are two different lengths.** The street stair's well was cut one
column longer than the flight that climbs it, so the top tread stood beside an eleven-block drop back to
the concourse and the kerb round the well closed the way out: the transect read `+1 … +1 · DROP −11 ·
BARRIER +13`. The kerb round a stairwell is a **U** — its fourth side is where the top tread meets the
pavement — and the hole ends where the flight does.

**`base_height` is a thickness measured from `floor`, and I used it as a top.** A soffit stated
`floor 1, base_height 2` on a layer at `base_y 37` builds `y38` *and* `y39`, which is the deck's own
floor: `SK10`, *'traeger' and 'viadukt' driven 2 blocks into each other over 768 columns*. One course is
`floor 1, base_height 1`.

## Three complaints I could not clear, with the reads that bound them

**`SK11` — 9 209 places of standable ground around `(−14, −76)` @7 unreached.** The board is connected
and every leg of the chain measures 0 placed in both directions: island platform → concourse 22 blocks,
concourse → street 36, tunnel bore → island platform 48, deep track → own spawn 111 blocks with no drop
at all. Pre-flight answers *traversability: spawn ↔ objective chain connected across the build
geometry*, and the export gate is OPEN. The two 72-place complaints beside it are the two viaduct
parapets, whose tops stand two courses over the platform on purpose. **Verdict: not settled.** I could
not find the disconnection the rule names and did not want to reshape a board around a number I could
not reproduce with a walk.

**`SK18` — the elevated canopy and the deep monument in ten shared columns.** The test is
two-dimensional and the two things are forty blocks apart in Y. Read at `(−14, 58)`, the first column it
names: `y48` canopy · `y39–42` deck · `y37–38` girder · `y12–29` tunnel vault · `y4–5` ballast — and no
obsidian anywhere in it, because the monument is at `(−12, 56)` standing at `y8–y9`. **Verdict:
mistaken, in the rule's favour** — the geometry it warns about is real on a board where a made thing and
a goal share a storey, and this is not one.

**`WX11` — the deep monument thirty-nine blocks above the cell beside it.** `?at=-12,56` reads obsidian
`y8–y9` over ballast topping at `y5`; `?at=-12,53`, the cell it names, reads `y5`. Three, not
thirty-nine. Thirty-nine is the distance to the viaduct's parapet, which crosses fifteen blocks north of
the goal and thirty-six above it, and the fix the finding offers is an `area` relief mark held at 45 —
the viaduct's height. The first pass reported the same complaint as twenty-one against a measured three.
**Verdict: the number is wrong on a stacked board**, and it was wrong on this board before the rework
too.

## What worked first time

- **`material` on every made shape.** No `SK23`, no `SK24`, and the four theme registry entries left are
  four places rather than nine materials wearing a theme each.
- **The cess.** One column of concrete a course over each rail head turns a track into `y8 → y7 → y6 →
  y5` and back, four one-block steps, and `03-slopes.txt` row 30 reads `.` from `x −20` to `x 20` where
  the first board read `##` at four places. It is what makes a monument on the track reachable on foot.
- **`carve` for the carriages.** The same rectangle-minus-holes routine that cuts a stairwell out of a
  lid cuts doors and a cab out of a carriage side: `(10, 30)` reads black underframe, red body, grey
  roof; `(10, 32)` is a door in light grey; `(10, 37)` has the window band in light-blue glass; `(10,
  40)` is the gap between the cars.
- **The goals' own storey and the bedrock plate.** `{"layer": "ground"}` at `(−12, 56)` and `{"layer":
  "viadukt"}` at `(24, 63)` both landed on the surface they named, and the plate is under the ground the
  goal resolved on — `y2` beneath a track topping at `y5`, and `y38` beneath a deck at `y39`. The
  unbreakable sheet the first board put at `y26` over a monument at `y11` is gone.
- **Reading the claims raster before placing anything.** `06-claims.txt` is the whole board as one
  raster of what claims each cell, and the door approach in front of a spawn is wide enough that three
  buildings and three trees were declined for standing in it. Reading it, moving them and re-driving got
  to **placed 26, declined 0**.

## What the author corrected mid-run

**A noise scale is not a texture knob on a board this size.** `stadt` was a two-block `noise` at scale
18 and `schotter` one at scale 9, and the author's ruling was that a scale that large *"will look worse
than a single material"*. Measured rather than argued: `POST /terrain/material-preview` at scale 18 draws
amorphous twenty-block blobs, and even brought down to 4 the built world reads eight adjacent columns of
one block — `(8, 105)` to `(15, 105)` all Stone Bricks, `(20, 101)` to `(20, 107)` all Andesite. Two
blocks of nearly one shade sampled at any scale a fractal field will give you are blotches of two
pavements, not grain in one. **The city is one block now, and every variation on it is drawn**: black
carriageways with yellow dashes, smooth-stone pavements, two planted verges, the station's one-block
checker, brick buildings and banded piers. The general form of the correction: on a board of a hundred
blocks or less, *reach for a second shape before reaching for a second stop.*

## Open gameplay questions

Four, decided without an oracle, built, and recorded here rather than filed as facts.

**Is a goal on the track the right place for it?** The author suggested seating the goals on the rails
and it reads well — the monument stands between the rails with the train behind it. But it puts the
objective in the narrowest part of the station, four blocks wide between two rails, reached along a
trough, which is a place two defenders hold. The alternative was the open terminus deck the through
station removed.

**Is a one-way drop a route?** The shaft over the deep monument falls twenty-four blocks straight onto
the track. `aim=reach` takes it, because the walk prices a fall at nothing; in game it is most of a
player's health and the only way back is the stairs. Kept, and kerbed on both storeys so it reads as an
edge.

**Is a seventeen-block pillar a route?** The free way onto the viaduct is a stair tower, 94 blocks; the
fast one is straight up off the street, 53 blocks and seventeen placed.

**Is the inside of a station a corridor the brief rules out?** The board joins the two teams only by a
build zone over void, at every height. But each half's station is an enclosed hall an attacker walks end
to end, and the tunnel behind it is a dead-end bore eighteen blocks long that exists to say the line
continues. A match decides whether the shaft, the open bay and two stairs are enough ways in.

---

# Pass one — the board as it was first built

## What I set out to build

> A lane 80 × 224 blocks, `rot_180`, cut across its middle by a 32-block chasm. In each half, a terminus
> station buried under the street: two running tracks and three platforms at y8 in cut-and-cover, a
> concourse mezzanine at y18 over them, the street at y29 over that, and a brick viaduct at y41 over the
> street. Two destroyables a team — one on the deepest floor and one on the highest, 34 blocks apart in
> the vertical.

## What the surface let me say, and what it did not

### 1. A goal's storey — shipped

`DestroyablePlacement` carries `layer` — *"Which layer's surface this stands on, or null for the top
one"* — and it is carried through the compile onto every orbit image. Two fields in the plan, and both
monuments landed on the surface they were stated for on the first build. `opus5-interchange` reported
this as missing and worked round it with a `goalLayers` key in `tools/drive.py`; that key was not needed.

### 2. The walk's storey — mistaken, and it cost every route number in the sweep

`GET …/walk` takes `from` and `to` as *"`x,z`, or `x,z,y` to pick which storey of a stacked column is
meant"*, and the sweep does not pass a `y` — `tools/render/textreads.py` derives its endpoints from the
spawn point and the goal anchor as `x,z`. So on any stacked board `04-routes.txt` measures the walk to a
*column* and calls it the walk to the goal, and `spawn-red -> hoch-0: 53 blocks, 0 placed, walked end to
end` described a route that never leaves y30 under a monument at y45. **Verdict: mistaken** — it exists,
it is documented, and the read that writes the file does not use it. Take the walks by hand, naming the
storey.

### 3. A stroke has no storey — missing, for one prop kind

`PlacedProp.layer` is on the abstract prop and `DR-LAYER` refuses a prop naming a layer the board has no
ground on; both apply to `stroke` in the schema and neither reaches the seating, so a stroke drawn under
the viaduct paves the viaduct's deck. `opus5-interchange` measured the same thing on lane markings.
**Verdict: missing** for `stroke`, and the rework's answer is not to use one: a road that must land on a
stated storey is an `addShapes` rectangle with a `material`.

### 4. A layer's paint runs from the bedrock course up — unreachable, and it cost a build

`TerrainPainter` walks the layers in order and each pass paints its column from the bedrock course to
its own top; the only thing that stops a pass treading on the one below is the **stone-only invariant**.
With ground themes filling in `1:0`, the viaduct's pass repainted twenty-six courses of city as iron and
nothing said so — the store answered 200, the export gate answered OPEN, `themes/census` counted the
surface and was right. **The fix is one field on a different theme**: no ground theme may fill in plain
stone. Every theme on this board still obeys that.

### 5. `rimEdges: "drop"` on a two-course slab caps the whole slab — the rule, working

*Drop* caps *"wherever the ground falls away, tread edges included"*, and a concourse slab two courses
thick has a drop on every side of every column. The rim took the top course everywhere and the surface
pattern never ran. `bahn` keeps `"void"`; `stadt` keeps `"drop"`, where it kerbs the street at the chasm
and round the trainshed's open bay.

### 6. A light — missing as a fixture, reachable as a block

`glowstone` — 0 hits in `GET /api/openapi/v1.json`. `torch` — 3, none of them a placement. There is no
lamp prop and no lit-block bucket. **But a material is any `(id, data)` pair**, so a lit floor is an
ordinary shape carrying glowstone, and the board is lit by one-column pavers down the platforms and
two-by-two panels cut out of the concourse slab and put back at the same span, so their light reaches
both the floor they are in and the platform beneath. **Verdict: missing** as a *fixture*, **not
missing** as a *material*.

### 7. The observer platform is the only ground in the strait

`GET …/column?at=0,0` reads one block of bedrock at the observer's own Y, which on a board whose middle
is void is the only ground in the strait; the walk stands on any ground and `aim=travel` does not price
a climb, so every cross-team route in `04-routes.txt` goes over it. `globals.observerY` is the plan's
only control and moving it does not change the read, because the walk does not respect the build ceiling
either. **Verdict: in the design.** The honest crossing number is `aim=reach`'s.

### 8. The layout has a fine-grained edit surface, and a generated board does not want it

`PATCH …/sketch/shapes/{shapeId}`, `POST …/sketch/layers/{layerId}/shapes`, `PUT
…/sketch/themes/{themeId}` and the rest are all there and documented. What a spec-driven board does
instead is edit a constant and re-derive every document from it, because on a stacked board one number
is load-bearing in four documents at once: moving the street flight off the centre line moved eleven
treads, re-cut the hole it makes in the concourse slab, re-cut the hole it makes in the street lid and
moved the lid's kerb round it — 34 rectangles across three layers, all derived by `carve`. The per-shape
routes are the right surface for a canvas and the wrong grain for a board whose geometry is a function.

## Rebuilding it

```bash
python3 specs/opus5-tiefkreuz/build-spec.py
python3 tools/drive.py specs/opus5-tiefkreuz "Tiefkreuz" \
        --out maps/opus5-tiefkreuz --renders specs/opus5-tiefkreuz/renders
```

The one ordering that is not obvious: the box is cut into the **compiled ground layer** as override
adds, and the tunnel vault, the concourse, the street lid, the girders and the viaduct are **layers over
it**, ordered ascending by `base_y`. Swap either — make the box a layer, or the lid an override add —
and the station is solid rock.
