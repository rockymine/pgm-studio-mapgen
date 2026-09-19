# What a board is made of

Every board in `specs/` passed every gate and several of them look wrong, and it is the same handful of
faults each time. This is the author's ruling in each case. **None of it is enforced anywhere** — no gate
asks whether a board looks like anything, which is why it is written down instead.

`ORDER-OF-WORK.md` says when the paint is decided; this says what to decide. Read it once before the first
theme is written, not while writing one.

**The through-line is simplicity.** A board is authored simple and detailed afterwards — the relief first,
then one ground, then the few places that are genuinely made of something else. Detail added later is
*chosen*; detail that comes out of a pattern is a roll of the dice, and a board is not improved by rolling it
five hundred thousand times.

---

## One objective, and air between the two sides

On a board a hundred blocks or less across, **one** destroyable a team is the answer — two of them close
together is one objective with two health bars.

And the two teams' ground is joined by a **build zone over void** spanning the board's whole width, never by
a land connection: a corridor is a place a defender stands, and a crossing a team has to pay to bridge is a
decision an attacker makes.

The land ends where the ground stops being anybody's, and the gap starts there. (The author's ruling. Both
halves of it were wrong on the first board authored against the brief that used to carry this.)

## Across a run of boards, check the tone families against each other

Name the three tone families for each board and check them **across** the set rather than within it. Five
boards can each be internally coherent and still be five greys: the ground family is the one nobody varies,
because grey stone is what every fill pattern and every exposed face reaches for.

Decide at least one board's ground to be warm, or pale, or red, before the first theme is written.

## What the studio checks for you, and what it does not

The numbers a board is held to are in `GET /api/rules` — the goal-to-spawn walk ratio (`GO1`), the strait
between two teams' groups (`CT12`), the ground a spawn door opens onto (`SP8`, `SP9`), the clearance around a
goal (`OB19`), the passage past a building (`DR-PASS`), how two wings of a house meet (`HJ1`–`HJ5`). Meeting
them is not a design achievement; it is the floor.

What no gate asks is whether the board **looks** like anything, and that is where every previous run's boards
came apart. The observations below are measured off shipped boards and are enforced nowhere:

- **How a board is painted is its own section** — *What a board is painted with*, below. It is the half of
  authoring no gate holds you to and the half every previous run got wrong.
- **Stained clay, wool and glass are shade rows, not ground** — a stated colour, never terrain.
- **The magenta block at the centre of every board is the observer platform's bedrock, and it is not a
  fault.** `SurfaceReport` legends a full cube no tone family claims as *unnamed material* and colours it
  magenta, so a block missing from a family reads as a fault in the board. Bedrock has no family on purpose —
  it is the map's floor and the shell of its walls. Do not go looking for what is wrong with it.
- **A goal's name is a name.** No `<Team>`, no angle brackets: PGM prints the attribute verbatim, on both
  teams, and a placeholder reaches a player.
- **The rim is off on ground a relief solved.** A rim caps every fall with a band and turns a rolling hill
  into contour lines; it belongs where an edge was *made* — a coast over void, a platform lip, a retaining
  wall's top course.
- **A landform meets its neighbour along an authored transition**, never a flat pad butted against a hill.
  The four fields are `skirt`, `anchor_heights`, `height_mode` and `relief_scope`.
- **Draw the routes as paths before the scenery.** Spawn door → objective, objective → flank, wool → hub. A
  path is the circulation diagram drawn: it states the route and keeps the ground along it clean.
- **A `polyline` *shape* is the layout's easiest curve, and it is not the `stroke` prop.** The rasterizer
  splines a polyline's points — centripetal Catmull-Rom, eight samples a segment — before offsetting the band,
  so four clicked points draw as a flowing wall rather than a chain of chords, and nothing has to be authored
  for it. `stroke_edge` is `solid`, `rough` (the width wanders ±45%) or `tapered`. `opus5-millrace`'s canal
  walls are three such shapes at three or four points each. Reach for one wherever a wall, a lane or a
  watercourse should flow; `controls` — Bézier handles — belong only on a closed ring of ground. **The
  `stroke` prop is the other thing entirely**: it repaints the top course of what it crosses and adds no
  cell, and `claimsGround` on it says whether trees, boulders and buildings keep off — which is about holding
  ground, not about players walking.
