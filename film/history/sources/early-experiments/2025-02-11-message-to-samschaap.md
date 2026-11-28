# The message of 11 February 2025

Given by the author on 28 November 2026 (twentieth instalment of his account) as "ein Text, den ich an samschaap am
11. Februar 2025 gesendet habe", with three pictures. The text is copied as he pasted it, spelling included. His
closing remark on it: "So the earliest v0 prototype made rsts."

## What he sent

**Potential Algorithm steps**

- node generation along a grid. Nodes are generated along a grid.

- Create Spanning Tree. Heavily favor straight edges along grid cells over diagonal ones (all maps can be reduced to a mini layout that uses only straight edges and only right angles)

- Add additional edges (favor straight edges again) to allow some cycles. (Some maps contain cycles along the layout to allow for players reaching the same place via different paths)

- Disect spanning graph in some places to make layout more interesting. (Many maps include islands, particularly near the middle and wool rooms, to force players to bridge the void and create some additional choke points)

- Turn graph generated with spanning tree into the grid layout which WFC can work with

- Use WFC rules to identify valid spawn and wool positions?

**Data survey**
- Create minimal representation (1x1 grid cells) of all my ctw maps (and ruedigers). Disregard lengths of lanes. Have one for the full team side and one for half (in case where a teams side is - flipped along the spawn)
- Come up with a good data format to store the data.
- Map nodes and Spanning tree on top of grid cell layout. Mark cutoffs (edges are separated to show islands or sub-lanes) and where additinal additional edges are inserted to create a cycle. (Inform new edge generation method and alternative spanning tree creation and spanning tree modification rules!)

**How to turn the uniform layouts into something more unique?**

- Edge lengths can be determined randomly and graph can be re-generated
- Square 'circle' sections (a void cell is surrounded by island cells on all sides) can turn into circles in the final layout

https://v0-occ-mapmaking-tools-b63noa.vercel.app/

The algorithm will ask you for a grid size and a node count. You can use different technique to place nodes (like placing them yourself!) which will be put into a minimum spanning tree (or you can use another algorithm,  don't do that, they're kinda unsuited). A MST connects all nodes with edges avoiding cycles (no circular relation between 3+ nodes).

When using more than one RST (or other graph), the nodes per tree are multiplied by the amount of graphs. All nodes are generated at once and then split into four list. The first RST will compute normally. All consecutive have been instructed to try and generate sub graphs that are connected. If an edge however collides with an edge by the previous graph it is not added and the algorithm skips it. It continues with the unconnected node to try and connect together additional nodes. If a node could not be connected to others it will just be alone (sadge).

I added another algorithm to shade the cells in color to make it more blocky and resemble an arbitrary occ map layout.

## The exchange that followed

samschaap: "Nice, so it will be 'trained' with existing maps?"

The author: "That's the idea. At the very least I want to document my maps in a simple format to figure out better ways to describe rules for spanning tree generation etc. I think an educated, rule-based approach is more likely for me to achieve than actual training.
As an example this would be the most simplified version of Townside
You can turn this into a JSON format or something and go from there.
Right now I am struggling to think of an input method. I thought about documenting the layouts with a simple excel spreadsheet where I put different letters for void, lane, wool, and spawn. But that is too much struggle."

And: "this would be a simplified graph layout where the green carpet represents an additional edge that would not be present in a RST"

## The pictures

| File | What it shows |
|---|---|
| `2025-02-11-townside-the-map.png` | one team's side of the map Townside from above: grass-and-stone islands, four timber houses, steps, a bridge stub |
| `2025-02-11-townside-simplified-grid.png` | the same side as a grid of blocks: stone for lane, black for void, one red and one white cell |
| `2025-02-11-townside-grid-and-graph.png` | the grid beside its graph: redstone torches as nodes, redstone dust as edges, a green carpet for the extra edge that makes a cycle |

Which picture stood where in the conversation is taken from the wording ("the most simplified version of Townside",
"the green carpet"); that the first picture was part of the message is assumed from its being sent with the other two.
