# showcase/ — one technique per map

Every map in `maps/` is a board: a whole design, with a dozen decisions in it at once. That makes them poor
things to learn from. A reader who wants to know *how a cliff is stated* has to find the cliff inside a
thousand-line finish and work out which of its fields are the cliff and which are the map around it.

A showcase is the other thing. It is **one technique, on a board that does nothing else**, so the document
that states it is short enough to read in full and small enough to paste into an example. Each folder here is
a complete map — it compiles, it builds, it exports, a server would load it — and the only reason it exists is
the one line in its README saying what it demonstrates.

## The rule that makes them readable

**Every showcase forks `02-theme` and changes only what its technique needs.** `02-theme` is a plain
**100 × 100 square destroy board**: two pieces, one spawn and one destroyable a side under `rot_180`, and
nothing else. It scores **0** against the evaluator with no violation and no lint, so anything a showcase's
evaluation says is about the technique rather than about the board.

That makes the **diff the lesson**. A reader comparing `08-cliff`'s finish against `02-theme`'s sees the
technique and nothing else, and a reader comparing two showcases against each other sees exactly what
separates two ways of moving ground.

**The board is a square because a technique is easier to read on ground that says nothing.** A
capture-the-wool board needs a lane, a technical void and a strait, and every one of them is a decision in
the picture beside the cliff you came to look at. A destroy board needs none of the three, so the square can
be empty — and it is, apart from two spawn pads at the ends and a cairn a quarter of the way in from each.
The 75% dead ground `/coverage` reports is that emptiness, not a fault.

**Four boards keep the capture board instead**, because their technique is about a wool board's own
furniture: `01-base-board` (which *is* that board), `16-forest` and `17-houses` (props measured against
spawn keep-outs and door approaches), and `18-wall-and-iron` (a defence wall whose chest face is derived from
where the wool is). Everything else is square.

**Nothing here ships a default room shell.** A spawn with no bound style stamps a bedrock box, so every board
binds `tools/styles/showcase-hall.json` — a shipped preset forked into the library's three tone families:
ground **verdant + dirt**, built **grey stone + loam**, accent **brick**. The four capture boards bind
`showcase-cage.json` beside it for the wool room.

## The two things `rot_180` decides for you

Both cost this folder a rebuild, so they are worth stating before the first technique.

**Every authored shape is fanned, so it has to clear every *other* shape's reflection as well as the shapes
themselves.** On a board twice as long that rarely bites; on a square centred on the mirror it bites
constantly — `03`'s dais landed in its own court, `10`'s tor and delve landed in each other, `21`'s two
flights landed on each other. The habit that avoids it is to draw on **one half of the board** and let the
fan finish, which is what every square showcase here now does.

**A shape centred on the mirror is its own image, and should be drawn once.** `21`'s wall runs the width of
the board: written as two boxes either side of the gate it comes out twice its stated thickness, because each
box's image lands on the other. Written as one box from the west edge to the gate, the fan produces the east
half exactly.

## What a folder holds

```
<nn>-<concept>/
  README.md                    what the technique is, the document that says it, what to look at
  <nn>-<concept>.plan.json     the board            — authored
  <nn>-<concept>.finish.json   the technique        — authored
  <nn>-<concept>.layout.json   what was posted      — written by the driver
  <nn>-<concept>.intent.json   what was posted      — written by the driver
  provenance.json              which pass claimed which column — a literal census of what landed
  renders/                     the pictures it was reviewed from, including the board grid and the flow
  world/                       region/, level.dat, map.xml — what a server loads, and nothing else
```

The two authored files are the whole of the input. Everything else is derived from them and committed so a
reader can see the result without a running studio.

## Running one

```bash
python3 tools/drive.py showcase/<nn>-<concept> "<Map Name>" --out showcase/<nn>-<concept>/world
```

The driver posts the two documents through the whole pipeline and prints every finding at every place one can
appear. `tools/README.md` documents it; `AUTHORING-BRIEF.md` is the authoring account these were written
against.

## The showcases

Read them in order the first time — each assumes the one before it. `02` is the square board, and is what
`03` onward fork; `01` is the capture board `16`–`18` are built on.

