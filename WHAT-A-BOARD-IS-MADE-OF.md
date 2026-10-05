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

## A core is the forward objective and a wool is the deep one

A core cannot be carried anywhere; it is breached where it stands, so it belongs where it will be fought over.
A wool has to be fetched and brought home, so it belongs behind. Drafted the other way round, `WL10` reads a
wool-front-distance of 8.

**A core on a group in open sky has nothing to catch its lava**, so the casing wants ground all round it: a
breach anywhere near an edge ends it at once. `float` and `leak` are one knob — the lava free-falls to the
terrain at `float` below the casing and leaks a course below `leak`.

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
- **Wool and glass are shade rows, not ground** — a stated colour, never terrain. Stained clay is ground
  only inside a set of its own tone, which *What a board is painted with* says.
- **The magenta block at the centre of every board is the observer platform's bedrock, and it is not a
  fault.** `SurfaceReport` legends a full cube no tone family claims as *unnamed material* and colours it
  magenta, so a block missing from a family reads as a fault in the board. Bedrock has no family on purpose —
  it is the map's floor and the shell of its walls. Do not go looking for what is wrong with it.
- **A goal's name is a name.** No `<Team>`, no angle brackets: PGM prints the attribute verbatim, on both
  teams, and a placeholder reaches a player.
- **A made thing is fanned onto the symmetry's orbit unless its layer group says otherwise.** The rasterizer
  copies a group's shapes onto every orbit axis where `mirrors` is true, which both the wire and
  `tools/sculpt/props.py`'s `LayerBuilder` leave it; a landmark seated on the symmetry centre is what states
  **`mirrors=False`**, so it is not doubled onto itself. Nothing refuses either mistake: the store answers
  200, pre-flight opens, and its mirror check reads spawns, wool rooms and build zones rather than made
  geometry. `column` at the image is what sees it, and the image of block `z` is **`−z−1`**.
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
  for it. `stroke_edge` is `solid`, `rough` (the width wanders ±45%) or `tapered`. A pair of canal
  walls comes out as three such shapes at three or four points each. Reach for one wherever a wall, a lane or a
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

## A hill is measured against the lane it stands in

**On a capture board a hill is measured against the width of the lane it stands in, and never against the
board.** A wool board's ground is thin by construction — spurs, limbs and a rim, with the objectives hung off
the ends — so a landform that would be one feature among many on an open map is the entire width of the ground
it sits in.

The measured case ran 36 blocks of land between a coast and a spawn hall's wall, with a spatter cone 20
blocks across in the middle of it. Every row of that lane carried 28 to 32 blocks of ground over 30°, 14 to 24
of them over 40°, and what was left to walk was a strip 4 to 8 blocks wide between the hall and a 42° face.

**So a hill on a capture board is either smooth enough to walk or far enough out to be off it, and the middle
of a lane is neither.** Smooth is measurable: the rebuilt cone rises 8 blocks over 16 at the shore, which
transects as *worst step 1, 0 barrier, 0 scramble, walked end to end*, and leaves 20 blocks of flat crest
between its foot and the spawn.

**A hill at the board's edge may keep its height, because only a portion of it stands on the board.** Centre
its ring over the void outside the coast and the skirt that lands reads as a cliff at the water rather than as
a cone with a path round it — which is the one place on a wool board where steep ground costs nobody a route.
The ring must still hold some land: a push's falloff is measured across the land, so a ring wholly over the
void lifts nothing and says nothing.

**The frontline and the ground in front of a bedrock wall are the two places a hill is always wrong.** Both
are ground a team has to cross under fire, and a landform there decides the fight instead of the players.

**A house is never inside a hill.** The measured case put a push's ring across the back third of a building's
footprint, and the ground at its back wall then stood **ten blocks** higher than the ground at its front: one
wall buried to the eaves and the other on the flat. It reads as a mistake from every angle it can be seen
from.

## What a board is painted with

Every ruling here was made looking at boards and swatches drawn with the game's own textures, and none of them
can be checked on a flat-colour picture: two noisy blocks of one colour are one calm grey in a swatch and
static on the ground. Where a ruling changed while it was being made, the later one is the one written here.

