# Mootgate — a board made of placed things

Two walled market towns, 80 blocks wide and 76 deep, facing each other across a 28-block build zone
over void. Each town keeps its wool in a moot hall at the back of the green; the enemy has to cross
the void, come through one of three gates, up a street plan, over the market square and across the
Moot Green to reach it. Capture the Wool, two teams, `rot_180`, 24 a side.

The ground is nearly flat on purpose. Everything a player reads inside the walls is a **placed
thing**: 18 house props a side over five house styles, two stamped rooms over two more, four paved
routes, and a town wall, two stair flights, two gate towers, a market cross, a wool stone and a town
well authored as terrain.

| | |
|---|---|
| slug | `opus5-mootgate` · name **Mootgate** · created 2026-09-03 |
| extent | x −40..39, z −90..89 · land z 14..90 a side · crossing z −14..14 |
| objective | one wool a team, defended in its own moot hall, captured by the other |
| spawn | red (24, 15, 77) yaw 90, its door on the −x face |
| wool | red (−23, 15, 77), inside the moot hall's shell x −29..−17, z 73..81 |
| buildings | 20 a side (18 props + moot hall + barracks), 40 on the board |
| themes | `vale` 71.3% · `rampart` 14.9% · `cobbles` 13.9% |

## The three numbers

```
03-slopes.txt   cells: 9836 walked, 106 scrambled, 2218 barrier; faces: 10, largest 808 at x -37..36 z -89..-29
06-claims.txt   placed 93, declined 0
04-routes.txt   raid 154 blocks / 43 placed straight; 177-220 / 20-21 by a gate  (taken by hand)
```

The 2,218 barrier cells and the 808-cell face are the two town walls, and they are the board. Inside
the ring every cell is `.` — the town is dead flat at y14 so that eighteen buildings a side can stand
on it. `preflight` ends **export gate OPEN**; coverage reads 10,757 reached, 592 decorated, 811 dead
(6.7%), the dead patches being the four corners behind the walls.

## How it is meant to play

The field between the crossing and the gate is open ground with a mere in a hollow under a knoll, a
steading, a tithe barn, a chapel, a cot, a wood and four erratics — cover for an attacker forming up,
and nothing a defender can stand behind. Three gates cut the front wall: the main gate at x −5..4
between two towers, and a postern at x −24..−19 and x 19..23. A lane runs in from each and they meet
on **Market Row** at z=44.

Behind Market Row is the **square** — 22 × 14 blocks of trodden ground with the market cross at its
middle, the town well beside it and three market stalls round it. The square is where a captured wool
is carried: the **wool stone** at x 7..9, z 47..49 is the plinth the author intended as the capture
point (see *What went wrong*).

North of the square the town thins into the **Moot Green** — the ten blocks the dressing pass keeps
clear of a wool-room door, which is a killing ground nobody had to draw. The moot hall stands in it
with a door cut on each of its four sides, because the piece abuts land on all four and every land
seam is an entry. A team may not enter its own wool room (PGM's own rule, written out as
`<apply enter="not-red" region="reds-woolrooms">`), so the defence is fought on the green and in the
streets, never inside the hall.

The barracks sit in the north-east corner with their door facing west, into the town rather than out
of it, so a defender leaving spawn arrives behind the green instead of on top of it.

## What the ground is made of

Three families, named before anything was painted. **Ground** is green and grey: `vale` is grass over
dirt over stone with a voronoi of stone and andesite in the fill, where a voronoi belongs; `cobbles`
is two greys of one shade — gravel into cobblestone at a noise period of 11 — laid as the square, the
moot avenue and four worn yards. **Built** is the buildings: whitewash (white stained clay), dark oak
timber and a cobble plinth, roofed in brick or spruce shingle with a dark oak verge. **Accent** is the
civic stone brick of the town wall, the moot hall, the market cross and the wool stone, weathered by a
two-block noise field of stone brick into mossy stone brick.

No building is walled in the ground's own family, and the only pattern anywhere on the surface is a
two-stop noise. Everything else is a **shape**: the square and the yards are one-course paint patches,
not a sampled field.

## The seven house styles

| style | is | what it demonstrates |
|---|---|---|
| `croft` | one storey, whitewash between dark oak posts, spruce shingle gable | the plain case, 7 of the 18 |
| `townhouse` | two storeys, cobble under a jettied half-timbered upper, brick gable | a `checker` of plaster and dark oak as half-timbering, and `beams` as the jetty |
| `store` | one tall volume, spruce boarding, shed roof, `slabBanded` windows | a `laidLog` eaves course; the granary is an L |
| `forge` | brick over cobble, hip roof stepped in brick slab, open working porch | `porch` with `roof: shed`, and a `slab` of the roof body's own material |
| `stall` | three courses of wall, lean-to over a railed deck | the smallest thing sayable: 5×5, the `DR-SIZE` floor |
| `hall` | the wool cage — stone brick with a mossy band, arched windows, hip roof in brick | `door: web`, which is what the wool room's break rule takes |
| `barracks` | the spawn cube — cobble under stone brick, shingle gable | the same stamper, a different room |

