# Tallowfleet — two objectives a side, asking for opposite things

A board played for a monument and a wool at once, on a grey tidal tallow works. The monument
stands out on the open quay a short walk forward of the spawn; the wool lies in a cellar at
the end of a walled spur behind the terrace.

**The sentence it was authored to:** *a tallow works on an estuary where the beacon is broken
where it stands and the wool has to be carried home, so a defence that holds the quay is not
a defence that holds the cellar.*

## Why the two objectives sit where they do

`docs/gameplay/approaches.md` settles it: **a core or a monument is the forward objective and
a wool is the deep one**, because a wool has to be fetched and brought back. Drafted the other
way round the wool sits at the front and `WL10` reads a wool-front-distance of 8.

So the beacon is fifty blocks from its own spawn and a hundred and seventy-seven from the
enemy's — `GO1` **3.54**, inside the 3–4 band — out on the middle finger with nothing in front
of it. The wool is two hundred and twelve blocks from the attacker and sixty-six from the
defender, behind a wall, in the board's own corner with void on two sides.

**They are not on the same journey, and that is the whole board.** The beacon is reached by
walking forward off the terrace and down a flight onto the quay; the cellar is reached by
turning inland along the back lane or by forcing the walled spur. A team standing on the quay
has its back to the wool.

## Where the beacon stands, and why it straddles the axis

The quay is three fingers with the fleet's two creeks between them, and the beacon stands on
the **centre** one, which crosses the symmetry line.

**On a flanking finger the two beacons sit diagonally opposite each other and `GO3` reads the
walk between them at 201, against a band topping out at 150.** Under `rot_180` the image of a
point off the axis is as far off it the other way, so a pair authored out on a flank is
separated by the board's whole diagonal. A finger that straddles the axis puts each beacon
opposite its own image down the middle.

## The board is ninety wide, and that is a `G8` answer

`FR9` holds a crossing to fifteen blocks of frontline, and the two flanking fingers presented
ten. Widening them took the fill ratio to **0.571** against a band topping out at **0.542**.

**Every way of paying for that out of the pieces cost a journey.** Shortening the fingers by
one cell widened the strait to fifty and `CT12` refused it — a CTW strait is 15–40. Narrowing
the terrace choked the spawn's own way out to five blocks. The ratio is land over the board's
**own box**, so moving the cellar five blocks further into its corner took the box to ninety
and the ratio to **0.517** with no ground given up anywhere.

## What the ground is made of

Three themes and all three paint: `strand` the estuary (49.4%), `works` the laid stone of the
terrace and the spur (45.3%), `flats` the wet silt where the tide runs out over the quay
(5.3%).

**The bands cut at 20° and 32°, read off this board's own `incline`.** 68.3% of the ground
stands under 10°, 85.3% under 20° and **0.9% at 40° or steeper**. Written first at 28°/50° —
Kilnbrow's numbers, on a board that is nothing like Kilnbrow — the face band was cut above the
whole population and painted nothing at all, and the shoulder carried the entire estuary.

**This is the run's one grey board.** A cool grey-green **Extreme hills** tint over gravel and
andesite, with the built family warm spruce over stone brick — the reverse of the other three,
which is what keeps a building legible against a cold ground.

## The erratics are clay, not stone

**A boulder is stone — except where the ground already is.** `DR-TONE` named all three: cut
from stone, cobble and andesite on a strand cut from gravel, cobble and andesite, every tone
family the rock was made of was one the ground already had, so it read as a patch of the
estuary standing up rather than as a rock.

The rule's own fix is to take the rock the other way on grey ground rather than to deepen the
grey, so they are dark clay over one cobble accent. An erratic is a mass carried here and
left, and on this board that is what it has to look like.

## The boiling house is layers, because nothing can stand on the spur

`POST …/sketch/seats?kind=house&width=&depth=` answers **34 legal cells for a 10 × 8 footprint
over this whole board and not one of them is on the spur** — the cellar's room, the defence
wall and the east finger's own edge take it between them. An 8 × 6 has two, both on the
terrace, and the second try-works stands on one of them.

So the thing an attacker up the spur has to go round is built out of **made layers**, where
the dressing pass has no say: three walls and a roof in the spur's north-east corner, open to
the south, `kind: "made"` with a `part_of` so `SK10`'s pair walk and `SK11`'s reachability walk
stay off it. `GET …/column` at (24, −92) and at its image (−25, 91) both read the same masonry
to y 19 under the same slab at y 20, which is the only read that says a made layer mirrored.

