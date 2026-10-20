# Seamworks — plan

**Seamworks is a dig under poisoned air.** Trenches eight to thirteen blocks deep are held back by dark steel
panels leaned against the cut, rock that would not cut is left standing, and a hot seam runs under plated floors.
The town lives in the cuts: brick works stand in them, a market keeps each forecourt, and soot
lies in black patches on the orange ground above.

**`scripts/plan.py` is the board.** Every cut, depth, wall, building, seam, spoil heap, ladder, tunnel, stall
and objective is stated there for team red, and team blue's half is its half turn about the middle. `look.py`
says what each part is made of. `gen.py`, `mapxml.py`, `renders.py` and `walk.py` read the two and decide nothing
they state.

## The arrangement

**The board is 300 by 140, two teams under a half turn.** Each team spawns in the back of its hall, in its own
corner. The hall's front stays open to attackers: only a box of ten by twenty-four at its back is the spawn.

**Three lanes cross it.** The middle runs from the forecourt through a quarry, round its mesa, down a throat ramp
into the middle at -13. The twin cut runs along the team's own long edge, two channels split by ribs, and ends in
the enemy's drift tunnel. The drift tunnel runs from the forecourt into the enemy's twin cut, with an unfinished
branch that ends in a ladder up to the surface beside the side cut's ladder.

**The land's edge is not the rectangle.** A smooth noise pushes the edge up to eleven blocks out past the 300 by 140
rectangle and pulls it up to eleven in, the same on both halves, and never comes within six blocks of anything dug or
built. Past the edge is void, and the cliff there shows the orange beds over the stone.

**The middle holds the golden apple.** A dais eight across stands square on the board's centre at the middle's floor:
a step of stairs all round, a plinth, four nether-brick posts and a slab canopy lit underneath. A golden apple appears
on the plinth every forty-five seconds while a player stands within four blocks, one at a time.

**Each side has three huts, placed against a wall with open floor in front.** One is eight by five at the gap in the
twin cut's rib, one six by four against the forecourt's north rock, and one eight by five at the far end of the
team's tunnel exit. A hut is dark oak posts and spruce plank walls three high under a gable roof of dark oak stairs,
with a window in each gable end and a table and a chest inside.

**Chevrons in the team's colour point the way toward the other side.** Seven pairs on each half, set into the floor of
the lanes: two in the forecourt and quarry, one in the middle, one south of the mesa, and three along the twin cut.

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
and up to two blocks over the surface. The quad is sampled every fifth of a block across its face, a block
belongs to it when its centre lies within two of the face straight back from it, so a panel is two thick at any
heading, and the wedge between the wall line and its face is cleared.

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
a building, a ladder, a stall, a tunnel mouth or a flag post.

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
| its own monument | 110 for red, 114 for blue |
| the enemy flag at the passage, the boiler house, the forecourt | 298, 297, 267 |
| the enemy monument | 263 |

## The look

**Every asset is built by one function and judged on a sheet before the map gets it.** `scripts/assets.py` builds each
form (a works building, a panel wall, a plated seam, spoil, a fallen panel, a timbered drift, a ladder bay, a flight,
a worn floor) and asks a look what each block is: a panel block by where it sits on its panel, a building block by
its role, its wall, window band, corner, band, sill, cornice or parapet. `scripts/sheet.py` lines the assets up on a flat crust,
panel palettes and building palettes side by side, and draws them in the game's textures into `renders/sheet/`.

**The sheet settled the panels in two rounds.** A panel is framed in polished andesite round its edge, so each plane
reads on its own, and filled with dark prismarine laid in layers of green wool every third block, upright on one
panel and level on the next. No andesite runs inside the frame. Green clay was tried beside the wool and barely
showed, and a smooth stone cap and andesite stripes were tried and dropped as noise beside the works.

**The works are brick, with a band of hardened clay through the windows' two courses.** Brick stairs under and over
the band have their full half inward, so the wall steps back half a block on either side of it and the band stands
proud.

**The corners, inside angles as well as outside ones, alternate nether brick and black clay by course.** The base is nether brick
and the roof's rim a nether-brick slab. Each storey's stripe and the cornice are the two smooth stone double slabs mixed in cells of
two, every sill under a window the smooth one alone, and the roof is the same with light grey wool among them.

**A building stands on level ground.** The crust within three of its walls lies at one height, the one most common
along them, and no soot is sunk there. Where a floor beside a wall lies lower than the building's own, its nether-
brick base is carried down to meet it. A door's head is black clay over nether-brick jambs.

