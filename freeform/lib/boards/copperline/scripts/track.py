"""PGM's payload Track, line for line, over a dict of rails: {(x, y, z): data}.

PGM builds a payload's track once, when the match loads: from the rail at the payload's `location` it follows
connected rails until the next block, and the block under it, hold none. It reads only each rail's data, never
whether two rails actually join, so a rail that merely stands where the line would go next is taken as part of
it. A bad track is not an error at load; it is a cart that stops short or runs on into the next leg. Tracing
here, with the same rules, is how a leg's length and end are known before anything is built — and, given the
built world's rails, after.

    faces: N is -z, S is +z, E is +x, W is -x
    data:  0 N-S, 1 E-W, 2..5 ascending E, W, N, S, 6 S-E, 7 S-W, 8 N-W, 9 N-E
"""
STEP = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}
# RailDirection, in data order: (kind, forwards' previous face, forwards' next face)
DIRECTIONS = [("straight", "N", "S"), ("straight", "W", "E"),
              ("slope", "W", "E"), ("slope", "E", "W"), ("slope", "S", "N"), ("slope", "N", "S"),
              ("curve", "S", "E"), ("curve", "S", "W"), ("curve", "N", "W"), ("curve", "N", "E")]


class Offset:
    """A RailOffset: which way a rail is being run, and whether it is a slope run upward."""

    def __init__(self, data, forwards):
        kind, prev, nxt = DIRECTIONS[data]
        self.data, self.forwards = data, forwards
        self.up = kind == "slope" and forwards          # SlopedRail's own getNextRail; reversed it is default
        self.prev, self.next = (prev, nxt) if forwards else (nxt, prev)

    def reverse(self):
        return Offset(self.data, not self.forwards)

    def next_rail(self, rails, pos):
        x, y, z = pos
        dx, dz = STEP[self.next]
        if self.up:
            return (x + dx, y + 1, z + dz)
        n = (x + dx, y, z + dz)
        return n if n in rails else (x + dx, y - 1, z + dz)


def of(rails, pos, previous):
    d = rails.get(pos)
    if d is None:
        return None
    if not 0 <= d <= 9:
        raise ValueError(f"Invalid rail metadata: {d} @ {pos}")
    f = Offset(d, True)
    if previous is None:
        return f
    return f if OPP[previous] == f.prev else f.reverse()


def trace(rails, start, limit=10000):
    """The positions PGM's Track holds for a payload at `start`, in order."""
    off = of(rails, start, None)
    if off is None:
        raise ValueError(f"Start must be a rail @ {start}")
    if off.next_rail(rails, start) not in rails:
        off = off.reverse()
    out, pos = [], start
    while off is not None:
        out.append(pos)
        if len(out) > limit:
            raise ValueError(f"the track from {start} does not end: a loop")
        pos2 = off.next_rail(rails, pos)
        off = of(rails, pos2, off.next)
        pos = pos2
    return out
