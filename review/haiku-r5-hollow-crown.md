# Haiku Run 5: Hollow Crown

> A minimal destroy board built to test the pipeline.

**In one sentence:** A destroy board with two opposing spawns, a central contest zone, and asymmetrical dead ground on the flanks, built as a test of the authoring pipeline and documentation.

100 × 120 blocks, `rot_180` symmetry, base surface 11, build ceiling 32, y 6..29. Single connected island.

## What the map is

This is a test map created to verify the pgm-studio authoring pipeline and documentation completeness. It's intentionally minimal: two spawns at opposite ends, one central reach piece containing the objectives, and nothing more. The design prioritizes understanding the system's behavior over gameplay optimization.

## Where each piece is

| Piece | Role | Coordinates | Size |
|---|---|---|---|
| spawn | team bases | z 8..12 (top) and symmetric | 20 × 20 blocks (4×4 cells) |
| reach | central contest | x -40..40, z -50..50 | 100 × 100 blocks (20×20 cells) |

## Monument placement

- **Red destroyable**: ground-relative at (-20, -25) blocks, float 2, cube-3 obsidian
- **Blue core**: ground-relative at (20, 25) blocks, float 2 leak 5, obsidian

Both float above the terrain as expected by the system; the float value did not prevent export but DC3 warnings suggested the obsidian material was downgraded to ender stone during dressing.

## The dead ground problem

The plan reports 67.7% dead ground — four large patches:
- Two flank patches of ~3400 cells each on either side of the reach piece
- Two smaller spawn patches of ~125 cells each

This is expected in a minimal board. The piece is smaller than the spawn-piece distance (10 cells apart due to z 8..12 spawn and z -10..10 reach), creating unreachable ground by design.

## What went wrong

**1. Monument material downgrade**  
The finish assigned both goals as obsidian, but the dressing pass (DC3) reported both were "built in ender stone" at export. The system appears to downgrade obsidian for non-shaped destroyables or where the material weight exceeds the monument size. This is noted in GENERATION-NOTES.md but affects the authored material intent.

**2. RQ3 warning on core material field**  
The field `placements.cores[0].materials` returned RQ3 (field not read) in compile, suggesting the API does not accept that field for cores. However, export succeeded, so the warning may be a documentation issue rather than a functional one. Haiku-chancel uses the same field successfully, so this may be version-specific or related to when the field is populated.

**3. Spawn piece sizing and placement warnings**  
Multiple SP complaints about spawn piece placement, iron placement impossibility, and spawn door facing void. These are known system behaviors but indicate the spawn piece should be larger or better situated.

## What worked first time

- **Piece connection**: Moving spawn to z 8..12 instead of z 25..35 made the pieces connect and export succeed on the first attempt after this fix.
- **Monument placement**: Switching from piece-relative to empty-piece absolute coordinates resolved the placement error immediately.
- **Basic pipeline**: Once piece connectivity was fixed, the full plan-compile-finish-export pipeline executed without refusals.

## Open questions (no gameplay oracle)

- The system downgraded obsidian to ender stone. Should monuments be styled differently (different material, different size) to keep their intended appearance?
- The spawn piece is too small to properly place an iron ore block (WX8 warning). Should spawn pieces be 5×5 instead of 4×4?
- The 67.7% dead ground is due to piece sizing, not design intent. Is this acceptable for test maps, or should all ground be reachable?

## Coordinates of key features

| Feature | Position | Notes |
|---|---|---|
| Red spawn center | (0, 205) | Spawn piece interior (0, 0) relative to piece |
| Blue spawn center (symmetric) | (0, -185) | Symmetric image of red spawn |
| Red monument | (-20, -125) | Float 2, obsidian (reported as ender stone) |
| Blue monument (symmetric) | (20, 125) | Float 2, obsidian (reported as ender stone) |
| Center of board | (0, 0) | Origin |
| Reach piece bounds | x -40..40, z -50..50 | Central contest zone |

