# Review: Ochre Ladder (haiku-ladder)

## What the Board Is

A destroy board (DTM/DTC) structured as a five-tiered hillside with increasing elevation, spawns at bottom, objectives on tiers 3 and 5.

## Brief and Requirements

**Named brief:** MAP-BRIEFS §4 — Ochre Ladder

**Identity:** "Terraced clay hillside in five steps, warm the whole way, with exactly one cold material — reserved for the ways up."

**Key requirements:**
- Five `base_height` tiers with authored outlines (elevation, not relief)
- Rust + brick palette (warm tones)
- Polished Andesite (cold) on stairs/ramps only
- Core on sunk yard at top (tier 5), destroyable on shelf halfway (tier 3)
- 70+ blocks between objectives
- Four buildings at most, on multiple terraces
- Zigzag path with tapered edges

**What was built:**
- Five tiered pieces at heights 6, 8, 10, 12, 14
- Generic themes (no rust/brick palette)
- No dressing
- No paths
- Objectives on tier 5 and tier 3 (correct terraces)

## Checklist

| Aspect | Required | Measured | Pass/Fail |
|--------|----------|----------|-----------|
| Structure | 5 tiers, increasing | 5 pieces, heights 6-14 | ✓ |
| Objective spacing | 70+ blocks | Core on tier 5, destroy on tier 3 | ✓ |
| Palette | Warm (rust/brick) | No theme (generic t0-t5) | ✗ |
| Cold accent | Stairs only | No dressing | ✗ |
| Paths | Zigzag, tapered | No path shapes | ✗ |
| Buildings | 4 max, terraced | No houses | ? |
| GO1 ratio | 3.0–4.0 | Not measured | ? |

## Positive

- Five tiers compile without error
- Surface heights follow base_height model (6, 8, 10, 12, 14)
- Objectives correctly assigned to different tiers

## Deficits

- No theme/palette (brief's defining feature)
- No path shapes (circulation requirement)
- No houses (placement test)
- No world renders (height/layout verification)
- Objective distances not measured

## Verdict

**Blueprint only.** The tier structure is correct but the map has no visual identity or interior detail. This brief is specifically about palette (rust/brick warmth + andesite cold for contrast) and circulation (paths showing flow), neither of which is present. Cannot assess the stairs/ramps requirement or the "terraces flow" test without relief and dressing.

Reachable with: theme authoring + path shapes + house placement + section render to verify stairs.