**A named block list is one answer, not the answer.** Where a ruling names blocks — a floor, a path, a boulder,
a ground's set — those are combinations that were looked at and passed, and the principle beside them is the
ruling. Five painters handed this section laid the same floor, the same boulder and the same two paths on five
different places, which is a default showing through rather than five choices. Find the board's own answer by
the same principle, and look at it.

**A tinted block's family is the biome's to decide, so choose the biome before the patterns.** Grass, leaves
and water take their colour from the chunk's biome byte and nothing else on a board does, which makes the
biome a palette decision rather than a line added to the finish at the end. The rule reads twice.

A cold board takes a **cold biome**: snow and ice are blocks, so a snowfield on `Plains` has a summer meadow
running through it, and `Ice plains`, `Cold taiga` or `Frozen river` — all three tinting grass `#80b497` — is
what makes the two agree.

And grass with **podzol** is a colour distance, not a prohibition. On `Plains` the tint is `#91bd59` against
podzol's grain of red, brown and muddy green, and the pair reads as a harsh border, worst when splotchy. On
`Mesa` (`#90814d`) or `Swampland` (`#6a7039`) the tint comes to meet it and the pair reads as one dry,
leaf-littered floor.

**Grass belongs on more than a meadow, once the biome is picked for it.** A desert, a badlands and an ash
field may each carry grass, and an ash field dirt as well, so long as the biome makes the grass flow into the
ground round it instead of standing in it as a summer meadow. `Desert` and `Savanna` both tint it `#bfb755`,
which sits beside sand; a snowy board takes a cold biome — `Cold taiga`, `Ice plains` or `Frozen river`, all
`#80b497`, or `Cold beach` just off them at `#83b593`.

**Two biomes of one colour are one biome on the ground.** Every biome the game stores is on the list, and many
share a colour: plains with beach, the frozen and cold ones with each other, every desert with every savanna.
A field that mixes two of one colour paints a boundary nobody can see, so a palette takes one biome per
colour, and `sharesTintWith` on each row of `GET /api/terrain/biomes` names which ones are the same.

`GET /api/terrain/biomes` answers every biome's grass, leaf and water hex, so the check is a look rather than a guess: ask it of
each tinted block the palette names, once, before the patterns are written.

### A ground is a set, not a block

**A ground is one tone carried by several textures.** The blocks mixed in one field sit close in colour and
differ in texture, and the closeness is what lets the textures merge into one ground: stone, andesite and
cobblestone; dirt, coarse dirt and spruce planks; stone bricks, polished andesite, andesite and stone. Tone is
also what decides how much of a noisy block a set can carry — cobblestone merges with andesite more easily
than with stone, because andesite sits nearer it.

**Three or four blocks, not two.** Two blocks side by side read as two materials colliding, even when their
colours are close. A path is best at a third each of three blocks, a built floor at a quarter each of four,
and dirt with coarse dirt at half and half — a few specks of coarse dirt in dirt look worse than none.

**What went wrong on the boards measured here was the tones, not the count.** Of 259 sampled surface patterns
on 77 boards, half mix two blocks more than 60 RGB apart in one field — grass speckled with gravel, sand with
coarse dirt — and that is the mottle a player sees. A `TerrainPalette` family is a colour bucket rather than
a recipe: it offers blocks that average to one colour, planks beside dirt and wool beside clay, so it is where
a list starts and never the list.

**A noisy block is capped, not banned.** Cobblestone in stony ground stays at or under 30%. Sandstone in sand
stays in small patches, never large splotches. How loud a block is shows only on the ground, which is why a
swatch cannot settle it.

### A ground of several tones is a main set with other sets inset in it

**One set is the ground and the others are patches contained inside it.** A badlands floor is an orange
ground — red sand, red sandstone, orange stained clay — holding patches of dirt and coarse dirt, and patches
of hardened clay. Each is a set in its own right, so an orange patch is never one bare block against a bare
dirt one. The same six blocks thrown into one field are a mess.