- **A board carries more than one placement idea.** A village behind the spawn may be one of them; a single
  house on a hill, a house in an authored clearing, a mine head or a wellhouse whose style says its function,
  a run of buildings as a boundary are the others. Six footprints in one style is a settlement; one footprint
  in six materials is a swatch.
- **Nothing is scattered.** Every prop is placed because there is an answer to *why here*. Bare ground you
  chose beats dressing you did not.
- **Start a house style from a shipped preset and fork it.** Ten exist, each demonstrating a technique;
  `GET /api/room-styles/{id}/json` answers one as the stamper's own JSON. Repaint `storeys[*].wall` as well
  as `wall`, or the fork is half applied.
- **Look at a house in section before building a world.** `/api/room-styles/preview` answers `plan` and
  `section`. Every shipped roof fault was visible in a section and invisible from above.

## What a board is painted with

The numbers here are measured over the **fifty-one** boards in this repository that carry a theme registry,
so they say how far a habit runs rather than how bad one board was.

**A pattern takes two blocks, not a family.** A `TerrainPalette` family is the set of blocks that read as one
ground, offered together so a list can be *filled* from one and then cut down — filling it is the first step,
not the answer. Two members is a texture; three is a mottle; five is a family shown off rather than a ground.
Of the **277 patterns** on these boards, **85% carry three entries or more**, 51 carry five and 8 carry six or
seven; only 15% carry two.

**A voronoi is never ground.** It draws a diagram — a grid of lines with cells reading off it — and there is
no landscape that looks like that. It belongs in the **fill**, where it is the body of the rock nobody sees
until a wall is cut, and it is made of **stone**. A voronoi whose bands are dirt and whose middle is grass is
the worst of both: a network of dirt lines nothing in nature draws. On these boards **44 of 50 voronois are on
the surface** and **none is in the fill**.

**Noise carries a texture, never a border.** A fractal field between two blocks of nearly the same shade —
sandstone into stone, dirt into coarse dirt — reads as one ground with grain in it. The same field between
two *different* grounds reads as static: the big destroy boards with the lake scattered sand into grass, and
what that draws is neither a beach nor a meadow. Where two grounds meet, the edge is **drawn** — a shape with
its own theme, a stroke, a painted band — and never sampled.

**A brush too small is static, and the cure is always bigger.** A field whose features are smaller than the
thing they dress reads as noise however good the palette is; the same field at three times the period reads as
patches, which is what looks deliberate.

The medians here are `cellSize` **6** for a cell pattern (down to 2) and `scale` **8** for a noise field (down
to 4). Those are the numbers that produced the boards being complained about.

Go up, then look at it: `POST /api/terrain/material-preview` renders one material and
`POST /api/terrain/theme-preview` the whole finish, in five views — `section`, `rim`, `surface`, `wall`,
`fill` — under `?format=png&view=…&scale=…`.

Without `format=png` it answers every view at once as JSON and `view` does nothing, which reads exactly like a
broken knob and is not one.

Neither preview builds a world, and neither can tell you what a theme sits **next to**: the sample terrain is
grey stone, so a grey theme reads as one mass there and may be perfectly legible on a board of grass.

**Three themes is a map.** A theme is a *place* — the moor, the works, the shore — and a board has two or
three of them. Giving every piece of the plan its own theme is not variety, it is the plan leaking into the
paint: sixteen boards here carry three themes, but eleven carry five, seven carry six, and five carry between
sixteen and twenty-four (`opus5-interchange` has **twenty-four**).

**Steps share one theme, and it is not the theme of what they join.** A flight of steps is *made* — it is the
one part of a landscape a person built — so it reads as stone, and it reads as the same stone the whole way
up. The grassy shelf at the top and the sandy floor at the bottom may each have their own theme; the stair
between them having a third is what turns a board into a swatch book.

**A landscape board is one theme, a relief and a handful of patches.** Every destroy board is a landscape
board. Author a **simple plan with few pieces**, put the shape of the ground into the **relief** rather than
into the piece list, paint the whole thing one ground, and then put the variation in where you *want* it. A
raised shelf carrying a city may have a theme of its own — but a city is not noise either, so that theme is
materials laid in courses, not a field sampled over them.

