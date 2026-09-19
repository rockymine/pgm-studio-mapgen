# Hushwater — a composed micro board adapted into a place

**The sentence, written before the first shape:** *a lead hush — two mine heads facing each other across
the gill their own water tore out of the fell, where the made ground at the top is flat and stated to be
flat and everything below it is raw ground at an angle.*

Capture the Wool, two teams, micro band — `G8` states that as **14–21 players a team**, so the
export writes `max="18"` on each — 120 × 216 blocks, 8864 ground cells, about 246 blocks² a player
against the band's measured 242. The arrangement came off
`GET /api/compose` at `players=18 teams=2 symmetry=rot_180 cell=4 seed=5` and was adapted; what the
composer contributed and what it did not is set out line by line in
`specs/opus5-hushwater/composed-vs-adapted.md`.

## How it plays

A team spawns at the mine head, on made stone at the back of its own half, and walks out onto the yard —
the ring of worked ground round the shaft, with the shaft itself a 16 × 16 hole players go round. From
the yard the ground falls away south down a fell bank to the wash, the scoured shore the gill runs
through. That fall is the board: six blocks over sixteen, cut on its west hand by the hush's own gully
and rising on its east into a knoll a defender can stand on.

The gill is forty blocks of void with a spoil bank standing in it, laid as a Z: one leg reaching toward
one team's shore, the other toward the enemy's. So the crossing is **two hops, not one, and the two are
different** — twelve blocks on one hand and twenty on the other, and `rot_180` gives each team the short
one on the opposite hand. A raid costs 30 placed blocks and about 210 of walking, measured both ways
within 1.4% of each other.

Each team defends two wools, one a side, and they are deliberately not the same kind of place:

- **West — the powder house.** An open spur of moor running out from the ring's west arm through a
  sixteen-block mouth, with the room at its far end, two of its four faces on void and a fell swelling
  between it and the hub so an attacker is seen coming. No wall. It is a long walk in the open.
- **East — the assay house.** A lane leaving the ring's east nose, with the board's one `walls` entry
  across its mouth: bedrock, two thick, sixteen long, five courses above the lane. There is no door in
  it, so it costs the defence too; the way in for a defender who has thought ahead is the **bing**, a pad
  of spoil cut off the team's own ground behind the head and bridged back over two team-owned build zones
  — the wall's far side reachable only from deep inside one team's half.

The nose is why the wall works. In the composed ring all four arms present a flush face at one x, and a
wall across a spur leaving a flush face is walked round with a two-block bridge. Pulling the east arm
twelve blocks proud of its neighbours makes the shortest bypass about fifteen blocks of open bridging,
beside a wall the defence is standing on.

## What the ground is made of

Three themes, each a place rather than a piece.

- **moor** (56.8%) — the fell. Finished on the **slope** axis, not by height: turf over soil to 12°,
  broken turf and coarse dirt to 26°, mottled stone above. `GET …/incline?format=text` reads
  `00-09° 62.6% · 10-19° 27.4% · 20-29° 6.7% · 30-39° 2.4%`, so those cuts put about two thirds of the
  fell in turf, a quarter in shoulder and six percent in rock.
- **floor** (24.5%) — the made ground: the mine head, the spawn apron, the walled lane and the assay
  house's yard. Laid cobble and stone brick over gravel, with a `wallRun` on the exposed face, which is
  the one surface on a board that wants stripes along its perimeter rather than a field sampled from
  above.
- **hush** (18.7%) — the scour: washed gravel over coarse dirt where the water ran, bare rock where it
  cut. It is the same ground at both ends of the fall — the scar on the bank, the shore the crossing
  lands on, and the spoil bank standing in the gill — which is what joins the two halves of the board's
  own idea.

Four brushes carry each theme across the other's riser so the paint boundary is not the height boundary.
The biome is **Extreme hills**, chosen before the patterns: it tints grass `#8ab689`, a grey-green that
agrees with the stone beside it where `Plains` at `#91bd59` reads as a lawn on a moor.

The buildings are timber — spruce boarding over a laid spruce log course, spruce posts and beams, brick
roofs — because the ground is grey stone and a stone building on stone is the hard thing to get right.
One style, three plots: the spawn hall, the store at the head's corner, the powder house on the spur.
Both wool cages are the same fork.

## The techniques, and what each one bought

| instrument | where | what it bought |
|---|---|---|
| per-piece `surface` | seven heights, 12 to 19 | ends the flat plan's merge into one polygon, which is the only way a composed board can carry more than one theme |
| `relief_scope: "exclude"` | the head, the spawn, the lane, the bing | states the made ground flat and takes it out of the solve; the fell is left to the relief |
| relief marks | 5 on the team group, 3 on the neutral | the wash pinned six under the yard, which is what puts the bank at an angle; a line mark with a `tread` for the hush gully; a knoll; a swell over the spur |
| a push | one, over the bank | the shoulder over the gill, added to the solved surface rather than negotiated with the marks |
| `height_mode: "level"` flights | two | one on the shore, where the transect measured two-block scrambles on the landing route; one up the bank |
| theme brushes | four, `height_mode: "raise"` | spill on the floor and the yard, scar at the shore, turf over the shore's east — each drawn to cross a riser |
| `polyline` shapes | two | the launder curving across the mine head, the tramway to the assay house door; four points splined, not a chain of chords |
| an intra-team build zone | the bing and its two planks | `CT4`'s team transient-link: every zone touching it touches one team's islands only |
| a `walls` entry | one | the prepared line into the east wool |
| a mid the composer did not emit | two neutral legs | two hops instead of one, and the two are different |
| a `pool` water prop | the dam on the mine head | the water the hush was let go from, on the one flat excluded ground where a prop that carves its own bed can be given a level |
| a `made` layer | the chimney on the bing | a 17-course tapered stack off `tools/sculpt/props.py` — five polygons, one layer, `kind: "made"` and `part_of` so `SK10` and `SK11` leave it alone, and `mirrors: true` on its group so both teams have one |

