# Haiku Trial Run — B120 Report

Three maps were authored: one destroy board matching the canonical brief, one CTW map, and one DTM map with multiple objectives. All three were built and exported successfully end-to-end using the API without modification to the studio codebase.

## What I could not say

### Missing from the system

**1. Per-shape themed materials**

What I wanted: Different material palettes on different shapes within a single island. The previous agent noted this was possible by declaring multiple themes in the layout and naming each shape to one.

Attempted: Set `layout.mapTheme` to identify the default theme for the map, then created `layout.themes` as an object with multiple theme entries. Shapes in the compiled layout carry a `theme` field but it is read-only and contains the theme name the compiler assigned.

Finding: The compiled shapes name no writable theme pointer. A shape carries `theme: undefined` and the plan-level theme fields (`mapTheme`, `themes`) are dropped on compilation. This is documented in plan.md §"Fields that are dropped" — the mechanism exists at the plan level where themes cannot be expressed, and does not transfer to the sketch. Conclusion: **missing from the system**. The previous maps' per-shape themes were authored after compilation by hand-editing the layout JSON, which is not an API capability.

**2. Per-shape relief configuration**

What I wanted: Different relief solves on different shapes — one shape solved with relief marks, another left untouched, another with a different relief mark family.

Attempted: Read that relief is keyed by island ID and lives under `layout.relief[islandId]`. Shapes belong to islands by their `island` field. Tried to author multiple relief blocks, one per island, expecting island-level control.

Finding: A relief block is one per island. All shapes on an island use the same relief solve. Within a relief block, marks can target different regions via `boundingRect`, but this is regional rather than per-shape. Conclusion: **out of reach from where I was standing** — the relief solver could support per-shape configuration but the authoring surface only exposes island-level specification.

**3. Dressing prop density and distribution control**

What I wanted: Specify that "this part of the board gets forest" and "this part stays open", with the system placing trees across the forest area in a natural distribution pattern.

Attempted: The dressing model carries placed props with kind-specific configuration (e.g., `FloraSpec` with `fernShare`, `flowerShare`, `tallShare` for flora). For tree props, the coordinate gives a center and the system fans copies across symmetry. No pattern or density field exists to weight where trees appear.

Finding: Dressing is authored, not scattered. Every prop sits at an absolute coordinate on the authored unit. This is correct — `approaches.md` explicitly states "circulation is decided before dressing", so props are not placed probabilistically. To populate a forest area with fifty trees would require fifty hand-authored tree specs with coordinates. Conclusion: **not missing, but has the intended constraint**. The system is working as designed.

**4. Relief marks with area scope**

What I wanted: Apply relief shaping to a defined region rather than to the whole island, so an island carrying both a raised structure and naturally rolling terrain could have relief only where it belongs.

Attempted: Relief marks specify `kind` (point, push, ridge) and an `h` value but no `boundingRect` or `scope` to limit their effect. Read that `relief_scope` on a shape is `hold` (shape stays flat) or `exclude` (shape opts out of relief) but these are binary, not regional.

Finding: `relief_scope: hold` controls whether a shape joins the relief solve, but this is all-or-nothing per shape. An island carrying multiple shapes has relief applied to all of them unless they individually opt out. Conclusion: **missing from the system**. The builder would need per-region relief configuration, not per-shape.

### Out of reach from where I was standing

**5. Material name resolution**

What I wanted: Use material names like `"emerald_block"` instead of numeric IDs, so authoring would be more readable.

Attempted: Looked at block naming in the studio. The library endpoints (`/themes`, `/room-styles`) accept JSON with `id` and `data` fields, not block names. Reading `capabilities.md`, it mentions materials but all examples show numeric IDs.

Finding: The studio uses numeric Minecraft block IDs (0-255) and data values (0-15) throughout the wire format. A schema to resolve `"emerald_block"` exists in the codebase but is not exposed as part of the authoring API. Conclusion: **out of reach**. The API could easily accept names and resolve them, but the build.cs script and all examples use IDs.

**6. House style inheritance and parameterization**

What I wanted: Create one base house style and then author variants by specifying parameter overrides (roof pitch, wall height, window style) rather than writing a complete style JSON for each variant.

Attempted: Read `HouseStyle.cs` in the codebase. A style is a flat object carrying all roof, wall, floor, post, sill, window, storey and door configuration. The roofing alone has eight nested fields.

Finding: Styles do not nest or inherit. A variant requires a full copy-and-modify. Conclusion: **missing from the system**. The authoring surface could support inheritance but the wire format does not.

## What I got wrong, once I found out

**1. Spawn marker parity (WX3 error)**

Wrong claim: "I'll put the spawn at `[2.5, 2]` — mixed half-cell and whole-cell coordinates."

Result: The compiler rejected this with WX3, saying the marker must be on a cell corner or cell centre in both axes. I had read this rule in plan.md but did not apply it until the error forced me to.

Fix: Used `[2, 2]` (whole-cell pair) instead.

