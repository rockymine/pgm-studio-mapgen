# Riad — the plan

A King of the Flag board, planned and waiting on a review before anything is built. It is a walled water-garden
palace: a court with a deep cistern at its heart, a garden on either side of a long canal, and three posts
where the one flag can come back.

![plan sketch](renders/00-plan-sketch.png)

## What already exists, and what I took from it

**Desert Sanctuary is the reference, read from its region files and its XML.** It is 99 × 153 blocks, with
red and blue spawning at the two ends, 144 blocks apart, and three posts on the line across the middle. The
Mid Post is a banner on a beacon on a pillar standing in a fountain basin, and a player swims up the water
beside it. The East and West Posts are banners on raised platforms in alcoves at the board's sides
(`renders/ref-desert-sanctuary-topdown.png`, `-section-z24.png`).

**The gamemode is the shared `kotf` include in PublicMaps, and nearly every KotF map in it uses it.** One flag
is `shared`, and its holder scores at `points-rate="1"`, a point a second. The holder gets slowness, four hearts
and three seconds of absorption. A compass points every player at the carrier. First to 200 wins.

**A team that holds the flag does not respawn.** Each spawn carries `filter="has-flag"`, and with
`<respawn spectate="true">` a dead player waits until their team no longer holds the flag. So a carrying team
shrinks with every death while the other keeps coming back, which is what makes guarding the carrier the game.

**The posts are one `<post>` with several children, and the flag comes back at a random one.** The flag
returns `respawn-time` after it is dropped, 18 seconds in the include, at a child chosen in random order.
`sequential="true"` would make the order fixed. A child post can carry a `respawn-filter`, and Desert
Sanctuary uses one to switch its Mid Post off in its competitive variants.

**PGM needs a real banner at the flag's first post.** `Flag.java` looks for a banner block at the default post
and fails the match with "must have a banner at its default post" when there is none. The banner's colour and
pattern become the flag's, so the generator will place a standing banner at the Cistern as a tile entity.

**Other KotF maps keep the carrier out of places with `enter="deny-flag-carrier"`.** Maple Syrup keeps the
carrier off its dam, and Harb keeps the carrier out of the bases. Riad uses the same filter to keep the carrier
out of the back gardens and off the roofs.

## The board

| Level | Height | What it is |
|---|---|---|
| the Cistern | 12 to 19 | the pool round the middle post, seven deep |
| the ground | 20 | the court, the gardens, the balconies, the Minaret's garden and the back gardens |
| the parkour stones | 21 to 23 | three stones from each back garden up to the arcade roofs |
| the posts' tops | 24 and 25 | the Cistern's tower and the Mirador's porch, bridge and pad at 24; the Minaret at 25 |
| the arcade roofs | 24 | a walk five wide either side of the canal, over the walk under it |
| the spawn decks | 32 | a room on top of each spawn house, twelve over the ground |

**Red spawns in the north and blue in the south, and blue's half is red's mirrored, z → −z.** Nothing is
mirrored in x, so the east and the west posts can be different things and still be the same walk for both
teams. The board is 96 × 121, the spawn points 110 apart.

**The spawn is a room raised over a patio, and the way out is a drop.** A player spawns on a deck twelve over
the ground, walks four blocks to a 5 × 5 hole in its floor and falls into a pool three deep beneath it. Water
takes the fall, and nothing climbs back. The patio opens through a door on either side, and each door is behind
a screen wall, so no post and no garden sees into it. The enemy team may not enter it.

**The carrier stays in the middle.** A line across the board at z = ±32 is the edge of the carrier's ground;
the back gardens behind it are where the dead come back, and the carrier may not enter them, nor the roofs, nor
either patio. It leaves 4,372 of the board's ground cells to the carrier. Without it, a carrier walks to the
far end from the enemy's spawn and the match is the length of the board.

## The three posts

**Each post is a different fight, and each is the same walk for both teams.** The flag starts at the Cistern.
After each carrier's death it comes back 15 seconds later at one of the three, chosen at random.

