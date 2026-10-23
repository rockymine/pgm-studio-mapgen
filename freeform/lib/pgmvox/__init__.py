"""pgmvox: the shared library for freeform PGM boards — blocks, orientation, the world, terrain, shapes, the
1.8 movement physics, plan walks and checks, sketches, renders and the reads of a built world.

It is an installed package. Install it once per machine, editable, so the checkout is what is imported:

    python3 -m pip install -e freeform/lib

and a board's scripts import it as any package, from wherever they run:

    from pgmvox import B, World

A board records the version it was built with (pgmvox.VERSION) in its build log, since the library moves.
"""
VERSION = "0.30.0"

from pgmvox.core.blocks import B, DYE  # noqa: E402,F401
from pgmvox.core.world import World, rng, seed  # noqa: E402,F401
