"""Recovering the buildings Grok placed.

Two different recoveries, and the difference matters.

The SPAWN and WOOL buildings are not a recovery at all — they are what he said. THEME.md assigns
`ridge-hall` to the spawn ("intended as the main spawn structure sitting on the crest") and `wool-shelter`
to the wool rooms ("sits over / beside the wool rooms as light cover"), and his props place exactly those
styles at exactly those pieces. The studio has a first-class key for that pair — `roomStyles: {spawn, cage}`
on the layout — and a bound room's footprint comes from the plan piece it sits on rather than from the prop
cap, so the assignment he stated goes straight in.

The FREE-STANDING houses need one interpretation, and it is stated rather than hidden. Every house rect is
in plan cells, so its ×5 centre is where he put it — all ten land on the piece their id names, which is what
proves the unit. Read ×5 the extent is a stadium (60×25 blocks, against a 192-block² cap). So the placement
is taken from the cell reading and the extent from the numbers as written: a 12×5 hall, centred where he
drew it. Every number is his; only the axis each is read on differs.
"""

CELL = 5

# THEME.md §"House styles", verbatim in intent: which style is the spawn building and which the wool one.
ROOM_STYLES = {
    'grok-ridge':       {'spawn': 'ridge-hall', 'cage': 'wool-shelter'},
    'sandscar':         {'spawn': 'desert-hall'},
    'sandscar-complex': {'spawn': 'desert-hall'},
}


def wings(points):
    """Centre from the cell reading, extent from the numbers as written."""
    (x0, z0), (x1, z1) = points
    cx, cz = (x0 + x1) / 2 * CELL, (z0 + z1) / 2 * CELL
    w, h = abs(x1 - x0), abs(z1 - z0)
    return [[[round(cx - w / 2), round(cz - h / 2)], [round(cx + w / 2), round(cz + h / 2)]]]
