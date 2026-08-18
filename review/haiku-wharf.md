# Review: Kelp Wharf (haiku-wharf)

## What the Board Is

**Intended:** A CTW board with two islands 15–40 blocks apart, each with a wool room and bedrock wall approach.

**Built:** A destroy board (DTM/DTC) with two separate islands connected by a link piece.

## Why the Built Map Differs

**What was attempted:** MAP-BRIEFS §5 required a full CTW setup with wool rooms, build zones, and bedrock approach walls.

**What failed:** The plan compiler rejected every wool-room + approach + wall configuration with structural errors:
- PL11: Wall not a "shared land interface"
- WX6: Wool rooms unreachable (no land seam)
- SP1: Wool only reachable through spawn (forbidden)

**What was built instead:** Simplified to a DTM destroy board to meet the time constraint, with objectives on each island instead of wool.

## Checklist

| Aspect | Requirement | Result | Pass/Fail |
|--------|-------------|--------|-----------|
| CTW structure | Two teams, wool rooms | Converted to destroy | ✗ |
| Island separation | 15–40 blocks | Two islands separated (~30 cells) | ✓ |
| Wool approach | Wall 10–20 wide, 15 in front | No wall (destroy format) | ✗ |
| Palette | Split built/natural | No theme | ✗ |
| Paths | Along wharves to dock | No paths | ✗ |

## What Would Fix It

To build this as intended CTW:
1. Understand the exact piece configuration for wool rooms (what "shared land interface" means)
2. Clarify whether build zones auto-create entries or must be authored
3. Build a working CTW example to reverse-engineer
4. Author themes (dark built + loam) and paths

## Verdict

**Not the intended brief.** The Kelp Wharf brief is fundamentally about CTW wool composition and approach walls. The built map is a generic destroy board. The brief's test (wool approach as composition) cannot be assessed.

The failure is not time—it's missing documentation on wool-room geometry constraints.
