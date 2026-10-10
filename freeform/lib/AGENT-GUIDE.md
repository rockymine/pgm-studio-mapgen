# Building a freeform board with pgmvox

This guide is for an agent handed a freeform board to build with the library. It is about the plan and the sketch,
because that is where a board goes right or wrong; the library's modules are in `README.md`, and the order a
board's decisions are made in is in the repository's `ORDER-OF-WORK.md`.

## Read first

**Four documents before the first line of a plan.** This guide; the repository's `ORDER-OF-WORK.md`, for the
nine decisions and the four that cannot be taken back; `pgm-studio/docs/gameplay/approaches.md`, the author's
law on what an objective needs around it; and `README.md` here, for what the library already does.

**How a map is played is not in this repository.** `pgm-studio/docs/gameplay/match-flow.md` is the account of it,
read off recorded matches. A plan decided without it is decided on look alone.

## Where a board goes right or wrong

**A board is decided in its plan, and every expensive failure here was a plan failure.** The faults the
read-backs found after a build were the ones the plan never stated. A roof's eave hung over the void because the
plan held the walls and not the roof. Three places on a terrain board were cut off because the board had no plan
at all, only a list of coordinates.

**A plan that is checked catches what a build cannot cheaply fix.** A siege plan's checker reported two
objectives unreachable to the attackers before a block was placed, and the fix was moving a ladder in the plan.
A capture plan was revised four times with the author in seconds each, because the plan was one file and the
checker and sketch reran from it.

**Detail decided only while building is detail nobody reviewed.** Every board report that says "I had to decide
while building" names something that should have been a line in the plan: a lane width, a join between two
heights, where a build zone ends, which way a spawn faces.

## The plan

**The plan is data and prose, and the data is the source of truth.** A `plan.py` holds the board as the library
reads it: a `Raster` or a `Course`, its `Symmetry`, the objectives as `Objectives`, footprints as `Frame` cells,
routes as polylines. `PLAN.md` says why each of them is where it is. The generator, map.xml, the sketch and the
read-back all import `plan.py`, so the four cannot disagree.

**A plan is complete when it states five things, in this order.**

1. **The identity.** One sentence: what the board is for, what kind of place it is, what a player remembers.
2. **The arrangement.** The land, the spawns, the objectives and the routes between them, before any detail.
3. **The numbers.** Every height, width, gap and walk that decides play, each with its target.
4. **The places.** Each named place: what it is, why a player goes there or what it frames, and how they get there.
5. **The look, decided now.** The biome, the three tone families (ground, built, accent), and which material
   belongs to which role.

**A number in the plan carries its target.** "Lanes 12 to 16 wide", "the walk from a goal to the enemy spawn three
to four times the walk to its own", "every gap at most three". The checker measures each and prints it beside its
target. A number without a target is a description; it cannot fail, so it cannot catch anything.

**A plan states what the build will add and the plan does not show.** Scenery outside the play area, dressing,
facade patterns and terrain past the edges belong in a short section of their own. Saying it is what keeps an
unplanned detail from quietly changing play: a tree on a lane, a facade inset that is a foothold, a mountain a
player can climb out over.

**The first plan is kept when the plan changes.** Keep the earlier sketch with a version suffix and add a section
saying what changed and why. A reviewer reads the change, not only the result.

### What each mode's plan must carry

**Every mode's plan carries the objectives as objects.** Spawns, hills, flags, wools, monuments, cores, score
boxes and portals are `pgmvox.objectives`, made once in `plan.py` and mirrored by the plan's symmetry. Their
markers in the sketch, their XML and their read-back come from the same objects.

| Mode | The plan must state, measured |
|---|---|
| Destroy the monument, destroy the core | Where each goal stands: off the line between spawns, exposed, with composed ground round it. The walks from each goal to its own spawn and to the enemy's, against the studio's goal rules. The approaches to each goal and how they differ. Every layer under the surface, each with its own floor height and its own way in. |
| Capture the wool | Lane widths and the gaps between stepping stones. Each wool room: its doors, what may be built inside, who may enter. Each monument: where it stands and the walk to it. The build zones, the void and the kill height. |
| Attack and defend | Every stage: what opens it, where each team spawns in it, and that the defenders arrive first. Proof that no stage can be skipped: the walk with each stage's gates open and the later ones shut. |
| Payload | The track as PGM traces it, rail by rail, each leg's start and end. The ways above, below and around each leg. Each team's walk to the cart, leg by leg. |
| King of the hill | Each team's arrival at each hill, equal by symmetry or measured equal. What a holder sees from the hill and who can see them. |
| Arcade | The rule the board plays by, and the measurement that proves it: every jump clearable, nothing standable over the void, the fall model for each drop, hiding places out of sight. |

**A destroy board carries the most detail because it has the most freedom.** Nothing about its land is fixed by
the mode, so everything a player meets has to be decided. Give each goal its own approaches, each layer its own
reason to exist, and each place a reason a player goes there. A board whose plan is shorter than its list of
places has left the places undecided.