**Which set sits inside which is part of the recipe.** Dirt at the centre, a ring of hardened clay round it and
orange outside works; hardened clay at the centre of a ring of dirt does not. Hardened clay may also stand in
the orange on its own, away from the dirt. Texturing is how the blocks are combined as much as which blocks
are chosen.

**A noise's stop list is how the nesting is written.** A `noise` is a ramp over a smooth field and each stop
takes an equal band of the field's value, so stops next to each other in the list are next to each other on
the ground. A stop may itself be a pattern, so each set is a nested `cell` or `noise` of its own blocks. Of
726 patterns on 77 boards, 32 nest one inside another, on 4 boards.

**Put the main set in the middle of the list and the patches at its ends.** The field is bell-shaped, so the
middle stops take most of the ground and join into one, while the end stops come out as separate patches.
Measured on the studio's own noise: two stops split about 53/47 and both form one maze, with no ground and no
patches; `[P, G, G]` gives 26% patches of `P`; `[P, G, G, Q]` gives 16% and 12% patches that never touch.

**The order of the ends says which patch sits inside which.** `[dirt, hardened clay, orange, orange]` rings
the dirt patches with clay inside the orange, which works. `[hardened clay, dirt, orange, orange]` puts clay
at the centre of a dirt ring, which does not. `[hardened clay, orange, orange, dirt]` keeps the two apart —
rendered, no clay block touched a dirt one.

**Even shares are a `cell`, not a `noise`.** A noise's middle stop always takes about half the ground, so no
stop list gives a third each. A `cell` gives each palette entry an equal share at any cell size — a third each
of three, a quarter each of four — and is what a path or a built floor is laid with.

### Grain

**Random ground noise is small patches, about five blocks across.** A finer speckle, about three blocks
across, reads as too random. On the studio's noise a stop at the end of `[P, G, G]` makes five-block patches
at `scale` 2 and seven-block ones at 3; the committed themes sit at 6 to 8, which makes patches of 17 blocks
and more — the large random splotches the boards were complained about for.

**A large patch is a feature, and a feature is a shape.** Worn ground is a shallow pit sunk a block into the
meadow, drawn as a shape or a stroke with its own theme, and painted dirt and coarse dirt half and half; a rim
of dirt round it is fine. Medium and large patches are right only where they are intentional like that, and
never as random terrain noise.

**Splotches beat patterns, and a splotch is a shape.** A theme is stated **on a shape** (`TP10`: map default ›
shape, winner takes all), so the brush an author reaches for is an `addShapes` polygon with a `theme` of its
own — a patch of bare dirt worn into a meadow, a sandy shelf at the water, a scorched ring. Ten of those over
one ground is a landscape somebody made.

The same patch sampled from a pattern instead is a board that is a third dirt *everywhere*, including the places dirt
has no reason to be. If the answer to *why is it here* is "the noise put it there", it is not an answer.

**A voronoi is never ground.** It draws a diagram — a grid of lines with cells reading off it — and there is
no landscape that looks like that. It belongs in the **fill**, where it is the body of the rock nobody sees
until a wall is cut, and it is made of **stone**. A voronoi whose bands are dirt and whose middle is grass is
the worst of both: a network of dirt lines nothing in nature draws. On these boards **44 of 50 voronois are on
the surface** and **none is in the fill**.

**Look at a finish before it is committed.** `POST /api/terrain/material-preview` renders one material and
`POST /api/terrain/theme-preview` the whole finish, in five views — `section`, `rim`, `surface`, `wall`,
`fill` — under `?format=png&view=…&scale=…`.

Without `format=png` it answers every view at once as JSON and `view` does nothing, which reads exactly like a
broken knob and is not one.

Neither preview builds a world, and neither can tell you what a theme sits **next to**: the sample terrain is
grey stone, so a grey theme reads as one mass there and may be perfectly legible on a board of grass.

### Where two grounds meet

**A hue jump is a boundary, never a noise.** Red sand in sand, light grey stained clay in red sand, gravel in
sand and white stained clay in snow all fail inside one field. Two such grounds meet as separate areas — a
plateau of red sand beside one of sand — and never scattered through each other, which is what the big
destroy boards with the lake did with sand in grass.