**Splotches beat patterns, and a splotch is a shape.** A theme is stated **on a shape** (`TP10`: map default ›
shape, winner takes all), so the brush an author reaches for is an `addShapes` polygon with a `theme` of its
own — a patch of bare dirt worn into a meadow, a sandy shelf at the water, a scorched ring. Ten of those over
one ground is a landscape somebody made.

The same two blocks in a cell pattern is a board that is a third dirt *everywhere*, including the places dirt
has no reason to be. If the answer to *why is it here* is "the noise put it there", it is not an answer.

**A building is never the ground it stands on.** A house is a thing somebody built on a landscape and it has
to read as one from across the map, which means its walls are not in the tone family under its feet. A stone
house on stone can be made to work and is a hard thing to get right; it is not the one to attempt. **9 of the
50 buildings** here are walled in the ground's own family — `opus5-siderite-bowl` puts three grey-stone houses
on grey stone.

Name three families out loud before painting: which is ground, which is built, which is the
accent. An accent that appears once is not an accent, and an ore block is never a building material.

**A path is solid, and it is three colours that are nearly the same.** A `worn` or `rough` band reads as
litter rather than as a way somebody walks: the style to state is `solid`, and the pave is three blocks a
reader cannot quite tell apart — **dirt, coarse dirt and spruce planks** where the ground is soft, **gravel,
andesite and cobblestone** where it is hard. A path is also a claim about circulation, so one that ends
nowhere, or that runs *through* a building rather than to its door, says the board was assembled rather than
drawn.

**Two blocks a landscape is not made of.** Mossy cobblestone and cracked stone bricks are noise wherever they
meet terrain — they read as damage, which is a statement about age that ground does not make. Keep them for a
built thing that has earned them.

**A boulder is stone.** Stone, cobblestone and andesite is the whole palette that reads as rock from any
distance, with an accent under it if the floor it stands on wants one. A boulder in the ground's own accent is
a lump, and a boulder in five materials is a sample board.

**A tinted block's family is the biome's to decide, so choose the biome before the patterns.** Grass, leaves
and water take their colour from the chunk's biome byte and nothing else on a board does, which makes the
biome a palette decision rather than a line added to the finish at the end. The rule reads twice.

A cold board takes a **cold biome**: snow and ice are blocks, so a snowfield on `Plains` has a summer meadow
running through it, and `Ice plains`, `Cold taiga` or `Frozen river` — all three tinting grass `#80b497` — is
what makes the two agree.

And grass with **podzol** is not a prohibition but a colour distance: on `Plains` the tint is `#91bd59`
against podzol's brown and a pattern mixing them reads as neither ground, where on `Mesa` (`#90814d`) or
`Swampland` (`#6a7039`) the tint comes to meet it and the pair reads as one dry, leaf-littered floor, which is
what those places are.

`GET /api/terrain/biomes` answers every biome's hex, so the check is a look rather than a guess: ask it of
each tinted block the palette names, once, before the patterns are written.

## Ground cover is one shape and two numbers

A `flora` prop is the pass that scatters ferns, grass and flowers over ground that already carries grass, and
it is the cheapest thing on a board: every one of its decisions is a noise field sampled per cell, so it
stores no state and re-exports identically.

**The shape is the whole board, not a patch of it.** `points` is an outline of three or more, and what it
states is the ground the pass is *eligible* to cover — the patchiness is the density field's job and the field
is better at it than a hand-drawn polygon. Several small shapes is an author doing the field's work by hand,
and it comes out as islands of planting with bare ground between them where no edge exists.

**Two of its numbers are gameplay and want to stay low.** `coverage` is how much of the eligible ground
carries anything at all, and `tallShare` is how much of that is two-block grass — which hides a player, and so
is cover nobody authored, in front of objectives nobody chose. A high `coverage` is a board whose ground
cannot be read at a glance, which undoes the slope banding it was painted with. Keep both modest and put the
character in `scale` — small is speckle, large is meadows and clearings — and in `flowerShare` with
`flowerScale`, which cluster into fields rather than confetti.

