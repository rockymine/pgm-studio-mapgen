# Opus 5 — four boards, one for each way a map is won

## What I set out to build

Four boards, decided together so that no two of them would be the same board in different
blocks: a **destroy-the-monument**, a **destroy-the-core**, a **capture-the-wool**, and one
board played for **a wool and a monument at once**.

| Slug | Played for | The sentence it was authored to |
|---|---|---|
| `opus5-kilnbrow` | dtm | a clay firing-ground where the monument stands out on the open pan, and the ground round it offers four different ways at it rather than one |
| `opus5-sluicehead` | dtc | a frozen sluice works where the core stands out on the open ice with ground all round it |
| `opus5-hallowgate` | ctw | a churchyard where the wool is fetched from a chapel at the end of one walled causeway, and the only other way at it is the long way round a hole nobody can cross |
| `opus5-tallowfleet` | ctw + dtm | a tallow works where the beacon is broken where it stands and the wool has to be carried home, so a defence that holds the quay is not a defence that holds the cellar |

The studio was not running and nothing was installed. `docs/cloud-setup.md` is accurate: the
SDK and MariaDB by apt, the database and its user, `--migrate-only` (M0001…M0038), then the
API, and `tools/seed-trees.cs` for the 84 copied trees, which a fresh studio does not seed.

## What I could not say

**The dead-share number has no card, and it is the one number that moved a board's whole
shape.** `GET …/coverage` is the only read that asks whether ground is on any journey, nothing
refuses on it, and `techniques/` has no card for it. Kilnbrow read **44.6% dead** with the
monument on the centre line and **6.0%** with it twenty blocks off, and I found that by
running the read three iterations late. The mechanism is not missing — the endpoint exists and
answers in one fetch. What is missing is anything that would make an author run it before the
third pass.

