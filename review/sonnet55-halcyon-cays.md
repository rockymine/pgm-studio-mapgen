# Halcyon Cays — a tropical atoll resort, joined by terrain

> A destroy board, one monument a team, mirror symmetry, with the middle joined by sandbars instead of a build
> zone over void, and a made resort set into wild cays.

**In one sentence:** a holiday resort on a string of cays in a lagoon, where a white hotel round a pool courtyard
faces a thatched bar on the sandbar between the two teams, and three different crossings run past rock stacks.

100 × 210 blocks, `mirror_z` (the image of block `z` is `−z−1`), plan cell 5, build ceiling 30, y 0…30.
Jungle was the first biome considered and Swampland the one kept, for its water.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy, one monument a team | one `pillar-3` of obsidian a team, default names | `<cuboid id="red-monument-region" min="8,16,-53" max="9,19,-52"/>` |
| mirror symmetry | `mirror_z`, one `team` group | relief read symmetry error 0 |
| the middle joined by terrain | three crossings, no zone in the plan | traversability OPEN; spit y11, ford top y9, islets y11 |
| goal arithmetic | monument 45 from its spawn, 151 from the enemy's | `GO1` 3.36 on the walk read |
| beaches, sandbars, small islands | 14 area marks over a pinned floor | range y7…15, symmetry 0 |
| towering rock stacks | five stacks of 2–4 `level` plates | Needle top y29, the Sentinel y21 |
| tropical trees from the corpus | four `jungle-2`/`jungle-5` copies | one species, soil only |
| a resort with new buildings | a layered hotel, two bungalows, a pavilion, a pool, a terrace, a bar | two forked styles, 37 made layers (15 are the hotel) |
| made meets grown along authored edges | terrace face 2 blocks, a flight, the beach shelf | `exclude` plinth, `level` ramp |

## How it is meant to play

**The monument is the forward objective on open sand at the mouth of a lane.** A defender walks 45 blocks from the pavilion down a 20-wide neck between the terrace and the lawn. An attacker arrives by the spit from the south, wades the reef ford from the east, or hops the western islets, and the three meet at the Driftwood Bar.

**The four approaches differ.** Around is the spit and the ford, above is the Needle and the lawn hill, through is the hotel's open arcade and lobby, and below is not built. The ford is slow and exposed under the Needle, and the islet hop trades speed for cover and a swim.

## What the ground is made of

**One relief group pins the lagoon floor at 7 and lets every cay give way to it by a bevel.** The beach is y11, the lawn crown y13, the ford y9, and the terrace is excluded made ground at y13. The water is a `basin` at level 10 over the whole lagoon, so islands stay dry and the sea reaches the rim.

**Three themes paint it.** `shore` is sand and sandstone with stone on slopes over 46°, `jungle` is grass over dirt on the lawns, and `karst` is the stacks. The resort's paving and decks state a `material` on each shape.

## Techniques used

- **made ground as an `exclude` plinth** for the terrace, a `level` flight with `anchor_heights` for its stair, and a `sink` shape with a `basin` for the pool.
- **erected stacks**, `height_mode: level` plates with a skirt on the foot and a sheer top.
- **layered made things**, one mass or one slab height to a layer, for the bar, the tower, the jetties and the furniture.
- **a hotel as one made thing**: 15 layers of one `part_of`, a `wallRun` facade, slabs shared by height, doors as sills and lintels.
- **forked house styles** for the bungalow and the pavilion, looked at in section before the world.
- **a basin over the whole sea**, `shore: 0`, so props are not claimed on the cays.

## What went wrong

**Pads drawn at their dry size came out a bevel too small, and a paint patch taller than the ground raised a tower.** Both showed in the first heightmap and column reads. The remaining faults are in the report: `DR-ROOT` on sand, `OB19` against the hotel and two standing `DR-PASS` complaints on the bungalows.

**The water is teal rather than turquoise and the vegetation is olive.** Swampland is the only biome that tints water; the cost is dull grass and leaves.
