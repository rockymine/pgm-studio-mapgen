"""The voxel volume the generator writes into, the 1.8 block ids it uses, and the bridge to write_world.cs.

Everything is numpy: ids uint16 and data uint8 over (x, y, z), offset by the world origin, so a builder
says `w.set(x, y, z, B.STONE)` in world coordinates and a terrain pass can write whole columns at once.
"""
import json
import os
import struct

import numpy as np


class B:
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
    SAND = 12
    GRAVEL = 13
    GOLD_ORE = 14
    IRON_ORE = 15
    COAL_ORE = 16
    LOG = 17           # 0 oak 1 spruce 2 birch 3 jungle; +4 along x, +8 along z, +12 bark
    LEAVES = 18        # +4 no-decay
    GLASS = 20
    DISPENSER = 23
    SANDSTONE = 24
    BED = 26
    RAIL_POWERED = 27
    COBWEB = 30
    TALLGRASS = 31     # 1 grass 2 fern
    DEADBUSH = 32
    WOOL = 35
    DANDELION = 37
    FLOWER = 38        # 0 poppy 1 orchid 2 allium 3 bluet 4-7 tulips 8 oxeye
    BROWN_MUSHROOM = 39
    RED_MUSHROOM = 40
    GOLD_BLOCK = 41
    IRON_BLOCK = 42
    DSLAB = 43         # double slab 0 stone 3 cobble 4 brick 5 stonebrick
    SLAB = 44          # 0 stone 1 sandstone 3 cobble 4 brick 5 stonebrick 7 quartz; +8 top half
    BRICK = 45
    TNT = 46
    BOOKSHELF = 47
    MOSSY = 48
    OBSIDIAN = 49
    TORCH = 50         # 1 east 2 west 3 south 4 north 5 floor
    SPAWNER = 52
    OAK_STAIRS = 53
    CHEST = 54
    CRAFTING = 58
    WHEAT = 59
    FARMLAND = 60
    FURNACE = 61
    SIGN_POST = 63
    OAK_DOOR = 64
    LADDER = 65
    RAIL = 66
    COBBLE_STAIRS = 67
    WALL_SIGN = 68
    LEVER = 69
    IRON_DOOR = 71
    PLATE_WOOD = 72
    SNOW_LAYER = 78
    ICE = 79
    SNOW = 80
    CLAY = 82
    REEDS = 83
    FENCE = 85
    PUMPKIN = 86       # 0 south 1 west 2 north 3 east
    NETHERRACK = 87
    GLOWSTONE = 89
    JACK = 91
    TRAPDOOR = 96
    STONEBRICK = 98    # 1 mossy 2 cracked 3 chiseled
    BROWN_CAP = 99
    IRON_BARS = 101
    PANE = 102
    MELON = 103
    VINE = 106
    FENCE_GATE = 107
    BRICK_STAIRS = 108
    STONEBRICK_STAIRS = 109
    LILY = 111
    CAULDRON = 118
    WOOD_DSLAB = 125
    WOOD_SLAB = 126    # +8 top half
    COCOA = 127
    SPRUCE_STAIRS = 134
    BIRCH_STAIRS = 135
    COBBLE_WALL = 139
    FLOWER_POT = 140
    CARROTS = 141
    POTATOES = 142
    SKULL = 144
    ANVIL = 145
    QUARTZ = 155
    STAINED_CLAY = 159
    STAINED_PANE = 160
    LEAVES2 = 161      # 0 acacia 1 dark oak; +4 no-decay
    LOG2 = 162         # 0 acacia 1 dark oak
    DARK_OAK_STAIRS = 164
    BARRIER = 166
    HAY = 170          # +4 along x, +8 along z
    CARPET = 171
    HARDENED_CLAY = 172
    COAL_BLOCK = 173
    PACKED_ICE = 174
    RED_SANDSTONE = 179
    CACTUS = 81
    DOUBLE_PLANT = 175  # 0 sunflower 1 lilac 2 tallgrass 3 fern 4 rose 5 peony; top half = 8
    BANNER = 176
    ACACIA_STAIRS = 163
    SPRUCE_FENCE_GATE = 183
    ACACIA_FENCE = 192
    DARK_OAK_FENCE_GATE = 186
    SPRUCE_FENCE = 188
    DARK_OAK_FENCE = 191
    SPRUCE_DOOR = 193
    DARK_OAK_DOOR = 197


# The ids a player stands on — what "ground" means for the surface reads in this generator.
NOT_GROUND = {B.AIR, B.WATER, B.WATER_FLOW, B.LAVA, B.LAVA_FLOW, B.LEAVES, B.LEAVES2, B.TALLGRASS, B.FLOWER,
              B.DANDELION, B.DOUBLE_PLANT, B.SAPLING, B.TORCH, B.WHEAT, B.CARROTS, B.POTATOES, B.REEDS,
              B.LILY, B.VINE, B.SNOW_LAYER, B.RED_MUSHROOM, B.BROWN_MUSHROOM, B.DEADBUSH, B.COBWEB}


