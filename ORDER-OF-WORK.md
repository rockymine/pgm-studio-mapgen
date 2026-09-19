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

**The gamemode decides the board's shape, not its rules.** A destroy board is a **lane**: on a square every
goal is equidistant from both spawns and the ratio that gates it flattens. A capture board is about **a third
land**, and its arrangement — a hub, a spawn hung off it, wool approaches, a frontline, a mid band with
stepping stones — is hard to invent and easy to get wrong, so a capture board may start from a composed plan
and be taken over.

**State the extent, the aspect and the two lines before any shape exists.** Where each spawn sits, where each
objective sits, and the two routes between them. Five numbers and two lines are the board; everything after
them is detail. A goal's distance from its own spawn is solvable with arithmetic at this point, and a board
whose size cannot satisfy it will not be rescued downstream.

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

**The studio describes itself, and four reads answer every capability question.** They are generated from
the routes and the types, so they are current by construction where a document is not:

- `GET /api/openapi/v1.json` — every route, its request, its answer and the failure codes it declares;
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

**`techniques/` is one card per instrument**, each holding its variants side by side in one world with the
reads that prove them. Read the card nearest what is being built.

**The `pgm-board` skill is the lookup from a question to the read that answers it**, and the order it states
is the order the *tools* are run in. This page is the order the *decisions* are made in, and they are not the
same list.
