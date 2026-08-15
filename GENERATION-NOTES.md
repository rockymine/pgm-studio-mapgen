# Generation notes — what an agent has to know before it can draw ground

Everything here was learned by driving the live API and reading a column back, not by reading a document.
Each entry is something that either is not written down, or is written down somewhere a person authoring a
map would not think to look. The tool documents in `pgm-studio/docs/tools/` remain the reference; this is
the errata an author needs beside them.

Measured against `pgm-studio` at `claude/pgm-studio-mapgen-tasks-5kj6sm` (14 Aug 2026), building
`maps/marlstone-steps` (a CTW board made of tiers) and `maps/basalt-reach` (a destroy board made of one
relief and a subtract). The two were authored the opposite way round on purpose, so several entries below
have a measurement from each.

---

## 1. A hand-authored shape needs three fields nobody mentions

This is the one that costs a whole cycle, because **nothing fails**.

A shape in a `SketchLayout` must carry `type`, `operation` and `floor`:

```json
{ "id": "strand", "type": "polygon", "operation": "add", "floor": 0,
  "base_height": 10, "theme": "marl-strand", "vertices": [[-58,-6], ...] }
```

`SketchShape.Type` defaults to `""`, and `RingOf` switches on it — `"polygon"`, `"rectangle"`, `"circle"`,
`"lasso"`, `"path"`, and `_ => []` for everything else. A shape with no `type` therefore rasterizes to **no
cells at all**.

What makes it expensive is how quietly it fails:

| Stage | What it did with 16 type-less shapes |
|---|---|
| `PUT /map/{slug}/sketch` | `{"ok": true}` |
| `GET /map/{slug}/sketch` | returned all 16 shapes, the island, and the relief, intact |
| `POST .../sketch/relief/read` | **HTTP 200, `{"islands": []}`** |

An empty `islands` array is the only symptom, and it looks like a relief problem rather than a geometry one.
The chain inside is `ReliefFields → SolveRelief → ground.Count == 0 → continue`: no shape rasterized, so the
island owned no cells, so it was skipped. Copy the field set off a shape that is known to build
(`specs/quillon-barrow/*.layout.json`) rather than writing one from the type definition.

**Diagnostic:** if `relief/read` answers `{"islands": []}` on a layout whose relief key matches its island
id, the shapes are not rasterizing. Post a known-good layout to the same endpoint to prove the endpoint is
fine before touching the relief block.

## 2. Height and paint resolve overlaps by *different* rules

This is the one that will visibly spoil a stepped board, and it is a direct consequence of the technique
`docs/tools/capabilities.md` recommends.

- **Height**: `RasterGroup`/`MergeCell` — *the taller add-shape wins* the column.
- **Paint**: `ShapeScopeOwners` — *the smallest-area shape wins* the cell ("the most specific scope").

The documented way to make an organic tier is to let the tier below **run under** it, so the upper one can
pull inward without opening a hole. But where the lower tier is the *smaller shape*, it keeps the paint
while the upper tier keeps the height — a band of the wrong material laid across the top of the upper
terrace.

Measured on the first Marlstone build, at `x = 0`, with `shelf` (`base_height 22`, theme `marl-shelf`,
white quartz) overlapping `terr-mid` (`base_height 18`, theme `marl-orchard`, grass over sandstone):

| column | ground top | painted | should be |
|---|---|---|---|
| `(0, 70)` | y21 | Quartz Block | Quartz — shelf alone, correct |
| `(0, 58)` | **y21** | **Grass / Dirt / Sandstone** | Quartz — shelf's height, orchard's paint |
| `(0, 50)` | y17 | Grass / Dirt / Sandstone | correct — `terr-mid` alone |

`shelf` covers ~3 300 cells and `terr-mid` ~1 500, so `terr-mid` is "more specific" and paints nine blocks
of the shelf's own surface.

**What to do about it.** The band is exactly the depth of the underlap, so author the two edges to overlap
by only two to four blocks and the seam reads as a transition rather than a stripe. Where the upper tier is
the *smaller* shape the problem does not arise at all — on the same board `crest` over `shelf`, `terr-mid`
over `low-mid` and `low-mid` over `strand` all paint correctly, because in each case the upper shape has the
smaller footprint. It is worth checking which way round each of your joins sits before building.

## 3. Bézier `controls` — the semantics, and why probing a vertex proves nothing

`controls` is a dictionary keyed by **vertex index as a string**, and the handles are **absolute board
coordinates**, not offsets:

