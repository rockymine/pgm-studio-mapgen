"""Scratch: one mass per pattern, side by side, to look at the facade system before the city uses it."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mc import World, B
import facade as Fa
import render_iso
w = World(-60, -20, 60, 40, sy=40)
O = (B.STAINED_CLAY, 1); K = (B.STAINED_CLAY, 15); L = (B.STAINED_CLAY, 8)
specs = [
    ((-58, -8, -48, 4), [Fa.band(3, 3, O), Fa.flutes(3, 1, 5, 12)], "cornice", "inset band and flutes"),
    ((-44, -8, -34, 4), [Fa.glyph_row(4, ["eye", "step", "key", "cross"], K), Fa.courses(4, Fa.DARK_CONCRETE)], "parapet", "glyphs"),
    ((-30, -8, -20, 4), [Fa.panels(3, 1, 13, L), Fa.band_from_top(1, 1, O)], "parapet-slotted", "panels"),
    ((-16, -8, -6, 4), [Fa.slits(3, 2, 12), Fa.checker(0, 0, K)], "cornice", "slits"),
]
for (x0, z0, x1, z1), faces, top, name in specs:
    m = Fa.Mass(Fa.rect_cells(x0, z0, x1, z1), 20, 34)
    Fa.build(w, m, base=Fa.concrete(), faces=faces, top=top, bottom="coffer")
w.save("/tmp/facade-test", "t", (0, 10, 0))
x0, z0, ids, dat = render_iso.load("/tmp/facade-test")
render_iso.render(ids, dat, x0, z0, sys.argv[1], 7, "se")
render_iso.render(ids, dat, x0, z0, sys.argv[2], 7, "nw")
