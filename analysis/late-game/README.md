# Holding a goal: the studio's approaches, a board under a roof, and the late game

**This note carries the studio's model of a goal's approach into pgmvox, puts a whole board under a roof, and
measures what keeps a goal's door a door as a match goes on.** It answers the author's review of Hollowstack: a wool must always be
defensible, and on that board one was not. It starts from `pgm-studio/docs/generator/model.md` §4–§5 and
`pgm-studio/docs/gameplay/match-flow.md` §4–§6, and every number in it is read off a built world.

## 1. What the studio builds around a goal

**A goal stands at the end of an approach, and the approach is a handful of rectangles each named for what it does.**
The generator's wool menu is I, L, Z, U, H, donut and clamp, with the scythe as a ninth form it builds and keeps off
the wool menu; each is an ordered template of parts: `entry`, `run`, `bar`, `leg`, `room-run` and the `room` the goal
stands in, last. The room never docks; the entry is the one edge a host attaches through.

**What a form leaves empty is as much the design as what it fills.** A donut's hole, a U's bay and a clamp's gap are
void the build zone does not cover, and a void outside the build zone can never be bridged at any height
(match-flow §5). So the empty cells decide which ways in exist for the whole match, not just its opening.

**Each way in gets one bedrock wall, ten to twenty blocks in front of the room.** A wall stands only on a seam with
void past both its ends, because one with ground running past an end is walked round. A plain approach has one way
in and one wall; a donut, a U, an H and a clamp have two and take a pair.

**The room is held from its corner.** It wants two faces on void (`approaches.md`), so a defender holds two lines and
an attacker chooses between them; ground all round a room leaves nothing to hold.

## 2. What pgmvox now has of it

| Module | What it does |
|---|---|
| `plan.approach` | the eight forms as part-named templates; `classify` reads a form back from its cells by the generator's own decision tree; `doors` counts the ways in; `walls` seats the defence walls by §5.14's rule |
| `built.chambers` | **the rejected way down**: lays an approach as a chain of chambers stepping down a storey a part; kept for the study in §6, not for boards (§5) |
| `plan.bunker`, `built.bunker` | a board the studio composed, read as a bunker under a roof and laid: its land islands, its build regions void, its holes pillars, its rooms sealed (§5) |
| `read.late` | a goal's walk in a long match's four phases (ground, bridged, sky, dug), and in each whether walling the room's doors shuts it off |
| `play.rules` | `Build(break_only=...)` keeps the void rule and lets a player break only those materials; `Crafting(disable=...)` takes recipes away; `Renewables(...)` makes ground grow back |

**A goal's approach is now a plan an author or a board script can state and check.** `classify` agrees with the
template on all eight forms at three sizes, `walls` closes every way in on all eight, and both are tests.

## 3. Why the late game leaves the map

**A long CTW match ends up played on ground nobody authored.** The recorded matches put a quarter of all play at
the build height by a match's last tenth, and on the two longest-running boards nearly half of all standing play is
on structure players built (match-flow §6.1, §6.12). The author's account adds what the logs cannot show: the middle
dug to bedrock and buried in kit blocks, the defenders' wall raised to the build limit, and the sky network.

**The defence of that sky is built from crafted blocks.** Anti-climb staircases of fences and iron bars side by side
take neither a placed block nor water; walls of crafting tables take no block placed against them without
sneaking; a crown of fence gates on the wall keeps attackers off it. All of it comes from a crafting table.

**Three rules open the board up, and every map has all three by default.** Every block may be broken, so the ground
is temporary. Building is allowed over any column with ground under it, up to a build height far over the terrain,
so the sky layer is the projection of the land onto the ceiling. And the kit's planks craft every defensive block.

## 4. What closes it, and what each measure changes

| Measure | In PGM | What it removes | What it costs |
|---|---|---|---|
| **Break only what was built** | `Build(break_only=("wood", ...))`: a block-break filter ahead of the void rule | pits, tunnels, the middle dug to bedrock: the dug phase is the built ground | no tunnelling; a defence builds walls rather than digging pits |
| **A ceiling at the terrain's top** | `maxbuildheight` a few blocks over the highest ground, or a roof the build height stops under | the sky layer: there is no height to bridge at that is not also ground | a board must give its height to the ground; a flat board has no game above it |
| **Void that is no build zone round the rooms** | leave the bays and holes out of `Build(areas=...)` | a sky route into a room by any face but its doors (match-flow §5) | the void must be designed: it is where the room is held from |
| **No crafting table** | `Crafting(disable=("crafting table",))` and none in the world | fences, fence gates, iron bars and stairs from planks: the anti-climb stairs, the gate crowns and the table walls | no player-made ladders or stairs; a board that wants them gives them in the kit |
| **Ground that grows back** | `Renewables([boxes], rate, avoid)` over the middle and the approaches | the pit and the desert, slowly, wherever nobody stands | a board whose ground keeps changing back under the players' blocks |
| **A time limit with a score** | the match's time limit and its result by objectives touched | the endless match | ends a match rather than shaping it |

**The first two measures are the ones that change what a door is.** With the rock unbreakable and the ceiling at the
terrain, every route to a goal is a route the map drew; the walls are fought at as walls; and the sky and dug phases
are the ground phase with building added, not a second map.

## 5. Under a roof

