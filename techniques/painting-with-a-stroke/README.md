# Painting with a stroke

**A stroke is a band of surface along a drawn line: it repaints the top course of every column it crosses
and adds no cell.** That is the whole difference from a shape. A shape's outline is where one finish stops
and another starts; a brush has no outline to stop at, so it is what feathers a strand into a meadow, and it
is what lays a road down a hillside without becoming a ramp. Open it in the studio as
`technique-painting-with-a-stroke`, or run `build.py`.

**Row 1 is a strand meeting a meadow four ways, row 2 a serpentine cut into a hillside and paved four ways,
row 3 what a pave may read and what turns the brush away.** Twenty-eight props over twelve panels and three
layers, and the board stores and builds with no finding at all.

## The document

A stroke is a **prop**, not a shape: it lives under `dressing.props` and it is placed after the ground is
built and the water is in. Its `points` are a centerline, `radius` is half the band, `style` shapes the
band, `pave` is what fills it, and `claimsGround` is whether it holds what it paved.

```json
{"id": "way-road", "kind": "stroke", "layer": "ground",
 "points": [[-201, -28], [-129, -28], [-129, -6], "…"],
 "radius": 3, "style": "solid", "claimsGround": false, "seed": 4,
 "pave": {"kind": "cell", "cellSize": 4, "palette": [
    {"kind": "solid", "id": 4}, {"kind": "solid", "id": 1}, {"kind": "solid", "id": 1, "data": 5}]}}
```

| panel | the stroke | what it built |
|---|---|---|
| `butted` | none | the sand shape's own outline: a ruled line against the meadow |
| `feathered` | one `rough` sand stroke on the seam | the same line, wandered: 930 cells |
| `two-tongues` | a mottled sand-and-grass stroke up, a sand stroke down | a zone instead of a line: 1,216 + 733 |
| `tapered-tongue` | the same line, `tapered`, radius 6 | full width at the middle, run out by the ends |
| `road` | `solid`, radius 3, three stones | 1,622 cells of clean road |
| `weathered` | the same band, the road's stones mixed with grass | 1,622 cells — the same brush, a different fabric |
| `verge` | radius 6 coarse dirt under radius 3 road | 3,302 + 1,622 on one centerline |
| `claimed` | the identical pair, `claimsGround: true` | the same paving; **1,136 fewer plants** |
| `by-height` | the pave as a `height` stack | coarse dirt at y11, cobble at y20, andesite at y30 |
| `by-inward` | the pave as an `inward` stack | **every cell the `beyond` material**; neither band lands |
| `over-a-crossing` | a way over a causeway and a way over a bridge | the causeway repainted; the bridge untouched, and the way paving the gorge floor under it |
| `keep-clear` | the causeway marked, the bridge paved on its own layer | 416 cells become **314**; the bridge takes 90 from a stroke of its own |

## A seam a shape cannot make

**A shape's outline is a ruled line, and against a second theme that is what it looks like.** In `butted` the
column at (−165, −95) is meadow and the one at (−165, −89) is strand, and the boundary between them runs
dead straight across the panel because it is the sand rectangle's own `min_z`.

**A `rough` stroke wanders its own width against a noise field, which is what makes the same seam read as a
shoreline.** `feathered` lays 930 cells of sand along the line, and at (−55, −96) — the same distance north of the same
seam, where `butted` is meadow — the column is sand. Nothing about the shapes changed; a band of surface was
laid over the join.

**Two tongues are better than one, because a shore is a zone rather than an edge.** `two-tongues` runs a
mottled sand-and-grass stroke up into the meadow and a plain sand stroke down onto the strand, and the
result is a gradient with no line in it at all.

**A `tapered` stroke varies its width along the arc — full in the middle, 0.35 of it at the ends — so a spit
fades out instead of stopping.** Measured across `tapered-tongue`: (165, −95) is sand, and (125, −95), the
same distance off the same line near its end, is still meadow with a fern on it.

## A road along the route a player walks

**The relief cuts the bed and the stroke paves it, and they are two statements about one road.** Every
row-2 panel carries the same serpentine as a `line` mark with a `tread` of 3, which is what makes the
switchback walkable; the stroke follows the same centerline and decides what the tread is made of.

**The brush and the fabric are independent, and the fabric is where a road stops looking like a ribbon.**
`road` and `weathered` pave the same 1,622 cells with the same `solid` brush at the same radius. `road`'s
pave is a cell pattern over three stones; `weathered`'s is the same three with the meadow's own grass and
coarse dirt mixed into it, at a cell size of 3.

**That is the answer to a broken-up road, and it is better than a broken-up brush.** `worn` thins the band
with a per-cell dice and `stones` keeps only discs, so both of them take the band apart; a small cell pattern
mixing the path's finish with the ground's leaves the band whole and lets the ground show through it.

