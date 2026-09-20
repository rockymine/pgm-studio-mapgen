# Raising a lane

**A composed lane bends, and giving it height is a choice between tiers rather than between tricks.** The
plan says what ground is where and at what surface; the layout draws shapes on it; the relief solves a field
under all of them; a made layer puts a storey over the lot. Every tier can raise a lane. What separates them
is what the climb costs a player — and what the **corner** does to it. Open the card in the studio as
`technique-raising-a-lane`, or run `build.py`.

Nine panels, each the same L: a stem **12 wide** running 40 north, a **12 × 12** corner at its head, and an
arm **36** east of it, with the foot at surface 9 and the arm's end eight blocks up at 17. The lane is an L
because a composed one is — a wool approach turns, a hub arm turns into its spawn — and a bar hides
everything a bend decides.

| Panel | Tier | Stated as | `walk` along the path | Across the lane |
|---|---|---|---|---|
| `piece-steps` | plan | 5 heights, every seam a step of 2 | **4 × `scramble +2`**, 4 placed | level |
| `piece-treads` | plan | 9 heights, one course a seam | walked, 0 placed | level |
| `tilted` | layout | one polygon, an anchor at each of six vertices | walked, 0 placed | **leans 3 blocks in 12** |
| `two-ramps` | layout | one tilted polygon a leg, the corner given to the stem's | walked, 0 placed | level |
| `ramps-and-landing` | layout | the same two, the corner held level between them | walked, 0 placed | level |
| `plates` | layout | 9 override plates over a lane left at its foot | walked, 0 placed | level |
| `marks` | relief | two `area` marks, everything between unpinned | walked, 0 placed | level but at the corner |
| `push` | relief | one push of 8 at the arm's end, `falloff` 22 | walked, 0 placed | level |
| `deck` | layers | the lane untouched, a storey over its corner and a flight up to it | the lane never climbs; the storey walks from its own flight | level |

## What the bend decides

**A step across a bend is still a rectangle, so the corner costs a piece of its own.** The stepped panels put
three steps up the stem, one on the corner square and five along the arm: the corner cannot be shared between
the stem's bands and the arm's, because one runs in z and the other in x. That is the plan tier's whole shape
— nine heights for eight blocks, and a piece for the turn.

**What it buys is that every tread is level across.** `across.txt` reads each lane at three stations, and
every stepped panel answers one figure a row. A rectangle is flat by construction, so a player running the
lane is never on a sideways slope.

**A tilted polygon cannot turn a corner.** `tilted` states an anchor at each of the L's six vertices and
comes out leaning: twenty-six blocks up the stem it reads **11 11 11 11 11 11 12 12 13 13 13 14** across its
twelve, a cross-fall of three. A tilt is one surface fitted to its anchors, and an L asks it to climb north
along the stem and east along the arm at once, so it splits the difference and the lane tips into its own
corner.

**The studio says the other half out loud.** Storing that panel answers `SK26` at 200: *"'tilted' … climbs,
and its high end arrives nowhere — from (−6, −45) at course 17 the ground falls 17 within four cells"*. A
tilt has to land on something, and on a lane whose arm ends at the void it lands on nothing.

**So an L takes one tilt a leg, and the join is flush by construction rather than by arithmetic.**
`two-ramps` climbs the stem from 9 to a middle height of 13 and the arm from 13 to 17. The stem's ramp holds
13 across its whole east edge and the arm's holds 13 down its whole west edge, because an anchor pair states
one height along the edge it spans — so the two meet at one course with nothing to line up by hand. Across
the stem it reads **12 12 12 12 12 12 12 12 12 12 12 12**: level, where one polygon leaned.

**Whether the corner climbs or waits is the knob between the two ramp panels.** `two-ramps` gives the corner
square to the stem's ramp, so the climb runs through the turn. `ramps-and-landing` holds it level at 13, and
the path reads twenty blocks of flat where a player changes direction — the landing a turned flight is
usually drawn with, and the place a defender stands.

**A tilted surface is rounded per column, so a riser line can miss a cell.** Counted over every riser line
of all three, the stem's rows and the arm's columns alike: `tilted` carries **6**, `ramps-and-landing` **2**
and `two-ramps` **1**. A notch is a one-block hole in a line that is otherwise flat — a rounding artefact
rather than a fault, and none of the three is free of it.

**The relief grades the path and cuts the corner on the diagonal.** `marks` pins the first eight blocks of
the stem and the last eight of the arm and leaves the stem, the corner and most of the arm to the relaxation,
which climbs one course at a time the whole way round. It is level across the stem and tilts at the corner
alone — 11 11 11 11 11 11 11 12 12 12 12 12 — because the relaxation grades on the straight line between two
pins and the lane does not.