```json
"controls": {
  "5": { "in": [77, 25], "out": [77, 35] },
  "6": { "in": [76, 37], "out": [69, 44] }
}
```

The edge from vertex *i* to vertex *j* is the cubic `p0 = verts[i]`, `c1 = controls[i].out`,
`c2 = controls[j].in`, `p3 = verts[j]` (`PolygonRing`, `SketchRasterizer.cs`). So a vertex's **`out` bends
the edge after it and its `in` bends the edge before it** — one vertex's handles belong to two different
edges. A vertex with a control but whose neighbour has none still curves: the missing handle falls back to
the endpoint itself.

**The curve's extremum sits between vertices, never at one.** Probing the vertex is the natural check and it
is worthless — the vertex is a fixed point of the curve. Work out where the bulge actually is (`t = 0.5` is
close enough) and probe there. A/B against a build of the same vertices with `controls` removed:

| column | no `controls` | with `controls` | shape |
|---|---|---|---|
| `(73, 36)` | void | **solid** | `low-east`, curve peaks x≈75.5 at z≈36 |
| `(74, 36)` | void | **solid** | " |
| `(75, 36)` | void | void | past the curve |
| `(52, 89)` | void | **solid** | `crest`, curve peaks x≈52.9 at z≈89 |
| `(52, 82)` | void | void | **the vertex itself** — the pinch between two bulges |

## 4. A ramp between two tiers is four fields and it works first time

`height_mode: "level"` plus `anchor_heights` is a tilted plane, and it is how you join two flat tiers that
would otherwise be a one-way drop. Vertices in order, one height each:

```json
{ "id": "ramp-d", "type": "polygon", "operation": "add", "floor": 0,
  "base_height": 22, "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
  "vertices": [[-46,68],[-34,68],[-34,82],[-46,82]], "anchor_heights": [22,22,26,26] }
```

Measured down `x = -40`, joining the shelf (22) to the crest (26):

| z | 66 | 70 | 74 | 80 |
|---|---|---|---|---|
| top | y20 | y22 | y23 | y25 |

A path prop laid over it paves the slope, so the ramp reads as a built stair. Four of these on one board turn
a stack of terraces from a series of one-way drops into a zigzag climb, which is the difference between a
hillside a defender can rotate on and one they cannot.

## 5. `relief_scope: exclude` takes a tier out of the elevation model entirely

Known already (`AGENT-REPORT-2.md`), confirmed again with a number worth quoting: Marlstone is a five-tier
board of roughly 19 000 ground cells, and its relief readback reports **4 294 cells** — the one tier that is
not `hold` or `exclude`. Everything above the base tier is outside the solve, so its variation has to come
from shapes: `raise` landforms, `sink` basins, `anchor_heights` tilts and ramps. Budget for that when you
design a stepped board, because "add relief" is not available as a later fix.

`hold` and `exclude` differ in how the join reads, not in whether the shape stays flat: `hold` lets the
ground ramp up to meet the shape, `exclude` meets the tier below at a face. A terrace wants `exclude`.

## 6. Read-backs: what each one will and will not tell you

- **`--column` is the only honest answer.** Every other read is a projection. Probe the coordinate you
  already expect something at.
- **A column through the middle of a house reads floor, air, roof** — the walls are at the perimeter. That
  is a correct building, not a broken one.
- **`--topdown --layer structure` is the building census, and `--buildings` is not.** Since `B133`/`B139` the
  export writes `region/provenance.json` beside the `.mca` files, recording what each pass *placed* and, now,
  **which prop placed it**. The structure layer reads that, so it draws exactly the buildings you authored.
  The owners list is a literal census — read it directly:

  ```powershell
  $j = Get-Content maps/<slug>/region/provenance.json -Raw | ConvertFrom-Json
  $j.owners | Group-Object { ($_ -split ':')[0] }
  ```

  Marlstone answers `house 24, spawn 2, redstoneline 4, roomfloor 4, wool 4, wall 2` — twelve authored houses
  in two orbit images, by id `h1`…`h12`. That is the question "did my buildings stamp" answered from the
  build itself rather than guessed from blocks.