**On the flat, the edge between two grounds is ragged or blended, never banded.** A ragged edge and a
speckled transition a few blocks wide both work between grass and sand. A strip of a third material laid
between them does not.

**Rock showing through grass, sand or snow belongs to the slope.** Stone, gravel and andesite in grass read as
rock faces coming through; a shore is sand, then stone where it steepens; a snowfield shows stone only where
the ground is too steep to have held snow. All three are the slope band's job rather than a flat-ground
noise. Stone in a meadow is an author's choice, not a fault.

**The grass band on the slope axis ends too early on most boards.** Of 65 slope stacks whose first band is
grass, on 58 boards, the grass ends at a median of 18°, and 20 of them end it at 12° or less. Grass that stops
that early leaves dirt showing along gentle edges that read as unintended, so the cut is tuned to the terrain
with `incline`, and is usually higher.

**Under a meadow the section is turf, two courses of dirt, then stone.** The soil courses are dirt and coarse
dirt; the stone is stone and andesite with cobblestone as its accent. A face that is dirt all the way down, or
cobblestone alone, does not read as ground.

### What a set is made of

| ground | the set | not |
|---|---|---|
| stony ground | stone and andesite as the base, cobblestone mixed in up to 30% | cobblestone as the base |
| meadow | grass; worn ground is dirt and coarse dirt together, as one area | coarse dirt or dirt alone as specks |
| desert | sand and sandstone, and more of the sand family where the ground wants detail; end stone only where sandstone is there too; grass, under a biome that suits it | red sand, gravel, end stone alone |
| badlands | an orange ground (red sand, red sandstone, orange stained clay) with inset patches of dirt and coarse dirt and of hardened clay; grass, under a biome that suits it | yellow sandstone, red stained clay, light grey stained clay |
| mesa cliff | several bands of hardened and stained clay; vanilla banding is colourful but not wrong, red included as a thin band | two colours as bands |
| snowfield | snow, or snow with packed ice | white stained clay; stone on the flat |
| ash field | grey and black stained clay — the safe answer, with room left for a third set inset in it: dirt, or grass under a biome that suits it | — |

**Stained clay is ground only inside a set of its own tone.** Orange stained clay belongs in a red-sand ground
and grey with black makes an ash field; white stained clay beside snow and light grey stained clay on red
sand do not work. Wool and glass stay shade rows — a stated colour, never terrain.

**Snow with quartz is a surface and never a wall.** Snow lies on the ground and nowhere else, so the pair
reads only as the top course, and even there it is not a pairing to reach for.

**Red stained clay is for abstract maps.** Nothing in nature is that red, so as ground or as a boulder it
reads as a stylised board and fails on any other.

**Strata follow the ground.** A `layered` stack on the `height` axis lays its beds at fixed world heights, so
on land that tilts they run across the slope and a hill's upper beds never reach the low ground. `follow: 100`
measures `from` below the ground averaged `reach` cells either side instead (16 unstated, 1–64), so each bed
rises and falls with the land. A reach of about sixteen keeps the land's broad tilt and lets a crag cut through
the beds, which is what a mesa looks like; a reach of a few cells lays them along every bump and reads as paint.

**The strata are the fill, the wall and the steepest slope band at once.** The `wall` bucket is only the
exposed riser below the top course: a one-block step on a hill belongs to the surface, and the side of a cut
or a tunnel is the fill. A stack stated on the wall alone therefore shows on the tallest drops and nowhere
else, and a culvert cut through that ground shows plain fill on its walls. Stating the same stack as the
theme's `fill` and as the steepest band of its `slope` stack makes every face the board shows cut one set of
beds.

### Themes and places

**Three themes is a map.** A theme is a *place* — the moor, the works, the shore — and a board has two or
three of them. Giving every piece of the plan its own theme is not variety, it is the plan leaking into the
paint: sixteen boards here carry three themes, but eleven carry five, seven carry six, and five carry between
sixteen and twenty-four, the worst of them carrying **twenty-four**.

