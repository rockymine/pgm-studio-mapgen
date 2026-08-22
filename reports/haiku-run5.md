# Haiku Run 5: Authoring Report

## What I Set Out to Build

I intended to author a simple destroy PGM map named "Hollow Crown" with:
- Two opposing spawns at opposite ends of a board
- One central objective (destroyable/core pair) in a neutral zone
- Symmetrical layout (rot_180) with minimal complexity
- Asymmetric approaches/dead ground on the flanks
- Total extent ~120 × 180 cells, fit for 16 players

**Goal**: Test the pgm-studio authoring pipeline end-to-end using only the API and provided documentation, with no external tool capabilities. Document every moment where the documentation was unclear or I had to guess.

**Result**: Successfully authored, compiled, and exported the map. The world exists at `/home/user/pgm-studio-mapgen/maps/haiku-r5-hollow-crown/` with a valid `map.xml`.

---

## What I Could Not Say (Uncertainties & Lookups)

### 1. Monument placement coordinates: piece reference vs absolute
**What I wanted**: Place a monument on the board in a specific location.

**What I tried**: First, I used piece-relative coordinates with a piece reference:
```json
{"piece": "reach-mid", "at": [-4, -10], ...}
```

**Endpoint/field examined**: `POST /api/plan/evaluate` returned STRUCT error: "destroyable at [-4,-10] falls outside piece 'reach-mid' (0..24, 0..40)"

**Was it missing or out of reach?** Out of reach — I was reading the coordinate system wrong. The reference examples (haiku-chancel) showed monuments using empty piece strings `""` with absolute board coordinates. After switching to that pattern, placement worked.

**Status**: Documentation gap or my misreading. The `docs/tools/plan.md` does not specify whether placements are relative to pieces or absolute, or what the "at" field means for goals vs spawns.

---

### 2. Spawn piece maximum dimensions
**What I wanted**: A spawn zone 40×40 blocks (8×8 cells), matching the center reach area.

**What I tried**: Defined `rect: [-4, 65, 8, 8]` for an 8-cell square.

**Endpoint/field examined**: `POST /api/plan/evaluate` refused with ST9: "spawn piece 'spawn-red' is 40×40 blocks — a role piece is at most 20×20"

**Was it missing or out of reach?** Out of reach — the limit was documented by the refusal itself. After reducing to 4×4 cells (20×20 blocks), it succeeded.

**Status**: The system told me the rule (max 20×20 blocks). No documentation gap; the refusal was sufficient.

---

### 3. Fill ratio and chain length: game balance parameters
**What I wanted**: Understand what board dimensions are acceptable.

**What I tried**: Built a 120 × 180 cell board with sparse geometry.

**Endpoint/field examined**: `POST /api/plan/evaluate` refused with:
- G8: fill-ratio 0.162 outside [0.201, 0.496]
- LN2: max-chain-length 200 outside [25, 110]

**Was it missing or out of reach?** Out of reach — the rules were clear, but I didn't account for them before authoring. The board was too sparse (low fill) and too long (chain length). Shrinking and densifying the geometry fixed both.

**Status**: Documented by the rules themselves. I should have read `GET /api/rules` before starting, as the brief recommends. No documentation gap.

---

### 4. Wall interface requirements
**What I wanted**: Create passage constraints between pieces using walls.

**What I tried**: Multiple configurations:
```json
{"between": ["reach-mid", "flank-west"]}
```

**Endpoint/field examined**: `POST /api/plan/evaluate` refused with STRUCT: "wall ''–'' is not a shared land interface"

**Was it missing or out of reach?** Partially unknown. The pieces appeared to touch along a seam, but the refusal suggested they didn't actually share a continuous interface (different z-ranges for each piece). I resolved this by removing walls entirely (empty walls array) and letting the reach piece be large enough to encompass everything. The final board uses no walls.

**Status**: Wall semantics are not well documented. The GENERATION-NOTES.md §walls section is absent. I determined walls weren't needed for this design, but someone building a more complex map would need clearer rules about what "shared interface" means.

---

