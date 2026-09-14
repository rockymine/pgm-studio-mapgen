# Agent A — four boards in the warm, arid family

Four boards, one of each objective kind, authored by driving pgm-studio's HTTP API on a server shared
with two other agents. The run's constraint beyond the objective kinds was a **ground family**: red rock,
sandstone, ochre, dust, dry grass, terracotta, weathered timber — and hue and value varied *within* it
across the four, so that four warm boards are not one warm board four times.

## What I set out to build

The four identity sentences, written together before anything was authored.

**`opus5-redmarl` — CTW.** *A wool board cut into a red marl gully: each team's dyehouse stands on its
own bank above a dry red watercourse, and the wool has to be fetched out of the enemy's dyehouse and
carried back over the gully to a plinth at your own back.* Deepest and most saturated of the four —
red sandstone and red hardened clay, with pale smooth sandstone for everything built.

**`opus5-dustwath` — DTM.** *A bleached dust-flat split by the bed of a river that has gone: each team's
monument stands in the open on a low sand bench a short walk forward of its camp, and the wath that named
the place is now a gap that has to be built across.* The palest board — sand over sandstone, dry grass,
weathered spruce.

**`opus5-potsherd` — DTC.** *A terracotta brickfield on a baked clay terrace: each team's core stands in
the open at the head of its own kiln yard, with the clay pit cut below it and the drying-shed rows behind.*
Mid value, warm orange-brown — hardened clay and brick, sandstone for the built things.

**`opus5-ochrepans` — KotH.** *Three square pads cut into an ochre salt-works: a centre pan sunk in a walled
evaporation yard and two flank pans out on the raised pan banks — a built board where every sightline is
broken by a pan wall rather than by a hill.* Yellow-ochre at mid-high value, the most structural of the four.

Across the set: **redmarl** dark and saturated, **dustwath** pale and bleached, **potsherd** mid orange-brown,
**ochrepans** yellow-ochre. No grey stone is the ground on any of them.

## What was built

One world rebuilt and three boards authored, all four driven through the same studio on `:7894`
shared with two other agents. Every world was exported into a directory emptied first, because the
export writes into a region directory it never clears — which is how the first dustwath world was lost.

All four numbers below are off the **final** drive, after the author's pass.

| slug | mode | size | plan | dead | declines | 03-slopes |
|---|---|---|---|---|---|---|
| `opus5-dustwath` | DTM | 88 × 208 | 5 pieces, a void wath, 3 build zones | 18.7% | 0 | 12 072 walked · 307 scrambled · 158 barrier · 8 faces |
| `opus5-redmarl` | CTW | 104 × 176 | 7 pieces, offset halves | **0.0%** | 0 | 11 191 walked · 341 scrambled · 210 barrier · 16 faces |
| `opus5-potsherd` | DTC | 104 × 208 | 8 pieces, a cut pit | 9.4% | 2 | 19 377 walked · 472 scrambled · 123 barrier · 7 faces |
| `opus5-ochrepans` | KotH | 104 × 192 | 2 pieces, everything authored | 50.8%, and the number is a blind spot — below | 1 | 16 536 walked · 325 scrambled · 811 barrier · 10 faces |

Every board carries four themes: its ground, one or two grounds that meet it, and a **`sward`** of grass
over two dirt that seats the copied trees. Shares: dustwath 80.3 / 10.9 / 6.2 / 2.6 · redmarl
64.4 / 23.2 / 7.9 / 4.5 · potsherd 87.8 / 4.9 / 4.5 / 2.8 · ochrepans 73.9 / 13.8 / 8.9 / 3.4.

The ground, read back: `level` / `largestField` / relief range —
dustwath 0.446 / 0.145 / 10 · redmarl 0.464 / 0.121 / 17 · potsherd 0.615 / 0.231 / 11 ·
ochrepans 0.682 / 0.282 / 8. The order is the order the four were meant to run in: the gully board
has the most ground shape, the salt-works the least and carries its shape in walls instead.

## The one finding worth reading first: the relief is solved for half the board

