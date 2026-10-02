"""Player-scale props, stated block by block.

Every prop is a stack of ASCII layers, bottom first. A layer's first row is the north edge, its first column
the west edge, and each character is one block named in the prop's legend as `id` or `id:data` in 1.8's
numbering — so a stair's facing, a button's wall and a sign's side are written where they stand. `.` and ` `
are air. A vehicle is drawn with its nose to the east.

`place` turns a prop by quarter turns and rewrites every direction-carrying data value with it, so one
drawing serves both lanes of a road.
"""

AIR = ".  "


class Prop:
    def __init__(self, name, title, theme, legend, layers, origin=(0, 0)):
        self.name = name
        self.title = title
        self.theme = theme
        self.legend = {key: parse(value) for key, value in legend.items()}
        self.layers = [block.strip("\n").split("\n") for block in layers]
        self.origin = origin

    def voxels(self):
        """`{(x, y, z): (id, data)}` relative to the prop's origin cell."""
        out = {}
        ox, oz = self.origin
        for y, rows in enumerate(self.layers):
            for z, row in enumerate(rows):
                for x, char in enumerate(row):
                    if char in AIR:
                        continue
                    if char not in self.legend:
                        raise KeyError(f"{self.name}: '{char}' at layer {y} row {z} col {x} has no legend entry")
                    out[(x - ox, y, z - oz)] = self.legend[char]
        return out


def parse(value):
    if isinstance(value, tuple):
        return value
    block, _, data = str(value).partition(":")
    return int(block), int(data or 0)


# --- turning ------------------------------------------------------------------------------------------------
# One quarter turn clockwise seen from above: north -> east -> south -> west.
STAIRS = {53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180}
WALL_FACING = {54, 61, 62, 65, 68, 130, 146, 23, 158, 154}       # 2 N, 3 S, 4 W, 5 E
ATTACHED = {50, 75, 76, 77, 143}                                   # 1 E, 2 W, 3 S, 4 N
SGWE = {86, 91, 107, 183, 184, 185, 186, 187, 26, 131}             # 0 S, 1 W, 2 N, 3 E (low two bits)
TRAPDOORS = {96, 167}                                              # 0 S, 1 N, 2 E, 3 W (hinge side)
DOORS = {64, 71, 193, 194, 195, 196, 197}                          # lower half: 0 W, 1 N, 2 E, 3 S

STAIR_CW = {0: 2, 2: 1, 1: 3, 3: 0}            # E->S, S->W, W->N, N->E
NSWE_CW = {2: 5, 5: 3, 3: 4, 4: 2}
ATTACHED_CW = {4: 1, 1: 3, 3: 2, 2: 4}
SGWE_CW = {0: 1, 1: 2, 2: 3, 3: 0}
TRAP_CW = {1: 2, 2: 0, 0: 3, 3: 1}
LEVER_CW = {**ATTACHED_CW, 5: 6, 6: 5, 7: 0, 0: 7}


def turn_data(block, data):
    if block in STAIRS:
        return (data & 4) | STAIR_CW[data & 3]
    if block in WALL_FACING:
        return NSWE_CW.get(data & 7, data & 7) | (data & 8)
    if block in ATTACHED:
        return ATTACHED_CW.get(data & 7, data & 7) | (data & 8)
    if block == 69:
        return LEVER_CW[data & 7] | (data & 8)
    if block in SGWE:
        return (data & ~3) | SGWE_CW[data & 3]
    if block in TRAPDOORS:
        return (data & ~3) | TRAP_CW[data & 3]
    if block in DOORS:
        return data if data & 8 else (data & ~3) | ((data + 1) & 3)
    if block in (17, 162, 170):
        axis = data & 12
        return (data & 3) | {0: 0, 4: 8, 8: 4, 12: 12}[axis]
    if block == 155 and data in (3, 4):
        return 7 - data
    if block == 145:
        return data ^ 1
    if block == 63:
        return (data + 4) & 15
    if block in (66, 27, 28, 157) and (data & 7) in (0, 1):
        return (data & 8) | ((data & 7) ^ 1)
    return data


def place(prop, x, y, z, turns=0):
    """The prop's voxels in world coordinates, turned `turns` quarter turns clockwise about its origin."""
    out = {}
    for (dx, dy, dz), (block, data) in prop.voxels().items():
        for _ in range(turns % 4):
            dx, dz = -dz, dx
            data = turn_data(block, data)
        out[(x + dx, y + dy, z + dz)] = (block, data)
    return out


