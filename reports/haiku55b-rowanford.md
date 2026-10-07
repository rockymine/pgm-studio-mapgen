# Rowan Ford — run report (Haiku 5.5)

## What I set out to build

A destroy board for two teams, 16 a side: **an autumn river valley**. A slow river runs across the board between
the two sides, a watermill stands on each team's bank, one monument a team, real relief, at least three buildings
a team, and one place players can use below ground. The plan is authored (`specs/haiku55b-rowanford/build-spec.py`
writes it), the map is `Rowan Ford`, the slug `haiku55b-rowanford`, credited to Haiku 5.5.

**Identity sentence (written before any request):** a golden valley on dry Savanna ground, a team's spawn on a flat
back crest, a monument on the near bank in front of it, and a sixteen-block void river between the banks, crossed by
a build zone that runs the length of the board.

**What the finished board does not deliver:** the relief is almost flat (a four-block step, walked end to end), and
the below-ground place is not in the world. Both are stated in the review and below. The river is a void gap, not
water.

Deliverables: `maps/haiku55b-rowanford/`, `specs/haiku55b-rowanford/`, `review/haiku55b-rowanford.md`, a row in
`BOARDS-BUILT.md` under *Haiku 5.5 — the haiku55b run*, and this report.

## How the layout was chosen

I read the seven destroy layouts in `destroy-layouts.md` and the author's account in `approaches.md`.

- **Side islands and a middle; a rim round a basin; a tour widened into land; a box cut by water, walled by
  mountains; a long lane of rolling ground; islands in a box; rings in water.** I took none of them whole. The
  nearest was *islands in a box*, two landmasses across a gap, and the nearest to a straight-ahead goal of the seven
  (45° ahead, 11 aside). The rest were ruled out for the reasons below.
- **The long lane** is the closest in spirit: rolling ground, a river, spawns at the high ends. Its spawn sits 90
  blocks of land behind it, which needs a board much longer than 16-a-side work wants, so I took its river and
  dropped its scale.
- **A spawn in the land at its back** is the corpus rule. I departed from it. The spawn is two blocks in from the
  board's edge (measured below). See *Open gameplay questions*.

What in `ORDER-OF-WORK.md` §1 decided it:

- *the board's identity in one sentence* was written first, and it asked for a river between two grounds, which is
  a void gap bridged, not an island arrangement;
- *a goal's position is a walk, and the studio gates it*: GO1 needs the enemy walk to be three to four times the
  own walk, which needs the two spawns about 150 blocks apart. That set the board's length and so the spawn's seat;
- *the biome is decided now*: Savanna (id 35) for a golden ground;
- *the objective stands in front of the spawn and off to one side*: each monument is off the spawn-to-enemy line.

**The spawn's seat, as measured** (the report's transect through spawn-0 along x, and the walk from it):

| Measure | Brief / corpus | Here |
|---|---|---|
| land behind the spawn | corpus median 20 blocks | 2 blocks, to the board's edge at x −84 |
| highest ground within 20 blocks, above the spawn | corpus median 8 | 0 (the crest is flat at y13 from x −84 to −65) |
| what stands beside it | rock, a mine, trees | the spawn room's own house, `spruce-roofed-oak-cottage`, in a 20 × 16 room |

**Each goal's distance ahead of and aside from its spawn** (spawn-0 at (−80, 0) in the walk reads):

| Goal | Ahead along x | Aside along z | Walk from spawn-0 |
|---|---|---|---|
| monument-0, own, at (−61, −38) | 19 | 38 | 46 blocks, 0 placed |
| monument-1, enemy, at (60, −38) | 140 | 38 | 156 blocks, 16 placed (the river crossing) |

The own walk (46) and the enemy walk (156) give GO1 a ratio of 3.39 in the walk and 3.33 on the plan. GO4 (own walk
at least 40) and GO3 (enemy walk at least 85) both pass.

## What the run cost

- **Wall time:** about eight minutes on the sandbox clock, from the first real drive's start to the thirteenth drive's
  finish. That clock did not agree with the sequence of drives, so I do not stand behind the figure; the drive logs in
  `/home/user/scratch/drive*.log` are the record of each store.
