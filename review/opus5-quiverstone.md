# Quiverstone Mesa — a badlands DTM, and a pinnacle that is a made thing on purpose

> A destroy-the-monument board in badlands colour: two banded buttes standing over the camp, an
> obsidian pillar a team on open caliche between them, hoodoos on the pan, and one sandstone reef in
> the middle that both sides pay to bridge to.

**In one sentence:** a dry mesa shelf where each team's two obsidian pillars stand on pale caliche
between two erected clay buttes, and the one reef between the sides is reached over twenty blocks of
wash.

156 × 216 blocks of rendered extent over a 140 × 200 plan, `rot_180` about the origin, base surface 16,
ground y13..y35, hoodoos to y40. Three landmasses: two team shelves (`shelf`, x −70..70, z −100..−40)
and one mid reef (`reef`, x −50..50, z −20..20), joined only by a build zone over the wash
(x −60..60, z −40..−20, fanned).

## The board

The camp sits at `(0, −90)` on a pad pinned at y20 with two pueblos and two assay offices on it. Two
tracks of gravel-and-red-sand leave the door and step down four pinned courses to the pan at y16, one
to each monument. The two monuments stand at `(±24, −54)`: **46 blocks of walk from their own camp,
0 placed blocks**, and 152–154 from the enemy's, of which **23–27 are placed** — the wash crossing.
Read against its own mirror the board is fair to a block.

Two monuments a team rather than one, for the reason `opus5-alderfen` measured: a single central goal
puts every journey down `x = 0` and leaves both 140-block flanks off every route. They are 48 apart,
which is `GO2`'s band, and the arrangement `docs/gameplay/approaches.md` states for a multi-goal board.

What the ground round each monument does: **open caliche** on its own pan (nothing within 10 blocks of
a marker), an **erratic** on its outer flank to hold behind, a **dished wash** across the front that a
player drops into, an **erected butte** behind the camp that an attacker climbs to bridge from, and
the two **assay offices** and **pueblos** on the pad above to fight back through.

## What the ground is made of

Five grounds, and the shares are what say one is the ground and three are splotches.

| Theme | Share | On | Says |
|---|---|---|---|
| `pan` | 73.6% | everything not otherwise stated | sand with gravel and orange clay as a `noise` field's two end stops, over three courses of sandstone at `rise: 8` |
| `scree` | 11.0% | four patches over the shoulder and edge pushes | red sand, orange clay and gravel in a `cell` at cellSize 8 |
| `caliche` | 7.1% | one patch a monument | white and light-grey clay over smooth sandstone — pale, so an obsidian pillar reads against it |
| `butte` | 7.0% | the two erected buttes and the six hoodoos | the strata: a **seven-band `layered` stack** in `surface`, `wall` **and** `fill` |
| `wash` | 1.2% | the dished channel | gravel and sand: what a river left when it stopped running |

The strata are the board. `PAN_WALL` is one `layered` material — sandstone, orange clay, hardened clay,
brown clay, hardened clay, light-grey clay, then stone — read down from the top of the bucket, and it is
the `wall` bucket of every ground theme. So every cut face on the board, coast and butte and hoodoo
alike, shows the same beds at the same heights, which is what a badlands actually looks like. Putting it
in `fill` as well is what makes the buttes banded all the way down rather than banded in their top four
courses: the surface bucket is only the top courses, and the face is the whole point.

## The techniques, and what each one bought

**A butte is an erected terrain shape; a hoodoo is a made thing. The difference is the build ceiling.**
Both are the pillar idiom — `height_mode: raise`, `skirt: 0`, `relief_scope: exclude`, sheer on every
side. But the ceiling is `BuildCeiling.Of(highestGround) = tallest terrain column + 20`, and an erected
shape *is* a terrain column, so a 20-course pinnacle beside a monument would hand the whole board a
ceiling 20 blocks over its own top. A `made` layer is out of that reckoning — and out of
`BuiltTerrain.Ground`, so nothing seats on one. So the two big buttes, which are meant to raise the
ceiling because they are the thing attackers bridge from, are terrain at `raise: 16`; the six hoodoos,
which are cover on the pan and nothing more, are three made slabs each carrying `seat: "ground"` and a
shared `part_of`, which settles the whole pinnacle onto the terrain as one thing.

Read at `(-66, -62)`: brown clay y37–38, smooth sandstone y35–36, orange clay y33–34, brown clay
y31–32 — the strata running the hoodoo's whole height. At `(-52, -86)`, the butte: orange clay y42–43,
sandstone y40–41, hardened clay y35–37, brown clay y33–34.

**A copied acacia is how a dead bush gets under a tree.** The template species grows an acacia; what it
cannot do is put a block that is neither wood nor leaf into the same recipe. The four copied bodies here
are a leaning trunk, a flat umbrella crown, one stripped laid limb, and two dead bushes at the foot —
one placement, and the ground cover comes with the tree rather than being scattered near it.

**Everything else is `opus5-alderfen`'s, applied without paying for it again**: pinned pads as
`lobed_box` rather than ellipses, buildings only on pinned ground with two clear columns between their
stamped extents, props at least eight apart and five and a half off a road's centreline, made things
clear of every building's columns, coasts drawn with `bendShapes` at `wander: 6` and every prop within
ten blocks of the old coast moved inward, and `maxPlayers` read as per-team.

## What the pass refused