| | Folder | The technique | Stated in |
|---|---|---|---|
| 01 | `01-base-board` | the smallest legal **capture** board, and what "legal" is measured by | the plan |
| 02 | `02-theme` | the square **destroy** board, and one `TerrainTheme` on it — surface, fill, rim, wall, bedrock, read off two columns | `themes` |
| 03 | `03-paving` | scoping a theme to a patch, picking a pattern legible where it lands, and why an edge is geometry rather than paint | `addShapes` + `themes` |
| 04 | `04-organic-outline` | replacing a compiled ring with a drawn one, bent by Bézier controls — the `elderwold` / `cairnmeadow` coast | `shapePropsById` |
| 05 | `05-steps` | a stair as one plan piece per tread, a theme per tread — and the one gate that names a step too tall, which is looking at the wrong end of the flight | the plan |
| 06 | `06-ramp-and-slant` | `anchor_heights`: a ramp below the build cap, a leaning slab above the ground, and the ceiling a tall shape raises for everyone | `addShapes` |
| 07 | `07-hill` | a relief: a `point` mark against a `push`, side by side, and why paint cannot follow elevation | `relief` |
| 08 | `08-cliff` | a `scarp` — two bands with the face left free, so what is authored is a grade — and the two ways up it | `relief` |
| 09 | `09-mesa-and-hollow` | the `area` mark, stacked rings, and the measurement of a push laid over a hollow | `relief` |
| 10 | `10-landform-shapes` | a landform as its own shape — `height_mode`, `skirt`, `anchor_heights` — so it can carry its own paint | `addShapes` |
| 11 | `11-channel` | a `subtract`: relief moves a surface, a subtract removes it, and its height is not read | `addShapes` |
| 12 | `12-underpass` | putting ground back over a cut with an override-add — a lid at a raised `floor` bridges it, the same shape at the cut's own floor refills it and is refused | `addShapes` |
| 13 | `13-pond` | a basin cut with a negative `crown`, and the water prop that fills it | `relief` + `dressing` |
| 14 | `14-river` | a valley `line` mark and the water course laid in it, one prop per fall | `relief` + `dressing` |
| 15 | `15-boulder-outcrop` | rock at three scales — a prop, a crowned push, an erected slab — and the block that silently gates every prop near it | `dressing` + `relief` + `addShapes` |
| 16 | `16-forest` | a wood is a list of trees somebody placed: an edge, two species, a flora floor, and what a canopy claims | `dressing` |
| 17 | `17-houses` | several buildings in one world — forked presets, roof forms, an L-wing, and a shell used as a boundary | `dressing` + `roomStyles` |
| 18 | `18-wall-and-iron` | the two structures the composer never asks for: a defence wall and a renewable iron cube | the plan |
| 19 | `19-mountain-range` | a range of mountains, drawn entirely with pushes, around a board that stays one open dale — `crown`, `amounts`, `falloff`, and the marks not written | `relief` |
| 20 | `20-undercroft` | a storey under the landmass: lifting the ground's floor to make room, and stating the **rock** banded round its rooms rather than the rooms alone | `addLayers` |
| 21 | `21-wall-and-stair` | a wall you can walk on, drawn once and fanned, with a flight as one anchored polygon — and `keepClear`, without which a road repaints its top course and a channel cuts it out | `addShapes` + `dressing` |
| 22 | `22-indoor-pool` | water in a theme's **surface bucket**, so a pool is the rectangle drawn rather than a swept disc's outline | `themes` |
| 23 | `23-maze` | a Backrooms lattice: runs on a pitch, one link in three left out, and the rule that survives `rot_180` | `addLayers` |
| 24 | `24-underground` | a room built inside the rock: a wall that is one even-odd ring, a doorway that is an override add, a ceiling on its own layer — and what a prop can be given in a cave | `addLayers` + `dressing` |

## What every board here found out, in one place

Twenty-three boards measured the same system, and these came up more than once. Each is stated in full where
it was found; this is the index to them.

