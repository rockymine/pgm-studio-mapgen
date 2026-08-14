# Tallow Mirefast — the canonical brief, built

> A destroy board, one connected island, the monument in the open with a forest closing the west flank,
> a hill east that attackers can bridge from, a village behind, a void channel twenty blocks in front.

**In one sentence:** a frozen peat fen where a wardstone of obsidian stands alone on open moor, screened
west by a spruce wood, overlooked east by an ice-and-diorite scarp, backed by a timber steading on a cut
terrace, and fronted by a curved ditch whose two ends are deliberately unequal.

138 × 204 blocks, `rot_180` about the origin, base surface 11, build ceiling 32, y 7..43. One landmass —
the fen polygon crosses `z = +8`, so its own image reaches `z = −8` and the two halves overlap across a
sixteen-block mid.

## Where the brief's six things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy board | one `<destroyable>` a team, **obsidian**, `column-plus` | `<cuboid id="team-wardstone-region" min="-1,16,-51" max="2,19,-48"/>`; `<gamemode>dtm</gamemode>`, `<objective>Destroy the enemy's monuments!</objective>` |
| one connected island | the fen crosses the axis; nothing is bridged | traversability: 18 566 navigable columns, 4 components, **0 isolated** |
| monument in the open | an `area` relief mark pins `x −18..18, z −62..−40` flat at y12 | nearest tree `(−22, −46)`, 22 blocks out; nearest building `z = −80`, 30 out; nearest boulder `(−10, −34)`, 16 out |
| forest closing the west flank | 13 template spruce in a wood, 5 grown spruce in the neck copse, one ride between them | wood `x −60..−22, z −64..−38`; copse `x −62..−52, z −28..−12` |
| hill east to bridge from | the `scarp`: a `raise` polygon with a per-vertex tilt, `skirt: 3` | crest y21 at `(42, −60)`; the wardstone's ground y11 and its top y18, 42 blocks away — the bridge runs downhill |
| void channel 20 in front | a curved `subtract` | at `x = 0`: ground to `z = −32` (top y8), **void `z = −30..−12`**, ground again at `z = −11`. Near lip exactly 20 blocks in front of a goal at `z = −50`, and 19 columns across |

## The two ways round the ditch are not the same way twice

This is the one design decision the board is actually built on. The ditch's west end stops at `x = −48`
and the fen's coast is at about `x = −64` there, so the **west way round is a seventeen-block neck** —
measured: ground at `(−58, −14)` and `(−50, −14)`, void at `(−44, −14)` — and it is under the trees. The
east end stops at `x = 30`, leaving an apron thirty blocks wide, but the scarp's foot begins at `x = 24`,
so the **east way round is a climb**. A defender who watches one is not watching the other, and the two
cost different things: the west is cover and no height, the east is height and no cover.

The channel is **permanent**. The board declares no build area at all and states
`build.voidEnforcement = {exclusions: []}` instead, which wires
`<apply block-place="deny(void)" region="void-enforcement-area">` over an `<everywhere>` region. Nothing
may be placed over the ditch at any point in the match. Bridging happens over *land*, from the scarp.

## What the ground is made of

Five themes, one per kind of ground, and the pairing of paint to what a shape is *for* is the whole of
why the board does not read as one material.

| Theme | On | Says |
|---|---|---|
| `mire-peat` | the fen | grown: **rim off**, a `cell` of grass/podzol/coarse dirt/gravel/snow over coarse dirt over two dirt, a clay-and-stone riser |
| `mire-timber` | the steading terrace and the two ramps | built: cobble rim, a beaten `checker` yard, a `wallRun` of mossy cobble → cobble → stone brick round the terrace face |
| `mire-hold` | the spawn bank | built and dark: polished-andesite rim, a `wallDiagonal` of stone brick, cracked and mossy |
| `mire-crag` | the scarp and the two mid blisters | landform: **rim off**, a `cell` of diorite/packed ice/snow/andesite/gravel, and a `layered` riser that is ice over ice over diorite over stone over granite — strata down the face |
| `mire-cut` | the two peat cuttings | wet and dark: podzol rim, a `noise` ramp through coarse dirt/clay/podzol/gravel, clay fill |

Turning the rim **off** on the two grown surfaces is the single most visible decision. With it on, every
contour of the relief takes a lip and the moor terraces itself; with it off the moor runs to its own
edge and only the built tiers wear a cap.

## The techniques, and what each one bought

**Author the layout whole and keep the plan for the intent.** The plan states five pieces, one spawn and
one goal; the compiled layout is discarded and a hand-written `SketchLayout` is `PUT` verbatim
(documented behaviour — `PUT /map/{slug}/sketch` is a verbatim replace). Role-tagged shapes are skipped
by the rasterizer and the rooms are stamped from the *intent*, so nothing of the plan's geometry needs
carrying across and no compiled tier ever has to be addressed by the height it stands at.

