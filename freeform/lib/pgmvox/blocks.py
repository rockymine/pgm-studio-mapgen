"""Block ids, block classes and colours: one table for every freeform board.

The names and constants in `B` are the 1.8 ids a generator writes. Everything else here is read from
`data/blocks.json`, which `data/export_blocks.cs` writes from the studio's own palette: the display name and
colour of every id and data value, its role and shape, and the data it takes under each symmetry operation.
Nothing here keeps a colour of its own, so a board renders in the colours the studio uses.

The classes are the questions a board asks of a block:

    PASSABLE      a player walks through it (air, flora, what lies flat or hangs, water, ladders)
    CLIMBABLE     a player climbs it (ladders, vines)
    LIQUID        water and lava, still and flowing
    NOT_GROUND    what World.top() steps past to find the ground (passable, leaves, logs of a tree are ground)
    SIGHT_CLEAR   an eye sees through it (passable, glass, panes, bars, fences, walls, gates); leaves hide
    GRAVITY       falls if nothing is under it
    FORBIDDEN_IN_PLAY  never placed where players walk (lava, fire, TNT, spawners, barriers, bedrock, cobweb)
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


class B:
    """1.8 block ids. A constant names an id; its data value (wood, colour, facing) goes beside it."""
    AIR = 0
    STONE = 1          # data 1 granite, 2 pol granite, 3 diorite, 4 pol diorite, 5 andesite, 6 pol andesite
    GRASS = 2
    DIRT = 3           # data 1 coarse, 2 podzol
    COBBLE = 4
    PLANKS = 5         # 0 oak 1 spruce 2 birch 3 jungle 4 acacia 5 dark oak
    SAPLING = 6
    BEDROCK = 7
    WATER_FLOW = 8
    WATER = 9
    LAVA_FLOW = 10
    LAVA = 11
    SAND = 12          # data 1 red sand
    GRAVEL = 13
    GOLD_ORE = 14
    IRON_ORE = 15
    COAL_ORE = 16
    LOG = 17           # 0 oak 1 spruce 2 birch 3 jungle; +4 along x, +8 along z, +12 bark
    LEAVES = 18        # +4 no-decay
    SPONGE = 19
    GLASS = 20
    LAPIS_ORE = 21
    LAPIS_BLOCK = 22
    DISPENSER = 23
    SANDSTONE = 24     # 1 chiseled 2 smooth
    NOTE_BLOCK = 25
    BED = 26
    RAIL_POWERED = 27
    RAIL_DETECTOR = 28
    STICKY_PISTON = 29
    COBWEB = 30
    TALLGRASS = 31     # 1 grass 2 fern
    DEADBUSH = 32
    PISTON = 33
    WOOL = 35          # data: the sixteen dyes
    DANDELION = 37
    FLOWER = 38        # 0 poppy 1 orchid 2 allium 3 bluet 4-7 tulips 8 oxeye
    BROWN_MUSHROOM = 39
    RED_MUSHROOM = 40
    GOLD_BLOCK = 41
    IRON_BLOCK = 42
    DSLAB = 43         # double slab 0 stone 1 sandstone 3 cobble 4 brick 5 stonebrick 7 quartz
    SLAB = 44          # 0 stone 1 sandstone 3 cobble 4 brick 5 stonebrick 7 quartz; +8 upper half
    BRICK = 45
    TNT = 46
    BOOKSHELF = 47
    MOSSY = 48
    OBSIDIAN = 49
    TORCH = 50         # 1 east 2 west 3 south 4 north 5 floor (the way it points)
    FIRE = 51
    SPAWNER = 52
    OAK_STAIRS = 53
    CHEST = 54
    REDSTONE_WIRE = 55
    DIAMOND_ORE = 56
    DIAMOND_BLOCK = 57
    CRAFTING = 58
    WHEAT = 59
    FARMLAND = 60
    FURNACE = 61
    SIGN_POST = 63     # 0-15 rotation, 0 south, 4 west, 8 north, 12 east
    OAK_DOOR = 64
    LADDER = 65        # 2 north 3 south 4 west 5 east (the way it faces)
    RAIL = 66
    COBBLE_STAIRS = 67
    WALL_SIGN = 68     # as ladder
    LEVER = 69
    PLATE_STONE = 70
    IRON_DOOR = 71
    PLATE_WOOD = 72
    REDSTONE_ORE = 73
    REDSTONE_TORCH = 76
    BUTTON_STONE = 77
    SNOW_LAYER = 78
    ICE = 79
    SNOW = 80
    CACTUS = 81
    CLAY = 82
    REEDS = 83
    JUKEBOX = 84
    FENCE = 85
    PUMPKIN = 86       # 0 south 1 west 2 north 3 east
    NETHERRACK = 87
    SOUL_SAND = 88
    GLOWSTONE = 89
    JACK = 91
    CAKE = 92
    STAINED_GLASS = 95
    TRAPDOOR = 96
    MONSTER_EGG = 97
    STONEBRICK = 98    # 1 mossy 2 cracked 3 chiseled
    BROWN_CAP = 99     # huge mushroom; 10 stem, 14 cap all sides, 15 stem all sides
    RED_CAP = 100
    IRON_BARS = 101
    PANE = 102
    MELON = 103
    VINE = 106
    FENCE_GATE = 107
    BRICK_STAIRS = 108
    STONEBRICK_STAIRS = 109
    MYCELIUM = 110
    LILY = 111
    NETHER_BRICK = 112
    NETHER_FENCE = 113
    NETHER_STAIRS = 114
    ENCHANTING = 116
    BREWING = 117
    CAULDRON = 118
    END_STONE = 121
    REDSTONE_LAMP = 123
    WOOD_DSLAB = 125
    WOOD_SLAB = 126    # +8 upper half
    COCOA = 127
    SANDSTONE_STAIRS = 128
    EMERALD_ORE = 129
    ENDER_CHEST = 130
    EMERALD_BLOCK = 133
    SPRUCE_STAIRS = 134
    BIRCH_STAIRS = 135
    JUNGLE_STAIRS = 136
    BEACON = 138
    COBBLE_WALL = 139  # 1 mossy
    FLOWER_POT = 140
    CARROTS = 141
    POTATOES = 142
    BUTTON_WOOD = 143
    SKULL = 144
    ANVIL = 145
    TRAPPED_CHEST = 146
    REDSTONE_BLOCK = 152
    HOPPER = 154
    QUARTZ = 155       # 1 chiseled 2 pillar upright 3 pillar along x 4 pillar along z
    QUARTZ_STAIRS = 156
    RAIL_ACTIVATOR = 157
    DROPPER = 158
    STAINED_CLAY = 159
    STAINED_PANE = 160
    LEAVES2 = 161      # 0 acacia 1 dark oak; +4 no-decay
    LOG2 = 162         # 0 acacia 1 dark oak
    ACACIA_STAIRS = 163
    DARK_OAK_STAIRS = 164
    SLIME = 165
    BARRIER = 166
    IRON_TRAPDOOR = 167
    PRISMARINE = 168   # 1 bricks 2 dark
    SEA_LANTERN = 169
    HAY = 170          # +4 along x, +8 along z
    CARPET = 171
    HARDENED_CLAY = 172
    COAL_BLOCK = 173
    PACKED_ICE = 174
    DOUBLE_PLANT = 175  # 0 sunflower 1 lilac 2 tallgrass 3 fern 4 rose 5 peony; upper half 8
    BANNER = 176       # standing, rotation as a sign post
    WALL_BANNER = 177  # as ladder
    RED_SANDSTONE = 179
    RED_SANDSTONE_STAIRS = 180
    RED_SANDSTONE_SLAB = 182
    SPRUCE_FENCE_GATE = 183
    BIRCH_FENCE_GATE = 184
    JUNGLE_FENCE_GATE = 185
    DARK_OAK_FENCE_GATE = 186
    ACACIA_FENCE_GATE = 187
    SPRUCE_FENCE = 188
    BIRCH_FENCE = 189
    JUNGLE_FENCE = 190
    DARK_OAK_FENCE = 191
    ACACIA_FENCE = 192
    SPRUCE_DOOR = 193
    BIRCH_DOOR = 194
    JUNGLE_DOOR = 195
    ACACIA_DOOR = 196
    DARK_OAK_DOOR = 197


DYES = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
        "purple", "blue", "brown", "green", "red", "black"]
DYE = {name: k for k, name in enumerate(DYES)}

STAIRS = {53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180}
DOORS = {64, 71, 193, 194, 195, 196, 197}
FENCES = {85, 113, 188, 189, 190, 191, 192}
FENCE_GATES = {107, 183, 184, 185, 186, 187}
RAILS = {66, 27, 28, 157}


def _load():
    with open(os.path.join(HERE, "data", "blocks.json")) as f:
        rows = json.load(f)["blocks"]
    return {r["id"]: r for r in rows}


TABLE = _load()


def info(bid):
    """The studio's row for an id: name, role, shape flags, names and colours per data, turned data per op."""
    return TABLE[int(bid)]


