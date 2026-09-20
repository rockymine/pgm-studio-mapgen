# Burrowgate — the defence rotates underground

> A CTW board adapted from the composed board `players=12 symmetry=rot_180 seed=65`
> (hub `twin`, frontline `bar`, wools `i` + `l`, score 3.964). The composed board is §2's
> fault in its clearest form: the attacker walks **129** blocks to one wool and **175** to
> the other, a ratio of **1.36**, and the defender **30** and **48**.

**In one sentence:** two wools sit on cut shelves five blocks below a flat-topped hill, and
a gallery runs the hill's whole length between them — forty-eight blocks of covered rotation
under the ground the match is being fought over.

90 × 140 blocks, `rot_180`, hill at surface 16, shelves at 11, frontline at 15, spawn at 17.

## What the composed board said and what was changed

| Composed | Here |
|---|---|
| hub bar `x −5..30, z 40..50`, ten blocks deep | twenty blocks deep, `z 40..60` — which is what gives the gallery under it a roof wide enough to be a place and the two ramps somewhere to run |
| wool-a hung off the bar's west end at `x −20..−10` | a shelf five blocks down, `x −30..−5, z 40..60`, with the room at `x −40..−30` — moved twenty blocks further out, which is what brought `WL9`'s `spawn-wool-ratio` inside its band |
| wool-b walked out along a twenty-five-block dog-leg east, room at `x 40..50, z 15..25` | the dog-leg deleted; the room is an **island** at `x 35..45, z 15..25`, fifteen blocks of void from its own shelf |
| frontline `x −15..15` | widened east to `x −15..20`, so it meets the hub's east prong and the walk to the east wool is not the whole way round the hub |
| one zone, the mid band | two: the mid band, and **`b-link`**, a team-only crossing `x 30..45, z 20..45` |
| no layers | one, `below` the compiled ground |
| spawn `x 10..20, z 55..65` | `x 5..20, z 60..70`, off the bar's south-west so it shares no edge with the east shelf |

## The intra-team build zone

`b-link` is what `CT4` calls a **team transient-link** and `BZ5` the defender-egress bridge:
every interfacing component of it touches only this team's islands — the east shelf on one
side and the wool room's island on the other, and nothing else on the board reaches it.
Outside a build zone the `not-build-area` filter denies placing into the void, so an attacker
standing on the frontline twenty blocks west of that island **cannot bridge to it**: they can
see the wool and they have to walk the whole hub and cross the defenders' own bridge to get
at it. That is the pad no enemy can flank.

It costs one thing and the cost is stated rather than hidden: a piece with no land interface
has no lane, so `LN1` reports `lane-width 0` and the board evaluates at **score 1** instead of
0. Measured — the same plan with the room joined to its shelf scores 0.578 and `LN1` is
silent. The one point is the price of the motif.

## The second storey, and what the storey is

One layer, `under`, `below: true`, `base_y 0`, six shapes, no subtract. The gallery is drawn
as the **complement of the space**: the rock fills the hill's body from `y1` to `y14`
everywhere the hub stands except along the lane, where `rock-sole` stops at `y10`. The hub's
own ground is a slab from `y15` (`shapePropsByHeight {"16": {"floor": 15}}`), and that slab
is the gallery's roof.

| Shape | Box | Span |
|---|---|---|
| `rock-crest` | `x 9..15, z 40..47` | y1..14 |
| `rock-north` | `x −5..29, z 48..49` | y1..14 |
| `rock-south` | `x −5..29, z 56..59` | y1..14 |
| `rock-sole` | `x −5..29, z 50..55` | **y1..10** |
| `rock-prong-w` · `rock-prong-e` | the two hub prongs | y1..14 |

Measured: the void scan reads `840 cells open x −5..29 y 11..14 z 50..55`, and the section at
`z = 52` reads rock to `y10`, four courses of air, and the hill's slab from `y15` up to `y21`.
`GET …/walk?from=-12,52,11&to=36,52,11` answers **`rises 0, falls 0, worst step 0, walked end
to end`** — forty-eight blocks from the west shelf to the east one without surfacing.
`GET …/column?at=12,52` reads cobblestone at `y10` over andesite and granite: the gallery's
floor is painted, because a `below` layer paints its own column before the ground layer's pass
runs and the ground theme's `fill` is not plain stone.

