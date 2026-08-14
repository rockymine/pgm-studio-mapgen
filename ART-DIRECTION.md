# Art direction — how a board is supposed to look, stated as law

Twenty-one boards sit in this repository and the eye reads most of them as one board. That is the finding this
document exists to correct, and it is not a matter of taste: it was measured. Ten of twelve settlements put
every house on **two or three z-rows** behind the spawn, all facing the same way, on a "town square" patch —
never a watchtower in a field, never a barn in a clearing. Twelve of fourteen maps carrying buildings have
**not one building without a footing**. Four maps by three models stacked grass three courses deep. Almost
every board turned its rim on, including boards whose ground was solved by a relief. **No board has ever used
a path.** No board has ever themed anything except a village. **There has never been a desert map, and never a
four-team CTW board.**

None of that is a capability gap. Every rule below is expressible today, most in one field, and the hardest
one has a worked example already committed here. What was missing is a document saying which choice is right,
so three models reached for the same default.

**Read this before you draw ground, and check the board against it before the next stage consumes it.** It is
the same list the reviewer agent works from (`REVIEWER-BRIEF.md`), and the reviewer does not read your report.

---

## 1. Plan the board's silhouette before you plan anything else

Nobody has done this, and it shows in every board's proportions. Before a single shape is authored, decide and
write down: **the board's extent, its aspect ratio, where each spawn sits, where each objective sits, and the
two routes between them.** Five numbers and two lines. That is the board.

**A destroy board is a lane.** Six of the eight `minuyo` boards — the tightest set in the corpus — have one
dimension under 90. Every generated board here is roughly square (240×190, 170×220, 136×190), and on a square
board every goal is nearly equidistant from both spawns, which is why the ratios came out flat. The corpus
median board is **118 × 149**.

**The cheapest number to check a destroy board against**: a goal sits about **three times** as far from the
enemy's spawn as from its own. Corpus median 2.9 over 164 `dtcm` maps; only 27 of 164 fall under 2.0.

| | own spawn → goal | enemy spawn → goal | ratio | |
|---|---|---|---|---|
| corpus median | 49.4 | 135.2 | **2.9** | |
| `tallow-mirefast` · `tallow-kilnrow` | 40 · 43 | 140 · 139.5 | 3.50 · 3.24 | good |
| `quillon-foundry` | 77.8 | 109.8 | 1.41 | corpus p10 |
| `corvid-hollow` · `ashfall-scar` | 80 | 100 | **1.25** | below p10 |

The three lowest ratios are the three boards judged worst on play, arrived at independently. Two goals of one
team stand at least **35** apart and 70–75 is the good band; the nearest enemy goal wants 95–110.

**Then the identity, in one sentence.** *A frozen peat fen, dark and low, with an ice scarp on one flank.* *A
terraced clay hillside in five ochre steps.* *A red sandstone waterless canyon with a brick caravanserai at the
head of it.* If you cannot write that sentence, you are not ready to choose a palette.

---

## 2. The palette is nineteen hand-authored families, and you take two or three of one — never all of it

`TerrainPalette.Families` is not a generated list. It is **nineteen tone families, hand-picked and ordered
light to dark**, and it is the same vocabulary the surface read-back names a world by — so what you paint and
what a report measures cannot drift apart.

| Family | Blocks, light → dark |
|---|---|
| `verdant` | Lime Stained Clay · **Grass Block** · Green Stained Clay · Green Wool · Dark Prismarine |
| `spring` | Slime Block · Lime Wool · Emerald Block |
| `turquoise` | Prismarine · Prismarine Bricks |
| `loam` | **Podzol** · Brown Stained Clay · Soul Sand · Dark Oak Planks · Brown Wool |
| `dirt` | Oak Planks · Jungle Planks · **Dirt** · **Coarse Dirt** · Spruce Planks |
| `brick` | Granite · Polished Granite · **Bricks** · Hardened Clay |
| `rust` | Acacia Planks · Orange Stained Clay · **Red Sand** · **Red Sandstone** · Smooth Red Sandstone |
| `sand` | **Sand** · Birch Planks · **Sandstone** · Smooth Sandstone · **End Stone** |
| `gold` | Yellow Wool · Sponge · Wet Sponge · Melon Block |
| `pale stone` | **Diorite** · Polished Diorite · Mushroom Stem |
| `ash` | Light Grey Wool · **Clay** · Smooth Stone · Stone Slab (double) |
| `grey stone` | **Stone** · **Andesite** · Polished Andesite · **Stone Bricks** · Iron Ore · Coal Ore |
| `cobble` | **Gravel** · **Cobblestone** · Cracked Stone Bricks · **Mossy Cobblestone** |
| `mauve` | Mycelium · Light Blue Stained Clay |
| `azure` | Blue Wool · Lapis Block · Blue Stained Clay |
| `slate` | Cyan Stained Clay · Grey Wool |
| `dark` | **Nether Brick** · Black Stained Clay · Black Wool · Coal Block · Obsidian |
| `ice` | **Ice** · **Packed Ice** |
| `bright` | **Snow Block** · **Quartz Block** · Chiselled Quartz |

