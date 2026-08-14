# Basalt Reach — a destroy board where the relief does the work and a subtract makes the decision

**In one sentence:** a black basalt wave-cut platform with three sea stacks standing out of it, cut across by
a channel that reaches from the west edge almost to the east, so every attack goes round one of two
isthmuses — a dark oak wood on one, open rock on the other — to reach a monument on a stack or a core sunk in
a yard behind.

150 × 204 blocks, `rot_180` about the origin, base surface 12, build ceiling 38. One landmass; the halves
overlap across `z = ±14`.

**Built as the opposite of `marlstone-steps` on purpose.** That board is five flat tiers with the relief
reaching one of them; this one is a single relief-solved platform with erected shapes standing out of it. The
readback numbers say it plainly: Marlstone's relief covers 4 294 cells, Basalt's covers **7 184** of a
comparable board. Two ways of making ground, one map each, so the pair can be compared.

## The board

| Shape | `base_height` | Mode | Theme | What it is |
|---|---|---|---|---|
| `reach` | 12 | relief | `basalt-reach` | the wave-cut platform, Bézier coastline, rim **off** |
| `channel` | — | **`subtract`** | — | the hole; resolves in plan only, so it states no height |
| `skerry` | 4 | `raise` | `basalt-stack` | a knuckle in the contested mid |
| `stack-e` | 6 | `raise` | `basalt-stack` | the east stack, on the east isthmus |
| `stack-w` | 8 | `raise` | `basalt-stack` | the west stack — the monument stands on it |
| `works` | 15 | `exclude` | `basalt-works` | the back platform and its settlement |
| `yard` | 3 | `sink` | `basalt-yard` | a sunken yard; the core sits in it |
| `back` | 18 | `exclude` | `basalt-back` | the spawn shelf, Bézier north edge |
| `ramp-w`/`ramp-e`/`ramp-back` | — | `level` + tilt | `basalt-works` | three tilted planes joining the tiers |

Five themes over eleven shapes, all inside one dark palette — andesite and polished andesite, cobble, gravel,
stone brick, with orange hardened clay as the lichen band in the stacks' strata and the yard's rim. The rim is
**off** on `reach` and the stacks (grown) and **on** for the three built tiers.

## Where the objectives are, and what each costs

| Objective | Position | Sits on | Measured |
|---|---|---|---|
| red destroyable "Red Stack" | `(-40, 26..28, 35)` | `stack-w`, top y21 | obsidian `cube-3`, `float 4`, on a bedrock plate at y20 |
| red core "Red Sump" | `(30, 17..21, 60)` | `yard`, floor y11 | obsidian shell over lava at y18–20, `float 5`, `leak 8`, **`digDepth 3`** |
| blue | `rot_180` images | | |

Both goals are **obsidian**, and that is a deliberate test rather than a palette choice: the kit that ships
with the map carries a **`diamond pickaxe`**, because `DestroyKitPairing` reads the hardest material any goal
needs and upgrades the tier. The previous run chose end stone to work around a gap that had already been
closed; this board takes the gap at its word and the pairing holds.

`<gamemode>dtm dtc</gamemode>`, objective line *"Destroy the enemy's monuments and leak the enemy's cores!"* —
the first board in this repository whose `map.xml` says what it is. Every earlier destroy board here ships as
`ctw`.

## The channel, and the decision that goes with it

The `channel` is a `subtract` polygon reaching `x −52 … 38` across `z 11 … 29`, with Bézier controls on its
two long edges so it reads as water-cut rather than ruled. Probed at `(−30, 20)` and `(20, 20)`: **0 solid
blocks at any height.** It leaves two isthmuses — **west, x −75…−52 (23 blocks)** and **east, x 38…75 (37
blocks)** — and because the board is `rot_180`, each team's wide way round is the other's narrow one.

**It is permanent, and that is stated rather than inherited.** The map declares **no build areas at all**, and
carries `build.voidEnforcement` with empty exclusions, which projects to:

```xml
<everywhere id="void-enforcement-area"/>
<apply block-place="deny(void)" region="void-enforcement-area" message="You may not edit the void!"/>
```

This is the first map here to use `B132`'s standalone enforcement. It matters because the previous run
discovered that a board with no build area gets **no void rule at all** — the channel was bridgeable from the
first tick, the exact opposite of what "no build zone" reads as — and worked around it by declaring a
90 × 10 build zone over land that changed nothing. That workaround is retired: the two are now independent
decisions and this board makes both explicitly.

One caveat found in the same breath: **the plan cannot say it.** `PlanModel` has no field for void
enforcement and `PlanCompiler` never emits one, so a compiled intent always carries `voidEnforcement: null`.
Reaching the capability means editing the compiled intent before `PUT …/intent/from-plan` — a one-line patch,
but out of reach from where the plan tool stands.

## How it is meant to play

**Two approaches that differ in kind, one per isthmus.**

*West, through.* Fourteen dark oaks stand over the narrow isthmus and the ground south of it, with fern and
tall grass under them. A player crossing there is unseen for the last forty blocks and arrives at the foot of
`stack-w`, which the monument stands on. It is the early approach and it costs nothing but time —
`approaches.md`'s reading of what a forest is for, and the canonical brief's "a forest closing the flank",
built on the flank that actually matters.

*East, open.* The wide isthmus is bare basalt with a boulder field and two tidal pools. There is no cover on
it at all, and it leads to the works and the core rather than to the monument. It is the expensive approach
and the one a defender can watch.

