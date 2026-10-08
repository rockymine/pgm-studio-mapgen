"""Curio Square — a hide-and-seek plan after the community's Hide n' Seek maps: a walled square of forty-eight plots,
eleven blocks a side with three-block streets between them, round a fountain in the middle. Three builders share
the plots, sixteen each, so that no two plots side by side across a street are by the same hand.

    the street is at y 64; plots draw from y 63 (their ground) to y 87
"""
STREET_Y = 64
N = 7                                                            # plots a side
PLOT = 11
STREET = 3
STEP = PLOT + STREET
CENTRE = (3, 3)                                                  # the fountain, not a plot
RIM = 4                                                          # the street round the outside of the grid
HALF = (N * PLOT + (N - 1) * STREET) // 2 + RIM                  # the square runs from -HALF to HALF
WALL = HALF + 1
BUILDERS = ("opus", "haiku", "sonnet")
SEED = 11                                                        # the shuffle that places each builder's plots

RELEASE = 25                                                     # seconds the seekers wait, blinded
ROUNDS = [85 + 60 * k for k in range(6)]                         # seconds into the match six plots vanish
PER_ROUND = 6
TIME = "7m"


def origin(i, j):
    """The north-west corner of plot (row i, column j), in world x and z."""
    return -PLOT // 2 + STEP * (j - N // 2), -PLOT // 2 + STEP * (i - N // 2)


def builder(i, j):
    """Whose plot: neighbours across a street, row or column, are never the same builder."""
    return BUILDERS[(i + 2 * j) % 3]


def plots():
    return [(i, j) for i in range(N) for j in range(N) if (i, j) != CENTRE]
