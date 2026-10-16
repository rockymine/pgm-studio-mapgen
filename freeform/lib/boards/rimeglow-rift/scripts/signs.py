"""Signposts at the places a player has to choose: written once for the north half and turned for the south, each half's
text in its own names."""
from pgmvox import B
from stamp import Stamp

# (x, z, rotation, north lines, south lines)
POSTS = [
    (17, -61, 8, ["Hearth Court", "Rimewatch >", "Meltgate v", "< Hoarwood"],
     ["Hearth Court", "Emberwatch >", "Meltgate v", "< Amberwood"]),
    (24, -47, 12, ["Frostmere", "< Meltgate", "Rimewatch >", ""],
     ["Cinder Mere", "< Meltgate", "Emberwatch >", ""]),
    (-4, -26, 8, ["Meltgate", "Causeway", "Hoarspan <", "Kindlespan >"],
     ["Meltgate", "Causeway", "Hoarspan <", "Kindlespan >"]),
    (-35, -29, 8, ["Hoarspan", "bridge", "Low road v", "Hoarwood ^"],
     ["Kindlespan", "bridge", "Low road v", "Amberwood ^"]),
    (35, -29, 8, ["Kindlespan", "bridge", "Low road v", "Rimewatch ^"],
     ["Hoarspan", "bridge", "Low road v", "Emberwatch ^"]),
    (39, -61, 4, ["Rimewatch", "the Core", "held over", "its pit"],
     ["Emberwatch", "the Core", "held over", "its pit"]),
    (-37, -66, 8, ["Hoarwood", "Woodcutters'", "Rest", ""],
     ["Amberwood", "Orchard", "Keeper's", "Cabin"]),
]


def build(w, H):
    n = 0
    for x, z, rot, north, south in POSTS:
        for isS, lines in ((False, north), (True, south)):
            S = Stamp(w, isS)
            px, pz = S.xz(x, z)
            g = w.top(px, pz)
            if g <= 0 or w.id(px, g + 1, pz) not in (0, B.SNOW_LAYER, B.TALLGRASS, B.CARPET) \
                    or w.id(px, g, pz) in (B.LEAVES, B.LEAVES2):
                continue
            w.set(px, g + 1, pz, B.AIR)
            w.sign(px, g + 1, pz, lines, rot=(rot + (8 if isS else 0)) % 16)
            n += 1
    return n
