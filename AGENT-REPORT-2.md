# Authoring a board from nothing — a second report

The first report (`AGENT-REPORT.md`) came out of recreating an existing map. This one comes out of
building `ashen_quarry` from a paint sketch, which is a different exercise and exposed different
things. First person again, and opinionated, for the same reason.

## What the exercise was

A destroy board, 360×240, `rot_180`, designed to touch every capability at once: a plan carrying its
own elevation tiers, tiers promoted to authored polygons, an erected mesa tilted by per-vertex
anchors, an area-mark relief, per-shape themes over a five-deep nested material, two monuments per
team, and fifty hand-placed props including a sixteen-house town in three authored styles. Twelve
builds, reviewed by the author after each.

It works, and it is not pretty. That distinction is the useful part of this report: almost everything
that is ugly about the result is something I got wrong, not something the system refused.

## The three things I got wrong, and what they have in common

### The quarry should have been a polygon, and my reason for saying it could not be was wrong

The mesa is a plan tier promoted to a polygon and it came out well — an organic plateau with a tilted
top carrying a monument. The quarry is a plan tier too, and I left it a rectangle, having written in
the previous review that a lower tier "cannot recede without leaving void".

That is true and it is not the obstacle. The rule I had already discovered for the town is:

> **the tier that recedes must be overlapped by the other one.**

For the town, the land is *lower*, so the land runs **under** it and the town can pull inward freely.
For the quarry, the land is *higher* — so the land needs to run **over** the quarry's fringe, and the
quarry can then pull inward exactly the same way. Same rule, mirrored. I had the principle written
down in my own review file and still concluded the opposite, because I was thinking about the ramp as
a special case instead of applying the rule I had just stated. The quarry could have looked like the
mesa.

### The void column, and it is the same mistake in miniature

There are **102 void columns along z=29**, a one-row slot at the quarry's mouth. My land polygon
enters its notch as a *diagonal* — `[0,26] → [-70,30]` — so between z=26 and z=30 the land has
already been cut away while the quarry rectangle does not begin until z=30. Nothing covers the strip.

Two boundaries that have to agree, drawn independently, in different files, in different coordinate
idioms — one a polygon vertex list, the other a plan rect. **Nothing checks that they meet.** The
build exported clean, the traversability gate passed, and the void only surfaced because the author
looked at the picture and asked. A "shapes leave a hole the tiers do not fill" lint is the single
check that would have caught the most expensive class of error I hit all session.

### The board is about 30% too big

I read the scale off a paint sketch with no dimensions on it and did not ask. The sketch shows
proportion, not size, and I treated it as if it showed both. Asking "how many blocks across is the
town, roughly?" would have cost one sentence.

**All three are the same failure**: I had the information needed to get it right and did not apply it.
That is the same shape as the dressing mistake in the first report. It is worth naming as a pattern
rather than as three incidents, because the fix is procedural — when a rule has just been written
down, check the next decision against it rather than against intuition.

## The scripts, which should not exist

Three of them, and the author's reaction on seeing them — that writing scripts is not what an agent
should have needed to do — is correct. They are in `tools/` because they were load-bearing, not
because they are good:

| Script | Does | Why it had to exist |
|---|---|---|
| `build.cs` | posts a plan through the six-call loop and injects theme / room / dressing JSON into the compiled layout | nothing composes the finish onto a compiled plan; `mapgen` reimplements a weaker version instead |
| `world-build.cs` | the same, plus promoting compiled tiers to polygons, dropping a tier's leftover shapes, and merging arbitrary shape properties by height | there is no way to say "this tier is actually this polygon" — the ids are minted by the compiler, so a tier has to be addressed by the *height it stands at* |
| `column-probe.cs` | prints one vertical column of a built world | six renderers, all plan-view; a layer stack, a wall, a stamped room and a void column are none of them visible from above |

The first two are a **missing endpoint**. Everything they do is legitimate — the layout is the
documented place for a finish, and `PUT /sketch/from-plan` takes it — but an agent should be able to
post a plan plus a finish bundle in one call rather than hand-rolling the merge, and it certainly
should not have to know that a tier is addressed by height because its id was minted.

The third is a **missing renderer**, and it is the one I would build first. It found the layer stack,
the step heights, the stamped rooms, the bedrock that was and then was not in the spawn, the two
monuments, and the void column. Every one of those is invisible to every picture the studio draws.

## What the system did well, and it is a lot

The list of things that worked first time is longer than the list of things that did not.

**Height modes and `relief_scope` are a genuinely good model.** `level` / `raise` / `sink`, `skirt`,
per-vertex `anchor_heights`, and `hold` / `exclude` compose in every combination exactly as
`relief.md` says they do. A tilted sunken bowl inside a flat pan is four fields, and it worked on the
first build. The document promising that the word is "orthogonal to the height function a shape
already carries" is telling the truth.

**Nesting.** A `cell` inside the top layer of a `layered` over a `noise` over a `voronoi` with another
`cell` in its innermost band — five deep — resolves without complaint. There is no arity limit and no
special case, and that is what let one theme carry grass, a dirt horizon, a rust band and a stone
body in a single material.

**The dressing model is right.** Placed, not scattered; fanned across the orbit; each prop seeded so
two of a kind differ but one re-exports identically. Fifty props, sixteen buildings in three styles
written for this map, and the only thing I could not express was a tree made of clay.

**The symmetry fan is exact.** Interlocking the halves across the seam — a land polygon crossing x=0
in three places so each overhang lands on the opposite side at the mirrored z — worked with no
adjustment at all. The one constraint is real and unwritten: an overhang must not fall in the z-band
where the *mirrored* quarry lands, or the mirror's higher land buries it.

## What I would ask for, in order

1. **A section renderer.** One vertical cut through a built world. Everything else on this list is a
   convenience; this one is the difference between checking your work and guessing.
2. **A geometry lint on the composed layout** — shapes that leave a hole no tier fills, boundaries
   between tiers that do not meet. It would have caught the void column and the one in ClayClay's
   spawn before either shipped.
3. **A finish bundle on the build call**, so an agent posts a plan and a finish rather than
   hand-merging JSON into a compiled layout.
4. **Decouple a spawn's building from its protection region.** They are one rectangle today, so the
   size of a hall and the size of the safe area are the same number.
5. **Reach the stranded knobs**: `bedrockCentre` on a destroyable, thickness and height on an approach
   wall, and a material on a goal's sky marker.

## The honest summary

The system can build this map. It built it in twelve iterations with an author reviewing each one,
and the parts that came out badly came out badly because I misapplied rules I had already written
down, or because I could not see what I had made. Neither of those is a capability gap. The capability
gaps that remain are narrow and specific, and they are listed above and in
`review/ashen_quarry.md` — which is a much better place to be than where the first report started,
where the tool I had been handed could not name the colour of a block.
