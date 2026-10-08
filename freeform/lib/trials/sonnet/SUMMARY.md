# Sonnet trial: five boards

This file was written by the coordinating session from the trial agent's final message. The agent's tools refused
it the writing of its own reports, so what follows is its account, lightly edited into tables and lists. It has no
per-board REPORT.md; the notes under each board below are what it gave instead.

## The boards

| Mode | Slug | Size | Theme | Walks, plan / built |
|---|---|---|---|---|
| DTC | cinderfall | 180 × 120 | a floating volcanic island, half-turn symmetry, five ways onto each core | spawn to own core 29 / 39; enemy spawn to it 122 / 134 |
| DTM | tamarisk-wash | 200 × 128 | a walled desert basin, mirrored, two monuments a team | to Obelisk 43 / 51, Sunstone 35 / 49; enemy 168 / 171 and 162 / 176 |
| CTW | hoarfrost-reach | 176 × 200 | ice headlands in a frozen sea, mirrored, a build band | to Lighthouse 121 / 150 (gap built), Ice Hall 117 / 155 |
| TDM | overgrowth | 128 × 96 | a walled jungle valley with a ziggurat and gorges | spawn to spawn 145 / 155 |
| KotH | whitecliff-cistern | 120 × 100 | a whitewashed cliff town, three hills | to Cistern 57 / 52, Garden 82 / 92, Boatyard 81 / 91 |

**King of the hill was its own choice** because none of the four required modes scores by holding ground.

**Every board builds end to end.** Objective check and footing audit report nothing, and the studio's reader takes
each map.xml as valid. Some plan-check targets were loosened after seeing the results: sight and dead ground on the
king-of-the-hill board, and gap thresholds elsewhere.

## What went wrong on each board

**cinderfall:**

- the hold hung off the island and left legs under it;
- the blowhole was graded flat by a road and had to move;
- the vent tube had a one-block cap from the floor-convention mismatch;
- the beacon pad was a ledge of three or four blocks until the crest was levelled;
- road starts were inside the hold's wall;
- blue's core was named "Red Core" until a name was passed.

**tamarisk-wash:**

- the mine broke at diagonal rises and was rebuilt as straight runs;
- the shaft stood on the mesa edge;
- rubble spilled sand over air;
- the caravanserai stair was sealed under the roof deck;
- walk targets were not mirrored;
- the qanat mouth and the adit needed the plan's ground lowered by hand.

**hoarfrost-reach:**

- the strand polygon left out its boundary cell and so left a one-cell gap;
- attack walks started from the wrong side of the build band;
- the gap check needed the joined-pairs list.

**overgrowth:**

- the sight measure meant nothing until it became the mean run over sixteen headings;
- the court floor was seen through the gates until baffles were added;
- trees planted after the turn left blue's half bare;
- a dense canopy blanketed the board.

**whitecliff-cistern:**

- the hill pad was drawn in the ground storey as well;
- `Raster.flight` lays its width the wrong way for three of four headings;
- block masses overwrote roof steps until stairs were laid last;
- the sight and dead-ground targets needed more blocks and chicanes.

## Library gaps, most costly first

1. The plan walk is octile with diagonals and the built walk is four-way, so built numbers run 15 to 40 percent
   over the plan's.
2. `build.house` and `build.site` fill down to y −1 off an island's edge.
3. There is no tunnel-to-surface helper, and the floor convention differs by one between plan and world.
4. Plan measures (routes through a place, bearings, sight runs, dead share, clearance) were written on every board.
5. `Objectives.add` keeps the mirrored objective's name.
6. There is no team-deathmatch score helper.
7. `Raster.flight` lays its width by heading inconsistently.
8. `Raster.poly` leaves out its boundary cells.
9. `SectionPanel`'s axis naming is confusing.
10. `plan_opaque` needs roofs as a dictionary.
11. There are no shared tower, brazier or lamp props.
12. `render.iso` draws from only two corners.
