# Sonnet Holdfast — the canonical brief

The fixed brief every agent built: *"A destroy board, one connected island, the monument in the open
with a forest closing the west flank, a hill east that attackers can bridge from, a village behind, a
void channel twenty blocks in front."* DTM, `rot_180`, authored entirely through the plan → sketch →
intent pipeline described in `docs/tools/`.

## The board

268×360 (one authored half plus its `rot_180` image), base surface 9, build ceiling 20, 8 players a
team. One island, one continuous landmass both teams stand on — no build-zone joint, because the
ground itself never separates except at the two void channels.

Order from each team's spawn toward the map's centre: **spawn** (a small raised platform, surface 11)
→ **village** (six houses on a street, between spawn and the goal) → **monument** (open ground,
`ender stone` `cube-3`, float 4) → **void channel** (20 blocks, cut with a `subtract`) → open field →
the mirror image of all of the above. West of that spine is **forest** (30 template trees, dense near
the monument, thinning toward spawn); east is a **hill** (a relief `push` to y17–19, three blocks under
the y20 build cap, sparse boulders and a few conifers).

| Piece | How |
|---|---|
| Field, forest, hill | three `add` polygons tiling one plan-compiled rectangle, each carrying its own `theme` |
| Void channel | one `subtract` rectangle, x −60..60 blocks, z −55..−35 (20 deep) — reaches from the forest's inner edge to the hill's, so **both** flanks are the only ways around it |
| Hill | one relief `push`, ring x 62..128 by z −140..−10, amount 7, crown 2 — solves to y17 low / y19 high, one block of headroom left under the cap for a bridge |
| Monument clearing, village pad | two relief `area` marks holding y9 flat, so neither reads the hill's slope |
| Bridging | one plan `zone` (build area) over the **eastern** third of the channel only, x 40..100 — the west two-thirds of the channel stays permanent void |

The bridging zone is a deliberate reading of the brief: "a hill east that attackers can bridge from"
is a claim about *where* a bridge is legitimate, not that the whole channel is crossable. Only the
strip under the hill's shadow is a build area; the forest side is never buildable, so the two "around"
routes the void creates are asymmetric on purpose — one is a bridge from height, the other is a walk
through cover.

## Techniques used

