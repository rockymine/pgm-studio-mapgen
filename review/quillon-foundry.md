# Quillon Foundry — a core and a stack, on a red hillside

**In one sentence:** a hillside foundry in red rock — brick terraces stepping down from the works stage
to a black casting floor, a furnace leaking into a brick-lined tail race, and a grey slag ridge out on the
ash field carrying a stack of end stone.

148 × 184 blocks, `rot_180`, base surface 14, build ceiling 34. One landmass. Two goals a team, which is
the ordinary combined destroy board (`capabilities.md`: of the seventeen corpus maps carrying both kinds,
sixteen have exactly one core a team).

## The two goals, and why they are not the same problem

`approaches.md`: where a board carries more than one goal they are placed **against each other rather than
scattered**, because their spacing is what decides whether the defence is one line or three. These two are
a west and an east, and they are also a low and a high.

| Goal | Kind | Position | Stands on | Reached by |
|---|---|---|---|---|
| `<Team> Furnace` | core, 5×5×5, shell 1, float 6, **leak 9** | casing `(−27..−22, 22..27, −40..−35)` | the casting floor, y15 | walking the works road down from the yard, or dropping into the tail race and coming up its mouth |
| `<Team> Gantry Stack` | destroyable, `column-plus`, `ender stone` | `(54..57, 28..31, −21..−18)` | the slag ridge, y23 | climbing the ridge from the ash field, or bridging to it from the mid |

**`leak` above `float` is the knob that makes a core an objective.** `float 6` puts the casing six above
the terrain; `leak 9` puts the leak level nine below the casing, which is three blocks *under* the ground.
The compiled intent carries `digDepth: 3`, and `<core leak="9">` reaches the XML. So breaking the casing
is not enough — the lava has to be given somewhere to fall to, and the attackers dig it.

**The stack is the opposite problem.** It is a `column-plus` of end stone on top of a landform that exists
only as an authored polygon, thirty blocks out from anything a defender can hold, with a bedrock platform
buried one course under it (the stamper's own, at y22). Holding it means standing on the ridge; holding
the furnace means standing in the works. A team cannot do both.

## What the ground is made of

Six themes, and the palette is doing one job: red terraces, a black floor, a grey ridge.

| Theme | On | Says |
|---|---|---|
| `foundry-ash` | the field (14) | red grit and clinker, **rim off**, a red-rock riser |
| `foundry-floor` | the casting floor (16) | the black thing on a red map — black clay, coal block, andesite, nether brick, with a nether-brick rim |
| `foundry-yard` | the works yard (18) | brick and red sandstone, the terrace face laid on the **diagonal** |
| `foundry-stage` | the back stage (20) | smooth red sandstone, the cleanest tier |
| `foundry-slag` | the ridge | grey against everything else, which is what makes it read as spoil |
| `foundry-race` | the tail race | brick-lined, because it was built to carry metal |

## The techniques, and what each one bought

**`hold` and `exclude` on the same board, deliberately.** The casting floor is `relief_scope: hold` — it
is pinned at its own level and the ash field ramps *up* to meet it, so the approach from the mid is walked
rather than climbed. The yard and the stage are `exclude` — they keep their own column and meet the tier
below at a face. One board, both joins, and the difference is legible in `05-section-core`.

**The tail race is a `sink` shape, not a tunnel.** `base_height 3`, `skirt 2`: a four-deep brick-lined
trench from the casting floor's foot at `(−30, −30)` running south to the field edge at `(−20, +5)`. The
skirt ramps its ends, so it is a route rather than a pit — a player drops in at the field, walks it
unseen, and comes out at the foot of the terrace the core stands on. That is `approaches.md`'s entrance
**from below** on a board where an overhang cannot be authored at all: the ground layer is the only layer
an agent should write, so "under" has to be modelled as "sunk".

**The cut is a `subtract`**, `x −12..26, z −24..−8`, sitting square in front of the casting ramp so the
straight run at the core is not available. It is not build-zoned, so it is permanent.

**The slag ridge is a `raise` polygon** — 10 above the field, `skirt 2`, tilted by `anchor_heights` — and
it carries the destroyable through an absolute `{"piece": "", "at": [11, -4]}` marker. The landform is
authored once, in the layout, and the goal rides it. That is exactly what the absolute-goal placement was
built for, and it is the thing the previous run had to fake with a manufactured plan tier.

## How it is meant to play

Attackers arrive on the ash field. The cut takes the middle away, so they go west past the slag bank and
the four scrub trees, or east under the ridge. West puts them at the tail race mouth and a covered walk to
the casting floor; east puts them under the stack, which is the cheaper goal and the more exposed one.
Defenders come down the works road from the stage — three seconds to the furnace, considerably longer to
the ridge — so the two goals genuinely pull the defence apart.

## What went wrong

**A claim I nearly shipped, and it was false.** I had this section written as "the core cannot be broken by
the kit this studio writes" — obsidian casing, no material knob, and `capabilities.md` saying in as many
words that "Nothing in the generator ties the two together yet: `TeamsGenerator.GenerateKits` writes one
fixed 'Standard' kit for every map with spawns, an iron pickaxe among its tools, with no branch for a
destroy objective". I went to the code for a line number to cite and found the opposite:
`DestroyKitPairing.RequiredPickaxe` upgrades the tier to diamond for any map carrying a core, and
`TeamsGenerator.GenerateKits` calls it. This map's `map.xml` carries a **diamond pickaxe**, and Quillon
Barrow's — whose only goal is end stone — correctly carries an iron one. The core is breakable. The
document is stale, not the system.

**The tail race was six deep on the first build and needed two goes.** `sink` measures from the median
ground under the footprint, so `base_height 4` with `skirt 1` gave a trench with a floor at y9 against a
field top of y15 — a one-way drop nobody could climb out of. `base_height 3` with `skirt 2` gives y11 and
ramped ends. Found by probing `(−30, −20)`, not by looking at a picture: a plan view cannot see a hole.

**The iron cube landed on the works road.** The marker was authored on the `yard` piece at `[11, 4]`,
which resolves to `(0, −50)` — the yard/casting seam, four blocks off the road's centreline. It reads as a
works fixture and it was not aimed there.

**The map ships as `<gamemode>ctw</gamemode>`, objective "Capture the enemies' wools!"** on a board with a
core and a destroyable and no wool. `MetaGenerator` writes both from constants and from the wool count
alone, and nothing upstream can say otherwise.

## The renders

`02-topdown`, `03-heightmap` (the four terraces, the race, the cut and the two ridges), `04-traversability`
(2 components, 4 markers, 0 isolated), `05-section-core` (down `x = −25`: the stage, a furnace house, the
casting floor, the core floating six above it, and the race), `06-objectives`, `07-surface`.
