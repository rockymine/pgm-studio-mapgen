# Siderite Bowl — a crater a team defends from above and behind

**In one sentence:** an iron-shot impact crater where each team's core lies in the bowl it made, the ejecta
ring stands behind the bowl rather than in front of it so the defence looks down into its own goal, and the
only walk between the two is one breach a single player holds.

100 × 210 blocks — the longest lane of the four. `rot_180`, base surface 9, build ceiling 34, ground y5..24.
One island, 5 345 cells, y6..14, relief 8, symmetry error 0.

## The topology is the whole design

`approaches.md`: *"the spawn sits remote at the back, the monument is a short walk forward of it, and the
contested space is everything beyond."* The first draft of this board had the crater behind the ejecta ring —
defenders in front of their own goal, attackers arriving above them. Reversing it is what the board is.

Spawn (`z 85..100`) → shoulder → **rim**, the ejecta ring at h13 (`z 55..65`) → **bowl**, the crater floor at
h6 (`z 40..55`), the core in it → apron → the seam. A defender stands on the rim looking *down and forward*
into the bowl; an attacker crosses the open apron and drops in. That is the destroy topology stated in
elevation rather than in distance.

## Where each thing is, measured

| Thing | Where | Read at |
|---|---|---|
| core | size 5, shell 1, float 6, leak 5, anchored `(−5, 52)` | `(−5, 52)` obsidian y15 and y19 with **lava y16..18 between them** |
| goal-to-own-spawn walk | 50 blocks | `POST /plan/inspect` |
| goal-to-enemy-spawn walk | 150 blocks | ratio **3.0** — `GO1`'s band is 3.0–4.0 |
| the breach | `x −10..5, z 55..65` at h10, the ring's only notch | the ramp below it tilts `6 → 10` |
| the east shelf | `x 20..35, z 40..55` at h8, tilted `6 → 9` | `anchor_heights [6, 9, 9, 6]` |
| two craterlets | circles r5 at `(−22, 26)` and r4 at `(14, 27)` | `(−22, 26)` = **0 solid** — cut to the void |
| the seam | pieces stop at `z = 10`; gap `z −10..10` | 20 blocks, one build zone across |

Traversability: **11 482 navigable columns, 764 bridged over void, 2 components, 0 isolated.**
`<gamemode>dtc</gamemode>`, `<objective>Leak the enemy's core!</objective>`.

## Two ways out of the bowl, and they cost different things

The bowl's floor is at y6 and the ring's crest at y13 — a seven-block face nobody walks. Two shapes make it a
place rather than a pit, and both are `anchor_heights` tilts laid as override-adds:

- the **breach ramp** (`x −8..3, z 47..57`) climbs `6 → 10` into the ring's notch. It is fifteen blocks wide,
  it is the defenders' own line back to their spawn, and one player standing in it can see everything coming.
- the **east shelf ramp** (`x 18..33, z 42..52`) falls `9 → 6` from the apron down into the bowl. It is the
  attackers' way in, it is nowhere near the breach, and it arrives at the far side of the core from it.

The relief does the rest: a **`scarp`** mark along `(−28, 43) → (12, 43)` states the inner face as a *grade*
rather than as a height — `high: 9, low: 6, face: 2, band: 6` — so the ground arrives at the crater lip
through six blocks of fall instead of stepping off it, and an **`area`** mark holds the floor the core stands
on flat at 6 inside its own ring.

The **ejecta blanket** is a `push` with per-vertex `amounts [1, 3, 4, 4, 2]` and a falloff of 9, thrown
thickest over the near shoulder of the apron and thinning west. A push adds to the surface the marks already
solved rather than pinning it, which is why it can sit on top of the scarp's answer without arguing with it.

## The two craterlets are at the seam and nowhere else

Both subtracts sit in the apron's front third, `z 22..32`, where the two sides meet — not between the bowl and
the middle, which is the cut `tallow-kilnrow` made and `approaches.md` withdrew. They are what makes the two
flanks of the apron worth walking to instead of everyone funnelling up the centre.