def lay(*rows):
    return "\n".join(rows)


# --- the props ----------------------------------------------------------------------------------------------
# Shared words, overridden per prop where a character means something else.
COMMON = {
    "#": "173",        # coal block: a tyre
    "|": "102",        # glass pane
    "n": "77:4",       # stone button on a north face (hubcap, handle)
    "v": "77:3",       # stone button on a south face
}

PROPS = []


def prop(name, title, theme, legend, layers, origin=(0, 0)):
    made = Prop(name, title, theme, {**COMMON, **legend}, layers, origin)
    PROPS.append(made)
    return made


# Modern street ----------------------------------------------------------------------------------------------

prop("hatchback", "Hatchback", "modern", {
    "q": "155", "Q": "155:1", "T": "159:14", "L": "155:1", "s": "156:0", "S": "156:1",
    "b": "44:7", "c": "171:0", "K": "54:4", "p": "68:5", "P": "68:4", "k": "77:1",
}, [
    lay("..n..n..",
        "..#qq#..",
        ".qqqqqq.",
        "..#qq#..",
        "..v..v.."),
    lay("....n...",
        ".TqqqqLk",
        "PqqqqqQp",
        ".TqqqqLk",
        "....v..."),
    lay("........",
        ".s||||b.",
        ".sKSS|b.",
        ".s||||b.",
        "........"),
    lay("........",
        "..cccc..",
        "..cccc..",
        "..cccc..",
        "........"),
], origin=(1, 1))

prop("jeep", "Off-roader", "modern", {
    "g": "159:13", "F": "191", "R": "123", "i": "101", "w": "77:2", "f": "191",
    "S": "134:1", "V": "69:6", "c": "171:13",
}, [
    lay("...n..n..",
        "...#..#..",
        "...F..F..",
        "...#..#..",
        "...v..v.."),
    lay(".........",
        "..gggggR.",
        "w#gggggi.",
        "..gggggR.",
        "........."),
    lay(".........",
        "..fSS|cc.",
        "...SV|cc.",
        "..fSS|cc.",
        "........."),
    lay(".........",
        "..f......",
        "..f......",
        "..f......",
        "........."),
], origin=(2, 1))

prop("bus", "City bus", "modern", {
    "c": "159:7", "Y": "159:4", "T": "159:14", "R": "123", "S": "135:1",
    "D": "71:3", "E": "71:8", "l": "160:3", "_": "44:7", "p": "68:5",
    "m": "69:4", "M": "69:3", "A": "151",
}, [
    lay("..n.....n..",
        ".c#ccccc#c.",
        ".ccccccccc.",
        ".c#ccccc#c.",
        "..v.....v.."),
    lay("...........",
        ".TYYYYYYYR.",
        ".YSSSSS.SY.",
        ".TYYYYYDYR.",
        "..........."),
    lay(".........m.",
        ".YlllllllY.",
        ".l.......l.",
        ".YlllllElY.",
        ".........M."),
    lay("...........",
        ".________Y.",
        ".________Yp",
        ".________Y.",
        "..........."),
    lay("...........",
        "...........",
        "....AA.....",
        "...........",
        "..........."),
], origin=(1, 1))

prop("box-truck", "Delivery truck", "modern", {
    "t": "44:8", "W": "35:0", "X": "35:14", "R": "159:14", "L": "123", "i": "101",
    "P": "68:4", "S": "114:1", "c": "171:14", "_": "44:7", "m": "69:4", "M": "69:3",
}, [
    lay("..nn....n..",
        ".t##tttt#t.",
        ".ttttttttt.",
        ".t##tttt#t.",
        "..vv....v.."),
    lay("...........",
        ".WWWWWWRRL.",
        "PWWWWWWRRi.",
        ".WWWWWWRRL.",
        "..........."),
    lay(".......m...",
        ".XXXXXXR||.",
        ".WWWWWWRS|.",
        ".XXXXXXR||.",
        ".......M..."),
    lay("...........",
        ".WWWWWWRcc.",
        ".WWWWWWRcc.",
        ".WWWWWWRcc.",
        "..........."),
    lay("...........",
        ".______....",
        ".______....",
        ".______....",
        "..........."),
], origin=(1, 1))

