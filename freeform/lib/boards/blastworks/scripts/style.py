"""Style 4, worked on: polished diorite and stone brick under a spruce rim, a cyan band a storey, spruce posts, and
quartz for the details: the sills under the windows, the posts' heads under the rim, the pillars' capitals and
finials. No glowstone, no iron block, gravel nowhere."""
from pgmvox.core.blocks import B
from pgmvox.core.orient import stair
from pgmvox.grammar import marks
from pgmvox.grammar import rules as G

DIORITE, DIORITE_RAW, SBRICK = (B.STONE, 4), (B.STONE, 3), (B.STONEBRICK, 0)
SPRUCE, SPRUCE_LOG, CYAN = (B.PLANKS, 1), (B.LOG, 1), (B.STAINED_CLAY, 9)
QUARTZ, CHISELED, QPILLAR = (B.QUARTZ, 0), (B.QUARTZ, 1), (B.QUARTZ, 2)
SILL = (B.SLAB, 15)                                  # a quartz slab in the upper half
BARS = (B.IRON_BARS, 0)


def rim(inward):
    return B.SPRUCE_STAIRS, stair(inward, upside_down=True)


def style():
    def body(w, x, z, h):
        for y in range(1, h):
            w.set(x, y, z, *(SBRICK if y < 3 else CYAN if (h - y) % 6 == 4 else DIORITE))
        w.set(x, 0, z, B.BEDROCK)                        # the concept's floor
    pane = G.Course(BARS, back=SPRUCE)
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
