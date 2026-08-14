# Quillon Saltworks — a capture board on a salt pan

**In one sentence:** a working saltworks in white — quartz-and-sandstone pans stepping down to the brine,
a black spoil bank raked across the flat, and the wool sheds standing at the two far corners of the works.

168 × 168 blocks, `rot_180`, four wools (two a team), base surface 10, build ceiling 26. Two landmasses,
joined only by the mid band's build region — the ordinary capture topology, and the opposite of Quillon
Barrow's one continuous island.

## The board, read as a capture map

`match-flow.md` §6.4 says the convention that actually matters is **interpose the spawn**: on 62 of 87
corpus maps whose two objectives stand more than 40 blocks apart, the defending spawn lies on the segment
between them, and the wool-to-wool rotation is dead as a result — 5% of attacking lives that reach a
captured room reach the other one. So the spawn is put on that segment exactly:

| | position | on the wool–wool line |
|---|---|---|
| west wool | `(−72.5, 14, −72.5)` | — |
| east wool | `(72.5, 14, −72.5)` | — |
| red spawn | `(0, 16, −70)` | **on it**, 2.5 blocks off |

The rotation between the two sheds therefore runs through the enemy respawn point, and an attacker who
takes one wool has no cheap route to the other.

**The funnel is ten blocks.** §4.2 measures the minimum cut from the mid band to the wool room at 2 cells
— 10 blocks — on 79% of objectives. Each lane is exactly two cells wide where it leaves the flat: the west
lane mouth is `x −65..−55` at `z = −55`, and it is the only way into the west shed.

**One approach is walled and one is not, on purpose.** The plan declares a single `walls` entry on the
`lane-w`/`hub` interface. The compiler put a two-thick bedrock barrier at `x −65..−55, z −56..−54` with
`topY 14` — three courses proud of the attack side (the flat, surface 12), one proud of the lane behind
it, with a cobweb course on top at y15. The east lane has none. That is `approaches.md`'s "the approaches
differ" applied to two objectives of the same kind: one wool is taken by building over a prepared line,
the other by crossing open pan under fire from the spoil bank.

**Two water lanes, used for the one thing they are for.** `approaches.md` is explicit that a lane can
never be what connects two teams' lands, because for 45 minutes there is no route across it. So the mid
band's build region is the connection (`x −40..40, z −15..15`, 1 572 bridged columns in the traversability
read), and the two lanes sit on the **flanks** — `x −75..−45` and `x 45..75`, `z −10..10`, over void only.
Three quarters of an hour in, the endgame gets two new crossings on the outside of a board whose whole
opening was fought down the middle.

## What the ground is made of

Six themes. The board is white and the eye is meant to find exactly two things on it: the black spoil bank
and the dark shed roofs.

| Theme | On | Says |
|---|---|---|
| `salt-brine` | the pan (surface 10) | white crust — a `cell` of white clay/quartz/smooth sandstone/grey clay over two sandstone, quartz rim |
| `salt-flat` | the worked flat (12) | sand and sandstone, **rim off**, a `wallRun` retaining face |
| `salt-works` | the lanes and shed ground (14) | built — a chiselled-quartz rim on **every** boundary, a `wallDiagonal` face |
| `salt-stage` | the loading stage (16) | the cleanest thing on the map: quartz over smooth sandstone |
| `salt-spoil` | the raised bank | the only dark ground — coarse dirt, gravel, andesite, brown clay |
| `salt-basin` | the two sunk pans | thicker, whiter crust where the brine stood longest |

## The techniques, and what each one bought

**A stepped board is authored in shapes, and only the base tier can carry relief.** The pan sits at the
relief's own base (10) and takes the whole solve; the flat, the works and the stage are all
`relief_scope: exclude`, which gives each a clean two-block face rather than a ramp. The readback confirms
it: the island reports **3 169 cells**, which is the pan alone — the excluded tiers are not in the field
at all. The consequence is worth stating plainly, because it decided the design: a tier that is excluded
cannot then carry any relief of its own, so every landform above the base tier has to be an **erected
shape** rather than a mark.

**So the spoil bank is a shape.** `height_mode: raise`, `base_height 4`, `skirt 2`, and
`anchor_heights [3,4,5,4,3,3,4,3]` so the crest falls along its length. It stands on the flat, wears its
own theme, and is the one piece of cover between the mid band and the lane mouths.

**And the two basins are shapes too.** `height_mode: sink`, two deep, `skirt 1`, cut into the pan at
`x −64..−32` and `x 32..64`. A player crossing the pan drops into one and is out of sight of the shed for
its length — the "from below" approach on a board that has no room for a real depression.

**A wool cage written for this map.** Quartz and dark-oak courses under a dark-oak gable with a ridge cap
and a slab eave, slab-banded windows, and a stained-glass-pane door — the door choice matters, because the
wool-room block filter whitelists exactly the door materials an attacker may break.

## How it is meant to play

From the spawn a defender walks the stage, drops to the flat, and is at either lane mouth in about forty
blocks — the two are equidistant, which is the point of interposing the spawn. An attacker crosses the mid
band on a bridge, lands on the pan, and has ninety blocks of white open ground with two sunk basins and a
spoil bank in it before reaching a lane. The bank is where both sides want to be.

Then the match goes up, as `match-flow.md` §4.4 says it does: the build cap is 26, sixteen above the pan,
and the mid band is the one place a bridge may cross nothing.

## What went wrong

**Nothing was dropped this time**, because the frontage lines were kept two blocks clear of every path
band from the start — the lesson Quillon Barrow paid for. All 18 buildings stamped (2 offices, 4 cages,
12 sheds counting orbit images).

**The pans are flatter than the heightmap suggests.** The relief readback reports the pan running y9–11 —
a two-block range over 3 169 cells, which is a texture rather than terrain. That is right for a salt pan
and it means the board's whole vertical interest is in the four authored tiers.

**The board still ships as `<gamemode>ctw</gamemode>`** — which for once is correct, and only by accident:
the label is hardcoded regardless of what the map carries.

## The renders

`02-topdown`, `03-heightmap` (the four tiers, the spoil crescent and the two sunk basins), `04-traversability`
(2 components, 0 isolated, 1 572 bridged columns), `05-buildings`, `06-section-x-60` (down the west lane,
through the bedrock wall), `07-objectives`, `08-surface`.
