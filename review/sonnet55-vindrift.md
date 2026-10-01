# Vindrift — a snow capture board, built on the deployed studio

> A capture-the-wool board on a glacier: each team's lodge on the snowfield's high shoulder, a crevasse in
> the hub, the wool kept in a timber hall at the cold end of a walled spur, and a holm of ice pillars between.

**In one sentence:** two timber lodges on opposite shoulders of one glacier, each team's wool in a hall at the
end of a spur beyond a crevasse, the ice between them crossed over a sixteen-block gap to a holm where blue
pillars cut the one long sightline.

96 × 216 blocks, `rot_180` about the origin, plan surface 9, ground y9..19. Built on pgmstudio.de as
`sonnet55-vindrift`, in the Sketch tool's In game phase for the author's notes.

## The arrangement is a composed one, and it is the same one as Murkwick's

The plan is `GET /api/compose` at 20 players a team, seed 43, taken whole: a spawn, a hub ringed round a
16-block hole, two wools at the ends of walled spurs, a twin frontline and a mid band with a stone holm in it.
`sonnet55-murkwick` is the same seed at 16 players and comes out as the same 96 × 216 arrangement.

**That is a solved arrangement reused, which `AUTHORING-BRIEF.md` §3 says not to do.** It was found out after
the board was built, when the BOARDS-BUILT entry for Murkwick was read to write this one up. What differs is
everything downstream of the plan: the outline, the ground, the paint, the buildings, the middle and the
dressing. The open question is whether the author wants the arrangement itself changed.

## What was authored over the plan

Two edits to the composed plan: the right-hand frontline spur widened to the band's edge so both crossings
are 16 blocks (`FR9`), and the holm shortened so each strait to it is 16 blocks rather than 12. Everything
else is in the finish.

| Decision | Where it is | Measured |
|---|---|---|
| a glacier, so a cold biome | Cold taiga, `#80b497` | every tinted block agrees with the snow |
| ground, built, accent | snow and packed ice · dark spruce timber · brick-red roofs | no wall is in the ground's family |
| relief | five `area` marks, five pushes | `level` 0.57, `largestField` 0.28, no seams, no silent marks |
| the crevasse | the compiled `void-1-cut`, bent point by point | 16 blocks, `side: both`, wander 2 |
| the coast | 18 points added along six outer edges of the compiled outline | the brinks, the wool rooms' ends and the spawn's stay as composed |
| the paint | one slope-banded snow theme, a forest floor per tree, an ice theme for the pillars | 91.5% snowfield, 8.5% forest floor |

## How the ground is shaped

The spawn shelf is pinned at y15 and the front apron at y9, and the ground between them is left to the solver,
so the lodge stands on a shelf that steps down toward the front a course at a time. The two wool pads are
pinned flat at y10, because the bedrock wall each hall stands behind is four courses high and a raised pad
would eat it.

**Three kinds of landform sit on that ground.** A cornice ring round the crevasse lifts a band two blocks
along its lip; a wooded drift on each flank of the back bar lifts three with a crown; and two low berms
across the holm are cover to cross behind rather than a hill in the middle of the lane.

## How it is finished

**The snowfield theme is banded by angle.** Snow with sparse packed-ice patches to 40°, packed ice with
stone beneath from 40° to 60°, scree beyond. The surface is one course of snow over two more rather than over
dirt, because a one-block riser on a drift shows its second course and dirt there is a brown stripe.

**A cut face is glacier.** The wall bucket is a snow cap, seven courses of packed ice and then dark rock,
and the rim carries the cap round every coast over void so no brown course shows at the lip.

**Trees need soil and the snow is not soil.** `DR-ROOT` refuses a trunk on snow, so each spruce stands in a
disc of podzol and coarse dirt drawn level with the island's top. The discs also read as ground the snow is
kept off by a crown.

## What stands on it

Dark-oak posts, spruce plank walls and brick roofs on one house style for the spawn lodge and both wool
halls; floors are four stone tones in a `cell`; no footing, no shed roof. Roads are coarse dirt, podzol and
spruce plank in a `cell`, with a wander of two, running from the spawn door to each hall's wall and to each
crossing.

Eight copied spruce, two species — a compact tall-spruce for the two wooded drifts and tiny spruces around
them and on the hub's outer banks — and a rock on the east coast. The holm carries a hexagonal ice needle on
the centre line, eleven high, and a stump either side, as made layers seated on the ground.

## What it plays like

The attacker walks 208 and 201 blocks to the two wools and the defender 52 and 56, so `GO1`'s ratio is 4.0
and 3.6 and the two wools are within a few blocks of each other. The crevasse forces every route round it, the
crossings are 16 blocks to the holm and 16 on, and the needle takes the sightline between the lodges.

**Read straight off the board:** 8 465 cells walked, 44 scrambled and 8 barrier, the barrier being the
needle's own faces; 1.3% dead ground, both patches the holm's ends; 32 props placed and none declined;
pre-flight `export gate OPEN`.

## What went wrong

**The arrangement was reused** (above). **Boulders were hard to seat:** the corridors are twelve to sixteen
blocks wide, a road's wander moves the paving after the boulder is placed, and an outcrop had no legal cell on
either flank; it was dropped. **A bend on the outline broke the build zones:** `bendShapes` on the island pulled
the frontline's brink and a wool spur's end in by a block, which `EZ2` named at nine and one columns, so the
coast is edited point by point instead.

## Open gameplay questions

**Are two ways round the crevasse enough for a defender?** It is the composed shape and was not changed.
**Does the needle make the holm too safe to cross, or is cover in the middle what the author wants?** It was
built, not decided.
