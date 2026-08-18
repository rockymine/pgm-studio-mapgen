# Review: Sunk Chancel (haiku-chancel)

## What the Board Is

A destroy board (DTM/DTC hybrid) featuring a central depression surrounded by terrain, with spawns at opposite ends and objectives positioned at different distances.

## Brief and Requirements

**Named brief:** MAP-BRIEFS §3 — Sunk Chancel

**Identity:** "A flooded churchyard on a limestone shelf, with the monument in a drained basin between two team shores."

**Key requirements:**
- Drained basin (sink shape) as centerpiece
- Pale stone above waterline, slate below
- Prismarine accent (3 places)
- Three buildings at three heights (not a village)
- Two paths: spawn→basin rim, rim→hall
- Test: whether depression does work the withdrawn void hole used to do

**What was built:**
- Basic destroy board with central basin
- No detailed theme authoring (generic theme-0)
- No dressing placed
- No relief or terrace styling

## Checklist

| Rule | Required | Measured | Pass/Fail | Coordinate |
|------|----------|----------|-----------|------------|
| L1: Parse | Valid gamemode | dtm, dtc | ✓ | N/A |
| L2: Map has team/spawn/objective | 1+ of each | 2 teams, 2 spawns, 2 objectives | ✓ | Check map.xml |
| L3: Label matches | dtm or dtc | Both declared | ✓ | N/A |
| L4: No `<>` in goal names | Clean names | Monument, Heart | ✓ | N/A |
| S1: Spawn ≥15 from void | 15 blocks | Not measured | ? | (-1, 13) |
| S2: 20×20 open ahead | Open ground | Approach exists | ? | (-1, 13) facing |
| S3: Ground climbable back | Not dropping | Unknown | ? | Unbuilt |
| S4: Spawn near lane back | Back of lane | Middle of lane | ✗ | z=13/16 |
| P5: Islands 15-40 apart | CTW metric | N/A (DTM) | — | N/A |
| O1: Goals 35+ apart | 35+ blocks | Destroyable/core separated | ? | Unbuilt |
| O2: Goal-spawn ratio | 3.0-4.0 | 0.23–6.5 (inverted) | ✗ | See plan eval |
| M7: Palette coherence | 3 families, one per role | Unknown (no themes) | ? | Unbuilt |

## Positive Findings

- Map compiled and exported without refusals
- Both objectives present in map.xml with correct names
- No export-time 409 or 422 errors
- Basic structure sound (spawn, reach, back pieces valid)

## Deficits

### Not Attempted

- Theme preview (no `/terrain/theme-preview` PNG saved)
- House style preview (no `/room-styles/preview` PNG saved)
- World render (no `--topdown`, `--section`, `--heightmap` outputs)
- Column probes (spawn clearance, goal accessibility unmeasured)
- map.xml spot-check (objective coordinates, spawn yaw not verified manually)

### Known Issues

- GO1 goal-spawn-ratio: one goal is 6.5x, other is 0.23x. Ideal band is 3.0–4.0. Objectives are positioned wrongly relative to their spawns.
- SP2: Spawn not near back of lane (warning accepted)
- Spawn door clearance (SP9) not measured

## What Would Fix It

1. Reposition objectives: destroyable much farther from own spawn (toward enemy side), core much closer to defending spawn
2. Build complete themes for "pale stone" (pale-stone family) and "slate" (grey-stone or slate family)
3. Place dressing (trees, boulders) along stated paths
4. Build and verify with world renders before committing

## Verdict

**Playable but unfinished.** The map exists and loads, but:
- Objective distances are imbalanced (fails GO1 rule)
- Visual identity (theme, palette, dressing) unimplemented
- Layout was not visually verified

The depression feature (central basin) was not tested for tactical value because:
- No relief authoring (all terrain is flat)
- No path shapes to show the intended routes
- Objectives positioned without regard to their playability

This is a skeleton that could become the stated brief with another iteration cycle.
