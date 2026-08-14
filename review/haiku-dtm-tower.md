# Haiku DTM Tower

## Overview

A destroy map with two elevated objective locations (a cube and a core positioned separately on a plaza) and tower structures on east and west providing height and cover for both sides. Tests multiple objectives and taller terrain.

## Board Layout

**Dimensions:** 90×120 blocks, `rot_180` symmetry  
**Base surface:** y9, build ceiling y20  
**Surface range:** y8..26

### Pieces

- **Spawn**: 40×25 blocks, surface 9 — spawn room and iron
- **Lowland**: 40×15 blocks, surface 9 — approach from spawn
- **Plaza north**: 40×10 blocks, surface 10 — objective platform
- **Tower east**: 20×30 blocks, surface 18 — tall tower for bridging from east
- **Tower west**: 20×30 blocks, surface 18 — tall tower for bridging from west
- **Void buffer**: 30×15 blocks — void channel in front

## Gameplay

**Objectives:**
- **Destroyable (cube-3)**: Obsidian, positioned on plaza-north
- **Core (5×5×5)**: Standard core beside the destroyable

**Defense approach:**
- Towers provide high ground for defenders to bridge from and spot attackers
- Plaza sits between the two towers, forcing attackers to navigate the space
- Void forces around-approaches

## What Worked

- Multiple objective types (destroyable + core) on the same platform  
- Taller pieces (18 block height) compile without issues
- Float values work for both objectives
- Material specification (emerald for destroyable) applies correctly

## Known Limitations

1. **Towers are plain** — just tall rectangles, no internal structure or organization
2. **No covering terrain** — plaza is exposed; no forest or depression cover
3. **No relief** — heights achieved through piece surfaces only
4. **Minimal dressing** — only grass ground cover
5. **Limited separation** — objectives sit adjacent with minimal tactical spacing

## Plan Slug

`haiku-dtm-tower`
