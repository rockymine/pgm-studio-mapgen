# Emberwood Vale — the canonical brief, built

> Two hamlets at opposite ends of an autumn forest clearing, each keeping its wool at a shrine behind
> the village, with the wood between them the only way across.

**In one sentence:** a timber hamlet sits behind a split village green, its wool kept at a small
stone-and-quartz shrine further back still, and the two hamlets are joined only by a forest whose
central brook forces every crossing through one open ford — with a rougher trail along the west flank
for whoever would rather not be seen taking it.

110 × 240 blocks, `rot_180` about the origin, base surface 9, a modest relief of three gentle marks
(low 6, high 12) rather than anything mountainous — this is a village board, not a hill board. `ctw`,
one wool a team, `maxPlayers` 10 a side.

## Where the brief's things are

| The brief asked for | Where it is | Measured |
|---|---|---|
| split site (hamlet + garden island) | `garden-red` is its own 20×30 piece, cut off from `approach-red` by a 10-block void and rejoined by a hand-built plank bridge | `garden-bridge`, an override-free `add` rectangle at `x 20..30, z -33..-27`, `base_height 9` matching the ground either side |
| internal build zone (a village green) | `village-green`, a 10×30 void carved between the two hamlet halves, declared a buildable zone from the first tick | `PlanVoids` auto-declared it `void-1-cut`; the stated `zones` entry over the same rect is what makes it crossable at kickoff rather than a hole |
| wool accessibility checked from its own spawn | `POST /plan/inspect` and the driven flow both read it before anything was built | flow: "the attacker walks 193 blocks to it; the defender 33" — the shrine sits close and direct behind the hamlet, no repositioning needed |
| circulation before the wood | plan pieces state the street, the flank trail and the clearing frontage first; trees were scattered only after the paths were drawn | `street-main` and `trail-flank` are strokes drawn before `scatter_trees` ran in the same script |
| ≥2 broadleaf species, canopy with gaps | oak, birch and dark oak template trees at two heights each, spaced 8–15 blocks apart | 24 trees on the authored half (48 fanned); `world-iso.png` shows canopy with real gaps between crowns |
| one hamlet, ≤2 house styles | `cottage_a` (gable, the spawn hall) and `cottage_b` (hip, the second cottage) — one wall recipe, one roof swap and one plank repaint apart | `renders/room-spawn-section.png`, `room-wool-section.png`; `hamlet-east-cottage` is the only hand-placed house |
| timber rules (no footing, laid-log + beam, two-species checker) | `foundation.footing: null`; wall stack is `laidLog(spruce) → checker(oak, spruce) → solid(plank)`; `beams` enabled on the same recipe | `sonnet5-emberwood-vale.finish.json`, `cottage_a`/`cottage_b` |
| three themes (ground / built / accent) | `emberwood-floor` (forest), `hearth-yard` (dooryard), `shrine-stone` (shrine) | `05-themes.txt`: 71.7% / 19.0% / 9.3%, two borders, no fourth theme |
| leaf-litter as its own shape | `leaf-litter`, a five-vertex polygon west of the street, `layered(depth)` of a podzol/coarse-dirt pick over plain dirt | `add_shapes["leaf-litter"]` |
| WL8 second, harder route | the flank trail — narrower (`radius 2`), `worn` at 65% coverage, its own denser wood, reaching the brook in its own right rather than only rejoining the street | `FR6`/`FR8` both read against the *combined* frontage of `approach-red` + `flank-red`, 75 blocks, inside the 16-cell cap |

## The forest is a village-in-a-clearing, not a wall of trees

The order the brief asked for is the order the spec is written in: `street-main` and `trail-flank` are
authored before a single tree is scattered, and the scatter itself is boxed away from both — the street's
own eight-block corridor, the spawn door's twenty-block apron, the wool room's ten-block one. What is
left is what the wood may fill, and it does not fill all of it: `approach-red`'s two flanks carry a
loose grid at 13-block spacing, the harder flank trail's own strip at 8, the garden island a lighter
one at 15. Coverage still reads 16.6% dead — mostly the two ornamental knolls under the garden and the
flank wood's own far corners, ground that is genuinely a side pocket rather than a through-route, not a
mistake in the plan.

## The brook is the void doing capture's own job

`approaches.md` names void as the primary flow control on a capture board, and this map's middle is one:
`clearing-red` stops eleven cells short of the axis on both sides, and the ten-block gap between the
two teams' clearings is a real void, not a relief dip — nothing added it back. `CT12` reads the strait
at 20 blocks (inside 15–40); `FR6` reads the frontage the two clearings present at 75 blocks (inside
the 16-cell/80-block cap once flank-red's own frontage is folded in). What crosses it is a stated
`ford` zone the width of that whole frontage, not a narrow plank — the brief's own `FR8` finding, that a
crossing should span the face it docks against rather than funnel through a slice of it.

## Techniques, and what each bought

**A split site built from arrangement, not subtraction.** `garden-red` was never carved out of a bigger
polygon; it is its own rectangle from the plan tier, with the ten-block gap simply the space no piece
covers. The plank bridge across it is an ordinary `add` — nothing subtracts that ground, so no
`override` was needed, only a `material` of its own (Spruce Planks) so it reads as a made thing rather
than more forest floor.

**A build zone drawn where the composer never puts one.** The village green is the composer's known
gap named outright in the brief: a void *inside* a team's own site, walled on all four sides by the
hamlet's own pieces (`wool-room-red` to the north, `approach-red` to the south, the two hamlet halves
east and west), and covered by a stated `zones` entry so it opens at kickoff rather than waiting on a
subtract that was never going to be crossable at all.

