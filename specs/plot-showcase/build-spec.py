"""The plot showcase: the chunk showcase's twelve points of interest given room — each a 32 x 32 plot of four
chunks, with the same things on it laid out with space between them and relief under them.

    python3 specs/plot-showcase/build-spec.py <out-dir> [world-dir] [--only name,name]

Plots sit on chunk boundaries, half a plot apart, joined by plank bridges at their surface height, with a spawn
platform south of the grid. The board, the kit and the tree registry are the chunk showcase's.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "chunk-showcase"))
import board_builder    # noqa: E402
import plots            # noqa: E402

if __name__ == "__main__":
    board_builder.run(sys.argv[1:], plots.ALL, "plot-showcase", "Plot Showcase", size=32, step=48,
                      test_prefix="plot-test-")
