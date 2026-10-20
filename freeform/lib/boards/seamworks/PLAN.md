# Seamworks — plan

**Seamworks is a dig under poisoned air.** Trenches eight to thirteen blocks deep are held back by dark steel
panels leaned against the cut, rock that would not cut is left standing, and a hot seam runs under plated floors.
The town lives in the cuts: brick works stand in them, a market keeps each forecourt, and soot
lies in black patches on the orange ground above.

**`scripts/plan.py` is the board.** Every cut, depth, wall, building, seam, spoil heap, ladder, tunnel, stall, lamp
and objective is stated there for team green, and team purple's half is its half turn about the middle. `look.py`
says what each part is made of. `gen.py`, `mapxml.py`, `renders.py` and `walk.py` read the two and decide nothing
they state.

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

**The crust rises and falls by up to seven blocks.** Its height is rough noise from two under the surface level to
five over it, made symmetric under the half turn. Cut floors keep their depths from the surface level, so a cut is a block deeper
under a rise. Panel lips, ladder tops, the shaft and the monument's float follow the crust where they stand.

**A building shows two or three storeys over the crust, by section.** Under the crust it has as many storeys as its
cut is deep, every one whose floor lies below the surface level. A storey is five blocks, a slab and four of air,
and each section has a ladder through all of its slabs and windows where its wall faces open air. A taller section walls itself off over a
lower one, whose roof becomes a terrace.

| Building | Sections, in storeys over the crust |
|---|---|
| hall | the north end three, the wing and the south end two |
| boiler house | the west body three, the east arm two |
| winch house | west three, east two |
| pump house | the slot side three, the east side two |

**The crust between the twin cut and the quarry is panelled on one side only.** The twin cut's wall keeps its
panels; the quarry's is a rock face set four blocks back, so the crust the monument stands on is eighteen deep, and
the quarry's ladder climbs the rock.

**One panel has fallen from the link's west wall.** It lies eleven out from the wall, three over the floor at its
foot and one at its far end, on the spoil that slumped through the gap.

## The walls

**A panel is a quad leaning back into the earth, solved from its four corners.** Its base is two points on the
wall line at the floor, its top the same two points carried back by the lean at each end, ten to fourteen degrees,
and up to two blocks over the surface. The quad is sampled every fifth of a block across its face and two blocks
through its thickness, and the wedge between the wall line and its face is cleared.

**A wall is cut into panels ten to seventeen long, half a block apart.** Each wall's lean is drawn once and each
panel varies it by a degree and a half at either end, so a run reads as one wall with uneven tops. Each panel is
framed and its neighbour striped the other way, so the runs can be counted.

**Where two walls meet at an outside corner, the shorter of the two panels there is left out.** Both lean into the
same wedge of earth, so one is dropped and the rock shows instead of two panels passing through each other: ten on
the board, five a side, at the slot's two corners, the crust's west tip, the side cut's mouth and the passage's bend.
Between neighbours on one wall a shared block goes to the nearer foot, and no panel is laid inside a building or
past the board's edge.

## The floors and the flights

**A cut floor is worn.** Where a noise field rises it carries lumps of cobblestone half a block or a block high. No lump stands more than half a block
over a neighbour, so the floor is walked without a jump, and none lies on a flight, a plated strip, or within two of
a building, a ladder, a stall, a lamp, a tunnel mouth or a flag post.

**A flight's step edges wander.** The height along a ramp is pushed up or down its slope by a noise of a block and a
half before it is rounded, so each step's edge bends, and a stair faces whichever neighbour one higher lies most
nearly uphill.

## The numbers, as walked

**Every post and monument is reached from both spawns, and the two sides agree within a move.** `walk.py` walks from
each spawn with the other team's spawn closed, as PGM closes it.

| From a spawn to | Moves |
|---|---|
| its flag at the passage | 46 |
| its flag at the boiler house, the forecourt | 83, 73 |
| its own monument | 110 for green, 114 for purple |
| the enemy flag at the passage, the boiler house, the forecourt | 298, 297, 267 |
| the enemy monument | 263 |

## The look

**Every asset is built by one function and judged on a sheet before the map gets it.** `scripts/assets.py` builds each
form (a works building, a panel wall, a plated seam, spoil, a fallen panel, a timbered drift, a ladder bay, a flight,
a worn floor) and asks a look what each block is: a panel block by where it sits on its panel, a building block by
its role, its wall, window band, corner, band, sill, cornice or parapet. `scripts/sheet.py` lines the assets up on a flat crust,
panel palettes and building palettes side by side, and draws them in the game's textures into `renders/sheet/`.

**The sheet settled the panels in two rounds.** A panel is framed in polished andesite round its edge, so each plane
reads on its own, and filled with dark prismarine striped in andesite, upright on one panel and level on the next.
Patches of green wool weather the infill; green clay was tried beside it and barely showed. A smooth stone cap was
tried first and dropped.

**The works are brick, with a band of hardened clay through the windows' two courses.** Nether brick stands at the
corners and the base, smooth stone at each storey's band, the sills and the cornice. A chimney is stone brick ringed
in polished andesite every fourth course, crowned in cobblestone wall, with a plume of grey glass drifting downwind,
one wind for the whole board.

**The cuts were dug through orange ground down to stone, and the stone is what was left.** Under the crust lie five
to eight blocks of overburden in beds that follow the crust: red sandstone, smooth red sandstone, a thinner bed of
hardened clay and one of orange clay. Under them is the rock, so a cut wall shows orange over grey and every floor a
player walks on is stone. The rock nobody could dig, the ribs, the mesa, the pillars and the masses beside the
middle, is stone to its top.

**Thin beds run through the stone.** Every eight blocks a dark bed of cyan clay, and halfway between two of them a
pale bed of clay, each a block thick, leaning a little with the crust and broken where a noise field is low. They
show in the faces of the cuts and the standing rock, never on a top a player walks on, and the stone's own mix of
stone, andesite and cobblestone is left as it was.

**The crust is badlands with soot sunk into it.** Red sand and red sandstone are the ground, with orange clay in it.
Large patches, about a third of the crust, are cored with black clay and dark oak planks a block below the crust and
two in their deepest part, ringed in coarse dirt and podzol. Grey ash, flat clay and a smaller speckle of soot were
tried on the sheet first.

**The floor players walk on is stone, not the crust's ground.** A cut floor is a noise mix of stone and andesite with polished
andesite and cobblestone in patches, so it is told apart from the crust over it. Its lumps are cobblestone and a
flight is stone brick. Spoil is the overburden broken, red sand, red sandstone and coarse dirt, and the
seam's rock is netherrack. Nothing that falls stands over
air.

**The town's dressing is placed, not scattered.** Three stalls stand against the forecourt's rock, out of the flag's
way, and lamps on nether-brick posts stand against the walls of the routes. The drift tunnels are timbered every
six blocks with spruce posts and a beam. The boiler house holds furnaces and coal under a brick chimney.

**The board ends at its edge.** There is no rim: the crust runs to the board's last column and the world stops there.

## Open

**What wins the match, and what the surface air does.** Neither is decided, and neither changes the ground.
