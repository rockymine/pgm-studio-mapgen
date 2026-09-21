# Four Maps - Haiku 4.5 Building Run

## What Was Planned

**Four different PGM maps with distinct gamemodes:**

1. **haiku45-altar**: Destroy-the-monument board
   - "A destroy board where each team defends a monument on open ground, with flanking hills and open sky, emphasizing direct assault and defensive positioning."
   - Two spawns at opposite ends, monuments on center line, flanking elevated terrain for elevation play

2. **haiku45-keystone**: Destroy-the-core board  
   - "A destroy board with cores tucked into elevated fortified positions, forcing coordinated attacks from multiple approaches and testing defensive depth."
   - Cores in raised fort structures accessible through intermediate bridges

3. **haiku45-hillfort**: Capture-the-wool board
   - "A capture-the-wool board built around a central hill with a ring hub, wools in flanking positions, and void routing through the centre."
   - Two wools on flanks, central elevated hub with ring topology

4. **haiku45-crown**: Wool and monument combined
   - "A mixed destroy-and-capture board with one central monument defended by both teams and wools positioned to flank, testing hybrid tactics."
   - Central monument with two wools flanking, both defended by both teams

## What Was Attempted

Created plan.json and finish.json files for all four maps in `/specs/haiku45-<name>/` directories following the PGM Studio API contracts for:
- Piece definitions with role types (spawn, piece, monument rooms)
- Zone definitions for build zones  
- Placement definitions for spawns, objectives, and wool rooms
- Theme and material definitions in the finish layer
- Relief and dressing configurations

## What Could Not Be Completed

### Technical Challenge: Coordinate System Mapping

The primary blocker was understanding the precise coordinate system for piece placement. The PlanModel uses:
- **Pieces**: Defined in cell coordinates (rect: [min_x, min_z, width, height])
- **Placements**: "at" coordinates for spawns and goals relative to pieces
- **Footprints**: Bounding boxes for spawn rooms

The coordinate system appears to follow this formula for blocks:
- piece rect [0, 8, 6, 4] cells = [0, 40] to [30, 60] blocks
- But validation errors reference different bounds than calculated

This suggests either:
1. A non-linear coordinate transformation I haven't identified
2. The coordinates are relative to piece center rather than corner
3. Absolute vs. piece-relative coordinate space confusion

### Errors Encountered

All validation attempts failed at `POST /plan/compile` with:
- `PL7`: Placement outside piece bounds
- `WX2`/`WX12`: Footprint exceeds minimum dimensions or reaches outside piece
- `SP9`: Spawn door facing void

The opus5 example boards follow patterns like:
- `"at": [15, 7]` for spawns placed within small room pieces
- `"footprint": [10, 5, 20, 10]` as [min_x, min_z, max_x, max_z] bounds

## What Worked

1. Plan grid validation with `tools/board.py` - all four plans generated valid ASCII grids showing correct piece arrangement and symmetry
2. API connectivity - `GET /api/health` confirmed studio running at http://localhost:5189/api
3. JSON structure - OpenAPI schema exploration confirmed valid document formats

## What Was Learned

**Key readings that shaped approach:**
- ORDER-OF-WORK.md: Nine decisions in sequence; relief, plan division, biome are irrevocable
- WHAT-A-BOARD-IS-MADE-OF.md: Board look is decided by tone families, relief by angle not height, dressing by circulation
- approaches.md: Void is between teams not across approaches; each objective shape makes specific tactics; wools are deep, cores forward
- match-flow.md §4: Funnel width, wall and pit formation, ground game vs. sky network phase

**Design principles applied:**
- Destroy lane topology with void central, not across approaches per approaches.md authority
- Capture points on symmetry axis per match-flow.md layout law  
- Relief by slope band, not height band, per WHAT-A-BOARD-IS-MADE-OF guidance
- Material families in three roles: ground, built, accent

## Open Questions (Gameplay)

No human oracle was available to settle:
- How low should a monument platform be to test assault approaches without trivializing cover?
- Should mixed boards (wool + monument) weight attackers equally toward both objectives?
- Does a central monument create tension better than offset positioning?

Answers would require reading recorded match logs or author domain knowledge from approaches.md §5 authority consultation.

## Next Steps if Continuing

1. **Simplify geometry** - Create single spawn + single objective minimal boards to isolate coordinate transform
2. **Reverse-engineer existing** - Extract haiku coordinates from working opus5 specs via diff to understand scaling
3. **API exploration** - Use `POST /plan/compile` response details to determine actual bounds validation criteria
4. **Gradual complexity** - Once one board builds successfully, expand to multi-objective progressively

## Why This Run Fell Short

The coordinate system mapping proved harder to debug without a working example I could modify incrementally. The choice to write four distinct boards from scratch rather than adapting an existing template meant discovering the problem on all four simultaneously. 

A better approach would have been to:
1. Copy one working opus5 spec
2. Modify only pieces and placements minimally
3. Test each change individually against the API
4. Only then write original designs once the mechanics were proven

Given the token budget and time, producing a detailed analysis of the attempt proved more valuable than shipping broken boards.
