"""Where the houses stand: (key, x, z, heading, L, W, storeys, style, door side, name), red's half. The ground is levelled under each
by land.py, so a house is seated on made ground and not buried in a slope."""

# (key, x, z, heading, L, W, storeys, style, door side, name)
HOUSES = [
    ("lodge", 0, -87, 0, 16, 8, 2, "hearth", 1, "Hearth Lodge"),
    ("woodshed", -13, -82, 90, 8, 5, 1, "hearth", 1, "the Woodshed"),
    ("stable", 13, -81, 90, 9, 6, 1, "hearth", -1, "the Stable"),
    ("bakehouse", -10, -61, 0, 9, 6, 2, "maple", 1, "the Bakehouse"),
    ("press", 12, -58, 0, 10, 7, 2, "maple", 1, "the Cider Press"),
    ("chapel", -11, -43, 0, 10, 7, 2, "pine", 1, "the Chapel"),
    ("hawthorn", 14, -43, 0, 8, 6, 2, "maple", -1, "Hawthorn Cottage"),
    ("mill", -13, -27, 0, 11, 7, 2, "hearth", 1, "the Mill Barn"),
    ("pinewatch", -26, -71, 0, 9, 6, 2, "pine", 1, "Pinewatch"),
    ("foundry", 40, -77, 0, 10, 7, 2, "forge", 1, "the Foundry"),
    ("armoury", 27, -70, 0, 8, 6, 2, "forge", 1, "the Armoury"),
    ("slagstore", 49, -47, 90, 8, 6, 1, "forge", 1, "the Slag Store"),
]
