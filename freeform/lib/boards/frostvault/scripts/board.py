"""Frostvault's plan and its blocks, for every script to share.

    plan()          the bunker plan drawn from the composed board
    laid()          where everything stands once laid, read without building a world
"""
import layout as L
from pgmvox.built import bunker as BB
from pgmvox.plan import bunker as PB


def plan():
    return PB.draw(PB.load(L.COMPOSED), gap=L.GAP, moat=L.MOAT, cut=L.CUT)


class _Nowhere:
    """A world that keeps nothing: laying into it says where things go."""

    def set(self, *a):
        pass

    def column(self, *a):
        pass

    def id(self, *a):
        return 0


def laid(b=None):
    return BB.lay(_Nowhere(), b or plan(), L.H)