**Steps share one theme, and it is not the theme of what they join.** A flight of steps is *made* — it is the
one part of a landscape a person built — so it reads as stone, and it reads as the same stone the whole way
up. The grassy shelf at the top and the sandy floor at the bottom may each have their own theme; the stair
between them having a third is what turns a board into a swatch book.

**A landscape board is one theme, a relief and a handful of patches.** Every destroy board is a landscape
board. Author a **simple plan with few pieces**, put the shape of the ground into the **relief** rather than
into the piece list, paint the whole thing one ground, and then put the variation in where you *want* it. A
raised shelf carrying a city may have a theme of its own — but a city is not noise either, so that theme is
materials laid in courses, not a field sampled over them.

**A building is never the ground it stands on.** A house is a thing somebody built on a landscape and it has
to read as one from across the map, which means its walls are not in the tone family under its feet. A stone
house on stone can be made to work and is a hard thing to get right; it is not the one to attempt. **9 of the
50 buildings** here are walled in the ground's own family, one board putting three grey-stone houses on grey
stone.

Name three families out loud before painting: which is ground, which is built, which is the
accent. An accent that appears once is not an accent, and an ore block is never a building material.

**A tunnel is cut through one rock.** Its floor, its walls and its ceiling read as the rock the ground is
made of, never as the surface on top: sand on a desert tunnel's floor or ash on an ash field's is the sky's
ground brought indoors. The studio paints ground that another layer's wall stands on as rock (`TP25`), but a
tunnel's open floor is still the ground's own top course, so it takes a shape of its own with the rock or a
path set.

### What is laid rather than grown

**A path is solid, and it is three blocks of one tone laid a third each.** A `worn` or `rough` band reads as
litter rather than as a way somebody walks: the style to state is `solid`, and the pave is a `cell` of three
blocks a reader cannot quite tell apart by colour. **Dirt, coarse dirt and spruce planks** is one where the
ground is soft and **gravel, andesite and cobblestone** one where it is hard; a board may find its own three.

**A path goes everywhere the players go.** A board is walked from each spawn to the front, to the other side
and to every wool room, so one thin line from the spawn to the front says only one of those walks was thought
of. A path is wide enough to read as a way rather than a trail.

**A path wanders between its points.** A stroke through a handful of points runs nearly straight between them:
across 266 strokes on the boards here the median is four points, and the longest straight run is 12 blocks at
the median and 18 at the 90th percentile, which reads as ruled. A stroke's `wander` (0–8 blocks) bends it from
side to side every `wanderLength` blocks of line (16 unstated, 4–64) and eases to nothing at both ends, so the
path still arrives at the door it was drawn to. Three blocks over a bend of about fourteen reads as walked, and
two where a lane leaves little room either side.

**A path that wanders moves the ground it claims.** A claiming stroke keeps a tree 3 blocks and a boulder 2
off the line it is paved along, and that line is the bent one, so a prop that cleared a straight path can be
declined once the path wanders (`DR-ROAD`). Read the pre-flight again after adding wander; the census names
the cell, and a block or two of move clears it.

**A warm path is granite with brick.** Granite and polished granite carry it, with brick in strips; hardened
clay can stand in for the brick but is flat. Granite with hardened clay belongs in a path and nowhere else. A
path is also a claim about circulation, so one that ends nowhere, or that runs *through* a building rather
than to its door, says the board was assembled rather than drawn.

**A built floor is four blocks of one tone, a quarter each in a `cell` of about three.** Stone bricks,
polished andesite, andesite and stone is one such floor and reads as one paved ground with depth; a board whose
buildings are warm lays its floor from its own family by the same rule. Stone bricks alone are dead; stone
bricks with a little cracked stone brick look out of place; two blocks collide.

**Mossy cobblestone and cracked or mossy stone bricks are not ground.** Their veins and cracks are noise
wherever they meet terrain and read as damage, which is a statement about age that ground does not make.
Mossy cracked stone brick belongs, if anywhere, faintly in a wall.