One instrument this board does **not** use, named rather than padded: there is no **copied tree**. The
birches and firs are vanilla templates, where a `copied` recipe carrying a body block for block would have
given the fell a rowan nobody has seen before. That is the board's largest remaining gap.

## What went wrong

**The first build was grey, and the cause was not the band cuts.** `05-themes.txt` read
`floor 50.5% · moor 35.6% · hush 13.8%`: I had excluded the whole hub ring from the relief and painted it
as made floor, so nearly two thirds of the board was *stated* to be grey stone. No slope band can make a
board green when that much of it is not green ground. Putting the ring's three lower arms back into the
solve and painting them moor took it to `moor 56.8% · floor 24.5% · hush 18.7%`. The lesson is the
brief's own: a mine head is a patch of laid stone in a fell, not a floor with a fell round it.

**Both flights were authored before the ground existed to measure them against.** The east one cut a
five-block trench across a knoll — `(18,32) 20 · (18,33) 15 DROP -5` on a transect — because the `knowe`
mark and the `brow` push had put that ground *above* the yard it was meant to climb to. Nothing refuses
this: `EL1` and `WL11` walk the plan flat and cannot see an authored flight at all. Moving it to the
shore, where the transect measured real two-block scrambles at `(8,21)` and `(8,31)`, took the board from
`132 barrier, 8 faces, largest 44` to `54 barrier, 6 faces, largest 16`.

**A brush drawn over the composer's yard hole drew nothing.** `SK13`: *"'spill-yard' draws nothing over
130 columns … 'void-1-cut' takes them away"*. A hole is never scenery.

**`jitter` is an integer percentage, not a fraction.** `DR-DOC` said so about a prop's pave; the same
mistake was sitting inside three themes, where `RQ3` does not reach.

**A three-block wool cube floats thirty courses above each wool room** and is not a fault: it is
`GoalMarkerStamper`, a sky sign stamped five blocks above the build cap so nobody can reach or grief it.
I read the source before writing it up, which is the third time in this repository's history that would
otherwise have become a filed bug against a feature.

## Open gameplay questions

Both were decided without an oracle and are recorded as questions rather than facts.

1. **Is a bedrock wall with no door fair to the team that owns the wool behind it?** It costs the defence
   three placed blocks to cross its own wall, against four to reach the unwalled wool on the other flank.
   I decided yes, and built the bing as the defence's way round, so the wall is a prepared line the
   defence can also plan for rather than a tax it pays every rotation.
2. **Should the two hops across the gill be equal?** I made them 12 and 20 on purpose, mirrored so each
   team gets the short one on the opposite hand. That makes one crossing cheap and contested and the
   other long and safer, and it makes the two halves of the middle read differently without making them
   unfair. A board with two equal hops would be simpler to read and less interesting to fight over; I do
   not know which the author would prefer.

## Coordinates

| thing | where |
|---|---|
| spawn (red) | `0, 18, 104`, door facing −z |
| wool `red` (west, open) | `-46, 17, 68`, monument `-6, 20, 102` |
| wool `orange` (east, walled) | `56, 17, 70`, monument `5, 20, 102` |
| approach wall | `x 35..37, z 60..76`, bedrock, top y21 |
| the yard hole | `x 0..16, z 60..76`, 16 blocks across at its narrowest |
| the shoal | `x -16..8, z 0..8` and `x -8..16, z -8..0`, crown y14 at the origin |
| the bing | `x 40..56, z 88..100`, planks `x 40..56, z 76..88` and `x 24..36, z 80..100` |
| the hush gully | a line mark `(-13,47) → (-11,36) → (-9,26)`, r 6, tread 2 |
| the shore flight | `x 3..11, z 20..34`, foot 11, head 17 |
| the bank flight | `x -6..2, z 33..48`, foot 14, head 18 |
| the knoll | point mark `(25, 37)`, r 9, h 18; rocks at `(24,30)`, `(28,42)` |
| the observer | `0, 33, 0` — lifted from the derived 27 so its bedrock plate clears the shoal's crown by 18 |
| the dam | a `pool` water prop, ring `(-15,79) (-9,78) (-8,86) (-13,90) (-16,85)`, level y17 over a bed at y15 |
| the launder | a polyline `(-6,84) → (2,80) → (11,86) → (22,81)`, flush in the head's floor |
| the store | `[[17,85],[23,91]]` on the mine head |
| the chimney | a `tapered_tower` at `(48, 94)`, floor y18, 17 courses, base radius 3.4 tapering to 2.2 |
| the powder house | `[[-31,60],[-25,64]]` on the west spur |

Everything is fanned by `rot_180`; the blue images are at `(-x-1, -z-1)`.
