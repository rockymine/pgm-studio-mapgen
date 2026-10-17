# Sixes and Sevens — the plan

## The identity

**Two bunkers dug into the mountains at either end of a frozen wasteland, and a cracked snowfield between them
where the crevasses glow with lava because something went wrong.** Bunker 06 in the west is Red's, bunker 07 in
the east is Blue's, each the half turn of the other. A player remembers the walled front with its eighteen-wide
door, the lofted walls holding the mountain back, and the seam of lava down the middle.

## The arrangement

**The snowfield runs the full width of the board between the two mountains.** The play area is 280 blocks long
and 200 wide. Each mountain holds its bunker and is out of play above y 75. The field between the two fronts is
about 90 blocks deep, and it carries no rim of mountains along its north and south edges.

**Each team spawns deep in its mountain and defends two monuments near its front.** The Reactor floats in the tall
hall behind the door. The Pump floats in the yard, a recess cut into the cliff beside the facade and open to the
field. The spawn hall lies about 45 blocks behind both, joined to the tall hall by a tunnel with a corridor over
it, and to the yard by a second tunnel.

**The crevasses lie between the teams.** A seam of them runs along the board's middle, irregular and to lava, with
the Spine, a rock crossing, in the centre and a snow bridge on each side. A second crack crosses each half's open
snow north of the Teeth, with one snow bridge. A build region covers them, so they can be bridged.

## The numbers

| Measured | Target | Plan | Built |
|---|---|---|---|
| Reactor to its spawn | 40 to 90 | 52 | 55 |
| Pump to its spawn | 40 to 90 | 49 | 49 |
| enemy spawn over own, Reactor | 3 to 4 | 3.19 | 3.02 |
| enemy spawn over own, Pump | 3 to 4 | 3.60 | 3.59 |
| Reactor to Pump | 35 to 65 | 54 | — |
| a monument to every enemy monument | 85 to 150 | 121 to 144 | — |
| the door | 18 by 16 | 18 by 16 | 18 by 16 |
| a mud path | wide | 9 | 9 |

**The plan's walks are the plan raster's, and the built walks are the voxel walk's, on foot and placing nothing.**
`plan_check.py` prints the first set and `walk.py` the second.

## The places

| Place | What it is | Why a player goes there | How |
|---|---|---|---|
| tall hall | three segments high behind the door, a gallery round its back and south side at 49 | the Reactor | the door; the spawn tunnel; the dark room's tunnel to its back corner; the gallery |
| spawn hall | two segments high, a switchback stair of 3-deep treads to the upper floor | spawning | — |
| dark room | the bunker's one dark room, the dark segment at its foot, the dark floor | a defenders' way into the tall hall's back | a tunnel from the spawn hall |
| upper corridor | over the spawn tunnel, a segment tall | the gallery over the Reactor | the stair |
| yard | open to the sky, its back wall in panels set out of line | the Pump | the field; the yard tunnel from the spawn hall; the cut from below; the shelf from above |
| the Teeth | rock in front of the door | cover and height on the way in | the field |
| the cut | a trench six deep into the yard | the Pump from below | from the field |
| high shelf | a plateau at 47 held by a lofted wall, south of Red's yard | the Pump from above | wide steps at its east end |
| the Spine, the snow bridges | the crossings of the seam | the middle | the mud paths |

## The look

**Ground, built and accent.** The ground is snow over stone, andesite and cobblestone, with packed ice in the
crevasses' walls and mud of coarse dirt, podzol and gravel on the paths.

**The built family is the author's Bunker style.** It is `pgmvox.grammar.bunker`: the stone segments and their stripe and gray-wool variants. The dark segment is
used in its own room only. The accents are the lofted walls' gray-wool line and the obsidian number on each north
spur. The biome is ice plains.

**What the build adds that the plan does not show.** The mountain over each bunker carries the snowfield pushed
further, with deeper drifts, more rock, cracks of ice, a lofted wall on its upper step and two needles of rock.
Boulders stand on the field away from the paths.