## A claim is a word, not a brush

**`claimsGround` decides whether the paving holds its cells against everything placed after it, and nothing
about how the band is drawn.** `verge` and `claimed` are the same two strokes on the same centerline over
the same relief: a radius-6 coarse-dirt verge under a radius-3 road, 3,302 and 1,622 cells in both panels.
One word differs.

**A claimed cell is skipped exactly, with no margin.** `PlaceFlora` reads `if (claims.Holds(x, z) …)
continue`, so the cover over `verge` grows on the verge — 2,927 plants — and the cover over `claimed` stops
at the paving, at 1,791. The two transects are the read: cell for cell, stations z −37 to −26 carry the same
two strokes on both panels.

**Paint is the default, and it has to be.** A claim is what a tree's and a boulder's standoff is measured to
— three blocks for a tree, two for a boulder — so asking one of every painted patch leaves a board with
nothing plantable on it. A road between two spawns is a claim; a gravel tongue over a crag is not.

## What a pave may read

**A pave is a full terrain material resolved per cell, not a block list — but the context a stroke hands it
is thinner than a theme's.** `PlaceStroke` resolves at
`new BucketContext(x, top - 1, z, TerrainBucket.Surface, 0)`: a world coordinate, the surface bucket, and
nothing else. Everything a band stack could be read along is answered from that.

| axis | what it reads | on a stroke |
|---|---|---|
| `height` | the block's own Y, less `from` | **works** — bands pinned to altitude |
| `depth` | `DepthFromTop`, which is 0 | the stack's first band, everywhere |
| `slope` | `SlopeDegrees`, which is 0 | the stack's first band, everywhere |
| `inward` | `Inset`, which is **−1** | `step < 0`, so the **`beyond`** material, everywhere |

**A `height` stack is the one that lands, and it is worth having.** `by-height` states coarse dirt for nine
courses from y6, then cobble for nine, then andesite: one stroke, and the road reads coarse dirt at y11 near
the foot, cobble at y20 halfway up and andesite at y30 at the top. A track that turns to bare stone as it
climbs is one prop.

**The same rule clips the foot of a `height` stack, and this board shows it.** `by-height` states
`from: 6`, and where the serpentine runs out below that — at (−129, 106), whose top block is y5 — the step
is negative and the column reads plain **Stone**, the default when no `beyond` is named. It is a pale patch
at the bottom of the road, and it is the one thing on this board that was not meant to be there.

**An `inward` stack does not land, and it fails the same way.** `by-inward` states a cobble rim over a
coarse-dirt middle and names spruce planks as `beyond`, and every cell of the stroke comes out spruce
planks: `LayeredMaterial.Resolve` returns `Beyond` when the step is negative, and a stroke's `Inset` is −1
because a stroke is not inside a landmass footprint. There is no finding.

**So a path cannot be banded across its own width by its material, and the way to band one is two strokes.**
`verge` is exactly that: a wide coarse-dirt stroke and a narrow road on the same centerline, laid in
document order, which gives the ring a single `inward` pave could not.

## What turns the brush away

**A stroke is turned away by ground somebody drew, and by nothing else.** The keep-out mask is about things
that *stand* on ground, and a stroke stands on nothing — held to the whole mask a road stops short of every
spawn and tapers away under an approach rect. What it does respect is **`"keepClear": true`** on a shape:
*"a shape drawn to be something — a town wall, a crop bed, a well's rim, a flight of stairs — is terrain by
construction and indistinguishable from the ground beside it."*

**The two crossings in row 3 are the two things a deck can be, and only one of them is terrain.** A
**causeway** is a ground-layer shape: `height_mode: "level"` at the bank's own top, solid to the bedrock,
constrained to the gap with one block of landing each side. A **bridge** is one course on a layer of its
own, `base_y` set so its top block is level with the banks and the gap under it stays open —
`section-crossing.png` is that gap.

**A causeway is repainted, because the brush cannot tell it from the bank it joins.** In `over-a-crossing`
its column reads **Cobblestone**; in `keep-clear`, marked, it reads **Spruce Planks**. The way paves 416
cells across the unmarked panel and **314** across the marked one, and it still runs to the causeway and
resumes beyond it — the keep-out is exact, with no margin.

**A bridge is not repainted, and it needs no marking: it is on another layer, and a stroke paves the layer
it names.** Its column reads Spruce Planks in `over-a-crossing` with no `keepClear` anywhere.

**Which is also why a ground-layer way across a bridged gorge paves the gorge floor.** The stroke asks
`context.GroundFor(path)` for the surface of *its* layer, and over the gorge that is the floor eleven blocks
down: at (79, 95) it reads andesite from the road's own pave where (70, 90), outside the band, is grass.
The stroke never stops — 416 cells over a 64-cell line.

