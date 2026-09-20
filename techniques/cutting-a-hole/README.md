# Cutting a hole

**A subtract is the only instrument that removes ground, and the only one whose own height is never read.**
Relief moves a surface, a shape adds one, a push lifts one — a subtract deletes the column and leaves the
void. Beside it sits the override add, the one add that may stand over a cut and the one that takes a column
it is too short to have earned. Open the card in the studio as `technique-cutting-a-hole`, or run `build.py`.

Seven islands, each 68 × 52 at surface 9, so the only thing that differs between two panels is the
instrument drawn on it.

| Panel | States | What the column reads | Why |
|---|---|---|---|
| `a-hole` | one `subtract` through the island | `0 solid block(s)` | a cut goes to the void, not to a depth |
| `height-not-read` | the same footprint at `base_height` 1 and at 40 | both `0 solid block(s)` | a subtract has no height to state |
| `a-lid` | an override add whose `floor` is **above** the cut's | 3 blocks at y6–y8, **nothing under them** | a deck over a void |
| `a-room` | a floor under a stated void, a ceiling over it | y0–y2, five courses of air, y8–y9 | a room, and it costs a second layer |
| `override-wins` | an override add 4 courses tall on ground 9 tall | 4 blocks | the privileged set wins the column whatever its height |
| `the-taller-wins` | two override adds, 14 courses and 4 | 14 blocks | inside that set the taller wins and order decides nothing |
| `a-declared-void` | the polygon subtract a compile writes | `0 solid block(s)` | this is how a composed board states its gaps |

## A cut has no depth, and that is the whole difference from relief

**A subtract deletes every column its outline covers, and its own `floor` and `base_height` are not read.**
`height-not-read` cuts the same footprint twice, once one course tall and once forty, and `holes.txt` reads
both as void: 36 columns of it across the island, 18 to a cut. A one-block subtract carves exactly as deep
as a two-hundred-block one.

**So a hole is never a relief question.** A mark moves a surface and cannot take it away; a channel in front
of an objective is one subtract rectangle drawn at the width the gap wants, and a dip in the ground is
`techniques/hollows`. The two instruments do not overlap anywhere.

**A void answers no height at all.** `column` says `0 solid block(s)` and names nothing; `transect` prints
` ·` where its `ground` is null. A hole therefore cannot be found in a surface figure — a read that averages
or interpolates heights will step straight over it, which is what makes `transect` the read that finds one
and a render the read that does not.

## What may stand over a cut, and what the floor decides

**An override add whose floor stands above the subtract's is a deck, and it records nothing beneath itself.**
`a-lid` reads three blocks at y6, y7 and y8 with the column empty under them: a layer holds one span a
column, so the span simply moves up and the drop stays open. That is the cheapest roofed void there is.

**A floor and a ceiling either side of a stated void is a room, and it costs a second layer.** `a-room` gives
its subtract the five courses the void is meant to be, stops the floor's top at the cut's floor and starts
the ceiling at the cut's top — which is exactly what `SK13` asks for. Drawn on one layer the two do not both
survive: one span a column means the taller of them takes it, and the floor is simply gone. The ceiling here
is on a `made` layer of its own, and `techniques/stacking-layers` is where that rule is worked.

**The floor is the whole of the gate's test.** `refusals.txt` puts four adds over one cut: at the cut's own
floor an override add is a refill, and one course higher the same shape is a bridge that passes in silence.
Nothing about the shape changed but its `floor`.

## `SK13` answers at two volumes, and only one of them stops anything

**A fill complains at the store and refuses at the finish.** `PUT …/sketch` answers **200** and keeps the
shape, naming the fault as a `complaint`; `POST …/sketch/finish` answers **422** with the same sentence at
severity `refusal` and builds nothing. A board can therefore sit stored for a long time carrying a fault
that only the finish says out loud.

**A plain add over a cut is the quieter half and is not a refusal at all.** Without `override` the shape
loses to the subtract on its own layer whatever order the two are written in, so it complains at both calls,
the board builds, and that shape is simply absent from the world — visible on the canvas, nowhere in the map.

