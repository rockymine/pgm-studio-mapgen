# Sallyport — a rampart with a postern, and a wool you have to bridge to

**In one sentence:** a team that has to bridge to its own wool defends a different board from one
that can walk to it, and the rampart in front is what it walks out through.

Composed from `GET /api/compose?players=30&symmetry=rot_180&seed=66` — hub `bar` (one 10 × 6 piece),
frontline `single` (two steps), wools `i`/`l`, card score 1.392 with `WL10`'s `wool-front-ratio` at
**1.745**, 138 land cells, 110 × 170 blocks. The adapted plan is 120 × 180 and evaluates at
**score 0, valid**.

## What the composer gave, and what was done with it

**The hub bar was cut across its width.** Its front two cells became a terrace three courses over the
moor; the rampart stands on the terrace's lip, and between its two runs is a gap the two drum towers
flank. That gap is the sally port. The flight that fills it is eight blocks of run for three courses,
set into a re-entrant cut for it, and the terrace's *back* carries a second re-entrant and a second
flight — because a three-course drop is a drop on both sides, and without the back ramp the only walk
onto the garrison's own rampart would have been the attackers' stair.

**The near wool was taken off the team's landmass.** It stands on an outwork over a twenty-block
strait, and the only way on is `team-bridge`: a build zone whose every interfacing component touches
one team's islands and nobody else's. That is `CT4`'s **team transient-link** and `BZ5`'s
defender-egress bridge, measured as the `team-stepping-count` term with a band of [0, 2]. The
composer models none — it emits exactly one zone, the mid band, on every board it makes.

## The lopsided wool: what was predicted, and what was measured

Before building this board I wrote down that the lopsidedness would **not** close, because the spawn
hangs off one corner of the team's half and the locus of points equidistant from both spawns runs
outside that half. The plan was to leave the ratio and make the near wool cost a bridge instead.

The measurement said otherwise. Moving the near wool twenty blocks west onto an outwork, over a
strait a raider has to bridge, moved the *walk* as well as the cost:

| | composed (seed 66) | Sallyport |
|---|---|---|
| attacker's walk, deep wool / near wool | 167 / 130 blocks | **169 / 165** |
| attack ratio | **1.28** | **1.02** |
| defender's walk | 78 / 72 | 78 / 95 |
| defence ratio | 1.08 | 1.22 |
| `wool-front-ratio` (`WL10`) | 1.745, refused | in band |

The straight-line arithmetic was right and the conclusion from it was wrong: a wool 20 blocks further
out across water is 35 blocks further by walk, because the walk has to come back round. The finding
that survives is the narrower one — *a corner spawn cannot have both readings at 1* — and it is what
board 1 answers by moving the spawn onto the axis.

## How it is meant to play

The attacker crosses a 20-block mid and lands on 50 × 25 blocks of moor with a rigg across its east
half, a steading standing in it for cover, and a three-course terrace face in front carrying a
crenellated rampart. There is exactly one way up: the sally port, ten blocks wide between two towers.
Behind it the moor runs back to the spawn past a stepped barrow, and the two wools pull the defence
in opposite directions — one a walk north-west behind a bedrock wall, one a bridge west across water
onto a crag with its own curtain facing the landing.

## The techniques, and what each one bought

**Two re-entrants and two flights** on one terrace, one per side, each cut to exactly the flight
that fills it. The transect through the sally port reads `11 11 11 12 12 13 13 13 14` and
`walked end to end`; the back ramp reads `worst step 1`.

**Nine made layers**: two runs of crenellated rampart, two drum gate towers, a three-tier ziggurat
barrow on the moor, and two runs of curtain on the outwork's east face with the bridge's landing left
open between them.

**A drystone dyke as a `polyline`.** Four points across the moor, radius 1.2, `stroke_edge: rough`,
`height_mode: raise` at two courses — so it is proud of whatever ground it crosses and is a scramble
rather than a barrier. It breaks the sightline down the moor without closing it, and it is one shape
rather than a chain of chords.

**A barrow needs a pad.** A made thing states an absolute floor and the moor is solved, so the
barrow's ground is stated with its own `area` mark. So is the ground at the sally port's foot, for
the same reason in reverse: a stair states its two ends and the ground beside it has to arrive at the
lower one.

**The push clears the stair.** Ring 10 plus falloff 6 reaches sixteen blocks from (20, 20); the sally
port's foot is 22.8 away, so the first tread is met on the flat it was anchored to.

**Numbers.** `preflight` ends `export gate OPEN`. `coverage`: 7900 reached, **0.0% dead**, with 150
blocks (1%) off every route — one sliver under 100 blocks, which the read itself says is not a place.
`03-slopes.txt`: 6788 walked, 232 scrambled, 272 barrier, 4 faces, the largest 76 — that run is the
terrace's front, which is the rampart and is meant to be impassable. Relief: `level` 0.551,
`largestField` 0.185, range 8 over 2777 cells, `symmetryError` 0, one seam of step 2. Themes: moor
76.1%, crag 12.1%, works 11.7%.

## What went wrong

**The terrace was climbable from the wrong side only.** The first build gave the sally port its
flight and nothing else, and the transect out of the spawn read `−3` at z 45: the garrison could drop
off its own rampart and not get back up. Neither `preflight` nor the relief read says a word about
it — `EL1` named the seam at the plan tier and I had read that as answered.

**`@hb-cage` and `@lk-terrace` both refuse with `HS9`**: they lay beams and no course of any wall is
a laid log. The tell is `beams.any: true` with no `laidLog` band anywhere in the style. `@ow-cage`
and the `talltimber` pair carry `any: false` and pass.

**Five props declined** on the first pass, all of them guesses. Every placement now comes from
`loop.py --candidates`.

## Standing complaints

- **`EL1` ×2** on the terrace's two seams, three blocks each. Both are answered by a flight and both
  transect `walked end to end`.
- **`SK27`**: four plateaus, three paints. The moor, the terrace and the outwork are three places and
  the risers between them are where a player crosses from one to another.
- **`SP2`**, "not near the back of its lane". The rule's own text says the current lint approximates
  "back" per piece and misreads a spawn placed mid-chain (`G24` open); the composed source raises it
  too, unchanged.

## Coordinates

| thing | at |
|---|---|
| the terrace | x −15..35, z 35..45, surface 14 |
| the rampart | z 35..37, x −15..−6 and 6..35, four courses over the terrace |
| the sally port | x −5..5, flight z 31..39, 11 → 14 |
| gate towers | (−9, 41) and (9, 41), drum, outer 3, 12 tall |
| the back ramp | x 26..34, z 41..49, 14 → 11 |
| the barrow | (10, 56), three tiers, half 6 |
| the dyke | polyline (6,52)→(16,56)→(26,55)→(34,60), two courses |
| the outwork | x −60..−35, z 40..60, surface 13 |
| the strait | x −35..−15, twenty blocks |
| `team-bridge` zone | x −35..−15, z 45..55 |
| bedrock wall | z = 65, x −10..0 |
| wools | (−20, 80) and (−50, 50) |