- **Stores:** 13 real stores, each a single `PUT /map/haiku55b-rowanford/source` that carries the plan, the relief,
  the themes and the dressing together. So the plan and the relief were each stored 13 times. Twelve of the thirteen
  stores completed an export: the twelfth store was accepted (200), but its export was refused (`RQ1`, the biome
  written as a string), and the thirteenth store, with the biome as an object, exported.
- **Dry runs:** about sixteen (`--dry`), before each store and while I tested single fields.
- **Refused stores (dry, nothing written), by rule id:**
  - `PL12` — the on-axis river bed joined mirrored pieces into one island (422);
  - `DR-DOC` ×4 — a house style named but not stated in `dressing.styles` (400), and three door `front` values
    (`right`, `+x`, `east`) the field did not take (400);
  - `PT4` — a cell pattern on the wall with no rise (400);
  - `SK13` — a crypt add filled the columns a shaft subtract takes away (422).
- **The three numbers, from the final store (`drive.py`):**
  1. `ground 13376 walked, 0 scrambled, 0 barrier — 0.0% steps further than a player walks`
  2. `props 6 placed, 0 declined`
  3. `routes worst step 0, on route spawn-0 to destroyable-0`
- **Declines and complaints on accepted stores, by rule id:** `LN5` on every store (33% of the ground is off every
  route; accepted); `SP2`, `WX4` and `WX11` on the spawn room (fixed); `WX13` and `WX14` on the spawn room's size and
  house (fixed); `HP2` ×6, a house wing with four corners (fixed); `DR-CLAIM` ×3, the authored mirrored houses
  colliding with the symmetry's fan (fixed); `DR-PASS` on the mill and the store (fixed); `DR-KEEP` on a lookout that
  sat on a walk or in front of a door (fixed after four moves); `OB19` on a lookout inside the monument's clearance
  (fixed). The thirteenth store declines nothing.

## What I could not say

Each item says what I wanted, what I tried, and whether the capability is missing or only out of reach from where I
stood.

1. **A place below ground** — what I wanted: a room under the west bank with a shaft down to it. What I tried: (a)
   a made storey with `below: true`, which was accepted but painted as stone, so no room; (b) a subtract for the room
   and a subtract for the shaft, which the store accepted and which cut every column down to the void, bedrock
   included (`column` at (−45, −28) read zero blocks at every height). The studio's `techniques/cutting-a-hole`
   card says the room is a floor layer under a stated void with a ceiling layer over it, and that a subtract takes
   the column down to void. I did not build the three-layer form. **Verdict: out of reach from where I stood.** The
   mechanism exists; I did not get it to land inside the run. The final map has no below-ground place.
2. **A river with water in it** — what I wanted: a slow river, water in a bed. What I tried: a void gap, with no bed.
   The water card says a fluid carves against a layer it names, and a void has none. I did not try a bed shape
   (`addShapes`, neutral group) under the water, because the on-axis bed piece was refused as `PL12`. **Verdict: out of
   reach** — the bed shape is the untried route.
3. **Relief with sides** — what I wanted: a valley whose sides rise. What I tried: a raised crest and a flat bank, with
   three area marks and no pushes. I reasoned that a higher crest would put a cliff under the monument pad, and kept the crest flat; I did not test a higher one. The studio has
   pushes, lines, `tread` and `batter` for exactly this (`techniques/marks-and-pushes`, `relief-on-shapes`); I did not
   use them. **Verdict: out of reach — I did not exercise them.** Not a missing capability.
4. **A door's `front`** — what I wanted: the lookout's door on a named wall. What I tried: `east`, `right`, `+x`, each
   refused by `DR-DOC`. The schema describes `front` ("which wall the door is cut through") but does not list its
   values. **Verdict: possibly mistaken — the value set is not in the description I read.** I left it unset.
