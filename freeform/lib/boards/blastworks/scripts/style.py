"""Style 4, worked on: polished diorite and stone brick under a spruce rim, a cyan band a storey, spruce posts, and
quartz for the details: the sills under the windows, the posts' heads under the rim, the pillars' capitals and
finials, the house's cornice. No glowstone, no iron block, gravel nowhere."""
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

DIORITE, DIORITE_RAW, SBRICK = (B.STONE, 4), (B.STONE, 3), (B.STONEBRICK, 0)
SPRUCE, SPRUCE_LOG, CYAN = (B.PLANKS, 1), (B.LOG, 1), (B.STAINED_CLAY, 9)
QUARTZ, CHISELED, QPILLAR = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2)
SILL = (B.SLAB, 15)                                  # a quartz slab in the upper half
PANE = (B.PANE, 0)


def rim(inward):
    return B.SPRUCE_STAIRS, stair(inward, upside_down=True)


def style():
    def body(w, x, z, h):
        for y in range(1, h):
            w.set(x, y, z, *(SBRICK if y < 3 else CYAN if (h - y) % 6 == 4 else DIORITE))
        w.set(x, 0, z, 36)
    pane = G.Course(PANE, back=SPRUCE)
    plain = [rim, SPRUCE, DIORITE, DIORITE, CYAN, DIORITE, DIORITE, DIORITE, DIORITE, DIORITE, CYAN]
    post = [rim, CHISELED] + [SPRUCE_LOG] * 8 + [QUARTZ]
    window = [rim, SPRUCE, QUARTZ, pane, pane, SILL, DIORITE, DIORITE, DIORITE, DIORITE, CYAN]
    edge = G.Face(plain, G.Accent(5, frame=post, inner=window, every=2, min_air=7), floor=1)
    low = G.Face([rim, SPRUCE, DIORITE], floor=1)               # where a piece stands too low for the storey
    fills = {
        "deck": marks.field(lambda c: DIORITE_RAW if ((c.x - c.x0) // 3 + (c.z - c.z0) // 3) % 2 else DIORITE,
                            name="deck"),
        "lanes": marks.field(lambda c: SBRICK if (c.z - c.z0 if c.hw >= c.hh else c.x - c.x0) % 4 == 0 else DIORITE,
                             name="lanes"),
        "plain": marks.field(lambda c: QUARTZ if c.edge < 1 else DIORITE, name="plain"),
        "flight": marks.flight(DIORITE, B.SPRUCE_STAIRS),
    }
    return G.Style("diorite-spruce", body=body, faces={"edge": edge, "low": low}, seam=SPRUCE, fills=fills,
                   choose=lambda sec, lot: ["deck"], params={})


CAP = {(0, 0): (1, 0), (1, 0): (0, 1), (1, 1): (-1, 0), (0, 1): (0, -1)}   # a pinwheel: each rises to the next


def pillar(w, x, z, floor, h=7):
    """Two by two: a stone-brick base, a diorite shaft with a cyan band, a quartz necking, a chiseled quartz
    capital, and a cap of four quartz stairs, each rising to the middle, so they close into one."""
    for dx in (0, 1):
        for dz in (0, 1):
            X, Z = x + dx, z + dz
            w.set(X, floor + 1, Z, *SBRICK)
            for y in range(floor + 2, floor + h - 2):
                w.set(X, y, Z, *(CYAN if y == floor + 3 else DIORITE))
            w.set(X, floor + h - 2, Z, *QUARTZ)
            w.set(X, floor + h - 1, Z, *CHISELED)
            w.set(X, floor + h, Z, B.QUARTZ_STAIRS, stair(CAP[(dx, dz)]))


def house(w, x0, z0, x1, z1, floor, door=("s",)):
    """A flat-roofed house: spruce posts at its corners and every fourth block, diorite walls, windows with quartz
    lintels and sills, a quartz cornice and a spruce rim round a roof of spruce planks."""
    hgt = 5
    mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(floor + 1, floor + hgt + 1):
                if not edge:
                    w.set(x, y, z, B.AIR)
                    continue
                corner = x in (x0, x1) and z in (z0, z1)
                along = (x - x0) if z in (z0, z1) else (z - z0)
                if corner or along % 4 == 0:
                    w.set(x, y, z, *SPRUCE_LOG)
                elif y == floor + hgt:
                    w.set(x, y, z, *QUARTZ)                      # the cornice
                elif along % 4 == 2 and y in (floor + 2, floor + 3):
                    w.set(x, y, z, *PANE)
                elif along % 4 == 2 and y == floor + 4:
                    w.set(x, y, z, *QUARTZ)                      # the lintel
                elif along % 4 == 2 and y == floor + 1:
                    w.set(x, y, z, *SILL)
                else:
                    w.set(x, y, z, *DIORITE)
            w.set(x, floor + hgt + 1, z, *(SPRUCE if not edge else (B.SPRUCE_STAIRS, stair(
                ((1 if x == x0 else -1 if x == x1 else 0), (1 if z == z0 else -1 if z == z1 else 0))
                if not (x in (x0, x1) and z in (z0, z1)) else (1 if x == x0 else -1, 0), upside_down=False))))
    if "s" in door:
        for x in (mx, mx + 1):
            for y in (floor + 1, floor + 2, floor + 3):
                w.set(x, y, z1, B.AIR)
            w.set(x, floor + 4, z1, *CHISELED)