**`G8`'s fill ratio names a band and not a lever.** The refusal says `fill-ratio 0.571 outside
authored band [0.201, 0.542]` and the rule prose is about `maxPlayers` and land-per-team,
which is a different quantity from land over the board's bounding box. I worked out that the
box is the denominator by shrinking the land twice — which cost `CT12` once and nearly cost the
spawn's own egress — before trying the box. `GET /api/rules/terms` is the index that would
have said which term the band is over, and I did not run it. **Out of reach from where I was
standing, not missing.**

**`DR-TONE` and `WHAT-A-BOARD-IS-MADE-OF.md` appear to disagree, and do not.** The document
says *a boulder is stone*; the rule says a rock made only of tones the ground has reads as
ground standing up. On the one grey board in this run both are true at once, and the rule's own
`fix` field carries the resolution — *where the ground is itself grey stone, take the rock the
other way.* I only read it because the complaint fired. `GET /api/rules?rule=<id>` returns the
fix as well as the meaning and I had been reading only the meaning.

## What I got wrong

**I read the existing map specs first, and it cost me directly.** I opened four boards under
`specs/` to reverse-engineer the field vocabulary, copied a flight that states `height_mode`
**and** `relief_scope` on one shape, and `made-ground`'s card says plainly that stating both
silently discards the scope. The cards were the right source and they are smaller: the whole
of `techniques/` is 27 cards at a ~2.4k-token median, each one a world with its variants side
by side and its reads committed. **A spec is dated evidence; a card is a demonstration.**

**I left both rooms as the studio's bedrock box on all three of the first boards.** A finish
that states no `roomStyles` stamps a bedrock cage at 200 with no finding, and those are the two
structures every player sees from the inside. The cards' own boards wear it — correctly, since
a card about relief is not about a room — and I read that as the shape a room takes.

**Then I built the rooms flat with a hole in the lid, which is the bedrock box's own shape.**
`a-house-and-its-wings` says *`flat` is the only one that can carry a hole — which is why a
wool room and a spawn have always worn it*, and I read the second half as a requirement. It is
a description of what boards have done. A room entered through its own door has no use for a
lid that opens. Three cards now say so and the wording that misled me is reworded.

**I blamed a `PL9` on Tallowfleet's defence wall and the wall was innocent.** I removed it and
re-drove and `PL9` was exactly where it had been: the cause was a quay piece that was an island
on both sides of the symmetry. **Removing the thing you suspect and re-driving is cheap**, and
it is the only reason the second guess was not also wrong.

**I placed props by eye on the first board and five came back declined** — `DR-STEEP`,
`DR-CUT`, `DR-ROAD`, `DR-CLAIM`, `DR-KEEP`. `POST …/sketch/seats` answers where a kind may
stand forwards over the whole board, and once every position came off that mask the declines
went to zero on all four. **Take the cell from the middle of a seat block, not from its edge**:
a placement names where a recipe is seated and a copied tree's foot is several cells across, so
a tree asked for at (−19, −77) rested on (−16, −76) and came back `DR-ROAD` from a legal seat.

**Two made structures floated one course above what they were meant to rest on.** A layer's
`base_y` is the layer below's **top block** plus one, and a shape of `base_height` N tops out
at N−1. Written as `TERRACE + 1` against a terrace of `base_height` 14, both left a gap no gate
reports.

**I cut Tallowfleet's slope bands at Kilnbrow's angles.** 28°/50° on a board with 0.9% of its
ground at 40° or steeper puts the face band above the whole population, so it paints nothing
and the shoulder carries the estuary. `GET …/incline?format=text` prints the distribution under
its own grid and the cut has to be read off it every time.

## What worked first time

- **`relief_scope: "exclude"` on a made tier, once I understood what it does.** A solved
  shape's own `base_height` decides nothing about where its ground ends up. Excluding the tier
  is what gives it a face for a flight to state; three of the four boards are built on it and
  Tallowfleet built with **0 faces** until it was applied.
- **Slope-axis banding.** One `layered` surface on the `slope` axis finishes the flat, the
  shoulder and the face of the same hill, and it is the difference between a board that reads
  as ground and a board that reads as a sheet.
- **Transecting a flight to answer `EL1`.** The plan tier walks the pieces flat and cannot see
  an authored flight, so the complaint is right about the plan and says nothing about the
  board. All nine flights across the four boards measure `worst step 1, walked end to end`.
- **`GET …/column` at a structure's image.** Pre-flight's mirror check reads spawns, wool rooms
  and build zones and never made geometry. Two columns settle it.
- **Both boards' four objectives landed inside `GO1`'s band on the first placement**, because
  the distance was composed rather than measured afterwards.

## Open gameplay questions, and what I decided

**Does a mixed board's wool go in front of its monument or behind it?** `approaches.md` settles
it — a monument is breached where it stands and a wool has to be carried home — so the beacon is
forward on the quay and the cellar is deep behind the terrace. Drafted the other way `WL10`
reads a wool-front-distance of 8, which is the rule agreeing.

**May a wool room have only one way in?** I decided no, and gave Tallowfleet's cellar a back
lane as well as the walled spur. A room with one approach is sealed rather than defended, and
`PL9` refuses a wool no enemy can reach. **This is an author's call and I made it without an
oracle.**

**Is a hole in a team's own ground a feature or a funnel?** On Kilnbrow I decided against one —
on a destroy board void belongs *between* the teams, and a hole in a team's own pan empties the
ground the contest was meant to happen on, so the worked clay pit is a depression. On Hallowgate
I left the composer's enclosed grave-pit exactly as composed, because `match-flow.md` §4.9
measures it as the rotation device. **Both are decisions, and they point opposite ways.**

**How much of a board may be flat?** Tallowfleet's quay reads `level` 0.603 — over the 0.45 the
warmup calls a table — with `largestField` 0.080, well under 0.13. I kept it: an objective wants
open ground round it, a tidal quay is flat ground, and the two numbers disagree about whether
that is one table or many small ones. **I trusted the second.**
