"""The chunk showcase: every chunk in `chunks/` on one board, each a 16 x 16 column standing out of a sea.

    python3 specs/chunk-showcase/build-spec.py <out-dir> [world-dir] [--only name,name]

Chunks sit on chunk boundaries, a chunk apart, joined by plank bridges at their own surface height, with a spawn
platform south of the grid (`board_builder.py`).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board_builder    # noqa: E402
import chunks           # noqa: E402

if __name__ == "__main__":
    board_builder.run(sys.argv[1:], chunks.ALL, "chunk-showcase", "Chunk Showcase", size=16, step=32,
                      test_prefix="chunk-test-")