def name(bid, data=0):
    return TABLE[int(bid)]["names"][int(data) & 15]


def _hex(h):
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


COLOURS = np.array([[_hex(TABLE[i]["colours"][d]) for d in range(16)] for i in range(256)], dtype=np.uint8)


def colour(bid, data=0):
    """(r, g, b) of a block as the studio paints it."""
    return tuple(int(v) for v in COLOURS[int(bid), int(data) & 15])


# ---- the classes ----------------------------------------------------------------------------------------
LIQUID = {i for i, r in TABLE.items() if r["liquid"]}
CLIMBABLE = {B.LADDER, B.VINE}
# what a player walks through: the studio's "stood through" (flora and what lies flat or hangs), air, water
# and ladders; doors, trapdoors and fence gates stay shut, as the studio reads them
PASSABLE = ({0} | {i for i, r in TABLE.items() if r["stood_through"]} | {B.WATER, B.WATER_FLOW, B.LADDER}
            | {B.SIGN_POST, B.WALL_SIGN, B.BANNER, B.WALL_BANNER, B.TORCH, B.REDSTONE_TORCH, 75, B.LEVER,
               B.BUTTON_STONE, B.BUTTON_WOOD, B.PLATE_STONE, B.PLATE_WOOD, 147, 148, B.REDSTONE_WIRE, 36,
               B.RAIL, B.RAIL_POWERED, B.RAIL_DETECTOR, B.RAIL_ACTIVATOR, B.CARPET, B.SNOW_LAYER, B.COBWEB,
               B.SAPLING, B.TALLGRASS, B.DEADBUSH, B.DANDELION, B.FLOWER, B.BROWN_MUSHROOM, B.RED_MUSHROOM,
               B.WHEAT, B.CARROTS, B.POTATOES, B.REEDS, B.VINE, B.LILY, B.DOUBLE_PLANT, B.COCOA, B.FIRE})
NOT_GROUND = PASSABLE | {B.LAVA, B.LAVA_FLOW, B.LEAVES, B.LEAVES2}
SIGHT_CLEAR = PASSABLE | {B.GLASS, B.STAINED_GLASS, B.PANE, B.STAINED_PANE, B.IRON_BARS, B.COBBLE_WALL} | FENCES \
    | FENCE_GATES
GRAVITY = {B.SAND, B.GRAVEL, B.ANVIL}
FORBIDDEN_IN_PLAY = {B.LAVA, B.LAVA_FLOW, B.FIRE, B.TNT, B.SPAWNER, B.BARRIER, B.BEDROCK, B.COBWEB}


def mask(ids, members):
    """A boolean array over an id volume: True where the id is in the class."""
    return np.isin(ids, sorted(members))