prop("quad", "Quad bike", "modern", {
    "R": "159:14", "c": "171:14", "S": "114:1", "k": "77:1", "i": "101",
}, [
    lay(".n.n.",
        ".#.#.",
        ".RRR.",
        ".#.#.",
        ".v.v."),
    lay(".....",
        ".c.c.",
        ".SRRk",
        ".c.c.",
        "....."),
    lay(".....",
        "...i.",
        "...i.",
        "...i.",
        "....."),
], origin=(1, 1))

prop("forklift", "Forklift", "modern", {
    "Y": "159:4", "i": "101", "T": "167:0", "A": "145:0", "S": "114:1", "f": "113",
    "U": "167:8", "V": "69:5",
}, [
    lay("#Y#iTT",
        "YYYi..",
        "#Y#iTT"),
    lay("Y.fi..",
        "ASVi..",
        "Y.fi.."),
    lay("f.fi..",
        "...i..",
        "f.fi.."),
    lay("UUUi..",
        "UUUi..",
        "UUUi.."),
])

prop("street-lamp", "Street lamp", "modern", {
    "w": "139", "b": "44:0", "L": "169",
}, [
    lay("w.."), lay("w.."), lay("w.."), lay("w.."), lay("w.L"), lay("wbb"),
])

prop("double-lamp", "Double street lamp", "modern", {
    "w": "139", "b": "44:0", "L": "169",
}, [
    lay("..w.."), lay("..w.."), lay("..w.."), lay("..w.."), lay("L.w.L"), lay("bbwbb"),
], origin=(2, 0))

prop("traffic-light", "Traffic light", "modern", {
    "w": "139", "G": "35:5", "Y": "35:4", "R": "35:14", "b": "44:0", "B": "35:15",
    "e": "77:1", "W": "77:2",
}, [
    lay("w"), lay("w"), lay("w"), lay("G"), lay("Y"), lay("R"), lay("b"),
])

prop("phone-box", "Phone box", "modern", {
    "R": "159:14", "o": "77:3", "G": "89", "n": "44:6", "S": "68:3",
}, [
    lay(".RRR.",
        ".|o|.",
        ".R.R.",
        "....."),
    lay(".RRR.",
        ".|.|.",
        ".R.R.",
        "....."),
    lay(".RRR.",
        ".RGR.",
        ".RRR.",
        "..S.."),
    lay(".nnn.",
        ".nnn.",
        ".nnn.",
        "....."),
], origin=(1, 0))

prop("fuel-pumps", "Fuel pumps", "modern", {
    "D": "43:8", "w": "139", "R": "159:14", "l": "69:4", "q": "155", "s": "68:3",
    "S": "68:2", "_": "44:7",
}, [
    lay(".....",
        "DDDDD",
        "....."),
    lay(".l.l.",
        "wR.Rw",
        "....."),
    lay(".S.S.",
        ".q.q.",
        ".s.s."),
    lay(".....",
        "._._.",
        "....."),
])

prop("bus-stop", "Bus stop", "modern", {
    "Q": "155:2", "S": "156:3", "_": "44:7", "w": "139", "B": "35:11",
    "s": "68:3", "N": "68:2",
}, [
    lay("Q||Q..",
        "|SS|..",
        "Q..Q..",
        "......"),
    lay("Q||Q..",
        "|..|..",
        "Q..Q.w",
        "......"),
    lay("____..",
        "____.N",
        "____.B",
        ".....s"),
], )

prop("park-bench", "Park bench", "modern", {
    "S": "134:2", "P": "68:4", "p": "68:5",
}, [
    lay("PSSSp"),
], origin=(1, 0))

prop("hydrant", "Hydrant and bins", "modern", {
    "R": "159:14", "w": "77:2", "e": "77:1", "c": "171:14", "K": "118:0", "H": "154:0",
}, [
    lay("wRe.KH"),
    lay(".c...."),
], origin=(1, 0))

prop("ice-cream", "Ice-cream cart", "modern", {
    "t": "44:15", "s": "68:2", "f": "85", "P": "35:6", "K": "118:0", "w": "35:0",
}, [
    lay("..#..",
        ".ttt.",
        "..#.."),
    lay(".s...",
        "fPKK.",
        "....."),
    lay(".....",
        ".f...",
        "....."),
    lay(".....",
        ".f...",
        "....."),
    lay("PwP..",
        "wPw..",
        "PwP.."),
    lay(".....",
        ".P...",
        "....."),
], origin=(1, 1))

# Village ---------------------------------------------------------------------------------------------------