**A goal with an empty `piece`.** `{"piece": "", "at": [0, -10]}` resolves to the absolute board position
`(0, −50)` and takes its Y from the terrain the rasterizer actually built. No plan tier was manufactured
to carry the marker; the ground under it is one `area` relief mark.

**Obsidian, on purpose.** The goal is obsidian and the kit that shipped with it carries a **diamond
pickaxe** (`map.xml` line 17), because `DestroyKitPairing` upgrades the tier for an obsidian goal. The
export gate did not refuse it. Run 1 chose end stone to dodge a refusal that no longer exists.

**Bézier outlines on four shapes.** The fen's coast carries seven control entries, the terrace's western
headland two, the ditch's lip and shore six, the scarp's south face two. The fen reads as a headland
rather than a twelve-sided plate, and the ditch reads as terrain rather than as a ruled slot.

**A tilt on three shapes, and each tilt does a job.** The scarp is a `raise` polygon whose
`anchor_heights` are `[12, 13, 12, 10, 7, 4, 4, 8]` — twelve at the north crest, four at the south foot
— so the side the attack arrives from is the side that can be walked up, and the side that overlooks the
goal is the side that is high. The two terrace ramps are `level` shapes with
`anchor_heights [14, 14, 11, 11]`, which is a staircase off the terrace stated in four numbers.

**Relief for the ground that is grown, shapes for the ground that is placed.** The island carries a rim
mark, an `area` mark holding the goal's ground flat, a `scarp` mark cutting the fen's southern lip down
to the mid, two `point` swells the wood stands on, a `line` spur off the scarp's foot, and two pushes —
a falling shelf under the wood (`amounts [4, 3, 1, 2]`) and a dished hollow in the mid. The steading and
the bank are `relief_scope: exclude`, so they keep their own column and meet the moor at a face.

**Nine buildings on two frontage lines.** Three styles that differ first in proportion — a long low
longhouse, a two-storey croft, a squat hipped store — squared to a common frontage either side of a
street at `z = −76`, with the gap in the middle where the ramp comes up. All nine stamp on both orbit
images: `--structures` reports **22 structures** (9 × 2 buildings, 2 spawn halls, 2 goal markers).

## What went wrong

**The grown trees were authored in degrees.** `branchAngle` on a grown tree is in **radians**, clamped to
`[0.2, 1.5]`; the first pass wrote `40` and `35`, which clamps to the maximum and produces a nearly
horizontal branch fan. The foliage read-back showed the neck copse as five crowns of about fourteen
blocks' radius fused into one blanket. `sketch.md` names the field and gives it no unit. Corrected to
`0.45–0.65` with `leafSize 0.24`; the copse is still a thicket, which is what a neck wants, but it is now
five trees rather than one mass.

**The crag's cell palette contained plain stone.** `solid(STONE)` was one of five entries, and the fill
is also stone, so about a fifth of the crest read as unpainted rock in a column probe at `(44, −58)`.
Replaced with andesite and gravel; the same column now reads gravel over stone at y20–21.

**The mid was sixteen blocks deep on the first build**, because the ditch's south edge sat at `z = −8`
and its image at `z = +8`. Widened to `z = −11`, which is 22 blocks of contested ground. Visible only in
the top-down, and only once the two halves were drawn together.

**Hay bale and packed ice read as "unnamed material" in `--surface`.** The steading's roofs and the
scarp's cap paint magenta in that render. It is a palette gap in the read-back, not in the map — the
column probes show the blocks are exactly what was asked for.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red wardstone | `(-1..2, 16..19, -51..-48)` | obsidian, `column-plus`, ground y11, floats 5 |
| red sky marker | `(0, 36..38, -50)` | red wool, above the build cap |
| bedrock plate under the goal | `(0, 10, -50)` | one course, buried under gravel |
| ditch, at `x = 0` | void `z = -30..-12` | 19 columns; ground y8 at `z = -32`, y7 at `z = -11` |
| west neck | `x -65..-48, z -14` | ground at `(-58,-14)` and `(-50,-14)`, void at `(-44,-14)` |
| scarp crest | `(42, -60)` | y21; gravel over stone |
| scarp south foot | `(46, -24)` | the climbable side, rise 4 |
| peat cutting A | `(-28, -38)` | top y9 against y11 around it |
| steading street | `z = -76`, `x -44..44` | worn gravel-and-cobble band, radius 2 |
| spawn hall | `(0, -90)` | timber over stone brick, gable, hay roof |
| observer | `(44, 42, -44)` | over the scarp, not the origin |
