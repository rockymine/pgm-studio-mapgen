# Haiku CTW Rush

## Overview

A Capture the Wool map designed as a simple, frontline-based CTW board testing basic woolroom and spawn setup. Intended to explore whether CTW routing and objective placement work end-to-end through the API.

## Board Layout

**Dimensions:** 60×140 blocks, `rot_180` symmetry  
**Base surface:** y9, build ceiling y20  
**Surface range:** y1..26

### Pieces

- **Spawn**: 40×30 blocks, surface 9 — spawn room and iron  
- **Mid-band**: 40×20 blocks, surface 9 — passage between spawn and frontline
- **Frontline mid**: 20×10 blocks, surface 10 — central frontline bar
- **Frontline left**: 10×10 blocks, surface 10 — left leg
- **Frontline right**: 10×10 blocks, surface 10 — right leg
- **Hub**: 30×20 blocks, surface 9 — central meeting space
- **Wool room**: 20×10 blocks, surface 9 — wool placement location

## Gameplay

**Route structure:** Standard spawn → mid-band → frontline forks → hub → wool-room

**Wool placement:** Single wool per team, center of wool-room

**Approach:**
- Players must cross the frontline to reach the wool
- Frontline geometry provides three potential routes (mid, left, right)
- Defender control point is at the hub entrance

## What Worked

- Wool room role compiles and stamps correctly  
- Build zones apply over the play area
- Iron placement in spawn works
- Single wool per team routes cleanly

## Known Limitations

1. **No architectural features** — frontline pieces all flat rectangles, no void hops or defensive features
2. **Hub is solid** — no internal structure, just open ground
3. **No relief** — terrain is flat grid
4. **Minimal dressing** — only basic flora coverage
5. **No secondary routes** — topology is tree-like, not multi-threaded

## Plan Slug

`haiku-ctw-rush-2`