In gameplay terms the storey is **the defence's rotation**. The two wools are sixty-five
blocks apart over the hill and forty-eight under it; a defender who loses the west shelf can
be at the east bridge without ever being seen from the frontline, and an attacker who takes
the hill has taken the roof rather than the road.

## Relief

One group. The hill's top is **stated flat at 16 over its whole footprint** and carries no
tread: it is the gallery's roof and the ground the match is fought on, and a tread there
would grade the two flights' heads into the hillside. What rolls is the frontline's back half
— two point knolls and a push (`brow`, amount 3) between the landing apron at 15 and the hill
— and the ground behind the spawn.

The two flights (`ramp-w` `x −5..8, z 40..47`, `ramp-e` `x 16..29, z 40..47`) are
`relief_scope: "exclude"`, `height_mode: "level"`, `skirt: 0`, twelve blocks of run for five
of rise, cut into the hill's north face and carrying a material rather than a theme. They are
what answers `EL1`'s two standing complaints about the `hub-bar`–shelf seams: the plan tier
walks those pieces flat and cannot see a flight. Transect across the west one at `z = 44`
reads one block of rise every two or three columns and no barrier.

Relief read: level **0.606**, largestField **0.508**, 0 faces, 0 seams, 0 silent marks. That
is flatter than this repository's rule of thumb likes, and it is deliberate: 24 % of the
board's ground is a roof and another 20 % is a cut shelf, and neither is terrain that should
roll. The first attempt let the hill roll and produced `RL5` at 29 % level instead.

## What it is painted with

Three themes: `fell` 64.4 %, `shelf` 35.6 % on the surface, and `rock` under both of them.
Ground family is a dry ochre hill — grass, coarse dirt and podzol over terracotta and granite
on a `Mesa` tint, so the greens come to meet the browns. Built family is the two flights'
cobble-and-brick and the two buildings' spruce. The `fell` surface is a `layered` material on
the **`slope`** axis, cutting at 18° and 32°.

`05-themes.txt` counts **two** themes, not three, and that is not a theme that painted
nothing: `themes/census` reads the surface, and the whole of `rock` is under a roof. The read
that sees it is `column`.

## The numbers

| Read | Answer |
|---|---|
| `/plan/evaluate` | score **1**, valid; one soft term, `LN1 lane-width 0` |
| `/preflight` | **export gate OPEN** |
| `/coverage` | reached 5 341, decorated 46, dead 13 — **0.2 %** |
| `03-slopes.txt` | 5 069 walked, 125 scrambled, 206 barrier; 10 faces, largest 39 |
| `06-claims.txt` | placed 28, declined **0** |
| `/plan/flow` before | attacker **129 / 175** (1.36×), defender **30 / 48** (1.60×), *one way in* |
| `/plan/flow` after | attacker **151 / 161** (**1.07×**), defender **39 / 50** (1.28×), **3 ways in** |
| relief read | level 0.606 / 0.508, 0 seams, 0 silent |

## What went wrong

**The relief pushed the hill ten blocks over the flights' heads.** The first build's ramps
ended at `y16` while the hill around them solved to `y26`, and the transect read
`BARRIER +12 at (5, 44)`. A ramp with absolute anchors has to arrive at ground whose height is
also stated; an `area` mark pinning the hub at exactly 16 is what fixed it.

**`SK11` named 1 178 unreachable places** while the flights were unreachable, and named
nothing once they were. It is the read that caught the fault the transect then explained.

**A plan wall's worth of arithmetic on `G5`.** Placing the wool-b island took three tries:
each candidate position was inside ten blocks of some corner of the hub or the frontline, and
`G5` refuses a hop under 10. The read that settles it is `/plan/evaluate` on a `--dry` pass,
which costs nothing.

**`relief.*.stairs` is not a field.** Two `RQ3` complaints named it. It was copied from a spec
in this repository older than the schema.
