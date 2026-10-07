# Russetford — the composition, before the relief

The map is drawn as a place first, and this page is that drawing. Every zone has a reason for a player to
be in it, or is the frame the playing ground is seen against. The first build had none of this and came
out as a ramp with a few houses on it.

**The place.** A meandering autumn river, the Russet, winds through the bottom of a valley, and each team
holds one side. Its farm sits on a knoll under a wooded ridge, an orchard is terraced down the slope
toward the river, the monument stands on the village green, and the mill hamlet lies on the river flats.
A beech hanger climbs behind the village to a ruined tower. An old stone bridge carries the lane over
the river in the middle of the map, and the river is crossed anywhere else by swimming or bridging.

**The river is one body of water across the middle.** It meanders as an S through the origin, and that S
is point-symmetric by itself, so `rot_180` gives each team one outer bend and one inner bend. On its
outer bend a team's bank is a cut cliff; on its inner bend it is a gravel beach and water meadow. So
at the west bend an attacker lands on a beach and has to climb out under the defenders' orchard. At
the east bend the attacker drops off their own cliff and lands on the defenders' water meadow, right
below the village.

## The zones (red, the north bank; blue is the same turned about the origin)

```
 z    x -64 ............ -32 ............. 0 .............. 32 ............. 64
 -96  [ ridge wood ~~~~~~~~~~~~~~~~~~~~ ][ saddle pasture ][ the hanger ~~~~~~~ ]
 -84  [ wood ][ SPAWN tower+farm ]   [ walls, sheep ]   [ ~~ oak wood ~~ (T) ]
 -70  [ wheat | roots ][ hay yard ]       \  lane          [ ~~ wood edge ~~~~  ]
 -56  [ fields ]        \                 [ GREEN  (M) ]---[ village street --- ]
 -44  [ orchard terraces . . . . ]          |   chamber     [ cottages ][ well ]  ]
 -30  [ orchard . . . . . . . . ]           |  lane         [ miller ][ MILL ]~leat~
 -18  [ cut bank cliff  (cave) ~~~~~~~~ ]   |               [ holm: water meadow ]
   0  ~~~~~~~~~~~~~~ river ~~~~~~~~~~~~~ [ bridge ] ~~~~~~~~~ [ beach ] ~~~~~~~~~~~~
```

| Zone | Where (red) | What it is for |
|---|---|---|
| river | an S through the origin, 12 wide, water at y20 | the frontline. It is swum or bridged anywhere, and crossed dry only at the bridge |
| bridge | `x −3..3, z −12..12`, a humpback stone arch | the one made crossing, on the contested middle. It is a structure, not scenery |
| cut bank | `x −50..−8`, the river's outer bend | a cliff the attacker must climb or bridge up, with a cave mouth at water level |
| cave | from the cliff at `(−28, −20)` under the orchard to a chamber under the green's west lip | the approach from below: swum to from the far beach, and dug up from near the monument |
| orchard | `x −62..−30, z −52..−24`, a quincunx on the slope | the west approach from the cliff top to the farm and the green. Rows of fruit trees give cover in lines, not in a mass |
| farm | the spawn tower on a knoll at `(−32, −76)`, the farmhouse built onto it, the hay yard east | the spawn seated in a working place: land behind it, the ridge above, buildings beside |
| fields | `x −62..−42, z −68..−54`, wheat and roots, hedged | what the farm is for, beside the defenders' walk to the orchard |
| ridge wood | the back strip, `z −96..−84`, rising to y48 | the frame behind the spawn, wooded and rocky, with a woodcutter's clearing in it |
| green | a knoll at `(4, −56)` | the monument in the open, where the lanes meet and a defender can see it from the spawn |
| village | a street from the green east to `x 60` at `z ≈ −42` | cover all the way in, fought through house by house. Cottages, the miller's house, a well |
| mill and leat | the mill straddles a leat cut from the river, the wheel in the leat | the leat makes the water meadow an island (the holm) with two footbridges off it |
| holm | between the leat and the river, `x 14..62` | where the attacker lands from the east bend: open, wet ground under the village |
| the hanger | a hill `x 24..64, z −94..−58`, oak and beech on its slopes, a ruined tower on top | the forest beside the monument, with height an attacker can bridge from. The tower is something to find there |
| saddle | `x −4..24, z −94..−66` | a walled sheep pasture between the ridge wood and the hanger, crossed by the lane from the farm to the hanger |

## The ways a player goes

1. Spawn door, down past the hay yard, to the green (the defender's walk, about 45 blocks).
2. Green, down the hedged lane, over the bridge (the middle).
3. Green, along the village street, to the mill, over a footbridge onto the holm (the east bank).
4. Farm, past the fields, through the orchard, to the cliff top over the cave (the west bank).
5. Village, up through the hanger, to the tower (the height beside the monument).
6. Farm, across the saddle pasture, to the hanger (the back way round).
