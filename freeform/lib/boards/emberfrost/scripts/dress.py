"""Everything that stands on or is cut into red's half, in the order it is laid; gen.py then turns it onto blue's."""
import numpy as np

import details
import extras
import forge
import paths
import plan as P
import rime
import spans
import util
import village
import wood
from pgmvox import rng


def everything(w, deg, ice, fire, bottom, O, stats):
    util.reset_claims()
    paths.lay(w, rng(P.BOARD, "roads"), stats)
    rime.build(w, rng(P.BOARD, "rime"), stats)
    forge.build(w, rng(P.BOARD, "forge"), stats)
    spans.build(w, rng(P.BOARD, "spans"), stats)
    # the ground an objective keeps bare: seven blocks round each core, and each plaza whole
    util.claim_disc(*P.RIME, 13)
    util.claim_disc(*P.FORGE, 15)
    util.claim_cells([(x, z) for x in range(-46, -34) for z in range(-24, -1)])
    util.claim_cells([(x, z) for x in range(-5, 6) for z in range(-24, -1)])
    util.claim_cells([(x, z) for x in range(36, 46) for z in range(-24, -1)])
    village.build(w, rng(P.BOARD, "village"), stats)
    extras.build(w, rng(P.BOARD, "extras"), stats)
    placed = wood.plant_woods(w, deg, ice, fire, rng(P.BOARD, "wood"), stats)
    wood.dead_trees(w, deg, fire, rng(P.BOARD, "dead"), stats)
    details.falls(w, rng(P.BOARD, "falls"), stats)
    details.litter(w, placed, rng(P.BOARD, "litter"), stats)
    details.embers(w, fire, deg, rng(P.BOARD, "embers"), stats)
    details.lamps_on_roads(w, stats)
    details.frost(w, ice, rng(P.BOARD, "frost"), stats)
