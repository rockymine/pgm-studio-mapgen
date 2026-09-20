# Destroy goals

**A destroyable is two authored words — a `style` and a `materials` — and neither is free text.** Both come
from closed sets the studio publishes at `GET /api/objectives/vocabulary`, and between them they decide what
a player sees from across the board and how long the raid takes. Neither is recoverable from a plan view, so
this card is one flat island with a goal at every station: the six styles along the north row, the four
materials along the south, and a core beside them for the one goal that has no material knob at all. Open it
in the studio as `technique-destroy-goals`, or run `build.py`.

Eleven objectives on one board is not a playable map. It is the vocabulary, laid out so the shapes can be
compared.

| Station | `style` | `materials` | What it built |
|---|---|---|---|
| `pillar-1` | `pillar-1` | obsidian | one block |
| `pillar-2` | `pillar-2` | obsidian | two, stacked |
| `pillar-3` | `pillar-3` | obsidian | three, stacked — the vocabulary's own default |
| `cube-3` | `cube-3` | obsidian | 3 × 3 × 3 round a 1 × 1 × 1 bedrock centre, **in ender stone** |
| `cube-4` | `cube-4` | obsidian | 4 × 4 × 4 round a 2 × 2 × 2 bedrock centre, **in ender stone** |
| `column-plus` | `column-plus` | obsidian | a plus section, five cells a layer, **in ender stone** |
| the material row | `cube-4` | each of the four | emerald and gold as authored; obsidian rebuilt |
| the core | — | *no such field* | an obsidian casing over three courses of lava |

## The two words, and where they come from

**`GET /api/objectives/vocabulary` is the whole authoring surface and it answers in one fetch.** Six style
slugs — `pillar-1`, `pillar-2`, `pillar-3`, `cube-3`, `cube-4`, `column-plus` — four material words —
`obsidian`, `emerald block`, `gold block`, `ender stone` — and the defaults a station takes when it states
neither. Nothing here needs a document; asking is cheaper than reading one.

**A style is a shape, and `footprints.txt` is the half a column cannot say.** A pillar is one column however
tall it is. `cube-3` and `cube-4` are solid squares. `column-plus` is the one that is neither — five cells a
layer with its corners left open — so it reads as a cross from above and as a block from the side.

**An even-sided cube has no centre column.** A `cube-4`'s anchor sits on one of its four middle cells rather
than in the middle of the square, so the cube grows unevenly about the point that was authored. Where a goal
has to be centred on something, that is an offset to author rather than a fact to assume.

## The size and the material have to agree, and the studio settles it

**Three of the six styles did not come out in the material they were authored in.** Every station in the
style row states `materials: "obsidian"`; `goals.txt` reads End Stone at `cube-3`, `cube-4` and
`column-plus`. The export answered **200 with `Pgm-Warnings: 4 DC3`** and built the board anyway.

**`DC3` is the rule and its reason is the match clock.** Obsidian is worth at most three blocks: a cube or a
plus-section column carrying it is a grind rather than a raid, because the defender repairs it about as fast
as the attacker mines it. The fix is the pairing — obsidian for a pillar, ender stone, gold or emerald for
anything larger.

**The map.xml declares what was laid, not what was asked for.** `xml.txt` shows the three rebuilt goals
carrying `materials="ender stone"`. That matters because `materials` is the filter PGM breaks the goal by: a
document naming a material that is nowhere in its own region is a goal at zero health, and the studio will
not ship one.

**A material outside the four is resolved rather than passed through.** `mismatch.txt` authors
`materials: "diamond block"` on a `pillar-3`: the export answers 200 with one `DC3`, builds three obsidian,
and writes `materials="obsidian"` into the document. Both ends move together, so the contract stays whole —
but the goal is not made of what was asked for, and only the warning header says so.

## What a core is, and what it is not

**A core has no material field anywhere in the pipeline.** Not on the placement, not on the intent, not in
the XML: `xml.txt`'s `<core>` element carries an owner, a region and a mode flag and nothing about blocks.
Asking a core for a different casing is not a gap to work around — it is not expressible.