class World:
    """A box of the world: x in [x0, x0+sx), y in [0, sy), z in [z0, z0+sz)."""

    def __init__(self, x0, z0, sx, sz, sy=128):
        self.x0, self.z0, self.sx, self.sy, self.sz = x0, z0, sx, sy, sz
        self.ids = np.zeros((sx, sy, sz), dtype=np.uint16)
        self.dat = np.zeros((sx, sy, sz), dtype=np.uint8)
        self.biome = np.full((sx, sz), 1, dtype=np.uint8)
        self.tiles = []

    # --- coordinates -------------------------------------------------------------------------------
    def inside(self, x, y, z):
        return 0 <= x - self.x0 < self.sx and 0 <= y < self.sy and 0 <= z - self.z0 < self.sz

    def set(self, x, y, z, bid, d=0):
        if self.inside(x, y, z):
            self.ids[x - self.x0, y, z - self.z0] = bid
            self.dat[x - self.x0, y, z - self.z0] = d

    def get(self, x, y, z):
        if not self.inside(x, y, z):
            return (0, 0)
        return int(self.ids[x - self.x0, y, z - self.z0]), int(self.dat[x - self.x0, y, z - self.z0])

    def id(self, x, y, z):
        return self.get(x, y, z)[0]

    def fill(self, xa, ya, za, xb, yb, zb, bid, d=0):
        """Inclusive box, clipped to the volume."""
        xa, xb = sorted((xa, xb)); ya, yb = sorted((ya, yb)); za, zb = sorted((za, zb))
        xa = max(xa, self.x0); xb = min(xb, self.x0 + self.sx - 1)
        za = max(za, self.z0); zb = min(zb, self.z0 + self.sz - 1)
        ya = max(ya, 0); yb = min(yb, self.sy - 1)
        if xa > xb or ya > yb or za > zb:
            return
        sl = (slice(xa - self.x0, xb - self.x0 + 1), slice(ya, yb + 1), slice(za - self.z0, zb - self.z0 + 1))
        self.ids[sl] = bid
        self.dat[sl] = d

    def top(self, x, z, ignore=NOT_GROUND):
        """The y of the highest ground block in a column, or -1."""
        if not (0 <= x - self.x0 < self.sx and 0 <= z - self.z0 < self.sz):
            return -1
        col = self.ids[x - self.x0, :, z - self.z0]
        for y in range(self.sy - 1, -1, -1):
            if int(col[y]) not in ignore:
                return y
        return -1

    def chest(self, x, y, z, items, facing=2):
        """items: [(slot, 'minecraft:id', count, damage)]. facing 2 north 3 south 4 west 5 east."""
        self.set(x, y, z, B.CHEST, facing)
        self.tiles.append({"kind": "Chest", "x": x, "y": y, "z": z,
                           "items": [{"slot": s, "id": i, "count": c, "damage": d} for s, i, c, d in items]})

    def sign(self, x, y, z, lines, wall_facing=None, rot=0):
        if wall_facing is None:
            self.set(x, y, z, B.SIGN_POST, rot)
        else:
            self.set(x, y, z, B.WALL_SIGN, wall_facing)
        self.tiles.append({"kind": "Sign", "x": x, "y": y, "z": z, "lines": list(lines)})

    def banner(self, x, y, z, base, patterns=(), wall_facing=None, rot=0):
        """A banner, standing (rot 0..15) or on a wall (facing 2 north 3 south 4 west 5 east); base is the dye
        colour, 1.8's numbering (0 black .. 15 white); patterns are (code, dye) pairs."""
        if wall_facing is None:
            self.set(x, y, z, B.BANNER, rot)
        else:
            self.set(x, y, z, 177, wall_facing)
        self.tiles.append({"kind": "Banner", "x": x, "y": y, "z": z, "base": base,
                           "patterns": [{"pattern": p, "color": c} for p, c in patterns]})

    # --- output ------------------------------------------------------------------------------------
    def save(self, build_dir, name, spawn):
        os.makedirs(build_dir, exist_ok=True)
        with open(os.path.join(build_dir, "volume.bin"), "wb") as f:
            f.write(b"RWV1")
            f.write(struct.pack("<6i", self.x0, 0, self.z0, self.sx, self.sy, self.sz))
            f.write(np.ascontiguousarray(self.ids, dtype="<u2").tobytes())
            f.write(np.ascontiguousarray(self.dat).tobytes())
            f.write(np.ascontiguousarray(self.biome).tobytes())
        with open(os.path.join(build_dir, "tiles.json"), "w") as f:
            json.dump(self.tiles, f)
        with open(os.path.join(build_dir, "level.json"), "w") as f:
            json.dump({"name": name, "spawn": list(spawn)}, f)