**A `rot_180` board's relief is solved for the `z ≤ 0` half and rotated onto the rest. Anything whose
ring is centred on the centre line is therefore built on one side of it and not the other.**

Ochrepans' west pan bank was a single `area` mark at h 26 spanning z −19..19. Built, it is a bank from
z −19 to −1 and then a seven-block fall, and the control point standing on that seam answered
`ground 61° from level`. Splitting the ring into two, one each side of z 0, changed **nothing** — the
second ring lies in the half that is never solved. Four columns settle it:

```
h(-45,-5) = h(45,5) = 26        h(-45,5) = h(45,-5) = 19
```

a perfect rotation of the `z ≤ 0` half. **So: draw every mark, flight, wall and prop seat wholly in
`z ≤ 0`, both sides of x, and let the rotation build the rest.** A pair of flank platforms cannot be
centred on z 0; moved off it, one drawn platform and its own image are a diagonal pair — which is what
the three destroy boards here do without anyone having had to say so.

Nothing refuses the centred version. `preflight` opens the gate, `POST /sketch/relief/read` reports
`seams 0`, the plan evaluator scores 0, and no render shows it. **The only read that found it was a
transect down the bank.**

## Nine things the studio does that no document here said

Each of these was measured, and each changed a board.

**`fill-ratio` (`G8`) is asked of a capture board and of nothing else.** Band **[0.201, 0.542]**,
computed exactly as *union of piece cells over the bounding box, in cells* — verified on four variants
of one plan that reported 1.0, 0.906, 0.708 and 0.563 against hand arithmetic. Swapping the wools of
that same plan for a destroyable makes the term disappear entirely. A wool board in this corpus is
therefore about half void, and redmarl's first plan — a filled rectangle, the shape three destroy
boards here use without complaint — scored **1003** and had to be thrown away.

**`max-chain-length` (`LN2`) is a piece's longest side in blocks**, band [25, 110]. Scaling one plan's
`cell` from 3 to 6 moved it 96 → 192 with no other change. Ochrepans' first `works` piece was 152
blocks long in one run and had to be cut into two bands.

**A wool room must abut, not nest.** `WX6` refuses a `wool-room` piece wholly inside another piece:
no land seam and no abutting build zone to enter by.

**`ST10` caps the spawn *piece* at 30 × 20**, not the protection region it names. A 32 × 16 piece is
refused; the fix is the piece, and the knock-on is `WL2` — a 28-block spawn piece cannot hold the 27
blocks of spawn-to-wool separation `WL2` wants unless **each wool marker stands at the far side of its
own room**, which is what `heftfold` does and what the arithmetic forces.

**`WX8`'s iron-cube window is narrow and not symmetric.** On a 28-block piece with a 16-block room,
offsets 2, 3, 26 and 27 placed and 4, 23, 24, 25 did not. Probing eight offsets against
`POST /plan/evaluate` took ten seconds; reasoning about the shell's thickness did not work.

**A `line` relief mark takes `h` as a list, one per point.** `{"kind":"line","width":6,"points":[[0,-76],
[0,-68]],"h":[26,23]}` is the form `EL1`'s own fix-hint emits, and `opus5-threap-edge` uses a nine-value
list for a ridge crest. None of the four flat specs read first carries one, so every ramp on all three
new boards is a `level` polygon with `anchor_heights` instead — which works, and is more code.

**Control points live in the finish, not the plan** (`controlPoints` + `scoreLimit`), and nothing fans
them, so all three are stated. The consequence is measured: `GET /coverage` on ochrepans answers
`markers` = **two spawns and one crossing**, `journeys 3`, and **50.7% dead** — with the two largest
dead patches, 4 307 and 4 094 cells, sitting exactly on the two flank pads. The coverage walk does not
know a control point is a place, so a capture board's own scoring ground reads as ground nobody goes to.
That number is not this board's emptiness; it is the read's blind spot, and it must not be used as the
empty-board calibration on a capture board. **The author has confirmed this**, and agent B found the
same thing independently on the same run.

