# Coldharbour — the measured record

> A capture board on a chalk down. Two wool rooms a team, placed against each other and reached two
> different ways: one low in a walled yard behind a cut pit, down a sunken lane; one on an open chalk shelf
> with a water lane that opens onto it three quarters of an hour in. The mid is void the build zone crosses,
> and two twenty-block channels in the frontline are void that nothing crosses at all.

Authored for `reports/opus5-coldharbour-authoring.md`, which is the point of it — that document records how
the studio was driven and this one records what came out.

144 × 280 blocks, `rot_180` about the origin, base surface 12, build ceiling 32, ground y 9..46. Nineteen
pieces at six surfaces — 10, 12, 14, 16, 18, 20 — compiling to 12 terrain polygons and 6 structural
rectangles on one island.

## What it is composed for

`docs/gameplay/approaches.md` is law, and three of its claims are what this board is made of.

**Void is the instrument.** The mid is a void band a build zone crosses, so it is contested from the first
minute at the price of building across it. The two frontline channels are 20 blocks and carry **no** build
region, so they are permanent: an attacker who lands on the west front cannot cross to the centre, and the
choice of which third of the frontline to enter is made in the mid and cannot be revised. That is the
"whether a hole can be crossed is a separate decision from cutting it" rule used deliberately in both
directions on one board.

**The two approaches to a team's wools differ.** The yard wool sits behind a 15 × 20 pit cut into its own
ground, so its room has no seam onto the yard at all — the two ways in are round the pit's east arm and down
the walled centre route, and the pit itself is an entrance from below for anyone willing to drop into it and
bridge. The shelf wool is the opposite: open ground, a short run from the frontline, and a **third** way that
does not exist for forty-five minutes.

**The water lane is a second route, never the connection.** It sits between the knoll and the shelf — inside
one team's own land — so the board is fully joined without it and the endgame changes shape when it opens.
`map.xml` carries it as the `water-lanes` region; nothing of it is in the world, which is correct and is why
it appears in no render.

## Measured

| | |
|---|---|
| gamemode | `ctw`, "Capture the enemies' wools!" |
| teams / spawns | 2 / 2, `rot_180`, 24 players |
| wools | 4 — `red` `(-58, 9, 102)`, `orange` `(57, 15, 102)` for blue; mirrored for red |
| build ceiling | `maxbuildheight` 32 (surface 12 + headroom 20) |
| walls | one, `holloway`–`back-west`, defence chests on `back-west` |
| dressing | 4 paths, 16 trees, 4 boulders, 4 flora rings, 4 houses |
| traversability | 30 133 navigable columns, 4 164 bridged over void, 3 components, **0 of 4 markers isolated** |
| evaluator | `score 3.243`, `valid: true` — `fill-ratio 0.68` (band .201–.496), `lane-width 30` (band 10–20) |

**The fill-ratio is a stated choice, not an oversight.** It came down from 0.724 by splitting the hub around
a hole, trimming the corners and cutting the yard pit; closing the rest of the gap meant deleting a third of
the board. The evaluator ranks composed candidates and the compile's 422 is the only refusal, so the number
is recorded rather than chased.

**Zero isolated markers, where Grok Ridge reported four.** A stamped wool cage reads as its own traversability
component when the only ground it touches is the cage floor. Both rooms here carry a land seam onto walkable
ground — the yard room 15 blocks onto `back-west`, the shelf room onto both the shelf and `back-east` — so
the cage is the same building and the reading is different.

## The finish

Three terrain themes, all hand-authored and previewed through `POST /api/themes/preview` before the build:

| Theme | On | Is |
|---|---|---|
| `chalk-down` | the map default | grass rimmed with coarse dirt over two courses of diorite, a quartz rim on the true coast only (`rimEdges: "void"`), a scarp wall banded mushroom-stem / quartz / diorite |
| `chalk-yard` | the two shapes at surface 10 | cobble, gravel and mossy cobble — a beaten farmyard, with a cracked-stone-brick lip |
| `chalk-hanger` | the shape at surface 18 | podzol-edged turf over dirt — the wooded high ground |

The holloway and yard were dropped to surface 10 **so that they would have a shape of their own to paint**: a
compile fuses pieces of equal height into one shape and a shape takes one theme. It is also what a holloway
is.

Room shells: one flint-and-stone cage — cobble plinth, stone-brick body, quartz top course, oak posts, arched
door and windows, stone-slab roof — bound to every wool room, and the same language in hardened clay under a
hipped roof for the spawn barn. Both are previewed in `specs/coldharbour/room-*-iso.png`, and the two
free-standing houses wear the cage style so the yard byre and the wool house read as one farm.

Relief: the played surfaces pinned with `relief_scope: "hold"`, and only the frontline (12) and the downland
(18) left to the field, where a summit mark raises the knoll to 21 and a `rim` mark drops the coast to 11.

## What is worth changing next

**The sward has a ruled edge.** Both flora rings are rectangles, so the ground cover stops on a straight
line — `approaches.md`'s own warning that "an organic polygon reads as terrain where a ruled line reads as a
wall" applies to cover as much as to coasts. The outline should be traced rather than boxed.

**The trees ring the knoll rather than screening a flank.** Eight placed around the hill's perimeter read as a
copse on a hilltop, not the beech hanger closing one side that the design called for. The circulation was
drawn first, correctly; the wood was then fitted round it instead of into the space beside it.

**The knoll is climbed, not bridged from.** It stands at 18 with a summit of 21 against a hub at 14, so it
gives height and sightline but no ledge high enough to bridge to a wool from. `approaches.md` describes a hill
as the "from above" approach; this one is only "around, higher up".
