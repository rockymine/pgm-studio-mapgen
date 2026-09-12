# Talltimber Yard — the canonical brief, built

> Two rival logging outfits, each running a small timber yard around a tall counting-house where their
> ledger-core is kept, and the two yards face each other across the felled ground between them.

90 × 230 blocks, `rot_180` about the origin, cell 5, base surface 9. One relief group ("team"), fused from
a spawn piece and a yard piece at one surface, y 7..12 over most of the board.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy, a core per team | `<cores><core team="red" name="Ledger" material="obsidian" leak="6">` | anchor `(17, 9, -62)`, 5×5×5 obsidian casing over 3×3×3 lava, `float 5`/`leak 6` — players dig 2 |
| one tall counting-house, two wings | `talltimber-hall`: an 11×13 hall (4 storeys, hip roof) plus a touching 8×5 lean-to (gambrel roof) | `POST /terrain/prop-preview` validated the joint before the build; wings share the edge `x -6/-5` over `z -62..-60`, no `HJ*` refusal |
| timber construction throughout | log corner posts (spruce) on all three styles; laid-log courses under the checker bands; a two-species log checker (oak/spruce, then oak/birch, then birch/jungle) | `talltimber-hall.json`, `talltimber-cottage.json`, `talltimber-store.json` in `tools/styles/` — `footing: null` on all three |
| one or two smaller buildings, human scale | `cottage` (9×9, gable) and `store` (9×9, hip) — the same family repainted, forked from the `cottage` preset | `dressing.props[1..2]` |
| paths, solid, three-colour triad | four `stroke` props, `style: "solid"`, `pave` a `cell` of Dirt/Coarse Dirt/Spruce Planks, `claimsGround: true` | spawn door → the two small buildings → the hall's door → the ledger's plaza |
| sparse street trees | 3 template oaks per side, height 9 | `06-claims.txt`: placed 20, declined 0 |
| void between the yards, build-zone-spanned | `zones: [{"id": "clearing", "rect": [-9,-3,18,6]}]` compiles to `build.areas`; `voidEnforcement: true` denies the void everywhere else | `CT12` strait 30 blocks; column at `(13, 0)` reads void |

## The three numbers a destroy goal is held to

| Rule | Band | Measured |
|---|---|---|
| `GO1` (enemy ÷ own walk) | [3.0, 4.0] | **3.76** |
| `GO4` (own-spawn walk) | [40, 90] | **46** |
| `GO3` (opposing-goal walk) | [85, 150] | **139** |

All three land comfortably inside their bands on the first plan that reached `/plan/inspect`, because the
five numbers — spawn at `z -95`, the hall at `z -68..-56`, the core 6 blocks past its wall — were solved
algebraically first (`d_own = 46`, `ratio = (L+d)/(L-d)` for `L` the spawn-to-spawn half-distance) and only
then drawn.

## The house, and the joint

The counting-house forks `room-styles/9` ("counting house"), which is already a four-storey hip-roofed hall
with log posts and a noise-and-checker ground floor — the closest shipped preset to the map's own name. The
fork:

- drops `footing` to `null` on all three of this map's styles (never state one);
- repaints the top-level wall and all three storeys' walls in laid spruce log and an oak/spruce log
  checker, rather than the preset's plank-and-sandstone stack;
- adds `beams` (spruce, matching the post) — which is what taught the first refusal: `HS4` refuses a beam
  species that disagrees with the post or with any plain laid-log course, because "a post, the beam ends
  docking against it and the course they are the ends of are one frame." The style started with oak beams
  over a spruce post and a birch top-storey course; all three now agree on spruce.

The lean-to wing states only `{"form": "gambrel"}` and wears everything else the hall does — the technique
`showcase/17-houses`' barn uses. Its own proportions (8 wide by 5 deep, ridge along the shared edge's
perpendicular) tie its ridge into the hall's wall without an explicit `ridge` override, which is what keeps
`HJ3`/`HJ4` from firing: stating one would have been guessing at a rule the geometry already satisfies.
`RoofForm.Shed` is not used anywhere on the map.

## The ledger is beside the hall, not inside it

The brief's own core-in-a-building's-base idea runs into a real mechanical wall: `OB19`'s dressing rule
holds a tree, a boulder **and a building** at least ten blocks from a goal's own marker, and a building
within that ring is declined outright rather than built smaller. No footprint under the 192-block wing
cap can have every wall ten blocks from its own centre, so a goal genuinely enclosed by a building's walls
is not buildable at all. The ledger sits in a small worked-dirt clearing at `(17, -62)`, twelve blocks off
the hall's east wall (`x = 5`) and twenty-three off the lean-to's — held by the counting-house rather than
under it, with a swept path running to it and nothing else standing near. This is recorded as an open
question rather than a silent substitution: see the report's own section on it.

## What the ground is made of

Two themes, the way the brief asked for — a worked camp and an open clearing — plus the buildings' own
timber and stone:

