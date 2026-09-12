# Kilnholt Cut — a destroy board on a worked-out quarry

**In one sentence:** two rival stonework guilds have driven their excavation into opposite flanks of
the same worked-out quarry, each guarding two buried obsidian monuments at the bottom of their own
cut, and a played-out mine adit under the west flank still connects the two sides for whoever is bold
enough to use it.

80 × 188 blocks, `rot_180` about the origin, base surface 16, y 0..30 on the surface (the tunnel runs
y 0..8 underground). One destroyable pair a team — `dtm` only, kept to one goal kind per the brief.
`<gamemode>dtm</gamemode>`, `<objective>Destroy the enemy's monuments!</objective>`.

## The board is one shape a side, carved by three relief marks

The plan is two pieces a team — a 20×20 spawn and a 40×58 excavation — stated at the same surface so
they fuse into one landmass at compile (`docs/generator/model.md`'s "abutting pieces of equal height
fuse"). Everything else is relief: a `rim-w`/`rim-e` line pair holding the two flanks at y28-30, and one
wide `descent` line down the centre — spawn knoll (y28) to the worked floor (y10) to a low apron at the
void's edge (y6) — with a 24-block-wide `tread` so the flat floor stays flat and only the outer 8 blocks
either side loft into the rim's height. That one mark is the whole "flat floor, graded shoulder, sheer
face" reading: `incline?format=text` puts 67.9% of the ground under 30° (the floor and the spawn knoll),
6.3% at 30-39° (the shoulder) and 25.7% at 40° or steeper (the cut face up to the rim) — a spread across
bins rather than a single spike, which is what a real graded slope reads like rather than a stepped one.

## The tunnel, built bottom-up

The two guilds' territories are joined on the surface only by a **permanent void gap** 32 blocks wide,
spanned edge to edge by a build zone — bridgeable from the first minute, at the price of building in the
open. Underground, a mine adit runs diagonally from `(-30, -22)` in the western excavation, under the
gap, to `(30, 22)` — the same point turned 180° about the origin, so the whole corridor is its own
`rot_180` image and needs authoring only once.

Four layers, bottom-up, exactly as `specs/rockymine-probe`'s README describes the technique: an
`override` cavity on the compiled ground layer drops the corridor's own columns to a floor at y1 (and
takes them out of the relief solve with `relief_scope: exclude`, so the surrounding hillside's grading
never writes back over it); `tunnel-walls` at base_y 1 lays two 2.5-block strips either side of a
3-block walkway; `tunnel-cover` at base_y 4 seals the roof across the whole width; `tunnel-resume` at
base_y 6 puts two more blocks of rock over that before the hillside's own ground resumes. A stair at the
red end climbs from the tunnel floor back to the surface over an 11-block run — visible in
`renders/world-xray.png` as the pale diagonal breaking out of the hillside beside the portal. The blue
end's stair is the same shape's `rot_180` image, built by the ordinary team fan.

The two side-wall strips and the roof are **not** in the fanned `team` group — each of the three new
layers states its own `groups` entry with `mirrors: false`, so the studio's usual half-a-map-for-free
fan is switched off for exactly these shapes and the adit is built once, where it was drawn, rather than
appearing under both flanks. The floor cavity is the one shape that *is* on the fanned ground layer, and
it works there only because the two portals are already `rot_180` images of each other: fanning it
reproduces the same cavity rather than a second one.

`GET /map/sonnet5-kilnholt-cut/column?at=0,0` under the middle of the void reads bedrock at y0, open air
y1-3 (the walkway), then solid from y4 — floor, corridor, roof, in one probe. And the walk endpoint
confirms it is doing real work: `spawn-red -> destroyable-1-1` (red's spawn to **blue's** deep mark)
reads `rises 0, falls 0, worst step 0, walked end to end` — the only zero-cost, zero-climb way across
this board is through the tunnel, because bridging the surface gap costs placed blocks and a fall the
tunnel does not.

## Two goals a side, repositioned once the numbers said so

The brief asked for this to be checked rather than assumed, and the first placement needed it. Both
destroyables started at `(±8, -46)` — `/plan/inspect` read `GO2` (a team's own goals should stand
35-65 apart, by walk) at **16**, far under band, because two goals eight blocks either side of the
spawn's own axis are eight apart, not sixteen. Spreading them to `(±19, -46)` fixed `GO2` but broke
`GO1` (the enemy/own walk ratio wants 3.0-4.0): the wider stance cost eight extra blocks of own-spawn
walk and dropped the ratio to 2.6-2.8. Moving them along the excavation's own axis instead — closer to
spawn, to `(±19, -50)` — bought back the ratio without touching the pair spacing, and the final read is
clean:

| goal | own walk | enemy walk | GO1 ratio |
|---|---|---|---|
| Kilnholt's Deep Mark (west) | 42 | 139 | 3.31 |
| Kilnholt's Shallow Mark (east) | 41 | 140 | 3.41 |

Both inside `[3.0, 4.0]`, both inside `GO4`'s `[40, 90]`, and the pair 38 apart by walk (`GO2`'s
`[35, 65]`) — close together on the excavation floor rather than scattered, and still each its own
health bar per `approaches.md`.

