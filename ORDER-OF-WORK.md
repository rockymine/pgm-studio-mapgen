# The order a board is decided in

This is the whole of what has to be in mind before the first request. It is not an explanation of any
instrument — it says **when** each decision is made and **what cannot be taken back** once the next one is
made on top of it. Everything it names is answered in full somewhere else, and the last section says where.

Nine decisions, in order. A board goes wrong by making one of them out of order far more often than by
making one of them badly.

---

## 1. What the board is

**Write the board's identity in one sentence before anything else.** What it is for, what kind of place it
is, and what a player remembers about it. If the sentence cannot be written the board is not ready, and no
amount of terrain will supply it later.

**A monument or a core never stands at the end of a lane.** Ending a lane is what a wool does, and a destroy or
core board that copies it comes out as a straight box with a spawn glued to each end and the goal partway along.
That box is the one shape ruled out, and nearly every other shape is open.

**A destroy or core board can be any arrangement of land in the void.** One long island with a side island
holding the objective; a peninsula of several islands; one large island of abstract shapes with smaller islands
between; a large flat island where built ground and grown ground take turns; floating islands. Choose the
arrangement in the identity sentence, because it is what a player remembers the board by.

**A destroy spawn stands in the land at its back, not on a box behind it.** A spawn piece hung off the back of
the main island across a gap is attached to the board without belonging to it. Seat the spawn house on the
ground — on a hill, beside a mountain or a stack of rock, near a mine — up to ten blocks into the land, and it is
still at the back.

**The boards built here seat the spawn on a bare pad at the edge.** On the corpus layouts the author points to, a spawn
has a median 20 blocks of its own land behind it and ground 8 blocks above it within 20; on the boards built
here, 10 and none, and 29% of them have neither a rise nor a tree within 20 blocks
(`pgm-studio/docs/world-scan/destroy-layouts.md`).

**The objective stands in front of the spawn and off to one side.** A defender has to see it, and it is rarely
straight ahead: the goals of the corpus destroy maps sit a median 42° off the line from the spawn to the enemy
spawn, and the boards built here a median 28°. Two goals are an east and a west, or a front and a back near the
spawn. `pgm-studio/docs/gameplay/approaches.md` lists the destroy boards worth reading and what each shows.

**An arrangement can be drawn from a rule rather than invented.** Points sampled at random over the area, a
noise field cut at a level, or a set of about twenty points joined by a tour that annealing solves each give
islands no hand would draw. Take the land the rule gives, then decide where the spawns and goals stand on it.

**A capture board is about a third land, and its arrangement is the hard one to invent.** A hub, a spawn hung
off it, wool approaches at the ends of their lanes, a frontline and a mid band with stepping stones are easy to
get wrong, so a capture board may start from a composed plan and be taken over.

**State the land, the spawns, the objectives and the routes before any detail.** Where the islands lie, where
each spawn and each objective sits, and how a player walks from one to the next. That is the board; everything
after it is detail.

**A goal's position is a walk, and the studio gates it.** The walk from a monument or core to the nearest enemy
spawn is 3 to 4 times the walk to its own (`GO1`), its own spawn is 40 to 90 blocks of walk away (`GO4`), and
an enemy goal 85 to 150 (`GO3`). A route that bends round an island or crosses between two meets all three as
well as a straight one does, so a refusal moves the goal or a spawn, never the board back into a box.

**Choose the biome now, with the three tone families.** A tinted block takes its colour from the chunk's
biome byte and nothing else on a board does, so the biome is a palette decision rather than a line added at
the end — a snowfield on a summer biome has a meadow running through it. The families are which is the
ground, which is built, which is the accent.

## 2. The plan

**The plan states the board's arrangement and nothing else** — which ground is where, at what height, next to
what. It is not the board's shape. Two shapes it may take: three or four distinct height zones as pieces, or
one rectangle with every landform authored downstream.

**A piece earns its place by stating something the arrangement needs** — a height a lane climbs, a room a
building is seated in, a footprint the symmetry fans. A piece that exists so a theme can be hung on it should
have been a shape scope, and a plan cut up that way produces a board whose look was decided by how it
happened to be divided.

**A hole is made by arrangement.** Pieces ring a gap and no piece covers it. No relief mark of any kind cuts
one, and the instrument that cuts ground away is downstream, so a board that needs holes is arranged for them
here or not at all.

**Read the plan as a grid before posting it.** Most of what goes wrong with a plan is a relation between two
rectangles — a landform wider than the window that reaches it, a wall on the only throat, a room whose door
opens onto its own apron — and no render of a built world can show that, because by then they are terrain.

## 3. The ground

**The relief is decided immediately after the plan and cannot be added later.** A board authored flat is a
board whose variation has to come from shapes for the rest of its life. Budget for the shape of the ground
here, in the same breath as the arrangement.

**A mark is a constraint and a push is a landform, and the two are not interchangeable.** A mark states that
the ground *is* this height, honoured exactly with no falloff — so it pins a floor, a shelf, a pan, an apron.
A push lifts the solved surface inside a drawn ring and is the only thing that builds a hill. Asking one to
do the other's job is the single most expensive mistake available at this stage.

**What is not written is where the design happens.** Pinning every region because it should be about that
height leaves the solver nothing to solve, and a board with a mark on every region is a table with bumps on
it however tall the bumps are. Pin the ground a player stands on and leave the flanks alone.