## What the ground is made of

Five themes. **Ground** is `dark` (the scorched outfield and apron); **built** is `grey stone` (the ring, the
breach, the works); the **accent** is `rust`, and it appears in exactly two places — the crater floor, where
the iron rusted into the ground, and the paving of the attackers' road.

| Theme | On | Says |
|---|---|---|
| `bowl-scorch` | outfield and apron, and the map default | rim off, a `noise` of grey and black clay over coal |
| `bowl-floor` | the crater floor | rim off, a `cell` of orange clay, red sand and coal — the one warm ground on the board |
| `bowl-rim` | the ejecta ring and the east shelf | rim off (it grew), a `cell` of stone, andesite and **iron ore** |
| `bowl-breach` | the notch and its ramp | rim **on** in iron block, and a **`teamTint`** course through its wall — the one place the board says whose crater this is |
| `bowl-works` | the shoulder and the spawn terrace | rim on, a 5-block `checker` of stone brick and cracked |

The wall bucket of the floor and the ring is a **`wallDiagonal`** — stripes sheared by height, so the crater
face's strata climb it rather than standing straight up, which is `AD-R3`'s point that a cliff and a retaining
wall must not read the same.

## The buildings: a boundary, and one place

`C13` names four house idioms none of the twenty-one boards had carried. This board carries the one that
needed a whole new style: a **flat-roofed blockhouse**, `RoofForm.Flat` over a wall of the ring's own stone
with the storey stack emptied, so it is a lid on a box rather than somewhere to go.

| Prop | At | Is |
|---|---|---|
| `h1` blockhouse | `x −31..−24, z 67..73` | six courses |
| `h2` blockhouse | `x −22..−16, z 68..72` | four courses, smaller footprint, same material |
| `h3` blockhouse | `x 19..27, z 67..73` | six courses |
| `h4` assay office | `x 22..34, z 56..63` | an **L** with a projecting wing, on the east ring — a real building, so the run reads as a boundary by contrast |

Three blockhouses differing in footprint and course count while sharing a material is `AD-S2` stated the way
round it asks for: six footprints in one style is a settlement, one footprint in six materials is a swatch.

## What went wrong

**`HJ4` on the assay office's L**, the same square-hall ridge tie that caught the kiln on `alabaster-rake`.
Third L-plan of the run refused for it, and the diagnosis is worth stating once: a roughly square hall ties
its ridge toward x, a wing meeting it on a **vertical** shared edge also runs into that edge, and both-into-it
is `HJ4`. State the hall's ridge along the shared edge.

**A `teamTint` with no `neutral` took the theme preview down with a 500.** `TeamTintedMaterial` is
`{blockId, neutral}` and I wrote `{id, data}`; a neutral cell then dereferenced null. The response called the
fault the studio's own (`RQ2`) when it was the document's. Fixed in the studio this session, so it now answers
400 by name.

## Where it is weak

The apron is the largest flat surface on any of the four boards and the push is the only thing on it. Two
craterlets and a boulder are not enough furniture for 75 × 15 blocks, and the honest reason there is nothing
else there is that it is the ground the fight crosses and I did not want to slow it.

There is no water and no tree on the board at all. The identity is a blast crater and both would be wrong,
but it means the whole board is stone and clay, and the accent is doing a lot of work.

## Open questions

**Should the defenders' way to their own goal be the same one the attackers use?** Here they are deliberately
different — the breach in the back of the ring for the defence, the east shelf for the attack — so neither
side is queuing behind the other. `approaches.md` says a defended goal wants more than one angle onto it and
says nothing about whether the defence gets its own. Built as two; unverified.

**How steep may a goal's own bowl be before the goal is unattackable rather than defended?** The face is
seven blocks and the only walk down is a fifteen-wide ramp at the far end. Chosen by eye.
