# Grok Ridge — Theme & Dressing

## Palette (legacy block IDs)

| Role            | Block                         | ID:data   |
|-----------------|-------------------------------|-----------|
| Primary wall    | Andesite                      | 1:5       |
| Wall base/trim  | Stone brick                   | 98:0 / 98:1 / 98:3 |
| Posts / beams   | Spruce log                    | 17:1      |
| Roof            | Gray stained clay             | 159:7     |
| Floor (hall)    | Stone brick                   | 98:0      |
| Floor (cottage) | Spruce planks                 | 5:1       |
| Glass           | Glass pane                    | 102:0     |
| Path mix        | Stone brick + andesite + cobble | 98 / 1:5 / 4 |

Overall feel: cool gray ridge stone with dark spruce timber framing and a slate-like roof.

## House styles

### `ridge-hall` (spawn)
- **Form**: gable, pitch 1, ridge cap, overhang
- Larger footprint (extent 8)
- Full height courses: stonebrick base → andesite body → stonebrick cornice
- Arched windows + arched door head
- Intended as the main spawn structure sitting on the crest

### `ridge-cottage`
- **Form**: hip roof
- Smaller (extent 5)
- Same material language, simpler pane windows
- Used on the crest flanks and mid terrace

### `wool-shelter`
- **Form**: shed roof (single pitch)
- Compact (extent 4)
- Minimal windows, no gable windows
- Sits over / beside the wool rooms as light cover

## Placed dressing (see `grok-ridge.props.json`)

| Kind   | Count | Notes                                      |
|--------|-------|--------------------------------------------|
| House  | 7     | 1 hall, 4 cottages, 2 wool shelters        |
| Path   | 4     | crest, central run, approaches to both wools |
| Tree   | 4     | spruce, framing the upper and low areas    |

All coordinates are in the same cell space as the plan. The studio scales and seats them on real ground when the layout is finished / exported.
