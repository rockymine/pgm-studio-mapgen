"""Emberfrost: a destroy-the-core board for two teams of twenty-four on one island held in the void, mirrored across z = -0.5.
Red holds the north (z < 0), blue is its mirror image. West is the ice lane and east the fire lane, the orchard of Amberford
lies between them and the Thaw, a gorge with water in its west half and lava in its east, crosses the waist. Each team keeps
two cores: the Rime Core in the ice keep on the glacier's shoulder and the Forge Core on the caldera floor.

    Hearth yard      the spawn, in a level yard under the back ridge, a lodge and two outbuildings
    Rime Keep        the ice core: a round stone keep on a terrace at 72 on the glacier's shoulder
    The Mirror       a frozen lake below the glacier; the Blue Cave runs from its shore up under the terrace into the keep
    The Forge        the fire core: a crater at 66 ringed by rock at 77, a lava moat round a plinth, two gaps in the rim
    Amberford        an orchard hamlet in the middle, Beacon Hill over it
    The Thaw         the gorge: Frostspan over the water, the Cinder Span over the stone bar, Brimstone Bridge over the lava
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

import land  # noqa: E402
from pgmvox.core.blocks import B  # noqa: E402
from pgmvox.play.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402

BOARD = "emberfrost"
X_MIN, X_MAX = land.X0, land.X0 + land.NX - 1
Z_MIN, Z_MAX = land.Z0, land.Z0 + land.NZ - 1
SYM = land.SYM
KILL_Y = 4
MAX_BUILD = 118
BIOME = 35                                  # Savanna: a gold grass and foliage, the autumn the whole board leans on

X, Z, H, LAND = land.ground()


def g(x, z):
    """The ground's floor block at a column."""
    return int(H[x - X_MIN, z - Z_MIN])


# ---- the spawn -------------------------------------------------------------------------------------------------------
YARD = land.PAD_SPAWN
SPAWN_AT = (0, g(0, -76) + 1, -76)
OBSERVER_AT = (0, 100, 0)
SPAWN_AREA = Box(-16, 0, -94, 16, 140, -70)

# ---- the cores: a five-cube of obsidian round three cubes of lava, floating three over the floor under it -----------
FLOAT = 3
RIME = land.RIME
FORGE = land.FORGE
RIME_CORE = Box(RIME[0] - 2, land.RIME_LEVEL + 1 + FLOAT, RIME[1] - 2, RIME[0] + 2, land.RIME_LEVEL + FLOAT + 5, RIME[1] + 2)
FORGE_CORE = Box(FORGE[0] - 2, land.FORGE_LEVEL + 1 + FLOAT, FORGE[1] - 2, FORGE[0] + 2, land.FORGE_LEVEL + FLOAT + 5, FORGE[1] + 2)

# ---- the places: (name, x, z), red's half; their images are blue's ------------------------------------------------------
PLACES = [("HEARTH YARD (spawn)", 0, -80), ("Hearth Lodge", 0, -88), ("RIME KEEP (ice core)", RIME[0], RIME[1]),
          ("the Mirror", -50, -28), ("the Blue Cave", -52, -44), ("Frostspan", -40, -8), ("THE FORGE (fire core)", FORGE[0], FORGE[1]),
          ("Brimstone Bridge", 40, -8), ("the Cinder Span", 0, -8), ("Amberford", 2, -52), ("Beacon Hill", land.BEACON[0], land.BEACON[1]),
          ("the Cider Orchard", 12, -26), ("Aurora Pines", -22, -72), ("Ash Hills", 62, -22), ("the Shingle", -26, -4)]


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 24), ("blue-team", "Blue", "blue", 24)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=SPAWN_AREA, protect=True))
    O.add(Observer(OBSERVER_AT, yaw=0), mirror=False)
    O.add(Core("red-rime", "Red Rime Core", "red-team", RIME_CORE, leak=5), name="Blue Rime Core")
    O.add(Core("red-forge", "Red Forge Core", "red-team", FORGE_CORE, leak=5), name="Blue Forge Core")
    return O
