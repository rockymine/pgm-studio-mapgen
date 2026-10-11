"""Write Tidewell Canals' map.xml: teams of sixteen, their spawns, the three hills (the Campo worth two a second,
each fish market one), a score limit and a time limit, the kit; no building, the lagoon kills.

    python3 mapxml.py > map.xml
"""
import plan as P
import common as C
from pgmvox.play.rules import Build, Map, Match, terrain_of
from pgmvox.play.objectives import Hill

O = P.objectives()
for h in O.of(Hill):                               # the progress shows on the pad's clay ring, the owner on the pad
    h.progress = P.pad_ring(h.pad, 1)
M = Map("Tidewell Canals", "1.0.0", "Hold the markets: the Campo is worth two points a second, each fish market one.",
        "koth",
        terrain=terrain_of(__file__),
        authors=["Claude (pgmvox trial)"],
        objectives=O,
        kit=C.kit(wood=0),
        build=Build(never=True, message="The quarter is not yours to build on!"),
        match=Match(score=1000, time=15 * 60))
print(M.xml())
