# Seamworks — plan

**Seamworks is a dig under poisoned air, built first as a gray map.** Trenches eight to thirteen blocks deep are held
back by steel panels leaned against the cut, rock that would not cut is left standing, and a hot seam runs under
plated floors. This build exists to test the board's size and walls in game; its materials only tell the parts
apart.

**`scripts/plan.py` is the board.** Every cut, depth, wall, building, seam, spoil heap, ladder, tunnel and objective
is stated there for team green, and team purple's half is its half turn about the middle. `gen.py`, `mapxml.py`,
`renders.py` and `walk.py` read it and decide nothing it states.

## The arrangement

**The board is 300 by 140, two teams under a half turn.** Each team spawns in the back of its hall, in its own
corner. The hall's front stays open to attackers: only a box of ten by twenty-four at its back is the spawn.

**Three lanes cross it.** The middle runs from the forecourt through a quarry, round its mesa, down a throat ramp
into the middle at -13. The twin cut runs along the team's own long edge, two channels split by ribs, and ends in
the enemy's drift tunnel. The drift tunnel runs from the forecourt into the enemy's twin cut, with an unfinished
branch that ends in a ladder up to the surface beside the side cut's ladder.

## What is played for

**Destroy the monument and capture the flag.** The monument is two by two by two, floating three over the crust at
(109, 38). The flag starts in the passage between the hall and the boiler house and comes back to one of three posts,
drawn at random: the passage, the boiler house or the forecourt.

**A flag is scored in the capturing team's own spawn.** The match ends at the first monument down or the third
capture; that rule is a placeholder until the author decides it.

## The ground and the buildings

**The crust rises and falls a block or two.** Its height is smooth noise one to three blocks about the surface level,
made symmetric under the half turn. Cut floors keep their depths from the surface level, so a cut is a block deeper
under a rise. Panel lips, ladder tops, the shaft and the monument's float follow the crust where they stand.

**A building is two or three storeys, by section.** A storey is five blocks, a slab and four of air, and each section
has a ladder through its slabs and windows where its wall faces open air. A taller section walls itself off over a
lower one, whose roof becomes a terrace.

| Building | Sections, in storeys |
|---|---|
| hall | the north end three, the wing and the south end two |
| boiler house | the west body three, the east arm two |
| winch house | west three, east two |
| pump house | the slot side three, the east side two |

**A two-storey section in a deep cut ends near the crust.** Ten blocks of storeys from a floor at -10 or deeper put
its roof at the ground beside it, so it reads as two storeys from the cut and as a flat roof from the surface.

## The walls

**A panel is a quad leaning back into the earth, solved from its four corners.** Its base is two points on the
wall line at the floor, its top the same two points carried back by the lean at each end, ten to fourteen degrees,
and up to two blocks over the surface. The quad is sampled every fifth of a block across its face and two blocks
through its thickness, and the wedge between the wall line and its face is cleared.

**A wall is cut into panels ten to seventeen long, half a block apart.** Each wall's lean is drawn once and each
panel varies it by a degree and a half at either end, so a run reads as one wall with uneven tops. Alternate
panels take two shades of gray clay so the runs can be counted in game.

## The numbers, as walked

**Every post and monument is reached from both spawns, and the two sides agree within a move.** `walk.py` walks from
each spawn with the other team's spawn closed, as PGM closes it.

| From a spawn to | Moves |
|---|---|
| its flag at the passage | 46 |
| its flag at the boiler house, the forecourt | 83, 82 |
| its own monument | 117 |
| the enemy flag at the passage, the boiler house, the forecourt | 308, 303, 279 |
| the enemy monument | 283 |

## The look, for now

**Each material names one part.** Stone is the ground and undug rock, yellow clay the toxic crust, polished
andesite a cut floor, light and dark gray clay the panels, iron the plates, coarse dirt the spoil, stone brick the
buildings, lava the seam. The board's rim is bedrock to the surface and barrier above it.

## Open

**What wins the match, and what the surface air does.** Neither is decided, and neither changes the ground.