**The author ruled out the chain of chambers: a map is not made better by being moved underground.** Narrow
corridors are shut by the defence with a few blocks, a parapet over a shaft takes away the fall the shaft is there
for, and a mass of rock round an approach is something to build round unless the rock is the edge of play. What the
author's concept is instead is an image of a normal map under a roof, the same size as one.

**The concept is four exchanges, and `plan.bunker` makes them on any composed board.** The land is islands standing
in the void. A build region stays void, crossed by bridging, and a fall is a death. An enclosed void, the hole a
ring or a donut leaves, is a pillar of bedrock from the floor to the roof: the negative of the hole, stopping sight
as well as movement. The world outside is rock, the edge of play, with a moat of void along every shore.

**A generated board has one island a team, and a bunker lives from its gaps, so the board is cut.** The cut is the
generator's own isolation cut (model.md §6.2): a wool's approach and the frontline are each cut from the rest of the
team's land by two cells of void. A wool room is rock with its seal on the void, the land in front of it cut back.

**The author judged Frostvault, the first board drawn so, a miss, and three rules come out of it.** A pillar stands
alone in the void with a gap all round it, never on land, so a hole in the land is not a pillar. A defence wall is
not raised to the roof. And a layout for the concept is drawn from the void outward, not taken from the generator's
land with holes in it (`reports/frostvault.md` §6).

**The roof is the measure that closes the late game, and it closes it by construction.** The sky phase is building
on every column to the build height, and under a roof that height is 24 blocks over the floors: there is no sky
route that is not a bridge. The seal is the door, and only a blast breaks it.

## 6. What was measured

**`pgmvox.read.late` walks a goal in four phases:** on the ground as built; with the build zone bridged; with every
column that is not void built on to the build height, the sky; and with every block a player may break taken out,
the dug limit. In each it walls the room's doors and walks again: a door holds where the goal is then shut off.

The approach study (`freeform/lib/studies/approaches/`) lays all eight forms as the rejected chamber chains in one
block of rock, its roof at y 72, and walks each from its host's floor to its room under CTW's usual rules
(everything breaks, building to y 96) and held rules (nothing of the rock breaks, building to the roof):

| Form | ground | bridged | sky | dug, usual | door holds, usual | door holds, held |
|---|---|---|---|---|---|---|
| I, L, Z | — | — | 33, 52, 52 | the same | sky | sky, dug |
| scythe | 74 | 74 | 74 | 24 | ground, bridged, sky | all four |
| clamp, U, H, donut | 31, 38, 45, 66 | the same | the same | the same | ground, bridged, sky | all four |

**Under the usual rules a scythe's door is dug round in 24 moves against 74 walked; under held rules no door is
gone round.** The I, L and Z read nothing on the ground because their chains climb out of the host by more than a
step, which is a fault of the chamber layout and one more reason it was dropped.

The two bunker boards walk a team's spawn to the enemy's wool, the seal and its screen walled as the door:

| Board | Seal standing: ground, bridged, sky, dug | Seal blown: ground, bridged, sky, dug | Door holds |
|---|---|---|---|
| Coldstore, the author's quarter finished | not reached in any | —, 209, 209, 209 | bridged, sky, dug |
| Frostvault, a composed board as a bunker, the nearer wool | not reached in any | —, 243, 243, 243 | bridged, sky, dug |
| Frostvault, the farther wool | not reached in any | —, 348, 348, 348 | bridged, sky, dug |

**The sky is never shorter than the bridge, and nothing goes round a seal.** That is the roof and the bedrock doing
what the rules of §4 do on an open board, without a rule to state them.

On Hollowstack, red's walk from its spawn to blue's Vault monument, the Vault's 36 blocks of door walled:

| Rules | ground | bridged | sky | dug | door holds in |
|---|---|---|---|---|---|
| usual: every block breaks | — | 208 | 193 | 176 | bridged, sky |
| held: the kit's wood and glass break | — | 208 | 193 | 193 | bridged, sky, dug |

**On the ground the Vault is not reached at all, and that is the defence walls working:** no route crosses a
bedrock wall without a block placed. Under the usual rules the dug route is 17 blocks shorter than the sky's and
never passes a door; under held rules the dug route is the sky route, and walling the doors shuts the monument off.

**On an open board a ceiling barely moves the walk, and that is the point to take from it.** On Chantry Gill, red's
walk to blue's town monument:

| Rules | ground | bridged | sky | dug | door holds in |
|---|---|---|---|---|---|
| build height 70, the map's | — | 172 | 158 | 158 | the monument has no room |
| a ceiling at y 26, eight over the coast | — | 172 | 159 | 158 | the monument has no room |

The sky is fourteen blocks shorter than the bridge at either height, because it runs straight over the town rather
than round by the streets. What a high ceiling buys a team is not distance but height over the defence and a way
over a prepared line, and the walk does not price either. On a board whose goals stand in rooms, those are exactly
the door question: an open board answers it with its rules, an underground one with its rock.

## 7. What is open

- `read.late` prices digging at nothing: a dug block is air. It says whether a door can be gone round, not how long
  going round takes; a weighted walk would answer the second.
- The phases are limits, not a match. Population, the order things are built in and the fight at a seal are not in
  them; the recorded matches are the only measure of those (match-flow §6).
- How much TNT a seal takes, and whether ten blocks of void is the right cut, are numbers a played match gives;
  the author's recorded matches (match-flow §6) are the measure to hold them to.
- A ceiling per region (building allowed higher over a team's own base than over the middle) is a measure PGM can
  express with `apply block-place` over a region above a height; pgmvox does not write it yet.