**A push reaches a corner radially, which is not how a lane runs.** `push` lifts the arm's end by 8 and
grades back over `falloff` 22: the arm climbs, the corner catches the edge of the skirt, and the stem never
leaves the base. A push builds a landform a lane crosses; it does not raise a lane.

**A made storey ignores the bend entirely, and it is only a route if something climbs to it.** `deck` leaves
the L at 9 and crosses a stone floor over the corner at 16 on four legs. Drawn with nothing but that, the
walk answers **`barrier +8` at every edge of it**: a storey nothing reaches is a roof, and the lane under it
is the only route on the panel.

**So the flight is part of the structure.** Eight treads two blocks deep rest on the lane at the arm's far
end and climb to y16, flush with the slab — all on the deck's own made layers, so the ground never changes.
From the stair's foot the deck walks **40 blocks, nothing placed**, back over the corner the lane turns.

**Asking about a storey takes a `to` that names one.** `walk?to=x,z,y` is the difference between the deck and
the lane under it, and it is the only way to get an answer about the upper surface at all.

## What the columns say that neither profile can

**`plates` and `piece-treads` read the same profile and are not the same ground.** Both climb 9, 10, 11 … 17
along the path and read level across. The column under a plate is the plate: an **override add is a
privileged set and wins the column whatever its height**, so a plate replaces the lane under it rather than
standing on it.

**The two relief panels start a course lower than the drawn ones.** They read 8 where the drawn panels read
9, because the relief's `base` is what unpinned ground settles at and a shape's drawn height is only what it
was drawn at.

## The recipe

- **a lane that has to be walked wants one course a seam.** Nine pieces, or a relief that grades. Two is a
  placed block, and `EL1` names a land seam of 2 before anything is built.
- **a bend costs a piece.** A step is a rectangle and the corner of an L belongs to neither leg, so it takes
  a step of its own — which is also the step a theme, a relief scope or a keep-out can be hung on.
- **do not tilt an L with one polygon: use one a leg.** Give both legs the same height along the edge they
  share and the join is flush with no arithmetic. One polygon over a bend leans the ground under the player.
- **decide whether the corner climbs or waits.** Giving it to a leg's ramp keeps the climb continuous;
  holding it level makes a landing, which is where a turn is actually taken.
- **a tilt has to arrive somewhere.** `SK26` names a climb whose high end falls away, which is what a ramp
  drawn to the edge of a piece does.
- **the relief grades between what it pins, not along what you drew.** Pin the corner too if the corner is
  meant to be level.
- **a push is a landform, not a climb.** Its falloff is radial, so it reaches a bend from the outside and
  leaves the far leg where it was.
- **an override add wins the column whatever its height**, so use it where the plate *is* the new ground.
- **a storey needs its own way up, drawn with it.** A deck with no flight is a roof: the walk says
  `barrier +8` at every edge, and nothing else reports it because the lane underneath still walks.

## Limits

**No `raise` panel, deliberately.** A `raise`'s `skirt` is taken in from the outline on every edge at once,
so on a lane 12 wide it leaves a two-column ridge with the ground falling away either side — and bending the
lane does not help, because the legs are as narrow as before. A raise belongs beside a route rather than on
one; `techniques/made-ground` is where the instrument is worked, and the arithmetic is in
`GENERATION-NOTES.md`.

**The plan panels are what a plan compiles to, not a plan.** A compiled plan carries its own `mirror_mode`
and a group that mirrors, so seven compiles cannot share a world —
`techniques/taking-over-a-composed-board` is the worked plan-driven case.

**The climb is eight blocks over a path of about 76.** A longer run at the same rise walks at a shallower
grade; a shorter one does not. What transfers is the rule, not the profile.

## What checks it

- `profiles.txt` — every lane along its own path: up the stem, round the corner, out to the arm's end.
- `across.txt` — every lane read across itself at three stations, which is where the bend shows.
- `walks.txt` — `walk` over each one: the route, the blocks placed, and the word for every step that is not
  a plain walk. Beside them the deck's own two, under the storey and up its flight, which is what a `to`
  naming a storey answers.
- `columns.txt` — five columns: under a plate against under a tread, the deck's own column, and the two
  sides of the leaning stem.
- `across.txt` also counts every riser row of the three tilted panels, which is where the rounding notch is.
- `raising-a-lane.layout.json` — what `build.py` writes: 37 ground shapes in nine groups, and ten made
  layers for the deck, its legs and the eight treads of its flight.

Renders: `iso.png`, the nine Ls together; `piece-treads.png`, `tilted.png`, `two-ramps.png`,
`ramps-and-landing.png`, `marks.png` and `deck.png`, each close enough to see what the bend did.