prop("hand-cart", "Hand cart", "village", {
    "W": "17:9", "t": "126:9", "f": "188", "h": "170:0", "M": "103",
}, [
    lay(".W...",
        "ttt.f",
        "ttt..",
        "ttt.f",
        ".W..."),
    lay(".....",
        "fffff",
        "fhM..",
        "fffff",
        "....."),
])

prop("hay-wagon", "Hay wagon", "village", {
    "D": "162:9", "t": "126:13", "f": "188", "h": "170:4", "H": "170:0", "T": "50:5",
}, [
    lay(".D..D....",
        "tttttt...",
        "tttttt...",
        "tttttt...",
        ".D..D...."),
    lay(".........",
        "ffffff..f",
        "fhhhhffff",
        "ffffff..f",
        "........."),
    lay(".........",
        ".....T...",
        ".hhh.....",
        ".........",
        "........."),
    lay(".........",
        ".........",
        "..H......",
        ".........",
        "........."),
])


def stall(name, title, stripe):
    return prop(name, title, "village", {
        "f": "85", "h": "170:0", "K": "54:3", "C": "5:1", "s": "68:3", "k": "92",
        "M": "103", "p": "140", "r": stripe, "w": "35:0",
    }, [
        lay("....",
            "fhKf",
            "....",
            "fCCf",
            ".s.."),
        lay("....",
            "f..f",
            "....",
            "fkMf",
            "...."),
        lay("....",
            "f..f",
            "....",
            "f..f",
            "...."),
        lay("rwrw",
            "rwrw",
            "rwrw",
            "rwrw",
            "rwrw"),
        lay("....",
            "rwrw",
            "rwrw",
            "....",
            "...."),
    ], origin=(0, 1))


stall("stall-red", "Market stall", "35:14")
stall("stall-blue", "Market stall (blue)", "35:11")

prop("well", "Well", "village", {
    "c": "4", "C": "48", "W": "9", "w": "139:0", "m": "139:1", "f": "85",
    "S": "134:2", "s": "134:3", "P": "5:1", "b": "126:1", "K": "118:3",
}, [
    lay(".....",
        ".ccC.",
        ".cWc.",
        ".Ccc.",
        "....K"),
    lay(".....",
        ".wmw.",
        ".f.f.",
        ".mww.",
        "....."),
    lay(".....",
        ".....",
        ".f.f.",
        ".....",
        "....."),
    lay(".....",
        ".....",
        ".fff.",
        ".....",
        "....."),
    lay(".....",
        "SSSSS",
        "PPPPP",
        "sssss",
        "....."),
    lay(".....",
        ".....",
        ".bbb.",
        ".....",
        "....."),
], origin=(2, 2))

prop("lantern-post", "Lantern post", "village", {
    "B": "98", "F": "188", "G": "89", "b": "126:1",
}, [
    lay("B."), lay("F."), lay("F."), lay("FG"), lay("FF"), lay("b."),
])

prop("signpost", "Signpost", "village", {
    "L": "17:0", "f": "85", "E": "68:5", "W": "68:4", "N": "68:2", "S": "68:3",
}, [
    lay("...", ".L.", "..."),
    lay(".N.", ".L.", "..."),
    lay("...", "WLE", "..."),
    lay("...", ".L.", ".S."),
    lay("...", ".f.", "..."),
], origin=(1, 1))

prop("log-bench", "Log bench", "village", {
    "L": "17:0", "b": "126:0",
}, [
    lay("LbbL"),
])

prop("barrels", "Barrels and crates", "village", {
    "L": "17:0", "K": "54:3", "h": "170:0", "C": "118:0", "x": "58",
}, [
    lay("LLx",
        "LhK",
        ".C."),
    lay("L..",
        "...",
        "..."),
])

prop("scarecrow", "Scarecrow", "village", {
    "f": "85", "H": "170:0", "P": "86:0", "c": "171:12",
}, [
    lay(".f."), lay(".f."), lay("fHf"), lay(".P."), lay(".c."),
], origin=(1, 0))

prop("tractor", "Tractor", "village", {
    "g": "159:13", "F": "191", "H": "69:2", "S": "114:1", "k": "77:1", "f": "191",
    "c": "171:13", "L": "69:5", "x": "113",
}, [
    lay(".....n.",
        ".##..#.",
        ".ggggF.",
        ".##..#.",
        ".....v."),
    lay(".....n.",
        ".##....",
        "HgSgggk",
        ".##....",
        ".....v."),
    lay(".......",
        ".fc....",
        "...Lx..",
        ".fc....",
        "......."),
    lay(".......",
        ".f.....",
        ".f..x..",
        ".f.....",
        "......."),
], origin=(1, 1))

