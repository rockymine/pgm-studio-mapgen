# Generation notes — what an agent has to know before it can draw ground

Everything here was learned by driving the live API and reading a column back, not by reading a document.
Each entry is something that either is not written down, or is written down somewhere a person authoring a
map would not think to look. The tool documents in `pgm-studio/docs/tools/` remain the reference; this is
the errata an author needs beside them.

Measured against `pgm-studio` at `claude/pgm-studio-mapgen-tasks-5kj6sm` (14 Aug 2026), building
`maps/marlstone-steps`.

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
- **`--buildings --roof <ids>` under-reports if your roof is slabs.** A `HouseStyle` with `roofSlab: 44`
  surfaces its roof in *brick slabs* (id 44), not brick blocks (id 45), so `--roof 45:0` finds only the ridge
  and verge. Twelve houses that had all stamped reported as "6 roof components". Check the census against the
  top-down before believing a house is missing.
- **The category top-down now reads structure from recorded provenance** (`B133`) — it prints
  `STRUCTURE READING: RECORDED PROVENANCE`. Terrain painted in stone brick, quartz or sandstone reads as
  *ground*, which it did not before. The warning in older reports that a built-looking block reads orange no
  longer applies to a map this studio built.

## 7. Things that were true, still are, and cost other runs a cycle

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

## 8. Two PowerShell traps, if you drive the API from Windows

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
