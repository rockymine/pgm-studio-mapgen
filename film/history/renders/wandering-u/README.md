# Wandering U, rendered

Rendered from the world and `map.xml` the author supplied on 27 November 2026 as a zip from the private maps repository. The
world is saved with the wool rooms at their start stop (the rear dock); a match moves them, so every picture shows
stop 0. Nothing of the map itself is committed here, only these pictures. Camera conventions: x east, y up, z south;
yaw 0 looks south, 90 looks west; pitch positive looks down. All JPG, quality 90, looked at before saving.

| file | size | camera (x, y, z, yaw, pitch, fov) | shows |
|---|---|---|---|
| `01-overview-top.jpg` | 960x540 | straight down, from the render tool's `overview` | The whole map from above: two mirrored combs of grass-and-brick terrain hanging off a central spine, a 20x20 void gap between them, the two spawn buildings at the left edge, a bedrock 10x10 wool room at the right of each half, and a small dark block at the middle right (near the observer spawn at 0,25,0). |
| `02-whole-map.jpg` | 1920x1080 | -30, 70, -125, 0, 38, 75 | The map from the red end looking south. Red half in front, blue half behind; the bedrock chunk with a red wool band at the left of the red half is the wool room parked at its rear dock; the white box at far left is the front-dock platform. |
| `03-wool-room-at-rear-dock.jpg` | 1920x1080 | 24, 34, -98, 50, 22, 70 | The red half's wool room (bedrock column x -10..0, y 0..22, z -75..-65, with the 8x8 cage and red wool band on top) at the end of the white-and-red leg, with the front-dock platform at lower left and the other half behind. |
| `04-wool-room-underside.jpg` | 1920x1080 | 28, -18, -90, 60, -30, 80 | The same room seen from below the world: the bedrock reaches down to y 0 and nothing is under it but sky, as is every other piece of the map. |
| `05-red-spawn.jpg` | 1920x1080 | -52, 22, -40, 90, 18, 75 | The red spawn building: a stone-brick deck leading into a bedrock cage, with the red spawn pad (red wool, x -71..-70, z -41..-40, y 14) on its floor. |

Facts read from the blocks, with coordinates: the room's red wool (damage 14) is at x -8..-2, y 14..18, z -72..-67, and
the bedrock column is at x -12..-1, y 0..22, z -75..-66 at the saved stop. The world's bounds are x -75..9, y 0..25,
z -75..74. A camera at the front dock was tried and discarded because the picture did not show the dock clearly.