## What the ground is made of

Two themes. `quarry-cut` is the whole surface: a `layered` material on the **slope** axis carries grass
over dirt below 28°, a coarse-dirt/andesite cell mottle from 28-44°, and a bare stone/andesite/cobble
cell above that — the flat reclaimed floor, the worked shoulder and the cut face in one stack, finished
by angle rather than by height. `quarry-under` is the tunnel's own stone/andesite/cobblestone cell mix,
carrying no slope banding at all since nothing underground needs one. The fill on `quarry-cut` is a
seven-block stone/andesite/cobble cell with `rise: 8`, so a cut face reads as a mottled body rather than
vertical stripes.

One winch shed stands on the flat floor, well back from both objectives and off the main descent —
timber (log corner posts) over a brick wall, forked from the `cottage` preset with `footing` left unset
and the roof kept gable (never shed-form). A three-material Gravel/Andesite/Cobblestone path runs solid
from the spawn door down onto the floor, drawn before the trees were placed. Six spruce, template
recipes at varied heights, stand at the rim on both flanks — all more than fifteen blocks from either
destroyable, clear of the four-block cover ring and the ten-block standoff alike.

## What went wrong

**The first cut piece was too wide, and coverage said so before I looked at a picture.** At a
104-block excavation, `coverage` read 30.3% dead — four roughly-1000-cell patches in the corners beyond
where the descent spine or the rim marks give anyone a reason to walk. Narrowing the piece to 80 blocks
(and pulling the rim marks and rim trees in to match) cut that to 9.4% dead without moving a single
placement, which is the shape of the fix the docs describe: the flank was decorative width, not play
space, and the number said exactly how much of it to give back.

**A subtract on a new layer reads as contradicting the ground layer beneath it, even when the two never
overlap in the world.** My first cut at the tunnel's side walls was one full-width `add` plus a
`subtract` for the walkway gap, both on `tunnel-walls`. The store refused it — `SK13` — naming the
compiled excavation shape and the subtract as disagreeing about whether that ground is void, even though
`tunnel-walls` sits four blocks under the excavation's own surface and the two can never actually share a
column. Reading the rule text again: it is checking the **document's** shapes against each other, not
the resolved world, so a subtract's implied "this is empty" is compared to every `add` in the whole
layout regardless of layer. Two plain `add` strips (one either side of the walkway) instead of an
add-and-subtract sidesteps it entirely and builds the identical corridor.

**A quad's `anchor_heights` follow the vertex order the helper emitted, not the order I was thinking
in.** The stair's four corners come out of a shared `strip()` helper as `[near-lo, far-lo, far-hi,
near-hi]`, and my first anchor list assumed `[near, near, far, far]` — which puts one near corner at the
tunnel floor and the other at the surface, and a diagonal twist where a clean rise should be. Checking
the helper's own return order against the anchor list before trusting a column read is what caught it.

**One rough edge I did not fully resolve.** `sketch/relief/read` still raises `SK11` for 350 cells of
standable ground near the western portal with "no route onto them" — almost certainly the stair's own
risen shoulder or the tunnel-cover's edge, a ledge a player could stand on but that nothing currently
walks up to from the rest of the board. It is a complaint, not a refusal, and the export gate is open
with the spawn-to-objective chain connected either way; I have not traced the exact cells it means, and
I am reporting it rather than guessing at a fix.

## Open gameplay question

**The tunnel is a free crossing where the surface gap is not.** Bridging the void costs placed blocks
and time in the open; the tunnel, once its two stairs are built, costs neither — the walk endpoint
confirms a zero-cost, zero-climb route through it in both directions. Whether that is right for this
board (a genuine secret shortcut worth the trouble of finding it) or whether it should carry some price
of its own — a narrower walkway, a longer detour, a chokepoint at one portal — is a question about how
the map plays rather than one the geometry answers, and I built the cheap version because the brief
called the tunnel a reward "for whoever is bold enough to use it" rather than asking for it to be costed
against the bridge. Recorded here rather than decided.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red Deep Mark | `(-19, -50)`, floats 4 | obsidian, `pillar-3` |
| red Shallow Mark | `(19, -50)`, floats 4 | obsidian, `pillar-3` |
| red spawn | piece `(-10, -94)..(10, -74)` | facing `back`, 20×20 |
| the void gap | `x -40..40, z -16..16` | build zone, permanent void outside it |
| the adit, red portal | `(-30, -22)` | floor y1, corridor y1-3, roof from y4 |
| the adit, blue portal | `(30, 22)` | the `rot_180` image, same profile |
| the adit under the gap | `(0, 0)` | bedrock y0, open y1-3, solid from y4 — probed |
| red stair | from `(-30, -22)` rising over 11 blocks | y1 to y14, `override` + `relief_scope: exclude` |
| winch shed | `(-24, -73)..(-16, -65)` | timber-over-brick, gable, no footing stated |
| the path | `(0, -80)` to `(0, -50)` | Gravel/Andesite/Cobblestone, solid, radius 3 |
| traversability | — | export gate OPEN, spawn↔objective chain connected both sides |
| coverage | — | 9.4% dead, down from 30.3% before the excavation was narrowed |