**Its masonry is a material and not a theme.** A wall two blocks thick has no column with
ground on all eight sides, so the surface bucket paints none of them and the rim and the wall
buckets carry the whole shape — `SK23`, which is right: a theme is a place and a shed's wall is
a thing that was built.

## The numbers

| Read | Answer |
|---|---|
| `03-slopes.txt` | 10 366 walked · 184 scrambled · 150 barrier; 12 faces, largest 21 at x 0…9, z −77…−75 |
| `06-claims.txt` | **26 placed, 0 declined** |
| `GET …/coverage` | reached 10 699 · dead 1 of 10 700 = **0.0% dead** |
| `POST …/sketch/relief/read` | 2 750 cells, relief 9, symmetry error 0, no silent marks, no seams |
| `GET …/plan/flow` | beacon: own 50 · enemy 177 · ratio **3.54** · wool: attacker 212 · defender 66 |
| `GET …/preflight` | **export gate OPEN**, per team |

## Both rooms are buildings

`roomStyles` states both, because a finish that states none stamps the studio's built-in
bedrock box — at 200, with no finding — and those are the two structures a player sees from
the inside. Both wear the works' own family under a **gambrel**, which breaks on the way up
and so rises further than a gable over the same span: a warehouse roof, which is what a tallow
works has. Neither is flat with a hole in it, which is the bedrock box's own shape.

## What went wrong

**`PL9` was blamed on the defence wall and the wall was innocent.** The first quay was two
slabs of land either side of the middle, and removing the wall left `PL9` exactly where it
was: the cause was a piece that was an island on both sides of the symmetry. Three fingers is
what answered it, and the test that found it was removing the thing I suspected and re-driving.

**The works terrace did not hold the height it was drawn at.** A solved shape's own
`base_height` decides nothing about where its ground ends up — the relief replaces the top of
every column it solves — so the terrace settled to the quay's level and the board built with
**0 faces**. `relief_scope: "exclude"` on `cellar-15` is what gave it its five-course face and
the flights something to state.

**The boiling house and the east flight stood through each other.** Both were drawn to the
spur without either being read against the other, and a transect at x 25 read `BARRIER +6 at
(25, −93)` and `DROP −7 at (25, −81)` and never reached the flight at all. Nothing else would
have found it: the plan tier cannot see an authored flight, and both structures stored at 200.

**A placement names where a recipe is seated, and a copied tree's foot is several cells
across.** `salt-4` was asked for at (−19, −77), a legal seat with two cells of margin on the
mask, and came to rest on (−16, −76) — `DR-ROAD`. The answer is to pick a cell deep inside a
seat block rather than one that merely is one.

## Two standing complaints, accepted

`EL1` names the three works↔quay seams as five-block steps, which is right about the plan and
wrong about the board: the plan tier walks the pieces flat and cannot see a flight. All three
transects, over the full run from the terrace to the pan:

```
x −25 from z −95 to −66   rises 1, falls 5, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
x  −3 from z −95 to −66   rises 1, falls 5, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
x  24 from z −95 to −66   rises 1, falls 6, worst step 2: 0 barrier, 1 scramble, 0 drop | walked end to end
```

`SK27` reads the terrace and the quay as one component carrying two paints with a hard line at
the riser. That line is the retaining face, it is the thing the board is composed around, and
it carries its own `wallRun`.

## Coordinates

| Thing | At |
|---|---|
| beacon (red) | (−4, −61), on the centre finger |
| wool (red) | (35, −105), in the cellar |
| spawn (red) | x −40…−20, z −115…−95, door +z |
| works terrace | x −35…15, z −95…−75, surface 15, `exclude`d |
| spur, and the defence wall | x 15…40, z −95…−75; the wall on `spur` ↔ `works` |
| back lane | x 10…25, z −115…−95 |
| quay fingers | x −35…−20, −10…10, 20…35, all z −75…−20 |
| flights | x −28…−22, −7…1, 20…28, all z −83…−67 |
| boiling house | walls x 29…39, z −93…−84, y 15…19; roof x 28…40, z −94…−83, y 20 |
| the fleet | (−32, −91) → (−8, −90), radius 3, depth 3 |
| shingle bank crest | ≈ (−1, −42) |
| build zones over void | three, one a finger, z −20…20 |
