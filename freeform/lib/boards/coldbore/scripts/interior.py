"""The station's rooms dressed with depth: every wall a skirting, pilasters with chiseled bases and capitals, panels
set back between them and a frieze under the ceiling; every door framed by jambs and a lintel; beams of cobblestone
wall carried across the ceiling from pilaster to pilaster, so a room is gridded and a corridor ribbed; a floor of
two-block tiles inside a border. Each room takes its own style, so the entrance hall, the spawn, the workshop, the
generator house and the vault read as different places.

A recess is cut only where rock stands behind it, so no panel opens into a neighbour. The reactor hall keeps its own
dressing, which `bunker.reactor` lays.
"""
from dataclasses import dataclass

import plan as P
from pgmvox import B

STONE, ANDESITE, POLISHED = (B.STONE, 0), (B.STONE, 5), (B.STONE, 6)
BRICK, CHISELED, CRACKED = (B.STONEBRICK, 0), (B.STONEBRICK, 3), (B.STONEBRICK, 2)
TEAM = (B.STAINED_CLAY, 14)                                                 # red; blue's image recolours it
HAZARD = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)]


@dataclass(frozen=True)
class Style:
    """How a room's walls, ceiling and floor are dressed. `panel` is the block set back in each bay (None keeps the
    bay flush), `frieze` the course under the capitals (`frieze_inset` sets it back), `beams` the ceiling's beam
    block and `grid` whether beams run both ways or only across the room's long walls."""
    period: int = 4
    body: tuple = BRICK
    cap: tuple = CHISELED
    base: tuple = POLISHED
    skirt: tuple = POLISHED
    face: tuple = STONE
    frame: tuple = BRICK
    panel: tuple = None
    frieze: tuple = BRICK
    frieze_inset: bool = False
    pipe: tuple = None
    light: tuple = None
    beams: tuple = (B.COBBLE_WALL, 0)
    beam_x: tuple = None
    beam_z: tuple = None
    grid: bool = True
    border: tuple = POLISHED
    lintel: tuple = POLISHED


HALL = Style(panel=(B.NETHER_BRICK, 0), frieze=TEAM, frieze_inset=True, period=5)
VESTIBULE = Style(panel=ANDESITE, frieze=TEAM, frieze_inset=True)
ROOM = Style(panel=ANDESITE)
SPAWN = Style(panel=POLISHED, face=BRICK, frieze=TEAM, frieze_inset=True)
WORKSHOP = Style(panel=(B.COBBLE, 0), face=BRICK, frieze=CRACKED)
ARMOURY = Style(panel=(B.PLANKS, 1), frieze=(B.LOG, 1 | 4))
GENERATORS = Style(panel=POLISHED, pipe=(B.COBBLE_WALL, 0), frieze=(B.IRON_BLOCK, 0), period=5)
CORRIDOR = Style(grid=False, border=None)
SERVICE = Style(grid=False, border=None, frieze=HAZARD[0], frieze_inset=True)
VAULT = Style(period=4, body=(B.QUARTZ, 2), cap=(B.QUARTZ, 1), base=(B.QUARTZ, 1), skirt=(B.QUARTZ, 1),
              face=(B.QUARTZ, 0), frame=(B.QUARTZ, 0), panel=(B.STONE, 4), frieze=(B.QUARTZ, 1),
              light=(B.SEA_LANTERN, 0), beams=None, beam_x=(B.QUARTZ, 4), beam_z=(B.QUARTZ, 3),
              border=(B.QUARTZ, 1), lintel=(B.QUARTZ, 1))

STYLES = {
    "gate vestibule": VESTIBULE, "entrance hall": HALL, "armoury": ARMOURY, "west corridor": CORRIDOR,
    "spawn room": SPAWN, "iron room": WORKSHOP, "generator house": GENERATORS, "annex corridor": CORRIDOR,
    "annex link": CORRIDOR, "south corridor": SERVICE, "store passage": SERVICE, "service corridor": SERVICE,
    "vault passage": SERVICE, "vault": VAULT,
}