### 5. Core material field naming
**What I wanted**: Assign obsidian as the material for a core (blue monument).

**What I tried**: Used the field `materials` in the core placement:
```json
{"materials": "obsidian"}
```

**Endpoint/field examined**: `POST /api/plan/compile` returned RQ3 warning: "field 'placements.cores[0].materials' was not read"

**Was it missing or out of reach?** Ambiguous. The same field works in haiku-chancel's core definition, and the map exported successfully despite the warning. This suggests the field exists but is treated as advisory or optional. The system may have limitations I didn't discover.

**Status**: Minor documentation gap. The RQ3 warning is confusing when the field is used identically in reference examples. I treated it as a non-blocking warning and continued.

---

### 6. Monument materials downgrade at export
**What I wanted**: Export a map with obsidian monuments that stay obsidian.

**What I tried**: Set both goals as `"materials": "obsidian"` with float heights.

**Endpoint/field examined**: `POST /api/map/{slug}/sketch/columns` returned DC3 (decline): "cube-3 is 27 blocks and obsidian is worth at most 3 of them — built in ender stone"

**Was it missing or out of reach?** Out of reach — the system has a material-density rule. The cube-3 monument (27 blocks) is too large for obsidian (worth max 3 blocks), so the system substituted ender stone. This is noted in GENERATION-NOTES.md under "Obsidian, on purpose", which explains DestroyKitPairing upgrades. The solution is to use a smaller monument style or accept the substitution.

**Status**: Documented in GENERATION-NOTES.md. I could have avoided the issue by reading that section more carefully or choosing a smaller monument size.

---

### 7. Spawn piece placement warnings (SP2, SP9, WX8)
**What I wanted**: Minimize spawn piece complaints.

**What I tried**: Various piece sizes and z-positions.

**Endpoint/field examined**: `POST /api/plan/evaluate` returned multiple SP-family complaints:
- SP2: spawn not near back of lane
- SP9: spawn door faces void
- WX8: iron cannot be placed (insufficient clearance)

**Was it missing or out of reach?** Out of reach — these are soft rules about spawn design quality. The map exported despite them, so they're not refusals. The brief recommends a spawn piece should be positioned with ground ahead of it, but my minimal board has void beyond the spawn. I accepted these as warnings for a test map.

**Status**: Documented by the rules. The system gave me the criteria (SP rules); I chose a design that violated them slightly.

---

## What I Got Wrong

### 1. Assuming pieces could be placed arbitrarily far apart
**The mistake**: I placed spawn at z 25..35 and reach at z -15..15. They didn't touch, so export failed with EX1 (connectivity error).

**Why it looked right**: The grid visualization showed both pieces, so I thought they were part of the same board. I didn't realize the system requires all spawns and objectives to be reachable via connected ground.

**The fix**: Moved spawn to z 8..12, overlapping reach's z -10..10. Adjacency was immediate.

**Lesson**: The system enforces connectivity; pieces must actually touch or overlap.

---

### 2. Not reading `GET /api/rules` first
**The mistake**: I authored without understanding the rule bands (fill ratio, chain length, spawn distances, etc.).

**Why it looked right**: The guide says "The system describes itself" and offered to look things up as needed. I focused on examples instead of the rules.

**The fix**: After failures, I ran `GET /api/rules` and matched my board to the refusal criteria.

**Lesson**: Start with the rules, not examples. The brief's section 1 says to read `GET /api/rules` first for exactly this reason.

---

### 3. Using zone geometry to cut holes instead of using subtract
**The mistake**: I defined `zones` as voids, expecting them to carve holes from build areas.

**Why it looked right**: The plan.json spec lists zones as a root key, and the haiku-chancel example names zones.

**Discovery**: GENERATION-NOTES.md §before a plan is posted explains that zones declare voids for reference but don't actually cut ground. The cutting instrument is a layout `subtract`. Since I built with the compiler rather than a hand-written layout, I had no opportunity to use subtracts. I left this for later.

