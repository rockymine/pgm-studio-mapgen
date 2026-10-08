"""Solids: the repository's own `tools/sculpt/solid.py`, and what a freeform board needs on top of it.

    from pgmvox import solid as S
    vase = S.revolve([(3, 0), (4, 3), (2, 6), (3, 9)], 0.5, 0.5, 40)
    S.fill(w, S.shell(vase) - S.box(-1, 1, 40, 41, -5, 5), (B.QUARTZ, 0))
    S.fill(w, S.image(vase, Symmetry("half")), (B.QUARTZ, 0))

**There is one solid module in this repository, and this is not a second.** A solid there is a membership test
over block centres and the box it can occupy, with unions, differences, shells, turns and two dozen primitives
(boxes, ellipsoids, cylinders, frustums, tori, beams, prisms, revolves, extrusions, tubes, sheets). This module
loads that file and re-exports all of it, so a fix there reaches every board here.

What it adds is the freeform side: `fill` writes a solid into a `World` with a block or a paint function, and
`image` carries a solid through a plan `Symmetry`, so a sculpture is drawn once and its other half follows.
"""
import importlib.util
import os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "sculpt", "solid.py")
_spec = importlib.util.spec_from_file_location("pgmvox._sculpt_solid", _PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

Solid = _mod.Solid
for _name in dir(_mod):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_mod, _name)


def fill(w, solid, block, only_air=False):
    """Write a solid into a World. block is (id, data) or a function (x, y, z) -> (id, data) or None; with
    only_air, nothing already standing is overwritten. Returns how many blocks were written."""
    paint = block if callable(block) else (lambda x, y, z: block)
    n = 0
    for x, y, z in solid.cells():
        if not w.inside(x, y, z) or (only_air and w.id(x, y, z) != 0):
            continue
        b = paint(x, y, z)
        if b is not None:
            w.set(x, y, z, *b)
            n += 1
    return n


def image(solid, symmetry):
    """The solid carried through a plan Symmetry ("half", "mirror_x", "mirror_z" about its axis), so the second
    half of a symmetric board's sculpture is the first one's image, block for block."""
    ax, az = symmetry.axis
    # the axis is in block indices (-0.5 is the seam between -1 and 0); in centre coordinates it is a + 0.5
    cx, cz = ax + 0.5, az + 0.5
    if symmetry.op == "mirror_x":
        return _mod.mirror_x(solid, cx)
    if symmetry.op == "mirror_z":
        return _mod.mirror_z(solid, cz)
    return _mod.mirror_z(_mod.mirror_x(solid, cx), cz)          # a half turn is both mirrors


def turned(solid, degrees, cx, cz):
    """The solid turned about the vertical through (cx, cz), any angle: `rotate_y` under the library's name."""
    return _mod.rotate_y(solid, degrees, cx, cz)


def count(solid):
    return len(solid.cells())


__all__ = [n for n in dir(_mod) if not n.startswith("_")] + ["fill", "image", "turned", "count"]