| Post | Where | How it is reached | The fight it makes |
|---|---|---|---|
| **The Cistern** | the middle: a banner on a tower 3 × 3 standing in the pool, four over the court | by swimming up one of two water columns caged in glass against the tower's north and south faces. A player dives under the cage's lip, rises, and steps out on top | the mosh pit: everyone in the water, the climbers slow and boxed, a player on top hitting down at whoever surfaces. Leaving is a drop of five into the pool |
| **The Mirador** | the west: a banner on a 3 × 3 pad at the end of a bridge over the void, ten long and three wide | from a porch four over the ground. Red climbs to it by a stair from the north balcony, blue by one from the south, and the court's side is a drop only | the waiting room: both teams on the porch, then a run across ten blocks of bridge in the open, in bow range of both balconies below. The carrier has to come back across it slowed |
| **The Minaret** | the east: a banner on a pillar 3 × 3, five over a garden | by a ladder on any of its four faces | four ways up and one top: a climber cannot fight, so the top is held from the ground round it. Hedges in a broken ring give cover, and the void behind is a knock-off |

**No post can see a spawn.** The checker casts lines from a player standing at each post to blue's pool and
doors and finds none clear.

## The routes, and what each is for

**Every route has a job.** Lengths are blue's, walked on the plan by `scripts/plan_check.py`, in blocks with
water counted double and a climb counted at its cost; red's are the same mirrored.

| Route | Length | What it is for, and when it is used |
|---|---|---|
| **The canal:** out of the patio's door, round the screen, down either side of the canal to the court | 86 to the Cistern's top | the straight way to the middle post, and the way back to the fight after a respawn |
| **The west garden** to the balcony and blue's own stair onto the Mirador's porch | 94 to the Mirador's pad | the side approach, past the kiosk, which splits the garden into two ways |
| **The east garden** to the Minaret's garden | 92 to the Minaret's top | the side approach, past the fountain house |
| **The arcades:** a covered walk either side of the canal, columns every four | — | cover along the canal for whoever is carrying or guarding; partial, never a place to hide |
| **The roof walk:** three stones up from the back garden, then the arcade roof to the court | — | the guards' and attackers' high line over the canal and the court, level with the Cistern's tower. The carrier is kept off it |
| **The porch's drop** into the court | one way | the quick way off the Mirador for a team that lost the porch |

**Between the posts the Cistern is the hub.** From the Cistern the Minaret is 45 and the Mirador 61; from
either side post to the other is 91 through the court.

**The jumps are only the ones planned.** The checker looks for every gap of one to three blocks, in any
direction, that a player can cross landing no higher than a block up and that saves more than a few steps. It
finds the three-stone climb onto each arcade roof and nothing else.

## Cover

**Cover comes in two sizes, as the capture-board law asks.**

- **Large cover:** a kiosk 7 × 7 in each west garden and a fountain house 7 × 7 in each east garden split a
  garden into two ways round. The screen walls by the spawn doors are large cover too.
- **Small cover, two high:** four planters at the court's corners and cypresses on the Cistern's axes, one
  in front of each swim column. There are hedges in the gardens and by the canal, and a broken ring of hedges
  round the Minaret.
- **Partial cover:** the arcade's columns, every four blocks.

**Nothing on the board is a room a player can hide in.** The arcades are open on both sides, the kiosks and
fountain houses are solid, and the patios are out of bounds to the carrier.

## What `map.xml` will say

- **Teams:** red and blue; the flag purple. Each spawn uses `filter="has-flag"` and a three-second respawn,
  with `<respawn spectate="true">`.
- **One `<flag shared="true" points-rate="1">`** with the include's carrier kit and drop kit. Its one
  `<post respawn-time="15s" return-time="0s">` holds three children: the Cistern first, then the Mirador and
  the Minaret, each facing the way its approach comes in.
- **Score limit 200,** compass on the carrier.
- **Regions:**
  - the enemy may not enter a patio;
  - the carrier may not enter the back gardens, the roofs, the stones or the patios;
  - no block interaction.
- **The include's pieces are written out in full,** so the map runs on any PGM server, not only one with
  PublicMaps' includes.

## Theme

- **A palace water garden:** smooth sandstone ground in a tiled pattern, the walls of red sandstone and
  hardened clay, the arcades of quartz columns under a terracotta roof.
- **The water:** the canal and the Cistern in prismarine and sea lantern, the swim columns in light-blue
  glass.
- **The gardens:** hedges of leaves, cypresses of spruce leaves.
- **The team's colour:** stained clay on its spawn house, its screens and its half of the board's edge. The
  posts carry the flag's purple, in a banner over a beacon.

## Questions for the review

- **Should the middle post be switched off in a competitive variant?** Desert Sanctuary does that.
- **Is the bridge wide enough?** It is three wide, with nothing either side, over the void.
- **Is the carrier's line at z = ±32 too far forward or too far back?**
