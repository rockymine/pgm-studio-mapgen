"""Write Rimeglow Rift's map.xml."""
from plan import KILL_Y, kit, objectives
from pgmvox.play.rules import Build, KillHeight, Map, Match, terrain_of

M = Map("Rimeglow Rift", "1.0.0", "Break the enemy's core, held over its pit on the far butte.", "dtc",
        authors=["Claude (pgmvox)"],
        rules=["Break the enemy core: it is held over a pit, and the lava must run.",
               "Three crossings span the rift; the ledges along the lava are a fourth way, on foot.",
               "The lava is lava. Build over it if you must."], terrain=terrain_of(__file__), objectives=objectives(), kit=kit(),
        build=Build(max_height=104), kill=KillHeight(KILL_Y), match=Match(time="40m", result="objectives"))
print(M.xml())
