# sonnet55-vindrift — run report

## What I set out to build

A capture-the-wool board with a snowy theme, on the deployed studio at pgmstudio.de, left open for the author to
pin notes to in the Sketch tool. The identity written before anything was posted: **two timber lodges on
opposite shoulders of one glacier, a crevasse in each hub, the wool kept in a hall at the cold end of a spur,
and the ice between the teams crossed to a holm of blue pillars.**

The plan was to take a composed capture arrangement, as the brief allows, and take it over: a cold biome, a
snow ground banded by angle, glacier faces, dark-timber buildings under red roofs, a relief that steps down from
each spawn, a coast cut point by point and a landmark in the middle.

## What I could not say

**Nothing was missing from the system.** Four things were out of reach from where I stood.

| Wanted | Tried | Verdict |
|---|---|---|
| a camera that frames a hall from outside its walls | `render/eye?look=x,z`, which placed the eye inside the hall's bedrock wall and inside a spruce trunk | **unreachable**: `from=x,z&yaw=&pitch=` stands the eye by hand and works; `look` frames from wherever it finds room |
| a place for an outcrop beside the spawn road | `loop.py --candidates` at fifteen cells over both flanks | **out of reach**: every cell was refused by `DR-ROAD`, `DR-KEEP`, `DR-SITE` or `DR-STEEP`, the corridor being twelve to sixteen blocks wide |
| to bend the outer coast without moving the build zones' edges | `bendShapes` on the island at `side: in` | **mistaken**: bend resamples every long edge, so it moved the frontline brink and a wool spur's end; `editShapes` per vertex does it |
| a different arrangement than Murkwick's | not looked for until the board was built | **my fault**, see below |

## What I got wrong

**I reused a solved arrangement.** I chose composed p20 seed 43 from the feed because it had a ring hub and a twin
frontline, and only read `sonnet55-murkwick`'s entry in `BOARDS-BUILT.md` afterwards. It is the same arrangement,
and `AUTHORING-BRIEF.md` §3 says that is how a run ends up shipping the previous board in different blocks. It looked
right because the feed showed cards and a card carries no name. The paint, outline, relief, buildings and middle are
this board's own; the plan is not.

**I expected trees to stand on snow.** Seven spruce were declined or complained of as `DR-ROOT` or `DR-CLAIM` until each had
a disc of podzol of its own, and until a tall spruce's crown claim, about five blocks, was allowed for in the spacing.

**I put dirt under the snow.** The first surface was snow over two courses of dirt, which is the meadow's section, and every
one-block riser on a drift showed a brown stripe. Snow over snow fixed it.

**I applied `bendShapes` to the whole outline.** `EZ2` named nine void columns beside a wool spur and four at each frontline
crossing.

## What worked first time

The whole loop on the deployed studio: a build, a read-back and an export in 13 seconds a pass, with the token added by the
proxy. `POST /plan/compile` named the compiled shape ids, `editShapes` took eighteen inserted vertices in one replay, and the
sculpt emitter's `spire` with `kind: "made"` and `seat: "ground"` settled the needle on a holm the relief had raised.
`loop.py --candidates` answered each tree and rock in two seconds without a build.

## Open gameplay questions

**Is a composed arrangement shared with another board acceptable on the same site?** Decided: shipped it, said so, and offered to
change the plan. **Is cover on the holm wanted?** The needle and berms cut the long sightline between the lodges; I built them
and did not decide it. **Are two ways round the crevasse enough?** Unchanged from the composed plan.