- **`--buildings` is a forensic tool for worlds the studio did not build**, and it will mislead you about one
  it did. It finds roofs by material and then judges them, and all three of its stages are tuned to a
  timber-and-plaster convention:
  1. **the `--roof` filter is exact.** A `HouseStyle` with `roofSlab: 44` surfaces its roof in brick *slabs*
     (44:4) with a quartz-pillar verge (155:2) — solid brick (45) appears only at the ridge.
  2. **`IsTerrain` swallows whole styles.** Its list includes `1, 4, 13, 24, 98, 155, 159, 172` — stone,
     cobble, gravel, sandstone, stone brick, quartz, stained clay, hardened clay. A cottage roofed in
     `159:14` is classified as *ground*, so its clearance over terrain is nil and it is discarded by the
     `RoofHigh − GroundY < minimumHeight` gate. `--roof 159:14` on Marlstone returns **0 components**.
  3. **`CornerStems` looks for a vertical log** within two blocks of each footprint corner. Styles with
     quartz-pillar posts and quartz beams carry none, so every candidate reads `corners: 0` and is labelled
     *"hangs, unframed — not a building"*.

  On Marlstone the three compound: `--roof 45:0` reported "6 roof components", all of them the spawn hall's
  four concentric hip courses, while twenty-four houses stood in the world. Relaxing `--min-area`,
  `--min-side` and `--min-height` changed nothing. **Opus run 1's `quillon-barrow` census worked** because
  its houses used `post: 17:1` (oak log) and `roof: 5:1` (spruce planks) — a log at every corner, and a roof
  material that is not in `IsTerrain`. If your palette is stone and quartz, `--buildings` cannot see your
  town; use the structure layer.

- **A provenance sidecar written by an earlier revision crashes the renderer.** `WorldProvenanceFile.TryRead`
  handles a *missing* file and falls back, exactly as its doc comment promises, but a file it cannot
  *deserialize* throws straight out: `--topdown --layer structure` exited 255 with an unhandled
  `JsonException` on worlds built two hours earlier, because `B139` changed the sidecar from a bare array of
  runs to `{"owners": [...], "runs": [...]}`. **Rebuild a world before rendering it against a newer studio**,
  or delete `provenance.json` to get the material-estimate fallback.

## 7. A path claims ground, and a building that touches it is dropped — silently, still

Known (`AGENT-REPORT-2.md`), **still live**, and it is the single most expensive thing on this list because
the only symptom is a house that is not there. `Decorator.PlacePath` adds every band cell to the `taken` set;
`PlaceHouse` returns 0 if any footprint cell is taken, for **both** orbit images, with nothing logged, nothing
refused, and a clean `200` from export.

Four of five houses on `basalt-reach` went this way on the first dressed build:

| House | footprint | claimed by | that path's band | stamped |
|---|---|---|---|---|
| `w1` | `x −45…−37, z 64…72` | — | — | yes |
| `w2` | `x −34…−25, z 64…71` | `p-ramp-back` at `(−26, 70)` | `x −28…−24, z 68…72` | **no** |
| `w3` | `x −22…−14, z 64…73` | `p-ramp-back` at `(−22, 63)` | `x −24…−20, z 61…65` | **no** |
| `w4` | `x −11…−3, z 64…70` | `p-spawn` at `(−8, 66)` | `x −10…−6, z 64…68` | **no** |
| `w5` | `x 0…7, z 64…72` | `p-spawn` at `(0, 72)` | `x −2…2, z 70…74` | **no** |

Three commits landed during this run about what a *building* claims (its eaves, its roof ring, two buildings
that touch). None of them touch the path side, so this is unchanged.

**How to work with it.** A path's band is `radius` blocks either side of the centreline, computed along the
whole polyline — so an intermediate point you did not think about is what claims the ground. Give every
building **three or more blocks** of clear ground to the nearest band, and remember the building claims one
block past its own walls for the eaves. Then **check by probing each building's centre**: a stamped house
reads its own `floor` material there, and a beam or roof slab higher up; a dropped one reads the terrain
theme's own surface palette. That check is four seconds and it is the only one that answers.

## 8. A prop over void is skipped, and the tree count does not notice

A tree authored at a coordinate with no ground under it simply does not appear. Nothing refuses it — and
`--topdown --layer foliage --dressing <layout>` still reports it, because **that count comes from the
document, not from the world**. `s1` at `(−46, 74)` on `basalt-reach` was outside the `works` polygon at that
z, probes as 0 solid blocks, and the render said "34 tree(s)" with and without it.

Check a prop's coordinate against the polygon it is meant to stand on before building, especially near an
organic edge, where "inside the shape" is not something you can eyeball off a vertex list.

## 9. Two capabilities the plan cannot reach, that the intent can