**A boulder is one rock.** Stone and andesite, with cobblestone if it wants grain, reads as rock from any
distance. Mossy cobblestone goes in only as rare specks beside cobblestone and andesite, and that is the
limit. Two different rocks in one boulder — granite beside stone — read as two geological features, and a
boulder in the ground's own set is a lump.

**The same boulder on every board is a default, not a rock.** The library holds several forms and sizes, and
five boards carrying one recipe between them is the first one that came to hand. A board's rock is chosen for
that board, within the rule above.

**A stylised stone is carried by one hue.** A rock of prismarine, mossy cobblestone and emerald ore works
because all three carry the same green, and it is a deliberate choice for a board that wants it rather than a
default.

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

## Where a tree stands, and how many

**A possible placement is not a required one.** Anything that answers where a prop *may* stand — a search
over the board, a legal field, a list of sites — answers legality and says nothing about composition, and
planting every site it offers is how a board of ten-block corridors comes out as a forest. Ask how many the
piece wants first, then which of the legal places those are.

**To the outside of a piece, never down its middle.** With no road on it a player still runs down the centre
of a corridor, so a line of trees along the rim reads as an alley and the same trees in the middle read as an
obstacle course. Two in front of a hole, three along a road, one in a corner: a piece takes a handful, not a
field.

**Nothing where a player arrives, and nothing on the brink they leave from.** A bridger who crosses a void
and lands in three trees has been handed an obstacle the arrangement never asked for, and a tree two blocks
off a bridging edge crowds the edge itself. Both belong on the far side of the piece.

**Nothing on the approach in front of a wall, and nothing on a contested middle.** The ground in front of a
defensive wall is fought over and wants to be read at a glance, and a neutral middle is where a structure
goes rather than scenery. A deck on four legs is worth more there than any number of oaks.

**The studio's own rules are narrower than any search, so check a site against the dressing pass.** What it
asks is ground under the trunk, three blocks clear of paving, unclaimed, and not kept clear; a search that
also demands eight level neighbours refuses every rim cell on the board, and the rim is often the only place
a road leaves. A search is a way of proposing sites nobody has to think about — its silence is conservatism,
not a refusal.

**Two species a board, and never three.** A dense oak, a birch and a willow on one board read as three woods
pushed together rather than as one place, where an oak with a tiny spruce among it is one wood with an accent
in it — which is what the pair is for. A third species is the one that stops being scenery and starts being a
catalogue (author).

**A board's trees belong to its climate, and pine and spruce belong to a cold one.** `large-pine-1` standing
on savanna — warm, sandy ground — is the measured case, and no amount of placement repairs a
species being wrong for the ground it is on.

**What a tree *is* is what `corpus/README.md` says, not what its blocks are.** The library names every tree by
it — `large-pine`, `tall-spruce`, `willow`: `r2` and `r3` are pines built of dark-oak log under birch and spruce leaves, `r7` is a tall spruce of acacia
log and birch leaves, and `r4` is a tiny spruce of the same two blocks. Reading the log is how a spruce ends
up on a savanna.

**A tree holds the disc its crown covers, and the pass says so.** `DR-CLAIM` refuses a trunk inside another
tree's crown, at `Decorator.CanopyRadius` — the tree's own farthest leaf, measured rather than taken from its
species — so two trees stand at least their two crowns apart. Crowns that interpenetrate read as one mass of
foliage, and `r11`'s dense oaks are the worst of it because their crowns are the widest in the corpus.

## What a building is made of

The two sections above are what the ground is made of. This is the other half, and it is shorter, because a
building is a short list of decisions and a shorter list of things not to do.

**The list is the author's, and the studio names nearly all of it.** Each ruling below that names a rule id is a
complaint when a style is stored or saved to the library: an aesthetic verdict the store reports and does not
block on. The one it does not name is checked nowhere.

**No footing.** `Foundation.Footing` is null by default and that is the answer rather than an omission: a footing
is the course ringing the plate one block proud, and round a house it reads as a rim rather than as masonry the
building stands on. The studio complains of one of any block round a plate of any depth (`HS7`).