def walls(s):
    """The four walls round a space: (cells along the wall, the way out of the room, beams' axis from them)."""
    return [([(x, s.z0 - 1) for x in range(s.x0, s.x1 + 1)], (0, -1), "z"),
            ([(x, s.z1 + 1) for x in range(s.x0, s.x1 + 1)], (0, 1), "z"),
            ([(s.x0 - 1, z) for z in range(s.z0, s.z1 + 1)], (-1, 0), "x"),
            ([(s.x1 + 1, z) for z in range(s.z0, s.z1 + 1)], (1, 0), "x")]


def solid(w, x, y, z):
    return w.id(x, y, z) not in (B.AIR, B.WATER, B.LAVA)


KEEP = {B.BEDROCK, B.IRON_BLOCK, B.LADDER}                                 # doors and fittings stay


def dress(w, s, st):
    """Dress one space's walls, ceiling and floor in its style."""
    h, top = s.h, s.feet + s.h - 1
    long_run = max(s.x1 - s.x0, s.z1 - s.z0) + 1
    for cells, (ox, oz), axis in walls(s):
        run = len(cells)
        pilasters = {i for i in range(run) if i % st.period == st.period - 1 and i < run - 1}
        beams = st.grid or run == long_run
        opening = {(j, t) for j, (x, z) in enumerate(cells) for t in range(-1, h) if not solid(w, x, s.feet + t, z)}
        for i, (x, z) in enumerate(cells):
            for t in range(h):
                y = s.feet + t
                if (i, t) in opening or w.id(x, y, z) in KEEP:
                    continue
                bx, bz = x + ox, z + oz                                  # the block behind the face
                door_side = (i - 1, t) in opening or (i + 1, t) in opening
                door_over = t > 0 and (i, t - 1) in opening
                if door_over:
                    w.set(x, y, z, *st.lintel)
                elif i in pilasters or door_side:
                    w.set(x, y, z, *(st.base if t == 0 else st.cap if t >= h - 2 else st.body))
                elif t == 0:
                    w.set(x, y, z, *st.skirt)
                elif t == h - 2:
                    if st.frieze_inset and solid(w, bx, y, bz):
                        w.set(x, y, z, B.AIR)
                        w.set(bx, y, bz, *(HAZARD[(i // 2) % 2] if st.frieze == HAZARD[0] else st.frieze))
                    else:
                        w.set(x, y, z, *st.frieze)
                elif st.panel and 2 <= t <= h - 4 and solid(w, bx, y, bz):
                    middle = i % st.period == st.period // 2 - 1
                    w.set(bx, y, bz, *st.panel)
                    if st.pipe and middle:
                        w.set(x, y, z, *st.pipe)
                    elif st.light and middle and t == (h - 2) // 2 and (i // st.period) % 2 == 0:
                        w.set(bx, y, bz, *st.light)
                        w.set(x, y, z, B.AIR)
                    else:
                        w.set(x, y, z, B.AIR)
                elif st.panel and t in (1, h - 3):
                    w.set(x, y, z, *st.frame)
                else:
                    w.set(x, y, z, *st.face)
            if i in pilasters and beams:
                beam(w, s, x, z, axis, top, st)
    if st.border:
        for x in range(s.x0, s.x1 + 1):
            for z in range(s.z0, s.z1 + 1):
                if (x in (s.x0, s.x1) or z in (s.z0, s.z1)) and solid(w, x, s.feet - 1, z) \
                        and not solid(w, x, s.feet, z):
                    w.set(x, s.feet - 1, z, *st.border)


def beam(w, s, x, z, axis, y, st):
    """A beam across the ceiling from the pilaster at (x, z), through the room's air."""
    block = st.beams or (st.beam_z if axis == "z" else st.beam_x)
    if axis == "z":
        for zz in range(s.z0, s.z1 + 1):
            if w.id(x, y, zz) == B.AIR:
                w.set(x, y, zz, *block)
    else:
        for xx in range(s.x0, s.x1 + 1):
            if w.id(xx, y, z) == B.AIR:
                w.set(xx, y, z, *block)


def build(w):
    for s in P.SPACES:
        st = STYLES.get(s.name)
        if st is not None:
            dress(w, s, st)
