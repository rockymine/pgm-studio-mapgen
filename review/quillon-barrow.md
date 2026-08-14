# Quillon Barrow — the canonical brief, built

> A destroy board, one connected island, the monument in the open with a forest closing the west flank,
> a hill east that attackers can bridge from, a village behind, a void channel twenty blocks in front.

**In one sentence:** a chalk-and-heather headland where a barrow stands alone on open ground, screened
west by a wood, overlooked east by an andesite crag, backed by a village on a mossy stone-brick fold, and
fronted by a channel nobody can bridge.

148 × 228 blocks, `rot_180` about the origin, base surface 12, build ceiling 34. One landmass; the two
halves overlap across `z = ±5`, so the mid is a walked crossing rather than a bridged one.

## Where the brief's six things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy board | one `<destroyable>` a team, `ender stone`, `cube-3` | red at `(0, 16..18, −50)`, blue at `(0, 16..18, 50)` |
| one connected island | the `field` polygon crosses `z = +6`; its `rot_180` image reaches `z = −6` | traversability: 0 isolated objectives, one dominant component |
| monument in the open | an `area` relief mark pins `x −20..20, z −64..−36` flat at y12 | nearest tree `(−32, −24)`, nearest building `z = −71`, nearest boulder `(26, −32)` |
| forest closing the west flank | 21 template trees in two stands either side of a 4-block clear run | `x −70..−32`, `z −64..−16` |
| hill east to bridge from | the `crag`: a `raise` polygon, 11 above the ground, `skirt: 3` | crest y22–23 at `(45, −45)`; monument top y18; 30 blocks of bridge to the goal |
| village behind | 11 buildings on two frontage lines either side of a street | `z −82..−65`, street centreline `z ≈ −74` |
| void channel 20 in front | a `subtract` polygon | near lip `z = −30`, exactly 20 blocks in front of the goal; 22 blocks across at `x = 0`; 43 void columns on the `x = 0` section |

## What the ground is made of

Four themes, one per kind of ground, which is the whole of why the board does not read as one material.

| Theme | On | Says |
|---|---|---|
| `barrow-heath` | the field | grown: **rim off**, a `cell` of grass/podzol/coarse dirt over two dirt, a chalk-strata riser |
| `barrow-fold` | the village terrace | built: mossy-brick rim, a `wallRun` of stone brick coursing round the terrace face |
| `barrow-hold` | the back platform | built and dark: polished-andesite rim, a `wallDiagonal` face |
| `barrow-crag` | the crag and its ramp | landform: rim off, a banded andesite/gravel/granite face that reads as strata |

Turning the rim **off** on the two grown surfaces is the single most visible decision here. With it on,
every contour of the relief takes a lip and the heath terraces itself; with it off the heath runs to its
own edge and only the two built tiers wear a cap.

## The techniques, and what each one bought

**Author the layout wholesale, keep the plan for the intent.** The plan states four pieces, one spawn and
one goal; the compiled layout is thrown away and a hand-written `SketchLayout` is `PUT` verbatim. This
is not a workaround — `PUT /map/{slug}/sketch` is documented as a verbatim replace — and it removes the
whole "address a compiled tier by the height it stands at" problem the previous run had. Role-tagged
shapes are skipped by the rasterizer, so nothing of the plan's geometry needs carrying across.

**A goal with an empty `piece`.** The monument rides no plan piece: `{"piece": "", "at": [0, -10]}`
resolves to the absolute board position `(0, −50)` and takes its Y from the terrain the rasterizer built.
The landform under it is authored once, in the layout, as it should be.

**A landform that carries its own paint.** The crag is not a relief mark — it is a polygon with
`height_mode: raise`, `base_height: 11`, `anchor_heights` tilting the crest and `skirt: 3`. That matters
because paint scopes to a **shape**: a hill made of relief marks lives inside the field's footprint and
can only ever wear the field's theme. The crag is grey because it is a shape.

**Relief for the ground that is grown, shapes for the ground that is placed.** The relief carries a rim
mark, an area mark holding the goal's ground flat, three low swells and two pushes — a dished hollow west
(`amount −5`, `crown −2`) and a shelf (`amounts [5,4,3,3,4]`). The village and the back platform are
`relief_scope: hold`, so they stay flat while the heath rolls up to them.

## How it is meant to play

Two approaches, and they differ in kind rather than in flavour.

**West, through.** From the mid at `x ≈ −50` the ground drops into the hollow (floor y6, five below the
field) and runs north under the wood. A player in the hollow cannot be seen from the monument, and the
21 trees screen the last forty blocks. It is the early approach, and it costs nothing but time.

**East, above.** The crag's ramp climbs from `(46, −8)` to `(52, −34)`, `height_mode: level` with
`anchor_heights [12,12,23,23]` — a clean tilted plane. From the crest at y22 the monument is thirty blocks
west and six blocks down, so an attacker bridges in from above and does it in full view. It is the late
approach, and it costs blocks and visibility.

**Nothing goes straight up the middle.** The channel spans `x −34..34` in front of the goal and there is
no build region over it, so the two ways round it are the two approaches above. That is one decision I had
to make without an oracle: a channel with a build zone over it is crossable from the first minute, and one
without is permanent. I chose permanent, because the brief's channel is there to make players go around
and a bridgeable one does not.

The defence holds the fold: the village terrace stands two above the field with a coursed retaining face,
and the street runs the width of it, so a defender rotates along the terrace faster than an attacker
crosses the open ground under it.

## What went wrong

**Five houses vanished and nothing said so.** The first village had its frontage line at `z = −77` and the
street's band reaches `z = −77` where the centreline dips to `−75`. A path adds every band cell to the
decorator's `taken` set, and a building landing on a taken cell is dropped whole — both orbit images. The
build exported clean with six of eleven houses. Found by probing `(−22, −79)` and seeing terrace where a
longhouse should be. Fixed by moving the frontage to `z = −78`.

**The board carries no `not-build-area` unless a build zone is declared.** The first export had zero
declared build areas, so no `block=no-void` rule was written at all and the channel was bridgeable from
the first tick — the exact opposite of what "no build zone" reads as. A 90 × 10 build zone was added over
the mid causeway, which is all land and changes nothing about play, purely to switch the void rule on.

**The map ships as `<gamemode>ctw</gamemode>` with "Capture the enemies' wools!" as its objective**, on a
board with no wool anywhere. Nothing in the plan, the intent or the layout can say otherwise.

**The relief is gentler than intended.** The readback says 99.75% of the ground is walkable at a one-block
step, with four faces and no cliffs. The board's level changes are almost entirely in the shapes — the
crag, the two terraces, the hollow — and the heath between them is nearly flat. That is defensible for
ground an objective sits in the open on, and it is less terrain than I set out to make.

## The renders, in the order they were looked at

`01-plan` (the plan board — note it does **not** draw the absolutely-placed goal), `02-topdown`,
`03-section-x0` (the two channels and the causeway), `04-heightmap`, `05-traversability`,
`06-section-crag` (the crag's face and the hollow), `07-buildings` (the census that caught the missing
houses), `08-section-village`, `09-topdown-objectives`, `10-surface`.