**The two goals are unlike in every dimension**, which is `approaches.md`'s "placed against each other rather
than scattered": the monument is forward, west, high on a stack and broken with a pickaxe; the core is back,
east, sunk in a yard and needs three blocks of ground opened under it after the casing goes. A defence that
holds one is not holding the other.

**The skerry is why the mid is not a field.** A `raise` knuckle at the centre of the contested platform with
twelve boulders and two pools around it — enough to break the sightline across ninety blocks of open rock
without giving anyone cover near a goal.

**Circulation, drawn first.** Seven paths: the works street, the spawn descent, one on each of the three
ramps, and one down each isthmus (`rough` edged, 0.85 coverage, so they read as worn tracks rather than
roads). The wood and the boulder fields are what is left over.

## Techniques, and what each bought

**A `subtract` is the only instrument that cuts a hole**, and it resolves in plan only — no `base_height`, no
height mode. It is what makes this board a decision rather than a field.

**A goal on ground authored once.** Both objectives name an empty `piece` and an absolute `at`, so
`stack-w` is a `raise` polygon with per-vertex `anchor_heights` and nothing manufactured a plan tier to carry
a marker. The monument's height resolved from the terrain the rasterizer actually built.

**Bézier on a coastline.** `reach` carries controls on five vertices and `back` on two. The board reads as a
landmass with a shore rather than a rounded rectangle, and the same technique on the `channel`'s long edges is
what stops the hole reading as a trench.

**One relief, four excluded tiers.** `reach` takes the whole solve — a rim mark, an area mark holding the mid
flat where the halves meet, two point swells, a dished hollow behind the west stack (`amount −4`, `crown −1`)
and a tilted shelf east (`amounts [4,3,2,3,4]`). Readback: 7 184 cells, y7 to y20, **2 cliffs**, 98.5 %
walkable at a one-block step, `symmetryError 0`.

## What went wrong

**Four of five houses were dropped, silently, and the export was clean.** `Decorator.PlacePath` adds every
band cell to the `taken` set and `PlaceHouse` returns 0 for any footprint touching one — for both orbit
images, with nothing logged and no refusal. Measured on the first dressed build:

| House | footprint | the path that claimed it | band | stamped |
|---|---|---|---|---|
| `w1` | `x −45…−37, z 64…72` | — | — | yes |
| `w2` | `x −34…−25, z 64…71` | `p-ramp-back` at `(−26, 70)` | `x −28…−24, z 68…72` | **no** |
| `w3` | `x −22…−14, z 64…73` | `p-ramp-back` at `(−22, 63)` | `x −24…−20, z 61…65` | **no** |
| `w4` | `x −11…−3, z 64…70` | `p-spawn` at `(−8, 66)` | `x −10…−6, z 64…68` | **no** |
| `w5` | `x 0…7, z 64…72` | `p-spawn` at `(0, 72)` | `x −2…2, z 70…74` | **no** |

Found by probing each house's centre and reading the works' own surface palette where a floor should be. This
is the fault the previous run documented and it is **still live on the current build** — the three commits
that landed during this run about what a building claims changed the house side of the collision, not the
path side. Fixed authorially: the settlement moved to a block with no path through it and every house now
reads a floor at y14 and a roof at y22 (`shed`) or y24 (`hall`).

**A tree over void is skipped, and the foliage read-back still counts it.** `s1` was authored at `(−46, 74)`,
which is outside the `works` polygon at that z — `(−46, 74)` probes as 0 solid blocks. Nothing refused it, and
`--layer foliage --dressing` reported "34 tree(s)" either way, because that count comes from the **document**
rather than from what stands in the world. A prop count from that render is not evidence a prop was placed.

**`species: "dark_oak"` produced oak logs.** The wood's trunks read `17:12` (oak log) and `18:4` (oak leaves)
rather than `162`/`161`. The trees are the right shape and size — nine-block trunks under a broad crown — so
the species is selecting a template, but the blocks it is built from are oak. Recorded as a measurement rather
than a diagnosis; I did not read the tree corpus to find out whether that is intended.

**The objective line counts across both teams.** One destroyable *per team* gives
`intent.Destroyables.Count == 2` and therefore "monument**s**" plural. On a board where each team destroys one
monument the line overstates by one. Cosmetic, and the same arithmetic is right for the wool case.

## Open questions, decided without an oracle

**How wide should the two ways round be?** I made them deliberately unequal — 23 blocks west and 37 east —
so each team's cheap route is the other's expensive one under `rot_180`. Whether that reads as designed
asymmetry or as one team's advantage is a question about play.

**Is a core in a sunken yard fair?** The yard is three blocks below the works, so attackers drop in and are
below the lip while they dig. That makes the core easier to reach and harder to leave, which felt right; I
have no basis for preferring it to a core on flat ground.

**Is `digDepth 3` a task or a chore?** `float 5, leak 8`. The previous run chose the same number for the same
reason — it feels like real work — and neither of us can say why not two or five.

## The renders, in the order they were looked at

`01-topdown`, `02-foliage` (the wood against the bare east isthmus), `03-heightmap` (one relief-solved
platform, contours everywhere rather than terraces), `04-section-x-40` (**the one image that carries the whole
design**: platform, the void channel cut clean through, the stack, the monument floating over it, the works
and its roofs), `05-section-z20` (the channel across the board's width), `06-trav` (2 components, 4 objective
markers, **0 isolated**), `07-surface` (the paint families, which is how the five themes were checked against
each other).
