"""Riftwater's plan: every place, route and height the generator builds from, written for the red (west)
half. The blue half is its mirror image across the rift, x' = -1 - x, so one statement serves both teams.

Coordinates are world x, z (north is -z). Heights are the ground a player stands on.
"""

# The board and the rift between the teams.
X_MIN, X_MAX = -120, 119
Z_MIN, Z_MAX = -88, 87
RIFT_HALF = 10            # void for x in [-10, 9]: the build zone that joins the teams
BANK_X = -11              # the last land column on red's side, give or take the edge noise


def mirror_x(x):
    return -1 - x


# ---- Places (red half). Each: name, kind, where, why a player goes there, how they get there. --------
PLACES = [
    dict(key="spawn", name="The Watch House", at=(-99, -7), r=7,
         what="Red's spawn: a stone watch house with a timber upper storey, seated on a terrace cut into the ridge",
         why="spawn; looks down the valley at the falls and both monuments",
         how="terrace steps east to Spawn Lane; Spring Path south; Forest Path north; mine adit beside it"),
    dict(key="ridge", name="The Ridge", poly=[(-120, -88), (-100, -88), (-96, -60), (-104, -30), (-103, -18),
                                               (-106, 10), (-100, 40), (-104, 87), (-120, 87)],
         what="the back of the board: a forested ridge with two spurs, 14-22 blocks over the spawn",
         why="frames the spawn; its spurs carry the woods", how="climbed from the woods' paths"),
    dict(key="north_wood", name="North Wood", poly=[(-120, -88), (-74, -88), (-74, -74), (-82, -52), (-90, -30),
                                                    (-104, -20), (-120, -24)],
         what="oak and birch wood on the north spur", why="cover onto the north monument's flank; the hut's chest",
         how="Forest Path from the spawn terrace"),
    dict(key="hut", name="Woodcutter's Hut", at=(-104, -64), r=4,
         what="a one-room log hut at the end of the forest path, with a chest, a chopping block and a woodpile",
         why="supplies; the path's end", how="Forest Path"),
    dict(key="square", name="Market Square", at=(-66, -44), r=10,
         what="the town's paved square, the north monument standing open in it, the town hall on its north side",
         why="RED NORTH MONUMENT", how="Main Street from the rift; Spawn Lane north fork; the cellar under the hall"),
    dict(key="town", name="Market Town", poly=[(-76, -88), (-12, -88), (-12, -18), (-30, -14), (-52, -14),
                                               (-56, -26), (-74, -30)],
         what="a brick-and-timber market town on a bluff over the river: two streets, a chapel with a tower, an inn",
         why="the north approach is fought through it street by street; the chapel tower overlooks the square",
         how="Old Bridge at the rift, Bridge Street from the stone bridge, the square from the spawn"),
    dict(key="old_bridge", name="The Old Bridge", at=(-10, -44), r=4,
         what="a stone bridge across the rift that broke in the middle: two stubs, ten blocks of air between",
         why="the shortest crossing, straight into the town", how="Main Street"),
    dict(key="chapel", name="The Chapel", at=(-44, -68), r=6,
         what="a stone chapel with a belfry tower", why="the highest point in town: a perch over the square",
         how="North Lane; a ladder up the tower"),
    dict(key="inn", name="The Falls Inn", at=(-30, -22), r=5,
         what="the inn at the town end of the stone bridge", why="cover at the bridgehead", how="Bridge Street"),
    dict(key="cellar", name="The Gaol Cellar", at=(-56, -30), r=4,
         what="a dungeon of cells under the old gaol house, its back wall broken into the cave",
         why="the cave's way up into the town, eighteen blocks from the north monument", how="the cave; the gaol's stair"),
    dict(key="river", name="Red River", line=[(-74, 22), (-66, 17), (-56, 13), (-46, 7), (-36, 3), (-26, 1),
                                              (-17, 0), (-11, 0)],
         what="the river from the mill pond to the falls, sunk between a town bluff and a field bank",
         why="a low covered route from the falls to the bridge; swimming it is slow", how="its banks and fords"),
    dict(key="pond", name="Mill Pond", at=(-84, 20), r=12,
         what="the pond the river rises in, fed by a spring falling off the ridge, with a jetty and a rowboat",
         why="frames the spawn; the jetty is a vantage; the footbridge at its outlet is the quick way south",
         how="Spring Path; the outlet footbridge"),
    dict(key="mill", name="The Mill", at=(-62, 9), r=5,
         what="a watermill with a wheel turning in the race beside the weir", why="the weir is a crossing",
         how="Mill Lane along the north bank"),
    dict(key="stone_bridge", name="Stone Bridge", at=(-36, 3), r=4,
         what="a three-arch stone bridge carrying the road from the town to the fields", why="the chokepoint between the two monuments",
         how="Bridge Street, Field Road"),
    dict(key="falls", name="The Falls", at=(-12, 0), r=5,
         what="the river pours over the rift's lip into the void, facing blue's falls across the gap",
         why="the middle crossing; behind the water, the cave mouth", how="the riverbanks; the Falls Walk"),
    dict(key="cave", name="Falls Cave", line=[(-12, 0), (-24, 4), (-38, 10), (-50, 20), (-52, 38)],
         what="a water-cut cave behind the falls: a long gallery under the river, a lake chamber, three ways up",
         why="the approach from below: to the sinkhole by the south monument, to the gaol cellar, to the mine",
         how="its mouth in the rift face behind the waterfall"),
    dict(key="village", name="Ironhollow", poly=[(-100, 36), (-72, 36), (-72, 82), (-100, 82)],
         what="a mining village: cottages on paths, a smithy, a well, the headframe over the mine shaft, a spoil heap",
         why="cover behind the south monument; the shaft is the mine's way up", how="Spring Path, Village Road"),
    dict(key="headframe", name="The Headframe", at=(-84, 56), r=4,
         what="a timber tower over the shaft with its winding wheel", why="height over the fields; the shaft ladder",
         how="Ironhollow's lanes"),
    dict(key="green", name="Winding Green", at=(-66, 48), r=8,
         what="open grass at the village's edge where the ore carts turn, the south monument standing on it",
         why="RED SOUTH MONUMENT", how="Village Road, the outlet footbridge, the mine shaft"),
    dict(key="mine", name="Ironhollow Mine", line=[(-102, 2), (-98, 20), (-90, 40), (-84, 56), (-72, 50), (-58, 38)],
         what="timbered galleries from an adit by the spawn to the shaft under the headframe and on to where the miners broke into the cave",
         why="the defenders' covered way to the south monument, and the cave's way to the spawn",
         how="the adit, the shaft, the breakthrough"),
    dict(key="fields", name="The Fields", poly=[(-62, 26), (-14, 22), (-12, 87), (-66, 87)],
         what="wheat in strips with a scarecrow, a hay cart, a barn, hedgerows", why="open ground in front of the south monument",
         how="Field Road; the south rift crossing"),
    dict(key="sinkhole", name="The Sinkhole", at=(-50, 40), r=4,
         what="a collapse in the field where the cave roof fell in", why="the cave's way up, 16 blocks from the south monument",
         how="the cave"),
    dict(key="knoll", name="Lone Oak Knoll", at=(-22, 74), r=7,
         what="a grassy knoll by the rift with one big oak", why="the south crossing's lookout", how="the fields"),
    dict(key="clearing", name="The Cutting", at=(-110, 68), r=7,
         what="a clearing of stumps and log piles where the south wood was felled for pit props, a timber sledge",
         why="frames the village; the log piles are a climb onto the ridge", how="Clearing Path from Ironhollow"),
]