**What it does state is its lava.** `goals.txt` reads the card's core as obsidian at y18, three courses of
lava above it, and obsidian at y22 — the casing, the lava the leak is measured from, and the lid. `lava`,
`lavaHeight`, `openTop`, `leak` and `digDepth` are its knobs; `techniques/objectives-and-clearances` is
where `leak` and `float` are worked against the ground.

## What every goal gets without asking

**A defence chest one course over the ground, under every goal.** It is the stamper's, not the author's, and
it is why a column read through a goal has a `Chest` in it that belongs to nothing in the intent.

**A wool beacon far over the board.** Left out of `goals.txt`'s rows on purpose — it stands around y44 here —
and it is how a player finds the goal from across the map.

**A modes ladder, where the map states none.** The export wrote `gold block` at 15m and `glass` at 20m and
marked every objective `mode-changes="true"`, which is what keeps `OB26` quiet: a destroy map with no ladder
is a map a determined defence can hold forever.

**And the kit.** The spawn's pickaxe is chosen from what the goals are made of, so choosing a material is not
also a decision about tools. Nothing here needs authoring.

## `float` is measured from the ground, and the ground is read

**Every station states `float` 4 over an island topping at y11, and every structure starts at y16.** A
`float` of N puts the goal's lowest course at the ground's top block plus N plus one. The float is measured
from whatever the relief leaves under the column, so it is a distance and not a height.

**An anchor is an absolute point and the studio seats nothing.** Every `anchor.y` in this card's intent is
the island's own top block, read once and written down. `OB22` refuses a float larger than a goal may have,
and `techniques/objectives-and-clearances` is where the two export-time gates are worked.

## The recipe

- **ask the vocabulary, do not guess a word.** `GET /api/objectives/vocabulary` is one fetch and it is the
  closed set; a word outside it is resolved to obsidian and only a warning header mentions it.
- **pair the material to the size.** Obsidian for a pillar; ender stone, gold or emerald for a cube or a
  column. Author it the other way and the studio rebuilds it and says `DC3`.
- **read the `Pgm-Warnings` header on every export.** A 200 is not "as authored" — it is "built, with these
  changed".
- **do not centre a `cube-4` by its anchor.** The anchor is a corner of the four middle cells; offset it.
- **a core takes no material.** Its knobs are `lava`, `lavaHeight`, `openTop`, `leak` and `digDepth`.
- **check the map.xml's `materials` against the blocks.** It is the filter the goal is broken by, and the
  one place a mismatch is silent in a world that otherwise looks right.

## Limits

**Where a goal may stand is not this card.** `float`, `leak`, the void, the spawn room and the wool room —
the two gates heard only at the export — are `techniques/objectives-and-clearances`.

**No wool and no capture point.** This board carries destroy goals only, so `OB25`'s monument placement and
the `ControlPoint` rules are elsewhere.

**Eleven objectives, two teams and no way to win.** The board exists to be looked at. Nothing about the
counts here is a model — one destroyable a team is the ordinary shape, and how many a board should carry is
`docs/gameplay/approaches.md`.

## What checks it

- `goals.txt` — a column through every station: the blocks, their heights, and the chest under each.
- `footprints.txt` — every block within three of each anchor, so the plan shape of each style is visible.
- `export.txt` — the export's status and warning header, with `DC3` quoted from `GET /api/rules`.
- `xml.txt` — the `<destroyables>` and `<cores>` the export wrote, which is what a server reads.
- `mismatch.txt` — a material outside the vocabulary, and what the world and the document each did with it.
- `destroy-goals.layout.json` · `destroy-goals.intent.json` — the flat island and the eleven objectives.

Renders, all off the **built** world rather than the sketch, because a goal only exists after the export:
`styles.png` and `materials.png`, the two rows cut in elevation; `core.png`, the casing and its lava;
`board.png`, the whole island from above.
