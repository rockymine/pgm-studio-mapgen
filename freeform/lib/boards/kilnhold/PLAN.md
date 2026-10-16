# Kilnhold - the plan

**Identity.** Two geothermal bunkers dug into the walls of a volcanic caldera, a lava-lake crater between them: destroy
the enemy's two monuments and carry its flag home. A player remembers the black-and-grey ash floor, the long concrete
facade with its pilasters, and the glow of lava under iron grates inside the machine halls.

**Arrangement.** 140 x 200 (x -70..69, z -100..99), half-turn symmetric: red north, blue south, blue is red's
(x, z) -> (-1 - x, -1 - z). Each bunker is a rock massif across the back of its half with the spawn at the back, the
gate hall at the front under a stone facade, a paved apron before it, and four levels:

| level | floor | what |
|---|---|---|
| Crown (roof deck) | 77 | open surface fight: Crown Beacon in a sunken court, pillboxes, cover, cooling basin, mast, east battery |
| galleries | 70 | gate hall galleries, a loft over the gate, two crown ramps |
| gate level | 65 | muster hall (spawn), spine, gate hall with the capture dais, workshop, command post |
| deep level | 57 | pump hall (monument under it), turbine hall and shrine (flag), cross gallery, culverts |

Levels meet by slab ramps rising half a block a cell (descents 16 cells, crown ramps 14, exterior ramps 22-44).
The caldera floor holds the crater (climbable one-block walls, lava lake), two slag banks per half, the cooling tower
(court sunk to 57, culvert to the pump hall) and the quarry pit (culvert to the turbine hall).

**Numbers and targets** (checker: `renders/plan-check.txt`, built read-back: `renders/walks.txt`)

| number | target | plan | built |
|---|---|---|---|
| spawn to each own goal | 40-90 (GO4) | 73 / 71 | 67 / 65 |
| enemy walk / own walk, each destroy goal | 3.0-4.0 (GO1) | 3.27 / 3.06 | 3.42 / 3.22 |
| a team's two goals apart | 35-65 (GO2) | 108 | not met |
| opposing goals apart | 85-150 (GO3) | about 300 | not met |
| steepest interior ramp | 0.5 block a cell | 0.5 | - |
| air under a monument | at least 3 | 3 | 3 |

GO2 and GO3 stand red on purpose. One goal is on the roof and one two levels down, so a team's goals are two ramps
apart; and the board was asked to be 180-220 long, so the opposing goals are a long walk across it. The flag is the
CTF half of the match, three captures to win, and not a destroy goal; its ratio is 2.6.

**Places.** Muster hall: the spawn, dark-oak posts, team-wool stripe, alcoves with kit chests. Spine: the one way
from spawn to gate hall. Gate hall: concourse 30 x 21 x 10, pilasters on the end walls, galleries up both sides by
ramps from the spine end, a loft above the gate, the capture dais (the net) in the middle. Workshop and command post
flank the muster hall. Pump hall: orange sandstone, the monument floating over a grated pool. Turbine hall: black clay
and coal, a drum ringed by a grated lava moat, walkways across; the flag stands in a shrine off its east wall. Cross
gallery joins the two halls under the gate hall. Crown: roof deck; the beacon sits in a court sunk a block so it floats
four over its floor. Cooling tower and quarry pit: the two ways under the facade from the field.

**Approaches.** Crown Beacon: the west ramp from the lane (open, 70 cells of climb), the crown ramp from the gallery
(covered, from the gate hall), or across the deck from the east (flat, pillboxes). Pump Hall Monument: the west
descent from the gate hall, or the west culvert from the cooling tower, which bends twice (a flanking tunnel).
Flag: the east descent or the east culvert from the quarry pit.

**The look.** Ground: ash, grey and black clay with coarse dirt, scoria of red sandstone and orange clay near the
heat, rock in beds with black basalt courses. Built: bone concrete, stone brick and polished andesite, dark oak
timber. Accent: hazard orange, lava and glowstone, team wool (red 14, blue 11).

**What the build adds that the plan does not show.** Boulders and bare spruce trunks on the open ash (kept off the
ways and 27 blocks from the crater's middle), lamp posts at the apron and the two entries, banners on the gate
hall pilasters, the portal frame and the muster hall wall, furnaces, anvils and bookshelves in the wings, valve
stands in the pump hall.