**`DC3`: obsidian is worth at most three blocks.** A `column-plus` destroyable is fifteen, so the studio
built both monuments in **ender stone** and said so — a complaint on a 200, and the map.xml declared what
was actually laid. The rule's own fix names the pairs: obsidian for a pillar, ender stone or gold or
emerald for a cube or a column. `pillar-3` in obsidian is what shipped, and a slim black spire on white
caliche is the better silhouette anyway.

**`HS3`: a bare log is not a roof material.** The pueblo's verge was `solid(162, 0)` — *a bare log, which
has no axis and stands every one of them on end, a sawn face out at whoever looks at the slope*. Laid
(`kind: laidLog`) it takes the ridge's own axis.

**A `Storey`'s `deck` is a bare `TerrainMaterial`, not a `{stack, extent}`.** Handed a band stack it is a
**500** whose only diagnostic is in the server log: *the JSON payload for polymorphic … TerrainMaterial
must specify a type discriminator. Path: $.shell.storeys[1].deck*. The same field cost the same 500 on
`opus5-alderfen`, where it was worked around with `deck: null` rather than understood.

**`DR-CUT`: a prop seats clear of what it then reaches into.** Two acacia placed at `(∓60, −76)` stood
inside a butte's own sheer footprint and lost 55 of 108 blocks to the clip. The finding says exactly
that — *7 of its blocks are inside something already standing and were not written, and that cut 48 more
off its own footing* — and names the first column it stopped at.

**A reef 100 × 30 doubled by the fan is not room for fourteen footprints.** Three shrines, three acacia,
a boulder and two beds, each with a rot_180 image, could not be placed without one of them standing in
another's image. It carries two shrines, two acacia, a bush bed and a bone pile now. The trap worth
naming: **a prop must clear every other prop's own orbit image, not only the props as drawn** — an
acacia at `(26, 10)` was declined by a *tree at* `(-28, -10)`, whose image is at `(28, 10)`.

## Not a fault

**The red and blue wool three courses high over each monument, and the two coloured dots in the
isometric.** `GoalMarkerStamper` *stamps a small coloured marker high above a goal — a wool room, a
destroyable or a core — so a player can see where it is*. At `(-24, -54)` it reads Red Wool y69–71 with
the monument's own obsidian at y20–22. It is the same class of thing as the magenta observer bedrock the
brief warns about: deliberate, and not something to go looking for the cause of.

## Open gameplay questions

- **Two monuments a team, 48 apart, on a 140-wide board.** Same question `opus5-alderfen` left open: the
  measured case for splitting the goal is strong (it is what makes the flanks used) and whether a
  16-a-side team can hold two is played rather than measured.
- **The wash as the board's only depression.** Three courses of dish across the pan's front, which
  `approaches.md` names as the entrance from below in place of a hole cut in a team's own ground.
  Whether three is enough to read as one is worth a look in game.
- **A hoodoo is climbable and unbridgeable-from.** Being a made thing it does not raise the ceiling, so
  a player standing on one cannot build up from it as high as from the butte. Whether that asymmetry
  between the two rocks reads as deliberate is the author's.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| red spawn point | `(0, 20, -90)` | on the pinned camp pad |
| red monuments | `(-24, -54)` and `(24, -54)` | obsidian y20–22 over red sand y15, `pillar-3`, float 4 |
| the crossing, at `x = 0` | shelf front z −40, reef back z −20 | 20 blocks of wash; build zone z −40..−20 |
| the two buttes | `(-52, -86)` and `(52, -86)` | erected, `raise: 16`, top y43, strata y33..y43 |
| the six hoodoos | `(-66, -62)` · `(-30, -74)` · `(-6, 12)`, and their rot_180 images | `made`, `seat: ground`, 20 courses, top y38 at the first |
| goal markers (not a fault) | `(±24, -54)` at y69–71 | team wool, `GoalMarkerStamper` |
| largest barrier face | `x 39..66, z -98..-76` | 134 cells — the east butte's own shoulder |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0.71**, `valid: true`. One soft term: `LN2 max-chain-length 140 outside [25, 110]` — the lane lint reading a landmass as a lane |
| `POST /plan/inspect` | `mon-w` own 45 / enemy 148, **ratio 3.29**; `mon-e` own 43 / enemy 150, **3.49**. Own pair 48 apart. Island gap **20** |
| `POST …/sketch/relief/read` | `team` 9 513 cells, low 13, high 35, **relief 22**, symErr **0**; `neutral` 4 627 cells, low 15, high 17, relief 2, symErr 0 |
| `03-slopes.txt` | 20 450 walked · 2 297 scrambled · **906 barrier** (3.8%); 20 faces, largest 134 |
| `06-claims.txt` | **placed 48, declined 0** |
| `04-routes.txt` | own camp → own monument 46 blocks, **0 placed**; enemy camp → monument 152–154 blocks, **23–27 placed**. All eight walked end to end |
| `05-themes.txt` | 5 themes, 13 distinct surface blocks; largest border `pan | scree` 522 cells |
| `GET …/preflight` | export gate **OPEN** |
| `GET …/coverage` | reached 10 620 · decorated 3 557 · **dead 9 476 of 23 653 = 40.1%**. Higher than Alderfen's 36.7% for one reason: a badlands is deliberately bare, so `decorated` is 3 557 against 6 819 — the same reached ground, less of it dressed |
| provenance | 24 trees · 12 houses · 6 boulders · 4 strokes · 4 destroyables · 2 spawns |
