# The author's read on ten painted boards

Ten boards from the colouring probe, looked at in-game by the repository's author. Every claim below is
the author's; nothing here is derived. It is committed because nothing can re-derive it — the scorer counts
block pairs and cannot say whether a board reads as a place.

Boards are named by slug. Which arm each belonged to is in `PROBE-RUNS.md`; the author's ranking was taken
against the boards, not against the arms.

## The verdict per pair

| place | preferred | margin |
|---|---|---|
| a desert | `probe-desert-1` | way better |
| a snowfield | `probe-snowfield-1` | better by a margin |
| badlands | `probe-badlands-2` | better |
| a volcanic ashfield | `probe-ashfield-1` | better, smaller margin than the desert pair |
| plains | `probe-plains-1` | very narrow — each has something the other lacks; the podzol decided it |

Treatment took two of five, control three. The palette carrying texture data did not decide a single pair.

## What the author said, board by board

**`probe-desert-1`** — Large splotches of red sand on sand do not read as intentional. Paths of coarse dirt
and gravel on sand are too contrasting. Boulders of sandstone on sand disappear against the sandstone
structures; boulders of red sandstone and orange clay are a correct combination but stand out too much
against the sand. The tunnel floor of coarse dirt, gravel and sand is noisy, especially at that scale.
Sandstone cover against red sand near the wool room is too contrasting, and so is the sandstone of the
buildings against red sand.

**`probe-desert-2`** — A path of red sand on sand is too contrasting, and so is a sandstone path on red sand.
Broken whorled trees. Boulders of sandstone on sand disappear. Boulders and trees block player paths.
Boulders made of sandstone and red sandstone are pure noise and too much colour difference. The layering of
hardened clay, red sandstone, orange clay and sandstone is good — it reads as orange stone with sandstone
over it — but it is missing a course of actual sand for the surface.

**`probe-snowfield-1`** — Mixing snow and quartz for the ground is nice. Snow-capped boulders and the other
kind are good. The tunnel walls and stone layers are a great texture. It misses a course of dirt below the
surface, which is minor. **The structures are coloured the same way as the terrain and are not
differentiated.** Overall good.

**`probe-snowfield-2`** — Terrible execution. Broken whorled trees. Too much quartz in the terrain compared
to `probe-snowfield-1`. Path materials could work together but not against white. Boulder colours are
diabolical, using diorite and andesite. The stairs and monument platform mix snow, gravel, clay, stone
bricks, smooth stone slabs, cracked stone bricks and cobblestone — three colour families. The monument
pillars use a log checker, which makes no sense when some logs show their exposed face. The houses use a log
checker of the same wood as the house pillars, so nothing distinguishes the two; an oak checker in the walls
with spruce kept for the pillars would have looked good. The layering is good in theory — a white snowy mix,
a clean one-block clay course, then stone — but the tunnel ground reuses that same pattern, so the roof is
white-and-clay, the pillars are coal, and another course of white-and-clay sits under it: two white buns and
a grey stone patty.

**`probe-badlands-1`** — Boring; everything is orange. Stacked terrain wants some stone courses at the
bottom. The houses are the base example retextured and could be much better. The pillars near the
destroyable, in white and light grey stained clay, clash against an otherwise red map. The floor under the
destroyable, spawn and wool platforms is noisy — white clay, yellow clay, orange clay, sand, dirt — a mottle
rather than a texture. The worst theme of the five preferred boards' opposites.

**`probe-badlands-2`** — The platform floor is better: white clay, light grey clay and sand in that pattern
are nice, spoiled by a dirt path thrown against it. The colour stack is more coherent. The surface pattern
of hardened clay, red sand and orange clay is good, and the small addition of white and light grey clay near
the bedrock wall works. What breaks it is a rim of red clay clashing with an otherwise natural surface —
with no rim at all and that surface everywhere it would be good. Paths on red sand are fine; a third block
would have helped, and **granite bridges the two textures**. Boulders disappear again: red clay and hardened
clay are too opposing to randomise between. Broken whorled trees. The destroyable pillars in courses of red
sandstone and normal sandstone are bad. The houses are ugly — too many colours, no concept of a house.

**`probe-ashfield-1`** — Actually sexy.

**`probe-ashfield-2`** — An interesting colour palette. Obsidian should not be used in terrain like that —
at most one course above bedrock, never a course inside the map. Quite noisy, but the noise works because of
the theme and the colours.

**`probe-plains-1`** — The boulders are a little much, especially where some sit flat on top of cover
elements. The texture is okay and the path reads well; it is a bit dirty with the dirt and gravel but it
works. The tunnel walls including courses of mossy cobblestone are not good — that block has too much noise
to be nice in a layered form and belongs in small specks, as in the boulders. The bottom house courses
should have been plain cobblestone without the mossy variant. The bottom of the spawn and wool rooms is
unthemed.

**`probe-plains-2`** — The themes on the tunnel walls and the bottom of the world do not get their noise
pattern through: vertical strips of each material appear instead of a pattern, so the values are wrong.
Podzol and grass are combined again, which does not work, and the path is too noisy as a result. The bottom
of the spawn and wool rooms is unthemed.

## The rules the author stated

Each is the author's ruling, and none is derivable from the corpus or the code.

- **A boulder must not share a tone family with the ground it sits on**, or it disappears. When unsure, build
  rocks from stone, andesite and cobblestone — boring, but it works against sand, grass, dirt and red sand.
  A rock of a single clay also works, since no two clay colours are close.
- **Do not randomise between two opposing colours.** Red clay against hardened clay on one boulder is noise,
  not variation.
- **A third block can bridge two that fight.** Coarse dirt and light grey clay with granite added works where
  the two alone are too far apart.
- **Mossy cobblestone belongs in specks, never in courses.** Too much noise of its own to be laid in layers.
- **Podzol and grass do not combine.**
- **Obsidian is a floor material**, at most one course above bedrock, never a course inside the map.
- **A rim clashes with a surface that is already natural.** Where the ground reads well, the rim should be off.
- **A stacked terrain wants stone at the bottom**, whatever colour the courses above it are.
- **A platform floor of five materials is a mottle, not a texture.**
- **A checker in a wall must not use the wood the pillars use**, or the two stop reading as different things.
- **A path on sand needs a near neighbour, not a contrast.** Coarse dirt and gravel on sand is too far.

## What this says about the scorer

`mush` — two blocks of one tone family whose contrast is within a third — **predicts the author's preference
in two of five pairs, and flags by name the combinations the author praised**: `Snow Block + Quartz Block` on
the snowfield board called nice, and `Gray + Black Stained Clay` four times on the ashfield board called
sexy. Subtle variation inside one family is the goal rather than the fault, and `mush` is the wrong sign for
a terrain surface.

`clash` — near-identical colour, contrast differing by over 2.5× — predicts the preference in four of five,
every case where it distinguishes them at all.

The author's commonest complaint, *too contrasting*, has no reading at all: it is a large colour distance
between blocks of **different** families inside one pattern, which nothing measures. Scored as such at a
threshold of 60 in RGB, it predicts the preference in four of five, missing only the desert pair, where the
complaints were about splotch size and boulders rather than about contrast.