# The objectives (red's; blue's mirror them). Monument blocks stand 2 over the ground.
MONUMENTS = {"north": (-66, -44), "south": (-66, 48)}
SPAWN = (-99, -7)

# Routes: polylines a player walks. kind: street (hard), lane (soft), path (forest), plank (bridge)
ROUTES = [
    dict(name="Spawn Lane", kind="lane", pts=[(-92, -7), (-84, -7), (-78, -12), (-74, -24), (-72, -36)]),
    dict(name="Spawn Lane south", kind="lane", pts=[(-78, -12), (-74, 0), (-71, 12), (-70, 22), (-70, 34), (-68, 40)]),
    dict(name="Main Street", kind="street", pts=[(-56, -44), (-44, -45), (-32, -43), (-20, -44), (-12, -44)]),
    dict(name="Bridge Street", kind="street", pts=[(-42, -44), (-40, -32), (-36, -20), (-36, -8)]),
    dict(name="North Lane", kind="street", pts=[(-62, -56), (-52, -62), (-40, -66), (-26, -64), (-16, -70)]),
    dict(name="Mill Lane", kind="lane", pts=[(-38, -10), (-48, -4), (-56, 0), (-62, 4)]),
    dict(name="Field Road", kind="lane", pts=[(-36, 12), (-40, 22), (-46, 30), (-56, 40), (-61, 46)]),
    dict(name="Farm Track", kind="lane", pts=[(-61, 52), (-58, 60), (-56, 66), (-46, 79), (-34, 80), (-24, 76)]),
    dict(name="Falls Walk", kind="lane", pts=[(-34, 12), (-26, 11), (-18, 9), (-14, 7)]),
    dict(name="Spring Path", kind="lane", pts=[(-96, 0), (-100, 12), (-99, 28), (-94, 38), (-88, 44)]),
    dict(name="Village Road", kind="lane", pts=[(-88, 44), (-80, 46), (-72, 47), (-62, 48)]),
    dict(name="Forest Path", kind="path", pts=[(-90, -14), (-88, -26), (-94, -40), (-96, -52), (-102, -60)]),
    dict(name="Clearing Path", kind="path", pts=[(-96, 66), (-102, 68), (-108, 68)]),
]