**The rule nobody followed: a pattern takes two or three members of a family, not the family.** A `cell` over
all five of `sand` is not a sandy ground, it is five sands fighting for the same square metre, and it reads as
noise from above. `tallow-kilnrow`'s `kiln-stack` is exactly that fault — a `cell` over five near-identical
whites — and it is why that board is described as clashing even though every block in it is pale. **Two
members is a texture. Three is a mottle. Five is a mistake.** If you want a fifth block, put it in a
*different* shape's theme, where the eye reads it as different ground rather than as the same ground being
indecisive.

**Reach across two families for a ground that has to read as one thing but not as one block** — `sand` +
`rust` is a desert, `cobble` + `grey stone` is a worked hillside, `loam` + `dirt` is a fen. Two members from
each, four blocks total, is a strong ground.

**Three sixteen-shade rows are not families and are not ground.** Stained clay, wool and stained glass are
*shade rows* — every damage value of one id. They are what you reach for when you want a **stated colour**: a
team's accent, a roof, a marker, a wool room's interior. Painting terrain out of a shade row is how a board
ends up looking like a colour picker. And be aware of a real gap: **eight stained-clay values belong to no
family at all** (`159:0/2/4/6/7/8/10/14`), so a board leaning on them renders magenta "unnamed material" in
`--surface` and you will briefly think your paint failed. That is `B147`, not your board.

**The two ways a palette fails, both shipped here.** It **vanishes** — `basalt-reach` puts all five themes on
Stone or Andesite and walls three of its five houses in Stone with an Andesite roof, so a building and the
hill it stands on are the same rock. Or it **clashes** — Kilnrow's five whites with a Red Sandstone two blocks
away and a Red Stained Clay boulder in the middle. **The test:** name your three tone families out loud and
say which is ground, which is built, which is accent. **A building may not be in the same family as the ground
it stands on**, and an accent that appears exactly once is not an accent.

**And match a pattern's cell size to the shape it covers.** Mirefast's `mire-timber` puts a
`{"kind":"checker","size":2}` over a shape 92 blocks wide. A two-block checker is texture at ten blocks and
noise at ninety.

---

## 3. The rim is off by default, and with relief it is off

Almost every board turned it on, because it was the default and nobody chose. **`Rim` is a `TopBand` with an
`Enabled` toggle**, and `RimEdges` decides which edges it caps at all: `void` caps only the landmass's true
outside, `drop` caps wherever ground falls away, `boundary` caps every plateau boundary.

**On any shape whose ground is solved by a relief, the rim is off.** A relief makes ground that rises and falls
continuously; a rim caps every one of those falls with a band of a different material, and the result is a
rolling hill wearing contour lines — terraced, artificial, and worse than no rim at all. This is the single
most common reason a board that should read as landscape reads as a model.

**Keep it where an edge is meant to read as an edge**: the outer coast of a landmass over void (`void`), the
lip of a built platform, the top course of a retaining wall. Those are edges an author *made*, and a band
along them is the map saying so.

**The wall bucket takes a pattern, not a block, and nobody used that either.** `wallRun` reads a cell's arc
along the outer void-facing face so a pattern runs *along* a wall; `wallDiagonal` cuts across it; a `layered`
stack varies the material *down* the riser, which is what a real cliff or a coursed retaining wall does. Tie
the choice to what the wall **is** — a natural cliff face, a built retaining wall and the side of a platform
should not read the same, and they currently all do.

---

## 4. Landforms have to flow into each other

