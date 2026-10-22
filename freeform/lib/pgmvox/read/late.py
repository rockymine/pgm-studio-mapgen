"""How a board holds up as a match goes on: the walk to a goal in the four phases a long capture or destroy match
passes through, and whether the goal's door still decides anything in each.

    got = phases(w, start, goal, zone, max_y, door=cells, breakable=ids)
    got["ground"], got["bridged"], got["sky"], got["dug"]          # moves, or None where not reached
    got["door"]                                                     # phase -> True where walling the door shuts it

**A match leaves its board in four phases, and a board is read in all four** (`pgm-studio/docs/gameplay/
match-flow.md` §4). First the ground as built, walked. Then the build zone bridged. Then the sky: every column
that is not void may be built on to the build height, so the late game's skybridge network is the projection of
land and zone onto the ceiling (§5). Last the ground itself dug away, every block a player may break taken out:
the pit in front of a wall and the desert of the middle, at their limit.

**A door holds where walling it shuts the goal off.** The cells given as `door` are made bedrock and the phase is
walked again; a goal still reached is one the late game goes round its door to. A board whose doors hold in the
sky and dug phases is one whose approaches the players cannot rebuild around.

**What may be broken is the board's rule, not a guess.** `breakable` is the set of block ids a player may break;
CTW's default is everything but bedrock, a board that lets only its kit be broken passes the kit's blocks, which
are none of the ground's.
"""
import numpy as np

from pgmvox.core.blocks import B
from pgmvox.read.walk import MoveRules, nearest, walk

EVERYTHING = None                                   # every block but bedrock, barrier and the void's own air


def _dig(ids, breakable):
    out = ids.copy()
    if breakable is EVERYTHING:
        m = (out != 0) & (out != B.BEDROCK) & (out != B.BARRIER)
    else:
        m = np.isin(out, list(breakable))
    m[:, 0, :] &= False                              # the floor of the world stays, or every column were void
    out[m] = 0
    return out


def phases(w, start, goal, zone, max_y, door=(), breakable=EVERYTHING, r=2, low=1):
    """The moves from `start` to within `r` of `goal` (feet) in the four phases, and for each whether walling the
    cells `door` shuts the goal off. `zone` is the build zone over the world's columns, `max_y` the build height."""
    land = w.ids[:, 0, :] != 0
    foot = MoveRules(max_drop=3, jumps=False)
    rules = {"ground": foot,
             "bridged": MoveRules(max_drop=3, jumps=False, build=(zone, (low, max_y))),
             "sky": MoveRules(max_drop=3, jumps=False, build=(zone | land, (low, max_y))),
             "dug": MoveRules(max_drop=3, jumps=False, build=(zone | land, (low, max_y)))}
    dug = _dig(w.ids, breakable)
    out, held = {}, {}
    for name, rule in rules.items():
        ids = dug if name == "dug" else w.ids
        d = walk(ids, [start], w.x0, w.z0, rule)
        out[name] = nearest(d, w.x0, w.z0, *goal, r=r)
        if door:
            shut = ids.copy()
            for x, y, z in door:
                if 0 <= x - w.x0 < w.sx and 0 <= z - w.z0 < w.sz:
                    shut[x - w.x0, y, z - w.z0] = B.BEDROCK
            d2 = walk(shut, [start], w.x0, w.z0, rule)
            held[name] = None if out[name] is None else nearest(d2, w.x0, w.z0, *goal, r=r) is None
    out["door"] = held
    return out


def table(rows):
    """Readings as text: one line a goal and rule set, each phase's moves and whether its door holds."""
    lines = [f"{'':34} {'ground':>8} {'bridged':>8} {'sky':>8} {'dug':>8}   door holds in"]
    for name, got in rows:
        held = [p for p in ("ground", "bridged", "sky", "dug") if got["door"].get(p)]
        cells = [f"{got[p] if got[p] is not None else '-':>8}" for p in ("ground", "bridged", "sky", "dug")]
        lines.append(f"{name:34} {' '.join(cells)}   {', '.join(held) or 'none'}")
    return "\n".join(lines)
