# Kilnhold — the report

**A Destroy the Monument and Capture the Flag board in a volcanic caldera, built overnight by a competitor agent to a
rough brief.** The agent could not write this file itself, so its report is set down here as it returned it, with
the read-back taken afterwards added at the end.

## Story and concept

**A Cold War geothermal station built into the rim of a volcanic caldera.** Two concrete bunkers face each other
across an ash plain with a lava-lake crater in the middle. Each bunker is a rock massif with a stone-brick
gatehouse, a roof deck (the Crown), a gate hall, and machine halls two levels down where lava glows under iron
grates.

## Mode

**Each team has two floating obsidian monuments and one flag.** The Crown Beacon stands in a sunken court on the
roof, and the Pump Hall Monument over a grated pool; both are 3 by 3 by 3 with four blocks of air under them. The
flag stands on a dais in the turbine hall's shrine, and a team captures at a net over the capture dais in its own
gate hall. Three captures win, otherwise the monuments, within 40 minutes. The library's `Flag` writes neither
nets nor the pickup filter, so `mapxml.py` adds both.

## Layout

**140 by 200, half-turn symmetric, red north.** The levels are the Crown deck at 77, the galleries at 70, the gate
level at 65 (the muster hall with the spawn, the spine, the gate hall, the workshop, the command post) and the deep
level at 57 (the pump hall, the turbine hall and shrine, the cross gallery, the culverts). Levels meet by slab
ramps rising half a block a cell. Outside stand the facade with pilasters stepped out and panels recessed, the
apron, the cooling tower, the quarry pit, the ramps to the Crown, and the crater.

## Approaches

| Objective | Ways in |
|---|---|
| the Crown Beacon | the west ramp from the lane (open), the crown ramp from the gate hall's gallery (covered), across the deck from the east |
| the Pump Hall Monument | the west descent from the gate hall, the west culvert through the cooling tower (two bends) |
| the flag | the east descent, the east culvert from the quarry pit |

## Palette

**Ash ground, bone-grey concrete, hazard orange.** The ground is grey and black stained clay with coarse dirt and
scoria; the buildings are stone brick, polished andesite, andesite, dark oak, iron and coal; the accents are hazard
orange, lava, glowstone, sea lanterns and team wool. Blue clay reads purple in the textured renderer, so the teams
use wool.

## Numbers

| Measure | Target | Plan | Built |
|---|---|---|---|
| spawn to each own goal | 40 to 90 (GO4) | 73 / 71 | 67 / 65 |
| enemy walk over own, each destroy goal | 3 to 4 (GO1) | 3.27 / 3.06 | 3.42 / 3.22 |
| a team's two goals apart | 35 to 65 (GO2) | 108 | missed |
| opposing goals apart | 85 to 150 (GO3) | about 300 | missed |

**GO2 and GO3 miss because a roof goal and a deep goal are two ramps apart and the board is long.** A spiral flue
from the Crown to the pump hall would bring GO2 to about 74; it is not built. The half-turn comparison disagrees at
no place, the objective check and the footing audit report nothing, and the studio's parser reads the map.xml as
valid.

## What did not work

- No way up the cooling tower's ring, a smooth slab underside, sparse boulders and trees, speckled steep ash slopes.
- The lining first lined air cells, and a first build walled the gate shut; the walk caught it.
- The descent door was blocked by the gallery wedge until the deck stood on piers.

## The read-back taken afterwards

**220 blocks stand apart from the board: 120 pieces of dead-tree log, six of glowstone, and a few planks and stone
bricks.** The trees' arms meet their trunks at a corner, not a face, so in the game they hang in the air. The
monuments float by design and are not counted.

**Its world was first written to `maps/mixed/kilnhold_pgmvox`,** the name `pgmvox.run` falls back to when the
plain one is held, most likely by a row an earlier run registered under a doubled path (the other competitor's run
did exactly that). The world is now `maps/mixed/kilnhold`, and `pgmvox.run` refuses a
folder with no `scripts/` in it.