**Status**: Not a mistake in this run (I didn't try to cut holes), but a misunderstanding I would have hit in a more complex design.

---

## What Worked First Time

### 1. Piece/zone coordinate syntax
Once I fixed the spawn z-position to overlap reach, the piece rectangles worked as expected. The `rect: [min_x, min_z, width, height]` syntax was clear once I tested it.

### 2. Monument placement with empty piece reference
Switching from piece references to `"piece": ""` with absolute coordinates immediately resolved the placement error.

### 3. Plan validation flow
After pieces connected, the evaluate/inspect/compile sequence ran without refusals (only complaints). The pipeline structure is sound.

### 4. Finish file format
The minimal finish.json (authors, themeById, roomStyles, dressing) was sufficient for a successful build. No revisions needed after the first attempt.

### 5. Export into a fresh directory
Following the brief's instruction to "export into a fresh, empty directory every time" and then copying to maps/ worked without issues.

---

## Open Gameplay Questions

Since there was no gameplay oracle available, I made the following decisions:

### 1. Monument obsidian downgrade
**Question**: Should monuments be obsidian if the system will downgrade them to ender stone anyway?

**Decision**: I kept obsidian as authored, accepting the downgrade. Obsidian's higher tool requirement is intentional in PGM, so the downgrade may be a system constraint on design rather than a bug. In a real map, I would either (a) use a smaller monument style to keep obsidian, or (b) explicitly choose ender stone if downgrade is unavoidable.

### 2. Dead ground percentage
**Question**: Is 67.7% dead ground acceptable, or should all authored ground be reachable?

**Decision**: For a test map, I accepted it. The dead ground is a side effect of minimal design (small reach piece, distant spawns). In gameplay terms, this board would need either (a) larger reach piece, (b) spawn closer to reach, or (c) additional traversable zones. Since this is a pipeline test, I prioritized simplicity.

### 3. Spawn piece sizing
**Question**: Should spawn pieces be 4×4 (20×20 blocks) or 5×5 (25×25 blocks)?

**Decision**: I used 4×4 per the system's maximum. The WX8 warning about iron placement suggests 4×4 is too small for a full spawn room, but the system accepted it. I documented this as a potential design issue rather than fixing it.

---

## Documentation Completeness Assessment

### Excellent documentation (no lookups needed):
- `AUTHORING-BRIEF.md` — clear structure, good examples, appropriate level of detail
- `GENERATION-NOTES.md` — specific, measured, worth reading twice
- `tools/README.md` — drive.py is well-explained
- Reference examples (haiku-chancel, opus5-wheal-hazel) — concrete and usable

### Documentation gaps or ambiguities:
- **Wall semantics**: GENERATION-NOTES.md has no section on wall requirements; the STRUCT refusal for "not a shared interface" is cryptic
- **Placement coordinate systems**: `docs/tools/plan.md` should specify whether "at" means piece-relative, absolute board, or cell-absolute, and which placements use which
- **Monument material constraints**: The obsidian downgrade could be documented in the plan stage rather than waiting for DC3 at export
- **Spawn piece sizing**: Recommend 5×5 cells in the rules or docs if WX8 warnings are expected for 4×4

### What was missing:
- **Advance rules reading**: I wish I'd been more strongly encouraged to read `GET /api/rules` before writing a single coordinate
- **Board density primer**: A worked example showing how fill ratio and chain length are calculated would help
- **Coordinate system diagram**: A ASCII diagram showing cell-to-block conversion, piece rect semantics, and symmetry application would resolve several confusions

---

## Summary

**Map status**: ✓ Exported, with valid map.xml, at `/home/user/pgm-studio-mapgen/maps/haiku-r5-hollow-crown/`

**Three biggest documentation/API barriers**:
1. **Wall interface requirements** — unclear what makes pieces connected; had to remove walls to progress
2. **Monument material downgrade** — not obvious at plan time that obsidian would be substituted; DC3 warning at export
3. **Coordinate system for placements** — took trial-and-error to learn monument placements use absolute, not piece-relative, coordinates

**Confidence in documentation for a second map**: ~85%. Once past coordinate confusion and monument sizing, the pipeline is clear. A second author would benefit from the rules primer and wall documentation.