**The relief is solved for the stated half and rotated onto the rest, so nothing centred on the centre
line is built twice.** Ochrepans' west pan bank was one `area` mark at h 26 spanning z -19..19. Built,
it is a bank from z -19 to -1 and then a seven-block fall: `transect x=-45` read `DROP -7 at (-45, 0)`,
and the control point standing on that seam answered `ground 61° from level`. Splitting the ring into
two, one either side of z 0, changed **nothing** — the second ring is in the half that is never solved.
Four columns settle it: h(-45,-5) = h(45,5) = 26 and h(-45,5) = h(45,-5) = 19, a perfect rotation of the
z ≤ 0 half.

So the rule is: **draw every mark, flight and wall wholly in z ≤ 0, both sides of x, and let the rotation
build the rest.** A pair of flank platforms cannot be centred on z 0; moved off it, one drawn platform
and its image are a diagonal pair, which is what the three destroy boards here do without anyone having
to say so. Nothing refuses the centred version, no render shows it, `preflight` opens the gate and
`relief/read` reports `seams 0` — the only thing that found it was a transect down the bank.

**A dressing prop is mirrored like everything else.** Three of redmarl's boulders were declined
`DR-CLAIM ... claimed by the prop 'rock-2'` when they were spread across the gully neck: each was
sitting in the claim of another prop's own `rot_180` image. Props also want about eight blocks between
them, and a door's keep-clear approach reaches further out than the building does. `06-claims.txt` is
written on every drive and says all of this as a raster.

## What I got wrong

- **I assumed a wool board is judged like a destroy board.** It is not, and the two-minute probe that
  says so — swap the objective, re-evaluate — would have saved a whole plan.
- **I claimed most of redmarl's apron with two vat pads and then spent three builds moving trees out of
  ground I had already claimed.** `06-claims.txt` is written on every drive and I did not open it until
  the third. Two props will not stand within about eight blocks of each other, and a door's approach
  reaches further than the building does.
- **I placed potsherd's core two blocks back from the pit lip, which is on the terrace mark's own
  four-cell bevel.** `column` answered 30° from level. A piece's rectangle is not its ground.
- **I ran potsherd's spawn track through its own kiln** and would not have known from any picture; the
  transect read `BARRIER +15, DROP -15`.
- **I set a push's ring clear of a flight and its falloff over it.** The `swell` stood two blocks proud
  of the pit-step's head from fifteen blocks away.

## Questions about how these play — for the author, not for a read

1. On a wool board, is a four-block face along the whole frontline with exactly **two** authored ways
   down per team the right amount of wall in front of a carry, or does a carrier need more ways out
   than one defender can watch?
2. Redmarl's two teams come onto the gully neck at opposite corners, because under `rot_180` a team's
   own slip is on the flank opposite its enemy's. Does that diagonal read as fair, or does one side's
   carry end up shorter?
3. On a capture board, should a **sunk** centre pad (held from above) and two **raised** flank pads
   (held from below) be worth the same per second, or is the harder one worth more?
4. Ochrepans is deliberately the flattest board of the four and carries its whole shape in walls, a sunk
   yard and one-block pan benches. Is a board whose cover is *built* rather than terrain a legitimate
   kind here, or does the flat-and-empty fault apply to it regardless of where the cover came from?
5. Potsherd's clay pit is seven blocks below the core's terrace with four authored ways out. Is a pit in
   front of a core a killing ground the attacker wants, or a trap that makes the core undefendable from
   below?
6. A `cube-3` in ender stone is 27 blocks at hardness 3; the `pillar-3` in obsidian it replaced was 3
   blocks at hardness 50. The **count** went up nine-fold and the **total work** went down, and `DC3`
   is what forced the material once the count changed. Is the count what matters here — twenty-seven
   interruptible breaks a defender can arrive during — or should `cube-3` carry emerald block, which is
   the hardest of the four the gate still accepts at that size?

## The author's pass, and what each item changed

Eight items came back from the author. Seven were changes; every one of them is a read.