**Standalone void enforcement (`B132`).** `BuildIntent.VoidEnforcement` fires whether or not `Areas` is
declared, which is what lets a board have a permanent void with no build zones at all. But `PlanModel` has no
field for it and `PlanCompiler` never emits one, so a compiled intent always carries
`"voidEnforcement": null`. Patch it before `PUT …/intent/from-plan`:

```json
"build": { "maxHeight": 38, "areas": [], "holes": [],
           "voidEnforcement": { "exclusions": [] } }
```

which projects to `<everywhere id="void-enforcement-area"/>` plus
`<apply block-place="deny(void)" region="void-enforcement-area" …/>`. This retires the previous run's
workaround of declaring a harmless build zone purely to switch the void rule on.

**Note the interaction:** `Areas` wires `block=no-void` *inside* `not-build-area`, while `VoidEnforcement`
wires `block-place=deny(void)` over *everywhere minus its exclusions*. Declaring both on a board that wants
bridgeable zones will deny the bridging the zones were for — put those zones in the exclusions, or use one
mechanism and not both.

**The evaluator does not see a layout `subtract`.** `POST /plan/evaluate`'s `G8 fill-ratio` is measured on the
plan's rectangles. `basalt-reach` reads 0.811 — almost solid — while the built board has two large voids cut
through it by a `subtract` in the layout. The advice is still worth having; it is measuring a document that
does not yet know about the hole.

## 10. Things that were true, still are, and cost other runs a cycle

Carried forward from `AGENT-REPORT.md` / `AGENT-REPORT-2.md` / `FINDINGS.md`, re-confirmed on this build:

- **`base_height: N` puts the top block at `y = N−1`.** Confirmed at every tier: `low-mid` at 13 → y12,
  `terr-mid` at 18 → y17, `shelf` at 22 → y21, `crest` at 26 → y25.
- **A spawn shape's interior is never painted by its theme.** `(0, 85)`, the centre of the spawn platform,
  reads raw `Stone` under the wool monument on a board whose crest theme is quartz. Third map to report it.
- **Export into a fresh, empty directory every time** (`B102`). The harness in `tools/` deletes the target
  before unzipping for this reason.
- **Ask the evaluator before compiling.** `POST /plan/evaluate` costs nothing, needs no map row, and named a
  hard `BZ6` violation (a build band two cells from a wool room) plus three soft ones on the first draft of
  the Marlstone plan. Score went 1008 → 3.7 across two edits, both of which improved the board.

## 11. Four more silences, found by driving another model's documents through cold

Everything in this entry came from `reports/grok-run1.md`: three maps written against the documentation
with no live API, then posted to the endpoints for the first time. Every fault below is one the author
could not have seen, because each of them answers `200`.

**A rectangle's four fields are `min_x`/`min_z`/`max_x`/`max_z`, not `x`/`z`/`w`/`h`.** This is entry §1's
trap one level down: the shape carries `type: "rectangle"`, so `RingOf` dispatches correctly, and then
reads four properties that are not there. Unknown keys are dropped, the known ones default to zero, and
the ring is a degenerate point at the origin. Fourteen rectangles across two maps covered nothing.
`sketch/from-plan` answered `{"ok": true}`; `sketch/finish` answered `422 Nothing is drawn`, naming the
layout rather than the shapes.