prop("mine-cart", "Mine cart and portal", "village", {
    "L": "17:1", "r": "66:1", "K": "118:0", "o": "16", "T": "50:2", "Z": "17:9",
    "b": "17:4", "X": "46", "C": "54:2",
}, [
    lay(".......L...",
        "brrrKKrrrrr",
        ".......L...",
        "..XC......."),
    lay(".......L...",
        "....oo.....",
        ".......L...",
        "..X........"),
    lay("......TL...",
        "...........",
        ".......L...",
        "..........."),
    lay(".......Z...",
        ".......Z...",
        ".......Z...",
        "..........."),
], origin=(1, 1))

prop("locomotive", "Tank locomotive", "village", {
    "N": "112", "n": "114:2", "s": "114:3", "B": "35:14", "k": "77:1", "g": "159:13",
    "d": "126:5", "H": "154:0", "S": "44:1", "r": "66:1", "L": "123", "o": "77:4",
}, [
    lay("...o.o.o....",
        "...#.#.#Bk..",
        "rrrNNNNNBrrr",
        "...#.#.#Bk..",
        "...v.v.v...."),
    lay("............",
        "...ggNNNN...",
        "...g.NNN#k..",
        "...ggNNNN...",
        "............"),
    lay("............",
        "...g|nnnn...",
        "...|.NNNL...",
        "...g|ssss...",
        "............"),
    lay("............",
        "...dd.......",
        "...dd.SH....",
        "...dd.......",
        "............"),
], origin=(3, 1))

# Water and air ----------------------------------------------------------------------------------------------

prop("rowboat", "Rowing boat", "harbour", {
    "P": "5:0", "b": "126:0", "S": "53:0", "f": "85",
}, [
    lay(".PPP.",
        "PPPPP",
        ".PPP."),
    lay(".bbb.",
        "b.b.S",
        ".bbb."),
], origin=(0, 1))

prop("canoe", "Canoe", "harbour", {
    "P": "5:1", "b": "126:1", "H": "134:1", "E": "134:0",
}, [
    lay(".PPPP."),
    lay("Hb..bE"),
])

prop("fishing-boat", "Fishing boat", "harbour", {
    "S": "134:6", "s": "134:7", "a": "134:4", "B": "134:5", "P": "5:1", "f": "188",
    "q": "155", "L": "69:5", "K": "54:5", "C": "118:3", "W": "30", "_": "44:7",
    "D": "151",
}, [
    lay("..PPPP...",
        ".PPPPPP..",
        ".PPPPPPP.",
        ".PPPPPP..",
        "..PPPP..."),
    lay(".SSSSSS..",
        "aPPPPPPS.",
        "aPPPPPPPB",
        "aPPPPPPs.",
        ".ssssss.."),
    lay(".ffffff..",
        "fqqq...f.",
        "f.Lq.KC.f",
        "fqqq..Wf.",
        ".ffffff.."),
    lay(".........",
        "fq|q.....",
        ".q.|.....",
        ".q|q.....",
        "........."),
    lay(".........",
        ".____....",
        ".____....",
        ".____....",
        "........."),
    lay(".........",
        ".........",
        "..fD.....",
        ".........",
        "........."),
    lay(".........",
        ".........",
        "..f......",
        ".........",
        "........."),
    lay(".........",
        ".........",
        "..f......",
        ".........",
        "........."),
], origin=(0, 2))

prop("crates", "Dock cargo", "harbour", {
    "L": "17:0", "K": "54:2", "h": "170:4", "x": "58", "W": "30",
}, [
    lay("xLL",
        "hhK"),
    lay("x..",
        "..."),
])

prop("airplane", "Propeller plane", "air", {
    "q": "155", "R": "159:14", "_": "44:7", "^": "44:15", "S": "156:1", "g": "95:3",
    "i": "101", "N": "44:14", "f": "85",
}, [
    lay("........",
        "........",
        ".....#..",
        "f.......",
        ".....#..",
        "........",
        "........"),
    lay("...NN...",
        "...^^..i",
        "^..^^..i",
        "qqqqqqRi",
        "^..^^..i",
        "...^^..i",
        "...NN..."),
    lay("........",
        "........",
        "........",
        "q__Sg__.",
        "........",
        "........",
        "........"),
    lay("........",
        "........",
        "........",
        "R.......",
        "........",
        "........",
        "........"),
], origin=(0, 3))