**Paint patches, not themes on role-tagged shapes.** `GENERATION-NOTES.md`'s own finding — a spawn or
wool piece's interior is never painted by `themeById`, because the projected room rectangle carries a
`role` and the theming pass skips anything that does — meant `hearth-yard` and `shrine-stone` had to
reach the board as ordinary `add` shapes at the ground's own height (`dooryard-w`/`dooryard-e` and
`shrine-yard`), never as a `theme` key on the structural rectangles themselves. `SK13` confirmed the
naive version of this (one dooryard rectangle spanning the green's own void) drew nothing over the void
— expected, and fixed by splitting the patch either side of it rather than fighting the subtract.

**A relief this restrained is still relief.** Three point marks, reach 22, low 6 to high 12 — nothing
mountainous, but not a table either: a knoll behind the flank trail, a shallow hollow in the main
approach, a smaller rise by the garden. `relief/read` confirms the fold is exact (`symErr 0`), and the
forest floor's `surface` material is a `layered` stack on the `slope` axis regardless, so the handful of
places the ground does tip read as a different band than the flat majority rather than one flat green
sheet with bumps painted the same as everything else.

## What went wrong

**A window's host block disagreed with its pane (`HS4`).** The first cottage recipe stated
`windows.hostBlock` as the wall's own plank species, on the assumption a window's frame should be cut
from the wall it sits in. `HS4` reads it the other way — the *window's own two blocks* have to agree
with each other, not with the wall — and the fix was to leave `hostBlock: -1` (cut wherever one fits)
rather than naming a species at all.

**Two wall/fill patterns read as vertical stripes before they had a `rise` (`PT4`).** Both stone-family
`cell` patterns on `emberwood-floor` and `hearth-yard` were written for the `surface` bucket's habits
first and only added to `wall`/`fill` afterward, which is exactly backwards: a plane-sampled field on a
bucket seen edge-on paints the same block up an entire column. A `rise` of 3–5 blocks fixed both.

**A picked surfacing block cannot be a shape's whole `material` (`PT1`).** The leaf-litter patch first
stated its podzol/coarse-dirt mix as a bare `cell` pick used directly as the shape's `material` — which
paints identically to a theme's `fill` bucket, and podzol is one course thick by definition. Wrapping it
in a one-course `layered(depth)` band over plain dirt is what a picked surfacing block always wants.

**A straight-line walk reads as climbing the spawn hall's own wall.** `04-routes.txt`'s own-spawn-to-own-wool
route shows a `barrier +3`/`barrier +5`/`drop -8` right at the spawn building's post — a real column read
confirms it is the hall's wall (`Oak Log` post, y9–16) and not a terrain fault. This is the `aim=travel`
walker cutting the geometric short line through an obstacle it can place-block over rather than routing
through the actual door; the export gate's own `Traversability.Check`, which is what the game plays
against, reported the chain connected and opened clean. Recorded as an open question below rather than
"fixed," since nudging the door or the spawn marker to chase a diagnostic tool's straight-line preference
is not obviously the right trade against the door siting the piece adjacency already gave it.

## What worked first time

The plan tier — pieces, zones, placements — refused cleanly and legibly every time something was
actually wrong (`PL12`'s mixed-mirror complaint when the shared clearing was first drawn `mirrors:
false`; `WX3`'s marker parity; `ST9`/`ST10`'s footprint and pad caps) and never once for something that
turned out to be fine. `POST /plan/room` handed back the exact `at`/`footprint`/`iron` numbers for both
the spawn hall and the shrine on the first ask, once the pieces were sized to fit `ST10` — no guessing,
no disagreement between the seeded rectangle and what the export would have defaulted to. The house
styles compiled and stamped correctly the moment the two material refusals above were fixed; nothing
about the timber recipe itself — the laid-log course, the two-species checker, the disabled footing —
needed a second pass.

## Open questions for the human oracle

- **The own-spawn-to-own-wool ratio is 0.17** (33 blocks defending, 193 attacking) — a very short,
  direct defensive patrol and a long attacking walk. `approaches.md` calls this the right shape for a
  destroy board's monument-behind-spawn arrangement; whether a *capture* board's own wool wants the same
  ratio, or something closer to parity with the enemy's approach, is a judgement call this session made
  without an oracle. Decided: keep it, on the reading that "the wool belongs behind, deep and
  protected" is the same principle stated for destroy in `approaches.md` and there is no stated reason
  capture should differ.
- **Whether the flank trail is actually taken as a second route**, or whether the main street is simply
  wide and direct enough that nobody bothers (`match-flow.md` §6.9's "an alternative is used when taking
  it costs little, and refused when the main road is already wide and direct") is a question only
  recorded play could answer; the plan and dressing make it *available* — its own frontage share of the
  crossing, its own wood, its own worn path — without being able to say it is *chosen*.