| Theme | On | Says |
|---|---|---|
| `yard-worked` | the camp, spawn to the hall | a slope-banded `layered` stack: Dirt/Coarse Dirt/Gravel over two Coarse Dirt on the flat, Coarse Dirt/Gravel/Andesite on a shoulder, Stone/Cobble/Andesite on a face — packed ground, worked hardest near the buildings |
| `felled-open` | the strip toward the void, `z -40..-15` | Grass Block (weighted two of three) and Coarse Dirt over two Dirt on the flat, the same shoulder-then-face bands past it — a clearing rather than a lawn |

`05-themes.txt`: 71.2% `yard-worked`, 28.8% `felled-open`, one border of 180 cells between them, and no
seam in a transect through it (`z -45` to `z -10` at `x 0` reads a flat `10` the whole way).

## The paint patch that would not paint, and what actually fixed it

The documented technique for scoping a second theme onto solved ground — `GENERATION-NOTES.md`'s "A paint
patch on solved ground is an ordinary one-course add, not an override" — is `operation: "add"`,
`base_height: 1`, no `override`, on the theory that the smallest-area shape wins the paint and the group's
solved relief repairs the height back regardless. On this board, on a group that carries a relief, it did
not: a plain `add` patch (and, tested separately, an `override: true` one) both painted zero cells at every
size tried, down to a bare `solid` swap to an unmistakable block. The census read 100% of the ground as the
map default no matter what the patch's own theme said.

What worked was the SK14 message's own suggestion: `"relief_scope": "exclude"`, with `base_height` stated
to match the group's own solved height (10, read off `relief/read`) so the patch's own flat plate sits flush
with the ground around it rather than opening a face. That produced the 180-cell border above with no step
in a transect. This reads as a real behaviour difference from what the notes describe for a relief-carrying
group, not a mistake in how the patch was authored — both forms in the notes' own table were tried and
measured, not guessed at — and it is written up as a finding in the run report rather than assumed away.

## Techniques used

- **A plan solved for the three GO bands before a shape existed.** Own distance, ratio and opposing-pair
  distance are three equations in the spawn's, the hall's and the core's positions; solving them first
  meant the first `/plan/inspect` came back in every band.
- **The wing joint was validated with a preview, not drawn and hoped for.** `POST /terrain/prop-preview`
  answered the L-shaped footprint and its two roofs before a map row existed, the way
  `docs/tools/library.md` recommends.
- **A road forks rather than crossing a building.** The first draft ran one stroke from the spawn straight
  through the hall to the ledger; `DR-CROSS` named it — "the way through is now two dead ends at a
  building." The fix is two strokes sharing a point outside the hall's wall, one ending at its door and one
  routing round its east flank to the plaza.
- **A void gap authored by arrangement, not by subtraction.** The two team pieces simply stop six cells
  short of the axis; nothing was cut. A `zones` rectangle over the gap is the only thing that makes it
  bridgeable, and `voidEnforcement: true` is what keeps the rest of the board's edges from being bridgeable
  too.

## What went wrong, and was fixed before shipping

- **`HS4`** (beam/post/laid-log species had to agree) — fixed by bringing every log in the hall to spruce.
- **`PT4`** (a `cell`/`voronoi` material on `wall`/`fill` needs a `rise` or it stripes vertically on a cut)
  — fixed by stating `rise: 3`–`4` on both themes' wall and fill patterns.
- **`PT1`** (a surfacing block — grass — cannot be a bare multi-course pick) — fixed by nesting the
  flat-slope band as its own two-band depth stack, grass on top of two courses of dirt.
- **`ST9`** (the spawn's default footprint, 28×14, is over the 20×20 building cap) — fixed by stating an
  explicit `[5, 3, 20, 14]` footprint on the spawn placement.
- **`DR-CROSS`** — the road-through-the-hall fault above.
- **The felled-open paint not applying at all** — the `relief_scope: "exclude"` fix above.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-iso.png` / `world-iso-turned.png` | the whole board: two symmetric yards, the void gap between them, the worked camp reading brown against the felled clearing's green |
| `renders/world-surface.png` | the two ground themes and their shared border, by material family |
| `renders/house-counting-house-section.png` | the hall's four storeys and its hip roof, forked from the counting-house preset |
| `renders/world-topdown.png` | role-coloured plan: the core (red), the hall and its two small neighbours, the trees |
| `renders/theme-yard-worked-surface.png` / `theme-felled-open-surface.png` | the two ground patterns on their own |

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red spawn | `(0, -105)`, facing `+z` | footprint `[5,3,20,14]`, styled `@talltimber-cottage` |
| red ledger core | `(17, 9, -62)` | obsidian 5×5×5 over 3×3×3 lava, float 5, leak 6, dig 2 |
| counting-house hall | `x -5..5, z -68..-56` | 4 storeys, hip roof, `talltimber-hall` |
| counting-house lean-to | `x -13..-6, z -62..-58` | gambrel roof, touching the hall at `x -6/-5` |
| cottage | `x 20..28, z -88..-80` | gable roof, door facing `-x` |
| store | `x -30..-22, z -86..-78` | hip roof, door facing `+x` |
| void gap | `z -15..15`, full width | build-zone-spanned, `CT12` 30 blocks |
| worked/felled seam | `z = -40`, `x -45..45` | 180-cell border, flat transect both sides |