This is the fault behind the ugliest ground in the repository, and it has a precise description: **a flat
20×20 pad butted straight against a hill.** One side of the seam is a level tier, the other is a slope, and
they meet at a vertical step nothing accounts for. It reads as two unrelated pieces of ground shoved together,
because it is.

**A landform meets its neighbour along a transition, and the transition is authored.** Four fields do it and
all four are shipped:

- **`skirt`** — how far a `raise` or `sink` shape's own edge ramps out into what surrounds it. A `raise`
  polygon with no skirt is a mesa with vertical sides; the same polygon with `skirt: 3` sits in the ground.
  **A hill with no skirt is the fault above.**
- **`anchor_heights`** — a height per vertex, so a surface **tilts** rather than sitting level. A depression
  whose far rim is two blocks higher than its near one is a bowl you look into; one at a single height is a
  hole.
- **`height_mode`** (`level` / `raise` / `sink`) — say which, deliberately. A shelf that should be cut into a
  slope is a `sink`, not a `level` tier that happens to be lower.
- **`relief_scope`** (`hold` / `exclude`) — `hold` keeps a built thing flat while the ground rolls around it.
  Without it the relief solves straight through your platform and the town arrives covered in contour rings.

**A depression and the hill beside it are one composition, not two.** If a board has both, the ground between
them is the interesting part: a saddle, a spur, a shoulder the path runs along. Author that ground. Leaving it
as the leftover rectangle between two features is what makes both of them look pasted on.

**Elevation is built from shapes, and a single relief pass is the generic answer.**
`tools/seeds/ruediger.plan.json` — hand-authored by this repository's author — steps its ground with **ten
`base_height` tiers and no relief block at all**. Use relief for ground that should read as *grown*, tiers and
shapes for ground that should read as *built* or *placed*, and let the two meet along a skirt.

**Rectangles are where a shape starts.** Promote a compiled tier to a polygon by replacing its `vertices`;
take Bézier `controls`. Two catches, both learned the hard way: a tier can fuse to **more than one shape**, so
reshaping only the first leaves the others' rectangles showing through; and **where the land is higher than the
piece** — a quarry, a sunken bowl — the land must run **over** the lower tier's fringe, mirrored from the
ordinary case.

**A large open area wants level changes in it, not more trees.** If a region ends up bigger than what fills
it, shrink the region.

---

## 5. Paths — the thing no board has ever used, and the one that plans the board

Not one of twenty-one boards authored a path. That is the largest single unused capability here, and it is
unused at exactly the layer where it would have done the most good, because **a path is not decoration. It is
the circulation diagram, drawn.**

**Author the path before the scenery, and author it as a route you named.** From the spawn door to the
objective. From the objective to the flank. From the wool room to the hub. You have to decide those routes
anyway — `approaches.md` says circulation is decided before dressing — and drawing them as paths does three
things at once: it states the route so a player can read it, it makes the ground along it **stay clean**,
and it forces you to have decided where a player goes before you start putting things in the way.

**Two different things are both called a path, and you want to know which you are using.**

- A **`path` shape** is *terrain*: a centreline with a band, rasterized into the ground as a footprint. It
  carries `path_edge` (`solid`, `rough`, `tapered`) and a `path_seed`, because a path is stored as the open
  line it was drawn as and the band is derived from it. This is the one that changes the ground.
- A **`path` prop** is *dressing*: it **replaces** the surface it crosses rather than adding to it — a finish,
  like paving. `GET /terrain/path-styles?pave=…` draws the five band presets so you can see one before you
  place it.

**`tapered` and `rough` are what stop a path reading as a stripe.** A `solid` edge at a constant radius is a
road painted on with a ruler. A path that narrows where it climbs and frays where it crosses rough ground is a
path people wore.

**And the hazard, because it will eat your village if you do not know it: a path's claimed band drops any
building that touches it, silently** (`B146`). Four of five houses on `basalt-reach`'s first build vanished
this way, on both orbit images, with no refusal and no warning. So place the paths, then place the buildings
clear of them — and if a building disappears between two builds, this is why.

---

## 6. A settlement is not a village, and a village is not a street

Ten of twelve boards built the same village. Measured:

| Map | Houses | Distinct z | Distinct x | Orientations |
|---|---|---|---|---|
| `tallow-weirgate` · `tallow-mirefast` · `ashfall-scar` | 14 · 9 · 9 | **2** | 14 · 9 · 9 | 2 |
| `tallow-kilnrow` · `basalt-reach` | 7 · 5 | **2** | 7 · 5 | **1** |
| `corvid-hollow` · `marlstone-steps` · `quillon-barrow` | 9 · 12 · 11 | 3 | 9 · 12 · 11 | 2 |

Only `sonnet-cinderreach` and `sonnet-holdfast` vary, and they are the same two boards that turned the footing
off — one model did notice, twice.

**Two separate faults are hiding in that table.** The first is that the houses are in a line. The second, and
the bigger one, is that **the only thing anyone has ever themed is a village**. A board is allowed other
built things, and they are more interesting than a sixth cottage:

- **A single house on a hill**, alone, with the ground around it bare. One building placed deliberately reads
  as more considered than nine placed adequately.
- **A house in a forest clearing** — the clearing authored as a shape with its own theme, the trees placed
  around its edge, and a path running to the door.
- **A mine head, a kiln, a wellhouse, a boathouse, a shrine** — one structure whose *style* says what it is.
  A `HouseStyle` carries a roof form and pitch, an overhang, a verge, a stacked `RoomCourse` wall, posts, a
  sill, beams, a porch and a storey stack; a squat one-storey building in stone with no windows and a heavy
  slab roof reads as a kiln without anyone being told.
- **A run of buildings along a board edge**, acting as a boundary. Note the limit honestly: a building whose
  interior is *filled* — a mass rather than somewhere to walk into — is **`B92` and is not built**, so an edge
  run today is enterable buildings and your review says so.

**A board carries at least three distinct placement ideas.** The village may be one of them.

**Where there is a village, its alignment is authored one prop at a time.** Buildings share a frontage line
because you gave them the same coordinate. And **the difference an eye reads first is aspect ratio and height,
not material**: six buildings in one style at six footprints and storey counts reads as a settlement; six
identical footprints in six materials reads as a swatch.

**Three placement rules are hard**, each somebody's shipped fault:

- **20 × 20 of open ground in front of a spawn** (`B172`). Only a single tree at the edge of it, boulders and
  fauna. **No houses.** Mirefast's corridor came out 12 wide; `quillon-barrow` has three houses in the box.
- **One block of clearance between buildings, eaves included** (`B166`). Corvid Hollow's house stands flush
  against the spawn with `"overhang": 2`, putting its eaves two blocks *inside* the spawn wall.
- **A building is at least 5 × 5 and at most 20 × 20** (`B167`, `B157`). Eight of Weirgate's fourteen came out
  four deep; `sable-marsh`'s spawn came out a **90-block hall**, because a stamped building is sized by its
  plan piece and nothing bounds it.

And: **a house may be stamped over void and nothing refuses it** (`B187`). Eight of eleven columns of
`quillon-saltworks`' `h1` stand on nothing. Check the ground under a footprint yourself.

---

## 7. Be literal: name the blocks, and start from a preset that exists

The last runs wrote house styles the way someone describes a mood. The system does not take a mood. It takes
a roof form, a pitch, a slab id, a wall of stacked courses with heights, a window form with a block and a
sill course, a door head with a stair. **Write the style at that level of detail, and start from a shipped
preset rather than from nothing.**

`HousePresets` carries ten worked, correct styles, and each one is a demonstration of a technique:

| Preset | Is | Worth copying for |
|---|---|---|
| `Desert` | *desert brick* — end stone and sandstone walls, a brick gable, birch stair lattice, **no sill** | a correct arched door head; a two-band `RoomPart` wall; a building with no footing |
| `Diorite` | *diorite pyramid* — two storeys of five under a brick hip | **the only correct slab roof idiom**: `Roof = Brick`, `RoofSlab = StoneSlab`, `Pitch = 1` |
| `Alpine` | *alpine mining* | a storey stack, and windows seated per storey |
| `Townside` · `Stilts` | a street building, and the same on stilts | how one style forks into two by geometry rather than by material |
| `Cottage` · `Longhouse` · `Terrace` | small, long, joined | **aspect ratio as the variable** |
| `Counting` · `Workshop` | a townhouse and a shed | function read from proportion |

### A house is not a rectangle with a roof on it, and four idioms nobody used prove it

