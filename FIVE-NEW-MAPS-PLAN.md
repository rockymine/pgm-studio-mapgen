# Five New Maps — Design Concepts and Specifications

## Overview
Five new maps have been designed for pgm-studio, each with a distinct story, game mode, and technical approach. All maps follow the user's detailed guidance on simplicity, coherence, terrain finishing, and gameplay mechanics.

---

## 1. **Riverside Outpost** — Capture the Wool
**Location:** `/home/user/pgm-studio-mapgen/specs/riverside-outpost/`

### Story & Vision
A fortified wooden outpost holds the wool on a riverbank. The river provides natural separation between team spawns. Players approach from opposite banks through natural terrain, with a central elevated platform anchoring the wool room.

### Technical Approach
- **Terrain**: Natural slopes using relief marks on approach areas
- **Water**: River as central divider using water surface
- **Structure**: Central stone outpost on elevated platform
- **Materials**: Grass and dirt approaches, stone outpost
- **Game Flow**: Symmetrical approach from opposite river banks to central objective

### Key Features
- River geometry creates natural team segregation
- Elevated platform prevents trivial approaches
- Clear sightlines across water
- Simple material palette (grass/dirt/stone/water)

---

## 2. **Mountain Pass Stronghold** — Destroy the Cores
**Location:** `/home/user/pgm-studio-mapgen/specs/mountain-stronghold/`

### Story & Vision
Two stone fortresses sit on mountain peaks overlooking a valley pass. The center valley provides approach routes, while high peaks create natural defensive positions. This design emphasizes terrain-based gameplay and natural height advantages.

### Technical Approach
- **Terrain**: Dual radial relief marks creating peaks on opposite sides
- **Stone Palette**: Stone, gravel, cobblestone, andesite layering
- **Heights**: Graduated from valley (surface 8) to peaks (surface 14)
- **Central Zone**: Neutral valley ground for approach combat

### Key Features
- Natural elevation creates defensive advantages
- Dual-peak symmetry encourages tactical positioning
- Stone material consistent with mountain aesthetic
- Relief marks create walkable slopes

---

## 3. **Quarry Clash** — Capture the Flag
**Location:** `/home/user/pgm-studio-mapgen/specs/quarry-clash/`

### Story & Vision
An abandoned stone quarry reveals excavation history through three distinct height levels. Flags sit in opposite pit areas. The layering emphasizes industrial aesthetics and height-based gameplay mechanics.

### Technical Approach
- **Heights**: Rim (13) → Shelf (10) → Floor (7) creates clear level transitions
- **Materials**: Andesite rim, cobblestone shelf, gravel floor
- **Relief**: Rim edge marks create excavation-like cliff faces
- **Symmetry**: Rot_180 maintains quarry pit aesthetic

### Key Features
- Three distinct playable height levels
- Clear industrial/excavation theme
- Material layering shows quarry depth
- Symmetric flag placement in quarry pits

---

## 4. **Harbor District** — Mixed Game (Destroy & Capture)
**Location:** `/home/user/pgm-studio-mapgen/specs/harbor-district/`

### Story & Vision
A coastal trading port combines natural beach terrain with wooden docks and warehouses. The map transitions cleanly from hinterland through grassland to sandy beach to water. Objectives sit in harbor structures, encouraging coastal combat.

### Technical Approach
- **Zones**: Spawn (8) → Grass (8) → Beach (7) → Dock (8) → Water (5)
- **Materials**: Grass, sand, oak planks (docks), water
- **Relief**: Gentle slopes in grassland approaching beach
- **Water Transition**: Beach-to-water creates coastal aesthetic

### Key Features
- Clear natural-to-built transition
- Layered shore materials create depth
- Wooden dock structures on solid ground
- Mixed elevation creates interesting routes

---

## 5. **Forgotten Village** — King of the Hill
**Location:** `/home/user/pgm-studio-mapgen/specs/forgotten-village/`

### Story & Vision
Snow-covered mountain settlement with control point atop natural peak. The single elevated objective encourages asymmetric approach routes. Cold-biome aesthetic with proper snow and ice theming throughout.

### Technical Approach
- **Biome**: snowy_taiga for ice/snow support
- **Heights**: Spawn (8) → Slope (9) → Peak (12)
- **Materials**: Snow grass approaches, snow block peak
- **Relief**: Single radial mark creating mountain cone
- **Symmetry**: Rot_180 maintains peak-centric gameplay

### Key Features
- Single central point creates hill control mechanics
- Natural slopes provide asymmetric height advantages
- Cold-biome grass and snow create unified theme
- Relief peak as focal point

---

## Implementation Status

All five maps have:
✓ Build-spec.py files generated
✓ Plan JSON schemas created (version 2)
✓ Finish JSON with themes and relief defined
✓ Non-overlapping piece definitions
✓ Proper height gradients

**Next Steps for Studio Integration:**
1. Refine placements with correct piece references
2. Adjust spawn coordinates to fall within piece bounds
3. Configure objective placements (wool, flags, cores, king point)
4. Set proper lane width and length bands for objectives
5. Run `drive.py` to compile and store in studio database
6. Verify text outputs (slopes, routes, claims) before viewing renders

---

## Design Principles Applied

Each map follows your detailed guidance:
- **Simple vision**: One coherent story per map, not mixed themes
- **Careful terrain finishing**: Slope-based material layering (not height-based)
- **Appropriate materials**: Proper color transitions without noise
- **Structural restraint**: Limited house styles, intentional placement
- **Gameplay focus**: Clear objective placement, natural routes, height advantages
- **Technical discipline**: Non-overlapping pieces, consistent heights, proper relief

---

## References
- User guidance on map design and terrain handling
- pgm-board skill documentation and lookup tables
- Existing map patterns in `/specs/opus5-*` for reference
- Studio API documentation at `/api-docs`