All seven previewed at 200 in section before the world was built. The two multi-wing buildings — the
granary (hall 9×10 + wing 5×5) and the inn (hall 7×10 + wing 4×7) — went through
`POST /terrain/prop-preview` with the theme they stand on, which is the only view that draws an L.

## The techniques, and what each one bought

**The town wall is terrain, not a prop.** Seven rectangles at `override: true`,
`height_mode: "level"`, `skirt: 0`, `relief_scope: "exclude"`, `keepClear: true`, `base_height: 23` —
a sheer 8-course ring over ground at y14, with three gaps cut in its front face. `keepClear` is what
makes it safe to build a town against: an authored shape carrying it joins the dressing keep-out with
no margin, and a boulder that leans on it is declined `DR-KEEP` rather than eaten.

**The two stair flights are one tilted quad each.** `x −11..−8` and `7..10`, `z 33..48`, four
`anchor_heights` running 23 → 16: 16 blocks of run for 7 courses of rise, which is the 2:1 a flight
has to keep. `03-slopes.txt` reads them as `##..##` — the two middle columns walk, the edges are the
drop off the side.

**The market cross, the wool stone and the town well are terrain too**, because there is no prop kind
below a 5×5 building. The cross is three stepped squares and a 1×1 shaft to y24; the well is a
four-rectangle ring two courses proud round one open column at (−4, 57).

**The moot avenue is paint, not paving.** A `stroke` is a prop, and any route laid inside a wool
room's door approach is declined `DR-KEEP` whole. So the avenue to the hall is a one-course `add`
carrying the `cobbles` theme — the same picture, and no rule to argue with.

**The relief does almost nothing, and that is the design.** Four marks: an `area` at h15 over the
whole town, a knoll at (−31, 21) h17, the mere's pan at (−33, 20) h12, and a swell at (37, 20) h16.
`relief/read` answers 11,948 walk steps against 40 barrier and 16 scramble.

## What went wrong

**The capture point is not where the board says it is.** The wool stone on the square exists, its top
is at y15 and the block above it is clear — and the exported `map.xml` writes
`<block id="red-blue-monument">-20,16,-80</block>`, inside blue's spawn room. Stating the monument
through `POST /wools/red/monuments` and again through `PUT /intent` stores it in both documents and
changes nothing in the world. The map ships playable, with the derived monument.

**The moot hall has four doors.** A wool room's entries are every land seam it presents, and the
piece abuts land on all four sides because it has to — a room with void beside it fills that face with
bedrock to y0. A market hall with four doorways is defensible from the green rather than from inside,
which is the reading this board takes, but it was not a choice the author got to make.

**The board is a third bigger than the corpus would size it.** 6,080 blocks of land a team at 24 a
side is 253 blocks per player against `G8`'s ~184 saturation. A walled town with a street plan does
not compress, and the trade was taken deliberately.

## Coordinates

| thing | where |
|---|---|
| town wall | front z 29..31 (x −36..−24, −18..−5, 5..18, 24..36) · west x −36..−34 · east x 33..35 · back z 85..87 · top y22 |
| gates | main x −5..4 · west postern x −24..−19 · east postern x 19..23 |
| gate towers | x −9..−6 and x 5..8, z 27..34, top y26 |
| stair flights | x −11..−8 and x 7..10, z 33..48, y22 → y15 |
| market square | x −11..10, z 47..60 (`cobbles`) |
| market cross | steps (−3..3, 47..53) y15 · (−2..2, 48..52) y16 · (−1..1, 49..51) y17 · shaft (0, 50) y24 |
| wool stone | x 7..9, z 47..49, top y15 |
| town well | ring x −5..−3, z 56..58, top y16, open column (−4, 57) |
| moot hall | piece x −32..−14, z 70..84 · shell x −29..−17, z 73..81 · wool (−23, 15, 77) |
| barracks | piece x 16..32, z 70..84 · shell x 18..30, z 73..81 · spawn (24, 15, 77) |
| the mere | pool about x −38..−28, z 15..26, bed 2 deep |
| observer | (0, 30, 0) — the magenta cube in the middle of every render is its bedrock plate |
