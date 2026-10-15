# Studies

**A study is a sheet of forms, not a board.** Each folder here renders shapes built from pgmvox to see what a kind
of ground can look like before a board uses it: no spawns, no objectives, no map.xml. `check.py` does not build
them, because nothing in them is held to a hash.

**Each study keeps its scripts and the renders the author judged.** `scripts/` writes into `renders/`, one round per
folder where a study went round twice, and every script runs from its own folder:

    cd studies/volcanoes/scripts && python3 round2.py [name ...]

**A round is kept even when the next one replaced it.** The first round is what the author's notes in the table
below were written against, and the second cannot be read without it.

## What each holds

| Study | Scripts | What it draws | What the author kept, and what the next round changed |
|---|---|---|---|
| `volcanoes/` | `volcanoes.py` → `round1/`, `round2.py` → `round2/` | twelve volcano forms in round one, shaded three tones by slope; the eight kept forms rebuilt in round two | Kept the strato, the caldera lake, the horseshoe's rubble, the somma and the maar; the tuya kept as a jungle monolith with an uneven top. Dropped the cinder field, the neck, the shield and the floating island. Round two warps every outline, so no form is a circle or a ruled line, and makes the fissure layered and bent. |
| `volcanoes/explain/` | `gen.py`, `overlay.py`, `page.py` | `caldera-lake-layers.html`: the caldera lake taken apart layer by layer, with the shapes its recipe names drawn over it | `page.py` fills `template.html` with the two data files and rebuilds the page byte for byte. |
| `winter/` | `winter.py` → `renders/` | a glacier tongue breaking up into a canyon, pack ice, an ice shelf, cirques and a snowfield | The ice shelf and the tongue kept. Pack ice wants larger pieces and no circles; the snowfield wants rock poking through flowing snow and deep cracks in the ice. |
| `combinations/` | `combos.py` → `renders/` | a lava rift with mesas and tangled bridges, the same rift under broken ice, and a somma facing an ice cliff | The rifts and the somma's ice kept. The mesas should be less round, the canyon rim varied with no ledge running its whole length, and the ice cliff stepped over several levels. A lava caldera was dropped. |
| `water/` | `water.py` → `round1/`, `water2.py` → `round2/` | cascades, a plunge, a delta, meanders, travertine terraces, and lava lakes, rivers and falls | Round one dropped rivers too hard, left a fall unjoined and cut straight walls. Round two states the river's surface first, falls a block at a time with falls only where placed, and grades every form into the ground. |
| `dungeons/` | `dungeons.py` → `layouts/`, `deep.py` → `deep/` | six dungeon and bunker plans measured for play, then the same plans given height, finished walls and floors, and cut open | — |
| `bunker-cores/` | none | `bunker-cores.html`: ten ways a core and a wool can depend on each other in a bunker map without TNT, with PGM's leak rule | — |

## What came out of them

**What a study proved general went into the library.** `noise.warp`, `landform.gullies` and `landform.lumps` came
out of the volcanoes, `shapes.shatter` out of the winter ice, and `forms.sweep` and `forms.spike` out of the
bridges and spikes, which became `examples/bridges` and `examples/spikes`.

**What stayed here is still a study.** The river channel, the basin fill and the falling curtains in `water2.py`,
and the room plans in `dungeons.py`, are written for the sheet they draw and have not been asked for as library
code.