**A subtract reaches only the layer it is on, and the gate does not.** An add on a second layer at the cut's
floor is refused exactly as one beside it is: the negative space is the board's statement, and `SK13` reads
it across the stack.

## An override add wins the column, and that is not the same as owning it

**The privileged set is resolved after the ordinary adds, so an override add takes a column it is shorter
than.** `override-wins` is four courses standing on ground nine courses tall, and the column reads four
blocks: the ground under it is not buried, it is gone. The resolution is
`((adds − subtracts) ∪ override-adds) − override-subtracts`.

**Inside that set the taller surface wins and document order decides nothing.** `the-taller-wins` writes the
14-course plate first and the 4-course plate second, and the column reads 14.

**Winning the column is not winning the paint.** `override-wins` reads grass over dirt rather than the
material the plate states, because paint is owned by the tallest shape covering the cell and the island's own
9-course ground is still taller than the 4-course plate. The plate holds the geometry and the ground holds
the surface. `techniques/painting-a-patch` is where that ownership test is worked.

## What a compile cuts with

**A plan has no subtract of its own, and the compiler supplies one.** A hole in a plan is a gap no piece
covers; `PlanVoids.Declare` names every such gap a `void-N` buffer on every compile, drawn or not, and each
one comes back in the layout as a polygon subtract called `void-N-cut`. `compiled.txt` posts a composed plan
to `POST /api/plan/compile` and reads back six adds and two cuts.

**A compiled cut states four of its twenty-nine fields.** `id`, `type`, `operation`, `vertices` — and no
`floor` and no `base_height`, because there is nothing for them to say. The compiler writes the same fact
`height-not-read` measures out of the built world.

**So the void of a composed board is an ordinary shape and is edited like one.**
`techniques/taking-over-a-composed-board` redraws one, and its vertices move the way any polygon's do.

## The recipe

- **use a subtract for a hole and relief for a dip.** They are not two strengths of one instrument: one
  removes the column and one moves its top.
- **do not state a height on a cut.** Nothing reads it. A `base_height` on a subtract is a note to the
  next reader that will be believed and is not true.
- **look for a hole with `transect` or `column`, never with a surface number.** A void has no height, so
  anything that answers in heights has already lost it.
- **raise the `floor` to bridge, keep it to refill.** An override add one course above the cut spans it and
  says nothing; at the cut's own floor it is `SK13` at the finish.
- **a floor and a ceiling are two layers.** One layer holds one span a column, so the two halves of a room
  cannot share one however correctly their courses are stated.
- **run the finish before believing the store.** A 200 from `PUT …/sketch` is not a board that builds.
- **an override add wins the column and not the paint.** Use it where the plate *is* the new ground, and
  check what painted it rather than assuming its `material` landed.

## Limits

**Nothing here is underground space as a place.** The lid and the room are the mechanism, not a cellar with
a way in: an opening is a gap between shapes rather than a subtract, and
`techniques/sculpture-with-layers` is where that is worked.

**The paint is incidental and deliberately not the lesson.** Two panels carry a `material` so the stone
reads apart from the ground; which shape owns a cell's surface is `techniques/painting-a-patch`.

**No relief on any panel.** A cut interacts with a solved field, and that interaction belongs to
`techniques/hollows` and `techniques/made-ground`, which both have ground to solve.

## What checks it

- `columns.txt` — two columns a panel: the one the instrument acted on, and plain island beside it.
- `holes.txt` — every island read across itself, where a void prints as ` ·` and a cut is a gap in the row.
- `refusals.txt` — four adds over one cut, with what `PUT` and what `finish` each said about it.
- `compiled.txt` — a composed plan through `POST /api/plan/compile`, and the `void-1-cut` it answered with,
  verbatim.
- `cutting-a-hole.layout.json` — what `build.py` writes: 18 shapes on the ground layer and one made layer
  for the room's ceiling.

Renders: `iso.png`, the seven islands together; `a-hole.png`, `height-not-read.png`, `a-lid.png`,
`a-room.png` and `the-taller-wins.png`, each close enough to see what the instrument left.
