"""pgmvox: the shared library for freeform PGM boards — blocks, orientation, the world, terrain, shapes, the
1.8 movement physics, plan walks and checks, sketches, renders and the reads of a built world.

Import it by path from a board's scripts:

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
    from pgmvox import B, World

A board records the version it was built with (pgmvox.VERSION) in its build log, since the library moves.
"""
VERSION = "0.5.0"

from .blocks import B, DYE  # noqa: E402,F401
from .world import World, rng, seed  # noqa: E402,F401
