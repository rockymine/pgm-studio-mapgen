# Sonnet Cinderreach — a destroy-core map of my own design

Deliberately not a variation on Sonnet Holdfast: a DTC (core) board rather than DTM, an erected knoll
rather than a flat clearing, a river rather than a void channel, and a scarp rather than a push for its
one elevation change. `rot_180`, 8 players a team.

## The board

220×320. Spawn at the back; a river (the `Natural` water form, wandered shore) crosses the whole width
of the approach about 30 blocks out, so it is the first thing either team's push has to bridge — a
`docs/gameplay/approaches.md` device ("a river or a drop forces a bridge, which is a chokepoint that
must be built before it can be used") stated with the dressing tool rather than the plan. Past the
river the ground rises into a broad **knoll** the core stands on, with a shallow **depression** cut into
its attacking face — the two devices `approaches.md` calls "above" and "below" on the same landform
rather than on two separate ones. West of the spine is a five-house **ruin** (a "village… fought room by
room," built small and broken-looking on purpose); east is an open ash shelf, cut a scarp-height below
the knoll, "exposed" the way the document says an objective's own ground should be.

| Piece | How |
|---|---|
| Core knoll | a relief `point` mark, h13 r11, at the core's own anchor |
| Depression | a relief `area` mark, h5, on the knoll's attacking (south) face |
| River | a `water` prop, `Natural` form, five-point wander, crossing x −105..105 at z ≈ −100 |
| East shelf | a relief `scarp`, high9/low6/face3/band7, along x=40 |
| Ruin | five small `house` props, a flat-roofed broken-looking shell, `Open` windows (cut, ungrazed) |

## Techniques used, distinct from Sonnet Holdfast

**A goal on a relief-raised knoll instead of a flat clearing.** The core's anchor is still an
absolute `{"piece": "", "at": [...]}` placement, resolved against the terrain the relief actually built —
so the same B128 mechanism that let Holdfast's monument ride authored ground here lets Cinderreach's
core ride *solved* ground, with no plan tier standing in for either.

**A `scarp` mark for a legible one-sided drop**, rather than a `push` for a rounded hill. `relief.md`
§5's grade table is what the numbers were chosen from: face 3 over a 3-block drop is close to the
"soft wall" row — crossable on foot at a cost, not a hard barrier — which is right for a shelf that is
meant to be walked up onto rather than defended as a cliff.

**Water read as a chokepoint rather than as scenery.** `docs/world-export/decoration.md` §7: a channel
"only ever touches existing terrain," so drawing it across the open field between spawn and the knoll
did not require any relief authored underneath it first — the flat ground was enough for a first pass,
exactly as the document says a channel "works on the flat layouts the sketch tool builds today."

## What went wrong

**A rim or wall material chosen for its look, not its render classification, painted the whole knoll
orange in the category topdown.** `BlockRoles.BuiltSurfaces` — the table `RenderCategories.Of` reads to
decide `Ground` against `Structure` — lists **netherrack (87)** alongside sandstone, quartz and stone
brick as a "built" surface. My first `cinder-field`/`cinder-ash` themes used netherrack for the rim and
one wall run, reasoning it would read as "natural scorched rock" the way `docs/tools/capabilities.md`'s
own caution led me to expect only from stone brick or planks. Every 1-block riser the knoll's slope
produces painted in it, and the combined-category render showed a single orange mass roughly the size
of the knoll itself, which is exactly the documented "terrain painted in a built block reads as a
building" failure mode — except the block in question is not one the docs name as an example, so I could
not have avoided it by re-reading them, only by checking a render before moving on (which is what
caught it). Swapping the rim and wall to plain stone (`1`) fixed the read completely with no other
change. **Cobblestone (4) and mossy cobblestone (48) are not in the built-surfaces table and read as
ground**, which is worth recording since they are the two blocks map 1's forest/hill walls already used
and is presumably why that map never showed the same fault at anywhere near this scale.

Otherwise this was the fastest of the three builds: both format lessons from Sonnet Holdfast (`kind`
first on every prop, PascalCase on every enum) applied without incident, and the export, the
traversability read and the column probe on the core all passed on the first try once the theme fix
landed.

## Open gameplay question, decided without an oracle

**Is a river a legitimate *sole* approach control on a destroy map, the way a void channel is?**
`approaches.md` names "a river or a drop forces a bridge" in the same breath as the void-hole and hill
devices, but every worked example in the document and in `docs/pgm/water-lanes.md` is about a *capture*
map's lane. I could not find a documented DTM/DTC precedent for a plain (non-lane) water crossing as an
approach control, so I treated the general claim as settling it — a bridgeable body of water forces the
same kind of committed, visible construction a void gap does, and `docs/world-export/decoration.md`
never restricts a channel to a particular gamemode. The traversability read (0 isolated, 2 components)
is consistent with that reading, but it cannot confirm the river *plays* as a chokepoint rather than as
a shallow ford nobody notices — that is a claim about depth and width under real feet, which is exactly
the kind of question `CLAUDE.md` says belongs to the human oracle this run does not have.

## Coordinates, for checking in-game

| What | World position | Note |
|---|---|---|
| Red spawn | (0, 10, −145) | facing +Z |
| Red core | (0, ~19–23, −60) | obsidian shell, lava interior, floats above a y12–13 knoll |
| Depression | x −16..16, z −48..−30 | held to y5, the core's south-facing entrance from below |
| River | z ≈ −100, full width | `Natural` water, radius 4, wandering shore |
| East scarp | x = 40, the full length of the board | high9/low6, a 3-block soft face |
| Ruin cluster | x −70..−92, z −50..−110 | five small broken-roofed houses |
| The netherrack-as-structure defect, before the fix | anywhere on the knoll's slope | see above — corrected in the shipped build |