**The lowest storey stands on a plinth.** Its foot is a course of nether brick over the base, and a course of
nether-brick stairs over that steps the wall back half a block. Above them runs the same hardened clay band as the
floors above, its windows in pairs on sills of the smooth double slab.

**No window touches a pillar or a door's jamb.** A window opens only with a block of wall between it and the nearest
corner pillar, and one left beside a jamb when a door is cut is closed into the band.

A chimney is stone brick ringed
in polished andesite every fourth course, crowned in cobblestone wall, with a plume of grey glass drifting downwind,
one wind for the whole board.

**The cuts were dug through orange ground down to stone, and the stone is what was left.** Under the crust lie five
to eight blocks of overburden in beds that follow the crust: red sandstone, smooth red sandstone, a thinner bed of
hardened clay and one of orange clay. Under them is the rock, so a cut wall shows orange over grey and every floor a
player walks on is stone. The rock nobody could dig, the ribs, the mesa, the pillars and the masses beside the
middle, is stone to its top.

**A bare rock face overhangs and is undercut, and none can be climbed.** Over the floor beside a face the rock juts
out one to three blocks, starting at least three over the floor and higher the further out it reaches, and it runs
unbroken up to the crust, so it leaves no ledge to stand on. It juts only where the floor runs on eight blocks past
it, so no cut is narrowed to a jump.

**At a face's foot the rock is hollowed two or three high in places.** Panelled
walls, and the rock within reach of a ladder, door, stall, tunnel mouth, flag post or plated seam, are left
straight.

**A team's colour runs round the foot of every wall on its half.** Where the floor meets a wall, the floor's edge
course is red clay on red's half and blue clay on blue's, the half split at the board's middle line. It follows the
floor into the hollows under the rock, and it stops where a side opens into a tunnel or a doorway rather than a
wall. A plated seam keeps its plates.

**Thin beds run through the stone.** Every eight blocks a dark bed of cyan clay, and halfway between two of them a
pale bed of clay, each a block thick, leaning a little with the crust and broken where a noise field is low. They
show in the faces of the cuts and the standing rock, never on a top a player walks on, and the stone's own mix of
stone, andesite and cobblestone is left as it was.

**The works' roofs carry their plant.** Cooling units, smooth stone boxes three by two with iron-bar grilles down their
long sides and fans on top, stand in rows two in from the parapet every seven blocks. Vents, a cobblestone-wall pipe
under a slab, stand in the corners, and each building's highest roof carries an antenna: an iron-bar mast six high
with two cross-arms, a redstone block at its tip and a redstone torch over it. They keep clear of the chimneys and stand beside the skylights,
never on them, and blue's are red's turned.

**The crust is badlands with soot sunk into it.** Red sand and red sandstone are the ground, with orange clay in it.
Large patches, about a third of the crust, are cored with black clay and dark oak planks a block below the crust and
two in their deepest part, ringed in coarse dirt and podzol. Grey ash, flat clay and a smaller speckle of soot were
tried on the sheet first.

**The crust is dead ground.** A one-block step on the orange ground carries a red sandstone slab on its low side,
so the surface climbs in halves. A soot patch runs four blocks down in its core and two in its rim, so a cliff or a
cut through one shows it. The land is mesa and the soot patches swamp, and both brown the scattered oak leaves that
lie on the orange and the soot, never within reach of a ladder, a monument, a cut's edge or a building.

**Five bare olives stand on each side's crust.** They are the last five of the studio's library, `olive-6` to
`olive-10`, planted with their leaves taken off, at least twenty-two blocks apart and clear of the cuts, the
buildings and the monument; blue's are red's turned.

**The floor players walk on is stone, not the crust's ground.** A cut floor is a noise mix of stone and andesite with polished
andesite and cobblestone in patches, so it is told apart from the crust over it. Its lumps are cobblestone and a
flight is stone brick. Spoil is heaped soot, black clay and charred boards in coarse dirt and podzol, dark against the
orange, and the seam's rock is netherrack. Nothing that falls stands over
air.

**The town's dressing is placed, not scattered.** Three stalls stand against the forecourt's rock, out of the flag's
way. The drift tunnels are timbered every
six blocks with spruce posts and a beam. The boiler house holds furnaces and coal under a brick chimney.

**The board ends at its outline.** There is no rim: past the land's edge is void.

## Open

**What wins the match, and what the surface air does.** Neither is decided, and neither changes the ground.
