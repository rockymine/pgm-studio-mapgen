# ClayClay recreation — what the system could and could not say

A recreation of `CommunityMaps/ctw/clayclay` authored as a plan document and driven through the
studio's own API (`tools/build.cs`), not through `tools/mapgen`. This records what matched, what
did not, and where the gap sits.

## What the original is, measured

Read off the world with `--island-sketch`, `--surface`, `--structures` and a column probe, not
guessed from the XML.

- **`rot_180` about world (47, 15)** — confirmed independently by the observer spawn at `47,53.2,14`.
- Two **plus-shaped islands** of 13-wide bars, plus two detached **13×13 caps**.
- **Four ~21-block void hops** chaining cross → cap → cross. The kit's 64 stained clay is the bridge.
- Ground almost flat: median y12, p10–p90 12..16. `maxbuildheight` 26.
- Built entirely from **stained clay** (id 159), one column being
  lime / light blue×2 / blue×2 / light blue×4 / black / clay(82)×5 / bedrock.

### The spawn approach

Measured east from the spawn platform along the bar (identical at z=−14 and z=−4, so it is a clean
ramp across the full width):

| world x | surface y | depth |
|---|---|---|
| −24..−8 | 15 | the spawn platform, acacia building on it |
| −7..−4 | 14 | **4 deep** |
| −3..1 | 13 | **5 deep** |
| 2.. | 12 | the field |

## What the recreation reproduces

| | ClayClay | Recreation |
|---|---|---|
| Extent | 142×158 | **142×158** |
| Symmetry | rot_180 | rot_180 |
| `maxbuildheight` | 26 | 26 |
| Spawn approach | 15 → 14 (4 deep) → 13 (5 deep) → 12 | **identical** |
| Void hops | 4 × ~21 blocks | 4 × 21 blocks |
| Material | stained clay throughout | stained clay throughout |
| Traversability | — | 3 components, 2 markers, **0 isolated** |

Ground tone shares (recreation vs original): verdant 43.6/25.4, azure 28.2/23.2, dark 12.0/17.3,
slate 8.0/6.1, mauve 1.6/11.9. The top course is deliberately hot on lime and short on light blue —
light blue is present but sits under the surface course rather than on it.

## The three things that made it work

1. **`cell: 1`.** The steps are 4 and 5 blocks deep, and no cell size above 1 can state both. At
   `cell: 6` the geometry was 144×156 and the steps were unrepresentable; at `cell: 1` the plan is
   block-exact and lands on 142×158. A plan rect is a multiple of `cell` in every direction, so
   **`cell: 1` is the escape hatch for tracing a real map** and costs nothing but larger numbers.

2. **Driving the API rather than mapgen.** A `MapSpec` theme names a *palette family*, and `solid`
   resolves a family to its **first** entry. Of the sixteen stained clays only lime (`159:5`, first in
   `verdant`) and cyan (`159:9`, first in `slate`) are reachable; ClayClay's dominant blue `159:11` is
   third in `azure` behind blue wool, and black `159:15` second in `dark` behind nether brick. The
   first mapgen build came out dark prismarine and nether bricks. Compiling the plan and injecting
   `themes` / `mapTheme` / `roomStyles` into the layout before `PUT /sketch/from-plan` — exactly
   `SketchLayout.FinishKeys` — reaches every block.

3. **Nesting `cell` inside `layered`.** A layer stack renders as one flat colour from above, which is
   what the docs say and what the first attempt looked like. Because every material kind nests, the
   stack's **top layer can itself be a `cell` pattern** — patchy top course, layered depth below.

## What could not be done

### A tree cannot be made of anything but wood

ClayClay's caps each carry a **stained-clay tree**: brown clay trunk (`159:12`), green clay canopy
(`159:13`) at y22–25, dark oak stair branches. A `TreeProp` carries a **wood name**, resolved by
`DressingPalette.WoodNamed` against `DressingPalette.Woods` — a closed six-entry table of
`(name, logId, logData, leafId, leafData)`. The wire carries the name, not the blocks, so no tree of
any other material is placeable. The terrain half of the library is fully block-addressable; the
dressing half is not, and the asymmetry is the gap.

Everything else on those caps *is* reachable — the layered column under them was reproduced exactly.

### A wool always fans team-outer

ClayClay puts red's spawn, red's monument **and** the wool red fetches all on the same cross; the run
never crosses the void and the contest is blue raiding to stop it. `plan.md` states each wool fans
team-outer and the compiler has no override, so the recreation puts the wool on the enemy cross.
(Filed already, and not important per the author — recorded only because it is the one *structural*
thing the plan could not say.)

### No renderer shows a vertical section

All six renderers are plan-view. `--underground` looks like the exception but reports *enclosed
space* — on a solid clay board it found only the 36 room-interior columns. `layered` exists precisely
to vary down a riser and **no picture can check it**. `structures.png` additionally merges a building
into the ground when the two share a material, which is the normal case for a single-material map:
the original's rooms separate, the recreation's do not.

`tools/column-probe.cs` was written for this and prints one column top-to-bottom. It is what verified
the layer stack, the step heights and the stamped room.

### Smaller notes

- **`surface: N` puts the top block at `y = N−1`.** Every height was one low until corrected. Worth a
  sentence in `plan.md`, since a plan tracing a real map has to match absolute heights.
- **`globals.maxPlayers` lands per team.** `26` produced `max="26"` on each team; ClayClay is 13 a side.
- `--structures` describing a same-material building as terrain is the measurement fault that would
  make an automated check of a themed map read wrong.

## Reproducing

Needs the API running (`dotnet run --project src/PgmStudio.Api`) and a migrated database.

```bash
dotnet run tools/build.cs -- specs/clayclay.plan.json specs/clayclay.theme.json \
                            specs/clayclay.room.json "ClayClay" out.zip
dotnet run tools/column-probe.cs -- maps/clayclay/region -54 -24 -50 -24
```