**The goal is a cube.** `dustwath`'s destroyable was `pillar-3` — three blocks of obsidian on a goal
standing forty blocks out of its own camp door, at `GO1 3.09`. It is `cube-3` now, twenty-seven. The
same re-drive had earlier "corrected" a stored `cube-3` back to `pillar-3` to match the plan: the plan
was what was wrong, and it is the plan that changed.

**`potsherd`'s goal is a core, and `CorePlacement` carries no `style` at all.** Its casing size is set
by `lava`, and `lava: 3` — the corpus default — already builds a **5 × 5 × 5** obsidian cube. Measured
rather than assumed: `render/section?axis=x&at=-60` shows the casing five wide and five tall with three
courses of lava inside it, and `column?at=-34,-60` reads obsidian y31, lava y32–34, obsidian y35. That
is 98 blocks of shell against `cube-3`'s 27, so the item was already satisfied and nothing changed. If
a bigger one is wanted, `lava: 4` is the dial.

**And the cube decided the material.** `cube-3` in obsidian came back as `DC3` — *"cube-3 is 27 blocks
and obsidian is worth at most 3 of them — built in ender stone"*. The world build substitutes; the plan
does not, so `materials: "obsidian"` would have written obsidian into `map.xml` while the blocks came
out ender stone, and a declared material matching nothing in its own region is a goal at zero health
(`OB3`). The goal is **ender stone**, which is what the gate names, out of the four the stamper builds
(obsidian · emerald block · gold block · ender stone). The count is the author's point and the material
follows from it.

**A path of dirt on sand.** `dustwath`'s three track strokes paved `dirt · coarse dirt · spruce planks`
across a bleached board — a dark band with nothing to say where it changes. They pave **sand, granite
and polished granite** now: the sand breaks the run up and the two granites are a lighter hue that sits
with it.

**Two of the copied trees are conifers.** `spar-1` and `spar-2` are **acacia log under birch leaves**
(`162:12` under `18:14`) at thirteen to fifteen blocks — a pine silhouette. `thorn-1/2/3` are acacia
under acacia (`162:12` under `161:12`) at eight or nine, and are right. The library names rows
(`tree-showcase-r13-1`) and not species, so **the leaf id is what has to be read before a body is
used**; the log alone is what I went on. Both spars are dropped from `dustwath` and from `ochrepans`,
which carried the same two bodies and which the feedback did not name — the check was worth running
across all four. For the record, the other copied bodies here are: `redmarl`'s `scrub-1` and
`potsherd`'s `roundel-1` are oak (`17:12`/`18:12`, 7 tall), and `potsherd`'s `birk-1/2/3` are genuine
birch (`17:14` under `18:14`, 11–13 tall).

**Grass, and a seat for every tree.** A copied tree body wants soil under it, and eleven of them stood
on hardened or stained clay. All four boards now carry a **`sward`** theme — grass over two dirt over
the local rock — laid as small seven-point patches with the radius wobbled per point, one under each
tree the author named and a few more on open ground. The patch's own cell carries the ground's top
block beside the grass (sand on dustwath, red sand on redmarl, coarse dirt on potsherd, sand on
ochrepans), so it feathers out rather than ending on a line, and each board's biome — Savanna, Mesa,
Desert, Savanna Plateau — puts the grass a long way off green. Every patch is drawn in `z ≤ 0` so that
its own image seats the mirrored tree; `redmarl`'s one tree at z +16 moved to (−10, −14) for that
reason.

**A build zone whose edge is a ruled line.** `dustwath`'s `build.areas` was one rectangle at z ±24
spanning all 87 columns, with `<apply block-place=… region="not-build-area">` outside it and land
running past it on both sides. It is three rectangles now, stepping at x ±16 — the two bays' own inner
edges — and reaching eight blocks further inland over the middle, where the hollow and the causeway
flight are. A plan's `zones` are what compile to `build.areas`, one area per zone plus its image, which
is how `opus5-flintwick` gets three out of two. The terrain was not touched.
