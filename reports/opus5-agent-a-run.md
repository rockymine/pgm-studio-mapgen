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

| slug | mode | size | plan | dead | 03-slopes |
|---|---|---|---|---|---|
| `opus5-dustwath` | DTM | 88 × 208 | 5 pieces, a void wath | 18.7% | 12 246 walked · 100 scrambled · 146 barrier · 4 faces |
| `opus5-redmarl` | CTW | 104 × 176 | 7 pieces, offset halves | 0.0% | 11 236 walked · 258 scrambled · 202 barrier · 14 faces |
| `opus5-potsherd` | DTC | 104 × 208 | 8 pieces, a cut pit | 9.4% | 19 463 walked · 386 scrambled · 123 barrier · 7 faces |
| `opus5-ochrepans` | KotH | 104 × 192 | 2 pieces, everything authored | see below | 15 678 walked · 346 scrambled · 904 barrier · 4 faces |

The ground, read back: `level` / `largestField` / relief range —
dustwath 0.446 / 0.145 / 10 · redmarl 0.464 / 0.121 / 17 · potsherd 0.615 / 0.231 / 11 ·
ochrepans 0.719 / 0.316 / 8. The order is the order the four were meant to run in: the gully board
has the most ground shape, the salt-works the least and carries its shape in walls instead.

## Eight things the studio does that no document here said

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
That number is not this board's emptiness; it is the read's blind spot, and it should not be used as
the empty-board calibration on a KotH map.

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