5. **A spawn in the land at its back, with the enemy walk still at three times the own** — I found no way to keep
   both on a board of this length. This is a geometric trade (GO1 against the spawn's seat), not a missing capability,
   and it is an open question below.

## What I got wrong, and why the wrong claim looked right

- **A river as a neutral bed piece.** It looked like the way to get a river. Piece `mirrors: false` on the axis is
  how the spec says a centre piece is neutral; it does not allow a piece on the axis to touch mirrored pieces (`PL12`).
- **Two spawns 104 blocks apart.** The first dry run put the monument's GO1 ratio at 2.16 (own walk 38, enemy 82). I
  had assumed the spawns' separation was the only lever on the ratio and that the monument could sit anywhere on the
  bank. Widening the board so the spawns are about 150 blocks apart brought the ratio to 3.3.
- **Four-corner house wings.** The wing takes "exactly two opposite corners" (`openapi.json`, `AuthoredWing`). I wrote
  a rectangle as four points, which the studio read as corners 0 and 1, a 9 × 1 wing (`HP2`, six declines). I read the
  schema after the declines, not before the first store.
- **Authoring the team-1 houses.** `mirror_x` fans a dressing prop onto the second team by itself. My explicit copies
  collided with the fan (`DR-CLAIM`). One rule: author the team-0 building and let the symmetry place the other.
- **A below-ground storey carves.** I believed a made storey under the ground would be air inside stone. The layer
  is painted as its own material, and the stone of the bank is not removed by it.
- **A subtract with a floor.** I believed `floor` and `base_height` on a subtract bounded the cut. The card says a
  subtract takes every column to the void, and `column` showed it. The store had accepted it at 200. Only the column
  read found it.
- **The biome as a string.** `"biome": "Savanna"` looked like the form `terrain/biomes` names. The field takes a
  `BiomeField` object, `{"kind": "solid", "id": 35}`.

## What worked first time

- **The dry-run then drive loop.** Every store that the dry run accepted exported on the drive, and every dry run
  refusal named a rule id whose fix was the next edit.
- **The plan grid.** `board.py` on the plan, before any store, showed the highland, bank and gap as rectangles, and
  the fault in the first plan (the on-axis bed) was visible in it.
- **The GO1 read in the dry run.** `GET /rules/terms` printed the own and enemy walks as the goal ratio, so each
  spawn move was one line of feedback.
- **The `column` read at the end.** It found the crypt's void hole, which no store, preflight or export reported.
- **The spawn-room mechanics.** Once the spawn room was its own piece and its own house, SP2, WX4, WX13 and WX14 all
  cleared in one edit.

## Open gameplay questions

These are decisions I made without an oracle, and I list them so the author can overrule them.

1. **Is a full-length build zone over the river the intended crossing?** I chose a zone over the whole 88-block
   depth of the void. `approaches.md` says a river "forces a bridge"; the brief says the two sides are joined by a
   build zone "spanning the board's whole width". Every point of the river is bridgeable. The alternative is a zone
   at one or two crossings, which would make the river a choke point. **Decided:** the full length.
2. **Is the spawn at the board's edge acceptable?** `approaches.md` puts the spawn in the land, up to ten blocks in.
   Here it is two blocks in, because of GO1. **Decided:** the edge, and the trade is recorded here rather than hidden.
3. **Is the monument far enough from the spawn to be the defended objective?** The own monument is 19 blocks ahead of
   the spawn and 38 aside, at the north corner of the bank. A defender stood at the spawn sees it at about 40 blocks.
   **Decided:** kept, because GO4 needs at least 40 of own walk and a monument nearer the spawn drops GO1 below three.
4. **Is a dead flank acceptable on a destroy board?** `coverage` reads 30% dead, almost all of it the two south corners
   behind the stores, z 28 to 44. `approaches.md` treats a dead flank on a destroy board as a note, and capture boards
   as a fault. **Decided:** kept.
5. **Is a void river, with no water, the right river?** A void reads as a gap a player bridges. A river of water would
   be walkable with a bed under it and would not force a bridge. **Decided:** void, because the approaches law wants a
   bridge there.
6. **Is relief this flat a valid autumn valley?** The brief asks for sides; the board has a four-block step. I did not
   run a second relief sketch (`ORDER-OF-WORK.md` §3 asks for three or four). **Decided:** flat marks, and this is the
   first thing a second run should change.