## What a building is made of

The two sections above are what the ground is made of. This is the other half, and it is shorter, because a
building is a short list of decisions and a shorter list of things not to do. The list is the author's and
none of it is enforced, which is why the shipped presets break the first item on it.

**No footing.** `Foundation.Footing` is null by default and that is the answer rather than an omission: a
footing is the course ringing the plate one block proud, and it is what a **deep** plate stands on — over a
plate of one course, which is what a house on a board has, it is a rim round a building with no foundation to
speak of and it reads as noise rather than as masonry.

Five of the thirteen presets carry one in cobblestone — `cottage`, `longhouse`, `terrace`, `counting house`
and `workshop` — and so do three of `opus5-lodestar`'s own styles (`berth`, `vault`, `shed`) and both of its
room shells. A fork of any of them carries the footing in unless it is set back to null.

**No shed, and no shed roof.** `RoofForm` offers six — `gable`, `flat`, `hip`, `gambrel`, `shed`,
`saltbox` — and one of them is not for a map.

**A log is a post or a beam, and a wall is neither.** Posts at the corners are what make a house read as
framed, which is what every hand-built house on the corpus does. Beams run out past those corners where two
storeys meet — and a beam has to be the end of something, so the wall under it carries a course of **laid**
log. A beam over plain infill is a beam ending in nothing.

**A checker in the same log as the posts is one mass.** Where a wall wants a checker it wants a *different*
log; where it does not, the posts are already doing that work.

**Two buildings are a row when they differ in height and footprint and in nothing else.** One style, three
plots, one of them a storey taller: that is a town. Three styles is three ideas, and five styles on a board is
a swatch book. What carries variety instead is shape — a tall wing against a low one, a hall against a cross
wing, two storeys against three — and a tall building is a perfectly good building where a board wants one.

**Fewer, and each one placed because there is an answer to *why here*.** A yard already standing a spawn hall
and two wool rooms does not need a fourth building, and `DR-PASS` will eventually say so anyway, which is the
wrong way to find out.

## Where made ground meets grown ground

A terrace over a meadow, a yard over a pasture, a quay over a shore: two grounds at two heights, and
everything a match is about happening where they meet. It is the most useful thing a plan can state, and it is
four decisions rather than one.

**The made ground is `exclude`, not `hold`.** `hold` lets the relief bring the lower tier *up* to the shape,
and then there is no step and no reason for a stair; `exclude` takes the footprint out of the solve and the
two tiers meet at a face.

**The boundary is not a straight line.** A retaining wall is straight where it is a wall and interesting where
it is a gate. Cut re-entrants and salients into the compiled edge one vertex at a time, and size each
re-entrant to exactly the flight that fills it, so a stair is set *into* the wall rather than leaning on it.

**The height difference is bridged by a stair and not by the relief.** A relief graded across the seam deletes
the boundary; a flight states it.

One polygon, two anchors at the foot and two at the head, `height_mode: "level"`, `skirt: 0`,
`keepClear: true`, and a `material` rather than a theme — a stair is a thing somebody built and a theme is a
place.

Give it at least twice the run as rise, and prove it with a transect: the plan tier walks pieces flat and
cannot see an authored flight at all, so `EL1` and `WL11` will go on naming the seam and they are not wrong
about the plan.

**The made ground's face is where its paint goes.** A `wallRun` stripes along the perimeter and a
`wallDiagonal` shears those stripes by height so they climb the wall at a slope. Neither is reachable by
anything sampled from the plane, and a retaining wall is the one surface on a board that wants them. Put a
`teamTint` in one run and the town wears the colour of whoever holds it, so a player reads whose terrace they
are looking at from the far bank.

That reads as ownership only where the ground under it is ownable. A tint is one colour per **canonical
island**, so on a board whose land is a single landmass — the ordinary capture board — every tinted cell takes
whichever team's spawn the ownership read first, and the whole map comes out one colour. `PT5` says so on the
build.

Where the land is one piece, put the tint on a **shape's own theme** — the terrace, the wall, the
structure that actually belongs to somebody — rather than on the terrain.