**No shed, and no shed roof.** `RoofForm` offers six — `gable`, `flat`, `hip`, `gambrel`, `shed`, `saltbox` — and
one of them is not for a map. The studio complains of it on a house, on a wing that names its own roof and on a
porch canopy (`HS14`); a porch that names no roof wears a gable.

**A porch roof may be one block.** A canopy takes the house roof's body, with the verge along its ridge where the
roof is capped; where that trim stands out, the `canopy` part lays the whole porch roof in one block.

**A log is a post or a beam, and a wall is neither.** Posts at the corners are what make a house read as
framed, which is what every hand-built house on the corpus does. Beams run out past those corners where two
storeys meet — and a beam has to be the end of something, so the wall under it carries a course of **laid**
log. A beam over plain infill is a beam ending in nothing.

**A log in a building is cut timber, so it shows its sawn end.** Posts stand upright, and beams and laid
courses lie along their run, which is what puts the rings at the end of every beam — the signature look of a
timbered house. The log with bark on all six faces is a tree's: a tree is whole rather than felled, and built
into a wall it reads as a trunk.

**A checker in the same log as the posts is one mass.** Where a wall wants a checker it wants a *different*
log; where it does not, the posts are already doing that work. The studio complains of the checker (`HS15`).

**Corner beams need log posts and a laid course at their level.** Where a storey seam lays beam ends, the course
they come out of is a laid log and the corners beside them are log posts; the studio complains of either missing
(`HS9`, `HS11`). Log posts with no beam ends need neither.

**A laid log is never the bottom course.** It belongs at the top of a storey, where beam ends come out of it; at
the foot of the wall it is a log lying round the footprint, and the studio complains of it there (`HS13`).

**The gable is never the overhang's block.** The verge borders the roof at the gable end, and in the gable's own
block it borders nothing. The author's pairing is spruce planks under a dark oak overhang, and the studio
complains of the same block on both (`HS12`).

**No birch log in a building.** Not as a post, a laid course, a beam or a band; birch planks, stairs and slabs
are allowed. This is the ruling the studio does not check.

**A wall is never the ground's skin.** Grass, podzol, mycelium and farmland are the top of the ground and never a
wall or a gable (`HS16`). Sand, gravel and even dirt can work in a wall.

**No snow or ice in a building.** Snow, a snow layer, ice and packed ice are weather, never a wall, a gable or a
roof (`HS17`). White blocks are not the fault: white clay, white wool and quartz are walls.

**A storey over the stilts names its floor.** A stilt house's plate is air, and a storey naming no deck stands on
that air; the studio complains of a storey above the ground with nothing under it (`HS18`).

**A library style is named for what it is.** Its name is describing words then the kind of building —
`brick-roofed-stone-cottage`, `oak-stilt-house` — every word from the two lists `GET /api/room-styles/name-words`
answers (`HS19`). A board's name, a role, an occupation or a place says where a style was used, not what it is.

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

### A terraced hillside

**A terraced slope is polygons stacked against each other at different levels, never rectangles in a row.**
Each terrace is a field somebody levelled: its outline is angled, its neighbours share its edges, and it stands
two or three blocks over the one in front of it. A row of square terraces reads as plinths and a grass slope
cut into three-block steps reads as nothing at all. (The author's ruling.)

**A terrace is a little out of level.** It tilts a block or so across its width, so one dips toward a corner
and the next leans the other way, and two terraces of one row a block apart merge into each other with no wall
between them. The tilt is the polygon's vertex heights, read off one plane per terrace.

**Every face a terrace stands on is a wall somebody built to hold it, and its top is a low wall.** The face is
cobbled — dry stone, cobblestone with andesite — where the natural faces round it stay the board's own rock,
and along the terrace's front runs a wall one course high and a little crumbled, following the ground's tilt.
A wall several blocks tall, or one that stands as posts down the face, is the fault this rules out.

**A path crosses a face by a flight set into a notch in the upper terrace**, as above, and the wall stops
short of it on both sides. `GENERATION-NOTES.md`, *Shapes*, carries how the rows, the tilt and the wall are
drawn so that none of them spills.

