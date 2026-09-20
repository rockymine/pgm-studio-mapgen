# Eaveswick — a frontline with two floors

> A CTW board adapted from the composed board `players=12 symmetry=mirror_z seed=61`
> (hub `single`, frontline `bar`, wools `i` + `l`, score 5.806). The composed board puts one
> wool **29** blocks from its own spawn and the other **59** — a 2.03× spread, which is
> exactly the failure `WL9` is written against — and gives each approach a single road.

**In one sentence:** the frontline is a quay cut seven blocks down into a river terrace, and
the hub's own ground is carried out over it on a timber gallery, so the defence holds an
upper deck, the attack lands on a lower lane, and the only two ways between them are the
flank ramps the deck looks straight down.

100 × 140 blocks, `mirror_z`, three tiers: the quay at surface 12, a grazed shelf at 16, the
upland at 19; the gallery's deck at `y18`.

## What the composed board said and what was changed

| Composed | Here |
|---|---|
| spawn on the west flank, `x −30..−20, z 35..45` | moved to the **back centre**, `x −10..10, z 60..70`, marker at `(0, 65)` |
| wool-a deep behind the spawn at `x −5..5, z 55..65` (defend 29) | re-hung off the hub's **west** end, room at `x −50..−40, z 40..50` |
| wool-b out east at `x 25..35, z 55..65` (defend 59) | re-hung off the hub's **east** end, room at `x 40..50, z 40..50` |
| frontline `x −10..10, z 10..30`, flat with the rest | widened to `x −20..20`, deepened to `z 10..40`, and **cut down seven blocks** to surface 12 |
| `"walls": []` | one: `{"a": "quay", "b": "wool-b-t1"}` — bedrock two thick across the ten-block lane mouth from the quay onto the east spur, stamped `min 19,30 → max 21,40`, twenty blocks out from the room |
| no layers | three: `posts`, `deck`, `rail` |
| hub `x −15..15`, two pieces | one piece `x −20..20, z 40..55` |

The two rooms are now mirror images in `x` about the spawn, which is why the balance is exact
rather than approximate. What differs between them is not distance but **character**: the
west wool stands on an open grazed shelf a three-block flight below the hub; the east wool
stands on the upland behind a knoll and an approach wall.

## The second storey, and what the storey is

Three made layers:

| Layer | `base_y` | Holds |
|---|---|---|
| `posts` | 12 | twelve 2 × 2 dark-oak trestles, `y12..y17`, standing on the quay |
| `deck` | 18 | one slab `x −14..14, z 26..40`, the course at `y18` — so a player stands on it at 19, level with the hub |
| `rail` | 19 | the log rail along the deck's outer edge at `z 26` |

Measured: the void scan reads `2 101 cells open x −14..14 y 12..17 z 26..40` — six clear
courses of lane under a 29 × 15 deck.

In gameplay terms the storey is a **height that is not a detour**. The deck is continuous
with the hub at `z = 40`: a defender walks straight out onto it from their own ground and is
seven blocks above everything in front of them. An attacker off the crossing lands on the
quay, and the low lane **dead-ends** at the hub's face under the deck — the only ways up are
`ramp-w` (`x −20..−15, z 26..40`) and `ramp-e` (`x 14..19, z 26..40`), each fourteen blocks of
run for seven of rise, each at a flank, and both in the deck's field of fire. Transect up the
west ramp, `(−17, 22) → (−17, 46)`:
`rises 7, falls 1, worst step 1: 0 barrier, 0 scramble, walked end to end`.

The ground under the deck is unpainted by the surface bucket — one column resolves one band
stack and covered ground falls in the `fill` — so `quay`'s `fill` is a cell of gravel,
sandstone and andesite rather than plain stone, and reads as the shaded floor of an
undercroft rather than as bedrock.

## Relief

One group, base 19, reach 14, grain 1.3/15. Two flats are **stated** rather than solved:

- the **quay** (`area`, `h 12`, `x −21..21, z 9..41`), because the gallery stands on it and
  the crossing lands on it — no tread, flat to its edge;
- the **hub apron** (`area`, `h 19`, `z 39..50`), because that is where the deck lands.

What rolls: the knoll the east wool stands behind (`point`, `r 5`, `h 23`), the rise behind
the spawn (`point`, `r 6`, `h 22`), and two pushes — one over the east upland and a gentler
one on the west shelf.

**Excluded from the solve** (`relief_scope: "exclude"`): the three flights. Each carries a
`material` rather than a theme, because a flight is a thing somebody built and a theme is a
place.

Relief read: level **0.562**, largestField **0.340**, **7 faces**, 0 cliffs, 0 seams, 0 silent
marks. Incline: 46.5 % under 10°, 23.2 % teens, 12.3 % twenties, 8.4 % thirties, 9.6 % at 40°
or steeper.

## What it is painted with

Three themes — `upland`, `holm`, `quay` — on three tiers, with the `upland` surface a
`layered` material on the **`slope`** axis cutting at 18° and 32°. Ground family is a pale
river terrace: sand, gravel and sandstone under a grey-green `Extreme Hills` turf. Built
family is dark oak: the deck, the rail, the posts and the wharf shed. The accent is the
quay's smooth and chiselled sandstone.

`SK27` complains that one component compiles to three plateaus painting three themes. That is
the complaint to answer rather than dismiss, and the answer is that the three tiers are not
one landform with risers in it: they are separated by stated faces of three and seven blocks
with authored flights cut into them, and each is a different place — a wharf, a pasture and a
terrace. The failure `SK27` is written against is a theme *per piece*; this is a theme per
**tier**, and the board has three of each rather than thirteen and six.

## The numbers

| Read | Answer |
|---|---|
| `/plan/evaluate` | score **0**, valid; three `EL1` seam complaints, all answered by flights |
| `/preflight` | **export gate OPEN** |
| `/coverage` | reached 5 820, dead **0**, **0.0 %** |
| `03-slopes.txt` | 5 300 walked, 230 scrambled, 290 barrier; 10 faces, largest 86 |
| `06-claims.txt` | placed 26, declined **0** |
| `/plan/flow` before | attacker **113 / 137** (1.21×), defender **29 / 59** (**2.03×**) |
| `/plan/flow` after | attacker **143 / 140** (**1.02×**), defender **46 / 44** (**1.05×**) |
| relief read | level 0.562 / 0.340, 7 faces, 0 seams, 0 silent |

## What it does not say about itself

`/plan/flow` reports *"One way in, end to end: nothing forks and nothing merges"* for both
wools, and that is true of the **plan** and false of the board. The plan tier has no storeys,
so the split between the deck and the lane under it — which is the whole of what this board
is about — is invisible to it, as are the two flank ramps, which are authored shapes rather
than pieces. The reads that see them are `render/section`, the void scan, and
`walk` with a `y` in its `from`.

## What went wrong

**Nothing refused.** This was the board that went in first time: the plan evaluated at 0 on
the first `--dry`, the compile and the store raised only `SK27`, the dressing declined
nothing, and the export gate opened on the first build. The reason is that every number in it
— the seven-block cut, the fourteen-block ramps, the six courses under the deck — was
arithmetic done against a rule read out of `GET /api/rules` before the first shape, rather
than a figure adjusted after a decline.

**The one thing to watch:** `seats` answers only **40** house seats on this board at 11 × 9,
all of them on the quay, and 3 905 cells refused for `DR-KEEP`. Two wool rooms, a spawn and
two roads on a 12-player board leave very little ground a building may stand on.