Every building on every board is a rectangle with a roof form. That is not the shape of the system — it is the
shape of what the last runs reached for. Four things are expressible **today**, three of them demonstrated by a
shipped preset, and none has appeared on a board:

- **A house on stilts.** `HousePresets.Stilts` is `Townside` with its ground storey's wall replaced by
  `RoomCourse(Air, 5)` under one laid-log course — air below, the beam course kept, because on a building with
  nothing under it that seam is the one course that has to be there. Its windows are cleared, since there is no
  wall to cut one through. A wharf, a bank over water, a hut on a slope: all of them are this.
- **A flat roof walled by a parapet, roofed by nothing.** `HousePresets.Terrace` is "a room with an open deck
  on top of it": a storey whose wall is one course of cobblestone over two of air, with `Post = Air`. It is a
  **storey-stack idiom**, not a roof form — which is why nobody found it looking at `RoofForm`. A watchtower,
  a gun platform, a rooftop a player can stand on.
- **A porch.** `PorchStyle` gives a strip of the footprint up to a deck with its own `Roof` (a `Shed` by
  default, seated under the house's eave) and a `RailBlock` fence along its open edges. `Workshop` uses a
  spruce fence.
- **A storey stack where each storey differs.** `Storey` carries its own wall, posts, windows, floor surface
  and ceiling. Two storeys of the same material at different window forms is a different building from two
  identical ones, and it costs one field.

**And the one an author cannot reach yet, stated precisely so nobody claims it works.** The stamper builds a
house from a **`Footprint` of touching rectangles — wings** — and roofs the junctions properly: a building's
roof is the **union** of its wings' roofs, never a max of their crowns. Where a wing **projects** into another
it cuts the roof it pushes into across its own span, so its verge has something to sit on; where a wing's gable
end runs up against another it **marches**, each course stepping on along its own ridge until it hits a block,
with no overhang, since an overhang is what a roof has outside a wall. An L, a T or a U is one house under one
style. **All of that is built.** What is not is the authoring: a placed building is stored as **exactly two
corners**, so nothing in the studio can state a second wing, and two buildings drawn touching are stamped as
two buildings. That is `G172`'s open half and it is on the board. Until it lands, **do not draw an L as two
touching rectangles** — you get two buildings, or one building and a dropped prop where they overlap.

### Look at a house before you build a world

`/room-styles/preview` and its snapshot return **plan, section, isometric and cutaway** as SVG inside JSON, so
a style can be judged without a build — and `--section <regionDir> <out.png> --x <lo> <hi> --z <fixed>` cuts a
built one with a Y scale. Use both. A roof laid in slabs at a whole-block rise, a lintel that came out a solid
cube, a parapet a course too low: every one of those is visible in a section and invisible from above, and
every one of them shipped because nobody cut one.

**The one correct roof in this repository outside the presets** is `quillon-saltworks`' `h2` and `h5`:
`form: "gambrel"`, `pitch: 1`, `roofSlab: 126`, `roof: 5:5` — the slab in `roofSlab`, a whole block in `roof`.
Every other board inverted those two fields. Read it before you write a roof.

**A technique worth having**, and the one thing the last runs found that worked: nesting a `cell` inside a
`layered` gives a patchy top course over measured depth. A layer stack renders as one flat colour from above;
a `cell` in its top layer breaks that up without stacking anything. It is also how you satisfy the grass rule
below while keeping a varied surface.

### The material rules, and they are hard

Every one was broken on a shipped board. Each carries the task that will eventually enforce it in code; until
that ships, **this document is the enforcement.**

| Rule | The law | Broken on | Owns it |
|---|---|---|---|
| **Grass is one course** | A grass course is exactly **1 block** and grass never appears below it. A palette containing Grass Block is invalid at any `depth` > 1 unless it is the **top layer of a `layered` stack** — a `cell` is a pick, not a stack, so it writes its choice to every course. | 4 maps, 3 models | `B163` |
| **Obsidian caps at three** | A destroyable carries at most **3 obsidian**, so only the **pillar** styles may use it. `cube-3` (27), `cube-4` (64) and `column-plus` (15) take **end stone, gold or emerald**. | 27 · 27 · 15 | `B162` |
| **A slab goes in `roofSlab`** | A slab named in `roof` builds a roof you can see straight through. Slab in **`roofSlab`**, whole block in **`roof`**; a slab-course roof is right only at a **half-course rise**. | 6 houses + a spawn | `B168` |
| **No log, no ground material, in a roof or a verge** | Never a log. Never Grass Block or Podzol. | `verge: 162` on three boards; `quillon-barrow` roofs in **Grass Block** over **Podzol** | `B168` |
| **A block must be the kind its role needs** | `doorHead.block` a **stair**; `doorHead.fillBlock` under `upperSlab` a **slab**; a `slabBanded` window's block a slab, a `stairLattice`'s a stair. | cobble/cobble/pane · 98/4 · oak fence | `B160` |
| **A spawn door is 2.5 clear; a window is plain** | 2.5 blocks of clear height. A window is air or glass, and if filled, a **single block** — no patterned form, whatever blocks it is given. | 2.0 on two boards | `B161` |
| **A building seated into terrain has no footing** | Turn `Sill` off by naming **air**, as `HousePresets.Desert` does. | 12 of 14 maps, 0 opted out | `B164` |
| **Gable at `pitch: 2` loses to its own wall** | The wall wins where they disagree. Use `pitch: 1` on a gable until it is traced. | 13 houses on 3 boards | `B165` |
| **A goal name is a name** | No `<Team>`, no `<`, no `>`. PGM prints the attribute verbatim on both teams. | 5 boards, all Opus | `B182` |

---

## 8. Where the void goes, and the five things about a spawn

**Void belongs between the teams, not across an approach.** `approaches.md` is **amended**: the
middle-of-terrain hole is **withdrawn** for `dtm`/`dtc` and replaced by a **depression or a pond** — the same
interruption of a run, the same reason to go around or drop through, without removing the ground, and a
depression is an entrance from *below* besides. `tallow-kilnrow` is the counter-example: an 88-block cut across
65% of the board sat between its own objectives and the middle while the mid band, where the two sides meet,
stayed solid. The hole was where the join belongs.

Do not overcorrect: four small holes around a connected middle draw play into the centre and leave the flanks
unused. **A hole is also what makes a flank worth walking to.**

On a CTW board two islands sit **15 to 40** apart (`B158`), and a whole island belonging to one team is the
right shape rather than a defect. A **deliberately shared middle** crossing the symmetry axis is the one
composition an agent invented that the author wants kept — and it still needs the gap on **both** its sides.

**And the spawn, where four boards each broke a different rule:**

1. The door stands **≥ 15 blocks** from the nearest void (`B158`).
2. **20 × 20** of open ground in front of it (`B172`).
3. The ground it opens onto is **climbable back** (`B180`). **Move the route to the door, not the door to the
   route** — turning a spawn to face its stair puts an objective behind the player.
4. The spawn sits near the **back** of its lane (`SP2`); iron goes **beside or ahead**, never behind (`SP7`),
   and never inside its own protection region.
5. The ground under it carries something. Weirgate's yard is 80 wide for a 20-block spawn; Mirefast's is 92.

---

## 9. Circulation, and then dressing

State the routes, draw them as paths (§5), and **those runs plus a margin are the ground foliage does not
get.** This is the order the last runs inverted, and the symptom is a forest swallowing the route it was meant
to shelter.

**Nothing is scattered.** Every prop is placed because there is an answer to *why here*. If you cannot answer
it, leave the ground bare and say so — bare ground you chose beats dressing you did not.

**Compose the approaches so they differ.** Around · above · below · through. Three approaches that are all
"walk through cover" is one approach drawn three times.

**A forest is measured as canopy share, not leaf count** — a spruce forest at 17,600 leaves rendered as one
solid mass with the routes buried, while a corpus map at 17,897 leaves over 72 trees renders as a wood a
player walks through. And **avoid `whorled: true`**: 46 logs a tree at 1.26 leaves per log, against a template
spruce's 14 at 5.29 (`B174`).

---

## What this document does not cover

It says how a board should look and be composed. It does not say how a map **plays** — that is
`docs/gameplay/approaches.md`, whose claims are the author's and settled, and `match-flow.md`. Where those and
this one disagree, they are the law and this is the style guide.

And it decides nothing the author has not. A question about play that `approaches.md` does not settle is
**recorded as an open question in your report**, with what you decided and why — never filed as a fact. This
repository has already committed one confident, wrong, invented gameplay claim derived from a correct
measurement.