prop("balloon", "Hot-air balloon", "air", {
    "h": "170:0", "f": "85", "K": "118:0", "r": "35:14", "y": "35:4",
}, [
    lay(".....", ".hhh.", ".h.h.", ".hhh.", "....."),
    lay(".....", ".f.f.", ".....", ".f.f.", "....."),
    lay(".....", ".f.f.", ".....", ".f.f.", "....."),
    lay(".....", ".f.f.", "..K..", ".f.f.", "....."),
    lay(".....", ".ryr.", ".ryr.", ".ryr.", "....."),
    lay(".ryr.", "ryryr", "ryryr", "ryryr", ".ryr."),
    lay(".ryr.", "ryryr", "ryryr", "ryryr", ".ryr."),
    lay(".ryr.", "ryryr", "ryryr", "ryryr", ".ryr."),
    lay(".....", ".ryr.", ".ryr.", ".ryr.", "....."),
    lay(".....", ".....", "..y..", ".....", "....."),
], origin=(2, 2))

# More ---------------------------------------------------------------------------------------------------------

prop("pickup", "Pickup truck", "modern", {
    "t": "44:8", "T": "159:14", "B": "35:11", "L": "155:1", "k": "77:1", "P": "68:4",
    "i": "101", "h": "170:4", "S": "114:1", "c": "171:11",
}, [
    lay("..n...n..",
        ".t#ttt#t.",
        ".ttttttt.",
        ".t#ttt#t.",
        "..v...v.."),
    lay(".........",
        ".TBBBBBLk",
        "PBBBBBBi.",
        ".TBBBBBLk",
        "........."),
    lay(".........",
        ".BBB||cc.",
        ".Bh.S|cc.",
        ".BBB||cc.",
        "........."),
    lay(".........",
        "....cc...",
        "....cc...",
        "....cc...",
        "........."),
], origin=(1, 1))

prop("scooter", "Scooter", "modern", {
    "b": "44:0", "S": "114:1", "R": "159:14", "i": "101", "k": "77:1",
}, [
    lay("#b#."),
    lay("S.Rk"),
    lay("..i."),
])

prop("vending", "Vending machine", "modern", {
    "R": "159:14", "L": "169", "v": "77:3", "b": "44:0",
}, [
    lay("RR", ".."),
    lay("LR", ".v"),
    lay("bb", ".."),
])

prop("sailboat", "Sailing dinghy", "harbour", {
    "q": "155", "_": "44:7", "S": "156:0", "f": "188", "W": "35:0", "R": "35:14",
}, [
    lay(".qqqq.",
        "qqqqqq",
        ".qqqq."),
    lay(".____.",
        "_..f.S",
        ".____."),
    lay("......",
        ".WWfW.",
        "......"),
    lay("......",
        "..WfW.",
        "......"),
    lay("......",
        "..Wf..",
        "......"),
    lay("......",
        "...f..",
        "......"),
    lay("......",
        "..Rf..",
        "......"),
], origin=(0, 1))

prop("wheelbarrow", "Wheelbarrow", "village", {
    "f": "85", "t": "126:8", "W": "17:9", "D": "3:1",
}, [
    lay("ftt.",
        ".ttW",
        "ftt."),
    lay("fff.",
        ".DDf",
        "fff."),
], origin=(0, 1))

prop("cannon", "Cannon", "village", {
    "W": "17:9", "p": "126:9", "C": "173", "D": "23:5", "l": "69:2",
}, [
    lay(".W.W.",
        "pppp.",
        ".W.W."),
    lay(".....",
        "lCCCD",
        "....."),
], origin=(0, 1))

prop("picnic-table", "Picnic table", "village", {
    "b": "126:1", "t": "126:8", "p": "140", "k": "92",
}, [
    lay("bbb", "ttt", "bbb"),
    lay("...", "pk.", "..."),
])

prop("tent", "Tent", "village", {
    "W": "35:13", "f": "85",
}, [
    lay("WWWW", "W...", "WWWW"),
    lay("....", "WWWW", "...."),
])

prop("campfire", "Campfire", "village", {
    "X": "17:4", "Z": "17:8", "N": "87", "F": "51",
}, [
    lay(".Z.", "XNX", ".Z."),
    lay("...", ".F.", "..."),
], origin=(1, 1))