**A goal with no plan piece under it.** The destroyable is `{"piece": "", "at": [0, -13]}` in the plan
— an absolute cell offset resolved against the symmetry centre rather than against a piece. It rides
whatever the sketch's own shapes leave under it, so the monument's ground was authored once (as
`ground-mid`) rather than twice (`docs/tools/plan.md`'s `B128`).

**A relief `push` for the hill, `area` marks for what must stay flat.** The push is a drawn ring with a
falloff, so the mound's footprint is the ring's own shape rather than a circle; the two area marks pin
the monument clearing and the village pad to y9 so neither the push's gradient nor the grain wobble
reaches them.

**A build zone over one third of a void, not the whole of it.** `docs/gameplay/approaches.md`: "whether
a hole can be crossed is a separate decision from cutting it, and it is made in the intent." Cutting the
channel and deciding where it may be bridged were two separate authoring steps here, on purpose.

**A destroyable material chosen for the kit it will actually be broken with.** See the open question
below — `ender stone` rather than the obsidian default.

## What went wrong, in order, and what I learned from each

**Dressing silently disappears from every export unless a prop's `kind` is its JSON's first key.**
`GET /map/{slug}/export` (and `/xml`) throws `PgmStudio.Minecraft.Dressing.PlacedProp must specify a
type discriminator` and 500s the whole call whenever the very first property of a prop object is
anything other than `"kind"` — even though `PUT`/`GET /map/{slug}/sketch` and `POST
/map/{slug}/sketch/paint` accept and round-trip the object in **any** field order, including the order
`docs/tools/sketch.md`'s own worked example uses (`{"id": "d1", "kind": "path", …}`, id first). See the
report for the full bisection; every one of my first attempts followed the documented example's field
order and every one 500'd at export with no prop stamped. Putting `kind` first fixed it completely, on
every prop kind tried.

**Every enum-valued field a prop or a `HouseStyle` carries has to be written in its literal C# member
name (`Template`, `Worn`, `StairLattice`, `Arched`, `NegX`, `Air`…), not the camelCase
`docs/tools/sketch.md` and `docs/world-export/decoration.md` show (`"template"`, `"worn"`, `"negZ"`).**
`DressingJson.Options` declares a `JsonStringEnumConverter(JsonNamingPolicy.CamelCase)`, which is what
the docs' examples are written against, but the *deserializer* used at export time does not accept the
camel-cased form — and a JSON exception anywhere inside a prop is caught and the **entire** `props`
list silently becomes empty rather than reporting which prop or field was wrong. My first full-village
build exported at 200 with 53 props stored and stamped **nothing**: no houses, no trees, no boulders,
ground everywhere exactly as the bare terrain left it. I found it only by column-probing a location I
knew should carry a tree. See the report for the full account and every enum name confirmed against the
C# source.

**A spawn-role piece's terrain paint never shows.** The spawn platform column-probes as raw, unpainted
stone (`y1..y9` id 1) under a `holdfast-spawn` theme correctly assigned to shape `s1`, with a stray
detached `Bedrock` block floating at y18 above it. This matches `FINDINGS.md`'s report of the identical
symptom on ClayClay Redux, so I am corroborating a still-open defect rather than filing a new one — see
the report for the coordinate.

**Once those two were understood, everything else landed on the first or second try**: the relief push,
the two area marks, the absolutely-placed destroyable, the eastern-only build zone, the per-shape
themes, and all six house placements and thirty-odd trees stamped correctly the moment the field order
and enum casing were both right.

## Open gameplay question, decided without an oracle

**`approaches.md` says nothing about what material a DTM goal should be built from when the map's own
kit is fixed.** `capabilities.md` records that `TeamsGenerator` always writes one "Standard" kit with an
iron pickaxe, with no branch for a destroy objective's material, so the obsidian default — the
corpus's own centre — is unbreakable with the kit this pipeline actually generates. I could not find an
endpoint or plan field that edits kit contents (Edit's own free-text box only *names* a kit, per
`docs/tools/flow.md`'s "what nothing owns"), so hand-editing the exported `map.xml`'s kit was the only
route to keeping obsidian, and that would have meant shipping a map whose deliverable world disagrees
with what the studio itself produced. I decided **not** to do that: I named the destroyable's material
`ender stone` instead, one of the four buildable words `capabilities.md` documents, minable by the
standard kit's iron pickaxe with no further edit. `GET /map/{slug}/export` did not refuse the map for an
unwinnable goal (`OB18`), which is the closest confirmation available that the choice is sound; whether
a pale destroyable reads as "wrong" for a map named Holdfast is a materials question, not a mechanical
one, and I recorded the trade rather than asserting a verdict on it.

## Coordinates, for checking in-game

| What | World position | Note |
|---|---|---|
| Red spawn | (0, 11, −165) | facing +Z (toward the field) |
| Red monument | (0, 9, −65) | `ender stone`, `cube-3`, float 4 — structure floats to ~y13 |
| Void channel (red side) | x −60..60, z −55..−35 | subtract, full column removed |
| Bridging zone over the channel | x 40..100, z −55..−35 | the only buildable third of the channel |
| Hill crest | ~x 95, z −75 | solves to y17–19 |
| Forest, densest belt | x −110..−60, z −90..−20 | thins toward spawn |
| Village street | x 0, z −140..−100 | six houses, grid-aligned either side |
| Spawn-role paint defect | (0, −170) | raw stone y1–9 under a themed, unpainted spawn piece |
| Blue spawn / monument / channel | point-mirror of the above through (0,0) | |