**A board whose detail is structure carries it in the plan as structure.** Where a board is remembered for how it
plays (a siege's stages, a payload's legs, a conquest's lines) the plan's detail is the thought process: who
arrives where first, what each team can see, what each choice of way costs. Write that as numbers with targets,
the same as a lane width.

### Terrain in the plan

**A board led by its terrain still has a plan.** Shape the heights in the plan phase: the landforms are cheap,
run in seconds, and need no world. Keep the list of landforms and their numbers in `plan.py` (or a `land.py` the
plan imports), and the places, spawns and objectives beside them.

**Check terrain before writing a block.** Turn the heights into a `Raster` (a kind by slope and by water) and run
the walk graph over it: every place reached from every spawn, by road if there are roads, without a drop past
three. The read-back walk on the built world then confirms what the plan already measured.

**Placement is a plan decision, made against the measured ground.** Seat a spawn, a village or a goal where the
slope and the walk say it fits, and write down why. A coordinate picked by eye and fixed by looking at a render is
a decision nobody can review.

## The sketch

**The sketch is the plan drawn so it can be reviewed, before anything is built.** It is not a picture of the
board. It draws what the plan states, annotated, with the checker's numbers on the same sheet. `pgmvox.sketch`
holds the format; `examples/islets/scripts/sketch.py` and `examples/drop/scripts/sketch.py` are worked sheets.

**A sketch carries as much detail as its plan, and no more.** Draw every piece, place, objective, route and
number the plan states. Draw nothing the plan does not decide: a texture or a facade in a sketch looks like a
decision and is not one.

**The panels a sheet needs:**

- **The board from above.** Pieces filled by kind, the floor height written on each, places named, objectives as
  team-coloured markers, the image half paler so the symmetry shows. One panel per layer when the board has one
  under or over the surface, the others ghosted for orientation.
- **The routes.** On the board dimmed: each team's walk to each objective, arrowed, with jumps and their gaps.
  This is the panel that shows what play the layout makes.
- **Sections, true scale.** Across the board through every height change that matters, and unrolled along the
  routes that matter most, with the kill height, water and floors marked.
- **The check.** Every measurement against its target, a miss in red.

**Every panel's title carries its legend.** The reader should never have to guess what a colour, a number or a
dashed line means. `Panel.legend` is written into the heading for exactly this.

**A red row is resolved or explained before the build.** Move the piece, change the target with a reason, or
write in `PLAN.md` why the miss stands. A build started over a red row has made the decision without saying so.

**The annotated top-down closes the loop.** After the build, draw the plan's names and markers over the built
world (`MapPanel.built`), so a reviewer sees the board landed where the plan put it.

## The checker

**The checker measures the plan, not the world, and runs in seconds.** Use `plangraph` for walks, arrivals and
jumps, `sight` for what can be seen, `pieces` for a course's links, and the objectives' own positions. Print one
line per measurement, the value then the target. `run` writes it to `renders/plan-check.txt` beside the sketch.

**Measure what decides play, not what is easy to count.** Arrival times per team per objective, the ratio of a
goal's walks, the widest gap, the narrowest lane, what is exposed from where, which stage can be reached when.
A count of pieces or a total area says little about a match.

## Building from the plan

**The generator reads the plan; it decides nothing the plan states.** Heights, footprints, objective positions and
routes come from `plan.py`. What the generator adds is what the plan's last section said it would: the look.

**The read-back is the last check, not the first.** `walk.py` walks the built world from each spawn, asks each
objective `check(w)`, looks for ground to stand on over the void, and runs `audit.footing`. A fault it finds is
a fault the plan let through; fix the plan if it can say it, the generator if it cannot.

## Using the library, and going past it

**What must come from the library:** blocks, orientation and turning; the conventions (heights, symmetry,
directions, eye height, random streams); writing the world; map.xml through `objectives` and `mapxml`; and the
read-back. These keep every board consistent and its XML readable by the studio.

**What should come from the library:** the plan (`Raster`, `Course`, `Symmetry`), the walk graph, the sketch,
and the `run` pipeline. They are how a board is reviewed before it is built.

**What is free:** terrain, landforms, routes, buildings, patterns and solids are there to use, not to obey. A
`World` is two numpy arrays; write any geometry straight into it. A board that wants a shape the library lacks
writes it in its own scripts.

**A thing written twice belongs in the library.** Write it in the board first. When a second board needs it,
move it into `pgmvox` with a test, the way every module here arrived. Do not change `pgmvox` in the middle of a
board run; write it locally and say in the report what the library should take.

**`python3 check.py` before any change to the library is committed.** It runs the tests, rebuilds every example
and compares what each reads back with the snapshot, and rebuilds every board and compares its world's hashes;
`--studio` also holds the exported tables to the studio. A changed number or a moved hash fails until it is
looked at and accepted with `--update`.

## The report

**A board ends with a report whose last section is a table.** Three columns: what you wanted, how hard it was,
and what a studio feature would need to do it. The library and the studio both grow from those rows; a row
without the third column is a complaint, not a request.

**Say what the plan missed.** For each thing decided only while building, one line: what it was, and what in
the plan would have decided it. That list is how the next plan gets better.