**`relief` rides at the document root, not inside `layout`.** Written beside `shapes` and `islands` it is
dropped silently. Root, keyed by island id — and the island id has to be the one the layout actually
carries (a compiled layout's is `team`, not whatever the hand-written document called it).

**The relief vocabulary is `marks`, and a plausible one is not read.** `{noise: {...}, features: [{type:
"hill", …}]}` parses, keeps `base`, and produces a flat field: `SketchReliefJson` reads `grain` and
`marks[{kind: point|line|area|rim|scarp, at, r, h}]` and ignores the rest. Relief is also **island-wide**:
a shape keeps its own stated top only under `relief_scope: "hold"`, so a relief whose `base` disagrees with
a terraced board's surfaces flattens the terraces and nothing reports the conflict.

**A house prop over the footprint cap is dropped without a word.** `HouseProp.MaxFootprint` is 192 blocks²
and `Footprint()` answers null past it — no finding, no warning, an export with no building in it. Seven
of seven houses vanished this way. The cause upstream was a unit error worth its own line: **dressing is
in world blocks, and a plan is in cells**, so props copied from plan-space coordinates land at 1/`cell`
scale — and a room dimensioned in cells (12 × 5) becomes a 60 × 25 stadium once multiplied back.

**A section's lines are the renderer's, not the world's.** `--section` blends a horizontal scale over the
image (`SectionRender.DrawScale`): a white line at 16% alpha every `--ticks` blocks of Y (default 8) and a
**yellow** one (`#FFD400`) at 36% every fifth tick — every 40 blocks by default. They are translucent because
they are drawn over the terrain rather than replacing it, the same discipline the heightmap's contours use,
and there are **no vertical gridlines at all**: every vertical division in a section is a real block. The two
backgrounds are also two different answers — pale `#E7ECF3` is air inside a loaded chunk, near-black
`#0E0E12` is no chunk at all.

**A house wing under three blocks on either side is dropped, silently, like one over the cap.**
`HouseProp.Footprint()` answers null when `maxX - minX + 1 < 3` or the same on Z — a wing has to hold two
walls and an inside — and null past `MaxFootprint` at the other end. Both ends of the range fail the same
way: no finding, no warning, an export with one fewer building than the document asked for. Three blocks is
therefore the legal minimum and not a fault; the smallest building in the Grok run measures 7×7 stamped,
from a 4×4 authored wing plus its eaves.

**The approach wall is recorded one column wider than it is built, on both axes.** A structure read that
trusts `provenance.json` — which `--topdown` does, and says so with `STRUCTURE READING: RECORDED
PROVENANCE` — draws Grok Ridge's wall as a **26 × 3** bar. The world has a **25 × 2** one. Measured on
`maps/grok-ridge`, four columns along its length:

| column | top block |
|---|---|
| `(−25, 34)` · `(−25, 35)` · `(−12, 34)` · `(−12, 35)` · `(−1, 34)` | cobweb y21 over bedrock y20…16 — the wall |
| `(−25, 36)` · `(−12, 36)` · `(−1, 36)` | stone brick y17 — the mid terrace, no wall |
| `(0, 35)` | chiselled stone brick y18 — the rim, no wall |

The cause is two conventions meeting: `StructureStamper.StampWall` walks its footprint **max-exclusive**
(`for x < maxX`), which is what the intent's own rect means — `SketchWorldBuilder` says so in a comment
("intent footprints are a fractional corner pair over whole world blocks (max exclusive)") — while
`ClaimStructures` hands the same rect to `WorldProvenance.ClaimRect`, which walks it **max-inclusive**
(`for x <= maxX`). One extra column on each max edge, in the sidecar only.

Worth knowing for two reasons. A wall read from a render looks thicker than it plays, and a bedrock line's
thickness is exactly what decides whether it can be built over. And it is a reminder that the provenance
sidecar is a *record of intent to claim*, not a read of the blocks: where the two disagree, `--column` is
the one that has looked at the world.

## 12. Two PowerShell traps, if you drive the API from Windows

Not the studio's fault, but they cost a cycle each and the failure looks like a server bug.

- `ConvertFrom-Json` hands an array to the pipeline as **one object**, so a helper function that returns it
  re-wraps it: `@(Read-Doc 'props.json')` yields a single element. Read inline.
- `ConvertTo-Json` wraps an `Object[]` that came from `ConvertFrom-Json` in a `{"value": [...], "Count": n}`
  envelope when it is nested inside another object, and unrolls a **one-element** array to a bare object.
  The first produced a `dressing.props` the rasterizer read as nothing; the second produced
  `layout.islands` as an object, which `sketch/finish` refused by name — the good case, because it said so.

---

## The loop, as actually driven

```
POST /api/plan/evaluate      <plan>                 # no map row needed; do this first, twice
POST /api/plan               {"name": "..."}        -> {"slug": "..."}
PUT  /api/map/{slug}/plan    <plan>
POST /api/plan/compile       <plan>                 -> {layout, intent, warnings}
PUT  /api/map/{slug}/sketch  <your own layout>      # verbatim replace; the compiled shapes are discarded
POST /api/map/{slug}/sketch/relief/read <layout>    # look at the ground before building it
POST /api/map/{slug}/sketch/finish
PUT  /api/map/{slug}/intent/from-plan <compiled intent>
GET  /api/map/{slug}/export                         -> the world, into a fresh directory
```

The compiled layout is thrown away and a hand-written one `PUT` in its place, which is documented behaviour
and removes the whole "address a compiled tier by the height it stands at" problem. What is kept from the
compile is the **intent** — it carries the spawns, the wool rooms, their entries and floors, and the
`structures.walls` a plan's `walls` entry produced, none of which the layout states.