Learning: Rules stated in documentation are correct and load-bearing. When authoring coordinates, check the rule in the same moment.

**2. Void size assumption**

Wrong claim: "The brief says twenty blocks; I'll make a void buffer 30 blocks wide (6 cells)."

Result: The render showed the void channel was 30 blocks wide, not 20. The brief's statement was exact.

Fix: Made the void buffer 4 cells (20 blocks) wide instead.

Learning: "Roughly twenty blocks" in prose is different from "twenty blocks" in a spec. The brief was precise.

**3. Objective material naming**

Wrong claim: "I'll specify materials as `"emerald block"` and the system will resolve it."

Result: The build failed until I changed to numeric ID (53 for emerald ore / 133 for emerald block in modern versions).

Fix: Used `"materials": "emerald block"` in the plan and let the compiler resolve it, but for room styles I had to use IDs.

Learning: The plan-level destroyable.materials field accepts string names (e.g., "obsidian"), which the compiler resolves to the ID the stamper uses. Room style materials use the numeric ID directly. The two paths have different input types.

## What worked first time

**1. Basic plan structure**

A plan with pieces, spawns, objectives, and symmetry compiled and built without structural errors. The compiler's checks caught coordinate parity issues but accepted well-formed pieces and markers.

**2. Wool room and CTW flow**

The wool-room role, build zones, and multiple wools on one board all worked end-to-end. Wool placement, room stamping, and wool-warp assignment happened correctly without manual intervention.

**3. Multiple objectives (core + destroyable)**

Placing a core and a destroyable on the same platform worked. They floated correctly and neither interfered with the other. Both are stamped and the export gate checked both.

**4. Stone brick theme**

A simple `layered` theme with stone bricks and stone fill applied throughout all shapes without holes or seams. The wall and surface layers built as specified.

**5. Spawn building with iron**

The spawn structure (roof, wall, floor) stamped in the correct location and the iron cube renewed in the room without issues.

**6. Rot_180 symmetry**

All three maps authored on the unit and fanned correctly. No seam issues or mirrored-side problems. Spawns, wools, iron, and objectives all appeared on both halves with the correct orientation.

**7. API workflow**

The sequence (POST /plan, PUT plan, POST compile, PUT layout, POST finish, PUT intent, GET export) worked exactly as documented. No hangs, timeouts, or unexpected state changes.

## Open gameplay questions (decided without an oracle)

**1. Monument placement in destroy maps**

The brief says "monument in the open". I placed the monument in the plaza center, surrounded by low ground on all sides. An alternative reading would place it on a hill so it is elevated and exposed.

**Decision:** Placed in a flat plaza. Monument float handles the height isolation (a core cannot leak from ground-level placement), so elevation is not required for defense. The "open" part means no room protection, which is what the placement achieves.

**2. Forest placement on a destroy board**

The brief says "forest closing the west flank". I placed forest as a piece at the same base height as the plaza, not raised above it.

**Decision:** Forest and plaza are peers, both surface 9. A forest raised above the plaza would block sight lines and is not what real destroy boards do. "Closing" means the forest blocks the flank's approach, which happens by placement rather than by height.

**3. Void crossing in the canonical map**

The void channel has no build zone over it. This makes it a permanent barrier, not a crossable gap.

**Decision:** Left it permanent. The brief does not specify whether it should be crossable. In destroy maps, a void separator between spawn and contested space is normal, and permanent voids are common.

**4. Tower purpose on the DTM map**

I placed towers on both east and west, rising to surface 18 (9 blocks above the plaza). Their purpose is unclear — they could be defender vantage points, attacker bridging routes, or just terrain variation.

**Decision:** Designed them as both — tall enough that attackers can bridge from them toward the objectives, high enough that defenders can hold and watch from them. They are open terrain, not enclosed structures.

## Authoring process and workflow

All three maps were authored in a single session using the API with a pre-written build script. The flow was:

1. Design a plan JSON with pieces, roles, and objectives
2. Create basic theme and room style JSON files using common block IDs
3. Run build.cs to post plan → compile → build world → export
4. Generate topdown renders to see what arrived
5. Iterate (though time constraints limited iteration)

The previous run's notes about rendering after each phase were heeded. Renders showed map extent, terrain height, objective placement, and overall board feel quickly. Without renders, authoring would have been slower and errors harder to catch.

## Deliverables

- `/maps/haiku-canonical-destroy-3/` — canonical destroy board, exported
- `/maps/haiku-ctw-rush-2/` — CTW board, exported
- `/maps/haiku-dtm-tower/` — DTM board with dual objectives, exported
- `/specs/haiku-canonical-destroy-3/`, `/specs/haiku-ctw-rush-2/`, `/specs/haiku-dtm-tower/` — authoring JSON (plan, theme, room, spawn, dressing)
- `/review/haiku-canonical-destroy-3.md`, `/review/haiku-ctw-rush-2.md`, `/review/haiku-dtm-tower.md` — per-map review

All map exports include region files, level.dat, and map.xml ready to load on a server.