**Sketch the relief more than one way before settling it.** The same plan under three or four reliefs, driven
unpainted and looked at side by side, turns a judgement about ground into a choice between built alternatives,
and the relief that ships takes what each did well. It is the one decision here that cannot be added later, so
it is the one worth building more than once.

## 4. The shapes

**A shape is drawn once and reshaped one point at a time.** Moving, inserting and removing a vertex each
leave every other point exactly where it was drawn, which is the whole property: a board's shapes abut, and a
transform that drags a ring's other points opens ground between two that were flush.

**Never reach for a second shape to enlarge the first or to eat into it.** That is the move that produces a
board nobody can read, and every case it is reached for has its own instrument.

**A shape says how its top is decided, or how it takes part in the relief — never both.** The two fields are
alternatives: one puts the shape *out* of the field, the other says how a shape that is part of the ground
takes part in the solve. Stating both writes a field that binds and is never consulted.

## 5. The storeys

**A board is one storey unless a decision here makes it more,** and that decision belongs before the paint.
A layer is a slab keeping one span per column, so a cell may be on several and the air between them is the
feature — a hall under a deck, an undercroft, a viaduct over a street.

**Everything downstream of a stacked cell reads one number: the top.** A placement climbs onto the upper
layer by itself, ground under a slab is not dressed, and a read that projects to one height per column cannot
see the storey beneath. A placement that means a lower storey names it.

## 6. The paint

**Construction comes before dressing, and a bad construction cannot be dressed out of.** If the ground is
wrong here, stop and fix the ground.

**Three themes is a map.** A theme is a *place* — the moor, the works, the shore — and a board has two or
three of them. Giving every piece its own theme is the plan leaking into the paint.

**Finish the ground by its angle, not by its height.** A theme hung on plan pieces or on height bands paints
a board flat from above however much relief is under it, because nothing in the geometry tells a hillside
from a meadow unless the band axis is the slope. Read the board's angles before choosing where the bands cut.

**A ground is a set of one tone, not a block.** Two or three blocks close in colour and different in texture
make one ground, and a ground of several tones is one main set with the others inset in it as patches.
`WHAT-A-BOARD-IS-MADE-OF.md` carries the sets and how a stop list writes them.

**A patch of different ground is a shape carrying its own theme**, and ten of those over one ground is a
landscape somebody made. A field sampled over the whole board is a roll of the dice, and *the noise put it
there* is not an answer to *why is it here*.

## 7. The dressing

**Nothing is scattered.** Every prop is placed because there is an answer to why here, and bare ground chosen
is better than dressing that was not.

**A building is never the ground it stands on.** A house has to read as a built thing from across the map,
which means its walls are not in the tone family under its feet.

**A path is a claim about circulation.** One that ends nowhere, or runs through a building rather than to its
door, says the board was assembled rather than drawn.

## 8. Reading it back

**Every 2xx carries `warnings`, and a decline means a piece of what was posted is not in the world.** A
driver that reads only the status code is throwing away the half of the answer that says what the map became.

**Read the numbers before the pictures.** A picture answers whether a thing came out; a number answers
whether it is right. When two reads disagree, the column at a coordinate is the one that is not a projection.

## 9. The export

**Pre-flight before exporting.** It runs the export's own verdict at a fraction of its cost, per team, and
nothing refuses a run for skipping it.

**Two gates are heard for the first time at the export, after the whole world is built** — a goal standing
over void or inside a room, and a prop inside a goal's clearance, which is ten blocks about the anchor tested
against a prop's footprint plus its eaves and against every orbit image. Neither is predicted earlier, so
compute both before building rather than after.

---

## What cannot be taken back

Four decisions are not edits:

- **the relief**, because a flat board cannot be given ground afterwards;
- **the plan's division**, because the paint inherits it;
- **the biome**, because every tinted block on the board answers to it;
- **the board's size**, because the goal bands are arithmetic and a board too small cannot satisfy them.

Everything else can be changed by posting a different document.

## Where the detail is

**The studio describes itself, and five reads answer every capability question.** They are generated from
the routes and the types, so they are current by construction where a document is not:

- `GET /api/openapi/v1.json` — every route, its request, its answer and the failure codes it declares;
- `GET /api/glossary` — every word the rules and the studio use, defined once;
- `GET /api/rules` — every refusal the studio can raise, with what it means and how to fix it;
- `GET /api/rules/terms` — every measured number with its band and where the band came from;
- `GET /api/terrain/patterns` — the fourteen material kinds with their exact field names.

Read those rather than any document, including this one. A capability written up as missing is a claim about
the surface until it has been searched for by the name it would have, by the sentence describing what it
would do, and in the term list.

**`GENERATION-NOTES.md` is what none of them can say** — a fact about how two correct mechanisms interact, a
number no gate checks, a read-back that misleads. It is thirteen chapters in this same order, so open the one
for the stage being worked on rather than the file: *the board · the plan · a board somebody else arranged ·
the compile · relief · shapes · layers · painting · buildings · dressing · the export · reading it back ·
what an answer says*.

**`WHAT-A-BOARD-IS-MADE-OF.md` is the author's ruling on how a board should look**, and it is the one other
document read before authoring rather than at a question: what a board is painted with, what a building is
made of, how ground cover is stated, and how made ground meets grown ground.

**`techniques/` is one card per instrument**, each holding its variants side by side in one world with the
reads that prove them. Read the card nearest what is being built.

**The `pgm-board` skill is the lookup from a question to the read that answers it**, and the order it states
is the order the *tools* are run in. This page is the order the *decisions* are made in, and they are not the
same list.