| Fact | Measured in |
|---|---|
| Stone, Andesite, Stone Bricks and Cobblestone are four names for one grey — a pattern built out of them is invisible | `02` |
| Paint cannot draw an edge on ground it is flush with: `axis: "inward"` reads inset from the **landmass**, and `rimEdges: "boundary"` groups by height. A kerb is one course up | `03` |
| A theme has no bucket keyed on elevation. Rock above grass is a second **shape** | `07`, `10` |
| One gate names a step too tall and it only looks at the step **out of a spawn** (`SP8`). Three treads down the same flight it is silent, and `WalkGround.Steps` has no maximum climb at all, because it models a player who can place blocks | `05` |
| A plan lint reads plan-piece surfaces and nothing else, so it complains about a walkable flight stated on the plan and says nothing about a fifteen-block slab stated in the layout. Its silence and its complaint are worth the same | `05`, `06` |
| An erected shape raises `<maxbuildheight>` for the **whole board**: twenty over the highest ground the world builds | `06` |
| A mark that carries the wrong field names is not defaulted sensibly — a `scarp` written with a `line`'s fields pinned the board to bedrock, gate still OPEN | `08` |
| A push applies to the already-solved surface, so a push over a hollow fills it in, and a push cannot be matched to a ramp | `09`, `maps/opus5-whinnymoor` |
| A subtract's `floor` and `base_height` are not read: the whole column goes, however tall the shape says it is | `11` |
| Within one sketch layer a column carries one span, so an override-add **replaces** the column rather than standing over it. Stacking is what `addLayers` is for | `12` |
| That is also what separates a lid from a fill: an override add resting **above** a subtract's own floor moves the span up and leaves the void under it, and the same shape at the subtract's floor refills it and is refused | `12` |
| Two adds at one floor are ordinary ground and the taller wins the column outright — so a room stated as a shorter add inside a taller slab is **not in the world**, with no finding anywhere. Band where the heights differ, overlay where they do not | `20`, `22` |
| A water prop's level is the single lowest ground its band touches — one prop over a falling course pools the whole run flat | `13`, `14` |
| A **subtract is a claim about the whole stack**, not about one layer: rock cut with subtracts forbids the landmass over it, and rock stated over the board's own void fills that void from below. State a storey as adds, banded round its holes | `20` |
| Lifting the compiled ground to make room for a storey needs the **plan** to say so too. Move the finish's floor alone and the spawns stay where the plan put them, thirteen courses under their own ground, and every placement reads as over open void | `20` |
| A placement reads as over open void unless its column has a span at **Y = 0** — a storey resting at `floor 1` leaves the whole board without one | `20` |
| A wall or a crop bed drawn as terrain **is** terrain: the painter writes it with a theme like any other ground, so a stroke repaints its top course and a channel cuts it down to the water line. `keepClear` is what separates a made thing from the ground | `21` |
| A keep-out **stops** a prop; it does not route one. A road that would cross a marked shape wants redrawing | `21` |
| Water in a theme's surface bucket is a pool; a water prop is a river. The prop sweeps a disc and carves its own bed, which gives an outline no room has | `22` |
| A storey's headroom is the gap between two spans and needs no field: a floor of seven courses under rock starting at fourteen is six courses, everywhere, by construction | `20`, `23` |
| A block's own id decides whether a prop may stand near it: wool, sandstone, stone brick and stained clay are all in `BlockRoles.IsBuilt`, and a prop declines on built ground | `15` |
| A goal keeps a 21-block clearance (`OB19`), which on a square board is a quarter of the middle band — the objectives, not the terrain, are what decides where dressing may go | `15` |
| A `wallRun` reads `PerimeterArc`, and an **internal riser** is `-1`, which falls back to the first run: a raised patch inside an island comes out one flat colour on all four sides. It is the same "measured off the landmass, not off the shape" cause as `axis: "inward"` | `03` |
| A tree claims every cell its **canopy** reaches, not its trunk cell | `16` |
| Repainting a preset's top-level `wall` and not `storeys[*].wall` is a fork that changes nothing — provable by a byte-identical preview | `17` |
| The defence wall's chest face is derived, not authored: it is the **approach** side, and a `side` field is silently ignored | `18` |
| A mark is a constraint with no falloff, so no mark makes a mountain: a `point` summit is a drum on a sheer wall. A landform is a **push**, and its `crown` — record default `0` — is what separates a mountain from a mesa | `19` |
| A brush stroke reaching past the land is the only add on that column and builds a speck of bedrock standing over the void — a disconnected island made of paint | `19`, `maps/opus5-sandcaster` |
| A hollow ring is one even-odd polygon and the thickness it states is the thickness it builds, from one block up — under a landmass exactly as above it | `24` |
| A wall inside a room is stated from the **floor's own floor**. From the floor's top it stands over a trench of its own depth, and `SK9` — the only `Severity.Decline` the layout check raises — reaches no 2xx response: `GET …/findings` is the one read that answers it | `24` |
| `layer` is a prop's only vertical control and a stroke honours it. A goal's clearance and a `keepClear` mark do not: both are 2-D and reach every storey, so a lid marked `keepClear` makes the room under it undressable | `24` |
| `seat: "ground"` reads the **maximum** ground top over every layer, so a made thing drawn in a cellar seats on the roof of the cellar | `24` |

And one that no board found and every board needed: **a per-block column transect is the only read that says
whether a route can be walked.** Sampling every two blocks makes a two-block riser and two one-block risers
the same number.

## The map they add up to

`maps/opus5-whinnymoor` is a whole board built out of them — a slate quarry cut into a moor, at score 0 with
0.0% dead ground. `review/opus5-whinnymoor.md` says which showcase every part of it came from, and records
the one pair that fought: a push and a ramp cannot be matched to each other, because a push is applied after
every constraint the ramp was drawn against.
