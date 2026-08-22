# Opus 5 — Hoarstone: erected shapes, an archipelago, and four house plans

## What I set out to build

A second board in Elderwold's language, **smaller**, and abstract where that one was naturalistic:

- **erected pieces standing out of the terrain**, themed as materials the ground is not made of, with
  sharp-edged polygon plans and slanted tops rather than the raised rectangles `tools/seeds/ruediger`
  builds its steps from;
- an **icy landscape** with areas of exposed stone and areas of snow;
- **template spruce**, not the grower's;
- **houses taken seriously** — an L, a T and a U, with different storey stacks and different roofs;
- **one island a team plus three neutral islands in the middle**, all drawn the same way.

`maps/opus5-hoarstone`, `specs/opus5-hoarstone/`, `review/opus5-hoarstone.md`.

## What worked first time

- **`height_mode: raise` with `skirt: 0` is the whole erected-pillar idiom.** One probe answered the
  semantics: a raise of 10 over flat y11 ground tops at y21 everywhere, and the same shape carrying
  `anchor_heights` runs y19→y25 across its own footprint. Sheer face, stated height over whatever it
  stands on, slant per vertex. Ruediger's raised rectangles are a *different* device — plates at
  successive `base_height` — and both are right for what each is doing.
- **A polygon with no `controls` at all.** The skerry and every standing stone are drawn as bare
  vertex lists; the sharp corners are the point. The handle machinery is opt-in per edge, so "sharp"
  costs nothing to say.
- **An on-axis piece with `mirrors: false` becomes its own island, `neutral`**, and the relief keys
  by island, so a two-island board is two relief documents in one finish. `{"*": {...}}` would have
  given both the same terrain; naming them separately gave the middle its own.
- **Authoring a ring as half its points plus their negations** makes a shape that is exactly its own
  rot_180 image (measured: worst point-to-mirror distance 0.000), which is what lets every prop and
  every stone on the core island be authored once and fanned.
- **`POST /terrain/prop-preview`** answers a house *at the footprint it will actually stand on*, wings
  and all, as a PNG at `scale=8`. `room-styles/preview-snapshot` draws the style on a default box; for
  an L or a U that is not the building. This is the read to take before a multi-wing house is placed.

## What I got wrong

**I put the pillars in the ground's own tone family.** The first cut painted them andesite, polished
andesite and cobble — a reasonable "rock" palette, and invisible on a board whose exposed ground is
rock. `render/surface` showed them as terrain with a different seed. An erected shape is a *statement*,
and it has to leave the family the ground is in: black stained clay, ice-blue clay and ochre terracotta
each read at a glance. The same rule the brief states for buildings turns out to be the rule for
terrain features too.

**I gave a three-course storey a seven-band wall.** A storey carries `clear + 1` courses, so the watch
house's brick/checker/spruce stack built brick and checker and stopped. The section read as one grey
mass and I nearly blamed the roof. Sizing each storey's stack to its own clear is also what makes three
storeys read as three rooms rather than one tall wall.

**I let a building stand inside a standing stone.** A stone is an authored *shape* — terrain — so
`DR-CLAIM` never sees it, and the build reported nothing. The map had an L-plan shrine sitting in the
middle of a monolith and the only way I found out was looking at the top-down. Houses are placed by
hand and nothing filters them, so the build script now audits every footprint against the islands, the
stones and the goal ring: nine faults on the first pass, none on the last.

**My site filter ignored the fan.** Three of the first build's four declines were a prop clashing with
another prop's *mirror image* — a rock beside a building on the core island is a rock inside that
building's twin. A prop is stamped at every image of its orbit and declined whole if any image fails,
so a filter that tests only the authored cell is testing half the map.

**I tested footprints against the authored polygon instead of the built coast.** The Bézier bulges
outside the vertex ring on convex stretches and inside it on concave ones, so the raw ring both
rejects good sites and passes bad ones. One house corner sat inside the drawn polygon and one block
past the built shore, and `DR-SITE` was the first thing to say so.

## What I could not say

**A second theme on one island without a second shape.** `TP10` scopes a theme to a shape, so the only
way to paint part of an island differently is to draw part of it as its own shape — or to brush it with
a path, which cannot carry a prop. That is a real and reasonable boundary; I mention it because "give
the wood its own palette" is the obvious next thing to want and there is no third answer. **In the
design, not missing from it.**

**A per-shape island assignment for an authored shape.** `tools/drive.py` appends every `addShapes`
entry to `islands[0]`, so all thirteen stones joined `team` and were fanned — which happened to be
what I wanted on all three landmasses, but only because I made the core island its own mirror image
first. A stone that should *not* fan has nowhere to go without editing the layout after the patch.
The layout format has the field; the driver does not surface it. **Out of reach from where I stood.**

**How far apart two spruce must stand.** The same gap Elderwold reported for oaks. I reused the
`(hₐ + h_b) / 4.7` Chebyshev fit measured on oaks and it held for spruce with nothing declined, but
that is one board's luck, not a measurement. `Decorator.CanopyRadius` knows the answer before any world
exists; nothing answers it over HTTP.

**Whether a house overlaps an authored shape.** `HP1`–`HP3` check a building against itself, `HJ1`–`HJ5`
check its wings against each other, `DR-*` check it against other *props*. Nothing checks it against
terrain the author drew, because from the pass's side that is just ground. I looked for it in the
openapi — there is no route that takes a footprint and answers what is under it except
`sketch/columns`, which builds the world. **Missing from the surface**, and cheap to want: a building is
the one prop big enough to sit on a landform without noticing.

## Open gameplay questions

1. **Is a 64-block build ceiling too high?** The ceiling is 20 over the highest terrain, and the highest
   terrain is now a 36-block monolith rather than a hill. On a 130-wide board that is a lot of sky to
   build in. Capping the stones nearer the terrain would lower it; so would deciding the ceiling off
   the terrain the *relief* solved rather than off every shape. I built it as it stands.
2. **Do the stones read as cover or as walls?** Each is sheer on every side (`skirt: 0`) and 8–18
   blocks across, so a fight around the ring is a fight around eight blind corners. That is either the
   best thing on the board or unplayable, and nothing measures the difference.
3. **Three straits, all bridged by build zones — is the middle too easy to hold?** The core island is
   reached by three separate spans and holds the ring, the hearth and both altars. A team that takes
   it early takes the only ground between the two halves.
4. **42.8% of the ground is dead** by `coverage`, against Elderwold's 57%. The repository's author has
   said that reading is imperfect and that Elderwold's share was fine for what that board is; I record
   the number here without treating it as a verdict.
