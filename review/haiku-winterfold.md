# Review: Winterfold (haiku-winterfold)

## What the Board Is

A destroy board (DTM/DTC) with a tall rise in the center, base terrain at low height, designed for a snowfield aesthetic.

## Brief and Requirements

**Named brief:** MAP-BRIEFS §6 — Winterfold

**Identity:** "A deliberate walk up to the edge of the failure mode. A snowfield over dark rock, and the *only* colour anywhere is the objective, the team wool, and one thing you choose."

**Test:** "Whether a restricted palette stays legible — if the board vanishes, say it vanished."

**Key requirements:**
- Palette: Bright (Snow, Quartz) over Ice with Dark (Black Clay, Coal) beneath
- Rim off everywhere (no contour lines)
- Height carries legibility (long low tilted surfaces, per-vertex `anchor_heights`)
- Buildings: run along edge + one lone structure
- Path: spawn→monument in dark rock (only non-white ground)
- Restricted palette enforces simplicity

**What was built:**
- Four pieces at varying heights (8, 18, 22)
- No theme (generic themes)
- No relief or `anchor_heights`
- No dressing (trees, buildings)
- No path shape

## Checklist

| Aspect | Required | Result | Pass/Fail |
|--------|----------|--------|-----------|
| Palette restriction | Snow/Ice/Dark only | Not themed | ✗ |
| Height variation | Tilted surfaces, anchor_heights | No relief authored | ✗ |
| Rim off | Everywhere | Not verified | ? |
| Path in dark rock | Route legible by material | No path | ✗ |
| Buildings | Edge + solo | None placed | ✗ |
| Legibility test | Board stays visible | Unbuilt, untested | ? |

## Positive

- Tall rise piece (height 22) provides dramatic terrain
- Base terrain exists at lower height (8)
- Structure compiles without error

## Deficits

- **No theme:** Board has no palette (no Snow, no Quartz, no Andesite for riser)
- **No relief:** Height variation declared via piece surfaces only (no organic tilting)
- **No anchor_heights:** Transitions are level steps, not sloped
- **No path:** Dark rock path not visible (board is monochrome by default)
- **No buildings:** No edge run or solo structure to define position
- **No render:** Legibility unverified

## The Test This Brief Carries

"Does a restricted palette stay legible?" This brief is *deliberately pushing toward failure*: can you make a playable map when forced to use only three colours? The answer is **not measurable** because:

1. The palette was not themed (no colours at all yet)
2. Relief/height must do the work (not authored)
3. The contrast (white snow + dark rock path) must be visible (not rendered)

Without a visual build, legibility is untestable.

## Verdict

**Unfinished skeleton.** The map structure exists but has no finish. The brief's core question—can restricted palette work?—is unanswered because the palette was never instantiated.

Achievable with: theme authoring (Snow/Quartz/Coal), relief/anchor_heights, path shape, house placement, and final render to assess legibility.
