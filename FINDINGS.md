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

## Answering the review

`review/clayclay_redux.md` raised five points. Three were fixed; two are confirmed inexpressible, and
one of the fixes is only approximate.

**The side pattern was wrong and is now measured.** A column probe of the real wool room's edge gives
it exactly, and the theme's `wall` stack was rewritten from it:

| course | ClayClay | Recreation |
|---|---|---|
| rim | blue stained clay ×1 | same |
| | light blue ×3 | same |
| | cyan ×1 | same |
| | gray ×1 | same |
| | black ×1 | same |
| | nether brick ×1 | nether brick ×2 |
| | nether brick **stairs** ×1, one facing | — |
| rest | clay (82) | same |

The stair course is the one miss. A `layered` layer takes a *material*, and a material resolves its
own data from where the cell sits — which is exactly why the library picks windows and rails as
blocks rather than styles ("their metadata is geometry, not material"). A course of stairs all facing
one way cannot be stated, so it is laid as a second course of plain nether brick.

**The houses were in the wrong style and are now the map's own.** Probing the real wool house gives
hardened clay and bricks alternating up the wall, orange stained clay posts, **dark oak fence as the
window** (four courses, y13–16), red sandstone and red sandstone stairs over it, and a light gray clay
cap. The room style is rebuilt from that — the wall body is a `checker` of hardened clay against
bricks, the window is `pane` with block 191, and the roof is red sandstone with a `roofSlab` of red
sandstone slab. The rooms now read as their own structures again (169 area, roof y20..32, red
sandstone 40%), where before they dissolved into the ground.

**The bedrock wall is placed, but it is not the same wall.** The interface it wants already existed —
`wool-room` meets `north-lane` at rel z −67/−66, which is precisely where the real bedrock sits — so
it needed a `walls` entry rather than a split. What stamps there is the plan's own barrier: **two
blocks thick and three courses tall**, per `plan.md`. ClayClay's is **one block, one course** at y12,
a threshold rather than a barrier. `walls` has no thickness or height knob, so the intent is
expressible and the dimensions are not.

## What could not be done

### A tree cannot be made of anything but wood

ClayClay's caps each carry a **stained-clay tree**: brown clay trunk (`159:12`), green clay canopy
(`159:13`) at y22–25, dark oak stair branches. A `TreeProp` carries a **wood name**, resolved by
`DressingPalette.WoodNamed` against `DressingPalette.Woods` — a closed six-entry table of
`(name, logId, logData, leafId, leafData)`. The wire carries the name, not the blocks, so no tree of
any other material is placeable. The terrain half of the library is fully block-addressable; the
dressing half is not, and the asymmetry is the gap.

Everything else on those caps *is* reachable — the layered column under them was reproduced exactly.

### A surface has one rim, not a stack of them inward

ClayClay's ground is four concentric bands walking inward from the edge: brown and gray stained clay
at random, then light blue and cyan at random, then dark oak and nether brick at random, then a fill
of random grass and lime. A theme has exactly **one** `rim` bucket, and its `depth` counts *courses
downward*, not rings inward — so the model has no way to say "a second band one ring in from the
first". The recreation paints the innermost band only (random grass and lime), which is most of the
area and the right reading of the map from above, and loses the three borders.

This is the one gap here that is a genuine hole in the *model* rather than a missing knob. Everything
else on this list is a field that could be added to an existing shape; concentric banding is a second
axis the painter does not have.

### A wool's sky marker cannot be stated

Above the real wool sits a **3×3×3 of stained glass with a wool block at its centre**, at y39–41 —
the beacon that says where the objective is from across the map. Nothing in the intent or the
structure directives places a volume over a wool; the wool marker resolves to the wool block and its
room, and the studio's own shell is the cage around it rather than anything above it.

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
dotnet run tools/build.cs -- specs/clayclay_redux.plan.json specs/clayclay_redux.theme.json \
                            specs/clayclay_redux.room.json "ClayClay Redux" out.zip
dotnet run tools/column-probe.cs -- maps/clayclay_redux/region -54 -24 -50 -24
```

## Naming

The map is `ClayClay Redux` in `map.xml` and `clayclay_redux` on disk, not `ClayClay`. A recreation
that keeps the original's name gives a PGM server two maps with one identity as soon as this repo
sits beside the community corpus. The name the server reads comes from the plan document's
`meta.name` — the folder, the map row and the `POST /plan` name are all separate from it, so renaming
the folder alone leaves the clash in place.