**So a way over a bridge is three strokes, and `keep-clear` is the worked one.** Two on the ground layer
that stop at the lip on each side (176 cells each), and one on the bridge's own layer that paves the deck
(90). That deck's column reads **Cobblestone**, and the gorge floor under it is left alone.

**A deck lands on its banks when the marks that make the gorge share their boundary, and not otherwise.** A
ring covers the cells whose centres fall inside it, so a bank stopping one short of the cut leaves the cell
between them pinned by neither mark and the relaxation splits the difference — a ledge halfway down, and a
deck with nothing under its ends. Stated as abutting bands the walk reads **worst step 0, walked end to
end** from bank to deck to bank.

**A stamped block is never a road's to take, with no marking at all.** `DressingPalette.IsStamp` names
bedrock, obsidian, wool, gold, iron, emerald, chests and stained glass, and `PlaceStroke` skips any column
whose top is one of them. A monument does not need `keepClear`; a causeway does.

## Where the bands were cut

**The ground theme's slope bands were cut off this board's own `incline`.** 51.4% of its ground stands under
10° and 4.9% at 40° or steeper, with the serpentine's cut faces filling the 10–29° buckets; the bands cut at
30° and 55°, which puts meadow on the flats, coarse dirt on the road's cut faces and bare rock nowhere much.

**A stroke is finished after the painter, so the bands do not decide what a road is made of.** `census.txt`
says it plainly: the `moor` theme carries **seven** distinct surface blocks over this board — grass, coarse
dirt, cobble, stone, andesite, spruce planks and sand — because eighteen strokes wrote over it.

## The recipe

```json
{"id": "way", "kind": "stroke", "layer": "ground",
 "points": ["…the centerline…"], "radius": 3, "style": "solid",
 "claimsGround": false,
 "pave": {"kind": "cell", "cellSize": 3, "palette": ["…the path's blocks and the ground's…"]}}
```

- **a stroke repaints and adds nothing** — the bed is the relief's job, the finish is the stroke's.
- **feather a seam with `rough`, fade a tongue with `tapered`**, and reach for `worn` or `stones` only when
  the band is meant to come apart.
- **mix the ground's own blocks into the pave** for a weathered path; a small `cell` size does what a
  broken-up brush does without taking the band apart.
- **`claimsGround` only for what must stay clear** — a road, a protected verge, a crop bed's margin. Paint
  is planted over, and that is the default for a reason.
- **the pave can be banded by `height` and by nothing else**; across the width, use two strokes.
- **name a `beyond` on any stack**, or every cell whose step falls negative comes out plain stone.
- **mark a causeway, a wall or a flight `"keepClear": true`**, or the way over it repaints it. A bridge on
  its own layer needs no marking, and needs its own stroke to be paved at all.
- **budget a claim like a road**: three blocks of standoff for a tree round every paved cell.

## Limits

**Two of the five styles are deliberately unused here.** `worn` keeps a per-cell share of its band —
`PatternNoise.Unit(x, z, seed + 11) < coverage` — and `stones` keeps discs along the arc with gaps between
them; both are the right brush for a stepping-stone crossing or a scatter, and both are the wrong answer to
"make this road look weathered", which is `weathered`'s pave.

**What `DR-ROAD` charges for a claim is priced on the board it is on, not here.** A radius-10 claimed brush
is a 26-wide strip nothing plants in, and this card's claimed verge is radius 6.

## What checks it

- `dressing.json` — every prop and the cells it laid: the pair that differs in one word (3,302 against
  3,302, 1,622 against 1,622, 2,927 plants against 1,791), and the pair that differs in a keep-out (416
  against 314, with 176 + 176 + 90 in its place). No declines.
- `columns.txt` — twenty-two columns: both sides of the ruled seam, the same cell brushed, the taper at its
  middle and at its end, the three altitudes of one `height` stack and the stone at its foot, the whole of
  an `inward` one, all four crossings and the bank a deck lands on.
- `transects.txt` — five profiles: the beach the brush did not move, the same road section on both sides of
  the claim, the causeway along its way, and the bridge cell by cell from bank to bank.
- `census.txt` — three themes and nine surface blocks, which is what says a stroke changes blocks without
  changing themes.
- `incline.txt` · `slopes.txt` — the histogram the bands were cut against, and what the paving did to the
  walk, which is nothing.
- `painting-with-a-stroke.layout.json` — the one document the board was stored from.

Renders: `row1-seam.png`, `row2-path.png`, `row3-limits.png`; `crossings.png` for the two decks and
`section-crossing.png` for the gap under one of them; `iso.png` for all twelve.
